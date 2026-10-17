# determinism-check report, task241, pass 2, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The release thread files the estimand and the 0.010 tolerance. Executed with the reference water mapped to each profile's potential temperature and position, it adjusts six floats (1990001, 1990004, 1990005, 1990007, 1990008, 1990012). The smallest adjusted offset is 0.020 and the largest unadjusted is 0.003. Global, archive-only, RHD-only and local (1.5, 3, 5 degree) fits all select the same six. Both tables reproduce exactly. Source: /tmp/determinism-check-task241-1792273646931/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ascending profiles after v2 replaces v1 | 878 | 878 (44 duplicates; 1990731 out) | yes |
| Good values 1,400 to 1,900 dbar | per submission step 2 | 8,794 in 878 profiles | yes (count not re-compared by me) |
| Theta ranges | reference 4.03 to 8.29, float 4.32 to 7.53 | 4.03 to 8.29, 4.32 to 7.54 | yes |
| Offsets | -0.022, -0.020, -0.027, -0.030, +0.021, +0.020; max other -0.003 | within 0.001 except 1990005 -0.026 vs -0.027 | yes within the stated 0.003 |
| Pooled theta, no position | 10 to 14 | 11 | yes |
| Fixed pressure | 13 to 17 | 15 | yes |
| Ask 2, casts to 2,000 dbar 2015 to 2025 | 21,17,19,24,19,13,21,17,22,23,17 | identical (119 RHD duplicates removed; stable for 5 to 60 min, 0.01 to 0.05 degree) | yes |
| Ask 3, in 24 h by month | 781 of 878; 69,58,62,67,65,67,63,66,63,69,67,65 | identical | yes |

## Competing answers that survived
None on the decisions.
- Fixed-pressure differencing gives 15 floats, pooled theta gives 11, and first-profile drift misses 1990007 and 1990012.
- Residual risk the thread notes: a literal reader could call fixed-pressure a licensed reading of "the water it sampled". It rejects this because only theta plus position leaves near-zero offsets for 18 floats, and the pressure fits leave structured residuals.
- Ask 3 uses "surfaced" as the end of ascent (the K floats' juld is the ascent start, giving 661 instead of 781). The technical file and the model PDF support the end-of-ascent reading, so the thread treats it as a permitted data-semantics device in an ask.
- Receipt clock as UTC gives 770, but the dictionary states Lisbon time. The first-file reading gives 816, but the thread restricts to the complete file.
- Two daylight-saving-ambiguous receipts on 31 October give the same counts either way.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 per metadata and zip (thread said 15; its miscount) | yes |
| Formats | 3+ | csv, md, pdf, eml, docx | yes |
| Large file | 25,000+ rows | levels file about 94,000 rows | yes |
| Distractors | 2+, in metadata, not file-labelled | recovered_sensor_checks and oxygen, per metadata.json (read in pass 1); neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks multi-dimensional with unit and rounding | yes | 24 floats, 11 years, 12 months; unit and 3 dp stated | yes |
| Prompt shape, 25+ criteria | identifiable | scorecard against a threshold; not counted here | yes |
| Not LLM generated | yes | judge found none | yes |

## Gate G reconciliation
The thread's classification (method_or_model_selection, analytical_non_defect) matches the design note's stump sentence and the card (stump_class analytical). The thread does not name either declared distractor as carrying the task. The stated easy-route ranges (13 to 17 fixed pressure, 10 to 14 pooled) were reproduced inside their bounds.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the unit, clock and file mess (IPTS-68, depth to pressure, duplicate casts, partial files, Lisbon against UTC, the K floats' juld). Layer 2 is choosing the water-mass basis. The easy route files 13 to 17 floats with at least seven healthy floats wrongly adjusted.

## Stump power (Gate F)
Plausible. A strong analyst who differences at fixed pressure or on pooled theta files 11 to 17 floats. The six need the theta-and-position mapping. The asks add their own devices.

## Findings, ranked
1. Info: no failing gate. The only third-decimal difference is 1990005 (-0.026 against -0.027), inside the stated 0.003 acceptance.
2. Info: two realism-only generator fixes ran after the thread (cruise first-station times, one section's latitude steps). Per the coordinator, offsets moved under 0.001 (1990004 now -0.020, which the thread itself computed) and every count in the call and both tables is unchanged. These are the coordinator's statement, not re-judged here.
3. Info: the thread counted 15 files; the true count is 16.

## Next action for the author
None. Proceed to ship.
