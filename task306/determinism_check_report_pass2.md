# Determinism verdict, task306 r2

- **Verdict:** DETERMINISTIC, with one fork closed only by inference (survival conditioning, see Q1). No SOLUTION_WRONG: every committed figure reproduced.
- **Disposition:** APPROVE. Optional hardening, not required: one sentence in tooling_plan_2027_draft.docx s.3 filing the population as "the packs the cars carry on the day, alive on that day" would close the fork in text, but it changes what solvers see and needs a rerun.
- **Why:** The docx s.3 fixes population, warranty clock (date of first admission, replacement does not restart), failure window (failures in 2027 after the OEM period ended), one pack per car, no exits, straight-line curves, and the arrivals from 1 Jul 2026 to end 2027. Under that reading the golden reproduces: 3,438 on the register plus 364 imports gives 3,802, which rounds to 3,800, and the split is 1450/900/350/250/50. The one thing the text does not say is that a pack carried on 30 June 2026 is conditioned on having survived to then. The data force it: the Mira curve reaches 1.0000 at age 13, so an unconditional share would give a surviving 13-year-old Mira pack zero chance of failing. Gates A to E pass.

## Evidence (recomputed from target/)
| Value | Golden | Recomputed | Source |
|---|---|---|---|
| Register-only 2027 failures | 3,448 | 3,438 (365.25-day year), the same family as the golden within about 10 | rdw csv + accuvervangingen + curves + docx s.3 |
| Imports still to arrive | 363 (Mira 360) | 364 (Mira 361) | rdw csv, trailing 12 months, arrivals 1 Jul 26 to 31 Dec 27 |
| Total | 3,800 | 3,802, which rounds to 3,800 | |
| Mira imports, 12 months to 30 Jun 26 | 1,394 at 8.1 years | 1,394 at 8.09 years | datum_eerste_tenaamstelling_in_nederland greater than datum_eerste_toelating |
| Slots | 1450/900/350/250/50 | 1450/900/350/250/50 | largest remainder; remainders Mira 0.79, Plover 0.70, Tern 0.42 |
| Modules per lot of 50 | 167/274/190/149/224 (Volta, Kestrel, Plover, Mira, Tern) | reproduced only after capping each supplier lot's issues at its receipts | mutaties, ontvangsten, artikelstam (Kestrel carrier = 2 modules), verzendingen |
| First-EOL pass share | 92.6/88.2/94.0/88.3/90.5 | reproduced (VH/KS/PS/MC/TV) | eol_testlog mapped to work order through mes_bms_koppelingen, first non-ABORT run, start in window |
| Core intake reject share | 8.9/5.9/11.0/14.7/8.3 | reproduced | kernen_inname with AFGEKEURD cores that appear in mes_werkorders removed |

Plain reading of the three ask-side items gives different numbers:
- Naive net issues per shipped pack gives 171/283/195/150/238. The golden needs the per-lot cap: the over-issued small lots (e.g. MC2509-05 receipt 8, issued 20, as 6+6+6+1+1 on one pick list) lose the repeated lines. The text signals this only through "no lot's stock goes below zero" and "one list can serve several work orders". The result is forced by stock conservation, but by inference.
- The raw `keuring` share gives 10.1/17.6/13.2/12.5/12.6. The 99 AFGEKEURD cores that sit on a work order were accepted at intake and scrapped later. The README says `keuring` is the grade on 1 July 2026, which is the hint.
- Counting an ABORT as the first run gives 85.4/85.9/91.4/90.5/91.4.
- Grouping runs by pakket_id instead of work order gives 92.3/87.2/94.2/88.0/91.3. Replaced BMS serials split a pack's history.
Each has its closing fact in the README or the data, so I count them as closed, though none is spelled out as a rule.

