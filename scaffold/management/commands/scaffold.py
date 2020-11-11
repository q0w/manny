from django.core.management.base import BaseCommand
from scaffold.scaffold import Scaffold


class Command(BaseCommand):
    def get_version(self):
        return f'scaffold 0.1'

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        return parser

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='*')

    def handle(self, *args, **options):
        if not options['app_name']:
            print('Provide app name...')
            return
        app_name = options['app_name'][0]

        scaffold = Scaffold(app_name)
        scaffold.execute()
