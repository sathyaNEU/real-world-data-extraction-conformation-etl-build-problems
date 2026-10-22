# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 5, drawn 2026-10-22 after architectures 1
to 4 were spent at stage 4; architecture 4's world and pack are kept, its decisive step is not: the constant-quality
regression that landed architecture 4 is this architecture's default path.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v5, lineage v1 to v4 spent), registered
  2026-10-22 after a pull. Guard WARN only, answered here: `driver.near` (0.20 against this slot's v4, whose driver
  stops at the constant-quality regression this one starts from), `people.first` (Evelyn, a common first name; surname
  unused), `overuse.objective` (the lane), `repeat.gate_g` and `repeat.decision` (task273: a designation set chosen
  between two defensible methods; that build fits a load test, this one aggregates a stock), `repeat.question_form`
  (the circular designates areas, so the pick asks which).
- **Redrawn at the draw, and why the replacements are the honester labels.** The v4 identity carried over BLOCKed on
  own_lineage (gap objective, the same decisive pattern as v4), then gap population BLOCKed on same-puzzle and
  same-driver against task251 v5. The card now carries gap objective with pattern D: the pooled constant-quality change
  is a correct figure and not the stock's value change the designation is scored on, and the two grains (the traded
  mix and the stock's types) are each flawless. Shape 10 (task249 v6) became `other`, a designation over every
  candidate against one line with the transactions asked beside it. The context artifact filed_standard (task478 v4)
  became planning_thread, the Department's circular the Office answers. The forcing event vote_or_meeting, then
  statutory_or_regulatory_filing (task249 v6), became budget_or_appropriation, and the world changed to match: the
  circular now settles each designated area's allocation from the Housing Supply Act's 2027 infrastructure fund in a
  round that closes on 20 November. The strategy is composition_mix (the traded mix against the stock's).
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: the residential property price register in two layouts, the valuation register's dwelling attributes,
  the address point file's electoral divisions and the census dwelling stock conformed into one sales table, and each
  area's residential property price change built from it.
- **The decision and the quantity:** the Minister for Housing designates as rapid price growth areas for 2027 the
  local authority areas whose residential property price index, as the Brannagh Statistics Office measures it, rose by
  more than 8 per cent from the year to September 2025 to the year to September 2026; the methodology note files the
  index as the change in the market value of the area's dwelling stock, the dwellings the 2022 census counts there.
  Forward facing: the designation governs 2027 and its fund allocation.
- **Shape:** `other`: sixteen areas' changes to one decimal (16) and verdicts (16), the designated set (1), a chart's
  named parts (the sixteen bars, the 8 per cent line, the designated areas marked: 3), the workbook (1), and the ask's
  32 figures (each area's purchases and total paid): 69 criteria.
- **Strategy:** `composition_mix`; Gate G `method_or_model_selection` (the pooled year effect against each type's own
  year effect over the stock, the standard's estimand pinning the second); gap `objective`; pattern D; generators G6
  (the traded mix against the stock, decisive), G16, G17. Layer 2 family `estimand_identification`, pattern `own:a
  stock's value change taken from a regression on what traded, when the types' prices move apart and the traded mix
  over-represents one type against the stock`.
- **World:** a fictional Ireland-like state: the Brannagh Statistics Office, sixteen local authority areas, 69,527
  market sales in the two years. People from `guard.py names --geo ireland --seed 4824` and `--seed 4825`: Clare
  McEntee (Head of Price Statistics) and Evelyn Clune (Housing Supply Policy).
- **Forcing fact:** the Office sends its figures on 6 November 2026; the fund's 2027 allocation round closes on 20
  November.
- **Forum and forcing event:** minister_or_cabinet, budget_or_appropriation. Organisation research_or_statistics_office;
  role statistical_office_head.
- **Data-native sentence:** in Moyrath, Carrigvore, Innishrue and Drumshallon apartments are 44 to 45 per cent of the
  sales against 12 to 14 per cent of the census stock, and their prices moved apart from the houses': in Moyrath and
  Carrigvore apartments rose 0.5 and 1.1 per cent while the houses rose about 10 to 13, in Innishrue and Drumshallon
  apartments rose about 17 while the houses rose 3 to 6; a regression with one year term averages the types over what
  sold, while the stock the index prices is mostly houses.
- **The WHAT screen.** Population: each area's dwelling stock, the dwellings the 2022 census counts there, read
  through its sales at full market price (note sections 1 and 2). Outcome: the change in their market value. Window:
  the year to September 2026 on the year to September 2025, each year as a whole, by date of sale. Unit: each area.
  Comparison: more than 8 per cent (circular section 1). The decisive step settles none of them: it is how the stock's
  value change is estimated from the sales, which nothing files.
- **Sources, one line each:**
  - The client's official-statistics rigor patterns (a price index from a changing sample of transactions; weights
    from the population the index describes): here the hedonic time effect is estimated by type and the types are
    weighted by the stock's value.
  - Handbook on Residential Property Prices Indices (Eurostat, 2013), cited by the note: stratified and hedonic
    methods, stock weights; the note cites it without a method.
  - This slot's architecture 4 (a constant-quality regression with location) is the default path here.
- **Same-puzzle and same-driver tests:** (objective, D, designation_set) and (objective, D, method_or_model_selection)
  against the last twelve builds, lineage included: no match.
- **Abstraction test:** the nearest drivers stripped of nouns (this slot's v4, a change read from a shifting sample
  held fixed by a regression with location; task251 v5, a population chosen for an index) do not aggregate type-level
  effects to a stock whose mix differs from the traded mix.

## Default path

A strong analyst with every field read correctly:

1. Reads the circular: an area is designated when the Office's residential property price index for it rose by more
   than 8 per cent in the year to September 2026 on the year to September 2025; and the methodology note: the index
   measures the change in the market value of the area's dwelling stock, sales at full market price, by date of sale,
   new dwellings with VAT, compiled to the Handbook on Residential Property Prices Indices.
2. Conforms the two register extracts (day-first dates, euro text, VAT grossed up, the ten-day overlap counted once),
   joins the valuation register for type, floor area and newness and the address point file for the electoral
   division, and keeps the market sales of the two years.
3. Sees that what sold differs between the years by location, size and newness, so holds the dwelling fixed: one
   hedonic regression per area of log price on dwelling type, log floor area, new-dwelling status and electoral
   division, with a year term; the year term's change is the constant-quality change the Handbook describes.
4. Compares with 8 per cent.

**Ends on:** Ardcullen, Annaghvale, Dunmarra, Drumshallon, Glenaskin, Innishrue and Kilbrannagh designated

- On that path Carrigvore and Moyrath stand at 6.2 and 6.4 per cent and Drumshallon and Innishrue at 10.0 and 9.7; the
  same regression with monthly terms, and electoral division by type cells, file the same seven.

**Golden:** Ardcullen, Annaghvale, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh and Moyrath designated; the stock's
value changes are 9.5 to 12.0 per cent in the seven and 3.4 to 5.7 elsewhere.

## Stump sentence

The default path fits one hedonic regression of log price on dwelling type, floor area, new-dwelling status and the address point file's electoral division with a single year term for each area and designates Ardcullen, Annaghvale, Dunmarra, Drumshallon, Glenaskin, Innishrue and Kilbrannagh, because the one year term averages the types' changes over what sold: in Moyrath and Carrigvore apartments are 45 and 44 per cent of the sales against 14 per cent of the stock and rose 0.5 and 1.1 per cent while the houses rose about 10 to 13, and in Innishrue and Drumshallon the apartments rose about 17 per cent and the houses 3 to 6; each type's own year effect, weighted by the census stock's value of that type, designates Carrigvore (9.5) and Moyrath (10.4) in place of Drumshallon (5.6) and Innishrue (4.8).

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics): the residential property price register in two systems' layouts, the valuation register, the address point file and the census dwelling stock conformed into one table of sales with each dwelling's attributes and location, and each area's price change measured from it for the stock the census counts, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each area's residential property price change worked the way official property price statistics measure it from administrative sales: the sales are a changing sample of the dwelling stock, so each dwelling type's change is a hedonic time effect holding size, newness and location fixed, and the area's index aggregates the types with the stock's value weights (the Handbook on Residential Property Prices Indices); a single pooled time effect averages the types over what sold.

Swap: "which bakeries' loaf prices rose more than 8 per cent" keeps a price change and loses the step: a bakery's loaves are the same products in both years, nothing about which were bought changes what one costs, and there is no stock of loaves whose mix differs from what sold.

Layer 1: the old register layout's day-first dates and euro text prices, its new-dwelling prices exclusive of VAT, eircodes keyed in four styles or missing (joined by address), the new system's property numbers and VAT-inclusive consideration, the ten days of October 2025 filed in both systems, sales filed in one year for a sale in the other, out-of-window sales in both extracts, sales not at full market price, the location held only in the address point file and the stock only in the census workbook; each is how the producing systems write, nothing is placed to be caught, and checks.py asserts the call under them (SF1 to SF8).

Layer 2: estimand_identification, a stock's value change estimated from a sample of sales whose mix differs from the stock's: the choice that flips the call is estimating each dwelling type's own year effect, holding size, newness and electoral division fixed, and weighting the types by the census stock's value, instead of one pooled year term, summaries of what sold, or type medians weighted by the stock.

Decisive step: estimating each area's change as the stock-value-weighted average of the dwelling types' own year effects from a hedonic regression of log price on type, log floor area, new-dwelling status and electoral division with a year term per type, which puts Carrigvore and Moyrath at 9.5 and 10.4 per cent and Drumshallon and Innishrue at 5.6 and 4.8.

Not semantics: every field, code and definition read correctly (the two layouts, VAT, the market basis, the property numbers, the electoral divisions, the census stock, "the market value of the area's dwelling stock") still leaves the strong route on one pooled year term, because no field says the types' prices moved apart or that the sales over-represent a type; the step is the inference that the year effect differs by type and the aggregation to the stock it calls for, which the joined data show and no sentence says.

Not rule application: the circular and the methodology note fix the population (each area's census dwelling stock, read through its sales at full market price), the outcome (the change in market value), the window, the unit and the comparison, and no rule says how the stock's value change is estimated from the sales; executing every filed rule with the Handbook's constant-quality regression files the default path's seven.

Analyst test: a strong analyst who conforms every file, reads every rule and fits the constant-quality hedonic regression with the electoral division and one year term files Ardcullen, Annaghvale, Dunmarra, Drumshallon, Glenaskin, Innishrue and Kilbrannagh designated (the default path's Ends on); the median, the median per square metre, type medians weighted by the census stock and a regression without location each file another wrong set; only the types' own year effects weighted by the stock's value file the golden seven; checks.py runs them on the clean truth (R3a to R3d).

Estimand: the circular (dhlgh_circular_rapid_price_growth_areas_2026.pdf, section 1) and the methodology note (bso_rppi_methodology_note_2026.pdf, sections 1 and 2): the population (each local authority area's dwelling stock, the dwellings the 2022 census counts there, read through its sales at full market price), the outcome (the change in their market value), the window (the year to September 2026 on the year to September 2025, each year as a whole, by date of sale), the unit (each area) and the comparison (more than 8 per cent).

No decoy: nothing is planted: the register extracts, the valuation register, the address points, the electoral divisions and the census are the producing bodies' records, the note states the estimand without a method, and no earlier index, published change or ranking of the areas ships; the rents and mortgage files rank nothing on the value of the stock.

No certified replay: no certified or published index, change or coefficient ships; the method is not recovered by reproducing any figure.

Lesson: a constant-quality regression on what sold measures the change for the mix that sold; when the types' prices move apart and the sales are not the stock, the stock's value change takes each type's own time effect weighted by the stock's value, which a single pooled time term does not.

## Readability screen

| Rung | What takes the reader there | Verdict |
|---|---|---|
| Layer 1: layouts, VAT, overlap, eircodes, market basis | the dictionary, the note's sections 2 and 3 | readable |
| R0 the median change | the register extracts | readable |
| R1 the median per square metre | the valuation register's floor area | readable |
| R2 type medians weighted by the census stock | the census workbook beside the note's "the area's dwelling stock" | readable |
| R3 regression without location | the valuation register's attributes | readable |
| R4 (default path) one hedonic regression with the electoral division and one year term | the note's Handbook citation and the address point file | readable |
| G (decisive) each type's own year effect weighted by the stock's value | nothing: no sentence names a regression, a type effect, a mix or a weight | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | new-dwelling prices in the old layout | grossed up by 13.5 per cent | as filed | same call (asserted) | note section 3 |
| SF2 | the two systems' overlap | one record per sale | both kept | same call (none kept twice, asserted) | note section 3 |
| SF3 | the year | by date of sale | by filing | not filed alternatives | note section 2 |
| SF4 | which sales | at full market price | every sale | not filed alternatives | note section 2 |
| SF5 | the two years | each as a whole | the September months | not filed alternatives | note section 1 |
| SF6 | the form of the types' time effects and their weights | a year term per type in one log regression, the stock's value weights | separate regressions by type, second-hand only, with year built, the stock's counts as weights | same call (C2, C3) | the data |
| SF7 | more than 8 per cent | strictly over, on the change to one decimal | at or over | same call (asserted) | circular section 1 |
| SF8 | the printed change | the unrounded change rounded once | rounded first | same call (asserted) | prompt |

## Ladder

Built values from the cut pack (generator/checks.py L1 and L2, C1 to C4), per cent.

| Rung | Route | Designated | Carrigvore, Moyrath / Drumshallon, Innishrue |
|---|---|---|---|
| R0 | median sale price | Annaghvale, Ballymarne, Carrigvore, Drumshallon, Glenaskin, Kilbrannagh, Moyrath, Rathgowan | 8.3, 8.4 / 9.6, 6.2 |
| R1 | median per square metre | Annaghvale, Ballymarne, Drumshallon, Glenaskin, Innishrue, Kilbrannagh, Rathgowan | 5.7, 5.9 / 9.3, 9.4 |
| R2 | type medians weighted by the census stock | Annaghvale, Ballymarne, Carrigvore, Glenaskin, Kilbrannagh, Moyrath, Rathgowan | 9.8, 11.2 / 7.2, 7.1 |
| R3 | regression without location | Annaghvale, Ballymarne, Drumshallon, Glenaskin, Innishrue, Kilbrannagh, Rathgowan | 5.9, 6.2 / 10.0, 10.3 |
| R4 (default path) | one regression with the electoral division, one year term | Ardcullen, Annaghvale, Dunmarra, Drumshallon, Glenaskin, Innishrue, Kilbrannagh | 6.2, 6.4 / 10.0, 9.7 |
| R4b | the same with monthly terms (electoral division by type cells files the same seven) | the default seven | 6.3, 6.5 / 10.2, 10.2 |
| Golden | each type's year effect, the stock's value weights | Ardcullen, Annaghvale, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh, Moyrath | 9.5, 10.4 / 5.6, 4.8 |

- Dominance: under the golden every area sits 1.5 points or more from 8 (C1); under every member of the golden's family
  (year built added, separate regressions by type, second-hand sales only, the stock's counts as weights), a point or
  more (C2); the log forms agree within 0.7 of a point (C3).
- The data separates the readings: a regression with a year term per type shows the apartments' change apart from the
  houses' in the four areas (0.5 and 1.1 against about 11 in Moyrath and Carrigvore, about 17 against 3 to 6 in
  Innishrue and Drumshallon), and the census workbook shows apartments at 12 to 14 per cent of their stock against 44 to
  45 per cent of their sales.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the census dwelling stock, read through sales at full market price | filed (SF4) |
| 2 | Unit of account | each area | filed |
| 3 | Attribution window | the two years to September, by date of sale | filed (SF3, SF5) |
| 4 | As-of dating | the 15 October 2026 extract | filed |
| 5 | Version basis | one record per sale | SF2 |
| 6 | Denominator | none | commutes |
| 7 | Weighting | the census stock's value by type | SF6 (count weights converge) |
| 8 | Window length | a year | filed |
| 9 | Boundary inclusivity | strictly over 8 | SF7 |
| 10 | Rounding path | one decimal, once | SF8 |
| 11 | Tie-break | none | C1 |
| 12 | Maturity and censoring | none | commutes |
| 13 | Order of operations | conform, join, estimate by type, weight, compare | commutes |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | the overlap | SF2 |
| 16 | Identity normalisation | eircodes, addresses | the dictionary |
| 17 | Netting against gross | VAT | SF1 |
| 18 | Dimensional units | euro, square metres | the dictionary |
| 19 | Code and status semantics | market basis, dwelling status | the dictionary; never the stump |
| 20 | Integerisation | none | commutes |
| 21 | Clause scope | every area | filed |
| 22 | Forward window contents | none | commutes |

## Literal reader

The circular and the note executed word for word ask for the change in the market value of each area's dwelling stock,
the dwellings the 2022 census counts there, between the two years, read through the sales at full market price. The
literal question is a change for the stock, not for the sales, and the sales of each year are a different selection
of the stock by type, size, newness and location. A literal reader who fits one time term over the sales has assumed
the types moved together or sold in the stock's proportions, which the joined data and the census contradict; every
other reading converges or violates a quoted sentence (fork table). Re-run on the finished pack.

## Oracles

- No shipped file carries an index, a change, a coefficient or a ranking of the areas.
- The rents workbook and the mortgage file are distractors (metadata.json).
- No control ties only under the golden on the ask.

## Ask sheet

- **Ask, each area's residential purchases in the year to September 2026, number and total paid including VAT
  (sixteen areas, two figures each, whole numbers and whole euros).** H18 home: the transactions the Department
  records with the designation (circular section 2). Path: both register extracts by date of sale, every market basis,
  and the address point file's building. Primary device: D6, an event's quantity on every line it covers: a housing
  body's purchase of a block of new apartments is filed as one line per apartment, each line carrying the whole
  block's consideration, not at full market price, so counting lines over-counts purchases and summing them multiplies
  the block's price; only the lines that share a building, a date and a consideration reveal one purchase. Every area
  has at least one block in the second year (A3). Hazards: the overlap (SF2), VAT on the old layout, date of sale
  against filing. Held against both architecture 4 readers (0 of 32 each).
- **The construction layer:** the call, the sixteen decisions, the sixteen changes and the chart; the cracker has them.
- **Main population zero-counts (asserted):** every block line is not at full market price, outside the call (X1);
  the call is unchanged with the blocks removed (SF6 in checks.py).
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| Purchases and total paid | every line a purchase at its own consideration; keeps 0 of 32 | miss |

Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 32).

Pair ceiling: 36.5 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the mirror at
the default path misses the set and keeps 12 of 16 decisions, 28.0).

Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **Stage 4 readers.** Both isolated readers missed the call on the same wrong seven, R2's (Annaghvale, Ballymarne, Carrigvore, Glenaskin, Kilbrannagh, Moyrath, Rathgowan): reader A from type medians weighted by the census stock's shares, reader B from a regression with a year term per type weighted by the stock's counts and no location term. Asks 0 and 1 of 48 (both counted every line of a block purchase; reader B's one hit, Kilbrannagh's 11.2, is its own regression coinciding). Question 1 none from both (the note's estimand "points at stock weighting but does not say how"), question 6 analytical from both, the REVIEW lines harmless (leak_check_report.md).

- **Stage 4 judge.** r5a (determinism_check_report_v5.md) NOT_DETERMINISTIC, SEND_BACK by label: ask 4's purchases open (the circular's "number of dwellings sold" against the golden's one purchase per block), ask 3's one-decimal changes open across location-constant estimators (0.2 to 1.1 points), and the designated set resting on a location control no filed sentence requires; Gate G method_or_model_selection, analytical_non_defect, Gate H pass. The judge's own derivation (type means weighted by the census stock) filed the readers' seven.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
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
