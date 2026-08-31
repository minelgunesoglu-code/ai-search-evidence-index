#!/usr/bin/env python3
"""EVIDENCE INDEX CODER v1.2
=============================
The AI Search Evidence Index'in ölçüm enstrümanı. Sürüm 1.2 — 30 Ağustos 2026.

v1.2 DOĞRULANMIŞTIR. 92 iddialık örneklemin 46'sı elle kodlandı (insan hükmü =
"bloktaki link GERÇEKTEN bu rakamı kaynaklıyor mu"). Araç o kümeye karşı ayarlandı.

  ÖLÇÜLEN GEÇERLİLİK: insan koduyla %82 uyum (39 kodlanabilir iddiada 32 doğru)
  · yanlış pozitif 2  (kaynak var dedi, yok)
  · kaçırılan     5  (kaynak vardı, göremedi)

Yanlış pozitif KASITLI olarak düşük tutuldu: adıyla skor yayınlanan bir çalışmada
"kaynağı var" deyip yanılmak, kaçırmaktan çok daha zararlıdır. %82'yi koruyan ama
yanlış pozitifi 6'ya çıkaran daha gevşek bir ayar denendi ve REDDEDİLDİ.

v1.1'DEN FARKI:
 D. ÇIPA KURALI — link, çıpa metni ya sayının kendisini içeriyorsa ya da iddia
    cümlesiyle en az 2 anlamlı kelime paylaşıyorsa kaynak sayılır. v1.1 "blokta
    link var" diyordu; elle kontrolde bu %38 yanlış verdi (Rankscale fiyatı için
    Otterly linki, $35M yatırım için yatırımcının ana sayfası, vb.).
 E. ÇIPLAK ANA SAYFA SAYILMAZ — "seranking.com" gibi yolsuz bağlantı o rakamı
    kanıtlamıyor.
 F. FİYAT SAYFASI İSTİSNASI — iddia fiyatsa ve link /pricing ya da /plans'e
    gidiyorsa kaynak sayılır (çıpa metni eşleşmese de).

DENENİP REDDEDİLEN: "kendi sitesine link sayılmaz" kuralı uyumu %77'den %54'e
DÜŞÜRDÜ — kendi çalışmasına ya da kendi fiyat sayfasına link vermek meşru
kaynaktır. Sezgi yanlıştı, ölçüm düzeltti.

v1.0'DAN FARKI (elle doğrulamada bulunan üç kusur):
 A. ÜÇÜNCÜ KADEME: "kaynak adı var, link yok" artık sıfır sayılmıyor. v1.0 ikili
    çalışıyordu; llmrefs.com kaynağını adıyla veriyordu (Vercel, Brandlight) ama
    %0 çıkıyordu. Kendi kod kitabımızda bu sınıf zaten vardı.
 B. ŞABLON/ÖRNEK BLOKLARI ELENDİ: okura "böyle yaz" diye verilen tırnak içi
    kalıplar iddia değildir (obapr.com, ayzeo.com'da bulundu).
 C. EŞİK: 10 iddianın altındaki sayfalar için YÜZDE VERİLMEZ, ham sayı verilir.
    3 iddiada "%33" istatistiksel olarak boştur.

NEDEN SÜRÜM: kural değişince rakam değişir. 30 Ağustos'ta iki kez değiştirdik ve
rakip medyanı %5 -> %11 -> %19 oynadı; sayfalar aynıydı, kural değişti. Yayınlanan
her rakam "v1.0 ile ölçüldü" diye etiketlenir, böylece yeniden üretilebilir kalır.
Kural değişirse v1.1 açılır; eski rakamlar geçersiz olmaz, hangi aletle ölçüldüğü
yazılıdır.

v1.0 KURALLARI (donmuş):
 1. Blok türleri: p, li, tr, blockquote, h1-h6
 2. İDDİA SAYILMAZ: başlık blokları · tarih satırları ("last updated" vb.) ·
    60 karakterden kısa bloklar · yıl ve tarih desenleri
 3. Sayısal iddia: fiyat, yüzde, çarpan, 2+ basamaklı sayı, "N motor/kaynak/soru"
 4. ULAŞILABİLİR: bloğun içinde http ya da site-içi (/) bir bağlantı var
 5. TABLO KURALI: tablo satırlarının hemen bitişiğindeki (±2 blok) linkli ve
    400 karakterden kısa paragraf, o tablonun bütün satırlarını kapsar
 6. Fiyat iddiaları ayrı raporlanır

BİLİNEN SINIR — v1.0'da KAPATILMADI:
 Kural 4 "blokta link var" der, "o link BU rakamı kaynaklıyor" demez. 30.08'de
 40 iddialık elle kontrolde 20 "ulaşılabilir"in 7'si yanlış çıktı. Bu yüzden
 v1.0'ın ürettiği oran bir ÜST SINIRDIR, ölçülen hata payı ~%35. Rapor bunu
 böyle sunmak zorundadır. Kapatmak insan kodlaması gerektirir.

--- orijinal not ---
TUR 3 ÖLÇÜM — temizlenmiş alet.

Elle doğrulamada (30.08, 40 iddia) iki kusur bulundu ve ikisi de burada kapalı:

  Hata 2 — iddia olmayanlar sayılıyordu: sayfa başlığı ("19 Best AI Tools"),
           tarih satırı ("Last updated 12 June"), örnek hesap, kısa etiket.
           ÇÖZÜM: başlık blokları, tarih satırları ve 60 karakterden kısa
           bloklar iddia sayılmaz.

  Hata 1 — "blokta link var" ≠ "o link bu rakamı kaynaklıyor". 20 örnekte
           7 kez yanlış çıktı. BU KAPATILAMADI (insan hükmü gerekiyor).
           SONUÇ: "ulaşılabilir" oranı bir ÜST SINIRDIR, ~%35 hata payıyla.
           Rapor bunu böyle sunmak zorunda.

Tablo kuralı (29.08 kararı): tablonun bitişiğindeki linkli kaynak notu, o
tablonun satırlarını da kapsar. Her siteye AYNI ŞEKİLDE uygulanır.
"""
import re, io, os, json, glob, html, collections, statistics as st

