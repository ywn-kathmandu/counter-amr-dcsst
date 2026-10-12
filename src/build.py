#!/usr/bin/env python3
"""Build the DC-SST prototype.

Two outputs from one source:
  index.html  - demo build.  Seeds example traffic, phase switchable, so an
                evaluator can see both states of the trial.
  field.html  - field build. No seeded data, phase fixed by the cluster
                activation date, demonstration controls removed.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent if (HERE.parent / 'data').is_dir() else HERE
DATA = ROOT / 'data' if (ROOT / 'data').is_dir() else HERE

aware  = json.loads((DATA / 'aware.json').read_text())
brands = json.loads((DATA / 'brands.json').read_text())
nonab  = json.loads((DATA / 'nonab.json').read_text())
tpl    = (HERE / 'app.tpl.html').read_text()

def build(mode, out):
    s = (tpl
         .replace("/*BUILD_MODE*/'demo'", f"'{mode}'")
         .replace("/*AWARE_DATA*/[]", json.dumps(aware,  separators=(",", ":"), ensure_ascii=False))
         .replace("/*BRAND_DATA*/[]", json.dumps(brands, separators=(",", ":"), ensure_ascii=False))
         .replace("/*NONAB_DATA*/[]", json.dumps(nonab,  separators=(",", ":"), ensure_ascii=False)))
    out.write_text(s)
    return len(s)

n1 = build('demo',  ROOT / 'index.html')
n2 = build('field', ROOT / 'field.html')

from collections import Counter
print(f"AWaRe entries : {len(aware)}")
print(f"Non-antibiotic: {len(nonab)} brands")
print(f"Brand rows    : {len(brands)}  ({len(set(b['b'] for b in brands))} unique brands)")
print(" ", dict(Counter(b['a'] for b in brands)))
print(f"index.html    : {n1/1024:.0f} KB  (demo build)")
print(f"field.html    : {n2/1024:.0f} KB  (field build)")
