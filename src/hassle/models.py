import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime
from functools import cached_property
from typing import Any

import black
import dacite
import isort
import requests
from bs4 import BeautifulSoup, Tag
from packagelister import packagelister
from pathier import Pathier, Pathish
from typing_extensions import Self

from hassle import utilities

root = Pathier(__file__).parent


@dataclass
class Sdist:
    exclude: list[str]


@dataclass
class Targets:
    sdist: Sdist


@dataclass
class Build:
    targets: Targets


@dataclass
class BuildSystem:
    requires: list[str]
    build_backend: str


@dataclass
class Urls:
    Homepage: str = ""
    Documentation: str = ""
    Source_code: str = ""


@dataclass
class Author:
    name: str = ""
    email: str = ""


@dataclass
class Git:
    tag_prefix: str = ""


@dataclass
class IniOptions:
    addopts: list[str]
    pythonpath: str


@dataclass
class Pytest:
    ini_options: IniOptions


@dataclass
class Hatch:
    build: Build


@dataclass
class Tool:
    pytest: Pytest
    hatch: Hatch


@dataclass
class Project:
    name: str
    authors: list[Author] = field(default_factory=list)
    description: str = ""
    requires_python: str = ""
    version: str = ""
    dependencies: list[str] = field(default_factory=list)
    readme: str = ""
    keywords: list[str] = field(default_factory=list)
    classifiers: list[str] = field(default_factory=list)
    urls: Urls = field(default_factory=Urls)
    scripts: dict[str, str] = field(default_factory=dict)


@dataclass
class Pyproject:
    build_system: BuildSystem
    project: Project
    tool: Tool

    @staticmethod
    def _swap_keys(data: dict[str, Any]) -> dict[str, Any]:
        """Swap between original toml key and valid Python variable."""
        if "build-system" in data:
            data = utilities.swap_keys(data, ("build-system", "build_system"))
            if "build-backend" in data["build_system"]:
                data["build_system"] = utilities.swap_keys(
                    data["build_system"], ("build-backend", "build_backend")
                )
        elif "build_system" in data:
            data = utilities.swap_keys(data, ("build-system", "build_system"))
            if "build_backend" in data["build-system"]:
                data["build-system"] = utilities.swap_keys(
                    data["build-system"], ("build-backend", "build_backend")
                )

        if "project" in data and (
            "requires-python" in data["project"] or "requires_python"
        ):
            data["project"] = utilities.swap_keys(
                data["project"], ("requires-python", "requires_python")
            )
        if all(
            [
                "project" in data,
                "urls" in data["project"],
                (
                    "Source code" in data["project"]["urls"]
                    or "Source_code" in data["project"]["urls"]
                ),
            ]
        ):
            data["project"]["urls"] = utilities.swap_keys(
                data["project"]["urls"], ("Source code", "Source_code")
            )

        return data

    @classmethod
    def load(cls, path: Pathish = Pathier("pyproject.toml")) -> Self:
        """Return a `datamodel` object populated from `path`."""
        data = Pathier(path).loads()
        data = cls._swap_keys(data)
        return dacite.from_dict(cls, data)

    def dump(self, path: Pathish = Pathier("pyproject.toml")):
        """Write the contents of this `datamodel` object to `path`."""
        data = asdict(self)
        data = self._swap_keys(data)
        Pathier(path).dumps(data)

    @classmethod
    def from_template(cls) -> Self:
        """Return a `Pyproject` object using `templates/pyproject_template.toml`."""
        return cls.load(root / "templates" / "pyproject.toml")