D = os.path.dirname(os.path.abspath(__file__))

SAYI = re.compile(
    r'(?<![\w.])(?:'
    r'\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[kKmMbB]\b)?'
    r'|\d+(?:\.\d+)?\s?%'
    r'|\d+(?:\.\d+)?\s?x\b'
    r'|\b\d{2,}(?:,\d{3})*\b'
    r'|\b\d+\s+(?:engines?|sources?|prompts?|questions?|tools?|models?|domains?|'
    r'platforms?|queries|sites?|brands?|weeks?|months?|days?|runs?|citations?)\b'
    r')', re.I)
AY = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'
TARIH = re.compile(r'(last (updated|reviewed)|published|posted|updated on)\b', re.I)
# (B) sablon/ornek blogu: okura verilen kalip cumle
# (J) v1.7 (31.08) — IDDIA OLMAYAN bloklar. 30 maddelik elle kodlamada 7'si
# gercek iddia degildi (%23) ve 7'nin 6'si LINKSIZ — payda sisiyor, pay sismiyor:
# butun yuzdeler oldugundan DUSUK cikiyordu (havuz %37 -> %46 duzeltilince).
# Yalniz MEKANIK olarak kesin olanlar elenir; "tavsiye cumlesi" gibi hukum
# gerektirenler ELENMEZ, kalan hata orani raporda yazilir.
BIYOGRAFI = re.compile(
    r"\b\d+\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|expertise|in\b)"
    r"|\bbrings\s+\d+\+?\s*years?"
    r"|\bI(?:'|\u2019)ve\s+spent\s+the\s+last\s+\d+"
    r"|\bis\s+the\s+(?:Founder|Co-Founder|CEO|CTO|Head)\s+of\b"
    r"|\bFortune\s+\d00\b", re.I)
