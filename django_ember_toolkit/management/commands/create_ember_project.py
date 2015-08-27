from os.path import abspath, join
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from termcolor import colored

EMBER_PATH = abspath(join(settings.BASE_DIR, 'client'))
SEPARATOR = '---------------------------------------------------------------'


def run_ember_command(cmd_name, *args, **kwargs):
    command = ['ember', cmd_name] + list(args)

    for key, value in kwargs:
        command.append('--' + key)
        command.append("'{}'".format(value))

    print(SEPARATOR)
    print('Running {}...'.format(colored(' '.join(command), 'green')))
    print(SEPARATOR)

    subprocess.check_call(command, cwd=EMBER_PATH)


class Command(BaseCommand):
    args = 'app_name'
    help = 'Generate a new Ember app for use with your Django project'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError("An app_name argument is required.")

        app_name = args[0]

        print(SEPARATOR)
        print('Generating new Ember project at: ')
        print(EMBER_PATH)
        print(SEPARATOR)

        # create the project using ember-cli
        # subprocess.check_call(
        #     [
        #         'ember', 'new', app_name,
        #         '--dir', EMBER_PATH
        #     ])

        # install and scaffold the Ember adapter for Django REST Framework
        run_ember_command('install', 'ember-django-adapter')

        run_ember_command('generate', 'drf-adapter', 'application')
        run_ember_command('generate', 'drf-serializer', 'application')

        # install the modified config file
        config_source = render_to_string(
            'django_ember_toolkit/environment.js',
            {'app_name': app_name})
        config_path = join(EMBER_PATH, 'config/environment.js')

        with open(config_path, 'w') as config_file:
            config_file.write(config_source)
