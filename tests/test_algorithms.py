import pytest
from src.point import Point
from src.algorithms.graham_scan import graham_scan, is_convex_set
from src.algorithms.jarvis_march import jarvis_march


class TestGrahamScan:
    def test_simple_triangle(self):
        points = [Point(0, 0), Point(1, 0), Point(0.5, 1)]
        hull = graham_scan(points)
        assert len(hull) == 3
    
    def test_square(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        hull = graham_scan(points)
        assert len(hull) == 4
    
    def test_with_interior_points(self):
        points = [
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),  # Kare köşeleri
            Point(1, 1), Point(0.5, 0.5), Point(1.5, 1.5)  # İç noktalar
        ]
        hull = graham_scan(points)
        assert len(hull) == 4  # Sadece köşeler
    
    def test_collinear_points(self):
        points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
        hull = graham_scan(points)
        assert len(hull) == 2  # Sadece uç noktalar


class TestConvexSet:
    def test_convex_set(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        assert is_convex_set(points) == True
    
    def test_non_convex_set(self):
        points = [Point(0, 0), Point(2, 0), Point(2, 2), Point(1, 1), Point(0, 2)]
        assert is_convex_set(points) == False


class TestJarvisMarch:
    def test_square(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        hull = jarvis_march(points)
        assert len(hull) == 4