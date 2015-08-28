import subprocess

from django.apps import apps as django_apps
from django.conf import settings
from inflection import dasherize, underscore

from ._base import EmberCommand

def model_to_command_args(Model):
    '''Take a model class and return a list of args that will create an
    equivalent model in Ember.'''
    return ['generate', 'model', dasherize(underscore(Model.__name__)),]

class Command(EmberCommand):
    help = 'Generate Ember models based on Django models from INSTALLED APPS'

    def handle(self, *args, **options):
        self.assert_required_settings('EMBER_APP_PATH', 'MODELS_TO_SYNC')

        model_name_set = set(self.get_setting('MODELS_TO_SYNC'))
        model_set = set()

        for app_config in django_apps.get_app_configs():
            for Model in app_config.get_models():
                key = Model._meta.app_label + '.' + Model.__name__
                app_star = Model._meta.app_label + '.*'

                if key in model_name_set or app_star in model_name_set:
                    model_set.add(Model)

        self.notify('Generating Ember models for: ' +
            ', '.join([
                Model._meta.app_label + '.' + Model.__name__
                for Model in model_set]))

        for Model in model_set:
            print(model_to_command_args(Model))
