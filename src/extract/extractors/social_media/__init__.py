"""social_media extractor module"""
from ...extractor_factory import create_extractor_class

SocialMediaExtractor = create_extractor_class('social_media')

__all__ = ['SocialMediaExtractor']
