# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午2:14
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : node.py
@Software: PyCharm
"""
from typing import Literal, Optional
from enum import Enum

from pydantic import BaseModel, Field

from liteyuki_autodoc.docstring.docstring import Docstring
from liteyuki_autodoc.i18n import get_text


class TypeHint:
    NO_TYPEHINT = "NO_TYPE_HINT"
    NO_DEFAULT = "NO_DEFAULT"
    NO_RETURN = "NO_RETURN"


class AssignNode(BaseModel):
    """
    AssignNode is a pydantic model that represents an assignment.
    Attributes:
        name: str
            The name of the assignment.
        type: str = ""
            The type of the assignment.
        value: str
            The value of the assignment.
    """
    name: str
    type: str = ""
    value: str


class ArgNode(BaseModel):
    """
    ArgNode is a pydantic model that represents an argument.
    Attributes:
        name: str
            The name of the argument.
        type: str = ""
            The type of the argument.
        default: str = ""
            The default value of the argument.
    """
    name: str
    type: str = TypeHint.NO_TYPEHINT


class AttrNode(BaseModel):
    """
    AttrNode is a pydantic model that represents an attribute.
    Attributes:
        name: str
            The name of the attribute.
        type: str = ""
            The type of the attribute.
        value: str = ""
            The value of the attribute
    """
    name: str
    type: str = ""
    value: str = ""


class ImportNode(BaseModel):
    """
    ImportNode is a pydantic model that represents an import statement.
    Attributes:
        name: str
            The name of the import statement.
        as_: str = ""
            The alias of the import
    """
    name: str
    as_: str = ""


class ConstantNode(BaseModel):
    """
    ConstantNode is a pydantic model that represents a constant.
    Attributes:
        value: str
            The value of the constant.
    """
    value: str


class FunctionNode(BaseModel):
    """
    FunctionNode is a pydantic model that represents a function.
    Attributes:
        name: str
            The name of the function.
        docs: str = ""
            The docstring of the function.
        args: list[ArgNode] = []
            The arguments of the function.
        return_: ReturnNode = None
            The return value of the function.
        decorators: list[str] = []
            The decorators of the function.
        is_async: bool = False
            Whether the function is asynchronous.
    """
    name: str
    docs: Optional[Docstring] = None

    posonlyargs: list[ArgNode] = []
    args: list[ArgNode] = []
    kwonlyargs: list[ArgNode] = []
    kw_defaults: list[ConstantNode] = []
    defaults: list[ConstantNode] = []

    return_: str = TypeHint.NO_RETURN
    decorators: list[str] = []
    src: str
    is_async: bool = False

    def is_private(self):
        """
        Check if the function or method is private.
        Returns:
            bool: True if the function or method is private, False otherwise.
        """
        return self.name.startswith("_")

    def is_builtin(self):
        """
        Check if the function or method is a builtin function or method.
        Returns:
            bool: True if the function or method is a builtin function or method, False otherwise.
        """
        return self.name.startswith("__") and self.name.endswith("__")

    def markdown(self, lang: str, indent: int = 0, is_classmethod: bool = False) -> str:
        """
        Args:
            indent: int
                The number of spaces to indent the markdown.
            is_classmethod: bool
            lang: str
                The language of the
        Returns:
            markdown style document
        """
        self.complete_default_args()
        PREFIX = "" * indent
        # if is_classmethod:
        #     PREFIX = "- #"

        md = ""

        # 装饰器部分
        if len(self.decorators) > 0:
            for decorator in self.decorators:
                md += PREFIX + f"### `@{decorator}`\n"

        if self.is_async:
            md += PREFIX + "### *async def* "
        else:
            md += PREFIX + "### *def* "

        md += f"`{self.name}("  # code start

        # 配对位置参数和位置参数默认值，无默认值用TypeHint.NO_DEFAULT
        args: list[str] = []  # 可直接", ".join(args)得到位置参数部分
        arg_i = 0

        if len(self.posonlyargs) > 0:
            for arg in self.posonlyargs:
                arg_text = f"{arg.name}"
                if arg.type != TypeHint.NO_TYPEHINT:
                    arg_text += f": {arg.type}"
                arg_default = self.defaults[arg_i].value
                if arg_default != TypeHint.NO_DEFAULT:
                    arg_text += f" = {arg_default}"
                args.append(arg_text)
                arg_i += 1
            # 加位置参数分割符  /
            args.append("/")

        for arg in self.args:
            arg_text = f"{arg.name}"
            if arg.type != TypeHint.NO_TYPEHINT:
                arg_text += f": {arg.type}"
            arg_default = self.defaults[arg_i].value
            if arg_default != TypeHint.NO_DEFAULT:
                arg_text += f" = {arg_default}"
            args.append(arg_text)
            arg_i += 1

        if len(self.kwonlyargs) > 0:
            # 加关键字参数分割符 *
            args.append("*")
            for arg, kw_default in zip(self.kwonlyargs, self.kw_defaults):
                arg_text = f"{arg.name}"
                if arg.type != TypeHint.NO_TYPEHINT:
                    arg_text += f": {arg.type}"

                if kw_default.value != TypeHint.NO_DEFAULT:
                    arg_text += f" = {kw_default.value}"
                args.append(arg_text)

        md += ", ".join(args) + ")"

        if self.return_ != TypeHint.NO_RETURN:
            md += f" -> {self.return_}"

        md += "`\n\n"  # code end

        """此处预留docstring"""
        if self.docs is not None:
            md += f"\n{self.docs.markdown(lang, indent, is_classmethod)}\n"
        else:
            pass
        # 源码展示
        md += PREFIX + f"\n<details>\n<summary>{get_text(lang, 'src')}</summary>\n\n```python\n{self.src}\n```\n</details>\n\n"

        return md

    def complete_default_args(self):
        """
        补全位置参数默认值，用无默认值插入
        Returns:

        """
        num = len(self.args) + len(self.posonlyargs) - len(self.defaults)
        self.defaults = [ConstantNode(value=TypeHint.NO_DEFAULT) for _ in range(num)] + self.defaults

    def __str__(self):
        return f"def {self.name}({', '.join([f'{arg.name}: {arg.type} = {arg.default}' for arg in self.args])}) -> {self.return_}"


class ClassNode(BaseModel):
    """
    ClassNode is a pydantic model that represents a class.
    Attributes:
        name: str
            The name of the class.
        docs: str = ""
            The docstring of the class.
        attrs: list[AttrNode] = []
            The attributes of the class.
        methods: list[MethodNode] = []
            The methods of the class.
        inherit: list["ClassNode"] = []
            The classes that the class inherits from
    """
    name: str
    docs: Optional[Docstring] = None
    attrs: list[AttrNode] = []
    methods: list[FunctionNode] = []
    inherit: list["ClassNode"] = []
