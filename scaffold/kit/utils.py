import functools
import ast


def default_kwargs(**defaultKwargs):
    def actual_decorator(fn):
        @functools.wraps(fn)
        def g(*args, **kwargs):
            defaultKwargs.update(kwargs)
            return fn(*args, **defaultKwargs)

        return g

    return actual_decorator


class FileScanner:
    def __init__(self, file):
        self.file = file

    def get_tree(self):
        with open(self.file, 'r') as f:
            tree = ast.parse(f.read())
        return tree

    def get_imports(self):
        imports = {}
        for node in ast.walk(self.get_tree()):
            if isinstance(node, ast.ImportFrom):
                imports[node.module] = [x.name for x in node.names]
            if isinstance(node, ast.Import):
                imports[None] = [x.name for x in node.names]
        return imports

    def get_assignments(self, variable):
        for node in ast.walk(self.get_tree()):
            if isinstance(node, ast.Assign) and node.targets[0].id == variable:
                assignments = [x.value for x in node.value.elts]
                return assignments
        return None
