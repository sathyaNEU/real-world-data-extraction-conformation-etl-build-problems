# determinism-check report, task247, 2026-11-02 (pass 2)

## Verdict
DETERMINISTIC on the main call and the DHW figures; the logger-hours ask (supplementary answer 2) reproduces exactly but rests on two conventions no shipped sentence files. No SOLUTION_WRONG: every golden figure reproduced.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (with etl_conformance for the extract, flag and logger work), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle: target.zip md5 c4e68804715e9c56d6463d7721d8f91f. One thread (sonnet, medium). Verdict at /tmp/determinism-check-task247-85125/verdict.md.

## Why
The nine-site list is forced. Gap-filling the near-real-time analysis from the observed days either side is the only candidate the 2018 to 2026 overlap validates (rms 0.065 and hot-day bias -0.001, against 0.142 and -0.262 for the flag-mean correction, 0.143 and -0.270 for the raw feed). Every reasonable variant leaves all 16 whole-number DHW values and all 16 levels unchanged.

The logger-hours ask reproduces exactly under the golden's site mapping and clock, but the literal reading of the shipped pin register and log gives different numbers. The readings themselves contradict that literal reading, so one reading is evidence-supported, but no filed sentence says so (Gate C/E exposure; underspecified_objective if a reader holds to the register).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| NRT extract, latest issue per pixel-day | 57,824 rows to 57,472 pixel-days, 17 June 2027 absent | 57,824 to 57,472; 3,592 days per pixel; 17 June absent; flag by version (3.2: 2 observed, 1 not; earlier 1 and 0) | yes |
| CC1 NRT less reprocessed, observed days | 0.06 | 0.0595 | yes |
| CC2 refill rms / hot bias (1,174 hot days) | 0.065 / -0.001 | 0.065 / -0.001 | yes |
| CC2 flag-mean correction rms / hot bias | 0.142 / -0.263 | 0.142 / -0.262 | yes |
| Season-max DHW, 16 sites | 3, 5, 2, 6, 5, 9, 11, 7, 10, 12, 13, 10, 12, 9, 11, 6 | 3.11, 4.94, 2.04, 6.07, 5.02, 8.85, 11.06, 6.96, 10.00, 11.98, 12.99, 9.90, 12.25, 9.01, 11.02, 5.96 | yes, all 16 round to the golden |
| Levels, verdicts | 8 confirm, 8 raise, none lowered | same | yes |
| CC3 declared levels (27 bulletins) | as listed | match exactly; bulletin level against DHW consistent in all 432 rows | yes |
| Logger hours, 16 sites | 2,565 (PB09) to 4,678 (PB04) | exact under the golden mapping plus the 5-hour clock correction | yes, under the golden's two conventions only |

Variants (offset 0.0595, per-site offset, raw-SST interpolation, window to 2 Nov, uncorrected fill): no whole-number or level change. Nearest margin to a threshold: PB06 at 8.85 against 8. Competing methods fail the list: raw NRT gives PB06 8.32 and PB04 5.37 but misses PB11 to PB15 (7.55, 5.99, 7.05, 4.93, 7.37); offset-only and flag-mean corrections do the same (PB06 7.80 and 8.00 against 8).

## Competing answers that survived
Two forks, both on ask 2, all 16 hour figures.

1. **Site of each deployment.** Shipped text gives only logger_pin_register.csv (E01 to PB01 through E16 to PB16, no date or caveat) and a log with a pin column and no site. The literal reading (register applied to every row) is a second answer. The files do not state that the tags of the five trips before 18 August 2025 differ, nor that the boat's stops run north to south. The data do show that within a trip the log's time order is the same on the four trips of Aug 2023 to Apr 2025 (E06 E05 E07 E13 E08 E02 E01 E14 E03 E04 E09 E10 E16 E12 E11 E15) and is E01 to E16 on the four later trips. On the 48 earlier deployments the readings' daily changes correlate with the reprocessed SST at the golden-mapped pixel in 48 of 48 cases as the best of 16 (mean r 0.72), against 0.24 for the register reading. On later trips both mappings coincide (mean r 0.69). The data single out the golden mapping, but only a solver who tests the register against the satellite series, or reads the stop order, gets there. Register-throughout difference from golden (hours): PB01 -419, PB02 -255, PB03 +111, PB04 -503, PB05 +55, PB06 +318, PB07 +49, PB08 +524, PB09 +186, PB10 +470, PB11 +99, PB12 +9, PB13 +424, PB14 -778, PB15 -89, PB16 -218. All 16 differ.
2. **Clock.** The log carries no time-zone label. The 2025 and 2026 Cozumel II rows read 13:27 to 18:19 while Ixchel rows read 08:00 to 13:10, and the readings show the logger leaving the water about 4.4 hours before the logged retrieval on the August 2025 trip (Ixchel retrievals: +0.5 hour after). Only the August 2025 retrievals touch a June to October season. Reading the log as local gives +5 hours at every one of the 16 sites (e.g. PB01 3,589 for 3,584, PB09 2,570 for 2,565). Other boundary choices move nothing.

