from django.test import TestCase
from mock import patch

COMMANDS_PACKAGE = 'django_ember_toolkit.management.commands'

class EmberMockTestCase(TestCase):
    '''A TestCase where all calls to Ember commands will be automatically
    mocked (at self.ember_mock).'''

    def setUp(self):
        patcher = patch(COMMANDS_PACKAGE +
            '._base.EmberCommand.run_ember_command')
        self.addCleanup(patcher.stop)
        self.ember_mock = patcher.start()
