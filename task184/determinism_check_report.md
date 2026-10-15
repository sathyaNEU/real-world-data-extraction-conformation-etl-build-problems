# Determinism check, task184 (architecture 2)

Two passes, each one isolated thread at medium effort reading only a fresh unzip of `target.zip`, `prompt.txt`,
the submission's graded blocks and the judge's system prompt.

**Pass 1 (2026-10-15): NOT_DETERMINISTIC, SEND_BACK, `underspecified_objective`** on Gates C and E, with Gate G
passing (`method_or_model_selection`, `analytical_non_defect`, no surface-read dependency) and Gate H passing
(domain pass, layers pass, decisive step analytical). Four conventions were unpinned: the season basis of the slot
figures (2026 alone moved Wednesday and Thursday 20:00 from 400 to 450), the class set behind ask 1, the base
behind ask 2's shares, and the treatment of the sensor fault hours in ask 3. The judge put the fix in the prompt,
and that is where it went; the main call, the ladder and the decisive step were untouched. The tasking agreement
also gained clause 4.4, which confines the count to the force's record of the covered offences and forbids any
other offence, source or proxy from placing an offence inside its window, after the leak reader's first pass
weighted the windows by the pedestrian feed and filed a different slate.

**Pass 2 verdict follows, on the rebuilt pack.**

## Pass 2

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no repair required; optional note below on two supplementary readings, no rerun).
- **Why:** Contract 4.1 to 4.4 and the data dictionary fix the population (five Annex B classes, RMS, five register locations, 1 Apr to 30 Sep), forbid any derived time or outside proxy (footfall, premises, trading hours) and leave only the window itself to place an offence, so each offence's window is spread over the slots it touches in proportion to time. That is the only partition of the 12,510 covered offences that uses nothing but the window; the eight heaviest slots are the same under equal split among touched slots, under clipping to the season and under dropping season-straddling windows. The main recommendation (8 slots, 4,100) is forced with a clear margin (8th slot 405, 9th 349).
- **Evidence (recomputed from the bundle, all reproduced):**
  - Covered offences: RMS rows in the 5 classes with HG-L01..L05 (Cranstoun CR-* excluded): 25,020 over two seasons, 12,510 a season. Reproduced. 87.4 per cent of windows exceed 4 h (mean 12.6 h). Reproduced.
  - Proportional slot grid (per season): Sat 20-00 668.8, Fri 20-00 628.6, Sun 00-04 570.1, Sat 00-04 530.9, Sun 04-08 441.1, Thu 20-00 420.4, Wed 20-00 417.4, Sat 04-08 405.3; ninth Sun 20-00 348.5. Eight sum 4,082.7, rounds to 4,100. Matches golden figures and set, and the 42-slot grid matches the golden workbook rows. Minimum slot about 150, maximum about 650. Reproduced.
  - Wrong-method sets scored on the grid: earliest 3,329 (golden 3,350), midpoint 2,735 (golden 2,750), latest-time set 2,370 (golden 2,400 is from reported_at, narrative only, not a graded figure; not rechecked).
  - Rounding edge: Fri 20-00 is 628.6 against the 625 line (clipping and dropping windows leave every slot's rounding unchanged except Wed 20-00 417 vs 428 under season clipping; the set and total stay). The total 4,076.6 to 4,083 stays at 4,100.
  - Class counts: five covered classes reproduce the golden to the nearest ten. The four other classes reproduce only on the union of CIS and RMS with the 354 fortnight duplicates matched one-to-one on class, normalised address and occurrence time: Assault 2025 1,147 (1,150), Public order 1,413 (1,410), Shoplifting 2,173 (2,170), Theft from the person 757 (760), 2026 1,221/1,501/2,307/803 (1,220/1,500/2,310/800). Reproduced.
  - Location shares (all nine classes, union, 5 locations): 35.41/13.50/20.27/21.33/9.49 for 2025 and 36.42/13.79/18.99/20.78/10.02 for 2026. Reproduced.
  - Footfall per trading hour (UTC+1 to local, trading hours with the Saturday close at 05:00 Sunday and Friday 03:00 Saturday spillover, fault periods excluded): FG-01 1,321/1,380, FG-02 858/900, FG-04 599/619, FG-07 480/500. Reproduced; insensitive to fault_to inclusive or exclusive and to a one-hour shift of the fault window.
  - Surviving forks (none touches the main call): (1) Assault without injury 2025 reads 1,140 if the extract is assembled by migration date (CIS to 27 July, RMS from 28 July, 1,144) instead of the matched union (1,147, golden 1,150). (2) Footfall without removing the listed sensor faults gives FG-01 1,270/1,350 and others 5 to 7 per cent lower; a reading that keeps readings the register records as not counting is not defensible for what a location "saw". (3) Any-touch counting (15,011 across the eight, more than the 12,510 offences) and contained-only counting (about 294, which rounds to 0 or 50 per slot) cannot give the totals the prompt asks for, so neither is a competing answer to the main call.
- **Files/Hygiene:** PASS. 16 files; formats csv, md, pdf (2), xlsx; two files over 25,000 rows (RMS extract 33,700, footfall 35,136). Distractors present and unused by the solution: patrol_plan_2026.xlsx, footfall feed, licensed premises, trading hours (trading hours used only for the workbook footfall figure), beat map. No authoring or benchmark language, no solver-facing text, dates consistent with a 22 Jan 2027 extract and a 4 Dec 2026 signature. No answer-ranking artifact in any shipped file. No exclusion-level finding.
- **Stump power:** Moderate to high. Earliest time (the first field a capable analyst reaches for), midpoint or latest time all give a complete, plausible-looking slate that meets 2,400 to 3,350 against 4,100; the dictionary and contract 4.4 push away from single-time placement but do not state the apportionment, so a model has to choose it. The CIS/RMS union and the sensor-fault exclusion add ask-level difficulty.
- **Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Interval-censored occurrence times handled by apportioning each window over the slots it spans (aoristic analysis); no reported number is wrong and the stump survives on perfectly clean data.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: crime analysis, aoristic apportionment of offences with unknown times to patrol slots is the field's own estimate (swap "megawatt-hours" or "visits" in and the interval-censoring problem disappears). Layer 1: two recording systems with overlapping fortnight, per-victim shoplifting change, alternative street names, Cranstoun length of the street, UTC feed, sensor fault periods, spill-over trading hours. Layer 2: placing offences with window-only times. Easy route: take occurred_from (or midpoint) after cleaning everything correctly, which files a different eight (for example five evenings and three late afternoons, 3,350 against 4,100).
- **Fix:** none. Optional, no rerun: none of the forks above needs a pin; if the author wants the Assault 2025 figure and the footfall figures safer, state in the prompt that the extract is the union of both files and that sensor fault periods are excluded.

## After the verdict

Two things changed after pass 2 read the bundle, neither of them a graded figure:

- The 2026 patrol plan, a declared distractor, was rewritten from a mostly empty grid into the monthly return
  clause 5.1 of that season's agreement called for (hours worked, slots stood down and why), because the leak
  reader read the old sheet as a stub.
- One sentence of prose in the tasking paper, and `verify.py` gained the assertion that the migration-date route
  through the two exports gives the same class counts as the matched union, offence for offence, which closes the
  first fork the verdict lists (the pack's own resolution leaves no difference).
- The generator now holds every occurrence window inside its own season, so the second residual the verdict
  names, Wednesday 20:00 reading 417 or 428 depending on whether windows are clipped to the season, cannot arise:
  there are no season-straddling windows to clip. The figures moved with that change and the draw was re-fixed so
  all 43 call figures sit mid-bin again; every free gate was re-run green.
