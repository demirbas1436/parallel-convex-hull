"""
Matplotlib ile convex hull görselleştirme
"""

import matplotlib
matplotlib.use('Agg')  # Headless ortam için

import matplotlib.pyplot as plt
from typing import List, Optional
from src.point import Point


def plot_convex_hull(points: List[Point], hull: List[Point], 
                     save_path: Optional[str] = None,
                     title: str = "Convex Hull") -> None:
    """
    Noktaları ve convex hull'u çiz
    
    Args:
        points: Tüm noktalar
        hull: Convex hull noktaları
        save_path: Kaydetme yolu (None ise göster)
        title: Grafik başlığı
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Tüm noktaları çiz (iç noktalar)
    hull_set = set(hull)
    interior_points = [p for p in points if p not in hull_set]
    
    if interior_points:
        ax.scatter([p.x for p in interior_points], 
                  [p.y for p in interior_points],
                  c='lightblue', s=50, alpha=0.6, label='İç Noktalar', zorder=2)
    
    # Hull noktalarını çiz
    if hull:
        ax.scatter([p.x for p in hull], 
                  [p.y for p in hull],
                  c='red', s=100, marker='o', label='Hull Noktaları', zorder=3)
        
        # Hull çizgileri
        hull_closed = hull + [hull[0]]  # Kapalı şekil
        ax.plot([p.x for p in hull_closed], 
               [p.y for p in hull_closed],
               'r-', linewidth=2, label='Convex Hull', zorder=1)
    
    ax.set_xlabel('X Koordinatı')
    ax.set_ylabel('Y Koordinatı')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"📊 Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_benchmark_comparison(results: dict, save_path: str = 'benchmark.png') -> None:
    """Benchmark sonuçlarını karşılaştırmalı çiz"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Süre karşılaştırması
    labels = ['Seri', 'Paralel']
    times = [results['serial_time'], results['parallel_time']]
    colors = ['#3498db', '#e74c3c']
    
    ax1.bar(labels, times, color=colors)
    ax1.set_ylabel('Süre (saniye)')
    ax1.set_title('Hesaplama Süresi Karşılaştırması')
    
    for i, v in enumerate(times):
        ax1.text(i, v + 0.001, f'{v:.4f}s', ha='center', fontweight='bold')
    
    # Hızlanma
    speedup = results.get('speedup', 0)
    ax2.bar(['Hızlanma (x)'], [speedup], color='#2ecc71')
    ax2.set_ylabel('Kat Hızlanma')
    ax2.set_title(f'Paralel Hızlanma: {speedup:.2f}x')
    ax2.text(0, speedup + 0.1, f'{speedup:.2f}x', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()