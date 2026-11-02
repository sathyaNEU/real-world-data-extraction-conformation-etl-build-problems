# task271 determinism check (architecture 6)

3 isolated judge pass(es), each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 8131c7cd | DETERMINISTIC, SOLUTION_WRONG on the write-up's per-lake figures (order kept; F strong; G PASS; H PASS) | FIX_NOW | the per-lake angler-hours list and every per-lake figure in the write-up replaced by bands every estimator shares; the dead-fish count labelled in fish; the flight log's airborne legs made to contain every count time |
| 2 | 9ec2a0b9 | DETERMINISTIC, SOLUTION_WRONG on critical component 4's wording (order kept; F good; G PASS; H PASS) | FIX_NOW | critical component 4 states the plain expansion's list under the readings where it holds; every band widened to 74 readings (above 510, below 480); Brackwater's overlapping loggers made to agree on every overlap day |
| 3 | 1bb0af6b | DETERMINISTIC (order kept; F good; G PASS; H PASS) | APPROVE | none (the raceway switch left to reconciliation, as the judge advised) |

Earlier architectures' records are in the folder's _arch5 reports.

---

# Determinism check, round 1 (2026-11-02): DETERMINISTIC, SOLUTION_WRONG on the write-up's per-lake figures (order kept; F strong; G PASS; H PASS), FIX_NOW

Isolated thread, Sonnet at medium effort, on target.zip 8131c7cd.

# Verdict, task271 (judge a6r1)

