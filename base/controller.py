# -*- coding: utf-8 -*-
import sys, os, pepper

class Controller:
    __method = ''
    __methods = {}
    __args = []

    def __init__(self, args):
        if len(args) > 0: self.__method = args[0]
        if len(args) > 1: self.__args = args[1:]

        for f_name in dir(self):
            if f_name.startswith('option'):
                self.__methods[pepper.utils.deCamelCase(f_name[6:])] = f_name

    def execute(self):
        if not self.__method in self.__methods:
            if self.__method:
                print u' ! Error: method ' + repr(self.__method) + u' not found.\n'

            print 'Choose a valid method:'
            for method, f in self.__methods.items():
                func = getattr(self, f)
                print ' ' + sys.argv[0], sys.argv[1], method, func.__doc__
            return

        method = getattr(self, self.__methods[self.__method])
        method(*self.__args)
