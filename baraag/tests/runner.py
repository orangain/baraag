#coding: utf-8

import unittest

import baraag.tests

TEST_MODULES = [
    'baraag.tests.test_evernote',
]

def main():
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
