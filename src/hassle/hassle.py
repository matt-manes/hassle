import argparse
import os

from pathier import Pathier

from hassle import hassle_utilities
from hassle.generate_tests import generate_test_files
from hassle.run_tests import run_tests

root = Pathier(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package",
        type=str,
        default=".",
        nargs="?",
        help=""" The name of the package or project to use,
        assuming it's a subfolder of your current working directory.
        Can also be a full path to the package. If nothing is given,
        the current working directory will be used.""",
    )

    parser.add_argument(
        "-b", "--build", action="store_true", help=""" Build the package. """
    )

    parser.add_argument(
        "-t",
        "--tag_version",
        action="store_true",
        help=""" Add a git tag corresponding to the version in pyproject.toml. """,
    )

    parser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help=""" Install the package from source. """,
    )

    parser.add_argument(
        "-iv",
        "--increment_version",
        type=str,
        default=None,
        help=""" Increment version in pyproject.toml.
        Can be one of "major", "minor", or "patch". """,
    )

    parser.add_argument(
        "-p",
        "--publish",
        action="store_true",
        help=""" Publish package to PyPi.
        Note: You must have configured twine 
        and registered a PyPi account/generated an API
        key to use this option.""",
    )

    parser.add_argument(
        "-rt",
        "--run_tests",
        action="store_true",
        help=""" Run tests for the package. """,
    )

    parser.add_argument(
        "-gt",
        "--generate_tests",
        action="store_true",
        help=""" Generate tests for the package. """,
    )

    parser.add_argument(
        "-uc",
        "--update_changelog",
        action="store_true",
        help=""" Update changelog file. """,
    )

    parser.add_argument(
        "-od",
        "--overwrite_dependencies",
        action="store_true",
        help=""" When building a package, packagelister will be used
        to update the dependencies list in pyproject.toml.
        The default behavior is to append any new dependencies to
        the current list so as not to erase any manually added dependencies
        that packagelister may not detect. If you don't have any manually 
        added dependencies and want to remove any dependencies that your
        project no longer uses, pass this flag.""",
    )

    parser.add_argument(
        "-ca",
        "--commit_all",
        type=str,
        default=None,
        help=""" Git stage and commit all tracked files
        with this supplied commit message.
        If 'build' is passed, all commits will have
        message: 'chore: build v{current_version}""",
    )

    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help=""" Pull from github, then push current commit to repo. """,
    )

    parser.add_argument(
        "-dv",
        "--dependency_versions",
        action="store_true",
        help=""" Include version specifiers for dependencies in
        pyproject.toml.""",
    )

    parser.add_argument(
        "-up",
        "--update",
        type=str,
        default=None,
        help=""" Excpects one argument: "major", "minor", or "patch".
        Passing "-up minor" is equivalent to passing the cli string: "-b -t -i -iv minor -uc -ca build -s".
        To publish the updated package, the -p/--publish switch needs to be added to the cli input.""",
    )

    parser.add_argument(
        "-st",
        "--skip_tests",
        action="store_true",
        help=""" Don't run tests when using the -b/--build command. """,
    )

    args = parser.parse_args()

    args.package = Pathier(args.package).resolve()

    if args.update:
        args.build = True
        args.tag_version = True
        args.install = True
        args.increment_version = args.update
        args.update_changelog = True
        args.commit_all = "build"
        args.sync = True

    if args.increment_version and args.increment_version not in [
        "major",
        "minor",
        "patch",
    ]:
        raise ValueError(
            f"Invalid option for -iv/--increment_version: {args.increment_version}"
        )

    if args.commit_all == "":
        raise ValueError("Commit message for args.commit_all cannot be empty.")

    return args


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()

    pyproject_path = args.package / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(f"Could not locate pyproject.toml for {args.package}")

    if args.generate_tests:
        generate_test_files(args.package)

    if args.run_tests:
        run_tests(args.package)

    if args.increment_version:
        hassle_utilities.increment_version(pyproject_path, args.increment_version)

    if args.build:
        (args.package / "dist").delete()
        os.system(f"black {args.package}")
        os.system(f"isort {args.package}")
        hassle_utilities.update_dependencies(
            pyproject_path, args.overwrite_dependencies
        )
        # Vermin isn't taking into account the minimum version of dependencies.
        # Removing from now and defaulting to >=3.10
        # hassle_utilities.update_minimum_python_version(pyproject_path)
        hassle_utilities.generate_docs(args.package)
        os.system(f"py -m build {args.package}")

    if args.update_changelog:
        hassle_utilities.update_changelog(pyproject_path)
        # If we're going to add tag for current version
        # commit changelog first
        if args.tag_version:
            input(
                "Press enter to continue after optionally pruning the updated changelog..."
            )
            os.chdir(args.package)
            os.system("git add CHANGELOG.md")
            os.system('git commit CHANGELOG.md -m "chore: update changelog"')

    if args.commit_all:
        os.chdir(args.package)
        if args.commit_all == "build":
            version = pyproject_path.loads()["project"]["version"]
            args.commit_all = f"chore: build v{version}"
        os.system("git add .")
        os.system(f'git commit -m "{args.commit_all}"')

    if args.tag_version:
        hassle_utilities.tag_version(args.package)

    if args.publish:
        os.system(f"twine upload {args.package / 'dist' / '*'}")

    if args.install:
        os.system(f"pip install {args.package} --no-deps --upgrade --no-cache-dir")

    if args.sync:
        os.chdir(args.package)
        os.system(f"git pull --tags origin main")
        os.system(f"git push origin main:main --tags")


if __name__ == "__main__":
    main(get_args())