## Q1 (Gates C and D): projection variants
I ran 40 variants. Each was run end to end: register plus simulated arrivals, then largest-remainder lots.
- Dimensions crossed: conditioning (none / on survival to 30 Jun 2026 or to registration / on survival to window start) x warranty-window treatment (pro-rata by day, whole-car at 1 Jan, at 1 Jul, at 31 Dec) x year length (365.25 / 365).
- One-at-a-time variants on top: ignore replacements; warranty from the Dutch registration date; arrival rate from 6 / 24 months or a linear trend; pack origin for imports; arrivals for 2027 only (12 months).
- **Span of all 40:** total 1,532 to 5,732; Mira 281 to 3,248. The extremes are the two misreadings (warranty from the Dutch registration date, and ignoring the replacement log).
- **Conditional on survival, daily pro-rata (the golden family), 8 variants** (year length, 6 / 24-month and trend arrival rates, imports' pack origin, 12-month arrival window): total 3,681 to 3,810, Mira 1,706 to 1,834. The slot split matches the golden in 7 of 8 and the total rounds to 3,800 in 7 of 8. The exception is arrivals counted for 2027 only, which the docx excludes ("from 1 July 2026 to the end of 2027"): 3,700 and Mira 1,400 / Volta 950. With the 1 Jul whole-car cut-off the result is also unchanged (3,787 to 3,795, same split).
- **Flips in that family:** whole-car classification at 1 Jan 2027 gives about 3,555 and Mira 1,550 / Plover 300 / Kestrel 200; at 31 Dec gives about 4,000 and Mira 1,350 / Kestrel 300 / Tern 100. The docx counts failures by date ("a pack fails in 2027 ... and the OEM's pack warranty has ended"), so pro-rata is the literal reading and these two are not equal alternatives.
- **Unconditional F(b)-F(a), the only serious literal competitor (16 variants):** total 1,532 to 3,019 (2,494 to 2,899 on the sound population definitions), Mira 281 to 1,193. The usual split is Mira 1300 / Volta 900 / Plover 400 / Kestrel 300 / Tern 100, so it differs from the golden. The golden's 1450/900/350/250/50 appears only by coincidence in its whole-car-at-1-Jan variants.
- **Conditioned on survival to window start (8 variants):** about 4,100 to 4,570, Mira about 2,270; the split is always different. This is the wrong estimand: failures in Jul to Dec 2026 are not counted, since the replacement pack is left out by the docx.
- **Thresholds:** the total to the nearest hundred holds at 3,800 only under survival conditioning with pro-rata or 1 Jul cut-off. The Mira city car figure is stable (1,820 to 1,834) across rate method, year length and pack origin. The Plover-over-Tern third-remainder call (0.70 vs 0.42) never changed within the family.
- **Reading:** Gate C survives only if conditioning on survival is accepted as forced. By the brief's strict rule this counts as a fork closed by inference. I rule it forced, not open, because the data contradict the unconditional reading (Mira cdf equals 1 from age 13, and the register holds surviving original Mira packs older than that). Residual risk is real: the text never says "alive".

## Q2 (Gates F and H): what decides the answer
- **Deciding material:** docx s.3 sets the population and the dating rules: "The cars in use ... are those on the register on 30 June 2026 and those first registered here from 1 July 2026 to the end of 2027". The load-bearing analysis is not stated: (a) condition each carried pack's curve on having survived to 30 June 2026, and (b) estimate the post-snapshot used-import stream (rate and age profile) from the register's own `datum_eerste_tenaamstelling_in_nederland` versus `datum_eerste_toelating`. The Mira city car's 5-year warranty (garantievoorwaarden pdf, s.1) means its imports (about 8.1 years old) fail at once, and they carry 360 of the 1,829 Mira failures.
- **Easy route:** a strong analyst who cleaned the data and applied every stated rule, but took F(b)-F(a), would file about 2,700 with Mira 1,300 / Plover 400 / Kestrel 300 / Tern 100, wrong on three platforms. One who stopped at the register would file Mira 1,250 / Volta 1,000 / Kestrel 300 / Tern 100. So the call is not reachable by reading fields and applying rules alone: the survival conditioning and the arrival model are judgement the data settle. The docx closes a great deal, so the residual analytical content is thin but real.
- **Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is life-curve survival with left truncation, plus forecasting an arrival stream. Layer 1 mess is the replacement log (abroad and Voltwerk rows, multiple per car), name variants in `handelsbenaming`, and the BMS-serial reuse; Layer 2 is the conditional-survival estimand and the import stream.
- **mechanism:** forecasting. **stumping_family:** method/estimand selection on correctly read data. **surface_read_dependency:** no (nothing shipped ranks the candidates). **sole_data_defect:** no.

## Cross-batch, Files/Hygiene
PASS. 18 files; formats csv, xlsx, pdf, docx, md (5); rdw csv has 88,128 rows (over 25,000). Unused-but-relevant distractors: prijslijst pdf, module_levertijden xlsx, afvoer_recycler xlsx. No authoring language found in the files read. `lijn_exports_toelichting.md` is an in-fiction README. Dates are coherent (exports 1 Jul 2026, docx dated 14 Aug 2026 for a 2 Sep meeting). The RDW extract is synthetic in the make names. No exclusion-level finding. I did not run a cross-batch fingerprint (no other tasks readable).

## Stump power (Gate F)
Plausible stump: the survival-conditioning and post-snapshot Mira imports step. A solver who files the unconditional share gets 2,700 and a different split; one who stops at the register misses the Mira import stream. Possible too-easy signal: the docx specifies nearly every convention, so the careful solver only has to recognise conditioning.

## Stumping type (Gate G)
`mechanism: forecasting`, `stumping_family: method/estimand selection`, `surface_read_dependency: no`, `sole_data_defect: no`. Passes: no reported number is rejected; the difficulty is the estimand and the arrival model on correctly read data.

## Fix
none (prompt or input_files only if the author wants the survivor conditioning filed in words: add to docx s.3 that "the share that fails in a year is of the packs still on the car at the start of it").
