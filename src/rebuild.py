#!/usr/bin/env python3
"""Rebuild brands.json + nonab.json from the Nepal register.

Resolution order for every product:
  1. own ATC code                      - the register said so
  2. component-level composition match - every molecule tested, not just the first
  3. curated molecule map (molmap)     - for molecules the register never ATC-codes
  4. Product System                    - Ayurvedic / homeopathic / Unani / veterinary
  5. cannot confirm                    - flagged for the research panel

AWaRe group is taken per route (oral vs injection) rather than by worst case.
"""
import sys, json, re, pickle
import pandas as pd
from collections import Counter, defaultdict
sys.path.insert(0, '/tmp/claude-0/-home-claude/b8c7761f-ccb1-5b09-9a02-2498ecd06ee7/scratchpad')
import molmap

SP = '/tmp/claude-0/-home-claude/b8c7761f-ccb1-5b09-9a02-2498ecd06ee7/scratchpad/'
OUT = '/home/claude/dcsst/'

df = pickle.load(open(SP + 'full.pkl', 'rb'))
aw = json.load(open(SP + 'aware.json'))

# ---------------------------------------------------------------- AWaRe index
RANK = {'Access': 0, 'Watch': 1, 'Reserve': 2, 'Not recommended': 3}

def nz(s):
    s = str(s).lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'[^a-z+ ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.replace('ph', 'f')

def route_of(name):
    n = str(name).lower()
    if 'inject' in n or 'parenteral' in n or 'infusion' in n or 'iv' == n.strip():
        return 'inj'
    if 'oral' in n or 'rectal' in n:
        return 'oral'
    return 'any'

def yi(s):
    """Second spelling key: amoxycillin / amoxicillin, oxytetracycline / oxitetracycline."""
    return s.replace('y', 'i')

AW_SINGLE = defaultdict(dict)     # base -> {route: group}
AW_COMBO = {}                     # frozenset(molecules) -> group
for a in aw:
    base = nz(a['n'])
    r = route_of(a['n'])
    if '+' in base:
        parts = frozenset(x.strip() for x in base.split('+') if x.strip())
        AW_COMBO[parts] = a['g']
        AW_COMBO[frozenset(yi(x) for x in parts)] = a['g']
    else:
        for k in {base, yi(base)}:
            prev = AW_SINGLE[k].get(r)
            if prev is None or RANK.get(a['g'], 9) > RANK.get(prev, 9):
                AW_SINGLE[k][r] = a['g']

INJ_FORMS = ('inject', 'vial', 'ampoule', 'infusion', 'parenteral')

# normalised key -> the AWaRe list's own spelling, so one molecule is never counted
# twice because the register writes amoxycillin where WHO writes amoxicillin.
AW_CANON = {}
for a in aw:
    base = nz(a['n'])
    if '+' in base:
        continue
    disp = re.sub(r'\(.*?\)', '', a['n']).strip()
    AW_CANON.setdefault(base, disp)
    AW_CANON.setdefault(yi(base), disp)

def canonical(mol):
    key = nz(molmap.AWARE_SYN.get(mol, mol))
    return AW_CANON.get(key) or AW_CANON.get(yi(key))

def aware_group(mol, form):
    """Group for one molecule, choosing the route variant that matches the form."""
    key = nz(molmap.AWARE_SYN.get(mol, mol))
    d = AW_SINGLE.get(key) or AW_SINGLE.get(yi(key))
    if not d:
        return None
    is_inj = any(w in str(form).lower() for w in INJ_FORMS)
    for r in (('inj', 'any', 'oral') if is_inj else ('oral', 'any', 'inj')):
        if r in d:
            return d[r]
    return None

# ---------------------------------------------------------------- composition parsing
SALTS = (r'\b(hydrochloride|hcl|dihydrochloride|sodium|potassium|calcium|magnesium|'
         r'sulphate|sulfate|phosphate|maleate|fumarate|tartrate|succinate|citrate|'
         r'besylate|mesylate|acetate|trihydrate|dihydrate|monohydrate|anhydrous|'
         r'as extended release pellets|extended release|er|sr|micronised|micronized|'
         r'base|bp|usp|ip|eq to|equivalent to|stearate|palmitate|lactobionate|'
         r'nitrate|bromide|chloride|iodide|oxide|carbonate|gluconate|orotate|'
         r'pivoxil|axetil|proxetil|estolate|propionate|valerate|'
         r'dipropionate|furoate|acetonide|xinafoate|bromhydrate|hydrobromide)\b')

STEREO = r'^(s|r|l|d|dl|rs|es|levo|dextro)\s+'

