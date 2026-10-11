# task229 design note

Seed DQ02 (whether the release-health alert fires on this week's build, when the metric is the
average user's rate). The seed's pairing was product-analytics; task228 is being built the same day
in the same objective inside the product-analytics experiment-platform world, so this build keeps the
seed's Layer 2 pitfall and objective and moves the world to a smart-meter metering data provider,
where the object under analysis (interval data delivery) is the health of the data itself.

## DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | Energy Systems & Utilities / other (smart-meter interval data delivery quality, the metering data provider's read performance; the client list carries no energy task type that serves Data Quality Monitoring) |
| Objective | Data Quality Monitoring & Alerting |
| Niche | a smart-meter data provider's read-health gate on the communications-module firmware builds live in its fleet, deciding which builds the read-health alert fires on before the next rollout wave |
| Shape | 10 scorecard against thresholds: eight builds, each with its assessed installations, read health, lower limit and fire or hold, plus the wave's exposure and the week's upgrade-night cost |
| Decision type / unit | designation_set (which builds the alert fires on) / set_of_items |
| Gap / pattern / generators | population (decisive: the unit the standard scores is the installation that ran the build all week, the file grain is the register-day delivery), time (the delivery cut-off as of which a read counts); pattern D (two grains, both flawless); G2 grain mismatch, G7 operating window, G17 statistical rigor |
| Gate G mechanism | signal_vs_noise_or_hold (which builds sit below the reference by more than their own noise; five of eight hold) |
| Stump strategy | grain_or_unit; decisive rule filed (the read-health standard defines the measure and its limit); no official decoy; no validated decoy; no calibration organ |
| Layer 2 | estimation_fit, `product-analytics/metric-definition-measurement-science/2` (ratio of sums is not mean of ratios; the limit follows the unit), made this build's own: the heavy unit is a 5-minute, three-register installation that files eighteen times a 30-minute single-register household's reads, and the build's error has to come from installation-to-installation spread |
| Layer 1 | interval reads with quality codes at mixed 5, 15 and 30 minute resolution; register-days re-delivered when a later retrieval completes them; receipts in UTC, market time in AEST, field times in AEDT, against a filed cut-off; firmware build codes spelled three ways across the head-end, the rollout schedule and the MDM; effective-dated meter-to-installation assignments with mid-week exchanges; head-end events replayed after a failover and failed activations rolled back |
| Calibration form | none, because the strategy is a stated rule whose construction is the work; no closed corpus is needed or shipped |
| Context artifact | monitoring_export (the MDM interval receipt extract) |
| Stakeholder | metering data services lead, who owns the read-health alert the rollout desk gates each wave on |
| Forum / forcing event / org family | operations_desk (the rollout desk holds the wave for any build the alert fires on) / cutover_or_migration (Wave 8 of the firmware migration goes out on Tuesday night) / utility_or_infrastructure |
| World | Halvane Metering, an accredited metering provider and metering data provider in the National Electricity Market, New South Wales, AUD; personas drawn with `guard.py names --locale en_AU --seed 229` |
| Deliverables | `wave8_read_health_alerts.json` (the alert payload the routing system ingests: commits), `read_health_by_build_wk41.png` (reads at a glance) |
| Guard | PASS (WARN repeat.deliverables cleared by moving to json plus png, a set the batch has not used); NOTE same_puzzle_older against task98 v3, differentiated on the card; nearest driver 0.06 (task87 v3) |

**Coordination with task228.** Drawn the same day in the same objective. task228 holds the
product-analytics experiment-platform guardrail world; this build differs in domain (energy
utilities), organisation (a metering data provider), forum (the rollout desk), forcing event (a
firmware migration wave), geography (New South Wales), personas (en_AU draw), data structure
(register-day deliveries of interval counts by quality flag, with an activation history) and
stump strategy (grain_or_unit with a limit that follows the unit).

**Data-native sentence.** A metering data provider's fleet mixes 30-minute single-register
household meters with 5-minute three-register installations (solar export and controlled load, or
small commercial sites) that file up to eighteen times as many interval reads a day, and its
communications firmware fails in ways that hit one profile and not the other; so on this fleet the
pooled share of interval reads and the average installation's share are different measures of the
same week, and the record-count error a pooled share invites is a fraction of the installation-level
noise, which is exactly the shortcut a capable analyst takes on interval data.

**Why every element is real.** NEM metering data providers deliver interval data with quality flags
(actual, substituted, estimated) by register (data stream suffix) and day, re-deliver a day when a
later retrieval recovers the reads, work in market time (AEST, no daylight saving) while field crews
and the head-end log local or UTC time, and roll communications firmware out in waves with a
go/no-go per build.

## Stump sentence

A competent solver builds each firmware build's read health from the MDM receipts as the share of
all expected interval reads that came in actual, keeps the latest delivery of each register-day,
counts every installation on the build it ends the week on, and sets the limit with the binomial
error on those reads: it fires the alert on EM3.10.9, EM3.12.2, PX5.3.0 and PX5.3.1 and holds
EM3.12.1, PX5.2.7 and EM3.12.0. The step that carries the stump is the unit and its error: the
standard scores the average installation that ran the build all week, so the 5-minute three-register
installations that file about three quarters of PX5.3.0's reads count once each (PX5.3.0 holds at
99.49 against a limit of 99.36, where pooled reads put it at 98.49), EM3.12.1's degraded 30-minute
households stop hiding behind its healthy 5-minute sites (98.99 against 99.33, where pooled reads
clear the reference at 99.58), and the limit comes from installation-to-installation spread, which
is several times a read-count error, so EM3.12.0 (99.43 against 99.37) and the 37-installation
PX5.3.1 pilot (98.96 against 96.83) hold. With the reads held at the 06:00 cut-off and only the
installations that ran the build all week, the alert fires on EM3.10.9, EM3.12.1 and PX5.2.7 and the
other five hold.

