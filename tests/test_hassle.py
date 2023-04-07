import os
import shutil

import pytest
from pathier import Pathier

from hassle import generate_tests, new_project

root = Pathier(__file__).parent
dummy_functions = ["one", "two", "three", "check_check", "is_this_thing_on"]
more_dummy_functions = ["four", "five", "six"]


def test__generatetests__get_function_names():
    functions = generate_tests.get_function_names(
        root / "dummy" / "src" / "dummy" / "dummy.py"
    )
    for function in dummy_functions:
        assert function in functions
    assert len(dummy_functions) == len(functions)
    assert dummy_functions == functions


def test__generatetests__write_placeholders():
    startdir = Pathier.cwd()
    os.chdir(startdir / "tests" / "dummy")
    generate_tests.write_placeholders(
        Pathier(startdir / "tests" / "dummy"), "dummy.py", dummy_functions
    )
    test_dummy_path = startdir / "tests" / "dummy" / "tests" / "test_dummy.py"
    assert test_dummy_path.exists()
    content = test_dummy_path.read_text()
    for function in dummy_functions:
        assert f"def test_{function}():\n    ..." in content
    shutil.rmtree(test_dummy_path.parent)
    os.chdir(startdir)


def test__generatetests__generate_test_files():
    package_path = Pathier.cwd() / "tests" / "dummy"
    generate_tests.generate_test_files(package_path)
    test_dummy_path = package_path / "tests" / "test_dummy.py"
    content = test_dummy_path.read_text()
    for function in dummy_functions:
        assert f"def test_{function}():\n    ..." in content

    test_more_dummy_path = package_path / "tests" / "test_more_dummy.py"
    content = test_more_dummy_path.read_text()
    for function in more_dummy_functions:
        assert f"def test_{function}():\n    ..." in content

    shutil.rmtree(test_dummy_path.parent)


def test__generatetests__main():
    class MockArgs:
        def __init__(self, package_name, tests_dir=None):
            self.paths = [package_name]
            self.tests_dir = tests_dir

    for arg in ["dummy", "."]:
        if arg == "dummy":
            os.chdir(root)
        if arg == ".":
            os.chdir(root / "dummy")
        args = MockArgs(arg)

        generate_tests.main(args)
        test_dummy_path = root / "dummy" / "tests" / "test_dummy.py"
        content = test_dummy_path.read_text()
        for function in dummy_functions:
            assert f"def test_{function}():\n    ..." in content

        test_more_dummy_path = root / "dummy" / "tests" / "test_more_dummy.py"
        content = test_more_dummy_path.read_text()
        for function in more_dummy_functions:
            assert f"def test_{function}():\n    ..." in content

    test_dummy_path.parent.delete()
    # ================================single file================================
    os.chdir(root / "dummy")
    args = MockArgs("src/dummy/dummy.py", "secondary_tests_dir")
    generate_tests.main(args)
    test_dummy_path = root / "dummy" / "secondary_tests_dir" / "test_dummy.py"
    content = test_dummy_path.read_text()
    for function in dummy_functions:
        assert f"def test_{function}():\n    ..." in content
    shutil.rmtree(test_dummy_path.parent)


def test__new_project__main():
    class MockArgs:
        def __init__(self):
            self.name = "dummypack"
            self.source_files = ["__init__.py", f"{self.name}.py"]
            self.description = "dummypack"
            self.dependencies = ["dep1", "dep2"]
            self.keywords = ["key1", "key2"]
            self.add_script = True
            self.no_license = False
            self.operating_system = None
            self.not_package = False

    os.chdir(root)
    args = MockArgs()
    new_project.main(args)
    name = "dummypack"
    dumpath = root / name

    def assert_exists(file: str | Pathier) -> Pathier:
        """Assert file exists and return
        Path object to file"""
        file_path = dumpath / file
        assert file_path.exists()
        return file_path

    assert dumpath.exists()
    readme = assert_exists("README.md")
    assert name in readme.read_text()
    pypr = assert_exists("pyproject.toml")
    pypr_content = pypr.read_text()
    for i in [args.dependencies, args.keywords]:
        for x in i:
            assert x in pypr_content
    assert f"{name}.{name}:main" in pypr_content
    dummysrc = assert_exists(Pathier("src") / name)
    assert (dummysrc / "__init__.py").exists()
    assert (dummysrc / f"{name}.py").exists()
    tests = assert_exists("tests")
    assert (tests / f"test_{name}.py").exists()
    assert_exists(".gitignore")
    assert_exists("LICENSE.txt")
    assert_exists(".vscode")
    assert_exists(".git")
    os.chdir(root.parent)
    shutil.rmtree(dumpath)
