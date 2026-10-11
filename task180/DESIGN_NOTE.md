# task180 design note: Ellesmere Lines, the three internal inspections of 2027/28 (architecture 2)

Seed AD03 (revenue-protection crew). Architecture 1 (revenue protection, the screen grain) was spent at in-house
round 1 and is recorded under Tried and rejected. This is the re-root: same objective, same number, a new draw. The
seed's idea that carries over is the one AD03 shares with the whole lane: the loudest signal is not all cause.

Figures marked *target* are what the generator is tuned to; `checks.py` asserts the shipped values and the write-up
uses only those.

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
Stump strategy: stated_rule_hard_construction   Decisive rule filed? yes (ES-DGA-02 s4.1 scope and s5 priority)
Official decoy filed? no   Validated decoy? no
Forum: board_of_directors (28 October 2026)   Forcing event: audit_or_inspection   Org family: utility_or_infrastructure
People (guard.py names, en_NZ, seed 1802): Donna Carson (network asset manager, the requester), Barry Forbes (zone
  substation engineer, owner of ES-DGA-02 and the oil results), Wendy Godfrey (board chair), Connor McGill (oil sampling
  technician)
```

**Data-native sentence.** Older zone-substation transformers switch load on an in-oil arcing tap changer that sits in a
compartment sharing a barrier with the main tank, so when that barrier weeps, the acetylene every tap change makes in
the compartment turns up in the main-tank oil the fleet is coded on, rising with the tap-change count rather than with
any fault in the winding.

**Layer 1 (realistic mess and the system that produces it).** A laboratory results file per sampling round (sampling
date and analysis date, gases in ppm with below-detection values written as `<n`, oxygen and nitrogen, moisture, the oil
temperature the technician wrote down or left blank); tap-changer compartment results on their own annual schedule; an
asset register with rewind years and tap-changer types; SCADA daily tap-change counters that roll over at 99,999 and
reset when a counter is replaced at a tap-changer service; hourly SCADA top-oil temperatures exported from the
historian in UTC; a maintenance log in free text.

**Layer 2 (the analytical shortcut).** Coding each transformer on its main-tank gases and ranking the code-3 units by
severity. The standard's arithmetic is right and every gas really is in the main-tank oil; an expert first asks where
each fault gas was made, because the standard codes gases generated in the main tank, and acetylene carried in from a
tap-changer compartment is made by normal switching, not by a fault an internal inspection can find.

**Similarity claim.** No prior build attributes a measured anomaly to an attached compartment's normal operation before
ranking. task181 (explaining away a dominant source among pooled victims) is a different structure: there the sources
compete for the same victims; here each unit's own signal has a second, benign origin.

## GATE G

- **Litmus.** Nothing reported is overturned: every laboratory value, counter reading and register field is correct;
  the standard's codes and severities are computed correctly. The difficulty is which units' gases point to a fault
  inside the main tank.
- **Primary mechanism:** decomposition_attribution.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete Barry's note and the mobile substation schedule: coding on main-tank gases still names the
  two leaking units; attribution still removes them.
- **Clean-data and instrument test.** No file is incomplete or stale for the decision: every main-tank sample, every
  compartment sample and every counter reading ships. A perfect main-tank gas analyser still reads the leaked acetylene,
  because it is really in the oil; what the decision needs is its origin, which the counters, the tap-changer types and
  the gas ratios settle.
- **Lens swap.** Not one population under two lenses: the answer's ranking runs on main-tank gases generated in the main
  tank, a different set of gas volumes from the naive ranking's, built per unit from three files.

## STUMP SENTENCE

A competent solver codes every transformer under ES-DGA-02 from its main-tank samples (limits by preservation type and
age, twelve-month increases, code 3 ranked by severity) and names the three highest code-3 units, two of which carry
acetylene leaked from in-oil tap-changer compartments; the step that lands it there is reading main-tank acetylene as a
main-tank fault, when at those two units its increments track the tap-change counts and its ratio to hydrogen is the
tap changer's, so the slate takes the vacuum-tap-changer unit with the same acetylene, the in-oil unit whose acetylene
is internal, and the worst thermal fault.

## ENTITY AND UNIT OF VALUE

One transformer, one inspection outage. The standard's severity score is a ratio of a gas's twelve-month increase to its
rate limit; the slate is three transformers in priority order.

## LADDER (targets)

Units (target severities): L2 and L1 (in-oil tap changers, leaking barriers), V (vacuum tap changer, internal arc), A3
(in-oil tap changer, internal arc, not leaking), T1, T2, T3 (thermal faults).

| Rung | Construction | Slate | Why a careful analyst stops | Killed by |
|---|---|---|---|---|
| 0 | Highest latest acetylene (arcing read off the Duval triangle) | L2, L1, V | arcing is the most severe fault class | ES-DGA-02 s4 codes on levels and twelve-month increases, not the latest level |
| 1 | ES-DGA-02 code 3 on main-tank gases, ranked by severity | L2 (9.6), L1 and V (8.1 each), then A3 (4.9), T1 (4.7) | the filed standard applied exactly | at L1 and L2 the main-tank acetylene increments track tap-change counts (r at least 0.97), C2H2/H2 is 4 or more, the tap changers are in-oil arcing types |
| 2 | Drop the unit with the clearest leak only | L1 or L2, V, A3 | one contaminated unit found | the other leaking unit carries the same signature |
| 3 | Drop acetylene at every in-oil tap-changer unit | V, T1, T2 | a rule of thumb about tap changers | A3's acetylene does not track its counter and its C2H2/H2 is 0.6: internal |
| 4 (answer) | Attribute each unit's acetylene, code what the main tank made | **V, A3, T1** | | |

**Twin pair.** L1 and V carry the same main-tank acetylene trajectory (the same levels and the same twelve-month
increase to 0.1 ppm), the same preservation class and the same age band, so code and severity are identical; L1's tap
changer is in-oil and its acetylene tracks the counter, V's is vacuum. Any rule on main-tank gases keeps both or drops
both.

Margins: the answer's third unit (T1, 4.7) clears the fourth (T2, 4.4) by at least 5 per cent of severity; every wrong
slate differs from the answer by at least one named unit, asserted.

## GRID (asserted in checks.py)

Rows: the five rungs above; acetylene dropped for units with C2H2/H2 above 2, 3 and 5; correlation thresholds 0.8, 0.9
and 0.95; leak judged on increments per sample interval or on cumulative growth. Columns: below-detection values at
zero, half the limit or the limit; twelve-month base sample at 330, 365 and 400 days; preservation class from the latest
or the median O2/N2. Asserts: every attribution rule that uses any two of the three signatures (in-oil type, tracking,
ratio) returns V, A3, T1 in every column; every main-tank-only rule returns a slate with L1 or L2 in it.

## CLOSURE (the 22 axes)

1 Population: the 44 zone-substation transformers in service (ES-DGA-02 s1). 2 Unit: transformer. 3 Window: twelve
months to the latest sample (s4.3). 4 As-of: latest main-tank sample on or before 30 September 2026. 5 Version basis: the
laboratory report of record is the latest issued for a sample ID (s3). 6 Divisor: rate limits per gas (s4.3 table).
7 Weighting: none. 8 Window length: base sample the earliest at least 330 days before the latest (s4.3); 365 and 400
converge. 9 Boundary: no severity within 2 per cent of the slate cut. 10 Rounding: severity to two decimals, no unit
within 0.005 of a rounding edge. 11 Tie-break: the L1/V tie sits inside the naive slate, never at its cut. 12 Maturity:
the September round complete for every unit. 13 Order of operations: attribute, then code, then rank. 14 Row order:
irrelevant. 15 Duplicates: re-issued laboratory reports for the same sample ID (D2, ask layer only). 16 Identity:
transformer IDs stable; tap-changer counters replaced keep the transformer ID. 17 Netting: none. 18 Units: ppm (uL/L).
19 Code semantics: preservation class by O2/N2 (s4.1). 20 Integerisation: none. 21 Scope: s4.1 gases generated in the
main tank. 22 Forward window: none in the call.

## ASK SHEET (devices off the main call's rows)

Main call row population (declared, asserted device-free): main-tank and compartment results for every transformer;
the daily tap-change counts and the asset register rows of every code-3 transformer.

| Ask | Figures | Primary devices (silent) | Shared hazard |
|---|---|---|---|
| A. Tap-changer service: every in-oil tap changer's operations since its last service and whether it is past the interval (ES-DGA-02 annex B) | about 28 x 2 | D7/D2: a counter drop is a rollover at 99,999 unless the counter was replaced at a service that day (maintenance log free text); the asset register's last-service field predates the 2025 and 2026 services, and the maintenance log is the record of service (s6) | H1 laboratory re-issues (a corrected report under the same sample ID supersedes the first) |
| B. Wet transformers: relative saturation at each unit's latest sample, those above 30 per cent | about 6 | D8: the SCADA historian exports UTC (New Zealand is UTC+13 in October), so joining the hourly top-oil temperature on the local clock reads the wrong half of the day where the technician left the sampling temperature blank; D8: the results file's `date` is the analysis date, the sampling date is `sampled` | H1 |

Use test: both are the next two tables of a board paper that asks for three inspection outages (tap-changer backlog,
wet units for oil processing). Decoupling: clearing the attribution moves no figure in A or B (asserted).

## PINS

Filed: ES-DGA-02 Fleet DGA condition standard (governing): scope (s1), sampling and the report of record (s3), coding
(s4: preservation class, age bands, levels, twelve-month increases, codes, severity), inspection priority (s5: an
internal inspection is the remedy for a fault in the main tank; the outages go to the transformers whose main-tank gases
point to the most severe such faults), tap-changer service record (s6), annex A limit tables, annex B service intervals,
annex C relative saturation. Oil results notes (field semantics). No sentence mentions compartment leakage.

## PACK GATES (targets)

At least 12 files, at least 5 formats; hourly SCADA top-oil temperature parquet above 1,500,000 rows; two distractors
named in metadata.json: the protection relay event log (fault records on the 11 kV feeders) and the 2026 thermal
imaging survey of the 11 kV switchboards.

## SIX-POINT CHECK

1. Real work: laboratory formats, detection limits, preservation class from O2/N2, rollovers and counter replacements, a
   free-text maintenance log, UTC historian exports. 2. The flip is a method choice: attributing gases to their source
   before coding. 3. ES-DGA-02 defines the population, the coding, the window and the priority. 4. No decoy memo; Barry's
   note is true. 5. The method is not recovered from certified figures. 6. No earlier task teaches source attribution of
   a diagnostic signal before ranking.

## STOPPING RULE

Two rounds in which both solvers attribute the acetylene unprompted file this architecture as at-ceiling; a miss landing
anywhere other than rungs 0 to 3 is read for a fork before any hardening.

## Tried and rejected

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

- **Re-root candidates weighed for architecture 2 and not drawn (2026-10-11).** A heat-pump drop told from a diversion
  by its day and night registers, with the heating measures register as the convenient record: the register would be
  the narrower file the clean-data test repairs, so the defect would carry the stump. A weekly referral queue replayed
  run by run: a filed lifecycle is a filed formula, executed. Re-tampers hidden by a baseline that includes the earlier
  diversion: the use-versus-recorded distinction has to be filed in RP-07's glossary, which is where architecture 1 was
  read. Evaluating a new screen on a verification sample: inverse weighting is reflexive once the sampling is stated.
  Revenue protection was left for a transformer fleet, where the decisive step is a diagnostic attribution no filed
  sentence names.
