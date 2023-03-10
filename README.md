# Hassle

Automate creating, building, testing, and publishing Python projects and packages from the command line. <br>
This package wraps several other packages and tools to streamline the package creation and distribution workflow
for smaller scale personal projects.

## Installation

Install with:

<pre>
pip install hassle
</pre>

### Additional setup:

Install git and add it to your PATH if it already isn't.<br>
You will also need to register a [pypi account](https://pypi.org/account/register/) if you want to publish pip-installable packages to https://pypi.org with this tool.<br>
Once you've created and validated an account, you will need to follow the directions to generate an [api key](https://pypi.org/help/#apitoken).<br>
Copy the key and in your home directory, create a '.pypirc' file if it doesn't already exist.<br>
Edit the file so it contains the following (don't include the brackets around your api key):

<pre>
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-{The api key you copied}
</pre>

## Configuration

After installation and the above additional setup, it is a good idea to run the 'hassle_config' tool.
This isn't required and a blank config will be generated whenever another tool needs it if it doesn't exist.
This info, if provided, is used to populate a new project's 'pyproject.toml' file.
Invoking the tool with the -h switch shows the following:

<pre>
C:\python>hassle_config -h
usage: hassle_config [-h] [-n NAME] [-e EMAIL] [-g GITHUB_USERNAME] [-d DOCS_URL] [-t TAG_PREFIX]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Your name. This will be used to populate the 'authors' field of a packages 'pyproject.toml'.
  -e EMAIL, --email EMAIL
                        Your email. This will be used to populate the 'authors' field of a packages 'pyproject.toml'.
  -g GITHUB_USERNAME, --github_username GITHUB_USERNAME
                        Your github account name. When creating a new package, say with the name 'mypackage', the pyproject.toml 'Homepage' field will be set to 'https://github.com/{github_username}/mypackage' and the 'Source code' field will be set to
                        'https://github.com/{github_username}/mypackage/tree/main/src/mypackage'.
  -d DOCS_URL, --docs_url DOCS_URL
                        The template url to be used in your pyproject.toml file indicating where your project docs will be hosted. Pass the url such that the spot the actual package name will go is held by '$name', e.g. 'https://somedocswebsite/user/projects/$name'. If
                        'hassle_config.toml' didn't exist prior to running this tool and nothing is given for this arg, it will default to using the package's github url. e.g. for package 'mypackage' the url will be 'https://github.com/{your_github_name}/mypackage/tree/main/docs'
  -t TAG_PREFIX, --tag_prefix TAG_PREFIX
                        The tag prefix to use with git when tagging source code versions. e.g. hassle will use the current version in your pyproject.toml file to when adding a git tag. If you've passed 'v' to this arg and the version of your hypothetical package is '1.0.1', it will
                        be tagged as 'v1.0.1'. If 'hassle_config.toml' didn't exist prior to running this tool and you don't pass anything for this arg, it will default to ''.
</pre>

Invoking 'hassle_config' with no arguments will create a blank config if a config file doesn't already exist and it will also print where the config file is located so manual edits can be made.<br>
On a typical Python installation that'll look something like:

<pre>
C:\python>hassle_config
Manual edits can be made at C:\Users\%USER%\AppData\Local\Programs\Python\Python311\Lib\site-packages\hassle\hassle_config.toml
</pre>

## Generating New Projects
New projects are generated by invoking the "new_project" tool from your terminal.<br>
The -h/--help switch produces the following:

<pre>
C:\python>new_project -h
usage: new_project [-h] [-s [SOURCE_FILES ...]] [-d DESCRIPTION] [-dp [DEPENDENCIES ...]] [-k [KEYWORDS ...]] [-as] [-nl] [-os [OPERATING_SYSTEM ...]] name

positional arguments:
  name                  Name of the package to create in the current working directory.

options:
  -h, --help            show this help message and exit
  -s [SOURCE_FILES ...], --source_files [SOURCE_FILES ...]
                        List of additional source files to create in addition to the default __init__.py and {name}.py files.
  -d DESCRIPTION, --description DESCRIPTION
                        The package description to be added to the pyproject.toml file.
  -dp [DEPENDENCIES ...], --dependencies [DEPENDENCIES ...]
                        List of dependencies to add to pyproject.toml. Note: hassle.py will automatically scan your project for 3rd party imports and update pyproject.toml. This switch is largely useful for adding dependencies your project might need, but doesn't directly import in
                        any source files, like an os.system() call that invokes a 3rd party cli.
  -k [KEYWORDS ...], --keywords [KEYWORDS ...]
                        List of keywords to be added to the keywords field in pyproject.toml.
  -as, --add_script     Add section to pyproject.toml declaring the package should be installed with command line scripts added. The default is '{name} = "{name}.{name}:main". You will need to manually change this field.
  -nl, --no_license     By default, projects are created with an MIT license. Set this flag to avoid adding a license if you want to configure licensing at another time.
  -os [OPERATING_SYSTEM ...], --operating_system [OPERATING_SYSTEM ...]
                        List of operating systems this package will be compatible with. The default is OS Independent. This only affects the 'classifiers' field of pyproject.toml .
</pre>

Most of these options pertain to prefilling the generated 'pyproject.toml' file.<br>
As a simple example we'll create a new package called 'nyquil' with the following:

<pre>
C:\python>new_project nyquil -d "A package to help you sleep when you're sick." -k "sleep" "sick"
</pre>

You should see the following output:

<pre>
reformatted C:\python\nyquil\tests\test_nyquil.py

All done! ??? ???? ???
1 file reformatted.
Fixing C:\python\nyquil\tests\test_nyquil.py
Initialized empty Git repository in C:/python/nyquil/.git/
</pre>

A new folder in your current working directory called 'nyquil' should now exist.<br>
It should have the following structure:

<pre>
nyquil
|  |-.git
|  |  |-config
|  |  |-description
|  |  |-HEAD
|  |  |-hooks
|  |  |  |-applypatch-msg.sample
|  |  |  |-commit-msg.sample
|  |  |  |-fsmonitor-watchman.sample
|  |  |  |-post-update.sample
|  |  |  |-pre-applypatch.sample
|  |  |  |-pre-commit.sample
|  |  |  |-pre-merge-commit.sample
|  |  |  |-pre-push.sample
|  |  |  |-pre-rebase.sample
|  |  |  |-pre-receive.sample
|  |  |  |-prepare-commit-msg.sample
|  |  |  |-push-to-checkout.sample
|  |  |  |_update.sample
|  |  |
|  |  |-info
|  |  |  |_exclude
|  |
|  |-.gitignore
|  |-.vscode
|  |  |_settings.json
|  |
|  |-LICENSE.txt
|  |-pyproject.toml
|  |-README.md
|  |-src
|  |  |-nyquil
|  |  |  |-__init__.py
|  |  |  |_nyquil.py
|  |
|  |-tests
|  |  |_test_nyquil.py
</pre>

'new_project' has generated our project structure and files for us as well as initialized a git repository.<br>
**Note: By default 'new_project' adds an MIT License to the project. Pass the `-nl/--no_license` flag to prevent this behavior.**<br>
If you open the 'pyproject.toml' file it should look like the following except
for the 'project.authors' and 'project.urls' sections:

<pre>
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "nyquil"
description = "A package to help you sleep when you're sick."
version = "0.0.0"
requires-python = "3.0"
dependencies = []
readme = "README.md"
keywords = ["sleep", "sick"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]

[[project.authors]]
name = "Matt Manes"
email = "mattmanes@pm.me"

[project.urls]
"Homepage" = "https://github.com/matt-manes/nyquil"
"Documentation" = "https://github.com/matt-manes/nyquil/tree/main/docs"
"Source code" = "https://github.com/matt-manes/nyquil/tree/main/src/nyquil"

[tool.pytest.ini_options]
addopts = [
    "--import-mode=importlib",
    ]
pythonpath = "src"

[tool.hatch.build.targets.sdist]
exclude = [
    ".coverage",
    ".pytest_cache",
    ".vscode",
    "tests",
    ".gitignore"
    ]
[project.scripts]
</pre>

The package would do absolutely nothing, but with the generated files we do have the
viable minimum to build an installable python package.

## Generating Tests

While Hassle won't write your tests for you, 
it will generate the scaffolding to write tests for you.<br>
When you run the tool, it will scan the files in your 'src' directory
and generate placeholders for each function in the file and place
them in a test file in the 'tests' directory.<br>
If the test file already exists, functions will not be duplicated 
and existing content will not be overwritten, only appended to.

Let's navigate into our new 'nyquil' folder from the terminal:

<pre>
C:\python>cd nyquil
</pre>

**Note**: All of the following Hassle tools can be run from the parent folder of 'nyquil',
but you will need to specify the package name as the first argument, since we're navigating into 'nyquil' we can omit it.

Before we run the test generator tool, we need to add something to test.<br>
Open up the 'nyquil.py' file in the 'src' directory and add the following (be sure to save):

<pre>
from pathlib import Path

import tomlkit

root = Path(__file__).parent


def get_project_name() -> str:
    """Return the name of this project from its pyproject.toml file."""
    content = tomlkit.loads((root.parent.parent / "pyproject.toml").read_text())
    return content["project"]["name"]
</pre>

There are two ways to generate tests:<br>

<pre>
C:\python\nyquil>generate_tests
</pre>
and
<pre>
C:\python\nyquil>hassle -gt
</pre>

They both produce the same results, so we'll use the shorter one.<br>
After running `hassle -gt` in your terminal, look at the 'test_nyquil.py' file
inside the 'tests' folder.<br>
It should look like this:

<pre>
import pytest

from nyquil import nyquil


def test__nyquil__get_project_name():
    ...
</pre>

Go ahead and modify it to this (and save):

<pre>
import pytest

from nyquil import nyquil


def test__nyquil__get_project_name():
    assert "nyquil" == nyquil.get_project_name()
</pre>

## Running Tests

Similarly to generating tests, running tests can be done with either

<pre>
C:\python\nyquil>run_tests
</pre>

or 

<pre>
C:\python\nyquil>hassle -rt
</pre>

and as before we'll stick with the first.

Hassle uses [Pytest](https://pypi.org/project/pytest/) and [Coverage](https://pypi.org/project/coverage/) to run tests, so when we invoke the `hassle -rt` command,
we should see something like this:

<pre>
C:\python\nyquil>hassle -rt
================================================================================================================================== test session starts ==================================================================================================================================
platform win32 -- Python 3.11.0, pytest-7.2.1, pluggy-1.0.0
rootdir: C:\python\nyquil, configfile: pyproject.toml
plugins: anyio-3.6.2, hypothesis-6.63.0
collected 1 item

tests\test_nyquil.py .

=================================================================================================================================== 1 passed in 0.06s ===================================================================================================================================
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src\nyquil\__init__.py       0      0   100%
src\nyquil\nyquil.py         6      0   100%
tests\test_nyquil.py         4      0   100%
------------------------------------------------------
TOTAL                       10      0   100%
</pre>

For more about testing refer to the Pytest documentation.

## Building

Building the package is as simple as running the following:

<pre>
C:\python\nyquil>hassle -b
</pre>

which should produce

<pre>
All done! ??? ???? ???
3 files left unchanged.
Skipped 1 files
 [____________________________________________________________________________________________]-100.00% Scanning test_nyquil.py
* Creating venv isolated environment...
* Installing packages in isolated environment... (hatchling)
* Getting build dependencies for sdist...
* Building sdist...
* Building wheel from sdist
* Creating venv isolated environment...
* Installing packages in isolated environment... (hatchling)
* Getting build dependencies for wheel...
* Building wheel...
Successfully built nyquil-0.0.0.tar.gz and nyquil-0.0.0-py3-none-any.whl
</pre>


There should be two new folders in the top nyquil directory: "dist" and "docs".<br>
The "dist" folder contains the tar.gz and .whl files that are needed to install the package
and "docs" contains .html and .js files autogenerated by the [pdoc](https://pypi.org/project/pdoc/) package.<br>

The build command also invokes the [Vermin](https://pypi.org/project/vermin/) package to determine the minimum Python version
our package will support as well as the [Packagelister](https://pypi.org/project/packagelister/) package to determine our package's dependencies.<br>
hassle then updates the 'pyproject.toml' file with this new information.<br>
The version of pyproject that was generated initially showed this for "requires-python" and "dependencies":

<pre>
requires-python = "3.0"
dependencies = []
</pre>

but now it should show

<pre>
requires-python = ">=3.4"
dependencies = ["tomlkit~=0.11.6", "pytest~=7.2.1"]
</pre>

Another command line switch for Hassle that's relevant to this is the `-od/--overwrite_dependencies` flag.<br>
The defualt behavior of `hassle -b` is to append any new packages it finds to the dependencies list that aren't already there.<br>
This is good for when you've manually added dependencies your package needs that aren't explicitly imported in any of your source files.<br>
For instance, Hassle invokes a lot of things through the `os.system()` function, such as the [Black](https://pypi.org/project/black/) 
and [Isort](https://pypi.org/project/isort/) packages.<br>
Packagelister doesn't pick these up even though Hassle depends on them because they're never explicitly imported into a source file.<br>

However if our package doesn't have any manually added dependencies like that and, after some modifications from our first build,
we know there are some packages we were using that we don't use anymore, we can run

<pre>
C:\python\nyquil>hassle -b -od
</pre>

and our dependencies list will get overwritten, effectively removing the packages we no longer need in our project.


## Installing
We can install the package to our "site-packages" directory like any other package so that it's available to import with the command

<pre>
C:\python\nyquil>hassle -i
</pre>

## Publishing

Assuming you've set up a [PyPi](https://pypi.org/) account, generated the api key, and configured the '.pypirc' 
file as mentioned earlier, then you can publish the current version of your package by running

<pre>
C:\python\nyquil>hassle -p
</pre>


## Updating

After fixing some bugs or adding some features, you can increment your version number in the pyproject file
with the `-iv/--increment_version` flag using one of three arguments: `major`, `minor`, or `patch`. 
This follows the [semantic versioning standard](https://semver.org/)
so, if the project's current version is `1.3.7`, then

<pre>
>hassle -iv patch
</pre>

produces `1.3.8`,

<pre>
>hassle -iv minor
</pre>

produces `1.4.0`,

and

<pre>
>hassle -iv major
</pre>

produces `2.0.0`

## Git Stuff

#### Version Tagging

The command `>hassle -t` can be used to git tag your repo's current state according to the version number in the pyproject file
and the tag prefix in your hassle_config file we made earlier.

#### Committing

Using the `-ca/--commit_all` flag followed by a commit message with Hassle will git commit all uncommitted
files with the provided message.<br>
If you only pass "build" as the message, i.e. `>hassle -ca build`, all uncommitted files will be
committed with the message `chore: build v<pyproject.toml_version>`.<br>
This is particulary useful to run with the build flag so as to commit the files created and modified 
by the build process such as "dist", "docs", etc.

#### Syncing

**Note: This section requires Git and GitHub to be able to talk to each other.<br>
If you need help with that, look [here](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git).<br><br>
The `-s/--sync` flag can be used to sync your changes with your remote repo.<br>
Running
<pre>
>hassle -s
</pre>

really just invokes

<pre>
>git pull --tags origin main
>git push origin main:main --tags
</pre>

So for our example package 'nyquil', we can log into github and create an empty repository named "nyquil".<br>
Then, in your terminal, run the command
<pre>
C:\python\nyquil> git remote add origin https://github.com/{your-username}/nyquil.git
</pre>

Now you should be able to sync your local commits to GitHub using `>hassle -s`.

#### Changelog Generation

You can also generate a formatted changelog using `>hassle -uc`.<br>
This isn't strictly a Git operation, but it invokes the [auto-changelog](https://pypi.org/project/auto-changelog/) package and relies on
git version tagging, [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style commit messages, and your remote repo.

## Tying It All Together

Let's fastfoward in time and assume we've already published our 'nyquil' package as version `0.0.0`.<br>
We've decided to add some non-breaking additions to our package.<br>
Assuming we've dilligently done our tests and updated our readme, we can accomplish the whole build, publish, and sync process with the command
<pre>
C:\python\nyquil>hassle -b -t -i -iv minor -p -uc -ca build -s
</pre>

This will: 
* increment our pyproject version to `0.1.0`
* delete the previous distribution files
* update our package's dependencies
* update our package's minimum Python version
* generate updated documentation
* build the distributable 'tar.gz' and '.wheel' files
* update our changelog and git commit it with the message `chore: update changelog`
* git commit the rest of the modifications and additions with the message `chore: build v0.1.0`
* git tag the current code state as `<prefix_in_hassle_config_.toml>0.1.0`
* publish the updated package to PyPi
* install the package to our system
* sync everything to our remote repo.

For reference, here is the full `-h/--help` output for hassle:

<pre>
>hassle -h
usage: hassle [-h] [-b] [-t] [-i] [-iv INCREMENT_VERSION] [-p] [-rt] [-gt] [-uc] [-od] [-ca COMMIT_ALL] [-s] [package]

positional arguments:
  package               The name of the package or project to use, assuming it's a subfolder of your current working directory. Can also be a full path to the package. If nothing is given, the current working directory will be used.

options:
  -h, --help            show this help message and exit
  -b, --build           Build the package.
  -t, --tag_version     Add a git tag corresponding to the version in pyproject.toml.
  -i, --install         Install the package from source.
  -iv INCREMENT_VERSION, --increment_version INCREMENT_VERSION
                        Increment version in pyproject.toml. Can be one of "major", "minor", or "patch".
  -p, --publish         Publish package to PyPi. Note: You must have configured twine and registered a PyPi account/generated an API key to use this option.
  -rt, --run_tests      Run tests for the package.
  -gt, --generate_tests
                        Generate tests for the package.
  -uc, --update_changelog
                        Update changelog file.
  -od, --overwrite_dependencies
                        When building a package, packagelister will be used to update the dependencies list in pyproject.toml. The default behavior is to append any new dependencies to the current list so as not to erase any manually added dependencies that packagelister may not
                        detect. If you don't have any manually added dependencies and want to remove any dependencies that your project no longer uses, pass this flag.
  -ca COMMIT_ALL, --commit_all COMMIT_ALL
                        Git stage and commit all tracked files with this supplied commit message. If 'build' is passed, all commits will have message: 'chore: build v{current_version}
  -s, --sync            Pull from github, then push current commit to repo.
</pre>
