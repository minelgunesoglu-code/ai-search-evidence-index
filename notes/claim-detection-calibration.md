# İddia sayımının doğrulanması — 31 Ağustos 2026

Şimdiye kadar aracın **hükmü** sınandı ("bu rakamın linki var mı"). Bu belge
aracın **sayımını** sınar: *makinenin iddia saydığı şey gerçekten bir iddia mı?*

Bu, yüzdelerin **paydası** demektir. Payda şişerse bütün oranlar düşer.

## Yöntem

İki bağımsız örneklem, ikisi de rastgele (tohum kayıtlı), toplam **50 madde**
elle kodlandı. Soru tek: *bu, okuyucunun kaynağını sorabileceği bir olgusal
sayısal iddia mı?*

- **İddia sayılanlar:** araştırma istatistiği, fiyat, ürün kapsamı (motor/dil
  sayısı), vaka sonucu, kendi ölçümlerinin metodolojisi
- **İddia sayılmayanlar:** tavsiye ("her 90 günde bir güncelleyin"), yazar
  biyografisi, iyi yazım örneği, deyim ("Fortune 500"), tarih, formül örneği

## Sonuç

| | |
|---|---|
| Kodlanan madde | **50** |
| İddia olmayan | **11** |
| **Yanlış pozitif oranı** | **%22** (95% GA: %11 – %33) |
| Bunların linksiz olanı | **6/7** *(ilk örneklemde ölçüldü)* |

## Önemli olan yön

Yanlış pozitiflerin neredeyse tamamı **linksiz**. Yani payda şişiyor, pay
şişmiyor → **bütün yüzdeler olduğundan DÜŞÜK.** Bu, herkesi (bizi de) daha
kötü gösteren bir hata.

| | Ham | Düzeltilmiş nokta tahmin | Aralık |
|---|---|---|---|
| Havuz oranı (474 iddia, 178 linkli) | **%37,6** | **%46,3** | %41 – %53 |
| Sayfa medyanı | **%24** | **~%29** | — |

## Mekanik düzeltme DENENDİ ve YETMEDİ

v1.7'de kesin olan kategoriler elendi (biyografi kalıpları, `N out of M` formül
örneği, `31 Jul 2026` tarih biçimi, `Fortune 500`). 474 iddiadan 13'ü düştü,
medyan %23'ten %24'e çıktı.

**Ama ikinci örneklemde yanlış pozitif oranı %20 kaldı** (%23'ten). Filtreler
o özel ifadeleri yakaladı, kategoriyi yakalamadı:

| Kaçan | Neden regex yakalayamaz |
|---|---|
| "Review top-performing content every 90 days" | tavsiye — dilbilgisel olarak iddiadan ayırt edilemez |
| "worked as senior SEO specialist for Chess.com — one of the top 100 most visited websites" | biyografi ama farklı ifade |
| `GEO-optimized: "Video content is increasingly surfaced by AI engines…"` | iyi yazım örneği, tırnak içinde ama şablon filtresi kaçırıyor |
| "Choose Google AI Overviews if: You already rank well organically" | tavsiye |

**Karar: daha fazla desen eklenmeyecek.** Her ekleme yeni yanlış alarm üretti
(bkz. `ARAC-REVIZYON-GECMISI.md` v1.4, v1.6). Onun yerine **kalibrasyon
yayınlanacak**: ham rakam + elle ölçülmüş %22 yanlış pozitif oranı + güven
aralığı + düzeltilmiş tahmin.

## Rapora gireceği hâl

> Aracımız her sayfadaki sayısal iddiaları otomatik sayar. 50 iddianın elle
> kontrolünde bunların **%22'sinin (95% GA: %11–%33)** aslında iddia olmadığını
> ölçtük — tavsiye cümleleri, yazar biyografileri, yazım örnekleri. Bu
> yanlış sayımların neredeyse tamamı linksiz bloklarda; yani yayınladığımız
> oranlar **gerçeğin altındadır**. Ham ve düzeltilmiş rakamları birlikte
> veriyoruz; ham rakam ölçtüğümüz, düzeltilmiş rakam tahminimizdir.

## Bu neden kabul edilebilir

1. Hata **simetriktir** — aynı araç herkese uygulandı, sıralama değişmez
2. Yönü **bilinir ve tek yönlüdür** — kimseyi olduğundan iyi göstermiyor
3. Büyüklüğü **ölçülmüştür**, tahmin değil
4. Asıl bulgu (**%0–%74 yayılım, aynı site içinde bile**) bu düzeltmeden
   etkilenmiyor — yayılım oranların mutlak düzeyine değil, aralarındaki farka
   dayanıyor
