# task273 portal determinism check, architecture 2 (2026-10-28)

Both portal judge runs on the architecture 2 pack (target.zip of 2026-10-23, the reworded prompt), as the author relayed them. Evidence for the architecture 4 re-root; architecture 2 was already spent at the portal on 2026-10-27 (both responses filed the golden four).

## Judge run 1 (failed: underspecified_objective, asks 2 and 3)

```
Response 1

Reviewed 25 resources
· 9m
failed

gate_status: A=pass B=pass C=fail D=fail E=pass F=plausible G=pass taxonomy: underspecified_objective fix_location: input_files model_response: semantic_fork

PACKAGE CHECK: 17 files, ~6 formats (csv, xlsx, pdf, pptx) | listed-but-absent: none

PROMPT AUDIT: leaked method: none (prompt says only "rate per mile," "all crashes 2021-2025," "crash unit costs" -- method vague, objective pinned) | padding/trap narration: none | multi-readable ask: the KSI/cost asks do not pin how to reconcile duplicate person records | envelope: 2 deliverables (xlsx, pptx), ~15 determinate asks, unassigned: none

DECIDING STEP (Gate G): building the per-use exposure denominator (quasi-induced exposure: DOT VMT allocated to road/time strata, split to uses by non-at-fault "struck" vehicles) then comparing each caused-crash rate to 1.5x private drivers | class: ANALYTICAL-RIGOR | realistic in the real source: yes | the test: yes -- the main recommendation turns on genuine exposure estimation, so G passes for the main call.

COMMITTED ANSWERS:

main (cover 4: taxi, ride-hail, parcel, app): reproduced yes (model deliverable agrees, rates ~1.83/1.96/1.76/1.94 vs private, others ~1.18-1.24; margin band 1.3-1.7 is robust) | forced: yes
ask1 coverage flags (7): reproduced yes | forced: yes
ask2 KSI people (74/402/45/63/55/109/136): reproduced only under "take the later duplicate record" | forced: NO -- model used "most severe reconciled" and got 75/414/47/64/57/112/140
ask3 costs ($m) (505.9/1979.6/242.4/299.5/279.5/641.9/699.9): reproduced only under "later record" | forced: NO -- model got 508.3/1998.1/244.1/301.2/281.6/647.0/705.7
FORK LEDGER:

duplicate-person reconciliation: "take the later record" (committed) vs "most severe KABCO" (model) | OPEN -- ~9,090 person rows sit in same crash/unit/seat duplicate groups with differing INJURY_SEVERITY; among dup groups KSI membership is 842 (later) vs 1034 (most-severe) vs 494 (first). No shipped file (data dictionary, README, cost PDF) states which record governs; the only severity-aggregation convention anywhere -- dot_crash_unit_costs_2025.pdf, "a crash is costed once, at the unit cost of its most severe injury" -- supports the model's reading, making "later record" the weaker, unforced choice.
exposure method (quasi-induced vs direct mileage): no direct per-use mileage is shipped (platform reports carry TRIPS not miles; fleet returns carry vehicle counts), so induced exposure is forced in kind; strata granularity (model used 48-cell vs author's 288) does not move the 4/3 split -- not decisive.
DISQUALIFYING FINDINGS:

Gate C/D, underspecified_objective. The committed KSI (ask2) and cost (ask3) answers depend on an undocumented rule for reconciling duplicate person records. A strong solver (the shipped model response) reached the exact intended mechanism and diverged on every one of these 14 numbers (e.g., ride-hail KSI 402 vs 414; ride-hail cost 1979.6 vs 1998.1) by choosing "most severe reconciled," which is at least as defensible and better aligned with the shipped cost convention. No shipped file forces "later record," so these committed answers are not uniquely forced -- a non-unique answer ask is disqualifying even though the main recommendation is robust.
REQUIRED FIX: input_files -- add a line to crash_extract_data_dictionary.pdf stating that where a person appears more than once for the same unit/seat, the governing injury severity is [the most severe recorded] (or [the highest PERSON_NO record]), so one reading is forced; then confirm the per-use KSI and cost columns resolve to a single value under that rule.

STUMP LEVER: The real analytical work -- estimating per-use miles by road/time-weighted quasi-induced exposure from non-at-fault vehicles and ranking against the 1.5x line -- is genuine and decides the main call cleanly. Keep it; the only defect is the unpinned duplicate-record reconciliation that makes the auxiliary harm/cost asks non-deterministic.

NON-BLOCKING NOTES:

Main recommendation (4 uses) is robustly reproduced by the model deliverable; the exposure caveat the model prints ("assumes that method is accepted") is honest given no direct mileage ships, but the margin band (nothing between 1.3x and 1.7x) protects the call.
Strata granularity differs between author (288) and model (48) with no effect on coverage -- healthy robustness, not a defect.
```

