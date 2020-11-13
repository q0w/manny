import os, sys, json
from django.conf import settings

from scaffold.utils import default_kwargs


@default_kwargs(max_length=255, null=False, blank=False)
def get_charfield(**kwargs):
    if not kwargs.get('name'):
        raise SystemExit('Provide field name...')
    return f"{kwargs['name']} = models.CharField(max_length={kwargs['max_length']}, null={kwargs['null']}, blank={kwargs['blank']})"


@default_kwargs(default='None', null=True)
def get_integerfield(**kwargs):
    if not kwargs.get('name'):
        raise SystemExit('Provide field name...')
    return f"{kwargs['name']} = models.IntegerField(null={kwargs['null']}, default={kwargs['default']})"

@default_kwargs(null=False, blank=False)
def get_textfield(**kwargs):
    if not kwargs.get('name'):
        raise SystemExit('Provide field name...')
    return f"{kwargs['name']} = models.TextField(null={kwargs['null']}, default={kwargs['default']})"


MODEL_TEMPLATE = """
class %s(models.Model):
    %s
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
"""


# MODEL_TEMPLATE = 'class {name}(models.Model):\n' \
#                  '{line}' \
#                  '    update_date = models.DateTimeField(auto_now=True)\n' \
#                  '    create_date = models.DateTimeField(auto_now_add=True)\n' \
#                  '    class Meta:\n' \
#                  '        ordering = ["-id"]'

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
                    os.system(f'python manage.py startapp {app}')
                except Exception as e:
                    print(e)

    # TODO:add file deserialize support (json.load) ???
    def get_field(self, field):
        # f = open(field)
        field = json.loads(field)
        # print(field)
        field_type = field.get('type')

        if field_type.lower() == 'char':
            return get_charfield(**field)
        if field_type.lower() == 'int':
            return get_integerfield(**field)
        if field_type.lower() == 'text':
            return get_textfield(**field)

    def create_model(self):
        models_file_path = f'{self.SCAFFOLD_APP_DIRS}{self.app[0]}/models.py'
        with open(models_file_path, 'r') as mf:
            # check if model already exists
            for line in mf.readlines():
                if f'class {self.model}' in line:
                    # TODO: add logging
                    sys.exit(f'Model {self.model} already exists')
                    # return

        fields = []
        for field in self.fields:
            new_field = self.get_field(field)
            fields.append(new_field)
        # print(fields)
        with open(models_file_path, 'a') as mf:
            mf.write(MODEL_TEMPLATE % (self.model, '\n    '.join(field for field in fields)))
            # mf.write(MODEL_TEMPLATE.format(name=self.model,line=''.join('    ' +field + '\n' for field in fields)))

    def execute(self):
        if not self.app:
            sys.exit("No application found. Provide app name...")
        self.create_app()
        if self.model:
            self.create_model()
