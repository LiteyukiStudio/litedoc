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

from litedoc.syntax.astparser import AstParser
from litedoc.syntax.node import *
from litedoc.i18n import get_text

litedoc_hide = "@litedoc-hide"


def generate(parser: AstParser, lang: str, frontmatter: Optional[dict] = None, style: str = "google") -> str:
    """
    Generate markdown style document from ast
    You can modify this function to generate markdown style that enjoys you
    Args:
        parser:
        lang: language
        frontmatter:
        style: style of docs
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

    # 添加标题，如果有
    if parser.title is not None:
        md += f"# {parser.title}\n\n"

    # 添加描述，如果有
    if parser.description is not None:
        md += f"{parser.description.markdown(lang)}\n\n"

    for node in parser.all_nodes:
        if isinstance(node, FunctionNode):
            if node.name.startswith("_") or (node.docs is not None and litedoc_hide in node.docs.reduction()):
                continue
            md += node.markdown(lang)
        elif isinstance(node, ClassNode):
            md += node.markdown(lang)
        elif isinstance(node, AssignNode):
            if node.docs is not None and litedoc_hide not in node.docs:
                md += node.markdown(lang)
    return md
