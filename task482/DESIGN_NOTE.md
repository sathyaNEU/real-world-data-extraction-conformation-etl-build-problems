# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 13, drawn 2026-10-24 after architectures 1
to 12 were spent at stage 4: a fresh world and pack in the ETL objective, a clinically integrated network's 2027
two-sided risk elections for its thirteen independent primary care practices, each practice's 2026 total cost of care
per attributed member month carried from the payers' interim attribution run to the year-end attribution, where the
members a retrospective attribution adds after the cut are mostly members whose one primary care visit of the year
falls late in it.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v13, lineage v1 to v12 spent), checked
  2026-10-24 after a fetch of main: WARN, no BLOCK, nearest driver on file 0.08. The window the axis bans read
  (task281, task484 v3 and task305, the live cards filed last; task482 v12, task280 and task279 carry
  `architecture_spent`) closes the strategies forecast_method_backtest, causal_design and population_selection, the
  forums minister_or_cabinet, council_or_assembly and committee_or_panel, the forcing events budget_or_appropriation,
  season_or_peak and vote_or_meeting, the organisations government_agency, local_government and retailer_or_ecommerce,
  the roles research_desk, policy_adviser and finance_controller, the context artifacts published_series, register and
  monitoring_export, the calibration existing_book_actuals, and the shapes 14 and 07. The draw's honest labels clear
  all of them: the network's board enters each practice in the payers' 2027 track (forum board_of_directors, forcing
  event purchase_order_or_contract, the payers' election deadline), organisation hospital_or_health_provider, role
  portfolio_manager (the director who runs the three payer contracts' performance), the shape a scorecard against each
  practice's own threshold (10), the context artifact the payers' 2025 settlement statements (close_out_summary), the
  calibration organ the payers' final 2025 attribution with the claims the network holds for it
  (prior_period_close_out).
- **WARNs answered.** `overuse.shape` (10 in three of the last twelve): each practice is scored against its own
  benchmark threshold, which is shape 10 and no other. `repeat.deliverables` (png and xlsx against task281): the
  workbook is the board packet's exhibit and the practices against their thresholds read at a glance as a chart.
  `repeat.question_form` (which, against task484 v3): the board names the practices it enters, so the question asks
  which. People drawn with `guard.py names --geo "United States" --seed 482 --n 24`: Andre O'Connor (the network's
  president, the requester), Joel Brewer (the director of payer performance analytics, whose files these are) and
  Carlos Howard (Merrinlake Health Plan's provider performance manager, who signs its statement), owners in file
  properties and statement sign-offs only; the names of architectures 9 to 12 are not reused, and Evelyn Morse,
  Michelle Curtis, Olivia Williamson, Diana Jenkins, Jennifer Nelson, Richard Lynch, Adam Johnston and Anthony Jackson
  were set aside on `people.first`.
- **Pairing:** Healthcare Delivery & Health Economics, task type `payment-claims-health-plan-analytics`, which serves
  ETL: three commercial payers' feeds in three layouts (eligibility and member months, claim lines, monthly attribution
  runs), the network's practice and clinician roster with its effective dates, its master patient index across the
  payers' member identifiers, and the network's performance standard conformed into each practice's 2026 total cost of
  care per attributed member month on the standard's basis, against its benchmark.
- **The decision and the quantity:** the network's 2026 shared savings agreements with Merrinlake Health Plan,
  Kesselcrest Benefit Partners and Pemberglen Mutual Health (all invented) share savings on one measure, set out in the
  network's Performance Standard (Exhibit B to each agreement) and pooled across the three payers: a practice's total
  cost of care per attributed member month, the allowed amounts for covered medical and pharmacy services incurred in
  the year for the members attributed to it, each member's year capped at USD 250,000, over every month of the year
  the member was enrolled with a payer. A member is attributed for the year to the practice whose primary care
  clinicians furnished the plurality of the member's qualifying primary care services in the year, final on each
  payer's April run after the year; a practice's benchmark is its 2025 figure on the final 2025 attribution times the
  agreements' 2026 trend of 1.052. For 2027 the payers offer a two-sided track (a larger share of savings, a share of
  losses), and the board's resolution enters a practice only where its 2026 figure on the payers' final 2026
  attribution comes in at least 2 per cent under its benchmark. The elections are due with the payers by 30 October
  2026, so the board decides at its meeting of 29 October on the network's projection of each practice's 2026 figure.
  The quantity is forward: the year and its attribution close after the decision.
- **Shape:** `10`, a scorecard against thresholds: each of the thirteen practices' projected 2026 figure on the final
  attribution, its benchmark and 98 per cent of it, and whether it enters the two-sided track, beside the call (which
  practices enter); the asks are wide and fixed at stage 2.
