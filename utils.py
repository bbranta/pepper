# -*- coding: utf-8 -*-
import sys, os, pepper
import re, unicodedata

def deCamelCase(string):
    if string is None: return None

    normalize = lambda s:s.lower()
    pattern = re.compile('([A-Z][A-Z][a-z0-9])|([a-z0-9][A-Z])')
    normalized = normalize(pattern.sub(lambda m: m.group()[:1] + '_' + m.group()[1:], string))
    return normalized.replace('/', '.')

def camelCase(value, ucfirst = False, separator = ''):
    if type(value) == unicode:
        value = value.encode('utf-8')
    if not type(value) == str:
        raise Exception('Tipo invalido para camelCase: ' + repr(value))

    def camelcase():
        if ucfirst:
            yield str.capitalize
        else:
            yield str.lower

        while True:
            yield str.capitalize

    c = camelcase()
    return separator.join(c.next()(x) if x else '_' for x in re.split(r'[-_]', value))

def fileGetContents(filename):
    with open(filename) as f:
        return f.read()

def filePutContents(filename, contents, append=False):
    f = open(filename, 'a' if append else 'w')
    f.write(contents)
    f.close()

def removeDiacritic(s):
    #return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')
    if type(s) == str: s = s.decode('utf-8')
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