## Gate G

- **Litmus.** No reported number or stakeholder conclusion is overturned. The pack carries no
  read-health report, no scorecard and no ranking of the builds; the MDM receipts, the head-end
  history and the register are correct records of what happened. The one belief in the prompt (the
  desk expects PX5.3.0 to be pulled because its commercial sites are the ones retailers chase) is true
  about those sites and is a belief about the call, not a figure. The difficulty is constructing the
  measure the standard defines from register-day deliveries: the unit, its error, the population and
  the version. Answer: no.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Primary mechanism:** signal_vs_noise_or_hold (which builds sit below the reference by more than
  their own installation-level noise), with `statistical_rigor` support (the error that follows the
  unit). The unit itself is Pattern D, two grains both flawless.
- **Deletion test.** Nothing in the pack is wrong; there is nothing to delete. Still hard because the
  pooled read and the installation average are both arithmetically perfect and disagree in both
  directions on this fleet.
- **Clean-data test (asserted).** Drop every delivery after its cut-off and every installation that
  did not run its build all week (the two population and version rungs repaired): the pooled
  read-count pipeline still fires EM3.10.9, EM3.12.0, PX5.2.7, PX5.3.0 and PX5.3.1, and with an
  installation-level error it still fires PX5.3.0 and holds EM3.12.1. The decisive rung survives a
  perfect instrument because no instrument is lying: the heavy installations really do file eighteen
  times the reads.
- **Lens-swap test.** The naive reading and the answer are not one population at one moment: the
  naive reading takes 7,930 installations on their end-of-week build with the latest deliveries; the
  answer takes the 6,729 that ran one build all week, with the deliveries held at each day's cut-off,
  and four constructions separate them (asserted: the populations differ by 1,201 installations).
