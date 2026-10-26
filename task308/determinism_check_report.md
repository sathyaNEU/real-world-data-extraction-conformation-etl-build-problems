# determinism-check report, task308, 2026-10-26

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer / underspecified_objective). The call (University) is robust; supp asks 4 and 6 and the dollar grain are not forced by the shipped text.
**Disposition:** SEND_BACK (the judge's disposition; the fix is prompt text, so any model runs must be redone)
**Stumping type:** mechanism: decomposition_attribution/forecasting (censored-demand estimation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
- Supp 6 (workshop jobs): the golden drops 441 of 1,452 jobs as failed road-test retests. No shipped file or the prompt states this. Literal all-jobs answer is 53.2/32.8/50.7/29.6 (e-bike) and 14.0/16.3/16.9/11.2 (classic); 7 of 8 cells differ from the golden.
- Supp 4 (people): the conditional card-merge rule is not in the prompt or dictionary (dictionary says only "Token of the payment card"). Per-fingerprint gives 9,413/4,793/7,709/5,064/3,232; per-account gives 9,810/5,078/7,999/5,272/3,383.
- Main and Supp 2/3 (dollars): the estimation grain (month x daytype x hour) is unfiled. Coarser grains move University to 100k or 75k; hour-only ties Central at 75k. University still leads on most grains, but its 125k holds only on the fine grain. The step-5 revenue formula is also not in the files (without the uplift: University 99.8k, Central 36.4k).
- Supp 1, 5 and the recommendation text are forced or consistent. Energy dedup and local-month rule are defensible from the dictionary.
- Unverified risk (not a fork): the pilot e-bike share transferring to University at about 60 e-bikes per station against mean capacity 53.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| University turned away / demand | 29,600 / 205,100 (14.4%) | 29,622 / 205,101 | yes |
| Central turned away | 7,400 (2.5%) | 7,430 | yes |
| Pilot e-bike share | 41.7% | 41.73% | yes |
| Pilot uplift | 4.4% | 4.42% | yes |
| E-bike premium | USD 0.11 | 0.1130 | yes |
| Revenue (golden formula) | 75/125/50/25/25k | 76.3/127.8/47.6/22.7/24.2k | yes, only under the filed grain and formula |
| Revenue, served rides only | Central 50k | Central 52k | yes |
| People | 9,486 / 4,853 / 7,759 / 5,102 / 3,258 | match under conditional merge | yes, only under the unfiled merge rule |
| Energy by month | 212 ... 224 | match | yes |
| Workshop jobs per 10,000 | 49.1 ... 10.2 | match only with the road-test exclusion | no under the literal reading |

## Competing answers that survived
- Workshop jobs: all jobs (literal) against retests dropped; closing rule not shipped.
- People: per account / per fingerprint / conditional merge; closing rule not in prompt or dictionary.
- Dollars: grain of the turned-away estimate (month x daytype x hour against coarser or month x day-of-week) and the uplift form; University 125k against 100k or 75k.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or more | 267,968 rows (rides_2025Q3.csv) | yes |
| Distractors in metadata.json, none named in a file name | 2 or more | 2 (open_data_bikeshare_trips_by_area_2025.csv, vendor_quote_ebikes_2026.pdf) | yes; the open-data file name does not label it as a distractor |
| Distractor unused, relevant | yes | open data counts rides by area (same quantity as the trips, suppressed counts); quote is a vendor quotation; judge found them unusable for the graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks: unit and rounding stated | each | prompt states rounding for revenue, energy, people, jobs | yes |
| Asks multi-dimensional | yes | people by 5 areas, 12 months, 8 quarter/class cells | yes |
| Rubric 25 or more criteria | 25 | not generated at this stage; 3 + 5 + 12 + 8 graded figures plus components exceed 25 | yes (by count) |
| Not LLM-generated, goldens realistic | yes | judge found no provenance or authoring leakage; golden realism not re-read here | yes (not re-read) |

## Gate G reconciliation
Thread: mechanism censored-demand estimation, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; the stump is the rides-served route (Central about 50k) against rebuilt requests (University); the same mechanism. The declared distractors (open data by area, vendor quote) are not named as the surface read carrying the task; the surface read is the served-ride ranking, which is the stump itself. Match, no finding. Gate G passes.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the card (analyst_test: strong analyst takes Central at 50k; domain_test: availability-censored demand) and the note's Three rules. Judge residual concern: "2025 demand" undefined, but choosing requests over rides is an estimand choice. The design note's own SF14 and SF20 show the supp devices (card merge, road-test retest) as deliberately silent; the judge reads them as hidden rules, so the literal-determinism bar is not met.

## Stump power (Gate F)
The easy route (served-rides ranking, Central 50k) is plausible for a strong solver; doing it right needs the stock rebuild from audit, trips and van moves, plus pilot transfer. Risk: a solver reaching University on a coarser grain files a different dollar figure.

## Findings, ranked
1. Supp 6 workshop jobs: road-test retest exclusion is an unshipped rule; literal answer differs in 7 of 8 cells.
2. Supp 4 people: card-merge rule unshipped; literal readings differ in every network.
3. Dollar figures: estimation grain and uplift formula unfiled; University 125k holds only on the fine grain.
4. The design note's SF8 and SF14 claim the readings are "asserted" closed, but nothing quotable in the shipped files closes them.
5. Unverified: pilot e-bike share transfer to University at higher bikes per station (risk, not fork).

## Next action for the author
Run /fix-determinism on task308: file the WHAT in prompt.txt for the three groups (what counts as one job after a failed repair, what counts as one person across accounts on one card, demand as the requests made including those turned away with the estimation grain, or coarsen the revenue rounding), not the HOW.
