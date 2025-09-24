"""Modular extractors package"""

from pathlib import Path
import importlib
import logging

logger = logging.getLogger(__name__)


def load_extractors():
    """
    Dynamically load all extractors from subdirectories

    Returns:
        Dict of extractor name -> extractor class
    """
    extractors = {}
    extractor_dir = Path(__file__).parent

    for item in extractor_dir.iterdir():
        if item.is_dir() and (item / 'extractor.py').exists():
            module_name = item.name
            try:
                # Import the extractor module
                module = importlib.import_module(f'.{module_name}.extractor', package='src.extract.extractors')

                # Find the extractor class (assumes it ends with 'Extractor')
                for attr_name in dir(module):
                    if attr_name.endswith('Extractor') and attr_name != 'BaseExtractor':
                        extractor_class = getattr(module, attr_name)
                        extractors[module_name] = extractor_class
                        logger.debug(f"Loaded extractor: {module_name} -> {attr_name}")
                        break

            except Exception as e:
                logger.error(f"Failed to load extractor {module_name}: {str(e)}")

    return extractors


# Load all extractors at import time
EXTRACTORS = load_extractors()