- **Forward framing.** The measure is of the week just closed, which is what the standard scores;
  the decision is forward (Wave 8 moves nothing onto a build the alert fires on). A Data Quality
  Monitoring call is a gate on the next action, and its evidence is the last complete window by
  design, which is the reason the ask is not a forecast.

## The decisive move, and why it survives the opponent

1. **Written in no sentence.** The standard defines the installation's read health and says a build's
   read health is the mean over its assessed installations, and that the limit is three standard
   errors of the build's read health. Nothing says that the installations differ eighteen-fold in the
   reads they file, that pooled reads and the installation mean disagree, or that the standard error
   of a mean of installation shares is their spread over the square root of their number. The
   construction (per installation, over every data stream and day, from the cut-off version, then the
   mean, then the spread) is the work.
2. **No sweepable corpus.** There is no prior read-health report, no published figure, no closed
   corpus; nothing nominates a method.
3. **No arithmetic symptom.** Pooled reads reconcile to the receipts exactly; every register-day
   carries a full day of intervals; the pooled figure and the binomial error are complete, plausible
   and internally consistent.
4. **Not a per-row predicate.** It needs a group (installation), a share per group across streams and
   days, a mean across groups, and a spread across groups.
5. **Enumeration is arithmetic.** The assessed population comes from an effective-dated register and
   an activation history; the unit from a group-by the row grain does not carry.
6. **No cutover date.** Wave 7 is dated and sits on the decoy side: counting its movers fires
   EM3.12.2, and an event-study read of the week shows the movers' upgrade-night loss, which is real
   and is not what the standard scores.
7. **Survives the deletion** (above).

## Layers

- **Layer 1 (the realistic mess and the system that produces it).** MDM interval receipts at
  register-day by delivery grain with A, S and F quality counts at 5, 15 and 30 minute resolution; a
  later delivery replaces the register-day (real MDM behaviour when a retrieval recovers reads); UTC
  receipt stamps against a market-time (AEST) cut-off, while the register and the schedule are in
  local time (AEDT since 4 October); the head-end history as nested JSON with staging, failed
  activations, rollbacks, decommissioning and events re-stored after a failover; HES image ids that
  the catalogue maps to release names and the schedule spells a third way ("EM3 12.0"); NMIs with and
  without the checksum character; meter serials that lost their leading zeros in the register where
  the old CIS migrated them as numbers. Every piece is what these systems export.
- **Layer 2 (the analytical shortcut).** Pooling interval reads (a ratio of sums) when the standard
  scores the average installation, and taking the error of that pooled share from the read count. An
  expert in measurement recognises both: the pooled share is carried by the heaviest installations,
  and the reads of one installation are not independent draws, so the error belongs to the unit the
  measure averages.

## Ladder (asserted by name in `generator/checks.py`)

Answer: fire on {EM3.10.9, EM3.12.1, PX5.2.7}, hold on the other five.

