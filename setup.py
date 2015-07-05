#!/usr/bin/env python
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["tests"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README') as file_:
    LONG_DESCRIPTION = file_.read()


setup(name='jscrambler',
      version='2.0b1',
      description='Submit javascript obfuscation jobs to jscrambler.com',
      author='Audit Mark',
      author_email='support@jscrambler.com',
      url='https://github.com/auditmark/python-jscrambler',
      packages=['jscrambler',
                'jscrambler.management',
                'jscrambler.management.commands',
                ],
      scripts=["jscrambler-tool"],
      zip_safe=False,
      long_description=LONG_DESCRIPTION,
      install_requires=["requests"],
      test_suite='tests',
      tests_require=["httmock", "pytest"],
      cmdclass={'test': PyTest},
      )
