"""
Örnek veri üretme aracı
"""

import json
import random
from src.point import Point


def generate_convex_points(count: int, filename: str) -> None:
    """Convex bir nokta seti üret (daire üzerinde)"""
    import math
    
    points = []
    for i in range(count):
        angle = 2 * math.pi * i / count
        x = 50 + 40 * math.cos(angle)
        y = 50 + 40 * math.sin(angle)
        points.append({'x': round(x, 2), 'y': round(y, 2)})
    
    with open(filename, 'w') as f:
        json.dump({'points': points}, f, indent=2)
    
    print(f"✅ Convex veri üretildi: {filename}")


def generate_random_points(count: int, filename: str, max_val: float = 100.0) -> None:
    """Rastgele nokta seti üret"""
    random.seed(42)
    points = []
    for _ in range(count):
        points.append({
            'x': round(random.uniform(0, max_val), 2),
            'y': round(random.uniform(0, max_val), 2)
        })
    
    with open(filename, 'w') as f:
        json.dump({'points': points}, f, indent=2)
    
    print(f"✅ Rastgele veri üretildi: {filename}")


if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    
    # Örnek veriler
    generate_convex_points(20, 'data/convex_20.json')
    generate_random_points(100, 'data/random_100.json')
    generate_random_points(1000, 'data/random_1000.json')
    generate_random_points(10000, 'data/random_10000.json')