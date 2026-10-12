# task185 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task185.json`, architecture v1, drawn 2026-10-12 from seed AD08 (a
  heat-index cover priced off one weather station with a break). The world, the decision and the quantity are the
  seed's; the pitfall is re-found from the station record.
- **Pairing:** General Statistics & Data Science, exploratory data analysis and distribution assessment (primary;
  the task type serves Anomaly Detection & Diagnostics in the taxonomy). Secondary domain Physical & Environmental
  Sciences, whose own Layer 1 technique (station histories with moves and instrument swaps, documented in station
  metadata) supplies the record's mess. Objective: Anomaly Detection & Diagnostics, a real event (the warming in the
  station's heat days) separated from an artifact (the 1995 change of instrument and screen).
- **Niche:** Southward Mutual, an agricultural mutual insurer, quotes Merrin Valley Winegrowers Co-operative its
  vineyard heat-day cover for the 2027/28 season. The cover pays per hectare on the days from 1 December to the last
  day of February whose maximum at Merrin Flat reaches 35.0 C (heat days, after a deductible) and 40.0 C (severe
  heat days). Merrin Flat went automatic on 1 November 1995: an electronic probe in a small plastic shield replaced
  the glass maximum thermometer in the large wooden screen, and the glass was read beside it until 30 April 1998.
- **Forcing and forum:** the co-operative's cover renews on 1 November 2027 and the quote is due to it first
  (`purchase_order_or_contract`, `customer_or_counterparty`); the organisation is a `financial_institution`; the
  stakeholder is the mutual's weather portfolio manager (`portfolio_manager`).
- **Call:** the premium per hectare for the 2027/28 season, with the season's expected heat days and severe heat
  days on the present instrument's basis.
- **Shape 14** (cuts by segment: each cut per segment). The quote cuts the 2027/28 schedule by the co-operative's four
  sub-districts (member blocks, insured hectares, premium) and the cover's own record by season since it began
  (claims paid and what they came to). Criteria arithmetic: the call and its two expected counts (3), the critical
  components (glass-era days the present probe would have counted over each trigger, the heat-day line's slope: 3),
  the sub-district cut (4 sub-districts by 3 figures: 12), the season cut (8 seasons by 2 figures: 16), the chart's
  named parts (4), the files and units (3): 41. Shape 08 (the replay of the terms on past seasons) was the draw's
  first label; the replayed seasons sit in the call's own population, where no ask device may live, so the cuts moved
  to rows outside it.
- **Strategy and mechanism:** `population_selection` (the conversion estimated on the days like the one being
  converted, not on all days); gap rule over population (the manual's basis, each past day as the present instrument
  would have recorded it, selects a conversion sized at each reading once the paired readings show the difference
  grows with the reading); G16 then G14; Gate G `method_or_model_selection`; calibration `parallel_run_overlap` (the
  station's own two and a half summers of paired readings and the network's comparison programme at other sites).
- **Data-native sentence:** the small shield heats on still, sunny afternoons, so the probe reads the same as the
  glass on ordinary days and runs warmer only on the hot ones, and the glass register was kept to the half degree, so
  the change is invisible in the mean, invisible against neighbours that changed in the same rollout, and invisible to
  any single offset: only a conversion sized at each reading carries the 34.5 C days over 35.0 C and the 39.0 C days
  over 40.0 C while leaving the 34.0 C and 38.5 C days where they were.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 17 builds): 25 and 28 a second-source
  inflow and a reachable share; 33 forward yield cut by an intervention; 48 a two-sided grain; 54 exposure while in
  custody; 68 a matched panel through identity successions; 76 a look-back class with zero conversion; 85 a unit's own
  observation window; 103 a fan-out through authorisations; 104 a self-adapting scorer replayed at another setting;
  119 waits a unit could shorten; 182 a lagged response to a shared driver; 183 repeat failers in parts; 125 a
  recruitment filter's carried difference; 180 detection by the quiet hours; 181 crossings of moving units; 184 host
  stand-down crowd-out. None sizes an instrument change by the reading, none turns on a threshold count whose trend a
  changeover step inflates.
