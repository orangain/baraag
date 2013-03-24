#coding: utf-8

from __future__ import print_function

import logging

from fsevents import Observer, Stream


class FileSystemNotifier(object):

    def __init__(self, target_dirs, callback):
        self.target_dirs = target_dirs
        self.callback = callback

    def start(self):
        self.stream = Stream(self.directory_changed, *self.target_dirs)

        self.observer = Observer()
        self.observer.schedule(self.stream)
        self.observer.daemon = True # Kill observer when main thread killed.
        self.observer.start() # start observer in the other thread.

    def directory_changed(self, subpath, mask):
        logging.debug('Directory changed: %s, %s' % (subpath, mask))
        self.callback(subpath, mask)

    def shutdown(self):
        self.observer.unschedule(self.stream)
        self.observer.stop()

if __name__ == '__main__':

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

    print('\n'.join("%s:\t0x%x" % (k, v) for k, v in flags))
