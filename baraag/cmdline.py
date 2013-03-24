#coding: utf-8

import logging

def main():

    from baraag.baraag import Baraag

    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    baraag = Baraag()
    baraag.start()
    # come here when the server was terminated
    baraag.shutdown()

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
