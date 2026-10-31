# task306 design note

## Draw

1. Card: `.claude/skills/fingerprint/cards/task306.json`, architecture 3, registered 2026-10-31; its text was brought to the second-event design at stage 3, the axes unchanged.
2. Pairing: Actuarial Science & Insurance, task type reinsurance-capital, objective Opportunity Sizing & Decision Support, shape other (a buy-or-not call sized by the capital the cover releases and its worth a year, the year's loss occurrences by line of business, the farm book by county and section).
3. World: Hartcombe Mutual Insurance Society Limited, a county farm-and-home mutual writing in Cornwall, Devon, Somerset and Dorset; its catastrophe model vendor Seaborne Risk (Seaborne UK Windstorm Model 8.2), broker Penwarden Reinsurance Brokers, loss adjusters Penhallow, co-insurers on large farms. People from `guard.py names`: Elizabeth Farmer (chief executive, who sends the request), Mandy George (head of reinsurance), Arthur Begum (chief actuary).
4. Quantity: the 1-in-200 windstorm capital the second-event cover releases under the capital policy, and its worth a year at the cost of capital less its margin; the call is whether the Board adds it to the 2027 programme.
5. Default path: one incurred-over-hindcast ratio for every storm of record, the field's model adjustment factor.
6. Data-native sentence: windstorms reach the mutual in trains inside a season, and the record carries each storm's first damage date and the model's hindcast of it, so the extra cost of a storm that strikes while the roofs from the one before are still sheeted is a relation between consecutive rows of the record, which no column holds and a single ratio averages away; the second-event cover pays on exactly the later storms of a train.
7. Against task309 (one cut ratio across storms varying with gust intensity, carried through a vendor event set): here the deciding relation is a storm's gap to the storm before it, read across two files, and the cover is valued by the capital it releases, not by a loss ratio.
8. Furniture: forum board_of_directors, forcing vote_or_meeting (the November Board), org cooperative_or_member_body, role procurement_lead (the head of reinsurance places the programme), question form whether.
9. Prompt shell: a whether question that the gate reads as how-much (its first sentence asks how much capital), the second sentence opening "My", the rounding sentence opening "Capital", deliverables pdf and xlsx.
10. Guard WARN people.first answered: the first name Elizabeth appears in one older build (task128); she is the drawn persona for this seed and no other persona in the pack shares her names.

## Default path

1. Read CP-04: the 1-in-200 is the average of the 50 worst of the 10,000 simulated years, each simulated storm costed at the mutual's incurred over the model's hindcast, a cover valued at 12 per cent of the capital it releases less its margin.
2. Total the incurred in windstorm_experience_2001-2025.xlsx over the loss in seaborne_windstorm_hindcast_2001-2025.csv: 1.06, the model adjustment factor; check it the way the field does, against storm size and over time, and find no trend.
3. Load every storm of seaborne_windstorm_ylt_2027_portfolio.csv at 1.06, net each simulated year of the occurrence cover and then of both covers on the quotation's terms.
4. Read the release, the margin and the worth, and decide.

Ends on: do not add the second-event cover, which releases £5 million of capital and is worth minus £0.3 million a year.

Golden: add the second-event cover, which releases £7 million of capital and is worth £0.1 million a year.

## Stump sentence

A competent analyst costs every storm in the 2027 table at the record's one incurred-over-hindcast ratio of 1.06 and files that the second-event cover releases £5 million and is worth minus £0.3 million a year, so it is not bought; the step that lands it there is reading the record as one population, when the storms that strike within weeks of the storm before cost the mutual 1.62 times the model and every other storm 0.98 times, and those later storms of a train are the ones the cover pays on in the years that set the capital.

## Three rules

Task type: reinsurance-capital in Actuarial Science & Insurance, which serves Opportunity Sizing & Decision Support: the call is a cover sized by the capital it releases and bought on that capital's worth against its cost.

Domain test: the 1-in-200 annual windstorm loss net of reinsurance, the average of the worst simulated years of a vendor's year loss table with each simulated storm adjusted to the company's own claims against the vendor's hindcast of the same storms (the catastrophe model adjustment an actuarial function runs each year), and the release and cost of capital that decide a reinsurance purchase.

Swap: "add the second-event cover because it releases £7 million of 1-in-200 windstorm capital" with a hospital's nouns ("add a second ward because it releases 7 million bed-days of capacity") stops making sense: there is no year loss table, no hindcast to adjust against, no retention, reinstatement or second loss occurrence and no capital read off the worst simulated years.

Layer 1: the hindcast's peaks in UTC on the damage date or the day after (the vendor's timestamps); storm names only from the autumn 2015 season (the naming practice); two claims systems in the experience (the 2014 migration); the web form recording the day it is sent as the loss date, the adjusters' portal spacing the claim number, reopened claims on a suffixed line, the farm book in thousands, holdings renumbered by the Rural Payments Agency and the coinsurance register keyed by the main holding's CPH as it stood at its last renewal (each from the system named, none placed to be caught, none on the main call's rows).

Layer 2: catastrophe model adjustment by storm class, the composition of the record behind a pooled factor: which past storms are like each simulated storm, read from the record's own sequence of storms.

Decisive step: recognising that the storms of record are not one population, since a storm that strikes within weeks of the storm before it costs the mutual far more per pound of the model's loss, so each simulated storm takes the experience of the storms of its own class and the table's later storms of a train carry the cost the second-event cover pays on.

Not semantics: every field, code and term read correctly (incurred, hindcast, dates, the covers' terms, the capital policy's definitions) still leaves the analyst on one ratio, because no column, code or definition marks a storm's class; the class is a relation between consecutive rows of the record.

Not rule application: CP-04 files that each storm is costed at what the claims show for the past storms like it and never says which storms are alike, so executing every filed rule with the record as one class files the default path's answer; the enumerated family (one class, by size, by year type, by rank in year, by rank in season, by season type, autumn against winter and by gap class, each under the ratio of totals, the mean and the median of the storms' ratios, 26 routes) spreads the cover's worth from minus £0.32 million to plus £0.13 million a year and its release from £4.8 million to £6.9 million, while the standing family (the routes the record does not refute: the gap class under the three estimators and every window from 25 to 69 days) gives a release of £7 million, a margin of £0.7 million and a worth of £0.1 million, a spread of 0.002 million in worth; the ruling-out is quiet, the record's later storms on quiet seasons costing what the model says.