- **Strategy:** `maturity_censoring` (the year's attributed population is still arriving at the cut: a member joins it
  when a qualifying visit happens, and the interim run holds only the members whose visit has happened); not
  population_selection (the standard files the population in full, and the difficulty is that it has not finished
  arriving) and not forecast_method_backtest (no method is chosen by a back-test). Gate G `etl_conformance` (each
  practice's conformed cost of care on the standard's basis judged against the board's threshold); gap `population`
  (the run's members are not the year's attributed members) and `time` (the year is open); pattern none; generators
  G13 (decisive: the run's horizon is the cut, the standard's the year), G6 (the added members' composition), G16
  (each practice's own run-out, which the data select over a pooled one) and G17. Layer 2 family `field_method`,
  pattern `own:a retrospective attribution's run-out carried from last year's same cut`.
- **World:** the United States, Wisconsin, USD; the Larrowbrook Physician Network, a physician-led clinically
  integrated network of thirteen independent primary care practices in the state's east-central counties, its
  practices and the three payers invented, the names screened against populated places and organisations in the
  field before the pack is cut (H21).
- **Forcing fact:** the payers' 2027 track elections are due by 30 October 2026, and the board meets on 29 October.
- **The field facts the mechanism stands on:**
  - Retrospective attribution counts a member for the whole year once a qualifying primary care visit happens, so a
    payer's interim run (monthly, on services incurred to date) lists only the members whose visit has already
    happened; under the data agreements a payer sends the network claims only for the members on a run, and the
    claims for members attributed later come with the final run.
  - The members a year's attribution still adds after August are mostly healthy members with one visit a year, a
    physical or a well visit in the autumn, who cost a fraction of the run's members over a whole year of enrollment,
    while members with chronic conditions visit early and often.
  - Practices differ in when their members come (January wellness outreach at some, employers whose members book late
    in the year at others), so the share of a year's attribution still to come at the end of August runs from under a
    tenth to over a quarter.
- **Data-native sentence:** the payers' interim run attributes only the members whose qualifying visit has already
  happened, and the network holds claims only for them, while the year-end attribution adds the members whose one
  visit of the year comes after the cut, with their whole year of enrollment and their small amounts; how many they are
  and what they cost shows in 2025's own attribution re-run at the same cut on the 2025 claims the network holds.
- **Paper screen, then the cut pack** (`generator/golden.py` on the pack, `checks.py` on the world's clean truth): on
  the October runs' interim measure three practices come in under their thresholds; each practice's own 2025 run-out
  (its final figure over the figure of the members attributed by 31 August) runs from 0.822 to 0.996, a per-payer
  run-out agrees with it, and a pooled network run-out (0.881) files a different set; Birrelhaven, the paediatric
  clinic, is placed just over its threshold because its late members cost nearly what its others cost, so reading the
  October run's short counts as members who cost nothing enters it.
- **The WHAT screen.** Population: each practice's members on the payers' final 2026 attribution (the standard's
  attribution clause), members a later visit will attribute included. Outcome: allowed amounts for covered services
  incurred in 2026, each member's year capped at USD 250,000. Unit: USD per attributed member month (every 2026 month
  of enrollment), against 98 per cent of the practice's benchmark. Window: calendar 2026. Comparison: each practice
  against its own benchmark. The decisive step settles none of them: it is how the year's attributed population and
  its cost are reached from the interim run, which no record or filed rule states and which only the 2025 attribution,
  re-run at the same cut, measures.
- **Sources, one line each:**
  - prospective and retrospective attribution in shared savings programs: preliminary lists during the year, final
    assignment after it;
  - the plurality of qualifying primary care services as the attribution rule, and the payer's data sharing limited to
    attributed members;
  - annual preventive and well visits as the reason many low users of care see a clinician at all in a year.
- **Same-puzzle and same-driver tests:** (population and time, none, designation_set) and (population and time, none,
  etl_conformance) against the last twelve builds, lineage included: no match.
- **Abstraction test:** the nearest drivers (0.08 and under) stripped of nouns: task103 v3 reads what a record of
  contact stands for beside a standing authorization; task268 v1 counts the people present at a place on a typical day;
  task483 rebuilds two quantities recorded at a coarser grain. None states a population that fills by contact during
  the period it is measured over. The card's differentiation answers task451 (a closed year's unpaid claims for twelve
  partners' total cost of care), task458 (a lasting trait seen through events while each member is observed), task130's
  lineage (a group chosen on an extreme outcome) and this slot's architecture 10 (each member's share of a lifetime
  total).

## Three rules

Task type: Healthcare Delivery & Health Economics, payment-claims-health-plan-analytics, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each practice's 2026 total cost of care per attributed member month on the payers' final 2026 attribution, a rate over a population that a retrospective attribution is still filling at the cut; health plan analytics develops any immature quantity from the prior year's development at the same age (the payers' own completion factors do it for the claims), and the attributed population needs the same development: each practice's 2025 attribution re-run at the October run's cut against its final 2025 run is the run-out that carries its interim measure to the year.
Swap: "which of our thirteen schools enter the 2027 two-sided track on each school's 2026 cost per enrolled student-month" (schools for practices, students for members) has an enrolment roll fixed before the year starts, so nobody joins the population through a visit after the cut, no interim run lists only the students seen so far, and a run-out has nothing to carry: the task stops making sense.
Layer 1: three claim feeds in three layouts (Merrinlake's CSV voiding and replacing reprocessed claims under new numbers, Kesselcrest's pipe-delimited extract in cents with MM/DD/YYYY dates whose adjusted lines stand beside a suffixed reprocessed claim, Pemberglen's JSON of claim versions), three coverage files with open spans written as 9999-12-31 or left blank, three attribution files (Kesselcrest's a workbook with a title block above its header), TINs with and without a hyphen, each payer's own member identifiers beside the network's master patient index, the roster's effective-dated clinician rows (a clinician who moved practices on 1 July 2025, one who joined on 1 April 2026), and 2025 claims paid after the 31 March cut-off still in the feeds; each is what that payer's or the network's system writes, none is placed to be caught, and mishandling any one leaves the call (checks.py R2).
Layer 2: field_method, an immature retrospectively attributed population developed to its final state: each practice's interim measure carried to the year by its own 2025 run-out at the same cut, the development a health plan actuary applies to any quantity still maturing, which the data select over a pooled network run-out (the practices' run-outs run 0.822 to 0.996 against a pooled 0.881).
Decisive step: recognising that the October interim run attributes only the members whose qualifying visit has already been paid, so the year-end attribution will add the members whose one visit of 2026 falls after August, with every month of their coverage and their own costs, and carrying each practice's interim measure to the year by its own 2025 run-out: its 2025 measure on the final run over the January to August measure of the members the 2025 attribution, re-run on the 2025 claims at 31 August and 30 September, assigns to it.
Not semantics: with every field read correctly (claims at their current version, Kesselcrest's cents in dollars, member months from the spans, the runs' TINs mapped to practices, the completion factors by payer and incurred month), the easy route still takes the October run's interim measure as the 2026 figure, because nothing in any file marks a member as not yet attributed: each run is the payer's own, complete for what it covers, and the standard's section 4.1 defines its measure.
Not rule application: the standard files the population (the final 2026 attribution), the outcome, the cap, the unit and the comparison, and its section 4.1 files the interim measure, but no clause says how a year's figure on the final attribution is reached from an interim run, so executing every filed rule computes the interim measure and enters Ostrelwood, Thornelfield and Jesselford. Measured on the cut pack: the enumerated family (the interim measure as it stands; carried by the final 2025 members' own January to August against their year; scaled by the October run's short counts as members who cost nothing, by members or by member months; carried by one pooled run-out; carried by each practice's own run-out) enters 3 to 11 practices in four different sets; the standing family (every construction that measures each practice's own 2025 run-out at the October run's cut: the 32 of the cross product of the re-run's paid basis, its cut-off, the same-cut figure's basis, the claim version and the grain, the attribution files' own qualifying-day fields, either tie-break) enters the golden nine, worst margin 2.1 per cent; and what rules out the pooled run-out is no filed clause but the practices' own run-outs, 0.822 to 0.996, which only the same re-run measures.
Analyst test: A strong analyst who reads every file correctly conforms the three feeds, computes each practice's interim measure on the October runs as section 4.1 defines it (claims incurred January to August and paid by the feed date over each payer's completion factor by incurred month, capped year to date, over the run members' January to August member months), takes it as the practice's 2026 figure against 98 per cent of its benchmark, and enters Ostrelwood, Thornelfield and Jesselford alone.
Estimand: each practice's 2026 network measure (the allowed amounts, at current version, of the claims for covered medical and pharmacy services incurred in 2026 and first paid by 31 March 2027, each member's year capped at USD 250,000, over every 2026 month of coverage) for its members on the payers' final 2026 attribution, the members a later visit attributes included, against 98 per cent of its benchmark (its 2025 measure on the final 2025 attribution times 1.052); filed in the standard's sections 2 and 3 and the resolution.
No decoy: nothing is planted; the feeds, runs, roster, index, fee schedules, remittances and statements are the payers' and the network's own records as their systems write them, no memo, draft, interim report, briefing or stakeholder figure carries a wrong answer, and no filed sentence prescribes taking the interim measure as the year's figure.
No certified replay: no certified or published figure is reproduced to recover the method; the payers' 2025 settlement statements carry their own Schedule A bases (other caps, Kesselcrest medical only) and no 2026 figure, and the run-out follows from the estimand and the 2025 records.
Lesson: a population that a retrospective rule fills by contact during the year is short at any interim cut, by an amount and at a cost that differ by unit, so its interim rate has to be developed to the year like any other immature quantity, from the unit's own run-out at the same cut a year earlier; no build on file develops the attributed population itself rather than the claims or a count.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect on the call (checks.py) |
|---|---|---|---|---|
| reprocessed claims voided and replaced under new numbers | Merrinlake's claim system | mlh_tcoc_claims_2025-01_2026-09.csv | the void lines dropped, the originals kept beside their replacements | none (R2) |
| adjusted lines beside a suffixed reprocessed claim | Kesselcrest's claim system | KBP_CLAIMS_LPN_20261009.txt | every line kept | none (R2) |
| claim versions | Pemberglen's adjudication engine | pmh_partner_claims_2026-10-12.json | every version summed | none (R2) |
| allowed in cents, MM/DD/YYYY dates, pipes | Kesselcrest's partner extract | the KBP text files | read as dollars or as day-first dates | loud (impossible amounts or unparseable dates) |
| open coverage as 9999-12-31 or blank | each payer's eligibility system | the three coverage files | an open span ended at the feed date | none: every member month the measure counts unchanged (R2) |
| a title block above the header | Kesselcrest's reporting tool | KBP_ATTRIBUTION_PY2025F_PY2026R10.xlsx | the first row read as the header | loud (no member numbers) |
| TINs with and without a hyphen | the payers' provider files | the attribution and remittance files | joined as written | loud (a payer's members unmatched); every TIN maps once the hyphen is dropped (asserted) |
| member identifiers per payer, the master patient index | the payers and the network's registration | lpn_master_patient_index.csv | persons merged across payers | none: no patient holds two payers' coverage in one year (SF11) |
| a clinician's move on 1 July 2025, a new clinician on 1 April 2026 | the network's credentialing | lpn_primary_care_roster_2026-10.xlsx | each clinician at the current practice | none (R2, SF12) |
| 2025 claims paid after 31 March 2026 | the payers' feeds through October | the three claim feeds | counted in the 2025 measure | none (R2, SF16) |

