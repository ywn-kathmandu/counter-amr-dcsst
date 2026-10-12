# Standards and data

## Classifications used

| Standard | How it is used |
|---|---|
| **WHO AWaRe 2025** | The primary classification. Every antibiotic product carries an Access / Watch / Reserve / Not recommended assignment, chosen for the route of administration actually dispensed. 376 AWaRe entries mapped onto 2,869 registered antibiotic products. |
| **WHO ATC** | Determines whether a product is antibacterial, and supplies the therapeutic class shown when a product is not an antibiotic. Classes J01, J04, P01AB, A07AA, G01AA, G01AF, S01AA, S02AA, S03AA, D06A. |
| **WHO DDD** | Reported on the surveillance screen where a molecule has a mapped defined daily dose. |
| **DDA product register** | Brand, composition, strength, dosage form and manufacturer for all 16,831 products licensed in Nepal, from the Department of Drug Administration's public product-information pages, enriched with the classification work described in the README. |
| **ISO 8601** | All dates and timestamps in the export. |

## Scope: why the instrument is self-contained

The study addresses the counter where **no prescription arrives at all** and an antibiotic is
handed over anyway. At that counter there is no prescriber, no patient record, no referral
letter and no dispensing system — the encounter leaves no trace in any health information
system, which is precisely why it is invisible to existing surveillance and why it needs an
instrument of its own.

A self-contained tool is therefore the correct design, not a limitation of one:

- **It creates the record that does not otherwise exist.** The sale is currently unrecorded
  anywhere. The tool is the first point at which it becomes data.
- **It runs where the work happens.** A counter on an intermittent connection cannot wait on
  a remote system, and entry time is itself a study outcome.
- **It collects no patient identifier.** Age is recorded as a band; no name, contact or
  identifier of any kind is taken. There is nothing that could or should be joined to a
  clinical record, which removes the usual reason for interoperability at this point of care.
- **It keeps the data where the study governs it.** Records stay on the device and reach the
  research team by direct export, so custody is explicit and auditable.

The classification layer is where interoperability matters for this work, and it is
standards-based throughout: AWaRe and ATC are the vocabularies in which antimicrobial
consumption is reported internationally, so the exported dataset is directly comparable with
GLASS-AMC and national AMR reporting without any mapping step.

## Export

Five CSV tables, downloadable from the tool, plus a single plain-text backup bundle
containing all five with pharmacy, cluster, export time and build version in its header.

| Table | Grain |
|---|---|
| `transactions` | One row per antibiotic encounter, 69 fields. The analysis table. |
| `products_added` | One row per product added at a counter, with review status. |
| `product_searches` | One row per completed lookup, with outcome and latency. |
| `prompts` | The prompt-library version in force. |
| `daily` | Pharmacy-day rollup. |

`transactions.csv` fits the primary model with no joins and no reshaping.
