import ast


def remove_docstring_from_function(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if len(node.body) > 0 and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
            node.body.pop(0)
    return node


def remove_docstrings_from_code(source_code):
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        remove_docstring_from_function(node)
    return ast.unparse(tree)
