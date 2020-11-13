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
    def __init__(self):
        template = "$name = models.${type}Field(default='$default', null=$null, blank=$blank)"
        super().__init__(template)

    @default_kwargs(null=False, default='None', blank=False)
    def safe_replace(self, **kwargs):
        try:
            return self.substitute(**kwargs)
        except KeyError:
            raise SystemExit('Provide field name...')
