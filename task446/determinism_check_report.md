# determinism-check report, task446 (architecture 2, loop 1), 2026-10-11

Run note: one isolated judge thread (general-purpose, Sonnet, medium) spawned by the main session under the determinism-check contract (the judge agent in this runtime cannot spawn): the judge system prompt verbatim, the submission's graded blocks and a fresh unzip of target.zip (cut d1696c6) as its only readable path, the literal reading first. Its verdict.md follows verbatim.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate H:** domain pass, layers pass, decisive_step analytical

## Spec gates (main session)
17 files, 6 formats, largest file ews_entity_signals_2022-09_to_2026-09.csv at 125,317 rows, 2 distractors named in metadata.json only, 2 deliverables, every ask with unit and rounding, target.zip 17 members matching target/ (H7).

## Gate G reconciliation
Card and design note: method_or_model_selection (the basis chosen by the filed leave-one-cohort-out test); the thread reads the same. No mismatch.

## Judge thread verdict.md

# Verdict (task 446)

## Literal reading
Executed CRM-07 v3.1 word for word on the shipped files.
- 4.1/4.2 book and outcome: group active on register at 30 Sep (start <= date, end blank or > date), not on an open watch-list case at that date. Books 846/871/889/902/913 (2022-26); arrivals 75/43/36/47 (2022-25). Boundary variants (>= instead of >) change nothing (no placed/removed/ended dates fall on 30 Sep).
- 2.2/3.2 membership and flags: master group_id (customers with blank group placed via LEI) plus GLEIF ULTIMATELY/DIRECTLY_CONSOLIDATED_BY chains in force at the date. Flagged counts 119/98/95/104 (2022-25), 165 (2026).
- 5.2 is silent on which bases compete, so I enumerated every pairing of 4.3's rates plus a flat rate and ran the filed leave-one-cohort-out test on each (largest miss as share of cohort arrivals):
  - capture + false-alarm (prior-shift inversion on the cohort's own flagged share): 1.57% (misses -0.2, -1.6, +0.5, +1.1). 2026 expectation 133.04.
  - hit + miss: 40.6%. 2026 expectation 72.9.
  - hit + capture: 35.6%. 2026 expectation 79.7.
  - capture + miss: 58.4%. flat reach rate: 55.6%. hit + FA: 352%.
  - The filed test picks capture/FA by a margin of 25x. No tie, no second basis wins.
- 6.1 exposure: limit version latest with effective_from before 2026-09-30T23:00Z (end of 30 Sep UK/BST, per 1.3), facilities with start <= 30 Sep and maturity > 30 Sep, each (booking entity, facility) once per group with any member obligor, converted at units_per_gbp. Bands per 6.2, lower bound inclusive.
- Literal answer: 133.04 -> 133 whole groups.

## Verdict: DETERMINISTIC

## Disposition: APPROVE
No repair. No fork found; no rerun.

## Why
CRM-07 5.2 files both the probability structure (flag-only, same across book) and the selection test, and the test separates the bases by 1.6% vs 40.6%. 133.04 sits far from a rounding boundary. Every committed answer (call, 5 band rows x 5 figures, total row) recomputes from the shipped files. Upstream choices the files pin (GLEIF membership under 2.2, UK-time limit cut-off under 1.3/6.1, facility dedup under 6.1) are each stated in the standard.

## Evidence
Recomputation ledger (files: credit_group_register_20260930.xlsx, watch_list_history, ews_entity_signals, credit_obligor_master, gleif_rr/lei, facility_obligor_extract, facility_limit_history, treasury_closing_rates).

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Monitored book 30 Sep 2026 | 913 | 913 | yes |
| Flagged 2026 | 165 | 165 (18.07%) | yes |
| Pooled capture 2022-25 | 78.1% | 78.11% (157/201) | yes |
| Pooled false-alarm | 7.83% | 7.83% (259/3307) | yes |
| Largest miss, capture/FA | 1.6% | 1.57% | yes |
| Largest miss, hit/miss | 40.6% | 40.60% (2024 cohort) | yes |
| Implied share reaching list | 14.6% | 14.57% | yes |
| P(reach \| flagged) | 63.0% | 62.98% | yes |
| P(reach \| not flagged) | 3.9% | 3.89% | yes |
| Caseload | 133 | 133.04 | yes |
| Under 5m: n / exposure / flag / not flag / arriving | 201 / 475.8 / 21.4 / 6.5 / 69.6 | 201 / 475.78 / 21.41 / 6.50 / 69.58 | yes |
| 5-15m | 306 / 3016.2 / 34.0 / 9.8 / 411.5 | 306 / 3016.22 / 34.01 / 9.81 / 411.52 | yes |
| 15-40m | 250 / 7153.8 / 29.6 / 7.9 / 1108.6 | 250 / 7153.81 / 29.60 / 7.90 / 1108.60 | yes |
| 40-100m | 120 / 8213.8 / 12.6 / 3.9 / 1121.5 | 120 / 8213.80 / 12.60 / 3.89 / 1121.52 | yes |
| 100m+ | 36 / 6640.9 / 6.3 / 1.0 / 1283.4 | 36 / 6640.89 / 6.30 / 1.01 / 1283.40 | yes |
| Total | 913 / 25,500.5 / 103.9 / 29.1 / 3,994.6 | 913 / 25500.49 / 103.91 / 29.12 / 3994.62 | yes |
| SVG title/caseload (text) | 133 of 913 | consistent with above | yes (text only; SVG not shipped) |

Sensitivity of the call to choices the files pin (all stay under the standard's own wording):
- Master-only membership gives 131; GLEIF-only 127. Filed 2.2 requires both, so not a fork.
- Branch/fund relationships, lapsed LEIs, successor LEIs, relationship dates: no change (165 flagged, 133.04).
- Book including watch-list groups (violates 4.1): 147. Book excluding ever-listed groups: 122.
- UTC end-of-day limit cut (violates 1.3): same 133 but band rows shift (e.g. 100m+ 46 groups, 4,059.1m arriving); no dedup across booking entities: 29,095m total. Both contradicted by filed 1.3/6.1.

## Competing answers that survived
None for the call. Competing figures exist only under readings the filed text rules out: hit/miss 73 (loses 5.2's test by 25x), hit+capture 80, flat 52, master-only membership 131, book incl. watch-list 147. Band-table alternatives (UTC cut, no dedup) are excluded by 1.3 and 6.1.

## Files/Hygiene: PASS
17 files; formats xlsx (3), csv (9), md, docx, pdf, txt. Signals file 125,317 rows. Distractors: internal_rating_master_scale_2026.xlsx and group ratings sheet, group_economics_uk_outlook_oct2026.xlsx (stress scenarios), committee agenda docx. They look relevant but are not used by the standard. Operational artifacts (extract log, GLEIF CDF files, SOD_BATCH history) read as system output. Minor note: the extract log says "limit history reconciled to the facility extract, no breaks" while 101 facility limits in the extract differ from the 30 Sep UK-time version, because the extract ran after the 1 Oct SOD batch; this is in-world consistent (the log notes the extract ran after start of day 01/10), not a defect. No authoring/benchmark disclosures found. Nothing exclusion-level.

## Stump power
Moderate. The naive route is the hit and miss rates the committee is already shown (4.3), carried onto this year's flags (73 groups); it fails because the hit rate moves with each cohort's base rate (40.6% miss on the 2024 cohort). 5.2 files the backtest, so a solver that runs it will see hit/miss fail and may search for a better basis; those that stop at the reported rates or at a latest-cohort/trended rate land on a wrong whole number. Risk of being cracked is real (the test is spelled out), the lever if too easy is to leave the test pin while moving the candidate bases off the named 4.3 rates.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported hit and capture rates are correct; the difficulty is choosing the predictive basis under a base-rate shift by out-of-sample backtest, and it survives on clean data.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: GLEIF consolidation chains, LEI/CRN keys, ungrouped customers, two ledgers with overlapping facility ids, multi-currency, UTC versions vs UK day. Layer 2: prior-shift (label-shift) inversion of the capture and false-alarm rates validated leave-one-cohort-out. The easy route (hit/miss rates on this year's flags, the committee's own reported rates) gives about 73 instead of 133. Swap test: a monitoring-system backtest of flag precision/recall under base-rate drift is credit-risk specific.

## Fix
none (no change to prompt, input files or solution).