## Default path

1. Conform the three payers' feeds: claims at their current version (Merrinlake's voids and replacements, Kesselcrest's
   adjusted lines, Pemberglen's latest version), Kesselcrest's cents in dollars, the three date formats, member months
   from the coverage spans, every run's TIN mapped to a practice through the roster.
2. Compute each practice's 2025 network measure on the payers' final 2025 runs (claims incurred in 2025 and first paid
   by 31 March 2026, each member capped at USD 250,000, over the year's member months, pooled across the payers), its
   benchmark at 1.052 times it and its threshold at 98 per cent of the benchmark.
3. Compute each practice's interim measure on the payers' October runs as section 4.1 sets it out: claims incurred
   January to August 2026 and paid by the feed date, divided by each payer's completion factor by incurred month, each
   member's year to date capped, over the run members' January to August member months, pooled across the payers.
4. Take the interim measure as the practice's 2026 figure and compare it with the threshold.

Ends on: Ostrelwood, Thornelfield and Jesselford enter the two-sided track; the other ten stay one-sided.

Golden: Ostrelwood, Callowglen, Thornelfield, Raddelview, Jesselford, Nerrincreek, Torrinridge, Mallowcrest and Garrowdale enter; Haddelcrest, Birrelhaven, Wexelmoor and Prestelglen stay one-sided.

## Stump sentence

The default path takes each practice's interim measure on the October runs as its 2026 figure, so the six practices whose members visit late in the year (Callowglen, Raddelview, Nerrincreek, Torrinridge, Mallowcrest and Garrowdale) sit 4.6 to 15.2 per cent over their thresholds and Ostrelwood, Thornelfield and Jesselford enter alone; but the October run attributes only the members whose qualifying visit has been paid, 24 to 30 per cent short of the 2025 final counts at those six, and the year-end attribution adds the members whose one visit of 2026 falls after August, with every month of their coverage and a fraction of the cost: carried by each practice's own 2025 run-out (0.822 to 0.885 at the six) all six come in 5.4 to 7.9 per cent under, while Birrelhaven, whose late members are children costing nearly what its other members cost (run-out 0.944), stays 5.4 per cent over, and nine practices enter.

## Readability screen

Measured on the cut pack (`generator/golden.py`): thresholds 746.07 (Ostrelwood), 387.84 (Callowglen), 484.33
(Thornelfield), 803.19 (Haddelcrest), 175.16 (Birrelhaven), 469.35 (Raddelview), 546.89 (Jesselford), 380.20
(Nerrincreek), 930.98 (Wexelmoor), 398.46 (Torrinridge), 166.12 (Mallowcrest), 770.98 (Prestelglen) and 446.46
(Garrowdale), USD per member month.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the interim measure (default) | each practice's section 4.1 measure on the October runs as its 2026 figure | the standard defines it; the runs are the payers' own | readable |
| L1 the year's seasonality | the interim measure carried by the final 2025 members' own January to August against their year | the 2025 claims of the final members | readable |
| L2 the short counts as members who cost nothing | the interim measure scaled by the October run's members over the 2025 final run's, or by the member months | the attribution files' counts | readable |
| L3 one pooled run-out | every practice carried by the network's 2025 run-out of 0.881 | the same re-run, pooled | readable |
| G each practice's own run-out (decisive) | the interim measure times the practice's 2025 measure over the January to August measure of its members at the same cut, the 2025 attribution re-run from the 2025 claims at 31 August and 30 September | nothing: no file holds a 2025 interim run or marks a member as attributed late; the re-run is the standard's section 2 executed on 2025's claims at the October run's cut, which no clause asks for | silent |

L2 lands one practice off: the members still to come at Birrelhaven are children who cost nearly what the others cost,
so reading them as costing nothing takes it 12.8 per cent under its threshold where its own run-out leaves it 5.4 per
cent over. L3 misplaces the practices whose members come early (Haddelcrest, Wexelmoor) and Birrelhaven.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | total cost of care | allowed amounts for covered medical and pharmacy services | medical alone (Kesselcrest's settlement basis) | same call | section 3.1 |
| SF2 | the member cap | USD 250,000 a member-year | no cap; USD 150,000 | same call (asserted) | section 3.1 |
| SF3 | member month | a calendar month of coverage in force | days of coverage; coverage on the first | identical: every span starts on a first and ends on a month end (asserted) | section 3.2 |
| SF4 | a claim's year | incurred on its first date of service | its last date of service (19 lines cross the new year) | same call (asserted) | section 3.1 |
| SF5 | a claim's version | the current version of every claim first paid by the cut | the version in force at the cut | same call (asserted) | section 3.1 |
| SF6 | the interim measure's completion | each payer's factor by incurred month | the payer's mean factor; no factor | same call (asserted) | section 4.1 and Appendix C |
| SF7 | the interim cap | each member's year to date capped | uncapped | same call (asserted) | section 4.1 |
| SF8 | the 2025 re-run's cut | services incurred by 31 August 2025, a visit counted once a version was paid by 30 September 2025 | the visit's current version's paid date; every 2025 claim paid by 31 March 2026 | same call (asserted) | section 2.3's interim run executed on 2025 |
| SF9 | the same-cut figure | January to August 2025 claims paid by 31 March 2026 over the members' January to August months | as the network would have reported it at 30 September 2025, over the factors | same call (asserted) | the records converge |
| SF10 | the run-out's grain | by practice | by practice and payer, weighted by projected member months | same call (asserted) | the records converge |
| SF11 | a member | each payer's own member, member months summed across the payers | persons through the master patient index | identical: no patient holds two payers' coverage in one year (asserted) | sections 2.1 and 3.3 |
| SF12 | a qualifying service's practice | the clinician's practice on the roster on the date of service | the clinician's current practice | same call (asserted) | section 2.1 |
| SF13 | a tie | to the practice of the latest qualifying day | to the earliest | same call (asserted) | section 2.1 |
| SF14 | the benchmark | the 2025 network measure on the final 2025 runs times 1.052 | the payers' 2025 settlement benchmarks | another basis: each payer's Schedule A, no network figure | section 3.4 |
| SF15 | at least 2 per cent below | at or under 98 per cent of the benchmark | strictly under | same call: no practice within 4.9 per cent (asserted) | the resolution |
| SF16 | the 2025 measure's paid cut-off | first paid by 31 March 2026 | every 2025 claim the October feeds carry | same call (asserted) | section 3.1 |
| SF17 | the interim window | January to August 2026, the October run's service cut | January to September | not available: the completion factors stop at August | sections 2.3 and 4.1, Appendix C |
| SF18 | pooling across payers | each practice's costs and member months summed across the payers | per-payer projections weighted by projected member months | same call (asserted) | section 3.3 |
| SF19 | a fill's incurred date | the fill date | none other in the feeds | identical | section 3.1 |

The live readings of the deciding quantity (SF5, SF8, SF9, SF10) are asserted as a cross product, 32 constructions.

## Ladder

Measured on the cut pack (`golden.py`; `checks.py` asserts each on the pack and L0 and G on the world's clean truth).

| Rung | Practices entering | Flips from the golden | Call kept |
|---|---|---|---|
| L0 the interim measure (default) | Ostrelwood, Thornelfield, Jesselford | 6 | no |
| L1 the final 2025 members' seasonality | Ostrelwood, Thornelfield, Jesselford | 6 | no |
| L2 the short counts as members who cost nothing (members or member months) | the golden nine and Birrelhaven | 1 | no |
| L3 one pooled run-out (0.881) | eleven: the golden nine less Nerrincreek, with Haddelcrest, Birrelhaven and Wexelmoor | 4 | no |
| G each practice's own run-out | the nine | none | yes |
| T the world's own final 2026 attribution | measured, not graded (checks.py R3b) | | |

The golden's positions against the thresholds are 8.4, 6.1, 5.8, 7.1, 7.7, 5.4, 7.9, 7.4 and 6.3 per cent under for
Ostrelwood, Callowglen, Thornelfield, Raddelview, Jesselford, Nerrincreek, Torrinridge, Mallowcrest and Garrowdale, and
5.3, 5.4, 4.9 and 5.7 per cent over for Haddelcrest, Birrelhaven, Wexelmoor and Prestelglen; the default's are 4.1, 5.4
and 3.0 per cent under for its three and 4.6 to 15.2 per cent over for the rest. The correction tracks how many of each
practice's members are still to come (the October run holds 70 to 76 per cent of the 2025 final count at the six late
practices, 96 to 101 per cent at the early ones) and what they cost, not the practice's size.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | each practice's members on the payers' final 2026 attribution, the members a later visit attributes included | filed (standard 2.1 and 3.3, the resolution) |
| 2 Unit of account | a practice's USD per attributed member month, pooled across the payers | filed (3.3); SF18 |
| 3 Attribution window | services incurred in 2026 | filed (3.1); SF4 |
| 4 As-of dating | the October feeds (7, 9 and 12 October 2026), the October runs on services to 31 August paid by 30 September | filed (2.3, 4.1); C1 |
| 5 Version basis | each claim at its current version | filed (3.1); SF5 |
| 6 Denominator | member months of coverage in force | filed (3.2); SF3 |
| 7 Weighting | costs and member months summed across payers | filed (3.3); SF10, SF18 asserted |
| 8 Window length | the calendar year; the interim January to August | filed (3.1, 4.1); SF17 |
| 9 Boundary inclusivity | at or under 98 per cent of the benchmark | filed (the resolution); SF15, margins asserted |
| 10 Rounding path | elections on unrounded figures; benchmarks and thresholds to the cent | the prompt's closing sentence; C1 |
| 11 Tie-break | attribution ties to the latest qualifying day | filed (2.1); SF13 |
| 12 Maturity and censoring | the 2026 claims completed by the payers' factors, the 2026 attribution by each practice's 2025 run-out | the decisive step; the factors filed (Appendix C) |
| 13 Order of operations | cap each member's year, then sum by practice | filed (3.1, 3.3); C1 |
| 14 Row order | none: every figure is a set computation | C1 |
| 15 Duplicate resolution | superseded versions and void lines out | filed (3.1, the field guide); R2 asserted |
| 16 Identity normalisation | TINs with or without a hyphen; members per payer, the index across them | the roster and the field guide; SF11, asserted |
| 17 Netting against gross | void lines net their originals | the field guide; R2 asserted |
| 18 Dimensional units | USD, Kesselcrest's cents | the field guide; loud if misread |
| 19 Code and status semantics | Appendix A's qualifying codes; claim types; status P and A | filed (Appendix A, the field guide) |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | commercial members only; each payer's settlement under its own Schedule A | filed (title, 1); SF14 |
| 22 Forward window contents | the 2026 attribution and run-out after the cut, carried by each practice's 2025 run-out | the decisive step; nothing else forward is estimated |

## Literal reader

Executing the prompt and every filed sentence word for word: the resolution enters a practice when its 2026 network
measure on the payers' final 2026 attribution comes in at least 2 per cent under its benchmark, and asks for the
network's projection of that figure because the elections close before the final runs. The standard defines the final
run for 2026 as the payers' April 2027 run on all qualifying services incurred in 2026, and the measure on it; no file
holds that run. The October run is an interim run (section 2.3) on services through August paid by September, and
section 4.1 defines its measure for management information. A literal reader therefore has to project the final run's
figure, and the only record of how a year's attribution and its cost move from the August cut to the final run is
2025's own, re-run from the 2025 claims under section 2 at the same cut: the attribution files show the October run
22 to 30 per cent short of the 2025 final counts at seven practices and within 4 per cent of them at the other six,
and the 2025 re-run shows what the members added after the cut cost. Taking the interim measure as the year's figure assumes the
final runs add no one, which the 2025 records contradict; the golden is the run-out those records imply.

## Oracles

No file ties only under the golden or only on a wrong read. No shipped file states a practice's 2026 figure on any
attribution or ranks the practices on the elections: the attribution files list members, the claims list services, the
standard and the resolution state rules, and the payers' 2025 settlement statements state each payer's own 2025
settlement on its own Schedule A. The asks' referees: Pemberglen's payment reference carries the month a line covers
(the device's evidence, never an answer), and the standard's section 5.1 fees carry Kesselcrest's commercial rate.

## Ask sheet

The call's declared population is each practice's members on the October runs and on the final 2025 runs, their
claims' allowed amounts and their coverage. Ask A reads the E&M lines' codes and allowed amounts against the fee
schedules, which the call never reads (the call reads an E&M line's allowed amount and its qualifying day, never its
level: re-coding every E&M line to one level leaves every call figure identical, asserted); ask B reads the three
remittance files, which the call never reads (emptied, every call figure identical, asserted).

- **Ask A, each practice's share of its clinicians' January to August 2026 established-patient visits (99211 to
  99215, in person or by telehealth) the payers paid at level 5, per cent to one decimal (13 figures).** H18 home: a
  measure every practice carries that the elections do not turn on, the level the payers pay its visits at, beside its
  cost. User: the payer performance director, whose payers' level reviews cut what the practices are paid. Primary
  device (silent, D3 two meanings one column apart): Kesselcrest's level review from 1 March 2026 allows a share of
  99215 visits at its 99214 rate and the claim keeps the code billed; nothing on the feed marks a reviewed claim, and
  only the allowed amount against Kesselcrest's 2026 schedule shows it. Second device (silent, D3 a per-row
  convention): Merrinlake allows an E&M billed with modifier 25 beside a same-day minor procedure by the same clinician
  at half its rate, so its level is read from half the schedule's rate; modifier-25 visits beside a same-day preventive
  visit carry the full rate. Hazards: the place-of-service rules (hospital-based clinics and Pemberglen's telehealth at
  the facility rate, the schedules' own notes), the claim versions, Kesselcrest's cents, the roster's dates. Files and
  columns: the three claim feeds (code, modifier, place of service, rendering NPI, allowed, version), the fee schedule
  workbook, the roster, 5 files and 9 columns. Stops: the code on the claim (0 of 13), the full level-5 rate only (0
  of 13), the non-facility rate everywhere (2 or more moved), the golden.
- **Ask B, the care coordination fees the three payers paid under the Performance Standard for each practice's
  members, by coverage quarter of January to September 2026, on the March to October runs, to the cent (39
  figures).** H18 home: the trail from an input the network books, through device rows the call never reads, to each
  practice's fee income for the year. User: the network's finance office, which passes the fees to the practices by
  quarter. Primary device (silent, D8 a posting date for the event date): Pemberglen's payment file posts every line
  to the period of the run that paid it, and the month a line covers is only in its payment reference; on a member's
  first run the catch-up lines for the year's earlier months post to that run's period. Second device (silent, D5
  out-of-scope rows known only by structure): Kesselcrest remits its Medicare Advantage care coordination fee (USD 6.50
  a member month) to the same TINs on the same remittances, from January, with no program column; only the amount per
  member against the standard's USD 2.80, and the Medicare Advantage attribution file's member counts, show which lines
  they are. Hazards: Merrinlake's retro lines, Kesselcrest's workbook, TINs with and without a hyphen. Files and
  columns: the three remittance files (period or coverage month, payment date, reference, TIN, members, amount), the
  standard, the roster, 5 files and 10 columns. Stops: every line as posted with Pemberglen by its period (0 of 39),
  Pemberglen's reference read with every Kesselcrest line kept (6 of 39, the two paediatric practices), the standard's
  fees alone with Pemberglen by its period (0 of 39), the golden.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | counts each practice's 99215 lines over its 99211 to 99215 lines at their current version, by the clinician's practice on the date | miss |
| B | sums each remittance line into the quarter of its coverage month, Pemberglen's by its period, every Kesselcrest line kept | miss |

Measured partial handlings on the cut pack: the best single-device handling keeps 6 of 52 figures (11.5 per cent of ask
weight); a response that finds both of ask B's devices keeps its 39, one that finds both of ask A's its 13.

Pair ceiling: 28.5 (the cracker 38 + 7 with none of 52 ask figures, the mirror 5 + 7 with none).

Mirror leakage: 0.0 per cent of ask weight (the mirror reads both asks as the cracker does).

Measured by: generator/ceiling.py on the cut pack.

## Leak sweep lines

leak.py on the final pack (`--asof 2026-10-16`): REVIEW, no LEAK.
- Sweep 3, answer figures: a few of the 270,000 claim lines in Merrinlake's and Pemberglen's feeds carry an allowed amount
  equal to a benchmark or threshold to the cent (pharmacy fills, outpatient and procedure lines); coincidences among
  allowed amounts, each line a claim like its neighbours and tied to no practice's measure. Harmless.
- Sweep 3, the payers' 2025 statements carry 16 of the call's 18 distinctive words: the words are the practices' names,
  which every statement lists; the statements state each payer's own 2025 settlement and no 2026 figure. Harmless.
- Sweep 4, the field guide, the standard and the statements carry 3 or 4 of the stump paragraph's 25 terms (interim,
  claims, attributed, months, records, family): the vocabulary of any payer feed pack; no shipped text names the run-out
  or a late-attributed member (checks.py, documents). Harmless; the readers' question 1 tests it.
- Sweep 6, the Kesselcrest attribution workbook, its Medicare Advantage attribution, the roster, the quality composite and
  the statements name the practices beside numbers: member lists, a clinician roster, 2025 quality measures and 2025
  settlements; none ranks the practices on the 2027 elections. Harmless.
- Sweep 9, dates after the setting: clean.

## Pre-ship check

The 10/10 rules re-read against the built pack. Rule 1: the deciding quantity is each practice's 2026 cost of care per
attributed member month on the payers' final 2026 attribution, which no file holds in October, estimated the way a
value-based contracting analyst projects a performance year from an interim run: the interim measure completed by the
payers' factors and carried by the practice's own 2025 run-out at the same cut, the 2025 attribution re-run from the
2025 professional claims (113,023 qualifying lines, 19,867 members at 31 August and 30 September 2025). Swapping the
method moves one to six elections (the interim measure as it stands and the final members' seasonality six, the short
counts as members who cost nothing one, one pooled run-out four). Rule 2: Layer 1 is the feeds' own mess (Merrinlake's
voids and replacements, Kesselcrest's adjusted lines, cents and pipe-delimited layout, Pemberglen's versions and posting
periods, three date formats, hyphenated TINs, clinicians who changed practice, open coverage spans), each mishandled
alone leaving the call (checks.py R2), and cleaning all of it leaves the default path at Ostrelwood, Thornelfield and
Jesselford; Layer 2 is the projection, which no cleaning performs. Rule 3: nothing planted (the October runs are the
payers' interim runs as issued, the 2025 statements report 2025 settlements), no field reading decides (checks.py R3a
runs the easy route on the clean truth with every filed rule applied and files the default three), and no stated rule
performs the re-run (section 2 defines the attribution and section 4.1 the interim measure; no clause asks for a 2025
run at the October cut). The analyst test executes in checks.py R3a and R3b; the standing family files the golden nine,
its 32-construction cross product at a worst margin of 3.9 per cent and the proxy construction at 2.1; the asks read
no projection.

## Architecture 13 record (spent 2026-10-25)

Architecture 13 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure on the payers' final 2026 attribution, projected from the October interim run by the practice's own
2025 run-out at the same cut, against the default path that takes the interim measure as the 2026 figure (Ostrelwood,
Thornelfield and Jesselford alone, against the golden nine). At stage 4 round 1 (zip ab79a5f44c18f637) both scored
readers landed the call (exit 1): each read the prompt's "projected to the payers' final 2026 attribution" beside the
standard's attribution rules as a population the October run cannot hold, re-ran the October 2025 interim run on the
2025 claims with the standard's own rules and the Appendix C factors, and carried each practice's interim measure by
its own 2025 final-to-interim ratio. Reader A kept all 78 ask figures (Kesselcrest's reviewed 99215 visits at the
99214 rate out of level 5, Merrinlake's halved modifier-25 visits counted by their code, Pemberglen's coverage month
from its payment reference, Kesselcrest's Medicare Advantage lines at 6.50 out); reader B kept every benchmark,
threshold and ask B figure and no ask A figure. The judge thread was stopped at the spend. Asked to project an interim
figure to a final one, a careful reader takes last year's interim-to-final ratio, the field's completion reflex, and a
standard whose rules can be re-run on last year's claims hands it that ratio in one pass.

## Architecture 12 record (spent 2026-10-24)

Architecture 12 certified the Quillmere Lake basin's 2027 Seasonal Communities Aid: each city's average population
present in its busiest month of the measurement year read from its plant's influent BOD load divided by the load per
person its own January to April 2026 fix, against the default path that counts residents plus the paid stays the fee
returns and both platforms record (Sorrelton and Esker Narrows alone, USD 1,200,000 each, against the golden's five
cities at USD 480,000 each). At stage 4 round 1 (zip be45d7b75ea5cc24) both scored readers landed the call (exit 1):
each read the Act's "every other person staying in or visiting the city" as a population no record holds, went to the
one file that measures everyone (the plants' influent), divided the load by 0.17 lb a person a day (the population
equivalent the world had been tuned to agree with), checked it against the residents in winter and filed the five
cities; both also counted Kettle & Pine's nights back from the departure in its reference (reader A all 32 of ask A,
reader B 26 of 32 on half-dollar rounding) and missed only the pond systems' flow basis in ask B. The judge thread was
stopped at the spend. A statute that defines the population as everyone present, beside records that plainly hold
only the paid stays, sends a careful reader looking for a measure of everyone, and a pack whose influent rows have
no other use hands it one.

## Architecture 11 record (spent 2026-10-24)

Architecture 11 settled Lumenfold Learning's 2025-26 outcomes guarantee district by district, each partner district's
share of eligible students at or above Proficient on a matrix-sampled spring science assessment re-estimated from its
students' own two-module answers with the district in the population model, against the default path that averages
the contractor's five plausible values by district (19 districts owed USD 32,045.00 against the golden's 16 owed
USD 25,493.75). At stage 4 round 1 both scored readers missed the call, reader A kept all of ask A through the
catalog's hours per session, and the judge's pass 1 returned FIX_NOW on a cent tie in the credits (seat prices moved to
whole half dollars). In round 2 reader C refitted the 2PL latent regression from the item responses with district in
the conditioning model, validated it on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75 and
kept every ask figure: a conditioning model that leaves out the grouping variable is a reflex for a reader who knows
plausible values, so the architecture was spent.