| Rung | Reading | Fires on | Killed by |
|---|---|---|---|
| R0 natural pipeline | latest delivery per register-day, every installation on its end-of-week build, pooled reads, binomial error on reads | EM3.10.9, EM3.12.2, PX5.3.0, PX5.3.1 | 3.5 (read held at cut-off) |
| R1 | + the delivery held at the 06:00 cut-off | EM3.10.9, EM3.12.0, EM3.12.2, PX5.2.7, PX5.3.0, PX5.3.1 | 3.6 and 3.7 (assessed installation) |
| R2 | + only installations that ran the build all week | EM3.10.9, EM3.12.0, PX5.2.7, PX5.3.0, PX5.3.1 | 4.2 (the average installation) |
| R3 | + the mean of installation read health | EM3.10.9, EM3.12.0, EM3.12.1, PX5.2.7, PX5.3.1 | 5.2 (standard error of the build's read health, over its installations) |
| R4 | + the error from installation-to-installation spread | **EM3.10.9, EM3.12.1, PX5.2.7** | answer |

- "A solver who does everything right up to R3 commits to firing EM3.12.0 and the PX5.3.1 pilot as
  well": the read-count error is 0.006 percentage points on EM3.12.0's 1.6 million reads against an
  installation-level 0.044.
- Satisfying to stop at: R0 is the dashboard number every MDP reports; R1 is what a careful analyst
  who read the cut-off clause files; R2 is the clause-by-clause reading of the population; R3 is a
  correct mean with the error a proportion invites.
- Every rung names a different set (asserted). The decisive pair is R2 to R4, the seed's pitfall:
  the unit, and the limit that follows the unit.
- **Position.** For a set answer the analogue of rank is how many of the eight calls a rung gets
  right: R0 3 of 8, R1 4, R2 5, R3 6, R4 8. No intermediate rung lands the call.
- **Discriminator dominance.** PX5.3.0: pooled 98.49 against limit 99.36 (fires by 0.87); average
  installation 99.49 against 99.36 (holds by 0.14). EM3.12.1: pooled 99.58 (above the reference
  itself); average 98.99 against 99.33 (fires by 0.34). The heavy installations are 15 per cent of
  PX5.3.0's installations and about 73 per cent of its reads, and 22 per cent of EM3.12.1's
  installations and about 77 per cent of its reads.
- **Grid (asserted cell by cell).** 3 versions (cut-off, latest, first) x 3 populations (whole week,
  start-of-week build, end-of-week build) x 4 units (installation, pooled reads, register-day rows,
  data streams) x 4 errors (installation spread, binomial on reads, binomial on installations, none)
  = 144 cells. Exactly two land the call: the standard's reading, and the same reading on the first
  delivery of each register-day, which moves every build's read health at two decimals (8 of 8) and
  so fails the scorecard. Every other cell files a different fire set and violates a named clause
  (3.5, 3.6 and 3.7, 4.2 or 5.2).
- **Sign discipline, margins.** Every build sits at least 0.05 percentage points from its limit and
  every pair of builds' distances to their limits differ by at least 0.04 (the payload's order is not
  a near tie). Every two-decimal figure sits at least 0.0015 from its rounding edge (asserted).

## Closure table (determinism-check, the 22 axes)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | installations whose meter ran the build all week | filed (3.7, 3.6); readings by start or end build are grid cells |
| 2 | Unit of account | the installation | filed (4.1, 4.2); rows, streams and reads are grid cells |
| 3 | Attribution window | market days 5 to 11 October | filed (3.2); the receipts carry only those read dates |
| 4 | As-of dating | the meter's build at the week start, no activation inside the week | filed (3.6, 3.7) |
| 5 | Version basis | latest delivery received before the cut-off | filed (3.5); first and latest are grid cells |
| 6 | Denominator | every interval of every data stream | filed (3.3); each row's A+S+F is a full day (asserted) |
| 7 | Weighting | equal per installation | filed (4.2) |
| 8 | Window length | one week | filed (3.2) |
| 9 | Boundary inclusivity | received before 06:00; fire when strictly below | C1: no delivery lands within 8 minutes of a cut-off; no build within 0.05 of its limit |
| 10 | Rounding path | compute unrounded, report two decimals | filed (7); every figure clear of its edge |
| 11 | Tie-break | none needed | C1: no ties in the order (distances 0.04 apart) |
| 12 | Maturity | the week is closed and every cut-off has passed | C1: the extract is after Sunday's cut-off |
| 13 | Order of operations | share per installation, then mean | filed (4.1, 4.2) |
| 14 | Row order | any | C1 |
| 15 | Duplicate resolution | head-end events by event id; deliveries by the cut-off rule | C1 for the population (replays change no assessed installation, asserted); filed for deliveries |
| 16 | Identity | NMI to 10 characters, serials to 8 digits | C1: the joins have one answer once normalised |
| 17 | Netting | not applicable | none |
| 18 | Dimensional units | interval counts only | C1: kWh totals are never used |
| 19 | Code semantics | A is a read; S and F are not; a rolled-back activation is not a move | filed (3.5, 3.6) and the field reference |
| 20 | Integerisation | counts are counts | C1 |
| 21 | Scope of a clause | the standard governs the alert; the Wave 7 and Wave 8 asks are defined in the prompt | prompt wording |
| 22 | Forward window contents | Wave 8 moves if it goes ahead, on the schedule as cut | prompt wording ("if it goes ahead"), decoupled from the call |

