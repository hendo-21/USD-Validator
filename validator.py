import argparse
import textwrap
import pathlib
import sys

from runner import check_runner
from reporter import report

def create_parser():
    parser = argparse.ArgumentParser(
        prog="USD Asset Validator",
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
            USD Asset Validator helps ensure a shared asset library stays clean.
            It extends the functionality of usdchecker by providing the following checks across
            batches of files, keeping pipeline-breaking errors out of the shared library:

            - Check defaultPrim has been defined
            - Check that all references resolve
            - Check asset names comply with studio naming conventions"""
    ))
    parser.add_argument("asset_dir", type=pathlib.Path, metavar="ASSET_DIR", help="directory containing USD assets to validate")
    parser.add_argument("-o", "--out", default=None, type=pathlib.Path, help="export the validation results to a JSON file at the desired filepath")
    parser.add_argument("-s", "--strict", default=False, action="store_true", help="validator exits with error code 1 if validation failires are found")
    parser.add_argument("-z", "--summarize", default=False, action="store_true", help="add LLM explanation of validation failures to results log")
    return parser

def validate_dir(path):
    if not path.is_dir():
        print(f"{path} is not a valid directory")
        sys.exit(1)

def main():
    parser = create_parser()
    args = parser.parse_args()

    # Validate dirs exist
    validate_dir(args.asset_dir)
    if args.out:
        validate_dir(args.out.parent)

    # Call runner module
    validation_results, file_count = check_runner(args.asset_dir)
    
    # TODO: If --summarize, call summarize module to summarize the results
    if args.summarize:
        pass
    
    # Call reporter module 
    report(args.asset_dir, validation_results, file_count, args.out)
    
    # if --strict, exit error code 1 if the validator caught any failures
    if args.strict and validation_results:
        sys.exit(1)

if __name__ == "__main__":
    main()