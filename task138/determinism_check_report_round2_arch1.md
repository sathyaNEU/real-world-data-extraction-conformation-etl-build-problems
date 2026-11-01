# determinism-check report, task138 round 2, 2026-10-14

The determinism judge's verdict (one isolated thread at medium effort, on the round 2 pack and prompt as built at stage 3), verbatim:

## Verdict, task138 round 2

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; no rerun. (Residual risk noted under Why/Evidence, not a defect.) Cross-batch fingerprint check not run: other task folders are outside the permitted directory.

**Why:** Every committed answer reproduces from the shipped files with no golden-block defects. The main call (215,000 AF) turns on WOP 2.4's "root zone as it stands at the end of 31 January". The only reading that honours it is to run each field's balance through the actual 2026 deliveries (Delivered sets, ordered flow x hours, Table 4 efficiency) to 31 Jan 2027, and that state is insensitive to where the spin-up starts (Gate A, B, C pass). The 24th-smallest replay (2012) is 214,499 AF, almost exactly mid-way between 214,000 and 215,000, so the thousand is forced and robust to every plausible convention I tried.

## Evidence (recomputed from target/)

| Item | Recomputed | Source | Reproduced |
|---|---|---|---|
| Fields on accepted requests | 631 fields, 40,309.43 acres (10 requests have no accepted version) | kbid_water_requests_2027.xlsx + field register (lateral, soil) | yes |
| 24th smallest of 30 replays | 2012 replay = 214,499 AF (23rd 212,936 in 2011; 25th 215,850 in 2003) | station39 + yard splice, WOP Tables 1-5, 2026 orders | yes, order 215,000 |
| Smallest / largest replay | 2024 = 167,024; 2002 = 221,984 | same | yes |
| Fields short of FC at end of last 2026 set | 196 drip + 255 micro + 50 sprinkler = 501; 0 of 130 border | orders, Table 4 | yes |
| Deliveries by lateral (AF) | 17,872 / 17,530 / 15,399 / 17,888 / 18,162 / 18,211 / 15,311 / 11,488 / 15,082 | meter book, rollovers, CCF to AF, 31 swaps chained via Reg out/in, spur 05-021..034 to L5 through the 15 Jun read then L6 | yes, all 9 round to golden |
| Water put in (AF) | 19,678 / 19,409 / 16,879 / 21,018 / 19,758 / 21,060 / 16,711 / 13,110 / 17,371 | heading daily totals + ops-log estimates for the absent days (days absent match the log exactly) | yes |
| Share not delivered | 9.2 / 9.7 / 8.8 / 14.9 / 8.1 / 13.5 / 8.4 / 12.4 / 13.2 | derived | yes |
| Tail weir spill (AF) | 579 / 631 / 440 / 270 / 548 / 650 / 511 / 419 / 361 | Q=3.33 L H^1.5, gauge held to next reading, crest + 2 in per board (set/added +1, pulled 1 -1, brds out 0) | yes, all round to golden |
| Winter claim | Oct 2026 to Jan 2027 rain 1.36 in, lowest of 31 seasons (next 2002 at 2.02) | station records | yes |

Metered turnout deliveries agree with ordered-flow x hours at turnout level (ratio mean 1.000, sd 0.012; 146,942 vs 147,048 AF), so crediting the 2026 sets at ordered flow is corroborated, not assumed.

**Literal-reading forks tested (24th replay, order):**
- Golden state: 214,499, 215,000.
- Spin-up start anywhere from 1 Oct 2025 to 1 Feb 2026 at full or half-full: 214,499 to 214,534, 215,000 (the 13.2 in of Oct-Jan rain fills every root zone). Only a full-TAW start on 1 Feb 2026 moves it (216,432, 217,000), an unnatural choice.
- Credit set water at start day, end day or hourly: 214,497 to 214,503, 215,000.
- Weather rounded to 0.01 in: 214,247, 215,000. Crop-report acres: same. GIS acres in the state only: 214,742, 215,000.
- `>=` tolerance on the AD test: no change.
- Wrong alternatives (the easy routes): start every field full 196,000; last 2026 set taken as refill 209,000; model-simulated 2026 season (irrigate at AD) 199,000; ignore Nov-Jan 213,000; no efficiency in the state 171,000; GIS acres everywhere 217,000. Each departs from a stated WOP term ("as it stands", Table 4, 6.2 request acres). Residual risk: WOP never says in so many words to credit past deliveries, so a reviewer could argue the "model-simulated 2026" or "full" start is licensed. I judge "as it stands" plus the shipped 2026 Delivered sets and Nov-Jan weather and coefficients as forcing the actual-delivery reconstruction.
- Spur fields: register lateral (L6) governs per WOP 6.2; using the request turnout number (L5) would move the requirement about 160 AF, inside the margin.

