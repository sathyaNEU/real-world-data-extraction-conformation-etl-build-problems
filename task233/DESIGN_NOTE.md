# task233 design note

Architecture 2 (re-rooted 2026-10-16), wave 2, seed DQ06 (whether a register statistic keeps its quality flag
when the missing field may not be missing at random): the seed's world, decision and quantity only, the pitfall
re-found from the data under the 10/10 rules. General Statistics & Data Science, missing data, censoring and
measurement error, Data Quality Monitoring & Alerting. The island's Department of Education publishes the school-leaver
destinations release each December from the survey a university's Social Survey Unit runs for it; the unit's
survey director signs a quality flag for each district's NEET rate and higher-education entry rate, the first under
the revised standard QS-4 v2.0, judged on how far the rate would move if the survey's nonrespondents departed from
the destination model's allocation as the 2025 nonresponse follow-up found.

Architecture 1 (same world and decision, follow-up in the five middle and deprived districts) was sent back by the
judge at stage 4: inside each attainment band its follow-up allocations barely varied, so a points gap or a ratio
per band fitted the follow-up within 1 to 4 log-likelihood units of the odds scale and gave other flags, and the
prompt's "rate the release will publish" was open for suppressed statistics (`determinism_check_report_arch1.md`,
the card's lineage, `## Tried and rejected`). Architecture 2 follows up five districts chosen across the island's
range, so within every band the follow-up's allocations differ by district and only the odds scale fits them, and
defines the headline rate as a computation made whatever the flag.

## Draw

Card `cards/task233.json` (architecture v2, re-registered 2026-10-16). Guard verdict WARN, one line each:
`three_rules.strategy_risk` (grain_or_unit) is answered by the analyst test below, which `checks.py` runs on the
clean truth; `repeat.gate_g` (task463) and `overuse.gate_g` (method_or_model_selection, 5 of the last 12) are
accepted because the mechanism, the task type and the forum differ from every neighbour (task463 chooses a seasonal
adjustment model for price index series);
`test.same_puzzle_older` (task458) and `test.same_driver_older` (task256, task262, task54) are differentiated on the
card; `driver.near` against this slot's v1 (0.57) is differentiated (the follow-up design and the forcing evidence
changed, the flags changed) and task446 v2 (0.13) is differentiated.

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, serving Data
  Quality Monitoring & Alerting (the domain index lists this task type under DD and DQ).
- **Niche.** The destinations survey, run by a university's Social Survey Unit for the Department of
  Education, asks every school leaver in October where they went; about one in six do not answer. The release allocates each nonrespondent across the five destinations in
  proportion to the previous year's respondents of the same district and attainment band (a missing-at-random
  allocation). In 2025 the unit's field team followed up a random sample of nonrespondents in five districts
  chosen across the island's range and found where they really went. The survey director flags each 2026 statistic
  standard, caution or suppressed on the sensitivity shift the revised quality standard defines.
- **The call.** For each of the twelve districts' NEET rate and higher-education entry rate (24 statistics),
  the flag: standard (shift under 1.0 point), caution (1.0 to under 3.0) or suppression (3.0 or more).
- **Shape.** 10, a scorecard against thresholds: each statistic's sensitivity shift in each district checked
  against the standard's two thresholds, each check graded. Decision designation_set, answer set_of_items, question
  form what.
- **Strategy.** grain_or_unit with G14 decisive (the departure measured in the followed-up pool does not carry
  as points to every pool) and G17 supporting (each shift judged against the flag bands); Gate G
  method_or_model_selection; calibration gold_standard_subsample; context artifact close_out_summary; layer 2
  family estimand_identification, pattern general-statistics-data-science/missing-data-censoring-measurement-error/3.
- **Forum, event, organisation.** customer_or_counterparty (the Department of Education, which commissions the
  survey and publishes the release, receives the flagged tables), launch_or_rollout (the 2026 release is the first
  under QS-4 v2.0, which replaced a flag on the nonresponse share alone), university_or_school (the Social Survey
  Unit). Redrawn at stage 3 with the role and the shape: task189, task463 and task152, filed before this card's
  re-registration, had taken the earlier statistics-office head, grid, panel, statutory filing and government agency.