## Architecture 10 record (spent 2026-10-24)

Architecture 10 accrued each Medicare hospice provider number's FY2026 aggregate cap repayment at the December 2026
close, each beneficiary counted under the proportional method on the days to come from their state at the close (an
open stay by its length so far, a live discharge by its time out, returns read at every hospice from the benefit
periods extract), against the default path that runs the open stays on and takes the live discharges as finished
(Fallowmere USD 0.3 million against nothing). At stage 4 all four isolated readers across two rounds missed the call
and the round 1 judge returned DETERMINISTIC, APPROVE; the round 2 judge returned NOT_DETERMINISTIC, SEND_BACK
(margin_or_boundary_fragility and competing_defensible_answer): the printed 0.3 needed Fallowmere's count inside a
window of 2.9 beneficiaries while independent builds of the projection scattered about a beneficiary either way, and
the pool start, the number of later elections and the Kaplan-Meier tail were left unfiled (0.248 to 0.447 on the
judge's variants); ask A's routine-paid days read as an unstated rule. A designation set would have held (every variant
put Fallowmere above its cap); a figure printed to USD 0.1 million on a three-beneficiary window did not.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.
- v10 stage 2, 2026-10-24: a lifetime projection with Brackwater, Lindmoor and Wexmoor owing beside Fallowmere: the
  standing family (Aalen-Johansen or empirical return chances, three valuations of a return, the open stays' later
  returns overall or from their time so far) moves each core program's cap by USD 30,000 to 70,000 against cells of
  USD 100,000, and the overall-rate route kept three of the four amounts; the core programs were placed under the cap
  and Fallowmere carries the call alone (nothing accrued on the default path, USD 0.3 million on the golden).
- v10 stage 2, 2026-10-24: pooled models across provider numbers and a split by discharge reason each moved
  Fallowmere's count by up to 1.3 per cent on cells of small programs; the policy files the reference class (the same
  provider number and diagnosis group), and Fallowmere's seller's system records no revocation against discharge
  reason, so the reason split is not available for its history.
