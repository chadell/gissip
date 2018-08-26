# pylint: disable=attribute-defined-outside-init
import sys
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def parse_requirements(requirements_file):
    with open(requirements_file) as f:
        return f.read().strip().split('\n')


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)

        self.pytest_args = [
        ]

        self.lint_args = [
            '--flake8',
            '--pylint'
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.pytest_args.extend(self.lint_args)

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="gissip",
    version="0.0.1",
    author="Christian Adell",
    author_email="chadell@gmail.com",
    description="Script to observer commits of your loved repos",
    packages=find_packages(),
    entry_points={'console_scripts': [
        'gissip = gissip.main:main'
    ]},
    install_requires=parse_requirements(os.path.join('requirements', 'requirements.txt')),
    tests_require=parse_requirements(os.path.join('requirements', 'test_requirements.txt')),
    cmdclass={'test': PyTest},
    test_suite='tests',
)
