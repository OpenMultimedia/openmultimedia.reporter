# -*- coding: utf-8 -*-

import hashlib
import httplib2
import json
import logging
import sys

from urllib import urlencode

from zope.component import getUtility

from zope.interface import implements

from plone.i18n.normalizer import idnormalizer

from plone.registry.interfaces import IRegistry

from openmultimedia.api.interfaces import IVideoAPI

from openmultimedia.reporter.interfaces import IUpload
from openmultimedia.reporter.interfaces import IReporterSettings

from openmultimedia.reporter.config import PROJECTNAME


logger = logging.getLogger(PROJECTNAME)


class Upload(object):

    implements(IUpload)

    def sign_request(self, params_dict, key, secret):
        params_dict['key'] = key
        cadena = u'%s' % secret
        for name in sorted(params_dict.iterkeys()):
            cadena += u'%s%s' % (name, params_dict[name])
        return hashlib.md5(cadena).hexdigest()

    def upload_url(self):

        video_api = getUtility(IVideoAPI)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IReporterSettings)

        multimedia_url = video_api.get_multimedia_url()
        upload_location = settings.upload_location

        return "%s/%s" % (multimedia_url, upload_location)

    def normalize_data(self, data):
        DATA_KEYS = ['titulo', 'descripcion']
        result = {}
        for key in data.keys():
            if key in DATA_KEYS:
                result[key] = idnormalizer.normalize(data[key])
            else:
                result[key] = data[key]
        return result

    def get_security_key(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IReporterSettings)
        security_key = settings.security_key

        return security_key

    def create_structure(self, data, file_type):

        video_api = getUtility(IVideoAPI)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IReporterSettings)

        multimedia_url = video_api.get_multimedia_url()
        image_notify = settings.image_notify
        video_notify = settings.video_notify
        security_key = settings.security_key
        key = settings.key

        if file_type == "image":
            url = "%s/%s" % (multimedia_url, image_notify)
        else:
            url = "%s/%s" % (multimedia_url, video_notify)

        body = self.normalize_data(data)
        headers = {'Accept': 'application/json'}

        sign_key = self.sign_request(body, key, security_key)
        body['signature'] = sign_key
        http = httplib2.Http()
        content_json = None
        try:
            logger.info("Making a request to: %s with headers: %s and body: %s"
                        % (url, headers, body))
            response, content = http.request(url, 'POST', headers=headers,
                                             body=urlencode(body))
        except:
            logger.info("There was an error when contacting the remote server: %s" % sys.exc_info()[0])
            response = {'status': '400'}
            content = None

        if content:
            content_json = json.loads(content)
        return response, content_json

    def publish_structure(self, slug, file_type):

        video_api = getUtility(IVideoAPI)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IReporterSettings)

        multimedia_url = video_api.get_multimedia_url()
        image_notify = settings.image_notify
        video_notify = settings.video_notify
        security_key = settings.security_key
        key = settings.key

        if file_type == "image":
            url = "%s/%s/%s" % (multimedia_url, image_notify, slug)
        else:
            url = "%s/%s/%s" % (multimedia_url, video_notify, slug)

        headers = {'Accept': 'application/json'}

        body = {'publicado': 'true'}
        sign_key = self.sign_request(body, key, security_key)
        body['signature'] = sign_key
        http = httplib2.Http()
        try:
            logger.info("Making a request to: %s with headers: %s and body: %s"
                        % (url, headers, body))
            response, content = http.request(url, 'PUT', headers=headers,
                                             body=urlencode(body))
        except:
            logger.info("There was an error when contacting the remote server: %s" % sys.exc_info()[0])
            response = {'status': '400'}
            content = ""
        return response, content

    def get_structure(self, slug, file_type):

        video_api = getUtility(IVideoAPI)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IReporterSettings)

        multimedia_url = video_api.get_multimedia_url()
        image_notify = settings.image_notify
        video_notify = settings.video_notify
        security_key = settings.security_key
        key = settings.key

        if file_type == "image":
            url = "%s/%s/%s" % (multimedia_url, image_notify, slug)
        else:
            url = "%s/%s/%s" % (multimedia_url, video_notify, slug)

        http = httplib2.Http()
        body = {}

        sign_key = self.sign_request(body, key, security_key)
        body['signature'] = sign_key
        headers = {'Accept': 'application/json'}
        body_url = urlencode(body)
        url = url + '?' + body_url
        try:
            logger.info("Making a request to: %s with headers: %s and body: %s"
                        % (url, headers, body))
            response, content = http.request(url, 'GET', headers=headers,
                                             body=urlencode(body))
        except:
            logger.info("There was an error when contacting the remote server: %s" % sys.exc_info()[0])
            response = {'status': '400'}

        content_json = None
        if response['status'] == '200':
            try:
                content_json = json.loads(content)
            except ValueError:
                logger.info("Invalid response content: %s" % content)
                content_json = {}

            if 'publicado' in content_json and not content_json['publicado']:
                self.publish_structure(slug, file_type)
            else:
                logger.info("Content is not yet published in remote server.")

        return response, content_json
