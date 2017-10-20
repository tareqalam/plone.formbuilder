# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.formbuilder.testing import PLONE_FORMBUILDER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that plone.formbuilder is properly installed."""

    layer = PLONE_FORMBUILDER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plone.formbuilder is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'plone.formbuilder'))

    def test_browserlayer(self):
        """Test that IPloneFormbuilderLayer is registered."""
        from plone.formbuilder.interfaces import (
            IPloneFormbuilderLayer)
        from plone.browserlayer import utils
        self.assertIn(IPloneFormbuilderLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLONE_FORMBUILDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['plone.formbuilder'])

    def test_product_uninstalled(self):
        """Test if plone.formbuilder is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'plone.formbuilder'))

    def test_browserlayer_removed(self):
        """Test that IPloneFormbuilderLayer is removed."""
        from plone.formbuilder.interfaces import \
            IPloneFormbuilderLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPloneFormbuilderLayer, utils.registered_layers())
