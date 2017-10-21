from Products.Five.browser import BrowserView


class SaveJsonSchemaOfForm(BrowserView):
    """
    Save json coming from formbuilder and save it to a dexterity content type
    """
    def __call__(self):
        """
        """
        if self.context.REQUEST.get('save_json') is not None:
            return 'saved'
