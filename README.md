# DC-SST - Dispensing-Counter Stewardship Support Tool

A counter-level tool for retail pharmacies in Nepal. It answers one question at the point of
sale **is this product an antibiotic, and if so which WHO AWaRe group?** and records the
sale in the order it actually happens.

Built as the measurement instrument for **COUNTER-AMR Nepal**, a pragmatic stepped-wedge
cluster implementation study of antibiotic stewardship at the pharmacy counter
(WHO/TDR call CA26-0034).

> **Research prototype.** Sample data throughout. Not a commercial product, not for clinical
> use, and the clinical prompt wording and red-flag rules are drafts awaiting panel sign-off.

**▶ Live demo (evaluator build):** https://ywn-kathmandu.github.io/counter-amr-dcsst/

There are **two builds from one source**, and the difference matters:

| | `index.html` — evaluator | `field.html` — pharmacy |
|---|---|---|
| Example traffic | Seeded on first run, labelled on every screen | **None.** Starts empty |
| Phase | Switchable, so a reviewer can see both states | **Fixed** by the cluster activation date; inert at the counter |
| Demonstration controls | Present | Removed |

Only `field.html` goes to a pharmacy. The seeded data and the phase switch exist so the
evaluator build can be explored in two minutes, and both are exactly what must not exist in
a baseline.

---

## 90-second tour

1. Open the demo. You land at the counter with a sample pharmacy already configured.
2. Search **`azixon`** → an antibiotic. The dispensing flow opens.
3. Search **`abamol`** → *Not an antibiotic. Nothing to record.* (Paracetamol, analgesic.)
4. Press the **Silent / Advisory** toggle, top right, and repeat step 2.

Step 4 is the study. The difference between those two screens is the entire intervention.

## Why the silent phase shows less

The baseline must record behaviour without changing it. A checklist, an AWaRe badge or a
suggested counselling script displayed during baseline *is itself an intervention*, it
contaminates the very measurement it is supposed to establish.

So in the silent phase the tool displays no AWaRe group, no prompts, no suggested scripts and
no instructional text. The three counselling tick boxes remain, because they *are* the
measurement — but their labels become neutral descriptions of what is being recorded
("whether the number of days was said") instead of advice about what to say. Risk flags are
still **computed and exported**, so the baseline carries them in the data, but they are never
shown. After a cluster is activated, the same encounter shows the group, the prompts and the
suggested wording.

The baseline does still ask what happened — dispensed, referred, or not dispensed for another
reason. Asking is measurement, not advice, and without it every baseline encounter would be
recorded as a sale and a baseline referral would be invisible.

This is verified rather than asserted. `src/verify.js` renders both phases and asserts that
the baseline carries no badge, no script and no instructional label while keeping all three
tick boxes. 82 assertions run across both builds.

## What it does

| | |
|---|---|
| **1 Identify** | 16,831 registered products. Brand, generic, misspelling, or partial name. |
| **2 Advise** | AWaRe group, counselling prompts, red-flag rules - advisory phase only. |
| **3 Refer** | Referral slip when a red flag fires. |
| **4 Record** | 69 fields per encounter, exported as one analysis-ready table. |

The tool never proposes a different molecule for a complaint. Where it suggests alternatives
at all, they are **the same molecule** in another brand or pack, a stock-substitution aid,
not a clinical decision.

## The primary outcome

Frozen in the software as `PO-2026.10.12`, computed per encounter and exported as
`primary_concordant` so the endpoint is not reconstructed at analysis time.

**Population.** Non-prescription antibiotic encounters — the counter where no prescription
arrives and an antibiotic is handed over anyway. Encounters ending in referral or
non-dispensing are included: those are the successes.

**Concordant when all four hold:**

1. Reason for the request recorded
2. Red-flag screening performed
3. Referral made where a red flag was present *(na if none present)*
4. Duration advice **and** safety-net advice given *(na if nothing was dispensed)*

Deliberately excluded: product identification, which measures the tool rather than the
pharmacist, and dosing advice, which is already near-universal. AWaRe group is not a
component — the tool never substitutes a molecule, so it is not judged on doing so.

**Scoring.** Every component is `yes`, `no`, `na` or `unassessed`. Any `no` makes the
encounter discordant. All applicable `yes` makes it concordant. An `unassessed` component
with no failure leaves it **unscorable** — never silently concordant. `primary_unassessed`
and `outcome_unscorable` export per row so missingness is visible; the surveillance screen
uses complete cases.

