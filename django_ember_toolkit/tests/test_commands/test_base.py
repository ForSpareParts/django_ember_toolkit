from django.core.management import call_command
from django.core.management.base import CommandError
from django_ember_toolkit.tests.utils import EmberMockTestCase
from django.test.utils import override_settings


class TestEmberCommandBase(EmberMockTestCase):

    @override_settings(EMBER_TOOLKIT={})    
    def test_assert_settings(self):
        '''Test that running a command without a required setting results
        in a useful error message.'''

        with self.assertRaisesRegexp(CommandError, 'EMBER_APP_NAME'):
            call_command('create_ember_project')
