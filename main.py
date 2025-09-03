#!/usr/bin/env python3
"""
Simplified main orchestrator for law firm data extraction system
Uses modular command handlers for cleaner architecture
"""

import argparse
import json
import logging
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

from supabase import create_client
from src.core.config_manager import ExtractionConfig
from src.commands import EmbedCommand, ExtractCommand, TestCommand

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Application:
    """Simplified main application"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize application with configuration"""
        self.app_config = self._load_config(config_file)
        self.supabase_client = self._init_supabase()
    
    def _load_config(self, config_file: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if config_file is None:
            env = os.environ.get('ENVIRONMENT', 'local')
            config_file = f'config/config.{env}.json'
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found")
            return {}
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            return {}
    
    def _init_supabase(self):
        """Initialize Supabase client if credentials available"""
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        
        if url and key:
            return create_client(url, key)
        
        logger.warning("Supabase credentials not found")
        return None
    
    def _get_extraction_config(self, override_params: Optional[Dict] = None) -> ExtractionConfig:
        """Get extraction configuration"""
        if override_params:
            return ExtractionConfig(**override_params)
        
        if self.app_config and 'extraction' in self.app_config:
            params = self.app_config['extraction'].copy()
            
            # Add Ollama URL if present
            if 'ollama' in self.app_config:
                params['ollama_base_url'] = self.app_config['ollama']['base_url']
            
            return ExtractionConfig(**params)
        
        raise ValueError("No extraction configuration found")
    
    def _get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration"""
        return self.app_config.get('storage', {
            'bucket': 'law-firm-html',
            'base_path': 'markdown'
        })
    
    def handle_embed(self, args):
        """Handle embed command"""
        # Load config
        config = self._get_extraction_config(
            self._load_config_from_file(args.config) if args.config else None
        )
        
        # Create and execute command
        command = EmbedCommand(config, self._get_storage_config())
        results = command.execute(args.targets, is_domain=args.domain, force=args.force)
        command.display_results(results)
    
    def handle_extract(self, args):
        """Handle extract command"""
        # Load config
        config = self._get_extraction_config(
            self._load_config_from_file(args.config) if args.config else None
        )
        
        # Create and execute command
        command = ExtractCommand(config, self.supabase_client)
        results = command.execute(args.targets, args.type, is_domain=args.domain)
        
        # Save or display results
        if args.output:
            command.save_results(results, args.output)
        else:
            command.display_results(results)
    
    def handle_test(self, args):
        """Handle test-domain command"""
        # Load config
        config = self._get_extraction_config(
            self._load_config_from_file(args.config) if args.config else None
        )
        
        # Create and execute command
        command = TestCommand(config, self._get_storage_config(), self.supabase_client)
        result = command.execute(args.domain, re_embed=args.re_embed)
        
        # Save results to evaluation directory with consistent naming
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'evaluation/extraction_test_{args.domain}_{timestamp}.json'
        command.save_results(result, output_file)
    
    def _load_config_from_file(self, config_file: str) -> Optional[Dict]:
        """Load extraction parameters from config file"""
        if not config_file:
            return None
        
        with open(config_file, 'r') as f:
            config_dict = json.load(f)
        
        # Extract extraction parameters
        if 'extraction' in config_dict:
            params = config_dict['extraction']
            if 'ollama' in config_dict:
                params['ollama_base_url'] = config_dict['ollama']['base_url']
            return params
        
        return config_dict


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(description='Law Firm Data Extraction System')
    
    # Global arguments
    parser.add_argument('--env-config', help='Environment config file')
    
    subparsers = parser.add_subparsers(dest='mode', help='Execution mode')
    
    # Embed command
    embed_parser = subparsers.add_parser('embed', help='Embed documents into vector database')
    embed_parser.add_argument('targets', nargs='+', help='File paths or domain names')
    embed_parser.add_argument('--domain', action='store_true', help='Targets are domains')
    embed_parser.add_argument('--force', action='store_true', help='Force re-embedding')
    embed_parser.add_argument('--config', help='Configuration file')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract from embedded documents')
    extract_parser.add_argument('targets', nargs='+', help='Document IDs or domain names')
    extract_parser.add_argument('--type', required=True, help='Extraction type')
    extract_parser.add_argument('--domain', action='store_true', help='Targets are domains')
    extract_parser.add_argument('--output', help='Output file path')
    extract_parser.add_argument('--config', help='Configuration file')
    
    # Test command
    test_parser = subparsers.add_parser('test-domain', help='Test extraction for a domain')
    test_parser.add_argument('domain', help='Domain name')
    test_parser.add_argument('--re-embed', action='store_true', help='Re-embed documents')
    test_parser.add_argument('--config', help='Configuration file')
    
    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # Initialize application
    app = Application(args.env_config)
    
    # Route to appropriate handler
    if args.mode == 'embed':
        app.handle_embed(args)
    elif args.mode == 'extract':
        app.handle_extract(args)
    elif args.mode == 'test-domain':
        app.handle_test(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()