@dataclass
class HassleConfig:
    authors: list[Author] = field(default_factory=list)
    project_urls: Urls = field(default_factory=Urls)
    git: Git = field(default_factory=Git)

    @classmethod
    def load(
        cls, path: Pathish = Pathier(__file__).parent / "hassle_config.toml"
    ) -> Self:
        """Return a `datamodel` object populated from `path`."""
        path = Pathier(path)
        if not path.exists():
            raise FileNotFoundError(
                f"Could not find hassle config at {path}.\nRun hassle_config in a terminal to set it."
            )
        data = path.loads()
        data["project_urls"] = utilities.swap_keys(
            data["project_urls"], ("Source_code", "Source code")
        )
        return dacite.from_dict(cls, data)

    def dump(self, path: Pathish = Pathier(__file__).parent / "hassle_config.toml"):
        """Write the contents of this `datamodel` object to `path`."""
        data = asdict(self)
        data["project_urls"] = utilities.swap_keys(
            data["project_urls"], ("Source_code", "Source code")
        )
        Pathier(path).dumps(data)

    @staticmethod
    def warn():
        print("hassle_config.toml has not been set.")
        print("Run hassle_config to set it.")
        print("Run 'hassle config -h' for help.")

    @staticmethod
    def exists(path: Pathish = Pathier(__file__).parent / "hassle_config.toml") -> bool:
        return Pathier(path).exists()

    @classmethod
    def configure(
        cls,
        name: str | None = None,
        email: str | None = None,
        github_username: str | None = None,
        docs_url: str | None = None,
        tag_prefix: str | None = None,
        config_path: Pathish = Pathier(__file__).parent / "hassle_config.toml",
    ):
        """Create or edit `hassle_config.toml` from given params."""
        print(f"Manual edits can be made at {config_path}")
        if not cls.exists(config_path):
            config = cls()
        else:
            config = cls.load(config_path)
        # Add an author to config if a name or email is given.
        if name or email:
            config.authors.append(Author(name or "", email or ""))
        if github_username:
            homepage = f"https://github.com/{github_username}/$name"
            config.project_urls.Homepage = homepage
            config.project_urls.Source_code = f"{homepage}/tree/main/src/$name"
        if not config.project_urls.Documentation:
            if github_username and not docs_url:
                config.project_urls.Documentation = (
                    f"https://github.com/{github_username}/$name/tree/main/docs"
                )
            elif docs_url:
                config.project_urls.Documentation = docs_url
        if tag_prefix:
            config.git.tag_prefix = tag_prefix
        config.dump(config_path)


