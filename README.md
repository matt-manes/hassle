# Hassle

Automate creating, building, testing, and publishing Python packages from the command line.   


## Installation

Install with:

<pre>
pip install hassle
</pre>

You should be able to type `hassle help` in your terminal and see a list of commands:
![](imgs/hassle_HassleShell.svg)


### Additional setup:

Install git and add it to your PATH if it isn't already.  
Some parts of this tool may require [communicating with Github]((https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)).  
You will also need to register a [pypi account](https://pypi.org/account/register/) if you want to publish packages to https://pypi.org with this tool.  
Once you've created and validated an account, you will need to follow the directions to generate an [api key](https://pypi.org/help/#apitoken).  
Copy the key and in your home directory, create a '.pypirc' file if it doesn't already exist.  
Edit the file so it contains the following (don't include the brackets around your api key):

![](imgs/pypirc.svg)

## Configuration

After installation and the above additional setup, it is a good idea to run the 'configure' command.
This isn't required and a blank config will be generated whenever it is needed if it doesn't exist.
This info, if provided, is used to populate a new project's 'pyproject.toml' file.
Typing `hassle help configure`:
![](imgs/hassle_configure.svg)

You can also view the current contents with the `config` command:
![](imgs/config.svg)

## Generating New Projects
New projects are generated with the `new` command:  
![](imgs/hassle_new.svg)

Most of these options pertain to prefilling the generated 'pyproject.toml' file.  
As a simple example we'll create a new package called 'nyquil':
![](imgs/new_use.svg)

A new folder in your current working directory called 'nyquil' should now exist.  
It should have the following structure:
![](imgs/folder_tree.svg)


**Note: By default an MIT License is added to the project. Pass the `-nl/--no_license` flag to prevent this behavior.**  
If you open the 'pyproject.toml' file it should look like the following except
for the 'project.authors' and 'project.urls' sections:
![](imgs/pyproject.svg)

The package would do absolutely nothing, but with the generated files we do have the
viable minimum to build an installable python package.


## Running Tests

Hassle uses [Pytest](https://pypi.org/project/pytest/) and [Coverage](https://pypi.org/project/coverage/) to run tests.  
When we invoke the `hassle test` command,
we should see something like this (pretending we have added test functions to `tests/test_nyquil.py`):
![](imgs/test.svg)


## Building

Building the package is as simple as using:

<pre>
>hassle build
</pre>

By default, the build command will:  
1. Run any tests in the `tests` folder (abandoning the build if any fail).  
2. Format source files with isort and black.  
3. Scan project import statements and add any missing packages to the pyproject `dependencies` field.  
4. Use [pdoc](https://pypi.org/project/pdoc/) to generate documentation (located in a created `docs` folder).  
5. Run `python -m build .` to generate the `tar.gz` and `.whl` files (located in a created `dist` folder).  


## Publishing

Assuming you've set up a [PyPi](https://pypi.org/) account, generated the api key, and configured the '.pypirc' 
file as mentioned earlier, then you can publish the current version of your package by running:

<pre>
>hassle publish
</pre>


## Updating

When the time comes to make changes to your package, the `hassle update` command makes it easy.  
This command needs at least one argument according to the type of update: `major`, `minor`, or `patch`.  
This argument tells Hassle how to increment the project version.  
Hassle uses the [semantic versioning standard](https://semver.org/),
so, for example, if your current version is `1.2.3` then 

`>hassle update major` bumps to `2.0.0`,  
`>hassle update minor` bumps to `1.3.0`,  
and  
`>hassle update patch` bumps to `1.2.4`.  

By default, the update command will:  
1. Run any tests in the `tests` folder (abandoning the update if any fail).  
2. Increment the project version.  
3. Run the build process as outlined above (minus step 1.).  
4. Make a commit with the message `chore: build {project_version}`.  
5. Git tag using the tag prefix in your `hassle_config.toml` file and the new project version.  
6. Generate/update the `CHANGELOG.md` file using [auto-changelog](https://pypi.org/project/auto-changelog/).  
(Normally `auto-changelog` overwrites the changelog file, but Hassle does some extra things so that any manual changes you make to the changelog are preserved).  
7. Git commit the changelog.  
8. Pull/push the current branch with the remote origin.  
9. Publish the updated package if the update command was run with the `-p` flag.  
10. Install the updated package if the update command was run with the `-i` flag.  

