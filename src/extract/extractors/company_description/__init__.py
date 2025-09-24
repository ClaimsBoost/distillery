"""company_description extractor module"""
from ...extractor_factory import create_extractor_class

CompanyDescriptionExtractor = create_extractor_class('company_description')

__all__ = ['CompanyDescriptionExtractor']
