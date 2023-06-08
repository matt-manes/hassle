# Changelog

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
#### Others



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