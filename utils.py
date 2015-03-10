# -*- coding: utf-8 -*-
import json
import random
import sys, os, pepper
import re, unicodedata, cgi


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


def fileGetContents(filename, encoding="text"):
    with open(filename) as f:
        text = f.read()

    if encoding == "text":
        return text

    if encoding == "json":
        return json.loads(text)

    return None


def filePutContents(filename, contents, append=False, encoding="text"):
    if encoding == "json":
        contents = json.dumps(contents)

    elif encoding != "text":
        return None

    f = open(filename, 'a' if append else 'w')
    f.write(contents)
    f.close()


def removeDiacritic(s):
    if type(s) == str: s = s.decode('utf-8')
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def htmlEntities(s):
    return cgi.escape(s).encode('ascii', 'xmlcharrefreplace')


def _getCPFVerifDigit(val):
    if len(val) != 9 or not val.isdigit():
        return False

    a = 10
    for c in range(0, 2):
        total = 0
        for i in range(0, c + 9):
            total += int(val[i]) * a
            a -= 1
        val += str((11 - (total % 11)) % 10)
        a = 11

    return val[9:11]

def validCPF(val):
    val = str(val) if type(val) != str else val.replace('.', '').replace('-', '')
    dig = _getCPFVerifDigit(val[0:9])
    if not dig:
        return False

    return val[9:] == dig

def randomCPF():
    n = str(random.randrange(100100100, 999000999))
    return n + _getCPFVerifDigit(n)