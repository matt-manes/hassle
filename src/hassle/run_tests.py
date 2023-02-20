import argparse
import os
from pathlib import Path


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package_name",
        type=str,
        default=".",
        nargs="?",
        help=""" The name of the package or project to run tests for,
        assuming it's a subfolder of your current working directory.
        Can also be a full path to the package. If nothing is given,
        the current working directory will be used.""",
    )

    args = parser.parse_args()

    return args


def run_tests(package_path: Path):
    """Run tests with coverage and pytest."""
    startdir = Path().cwd()
    os.chdir(package_path)
    os.system(f"pip install -e .")
    os.system(f"coverage run -m pytest -s")
    os.system(f"coverage report -m")
    os.chdir(startdir)


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    package_path = Path(args.package_name).resolve()
    run_tests(package_path)


if __name__ == "__main__":
    main(get_args())
