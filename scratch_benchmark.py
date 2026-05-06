import random
import time
from src.point import Point
from src.thread_manager import ParallelConvexHull

def run_benchmarks():
    point_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]
    threads = [2, 4, 8]
    
    print("Point Count Benchmarks (Threads = 4)")
    print("-" * 50)
    for count in point_counts:
        points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(count)]
        pch = ParallelConvexHull(num_threads=4)
        bench = pch.benchmark(points)
        print(f"Points: {count:6d} | Serial: {bench['serial_time']:.4f}s | Parallel: {bench['parallel_time']:.4f}s | Speedup: {bench['speedup']:.2f}x")
        
    print("\nThread Count Benchmarks (Points = 50000)")
    print("-" * 50)
    points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(50000)]
    for t in threads:
        pch = ParallelConvexHull(num_threads=t)
        bench = pch.benchmark(points)
        print(f"Threads: {t} | Serial: {bench['serial_time']:.4f}s | Parallel: {bench['parallel_time']:.4f}s | Speedup: {bench['speedup']:.2f}x")

if __name__ == "__main__":
    run_benchmarks()
