"""contact_info extractor module"""
from ...extractor_factory import create_extractor_class

ContactInfoExtractor = create_extractor_class('contact_info')

__all__ = ['ContactInfoExtractor']
