#coding: utf-8

import os
import tempfile
import signal
import logging

from .fsevents_wrapper import FileSystemNotifier
from .moo_wrapper import MarkdownPreviewServer
from .evernote import Evernote

TEMP_MARKDOWN_PATH = os.path.join(tempfile.gettempdir(), 'baraag.md')

class Baraag(object):

    def __init__(self, port=7777, debug=False):
        self.last_updated_dir = None
        self.evernote = Evernote()

        content_dirs = self.evernote.get_content_dirs()
        if len(content_dirs) == 0:
            logging.error('Evernote content directory not found!')
            raise IOError('Evernote content directory not found!')

        self.fs_notifier = FileSystemNotifier(
            target_dirs=content_dirs,
            callback=self.directory_changed,
        )
        self.md_server = MarkdownPreviewServer(
            markdown_path=TEMP_MARKDOWN_PATH,
            port=port,
            debug=debug,
        )

    def start(self):
        self.ensure_temp_markdown()
        signal.signal(signal.SIGALRM, self.deferred_directory_changed)
        self.fs_notifier.start()
        self.md_server.start() # wait until the md_server terminated

    def ensure_temp_markdown(self):
        # Should I always override temp file when baraag starting?
        if not os.path.exists(TEMP_MARKDOWN_PATH):
            logging.debug('Creating welcome message in %s' % TEMP_MARKDOWN_PATH)
            with open(TEMP_MARKDOWN_PATH, 'w') as f:
                f.write("""
# Welcome to Baraag!

Try write and save a note in Markdown format with Evernote.app.

EvernoteアプリでMarkdown形式のノートを書いて保存してみてください。
""")

    def shutdown(self):
        self.fs_notifier.shutdown()

    def directory_changed(self, subpath, mask):
        self.last_updated_dir = subpath

        # Defer notification to handle multiple notifications.
        # Calling multiple setitimer results in one time signal callback.
        signal.setitimer(signal.ITIMER_REAL, 0.5)

    def deferred_directory_changed(self, signum, frame):
        logging.debug('Deferred directory changed: %s, %s' % (signum, frame))

        img_url_prefix = '/note/' + ('/'.join(self.last_updated_dir.split('/')))
        self.evernote.convert_to_markdown(
            note_dir=self.last_updated_dir,
            output=open(TEMP_MARKDOWN_PATH, 'w'),
            img_url_prefix=img_url_prefix)

        # When the markdown file is updated, the browser will automatically reload.
