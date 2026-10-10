# ET04 — Organic deposit growth: the peer that "grew fastest" bought its growth

| Field | Value |
|---|---|
| Domain | Banking strategy / FP&A / peer benchmarking |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 03 · Bridge between two totals (2019 → 2024 deposits, organic vs acquired) |
| Core technique | Pro-forma (merger-adjusted) base construction from three event sources: charter transformations, holding-company relationship changes, and branch ownership moves |
| Trap family (honest data) | Only one of three acquisition channels captured; non-transitive merger chains; intra-family charter consolidations double counted |
| Primary sources | FDIC Summary of Deposits (SOD); FFIEC NIC bulk data (Attributes, Relationships, Transformations); FDIC BankFind Suite |

## 1. The real-world project

A regional bank's strategy office benchmarks itself against in-state peers at the **holding-company** level. The
board asked one question: *which peer grew deposits organically the fastest between June 2019 and June 2024?* The
analyst pulled SOD totals by holding company for both years and ranked growth. The winner was a peer that had
completed four acquisitions. The CFO sent it back.

## 2. The business decision (one deterministic recommendation)

**Which of the state's 15 largest holding companies (by June 2024 in-state deposits) had the highest organic deposit
growth from 2019-06-30 to 2024-06-30, and what was that growth rate?**

Method fixed in the benchmarking standard:

* Unit of analysis: top-tier holding company (`RSSDHCR`; stand-alone banks are their own top tier) — in-state branch
  deposits only (`STALPBR` = state).
* Organic growth = D₂₀₂₄ ÷ PF₂₀₁₉ − 1, where the pro-forma base PF₂₀₁₉ = 2019 in-state deposits of every branch office
  the holding company **controls in 2024**, measured at its 2019 owner, plus 2019 deposits of branches it controlled in
  2019 but sold or closed (closures stay in the base; sales leave it).
* "Controls in 2024" is established through all three channels: (1) charter transformations (predecessor charters
  discontinued into a family bank, transitively), (2) holding-company relationship changes (a bank that joined the
  family without losing its charter), and (3) branch-only purchases (a branch `UNINUMBR` that moved from another
  `CERT` with no charter event).
* Mergers between two banks already in the same family during the window are **not** acquisitions.
* `DEPSUMBR` is in thousands of dollars.

## 3. Why this gets overlooked in real projects

* Analysts know about "merger adjustment" but implement it with the Transformations table only. Whole-bank
  acquisitions that keep the target's charter (common for multi-bank holding companies) never appear there; they live in
  the Relationships table as a change of parent.
* Branch sales are invisible in both NIC tables; only the stable branch identifier `UNINUMBR` in SOD reveals them.
* Merger chains (A buys B after B bought C) require transitive closure; direct-predecessor joins miss C.
* After a holding company collapses two of its own charters into one, a bank-level transformation looks like an
  acquisition and gets added to the base twice.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–6 | `sod_2019.csv` … `sod_2024.csv` | CSV | ~85k branches each | FDIC Summary of Deposits | U.S. Gov public domain | Branch deposits, ownership, `UNINUMBR` |
| 7 | `CSV_ATTRIBUTES_ACTIVE.csv` | CSV | ~100k entities | FFIEC NIC bulk download | Public domain | Entity type, names |
| 8 | `CSV_ATTRIBUTES_CLOSED.csv` | CSV | ~100k | FFIEC NIC | Public domain | Discontinued charters |
| 9 | `CSV_RELATIONSHIPS.csv` | CSV | ~100k+ | FFIEC NIC | Public domain | Parent–offspring with start/end dates, control flags |
| 10 | `CSV_TRANSFORMATIONS.csv` | CSV | ~30k | FFIEC NIC | Public domain | Predecessor→successor, transformation code, date |
| 11 | `bankfind_institutions.json` | JSON | ~25k | FDIC BankFind Suite API | Public domain | CERT ↔ RSSD bridge |
| 12 | `nic_data_dictionary.pdf` | PDF | — | Federal Reserve / FFIEC | Public domain | Code meanings (verify transformation codes) |
| 13 | `sod_definitions.pdf` | PDF | — | FDIC | Public domain | Field meanings, units |
| 14 | `benchmark_standard.pdf` | PDF | — | Task author (strategy-office standard) | — | Rules in §2 |

