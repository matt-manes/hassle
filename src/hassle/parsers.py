import argshell


def get_edit_config_parser() -> argshell.ArgShellParser:
    parser = argshell.ArgShellParser(
        "config",
        description="Edit or create the `hassle_config.toml` file.",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=None,
        help=" Your name. This will be used to populate the 'authors' field of a packages 'pyproject.toml'. ",
    )
    parser.add_argument(
        "-e",
        "--email",
        type=str,
        default=None,
        help=" Your email. This will be used to populate the 'authors' field of a packages 'pyproject.toml'. ",
    )
    parser.add_argument(
        "-g",
        "--github_username",
        type=str,
        default=None,
        help=""" Your github username name. 
        When creating a new package, say with the name 'mypackage', the pyproject.toml 'Homepage' field  will be set to 
        'https://github.com/{github_username}/mypackage' 
        and the 'Source code' field will be set to 
        'https://github.com/{github_username}/mypackage/tree/main/src/mypackage'.""",
    )
    parser.add_argument(
        "-d",
        "--docs_url",
        type=str,
        default=None,
        help=""" The template url to be used in your pyproject.toml file indicating where your project docs will be hosted.
        Pass the url with '$name' as a placeholder for where the package name should go, 
        e.g. 'https://somedocswebsite/user/projects/$name'.
        If 'hassle_config.toml' didn't exist prior to running this tool and nothing is given for this arg, it will default to using the package's github url. 
        e.g. for package 'mypackage' the url will be 'https://github.com/{github_username}/mypackage/tree/main/docs' """,
    )
    parser.add_argument(
        "-t",
        "--tag_prefix",
        type=str,
        default=None,
        help=""" When using Hassle to do `git tag`, this will be prefixed to the front of the version number in the `pyproject.toml` file.""",
    )
    return parser


def get_new_project_parser() -> argshell.ArgShellParser:
    parser = argshell.ArgShellParser(
        "new", description="Create a new project in the current directory."
    )

    parser.add_argument(
        "name",
        type=str,
        help=""" Name of the package to create in the current working directory. """,
    )

    parser.add_argument(
        "-s",
        "--source_files",
        nargs="*",
        type=str,
        default=[],
        help=""" List of additional source files to create in addition to the default
        __init__.py and {name}.py files.""",
    )

    parser.add_argument(
        "-d",
        "--description",
        type=str,
        default="",
        help=""" The package description to be added to the pyproject.toml file. """,
    )

    parser.add_argument(
        "-dp",
        "--dependencies",
        nargs="*",
        type=str,
        default=[],
        help=""" List of dependencies to add to pyproject.toml.
        Note: hassle.py will automatically scan your project for 3rd party imports and update pyproject.toml. 
        This switch is largely useful for adding dependencies your project might need, 
        but doesn't directly import in any source files, like an os.system() call that invokes a 3rd party cli.""",
    )

    parser.add_argument(
        "-k",
        "--keywords",
        nargs="*",
        type=str,
        default=[],
        help=""" List of keywords to be added to the keywords field in pyproject.toml. """,
    )

    parser.add_argument(
        "-as",
        "--add_script",
        action="store_true",
        help=""" Add section to pyproject.toml declaring the package should be installed with command line scripts added. 
        The default is '{package_name} = "{package_name}.{package_name}:main".""",
    )

    parser.add_argument(
        "-nl",
        "--no_license",
        action="store_true",
        help=""" By default, projects are created with an MIT license.
        Set this flag to avoid adding a license if you want to configure licensing at another time.""",
    )

    parser.add_argument(
        "-np",
        "--not_package",
        action="store_true",
        help=""" Put source files in top level directory and delete tests folder. """,
    )
    return parser


def get_build_parser() -> argshell.ArgShellParser:
    """Returns a build parser."""
    parser = argshell.ArgShellParser(
        "build",
        description=""" 
Run the build process:
    * Run tests (abandoning build on failure)
    * Sort imports and format with Black
    * Update dependencies
    * Generate docs
    * Invoke `build` module""",
    )
    parser.add_argument(
        "-s", "--skip_tests", action="store_true", help=""" Skip running tests. """
    )
    parser.add_argument(
        "-o",
        "--overwrite_dependencies",
        action="store_true",
        help=""" Overwrite dependencies instead of appending new ones to the current contents of `pyproject.toml`. """,
    )
    parser.add_argument(
        "-v",
        "--include_versions",
        action="store_true",
        help=""" Include versions when adding dependencies. """,
    )
    return parser


def get_update_parser() -> argshell.ArgShellParser:
    """Returns a update parser."""
    parser = get_build_parser()
    parser.prog = "update"
    parser.description = """
Update this package:
    * Run the build command (run `hassle build -h` for info)
    * Increment project version
    * Update/create changelog
    * git commit -m "chore: build {version}"
    * Git tag with new version number
    * Pull/push to remote
    """
    parser.add_argument(
        "update_type",
        type=str,
        choices=("major", "minor", "patch"),
        help=""" The type of update. """,
    )
    parser.add_argument(
        "-p",
        "--publish",
        action="store_true",
        help=""" Publish theupdated package to PYPI. """,
    )
    parser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help=""" Install updated package. """,
    )
    return parser


def get_add_script_parser() -> argshell.ArgShellParser:
    """Returns a add_script parser."""
    parser = argshell.ArgShellParser(
        "add_script", description=""" Add a script to the `pyproject.toml` file. """
    )
    parser.add_argument("name", type=str, help=""" The name of the script """)
    parser.add_argument(
        "file", type=str, help=""" The file stem the function/script is located in. """
    )
    parser.add_argument(
        "function",
        nargs="?",
        type=str,
        default="main",
        help=""" The name of the function to invoke with the script. Defaults to `main`. """,
    )
    return parser


def add_default_source_files(args: argshell.Namespace) -> argshell.Namespace:
    """Add `__init__.py` and `{args.name}.py` to `args.source_files`."""
    args.source_files += ["__init__.py", f"{args.name}.py"]
    return args
