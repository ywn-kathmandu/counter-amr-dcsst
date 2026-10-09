# DC-SST — Dispensing-Counter Stewardship Support Tool

A counter-level tool for retail pharmacies in Nepal. It answers one question at the point of
sale — **is this product an antibiotic, and if so which WHO AWaRe group?** — and records the
sale in the order it actually happens.

Built as the measurement instrument for **COUNTER-AMR Nepal**, a pragmatic stepped-wedge
cluster implementation study of antibiotic stewardship at the pharmacy counter
(WHO/TDR call CA26-0034).

> **Research prototype.** Sample data throughout. Not a commercial product, not for clinical
> use, and the clinical prompt wording and red-flag rules are drafts awaiting panel sign-off.

**▶ Live demo:** *(set once GitHub Pages is enabled — Settings → Pages → Deploy from branch `main`, folder `/`)*

---

## 90-second tour

1. Open the demo. You land at the counter with a sample pharmacy already configured.
2. Search **`azixon`** → an antibiotic. The dispensing flow opens.
3. Search **`abamol`** → *Not an antibiotic. Nothing to record.* (Paracetamol, analgesic.)
4. Press the **Silent / Advisory** toggle, top right, and repeat step 2.

Step 4 is the study. The difference between those two screens is the entire intervention.

## Why the silent phase shows less

The baseline must record behaviour without changing it. A checklist, an AWaRe badge or a
suggested counselling script displayed during baseline *is itself an intervention* — it
contaminates the very measurement it is supposed to establish.

So in the silent phase the tool records and displays nothing: no AWaRe group, no prompts, no
scripts. Risk flags are still **computed and exported** (so the baseline carries them in the
data) but never shown. After a cluster is activated, the same sale shows the group, the
prompts and the suggested wording.

This is verified rather than asserted: `src/verify.js` renders both phases and asserts zero
badges and zero scripts in silent.

## What it does

| | |
|---|---|
| **1 Identify** | 16,831 registered products. Brand, generic, misspelling, or partial name. |
| **2 Advise** | AWaRe group, counselling prompts, red-flag rules — advisory phase only. |
| **3 Refer** | Referral slip when a red flag fires. |
| **4 Record** | 62 fields per sale, exported as one analysis-ready table. |

The tool never proposes a different molecule for a complaint. Where it suggests alternatives
at all, they are **the same molecule** in another brand or pack — a stock-substitution aid,
not a clinical decision.

## The register

Every product licensed in Nepal, so *"is this an antibiotic?"* has a real answer rather than
a shrug.

| | Products |
|---|---|
| Antibiotic | 2,869 |
| Not an antibiotic (classified) | 13,717 |
| Cannot confirm | 245 |

The 245 are products for which the source register records **no composition and no ATC code**.
Nothing can be resolved from the data, so the tool says so and asks the pharmacist to read the
strip.

**Resolution is component-level.** The register's generic-name field holds only the first
molecule of a fixed-dose combination, so matching on it misclassifies every FDC — and in the
reassuring direction. Each component is resolved separately against ATC, the AWaRe list, and a
curated molecule map (`src/molmap.py`), which is also where the auditable judgement calls live.

Of 16,831 products, 11,604 carry an ATC code in the source register. The remaining 5,227 are
resolved as: 1,268 non-allopathic (by product system), 559 combinations (component-level),
3,446 single-molecule (curated map), 245 unresolvable.

AWaRe groups are assigned **per route** — minocycline is Watch orally and Reserve by
injection, and a retail pharmacy sells the oral form.

Antituberculosis agents are **not** filed as "unclassified": WHO AWaRe excludes them by
design, so they carry their own group and raise a stop-level prompt pointing to the nearest
DOTS centre. Veterinary antibacterials are flagged and exported in their own column, so they
can be included in or excluded from the primary outcome by analysis choice rather than by
accident.

## Open decisions

`DC-SST_panel_decision_log.xlsx` is every classification call the source register did not make
itself — 415 products and 53 molecule-level judgements — for sign-off by the study's clinical
pharmacologist, microbiologist, pathologist and clinician.

Sheet 4 (molecule calls) is the one to check first: an error there propagates to every brand
containing that molecule.

## Build

Single self-contained HTML file. No build step required to run it; `index.html` is the built
artefact and GitHub Pages serves it directly.

To rebuild after editing the template or the data:

```bash
python3 src/build.py          # src/app.tpl.html + data/*.json  ->  index.html
node src/verify.js            # 30 assertions over the built file
```

`src/rebuild.py` regenerates `data/brands.json` and `data/nonab.json` from the source register
workbook (not included — see below).

## Data provenance and licensing

- **Product register** — derived from Department of Drug Administration (DDA) Nepal product
  registration data, enriched. The source workbook is not redistributed here.
- **AWaRe classification** — WHO AWaRe 2025 (376 entries).
- **Therapeutic classes for ATC-blank products** — curated, in `src/molmap.py`, pending panel
  sign-off.

Code is MIT (see `LICENSE`). The derived data files in `data/` are published under
CC BY 4.0 **subject to confirmation of redistribution rights for the DDA-derived register** —
see `PUBLISHING_CHECKLIST.md`.

## Status

Prototype. Not externally validated. Prompt wording and red-flag rules are drafts, labelled as
such inside the tool, and require panel sign-off before any field use.

## Use of AI assistance

Declared so that reviewers and reusers can weigh it.

AI assistance (Anthropic's Claude) was used in building this repository for:

- writing and refactoring the application code and the test suite;
- processing the national drug register — parsing compositions, resolving fixed-dose
  combinations component by component, and reconciling spelling variants against the WHO
  AWaRe list;
- drafting the curated molecule classification in `src/molmap.py`;
- drafting documentation, including this README.

All clinical content — the counselling prompts, the red-flag rules and the molecule-level
antibacterial calls — is **draft pending verification** by the study's clinical
pharmacologist, microbiologist, pathologist and clinician. Those decisions are recorded
product by product in `DC-SST_panel_decision_log.xlsx` precisely so that they are checked by
people rather than trusted because software produced them.

Study design, research questions, outcome definitions and all methodological decisions are
the responsibility of the named investigators.

## Citation

See `CITATION.cff`.
