from string import Template

from scaffold.kit.patterns import (MODEL_TEMPLATE,
                                   FIELD_TEMPLATE,
                                   CHAR_FIELD_TEMPLATE,
                                   DECIMAL_FIELD_TEMPLATE,
                                   LIST_VIEW_TEMPLATE)
from scaffold.kit.utils import default_kwargs


class FieldTemplate(Template):
    template = FIELD_TEMPLATE

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
    template = DECIMAL_FIELD_TEMPLATE

    @default_kwargs(max=5, places=2)
    def safe_replace(self, **kwargs):
        #TODO: refactor, use logging
        if kwargs['places'] >= kwargs['max']:
            raise SystemExit('Error: decimal places should be less than max_digits')
        return super().safe_replace(**kwargs)


class CharFieldTemplate(FieldTemplate):
    template = CHAR_FIELD_TEMPLATE

    @default_kwargs(max=255)
    def safe_replace(self, **kwargs):
        return super().safe_replace(**kwargs)


class ModelTemplate(Template):
    template = MODEL_TEMPLATE

    def __init__(self):
        super().__init__(self.template)


class ListViewTemplate(Template):
    template = LIST_VIEW_TEMPLATE
