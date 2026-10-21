# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 4, drawn 2026-10-21 after architectures 1
to 3 were spent at stage 4; nothing of their worlds or decisive steps is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v4, lineage v1 to v3 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `people.first` (Evelyn, a common first name; surname
  unused), `overuse.objective` (the lane), `overuse.gate_g`, `repeat.decision` and `repeat.question_form` (a
  designation set asked as "which"), `repeat.deliverables` (one workbook). Redrawn at the draw: context artifact
  register then published_series (bans against task478 and task486) to filed_standard; gap population to objective
  (the same-driver signature was spent in five builds); differentiation lines for task481, task470, task251, task479,
  task464 and task484. People from `guard.py names --geo ireland --seed 4824` and `--seed 4825`: Clare McEntee and
  Evelyn Clune.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: the residential property price register in two layouts, the valuation register's dwelling attributes
  and the address point file's small areas conformed into one sales table, and each area's residential property
  price change built from it.
- **The decision and the quantity:** the Minister for Housing designates as rapid price growth areas for 2027 the
  local authority areas whose residential property price index, as the Brannagh Statistics Office measures it, rose by
  more than 8 per cent from the year to September 2025 to the year to September 2026. Forward facing: the designation
  governs 2027.
- **Data-native sentence:** the homes that sold in each area are a different slice of its stock in each year, more of
  them in the cheaper or the dearer electoral divisions, larger or smaller, new or second-hand, and the electoral
  division of a sale sits only in the address point file.
- **Strategy:** `population_selection`; Gate G `method_or_model_selection`; gap `objective` (the median sale price is
  correct and is not what the designation is scored on); generators G6, G17; pattern none. Layer 2 family
  `estimand_identification`, pattern `own:an area's price change read from summaries of what sold when the sold
  homes are a shifting sample of the stock by location, size and newness`. Compound by design: the client's held
  tasks keep a dimension in another file, and here every partial correction (per square metre, by dwelling type
  against the census stock, a regression without location) files its own wrong set.

## Default path

A strong analyst with every field read correctly:

1. Reads the circular: an area is designated when the Office's residential property price index for it rose by more
   than 8 per cent in the year to September 2026 on the year to September 2025; and the methodology note: the index
   measures the change in the market value of the area's dwellings, sales at full market price, by date of sale, new
   dwellings with VAT.
2. Conforms the two register extracts (day-first dates, euro text, VAT grossed up, the ten-day overlap counted once),
   joins the valuation register for the dwelling type and keeps the market sales of the two years.
3. Sees that the mix of types differs between the years and against the census stock, so takes each type's change in
   median price and weights the four changes by the census stock of each area.
4. Compares with 8 per cent.

**Ends on:** Annaghvale, Ballymarne, Carrigvore, Glenaskin, Innishrue, Kilbrannagh, Moyrath and Rathgowan designated

- On that path Ardcullen and Dunmarra stand at 2.9 and 3.5 per cent, and Ballymarne, Innishrue, Moyrath and
  Rathgowan at 11.9 to 14.4. The raw median change and the median per square metre file sets of the same kind; a
  regression on type, floor area and new-dwelling status without location drops Innishrue and Moyrath but keeps
  Ballymarne and Rathgowan and still leaves Ardcullen and Dunmarra out.

**Golden:** Ardcullen, Annaghvale, Carrigvore, Dunmarra, Glenaskin and Kilbrannagh designated; the hedonic changes are
9.9 to 12.3 per cent in the six and 2.0 to 6.3 elsewhere.

## Stump sentence

The default path compares each area's sales between the two years dwelling type by dwelling type, weights the changes by the census stock and files Annaghvale, Ballymarne, Carrigvore, Glenaskin, Innishrue, Kilbrannagh, Moyrath and Rathgowan designated, because it never asks whether the homes that sold within each type were the same kind of home in both years: in several areas the second year sold more homes in the cheaper or the dearer electoral divisions, or new homes at a premium, and only a hedonic regression on type, floor area, new-dwelling status and electoral division gives each area's change for an unchanged dwelling.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics): the residential property price register in two systems' layouts, the valuation register and the address point file conformed into one table of sales with each dwelling's attributes and location, and each area's price change measured from it, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each area's residential property price change for an unchanged dwelling, worked the way official property price statistics measure it from administrative sales records: the sales are a changing sample of the dwelling stock, so the change is the time effect of a hedonic regression of log price on the dwelling's characteristics and location (the Handbook on Residential Property Prices Indices).