- v10 stage 2, 2026-10-24: with return stays as long as first stays the overall rate times the census average landed
  the golden's cell (0.325 against 0.300); re-elections run shorter (the beneficiary comes back in decline) and seldom
  end alive again, so that route files 0.53 and the census-average valuation by time out 0.19.
- v10 stage 2, 2026-10-24: the outside share of Fallowmere's returns was raised from a third to four in five, so the
  route that reads returns from Elderglen's own records files nothing (cap ratio 0.971) instead of landing beside the
  golden.
- v10 stage 3, 2026-10-24: the organisation and program names Elderglen, Brackwater, Corrinbrook, Dunsmere, Lindmoor,
  Pennacott, Sallowfield and Wexmoor sat within two edits of real places in the GeoNames register (Eden Glen,
  Blackwater, Swallowfield and Fallowfield, Dunmore and Dinsmore, Wyndmoor, Dixmoor) or carried a place word (Penna,
  and Cornbrook in Manchester two edits from Corrinbrook); renamed Wendleglen, Brindlemoor, Corvelfield, Darrelbrook,
  Marrellford, Rennickdale, Varrowmere and Farrinridge in the generator, every figure unchanged. The lines above keep the
  names they were written with.
- v10 stage 4 round 1, 2026-10-24: both scored readers missed the call (each ran the open stays on and took the
  live discharges as finished, nothing accrued) and the judge returned DETERMINISTIC, APPROVE (Gate G analytical, Gate H
  pass); reader A joined the claim lines to the remittance register and kept all 24 ask A figures (exit 1), so the
  device that the latest version is not the paid one sat off the careful path. Re-sited: the contractor's prepayment
  review pays some held inpatient days at the routine rate, visible only by repricing the paid version, with the
  returned replacements kept as a hazard and moved more than 118 days before the close (reader B had priced them as
  pending, cutting payments); the census report's length-of-stay table, blank on a group key mismatch, now prints.
