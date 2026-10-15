# Verdict (task143, ZC2638 warranty reserve)

**Verdict:** DETERMINISTIC (the golden reproduces from the bundle; one low-severity open convention on a single cell, see Evidence).

**Disposition:** FIX_NOW (optional, low severity). Pin in one place how a replacement whose removed battery never reached the Bielefeld returns log is costed (zero freight, counted in the average). It changes only the Ljungqvist cell (112 against 113). Otherwise APPROVE. No change to the main call, the data or the stump.

**Why:** The reserve is forced by the shipped files. RL-3's log-life error is mostly the formation tray's (tray sd 0.160, cell sd 0.086, 78% at the tray). 7,063 of the 7,200 packs are three tray-mates, and the pack spec (s.4) makes the pack its weakest cell. Integrating over a new tray's shared error gives about 398 packs, so 400 at the nearest 50. The independent-cell shortcut gives 514 (500). Every supplementary figure also recomputes, apart from the single-cell convention below.

## Literal reading
1. Reserve (FIN-RS-04 3.2, 3.3, 3.4): the sum over the 7,200 packs of P(any of the 3 cells has N80 < 600), rounded to the nearest 50. The estimand is filed. Method stays open but is forced by the data (tray ICC 0.78).
2. Partner counts and months: CAP + WTY + REPLACED, by the invoice service period (README_service_extracts: "a line per job in the invoice's service period"). TM-2603-R1 replaces TM-2603. DACH uses SAP Techn. Abschluss to 1 March and the case-system closing day from 2 March; an SAP order is counted once.
3. Cost per replacement: invoice line in EUR at the treasury month-end rate of the service period, plus the battery's share of its consignment charge, plus the service-pack standard cost valid at the service period.
4. Silent points: (a) replacements with no returns-log row (18 of 317); (b) closed_utc as the work date for partners; (c) cycle_count exactly 600 against the warranty field; (d) the FX month; (e) the freight allocation basis. Each is run below.

## Evidence (recomputed from the bundle)
| Item | Recomputed | Golden | Source |
|---|---|---|---|
| RL-3 coefficients (refit on 2,373 EOL cells) | 8.7067 / -0.4265 / -0.0671 | same | fleet A + B first-100 files (A cycle +1, B deduplicated, 4 continued tests stitched), life results |
| Tray sd / cell sd / tray share | 0.1601 / 0.0856 / 77.8% (ANOVA and REML agree; lot variance 0) | 0.160 / 0.086 / 78% | register + life results |
| Pack composition | 7,063 / 136 / 1 | same | genealogy joined to cell data trays |
| Release-test predicted lives | 120 cells, all above 600 (min 701, median 886) | all outlive 600 | features F1, F2 |
| Expected packs | 397.4 to 398.5 (my implementations) | 398.9 | RL-3 + pack spec s.4 |
| Independent cells (2.44% per cell, 3 cells) | 514 | 514 | same inputs |
| Dauvergne / Tolley Marsh / Ljungqvist / Ferrucci replacements | 99 / 81 / 58 / 79 | same | invoices (R1 used, original March sheet dropped) |
| Monthly totals Oct 2025 to Sep 2026 | 8, 17, 23, 25, 26, 39, 41, 51, 57, 56, 74, 71 (sum 488) | same | partners 317 + DACH 171 |
| Average cost, zero freight for the 18 unreturned | 99.0 / 102.0 / 112.0 / 96.0 | 99 / 102 / 112 / 96 | invoices, rates, carrier statement, cost sheet |

Robustness of the reserve:
- Censored STOPPED cells (27) changed the tray sd by 0.0004 when imputed.
- Fleet means and homoscedasticity are fine, and errors are close to normal.
- The 375 to 425 rounding window holds for any sensible estimator. A one-standard-error move in the tray sd would reach 360 or 437, but the shipped estimators agree to three decimals.
- Plugging in the lot's mean predicted life gives 237 (250). It drops the real cell-to-cell spread of predicted lives and is not a defensible rival.
- Treating the three cells as one (perfect correlation) gives 176 (150). The data show ICC 0.78, not 1.

