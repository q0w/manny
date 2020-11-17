import functools
import ast
import astor


def default_kwargs(**defaultKwargs):
    def actual_decorator(fn):
        @functools.wraps(fn)
        def g(*args, **kwargs):
            defaultKwargs.update(kwargs)
            return fn(*args, **defaultKwargs)

        return g

    return actual_decorator


class Walker(ast.NodeTransformer):
    __imports = {}

    def __init__(self, file, options):
        self.file = file
        with open(self.file, 'r') as f:
            self.tree = ast.parse(f.read())
        self.options = options
        super().__init__()

    def visit_Assign(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        if node.targets[0].id == self.options['variable']:
            node.value.elts.extend([ast.Constant(value=x, kind=None) for x in self.options['variable_values']])
        return node

    def visit_Import(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.__imports['free'] = [x.name for x in node.names]

    def visit_ImportFrom(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.__imports[node.module] = [x.name for x in node.names]

    def get_imports(self):
        self.visit(self.tree)
        return self.__imports

    def mutate(self):
        with open(self.file, 'w') as f:
            f.write(astor.to_source(self.visit(self.tree)))

    def get_assignments(self, variable):
        for node in ast.walk(self.get_tree()):
            if isinstance(node, ast.Assign) and node.targets[0].id == variable:
                assignments = [x.value for x in node.value.elts]
                return assignments
        return None
