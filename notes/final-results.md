# The AI Search Evidence Index — geçerli sonuç

**Çekim:** 30 Ağustos 2026, 20:38:51–20:40:15 UTC · **Araç:** v1.7 (blok bazlı)
**Doğrulama:** yayınlanan her blok elle okundu (90 blok, istisnasız); 10 makine hükmü reddedildi

## Tablo

Birim = **blok**. Bir blok, içinde en az bir sayısal iddia taşıyan bir paragraf,
liste maddesi, tablo satırı ya da alıntıdır. "Kaynaklı" = blokta, o iddiayı
kaynaklayan çalışan bir bağlantı var.

| Sayfa | Blok | Kaynaklı | **A%** | *(rakam bazlı)* |
|---|---|---|---|---|
| industry-lens.com | 21 | 13 | **%62** | *%63* |
| tryprofound.com — *top-experts* | 11 | 6 | **%55** | *%74* |
| tryprofound.com — *what-is-aeo* | 10 | 5 | **%50** | *%59* |
| promptzero.tech | 15 | 6 | **%40** | *%44* |
| writer.com | 35 | 14 | **%40** | *%58* |
| frase.io | 48 | 19 | **%40** | *%41* |
| ahrefs.com | 15 | 5 | **%33** | *%57* |
| aisearch.similarweb.com | 24 | 8 | **%33** | *%37* |
| semrush.com | 18 | 2 | **%11** | *%11* |
| seocrawl.ai | 17 | 1 | **%6** | *%9* |
| tryprofound.com — *best-tools* | 17 | 1 | **%6** | *%10* |
| llmrefs.com | 11 | 0 | **%0** | *%0* |
| zapier.com | 10 | 0 | **%0** | *%5* |

**13 sayfa · medyan %33 · aralık %0–%62 · havuz 80/252 = %31,7**

10 bloktan az olan 12 sayfa yüzdesiz bırakıldı.

## Elle yapılan düzeltmeler (makine → insan)

Her biri okunup reddedildi:

| Sayfa | Reddedilen | Gerekçe |
|---|---|---|
| `ahrefs.com` | `help.ahrefs.com/…` · `linkedin.com/in/joshuahardwick28` | yardım dokümanı · kişi profili |
| `frase.io` | `/blog/ai-visibility` · `/tools/geo-score?utm_…` | kendi rehberi · kendi aracı |
| `aisearch.similarweb.com` | `/ai-brand-visibility/prompt-analysis/` | kendi aracı |
| `promptzero.tech` | `promptzero.tech/#features` | kendi ürün bölümü |
| `semrush.com` | `semrush.com/ai-seo/overview/` | kendi ürün sayfası |
| `zapier.com` | `zapier.com/apps` | kendi uygulama dizini |
| `industry-lens.com` | `ahrefs.com/pricing` ("466M prompt" için) | fiyat sayfası o rakamı taşımıyor |
| `tryprofound.com-4` | kendi ilgili yazısı (Gartner iddiası için) | iddiayı kaynaklamıyor |

## Yayınla birlikte verilecek üç uyarı

**1. `industry-lens.com` yapısal olarak avantajlı.** Tablo lideri, ama
kaynaklarının çoğu **kendi `/reports/` sayfaları**. Site bir haber toplayıcı;
her haberi zaten bir kaynağa bağlı. Bu bir üstünlük değil, bir tür farkı.

**2. İddia sayımının ölçülmüş hatası: %22,4.** 120 bloklu kör örneklemde,
aracın gerçekten puanlayacağı 85 bloğun 19'u aslında iddia değildi (tavsiye,
biyografi, yazım örneği) — %95 GA %13–%31. Bu 19'un yalnız 3'ü kaynaklı
sayılmıştı, yani ağırlıkla kaynaksız tarafta duruyorlar ve **yayınlanan oranlar
gerçeğin altındadır.** 252 bloğa uygulanınca düzeltilmiş havuz tahmini
≈ **%36**. (Daha önceki 50 bloklu geçiş tutarlı bir %22 vermişti ama madde
bazındaki hükümleri saklanmadı; yayınlanan sayfalardan yeniden üretilemiyor.)

**3. Altı sayfa çekilemedi: dördü HTTP 403 bot koruması, ikisi bağlantı hatası** ve rastgele değiller —
searchengineland (2), business.adobe.com, technologyadvice, brafton, otterly.
Tarayıcıda alınan kaba gözlem: %8, %14, %11, %71, %100. Ana tabloya
katılmadılar.

## Değişmeyen bulgu

Ölçüm birimi değişti (rakam → blok), 10 link elle reddedildi, örneklem iki
sorgudan altıya çıktı. **Manşet bulgu üç değişikliğin de altından aynı çıktı:**

> Bu alanda kaynak verme diye bir norm yok. Sayfalar **%0 ile %62** arasında
> dağılıyor ve **aynı yayıncının kendi sayfaları arasındaki fark**, yayıncılar
> arasındaki fark kadar büyük: `tryprofound.com` bir sayfasında %55, başka bir
> sayfasında %6.

Kaynak vermek bir kurum politikası değil; sayfa sayfa, yazar yazar değişiyor.
