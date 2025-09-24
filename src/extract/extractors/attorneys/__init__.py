"""attorneys extractor module"""
from ...extractor_factory import create_extractor_class

AttorneysExtractor = create_extractor_class('attorneys')

__all__ = ['AttorneysExtractor']
