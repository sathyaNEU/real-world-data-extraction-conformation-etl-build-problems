# Judge verdict, task184

**Verdict:** NOT_DETERMINISTIC (the golden reproduces exactly, but only under method and convention choices the shipped text never files).

**Disposition:** SEND_BACK. The main call's estimand has to be filed in the prompt or the contract so that its literal execution is the golden. That changes what solvers see, so a rerun is required.

**Why:** The prompt asks how many covered offences "the patrol would meet" in each slot. For 80.1% of covered offences the record holds only a window, and the data dictionary says "none is derived", so no count of offences in a slot exists in the record. The golden turns on a pooled hour-of-week occurrence distribution, estimated by maximum likelihood across the five classes and both seasons, and run to convergence. Nothing in the prompt, the contract, the dictionary or the standard files that estimand. Clause 4.4 ("built from the force's record ... and from nothing else") rules out external profiles such as footfall, trading hours and licensed premises. It does not choose between the exact-time rows alone, the whole record pooled, or the record by class. Gate C fails on the main recommendation, supplementary answers 1 and 2 of the PDF, and the 42-slot grid. Governing label: underspecified_objective, with competing_defensible_answer for the surviving alternative slates.

## Evidence

**Reproduced.** All of these came from the bundle alone.

| Value | Result |
|---|---|
| Covered rows (five Annex B classes, location code HG-L01 to HG-L05) | 25,020, so 12,510 a season. Season by occurred_from: 12,135 and 12,885. No window crosses a season boundary. |
| Covered rows by address instead of code | Same set. Covered classes carry a code on every row. CR-L codes are the Cranstoun length and are excluded. |
| Windowed share | 80.1% |
| Window longer than 4 hours | 79.6% |
| Converged pooled hour-of-week MLE, half-open windows, hour cells | Heaviest 1,119.7 (Thu 20:00 to 00:00), lightest about 50. Top eight are the golden eight, ninth is Fri 16:00 to 20:00 at 408. Eight sum to 5,705.2, which is 5,700 when each figure is rounded to 50. |
| Same MLE from three random starts and at 10-minute cells | Converges to the same shares (max slot difference about 1e-9). Same slate. |
| Workbook class counts (RMS plus CIS, with the 14 to 27 July overlap de-duplicated by class, location and time) | All 18 figures reproduce within the stated rounding to 10. |
| Location shares | 35.8, 13.8, 19.3, 21.2, 9.9 for 2025 and 35.7, 13.8, 19.8, 21.1, 9.6 for 2026. All 10 reproduce. |
| Footfall, UTC+1, trading hours from the trading-hours file, sensor fault windows excluded | 1,319, 1,380 / 859, 898 / 597, 623 / 477, 500. All 8 reproduce. |

I recomputed every figure at the golden's grain, which is 201 figures in all. Every one reproduces under the golden's conventions. The conventions are what is open.

**Open forks on the main call (literal reading, nothing inferred).**

| Reading | Slate or figures | Eight total |
|---|---|---|
| Golden: pooled MLE, converged, half-open windows | Thu 20, Sat 00, Sun 00, Sun 20, Fri 12, Wed 20, Mon 20, Tue 20 | 5,700 |
| Flat spread over the window's hours (my own eight-slot sum on its own weights) | Weights flat at 350 to 450; Fri 12:00 to 16:00, Thu 20:00 to 00:00, Fri 00:00 to 04:00 lead; the set differs from the golden | about 3,150 |
| Profile from exact-time rows only, one pass | Takes Thu 08:00 to 12:00, Thu 12:00 to 16:00, Sat 08:00 to 12:00 and Sat 12:00 to 16:00 in place of Sat 00:00 to 04:00, Sun 00:00 to 04:00, Wed 20:00 to 00:00 and Tue 20:00 to 00:00 | about 4,900 |
| Same MLE fitted per class (the data does not reject pooling: LR 511 on 668 extra parameters, but the per-class fit is a defensible modelling choice and nothing forbids it) | Swaps Mon 20:00 to 00:00 for Fri 16:00 to 20:00; heaviest 950 | about 4,850 |
| Same MLE with the window end treated as an inclusive hour cell (an 11:00 end touches the 11:00 hour) | Different set (Sun 00:00 to 04:00 and Tue 20:00 to 00:00 give way to Sun 04:00 to 08:00 and Fri 16:00 to 20:00) | about 5,400 |
| Same MLE stopped early (50 iterations) | Heaviest 1,050; total 5,457 | 5,457 |
| Likelihood on windowed rows only | Different slate again | n/a |

The convergence criterion ("until they stopped moving") is also not filed. Early stopping moves the figures (at 10 iterations the slate itself differs), though from about 200 iterations the 8-slot set is stable. The pooled-across-classes, ignorable-windows assumption is not filed either, and the data cut against it. The probability that a row carries an exact time runs from 0.00 to 0.62 by slot (Sun 04:00 to 08:00 is 62% exact, Sun 00:00 to 04:00 is 0%) and from 4% to 34% by class. A solver can reasonably doubt that exact-time rows and windowed rows share one occurrence distribution.

