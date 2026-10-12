# task447 design note

Seed ET04 (organic deposit growth with merger-adjusted bases). Objective Data Extraction &
Conformation (ETL). Client domain Healthcare Delivery & Health Economics, task type
`payment-claims-health-plan-analytics`. Architecture 1.

The seed is redrawn under START_HERE rule 2. Its own pairings are blocked by the guard (probe cards,
2026-10-11): banking x etl repeats task446 v2, quantitative-finance x etl repeats task445, shape 03
repeats task445, the financial_institution family repeats task446, and the seed's stump (restating a
base through charter, holding-company and branch events) is rule application. What survives of the
seed is its mechanics, kept as supporting work in a provider-ownership world (appendix A5's joining): an owner
gains physicians through three channels (a practice's billing TIN retired into the owner's, a
practice joining under the owner as parent while keeping its TIN, and physicians reassigned one by
one with no organisation event), with a transitive chain and an intra-system TIN consolidation that
is not an acquisition.

Why ETL and not Forecasting: the work is conforming two APCD layouts, eligibility spans split at
plan-year renewals, an ownership register, NPI reassignment spans, a rate exhibit in two payment
formats and per-plan-year network placements into one projection-ready dataset; the committed figure
is a forward projection (2026 has not opened), which is the default shape of the call, not a retag.

## Draw

| Axis | Draw |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task447.json`, registered 2026-10-11, refined in place at stage 2 (same architecture, prose fields only), `guard.py check task447` WARN, answered below |
| Shape | 07, grid of cells: the call and the 2026 increase, then the review's two market exhibits (appendix A2): the commercial imaging, endoscopy and arthroscopy services each lakeshore county's residents received in 2024 with the share Brightwater's physicians referred (county by line, 12 cells), and the shares of the two counties' commercial office visits Brightwater and Ledgestone billed, by specialty (8 cells) |
| Gate G mechanism | `method_or_model_selection` (which referral-capture model the closed acquisitions select), with `forecasting` support (2026 has not opened, and the carriers' 2026 placements differ from the history's) |
| Gap / pattern | objective, then population / C (the share that can move sits behind a join: claim to eligibility span to product to the carrier's placement of one system in one plan year) |
| Generators | G8 (only the referrals whose plan does not tier the new owner as dearer can move), G14 (capture conditioned on the patient's tier for the acquirer), G16 (the capture model the closed acquisitions' own records force), G19 on the asks |
| Decision type | go, hold or stop: proceed to a cost and market impact review of notice N25-014, or close the preliminary review, on the projected 2026 increase in commercial spending against the regulation's $2,000,000 threshold |
| Stakeholder | director of market oversight at a state health care cost review office (role family `compliance_or_audit`) |
| Context artifact | filed standard (the office's projection regulation) |
| Calibration form | `other`: a natural experiment in the claims history, the 2021 to 2023 physician-practice acquisitions by Ledgestone and Wolf River observed before and after, with Norbridge's 2024 re-tiering of Wolf River inside the window |
| Stump strategy | `composition_mix`; the estimand is filed literally (rule OHCCR 4.04 and 4.05: the share expected for each referred service in the projection year, measured on the physicians who joined systems by acquisition before and after, stated in whole per cent) and the method is forced by the records (`determinism-check` §1 form 1, with 4.05's before-and-after measurement as the general method of form 2); no selection criterion is filed, the decisive rule is not filed, no official decoy, no validated decoy |
| Forum / forcing / org | the Attorney General's health care division, which receives the preliminary review (`regulator_or_inspector`) / the notice's 30-day statutory review clock (`statutory_or_regulatory_filing`) / `government_agency` |
| People | Samantha Abbott (the office's APCD data manager), Jacob Murillo (Ledgestone's counsel, who filed the notice), Debra Prince (Brightwater's administrator), drawn with guard.py names, seed 447. Physicians come from the generator's seeded draw, a surname another build carries (Johnson, against task130) replaced from a separate stream; the surface screen reads two Exhibit B physicians, Clayton Brown and Donna Mcintosh, as personas, and both are on the card |
| As of | 2025-10-21, the pack's export date (the notice was complete on 8 October 2025; the review closes on 7 November 2025) |
| Invented names | Office of Health Care Cost Review (the office); Ledgestone Health (acquirer); Brightwater Medical Group (target); Wolf River Health and Kinnickinnic Health (rival systems); carriers Cedarbrook Health Plan, Bayfield Mutual Health, Norbridge Health Insurance, Lakefront Benefit Administrators, Heartland Cooperative Health; practices and facilities invented from word lists |
| Deliverable | one file, `N25-014_preliminary_review.pdf` |
| Opening move | question-first, question form `whether` (`prompt.txt`) |

**WARNs answered.**
- `overuse.org_family` (government_agency in 22 builds): the decision belongs to a regulator by
  statute, and no other family is honest; the forum (the Attorney General) and the forcing event
  (a statutory notice clock) are fresh against the last three builds.
- `overuse.shape` (07 in 3 of the last 12): the criteria come from three grids, each a different
  measure, and the main figure is not a max over a table; shapes 01, 03 and 05 are banned by the last
  two builds and the funnel shape would name the method in the ask.
- `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, against task445 and task446 v2):
  task445 chose a completion method for a censored filing window by back-test, and task446 v2 carries
  a screen's yield from past populations onto one with a different base rate; here the choice is which
  capture model the closed acquisitions select, and the model that survives has to be carried onto a
  plan design the history never saw. `decomposition_attribution` is also honest but repeats task119 v2 and
  task38 v3 on the same_driver test.
- `test.same_driver_older` NOTE against task35 v1: differentiated on the card (a filed floor and a
  filed certification share against a capture that exists only for referrals the plan lets move).

**Similarity claim.** No prior build projects the spending effect of a change of ownership from a
natural experiment of earlier ownership changes. The nearest drivers on file sit at 0.08 (task72 v2,
booking a movement to the owner whose agreement covered each piece of service; task123, a trailing
total over closed filing years). task446 v2 (0.05) carries a screen's yield from past populations onto
one with a different base rate; this build's moderator is not a base rate but a carrier's placement
of one hospital system in one plan year, which changes for the projection year, and the model that
transports it is forced by the records of two owners' acquisitions (the in-history re-tiering), with no
filed criterion. task181 (pooled arrival
speed against each unit's own arrival history) is a completion driver and does not come near.

## Domain coupling (examples read before the stump sentence)

- Exemplar, Medicare Billing Integrity Review (0.18): a claims-based provider measure where the face
  reading of one file loses to the lowest value consistent with every file of record. Teaches that
  the asks should be the construction's outputs by segment (the top ten, the counts above ninety and
  eighty). This build differs: the decisive step is a model choice for a forward projection, not a
  reconciliation of two files, and nothing is filed as a lowest-value rule.
- Exemplar, Hospital Uncompensated Care Policy (0.26): a residual against a matched reference group,
  pinned by reproduction of certified cycles. Teaches the depth the client pays for (raw cost-report
  cells through windows, pools and matching). This build differs: no certified figure exists and no
  criterion is filed; the records of the earlier acquisitions force the model, and the decisive move
  is carrying it onto the 2026 plan designs.
