# task170 design note: the cases Ruvari County's March 2027 net campaign will avert among the people sleeping under its nets

Architecture 3, a from-scratch rebuild of a reopened number (Forecasting lane, sathya8571), in the cell the main
session assigned: epidemiology-public-health / health-burden-impact-modeling. Architecture 1 (the paediatric ARV
order) is summarised under `## Architecture 1 record`; architecture 2's two cells and the 2026-10-23
expected-credit-loss cell died before any card (`## Tried and rejected`). The setting is fictional throughout: Ruvari
County, its health department, Tulivu Health Partners, the Arnbridge Foundation, Ombeni fever (a mosquito-borne
protozoal fever), its vector *Anopheles ruvariensis*, the KINGA-5 trial and the LulaNet R repellent sleeping net are
invented, and no record is a real place's or a real outbreak's.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task170.json`, architecture v3, v1 moved into `lineage` with its fate.
   `guard.py check` WARN (answered in item 9). Nearest drivers 0.09 (task121 v3, odour complaints against the wind at
   the same clock hours), 0.08 (task474 v2 lineage), none flagged.
2. Pairing: Epidemiology & Public Health (client domain) / `health-burden-impact-modeling` / Forecasting & Predictive
   Modeling (the taxonomy lists the task type under F and OS). The deciding analysis is the impact model's carry of a
   vector-control tool's trial efficacy to a new setting through the share of human exposure to the vector that falls
   while people are in bed under the net. task149 is the one card in the task type (a recordable-injury hazard rising
   with work pace) and is differentiated on the card.
3. Niche: an implementing non-profit's cases-averted forecast for its donor's grant approval of a county-wide
   distribution of repellent sleeping nets (one net to two people, distributed in March 2027), counted among the
   people sleeping under the nets from April to December 2027.
4. Call and shape: the Ombeni fever cases the campaign will avert among net users from April to December 2027, a count
   (`quantity_figure`, how many). Shape `other`: the call with its critical components (the per-bite protection the
   trial's sites share, the county's in-bed share of exposure, the share of the period's cases averted, and the cases
   averted in each sub-county, which inherit the decisive step), and asks on rows the call never reads (the household
   registration, the facility reports, the sentinel catches of the other species). The forecast across months (shape
   `02`) was the first draw and was blocked inside the registration lock by task171's shape 02 and its forcing event;
   criteria are counted in `## Ask sheet`.
5. Mechanism keys: gap population (the trial sites' exposure against the county's), then time (the hour each bite
   arrives against the hour each person goes to bed); pattern none; generators G7 (the operating window: a net stops
   only the bites that arrive while its sleeper is in bed under it), G14 (the trial's pooled efficacy does not carry
   to this population); Gate G `forecasting`; strategy `causal_design`, read as transportability (the card's notes
   say why, and that `composition_mix`, in the ban window, also describes it); Layer 2 family `field_method`, pattern
   `own:protective-efficacy-carried-through-the-in-bed-share-of-exposure`.
6. Default path's answer against the golden: the trial's pooled protective efficacy (56.7 per cent) applied to
   the plan's expected cases among users files 22,000 cases averted; multiplying that efficacy by the county's
   in-bed share of exposure, without dividing out the sites' own share, files 8,000; the golden, the per-bite
   protection the five sites share (0.80) carried through the county's in-bed share (0.36), files 11,000 (11,208
   unrounded), 21 per cent of the 53,494 cases the county expects.
7. **Data-native sentence.** The county's vector bites from dusk and peaks before most people are in bed, half its
   bites land outdoors where the evening is spent, and the KINGA-5 sites' vectors bit after midnight indoors, so a
   net that stops about four in five of the bites that reach its sleeper stopped most of a trial participant's
   exposure and will stop well under half of a Ruvari resident's; the landing catches by hour and position and the
   behaviour survey's clock times are the only records of that overlap, at a grain the trial's headline efficacy
   does not carry.
8. Sources, one line each. `layer2-rigor-patterns.md` health-burden cards 1 (the reference life table for YLL) and 2
   (a potential impact fraction from the shifted exposure distribution, not a scaled PAF): card 2's shortcut is the
   default path's family (a headline effect scaled by coverage), and the judgment beyond it is what the trial's
   effect is a measure of, which the data settle through the five sites. Infectious-disease cards 1 and 2 (Rt and the
   next-generation matrix) are not used: the estimand counts personal protection among users and no transmission
   feedback. task149 (same task type, a hazard read within each unit against pace), task177 (an effect read at the
   point of each unit's own cycle) and task172 (a deadline's bite moving with a step) were read for their drivers and
   differ in the structure carrying the call (card `differentiation`). The seed FC41 is not used.
9. WARN answers. `repeat.gate_g` and `overuse.gate_g` (forecasting in 5 of 12, beside task175 and task171): the objective is the
   lane's; the mechanism is not task175's (a vacant lot's chance read at its street's build-out). `repeat.decision`
   (quantity_figure beside task175): the call is a count of cases averted, the decision's own unit.
   `repeat.deliverables` (xlsx plus png): reviewed at stage 3 against the deliverable a donor's impact forecast
   takes. `repeat.question_form` (how-many, beside task175 and task171): a count asks how many.
