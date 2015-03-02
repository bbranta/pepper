# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os, pepper

class BaseWrapperDebug:
    default_level = 1
    levels = {
        'NONE'      : 0,
        'ERROR'     : 1,
        'WARNING'   : 2,
        'VERBOSE'   : 3,
    }

    def __init__(self, tag, debug_level=0):
        self.tag = tag

        if not debug_level:
            self.debug_level = 0
        elif not debug_level in self.levels:
            self.debug_level = self.default_level
            self.log('ERROR', 'Invalid debug level %s' % repr(debug_level))
        else:
            self.debug_level = self.levels[debug_level]

    def checkLevel(self, debug_level):
        return self.levels[debug_level] <= self.debug_level

    def log(self, debug_level, *args, **kwargs):
        if not self.checkLevel(debug_level): return

        print('[%s][%s]' % (self.tag, debug_level), *args, **kwargs)
