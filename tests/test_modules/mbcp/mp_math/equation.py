# -*- coding: utf-8 -*-
"""
本模块定义了一些数学方程相关的函数。
"""

from mbcp.mp_math.mp_math_typing import OneVarFunc, Var, MultiVarsFunc, Number
from mbcp.mp_math.point import Point3
from mbcp.mp_math.const import EPSILON


def cal_gradient_3vf(func: ThreeSingleVarsFunc, p: Point3, epsilon: float = EPSILON) -> Vector3:
    """
    计算三元函数在某点的梯度向量。
    $\nabla f(x_0, y_0, z_0) = \\left(\\frac{\\partial f}{\\partial x}, \\frac{\\partial f}{\\partial y}, \\frac{\\partial f}{\\partial z}\\right)$
    Args:
        func: 三元函数
        p: 点
        epsilon: 偏移量
    Returns:
        梯度
    """
    dx = (func(p.x + epsilon, p.y, p.z) - func(p.x - epsilon, p.y, p.z)) / (2 * epsilon)
    dy = (func(p.x, p.y + epsilon, p.z) - func(p.x, p.y - epsilon, p.z)) / (2 * epsilon)
    dz = (func(p.x, p.y, p.z + epsilon) - func(p.x, p.y, p.z - epsilon)) / (2 * epsilon)
    return Vector3(dx, dy, dz)


def cal_gradient_3vf2(func: ThreeSingleVarsFunc, p: Point3, epsilon: float = EPSILON) -> Vector3:
    """
    计算三元函数在某点的梯度向量。
    > [!tip]
    > 已知一个函数$f(x, y, z)$，则其在点$(x_0, y_0, z_0)$处的梯度向量为:
    Args:
        func: 三元函数
        p: 点
        epsilon: 偏移量
    Returns:
        梯度
    """
    dx = (func(p.x + epsilon, p.y, p.z) - func(p.x - epsilon, p.y, p.z)) / (2 * epsilon)
    dy = (func(p.x, p.y + epsilon, p.z) - func(p.x, p.y - epsilon, p.z)) / (2 * epsilon)
    dz = (func(p.x, p.y, p.z + epsilon) - func(p.x, p.y, p.z - epsilon)) / (2 * epsilon)
    return Vector3(dx, dy, dz)


class CurveEquation:
    def __init__(self, x_func: OneVarFunc, y_func: OneVarFunc, z_func: OneVarFunc):
        """
        曲线方程。
        Args:
            x_func: x函数
            y_func: y函数
            z_func: z函数
        """
        self.x_func = x_func
        self.y_func = y_func
        self.z_func = z_func

    def __call__(self, *t: Var) -> Point3 | tuple[Point3, ...]:
        """
        计算曲线上的点。
        Args:
            *t:
                参数
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
            """
            :param args:
            :return:
            """
            args_list_plus = list(args)
            args_list_plus[var] += epsilon
            args_list_minus = list(args)
            args_list_minus[var] -= epsilon
            return (func(*args_list_plus) - func(*args_list_minus)) / (2 * epsilon)

        return partial_derivative_func
    elif isinstance(var, tuple):
        def high_order_partial_derivative_func(*args: Var) -> Var:
            """
            求高阶偏导函数 @litedoc-hide
            :param args:
            :return:
            """
            result_func = func
            for v in var:
                result_func = get_partial_derivative_func(result_func, v, epsilon)
            return result_func(*args)

        return high_order_partial_derivative_func
    else:
        raise ValueError("Invalid var type")


def curry(func: MultiVarsFunc, *args: Var) -> OneVarFunc:
    """
    对多参数函数进行柯里化。
    > [!tip]
    > 有关函数柯里化，可参考[函数式编程--柯理化（Currying）](https://zhuanlan.zhihu.com/p/355859667)
    Args:
        func: 函数
        *args: 参数
    Returns:
        柯里化后的函数
    Examples:
        ```python
        def add(a: int, b: int, c: int) -> int:
            return a + b + c
        add_curried = curry(add, 1, 2)
        add_curried(3)  # 6
        ```
    """

    def curried_func(*args2: Var) -> Var:
        """@litedoc-hide"""
        return func(*args, *args2)

    return curried_func


def test_kwargs(*args, **kwargs):
    """
    测试kwargs
    Args:
        *args:
        **kwargs:
    """
    print(args)
    print(kwargs)
