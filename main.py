#!/usr/bin/env python3
"""
Ana çalıştırma dosyası
"""

import argparse
import json
import random
import time
from typing import List
from src.point import Point
from src.convex_checker import ConvexChecker
from visualization.plotter import plot_convex_hull


def generate_random_points(count: int, max_val: float = 100.0) -> List[Point]:
    """Rastgele nokta üret"""
    return [Point(random.uniform(0, max_val), random.uniform(0, max_val)) 
            for _ in range(count)]


def main():
    parser = argparse.ArgumentParser(description='Paralel Convex Hull Hesaplama')
    parser.add_argument('--input', '-i', help='Girdi JSON dosyası')
    parser.add_argument('--output', '-o', default='output.json', help='Çıktı JSON dosyası')
    parser.add_argument('--points', '-p', type=int, help='Rastgele nokta sayısı')
    parser.add_argument('--threads', '-t', type=int, default=4, help='Thread sayısı')
    parser.add_argument('--parallel', action='store_true', help='Paralel mod')
    parser.add_argument('--visualize', '-v', action='store_true', help='Görselleştir')
    parser.add_argument('--benchmark', '-b', action='store_true', help='Benchmark yap')
    
    args = parser.parse_args()
    
    checker = ConvexChecker(use_parallel=args.parallel, num_threads=args.threads)
    
    # Noktaları yükle veya üret
    if args.input:
        print(f"📂 Dosya yükleniyor: {args.input}")
        checker.load_from_json(args.input)
    elif args.points:
        print(f"🎲 {args.points} adet rastgele nokta üretiliyor...")
        points = generate_random_points(args.points)
        checker.set_points(points)
    else:
        # Demo verisi
        print("📊 Demo verisi kullanılıyor...")
        checker.set_points([
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
            Point(1, 0.5), Point(0.5, 1), Point(1.5, 1.5)
        ])
    
    # Hesaplama
    print(f"\n🔢 Toplam nokta sayısı: {len(checker.points)}")
    print(f"⚙️  Mod: {'Paralel' if args.parallel else 'Seri'} (Thread: {args.threads})")
    
    start_time = time.time()
    hull = checker.compute_hull()
    elapsed = time.time() - start_time
    
    # Sonuçlar
    print(f"\n✅ Hesaplama tamamlandı!")
    print(f"⏱️  Süre: {elapsed:.4f} saniye")
    print(f"📐 Hull nokta sayısı: {len(hull)}")
    print(f"🔍 Convex mi?: {'Evet' if checker.is_convex() else 'Hayır'}")
    
    # İstatistikler
    stats = checker.get_statistics()
    print(f"\n📊 İstatistikler:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Kaydet
    checker.save_to_json(args.output)
    print(f"\n💾 Sonuçlar kaydedildi: {args.output}")
    
    # Benchmark
    if args.benchmark and args.parallel:
        print("\n🏁 Benchmark başlatılıyor...")
        from src.thread_manager import ParallelConvexHull
        pch = ParallelConvexHull(num_threads=args.threads)
        bench = pch.benchmark(checker.points)
        
        print(f"\n📈 Benchmark Sonuçları:")
        print(f"   Seri süre: {bench['serial_time']:.4f}s")
        print(f"   Paralel süre: {bench['parallel_time']:.4f}s")
        print(f"   Hızlanma: {bench['speedup']:.2f}x")
        print(f"   Doğruluk: {'✅' if bench['is_correct'] else '❌'}")
    
    # Görselleştirme
    if args.visualize:
        print("\n📈 Görselleştirme oluşturuluyor...")
        plot_convex_hull(checker.points, hull, save_path='convex_hull.png')
        print("🖼️  convex_hull.png kaydedildi")


if __name__ == '__main__':
    main()