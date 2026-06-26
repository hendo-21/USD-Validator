from pathlib import Path

from checks.default_prim import run_default_prim_check
from checks.naming import run_naming_check
from checks.references import run_references_check
from config import get_severity, get_conventions

CHECKS = {
    "default_prim": run_default_prim_check,
    "references": run_references_check,
    "naming": run_naming_check,
}

def check_runner(asset_dir: Path) -> list:
    naming_conventions = get_conventions()

    results = []
    for usda_file in asset_dir.glob("*.usda"):
        for check_name, check_fn in CHECKS.items():
            check_results = check_fn(usda_file, naming_conventions) if check_name == "naming" else check_fn(usda_file)
            if check_results:
                for result in check_results:
                    results.append(result)

    # Resolve severity on returned results
    for result in results:
        result["severity"] = get_severity(Path(result["root_path"]), result["check_name"])

    return results
