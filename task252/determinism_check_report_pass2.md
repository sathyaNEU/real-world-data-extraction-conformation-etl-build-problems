# determinism-check report, task252 (2026-11-01, the isolated thread's verdict on the leak-repaired cut 19b5e04d, kept as filed; not reconciled, because the build went to an ask rework and then to PAUSED)

**Verdict:** NOT_DETERMINISTIC (the main call and supplementary ask 1 are forced and reproduce; supplementary asks 2 and 3 are not forced by any shipped file). No SOLUTION_WRONG: every golden figure reproduces from the files under the reading the solution blocks describe.

**Disposition:** FIX_NOW. Pin two facts in the input files (the laboratory's analysis clock; which of the historian's unfilled F runs reached the PLC) with the readings, the register, the checks and the ask 1 golden untouched. Only the ask 2 and ask 3 answers need a rerun, and the stump on the main call is not touched.

**Why:** The flagged set (BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1) falls out of the readings, the register and the checks the same way for every rigorous route I tried, with at least 0.0034 mg/L of clearance to the 0.005 line. Ask 2 (late-analysis counts) holds only if every laboratory analysis stamp is moved forward an hour, and no file says the laboratory clock runs an hour behind. The literal stamps give 11/6/7/9/8/7/11/10, not 14/9/8/12/11/13/14/11. Ask 3 (fixed-dose hours) depends on deciding which unfilled F runs reached the PLC. The only stated rule (a check follows every cleared fault) points the other way for the storm-night stops, so a literal reader gets 26.0/22.0/32.0/28.5/21.5/28.5/26.0/23.5, not the golden. Gates C and E fail on asks 2 and 3; governing label underspecified_objective (analysis time base and PLC-reach rule not pinned). Gates A, B and D pass for the main call.

**Evidence** (all recomputed from target/; "reproduced" means my figure matches the golden)

Main call, ask 1. Reading = nh3_online_readings_2027Q4.csv, G rows only (F/G duplicate slots resolved to G; V excluded).
- Fitted shares (readings of the two earlier slots, both treated ports, each with its own level and raw readings 2 to 8 h earlier; per analyser):

| Analyser | Slot before | Slot before that |
|---|---|---|
| BRN | 0.072 | 0.019 |
| DUN | 0.079 | 0.017 |
| ELS | 0.076 | 0.021 |
| GAR | 0.066 | 0.019 |
| HOL | 0.070 | 0.020 |
| ASH, CAL, FEN | below 0.006 | below 0.002 |

  Reproduced (7 per cent and 2 per cent).
- Carryover offsets (shares times the differences, divided by one less both shares): BRN-FW1 +0.0115, DUN-FW1 +0.0122, ELS-FW1 +0.0091, GAR-FI1 +0.0265, GAR-FW1 +0.0112, HOL-FI1 +0.0254, HOL-FW1 +0.0077, all others within 0.0015 of zero.
- Calibration, from the check means in analyser_verification_2027Q4.xlsx against the raw grabs in lims_ammonia_2027Q4.csv (raw readings with raw-port carryover removed, 12 to 13 pairs per plant):
  - HOL is short by about 0.007 to 0.008 at a lab level of 0.35, so it is a zero error of -0.008.
  - CAL is about 8 to 10 per cent low at 0.49, so it is a span error.
  - The other six are within 0.002 of 0.100.
  - Reproduced.
- Line loss, from the monthly flushes in the register's Planned maintenance sheet (NZ time). CAL-FI1 and HOL-FI1 rise at each flush (about 0.010 and 0.019) and relax back, with best-fit regrowth time 2.0 days for both.
  - Mean loss over the quarter: 0.0104 and 0.0192. This holds whether the loss is fitted as additive or as a fraction of the level. Reproduced (0.010 and 0.019).
  - No other channel moves at flushes.
- Totals (carryover + calibration + line loss):

| Channel | Offset (mg/L as N) | Flagged |
|---|---|---|
| BRN-FW1 | +0.0116 | yes |
| CAL-FI1 | -0.0095 | yes |
| DUN-FW1 | +0.0121 | yes |
| ELS-FW1 | +0.0092 | yes |
| GAR-FI1 | +0.0267 | yes |
| GAR-FW1 | +0.0113 | yes |
| HOL-FI1 | -0.0018 | no |
| HOL-FW1 | -0.0003 | no |
| CAL-FW1 | -0.0009 | no |

  All other channels are within 0.0009 of zero. This reproduces the six flagged channels and the three named non-flags. The claims "0.006 or more" and "within 0.004" are true, though loose. The tightest clearances are HOL-FI1 at 0.0034 below the line and ELS-FW1 at 0.0042 above it. Sensitivity: shares moved by 0.005 shift ELS-FW1 by about 0.0006; the HOL-FI1 terms (carryover, zero error, line loss) are each good to about 0.001 to 0.0015.
