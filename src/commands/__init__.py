"""
Command handlers for the CLI application
"""

from .embed_command import EmbedCommand
from .extract_command import ExtractCommand
from .test_command import TestCommand

__all__ = [
    'EmbedCommand',
    'ExtractCommand',
    'TestCommand'
]