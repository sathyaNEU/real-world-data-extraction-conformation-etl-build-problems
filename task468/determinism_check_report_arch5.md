# determinism-check report, task468 (architecture 5), 2026-11-01

target.zip sha256 2b95ef4209da0565f805001d6c8941420141e73f742d945d5faddd56ebf7aed2. Judge thread scratch: /tmp/determinism-check-task468-1793493282/ (verdict.md there). One pass, one thread.

## Verdict
NOT_DETERMINISTIC (answer_contradicts_files / underspecified_objective on the main call), plus SOLUTION_WRONG on ask 3 (net additional dwellings, unreproduced: golden 348, judge 365).
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection (constant-quality adjustment), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read word for word, hvha_ward_house_price_index_methodology.pdf section 3 defines a pair as two consecutive standard sales of one dwelling and removes nothing else. On that reading Pellbury is 6.0 per cent, over the 5.0 line, so four wards are pressured and the GBP 12M splits over 148 + 96 + 71 + 118 = 433 pipeline homes, not the golden's three. The golden's 3.1 needs every pair spanning a completion certificate set aside. The only filed hook is section 1's "same dwelling at the same quality"; no sentence says building work is a quality change or that certificates are the test. A narrower reading, where only New dwelling, Conversion and Demolition/erection certificates count as the quality change, is equally licensed and leaves Pellbury at 6.0. The main call and asks 1 and 2 (PDF and xlsx) are affected. The design note's own Pins line and fork SF1 concede that deleting "at the same quality" leaves the every-pair index as the literal reading. SF1 is closed only by that same phrase, which the thread finds too thin.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ward index change 2025 to 2026, all 12, set-aside of every certificate | Pellbury 3.1; Calder Bank 7.9; Kestrel Rise 6.7; Abbots Hollow 5.8; others as filed | all 12 equal golden to 0.1 (address matching keeps 218 Pellbury pairs against the claimed 226, index still 3.1) | Yes |
| Index with no set-aside (literal section 3) | not claimed | Pellbury 6.0; Calder Bank 8.0; Dunmore 2.4; Eastholme 4.0; Gorsey Hill 3.8; Hollin Edge 3.9; Moss Brow 2.2; Fennick 3.5 | n/a, competing answer |
| Pellbury with only new-dwelling certificates set aside | not claimed | 6.0 | competing answer |
| Pipeline homes 148 / 96 / 71 (Pellbury 118) | 148 / 96 / 71 | same | Yes |
| Shares 5,638,095 / 3,657,143 / 2,704,762 | as filed | arithmetic from 148/96/71 over 315 | Yes |
| Net additional dwellings 2026 (ask 3) | 348 (Calder Bank 61, Moss Brow 60, Wexley 48 ...) | 365, each ward 1 to 2 higher (Calder Bank 62, Moss Brow 61, Wexley 50); 17 unexplained | NO |
| Affordable starts 2026 (ask 5) | 1540 | raw 1839; removing the Calderstone repeats (about 299) is consistent with 1540; not traced per ward | Partly |
| Category B 2026 entries and money (ask 4) | 525 entries, GBP 160,661,830 | not recomputed | Not checked |

