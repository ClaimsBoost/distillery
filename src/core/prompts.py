"""
Simplified prompt management system using markdown files
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class PromptTemplates:
    """Loads and manages prompts from markdown files"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize prompt templates
        
        Args:
            prompts_dir: Directory containing prompt markdown files
        """
        self.prompts_dir = Path(prompts_dir)
        self._cache = {}
        
        # Schema is now handled directly by Ollama API, not in prompts
    
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
    
    def _load_json(self, relative_path: str) -> Dict[str, Any]:
        """
        Load JSON content from a file
        
        Args:
            relative_path: Path relative to prompts directory
        
        Returns:
            Parsed JSON content
        """
        content = self._load_file(relative_path)
        return json.loads(content)
    
    def get_system_prompt(self) -> str:
        """
        Get the base system prompt
        
        Returns:
            System prompt text
        """
        return self._load_file("system/base.md")
    
    def get_office_extraction_prompt(self, content: str) -> str:
        """
        Generate prompt for office location extraction
        
        Args:
            content: The text content to extract from
        
        Returns:
            Formatted extraction prompt
        """
        # Load the base extraction prompt
        prompt_template = self._load_file("extraction/office_locations.md")
        
        # Format the prompt with content
        prompt = prompt_template.replace("{content}", content)
        
        return prompt
    
    def extract_offices_from_chunks(self, chunks: List[str]) -> str:
        """
        Generate extraction prompt from multiple text chunks
        
        Args:
            chunks: List of text chunks from RAG retrieval
        
        Returns:
            Complete prompt for extraction
        """
        # Combine chunks with separators
        combined_content = "\n---\n".join(chunks)
        
        # Get system and extraction prompts
        system_prompt = self.get_system_prompt()
        extraction_prompt = self.get_office_extraction_prompt(combined_content)
        
        # Combine them
        return f"{system_prompt}\n\n{extraction_prompt}"
    
    def validate_extraction(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted data against schema (simplified string array format)
        
        Args:
            extracted_data: The extracted JSON data
        
        Returns:
            Validation results with any errors found
        """
        errors = []
        warnings = []
        
        # Check if offices key exists
        if "offices" not in extracted_data:
            errors.append("Missing 'offices' key in extracted data")
            return {"valid": False, "errors": errors, "warnings": warnings}
        
        offices = extracted_data["offices"]
        
        # Check if offices is a list
        if not isinstance(offices, list):
            errors.append(f"'offices' must be a list, got {type(offices).__name__}")
            return {"valid": False, "errors": errors, "warnings": warnings}
        
        # Validate each office (now just strings)
        valid_offices = []
        for i, office in enumerate(offices):
            # Check if office is a string
            if not isinstance(office, str):
                errors.append(f"Office {i}: Must be a string, got {type(office).__name__}")
                continue
            
            # Check if it's not empty or just whitespace
            if not office or not office.strip():
                warnings.append(f"Office {i}: Empty or whitespace-only string")
                continue
            
            # Check for placeholder text
            if office.lower() in ["string", "address", "office address", "n/a", "none"]:
                warnings.append(f"Office {i}: Appears to be placeholder text")
                continue
            
            valid_offices.append(office)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "office_count": len(valid_offices),
            "total_offices": len(offices)
        }
    
    def fix_extraction_structure(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to fix common structural issues in extracted data (string array format)
        
        Args:
            extracted_data: The extracted JSON data
        
        Returns:
            Fixed data structure
        """
        if "offices" not in extracted_data:
            return {"offices": []}
        
        offices = extracted_data["offices"]
        
        # Handle if offices is not a list
        if not isinstance(offices, list):
            # Try to convert to list if it's a single string
            if isinstance(offices, str):
                offices = [offices]
            else:
                return {"offices": []}
        
        fixed_offices = []
        for office in offices:
            # Handle dict format (old structure) by converting to string
            if isinstance(office, dict):
                if "address" in office and isinstance(office["address"], dict):
                    addr = office["address"]
                    # Combine address fields into a single string
                    parts = []
                    if addr.get("street"):
                        parts.append(addr["street"])
                    if addr.get("city"):
                        parts.append(addr["city"])
                    if addr.get("state") and addr.get("zip"):
                        parts.append(f"{addr['state']} {addr['zip']}")
                    elif addr.get("state"):
                        parts.append(addr["state"])
                    elif addr.get("zip"):
                        parts.append(addr["zip"])
                    
                    if parts:
                        office_str = " ".join(parts)
                        fixed_offices.append(office_str)
                elif "street" in office:  # Flat structure
                    parts = []
                    if office.get("street"):
                        parts.append(office["street"])
                    if office.get("city"):
                        parts.append(office["city"])
                    if office.get("state") and office.get("zip"):
                        parts.append(f"{office['state']} {office['zip']}")
                    elif office.get("state"):
                        parts.append(office["state"])
                    elif office.get("zip"):
                        parts.append(office["zip"])
                    
                    if parts:
                        office_str = " ".join(parts)
                        fixed_offices.append(office_str)
            elif isinstance(office, str):
                # Already a string, just validate it's not empty
                if office and office.strip() and office.lower() not in ["string", "address", "none", "n/a"]:
                    fixed_offices.append(office.strip())
        
        return {"offices": fixed_offices}
    
    def reload_prompts(self):
        """Clear cache to reload prompts from disk"""
        self._cache.clear()