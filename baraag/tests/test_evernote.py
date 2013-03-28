#coding: utf-8

import os
import re
from unittest import TestCase
from cStringIO import StringIO

from baraag.evernote import enml_to_markdown

FIXTURES_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'fixtures')

class TestEnmlToMarkdown(TestCase):

    def test_convert_simple(self):
        self._test_convert('simple')

    def test_convert_multibyte(self):
        self._test_convert('multibyte')

    def test_convert_image(self):
        self._test_convert('image')

    def _test_convert(self, fixture):
        enml_path = os.path.join(FIXTURES_DIR, '%s_content.enml' % fixture)
        expected_md_path = re.sub(r'enml$', 'md', enml_path)

        with open(enml_path) as enml_file, open(expected_md_path) as expected_file:

            converted = StringIO()
            enml_to_markdown(enml_file, converted, '/images/')

            self.assertEqual(converted.getvalue(), expected_file.read().rstrip())