Analyst test: a strong analyst who reads CP-04, the quotation and the wording correctly and runs the model adjustment on the record as one population files that the cover releases £5 million and is worth minus £0.3 million a year, and does not buy it.

Estimand: CP-04 sections 2 and 3 in CP-04_capital_policy_windstorm_2026.pdf: the 1-in-200 annual windstorm loss is the average of the 50 worst of the 10,000 simulated years of the 2027 portfolio's table, each year net of the covers in force with reinstatement premiums added back, each storm one loss occurrence costed at incurred over hindcast for the past storms like it; the release is the 1-in-200 without the cover less with it, the occurrence cover in force in both; the worth is 12 per cent of the release less the premium and expected reinstatement premiums plus expected recoveries.

No decoy: nothing planted carries the wrong answer: no copied block, memo, staff draft, broker opinion, validation sheet or stakeholder figure computes or argues the pooled factor or any route, and the request names no answer.

No certified replay: the method is not recovered by reproducing certified figures; the record ships raw (each storm's date, incurred and hindcast) and the golden is computed forward from it.

Lesson: a model learns that an adjustment factor fitted to a whole record of events can hide a structure in the events' sequence that matters most to the cover being valued, and to read the record's rows in order before pooling them; no build on file values a reinsurance cover on what a storm costs by its place in a train.

## Survivor anatomy

Actor: the deciding property, whether a storm struck within weeks of the storm before it, has no column in any file: the experience lists each storm's first damage date, the hindcast each storm's peak and the table each simulated storm's peak, so the class is a relation between consecutive rows.

Link: the record's storms carry no key into the hindcast (the experience's storm references and the vendor's event ids share nothing), and the per-storm cost the class needs is read by date across the two files, the hindcast's UTC peak on the damage date or the day after; no sentence invites a per-storm comparison, since the pooled factor needs no link.

Reflex: the field's method for the deciding quantity, the catastrophe model adjustment factor as total incurred over total hindcast, sits at rung 1 and files the wrong call (a release of £5 million and a worth of minus £0.3 million).

Back-test: the factor validates the way the field validates it: it reproduces the record's total incurred exactly and shows no meaningful trend with storm size (a fitted slope of minus 0.03 a log unit) or over the years, so the actuarial checks pass on the wrong route.

Second use: every file the decisive step reads is in the pack for the default path itself (the year loss table, the hindcast and the experience are what any model adjustment reads), so deleting the decisive step drops no file.

Shock: the storms that follow another read as ordinary scatter on every shipped statistic: they are not the largest, the newest or one season's storms, and sorted by incurred, hindcast, date or claim count they form no interval; their extra cost shows only in a ratio no file holds.

Pins: CP-04 files the WHAT in the mutual's own capital policy (the 1-in-200 as the average of the 50 worst years, each storm one loss occurrence costed at incurred over hindcast for the past storms like it, the release with the occurrence cover in force, the worth at 12 per cent less the margin), and no filed sentence names a storm's gap, a train, a season or a window.

## Readability screen

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| Rung 0, the model's losses as they stand | CP-04 costs storms at the claims | no | no | no | no | no | no | readable |
| Rung 1, one incurred-over-hindcast factor | no | no | the field's model adjustment | no | no | one ratio | no | readable |
| Rung 2, the factor by storm size | no | hindcast column | the field's bias check | no | no | one fit | no | readable |
| Rung 3, later storms of a year or season against the first | no | dates | a clustering habit | no | no | one split | no | readable |
| Rung 4, each storm by its gap to the storm before it (decisive) | no sentence names a gap, train or window | no column holds it | not the field's adjustment | no control scores it | the battery never orders rows into gaps | a link and a class, then the table re-classed | no file exists only for it | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | 1-in-200 | average of the 50 worst of the 10,000 years | the 50th worst year | not the filed figure | CP-04 section 2 files the average |
| SF2 | capital released | net of the occurrence cover less net of both | gross less net of both | not the filed figure | CP-04 section 3, the covers already bought in force in both |
| SF3 | margin | premium and expected reinstatement premiums less expected recoveries | the premium alone | not the filed figure | CP-04 section 3 |
| SF4 | worth a year | 12 per cent of the release less the margin | the release alone | not the filed figure | CP-04 section 3 |
| SF5 | a loss occurrence in the table | each storm one occurrence | storms peaking within 72 hours merged | same call, same bins | CP-04 section 2, and asserted inert |
| SF6 | the claims for the storms like it | incurred over hindcast, ratio of totals | the mean or median of the storms' ratios | same call, same bins | CP-04 section 2's wording, and asserted convergent |
| SF7 | within weeks of the storm before | any window from 25 to 69 days | a shorter or longer window | same storms classed | the record's gaps (none from 25 to 69 days), asserted |
| SF8 | the same storm in the hindcast | peak on the first damage date or the day after | the same date only | storms unmatched, never mismatched | one-to-one link asserted |
| SF9 | the storm before it in the table | the one before in its simulated year | chained across simulated years | same call and release | the table's year column, each year its own simulation; asserted |
| SF10 | the second-event cover's subject loss | the loss up to the occurrence cover's retention | the loss net of the occurrence cover | not the quoted cover | quotation B's subject loss |
| SF11 | the first loss occurrence of the period | the one whose 72 hours begin first, the year's first storm | the largest | not the quoted cover | quotation B |
| SF12 | reinstatement | one, at 100 per cent pro rata as to amount | free or pro rata as to time | not the quoted cover | quotations A and B |
| SF13 | the portfolio of their time | ratios are scale-free | on-levelled to 2027 | same ratios and call | asserted |
| SF14 | cost of capital | 12 per cent | another rate | not the filed figure | CP-04 section 3 |
| SF15 | the covers in force | the occurrence cover renewed on quotation A | the expiring terms | not the filed basis | CP-04 section 3, any further cover valued with it in force |
| SF16 | what an occurrence has cost us | paid and outstanding | paid only | not the expiring cover's basis | the wording's Ultimate Net Loss |
| SF17 | the 72 hours | the Reassured's choice of start | the first day not yet in one | same occurrences | the wording's clause 3, and asserted equal |
| SF18 | £1 million or more | each occurrence's incurred | each storm's | same list | the prompt, asserted |
| SF19 | home and farm policies | the extract's line column | the policy prefix | same split | asserted |
| SF20 | our share of the farm sums insured | the register's share on the whole coinsured policy | the holding on the register row only | ledgered ask device | the register keyed by the policy's main holding, asserted |
| SF21 | by where the holding is | the Holdings sheet's county | the correspondence county | ledgered ask hazard | the prompt |
| SF22 | the farm sums insured's unit | thousands of pounds | pounds | ledgered ask hazard | the columns' _000 |
| SF23 | the farm book | the workbook as extracted on 31 October 2026 | a date filter | same book | asserted, every policy with its holdings |

## Ladder

| Rung | Route | Release | Margin | Worth a year | Call |
|---|---|---|---|---|---|
| 0 | the model's losses as they stand | £4.8m | £0.90m | minus £0.32m | not bought |
| 1 | one factor, 1.06 (default path) | £4.9m | £0.87m | minus £0.28m | not bought |
| 2 | the factor by storm size | £5.0m | £0.87m | minus £0.27m | not bought |
| 3a | storms in years with more than one against the rest | £5.1m | £0.86m | minus £0.26m | not bought |
| 3b | later storms of the year against the first | £5.8m | £0.80m | minus £0.10m | not bought |
| 3c | the worst of 26 enumerated routes (later storms of the year, mean of ratios) | £6.0m | £0.78m | minus £0.06m | not bought |
| over | every storm at the follow-on ratio, 1.62 | £5.7m | £0.60m | £0.09m | bought, release and margin wrong |
| golden | each storm by its gap, 1.62 and 0.98 | £6.9m | £0.70m | £0.13m | bought |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every storm of the 2027 table and every storm of record | filed in CP-04; C1 |
| 2 Unit of account | the simulated year; each storm one loss occurrence | filed in CP-04 |
| 3 Attribution window | the 2027 programme year; each simulated year | filed in the quotation and CP-04 |
| 4 As-of dating | the claims extract of 31 October 2026; the farm book as extracted | the files' own dates; C1 |
| 5 Version basis | the 2027 portfolio's table, the hindcast and experience refreshed in the summer | filed in CP-04 |
| 6 Denominator | the hindcast of the same storms | filed in CP-04 |
| 7 Weighting | pounds paid over pounds modelled | filed in CP-04; C1 across the mean and median (SF6) |
| 8 Window length | within weeks of the storm before | C3, every window from 25 to 69 days (SF7) |
| 9 Boundary inclusivity | exactly 50 years; £1 million or more | filed; nothing on an edge, asserted |
| 10 Rounding path | pounds throughout, rounded once at the end | the prompt's rounding sentence |
| 11 Tie-break | none arises | asserted, no tie at the 50th year or on the floor |
| 12 Maturity and censoring | the 2026 claims paid and outstanding at the extract; the record's storms closed | the wording's Ultimate Net Loss (SF16) |
| 13 Order of operations | recoveries, then reinstatement premiums added back, then the average | filed in CP-04 and the quotation |
| 14 Row order | by date within each simulated year | C1, the table's own order |
| 15 Duplicate resolution | reopened claim lines kept; the register's lapsed arrangements dropped | ledgered ask devices; none on the main path |
| 16 Identity normalisation | the record linked by date; the adjusters' spaced claim number; the CPH with and without its slashes and its previous number | C1 on the main link (SF8); ask devices |
| 17 Netting against gross | the second-event cover on the loss up to the occurrence cover's retention | filed in quotation B (SF10) |
| 18 Dimensional units | pounds; the farm book in thousands | the columns' own names (SF22) |
| 19 Code and status semantics | the claims' Storm peril and Home or Farm line | the extract's own codes |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | the 72-hour clause on the 2026 claims; one storm one occurrence in the table | filed in the wording and CP-04 (SF5, SF17) |
| 22 Forward window contents | the vendor's table for the 2027 portfolio | the shipped table |

## Literal reader

Executed word for word on the cut pack: CP-04's 1-in-200, the average of the 50 worst of the 10,000 simulated years of the 2027 table, each storm one loss occurrence costed at incurred over hindcast for the past storms like it, the occurrence cover in force in both valuations and the worth at 12 per cent less the margin; the literal reader must decide which past storms are like a simulated storm, which no sentence says, and every reading the record leaves standing (the gap class under any window from 25 to 69 days and any of the three estimators) files the golden, while the readings the record refutes (one class, size, rank, year type or season type) fail because the record's later storms on quiet seasons cost what the model says (SF6, SF7 and the ladder, asserted in checks.py and recomputed by verify.py from target.zip alone).

## Oracles

None ships. No control ties only under the golden or only on a wrong route; the hindcast and the experience are the inputs every route reads; the request names no answer; generator/verify.py recomputes the call and every graded figure from target.zip alone, taking the covers' terms from the quotation's text.

leak.py (REVIEW, 2026-10-31, as-of 2026-11-02): sweep 2 flags "the model" twice in CP-04, harmless, the catastrophe model is the policy's own subject in the mutual's words; sweep 3 flags the quotation for carrying the call's words, harmless, it names the cover it quotes and gives no figure the call is graded on.

## Ask sheet

**Ask A, each 2026 loss occurrence of £1 million or more, its cost on home and on farm policies to the nearest £1,000, then the expiring cover's recovery on the year and the reinstatement premium it calls** (8 figures). H18: an audit trail of the expiring cover the renewal replaces, on claims the call never reads. Primary device D8 (a recorded date for the event date): the web form records the day it is sent as the loss date, two to nine days after the damage, so the recorded dates spread each storm's web claims over the following week and out of its 72 hours; only the adjusters' instructions carry the day the damage was done, keyed by the claim number as their portal spaces it. Second primary (which records are one event, by cardinality): a claim open when the next storm came was reopened for the further damage on a suffixed line that keeps the claim's loss date, and the adjusters were instructed a second time for it; a claim with two lines and two instructions has done damage on two days, while a claim with two lines and one instruction is a later payment on the same damage. Hazards: ordinary wind claims on other days, the 72-hour choice, the reopened lines that look like duplicates. Path: the claims extract, the adjusters' instructions and the wording (3 files, 11 columns). Stops: the recorded dates (eight occurrences, recovery £3,631,000), every line at the claim's first instruction (recovery £12,590,000), at its last (£11,085,000), the instructions joined on the full claim number (£12,303,000); golden £12,015,000.

**Ask B, our share of the farm sums insured, buildings and farm contents apart, in each county by where the holding is, in £ million to one decimal** (8 figures). H18: the exposure the programme protects, on the farm book the call never reads. Primary device D7 (the true key elsewhere): the coinsurance register keys each coinsured policy by its main holding's CPH, and the share is a share of the whole policy, so matching it holding by holding leaves every other holding of the policy at the full sum. Second primary D2 (a key stored before a switch): the register keeps the main holding's CPH as it stood when the arrangement was last renewed, so a holding the Rural Payments Agency renumbered since then is under its old number, found only in the Holdings sheet's previous_cph, while the register's other unmatched rows are arrangements on policies that did not renew; the join on the current CPH looks clean. Hazards: thousands of pounds, the CPH with and without its slashes, the policy's correspondence county. Path: the farm workbook's two sheets and the register (3 sources, 10 columns). Stops: the register on the current main CPH only (Cornwall buildings £1,315.6m), holding by holding (£1,426.4m), no shares (£1,528.3m); golden £1,302.1m.

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the recorded loss dates kept (D8) | A | recovery minus £8.4m |
| every line at the first instruction (fan-out) | A | Juno farm minus £101,000, recovery plus £575,000 |
| the register on the current CPH only (D2) | B | Cornwall buildings plus £13.5m |
| the register joined holding by holding (D7) | B | Devon buildings plus £132.4m |
| the correspondence county (hazard) | B | Dorset buildings minus £99.3m |

Referee: the adjusters' instructions for the day of damage and the second instruction; the Holdings sheet's previous_cph for the renumbered holdings.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, the occurrences' home and farm costs | web dates re-dated from the adjusters, the fan-out collapsed to the claim's first instruction, the 72-hour clause executed | miss |
| Ask A, the recovery and the reinstatement premium | the same | miss |
| Ask B, Cornwall and Devon | the register on the policies' current main CPH, unmatched rows dropped as lapsed, thousands and slashes handled, the holdings' counties | miss |
| Ask B, Somerset and Dorset | the same | miss |

Measured by: generator/pair.py on the cut pack (target.zip 5102c315): the cracker keeps 0 of the 16 ask figures (also 0 keeping the fan-out at the last instruction, joining on the full claim number, joining the shares holding by holding, or keeping the recorded dates); the mirror (stopped at the default path on the call) keeps 0 of 16 and 0 of the 7 graded main figures.

Pair ceiling: 26.0 ((38 + 7 + 55 x 0) and (0 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Tried and rejected

- Pack 1 of the prototype (2026-10-24, seed 3061) hid each imported car's pack history before its Dutch registration (the log started at the Dutch registration), so a solver could not know an import's pack state and both probes repaired it differently (sonnet calibrated the imports down by 0.74, opus modelled the abroad replacements in expectation): a fork, not the stump. The log is now the OEMs' EU-wide record plus Voltwerk's own, and a car whose pack failed outside warranty abroad is scrapped there and never imported.
- The prototype's truth carried a scrappage and export rate that no file shows; the forecast now takes a car in use to stay in use through 2027, filed in the tooling plan.
- The first cut's imports arrived about six years old, inside the eight-year warranty, and moved the call by three per cent and one lot; the Mira city car is now the platform kept alive by old imports from abroad, as old cheap EVs are.
- A refurbished pack failing inside Voltwerk's two years was logged as an OEM warranty fit in the prototype (99 rows): fixed, a Voltwerk-warranty failure takes another refurbished pack under Voltwerk's cover.
- The first stage-2 world kept the Mira city car launched in 2014 with 520 imports a month and an eight-year warranty: its arrival stream still ramped through the replay windows, so the 6- and 24-month windows spread the Mira's forecast by 51 and the total straddled a hundred bin. The Mira is now launched in 2013 with a five-year warranty and a steeper wear-out, its stream flat over the last 36 months and its imports arriving as survivors on their original packs.
- An estimand counting only failures outside both warranties left out the packs Voltwerk itself replaces under its two-year warranty, which the line supplies too; the plan now counts every failure outside the OEM warranty.
- Grading each platform's forecast paid the wrong route: the register-only route files four of the five platforms' forecasts at the nearest hundred (only the Mira moves); the prompt grades the slots and the total.
- Ask B's re-keying first moved the naive share by under 0.1 point on the Volta hatch, the new ids passing at about the platform's own rate; the BMS is now replaced in seven reworks in ten and the line seed (31062, from 750 swept) keeps every platform's natural read and over-repair outside its bin on all three asks, worst golden edge 0.155 of a bin.
- The dealer rows of the replacement log first carried plates typed with dashes; a solver who joined without normalising them filed Mira 1,350 and Volta 1,000, so that mess could move the call (dataset-generation R2) and was cut: both sources now carry the register's own plate format.
- Ask C's first device, dock 2 setting its rejects aside without scanning them (absent from the intake export, present at the recycler without a core code), was landed 5 of 5 by the stage 4 reader: dock 2's zero rejects and the blank core codes sit on the path of anyone counting rejects, and the judge found the dock's practice stated in no file. Re-sited onto the grade's date (D2): the intake export carries each core's grade on 1 July 2026, so a core the line built on and scrapped reads AFGEKEURD, and only its work order in the MES shows it passed intake; every ask C figure is unchanged.
- The plan's "a car in use in the Netherlands is taken to stay in use through 2027" read to the stage 4 reader, and to the judge as its one soft spot, as freezing the register of 30 June 2026; the sentence now places the car in 2027 ("a car in use in the Netherlands in 2027 is taken to stay in use for the rest of the year"), the population the estimand already files, and names no import.
- The portal returned the build on determinism (both judges: Gates C, D and E, underspecified_objective, A, B and G passing): the plan as shipped named the register as its only source and its only dynamics clause was about exits, so both judges forecast the register of 30 June 2026 alone (3,448, 3,500 with a judge's renewals), and a judge also summed ask A's batch lines as written. Pinning the population to the register was refused (it makes the judges' answer the golden and spends the stump), and filing the projection (a twelfth a month at the trailing rate, mix and age) was refused (rule application, CLAUDE.md rule 3). Closed instead by the WHAT at authority: plan section 3 files the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027 (SF25) and one pack per car (SF26), the projection left open and forced by C1 over 144 projections, and the line notes file the lot stock rule for ask A (SF27); no graded or stated figure moved (freeze.py). The cost: that the later registrations are in the fleet is now readable, so the decisive rung keeps only what no sentence says, which of them fall due; the default path's answer is now the easy route's on the literal estimand (the later registrations carried as new cars).
- 2026-10-31, architecture 1 spent at the batch 1 triage: shipped 10-24 and reshipped 10-26 after the portal's determinism block, its isolated cold reader reproduced the call cell for cell (Volta 900, Kestrel 250, Plover 350, Mira 1,450, Tern 50, 3,800) and named the decisive step a procedure, since the repair's population sentence and the plan's pack-age sentence read together as the method; the surviving risk the note recorded was that conditioning a survival curve on survival to the as-of date is reflex reachable. Re-rooted in a new world rather than hardened.
- 2026-10-31, re-root screen before this draw: an actuarial reinsurance-capital draw (a county mutual's 2027 windstorm programme, the vendor's year loss table loaded storm by storm for demand surge read off the market's index loss) cleared `guard.py check` and was set aside unregistered, because task309 (FORTIFIED roofs, one cut ratio across storms that varies with gust intensity, carried through a vendor event set) is the same insight in the same domain; regression to the mean in a health-services pilot and a healthy-adopter uptake were set aside as general statistical mechanisms readers name unprompted (task308's screen of six); stale-priced returns in a portfolio's risk budget were set aside as task135's cross-day covariance.
- 2026-10-31, architecture 2 (the development corporation's 2027 inward investment award between a logistics hub on the city region's boundary and an inland food plant, the induced round read where each project's staff live) drawn, registered and spent at stage 2 before any data was cut: the survivor anatomy's Actor test failed on paper, since where the hub's staff live is one join from a column (a roster postcode against the postcode directory's local authority), and every honest way to ship it (a roster, a travel plan's postcode survey, a commuting flow for the depot's zone) is a column or a sentence that sends a solver to it; the IO world offered no relation between rows that carries the induced round's leak.
- 2026-10-31, architecture 3 first cut (an occurrence cover against an annual aggregate cover): the two covers' releases separated by about 1.12 times under every loading of the storms, so no costing of the record moved the call; redesigned at stage 2 into the second-event cover, buy or not, on the occurrence cover's retained band.
- 2026-10-31, the second-event cover on the 50th worst year alone, an upper layer above the occurrence cover and a tall tower from 12 to 60 million were each priced: the single year was noisy enough to flip on the seed, the upper layer's release was small and noisy, and the tower closed the gap between the cheap routes and the golden; the capital policy's average of the 50 worst years and the 7.5 million xs 4 million band were kept.
- 2026-10-31, the first record draw (seed 498): the ratio of totals over the later storms of each season landed the call (worth plus 0.13 million) with the golden's release, and the mean of ratios over the later storms of each year landed it too; a stormier physics with more trains a season made the rank routes buy harder, and shifting a year's first train to clear the year end left nine gaps of exactly 70 days and one inside the window corridor. The record is now drawn with trains kept apart across the year end and searched over 7,500 seeds for one where every rank, year, season, size and pooled route under every estimator files the wrong call (seed 2703, worst route minus 0.06 million).
- 2026-10-31, an exposure ask on the home book (sums insured in force by county) was set aside: in-force by date, renewal terms under new numbers and lapses are rule application a careful solver executes, with no reconstruction left after noticing; the home extract ships as a distractor and the farm book carries the exposure ask.
- 2026-10-31, a reopened claim's further damage first came to some claims before they had been notified, which no claims system allows and which left the pairing of lines and instructions unrecoverable for those claims; further damage now comes only to a claim already open with its adjuster instructed.
