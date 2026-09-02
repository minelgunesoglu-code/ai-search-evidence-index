#!/usr/bin/env python3
"""End-of-page bibliography scan — the known blind spot of block-unit measurement.

The instrument judges each block on its own. A page that collects its sources in a
list at the BOTTOM scores low here even though it does cite them. This scan looks
for that: a sources heading in the last third of the page, followed by external
links. Every hit must still be read by hand — the heading alone proves nothing.

Run:  SNAPSHOTS=<dir> python3 code/bibliography-scan.py
"""
import re, io, os, glob, json, csv, sys, importlib.util
spec=importlib.util.spec_from_file_location("ins","code/measure.py")
ins=importlib.util.module_from_spec(spec); spec.loader.exec_module(ins)
ANLIK=os.environ.get("SNAPSHOTS")

BASLIK = re.compile(r'^\s*(sources?|references?|bibliography|citations?|works cited|'
                    r'further reading|sources? (?:&|and) references?|cited (?:works|sources))\s*:?\s*$', re.I)

def alan_adi(u):
    m=re.match(r'https?://([^/]+)', u or '')
    return m.group(1).replace('www.','').lower() if m else ''

puanlanan={r['page_id']:r for r in csv.DictReader(open('data/results.csv'))}
log={r['page_id']:r for r in csv.DictReader(open('data/retrieval-log.csv'))}
sonuc=[]
for yol in sorted(glob.glob(os.path.join(ANLIK,'v2-*.html'))):
    ad=os.path.basename(yol)[3:-5]
    if ad not in log: continue
    h=io.open(yol,encoding='utf-8',errors='ignore').read()
    bl=ins.bloklar(h)
    if not bl: continue
    kendi=alan_adi(log[ad]['url'])
    # son %35'lik dilimde kaynak basligi ara
    esik=int(len(bl)*0.65)
    bulundu=None
    for i,(tur,txt,ham) in enumerate(bl):
        if i<esik: continue
        if BASLIK.match(txt.strip()) or (tur.startswith('h') and BASLIK.match(txt.strip())):
            bulundu=i; break
    if bulundu is None:
        sonuc.append({"page_id":ad,"bibliography":False}); continue
    # basliktan sonraki bloklardaki linkler
    ic=dis=0; ornek=[]
    for tur,txt,ham in bl[bulundu+1:]:
        for m in re.finditer(r'<a[^>]*href="([^"]+)"', ham):
            u=m.group(1)
            if not u.startswith('http'): 
                ic+=1; continue
            if alan_adi(u)==kendi: ic+=1
            else:
                dis+=1
                if len(ornek)<3: ornek.append(u[:70])
    sonuc.append({"page_id":ad,"bibliography":True,"heading":bl[bulundu][1].strip()[:40],
                  "external_links":dis,"own_links":ic,"examples":ornek})

print(f"{'sayfa':<26}{'puanli':>7}  kunye  dis-link")
for r in sorted(sonuc,key=lambda x:(not x['bibliography'],x['page_id'])):
    p=f"%{float(puanlanan[r['page_id']]['percent_sourced']):.0f}" if r['page_id'] in puanlanan else "  —"
    if r['bibliography']:
        print(f"  {r['page_id']:<24}{p:>7}   VAR   {r['external_links']:>3} dis · {r['own_links']} ic   [{r['heading']}]")
        for u in r['examples']: print(f"      {u}")
    else:
        print(f"  {r['page_id']:<24}{p:>7}   yok")
json.dump(sonuc, io.open('/tmp/kunye-sonuc.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
