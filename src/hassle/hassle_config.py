from dataclasses import asdict, dataclass, field

import dacite
from pathier import Pathier, Pathish
from typing_extensions import Self

root = Pathier(__file__).parent


@dataclass
class Author:
    name: str = ""
    email: str = ""


@dataclass
class ProjectUrls:
    Homepage: str = ""
    Documentation: str = ""
    Source_code: str = ""


@dataclass
class Git:
    tag_prefix: str = ""


@dataclass
class HassleConfig:
    authors: list[Author] = field(default_factory=list)
    project_urls: ProjectUrls = field(default_factory=ProjectUrls)
    git: Git = field(default_factory=Git)

    @staticmethod
    def _correct_source_code_key(data: dict) -> dict:
        swaps = None
        keys = data["project_urls"].keys()
        if "Source code" in keys:
            swaps = ("Source_code", "Source code")
        elif "Source_code" in keys:
            swaps = ("Source code", "Source_code")
        if swaps:
            data["project_urls"][swaps[0]] = data["project_urls"].pop(swaps[1])
        return data

    @classmethod
    def load(
        cls, path: Pathish = Pathier(__file__).parent / "hassle_config.toml"
    ) -> Self | None:
        """Return a `datamodel` object populated from `path`."""
        path = Pathier(path)
        if not path.exists():
            print(
                f"Could not find hassle config at {path}.\nRun hassle_config in a terminal to set it."
            )
            return None
        data = path.loads()
        data = cls._correct_source_code_key(data)
        return dacite.from_dict(cls, data)

    def dump(self, path: Pathish = Pathier(__file__).parent / "hassle_config.toml"):
        """Write the contents of this `datamodel` object to `path`."""
        data = asdict(self)
        data = self._correct_source_code_key(data)
        Pathier(path).dumps(data)

    @staticmethod
    def warn():
        print("hassle_config.toml has not been set.")
        print("Run hassle_config to set it.")
        print("Run 'hassle_config -h' for help.")

    @staticmethod
    def exists(path: Pathish = Pathier(__file__).parent / "hassle_config.toml") -> bool:
        return Pathier(path).exists()


def edit_config(
    name: str | None = None,
    email: str | None = None,
    github_username: str | None = None,
    docs_url: str | None = None,
    tag_prefix: str | None = None,
):
    """Create or edit `hassle_config.toml` from given params."""
    print(f"Manual edits can be made at {root / 'hassle_config.toml'}")
    if not HassleConfig.exists():
        config = HassleConfig()
    else:
        config = HassleConfig.load()
    assert config
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
    config.dump()
