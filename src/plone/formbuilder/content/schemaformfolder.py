# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implementer
# from zope.interface import Interface
from plone.supermodel import model
from plone.dexterity.content import Container
from plone.autoform import directives
from collective.z3cform.rawdictwidget import RawDictWidgetFactory

from plone.formbuilder import _


class ISchemaFormFolder(model.Schema):
    """Center of Responsibility (CDR)
    """

    formname = schema.TextLine(
        title=_(u'Form name'),
        description=_(u'Name of form'),
        required=False
    )

    directives.widget('schema_json', RawDictWidgetFactory)
    schema_json = schema.Dict(
        title=_(u'Schema json'),
        readonly=True,  # to make the field readonly, and possible to set using some event based code or method. that is normally the use case
        required=False)


@implementer(ISchemaFormFolder)
class SchemaFormFolder(Container):
    """Convenience subclass for ``CDR`` portal type
    """
    # Make sure Container's accessors don't take precedence
