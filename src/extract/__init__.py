"""Extractors for law firm data"""
from .base_extractor import BaseExtractor
from .office_extractor import OfficeExtractor

# Keep RAGPipeline as alias for backward compatibility
RAGPipeline = OfficeExtractor

__all__ = [
    'BaseExtractor',
    'OfficeExtractor',
    'RAGPipeline'  # Backward compatibility
]