#coding: utf-8

"""
Baraag, a small markdown preview server work with Evernote.app in Mac OS X.

Usage:
    baraag [options]

Options:
  -p <PORT>, --port=<PORT>  Server port. [default: 7777]
  -q, --quiet               Output minimum logs.
  --debug                   Output verbose debug logs.
"""

from __future__ import absolute_import

import logging

from docopt import docopt

from baraag.baraag import Baraag

def main():
    options = docopt(__doc__, version='0.2')

    port = int(options['--port'])

    if options['--quiet']:
        log_level = logging.ERROR
        debug = False
    elif options['--debug']:
        log_level = logging.DEBUG
        debug = True
    else:
        log_level = logging.INFO
        debug = False

    logging.basicConfig(level=log_level,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    baraag = Baraag(port=port, debug=debug)
    baraag.start()
    # come here when the server was terminated
    baraag.shutdown()

if __name__ == '__main__':
    main()
