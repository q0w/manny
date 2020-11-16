from string import Template

#from utils import default_kwargs
from scaffold.utils import default_kwargs


class FieldTemplate(Template):
    template = "$name = models.${type}Field()"

    def __init__(self):
        super().__init__(self.template)

    def safe_replace(self, **kwargs):
        try:
            return self.substitute(**kwargs)
        except KeyError:
            raise SystemExit('Provide field name...')
        except Exception as e:
            print(e)


class DecimalFieldTemplate(FieldTemplate):
    template = "$name = models.${type}Field(max_digits=${max}, decimal_places=${places})"

    @default_kwargs(max=5, places=2)
    def safe_replace(self, **kwargs):
        return super().safe_replace(**kwargs)


class CharFieldTemplate(FieldTemplate):
    template = "$name = models.${type}Field(max_length=${max})"

    @default_kwargs(max=255)
    def safe_replace(self, **kwargs):
        return super().safe_replace(**kwargs)


class ModelTemplate(Template):
    template = """
class ${name}(models.Model):
    ${field}
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
"""

    def __init__(self):
        super().__init__(self.template)
