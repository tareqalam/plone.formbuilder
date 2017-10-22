# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI
from plone.app.testing import TEST_USER_ID, setRoles

from plone.formbuilder.testing import PLONE_FORMBUILDER_INTEGRATION_TESTING
from plone.formbuilder.content.schemaformdata import ISchemaFormData

import unittest2 as unittest


class SchemaFormDataIntegrationTest(unittest.TestCase):

    layer = PLONE_FORMBUILDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('SchemaFormFolder', 'formfolder')
        self.formfolder = self.portal.formfolder

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name='SchemaFormData')
        schema = fti.lookupSchema()
        self.assertEqual(ISchemaFormData, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='SchemaFormData'
        )
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='SchemaFormData'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISchemaFormData.providedBy(new_object))

    def test_adding(self):
        self.formfolder.invokeFactory(
            'SchemaFormData',
            'formforlderdata'
        )
        self.assertTrue(ISchemaFormData.providedBy(self.formfolder['formforlderdata']))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SchemaFormDataIntegrationTest))
    return suite
