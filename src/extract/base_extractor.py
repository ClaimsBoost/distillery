"""
Base extractor class for all extraction components
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import re
from pathlib import Path


class BaseExtractor(ABC):
    """Abstract base class for all extractors"""
    
    def __init__(self):
        # Schema is now defined in each concrete extractor class
        pass
    
    @abstractmethod
    def extract(self, markdown_content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract structured data from markdown content
        
        Args:
            markdown_content: The markdown text to extract from
            metadata: Optional metadata about the document (URL, source, etc.)
        
        Returns:
            Extracted data matching the schema
        """
        pass
    
    def clean_markdown(self, markdown_content: str) -> str:
        """
        Clean and normalize markdown content
        
        Args:
            markdown_content: Raw markdown text
        
        Returns:
            Cleaned markdown text
        """
        # Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # Remove markdown image tags but keep alt text
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', content)
        
        # Normalize whitespace
        content = ' '.join(content.split())
        
        return content