- **People** (`guard.py names --geo Ireland --seed 233`): Polly Ganley, the survey director, who signs the
  flags; Emmett Phelan, field manager who ran the 2025 follow-up; Leanne Henebry, survey methodologist who
  keeps the allocation and the quality standard.
- **Deliverables.** `leaver_destinations_2026_quality_flags.xlsx`: each statistic's flag beside its headline
  rate, and the attainment-band table.
- **Data-native sentence.** A nonrespondent's allocation is the previous year's respondents' share in its own
  district and attainment band, so NEET allocations run from under 1 per cent (a high attainer in an affluent
  district) to over 55 (a low attainer in a deprived one), and the follow-up found nonrespondents departing from
  them by one factor on the odds in every district and band it covered (a 3 per cent allocation became about 7 and
  a 35 per cent one about 57), so the same departure is a few points at one end of the island and twenty at the
  other, and differs between two districts inside the same band.

Sources, one line each (what it teaches; how this build differs):
- Client pattern missing-data-censoring-measurement-error/3 (delta-adjust for nonignorable missingness;
  shortcut: complete-case agrees with the imputation, so robust): the frame; here the delta is not swept over a
  grid but calibrated on a gold-standard follow-up and carried to districts it never covered, and the shortcut is
  this build's rung 0.
- Seed DQ06: the world, the decision and the quantity only; its decoy architecture is not used.
- Hansen and Hurwitz (1946), the nonresponse follow-up subsample; Little and Rubin, Statistical Analysis with
  Missing Data, pattern-mixture models; Carpenter and Kenward (2013), Multiple Imputation and its Application,
  delta adjustment on the logit scale for binary outcomes: the field's method. No card or ledger row on file
  carries it.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomisation unit),
  task229 (a daily mean through a convex rating), task230 (net coding bias of a late channel), task231 (a rate over
  units still active, exits reported late), task232 (a transmission rate from delayed, mixed outcomes). None
  carries a missing-not-at-random departure or a scale of transport.
- task446 v2 (nearest other driver, 0.13): a screen's yield carried across pools through its error rates; this
  build has no screen and no base rate to recover.

## Default path

1. Read the quality standard (QS-4): the flag bands on the sensitivity shift (under 1.0 point standard, 1.0 to
   under 3.0 caution, 3.0 or more suppression), the headline rate, and the counterfactual the shift measures (each
   nonrespondent's allocation moved as the most recent nonresponse follow-up found followed-up nonrespondents'
   destinations departing from their allocations, worked for each nonrespondent in turn and summed to the
   district).
2. Conform the 2026 survey frame: map school codes to the 2026 districts (two schools moved), count leavers and
   nonrespondents per district, and total each district's NEET and HE allocations over its nonrespondents.
3. Conform the 2025 follow-up: join its outcomes to the 2025 frame through the case crosswalk (references
   prefixed L), keep one outcome per case, drop unresolved cases and the cases whose leaver has a form in the final
   file, and map the field team's codes to destinations: 3,134 comparable cases.
4. Measure the departure the follow-up found: the comparable cases' NEET share minus their mean NEET allocation,
   14.5 points, and the same for higher-education entry, minus 11.1.
5. Each district's shift: its nonrespondent share times the gap.
6. Flag each statistic against the bands.

Ends on: 11 of the 24 flags wrong. It cautions the NEET rates of Southern Shore, Upper Valley and Glen Villages
(standard), suppresses the NEET rates of Hill Country and Northern Plains (caution), cautions the NEET rates of City
West and City East (suppression), cautions the higher-education entry rates of Hill Country and Northern Plains
(suppression) and cautions those of Old Docks and Mill Towns (standard).

Golden: suppression for the NEET rates of Riverside, City West and City East and the higher-education entry rates
of Hill Country and Northern Plains; the standard flag for the NEET rates of Southern Shore, Upper Valley and Glen
Villages and the higher-education entry rates of Old Docks and Mill Towns; caution for the other fourteen.

