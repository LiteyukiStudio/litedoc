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

RealNumber: TypeAlias = int | float
Number: TypeAlias = RealNumber | complex
SingleVar = TypeVar("SingleVar", bound=Number)
ArrayVar = TypeVar("ArrayVar", bound=Iterable[Number])
Var: TypeAlias = SingleVar | ArrayVar

OneSingleVarFunc: TypeAlias = Callable[[SingleVar], SingleVar]
OneArrayFunc: TypeAlias = Callable[[ArrayVar], ArrayVar]
OneVarFunc: TypeAlias = OneSingleVarFunc | OneArrayFunc

TwoSingleVarsFunc: TypeAlias = Callable[[SingleVar, SingleVar], SingleVar]
TwoArraysFunc: TypeAlias = Callable[[ArrayVar, ArrayVar], ArrayVar]
TwoVarsFunc: TypeAlias = TwoSingleVarsFunc | TwoArraysFunc

ThreeSingleVarsFunc: TypeAlias = Callable[[SingleVar, SingleVar, SingleVar], SingleVar]
ThreeArraysFunc: TypeAlias = Callable[[ArrayVar, ArrayVar, ArrayVar], ArrayVar]
ThreeVarsFunc: TypeAlias = ThreeSingleVarsFunc | ThreeArraysFunc

MultiSingleVarsFunc: TypeAlias = Callable[..., SingleVar]
MultiArraysFunc: TypeAlias = Callable[..., ArrayVar]
MultiVarsFunc: TypeAlias = MultiSingleVarsFunc | MultiArraysFunc
