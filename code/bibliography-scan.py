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
SNAPS=os.environ.get("SNAPSHOTS")

HEADING = re.compile(r'^\s*(sources?|references?|bibliography|citations?|works cited|'
                     r'further reading|sources? (?:&|and) references?|cited (?:works|sources))\s*:?\s*$', re.I)

def host_of(u):
    m=re.match(r'https?://([^/]+)', u or '')
    return m.group(1).replace('www.','').lower() if m else ''

scored={r['page_id']:r for r in csv.DictReader(open('data/results.csv'))}
log={r['page_id']:r for r in csv.DictReader(open('data/retrieval-log.csv'))}
result=[]
for path in sorted(glob.glob(os.path.join(SNAPS,'v2-*.html'))):
    name=os.path.basename(path)[3:-5]
    if name not in log: continue
    h=io.open(path,encoding='utf-8',errors='ignore').read()
    bls=ins.blocks(h)
    if not bls: continue
    own=host_of(log[name]['url'])
    # look for a sources heading in the last 35% of the page
    cutoff=int(len(bls)*0.65)
    found=None
    for i,(kind,txt,raw) in enumerate(bls):
        if i<cutoff: continue
        if HEADING.match(txt.strip()) or (kind.startswith('h') and HEADING.match(txt.strip())):
            found=i; break
    if found is None:
        result.append({"page_id":name,"bibliography":False}); continue
    # links in the blocks that follow the heading
    internal=external=0; examples=[]
    for kind,txt,raw in bls[found+1:]:
        for m in re.finditer(r'<a[^>]*href="([^"]+)"', raw):
            u=m.group(1)
            if not u.startswith('http'):
                internal+=1; continue
            if host_of(u)==own: internal+=1
            else:
                external+=1
                if len(examples)<3: examples.append(u[:70])
    result.append({"page_id":name,"bibliography":True,"heading":bls[found][1].strip()[:40],
                   "external_links":external,"own_links":internal,"examples":examples})

print(f"{'page':<26}{'scored':>7}  biblio  ext-links")
for r in sorted(result,key=lambda x:(not x['bibliography'],x['page_id'])):
    p=f"{float(scored[r['page_id']]['percent_sourced']):.0f}%" if r['page_id'] in scored else "  —"
    if r['bibliography']:
        print(f"  {r['page_id']:<24}{p:>7}   YES   {r['external_links']:>3} ext · {r['own_links']} own   [{r['heading']}]")
        for u in r['examples']: print(f"      {u}")
    else:
        print(f"  {r['page_id']:<24}{p:>7}   no")
json.dump(result, io.open('/tmp/bibliography-scan.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