## Stump sentence

A competent solver adds the 2025 follow-up's pooled points gap to each district's nonrespondents in proportion to
their share and files 11 of the 24 flags wrong (Ends on: caution for three affluent NEET rates that stay standard,
suppression for the Hill Country and Northern Plains NEET rates, caution for the City West and City East NEET rates
and the Hill Country and Northern Plains higher-education rates that are suppressed, caution for the Old Docks and
Mill Towns higher-education rates that stay standard); the step that lands it there is carrying a departure measured
across allocations from under 1 to over 55 per cent as a fixed number of points instead of nonrespondent by
nonrespondent on the odds scale, the one scale on which the follow-up's districts and bands agree.

## Three rules

- **Task type:** general-statistics-data-science / missing-data-censoring-measurement-error, which serves
  Data Quality Monitoring & Alerting: a published statistic's sensitivity to nonignorable nonresponse, judged
  against a quality flag's bands, the departure calibrated on a gold-standard follow-up.
- **Domain test:** the quantity that decides is each statistic's shift under a departure from missing-at-random,
  the pattern-mixture delta adjustment the missing-data field calibrates on a nonresponse follow-up and applies to
  each nonrespondent on the logit scale for a binary outcome.
- **Swap:** in this domain the setting is another field's and the swap is of the method. Put a generic summary in
  place of the delta adjustment (the follow-up's points gap times the nonresponse share, the same gap per band, or
  the agreement between the respondent-only rate and the allocated rate) and 9 to 11 flags change; the call stands
  on the missing-data object, not on the education nouns. Swapping the nouns alone ("hospitals' readmission rates,
  patients lost to follow-up") keeps the method and is the same task, which is what a General Statistics draw is
  meant to be.
- **Layer 1:** the 2026 survey came back on paper and online forms with different code lists, and the online form's
  2026 edition went live a day into fieldwork, as the form change of 2026 produced; the follow-up's outcomes are
  keyed by the field team's case numbers and reach the survey through a crosswalk that drops the reference's letter
  prefix, with 174 cases found by two routes; the follow-up sample was drawn from the nonrespondents at the close, so
  358 resolved cases answered late and sit in the final 2025 file as respondents; the district map was revised for
  2026 and two schools moved. None is placed to be caught, and on the clean truth the default path and the golden
  are unchanged.
- **Layer 2:** estimand_identification, missing-data-censoring-measurement-error/3: the departure found on the
  follow-up has to be carried to nonrespondents the follow-up never reached, on the scale on which it is stable;
  the follow-up's free-slope calibration on the logit of the allocation returns slope 0.99 for NEET and 1.03 for
  higher education, while a points gap or a ratio, pooled or per band, misfits it.
- **Decisive step:** carrying the follow-up's departure nonrespondent by nonrespondent on the odds scale (the
  logit delta, or any model of the departure on each nonrespondent's own allocation that fits the follow-up),
  because allocations run from under 1 to over 55 per cent and differ by district inside each band, and the
  follow-up's districts and bands agree on one odds ratio, not on a points gap or a ratio.
- **Not semantics:** the default path reads every field, code and definition right (the five destinations, the
  code lists, the allocation columns, the 2026 district map, the crosswalk, the headline rate) and computes the
  right gap; the wrong flags come from the scale the gap is carried on, which no field, code or unit names.
- **Not rule application:** the standard files the bands, the rounding, the headline rate and the counterfactual
  (each nonrespondent's allocation moved as the follow-up found, the rate recomputed); no filed sentence says on what
  scale the departure moves, so executing every stated rule with the gap the follow-up gives still files the eleven
  wrong flags.
- **Analyst test:** with every field read and every rule applied, a strong analyst takes the follow-up's departure
  as its pooled points gap (14.5 points for NEET, minus 11.1 for HE entry), adds it to each district's
  nonrespondents and files the default path's Ends on: 11 of the 24 flags wrong; stratifying the gap by band keeps
  the same 11; `checks.py` runs that route on the generator's clean truth and asserts it, then changes the scale
  alone and asserts the golden.
- **Estimand:** the quality standard (QS-4, in the pack) fixes the population (all leavers of the 2025-26 school
  year on the 2026 frame, by 2026 district, respondents and nonrespondents), the outcome (the headline NEET and HE
  rates), the comparison (the headline rate against the rate with each nonrespondent's allocation moved as the 2025
  follow-up found followed-up nonrespondents departing from theirs), the unit (percentage points) and the bands.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states a gap, a ratio or a flag;
  the follow-up report gives its design and completion, not a headline departure; no rule is withheld and no block
  is copied; no shipped artifact ranks or flags the statistics.
- **No certified replay:** no certified or published figure exists for the method to reproduce; the follow-up's
  outcomes are field findings per case, and the scale is read from how those findings vary with the allocation, not
  recovered by matching a stated number.
- **Lesson:** a departure from missing-at-random measured on a follow-up transports on the scale on which the
  follow-up shows it constant; for a binary outcome whose allocations run from under 1 per cent to over a half that
  is the odds scale, so one departure moves a 3 per cent allocation by 4.1 points and a 35 per cent one by 22.0, and
  a pooled or per-band points gap flags the statistics least exposed to it and clears the ones most exposed. No
  build on file teaches nonignorable-nonresponse sensitivity carried on the logit scale.

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the allocation's own shift (headline rate minus respondent-only rate): 9 flags wrong | QS-4 s.3 names the follow-up's departure, so a reader of the standard leaves it | the allocation columns sit beside the forms | yes, complete case against the imputed rate | the follow-up shows nonrespondents unlike respondents | no | one subtraction | readable |
| 1 the follow-up's pooled points gap times each district's nonrespondent share: 11 flags wrong | QS-4 s.3 "as the follow-up found" invites the gap | the follow-up's outcome beside the 2025 allocation | yes, the first summary of a follow-up | the follow-up rejects it (54.4 and 242.0 log-likelihood units worse than one odds ratio, NEET and HE) for a solver who fits it | no | one subtraction and one product | readable |
| 2 the points gap per attainment band, carried by each district's band mix: 11 wrong | none | the band column on both frames | yes, holding the pool to a visible attribute | the follow-up rejects it (17.8 and 98.3 worse, four parameters against one): inside a band the gap still moves with the district's allocation | no | a group-by | readable |
| 2 a ratio of rates, pooled or per band: 2 wrong | none | none | yes, when the gap is seen to grow with the allocation | the follow-up rejects it (60.0 and 36.6 pooled, 22.8 and 14.2 per band) | no | one division | readable |
| 3 (decisive) the departure carried nonrespondent by nonrespondent on the odds scale, the scale on which the followed-up districts and bands agree | no sentence names a scale, a model or a link; QS-4 s.3 says only that each allocation moves as the follow-up found | no column names a scale or an odds ratio; the follow-up has outcomes and allocations only | no: the reflexes stratify, borrow or take a ratio | only the follow-up's own cases, which show it to a solver who asks on what scale its districts and bands agree | no | not linear: the shift per nonrespondent runs from 4.1 points at a 3 per cent allocation to 22.0 at 35 | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "NEET rate" | the release's NEET destination (unemployed and seeking work, or not working or studying) | unemployed only | same call: the shift reads the NEET allocation column, never a respondent's code | same call (asserted: the shift uses no activity code) |
| SF2 | "higher-education entry rate" | higher-education courses on or off the island | island courses only | same call: the shift reads the HE allocation column | same call (asserted) |
| SF3 | "district" | the 2026 map | the 2025 map (two schools) | every flag unchanged | QS-4 s.1 (the map in force on the census date); same call (asserted) |
| SF4 | the rate's denominator | every leaver on the 2026 frame | respondents only | shifts about a fifth larger, flags move | QS-4 s.2 (a rate over all leavers on the frame) |
| SF5 | "nonrespondent" | no form returned by the close (allocation present) | none on the frame | one reading: every row with an allocation has no form and every row without one has a form | C1 (asserted) |
| SF6 | "allocation" | the frame's allocation columns (the previous year's respondents in the same district and band) | current-year respondents' shares recomputed | every flag unchanged | QS-4 s.2 and methodology s.4 (the destination model's allocation is the frame's); same call (asserted) |
| SF7 | "shift" and its sign | sensitivity rate minus headline rate, banded on its size | signed bands | HE shifts are negative, so a signed reading clears every HE rate | QS-4 s.4 (bands on the size of the shift) |
| SF8 | "the most recent nonresponse follow-up" | the 2025 follow-up | none | one follow-up in the pack | C1 |
| SF9 | "followed-up nonrespondents" | resolved cases whose leaver has no form in the final 2025 file | with late returners or unresolved cases | late returners carry no allocation and unresolved cases no outcome, so neither can be compared | QS-4 s.6 (resolved cases of leavers who remained nonrespondents); C1 (asserted) |
| SF10 | cases found by two routes | one outcome per case | each row counted | every flag unchanged | follow-up report s.3 (one outcome per case); same call (asserted) |
| SF11 | grain of the counterfactual | each nonrespondent's own allocation moved, summed to the district | the departure applied once to the district's mean allocation | one flag moves (Riverside HE) | QS-4 s.3 ("worked for each nonrespondent in turn") |
| SF12 | rounding path | the unrounded shift banded | the shift rounded to one decimal, then banded | same call (no shift within 0.2 points of an edge) | QS-4 s.5; same call (asserted) |
| SF13 | band edges | 1.0 and 3.0 belong to the higher flag | strict | same call | QS-4 s.4; same call (asserted) |
| SF14 | as-of | the 2026 frame extract of 10 November 2026 | none | one 2026 frame | C1 |
| SF15 | case references | the crosswalk's references with the frame's letter prefix | raw strings | the raw join matches no case | C1: every resolved case matches after the prefix (asserted) |
| SF16 | headline rate of a suppressed statistic | the rate computed under QS-4 s.2 | the suppression mark | the four suppressed rates' figures | QS-4 s.2 ("computed for every district whatever its flag") and s.4 ("headline rate withheld") |
| SF17 | activity codes of online returns made on build 7 | the 2025 edition's order (the 2025 final file's build-7 returns with their processed destinations) | the reference list's 2026 order | ask figures move (no flag) | data dictionary (the list is the 2026 edition's); C1: every 2025 online return is build 7 and no build-7 return carries the 2026 edition's code 8 (asserted) |

