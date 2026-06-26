from pathlib import Path
from pxr import Usd

def run_default_prim_check(asset_file_path: Path) -> list:
    stage = Usd.Stage.Open(asset_file_path) # type: ignore
    errors = []
    if not stage.HasDefaultPrim():
        error_result = {
            "root_path": str(asset_file_path),
            "check_name": "default_prim",
            "severity": None,       # set in runner by config
            "error": "MISSING_DEFAULT_PRIM",
            "message": f"No default prim is declared in {asset_file_path}",
            "detail": {}
        }
        errors.append(error_result)

    return errors