Swap: "which bakeries' loaf prices rose more than 8 per cent" keeps a price change and loses the step: a bakery's loaf is the same product in both years, nothing about which loaves were bought changes what one loaf costs, and no register holds a loaf's size and location apart from its price.

Layer 1: the old register layout's day-first dates and euro text prices, its new-dwelling prices exclusive of VAT, eircodes keyed in four styles or missing (joined by address), the new system's property numbers and VAT-inclusive consideration, the ten days of October 2025 filed in both systems, sales filed in one year for a sale in the other, out-of-window sales in both extracts, sales not at full market price, and the location held only in the address point file; each is how the producing systems write, nothing is placed to be caught, and checks.py asserts the call under them (SF1 to SF8).

Layer 2: estimand_identification, a price change read from a shifting sample of a heterogeneous stock: the choice that flips the call is holding the dwelling's type, size, newness and electoral division fixed in a regression with a year term, instead of comparing what sold, per square metre, by type against the stock, or by regression without location.

Decisive step: estimating each area's change as the year effect of a hedonic regression of log price on dwelling type, log floor area, new-dwelling status and electoral division, which puts Ardcullen and Dunmarra at 9.9 and 10.1 per cent and Ballymarne, Innishrue, Moyrath and Rathgowan at 5.7 to 6.3.

Not semantics: every field, code and definition read correctly (the two layouts, VAT, the market basis, the property numbers, the electoral divisions) still leaves the easy route on summaries of what sold, because no field says the homes that sold in the second year were a different slice of the stock; the step is the inference that the sales are a sample whose mix of location, size and newness moved, which the joined attributes against each other show and no sentence says.

Not rule application: the circular and the methodology note fix the population (each area's dwellings, sales at full market price), the outcome (the change in market value), the window (the two years to September), the unit (each area) and the comparison (more than 8 per cent), and no rule says how the value of the area's dwellings is read from the sales; executing every filed rule on the sales by type files the default path's eight.

Analyst test: a strong analyst who conforms every file and reads every rule, comparing each type's median sale price and weighting by the census stock, files Annaghvale, Ballymarne, Carrigvore, Glenaskin, Innishrue, Kilbrannagh, Moyrath and Rathgowan designated (the default path's Ends on); the raw median, the median per square metre and a regression without location each file another wrong set; only the hedonic regression with the electoral division files the golden six; checks.py runs them on the clean truth (R3a to R3d).

