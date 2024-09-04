# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午3:39
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : markdown.py
@Software: PyCharm
"""

from litedoc.syntax.astparser import AstParser
from litedoc.syntax.node import *
from litedoc.i18n import litedoc_hide


def generate(parser: AstParser, lang: str, frontmatter: Optional[dict] = None, **kwargs) -> str:
    """
    Generate markdown style document from ast
    You can modify this function to generate markdown style that enjoys you
    Args:
        parser:
        lang: language
        frontmatter:
        **kwargs: 更多参数
    Returns:
        markdown style document
    """
    code_frontmatter = parser.description.front_matter if parser.description is not None and parser.description.front_matter else {}
    frontmatter = frontmatter or {}
    frontmatter.update(code_frontmatter)
    if frontmatter:
        md = "---\n"
        for k, v in frontmatter.items():
            md += f"{k}: {v}\n"
        md += "---\n"
    else:
        md = ""

    # 添加标题，如果有
    if parser.title is not None:
        md += f"# **{get_text(lang, 'module')}** `{parser.title}`\n\n"

    # 添加描述，如果有
    if parser.description is not None:
        md += f"{parser.description.markdown(lang)}\n\n"

    for node in parser.all_nodes:
        if isinstance(node, FunctionNode):
            if node.name.startswith("_") or (node.docs is not None and litedoc_hide in node.docs.reduction()):
                print("skip", node.name)
                continue
            md += node.markdown(lang, **kwargs)
        elif isinstance(node, ClassNode):
            md += node.markdown(lang, **kwargs)
        elif isinstance(node, AssignNode):
            if node.docs is not None and litedoc_hide not in node.docs:
                md += node.markdown(lang, **kwargs)
    return md
