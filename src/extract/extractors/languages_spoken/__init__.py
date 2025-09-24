"""languages_spoken extractor module"""
from ...extractor_factory import create_extractor_class

LanguagesSpokenExtractor = create_extractor_class('languages_spoken')

__all__ = ['LanguagesSpokenExtractor']
