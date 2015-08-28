from os.path import abspath, join
import subprocess

from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from termcolor import colored

SEPARATOR = '---------------------------------------------------------------'

# settings with a default of None are required
DEFAULT_SETTINGS = {
    'EMBER_APP_NAME': None,
    'API_PATH': None,
    'EMBER_APP_PATH': 'client',
    'MODELS_TO_SYNC': None
}


class EmberCommand(BaseCommand):

    @classmethod
    def get_setting(cls, key):
        '''Get a setting from the user's project by key, falling back on the default
        if there's no setting available.'''
        return settings.EMBER_TOOLKIT.get(key, DEFAULT_SETTINGS[key])

    @classmethod
    def get_full_ember_path(cls):
        '''Return the full, absolute path to the project's Ember app.'''
        return abspath(join(
            settings.BASE_DIR,
            cls.get_setting('EMBER_APP_PATH')))

    def notify(self, some_text):
        self.stdout.write(SEPARATOR)
        self.stdout.write(some_text)
        self.stdout.write(SEPARATOR)

    @classmethod
    def assert_required_settings(cls, *args):
        '''Raise a useful error if any of args are not configured in
        settings.EMBER_TOOLKIT'''

        if not hasattr(settings, 'EMBER_TOOLKIT'):
            raise CommandError('You must define an EMBER_TOOLKIT dict in settings')

        missing_settings = []

        for key in args:
            if cls.get_setting(key) is None:
                missing_settings.append(key)

        if missing_settings:
            raise CommandError(
                'settings.EMBER_TOOLKIT is missing the following keys: ' +
                ', '.join(missing_settings))

    def run_ember_command(self, cmd_name, *args, **kwargs):
        '''Run the named ember in the project's FULL_EMBER_PATH. Any args and kwargs
        will be converted into positional and named arguments respectively
        (booleans are assumed to be "boolean positional arguments")

        e.g.: run_ember_command('generate', 'route', 'foobar', pod=True)
        becomes: ember generate route foobar --pod
        '''

        command = ['ember', cmd_name] + list(args)

        for key, value in kwargs:
            # in the unlikely case we pass None or False, just omit the kwarg
            if value:
                command.append('--' + key)

                if value is not True:
                    command.append("'{}'".format(value))

        self.notify('Running {}...'.format(colored(' '.join(command), 'green')))
        subprocess.check_call(command, cwd=self.get_full_ember_path())

    @classmethod
    def write_initial_config(cls):
        '''Generate an Ember config file with support for backend
        "autoconfiguration" at the given path.'''

        config_source = render_to_string(
            'django_ember_toolkit/environment.js',
            {'app_name': cls.get_setting('EMBER_APP_NAME')})
        config_path = join(cls.get_full_ember_path(), 'config/environment.js')

        with open(config_path, 'w') as config_file:
            config_file.write(config_source)

    def get_sync_model_set(cls):
        '''Return a set containing the actual Model class objects that are
        specified by MODELS_TO_SYNC.'''

        for app_config in django_apps.get_app_configs():
            model_name_set = set(cls.get_setting('MODELS_TO_SYNC'))
            model_set = set()

            for Model in app_config.get_models():
                key = Model._meta.app_label + '.' + Model.__name__
                app_star = Model._meta.app_label + '.*'

                if key in model_name_set or app_star in model_name_set:
                    model_set.add(Model)

        return model_set