- Rigor patterns, payment, claims and health-plan analytics: claims completion (spent by task445 and
  task181, avoided), difference-in-differences for voluntary programmes (the history here has its own
  pre-periods), reconciliation order, PMPM as a ratio of totals. This build takes its own pattern
  (referral capture transported across a change in the moderator's value), which none of the four
  covers.
- `traps/_measured.md`: trap 13 (validates on one population, applies to another) is the stump; traps
  1 and 3 (ships a failed back-test, stops at a close but inexact match) are the rungs the records'
  structure exposes; trap 12 (stops at the first control that passes) is the acquirer-only back-test.
- `proven-in-production.md`: L7 (the product-by-product capture reproduces every Ledgestone purchase
  exactly, which is why it is trusted), L5 (the answer is the top cell of the grid), L6 (pinned by an
  absolute split: every tier-two referral after an acquisition stays where it was, every tier-one
  outside referral moves at the same rate), L8 (no reconciliation sees the 2026 placement), and the
  dead shape "a forward population named by a filed clause", which is why the regulation names the
  projection year and the product but never the placement.
- The domain coupling, in one line: the field's method for the referral half of a vertical-integration
  projection is a capture model moderated by benefit design, projected under the plan designs of the
  year being projected; a generalist's correction (stratify by carrier or product, reweight to the
  target's mix) reproduces the history and still misses, because the stratum that decides is a
  carrier's placement of one system in one plan year.

## Three rules

- **Domain test:** the call is health-economics practice for vertical integration, professional price
  convergence plus referral capture into hospital outpatient departments priced on commercial allowed
  amounts, with tiered-network cost sharing deciding which referrals can move. Swap in another field's
  nouns and the site-of-service price gap, the tiered cost sharing and the referral capture after
  physician integration have nothing to attach to.
- **Analyst test:** a strong analyst who conforms every claim, eligibility span, ownership change and
  rate exhibit correctly and reads the rule correctly measures the referral shift on Ledgestone's
  earlier purchases, finds a product-by-product share that reproduces every one of them (Bayfield
  Value Tier patients never moved), applies it to Brightwater's referrals, projects about $1.6 million
  and closes the review. Nothing it read is wrong; what is wrong is carrying a share measured under the
  2021 to 2024 placements onto a year in which Bayfield's placement of Ledgestone has changed, when the
  records of every earlier acquisition, Wolf River's included, show the share following the patient's
  tier for the acquirer. Decisive step class: analytical.
- **Layer 1:** an all-payer claims database on two layouts, line-grain claims with replacements and
  voids, eligibility spans cut at plan-year renewals and address changes, provider identities that do
  not line up, an ownership register blind to physician-by-physician moves, per-plan-year tier filings,
  a rate exhibit in two payment formats, late payments (detail under The two layers).
- **Layer 2:** a referral share measured on earlier acquisitions and transported to a year whose plan
  designs differ; the rigorous method keys the share to the patient's tier for the acquirer in the plan
  year and carries it with each referral's 2026 placement.

## Literal reader

A reader who executes every filed definition literally, with no domain inference, computes this:
Brightwater's baseline services are its professional claims billed under its TIN and the outpatient
facility claims that name one of its physicians as referring provider, 2024 dates of service paid by
30 June 2025 (rule 4.03); each is projected as the same service to the same member under the same
product in 2026 (4.04); professional services take Ledgestone's filed professional rates, and a
referred service Ledgestone offers that was not at a Ledgestone site moves there in the share expected
for that service in the projection year, at Ledgestone's filed rate, every other service keeping its
baseline allowed amount (4.04(b)); that share is measured on the referred services of the physicians
who joined health systems by acquisition (appendix A5) where the database holds them before and after,
each service dated against its own physician's joining date, as the rise in the share at the acquiring
system over the share that was elsewhere before, and stated in whole per cent (4.05); the increase is
the with-transaction spending less the baseline (4.06), against $2,000,000. That is the golden's
estimand exactly. 4.05 names no model and no criterion: what the expected share for a service depends
on is the analyst's, and the records force it (`determinism-check` §1 form 1). In every acquired
practice and every product the share is 86 per cent for patients whose plan placed the acquirer first
(or had no tiers) and nil in the second tier, and the one product whose placement of a system changed
inside the history moved with it (Norbridge's Tiered EPO at Wolf River's practices: nil before plan
year 2024, 86 per cent from it). A share pooled, by carrier or by product contradicts those records
(it misses Wolf River's 2024 by 8 points or more); only the tier in force reproduces every practice-
year, and 4.04 projects each service under its product's 2026 terms. The easy answer comes from an easy
method (a share pooled, by carrier or product by product, measured on the acquirer's own purchases),
never from another reading of the text: no filed sentence names the employed group's share, a pooled
rate, the 2024 placements or Ledgestone's 2024 claim prices, and the one place a reading could split
(services already at Ledgestone) is pinned by 4.04(b), which moves only services that were not at a
Ledgestone site.

Where the filed text leaves a choice, every option and what it gives (make.py prints each figure,
checks.py asserts it):
- The estimator of the tier-one share (pooled over practice-years, practices averaged, Ledgestone's
  purchases only, Northpoint missed or dated at its first or last physician's move, by service line):
  fitted 0.8583 to 0.8615, every one stated as 86 per cent, so the projection is one figure. A reader
  who skips the whole-per-cent statement still lands the total in the 2.2 bin and every part in its
  $10,000 bin ($2,206,044 to $2,211,006).
- Finer versions of the tier model (by system, carrier, product, service line, practice, the latest
  year or plan year): every cell states 86 per cent in tier one and nil in tier two (C1, asserted cell
  by cell), so any of them projects the same figure.
- The tier in the history by plan year or by calendar year: both state 86 and nil, and plan years 2025
  and 2026 carry the same placements, so the projection does not move.
- Expected moves against whole referrals: 4.05 files a share, so a referral moves in its expected
  share.
- Which Ledgestone site a moved referral lands at: one chargemaster, one price (C1).

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain:
1. Conform the 2021 to 2023 extract (layout 2.4) to layout 3.1 and keep each claim's latest version
   net of voids.
2. Take Brightwater's 2024 baseline under 4.03: professional lines under its TIN, outpatient facility
   lines its physicians referred, paid by 30 June 2025.
3. Reprice the professional lines at Exhibit C: $609,633.
4. Measure 4.05's share on Ledgestone's earlier purchases, cut product by product as the claims carry
   it: every purchase is reproduced, and Bayfield Value Tier patients never moved.
5. Apply the product shares to Brightwater's referrals for codes Ledgestone bills, priced at Exhibit C:
   $1,023,436.
6. Add the parts and compare with $2,000,000.

Ends on: close the review at $1.6 million ($1,633,069)
Golden: proceed to a cost and market impact review at $2.2 million ($2,209,205)

The same path cut by carrier lands $1.6 million ($1,551,117), pooled $1.4 million, and product by
product over every acquisition $1.6 million ($1,643,405); every one closes the review.

## Stump sentence

A competent solver conforms the APCD extracts, the ownership changes and Ledgestone's rate exhibit
correctly, measures how much of each earlier purchase's outside referral flow moved to the new owner,
pooled, by carrier or product by product, finds that Bayfield Value Tier patients never moved,
projects a 2026 increase of about $1.6 million against the office's $2.0 million threshold and closes
the preliminary review; the capture follows each patient's tier for the acquirer, as Wolf River's 2024
re-tiering shows inside the history, and Bayfield places Ledgestone in its first tier from 2025, so
the projection with each referral's 2026 tier is about $2.2 million and the notice goes to a cost and
market impact review.

## Data-native sentence

Commercial referrals follow cost sharing: after a hospital system buys a physician group, the group's
patients move into the system's outpatient departments only where their plan's network does not put
those departments in the dearer tier, the plan a group's patients carry is set by the local employers
who buy it, and carriers re-tier hospital systems at plan-year renewals when rates are renegotiated,
so a group in one town whose biggest employers buy Bayfield's Value Tier PPO is projected wrongly by
any capture measured while Bayfield still tiered Ledgestone as dearer.

## The two layers

- **Layer 1 (mess, real system behaviour):** an all-payer claims database fed by five carriers on a
  common data layout with a layout revision between the 2021 to 2023 history extract and the 2024
  extract; facility and professional claims at line grain, with replacement and void submissions
  marked by claim frequency code; eligibility spans split at employer plan-year renewals, some on
  1 July, with product moves at renewal and address changes; carrier-submitted provider files that
  repeat one physician across carriers under different spellings; NPIs, billing TINs, CMS
  certification numbers and practice names that do not line up; an ownership register that records
  organisation events but not physicians reassigned one at a time; network tier placements filed per
  product and plan year; a rate exhibit with four carriers on fee schedules and one on a percent of
  Medicare by service category; claims paid after the runout date in an extract pulled later; units
  above one on some procedure lines. Every piece is something an APCD, a carrier or a provider
  registry actually produces.
- **Layer 2 (decides the call):** the referral shift is transported from earlier purchases. Shortcut:
  a capture measured on Ledgestone's earlier purchases (pooled, by carrier, product by product, or the
  employed group's share) applied to Brightwater's referrals. Expert move: the capture is the same
  share of outside referrals for every patient whose plan places the acquirer in tier one (or has no
  tiers) and nil for tier-two patients, in every acquisition and every year, Wolf River's 2024
  re-tiering included; so the projection applies it to each Brightwater referral's tier for
  Ledgestone in 2026, reached through APCD eligibility to the product and the carrier's 2026
  placement, where Bayfield's Value Tier PPO now places Ledgestone in tier one.

## Gate G

- Litmus: no reported number in the pack is wrong and no stakeholder conclusion is overturned. Every
  claim is as submitted, every rate is as filed, every placement is as filed, and the earlier
  purchases' referral shifts are what happened. Nothing in the pack states a projection. The
  difficulty is that the shift the acquirer's own history shows was measured under placements that
  no longer hold.
- Mechanism: `method_or_model_selection` (the capture model the closed acquisitions select), with
  `forecasting` support.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- Clean-data test: repair every Layer 1 item and the answer and the product-by-product projection do
  not move (the main call's rows carry none of them, asserted in the generator).
- Lens swap: the product-by-product read and the answer are not one population under two lenses; they
  apply different models (one keyed to a product's history, one to the tier in force) to the same
  2026 population.
- Delete every wrong number: there are none to delete; still hard.

## Readability screen

The six tests of `stumping` Part 2.1 on every rung (no means the test does not fire).

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 professional repricing only | yes, 4.04(a) is this step | no | no | no | no | yes, one repricing | readable |
| R1 the employed group's or the affiliate's share | no | no | yes, build the analog | no | no | no | readable |
| R2 one share pooled over the acquisitions | yes, 4.05 executed with no cut | no | no | no | no | no | readable |
| R3 the share by carrier | no | yes, submitter code on every line | yes, hold the pool to a visible attribute | no | no | no | readable |
| R4 the share product by product, or by tier with the 2024 placements | no | yes, product on every eligibility span | yes, hold the pool to a visible attribute | no, Ledgestone's purchases reproduce it | no | no | readable |
| R5 the share keyed to the patient's tier for the acquirer in the plan year, carried with each referral's 2026 placement (decisive) | no: no shipped sentence mentions tiers beside referrals, shares or the projection year | no: no claim or span carries a tier; the tier for the acquirer is a join from the span's product and benefit period into a filing kept for the cost trends report | no: the reflex strata (carrier, product) reproduce Ledgestone's purchases | no: nothing scores candidate models; on Ledgestone's purchases the corpus reproduces the product shares, and the only refutation sits in Wolf River's 2024 by product, a cut the default path never takes | no: every key, join and total ties on the wrong path | no: the share is not a ratio or difference of any reported figure | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | commercial | products the product reference lists with line of business Commercial | add the Medicare Advantage claims | not computable: Exhibit C files no Medicare Advantage rate | rule 4.02(b) |
| SF2 | spending | allowed amount, plan payment and cost sharing together, latest version net of voids | the plan's payment alone | not computable: the filed rates are allowed amounts | rule 4.02(c) |
| SF3 | the increase the deal will cause | projected spending less baseline spending on the baseline services | Ledgestone's gross revenue on the services that move | proceed (larger) | rule 4.06 and 4.04(b), the rest keeps its baseline amount |
| SF4 | 2026 | the projection year, each service under its product's 2026 placement | the plan year in force on a July renewer's date carried forward (plan year 2025) | same call: plan years 2025 and 2026 place Ledgestone alike for every moving referral | same call |
| SF5 | millions of dollars to one decimal | unrounded parts summed, total rounded once | rounded parts summed | same call, same 2.2 | same call |
| SF6 | the review threshold | $2,000,000 or more proceeds | more than $2,000,000 | same call, the projection is above either | same call |
| SF7 | the baseline window | 2024 dates of service paid by 30 June 2025 | everything the extract holds (paid through 31 August 2025) | same call: no Brightwater line was paid after the runout | rule 4.03; same call |
| SF8 | Brightwater's physicians | billing under its number on the date of service | Exhibit B's list | same call: the same eighteen | same call |
| SF9 | services Ledgestone offers | codes its outpatient sites bill | codes Exhibit C prices | same call: the two agree on every code Brightwater refers elsewhere | same call |
| SF10 | Ledgestone's facility price | the rate filed with the notice (Bayfield at its percent of the CY2025 Medicare amounts) | Ledgestone's 2024 claim prices | proceed ($2.6 million) | rule 4.04(b), priced at the rate filed with the notice |
| SF11 | the expected share's precision | stated in whole per cent | the fitted share unrounded | same call, the same total and parts | rule 4.05; same call |
| SF12 | the services that move | referrals that were not at a Ledgestone site | every referral of the class, the 8 per cent already at Ledgestone included | proceed ($2.3 million) | rule 4.04(b), only services not at its sites in the baseline |

The stump is none of these readings: every row lands the golden's call or is refused by the cited rule,
and `generator/checks.py` asserts each (SF1 to SF12).

## Entity, unit, decision

The Office of Health Care Cost Review receives notices of material change. Ledgestone Health (two
hospitals in Green Bay and Appleton and an outpatient centre in Manitowoc, one chargemaster) filed
notice N25-014 on 8 October 2025 to buy Brightwater Medical Group (18 physicians in Manitowoc, Two
Rivers and Kewaunee), with closing on 1 January 2026 and Brightwater's TIN retired into Ledgestone
Medical Group's. The regulation requires the office, within 30 days of a complete notice, to project
the increase in annual commercial spending the transaction will cause in its first full calendar year
and to proceed to a cost and market impact review when the projection is $2,000,000 or more.

- Entity and unit of value: Brightwater's 2024 commercial services, scored on allowed dollars (plan
  paid plus member cost sharing), professional and referred.
- Two quantities that both read as "how much referral moves": the share of Ledgestone's earlier
  purchases' outside referrals that moved after each purchase (0.39 pooled, 0.324 to 0.507 practice by
  practice), and the share of a tier-one outside referral that moves (0.860 in every practice, both
  systems, fitted 0.8595 to 0.8622). They rank the projection differently because two in five Brightwater patients
  carry the one product whose placement of Ledgestone changes before the projection year.
- Decision: exactly one of {proceed to a cost and market impact review, close the preliminary
  review}, for notice N25-014, on the projected 2026 increase against $2,000,000.

## Ladder

Built figures: make.py prints every one from the shipped bytes and checks.py asserts them.

**ANSWER: proceed to a cost and market impact review; projected 2026 increase $2,209,205 (filed as
$2.2 million), professional prices $609,633, referred services $1,599,573** (imaging $501,706,
echocardiography $130,261, endoscopy $670,166, arthroscopy $237,732, laboratory $59,708). Above the
threshold by 10.5 per cent. Rank on the natural pipeline: the top cell of the grid (L5).

| Rung | Construction | 2026 increase | vs threshold | Killed by |
|---|---|---|---|---|
| R0 | professional repricing only, referrals stay where they are | $0.610M | -69.5% | 4.04(b) moves referred services, and every earlier acquisition shows referrals moving |
| R1 | Ledgestone Medical Group's 2024 share of referrals at Ledgestone taken as Brightwater's future share (stated 35 per cent); Mishicot Family Practice, the lakeshore affiliate, gives 54 per cent | $1.296M; $1.669M | -35.2%; -16.5% | 4.05 measures the share on physicians who joined by acquisition, observed before and after, and neither group has a before in the database |
| R2 | one share pooled over Ledgestone's purchases (39 per cent), or over every acquisition (44 per cent) | $1.375M; $1.473M | -31.3%; -26.3% | the records: the share is 86 or nil by tier in every practice, never one number; pooled misses Fond du Lac Digestive Health's 2024 by 20.0 points |
| R3 | share by carrier on Ledgestone's purchases (Cedarbrook 30, Bayfield 60, Norbridge 28, Lakefront 50, Heartland 86 per cent) | $1.551M | -22.4% | the records: misses the same practice-year by 20.8 points |
| R4 | share product by product on Ledgestone's purchases (each one reproduced; Value Tier nil), over every acquisition, by product and system, or by tier with the 2024 placements | $1.633M; $1.643M; $1.633M; $1.633M | -18.3% to -17.8% | the records: Norbridge's Tiered EPO patients at Wolf River moved once the plan placed Wolf River first, so a product's share follows its placement (product by product misses Fond du Lac Digestive Health's 2024 by 16.9 points, product and system Lakeside's 2024 by 8.3); the tier model with 2024 placements projects 2024's plan designs into 2026, against 4.04 |
| R5 | share by the patient's tier for the acquirer in the plan year (86 per cent tier one, nil tier two), carried with each Brightwater referral's 2026 placement | **$2.209M** | **+10.5%** | answer |

"A solver who does everything right up to R4 commits to closing the review at about $1.6 million."
Every rung names a different figure; R0 to R4 all name the same wrong call, which is what the call
needs (one call, many paths to the wrong side). The stump sits at R4 to R5, and its cheapest stop is
R4's product-by-product share, which reproduces every one of Ledgestone's own purchases (L7).
Corrections walk upward (R0 to R4), and the decisive rung continues the direction past the
threshold; the partial insight (tier with 2024 placements) lands at R4, not near the answer (L3).

**The records' structure, which forces the model with no filed criterion.** Fitted only to years
before each test year over the 12 practice-years (Oak Hollow 2022 to 2024, Baird Creek 2023 and 2024,
Northpoint 2023 and 2024, Harborview 2024, Cedar Ridge 2024, Lakeside 2023 and 2024, Fond du Lac
Digestive Health 2024), the largest miss in a practice's share at its acquirer: the tier model 1.53
points (by plan year or by calendar year alike); product and system 8.33; acquiring system 12.05;
tiered or not 15.84; product 16.88; pooled 20.00; carrier 20.78. Fitted on everything, the tier-one
share is 0.8595 to 0.8622 practice by practice and 0.8598 to 0.8639 product by product, tier two
-0.0020 to 0.0016, and Norbridge's Tiered EPO patients at Wolf River moved -0.0002 of their outside
referrals before plan year 2024 (481 services) and 0.8598 from it (303 services). On Ledgestone's
purchases alone the product shares fit as well as the tier (1.59 against 1.53 points): the
refutation lives only in Wolf River's records.

**Corridor on the answer (C1/C3).** Every estimator form states 86 per cent (fitted 0.8583 to
0.8615), so the projection is one figure; projected with the unrounded share, the forms land
$2,206,044 to $2,211,006 (the calendar-year twin $2,204,633), inside the 2.2 bin (2.15 to 2.25) with
every part in its $10,000 bin (asserted).

### Correction grid

Toggles: the share model (six, each share stated in whole per cent), the Ledgestone price (the filed
Exhibit C, or the 2024 claims' Bayfield prices, which the 2025 agreement replaced), and the base the
share is applied to (outside referrals only, or every referral of the class including the 8 per cent
already at Ledgestone): 24 cells, in $ millions, * at or above the threshold.

| Model | Exhibit C, outside | Exhibit C, all | 2024 prices, outside | 2024 prices, all |
|---|---|---|---|---|
| pooled, Ledgestone's purchases | 1.375 | 1.442 | 1.558 | 1.640 |
| pooled, every acquisition | 1.473 | 1.548 | 1.679 | 1.773 |
| by carrier | 1.551 | 1.633 | 1.832 | 1.939 |
| product by product | 1.633 | 1.722 | 1.697 | 1.792 |
| tier, 2024 placements | 1.633 | 1.722 | 1.697 | 1.792 |
| tier, 2026 placements | **2.209*** | 2.349* | 2.612* | 2.787* |

Every cell off the tier-2026 row closes the review, the nearest at 1.939 (three violations: a carrier
model, prices 4.04 does not file, and a share applied to referrals already at Ledgestone). Every cell
on the tier-2026 row proceeds, the nearest to the answer 6.3 per cent away (one violation of 4.04's
base). No single defensible reading moves the call.

## Closure table

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | Brightwater's TIN for professional claims; referring NPI of a Brightwater physician for facility claims (4.03); the physician who also bills Thursdays under Kinnickinnic's TIN keeps his Brightwater referrals and his Kinnickinnic-billed visits are not Brightwater's | filed (4.03); C1 asserted: no Brightwater roster change in 2024 |
| 2 | Unit of account | the claim line, expected value of its move | C1: line and claim grain give the same sum (one service line per facility claim on the main rows) |
| 3 | Attribution window | 2024 dates of service, paid by 30 June 2025 | filed (4.03); C1: no main-row claim paid after the runout |
| 4 | As-of dating | product on the service date from the eligibility span; tier for 2026 from the product's 2026 placement | filed (4.04: same member, same product, 2026); C1: no Brightwater member changes product in 2024 |
| 5 | Version basis | Ledgestone's rates filed with the notice (Exhibit C, the 2025 Bayfield agreement); placements filed for plan year 2026 | filed (4.04); the 2024 claim prices are a grid cell, not a fork |
| 6 | Divisor | the share as the rise at the acquirer over the share elsewhere before (4.05); equivalent forms | filed (4.05, and the share in whole per cent); C1/C3: every form states 86 per cent |
| 7 | Weighting | pooled over practice-years | C1/C3: the practice average and every finer cell (system, carrier, product, line, practice, latest year) state the same 86 per cent and nil |
| 8 | Measurement window | all pre and all post months | C1: the quota keeps every key's share stable month to month |
| 9 | Boundary inclusivity | a service on an acquisition date is after it; 1 January counts include spans starting that day | filed in the appendix; C1: no event or hire on a boundary in the asks' populations |
| 10 | Rounding path | the expected share in whole per cent first (4.05), then sum in dollars and round each graded figure once | the parts sit $2,700 or more inside their $10,000 bins (arthroscopy, $237,732, the tightest) and the total $40,795 inside its $0.1 million bin (asserted at $1,000 and $20,000); the thinnest exhibit boundary is Exhibit 1's Kewaunee imaging share (45.437, 0.013 points inside), then Exhibit 2's Brightwater primary-care share (35.034, 0.016), both ratios of counted services with no estimator in them (asserted at 0.01) |
| 11 | Tie-break | none | no ties exist |
| 12 | Maturity | baseline runout to 30 June 2025 | filed; late-paid claims sit only on ask rows (zero-count asserted) |
| 13 | Order of operations | reprice, then sum | commutes |
| 14 | Row order | none | C1: two row orders give the same bytes (asserted) |
| 15 | Duplicate resolution | latest version of a claim (replacement over original, void removes both) | dictionary; C1: no replacement or void on the main rows |
| 16 | Identity normalisation | NPI as the physician key, TIN as the billing entity, facility NPI to system through the directory | C1: Ledgestone's three sites share one chargemaster, so the site a moved referral lands at cannot move its price |
| 17 | Netting | net change (a referral moving off a dearer site lowers spending) | filed (4.06: with-transaction spending less baseline) |
| 18 | Dimensional units | dollars; units of one on every main-row line | C1 asserted |
| 19 | Code semantics | claim frequency codes, place of service, product to tier by plan year | dictionary and placement file |
| 20 | Integerisation | none (expected values) | none |
| 21 | Scope of a clause | "services the acquiring party does not offer stay where they are" covers sleep studies and nuclear cardiology | filed (4.04); C1: no other service lacks a Ledgestone rate |
| 22 | Forward window | the whole of 2026, every member in a plan year that places Ledgestone in tier one for the Value Tier PPO | C1: plan years 2025 and 2026 carry the same placements for every product, so July renewers converge |

## Oracles

- The earlier acquisitions in the claims history (the 2021 to 2023 extract and the acquired practices'
  2024 lines): the evidence 4.05 measures the share on. On the default path's cut (Ledgestone's
  purchases, product by product) they reproduce the naive shares exactly; they refute them only at
  Wolf River's 2024 by product, which the default path never cuts. No artifact scores candidate
  models.
- Exhibit C and the CY2025 Medicare amounts: the prices of both paths, confirming nothing about the
  share.
- The tier filings: the placements of every product by plan year, the same file on both paths, kept
  for the annual cost trends report; it confirms no projection.
- No control total, published figure or reconciliation column ties under one basis only: the export
  manifest's row counts tie on every path.

## Ask sheet

The asks are the review's two standing exhibits. Rule 4.07 says the preliminary review states the projected
increase, its professional and referred parts, and the exhibits the market oversight unit maintains in its
technical appendix; appendix A2 and A3 define them. Both are counted on rows outside the main call's
population and neither needs the call or its construction, so the cracker and the mirror file the same
exhibit figures.

Main block (recommendation and critical components): the call; the 2026 increase in $ millions to one
decimal; the parts 4.07 names (professional $610,000, referred $1,600,000); the 86 per cent measured on the
earlier acquisitions; Bayfield's first-tier placement of Ledgestone from plan year 2025. The cracker keeps
all of it. The mirror (R4) keeps the professional part, which is right on every rung (`r` about 3).

**Ask 1, Exhibit 1 (appendix A2): the commercial imaging, endoscopy and arthroscopy services Manitowoc and
Kewaunee county residents received in 2024, by county and line, with the share Brightwater's physicians
referred (12 figures).**
- Golden: Manitowoc imaging 3,269 services, 40.6 per cent referred by Brightwater's physicians; endoscopy
  1,574, 52.9; arthroscopy 328, 42.7. Kewaunee imaging 1,008, 45.4; endoscopy 444, 64.0; arthroscopy 97,
  41.2.
- H18 home: a standing exhibit of the same review (4.07). It shows how much of each county's outpatient
  care the target's physicians direct, which is the flow the referral shift draws on; the call does not
  turn on it. Use: the Attorney General's health care division reads it with the call.
- Primary device (D1, the same records under two sources): 1,025 members are covered twice, under their
  own employer's plan and as a spouse or child under a second carrier's plan, with concurrent eligibility
  spans from both submitters. Once the first carrier has paid, the second carrier's claim for the same
  service arrives under its own submitter code, product, claim number and paid date, priced on what the
  first carrier left the member to pay. On file: 659 facility services and 1,807 office services billed by
  both carriers. Allowed equals plan paid plus member liability on every row, and nothing names a second
  plan. Key uniqueness, exact duplicates (none, even with the claim number dropped), the amount identity
  and the claim-to-eligibility join on member, product and date all pass, because each copy joins its own
  carrier's span. Only a cut across submitters finds it: one member, one date, one code and modifier, one
  facility, two carriers, each with a span that day. Fair handling (asserted against the services the
  simulation generated): for each member, date, code, modifier and facility, count the units one plan
  holds. Over-cleaning half: de-duplicating on member, date, code and facility also removes the genuine
  RT and LT lines of bilateral knee films and arthroscopies.
- Hazards: H1 versions, H2 late payment, H4 residence on the date of service, H5 RT and LT lines.
- Path: eight files (the 2024 facility claims, the eligibility spans, the product reference, the data
  dictionary for frequency codes and ZIP to county, the technical appendix A1 and A2, rule OHCCR 4.02 for a
  physician of a practice and a referred service, the notice for Brightwater's number, the NPI reassignment
  history) and fifteen columns (submitter_code, payer_claim_control_number, claim_frequency_code,
  original_claim_control_number, member_id, product_id, service_from_date, procedure_code,
  procedure_modifier_1, quantity, service_facility_npi, referring_provider_npi, coverage_start,
  coverage_end, member_zip).
- Stops (make.py prints each, checks.py asserts each lands outside its bins), in services and points,
  Manitowoc imaging, endoscopy, arthroscopy, then Kewaunee:
  - every claim counted (the cracker): +67, +49, +12, +33, +5, +4 services; shares -0.82, -1.60, -1.51,
    -1.44, -0.71, -1.63
  - de-duplicated on member, date, code and facility: -64, 0, -7, -19, 0, -4; +0.81, 0, +0.93, +0.77, 0,
    +1.77
  - residence by the member's first ZIP: +23, +16, +2, -17, -9, 0; -0.28, -0.53, -0.26, +0.78, +1.32, 0
  - rule 4.03's runout applied to the exhibit: -12, -2, -1, -12, -2, 0; +0.15, +0.07, +0.13, +0.55,
    +0.29, 0
  - versions as filed: Manitowoc imaging +29, -0.36
  - every combination of the five (24 pipelines): none lands back inside a bin it left, the nearest 0.13
    points off.
- Realism: dual coverage is ordinary in commercial claims, a second carrier's claim follows the first
  carrier's payment, and pricing the secondary on the remaining liability is one of the formats APCD
  submitters use.

**Ask 2, Exhibit 2 (appendix A3): Brightwater's and Ledgestone's shares of the two counties' 2024
commercial office visits, by specialty (8 figures).**
- Golden: primary care 35.0 and 7.6 per cent; gastroenterology 41.8 and 4.0; orthopaedic surgery 35.7
  and 3.7; cardiovascular disease 71.9 and 7.6.
- H18 home: the second standing exhibit (4.07), the parties' combined position in the physician services
  the transaction consolidates; the call does not turn on it.
- Primary device (D2, an attribute reported at the wrong level): Kinnickinnic's Sheboygan business office
  reports the network's own family-medicine taxonomy in the rendering-provider field for every
  practitioner it bills. That covers its internists, the Brightwater gastroenterologist's Thursday clinic,
  and the gastroenterologists, orthopaedic surgeons and cardiologists who hold clinic days at its Manitowoc
  hospital: 7,471 lines, 12 NPIs. Every code is valid and maps to a specialty, so a specialty read from
  the claim moves the visiting specialists' visits into primary care. Only a cut across files finds it:
  the carriers' provider files give each NPI one taxonomy; a "family medicine" provider on these lines
  bills knee arthroscopy and echocardiography interpretation; the Brightwater gastroenterologist carries
  two taxonomies on two numbers' claims. Fair handling: each physician's specialty from his or her own
  taxonomy (asserted one per NPI across every carrier's file).
- Shared device: Ask 1's second-plan copies, 1,807 office services, move every denominator.
- Hazards: H2 late payment, H3 control through the register (Mishicot Family Practice is Ledgestone's as
  an affiliated, controlled practice), H6 physicians only (Mishicot's nurse practitioner), H7 telehealth
  (A3: a visit by telehealth is not an office visit; 706 at place of service 10, 701 with modifier 95).
- Path: eight files (the 2024 professional claims, the carriers' provider file, the provider ownership
  register, the notice for Exhibit A and Brightwater's number, the technical appendix A3 and A4, the data
  dictionary for place of service, modifiers, taxonomy and ZIP to county, the eligibility spans for the
  second plans, the product reference) and fourteen columns (procedure_code, place_of_service,
  procedure_modifier_2, rendering_provider_npi, rendering_provider_taxonomy, billing_provider_tin,
  service_facility_zip, member_id, service_from_date, submitter_code, primary_taxonomy, entity_tin,
  relationship, effective_from).
- Stops, in points, Brightwater then Ledgestone, primary care, gastroenterology, orthopaedic surgery,
  cardiovascular disease:
  - the claim's taxonomy and both plans' copies (the cracker): -1.75, +6.29, +3.59, +18.15; -0.38, +0.76,
    +0.49, +2.33
  - the claim's taxonomy alone: -0.85, +7.49, +4.74, +18.52; -0.19, +0.72, +0.49, +1.96
  - both plans' copies alone: -0.90, -1.00, -1.13, -0.92; -0.20, +0.04, -0.01, +0.22
  - telehealth counted: -1.07, -0.34, -0.55, -0.37; +0.10, -0.03, -0.06, -0.04
  - Mishicot's nurse practitioner counted: primary care -0.52 and +1.38
  - Ledgestone Medical Group's number only: Ledgestone's primary care -7.61 (to nil)
  - rule 4.03's runout applied: +0.27, +0.03, +0.18, +0.14; 0.00, -0.07, -0.01, -0.12
  - every combination of the seven (128 pipelines): none lands back inside a bin it left by a full point
    of rounding, the nearest 0.065 points off.
- Realism: a central business office reporting the group's taxonomy in the rendering loop is one of the
  most common provider-field faults in APCD professional claims.

**Hazards (cross-cutting).**

| Hazard | What it is | Ask 1 | Ask 2 |
|---|---|---|---|
| H1 versions | Kinnickinnic's referrals to its Manitowoc hospital: replacements (code 7) and voids in error with rebills (code 8); the dictionary files the codes | Manitowoc imaging +29 as filed | none |
| H2 late payment | two self-funded groups' fourth-quarter claims paid in July and August 2025, inside the extract | up to -12 services under a runout | Brightwater up to +0.27 under a runout |
| H3 control | Mishicot under Ledgestone (register and Exhibit A) | none | Ledgestone primary care to nil on LMG's number only |
| H4 residence | 4 per cent of the other lakeshore members move, spans cut at the move | first ZIP: up to 23 services | none |
| H5 RT and LT | bilateral knee films and arthroscopies on two lines | the over-cleaner's loss | none |
| H6 physicians | Mishicot's nurse practitioner (A4: physicians only) | none | primary care -0.52 and +1.38 |
| H7 telehealth | place of service 10 or modifier 95 (A3) | none | Brightwater -0.34 to -1.07 |

**Referees.** Ask 1: the eligibility file (every second-plan claim has the second carrier's own span
covering the date, and every member billed by two carriers for one service holds both). Ask 2: the
carriers' provider file (one taxonomy per NPI across every carrier). Neither hands over a level: the
eligibility file counts nothing and the provider file ranks nothing.

**No marker, no oracle.** The second-plan claims carry frequency code 1 and fill every column as first
claims do, and the second carriers' claims for their own members look the same. The family-medicine code
on Kinnickinnic's lines is the code of every family physician in the file. No control total ties under one
handling only: the export manifest's row counts tie on every path.

**The separation line.** Zero device and hazard rows in the main call's population, asserted by count: no
second plan for any Brightwater, acquired-practice or Ledgestone Medical Group member; none on Mishicot's
lines or at Ledgestone's sites (so R1 and the 2024-price column of the grid do not move); the taxonomy
device on Kinnickinnic's professional lines only. `generator/main_call_ref.json`, written from the build
before this ask layer, holds every main row, every reference file the call reads whole and every main
figure; checks.py asserts the current build reproduces it byte for byte.

**Cracker sheet.**

| Ask figures | n | The cracker's path (lands R5, runs the battery, executes A2 and A3) | Cracker |
|---|---|---|---|
| Exhibit 1, services by county and line | 6 | counts every claim's units: the second plans' copies add 67, 49, 12, 33, 5 and 4 services | miss |
| Exhibit 1, Brightwater's referred share | 6 | the same totals: every share 0.71 to 1.63 points low | miss |
| Exhibit 2, Brightwater's share by specialty | 4 | specialty from the claim and both plans' copies: -1.75, +6.29, +3.59, +18.15 | miss |
| Exhibit 2, Ledgestone's share by specialty | 4 | the same totals: -0.38, +0.76, +0.49, +2.33 | miss |

Mirror leakage: 0 per cent (the mirror stops at R4 and counts both exhibits exactly as the cracker does).

Pair ceiling: 27.5 (planning weights 38 / 7 / 55 and r = 3: the cracker 38 + 7 + 0 = 45, the mirror
3 + 7 + 0 = 10).

The honest exposure: a response that cuts across submitters and reads each specialty from the provider
file keeps both exhibits, about 3 + 7 + 55 = 65 with the call held, and two such responses would fail the
bar on their own. The build rests on the two silent devices holding at least one of the top two.
Criteria: the call, the increase, four critical components, twenty exhibit figures and two instruction
criteria, 28.

## Pack plan

| File | Format | Rows | Role |
|---|---|---|---|
| `apcd_op_facility_claims_2024.csv` | CSV | 67,976 | spine: 2024 commercial outpatient facility claims for the directory's facilities, layout 3.1, paid through 31 August 2025 |
| `apcd_op_facility_claims_2021_2023.csv` | CSV | 31,568 | the acquired practices' physicians' referrals 2021 to 2023, layout 2.4 |
| `apcd_professional_claims_2024.csv` | CSV | 69,086 | professional claims performed in Manitowoc and Kewaunee counties, 2024 |
| `apcd_eligibility_spans.csv` | CSV | 102,665 | member spans 2021 to 2024, cut at product, benefit period and address, one set per carrier for members covered twice |
| `apcd_product_reference.csv` | CSV | 14 | product, carrier, line of business, tiered network flag |
| `network_tier_placements_2020_2026.json` | JSON | | each tiered product's placement of each system by plan year, from the carriers' form filings |
| `apcd_extract_data_dictionary.pdf` | PDF | | both layouts, frequency codes, place of service, taxonomy, ZIP to county |
| `provider_ownership_register.csv` | CSV | 21 | notices of material change and annual registrations |
| `npi_reassignment_history.csv` | CSV | 246 | physician to billing TIN spans |
| `carrier_provider_file.csv` | CSV | 1,042 | carrier-submitted provider records, name variants across carriers |
| `facility_directory.csv` | CSV | 20 | facility NPI, system, type, county |
| `N25-014_notice_of_material_change.pdf` | PDF | | the notice with Exhibits A and B |
| `N25-014_exhibit_C_ledgestone_rates.xlsx` | XLSX | | Ledgestone's facility rates by carrier (Bayfield as a percent of Medicare by category) and professional schedule |
| `cms_opps_clfs_2025_wisconsin.csv` | CSV | 21 | the Medicare amounts the Bayfield terms reference |
| `ohccr_rule_4_preliminary_review.pdf` | PDF | | the rule (estimand, criterion, threshold) |
| `market_oversight_technical_appendix.pdf` | PDF | | service lines, the two exhibits (residence, office visits), physicians and joining |
| `export_manifest.csv` | CSV | 18 | the extract's manifest |
| `hcris_hospital_outpatient_extract_fy2023.csv` | CSV | 6 | distractor: cost report outpatient lines, costs and charges |
| `apcd_medicare_advantage_facility_claims_2024.csv` | CSV | 5,200 | distractor: Medicare Advantage claims for the same referrers, outside the commercial estimand |

19 files, four formats (CSV, JSON, PDF, XLSX), the eligibility spans at 102,665 rows, two distractors
named in `metadata.json` only. No filed document says that referrals follow tiers, that the share
depends on a plan's placement, or that placements change what an acquisition does.

## Assertion regime

`generator/checks.py` runs every assertion on each build (the count is in `pipeline.json`), and
`generator/verify.py` recomputes every graded figure from `target/` alone with csv, json, openpyxl and
pypdf, sharing no code with the generator: the answer and every component; every rung and its distance to
the threshold (each wrong rung 8 per cent or more below, the nearest at 16.5 per cent; the answer 10.5 per
cent above); the 24-cell correction grid; the records' structure (the tier model within two points of
every practice-year, every model outside the tier family 8 or more points off one; every finer cell,
every practice and Norbridge's Tiered EPO at Wolf River before and after plan year 2024 stating 86 and
nil); the estimator corridor; the semantic fork table, SF1 to SF12; the rule filing no selection
criterion; every graded figure's distance to its bin edge; the clean-data test; zero device and hazard
rows in the main population; the main call reproduced byte for byte against `main_call_ref.json`; both
exhibits' goldens against the simulation's own services, every stop and the cracker outside every bin,
every combination of mishandlings (24 on Exhibit 1, 128 on Exhibit 2) kept out of the bins it leaves;
the referees (one taxonomy per NPI in the provider file, a second carrier's span under every
second-plan claim); the distractor-deletion test; the realism sweep (no two facilities with one count,
no constant monthly series, no recurring monthly totals, no round headline figure); the input gates;
the submission's figures and the house checks; the prompt as one plain-text paragraph; two consecutive
builds byte-identical and the zip member for member. The generator writes `generator/figures.json` and
`figures_check.py` passes.

## Realism debts

- Capture switches on at the acquisition date with no ramp, and the tier-one capture is identical
  across practices, families and systems (0.860). Forced because the out-of-sample criterion has to
  separate the models with margin and every estimator form has to state the same whole per cent;
  mitigation: shares
  are assigned by quota so the monthly series reads as ordinary counts, and the pre-acquisition share
  differs by practice (0.075 to 0.085).
- Brightwater's members do not change product inside 2024 and no main-row claim carries a
  replacement, a void or a late payment. Forced by mess neutrality; mitigation: the same mess is dense
  on the other referrers' rows in the same files.
- Bayfield's percent-of-Medicare terms differ by service category (405 per cent for imaging). Forced by
  the price book; such carve-outs exist in hospital agreements.
- No Brightwater, acquired-practice or Ledgestone Medical Group member has a second plan, Mishicot's office
  files no claims with second plans, and no second plan submits a service at a Ledgestone site. Forced by
  the separation line (the main call reads those members' rows, and the R1 rung and the grid's 2024-price
  column read Mishicot's referrals and Ledgestone's site prices); mitigation: 1,025 other members carry
  two plans, with second-plan claims at every other facility and practice.
- Exhibit C's facility rates are one chargemaster times a constant factor per carrier (Norbridge's are
  1.06 of Cedarbrook's on every code). The rates are main-call inputs, frozen through the ask-layer pass;
  a revision that may move the call can give each carrier its own negotiated schedule.
- Kinnickinnic's visiting specialists see patients in Manitowoc but their lakeshore patients' outpatient
  referrals are not in the extract's lakeshore rows. Accepted: no exhibit counts their referrals, and the
  Sheboygan rows carry their referral pattern.

## Stopping rule

Written before the solver round. A round where the solver commits to proceeding with a 2026 figure
inside the 2.2 bin is a landed call: harden by moving the decisive rung (a second product's 2026
placement, or the moderator carried by a different field), never by planting. A round where the
solver closes the review passes the gate. A portal result with the top two over 50 and the call held
goes to the ask-only revision; one where two responses land the call re-roots.

## Leak check

`leak.py --asof 2025-10-21` (the pack's export date) returns REVIEW with no LEAK, each line answered:
- `014` in the notice and the data dictionary: the notice number N25-014, which the prompt names.
- 'Brightwater Medical Group' beside decision vocabulary in the notice: the certification block of the
  filing under review; the target is named in the prompt.
- `4.05` and `4.06` in the rule: the rule's own section numbers, which the submission cites.
- Design-note vocabulary in the notice (3 terms), the dictionary (7), the appendix (8) and the rule (9):
  the field's ordinary nouns (product, carrier, service, practice, claims, history, shares, records,
  projection); no document connects tiers with referrals, the share that moves or the projection year,
  the rule files no selection criterion, and the placement file says only what it is kept for (the
  annual cost trends report).

Two isolated solver's-eye reads ran, on the stage 3 pack and again after the appendix pins. Neither quoted a sentence for the decisive step,
found no file that ranks or answers, no file that exists only to help, no figure that reads as the answer,
and both called all nine REVIEW lines harmless. Their literal readings of 4.02 to 4.06 execute to the golden. Their
literal reading of the exhibits counts claim units and takes specialty from the claim's taxonomy, which is
the cracker's path the ask sheet designs for (the second read names the provider file as a competing source;
the judge took it, from the records). Rulings on the first read's other points:
- Exhibit definitions without a paid-date cut, version netting stated only for spending, and
  "Internal Medicine, Gastroenterology" read as internal medicine: closed in the appendix (A2 and A3 count
  every 2024 date of service whenever paid, on the latest version net of voids; A3 maps each specialty to
  its NUCC codes and defines a physician's specialty as the classification of the physician's taxonomy).
  Hazards only; no figure moved.
- The export manifest's "lakeshore physicians" on the Medicare Advantage file: reworded to the two counties.
- Bayfield's percent-of-Medicare cells (4.05 shown as 405 per cent under the 0% format) and the CY2025
  amounts for a 2026 projection: harmless; the workbook stores percentages as Excel does, and 4.04 does
  not trend prices, so the filed CY2025 amounts are the only ones a literal reader can apply (the judge
  executed both the same way).
- Exhibit C's rates scale by a constant carrier factor over one chargemaster: accepted as a realism debt,
  because the rates are main-call inputs and the ask-layer pass keeps the main call byte-identical.

## Determinism check

Judge pass 1 (2026-10-12, isolated, Sonnet, medium, literal reading first): DETERMINISTIC, APPROVE
(`determinism_check_report.md`). Every component, the call and all twenty exhibit figures reproduced; the
judge found both ask devices (it counted the 659 cross-carrier facility services and 2,420 office visits
once and took each physician's specialty from the provider files) and recorded the claim-taxonomy reading
as a semantics error with no shipped sentence naming the source. Its optional pin (naming the provider
file in A3) would settle the Exhibit 2 device by a filed sentence, so it is not taken; A3 instead defines
a physician's specialty as the classification of the physician's taxonomy. Gate G: method_or_model_selection
with forecasting, analytical_non_defect, no surface-read dependency, no sole data defect. Gate H: domain
pass, layers pass, decisive step analytical. Its second optional pin (filing the tier stratification) would
remove the stump and is not taken.

## Tried and rejected

- Seed ET04 as written (the organic-growth winner decided by restating 2019 bases through charter
  transformations, holding-company changes and branch purchases): rule application and data semantics
  as the decisive step, banned; its pairings and shape are also guard-blocked (probe cards above).
- The deposits world kept in Economics & Econometrics (a merger screen on pro-forma deposit shares,
  with post-merger run-off conditioned on branch overlap as the forward step): the screen is a filed
  formula, and crediting run-off is not how a competitive screen is computed, so the decisive step was
  either rule application or not the field's method.
- The deposits world in Survey Research & Official Statistics (break-adjusted growth of a deposit
  series, projected seasonal factors with merger level shifts): the decisive step reduced to restating
  history on current membership, which is task446 v1's spent driver, or to a stated statistical rule;
  projected seasonal factors for a state-chartered deposit series are not a real product.
- The deposits world in Urban & Regional Science (banking access after a merger's branch
  consolidations): the access computation is a stated distance rule applied to a branch list.
- A natural experiment in which every earlier practice had the same plan mix, so the pooled capture
  reproduced every earlier purchase: the validated-decoy architecture (the record blesses the wrong
  method and only the forward mix breaks it), banned; the earlier practices' mixes are set apart so the
  pooled rate misses each of them.
- Card drafts: objective, C and a quantity figure were blocked by test.same_puzzle_older (five
  builds); `decomposition_attribution` was blocked by test.same_driver_older (task119 v2, task38 v3);
  every pattern E variant was blocked by both tests. The decision is the office's real one (proceed or
  close) and the projected increase is graded beside it.
- A second pending notice as an ask (the same projection on another transaction): H18, a second
  decision riding in the same file.
- An ask for each earlier purchase's realised change in referral spending: it is the per-practice
  heterogeneity that points at the moderator, so it would teach the ladder.
- Static placements in the history, with only the transported mix (Brightwater's patients mostly in
  plans placing Ledgestone in tier one) separating the answer: the product-and-system model and the
  tier model then reproduce the history identically, so no filed criterion can choose between them
  and a literal reader has a fork; the history now carries Norbridge's 2024 re-tiering of Wolf River
  and the projection carries Bayfield's 2025 placement of Ledgestone, which only the tier model
  reproduces and transports.
- Relative price by system and carrier (15 cells) as an ask: every device it could carry (capitated
  encounters, one carrier's reprocessing, units on basket lab codes) moves two or three of the fifteen
  cells, so a device-blind solver keeps four-fifths of it; dropped.
- The share of each Manitowoc County site's 2024 revenue the deal moves, as the coupled ask: any
  site-level device (a reprocessing, a billing conversion, late payment) lands on Brightwater's own
  referral rows at the same sites, which the main call reads, so the ask could carry no device without
  breaking mess neutrality; replaced by Ledgestone's residence-based market share, whose devices sit on
  other residents' rows.
- The parties' share of office visits as a third ask: dropped to keep the prompt under 1,000
  characters with two multi-dimensional asks; its devices (a network that bills from Sheboygan,
  telehealth billed at the office place of service with modifier 95) stay available for an ask-only
  revision.
- Pre-acquisition shares that differ by tier: the counterfactual for a tier-one patient whose plan
  re-tiers between baseline and projection year becomes ambiguous (the deal-caused shift against the
  re-tiering's own shift); pre-acquisition shares are the same for every tier.
- A history extract scoped by notice only: Northpoint's orthopedists (no notice) would have no
  history and arthroscopy capture would be unobserved; the extract is scoped by reassignment records,
  so Northpoint is in it and the register-only read is an Ask C device instead.
- Rule 4.05 with closeness alone: a finer split of the tier model by carrier came closer on noise
  (0.50 points against 0.86), so a literal reader had to take it, and projected it moved five of Ask
  B's after cells by 0.1 point; 4.05 now lets a finer estimate replace a coarser one only when it is
  a full point closer.
- The projection with the fitted share at full precision: Ask B's after cells moved by 0.1 point
  between estimator forms a few ten-thousandths apart; 4.05 states the share in whole per cent, which
  every form rounds to the same 86.
- A history population left to "practices acquired", with each practice dated by its organisation
  event: literally, a practice whose number was retired has no referred services after it, and
  Northpoint has no event at all; 4.05 now takes the physicians who joined by acquisition (appendix
  A5), each service dated against its own physician's joining date.
- A late-paid device on a single employer group: too few lines to move an Ask B figure; two groups on
  Lakefront's self-funded PPO carry it.
- Facility names built from local street names that matched real outpatient centres in the region:
  renamed.
- Rule 4.05 with a filed selection criterion (the back-test over the closed acquisitions, then a
  parsimony clause on top of it): task445 and task446 v2 pin their open methods with the same organ,
  and three consecutive builds with a filed back-test read as a template (`determinism-check` §1, form
  3 never in consecutive builds). The criterion is removed; 4.04(b) and 4.05 file the estimand (the
  share expected for each service in the projection year, its measurement and its rounding) and the
  records force the method (form 1): the tier split is absolute in every practice and product,
  Norbridge's re-tiering of Wolf River moves its Tiered EPO patients inside the history, and the
  acquired practices' shares were rebuilt product by product so every finer cell states 86 and nil.
- An expected share worded in the singular ("the expected share is estimated from ..."): its literal
  execution is one pooled number, the easy answer from a reading rather than a method; 4.04(b) files
  the share expected for each service.
- The first ask layer (the increase split by part and service line with its chart, Ledgestone's county
  shares in 2024 and after the referral shift, Ledgestone's physicians each 1 January and those who joined
  by acquisition): the split, the after cells and the chart were keyed to the call's construction, and
  every device was settled by a filed sentence (appendix A2's residence, versions, units and runout, A4's
  control and credentials, A5's joining rule), so a response that landed the call kept every figure (pair
  ceiling 72). Replaced by the review's two standing exhibits, each held by a device no filed sentence
  settles.
- A bilateral knee film billed as one line with modifier 50 and two units beside hospitals' RT and LT
  lines: "how many services" then read as lines or as units. Every bilateral service is two lines now and
  A2 counts units.
- Kewaunee's endoscopies and arthroscopies left to the movers and the outreach top-ups: no second-plan
  copy fell in either cell, so the cracker kept four figures. The Manitowoc gastroenterology and
  orthopaedic groups now see Kewaunee patients.
- Second-plan claims on Mishicot's office visits: the copies grew Ledgestone's primary-care numerator with
  its denominator and left that share 0.06 points from the golden on the cracker's path. Mishicot's office
  files no second-plan claims.
- Office visits counted in person or by telehealth, and replacements on Kinnickinnic's professional
  lines: telehealth and the replacements pushed against the late payments, and four-mistake combinations
  landed back inside a bin on three specialty shares. A3 counts in-person visits only and the professional
  replacements are gone.
- The new lines drawn by their position in the claim stream: tuning one exhibit's volumes moved the
  other's cells. Each new line now draws from its own key.
- The judge's optional pin naming the carriers' provider file as the source of a physician's specialty:
  it would settle the Exhibit 2 device by a filed sentence the cracker executes; A3 defines specialty as
  the classification of the physician's taxonomy instead, which closes the code-to-specialty reading
  without naming a source.
