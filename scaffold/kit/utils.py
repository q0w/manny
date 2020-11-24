import ast
import astor


class Walker(ast.NodeTransformer):
    __imports = {}
    __models = []

    def __init__(self, file, options=None):
        self.file = file
        with open(self.file, 'r') as f:
            self.tree = ast.parse(f.read())
        self.options = options
        super().__init__()

    def visit_Assign(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        if self.options:
            if node.targets[0].id == self.options['variable']:
                node.value.elts.extend([ast.Constant(value=x, kind=None) for x in self.options['variable_values'] if
                                        x not in [app.value for app in node.value.elts]])
        return node

    def visit_Import(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.__imports['free'] = [x.name for x in node.names]
        return node

    def visit_ImportFrom(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.__imports[node.module] = [x.name for x in node.names]
        return node

    def visit_ClassDef(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        if node.bases and node.bases[0].value.id == 'models' and node.bases[0].attr == 'Model':
            if node.name not in self.__models: self.__models.append(node.name)
        return node

    def get_imports(self):
        self.visit(self.tree)
        return self.__imports

    def get_models(self):
        self.visit(self.tree)
        return self.__models

    def mutate(self):
        with open(self.file, 'w') as f:
            f.write(astor.to_source(self.visit(self.tree)))

