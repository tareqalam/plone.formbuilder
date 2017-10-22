# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
from plone.restapi.testing import PLONE_RESTAPI_AT_FUNCTIONAL_TESTING
from plone.restapi.testing import RelativeSession
from plone.formbuilder.testing import PLONE_FORMBUILDER_ACCEPTANCE_TESTING
import simplejson as json
import transaction
import unittest


class TestSchemaformdataEndpoint(unittest.TestCase):

    layer = PLONE_FORMBUILDER_ACCEPTANCE_TESTING

    def setUp(self):

        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # import ipdb;ipdb.set_trace()
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.portal.invokeFactory(
            'SchemaFormFolder',
            id='folder1',
            title='My Folder'
        )
        # wftool = getToolByName(self.portal, 'portal_workflow')
        # wftool.doActionFor(self.portal.folder1, 'publish')
        transaction.commit()

    def test_post_to_folder_creates_document(self):
        response = self.api_session.post(
            self.portal.folder1.absolute_url() + '/@schemaformdata',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            json={
                "@type": "SchemaFormData",
                "id": "mydocument",
                "title": "My Document",
                "schema_form_data": '{"k1": "val1", "k2": 2}'
            },
        )
        self.assertEqual(201, response.status_code)
        transaction.begin()
        self.assertEqual("My Document", self.portal.folder1.mydocument.Title())
        self.assertEqual("SchemaFormData", response.json().get('@type'))
        self.assertEqual("mydocument", response.json().get('id'))
        self.assertEqual("My Document", response.json().get('title'))
        saved_dict = response.json().get('schema_form_data')
        saved_dict = json.loads(saved_dict)
        self.assertEqual(saved_dict.get('k1'), 'val1')
        self.assertEqual(saved_dict.get('k2'), 2)

        expected_url = "http://localhost:55001/plone/folder1/mydocument"
        self.assertEqual(expected_url, response.json().get('@id'))
