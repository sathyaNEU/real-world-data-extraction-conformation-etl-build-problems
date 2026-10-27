# determinism-check report, task204, 2026-10-27

Two passes are recorded here. Pass 1 read a pack that no longer exists (target 61bfc61aa80614e5, golden 720e33b52e02f418). Pass 2 reads the repaired pack (target 4b33e7a0366c08f2, golden 089043e9fd91fc61), copied fresh to /tmp/determinism-check-task204-2/target/. Each pass was one isolated sonnet thread at medium effort; the pass-1 raw verdict is kept beside this file as determinism_check_report_pass1_raw_verdict.md. The target hashes and the gate list are the coordinator's account, not something I re-measured.

## Verdict (pass 2, the pack as it stands)
DETERMINISTIC
**Disposition:** FIX_NOW. The fix is in the submission's solution block (Gate A, below). One further generator pin is recommended for the block aggregation fork (Gate C exposure, below), and one is optional for ANG-016.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Pass 1 (superseded pack): NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer
The thread found that nothing filed fixed the session quadrature. EST-14 s3 then read "each logged reading represents the five minutes beginning at its timestamp", which is a rectangle rule read literally. The golden's trapezoid gave 5.05 to 5.08 (printing 5.0) and the filed rectangle gave 5.37 to 5.60 (printing 5.5), so the headline rate and ask 1 forked. The A-or-B call was forced and unaffected. A staff-count inference on ask 4 and a hours-versus-occupants rounding conflict between EST-14 s4 and the prompt were also noted.

