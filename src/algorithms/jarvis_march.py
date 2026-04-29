"""
Jarvis March (Gift Wrapping) algoritması
Karmaşıklık: O(nh) - h = hull üzerindeki nokta sayısı
"""

from typing import List
from src.point import Point


def jarvis_march(points: List[Point]) -> List[Point]:
    """
    Jarvis March algoritması ile convex hull
    
    Args:
        points: Nokta listesi
    
    Returns:
        Convex hull noktaları
    """
    n = len(points)
    if n < 3:
        return points
    
    # En sol noktayı bul
    start = min(points, key=lambda p: (p.x, p.y))
    
    hull = []
    current = start
    
    while True:
        hull.append(current)
        
        # Sonraki noktayı bul
        next_point = points[0]
        for p in points[1:]:
            if p == current:
                continue
            
            # Orientation kontrolü
            orient = Point.orientation(current, next_point, p)
            
            if next_point == current:
                next_point = p
            elif orient == 2:  # counter-clockwise
                next_point = p
            elif orient == 0:  # collinear - daha uzak olanı seç
                if current.distance_to(p) > current.distance_to(next_point):
                    next_point = p
        
        current = next_point
        
        if current == start:
            break
    
    return hull
