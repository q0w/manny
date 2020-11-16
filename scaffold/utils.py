import functools


def default_kwargs(**defaultKwargs):
    def actual_decorator(fn):
        @functools.wraps(fn)
        def g(*args, **kwargs):
            defaultKwargs.update(kwargs)
            return fn(*args, **defaultKwargs)

        return g

    return actual_decorator


class safelist(list):
    def get(self, index, default=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            return default


def prompt_parse(s):
    core_names = safelist(s.split('--model '))
    app_names, model_data = core_names.get(0).split(' '), core_names.get(1)
    if not model_data:
        return app_names, None, None

    model_name, fields = model_data.split(' ')[0], model_data.split(' ')[1:]
    return app_names, model_name, fields