How it was closed (the coordinator's account, checked against the shipped text and the design note):
- EST-14 s3 now reads "Hours in the returns made under this note are counted reading by reading: a logged reading counts as the five minutes beginning at its own timestamp, and falls in the calendar month of that timestamp ... This section governs the counting of hours and of readings and no other quantity." I confirmed this wording in the shipped PDF.
- Block supply rates were rescaled by 0.991. This is not a pin: the licensed constructions now share one half-litre bin.
- EST-14 s4 now files the occupant population (present marks, whichever role, absent and authorised-absent excluded). EST-14 s5 now gives two decimals for hours, whole persons for occupants and one decimal for shares.
- No integration rule was filed. I treat pinning one as the wrong repair, because it files the HOW and turns the decisive step into rule application (client rule 3).

## Why (pass 2)
The main call (option A) is forced. The block's pooled supply is 5.03 L/s per occupant present, printing 5.0, against the 8 required. Option B (moving CON5A, HSC5A, BUS5A and GEN5A out) leaves about 5.7 on the remaining sessions, so only A changes the supply. Every graded figure the thread tried reproduced. The thread found no filed sentence that fixes HOW the rate is obtained, and no gate A to E failure on the main call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Block rate, trapezoid pooled | 5.0 (5.027) | 5.027 | yes |
| Requirement as multiple of rate | 1.59 | 8 / 5.027 = 1.591; 8 / 5.0 = 1.60 | reproduces only from the unrounded rate (Gate A item) |
| CC1 timetabled sessions | 1,728 | 1,728 | yes |
| CC2 occupant-hours | 70,404.6 | 76,805 x 55/60 = 70,404.6 | yes |
| CC3 shortest response time (TUL-G07) | 191 min | 191 | yes |
| CC4 rooms below 8 | 6 of 6 | per-room pooled 5.08, 4.72, 4.73, 5.92, 4.84, 5.15 | yes |
| Ask 2, all 56 occupied-hours and over-1,500 cells | as filed | 56 of 56 to two decimals | yes |
| Ask 3, 14 capture shares | as filed | 14 of 14 (ANG-016 93.7) | yes |
| Ask 4, six mean occupants | 35 / 48 / 37 / 49 / 41 / 56 | 35.3 / 48.2 / 36.7 / 49.4 / 40.9 / 56.3 | yes, none on a .5 point |
| Ask 5, four largest rises | G12 P1 11-02, G12 P1 10-19, G07 P2 10-13, G12 P1 11-09 | 458 / 435 / 427 / 416 ppm, same order | yes |
| Option B residual | 5.696 (the coordinator's measure) | about 5.7 | yes |

Every graded figure the thread tried reproduced. The only discrepancy is the Gate A item: 1.59 does not follow from the printed 5.0.

Uniqueness of the nearest, largest or first asks:
- Ask 5: the fourth rise (416) and the fifth (412) are distinct. Identity and order hold under both end-reading conventions (12 readings, or 11 with the last at end minus 5). Only the ppm magnitudes move, and the ask names space and date, not magnitude.
- Ask 4: no mean sits on a .5 point.
- Ask 1: 5.027 sits 0.223 from its cell edge (5.25), so the printed 5.0 is stable.

## Is the integration rule filed? (the scope-limit test)
No sentence fixes it. The two filed rate sentences are TGD-M4 4.3 ("established in that space and over the periods for which it is timetabled") and 4.4 ("per person present", "over the whole of the period assessed"). Neither files a quadrature. EST-14 s3 ends "This section governs the counting of hours and of readings and no other quantity", and the thread read it as holding to its own subject, so it cannot be taken as an integration rule for the rate. The scope limit fences the sentence off from the rate; it does not file how the rate is found. On this evidence the closure did not narrow what the solver must work out, so the decisive step is not rule application.

The numbers that carry it (every construction in the stored-term family prints 5.0):
- Rectangle backward: 4.972.
- Trapezoid (gold): 5.027.
- Mean-value integral: 5.029.
- Rectangle forward: 5.086.
- That is a spread of about 0.23 of a bin, against the settled read at 9.3 to 10.9, which prints 9.5 to 11.0 and is roughly 8.5 bins away.

This is why pass 1 was repairable and not a redesign. The fork sat inside the decisive step, between constructions that all carry the stored term and sit one bin apart, and the data could close it. It was not a fork at the decisive step itself.

Other constructions the thread ran:
| Construction | Unrounded | Printed |
|---|---|---|
| Trapezoid, 55-min span regardless of missing readings | 5.049 | 5.0 |
| Pooled, denominator all 1,728 sessions | 4.882 | 5.0 |
| Mean of the six per-room pooled rates | 5.072 | 5.0 |
| Outdoor fill variants (Macehead raw, offset-adjusted, interpolated, term mean, constant 420) | 5.007 to 5.037 | 5.0 |
| Outdoor held at 400 ppm | 4.875 | 5.0 |
| Unweighted mean of per-session rates | 5.473 | 5.5, closed by TGD 4.4 |
| Five-minute rectangle with storage over a 50-min window (inconsistent windows) | 5.54 | 5.5, rejected as inconsistent |
| Worst single room (F09) | 4.72 | 4.5, see the aggregation fork below |
| Settled read, integral | 10.93 | 11.0 |
| Settled read, end-of-session reading | 9.29 (9.51 unweighted) | 9.5 |

Two constructions print off 5.0 and depend on inference, not on a quoted sentence:
- The unweighted mean of session rates (5.473) is closed by 4.4's "over the whole of the period assessed".
- The five-minute-a-reading rectangle is excluded because the scope limit takes it off the rate, and because its window (12 readings is 60 minutes against a 55-minute session) does not match the session. The design note's own figures for it are 4.649 holding the window and 5.475 extending it; the first would print 4.5, and the thread did not run it. Both rest on the scope limit and the window mismatch, so the closure of this family is by construction, not by a filed sentence. This touches the printed rate only, not the call.

## Competing answers that survived
| Fork | Answers | Touches | Closed by |
|---|---|---|---|
| Block aggregation (below) | pooled 5.03 (5.0), mean of rooms 5.07 (5.0), worst room 4.72 (4.5) | the printed rate in ask 1 only; not the call (option A holds under all three) | nothing quotable; see below |
| ANG-016 2026-11-13, 288 readings flagged `uncertain` | counted: Nov 127.50 h, share 93.7. Excluded: 120.00 h, 91.6 | asks 2 and 3 (one cell each) only | the literal reading of EST-14 s3 ("a logged reading counts") supports the gold; no data dictionary or filed sentence says flagged readings are excluded |
| Remedy rule | not filed: no sentence says what rate A delivers or when B suffices | the main call's remedy. The thread marks it inference-dependent with no competing answer surviving (B reaches 5.7, short of 8; only A changes supply) | the data |
| Rise magnitude in ppm (ask 5) | differs by end-reading convention (e.g. 458 versus 452) | ask 5 values only, if graded; identity and order are unaffected | not needed for the asked fields |
| "Over" 1,500 | strictly greater (note s2 "passes", prompt "over"); at or above would move 5 cells by 0.08 to 0.17 h | ask 2 only | the wording |

I report the remedy-rule fork as the thread scored it, touching the main call's remedy with no competing answer surviving, and not as an ask-only fork. The coordinator had it down as ask-only, and the thread's note does not support that.

## The block aggregation fork (Gate C exposure)
Which sentence makes pooling the reading of the block figure? None that I can quote. What the shipped text says:
- The prompt: "what are they getting across this term's timetabled sessions" and "the rate per occupant present settles it". This uses a collective subject and a single rate, and it is the nearest thing to a pooled reading. It does not say how six rooms combine.
- TGD-M4 4.4: "Where a space serves groups of different size the rate is reported over the whole of the period assessed rather than for a single group." This pools sessions inside one space across groups. It does not say how spaces combine into a block.
- TGD-M4 4.2: "The requirement applies to each teaching space separately." This pulls the opposite way, towards a per-room reading.

Gold is 5.027 (printing 5.0). The worst-room figure is 4.72 (F09), printing 4.5. The mean of room rates is 5.07 and also prints 5.0, so only the worst-room reading forks the printed figure.

Honest answer: nothing quotable closes pooled against worst-room, and 4.4's "whole of the period" only leans toward pooling over time. What disfavours the worst room is that it is a minimum, a statistic no filed sentence names, and the prompt asks what "they" are getting. That is inference, not a quoted sentence. The printed rate is graded in its own right (ask 1), so this is a Gate C exposure whatever happens to the call. The design note's fork table (SF9, closure axes 7 and 21) closes the block's membership and the weighting among pooled aggregations, but has no row for a worst-room reading.

Recommended generator action: file the WHAT once at authority, for example one sentence in EST-14 s4 or a new sentence saying that a block's rate is the outdoor air supplied across all its timetabled sessions per occupant present across the same sessions. That files the population and the denominator, not the integration method. The prompt has about 3 characters of room (997 of 1,000), so EST-14 is the place. It needs a rebuild and must not mention any quadrature.

## Population and conventions filed once at authority
- Who "per person" counts: EST-14 s4 files present marks only, learner, tutor and assistant alike; absent and authorised-absent excluded; one mark per person per session; an amended flag adds no second mark. The alternatives are each ruled out by a quoted sentence. Learners only would give ask 4 as 34 / 47 / 35 / 48 / 40 / 55.
- The 8 L/s per person requirement is filed once, at TGD-M4 4.2, naming no method.
- Rounding: filed once at EST-14 s5 (half litre, a figure on the point reported upward, rounded once at reporting), with hours, occupants and shares to the same precisions as the prompt. No conflict remains.
- Counting period: the prompt window plus the academic calendar (48 teaching days). EST-14 s3 files the counting of hours and readings reading by reading.
- None of these three reads as fixing HOW the rate is found.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000 rows or more | bms_co2_5min_autumn2026.csv, 293,559 rows | yes |
| Distractors | 2 or more named in metadata.json, no file name labels one | campus_energy_halfhourly_2026.csv and bms_temperature_rh_hourly_autumn2026.csv; neither name labels it | yes |
| Distractors weigh but are unused | relevant, unused; a wrong-basis one reproduces and is ruled out by a shipped fact | the 8.5 L/s design supply (commissioning record), ruled out by its own s3 and TGD 4.3 | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx and png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 56 + 14 + 6 + 4 fields; the prompt's last sentence states the rounding | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | prompt shape clear; criteria well over 25 by the cells and fields graded (I did not see the generated rubric) | yes |
| Reads as real | no LLM tells, goldens read as work products | the thread found no authoring disclosure or leak; I did not independently review the golden prose | yes |
| Layer 1 mess | present and never the stump | DST on 25 Oct (a Sunday with 300 stamps), quoted thousands strings, UTC Macehead gap fill, duplicate TUL-F04 register row, 8 network-fault room-days | yes |
| Write-up consistency | every figure recomputes | 1.59 against the printed 5.0 | no, see Findings |

## Gate G reconciliation
The thread's mechanism is method_or_model_selection (a transient mass balance against a settled read), family analytical_non_defect, with no surface-read dependency and no sole data defect. The design note's stump is the same step: treating a still-rising concentration as settled, in spaces whose response time is 3.5 to 6.5 times the session. Its Layer 2 is labelled estimation_fit, which is the same thing under another name. I read the note and metadata.json only after the thread returned. The declared wrong-basis distractor (commissioning 8.5 L/s) is not what carries the task: the thread says it "invites the same comfort" but the call turns on the settled read, which the data refute (concentration still rising at session end, 0.70 of the implied steady value, storage 47 percent of the source). No mismatch. Gate G: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no.

## Gate H
domain pass, layers pass, decisive_step analytical. The deciding quantity is the outdoor-air supply per person from a CO2 transient balance, which the field estimates; the swap test makes the quantity stop existing (no volume, generation rate or response time). Layer 1 is the offsets, DST, quoted numbers, outdoor gap and duplicate key; Layer 2 is the stored-term balance. This matches the design note's `## Three rules`.

## Stump power (Gate F)
Plausibly strong. The easy route (settled or end-of-session reading with 0.0072 times occupants over the excess) files 9.3 to 10.9 L/s per person and a "compliant" finding, and the commissioning record's 8.5 invites the same comfort. The transient balance with the stored term gives 5.0. The thread classed the decisive step analytical. It reached the golden by applying the field's tracer-gas method, with no judgment filed in the text, and the stored-term family is a textbook route a strong solver takes (`stumping` 1.3). I record that as a landable call, and the main thread should weigh it against the design note's ladder. Option B being unable to reach 8 under any reading makes the call itself easy once the rate is below 8. Ask 2 and 3 add careful-counting traps (ANG-016 gap, 300-stamp day, 288-per-day basis).

## Findings, ranked
1. **Gate A, write-up (certain).** `submission.md` says the 8 required is 1.59 times the rate, but 8 divided by the shipped 5.0 is 1.60. The 1.59 comes from the unrounded 5.027. The same figure is in the Final Recommendation. A reviewer re-dividing the printed numbers will reject it. Restate it as 1.6, or print the rate as 5.03 next to 5.0.
2. **Gate C, block aggregation (open).** Nothing quotable closes pooled against worst-room; the worst room prints 4.5 against the gold 5.0. It touches ask 1's printed rate, not the call. Close it with one filed WHAT sentence (see above).
3. ANG-016 uncertain readings (asks 2 and 3, one cell each). The literal EST-14 supports the gold. One filed sentence that a flagged reading still counts as logged would close it.
4. Remedy rule unfiled. The call is inference-dependent but no competing answer survives.
5. Ask 5 magnitude and "over" 1,500 forks: ask-only, closed by the asked fields and the wording.
6. Hygiene: "Kilmoneen Further Education Campus campus" doubled word in EST-14 s1. Terminal counts differ between the zone sheet and the room data sheets (the declared distractor doing its job; no effect).

Any pin added to the input files requires a rerun of the judge's reading, and none may file a quadrature.

## Next action for the author
Fix the Final Recommendation's ratio to 1.6 (or print 5.03 beside 5.0), then file one WHAT sentence in EST-14 saying a block's rate is the outdoor air supplied across all its timetabled sessions per occupant present across the same sessions, and rebuild.
