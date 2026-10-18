# task201 determinism judge report

**Order kept:** yes. My own derivation was computed from the pack alone and saved to
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task201_derivation.md`
before `task201_graded_blocks.md` was opened. My independent answer was
**ZAN / Zanowiec Miasto / SN-magistrala, 102,124 customer-interruptions, runner-up PUS**; the
committed answer is **GRB / Borowa Puszcza / SN-odgalezienie, 7,152, runner-up ZAN**.

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK (the fork lives in the governing document, so the repair changes what
  solvers see; a rerun is required)
- **Taxonomy:** underspecified_objective (with solution_incorrect on supplementary 2 and 3)
- **Fix location:** input_files (PR-07 section 3), plus solution regeneration for answers 9, 10, 11

## Why

The whole call turns on a step no shipped sentence requires or specifies: re-timing the start of
every interruption that SD-OMS timed from the first customer notification rather than from a line
device. PR-07 section 3 says the basis is "odbiorco-godziny ... odbiorcy ... pomnozeni przez liczbe
godzin, w ktorych byli bez zasilania" and anchors inclusion on "ktorej poczatek przypada w oknie
analizy"; `slownik_danych.md` only *describes* the mixed clock ("Dla linii objetej telemetria linii
przyjmowany jest znacznik operacji urzadzenia liniowego ...; dla pozostalych linii przyjmowany jest
czas przyjecia pierwszego zgloszenia klienta"). Nothing states that the start must be corrected, and
nothing states the estimator. Equally licensed estimators give three different leaves, so the
recommendation is not forced.

## Gate table

| Gate | Result | The number or quotation that decides it |
|---|---|---|
| **H** | pass on H1/H2, H3 analytical but see Gate G | domain: pass, layers: pass, decisive_step: analytical. Full line below. |
| **G** | **FAIL, banned_stumping_type** | The misleading reported read is SD-OMS `czas_trwania_min` / `poczatek_lokalny`: 4,940 of 6,005 interruptions are timed from the first customer call, so the recorded customer-hours understate 82% of events and the task is won by flipping away from them. `mechanism: planted_defect_flip (mixed measurement clock)`, `stumping_family: surface_read_rejection`, `surface_read_dependency: yes`, `sole_data_defect: yes`. |
| **A** | **FAIL** | The main path reproduces exactly (6,005 selected; 1,065 timed / 4,940 untimed under "flag OR SN-magistrala"; class intervals 8.636 / 16.9918 / 164.6443 / 242.5032 min; GRB 270.8k vs ZAN 206.9k vs PUS 182.5k vs NIE 148.7k; lead 1.309x; 7,152). Three committed figures do not: answer 9 (**3,400** is the count of distinct `nr_ppe`, not of notifications; the shipped notification count with an empty `id_zdarzenia` is **3,542**, and every one of the 12 branch x channel cells differs, e.g. ZAN telefon 458 not 432); answer 10 (216,840 / 99,527 / 53,061 / 30,657 is a per-notification sum over the PPE-deduplicated set, i.e. one device's customers counted once per PPE; the customers behind the *distinct devices named* are ZAN 193,228, PUS 79,713, NIE 47,192, GRB 27,096, and the per-notification sum over all 3,542 is ZAN 226,024); answer 11 (**+0.6 min / +15.7%** SN and **+0.3 / +11.0%** nN appear nowhere: the shipped correction in `sprawozdanie_URE_2026_wstepne_i_korekta.xlsx` is SN 3.93 -> 4.35 = **+0.42 min, +10.687%** and nN 2.40 -> 2.55 = **+0.15 min, exactly 6.2500%**, and I searched 100+ clock-restatement variants, the closest being +0.659 / 16.7% and +0.474 / 16.0%). Also wrong in the recommendation prose: "Nierzyca leads on the pack as it stands" - with planned switching left in, ZAN leads at 29.90% against NIE 26.99%; NIE leads only on planned outages taken alone (56.3%). |
| **B** | **FAIL** | The decisive rule is in no shipped file. PR-07 section 3 never says the recorded start may or must be replaced, no file states a pre-notification interval, and the committed reasoning's own vocabulary ("pre-notification interval") returns zero hits across all 16 members. Read literally, the pack's procedure executes on the recorded `poczatek`/`czas_trwania_min` and selects ZAN. |
| **C** | **FAIL** | Four equally licensed operationalizations of "hours without supply", three leaves: recorded clock -> **ZAN / Zanowiec Miasto / SN-magistrala** (31.94 / 24.04 / 22.23 / 21.78); conform everything down to the notification clock, using only shipped timestamps -> **ZAN** again (29.56 / 26.03 / 22.61 / 21.79); one pooled mean interval of 101.84 min -> **PUS / Dolna Wierzba / SN/nN-stacja** (PUS 33.92); interval stratified by section class -> **GRB / Borowa Puszcza / SN-odgalezienie** (GRB 33.48). A pooled *median* of 22 min returns ZAN. The committed block argues the pooled variant away ("the station sections carrying its untimed interruptions stand at 17.0 minutes"), which is the author's reasoning, not a shipped rule. The "timed" set is itself unpinned: the registry flag alone gives 961 events, flag-or-SN-magistrala 1,065 (the golden), membership of the SCADA archive 1,150, and under the last the SN/nN-stacja interval is 13.8 min, not 17.0. Supplementary forks: 85 jobs / 57.95 h at job level against 88 records / 58.68 h at section level; "the customer-hours those jobs account for" as the whole outage (NIE 15,275.2 / PUS 11,465.3 / ZAN 6,669.0 / GRB 2,251.1, which the golden takes) against the overrun portion only (2,968.9 / 2,570.8 / 1,091.8 / 523.1); and answer 11's nN percentage sitting exactly on 6.2500%, so one decimal is 6.3 half-up and 6.2 under Python's `round`. |
| **D** | **FAIL** | The divergence between ZAN and GRB is a reading of whether PR-07 section 3 licenses re-timing, and then a free choice of estimator, not a difference in analysis. Gate F's own words: solvers who do everything right split on interpretation, which is never credited as a stump. |
| **E** | **FAIL** | The prompt pins which decision ("Which branch, district and section class takes this season's one remediation crew-week") but not the measurement basis, and three supplementary asks are loose: "the customer-hours those jobs account for" (whole outage or overrun), "the customers behind the devices they name" (distinct devices or per notification), "October 2026's correction" (the workbook's correction, which is what it plainly reads as, or a restatement). |
| **F** | High but invalid | The record clock is a genuine trap: every Layer-1 shortcut I tried (concatenating both exports without dedup -> ZAN 32.18; joining device ids raw and losing 2,823 of 6,448 rows -> ZAN 38.68; leaving planned outages in -> ZAN 29.90; carrying the three open events to the pull time -> ZAN 31.90) lands the recorded-clock leaf, so a strong model does fail. It fails on an unpinned operationalization, which Gate F forbids crediting. |

## Gate G line, in full

`mechanism: planted_defect_flip (mixed measurement clock)`, `stumping_family: surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`. Banned scaffold: the primary stumping
strategy is catching that a misleading reported read, SD-OMS's own interruption start and duration,
is wrong and flipping away from it, and that shape is retired for tasks on or after 8/16 no matter
how many corrections it takes. The misleading read is `poczatek_lokalny` / `czas_trwania_min` on the
4,940 interruptions timed only by the first customer call. On clean data (one uniform clock) the task
collapses into executing PR-07 section 4's drill, so it does not survive the clean-data test. Rebuild
the difficulty where the reported numbers are FINE: a binding constraint on honest customer-hours (one
crew-week against section lengths or material), a decomposition of a correctly reported movement
across the two storm episodes, or a forward projection of the remaining season the trailing six weeks
do not pin.

## Gate H line, in full

`domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is the field's own:
interrupted customer-hours behind the operating device, the SAIDI/SAIFI numerator, with the detection
lag that unmonitored feeders carry, and the swap test does not survive the substitution. Layer 1 is
real and strong: two overlapping SD-OMS exports with renamed columns, 2,823 legacy unpadded device
ids, SCADA in UTC against local time, IVR rows with no branch or device, a re-issued outage schedule,
hours in the 2024 report against minutes in 2025, preliminary against corrected regulatory data.
Layer 2 is the measurement-clock conformation. The easy route a strong analyst who cleaned everything
and read every field correctly would take is to compute on the recorded durations, which gives ZAN /
Zanowiec Miasto / SN-magistrala, so H3 reads analytical on its own test; but the same step is what
Gate G bans and what Gate C leaves open, so the disposition stands at SEND_BACK.