## Ladder

Four rungs, each a defensible analysis, each dying to one shipped fact (shifts in points; flags S standard, C
caution, X suppression).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | the allocation's own shift (headline minus respondent-only) | 9 wrong | QS-4 s.3: the shift is under the follow-up's departure |
| 1 (default) | pooled points gap (NEET 14.5, HE minus 11.1) times each district's nonrespondent share | 11 wrong (above) | the follow-up's cases: one odds ratio fits them 54.4 and 242.0 log-likelihood units better |
| 2 | the gap per band carried by band mix; a ratio of rates, pooled or per band | 11, 2 and 2 wrong | the follow-up's cases inside each band: a gap per band misfits by 17.8 and 98.3 units, a ratio by 60.0 and 36.6 pooled and 22.8 and 14.2 per band |
| 3 (golden) | the follow-up's odds ratio (NEET 2.46, HE 0.41), fitted with the allocation as offset, applied to each nonrespondent's allocation | the golden grid | |

- **Margins.** Every logit-scale estimator (pooled offset, fixed-effects logistic on the followed-up districts,
  Mantel-Haenszel over district and band, band-specific odds ratios, district-own odds ratios, a logistic
  calibration with free slope) gives the golden grid, every shift at least 0.29 points from a band edge; the
  default path's shifts sit at least 0.22 from an edge. A quadratic points model, a probit shift, a straight line in
  the allocation and the nearest followed-up district's band gaps also give the golden grid.
