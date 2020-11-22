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
        parser.add_argument('--model', dest='model', default=None, nargs='+')
        parser.add_argument('--serializers', dest='serializers', default=None, nargs='+')

    def handle(self, *args, **options):
        if not options.get('app_name'):
            SystemExit('Provide app name...')
            # print('Provide app name...')
            # return
        app_name = options['app_name']
        model_name = options['model'][0] if options.get('model') else None
        fields = options['model'][1:] if options.get('model') else None
        serializers = options.get('serializers', None)

        scaffold = Scaffold(apps=app_name, model=model_name, fields=fields,serializers=serializers)
        scaffold.execute()
