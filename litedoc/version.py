# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/29 下午2:36
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : version.py.py
@Software: PyCharm
"""


def format_date_number() -> str:
    """
    将日期转换为20240212114514
    Args:
        date: 日期
    Returns:
        日期字符串
    """
    import datetime
    date = datetime.datetime.now()
    return date.strftime("%Y%m%d%H%M%S")


def get_version() -> str:
    return f"0.1.0.dev{format_date_number()}"