- **Position and dominance.** The default path is wrong in 11 cells across both statistics and all three flags;
  the per-band gap is wrong in the same 11 and the ratio in two others; no correction short of conditioning the
  departure on each nonrespondent's own allocation reaches the golden, and the follow-up rejects every one that
  does not.
- **Grid.** The decisive choice moves 11 of 24 cells; the rung-2 constructions move 2 to 11.
- **Worth.** The flags are the graded call; worth is counted on flags, never on an intermediate.

## Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | every leaver on the 2026 frame, respondents and nonrespondents, by 2026 district | QS-4 s.2; C1 |
| 2 | Unit of account | the leaver; the statistic is a district rate | QS-4 s.2 |
| 3 | Attribution window | the 2025-26 school year's leavers, destination on 1 October 2026 | methodology s.1; one frame |
| 4 | As-of dating | the frame extract of 10 November 2026 after the allocation run of 9 November | manifest and dictionary |
| 5 | Version basis | the 2025 final file (31 March 2026) for the follow-up's allocations | QS-4 s.6; C1 (the only 2025 file) |
| 6 | Denominator | all leavers on the frame | QS-4 s.2 (SF4) |
| 7 | Weighting | none: a census of leavers, each counts once | methodology s.1 |
| 8 | Window length | one survey year | QS-4 s.3 |
| 9 | Boundary inclusivity | bands closed at 1.0 and 3.0 on the higher flag | QS-4 s.4; C1 (no shift within 0.2 of an edge, asserted) |
| 10 | Rounding path | flags on the unrounded shift; rates shown to one decimal | QS-4 s.5 (SF12) |
| 11 | Tie-break | none needed: each statistic gets its own flag | QS-4 s.4 |
| 12 | Maturity and censoring | nonrespondents' true destinations unknown; the follow-up's resolved cases only | QS-4 s.6 (SF9) |
| 13 | Order of operations | move each allocation, sum to the district, subtract, band | QS-4 s.3 and s.4 (SF11) |
| 14 | Row order | irrelevant to sums | C1 |
| 15 | Duplicate resolution | one outcome per follow-up case | follow-up report s.3; C1 (SF10) |
| 16 | Identity normalisation | case references given the frame's letter prefix | C1 (SF15) |
| 17 | Netting against gross | none: each statistic's shift stands alone | QS-4 s.3 |
| 18 | Dimensional units | allocations as fractions, rates and shifts in percentage points | dictionary; QS-4 s.3 |
| 19 | Code and status semantics | field team codes mapped to release destinations; build-7 online returns in the 2025 edition | follow-up report s.5 (SF1, SF2); dictionary (SF17) |
| 20 | Integerisation | none | not applicable to a rate |
| 21 | Clause scope | QS-4 applies from the 2026 release to each district's NEET and HE rate; the headline rate whatever the flag | QS-4 s.1 and s.2 (SF16) |
| 22 | Forward window contents | the 2026 nonrespondents, whose destinations no follow-up has reached | QS-4 s.3; the 2026 frame |

