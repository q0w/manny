import functools
from string import Template


def default_kwargs(**defaultKwargs):
    def actual_decorator(fn):
        @functools.wraps(fn)
        def g(*args, **kwargs):
            defaultKwargs.update(kwargs)
            return fn(*args, **defaultKwargs)

        return g

    return actual_decorator


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