Estimand: the circular (dhlgh_circular_rapid_price_growth_areas_2026.pdf, section 1) and the methodology note (bso_rppi_methodology_note_2026.pdf, sections 1 and 2): the population (each local authority area's dwellings, read through its sales at full market price), the outcome (the change in their market value), the window (the year to September 2026 on the year to September 2025, each year as a whole, by date of sale), the unit (each area) and the comparison (more than 8 per cent).

No decoy: nothing is planted: the register extracts, the valuation register, the address points, the electoral divisions and the census are the producing bodies' records, the note states the basis without a method, and no earlier index, published change or ranking of the areas ships; the rents and mortgage files rank nothing on the price of an unchanged dwelling.

No certified replay: no certified or published index, change or coefficient ships; the method is not recovered by reproducing any figure.

Lesson: a price change read from the sales is a change in what sold unless the dwellings are held fixed, and holding them fixed takes every attribute the stock varies on, location included, which sits in its own register; no build on file reads a constant-quality price change.

## Readability screen

| Rung | What takes the reader there | Verdict |
|---|---|---|
| Layer 1: layouts, VAT, overlap, eircodes, market basis | the dictionary, the note's sections 2 and 3 | readable |
| R0 the median change | the register extracts | readable |
| R1 the median per square metre | the valuation register's floor area | readable |
| R2 (default path) types weighted by the census stock | the census workbook beside the note's "the market value of the area's dwellings" | readable |
| R3 regression without location | the valuation register's attributes | readable |
| R4 (decisive) the regression with the electoral division | nothing: no sentence names a regression, mix or location effect; the address point file is listed as a source | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | new-dwelling prices in the old layout | grossed up by 13.5 per cent | as filed | same call (asserted) | note section 3 |
| SF2 | the two systems' overlap | one record per sale | both kept | same call (none kept twice, asserted) | note section 3 |
| SF3 | the year | by date of sale | by filing | not filed alternatives | note section 2 |
| SF4 | which sales | at full market price | every sale | not filed alternatives | note section 2 |
| SF5 | the two years | each as a whole | the September months | not filed alternatives | note section 1 |
| SF6 | the form of the time effect | pooled year term on log price | monthly terms averaged, levels, second-hand only, with year built | same call (C2, C3) | the data |
| SF7 | more than 8 per cent | strictly over, on the change to one decimal | at or over | same call (C1) | circular section 1 |
| SF8 | the printed change | the unrounded change rounded once | rounded first | same call (asserted) | prompt |

## Ladder

Built values from the cut pack (generator/checks.py L1 and L2, C1 to C4), per cent.

| Rung | Route | Designated | Ardcullen, Dunmarra / Ballymarne, Innishrue, Moyrath, Rathgowan |
|---|---|---|---|
| R0 | median sale price | Annaghvale, Ballymarne, Glenaskin, Innishrue, Kilbrannagh, Moyrath, Rathgowan | 4.3, 3.0 / 11.9, 16.2, 19.3, 14.1 |
| R1 | median per square metre | the default eight | 4.2, 3.7 / 12.0, 10.5, 12.4, 11.8 |
| R2 (default path) | types weighted by the census stock | the default eight | 2.9, 3.5 / 11.9, 12.6, 14.4, 12.5 |
| R3 | regression without location | Annaghvale, Ballymarne, Carrigvore, Glenaskin, Kilbrannagh, Rathgowan | 4.8, 3.0 / 11.3, 6.2, 5.1, 11.8 |
| R3b | electoral division by type cells | the golden six with Innishrue and Moyrath | 9.0, 10.4 / 5.9, 8.5, 8.7, 6.2 |
| Golden | hedonic with the electoral division | Ardcullen, Annaghvale, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh | 9.9, 10.1 / 5.7, 6.3, 5.7, 6.2 |

- Dominance: under the pooled hedonic every area sits 1.5 points or more from 8 (C1); under every log form and the
  levels form, a point or more (C2); the log forms agree within 0.7 of a point (C3).
- The data separates the readings: in Ardcullen and Dunmarra the second year's second-hand sales lean to the cheaper
  divisions, in Ballymarne and Rathgowan to the dearer, and in Innishrue and Moyrath a fifth of the second year's
  sales are large new homes in the dearer divisions.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | sales at full market price | filed (SF4) |
| 2 | Unit of account | each area | filed |
| 3 | Attribution window | the two years to September, by date of sale | filed (SF3, SF5) |
| 4 | As-of dating | the 15 October 2026 extract | filed |
| 5 | Version basis | one record per sale | SF2 |
| 6 | Denominator | none | commutes |
| 7 | Weighting | none (a common shift) | commutes |
| 8 | Window length | a year | filed |
| 9 | Boundary inclusivity | strictly over 8 | SF7 |
| 10 | Rounding path | one decimal, once | SF8 |
| 11 | Tie-break | none | C1 |
| 12 | Maturity and censoring | none | commutes |
| 13 | Order of operations | conform, join, estimate, compare | commutes |
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

The circular and the note executed word for word ask for the change in the market value of each area's dwellings
between the two years, read through the sales at full market price; the literal question is a change for the
dwellings, not for the sales, and the sales of each year are a different selection of the dwellings. A literal reader
who compares what sold has assumed the sold homes are alike in both years, which the joined attributes contradict;
every other reading converges or violates a quoted sentence (fork table). Re-run on the finished pack.

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
  against filing.
- **The construction layer:** the call, the sixteen decisions, the sixteen changes and the chart; the cracker has them.
- **Main population zero-counts (asserted):** every block line is not at full market price, outside the call (X1);
  the call is unchanged with the blocks removed (SF6 in checks.py).
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| Purchases and total paid | every line a purchase at its own consideration; keeps 0 of 32 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 32).
- Pair ceiling: 34.8 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the set and keeps 10 of 16 decisions, 24.5). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
