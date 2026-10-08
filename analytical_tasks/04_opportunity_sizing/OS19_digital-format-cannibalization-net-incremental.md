# OS19 — More e-book licences, more reading? Net of the print checkouts they replace

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Cannibalisation in multi-channel products (app versus web, streaming versus physical, new SKU versus existing) when sizing the gain from expanding one channel |
| Domain | Public libraries / digital media |
| Task shape | 03 · Bridge between two totals (gross digital checkouts gained from added licences → net incremental circulation after print substitution; the budget split) |
| Core method | Title-level panel: titles that gained a digital edition (first month with e-book or audiobook checkouts after ≥ 12 months of print-only circulation) versus matched print-only titles (publication year band, prior print circulation); difference-in-differences on digital and physical checkouts; substitution rate = −Δphysical ÷ Δdigital |
| Analytical stump | Counting all extra digital checkouts as added reading ignores that many patrons would have borrowed the print copy. Comparing titles before/after purchase without controls also picks up the title's natural popularity decay. Net incremental circulation determines the budget split |
| Primary sources | Seattle Public Library "Checkouts by Title" (monthly checkouts by title and format, Seattle Open Data) |

## 1. The real-world situation

A library system is deciding how to split next year's collection budget between print copies and e-book/audiobook licences. The digital
team sized the benefit of more licences as the extra digital checkouts after past licence purchases. The print team argued those checkouts
partly replaced print loans.

## 2. The decision (one deterministic recommendation)

**The net incremental checkouts per $1,000 for digital licences, the substitution rate, and the budget split rule outcome (shift 10% of print
budget to digital if net digital per $ > print per $).**

Rules (collections memo):

* Data: monthly checkouts by title and material type, 2019–2023 (title-level, both print and digital formats aggregated by normalised title per
  the memo's key).
* Digital-edition events: the first month a title records e-book or audiobook checkouts, provided it had ≥ 12 consecutive months of print
  checkouts and no digital checkouts before; events in 2021–2022 (derived from the data itself).
* Controls: titles without events matched on publication year band, prior-6-month digital and print checkouts (nearest neighbour, 1:1).
* DiD over 6 months before vs after: Δdigital, Δphysical (treated − control).
* Substitution rate s = −Δphysical ÷ Δdigital; net incremental per event = Δdigital + Δphysical.
* Per $1,000: net incremental ÷ licence cost (memo); print per $: from the memo's print circulation per copy.
* Rule: shift if net digital per $ > print per $.

## 3. Why capable analysts get it wrong

* Gross channel gains are the natural metric for the channel team.
* Substitution is visible only in the other channel.
* Titles purchased are often rising or falling in popularity; controls are needed.
* Title normalisation across formats must be consistent.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Checkouts_by_Title.csv` (2019–2023 extract) | CSV | ~25M | Seattle Open Data (Seattle Public Library) | Public domain / Seattle open data terms | Monthly checkouts by title, format |
| 2 | `title_key_rules.json` | JSON | — | Task author | — | Normalised title key |
| 3 | `digital_edition_events.csv` | CSV | ~3k | Derived from the checkouts file by the memo's rule | Same as source | Treatment events |
| 4 | `collections_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `digital_team_gross_sizing.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 6 | `matching_spec.json` | JSON | — | Task author | — | Matching rules |
| 7 | `did_check_titles.json` | JSON | ~5 | Task author | — | Hand-checked titles |
| 8 | `cost_assumptions.json` | JSON | — | Task author | — | Licence and print costs |

## 5. Deterministic solution path

1. Build the title-month panel by format with normalised keys.
2. Derive digital-edition events; identify treated titles; match controls.
3. DiD for digital and physical; substitution; net per event.
4. Per-$ comparison; rule; bridge from gross to net.

## 6. Wrong paths (method errors, not misreadings)

**A — gross digital gains.** Overstated.

**B — before/after without controls.** Popularity trends confounded.

**C — physical checkouts ignored.** No substitution measured.

**D — title keys inconsistent across formats.** Mismatched panel.

## 7. Why the stump is analytical, not semantic

Keys, matching and DiD are specified. The trap is cannibalisation in incremental sizing.

## 8. Draft task prompt (prose)

> Should we shift budget from print to digital licences? Estimate net incremental checkouts from past digital-edition additions with the matched
> design in the collections memo. Provide `cannibalisation_bridge.csv` (gross digital, substitution, net), `did_event_plot.png`, and a one-page
> `budget_split.pdf`.

## 9. Deliverables

* `cannibalisation_bridge.csv`, `did_event_plot.png`, `budget_split.pdf`.

## 10. Where 25+ rubric criteria come from

* Treated and control counts; Δdigital, Δphysical; s; per-$ values; rule; 6 monthly event-time points; check titles.

## 11. Golden-output checklist

* Panel construction; event selection; matching; DiD windows; substitution; rule.

## 12. Build notes (scope tuning)

* Confirm substitution ≥ 30% so the gross and net per-$ comparisons fall on opposite sides of the print benchmark.
