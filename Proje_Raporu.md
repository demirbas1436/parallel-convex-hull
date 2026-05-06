# Paralel Convex Hull Proje Raporu

## 1. Programın Çalışma Prensibi, Kullanılan Fonksiyonlar ve Çalışma Örnekleri

### 1.1 Çalışma Prensibi
Convex Hull (Dışbükey Örtü), 2 boyutlu bir düzlem üzerinde bulunan bir dizi noktayı tamamen içine alan en küçük dışbükey çokgeni bulma problemidir. Bu proje, nokta setlerinin Convex Hull'unu hesaplamak için **Graham Scan** ve **Jarvis March** (Gift Wrapping) algoritmalarını implemente etmektedir. Program, modern işlemcilerin çok çekirdekli yapısından faydalanabilmek adına bu hesaplamaları sadece standart (seri) yöntemle değil, **paralel hesaplama (multi-threading)** teknikleriyle de çözebilecek şekilde tasarlanmıştır.

### 1.2 Kullanılan Temel Sınıf ve Fonksiyonlar

- **`Point` Sınıfı:** Sistemdeki noktaları nesne yönelimli olarak temsil eder.
  - `Point.orientation(p1, p2, p3)`: Üç noktanın dönüş yönünü hesaplar. Matematiksel olarak vektör çarpımından yararlanarak noktaların saat yönünde (clockwise), saat yönünün tersinde (counter-clockwise) veya doğrusal (collinear) olup olmadığını belirler. Bu fonksiyon Convex Hull algoritmalarının kalbidir.
  - `Point.distance_to()`: İki nokta arasındaki Öklid mesafesini hesaplar (Aynı açıdaki noktalarda en uzak olanı seçmek için kullanılır).

- **`graham_scan(points)`:** 
  - **Karmaşıklık:** O(n log n)
  - İşleyişi: Y-koordinatı en küçük olan noktayı pivot olarak seçer. Diğer tüm noktaları pivota göre kutupsal (polar) açılarına göre saat yönünün tersine sıralar. Ardından noktaları sırayla bir yığına (stack) ekler ve sola dönüş yapmayan (içe doğru kıvrılan) noktaları yığından çıkararak dışbükey sınırları elde eder.

- **`jarvis_march(points)`:**
  - **Karmaşıklık:** O(nh) (n: toplam nokta, h: hull üzerindeki nokta sayısı)
  - İşleyişi: En soldaki noktadan başlayarak her adımda, mevcut noktaya göre en geniş açıyı yapan (en dışarıda kalan) noktayı bulur. Tüm çevre sarılana kadar bu hediye paketi sarma mantığı devam eder.

- **`ConvexChecker` Sınıfı:** Sistemin koordinatörüdür. Noktaların yüklenmesi, JSON olarak dışa/içe aktarılması, sonuçların analizi ve istatistiklerin üretilmesini sağlar.

### 1.3 Çalışma Örnekleri

Proje, Komut Satırı Arayüzü (CLI) kullanılarak esnek bir şekilde çalıştırılabilir.

**Örnek 1: Seri (Normal) Çalıştırma**
Rastgele üretilmiş 1000 noktanın tek iş parçacığı (seri) ile işlenmesi:
```bash
python main.py --points 1000
```
*Çıktı Özeti: 1000 nokta oluşturulur, seri Graham Scan çalıştırılır ve 16 noktadan oluşan convex hull milisaniyeler içinde bulunur.*

**Örnek 2: Paralel Benchmark ve Görselleştirme**
10.000 nokta üretip 8 thread ile paralel modda benchmark yapmak ve sonucu grafik (PNG) olarak kaydetmek:
```bash
python main.py --points 10000 --parallel --threads 8 --benchmark --visualize
```
Bu komut, hem seri hem paralel süreyi karşılaştırır, istatistikleri konsola basar ve `convex_hull.png` dosyasını oluşturur.

---

## 2. Parametrelerin Etkisi ve Elde Edilen Hızlanma Katsayıları

Paralel algoritmanın performansını test etmek için `ParallelConvexHull.benchmark()` fonksiyonu üzerinden yapılan testlerin sonuçları aşağıda tablolaştırılmıştır. Hızlanma Katsayısı (Speedup), **S = T_seri / T_paralel** formülü ile hesaplanmıştır.

### Nokta Sayısına Göre Hızlanma (Sabit 4 Thread)

| Nokta Sayısı (n) | Seri Süre (sn) | Paralel Süre (sn) | Hızlanma Katsayısı (Speedup) |
|:---:|:---:|:---:|:---:|
| 100 | 0.0002 | 0.0072 | **0.03x** |
| 500 | 0.0008 | 0.0015 | **0.52x** |
| 1.000 | 0.0016 | 0.0030 | **0.51x** |
| 5.000 | 0.0080 | 0.0098 | **0.81x** |
| 10.000 | 0.0163 | 0.0205 | **0.80x** |
| 50.000 | 0.0901 | 0.1068 | **0.84x** |
| 100.000 | 0.2061 | 0.2675 | **0.77x** |