- **Guard:** WARN `overuse.objective` (Anomaly Detection in 4 of the last 12): the lane is Anomaly Detection, and the
  mechanism, domain and shape are each new to it (General Statistics & Data Science has never carried an Anomaly
  Detection build; shape 08 is not in the last 12). The older signature (gap rule, G16, quantity figure) is task80 v2
  only, differentiated on the card: a time rule executed over records there, a distributional estimate here.
- **Sources:** the seed (AD08) gives the world and decision, its hold-on-tolerance design is not used (a filed
  tolerance applied to a size is rule application); the client's distribution-assessment techniques (outliers on the
  right scale, stratify before a correlation) teach that the distribution's shape, not its centre, decides, and this
  build moves that to a paired-instrument difference whose shape is reading-dependent; the client's Physical &
  Environmental Sciences technique 1 (station histories, changes documented as real networks do, never hidden to make
  a step) sets the rule that the change is documented and only its size at the reading is the analysis.

## Default path

1. Read the pricing manual: the record is Merrin Flat's daily maximum from the 1965/66 season to 2026/27, each day as
   the present instrument would have recorded it; heat and severe heat days counted per season; a least-squares line
   per count against the season's year, each season detrended to 2027/28; the cover's 2027/28 terms applied season by
   season; the burn loaded by the manual's factor.
2. Join the glass register (old station number, one sheet per year) to the automatic station's daily file (new
   number) through the station register; keep approved readings.
3. Read the station history: the 1995 change to the probe in the small shield, with paired readings to April 1998.
4. Bring the glass era to the probe's basis with the comparison readings' mean difference, probe minus glass, +0.13 C
   at Merrin Flat (+0.25 C on summer days); no half-degree reading crosses 35.0 C or 40.0 C, so the glass era's counts
   stand.
5. Count heat and severe heat days per season, fit the two lines, detrend, replay the terms, average and load.

Ends on: $567 a hectare, the raw record's premium, assuming 17.2 heat days and 4.5 severe heat days, with the
heat-day line rising 0.74 days a decade.
Golden: $525 a hectare, assuming 16.7 heat days and 4.1 severe heat days, with the heat-day line on the present basis
rising 0.30 days a decade.

## Stump sentence

The default path converts the glass era with the comparison readings' mean probe-minus-glass difference (+0.13 C,
+0.25 C on summer days), which moves no half-degree reading across 35.0 C or 40.0 C, so the 1995 step stays in the
heat-day line and it ends on $567 a hectare, the raw record's premium; a solver who sizes one hot-day offset moves the
34.5 C days but not the 39.0 C days ($542), or the 34.0 C days as well ($506).

## Three rules

- Task type: general-statistics-data-science / exploratory-data-analysis-distribution-assessment, which serves
  anomaly-detection; the decisive step assesses the distribution of a paired-instrument difference across the range
  of the reading.
- Domain test: the deciding quantity is the probe-minus-glass difference as a function of the glass reading (a
  reading-dependent shift, estimated conditionally or by quantile matching), which distribution assessment estimates
  and a location summary misses.
- Swap: rewrite the call with a blood-pressure cuff replaced mid-record and hypertension days, and the setting survives,
  as it does in a methods domain; swap the method, the mean difference or one pooled hot-day offset for the
  reading-dependent conversion, and the call moves ($567, $557, $542 or $506 against $525).
- Layer 1: the two station numbers joined through the network register (the network renumbers a site when it goes
  automatic); the glass register as one wide sheet per year, days by months, with the observer's header block (how the
  network digitised paper registers); half-degree glass readings (the observers' practice, stated in the station
  history); provisional and approved automatic readings overlapping for the months after the latest approval run
  (outside every cover window); neighbour stations' monthly series with gaps and their own changes; the term sheet's
  history of deductible and day rates by season; the co-operative's member schedule with endorsements and
  cancellations. None is placed to be caught.