## Literal reader

Executed word for word, QS-4 and the prompt fix the population (every leaver on the 2026 frame by 2026 district),
the statistic (the headline NEET and HE rate, allocations included, computed whatever the flag), the counterfactual
(each nonrespondent's allocation moved as the 2025 follow-up found followed-up nonrespondents' destinations
departing from their allocations, worked nonrespondent by nonrespondent and summed), the bands and the rounding. No
sentence fixes the scale on which a departure moves an allocation; the follow-up does. Its five districts run from
the most affluent to the most deprived (the field report says they were chosen to cover the island's range), so
inside every band its 3,134 comparable cases carry allocations that differ by district; regressing the found
destination on the logit of the allocation returns slope 0.99 for NEET and 1.03 for higher education, a pure shift
on the odds scale, and one odds ratio fits the cases better than a pooled points gap (by 54.4 and 242.0
log-likelihood units), a pooled ratio (60.0 and 36.6), a points gap per band (17.8 and 98.3, with four parameters
against one) or a ratio per band (22.8 and 14.2), while odds ratios per band add under one unit. A points departure
would also put 1,915 of the 7,641 nonrespondents' HE allocations below zero. Every model that fits the cases (the
logit offset, a free-slope calibration, a quadratic or a line in the allocation) gives the golden grid. The default
path reads every term the same way and differs only in the scale, so the stump is analysis, never a reading.

