# Changelog

## 2.5.0 (2023-04-15)

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