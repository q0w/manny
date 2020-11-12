import functools


def default_kwargs(**defaultKwargs):
    def actual_decorator(fn):
        @functools.wraps(fn)
        def g(*args, **kwargs):
            defaultKwargs.update(kwargs)
            return fn(*args, **defaultKwargs)

        return g

    return actual_decorator
