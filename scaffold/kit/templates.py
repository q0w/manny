from enum import Enum
from django.template import Template, Context
from scaffold.kit.patterns import (MODEL_TEMPLATE,
                                   FIELD_TEMPLATE,
                                   CHAR_FIELD_TEMPLATE,
                                   DECIMAL_FIELD_TEMPLATE,
                                   FOREIGN_KEY_TEMPLATE, MANY_TO_MANY_FIELD_TEMPLATE, ONE_TO_ONE_FIELD_TEMPLATE,
                                   SERIALIZER_TEMPLATE)


class Field(Enum):
    Genl = FIELD_TEMPLATE
    Char = CHAR_FIELD_TEMPLATE
    Foreign = FOREIGN_KEY_TEMPLATE
    ManyToMany = MANY_TO_MANY_FIELD_TEMPLATE
    OneToOne = ONE_TO_ONE_FIELD_TEMPLATE
    Decimal = DECIMAL_FIELD_TEMPLATE


class FieldTemplate:
    @staticmethod
    def convert(context):
        try:
            pattern = Field[context.get('type')].value
        except KeyError:
            pattern = Field.Genl.value
        return Template(pattern).render(context=Context(context))


class ModelTemplate:
    @staticmethod
    def convert(context):
        return Template(MODEL_TEMPLATE).render(context=Context(context))


class SerializerTemplate:
    @staticmethod
    def convert(context):
        return Template(SERIALIZER_TEMPLATE).render(context=Context(context))