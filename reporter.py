import json

from pathlib import Path
from rich.console import Console
from rich.text import Text


console = Console()

def report(asset_dir: Path, validation_results: list, file_count: int, out_path: Path | None = None) -> None:
    if out_path:
        with open(out_path, "w") as file:
            json.dump(validation_results, file, indent=4)

    if not validation_results:
        text = Text()
        text.append("0 issues found. ", style="bold green")
        text.append(str(file_count), style="bold yellow")
        text.append(" files scanned in ", style="dim white")
        text.append(str(asset_dir), style="dim white")
        console.print(text)
        return

    # Sort results by error and then check name ascending
    priority = {"WARNING": 0, "ERROR": 1}
    sorted_results = sorted(validation_results, key=lambda x: (priority[x["severity"]], x["check_name"]))

    for res in sorted_results:
        text = Text()
        text.append(f"{res['root_path']}  ", style="cyan")
        if res["severity"] == "ERROR":
            text.append(f"{res['severity']}", style="bold white on red")
            text.append(f"   {res['error']}", style="bold red")
        elif res["severity"] == "WARNING":
            text.append(f"{res['severity']}", style="bold black on yellow")
            text.append(f"   {res['error']}  ", style="bold yellow")
        if res["detail"]:
            (key, value), = res["detail"].items()
            text.append(f"   {value}", style="magenta")
        console.print(text)
    
    text = Text()
    text.append(f"--------------------------------------------------------------------------------------\n")
    text.append(f"{len(sorted_results)} issues found. ", style="bold red")
    text.append(str(file_count), style="bold yellow")
    text.append(" files scanned in ", style="dim white")
    text.append(str(asset_dir), style="dim white")
    console.print(text)

    return

if __name__ == "__main__":
    path = Path("/Users/ianhenderson/Documents/USD-Validator/checks")
    report(path, [], 5)

    errors = [
        {
            "root_path": "usd/tutorials/referencingLayers/RefExample.usda",
            "check_name": "references",
            "severity": "ERROR",
            "error": "UNRESOLVED_REFERENCE",
            "message": "Could not load asset refenced by ...",
            "detail": {"unresolved_path": "./HelloWorld_MISSING.usda"}
        },
        {
            "root_path": "/prod/assets/SQ040/char_body_geo_v001.usda",
            "check_name": "default_prim",
            "severity": "ERROR",
            "error": "MISSING_DEFAULT_PRIM",
            "message": "No defaultPrim declared in char_body_geo_v001.usda",
            "detail": {}
        },
        {
            "root_path": "/prod/assets/SQ040/char_body_geo_v001.usda",
            "check_name": "naming",
            "severity": "WARNING",
            "error": "PRIM_NAME_STYLE_VIOLATION",
            "message": "The prim name char_body_geo violates prim name style guidelines.",
            "detail": {"prim_path": "char_body_geo_v001.usda"}
        }
    ]
    report(path, errors, 5)
