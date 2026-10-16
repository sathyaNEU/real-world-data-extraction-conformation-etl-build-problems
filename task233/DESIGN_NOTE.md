# task233 design note

Architecture 1 (drawn 2026-10-16), wave 2, seed DQ06 (whether a register statistic keeps its quality flag
when the missing field may not be missing at random): the seed's world, decision and quantity only, the
pitfall re-found from the data under the 10/10 rules. General Statistics & Data Science, missing data,
censoring and measurement error, Data Quality Monitoring & Alerting. The island's Statistics Office
publishes its school-leaver destinations release each December; the head of education statistics signs a
quality flag for each district's NEET rate and higher-education entry rate, judged on how far the rate
would move if the survey's nonrespondents departed from the destination model's allocation as the 2025
nonresponse follow-up found.

## Draw

Card `cards/task233.json` (architecture v1, registered 2026-10-16). Guard verdict WARN, one line each:
`three_rules.strategy_risk` (grain_or_unit) is answered by the analyst test below, which `checks.py` runs on
the clean truth; `overuse.org_family` (government_agency) and `overuse.gate_g` (method_or_model_selection,
5 of the last 12) are accepted because the mechanism, the task type and the forum differ from every
neighbour; `test.same_puzzle_older` (task458) and `test.same_driver_older` (task256, task262, task54) are
differentiated on the card; `driver.near` task446 v2 (0.13) is differentiated on the card (a screen's yield
recovered through error rates, no missing data).

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, serving Data
  Quality Monitoring & Alerting (the domain index lists this task type under DD and DQ).
- **Niche.** The Statistics Office's destinations survey asks every school leaver in October where they
  went; about one in six do not answer. The release allocates each nonrespondent across the five
  destinations in proportion to the respondents of the same district and attainment band (a missing-at-
  random allocation). In 2025 the Office's field team followed up a random sample of nonrespondents in five
  districts and found where they really went. The head of education statistics flags each 2026 statistic
  standard, caution or suppressed on the sensitivity shift the quality standard defines.
- **The call.** For each of the twelve districts' NEET rate and higher-education entry rate (24 statistics),
  the flag: standard (shift under 1.0 point), caution (1.0 to under 3.0) or suppression (3.0 or more).
- **Shape.** 07, a grid of cells, each cell graded. Decision designation_set, answer set_of_items, question
  form which.
- **Strategy.** grain_or_unit with G14 decisive (the departure measured in the followed-up pool does not
  carry as points to every pool) and G17 supporting (each shift judged against the flag bands); Gate G
  method_or_model_selection; calibration gold_standard_subsample; context artifact close_out_summary;
  layer 2 family estimand_identification, pattern general-statistics-data-science/missing-data-censoring-
  measurement-error/3 (delta adjustment for nonignorable missingness).
- **Forum, event, organisation.** committee_or_panel (the release quality panel the head chairs),
  statutory_or_regulatory_filing (the release goes out under the statistics code with its quality flags),
  government_agency.
- **People** (`guard.py names --geo Ireland --seed 233`): Polly Ganley, head of education statistics, who
  signs the flags; Emmett Phelan, field manager who ran the 2025 follow-up; Leanne Henebry, survey
  methodologist who keeps the allocation and the quality standard.
- **Deliverables.** `leaver_destinations_2026_quality_flags.xlsx`: each statistic's flag with its shift,
  and the supporting asks.
- **Data-native sentence.** A nonrespondent's allocation is the respondents' share in its own district and
  attainment band, so allocations run from about 2 per cent NEET (a high attainer in an affluent district)
  to over 40 (a low attainer in a deprived one), and the follow-up found nonrespondents departing from them
  by one factor on the odds (a 3 per cent allocation became about 7 and a 30 per cent one about 52), so the
  same departure is a few points at one end of the island and twenty at the other.

Sources, one line each (what it teaches; how this build differs):
- Client pattern missing-data-censoring-measurement-error/3 (delta-adjust for nonignorable missingness;
  shortcut: complete-case agrees with the imputation, so robust): the frame; here the delta is not swept
  over a grid but calibrated on a gold-standard follow-up and carried to districts it never covered, and
  the shortcut is this build's rung 0.
