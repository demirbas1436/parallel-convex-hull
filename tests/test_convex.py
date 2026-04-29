import pytest
from src.point import Point
from src.convex_checker import ConvexChecker


class TestConvexChecker:
    def test_convex_square(self):
        checker = ConvexChecker()
        checker.set_points([
            Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)
        ])
        assert checker.is_convex() == True
        assert len(checker.hull) == 4
    
    def test_non_convex_with_interior(self):
        checker = ConvexChecker()
        checker.set_points([
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
            Point(1, 1)  # İç nokta
        ])
        assert checker.is_convex() == False
        assert len(checker.hull) == 4
    
    def test_json_roundtrip(self, tmp_path):
        checker = ConvexChecker()
        checker.set_points([Point(1, 2), Point(3, 4)])
        
        filepath = tmp_path / "test.json"
        checker.save_to_json(str(filepath))
        
        checker2 = ConvexChecker()
        checker2.load_from_json(str(filepath))
        
        assert len(checker2.points) == 2
        assert checker2.points[0].x == 1
    
    def test_parallel_mode(self):
        import random
        random.seed(42)
        points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(200)]
        
        checker = ConvexChecker(use_parallel=True, num_threads=4)
        checker.set_points(points)
        hull = checker.compute_hull()
        
        assert len(hull) >= 3
    
    def test_statistics(self):
        checker = ConvexChecker()
        checker.set_points([
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
            Point(1, 1)
        ])
        stats = checker.get_statistics()
        
        assert stats['total_points'] == 5
        assert stats['hull_points'] == 4
        assert stats['is_convex'] == False