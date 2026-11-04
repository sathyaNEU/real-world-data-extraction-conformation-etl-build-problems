# determinism-check report (pass 2), task192, 2026-11-04

## Verdict
DETERMINISTIC on the main call, SOLUTION_WRONG on ask 4 (seven of sixteen SAIDI figures).
**Disposition:** FIX_NOW
**Failed gate:** A / C, confined to ask 4. Gates G and H pass. This is an ask-layer repair, not a redesign.
**Stumping type:** mechanism: signal_vs_noise, stumping_family: statistical_rigor, surface_read_dependency: no, sole_data_defect: no

## Why
MLR-2 (breaker MLR-F2-52 to R-2207 at MLR2-P071) is forced: 11 same-phase, same-current momentary faults on separate days against 7 on R-3114, nobody else above 4. Asks 5 (MAIFI-E) and 6 (CEMI-2) reproduce 16 of 16. Ask 4 reproduces 16 of 16 only if an unticketed lockout starts at the lockout opening. DRP-04 2.5 says momentary operations ending in a sustained interruption are part of it, and all 73 ticketed lockouts start at the first operation (e.g. BLV-F1-52, 14 Feb 2026: first trip 09:45:23, lockout 09:45:40, ticket Out 09:45). The literal reading starts the nine unticketed 2026 lockouts at the first operation. The golden's "at the log's times" is only in SOLUTION_STEPS, not in a shipped file.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MLR-F2-52 phase C faults | 11, 1,423-1,448 A | 11 on 11 days, same range | yes |
| R-3114 phase A faults | 7, 996-1,005 A | 7 | yes |
| Next largest cluster | at most 5 | 4 (BLV-F3-52 B) | yes |
| Customers behind MLR-F2-52 / R-3114 | 2,625 / 863 | 2,625 verified; 863 not recounted | partly |
| Major event days | 19 May, 27 Jun, threshold 38.03 | 618.6 and 1,405.4; next day 21.1 | yes |
| Ask 5 MAIFI-E, all 16 (CTR-1 43.00) | as filed | 16/16 match; CTR-1 43.00 | yes |
| Ask 6 CEMI-2, all 16 | as filed | 16/16 match | yes |
| Ask 4 SAIDI, nine feeders (BLV-1, BLV-2, BLV-3, CTR-2, MLR-1, MLR-3, NYD-1, NYD-3, NYD-4) | as filed | same under both readings | yes |
| Ask 4 CTR-1 / CTR-3 / MLR-2 / NYD-2 | 146.6 / 76.8 / 139.8 / 412.9 | 146.8 / 77.1 / 140.1 / 413.2 | no |
| Ask 4 SYC-1 / SYC-2 / SYC-3 | 153.2 / 127.5 / 356.4 | 153.9 / 127.8 / 356.7 | no |

CTR-1 43.00 check (builder's claim): it holds. The thread reproduces 43.00 and 44.44 appears only without the five-minute dedupe. The fuse-blown-in-the-minute exclusion changes nothing at two decimals, so the 17 June fuse outage is absorbed under every literal reading. Consistent with SF15, SF17 and SF22 to SF24.

## Competing answers that survived
- Ask 4 start of an unticketed lockout: lockout opening (golden) vs first operation (literal 2.5, ticketed practice). Moves seven figures by 0.2 to 0.7 minutes. No shipped sentence closes it (DRP-04 2.7 times a recloser's momentary interruptions from its event log but does not say where an unrecorded lockout starts). SF22 in the design note covers OMS vs SCADA times, not this.
- Main call, residual and non-flipping: clustering tolerance (2 percent) and window (since 1 Aug) unfiled, every reading prints MLR-2; recency tie at 7 each, count, duration and customers all favour MLR-2; stretch scope (breaker zone per 5.4 vs narrowed sub-span).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | csv, xlsx, pdf, geojson (4) | yes |
| Large file | 25,000+ rows | service_points 35,909 rows; lightning and weather files | yes |
| Distractors | 2+ in metadata.json, none named in a file name | 3 (vegetation, blinking-lights, lightning), none labelled | yes |
| Distractors unused yet weighty | yes | judge: unused by the solution, relevant | yes |
| Deliverables | 1-3 in golden | 2 (xlsx, svg), both present | yes |
| Asks multi-dimensional, unit and rounding | yes | 16-feeder indices with unit and rounding in the prompt | yes |
| Prompt shape, 25+ criteria | yes | 16x3 graded cells plus call and second choice | yes (by count) |
| Reads as real, not LLM | yes | judge found no provenance leakage; golden realism not re-audited here | yes (unaudited) |
| Ask 4 reproduces | yes | 9 of 16 | NO (A/C) |

## Gate G reconciliation
Thread: mechanism signal_vs_noise, stumping_family statistical_rigor, surface_read_dependency no, sole_data_defect no. No shipped artifact ranks candidates wrongly; the declared distractors are not named as the surface read carrying the task. The design note's Three rules agree: the failing insulator leaves only its own flashovers in the relay records, executing DRP-04 files NYD-3, and the enumerated family never puts MLR-2 first or second. No mismatch. (I read the design note, not the card file, which I did not locate; a card check is left to the main thread.)

## Gate H
domain pass, layers pass, decisive_step analytical (precursor fault-signature detection per protective device). The easy route is the feeder with the worst aggregate index (NYD-2, 47.18 MAIFI-E). Matches the note's No decoy, Not semantics and Not rule application lines.

## Stump power (Gate F)
Moderate. A strong solver who rebuilds the signature from relay currents lands on MLR-2, and SYC-3 is a near-identical second. Most weight is lost in the asks (SAIDI, MAIFI-E, CEMI across 16 feeders). The thread's note that a strong model reading the relay currents will see the 11 equal 1,4xx A trips is a landable-call warning for the main thread to weigh against the ladder.

## Findings, ranked
1. Ask 4 seven SAIDI figures wrong under the literal first-operation start (Gate A/C, ask-only).
2. Second-choice rationale is three points, gradable but soft.
3. Clustering tolerance and window unfiled in the solution text (no flip).
4. 863 customers behind R-3114 not independently recounted.

## Next action for the author
Regenerate ask 4 in the golden xlsx, the SVG (it plots minutes) and submission.md answer 4 for CTR-1 146.8, CTR-3 77.1, MLR-2 140.1, NYD-2 413.2, SYC-1 153.9, SYC-2 127.8 and SYC-3 356.7, and change SOLUTION_STEPS step 5 so an unticketed lockout starts at its sequence's first operation; add an SF row to the fork table for it and assert it in checks.py. The alternative (a sentence in DRP-04 2.7 pinning the lockout opening) changes the shipped pack and needs a rebuild and re-judge, so it is not preferred.
