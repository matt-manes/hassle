import argparse

import coverage
import pytest
from pathier import Pathier


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


def run_tests(package_path: Pathier) -> bool:
    """Run tests with coverage and pytest.

    Returns True if all tests passed."""
    startdir = Pathier().cwd()
    package_path.mkcwd()
    cover = coverage.Coverage()
    cover.start()
    results = pytest.main(["-s"])
    cover.stop()
    cover.report()
    startdir.mkcwd()
    return results == 0


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    package_path = Pathier(args.package_name).resolve()
    run_tests(package_path)


if __name__ == "__main__":
    main(get_args())
