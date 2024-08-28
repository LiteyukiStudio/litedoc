# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午2:13
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : astparser.py
@Software: PyCharm
"""
import ast

from .node import *
from ..docstring.parser import parse


class AstParser:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)

        self.classes: list[ClassNode] = []
        self.functions: list[FunctionNode] = []
        self.variables: list[AssignNode] = []

        self.parse()

    def parse(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                if not self._is_module_level_class(node):
                    continue

                class_node = ClassNode(
                    name=node.name,
                    docs=parse(ast.get_docstring(node)) if ast.get_docstring(node) else None,
                    inherits=[ast.unparse(base) for base in node.bases]
                )
                self.classes.append(class_node)

                # 继续遍历类内部的函数
                for sub_node in node.body:
                    if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        class_node.methods.append(FunctionNode(
                            name=sub_node.name,
                            docs=parse(ast.get_docstring(sub_node)) if ast.get_docstring(sub_node) else None,
                            posonlyargs=[
                                    ArgNode(
                                        name=arg.arg,
                                        type=ast.unparse(arg.annotation).strip() if arg.annotation else TypeHint.NO_TYPEHINT,
                                    )
                                    for arg in sub_node.args.posonlyargs
                            ],
                            args=[
                                    ArgNode(
                                        name=arg.arg,
                                        type=ast.unparse(arg.annotation).strip() if arg.annotation else TypeHint.NO_TYPEHINT,
                                    )
                                    for arg in sub_node.args.args
                            ],
                            kwonlyargs=[
                                    ArgNode(
                                        name=arg.arg,
                                        type=ast.unparse(arg.annotation).strip() if arg.annotation else TypeHint.NO_TYPEHINT,
                                    )
                                    for arg in sub_node.args.kwonlyargs
                            ],
                            kw_defaults=[
                                    ConstantNode(
                                        value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT
                                    )
                                    for default in sub_node.args.kw_defaults
                            ],
                            defaults=[
                                    ConstantNode(
                                        value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT
                                    )
                                    for default in sub_node.args.defaults
                            ],
                            return_=ast.unparse(sub_node.returns).strip() if sub_node.returns else TypeHint.NO_RETURN,
                            decorators=[ast.unparse(decorator).strip() for decorator in sub_node.decorator_list],
                            is_async=isinstance(sub_node, ast.AsyncFunctionDef),
                            src=ast.unparse(sub_node).strip()
                        ))
                    elif isinstance(sub_node, (ast.Assign, ast.AnnAssign)):
                        if isinstance(sub_node, ast.Assign):
                            class_node.attrs.append(AttrNode(
                                name=sub_node.targets[0].id,  # type: ignore
                                type=TypeHint.NO_TYPEHINT,
                                value=ast.unparse(sub_node.value).strip()
                            ))
                        elif isinstance(sub_node, ast.AnnAssign):
                            class_node.attrs.append(AttrNode(
                                name=sub_node.target.id,
                                type=ast.unparse(sub_node.annotation).strip(),
                                value=ast.unparse(sub_node.value).strip() if sub_node.value else TypeHint.NO_DEFAULT
                            ))
                        else:
                            raise ValueError(f"Unsupported node type: {type(sub_node)}")

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 仅打印模块级别的函数
                if not self._is_module_level_function(node):
                    continue

                self.functions.append(FunctionNode(
                    name=node.name,
                    docs=parse(ast.get_docstring(node)) if ast.get_docstring(node) else None,
                    posonlyargs=[
                            ArgNode(
                                name=arg.arg,
                                type=ast.unparse(arg.annotation).strip() if arg.annotation else TypeHint.NO_TYPEHINT,
                            )
                            for arg in node.args.posonlyargs
                    ],
                    args=[
                            ArgNode(
                                name=arg.arg,
                                type=ast.unparse(arg.annotation).strip() if arg.annotation else TypeHint.NO_TYPEHINT,
                            )
                            for arg, default in zip(node.args.args, node.args.defaults)
                    ],
                    kwonlyargs=[
                            ArgNode(
                                name=arg.arg,
                                type=ast.unparse(arg.annotation).strip() if arg.annotation else TypeHint.NO_TYPEHINT,
                            )
                            for arg in node.args.kwonlyargs
                    ],
                    kw_defaults=[
                            ConstantNode(
                                value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT
                            )
                            for default in node.args.kw_defaults
                    ],
                    defaults=[
                            ConstantNode(
                                value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT
                            )
                            for default in node.args.defaults
                    ],
                    return_=ast.unparse(node.returns).strip() if node.returns else TypeHint.NO_RETURN,
                    decorators=[ast.unparse(decorator).strip() for decorator in node.decorator_list],
                    is_async=isinstance(node, ast.AsyncFunctionDef),
                    src=ast.unparse(node).strip()
                ))

            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                if not self._is_module_level_variable2(node):
                    # print("变量不在模块级别", ast.unparse(node))
                    continue
                else:
                    pass
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.variables.append(AssignNode(
                                name=target.id,
                                value=ast.unparse(node.value).strip(),
                                type=ast.unparse(node.annotation).strip() if isinstance(node, ast.AnnAssign) else TypeHint.NO_TYPEHINT
                            ))
                elif isinstance(node, ast.AnnAssign):
                    self.variables.append(AssignNode(
                        name=node.target.id,
                        value=ast.unparse(node.value).strip() if node.value else TypeHint.NO_DEFAULT,
                        type=ast.unparse(node.annotation).strip()
                    ))

    def _is_module_level_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        for parent in ast.walk(self.tree):
            if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if node in parent.body:
                    return False
        return True

    def _is_module_level_class(self, node: ast.ClassDef):
        for parent in ast.walk(self.tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return False
        return True

    def _is_module_level_variable(self, node: ast.Assign | ast.AnnAssign):
        """在类方法或函数内部的变量不会被记录"""

        # for parent in ast.walk(self.tree):
        #     if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        #         if node in parent.body:
        #             return False
        #         else:
        #             for sub_node in parent.body:
        #                 if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        #                     if node in sub_node.body:
        #                         return False
        # return True
        # 递归检查
        def _check(_node, _parent):
            if isinstance(_parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if _node in _parent.body:
                    return False
                else:
                    for sub_node in _parent.body:
                        if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            return _check(_node, sub_node)
            return True

        for parent in ast.walk(self.tree):
            if not _check(node, parent):
                return False
        return True

    def _is_module_level_variable2(self, node: ast.Assign | ast.AnnAssign) -> bool:
        """
        检查变量是否在模块级别定义。
        """
        for parent in ast.walk(self.tree):
            if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if node in parent.body:
                    return False
        return True

    def __str__(self):
        s = ""
        for cls in self.classes:
            s += f"class {cls.name}:\n"
        for func in self.functions:
            s += f"def {func.name}:\n"
        for var in self.variables:
            s += f"{var.name} = {var.value}\n"
        return s
