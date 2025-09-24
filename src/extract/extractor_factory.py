"""Factory for creating extractors from configs"""

from .base_extractor import BaseExtractor
from typing import Type


def create_extractor_class(module_name: str) -> Type[BaseExtractor]:
    """
    Create an extractor class that uses the specified module's config

    Args:
        module_name: Name of the extractor module (e.g., 'office_locations')

    Returns:
        A BaseExtractor subclass configured for the specific extraction type
    """

    class ConfiguredExtractor(BaseExtractor):
        """Dynamically configured extractor"""
        pass

    # Set the module path to point to the extractor module (not config)
    # The _get_config method will convert this to the config path
    ConfiguredExtractor.__module__ = f"src.extract.extractors.{module_name}.extractor"

    # Set a meaningful name for the class
    ConfiguredExtractor.__name__ = f"{module_name.title().replace('_', '')}Extractor"
    ConfiguredExtractor.__qualname__ = ConfiguredExtractor.__name__

    return ConfiguredExtractor