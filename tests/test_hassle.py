import pytest
from pathier import Pathier

from hassle import utilities
from hassle.models import HassleConfig, HassleProject, Pyproject

root = Pathier(__file__).parent


@pytest.fixture(scope="module")
def userdir(tmp_path_factory) -> Pathier:
    userdir = Pathier(tmp_path_factory.mktemp("user"))
    userdir.mkcwd()
    return userdir


@pytest.fixture(scope="module")
def dummy_projectdir(userdir: Pathier) -> Pathier:
    dir_ = userdir / "dummy"
    dir_.mkdir()
    return dir_


@pytest.fixture(scope="module")
def config_path(userdir: Pathier) -> Pathier:
    return userdir / "hassle_config.toml"


def test__config_set_config(config_path: Pathier):
    assert not HassleConfig.exists(config_path)
    HassleConfig.configure(
        "yeehaw", "yeehaw@yeet.com", "big_boi", None, "UwU", config_path
    )
    assert HassleConfig.exists(config_path)


def test__config(config_path: Pathier):
    config_ = HassleConfig.load(config_path)
    assert config_.authors
    assert config_.authors[0].name == "yeehaw"
    assert config_.authors[0].email == "yeehaw@yeet.com"
    assert config_.project_urls.Homepage == "https://github.com/big_boi/$name"
    assert config_.git.tag_prefix == "UwU"


def test__pyproject():
    pyproject = Pyproject.from_template()
    assert pyproject


def test__hassleproject(dummy_projectdir: Pathier, config_path: Pathier):
    name = dummy_projectdir.stem
    pyproject = Pyproject.from_template()
    config = HassleConfig.load(config_path)
    pyproject.project.name = name
    pyproject.project.authors = config.authors
    for url in dir(config.project_urls):
        if not url.startswith("_"):
            setattr(
                pyproject.project.urls,
                url,
                getattr(config.project_urls, url).replace("$name", name),
            )
    hassle = HassleProject(pyproject, dummy_projectdir, ["__init__.py", f"{name}.py"])
    hassle.generate_files()
    for f in dummy_projectdir.rglob("*"):
        print(f)
    for file in [
        "pyproject.toml",
        ".gitignore",
        "README.md",
        "LICENSE.txt",
        ".vscode/settings.json",
        f"tests/test_{name}.py",
    ]:
        assert (dummy_projectdir / file).exists()
    print((dummy_projectdir / "pyproject.toml").read_text())


def test__utilities_bump_version():
    version = "0.0.0"
    version = utilities.bump_version(version, "major")
    assert version == "1.0.0"
    version = utilities.bump_version(version, "minor")
    assert version == "1.1.0"
    version = utilities.bump_version(version, "patch")
    assert version == "1.1.1"
