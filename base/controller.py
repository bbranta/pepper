# -*- coding: utf-8 -*-
import sys, os, pepper

class Controller:
    __methods = {}
    __args = []
    __kwargs = {}

    def __init__(self):
        for f_name in dir(self):
            if f_name.startswith('option'):
                self.__methods[pepper.utils.deCamelCase(f_name[6:])] = f_name

    def validMethod(self, method):
        return method in self.__methods

    def printMethods(self):
        for method, f in self.__methods.items():
            func = getattr(self, f)
            print ' ' + sys.argv[0], sys.argv[1], method, func.__doc__

    def setMethod(self, method):
        if not self.validMethod(method):
            return False

        function_name = self.__methods[method]
        function = getattr(self, function_name)

        self.__method = {
            'option'    : method,
            'f_name'    : function_name,
            'function'  : function,
        }

    def setArgs(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        if not self.__method:
            print ' ! Error: Method not set'
            return

        return self.__method['function'](*self.__args, **self.__kwargs)
