# task309: which county gets the 2027 roof-retrofit grant round, and the hurricane loss it removes there

Wave 7, Opportunity Sizing & Decision Support. Architecture 1, drawn 2026-10-27. Seed OS11 (an express-lane conversion
under a toll cap) is spent: task308 tried its corridor world and task307 holds road networks, so the build keeps only
the seed's decision form (which of N gets one scarce programme, sized as an annual sum) and moves to a pairing and a task
type never drawn, actuarial-science-insurance / catastrophe-exposure-accumulation. No probe, reader or solver was run
(the STOP rule); the stump is argued on paper below.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | actuarial-science-insurance / catastrophe-exposure-accumulation (serves Opportunity Sizing) |
| Objective | Opportunity Sizing & Decision Support: the headline is the 2027 expected hurricane loss the round removes, sized from the pool (each county's modelled annual loss on its eligible homes) to the realisable (the part a FORTIFIED re-roof takes off it, event by event), and the largest figure picks the county |
| Decision / answer unit / question form | pick_one_of_n / named_option with a USD figure / which |
| Shape | 01, a ranked list of the four counties (each county's annual loss and loss removed, the call, the runner-up and the gap) |
| Gap / pattern / generators | rule, population / none / G6 (composition), G14 (conditioned yield) |
| Gate G / strategy | method_or_model_selection / composition_mix: the cut the retrofit gives depends on the event's local gust, and the record's exposure and each county's annual loss sit in different parts of the gust range |
| Layer 2 | estimation_fit, own:a-mitigations-loss-reduction-falls-with-local-gust |
| Forum / forcing event / org family | board_of_directors (Sandpiper's board, January 2027 meeting) / season_or_peak (re-roofs finished before the 1 June 2027 start of the hurricane season) / financial_institution |
| Stakeholder | Sherry Lang, Catastrophe Risk Manager (portfolio_manager) |
| People (guard.py names --geo "United States" --seed 309) | Sherry Lang; Andrew Mack, Claims Director (the storm close-out summaries); Eric Brown, Chief Risk Officer (the model-governance standard) |
| World | Sandpiper Mutual Insurance Company, a mutual homeowners insurer on a fictional US Gulf Coast; USD; records to 30 September 2026, board paper November 2026 |
| Deliverables | retrofit_round_2027.xlsx (the county workbook), avoided_loss_by_county.png (the chart for the board pack), board_note_retrofit_2027.docx (the one-page note) |
| Guard | WARN only: repeat.gate_g against task270, repeat.question_form against task139 and task270, people.first |

The WARNs, answered: the decisive move is a choice between a one-ratio model and an intensity-conditioned one that a
filed criterion and the claims settle, so method_or_model_selection is the honest Gate G; the board picks one county,
so the question is which. The axes redrawn at the check: the decisive generator from G14 to G6 (G14 is task308's
pattern, inside the ban window), the decisive gap from population to rule after (population, G6, pick_one_of_n) repeated
task144's lineage inside the batch (the company's model-governance standard is a filed criterion the claims settle,
C2), and the context artifact from filed_model (task307) to close_out_summary, the claims department's per-storm
close-out summaries, which are the catastrophe risk manager's own file; the vendor's event set is an input.

### Candidates written before the choice (each with its default path)

1. **Survey boost inside existing clusters** (survey-research-official-statistics / sample-design-allocation-weighting x
   OS: which region gets a labour force survey boost, sized as local-area estimates made publishable). Default: scale
   each published CV by the root of the sample ratio, the region with most near-threshold areas. Dropped: the design
   effect under a larger take per cluster is Kish's textbook formula, small-area shrinkage is on file as a reflex the
   opponent applies unprompted (task253), and the boost specification that the estimand needs names the clusters.
2. **Deprescribing review where risk concentrates after initiation** (pharmacology / benefit-risk-assessment x OS: which
   drug class gets a falls-prevention medication review). Default: pooled excess fall rate over all exposed time times
   current users. Dropped: the natural prevalent-user cohort from a snapshot date lands the golden without any insight,
   and confounding by indication forks the estimand.
3. **Currency hedge on a fund's foreign sleeves** (quantitative-finance / portfolio-construction-risk x OS). Default:
   hedge the most volatile currency exposure. Dropped: the value turns on the currency's co-movement with the fund's bad
   states, task308's driver.
4. **Volume-weighted conjoint launch** (marketing-consumer-research / conjoint-choice-willingness-to-pay-analysis x OS).
   Default: share of preference times category units. Dropped: weighting a simulator by volume or distribution is
   practice (task174's screen), and task301's conjoint probe fitted latent classes unprompted.
5. **Retention of retrofitted homes** (this world, the round valued on homes still on Sandpiper's book in the season).
   Default: loss removed on every retrofitted home. Dropped: whether the round's value counts homes that leave the book is
   a reading of the estimand, a semantic fork, never a stump.
6. **The retrofit's cut read class by class of local gust (chosen).** Default: one cut ratio over the record's storms
   times each county's modelled annual loss names Marlin Shoals; golden Cypress Ridge.

The data-native sentence: the company's storm record holds its FORTIFIED homes mostly in gusts under 130 mph, where a
sealed roof deck keeps the cover on and the paid loss per insured dollar falls by about three fifths, and only a few
majors put them above 130 mph, where the structure fails with or without the roof and the fall is under a tenth; one
ratio over the record therefore averages a large cut over most of the exposure with a small cut over most of the loss,
and the vendor's 2027 event set puts Marlin Shoals' annual loss almost wholly above 130 mph and Cypress Ridge's almost
wholly below.

## Default path

The strong analyst's route, every field read correctly and every filed rule applied (final pack, world seed 309):
1. Takes the named storms since 2012 from named_storm_register_2008-2025.csv and sums every payment line coded to each
   storm in claims_payment_lines_2012-01_to_2026-09.csv (indemnity, supplements, recoveries), by ZIP code and by the
   FORT-R credit, against Coverage A at landfall from inforce_at_landfall_by_zip_2008-2025.parquet (USD thousands
   before 2019).
2. Measures the FORTIFIED Roof's cut as one ratio: one minus the FORTIFIED homes' paid per dollar of Coverage A over
   the standard homes', over all the storms (0.106 pooled; 0.29 when each FORTIFIED home is set against the standard
   homes of its own ZIP and storm).
3. Joins the vendor's event loss table to its hazard summary, takes each county portfolio's 2027 annual expected loss
   (Marlin Shoals USD 10.12 million, Heron Bay 5.65, Cypress Ridge 4.38, Calloway Flats 0.51) and applies the one cut
   to every event.
4. Files the largest loss removed: Marlin Shoals, USD 1.07 million a year (2.92 on the ZIP-matched ratio), Heron Bay
   next; any single cut ranks the counties by their annual loss.
Ends on: Marlin Shoals, about USD 1.1 million a year of expected loss removed (1.07).
Golden: Cypress Ridge, USD 2.8 million a year removed (2.80), Marlin Shoals next at 2.08.

## Stump sentence

A competent analyst measures the FORTIFIED Roof's cut in paid loss per dollar insured as one ratio over the company's
storms since 2012, applies it to each county's 2027 annual expected loss and files Marlin Shoals at about USD 1.1
million a year (1.07), the county with the largest annual loss; the step that lands it there is carrying one cut to
every vendor event when the cut is about three fifths in the gust classes under 130 mph and under a tenth above, which
MG-04's storm-by-storm reproduction rejects (the one ratio misses Kendra by 72, Marisol by 46 and Odile by 136 per
cent), so that Marlin Shoals, whose annual loss sits 81 per cent in events gusting 130 mph or more, gets a cut its
events do not give, and Cypress Ridge, with 1 per cent there, is the county where the round removes the most (USD 2.8
million).

## Three rules

Task type: actuarial-science-insurance / catastrophe-exposure-accumulation, which serves Opportunity Sizing: a catastrophe team sizing, from a vendor's event set, where a mitigation round removes the most expected annual loss.
Domain test: the deciding quantity is the expected annual loss a mitigation removes from a portfolio, computed event by event over the vendor's stochastic set at each event's annual rate, the event's local wind intensity deciding how much the mitigation cuts its loss, as hurricane models carry mitigation credits through a vulnerability function of gust; swap the nouns into another field and the event set, the gust classes, the named-storm deductible and the wind engineering of a sealed roof deck all stop making sense.
Swap: "which hospital ward should get the falls-prevention programme, sized as falls avoided" keeps a pick and an effect size, but the object that decides, a roof's cut in paid loss that holds below the design gust and collapses above it, carried through a vendor's events at their local gust, has no ward equivalent.
Layer 1: the company's own systems produce every mess item: footprints issued in knots before 2019 under a title block, Coverage A in USD thousands in the older in-force extracts, supplements filed under suffixed claim numbers and recoveries as negative lines, storm codes in the claims system against storm names in the footprint workbook, vendor event ids written two ways, legacy valuations dated month first; none decides the call (each asserted not to move it: indemnity only, the 1.15 knot factor and the Poisson form all keep Cypress Ridge at 2.8).
Layer 2: estimation_fit, the mitigation's cut read class by class of the event's local gust from the company's claims and carried event by event through the vendor's set, where one cut over the record averages a large cut over most of the exposure with a small cut over most of the loss.
Decisive step: conditioning the FORTIFIED cut on each event's peak-gust class, read from the paid loss of FORTIFIED and standard homes in the same gust class, instead of carrying one cut measured over all the storms.
Not semantics: every field read correctly (FORT-R is the FORTIFIED credit, the gust is the ZIP's peak 3-second gust, the hazard class is the event's gust at the portfolio) still leaves the easy route on Marlin Shoals, because nothing in the pack says the cut varies with the gust: it is an estimate the analyst has to make from the claims, class by class.
Not rule application: no filed rule computes the cut; MG-04 files what an adjustment is and the test it has to pass, and leaves the adjustment to the analysis. Measured on the final pack: every single cut (pooled 0.106, ZIP-matched 0.29) fails the test on three of five storms (worst 136 per cent) and files Marlin Shoals at 1.07 to 2.92; two classes at 130 mph fail it (13.0 per cent on Odile) and 20 mph classes fail it (26.4 per cent); the 10 mph class cuts, pooled or ZIP-matched, pass it (worst 3.8 and 1.7 per cent) and both file Cypress Ridge at 2.80 and 2.77, the same printed 2.8.
Analyst test: a strong analyst who resolves the claims' supplements and recoveries, converts the older footprints from knots and the older extracts from thousands and joins the vendor's tables measures the FORTIFIED cut as one ratio across the storms, applies it to each county's annual loss and names Marlin Shoals at about USD 1.1 million a year (1.07), while the cut read by gust class, which MG-04's test accepts and the one ratio fails, puts Cypress Ridge first at USD 2.8 million.
Estimand: the board brief (retrofit_grant_round_2027_board_brief.pdf, sections 1 to 3) files the population (the county's 1,500-home portfolio, every home re-roofed before the 2027 season), the outcome (the portfolio's 2027 annual expected loss under Corvane HU 27.1 as modelled, less the same with every home carrying a FORTIFIED Roof, gross of reinsurance after the deductible), the window (2027, annual), the unit (USD a year, expected) and the comparison (the vendor's event losses adjusted for the roof's effect as the company's own named-storm claims show it, an adjustment meeting MG-04); MG-04 (sections 2 to 4) files what an adjustment is, the reproduction test, its storms (from 2012, at least USD 10 million paid on homes with the feature), its tolerance (10 per cent) and its definitions.
No decoy: nothing is planted to be caught: no memo, figure or stakeholder argues for a county, no file ranks the counties on the loss removed, the vendor's note says only what was modelled, and the close-out summaries report storm totals, never a cut or a county.
No certified replay: no published or certified figure in the pack reproduces either method; MG-04's test is a filed criterion the claims settle, a single cut failing it on three storms and the class cuts passing all five.
Lesson: a mitigation's measured effect is an average over the intensities the record happened to hold, and a forward event set weights those intensities differently, so the effect is carried event by event at the event's own intensity; no build on file teaches a mitigation credit read through a vulnerability curve of gust (task308's architecture 2 re-costed claims at a repair panel's load; task301's first architecture read a deposit falling with distance).

## Readability screen

| Rung | What it needs | Verdict |
|---|---|---|
| storm claims coded since 2012, net of recoveries | MG-04 section 4, the claims file | readable |
| Coverage A at landfall in USD | the in-force extract's coverage_unit column | readable |
| gust per ZIP in mph | the footprint sheets' headers (kt before 2019) | readable |
| the board's measure: annual expected loss removed under the vendor set | board brief section 3 | readable |
| an adjustment must reproduce each qualifying storm within 10 per cent | MG-04 section 3 | readable |
| the cut read class by class of local gust and carried to each event's class (decisive) | no sentence; the paid loss of FORTIFIED and standard homes by gust class in the claims and the in-force extract | silent |

## Ladder

| Rung | Construction | Marlin Shoals | Heron Bay | Calloway Flats | Cypress Ridge | Call |
|---|---|---|---|---|---|---|
| R0 | the pool: 2027 annual expected loss, standard roofs | 10.12 | 5.65 | 0.51 | 4.38 | Marlin Shoals |
| R1 | the default path: one cut over all storms, pooled (0.106) | 1.07 | 0.60 | 0.05 | 0.46 | Marlin Shoals |
| R2 | one cut, each FORTIFIED home against its own ZIP and storm (0.29) | 2.92 | 1.63 | 0.15 | 1.26 | Marlin Shoals |
| R3 | two classes split at 130 mph (fails MG-04 on Odile) | 1.60 | 1.37 | 0.30 | 2.55 | Cypress Ridge |
| R4 | 20 mph classes (fails MG-04, 26.4 per cent) | 2.34 | 1.77 | 0.32 | 2.85 | Cypress Ridge |
| R5 | the golden: 10 mph classes, pooled | 2.08 | 1.66 | 0.34 | 2.80 | Cypress Ridge |
| R5' | 10 mph classes, ZIP-matched | 2.10 | 1.66 | 0.34 | 2.77 | Cypress Ridge |

USD million a year. R1 is the stump and R2 the closest repair that misses (it removes the location mix and keeps one
cut). R3 and R4 name Cypress Ridge but print other figures and fail MG-04, which is what selects R5 (C2). Every rung is
asserted in checks.py. On the call's own figure the decisive step is worth about 24 bins of 0.1 million (Cypress
Ridge at 0.46 on R1 against 2.80 on R5), the two passing constructions differ by 0.35 of a bin (2.80 against 2.77) and
both sit 0.018 or more from the 2.75 and 2.85 edges.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | expected annual hurricane loss the round removes | annual expected loss on standard roofs less with every home FORTIFIED, under the vendor's set | a cut in a return-period loss, or several years summed | another quantity | board brief section 3 |
| SF2 | the county's portfolio | the 1,500 homes listed and modelled | every insured home in the county | another pool | board brief section 2; the ELT exposed value equals the list's Coverage A (asserted) |
| SF3 | loss basis | gross of reinsurance, after the named-storm deductible, as paid | ground-up | same call | vendor note section 2; MG-04 section 4 (paid loss) |
| SF4 | the storms the cut comes from | named storms from 2012 | the legacy storms too | same call (no FORTIFIED home before 2012, asserted) | MG-04 section 4 |
| SF5 | paid loss | every payment line, supplements in, net of recoveries | indemnity lines only | same call (asserted) | MG-04 section 4 |
| SF6 | a FORTIFIED home | the FORT-R credit at the date of loss | any mitigation credit (SHUT) | another population | MG-04 section 4; the in-force extract's roof designation |
| SF7 | Coverage A before 2019 | USD thousands | dollars | another cut | the extract's coverage_unit column |
| SF8 | gust before 2019 | knots times 1.150779 | knots times 1.15 | same call, same 2.8 (asserted) | the footprint sheets' headers |
| SF9 | which event is which | HU27- prefix dropped, the same event number | unmatched events left out | same call (every row joins, asserted) | vendor note section 3 |
| SF10 | the class cut's pooling | pooled over the class's storms and ZIP codes | each FORTIFIED home against its own ZIP and storm | same call, same 2.8 (asserted) | both pass MG-04; converge |
| SF11 | annual expected loss | sum of rate times mean loss | one minus e to the minus rate, times loss | same call, same 2.8 (asserted) | vendor note section 2; converge |
| SF12 | the storms MG-04 tests | the five with USD 10 million or more paid on FORTIFIED homes | every storm since 2012 | same selection of adjustment | MG-04 section 3 |
| SF13 | a hazard class's gust | the class itself | its midpoint | same lookup (asserted) | the class table is by class |
| SF14 | rounding | loss removed to USD 0.1 million, the rest to 0.01 | other paths | same figures, clear of edges (asserted) | the prompt's closing sentence |
| SF15 | the runner-up | second by loss removed | second by annual loss | Marlin Shoals either way | the prompt (the runner-up to the call) |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each county's 1,500 listed homes, none added or lost in 2027; FORTIFIED homes as credited at the date of loss | filed (brief section 2; MG-04 section 4) |
| 2 | Unit of account | USD a year of expected loss on the portfolio | filed (brief section 3) |
| 3 | Attribution window | the 2027 annual view; the storms from 2012 for the cut | filed (brief, MG-04) |
| 4 | As-of dating | claims to 30 September 2026; the vendor run of October 2026 | filed (file names, vendor note) |
| 5 | Version basis | Corvane HU 27.1 near-term view as delivered | filed |
| 6 | Denominator | Coverage A in force at landfall | filed (MG-04 section 4) |
| 7 | Weighting | events at their annual rates; the class cut pooled or ZIP-matched | C1 (SF10, asserted) |
| 8 | Window length | every storm from 2012 | filed (MG-04 section 4) |
| 9 | Boundary inclusivity | gust classes as the vendor reports them (120-129, 130-139); at MG-04's USD 10 million line five storms qualify, and at a USD 5 million line seven do, with the same verdicts (class cuts pass, every single cut and the two-class split fail) | C1 (asserted) |
| 10 | Rounding path | unrounded sums, rounded once at the end | the prompt |
| 11 | Tie-break | none: 2.80 against 2.08 | asserted |
| 12 | Maturity and censoring | the 2025 storm's claims still paying at 30 September 2026; Rosalind is outside MG-04's test and its paid moves no class cut's call | C1 (asserted on the call) |
| 13 | Order of operations | cut by class, then applied per event, then summed | WHAT filed (MG-04 section 2); the class cut is the analysis |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | supplements under suffixed numbers summed with the claim; no exact duplicates | C1 (the call sums lines) |
| 16 | Identity normalisation | storm codes through the register; event ids with the prefix dropped | asserted (SF9) |
| 17 | Netting against gross | recoveries netted | filed (MG-04 section 4) |
| 18 | Dimensional units | knots and thousands in the older records | filed in the records (SF7, SF8) |
| 19 | Code and status semantics | FORT-R and SHUT credits; line types | filed (MG-04 section 4); never the stump |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | MG-04's test applies to every adjustment of vendor event losses | filed (MG-04 section 1) |
| 22 | Forward window contents | the vendor's event set is the 2027 window; no event outside the claims' gust range (the set's classes reach 160 to 169, the claims' FORTIFIED homes reach the same class) | asserted |

## Literal reader

Executing the prompt and every filed sentence word for word (the brief's sections 1 to 3, MG-04's sections 2 to 4, the
vendor note's sections 2 and 3) leaves one open move on the call: the form of the FORTIFIED adjustment. The estimand is
filed literally (the portfolio's annual expected loss less the same with every home FORTIFIED, under the vendor's set),
MG-04 files the test any adjustment must pass, and the claims settle it: every single cut fails on three of the five
storms, the 10 mph class cuts pass on all five, and every passing construction files Cypress Ridge at 2.8; the default
files Marlin Shoals at 1.1 by an easy method on the same literal estimand, never another reading of it.

## Oracles

None on the call: no file states a FORTIFIED cut, ranks the counties on loss removed or prints an annual loss. The
close-out summaries report each storm's claims and paid at its close-out, which the claims file reproduces up to the
payments made after the close-out (context, asserted only through the claims file's own sums). On the asks there is
no control total.

## Ask sheet

**Ask A: each candidate county's insured homes holding a valid FORTIFIED Roof certificate on September 30, 2026, and
their Coverage A (8 figures, homes and whole USD thousands).** H18: the FORTIFIED stock each candidate already
carries, a measure every county has that the call does not turn on (the call reads the claims' credit and the in-force
designation, never the certificate register; asserted). Use: the board and the reinsurers' February submission ask for
mitigation counts by county. Primary device, silent (D7, the true key elsewhere, and D2, an attribute at the wrong
vintage): a certificate stays with the building, so after a sale it sits on a policy number the master no longer holds
in force, and the register keeps the street name the building had when the certificate was issued, while four
counties renamed a street each between July 2022 and January 2024; only the parcel and the building (main house or
cottage) identify the home. Interior: about 3 per cent of parcels carry a second insured building with its own
certificate, so collapsing to one home per parcel over-repairs. Hazards: renewal certificates issued up to 60 days
before the old one expires (two valid on one home), certificates voided at audit on a separate row, parcel ids written
with and without dashes, addresses upper case with abbreviated street types. Files: fortified_certificate_register,
policy_master. Stops (homes, Marlin Shoals / Heron Bay / Calloway Flats / Cypress Ridge): joined on the policy issued
under 1,594 / 1,372 / 1,314 / 1,533; parcel and address as written 1,691 / 1,660 / 1,405 / 1,806 (the careful path);
one home per parcel 1,725 / 1,679 / 1,438 / 1,827; certificates counted, not homes 1,727 / 1,678 / 1,442 / 1,826;
voids ignored 1,726 / 1,678 / 1,439 / 1,842; golden 1,711 / 1,665 / 1,420 / 1,813.

**Ask B: for Corwin (2008), Della (2009) and Evander (2011), the company's net paid to date and the part of it paid
after 2011 (6 figures, whole USD thousands).** H18: the storm record before the FORTIFIED programme, outside the call's
storms from 2012 (asserted: no carried legacy line and no cut-over line sits in a 2012+ storm). Use: the paper's
storm history. Primary device, silent (D6/D1, the same money in two systems): a claim still open at the 2012 cut-over
was carried into the new system under a new number with its paid-to-date posted as its first line on January 1, 2012,
the same amount the legacy valuation already holds; only setting that line against the legacy paid to date shows it.
Hazards: legacy valuations are cumulative paid to date by quarter (summing them counts each payment many times), dates
month first, carried supplements under suffixed numbers, recoveries reducing the cumulative. Files:
legacy_claims_valuations, claims_payment_lines, named_storm_register. Stops (total / after 2011, USD thousands, Corwin,
Della, Evander): legacy paid to date plus every carried line 50,037 / 3,838, 10,734 / 513, 25,842 / 15,239 (the careful
path); the legacy valuations alone 46,199 / 0, 10,221 / 0, 10,602 / 0; golden 47,101 / 902, 10,486 / 265, 19,875 /
9,273.

**Ask C: each county's portfolio homes whose roof will be 15 or more years old on June 1, 2027, and their Coverage A
(8 figures, homes and whole USD thousands).** H18: how many of the round's homes have roofs at the end of their
life, a measure of each candidate's list the call does not read (the call reads the vendor's tables, never the list's
roof years or the permits; asserted). Use: the programme's case for re-roofing. Primary device, silent (D2, a label
stored before a silent switch): the roof year on the underwriting record is the one recorded when the policy was
written, and a re-roof since (after a storm or for age) shows only in the county permit portals; the portals keep the
street name a permit was issued under, so a re-roof on a street renamed since matches only by ZIP code and house number.
Interior: ROOF REPAIR permits leave the roof year alone; a BLDG 2 permit is the cottage's. Hazards: addresses upper
case with abbreviated street types, other trades in the same extract. Files: retrofit_2027_modeled_portfolios,
county_building_permits_roofing, policy_master. Stops (homes): the roof year on record 1,500 in every county; RE-ROOF
permits at the address as written 84 / 410 / 559 / 621 (the careful path); any roofing permit 45 / 236 / 303 / 387;
golden 77 / 382 / 520 / 610.

Main population zero-counts: the call reads the claims lines of the 2012+ storms, the in-force extract, the footprints,
the register and the vendor's two tables; the asks read the certificate register, the policy master, the legacy
valuations, the carried lines of the legacy storms, the portfolio list's roof years and the permits (asserted in
checks.py: no carried legacy line or cut-over line in a 2012+ storm).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A homes and Coverage A by county | 0 of 8 | miss |
| B paid to date and after 2011 by storm | 0 of 6 | miss |
| C old roofs and Coverage A by county | 0 of 8 | miss |

Pair ceiling: 28.5 ((45.0 + 12.0) / 2), the cracker keeping 0 of the 22 ask figures on the call and the mirror 0 on the
default path's call; the cracker's ask routes are this note's model of the careful path (address joins as written,
every carried line added, permits at the address as written), not a measurement of a reader.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Tried and rejected

- Candidates 1 to 5 above, at the draw (2026-10-27), each for the reason given on its line.
- The composition card as first drafted (gap population, G14 then G6 decisive): blocked by ban.pattern (G14, task308)
  and by test.same_puzzle against task144's lineage; redrawn with the company's model-governance standard as the filed
  criterion (gap rule) rather than relabelled.
- The vendor's own FORTIFIED loss column in the event table: dropped, it hands each event's cut over and leaves no
  analysis; the cut is read from the company's claims.
