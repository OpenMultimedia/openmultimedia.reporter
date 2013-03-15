# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from openmultimedia.api.interfaces import IAPISettings

from openmultimedia.reporter.interfaces import IUpload

from openmultimedia.reporter.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):
    """Ensure the NITF package is properly installed.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.utility = getUtility(IUpload)

    def test_signing(self):
        params = {'title': 'test title'}
        key = 'test-key'
        secret = 'secret-key'

        sign_should_be = 'abfbd09d1faf288c75e550c5a2ed2bb8'

        sign = self.utility.sign_request(params, key, secret)

        self.assertEqual(sign, sign_should_be)

    def test_upload_url(self):
        upload_url = self.utility.upload_url()
        upload_url_should_be = u'http://localhost:15555/upload'

        self.assertEqual(upload_url, upload_url_should_be)

    def test_normalize_data(self):
        title = u'!@Mi Título de prueba $'.encode("utf-8", "ignore")
        report = u'å∫çDescripción'.encode("utf-8", "ignore")

        data = {'titulo': title,
                'report': report}

        normalized_dict = self.utility.normalize_data(data)
        normalized_dict_should_be = {'report': report,
                                     'titulo': title}

        self.assertEqual(normalized_dict, normalized_dict_should_be)
        
        data = {'titulo': 'a'*150}
        # Title should be no longer than 120 chars
        normalized_dict = self.utility.normalize_data(data)
        normalized_dict_should_be = {'titulo': 'a'*120}

        self.assertEqual(normalized_dict, normalized_dict_should_be)
        

    def test_get_security_key(self):
        security_key = self.utility.get_security_key()
        security_key_should_be = u'security_key'

        self.assertEqual(security_key, security_key_should_be)

    def test_create_structure(self):

        file_types = ["image", "video"]

        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        for file_type in file_types:
            data = {'titulo': 'titulo',
                    'report': 'descripcion'}

            response, content = self.utility.create_structure(data, file_type)

            self.assertEqual(response['status'], '200')
            self.assertEqual(response['content-type'], 'application/octet-stream')
            self.assertEqual(content, {u'slug': u'valid-slug'})

            # Vamos a simular que en el servidor remoto devuelve contenido no Jsonable
            data['titulo'] = 'no-jsonable'

            response, content = self.utility.create_structure(data, file_type)

            self.assertEqual(response['status'], '200')
            self.assertIsNone(content)

            # Vamos a simular que en el servidor remoto se produjo un error
            data['titulo'] = 'error'

            response, content = self.utility.create_structure(data, file_type)

            self.assertEqual(response['status'], '400')
            self.assertIsNone(content)

            # Vamos a cambiar la url_base temporalmente para simular un timeout
            records.url_base = u"http://localhost:15556"
            response, content = self.utility.create_structure(data, file_type)
            # Devolvemos la url_base a como estaba
            records.url_base = u"http://localhost:15555"

            self.assertEqual(response['status'], '400')
            self.assertIsNone(content)

    def test_publish_structure(self):

        file_types = ["image", "video"]

        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        for file_type in file_types:
            slug = "valid-slug"

            response, content = self.utility.publish_structure(slug, file_type)

            self.assertEqual(response['status'], '200')
            self.assertEqual(content, '')

            # Vamos a simular que en el servidor remoto se produjo un error
            slug = "error-slug"

            response, content = self.utility.publish_structure(slug, file_type)

            self.assertEqual(response['status'], '400')
            self.assertEqual(content, '')

            # Vamos a cambiar la url_base temporalmente para simular un timeout
            records.url_base = u"http://localhost:15556"
            response, content = self.utility.publish_structure(slug, file_type)
            # Devolvemos la url_base a como estaba
            records.url_base = u"http://localhost:15555"

            self.assertEqual(response['status'], '400')
            self.assertEqual(content, '')

    def test_get_structure(self):
        file_types = ["image", "video"]

        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        for file_type in file_types:
            slug = "test-valid-slug"

            response, content = self.utility.get_structure(slug, file_type)

            self.assertEqual(response['status'], '200')
            self.assertEqual(content, {u'publicado': True, u'slug': u'valid-slug'})

            slug = "test-unpublished-valid-slug"

            response, content = self.utility.get_structure(slug, file_type)

            self.assertEqual(response['status'], '200')
            self.assertEqual(content, {u'publicado': False, u'slug': u'valid-slug'})

            # Vamos a simular que en el servidor remoto se produjo un error
            slug = "test-error-slug"

            response, content = self.utility.get_structure(slug, file_type)

            self.assertEqual(response['status'], '400')
            self.assertEqual(content, None)

            # Vamos a cambiar la url_base temporalmente para simular un timeout
            records.url_base = u"http://localhost:15556"
            response, content = self.utility.get_structure(slug, file_type)
            # Devolvemos la url_base a como estaba
            records.url_base = u"http://localhost:15555"

            self.assertEqual(response['status'], '400')
            self.assertEqual(content, None)

            slug = "test-invalid-response"

            response, content = self.utility.get_structure(slug, file_type)

            self.assertEqual(response['status'], '200')
            self.assertEqual(content, {})

    def test_delete_structure(self):
        file_types = ["image", "video"]

        for file_type in file_types:
            slug = "valid-response"

            response, content = self.utility.delete_structure(slug, file_type)

            self.assertEqual(response['status'], '204')
            self.assertEqual(content, '')

            slug = "invalid-response"

            response, content = self.utility.delete_structure(slug, file_type)

            self.assertEqual(response['status'], '404')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