- Layer 2: estimation_fit, the conversion between instruments estimated at each reading because the paired difference
  grows with the reading and the record is rounded to the half degree.
- Decisive step: sizing the conversion at each reading is a choice of estimator for a documented change, not catching
  a plant (the change and its paired readings are filed as the network files them), not reading a field (every field
  is read the same on both routes) and not applying a rule (the manual states the basis, never the method).
- Not semantics: every field, unit and code is read the same on the easy route and the golden one (the half-degree
  register, the two station numbers, the 09:00 day, the approved flag); a reader who reads them all correctly and
  converts by the average difference still quotes the raw record's premium, $567.
- Not rule application: the manual states the basis (each day as the present instrument would have recorded it) and
  the counting, line, burn and loading, but no filed rule says how to size the conversion; executing every stated
  rule with the average conversion still files $567.
- Analyst test: a strong analyst who joins the two station numbers, reshapes the register, keeps approved readings,
  reads the station history and applies the manual exactly still converts the glass era with the comparison readings'
  mean difference and ends on $567 a hectare, the raw record's premium (R3a in `checks.py`).
- Estimand: the pricing manual's basis sentence (each past day's maximum as the present instrument would have recorded
  it; heat days and severe heat days counted per season from 1965/66), filed in the manual, with the cover's terms in
  the term sheet.
- No decoy: no memo, draft, briefing or stakeholder figure carries a premium, a conversion or a count; the network
  publishes no adjusted series for Merrin Flat (it is not a reference station), and the station history states the
  change and the paired readings without a size.
- No certified replay: no certified or published figure is reproduced to recover the method; the method is the
  estimator's choice on paired readings the network files.
- Lesson: an instrument change can leave the mean untouched and stretch the upper tail, so a threshold count needs the
  conversion sized at each reading, and a mean conversion leaves the changeover step in the count to be read as
  climate; no build on file teaches a reading-dependent conversion (17 Anomaly Detection drivers read above).

## Readability screen

The six tests per rung (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear), verdict last.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 convert the glass era at all | the manual's basis sentence asks for it | the station history files the change | yes | no | no | no | readable |
| R2 size the conversion from the paired readings, not the neighbours | no | the paired readings are a file of their own | yes | no | no | one subtraction | readable |
| R3 one hot-day offset | no | no | a tail check on a threshold index | no | no | one subtraction on a filtered set | readable |
| R4 (decisive) a conversion sized at each reading | no: the basis sentence is met on its face by the average | no column states a difference by reading | no: the defaults (overall, by month, by site, one hot subset, a linear fit over all days) each land wrong | none ships | the battery is clean on every path | no: a function of the reading applied reading by reading, under two triggers that need different offsets | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | heat day | maximum 35.0 C or more | above 35.0 C | $490 (probe readings of exactly 35.0 C and 40.0 C drop out) | the term sheet's "35.0 C or more"; no converted glass reading within 0.1 C of a trigger (asserted) |
| SF2 | severe heat day | 40.0 C or more, and also a heat day | a severe day not counted as a heat day | a lower premium | the term sheet: a severe heat day is also a heat day |
| SF3 | season | 1 December to the last day of February, 29 February in leap years, named by its first year | 90 days fixed | $523 | the manual's season sentence and the term sheet's period (to 29 February 2028) |
| SF4 | present instrument | the probe in the small shield installed 1 November 1995, unchanged since (recalibrations only) | a later probe | none ships | the station history: no change since 1995 |
| SF5 | pricing record | 1965/66 to 2026/27 | the record since 1995 | a different premium | the manual's basis sentence |
| SF6 | the line | least squares of each count on the season's first year over the record, each count on its own line | one line on the sum | a different premium | the manual's projection sentence |
| SF7 | a projected count below zero | taken as zero | kept negative | same call (no projected count below zero, asserted) | the manual |
| SF8 | the burn | the average over the record of each projected season's payout per hectare under the 2027/28 terms, counts unrounded | payout at the average counts | $468 | the manual's burn sentence |
| SF9 | loading and rounding | the burn times 1.32, rounded once to the whole dollar | rounded before loading | $524 | the manual's "rounded once" |
| SF10 | the overlap months, November 1995 to April 1998 | the official record is the probe from 1 November 1995; the glass readings sit only in the comparison file | the glass converted for the overlap | same call ($525) | the station list and the station history |
| SF11 | the paired readings used for the conversion | Merrin Flat's own, or all seven comparison sites | either | same call (the same readings cross each trigger, asserted) | same call |
| SF12 | the estimator of a reading's conversion | the mean difference at that reading | the median at each reading, a local line within 1.5 C, quantile matching, a line over glass readings of 25, 28 or 30 C and up, a polynomial of degree 2 or 3 over all pairs | same call (each moves exactly the 34.5 C and 39.0 C readings and up, and none of 34.0 C or 38.5 C; all eight asserted at $525, 16.7 and 4.1) | same call |
| SF13 | approved against provisional readings | approved, to 30 June 2027 | provisional | same call (provisional rows fall in July and August 2027, outside every season) | same call |
| SF14 | the expected counts the premium assumes | the lines' values at 2027/28 | the average projected count | same call (no floor binds, asserted) | the manual |
| SF15 | the daily maximum's day | the 24 hours from 09:00, filed against the day they begin, both eras | filed against the reading's day | same call (the station history files one convention) | the station history |