- **Order kept:** yes. derivation.md was written to disk from prompt + bundle before graded_blocks.md was opened. (One correction after opening: my first derivation assumed the trip sheet keeps old raceway numbers through the whole season; I then re-tested against fish_on_hand and confirmed the golden's reading, see Evidence.)
- **Verdict:** DETERMINISTIC (main call and all tiers forced) with SOLUTION_WRONG on the precision of one supplementary list (angler-hours per hectare "nearest 10").
- **Disposition:** FIX_NOW. Regenerate the supplementary-2 block (per-hectare figures as approximate bar heights, or tier plus margin, not "nearest 10") and, optionally, pin the unit of `doa`. No change to what solvers see is required for the block fix; no model rerun.

## Why
The ten-lake high-use set is the only one that comes out of the files once each aerial count is turned into anglers with the lake's own boat party size and expanded by that lake's own interview hour profile. I recomputed it under 8 profile conventions and 4 party-size conventions, stratified and unstratified: every variant that uses a lake-specific (or lake-type) profile with lake or group party size returns the same ten lakes, with the closest high lake at 626 and the closest standard lake at 411-462. Every simpler route (17 h flat, pooled profile, boats-as-anglers) returns a different set. Supplementary 2 (per-hectare figures to the nearest 10) is not forced: it reproduces only with hour-floor binning and moves up to 15 percent under other valid conventions.

## Evidence (recomputed from the bundle)
| Item | My value | Golden | Source |
|---|---|---|---|
| High set (>=500) | Kittiwake, Pinewhistle, Kesterway, Inverkeld, Corriemore, Tessaly, Ellerdine, Ravensky, Quorrin, Brackwater | same 10 | counts + interviews + register |
| Per-ha, hour-floor bins (golden's method) | Kittiwake 1264, Pinewhistle 995, Inverkeld 830, Quorrin 789, Tessaly 775, Corriemore 762, Ellerdine 705, Kesterway 699, Brackwater 659, Ravensky 660, Nockell 430, Galloran 387, Kelloran 384, Farrowdale 364 ... | Kittiwake 1,260 ... (all 22 within 5 of the listed nearest-10) | reproduced |
| Per-ha, continuous interpolated profile | Kittiwake 1420, Pinewhistle 871, Quorrin 702, Ravensky 706, Nockell 388 | n/a | same data, other valid convention |
| Plain expansion (CC4) | Galloran 623, Nockell 586, Farrowdale 611; Ellerdine 420, Quorrin 431, Ravensky 322, Inverkeld 392 | 620, 590, 610; 420, 430, 320, 390 | reproduced |
| Pooled profile leaves list unchanged (CC4) | yes (Farrowdale 555, Galloran 558, Nockell 511 in; same four out) | same | reproduced |
| Releases alive (nearest 100) | 22 of 22 match the golden with: kg split by nets across a trip's lakes, g per fish from the latest/nearest/interpolated weekly sample of the raceway, trip-sheet raceway numbers old->new for 22 Jun to 17 Aug and already new from 18 Aug, doa read as fish | Brackwater 5,000 ... Thornhollow 2,300 | reproduced |
| Raceway numbering | fish_on_hand step-downs reconcile with the trips only under "old numbers 5 May to 17 Aug (mapped after 22 Jun), new numbers from 18 Aug"; max residual 151 fish, versus 3,690 if every trip after 22 Jun is mapped | CC/step 6 | data-derivable, not filed |
| Warm days | PP-02 19, PP-03 57, PP-07 19, PP-09 6, PP-11 57, PP-19 11, PP-20 6, PP-26 19, PP-29 2 | Corriemore 19, Tessaly 57, Kesterway 19, Quorrin 6, Brackwater 57, Kelloran 11, Inverkeld 6, Kittiwake 19, Mosswater 2 | reproduced; mapping serial->lake by deployment time, 20184409 and 20184421 on a UTC clock (step change 7 h after deployment) converted at -7 h, 3 m logger dropped |

Forks examined and closed or small:
- Tier set: closed (above). Tier call is a margin of 160+ either side of 500.
- Raceway number switch on 18 Aug: closed by the on-hand reconciliation (a solver who maps every trip after 22 Jun, the literal reading of raceway_numbers.csv from_date, gets 9 lakes wrong). Closed by data, not by any sentence.
- Weight-sample convention (latest, nearest, interpolated): with doa as fish all three round identically for 22 of 22 lakes. Closed.
- Warm days: PP-11 gives 56 only if the UTC logger is left unconverted or the short overlapping logger 20184533 (reads 0.28 C lower) alone is used for 10 Jul; pooled, averaged, or the long logger give 57. Gap days (PP-19 1-13 Jul after the 20184417 stopped 3 Jun; PP-20 1-21 Jul because logger 20184446 is absent from the file) are counted only where data exist; partial first days do not change a count. Ignoring the deployment windows gives PP-03 37, PP-11 34, PP-19 20, PP-20 24.

**Findings (each with the gate it fails):**
1. Supplementary 2, angler-hours per hectare "nearest 10": not forced; the figure depends on hourly-bin convention (Kittiwake 1264 floor-hour, 1420 interpolated, 1519 nearest-hour; Pinewhistle 995/871/995; Quorrin 789/702/928). The prompt gives no rounding for these and the filed text does not pick the binning. The tier is unaffected. Fails Gate C/E for that supplementary answer; repairable in the block (SOLUTION_WRONG). Taxonomy label: solution_incorrect (precision overclaim).
2. Sheet 2, unit of `doa` is filed nowhere (drop-tally JSON has `nets` and `doa`, no dictionary). Read as fish it gives the golden; ignoring it gives the same 100s for 20 of 22 lakes; read as nets (alive share 1-doa/nets) every lake drops 15-30 percent (Corriemore 2,200 vs 3,000). Domain convention (dead fish, mortality under 2 percent) supports fish, but no file pins it. Gate E (small, supplementary 3). Optional pin: name the field in fish.
3. Hygiene, temporal coherence: vellacott_air_flight_log shows the aircraft on the ground at the Pillory dock 15:30-16:19 PT on 14 and 16 Aug, yet survey_flight_counts timestamps lakes 11-17 at 15:32-16:11 PT on both days. No effect on tiers.
4. Logger clock is undocumented; two serials (20184409, 20184421) are on UTC and the rest on Pacific, and the Site column is a stale label for two re-deployed serials. Derivable (step change at deployment time, diurnal peak), prompt hints with "Pacific-time day". Acceptable Layer 1; no gate fails.

## Files/Hygiene
PASS with the notes above. 13 files, formats: csv x6, xlsx x4, pdf x2, json x1 (4 formats), one file of 101,650 rows. Distractors in play: campground_permits_2026.xlsx, vellacott_air_flight_log_2026.xlsx, the clipped-fin and licence columns. No README or authoring language seen; no public-data contamination. Findings 3 and 4 above are not exclusion-level.

## Stump power (Gate F)
Strong. The two natural routes (count x 17 h, or pooled hourly profile) are wrong by 7 lakes, and the interviews that separate them are shipped without a hint; party size per boat is the second needed step (boats-as-anglers gives only 3 high). A strong model that builds lake-specific hour profiles clears it, so I expect partial stumps, not a coin flip. No too-easy signals: no shipped artifact ranks the lakes.

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (estimator choice: diurnal expansion of instantaneous counts), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported counts are correct; the difficulty is the estimator, and on clean data the flat expansion would still be wrong. Passes.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to read the same: the deciding quantity is a creel-survey angler-effort estimate (aerial counts expanded by an interview-derived diurnal pattern). Layer 1: UTC and Pacific logger clocks, serial re-deployment, old and new raceway numbers, re-issued Vellacott numbers, boats vs anglers. Layer 2: expansion of two midday counts by each lake's own effort curve. Easy route: boats times lake party size times 17 hours, which files Galloran, Nockell and Farrowdale high and Ellerdine, Quorrin, Ravensky and Inverkeld standard.

## Fix
solution: restate supplementary 2 as bar heights within about 15 percent (or tier only, with the 500 line); optionally note in the block that doa is read as fish. input_files: none required (optional: label the JSON field as fish).

---

# Determinism check, round 2 (2026-11-02): DETERMINISTIC, SOLUTION_WRONG on critical component 4's wording (order kept; F good; G PASS; H PASS), FIX_NOW

Isolated thread, Sonnet at medium effort, on target.zip 9ec2a0b9.

# Verdict, task271 (judge a6r2)

Order kept: derivation.md was written to disk before graded_blocks.md was opened. Yes.

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (one overclaim in CRITICAL_COMPONENTS 4; no graded figure is wrong).
- **Disposition:** FIX_NOW. Reword CRITICAL_COMPONENTS 4 (and the "stays above 550 however..." phrasing if kept) to the variants that actually hold; the shipped files and prompt stay byte-identical, no model rerun needed. Optional prompt-side pins listed under Fix would change what solvers see, so they are not required for this verdict.
- **Why:** Rebuilt from the files, the ten-lake high-use set is forced: every lake-specific-profile estimator I ran (36 variants: smoothing 0/1/2 h, day-type split or not, lake or pooled boat party size, three stratifications) gives the identical tier list, with the closest high lake Brackwater at 551 and the closest standard lake Galloran at 454. The lake's own interview profile is also validated by the data (AM-implied and PM-implied daily effort agree per lake, ratio about 0.6 to 2.0, while counts alone differ 3x for Tessaly and Kesterway), so the flat and pooled-profile lists are analytical errors, not an open fork. Gates A to E pass; Gate A fails only on CC4's overclaim, which is a SOLUTION_WRONG carve-out.

## Evidence (recomputed, reproduced yes/no)
| Item | Mine | Golden | Source |
|---|---|---|---|
| High-use set (angler-hours/ha, ref estimator) | Kittiwake 1416, Pinewhistle 874, Kesterway 839, Inverkeld 828, Corriemore 797, Tessaly 754, Ellerdine 724, Ravensky 700, Quorrin 699, Brackwater 646 | same 10 | counts + interviews + register |
| Standard set | Galloran 400, Nockell 388, Kelloran 367, Farrowdale 350, Bufflehead 298, Copperjack 298, Saddlebank 245, Ostrum 240, Thornhollow 227, Canvasback 215, Mosswater 178, Pillory 168 | same 12 | same |
| "high above 550, standard below 480" | min high 551 (Brackwater), max standard 454 over the 36 variants | holds | reproduced |
| Releases alive, nearest 100 (22 lakes) | all 22 equal the golden (e.g. Brackwater 5000, Canvasback 4400, Mosswater 4500, Pillory 4800, Kelloran 3200, Ellerdine 1000) | same | trip sheets x raceway samples x drop tallies; identical under prev/next/nearest/interpolated sample choice |
| Warm days | PP-11 57, PP-03 57, PP-02 19, PP-07 19, PP-26 19, PP-19 11, PP-09 6, PP-20 6, PP-29 2 | same 9 | loggers x deployments |
| CC4 "plain expansion puts Galloran, Nockell, Farrowdale above 550 and Ellerdine, Quorrin, Ravensky, Inverkeld below 460, however the boats are turned into anglers" | holds only with lake party size (Galloran 623, Nockell 586, Farrowdale 611; Ellerdine 420, Quorrin 431, Inverkeld 392, Ravensky 322). With pooled party size: Galloran 518, Nockell 488, Farrowdale 508, Quorrin 533, Inverkeld 499; with 2 per boat: 530/498/519 and Quorrin 548 | overclaimed | NOT reproduced as worded |

Lake-by-lake range over the 36 estimator variants is in derivation.md. Flat (count x 17 h) flips 7 lakes (Farrowdale, Galloran, Nockell wrongly High; Ellerdine, Inverkeld, Quorrin, Ravensky wrongly Standard). A pooled all-lake profile with lake party size also puts Farrowdale 551 and Galloran 557 High.

Layer-1 derivations verified: (a) trip sheets repeat the whole truck load on each destination row, split by drop-tally nets and less DOA; (b) raceway renumbering: the trip sheet stays in OLD numbers through 14 Aug and is in NEW numbers from 18 Aug (fish_on_hand weekly drops reconcile only under that switch; applying the csv from_date 22 Jun to every later trip moves 9 lakes: e.g. PP-11 5400, PP-14 2800, PP-18 2800, PP-19 2600); (c) loggers 20184409 and 20184421 are on UTC (step at deployment is +7 h), Site labels in the logger csv are each logger's final site, not its position in July.

Residual forks (all minor, none changes the main call):
1. Ask 5 Brackwater (PP-11): two simultaneous 1 m loggers to 14 Jul; on 10 Jul the continuous logger reads 20.21 and the second 19.93. Continuous logger or the mean gives 57; second-logger-only for its days gives 56. Also an unshifted (non-UTC) 20184409 gives 56. No filed rule picks the logger. Gate C (supplementary 5), minor.
2. Ask 5 Kelloran (PP-19) and Inverkeld (PP-20): the loggers have no data for 1-13 Jul and 1-21 Jul (20184417 stopped 3 Jun though its record says retrieved 14 Jul; 20184446 has no file at all). 11 and 6 are counts of observed warm days only; the unobserved early-July days were warm at the other lakes (about 5 of the first 9 days), so the true counts are likely higher. The literal reading gives 11 and 6; inclusion of the two rows is not pinned. Gate E (supplementary 5), minor.
3. Raceway-number switch date has to be inferred (tank-temp column starts 18 Aug; on-hand reconciliation settles it). Derivable, so it passes Gate B; it is data semantics, allowed because it sits in an ask, not the main call.
4. Note chart "every lake's angler-hours per hectare": 22 stocked lakes or all 24 register lakes is not pinned. Gate E, deliverable-form only; ungraded for the tier call.

## Files/Hygiene
PASS. 13 files, formats csv, xlsx, pdf, json (4), one file of 101,650 rows (loggers), distractors present (campground_permits, vellacott_air_flight_log, 3 m logger, raceway on-hand column). Mess is system-produced (UTC vs Pacific, renumbering, duplicate rows, final-site labels, partial fog/smoke loops). Dates coherent (policy 12 Mar 2026, protocol 28 Apr, export 2 Sep, November board). No authoring language in files; PDF/xlsx properties carry plausible in-fiction authors. Interviews and flight counts are clean-looking synthetic but not machine-signed. No exclusion-level finding.

## Stump power (Gate F)
Good. The trap that does the work is the count-to-effort expansion: the flights pass every lake only at 09:30-12:00 and 14:30-17:00, and the interviews show three diurnal archetypes, so a flat 17 h expansion (or one pooled hourly profile) gives a wrong 7-lake list that a competent analyst could file without ever seeing an error. Nothing in the prompt, protocol or policy names the diurnal issue; the policy's "anglers fishing it in each hour" is the only hint. Asks (renumbering, split trips, UTC loggers, final-site labels) add independent difficulty.

## Stumping type (Gate G)
`mechanism: other (estimator design for a creel effort estimate, count-to-effort expansion with the lake's own diurnal profile)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is misleading and none is shipped; on perfectly clean data the flat-versus-profile expansion still splits the call, so it is not a defect flip. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
H1: swap test fails the swap (angler effort from aerial counts and access interviews with diurnal correction is a core fisheries creel-survey estimate; changing nouns to hospital/visits breaks the interview-time profile logic). H2: Layer 1 is UTC vs Pacific logger clocks, renumbered raceways, duplicated trip rows, fog/smoke-missing loops, final-site labels; Layer 2 is the lake-specific time-of-day expansion of instantaneous counts. H3: a strong analyst who cleaned everything and read the policy correctly still files count x 17 h (Farrowdale, Galloran, Nockell High; Ellerdine, Inverkeld, Quorrin, Ravensky Standard), the wrong answer; no planted decoy, hidden rule or stated-score execution.

## Fix
Location: solution. Reword CRITICAL_COMPONENTS 4 to the claim that holds ("with each lake's own anglers per boat, the plain expansion puts Galloran, Nockell and Farrowdale above 580 and leaves Ellerdine, Quorrin, Ravensky and Inverkeld below 440"; with pooled party size they sit at 488 to 518 and Quorrin 533, so do not claim "however the boats are turned into anglers"). Drop the same universal from FINAL_RECOMMENDATION's contrast sentence if kept. Optional (changes what solvers see, so a rerun): close ask 5 with a clause on which logger counts where two hang at 1 m and what to do for lakes with no readings in part of July, and pin whether the chart shows 22 or 24 lakes.

---

# Determinism check, round 3 (2026-11-02): DETERMINISTIC (order kept; F good; G PASS; H PASS), APPROVE

Isolated thread, Sonnet at medium effort, on target.zip 1bb0af6b.

# Verdict, task271 (stocking tiers 2027)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; two optional notes below (no rerun implied).
- **Order kept:** yes. derivation.md was written to disk first; graded_blocks.md was opened only afterwards (an addendum records what changed).

## Why
The ten-lake high-use list is forced once each flight count is read against the hours that lake's own anglers fish (interview presence profile per lake or per regulation class). Using both loops, every high-use lake stays at 559 ah/ha or more and every standard lake at 430 or less across class or lake profile, hour / nearest / interpolated / around readings, own, class or shared party size, month or weekday-weekend strata, mean or ratio of loops (the AM-only subset is not a defensible estimator). The pooled-profile and plain 17-hour expansions give a different list (Galloran, Nockell, Farrowdale in; Ellerdine, Quorrin, Ravensky, Inverkeld out) but are refuted by the data (see Evidence). Release counts and warm days reproduce for every lake.

## Evidence (recomputed from target/)
| Item | Result | Reproduced |
|---|---|---|
| Lakes taking catchables | 22 (lake_register col K = yes; PP-35, PP-37 not) | yes |
| Tier list, class/lake profile | High: Corriemore, Tessaly, Ellerdine, Kesterway, Quorrin, Brackwater, Pinewhistle, Ravensky, Inverkeld, Kittiwake; others standard (ah/ha e.g. Kesterway 610-870, Ellerdine 617-870, Nockell 324-430, Galloran 322-398, Farrowdale 302-416) | yes |
| Plain expansion (count x 17 h x 109 d, own party size) | Galloran 699, Nockell 668, Farrowdale 670 in; Ellerdine 444, Quorrin 442, Ravensky 395, Inverkeld 421 out | yes, matches golden CC4 |
| Profile choice | Fly-only share peaks 06-08 / 18-21, general 11-14. AM/PM expanded medians agree under class profiles (0.85-1.12), split under pooled (1.82 / 1.30 / 0.80) | data separates the candidates |
| Releases (alive, nearest 100) | all 22 equal the golden (e.g. Brackwater 5000, Nockell 3100, Pillory 4800) | yes; identical under prev / nearest / next / interpolated sample weight, none within 20 fish of a rounding edge |
| Warm days | Brackwater 57, Corriemore 19, Inverkeld 6, Kelloran 11, Kesterway 19, Kittiwake 19, Mosswater 2, Quorrin 6, Tessaly 57 | yes (deployment-table key, 20184409 / 20184421 UTC to Pacific) |

Forks examined, with the answer each gives:
1. **Trip-sheet raceway numbering after 22 Jun (Gate B/C, supplementary 4).** No file states which numbering the trip sheet uses. Read literally from raceway_numbers.csv (new numbers from 22 Jun) it gives e.g. Corriemore 2500, Inverkeld 2400, Nockell 3500, Kesterway 3800. Reconciling trip kg / sample weight to the weekly fish_on_hand declines shows trip sheets stay in old numbers until 14 Aug and are new from 18 Aug, the day the Tank temp column first fills (max residual 150 fish; switch 22 Jun gives residuals up to 4450). The golden uses this. It is forced by the files but only by that reconciliation. Risk: low to moderate.
2. **Diurnal profile pooled vs class / lake (main call).** Pooled gives the plain list; refuted by the AM/PM consistency test and by the visibly different interview profiles. The prompt's "the angler-hours it drew" supports the lake's own hours. Risk: low.
3. **Logger days with no data (PP-19 Jul 1-8, PP-20 Jul 1-21; logger 20184446 never retrieved, 20184417 stopped 3 Jun).** Literal count of days with a measured above-20 mean gives 11 and 6; the partial days (Jul 9, Jul 22) are below 20 either way. Site-label keying would give 20 and 24; UTC-day reading gives PP-11 56, PP-19 10. Low risk.
4. Nets as the split of a multi-lake trip load: kg per net about 10 on every trip, so the split is evident. Low risk.
5. Gate E: golden supplementary answer 3 gives only bounds (above 510, below 480) for ah/ha; the chart's bar heights are estimator-dependent, but only the tier against 500 is graded and it is robust.

## Files / Hygiene: PASS
13 files; formats: xlsx (4), csv (6), pdf (2), json (1). The 101,650-row logger csv exceeds the 25,000-row gate. Distractors present and unused: campground_permits_2026.xlsx, vellacott_air_flight_log_2026.xlsx (UTC; consistent with the count times), the 3 m Quorrin logger, licence and clipped-fin interview fields. Layer-1 mess reads like system output (re-issued Vellacott numbers, logger Site labels that do not follow deployments, mixed UTC / Pacific clocks, repeated trip rows per destination, a trip-sheet layout change on 18 Aug). No authoring or synthetic disclosures seen; dates coherent (drop-tally export 2 Sep, loggers retrieved 9-12 Sep, policy for the Nov board). Nothing exclusion-level. Cross-batch fingerprint: no prior package supplied in this folder, so no duplicate could be tested.

## Stump power (Gate F)
Good. The trap that does the work is applying the interview-derived hours of the lake's own regulation class to counts taken at route-fixed times (about 09:30-12:00 and 14:30-17:00): the plain or pooled expansion moves seven lakes (three in, four out). A strong model that expands counts by 17 hours, or uses one survey-wide profile, files the wrong list; one that checks AM against PM agreement lands the right list. No too-easy signals (no document explains the profile; the margin 559+ vs 430- is wide).

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (estimator choice on honest data, pinned by AM/PM validation), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is wrong; the clean-data version still stumps. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: creel-survey effort estimation from aerial counts and access interviews is the fisheries field's own method (swap "visits" for "angler-hours" and the task no longer reads). Layer 1: re-issued Vellacott numbers, mislabelled / moved / UTC loggers, renumbered raceways, repeated trip rows, fog and smoke blanks. Layer 2: expanding instantaneous counts by the lake's own diurnal profile and angler-per-boat size, stratified by day type. Easy route: count x 17 h (or one pooled profile) gives Galloran, Nockell and Farrowdale high-use and Ellerdine, Quorrin, Ravensky, Inverkeld standard, wrong for seven lakes. No planted defect, withheld rule or pure rule execution decides the call; the asks (releases, warm days) lean on data semantics, which is allowed.

## Fix
none required. Optional, in-house and without moving any figure: nothing to add to files (a note would pre-disarm the raceway reconstruction); keep the tank-temp layout change as the only cue.