@dataclass
class HassleProject:
    pyproject: Pyproject
    projectdir: Pathier
    source_files: list[str]
    templatedir: Pathier = root / "templates"

    @property
    def source_code(self) -> str:
        """Join and return all code from any `.py` files in `self.srcdir`.

        Useful if a tool needs to scan all the source code for something."""
        return "\n".join(file.read_text() for file in self.srcdir.rglob("*.py"))

    @cached_property
    def srcdir(self) -> Pathier:
        return self.projectdir / "src" / self.pyproject.project.name

    @cached_property
    def changelog_path(self) -> Pathier:
        return self.projectdir / "CHANGELOG.md"

    @cached_property
    def pyproject_path(self) -> Pathier:
        return self.projectdir / "pyproject.toml"

    @cached_property
    def docsdir(self) -> Pathier:
        return self.projectdir / "docs"

    @cached_property
    def testsdir(self) -> Pathier:
        return self.projectdir / "tests"

    @cached_property
    def vsdir(self) -> Pathier:
        return self.projectdir / ".vscode"

    @cached_property
    def distdir(self) -> Pathier:
        return self.projectdir / "dist"

    @property
    def name(self) -> str:
        """This package's name."""
        return self.pyproject.project.name

    @property
    def version(self) -> str:
        """This package's version."""
        return self.pyproject.project.version

    @version.setter
    def version(self, new_version: str):
        self.pyproject.project.version = new_version

    @classmethod
    def load(cls, projectdir: Pathish) -> Self:
        """Load a project given `projectdir`."""
        projectdir = Pathier(projectdir)
        pyproject = Pyproject.load(projectdir / "pyproject.toml")
        name = pyproject.project.name
        # Convert source files to path stems relative to projectdir/src/name
        # e.g `C:/python/projects/hassle/src/hassle/templates/pyproject.toml`
        # becomes `templates/pyproject.toml`
        source_files = [
            str(file.separate(name))
            for file in (projectdir / "src" / name).rglob("*")
            if file.is_file()
        ]
        return cls(pyproject, projectdir, source_files)

    @classmethod
    def new(
        cls,
        targetdir: Pathier,
        name: str,
        description: str = "",
        dependencies: list[str] = [],
        keywords: list[str] = [],
        source_files: list[str] = [],
        add_script: bool = False,
        no_license: bool = False,
    ) -> Self:
        """Create and return a new hassle project."""
        pyproject = Pyproject.from_template()
        config = HassleConfig.load()
        pyproject.project.name = name
        pyproject.project.authors = config.authors
        pyproject.project.description = description
        pyproject.project.dependencies = dependencies
        pyproject.project.keywords = keywords
        pyproject.project.urls.Homepage = config.project_urls.Homepage.replace(
            "$name", name
        )
        pyproject.project.urls.Documentation = (
            config.project_urls.Documentation.replace("$name", name)
        )
        pyproject.project.urls.Source_code = config.project_urls.Source_code.replace(
            "$name", name
        )
        hassle = cls(pyproject, targetdir, source_files)
        if add_script:
            hassle.add_script(name, name)
        hassle.generate_files()
        if no_license:
            hassle.pyproject.project.classifiers.pop(1)
            (hassle.projectdir / "LICENSE.txt").delete()
        hassle.save()
        return hassle

    def get_template(self, file_name: str) -> str:
        """Open are return the content of `{self.templatedir}/{file_name}`."""
        return (self.templatedir / file_name).read_text()

    def save(self):
        """Dump `self.pyproject` to `{self.projectdir}/pyproject.toml`."""
        self.pyproject.dump(self.pyproject_path)

    def format_source_files(self):
        """Use isort and black to format files"""
        for file in self.projectdir.rglob("*.py"):
            isort.file(file)
        try:
            black.main([str(self.projectdir)])
        except SystemExit as e:
            ...
        except Exception as e:
            raise e

    def latest_version_is_published(self) -> bool:
        """Check if the current version of this project has been published to pypi.org."""
        pypi_url = f"https://pypi.org/project/{self.name}"
        response = requests.get(pypi_url)
        if response.status_code != 200:
            raise RuntimeError(
                f"{pypi_url} returned status code {response.status_code} :/"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        header = soup.find("h1", class_="package-header__name")
        assert isinstance(header, Tag)
        text = header.text.strip()
        pypi_version = text[text.rfind(" ") + 1 :]
        return self.version == pypi_version

    # ====================================================================================
    # Updaters ===========================================================================
    # ====================================================================================
    def add_script(self, name: str, file_stem: str, function: str = "main"):
        """Add a script to `pyproject.project.scripts` in the format `{name} = "{package_name}.{file_stem}:{function}"`"""
        self.pyproject.project.scripts[name] = f"{self.name}.{file_stem}:{function}"

    def update_init_version(self):
        """Update the `__version__` in this projects `__init__.py` file
        to the current value of `self.pyproject.project.version`
        if it exists and has a `__version__` string.

        If it doesn't have a `__version__` string, append one to it."""
        init_file = self.srcdir / "__init__.py"
        version = f'__version__ = "{self.version}"'
        if init_file.exists():
            content = init_file.read_text()
            if "__version__" in content:
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if line.startswith("__version__"):
                        lines[i] = version
                content = "\n".join(lines)
            else:
                content += f"\n{version}"
            init_file.write_text(content)

    def bump_version(self, bump_type: str):
        """Bump the version of this project.

        `bump_type` should be `major`, `minor`, or `patch`."""
        # bump pyproject version
        self.version = utilities.bump_version(self.version, bump_type)
        # bump `__version__` in __init__.py if the file exists and has a `__version__`.
        self.update_init_version()

    def update_dependencies(
        self, overwrite_existing_packages: bool, include_versions: bool
    ):
        """Scan project for dependencies and update the corresponding field in the pyproject model.

        If `overwrite_existing_packages` is `False`, this function will only add a package if it isn't already listed,
        but won't remove anything currently in the list.
        Use this option to preserve manually added dependencies."""
        project = packagelister.scan_dir(self.srcdir)
        version_conditional = ">=" if include_versions else None
        if overwrite_existing_packages:
            self.pyproject.project.dependencies = project.get_formatted_requirements(
                version_conditional
            )
        else:
            # Only add a package if it isn't already in the dependency list
            self.pyproject.project.dependencies.extend(
                [
                    (
                        package.get_formatted_requirement(version_conditional)
                        if version_conditional
                        else package.distribution_name
                    )
                    for package in project.requirements
                    if all(
                        package.distribution_name not in existing_dependency
                        for existing_dependency in self.pyproject.project.dependencies
                    )
                ]
            )

    def _generate_changelog(self) -> list[str]:
        if HassleConfig.exists():
            tag_prefix = HassleConfig.load().git.tag_prefix
        else:
            HassleConfig.warn()
            print("Assuming no tag prefix.")
            tag_prefix = ""
        raw_changelog = [
            line
            for line in subprocess.run(
                [
                    "auto-changelog",
                    "-p",
                    self.projectdir,
                    "--tag-prefix",
                    tag_prefix,
                    "--stdout",
                ],
                stdout=subprocess.PIPE,
                text=True,
            ).stdout.splitlines(True)
            if not line.startswith(
                (
                    "Full set of changes:",
                    f"* build {tag_prefix}",
                    "* update changelog",
                )
            )
        ]
        return raw_changelog

    def update_changelog(self):
        """Update `CHANGELOG.md` by invoking the `auto-changelog` module.

        If `hassle_config.toml` doesn't exist, an empty tag prefix will be assumed."""
        raw_changelog = self._generate_changelog()
        # If there's no existing changelog, dump the generated one and get out of here.
        if not self.changelog_path.exists():
            self.changelog_path.join(raw_changelog)
            return

        # Don't want to overwrite previously existing manual changes/edits
        existing_changelog = self.changelog_path.read_text().splitlines(True)[
            2:
        ]  # First two elements are "# Changelog\n" and "\n"
        new_changes = raw_changelog
        for line in existing_changelog:
            # Release headers are prefixed with "## "
            if line.startswith("## "):
                new_changes = raw_changelog[: raw_changelog.index(line)]
                break
        changes = "".join(new_changes)
        # "#### OTHERS" gets added to the changelog even when there's nothing for that category,
        # so we'll get rid of it if that's the case
        others = "#### Others"
        if changes.strip("\n").endswith(others):
            changes = changes.strip("\n").replace(others, "\n\n")
        # If changes == "# Changelog\n\n" then there weren't actually any new changes
        if not changes == "# Changelog\n\n":
            self.changelog_path.write_text(changes + "".join(existing_changelog))

    # ====================================================================================
    # File/Project creation ==============================================================
    # ====================================================================================

    def create_source_files(self):
        """Generate source files in `self.srcdir`."""
        for file in self.source_files:
            (self.srcdir / file).touch()
        init = self.srcdir / "__init__.py"
        if init.exists():
            init.append(f'__version__ = "{self.version}"')

    def create_readme(self):
        readme = self.get_template("README.md")
        readme = readme.replace("$name", self.name)
        readme = readme.replace("$description", self.pyproject.project.description)
        (self.projectdir / "README.md").write_text(readme)

    def create_license(self):
        license_ = self.get_template("license.txt")
        license_ = license_.replace("$year", str(datetime.now().year))
        (self.projectdir / "LICENSE.txt").write_text(license_)

    def create_gitignore(self):
        (self.templatedir / ".gitignore.txt").copy(self.projectdir / ".gitignore")

    def create_vscode_settings(self):
        self.vsdir.mkdir()
        (self.templatedir / "vscode_settings.json").copy(self.vsdir / "settings.json")

    def create_tests(self):
        (self.testsdir / f"test_{self.name}.py").touch()

    def create_py_typed(self):
        (self.projectdir / "py.typed").touch()

    def generate_files(self):
        """Create all the necessary files.

        Note: This will overwrite any existing files."""
        self.projectdir.mkdir()
        for func in dir(self):
            if func.startswith("create_"):
                getattr(self, func)()
        self.pyproject.dump(self.pyproject_path)

    def generate_docs(self):
        """Generate docs by invoking `pdoc`"""
        self.docsdir.delete()
        subprocess.run(["pdoc", "-o", self.docsdir, self.srcdir])
