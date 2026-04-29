"""
Point sınıfı - 2D geometrik nokta işlemleri
"""

import math
from typing import List, Tuple


class Point:
    """2D nokta temsili"""
    
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
    
    def __hash__(self):
        return hash((round(self.x, 10), round(self.y, 10)))
    
    def __lt__(self, other):
        """Sıralama için: önce x, sonra y"""
        if not isinstance(other, Point):
            return NotImplemented
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
    
    def distance_to(self, other: 'Point') -> float:
        """İki nokta arası Euclidean mesafe"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def cross_product(self, other: 'Point') -> float:
        """2D cross product (self × other)"""
        return self.x * other.y - self.y * other.x
    
    @staticmethod
    def orientation(p1: 'Point', p2: 'Point', p3: 'Point') -> int:
        """
        Üç noktanın yönünü belirler
        Returns:
            0 -> doğrusal (collinear)
            1 -> saat yönünde (clockwise)
            2 -> saat yönünün tersi (counter-clockwise)
        """
        val = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        
        if math.isclose(val, 0, abs_tol=1e-9):
            return 0
        elif val > 0:
            return 1  # Clockwise
        else:
            return 2  # Counter-clockwise
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    @classmethod
    def from_tuple(cls, t: Tuple[float, float]) -> 'Point':
        return cls(t[0], t[1])
    
    @classmethod
    def from_dict(cls, d: dict) -> 'Point':
        return cls(d['x'], d['y'])
    
    def to_dict(self) -> dict:
        return {'x': self.x, 'y': self.y}


def cross(o: Point, a: Point, b: Point) -> float:
    """Cross product of vectors OA and OB"""
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
