# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/9 上午11:32
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : equation.py
@Software: PyCharm
"""

from mbcp.mp_math.mp_math_typing import OneVarFunc, Var, MultiVarsFunc, Number
from mbcp.mp_math.point import Point3
from mbcp.mp_math.const import EPSILON


class CurveEquation:
    def __init__(self, x_func: OneVarFunc, y_func: OneVarFunc, z_func: OneVarFunc):
        """
        曲线方程。
        :param x_func:
        :param y_func:
        :param z_func:
        """
        self.x_func = x_func
        self.y_func = y_func
        self.z_func = z_func

    def __call__(self, *t: Var) -> Point3 | tuple[Point3, ...]:
        """
        计算曲线上的点。
        Args:
            *t:

        Returns:

        """
        if len(t) == 1:
            return Point3(self.x_func(t[0]), self.y_func(t[0]), self.z_func(t[0]))
        else:
            return tuple([Point3(x, y, z) for x, y, z in zip(self.x_func(t), self.y_func(t), self.z_func(t))])

    def __str__(self):
        return "CurveEquation()"


def get_partial_derivative_func(func: MultiVarsFunc, var: int | tuple[int, ...], epsilon: Number = EPSILON) -> MultiVarsFunc:
    """
    求N元函数一阶偏导函数。这玩意不太稳定，慎用。
    Args:
        func: 函数
        var: 变量位置，可为整数(一阶偏导)或整数元组(高阶偏导)
        epsilon: 偏移量
    Returns:
        偏导函数
    Raises:
        ValueError: 无效变量类型
    """
    if isinstance(var, int):
        def partial_derivative_func(*args: Var) -> Var:
            args_list_plus = list(args)
            args_list_plus[var] += epsilon
            args_list_minus = list(args)
            args_list_minus[var] -= epsilon
            return (func(*args_list_plus) - func(*args_list_minus)) / (2 * epsilon)
        return partial_derivative_func
    elif isinstance(var, tuple):
        def high_order_partial_derivative_func(*args: Var) -> Var:
            result_func = func
            for v in var:
                result_func = get_partial_derivative_func(result_func, v, epsilon)
            return result_func(*args)
        return high_order_partial_derivative_func
    else:
        raise ValueError("Invalid var type")
