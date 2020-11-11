import os, sys
from django.conf import settings


class Scaffold:
    def __init__(self, app):
        self.app = app
        try:
            self.SCAFFOLD_APP_DIRS = settings.BASE_DIR
        except:
            self.SCAFFOLD_APP_DIRS = './'

    def create_app(self):
        if not os.path.exists(self.SCAFFOLD_APP_DIRS):
            raise Exception(f'SCAFFOLD_APP_DIRS "{self.SCAFFOLD_APP_DIRS}" does not exist')
        if not os.path.exists(f'{self.SCAFFOLD_APP_DIRS}{self.app}'):
            try:
                os.system(f'python manage.py startapp {self.app}')
            except Exception as e:
                print(e)

    def execute(self):
        if not self.app:
            sys.exit("No application found. Provide app name...")
        self.create_app()