## Oracles

- The follow-up's own cases (resolved nonrespondents against their allocations, by district and band): under every
  scale they are what the departure is measured on; they reject the points gap and the ratio only for a solver who
  fits them by allocation and asks on what scale they agree, which is the decisive insight. They are the field's
  bench, not a figure that ties only under the golden.
- The 2025 release tables (a distractor) give 2025 rates on the 2025 map; they flag nothing and tie with nothing in
  2026.
- No published shift, flag, odds ratio or control total ships; no artifact ranks or flags the statistics.

## Ask sheet

Two asks, 36 figures, decoupled from the call: the call reads the frame's allocation columns, the leaver count and
the follow-up; the asks read the returned forms' activity codes and the attainment bands, columns the call never
reads.

**Main population (zero device rows, asserted):** the 2026 frame's school codes, nonrespondent rows and their
allocation columns; the 2025 final file's nonrespondent rows and allocations for followed-up districts; the
follow-up's resolved cases and the crosswalk. Devices live in the returned forms' `activity_code` and `form_build`
and in `attainment_band`, which the call does not read (asserted: every flag unchanged when every activity code and
band is scrambled).

| Ask | Figures | H18 home | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|
| A: each district's headline NEET rate and HE entry rate | 24 | a component of the call: the figure each flag attaches to | D3, meaning set per form build: online returns made before the 2026 edition went live (build 7) carry the 2025 edition's codes, whose order the 2026 edition shifted when it inserted "higher education outside the island" as code 2; the reference list holds the 2026 edition. Read with it, early further-education returns become higher education and early unemployed returns become employment. The 2025 order is recoverable from the 2025 final file, whose build-7 returns carry their processed destinations | the two schools that moved district (main-path mess, neutral there) | 2026 frame (school_code, return_form, form_build, activity_code, the five allocation columns), activity code list, school register, 2025 frame (activity_code, form_build, destination) | natural read with the 2026 list (every rate off by 0.09 to 1.37 points); the old order applied to every online return; the answer |
| B: for each attainment band across the island, the number of leavers and the headline NEET and HE entry rates | 12 | a component of the release: the band table published beside the district flags | D2, a label stored before a silent switch: the frame's attainment band came with the schools' September leaver returns, before the October appeals raised about one leaver in twenty-five into a higher band; the release bands on the examination points as finalised, which the points file carries | ask A's form-build device (every band rate moves with it) | 2026 frame (attainment_band, activity_code, form_build, allocations), examination points file, methodology s.5 band cut-offs | frame bands (counts and rates off in every band); final bands with the 2026 code list (rates off); the answer |

- **Span:** nine files and 16 column uses across the two asks; no shared primary.
- **Shared hazard:** the form-build device moves every figure in both asks; the band device moves ask B only.
- **Realism:** a web form whose new edition went live a day into fieldwork while the processing reference table
  holds only the current edition, and a leaver return whose bands were filled before appeals, are both records a
  survey unit's systems make with no task in mind.
- **Referee:** none; nothing ties only under the golden (the allocations come from the previous year's respondents,
  so the 2026 forms cannot be checked against them).

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 1) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A NEET rate (12) | maps every online code with the activity code list it is given, which is the 2026 edition | misses the same way | miss |
| A HE entry rate (12) | the same mapping turns early further-education returns into higher education | misses the same way | miss |
| B leavers per band (4) | counts the frame's attainment band | misses the same way | miss |
| B NEET and HE rate per band (8) | the frame's band and the 2026 code list; a solver who rebands on the final points still carries the code device | misses the same way | miss |

- **Cracker keeps:** about 0.11 of the ask weight at most (a cracker that rebands on final points keeps the four band
  counts; no single habit keeps a rate).
- Mirror leakage: 11 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the
  call's construction).