Open point (low severity): 18 CAP/WTY/REPLACED partner lines have no row in the returns log, and all 222 statement consignments match the log row for row, so no freight was billed for them.
- Counted with zero freight (golden): Ljungqvist 111.98, which is 112.
- Dropped from the average, or filled with the mean freight: Ljungqvist 112.95 or 113.04, which is 113.
- The other three partners round identically under every variant (99 / 102 / 96).
- The text does not say which reading governs. "What one cost us on average" over the 58 replacements favours the golden, but this is a real if small fork on one graded cell.

Other forks that close:
- Partner closed_utc is always after the invoice date (lag 1 to 2 months), so it cannot be the work date. Counting by closing month would give 87 / 69 / 51 / 69. The invoice period is forced.
- Month-end FX: only the service-period month-end exists for September 2026, and prior-month FX moves nothing at rounding.
- Pack standard cost by service period, closing date or return date does not change any rounded figure.
- KS26-015372 (UKI, cycle_count 600, GW) is excluded by the warranty field. A solver applying "within 600 cycles" literally to cycle_count could include it. Minor.

Gate B: every decisive fact is in a shipped file (tray key and register, pack spec s.4, policy 3.2 to 3.4, cost sheet, rates). Competing answers: 500 (independence), 250 (plug-in) and 150 (perfect correlation) each lose to the data.

## Files/Hygiene
PASS, with notes.
- 25 files in 4 formats (pdf, csv, xlsx, txt). One file exceeds 25,000 rows (fleet A, 174k).
- Mess is realistic: semicolons and decimal commas against UTC ISO, cycle 0 against cycle 1, a serial in three spellings, overlapping weekly pulls, reissued invoice, SAP to case-system migration, three languages on the invoices, three currencies.
- Notes: the two README_* files are in-fiction extract notes ("pulled for Product Finance by ..."). No authoring language, but the "README" file name reads like a build artifact and may be renamed. The extract notes also define file grain, which is acceptable.
- Temporal coherence is fine (pull 12 October 2026, release 16 October, QM-07 rev 4 of 30 September 2026).
- No exclusion-level finding. No public-data contamination is evident.

## Stump power
Good. The trap is treating RL-3's published RMSE 0.182 as independent per-cell error (514, so 500), when a tray's shared error is perfectly visible in the register and genealogy. A strong model that cleans everything correctly still reaches 500 by compounding the 2.4% over three cells. The ~25 graded ETL figures (12 months, 4 counts, 4 costs, the freight-share and R1 traps, the SAP/case-system overlap) add many independent ways to miss points. The asks plausibly hold the top two under 50.

## Stumping type
`mechanism: statistical_rigor` (clustered errors, weakest-link pack probability; also `etl_conformance` for the second table), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported RMSE, coefficients and counts are all correct. The difficulty is the dependence structure of the errors and the pack's weakest-cell logic, and it survives clean data. Not a banned scaffold.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: the deciding quantity is a cycle-life prediction model's error structure turned into a pack-level warranty probability. A stated score or list rule is not what decides it.
- Layer 1: cycler fleet formats, UTC against Bielefeld wall time, continued tests, serial formats, partner invoice layouts and currencies, SAP against case system, a reissued invoice.
- Layer 2: random-effects error (tray within lot) propagated through a weakest-cell series pack.
- Easy route: a strong analyst who read everything correctly applies RMSE 0.182 per cell and compounds it over three independent cells. That gives 514, so a reserve of 500 instead of 400.

## Fix
Where: prompt or the extract notes (optional, one line). State that a replacement whose removed battery has no returns-log row carries no freight, or that the average runs over returned batteries only, whichever the author intends. The 112 golden requires the former. Otherwise none. Rename README_* if the house wants to avoid that file name.
