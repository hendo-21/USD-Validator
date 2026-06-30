import re

from pxr import Usd, Tf
from pathlib import Path

def run_naming_check(asset_filepath: Path, naming_conventions: dict) -> list:
    errors = []

    check_root_res = _check_root(asset_filepath, naming_conventions["file_pattern"])
    check_prims_res = _check_prims(asset_filepath, naming_conventions["prim_patterns"])

    for lst in [check_root_res, check_prims_res]:
        errors.extend(lst)

    return errors

def _check_root(asset_filepath: Path, regex_str: str) -> list:
    errors = []
    filepath_str = str(asset_filepath)
    match_res = re.fullmatch(regex_str, asset_filepath.name)
    if not match_res:
        error_result = {
            "root_path": filepath_str,
            "check_name": "naming",
            "severity": None,       # set in runner by config
            "error": "FILENAME_STYLE_VIOLATION",
            "message": f"The file name {asset_filepath.name} violates filename style guidelines.",
            "detail": {"violation_path": filepath_str}
        }
        errors.append(error_result)
    return errors

def _check_prims(asset_filepath: Path, prim_patterns: dict) -> list:
    errors = []
    filepath_str = str(asset_filepath)

    try:
        stage = Usd.Stage.Open(filepath_str)    # type: ignore
    except Tf.ErrorException:
        return [{
            "root_path": filepath_str,
            "check_name": "naming",
            "severity": None,       # set in runner by config
            "error": "STAGE_OPEN_FAILED",
            "message": f"Could not open or parse {asset_filepath}. Validation skipped.",
            "detail": {}
        }]

    for prim in stage.Traverse():
        pname, ptype = prim.GetName(), prim.GetTypeName().lower()
        if ptype in prim_patterns:
            if not pname.endswith(prim_patterns[ptype]):
                error_result = {
                    "root_path": filepath_str,
                    "check_name": "naming",
                    "severity": None,       # set in runner by config
                    "error": "PRIM_NAME_STYLE_VIOLATION",
                    "message": f"The prim name {pname} violates prim name style guidelines.",
                    "detail": {"prim_path": prim.GetPath().pathString}
                }
                errors.append(error_result)

    return errors