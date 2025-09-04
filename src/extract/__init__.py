"""Extractors for law firm data"""
from .base_extractor import BaseExtractor
from .office_extractor import OfficeExtractor
from .law_firm_confirmation_extractor import LawFirmConfirmationExtractor

# Keep RAGPipeline as alias for backward compatibility
RAGPipeline = OfficeExtractor

__all__ = [
    'BaseExtractor',
    'OfficeExtractor',
    'LawFirmConfirmationExtractor',
    'RAGPipeline'  # Backward compatibility
]