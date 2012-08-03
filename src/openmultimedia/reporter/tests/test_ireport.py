# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from openmultimedia.reporter.content.ireport import IIReport
from openmultimedia.reporter.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('openmultimedia.reporter.ireport', 'test-i-report')
        self.folder = self.portal['test-i-report']

    def test_adding(self):
        self.assertTrue(IIReport.providedBy(self.folder))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.reporter.ireport')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.reporter.ireport')
        schema = fti.lookupSchema()
        self.assertEquals(IIReport, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.reporter.ireport')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IIReport.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
