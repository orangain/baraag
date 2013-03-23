#coding: utf-8

import signal
import sys
import subprocess

def alerm_handler(signum, frame):
    print "got signal"

    global updated_path
    update_markdown(updated_path)
    updated_path = None

signal.signal(signal.SIGALRM, alerm_handler)


from fsevents import *
flags = (
    ('CF_POLLIN', CF_POLLIN),
    ('CF_POLLOUT', CF_POLLOUT),
    ('FS_IGNORESELF', FS_IGNORESELF),
    ('FS_FILEEVENTS', FS_FILEEVENTS),
    ('FS_ITEMCREATED', FS_ITEMCREATED),
    ('FS_ITEMREMOVED', FS_ITEMREMOVED),
    ('FS_ITEMINODEMETAMOD', FS_ITEMINODEMETAMOD),
    ('FS_ITEMRENAMED', FS_ITEMRENAMED),
    ('FS_ITEMMODIFIED', FS_ITEMMODIFIED),
    ('FS_ITEMFINDERINFOMOD', FS_ITEMFINDERINFOMOD),
    ('FS_ITEMCHANGEOWNER', FS_ITEMCHANGEOWNER),
    ('FS_ITEMXATTRMOD', FS_ITEMXATTRMOD),
    ('FS_ITEMISFILE', FS_ITEMISFILE),
    ('FS_ITEMISDIR', FS_ITEMISDIR),
    ('FS_ITEMISSYMLINK', FS_ITEMISSYMLINK),
    ('X_KernelDropped', 0x04),
    ('X_RootChanged', 0x20),
    ('X_Mount', 0x40),
    ('X_Unmount', 0x80),
)

#print '\n'.join("%s:\t0x%x" % (k, v) for k, v in flags)
#exit()

from fsevents import Observer
observer = Observer()
observer.daemon = True # Kill observer when main thread killed.
observer.start() # start observer in the other thread.

updated_path = None

def callback(subpath, mask):
    print '----'
    print subpath, mask
    for name, flag in flags:
        if mask & flag > 0:
            print name
            mask -= flag
    print mask

    global updated_path
    updated_path = subpath[:-1]
    print signal.setitimer(signal.ITIMER_REAL, 0.5)

def update_markdown(path):
    args = ['python', 'enml_to_markdown.py', '/'.join(path.split('/')[-2:])]

    subprocess.call(args, stdin=open(path + '/content.enml'), stdout=open(markdown_file, 'w'))

from fsevents import Stream
from glob import glob
note_dir = glob(os.path.join(os.environ['HOME'], 'Library/Containers/com.evernote.Evernote/Data/Library/Application Support/Evernote/accounts/Evernote/*/content/'))[0]

stream = Stream(callback, note_dir)
observer.schedule(stream)

#print 'Press Ctrl+C'

from moo import moo
from moo.cmdline import open_local_url
import logging

import os
import tempfile
import bottle
from bottle import Bottle
from moo.server import StoppableCherryPyServer
from moo.moo import DEFAULT_STATIC_FILES_DIR, Markup

import inspect
import re

# insert custom note handler into moo.build_app function
build_app_source = inspect.getsource(moo.build_app)
build_app_source = re.sub(r'return run_app', """

    @app.route('/note/<filename:path>')
    def handle_note(filename):
        logging.debug('note: %s' % filename)
        return bottle.static_file(filename, root=note_dir)

    return run_app
""", build_app_source)

print build_app_source
exec build_app_source

port = 7777
debug=True
quiet=False
markdown_file = os.path.join(tempfile.gettempdir(), 'baraag.md')
print markdown_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

try:
    open_local_url(port)
except:
    pass

print 'Preview on http://127.0.0.1:%d' % port
print 'Hit Ctrl-C to quit.'

app = build_app(filename=markdown_file, port=port, debug=debug, quiet=quiet)

logging.debug('starting server at port %d', port)
app()

print 'moo ended'

observer.unschedule(stream)
observer.stop()

print 'Exit!'
