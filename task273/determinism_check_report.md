# determinism-check report, task273, 2026-10-22 (pass 1)

## Verdict
NOT_DETERMINISTIC (asks 2 and 3 only; the main recommendation and ask 1 are forced)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (stratified induced exposure against a VMT denominator), stumping_family: method_selection, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (fresh unzip of the target.zip with md5 4c8e07aac903ee4ceade58cf0fc79c5f, inlined blocks only) reproduced every golden figure, but the prompt said "all the crashes its drivers caused" while rule 4.1 defines "Crash" as two or more motor vehicles in transport and says single-vehicle events "are not counted". Read literally with the defined term, asks 2 and 3 give different figures from the golden, which counts crashes of any kind (competing_defensible_answer / prompt_ambiguity, Gate C). A softer issue: persons listed twice in the same unit (non-motorists with a blank seat) had to be collapsed, and register deaths matched one-to-one to persons, for the golden to reproduce. The dictionary never said persons are repeated.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Crashes with 2+ vehicles in transport | 124,753 | 124,753 | yes |
| Crashes caused: taxi / ride-hail / limo / shuttle / paratransit / parcel / app / private | 1,564 / 6,762 / 558 / 648 / 865 / 3,317 / 3,282 / 91,211 | same | yes |
| Strata; miles | 288; 60,420 M | 288; 60,420 M | yes |
| Struck vehicles, single at-fault crashes | 134,224 | 134,224 | yes |
| Ratios to private | 1.9 / 2.1 / 1.7 / 2.0 covered; 1.2 uncovered | 1.92 / 2.08 / 1.74 / 2.00; 1.21 / 1.22 / 1.22 | yes |
| Ask 2 KSI (74/402/45/63/55/109/136) | as filed | same, only with the extra dedupe above | yes, conditionally |
| Ask 3 cost USD M (505.9/1,979.6/242.4/299.5/279.5/641.9/699.9) | as filed | same, same condition | yes, conditionally |

## Competing answers that survived
- Fork 1 (asks 2 and 3): crashes restricted to rule 4.1. KSI 52/274/30/50/41/63/75; cost 398.2/1,340.2/157.4/226.9/218.7/448.4/443.3. Every figure differs. Closing sentence needed in the prompt.
- Dedupe fork (asks 2 and 3): collapsing duplicates by seat only gives ride-hail 403, parcel 110, app 137 and costs 700.8/642.0/1,981.3. Unstated in the dictionary.
- Fork 2 (miles estimator, main call): fleet or registration counts put all seven uses above 1.5; class-only induced exposure puts ride-hail at 1.38 and paratransit at 1.42; class x hour gives the golden. The thread treated the main call as forced by the data for an expert, but the estimator is not filed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 plus README | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | crashes 176,063 | yes |
| Distractors | 2+ in metadata.json, none in a file name | weather and work_zone_log named; thread also saw DMV registrations, platform reports and fleet returns carry a wrong basis | yes (see finding 3) |
| Deliverables | 1 to 3, all in golden | xlsx and pptx, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 uses x 3 asks, units and rounding stated | yes |
| Rubric 25+ criteria, shape identifiable | 25+ | not verifiable from the folder (no rubric shipped); the 7 x 3 figures plus recommendation point to 25+ | unverified |
| Reads as real, not LLM | yes | no exclusion-level finding from the thread; provenance recorded as constructed, CC0 | yes |

## Gate G reconciliation
Thread: mechanism method/model selection, family method_selection, surface_read_dependency no, sole_data_defect no. The design note (Three rules, Domain test) names induced exposure for a missing denominator, so mechanism and family match. The surface reads that file a wrong set (registration and platform vehicle counts, class-only or hour-only exposure) are not the declared distractors, which are the weather and work zone files. The thread did not class a declared distractor as carrying the task. Gate G: pass. Gate H: domain pass, layers pass, decisive_step analytical.

## Stump power (Gate F)
The thread rates it strong: per-vehicle exposure and class-only exposure each file a wrong covered set. The decisive step is the standard traffic-safety method, which a strong solver takes, so the main thread weighs the thread's result with the scored readers' (stumping 1.3).

## Findings, ranked
1. Prompt population: "all the crashes" collides with rule 4.1's defined "Crash". Fix in the prompt (done in the rebuild, to be re-judged once).
2. Person dedupe is unfiled mess; the dictionary should say persons can be listed again in a unit.
3. The wrong-basis reads (DMV registrations, platform reports, fleet returns) rank the candidates wrongly (all seven above the line) but are not declared as distractors in metadata.json; declare them or confirm a shipped fact rules them out.
4. The miles estimator is not filed; the thread accepted it as data-forced.

## Next action for the author
Pin the asks' population in the prompt and the person-listing rule in the dictionary, rebuild, and send the rebuilt pack to the one re-judge.