Standard deviation divisor: pinned (7, sample standard deviations); the n divisor moves only the
37-installation pilot's limit at two decimals (asserted).

## Ask sheet (supplemental-stumping)

Main row population: the receipts of the 6,729 assessed installations on read dates 5 to 11 October,
their meters' head-end histories up to the week start, and their register rows. Zero mover, exchange
or schedule rows inside it (asserted).

| Ask | What it is in the decision | Primary device | Stops (asserted) | Named use |
|---|---|---|---|---|
| A. Wave 8 moves onto EM3.12.2 and PX5.3.1 if the wave goes ahead | the exposure beside each go/no-go | D2 a schedule cut on 1 October before 37 + 9 meters went in Wave 7 and 22 were exchanged out; D7 serials that lost their leading zeros on batch A; D1 rows re-batched onto B and left on A (16 + 5), with blank NMIs on a third of batch A punishing a dedup on NMI | rows 1,349 / 123; distinct rows 1,339 / 119; one per NMI cell 1,134 / 103; answer **1,274 / 109** | the desk sizes field support and Settlement's substitution load for the night |
| B. Wave 7 moves this week: installations moved onto EM3.12.2 and PX5.3.1 and the interval reads they were missing at the cut-off on the market day they moved | the audit trail of what a wave costs, which the desk weighs beside the alert | D8 the move day in market time (UTC stamps, AEDT local nights from 23:30); D1 events re-stored after the 7 October failover; D5 41 meters that failed on Tuesday, rolled back and moved on Wednesday, and 29 exchanged meters commissioned on EM3.12.2 that no wave moved | UTC day 2,808 / 332; AEDT day 20,040 / 1,072; latest deliveries 16,232 / 926; answer **1,109 installations, 16,415 reads / 63, 933** | Settlement Operations carries the substitutions |

Both asks run on rows the main call never reads (movers, exchanges, the schedule). Chart parts: one
row per build in the payload's order, the point, the limit marker, the reference line with its value,
the firing builds named, the title naming them.

**Pair arithmetic.** A response that lands the call keeps the scorecard (32 figures) and the chart and
loses what the devices take from the six ask figures; a response that misses the call on the unit or
the error is wrong on every build's read health or every limit, so it keeps little beyond the counts
of assessed installations it got right. The ask layer is thin by count (six figures plus the chart)
and the scorecard is coupled to the main construction by design, so the build leans on the main call
staying missed: the worth-it gate in the solver round is the test of that.

## Shape and criteria

Shape 10: eight builds x (assessed installations, read health, lower limit, fire or hold) = 32, plus
the fire and hold lists, the order, Wave 8 (2), Wave 7 (4) and the chart parts (6): about 46.

## Realism debts

- 2,242 installations on one build and 37 on the pilot is the shape of a real fleet mid-migration.
- PX5.3.0's heavy installations lose about 1.8 per cent of their reads to a firmware profile issue;
  that is a large defect for 5-minute sites and is what makes retailers chase them, which is the
  belief the prompt reports.

## Stopping rule

At ceiling if the portal's top two land the call; licensed one repair if the top two miss the call
but the asks leak above a fifth each.

## Build record

