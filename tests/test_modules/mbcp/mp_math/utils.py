# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/12 下午9:16
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : utils.py
@Software: PyCharm
"""
from typing import overload, TYPE_CHECKING

from .mp_math_typing import RealNumber
from .const import APPROX

if TYPE_CHECKING:
    from .vector import Vector3
    from .point import Point3
    from .plane import Plane3
    from .line import Line3


def clamp(x: float, min_: float, max_: float) -> float:
    """
    区间限定函数
    Args:
        x: 待限定的值
        min_: 最小值
        max_: 最大值

    Returns:
        限制后的值
    """
    return max(min(x, max_), min_)


class Approx:
    """
    用于近似比较对象

    已实现对象 实数 Vector3 Point3 Plane3 Line3
    """
    def __init__(self, value: RealNumber):
        self.value = value

    def __eq__(self, other):
        if isinstance(self.value, (float, int)):
            if isinstance(other, (float, int)):
                return abs(self.value - other) < APPROX
            else:
                self.raise_type_error(other)
        elif isinstance(self.value, Vector3):
            if isinstance(other, (Vector3, Point3, Plane3, Line3)):
                return all([approx(self.value.x, other.x), approx(self.value.y, other.y), approx(self.value.z, other.z)])
            else:
                self.raise_type_error(other)

    def raise_type_error(self, other):
        raise TypeError(f"Unsupported type: {type(self.value)} and {type(other)}")

    def __ne__(self, other):
        return not self.__eq__(other)


def approx(x: float, y: float = 0.0, epsilon: float = APPROX) -> bool:
    """
    判断两个数是否近似相等。或包装一个实数，用于判断是否近似于0。
    Args:
        x: 数1
        y: 数2
        epsilon: 误差
    Returns:
        是否近似相等
    """
    return abs(x - y) < epsilon


def sign(x: float, only_neg: bool = False) -> str:
    """获取数的符号。
    Args:
        x: 数
        only_neg: 是否只返回负数的符号
    Returns:
        符号 + - ""
    """
    if x > 0:
        return "+" if not only_neg else ""
    elif x < 0:
        return "-"
    else:
        return ""


def sign_format(x: float, only_neg: bool = False) -> str:
    """格式化符号数
    -1 -> -1
    1 -> +1
    0 -> ""
    Args:
        x: 数
        only_neg: 是否只返回负数的符号
    Returns:
        符号 + - ""
    """
    if x > 0:
        return f"+{x}" if not only_neg else f"{x}"
    elif x < 0:
        return f"-{abs(x)}"
    else:
        return ""
