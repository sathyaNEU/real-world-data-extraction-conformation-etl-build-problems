# leak check, task186

**Verdict: REVIEW.** 14 files read, 21 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: change, tallis, margin, routes, register, golden, standard, harbourline, changes, decisive, default, dealer, statistics, anomaly, reference, spread, ownership, detection, cross-section, examined, robust, exactly, pellow, period, cycles

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `extract_notes_2026-11-16.md`: 3 of 25 stump-paragraph terms appear (change, register, standard); read whether the document names the move
- **REVIEW** `pass_through_monitoring_standard_PM-04.pdf`: 8 of 25 stump-paragraph terms appear (change, margin, register, standard, changes, statistics); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `fuel_sales_survey_returns_2026.csv`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `station_register_2026-11-16.xlsx`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `monitored_brand_register.json`: names 7 of 8 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader 1 (isolated, Sonnet at medium effort, on prompt.txt and target/ only), on the pack before the stage 4 fixes.

1. Decisive step: none quoted. PM-04 4.1 states the selection rule and threshold, not a shortcut.
2. Ranking or scoring file: none ranks the brands on pass-through. The complaints register counted complaints by brand named (Tallis most, from having the most stations): a tally, not pass-through, but an attractor toward Tallis.
3. Hint-only file: none; every file has an organisational role.
4. Answer-like figure or name: none; the nearest was the complaints tally.
5. Filed sentences (PM-04 2.1 to 4.1) fix the population, the daily price, the margin, the windows, the examined stations, Benjamini-Hochberg at 5 per cent across every examined station and the share. Left open: the per-station test behind each p-value (one or two-sided, the test, autocorrelation). Smaller gaps named: the tax divided out or subtracted, the levy's start, the latest published rack.
6. What decides the answer: an analytical choice, the per-station test under the false discovery rate (PM-04 3.3); the cleaning is Layer 1 mess the notes explain.

Sweep verdicts: the extract notes (6 terms) harmless; the standard (11 terms) harmless; the survey returns (owner names beside litres) harmless; the station register (trading names beside numbers and dates) harmless.

Realism: eight closures on 1 April 2026 read as a batch; the weekly bulletin jumps about 7 cents in the week of 23 February 2026; the operations log lists the June renumbering after the September outage.

Ask forks: "stations it prices itself" read as company-owned sites or all of the brand's stations; the litres' brand read in each month or on 1 December 2026.

Main-thread rulings: the complaints register drops the brand column (area and category only), so it ranks nothing; the reissued references' closed stations close on dates from April to early June and their references go to stations added to the frame late, so no batch marks them; the operations log sorted and numbered by date; the bulletin's February step checked against the rack; the register's About sheet defines site_ownership flatly (who owns the site); the prompt reads "at the stations then carrying each brand"; the tax read as a 5 per cent deduction asserted to file the same call. Question 5's open test is the decisive analytical choice, as designed.

## Solver's-eye read (second pass)

Reader 2 (isolated, Sonnet at medium effort, on prompt.txt and target/ only), after the first pass's fixes.

1. Decisive step: none quoted; PM-04 4.1 is the selection rule and does not say how to test a station.
2. Ranking or pointing file: none. The bulletin is area-level, the complaints register area and category only, the brand register a plain list, the operations log the platform's.
3. Hint-only file: none.
4. Answer-like figure or name: none.
5. PM-04 2.2 to 4.1 fix the daily price, the margin, the windows, the examined stations, Benjamini-Hochberg at 5 per cent and the share; left to the analyst: the null for "would have had the levy not changed", the per-station statistic and its variance.
6. An analytical choice decides it: turning "more than the rise" into a per-station test whose false discovery rate holds; nothing planted.

Sweep verdicts: the extract notes, the standard, the survey returns and the station register all harmless.

Realism: the five-digit closed stations clustered in April to June 2026; the bulletin's late-February step; October 2026 returns fewer than earlier months; outage counts tidy.

Ask forks: the litres' brand "then" (each month or 1 January 2026); revisions; "prices itself" read as Company sites; 1 December after the export; the share's denominator.

Main-thread rulings: the closures now run from March to September 2026 under both numbering schemes; the bulletin's February step is the rack's (0.59 to 0.67 dollars a litre over 10 to 24 February); October's returns are the ones received by the 16 November pull (late returns not yet in); "then carrying" reads the month's brand and the notes file the revision rule; "prices itself" read as Company sites is the ask's device (the register's About sheet defines site_ownership as who owns the site); the share's denominator files the same bins either way (SF9, asserted).

