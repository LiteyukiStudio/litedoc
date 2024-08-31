# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午2:14
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : node.py
@Software: PyCharm
"""
from typing import Optional

from pydantic import BaseModel

from litedoc.docstring.docstring import Docstring
from litedoc.i18n import get_text, litedoc_hide


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
    docs: Optional[str] = ""

    def markdown(self, lang: str, **kwargs) -> str:
        """
        Args:
            lang: str
                The language of the
        Returns:
            markdown style document
        """
        vd = kwargs.get("vd", "var")
        md = ""
        md += f"### {vd} `{self.name}`\n\n"
        if self.docs is not None:
            md += f"- **{get_text(lang, 'desc')}**: {self.docs}\n\n"
        if self.type != TypeHint.NO_TYPEHINT:
            md += f"- **{get_text(lang, 'type')}**: `{self.type}`\n\n"
        md += f"- **{get_text(lang, 'default_value')}**: `{self.value}`\n\n"


        return md


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
    vararg: Optional[ArgNode] = None
    kwonlyargs: list[ArgNode] = []
    kwarg: Optional[ArgNode] = None
    kw_defaults: list[ConstantNode] = []
    defaults: list[ConstantNode] = []

    lineno: int = 0
    module_file_path: str = ""  # 去头路径，不包含模块顶级文件夹

    return_: str = TypeHint.NO_RETURN
    decorators: list[str] = []
    src: str
    is_async: bool = False
    is_classmethod: bool = False

    magic_methods: dict[str, str] = {
            "__add__"     : "+",
            "__radd__"    : "+",
            "__sub__"     : "-",
            "__rsub__"    : "-",
            "__mul__"     : "*",
            "__rmul__"    : "*",
            "__matmul__"  : "@",
            "__rmatmul__" : "@",
            "__mod__"     : "%",
            "__truediv__" : "/",
            "__rtruediv__": "/",
            "__neg__"     : "-",
    }  # 魔术方法, 例如运算符

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

    def markdown(self, lang: str, indent: int = 0, **kwargs) -> str:
        """
        Args:
            indent: int
                The number of spaces to indent the markdown.
            lang: str
                The language of the
            **kwargs: more parameters
        Returns:
            markdown style document
        """
        self.complete_default_args()
        PREFIX = "" * indent
        # if is_classmethod:
        #     PREFIX = "- #"
        func_type = kwargs.get("fd", "func") if not self.is_classmethod else kwargs.get("md", "method")
        h_level = 3 if not self.is_classmethod else 4
        h = "#" * h_level
        """标题等级"""

        md = ""
        # 装饰器部分
        # 特殊装饰器
        special_decorators = {
            "classmethod": "https://docs.python.org/3/library/functions.html#classmethod",
            "staticmethod": "https://docs.python.org/3/library/functions.html#staticmethod",
            "property": "https://docs.python.org/3/library/functions.html#property",
            "abstractmethod": "https://docs.python.org/3/library/abc.html#abc.abstractmethod",
        }
        if len(self.decorators) > 0:
            for decorator in self.decorators:
                if decorator in special_decorators:
                    md += PREFIX + f"[`@{decorator}`]({special_decorators[decorator]})\n"
                else:
                    md += PREFIX + f"`@{decorator}`\n"

        if self.is_async:
            md += PREFIX + f"{h} ***async {func_type}*** "
        else:
            md += PREFIX + f"{h} ***{func_type}*** "

        # code start
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

        if arg := self.vararg:
            arg_text = f"*{arg.name}"
            if arg.type != TypeHint.NO_TYPEHINT:
                arg_text += f": {arg.type}"
            args.append(arg_text)

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

        if self.kwarg is not None:
            arg_text = f"**{self.kwarg.name}"
            if self.kwarg.type != TypeHint.NO_TYPEHINT:
                arg_text += f": {self.kwarg.type}"
            args.append(arg_text)

        """魔法方法"""
        if self.name in self.magic_methods:
            if len(args) == 2:
                md += f"`{args[0]} {self.magic_methods[self.name]} {args[1]}"
            elif len(args) == 1:
                md += f"`{self.magic_methods[self.name]} {args[0]}"
            if self.return_ != TypeHint.NO_RETURN:
                md += f" => {self.return_}"
        else:
            md += f"`{self.name}("  # code start
            md += ", ".join(args) + ")"
            if self.return_ != TypeHint.NO_RETURN:
                md += f" -> {self.return_}"

        md += "`\n\n"  # code end

        """此处预留docstring"""
        if self.docs is not None:
            md += f"\n{self.docs.markdown(lang, indent)}\n"
        else:
            pass
        # 源码展示
        if kwargs.get("bu", None):
            # 源码链接
            self.module_file_path = self.module_file_path.replace("\\", "/")
            origin_url = kwargs.get("bu") + f"{self.module_file_path}#L{self.lineno}"
            # a_tag = f"\n\n[{get_text(lang, 'view_on_github')}]({origin_url})"
            a_tag = f"<a href='{origin_url}' target='_blank'>{get_text(lang, 'view_on_github')}</a>"
            or_and_a = f" {get_text(lang, 'or')} {a_tag}"
        else:
            a_tag = ""
            or_and_a = ""
        md += PREFIX + f"\n<details>\n<summary> <b>{get_text(lang, 'src')}</b>{or_and_a}</summary>\n\n```python\n{self.src}\n```\n</details>\n\n"

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
        inherits: list["ClassNode"] = []
            The classes that the class inherits from
    """
    name: str
    docs: Optional[Docstring] = None
    attrs: list[AttrNode] = []
    methods: list[FunctionNode] = []
    inherits: list[str] = []

    def markdown(self, lang: str, **kwargs) -> str:
        """
        返回类的markdown文档
        Args:
            lang: str
                The language of the
        Returns:
            markdown style document
        """
        hidden_methods = [
                "__str__",
                "__repr__",
        ]
        md = ""
        md += f"### ***{kwargs.get('cd', 'class')}*** `{self.name}"
        if len(self.inherits) > 0:
            md += f"({', '.join([cls for cls in self.inherits])})"
        md += "`\n"
        for method in self.methods:
            if (method.name in hidden_methods or
                    method.name.startswith("_") and not method.name.startswith("__") or
                    method.docs is not None and litedoc_hide in method.docs.reduction()):
                continue
            md += method.markdown(lang, 2, **kwargs)
        for attr in self.attrs:
            if attr.type == TypeHint.NO_TYPEHINT:
                md += f"#### ***{kwargs.get('ad', get_text(lang, 'docstring.attribute'))}*** `{attr.name} = {attr.value}`\n\n"
            else:
                md += f"#### ***{kwargs.get('ad', get_text(lang, 'docstring.attribute'))}*** `{attr.name}: {attr.type} = {attr.value}`\n\n"

        return md
