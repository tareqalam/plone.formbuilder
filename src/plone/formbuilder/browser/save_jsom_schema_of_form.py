
from plone import api
from Products.Five.browser import BrowserView

import simplejson as json
from plone.protect.auto import safeWrite


class SaveJsonSchemaOfForm(BrowserView):
    """
    Save json coming from formbuilder and save it to a dexterity content type
    """

    def __call__(self):
        """
        """
        request = self.context.REQUEST
        # import pdb;pdb.set_trace()
        if request.get('save_json') is not None:
            if self.context.portal_type not in ['SchemaFormFolder']:
                api.portal.show_message(message='Can not add schema in the context!', request=request)
                return request.RESPONSE.redirect(self.context.absolute_url() + '/formbuilder')

            if str(request.get('schema_json')).strip() in ['None', '']:
                api.portal.show_message(message='Form can not be empty', request=request)
                return request.RESPONSE.redirect(self.context.absolute_url() + '/formbuilder')
            obj = self.context
            safeWrite(obj, request)
            raw_json = request.get('schema_json')
            schema_json = json.loads(raw_json)
            obj.schema_json = schema_json
            obj.reindexObject()
            api.portal.show_message(message='Saved form succesfully!', request=request)
            return request.RESPONSE.redirect(self.context.absolute_url())
