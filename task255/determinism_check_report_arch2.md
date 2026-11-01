# task255 determinism check, architecture 2 (spent)

Two isolated judge passes on the metro reach architecture. Round 1 forced the main call and failed asks and reach cells on Gates A and C (a generator repair); round 2 failed Gate G (planted_defect_flip, surface_read_rejection) and Gate H3 (the peak through-running written in no file) and could not reproduce three reach figures. Architecture 2 was spent on round 2 and the slot re-rooted.

---

# Determinism check, round 1 (2026-11-01): NOT_DETERMINISTIC, SEND_BACK as labelled; order kept; main call forced; Gate G and Gate H pass (each marked borderline)

Read against the gate table the failing gates are A and C on the reach cells and on asks 3 and 4 (the re-cabling instant, the shared-position replacements, three reach figures by the per-journey duration test), a generator repair that spends no architecture. Isolated thread, Sonnet at medium effort, on target.zip 23cb43ec.

# Verdict, task255 r1 (Spoorbeeld Tier G 2027)

Order kept: yes. derivation.md was written to disk before graded_blocks.md was opened. My first derivation took the line map literally (changes at Centraal wherever lines meet) and put CEN and BNS in Tier G; I found the through-running regime only afterwards, while testing the golden's claim against the ride timestamps (see Evidence).

- **Verdict:** NOT_DETERMINISTIC (the main call is forced; supplementary answers 2, 3 and 4 are not, see Why).
- **Disposition:** SEND_BACK. The forks sit in what solvers see (register, re-cabling dates, reach cells), so closing them changes the pack or the asks and needs a model rerun.
- **Why:** Main recommendation (Tier G = Overstappunten, Zuidtak, Oosttak) is forced once the rider-level data are read: journeys between the north and east branches, and between west and south, on weekday peaks run through Centraal with no change, so CEN-OV is not passed. Every tier survives all route and classification variants I tried (CEN 31 to 33, BNS 32 to 33, OVP 47.7 to 49.3, ZDT 48.2 to 48.6, OST 46.8, EIN 35.8 against the 40 line). But three committed answers are not uniquely forced: supp 2 (several whole-per-cent reach cells), supp 3 (make-good hours, two licensed sources for the re-cabling instant), supp 4 (screens on sale, position versus tag). Gates failed: C (supp 3, supp 4), A/C (supp 2). Governing label: competing_defensible_answer.

## Evidence (recomputed from target/)
| Item | Golden | My value (file, field) | Reproduced |
|---|---|---|---|
| Regular riders | 1,949 | 1,949 (rides csv, card_class from productcodes, 4 Mon-Sun weeks by travel_date) | yes |
| Gate to hall | old+new codes | Gates sheet, 0 mismatches vs code parse | yes |
| Through-running | N-E and W-S pairs, weekday peaks | residual of journey duration against run+hall walk+interchange walk: about -4.5 min flat in peaks, +5 min off-peak; ES and NW pairs +3 in peaks; gap between -1 and 0 holds 1 record in 36k. Time at Centraal 06:56 to 09:28 and 15:55 to 18:27. | yes (data-supported) |
| OST reach | 47 | 46.79 | yes |
| EIN, RNG, NRD, WST | 36, 32, 31, 25 | 35.76, 32.32, 31.14, 24.68 | yes |
| ZDT reach | 48 | 48.59 with hall walks in route choice, 48.23 without | fork (48 or 49) |
| OVP reach | 49 | 47.72 with per-journey duration test; 48.59 with clock windows from my time-at-Centraal; 49.31 only with windows shifted 2 min earlier | not reproduced by the exact reading (48) |
| CEN reach | 33 | 30.99 per-journey; 31.91 clock windows; 32.58 windows shifted 2 min | not reproduced (31) |
| BNS reach | 33 | 31.55 per-journey; 32.12 windows; 32.68 shifted | not reproduced (32) |
| Make-good, 9 of 10 bookings | 113,34,171,64,203,195,45,87,137 | identical when re-cabling is dated from the receiving player's CMS DISPLAYS step-up (my fork C) | yes, under that dating only |
| Make-good SB-26-0415 | 591 | 592 (dark 622.27 h, threshold 31.02 h) | off by one hour |
| Make-good, register dating of re-cabling (Bekabeling connected_from, local) | n/a | 280,77,723,324,232,358,466,147,291,405 | differs by up to 460 h per booking |
| Screens on sale | positions deduplicated: CEN 10, BNS 9, OVP 10, NRD 12, OST 18, WST 8, ZDT 19, RNG 14, EIN 14 | identical with position dedupe; per distinct tag: CEN 13, BNS 12, OVP 13, NRD 14, OST 24, WST 11, ZDT 22, RNG 17, EIN 16 | yes under one reading only |
| Net revenue per package | 9,100 / 5,050 / 8,190 / 5,530 / 5,930 / 2,310 / 7,260 / 4,210 / 4,070 | identical (old invoices /1.21, credits via SBM reference, rates 17.5 / 12.5 / 13.5 from statements over gross, commission on net of all credits) | yes, all nine |

