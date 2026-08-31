# Sayım birimi kararı — 31 Ağustos 2026

**Ölçümün birimi BLOK olarak değiştirildi.** Rakam bazlı sayım sağlamlık
kontrolü olarak yanında raporlanır.

## Sorun

v1.2'den beri araç, bir bloktaki **her ayrı rakamı** bir iddia sayıyordu ve
hepsine bloğun link hükmünü uyguluyordu. Yani beş rakam içeren ve **tek** link
taşıyan bir blok, **beş linkli iddia** olarak sayılıyordu.

Tek link beş rakamı kaynaklamaz. Genellikle birini kaynaklar.

## Bu kimi kayırıyordu

Rakam yoğun bloklar yazan sayfaları — yani yazım tarzını, kaynaklama davranışını
değil.

| Sayfa | Rakam bazlı | Blok bazlı | Fark |
|---|---|---|---|
| `tryprofound.com` | %74 | **%55** | −19 |
| `writer.com` | %58 | **%40** | −18 |
| `ahrefs.com` | %57 | **%47** | −10 |
| `industry-lens.com` | %63 | %67 | +4 |
| `semrush.com` | %11 | %17 | +6 |

**Tablonun tepesindeki üç sayfa da şişmişti.** Adıyla yayınlanacak bir tabloda
bu kabul edilemez.

## Karar

**Ana ölçü: blok bazlı.** Bir blok = bir iddia; blokta çalışan bir kaynak
bağlantısı varsa ulaşılabilir sayılır.

**Gerekçe:**
1. Tek link, bloktaki bütün rakamlara kredi kazandırmıyor
2. Yazım tarzından (rakam yoğunluğundan) bağımsız
3. Okuyucunun deneyimine daha yakın: kaynaklı paragraf / kaynaksız paragraf

**Rakam bazlı ölçü kaldırılmıyor** — her tabloda ikinci sütun olarak veriliyor.
Okuyucu iki ölçünün de sonucunu görsün.

## Alan düzeyindeki bulgu iki ölçüde de aynı

| | Rakam bazlı | Blok bazlı |
|---|---|---|
| v2 rakip medyan | %41 | **%40** |
| Tur 5 rakip medyan | %5 | **%6** |
| Yayılım | %0 – %74 | **%0 – %67** |

Manşet bulgu — **norm yok, aynı site kendi içinde bile değişiyor** — birim
seçiminden etkilenmiyor. Etkilenen tek şey tek tek sayfa yüzdeleri, ve o yüzden
ikisi birden yayınlanıyor.

## Kendi sayfalarımız (tur 5, tabloya girmiyor ama simetri için)

| Sayfa | Rakam bazlı | Blok bazlı |
|---|---|---|
| `BIZ-cited` | %90 | %91 |
| `BIZ-geo` | %85 | **%75** |
| `BIZ-tools` | %74 | %74 |
| `BIZ-track` | %24 | **%33** |

Aynı düzeltme bize de uygulandı; `BIZ-geo` 10 puan kaybetti.
