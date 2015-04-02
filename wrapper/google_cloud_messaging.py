# -*- coding: utf-8 -*-
import sys, os, pepper
import gcm

class BaseWrapperGoogleCloudMessaging:

    def __init__(self, api_key):
        self.api_key = api_key
        self.gcm = gcm.GCM(self.api_key)

    def send(self, registration_id, message, **kwargs):
        if type(registration_id) == list:
            registration_id_list = registration_id
        else:
            registration_id_list = [registration_id]

        r = self.gcm.json_request(registration_ids=registration_id_list, data=message, **kwargs)

        ret = {}
        for registration_id in registration_id_list:
            ret[registration_id] = {'status': 'success'}

        if 'errors' in r:
            for error, reg_ids in r['errors'].items():
                if error in ['NotRegistered', 'InvalidRegistration']:
                    for reg_id in reg_ids:
                        ret[reg_id]['status'] = 'error'
                        ret[reg_id]['message'] = error
                else:
                    for reg_id in reg_ids:
                        ret[reg_id]['status'] = 'fail'
                        ret[reg_id]['message'] = error

        if 'canonical' in r:
            for reg_id, canonical_id in r['canonical'].items():
                ret[reg_id]['status'] = 'canonical'
                ret[reg_id]['canonical_addr'] = canonical_id
                ret[reg_id]['message'] = 'Canonical: ' + canonical_id


        if type(registration_id) != list:
            return ret[registration_id]

        return ret
