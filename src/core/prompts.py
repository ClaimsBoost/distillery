"""
Simplified prompt management system - only handles system prompts
Individual extractors manage their own prompts
"""

from pathlib import Path


class PromptTemplates:
    """Manages system-level prompts only"""

    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize prompt templates

        Args:
            prompts_dir: Directory containing system prompt files
        """
        self.prompts_dir = Path(prompts_dir)
        self._cache = {}

    def _load_file(self, relative_path: str) -> str:
        """
        Load content from a file in the prompts directory

        Args:
            relative_path: Path relative to prompts directory

        Returns:
            File content as string
        """
        if relative_path in self._cache:
            return self._cache[relative_path]

        file_path = self.prompts_dir / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        content = file_path.read_text()
        self._cache[relative_path] = content
        return content

    def get_system_prompt(self) -> str:
        """
        Get the base system prompt for extraction tasks

        Returns:
            System prompt text
        """
        return self._load_file("system/base.md")