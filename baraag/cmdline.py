#coding: utf-8

from __future__ import absolute_import

import logging

from baraag.baraag import Baraag

def main():

    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    baraag = Baraag()
    baraag.start()
    # come here when the server was terminated
    baraag.shutdown()

if __name__ == '__main__':
    main()