**Clause 4.4.** Read on shipped bytes, the sentence composes into the method. By itself it forbids bringing a footfall, trading-hours or licensed-premises profile in. It also endorses building a slot count out of the record's own exact times, which is the exact-profile reading and gives about 4,900, not 5,700. The sentence does not by itself reach the golden, because it does not say the windowed rows may inform the shares or that classes pool. It reads as a nudge toward the intended method without closing it. The write-up's step 4 states the missing method ("the hour-of-week shares under which the windows the force recorded are the likeliest set of windows to have been recorded") and that is not in the shipped text. A fork closed only by the write-up counts as open.

**Exact-time rows (about a fifth of covered offences, 4,973 of 25,020).** They do not read as planted. They are an authentic consequence of the shipped data: the dictionary and standard 3.1 record a known time as a point, and the CIS notes describe the same convention. The pattern by class (vehicle and cycle theft 4 to 5%, burglary and damage 27 to 34%) is plausible for recording practice. I could not distinguish authentic mess from a generator mechanism from the bytes. They are, though, the sole anchor of the golden's slate and they are strongly time-dependent in how often they occur, which is the ground on which the pooled estimate is contestable.

**Supplementary answers.**
- The PDF slate and the 42-slot grid inherit the main call's open estimand.
- Workbook items 2 and 3 (class counts and location shares) depend on three conventions the prompt does not state: nine classes including the CIS four, de-duplication of the 14 to 27 July double entry, and "all of them" meaning all nine classes. Dropping the CIS file moves the 2025 shares to 34.2, 15.4, 20.5, 18.8, 11.2. The extract notes close the migration and the overlap, so these are closable by the files, but they are not closed by the prompt.
- Workbook item 4 (footfall) needs three further choices: the UTC+1 shift (stated in the notes), trading hours (from the file), and excluding the sensor fault windows. The last is only inferable. Counting faulted hours gives 1,273, 1,346 / 819, 850 / 578, 575 / 460, 483. Averaging all hours rather than trading hours gives about 1,090, 1,141 etc. The prompt says "per trading hour" but never says to drop the fault windows, and it asks for "the footfall each sensor's location saw", which a faulted hour does not measure. The fault file's presence makes exclusion likely but not literal.
- Shoplifting counts are per victim in RMS and per incident in CIS (extract notes). The golden sums them as recorded, which the question's "recorded offences" supports. This stays as a note, not a fork.

**Estimand test.** The main call's estimand is not filed literally enough. "How many ... would the patrol meet" asks for an expectation under a time distribution the record does not hold. The prompt does not name the population (all covered offences, pooled), the distribution (hour-of-week, common across classes and seasons) or the convention for window ends. A literal execution of the shipped text gives no count at all. Executing the literal text word for word gives no count; the readings above give the other slates.

## Files/Hygiene
PASS. 16 files in six formats: csv (11), pdf (2), xlsx (1), md (1). The input gates are met: one file of 33,766 rows, one of 35,136 and one of 3,598. The 2026 patrol plan workbook, the licensed-premises file, the trading-hours file and the CIS extract are plausible distractors or context. The documents read as system exports with realistic mess (CIS date format and four-field occurrence, alternative street names, CR-L Cranstoun rows, per-victim shoplifting). No authoring leakage, benchmark language or temporal incoherence found (extract dated 22 January 2027, contract signed 4 December 2026, standard current at 1 January 2027). No exclusion-level finding.

## Stump power
The trap that would do the work is the unobserved time inside a window: a flat or midpoint read lands on a different slate, and only a deconvolution against the exact-time rows gives 5,700. A strong model that spreads windows evenly fails for a real analytical reason, so stump power is high. But a model that fits a per-class or exact-profile estimate also fails, and that is the unfiled-method fork above, not an analytical error.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported data are fine and the difficulty is choosing an estimator for an interval-censored occurrence time. It passes Gate G, and on clean data it would still stump. The defect is that the method selection is not pinned by anything shipped (no back-test, no standard, no filed selection criterion).

**Gate G classification:** pass (method_or_model_selection on honest data). **Gate H:** domain: pass, layers: pass, decisive_step: analytical.
Gate H detail: the field's own analysis (estimating an occurrence-time distribution from interval-censored records, then sizing patrol coverage) decides the answer. Layer 1 is the CIS to RMS migration, UTC against local time, address variants, per-victim against per-incident counting and the sensor faults. Layer 2 is the censoring-aware estimate of slot counts. The easy route (spread each window evenly, or use the windows' earliest time) lands on a different slate.

## Fix
Fix location: prompt (and the contract if an in-fiction place is wanted). File the estimand, not the method: the population is every covered offence in the quarter, pooled across the five classes and both seasons. The occurrence time of each is unobserved within its window and is to be treated as drawn from one common hour-of-week distribution estimated from the whole record, with a window's end taken as exclusive. Say that the slot figure is the expected count under that distribution. Say in the workbook asks that sensor-fault hours are excluded from the per-trading-hour footfall. Then add to the data a separation of the candidates that the filed estimand does not already pin (for example a back-test the record supports), so that the per-class and exact-profile fits are ruled out by the files and not by the write-up. Clause 4.4 can stay if the filed estimand makes clear it bars external profiles only.
