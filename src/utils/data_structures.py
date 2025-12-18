"""
Модуль для структур данных, которые заменяют примитивные типы
для представления игровых понятий.
"""

from dataclasses import dataclass
from enum import Enum
from src.consts import HeartsTypes


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


# одержимость простыми типами
class Health:
    """
    Класс для представления здоровья персонажа.
    Заменяет использование примитивных чисел для здоровья.
    """
    def __init__(self, max_red_hp: int = 6):
        self.max_red_hp = max_red_hp
        self.red_hp = max_red_hp  # кол-во красных хп (половинки сердца)
        self.blue_hp = 0  # аналогично красным, только синие
        self.black_hp = 0  # аналогично красным, только чёрные

    def get_total_hp(self) -> int:
        """Возвращает общее количество здоровья (в половинках сердец)."""
        return self.red_hp + self.blue_hp + self.black_hp

    def get_hp_by_type(self, heart_type: HeartsTypes) -> int:
        """Возвращает количество здоровья определенного типа."""
        if heart_type == HeartsTypes.RED:
            return self.red_hp
        elif heart_type == HeartsTypes.BLUE:
            return self.blue_hp
        elif heart_type == HeartsTypes.BLACK:
            return self.black_hp
        return 0

    def add_health(self, heart_type: HeartsTypes, amount: int) -> None:
        """Добавляет здоровье определенного типа."""
        if heart_type == HeartsTypes.RED:
            self.red_hp = max(0, self.red_hp + amount)
        elif heart_type == HeartsTypes.BLUE:
            self.blue_hp = max(0, self.blue_hp + amount)
        elif heart_type == HeartsTypes.BLACK:
            self.black_hp = max(0, self.black_hp + amount)

    def subtract_health(self, damage: int) -> None:
        """Вычитает урон из здоровья согласно приоритету: синие -> черные -> красные."""
        remaining_damage = damage

        # Сначала вычитаем из синих сердец
        if remaining_damage > 0 and self.blue_hp > 0:
            old_blue_hp = self.blue_hp
            self.blue_hp = max(0, self.blue_hp - remaining_damage)
            remaining_damage -= (old_blue_hp - self.blue_hp)

        # Потом из черных сердец
        if remaining_damage > 0 and self.black_hp > 0:
            old_black_hp = self.black_hp
            self.black_hp = max(0, self.black_hp - remaining_damage)
            remaining_damage -= (old_black_hp - self.black_hp)

        # Наконец из красных сердец
        if remaining_damage > 0:
            self.red_hp = max(0, self.red_hp - remaining_damage)

    def is_alive(self) -> bool:
        """Проверяет, жив ли персонаж (осталось ли красное здоровье)."""
        return self.red_hp > 0

    def is_full_red_health(self) -> bool:
        """Проверяет, полностью ли заполнено красное здоровье."""
        return self.red_hp >= self.max_red_hp
