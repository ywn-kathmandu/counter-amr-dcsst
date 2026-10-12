# Data

| File | Rows | What it is |
|---|---|---|
| `brands.json` | 2,869 | Registered antibiotic products: brand, generic, AWaRe group, strength, form, ATC. `v: 1` marks veterinary. |
| `nonab.json` | 13,962 | Every other registered product, with a therapeutic class label. `u: 1` means the class could not be confirmed. |
| `aware.json` | 376 | WHO AWaRe 2025 entries. |

## Provenance

- Product data derives from Department of Drug Administration (DDA) Nepal product
  registration records, enriched. The source workbook is not redistributed here.
- AWaRe groups are from the WHO AWaRe classification 2025.
- Therapeutic classes for products with no ATC code in the source register are curated in
  `../src/molmap.py` and are pending panel sign-off.

## Caveats

- `a: "Needs panel decision"` (246 products) — an antibacterial combined with a
  non-antibacterial, or several antibacterials in one product. AWaRe classifies neither.
- `a: "Unclassified"` (149) — antibacterials genuinely absent from the AWaRe list, mostly
  topical and veterinary-only agents.
- `a: "Antituberculosis"` (20) — AWaRe excludes TB agents by design.
- `u: 1` in `nonab.json` (245) — the source register records no composition and no ATC code.

See `../DC-SST_panel_decision_log.xlsx` for all of the above, product by product.

## Licence

CC BY 4.0, subject to confirmation of redistribution rights for the DDA-derived register.
See `../PUBLISHING_CHECKLIST.md`.
