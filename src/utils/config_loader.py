import yaml
import os
import logging
from typing import Dict,Any

logger = logging.getLogger("QFE")
def load_config(config_file="config/default_config.yaml") -> Dict[Any, Any]:
    if not os.path.exists(config_file):
        logger.error(f"Configuration file not found: {config_file}")
        return {}
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration file loaded: {config_file}")
        return config
    except yaml.YAMLError as exc:
        logger.error(f"Error: {exc}")
        return {}

if __name__ == "__main__":
    config = load_config()
    if config:
        print("cfg:")
        print(config)
        start_date = config.Get("simulation", {}).get("start_date")
        print(f"Start: {start_date}")
    else:
        print("No cfg")