def norm_mol(s):
    s = str(s).lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'[\d.]+\s*(mg|mcg|g|gm|ml|iu|%|lac|million|units?)\b', ' ', s)
    pre = re.sub(r'\s+', ' ', re.sub(r'[^a-z ]+', ' ', s)).strip()
    s = re.sub(SALTS, ' ', s)
    s = re.sub(r'[^a-z ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # a name made only of salt words (sodium acetate, potassium citrate) empties out:
    # keep the original rather than losing the product.
    if len(s) < 3:
        s = pre
    return s


def variants(m):
    """Spellings to try, most faithful first. 'l asparaginase' must win over
    'asparaginase'; 's amlodipine' must fall through to 'amlodipine'."""
    out = [m]
    st = re.sub(STEREO, '', m).strip()
    if st and st != m:
        out.append(st)
    for part in (m.split()[-1], m.split()[0]):
        if part and part not in out:
            out.append(part)
    return out

def components(comp):
    s = str(comp)
    if s.strip() in ('', 'nan', '---', '--', '-'):
        return []
    parts = re.split(r'\s*\+\s*|\s*&\s*|\s*,\s*(?=[A-Za-z]{4})', s)
    return [n for n in (norm_mol(p) for p in parts) if len(n) >= 3]

def blank(s):
    return s.isna() | (s.astype(str).str.strip()
                       .isin(['', 'nan', 'None', '-', 'NA', 'N/A', '---', '--']))

# ---------------------------------------------------------------- learn from register
has = df[~blank(df['ATC Code'])]
m2atc, m2cat = defaultdict(Counter), defaultdict(Counter)
for comp, atc, cat in zip(has['Composition (Generic)'], has['ATC Code'], has['ATC Category']):
    cs = components(comp)
    if len(cs) != 1:
        continue
    m2atc[cs[0]][str(atc).strip().upper()] += 1
    if pd.notna(cat):
        m2cat[cs[0]][str(cat).strip()] += 1
MOL_ATC = {m: c.most_common(1)[0][0] for m, c in m2atc.items()}
MOL_CAT = {m: c.most_common(1)[0][0] for m, c in m2cat.items() if c}

ABX_PRE = ('J01', 'J04', 'P01AB', 'A07AA', 'G01AA', 'G01AF', 'S01AA', 'S02AA', 'S03AA', 'D06A')
def is_abx(a):
    return bool(a) and any(str(a).upper().startswith(p) for p in ABX_PRE)

SYS_LABEL = {'AYURVEDIC': 'Ayurvedic preparation', 'HOMEOPATHY': 'Homeopathic preparation',
             'UNANI': 'Unani preparation', 'VETERENARY': 'Veterinary product'}

def tidy_cat(c):
    c = re.sub(r'^[A-Z]\d{2}\s*-\s*', '', str(c)).strip()
    return c

# ---------------------------------------------------------------- classify
brands, nonab = [], []
tally, why_tally = Counter(), Counter()
panel_rows = []

for _, r in df.iterrows():
    brand = str(r['Brand / Product Name']).strip()
    if not brand or brand.lower() == 'nan':
        continue
    sysraw = str(r['Product System']).strip().upper() if pd.notna(r['Product System']) else ''
    atc = str(r['ATC Code']).strip().upper() if pd.notna(r['ATC Code']) else ''
    form = r['Dosage Form'] if pd.notna(r['Dosage Form']) else ''
    strength = str(r['Strength']).strip() if pd.notna(r['Strength']) else ''
    cs = components(r['Composition (Generic)'])
    is_vet = sysraw == 'VETERENARY'

    # --- resolve every component
    abx_mols, groups, classes, unres, vet_abx = [], [], [], [], False
    for m in cs:
        vs = variants(m)
        a = next((MOL_ATC[v] for v in vs if v in MOL_ATC), None)
        g = next((x for x in (aware_group(v, form) for v in vs) if x), None)
        ov = next((molmap.ABX_GROUP_OVERRIDE[v] for v in vs
                   if v in molmap.ABX_GROUP_OVERRIDE), None)
        in_extra = next((v for v in vs if v in molmap.ABX_EXTRA), None)
        cls_hit = next((molmap.CLASS[v] for v in vs if v in molmap.CLASS), None)
        # a curated non-antibacterial class wins over a loose stereo-stripped
        # antibiotic match, so 'l asparaginase' is not read as an antibiotic.
        known_abx = (is_abx(a) or g is not None or in_extra is not None) and not (
            cls_hit and cls_hit != 'Antibacterial' and not is_abx(a)
            and g is None and in_extra is None)
        if known_abx:
            abx_mols.append(m)
            if m in molmap.VET_ONLY or in_extra in molmap.VET_ONLY:
                vet_abx = True
            if g:
                groups.append(g)
            elif ov and ov[0] not in ('adjunct',):
                groups.append(ov[0])
            elif ov and ov[0] == 'adjunct':
                pass
            else:
                groups.append('Unclassified')
        elif cls_hit:
            classes.append(cls_hit)
        elif a:
            c = tidy_cat(next((MOL_CAT[v] for v in vs if v in MOL_CAT), ''))
            if c:
                classes.append(c)
        else:
            unres.append(m)

    own_abx = is_abx(atc)

    # --- whole-composition AWaRe combination match (catches FDCs AWaRe names directly)
    combo_g = None
    if len(cs) > 1:
        combo_g = AW_COMBO.get(frozenset(nz(molmap.AWARE_SYN.get(m, m)) for m in cs))

    if own_abx or abx_mols:
        # an antibiotic: decide the group
        tb = [m for m in abx_mols if m in molmap.TB_MOLS] or \
             ([1] if atc.startswith('J04') and not any(m not in molmap.TB_MOLS for m in abx_mols) else [])
        if combo_g:
            grp, basis = combo_g, 'AWaRe combination entry'
        elif tb and len(abx_mols) <= len(tb):
            grp, basis = 'Antituberculosis', 'AWaRe excludes antituberculosis agents'
        elif len(abx_mols) > 1:
            grp, basis = 'Needs panel decision', f'{len(abx_mols)} antibacterials combined'
        elif classes and abx_mols:
            grp, basis = 'Needs panel decision', 'antibacterial combined with a non-antibacterial'
        elif groups:
            grp = sorted(set(groups), key=lambda g: -RANK.get(g, -1))[0]
            basis = 'AWaRe single molecule'
        elif own_abx:
            grp, basis = 'Unclassified', 'antibacterial ATC, not on the AWaRe list'
        else:
            grp, basis = 'Unclassified', 'antibacterial molecule, not on the AWaRe list'
        if unres and grp not in ('Needs panel decision',):
            grp, basis = 'Needs panel decision', f'unresolved component: {unres[0]}'

        if abx_mols:
            gname = canonical(abx_mols[0]) or abx_mols[0].title()
        else:
            gname = str(r['Generic INN Name']).title() if pd.notna(r['Generic INN Name']) else ''
        rec = {'b': brand, 'g': gname, 'a': grp, 's': strength, 'f': str(form), 'c': atc}
        if is_vet or vet_abx:
            rec['v'] = 1
        brands.append(rec)
        tally['antibiotic'] += 1
        why_tally[basis] += 1
        if grp in ('Needs panel decision', 'Unclassified', 'Antituberculosis'):
            panel_rows.append({'brand': brand, 'composition': str(r['Composition (Generic)']),
                               'form': str(form), 'group': grp, 'basis': basis})
        continue

    # --- not an antibiotic: find the best label we can defend
    if sysraw in SYS_LABEL and sysraw != 'VETERENARY':
        label, u, basis = SYS_LABEL[sysraw], 0, 'non-allopathic system'
    elif atc and pd.notna(r['ATC Category']):
        label, u, basis = tidy_cat(r['ATC Category']), 0, 'own ATC'
    elif classes:
        label, u, basis = next(c for c in classes if c), 0, 'curated molecule class'
    elif atc:
        label, u, basis = '', 0, 'own ATC, no category'
    elif is_vet and not unres:
        label, u, basis = 'Veterinary product', 0, 'veterinary, components resolved'
    else:
        label, u, basis = ('Veterinary product' if is_vet else ''), 1, 'cannot confirm'

    if is_vet and label and 'eterinary' not in label:
        label = label + ' · veterinary'
    rec = {'b': brand, 'g': str(r['Composition (Generic)'])[:60], 'c': label, 'u': u}
    nonab.append(rec)
    tally['not-antibiotic' if not u else 'cannot-confirm'] += 1
    why_tally[basis] += 1

# ---------------------------------------------------------------- write
json.dump(brands, open(OUT + 'brands.json', 'w'), separators=(',', ':'), ensure_ascii=False)
json.dump(nonab, open(OUT + 'nonab.json', 'w'), separators=(',', ':'), ensure_ascii=False)
json.dump(panel_rows, open(SP + 'panel_review.json', 'w'), indent=1, ensure_ascii=False)

print('=== product classification ===')
for k, v in tally.most_common():
    print(f'  {k:18s} {v:6d}')
print(f'  {"TOTAL":18s} {sum(tally.values()):6d}')
print()
print('=== basis ===')
for k, v in why_tally.most_common():
    print(f'  {v:6d}  {k}')
print()
print('=== antibiotics by AWaRe group ===')
for k, v in Counter(b['a'] for b in brands).most_common():
    print(f'  {k:24s} {v:5d}')
print(f'  veterinary-flagged       {sum(1 for b in brands if b.get("v")):5d}')
print()
print(f'brands.json : {len(brands)} rows, {len(set(b["b"] for b in brands))} unique brands')
print(f'nonab.json  : {len(nonab)} rows, cannot-confirm {sum(1 for n in nonab if n["u"])}')
print(f'panel review: {len(panel_rows)} products')
