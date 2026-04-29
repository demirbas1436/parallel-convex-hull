import pytest
import random
from src.point import Point
from src.thread_manager import ParallelConvexHull
from src.algorithms.graham_scan import graham_scan


class TestParallelConvexHull:
    def test_small_set_falls_back_to_serial(self):
        points = [Point(0, 0), Point(1, 0), Point(0.5, 1)]
        pch = ParallelConvexHull(num_threads=4)
        result = pch.compute_parallel(points)
        assert len(result) == 3
    
    def test_large_set_correctness(self):
        # Rastgele noktalar üret
        random.seed(42)
        points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(1000)]
        
        pch = ParallelConvexHull(num_threads=4)
        parallel_result = pch.compute_parallel(points)
        serial_result = graham_scan(points)
        
        # Sonuçlar aynı olmalı
        parallel_set = set((p.x, p.y) for p in parallel_result)
        serial_set = set((p.x, p.y) for p in serial_result)
        assert parallel_set == serial_set
    
    def test_benchmark(self):
        random.seed(42)
        points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(500)]
        
        pch = ParallelConvexHull(num_threads=4)
        result = pch.benchmark(points)
        
        assert result['is_correct'] == True
        assert 'serial_time' in result
        assert 'parallel_time' in result