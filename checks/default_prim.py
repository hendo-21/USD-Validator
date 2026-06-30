from pathlib import Path
from pxr import Usd, Tf

def run_default_prim_check(asset_filepath: Path) -> list:
    errors = []
    filepath_str = str(asset_filepath)

    try:
        stage = Usd.Stage.Open(filepath_str)    # type: ignore
    except Tf.ErrorException:
        return [{
            "root_path": filepath_str,
            "check_name": "default_prim",
            "severity": None,       # set in runner by config
            "error": "STAGE_OPEN_FAILED",
            "message": f"Could not open or parse {asset_filepath}. Validation skipped.",
            "detail": {}
        }]

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