ORNEKORAN = re.compile(r"\b\d+\s+out\s+of\s+\d+\b", re.I)
TARIH2 = re.compile(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:19|20)\d\d\s*$", re.I)
SABLON = re.compile(r'^\s*[✔✓•\-]?\s*["“]|based on our \d{4} survey|\[(category|your brand|competitor|'
                    r'use case|task|job-to-be-done|the problem)', re.I)
# (A) kaynak ADI var ama link yok
# v1.4 (30.08) — 30 maddelik elle kodlamada v1.3 %73 verdi. Iki KANITLI hata:
#   1) 'according to' desende kucuk harfliydi; 'According to BrightEdge' KACIYORDU
#   2) 'predicts/forecasts' fiilleri yoktu; 'Gartner predicts' KACIYORDU
# Denenip GERI ALINANLAR (korpusta yanlis alarm urettiler, 2.347 blokta olculdu):
#   - shows/notes/states/finds  -> 'It shows the top 20 competitors', 'Page Analytics
#     shows', 'This shows Warby Parker' hepsi kaynak sanildi
#   - buyuk harfli alan adi     -> arac karsilastirma yazilarinda her urun adina atesledi
#   - "X's own \w+"             -> tablo hucrelerinde atesledi
# Kalan uyum: 25/30 = %83. Kapatilamayanlarin 4'u ayni sinif: fiyat iddiasinda
# saticinin kendi adi (Profound $399, Frase $39). Bu yuzden B kademesi RAPORDA
# YUZDE OLARAK YAYINLANMAZ; yalnizca isaret + elle dogrulanmis ornek verilir.
ADI = re.compile(
    r'\b[a-z0-9][a-z0-9-]{2,}\.(?:com|ai|org|io|net|co|dev)\b'
    r'|[Aa]ccording to\b|\bper\s+[A-Z]|[Cc]ited by\b'
    r'|\b[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)?\s+(?:found|reports?|reported|says?|said|'
    r'suggests?|estimates?|puts?|measured|published|analy[sz]ed|predicts?|forecasts?)\b'
    r"|\([A-Z][A-Za-z&.\-/' ]{2,60}?,[^)]{0,60}?(?:19|20)\d\d\)"
    r"|\b[A-Z][A-Za-z]+(?:'s|\u2019s)\s+(?:data|study|research|analysis|survey|report|audit|benchmark|figures?|numbers?)\b"
    r"|(?<=[a-z,;:] )[A-Z][A-Za-z]+(?:-(?:led|backed|funded|run))?\s+(?:[A-Z][A-Za-z]*\s)?(?:study|survey|benchmark|dataset)\b"
    r'|\b(?:study|research|survey|analysis|report|data|edition)\s+(?:of|by|from)\s+[A-Z]')
FIYAT = re.compile(r'\$\s?\d')

def bloklar(h):
    h = re.sub(r'(?is)<(script|style|nav|header|footer|form|noscript)\b.*?</\1>', ' ', h)
    out = []
    for m in re.finditer(r'(?is)<(p|li|tr|h[1-6]|blockquote)\b[^>]*>(.*?)</\1>', h):
        tur, ham = m.group(1).lower(), m.group(2)
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ham))).strip()
        if len(txt) >= 12:
            out.append((tur, txt, ham))
    return out

