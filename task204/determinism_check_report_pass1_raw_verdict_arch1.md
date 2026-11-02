# Determinism verdict, task204 (Tulrohan ventilation)

**Verdict:** NOT_DETERMINISTIC (the A-or-B call is forced; the graded rate, the headline figure and supplementary answer 1, is not).

**Disposition:** SEND_BACK. Pin the session quadrature and the occupant population in the filed text (EST-14 conventions or the prompt) so every literal reading gives 5.0, or re-cut the data so rectangle and trapezoid land in one half-litre bin. Solvers see changed text, so a rerun is needed.

**Why:** Nothing filed says how the session carbon dioxide balance is integrated. The stored term is taken between the first and last reading, which implies a 55-minute span. EST-14 s3 says "each logged reading represents the five minutes beginning at its timestamp", which read literally is a rectangle rule over 12 readings, or 11 if the last is excluded. Using a trapezoid, as the golden does, the block rate is 5.05 to 5.08 and files as 5.0. Using the rectangle the filed convention gives, it is 5.37 to 5.60 and files as 5.5. The data do not separate the two, and no filed back-test or selection criterion exists. This hits the headline "5.0" and supplementary answer 1 (Gates C and E, taxonomy `competing_defensible_answer`; the fork is a method choice the text never pins). The A-versus-B remedy is not affected.

## Evidence (recomputed from target/)

Method used: per session, V*dC = G*n*T minus Q*integral(C - Cout)dt. G = 0.0072 L/s per person, from the TGD-M4 table 2.3 extract. Volumes are from the as-built PDF. Cout is the campus hourly analyser matched on UTC hour, with 337 missing hours (11 to 25 Oct) filled from Macehead. The result is pooled as sum(Q*T) over sum(n*T).

| Reading | Block rate (L/s per person) | Files as |
|---|---|---|
| Trapezoid, all persons present (learners present + tutor + assistant) | 5.07 | 5.0 (golden) |
| Trapezoid, learners only / learners + tutor | 4.91 / 5.05 | 5.0 |
| Rectangle, 11 readings, all persons | 5.63 | 5.5 |
| Rectangle, 12 readings, all persons | 5.52 to 5.57 | 5.5 |
| Rectangle, learners only | 5.37 to 5.42 | 5.5 |
| Mean of per-session Q/n instead of pooled (trapezoid, all persons) | 5.52 | 5.5 |

- The outdoor fill (raw Macehead vs bias-adjusted, 3.4 ppm mean offset, vs interpolation) moves the rate by 0.01 or less. It is not a fork.
- The golden is the trapezoid reading. Critical component 3 (189 min for TUL-G07) reproduces only under the trapezoid. The rectangle gives 178.
- Pooled against per-session-mean: TGD-M4 4.4 ("over the whole of the period assessed") closes pooled. Quadrature is the only fork that survives for the rate.
- Gap handling: 173 sessions have a missing reading in the window and 48 sessions (8 network-fault days) have no readings at all. Trapezoid-on-available-points vs skipping those sessions changes the rate by less than 0.01. Including the 48 sessions' occupant-seconds in the denominator gives about 4.93, which still files as 5.0.
- Outcome on the main call: moving the four largest groups out (CON5A, HSC5A, BUS5A, GEN5A, a unique top four by enrolment) leaves a block rate of 5.75 against 8. Option B cannot comply under any reading and option A is the only remedy that can. The remedy is forced. The 1.58 ratio in the recommendation is 8 over the unrounded 5.07; under the rectangle it is about 1.45.
- The design supply (8.5 per person) is ruled out as evidence by TGD-M4 4.3 and by the commissioning record s3. Both are shipped.

