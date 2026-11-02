# determinism-check report, task129, pass 3, 2026-11-02

Scope: rubric repair of a shipped build. Main call frozen, the three workbook asks rebuilt. target.zip sha256 d9d05fe69b3939bf60810ca9bc8bac7f8a577e233d1e8a5f29154c03b3c914e1. One judge thread (general-purpose, sonnet, medium) spawned by the main session from my brief (my runtime has no Agent tool); its verdict is /tmp/determinism-check-task129-p3/verdict.md. prompt.txt is current (not legacy).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution (statistical_rigor on the time-since-trim confound), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded figure, the call and all three asks, reproduces from the shipped files. ENG-REL-02 fixes the outage unit, the sustained test, the major event day test and the rate; OPS-ROW-01 section 6 maps each driver to one programme. The rise is real (11.2 to 21.9) and sits in North. At equal time since last accepted trim, North units last trimmed by Garrity and by Hollenbeck run at 0.98 and 1.01 of expected, so neither a re-bid nor catch-up carries it. The 2025 excess climbs with ash share (about 12 to 53 per 100 miles across bands) while 2021-23 is flat near 11, so hazard-tree removal (6.3) is forced. Main-call forks (MED denominator year, sample vs population SD, mean of yearly vs pooled rate, retired-day inclusion) leave the same MED dates and the same rounded rates.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MED dates 2025 | 18 Jun, 9 Dec | 18 Jun (SAIDI 136.3), 9 Dec (90.3); threshold 8.3-8.5; next day 4.98 | yes |
| Coop rate 2025 | 21.9 | 21.92 (910 / 4151.7 mi) | yes |
| Coop rate 2021-23 avg | 11.2 | 11.17 (pooled 11.18) | yes |
| North 2025 / 2021-23 | 30.2 / 11.1 | 30.21 / 11.08 | yes |
| Ask B North | 164 / 6,059 / 1,830,630 | same | yes |
| Ask B East | 128 / 3,674 / 1,217,472 | same | yes |
| Ask B South | 118 / 3,802 / 1,181,773 | same | yes |
| Ask A Hollenbeck Q1-Q4 | 66.5, 80.9, 84.4, 56.6 | 66.49, 80.87, 84.44, 56.57 | yes |
| Ask A Garrity Q1-Q4 | 94.7, 136.3, 114.9, 178.5 | 94.70, 136.34, 114.88, 178.52 | yes |
| Ask C North / East / South | 441.8 / 89.7 / 281.3 | 441.81 / 89.71 / 281.29 | yes (A and C both total 812.8) |
| Time-since-trim shares (0.98, 1.01; North +18.8) | stated in the solution | North attribution ~8.2 of 10.7 points; gradient and contractor ratios consistent | yes (judge reproduced the pattern, not each decimal of 0.98/1.01/18.8; those are the prose support, not graded asks) |

## Competing answers that survived
Two residual forks, both on workbook asks only, neither on the call. The thread judged both closed by the shipped text, at moderate risk.
1. Negative restoration steps (15 rows, all on the two MED days). Golden: split where the device opened again (ENG-REL-02 2.1, one device opening): 164/6,059, 128/3,674, 118/3,802. Counting a ticket as one outage gives 160/5,956, 123/3,559, 112/3,598. Customer-minutes are identical either way. The policy does not say in words what a negative step means.
2. Invoice work month. Golden: period stated in the line text, else service month, a credit memo at the work period of the invoice it reverses (OPS-ROW-01 4.3). Service month only gives Garrity 69.0/156.1/105.5/131.0 and Hollenbeck 98.1/50.1/97.2/43.5, districts 92.8/399.9/257.8; a credit memo in its own month gives Garrity 100.2/130.9/118.1/175.3 and Hollenbeck 66.5/90.2/75.2/69.1. The prompt says "trimming done", and the text-stated work dates are the better evidence.
The thread suggests optional one-clause pins in ENG-REL-02 2.1 and OPS-ROW-01 4.3. Not required to ship, but if the design note's fork table does not already close both with a sentence asserted in checks.py, that is the cheapest hardening.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 5 (csv, parquet, xlsx, docx, pdf) | yes |
| Large file | 25,000+ rows | OMS 30,965 rows; parquet 168,644 | yes |
| Distractors | 2+ in metadata.json, none named in a file name | statewide_cooperative_reliability_2020-2024.csv, ami_momentary_events_2025.csv | yes |
| Distractors unused yet weighable | unused, a shipped fact rules out | thread confirms relevant and not needed by the golden; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 20 figures across 3 grids; prompt states "Rates and miles to one decimal place"; counts and minutes are integers | yes |
| Prompt | one paragraph, under 1,000 chars | 910 chars, question first | yes |
| Prompt shape and 25+ criteria | identifiable shape, 25+ | shape 07 per metadata; criteria total not recounted by me (call plus 20 ask figures plus instruction criteria exceeds 25 by construction) | yes (by construction, not counted) |
| Reads as real work | no LLM tells | thread found no tells; minor note: 67 UNDERGROUND units carry retired_date Jan-Oct 2026 after the invoice cut-off, no effect on 2021-25 figures | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Card/note: strategy decomposition_attribution, Layer 2 estimand_identification, Gate G "the reported rise is correct, and the work is booking it to the right driver", stump_class analytical. Match. The thread's naive paths (re-bid from the Garrity handover, catch-up, raw counts, "weather, nothing new") are the note's default path and declared rivals, not the declared distractors; the two named distractors (statewide survey, AMI blinks) were not named as the surface read carrying the task, so they are not too load-bearing. Gate G classification: no shipped artifact ranks the programmes and gets it wrong; pass.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Thread: utility vegetation management on the regrowth clock and species gradient; Layer 1 invoice layouts, duplicate tickets, species code changes, rebuilt/retired units; Layer 2 age-adjusted attribution by contractor and ash share. Note: Domain test, Not semantics, Not rule application and No decoy lines all agree with the thread. No mismatch with `analyst_test`/`domain_test` on the card.

## Stump power (Gate F)
Good. The easy routes (re-bid at the handover, catch-up, raw rates, nothing new) fail on honest numbers; the answer needs the equal-time-since-trim comparison and the ash gradient. The decisive step is not the field's standard textbook method applied without judgment: the thread did not class it analytical merely because the method is standard. The design note's paper ceiling for the rebuilt asks is pair 28.5 on the ask side (cracker 0 of 20); this is paper argument only, no solver was run.

## Findings, ranked
1. Two ask-level forks (negative restoration steps; invoice work month) have plausible rival answers and rest on a policy clause the thread read as silent in words. Moderate risk, no stump impact.
2. Minor hygiene: 67 underground units with retired_date after the data cut-off. No figure affected.
3. Rubric criteria count not recounted here.

## Next action for the author
Confirm the design note's fork table closes both ask forks with a sentence asserted in `checks.py`; if not, add the one-clause pins (ENG-REL-02 2.1: a negative restoration step means the device opened again and starts a new outage; OPS-ROW-01 4.3: work month is the period in the line's own text and a credit memo takes the work month of the invoice it reverses), rebuild twice byte-identical and re-judge once. Otherwise ship.
