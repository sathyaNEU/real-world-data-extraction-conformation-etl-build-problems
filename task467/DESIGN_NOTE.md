# task467 design note: Velmont's 2027 taxi pickup fee

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: seven architectures
were weighed for this seed and dropped before the card was registered.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task467.json` (architecture v1), registered 2026-10-17. Guard check WARN
  only. Answered: Gate G decomposition_attribution repeats task266, whose split is a program's completions among
  competing endings in an event history; here the split is one series' fall between a temporary rank and a permanent
  rail line that began the same day, read against a comparison series within the line's station zones, and the batch
  varies elsewhere (gap time, a dial, shape 04, a causal-design strategy, a board of directors, a Canadian airport
  authority). Redrawn at the check before registering: gap population with pattern E and Gate G
  decomposition_attribution blocked as a spent signature (task107, task129, task36, task44), so the decisive gap is
  time (the base year carries an arrangement the budget year reverses) with population second; Amy and Michael (first
  names in older builds) replaced from the same draw; deliverables docx and csv (csv and pdf repeated task466).
  Redrawn at the stage-3 heart check: task238 (another lane, registered 23 minutes before this card and not yet in this
  checkout at the draw) holds shape 04 and causal_design, both BLOCKs. The fee-step table left the prompt and the memo,
  so the criteria come from the brokerage-by-month ledger grid (shape 07), and the strategy is composition_mix, the
  vocabulary's family for a Simpson's reversal that changes the comparison, which is the decisive move (causal_design
  named the lower rung's choice of a control series). The heart check's WARNs, answered: Gate G
  decomposition_attribution repeats task266 (a program's completions split among competing endings) and task238 (a
  mode effect read through randomly allocated letters), where here one series' fall is split between a temporary and a
  permanent change within the line's footprint; dial_setting repeats task238 (a monitoring band), here a fee the by-law
  sets in 25-cent steps, with the prompts now different in shape; the question form "what" repeats task238, and the
  form comes from the decision (an amount the by-law sets; "how much" was task466's).
- **Seed:** ET24 (an airport ground transportation team budgets next year's revenue from the per-trip fee on taxi
  pickups, from monthly trip-record drops; a fee column that changed case and a fee that changed price). Kept: the
  world (an airport authority's per-trip taxi pickup fee, the regulator's monthly trip drops), the decision (next
  year's fee revenue, here the cost-recovery fee it sets) and the quantity (next year's fee-liable pickups). Dropped:
  the seed's mechanism rows (the column's case, the fee's step), which are data semantics; both survive only as Layer 1,
  each asserted neutral for the call.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / ETL, own
  pattern "a temporary break and a permanent one that began the same day, separated against a comparison series within
  the components the permanent one acts on". The authority's official monthly series of airport taxi pickups and
  drop-offs is conformed from the Vehicle-for-Hire Office's annual and monthly Parquet files (field names and time
  zones that change between them, void rows, late records, a meter vendor's re-sent copies) and its 2023 archive,
  then restated to the loading arrangement the budget
  year will have; the restatement is the time-series producer's intervention adjustment, and SROS is a methods domain,
  so the swap is of the method: replacing the component-wise intervention estimate with the series' own break or the
  aggregate comparison moves the fee.
- **Shape:** 07, a grid of cells: each brokerage's fee-liable pickups and fees owed in each month from January 2025
  to August 2026 (six brokerages by twenty months, two figures a cell), beside the call, the recorded and restated
  base, the rank's share, the surplus at the fee and the shortfall 25 cents below it, and the chart of the monthly
  series.
- **Strategy:** composition_mix, a Simpson's reversal in the comparison series. The temporary rank (4 November 2024 to 31 December
  2026) and the Airport Line (opened 4 November 2024) began the same day. The rank touches only pickups; the line takes
  riders in both directions, but only on trips to and from the zones its stations serve, and the airport's taxi
  drop-offs come from those zones far more often than its pickups go to them (business travellers ride from downtown
  offices and hotels to the airport and home to the suburbs when they return). So the pickups' own fall carries the
  line, the aggregate drop-off comparison carries the zones' different shares and shows almost no rank effect, and only
  comparisons within the station zones and within the rest, which agree, recover the rank's effect (a Simpson's paradox
  across strata in the aggregate comparison). Gap time (the evidence year holds an arrangement the decision year
  reverses) with population second; generators G6 (the comparison series' mix), G14 (the pooled comparison does not
  apply), G13 (the budget year's arrangement differs from the base year's); pattern E (an absolute split, the confounder
  controlled by construction, no column naming it); Gate G decomposition_attribution.
- **World:** Canada, an unnamed province. Velmont International Airport (about four million passengers a year) is run
  by the Velmont Airport Authority, a not-for-profit corporation with a calendar fiscal year. Licensed taxis pay the
  Authority a fee for each trip they begin at the airport; the Authority bills each taxi brokerage monthly from the
  City of Velmont's Vehicle-for-Hire Office trip records, and its Ground Transportation Fees By-law sets each year's
  fee at the lowest multiple of 25 cents at which the year's budgeted fee-liable pickups recover the Ground
  Transportation Program's budget. Finance Policy FP-07 budgets fee-liable pickups as the most recent complete year's,
  restated for any change in taxi loading arrangements (the location and operation of the taxi rank and holding lot)
  between that year and the budget year, with no traffic growth. On 4 November 2024 the forecourt reconstruction
  around the new Airport Line station began, the day Velmont Transit opened the line (Airport, Commerce Park,
  University, Midtown and Central stations), and taxis moved to a temporary rank on the parkade's Level 2 road; the
  forecourt rank reopens on 1 January 2027. The Vehicle-for-Hire Office publishes each month's taxi trip records as
  Parquet about five weeks after the month ends and, once a year closes, an annual file that replaces the year's
  monthly files; the Authority receives the trips that begin or end in zone 1 (the airport) and its folder holds the
  2024 and 2025 annual files, the eight 2026 monthly files to August and, for 2023, the Office's daily
  origin-destination archive.
- **Forcing fact:** the Authority's board approves the 2027 budget and the 2027 fee schedule in December 2026; the
  budget package goes to the Finance and Audit Committee first. The call faces forward: the fee charged on every 2027
  pickup. As-of: 16 October 2026, the date of the finance manager's memo, after the August 2026 drop (published
  2 October) and before September's.
- **Forum and forcing event:** board_of_directors (the Authority's board), budget_or_appropriation (the 2027 budget
  that carries the fee). Organisation utility_or_infrastructure; role finance_controller. Personas from `guard.py names
  --geo Canada --seed 467`: Olivia White (the Authority's manager of ground transportation finance, who brings the fee to
  the board), Joseph Heath (the Authority's director of ground transportation, who signed the temporary rank notice)
  and Johnny Houston (the Vehicle-for-Hire Office's open data coordinator, who signs the drops' change notes).
- **Data-native sentence:** the Airport Line took taxi riders in both directions but only on trips to and from the
  zones its stations serve, and the airport's taxi drop-offs come from those zones far more often than its pickups go
  to them, so all drop-offs fell almost as far as all pickups when the line opened the day the rank moved, although
  only the pickups moved rank; within the station zones and within the rest, the pickups fell the same share more than
  the drop-offs, and that share is the rank's.
- **The WHAT screen.** The estimand's five parts are filed. Population: the fee-liable pickups of 2025 (every trip a
  licensed taxi began at the airport, voided trips out; the by-law and FP-07). Outcome: those pickups restated to the
  forecourt rank, the loading arrangement 2027 will have (FP-07, which defines a taxi loading arrangement as the rank's
  and holding lot's location and operation, so the line is not one). Window: calendar 2025, the most recent complete
  year. Unit: trips; the fee in dollars, rounded up to the next 25 cents. Comparison: the program budget for 2027. The
  decisive step settles none of them: it is how the filed counterfactual (2025 with the forecourt rank) is estimated,
  and the data's structure (the line's footprint and the two directions' different zone shares) rules out the series'
  own break and the aggregate comparison.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, seasonal-adjustment-official-time-series-production 1 (model
    level shifts in regARIMA before seasonal filtering, the event's date and type given): here both events' dates and
    types are given, and the step is splitting one dated fall between a temporary and a permanent change with a
    comparison series, which the listed pattern does not cover.
  - `stumping/references/client/two-layer-task-design.md`, estimand and identification (the right counterfactual,
    Simpson's paradox across strata): the client's own family; here the paradox sits in a comparison series whose
    strata mix differs from the treated series'.
  - `stumping/references/strategies.md` F8 and F1 (never a dated cause found by an event study): the dates here are
    filed and the fall is visible; an event study finds the combined fall, the reflex control finds a wrong split, and
    the step is the comparison's design within the line's footprint.
  - `dataset-generation/references/layer1-messiness.md`: annual and monthly files with renamed fields, local time
    against UTC, void rows, late records, a vendor's re-sent copies, a fee that steps each 1 January while meters are
    reprogrammed, an attribute stamped when the file was built; none on the decisive step, each asserted neutral.

## Default path

1. Read the Ground Transportation Fees By-law: the 2027 fee is the 2027 Ground Transportation Program budget divided by
   the 2027 budgeted fee-liable pickups, rounded up to the next 25 cents.
2. Read FP-07: the budgeted pickups are 2025's fee-liable pickups restated for any change in taxi loading arrangements
   between 2025 and 2027, with no traffic growth.
3. Read the Office's final 2025 annual file (FP-07 4.4) and count 2025's trips beginning in zone 1: 74,753
   fee-liable pickups (the file holds no voided trip).
4. Read the rank notice: the temporary rank opened on 4 November 2024 and the forecourt rank reopens on 1 January 2027,
   so 2025 is restated to the forecourt rank.
5. Measure the rank's effect as the fall in pickups when it opened, 2025 against the twelve months before the move
   (the 2023 archive supplying November and December 2023, the 2024 file's voided trips netted out): 22 per cent, so
   2025 restates to the earlier twelve months' level, 95,670 pickups.
6. The $535,027 the 2027 budget assigns to the fee over the restated pickups is $5.59 a trip; the lowest 25-cent step
   that recovers it is $5.75.

Ends on: $5.75 a pickup

Golden: $6.50 a pickup

## Stump sentence

The default path restates Velmont's 2025 fee-liable pickups by their whole fall when the temporary rank opened on
4 November 2024 and sets the 2027 fee at $5.75, but the Airport Line opened that day and took taxi riders in both
directions to and from its station zones, so the fall carries the line, which stays in 2027; the analyst who controls
for the line with all the airport's drop-offs finds the rank cost only about 3 per cent and sets $7.00, because the
drop-offs come mostly from the station zones; within the station zones and within the rest the rank cost about 11 per
cent in each, and the fee is $6.50.

## Three rules

Task type: seasonal-adjustment-official-time-series-production: the Authority's official monthly series of airport taxi pickups and drop-offs, conformed from the Vehicle-for-Hire Office's monthly Parquet drops and its 2023 archive and restated to the loading arrangement the budget year will have across a temporary rank that began the day the Airport Line opened, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is the temporary rank's effect on the monthly pickup series, the intervention a time-series producer removes to restate the series to the budget year's arrangement; with a permanent change beginning the same day, the series' own break carries both, and the comparison series (drop-offs) carries the permanent change's components in a different mix, so the effect is read component by component, and replacing that with the series' own break or the aggregate comparison (the generic intervention estimates) moves the fee from $6.50 to $5.75 or $7.00.

Swap: "a hospital's monthly admissions restated for an admissions desk moved the day a walk-in clinic opened, against its discharges" keeps the shape, because in a methods field the setting is always another field's; the swap is of the method, and the restatement fails the moment the component-wise intervention estimate is replaced by the series' break or the aggregate comparison, while the fee rule, the rank, the line's station zones and the two directions' zone shares are the airport's own.

Layer 1: the Vehicle-for-Hire Office's trip records as its systems write them: the 2024 annual file in version 2 field names with each voided trip beside its negative-amount reversal (the meter sends both); the 2025 annual file in version 3 names, without voids, each trip carrying the brokerage its licence held the day the file was built; the 2026 monthly files with meter times in UTC from firmware 8.1, void reversals, store-and-forward trips arriving in a later month's file, the Corvane units' re-sent copies under new record numbers beside their genuine memory-sent trips (both written to the minute) and the fee column written Airport_Fee from the June file; 2023 only as the Office's daily origin-destination archive; and meters charging last year's fee each January until reprogrammed. Each is asserted neutral for the call (checks.py R2); the ask-side items move only their asks.

Layer 2: estimand identification, the right counterfactual: a temporary intervention that began with a permanent one is measured against the comparison series within the components the permanent one acts on, because the aggregate comparison mixes components the two series carry in different shares (a Simpson's paradox across strata).

Decisive step: measuring the temporary rank's effect as the pickups' change against the drop-offs' change within the taxi zones the Airport Line serves and within the zones it does not (about 11 per cent in each), which restates 2025's 74,753 recorded pickups to about 84,000 and sets $6.50; the pickups' own fall (22 per cent) sets $5.75 and the aggregate drop-off comparison (about 3 per cent) sets $7.00.

Not semantics: every field, code, unit and definition read correctly (the zones, the switch to UTC, the void rows, the fee column's case, the late records, a taxi loading arrangement as the rank's and holding lot's location and operation) still leaves the easy route reading the rank's effect off the pickups' fall or off all pickups against all drop-offs, because no field says that the line acts only on its station zones or that the two directions carry those zones in different shares; the step is the comparison's design, not a reading.

Not rule application: the by-law fixes the fee from the budget and the budgeted pickups and FP-07 fixes the base year, what is restated and that no growth is assumed; no rule or procedure says how the rank's effect is measured, and executing every filed rule with the pickups' own fall files $5.75, or with the aggregate comparison $7.00, so the step no rule performs is the comparison within the line's footprint.

Analyst test: a strong analyst who conforms every drop and counts 2025's fee-liable pickups correctly restates them by their fall when the rank moved and sets $5.75 (the default path's Ends on), and one who also controls for the Airport Line with all of the airport's drop-offs finds about 3 per cent and sets $7.00; the within-zone comparison sets $6.50.

Estimand: the Ground Transportation Fees By-law (the year's fee is the program budget over the year's budgeted fee-liable pickups, rounded up to the next 25 cents; a fee-liable pickup is a trip a licensed taxi begins at the airport, a voided trip not being a trip) and Finance Policy FP-07 (budgeted fee-liable pickups are the most recent complete year's, restated for any change in taxi loading arrangements between that year and the budget year, with no traffic growth; a taxi loading arrangement is the location and operation of the taxi rank and holding lot).

No decoy: nothing is planted to be caught; the drops are the Office's records as published, the rank notice and the transit bulletin describe their subjects, no memo, draft or briefing argues a method or a figure, no document computes a restatement or a fee, and the passenger statistics and the 2023 ground access survey are what the Authority keeps.

No certified replay: no published or certified figure reproduces only under one method; the pack carries no bill, posting or published restatement, the 2026 fee in Schedule A comes with no budget or volume to back a method out of, and nothing is recovered by matching a filed number.

Lesson: a temporary change and a permanent one that begin the same day are separated against a comparison series only within the components the permanent one acts on, because the comparison series can carry those components in a very different mix and hide the temporary change almost entirely in the aggregate; no build on file restates a series across coincident breaks or reads an intervention against a comparison series whose component mix differs.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the pickups' own fall when the rank moved ($5.75) | the rank notice dates the move and FP-07 asks for the restatement: fires | none | an event study on the pickups is a reflex: fires | none | none | one ratio of two periods' pickups: fires | readable |
| R1, all pickups against all drop-offs, the line controlled ($7.00) | the transit bulletin dates the line's opening to the same day: fires | none | adding the comparison series the rank never touched is a reflex: fires | none | none | a ratio of two ratios: fires | readable |
| R2 (decisive), the comparison within the line's station zones and within the rest ($6.50) | no clause says the line acts only on its station zones or that the two directions carry those zones in different shares; the bulletin names stations, the zone file names neighbourhoods, nothing joins them: silent | no column marks a station zone or a trip the line could replace: silent | the reflex comparison is the aggregate one (R1); splitting it by where the line runs is no battery step: silent | no control, posting or published figure scores a comparison design: silent | every file reconciles and nothing is anomalous: silent | each stratum is a ratio of ratios, but no reported figure carries it: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | fee-liable pickup | a trip a licensed taxi begins at the airport (zone 1 in the Office's files), voided trips not counted | every trip touching zone 1, or trips ending there | $3.50 or $7.75 | By-law s.2: "fee-liable pickup" is a trip a licensed taxi begins at the airport, and a trip the meter records as voided is not a trip; the zone file names zone 1 the airport |
| SF2 | the most recent complete year | calendar 2025 | the twelve months to August 2026 | same call (the trailing year restates to about 85,100 and $6.50; asserted) | FP-07 4.2 "the most recent complete fiscal year"; FP-07 1.3 the fiscal year is the calendar year |
| SF3 | taxi loading arrangement | the location and operation of the taxi rank and holding lot | any change touching taxi trips, the Airport Line included | $5.75 (the line restated away) | FP-07 4.2 defines the term; the line is Velmont Transit's service |
| SF4 | restated | the pickups 2025 would have had under the budget year's arrangement | 2025's pickups grossed up by the uplift share of the rank's return | same call (the two are one restatement; asserted) | FP-07 4.3 |
| SF5 | measurement windows | the twelve months before 4 November 2024 against 2025 | calendar January to October 2024; November 2024 to October 2025; 2026 to date added | same call and the same whole-per-cent share on each (asserted) | C1: the within-zone ratio of pickups to drop-offs is stable on every window |
| SF6 | month and day convention | local time, a trip placed by its meter start | UTC dates | same call (the 2024 and 2025 files are local; the 2026 drops are off the main path; the share with 2026 added is unchanged under either convention; asserted) | by-law s.2: days, months and years are reckoned in Velmont local time; the dictionary: annual files in local time |
| SF7 | rounding of the fee | the lowest multiple of 25 cents at which the restated pickups at the fee are not less than the amount | the nearest 25 cents | same call ($6.50 on every window; asserted) | By-law s.4 "the lowest multiple of $0.25 at which" |
| SF8 | the amount to recover | the 2027 budget's line assigned to the taxi pickup fee | the program's gross cost | a higher fee | By-law s.4 "the amount the year's Ground Transportation Program budget assigns to the taxi pickup fee"; the budget's line of that name |
| SF9 | no traffic growth | the restated 2025 pickups are 2027's budgeted pickups | 2025 grown at the passenger trend to 2027 | $6.25 | FP-07 4.2 "No traffic growth is assumed" |
| SF10 | the share of pickups the rank cost | the pickups lost as a share of those 2025 would have had at the forecourt (11 per cent) | the uplift on the rank's return as a share of the recorded pickups (12 per cent) | same call; the graded share differs (12 against 11) | the prompt asks for the share of 2025's restated pickups the rank cost |
| SF11 | the budget year's arrangement | the forecourt rank for all of 2027 | the temporary rank for part of 2027 | same call | Notice GT-2024-11: the forecourt rank reopens on 1 January 2027 |
| SF12 | the 2024 file's voided trips | a voided trip and its reversal both out | the reversal dropped, the original kept | same call (every ratio unchanged; asserted) | By-law s.2 |
| SF13 | the 2023 archive against trip records | November and December 2023 from the archive's daily counts | the pre-period without them | same call (asserted) | C1 |

## Ladder

- **R0, the default path: the pickups' own fall ($5.75).** The twelve months before the rank moved against 2025:
  pickups fell 22 per cent (the line and the rank together, net of a year's traffic growth), so the restated base is
  the earlier twelve months' 95,670 and the amount over it is $5.59: $5.75. Dies to one fact: the airport's
  drop-offs, which the rank never touched, fell 19 per cent over the same span, so most of the fall is common to both
  directions.
- **R1, the obvious correction: all pickups against all drop-offs ($7.00).** The pickups' change relative to the
  drop-offs' is about 3 per cent (3.4), so the restated base is about 77,400 and the amount over it $6.91: $7.00.
  Dies to one construction: the line's fall sits only in the zones its stations serve (station-zone drop-offs fell
  32 per cent, drop-offs elsewhere rose 3 per cent with traffic), and before the move the drop-offs came from those
  zones 62 per cent of the time against the pickups' 43, so the aggregate comparison books most of the line's extra
  bite on drop-offs against the rank.
- **R2, the decisive move: within the station zones and within the rest ($6.50).** Pickups fell 10.6 per cent relative
  to drop-offs in the station zones and 11.0 in the rest (and between 10.2 and 12.1 in every zone with more than 1,500
  pre-move pickups), so the restated base is 83,855 (84,000 to the thousand) and the amount over it $6.38: $6.50.
- **Off the ladder (each breaks a filed sentence, misses the data's structure or lands on a rung):** no restatement
  $7.25 (FP-07 4.3); pickups per arriving passenger (the distractor workbook) $5.50; the zone list's districts as the
  groups $6.75 (9 per cent: the Central and Airport districts each mix station zones with zones the line does not
  serve); Central station's zone alone $6.75; growth to 2027 $6.25 (FP-07 4.2); the nearest 25 cents $6.50 (the same call;
  by-law s.4 files the lowest step); the station zones with two neighbours added $6.50 at 10 per cent (the fee, not the share). All asserted.
- **Bins and margins:** the amount over the restated base is $6.38, 1.9 per cent clear of the nearer edge of the $6.50
  step ($6.25 to $6.50); R0 at $5.59 in the $5.75 step (1.7 per cent clear); R1 at $6.91 in the $7.00 step (1.3); no
  restatement at $7.16 in the $7.25 step (1.3). Seven window pairs and the zone-by-zone estimate restate to 83,823 to
  83,865: every one 84,000, 11 per cent, $6.50, a $10,000 surplus and a $10,000 shortfall (asserted).
- **Position, separation and dominance:** a dial; each rung names its own setting (5.75, 7.00, 6.50; 7.25 off the
  ladder), no two adjacent rungs share one. Every correction from R0 walks the fee up and only the decisive move turns
  it down; the decisive move is two 25-cent steps (about 8 per cent of the restated base), far above the 0.1 per cent
  spread of the golden's estimates, though smaller than R0's overshoot, which is R1's whole move.
- **Worth on the graded quantities:** the restated base (graded to the nearest thousand) is 96,000, 77,000 and 84,000 on
  the three rungs; the share 22, 3 and 11 per cent; the fee 5.75, 7.00 and 6.50. The flip is a filed fact, not an
  estimate: the fee holds at $6.50 for any share from 9.2 to 12.7 per cent (asserted from the recorded pickups and the
  budget's amount); the golden 10.85 sits 1.7 and 1.8 points inside.
- **Grid:** the three corrections (recognise the line, use the drop-offs, split by the line's footprint) taken in any
  subset land on R0, R1, R1 or R2; the passenger rate, the districts and Central's zone alone land off the golden.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | 2025's fee-liable pickups: trips beginning in zone 1, voided trips out (by-law s.2); the 2025 file holds no voided trip (C1) |
| 2 | Unit of account | the trip; the fee in dollars a pickup (by-law s.2, s.4) |
| 3 | Attribution window | calendar 2025 by local meter start; trips straddling midnight on 31 December counted by start (C1: no bin moves) |
| 4 | As-of dating | the Office's final 2025 annual file (generated February 2026) |
| 5 | Version basis | the final annual files for 2024 and 2025; the provisional 2026 drops stay off the main path (asserted) |
| 6 | Denominator | the restated pickups under the fee (by-law s.4) |
| 7 | Weighting | each stratum's counterfactual on its own drop-offs, summed; the zone-level sum and either stratum's share agree (C1, asserted, and recomputed in verify.py); groupings that put zones the line serves with zones it does not (the zone list's districts $6.75, Central's zone alone $6.75) leave the line inside a group, which the zone-level drop-offs show (the four station zones fell about a third, no other zone's fell; asserted) |
| 8 | Window length | any windows either side of the move (C1 on the within-zone ratios; SF5) |
| 9 | Boundary inclusivity | 4 November 2024 sits outside both golden windows; calendar-month windows give the same call (asserted) |
| 10 | Rounding path | the amount over the unrounded restated pickups, then up to the next 25 cents (by-law s.4); the restated figure reported to the nearest thousand, the surplus and shortfall worked unrounded (same results, asserted) |
| 11 | Tie-break | none: the fee is a function of two figures |
| 12 | Maturity and censoring | the annual files are final; the 2026 drops provisional and outside the call (asserted) |
| 13 | Order of operations | restate, divide, round (by-law s.4) |
| 14 | Row order | no dependence (asserted on shuffled files) |
| 15 | Duplicate resolution | no duplicate on the main path; the 2024 void pairs out (ratio-neutral, asserted) |
| 16 | Identity normalisation | zone ids stable 2023 to 2026; the bulletin's stations map to zone names one to one |
| 17 | Netting | the program's other revenues netted inside the budget's own line (the amount assigned to the fee) |
| 18 | Dimensional units | trips and dollars; no conversion on the main path |
| 19 | Code and status semantics | zone 1 the airport; reversal rows by negated amounts (2024); dictionary semantics, never the stump |
| 20 | Integerisation | whole trips; the fee in 25-cent steps |
| 21 | Clause scope | FP-07 4.2 and 4.3 apply to the budget year 2027 and its base year 2025 |
| 22 | Forward window contents | 2027's arrangement filed: the forecourt rank from 1 January 2027 (notice), the line in service, no growth (FP-07) |

## Literal reader

Executed word for word, the by-law and FP-07 take 2025's trips beginning in zone 1 in the final annual file (74,753,
none voided) and restate them to the pickups 2025 would have had with taxis at the forecourt rank, a counterfactual
FP-07 files without saying how it is estimated; of the three estimates the files support, the pickups' own fall
($5.75) is contradicted by the drop-offs' fall, the aggregate comparison ($7.00) by the line's fall sitting only in
its station zones, which the two directions carry in different shares, and the within-zone comparison is the one every
group, zone and window agrees on, so the literal execution is 84,000 restated pickups and $6.50; no filed rule, basis
or formula reads to another fee.

## Oracles

- The airport's monthly passenger statistics (a distractor): volume grew about 3 per cent a year and did not fall at
  the move, so pickups per arriving passenger fell about a quarter; on the wrong path this reads as the rank's effect
  ($5.50), but no figure in it ties under any basis.
- The 2023 ground access survey (a distractor): mode shares from before the line, by direction and by trip purpose,
  with no zone breakdown; no figure ties under any reading.
- Schedule A's 2026 fee ($6.75): set on 2024 and the temporary rank, with no budget or volume beside it, so nothing
  backs out a method.
- None ties only under the golden.

## Ask sheet

- **Ask A, for each brokerage and each month of 2025, the fee-liable pickups and the fees owed for them (whole trips;
  dollars and cents at $5.75).** H18 home: the audit trail of the base year the call restates, to the brokerages the
  Authority bills; the input the call consumes (2025's pickups) carried to its billing basis. Use: the 2027 fee notice
  goes to each brokerage with its 2025 base. Path: the Office's 2025 annual file (meter start, pickup zone, vehicle,
  brokerage), the affiliation history (vehicle, brokerage, effective from, effective to), the brokerage register, the
  by-law (fee and billing) and its fee schedule: five files, ten columns. Primary device: D2, an attribute at the wrong
  vintage: the Office built the 2025 file in February 2026 and stamped each trip with its vehicle's latest brokerage,
  so every vehicle that changed brokerage during 2025 or at the 1 January 2026 licence renewal carries its whole 2025
  under the later brokerage; the affiliation history gives the brokerage at each trip's start. Every brokerage gained
  and lost vehicles at the renewal, so all 72 brokerage-months move (asserted). Hazard: January 2025's meters charged
  $5.50 until each was reprogrammed, so the fee column summed misses January's fees owed (the by-law bills the
  scheduled fee per pickup). Stops (asserted): the file's brokerage (the cracker) misses all 72 brokerage-months; the
  register's current brokerage misses all 72; the roster as at 1 January 2025 misses 27; the history as-of join on each
  trip's start date is the golden and equals the clean truth.
  Realism: an annual file built after the year closes joins its trips to the vehicle register as it stands that day.
- **Ask B, for each brokerage and each month from January to August 2026, the fee-liable pickups and the fees owed
  (whole trips; dollars and cents at $6.75).** H18 home: the current year's billing basis under the 2026 fee, the same
  ledger carried forward from the provisional drops. Use: the 2026 months the memo's chart plots, at the grain the Authority bills;
  the ledger's monthly totals are the chart's pickups in every month (asserted, H18). Path: the eight 2026 monthly drops, the dictionary, the brokerage register, the by-law: four
  file kinds, eleven columns. Primary device: D1, a replay under fresh ids: from firmware 8.1 a Corvane unit that
  loses its connection re-sends its unacknowledged trips once it reconnects, days later, and the Office's intake gives
  each copy a new record number; the unit writes a trip it sends from memory with its meter times to the minute, so
  the 1,741 copies sit among 1,545 genuine memory-sent trips written the same way, all with sf_flag Y; every
  brokerage runs Corvane meters, so every brokerage-month holds copies (at least four pickups; asserted). Hazards:
  meter times in UTC from the January 2026 file (local months move month-end trips), voided trips as a reversal row
  beside the original (sometimes in the next month's file), the fee column written Airport_Fee from the June file,
  late trips placed by meter start, January's meters at the 2025 fee. Stops (asserted): exact duplicates dropped with
  UTC converted and void pairs out (the cracker; 58 copies of memory-sent trips are exact and go, the rest survive)
  misses all 48 brokerage-months; UTC months miss 43; voided originals kept miss 44; grouping by file month misses 42;
  dropping every minute-stamped memory record (the over-cleaner) misses 48; the golden removes each record matching an
  earlier record number on licence, start and stop minute, zones, fare and total (exactly the copies; asserted),
  removes void pairs across files and groups by local month of meter start. The by-law bills each month's fee-liable pickups counting each
  trip once (the population, filed at authority after the stage-4 judge found records against trips open on this ask);
  nothing names copies or how to find them, and the data's own structure settles which records are one trip: no licence
  otherwise starts a trip within 25 minutes of ending one (asserted).
- **The construction layer:** the call, the recorded and restated base, the share, the surplus and shortfall and the
  chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the 2023 archive's November and December, the 2024 and 2025
  files' meter start, pickup zone, drop-off zone and (2024) amounts; Ask A's device lives in the brokerage column the
  call never reads, Ask B's in the 2026 drops outside the call's windows; the share with 2026 added, re-sent copies and
  void pairs kept or dropped, in UTC or local months, is unchanged (asserted).
- **Hazard table (asserted):** D2 moves all 72 Ask A brokerage-months; the January meter lag moves January 2025's
  six fees owed for a column-summing response, and January 2026's six; D1 moves all 48 Ask B brokerage-months; UTC
  moves 43 for a response that keeps UTC dates; void originals move 44; file months move 42; the June rename
  drops June to August fees for a response reading the column by its old name.
- **Referee:** none; no total in the asks' files ties under one handling only.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each brokerage's 2025 monthly fee-liable pickups and fees owed | groups the 2025 file by its brokerage column and bills the scheduled fee; every vehicle that moved brokerage at the renewal is booked to its later brokerage | miss |
| B, each brokerage's 2026 monthly fee-liable pickups and fees owed | concatenates the drops, converts UTC, removes void pairs and exact duplicates; the re-sent copies survive every key check | miss |

- Mirror leakage: 7.7 per cent of ask weight (a response on R1 keeps the two files and misses every Ask A and Ask B
  figure on the same devices as the cracker).
- Pair ceiling: 32.6 (planning weights 38 / 7 / 55 with the call, the recorded and restated base, the share, the
  surplus and shortfall and the chart in the main block and r = 5; the ask weight over 26
  criteria: Ask A 12 (each brokerage's 2025 pickups and fees), Ask B 12 (each brokerage's 2026 pickups and fees), the
  two files 2; the cracker keeps the files, 38 + 7 + 4.2 = 49.2; the mirror keeps r, instruction-following and the
  files, 5 + 7 + 4.2 = 16.2; average 32.7), rerun from the generated rubric at ship.

## Tried and rejected

- 2026-10-17, at the draw: a moving-holiday stump (Eid al-Fitr, Lunar New Year or Easter falling in a new month of
  the budget year): each fiscal year holds one occurrence, so the annual total moves under 1.5 per cent; only a monthly
  decision would carry it, and the seed's decision is a year's revenue.
- 2026-10-17, at the draw: a prudent budget at the annual total's 10th percentile with autocorrelated monthly errors:
  every reasonable model gives a different interval, so the figure is not determinate, and simulating paths from the
  fitted model, a strong solver's default, lands.
- 2026-10-17, at the draw: a fee elasticity read from the previous fee change and applied to a coming fee step: the
  functional form (constant elasticity or linear) moves the answer for a step of another size, a fork, and the naive
  route's two errors (the trend booked as the effect, then no trend after it) cancel.
- 2026-10-17, at the draw: a filed back-test choosing the forecasting method: the filed criterion makes the selection
  rule application, and the opponent back-tests by reflex.
- 2026-10-17, at the draw: a level shift at the end of the series (a recent fee change) under a univariate forecast:
  adaptive models absorb it within a few months, so the default lands.
- 2026-10-17, at the draw: the temporary rank alone, with the drop-offs as its comparison series: the drop-offs are the
  reflex control and land on the golden; the line opening the same day, acting only on its station zones, which the two
  directions carry in different shares, is what makes the reflex control wrong.
- 2026-10-17, at the draw: the airport's own passenger forecast as the driver, biased high: catching a stakeholder
  figure that is wrong so the task can overturn it is a plant.
- 2026-10-17, at the build: the general ledger's monthly fee postings as a context file: they tie the recorded pickups
  at each year's fee and invite reading a prior year's restatement back out of the bills; dropped.
- 2026-10-17, at the build: a 2026 column in the budget workbook: with Schedule A's 2026 fee it lets a solver back the
  2026 budgeted pickups out and copy last year's restatement method; removed.
- 2026-10-17, at the build: the re-sent copies as the only Corvane memory records written to the minute: seconds of
  zero with sf_flag Y isolated them exactly, a marker; the unit now writes every trip it sends from memory to the
  minute, so 1,566 genuine trips share the pattern.
- 2026-10-17, at the stage-3 heart check: shape 04 (a table of every 25-cent fee from $5.50 to $7.25) and the
  causal_design label: task238, registered 23 minutes earlier in another lane, holds both; the table left the prompt
  and the memo (shape 07, the ledger grid) and the strategy is labelled by the decisive move (composition_mix).
