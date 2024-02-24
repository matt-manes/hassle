# Changelog

## v3.1.8 (2024-02-24)

#### Others

* add 'imgs' and 'assets' to default sdist excludes


## v3.1.7 (2024-02-24)

#### Refactorings

* use `self.console.print` instead of `print`
#### Docs

* rewrite readme with svgs
#### Others

* reformat description strings
* add `!LICENSE.txt` to default ignore list
* add to gitignore


## v3.1.6 (2024-02-22)

#### Others

* `test` command can accept and pass arguments to pytest invocation


## v3.1.5 (2024-02-20)

#### Others

* add `create_py_typed()` to file generation


## v3.1.4 (2024-02-19)

#### Refactorings

* add `reportPrivateUsage = false` for pyright to default pyproject template


## v3.1.3 (2024-02-18)

#### Refactorings

* improve type annotation coverage
#### Others

* add to sdist excludes


## v3.1.2 (2024-02-15)

#### Fixes

* exclude files from coverage report and html generation that aren't in the cwd
* fix incorrect coverage numbers when testing a package imported by hassle or a package hassle imports


## v3.1.1 (2024-02-13)

#### Fixes

* strip quotes from name when running the `check_pypi` command
* prevent error when using `check_pypi` command from outside a hassel project


## v3.1.0 (2024-01-12)

#### Refactorings

* update packagelister usage


## v3.0.4 (2023-11-21)

#### Refactorings

* modify changelog formatting


## v3.0.3 (2023-11-21)

#### Fixes

* 'hassle help' does the same as 'hassle' from the command line
#### Performance improvements

* remove empty 'Others' headers from generated changelog

## v3.0.2 (2023-11-17)

#### Fixes

* fix changelog getting dumped as a list instead of a string when being generated for the first time

## v3.0.1 (2023-11-16)

#### Fixes

* don't include current package when updating dependencies


## v3.0.0 (2023-11-15)

#### Refactorings

* BREAKING: more or less completely rewrite package


## v2.13.4 (2023-11-04)

#### Fixes

* add changelog file before committing if it's untracked
#### Refactorings

* add '<3.12' to default requires-python field
* don't import pytest by default
#### Others

* add additional ignores


## v2.13.3 (2023-11-02)

#### Performance improvements

* add __version__ string to init during new project creation


## v2.13.2 (2023-09-22)

#### Fixes

* replace method of __init__ version updating

## v2.13.1 (2023-09-21)

#### Fixes

* change where `update_init_version` gets called to prevent init and pyproject from getting out of sync under certain conditions

## v2.13.0 (2023-09-21)

#### New Features

* add and update `__version__` in project's top level `__init__.py` file when using the `increment_version` arg
#### Others

* add `__version__` to init


## v2.12.4 (2023-08-19)

#### Refactorings

* update gitbetter usage

## v2.12.3 (2023-07-20)

#### Fixes

* prevent crashing when popping a key that doesn't exist

## v2.12.2 (2023-07-01)

#### Performance improvements

* add \*scratch* to gitignore template

## v2.12.1 (2023-06-13)

#### Others

* update gitbetter usage


## v2.12.0 (2023-06-07)

#### New Features

* add functionality to check if latest version of project has been published to pypi.org
#### Docs

* update readme

## v2.11.1 (2023-05-30)

#### Fixes

* fix sync command not properly pushing
#### Performance improvements

* replace 'main' with current branch in pull and push commands when syncing
#### Refactorings

* use gitbetter.Git.current_branch in on_primary_branch()

## v2.11.0 (2023-05-30)

#### New Features

* prompt user for confirmation when trying to publish a project that isn't on its main branch
* add on_primary_branch()
#### Performance improvements

* add choices param to -iv/--increment_version and -up/--update cli switches
#### Refactorings

* use gitbetter.Git context manager to capture output
* change git.pull and git.push args to just '--tags' in sync command
#### Docs

* update cli help message


## v2.10.3 (2023-05-26)

#### Fixes

* fix bug with determining the most recent tag
## v2.10.2 (2023-05-21)

#### Fixes

* fix startswith usage

#### Performance improvements

* add filters for changelog generation


## v2.10.0 (2023-05-21)

#### New Features

* new_project generates a modified pyproject.toml
#### Others

* update documentation


## v2.9.0 (2023-05-21)

#### New Features

* implement running changelog
#### Refactorings

* Running hassle with -up/--update arg doesn't set -i/--install to True
* change order of operations
#### Others

* add missing tag prefix
* update gitbetter usage to new package version


## v2.8.5 (2023-05-13)

#### Fixes

* fix sync command only pushing tags and not code


## v2.8.4 (2023-05-12)

#### Fixes

* run_tests() returns True if no tests are found


## v2.8.3 (2023-05-10)

#### Fixes

* fix bug where the package would get built before the version was incremented


## v2.8.2 (2023-05-10)

#### Fixes

* swap build and increment_version order so version isn't incremented if build/tests fail


## v2.8.1 (2023-05-10)

#### Fixes

* modify pip install invocation for better multi-platform support
#### Others

* remove unused import


## v2.8.0 (2023-05-09)

#### New Features

* add tests execution to build command
* add -st/--skip_tests flag to hassle parser
#### Fixes

* catch Black.main()'s SystemExit
* fix Pathier.mkcwd() usage
* invoke build with sys.executable instead of py
#### Refactorings

* replace os.system calls for black and isort with direct invocations
* replace os.system calls for git functions with gitbetter.git methods
* extract build process into it's own function
* make run_tests() invoke pytest and coverage directly and return pytest result
#### Others

* remove unused import


## v2.7.1 (2023-05-02)

#### Fixes

* remove update_minimum_python_version from build process since vermin is incorrectly reporting min versions
#### Refactorings

* set requires-python to >=3.10 in pyproject_template
#### Docs

* modify doc string formatting


## v2.7.0 (2023-04-28)

#### Refactorings

* add a pause to manually prune the changelog before committing the autoupdate


## v2.6.0 (2023-04-15)

#### Refactorings

* return minimum py version as string
* extract getting project code into separate function
* extract vermin scan into separate function


## v2.5.0 (2023-04-15)

#### Fixes

* fix already exist error by switching pathlib to pathier
#### Refactorings

* replace pathlib, os.chdir, and shutil calls with pathier
#### Others

* prune dependencies


## v2.4.0 (2023-04-07)

#### New Features

* implement manual override for 'tests' location
* generate_tests cli accepts individual files instead of only directories
#### Fixes

* add tests_dir.mkdir() to write_placeholders to keep pytest from throwing a fit
* fix not passing args.tests_dir param to test file generators
#### Refactorings

* generated test functions will have the form 'test_{function_name}'


## v2.3.2 (2023-04-02)

#### Refactorings

* install command will always isntall local copy b/c pypi doesn't update fast enough


## v2.3.1 (2023-03-31)

#### Fixes

* fix commit_all not adding untracked files in /dist


## v2.3.0 (2023-03-31)

#### New Features

* add -up/--update switch to hassle cli
#### Fixes

* add missing letter in commit_all git command
* fix pip install command arguments
#### Refactorings

* remove uneccessary git command in commit_all block
#### Others

* update readme


## v2.2.0 (2023-03-22)

#### New Features

* make dependency versions optional
* add alt structure for non-package projects


## v2.0.2 (2023-02-20)

#### Fixes

* add 'pip install -e .' cmd
* add missing '>=' to min py version in template


## v2.0.1 (2023-02-18)

#### Fixes

* change load_template to load_config
* fix project.urls in pyproject template