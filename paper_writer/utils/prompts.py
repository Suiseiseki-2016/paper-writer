import os
from pathlib import Path
from typing import Dict

class PromptLoader:
    """Load prompts from the prompts/ directory."""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize the prompt loader.
        
        Args:
            prompts_dir: Path to the prompts directory
        """
        self.prompts_dir = Path(prompts_dir)
        self.prompts: Dict[str, str] = {}
        self._load_prompts()
    
    def _load_prompts(self) -> None:
        """Load all prompt files from the prompts directory."""
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found: {self.prompts_dir}")
        
        for file_path in self.prompts_dir.glob("*.md"):
            prompt_name = file_path.stem  # Get filename without extension
            with open(file_path, 'r', encoding='utf-8') as f:
                self.prompts[prompt_name] = f.read().strip()
    
    def get_prompt(self, name: str) -> str:
        """
        Get a specific prompt by name.
        
        Args:
            name: Name of the prompt (filename without extension)
            
        Returns:
            The prompt content
            
        Raises:
            KeyError: If prompt not found
        """
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found. Available prompts: {list(self.prompts.keys())}")
        return self.prompts[name]
    
    def format_prompt(self, name: str, **kwargs) -> str:
        """
        Get and format a prompt with the given parameters.
        
        Args:
            name: Name of the prompt
            **kwargs: Parameters to format the prompt with
            
        Returns:
            Formatted prompt content
        """
        prompt = self.get_prompt(name)
        return prompt.format(**kwargs)
    
    def list_prompts(self) -> list:
        """Get a list of all available prompt names."""
        return list(self.prompts.keys())

# Create a global instance
prompt_loader = PromptLoader()

# Create individual variables for each prompt
DESCRIPTION_PROMPT = prompt_loader.get_prompt("description")
OUTLINE_PROMPT = prompt_loader.get_prompt("outline")
CITATIONS_PROMPT = prompt_loader.get_prompt("citations")

# Convenience functions
def get_prompt(name: str) -> str:
    """Get a prompt by name."""
    return prompt_loader.get_prompt(name)

def format_prompt(name: str, **kwargs) -> str:
    """Format a prompt with parameters."""
    return prompt_loader.format_prompt(name, **kwargs)

def list_prompts() -> list:
    """List all available prompts."""
    return prompt_loader.list_prompts()
