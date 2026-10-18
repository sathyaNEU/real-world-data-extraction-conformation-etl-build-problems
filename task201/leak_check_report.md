# leak check, task201

**Verdict: REVIEW.** 16 files read, 42 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: interval, recorded, decisive, zanowiec, golden, subset, nothing, pooled, register, overlap, supply, device, grabownik, spends, window, default, interrupted, quantity, absence, notification, opening, duration, telemetry, dispatch, population

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Also tell me whether any planned job ran past its published slot and if so how many and the hours over in total, with the customer-hours those jobs account for per branch; how many notifications match no interruption rec'

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read, preserved from the 2026-10-18 pass

`leak.py` rewrites this file on every run, so the reader's read below was carried forward by hand
after the world-level repair pass re-ran the sweeps. It was taken on the architecture 6 pack, before
the repair, by one isolated reader (Sonnet at medium effort) on a fresh unzip of the pack and the
prompt alone. No reader has run on the repaired pack: the documents and the telemetry archive changed,
so the reader has to run again at stage 4.

# task201 reader answers

1. Decisive step: no sentence states it. Nearest is slownik_danych.md, ts_poczatek row: "Dla linii objetej telemetria linii przyjmowany jest znacznik operacji urzadzenia liniowego z archiwum telemetrii; dla pozostalych linii przyjmowany jest czas przyjecia pierwszego zgloszenia klienta." That sentence shows the start time has two bases, but nothing says to correct for it. Supporting: provenance.md "Archiwum telemetrii obejmuje tylko urzadzenia transmitujace do SCADA".
2. Ranking file: none. PR-07 gives the procedure, not a ranking. Nothing shipped ranks the branches.
3. Exists only to help: slownik_danych.md (also provenance.md). Distractors that look unused: sprawozdanie_niezawodnosc_2024_2025.pdf, rejestr_zgloszen_jakosci_energii.csv, wycinka_i_przeglady_linii_2026.csv, notatka_sluzby_dyspozytorskiej.md.
4. Reads as the answer: none outright. The dispatcher note hints at Grabownik ("Dojazdy w Grabowniku byly najdluzsze", "drogi lesne w Borowej Puszczy"), but only as context.
5. procedura_PR-07, section 3: "Podstawa przypisania slotu sa odbiorco-godziny przerw w oknie analizy." with section 4 "oddzial o najwiekszym udziale ... rejon ... klasa". Read literally on the OMS timestamps (both OMS files merged, overlap de-duplicated, device ids de-zero-padded, register customers, awaryjne with restoration, start 1 Oct to 15 Nov): ZAN 205,993.8 customer-hours (32%), Zanowiec Miasto 48%, SN-magistrala 68%, 102,124 customer-interruptions in that class and district.
6. An analytical choice. The OMS start is the telemetry stamp on telemetry lines (94% of ZAN events, 4% of PUS, 8% of GRB) and the first customer report elsewhere. Detection lag measured on telemetry events is about 239 min for SN-odgalezienie, 161 for nN-obwod, 10 for stations and about 0 for magistrala, so durations on non-telemetry branches are understated. A second, smaller point: on telemetry lines the OMS start equals UTC+1 even before 25 Oct (CEST), which overstates those durations by 1 h. Deciding sentence: the slownik ts_poczatek row above plus the telemetry file itself.