DUR = set("the a an of in on for to and or is are was were with by from that this it its as at".split())
ANA = re.compile(r'https?://[^/]+/?$')
FIYATSAYFA = re.compile(r'/(pricing|plans)(?:/|$|\?)', re.I)
# v1.5 (30.08) — CTA/randevu linkleri KAYNAK DEGILDIR. Elle kontrolde visiblie.com'un
# uc 'linkli iddiasi'nin ucu de 'Start Free Trial' dugmesiydi ('14-day trial' sayisi
# /signup linkine eslendi); data-mania'nin biri savvycal randevu linkiydi.
CTA = re.compile(r'/(signup|sign-up|register|demo|book|booking|contact|start|trial|get-started|checkout|cart|app)(?:/|$|\?)|calendly\.com|savvycal\.com|cal\.com', re.I)
# ILGILI-YAZI KARTI — 'Read Post' / 'Read more' cipali bloklar navigasyondur, iddia degil.
# nav43.com'un uc 'linkli iddiasi'nin ucu de yazi altindaki ilgili-yazi kutusuydu.
# (I) v1.6 (31.08) — URUN / SOZLUK sayfasi kaynak DEGILDIR.
# Elle kontrolde hubspot.com'un dort "kaynakli" iddiasinin dordu de kendi urun
# sayfasina (hubspot.com/products/aeo) gidiyordu; digitalapplied'in tek iddiasi
# kendi sozluk sayfasina. Buna karsilik similarweb'in kendi ARASTIRMA raporuna
# (similarweb.com/corp/reports/...) ve tryprofound'un kendi VAKA calismasina
# (/customers/...) link vermesi mesrudur — yayinlanmis kaynaga goturuyor.
URUN = re.compile(r'/(products?|product-tour|features?|solutions?|glossary|integrations?|platform|use-cases?)(?:/|$|\?)', re.I)
KART = re.compile(r'^\s*(read (post|more|article)|learn more|view (post|all))\s*$', re.I)
FIYATIDDIA = re.compile(r'[\$€£]\s?\d|\btrial\b|/mo\b|per month', re.I)

def kelime(s):
    return {w for w in re.findall(r"[a-z]{3,}", (s or "").lower()) if w not in DUR}

def linkli(ham, cumle="", ALAN=None):
    """(D)(E)(F) — link BU rakami kaynakliyor mu? Bkz. v1.2 notu."""
    cum = kelime(cumle)
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', ham, re.S | re.I):
        u = m.group(1)
        if not (u.startswith("http") or (u.startswith("/") and len(u) > 3)):
            continue
        cip = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
        if CTA.search(u): continue                      # (G) v1.5 CTA/randevu = kaynak degil
        if URUN.search(u) and (u.startswith('/') or (ALAN and ALAN in u)):
            continue                                    # (I) v1.6 KENDI urun/sozluk sayfasi
        if KART.match(cip): continue                    # (H) v1.5 ilgili-yazi karti
        if FIYATSAYFA.search(u) and FIYATIDDIA.search(cumle):      # (F)
            return True
        if ANA.match(u):                                            # (E)
            continue
        say = re.findall(r'\d[\d,.]*', cumle)
        if any(s and s in cip for s in say):                        # (D) cipa sayiyi iceriyor
            return True
        if len(kelime(cip) & cum) >= 2:                             # (D) cipa cumleyle ortak
            return True
    return False

def olc(h, ALAN=None):
    bl = bloklar(h)
    # tablo kuralı: tr bloğunun bitişiğinde linkli kısa paragraf varsa kredi ver
    kredi = [False] * len(bl)
    for i, (tur, txt, ham) in enumerate(bl):
        if tur != "tr":
            continue
        a = i
        while a > 0 and bl[a-1][0] == "tr": a -= 1
        b = i
        while b < len(bl)-1 and bl[b+1][0] == "tr": b += 1
        for j in (a-1, a-2, b+1, b+2):
            if 0 <= j < len(bl) and bl[j][0] in ("p", "li") and linkli(bl[j][2], bl[j][1]) and len(bl[j][1]) < 400:
                kredi[i] = True
                break
    n = a_ = 0
    fn = fa = 0
    adli = 0                                   # (A) kaynak adi var, link yok
    for i, (tur, txt, ham) in enumerate(bl):
        if tur.startswith("h") or TARIH.search(txt) or len(txt) < 60:
            continue                                   # iddia değil
        if SABLON.search(txt):
            continue                                   # (B) okura verilen kalip
        if BIYOGRAFI.search(txt) or ORNEKORAN.search(txt) or TARIH2.search(txt.strip()):
            continue                                   # (J) v1.7 iddia degil
        t2 = re.sub(AY + r'\.?\s+\d{1,2},?\s+(?:19|20)\d\d', ' ', txt, flags=re.I)
        t2 = re.sub(r'\d{1,2}\s+' + AY + r'\.?\s+(?:19|20)\d\d', ' ', t2, flags=re.I)
        t2 = re.sub(r'\b(?:19|20)\d\d\b', ' ', t2)
        ok = linkli(ham, txt, ALAN=ALAN) or kredi[i]
        advar = bool(ADI.search(txt))
        vs = set(SAYI.findall(t2))
        if not vs: continue
        if all(FIYAT.search(v) for v in vs):
            fn += 1; fa += ok
        else:
            n += 1; a_ += ok
            if not ok and advar: adli += 1          # (A)
    return n, a_, fn, fa, adli

