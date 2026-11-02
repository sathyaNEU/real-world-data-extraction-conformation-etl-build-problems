# task123 determinism check (architecture 4)

3 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 1e6fa5a6 | DETERMINISTIC (order kept; F good; G PASS; H PASS) | APPROVE, with four Gate C forks on ask cells closed by the main session's rule | every off-site application resolvable to one car space; the reads export's own legend for read and register types; section 6 says a three-phase supply is outside while any phase is; ask devices rebuilt |
| 2 | b5549311 | NOT_DETERMINISTIC on supplementary 5 only (order kept; F high; G PASS; H PASS) | SEND_BACK as labelled; an ask repair by the gate table | section 6 says which record governs (a record counts only where the meter's own hourly extreme is outside the limits), that outside means above 253 V or below 216 V, and that the week runs midnight to midnight in market time; event extremes kept off the limits |
| 3 | d39160e5 | DETERMINISTIC (order kept; F good; G PASS, binding_constraint / analytical_non_defect; H PASS) | APPROVE | none (the two optional wording tweaks not taken: the rejected routes are named as alternatives, and the interval-sum route is the only exact one) |

Architecture 3's judge record is in determinism_check_report_arch3.md; architecture 2's in the _arch2 reports.

---

# Determinism check, round 1 (2026-11-02): DETERMINISTIC (order kept; F good; G PASS; H PASS), APPROVE, with four Gate C forks on ask cells closed by the main session's rule

Isolated thread, Sonnet at medium effort, on target.zip 1e6fa5a6.

# Verdict (task123, run a4r1)

Order kept: derivation.md was written to disk from prompt.txt and target/ before graded_blocks.md was opened.

**Verdict:** DETERMINISTIC (main call forced; four residual forks on the supplementary asks, none moves the call).

**Disposition:** APPROVE for the main recommendation and the 18-row asks as shipped; optional in-house tidy (pin the four forks below in the metadata or fork table) needs no model rerun. No SEND_BACK trigger (Gates G and H pass).

**Why:** Executing standard sections 2 to 5 literally on the files, with each single-phase apartment placed on its phase, gives busiest-phase shares A4 109, C3 97, B2 94, C6 89 over the 80 line and B3 75 nearest under (next A1 73, C4 71); margins are 9 points or more on every side and no rounding edge. The phase is in no column, but voltage co-movement in QES_PQ_hourly_V separates every riser into three clean clusters (18 of 18, ward and average linkage give the same partition, merge height 5-9 inside groups against 25-40 between), so the reconstruction is unique and the data, not a convention, forces it. All 18 x 4 supplementary figures reproduce.

**Evidence (recomputed from target/):**
| Figure | Source | Reproduced |
|---|---|---|
| Worst-phase share A4 109.19, C3 96.80, B2 94.06, C6 89.24, B3 75.13 | child register + lots + nem12 E1 (x2 kW, 40 half-hours) + works schedule (64 chargers x 3.7, 154 cooktops x 1.4, 3PH split equally) + voltage clusters + 2019 rating x 0.230 kW | yes, all 18 risers, same set over 80 |
| July use, 18 risers (11.76 ... 10.43) | register reads Jul 1/Aug 1 E1+E2, exchange file for 21 swaps, interval sum where Aug-1 read is E, register where interval series is truncated (66 meters) | yes, 18/18 |
| Request counts, 18 risers | applications, distinct car spaces, re-marking applied where the written number is old, accessory unit via lots extract, V-bays excluded | yes, 18/18 (C5, C6 = 0) |
| Voltage share, 18 risers | events JSON, union across elements and repeats, clipped to 2026-07-12T14:00Z to 07-19T14:00Z | yes, 18/18 at 2 dp |
Easy route check: assuming the load balanced over three phases flags no main (max B2 77), so the call turns on the phase reconstruction.

Forks found (gate each fails if it were counted against the asks; none touches the main call):
- F1 (Gate C/E, supplementary 5): three-phase apartments (B2 one, C6 two). Union of elements gives B2 1.50 and C6 1.71 (golden, and the literal reading of s.6 "the time its meter recorded"); mean over elements gives 1.47 and 1.64; sum gives 1.60 and 1.95. Only B2 and C6 change; the union is the dominant literal reading.
- F2 (Gate C, supplementary 3): "energy its meter registered" with E1 only gives 8.35, 8.52, 8.04, 8.47, 8.15 for A4, C3, B2, C6, B3 against 11.34, 11.96, 10.61, 10.43, 11.58 on E1+E2. The meter registers both and the golden says every register; reasonable but nothing defines the registers.
- F3 (Gate C, supplementary 3): the 40 estimated (E) August reads. Using them as read gives B2 10.40 and B3 11.50 instead of 10.61 and 11.58. "E" is not defined in any shipped file; the golden replaces them with the full-month interval sum. Moderate; section 7 "registered" supports it.
- F4 (Gate C/E, supplementary 4, the weakest): after the March 2025 re-marking, 31 of 48 in-complex B2/B3 applications still quote old numbers (confirmed by the stated unit and the works schedule), so the date cut does not work. For the five off-site, unapproved post-March (or re-)applications (EVC-25-069 B2-003, EVC-25-104 B2-053, EVC-26-098 B3-098, EVC-26-154 B2-027, EVC-26-172 B2-074) neither a stated unit nor the schedule fixes the numbering. The golden takes them as written. Taking all five as old numbers gives A4 7, C3 7, B2 7, B3 5 against the golden 6, 6, 5, 6. Support for as-written: all 9 approved off-site applications are new numbering, and two of the five are continuations of earlier lapsed requests only under new numbering. EVC-25-069, EVC-26-098 and EVC-26-154 have no such support.

**Files/Hygiene:** PASS. 15 files, 5 formats (xlsx 6, pdf 3, csv 5, json 1, plus nem12 csv variants), one 86,016-row file and a 6.5 MB NEM12; distractors present (thermal scan PDF, common property submeters, parent NEM12). Dates coherent (standard 14 Oct 2026, works schedule issued 6 Nov 2026, register as at 31 Oct 2026). No authoring or provenance language seen, no public-answer contamination. No exclusion-level finding. Cross-batch check: no prior-batch list was supplied to me, so no near-duplicate could be tested.

**Stump power:** Good. The deciding step is recovering which phase each single-phase apartment sits on from voltage co-movement; the balanced-phase easy route (and a random-phase one) flags nothing or the wrong set, so a strong model that does not reconstruct phase fails the call. The 18-row asks add real Layer 1 work (UTC vs market-time week, 21 meter swaps, 66 truncated interval series, estimated reads, re-marked car spaces, mixed address formats) that cannot all be got right by default.

**Stumping type:** `mechanism: other (latent structure recovery, phase membership from voltage, then a binding-capacity test)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is overturned; clean data would still need the phase reconstruction. Gate G passes.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Field analysis: per-phase peak coincident demand against rising-main rating (phase balancing and hosting capacity). Layer 1: market time vs UTC, meter swaps, estimated and truncated reads, re-marked spaces. Layer 2: phase identification. The easy route (spread each main's load evenly over three phases) is read and computed correctly yet gives no main over 80 (max B2 77), the wrong answer. Swap test: another utility's phase data is required, so it is not a backdrop.

**Fix:** none required for the call. Optional (solution or metadata only): record F1 to F4 in the fork table with their closures (union of elements; both registers; estimated read replaced by intervals; off-site numbering taken as written). If the author wants F4 removed outright, the only real repair is an input change (a stated unit or note on the three unresolved off-site applications), which would be a SEND_BACK-class change for five cells; not recommended.

---

# Determinism check, round 2 (2026-11-02): NOT_DETERMINISTIC on supplementary 5 only (order kept; F high; G PASS; H PASS), SEND_BACK as labelled; an ask repair by the gate table

Isolated thread, Sonnet at medium effort, on target.zip b5549311.

# Determinism verdict, task123 (a4r2)

Order kept: yes. derivation.md (literal reading, open options, my own values for every figure) was written to disk before graded_blocks.md was opened; the one addendum about the re-sent events was also written before it was opened.

- **Verdict:** NOT_DETERMINISTIC (one supplementary answer, Q5; the main recommendation and Q1 to Q4 reproduce).
- **Disposition:** SEND_BACK. The repair changes what solvers see (the standard's section 6 or the PQ event export), so prior runs are invalid and a rerun is required.
- **Why:** Q5 (voltage shares, riser_capacity_2027.xlsx item 5) is only reached by discarding 232 logged swell events (189 in the week) that repeat an earlier event on the same meter about 10 hours later, which nothing filed says to do. Section 6 of the standard says an apartment's time outside the limits "is the time its meter recorded its supply outside them"; read word for word, the event log is that record, and it gives A1 1.56, A3 1.91, B4 2.13, C1 1.25 and so on against the golden 1.50, 1.61, 2.02, 1.06, up to 0.72 points apart (2 of 18 figures survive). The meter's own hourly maxima contradict the repeats, so the golden's resolution is the better one, but which record governs is not filed (Gate C, underspecified_objective). Q5 also has a knife edge: C2 is 1.5671 (golden 1.57) only if the 11 events whose extreme is exactly 253.0 V count, 1.5648 (1.56) if they do not.
- **Evidence (recomputed from the bundle):**
  - Rising mains and ratings: 18 mains from the 2019 schedule, units joined by tower and level (board column agrees for 420 of 420), kW = A x 230 / 1000. Reproduced.
  - Phase: no file records which phase a single-phase apartment is on (register has only 1PH/3PH, element is 1 for every 1PH meter). Hourly voltage, minus the site mean, splits every main into three groups (within r about 0.95, between about 0), the three elements of each of the 14 three-phase meters land in three groups, and the partition is identical under average, single, complete and ward linkage and on raw series. Recoverable and unique, but by an inference no document names (see Gate B note below).
  - Peak demand, 40 half-hours (17:00 to 20:30 market time, 13 to 17 July), 2 x kWh, three-phase split in thirds, charger 3.7 and cooktop 1.4 kW to the unit named (4 chargers and 5 cooktop units are three-phase): A4 109.19, B2 94.06, C3 96.80, C6 89.24, B3 75.13 (next C4 70.99, A1 72.71). All match the golden. Controlled load is exactly zero in the window, so E1 against E1+E2 is not a fork. "Phase with highest existing, then add its additions" gives the same five graded shares (differs only on A3, B6, C2, C4, C5, none graded).
  - Golden's rejected alternatives reproduce: balanced allocation puts no main over (max B2 77), position rotation gives A1 86, B2 85, C6 88 and A4 79.5, C3 74.
  - Q3 use: register movement Jul 1 to Aug 1, exchanged meters spliced through old final and new initial, interval sum for the 32 meters whose Aug 1 midnight read is an estimate (estimate understates by about 46 kWh each; the later actual read overstates by 2 to 8 kWh of August use), registers for the 66 NMIs whose interval file stops on 20 or 22 July and for the E51-substituted series. All 18 reproduce to two decimals (A1 11.76 ... C6 10.43). Reading the late actual read or the estimate instead moves B1 to 12.42 or 11.87 and B2 to 10.63 or 10.27, so this too rests on an unfiled choice; section 7 ("energy the meter registered over the period") supports the golden, so I do not fail on it.
  - Q4 requests: 97 distinct car spaces, all 30 repeats follow a lapse or decline; B2/B3 numbers resolved row by row (exactly one of as-written or re-marked matches the owner named, 127 of 127); three "(for the OC)" visitor-bay applications left out (section 8). All 18 reproduce. Counting the OC ones would add A1 +1, B5 +1, C6 +1, a minor reading difference closed by section 8.
  - Q5: reproduces only with the repeats removed; see Why. Week taken in market time (12 July 14:00Z to 19 July 14:00Z); calendar UTC days would move every figure by 0.2 to 0.5 points and the standard names market time only in section 3, a smaller extra fork.
  - Gate A: no figure changes between blocks; the SVG item is described, not shipped, so not recomputed.
- **Files/Hygiene:** PASS. 15 files, 4 formats (6 xlsx, 5 csv, 3 pdf, 1 json); the half-hourly NEM12 (20,922 lines, 48 intervals each) and the 86,016-row hourly PQ file clear the size gate; distractors present (parent NEM12, house sub-meters, 2025 thermal scan, EV register's approved count against the works schedule). Dates cohere (standard 14 Oct 2026, register 31 Oct, schedule 6 Nov). Mess is plausible (six unit formats, mixed car-space numbering, estimated reads, truncated feeds). The standard reads somewhat like it was written to define the asks, a mild tell, not exclusion-level. No authoring leakage found. metadata.json not in the bundle, so the distractor naming was not checked. Cross-batch check: no other task is readable in this run, so not performed; no near-duplicate is visible inside the bundle.
- **Stump power (Gate F):** High. The easy routes both fail the main call: assuming balanced phases files "no main needs works", position rotation files A1, B2, C6 (wrong set). Only recovering the wiring from voltage co-movement gets A4, B2, C3, C6. Extra layers on the asks (meter exchanges, estimated reads, mixed car-space numbering, repeated events) each catch a careful but unlucky solver. Risk of being unreachable rather than hard: nothing in the bundle hints that voltage is the phase key.
- **Stumping type (Gate G):** mechanism: other (latent-attribute reconstruction, joined to etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. No reported number or stakeholder conclusion is overturned; the main difficulty survives on perfectly clean data because the phase column does not exist. The repeated-event removal in Q5 is a planted-defect step but sits on an ask, not the main call.
- **Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical (borderline, see note).
  - H1: rising-main phase loading against an 80% criterion, phase identification and voltage compliance are building electrical network work; swapping nouns does not leave the task unchanged.
  - H2: Layer 1 is meter exchanges, estimated and late reads, truncated interval feeds, re-marked car spaces, free-text unit formats, UTC against market time. Layer 2 is recovering each supply's phase and testing the heaviest phase, not the riser average.
  - H3: easy route = spread each single-phase apartment evenly or by position, which gives no main over the line, or A1/B2/C6; the committed set needs the recovered phases. Note: the step is a reconstruction with no filed instruction (an "actor with no column"), not a field reading or rule execution, so I classify it analytical, but it sits close to a hidden-rule step.
- **Gate B note (not a failure on its own):** the decisive wiring fact is absent as a field and recoverable only from the PQ voltage series; a literal reader who does not look there has no licence for any allocation and may answer "none". Consider one sentence in section 2 of the standard saying the register does not record the phase and the meter voltage record is what shows it (this lowers stump power, so the author's call).
- **Fix:** input_files. Pin Q5: either file in section 6 which record governs ("an excursion counts only where the meter's own hourly maxima show it"; this is a WHAT, the population of counted time) or remove the repeated events from the export so the log has one record per excursion; also decide the events at exactly 253.0 V (the C2 edge) by the same sentence or by removing them. Then rerun. Everything else (main call, Q1 to Q4, SVG) is frozen and reproduces.

---

# Determinism check, round 3 (2026-11-02): DETERMINISTIC (order kept; F good; G PASS, binding_constraint / analytical_non_defect; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip d39160e5.

# Verdict, task123 (a4r3)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (optional, in-house wording tidy-ups only: see Fix; no rerun needed).
- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened. Cross-batch fingerprinting could not be done (no access outside the folder); not reported as a pass.

## Why
The main call (A4, C3, B2, C6 over the 80 per cent line, B3 nearest under) reproduces exactly from the bundle under a literal execution of the 2026 capacity standard. The only unfiled step is which phase each single-phase apartment is on. The shipped voltage trace separates every riser's single-phase meters into exactly three groups (within-group correlation at least 0.988, between-group at most 0.97). Ward, single-linkage, average-linkage and k-means all give identical partitions, so the groups, and therefore the shares, do not depend on the method. Every one of the 18 rows of each supplementary answer matched my independent value.

## Evidence (my values vs golden, all reproduced)
| Item | Source and field | Mine | Golden |
|---|---|---|---|
| Busiest-phase share | NEM12 half-hours 17:00-20:30, 13-17 Jul, 2x kWh; phase groups from hourly V; works schedule 3.7/1.4 kW; MSB ratings x 0.230 | A4 109.19, C3 96.80, B2 94.06, C6 89.24, B3 75.13 (next A1 72.71, C4 70.99) | same, whole per cents |
| Window | E2 is exactly zero in the window; no E51 or N intervals on 13-17 Jul; every meter has those 5 days | E1 vs E1+E2 is not a fork | same |
| July use, 18 risers | register reads; 21 exchanged meters (old_final minus start, plus end minus new_initial); 40 meters whose 1 Aug 00:00 read is Estimated use the July interval sum; 66 meters have no interval days 23-31 Jul so intervals alone fail | A4 11.3367, B2 10.6064, C3 11.9641, C6 10.4289, B3 11.5764; all 18 match to 2 dp | same |
| Charger requests | distinct renumbered car spaces; applicant unit (incl. "Lot N" for off-site owners) matched against the renumbered space's accessory unit; 3 OC visitor-bay applications excluded; zero ambiguous rows | A4 6, B2 5, C3 6, C6 0, B3 6; all 18 match | same |
| Voltage share | window 12 Jul 14:00Z to 19 Jul 14:00Z (168 h); union of swell records; a record counts only if own hourly vmax is over 253 V in a covered hour | A4 1.29, B2 1.50, C3 1.32, C6 1.71, B3 1.30 (1.29995, rounds up); all 18 match | same |

- **Records the filter removes:** the filter drops 214 of 2349 in-window records. All 214 repeat an accepted record 10.0-10.7 h later, as the golden says.
- **Competing answers tested:**
  - Balanced phases: flags nothing (max 77.0, B2).
  - Whole-record vs bad-hours-only voltage time: identical.
  - Unfiltered voltage: 1.41/1.95/1.35/1.84/1.36 for A4/B2/B3... (a rule-reading error, not a fork).
  - Date-only renumber rule for requests: 31 rows disagree with the unit evidence, which resolves every row.
- **Residual forks, none moving a call:**
  1. **Phase recovery (main call).** No file states a single-phase apartment's phase. Voltage co-movement is the only evidence and it is unambiguous. The standard calls this fact "the phase its supply is connected to" and a solver must infer it.
  2. **Midnight register for the 40 meters with an Estimated 1 Aug read (Q3 only).** The standard says "energy its meter registered over the period" and does not name the fill-in. The interval sum is exact (it equals the register difference to 0.01 kWh on 554 clean meters). Using the later actual read gives A4 11.36, B2 10.63, C3 11.98/11.99, C6 10.45, B3 11.59. Using the estimate gives 11.15, 10.31, 11.81, 10.12, 11.43. Only the interval route satisfies "over the period", so the answer is forced. It is the softest committed answer.
  3. **"For every riser."** The prompt reads either as 18 rows or as the 5 named. The golden gives 18, a superset of the 5-row reading, so no answer changes.

## Files / Hygiene: PASS
- **Count and formats:** 15 files; xlsx (7), pdf (3), csv (5), json (1).
- **Large files:** the PQ hourly file has 86,016 rows and the NEM12 file about 6.5 MB.
- **Distractors:** parent NEM12, common-property submeters, thermal scan, lot entitlements.
- **Provenance and timeline:** consistent; no authoring language seen. No public-data contamination.
- **Minor:** the golden's FINAL_RECOMMENDATION names "the installer's rotation" and "random phasing" as rejected alternatives. These terms appear in no shipped file. They are solution commentary only and not an action vocabulary issue.

## Stump power (Gate F)
Good. The easy route (spread single-phase load over three phases, or assume a positional rotation) is arithmetically clean and files "no main needs works". Only recovering the latent phase from the voltage trace surfaces the 80 per cent breaches. The workbook's voltage column is a natural cue, but no sentence says how to use it. Some strong models will find the voltage clustering, so the stump rests on whether they bother. Further hardening is optional.

## Stumping type (Gate G)
`mechanism: binding_constraint` (per-phase limit on honest data, latent phase structure recovered), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is misleading; the difficulty is the unrecorded phase attribution. Clean data would still leave the task requiring the phase inference. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- **Layer 1:** meter exchanges, Estimated reads with later actuals, interval gaps, application-address formats, March 2025 renumbering, UTC vs market time.
- **Layer 2:** per-phase coincident-peak loading against the derated rising main, with phase recovered from the voltage trace.
- **Easy route:** a strong analyst who cleans the data and applies every rule would take the balanced split. The result is no flagged main (max 77 per cent, B2) and a wrong "nowhere" call.
- **Swap test:** the quantity deciding the call is network phase-balance engineering, which no other field's nouns would carry.
- **Caveat:** if a reader holds that the phase attribution is a hidden rule rather than inference, H3 would be contested. I judge it inference, because the data separates cleanly and no instruction is withheld.

## Fix
- **Where:** none required for determinism.
- **Optional (solution text only, no rerun):** drop the "installer's rotation" and "random phasing" phrases from FINAL_RECOMMENDATION.
- **Optional:** state in SOLUTION_STEPS that the interval sum is used because the Estimated midnight read and the later actual read both fail "over the period".

## Findings by gate
- **Gate B/C, low severity:** phase recovery rests on inference, but the data forces it.
- **Gate C, low severity:** the Q3 estimated-read fill-in is unfiled but forced.
- **Gate E, nil:** the "every riser" scope is a superset reading.
