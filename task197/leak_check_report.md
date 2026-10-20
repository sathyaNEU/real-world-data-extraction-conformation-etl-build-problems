# leak check, task197

**Verdict: REVIEW.** 18 files read, 37 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: second, clause, traverse, window, archive, published, extract, seconds, deviation, measured, inside, population, carries, sentence, boundaries, boundary, nothing, period, recording, asserted, device, zwartewater, printed, operator, decisive

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `operator/fcr_group_availability_2026-09.pdf`: 5 of 25 stump-paragraph terms appear (second, seconds, deviation, measured, operator); read whether the document names the move
- **REVIEW** `operator/fcr_technical_conditions_2026.pdf`: 8 of 25 stump-paragraph terms appear (second, clause, published, seconds, deviation, inside); read whether the document names the move
- **REVIEW** `standards/reserve_performance_standard_v4.pdf`: 9 of 25 stump-paragraph terms appear (second, window, published, seconds, deviation, inside); read whether the document names the move

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


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

The reader held only a fresh unzip of `target.zip` and `prompt.txt`, with the figure names (not values)
from `generator/figures.json`, and was scored by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | hit |
|---|---|
| main call | **0 of 4, the call MISSED** |
| ask figures | **24 of 49** (49.0 per cent) |

**The call held.** The reader filed a different site at 57 per cent of contracted gain on 152 episodes, against a golden of a different site at 72 per cent on 134. All three figures wrong, and it put its own confidence at about 85 per cent on the site, so it was confidently wrong, which is what a working ladder looks like.

**The ask layer did not hold**, at 24 of 49, which fails Gate F on its own. So this build needs the rubric repair and not a re-root: the main recommendation side is sound and must be frozen.

Worth keeping for the repair: the reader named the two choices it knew could move its answer, treating a capacity-reduction event as a full withdrawal and using the programme as a step baseline, and it left out the forcing and ladder keys saying they looked like alternative or wrong-method calculations it had not run. It also cleared the whole Layer 1 layer, the interval-end timestamps, one site metered in kWh, a site with two metering points joined mid-window, 258 duplicate seconds in a restored archive, and the cancelled event-log corrections.

```
== call figures ==
miss call_episodes                      golden 134                        reader 152
miss call_gain                          golden 72                         reader 57
miss call_name                          golden "Kampvliet"                reader "VKF-RDL"
miss call_site                          golden "VKF-KPV"                  reader "VKF-RDL"

== ask figures ==
HIT  as_of                              golden "2026-10-13"               reader "2026-10-13"
HIT  constants.deadband_mhz             golden 10                         reader 10
HIT  constants.full_activation_mhz      golden 200                        reader 200
HIT  constants.qualify_over_hz          golden 50.08                      reader 50.08
HIT  constants.qualify_secs             golden 15                         reader 15
HIT  constants.qualify_under_hz         golden 49.92                      reader 49.92
HIT  constants.span_hz                  golden 0.19                       reader 0.19
HIT  constants.tolerance_pct            golden 90.0                       reader 90
HIT  counts.auction_results             golden 126                        reader 126
HIT  counts.commitments                 golden 256                        reader 256
HIT  counts.dictionary                  golden 15                         reader 15
HIT  counts.event_log                   golden 52                         reader 52
HIT  counts.freq_1s                     golden 111454                     reader 111454
HIT  counts.freq_min                    golden 30240                      reader 30240
HIT  counts.imbalance_prices            golden 2016                       reader 2016
HIT  counts.metered                     golden 18144                      reader 18144
HIT  counts.prequalification            golden 13                         reader 13
HIT  counts.programme                   golden 18144                      reader 18144
miss down_low_gain                      golden 73                         reader 70
miss down_low_name                      golden "Kampvliet"                reader "VKF-KPV"
miss down_none_name                     golden "Meppelerdiep"             reader "VKF-MPD"
miss episodes_total                     golden 911                        reader 274
miss exact.VKF-DLK                      golden 93.14997                   reader 90.99
miss exact.VKF-HGZ                      golden 88.079998                  reader 74.95
miss exact.VKF-KPV                      golden 72.109951                  reader 68.49
miss exact.VKF-MPD                      golden 97.059985                  reader 78.69
miss exact.VKF-NWV                      golden 90.939998                  reader 91.47
miss exact.VKF-OOS                      golden 94.88999                   reader 95.74
miss exact.VKF-RDL                      golden 82.860041                  reader 57.41
miss exact.VKF-TRB                      golden 101.130036                 reader 76.81
miss exact.VKF-ZWT                      golden 98.859863                  reader 99.39
miss exact_down.VKF-DLK                 golden 92.069996                  reader 93.18
miss exact_down.VKF-HGZ                 golden 86.880042                  reader 78.93
miss exact_down.VKF-KPV                 golden 73.119956                  reader 69.89
miss exact_down.VKF-NWV                 golden 89.089967                  reader 81.51
miss exact_down.VKF-OOS                 golden 95.840012                  reader 89.89
miss exact_down.VKF-RDL                 golden 80.860001                  reader 80.93
miss exact_down.VKF-TRB                 golden 98.13985                   reader 103.33
miss exact_down.VKF-ZWT                 golden 93.910009                  reader 91.58
HIT  exposure_above_total               golden 114.4                      reader 114.4
HIT  exposure_below_total               golden 242.6                      reader 242.6
HIT  gap_pp                             golden 11                         reader 11
miss runner_gain                        golden 83                         reader 68
miss runner_name                        golden "Reiderland"               reader "VKF-KPV"
miss runner_site                        golden "VKF-RDL"                  reader "VKF-KPV"
miss sites_outside_tolerance            golden 3                          reader ["VKF-HGZ", "VKF-KPV", "VK
HIT  tolerance                          golden 90.0                       reader 90
HIT  window_from                        golden "2026-09-21"               reader "2026-09-21"
HIT  window_to                          golden "2026-10-11"               reader "2026-10-11"

call figures   0 of 4 hit
ask figures    24 of 49 hit (49.0 per cent)

FAIL  the ask layer leaks 49.0 per cent, at or over the 35 bar. Re-site the devices:
      a reader hit means the device is absent from its path, not weak.
```
