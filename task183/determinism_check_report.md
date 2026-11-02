# determinism-check report, task183, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** SEND_BACK (Gate G: the DMS fault-location log is a wrong-methodology official artifact, and it is the stump, not a declared distractor)
**Stumping type:** mechanism: planted_defect_flip (wrong-methodology official artifact), stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

Runtime note: no `Agent` tool was available. The brief was written to /tmp/determinism-check-task183-1793614319/judge_brief.md. The coordinator spawned the single sonnet thread, and its verdict is /tmp/determinism-check-task183-1793614319/verdict.md. Input: prompt.txt (not legacy), target.zip md5 a11364baec2f5b19cd19ed09cf133325, submission.md.

## Why
Every golden figure reproduces from the shipped files on a literal reading. Main call: 40 TRIP rows in 2026 (36 phase, 4 ground); the 24 section-7 trips sit at mile 6.91 to 7.14, at least 0.3 mi from any boundary. They are unchanged under larger, mean or smaller faulted-phase current, collapsing the 04/18 shots, or any window, ground-trip, duplicate or mile-versus-pole reading. The line model reproduces the study's 3.36 kA and 2.91 kA at mile 1.9. The block fails Gate G, not determinism. `dms_fault_location_log.csv` is an official, validated-looking artifact that locates the same 24 trips in section 9 (mile 8.58 to 8.88). It is right only before mile 3.6, and the main call stumps only because it is wrong. On clean data the DMS log would give section 7 directly, so the clean-data test fails. The DMS log is not named in `metadata.json` as a declared distractor (those are the pole inspection and member contacts files), so the Gate G exception does not apply.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2026 trips (r1407_event_history.csv) | 40 (36 phase, 4 ground) | 40 (36, 4) | yes |
| Section 7 trips / miles | 24, mile 6.9 to 7.1 | 24, mile 6.91 to 7.14 | yes |
| Next-largest section | at most 4 | section 2, 4 trips | yes |
| DMS cluster | mile 8.6 to 8.9, section 9 | 8.58 to 8.88, section 9 | yes |
| Section 7 ends | SW1406 F14-0132 mile 6.4; SW1407 F14-0149 mile 7.5 | same (docx and GIS) | yes |
| Lateral counts L05..L18 | 34 28 74 39 47 6 44 35 6 6 30 35 25 22 | identical | yes, all 14 |
| Section net costs S1..S14 (hundreds) | 2500 2200 900 2700 500 400 1100 3700 400 800 1100 400 1300 1100 | identical; all more than 20 dollars from a rounding edge | yes, all 14 |

## Competing answers that survived
None on the main call.

- **Main call, conductor legend:** no shipped file maps RAVEN to a C-3 row, only by industry convention (RAVEN = 1/0). Read as 4/0, the cluster moves to mile 8.27 to 8.40, section 8, 23 trips; read as #2, to section 6. The thread judged 1/0 forced for an expert. The ground-fault currents at the two crew poles sit nearer the 1/0 values. This is a soft Gate B note, not a surviving fork.
- **Lateral ask, planned outages:** the prompt says "lost power", not "unplanned". The literal reading gives L07 74. Excluding planned outages gives L07 3, with L11 unchanged. This is a soft fork, with the literal reading as the golden.
- **Lateral ask, other readings (all rejected by the shipped text):**

| Reading | Result |
|---|---|
| No merge of overlapping outages | L13 48, L16 36 |
| Ignore connect dates | L07 76, L12 36, L16 37, L17 26 |
| Include finaled meters | L06 29 |
| Threshold 3 or more | L10 37, L13 48, L14 33 |
| Threshold 5 or more | L05 1, L07 3, L11 44 |
| Count momentary shots | no change |
| AMI log alone | L05 28, L06 24, L07 69, L08 33, L09 37, L10 2, L11 37, L12 27, L13 3, L14 to L18 0 |

- **Section repairs, other readings:**

| Reading | Result |
|---|---|
| REPAIR orders only | S1 1,400; S2 1,100; S3 0; S4 1,600; S7 0; S13 minus 2,900 |
| Positive receipts only (ignore the NSF) | S7 minus 800 |
| Drop the squirrel-guard job at F14-0010 | S1 2,000 |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, docx, json) | yes |
| Large file | 25,000 rows or more | ami_outage_events_2026.csv, 25,701 rows (counted) | yes |
| Distractors | 2 or more, in metadata, none in a file name | 2 named (f14_pole_inspection_2024.csv, member_contacts_blinks_2026.csv). The thread also found pawnee_ridge_airport_daily_2026.csv unused. File names do not label them | yes |
| Distractors unused but weighable | relevant, ruled out by a shipped fact | not separately confirmed by the thread; the pole inspection and member contacts files are plausible feeder-relevant context | partial, not verified |
| Deliverables | 1 to 3, all in golden | 3 (docx, csv, csv), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 14 laterals, 14 sections, miles to one decimal, dollars to the nearest hundred | yes |
| Prompt shape and 25 criteria | identifiable, 25 or more | shape `other`; the design note's ladder gives about 6 call + 4 chart + 14 + 14 criteria (reaches 25 or more) | yes |
| Not LLM generated, goldens real | read as real work products | thread found utility-realistic artifacts, nothing exclusion-level; cosmetic PDF title mismatch | yes |

## Gate G reconciliation
- **Thread:** mechanism planted_defect_flip, stumping_family surface_read_rejection, surface_read_dependency yes, sole_data_defect yes.
- **Design note:** its stump sentence is the same: trust the DMS locator and file section 9, against re-deriving from the currents through the as-built line.
- **Match:** the two agree. The finding is the design itself: the surface read is the DMS log, which is not the declared distractor, and it is too load-bearing. The note calls it field_method (F2/F6, "a correct monitor blind at its configured grain"), but the shipped DMS artifact is the wrong ranker of candidates. A mismatch with the note is not the problem, so the finding is a design-level send-back.
- **Card:** the card's `stump_class` / `analyst_test` / `domain_test` lines were not printed, because my cards query returned no fields.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical` (narrowly). Impedance-based fault location is the field's own method, and the thread read the decisive step as a decoy as well as analysis. The design note's Three rules (No decoy / Not semantics / Not rule application) lines are present. The thread's "Honest note" that the decisive step reads as a decoy contradicts the note's claim of no decoy, so the main thread should weigh it.

## Stump power (Gate F)
The easy route (trust the DMS log, or use the AMI log or REPAIR orders alone) lands a clean wrong answer on all three deliverables. Asks are hard: many lateral meters sit at exactly four interruptions. Note for the main thread: the thread called the from-scratch impedance relocation real analysis, but the stump depends on a wrong official log. Impedance location is also a textbook route a strong solver can take once it distrusts the log, so the landable-call risk (`stumping` 1.3) should be weighed against the design note's ladder.

## Findings, ranked
1. Gate G, banned scaffold: the wrong DMS locator, an official artifact not declared in metadata, carries the main-call stump (retired surface-read-rejection strategy).
2. Soft, Gate B: no file maps RAVEN or SPARROW to a C-3 row. If RAVEN were 4/0, the answer moves to section 8 (23 trips).
3. Soft fork: "lost power" includes planned outages. L07 is 74 on the literal reading, 3 excluding planned.
4. Cosmetic: PDF title metadata says "Overhead Conductors" while the heading says "Primary Conductors".

## Next action for the author
Re-root the main-call stump so it does not depend on a wrong shipped locator. Either make the DMS model correct or drop it, and put the difficulty in the engineering (see the verdict's Fix). The solution blocks need no regeneration, since every figure reproduced.