Forks (answers produced):
1. Re-cabling instant (supp 3). Bekabeling connected_from versus the CMS DISPLAYS step-up on the receiving player, 3 to 6 days earlier for all ten moves (F025, DF65, C9E6, 38F7, 65D6, 61F8, 8D39, A860, 4B44, D830). AGB 6.2 says "connected" and names no source; the golden step 5 adopts the CMS date by an unfiled convention. Register reading gives 280/77/723/324/232/358/466/147/291/405; CMS reading gives the golden. Secondary forks: Bekabeling timestamps carry no zone (UTC reading adds 2 to 8 h per booking, e.g. 284 for SB-26-0411); AGB 6.3 "above 0.5 per cent" as the excess (golden) versus all dark hours.
2. Screens (supp 4). Seven pairs of rows share a position (new unit hung 3 to 5 Nov, old row open and "in bedrijf"). Replacement (golden) or addition (tag count) is stated nowhere. WLH replacements in the same sheet are closed with taken_down, which favours replacement, but the nine-package count differs by 2 to 5 per package.
3. Reach cells (supp 2). CEN, BNS, OVP and ZDT whole-per-cent values move by 1 to 2 points with the through-run test (per-journey duration versus clock window) and with the tie rule between two one-change routes for Centraal to M3 pairs. Tiers do not move.
4. Net revenue: a reader who takes the statement amounts as the commission ("settled on the agency's own statement") gets ZDT 7,060, RNG 4,060, EIN 3,780. AGB 8.2 and 8.3 say "commission due" at contract rate on value net of credits, so I rate this reading as defeated, not live.

## Files/Hygiene: PASS
14 files; formats pdf (4), csv (4), xlsx (6); rides csv 112,057 rows (25k gate met). Distractors present and unused: instappers_per_halte, reizigersonderzoek, ooh_benchmark, plus out-of-window rides and staff/service cards. Dates coherent (register snapshot 12 Nov, rate card 10 Nov, logs to 4 Nov). No README, generator or benchmark wording seen. Planned minor item: asset tag SB65945 sits on two register rows (HTM-H without take-down, KST-H hung 13 Nov), which is the cause of the WST count question; not exclusion-level. Cross-batch fingerprint against delivered tasks not possible from this directory.

## Stump power (Gate F)
Strong. The easy route (tariff 3.4 plus the line map: every M1/M2 change is at Centraal) gives 63 and 56 per cent for CEN and BNS and a five-package Tier G; halls-only gives ZDT alone. Both are wrong against the golden, and a strong model that reads the rules correctly still files them unless it tests the rides' durations against the planning model. The through-run signal is unmistakable once looked for (9.5 min step), so the trap is fair on the main call.

## Stumping type (Gate G)
`mechanism: other (operating pattern inferred from timings)`, `stumping_family: borderline analytical_non_defect / mixed`, `surface_read_dependency: borderline (leaning yes)`, `sole_data_defect: yes`. The stump is rejecting the planning model's line map for weekday peaks; on data without the through-running the task collapses to a pass tally. Route to live testing and author judgment; I do not raise banned_stumping_type on my own because the line map itself is not a reported wrong figure.

## Three rules (Gate H)
`domain: pass`, `layers: pass` (Layer 1: gate renumbering on 19 Oct, UTC log versus local opening hours, VAT-inclusive old system, a moved asset on two register rows, statements issued before later credit notes; Layer 2: estimating who really changes trains and the reach of a package as a 3-pass share of regular riders), `decisive_step: analytical (borderline planted)`. Reach on a regular-rider panel with pass counts is audience measurement for OOH, and swapping the nouns breaks it. The easy route is the line-map transfer set (CEN 63, BNS 56, five packages in Tier G). The through-running is never stated in a file, is recovered only from duration residuals, and exists only to flip CEN and BNS, so a reviewer may call it a hidden rule; I class it analytical because it is an estimate of who changed trains, which the rate card's own wording ("where the rider changes trains") asks for.