- v10 stage 4 round 2, 2026-10-24, architecture spent: both fresh scored readers again missed the call (open stays
  run on, live discharges finished, nothing accrued) and kept 0 of 24 ask figures, but the judge thread returned
  NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, competing_defensible_answer): Fallowmere's printed 0.3
  needs its count inside 177.6 to 180.5, a window of 2.9 beneficiaries (USD 0.1 million at the cap amount and 98 per
  cent), while independent builds of the same projection scatter about a beneficiary either way (0.248 to 0.311 on the
  judge's variants, 0.279 to 0.314 on the standing family), and it named four choices the policy leaves open (the
  Kaplan-Meier tail, one later election or several, stays begun before 1 October 2016, the last provider number when the
  open stay is at another hospice); it also read ask A's routine-paid days as an unstated counting rule. Lesson: a cap
  repayment printed to USD 0.1 million moves a cell every 2.9 beneficiaries of count, so a projection whose honest
  spread is a beneficiary cannot print one cell; the next architecture's call has to be a quantity whose cell is wider
  than its estimator family's spread, measured on independent builds rather than on the author's own family.
- 2026-10-24, architecture 11 draw, screened on paper before any code against v10's lesson (a call whose cell is wider
  than its estimators' measured spread): Medicare Advantage post-payment recoupments or denial overturns for a
  hospital's 2027 contract notices carry v10's latent structure (a terminal-looking state that is not final) and
  task451's (amounts still to arrive).
