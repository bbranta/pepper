# -*- coding: utf-8 -*-
import sys, os, pepper
import urllib2, urllib, datetime, time, re
import base64, mimetypes
from pyquery import PyQuery

class BaseWrapperHttpConnection:
    username = None
    password = None
    headers = {}
    timeout = 10

    def __init__(self, base_url='', timeout=None):
        if '@' in base_url:
            init_url, end_url = base_url.split('@', 2)
            protocol, auth_data = init_url.split('://')
            username, password = auth_data.split(':')

            base_url = protocol + '://' + end_url
            self.setAuth(username, password)

        self.base_url = base_url
        if timeout:
            self.timeout = timeout

    def setAuth(self, username, password):
        self.username = username
        self.password = password

    def __encodeMultipartFormdata(self, fields, files):
        def get_content_type(filename):
            return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(str(value))
        for (key, f) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, f.filename))
            L.append('Content-Type: %s' % f.getMimeType())
            L.append('')
            L.append(f.read())
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def urlEncodeDict(self, get):
        get_list = []
        for k, v in get.items():
            if v == None:
                continue
            if isinstance(v, list):
                get_list.extend([(k + '[]', x) for x in v])
            else:
                get_list.append((k, v))

        return urllib.urlencode(get_list)

    def request(self, url, post=None, get=None, username=None, password=None, headers={}):
        if not username and not password:
            username = self.username
            password = self.password

        if not '://' in url:
            url = self.base_url + url

        # Prepara o POST e FILES
        files = []
        str_post = None
        if type(post) == dict:
            post_list = []
            for k, v in post.items():
                if v == None:
                    continue
                if isinstance(v, list):
                    post_list.extend([(k + '[]', x) for x in v])
#                elif isinstance(v, BaseWrapperFile):
#                    files.append((k, v))
                else:
                    post_list.append((k, v))

            str_post = urllib.urlencode(post_list)

        # Prepara o GET
        str_get = None
        if type(get) == dict:
            str_get = self.urlEncodeDict(get)

        if str_get:
            if not '?' in url: url += '?'
            else: url += '&'
            url += str_get

        # Prepara a requisição
        if files:
            content_type, body = self.__encodeMultipartFormdata(post_list, files)
            headers['Content-type'] = content_type
            headers['Content-length'] = str(len(body))
            request = urllib2.Request(url, body, headers)
        else:
            request = urllib2.Request(url, str_post)

        # Prepara os headers
        for k in headers:
            key = pepper.utils.camelCase(k.replace('_', '-'), ucfirst=True, separator='-')
            request.add_header(key, headers[k])

        if username and password:
            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            request.add_header('Authorization', 'Basic %s' % base64string)

        # Faz a requisição
        self.result = urllib2.urlopen(request, timeout=self.timeout)

        # Guarda os resultados
        self.code = self.result.code
        self.url = self.result.geturl()
        self.headers = self.result.info()
        self.contents = self.result.read()

        content_type = self.headers['Content-Type']

        return self.contents
