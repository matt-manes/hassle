# Changelog

## 2.8.3 (2023-05-10)

#### Fixes

* fix bug where the package would get built before the version was incremented
#### Others

* build v2.8.2


## v2.8.2 (2023-05-10)

#### Fixes

* swap build and increment_version order so version isn't incremented if build/tests fail
#### Others

* build v2.8.2
* update changelog


## v2.8.1 (2023-05-10)

#### Fixes

* modify pip install invocation for better multi-platform support
#### Others

* build v2.8.1
* update changelog
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

* replace os.system call to git with gitbetter.git methods
* replace os.system calls for black and isort with direct invocations
* extract build process into it's own function
* make run_tests() invoke pytest and coverage directly and return pytest result
#### Others

* build v2.8.0
* update changelog
* remove unused import


## v2.7.1 (2023-05-02)

#### Fixes

* remove update_minimum_python_version from build process since vermin is incorrectly reporting min versions
#### Refactorings

* set requires-python to >=3.10 in pyproject_template
#### Docs

* modify doc string formatting
#### Others

* build v2.7.1
* update changelog


## v2.7.0 (2023-04-28)

#### Refactorings

* add a pause to manually prune the changelog before committing the autoupdate
#### Others

* build v2.7.0
* update changelog


## v2.6.0 (2023-04-15)

#### Refactorings

* return minimum py version as string
* extract getting project code into separate function
* extract vermin scan into separate function
#### Others

* build v2.6.0


## v2.5.0 (2023-04-15)

#### Fixes

* fix already exist error by switching pathlib to pathier
#### Refactorings

* replace pathlib, os.chdir, and shutil calls with pathier
#### Others

* build v2.5.0
* update changelog
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
#### Others

* build v2.4.0
* update changelog


## v2.3.2 (2023-04-02)

#### Refactorings

* install command will always isntall local copy b/c pypi doesn't update fast enough
#### Others

* build v2.3.2
* update changelog


## v2.3.1 (2023-03-31)

#### Fixes

* fix commit_all not adding untracked files in /dist
#### Others

* build v2.3.1
* update changelog
* build v2.3.0


## v2.3.0 (2023-03-31)

#### New Features

* add -up/--update switch to hassle cli
#### Fixes

* add missing letter in commit_all git command
* fix pip install command arguments
#### Refactorings

* remove uneccessary git command in commit_all block
#### Others

* build v2.3.0
* update changelog
* update readme


## v2.2.0 (2023-03-22)

#### New Features

* make dependency versions optional
* add alt structure for non-package projects
#### Others

* build v2.2.0
* update changelog


## v2.0.2 (2023-02-20)

#### Fixes

* add 'pip install -e .' cmd
* add missing '>=' to min py version in template
#### Others

* build v2.0.2
* update changelog


## v2.0.1 (2023-02-18)

#### Fixes

* change load_template to load_config
* fix project.urls in pyproject template
#### Others

* build v2.0.1
* update changelog


## v2.0.0 (2023-02-18)

#### Others

* build v2.0.0