# determinism-check report, task147, 2026-11-02 (pass 3)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope: reship after the leak-gate repair (pms_export_notes.txt and folder_contents.csv dropped, a reservation-status crosswalk sheet added to pms_code_lists.xlsx) and the ask rework (Ask A on the task log, payroll overtime lines, staff access events and day-badge log; Ask B and its invoice and framework agreement cut). target.zip md5 d05e2f5675e879ceae9dcc277575bd23. One isolated thread (sonnet, medium) on a fresh unzip of 16 files; its verdict is at /tmp/determinism-check-task147-1793579533/verdict.md. Prompt file is prompt.txt (not legacy).

## Why
The 2027 book at the extract holds Fri 13 and Sat 14 Aug at 480 each. Replaying each past season's later stayed bookings whole (a stay is taken only if every night has a room) puts the closing week 23 to 29 Aug first (about 413 room-nights over 380, nearest hundred 400) and the concert week 9 to 15 Aug second (about 211 to 226, nearest hundred 200). The order holds under every stay-constrained variant the thread ran. The per-night pickup route puts the concert week first at about 550 to 620, and that is the wrong answer a careful analyst files. Every cell of the 2026 table reproduced from the task log, timesheets, app and HR lists, access events, badge log and payroll lines, each with one supported reading of who did the room and on which day.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 13 and 14 Aug 2027 book at extract | 480 each | 480 each (pms_reservations_extract, RES rows without cancelled_utc) | yes |
| Stays after the cut touching aligned Fri/Sat, concert week's other five nights | about 420 | 460, 441, 372, 459, 389, mean 424 | yes |
| Give-back on concert nights | about 20 a night | about 21 (17.5 by rate code, 3.5 event rate) | yes |
| Concert week excess over 380 | about 200 | 211 (mean nightly), 226 (mean of weekly), 232 (median) | yes at nearest hundred |
| Closing week excess | about 400 | 413 (338 to 437 by season) | yes |
| Week 4 | below the concert week | 143 to 156 | yes (order); 156 under mean-of-weeks also rounds to 200, a figure tie on the unasked week only |
| Ask 3, 25 cells (920/1,100/184/206/17.25 ... 962/1,574/187/276/14.25) | table in submission | all 25 equal | yes |
| Overtime raw weekly sums vs golden | n/a | 17.75, 21.5, 15.75, 12.25, 15.0 raw; golden after removing 7 lines for days the attendant was not in | yes |

## Competing answers that survived
None on a committed figure.
- Concert week first: arises only from per-night pickup capped at 480 (554 to 618), which ignores that the full nights refuse the stays crossing them. Not defensible once HK-04 s2.2 and 2.3 and the extract's stay structure are read.
- Raw book with attrition ignored: 479 and 303, which breaks the rounding; HK-04 s2.3 (no-show not occupied) and cancelled_utc rule it out.
- Rooms left with the login's owner on the nine borrowed-login days: 178/204, 104/159, 334/572, 132/245, 173/272 for the Brennock cells. Not supported: no crew member satisfies the went-quiet-before and left-after test on any of the nine days.
- Residual ruled below.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats | 10+ files, 3+ formats | 16 files; csv, xlsx, pdf, json | yes |
| Large file | 25,000+ rows | pms_reservations_extract, 360,694 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | compset_rate_shop_2027-06-30.xlsx and callowfort_tourism_hotel_occupancy_survey_2019-2026.csv; names do not say distractor | yes |
| Distractor behaviour | unused by solution, relevant, ruled out by a shipped fact | rank nothing; compset shows 13 and 14 Aug sold out, consistent with the call | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pdf, both in golden; no format family required | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states nearest hundred, whole rooms, quarter hours; ask 3 is 25 cells across weeks, crews and overtime | yes |
| Prompt shape, rubric | shape identifiable, 25+ criteria | shape `other`, about 40 criteria per the design note (not regenerated here) | yes |
| Reads as real, not LLM | per thread hygiene | PASS; realistic noise (Min 2 nights cell, Sent home note, mixed payroll date formats); no authoring leakage | yes |

## Gate G reconciliation
Thread: mechanism forecasting with a binding stay-through constraint; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no (on clean data per-night pickup is still wrong). Card and note: stump_class analytical; analyst_test says the easy route (per-night pickup, capped, or a pace ratio) files the concert week at about 600; the stump is simulating by stay. These match, including the easy-route number (thread 550 to 620; note 600). The thread names no declared distractor as the surface read carrying the task: compset and tourism survey rank nothing. Gate H: thread domain pass, layers pass, decisive_step analytical; the note's Three rules (No decoy, Not semantics, Not rule application) say the same, with the swap test against a megawatt-hour forecast in agreement. No mismatch. Small numeric offset only: the note's golden is 408 and 180, the thread's is 413 and 211 to 226, same bins.

## Stump power (Gate F)
Good for an analytical reason: a strong analyst who cleans the data and reads HK-04 correctly still files the concert week at about 600 by forecasting each night from its own pickup. The decisive step is the resample-the-independent-unit move of the simulation task type, not a standard method a solver lands on by default, so the thread's analytical classification is not a standard-method landing. Ask 3 adds a second layer that a careless reader misses (borrowed logins, temp logins still held as crew, overtime paid for days the attendant was not in). The pair's ladder against the 60 build target stays with the main thread and the design note.

## Findings, ranked
1. Residual item, ruled: closed by coverage, not a second figure. The access and badge files begin on 1 August, so the absent-attendant test cannot be applied to 27 to 31 July. I checked the task log itself. On every borrowed-login day in August (nine login-days) the lent login starts closing at about 08:48 to 12:18 with 6 to 11 rooms, against 07:15 to 07:35 starts and 11 or more rooms on all ordinary crew logins. In 27 to 31 July no crew login shows that signature: every login starts 07:16 to 07:32 with 11 or more rooms. Design note line 427 records that no lent day falls before 1 August. So the files hold no lent day in the uncovered window, the reading "no event, therefore absent" would reassign the whole week and is incoherent, and the only coherent literal reading (the test applies where the files cover it) gives the golden's week-1 figures. Stating the coverage in a document would describe the data, which the reship brief bars, so no sentence is to be added. Ruling: no fix.
2. Correction to the thread's wording: it says week 1 cells equal the unflagged counts. They do not: 1 August (rkieran) is in week 1, so the golden's 184 and 206 differ from the unflagged 178 and 204. The ruling above is unaffected, since the difference comes from 1 August, which the files cover.
3. Optional wording notes from the thread (step 6 "the regular's who was in", step 5 "about 600" is the unattrited per-night variant, about 550 with attrition) move no figure and need no change; the submission is the author's, not edited here.
4. Cross-batch fingerprint was not run by the thread (no other task folder may be opened); guard.py heart and surface own that gate.

## Next action for the author
Ship as is: no change to the pack, prompt or submission is needed for determinism; the reship proceeds on the remaining gates (leak.py, guard.py heart and surface, voice-check).
