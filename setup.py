#!/usr/bin/env python
from setuptools import setup

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
      )
