import math
from typing import overload, TYPE_CHECKING

import numpy as np

from .const import APPROX
from .mp_math_typing import RealNumber
from .point import Point3
from .angle import AnyAngle
from .utils import approx

# if TYPE_CHECKING:
#


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        """
        3维向量
        Args:
            x: x轴分量
            y: y轴分量
            z: z轴分量
        """
        self.x = x
        self.y = y
        self.z = z

    def approx(self, other: 'Vector3', epsilon: float = APPROX) -> bool:
        """
        判断两个向量是否近似相等。
        Args:
            other:
            epsilon:

        Returns:
            是否近似相等
        """
        return all([abs(self.x - other.x) < epsilon, abs(self.y - other.y) < epsilon, abs(self.z - other.z) < epsilon])

    def cal_angle(self, other: 'Vector3') -> 'AnyAngle':
        """
        计算两个向量之间的夹角。
        Args:
            other: 另一个向量
        Returns:
            夹角
        """
        return AnyAngle(math.acos(self @ other / (self.length * other.length)), is_radian=True)

    def cross(self, other: 'Vector3') -> 'Vector3':
        """
        向量积 叉乘：v1 cross v2 -> v3

        叉乘为0，则两向量平行。
        其余结果的模为平行四边形的面积。

        返回如下行列式的结果：

        ``i  j  k``

        ``x1 y1 z1``

        ``x2 y2 z2``

        Args:
            other:
        Returns:
            行列式的结果
        """
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def is_approx_parallel(self, other: 'Vector3', epsilon: float = APPROX) -> bool:
        """
        判断两个向量是否近似平行。
        Args:
            other: 另一个向量
            epsilon: 允许的误差
        Returns:
            是否近似平行
        """
        return self.cross(other).length < epsilon

    def is_parallel(self, other: 'Vector3') -> bool:
        """
        判断两个向量是否平行。
        Args:
            other: 另一个向量
        Returns:
            是否平行
        """
        return self.cross(other).approx(zero_vector3)

    def normalize(self):
        """
        将向量归一化。

        自体归一化，不返回值。
        """
        length = self.length
        self.x /= length
        self.y /= length
        self.z /= length

    @property
    def np_array(self) -> 'np.ndarray':
        """
        返回numpy数组
        Returns:
        """

        return np.array([self.x, self.y, self.z])

    @property
    def length(self) -> float:
        """
        向量的模。
        Returns:
            模
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def unit(self) -> 'Vector3':
        """
        获取该向量的单位向量。
        Returns:
            单位向量
        """
        return self / self.length

    def __abs__(self):
        return self.length

    @overload
    def __add__(self, other: 'Vector3') -> 'Vector3':
        ...

    @overload
    def __add__(self, other: 'Point3') -> 'Point3':
        ...

    def __add__(self, other):
        """
        V + P -> P\n
        V + V -> V
        Args:
            other:
        Returns:

        """
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Point3):
            return Point3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Vector3' and '{type(other)}'")

    def __eq__(self, other):
        """
        判断两个向量是否相等。
        Args:
            other:
        Returns:
            是否相等
        """
        return approx(self.x, other.x) and approx(self.y, other.y) and approx(self.z, other.z)

    def __radd__(self, other: 'Point3') -> 'Point3':
        """
        P + V -> P\n
        别去点那边实现了。
        :param other:
        :return:
        """
        return Point3(self.x + other.x, self.y + other.y, self.z + other.z)

    @overload
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        ...

    @overload
    def __sub__(self, other: 'Point3') -> "Point3":
        ...

    def __sub__(self, other):
        """
        V - P -> P\n
        V - V -> V
        Args:
            other:
        Returns:
        """
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, Point3):
            return Point3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"unsupported operand type(s) for -: \"Vector3\" and \"{type(other)}\"")

    def __rsub__(self, other: 'Point3'):
        """
        P - V -> P
        Args:
            other:
        Returns:

        """

        if isinstance(other, Point3):
            return Point3(other.x - self.x, other.y - self.y, other.z - self.z)
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{type(other)}' and 'Vector3'")

    @overload
    def __mul__(self, other: 'Vector3') -> 'Vector3':
        ...

    @overload
    def __mul__(self, other: RealNumber) -> 'Vector3':
        ...

    def __mul__(self, other: 'int | float | Vector3') -> 'Vector3':
        """
        数组运算 非点乘。点乘使用@，叉乘使用cross。
        Args:
            other:

        Returns:
        """

        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (float, int)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Vector3' and '{type(other)}'")

    def __rmul__(self, other: 'RealNumber') -> 'Vector3':
        return self.__mul__(other)

    def __matmul__(self, other: 'Vector3') -> 'RealNumber':
        """
        点乘。
        Args:
            other:
        Returns:
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, other: RealNumber) -> 'Vector3':
        return Vector3(self.x / other, self.y / other, self.z / other)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"


zero_vector3: Vector3 = Vector3(0, 0, 0)
"""零向量"""
x_axis: Vector3 = Vector3(1, 0, 0)
"""x轴单位向量"""
y_axis: Vector3 = Vector3(0, 1, 0)
"""y轴单位向量"""
z_axis: Vector3 = Vector3(0, 0, 1)
"""z轴单位向量"""
