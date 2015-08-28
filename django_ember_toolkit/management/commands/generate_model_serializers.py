from os.path import abspath, join

from django.conf import settings
from django.template.loader import render_to_string

from ._base import EmberCommand

def get_field_names(Model):
    return sorted([field.name for field in Model._meta.get_fields()])

class Command(EmberCommand):
    help = ('Generate basic Django REST Framework serializers for '
        'models in MODELS_TO_SYNC')

    def handle(self, *args, **options):
        self.assert_required_settings('MODELS_TO_SYNC', 'SERIALIZER_NAMESPACE')

        serializer_module = self.get_or_create_module(
            self.get_setting('SERIALIZER_NAMESPACE'))

        # figure out which serializers we need to create

        apps_to_import = set()
        serializers_to_create = set()

        for Model in self.get_sync_model_set():
            serializer_name = Model.__name__ + "Serializer"

            if not hasattr(serializer_module, serializer_name):
                serializers_to_create.add(Model)

                app_models = Model._meta.app_label + '_models'
                if not hasattr(serializer_module, app_models):
                    apps_to_import.add(Model._meta.app_label)

        # generate serializer code
        import_block = ''
        code_block = ''

        for app_label in apps_to_import:
            import_block += 'from {app} import models as {app}_models\n'.format(
                app=app_label)

        for Model in serializers_to_create:
            field_list = ', '.join(get_field_names(Model))
            code_block += render_to_string(
                'django_ember_toolkit/_serializer.py',
                {
                    'model_name': Model.__name__,
                    'app_label': Model._meta.app_label,
                    'model_fields': field_list
                }) + '\n'

        print('IMPORTS: ')
        print(import_block)

        print('CODE: ')
        print(code_block)
