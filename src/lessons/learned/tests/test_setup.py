# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from lessons.learned.testing import LESSONS_LEARNED_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that lessons.learned is properly installed."""

    layer = LESSONS_LEARNED_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if lessons.learned is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'lessons.learned'))

    def test_browserlayer(self):
        """Test that ILessonsLearnedLayer is registered."""
        from lessons.learned.interfaces import (
            ILessonsLearnedLayer)
        from plone.browserlayer import utils
        self.assertIn(ILessonsLearnedLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LESSONS_LEARNED_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['lessons.learned'])

    def test_product_uninstalled(self):
        """Test if lessons.learned is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'lessons.learned'))

    def test_browserlayer_removed(self):
        """Test that ILessonsLearnedLayer is removed."""
        from lessons.learned.interfaces import ILessonsLearnedLayer
        from plone.browserlayer import utils
        self.assertNotIn(ILessonsLearnedLayer, utils.registered_layers())
