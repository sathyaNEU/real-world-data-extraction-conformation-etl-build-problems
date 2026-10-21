# Verdict (task252)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; no rerun. One watch item (the analysed-stamp clock offset, below) is closed by the shipped chronology and is an ask-level item only.

**Why:** The six flagged channels fall out of the shipped historian, register, verification workbook and LIMS grabs the same way for every rigorous solver. The carryover shares (about 7 and 2 per cent at five analysers) separate cleanly from the other three, and the zero error versus span error is separated by the raw-grab comparison, which is far apart (Holmedale about 1.7 per cent of level against 8 per cent for a span error; Calderwood about 10.7 per cent against about 1.6 per cent for a zero error). The margins are wide: flagged channels sit at 0.009 or more in my reconstruction and the rest within 0.003, so nothing sits near 0.005. Asks 2 and 3 reproduce exactly from the files.

## Evidence (recomputation ledger)

| Figure | Claimed | Recomputed | Reproduced | Source |
|---|---|---|---|---|
| Carryover shares BRN, DUN, ELS, GAR, HOL | about 7% of slot before, 2% of the one before | c1 0.066 to 0.081, c2 0.010 to 0.035 in per-port regressions with raw lags 2 to 8 h as controls; pooled fits about 0.07 and 0.02 (noisier at DUN and ELS for the 2-back share) | yes | nh3_online_readings, G rows, port order from register |
| Carryover shares ASH, CAL, FEN | under 1% | about 0 (CAL 0.003 to 0.006, ASH and FEN about 0) | yes | same |
| Holmedale check mean | 0.092 (0.008 low) | 0.0917 to 0.0923 | yes | verification workbook, HOL rows |
| Calderwood check mean | about 8% low | 0.0907 to 0.0923 | yes | verification workbook, CAL rows |
| Other six checks | within 0.002 of 0.100 | 0.0987 to 0.1020 (BRN Dec 0.102 is the largest) | yes | verification workbook |
| Holmedale zero error | 0.008, not 8% | raw grabs less carryover-removed raw reading: mean shortfall 0.0062 (SE about 0.002), relative 1.7% (n=12) | yes, zero not span | LIMS RW-HOL against HOL-RW1 slots |
| Calderwood span error | about 8% | relative shortfall 10.7% (SE about 0.7%) against 0.008 for a zero error (n=13) | yes, span | LIMS RW-CAL against CAL-RW1 slots |
| BRN-FW1 | 0.007 or more | carry +0.0115 (+0.0135 with shares inflated 15% and 25%) | yes | historian |
| DUN-FW1 | 0.007 or more | +0.0113 (+0.0133) | yes | historian |
| ELS-FW1 | 0.007 or more | +0.0091 (+0.0107) | yes | historian |
| GAR-FI1 | 0.007 or more | +0.0271 (+0.0316) | yes | historian |
| GAR-FW1 | 0.007 or more | +0.0118 (+0.0147); the two-back raw share matters here | yes | historian |
| HOL-FI1 | 0.007 or more | +0.0236 carry, -0.008 zero, net +0.0156 | yes | historian |
| HOL-FW1 | within 0.003 of zero | +0.0088 carry, -0.008 zero, net +0.0008 (+0.0030 at inflated shares) | yes, not flagged | historian |
| CAL-FI1, CAL-FW1 | about 0.002 | -0.0016, -0.0014 | yes | historian |
| Every other treated channel | within 0.003 | all within 0.0004 | yes | historian |
| Ask 2 counts (analysed more than 24 h after collection) | ASH 14, BRN 9, CAL 8, DUN 12, ELS 11, FEN 13, GAR 14, HOL 11 | identical with the analysed stamp moved forward 1 h (identical for any shift from 53 to 64 min); 16 courier-docket duplicates dropped; TW- and TUR codes mapped | yes | lims_ammonia, register Sample points, eml |
| Ask 3 hours at fixed dose | ASH 25.0, BRN 23.0, CAL 22.0, DUN 28.5, ELS 20.5, FEN 41.0, GAR 17.5, HOL 22.0 | identical, all eight, from the stated recipe (check cycles, filtered-port-only unfilled F, all-port unfilled F runs followed by V checks unavailable; filled F, missing rows and all-port runs with no check available; gap beyond the 2 h hold) | yes | nh3_online_readings, process summary, WQ-DS-04 |

