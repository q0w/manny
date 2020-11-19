import os
import sys
import glob
import json
import subprocess
from django.conf import settings
from scaffold.kit.templates import FieldTemplate, ModelTemplate
from scaffold.kit.utils import Walker


class Scaffold:
    def __init__(self, app, model, fields):
        self.app = app
        self.model = model
        self.fields = fields

        try:
            self.SCAFFOLD_APP_DIRS = f'{settings.BASE_DIR}/'
        except:
            self.SCAFFOLD_APP_DIRS = './'

    def create_app(self):
        if not os.path.exists(self.SCAFFOLD_APP_DIRS):
            raise Exception(f'SCAFFOLD_APP_DIRS "{self.SCAFFOLD_APP_DIRS}" does not exist')

        core_app = [filename for filename in
                    glob.iglob(self.SCAFFOLD_APP_DIRS + '**/settings.py', recursive=True)][0]
        subdirs = [d[1] for d in os.walk(f'{self.SCAFFOLD_APP_DIRS}')][0]
        not_installed_apps = [x for x in self.app if x not in subdirs]

        for app in not_installed_apps:
            try:
                subprocess.Popen(['python', 'manage.py', 'startapp', app]).wait()
            except Exception as e:
                print(e)
        if not_installed_apps:
            self.update_installed_apps(core_app)

    def update_installed_apps(self, core_app):
        walker = Walker(core_app, options={'variable': 'INSTALLED_APPS',
                                           'variable_values': self.app})
        walker.mutate()

    # TODO:add file deserialize support (json.load) ???
    def get_field(self, field):
        field = json.loads(field)
        return FieldTemplate.convert(context=field)

    def create_model(self):
        models_file_path = f'{self.SCAFFOLD_APP_DIRS}{self.app[0]}/models.py'
        existing_models = Walker(file=models_file_path).get_models()
        if self.model in existing_models:
            sys.exit(f'model {self.model} already exists...')
        fields = []
        for field in self.fields:
            new_field = self.get_field(field)
            fields.append(new_field)
        with open(models_file_path, 'a') as mf:
            mf.write(ModelTemplate.convert(context={'name': self.model, 'fields': fields}))

    def create_views(self):
        '''
        1. get app models
        2. check if urls.py and model urls exist
        3. check if view already exists
        4. #TODO: ........
         '''

    def execute(self):
        if not self.app:
            sys.exit("No application found. Provide app name...")
        self.create_app()
        if self.model:
            self.create_model()
