from typing import TYPE_CHECKING, overload

from .const import APPROX
from .utils import approx

if TYPE_CHECKING:
    from .vector import Vector3  # type: ignore


class Point3:
    def __init__(self, x: float, y: float, z: float):
        """
        笛卡尔坐标系中的点。
        Args:
            x: x 坐标
            y: y 坐标
            z: z 坐标
        """
        self.x = x
        self.y = y
        self.z = z

    def approx(self, other: "Point3", epsilon: float = APPROX) -> bool:
        """
        判断两个点是否近似相等。
        Args:
            other:
            epsilon:

        Returns:
            是否近似相等
        """
        return all([abs(self.x - other.x) < epsilon, abs(self.y - other.y) < epsilon, abs(self.z - other.z) < epsilon])

    def __str__(self):
        return f"Point3({self.x}, {self.y}, {self.z})"

    @overload
    def __add__(self, other: "Vector3") -> "Point3":
        ...

    @overload
    def __add__(self, other: "Point3") -> "Point3":
        ...

    def __add__(self, other):
        """
        P + V -> P
        P + P -> P
        Args:
            other:
        Returns:
        """
        return Point3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        """
        判断两个点是否相等。
        Args:
            other:
        Returns:
        """
        return approx(self.x, other.x) and approx(self.y, other.y) and approx(self.z, other.z)

    def __sub__(self, other: "Point3") -> "Vector3":
        """
        P - P -> V

        P - V -> P  已在 :class:`Vector3` 中实现
        Args:
            other:
        Returns:

        """
        from .vector import Vector3
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
