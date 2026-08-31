# Kodlayıcılar arası güvenilirlik — 31 Ağustos 2026

## Yöntem

İki bağımsız kodlayıcı, kör kodlama:

- **Kodlayıcı 1 (Claude):** 30 maddeyi kodladı ve kodları **önceden mühürledi**
  (`kor-kod-CLAUDE-1-30.json`, sha256 kayıtlı, 30 Ağustos)
- **Kodlayıcı 2 (site sahibi):** aynı maddelerden, **kodu hiç görülmemiş** 12
  tanesini bağımsız kodladı (31 Ağustos)

Konuşma sırasında kodu ifşa edilmiş 18 madde **kasıtlı olarak dışarıda
bırakıldı** — onlar artık kör sayılamaz. Kalan 12 madde kullanıldı.

Kodlayıcı 2'ye yalnızca blok metni ve ölçülen değer verildi; makinenin hükmü,
kodlayıcı 1'in kodu ve link durumu gösterilmedi. *(Bloklarda link olmadığı
mekanik olarak önceden doğrulanmıştı, o boyut karar dışıydı.)*

## Sonuç

| | |
|---|---|
| n | **12** |
| Uyum (Po) | **11/12 = %92** |
| Şansa bağlı uyum (Pe) | 0,583 |
| **Cohen's κ** | **0,800** |

Landis & Koch ölçeğinde *substantial* — 0,81'lik *almost perfect* eşiğinin
hemen altında.

## Tek ayrışma — ve ortaya çıkardığı kod kitabı boşluğu

**Madde 10** (`industry-lens.com`):

> "GEO went from a fringe idea to a **22,000**-search-a-month category in 2026."

| Kodlayıcı | Kod |
|---|---|
| Claude | **Y** (kaynak yok) |
| Site sahibi | **A** (kaynak adı var) |

Bloğun devamında *"IndustryLens tracks ten of them"* geçiyor — yani sayfa
**kendi adını** anıyor.

**Kod kitabı bu durumu düzenlemiyor:** *bir yayıncının kendi adını vermesi
"kaynak adlandırma" sayılır mı?*

Bu, kodlamadan **önce** karara bağlanmalıydı. Karar makalede açıkça yazılacak
ve bu ayrışma örnek olarak verilecek.

## Mühür yöntemi hakkında bir düzeltme

Mührü doğrularken hash **uyuşmadı**. İnceleme sonucu: kodlar değişmemişti;
mühür alınırken sözlük anahtarları **tamsayı**, dosyadan okununca **metin**
oluyordu ve `sort_keys` farklı sıralıyordu. Aynı veri, farklı sıra, farklı hash.

Tamsayı anahtarla yeniden hesaplanınca mühür **birebir tuttu**
(`0fa1d0bb…6070`).

**Ders:** doğrulanamayan bir mühür, mühür değildir. Bundan sonra hash almadan
önce anahtarlar tek biçime çevrilecek. Bu olay raporda yazılacaktır — bir
doğrulama adımının kendisinin kusurlu çıkması, saklanacak değil, yazılacak
bir şeydir.

## Rapora girecek hâli

> Kodlama güvenilirliği iki bağımsız kodlayıcıyla ölçüldü. Birinci kodlayıcının
> kodları, ikincisi kodlamadan önce şifrelenerek mühürlendi. Örtüşen 12 maddede
> uyum %92, **Cohen's κ = 0,80**. Tek ayrışma, kod kitabında düzenlenmemiş bir
> durumdan kaynaklandı: bir yayıncının kendi adını anmasının "kaynak
> adlandırma" sayılıp sayılmayacağı.

---

## Ayrışmanın çözümü — 31 Ağustos, tartışma sonrası

**Kodlayıcı 2 (site sahibi), madde 10 için yazdığı `A` kodunun soruyu yanlış
okumaktan kaynaklandığını, gerçek hükmünün `Y` olduğunu bildirdi.**

**κ yine de DEĞİŞMEZ ve 0,80 olarak raporlanır.** Gerekçe: "yanlış okudum" ile
"diğer kodlayıcının cevabını görünce fikrim değişti" ayrımı **dışarıdan
doğrulanamaz** — çoğu zaman kodlayıcının kendisi de ayırt edemez. Bu yüzden
güvenilirlik, kodlayıcıların **ilk kaydedilen** kodlarıyla hesaplanır.

Düzeltilmiş kodla κ = 1,00 çıkardı. Onu raporlamak iki sebeple yanlış olurdu:
kaydedilmiş veriyi tartışma sonrası değiştirmek olurdu, ve 12 maddede
mükemmel uyum zaten şüphe uyandırırdı. **0,80 hem gerçek hem savunulabilir.**

**Raporlanacak hâli:** tartışma öncesi uyum **%92, κ = 0,80**; tek ayrışma
tartışmayla çözüldü ve kod kitabına kural olarak eklendi.

### KURAL K (31.08.2026 — kodlamadan sonra eklendi, bu açıkça yazılacaktır)

> Yayıncının **kendi adını** anması kaynak adlandırma sayılmaz — ancak
> belirli, tanımlanmış bir çalışmaya işaret ediyorsa sayılır.

| Örnek | Kural K |
|---|---|
| "IndustryLens tracks ten of them" | **sayılmaz** — okuyucuyu bir belgeye götürmüyor |
| "Similarweb's *2026 Generative AI Brand Visibility Index*" | **sayılır** — adı olan belirli çalışma |
| "We analyzed 700,000+ conversations from ChatGPT.com (Oct–Dec 2025)" | **sayılır** — ne ve ne zaman ölçüldüğü yazılı |

Ölçüt değişmedi: **okuyucu gidip bakabiliyor mu?**

### Kural K'nin etkisi

Kural yalnızca **B kademesini** (adı var, link yok) ilgilendirir; A kademesi
link tabanlıdır ve etkilenmez. B zaten yüzde olarak yayınlanmıyor, bu yüzden
tabloya etkisi yoktur — etkisi, seçtiğimiz **B örneklerindedir**:

- `hubspot.com` için verdiğimiz "(HubSpot, January 2026)" örneği **Kural K
  gereği düşer** — kendi adı, belirli bir çalışma değil
- `tryprofound.com` için verdiğimiz "We analyzed 700,000+ conversations…
  (Oct–Dec 2025)" örneği **kalır** — tanımlı ve tarihli
