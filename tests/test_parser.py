# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午2:30
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : test_parser.py
@Software: PyCharm
"""
import os

from liteyuki_autodoc.syntax.astparser import AstParser


class TestParser:

    def test_one_file(self):
        file = "test_modules/tree.py"
        text = open(file, "r", encoding="utf-8").read()
        parser = AstParser(text)
        print(parser)