## 5. Deterministic solution path

1. Build a CERT↔RSSD bridge; assign each 2019 and 2024 branch to its top-tier holding company using Relationships
   active on 2019-06-30 and 2024-06-30 respectively.
2. Compute D₂₀₂₄ per holding company (in-state).
3. For each holding company, collect its 2024 `UNINUMBR` set; look up each branch's 2019 deposits wherever it sat
   in 2019 (this captures channels 1–3 at branch grain at once). Add 2019 deposits of its own 2019 branches that
   closed (no 2024 record) — closures remain organic; exclude 2019 branches that appear under another family in 2024.
4. Cross-check channel attribution: classify every non-family 2019 owner as (1) charter transformation, (2) relationship
   change, or (3) branch purchase, so the bridge has one bar per channel.
5. Compute organic growth; rank; report winner, runner-up and the raw-growth leader.
6. Bridge for winner and raw-growth leader: D₂₀₁₉ (as owned) → + charter mergers → + whole-bank acquisitions → + branch
   purchases → − branch sales → organic change → D₂₀₂₄.

## 6. The traps

**Trap A — raw growth.** The acquisitive peer ranks first.

**Trap B — transformations only.** Whole-bank acquisitions kept as separate charters and branch purchases inflate
organic growth; rank order among the top three changes.

**Trap C — direct predecessors only.** A chained acquisition's 2019 base is missed.

**Trap D — bank-level logic at HC level.** Intra-family consolidations are double added to the base, depressing one
peer's organic growth.

**Trap E — dropping closed branches from the base.** Overstates organic growth for peers that consolidated networks.

## 7. Why the data is honest

SOD and NIC are the regulators' official records; every event is real and dated. The pro-forma method is standard
practice. Difficulty comes from stitching three event channels together correctly.

## 8. Draft task prompt (prose)

> The board wants to know which in-state peer grew deposits organically the fastest from June 2019 to June 2024, at
> the holding-company level, using our benchmarking standard. Using the Summary of Deposits files and the NIC
> structure data in the folder, rank the fifteen largest holding companies by organic growth and tell me who wins and
> by how much over second place. Build `organic_growth_bridge.png` with two waterfalls side by side — the winner and the
> peer with the highest raw growth — each walking from June 2019 deposits to June 2024 through charter mergers,
> whole-bank acquisitions, branch purchases, branch sales and organic change. Then a two-page `peer_growth_memo.pdf`
> with the ranked table (2019 deposits, pro-forma base, 2024 deposits, raw and organic growth for all fifteen), the
> recommendation, and a sentence on which acquisition channel, if ignored, would change the winner.

## 9. Deliverables

* `organic_growth_bridge.png` (two waterfalls).
* `peer_growth_memo.pdf` (ranked table + decision).

## 10. Where 25+ rubric criteria come from

* 15 organic growth rates and ranks; winner and runner-up gap.
* Bridge bars (5 per waterfall × 2).
* Identification of the channel whose omission flips the winner; raw-growth leader named.

## 11. Golden-output checklist

* All three acquisition channels captured; transitive chains; intra-family events neutral; closures kept in base.
* Winner, rate and gap stated; bridges reconcile exactly to SOD totals.

## 12. Build notes (scope tuning)

* Choose a state where at least one top-15 holding company made a whole-bank acquisition that kept the charter and
  another bought branches only (detect via `UNINUMBR` changing `CERT` with no Transformations record).
* Verify that raw-growth and organic-growth winners differ, and that Trap B alone changes the winner.
* Transformation and relationship codes: copy the exact code list from the NIC dictionary at download time.
