# task166 design note

Architecture 4, drawn 2026-11-01 (Batch 5 queue, wave 4, oviya1301's backlog; Forecasting lane). The slot's three earlier
architectures were each landed on the portal by the field's named method executed by reflex: architecture 1 (10-25, the
bank's commercial real estate balloons extended on refinance cover), architecture 2 (10-26, the credit union's home equity
payoffs off the whole stack's blended rate, chosen on fit and back-test) and architecture 3 (shipped 10-27; the author's
Batch 5 sheet of 10-31 records the call as landed: the Southwest's founders linked to the users who left paying
customers through the directory's one mobile key). Nothing of them is kept: this draw is another world (a UK trade
publisher's year-end sale-or-return allowance), another dataset and another prompt shell, away from task144's axes
(product-analytics, feature-adoption-diffusion-modeling, software_or_platform). The field's own development of returns
sits at the bottom of the ladder and files a wrong answer; the decisive step is the precondition this book violates.

## Draw

| Item | Value |
|---|---|
| Card | `cards/task166.json` v4, registered 2026-11-01T22:03:36Z at WARN; v1, v2 and v3 in its lineage with their fates; `lineage_shells` holds v3's shell read off its shipped prompt and v1's and v2's deliverable sets |
| Pairing | accounting-audit-forensic (house) / revenue-receivables, client domain actuarial-science-insurance through its task type reserving-development-triangles, Forecasting & Predictive Modeling |
| World | Marrowgate Books Ltd, an independent London trade publisher (literary, crime, commercial and children's imprints) selling on sale-or-return through its distributor, Tallowmere Book Distribution, to a national bookshop chain, online retailers, wholesalers, a supermarket supplier, independent shops and export accounts; financial year to 31 October |
| Call | how much Marrowgate should hold as its returns allowance at the 31 October 2026 year end against trade sales invoiced to that date, and how much of it is for hardbacks: the credit it expects to give for copies already invoiced that accounts will send back under the terms of trade |
| Shape | other: the allowance and its hardback part (2 graded figures, to the nearest £250,000), then two asks on the distributor's returns records the call never reads: the copies of Marrowgate titles received back in each quarter of FY2026 by channel (24 cells) and the share of those copies written off by the year end by channel (6) and by format (3); 35 graded figures and the two files |
| Decision type, unit | quantity_figure, currency (GBP) |
| Strategy | composition_mix: the autumn 2026 hardback cohort differs from every cohort the development was measured on in a property no column names, the months from a hardback's publication to its own paperback's |
| Gap, pattern, generators | time then population; E (a hardback's remaining shop stock comes back on its paperback's on-sale date); G14, G13 (the paperback falls inside the returns window the history's hardbacks rarely exercised), G6 |
| Gate G | forecasting |
| Layer 2 | field_method, `own:hardback-returns-conditioned-on-its-paperback-date` (the client card `actuarial-science-insurance/reserving-development-triangles/1` warns that a development method assumes a stable pattern; here no triangle shows the change, which sits in the forthcoming paperbacks) |
| Forum, forcing event, org, role | auditor (the year-end audit of the allowance); period_close (the 31 October 2026 year end); media_or_publishing; finance_controller (Group Financial Controller) |
| Context artifact, calibration | published_series (the trade's weekly UK consumer sales panel beside the ledger); none |
| People | Hilary Singh (Group Financial Controller), Marc Hudson (Head of Sales Operations), Jade Hewitt (the distributor's returns manager), from `guard.py names --geo "United Kingdom" --seed 166`; none appears in the prompt |
| Deliverables | `returns_allowance_FY2026.xlsx` (the allowance, its parts and workings, the two asks' tables) and `returns_allowance_note.pdf` (one page: the allowance, its hardback part, how it was built) |
| Shell | how-much / build / pdf+xlsx, against v3's how-many / send / docx+xlsx and v1's and v2's which questions with pptx+xlsx and png+xlsx |
| Seed | none: drawn without a seed; world `s110` of the generator's sweep (`common.WORLD`), chosen on the back-test, the bin placement and the separation, recorded below |

**The guard's answers.** `guard.py check` on the registered card: WARN, no BLOCK.
- overuse.objective, repeat.gate_g and overuse.gate_g (forecasting, task273 v5 and task157 v3): the number belongs to the
  Forecasting lane and the allowance is a forecast of credit still to come; Gate G forecasting is that objective's
  natural mechanism, and neither neighbour shares the world, the decision or the driver.
- test.same_puzzle_older and test.same_driver_older (time, E, quantity_figure and forecasting): differentiated on the card
  line by line against task117, task137's lineage, task171's lineage, task37, task44, task481, task97 and task155; each
  conditions a yield on something else (draw caps through a dated join, a repricing gap, an own saving, a linked entity's
  authorisation, a pilot's moderator, a dual-coded window, a place's history, a scheduled task's continuity), none on a
  successor edition that sends its predecessor's stock back.
- test.own_lineage against v1 (time, E, forecasting): differentiated; v1 conditioned a borrower's own extension option on
  refinance cover under a rate path, here there is no option and no rate.
- ban.artifact cleared by redrawing the context artifact: filed_standard (task273 v5), register (task464) and
  operations_log (task157 v3) are held by the last three builds; published_series is the honest label for the consumer
  panel the finance team reads beside its ledger.
- Nearest drivers 0.05 to 0.07 (task43's lineage: a pooled effect carried onto a cohort with another mix of a moderator;
  task146; task137 v2; task157 v1; task173 v1). The closest in kind is task43's: a correct pooled quantity carried onto a
  forward cohort whose mix on a property differs; there the moderator was a behaviour in a pilot, here it is a date on
  another record (the paperback's) that only a title-and-contributor match reaches.

**Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the same): a
returns pattern measured on past cohorts is carried onto a cohort whose successor products arrive sooner. No approved
build says it: task132 restarts a wear curve when an item is replaced (the successor resets a hazard; here it ends the
predecessor's sales and sends its stock back), task107 lifts a rate at a fixed anniversary, task175 reads a lot's chance
off its street's fill and task124 a verified share within a kind of main.

**Data-native sentence.** A bookshop keeps a hardback face-out until the paperback of the same book arrives, then sends
what it has left back for credit, so a hardback's returns are set by when its own paperback goes on sale; Marrowgate's
returns history ran its hardbacks off with paperbacks about a year behind them (17 of the 253 hardbacks published from
August 2021 to October 2025 had a paperback within eight months), while 23 of the 26 autumn 2026 hardbacks have their
paperbacks listed on the title master as forthcoming titles four to five months after publication, under their own
ISBNs and often retitled.

**A line per source.**
- The client card `reserving-development-triangles` 1 (changing settlement speed distorts paid development; a development
  method assumes a stable pattern) supplies the precondition; the card's own fix (a disposal-rate adjustment read off
  closed counts) is not this build's step, because no triangle here shows the change.
- `stumping` 1.1b: the field's development of returns by format, channel and weeks since invoice is rung 0 and rung 1 and
  files the wrong allowance; the decisive step is that the autumn 2026 hardbacks violate its precondition.
- `stumping` 1.4, the survivor anatomy: the deciding property (months from a hardback to its own paperback) has no column;
  it is read through a title-and-contributor match between a sold hardback and a forthcoming paperback, which no key
  offers.
- The portal's three landings on this slot (`## Tried and rejected`): each was the field's named correction found because
  something announced it (a cover metric, a stack's rate, a removals surge with a key on every row); here nothing is loud:
  the autumn list's subscription copies sit inside the earlier autumns' range and its forthcoming paperbacks are ordinary
  catalogue rows among the season's forthcoming titles.
- Industry practice (no source shipped): sale-or-return is the UK trade's standard term, and a hardback's sales fall away
  when its paperback is published; publishers schedule paperbacks six to twelve months after the hardback.

## Three rules

- Task type: actuarial-science-insurance / reserving-development-triangles, which serves Forecasting: the allowance is a reserve for credit still to be given on copies already invoiced, developed by weeks since invoice from the returns history.
- Domain test: the quantity that decides the call is the expected credit for copies already invoiced that will come back under sale-or-return, which a reserving analysis develops from the returns triangle by format, channel and weeks since invoice (a chain ladder on returned shares, the field's method); the hardbacks' development turns on when each hardback's own paperback goes on sale.
- Swap: "how much should a hospital trust hold against readmissions of patients already discharged": a discharged patient has no successor edition whose publication sends the predecessor back, so the paperback dates that decide this call stop meaning anything.
- Layer 1: the organisation's own systems produce every mess item: the February 2023 ledger system change (legacy six-digit account numbers crosswalked on the account master, ISBNs hyphenated on the older lines), titles first catalogued in the old bibliographic system (contributor written surname-first, formats coded HB, TPB and PB), the distributor's own consignor references against Marrowgate's account codes, its exports starting November 2024, one day's export sent twice, hub and depot consignments booked carton by carton, other publishers' copies in a client's parcel, copies sent beyond an authorisation, a delivery booked in a second time, hurts re-inspected in two sessions or recounted after a query, the re-inspection workbook gaining an inspector column from August 2026, the panel's Saturday week ending and the October financial year against calendar quarters; nothing is placed to be caught, and none of it moves the call.
- Layer 2: the field's method and its precondition: a returns pattern measured on hardbacks whose paperbacks came about a year later does not carry a cohort whose paperbacks come four to five months later; giving those hardbacks their own pattern, read off the earlier hardbacks with a paperback that close, moves the allowance from £1.25 million to £1.75 million.
- Decisive step: recognising that a hardback's remaining shop stock comes back once its own paperback goes on sale, finding each hardback's paperback on the title master by title and contributor (often retitled, under its own ISBN, the contributor written two ways), and giving the hardbacks whose paperback comes within eight months their own returns pattern from the earlier hardbacks with a paperback that close.
- Not semantics: every field reads plainly (an invoice line, a credit quoting it, a format, a publication date, a forthcoming status) and reading all of it correctly still leaves every development on the history's pattern, because the deciding quantity, each hardback's months to its own paperback, is in no field and is built only by matching two catalogue rows no key joins.
- Not rule application: no filed rule says a paperback sends its hardback back or ties the two editions; executing the terms of trade (returns quote invoices three to twelve months old, matched earliest first, credited at the matched invoice's net price, lapsing after 60 days) and the policy's definition gives the history's figure; measured on the pack, the enumerated family without the step (18 developments: format or format and channel, maturity 400 to 450 days, all years or the last two or three) spans £1,295,941 to £1,363,118, all £1.25 million, and the standing family with the step (60: threshold 6 to 10 months, with or without channel, maturity 400 to 450 days, all years or three) spans £1,743,388 to £1,809,287, all £1.75 million; the ruling-out is quiet, a date on another catalogue row.
- Analyst test: with every channel, migrated account number, credit and transit claim read correctly, the easy route develops returns by format, channel and weeks since invoice on the five-year record (or takes a trailing twelve months' rate), back-tests it within 3.4 and 1.2 per cent at the 2024 and 2025 year ends and holds £1.25 million (computed £1,358,042); it never ties a forthcoming paperback to its hardback, so the autumn 2026 hardbacks are developed on a history whose paperbacks came about a year later.
- Estimand: the accounting policies (`marrowgate_accounting_policies_FY2026.pdf`) define the allowance as the credit the company expects to give, under its terms of trade, for copies invoiced on or before the balance sheet date that will be returned, transit claims no part of it; the terms of trade (`marrowgate_terms_of_trade_2024.pdf`) file who may return what (sale-or-return accounts, copies invoiced three to twelve months before the authorisation, matched earliest first, credited at the matched invoice's net price, lapsing after 60 days); the prompt fixes the date (31 October 2026), the unit (pounds) and the hardback part.
- No decoy: nothing is planted: the autumn list's paperback dates are the publisher's own schedule on its title master, no memo, model or file argues for the history's figure or ranks anything, the print orders and stock on hand are declared distractors in `metadata.json`, and the panel is a published series beside the ledger.
- No certified replay: no certified or published figure is reproduced to recover a method: no prior allowance, audited working or reserve file ships, and the development and its split are estimated from the invoices and the credits that quote them.
- Lesson: a reserving analyst learns to ask what ends a cohort's returns before carrying its history forward: where a successor product sends a predecessor's stock back, the successor's date sets the pattern, and a schedule that brings it forward moves the reserve where no triangle shows it; no build on file conditions a reserve on a successor edition's date found by matching catalogue rows.

## Survivor anatomy

- Actor: the hardback still in its returns window has rows (its invoices, the credits quoting them, its panel sales); the deciding property, the months from its publication to its own paperback's, has no column in any file: the title master lists the paperback as its own ISBN with its own publication date and often a changed title, and nothing on either row names the other.
- Link: the signal is read through a match no key offers: a hardback joined to its paperback by title and contributor across the title master's published and forthcoming rows (a subtitle added, an article dropped, an ampersand, the contributor written surname-first on the older rows); an exact join finds 234 of the 550 pairs and only 8 of the 23 autumn 2026 quick paperbacks, and the field's development of returns never asks for the comparison.
- Reflex: the field's method for the deciding quantity, the development of returns by format, channel and weeks since invoice (or a trailing twelve months' rate), sits at rung 0 and rung 1 and files £1.25 million (computed £1,358,042 and £1,254,879), `Ends on:`, not the golden.
- Back-test: the textbook route validates: the same development struck at 31 October 2024 and 31 October 2025 comes within 3.4 and 1.2 per cent of the credits that followed on the copies then open, because every cohort it was measured on had its paperbacks about a year behind.
- Second use: every file the decisive step reads sits in the pack for its own reason: the title master gives every route its formats and publication dates, the ledger is the development's own record; the step reads no file the default path does not already read, and none drops out when the step is deleted.
- Shock: the movement the step recovers reads as ordinary: the autumn 2026 hardbacks' subscription copies (279,219) sit inside the earlier autumns' range (128,783 to 437,756) and their forthcoming paperbacks are ordinary catalogue rows among the season's forthcoming titles; no file's largest movement is the step.
- Pins: the WHAT is filed in the accounting policies and the terms of trade (what the allowance is, who may return what, within how long of which invoice, at what credit) and no filed sentence names a paperback, a successor edition, a publication schedule or a development clock.

## Default path

1. Read the policy and the terms: the allowance is the credit to come for copies invoiced on or before 31 October 2026; a return quotes an invoice three to twelve months old, matched earliest first, credited at that invoice's net price.
2. Load the sales ledger's invoice and credit lines (FY2022 to FY2026), map the legacy account numbers through the account master, strip ISBN hyphens, attach format from the title master (HB, TPB and PB mapped) and channel and terms from the account master; keep sale-or-return accounts and returns credits, leave transit claims aside.
3. Tie each returns credit to the invoice it quotes and build the triangle of returned copies by weeks since invoice, by format and channel, on invoices from November 2021 at least 425 days old.
4. Develop it the field's way: each invoice line of the last twelve months takes the share of copies still to come after its age, at its own net price (a chain ladder on cumulative returned shares, or a trailing twelve months' rate phased by the lag profile).
5. Back-test the method at 31 October 2024 and 2025 against the credits that followed: within 3.4 and 1.2 per cent.
6. Sum over open invoice lines and round.

Ends on: £1.25 million (computed £1,358,042; hardbacks £631,889)

Golden: £1.75 million (computed £1,801,556; hardbacks £1.0 million, computed £1,075,403)

## Stump sentence

The default path develops returns by format, channel and weeks since invoice on the five-year record, back-tests within 3.4 and 1.2 per cent at the 2024 and 2025 year ends and holds £1.25 million (computed £1,358,042); the step that lands it there is developing the autumn 2026 hardbacks on the history's pattern, when their paperbacks, listed on the title master as forthcoming titles under their own ISBNs and often retitled, are due four to five months after publication instead of about a year, so the stock shops kept to sell through the spring comes back once each paperback is out and the allowance is £1.75 million.

## Readability screen

Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second use. The reflex row is
enumerated from the field's vocabulary for the deciding quantity (a returns reserve): trailing return rate, chain ladder
on returned shares, development by segment, Bornhuetter-Ferguson on sell-through, a back-tested selection among them.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 trailing twelve months' rate by format and channel, £1,254,879 | silent | silent | fires (the auditor's first check) | silent | silent | silent | silent | readable |
| 1 development by format, channel and weeks since invoice, £1,358,042 | silent | silent | fires (the field's method) | the back-test confirms it | silent | silent | silent | readable |
| 2 the paperback split on an exact title and contributor join, £1,481,409 | silent | silent | silent | silent | silent | silent | silent | silent |
| 3 (decisive) the hardbacks developed by their own paperback's date, matched by normalised title and contributor, £1,801,556 | silent: no clause names a paperback, an edition or a schedule | silent: no column names another edition | silent: no reserving reflex conditions a cohort on a successor's date | silent: the back-test passes the rung below | silent: nothing in the battery matches catalogue rows | silent: a match, a new segment and its own pattern from the analogs, not one ratio | silent: the title master and ledger are every route's files | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "returns allowance" | credit for returns only | transit claims kept in the development | £1,801,753, same call | the policy: transit claims form no part of the allowance; asserted inert |
| SF2 | "trade sales" | sale-or-return accounts' invoices | firm-sale accounts kept in | £1,798,924, same call | the terms, section 4 (firm sale may not return); asserted inert |
| SF3 | "invoiced up to that date" | invoices of the twelve months to 31 October 2026 open | invoices up to 16 months old kept open | £1,819,683, same call | the terms (three to twelve months); asserted inert |
| SF4 | credit value | each open line's own net price | the segment's average net price | £1,787,701, same call | the terms (the matched invoice's net price); asserted inert |
| SF5 | development unit | weeks since invoice | months since invoice | £1,743,547, hardbacks £1,064,899, same call | same call, asserted |
| SF6 | which hardbacks are early | paperback within 8 months | any threshold from 6 to 11 months | £1,801,556 at every threshold | no paperback falls between 5.4 and 11.3 months; asserted |
| SF7 | "hardbacks" | format Hardback, legacy code HB included | current label only | legacy titles would drop out of the triangle | the title master's own codes; asserted |
| SF8 | rounding | nearest £250,000 from the computed figure | rounding parts first | £1.75 million either way (40,000 or more from both edges) | the prompt; asserted |
| SF9 | "each quarter of the year to 31 October 2026" | financial-year quarters, November to January first | calendar quarters | different cells | the prompt's year to 31 October and the policy's financial year; asserted |
| SF10 | "written off" | graded unsaleable on receipt plus hurts pulped at re-inspection by the year end | graded unsaleable only | every share lower | the policy: pulped copies are written off; asserted |
| SF11 | "copies of our titles" | ISBNs on Marrowgate's title master | every row the distributor booked | other publishers' copies counted | the prompt's "our titles"; asserted |
| SF12 | a receipt's channel | the channel of the authorisation's account | the consignor reference read as an account | unmapped rows | the consignor references are the distributor's own, the authorisation names the account; asserted |
| SF13 | copies sent beyond an authorisation | received (held for collection) | capped at the authorised copies | 6 of 24 cells right | the terms: such copies are held for collection, so they came in; asserted |
| SF14 | "how much of it is for hardbacks" | the allowance on hardback invoice lines | the hardbacks' share of open net value | another figure | the prompt's "of it"; asserted |
| SF15 | how the credit still to come is estimated | each open line's share still to come after its age, at its own net price | expected ultimate share less the credits already given on the same invoices | £1,917,690, the £2.0 million bin | the record: struck at 31 October 2025 that estimator overshoots the credits that followed by 14.2 per cent against 0.2 per cent for the golden's (2024: 1.1 against 0.6), because a cohort running below the pattern does not catch up; asserted |
| SF16 | a tote's pulped copies in whole copies | shared in proportion to hurts | whole copies by largest remainder within each tote | the same share in every cell (Online 10.1514 against 10.1501) | same call, asserted; rounding each line on its own breaks the tote's pulped total |

## Ladder

| Rung | Route | Allowance | Hardbacks | Graded |
|---|---|---|---|---|
| 0 | trailing twelve months' returns rate by format and channel, phased by the lag | £1,254,879 | £601,308 | £1.25 million |
| 1 | development by format, channel and weeks since invoice (the field's method; 18 variants £1,295,941 to £1,363,118) | £1,358,042 | £631,889 | £1.25 million |
| 2 | rung 1 with the hardbacks split by their paperback on an exact title and contributor join (8 of 23 autumn 2026 paperbacks found) | £1,481,409 | £755,256 | £1.50 million |
| 3 | the golden: the split on the normalised match (60 variants £1,743,388 to £1,809,287; hardbacks £1,047,196 to £1,092,910) | £1,801,556 | £1,075,403 | £1.75 million, hardbacks £1.0 million |

The credit realised on the clean world after the year end on copies invoiced to it is £1,722,405 (also £1.75 million).
Golden over rung 1: 1.327. Gate F on the clean truth: of the cheap routes (the trailing rate, development by format and
channel, by format alone, by months), none lands the call (`checks.py` R3c); every route that lands it takes the step.
The back-test (rung 1 at the 2024 and 2025 year ends, -3.4 and -1.2 per cent) validates the rung below the golden.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | sale-or-return invoice lines dated on or before 31 October 2026 still within a return's reach | filed: the policy and the terms; SF2, SF3 asserted inert |
| 2 Unit of account | pounds of credit; copies for the asks | the prompt names both |
| 3 Attribution window | an invoice line belongs to its invoice date; a receipt to its received date | C1: nothing graded sits on a boundary (SF9) |
| 4 As-of dating | 31 October 2026, records to 30 October | filed in the prompt; the credits after it are the future |
| 5 Version basis | one ledger, one title master as at 30 October 2026 | C1, one version shipped |
| 6 Denominator | copies invoiced on mature invoices, by segment | the field's method; SF5 asserted inert |
| 7 Weighting | copies, pooled within segment | C3 corridor: format or format and channel, same bin (R3b) |
| 8 Window length | invoices from November 2021, maturity 400 to 450 days, all years or three | C3 corridor: every variant in the bin (R3b) |
| 9 Boundary inclusivity | on or before 31 October 2026 | C1: the year end is a Saturday, nothing invoiced on it |
| 10 Rounding path | round the computed total once | filed in the prompt; SF8 |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | only invoices at least 400 days old build the pattern | C3 corridor (R3b) |
| 13 Order of operations | segment, develop, then sum | C1: additive |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | the receipts' second bookings and the re-sent day (asks only) | the asks' devices; the call reads no duplicate |
| 16 Identity normalisation | legacy account numbers, hyphenated ISBNs, retitled paperbacks | the account master's crosswalk; the normalised match is the decisive step's own work, asserted complete and exact (F) |
| 17 Netting against gross | returns credits only | SF1 |
| 18 Dimensional units | pounds, copies | C1 |
| 19 Code and status semantics | HB, TPB, PB and the current labels; RET against DIT | SF7, SF1 |
| 20 Integerisation | copies whole, money to the pound | C1 |
| 21 Clause scope | the 2024 terms govern returns authorised from 1 March 2024; the sale-or-return section unchanged since 2019 | filed in the terms |
| 22 Forward window contents | the credits still to come on copies invoiced to the year end | the forthcoming paperbacks on the title master are the shipped driver for the uncovered span |

## Literal reader

Read word for word, the policy's estimand (the credit expected under the terms for copies invoiced on or before the
balance sheet date that will be returned) and the terms (sale-or-return accounts, invoices three to twelve months old,
earliest first, the matched invoice's net price) leave one open question, how the credit still to come is estimated; the
literal reader's every development of the record (18 without the step, 60 with it) prints £1.25 million or £1.75 million,
and nothing filed chooses between them: the data do, because the hardbacks whose paperbacks come within eight months come
back on another pattern and the autumn 2026 list is almost all of them. No reading of a term moves the call (SF1 to SF8 and
SF14 inert or ruled out by a quoted sentence); the asks' terms (SF9 to SF13) are each closed by the prompt, the policy or
the terms.

## Oracles

None arbitrates the call. The back-test confirms the rung below the golden (both year ends within 3.4 per cent), the
panel's sell-through agrees with every route, and no file holds a prior allowance, a reserve or the realised credit after
the year end. On the asks, one byte-clean referee exists by design and hands over no level: the ledger credits each
authorisation line once, so a reader reconciling receipts to credits sees that some lines were booked beyond what was
credited, which second bookings and copies sent beyond an authorisation both produce; it separates neither from the
other, and no control ties only under the golden.

## Ask sheet

**Ask A, copies of our titles received back by channel and FY2026 quarter (24 cells, whole copies).** Primary D1: a
delivery booked in a second time by another goods-in clerk (83 in the export, every channel and quarter but three
Supermarket cells), each a line-for-line repeat that takes its authorisation lines past their authorised copies by exactly
the copies repeated; its over-cleaning half is genuine: hub and depot consignments booked carton by carton under their own
references, many cartons of one title alike in copies and some alike in every grade, and parcels split across days. A
second primary D5: copies sent beyond an authorisation, booked as received and held (the terms say so), so capping at the
authorised copies over-corrects. Hazards: other publishers' ISBNs in a client's parcel (D5) and one day's export sent
twice (D1, the battery's). The repair is a reconstruction across two systems: which repeated reference is a second
booking is read from the authorisation file's copies, not from the receipts.

**Ask C, the share of those copies written off by the year end, by channel (6) and by format (3), one decimal.** Primary
D6: a tote's pulped copies are recorded once per tote and must be shared among the deliveries whose hurts went into it,
in proportion to those hurts (the receipts give each delivery line its tote). Primary D1/D2 from another family: a big
tote worked in two sessions (rows adding to the tote's hurts) against a tote recounted after a query (each row the full
quantity, the later standing), told apart only by comparing the rows with the hurts the clean deliveries put into the tote.
Shared hazards: Ask A's second bookings (they double a tote's hurts and the denominator) and other publishers' copies.

| Ask | Cracker (duplicates out, our titles, every filed rule, the battery) | Mirror (the most attractive wrong rung) | Full includer | Cracker verdict |
|---|---|---|---|---|
| A received, 24 cells | 3 of 24 (second bookings kept) | 0 of 24 (duplicates out only) | 12 of 24 (every repeated delivery dropped, grades included) | miss |
| C written off by channel, 6 | 0 of 6 (last re-inspection row per tote) | 0 of 6 (graded unsaleable only) | 4 of 6 | miss |
| C written off by format, 3 | 0 of 3 | 0 of 3 | 1 of 3 | miss |

Other routes measured on the cut pack: every row kept 0 of 24; a repeated authorisation line and quantity dropped 11; with
grades 11; capped at the authorised copies 6; the ledger's returns credits read as receipts 4; re-inspection rows summed 0
of 9; a tote's pulped copies on every line of it 0 of 9; second bookings kept 0 of 9.

Pair ceiling: 29.1 (the cracker on the call keeps 5.2 of 57 ask points, 48.2 in all; the mirror off the call keeps none, 10.0; a full includer on the call keeps 29.4, 72.4 in all, and with the mirror the pair is 41.2)

Mirror leakage: 0.0 per cent of the ask weight (no cell of either ask under the mirror's route)

Measured by: generator/ceiling.py on the cut pack (sha256 recorded in its output; it prints the cracker, the mirror and the full includer), its routes asserted in generator/checks.py

## Layer 1 inventory

| Mess | The system that produces it | Touches |
|---|---|---|
| Legacy six-digit account numbers on ledger lines before 6 February 2023 | the ledger system change; the account master keeps the old number beside the new code | the call's channel join |
| ISBNs hyphenated on the older ledger lines and on the distributor's files | the old ledger and Tallowmere's exports format ISBNs; the new ledger and the panel do not | every join |
| Contributor surname-first and formats HB, TPB, PB on titles first catalogued before 2023 | the old bibliographic system | the call's format and the step's match |
| Paperbacks retitled or subtitled against their hardbacks | the publisher's own titling | the step's match |
| Consignor references | Tallowmere's own account references | the asks' channel join |
| Distributor exports from November 2024 | Tallowmere's retention for client extracts | the asks |
| One day's export sent twice | Tallowmere's export job | Ask A, Ask C |
| Carton-by-carton booking of hub and depot consignments | Tallowmere goods-in | Ask A |
| Other publishers' copies in a parcel | shops packing returns | Ask A, Ask C |
| Copies sent beyond an authorisation, held | shops packing returns | Ask A |
| Second bookings of a delivery | two goods-in clerks | Ask A, Ask C |
| Re-inspection in sessions or recounted | Tallowmere's hurts bench | Ask C |
| Inspector column from August 2026 | the re-inspection workbook's layout | none |
| Panel weeks ending Saturday | the panel's own calendar | none graded |
| October financial year | Marrowgate's year end | Ask A's quarters |


## Stage 4 rulings

- leak.py sweep 12 (REVIEW): the terms of trade and the accounting policies use words the data files also carry
  (received, re-inspected, restocked, pulped, terms, title) in their own sentences; the leak reader read both as the
  organisation's own records. Harmless.
- leak.py sweep 13 (LEAK, fixed): the licence string's version number matched the hardback part's "1.0"; the licence is now
  written without it.
- Leak reader, invoice numbers beginning SI26 on 2021 invoices: a running sequence. Harmless.
- Leak reader question 5, "will be returned" read as excluding copies already credited: the golden's estimand. Harmless.
- leak.py sweep 4 (REVIEW): the terms of trade carry "months", "credit" and "invoice", the words of its own return window and
  credit price; it names no paperback, edition or schedule. Harmless.
- leak.py sweep 9 (REVIEW, run with the as-of date): the title master's forthcoming editions are dated after 31 October 2026,
  the forward-looking catalogue rows every route reads, each with status Forthcoming (asserted in `checks.py`). Harmless.
- Determinism judge, pass 1: DETERMINISTIC, APPROVE, Gate H analytical; its one flagged residual, expected ultimate less
  credits already given (about £1.92 million), closed by the record as SF15, and the golden's own back-test added to the
  write-up as step 5 (no graded figure moved). Its note that Online's written-off share is 10.1501, just above the 10.15
  edge, is exact under the filed handling and under whole-copy allocation by largest remainder (SF16).

## Tried and rejected

- The mortgages' prepayment by refinancing incentive as the decisive step (the brief's first idea), worked at the
  draw: an incentive curve fitted to the bank's own loan history is the field's textbook construction and the strong
  solver's reflex, and as a decisive step it is task137 v1's driver (a behavioural share stable only per unit of the
  rate gap) in mortgage nouns; kept as the default path's own correction, the rung that moves the mortgages off the
  call, never as the step that lands it.
- The +200 bp loss with behaviour re-projected under the shock (negative convexity) as the decisive step, prototyped:
  with the policy's swap-curve discounting the in-the-money mortgages' extension under the shock adds value (their
  coupons sit above the shocked curve), so the re-projected loss came out at half the static one (3.1 against 6.2 per
  cent of balance), and with product-rate discounting the scheduled-only and flat-hold routes land on the same pool as
  the golden; the policy files the base-case cash flows, re-discounted.
- Burnout (a pool's response falling with its time already in the money) as the decisive step: the 2023-24 vintage
  has already been through the 2024 and 2025 rate dips, so burnout slows it, which puts the golden on the pool every
  flat-hold route picks; and the latent-depletion structure sits in task137's family.
- Seasoning (a hazard by loan age) as the decisive step: task134 v2's driver, and an age covariate any full model
  carries.
- Eligibility as a forecast (a pool eligible only if its base-case balance stays above the notional to the swap's
  maturity, the portfolio layer method's own test): an eligibility check deciding the call is a backdrop and a
  threshold on a forecast; eligibility is filed as a plain fact on the designation-date balance.
- A first card with the honest keys gap time and pattern E blocked on the older same-puzzle and same-driver
  signatures; the keys were kept (pattern C was the other candidate and does not describe a conditioned share) and
  each older build got a differentiation line on the card.
- Redfern Capital Markets as a dealer's name, at stage 3: a letter from a real Florida real estate investor (H21); renamed
  Larkmoor Capital Markets, no figure moved.
- A soft extension response (a logistic scale of 0.05 in cover) with the push's balloons spread across the break, at
  stage 4 round 1: a data-chosen hard cut at 1.18 to 1.20 scored the best hold-out Brier and filed 160 to 161, and a
  constant share of 0.68 to 0.83 on every balloon landed the $150 million bin (0.75 gave 149.3); the $25 million bin
  could not narrow that band. Rebuilt with a sharp break near a cover of 1.10, half the push written as lower-leverage
  refinances, the bin cut to $10 million and the overlay's start filed in the prompt (a spot start would move the
  twelve month-ends and the figure to $160 million).
- Keeping the wall's extension share near four-fifths with a finer bin: the every-balloon guess band still held
  three-quarters, and the later balloons needed to separate the two bands raised the contractual loss and the
  note-rate DSCR rival past R2c's 1.2x margin.
- A $5 million bin: every construction would have to agree within $1.25 million, which no cover mix of the wall held
  against the bands and the debt yield since 2023.
- More seven-year 2021 loans to widen the gap between the two constant-share bands: the note-rate DSCR fitted on 2023
  onward moved into the bin (145 to 148) and R2c past 1.2x.
- Repaying the already-extended loans at their extended date with the practice stated only in the write-up, at stage 4
  round 2: the cover model run on their current maturities gave 156.1 on that pack, so the reading was an open fork;
  the bank's one extension is now filed in the extract notes with its terms, and the second extension (152.7 on this
  book) is asserted as the alternative.
- An extension on the note's rate and payment with nothing paid down (round 1's terms), at stage 4 round 2: no bank
  extends a five-year balloon three years on unchanged terms; the filed terms are a tenth paid down, the posted
  five-year rate on the maturity date and 25-year amortization, and on this book the old terms would file 159.9 (SF21).
- A break at a cover of 1.05: the 1.00 rule came within $7 million of the golden in half the lab draws and the
  bootstrap sigma ran 1.4 to 1.9 in the median draw; at 1.12 the 1.25 convention came within $7 million in most draws;
  the break was set at 1.08.
- A softer extension response (a logistic scale of 0.03 in cover, for a more gradual book): the 1.25 convention moved
  to within $5 million of the golden and, with the break at 1.10, the sigma rose to 1.4; kept at 0.025.
- Interest-only on a third of the push: the bootstrap sigma rose to 1.8 in the median lab draw, the family's plus or
  minus one sigma out of the middle half; interest only for the first 24 months and amortizing after left in-place
  cover too close to refinance cover; half the push interest only for its whole term puts the in-place and watch-list
  routes 72 to 117 below the golden.
- A larger later fixed-rate book (1.5 then 1.0 loans a month after 2022, or a quarter to a third of it on seven- and
  ten-year terms): the balloons-repaid loss rose to $42 to $44 million and the sigma to 1.5 to 1.9 in the median draw,
  the later balloons' extension adding model spread outside the wall; the later book was cut to a handful of five-year
  loans a year, new lending moved to floating rate.
- Total assets held at $31.15 billion: the 2027 wall would be 10.3 per cent of the balance sheet falling due in one
  year; raised to $38.06 billion (8.4 per cent), C&I taking up the rest, the EVE figures unchanged.
- Convenience extensions at high cover (about 1 per cent at any cover, the round 3 recheck's suggestion), at stage 4
  round 4: a logistic has no floor, so a few extensions at covers of 1.5 to 2.5 flattened the fitted scale from 0.023
  to 0.09 and split the family by 15 to 34 million in the lab; dropped, the response has none above a cover of 1.25.
- Softening the shoulder instead (3 per cent of maturities at covers of 1.10 to 1.35 taking the extension): the family
  held in the lab, but in the file-built golden the near-best hard cut at 1.12 left the middle half with one sigma
  (152.0 plus 0.6); dropped.
- Trailing twelve-month statements for the hotels and retail centres maturing in 2020 and 2021, so their decisions read
  the pandemic: a solver who reads only the fiscal-year statements sees those loans extend at covers of 1.5 to 2.3 and
  files 141.1 in the lab; dropped. The pandemic reaches the record through the 2020 statements, so its extensions run
  from 2021, and the 2020 maturities read 2019 statements (52 of 54 repaid).
- Sale extensions whatever the cover (round 2's 1.2 per cent): on the keyed world a sale-pending six months at a cover
  of 0.81 put a non-extension in the wall's densest band and moved the band constructions by 2.5 to 3.1; a sale repays
  the loan only from a property with equity, so a sale extension now needs a cover of 1.0 or more.
- Statements reviewed after a loan's payoff left in the operating statement file: the fiscal-year reading then picked up
  a hotel's collapsed 2020 statement for a loan paid in February 2021 and moved 4.6; the file now closes with the loan's
  credit file at its payoff.
- Keeping the round 2 realization: with one stream through the book, adding hotels or the ramp moved every later loan's
  draws. Each loan now draws from streams keyed by its origination month and place; on that world the round 2
  settings alone fail the middle half (lab spread plus sigma 5.7), and the ramp, the equity rule and the break at 1.10
  together hold it (2.2).
- The break kept at a cover of 1.08 on the keyed world: the 1.00 rule landed (inside the bin by 0.1); moved to 1.10.
- Loans below a cover of 1.0 sent to special assets at their original maturity (the recheck's coherence exceptions): the
  plateau the wall sits on would fall by about 0.07 and the figure by about $5 million, with a fork on how a transfer
  is read; dropped, and the support agreement and interest reserve that make the plateau real are filed instead.
- A deeper push (pro forma rents 19 to 21 per cent over actual) for a tighter family: the spread fell (lab 2.0) but the
  1.00 rule and every 2027 balloon extended landed; kept at 15 per cent.
- More lending after the push (14 to 18 loans a month from May 2022) to lift every 2027 balloon extended further above
  the bin: the near-best cut at 1.12 left the middle half (lab 2.8 to 3.0); kept at 10.
- The support agreement filed with an income condition ("Where the property's net operating income falls short of the
  extension's payments, the extension is granted on the guarantor's support agreement..."), at stage 4 round 4: the
  reader read it as a mild-to-moderate hint and the recheck as the first filed sentence setting income against forward
  debt service, one step from the cover metric; reworded as a blanket practice on every extension, the pin that the
  payments are made as scheduled kept, no figure moved.
- Portal round 1 (2026-10-25): both responses landed the call, Fixed-rate commercial real estate at $150 million, so conditioning each balloon's extension on refinance cover at the planning rate is a reflex for the portal's models, not a decisive step; the stump sentence's step is spent and the build returns to stage 2.
- Architecture 1 re-rooted at the draw of 2026-10-25, its card's identity moved to the v2 card's lineage: the portal's
  models executed every correction the ladder held (the servicing stitch, an incentive curve on the mortgages' own rates,
  the cover-conditioned extension chosen on held-out maturities), so a redesign inside the overlay world would only add a
  rung above a spent one; the new draw makes the own-rate prepayment curve, the reflex both responses showed, the wrong
  route.
- A plain 2027 run-off figure for the plan (the home equity production that would hold the book flat) as architecture 2's
  call, at the draw: `quantity_figure` with gap population and pattern E repeats task170 v5's structural signature inside
  the batch (`guard.py` test.same_puzzle), and the payoff forecast's own decision is where the retention pilot opens, so
  the call is the pilot's region with its payoff figure.
- The first mortgage's own refinancing incentive (the lock-in) as the decisive step, the draw's first design, at stage 2
  before any data was cut: the lock-in is the most discussed housing story of 2023 to 2026, a 2026 model that sees a
  first-mortgage tradeline takes it by reflex, and the prototype found one cheap route to its answer (the book behind
  first mortgages above the 2027 rate, one group-by, 1.95 over the next region). Kept as rung 2, where it names the
  Lakeshore; the decisive step became the whole stack's blended rate at the two balances, which names Muskegon and the
  North and which no column or one-group-by reaches.
- A semiannual bureau refresh as the forcing file (the draw's plan): it would carry every member's tradelines twice a
  year for eight years, a file several times the size of the cores, to give what the lending system already holds from
  the application's credit report; the senior lien as the underwriter took it is the forcing file, and the first's balance
  path follows from the amortization identity.
- Purchase seconds' first mortgages from a credit report, at the first build: a first opened in the month the second was
  funded is not yet on the report, so its balance reads the original amount and no rate solves; the lending file takes a
  simultaneous second's first-mortgage terms, its rate included, from the purchase file, as an underwriter does.
- Muskegon and the North's seasoned stacks above a blend of 7 per cent (the prototype's first world): they refinanced in
  the record's 2025 and 2026 dips, so the trailing payoffs and a boosted tree on the home equity loans' own fields named the
  golden; the stacks were sized to blend near 6.5 per cent, quiet while the posted 30-year rate held at 6.6 to 7.3 per cent,
  and the record's 2024 to 2026 rates were set so no month reaches them.
- A small 2019 to 2022 book in Muskegon and the North, made of old seasoned stacks: trees on the home equity loans' own
  fields with a region marker carried its 2022 payoff rate (0.16 a year at mid rates, against 0.07 elsewhere) onto 2027 and
  named the golden at implausible levels (41 to 87); the region's history was given the same mix of purchase seconds and
  taps as the others, and the trees now name Grand Rapids in four of four runs.
- A $5 million bin on the pick's figure: region effects in the blended model, significant at 2 per cent on the record
  (deviance 10 on 3 degrees of freedom), move Muskegon and the North by 1.5 to 2.0 and the two-month lag by 2.7, so the
  standing family spans two $5 million bins; at the nearest $10 million it spans one, [35, 45), with the golden at 39.19.
- Grading every center's 2027 figure: at the nearest $10 million the first-alone route matches three of the four (Grand
  Rapids 20, the Lakeshore 20, Kalamazoo and Battle Creek 10) and the own-rate route matches the golden's Muskegon and the
  North figure (43.9, 40); only the pick's figure and the second center are graded.
- Each lien against its own posted rate, weighted by balance (a stack-aware rival): it names the Lakeshore at 22.9 against
  Muskegon and the North 22.0 and the record rejects it (deviance 49,297 against 48,893); left as an enumerated rival, its
  figure outside the bin either way.

- Every first-mortgage statement in the log quoting both liens (primary 1's first cut, at stage 3): every MTG row sat on
  a stacked mortgage, so noticing the MTG rows was the remedy (count each one at a booked loan's address, 32 of 32 with
  the outage workbook), a device whose discovery and remedy were one act; the credit union's other first mortgages,
  members' quotes on the first alone and closings whose first request named the first mortgage before the title search
  found the second lien now share the log, and only the amount tells which statements paid the second loan too (counting
  every MTG statement unreconciled keeps 9 of 32).
- The ALM report's clause on why the home equity book grew ("as members borrowed against their equity rather than
  refinance their first mortgages"), at stage 3: a narrative of the lock-in in the context artifact, pointing a reader at
  rung 2, and a claim about the record no check reproduced; cut to the book's size, count and rate.
- Creditor and title agency names near real firms (H21), at stage 3: Arcadia Home Loans (a mortgage lender once licensed
  from Grandville, Michigan), Cross River, Horizon First (First Horizon reversed), Meridian Trust (a federal credit union),
  Pinehurst Mortgage, Trillium Mortgage, Summit, Meridian National (a trade name of Meridian Title, which has offices in
  Indiana and Michigan) and Tallgrass Title (a Kansas agency); renamed Marlstone, Fernwick, Dunmere, Corraven, Vellacott,
  Eldermoor, Tollmere, Ashgrove National and Larchwick, each searched without a hit; no figure moved.
- A statement on a loan funded earlier in its month, at stage 3: the generator quoted the loan's exit balance, a balance it
  did not yet have, and one first-mortgage statement failed to tie; the desk now quotes the amount funded for a loan
  funded in the statement's month, and no statement predates its loan's funding.
- Portal round 1 on architecture 2 (2026-10-26): both responses landed the call, Muskegon and the North at about $40 million with the Lakeshore second, the golden; reading each stack's payoff off its blended first-plus-home-equity rate, chosen over the own-rate and first-only curves on fit and back-test, is a reflex for the portal's models, as stage 4's Opus reader showed, so architecture 2 is spent and the build re-roots off the enumerate-and-back-test chain.
- Architecture 3 candidate 1, a homeowners late-reported claim count by territory completed by occupancy (seasonal
  homes found at the next visit, a seasonal book grown since July 2025), probed 2026-10-26 (p166b): the Opus call-only
  probe found the seasonal-residence endorsement at once, built lag curves by that flag and the loss season on the
  developed 2021 to 2023 losses, used Bornhuetter-Ferguson for the young seasonal book and landed the territory and
  the runner-up (Lakes about 80, Ridge second); an occupancy lag read off an endorsement column is a move visible in
  the schema. Its pack also read as built (no policies written 2021 to 2024, every 2025-26 policy a seasonal home, no
  cancellations, one form).
- Architecture 3 candidate 2, the same count with the lag driver rebuilt from a record kept for billing (homes standing
  empty at the loss date: seasonal cottages, and primary homes whose owners winter away, seen only as winter mailing
  addresses; a June to November 2026 book transfer into Ridge with no winter on the books), probed 2026-10-26 (p166d):
  the Opus call-only probe matched every claim to the term, the endorsement and the mailing address in force at the
  loss date, built four occupancy states, ran Bornhuetter-Ferguson on policy-days by territory, state and month and
  landed Ridge at about 70 with Lakes second; an attribute of the frame's own units, however it is recorded, is joined
  at the event date and modelled. The pack also carried rows dated after the pull and transfer policies whose original
  inception equalled the transfer date.
- Architecture 3 candidate 3, homeowners claims first reported in 2027 by territory with an exiting carrier's book
  rolling into Ridge at its renewal dates through May 2027, listed in the transfer desk's roster, probed 2026-10-26
  (p166f): the Opus call-only probe counted every policy in force in 2027, carried the roster's offered and
  not-yet-mailed rows at the decided acceptance, modelled them on the 2022 transfer block's first-months curve and
  landed Ridge first and Metro second at about 2,350; a roster listing the incoming units is read as future book
  growth. It also noticed every term ran exactly 365 days.
- Architecture 3 candidate 4, the same 2027 count with no roster, the transfer's continuation left to the record's own
  arrival flow (1,600 a month into Ridge from September 2026) and the 2022 block's twelve-month cycle, probed
  2026-10-26 (p166g): the Opus call-only probe fitted claims by territory, month and months since transfer on the
  2022 block, inferred one renewal cycle from the source's definition and the analogue, projected 1,595 a month to
  August and landed Ridge at about 2,550 with Metro second; an arrival flow that jumps a territory's book by 8 per cent
  a month, with an analogue block beside it, is salient however unlisted. Pack tells: dates on days 1 to 28 only, a
  pile of 1979 inceptions.
- Architecture 3 candidate 5, a self-insured manufacturer's 2027 workers' compensation claims by the claimant's last
  plant, a laid-off forge cohort turning 62 and filing hearing-loss claims from the HR master's separated rows,
  probed 2026-10-26 (p166i): the Opus call-only probe sliced the hearing-loss claimants by status (613 of 730 former),
  fitted a hazard by age, department and length of service on former workers, found the 2014 forge layoff and its
  1965 births and landed Kessler at about 340 with Harlow second; a separated population in the frame's own file is
  read once the claimants are sliced by status. It ignored the noise survey, taking department and tenure as the
  exposure, and flagged the single-date layoff and the birth bunching.
- Architecture 3 candidate 6, first form (measured 2026-10-26, never probed): the 1988-90 forge cohort crossing 62
  with a realistic birth spread, the golden on cumulative dose from the noise survey. With births spread over 1962
  to 1972 the cohort's first crossers fall in 2023-26, so the back-test p166j ran (fit 2016-22, test 2023-26) showed
  the department-and-tenure hazard over-predicting Kessler's hearing-loss filings by 40 to 70 per cent, and a
  per-plant recalibration of that hazard lands the golden; the cohort's separation moved to a November 2026 forge
  closure and the filing hazard onto years since leaving.
- Architecture 3 candidate 6, a November 2026 forge closure whose 1988-90 hires worked almost entirely under the
  1991 enclosure, the filing hazard by years since leaving and dB-years from the noise survey, probed 2026-10-26
  (p166k): the Opus call-only probe split acute injury from hearing loss, put acute claims on the 30 November roster
  by plant and department (the forge empty, Ellery's 1,625 hires counted), fitted the closure group's propensity by
  plant, department and hire era, measured the cohort's own low claim rate beside the noise drop, rejected the flat
  layoff precedent and landed Ellery at about 260 with Harlow second; a cohort the action concentrates on is dug
  into through every related file, the noise survey included.
- Architecture 3 candidate 7, a self-insured manufacturer's 2027 carpal tunnel claims by plant, a mid-2026 line
  speed-up at Ellery hidden by the disorder's onset lag, the ergonomics file carrying each job's Strain Index inputs,
  probed 2026-10-26 (p166m, p166n): both Opus call-only probes scored the Strain Index from the assessment rows,
  fitted log rate = -6.76 + 1.54 ln(SI) across the 56 job areas, confirmed it on the one area already changed, applied
  the speed-up's doubling with an onset ramp and landed Ellery at about 290 to 300 with Harlow second; an exposure
  field the solver recognises is scored and calibrated across the units.
- Architecture 3 candidate 8, a new acute hospital's first-year critical care admissions under a practice-allocation
  model, two independent-sector hospitals beside the new site sending their deteriorating patients to the nearest NHS
  unit (Ravensholt General today) whatever the patient's practice, probed 2026-10-26 (p166o): the Opus call-only probe
  ran the practice model (543, back-tested at 505 against 511), tabulated transferring sites in the admissions file,
  found the two Hindmarsh sites' transfers taken at Ravensholt whatever the practice, reassigned them by site (55 in
  2025-26, trended to 52.5) and landed 600 (595.4), rejecting the literal model as missing the flow; an outside body
  carried in the model's own records is tabulated, however small its share.
- Architecture 3 candidate 9, a new secondary academy's first Year 7 intake under the council's place-planning
  model (its area's demand less the existing schools' admission numbers, 130), a neighbouring area's oversubscribed
  schools turning away about 55 applicants a year whom the coordinated scheme's clause 8.1 offers the nearest school
  with a place (until 2027 one in another authority, from 2027 the new academy, filling it to its 180), built
  2026-10-26 as probe9 and never probed: it has the anatomy of task137 v3's stage-4 SEND_BACK, a filed clause that
  decides membership and a cap that makes the body's size immaterial (every golden reading exactly 180), so the
  decisive step reads as data semantics and rule application to the judge and to any reader of the scheme.
- The outside-population family as a whole (candidates 5 to 9 here, task137 v3): the decisive step cannot satisfy
  the three rules. Filed for determinacy, the institutional fact makes the step a presence flip read off a document
  (Gate H data semantics, task137 stage 4); withheld, the golden rests on a hidden rule; left measurable in the data,
  the body is tabulated or calibrated and landed (candidates 5 to 8); and a body large enough to move the bin
  robustly makes its own size immaterial, while a small one leaves the call on the rounding edge.
- Candidate 10 as first specified (regression to the mean in a pick: each unit's own frequency, raw or through a
  Poisson GLM with unit and year effects, against Buhlmann-Straub or empirical Bayes toward the fleet average),
  measured on the clean world 2026-10-26 (12 of 299 seeds) and set aside before a pack: guard.py blocks it on
  driver.text at 0.32 against task479 v6 (small-group experience weighed by credibility against the trust, shipped
  10-21), the same insight, and on the spent gap, pattern and decision signature; and with credibility toward the
  pool at the top of the ladder it is the opponent's first move (stumping 1.1b). Carried forward as candidate 10 P1,
  where credibility toward the pool is rung 1 and lands wrong.
- Explorer B probeB1 (Thornmere Water, 2027-28 pressure management programme, mains repairs avoided on N3 fitted
  across DMAs from one 14-day AZP reading each; the golden corrects the regression dilution with a check logger in
  three DMAs in ten), probed 2026-10-26: both Opus probes (p166qa 600.64, p166qb 593.3) sized the logger noise from
  the AZP and check pairs and landed 600. Regression dilution with replicate readings is the probe's reflex.
- Explorer C probeC1 (Arvenland Passport Office, 2027-28 applications, renewals pulled forward ahead of the 1 April
  2027 fee rise), probed 2026-10-26: Opus probe p166sb stitched the two case systems, read the 2023 fee rise as the
  precedent and landed 730,000 (731,094); the second probe was stopped. Anticipation before a price rise with a
  precedent in the history is calibrated, not missed.
- Explorer B probeB2 (probeB1's world with the check round six months after the AZP, so each pair's difference
  carries the night pressure season twice and the noise correction over-corrects to 700), probed 2026-10-26: Opus
  probe p166ta took the season out of both readings with a DMA fixed-effects sine and cosine model and landed 600
  (593.3, N3 2.16); p166tb fell into the 700 rung (694.5, N3 2.81). Dead on the probe gate: a seasonal swing large
  enough to move the bin is large enough for a strong probe's routine seasonality check, and taking a season out
  is a cleaning step a judge could class as Layer 1.
- Explorer C probeC2 (North Marches Ambulance Service, C3 to C5 calls answered in 2027-28 after the neighbouring
  NHS 111 service failed on 1 October 2024: public 999 calls carry about 82,000 a year of overflow from callers who
  gave up on 111, which goes when 111 recovers, against the plan's named channel of 111 referrals coming back),
  probed 2026-10-26: Opus probe p166ub read the October 2024 step in public calls against the flat C1, C2,
  healthcare professional and other-service lines, called it callers who could not get through to 111 ringing 999,
  switched the step off for the recovered year and landed 540,000 (540,100); the second probe was stopped. A step
  in the main series at a filed event is explained by the probe, and the overflow channel is common knowledge.
- Candidate 10 P1 (credibility weighted against each unit's class-rated expectation, 22 LTL service centers,
  probe10): Opus call-only probe p166rb landed Lexington at 12.5 on 2026-10-26. It cleared every Layer 1 item, built
  each center's expected claims from company-wide job-group rates times its own mix, and weighted each center's
  actual-to-expected ratio by Buhlmann-Straub (Z 0.80 at Lexington, about 0.4 at Clarksville), rejecting the raw
  record and credibility without the mix by name. Credibility on a class-rated complement is the reflex too: the
  field's method done right is the opponent's first move whatever its complement, so the regression-to-the-mean
  family is closed for this build.
- Explorer B probeB3 (Thornmere Water again: N3 differs by main material, cast iron 3.1 against plastics about 0.6,
  and the 260 single-inlet scheme DMAs are mostly plastic estates, so the network-wide exponent prices them at cast
  iron's 2.4 and files 450 against a golden of 300), probed 2026-10-26: both Opus probes (p166va 292.9, p166vb
  292.85) fitted a Poisson model with a slope per material and the material's length as exposure, corrected each for
  logger noise and landed 300. Heterogeneity across a recorded attribute that is also the natural
  exposure unit is modelled, not missed; the probe also flagged the exponents as the reverse of industry experience.
- Explorer C probeC3 (Larkspur Mobile, first-payment defaults on 2027-28 handset connections: fraud rings follow the
  operator's own zero-upfront campaigns three to six months later, so the careful channel rates file 10,000 against
  a golden of 13,000), probed 2026-10-26: both Opus probes scanned campaign days at lags against the daily fraud rate,
  found the 70 to 190 day window, fitted connections times base rate plus lift and filed 14,000 (14,210.6 and
  14,089.2), one bin above the golden because each filled the unplanned October 2026 to March 2027 campaigns from
  history and kept a lagged lift on credit defaults. Dead twice over: a lagged response to a filed calendar is found
  by a lag scan, and a forecast that leans on campaign exposure outside the plan's window has no unique execution.
- Explorer B probeB4 (Tamberley Bank's 2027 personal-loan charge-offs on the 30 September 2026 book, its own loans
  and the Northway loans bought current at the cut-off: loans cured in the last 12 months miss again at six to seven
  times the never-delinquent rate and roll on at about 90 per cent, and the bought book carries three times the
  recent cures, so the pooled roll-rate chain files 750 against a golden of 900), probed 2026-10-26: Opus probe
  p166xb fitted the miss rate on a recent-cure flag with the re-default rolls and filed 869.7, five below the 875
  edge, with its own variants at 869 to 882; p166xa conditioned the miss rate only, calibrated Northway on the
  survivor tape and filed 650 (660.9). Dead: the step is found by a strong probe, and the golden's margins of 4
  and 13 inside its bin leave the call on the rounding edge.
- Explorer C probeC4 (Dunmere Energy, write-offs on arrears cases opened in 2027: the collections team calls the weekly
  queue in case-reference order as capacity allows, so the record's write-off rates were earned at 84 in 100 cases
  called, and the flat 2027 agent plan against an 80 per cent case surge calls 49 in 100; the careful segment rates file
  13,000 against a golden of 15,000), probed 2026-10-26: Opus probe p166za rebuilt which cases were attempted from the
  weekly attempt counts and the queue order, measured unattempted cases writing off 1.45 times as often in every
  segment, applied the 2027 attempt share and landed 15,000 (15,066.1); the second probe was stopped. A
  capacity-rationed treatment whose footprint sits in a filed weekly pack is reconstructed, not missed.
- Architecture 2 re-rooted at the draw of 2026-10-26, its card's identity moved to the v3 card's lineage: the portal's models
  executed the whole-stack refinance incentive on fit and back-test, so a redesign inside the credit union's world would add a
  rung above a spent one; the new draw (candidate 11) makes the field's own back-tested count model the wrong route.
- Explorer B probeB5 (Calderton City Council, new housing register applications in 2027-28: tenants' adult children
  register in their own right, mostly in the year they turn 18, and the 1,098 tenancies let in 2009-10 put a cohort of
  1,269 children aged 16 at the 2026 audit, so the careful frame methods file 1,400 against a golden of 1,600), probed
  2026-10-26: Opus probe p166bb linked applicants to the 1 April tenancy audits by name and date of birth, found 150 to
  175 new applications a year from tenants' children, projected the 2009-10 cohort through age-specific rates and
  landed 1,600 (1,587.3); the second probe was stopped. A cohort spike sitting in the largest file is tabulated, and
  concealed households are standard housing need practice.
- The 90-day users ask (probe11's ordinary job for the directory: the median users on a 2025 new customer's workspace 90
  days after its first paid invoice), dropped at stage 2: it prints 8 under every reading and every handling (end or
  start of the day, regional clocks, cancelled customers in or out, by starting plan), so no device can sit on it and
  the cracker keeps it; sums of users fork on the day-90 boundary (about 120 creations and deactivations fall on it).
  The directory's ordinary job is now the planning basis's Seats and Hosting lines and rung 2's installed base.
- The ask devices as first cut (group bookings labelled "(group)" and "(drop-in)", the register's current terms against
  the case's terms at handoff): the label hands over the grain and the case is the at-start record a careful reader
  finds, so the cracker would keep 48 of 48; replaced by unlabelled group bookings, partner bookings, synced cases and
  same-day corrections.
- The prompt and deliverable shell of task175 and task179 (a question, a workbook named with its columns, a labelled
  chart, a rounding sentence; task179 came back a Duplicate of task175 over that shell): not used here; the prompt
  opens with the decision, asks for a short decision memo and a staffing workbook, and asks for no chart, and the
  memo's one chart labels only the recommended region.
- The deliverables as first named (pod_placement_2027.docx asked for as a one-page memo, pod_staffing_2025.xlsx): the
  surface screen put the shell beside task139's placement note and workbook (surface 0.103, corpus top 1 per cent);
  renamed onboarding_pod_2027.docx, asked for as a short memo, with the staffing figures in onboarding_staffing_2025.xlsx.
- The asks as cut for stage 4 round 1 (each region's specialist hours with its customers by the onboarding case, and the
  2025 cohort's plan and total contract value rolled back through the amendments, plan names on the register): reader
  B kept all 48 figures and reader A 24; a case's customer and an amendment's effective date are what a careful reader
  checks, so a device a cross-check repairs is no device. Replaced by stale mappings that only a second source exposes
  (the task137 pattern): the roster's pod today against the pod each specialist's sessions served that month, and the
  July 2026 catalog's SKU numbers against each subscription's own price and seats.
- The figure to the nearest 100, at stage 4 round 1: the judge's constructions ran 519 to 581 against 608.9, across
  the 550 edge; the honest family on the repaired pack spans 541.0 to 612.1 (509.2 with name matches anywhere added),
  so the prompt rounds to the nearest 200, [500, 700), with the golden 92.4 inside.
- A mobile missing on about one directory user in eight with a name fallback (round 1's link rule): the judge's
  mobile-only and mobile-then-name links gave different founder counts (2,228 and 2,637 since 2023), an open fork on
  the link rule. The field app signs every user in by mobile, so every directory row now carries one and the link has
  one key; a name match beside a different mobile is another person (the judge measured a median lag of 13 months on
  those against 11, and no peak).
- A founder's company spread over the regions on the same-region share (round 1's golden), read by the judge as the
  region its founder left: the memo counts each new customer at its own parent company's billing state, so the memo's
  sentence now says "its own parent company's" and the golden counts each founder where the new company bills (close
  to nine in ten in the region they left; the region left gives 641.6).
- The usual intake fitted from 2019 with founders removed only from 2023, where the judge sought links: a step down in
  2023 that a region trend reads as decline, 149.1 to 168.5 against 187.4 to 203.8 when the founders come out of the
  whole fitted record or the fit starts in 2023; that inconsistent split drove the judge's 138 to 225, and the call
  under it stays 541.0 or more.
- Pro and Enterprise list prices of 899 and 2,400 dollars a month (49 and 45 a seat), at stage 3 of the repair: with
  the contract value asked by region and plan, the Southeast's Pro cell sat 2.40 dollars from a rounding edge; the
  price list moved to 889 and 2,390 (48 and 44 a seat), no count or session moved, the nearest cell 9.40 from an edge.
- The webinar and office-hour rota without a free check, at stage 3 of the repair: seven field app trainings overlapped
  a session the same specialist covered for another pod; the rota now passes a slot to the next free senior, and the
  office-hour rota's start moved to turn 2 (turns 0 and 5 let one customer-pod cell land through a symmetric cover).
- Each company's plan and seats drawn apart from the team it signed up with (round 1's records, measured on zip
  d2bf801d): a 2025 new customer's workspace held a median of 8 users 90 days after its first paid invoice on Core, Pro
  and Enterprise alike, and 263 of 855 Core orders carried fewer seats than the users then on the workspace; the plan
  now follows the team a company signs up with and the order's seats cover it (Q9: Core 6, Pro 9, Enterprise 13; 4 of
  691 Core orders short), and the Core extra seat moved from 39 to 38 dollars a month, which put the nearest
  contract-value cell 6.40 dollars from an edge (2.20 at 39); the call and the 24 hours did not move, and ask B's 36
  figures were recomputed.
- The register's amendments typed Upgrade and Downgrade (measured on this pass's records before the relabel): read with
  the July 2026 catalog's numbers, 1,970 of 4,336 plan changes ran the wrong way (an Upgrade from PLW-300 to PLW-100
  reads Enterprise to Core), a contradiction in the very sheet every rollback reads; the billing platform types a change
  of rate plan as Plan change whichever way it goes, and the starting plan is still read off each subscription's own
  price and seats (SF23).
- The critical components as points (a median lag of 11 months, a usual intake of about 200), at stage 4 round 1: the
  judge read 10 to 10.5 months and a usual intake of 138 to 225; the write-up states the lag as 10 to 11 months (11
  calendar months, 333 days, 10 whole months elapsed) and the usual intake as about 150 to 200, the range over the golden
  family and the judge's choices on the mobile (149.1 to 203.8, F8), with the founder-led part 400 to the nearest 100 in
  every one of them.
- The stale mappings as the asks' primaries (the roster's one pod per specialist today, the July 2026 catalog's SKU
  numbers), at stage 4 round 2 on zip 39daad7a: reader B (Opus) took each starting plan from its own price and seats,
  which fit exactly one plan, and kept all 36 plan figures, so noticing the renumbering was its remedy; the judge read
  the roster's pods today and the undefined group session as two open forks on the hours (West one-to-one Q3 358.25,
  and West Q1 332.00 and 38.00 or 118.25 and 251.75, against 459.50, 323.00 and 47.00). The forks are closed in the
  dictionary and the roster (SF15, SF16), which spends the stale roster; the asks' primaries are re-sited as
  reconstructions on reader B's own route, a specialist listed on a booking a colleague took over (A7) and a day's
  amendments referenced in the order they were keyed (A8), and the renumbering stays as a hazard (B2).
- A leaving deactivation with no reason (about one in eight on round 2's records), at stage 4 round 2: the judge
  counted removals by their leaving reasons and read 5,715 Southwest removals from April to September 2026 against the
  Seats line's 6,487, and about 4,000 founders against 4,451, so its Southwest came out near 363 founded by leavers
  and 575 to 585 in all. Every leaving deactivation now carries its reason (R4: 6,483 by the Seats line, 6,486 by the
  reasons), and the judge's own route rebuilt from the repaired pack's files gives 6,486 removals and 4,451 founders.
- The step-by-step's unrounded parts of the 2027 figure (the Southwest's 403.7 founded by leavers, 203.8 usual intake
  and 607.5 in all, Texas & Gulf 484.3), at stage 4 round 2: a judge's own construction reproduces the bins, not the
  digits; block 3 states them as the components and the memo do (about 400, about 200 and about 600, Texas & Gulf
  second), and the 2027 figure is graded to the nearest 200.
- The keying-order device and the renumbering as ask B's devices, at stage 4 round 3 on zip 45fa2e01: reader B (Opus)
  undid each day's amendments by chaining one line's after terms to the next line's before terms ("every chain
  resolved") and fitted each plan from price and seats, keeping all 36 plan figures; noticing either was its remedy,
  because the chains resolve uniquely and the price fits one plan exactly. Both stay as hazards (B2, B4); the primary
  moves onto that route, a first-year offer priced at Core's list on Pro's own SKU, where the price fit itself lands
  on the wrong plan (A9).
- The listed-not-hosting clashes as partial overlaps (a colleague's booking overlapping the specialist's own session
  by 30 or 45 minutes), at stage 4 round 3: the judge read counting only the minutes outside the specialist's own
  session as a third defensible reading (30.25 hours removed against the golden's 60.5) and the file order and case
  ownership as settling nothing. Every listed booking now lies wholly inside the listed specialist's own session,
  which no one else hosts, so the minutes reading is the golden (A1, A7); the office hours moved onto the pod
  partner's webinar days, half an hour into the webinar, so the group cells can carry such a booking.
- Portal on architecture 3 (shipped 2026-10-27; the author's Batch 5 sheet of 2026-10-31 records the call as landed): the
  Southwest at about 600 new paying customers, the golden. Linking each new workspace's founder to the users who left
  paying customers, through the one mobile number the stage 4 determinism repair put on every directory row, and the
  Southwest's April to September 2026 removals (about four times their usual number, the pack's loudest movement) were
  read by reflex; architecture 3 is spent and, one architecture per world, the slot re-roots into another world, dataset
  and shell. Lessons kept: a determinism repair that gives the decisive link a key on every row hands the link over, and a
  forward driver that is the pack's largest movement is found.
- Architecture 4 candidates set aside at the draw of 2026-11-01, on paper, before any data was cut:
  an oncology trial's event-driven final analysis date (biomedical survival analysis): every oncology-native violation of
  the blinded event prediction (progression state, crossover, delayed death ascertainment, a cure fraction) is a named
  biostatistics correction or a reporting delay of task181's family, and no deciding relation without a column was found;
  an avocado or pistachio cooperative's 2027 intake under alternate bearing: the on-off cycle is the crop's best-known fact
  and the industry forecast's own first term, so the golden would be the field's method, and a synchronising frost or
  planting wave would be the pack's loudest movement;
  a condominium unit-owner book's water claims with leaks cascading down a stack: the expected count is additive over
  policies whatever the dependence, so the cascade moves the variance and not the mean, and the net-of-subrogation variant
  (no recovery when both units are insured by the same carrier) decides on the anti-subrogation rule, a rule application;
  a multicentre trial's recruitment with new sites sharing a referral pool: the cannibalisation reads the same for shops in
  one catchment (the swap test fails);
  warehouse picker congestion under a peak staffing plan: generic queueing (the swap test) and a congestion function whose
  form is a free method choice;
  a utility's 2027 retirements at first unreduced pension eligibility: age-and-service retirement tables are the pension
  actuary's own method, so the golden would be the field's method, and service transferred in from another scheme is a
  field reading;
  a school district's kindergarten intake fed by younger siblings of current pupils: the same abstraction as architecture
  3, next period's arrivals generated by a linked population's earlier events.
- 2026-11-01, v4 world s54 (the first world drawn for this architecture): the development without the step back-tested
  11 and 10 per cent short at the 2024 and 2025 year ends, because its autumn lists carried quick paperbacks into the
  back-test windows, so the Back-test line was false; set aside for s110 (-3.4 and -1.2 per cent), chosen from a sweep of
  70 worlds on the back-test, the bin placement and the separation.
- 2026-11-01, v4 ask device, second bookings under their own number range (D99...) and only beside genuine parcel
  splits: the number range marked them, and dropping every repeated line kept 18 of 24 cells; replaced by second bookings
  numbered in the day's sequence, carton-by-carton hub booking as the genuine repeats, and copies sent beyond an
  authorisation as the second primary.
- 2026-11-01, v4 retitling more paperbacks in the world's edition draw: it moved the price stream and put the hardback part
  on its bin's edge (1,126,294 against 1,125,000); the extra retitling moved to the title master's own stream instead.