```r
glmer(primary_concordant ~ exposure + factor(period_month) +
        (1 | cluster/pharmacy_id),
      data = subset(d, primary_eligible == 1),
      family = binomial)
```

Report marginal standardised probabilities alongside the odds ratio.

**Key secondary:** duration advice given, a single binary with the largest headroom at
baseline. Others available from the same table without derivation: safety-net advice,
red-flag screening, appropriate referral, the proportion of encounters not ending in a
dispensing, AWaRe Access share, entry seconds, lookup success and unresolved-product rate.

## Status

A working build, tested with pharmacists at the counter. The register is classified and
auditable, the analysis export is complete, and 60 assertions run against both builds.

The study proposed around this instrument is what takes it from counter testing into routine
implementation and produces the effectiveness evidence. Prompt wording and red-flag rules are
drafts pending panel sign-off, and are labelled as such inside the tool.

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
molecule of a fixed-dose combination, so matching on it misclassifies every FDC and in the
reassuring direction. Each component is resolved separately against ATC, the AWaRe list, and a
curated molecule map (`src/molmap.py`), which is also where the auditable judgement calls live.

Of 16,831 products, 11,604 carry an ATC code in the source register. The remaining 5,227 are
resolved as: 1,268 non-allopathic (by product system), 559 combinations (component-level),
3,446 single-molecule (curated map), 245 unresolvable.

AWaRe groups are assigned **per route** - minocycline is Watch orally and Reserve by
injection, and a retail pharmacy sells the oral form.

Antituberculosis agents: WHO AWaRe excludes them by
design, so they carry their own group and raise a stop-level prompt pointing to the nearest
DOTS centre. Veterinary antibacterials are flagged and exported in their own column, so they
can be included in or excluded from the primary outcome by analysis choice rather than by
accident.

## Build

Self-contained HTML, one file per build. No build step is required to run either; `index.html`
is the evaluator build that GitHub Pages serves, and `field.html` is the pharmacy build.

To rebuild after editing the template or the data:

```bash
python3 src/build.py          # src/app.tpl.html + data/*.json -> index.html AND field.html
node src/verify.js            # 82 assertions across both builds
```

`src/rebuild.py` regenerates `data/brands.json` and `data/nonab.json` from the source register
workbook (not included - see below).

## Data provenance and licensing

- **Product register** - built from the Department of Drug Administration's public product
  information for Nepal, enriched with the classification work described above.
- **AWaRe classification** - WHO AWaRe 2025 (376 entries).
- **Therapeutic classes for ATC-blank products** - curated, in `src/molmap.py`.

Code is MIT (see `LICENSE`). The classification work in `data/` — AWaRe assignment by route,
the brand–generic crosswalk, the molecule classification — is released under CC BY 4.0.

`STANDARDS.md` sets out the classifications used (WHO AWaRe 2025, WHO ATC, WHO DDD, ISO 8601)
and why a self-contained instrument is the right design for a counter where no prescription
arrives and the encounter leaves no trace in any health information system.

## Data handling and backup

Records are held in the browser's local storage on the device. There is no account, no server
and no automatic upload; nothing is transmitted anywhere. Data reaches the study only through
the manual export.

The export screen downloads each table as CSV, or all five as a single plain-text backup file
named with the pharmacy code and the date. The field procedure is a download at the end of
each working day, handed to the research team through the agreed channel. Clearing the
browser's site data destroys the records, and they cannot be recovered.

Prompt wording and red-flag rules remain drafts, labelled as such inside the tool, and
require panel sign-off before any field use.

## Use of AI assistance
AI assistance (Anthropic's Claude, Gemini) was used in building this repository for:

- writing and refactoring the application code and the test suite;
- processing the national drug register, parsing compositions, resolving fixed-dose
  combinations component by component, and reconciling spelling variants against the WHO
  AWaRe list;
- drafting the curated molecule classification in `src/molmap.py`;
- drafting documentation.

All clinical content - the counselling prompts, the red-flag rules and the molecule-level
antibacterial calls - is verified by the study's clinical
pharmacologist, microbiologist, pathologist and clinicians. Those decisions are recorded
product by product in `DC-SST_panel_decision_log.xlsx` precisely so that they are checked by
people rather than trusted because software produced them.

Study design, research questions, outcome definitions and all methodological decisions are
the responsibility of the named investigators.

## Citation

See `CITATION.cff`.
