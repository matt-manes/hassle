import argparse

from pathier import Pathier

root = Pathier(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=None,
        help=""" Your name. This will be used to populate the 'authors' field of a packages 'pyproject.toml'. """,
    )

    parser.add_argument(
        "-e",
        "--email",
        type=str,
        default=None,
        help=""" Your email. This will be used to populate the 'authors' field of a packages 'pyproject.toml'. """,
    )

    parser.add_argument(
        "-g",
        "--github_username",
        type=str,
        default=None,
        help=""" Your github account name. When creating a new package,
        say with the name 'mypackage', the pyproject.toml 'Homepage' field
        will be set to 'https://github.com/{github_username}/mypackage'
        and the 'Source code' field will be set to
        'https://github.com/{github_username}/mypackage/tree/main/src/mypackage'.""",
    )

    parser.add_argument(
        "-d",
        "--docs_url",
        type=str,
        default=None,
        help=""" The template url to be used in your pyproject.toml file
        indicating where your project docs will be hosted.
        Pass the url such that the spot the actual package name will go is
        held by '$name', e.g. 'https://somedocswebsite/user/projects/$name'.
        If 'hassle_config.toml' didn't exist prior to running this tool and nothing
        is given for this arg, it will default to using the package's github
        url. e.g. for package 'mypackage' the url will be 
        'https://github.com/{your_github_name}/mypackage/tree/main/docs' """,
    )

    parser.add_argument(
        "-t",
        "--tag_prefix",
        type=str,
        default=None,
        help=""" The tag prefix to use with git when tagging source code versions.
        e.g. hassle will use the current version in your pyproject.toml file to when 
        adding a git tag. If you've passed 'v' to this arg and the version of your
        hypothetical package is '1.0.1', it will be tagged as 'v1.0.1'.
        If 'hassle_config.toml' didn't exist prior to running this tool and you
        don't pass anything for this arg, it will default to ''.""",
    )

    args = parser.parse_args()

    return args


def config_exists() -> bool:
    """Check if hassle_config.toml exists."""
    return (root / "hassle_config.toml").exists()


def load_config() -> dict:
    "Load and return hassle_config contents if it exists."
    if config_exists():
        return (root / "hassle_config.toml").loads()
    else:
        raise FileNotFoundError(
            f"load_config() could not find {root/'hassle_config.toml'}.\nRun hassle_config to set it."
        )


def write_config(config: dict):
    """Dump config to "hassle_config.toml."""
    (root / "hassle_config.toml").dumps(config)


def warn():
    print("hassle_config.toml has not been set.")
    print("Run hassle_config to set it.")
    print("Run 'hassle_config -h' for help.")


def create_config(
    name: str = None,
    email: str = None,
    github_username: str = None,
    docs_url: str = None,
    tag_prefix: str = None,
):
    """Create hassle_config.toml from given args."""
    print(f"Manual edits can be made at {root/'hassle_config.toml'}")
    if not config_exists():
        config = {}
        if name and email:
            config["authors"] = [{"name": name, "email": email}]
        elif name:
            config["authors"] = [{"name": name}]
        elif email:
            config["authors"] = [{"email": email}]
        else:
            # In case anything upstream would fail if nothing is present for 'authors'
            config["authors"] = [{"name": "", "email": ""}]
        config["project_urls"] = {
            "Homepage": "",
            "Documentation": "",
            "Source code": "",
        }
        config["git"] = {}
    else:
        config = load_config()
        if name and email:
            config["authors"].append({"name": name, "email": email})
        elif name:
            config["authors"].append({"name": name})
        elif email:
            config["authors"].append({"email": email})

    if github_username:
        config["project_urls"][
            "Homepage"
        ] = f"https://github.com/{github_username}/$name"
        config["project_urls"][
            "Source code"
        ] = f"{config['project_urls']['Homepage']}/tree/main/src/$name"

    if docs_url:
        config["project_urls"]["Documentation"] = docs_url
    elif github_username and config["project_urls"]["Documentation"] == "":
        config["project_urls"][
            "Documentation"
        ] = f"https://github.com/{github_username}/$name/tree/main/docs"

    if tag_prefix:
        config["git"]["tag_prefix"] = tag_prefix
    elif not config_exists() and not tag_prefix:
        config["git"]["tag_prefix"] = ""

    if config:
        write_config(config)


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    create_config(
        args.name, args.email, args.github_username, args.docs_url, args.tag_prefix
    )


if __name__ == "__main__":
    main(get_args())
