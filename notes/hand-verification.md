# Elle doğrulama — tur 5 (30 Ağustos 2026, 20:04 UTC)

Adı verilecek her sayfanın "linkli" sayılan iddiaları **tek tek okundu.**
Amaç: makinenin verdiği her hükmü, sayfa adıyla yayınlanmadan önce insan onaylasın.

## 1. "%0" çeken üç sayfa — sıfır gerçek mi

Bir sayfaya haksız yere sıfır vermek, yanlış pozitiften daha ağırdır. Üçü de
gövdedeki bütün dış linkleri sayılarak kontrol edildi.

| Sayfa | Dış link | Ne çıktı | Hüküm |
|---|---|---|---|
| `llmrefs.com` | **0** | gövdede hiç dış link yok | %0 **doğru** |
| `ayzeo.com` | 8 | hepsi font / CDN / sosyal paylaşım | %0 **doğru** |
| `obapr.com` | 10 | 5 paylaşım düğmesi, font, LinkedIn + **3 satıcı linki** | aşağıya bak |

### `obapr.com` — kuralın belirleyici olduğu yer

Sayfa üç fiyat iddiası taşıyor ve üç satıcıyı da linkliyor:

- "Otterly.AI … Pricing: ~$99–299/month" → `otterly.ai` **(ana sayfa)**
- "Profound … Pricing: Custom enterprise" → `tryprofound.com` **(ana sayfa)**
- "AIClicks.io … Pricing: ~$79–199/month" → `aiclicks.io` **(ana sayfa)**

Kural (E) ana sayfa linkini kaynak saymaz: okuyucuyu fiyatın yazdığı yere
götürmüyor. Bizim kendi sayfamız `otterly.ai/pricing`'e link veriyor, o götürüyor.

Ayrım savunulabilir, ama **obapr'ın skorunu doğrudan belirliyor.** Raporda
kural bu örnekle birlikte açıkça yazılacak.

## 2. Kuralların kime ne kadar dokunduğu — tam sayım

Üç eleme kuralı (CTA/randevu, ana sayfa, ilgili-yazı kartı) her sayfada kaç
link düşürüyor:

| Sayfa | Dış link | CTA | Ana sayfa | Kart | Elenen |
|---|---|---|---|---|---|
| **BIZ-cited** | 11 | 0 | 0 | 0 | **0** |
| **BIZ-geo** | 3 | 0 | 0 | 0 | **0** |
| **BIZ-tools** | 21 | 0 | 0 | 0 | **0** |
| **BIZ-track** | 11 | 0 | 0 | 0 | **0** |
| data-mania.com | 42 | 2 | 24 | 0 | 26 |
| aiclicks.io | 22 | 0 | 17 | 0 | 17 |
| dageno.ai | 19 | 0 | 5 | 0 | 5 |
| evertune.ai | 5 | 0 | 3 | 0 | 3 |
| obapr.com | 4 | 0 | 3 | 0 | 3 |
| usegrowthos.com | 5 | 3 | 0 | 0 | 3 |
| istudiosmedia.com | 3 | 0 | 2 | 0 | 2 |
| xseek.io | 3 | 1 | 1 | 0 | 2 |
| llmpulse.ai | 7 | 1 | 0 | 0 | 1 |
| industry-lens.com | 25 | 0 | 1 | 0 | 1 |
| visiblie.com | 1 | 1 | 0 | 0 | 1 |
| aitoolssme.com, ayzeo, frase, nav43, semrush, useomnia | — | 0 | 0 | 0 | **0** |

**Bizim dört sayfamızdaki 46 dış linkten hiçbiri elenmiyor.**

Kurallar yapı olarak taraflı değil — bir kayıt düğmesi gerçekten kaynak
değildir. Ama **etkisi tek yönlü.** Bu tablo raporda yayınlanacak ki okuyucu
kuralın sonucu ne kadar belirlediğini kendisi görebilsin.

Ayrıca: bu kurallar **rakip sayfalar okunurken bulundu**, kendi sayfalarımız
okunurken değil.

## 3. Sayfa sayfa okunan A kademesi

