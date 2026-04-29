"""
Ana convex checker modülü
"""

import json
from typing import List, Optional
from src.point import Point
from src.algorithms.graham_scan import graham_scan, is_convex_set
from src.thread_manager import ParallelConvexHull


class ConvexChecker:
    """
    Convex hull kontrol sınıfı
    
    Özellikler:
    - Nokta setinin convex olup olmadığını kontrol etme
    - Convex hull hesaplama (seri/paralel)
    - JSON import/export
    """
    
    def __init__(self, use_parallel: bool = False, num_threads: int = 4):
        self.use_parallel = use_parallel
        self.num_threads = num_threads
        self.points: List[Point] = []
        self.hull: List[Point] = []
    
    def load_from_json(self, filepath: str) -> None:
        """JSON dosyasından noktaları yükle"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.points = [Point.from_dict(p) for p in data['points']]
    
    def save_to_json(self, filepath: str) -> None:
        """Noktaları ve hull'u JSON olarak kaydet"""
        data = {
            'points': [p.to_dict() for p in self.points],
            'hull': [p.to_dict() for p in self.hull],
            'is_convex': self.is_convex(),
            'point_count': len(self.points),
            'hull_point_count': len(self.hull)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def set_points(self, points: List[Point]) -> None:
        self.points = points
    
    def compute_hull(self) -> List[Point]:
        """Convex hull hesapla"""
        if not self.points:
            return []
        
        if self.use_parallel and len(self.points) >= 100:
            pch = ParallelConvexHull(num_threads=self.num_threads)
            self.hull = pch.compute_parallel(self.points)
        else:
            self.hull = graham_scan(self.points)
        
        return self.hull
    
    def is_convex(self) -> bool:
        """Tüm noktalar convex hull üzerinde mi?"""
        if not self.hull:
            self.compute_hull()
        
        hull_set = set(self.hull)
        points_set = set(self.points)
        
        return points_set == hull_set
    
    def get_statistics(self) -> dict:
        """İstatistikler"""
        if not self.hull:
            self.compute_hull()
        
        return {
            'total_points': len(self.points),
            'hull_points': len(self.hull),
            'interior_points': len(self.points) - len(self.hull),
            'is_convex': self.is_convex(),
            'parallel_used': self.use_parallel and len(self.points) >= 100
        }