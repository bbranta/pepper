# -*- coding: utf-8 -*-
import sys, os, pepper
import unittest

class TestCase(unittest.TestCase):

    def assertEqual(self, v1, v2, *args, **kwargs):
        x1 = v1.decode('utf-8') if type(v1) == str else v1
        x2 = v2.decode('utf-8') if type(v2) == str else v2
        if x1 == str: x1 = unicode
        if x2 == str: x2 = unicode
        super(TestCase, self).assertEqual(x1, x2, *args, **kwargs)

    def assertInDict(self, key, adict, atype=None, value=None, length=None):
        self.assertIn(key, adict)

        if atype != None:
            self.assertEqual(type(adict[key]), atype)
        elif value != None:
            self.assertEqual(type(adict[key]), type(value))

        if value != None:
            self.assertEqual(adict[key], value)

    def getTests(self, test_func='all'):
        r = []
        if test_func == 'all':
            for f in dir(self):
                if not f.startswith('test'): continue
                r.append(self.__class__(f))
        else:
            f = 'test' + pepper.utils.camelCase(test_func, ucfirst=True)
            r.append(self.__class__(f))

        return r

    def runTest(self):
        pass
