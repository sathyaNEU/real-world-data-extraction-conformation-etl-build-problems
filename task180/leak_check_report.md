# leak check, task180

**Verdict: REVIEW.** 16 files read, 39 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, catalogue, pfeilbrunn, record, completeness, scheme, lanzenried, decisive, method, reviewed, origin, window, earthquake, magnitude, complete, fourth, nothing, growth, ordinance, moorstetten, detection, sentence, counting, injection, federal

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `monitoring_ordinance_2026.pdf`: golden figure 0.6 appears: ...at it locates every earthquake of local magnitude 0.6 or more with an epicentre within 5 km of the open...
- **REVIEW** `tls_bulletin_2026Q3.pdf`: golden figure 120 appears: ...atalogue as at 8 October 2026. Amber is more than 120 in a quarter. Networks From 1 January 2027 the co...
- **REVIEW** `tls_scheme_2024.pdf`: golden figure 120 appears: ...Green: normal operation. 4.2 Amber: more than 120 earthquakes counted under section 3 in a calendar...
- **REVIEW** `tls_bulletin_2026Q3.pdf`: carries 7 of 10 distinctive words of the committed call: 'Pfeilbrunn will run over the traffic-light amber in the first and fourth quarters of 2027, at about 223 and 206 earthqua'
- **REVIEW** `tls_scheme_2024.pdf`: carries 8 of 10 distinctive words of the committed call: 'Pfeilbrunn will run over the traffic-light amber in the first and fourth quarters of 2027, at about 223 and 206 earthqua'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `datenabgabe_ampel_2026-10-12.md`: 12 of 25 stump-paragraph terms appear (catalogue, pfeilbrunn, record, scheme, lanzenried, reviewed); read whether the document names the move
- **REVIEW** `monitoring_ordinance_2026.pdf`: 8 of 25 stump-paragraph terms appear (completeness, scheme, earthquake, magnitude, complete, ordinance); read whether the document names the move
- **REVIEW** `operating_plans_2027.pdf`: 8 of 25 stump-paragraph terms appear (pfeilbrunn, scheme, lanzenried, complete, fourth, ordinance); read whether the document names the move
- **REVIEW** `tls_bulletin_2026Q3.pdf`: 9 of 25 stump-paragraph terms appear (catalogue, pfeilbrunn, scheme, lanzenried, reviewed, earthquake); read whether the document names the move
- **REVIEW** `tls_scheme_2024.pdf`: 10 of 25 stump-paragraph terms appear (catalogue, pfeilbrunn, record, scheme, lanzenried, reviewed); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'For each plant and each of the first three quarters of 2026 I also need, in tls_annex_2026.xlsx, its injected volume, the earthquakes of ML 1.0 or more within 5 km that our automatic system located, and the hours its net'

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

The reader held only a fresh unzip of `target.zip` and `prompt.txt`, with the figure names (not values)
from `generator/figures.json`, and was scored by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, on the reader's own words and on the ask layer

| block | hit |
|---|---|
| main call | **landed, on the reader's prose** (the scored keys read as counts, see below) |
| ask figures | **51 of 80** (63.8 per cent), already over the 35 bar on its own |

It filed the committed call in its own words, that only the one plant goes over the amber line and that it
goes over in Q1 and Q4 of the forecast year, with the other four under and the highest of them named
correctly. It then reconstructed the whole decisive route unprompted: that the reviewed catalogue is
nearly empty in the daytime at that plant, that the events appear only in a sharp local-time window which
moves with daylight saving and is therefore town noise at the surface stations, that the other four plants
show flat day and night profiles and a normal magnitude-frequency shape so their counts are already
complete, and that the rate must be taken from the quiet window over the volume injected in that window
and then applied to the full planned volume. It gave the ratio between the two bases and said in terms
that taking the published quarterly counts at face value would miss the amber, which is the default path
named from the inside.

It also cleared the whole Layer 1 layer: the month labels in the 2026 injection sheet running one month
ahead with a duplicated December row, the renamed injection well, the datalogger location-code change with
the unlisted gap between epochs, several automatic origins per event, and four distractors identified as
such. None of the mess was what made this hard, and none of it slowed the reader down.

**A scoring caveat, recorded because it cuts against the finding and not for it.** The two keys holding
the call are named for sets, and the reader answered their sizes, 1 plant and 2 quarters, both right. The
scorer therefore printed the call as 0 of 2. Its prose names the plant and both quarters, so the call is
landed; the key names were the ambiguity, and the scorer now flags this shape rather than reporting a
clean miss. The ask layer fails independently at 63.8 per cent whatever is done with the call.

```
READ AS A COUNT, so these misses are not sound: the reader answered the size of a set where
the golden holds its members, and the size is right. Read the reader's prose before scoring
the call, and rename the key or ask for the members next time.
     plants_over_amber                  golden ["Pfeilbrunn"]                 reader 1
     quarters_over_amber                golden ["Pfeilbrunn Q1 2027", "Pfeilb reader 2

call figures   0 of 2 hit
ask figures    51 of 80 hit (63.8 per cent)

FAIL  the ask layer leaks 63.8 per cent, at or over the 35 bar. Re-site the devices:
      a reader hit means the device is absent from its path, not weak.
```

The repair re-sites the ladder, not the wording. The specific finding is that the quiet-window reasoning
was reachable from the catalogue's own day-and-night profile, so the separation between the published
count and the window rate has to be widened or the profile has to stop being legible at a glance.


### A second independent reader, run on the same pack, and the stronger evidence of the two

A second reader at the same effort, holding the same pack and knowing nothing of the first, also filed the
plant and both quarters, and took **54 of 80** ask figures. It reached the construction by a different
route: it measured that the small events appear only inside a sharp local-time window while about 67 per
cent of the graded-magnitude events fall in that window against about 22 per cent at the other plants, and
that the share falls as magnitude rises and is gone by about ML 1.8. It gave the rate on the window, the
all-hours rate and their ratio, and it checked its own answer by recomputing on one year alone and
reporting the call unchanged.

**It corrects the first reader's account of why, and in the build's favour.** Asked what told it to take
the step, it said **no sentence in the files names it** and that it inferred the step from the hour-of-day
pattern in the catalogue, listing the ordinance and scheme sections only as supplying the setting. So this
build's readability screen holds, as task181's and task186's do, and the failure is magnitude: the
day-and-night profile is legible enough that two independent readers crossed the gap unaided. The line
above about the profile being reachable at a glance stands; the implication that the pack signposted the
step does not.

Two readers landing the same call independently is the strongest Gate F evidence on the lane, and it also
makes the repair clear: the profile has to stop being the thing a reader notices first.
