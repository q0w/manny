import os
import subprocess
import sys

from django.core.management import CommandError

from scaffold.kit.colors import TermColor
from scaffold.kit.templates import (
    FieldTemplate,
    ModelTemplate,
    SerializerTemplate,
    UrlTemplate,
    ViewTemplate,
    CommonTemplate,
)
from scaffold.kit.utils import Walker


class Scaffold:
    def __init__(
        self,
        proj_settings,
        app_config,
        new_model,
        fields,
        serializers,
        urls,
        views,
    ):
        self.proj_settings = proj_settings
        self.new_model = new_model
        self.app_config = app_config
        self.models = self.get_model_names()
        self.fields = fields
        self.serializers = serializers
        self.urls = urls
        self.views = views

    def get_model_names(self):
        return [m.__name__ for m in self.app_config.get_models()]

    def get_content(self, context, template: CommonTemplate):
        return template.convert(context)

    def check_models(self, models):
        missing_models = [x for x in models if x not in set(self.get_model_names())]
        return missing_models

    def check_sv(self, file, sv):
        if not os.path.isfile(file):
            return None
        existing_sv = Walker(file).get_sv()
        excess_sv = [x for x in sv if x in existing_sv]
        return excess_sv

    def create_model(self):
        if self.new_model in self.get_model_names():
            raise CommandError(f"model {self.new_model} already exists...")
        fields = []
        for field in self.fields:
            new_field = self.get_content(field.split(":"), FieldTemplate())
            fields.append(new_field)
        with open(self.app_config.models_module.__file__, "a") as mf:
            content = self.get_content(
                {"name": self.new_model, "fields": fields}, ModelTemplate()
            )
            mf.write(content)
        subprocess.call(["black", self.app_config.models_module.__file__, "-q"])
        print(f"{TermColor.OK}model: {self.new_model} has been created{TermColor.ENDC}")

    def check_imports(self, filename, imports):
        if not os.path.isfile(filename):
            return imports
        existing_imports = Walker(file=filename).get_imports()
        missing_imports = {}
        for key, value in imports.items():
            missing_values = [
                x for x in value if x not in set(existing_imports.get(key, []))
            ]
            if missing_values:
                missing_imports[key] = missing_values
        return missing_imports

    def create_serializers(self):
        serializer_file_path = f"{self.app_config.module.__path__[0]}/serializers.py"
        serializers = (
            self.get_model_names() if not self.serializers else self.serializers
        )

        missing_models = self.check_models(serializers)
        if missing_models:
            error = (
                f'{" ".join(missing_models)} do not exist...'
                if len(missing_models) > 1
                else f'{" ".join(missing_models)} does not exist...'
            )
            raise CommandError(error)

        excess_serializers = self.check_sv(serializer_file_path, serializers)
        if excess_serializers:
            serializers = [m for m in serializers if m not in excess_serializers]
            if not serializers:
                raise CommandError("all serializers already exist...")
            error = (
                f'{TermColor.ERROR}{" ".join(excess_serializers)} already exist...{TermColor.ENDC}'
                if len(excess_serializers) > 1
                else f'{" ".join(excess_serializers)} already exists...{TermColor.ENDC}'
            )
            print(error)

        missing_imports = self.check_imports(
            serializer_file_path,
            {"rest_framework": ["serializers"], f"{self.app_config.name}": ["models"]},
        )
        with open(serializer_file_path, "a") as sf:
            content = self.get_content(
                {"models": serializers, "imports": missing_imports},
                SerializerTemplate(),
            )
            sf.write(content)
        subprocess.call(["black", serializer_file_path, "-q"])
        print(
            f"{TermColor.OK}serializers: {' '.join(serializers)} have been created{TermColor.ENDC}"
        ) if len(serializers) > 1 else print(
            f"{TermColor.OK}serializer: {' '.join(serializers)} has been created{TermColor.ENDC}"
        )

    def create_urls(self):
        url_file_path = f"{self.app_config.module.__path__[0]}/urls.py"
        existing_models = self.get_model_names()
        with open(url_file_path, "w+") as uf:
            content = self.get_content(
                {"app": self.app_config.name, "models": existing_models}, UrlTemplate()
            )
            uf.write(content)
        subprocess.call(["black", url_file_path, "-q"])
        print(
            f"{TermColor.OK}urls: SimpleRouter for all models has been created{TermColor.ENDC}"
        )

    def create_views(self):
        view_file_path = f"{self.app_config.module.__path__[0]}/views.py"
        views = self.get_model_names() if not self.views else self.views

        missing_models = self.check_models(views)
        if missing_models:
            raise CommandError(f'{" ".join(missing_models)} do/does not exist...')

        excess_views = self.check_sv(view_file_path, views)
        if excess_views:
            views = [m for m in views if m not in excess_views]
            if not views:
                raise CommandError("all views already exist...")
            error = (
                f'{TermColor.ERROR}{" ".join(excess_views)} already exist...{TermColor.ENDC}'
                if len(excess_views) > 1
                else f'{TermColor.ERROR}{" ".join(excess_views)} already exists...{TermColor.ENDC}'
            )
            print(error)

        missing_imports = self.check_imports(
            view_file_path,
            {
                "django.shortcuts": ["get_object_or_404"],
                "rest_framework": ["viewsets", "response"],
                f"{self.app_config.name}": ["models", "serializers"],
            },
        )
        with open(view_file_path, "a") as wf:
            content = self.get_content(
                {"models": views, "imports": missing_imports}, ViewTemplate()
            )
            wf.write(content)
        subprocess.call(["black", view_file_path, "-q"])
        print(
            f"{TermColor.OK}views: {' '.join(views)} have been created{TermColor.ENDC}"
        ) if len(views) > 1 else print(
            f"{TermColor.OK}view: {' '.join(views)} has been created{TermColor.ENDC}"
        )

    def execute(self):
        if self.new_model:
            self.create_model()
        if self.urls:
            self.create_urls()
        if self.serializers is not None:
            self.create_serializers()
        if self.views is not None:
            self.create_views()


class ScaffoldApp:
    def __init__(self, proj_settings, new_apps):
        self.apps = new_apps
        self.proj_settings = proj_settings

    def create_app(self):
        for app in self.apps:
            try:
                subprocess.call(["python", "manage.py", "startapp", app])
            except Exception as e:
                print(e)
        walker = Walker(
            file=sys.modules[self.proj_settings].__file__,
            options={"variable": "INSTALLED_APPS", "variable_values": self.apps},
        )
        walker.mutate()
        print(
            f"{TermColor.OK}apps: {' '.join(self.apps)} have been created{TermColor.ENDC}"
        ) if len(self.apps) > 1 else print(
            f"{TermColor.OK}app: {' '.join(self.apps)} has been created{TermColor.ENDC}"
        )

    def execute(self):
        if self.apps:
            self.create_app()