- Seed DQ06: the world, the decision and the quantity only; its decoy architecture is not used.
- Hansen and Hurwitz (1946), the nonresponse follow-up subsample; Little and Rubin, Statistical Analysis
  with Missing Data, pattern-mixture models; Carpenter and Kenward (2013), Multiple Imputation and its
  Application, delta adjustment on the logit scale for binary outcomes: the field's method. No card or
  ledger row on file carries it.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomisation
  unit), task229 (a daily mean through a convex rating), task230 (net coding bias of a late channel),
  task231 (a rate over units still active, exits reported late), task232 (a transmission rate from delayed,
  mixed outcomes). None carries a missing-not-at-random departure or a scale of transport.
- task446 v2 (nearest driver, 0.13): a screen's yield carried across pools through its error rates; this
  build has no screen and no base rate to recover, the rates are published and the question is how far
  they move under a calibrated departure.

## Default path

1. Read the quality standard: the flag bands on the sensitivity shift (under 1.0 point standard, 1.0 to
   under 3.0 caution, 3.0 or more suppression) and the counterfactual the shift measures (each
   nonrespondent's allocation moved as the 2025 follow-up found followed-up nonrespondents departing from
   theirs, the district's rate recomputed).
2. Conform the 2026 survey file: map school codes to the 2026 districts (two schools moved), count leavers
   and nonrespondents per district, and total each district's NEET and HE allocations over its
   nonrespondents.
3. Conform the 2025 follow-up: join its outcomes to the 2025 survey file through the case crosswalk, keep
   one outcome per case, drop the cases that responded late (they carry a survey destination and no
   allocation in the final file) and map the field team's codes to destinations.
4. Measure the departure the follow-up found: the followed-up nonrespondents' NEET share minus their mean
   NEET allocation, about 17 points, and the same for higher-education entry, about minus 10.
5. Each district's shift: its nonrespondent share times the gap.
6. Flag each statistic against the bands.

Ends on: nine of the 24 flags wrong. It suppresses the NEET rates of Southern Shore, Hill Country, Northern
Plains and Market Towns (the odds scale cautions them), cautions the NEET rates of Upper Valley and Glen
Villages (standard), cautions Mill Towns' NEET rate (suppression) and cautions the HE entry rates of Old
Docks and Mill Towns (standard).

Golden: suppression for the NEET rates of Riverside, City West, City East and Mill Towns; the standard flag
for the NEET rates of Southern Shore, Upper Valley and Glen Villages and the HE entry rates of Old Docks
and Mill Towns; caution for the other fifteen.

## Stump sentence

A competent solver adds the 2025 follow-up's pooled points gap to each district's nonrespondents in
proportion to their share and files nine wrong flags (Ends on: suppression for the NEET rates of Southern
Shore, Hill Country, Northern Plains and Market Towns, caution for Upper Valley's, Glen Villages' and Mill
Towns' NEET rates and for the Old Docks and Mill Towns HE entry rates); the step that lands it there is
carrying a departure measured where allocations are middling as a fixed number of points instead of
leaver by leaver on the odds scale, on which the followed-up districts and attainment bands agree.

## Three rules

- **Task type:** general-statistics-data-science / missing-data-censoring-measurement-error, which serves
  Data Quality Monitoring & Alerting: a published statistic's sensitivity to nonignorable nonresponse,
  judged against a quality flag's bands, the departure calibrated on a gold-standard follow-up.
- **Domain test:** the quantity that decides is each statistic's shift under a departure from
  missing-at-random, the pattern-mixture delta adjustment the missing-data field calibrates on a
  nonresponse follow-up and applies to each nonrespondent on the logit scale for a binary outcome.
- **Swap:** in this domain the setting is another field's and the swap is of the method. Put a generic
  summary in place of the delta adjustment (the follow-up's points gap times the nonresponse share, or the
  agreement between the respondent-only rate and the allocated rate) and nine flags change, or every flag
  turns standard; the call stands on the missing-data object, not on the education nouns. Swapping the
  nouns alone ("hospitals' readmission rates, patients lost to follow-up") keeps the method and is the
  same task, which is what a General Statistics draw is meant to be.
- **Layer 1:** the 2026 survey came back on two form versions with different destination code lists (the
  new form splits NEET into unemployed and inactive and adds a deferred higher-education place), as the
  form change of 2026 produced; the follow-up's outcomes are keyed by the field team's case numbers and
  reach the survey through a crosswalk, with a few cases found by two routes; the follow-up sample was
  drawn from the provisional nonrespondent list, so some cases answered late and sit in the final 2025 file
  as respondents; the district map was revised for 2026 and two schools moved. None is placed to be
  caught, and on the clean truth the default path and the golden are unchanged.
- **Layer 2:** estimand_identification, missing-data-censoring-measurement-error/3: the departure found on
  the follow-up has to be carried to nonrespondents the follow-up never reached, on the scale on which it
  is stable; the follow-up shows one odds ratio across its districts and attainment bands while the points
  gap and the ratio of rates both drift with the allocation.
- **Decisive step:** carrying the follow-up's departure leaver by leaver on the odds scale (the logit
  delta, or any model of the departure on each nonrespondent's own allocation that fits the follow-up),
  because a nonrespondent's allocation runs from 2 to 50 per cent and the follow-up's districts and bands
  agree on the odds ratio, not on the points.
- **Not semantics:** the default path reads every field, code and definition right (the five destinations,
  the two code lists, the allocation columns, the 2026 district map, the crosswalk) and computes the right
  gap; the wrong flags come from the scale the gap is carried on, which no field, code or unit names.
- **Not rule application:** the standard files the bands, the rounding and the counterfactual (each
  nonrespondent's allocation moved as the follow-up found, the rate recomputed); no filed sentence says on
  what scale the departure moves, so executing every stated rule with the gap the follow-up reports still
  files the nine wrong flags.
- **Analyst test:** with every field read and every rule applied, a strong analyst takes the follow-up's
  departure as its pooled points gap (about 17 points for NEET, minus 10 for HE entry), adds it to each
  district's nonrespondents and files the default path's Ends on: nine wrong flags; `checks.py` runs that
  route on the generator's clean truth and asserts it, then changes the scale alone and asserts the golden.
- **Estimand:** the quality standard (filed in the methodology pack) fixes the population (all leavers of
  the 2025-26 school year in each 2026 district, respondents and nonrespondents), the outcome (the NEET
  rate and the HE entry rate as released), the comparison (the released rate against the rate with each
  nonrespondent's allocation moved as the 2025 follow-up found followed-up nonrespondents departing from
  theirs), the unit (percentage points) and the bands.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states a gap, a ratio or
  a flag; the follow-up report gives its design and completion, not a headline departure; no rule is
  withheld and no block is copied; no shipped artifact ranks or flags the statistics.
- **No certified replay:** no certified or published figure exists for the method to reproduce; the
  follow-up's outcomes are field findings per case, and the scale is read from how those findings vary
  with the allocation, not recovered by matching a stated number.
- **Lesson:** a departure from missing-at-random measured on a follow-up transports on the scale on which
  the follow-up shows it constant; for a binary outcome whose allocations run from a few per cent to a
  half that is the odds scale, so one departure moves a 3 per cent allocation by 4 points and a 30 per cent
  one by 22, and a pooled points gap suppresses the statistics least exposed to it. No build on file
  teaches nonignorable-nonresponse sensitivity carried on the logit scale.

## Tried and rejected

- Traced districts spanning the whole range of allocations (prototype, 2026-10-16): borrowing the nearest
  followed-up district's band gaps (an analyst's analog reflex) landed 23 of 24 flags, so the follow-up was
  moved to the five middle and deprived districts and the affluent districts left uncovered at the district
  level while their leavers' allocations stay covered at the leaver level.
- Flags required to agree under a probit or complementary log-log shift (prototype, 2026-10-16): the
  follow-up cannot separate the links in the low-allocation tail, and the logit delta is the field's
  standard for a binary outcome, so the golden corridor is built over the logit-scale estimators (pooled
  offset, fixed-effects logistic, Mantel-Haenszel, band-specific, district-own, free-slope calibration)
  and the probit and quadratic variants are reported, not required.