- Competing routes, each a different answer and none a reading fork:
  - Readings at face value flags nothing.
  - Treating HOL as 8 per cent span error flags HOL-FW1 at +0.0066.
  - Dropping the two-slots-back share loses GAR-FW1 (+0.0026).
  - Dropping line loss flags HOL-FI1 (+0.0174) and loses CAL-FI1.
  - Omitting the raw-water terms in the share fit biases DUN (a = 0.12, giving a false DUN-FI1 of +0.013); a careful solver includes them.
  - A lab-pairing route cannot resolve 0.005, because 157 of 224 treated results are "<0.030".
- Undefined items that open nothing here:
  - "<0.030": the flag set never uses a treated lab result. All 104 raw grabs are above the limit (minimum 0.071), and these are the only lab values used, for calibration. So how "<0.030" is taken opens no second figure. Treated results at or above the limit (67, two exactly 0.030) are not used either.
  - No data dictionary: the unit and sign are readable from the standard section 3, the register and the quality-code file, and reading_end_utc is defined by the process summary ("measurement at the end of that port's ten minutes").
  - The 00:00 1 January reading (11:00Z 31 December, one per analyser) sits on the quarter edge. Its inclusion moves no offset by 0.0001.

Ask 2, count of treated samples analysed more than 24 h after collection (lims_ammonia_2027Q4.csv).
- Reproduced exactly (Ashcombe 14, Brannock 9, Calderwood 8, Dunmere 12, Elstow 11, Fenwick 13, Garrick 14, Holmedale 11), but only with all three of these:
  - (a) the 16 second-logged 7 December treated bottles removed (same point, analysis stamp, result and release; the second copy has a different sample_no, collected time and received time). The count is the same whichever copy is kept.
  - (b) every analysis stamp moved +60 min. Any shift from 53 to 64 min gives the same counts.
  - (c) the 28 December round counted, collected in the quarter and analysed 5 January.
- Fork 1 (analysis clock): no file states the clock of the "analysed" stamp. The only evidence is that 5 treated results (and some raw) are stamped before reception (down to -53 min) and that release is never within 64 min. That is equally explained by late logging of reception, with the analysis stamps right. Without the shift the answers are 11/6/7/9/8/7/11/10 (Fenwick 7 against 13). A per-round shift only where stamps precede reception gives a third set. The standard (section 6) and the email say nothing about the clock.
- Fork 2 (minor): reading "the quarter's samples" as analysed within the quarter drops the 28 December round, giving 12/7/6/10/9/11/12/9.
- The old-to-new code switch is closed by the email plus the register; the location text names the plant anyway.

