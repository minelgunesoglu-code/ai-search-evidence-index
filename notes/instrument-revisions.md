# Ölçüm aracının revizyon geçmişi — Evidence Index coder

Araç **30 Ağustos 2026'da bir gün içinde beş kez revize edildi.** Her revizyon,
makinenin ürettiği sayıyı elle okuyunca ortaya çıktı. Hiçbiri makine tarafından
bulunamazdı.

Bu geçmiş yayınlanacak: bir ölçüm aracının kaç kez ve neden yanıldığını göstermek,
sonucun kendisi kadar önemli.

---

## v0 → v1.0

| # | Bulunan kusur | Nasıl bulundu | Etki |
|---|---|---|---|
| 1 | **Tarihler iddia sayılıyordu** — `Updated On: July 28, 2026`'dan `28` ve `2026` çıkarılıyordu | data-mania'nın %79'u şüpheli görünüp örnekler okundu | 275 → 261 iddia |
| 2 | **Tek blokta çok sayı** aynı kodu defalarca saydırıyordu | Tekrarlanan metinler fark edildi | Blok bazı raporlama eklendi |
| 3 | **Sayfa başlıkları** iddia sayılıyordu (`19 Best AI Tools`) | 40 iddialık elle kontrol | %15 çerçeve kusuru |
| 4 | **Tablo kaynak notu** satırları kapsamıyordu | Kendi GEO sayfamız %5 çıktı, sebebi arandı | Tablo kuralı eklendi |

## v1.0 → v1.1

| # | Bulunan kusur | Nasıl bulundu | Etki |
|---|---|---|---|
| 5 | **"Kaynak adı var, link yok" sıfır sayılıyordu** — llmrefs.com kaynağını adıyla veriyordu (Vercel, Brandlight) ama %0 görünüyordu | 5 sıfır sayfası elle okundu | Üçüncü kademe eklendi |
| 6 | **Şablon/örnek cümleler** iddia sayılıyordu — obapr'ın *"✔ PR ajansları $5.000-$50.000 alır"* okura verdiği KALIP | Aynı okuma | Şablon filtresi |
| 7 | **Küçük örneklemde yüzde** anlamsızdı — thehoth 3 iddiada "%33" | Aynı okuma | 10 iddia eşiği |
| 8 | **Parantezli akademik atıf görülmüyordu** — `(Ahrefs, 2025)`, `(Gartner, 2024)`. nav43 %8 görünüyordu, gerçekte iddialarının %44'ünde kaynak belli | nav43 elle okundu | Adlı kademe 30 → 64 |

## v1.1 → v1.2 — DOĞRULAMA KÜMESİ

Burada yöntem değişti: tahmin yerine **ölçülmüş geçerlilik.**

92 iddialık katmanlı örneklem çıkarıldı, **46 linkli iddia elle kodlandı**
(insan hükmü: *"bloktaki link GERÇEKTEN bu rakamı kaynaklıyor mu"*).

**v1.1'in ölçülen hatası: %38** (39 kodlanabilir iddiada 15 yanlış).
Ayrıca 46'nın 7'si (%15) iddia bile değildi — kart listelerindeki tarihler,
`arXiv:2311.09735` gibi belge kimlikleri.

Denenen kurallar ve doğrulama kümesine karşı uyumları:

| Kural | Uyum | Yanlış pozitif |
|---|---|---|
| v1.1 — "blokta link varsa yeter" | %62 | 15 |
| + kendi sitesine link sayılmasın | **%54** ↓ | — |
| + çıplak ana sayfa sayılmasın | %67 | — |
| + çıpa metni kuralı | %77 | 1 |
| **+ fiyat sayfası istisnası** | **%82** | **2** |
| + eşik gevşetilmiş hâli | %82 | 6 ❌ reddedildi |

**Seçilen: %82 uyum, 2 yanlış pozitif.** Aynı uyumu veren daha gevşek ayar
reddedildi — adıyla skor yayınlanan bir çalışmada *"kaynağı var"* deyip yanılmak,
kaçırmaktan çok daha zararlıdır.

### Sezgimin yanıldığı yer

*"Kendi sitesine verilen link kaynak sayılmaz"* diye bir kural ekledim; mantıklı
görünüyordu. Doğrulama kümesi uyumu **%77'den %54'e düşürdü** ve kural atıldı.
Kendi çalışmasına ya da kendi fiyat sayfasına link vermek meşru kaynaktır.

---

## Kalan sınırlar (v1.2'de KAPATILMADI)

