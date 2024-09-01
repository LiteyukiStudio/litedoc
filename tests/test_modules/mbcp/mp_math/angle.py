# -*- coding: utf-8 -*-
"""
---
test: Test
---
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/26 上午6:29
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : angle.py
@Software: PyCharm
"""
import math
from typing import overload

from .const import PI  # type: ignore
from .utils import approx


class Angle:
    ...


class AnyAngle(Angle):
    def __init__(self, value: float, is_radian: bool = False):
        """
        任意角度。
        Args:
            value: 角度或弧度值
            is_radian: 是否为弧度，默认为否
        """
        if is_radian:
            self.radian = value
        else:
            self.radian = value * PI / 180

    @property
    def complementary(self) -> 'AnyAngle':
        """
        余角：两角的和为90°。
        Returns:
            余角
        """
        return AnyAngle(PI / 2 - self.minimum_positive.radian, is_radian=True)

    @property
    def supplementary(self) -> 'AnyAngle':
        """
        补角：两角的和为180°。
        Returns:
            补角
        """
        return AnyAngle(PI - self.minimum_positive.radian, is_radian=True)

    @property
    def degree(self) -> float:
        """
        角度。
        Returns:
            弧度
        """
        return self.radian * 180 / PI

    @property
    def minimum_positive(self) -> 'AnyAngle':
        """
        最小正角。
        Returns:
            最小正角度
        """
        return AnyAngle(self.radian % (2 * PI))

    @property
    def maximum_negative(self) -> 'AnyAngle':
        """
        最大负角。
        Returns:
            最大负角度
        """
        return AnyAngle(-self.radian % (2 * PI), is_radian=True)

    @property
    def sin(self) -> float:
        """
        正弦值。
        Returns:
            正弦值
        """
        return math.sin(self.radian)

    @property
    def cos(self) -> float:
        """
        余弦值。
        Returns:
            余弦值
        """
        return math.cos(self.radian)

    @property
    def tan(self) -> float:
        """
        正切值。
        Returns:
            正切值
        """
        return math.tan(self.radian)

    @property
    def cot(self) -> float:
        """
        余切值。
        Returns:
            余切值
        """
        return 1 / math.tan(self.radian)

    @property
    def sec(self) -> float:
        """
        正割值。
        Returns:
            正割值
        """
        return 1 / math.cos(self.radian)

    @property
    def csc(self) -> float:
        """
        余割值。
        Returns:
            余割值
        """
        return 1 / math.sin(self.radian)

    def __add__(self, other: 'AnyAngle') -> 'AnyAngle':
        return AnyAngle(self.radian + other.radian, is_radian=True)

    def __eq__(self, other):
        return approx(self.radian, other.radian)

    def __sub__(self, other: 'AnyAngle') -> 'AnyAngle':
        return AnyAngle(self.radian - other.radian, is_radian=True)

    def __mul__(self, other: float) -> 'AnyAngle':
        return AnyAngle(self.radian * other, is_radian=True)

    def __repr__(self):
        return f"AnyAngle({self.radian}, is_radian=True)"

    def __str__(self):
        return f"AnyAngle({self.degree}° or {self.radian} rad)"

    @overload
    def __truediv__(self, other: float) -> 'AnyAngle':
        ...

    @overload
    def __truediv__(self, other: 'AnyAngle') -> float:
        ...

    def __truediv__(self, other):
        if isinstance(other, AnyAngle):
            return self.radian / other.radian
        return AnyAngle(self.radian / other, is_radian=True)