## Fix (location: input_files and prompt)
1. Supp 3: pin the dating rule for a re-cabled screen, or make the register and CMS agree (state the register's connected_from as entry date, or file that the CMS step-up is the instant), and state the zone of Bekabeling timestamps. Recompute 0415 (591 versus 592) and keep the asserted figure identical to the independent recompute.
2. Supp 4: close or drop the old rows at the shared positions (or add a note that the November units add to, rather than replace, the old ones) so the count is one number.
3. Supp 2: recompute CEN, BNS and OVP by the exact per-journey duration test (31, 32, 48 per cent) or state a determinate window and time-at-Centraal convention; state the route tie rule that fixes ZDT at 48 or 49. Tiers need no change. The golden's step 3 says "from its own duration" while its figures (33, 33, 49) only appear under a clock-window shift of about 2 minutes, so the blocks contradict the files at present.
4. Main call and net revenue need no change.


---

# Determinism check, round 2 (2026-11-01): NOT_DETERMINISTIC with SOLUTION_WRONG on three reach figures, SEND_BACK; order kept; Gate G banned; Gate H3 FAIL

The re-judge after round 1's repair. The weekday-peak through-running at Centraal is written in no shipped file and is recoverable only from ride durations: the judge read the stump as rejecting the planning model's line map (planted_defect_flip, surface_read_rejection, sole_data_defect yes) and failed H3 as planted. OVP, CEN and BNS did not reproduce (45, 33, 32 against 47, 34, 33), critical component 2 named the wrong journey pairs, and asks 3 and 4 kept open readings. Architecture 2 is spent and task255 re-roots as architecture 3 in another world. Isolated thread, Sonnet at medium effort, on target.zip bbcaedf8.

# Verdict, task 255 (r2)

ORDER: kept. derivation.md was written and on disk before graded_blocks.md was opened. (After opening it I ran extra checks, listed under Evidence, that the derivation did not contain: the weekday-peak through-running at Centraal and the first-status-ONLINE reading of the CMS log. Both were found by recomputing from the files, not from the blocks.)

- **Verdict:** NOT_DETERMINISTIC, with SOLUTION_WRONG on three reach figures. The Tier G set is itself stable, the failure is on supplementary answer 3 (make-good) and, less sharply, supplementary answer 4 (screens on sale).
- **Disposition:** SEND_BACK. The make-good conventions have to be closed in the shipped terms or the CMS data, and the decisive step is a Gate H and Gate G failure that has to be rebuilt; both change what solvers see, so a rerun is required.

## Why
The main call (Tier G = Overstappunten, Oosttak, Zuidtak) reproduces and is margin-robust, but it is decided by a hidden weekday-peak through-running at Centraal that is written in no shipped file and recoverable only from journey durations (Gate H3 planted, Gate G surface-read flip). Supplementary answer 3 (make-good per booking) is not uniquely forced: the golden stands on three conventions the terms leave open, and the plain alternatives move individual bookings by 20 to 200 hours (Gate C, underspecified_objective). Three golden reach figures (OVP 47, CEN 34, BNS 33) do not reproduce (I get 45, 33, 32), and critical component 2 names the wrong journey pairs.

## Evidence (recomputed from target/)
Reproduced:
- Regular riders: 1,901 (card_class reiziger in RVB_productcodes.csv, a journey by check-in date in each of the weeks of 5, 12, 19, 26 Oct). Reproduces.
- Gate to hall mapping complete (254/254 gate codes in the Gates sheet, both code schemes).
- Net revenue per package, nearest 10: CEN 9,100, BNS 5,050, OVP 8,190, NRD 5,530, OST 5,930, WST 2,310, ZDT 7,260, RNG 4,210, EIN 4,070. All nine reproduce. Invoices from facturen_oud_systeem (/1.21 equals boekingen net_value_eur exactly), SB-26-0429 from the billing export, six credit notes mapped through the legacy invoice numbers, rates 17.5, 12.5, 13.5 per cent recovered exactly from the three commission notes on gross invoiced value, applied to the value net of credit notes (art. 8.2). Forced by art. 8.2/8.3; the 15 per cent standard is the 2027 card, not a 2026 contract rate.
- Screens on sale 1 Jan 2027: reproduces only after collapsing 28 replaced-unit pairs to one screen per position: CEN 10, BNS 9, OVP 10, NRD 12, OST 18, WST 8, ZDT 19, RNG 14, EIN 14.
- Make-good: all ten golden values (254, 161, 734, 101, 207, 252, 65, 91, 342, 256) reproduce exactly, but only under conventions (a) to (c) below.
- Reach figures reproduce for OST 47, ZDT 46, EIN 35, RNG 32, NRD 32, WST 24. They do not reproduce for the three packages that contain the Centraal passage.

Did not reproduce (Gate A, SOLUTION_WRONG):
- With the interchange passage at Centraal credited only to journeys that actually changed, judged per journey from its own duration (an empty band of about 3 minutes separates ride-through from change: residual to the model below minus 3 versus above minus 1, 24,430 regular-rider journeys ride through), I get OVP 45.13, CEN 32.61, BNS 31.56. The golden has 47, 34, 33 (also in FINAL_RECOMMENDATION, SUPPLEMENTARY_ANSWERS 2 and CRITICAL_COMPONENTS 3). The reading is robust to the band cut and to the route model (run time, with waits, fewest changes) and the quadrant/time rule gives the same figures. The tier outcome does not move (CEN and BNS are about 7 points under the line, OVP about 5 over).
- CRITICAL_COMPONENTS 2 says the weekday-peak changes "fall on north-south and west-east journeys". North to south and west to east are same-line trips that never change. In the data the changes fall on north-west and south-east, the ride-throughs on north-east and south-west, as FINAL_RECOMMENDATION says. The block contradicts itself.

Forks (literal execution, the text silent), with the answers they give:
1. Pass counting (art. 3.4 "each time"): per hall or passage (golden): OST 46.66, ZDT 45.92, BNS 31.56 with the peak ride-through (55.55 on the line map alone). Per journey at most once: OST 43.50, ZDT 42.71, BNS 30.14 (54.87 on the line map). Tier unchanged; the sheet-1 figures for OST and ZDT would read 44 and 43 instead of 47 and 46. "Each time" supports the golden reading; treat as closed.
2. Route choice at the three interchanges: three cost models (run plus walk; with waits; fewest changes) give identical reach to two decimals. Not a fork.
3. Make-good, Q3 (Gate C fork, not closed):
   (a) CMS log, players whose first record is ONLINE (7 players: MP-38F7, 7FC3, 96B1, A109, CCF4, D7F0, EB53, all first ONLINE on 6 or 7 Oct). Golden: offline from the start of the log until that record. Alternative (online until an OFFLINE record): 59, 83, 649, 101, 55, 200, 65, 91, 192, 206. Literal art. 6.2 (a screen is connected only from the player's first report that counts it): before that record the screen is not connected, so neither dark condition is met: 55, 83, 647, 99, 38, 191, 65, 80, 190, 203. The golden: 254, 161, 734, 101, 207, 252, 65, 91, 342, 256. Only bookings 0419, 0429, 0430 are identical in all three. No shipped sentence says an ONLINE-first record means offline before it.
   (b) Art. 6.3 "Dark hours above 0.5 per cent ... are made good": excess over the allowance (golden) versus all dark hours once over the line: golden values become 280, 174, 765, 130, 228, 296, 78, 106, 378, 289 (+15 to +36 hours). The excess reading is the more natural one, but the text does not decide it.
   (c) Re-cabled screens: golden and my model use the first CMS report for the new player (17 to 150 hours before the register date, per art. 6.2). Using the register date instead gives 265, 298, 944, 191, 233, 409, 181, 311, 424, 477 (the trap, ruled out by 6.2). Booking SB-26-0415 sits 0.013 hours (0.8 minute) above the rounding edge (648.01 hours excess), so one minute of clock treatment moves 649 to 648.
4. Screens on sale, Q4: register rows give CEN 13, BNS 12, OVP 13, NRD 14, OST 24, WST 11, ZDT 22, RNG 17, EIN 16 (no shipped text says that the 28 new tags of 2 to 4 Nov replace the old ones; the evidence, same position code, same player output, display counts unchanged, supports the golden, so it is inferable but not literal). Excluding the ten "gepland" screens is a third reading (EIN 15, NRD 12, OST 21, ZDT 20 by rows).
5. Tier set under the wrong easy routes: line map only (every Centraal change credited): CEN, BNS, OVP, OST, ZDT (5 packages). No changes at all: only ZDT. All cards in the denominator: only OVP. Staff/service cards or 3-week riders: set unchanged.

Decisive facts and where they sit: threshold, window, regular rider, pass rule, packages: Spoorbeeld_tariefkaart_2027.pdf. Gate renumbering: planning model Gates sheet. Lines, run times, walks: planning model. The weekday-peak through-running at Centraal: in no file. It exists only as a latent pattern in RVB_metro_ritten (98.5 per cent of weekday 07:00 to 09:00 and 16:00 to 18:00 north-east and south-west journeys show no interchange walk and no second wait; the planning model's Frequencies sheet and Interchanges sheet imply a change).

## Files/Hygiene
PASS with notes. 14 files; xlsx (6), csv (4), pdf (4) = 3 formats; one file with 110,356 rows; distractors present (instappers per halte, reizigersonderzoek Q3, ooh_benchmark, the 2027 price table and 15 per cent standard commission). No README or authoring language, no file name naming the trap. Notes: (1) the general-terms pdf is a two-article extract (articles 6 and 8) holding exactly the clauses the asks use, which reads as cut for the task; (2) schermregister_2026-11-12 has SB65945 hung 2026-11-13 with status "in bedrijf" after its own snapshot date, and planned (gepland) rows next to taken_down dates in the future, a mild temporal incoherence; (3) the commission notes are dated 31 Oct and scanned 3 Nov while the credit notes they ignore are dated 2 Nov (coherent). Nothing exclusion-level.

## Stump power (Gate F)
High on the main call: a solver that routes by the planning model alone files five packages including Centraal and Binnenstad, and the Centraal ride-through is not documented anywhere, so only a solver who tests durations against the model will see it. The asks add many silent traps (renumbered gates, replaced units, commission netting, CMS first-report rule). Part of the expected failure on ask 3 is the unforced conventions in fork 3, which is not a valid stump.

## Stumping type (Gate G)
`mechanism: planted_defect_flip`, `stumping_family: surface_read_rejection`, `surface_read_dependency: yes`, `sole_data_defect: yes`.
Banned scaffold: the primary stumping strategy is catching that a misleading surface read, here the planning model's line map which implies a change at Centraal on every M1/M2 journey, is wrong on weekday peaks and flipping Centraal and Binnenstad out of Tier G. On clean data with no through-running the main call collapses to executing art. 3 (the five packages), so the stump does not survive the clean-data test. The surface read being wrong is not, by itself, a sufficient trap, and adding more corrections does not fix it; rebuild the difficulty where the reported numbers are FINE (for example a reach that must be projected or validated, a choice between two defensible audience estimators fixed by a filed back-test, or a binding constraint on honest data).

## Three rules (Gate H)
`domain: pass`, `layers: missing layer 2`, `decisive_step: planted`.
Effective reach (3+ frequency) is a genuine out-of-home audience measure, so the swap test passes. Layer 1 is present (two gate-code schemes, legacy invoices with VAT in Dutch format against the new export, UTC against local, register lag, replaced units). Layer 2 is not: the reach is a filed definition to execute (art. 3.2 to 3.5), and what separates the golden from the line-map answer is a service pattern inserted into the ride timings and written nowhere. Easy route that a strong analyst who read every rule correctly would take: credit the Centraal passage to every M1/M2 journey as the planning model implies, giving CEN 63, BNS 56, OVP 76 and a five-package Tier G, against the golden's three. H3 fails as a hidden rule recovered only from the data, with rule application and data semantics underneath it.

## Fix
- Q3 conventions: input_files/terms. State in art. 6 what an ONLINE record that opens the log means (or add the earlier OFFLINE records), say that connection by first report applies to re-cabled screens, and say whether 0.5 per cent is an allowance or a trigger. Prompt-side: nothing.
- Q4: close the replaced units (a taken_down date on the 28 old rows, or a replaced_by column), and file whether planned hang dates count.
- Solution blocks: regenerate OVP 45, CEN 33, BNS 32 (or fix whatever the author's pipeline does differently, I could not reproduce 47, 34, 33 under any reading), correct CRITICAL_COMPONENTS 2 to north-west and south-east.
- Main call: rebuild the decisive step on a FINE-numbers shape, since the through-running flip is Gate G and Gate H3. The ask layer (net revenue, screens, make-good) can be kept once its conventions are closed.

