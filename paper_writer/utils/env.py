import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

def load_env(env_path: Optional[str] = None) -> None:
    """
    Load environment variables from both system environment and .env file.
    
    Args:
        env_path: Optional path to the .env file. If not provided, will look for .env in the project root.
    """
    if env_path is None:
        # Look for .env file in the project root
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / '.env'
    
    # Load environment variables from .env file if it exists
    if os.path.exists(env_path):
        load_dotenv(env_path)
    
    # System environment variables are already loaded and will take precedence
load_env()
env = os.environ