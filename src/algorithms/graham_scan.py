"""
Graham Scan algoritması - Convex Hull
Karmaşıklık: O(n log n)
"""

from typing import List
from src.point import Point, cross


def graham_scan(points: List[Point]) -> List[Point]:
    """
    Graham Scan algoritması ile convex hull hesaplama
    
    Args:
        points: Nokta listesi (en az 3 nokta)
    
    Returns:
        Convex hull noktaları (saat yönünün tersi, son nokta ilk noktayı tekrar etmez)
    """
    n = len(points)
    if n < 3:
        return points
    
    # En küçük y'li noktayı bul (y eşitse en küçük x'li)
    start = min(points, key=lambda p: (p.y, p.x))
    
    # Start noktasına göre polar açıya göre sırala
    def polar_angle(p: Point) -> float:
        return math.atan2(p.y - start.y, p.x - start.x)
    
    import math
    
    # Start hariç diğer noktaları sırala
    sorted_points = sorted([p for p in points if p != start], 
                          key=lambda p: (polar_angle(p), start.distance_to(p)))
    
    # Aynı açıdaki noktalardan sadece en uzak olanı tut
    filtered = []
    for p in sorted_points:
        if not filtered:
            filtered.append(p)
        else:
            # Aynı açıda mı kontrol et
            if math.isclose(polar_angle(p), polar_angle(filtered[-1]), abs_tol=1e-9):
                # Daha uzaksa değiştir
                if start.distance_to(p) > start.distance_to(filtered[-1]):
                    filtered[-1] = p
            else:
                filtered.append(p)
    
    if len(filtered) < 2:
        return [start] + filtered
    
    # Stack başlat
    hull = [start, filtered[0], filtered[1]]
    
    # Graham Scan
    for i in range(2, len(filtered)):
        while len(hull) > 1 and cross(hull[-2], hull[-1], filtered[i]) <= 0:
            hull.pop()
        hull.append(filtered[i])
    
    return hull


def convex_area(hull: List[Point]) -> float:
    """Convex hull alanını hesapla (Shoelace formülü)"""
    n = len(hull)
    if n < 3:
        return 0.0
    
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += hull[i].x * hull[j].y
        area -= hull[j].x * hull[i].y
    
    return abs(area) / 2.0


def is_convex_set(points: List[Point]) -> bool:
    """
    Tüm noktalar convex hull üzerinde mi kontrol et
    (Yani tüm noktalar hull'in içinde veya üzerinde mi?)
    """
    if len(points) < 3:
        return True
    
    hull = graham_scan(points)
    hull_set = set(hull)
    
    # Tüm noktalar hull'da mı?
    return len(points) == len(hull_set)