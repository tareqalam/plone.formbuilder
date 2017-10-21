# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI
from plone.app.testing import TEST_USER_ID, setRoles

from plone.formbuilder.testing import PLONE_FORMBUILDER_INTEGRATION_TESTING
from plone.formbuilder.content.schemaformfolder import ISchemaFormFolder

import unittest2 as unittest


class SchemaFormFolderIntegrationTest(unittest.TestCase):

    layer = PLONE_FORMBUILDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name='SchemaFormFolder')
        schema = fti.lookupSchema()
        self.assertEqual(ISchemaFormFolder, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='SchemaFormFolder'
        )
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='SchemaFormFolder'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISchemaFormFolder.providedBy(new_object))

    def test_adding(self):
        self.portal.invokeFactory(
            'SchemaFormFolder',
            'form1'
        )
        self.assertTrue(ISchemaFormFolder.providedBy(self.portal['form1']))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SchemaFormFolderIntegrationTest))
    return suite
