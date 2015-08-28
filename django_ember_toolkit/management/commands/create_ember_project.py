from os.path import join
import subprocess

from django.core.management.base import BaseCommand, CommandError

from . import utils as ember_utils
from .utils import (
    SEPARATOR, run_ember_command, assert_required_settings,
    get_setting, write_initial_config, get_full_ember_path)


class Command(BaseCommand):
    help = 'Generate a new Ember app for use with your Django project'

    def handle(self, *args, **options):
        assert_required_settings('EMBER_APP_NAME')

        print(SEPARATOR)
        print('Generating new Ember project at: ')
        print(get_full_ember_path())
        print(SEPARATOR)

        # create the project using ember-cli
        subprocess.check_call(
            [
                'ember', 'new', get_setting('EMBER_APP_NAME'),
                '--dir', get_full_ember_path()
            ])

        # install and scaffold the Ember adapter for Django REST Framework
        run_ember_command('install', 'ember-django-adapter')

        run_ember_command('generate', 'drf-adapter', 'application')
        run_ember_command('generate', 'drf-serializer', 'application')

        # install the modified config file
        write_initial_config()
