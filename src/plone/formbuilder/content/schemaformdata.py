# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implementer
# from zope.interface import Interface
from plone.supermodel import model
from plone.dexterity.content import Item
from plone.autoform import directives
from collective.z3cform.rawdictwidget import RawDictWidgetFactory
import simplejson as json
from plone.formbuilder import _
from odict import odict


class ISchemaFormData(model.Schema):
    """Center of Responsibility (CDR)
    """
    directives.widget('schema_form_data', RawDictWidgetFactory)
    schema_form_data = schema.Dict(
        title=_(u'Schema form data'),
        readonly=True,  # to make the field readonly, and possible to set using some event based code or method. that is normally the use case
        required=False)


@implementer(ISchemaFormData)
class SchemaFormData(Item):
    """Convenience subclass for ``CDR`` portal type
    """
    # Make sure Container's accessors don't take precedence

    def get_schema_form_data(self):
        """
        """
        if self.schema_form_data:
            data = []
            json_data = json.loads(self.schema_form_data)
            for k, v in json_data.items():
                data.append([k, v])
            return data
        else:
            return []
