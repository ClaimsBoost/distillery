"""office_locations extractor module"""
from ...extractor_factory import create_extractor_class

OfficeLocationsExtractor = create_extractor_class('office_locations')

__all__ = ['OfficeLocationsExtractor']