## Ladder

Built values (`checks.py` asserts each by name).

| Rung | Construction | Premium a hectare | Heat days 2027/28 | Severe days 2027/28 | Heat line, days a decade |
|---|---|---|---|---|---|
| R0 | no conversion (the neighbours show no break at Merrin Flat) | $567 | 17.2 | 4.5 | 0.74 |
| R1, the default path | the comparison readings' mean difference, +0.13 C | $567 | 17.2 | 4.5 | 0.74 |
| R2 | the summer mean (+0.25 C) | $567 | 17.2 | 4.5 | 0.74 |
| R2 | a line through all the pairs (+0.39 C at 34.5 C) | $557 | 17.2 | 4.4 | 0.74 |
| R3 | one hot-day offset, glass at 33 C or more (+0.81 C) | $542 | 16.7 | 4.4 | 0.30 |
| R3 | one hot-day offset, glass at 35 C or more (+1.02 C) | $506 | 16.0 | 4.1 | negative |
| R4, decisive | the conversion at each reading (+0.72 C at 34.5 C, +1.35 C at 39.0 C) | $525 | 16.7 | 4.1 | 0.30 |

- **Kills, one fact each:** R0 by the manual's basis sentence (the present instrument); R1 and R2 by the paired readings
  (the difference rises with the reading, and a straight line through 10,409 pairs, most of them cool days, sits under
  the hot bins); R3 by the two triggers (no single offset moves 34.5 C over 35.0 C and 39.0 C over 40.0 C while leaving
  34.0 C below); R4 stands.
- **Why each is satisfying:** R1 is the textbook adjustment and the station history's own pairing; R2 decomposes the
  pilot by season or fits the difference against the reading; R3 answers the threshold worry with a tail offset.
- **Separation:** the default 8.0 per cent above the golden; the line through all pairs 6.1 per cent; the two hot offsets
  3.2 and 3.6 per cent, each also missing one of the two counts at one decimal.
- **Uniform-offset proof:** 34.5 C crossing needs 0.5 C or more, 34.0 C staying below needs under 1.0 C, 39.0 C
  crossing needs 1.0 C or more: no single offset satisfies all three; the sweep from 0.0 C to 2.0 C files $567, $542,
  $506, $477 or $446, never $525 (asserted).
- **Robustness:** every estimator that follows the reading (SF12, eight of them) files $525; the hot range's slope was
  set so the 38.5 C bin (+1.33 C) sits clear of the 1.5 C it would need to cross 40.0 C under every one.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | Merrin Flat's daily maxima, December to February, 1965/66 to 2026/27 | the manual's basis sentence |
