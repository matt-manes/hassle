import re
import subprocess
from typing import Any

import requests
from bs4 import BeautifulSoup
from gitbetter import Git
from pathier import Pathier

root = Pathier(__file__).parent


def swap_keys(data: dict[str, Any], keys: tuple[str, str]) -> dict[str, Any]:
    """Convert between keys in `data`.
    The order of `keys` doesn't matter.
    >>> data = {"one two": 1}
    >>> data = swap_keys(data, ("one two", "one-two"))
    >>> print(data)
    >>> {"one-two": 1}
    >>> data = swap_keys(data, ("one two", "one-two"))
    >>> print(data)
    >>> {"one two": 1}
    """
    key1, key2 = keys
    data_keys = data.keys()
    if key1 in data_keys:
        data[key2] = data.pop(key1)
    elif key2 in data_keys:
        data[key1] = data.pop(key2)
    return data


def run_tests(pytest_args: list[str] = []) -> bool:
    """Invoke `coverage` and `pytest -s`.

    Returns `True` if all tests passed or if no tests were found."""
    results = subprocess.run(["coverage", "run", "-m", "pytest", "-s"] + pytest_args)
    subprocess.run(["coverage", "report", f"--include={Pathier.cwd()}/*"])
    subprocess.run(["coverage", "html", f"--include={Pathier.cwd()}/*"])
    return results.returncode in [0, 5]


def check_pypi(package_name: str) -> bool:
    """Check if a package with package_name already exists on `pypi.org`.
    Returns `True` if package name exists.
    Only checks the first page of results."""
    url = f"https://pypi.org/search/?q={package_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f"Error: pypi.org returned status code: {response.status_code}"
        )
    soup = BeautifulSoup(response.text, "html.parser")
    pypi_packages = [
        span.text.lower()
        for span in soup.find_all("span", class_="package-snippet__name")
    ]
    return package_name in pypi_packages


def get_answer(question: str) -> bool | None:
    """Repeatedly ask the user a yes/no question until a 'y' or a 'n' is received."""
    ans = ""
    question = question.strip()
    if "?" not in question:
        question += "?"
    question += " (y/n): "
    while ans not in ["y", "yes", "no", "n"]:
        ans = input(question).strip().lower()
        if ans in ["y", "yes"]:
            return True
        elif ans in ["n", "no"]:
            return False
        else:
            print("Invalid answer.")


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump `current_version` according to `bump_type` and return the new version.

    #### :params:

    `current_version`: A version string conforming to Semantic Versioning standards.
    i.e. `{major}.{minor}.{patch}`

    `bump_type` can be one of `major`, `minor`, or `patch`.

    Raises an exception if `current_version` is formatted incorrectly or if `bump_type` isn't one of the aforementioned types.
    """
    if not re.findall(r"[0-9]+.[0-9]+.[0-9]+", current_version):
        raise ValueError(
            f"{current_version} does not appear to match the required format of `x.x.x`."
        )
    bump_type = bump_type.lower().strip()
    if bump_type not in ["major", "minor", "patch"]:
        raise ValueError(
            f"`bump_type` {bump_type} is not one of `major`, `minor`, or `patch`."
        )
    major, minor, patch = [int(part) for part in current_version.split(".")]
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"


def on_primary_branch() -> bool:
    """Returns `False` if repo is not currently on `main` or `master` branch."""
    git = Git(True)
    if git.current_branch not in ["main", "master"]:
        return False
    return True
