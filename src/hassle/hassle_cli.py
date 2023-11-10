import subprocess
import sys

import argshell
import pip
from gitbetter import Git
from pathier import Pathier

from hassle import parsers, utilities
from hassle.models import HassleConfig, HassleProject, Pyproject

root = Pathier(__file__).parent


class HassleShell(argshell.ArgShell):
    def __init__(self, command: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if command == "new":
            # load a blank HassleProject
            self.project = HassleProject(Pyproject.from_template(), Pathier.cwd(), [])
        else:
            try:
                self.project = HassleProject.load(Pathier.cwd())
            except Exception as e:
                print(f"{Pathier.cwd().stem} does not appear to be a Hassle project.")
                print(e)

    def _build(self, args: argshell.Namespace):
        self.project.format_source_files()
        self.project.update_dependencies(
            args.overwrite_dependencies, args.include_versions
        )
        self.project.generate_docs()
        self.project.distdir.delete()
        self.project.save()
        subprocess.run([sys.executable, "-m", "build", Pathier.cwd()])

    @argshell.with_parser(parsers.get_add_script_parser)
    def do_add_script(self, args: argshell.Namespace):
        """Add a script to the `pyproject.toml` file."""
        self.project.add_script(args.name, args.file.strip(".py"), args.function)
        self.project.save()

    @argshell.with_parser(parsers.get_build_parser)
    def do_build(self, args: argshell.Namespace):
        """Build this project."""
        if not args.skip_tests and not utilities.run_tests():
            raise RuntimeError(
                f"ERROR: {Pathier.cwd().stem} failed testing.\nAbandoning build."
            )
        self._build(args)

    def do_check_pypi(self, name: str):
        """Check if the given package name is taken on pypi.org or not."""
        if utilities.check_pypi(name):
            print(f"{name} is already taken.")
        else:
            print(f"{name} is available.")

    def do_config(self, _: str = ""):
        """Print hassle config to terminal."""
        config = root / "hassle_config.toml"
        if config.exists():
            print(config.read_text())
        else:
            print("hassle_config.toml doesn't exist.")

    @argshell.with_parser(parsers.get_edit_config_parser)
    def do_configure(self, args: argshell.Namespace):
        """Edit or create `hassle_config.toml`."""
        HassleConfig.configure(
            args.name, args.email, args.github_username, args.docs_url, args.tag_prefix
        )

    def do_format(self, _: str = ""):
        """Format all `.py` files with `isort` and `black`."""
        self.project.format_source_files()

    def do_install(self, _: str = ""):
        """Install this package."""
        pip.main(["install", "."])

    def do_is_published(self, _: str = ""):
        """Check if the most recent version of this package is published to PYPI."""
        text = f"The most recent version of '{self.project.name}' has"
        if self.project.latest_version_is_published():
            print(f"{text} has been published.")
        else:
            print(f"{text} has not been published.")

    @argshell.with_parser(
        parsers.get_new_project_parser,
        [parsers.list_to_string_post_parser, parsers.add_default_source_files],
    )
    def do_new(self, args: argshell.Namespace):
        """Create a new project."""
        # Check if this name is taken.
        if not args.not_package and utilities.check_pypi(args.name):
            print(f"{args.name} already exists on pypi.org")
            if not utilities.get_answer("Continue anyway?"):
                sys.exit()
        # Check if targetdir already exists
        targetdir = Pathier.cwd() / args.name
        if targetdir.exists():
            print(f"'{args.name}' already exists.")
            if not utilities.get_answer("Overwrite?"):
                sys.exit()
        # Load config
        if not HassleConfig.exists():
            HassleConfig.warn()
            if not utilities.get_answer(
                "Continue creating new package with blank config?"
            ):
                raise Exception("Aborting new package creation")
            else:
                print("Creating blank hassle_config.toml...")
                HassleConfig.configure()
        self.project = HassleProject.new(
            targetdir,
            args.name,
            args.description,
            args.dependencies,
            args.keywords,
            args.source_files,
            args.add_script,
            args.no_license,
        )
        # If not a package (just a project) move source code to top level.
        if args.not_package:
            for file in self.project.srcdir.iterdir():
                file.copy(self.project.projectdir / file.name)
            self.project.srcdir.parent.delete()
        # Initialize Git
        self.project.projectdir.mkcwd()
        git = Git()
        git.new_repo()

    def do_publish(self, _: str = ""):
        """Publish this package.

        You must have 'twine' installed and set up to use this command."""
        if not utilities.on_primary_branch():
            print(
                "WARNING: You are trying to publish a project that does not appear to be on its main branch."
            )
            print(f"You are on branch '{Git().current_branch}'")
            if not utilities.get_answer("Continue anyway?"):
                return
        subprocess.run(["twine", "upload", self.project.distdir / "*"])

    def do_test(self, _: str):
        """Invoke `pytest -s` with Coverage."""
        utilities.run_tests()

    @argshell.with_parser(parsers.get_update_parser)
    def do_update(self, args: argshell.Namespace):
        """Update this package."""
        if not args.skip_tests and not utilities.run_tests():
            raise RuntimeError(
                f"ERROR: {Pathier.cwd().stem} failed testing.\nAbandoning build."
            )
        self.project.bump_version(args.update_type)
        self.project.save()
        self._build(args)
        git = Git()
        if HassleConfig.exists():
            tag_prefix = HassleConfig.load().git.tag_prefix
        else:
            HassleConfig.warn()
            print("Assuming no tag prefix.")
            tag_prefix = ""
        tag = f"{tag_prefix}{self.project.version}"
        git.add_all()
        git.commit_all(f"chore: build {tag}")
        # 'auto-changelog' generates based off of commits between tags
        # So to include the changelog in the tagged commit,
        # we have to tag the code, update/commit the changelog, delete the tag, and then retag
        # (One of these days I'll just write my own changelog generator)
        git.tag(tag)
        self.project.update_changelog()
        with git.capturing_output():
            git.tag(f"-d {tag}")
        input("Press enter to continue after editing the changelog...")
        git.add_files([self.project.changelog_path])
        git.commit_files([self.project.changelog_path], "chore: update changelog")
        with git.capturing_output():
            git.tag(tag)
        # Sync with remote
        sync = f"origin {git.current_branch} --tags"
        git.pull(sync)
        git.push(sync)
        if args.publish:
            self.do_publish()
        if args.install:
            self.do_install()


def main():
    """ """
    command = "" if len(sys.argv) < 2 else sys.argv[1]
    shell = HassleShell(command)
    if command == "help":
        input_ = f"help {sys.argv[2]}"
    # Doing this so args that are multi-word strings don't get interpreted as separate args.
    elif command:
        input_ = f"{command} " + " ".join([f'"{arg}"' for arg in sys.argv[2:]])
    else:
        input_ = "help"
    shell.onecmd(input_)


if __name__ == "__main__":
    main()