| 2 | Unit of account | the hectare | the question and the term sheet |
| 3 | Attribution window | the season, 1 December to the last day of February | the manual; one daily convention in both eras (SF15) |
| 4 | As-of dating | the latest complete season, 2026/27 | the manual |
| 5 | Version basis | approved readings | C1: provisional rows only after June 2027 (SF13) |
| 6 | Denominator | the burn's average over the 62 seasons | the manual |
| 7 | Weighting | each season equally | the manual |
| 8 | Window length | the whole record from 1965/66 | the manual |
| 9 | Boundary inclusivity | 35.0 C and 40.0 C or more | the term sheet; no converted reading on a trigger (asserted) |
| 10 | Rounding path | the premium rounded once, at the end | the manual (SF9) |
| 11 | Tie-break | none: one figure | none needed |
| 12 | Maturity and censoring | 2026/27 complete; 2027/28 not in the record | the manual |
| 13 | Order of operations | convert, count, line, project, payout, average, load, round | the manual's order |
| 14 | Row order | none affects a sum or a least-squares line | C1 |
| 15 | Duplicate resolution | the overlap: probe official from 1 November 1995 | C1: the daily files do not overlap (SF10) |
| 16 | Identity normalisation | the two station numbers | the station register's successor row; C4 (either number alone misses 30 or 32 seasons) |
| 17 | Netting | none | none needed |
| 18 | Dimensional units | degrees Celsius throughout; the glass to the half degree | units in the data and the station history |
| 19 | Code and status semantics | quality flags (approved, provisional) | the dictionary |
| 20 | Integerisation | counts whole, projected counts unrounded | the manual (SF8) |
| 21 | Clause scope | the deductible and the cap per season and hectare | the term sheet |
| 22 | Forward window contents | 2027/28's counts are the lines' values | the manual (SF14) |

## Literal reader

Executing the manual word for word: the basis sentence asks for each past day's maximum as the present instrument
would have recorded it; the paired readings are the only record of what the probe reads for a given glass reading, and
their difference rises with the reading, so the literal conversion of a day is the difference at that day's reading;
the average satisfies the sentence only for a day whose reading is average. Every later clause (counting, the lines,
projection, burn, loading, rounding) is filed and executes to one figure, and every admissible estimator of the
reading-dependent conversion moves the same readings across the triggers (SF12), so every literal reading lands on the
golden; the easy answer comes only from the easy method (one offset) on the same estimand.

## Oracles

- The comparison readings: their mean confirms the mean path and their per-reading differences confirm the golden;
  the same file on both paths, so no tie decides between them.
- The neighbours' monthly series: no break at Merrin Flat on every path, because the neighbours changed in the same
  rollout (a distractor; no tie only under the golden).
- The claims history (Ask B) is the cover's own record since 2019/20, read the same on every main-call path.
- No published or adjusted series for Merrin Flat ships (it is not a reference station).

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, the 2027/28 schedule by the co-operative's four sub-districts | 12: member blocks, insured hectares, premium | a component of the quote: what the cover insures and the premium it brings | the co-operative apportions the premium by sub-district | D2, the sub-district stored on each block at inception and rewritten only at an endorsement, so blocks not endorsed since the co-operative's 2025 redraw carry the old one (same four names) | D6, variety lines repeat the block's insured hectares; over-clean, block numbers restart for each member | renewal schedule, block register, the extract notes' member-number line, term sheet, the quote's rate (5 files, 11 columns) | schedule labels and lines summed (every sub-district high and mis-split); lines deduplicated, schedule labels (totals right, split wrong); dedup on block number (low); register sub-districts over every register block (high); the answer | a policy system copies the customer's sub-district at inception and mirrors the grower's variety lines |
| B, the cover's record by season since 2019/20 | 16: claims paid and what they came to | the audit trail of the cover being repriced | the history table the co-operative weighs the new premium against | D1, duplicate lodgements: a member's claim lodged twice (broker and member portal) sits in the claims register twice, both assessed, only one ever paid; only the finance ledger shows which | D6, the register extract repeats each claim's amount on every insured block line of the claim; D8, the interim run in March and the final run after the Service's approval, often after 30 June, so the ledger's financial year is not the season | claims register, finance ledger, the extract notes (3 files, 9 columns) | register claim numbers counted and amounts summed by season (high every season); ledger by financial year (shifted); register rows counted (higher); the answer | a broker and a member both lodge after a hot season; a flattened claims report repeats claim fields on each risk line; insurers settle weather covers on approved data |
| Chart | 4 named parts | the exhibit of the line the premium is read from | the quote's second page | none (construction) | none | the seasons' counts and the line | the mirror's glass-era seasons and line differ | a pricing desk's standard exhibit |