- Pair ceiling: 34.6 (the cracker keeps the four band counts, 4 of 36 figures, about 0.11 of the ask weight: C = 38 + 7 + 55 x 0.11 = 51.1; the mirror's ask path is the cracker's: S = 5 + 7 + 55 x 0.11 = 18.1; mean 34.6; 28.5 when no figure is kept).

## Pre-ship check

1. Domain: the call stands on each statistic's shift under a missing-not-at-random departure calibrated on a
   gold-standard nonresponse follow-up and carried nonrespondent by nonrespondent on the logit scale (the
   missing-data task type's pattern-mixture delta); with the follow-up's points gap in its place 11 flags change,
   with the allocation's own shift 9: the method, not the education nouns, decides.
2. Two layers: Layer 1 (the paper and online code lists, the crosswalk's reference form, route duplicates, late
   returners in the follow-up sample, the 2026 map) is neutral on the call, each item asserted (R2); Layer 2 is the
   scale of transport, asserted alone to move the default to the golden (R3b).
3. No banned stump decides: nothing is planted (R3c); not semantics (every activity code and band scrambled leaves
   every flag, asserted); not rule application (QS-4 files no scale; the default path executes every filed rule and
   files 11 wrong flags, asserted on the clean truth, R3a).
4. Gate G: no shipped artifact ranks or flags the statistics; the 2025 release table (a distractor) holds 2025 rates
   on the 2025 map.
5. Determinism: the follow-up rejects the pooled and per-band points gaps and ratios (asserted at 8 log-likelihood
   units or more); every model that fits it gives the golden grid with every shift at least 0.29 points from a band
   edge; graded rates sit at least 0.02 from a rounding edge, the odds ratios and slopes mid-bin at two decimals.
6. Asks: A (24 figures) and B (12) are moved by the form-build device in every figure and B by the band device too;
   the call reads neither column (asserted).
7. Input gates: 15 files in four formats, the 2026 frame at 47,734 rows, three distractors named in metadata.json;
   two builds byte-identical; figures_check 57 of 57.

## Leak check

Architecture 1: leak.py REVIEW, no LEAK (--asof 2026-11-10); reader pass 1: Q1 to Q4 none, Q6 analytical, all seven
REVIEW lines harmless; realism notes fixed in the generator (careers counts, the field report's late-form sentence,
school names, QS-4's history line and the "own allocation" phrase). Architecture 2 re-runs both on the new cut.

## Tried and rejected

- QS-4 s.3 saying the sensitivity rate is worked "from that nonrespondent's own allocation" (stage 4, reader Q5):
  read as leaning toward a per-leaver odds or ratio form; cut, the per-nonrespondent grain kept.
- Architecture 1, follow-up in the five middle and deprived districts (built and judged 2026-10-16): SEND_BACK. Inside
  each attainment band its allocations barely varied, so a points gap or a ratio per band fitted the follow-up within
  1 to 4 log-likelihood units of one odds ratio while giving other flags, and the prompt's "rate the release will
  publish" was open for the four suppressed statistics. Re-rooted as architecture 2: the follow-up spans the island's
  range so the data reject every band-level and pooled points or ratio departure, and the headline rate is defined
  whatever the flag.
- Traced districts spanning the whole range in the first prototype (2026-10-16): borrowing the nearest followed-up
  district's band gaps landed 23 of 24 flags; with the affluent extremes left uncovered and every untraced district
  matched by leaver-level allocations, the borrowed gaps now agree with the golden and are an allocation-conditioned
  route to it, not a rung.
- Flags required to agree under a probit or complementary log-log shift (prototype, 2026-10-16): the follow-up
  cannot separate the links in the low-allocation tail and the logit delta is the field's standard for a binary
  outcome; in architecture 2 the probit shift agrees anyway and is asserted.
- Released rates and the follow-up's odds ratios and gaps on a rounding edge (stage 3, 2026-10-16): one or two
  recorded destinations changed between a graded and an ungraded destination (the generator's mid-bin step),
  leaving every shift and flag where it was.
