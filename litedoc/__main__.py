# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/28 下午4:08
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : __main__.py
@Software: PyCharm
"""
# command line tool
# args[0] path
# -o|--output output path
# -l|--lang zh-Hans en jp default zh-Hans


import argparse
import os
import sys

from litedoc.output import generate_from_module


def main():
    parser = argparse.ArgumentParser(description="Generate documentation from Python modules.")
    parser.add_argument("path", type=str, help="Path to the Python module or package.")
    parser.add_argument("-o", "--output", default="doc-output", type=str, help="Output directory.")
    parser.add_argument("-c", "--contain-top", action="store_true", help="Whether to contain top-level dir in output dir.")
    parser.add_argument("-cs", "--create-same", action="store_true", help="Create same file with folder name")
    parser.add_argument("-bu", "--base-url", default=None, type=str, help="base url of the document.")
    parser.add_argument("-l", "--lang", default="zh_Hans", type=str, help="Languages of the document.")
    parser.add_argument("-t", "--theme", default="vitepress", type=str, help="Theme of the document.")
    parser.add_argument("-s", "--style", default="google", type=str, help="Style of the document.")
    parser.add_argument("-f", "--frontmatter", default=None, type=str, help="Frontmatter of the document.")

    parser.add_argument("-fd", "--function-define", default="func", type=str, help="Function define of the document.")
    parser.add_argument("-md", "--method-define", default="method", type=str, help="Class function define of the document.")
    parser.add_argument("-cd", "--class-define", default="class", type=str, help="Class define of the document.")
    parser.add_argument("-vd", "--var-define", default="var", type=str, help="Variable define of the document.")
    parser.add_argument("-ad", "--attr-define", default="attr", type=str, help="Attribute define of the document.")
    # frontmatter 输入格式为 key1=value1,key2=value2, 空格用%20代替

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The path {args.path} does not exist.")
        sys.exit(1)

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    lang = args.lang

    if args.frontmatter is not None:
        frontmatter = {}
        for item in args.frontmatter.split(","):
            key, value = item.split("=")
            frontmatter[key] = value.replace("%20", " ")
    else:
        frontmatter = None

    generate_from_module(
        args.path, args.output,
        with_top=args.contain_top,
        lang=lang,
        theme=args.theme,
        style=args.style,
        frontmatter=frontmatter,
        fd=args.function_define,
        md=args.method_define,
        cd=args.class_define,
        vd=args.var_define,
        ad=args.attr_define,
        cs=args.create_same,
        bu=args.base_url
    )


if __name__ == '__main__':
    main()
