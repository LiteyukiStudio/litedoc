# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/7 上午12:42
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : segment.py
@Software: PyCharm
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .point import Point3  # type: ignore
    from .vector import Vector3  # type: ignore


class Segment3:
    def __init__(self, p1: "Point3", p2: "Point3"):
        """
        三维空间中的线段。
        :param p1:
        :param p2:
        """
        self.p1 = p1
        self.p2 = p2

        """方向向量"""
        self.direction = self.p2 - self.p1
        """长度"""
        self.length = self.direction.length
        """中心点"""
        self.midpoint = Point3((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2, (self.p1.z + self.p2.z) / 2)

    def __repr__(self):
        return f"Segment3({self.p1}, {self.p2})"

    def __str__(self):
        return f"Segment3({self.p1} -> {self.p2})"
