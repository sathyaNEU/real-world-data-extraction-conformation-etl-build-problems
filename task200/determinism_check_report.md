# determinism-check report, task200, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium) saw only the fresh unzip at /tmp/determinism-check-task200-r1/target/ and the inlined blocks. Every graded figure reproduced from the bundle: the six first-meeting rates, the 4,104 of 5,229 repeat count, screen time, clear searches and expiring certificates. The first-meeting restriction is not named in the prompt, SPS-04 or the email, but SPS-04 4.2 ranks teams on how likely they are to find a prohibited article in a passenger's bag, and a real article is by definition an image not yet met. Under that estimand the order Fell, Brook, Dene, Esk, Arden, Cleve is stable (Fell 62.8 against Brook 69.2). The overall projection score gives Brook, Dene, Esk, Fell, Arden, Cleve.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fell first-meeting rate | 63% (707/1,125) | 707/1,125 = 62.84 | yes |
| Brook / Dene / Esk / Arden / Cleve first-meeting | 69 / 74 / 77 / 81 / 85 | 69.24 / 73.73 / 77.15 / 80.85 / 84.93 | yes (all at least 0.35 pt from a .5 edge) |
| Fell repeats | 4,104 of 5,229, 84% hit | 4,104/5,229, 84.3 | yes |
| Overall rate Brook / Fell | 71 / 80 | 71.3 / 79.7 | yes |
| Screen time h (Arden, Brook, Cleve, Dene, Esk, Fell) | 5,168.8; 4,750.9; 5,545.6; 4,593.7; 5,297.1; 4,603.7 | 5,168.76; 4,750.88; 5,545.59; 4,593.74; 5,297.09; 4,603.70 | yes |
| Clear searches | 6,608; 4,399; 6,737; 6,429; 11,915; 5,683 | same | yes |
| Expiring certificates | 4; 2; 3; 2; 5; 3 | same | yes |
| Order | Fell, Brook, Dene, Esk, Arden, Cleve | same | yes |

## Competing answers that survived
None that changes a graded value on a reasonable reading. Open points:
- The prompt and SPS-04 never name the first-meeting restriction or an exposure window. A memory window of 548 days or less (no basis in the files) puts Brook first (Fell 71.0 against Brook 69.8); any window of 730 days or more, "ever met", class-standardised, non-OTHER-only, cancelled-as-met and deduplicated variants all keep the order. The judge ruled the short window outside the reasonable set.
- Certificate rivals are contradicted by a filed rule: issued date instead of assessment date gives Brook 1, Dene 0; the LMS keyed date for EXT-IIC rows gives 3/0/1/1/3/2; internal rows only gives 8/5/10/4/10/6. SPS-04 fixes expiry from the assessment day. That an EXT-IIC date is a keying date is derived from the centre list (16 to 75 days later), not stated.
- NF (Jan to Jun) and CLEAR (Jul to Dec) are the same "nothing found" code. No key ships; it is inferred from volumes and the PA/RI to PROHIBITED/RESTRICTED switch.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 (the judge said 19; metadata.json and the zip listing say 17) | yes |
| Formats | 3 or more | 5 (csv, xlsx, docx, pdf, eml) | yes |
| Large file | 25,000 rows or more | CT sessions 121,884; search log 50,436 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 (lane_throughput_daily_2026.csv, queue_time_samples_2026.csv, security_compliance_review_2026.pdf), unlabelled in names | yes |
| Distractors unused yet weighty | unused by the solution; a shipped fact rules each out | judge: rank nothing, unused; PDF states image interpretation is outside its review | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-team across six teams; screen time hours to one decimal; counts | yes |
| Prompt shape and 25 criteria | identifiable shape, 25 or more | shape 06 in metadata; criteria count not verifiable here (rubric generated downstream); every team and cell is separately gradable | unverified |
| Not LLM generated, goldens realistic | yes | judge found nothing exclusion-level; I did not re-read the goldens | yes (judge) |

## Gate G reconciliation
The thread's Gate G line is `statistical_rigor`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The design note's `## Three rules` agrees. It names the pooled projection score (Brook first) and d-prime (Esk first) as the easy routes, and says it plants no decoy, withheld rule or ranking artifact. No shipped artifact ranks the teams. The declared distractors (throughput, queue time, compliance PDF) carry nothing, and the thread named the clear-search volume (Esk 11,915), a derivable quantity, as the false lead. No mismatch, and the distractors are not load-bearing.
**Gate G class:** clean (statistical_rigor / analytical_non_defect).
**Gate H:** domain: pass, layers: pass, decisive_step: analytical. The design note's analyst_test and domain_test say the same. Choosing first meetings against all projections is an estimand and comparison-group choice. A strong analyst who cleaned the data and read every rule would still file Brook first by the overall score, so it is not semantics or rule application. Layer 1 mess (UTC against local time, overlapping sessions, Pier B log-off inference, badge replacements, vocabulary change, month-start duplicates, LMS keying date) does not carry the stump.

## Stump power (Gate F)
Moderate to good. The solver has to check the tip_image column for repeat exposure and see Fell's library of about 480 images against about 6,000 for the others. Whoever does that lands the call by the field's standard exposure-adjusted method with no further judgment, so this is a landable call (library `stumping` 1.3). It is not guaranteed to stump. The asks (overlapping CT sessions, Pier B log-off inference, tray split with latest reject, EXT-IIC and centre-only certificates) carry the more reliable difficulty. The main thread should weigh this against the design note's ladder.

## Findings, ranked
1. Unstated exposure window (open point, not a fail). A window of 548 days or less flips Fell and Brook, and no shipped text rules it out. "Never shown in the exports" is the only parameter-free reading. The judge's optional fix is a shipped file that grounds image familiarity without stating the answer.
2. Rounding margin. Dene screen time 4,593.74 is 0.011 h (40 s) from the .75 edge. Brook, Cleve and Esk are 0.03 to 0.04 h away. No constructible variant moves any of them, but Dene is the tightest cell.
3. Two inferred conventions in the asks. The NF/CLEAR equivalence has no shipped key, and the EXT-IIC date as a keying date is derived rather than stated. Neither moves a figure under the reading the files support. Both are semantic inferences on the asks, which the spec permits.
4. Raw counts under a different cancelled-projection reading would differ (687/1,087 and 4,142) while the integer percents and the order stay the same. SPS-04 closes this with "cancelled before it is shown".
5. Not assessed. The cross-batch fingerprint (no prior task is inside the scratch prefix) and the 25-criteria rubric count.
6. Judge slip, harmless. It reported 19 files where there are 17.

## Next action for the author
Nothing is required to ship on the determinism gate. Optionally, add a shipped file or sentence in the standing material that grounds image familiarity without stating the answer, to narrow the exposure-window fork (finding 1). Run `guard.py heart` and `surface` for the cross-batch check.