Other graded items:
- **Ask 2 (occupied and over-1,500 hours):** all 56 month cells reproduce, using the plant-status OCCUPIED intervals (07:55-12:00 and 12:55-15:00, which cover 48 days only) and a reading counted in its own local month. "Over" and "passes" are read as strictly greater. Reading at or above 1,500 ppm changes 5 cells (TUL-F04 Oct and Nov, TUL-G12 Oct and Nov, TUL-G18 Dec), because readings of exactly 1,500 exist. The wording closes this.
- **Ask 3 (share received):** reproduces, counting teaching-day readings over 48 x 288 and counting the 288 `uncertain` ANG-016 readings as received. Excluding them gives 91.6 for ANG-016. "Received" literally includes them, and no other room is affected.
- **Ask 4 (mean occupants):** the golden counts learners present + tutor + assistant. Learners only gives 34/47/35/48/40/55, and learners + tutor gives 35/48/36/49/41/56. Only the golden's population gives TUL-G18 = 37. No sentence says staff count. TGD-M4 "per person present" and the register's person_ref/role column point that way but do not state it. This fork is an inference only and affects ask 4 and the 70,404.6 occupant-hours. The rate stays 5.0 under the trapezoid whichever population is used.
- **Ask 5 (four largest rises):** unique and robust to window convention. Inclusive ends give 457, 434, 426, 416, with the fifth at 412. Exclusive ends give 451, 403, 392, 388, with the fifth at 377. The order is the same.
- **Critical component 1 (1,728 sessions):** reproduces. **Component 2 (70,404.6 occupant-hours):** reproduces only as 76,805 persons x 55/60 h, with staff counted and the 48 no-data sessions included.
- **Rounding conflict:** EST-14 s4 says hours and occupants to one decimal, and the prompt says two decimals and whole occupants. The prompt is the later ask and the golden follows it. Note it, but it is not decisive.

Answers to the brief's specific questions:
- (a) No filed sentence fixes HOW the per-person supply is computed. TGD-M4 table 2.3 supplies only G, which implies a balance. The quadrature and the window are unfiled. EST-14 s3 gives a reading convention that points to a rectangle, which contradicts the golden.
- (b) Population: TGD-M4 4.2 and 4.4 ("per person", "per person present") plus the attendance `mark` column rule out authorised or absent learners. Nothing rules staff in or out.
- (c) Requirement (8) is filed once at TGD-M4 4.2. Rate rounding (nearest 0.5, ties upward, round once) is filed in EST-14 s4 and repeated in the prompt. The counting period (28 Sep to 11 Dec timetabled sessions) is filed in the prompt and calendar. The per-person denominator and the integration are not filed.
- (d) The fork on quadrature touches the main figure of the main recommendation (5.0 vs 5.5) but not the call. The staff-count fork touches only ask 4 and the occupant-hours critical component. The strict-greater fork touches only ask 2 and is closed by the wording.

## Files/Hygiene
PASS, with notes.
- 19 files in 4 formats: csv, xlsx, pdf and txt. Distractors present: energy half-hourly, temperature/RH, enrolment workbook, Macehead (used only for the fill).
- Layer 1 mess is credible: local time with a repeated hour on 25 Oct (300 stamps on that Sunday), a UTC Macehead file, a duplicated `TUL-F04` row in the room register (a welfare room on AHU-03), quoted ppm strings with thousands separators, and a 24:00 interval end.
- Unused inconsistency: the terminal counts in the zone-assignment sheet disagree with the as-built supply terminals. This does not affect the answers.
- No authoring disclosures found, and no temporal incoherence (thread dated 11 to 12 Dec 2026, term closed).
- No exclusion-level finding.

## Stump power
Moderate. The real trap is the stored term: the shortest room response time is 189 min against 55-min periods. A steady-state shortcut, or reading the design 8.5 as achieved, overstates the supply, and a naive "peak minus outdoor" approach can pass the requirement. TGD-M4 table 2.3 hands over G, which helps the careful solver. The call itself is easy to reach (A) because option B cannot reach 8.

## Stumping type
`mechanism: method_or_model_selection` (a physical mass balance on honest data), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The commissioning design supply is an unproved record rather than a wrong number. Banned_stumping_type does not apply.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The domain is ventilation engineering: supply rate from a tracer-gas balance, normalised per person present. The swap test fails to make it generic. Layer 1 is the DST/UTC stamps, the register key, the outdoor-analyser gap and the network-fault days. Layer 2 is the stored-term mass balance. The easy route is the steady-state or design-supply read, which files a rate at or above 8 and the wrong remedy.

## Fix
`prompt` or `input_files`. Pin the integration estimand. For example, EST-14 s3 can state that a session's concentration is integrated as piecewise-linear between consecutive readings over first to last reading, or that readings are rectangles over the full period. Pin whether staff count as occupants in the attendance population. Alternatively tighten the data so rectangle and trapezoid give the same half-litre bin. The A-over-B call needs no change.