10. People (`guard.py names --geo Kenya --seed 170`): Dorcas Kagwiria (monitoring and evaluation lead, Tulivu Health
    Partners), Elkana Karanja (county vector-borne disease control coordinator), Amos Simiyu (county entomologist).
    None appears in the prompt.
11. Furniture: forum `funder_or_donor` (the Arnbridge Foundation's grant approval), forcing event `budget_or_appropriation`
    (the grant that funds the March 2027 distribution; `launch_or_rollout` was the first draw and task171 holds it in the
    window), organisation family `nonprofit_or_charity`, role family `programme_officer`,
    context artifact `other` (the KINGA-5 trial report), calibration form `other` (the trial's five site results).

## Default path

The route a competent burden modeller takes from the prompt and the pack, every field read and every filed rule applied:

1. Take the campaign's population and window from the plan's impact sentence (residents under a campaign net, April
   to December 2027) and the expected cases by sub-county and month from obf_planning_baseline_2027.xlsx.
2. Take the planned use by month from Table 2 of the plan, so the cases the users would have had are the baseline
   times the use: 40,140 cases.
3. Take LulaNet R's protective efficacy from the KINGA-5 report: the pooled 56.7 per cent of Table 1, the trial's
   primary result across five sites and three countries, with nightly use verified.
4. Cases averted are the users' expected cases times the efficacy, by sub-county and month, summed.

Ends on: 22,000 cases averted (22,121 unrounded), 41 per cent of expected cases.
Golden: 11,000 cases averted (11,208 unrounded), 21 per cent of expected cases.

## Stump sentence

A competent modeller applies the KINGA-5 pooled protective efficacy of 56.7 per cent to the plan's expected cases
among net users and files 22,000 cases averted against 11,000; the step that lands it there is carrying an efficacy
measured where most bites arrived after participants were in bed to a county whose vector bites early in the evening
and half outdoors, where 0.36 of a resident's bites arrive in bed against 0.49 to 0.96 at the trial's sites, so the
per-bite protection of 0.80 that every site shares reaches far less of a Ruvari resident's exposure.

## Three rules

- Task type: epidemiology-public-health / health-burden-impact-modeling, which serves Forecasting in the taxonomy:
  the cases a vector-control campaign will avert over a window not yet open.
- Domain test: the deciding quantity is the campaign's protective effect carried from the trial to the county through
  the share of human exposure to the vector that arrives while people are in bed under the net, built the way
  vector-control impact models carry trial efficacy, from human landing catches by hour and position against a human
  behaviour survey; nothing in it reads with hospital or school nouns, because it is a vector's biting rhythm against
  people's sleeping hours.
- Swap: "how many readmissions will the discharge calls avert among the patients called in 2027" keeps the
  coverage-times-efficacy arithmetic and loses everything that decides here: there is no hourly exposure that the
  intervention covers only while people are in one place, and no trial whose effect is that overlap at its own sites.
- Layer 1: the entomology unit's catch sheets change hour-label format twice (24-hour ranges, a 12-hour clock in two
  sub-counties' 2024 sheets, compact ranges from the July 2025 tablet app) and position labels once, carry absent and
  relieved collectors and other species in the same rows, and record a village under its sub-county on the night;
  the behaviour survey holds enumerators' clock times in three formats and revisits a third of round 1's households;
  the trial's tables sit inside a PDF; the registration app replays records and its mop-up re-registers households
  under new numbers; the KHIS export keeps each return under the hierarchy it was entered in, re-entered the realigned
  ward's June returns, and the parent hospitals' returns carried their outreach clinics to March 2026. Each is what
  the system writes; none is placed to be caught, and none moves the call (`generator/checks.py` R2 rows).
- Layer 2: family `field_method`. The choice that flips the call is reading the trial's efficacy as a per-bite
  protection times its sites' in-bed share of exposure, which the five sites' tables show, and carrying the
  protection, not the efficacy, to the county's own in-bed share.
- Decisive step: transport the protective efficacy through the proportion of exposure occurring while in bed, the
  sites' and the county's, each built from hourly biting indoors and outdoors and the population's hourly location.
- Not semantics: every term is read correctly on the default path (the population, the window, the baseline, the use,
  the efficacy as the report defines it), and it still files 22,000, because no field, code, unit or definition says
  that the efficacy is a property of the sites' biting and sleeping hours; the vector species, the hour labels and the
  survey times converge under every reading (SF5, SF7, R2 rows).
- Not rule application: no filed rule or procedure computes the cases averted, so executing every stated rule (the
  plan's population, window, baseline and use; the report's efficacy) files the default path's 22,000. The enumerated
  family of overlap constructions (in-bed share with outdoor exposure, indoor-only in-bed share, indoor share, a fixed
  22:00 clock, the nearest site, the trial efficacy alone or times the county's share) spreads 7,960 to 22,121; the
  standing family, the constructions that carry the per-bite protection through the in-bed share with outdoor exposure
  counted, by five estimators of the protection and two readings of the survey, spreads 11,170 to 11,230 (0.54 per
  cent), and what rules the rest out is the sites' own efficacies, whose ratio to the in-bed share holds at 0.77 to 0.85
  while the indoor-only ratio runs 0.71 to 0.92 and the indoor ratio 0.71 to 0.80 across the sites.
- Analyst test: a strong analyst who cleans the catches and the survey, reads the plan and the report correctly and
  applies the trial's pooled efficacy to the users' expected cases files 22,000 cases averted (8,000 if it multiplies
  that efficacy by the county's in-bed share without dividing out the sites'), against the golden 11,000.
- Estimand: the plan (lulanet_r_distribution_plan_2027.docx, section 5) files the population (residents sleeping
  under campaign nets, no others), the outcome (Ombeni fever cases averted), the window (April to December 2027), the
  comparison (the county's 2027 planning baseline without the campaign) and the use (Table 2); the prompt fixes the
  unit and the rounding.
- No decoy: nothing is planted. The KINGA-5 pooled efficacy is the trial's correct primary result, no document applies
  it to Ruvari or argues for it, no memo, draft or stakeholder figure carries any cases-averted number, and no file is
  copied or backfilled.
- No certified replay: no certified or published figure is reproduced to recover a method; the trial's five site
  efficacies are outcomes of the per-bite protection at five overlaps, read forward, and nothing in the pack certifies
  a cases-averted figure.
- Lesson: a trial's efficacy is the effect of a tool in its sites' exposure pattern, and carrying it to a population
  whose exposure arrives elsewhere in the day means dividing out the sites' pattern before applying the target's; no
  build on file teaches an effect read through an hourly overlap of two independently measured rhythms (task177 reads
  an effect at the point of a unit's own cycle; task149 a hazard against work pace).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 trial pooled efficacy | the report states it as the primary result | Table 1 | coverage times efficacy | none | no | one product | readable |
| R1 pooled efficacy times the county's in-bed share | no | hourly tables invite an overlap | a correction for local biting | none | no | one product | readable |
| R2 nearest site's efficacy | no | five site rows | analogue site | none | no | a lookup | readable |
| R3 indoor-only in-bed share | no | indoor catches | the entomologist's in-bed share of indoor biting | none | no | no | readable |
| R4 decisive: per-bite protection through the in-bed share with outdoor exposure, sites divided out | no sentence names the overlap, the protection or the division | no column holds a share or a protection; the overlap needs catches by hour and position against survey times at a person grain | the textbook carries the efficacy | the site efficacies refute R3 and R4 only once each site's share is built | no | a ratio of two sums over hours in two files | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | cases averted "among the people sleeping under them" | residents under a campaign net only | community or non-user effects added | larger | plan section 5: "It counts no cases averted among residents who are not under a campaign net" |
| SF2 | "from April to December 2027" | the nine baseline months | calendar 2027 | larger | the prompt and plan section 5; the baseline covers April to December only |
| SF3 | the cases the county "would otherwise expect" | the planning baseline without the campaign | a trend fitted to KHIS | other | plan section 4 and the baseline's title line |
| SF4 | how many sleep under the nets | Table 2's planned use by month | the registration's nets times two | other | plan section 5: "at the use in Table 2" |
| SF5 | the vector | An. ruvariensis | every anopheline | same call (11,000) | data dictionary and trial report; asserted |
| SF6 | the efficacy the trial measured | the report's one efficacy per site, nightly use verified | intention-to-treat against per-protocol | same call | the report reports one efficacy, use at 96 to 98 per cent of checks |
| SF7 | the share at an hour | members indoors and in bed at the half hour, as the report's Table 3 | the share of each hour spent | same call (11,170) | asserted |
| SF8 | which survey round | both rounds pooled | one round, or revisited members once | same call | asserted |
| SF9 | landings per hour | per minute collected | per collector-hour row | same call | asserted under R2 |
| SF10 | rounding path | unrounded by sub-county and month, rounded once per figure | sub-county figures rounded then summed | same call | prompt's rounding sentence; asserted |
| SF11 | the per-bite protection's estimator | inverse-variance fit through the origin | unweighted, ratio of pooled, mean of ratios, with an intercept | same call (11,208 to 11,230) | asserted |
| SF12 | case definition | confirmed cases in the baseline and the trial | clinical cases | same call | baseline title and report design; asserted |

## Ladder

| Rung | Construction | Cases averted | Rounded | Clearance from the golden's bin |
|---|---|---|---|---|
| R0 | trial pooled efficacy 56.7 per cent on the users' expected cases | 22,121 | 22,000 | 1.92x |
| R1 | pooled efficacy times the county's in-bed share 0.36 | 7,960 | 8,000 | 1.32x |
| R2 | the nearest site's efficacy (Kibondeni, share 0.49) | 15,226 | 15,000 | 1.32x |
| R3 | per-bite protection through the indoor-only in-bed share (0.45) | 14,316 | 14,000 | 1.25x |
| R4 | through the indoor share (0.50) | 14,041 | 14,000 | 1.22x |
| R5 | through the share of bites after a fixed 22:00 | 12,165 | 12,000 | 1.06x (ruled out by the survey's own bedtimes: children are in bed before 22:00 and members indoors awake or outdoors after it) |
| golden | per-bite protection 0.80 through the in-bed share 0.36 with outdoor exposure counted | 11,208 | 11,000 | edge 292 |

Position: the default path is the largest figure; every correction short of the decisive one lands in its own bin;
the golden is bracketed (R1 below, R2 to R5 above). Worth: the decisive step moves the call 49 per cent off R0.
The trial's draw is the shipped pack's (the generator's TRIAL_SEED): among 400 draws of the five sites' outcomes at
the same per-bite protection, it is one of the 46 in which every estimator of the protection agrees within 0.8 per
cent, so the standing family is closed on this pack; across draws the through-origin estimators stay within 1.5 per
cent of each other and the intercept fit wanders, which is why the intercept fit is asserted on the shipped draw.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | residents under a campaign net | plan section 5 (SF1) |
| 2 | Unit of account | cases | the prompt |
| 3 | Attribution window | the case's month in the baseline | C1: the baseline is monthly; the plan's months |
| 4 | As-of dating | the pull of 12 October 2026 | dictionary header; no figure moves with it |
| 5 | Version basis | plan v2.1, baseline run of 14 September 2026 | one version ships of each |
| 6 | Denominator | the share's denominator is the period's expected cases | the prompt's "cases the county would otherwise expect in that period" |
| 7 | Weighting | the overlap weights hours by landings; people equally | C1: survey members equally (SF8), estimators agree (SF11) |
| 8 | Window length | catches 2024 to 2026, both survey rounds | C1: every round and the pooled read agree (SF8) |
| 9 | Boundary inclusivity | a member is in bed at the half hour from the bedtime | C1 (SF7) |
| 10 | Rounding path | rounded once per figure | SF10 |
| 11 | Tie-break | none needed | no tie at any bin |
| 12 | Maturity and censoring | none: the baseline is complete for the window | not applicable |
| 13 | Order of operations | protection times share times use times baseline | commutative products |
| 14 | Row order | none | sums and means |
| 15 | Duplicate resolution | revisited survey members kept as second nights | C1 (R2 row) |
| 16 | Identity normalisation | the five sites by name across Tables 1 to 3b | one spelling |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | landings per minute in every hour | SF9 |
| 19 | Code and status semantics | IN and Indoor, OUT and Outdoor; three hour-label formats | dictionary; C1 (R2 rows) |
| 20 | Integerisation | none on the call | not applicable |
| 21 | Clause scope | the plan's section 5 governs the grant report's figures, the realignment sentence its sub-county figures | plan section 5 |
| 22 | Forward window contents | the baseline and the use for every month of the window | both ship for all nine months |

## Literal reader

Executed word for word, the prompt and the plan fix the population, window, comparison and use, and the report's one
efficacy per site; the literal reading that carries the report's pooled efficacy unchanged is the default path's easy
method on the same literal estimand (22,000), not another reading of a term, and every term's alternatives converge
or are ruled out by a quoted sentence (SF1 to SF12). Pass.

## Oracles

None ties only under the golden. The trial's Table 1 confirms every site efficacy on every path; the baseline and the
use are inputs on every path; no published cases-averted figure ships. The site efficacies refute the indoor-only and
indoor overlaps only after each site's share is built, which is the decisive step itself.

## Ask sheet

Asks, each on rows the call never reads (separation asserted in `checks.py`: the call's code reads no registration,
KHIS or facility file).

- Ask A, nets by sub-county (7 figures, whole numbers). H18 home: the procurement line of the grant case. Path:
  nets_registration_2026.parquet (16 columns), the plan's allocation rule. Primary device (D1, the same records under
  two keys, silent): the October mop-up re-registered 7,203 main-round households under new registration numbers,
  usually under another member's name and a different or missing ID; the same household shows only as a mop-up row
  matching a main-round row on its ward, dwelling mark, usual members, under-fives and sleeping spaces, while 11 per
  cent of dwellings hold two or three genuine households that never match on all three counts (so a dedup by dwelling
  mark deletes real households). Hazards: exact sync replays (battery), the cap of four nets. Stops: every row
  575,791; replays dropped 574,079; same-ID re-registrations dropped 571,208; one household per dwelling 488,073;
  golden 555,968. Realism: a registration app's sync replays and a mop-up round that re-registers households whose
  slip was lost are what campaign registrations produce.
- Ask B, confirmed cases January to September 2026 by sub-county (7 figures, whole numbers). H18 home: the reported
  burden behind the grant case. Path: khis_moh705_obf_2024_2026.csv (11 columns), facility_list_2026.csv, the plan's
  realignment sentence. Primary device (D6, a rollup above its parts, silent): each sub-county hospital's January to
  March 2026 returns still carried its outreach clinic's outpatients while the clinic reported under its own code from
  January, so the clinic's cases count twice; the only trace is a terse comment on the parent's rows and the facility
  list's parent code. Hazards: the export's sub-county is the hierarchy at entry (D2, the realigned Lwala ward's
  facilities sit under Kendagi to June 2026), and the ward's June 2026 returns were re-entered under Oyamo in July
  (battery). Stops: export column, every row 39,960; facility list, every row 39,960 (other split); June once 39,791;
  golden 39,331. Realism: a KHIS export keeps each value under the org unit it was entered against, and satellites
  coming onto their own codes are entered by both parent and satellite until the next data review.

Measured by: generator/ceiling.py

| Ask | Cracker (lands the call, runs the battery, applies the plan's rule and boundaries) | Figures kept | Verdict |
|---|---|---|---|
| A nets by sub-county | drops replays and same-ID re-registrations, keeps the rest | 0 of 7 | miss |
| B reported cases by sub-county | maps facilities to the realigned sub-counties, counts June once, keeps the outreach double count | 0 of 7 | miss |
| call construction (share and sub-county averted) | on the call | 8 of 8 | yes |

Mirror leakage: 0.0 per cent of ask weight (the mirror stops at R0 and takes both asks on their natural reads).
Pair ceiling: 38.5 ((65.0 + 12.0) / 2 on 38, 7 and 55), 47.2 if the cracker also reads the outreach comment.

## Leak review

`leak.py --asof 2026-10-12`: REVIEW, no LEAK. Each line answered:
- kinga5_final_report_2024.pdf carries 56.7: the trial's pooled efficacy is its primary result and the default
  path's input, stated where a trial report states it; it is a step figure, not the call.
- lulanet_r_distribution_plan_2027.docx shares the call's words (campaign, cases, nets, April to December 2027): the
  plan files the estimand (section 5) in the organisation's words; it carries no figure, efficacy or method.
- The trial report and the plan each carry four of the note's stump-paragraph terms (efficacy, pooled, survey,
  report; survey, report, register, catches): ordinary words of a trial report and a campaign plan; neither names
  an overlap, a share of bites in bed, a per-bite protection or a transport (`checks.py` R1 and R3c rows).

## Duplicate check

`guard.py heart task170` (2026-10-23, after the final pull): WARN, the five WARNs answered in `## Draw` item 9;
nearest text 0.05 (task121 v3). `guard.py surface task170`: one pair promoted, task168 against task170, two numbers
apart, on the decisive gap (population) and the decision type (quantity_figure), surface 0.080 (corpus percentile
46). Both axes are the honest labels here and both are broad; the mechanisms share nothing: task168 completes the
demand of units observed only until they reached a cap from the build of units that never did, while this build
carries a trial's efficacy through the hourly overlap of a vector's biting and residents' hours in bed. The trial's
site names were renamed once (a site whose name read as a person beside the next column) so the persona sweep reads
only the card's people.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Neutral |
|---|---|---|---|---|
| hour labels in three formats | paper sheets keyed by two teams, then the tablet app | hlc | dropping the 12-hour sheets | same call (R2) |
| IN/OUT against Indoor/Outdoor | the tablet app from July 2025 | hlc | splitting positions four ways | asserted labels |
| absent and relieved collectors | the field supervisor's sheet | hlc | counting rows, not minutes | same call (SF9) |
| other species in the rows | the catch sheet | hlc | pooling anophelines | same call (SF5) |
| village under its sub-county on the night | the sheet header | hlc | none on a county figure | not read |
| three clock formats | enumerators | survey | none once parsed; all unambiguous | asserted parse |
| revisited households | the round 2 design | survey | counting members once | same call (R2) |
| tables inside a PDF | the trial's report | trial | none | verifier reads it |
| sync replays, mop-up re-registrations | the registration app, CHVs | registration | ask A device | ask only |
| hierarchy at entry, June re-entry, outreach in parents' returns | KHIS, the records office | KHIS | ask B device | ask only |

## Architecture 1 record (spent 2026-10-18)

Architecture 1, wave 7 (new), Forecasting lane (sathya8571), numbered from seed FC41. The seed (a national Central
Medical Stores filing its order of the adult first-line pack, tenofovir, lamivudine and dolutegravir in one tablet
(TLD), for the January to June cycle C7 at the quantification review, while the children of a paediatric scale-up five
years ago grow into it) was read at its header and Situation only. Its world, decision and quantity are kept. Its
mechanism (a certified cohort model and a register read off one field) is not used: no document vouches for any
model, the paediatric register ships as honest data, and the SOP's stock-out wording is replaced by a filed maximum
stock level so no distribution-against-mean step can decide the call. The pitfall is re-found from how a child moves
onto TLD: at the first clinic weighing that reads 30 kg or more, while a single clinic weighing scatters more than a
kilogram either side of the child's own growth line and the line rises about a fifth of a kilogram a month.

The country is fictional and never named in the pack: a southern African ministry of health whose Central Medical
Stores (CMS) buys antiretrovirals for a national programme of about 310,000 adults on TLD and 12,000 children on treatment,
in US dollars, every product on a six-month cycle (C7 is January to June 2027). The TLD order has two lines (SOP QP-04
4.3): line 1 for the patients of the programme's projection, net of the stock and the lots on order, and line 2,
funded by the paediatric grant, for the children under 15 at the count in the paediatric and adolescent ART register.
The register holds every child's clinic visits, weighings and regimens since January 2023: children diagnosed in
infancy (born 2005 to 2026, fewer each year as PMTCT improved) and the 2021-22 catch-up campaign's children (born 2011
to 2018, diagnosed at three to ten, the more stunted and the slower growing the older they were found). The 2026
edition of the national guidelines, effective 1 March 2026, lowered the weight from which a child takes TLD from 35 kg
to 30 kg and gave children who are well two or three months of medicines at a visit; by the 31 August count most
stable children were on two or three months.


The full architecture 1 note (default path, ladder, closure, asks and the stage 4 repair) is in git at f7ff3fb2.

## Tried and rejected
- A national adult forecast left to the solver (consumption trend or the cohort model of the seed): the adult projection's own spread swamps the children's wave, so no estimator family agrees to a step of the order; the adult part is filed as the programme projection.
- The children's growth on reference centile curves (CDC-shaped weight-for-age) as the truth: per-child functional forms fitted to scattered weighings disagreed by more than a step; growth is straight in kg from age six in this world, and the pooled weighings show it.
- A transient dolutegravir supply constraint as the driver: a dated cause whose effect is a step in the switch series, read off the date.
- An adult nowcast of undetected exits filled by multi-month dispensing: the driver of task231 again, and the adult trend is immune to it.
- A report-back device on the call's own rows: banned by the separation line.
- The wave's peak inside the window (the 2015-16 cohort born half a year earlier): every estimator agreed, but the trailing switch count and its linear trend landed inside the golden's step; the cohort was set later so the window holds the rise.
- Twelve-month per-child growth fits as the golden family's member: on scattered weighings their slopes carry so much error that the first passage is overstated by about a sixth in the forecast and by 30 to 50 per cent on every closed window; the family is the fits on each child's whole register history, which the closed windows validate within five per cent.
- A chart of the national months of deliveries and dispensing labelled at its peak: the peak month was a figure the cracker landed; the chart carries the table's 24 figures by region.
- Reissued codes closing in December 2025: the cracker's region route cancelled across the two cycles and kept Capital C5 and Central C5; the closures moved to March 2026 with larger, varied sites.
- A rival list that included the pooled-velocity and shrinkage constructions as members of the golden's family: after the infants' scatter fix they spread the family over 4,700 bottles, the 29.95 kg member four bottles inside the step's edge; each under-forecasts every closed window by 9 to 24 per cent while the register measures the slopes' spread between children, so they are reported as decisive-step routes, not members, and the step is centred on the per-child family.
- The empirical Bayes member with the between-child variance from unweighted moments: on this register it comes out at zero and shrinks every child to one mean slope; the DerSimonian and Laird estimate stands beside it, and both fail out of sample.
- The same scatter for an infant's weighing as for a 25 kg child's: readings under 3 kg and one below zero; a reading's scatter and clothing allowance shrink below 15 kg (an infant scale), which moved no switch and lowered the pooled scatter from 1.31 to 1.28 kg.
- New sites' customer accounts opened after their first delivery, and opening stock signed for before the registry's opening date: accounts now open two to six weeks before a site opens and its opening stock arrives on the day it opens.
- Other products' eLMIS lines with a loss larger than the stock on hand: the balance identity broke on 12 lines; the loss is capped at the stock.
- "Bottles it allows for patients aged 15 and over" as one figure: a reader could leave the maximum stock out of it; consumption and maximum stock are asked apart.
- Back-test percentages for every rival in the write-up: the band and trailing-count constructions vary with the bin and window a reader picks; the write-up bounds only the golden and the growth line.
- A delivery picked from two batches split on two different draws: its two lines summed to more or less than the quantity the facility received, so CMS's deliveries and the facility's eLMIS receipts disagreed on every such delivery; the split now shares one draw (the stream of later draws kept), which moved the asks' delivery figures and nothing the call reads.
- A family placed on its single choices' midpoint: two upward choices made together (the 29.95 kg threshold with 24-month lines) then sat 58 bottles inside the step's edge; the step is now centred on the span of the members and of the two compound choices that push the need furthest up and down.
- The whole C7 order at the nearest 5,000 bottles as the call (stage 4, round 1): the judge found the step unforced (the textbook per-visit prediction variance crossed its edge by 380 bottles, 24-month lines with it and the shrunk slopes by more), and the audit found the children's part 0.93 per cent of the order; the call moved to line 2, the children's part as its own line, in whole pallets.
- The repaired register with paediatric multi-month dispensing from July 2024 (most stable children on three months for two years): the lever between the growth line and the golden fell to 4,000 to 5,000 bottles while the family, with the prediction-variance and shrinkage routes in it, spread over 3,300, and the register's band rates, band chain and trailing counts sat inside any rounding wide enough to hold the family; the rollout moved to March to August 2026, with the guidelines.
- A stationary register with TLD at 30 kg throughout: every history-based route (band rates, the band chain, the trailing counts) measured the same flow the golden forecasts and landed in its pallet; the 2026 edition's change from 35 kg follows the WHO update of 2021 that many programmes adopted late, and it makes every rate measured on the register's history a rate of a band no longer in force.
- Line 2 rounded to 5,000 bottles with every prediction-variance construction in the family: the per-visit prediction variance on 24-month lines sits 2,271 bottles above the golden and the shrunk 24-month plug-in 813 below, so no 5,000-bottle step holds both a quarter step and one sigma from its edges; the order is placed in pallets of 84 cartons of 96 bottles, and a pallet holds them.
- The paediatric line the moving children leave (ABC/3TC with DTG 50 mg, 20 to 29.9 kg) as the call: its inflow at 20 kg is dosed visit by visit, so the noisy first passage moves only its outflow, the lever is the same number of child-months as on the children's TLD line, and the line carries two transitions to forecast.
- The children who move onto TLD in the window as the line alone (about 16,000 bottles): a pallet is half the line, so the call would be two pallets against one.
- A season of 0.2 kg peaking in May, and a velocity ramp from 2 to 6 years: windows opening at the season's peak under-forecast by a fifth on every route, and the all-weighings lines of 9- and 10-year-olds under-projected their June weight by 0.3 kg; the season is 0.08 kg peaking in September and growth is the child's own line from five and a half.
- The campaign's size changed by redrawing the world: every child's draws moved with the size and the family's centre jumped; every child of the campaign's largest size is drawn and the first 7,040 kept, the size set so the family's centre sits at the pallet's.
- The scatter of a 10 to 15 kg child's weighing shrunk like an infant's: the pooled scatter fell below the near-band children's by 0.07 kg and the MAD member drifted; infant scales stop at 10 kg.
- A crossing-age rule left out of the asserted misses: 11 of its 24 binnings, those that move every child already past the crossing age at the next visit, land in the pallet; they are reported, and the binnings that wait for each child's age are asserted to miss.
- The whole C7 TLD order as the call: the children's switch timing moved it by under 1 per cent (the default 25,000 bottles short on 2.69 million), so the 5,000-bottle step was finer than the estimator family could hold and the lever was immaterial to the order.
- Line 2 in whole pallets (8,064 bottles) as the call: the lever between the default and the golden is 1.03 pallets, so the default misses by one pallet and P(both) is about 0.2, twice the bar; routes that land the pallet without the decisive step include a chosen lead of 3 to 6 months, a margin of 0.75 to 1.25 kg, the last weight at 28 kg, age 12 with the backlog and a weighing every month; architecture 1 is spent on strength and the number needs a re-root.
- Architecture 2 in pharmacology-pharmacoepidemiology-safety / population-pharmacokinetics-exposure-response (2026-10-19, never carded): twenty in-cell candidates screened before any card, every one in one of four graves (a filed pharmacokinetic formula executed: renal scaling, accumulation, Michaelis-Menten, weight-band edges, design and sample-size calls; a fit whose estimator family forks the graded figure: covariates inside the NLME, effective half-life on sparse troughs, a ceiling-censored Emax, variance components; the field's textbook route as the golden: actual dosing histories, within-patient trajectories, dialysis calendars, covariate-vector resampling, per-patient rates for an extended interval; or a reading or a rejected shipped number: unbound fraction, eta-shrinkage off a shipped post-hoc table, BLQ hiding the bottom), with the confounded exposure-response card blocked as `causal_design` by the window and the dose-level IOV call at 11 to 25 per cent against a 30 per cent bar. It is the verdict task171's own screen recorded for this cell (`task171/DESIGN_NOTE.md` line 42); the full table is in the build's scratch `r170/STATE.md`. The cell is spent for this slot.
- Architecture 2 in banking-credit-financial-risk / deposit-liquidity-behaviour (2026-10-19, never carded): composition is the deposit field's native mechanism and `composition_mix` is out this round (task137 and task166 drew it; three of the four banking forecasting builds on file carry it), so every heterogeneity candidate died on the ban (surge layers, hot against core money, primary relationships, dormant accounts, holder age, product migration, a relationship-tenure clock, burnout of rate-sensitive savers, the last two `population_selection` besides). The cards' own methods are the textbook route the readers take (cumulative and asymmetric betas, with level dependence in card 2's own note and the error-correction lag in card 1's "lagged repricing"; cohort decay; first cumulative breach; behavioural maturity), and the bank's own pricing reaction recovered from its history (funding need, a swap ceiling) is a withheld rule.
- Deposit cell, the rest: floors, notice periods, payment limits, insured-limit aggregation, early-repayment schedules and product terms are rule application or a reading, and the unconstrained periods hand over the floor-free beta; net against gross runoff is task89, a left-truncated cohort after a migration task133, loan-linked and refinance-ability exits task166, maturity retention task137, in-flight transfers by provider route task181, shared collateral across funding sources task106 and a rival-level crossing task115; lumpy repricing moves about 5 per cent of the expense and a hold on the core share fails the variance-only screen.
- Deposit cell, the three drafts scored with `guard.py nearest` (0.06 to 0.07, none flagged by text): re-timing the outflow on each saver's own notice for a cut notified to everyone on one day is task162's insight (a forward trigger alignment no recorded instance had, so the record's weekly profile understates the peak); a leaving hazard set by the interest given up (balance times gap) against a fixed bother of moving reads the same as any switching-cost churn, and its forward cell is either in the record (one balance-by-gap table lands it) or empty only by a selection that is composition; topping up to a raised deposit guarantee limit from the bunching at the old one is the public-finance bunching estimator (the swap test reads it as tax kinks) and its response rests on one past limit change.
- Rebuild of 2026-10-23 in banking-credit-financial-risk / expected-credit-loss-provisioning (never carded), the one candidate taken to code: a credit union's CECL allowance on its auto loans after a used-vehicle price surge, each defaulting loan's recovery forecast as its own vehicle's market value at its sale against a balance sized at its own purchase market, so the record's severities (vehicles bought at or below the market they sold at) carry nothing to the vehicles bought at the top. On the clean truth (40,655 open loans, 7,947 closed sales, three seeds) the golden family (five fits of resale over purchase price on the index at sale against the index at purchase, the ratio's coefficient free or fixed at one, point, smeared and residual-integrated) sat within 1.1 per cent of the truth and the rivals missed by a third or more (pre-surge severity 33 to 34 per cent low, the latest year's recovery rate scaled by the forecast index change 39 to 44, pooled severity 47, a valuation on the purchase price without the purchase market 64). It died on the shipped-proxy screen: the practitioner's macro-linked severity, the recovery rate regressed on the index's change over a holding horizon, filed 4.6 per cent high on a 12-month change where the fall sits in the forecast and 7 per cent low on a 24-month change where the fall comes before the report, because for loans that default 12 to 24 months after purchase the index's change over that horizon is the purchase-to-sale ratio; the horizon is a free knob whose range spans the golden, so some member lands in any world. A hedonic valuation on the vehicle's segment and age with no price information also landed (2 to 8 per cent high), and with the fall before the report the surge vintages' own realised severity shows the effect.
- Expected-credit-loss cell, the rest on paper: rate resets and interest-only, promotional and grace-period expiries (task166's due units, task177's exposure end, task46's and task157's cohort crossing a step); a collections, extension, repossession or court-order change that closes one route for distressed loans, and negative equity routing distressed borrowers into default instead of a sale (task169's driver both times); drawdown before default capped by the limit (task168's cap completion); cure, re-ageing and delinquency momentum (conditioning on the account's own history is a stratification, the opponent's first group-by, `stumping` Part 6); guarantees, first-loss covers, forward-flow debt sales, deficiency and repossession statutes, the CECL collateral-dependent expedient and line-freeze policies (each a filed rule executed); indexed mortgage loan-to-value (the field's own indexation is the textbook route); a distributed lag from a county panel (the field's lag reflex, task160's readers landed a lag, and it moves only a 12-month window under staging rules); a cut in the state's unemployment-benefit duration turning more job losses into defaults (task172's cap moving into the bulk of a duration distribution, the exceedance share read straight off the record's spells); sector-linked defaults at a select-employee credit union and a sponsor's plant closure (composition, the metro or sector forecast a proxy or a signpost, the closure a dated cause); dealer price packing, electric-vehicle depreciation and force-placed insurance (each a column to stratify on); a retained first-loss tranche (its expected loss turns on the spread of ten vintages' losses). The cell's core estimation mechanics (survival to date, competing exits, the remaining-life base) are task133's.
- Architecture 3 (epidemiology-public-health / health-burden-impact-modeling, the LulaNet R campaign's cases averted through the in-bed share of exposure) spent at Gate F at stage 4 on zip 74728781: the judge returned DETERMINISTIC / APPROVE with no fix, and blind reader A took the decisive step in its own words ("net protection only works while the person is in bed, so for each KINGA-5 site I computed the share of person-exposure to An. ruvariensis bites that falls in bed (survey in-bed/indoors by half hour x hourly indoor/outdoor landing rates). Trial protective efficacy divided by 0.97 net use, regressed through the origin on that share gave per-user efficacy = 0.824 x share in bed"), filing 12,000 against 11,000 and 22 against 21 per cent with 6 of 7 sub-counties landed (score_reader FAIL as landed), and took ask B ("outreach clinics' Jan-Mar 2026 rows dropped because parent hospitals' Jan-Mar returns already include outreach OPD"), 7 of 14 ask figures. Why: the trial report shipped each site's hourly biting and sleeping tables beside its widely varying efficacies, which laid the transport model out on one page, and a behaviour-time overlap is the field's standard entomological reasoning for nets, so it fails the library test at medium effort; an in-row comment is no silent device.

## Retired

task170 retired on 2026-10-19 under the author's rule for this round (a number that dies in its second new cell retires),
every card kept. Architecture 1 (the C7 order's line 2, children switched to TLD on the first passage of noisy
clinic weighings over 30 kg) was spent on strength at stage 4 on 2026-10-18: with the call in whole pallets the
first-passage lead was 1.03 pallets and routes with a chosen lead landed it. The redraw's first cell,
pharmacology-pharmacoepidemiology-safety / population-pharmacokinetics-exposure-response, died on paper (twenty
candidates, each a filed formula executed, a tail count or a textbook route); the second, banking-credit-financial-risk /
deposit-liquidity-behaviour, died before any card (efced35). The lesson the cells share: where the field's native
mechanism is composition or a filed formula, the judgment beyond the card is either a reading or a rule, and nothing
the data settle is left to carry the call.

## Rebuild (2026-10-23)

Reopened by the author for a from-scratch rebuild under the rule that no number stays retired, in
banking-credit-financial-risk / expected-credit-loss-provisioning. No draw was carded: the one candidate taken to code
(auto-loan recoveries forecast on each vehicle's purchase market) died on the shipped-proxy screen, and the rest died on
paper (`## Tried and rejected`, last two lines). The number is paused at stage 1 for another cell; the v1 card is
unchanged and no lineage was moved, since no new draw was registered.

The main session then assigned epidemiology-public-health / health-burden-impact-modeling the same day, and
architecture 3 (`## Draw`) was carded there: the repellent net campaign's cases averted, the trial efficacy carried
through the county's in-bed share of exposure.