## Solver's-eye read (third pass)

Reader 3 (isolated, Sonnet at medium effort, on prompt.txt and target/ only), after the register and notes change.

1. Decisive step: none named; PM-04 3.3 fixes the error control, not how to model the margin without the levy change.
2. Ranking or pointing file: none; the complaints register spreads evenly across months with no January spike and names no brand.
3. Hint-only file: none; the extract notes give conventions a real extract note would give.
4. Answer-like figure or name: none.
5. A literal read of PM-04 3.2 excludes the one station closed before the change (its brand ends on the register before it closed); the eleven later closures are examined under the 20-day rule.
6. An analytical choice decides it: the counterfactual margin and its test under Benjamini-Hochberg.

Realism: the levy day and the two outage-release days carry more rows (plausible); the survey's owner names in two casings (ordinary mess); trading names joining brand, town and street read slightly synthetic.

Ask forks: the litres' brand per month or on 1 January ("then" reads per month; brand changes take effect on the first of a month); the survey keyed by owner and address (the frame carries the reference); "prices itself" read as Company sites (the ask's device); shares near the one-in-ten edge (the inquiry reads the unrounded share; no brand but Tallis has a finding).

Main-thread rulings: harmless throughout; the trading-name format is left as the register writes it (no figure reads it).

## Solver's-eye read (fourth pass, prompt)

Reader 4 (isolated, Sonnet at medium effort, on prompt.txt and target/ only), on the prompt's month clause.

1. No phrase names the decisive step or how to judge "more than the rise"; the method sits in the standard.
2. No presupposition: "if any" and "or saying none" keep the outcome open; the opened-or-closed clause reads as a counting convention a requester would state and reveals neither the reused survey references nor how returns match to stations.
3. No input file, acronym, method, population rule or rate basis named.
4. Ask forks: "prices itself" (Company sites or the brand's own pricing; the ask's device, closed by the submissions' push times per both judge passes); "those litres" (the chart's litres or the priced-itself subset's).

Main-thread rulings: the prompt now says "the chart's litres"; "prices itself" stays the ask's device.

## Solver's-eye read (fifth pass, prompt)

Reader 5 (isolated, Sonnet at medium effort, on prompt.txt only), after "the chart's litres".

1. No phrase names a method; "found to have passed on more than the rise" names the outcome, not the test.
2. No presupposition names a qualifying brand, a found station or a reused identifier; the opened-or-closed clause and "then carrying" read as conventions about station turnover and brand changes the requester knows of.
3. "The chart's litres" are the memo chart's litres at the stations then carrying each brand, January to March 2026, in whole thousands; a second reading is low risk.
4. "Stations it prices itself" stays undefined in the prompt (the ask's device, closed by the submissions' push times).

Main-thread rulings: harmless throughout; nothing to fix.


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

The reader held only a fresh unzip of `target.zip` and `prompt.txt`, with the figure names (not values)
from `generator/figures.json`, and was scored by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | hit |
|---|---|
| main call | **1 of 1** |
| ask figures | **48 of 60** (80.0 per cent) |

It filed the brand and the found share. It built the decisive construction itself: each station's margin
change measured against the margin change of its own town's other stations, branded and unbranded, on a
one-sided Welch test over the daily series with Benjamini-Hochberg at 5 per cent. It reported the naive
reading, a margin change above zero, as flagging 195 of 369 stations and handing the call to the wrong
brand, which is the default path stated from the inside, and it gave the per-town drifts that make the
pooled reading wrong.

**The readability screen holds on this build, as it does on one other in this batch.** Asked what sent it
there, it said plainly that **nothing in the files states it**, that a clause's phrase "by more than it
would have had the levy not changed" suggested a counterfactual, and that it inferred the town benchmark
from the data, from the town-level pattern and the unbranded stations tracking their own town. So the pack
does not teach the method. It was landed anyway, which makes this a magnitude failure: the gap between the
pooled reading and the town benchmark was crossable by a careful reader at medium effort. The repair widens
the separation at stage 2 rather than removing a signpost.

It also found the eight reissued survey references pointing litres at unrelated stations, took the latest
return revision, handled three mid-window brand changes and a March closure, and named three distractors.
Its own caution is worth keeping: it flagged two of its found stations at about +0.3 cents as likely false
discoveries under its own 5 per cent rate, and noted the share survives dropping them.

```
call figures   1 of 1 hit
ask figures    48 of 60 hit (80.0 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```
