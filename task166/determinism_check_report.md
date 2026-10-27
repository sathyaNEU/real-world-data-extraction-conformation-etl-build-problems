# determinism-check report, task166, 2026-10-26 (round 2)

## Verdict
NOT_DETERMINISTIC (underspecified_objective, ask 1 of onboarding_staffing_2025.xlsx only). The main call, ask 2 and ask 3 are deterministic. The critical-component figures carry SOLUTION_WRONG-class drift (the call and buckets are unaffected).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Southwest at about 600 with Texas & Gulf second reproduces and survives every variant the judge ran (Southwest 575 to 665 against Texas & Gulf 430 to 505). The round 1 nearest-100 problem is closed at the nearest 200. Ask 1 (24 pod-hour cells) reproduces to the cent only under two unfiled readings: (1) "group" = the Field app training and Office hours templates, and (2) a specialist counts in the pod serving most of their sessions that month. Each literal alternative gives different cells. Asks 2 and 3 (36 values) reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| New paying customers 2025 | 1,744 (SW 303, SE 288, TX 388, MW 264, NE 222, Pac 279) | identical | Yes |
| Asks 2 and 3 (18 counts, 18 values) | as filed | identical | Yes, all 36 |
| Ask 1 (24 cells) | as filed | identical only under the two unfiled readings | Conditional |
| Leaver-founded share | about 2 in 5 | 756 of 1,733 = 44% | Yes |
| Median lag | 333 d (10 to 11 months) | 333 d | Yes |
| Founders billing in region left | 88% | 88.5% | Yes |
| Founders per 100 removals | 5.6 | 5.6 to 5.9 | Yes |
| Founders, all years | 4,451 | about 4,000 to 4,050 | No (about 10% low) |
| SW removals Apr to Sep 2026 | about 6,500 | 5,715 (6,337 with closure-tagged) | Ratio 4.07x yes, count no |
| SW 2027 total | 403.8 + 203.8 = 607.6 | about 575 to 585 | Same bucket (600), digits no |
| TX 2027 | 484.4 | about 475 | Same bucket (400) |

## Competing answers that survived
1. Group vs one-to-one never defined (session_type is only "the session template"). Golden: Field app training and Office hours = group (West Q1 323.00 / 47.00). Reading "more than one booking at same host and start" gives 332.00 / 38.00 (Q3 468.50 / 59.00). Reading "attendees above 1" gives 118.25 / 251.75. Closing rule: none shipped.
2. Pod membership by month not filed. Roster is one pod per specialist at 1 Oct 2026. Roster pod gives West one-to-one Q1 333.50, Q3 358.25, group Q4 34.50 against golden 323.00, 459.50, 47.50 (Frances Russell, Mark Simmons, Melissa Hansen moved). Assigning by the case customer's region gives West Q1 320.25. Closing rule: none shipped.
No fork on the main call. Quarter assignment (UTC vs Mountain) is robust; co-host rows and (host, start) are determinate.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | Yes |
| Formats | 3+ | csv, xlsx, pdf, docx | Yes |
| Large file | 25,000+ rows | user directory 256,204; sessions 24,292; register 24,119 | Yes |
| Distractors in metadata.json, none named by file | 2+ | board_deck_2023-03 PDF and onboarding_csat_responses CSV declared; file names do not label them | Yes |
| Distractors unused yet weighable, ruled out by shipped fact | yes | judge found both unused; deck on old map and FY counts, CSAT scores onboarding; neither reproduces a graded quantity as the answer | Yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | Yes |
| Asks unit and rounding | stated | nearest 200, two decimals, thousands to one decimal, whole counts, all in prompt | Yes |
| Prompt shape, 25+ criteria | yes | shape identified; 1 call + 1 figure + runner-up + 24 + 18 + 18 gradable figures (about 63) | Yes (not scored by a generated rubric here) |
| Not LLM generated; goldens real | yes | judge saw no generation language; messy-system realism good; golden-realism not re-run | Yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata (read after the verdict): declared stump is the leaver-to-founder channel found only by linking each new workspace's first user to removals elsewhere; distractors are the 2023 board deck and CSAT file; the note's Three rules claim no decoy, not semantics, not rule application. Match. Neither declared distractor is named as the surface read that carries the task, so they are not too load-bearing. No mismatch. Card fields were not separately opened beyond the note and metadata.
Gate H: domain pass, layers pass, decisive_step analytical (lead-lag forecast of new-logo acquisition, right-censoring corrected). Matches the design note. The thread did not describe the decisive step as a standard method applied with no judgment; it required discovering a latent relationship and estimating the censored rate, so I record no lenient-class flag.

## Stump power (Gate F)
High. Every own-history, trend, season and spend model, and the board-deck and CRM Sales Region shortcuts, file Texas & Gulf (about 480 vs Southwest about 380, both 400). Southwest requires discovering the link, fitting a censoring-corrected rate and pushing the 2026 spike through the lag. A solver skipping the censoring correction lands near 505, on the bucket edge. The Seats line in the planning basis points toward removals; the thread judged a strong model's chance of missing it as substantial but not certain. Hold that language. Note the stump bears on the main call only; the main thread weighs this with the scored readers.

## Findings, ranked
1. Ask 1 group vs one-to-one undefined (underspecified_objective). Cells of 24 differ by reading.
2. Ask 1 pod membership by month unfiled (roster is a single current pod).
3. Critical components and step 3 to 5 figures (6,500; 4,451; 403.8, 203.8, 607.6; 484.4) do not reproduce to the digit (about 5 to 10% off, same buckets). Regenerate from the exact build or soften to "about".
4. Likeliest second-grader dispute: SKU renumbering (100 Pro, 200 Enterprise, 300 Core before the 2026-07-01 catalog) is unstated but forced by contract value vs list and seat price; the thread judged it forced, not a fork. A catalog-literal solver swaps plans. Not a finding against determinism, but watch it.
5. Cross-batch fingerprint not performed by the thread.

## Next action for the author
In the generator, file the WHAT in the shipped pack, leaving the main call and the billing, CRM, user, marketing and planning files byte-identical. Add to data_dictionary.pdf which templates are one-to-one (Kickoff, Admin setup, Go-live review) and which are group (Field app training, Office hours), with a pod-history table (pod, from, to) in the roster or one dictionary line stating the pod a specialist worked in is the pod whose regions most of their sessions served that month. Then regenerate the critical-component and step figures from the exact rebuild, and re-run checks.py, verify.py and figures_check.
