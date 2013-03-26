#coding: utf-8

from __future__ import print_function

import sys
import os
from xml import sax
from glob import glob

class Evernote(object):

    def __init__(self):
        self.find_note_dirs()

    def find_note_dirs(self):
        # Evernote app from App Store
        base_dir = os.path.join(os.environ['HOME'],
                'Library/Containers/com.evernote.Evernote/Data/Library/' +
                'Application Support/Evernote/accounts/Evernote/')
        content_dirs = glob(os.path.join(base_dir, '*/content/'))

        if content_dirs:
            self.base_dir = base_dir
            self.content_dirs = content_dirs
            return

        # Evernote app from Evernote's Web site?
        base_dir = os.path.join(os.environ['HOME'],
                'Library/Application Support/Evernote/accounts/Evernote/')
        content_dirs = glob(os.path.join(base_dir, '*/content/'))

        if content_dirs:
            self.base_dir = base_dir
            self.content_dirs = content_dirs
            return

        # Not found. Maybe not installed
        self.base_dir = None
        self.content_dirs = []

    def convert_to_markdown(self, note_dir, output, img_dir_url):
        if not note_dir.startswith(self.base_dir):
            raise IOError('Invalid note_dir: %s' % note_dir)

        img_url_prefix = img_dir_url + note_dir[len(self.base_dir):]

        enml_path = os.path.join(note_dir, 'content.enml')
        self.enml_to_markdown(open(enml_path), output, img_url_prefix)

    def enml_to_markdown(self, input, output, img_url_prefix):
        converter = EnmlMarkdownConverter(img_url_prefix)
        parser = sax.make_parser()
        parser.setContentHandler(converter)
        parser.setFeature(sax.handler.feature_external_ges, False)
        parser.parse(input)

        output.write(converter.text.encode('utf-8'))


class EnmlMarkdownConverter(sax.handler.ContentHandler):

    def __init__(self, img_url_prefix):
        self.fragments = []
        self.img_url_prefix = img_url_prefix

        sax.handler.ContentHandler.__init__(self)

    def append(self, text):
        self.fragments.append(text)

    def startElement(self, name, attrs):
        #print(name, attrs)

        if name == 'br':
            self.append('\n')
        elif name == 'en-media':
            ext = attrs['type'].split('/')[1]
            file_uri = '%s%s.%s' % (self.img_url_prefix, attrs['hash'], ext)
            self.append('![](%s)' % file_uri)

    def characters(self, content):
        self.append(content)

    @property
    def text(self):
        return u''.join(self.fragments)


def main():
    img_url_prefix = sys.argv[1]

    evernote = Evernote()
    evernote.enml_to_markdown(sys.stdin, sys.stdout, img_url_prefix)


if __name__ == '__main__':
    main()