### İş Parçacığı (Thread) Sayısına Göre Hızlanma (Sabit 50.000 Nokta)

| Thread Sayısı | Seri Süre (sn) | Paralel Süre (sn) | Hızlanma Katsayısı (Speedup) |
|:---:|:---:|:---:|:---:|
| 2 Thread | 0.1064 | 0.1299 | **0.82x** |
| 4 Thread | 0.1013 | 0.1194 | **0.85x** |
| 8 Thread | 0.0983 | 0.1117 | **0.88x** |

### Performans Analizi Değerlendirmesi
Tablolardan açıkça görüldüğü üzere hızlanma katsayısı hiçbir senaryoda 1.0 değerini aşamamıştır. Yani paralel yaklaşım, seri yaklaşıma göre daha yavaş çalışmıştır. Bunun iki ana bilimsel sebebi vardır:

1. **Python'ın GIL (Global Interpreter Lock) Mekanizması:** Python'ın varsayılan yorumlayıcısı (CPython), aynı anda birden fazla thread'in Python bytecode'unu çalıştırmasına izin vermez. Convex Hull problemi, matematiksel hesaplamalara dayalı **CPU-bound (İşlemci Yoğun)** bir problemdir. I/O işlemleri (dosya okuma, ağ isteği vb.) beklemediği için, thread'ler birbirlerini beklerler (context switching) ve gerçek manada paralel CPU kullanımı sağlanamaz.
2. **Overhead (Ek Yük):** Thread'lerin oluşturulması, verilerin parçalara ayrılması ve en sonunda elde edilen kısmi Hull'ların bir araya getirilip (merge) tekrar Graham Scan'e sokulması sistemde sabit bir zaman maliyeti yaratır. Nitekim n=100 nokta için overhead o kadar fazladır ki algoritma 0.03x hızlanma (yaklaşık 33 kat yavaşlama) sergilemiştir.

---

## 3. Elde Edilen Paralel Çözümün Açıklanması

Projenin temel hedeflerinden olan paralel çözüm, **Böl ve Fethet (Divide and Conquer)** mimarisine dayalı olarak `src/thread_manager.py` dosyası içindeki `ParallelConvexHull` sınıfında gerçekleştirilmiştir. 

Paralel çözüm üç aşamalı bir boru hattı (pipeline) olarak kurgulanmıştır:

### Aşama 1: Bölme (Partitioning)
`_partition_points` metodu, ilk olarak verilen tüm noktaları x-koordinatına göre artan sırada sıralar. Sıralanmış bu devasa nokta listesi, sistemde tanımlı thread sayısı kadar (örneğin 4'e) mantıksal alt kümelere bölünür. Verilerin mekansal (spatial) olarak sıralı bölünmesi, her alt kümenin sadece kendi bölgesindeki sınırları bulmasını sağlar.

### Aşama 2: Eşzamanlı Hesaplama (Mapping via Threads)
Bölünen noktalar, Python'ın `concurrent.futures.ThreadPoolExecutor` sınıfı aracılığıyla havuzdaki iş parçacıklarına dağıtılır. `executor.submit(graham_scan, partition)` komutu ile her thread kendi bağımsız nokta listesini alır ve üzerinde Graham Scan algoritmasını çalıştırır. Eğer GIL limiti olmasaydı, bu aşamada 4 farklı çekirdek aynı anda alt-poligonları hesaplamış olacaktı. 

### Aşama 3: Birleştirme (Merging)
Bütün thread'ler işlemlerini tamamladığında, her bölgeden kısmi (partial) convex hull noktaları döner. Bu kısmi hull'lar `_merge_hulls` fonksiyonu ile sırayla birleştirilir. 
- İki alt-hull birleştirilirken, listeler birleştirilir ve mükerrer noktaların filtrelenmesi için matematiksel kümeler (`set()`) kullanılır.
- Birleştirilen bu taslak noktaların üzerine tekrar `graham_scan()` çalıştırılır. 
- Döngüsel olarak tüm parçalar birleştirildiğinde global ve kesin (final) Convex Hull noktalarına ulaşılır.

*Geliştirme Önerisi:* İleriki çalışmalarda GIL problemini aşmak ve %100 CPU kullanımına (gerçek paralellik) ulaşmak için Thread tabanlı `ThreadPoolExecutor` yerine, process tabanlı `ProcessPoolExecutor` (Multiprocessing) kütüphanesi kullanılarak hızlanma katsayısının (Speedup) 1.0'ın üzerine, hatta thread sayısına yakın bir değere (örneğin 4 core için ~3.5x'e) çıkarılması hedeflenmelidir.