No attribution, provenance or grain defects found. Gate B: every decisive fact is in a shipped file (WOP 2.3, 2.4, 3.x, 4.1, 6.1, 6.2; Tables 1-5; orders status "Delivered"; weather). Gate E: the prompt pins the single call, the units and rounding for each ask.

## Files/Hygiene: PASS (minor note)
18 files, formats: pdf (2), xlsx (5), docx, csv (9), txt. One CSV is about 107k rows and one meter book 16k. Distractors available: groundwater levels, crop report 2026 (consistent with requests), TVWA notice (allocation 241,000 does not bind), 2023-2025 orders. Dates coherent with a 1 Feb 2027 snapshot; ops log and meters carry realistic mess (CCF registers, rollovers, swaps, logger outages, mixed date formats, unit mm vs in, M flags). README_order_working_files.txt is a file index written in-fiction with no authoring disclosure; acceptable. Station 39 resembles a real state-network download; no answer contamination (the answer depends on shipped District data). Nothing exclusion-level.

## Stump power
Moderate. The request-level and Layer-1 work (weather splice, register vs request lateral, meter chaining, spur reassignment, flashboard remarks) is heavy but strong models clear most of it. The trap that does the work is the starting root-zone state: assuming fields start full, or treating the last 2026 set as a refill, gives 196,000 or 209,000, and the margin to 215,000 is about +-500 AF both ways, so a small mis-specification of the state is penalised. A hint exists in the WOP wording ("as it stands") and the Nov-Jan coefficients, so a careful model can avoid it; the asks (nine laterals x four figures) carry the rest of the discrimination.

## Stumping type
`mechanism: forecasting` (antecedent-state estimation feeding a 24-of-30 replay percentile), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is wrong; on perfectly clean data the same starting-state reconstruction still separates 215,000 from 196,000 to 209,000. Not a banned scaffold.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to swap: crop coefficients, soil total available water, allowable depletion, rooting depth and application efficiency, and a percentile of weather replays are irrigation-scheduling science, not a backdrop. Layer 1: mixed meter registers and swaps, spliced weather stations, a re-plumbed spur, logger outages. Layer 2: conditioning the replays on the root-zone state the 2026 deliveries actually left (not a full profile, not a climatological or refill assumption) and ordering to the 24th of 30. Easy route for an analyst who cleaned everything and read the rules: start each replay from field capacity, giving 196,000.

## Fix
none.

## Disposition

APPROVE taken; no repair, no re-judge. The pack, the goldens and every graded figure are unchanged: the final rebuild's
`target.zip` is byte-identical to the stage 3 cut (sha256 160a86191c3417df), and `freeze.py check task138 --mode
determinism` passes.

- The residual (WOP never says in so many words to credit past deliveries to the root zone, so a full or a
  model-simulated 2026 start might be argued as licensed) is recorded as SF34 in the design note's semantic fork table,
  closed by the estimand (WOP 2.4, the root zone "as it stands" at the end of 31 January, a state of the fields) and by
  the data. `checks.py` asserts it on the generator's clean truth: the record run misses the fields as they are by
  0.027 in acre-weighted, the full start by 4.326 in and the simulated 2026 season by 2.928 in.
- No method sentence is added to WOP: one would file the HOW of the decisive step (the estimator of the filed state) and
  turn it into rule application, which the 10/10 rules forbid.
- The leak reader's Q6 lean to rule application is recorded as SF35: no document names a start (asserted), and on the
  clean truth, every rule read correctly, the two estimators of the same filed state stand a full order apart (209,000
  against 215,000), the last set as a refill missing the fields as they are by 0.955 in acre-weighted.
