from os.path import abspath, join
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from termcolor import colored

SEPARATOR = '---------------------------------------------------------------'

# settings with a default of None are required
DEFAULT_SETTINGS = {
    'EMBER_APP_NAME': None,
    'API_ENDPOINT': None,
    'EMBER_APP_PATH': 'client'
}


def get_setting(key):
    '''Get a setting from the user's project by key, falling back on the default
    if there's no setting available.'''
    return settings.EMBER_TOOLKIT.get(key, DEFAULT_SETTINGS[key])


def get_full_ember_path():
    '''Return the full, absolute path to the project's Ember app.'''
    return abspath(join(settings.BASE_DIR, get_setting('EMBER_APP_PATH')))


def assert_required_settings(*args):
    '''Raise a useful error if any of args are not configured in
    settings.EMBER_TOOLKIT'''

    if not hasattr(settings, 'EMBER_TOOLKIT'):
        raise CommandError('You must define an EMBER_TOOLKIT dict in settings')

    missing_settings = []

    for key in args:
        if get_setting(key) is None:
            missing_settings.append(key)

    if missing_settings:
        raise CommandError(
            'settings.EMBER_TOOLKIT is missing the following keys: ' +
            ', '.join(missing_settings))


def run_ember_command(cmd_name, *args, **kwargs):
    '''Run the named ember in the project's FULL_EMBER_PATH. Any args and kwargs
    will be converted into positional and named arguments respectively
    (booleans are assumed to be "boolean positional arguments")

    e.g.: run_ember_command('generate', 'route', 'foobar', pod=True)
    becomes: ember generate route foobar --pod
    '''

    command = ['ember', cmd_name] + list(args)

    for key, value in kwargs:
        command.append('--' + key)
        command.append("'{}'".format(value))

    print(SEPARATOR)
    print('Running {}...'.format(colored(' '.join(command), 'green')))
    print(SEPARATOR)

    subprocess.check_call(command, cwd=get_full_ember_path())


def write_initial_config():
    '''Generate an Ember config file with support for backend
    "autoconfiguration" at the given path.'''

    config_source = render_to_string(
        'django_ember_toolkit/environment.js',
        {'app_name': get_setting('EMBER_APP_NAME')})
    config_path = join(get_full_ember_path(), 'config/environment.js')

    with open(config_path, 'w') as config_file:
        config_file.write(config_source)
