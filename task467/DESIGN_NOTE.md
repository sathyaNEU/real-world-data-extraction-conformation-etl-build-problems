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
| Forum, forcing event, org family | regulator_or_inspector (Calvermoor Trading Standards), statutory_or_regulatory_filing (the written assurance's return, due 30 November 2026), retailer_or_ecommerce |
| Role | the retailer's head of regulatory compliance (compliance_or_audit), who files the return and pays the fund |
| World | England, GBP. Wrenfield & Holt (an online fashion and homeware retailer), its Cotterby returns centre, Calvermoor Trading Standards, Tarnwell (the 2025 prepaid label carrier): all invented |
| People | `guard.py names --geo "United Kingdom" --seed 467`: Howard Jones (head of regulatory compliance), Steven Jennings (returns centre operations manager), Neil Fisher (the Trading Standards officer) |
| Deliverables | `goodwill_fund_return_h1_2026.csv` (the return, one row per month) and `refund_timeliness_note.pdf` (the note with the payment, the breach months and the chart); question form how-much, shell how-much, kesterfield, csv+pdf (architecture 1's what, send, csv+docx is in `lineage_shells`) |
| As-of | the extracts were pulled on 30 October 2026; the return is due 30 November 2026 |

**The world.** Through 2025 every Wrenfield & Holt return travelled under a prepaid Tarnwell label issued by the
returns portal, so the Cotterby centre's goods-in scan (the label barcode, the time the parcel came off the van) and
its processing record (the order read from the returns note inside, the time it was opened and graded) both carried
one tracking number. From 1 January 2026 the retailer stopped paying for returns: customers post parcels by any
carrier, the goods-in scan reads whatever carrier barcode is on the box, the processing record reads the order from
the returns note, and nothing joins the two. Parcels wait in roll cages in the returns hall; the cages are block-stacked in the hall, the newest in front, and the next parcel opened is always the
newest one waiting (the 2025 labelled records show it on every opening). January
2026 brought the post-Christmas surge on a smaller team, the hall filled to weeks of work, and refunds slowed. After
complaints, the retailer gave Calvermoor Trading Standards a written assurance in October 2026: a return for each
month from January to June 2026 giving the refunds made for posted returns and how many were made more than 14 days
after the day the goods were delivered to the Cotterby centre, £15 into a customer goodwill fund for each of those,
and a commitment that each month at least 95 per cent of refunds are made within 14 days.

**The decision and its quantity.** The payment is £15 times the refunds made late, and a month breaches when its late
share passes 5 per cent. The refund date is recorded for every refund; the delivery date behind a 2026 refund is not.
The deciding quantity is that delivery date, a link between two logs no key carries, and the task type's own
statistical object: a probabilistic record link estimated from the order in which a pool of records is worked.

**The abstraction.** Two event logs of one population share no key; items join a pool in the order of the first log
and leave it in the order of the second, and the leaving order is not the joining order but the reverse of it (the
newest item waiting leaves first), as the linked year shows on every item; the time each item spent in the pool, and so
how many passed a limit, follows only from replaying that order over the unlinked period's own arrivals and departures.

**The ETL pincer.** The correction's input is neither present (no 2026 record carries a delivery date for a refund),
absent (the 2025 labelled returns measure the picking behaviour on records that observe it), nor a sampled model of a
measurement: the forcing file, the 2025 goods-in scans tied to their processing records, pins an ORDER (the newest
parcel waiting is the one opened), and it is operational scanning, not an administrative
field. Reading it correctly is not sufficient: the behaviour has to be replayed over 2026's own arrivals and picks,
because how long a parcel waits depends on how deep the pool is when it arrives, and January 2026's pool was several
times deeper than any 2025 day.

**Data-native sentence.** Customer-posted parcels carry no label the centre's two systems share, and the hall's
cages are block-stacked so the newest parcel waiting is always the next opened, so in a deep hall the day a parcel
reached the centre is the reverse of its place in the arrival order, and only the labelled 2025 returns show it.

**The WHAT, filed at the draw (lesson 10's test).** The written assurance files the population (refunds made in the
month for goods returned by post), the outcome (made on day 15 or later, counting calendar days from the day the
returned goods reached the Cotterby centre, the goods-in scan's UK date, as day 0), the window (January to June 2026 by
the month of the payment run that makes the refund), the unit (a refund) and the commitment (95 per cent made by day
14 each month). No sentence says how a refund's delivery
date is found, how the hall is worked, or that the two logs are paired at all; the sentence that would close a judge's
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
  equally plausible targets diluting a linked attribute; here the easy route pairs in arrival order, the truth is the
  reverse order the labelled records show on every opening (not equally plausible targets), and the quantity is a
  waiting time, not a diluted share.

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

The pipeline a competent analyst builds from the prompt's words and the files' grain, every field read correctly:

1. Read the written assurance: the population (refunds made in the month for goods returned to the Cotterby returns
   centre), the made date (the payment run that pays, the succeeding one for a reissued refund), the month (the made
   date's), the count (calendar days, the delivery day as day 0, late on day 15 or later), the commitment and the
   payment of GBP 15 a late refund.
2. Conform the two goods-in exports to one UK-time delivery record: the 2025 CSV's `scanned_at_uk` and the 2026
   Parquet's `event_ts_uk`, renamed columns and carrier codes mapped; every row a return parcel, one delivery a barcode.
3. Conform the processing log (one record an opening, `processed_at_uk`) and the refund ledger (return refunds; a
   failed card refund's reissue as the made date; the UTC stamps to UK dates; the pence column from April).
4. Date each 2026 refund's parcel. The 2026 records share no reference, so pair the goods-in deliveries and the
   openings by the queue's own pairing: the cumulative arrival and opening curves, the k-th parcel opened being the
   k-th delivered (first in, first out), from the hall's content on 1 January 2026.
5. Validate: the curves close every day against the daily sheet's waiting count, and the mean days from delivery to
   opening over 2025 come out at 0.408, exactly what the labelled 2025 records give (Little's law).
6. Count each month's refunds made, those made on day 15 or later, the share and whether 95 per cent were made by day
   14; the payment is GBP 15 times the late refunds.

Ends on: a payment of GBP 189,330 (12,622 refunds made late), February and March in breach.

Golden: a payment of GBP 127,785 (8,519 refunds made late), February, March and April in breach.

## Stump sentence

Pairing the 2026 goods-in scans with the openings in arrival order (the cumulative curves, whose mean wait matches the
labelled 2025 records exactly) files a goodwill payment of GBP 189,330 with February and March in breach, because the
centre's block-stacked hall always gives up the newest parcel waiting: in January's deep hall the newest parcels went
out within days while the oldest waited until the hall emptied in March and April, so replayed that way the payment is
GBP 127,785 and April breaches too.

## Three rules

- Task type: general-statistics-data-science / data-integration-record-linkage-entity-resolution, which serves ETL;
  the conformed return needs every 2026 refund linked to the goods-in scan of its parcel across two record systems
  that carry no shared key.
- Domain test: the deciding quantity is the link from each 2026 refund's processing record to the goods-in scan of
  its parcel, the record linkage object itself, estimated by the linkage model the records where the true link is
  known (every 2025 parcel and January 2026's labelled stragglers) validate; swap the model for a generic summary and
  the payment and breach months change.
- Swap: put a single-lane counter queue (first come, first served by construction) in place of the block-stacked hall
  and arrival-order pairing is right, so the task stops; put another field's nouns in (a laboratory's sample racks, a
  records office's in-tray) and the call still turns on how two unlinked logs pair, which is the data-integration
  question, and replacing that pairing with the 2025 mean wait or 2025's late shares moves the payment from GBP
  127,785 to GBP 189,330 or GBP 11,265.
- Layer 1: two goods-in exports (new scanner software from 1 January 2026: a parquet export with renamed columns and
  carrier codes), prepaid labels on the 2025 processing records and on parcels still arriving on them in January 2026,
  failed card refunds reissued as store credit (in the same month and on the same side of day 15), the refund ledger's
  UTC stamps (its 18:00 payment runs fall on the same date either way), the finance system's pence column from April;
  each produced by the system named, none placed to be caught, none moving the call once read as its system writes it
  (asserted, the R2 block of `checks.py`).
- Layer 2: estimation_fit: the linkage model between two event streams that lost their key, arrival order (the
  cumulative curves) against the order the labelled records reveal (the newest parcel waiting is opened), replayed over
  2026's own deliveries and openings from the hall's 1 January content.
- Decisive step: recognising that the cumulative curves assume the hall is worked first in, first out, testing that
  assumption on the openings whose parcel is known (every 2025 opening and January's labelled stragglers), and dating
  each 2026 refund by the order those openings show, the newest parcel waiting at the moment of opening.
- Not semantics: every field read right (both goods-in layouts in UK time, the opening time, the made date of a
  reissued refund, the day-0 count, the return reason) still leaves each 2026 refund's delivery day unknown, and the
  arrival-order pairing built from correctly read fields files GBP 189,330.
- Not rule application: no filed rule says how the two logs pair or how the hall is worked; the assurance files only
  the WHAT. The enumerated family (opening day as delivery day, arrival order, 2025's monthly late shares carried,
  every waiting parcel equally likely, newest first over refunded parcels only, newest first by day, newest first by
  scan time) spans GBP 0 to GBP 192,000 and breach sets from none to February, March and April; the standing family
  (pairings the labelled openings leave defensible: newest first by scan time over every opening, started from the
  hall's real content on 1 January or from an empty hall, which it was) is one payment, GBP 127,785, and one breach
  set, spread zero; the ruling-out is the labelled openings themselves (newest first exact on 181,318 of 181,318,
  arrival order exact on 1,759, newest first over refunded parcels only on 113,850, newest first by day on 205), a
  comparison the cumulative curves never ask for, made on a 13-month file the question gives no reason to open.
- Analyst test: a strong analyst who conforms both goods-in exports, keys every refund to its processing record, reads
  the assurance's day count and pairs the 2026 logs in arrival order files a payment of GBP 189,330 with February and
  March in breach, against GBP 127,785 with April in breach too.
- Estimand: `calvermoor_written_assurance_oct2026.pdf` paragraphs 2 to 5: refunds made in each month January to June
  2026 for goods returned to the Cotterby returns centre (the month of the payment run that pays, a reissued refund at
  the succeeding payment), made late on day 15 or later counting calendar days from the goods-in scan day as day 0,
  the share, the 95 per cent commitment, GBP 15 a late refund.
- No decoy: nothing is planted; no document states a pairing, a wait, a late share or a picking practice; the 2025
  review states volumes and the team only; the labelled records are the prepaid scheme's own data, not a key left in
  to be found.
- No certified replay: the method is not recovered by reproducing certified figures; nothing in the pack publishes a
  2025 wait or late count, and the labelled openings are record-level evidence of an order, read row by row.
- Lesson: when two event logs lose their shared key, the order in which the buffer between them is worked is a linkage
  model to test on the records where the link survives, not the first-in, first-out order a cumulative curve assumes;
  no build on file links unlinked event streams through the service order their own surviving links reveal.

## Survivor anatomy

- Actor: each 2026 refund's delivery day has no column anywhere; it is a relation between a processing record and a
  goods-in scan that only the hall's working order fixes.
- Link: the pairing runs through the hall's order of working, which no key offers (the 2026 logs share no reference)
  and no sentence invites (the assurance names only the goods-in scan as the day-0 source).
- Reflex: the field's method for two unlinked event streams of one queue, cumulative arrival and departure curves
  (first in, first out), sits at rung 1 and files GBP 189,330 with February and March.
- Back-test: the textbook route validates on what the field checks: the curves close against the daily sheet's
  waiting count every day and give the labelled 2025 mean wait (0.408 days) exactly, since Little's law holds for any
  order.
- Second use: every file the decisive step reads is in the pack for its own reason: the goods-in exports (receiving),
  the processing log (grading and the refund trigger), the refund ledger (finance), the prepaid labels on the 2025
  processing records (the label scheme's own lookup).
- Shock: January's surge reads as the ordinary post-Christmas peak the 2025 review describes; the late refunds it
  causes are paid in March and April, months after it, as the hall empties.
- Pins: the WHAT is filed in the written assurance, Trading Standards' own genre; no filed sentence names the hall,
  its order of working, the pairing of the logs or the labels.

## Readability screen

| Rung | Filed sentence | Schema | Verdict |
|---|---|---|---|
| 0, the opening day as the delivery day | the assurance's day 0 is the goods-in scan, so no | the opening time is a column of the processing log | readable |
| 1, arrival order (the cumulative curves) | none | no key joins the 2026 logs | silent |
| 2, 2025's late shares carried to 2026 | none | needs the 2025 labels joined to the scans | silent |
| 3, every waiting parcel equally likely | none | no column holds an order of working | silent |
| 4 (decisive), newest parcel waiting opened, by scan time | none names a hall, an order of working or a pairing | no column holds it; the labels exist only on 2025 openings and January's stragglers | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a refund made late | made on day 15 or later, calendar days from the goods-in scan day (day 0) | more than 336 hours after the scan | GBP 127,995, same breach months | assurance para 3(iii), calendar days and day 15 |
| SF2 | the month a refund belongs to | the month of the payment run that pays it | the delivery month or the opening month | other monthly counts | assurance para 3(ii) |
| SF3 | when a reissued refund is made | the succeeding payment's run date | the failed run's date | moves Jan to Jun counts | assurance para 3(i) |
| SF4 | the delivery day | the goods-in scan day in UK time | the scan time taken as UTC and moved to UK time | moves the day count near midnight in summer | assurance para 3(iii), UK time; both exports' time columns are named for UK time |
| SF5 | one delivery a parcel | each barcode is one goods-in row | a barcode counted twice | same call (no barcode is scanned twice, asserted) | C1 |
| SF6 | refunds for goods returned to the centre | refunds with reason RETURN | every refund in the ledger | other counts | assurance para 2(a); the ledger's reason |
| SF7 | Irish site customers | in the population (their goods come to Cotterby) | UK customers only | other counts | assurance para 2(a) names the centre, not a site |
| SF8 | rejected parcels | not refunds, so outside 2(a) | counted | other counts | the assurance counts refunds made |
| SF9 | goods-in rows that are not returns | none ship; every row is a return | some rows read as stock | same call (the class columns hold one value, asserted) | C1 |
| SF10 | a processing record | one opening of one parcel | a record keyed twice | same call (every process id unique, asserted) | C1 |
| SF11 | the hall's content on 1 January 2026 | every 2025 delivery not yet opened (none at the turn of the year) | an empty hall | same call (asserted) | C1 |
| SF12 | met the commitment | at least 95 per cent of the month's refunds made by day 14 | more than 95 per cent | same call (no month on the edge) | assurance para 4 |
| SF13 | the late share | late refunds over refunds made, one decimal | over refunds made by day 14 | other shares | prompt and para 2(c) |
| SF14 | the payment | GBP 15 times January to June's late refunds | per month rounded | same figure | para 5 |
| SF15 | a voucher's value in pounds | the value in its customer's currency, euros at the order system's reporting rate of 0.86 | every value as pounds | other values | the order extract carries each customer's currency and the GBP 0.86 a euro on every euro order |
| SF16 | the vouchers issued in a month | every voucher, whatever its reason | refund-delay vouchers only | other values | the assurance para 2(e) and the prompt say the goodwill vouchers customer services issued |
| SF17 | vouchers given for a refund delay | reason Refund delay | every voucher on a refund-delay case | same set (asserted) | C1 |
| SF18 | the order a delayed refund was on | the order the voucher's case names | the voucher's own order field | other categories (counts 1,387, 656, 607, 498, 392, 285) | a delayed refund needs a refunded order: on all 1,378 Refund delay vouchers whose own field differs from the case's order, that field names a later order of the customer's with no refund of any kind (no ledger row of any reason or status) and no processing record, so the literal reading is impossible on every row (lesson 8, asserted); of the 1,631 vouchers of any reason whose own order differs, the 26 whose own order had a refund (4 of them made late) are Damaged item, Delivery delay or Other vouchers, which Ask B never reads, and Ask A reads no order (asserted) |
| SF19 | vouchers issued in January to June | issue time in UK time inside the half-year | the case's opening time | same set (asserted) | C1 |
| SF20 | an order's product category | the order extract's main category | the category of the refunded item | same (one category an order) | the extract's own column |
| SF22 | the month a voucher belongs to | the UK calendar month it was issued in | the UTC month of `issued_at` | March GBP 9,837 and April 1,570 against 9,832 and 1,575; the half-year's refund-delay vouchers are one set either way (asserted) | the prompt: the value of the goodwill vouchers customer services issued in that UK calendar month |
| SF23 | a voucher given for a refund delay | every Refund delay voucher, the voucher's own reason, with no test of the refund's lateness | only vouchers whose refund was made on day 15 or later | 3,824 vouchers against 3,825 (one, issued 27 May for 7, on a refund made on day 14) (asserted) | the prompt: vouchers given for a refund delay |
| SF21 | the openings that take a parcel from the hall | every opening, rejected parcels included | only the openings that end in a refund | GBP 102,615, March and April (exact on 113,850 of 181,318 labelled openings) | a rejected parcel was delivered and opened like any other; the labelled openings, rejected ones included, are exact only when every opening pops the hall |

## Ladder

Every rung a complete pipeline, each filing a payment and breach months the golden does not (measured on the cut pack,
`generator/ladder.py`, figures.json `rungs`):

| Rung | Pairing | Payment | Breach months | Late refunds, January to June |
|---|---|---|---|---|
| 0 | the opening day read as the delivery day | GBP 0 | none | 0, 0, 0, 0, 0, 0 |
| 1 (default) | arrival order, the cumulative curves | GBP 189,330 | February, March | 2, 8,841, 3,779, 0, 0, 0 |
| 2 | 2025's monthly late shares carried | GBP 11,265 | none | 0, 751, 0, 0, 0, 0 |
| 3 | every waiting parcel equally likely | GBP 192,000 | February, March | 507, 5,582, 6,210, 501, 0, 0 |
| 4 | newest first by day (a day's parcels all waiting from its start) | GBP 128,580 | February, March, April | 0, 1,106, 5,287, 1,965, 145, 69 |
| golden | newest first by goods-in scan time | GBP 127,785 | February, March, April | 0, 1,106, 5,292, 1,935, 151, 35 |

Rung 4 is the half-handled step (the order found, the clock coarsened); the labelled openings reject it (exact on 205
of 181,318). The golden's month shares are 0.0, 7.1, 28.9, 14.5, 1.2 and 0.3 per cent, none within two points of the
5 per cent line.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | refunds made for goods returned to the Cotterby centre, January to June 2026 | filed, para 2(a); SF6 to SF8 |
| 2 | Unit of account | a refund (one per returned order) | filed; asserted one paid return refund an order |
| 3 | Attribution window | the made date's month | filed, para 3(ii), SF2 |
| 4 | As-of dating | the extracts' own records to 28 October 2026 | C1: every January to June refund is made and on file |
| 5 | Version basis | records that stand; the succeeding payment | filed, para 3(i), SF3, SF10 |
| 6 | Denominator | the month's refunds made | filed, para 2(c), SF13 |
| 7 | Weighting | none, a count | C1 |
| 8 | Window length | January to June 2026 | filed |
| 9 | Boundary inclusivity | day 15 or later is late; at least 95 per cent by day 14 meets | filed, para 3(iii) and 4, SF1, SF12 |
| 10 | Rounding path | exact counts, one-decimal shares of exact counts, the payment exact | asserted |
| 11 | Tie-break | no scan and opening share a second | C1 by construction, asserted |
| 12 | Maturity and censoring | every refund made by 30 June is on file; deliveries after its opening cannot pair | C1 |
| 13 | Order of operations | conform the two goods-in layouts into one UK-time record, then replay every opening in time order | C1: both exports are already UK time and every row is a return parcel, so no other order exists; SF21 asserts the refunds-only replay differs |
| 14 | Row order | the replay sorts by time | C1: no two openings and no two deliveries share a second (asserted, L7) |
| 15 | Duplicate resolution | one delivery a barcode | C1, SF5 (no barcode scanned twice, asserted) |
| 16 | Identity normalisation | barcodes and order references as written | C1 |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | days and refunds; pounds and pence in the ledger, unused by the call | C1 |
| 19 | Code and status semantics | RETURN, PAID and FAILED, REFUND and REJECTED - RETURNED TO CUSTOMER, RET | the systems' own codes; never the stump |
| 20 | Integerisation | counts are whole | C1 |
| 21 | Clause scope | para 2 to 5 apply to January to June 2026 | filed |
| 22 | Forward window contents | none; the window is closed | C1 |

## Literal reader

Executed word for word: the assurance fixes the population, made date, month, day count and commitment, so the only
open step is each 2026 refund's delivery day, which no record states. Every pairing a literal reader could pick is a
model; the records where the pairing is known (every 2025 opening and 2,503 labelled openings in 2026) admit exactly
one, the newest parcel waiting by scan time (181,318 of 181,318 exact), and its replay gives the golden. The
arrival-order reading is not a literal reading of any filed text; it is a model the labelled records contradict on
179,559 openings. SF1 to SF21 each close by a quoted sentence or converge (C1, asserted).

## Oracles

No control ties only under the golden. The daily sheet's waiting count closes under every pairing (it is a count); the
mean wait is order-free and ties under every pairing; the labelled openings are the prepaid scheme's own records of
which parcel was opened, the evidence the step is tested on, not a referee for the 2026 figures; no file states a 2026
delivery date, a late count or a payment.

## Ask sheet

Two asks, each on records the call never reads (the goodwill voucher system, its redemptions, the customer cases and
the order extract), each a component of the return the assurance or the stakeholder needs:

- **Ask A, each month's goodwill vouchers in pounds (6 figures, the CSV's last column).** H18 home: para 2(e) of the
  assurance. Primary device D3, a missing currency read as the house's: the voucher system writes each value in the
  customer's own currency with no currency column, so the Irish site's vouchers are euros; the order extract carries
  every customer's currency and the reporting rate (GBP 0.86 a euro on every euro order), and a voucher redeemed on a
  euro order is applied in euros. Pin test: the asking sentence pins the unit (pounds) and the month (the UK calendar
  month the voucher was issued in, SF22), never a currency; the device sits in which rows are euros. Stops: every value
  as pounds (GBP 3,393, 16,860, 10,003, 1,594, 1,250, 1,044 against 3,325, 16,561, 9,832, 1,575, 1,229, 1,023); every
  value converted as euros; refund-delay vouchers only.
- **Ask B, refund-delay vouchers by the category of the order the refund was on (12 figures, the note's table).** H18
  home: the stakeholder's remedial plan by product line. Primary device D7, the true key elsewhere: the voucher form's
  order field defaults to the customer's latest order, so a customer who ordered again before the voucher carries the
  new order (never returned, never refunded), while the case the voucher was issued on names the order whose refund
  was slow. Second layer D3 on the values. Pin test: the asking sentence pins vouchers given for a refund delay (the
  voucher's own reason, SF23) on orders in the category, the order the delayed refund was on, which the voucher's own
  field is not for 36 per cent of the half-year's vouchers; no sentence names the field or the case.
  Stops: the voucher's order field (counts 1,387, 656, 607, 498, 392, 285 against 1,523, 648, 621, 402, 356, 275 in
  the order Womenswear, Menswear, Footwear, Home, Kids, Accessories); the case's order with values as pounds (counts
  kept, values missed); dropping vouchers whose own order has no refund.
- Main population zero-counts: no voucher, case or redemption row is read by the call; the ask files carry no
  goods-in, processing or refund field the call uses. Hazards: UTC times on vouchers, cases and redemptions (the
  voucher's month pinned to the UK calendar month, SF22); partial redemptions; vouchers on cases with no order.
- Referee: none; each device is forced by its rows (a euro order's redemption applied in euros; a refund-delay
  voucher's own order with no refund of any kind).

| Ask block | Device | Figures | Careful cracker route | Cracker verdict |
|---|---|---|---|---|
| A, vouchers issued each month in pounds | D3 euros without a currency column | 6 | sums the value column as pounds | miss |
| B counts, refund-delay vouchers by the order's category | D7 the voucher's own order field | 6 | joins the voucher's order to the extract's category | miss |
| B values, the same in pounds | D7 and D3 | 6 | the voucher's order and the value as pounds | miss |

Full includer (the case's order, each voucher's currency from its customer's orders): reproduces figures.json, or
ceiling.py exits 1.

Pair ceiling: 32.0 (the cracker on the call 45.0, the mirror off it 19.0; measured on the cut pack).

Mirror leakage: 0.0 per cent of ask weight (the mirror runs the cracker's ask routes).

Measured by: generator/ceiling.py on the cut pack (two careful responses on the call at most 63.3 each, the best stop
on each ask).

## Leak sweep

`leak.py task467 --asof 2026-10-30` on the stage 3 cut and again on the stage 4 repair (target.zip
cb252556972e11e3389478083d3b5f04 both times, the repaired prompt of 983 characters): REVIEW, no LEAK, the same four lines.
Sweep 11 (a roll call in the prompt) and sweep 13 (the metadata title and subdomain in the stump's vocabulary) were fixed
in the generator at stage 3, not ruled: the prompt's third sentence no longer attributes a wish to Calvermoor, and the
title and subdomain say what the return decides and which systems it is conformed from. Each remaining line ruled:

- Sweep 3, the assurance carries 12 of 17 distinctive words of the committed call: harmless; the shared words are the
  return's own terms (Wrenfield & Holt, the goodwill fund, refunds made late, January to June) that the assurance
  defines; it states no payment and no late count (asserted, checks.py `Gate G` on both documents) and no month's late
  share or breach.
- Sweep 4, the assurance (records, goods-in, record, centre, returned, returns): harmless; the words fix day 0 at the
  centre's goods-in scan and give the Service sight of the records, which is the WHAT; nothing names a pairing, the
  hall, an order of working or the labels (asserted with a positive control, checks.py `Leak:`).
- Sweep 4, the 2025 review (goods-in, parcel, centre, returns, and since the pre-ship check entered the swept
  paragraphs, february and review): harmless; the words are the review's own title, date and month table, and it states
  the centre's 2025 volumes, its team and the new goods-in software, naming no pairing, order of working or label (same
  assertion).
- Sweep 9, 365 dates after 2026-10-30 in `wh_goodwill_vouchers_2026.csv`: harmless; they are the `expires_on` validity
  window of vouchers issued to 28 October 2026, the one forward-looking column on the H16 allow-list, and no other column
  in the pack holds a date after the extracts (asserted, checks.py `H16`).

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Rule 1: the deciding quantity is each 2026 refund's delivery
  day, a record link between the centre's goods-in scans and its processing records that no key carries, estimated by
  the linkage model the surviving labelled links validate (the newest parcel waiting opened first, 181,318 of 181,318)
  and replayed over 2026's own deliveries and openings; with a laboratory's racks or a records office's in-tray in
  place of the hall the question is still how two unlinked logs of one buffer pair, and no stated score, list or
  eligibility check decides. Rule 2: Layer 1 is the systems' own mess (the goods-in layouts either side of the 1 January
  software change, prepaid labels on the 2025 records and January's stragglers, failed card refunds reissued as store
  credit, the ledger's UTC stamps, the pence column from April; on the asks UTC stamps, partial redemptions, statuses
  as at the extract, cases with no order), each asserted neutral on the call (R2); Layer 2 is the linkage model tested
  on the surviving links. Rule 3: nothing planted (R3c, the documents' positive-control sweep), no field read decides
  (every field read right, arrival order still files GBP 189,330, R3a) and no filed rule performs the step: the
  assurance files the WHAT (paragraphs 2 to 5) and nothing says how the logs pair or how the hall is worked.
- **The decisive step is still analytical, on the built pack.** The same pipeline with only the pairing changed to
  newest first files GBP 127,785 with February, March and April (R3b); arrival order passes the textbook checks (the
  daily waiting count, the 2025 mean wait of 0.408 days under any order) and fails the labelled openings (1,759 of
  181,318) and the 2025 back-test (615 in February and 889 in December, which it puts at 0 and 0, L12); the half-handled
  reading by day files GBP 128,580 and matches 205 labelled openings; the standing member left (an empty hall on 1
  January) files the same call (SF11), and the 336-hour reading the assurance's calendar days rule out files GBP 127,995
  (SF1).
- **Determinacy on the built pack.** The judge on cb252556 reproduced the main call exactly (the replay 181,318 of
  181,318; 2025's 615 and 889; 2026's late refunds 0, 1,106, 5,292, 1,935, 151 and 35; GBP 127,785; February, March and
  April) and passed Gate H. Its FIX_NOW was on the asks only, two forks now closed in the prompt as the WHAT and asserted
  in checks.py: SF22, each voucher counts in the UK calendar month it was issued (the UTC month gives March GBP 9,837
  and April 1,570 against 9,832 and 1,575, one GBP 5 voucher issued at 23:50 UTC on 31 March); SF23, a voucher given
  for a refund delay is every Refund delay voucher by its own reason, with no test of the refund's lateness (the
  lateness test gives 3,824 vouchers against 3,825, one issued 27 May for 7 on a refund made on day 14). Its third note,
  the voucher's own order against the case's, stays closed by the data as the judge read it (SF18). `freeze.py check
  task467 --mode determinism` PASS against the architecture 2 snapshot taken before the repair: no graded figure moved.
- **Gate G.** The judge read analytical_non_defect. No shipped artifact ranks months or pairings: the daily sheet
  counts, the review states 2025's volumes and team, the assurance files the WHAT.
- **Stage 4, final record.** The leak reader read cb252556 clean twice: on the stage 3 prompt (Q1 to Q4 none, Q6 an
  analytical reconstruction, both sweep lines harmless) and on the pinned prompt (the pins read as filters, not
  methods). The judge returned FIX_NOW on the stage 3 prompt (the two ask forks closed above) and DETERMINISTIC on the
  pinned prompt: every figure reproduced (the main call, with GBP 189,330, 192,000 and 0 each ruled out by the labelled
  test or the assurance; the voucher values; the category table), Gate G analytical_non_defect, Gate H pass (noted
  borderline but analytical, since the data separate the candidates). Its last FIX_NOW was wording only and is fixed
  with no rerun: critical component 1 and step 3 now give the labelled openings as every opening to the end of 2025 and
  the labelled stragglers opened to April 2026, and the note's sentences on the labelled span, the 2026 parcels with no
  shared reference (apart from the 2,503 stragglers), the voucher's own order field and the backlog (most of the late
  refunds from January's deliveries, those made in May and June from May's) now read literally true against the records,
  each asserted (L12, SF18) or derived from the replay in golden.py. The residual it asked measured on the category
  table: of the 1,631 vouchers whose own order differs from the case's, 26 own orders had a refund, 4 of them made late,
  all Damaged item, Delivery delay or Other vouchers; on Ask B's 1,378 Refund delay vouchers none had a refund of any
  kind or a processing record, so the case's order stays the only reading (SF18, lesson 8) and the pack is unchanged.
  The reader's two mild tells, ruled: the 2025 review's received total equals its opened total (167,730) because the
  records carry no year-end carry-over (the hall is empty at the close on 31 December 2024 and on 31 December 2025,
  every parcel delivered before each year end opened by it), so the review states the records as they are, and a
  carry-over would move the main call (SF11); the voucher values run from 5 to 40 because the voucher policy pays a
  tenth of the case order's value in whole units of the customer's currency with a floor of 5 and a cap of 40, and
  changing it would move Ask A's and Ask B's graded figures, which a determinism repair freezes.
- **The ask layer.** The cracker misses 18 of 18 ask figures; the mirror keeps none (leakage 0.0 per cent); pair
  ceiling 32.0; two careful responses on the call reach 63.3 at most (generator/ceiling.py).
- **Every gate on the final cut cb252556** (2026-11-02, after the wording fix): checks 89 assertions, 0 failures;
  verify, every figure recomputed from target/ alone; two builds byte-identical; target.zip md5
  cb252556972e11e3389478083d3b5f04, unchanged through stage 4 (the pins sit in the prompt and the wording in the
  write-up and the note; no pack file moved); freeze determinism PASS against the architecture 2 snapshot; precut 61
  checks, 0 FAIL, 0 WARN; voice-check PASS (983 characters); figures_check 84 figures, 0 absent; leak.py REVIEW with no
  LEAK, every line ruled in `## Leak sweep`; guard surface exit 0 (8 pairs promoted for the author's adjudication, the
  same as stage 3); guard heart WARN (window artifacts answered in the Draw); scrub audit clean in target/ and golden/.
- **House fixes run.** H1: no producer signature or out-of-band timestamp in target/ or golden/; H4: the archive's
  members are target/'s, flat, no enclosing folder; H8: every file the write-up cites ships under that name; H9: no file
  describes the pack (the documents' sweep and R1's column check); H16: no date past the extracts but the vouchers'
  `expires_on` (asserted); H21: the council, the trust and the carriers renamed off near-real names; H25: both PDFs in
  the pack read the same control sentence through pypdf and pdfminer.

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
- 2026-11-02, stage 2: the stochastic picking mix of the first draft (the oldest bay first in about three picks in
  five, any waiting parcel otherwise): its golden is a distribution, not one number (a judge's own draws, the closed
  form against a simulation, the share pooled or by month each land different exact counts), so on the coordinator's
  direction the hall is the deterministic order the records show, block-stacked cages giving up the newest parcel
  waiting, whose replay is exact; the 2025 peaks (February and December) carry the deep-queue back-test.
- 2026-11-02, stage 2, the ask layer's first forms, each dropped before a figure was graded: slow-refund vouchers by
  month (their mass sits in February and March, so January, May and June carry a handful each and the cracker keeps
  them); cancellation refunds timed from the customer's email while the order system logs the agent's keying (a
  recorded time standing in for the event, this batch's spent family); order amendments coded as web cancellations
  (the system did cancel the order, a coherent literal reading); first responses counting the automatic
  acknowledgement before a case-system release (every overnight contact answered within a minute, an inspection tell);
  a budget-rate workbook beside the vouchers (it announces that some values are not pounds; the rate now rides on the
  order extract's reporting column).
