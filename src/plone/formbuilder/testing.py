# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import plone.formbuilder


class PloneFormbuilderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.formbuilder)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.formbuilder:default')


PLONE_FORMBUILDER_FIXTURE = PloneFormbuilderLayer()


PLONE_FORMBUILDER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_FORMBUILDER_FIXTURE,),
    name='PloneFormbuilderLayer:IntegrationTesting'
)


PLONE_FORMBUILDER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_FORMBUILDER_FIXTURE,),
    name='PloneFormbuilderLayer:FunctionalTesting'
)


PLONE_FORMBUILDER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_FORMBUILDER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PloneFormbuilderLayer:AcceptanceTesting'
)