Ask 3, fixed-dose hours (nh3_online_readings_2027Q4.csv, process summary, standard).
- Reproduced exactly: 31.2, 27.8, 35.8, 32.2, 26.7, 34.8, 31.3, 29.3. Method: filtered-port readings counted as available to the PLC unless in a run that never reached it; for each gap between consecutive available readings (reading_end basis), hours = gap - 2 h, summed. Gaps are either 1.0 h or at least 4.0 h in every plant, so the 2 h hold and the begin/end convention (fixed from the last good reading + 2 h to the next good reading) never sits near a boundary and is closed by the process summary. No convention fork there.
- Classes in the historian (per plant):
  - Slots filled from the outstation (F row plus G row): historian-only.
  - 17 November, 01:30 to 06:40 NZ, no rows at all: historian-only (the summary's server-fault sentence).
  - Multi-port F runs followed by 3 V check rows: analyser stop, unavailable.
  - Single-port filtered-line F runs (the neighbour ports read normally): unavailable.
  - Multi-port F runs with no check where the port cycle runs on unbroken: counted by the golden as outstation clearing, available.
  - Multi-port F runs with no check where the sequence restarts at RW1 (26-27 October or 4 December, one per plant): counted by the golden as an analyser stop, unavailable.
- Fork (open): nothing in the pack records an outstation restart or a storm-night analyser stop. The partition rests on an unfiled inference (a stop restarts the sequence at the raw port, an unbroken cycle means the analyser ran). The Procedure sheet says a check follows any cleared fault, so a solver using only that evidence gets storm nights as historian-only. Results under the plausible alternatives:

| Reading of the F runs | ASH | BRN | CAL | DUN | ELS | FEN | GAR | HOL |
|---|---|---|---|---|---|---|---|---|
| Golden | 31.2 | 27.8 | 35.8 | 32.2 | 26.7 | 34.8 | 31.3 | 29.3 |
| Storm-night runs historian-only (check-based evidence only) | 26.0 | 22.0 | 32.0 | 28.5 | 21.5 | 28.5 | 26.0 | 23.5 |
| Every unfilled F run unavailable (the quality-code file says F is "No reading") | 34.2 | 30.8 | 38.3 | 34.7 | 28.7 | 36.8 | 32.8 | 32.8 |
| Single filtered-port runs with no check treated as historian-only | 25.7 | 20.8 | 29.3 | 28.7 | 20.2 | 28.8 | 26.8 | 24.3 |

- The golden is the only one of these that uses all the evidence in the data, but it is not the only one licensed by the text.

Cross-batch fingerprint: not run (no other package is readable from this sandbox); no EXACT/TEMPLATE finding raised here.

**Files/Hygiene:** PASS, no stump-affecting or exclusion-level finding.
- 10 files, 4 formats: CSV x5 (readings 106,100 rows, LIMS 328, daily output, rainfall, quality codes), XLSX x2, PDF x2, EML x1.
- Distractors present and unused by the answers: plant_daily_output_2027Q4.csv, catchment_rainfall_daily_2027Q4.csv (storm days 26 October and 3 December), the fixed-dose table and dose gain in the process summary.
- Business-realistic: the LIMS shows mixed date format, old and new codes, duplicate-logged bottles and a "<0.030" convention; the register carries a maintenance log. No tool banner, authoring language or answer-bearing text.
- Temporal: coherent (email of Thursday 28 October 2027 for codes from Monday 1 November; NZDT from 26 September; the 28 December round analysed 5 January, inside the filing window).
- Provenance: all fictional (Fernvale, Kowhai Bay), so there is no public-data contamination.

**Stump power:** High on the main call. The reading-at-face-value, check-standard-only, lab-pairing, one-slot-carryover and no-line-loss routes each produce a specific wrong flag set, and each fails for an analytical reason. The traps are:
- the zero-versus-span split of two analysers that both show 8 per cent low at the 0.1 check (the second level is in the raw grabs);
- the two-slots-back share, which alone decides GAR-FW1;
- the flush-linked line film on the filtered channels, which alone decides CAL-FI1 and HOL-FI1.

All stumps are on the main call and none depends on the forks above. The weakness is in the asks, where a careful solver can miss on a clock or a lineage assumption the files do not pin.

**Stumping type:** `mechanism: statistical_rigor` (identifying a measurement-system model: a memory effect, a zero versus span calibration and a time-varying line loss, from the readings, checks and flush log), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The readings are what the instruments recorded, and no stakeholder figure is overturned. The question asks how far the instruments are from the water, and the answer needs the instrument model, not the finding of a planted defect.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: measurement-system analysis for online water-quality instruments (carryover, calibration, sample-line loss, a standard's offset test).
- Layer 1: UTC readings against NZ quarters, F/G duplicate slots, a historian hole, old and new lab codes, duplicate bottles.
- Layer 2: separating three instrument errors that each shift specific channels across the 0.005 line.
- Easy route: a strong analyst who has cleaned everything and applies the check standard as a gain correction (or fits one-slot carryover) flags HOL-FW1 and drops GAR-FW1 and CAL-FI1, so the flagged list is wrong. This is not data semantics or rule application.

**Fix:** input_files, with the prompt unchanged.
- Ask 2: add to the laboratory email (or a LIMS export footer) a statement of the clock of the "analysed" stamp, for example that analysis times are recorded in New Zealand standard time all year. This files the WHAT and keeps the shift derivable. State that the quarter's samples are those collected in it.
- Ask 3: pin which unfilled F runs reached the PLC. The least leading way is a PLC or outstation event export (analyser stops and restarts, outstation restarts) shipped as an extra file, so the partition is read from a record, not inferred from the port cycle. A sentence in the process summary saying that a reading the analyser produced counts as available whether or not the historian filled it is a lighter pin, but still needs the event record to be decidable.
- Leave the readings, register, checks and the ask 1 golden untouched.
