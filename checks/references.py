from pathlib import Path
from pxr import UsdUtils

def run_references_check(asset_filepath: Path) -> list:
    filepath_str = str(asset_filepath)
    ref_errors = []
    layers, assets, unresolved = UsdUtils.ComputeAllDependencies(filepath_str) # type: ignore
    for filepath in unresolved:
        error_result = {
            "root_path": filepath_str,
            "check_name": "references",
            "severity": None,   # set in runner by config
            "error": "UNRESOLVED_REFERENCE",
            "message": f"Unresolved references found while scanning dependencies at {filepath_str}",
            "detail":{"unresolved_path": filepath}
        }
        ref_errors.append(error_result)
    return ref_errors