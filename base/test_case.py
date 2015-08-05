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

    def assertStartsWith(self, s, value, msg=None):
        if not msg:
            msg = 'Expected %s to start with %s' % (repr(s), repr(value))
        self.assertTrue(s.startswith(value), msg)

    def assertEndsWith(self, s, value, msg=None):
        if not msg:
            msg = 'Expected %s to end with %s' % (repr(s), repr(value))
        self.assertTrue(s.endswith(value), msg)

    def assertInDict(self, key, adict, atype=None, value=None, length=None, min_length=None,
                     max_length=None, starts_with=None, ends_with=None, contains=None):

        self.assertEqual(type(adict), dict, 'Not a dict: %r' % adict)
        self.assertIn(key, adict)

        if atype is not None:
            self.assertEqual(type(adict[key]), atype)
        elif value is not None:
            self.assertEqual(type(adict[key]), type(value))

        if value is not None:
            self.assertEqual(adict[key], value)

        if length is not None:
            self.assertEqual(len(adict[key]), length)

        if min_length is not None:
            self.assertGreaterEqual(len(adict[key]), min_length)

        if max_length is not None:
            self.assertLessEqual(len(adict[key]), max_length)

        if starts_with is not None:
            self.assertStartsWith(adict[key], starts_with)

        if ends_with is not None:
            self.assertEndsWith(adict[key], ends_with)

        if contains is not None:
            self.assertIn(contains, adict[key])

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
