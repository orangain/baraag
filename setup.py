#coding: utf-8

import os

from setuptools import setup, find_packages

long_description = """
Baraag
======

Baraag is a small server to preview Markdown-formatted note in Evernote
with browser.

Installation
------------

::

    $ pip install baraag

Baraag is tested with Python 2.7 on Mac OS X 10.7+ (Lion and Mountain
Lion).

Usage
-----

::

    $ baraag

Then, write and save a note in Markdown with Evernote app. You will see
a formatted note in your browser. The preview is automatically reloaded
when you save a note.

Dependency
----------

I appreciate these libraries:

-  `moo <https://github.com/metaphysiks/moo>`__
-  `macfsevents <https://github.com/malthe/macfsevents>`__
-  `docopt <https://github.com/docopt/docopt>`__
"""

setup(
    name = 'baraag',
    version = '0.1dev',
    packages = find_packages(),
    package_data = {
        'baraag': ['tests/*.md', 'tests/*.enml'],
    },
    install_requires = [
        'MacFSEvents',
        'moo',
        'docopt',
    ],
    test_suite = 'baraag.tests',
    author = 'orangain',
    author_email = 'orangain@gmail.com',
    license = "MIT",
    platforms = ["Mac OS X"],
    url = 'https://github.com/orangain/baraag',
    description = 'Markdown preview server work with Evernote in Mac',
    long_description = long_description,
    keywords = ['evernote', 'markdown', 'preview'],
    entry_points = {
        'console_scripts': [
            'baraag = baraag.cmdline:main',
        ],
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)
