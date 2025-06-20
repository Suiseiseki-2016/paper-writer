import yaml
from pathlib import Path
from typing import Dict, Optional

def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Optional path to the config.yaml file. If not provided, will look for config.yaml in the project root.
        
    Returns:
        Dict containing the configuration values.
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    if config_path is None:
        # Look for config.yaml file in the project root
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / 'config.yaml'
    
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return config if config is not None else {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing config file: {e}")
