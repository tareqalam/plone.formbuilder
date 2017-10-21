# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.formbuilder.testing import PLONE_FORMBUILDER_ACCEPTANCE_TESTING
from plone.restapi.testing import RelativeSession
from zope.component import getAdapter

try:
    from Products.CMFPlone.interfaces import ISecuritySchema
except ImportError:
    from plone.app.controlpanel.security import ISecuritySchema

# import transaction
import unittest


class TestSchemaEndpoint(unittest.TestCase):

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

        json_schema_form_form_builder = {
            "display": "form",
                       "components": [
                           {
                               "validate": {
                                   "minLength": "",
                                   "required": False,
                                   "customPrivate": False,
                                   "pattern": "",
                                   "maxLength": "",
                                   "custom": ""
                               },
                               "properties": {
                                   "": ""
                               },
                               "clearOnHide": True,
                               "multiple": False,
                               "inputMask": "",
                               "tableView": True,
                               "tags": [

                               ],
                               "type":"textfield",
                               "defaultValue":"",
                               "conditional":{
                                   "eq": "",
                                   "when": "",
                                   "show": ""
                               },
                               "persistent": True,
                               "label": "name",
                               "prefix": "",
                               "protected": False,
                               "key": "undefinedName",
                               "input": True,
                               "hidden": False,
                               "unique": False,
                               "placeholder": "",
                               "inputType": "text",
                               "suffix": ""
                           },
                           {
                               "validate": {
                                   "minLength": "",
                                   "required": False,
                                   "customPrivate": False,
                                   "pattern": "",
                                   "maxLength": "",
                                   "custom": ""
                               },
                               "properties": {
                                   "": ""
                               },
                               "clearOnHide": True,
                               "multiple": False,
                               "inputMask": "",
                               "tableView": True,
                               "tags": [

                               ],
                               "type":"textfield",
                               "defaultValue":"",
                               "conditional":{
                                   "eq": "",
                                   "when": "",
                                   "show": ""
                               },
                               "persistent": True,
                               "label": "email",
                               "prefix": "",
                               "protected": False,
                               "key": "undefinedEmail",
                               "input": True,
                               "hidden": False,
                               "unique": False,
                               "placeholder": "email",
                               "inputType": "text",
                               "suffix": ""
                           },
                           {
                               "validate": {
                                   "required": False
                               },
                               "properties": {
                                   "": ""
                               },
                               "clearOnHide": True,
                               "conditional": {
                                   "eq": "",
                                   "when": "",
                                   "show": ""
                               },
                               "name": "",
                               "tableView": True,
                               "tags": [

                               ],
                               "defaultValue":False,
                               "hideLabel":True,
                               "persistent":True,
                               "value":"",
                               "label":"remember me",
                               "protected":False,
                               "key":"undefinedRememberme",
                               "input":True,
                               "hidden":False,
                               "type":"checkbox",
                               "inputType":"checkbox",
                               "datagridLabel":True
                           },
                           {
                               "disableOnInvalid": True,
                               "tableView": False,
                               "leftIcon": "",
                               "rightIcon": "",
                               "label": "Submit",
                               "theme": "primary",
                               "key": "submit",
                               "action": "submit",
                               "input": True,
                               "type": "button",
                               "block": False,
                               "size": "md"
                           }
                       ],
            "page": 0
        }
        self.portal.invokeFactory(
            'SchemaFormFolder',
            id='test_schema_form_folder',
            title='Test schema form folder',
            schema_json=json_schema_form_form_builder
        )
        self.schemaform = self.portal.test_schema_form_folder
        import transaction
        transaction.commit()

    def test_get_schema(self):
        response = self.api_session.get(self.schemaform.absolute_url() + '/@schema')
        # import pdb
        # pdb.set_trace()
