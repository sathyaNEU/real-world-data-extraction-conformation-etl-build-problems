# determinism-check report, task461, 2026-11-04

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: other (etl_conformance plus method selection), stumping_family: analytical_non_defect (declared) but unfiled-rule in effect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (38.4 t, over the 20 t limit by 18.4 t) rests on bays 4 and 5 releasing 37.3 t. That needs three things no shipped file carries: (1) the vapour a load displaces is the previous cargo's, not the loaded liquid's; (2) a saturation factor of 1.0 for petrol vapour from a vapour-balanced drop and 0.6 for diesel's own vapour; (3) a loading-loss equation with its constants. Protocol 4.1 only says a release is estimated "by a recognised estimation method"; 4.2 to 4.4 and Tables 1 and 2 give vapour pressure and molecular weight per liquid, and 4.4 ties the estimate to the temperature and volume "the loading meter records for the load", which is a diesel load. Read literally, bays 4 and 5 are charged at diesel's vapour pressure: about 0.3 t, year about 1.4 t, within the limit. The design note itself enumerates this family (1.34 to 1.76 t across saturation 0.5 to 1.45) as what executing every filed rule produces. The golden is a method choice that no filed sentence selects and no shipped measurement separates.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| VRU-1 stack (CEMS) | 1.1 t | about 1.08 t (VOC_OUT2 mean 2.06 g/min) | yes |
| TK-1 kg | 1,723 | 1,724 (Tables 3, 4; work orders; ship outturn) | yes, rounding |
| Diesel at bays 4 and 5, own liquid | about 0.3 t (golden's own wrong alternative) | about 0.3 t | yes |
| Bays 4 and 5 | 37.3 t | not reproducible (needs unfiled S and equation) | no |
| 33.9 ML of 143.2 ML | as stated | not recomputed | not checked |
| Stock account kL | as stated | not recomputed | not checked |

## Competing answers that survived
| Reading | Bays 4 and 5 | Year | Over limit |
|---|---|---|---|
| Diesel own vapour at the meter liquid (literal protocol 4.4) | about 0.3 t | about 1.4 t | no |
| Previous-cargo petrol vapour, S 1.0 (golden) | 37.3 t | 38.4 t | yes, 18.4 t |
| Previous-cargo rule from the terminal's own exports only | smaller (misses 31.1 t of Selwyn Point petrol) | n/a | n/a |
| Previous-cargo with other S (0.6 to 1.45) | unfiled, different | different | varies |
No shipped rule closes any of these. Even a solver who adopts the previous-cargo concept has no filed S.

## Does the decisive step depend on method knowledge no shipped file carries or forces?
Yes. Confirmed. The previous-cargo concept, the saturation factors and the equation are absent from the protocol, the licence and the survey. Nothing shipped forces them.

## vr1_hose (confirmation and one correction)
The thread's statement "Y on all 24,593 docket lines" is slightly off, but its conclusion stands. I counted: vr1_hose is Y on 24,593 lines and blank on 20,809. The 24,593 equals every petrol line (Unleaded 91 12,990, Premium 95 7,866, Premium 98 3,737), and the 20,809 blanks equal every diesel line. So the column is a petrol-product flag and is perfectly redundant with product. It does not say which petrol drops went through a service station's vapour balance versus not, and it does not distinguish anything the product column does not. The design note (fork row SF6) claims "the docket's vr1_hose column records the balance on each drop"; that is not borne out as a discriminating field. Nothing in the licence, protocol, survey, shift log, CEMS or sites file names vapour balance, a previous cargo or a saturation factor (a keyword search of the PDFs and CSVs found none of these concepts).

Does any shipped measurement separate previous-cargo from loaded-liquid? No. Bays 4 and 5 are unmeasured (CEMS covers VRU-1 only, licence O3), so no observed mass at the uncontrolled bays can arbitrate. Only the stated outcome distinguishes them; the data is silent.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | dockets 45,402; CEMS about 35k | yes |
| Distractors in metadata.json, none labelled by name | 2 or more | 3 (bom daily, stack survey, delivery_sites) | yes |
| Distractor unused, relevant, ruled out by shipped fact | each | stack survey and weather plausible; not individually verified for arithmetic trap | partial, not checked |
| Deliverables | 1 to 3, all in golden | 3, all present in prompt and golden | yes |
| Asks multi-dimensional, unit and rounding stated | each | quarterly by point, per tank, per tank per quarter; rounding stated in prompt | yes |
| Prompt shape identifiable, rubric 25 or more | 25 | shape "other"; about 40 gradable figures in the golden, rubric not shipped | likely yes |
| Reads human, goldens realistic | yes | no LLM disclosures; goldens not reviewed here | yes |
| Gates B, C, E (the thread) | pass | fail, external_dependency | NO |

## Gate G reconciliation
Thread: mechanism other, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, gate_g method_or_model_selection, decisive_rule_filed false, official_decoy false. Declared distractors (weather, survey, sites) are not named as carrying the task, so the distractor is not too load-bearing. Gate G itself does not fire; no shipped artifact ranks candidates wrongly. The mismatch is on whether the rule is filed: the card says decisive_rule_filed false, and the guard bans a decisive rule left unstated. That is exactly this build.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step rule_application (borderline hidden rule). Card analyst_test and domain_test argue analytical and domain-native; the domain claim is fair (loading-loss estimation is what the field does, and the swap test fails on other nouns). But the card's own analyst_test concedes the strong analyst's easy route is the literal protocol route, and the design note's Not-rule-application line says "no filed rule says which vapour a load displaces". A decisive step that is a withheld method with the literal reading giving the opposite call is the banned hidden-rule form, not analysis the data forces. Per the stump power note: the field's standard method (AP-42 loading loss) is a textbook route, but here the solver cannot even reach the golden by applying it, because S for vapour-balanced service is not shipped. This is the worse case: neither a landable call nor a reproducible one.

## Stump power (Gate F)
Hard for the wrong reason. A strong solver follows protocol 4.4 and files "within the limit", which is the literal answer, not an analytical error. A solver who guesses the previous-cargo idea still cannot reproduce 37.3 t without the S values. The ladder cannot be argued to separate solvers by analysis.

## Findings, ranked
1. Decisive rule (displaced vapour is the previous cargo's; S 1.0 and 0.6; the equation) unfiled; literal reading gives the opposite call (Gates B, C, E).
2. vr1_hose is redundant with product (Y on every petrol line, blank on every diesel line); the design note's reliance on it as the balance record is wrong, so no field marks vapour-balanced drops.
3. Gate H decisive_step is rule application or a hidden rule.
4. 37.3 t, 33.9 ML and 143.2 ML and the stock-account figures were not independently reproduced (the first needs the unfiled factor).
5. Tank, CEMS and stock-account asks reproduce or are forced by filed rules and can be kept.

## Next action for the author
Re-root the main call: either (a) file the WHAT in the protocol (the release at a bay is the vapour displaced from the compartment, saturation by the service the compartment last carried, with the liquid-by-service table and a recognised equation stated), which converts the decisive step to rule application and so fails Gate H, or (b) replace the main call with a quantity the field estimates from filed rules where the data separates the candidates (for example a shipped measurement at the uncontrolled bays, such as a stack or ambient test, that the previous-cargo reading reproduces and the loaded-liquid reading does not). Option (b) is required to pass both determinism and the three rules. Keep the tank, CEMS and stock-account asks as asks.
