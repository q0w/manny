import os, sys, json
import subprocess
from django.conf import settings
from scaffold.utils import FieldTemplate


MODEL_TEMPLATE = """
class %s(models.Model):
    %s
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
"""


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
        for app in self.app:
            if not os.path.exists(f'{self.SCAFFOLD_APP_DIRS}{app}'):
                try:
                    subprocess.Popen(['python', 'manage.py', 'startapp', app])
                except Exception as e:
                    print(e)

    # TODO:add file deserialize support (json.load) ???
    def get_field(self, field):
        field = json.loads(field)
        return FieldTemplate().safe_replace(**field)

    def create_model(self):
        models_file_path = f'{self.SCAFFOLD_APP_DIRS}{self.app[0]}/models.py'
        with open(models_file_path, 'r') as mf:
            # check if model already exists
            for line in mf.readlines():
                if f'class {self.model}' in line:
                    # TODO: add logging
                    sys.exit(f'Model {self.model} already exists')

        fields = []
        for field in self.fields:
            new_field = self.get_field(field)
            fields.append(new_field)
        with open(models_file_path, 'a') as mf:
            mf.write(MODEL_TEMPLATE % (self.model, '\n    '.join(field for field in fields)))

    def execute(self):
        if not self.app:
            sys.exit("No application found. Provide app name...")
        self.create_app()
        if self.model:
            self.create_model()