- Architecture 11 draw: Medicaid procedural reinstatements and COBRA retroactive elections: retroactive eligibility was
  screened at task451 and task479 v5, and COBRA's selection is population_selection, banned against task275.
- Architecture 11 draw: ACA risk adjustment transfers estimated from competitors' public prior-year transfers: carrying
  a competitor's risk forward is a fork; ACA grace-period cures: rule-heavy, with the cure rate carried across the 2026
  subsidy expiry.
- Architecture 11 draw: censored transplant costs by inverse probability of censoring weights: mature cohorts are
  unbiased without a trend, and a trend makes the stump a dated step; authorization- or ADT-based claims reserves: the
  completion family, and a leading indicator is a reflex.
- Architecture 11 draw: price-standardised total cost of care tiers: the standardisation is a WHAT (filed is rule
  application, unfiled a fork); deductible leveraging is task479 v3's driver; prescription abandonment by out-of-pocket
  cost: the lever is too small; stop-loss and high-cost claimant pooling: non-linear aggregation at claimant level and
  level-dependent counts are closed.
- Architecture 11 draw: hospital coding intensity after an EHR conversion, separated by the same patients' successive
  admissions: adjacent to task453 (a measurement change read from a within-design contrast that nets a drift), the event
  study is the reflex and the WHAT signposts the method.
- Architecture 11 draw: low-voltage anode effect PFCs at aluminium potlines: task459's driver (a ratio with a fixed
  component carried across activity levels), and the IPCC slope method files it; wastewater digester relief-valve
  venting: v9's Gate G risk (an unmetered event inferred from indirect evidence); idle and shut-in wells: a setting clone
  of task462 and task450 v1; stack test-day tune-ups: population_selection and a surface read.
- Architecture 11 draw: a landfill's pre-record waste read from the volume survey: the gas collection record calibrates
  the decay model and absorbs the missing waste; refinery turnaround cycles: a schedule in a file is read; fuel switched
  during gas curtailments: a degree-day normalisation is the reflex.
- Architecture 11 draw: Fellegi-Sunter term-frequency weights: adjacent to task468 (false links on common
  identifiers); address agreement decaying with the gap between records: adjacent to task468 v1.
- Architecture 11 draw: majority-drifted or released anchors (v6, task450); rater severity drift on a shared
  constructed-response subset (task471 v2's driver); rapid guessing in a low-stakes sitting (task479 v4, sent back as
  cleaning contaminated data); speededness and not-reached items (an anchor-drift screen catches them).
- Architecture 11 draw: queue position for open appeals or a coding backlog against timely filing limits: the waiting
  time is a generic queue quantity, so the swap test fails and the domain is a backdrop; censored demand behind
  capacity is task18, task108 and task168; capture-recapture is task199, task243, task248 and task448.
- Architecture 11 draw: newborns and deliveries predicted from current pregnancies in an employer group's renewal: the
  base projection's credibility and trend choices fork, in a large group last year's deliveries already carry the
  component, and the honest strategy (who is in the 2027 population) is population_selection, banned against task275.
- Architecture 11 draw: race and ethnicity imputed from surname and geography for group counts: summing the
  probabilities is the reflex for counts, and the weighting-against-regression choice for rates needs a gold-standard
  subsample, banned against task275.
- Architecture 11 draw: the payroll survey's birth-death model against the lagged QCEW census is reserved for task484
  v2, and drawing it here through a house domain would game the survey x ETL ban against task483.
- Architecture 11 draw, first world: plausible values aggregated by school for a county school system's coaching list
  reskins task450's world and call (a district's own assessment naming the campuses below a share for coaching), so the
  mechanism moved to a company's guarantee settlement with its partner districts.
