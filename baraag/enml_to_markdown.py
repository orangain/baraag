#coding: utf-8

from __future__ import unicode_literals

import sys
from xml import sax

class Handler(sax.handler.ContentHandler):

    def __init__(self, url_prefix):
        self.fragments = []
        self.url_prefix = url_prefix

        sax.handler.ContentHandler.__init__(self)

    def append(self, text):
        self.fragments.append(text)

    def startElement(self, name, attrs):
        #print name, attrs

        if name == 'br':
            self.append('\n')
        elif name == 'en-media':
            ext = attrs['type'].split('/')[1]
            file_uri = '%s/%s.%s' % (self.url_prefix, attrs['hash'], ext)
            self.append('![](%s)' % file_uri)

    def endElement(self, name):
        pass

    def characters(self, content):
        self.append(content)

    @property
    def text(self):
        return ''.join(self.fragments)

class EntityHandler(sax.handler.EntityResolver):

    def resolveEntity(self, publicId, systemId):
        #print publicId, systemId
        return sax.handler.EntityResolver.resolveEntity(self,publicId,systemId)

def main():
    url_prefix = sys.argv[1]

    handler = Handler(url_prefix)
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    parser.setEntityResolver(EntityHandler())
    parser.setFeature(sax.handler.feature_external_ges, False)
    parser.parse(sys.stdin)

    print handler.text.encode('utf-8')

if __name__ == '__main__':
    main()
