#coding: utf-8

from __future__ import print_function

import re
import logging
import inspect

from moo import moo
from moo.cmdline import open_local_url

# BEGIN used in exec build_app_source
import os
import bottle
from bottle import Bottle
from moo.server import StoppableCherryPyServer
from moo.moo import DEFAULT_STATIC_FILES_DIR, Markup
# END used in exec build_app_source


class MarkdownPreviewServer(object):

    def __init__(self, markdown_path, note_base_dir, port=7777, debug=False, quiet=True):
        self.markdown_path = markdown_path
        self.note_base_dir = note_base_dir
        self.port = port
        self.debug = debug
        self.quiet = quiet

    def start(self):
        # insert custom note handler into moo.build_app function
        build_app_source = inspect.getsource(moo.build_app)
        build_app_source = re.sub(r'return run_app', """

    @app.route('/note/<filename:path>')
    def handle_note(filename):
        logging.debug('note: %s' % filename)
        return bottle.static_file(filename, root=note_base_dir)

    return run_app
        """, build_app_source) # indent is IMPORTANT!

        #print(build_app_source)

        in_vars = {
            'os': os,
            'logging': logging,
            'bottle': bottle,
            'Bottle': Bottle,
            'StoppableCherryPyServer': StoppableCherryPyServer,
            'DEFAULT_STATIC_FILES_DIR': DEFAULT_STATIC_FILES_DIR,
            'Markup': Markup,
            'note_base_dir': self.note_base_dir,
        }
        out_vars = {}

        # defines function 'build_app' which returns function
        exec(build_app_source, in_vars, out_vars)
        build_app = out_vars['build_app']

        try:
            open_local_url(self.port)
        except:
            pass

        print('Preview on http://127.0.0.1:%d' % self.port)
        print('Hit Ctrl-C to quit.')

        app = build_app(
                filename=self.markdown_path, port=self.port,
                debug=self.debug, quiet=self.quiet)

        logging.debug('starting server at port %d', self.port)
        app()
