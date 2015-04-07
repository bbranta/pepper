# -*- coding: utf-8 -*-
import sys, os, pepper
import random
from pyapns.apns import APNs, Payload

class BaseWrapperApplePushNotificationService:

    def __init__(self, sandbox=True, cert_file=''):
        self.sandbox = sandbox
        self.cert_file = cert_file
        self.apns = None
        self.apns_level = 0

    def start(self):
        self.apns_level += 1

        if self.apns_level == 1:
            self.apns = APNs(cert_file=self.cert_file, use_sandbox=self.sandbox)

    def finish(self):
        self.apns_level -= 1

        if self.apns_level == 0:
            self.apns = None

    def send(self, device_token, message=None, sound='default', badge=1, **kwargs):
        self.start()

        identifier = random.getrandbits(32)
        payload = Payload(alert=message,
                            sound=sound,
                            badge=badge,
                            custom=kwargs)

        self.apns.gateway_server.send_notification(device_token, payload, identifier=identifier)

        self.finish()

    def feedback(self):
        self.start()

        print ' * Not implemented'
        for (token_hex, fail_time) in self.apns.feedback_server.items():
            print 'E', token_hex, fail_time

        self.finish()