## Competing answers that survived
- Four wards including Pellbury (shares over 433 homes): the literal section 3. Survives as a defensible reading. Shipped rule meant to close it: section 1 "at the same quality", which does not name building work or certificates.
- Narrower certificate reading (new dwellings, conversions, demolition/erection only): Pellbury 6.0, same four-ward call. It also moves Calder Bank 7.9 against 8.0, and Dunmore, Eastholme, Gorsey Hill, Hollin Edge and Moss Brow at one decimal in ask 1.
- Boundary (certificate dated on a sale date), inclusive or exclusive: no effect. Update semantics (A, C, D): robust.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | Yes |
| Formats | 3 or more | csv, xlsx, pdf, eml (4) | Yes |
| Large file | 25,000 rows or more | pp-harrowmere-2015-2025.csv 75,003 lines | Yes |
| Distractors | 2 or more named in metadata.json, no file name labels one | official HPI csv and private rents csv; file names carry no label | Yes |
| Distractors unused yet weighable | yes | official HPI is city-wide with no ward detail; rents are not in the rules' test; neither answers a graded quantity | Yes |
| Deliverables | 1 to 3, each in the golden, no format family required | 2 (pdf, xlsx), both present in submission.md | Yes |
| Asks multi-dimensional with unit and rounding | yes | 12-ward grids, units and rounding stated in the asking sentence (ask 3's "net additional dwellings" is not reproduced) | Yes on form |
| Prompt shape and 25 or more criteria | yes | shape 05 allocation to a fixed total; design note counts about 69 criteria; prompt 814 characters | Yes (by design note) |
| Reads as real, not LLM generated | yes | thread saw no authoring disclosure; goldens read as work products | Yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H line: domain pass, layers pass (Layer 1: legacy and Uniform sheets, address variants, C/D updates, 2019 and 2023 wards; Layer 2: constant-quality repeat-sales index), decisive_step "analytical if the exclusion is filed; as shipped it risks reading as an unstated rule."

Design note and card (read after the thread returned): stump_class analytical, Estimand-identification strategy, Pellbury 6.0 against 3.1, decisive step "matching the council's completions to the sale addresses and setting aside every pair spanning a certificate." The mechanism and family match, and Gate H domain and layers agree. The declared distractors (official HPI, rents) are not named by the thread as the surface read, so they are not too load-bearing. The disagreement is on one point. The note says "Not rule application: no filed rule names building work", and treats the absence of a filed rule as the stump. The judge reads the same absence as an open fork, not a stump. This is the pattern the CLAUDE.md "decisive rule left unstated against a stated one" ban targets. Fork SF1 is closed only by the phrase "at the same quality", and the unfiled set-aside is the decisive step.

Would the thread's fix (file the set-aside in section 3) keep the decisive step analytical? Filing "a pair whose dwelling has a completion certificate dated between its sales is not a pair" names the register, the test and the join. The decisive step then becomes executing a filed rule: match addresses across two systems and drop pairs. That is rule application, the same reading as task445 architecture 2. The difficulty left is Layer 1 work (a keyless address join across the legacy and Uniform layouts), which is not Layer 2 analysis. A WHAT-only filing (the index compares one dwelling at unchanged quality, with the population defined as dwellings unaltered between sales) is closer to legal but, since the pack's only quality evidence is the register, the solver is told where to look and the easy route disappears. Both versions fail the client's check, one on determinism and one on the three rules. The fix as written trades a determinism block for a rule-application block, so I recommend redesign, not repair.

## Stump power (Gate F)
The trap is genuine: a solver who follows section 3 literally and treats the completions file as supply context only files four wards. But that competing reading is licensed by the text, so the stump on this call is partly a reading difference and not a clean analytical failure. The register ships for the supply ask and invites exactly that context-only reading. The golden is the field's standard constant-quality route once the quality issue is spotted. A strong solver who reads "at the same quality" and checks the dwellings' own change lands it, so the call is landable; the main thread should weigh it against the note's ladder (rung 3 as the only route to the golden).

## Findings, ranked
1. Main call, open fork: section 3 never states the set-aside; literal execution gives four wards (Pellbury 6.0) and a four-way split over 433 homes.
2. Certificate reading: the narrower new-dwelling certificate set also leaves Pellbury at 6.0 and moves ask 1 one-decimal figures for Calder Bank, Dunmore, Eastholme, Gorsey Hill, Hollin Edge and Moss Brow; the work types counted are not filed.
3. Ask 3: golden 348 against recomputed 365 (17 unexplained, 1 to 2 per ward); either the figures or the unstated rule behind them is wrong.
4. Ask 4 (category B count and money) was not recomputed by the thread; ask 5 reproduced only in total.
5. Repair trap: filing the set-aside turns the decisive step into rule application (task445 architecture 2 reading), so the repair is a redesign question.

## Next action for the author
Decide between redesign and a WHAT-only filing; do not run a plain "file the set-aside in section 3" repair, since it makes the decisive step rule application. Before either, trace and fix ask 3 (348 against 365 in the Uniform sheet) and recompute ask 4, then rerun this check.