- Generator: `generator/make.py` builds the pack (`build.py`), the goldens from the shipped bundle
  alone (`deliver.py` over `golden.py`), `metadata.json`, runs `checks.py` (74 assertions: the five
  rungs by name, the 144-cell grid, the convergences, the deciding contrasts in both directions, both
  asks' stops, chronology, separation, the gates, single statement of the reference and the cut-off)
  and the independent `verify.py` (standard library and openpyxl, no shared code), builds a second
  time into scratch and requires byte-identical target and golden files, then cuts `target.zip`
  (flat, ten members). Texture salts per build were chosen by `tune.py` so every two-decimal figure
  sits at least 0.0015 from its rounding edge and every build at least 0.05 from its limit; the
  design parameters did not move.
- Input gates: 10 files; csv, json, md, pdf, xlsx; the MDM receipts carry 94,384 rows; distractors
  `hes_firmware_census_20261012.csv` (the head-end's inventory by image and status, which counts
  removed and bench meters and every mover on its new image) and
  `carrier_maintenance_notices_oct2026.xlsx` (the carrier's IoT maintenance windows), both named in
  `metadata.json` and asserted unused by the golden.
- Surface screen (`guard.py surface`): 0 promoted pairs, nearest surface 0.10; no persona of another
  build in the cut pack. Heart check: PASS, nearest driver 0.06 (task87 v3), nearest stump 0.05.

## House fixes and realism (reduce-house-fixes, golden-realism)

- H1: the standard's PDF is written invariant and stamped 24/06/2026 with the owner as producer;
  `scrub_producer_metadata.py` audits the target clean; workbooks carry their owners and in-fiction
  dates. Goldens are script output (matplotlib, json) and are left as such.
- H2, H3: every figure in `submission.md` is printed by `golden.py` and re-derived by `verify.py`;
  the steps cite clauses rather than restating figures.
- H4: `target.zip` members equal the ten declared files, no enclosing folder; the chart was opened
  and read after rendering.
- H12: one convention sentence (percentages to two decimals, counts whole) carries every figure.
- H13: the call is the last sentence of the context; each later paragraph ties back to it.
- H16: no meter runs an image before its release date and no event postdates the extract (asserted);
  the standard (effective 01/07/2026) predates every document that cites it.
- H18: Wave 8's moves are the exposure each go/no-go releases; Wave 7's move-night cost is what a
  hold costs Settlement Operations if the wave proceeds. Both sit on rows the main call never reads.
- H20: the prompt names the comms firmware rollout, interval reads, installations, the market day
  and the retailers chasing missing data, which place the request with a metering data provider.
- H21: the invented organisation is Halvane Metering (first drafted under a name that sat on a
  common Australian business word, renamed in the generator); suburbs and postcodes are real NSW
  places used as texture.
- golden-realism: payload carries an alert id, the week, the routing list, notes sourced from the
  standard's own clauses, two-decimal percentages; the chart uses the validated categorical blue for
  holds and the reserved critical red for fires, with a FIRE label beside every red mark, ink-coloured
  text, a title stating the call and the reference line labelled with its value.

## Leak check (stage 4, mechanical half)

`leak.py --asof 2026-10-12`: REVIEW (no LEAK after renaming the schedule workbook off `_v2` and
dropping the reference figure from block 4). Each REVIEW line:

- `mdm_interval_receipts` "16,415": two adjacent CSV fields (`QTY_F` 16, `DAY_TOTAL` 415.054) read
  as one number; harmless.
- The standard "carries 6 of 6 distinctive words of the committed call": the words are read-health,
  alert, fire, hold and the like, which the standard defines; it names no build; harmless.
- The standard and the field reference carry generic stump-paragraph words (installation, standard,
  deliveries, average, measure, quality, receipts, head-end); these are the documents' own subject
  matter and neither says that the installations differ in volume, that pooled reads and the average
  disagree, or how the standard error is formed; harmless.

## Tried and rejected

- Keeping the seed's product-analytics crash-rate world: a per-user crash rate is a product health
  metric, not the health of data or of a pipeline, so the build would retag as Anomaly Detection
  without changing a word; and task228 holds product-analytics in this objective on the same day,
  so the pairing would block on `ban.pairing` at the heart check.
