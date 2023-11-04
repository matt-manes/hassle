import argparse
import tokenize

import isort
from pathier import Pathier

from hassle import hassle_utilities

root = Pathier(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "paths",
        type=str,
        default=".",
        nargs="*",
        help=""" The name of the package or project to generate tests for,
        assuming it's a subfolder of your current working directory.
        Can also be a full path to the package. If nothing is given,
        the current working directory will be used.
        Can also be individual files.""",
    )

    parser.add_argument(
        "-t",
        "--tests_dir",
        type=str,
        default=None,
        help=""" A specific tests directory path to write tests to.
        When supplying individual files to paths arg, the default
        behavior is to create a 'tests' directory in the parent 
        directory of the specified file, resulting in multiple 
        'tests' directories being created if the files exist in
        subdirectories. Supply a path to this arg to override
        this behavior.""",
    )

    args = parser.parse_args()
    return args


def get_function_names(filepath: Pathier) -> list[str]:
    """Returns a list of function names from a .py file."""
    with filepath.open("r") as file:
        tokens = list(tokenize.generate_tokens(file.readline))
    functions = []
    for i, token in enumerate(tokens):
        # If token.type is "name" and the preceeding token is "def"
        if (
            token.type == 1
            and tokens[i - 1].type == 1
            and tokens[i - 1].string == "def"
        ):
            functions.append(token.string)
    return functions


def write_placeholders(
    package_path: Pathier,
    pyfile: Pathier | str,
    functions: list[str],
    tests_dir: Pathier = None,
):
    """Write placeholder functions to the
    tests/test_{pyfile} file if they don't already exist.
    The placeholder functions use the naming convention
    test_{function_name}

    :param package_path: Path to the package.

    :param pyfile: Path to the pyfile to write placeholders for.

    :param functions: List of functions to generate
    placehodlers for."""
    package_name = package_path.stem
    if not tests_dir:
        tests_dir = package_path / "tests"
    tests_dir.mkdir()
    pyfile = Pathier(pyfile)
    test_file = tests_dir / f"test_{pyfile.name}"
    # Makes sure not to overwrite previously written tests
    # or additional imports.
    if test_file.exists():
        content = test_file.read_text() + "\n\n"
    else:
        content = f"from {package_name} import {pyfile.stem}\n\n\n"
    for function in functions:
        test_function = f"def test_{function}"
        if test_function not in content and function != "__init__":
            content += f"{test_function}():\n    ...\n\n\n"
    test_file.write_text(content)
    hassle_utilities.format_files(tests_dir)
    [isort.file(path) for path in tests_dir.rglob("*.py")]


def generate_test_files(package_path: Pathier, tests_dir: Pathier = None):
    """Generate test files for all .py files in 'src'
    directory of 'package_path'."""
    pyfiles = [
        file
        for file in (package_path / "src").rglob("*.py")
        if file.name != "__init__.py"
    ]
    for pyfile in pyfiles:
        write_placeholders(package_path, pyfile, get_function_names(pyfile), tests_dir)


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    args.paths = [Pathier(path).resolve() for path in args.paths]
    if args.tests_dir:
        args.tests_dir = Pathier(args.tests_dir).resolve()
    for path in args.paths:
        if path.is_dir():
            generate_test_files(path, args.tests_dir)
        elif path.is_file():
            write_placeholders(
                path.parent, path, get_function_names(path), args.tests_dir
            )


if __name__ == "__main__":
    main(get_args())
