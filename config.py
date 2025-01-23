import json
from pathlib import Path
from typing import Dict

from openai import AsyncOpenAI


def read_config() -> Dict[str, str]:
    """Reads the model config from the json config file.

    Returns:
        Dict[str, str]: The model config read in from disk.
    """
    current_dir = Path(__file__).parent
    with open(current_dir / "config.json") as f:
        config = json.load(f)
    return config


CONFIG = read_config()

MODEL_CLIENT = AsyncOpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")
