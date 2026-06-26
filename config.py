import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "pipeline_config.json"

try:
    with open(CONFIG_PATH, "r") as file:
        CONFIG = json.load(file)
except FileNotFoundError as e:
    raise FileNotFoundError (
        f"Pipeline configuration missing at '{CONFIG_PATH}."
        f"Please verify config file exists at validator tool root."
    ) from e

def get_config() -> dict:
    return CONFIG

def get_severity(asset_path: Path, check_name: str) -> str:
    default_severity = CONFIG["checks"][check_name]["default_severity"]
    severity_rules = CONFIG["checks"][check_name]["severity_by_path"]

    for pattern, path_severity in severity_rules.items():
        if asset_path.match(pattern):
            return path_severity
        
    return default_severity

def get_conventions() -> dict:
    return CONFIG["checks"]["naming"]["conventions"]