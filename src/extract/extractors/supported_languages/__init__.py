"""supported_languages extractor module"""
from ...extractor_factory import create_extractor_class

SupportedLanguagesExtractor = create_extractor_class('supported_languages')

__all__ = ['SupportedLanguagesExtractor']