- **Main population zero-counts:** no device row in Merrin Flat's daily maxima, the comparison readings or the manual
  and term sheet; asserted by count in `checks.py`.
- **Hazard table:** D6 moves Ask A's hectares and blocks in every sub-district and Ask B's claims and amounts in every
  season; D8 moves Ask B's amounts in every season with a final run after 30 June; D1 (a duplicate lodgement in every
  season that paid) moves Ask B's counts and amounts on the register path.
- **Referee:** none; the finance ledger and the claims register tie only by claim, never by season, under either
  handling.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A blocks by sub-district | schedule rows deduplicated by member and block, the schedule's own sub-district | right count, wrong split | miss |
| A hectares by sub-district | the same | right total, wrong split | miss |
| A premium by sub-district | the quoted rate times those hectares | wrong split | miss |
| B claims by season | distinct claim numbers in the register with an assessed amount | high by the duplicate lodgements | miss |
| B amounts by season | register amounts by claim and season | high by the duplicates and the block-line repeats | miss |
| Chart parts (construction layer) | the golden's construction | right | outside |

Mirror leakage: about 16 per cent of the ask weight (the chart's two presence parts and one in ten device figures).
Pair ceiling: about 37 (the cracker at about 55 with the call and the chart, the mirror at about 18).

## Build record

- Generator: `world.py`, `climate.py`, `pricing.py`, `book.py`, `records.py`, `docs.py`, `analysis.py`, `deliver.py`,
  `checks.py`, `verify.py`, `metadata.py`, `build.py`, `postprocess.py`; `python3 task185/generator/build.py` builds the
  pack, the goldens, `metadata.json` and `generator/figures.json`, runs the checks and the verifier, rebuilds into scratch
  for the byte comparison and cuts `target.zip`.
- Pack: 14 files in 5 formats; the automatic station's daily file 34,404 rows; the paired readings 10,409 rows at seven
  sites; distractors the district stations' monthly series and the 2026/27 term sheet.
- Mess neutrality (R2): the resent July 2012 batch and the provisional July and August 2027 rows fall outside every
  season; either station number alone carries 30 or 32 of the 62 seasons, a visible gap; the book's variety lines,
  endorsements, duplicate lodgements and payment runs touch only the asks.

## Judge record

- Pass 1 (stage 4): DETERMINISTIC, FIX_NOW. The premium ($524.58 unrounded), 16.7 and 4.1, the 54 and 29 glass-season
  days, the sub-district rows and the eight season rows reproduced; every reading-by-reading table the judge tried
  (pooled, Merrin Flat only, 1 C and 2 C bins, polynomials, a fit from 28 C, a Merrin Flat quantile map) crossed the
  same readings. Findings: the sub-district ask did not say whether the schedule's or the register's sub-district
  governs (fixed: the extract notes say the register's are the ones the co-operative reports and splits the premium
  by; the stale schedule label stays the device); step 2 mixed the pooled conversion with Merrin Flat's mean (fixed);
  the quote's total row summed rounded premiums to $1 over the policy's (fixed: no summed total). Left open by design:
  a straight line through every pair ($542 pooled, $557 Merrin Flat only) is the R2 rung, ruled out by the data (the
  difference is flat then bends) and never by a filed method, which would turn the decisive step into rule application.
  Gate G method_or_model_selection, analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical.
- Pass 2 (the one re-judge): DETERMINISTIC, APPROVE. Every figure reproduced; a 300-draw bootstrap of the pairs never
  moved the crossing readings; the unrounded premium ($524.58) sits $0.08 above the rounding line, definitive because
  every reading-by-reading estimator gives the same day counts. Same Gate G and Gate H lines.

## Pre-ship check

- Call: quote $525 a hectare for 2027/28, assuming 16.7 heat days and 4.1 severe heat days; the glass seasons gain 54
  heat days and 29 severe heat days at each reading, and the heat-day line rises 0.30 days a decade.
- Default path: the mean conversion (+0.13 C) ends on $567 with 17.2 and 4.5; a line through all pairs $557; one hot
  offset $542 or $506; no offset from 0.0 C to 2.0 C reaches $525; eight reading-dependent estimators all file $525.
- Gates: 5,902 checks with the R1 to R3c block, independent verifier from target/ alone, two byte-identical builds,
  figures_check 73 figures, precut 49 checks, scrub clean (target and golden), leak.py REVIEW (no LEAK), guard surface
  promotes task184 (back to back, different domain and driver) and task80 (gap rule and G16, differentiated on the
  card), heart WARN (Anomaly Detection overuse only).
- Deliverables: heat_cover_quote_2027_28.pdf (two pages: the call, the explanation, the sub-district table; the chart
  and the season table), heat_cover_payouts.csv (eight seasons); target.zip from the final rebuild, 14 files.
- Leak: two isolated reads, no decisive-step sentence, no ranking file, question 6 analytical.
- Judge: pass 1 DETERMINISTIC, FIX_NOW (the sub-district source, step 2's bases, the quote's total row), fixed; pass 2
  DETERMINISTIC, APPROVE.
- Card current: answer, spine rows 34,404, stump and driver at the built values.

## Tried and rejected

- Physical & Environmental Sciences, environmental monitoring exceedance, as the domain: blocked by `ban.pairing`
  (task180 is the same domain and objective in this draw's window).
- Actuarial Science & Insurance as the domain: none of its task types serves Anomaly Detection, so the domain would
  be a backdrop for the objective.
- The seed's hold design (the tail break's interval wider than a filed tolerance, so the rate holds): the decisive
  step would be applying a stated tolerance, rule application.
- Gap population with pattern E: `test.same_puzzle_older` and `test.same_driver_older` against seven older builds;
  the honest label is the rule gap (the filed basis selects the per-reading conversion once the data show the
  difference depends on the reading), G16.
- One trigger (35.0 C only): one live degree of freedom, since any single hot-day offset between 0.5 C and 1.0 C
  lands the golden; the 40.0 C severe tier makes every single offset miss (34.5 C needs 0.5 C or more, 34.0 C under
  1.0 C, 39.0 C 1.0 C or more).
- A Fahrenheit era before 1972 in the pricing record: whole-degree readings put 102 F (38.9 C) one bin from the
  severe trigger with a 0.14 C margin; the record starts in 1965 in Celsius instead.
- A 1989 changeover with the overlap to 1992: the glass era held 24 of 62 seasons and the premium moved under 5 per
  cent on some draws; the 1995 changeover balances the eras (30 and 32 seasons).
- A probe-minus-glass slope of 0.25 C a degree above 34.5 C: the 38.5 C bin (+1.74 C) crossed 40.0 C under the bin
  means but not under a polynomial or a line over glass from 25 C, which filed $689, a competing estimator; at 0.15 C a
  degree every estimator that follows the reading files one premium.
- An uncompressed hot tail: the simulated maxima reached 51 C at Merrin Flat and 57 C at a comparison site; the hottest
  days now flatten into the mid-forties (probe at most 47.1 C), which moves no day across either trigger.
- The terms D6, $48, $85, cap $760: the premium came to 88 per cent of the cap, a cover no co-operative buys; the quote's
  terms are now D14, $40, $60, cap $1,500 (35 per cent of the cap), and the bound seasons' day rates carry cents so no
  season's paid total sits on a half dollar.
