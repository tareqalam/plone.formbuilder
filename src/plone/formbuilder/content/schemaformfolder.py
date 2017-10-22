# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implementer
# from zope.interface import Interface
from plone.supermodel import model
from plone.dexterity.content import Container
from plone.autoform import directives
from collective.z3cform.rawdictwidget import RawDictWidgetFactory
import simplejson as json
from plone.formbuilder import _
from odict import odict


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

    def get_schema_json(self):
        """
        get schema json
        """
        if self.schema_json:
            return self.schema_json
        else:
            return """
            {
          components: [{
            type: 'button',
            theme: 'primary',
            disableOnInvalid: true,
            action: 'submit',
            block: false,
            rightIcon: '',
            leftIcon: '',
            size: 'md',
            key: 'submit',
            tableView: false,
            label: 'Submit',
            input: true
          }],
          display: 'form'
        };

        """

    def get_converted_json_schema_for_angular(self):

        def convert_type(type_name):
            type_map = {
                'textfield': 'string',
                'checkbox': 'string',
                'button': 'string',
                'radio': 'string'
            }
            return type_map.get(type_name, type_name)

        def convert_widget(input_type_name):
            input_type_map = {
                'text': 'string',
                'checkbox': 'checkbox',
                'radio': 'radio',
                'button': 'button'
            }
            return input_type_map.get(input_type_name, input_type_name)
        schema_json_new = {"properties": odict()}
        if self.schema_json:
            schema_json = json.loads(self.schema_json)
            for field in schema_json.get('components'):
                field_dict = {
                    "type": convert_type(field.get('type')),
                    "title": field.get('label', ''),
                    "widget": convert_widget(field.get('inputType', field.get('type'))),
                    "description": field.get('description', ''),
                    "placeholder": field.get('placeholder', '')
                }

                if field.get('type') == 'radio':
                    field_dict["oneOf"] = []
                    for option in field.get('values'):
                        field_dict["oneOf"].append({
                            "description": option.get('label'),
                            "enum": [option.get('value')]
                        })

                if field.get('type') == 'button':
                    if schema_json_new.has_key('buttons'):
                        field_dict['label'] = field_dict['title']
                        schema_json_new['buttons'].append(field_dict)
                    else:
                        schema_json_new['buttons'] = [field_dict]
                else:
                    schema_json_new["properties"][field['key'].replace('undefined', '')] = field_dict
            # import pdb;pdb.set_trace()
            # schema_json_new["required"] = ["email", "password", "rememberMe"]
        return schema_json_new
