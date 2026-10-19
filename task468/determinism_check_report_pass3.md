# determinism-check report, task468, 2026-10-19 (pass 3)

## Verdict
NOT_DETERMINISTIC (supplementary ask 4 only; the main call and asks 1, 2, 3, 5 are forced and reproduce)
**Disposition:** SEND_BACK (ask 4 fix changes what solvers see; main call, stump and other graded figures stay frozen)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Ask 4's golden counts rest on a rule no shipped text states: a stop whose spring-feed position lies 55 to 112 m from Facilities' inspected position (32 of 484 stops) is treated as moved, and only work orders completed April 5 to June 30 can give it a shelter; `Relocate shelter` is read as "shelter arrives at this stop code". A literal reader joining the spring stops to the inventory by stop code gets different counts for every route. Taxonomy: underspecified_objective (data-semantics fork), Gates C and E fail for ask 4. Evidence for the golden reading exists (January feed and Facilities coordinates agree, spring feed does not; work-order sheet note that shelters change only under a work order) but no file says the stop moved.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counting days | 125 | 125 (guidance 3.4) | yes |
| Departures / no trip | 106,687 / 17,112 | same (Arbor + Quinnell conformed) | yes |
| Review bus-days listed by month | per PDF | 1,350/1,244/1,451/1,392/1,350/1,392 | yes |
| Route 17 share of Transit Mall no-trip (weighted / unweighted) | 56% / 35% | 56.4% / 35.1% | yes |
| Route 17 lowest hour | 4.8 | 4.76 (6 a.m.) | yes |
| Other lowest hours | n/a | R2 4.77, R4 4.82, R6 4.72, R11 5.62, R22 4.86, R40 4.86; R9 3.72, R14 3.13, R31 3.46, R51 2.91 | verdicts yes |
| Ridership order | 2,4,6,17,22; R11 first out | same | yes |
| Ask 4 under golden rule | 15,16,8,6,9,10,13,8,7,12,13 | identical | yes |
| Ask 4, no move rule | n/a | 13,14,6,4,7,8,10,6,5,10,12 | differs on all 11 |
| Ask 4, relocate read as "away from" | n/a | R9 7, R31 8, others unchanged | differs on 2 |

## Competing answers that survived
- Ask 4 fork 1: stop-code join with work-order adjustments only gives 13,14,6,4,7,8,10,6,5,10,12 against the golden 15,16,8,6,9,10,13,8,7,12,13 (routes 2,4,6,9,11,14,17,22,31,40,51). No shipped rule closes it.
- Ask 4 fork 2: "Relocate shelter" as removal at the stop code gives Route 9 = 7 and Route 31 = 8 (golden 6 and 7). Not closed.
- Main call forks tested (weight by n_b alone, by month, counting-hour or weekday n_b, mix by weekday or by hour bands, renormalising without out-of-service): all give the same verdicts and five; minimum margin over 4.00 is about 0.7 and failing routes sit 0.3 or more below. None survives.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf, zip (4) | yes |
| Large file | 25,000 rows or more | 83,843 rows (Quinnell); Arbor larger | yes |
| Distractors | 2 or more named in metadata, none labelled in file name | title_vi_service_monitoring_2025.pdf, farebox_revenue_by_route_2026h1.xlsx; judge found them usable | yes |
| Distractor unused yet weighable | yes | judge: usable, not used by solution; arithmetic check of a rival answer not separately done by me | yes (partial) |
| Deliverables | 1 to 3 | 1 xlsx | yes |
| Asks | multi-dimensional, unit and rounding stated | counts and verdicts stated; ask 4 unit is a count of stops; not individually audited for rounding wording | yes (partial) |
| Prompt shape and 25 criteria | identifiable, 25 or more | shape 01 in metadata; rubric not generated in this folder, not verifiable here | not verified |
| Reads as real / not LLM | yes | judge found nothing exclusion-level | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. This matches the design note's account (design-weighted attribution of unmatched departures; the raw mix of the review files Routes 2,4,6,22,11 and the proportional share-out files 2,4,9,22,11). The declared distractors (Title VI report, farebox) are not named as carrying the task. Gate G line: pass, no shipped artifact ranks the candidates wrongly on the decision question; the difficulty survives deleting wrong numbers. No mismatch with the card.

Gate H line: domain pass; layers pass (Layer 1: Arbor/Quinnell cutover, UTC vs Central, renumbered stop ids, repeated file heads, January vs spring feed; Layer 2: design-weighted attribution of no-trip departures against four per hour); decisive_step analytical (the unweighted tally of the 2,400 reviewed events is the wrong easy route, giving 4,6,11,22,40).

## Stump power (Gate F)
Good. The review samples one event per bus-day, so inclusion probability falls with that bus-day's no-trip count. The month-only or raw mix puts Route 17 at 3.59 and Route 2 at 4.33 (both fail) and files 4,6,11,22,40. The design is stated in the review PDF, so it is reachable, but the within-bus-day 1/n_b step is one that strong analysts skip. Moderate risk of too easy only for careful readers of the sampling paragraph; not a determinism concern.

## Findings, ranked
1. Ask 4 moved-stop rule and "Relocate shelter" meaning are unstated (SEND_BACK).
2. Rubric criteria count not verifiable from this folder.
3. Hygiene: clean.

## Next action for the author
Run /fix-determinism for ask 4 only: in the prompt state that stops are taken at their positions in the April 5 feed and that a shelter exists at a stop only where Facilities' inventory or a completed work order places it, with a relocation order meaning the shelter now stands at that stop code (file the WHAT, not the move-detection HOW), or ship a Facilities/Operations note on the spring stop moves. Ask 4 then needs a rerun; the main call and asks 1, 2, 3, 5 stay frozen.