## Judge run 2 (failed: competing_defensible_answer, the main call)

```
Response 2

failed

gate_status: A=pass B=pass C=fail D=fail E=pass F=plausible G=pass taxonomy: competing_defensible_answer fix_location: input_files model_response: absent

PACKAGE CHECK: 17 files, 5 formats (csv/xlsx/pdf) | listed-but-absent: none

PROMPT AUDIT: leaked method: none (prompt refers to "the coverage rule," which ships) | padding/trap narration: none | multi-readable ask: the per-use "rate per mile", the miles denominator has no pinned estimation method | envelope: 2 deliverables (xlsx, pptx), ~15 determinate asks (coverage x7, KSI x7, cost x7) all assigned, unassigned: none

DECIDING STEP (Gate G): estimate each use's miles driven, then rate=crashes-caused/miles vs 1.5x private | class: ANALYTICAL-RIGOR (induced-exposure VMT estimation) | realistic: yes | the test: yes, but the method is NOT uniquely forced, and reasonable choices flip the call.

COMMITTED ANSWERS (main first):

main (cover taxi, ride-hail, parcel, app): reproduced: no, the author's 288-strata VMT-allocation pipeline is one unpinned estimator; forced: no.
crashes-caused numerators (critical-component): reproduced: yes (taxi 1564, limo 558, airport 648, para 865, parcel ~3319, app ~3285, ride-hail ~6780, file: crash units + operator register), these match, so the numerator path is sound.
KSI/cost asks x14: not assessed (stopped early after decisive C/D failure).

FORK LEDGER:

Canonical UNSTRATIFIED quasi-induced-exposure (caused/struck ratio, needs no VMT pipeline) vs golden 288-strata VMT allocation | OPEN: unstratified covers Airport shuttles (1.70) and Paratransit (1.65) and excludes taxi (1.12), ride-hail (1.02), parcel (1.43), app (1.20), the EXACT OPPOSITE of the golden. No shipped file pins the estimator or the road-class/day/hour stratification.
Mere provision of ccs_hourly_volumes / travel_monitoring VMT does not pin the estimator: the VMT total cancels in the ratio; only the (unstated) stratification weighting flips the answer | not closed by any shipped rule.

DISQUALIFYING FINDINGS:

Gate C/D (competing_defensible_answer). The coverage rule (cfsp_coverage_rule_2026.pdf 3.2) defines rate = crashes caused / "miles their vehicles drove," but ships NO per-use mileage and NO allocation formula. The author's miles come from a self-constructed pipeline: VMT by road class x count-station day-type/hour shares x within-stratum induced-exposure weighting (288 strata). I reproduced the numerators, then applied the canonical textbook quasi-induced-exposure estimator (relative accident involvement = (caused_use/struck_use)/(caused_priv/struck_priv)), which needs no VMT at all and is at least as defensible. It yields the OPPOSITE recommendation: covers Airport shuttles (1.70) and Paratransit (1.65), excludes taxicabs (1.12) and ride-hail (1.02). The main call is not uniquely forced; 10/10 rigorous analysts would not reconstruct the identical 288-strata VMT estimator, and the method is fully decisive (flips every use).

REQUIRED FIX: input_files | Ship a governing methodology note (or a Department VMT-by-use table) that states the single mandated exposure estimator and stratification, e.g. "use the Department's stratum VMT (road class x day type x hour from travel_monitoring_report Table 1 and ccs_hourly_volumes), allocate within each stratum in proportion to not-at-fault vehicles struck", so the miles denominator reads one way. | Check: unstratified and stratified estimators then no longer both sit as defensible, and the covered set is forced.

STUMP LEVER: The intended analytical centerpiece (recognizing no direct VMT-by-use exists and reaching for induced exposure) is genuine and hard (Gate G passes). But because neither the rule nor any file pins WHICH induced-exposure estimator or stratification to use, and the choice completely reverses the coverage, the task is non-deterministic; pinning the estimator in a shipped methodology document would keep the hard analysis while forcing one answer.

NON-BLOCKING NOTES:

Numerator pipeline (two form versions, PTCR-16 carrier to operator-register use mapping, hit-and-run exclusion, >=2 MV-in-transport filter) reproduced the committed crashes-caused within rounding, solid Layer-1 construction.
17 files / 5 formats / multi-million-row tables satisfy hygiene volume.
```
