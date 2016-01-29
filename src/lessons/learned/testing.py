# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import lessons.learned


class LessonsLearnedLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=lessons.learned)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'lessons.learned:default')


LESSONS_LEARNED_FIXTURE = LessonsLearnedLayer()


LESSONS_LEARNED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LESSONS_LEARNED_FIXTURE,),
    name='LessonsLearnedLayer:IntegrationTesting'
)


LESSONS_LEARNED_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LESSONS_LEARNED_FIXTURE,),
    name='LessonsLearnedLayer:FunctionalTesting'
)


LESSONS_LEARNED_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LESSONS_LEARNED_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='LessonsLearnedLayer:AcceptanceTesting'
)
