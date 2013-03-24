#coding: utf-8

import os

from setuptools import setup, find_packages

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

setup(
    name = 'baraag',
    version = '0.1dev',
    packages = find_packages(),
    install_requires = [
        'MacFSEvents',
        'moo',
        'docopt',
    ],
    author = 'orangain',
    author_email = 'orangain@gmail.com',
    license = "MIT",
    platforms = ["Mac OS X"],
    url = 'https://github.com/orangain/baraag',
    long_description = read('README.md'),
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
        'Topic :: Utilities',
    ],
)
