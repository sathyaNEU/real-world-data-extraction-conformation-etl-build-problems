# Judge verdict, task136 round 2

Cross-batch check: not run. Other task folders and prior reports were forbidden, so no near-duplicate finding is recorded either way.

**Verdict:** DETERMINISTIC (with one residual literal-reading risk, below). The solution blocks reproduce, so SOLUTION_WRONG does not apply.

**Disposition:** APPROVE. No repair is needed and no rerun. Pinning the rate basis in NPP-114 4.2 would hand over the stump, so I do not recommend it.

**Why:** Every graded figure reproduces from the shipped files. YRB27 is forced only through the one-line rate basis in NPP-114 4.1 and 4.2, "the quantity the rate is expressed per". The text never names that quantity. The data separates the candidates decisively, and every stable basis gives the same call and the same one-decimal figures. Per-letterbox, per-owner-occupied-house and per-house-without-PV rates swing 5x to 7x across the seven campaigns. Rates per first application swing about 9 percent. Residual risk (Gate C/E, `underspecified_objective`): a strictly literal reader could say the quantity is unpinned and the letter supplies only letterbox counts. I do not fail the gate, because the letterbox-type bases are demonstrably unreasonable on the shipped history.

## Evidence (recomputed from the bundle)

| Value | Result | Source |
|---|---|---|
| Connected capacity at 31 Aug 2026: YRB27 17,938 kW; YRB24 4,637 kW | Reproduced exactly | applications CSV, with legacy inverter kW × count for the 9,159 migrated rows, placed by the network model feeder |
| Trend: YRB27 1,852 kW/yr; YRB24 498 kW/yr | Reproduced | FY23-24 to FY25-26 increases at 30 June, less program systems at first connection (only YRB21 and YRB26 carry program deductions) |
| Pooled rate 505 / 431 = 1.172 | Reproduced | per-campaign ratios 1.03 to 1.35 |
| New-suburb first applications: Wattleview 209; Bindarra Waters 52 | Reproduced | rates roll land use 02 / R1, via the xref and the network model |
| Average new inverter, FY2025-26: YRB27 6.97 kW; YRB24 6.50 kW | Reproduced | applications CSV |
| Bulk-buys: Wattleview 1.71 MW → 1.7; Bindarra Waters 0.40 MW → 0.4 | Reproduced | |
| Excess at 2029 vs hosting capacity: YRB27 1.91 → 1.9; YRB24 1.40 → 1.4; third is YRB22 at 1.21; gap 0.5 | Reproduced | hosting capacity PDF, 2029 column |
| DER Register table (sites, FY2025-26 first lodged, kW, kWh, all 8 feeders) | Reproduced exactly | see rules below |

The register table follows these rules, all derivable from the files:
- NMI cut to 10 characters.
- Builder's temporary NMIs mapped to their replacement through the reallocations file.
- Feeder taken from the network model.
- Earliest registration across all connections, decommissioned included, decides the FY.
- Two-inverter connections lodged before July 2024 counted once.
- Sungrow SBR stack counted once.

Rounded values sit clear of the .5 boundaries (smallest margin: 746.02 kWh → 750).

The register rules are corroborated by the applications file, not just by naming conventions.
- Two-inverter rows before July 2024 carry exactly 2× the model nameplate (350 connections). Later ones carry 1× (74 connections).
- Sungrow battery stacks match the application's battery_kwh with first-row-only 168 of 168 times, and sum-of-rows 0 times.
- BYD and GoodWe stacks match with sum-of-rows every time (280 and 159).

**Literal-reading forks (where the text is silent):**

- **Rate basis (the stump).** All of the following keep YRB27, 1.9 MW above hosting capacity, and 1.7 / 0.4 MW for the bulk-buys at one decimal:
  - first applications from all NMIs in the suburb (1.86, 1.38; 1.66 / 0.38 MW);
  - first applications counting withdrawn ones (1.91, 1.37);
  - first connections in the prior 12 months (1.92, 1.39);
  - 2-year and 6-month windows (1.88, 1.39 and 1.88, 1.43).

  These baskets are not true competing answers.
  - Per homes letterboxed (2026 letter counts 6,240 and 5,240) gives bulk-buys of 0.7 MW (Wattleview) and 0.8 MW (Bindarra Waters). The call becomes **YRB24** at 1.8 MW above hosting capacity, with YRB22 second at 1.2.
  - Per owner-occupied house gives 1.1 and 1.2 MW, and YRB24 wins at 2.2.
  - Per owner-occupied house without PV gives 1.1 and 2.0 MW, and YRB24 wins at 3.0.
  - The letterbox, owner-occupied and no-PV bases have coefficient of variation (CV) of the campaign ratios of 0.61 to 0.72. The first-application bases have CV 0.08 to 0.12.
