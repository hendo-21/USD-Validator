from pathlib import Path
from pxr import Usd

def run_default_prim_check(asset_filepath: Path) -> list:
    filepath_str = str(asset_filepath)
    stage = Usd.Stage.Open(file_path_str) # type: ignore
    errors = []
    if not stage.HasDefaultPrim():
        error_result = {
            "root_path": filepath_str,
            "check_name": "default_prim",
            "severity": None,       # set in runner by config
            "error": "MISSING_DEFAULT_PRIM",
            "message": f"No default prim is declared in {asset_filepath}",
            "detail": {}
        }
        errors.append(error_result)

    return errors