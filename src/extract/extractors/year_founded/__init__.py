"""year_founded extractor module"""
from ...extractor_factory import create_extractor_class

YearFoundedExtractor = create_extractor_class('year_founded')

__all__ = ['YearFoundedExtractor']
