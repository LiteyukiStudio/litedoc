from abc import abstractmethod


def custom_decorator(func):
    def wrapper(*args, **kwargs):
        print("decorator")
        return func(*args, **kwargs)
    return wrapper

class B:
    ...


class A(B):
    """
    A class
    """

    def __init__(self):
        """
        A class constructor
        """
        self.a = 1
        self.a_prop: str = ""
        """类属性注解测试"""

    def a_method(self, arg1: int, arg2: str = ""):
        """
        A class method
        """
        print(arg1, arg2, self.a)

    @property
    def a_p(self) -> int:
        return self.a

    @classmethod
    def c_method(cls):
        print(cls)

    @staticmethod
    def s_method():
        print("static")

    @abstractmethod
    def abs_method(self):
        pass

    @custom_decorator
    def custom_method(self):
        print("custom")

def b_method(a, b=2, c=3):
    print(a)

async def async_func():
    print("async")

# 单行注释
CONST = 3
"""变量注解测试"""
