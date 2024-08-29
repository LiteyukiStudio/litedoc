# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/9 上午11:35
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : mp_math_typing.py
@Software: PyCharm
"""
from typing import Callable, Iterable, TypeAlias, TypeVar

RealNumber: TypeAlias = int | float  # 实数@litedoc-hide
Number: TypeAlias = RealNumber | complex  # 数
SingleVar = TypeVar("SingleVar", bound=Number)  # 单变量
ArrayVar = TypeVar("ArrayVar", bound=Iterable[Number])  # 数组变量
Var: TypeAlias = SingleVar | ArrayVar  # 变量

OneSingleVarFunc: TypeAlias = Callable[[SingleVar], SingleVar]  # 一元单变量函数
OneArrayFunc: TypeAlias = Callable[[ArrayVar], ArrayVar]  # 一元数组函数
OneVarFunc: TypeAlias = OneSingleVarFunc | OneArrayFunc  # 一元函数

TwoSingleVarsFunc: TypeAlias = Callable[[SingleVar, SingleVar], SingleVar]  # 二元单变量函数
TwoArraysFunc: TypeAlias = Callable[[ArrayVar, ArrayVar], ArrayVar]  # 二元数组函数
TwoVarsFunc: TypeAlias = TwoSingleVarsFunc | TwoArraysFunc  # 二元函数

ThreeSingleVarsFunc: TypeAlias = Callable[[SingleVar, SingleVar, SingleVar], SingleVar]  # 三元单变量函数
ThreeArraysFunc: TypeAlias = Callable[[ArrayVar, ArrayVar, ArrayVar], ArrayVar]  # 三元数组函数
ThreeVarsFunc: TypeAlias = ThreeSingleVarsFunc | ThreeArraysFunc  # 三元函数

MultiSingleVarsFunc: TypeAlias = Callable[..., SingleVar]  # 多元单变量函数
MultiArraysFunc: TypeAlias = Callable[..., ArrayVar]  # 多元数组函数
MultiVarsFunc: TypeAlias = MultiSingleVarsFunc | MultiArraysFunc  # 多元函数
