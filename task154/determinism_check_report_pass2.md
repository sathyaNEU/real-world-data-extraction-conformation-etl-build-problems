# determinism-check report, task154, 2026-11-02 (pass 2)

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Taxonomy: underspecified_objective (growth-rate basis). Judge verdict: /tmp/determinism-check-task154-1793605151/verdict.md. Zip md5 2320312b46930fdfa93134540cf22dd4. Brief: /tmp/determinism-check-task154-1793605151/judge_brief.md.

## Why
Every golden figure reproduces from the bundle, but the filed text does not license the growth rate that produces them. Section 6.4 says only "adding the wall loss its external corrosion produces after the run". No file gives a rate or says how to get one. The golden rate is "reported depth over days from the zone's failure to the run" (zero depth before failure, constant rate, nothing before failure). Other literal readings give different counts and some flip the call. The always-protected zones R-1, R-4 and R-8 carry external corrosion up to 29 per cent, so "all depth accrued after failure" is contradicted by the data, and the data do not separate the candidates. This is an unfiled WHAT (the estimand's growth basis), not a method choice the data settle.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible anomalies (Metal Loss, Corrosion, EXT, depth < 60) | 8,142 (implied) | 8,142; the 59 at 60 or deeper match the 59 register rows | yes |
| 34 mileposts (2 dp) | golden | interpolation between AGM markers matches all 34 | yes |
| R-7 failure | 12 Aug 2019 | RMU first low day; any threshold 15 to 94 per cent gives it | yes |
| R-5 failure | 9 Jul 2016 | RMU step change | yes |
| R-3 failure | 12 Jul 2011 | inspections only; 63-day gap, counts unchanged | yes |
| Run date and days | 2,102 R-7; 3,231 R-5 | pass-time interpolation puts all on 14 May 2025 (UTC same); 2,102, 3,231, R-3 5,055 | yes |
| Restorations | R-3 16 Oct 2028; R-7 10 Jun 2030 | capital plan Projects sheet; R-5 Deferred only | yes |
| Digs by year | 4, 9, 11, 6, 4 = 34 vs 24 | same; all 34 schedule rows match | yes |
| Nearest year-end crossing | n/a | 29 days (feature 29097, 3 Dec 2027); failure-date shifts and R-7 stop dates Feb 2030 to Mar 2031 give same counts | robust |
| Repairs: composite / type B / pipe replacement | 28 (72.0) / 17 (88.0) / 7 (63.3) | 52 distinct repairs from 59 rows; same | yes |
| Completed Jun to Sep | 7, 16, 15, 14 | same | yes |

## Competing answers that survived
- A1 growth-rate basis (open, decisive):
  - pipe-age rate, unprotected zones, stopped at restoration: 0,0,0,0,0 = 0, Yes
  - golden with 5 per cent background removed: 3,7,10,4,5 = 29, No
  - minus 9.6 per cent (mean of always-protected zones): 1,6,8,7,2 = 24, fails by year (2029)
  - minus 15 per cent: 17, Yes
  - minus 29 per cent: 5, Yes
  - Closing rule: none shipped (6.4 silent on the rate).
- A2 failure-date source (minor): annual survey last passing September gives 2,7,10,5,5 = 29; naive first RMU record for all zones gives 0,3,9,4,4 = 20. The RMU day is the precise source.
- A3 restoration stops growth (natural, unfiled): R-7 not stopped 4,9,11,6,18 = 48; R-3 not stopped 36.
- A4 dig timing: closed by 6.5.
- B repair ask (smaller fork):
  - unit = register row or dig (59): composite 31 / 87.0 ft, type B 19 / 98.0, pipe replacement 9 / 87.4; months 9, 18, 16, 16
  - union of placed intervals: pipe replacement 63.4 ft instead of 63.3
  - excavation month: 7, 17, 14, 14
  - The "count once" rule for shared repairs is filed only in the solution.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25,000 rows | 14 / csv, pdf, xlsx / 36,008 rows | yes |
| Distractors in metadata, none named by file | 2+ | 3 (soil resistivity, one-call tickets, class location study); names carry no label | yes |
| Distractor unused yet weighty | yes | not load-bearing per thread; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | mileposts 2 dp, depths and feet 1 dp; the repair ask's unit (repair counted once) is not stated | partial |
| Rubric 25+ criteria | 25+ | not generated here; 34-row schedule plus asks plausibly reach it, unverified | unverified |
| Reads as real, not LLM | yes | thread found no disclosures; one minor R-6 date oddity (RMU 4 Oct 2016 vs inspection remark 15 Nov 2016), touches no figure | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's stump sentence and its R3 line (full-life rate, 0 digs) match the thread's easy route (pipe-age rate, 0 digs, Yes), and the declared distractors are not named as the surface read. Gate G is consistent. The mismatch is that the design note calls the decisive step "dating growth from the failure day" and treats the rate as derived, while the files never file that estimand, so the thread finds the decisive step analytical only conditionally.

Gate H: domain pass (ILI growth projection by CP exposure to schedule digs); layers pass; decisive_step analytical (conditional). Pinning the rate as a formula turns it into rule application, so file the WHAT (wall loss accrues only while the zone is without protection, none before the failure) and not the formula.

## Stump power (Gate F)
A strong solver who dates failures from the RMU and stops R-7 and R-3 at restoration lands the golden, since depth over exposure is the natural rate. The failing easy route is the textbook pipe-age rate (0 digs, Yes). The stump is real but confounded with the unfiled rate basis. Pinning the exposure WHAT makes the golden the only literal reading and keeps the stump. The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Growth-rate basis unfiled (A1): decisive, flips call and every graded dig figure.
2. Restoration-stops-growth unfiled (A3): 48 or 36 digs under the second reading.
3. Repair unit and length basis unfiled (B): row reading gives 31/19/9 and different months; 63.3 vs 63.4 ft.
4. Failure-date source (A2): minor.

## Next action for the author
Edit Section 6.4 of northline_integrity_plan_section6.pdf in the generator to file that an anomaly's external corrosion occurs only while its zone is without cathodic protection, none before the failure, at a constant rate from the failure to the run, and that wall loss stops on the restoring project's in-service date. File the WHAT, not the formula. Pin the repair ask as each physical repair counted once however many anomalies it covers, with feet as the filed repair length. Then rebuild twice, rerun the free gates and the leak reader, and re-judge. Per the Guardrail, this is the single re-judge after the FIX_NOW, so a SEND_BACK follows the CLAUDE.md dead-design path (re-root) unless the author directs otherwise.
