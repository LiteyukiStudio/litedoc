# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午3:39
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : markdown.py
@Software: PyCharm
"""
from typing import Optional

from liteyuki_autodoc.syntax.astparser import AstParser
from liteyuki_autodoc.syntax.node import *
from liteyuki_autodoc.i18n import get_text


def generate(parser: AstParser, lang: str, frontmatter: Optional[dict] = None) -> str:
    """
    Generate markdown style document from ast
    You can modify this function to generate markdown style that enjoys you
    Args:
        parser:
        lang: language
        frontmatter:
    Returns:
        markdown style document
    """
    if frontmatter is not None:
        md = "---\n"
        for k, v in frontmatter.items():
            md += f"{k}: {v}\n"
        md += "---\n"
    else:
        md = ""

    # var > func > class

    for func in parser.functions:
        md += func.markdown(lang)

    for cls in parser.classes:
        md += f"### ***class*** `{cls.name}`\n\n"
        for mtd in cls.methods:
            md += mtd.markdown(lang, 2, True)

        for attr in cls.attrs:
            if attr.type == TypeHint.NO_TYPEHINT:
                md += f"#### ***attr*** `{attr.name} = {attr.value}`\n\n"
            else:
                md += f"#### ***attr*** `{attr.name}: {attr.type} = {attr.value}`\n\n"

    for var in parser.variables:
        if var.type == TypeHint.NO_TYPEHINT:
            md += f"### ***var*** `{var.name} = {var.value}`\n\n"
        else:
            md += f"### ***var*** `{var.name}: {var.type} = {var.value}`\n\n"

    return md