## Files / Hygiene: PASS (two FIX_NOW notes, nothing exclusion-level)

16 members, 4 formats (csv, xlsx, pdf, md), largest file 55,270 rows, three genuine distractors
(`rejestr_zgloszen_jakosci_energii.csv`, `wycinka_i_przeglady_linii_2026.csv`,
`sprawozdanie_niezawodnosc_2024_2025.pdf`), no README or authoring disclosure, no benchmark language,
no LLM tells, timeline coherent (pull 2026-11-16 06:00; latest restoration 2026-11-16 02:02).
Two internal contradictions to fix in house: `provenance.md` says the schedule holds "440 prac
planowanych" while the sheets hold 260 jobs covering 440 section outages; `slownik_danych.md` says IVR
dropped branch and device "od 9 do 19 pazdziernika 2026" while the blanks actually run 2026-10-09 to
2026-11-02 (3,777 IVR rows, and 348 of the 569 rows that supplementary 2 has to repair fall outside
the stated window).

## Fix

1. `input_files`, PR-07 section 3: state the measurement basis for the start of an interruption, at
   the level of the estimand rather than the recipe, e.g. that the hours without supply are counted
   from loss of supply and that an interruption not timed by a line device is corrected to it. Then
   rebuild the pack so the leaf is invariant across every licensed estimator of that correction: as
   shipped, stratified-by-class gives GRB, one pooled mean gives PUS and one pooled median gives ZAN.
   Closing the fork by naming the estimator in the document would make the decisive step rule
   application, so the margins have to carry it instead.
2. `prompt`: pin the three loose asks (whole-outage or overrun customer-hours; distinct devices or per
   notification; the workbook's correction) and give a tie-break for a percentage that lands on a half,
   since the nN figure is exactly 6.2500%.
3. `solution`: regenerate answers 9, 10 and 11. The literal figures are 3,542 notifications (ZAN
   400/427/458, PUS 228/273/274, GRB 220/311/276, NIE 187/236/252 as IVR/app/phone), customers behind
   the distinct devices named ZAN 193,228 / PUS 79,713 / NIE 47,192 / GRB 27,096, and the October
   correction SN +0.42 min (+10.7%), nN +0.15 min (+6.3%).