## Solver answer (confidence about 60%)
Slot: GRB (Grabownik), district Borowa Puszcza, class SN-odgalezienie, carrying 7,152 customer-interruptions (926 unplanned interruptions, about 71% of the district's lag-corrected customer-hours). Runner-up branch: PUS, about 23.3% against 36.2% for GRB.
Route:
- Merged the OMS files and removed the overlap (identical rows).
- De-padded device ids, joined the register, kept awaryjne with restoration and start in 1 Oct to 15 Nov: 6,005 events, 542,666 customer-interruptions.
- Found that OMS start differs by line type. Estimated lag by class from telemetry events (first linked report minus true local telemetry time) and added it to non-telemetry events. Also moved telemetry-line starts before 25 Oct forward by 1 h.
- The naive shares give ZAN, Zanowiec Miasto, SN-magistrala. The corrected shares give GRB 36.2, PUS 23.3, ZAN 20.7, NIE 19.9. Borowa Puszcza 40.0%, SN-odgalezienie 70.7%. The result is stable across mean or median lag and per-episode lag (GRB 35-36%, Borowa Puszcza about 40%, SN-odgalezienie about 71%).
- Runner-up is the least stable: PUS in most variants, but NIE or ZAN come close in some.
Other figures (lower confidence on definitions):
- Unplanned interruptions and customer-interruptions per level (GRB 4,694 / 53,268; NIE 450 / 125,948; PUS 560 / 139,433; ZAN 301 / 224,017). Borowa Puszcza 1,136 / 11,148. Class counts in Borowa Puszcza: magistrala 2 / 1,058, odgalezienie 926 / 7,152, stacja 7 / 387, nN 201 / 2,551.
- Planned overruns against the latest release (November wydanie 2 replaces wydanie 1): 85 jobs ran past the slot, 57.9 h over in total (88 events, 58.7 h). Over-slot customer-hours per branch: GRB 523.1, NIE 2,968.9, PUS 2,570.8, ZAN 1,091.8.
- Notifications with no id_zdarzenia: 3,542. IVR for 9-19 Oct has blank branch, so I resolved it through odbiorcy_ppe. Branch by channel (IVR / app / phone): GRB 220/311/276, NIE 187/236/252, PUS 228/273/274, ZAN 400/427/458. Customers behind distinct named devices: GRB 27,096, NIE 47,192, PUS 79,713, ZAN 193,228.
- October correction (korekta_1 minus wstepne, unplanned minutes): SN 4.35 - 3.93 = +0.4 min (10.7%), nN 2.55 - 2.40 = +0.2 min (6.3%; 6.25 exactly).
Uncertainties: whether the intended method adds estimated lag, whether the DST fix is intended, and how overrun and the "customers behind devices" are defined.

## Reads as written for an exercise
- procedura_PR-07_plan_remediacji.pdf: "Slot niewykorzystany nie przechodzi na sezon nastepny." and the three-step table. A real procedure would not spell out a share-of-parent tree and demand "oddzial drugi w kolejnosci" in the note; this is the prompt's request restated.
- procedura_PR-07, section 3: "Wylaczenia planowane, przerwy bez zapisanego zalaczenia oraz przerwy w sieci innych operatorow nie wchodza do pomiaru." This tidily pre-defines every exclusion the solver needs.
- sprawozdanie_URE_2026_wstepne_i_korekta.xlsx: sheet "wydania" note "korekta pazdziernika po zamknieciu zdarzen; zastepuje dane wstepne" and the unit-less 3.93/4.35 figures. They are far too small for monthly minutes per customer, when 2025 SAIDI was 171 min a year.
- slownik_danych.md: the line "Dokumenty ... opisuja sie same i nie maja tu wpisow." and the very clean ts_poczatek definition with both start bases.
- notatka_sluzby_dyspozytorskiej.md: "4245 wylaczen awaryjnych" matches the data count exactly. Real notes rarely match a system count to the unit.
- provenance.md: counts equal to the row count of every file, with a "Czego nie zawiera" column.
- harmonogram: every planned event starts at exactly window start + 20 min, and nearly every outage in a set carries the same cause text "prace planowane".

### The main thread's ruling, line by line

- **Question 1, no leak, and the reader says so itself.** The dictionary's `ts_poczatek` row states that the
  start comes from the line device where the feeder has telemetry and from the first customer notification
  otherwise. That is the honest description of a column and it has to ship, because the estimand is about
  when supply was lost. Nothing in the pack says to correct for the difference, name the telemetered subset
  as a measurement of it, or say it varies by class.
- **Questions 2, 3 and 4.** No file ranks the branches. The dictionary and the provenance note are the
  pack's own documentation rather than help, and the four files the reader calls distractors are the two
  declared distractors plus two documents the asks consume.
- **Question 5 executes to the default path, not to the golden**, which is the right answer for this build:
  the procedure's own basis read literally on the recorded timestamps gives Zanowiec, 205,993.8
  customer-hours, which is the default path's wrong answer to within rounding.
- **The solver answer landed the leaf at about 60 per cent**, by measuring the detection lag on the
  telemetered subset and adding it back by class. That is the decisive step, so Gate F is a live question
  here as it was on task190. It is weaker than task190's landing in one way that matters: the reader's
  runner-up is wrong and it says so itself, calling that the least stable part of its answer, and the
  runner-up and the shares are graded.
- **A real defect the reader found, verified here before anything was commissioned.** The reader moved the
  pre-25-October telemetry starts by an hour and was right to. Poland leaves summer time on 25 October 2026,
  so a UTC export and a local-time operational record differ by two hours before that date and one hour
  after. The pack uses a flat one hour throughout: `checks.py` R2.utc_offset asserts the local stamp equals
  the UTC stamp plus one hour for 99 per cent of rows, and 366 of the 1,505 telemetry stamps fall before the
  change. So a quarter of the file is an hour out, every duration built from it in that period is an hour
  short, and a solver who notices has a defensible second reading. A transition inside the window is good
  Layer 1 mess, but it has to be the real transition rather than a flat offset. This goes into the repair
  pass with whatever the judge returns.

### What the world-level repair pass closed, of the lines above

- The clock: the archive is now written at the offset that applied (+02:00 to 01:00 UTC on 25 October 2026,
  +01:00 after), `checks.py` R2 checks both regimes against the tz database and fails a flat hour, and
  `verify.py` repeats the check from the bundle alone.
- The procedure: rewritten without the exam-style step table, without the demand for the runner-up, and
  with the exclusions carried as operational clauses rather than a tidy pre-definition.
- The returns: the value columns name their index and unit, the interruption index is per customer rather
  than per thousand, and the prior-year report's annual level now matches the window's own daily rate.
- The dictionary's IVR window, the provenance's planned count and its row-count manifest, the dispatch
  note's exact system count, and the schedule's constant lead-in and single cause: all fixed, each with an
  assertion.
- Still open and not this pass's: the reader's own landing of the leaf at about 60 per cent (Gate F), which
  belongs to whatever architecture follows.
