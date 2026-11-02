# task467 design note: Wrenfield & Holt's goodwill fund for late refunds, January to June 2026

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: architecture 1
(Velmont's 2027 taxi pickup fee, survey research) is spent on its ask layer and stays delivered on the portal, and
the screens behind architecture 2's draw are recorded there.

## Draw

Architecture 2, re-rooted 2026-11-02 from the draw, on the coordinator's direction into general statistics and data
science. A new world, dataset, generator and shell; nothing of architecture 1 is reused.

| Axis | Draw |
|---|---|
| Pairing | general-statistics-data-science / data-integration-record-linkage-entity-resolution (serves ETL; `guard.py check` raises no task-type BLOCK), objective Data Extraction & Conformation (ETL) |
| Niche | an online fashion and homeware retailer's January to June 2026 refund timeliness return to Trading Standards, counting the refunds made more than 14 days after the returned goods reached its returns centre, when customer-posted parcels carry no label linking the centre's goods-in scans to its processing records |
| Shape | 08, a rule replayed on history: each month's refunds made, refunds made late, the late share and whether the month met the commitment (6 months, 4 figures each), the payment and the breach months, the chart's named parts, the asks |
| Decision | quantity_figure (the goodwill payment in pounds) with the breach months beside it; answer unit currency |
| Gap, pattern, generators | objective first (the centre's dates are right and are not what the commitment is scored on), population; pattern none; G16 (method selection) decisive, G3 (record against operation), G19 (contract conformance) |
| Gate G | method_or_model_selection: arrival-order pairing against the picking behaviour the 2025 labelled returns measure, the right one pinned by that validation record |
| Strategy | identity_resolution (pairing the events of two logs that share no key); the strategy-risk WARN is answered below |
| Calibration organ | prior_period_close_out: the 2025 returns, every one under a prepaid label the goods-in scan and the processing log both carry |
| Context artifact | close_out_summary: the returns centre's 2025 year-end summary the compliance lead works from |
| Forum, forcing event, org family | regulator_or_inspector (Kesterfield Trading Standards), statutory_or_regulatory_filing (the written assurance's return, due 30 November 2026), retailer_or_ecommerce |
| Role | the retailer's head of regulatory compliance (compliance_or_audit), who files the return and pays the fund |
| World | England, GBP. Wrenfield & Holt (an online fashion and homeware retailer), its Cotterby returns centre, Kesterfield Trading Standards, Parcelway (the 2025 prepaid label carrier): all invented |
| People | `guard.py names --geo "United Kingdom" --seed 467`: Howard Jones (head of regulatory compliance), Steven Jennings (returns centre operations manager), Neil Fisher (the Trading Standards officer) |
| Deliverables | `goodwill_fund_return_h1_2026.csv` (the return, one row per month) and `refund_timeliness_note.pdf` (the note with the payment, the breach months and the chart); question form how-much, shell how-much, kesterfield, csv+pdf (architecture 1's what, send, csv+docx is in `lineage_shells`) |
| As-of | the extracts were pulled on 30 October 2026; the return is due 30 November 2026 |

**The world.** Through 2025 every Wrenfield & Holt return travelled under a prepaid Parcelway label issued by the
returns portal, so the Cotterby centre's goods-in scan (the label barcode, the time the parcel came off the van) and
its processing record (the order read from the returns note inside, the time it was opened and graded) both carried
one tracking number. From 1 January 2026 the retailer stopped paying for returns: customers post parcels by any
carrier, the goods-in scan reads whatever carrier barcode is on the box, the processing record reads the order from
the returns note, and nothing joins the two. Parcels wait in bays by day of delivery; the pickers are asked to clear
the oldest bay but in practice take the oldest bay only part of the time and otherwise whatever is to hand. January
2026 brought the post-Christmas surge on a smaller team, the bays filled to weeks of work, and refunds slowed. After
complaints, the retailer gave Kesterfield Trading Standards a written assurance in October 2026: a return for each
month from January to June 2026 giving the refunds made for posted returns and how many were made more than 14 days
after the day the goods were delivered to the Cotterby centre, £15 into a customer goodwill fund for each of those,
and a commitment that each month at least 95 per cent of refunds are made within 14 days.

**The decision and its quantity.** The payment is £15 times the refunds made late, and a month breaches when its late
share passes 5 per cent. The refund date is recorded for every refund; the delivery date behind a 2026 refund is not.
The deciding quantity is that delivery date, a link between two logs no key carries, and the task type's own
statistical object: a probabilistic record link estimated from the order in which a pool of records is worked.

**The abstraction.** Two event logs of one population share no key; items join a pool in the order of the first log
and leave it in the order of the second, and the leaving order is neither the joining order nor random, but a mix the
linked year measures; the time each item spent in the pool, and so how many passed a limit, follows only from
replaying that measured mix over the unlinked period's own pool.

**The ETL pincer.** The correction's input is neither present (no 2026 record carries a delivery date for a refund),
absent (the 2025 labelled returns measure the picking behaviour on records that observe it), nor a sampled model of a
measurement: the forcing file, the 2025 goods-in scans tied to their processing records, pins an ORDER (the share of
picks that take the oldest bay, and how the rest are drawn), and it is operational scanning, not an administrative
field. Reading it correctly is not sufficient: the behaviour has to be replayed over 2026's own arrivals and picks,
because how long a parcel waits depends on how deep the pool is when it arrives, and January 2026's pool was several
times deeper than any 2025 day.

**Data-native sentence.** Customer-posted parcels carry no label the centre's two systems share, and the bays are
worked oldest first only part of the time, so in a deep queue the day a parcel reached the centre is not its place in
the arrival order, and only the labelled 2025 returns show how far it departs from it.

**The WHAT, filed at the draw (lesson 10's test).** The written assurance files the population (refunds made in the
month for goods returned by post), the outcome (made more than 14 days after the day the returned goods were
delivered to the Cotterby centre, the goods-in scan's date), the window (January to June 2026 by refund date), the
unit (a refund) and the commitment (95 per cent within 14 days each month). No sentence says how a refund's delivery
date is found, how the bays are worked, or that the two logs are paired at all; the sentence that would close a judge's
fork on the pairing would name the decisive step, so it is never filed, and the pairing is forced by the 2025 record
instead. Nothing in the pack states a wait factor, a picking rule or any 2026 late count (lessons 9 and 11).

**Guard.** `guard.py check` on the registered card (2026-11-02T19:00:47Z): WARN only. Answered:
- `three_rules.strategy_risk` (identity_resolution): the analyst test reads every field right (the refund date, the
  goods-in date, the assurance's definition) and still files the wrong payment, because the error is the pairing model,
  not a field or a rule.
- `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, task501 and 5 of the last 12): the honest label; the
  method in question (how two unlinked logs pair) shares nothing with task501's flows, and etl_conformance would name
  the deliverable rather than the mechanism.
- Blocks met and redrawn before registering: `ban.pattern` D and `ban.artifact` operations_log (task183), then G3
  first and filed_standard (task501), so G16 leads and the context artifact is the 2025 close-out summary; the shell
  moved off architecture 1's (`shell.lineage`); deliverables csv+pdf after docx+xlsx (task183, task464) and pdf+xlsx
  (task501) WARNed.
- `test.same_driver_older` against task195, task228 v2 and task478 v7: differentiated on the card (a paired-difference
  interval, a three-way error separation, a supplier property carried across spot tests; none pairs two logs).
- Nearest drivers 0.06 (task148 v2, task449, task269 v3): task449's spent ground is a link to the first of several
  equally plausible targets diluting a linked attribute; here the easy route pairs in arrival order, the truth is a
  measured mix that is neither first nor uniform, and the quantity is a waiting time, not a diluted share.

**Screens run before the first harness.** `guard.py recent`, `coverage`, `mechanisms --objective etl` (the cell's
drivers: task449's first-of-k link, task461's auxiliary series through its overlap, task465's two traits through a small
both-traits source, task466's censored historical extremes, task469's allowance-censored durations, task473's
observer-dependent detection, task458's spent periodic counts outside a window) and `slots` on the mechanism nouns
(random order, service order, cumulative curve, Little's law, SIRO, conditional logit, pick model, oldest first,
process mining, case ID, pairing, unlinked, FIFO, LIFO, queue discipline, work tray) and the setting nouns (refund,
returns centre, parcel, carrier, cage, Consumer Contracts, self-ship, prepaid label, work queue). Hits read: task198's
H3 (a capacity-limited queue whose service order changes, dead because the order was a stated prioritisation rule:
here no order is stated or changes, the behaviour is measured), task487 (alarms released in random order, a stage-3
detail), task133 (references reissued oldest first, a device). The neighbouring slots' `resume` lines read: task458
(spent), task464, task183 and task501 (in flight in other cells).

**Sources.** Synthetic, generated by `generator/` (the returns, the scans, the processing and refund records, the
assurance and the centre's summaries); the legal frame (a 14-day refund period running from the trader's receipt of the
goods) follows the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013, regulation
34, cited by name only. Provenance goes to `metadata.json`.

## Default path

Stage 2.

## Stump sentence

Stage 2.

## Three rules

Stage 2.

## Survivor anatomy

Stage 2.

## Readability screen

Stage 2.

## Semantic fork table

Stage 2.

## Ladder

Stage 2.

## Closure table

Stage 2.

## Literal reader

Stage 2.

## Oracles

Stage 2.

## Ask sheet

Stage 2.

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
- 2026-11-02, at the reship (the in-house re-check under the new leak gate, LEAK `vfh_trip_records_data_dictionary.pdf`):
  the shipped pack carried the Office's data dictionary (the field list, the version 2 to 3 names, the void,
  late-record and file-cycle notes, the clocks, and the contact line that was the pack's only mention of Johnny
  Houston) and folder_contents.csv (every file's source, date, description and rows), two files that describe the
  data; neither ships now. Provenance went to metadata.json; the annual files' clock to the files themselves (the 2025
  file's meter times written with the local zone; the 2024 file's unzoned times, read as UTC, file the same call and
  figures, C1); the void and late-record conventions to the rows (SF6, SF12, closures 4 and 19, each asserted through
  the verifier's reader); the version 2 names to themselves (R2's union by position). No document's text changed and
  no graded figure moved.
- 2026-11-02, the honest-cracker audit: both asks are spent. The careful solver (generator/ceiling.py on the cut pack)
  executes by-law s.3(2) through the register's effective dates and lands Ask A's stale brokerage label (144 of 144),
  and its near-exact duplicate check (one licence, zones, fare and total, start and stop minute) lands Ask B's re-sent
  copies (96 of 96): pair 83.5, mirror leakage 100 per cent. The shipped sheet's 0 of 240 came from two narrowed
  crackers (the file's own brokerage column; exact duplicates only). Ask A cannot be re-sited: it is computed over the
  call's own population (2025's fee-liable pickups), so its only device room is the brokerage attribution, which s.3(2)
  makes rule application.
- 2026-11-02, the ask rework stopped at step 5 with no device passing both tests. The candidate table (candidate;
  forced for the judge?; missed by the careful solver?; verdict), each measured on the world in scratch, nothing in the
  pack changed: (X) re-site in the 2026 drops, a Corvane unit that loses its licence pairing after a power cycle in the
  holding lot reports under its own serial for two to six days, linked to its licence by timing; no (a median of 9
  other licences, at least 6, are silent through each of 47 runs, and 9 of 47 runs have another licence that also fits
  a tight lot-wait bracket: a restart read from timing); yes; fork. (X2) the same unit linked by a meter trip counter
  or the odometer; yes; no (a sequence check or the field's plain meaning finds it, as task228's counter continuation
  fell to a told reader); spent. (X3) a meter reboot splitting one trip into two records; partly (a short zone 1 trip
  then a hotel pickup explains the pair too); no (the same-licence overlap check); spent. (D) the full replacement on a
  new ask-only record, the Authority's rank dispatch log (its own cab numbers, no licence) with flat-fare loads the
  meters never recorded, the ledger cut to 2026; yes (a Loaded dispatch whose cab's licence starts no airport pickup
  within four minutes); no (the battery's re-keyed match by time recovers the cab-to-licence pairing for 220 of 220
  cabs and all 262 off-meter loads with no false hit, 48 of 48 brokerage-months); spent. (D2) brokerage receivables with
  a re-keyed payer; yes; no (cash application by amount); spent. (D3) the rank contractor's per-load invoice, parties
  against taxis; yes; no (collapse by cab and minute); spent. task247's form (a clean, wrong join through a
  current-state register after a silent re-key) has no home here: billing runs through an effective-dated register
  and a filed rule, so a re-key on the 2026 rows leaves orphans, a mismatch s.3(2) settles, or a device on the call's
  own 2025 rows. On the house count (the call 1, the critical components 3, the surplus 1, the shortfall 1, the chart
  1, Ask A 12, Ask B 12, the two files 2: 33 criteria), cutting Ask A leaves 21 with Ask B spent besides, and cutting
  both leaves 8, each under 25. Owed: a new ask layer on records this world would hold, screened as code against the
  careful solver before any data is cut, or a re-root.
- 2026-11-02, the re-root: architecture 1 is spent on its ask layer (above) and the world cannot carry a new one, so the
  slot moved to a new world, dataset, generator and shell. On the coordinator's direction the client domain is general
  statistics and data science, task type data integration, record linkage and entity resolution; payment-claims
  analytics (its drivers sit beside spent ones), emissions inventory (13 live ETL cards) and survey research were not
  taken.
- 2026-11-02, architecture 2 draw screens in healthcare payment-claims and test equating before the redirection, each
  dead on paper: claims completion by lag triangle, credibility blends, redirection, coding intensity, retro
  eligibility, caps and deferrals (rule application, a sampled fork or task451's driver); latent-trait densities,
  formula scoring and automated scoring in equating (task445 and task488 hold the cell).
- 2026-11-02, architecture 2 screens in data integration, each dead before a card: door counters with per-door bias
  (a per-unit against pooled parameter, stumping 1.1c); meters to transformers by voltage correlation (a phase field
  re-derived from a finer key, a hygiene item; task164's world); desk occupancy from badges and Wi-Fi (Little's law, a
  reflex); flexible rail tickets placed by gated taps (a composition reflex, a transport fork); cookie linkability decay
  (one person under two keys); Fellegi-Sunter weights under correlated fields (a specification extension; the
  identity ground); Leslie depletion (dead in task135); Dawid-Skene raters and Cooke weights (a rater family, a knob);
  vending and laundromat re-timing (task123); dead-time saturation (dead); historian deadbands (a documented
  transformation, rule application); Berkson fusion and Chao1 (task465, capture-recapture); clock drift between syncs
  (task180's per-use drift).
- 2026-11-02, architecture 2 screens on the record-linkage objects themselves: coincident name and birth-date matches
  measured by near-miss birth dates (task488's cleanest determinate form) lives in person linkage beside the spent "one
  person under two member keys", is immaterial at city scale on full names, and on a coarse key (birth date, sex and
  postcode) the birth-year by postcode null lands it (1.1c); a pilot's precision carried to a full linkage (task488's
  record: task192 and task446 v2's lesson); value-specific agreement weights (no determinate prior); survivorship of a
  master's fields by update age (a covariate the battery stratifies); signs-of-life over-coverage (G12, task458's
  lineage).
- 2026-11-02, architecture 2 screens on observation schemes: fixed-time snapshots aliasing a daily cycle (a grouping by
  hour, 1.1c); a well-mixed or funnel-flow grain bin linking intakes to out-loads (task229's lesson: bulk-solids flow
  with a data-integration label, and task273 screened the well-mixed form); a rank-size tail beyond a top-k chart (a
  third tail build in the cell, the extrapolation form forks); random order of service from a pool (its truth is
  task449's equally plausible targets); sampled telemetry under a rate cap (a per-interval weight, 1.1c); dwell times
  deconvolved from entry and exit counters (the deconvolution forks and no contract reads a dwell share).
