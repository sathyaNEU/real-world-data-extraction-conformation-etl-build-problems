# determinism-check report, task465, 2026-10-17

## Verdict
DETERMINISTIC (SOLUTION_WRONG does not apply)
**Disposition:** SEND_BACK (Gate H: decisive_step = rule_application; the thread's own words: fixing it rebuilds the decisive step)
**Stumping type:** mechanism: etl_conformance (borderline planted_defect_flip), stumping_family: surface_read_rejection (borderline), surface_read_dependency: yes, sole_data_defect: yes

## Why
Run literally, the bundle fixes the answer. Methods note 2.1 states that a district is the total of all its counties, published or not, so the 10 withheld county-years are recoverable. Policy 5.3 with the term sheet defines the expected loss, and policy 5.2 gives the 1.4 threshold. Every graded figure reproduces: buy Ardley (1.08), Elster (1.10), Pallard (1.08); decline Corvin (1.71), Tresham (1.84). The call survives every fork the thread tried. The failure is not determinism but the client's rule 3: a strong analyst who cleans the data and reads every rule gets the golden, so the decisive step is a stated identity followed by a stated formula and a stated test.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 10 recovered yields (pull_2024-03 and pull_2026-10, district rows less published counties) | 11.4, 8.6, 12.5; 10.4, 8.0, 13.2; 9.8, 11.5; 24.5, 22.6 | same | yes |
| Expected loss % (Ardley, Corvin, Elster, Pallard, Tresham) | 6.47, 3.30, 7.46, 4.73, 3.94 | 6.471, 3.299, 7.462, 4.729, 3.942 | yes |
| Multiples | 1.08, 1.71, 1.10, 1.08, 1.84 | same | yes |
| Break-even rate (1.4 x expected loss) | 9.06, 4.62, 10.45, 6.62, 5.52 | same, except Elster 10.45 from the unrounded loss, 10.44 from the rounded 7.46 | yes, with a one-cent rounding fork (Elster) |
| Liability and premium, dollars to the nearest hundred | 827,200/57,900; 2,681,300/151,500; 781,600/64,100; 831,700/42,400; 593,300/43,000 | 827,216/57,905; 2,681,305/151,494; 781,595/64,091; 831,705/42,417; 593,302/43,014 | yes |
| Receipts share, % | 31.8, 21.8, 38.8, 27.5, 34.8 | 31.82, 21.81, 38.82, 27.48, 34.82 | yes |

## Competing answers that survived
No fork changes the call; two reading forks change graded figures:
1. Elster break-even rate: 10.45 (unrounded loss) against 10.44 (loss rounded to 7.46 first). The prompt names rounding of the outputs but not the order. Closing sentence needed in the prompt or policy.
2. Trend-year count: "for each year from that crop year to 2027" read inclusively adds one year of trend (Ardley 6.25 against 6.47, multiples 1.12, 1.79, 1.12, 1.10, 1.90). The calls hold; the graded expected losses and multiples move. The golden uses 2027 minus the crop year.
3. Caveat only: policy 3.1 caps one counterparty at 60 per cent of premium, and buying three covers puts all premium with Quillfield; no file gives the year's total premium and policy 2.1 and 5.4 leave the Board as decider. Policy 5.2 "buys only when" is necessary, not sufficient; the golden reads it as the buy rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, txt) | yes |
| Large file | 25,000 rows or more | clrs_county_estimates_pull_2024-03.csv, 48,354 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | drought_monitor_county_weeks_2000_2025.csv and apgc_prior_covers_2019_2025.xlsx; file names do not label them | yes |
| Distractor weighs but is unused; a shipped fact rules it out | required | drought monitor holds no yield; prior covers settle on published 2019 to 2025 yields for Corvin and Tresham only; neither answers a graded quantity (thread and design note agree) | yes |
| Deliverables | 1 to 3, all in the golden | 2 requested; golden holds county_area_yield_quotes_2027.xlsx (5 sheets, 1 chart on Covers) and a 176-line (175 rows plus header) conformed csv | yes |
| Asks | multi-dimensional, unit and rounding stated | covers x measures, shares, dollars; the prompt's closing sentence states rounding for all | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | metadata names shape 07 (grid of five covers); criteria count not generated at this stage, not checked | shape yes; count not verifiable here |
| Reads as real work | no LLM tells, goldens realistic | thread found no authoring language; I did not run golden-realism | no finding |

## Gate G reconciliation
Card: gate_g forecasting, stump_strategy population_selection, stump_class analytical, decisive_rule_filed false, official_decoy false. Thread: mechanism etl_conformance (borderline planted_defect_flip), stumping_family surface_read_rejection (borderline), surface_read_dependency yes, sole_data_defect yes. The distractors (drought monitor, prior covers) are not named by the thread as the surface read, so they are not too load-bearing. No shipped artifact ranks the covers wrongly, and the declared wrong-basis distractors are ruled out by shipped facts. Gate G line: no Gate G failure on distractors; the reconciliation mismatch is on stump class: the card and the design note declare analytical / population_selection, while the thread reads the difficulty as a data defect (sole_data_defect yes, surface_read_dependency yes, planted_defect_flip borderline).

## Gate H line
domain: pass, layers: pass, decisive_step: rule_application.
Reconciliation with the design note's `## Three rules`: the note says "Not rule application: no file says how a withheld year enters". The thread found methods note 2.1 states the additivity identity, so the file does say how the withheld year is recovered, and policy 5.3, the term sheet and policy 5.2 file the rest. The note's Not-rule-application line is contradicted by the shipped text. Analyst test as written in the card ("recovering each withheld year from the district totals less its published counties buys the right three") is a cleaning and reading step once note 2.1 is read.

## Stump power (Gate F)
Moderate. Published-years-only, district-fill and county-mean fills mostly decline all five (county-mean fill gives Ardley a multiple of 5.35, the opposite of the golden), and zero-yield reading buys Tresham too. A careful solver who reads methods note 2.1 and cleans will probably reach the golden, so the stump rests on cleaning discipline, not on a choice of method.

## Findings, ranked
1. Gate H3 fails: the decisive step (recovery by the stated additive identity, then the stated expected-loss procedure and 1.4 test) is rule application. Design note's Not-rule-application line is contradicted by methods note 2.1. Needs a rebuild of the decisive step.
2. Gate G / stump reconciliation: the thread classes the difficulty as a data defect (sole_data_defect yes), which the client's rule 3 bans as a decisive step; planted_defect_flip is borderline.
3. Elster break-even 10.45 against 10.44: the order of rounding is unfiled.
4. Trend-year count wording is mildly open (inclusive reading moves expected losses by about 0.2 points, the call holds).
5. Policy 3.1 concentration limit could draw a caveat; no effect on the recommendation.

## Next action for the author
Treat this as a redesign, not a /fix-determinism rerun: move withheld-year recovery into Layer 1 cleaning and re-root the decisive step on a quantity the field itself estimates (for example leave the expected-loss method unfiled and have the history pin it by an out-of-sample back-test, or make the 2027 yield level or the co-movement with the cooperative's own receipts the estimate), then re-record the card's analyst_test and the note's Not-rule-application line. The small repairs (state that break-even rates come from the unrounded expected loss; state the trend-year count as 2027 minus the crop year) can be folded in with the rebuild.
