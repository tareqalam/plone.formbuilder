# -*- coding: utf-8 -*-
from AccessControl.interfaces import IRoleManager

from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter


class SchemaFormFolderGet(Service):
    """Returns a serialized content object.
    """

    def reply(self):
        schema_json = self.context.get_converted_json_schema_for_angular()
        # import pdb;pdb.set_trace()
        return schema_json