1. **%18 uyumsuzluk sürüyor** — 2 yanlış pozitif, 5 kaçırılan. Bunlar insan
   hükmü gerektiriyor.
2. **Kural bir yazım tarzını ödüllendiriyor.** Çıpa metninin iddiayı içermesi
   iyi uygulamadır, ama bizim linklerimiz 30 Ağustos'ta tam o tarzda yazıldı;
   rakipler marka adına çıpalıyor. **Bu asimetri raporda belirtilecektir.**
3. Doğrulama kümesi **tek kodlayıcı** tarafından kodlandı (kör çift kodlama yok).
4. Örneklem 46 linkli iddia — daha fazla kodlama uyum tahminini daraltır.

---

## v1.3 — 30 Ağustos, isim katmanı düzeltmesi

### Nasıl bulundu

10 maddelik bir alt küme, aracın çıktısı görülmeden elle kodlandı (kodlar önce
`kor-kod-CLAUDE-1-10.json`'a mühürlendi, sha256 ile). Araçla uyum **7/10**.

Üç ıskanın **üçü de aynı yöndeydi**: kaynağını adıyla veren blokları
"kaynaksız" sayıyordu.

| # | Sayfa | Kaçan ifade | Neden |
|---|---|---|---|
| 1 | nav43.com | `(Joshua Blyskal/Profound, 100,000 prompts analyzed, 2025)` | parantezli desen `(İsim, YYYY)` bekliyordu; isimle yıl arasına metin girince kırılıyor |
| 3 | llmpulse.ai | `Indig's data showed` | iyelik + rapor fiili kalıbı yoktu |
| 9 | ayzeo.com | `Princeton-led GEO study` | yalnızca `study by X` vardı, `X-led study` yoktu |

### Neden ciddi

Hata tek yönlü: **rakipleri olduğundan kaynaksız gösteriyordu.** Sayfaları adıyla
yayınlayacağımız bir çalışmada bu, düzeltilemez bir yanlış beyandır.

### Aşırı uyum (overfitting) kontrolü

Desenler bu 10 maddeye bakılarak yazıldığı için sınav kendi sorularıyla çalışmak
olurdu. Bu yüzden yeni desenler **korpusun tamamına** (2.258 linksiz blok)
uygulandı ve yeni yakalananların hepsi elle okundu.

- İlk deneme: 20 yeni yakalama → **8'i yanlış alarm**
  (`One study analyzed…` = isimsiz; `AI audit`/`site audit` = ürün özelliği adı;
  `Once the report loads` = cümle başı gürültüsü)
- Desen sıkılaştırıldı: cümle başındaki büyük harf sayılmaz; `audit`/`report`
  baş isim olmaktan çıkarıldı (bu nişte ürün adı oluyorlar)
- İkinci deneme: **11 yeni yakalama, 11'i de gerçek** (elle okundu, 0 yanlış alarm)

### Etki

- Rakiplerde "adı var, linki yok" iddia: **69 → 85** (+%23)
- `nav43.com` %8 → **A %8 / A+B %48** · `llmpulse.ai` %15 → **%46** ·
  `xseek.io` %4 → **%42**
- **Link katmanı (A) hiç değişmedi.** Bu düzeltme yalnızca isim katmanına
  dokunur; v1.2'nin elle ölçülmüş **%82** link-katmanı geçerliliği aynen geçerli.

### Rapora giren zorunlu sonuç

Tek rakam yayınlanmayacak. Her sayfa **iki kademeli** verilecek:
**A (link var)** ve **A+B (kaynak hiç değilse adıyla anılmış)**. Yalnızca A
yayınlamak, kaynağını adıyla veren sayfaları kaynaksız göstermek olurdu.

### v1.3'te de kapatılmayan sınır

Blok düzeyinde tek etiket veriliyor. `ayzeo.com`'un 935 karakterlik bloğunda
%40 rakamı Princeton çalışmasına, byline alıntısı Google dokümanına ait —
iki ayrı kaynak, tek etiket. Blok başına birden çok atıf ayrıştırılmıyor.

---

## v1.4 — 30 Ağustos, doğrulama 30 maddeye çıkarıldı

Örneklem 10'dan 30'a çıkarıldı (kodlar `kor-kod-CLAUDE-1-30.json`'da mühürlü).
v1.3 bu kümede **%73** verdi. İki kanıtlı hata bulundu:

1. `according to` deseni **küçük harfliydi** — `According to BrightEdge` kaçıyordu.
   Bu hata v1.2'den beri vardı.
2. `predicts` / `forecasts` fiilleri yoktu — `Gartner predicts`, `Gartner forecasts`
   kaçıyordu.

**Uyum %73 → %83.**

### Denenip geri alınanlar

Sırf sayıyı yükseltmek için eklenip korpusta yanlış alarm ürettiği görülen ve
**geri çekilen** desenler:

| Denenen | Neden geri alındı |
|---|---|
| `shows / notes / states / finds` | `It shows the top 20 competitors`, `Page Analytics shows`, `This shows Warby Parker` — hepsi kaynak sanıldı |
| Büyük harfli alan adı | Araç karşılaştırma yazılarında her ürün adına ateşledi (`Frase, Profound, Otterly.ai…` listesi) |
| `X's own \w+` | Tablo hücrelerinde ateşledi (`Tied to Google's own retrieval`) |

Her deneme 2.347 linksiz bloğa uygulanıp yeni yakalamalar elle okundu.

### Kapatılamayan sınır → yayın kararı

Kalan 5 ayrışmanın 4'ü **tek bir sınıf**: fiyat iddiasında satıcının kendi adı
(`Profound covers one engine at $99 and three at $399`, `Frase plans start at
$39/month`). Beşincisi makale içi bir karakter (`James's fastest method`) —
okuyucunun dışarıdan bulamayacağı bir ad.

Bu yüzden **B kademesi rapora yüzde olarak GİRMEYECEK.** Her sayfa için yalnızca:

- **A (link var)** → yüzde yayınlanır, elle ölçülmüş **%82** geçerlilikle
- **B (adı var, link yok)** → yalnızca *var / yok* işareti + **elle doğrulanmış
  1-2 örnek** (ör. nav43 için `(Ahrefs, December 2025)`)

Gerekçe: ölçemediğimiz bir sayıyı yayınlamak, adını verdiğimiz bir siteye
haksızlık etme riski taşır. `nav43.com` tek rakamla %8 görünüyor; oysa
iddialarının önemli kısmında kaynağı adıyla anıyor — sadece linklemiyor.

---

## v1.5 — 30 Ağustos, ANA ölçümde bulunan hata (en ciddisi)

Bu revizyon isim katmanında değil, **yayınlanacak ana rakamda** bir hata düzeltir.

### Nasıl bulundu

Adı verilecek sekiz sayfanın "linkli" sayılan **her** iddiası tek tek okundu.
Aracın kaynak saydığı linklerin bir kısmı kaynak değildi:

| Sayfa | Araç | Gerçek |
|---|---|---|
| `visiblie.com` | 3 linkli iddia | **üçü de "Start Free Trial" düğmesi** — `14-day trial` / `500+ companies` sayıları `app.visiblie.com/signup` linkine eşlenmişti |
| `nav43.com` | 5 | **ikisi "Read Post" kartı** — yazı altındaki ilgili-yazı kutuları |
| `data-mania.com` | 9 | biri **savvycal randevu linki** |
| `useomnia.com` | 7 | biri `/demo` düğmesi |

Kök sebep: v1.2'nin **(F) fiyat kuralı** `/signup` yolunu da fiyat sayfası
sayıyordu; bir deneme süresi rakamı ile kayıt düğmesi eşleşiyordu.

### Eklenen iki kural

- **(G)** `/signup`, `/demo`, `/trial`, `/book`, `/contact`, `calendly`, `savvycal`
  gibi **çağrı ve randevu linkleri kaynak sayılmaz.** (F) kuralı yalnızca
  `/pricing` ve `/plans` ile sınırlandı.
- **(H)** Çıpası `Read Post` / `Read more` / `Learn more` olan bloklar
  **navigasyondur**, iddia değildir.

### Etki

| Sayfa | v1.4 | v1.5 |
|---|---|---|
| `visiblie.com` | %1 | **%0** |
| `nav43.com` | %8 | **%5** |
| `useomnia.com` | %41 | **%35** |
| `data-mania.com` | %5 | %5 |
| **bizim 4 sayfa** | — | **değişmedi (0 link düştü)** |

### Bu asimetri rapora yazılacaktır

Kural herkese aynı uygulanır; bizim sayfalarımızdan hiçbir link düşmez, çünkü
kaynak olarak çağrı düğmesi kullanmıyoruz. Ama kural **rakip sayfalar okunurken
bulundu**. Rapor bunu açıkça söyleyecek ve okuyucu kendi kontrol edebilsin diye
elenen link örnekleri (`app.visiblie.com/signup` → "Start Free Trial →")
verilecektir.

### Ders

İlk dört revizyon isim katmanını kovaladı; asıl hata **ana rakamdaydı** ve
ancak sayfalar tek tek elle okunduğunda görüldü. Regex'i regex ile doğrulamak
hatayı bulmuyor.

---

## v1.6 — 31 Ağustos, geniş çerçevede bulunan hata

v2 çerçevesi (38 sayfa) elle okunurken çıktı.

### Bulgu

| Sayfa | Araç | Elle okununca |
|---|---|---|
| `hubspot.com` | %36 (4 linkli iddia) | **dördü de kendi ürün sayfasına** (`hubspot.com/products/aeo`) |
| `digitalapplied.com` | 1 linkli | kendi **sözlük** sayfasına — ilgili içerik linki, kaynak değil |

Buna karşılık meşru sayılanlar — **kendi yayınlanmış çalışmasına** link vermek:
`aisearch.similarweb.com` → `similarweb.com/corp/reports/…` (kendi araştırma raporu),
`tryprofound.com` → `/customers/…` (kendi vaka çalışması). Bunlar okuyucuyu
rakamın çıktığı belgeye götürüyor; ürün sayfası götürmüyor.

### Kural (I)

Yayıncının **KENDİ** ürün / özellik / çözüm / sözlük / platform sayfasına giden
link kaynak sayılmaz.

### İlk deneme YANLIŞTI — düzeltildi

Kural önce bütün linklere uygulandı ve `blog.google/products/search/…`
adreslerini eledi. Bunlar Google'ın **blog yazıları**, ürün sayfası değil —
yolunda `/products/` geçiyor diye eleniyorlardı. Kural **yalnız iç linklere**
(aynı alan adı ya da göreli yol) daraltıldı.

### Etki

| Sayfa | v1.5 | v1.6 |
|---|---|---|
| `hubspot.com` | %36 | **%0** |
| `frase.io` | %42 | %41 |
| `purposelaunch.com` | %10 | %10 *(dış link, geri geldi)* |
| **rakip medyan** | **%36** | **%23** |

## v1.8 — 1 Eylül 2026, paketleme onarımı (ÖLÇÜM MANTIĞI DEĞİŞMEDİ)

31 Ağustos'ta dosya ve klasör adları Türkçe'den İngilizce'ye çevrildi, ama kod
güncellenmedi. Sonuç: **yayınlanan kod yayınlanan veriyi okuyamıyordu.** Kaynağa
ulaşılabilirliği ölçen bir çalışmada, çalışmanın kendisi çalıştırılamıyordu.

Bu revizyonda **hiçbir ölçüm kuralına dokunulmadı.** Kanıt: onarımdan sonra
`measure.py` yeniden çalıştırıldı ve `data/measurement-by-block.json`'ın 25
satırının 25'i, beş alanın hepsinde birebir aynı çıktı.

### Onarılanlar

1. **Yollar.** Bütün betikler `code/` klasörüne göreliydi; artık paketin kökünü
   buluyorlar. Anlık görüntüler `SNAPSHOTS` ortam değişkeniyle gösteriliyor
   (varsayılan `snapshots/`), çünkü telif nedeniyle yayınlanmıyorlar.
2. **`retrieval-log.csv` gerçek bir CSV.** `measure.py` ona `json.load()`
   uyguluyordu, `fetch.py` ise üzerine JSON yazıyordu. İkisi de düzeltildi;
   `fetch.py` artık yayınlanan dosyayla aynı sütunları yazıyor ve çekilemeyen
   sayfaları satır olarak bırakıyor (`status = failed_http_<kod>`).
3. **`sampling-frame.json` anahtarı.** `fetch.py` `sorgular` arıyordu, dosyada
   `queries` yazıyor.
4. **Çıktı anahtarları.** `measure.py` Türkçe anahtar yazıyordu; artık
   yayınlanan dosyanın İngilizce anahtarlarını üretiyor.
5. **`seed_query` kırpması.** Kodda 28 karakterlik bir kısaltma vardı. Yayınlanan
   dosyada tam sorgular yazılı, yani kırpma oraya hiç yansımamıştı — ama kod
   çalıştırılsaydı yansıyacaktı, çünkü yayınlanan dosyayı üreten sürüm bu
   kısaltmayı taşımıyordu. Kısaltma tamamen kaldırıldı.
6. **Import yan etkisi.** `measure.py` modül düzeyinde ölçümü çalıştırıp
   `data/measurement-by-block.json`'ın üzerine yazıyordu; `blind-sample.py` onu
   import ediyor. Onarımdan ÖNCE bu tehlike gerçekleşemiyordu, çünkü kod zaten
   yol hatasından çöküyordu (madde 1) — ama yollar düzelir düzelmez aktif hale
   geldi. Ölçüm artık `if __name__ == "__main__"` koruması altında.
7. **`blind-sample.py` veri siliyordu.** Yayınlanan `blind-sample-120.json`
   TAMAMLANMIŞ sayfadır (120 insan kodu + aracın hükmü). Betik ise BOŞ sayfa
   üretir ve aynı yola yazıyordu. Aynı şekilde bu da onarımdan önce çökme
   nedeniyle gerçekleşemiyordu; onarım sırasında bir kez gerçekleşti ve 120
   insan kodu silindi, yedekten birebir geri alındı. Betik artık çıktısını
   `SNAPSHOTS` klasörüne yazıyor.
9. **`blind-sample.py` dosya adı çıkarımı.** Yolları mutlaklaştırırken
   `alan = f[3:-5]` satırı `os.path.basename` almadan kaldı; blok kimlikleri
   tam dosya yolu olarak üretilmeye başladı ve `alan` bozulduğu için
   kendi-alan-adı kuralı yanlış çalıştı — tek bir blokta (`hubspot.com#85`)
   aracın hükmü değişiyordu ve κ 0,852 yerine 0,835 çıkıyordu. Bu hata
   onarım sırasında ÜRETİLDİ, aynı gün yapılan bağımsız denetimde yakalandı ve
   düzeltildi. Düzeltmeden sonra betik yayınlanan örneklemi birebir yeniden
   üretiyor: aynı 120 kimlik, aynı metinler, aynı hükümler, matris (37,1,7,75),
   κ = 0,8522, %95 GA 0,753–0,951.
8. **`dump-blocks.py`** `os`'u import etmiyordu ve argümansız çağrılınca
   traceback veriyordu; artık kullanım satırı yazdırıyor.

### Çekim penceresi — küçük ama bildirilmesi gereken fark

Yayınlanan `retrieval_window` değeri `fetch.py`'nin kendi başlangıç/bitiş
saatinden geliyordu ve son sayfanın indirme süresini de içeriyordu: 85,4 sn.
`retrieval-log.csv`'deki satır zaman damgalarından türetilen pencere 83,6 sn.
Tek kaynak artık CSV, çünkü yayınlanan tek şey o. Paketin tamamı bu değere
hizalandı: makale, README, CITATION.cff, `notes/final-results.md` ve
`data/measurement-per-number.json` artık 20:38:51–20:40:15 ve "84 saniye"
diyor. `measurement-per-number.json` bu paketteki tek elle düzeltilen veri
alanıdır; onu üreten bir betik yayınlanmıyor.

### Onarımın sağladığı: bağımsız sayaç iddiası ilk kez doğrulandı

Kod çalışır hale gelince `independent-counter.py` ilk kez v1.7 verisine karşı
çalıştırılabildi. Makale ve README'nin **"25 sayfanın 17'si birebir tuttu, 8
fark"** iddiası **doğrulandı** — ama yalnız doğru tabanda karşılaştırılınca.

Bağımsız sayaçta fiyat ayrımı yok: fiyat bloklarını da toplam iddiaya katıyor.
Karşılaştırma bu yüzden aletin fiyat DAHİL sayılarıyla yapılmalı — ve **hem
toplam iddia hem kaynaklı sayısı** birlikte kıyaslanmalı. Yalnız toplamlara
bakılırsa 19/25 çıkar; yayınlanan 17/25 ve adı geçen 8 sayfa ancak iki sayı
birlikte kıyaslanınca üretilir:

| karşılaştırma tabanı | birebir tutan | fark |
|---|---|---|
| fiyat dahil (sayacın saydığı gibi) | **17 / 25** | **8** — yayınlanan iddia |
| fiyat ayrı (aletin saydığı gibi) | 11 / 25 | 14 |

İlk denemede ikinci satırı hesaplayıp iddianın yeniden üretilemediğini
sandım; hata bendeydi, iddiada değil. **Ders:** makale "17 of 25" derken hangi
tabanda karşılaştırıldığını yazmıyor. Yazmalı — yoksa doğrulamaya çalışan
okuyucu da aynı yanlış tabanı seçip iddiayı çürütülmüş sanır.

Fiyat dahil tabanda kalan 8 fark: ahrefs.com, aisearch.similarweb.com,
digitalapplied.com, frase.io, llmrefs.com, orchly.ai, seocrawl.ai, writer.com.
README bunları iki nedene bağlıyor (bir uygulamada olan tablo-kredi kuralı ve
ondalık yakalama boşluğu); sayıları yukarıdaki tabloyla tutuyor.
