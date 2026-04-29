"""
Thread yöneticisi - Paralel convex hull hesaplama
"""

import concurrent.futures
import math
from typing import List, Callable
from src.point import Point
from src.algorithms.graham_scan import graham_scan


class ParallelConvexHull:
    """
    ThreadPoolExecutor kullanarak paralel convex hull hesaplama
    
    Strateji:
    1. Noktaları bölgelere böl
    2. Her bölge için ayrı thread'de convex hull hesapla
    3. Partial hull'ları birleştir
    """
    
    def __init__(self, num_threads: int = 4):
        self.num_threads = num_threads
    
    def _partition_points(self, points: List[Point], num_partitions: int) -> List[List[Point]]:
        """Noktaları x koordinatına göre bölgelere ayır"""
        if not points:
            return []
        
        sorted_points = sorted(points, key=lambda p: p.x)
        n = len(sorted_points)
        partition_size = math.ceil(n / num_partitions)
        
        partitions = []
        for i in range(0, n, partition_size):
            partitions.append(sorted_points[i:i + partition_size])
        
        return partitions
    
    def _merge_hulls(self, hull1: List[Point], hull2: List[Point]) -> List[Point]:
        """İki convex hull'ı birleştir"""
        # İki hull'ın tüm noktalarını birleştir ve yeniden hesapla
        combined = list(set(hull1 + hull2))
        return graham_scan(combined)
    
    def compute_parallel(self, points: List[Point]) -> List[Point]:
        """
        Paralel olarak convex hull hesapla
        
        Args:
            points: Nokta listesi
        
        Returns:
            Convex hull noktaları
        """
        if len(points) < 100:  # Küçük setlerde paralelleştirme overhead'ı yüksek
            return graham_scan(points)
        
        # Noktaları böl
        partitions = self._partition_points(points, self.num_threads)
        
        # Her bölge için paralel hull hesapla
        partial_hulls = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_partition = {
                executor.submit(graham_scan, partition): i 
                for i, partition in enumerate(partitions)
            }
            
            for future in concurrent.futures.as_completed(future_to_partition):
                try:
                    hull = future.result()
                    partial_hulls.append(hull)
                except Exception as e:
                    print(f"Bölge {future_to_partition[future]} hatası: {e}")
        
        # Partial hull'ları birleştir
        if not partial_hulls:
            return []
        
        final_hull = partial_hulls[0]
        for hull in partial_hulls[1:]:
            final_hull = self._merge_hulls(final_hull, hull)
        
        return final_hull
    
    def benchmark(self, points: List[Point]) -> dict:
        """
        Seri ve paralel performans karşılaştırması
        
        Returns:
            {'serial_time': float, 'parallel_time': float, 'speedup': float}
        """
        import time
        
        # Seri hesaplama
        start = time.time()
        serial_result = graham_scan(points)
        serial_time = time.time() - start
        
        # Paralel hesaplama
        start = time.time()
        parallel_result = self.compute_parallel(points)
        parallel_time = time.time() - start
        
        # Doğruluk kontrolü
        serial_set = set((p.x, p.y) for p in serial_result)
        parallel_set = set((p.x, p.y) for p in parallel_result)
        is_correct = serial_set == parallel_set
        
        return {
            'serial_time': serial_time,
            'parallel_time': parallel_time,
            'speedup': serial_time / parallel_time if parallel_time > 0 else 0,
            'is_correct': is_correct,
            'serial_hull_size': len(serial_result),
            'parallel_hull_size': len(parallel_result)
        }
