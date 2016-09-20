#!/usr/bin/env python
from __future__ import unicode_literals
import codecs
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import actistream


class DjangoTests(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from django.core import management
        DSM = 'DJANGO_SETTINGS_MODULE'
        if DSM not in os.environ:
            os.environ[DSM] = 'actistream.tests.settings'
        management.execute_from_command_line()


def read_files(*filenames):
    """
    Output the contents of one or more files to a single concatenated string.
    """
    output = []
    for filename in filenames:
        f = codecs.open(filename, encoding='utf-8')
        try:
            output.append(f.read())
        finally:
            f.close()
    return '\n\n'.join(output)

# Dynamically calculate the version based on actistream.VERSION.
version = actistream.__version__

setup(
    name='django-actistream',
    version=version,
    url='http://github.com/pennersr/django-actistream',
    description='Activities & notifications for Django',
    long_description=read_files('README.rst'),
    author='Raymond Penners',
    author_email='raymond.penners@intenct.nl',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.9',
    ],
    cmdclass={'test': DjangoTests},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
