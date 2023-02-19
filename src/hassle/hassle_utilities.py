import os
import shutil
from pathlib import Path

import tomlkit
import vermin

import packagelister
from hassle import hassle_config

root = Path(__file__).parent


def increment_version(pyproject_path: Path, increment_type: str):
    """Increment the project.version field in pyproject.toml.

    :param package_path: Path to the package/project directory.

    :param increment_type: One from 'major', 'minor', or 'patch'."""
    meta = tomlkit.loads(pyproject_path.read_text())
    major, minor, patch = [int(num) for num in meta["project"]["version"].split(".")]
    if increment_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment_type == "minor":
        minor += 1
        patch = 0
    elif increment_type == "patch":
        patch += 1
    incremented_version = ".".join(str(num) for num in [major, minor, patch])
    meta["project"]["version"] = incremented_version
    pyproject_path.write_text(tomlkit.dumps(meta))


def update_minimum_python_version(pyproject_path: Path):
    """Use vermin to determine the minimum compatible
    Python version and update the corresponding field
    in pyproject.toml."""
    project_code = "\n".join(
        file.read_text() for file in (pyproject_path.parent / "src").rglob("*.py")
    )
    meta = tomlkit.loads(pyproject_path.read_text())
    minimum_version = vermin.visit(project_code, vermin.Config()).minimum_versions()[1]
    minimum_version = f">={minimum_version[0]}.{minimum_version[1]}"
    meta["project"]["requires-python"] = minimum_version
    pyproject_path.write_text(tomlkit.dumps(meta))


def generate_docs(package_path: Path):
    """Generate project documentation using pdoc."""
    try:
        shutil.rmtree(package_path / "docs")
    except Exception as e:
        pass
    os.system(
        f"pdoc -o {package_path / 'docs'} {package_path / 'src' / package_path.stem}"
    )


def update_dependencies(pyproject_path: Path, overwrite: bool):
    """Update dependencies list in pyproject.toml.

    :param overwrite: If True, replace the dependencies in pyproject.toml
    with the results of packagelister.scan() .
    If False, packages returned by packagelister are appended to
    the current dependencies in pyproject.toml if they don't already
    exist in the field."""
    packages = packagelister.scan(pyproject_path.parent)

    packages = [
        f"{package}~={packages[package]['version']}"
        if packages[package]["version"]
        else f"{package}"
        for package in packages
        if package != pyproject_path.parent.stem
    ]
    packages = [
        package.replace("speech_recognition", "speechRecognition")
        for package in packages
    ]
    meta = tomlkit.loads(pyproject_path.read_text())
    if overwrite:
        meta["project"]["dependencies"] = packages
    else:
        for package in packages:
            if "~" in package:
                name = package.split("~")[0]
            elif "=" in package:
                name = package.split("=")[0]
            else:
                name = package
            if all(
                name not in dependency for dependency in meta["project"]["dependencies"]
            ):
                meta["project"]["dependencies"].append(package)
    pyproject_path.write_text(tomlkit.dumps(meta))


def update_changelog(pyproject_path: Path):
    """Update project changelog."""
    meta = tomlkit.loads(pyproject_path.read_text())
    if hassle_config.config_exists():
        config = hassle_config.load_config()
    else:
        hassle_config.warn()
        print("Creating blank hassle_config.toml...")
        config = hassle_config.load_config()
    changelog_path = pyproject_path.parent / "CHANGELOG.md"
    os.system(
        f"auto-changelog -p {pyproject_path.parent} --tag-prefix {config['git']['tag_prefix']} --unreleased -v {meta['project']['version']} -o {changelog_path}"
    )
    changelog = changelog_path.read_text().splitlines()
    changelog = [line for line in changelog if "Full set of changes:" not in line]
    changelog_path.write_text("\n".join(changelog))


def tag_version(package_path: Path):
    """Add a git tag corresponding
    to the version number in pyproject.toml."""
    if hassle_config.config_exists():
        tag_prefix = hassle_config.load_config()["git"]["tag_prefix"]
    else:
        hassle_config.warn()
        tag_prefix = ""
    version = tomlkit.loads((package_path / "pyproject.toml").read_text())["project"][
        "version"
    ]
    os.chdir(package_path)
    os.system(f"git tag {tag_prefix}{version}")
