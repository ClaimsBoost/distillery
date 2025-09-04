"""
Storage handler for accessing markdown documents from Supabase
Uses the Supabase Python client library for storage access
"""

import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from supabase import create_client, Client
import os

logger = logging.getLogger(__name__)


class StorageHandler:
    """Handles storage operations for markdown documents"""
    
    def __init__(self, config: Dict):
        """
        Initialize storage handler
        
        Args:
            config: Storage configuration from YAML
        """
        self.config = config
        self.bucket = config.get('bucket', 'law-firm-html')
        self.base_path = config.get('base_path', 'markdown')
        
        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        
        logger.info(f"Storage handler initialized for bucket: {self.bucket}/{self.base_path}")
    
    def list_domains(self) -> List[str]:
        """
        List all available domains in storage
        
        Returns:
            List of domain names
        """
        try:
            # List folders in the markdown directory
            items = self.client.storage.from_(self.bucket).list(self.base_path)
            
            # Filter for folders (domains)
            domains = []
            for item in items:
                if item.get('id') is None:  # It's a folder
                    domains.append(item['name'])
            
            logger.info(f"Found {len(domains)} domains in storage")
            return sorted(domains)
            
        except Exception as e:
            logger.error(f"Failed to list domains: {e}")
            return []
    
    def list_files_for_domain(self, domain: str) -> List[str]:
        """
        List all markdown files for a specific domain
        
        Args:
            domain: Domain name (e.g., '137law.com')
        
        Returns:
            List of file names
        """
        try:
            path = f"{self.base_path}/{domain}"
            items = self.client.storage.from_(self.bucket).list(path)
            
            # Filter for markdown files
            files = []
            for item in items:
                if item.get('id') and item['name'].endswith('.md'):
                    files.append(item['name'])
            
            logger.info(f"Found {len(files)} markdown files for domain {domain}")
            return sorted(files)
            
        except Exception as e:
            logger.error(f"Failed to list files for domain {domain}: {e}")
            return []
    
    def download_file(self, domain: str, filename: str) -> Optional[str]:
        """
        Download a specific markdown file
        
        Args:
            domain: Domain name
            filename: Markdown filename
        
        Returns:
            File content as string or None if failed
        """
        try:
            path = f"{self.base_path}/{domain}/{filename}"
            
            # Download using Supabase client
            response = self.client.storage.from_(self.bucket).download(path)
            
            if response:
                content = response.decode('utf-8') if isinstance(response, bytes) else str(response)
                logger.info(f"Downloaded {path} ({len(content)} characters)")
                return content
            else:
                logger.error(f"Empty response when downloading {path}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to download {domain}/{filename}: {e}")
            return None
    
    def download_domain_files(self, domain: str, limit: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        Download all markdown files for a domain
        
        Args:
            domain: Domain name
            limit: Optional limit on number of files to download
        
        Returns:
            List of (filename, content) tuples
        """
        files = self.list_files_for_domain(domain)
        
        if limit:
            files = files[:limit]
        
        results = []
        for filename in files:
            content = self.download_file(domain, filename)
            if content:
                results.append((filename, content))
        
        logger.info(f"Downloaded {len(results)} files for domain {domain}")
        return results
    
    def get_sample_domains(self, count: int = 5) -> List[str]:
        """
        Get a sample of domains for testing
        
        Args:
            count: Number of domains to return
        
        Returns:
            List of domain names
        """
        domains = self.list_domains()
        return domains[:count] if domains else []
    
    def get_file_metadata(self, domain: str, filename: str) -> Dict:
        """
        Get metadata for a file
        
        Args:
            domain: Domain name
            filename: File name
        
        Returns:
            Metadata dictionary
        """
        return {
            'domain': domain,
            'filename': filename,
            'path': f"{self.base_path}/{domain}/{filename}",
            'bucket': self.bucket,
            'url': f"https://{domain.replace('_', '.')}/{filename.replace('.md', '')}",
            'storage_path': f"supabase://{self.bucket}/{self.base_path}/{domain}/{filename}"
        }