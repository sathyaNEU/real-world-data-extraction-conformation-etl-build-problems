# task180 design note: Ellesmere Lines, the three internal inspections of 2027/28 (architecture 2)

Seed AD03 (revenue-protection crew). Architecture 1 (revenue protection, the screen grain) was spent at in-house
round 1 and is recorded under Tried and rejected. This is the re-root: same objective, same number, a new draw. The
seed's idea that carries over is the one AD03 shares with the whole lane: the loudest signal is not all cause.

Every figure below is the shipped value. `generator/checks.py` asserts them (146 assertions) and
`generator/verify.py` recomputes the slate and every graded figure from the shipped bytes alone.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (PASS)
Shape: 01 ranked list under a cap (three inspection outages, 44 transformers)
Gate G mechanism: decomposition_attribution (each transformer's main-tank acetylene attributed to its source)
Gap: population (decisive), rule        Pattern: none (own); generators G8 (the worst-looking units are the ones the remedy cannot reach), G3
Domain: energy-systems-utilities / asset-condition-maintenance   Objective: anomaly-detection (fault diagnosis from DGA)
Pairing repeated from a recent build? task180 architecture 1 only (its own lineage, a different puzzle)
Stakeholder role: network asset manager (portfolio_manager)   Context artifact: capacity_report (mobile substation bookings)
Calibration form: none   Decision type: ranked_slate_under_cap   Answer unit: set_of_items
Stump strategy: decomposition_attribution (relabelled at hardening loop 1 from stated_rule_hard_construction)   Decisive rule filed? yes (ES-DGA-02 5.1 remedy and 5.2 priority)
Official decoy filed? no   Validated decoy? no
Forum: board_of_directors (28 October 2026)   Forcing event: audit_or_inspection   Org family: utility_or_infrastructure
People (guard.py names, en_NZ, seed 1802): Donna Carson (network asset manager, the requester), Barry Forbes (zone
  substation engineer, owner of ES-DGA-02 and the oil results), Wendy Godfrey (board chair), Connor McGill (oil sampling
  technician). Drawn with seed 1803 for the pack: Emma Elliott (general manager network, approves ES-DGA-02), Dennis
  Trask and Ethan Mason (field services, tap-changer work), Aroha O'Brien (maintenance planning, MSU-2 bookings), Aimee
  Craig (contract thermographer), Allan Simpson (runs the extract, operator asimpson).
```

**Data-native sentence.** Older zone-substation transformers switch load on an in-oil arcing tap changer that sits in a
compartment sharing a barrier with the main tank, so when that barrier weeps, the acetylene every tap change makes in
the compartment turns up in the main-tank oil the fleet is coded on, rising with the tap-change count rather than with
any fault in the winding.

**Layer 1 (realistic mess and the system that produces it).** A laboratory results file per sampling round (sampling
date and time and a separate analysis date, gases in ppm with below-detection values written as `<n`, oxygen and
nitrogen, moisture, the label temperature the technician wrote down or left blank, and corrected reports re-issued under
the same sample ID); an asset register with rewind years
and tap-changer types whose last-service field stopped being written back in March 2025; SCADA daily tap-change counters
that roll over at 99,999 and restart at zero when a counter is replaced at a tap-changer service; hourly SCADA top-oil
temperatures exported from the historian in UTC with no zone marker; a maintenance log in free text.

**Layer 2 (the analytical shortcut).** Coding each transformer on its main-tank gases and ranking the code-3 units by
severity. The standard's arithmetic is right and every gas really is in the main-tank oil; an expert first asks where
each fault gas was made, because the inspection outages go to faults in the main tank (5.1, 5.2), and acetylene carried
in from a tap-changer compartment is made by normal switching, not by a fault an internal inspection can find. The
second shortcut is how to tell: following the tap counter is not enough, because an arc at the tap selector, which
works in the main-tank oil, also makes its gas at every operation. The gas the acetylene arrives with settles it: oil
from a diverter compartment brings acetylene with almost no hydrogen, an arc in the main-tank oil makes more hydrogen
than acetylene (IEC 60599, cited by the standard, reads a C2H2/H2 above 2 to 3 in the main tank as tap-changer oil).

**Similarity claim.** No prior build attributes a measured anomaly to an attached compartment's normal operation before
ranking. task181 (explaining away a dominant source among pooled victims) is a different structure: there the sources
compete for the same victims; here each unit's own signal has a second, benign origin.

**Differentiation (clone pre-flight, 2026-10-11, CLEAN).** task119: a unit blamed on its outcome count and
excused by capacity data through a bed-allocation record; here units the standard ranks worst are cleared because
their signal is a benign leak from an attached compartment. task101: a baseline cleaned of the fund's own top-ups;
here no baseline is restated, each unit's gas is attributed to its source. task121: identity of signed-out users;
here identities are fixed and the question is where a measured gas was made.

## GATE G

- **Litmus.** Nothing reported is overturned: every laboratory value, counter reading and register field is correct;
  the standard's codes and severities are computed correctly. The difficulty is which units' gases point to a fault
  inside the main tank.
- **Primary mechanism:** decomposition_attribution.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete Barry's notes and the mobile substation schedule: coding on main-tank gases still names the
  two leaking units; attribution still removes them.
- **Clean-data and instrument test.** No file is incomplete or stale for the decision: every main-tank sample and every
  counter reading ships, and the main call's rows carry no device (asserted, below). A
  perfect main-tank gas analyser still reads the leaked acetylene, because it is really in the oil; what the decision
  needs is its origin, which the gas it arrives with settles; the counters and the tap-changer types alone do not
  (Rolleston T2's acetylene follows its counter as closely as the leaks' do).
- **Lens swap.** Not one population under two lenses: the answer's ranking runs on main-tank gases generated in the main
  tank, a different set of gas volumes from the naive ranking's, built per unit from three files.

## STUMP SENTENCE

A competent solver codes every transformer under ES-DGA-02 from its main-tank samples (limits by preservation type and
age, twelve-month increases, code 3 ranked by severity) and names Dunsandel T1 (9.64), Leeston T2 (8.07) and
Southbridge T2 (8.07), two of which carry acetylene leaked from in-oil tap-changer compartments; the step that lands it
there is reading main-tank acetylene as a main-tank fault, when at Dunsandel T1 and Leeston T2 its increments track the
tap-change counts (r 0.998 and 0.995) and its twelve-month ratio to hydrogen is 9.8 and 8.2. A solver who does
attribute, but by the counter alone, drops Rolleston T2 as well (its acetylene tracks its counter at r 0.999, arc gas
from the tap selector in the main-tank oil, C2H2/H2 0.64) and names Southbridge T2, Coalgate T1 and Springston T2. The
slate takes the vacuum-tap-changer unit with the same acetylene (Southbridge T2), the in-oil unit whose acetylene is
made in its main tank (Rolleston T2, 4.98) and the worst thermal fault (Coalgate T1, 4.73).

## ENTITY AND UNIT OF VALUE

One transformer, one inspection outage. The standard's severity score is a ratio of a gas's twelve-month increase to its
rate limit; the slate is three transformers in priority order.

## LADDER (shipped)

Units: L2 = DSL-T1 Dunsandel T1 and L1 = LST-T2 Leeston T2 (in-oil arcing tap changers, barriers weeping from 1 July 2024
and 17 March 2025), V = SBG-T2 Southbridge T2 (vacuum tap changer, internal arc), A3 = RLS-T2 Rolleston T2 (in-oil tap
changer, arcing at the tap selector in the main tank from December 2024, gas made at every operation, not leaking), T1 = CGT-T1 Coalgate T1, T2 = SPN-T2 Springston T2, T3 = DFD-T1 Darfield T1
(thermal faults in oil).

| Rung | Construction | Slate | Why a careful analyst stops | Killed by |
|---|---|---|---|---|
| 0 | Highest latest acetylene (arcing read off the Duval triangle) | DSL-T1 (22.5 ppm), LST-T2 and SBG-T2 (12.9 each) | arcing is the most severe fault class | ES-DGA-02 4.4 codes on levels and twelve-month increases, not the latest level |
| 1 | ES-DGA-02 code 3 on main-tank gases, ranked by severity | DSL-T1 9.64, LST-T2 and SBG-T2 8.07 each, then RLS-T2 4.98, CGT-T1 4.73 | the filed standard applied exactly | at DSL-T1 and LST-T2 the main-tank acetylene increments track tap-change counts (r 0.998 and 0.995 from the first detectable result; 0.978 and 0.989 from the last below-detection one), twelve-month C2H2/H2 is 9.8 and 8.2, the tap changers are in-oil arcing types |
| 2 | Drop the unit with the clearest leak only | without DSL-T1: LST-T2, SBG-T2, RLS-T2; without LST-T2: DSL-T1, SBG-T2, RLS-T2 | one contaminated unit found | the other leaking unit carries the same signature |
| 3 | Drop acetylene at every in-oil tap-changer unit | SBG-T2, CGT-T1, SPN-T2 | a rule of thumb about tap changers | RLS-T2's acetylene arrives with more hydrogen than acetylene (C2H2/H2 0.64): made in the main tank |
| 3b | Drop acetylene wherever it tracks the unit's tap operations (round 2's step) | SBG-T2, CGT-T1, SPN-T2 | the two leaks track their counters, so tracking reads as the test | RLS-T2's acetylene tracks its counter too (r 0.999 raw, 0.992 per day) but arrives with 1.6 times as much hydrogen (C2H2/H2 0.64 against 9.8 and 8.2 at the leaks): arc gas made in the main-tank oil at each tap change, not diverter oil |
| 4 (answer) | Attribute each unit's acetylene by the gas it arrives with; the outages go to the code 3 units whose fault is in the main tank | **SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73** | | |

With their acetylene attributed, DSL-T1 and LST-T2 stay code 3 under section 4, which codes the main-tank results as
reported (the goldens carry the literal code and severity, 3 at 9.64 and 3 at 8.07), but neither has a fault in the
main tank, so 5.2 gives them no outage. Recoded on what the main tank made they would be code 2 on paper gases (0.81
and 0.38); no filed sentence asks for that recoding, and the slate is the same either way. Code 3 with a main-tank
fault: SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45.

**Twin pair.** LST-T2 and SBG-T2 are sampled on the same day every round (the route pairs Leeston with Southbridge) and
carry the same main-tank acetylene at the samples the standard reads: 4.7 ppm on 8 September 2025 and 12.9 ppm on 14
September 2026, 371 days apart, an increase of 8.2 ppm scaled to 8.07 (also level at 2.8 ppm in June 2025). Both are
free-breathing on the latest and on the median O2/N2 and both are 10 to 30 years old, so code and severity are
identical (code 3, 8.0674). LST-T2's tap changer is in-oil and its acetylene tracks the counter; SBG-T2's is vacuum,
its increments are uncorrelated with its counter (r -0.073 raw, 0.016 per day) and its hydrogen rose 16 ppm (C2H2/H2
0.51). Any rule on main-tank gases keeps both or drops both.

Margins: SBG-T2 over RLS-T2 1.62; RLS-T2 over CGT-T1 1.053; the slate cut CGT-T1 over SPN-T2 1.068 (6.8 per cent);
on the naive slate the cut is SBG-T2 8.07 over RLS-T2 4.98. Every wrong slate differs from the answer by at least one
named unit, asserted.

## GRID (asserted in checks.py)

Rows: six attribution rules that read the gas the acetylene arrives with (all three signatures; type and ratio;
tracking and ratio; acetylene dropped for C2H2/H2 above 2, 3 and 5) and eight that do not (type and tracking; any two
of three; tracking r of 0.8, 0.9 and 0.95 on increments per sample interval; r of 0.9 per day; cumulative growth
fitting the operations better than time, alone and with the tap-changer type), each on two tracking windows (from the
first detectable result, from the last below-detection result). Columns: below-detection values at zero, half the
limit or the limit; base sample at 330, 365 and 400 days; preservation class from the latest or the median O2/N2 (18
columns). Shipped: all 216 gas-signature cells return SBG-T2, RLS-T2, CGT-T1 in that order, and all 288 tracking-only
cells return rung 3b (SBG-T2, CGT-T1, SPN-T2); the main-tank-only rule returns DSL-T1, LST-T2, SBG-T2 in all 18 columns and the latest-acetylene rule keeps
DSL-T1 and LST-T2 in all three below-detection readings. Attribution is looked for only where acetylene rises faster than
its rate limit (DSL-T1, LST-T2, SBG-T2, RLS-T2).

## CLOSURE (the 22 axes)

1 Population: the 44 zone-substation transformers in service (ES-DGA-02 1.1). 2 Unit: transformer. 3 Window: twelve
months to the latest sample (4.3). 4 As-of: the September 2026 round, 14 to 30 September 2026, the latest sample of every
unit. 5 Version basis: the report of record is the latest issue for a sample ID (3.4); the five re-issues change
moisture or label temperature only, and the first issue leaves every code and severity unchanged (asserted). 6 Divisor:
rate limits per gas and class (table A3). 7 Weighting: none. 8 Window length: the base sample is the September 2025 round
sample for every unit (366 to 378 days back); 365 converges (every gap is 366 or more) and 400 takes June 2025 with the
same slate (grid). 9 Boundary: no severity within 5 per cent of the slate cut (6.8 per cent). 10 Rounding: severity to
two decimals, every severity at least 0.002 from a two-decimal edge (worst 0.0021, BNM-T1) and at least 0.0003 off the
round value; relative saturation at least 0.02 from a one-decimal edge and at least 0.5 from 30 per cent (worst 1.51,
SPF-T1). 11 Tie-break: the LST-T2/SBG-T2 tie sits inside the naive slate, never at its cut. 12 Maturity: the September
round is complete for every unit. 13 Order of operations: attribute, then code, then rank. 14 Row order: irrelevant.
15 Duplicates: re-issued laboratory reports for the same sample ID (H1, ask layer only). 16 Identity: transformer IDs
stable; replaced counters keep the transformer ID. 17 Netting: none. 18 Units: ppm (uL/L). 19 Code semantics:
preservation class by O2/N2 (4.1), every unit at least 0.09 from 0.2 on the latest and on the median ratio. 20 Integerisation: none. 21 Scope: 5.1 and 5.2, faults
in the main tank. 22 Forward window: none in the call. The analysis date read as the sampling date leaves the
slate unchanged (asserted).

## ASK SHEET (devices off the main call's rows)

Main call row population (declared, asserted device-free): main-tank results for every transformer;
the daily tap-change counts and the asset register rows of every code-3 transformer. Zero counts at the seven code-3
units: 0 counter drops 2021 to 2026, 0 stale register dates, 0 counter replacements, 0 laboratory re-issues.

| Ask | Figures | Primary devices (silent) | Shared hazard |
|---|---|---|---|
| A. Tap-changer service: every in-oil tap changer's operations since its last service and whether it is past the interval (ES-DGA-02 annex B) | 27 x 2 = 54; seven past (DSL-T1 87,322, DYL-T2 87,029, GLT-T1 75,013, TPR-T2 64,224, LST-T1 61,972; GLT-T2 and SHF-T1 on the seven years) | D7: a counter drop is a rollover at 99,999 (LST-T1, DYL-T2, TPR-T2, CGT-T2, GLT-T1, WDS-T1) unless the log has the counter replaced at a service that day (SBG-T1, WDN-T1, GDL-T1, LDB-T2, LIN-T1, KRW-T1, HOR-T1); D2: the register's last-service field predates the services since March 2025 (DSL-T2, HOR-T1, KRW-T1, LIN-T1, LIN-T2, SPF-T2, LDB-T2, WDS-T1, and WDN-T2 among the vacuum units), and the log is the record (6.1) | none (H1 moves ask B only) |
| B. Wet transformers: relative saturation at each unit's latest sample, those above 30 per cent | 44 in the CSV, six in the board paper (SHF-T1 36.1, GDL-T1 34.9, WDN-T1 34.1, DYL-T1 33.1, TPR-T2 31.7, SPF-T1 31.5) | D8: the historian exports UTC (UTC+12 to 27 September 2026, UTC+13 after), so the hourly top-oil temperature joined on the local clock reads the wrong half of the day for the 15 latest samples with a blank label temperature (12 before and 3 after the change to daylight time); D8: the results file's `date` is the analysis date, `sampled` is the sampling time | H1 laboratory re-issues (five; three on latest samples: SPF-T1 moisture, KRW-T1 and GDL-T2 label temperature) |

Stops (asserted, each moving its figures): ask A, register last-service date: 8 figures and 8 flags move (LIN-T1
84,026 against 16,064); every drop a rollover: 7 figures and 3 flags (SBG-T1 89,197 against 32,019); every drop a
reset: 6 figures, no flag (LST-T1 61,948 against 61,972); both together: 11 figures, 11 flags. Counting from the morning
after the service converges (no load operations on a service day). Ask B, the hourly temperature read on the export's
own clock: 15 figures move and the wet list falls to four (DYL-T1 22.2, TPR-T2 23.4); a fixed UTC+12: 3 move; a fixed
UTC+13: 12 move; the analysis date as the sampling date: 15 move and the list grows to seven (CGT-T2 34.1, LIN-T2 30.3);
the first issue of a re-issued report: 3 move and SPF-T1 (28.6) leaves the list while KRW-T1 (43.0) joins it.

Use test: both are the next two tables of a board paper that asks for three inspection outages (tap-changer backlog,
wet units for oil processing). Decoupling: clearing the attribution moves the slate and no figure in A or B (asserted);
the ask code reads no code and no slate (asserted).

## PINS

Filed: ES-DGA-02 Fleet DGA condition standard rev 3 (governing): scope (1.1, 1.2),
sampling and the report of record (3.4, 3.5), coding (4.1 preservation class and age band, 4.2 levels, 4.3 twelve-month
increase with the base sample the most recent main-tank sample taken 330 days or more before the latest, 4.4 codes and
severity over the seven fault gases), inspection priority (5.1 an internal inspection is the remedy for a fault in the
main tank; 5.2 the outages go to the code 3 transformers with such a fault, in descending order of severity), the
tap-changer service record (6.1 to 6.3), water in oil (7.1), annex A limit tables, annex B service intervals, annex C
relative saturation. Oil results notes (field semantics only). No sentence anywhere mentions compartment leakage,
contamination, weeping or barriers (asserted on the standard, the log and the notes).

## PACK GATES (shipped)

11 files, 6 formats (csv, xlsx, parquet, pdf, md, txt): main-tank results 1,077 rows (1,072 samples and 5 re-issues),
daily counters 93,060, hourly top-oil parquet 2,232,384 rows, asset register 44, maintenance log 275, relay events
1,161, mobile substation bookings 12. Two distractors named in metadata.json: the protection relay event log (feeder and incomer
relay operations) and the March 2026 thermal imaging survey of the 11 kV switchboards; the golden never reads either
(asserted). Two consecutive builds byte-identical (sha256 on every file of the pack, the goldens and metadata.json).

## THREE RULES (client, 2026-10-10)

- **Rule 1, the domain is used.** What decides the slate is a dissolved-gas diagnosis of where each transformer's
  main-tank acetylene was generated, diverter-compartment oil carried through a weeping barrier (C2H2/H2 of 8 to 10)
  against an arc in the main-tank oil (more hydrogen than acetylene): the field's own fault-gas interpretation (IEC
  60599), close to the asset-condition task type. Swap test: with schools or clinics in place of transformers there is
  no gas, tap changer or ratio to read, so the task does not survive the swap. The decision framing ("which three
  transformers") is the client's allowed kind; the severity ranking under section 4 is a lower rung, never the decider.
- **Rule 2, two layers.** Layer 1: laboratory re-issues under one sample ID, below-detection values written as `<n`,
  preservation class from O2/N2 rather than the register, a UTC historian export, five-digit counters that roll over or
  restart at a replacement, last-service dates the register stopped writing back, a free-text maintenance log. Layer 2:
  attributing each unit's main-tank acetylene to its source by the gas it arrives with, when two sources (a leaking
  diverter barrier and an arc at the tap selector) both follow the tap counter.
- **Rule 3, the decisive step is analytical.** Class `analytical`. Analyst test: a strong analyst who keeps the latest
  issue of every report, codes all 44 transformers correctly under ES-DGA-02 and reads 5.1 and 5.2 as giving the
  outages only to faults in the main tank still takes the easy attribution, dropping every transformer whose acetylene
  rises in step with its tap operations, and files Southbridge T2, Coalgate T1 and Springston T2 (rung 3b; all 288
  tracking-only cells). Rule application (the section 4 coding, the annex B interval) and data semantics (the `<n`
  notation, the UTC export, the analysis date) sit on lower rungs and in the asks; none of them moves the slate once the
  attribution is right (asserted), and none of them can produce the answer without it.

## PRE-SHIP CHECK (client, eight points)

1. Domain: transformer condition assessment's own analysis (DGA fault diagnosis and gas-source attribution); the swap
   test breaks it (no gas, tap changer or ratio with another field's nouns).
2. Real work, nothing planted: laboratory formats, detection limits, preservation class from O2/N2, rollovers and
   counter replacements, a free-text maintenance log, UTC historian exports, re-issued reports.
3. The flip is a methodological choice: attributing each unit's acetylene to its source by the gas it arrives with. Not
   a planted catch, not a field or code read correctly, not a stated rule applied.
4. Analyst test holds: the easy attribution (drop acetylene that tracks the tap operations) gives Southbridge T2,
   Coalgate T1, Springston T2; the design note names it (rung 3b) and checks.py asserts it in every grid cell.
5. ES-DGA-02 defines the population, the coding, the window and the priority (5.1, 5.2: outages to code 3 transformers
   with a fault in the main tank); every gas-signature attribution rule returns the answer in all 216 cells.
6. No decoy memo, staff draft or briefing; Barry's notes are a field dictionary and true.
7. The method is not hidden and recovered from certified figures: the attribution rests on the physics of where gas is
   made, and nothing in the pack is fitted to.
8. The lesson (a diagnostic signal that follows a component's operation is not proof that the component made it; read
   the gas it arrives with) is not one an earlier task teaches: task28 splits a flagged excess by source before ranking,
   but there the sources do not share a signature.

## STOPPING RULE

Two rounds in which both solvers attribute the acetylene unprompted file this architecture as at-ceiling; a miss landing
anywhere other than rungs 0 to 3b is read for a fork before any hardening.

## LEAK CHECK (leak.py, as-of 2026-10-16)

Verdict REVIEW, no LEAK; three REVIEW lines, each answered. Sweeps 1, 2, 3, 5, 6, 7 and 11 clean; sweep 10 found no writer signature.
`guard.py surface task180`: 124 builds screened, no pair promoted (nearest task89 at surface 0.104); personas found in the pack all on the card.

- Sweep 4, `ES-DGA-02_fleet_dga_condition_standard.pdf` carries six swept terms (register, manager, network, written,
  main-tank, remedy): ordinary words of a utility standard (the asset register, the General Manager Network who approves
  it, the temperature written on the label, the main-tank sample the fleet is coded on, an internal inspection as the
  remedy for a fault in the main tank, 5.1). It names gases and the main tank as any DGA standard does and says nothing
  about compartment oil reaching the main tank, about tap selectors or about telling one source from another by its
  gases (asserted).
- Sweep 8, `oil_temp_c` in the main-tank results: the label temperature column the brief names; "temp" is temperature,
  not a temporary field.
- Sweep 9, `mobile_substation_bookings_2027-28.xlsx` carries 18 dates in 2027 and 2028: it is the forward booking sheet
  for the windows the slate fills, forward by design.

Isolated reader, pass 2 (after the scope sentence, the compartment clause and the compartment file came out; read on
the pack before the 5.2 rewording): decisive step, the selection rule in 5.2, which the prompt itself points to; no
ranking file, no analyst-only file, no answer-like figure or name; all three REVIEW lines read harmless. Its plan of
attack coded every transformer on the main-tank results and put "the top three code 3 transformers" into the windows,
with no step that asks where a gas was made: the attribution is no longer a work order. Pass 3 reads the pack with 5.2
as reworded.

Isolated reader, pass 3 (5.2 as reworded, run beside round 2): nothing quoted for question 1 ("The closest is ES-DGA-02
s.5.2 ... That is the rule for who qualifies, not the move"), no ranking file, no analyst-only file, no answer-like
figure; all three REVIEW lines harmless. Its plan kept "only code 3 units with a main-tank fault (s.5.1-5.2). That means
dropping in-oil tap-changer units whose acetylene or hydrogen rise tracks tap operations": the qualifier turns the
attribution into a work order, which is what round 2 executed. 5.2 stays (without it the literal reading is rung 1) and
the hardening (loop 1) makes the tracking step return rung 3b. Pass 4 reads the hardened pack.

Isolated reader, pass 4 (hardened pack): nothing quoted for question 1 (5.2 "gives the condition for qualifying, not
how to test it. No file says how to tell a main-tank fault from tap-changer diverter oil leaking into the tank"), no
ranking file, no analyst-only file, no answer-like figure; the three REVIEW lines harmless (sweep 4 now carries six terms,
main-tank added, all ordinary standard wording). Its plan: "Acetylene that tracks tap operations is diverter leakage, so
those transformers are excluded", having seen "the acetylene in DSL-T1, LST-T2 and RLS-T2 rising in step with the SCADA
tap operations": rung 3b, with no step that reads the gas the acetylene arrives with.

## Tried and rejected

- **Round 2 landed (architecture 2, loop 0, 2026-10-11); hardened as loop 1.** One solver, proxy 74.6, the slate exact
  and every ask figure right. Its deciding step: "Main-tank test (5.2): joined monthly samples with tap ops from
  scada_tap_counters_daily (rollovers +100000; counters replaced -> reset). DSL-T1 and LST-T2 acetylene rises at a
  constant ~0.6 ppm per 1,000 ops in every interval (in-oil tap-changer leak) -> excluded; SBG-T2 (vacuum tap changer)
  and RLS-T2 acetylene rise in steps unrelated to ops." The confirming reader (pass 3, run beside the round) planned the
  same step off the 5.2 rewording: "Keep only code 3 units with a main-tank fault (s.5.1-5.2). That means dropping in-oil
  tap-changer units whose acetylene or hydrogen rise tracks tap operations." 5.2 stays as worded, because without it the
  literal reading is rung 1; the attribution is a work order and the hardening deepens it instead. Brief: build the next
  rung so that exactly this step completes and still returns the wrong slate. Rolleston T2's arc is now at the tap
  selector, which works in the main-tank oil: a little gas at every operation, so its acetylene follows its counter as
  closely as the leaks' (r 0.999 raw, 0.992 per day) and the tracking step drops it (rung 3b: Southbridge T2, Coalgate T1,
  Springston T2). What it cannot copy is the gas: an arc in the main-tank oil makes 1.6 times as much hydrogen as
  acetylene (twelve-month C2H2/H2 0.64), where the leaks bring diverter oil at 9.8 and 8.2. Construction: the gas per
  operation is held constant through the arc, the onset is just after the December 2024 sample, and Rolleston's tap
  changer follows the step loads of the processing plant on its feeder (its own random stream, so no other unit's
  draws move; plant seed chosen so all 18 grid columns keep the order with at least 5.3 per cent margin and the
  tracking r is at least 0.985 in every window and below-detection reading). Only RLS-T2's tap-operation figure moves
  in the goldens (27,534 to 49,897, still inside the interval). A first draw on the substation's ordinary load-swing
  switching, with the onset in January 2025, fell to r 0.884 from the last below-detection result and let Coalgate T1
  pass it on a 400-day base; both rejected.

- **Architecture 1 spent at round 1 (2026-10-11): screen grain (metering system against supply number).** Plain
  solver 81.3 and skeptic 85.6, both on Caithness 54 against Elgin 35. Plain: "rp_mart_weekly_import was rejected for
  screening because it sums each related point into its primary's metering system: mart = primary + related reads to
  within 0.2 kWh." Skeptic: "Supplies sheet (2,960 main MPANs) plus Related metering points sheet (699 heating-only
  MPANs, each with its own supply number) gives 3,659 supplies, matching the 3,659 MPANs in the reads parquet." The
  grain the procedure screens has to be filed for determinism, and once filed it is a work order: both rebuilt per
  supply from the reads and reconciled the mart before rejecting it. The ask devices (re-keyed jobs, appeals keyed to
  the raising system, the Scottish calendar, a mid-quarter start) were each executed off a filed rule. Not hardened:
  the only rung that would stop this step is a plant (withholding the glossary makes the grain a fork). Re-rooted.

- Seed AD03 as written (register split by each meter's switching regime, recovered from an operator acknowledgement
  corpus): the decisive rule withheld and recovered from a closed corpus is the capped Pattern B pin, and the
  acknowledgement file would refute the whole-house screen case by case (an alarm, not a stump).
- Register split from half-hourly data by time-of-use regime: if daily register reads ship the split is a lookup, and
  if they do not, the realistic route is the separate heating supply, which is how north-of-Scotland storage heating
  is actually metered, so the build uses related supply numbers.
- Account-level shortfall of heating diversions above 25 per cent (first parameter pass, heating 0.62 to 0.86 kWh per
  degree day): too close to the 30 per cent band for convergence across weather readings; heating sensitivity cut to
  0.42 to 0.62.
- Strathspey at 9 heating diversions tied Inverness City at 19 referrals, an ordering fork in the ranked chart; cut to 6.
- First cut of the pack (mart keyed by billing account and described as "the account's metered import", heating-only
  supply numbers listed inline on the Supplies sheet with a `related_mpan` column): the solver's-eye leak reader's plan
  of attack, before any solve, was "screen each MPAN separately, including the related heating-only ones" and "use the
  mart only as a sanity check, since it is per account". The decisive grain was announced by the file layout. The mart
  is now the metering-system table it would be at a supplier, keyed by the primary supply number, and the related
  metering points sit on their own CIS sheet, so the natural pipeline (Supplies sheet plus mart, or plus the reads) is
  keyed by supply number and silent everywhere. The same reader flagged RP-07's revision table (its two lines named the
  own-history degree days and the occupier window) and the DNO loss file ranking Lochaber top, echoing the belief; both
  rewritten.

- **Leak reader pass 1 on architecture 2 (2026-10-11), hardened before any solve.** The reader quoted nothing for
  question 1, but its plan of attack read "check that no code 3 rise looks like gas from the tap-changer compartment
  (1.2, 5.1)": the standard's scope sentence (the coding applies to the gases generated in the main tank), its
  clause on annual compartment sampling and the compartment results file together turned the attribution into a work
  order. Removed: the scope sentence, the sampling clause (and its revision-history mention) and the compartment file,
  which no ask needed. What stays filed is the remedy (5.1, an internal inspection is the remedy for a fault in the main
  tank) and the allocation to transformers whose main-tank gases point to such faults (5.2); the attribution rests on
  the tap-changer type, the counter tracking and the acetylene-to-hydrogen ratio, all of which the main call already
  reads for other reasons, and on IEC 60599, which the standard cites.

- **Section 5.2 reworded for determinism (2026-10-11).** With the scope sentence gone, section 4 codes the main-tank
  results as reported, so DSL-T1 and LST-T2 are code 3, and the old 5.2 ("the outages go to the transformers whose
  main-tank gases point to the most severe such faults") could be read as plain code 3 by severity, which lands rung 1.
  5.2 now allocates the outages "to the code 3 transformers with such a fault", the fault being 5.1's fault in the
  main tank, and the goldens report the literal section 4 code, so the code column has one reading and the slate turns
  only on where the fault is. The board paper says both stay code 3 and need tap-changer work instead.

- **Re-root candidates weighed for architecture 2 and not drawn (2026-10-11).** A heat-pump drop told from a diversion
  by its day and night registers, with the heating measures register as the convenient record: the register would be
  the narrower file the clean-data test repairs, so the defect would carry the stump. A weekly referral queue replayed
  run by run: a filed lifecycle is a filed formula, executed. Re-tampers hidden by a baseline that includes the earlier
  diversion: the use-versus-recorded distinction has to be filed in RP-07's glossary, which is where architecture 1 was
  read. Evaluating a new screen on a verification sample: inverse weighting is reflexive once the sampling is stated.
  Revenue protection was left for a transformer fleet, where the decisive step is a diagnostic attribution no filed
  sentence names.

- **Build of architecture 2 (2026-10-11), approaches dropped on the way to the shipped pack.** Leeston T2's last
  tap-changer service in February 2022 put both leaking units past their tap-changer interval (72,409 and 87,696
  operations), so the ask table pointed at the two tap changers the main call turns on; the service moved to May 2023
  (54,294, not past). Attribution signatures computed for every unit with detectable acetylene swept in stable traces
  (SBG-T1, GLT-T1) and the thermal units' crumbs, with C2H2/H2 undefined where hydrogen fell; the signatures are now taken
  only where acetylene rises faster than its rate limit. Thermal survey temperatures to the half degree collided with
  graded figures (33.1, 34.9, 12.5, 27.0, 28.5) inside a document; whole-degree maxima and fixed rises now, with a sweep
  asserting no graded figure in any shipped document. The extract log's "first hour 01/01/2021 00:00" against a parquet
  whose first timestamp reads 2020-12-31 11:00 announced the UTC export in one line; dropped. Interval-length confounding:
  with quarterly and monthly samples mixed, any steady gas source correlates with tap operations through interval
  length, so the vacuum unit's increments are designed in bursts and asserted uncorrelated raw and per day.
- **Severity distance "at least 0.005 from a two-decimal edge" (the build brief).** 0.005 is the half-width of a
  two-decimal bin, so only an exactly round severity meets it, which determinism-check reads as a receipt. Asserted at
  least 0.002 from the edge and at least 0.0003 off the round value instead (worst 0.0021, BNM-T1; naive 9.6415 and
  8.0674).
- **Personas the guard's people sweep read into the pack (2026-10-11).** The substation at Tai Tapu read as a person
  (first name Tai) and blocked against task123, and "Karl Fischer" in the water-content method line read as another
  persona; the substation is Ladbrooks (LDB) and the method line cites IEC 60814. No figure moved (per-unit draws are by
  fleet position, not by name).
