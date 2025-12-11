"""
Модуль для структур данных, которые заменяют примитивные типы
для представления игровых понятий.
"""

from dataclasses import dataclass
from enum import Enum


# одержимость простыми типами
@dataclass
class Vector2:
    """
    Класс для представления двумерного вектора (координат).
    Заменяет использование кортежей (x, y) для лучшей читаемости и типобезопасности.
    """
    x: int
    y: int

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(int(self.x * scalar), int(self.y * scalar))

    def to_tuple(self) -> tuple[int, int]:
        """Преобразует вектор в кортеж (x, y)."""
        return (self.x, self.y)


# одержимость простыми типами
class Direction(Enum):
    """
    Перечисление направлений движения.
    Заменяет использование кортежей в Moves.
    """
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)
    TOPLEFT = Vector2(-1, -1)
    TOPRIGHT = Vector2(1, -1)
    BOTTOMRIGHT = Vector2(1, 1)
    BOTTOMLEFT = Vector2(-1, 1)


# одержимость простыми типами
class HeartAmount(Enum):
    """
    Перечисление количества сердец.
    Заменяет использование примитивных чисел в PickHeart.
    """
    HALF = 1  # Половинка сердца
    FULL = 2  # Полное сердце
    DOUBLE = 4  # Два полных сердца (редко)

    @staticmethod
    def from_int(value: int) -> 'HeartAmount':
        """
        Преобразует целое число в ближайший HeartAmount.
        """
        for heart_amount in HeartAmount:
            if heart_amount.value == value:
                return heart_amount
        # Если точного соответствия нет, возвращаем ближайшее значение
        if value <= 1:
            return HeartAmount.HALF
        elif value <= 2:
            return HeartAmount.FULL
        else:
            return HeartAmount.DOUBLE