- Architecture 11 placement, benchmarks by prior tercile (12 to 20 for the lowest, up to 30 for the highest): no
  district the plausible values pull down could cross a benchmark it met, since the strong-implementation districts
  with weak backgrounds sit in the lowest tercile, so benchmarks became whole numbers from 12 to 35 per order form.
- Architecture 11 placement, a 5.5-point margin to the family's envelope with 2.5 points of crossing for every route:
  no maximum likelihood or curve-inversion count crossed anywhere, the routes' upward bias peaking near 9 points; the
  shipped margin is 4 points to the whole family's envelope with 1.5 to 3 points of crossing by route.
- Architecture 11 asks, a series' total on each row with series of up to 12 hours: the hours column summed put most
  districts at two to three times their contract, which reads as wrong at a glance; the series were cut to 3 and 4
  hours and the summer institute booked by day.
- Architecture 11 ask A, the offering's catalog hours on every session row (a series' total on each of its sessions):
  round 1's reader A set the series rows beside the catalog's hours per session and replaced them, keeping all 58 hours
  and 18 credits (exit 1); the catalog every reader opens for the live and recorded formats holds the tell one lookup
  away. Re-sited onto the session times the scheduler holds as hours and minutes after the point, every offering
  scheduled in whole hours so only the sessions that ran short or long carry minutes.
- Architecture 11, credits on quarter-dollar seat prices: a 15 per cent credit on a fee of 11,537.50 is 1,730.625, so the
  cent had a tie that no file breaks (judge pass 1, FIX_NOW); seat prices moved to whole half dollars, every credit a
  whole cent, the call's set unchanged.
Architecture 11 (the contractor's plausible values drawn from a conditioning model with no district term, each district re-estimated with the district in the model), spent at stage 4 round 2 on zip ce5456c3: reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, validated its fit on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75, and kept every ask figure (58 of 58 hours, 20 of 20 shortfall credits, 36 of 36 memo rows) by reading the hours field as hours and minutes from its fractions. A conditioning model that omits the grouping variable is a reflex for a reader who knows plausible values, so the round-3 PD re-site (series credit hours stacked on h.mm) is moot and the slot re-roots.
- 2026-10-24, architecture 12 draw: a Lunar New Year factory shutdown reaching a US East Coast port's container imports
  a Pacific or Cape crossing later, for its calendar-adjusted series: the decisive step is a lag and a window, the
  enumerable single choice the client's measured coin flips share, the effect is famous in trade data, and a port world
  would be this lane's third (task472, task474). Not drawn.
- 2026-10-24, architecture 12 draw: a state's payroll survey estimates early-benchmarked to the lagged unemployment
  insurance census where the birth-death model ran ahead in a slowdown: the two series count the same jobs side by side
  (architecture 8's reflex), the step is a choice between two files, and rejecting the published estimate for the census
  reads as a surface-read rejection at Gate G. Not drawn.
- 2026-10-24, architecture 12 draw: revisions measured from real-time vintages, or rebuilt pseudo-real-time by
  re-adjusting truncated spans: the client's pin makes the triangle rule application once the vintages ship, and the
  truncated re-adjustment forks between X-11 and STL end filters. A seasonal break from a school calendar moved to
  August: the post-break span is a window and the regime regressors are a reflex. Not drawn.
- 2026-10-24, architecture 12 draw: chain drift in a scanner-data price index (economics x ETL is undrawable, and the
  formula is one enumerable switch); suppressed county-industry cells rebuilt from their margins (identification is the
  step, so one linear solve is the easy route landing); custom-area margins of error from replicate tables against the
  approximation (the handbook licenses both, a fork at Gate C); register over-coverage by signs of life (every activity
  window is a threshold read as a fork). Not drawn.
- 2026-10-24, architecture 12 draw: the lake towns' population present also read from their transfer stations' scale
  tickets or their water meters: solid waste is collected on schedules that lag the stays, and summer water use carries
  the irrigation of empty cottages, so neither measures the people present as the sewer does; kept out of the pack.
- 2026-10-24, architecture 12 stage 4: the population present read through the plants' influent load per person,
  calibrated on the winter months; both round 1 readers landed the call at the 0.17 lb population equivalent (exit 1),
  because the Act's definition made the paid-stay records visibly incomplete and the influent rows had no other use in
  the pack. Spent.
- Architecture 13 draw (2026-10-24): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: Medicaid exposure developed through retroactive enrollment (task474 v4's capitation
  world, task451 and task479 v5's completion, and the recent months' dip shows on any monthly tabulation); linkage
  sensitivity by identifier stratum for linked mortality (a pooled clerical correction lands the stratified set on
  paper, and stratifying by the identifier is a reflex); three measurement systems combined by triple collocation
  (task228, landed); regression against equating in a score crosswalk (task464); payday counts by weekday schedule
  (task477); data fusion through a small joint source (task465); a prospective capitation priced on experience chosen
  the same way a period earlier (task130's lineage); business deaths confirmed after two years without reactivation
  (the standard's definition makes the adjustment a reflex); out-of-state births to residents arriving through the
  vital records exchange (a completion the place-of-occurrence field shows).
- 2026-10-24, architecture 13 stage 2: the October run's short counts read as members still to come who cost nothing
  (the interim measure scaled by the run's members over the 2025 final run's, or by the member months) filed the golden
  set with the practices as first placed, so a reader who saw the counts and assumed the rest landed the call without
  the 2025 re-run. Birrelhaven, the paediatric clinic whose late members cost nearly what its others cost (run-out
  0.944 on a 22 per cent short count), was placed 5.5 per cent over its threshold, where the zero-cost reading takes it
  12.8 per cent under.
- 2026-10-24, architecture 13 stage 2: asks with one device each (the code on the claim for ask A, Pemberglen's
  posting period for ask B) handed a whole ask to any response that found its device; each ask now carries a second,
  independent silent device (Merrinlake's halved modifier-25 visits; Kesselcrest's Medicare Advantage lines on the same
  remittances), and the best single-device handling keeps 6 of 52 figures.
- 2026-10-24, architecture 13 stage 2: the projected 2026 figure graded to the cent was dropped from the prompt's
  columns: the licensed constructions agree on every election but not on the cents (per payer against per practice
  moves a projection by up to 0.6 per cent), so the workbook carries the projection as context and the rubric grades
  the benchmarks, thresholds and elections.
- 2026-10-25, architecture 13 (each practice's interim measure carried to the payers' final attribution by its own
  2025 run-out at the same cut), spent at stage 4: both scored readers re-ran the October 2025 interim run from the
  2025 claims and landed the call, reader A with all 78 ask figures; a projection from an interim run to a final one
  whose prior-year ratio the standard's own rules rebuild is the completion reflex, and the second ask devices (the
  halved modifier-25 visits, the Medicare Advantage lines at another rate) fell to a reader who checked only the payer
  whose rates looked wrong and the one fee that did not match the standard.