| Sayfa | Makine | Elle okununca |
|---|---|---|
| `visiblie.com` | 3 linkli | **üçü de "Start Free Trial" düğmesi** → düzeltildi, 0 |
| `nav43.com` | 5 linkli | **ikisi "Read Post" kartı** → düzeltildi, 3 |
| `data-mania.com` | 9 | biri savvycal randevu linki → düzeltildi, 8 |
| `useomnia.com` | 7 | biri `/demo` düğmesi → 6. Kalanlar gerçek: G2, Microsoft Clarity, Forrester |
| `usegrowthos.com` | 3 | ikisi gerçek dış kaynak (TechCrunch, Gartner), biri kendi blogu |
| `industry-lens.com` | 24 | çoğu gerçek dış link (peec.ai/pricing, ahrefs.com/blog, tryprofound.com…). Site haber toplayıcı olduğu için yapısal olarak avantajlı — raporda belirtilecek |
| `llmpulse.ai` | 8 | kendi sözlüğü/fiyat sayfası + kendi çalışması. Meşru öz-atıf |
| `xseek.io` | 1 | arXiv GEO makalesi — gerçek akademik atıf |
| `BIZ-tools` | 31 | 21 dış linkin hiçbiri ana sayfa değil; hepsi belirli sayfalara |
| `BIZ-cited` | 18 | okunan 9'un 9'u dış: searchengineland, ahrefs, arxiv |
| `BIZ-geo` | 22 | çoğu kendi çalışmamıza öz-atıf — 30.08'de beşi kopuktu, düzeltildi |
| `BIZ-track` | 7 | 5'i satıcı fiyat sayfası, 3'ü BrightEdge |

## Kalan iş

- B kademesi için her sayfaya elle doğrulanmış birer örnek
- Az örneklemli sekiz sayfa (10'dan az iddia) yüzdesiz kalacak; adları anılacaksa
  onların da linkleri okunmalı

## 4. Sayfa sonu kaynakçası — aracın en büyük kalan kusuru

Ölçüm **blok bazlıdır**: bir rakamın kaynaklandığı sayılması için linkin o
bloğun içinde olması gerekir. Künyelerini akademik biçimde **sayfa sonunda**
toplayan bir sayfa, bu ölçüde hiç kaynak vermemiş gibi görünür.

Bütün sayfalar tarandı. Üç sayfada sayfa sonu künyesi var:

| Sayfa | Ölçülen A% | Künye | Linkli |
|---|---|---|---|
| **`ayzeo.com`** | **%0** | **9** | **0** |
| `xseek.io` | %4 | 2 | 1 |
| `obapr.com` | %0 | 1 | 1 |

### `ayzeo.com` — yayınlamadan önce yakalanan en ağır haksızlık

Sayfanın sonunda dokuz künyelik bir kaynakça var, hiçbiri linkli değil:

1. BrightEdge Research (2025). *ChatGPT Brand Mentions vs. Citations.*
2. Frase.io (2025). *Are FAQs and FAQ Schemas Important to AI Search, GEO and AEO?*
3. Averi (2025). *Schema Markup for AI Citations.*
4. SingleGrain (2025). *How E-E-A-T SEO Builds Trust in AI Search Results.*
5. **Reuters (2024).** *Reddit in AI content licensing deal with Google.*
6. **Reuters (2023).** *Associated Press, OpenAI partner…*
7. **Associated Press News (2023).** *OpenAI to start using news content from News Corp.*
8. Generative AI Pub (2024). *Stack Overflow Partners With OpenAI.*
9. Previsible (2025). *LLMs Are Transforming Search But…*

Ayrıca gövdede `Princeton-led GEO study` ve `Aggarwal, P. … (2024). GEO:
Generative Engine Optimization. KDD '24` gibi künyeli atıflar var.

Bu sayfayı yalnızca **"%0"** diye yayınlamak yanlış beyan olurdu. Okuyucu bu
künyelerle kaynağa ulaşabilir — birçok hyperlinkten daha kolay.

### `xseek.io` — "Sources & References" bölümü

Beş girdilik bir kaynak bölümü var; dördü linkli (arXiv GEO makalesi,
seranking.com, kendi çalışmaları). Ama künyeler **rakamların yanında değil,
sayfa sonunda** toplandığı için blok bazlı ölçü bunları gövdedeki iddialara
bağlayamıyor. Ölçülen A değeri %4 kalıyor.

### Karar

**A yüzdesi değişmez** — ölçtüğü şey satır içi ulaşılabilirlik ve bu geçerli
bir ölçüdür. Ama tabloya **kaynakça sütunu eklenir** ve her sayfa için
"sayfa sonu künyesi: N tane, M'si linkli" bilgisi yayınlanır.

Bu ekleme mekaniktir, yorum gerektirmez, ve tek başına A'ya bakan bir okuyucunun
`ayzeo.com` ve `xseek.io` hakkında yanlış sonuca varmasını engeller.