Clean checks: serial reuse across pins resolves by serial plus window with no overlap; no model bias between TidbiT and MX2203; hot deck readings before the logged deployment lie outside the window; one reading an hour, no duplicates, no gaps touching the season.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 in the bundle (judge counted 17) | yes |
| Formats | 3 or more | csv, xlsx, pdf, eml (4) | yes |
| Large file | 25,000 rows or more | logger_readings_from_2024-04-01.csv, 425,836 rows (plus 57,824-row NRT extract) | yes |
| Distractors named, none labelled in a file name | 2 or more | metadata.json names 4 (kd490 monthly, port tide gauge, 2023 slates, 2023 protocol); none labelled by name | yes |
| Distractors unused yet weighable | each | judge found them unused; none gives a site a heat-stress figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | DHW to nearest whole number, hours whole; per-site over 16 sites | yes |
| Prompt shape, 25 or more rubric criteria | identifiable, 25+ | shape 01 in metadata; 732-character one-paragraph prompt, no persona; criteria count is generated downstream and not checked here | shape yes, count not verified |
| Reads as real work product, not LLM generated | yes | judge saw no authoring language | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's declared stump is the reconstruction of the filled days (the flag-mean route files three, the golden nine), asserted analytical and neutral to Layer 1. This matches. The judge names no distractor as the surface read carrying the task; the bulletins are arithmetically right for the feed they ran on and are the comparison, not a ranking on the reference record. Gate G holds: no shipped artifact ranks the sites on the decision question wrongly except as declared bulletins. No mismatch.

Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: version-dependent flag coding, re-issues, kelvin against Celsius, a missing day, UTC against local logger clocks, re-tagged pins. Layer 2: estimating the season maximum on a record not yet released by validating the feed's correction against the overlap. This agrees with the design note's Three rules (no decoy, not semantics, not rule application).

## Stump power (Gate F)
The trap is the near-real-time analysis's fade toward climatology on unobserved days, which understates a lasting warm anomaly in the cloud-covered south. The bulletins' four sites and any raw-feed, offset-only or flag-mean rerun file a wrong list (4 to 6 sites against 9); only a back-test on the 2018 to 2026 overlap shows which correction works. A strong model that applies the 0.06 offset or the flag-mean correction falls for it. The logger ask adds a second, independent lure (register and clock) that is a reading question and not a stump. The decisive step is not a field-standard method reached without judgment, so no landable-call caveat applies; the main thread weighs the ladder.

## Findings, ranked
1. Ask 2 logger hours: site identity per deployment is unfiled (register has no date or caveat; earlier tags are recoverable only from stop order or correlation with satellite SST). All 16 figures differ under the literal register reading.
2. Ask 2 logger hours: log clock is unlabelled; Cozumel II August 2025 rows are UTC, 5 hours off at every site. Smaller, but it moves all 16.
3. Main call and DHW figures: no finding. PB06 at 8.85 against threshold 8 is the nearest margin and holds in every variant.
4. Criteria count not verified in this pass.

## Next action for the author
Close ask 2 by filing the WHAT in one place: the site each logger deployment is at (for example a dated column in logger_pin_register.csv, or a prompt sentence that a deployment's site is the site whose water it records) and the clock the log rows keep (a note in the log or a time-zone column). Do not file the HOW of the gap-fill. The alternative is to remove ask 2 from the graded set. Keep the main call and the 16 DHW values frozen; no rerun of the main call is needed.
