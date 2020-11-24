import os
import sys
import glob
import json
import subprocess
from django.conf import settings
from scaffold.kit.templates import FieldTemplate, ModelTemplate, SerializerTemplate, UrlTemplate
from scaffold.kit.utils import Walker


class Scaffold:
    def __init__(self, apps, model, fields, serializers, urls):
        self.apps = apps
        self.model = model
        self.fields = fields
        self.serializers = serializers
        self.urls = urls

        try:
            self.SCAFFOLD_APP_DIRS = f'{settings.BASE_DIR}/'
        except:
            self.SCAFFOLD_APP_DIRS = './'

    def get_core_app(self):
        return [os.path.dirname(filename) for filename in
                glob.iglob(self.SCAFFOLD_APP_DIRS + '**/settings.py', recursive=True)][0]

    def create_app(self):
        if not os.path.exists(self.SCAFFOLD_APP_DIRS):
            raise Exception(f'SCAFFOLD_APP_DIRS "{self.SCAFFOLD_APP_DIRS}" does not exist')

        core_app_settings = f'{self.get_core_app()}/settings.py'
        subdirs = [d[1] for d in os.walk(f'{self.SCAFFOLD_APP_DIRS}')][0]
        not_installed_apps = [x for x in self.apps if x not in subdirs]

        for app in not_installed_apps:
            try:
                subprocess.Popen(['python', 'manage.py', 'startapp', app]).wait()
            except Exception as e:
                print(e)
        if not_installed_apps:
            self.update_installed_apps(core_app_settings)

    def update_installed_apps(self, core_app):
        walker = Walker(core_app, options={'variable': 'INSTALLED_APPS',
                                           'variable_values': self.apps})
        walker.mutate()

    # TODO:add file deserialize support (json.load) ???
    def get_field(self, field):
        field = json.loads(field)
        return FieldTemplate.convert(context=field)

    def get_existing_models(self, file=None):
        if file is None:
            file = f'{self.SCAFFOLD_APP_DIRS}{self.apps[0]}/models.py'
        existing_models = Walker(file=file).get_models()
        return existing_models

    def check_models(self, models, existing_models):
        missing_models = [x for x in models if x not in set(existing_models)]
        return missing_models

    def create_model(self):
        models_file_path = f'{self.SCAFFOLD_APP_DIRS}{self.apps[0]}/models.py'
        existing_models = self.get_existing_models(file=models_file_path)
        if self.model in existing_models:
            sys.exit(f'model {self.model} already exists...')
        fields = []
        for field in self.fields:
            new_field = self.get_field(field)
            fields.append(new_field)
        with open(models_file_path, 'a') as mf:
            mf.write(ModelTemplate.convert(context={'name': self.model, 'fields': fields}))

    def check_imports(self, filename, imports):
        existing_imports = Walker(file=filename).get_imports()
        missing_imports = {}
        for key, value in imports.items():
            missing_values = [x for x in value if x not in set(existing_imports.get(key, []))]
            if missing_values:
                missing_imports[key] = missing_values
        return missing_imports

    def create_serializers(self):
        serializer_file_path = f'{self.SCAFFOLD_APP_DIRS}{self.apps[0]}/serializers.py'
        existing_models = self.get_existing_models()
        serializers = existing_models if self.serializers[0] == 'all' else self.serializers
        missing_models = self.check_models(serializers, existing_models)
        if missing_models:
            sys.exit(f'{" ".join(missing_models)} do/does not exist...')

        missing_imports = self.check_imports(serializer_file_path, {'rest_framework': ['serializers'],
                                                                    '.models': serializers})
        with open(serializer_file_path, 'a') as sf:
            sf.write(SerializerTemplate.convert(context={'models': serializers, 'imports': missing_imports}))

    def create_urls(self):
        url_file_path = f'{self.SCAFFOLD_APP_DIRS}{self.apps[0]}/urls.py'
        existing_models = self.get_existing_models()
        with open(url_file_path, 'w+') as uf:
            uf.write(UrlTemplate.convert(context={'app': self.apps[0], 'models': existing_models}))

    def create_views(self):
        '''
        1. get app models
        2. check if urls.py and model urls exist
        3. check if view already exists
        4. #TODO: ........
         '''

    def execute(self):
        if not self.apps:
            sys.exit("No application found. Provide app name...")
        self.create_app()
        if self.model:
            self.create_model()
        if self.serializers:
            self.create_serializers()
        if self.urls:
            self.create_urls()