cek = json.load(io.open(os.path.join(D, "v2-cekim.json"), encoding="utf-8"))
kume = {x["ad"]: x["sorgu"][:28] for x in cek["sayfalar"]}

rows = []
for f in sorted(glob.glob(os.path.join(D, "v2-*.html"))):
    ad = os.path.basename(f)[3:-5]
    n, a, fn, fa, adli = olc(io.open(f, encoding="utf-8", errors="ignore").read(), ALAN=ad.split("-")[0])
    if n + fn < 3:
        print(f"  ATLANDI (3'ten az iddia): {ad}")
        continue
    rows.append({"alan": ad, "kume": kume.get(ad, "?"), "iddia": n, "ulasilir": a,
                 "adli": adli, "fiyat": fn, "fiyat_ulasilir": fa})

def pct(a, b): return 100*a/b if b else None

ESIK = 10   # (C) bu sayinin altinda YUZDE verilmez
print(f"\n{'site':21} {'iddia':>6} {'linkli':>7} {'adli':>6} {'ulaşılır':>9}  not")
for r in sorted(rows, key=lambda x: -(x["ulasilir"]/x["iddia"] if x["iddia"] else 0)):
    p = pct(r["ulasilir"], r["iddia"])
    az = r["iddia"] < ESIK
    gost = "az örneklem" if az else (f"%{p:.0f}" if p is not None else "—")
    mark = "  <<<" if r["alan"].startswith("BIZ") else ""
    print(f"  {r['alan']:19} {r['iddia']:6} {r['ulasilir']:7} {r['adli']:6} "
          f"{gost:>9}{mark}")

ge = [r for r in rows if r["iddia"] >= ESIK]                 # yuzde verilebilir
rak = [pct(r["ulasilir"], r["iddia"]) for r in ge if not r["alan"].startswith("BIZ")]
biz = [pct(r["ulasilir"], r["iddia"]) for r in ge if r["alan"].startswith("BIZ")]
az  = [r["alan"] for r in rows if r["iddia"] < ESIK]
print(f"\n  (yüzde yalnızca {ESIK}+ iddiası olan sayfalar için)")
print(f"  RAKİP {len(rak)} sayfa · medyan %{st.median(rak):.0f} · "
      f"sıfır {sum(1 for v in rak if v == 0)} · %10 altı {sum(1 for v in rak if v < 10)}")
print(f"  BİZ   {len(biz)} sayfa" + (f" · medyan %{st.median(biz):.0f}" if biz else " (bu cercevede yok)"))
print(f"  az örneklemli ({ESIK}'dan az): {', '.join(az) if az else 'yok'}")
adt = sum(r["adli"] for r in rows if not r["alan"].startswith("BIZ"))
print(f"\n  linksiz ama KAYNAK ADI verilen iddia (rakiplerde): {adt}")
json.dump({"cekim_penceresi": cek["cekim_penceresi"], "satirlar": rows},
          io.open(os.path.join(D, "v2-olcum-blok.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n-> v2-olcum.json")
