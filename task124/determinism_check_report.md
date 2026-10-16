# Determinism check, task124 (round 3)

Stage 4 judge run, 2026-10-16: one isolated thread at medium effort on a fresh unzip of the round-3 cut (target.zip
sha256 8ef783ab336726f5), the prompt, the submission's graded blocks and the judge's system prompt. Its verdict follows
verbatim, between the rules; the disposition after it records what was done with its minor notes. Earlier rounds are
kept as history: `determinism_check_report_loop0.md`, `_pass2.md`, `_loop1.md` and `_round2.md`.

---

# Verdict, task124 (fresh judge pass, redesign r3)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun needed. Optional hardening of the zone-line/cost rounding margins (see Evidence) is not required.

**Why:** The call (RZ-06 Wexley finished in programme year 2037, inside 1 Nov 2037, plan cost about $267M, 10.5 years of the $25.4M appropriation) falls out of the shipped plan rule (plan rev 2 s4.3: each Lead Status Unknown line carried at the share of lead/GRR expected among the district's unknown lines of its era, s5.3 running-total schedule) once that share is estimated for the population actually left unknown. The verified lines are not that population: they sit overwhelmingly on mains whose tap cards read lead or galvanized, while 78% of the unknown lines sit on mains whose cards read only copper or plastic. Every estimator that conditions on the main's kind lands on 2037; the easy estimators (raw verified share, tap-card share) land on 2039/2040 and answer "no". The shipped files force one answer on the main call and on all three ask sets.

## Evidence (recomputed from the bundle)

| Item | Result | Source |
|---|---|---|
| Verified lines with no tap card, built before 1989, first result per line | 8,255 reproduced (CIS premise numbers zero-padded to 8 digits through cis_gis_crosswalk_2023.csv, 0 unmapped; result codes via sl_material_result_codes.csv) | sl_field_verifications, crosswalk, codes |
| Raw verified lead/GRR share by era | 0.735 / 0.524 / 0.061 reproduced | same |
| Share by main kind x era (main reads lead/galv if any tap card on it is LEAD/GALV) | LG mains 2867/2889 = 99.2%, 1306/1375 = 95.0%, 114/188 = 60.6%; copper/plastic mains 1/1014, 2/1123, 0/1666 reproduced exactly | inventory tap_card_material, main_segment |
| Unknown lines on LG mains by era | 4,212 / 2,121 / 261 reproduced (of 8,890 / 7,851 / 13,200) | inventory |
| Era shares 0.47 / 0.26 / 0.01 | 0.4707 / 0.2579 / 0.0120 reproduced | derived |
| Plan cost and years | $267.1M, 10.52 years, RZ-06 finishes 2037 reproduced | unit_cost_schedule_2027.xlsx, CIP docx, plan s4-5 |
| Zone lines (nearest 10), zone cost (nearest $0.1M), finish year | all 12 zones reproduce exactly (e.g. RZ-07 1,211.3 -> 1,210, $20.80M, 2027; RZ-06 710.1 -> 710, $16.61M -> 16.6, 2037) | derived |
| 2026 payments per full replacement, per contractor-quarter (Eastern quarter, latest closing per site, each change order once, TCU's two vendor numbers merged) | all 12 values reproduce (13,944 / 13,378 / 13,402 / 13,303; 14,401 / 13,741 / 14,096 / 13,944; 15,545 / 14,166 / 14,328 / 14,260). Quarter counts 98/501/427/103 match the progress report. Each change order's sites fall in one quarter, so CO attribution is unambiguous; co_amount equals the xlsx amount on every site. | lsl_completions, change_orders xlsx, progress report s2 |
| Signed access agreements by zone | all 12 reproduce (total 9,114 = 8,741 distinct SIGNED lines + 373 E-SIGNED tracker lines with no form in the agreement file); zone from inventory (plan rev 2), not zone_on_form (174 forms differ) | access_agreements, tracker, crosswalk, inventory |

Forks tested and results:
- Main call finish year, estimator variants: stratified by main kind x era 2037 (10.52 y); stratified by kind only (one rate per kind) 2037; stratified by zone 2037; visit-level instead of line-level 2037; logistic on build year within LG mains, era-averaged 2037; raw verified share 2039 (12.9 y); tap-card LG share 2040; whole-main share 2043 under my definition (the recommendation states 2041; non-load-bearing, the definition of "whole mains with or without lead taken out" is not filed). The yes/no on the deadline and the year 2037 are stable across every estimator that conditions on main kind (margin to 2038 is 0.48 y, about $12M).
- Main kind is cleanly bimodal in this data (share of LG cards on an LG main 0.71 to 1.0, on others exactly 0; LEAD-only, GALV-only and mixed mains give the same shares), so "any card" vs "majority" vs "LEAD only or GALV counted" does not move the answer. Verified lead share does not differ between LG mains that have unknown lines and those that do not (e.g. pre-1930 99.2% vs 99.3%, 30-49 94.6% vs 96.0%), nor by verification method, so the stratified estimate is not hiding a second selection.
- Repeat verifications (198 lines) never disagree, so first vs latest result is immaterial. No Lead Status Unknown line has a verification record (no posting lag). All 1,129 2026 completions are REPLACED/NON-LEAD in the inventory.
- Rounding fragility (asks only, not the call): the plan's "share ... of its construction era" pins one share per era; with that, rounded shares (0.47/0.26/0.01) or a logistic era-average change no rounded figure. A per-line model or a zone-level share, which the plan wording does not license, would change the rounded lines in 10 to 12 zones. Thinnest margins under the licensed era-level estimator: RZ-11 lines 1,568.3 vs the 1,565 boundary (a logistic era-average gives 1,565.3), RZ-09 cost $26.08M vs the $26.05M boundary. Low risk of a defensible disagreement, noted for the author.
- Convention items grounded in shipped text: quarters in Eastern time (progress report s2), reclosing replaces first closing (field notes), TCU vendor change is one contract (progress report s5, contracts file), E-SIGNED means signed (field notes, tracker), withdrawn forms excluded; the 63 E-SIGNED lines with only a withdrawn form were withdrawn after the e-signature date, so excluding them is the only consistent reading. A solver counting only file SIGNED forms gets 8,741 (a reading the tracker note contradicts).
- Gate E: the prompt asks for a finish year per zone, a yes/no on the deadline, each ask has unit and rounding in the sentence. The estimator for the unknown share is deliberately left open (method) while population, window, unit and comparison (district's unknown lines, by era, per plan s4.3) are filed. No loaded premise.
- Gate B: all decisive facts are in shipped files (plan, CIP docx table 25.4, unit cost xlsx, inventory, verifications, crosswalk). I did not find an external dependency. The 1 Nov 2037 deadline and 31 Oct season close are in plan s1.2 and s5.4.

Cross-batch check: not performed (other task folders and earlier reports are forbidden to this judge); fingerprint against delivered tasks is left to the author's clone check.

## Files/Hygiene
PASS. 17 files (>= 10), formats: csv (9), pdf (2), docx, xlsx (2), md (5 distinct formats); inventory 90,652 rows. Business-realistic system extracts (GIS inventory, WMS verifications with a CIS-to-WMS cutover, three recording code forms, zero-padded premise keys, UTC tablet stamps, RECLOSED rows, repeating change-order totals). Distractors present and unused by the solution: lcr_tap_samples (tier 1 lead samples), ami_meter_exchanges, sample CO descriptions. No README or generation disclosure; the field-notes file is explanatory but written as an asset-records handoff, plausible. Temporal coherence good (plan 20 Oct 2026, CIP 14 Dec 2026, extract 8 Jan 2027, board 19 Jan 2027). No public-data contamination. No exclusion-level finding. Minor: the field-notes md and extract log are tidier than a typical system artifact (cosmetic, non-stump).

## Stump power
Good. The trap that does the work: the 8,255 verified no-card lines are a selected sample (programme verified lead-main lines first), so the raw 73.5/52.4/6.1% era shares overstate the unknowns (2039, answers "no, misses the deadline by two years"), tap-card share gives 2040, and a model on era/year/zone without the main's kind gives about 2039. A strong model that cleans the joins correctly and fits the obvious estimator on verified lines files the wrong deadline call. The ETL layer (key padding, code forms, UTC, change orders, E-SIGNED vs form file) stacks additional ask-level failure chances. Stump rate is unmeasured here; the plan text ("among the district's Lead Status Unknown lines") is a legible but not announcing hint.

## Stumping type
`mechanism: statistical_rigor (selection bias / covariate shift, estimating an unobserved population from a non-representative verified sample)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. All reported inputs are correct; no stated figure or stakeholder conclusion is overturned. On perfectly clean data the same selection structure still stumps, so the clean-data test passes. Banned_stumping_type does not apply.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: expected lead/GRR share among unknown lines to cost and schedule an LCRI replacement programme is the field's own inventory-estimation work (swap test: "hospital" or "megawatt-hours" breaks it; the quantity is a material-prevalence estimate). Layer 1: CIS/WMS cutover, padded premise keys, three result-code vocabularies, UTC vs Eastern, reclosed rows, repeated CO totals, vendor renumbering. Layer 2: representativeness of the verified sample, stratifying by the main's kind and era. Easy route: era shares from all verified lines (0.735/0.524/0.061) or from tap cards, giving last zone 2039/2040 and "misses the deadline", versus the correct 2037 "meets it".

## Fix
none. Optional (author's discretion, no rerun if prompt unchanged): none of the asks needs a prompt change; if the author wants more headroom on rounded lines, move RZ-11 (1,568.3) and RZ-09 cost ($26.08M) off their boundaries in a regenerated pack (this would require a rerun).

---

## Disposition

APPROVE, shipped on this cut; no pack change, no golden figure moved, target.zip unchanged at 8ef783ab336726f5.

- (a) Submission block 1 gave the rivals finish years (the mains verified whole 2041, the judge 2043 under its own
  definition of whole mains; every verification and the model on era, year and zone 2039; the tap cards 2040). Every
  rival year is cut: block 1 names each rival and says it runs the last zone past the 1 November 2037 deadline, which
  holds under every definition the judge tried, and drops the 316 count from that sentence. Write-up only;
  `figures_check.py` exit 0 (99 figures), `precut.py` exit 0.
- (b) The ask rounding margins (RZ-11 lines, RZ-09 cost) are thin only under a per-line model or a zone-level share,
  which plan 4.3's one share per construction era does not license; recorded as an accepted risk in the design note.
