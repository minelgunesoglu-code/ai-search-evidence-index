# Genişletilmiş tasarım (v2) — 30 Ağustos 2026

Tur 5 geçerli ama **dar**: 19 sayfa, 19 alan adı, site başına tek sayfa.
Söyleyebildiğimiz tek şey "bu sayfa" hakkındaydı. v2 bunu genişletir.

**Kural: bu belge ölçüm başlamadan yazıldı. Ölçüm sırasında değiştirilmez.**
Değişirse tarihiyle not düşülür ve etkilenen her şey yeniden ölçülür.

## 1. Örnekleme çerçevesi

Aday havuzu, **altı tohum sorguda** ilk on organik sonuç. İki sorgu tur 5'ten
devralındı, dört tanesi kendi sayfalarımızın hedef sorgularından eklendi:

1. `generative engine optimization guide 2026` *(devralındı)*
2. `best AI search visibility tools comparison 2026` *(devralındı)*
3. `how to get cited by ChatGPT`
4. `how to track brand mentions in ChatGPT`
5. `what is answer engine optimization`
6. `how to rank in AI Overviews`

Sorgular kendi sayfalarımızın hedefleridir; böylece "bizimle aynı sorguda
yarışıyor" şartı korunur.

## 2. Dahil etme (tur 5'ten aynen devralındı)

1. Bağımsız site — yayın platformu değil (Medium, LinkedIn, Substack hariç)
2. Sayfada sayısal iddia bulunacak
3. Bizim bir sayfamızla aynı sorguda yarışıyor olacak

**Hariç:** ismybrandinai.com. Gerekçe: aracı elimizde tutarken kendi
sayfalarımızı düzelttik, ölçülen sayfalar bunu yapamadı — bizim için çıkacak
sayı onlarınkiyle kıyaslanabilir olmazdı. Kendi rakamlarımız gizlenmiyor: dört
sayfamızın ölçümü (%52, %42, %52, %17) makalenin "Why our own pages are not in
the table" bölümünde yayımlanıyor.

## 3. Derinlik: site başına ÜÇ sayfa

Her nitelikli alan adından, aynı türden üç sayfa (rakam taşıyan rehber ya da
karşılaştırma). Ortalaması alınmaz — **üçü de ayrı raporlanır.** Sayfa içi
değişkenlik başlı başına bir bulgudur: bir site bir sayfasında kaynak verip
diğerinde vermiyorsa, bunu görmek isteriz.

Üç sayfa bulunamayan siteler bulunanla girer ve kaç sayfayla girdiği yazılır.

## 4. Tür ayrımı (v2'de EKLENDİ)

Tur 5'te iki farklı tür tek metrikte karışmıştı:

| Tür | İddiaların doğası | Ulaşılabilirlik ne demek |
|---|---|---|
| **Araç karşılaştırma** | fiyat / özellik ("$99/ay, 10 motor") | satıcının fiyat sayfası linklendi mi |
| **Rehber / araştırma** | istatistik ("%68 tıklamasız arama") | çalışma linklendi mi |

İkisi **ayrı raporlanır.** Araç zaten fiyat iddialarını ayrı sayıyor
(`fiyat` / `fiyat_ulasilir` sütunları); v2'de bu ayrım rapora taşınır.

## 5. Ölçüm

- Araç **v1.5**, dondurulmuş. Ölçüm sırasında değiştirilmez.
- Tek zaman damgası, hepsi arka arkaya çekilir, çekilemeyen düşer ve raporlanır.
- **A kademesi (linkli) yüzde olarak yayınlanır** — elle ölçülmüş %82 geçerlilik.
- **B kademesi yüzde olarak YAYINLANMAZ** — işaret + doğrulanmış örnek.
- **Kaynakça sütunu**: sayfa sonu künyesi kaç tane, kaçı linkli.
- 10'dan az iddiası olan sayfa yüzde almaz.

## 6. Doğrulama

- Yayınlanan **her** A kademesi linki elle okunur. İstisnasız.
- Her sayfa için bir B örneği elle doğrulanır.
- Yeni eklenen sayfalardan rastgele 20 iddia kör kodlanır; araçla uyum raporlanır
  (tur 5'te 30 maddede %83'tü).

## 7. Baştan kabul edilen sınırlar

1. Tek gün, tek çekim. Sayfalar değişebilir — `data-mania.com` tur 3'te
   181 dipnot linkini kaybetmişti, kanıtı saklı.
2. Üç sayfa bir siteyi temsil eder mi — etmeyebilir. "Bu üç sayfa" denir.
3. Altı sorgu bir sektör değildir. "Bu sorgularda çıkan sayfalar" denir.
4. Çerçeve kusurları simetriktir ama sayfa yapıları farklıysa simetri bozulur:
   tablo yoğun sayfaların paydası şişer. Blok sayısı da ayrıca raporlanır.
5. Araç B kademesinde %83'te kalmıştır; bu yüzden o kademe yüzdesizdir.

## 8. Tur 5'in durumu

Tur 5 **iptal edilmez**. v2 tamamlanınca ikisi karşılaştırılır: dar örneklemin
sonucu geniş örneklemde de duruyor mu? Durmuyorsa bu da bir bulgudur.

---

## DEĞİŞİKLİK 1 — 30.08.2026, SERP toplandıktan sonra, ölçüm BAŞLAMADAN önce

**§3 "site başına üç sayfa" kuralı kaldırıldı.** Yerine: **çerçeve SERP'in kendisidir.**
Bir alan adı, Google onu kaç kez sıralıyorsa o kadar sayfayla girer.

**Gerekçe:** "site başına üç sayfa" kuralı, ikinci ve üçüncü sayfayı *benim seçmemi*
gerektiriyordu — hangi üç sayfa? Bu, tekrarlanabilirliği bozan bir hüküm adımıdır.
SERP çerçevesi ise mekaniktir: aynı sorguları çalıştıran herkes aynı listeye ulaşır.

Ayrıca doğal ağırlıklandırma sağlıyor: `tryprofound.com` dört sorguda birden çıkıyor
ve dört sayfayla giriyor. Bu bir kusur değil, o sitenin bu alandaki görünürlüğünün
ölçüsü. Tek sayfayla çıkan siteler tek sayfayla giriyor.

**Sonuç:** 38 URL · 30 tekil alan adı. Çok sayfayla girenler: tryprofound.com (4),
semrush.com (4), developers.google.com (2), searchengineland.com (2).

**Tur 5'in konumu:** iptal değil. Tur 5 iki sorguluk **pilot** olarak raporlanır;
altı sorguluk geniş çerçeve onu doğruluyor mu, ayrıca yazılır. Tur 5'in 19 sayfasından
altısı yeni çerçevede de çıktı (digitalapplied, evertune, frase, industry-lens,
llmrefs, semrush) — bu altısında iki turun sonucu karşılaştırılabilir.