## Competing answers and forks

- Treat the historian as truth (no carryover) and apply only the Holmedale check as a bias: flags HOL-FI1 and HOL-FW1, six channels short. This is the wrong easy route, not a surviving answer: the carryover is visible in the data (regressions above) and the answer is not forced by that reading.
- Holmedale as a span error: HOL-FW1 net +0.0076 flagged, HOL-FI1 net +0.021. Closed by the raw grab comparison (1.7% against 8%). Calderwood as a zero error: CAL-FI1 and CAL-FW1 at about -0.008, flagged. Closed the same way (10.7%).
- Ask 2 literal fork. The data dictionary gives no time basis for `analysed` (the other three clocks are stated as New Zealand time). Read literally with no shift the counts are ASH 11, BRN 6, CAL 7, DUN 9, ELS 8, FEN 7, GAR 11, HOL 10. The shipped data close it: 16 rows are stamped analysed before reception logged them (down to 53 minutes before) and no result is released within 64 minutes of its stamp, so a one-hour clock behind (NZST against NZDT) is the only coherent repair, and all shifts in 53 to 64 minutes give the golden counts. I count this as closed but an ask-level data-semantics step; it relies on an inference no file states.
- Ask 2 duplicates: keeping the courier-docket row (15:28 collected) instead of the sampler's row would lower counts for the 7 December round. Closed because 15:28 is the same time for all 16 points while the others are sampling-round times.
- Ask 3: counting every F row as unavailable, or none of the all-port runs, gives different hours. Closed by the process summary (PLC reads the analyser directly, the outstation and historian are separate), the dictionary (filled F, missing rows) and the verification sheet's note that a fault is followed by a check. This is also a multi-rule ask (asks may be rule application).

## Files/Hygiene
PASS. Ten files, five formats (csv x4, xlsx x2, pdf x2, md, eml); nh3_online_readings has 106,181 rows. Rainfall and plant output files are unused by the solution (distractor candidates). Timeline coherent (data and documents Oct to Dec 2027, dictionary revised 3 Nov). No authoring or benchmark language seen in the files I opened. The only oddity is the missing time basis for `analysed` in the dictionary, which I treat as realistic mess, not a hygiene fault. I did not open metadata.json (forbidden). Nothing exclusion-level.

## Stump power (Gate F)
Good. A capable solver who reads the historian offsets as the deliverable, or who finds only the Holmedale check shortfall, files HOL-FI1 and HOL-FW1 only. Reaching all six needs a fitted carryover model (two-slot shares, with the port's own raw-lag response controlled for) and a zero versus span separation from the raw grabs. The verification workbook says PASS for Holmedale and Calderwood, which is not a rejection trap by itself. The shipped prose never mentions carryover, so it is not pre-disarmed.

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (measurement-error model estimation), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The core is estimating the analyser's carryover shares and its calibration error structure; run on data with no carryover, the zero/span separation at Holmedale and Calderwood alone would still stump. Borderline note: a reviewer could read the carryover as an instrument "defect"; I judge it the field's own measurement-system analysis, not a planted decoy.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Domain swap test fails to swap: carryover and zero/span calibration error of an online analyser against laboratory grabs is what a water-quality instrument engineer estimates. Layer 1: clock and code mess in the laboratory export (NZ time, unlabelled analysis stamp, October-to-November code change, duplicated logging), historian fills and lost rows. Layer 2: estimating carryover shares per analyser and separating zero from span error. Easy route: take the historian or the check mean at face value, giving {HOL-FI1, HOL-FW1} instead of the six.

## Fix
none. Optional: none that changes what solvers see.