- **Program deduction.** Ignoring NPP 3.2's program deduction moves YRB21 above YRB24 (1.53 vs 1.40) and changes the runner-up. That is an explicit stated rule, so it is fine.
- **Hidden fork in the table (feeder).** The register's own `feeder` column is stale. It matches feeder-at-application, not current supply, and disagrees with the model on 591 rows. "Supplies" and NPP 3.1 point to the model, but a solver using the register column gets different counts, for example YRB23 1,904 vs 1,713. Moderate risk, resolved by "supplies".
- **Hidden fork in the table (first lodged).** "First lodged" could mean the earliest of the active connections only. That gives YRB21 120 vs 82. The site-level earliest registration, decommissioned included, is the natural reading and the golden's. Moderate risk, resolved by "first lodged" at site level.
- **Other readings tested.** Placement by feeder at application, and gross new-only capacity, leave the call at YRB27 and the runner-up at YRB24.

## Files/Hygiene
**PASS.**
- 15 files in 3 formats: CSV, XLSX and PDF. There is one PDF letter, two PDF reports, and several CSVs above 18,000 rows (the largest is 52,359 rows).
- Distractors present: home_battery_rebate_approvals, feeder_peak_demand_forecast and the summary-sheet bases.
- The extracts carry real-system mess: 11-character NMIs, reallocated NMIs, legacy migration, multi-row stacks, a stale register feeder and an old-NMI manifest.
- No authoring or benchmark disclosure found; dates are coherent.
- Minor, non-stump: the hosting capacity PDF says its customer counts come from a 30 June 2026 model, but they equal the 31 August 2026 model counts exactly. This is cosmetic and not exclusion-level.

## Stump power
Strong. The lure is per homes letterboxed: the summary table and the 2026 letter both supply it, and it yields a tidy answer, YRB24 at 1.8 MW. A capable solver who does not back-test the rate basis files the wrong call. The honest-data trap needs a constructed base: first applications in the 12 months before sign-ups, from the rates roll, xref and model. Rule-discovery is not involved; it is computation. The sanity of the data test (0.09 vs 0.6+ CV) means a careful solver can find it.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

The reported homes-letterboxed figures are accurate, and no stated conclusion is wrong. The difficulty is selecting the rate basis by out-of-history stability, plus heavy conformation; on clean data it would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`

- Domain test: distribution planning forecasts rooftop PV against hosting capacity at minimum demand and builds a program uptake rate. Swapping in another field's nouns breaks it.
- Layer 1: NMI reallocations, legacy migration, 11-character NMIs, and a stale register feeder.
- Layer 2: choosing the stable estimand for program uptake, which is analysis (estimand choice).
- Easy route: apply the pooled rate per homes letterboxed. The call becomes YRB24, 1.8 MW above, with bulk-buys of 0.7 and 0.8 MW.

## Fix
**none** (prompt, files and solution stand). If a strict-literal reviewer objects to NPP-114 4.2, the only repair is to name a basis in the NPP, which would remove the stump, so I recommend leaving it.

## Disposition (main thread, 2026-10-14)

APPROVE, shipped as round 2. No graded figure, no prompt sentence and no file under `target/` moved: the final
rebuild's 15 pack files, both goldens, `metadata.json`, `generator/figures.json` and `target.zip` (sha256
ac3475bd...) are byte-identical to the judged pack, and `freeze.py check --mode determinism` passes.

- **Rate basis (the stump).** Left unnamed in NPP-114 4.2, as the judge recommends. The design note's fork table
  carries it: SF15 (the estimator), SF16 to SF20 (every pool and contact basis, priced by the seven campaigns' scatter,
  0.61 to 0.80), and the first-application readings SF11 (dated by connection), SF12 (every residential NMI), SF13
  (24 and 36 months, and now six months), SF24 (withdrawn counted) and SF25 (the hazard forms), each asserted in
  `checks.py`. Six months at a yearly rate (not in the round-2 corridor, measured here) keeps the call, the runner-up,
  both excesses and both bulk-buys at one decimal (YRB27 1.863, YRB24 1.435, Bindarra Waters 0.435, Wattleview 1.668)
  and puts the gap at 0.428, a bin under the golden's 0.5; recorded as a residual, asserted as the same call, not
  closed (a filed window would name the basis).
- **The register's stale feeder (Ask 1 to 4).** New row SF27: the prompt's "sites it supplies" and the dictionary
  (the network model's feeder is the "Feeder supplying the NMI at 31 August 2026", the extract's only "added by
  Mirrabee's extraction"), asserted; the stamp misses all eight feeders on Ask 1 (YRB23 1,904, YRB27 2,830).
- **First lodged at site level (Ask 2).** New row SF28: the prompt counts sites ("how many of them") and the dictionary
  dates each AC connection and keeps a replaced one as Decommissioned, asserted; the active-only reading misses all
  eight (YRB21 120, YRB27 278).
- **The assessment's customer counts (cosmetic).** No change. The report (issued 24 July 2026) counts NMIs energised
  by its 30 June 2026 model; no NMI was energised, abolished or moved between feeders in July or August 2026 (the
  latest first energisation is 14 June 2026), so the 30 June and 31 August counts are the same set. Asserted in
  `checks.py` against the network model and the world.
- **Gate G and Gate H.** method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect
  no; domain pass, layers pass, decisive_step analytical.
