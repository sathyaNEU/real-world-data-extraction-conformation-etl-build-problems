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
| Shape | 07, grid of cells: the call and the 2026 increase, then the review's two market exhibits (appendix A2 and A3): the commercial patients living in Manitowoc and Kewaunee counties whom Ledgestone's and Kinnickinnic's physicians saw in person in 2024, by specialty (8 cells), and whom each independent practice saw (5 cells), and the patients the independent practices referred for outpatient imaging, endoscopy and arthroscopy (7 cells) |
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

## Three rules

Written on 2026-10-16, when the build came back from the house review; the card has carried
`stump_class: analytical`, `analyst_test` and `domain_test` since it was registered.

- **Task type:** `payment-claims-health-plan-analytics`, which the taxonomy lists against ETL and AD in
  Healthcare Delivery & Health Economics: all-payer claims, eligibility and provider files conformed into the
  quantity a filed regulation defines.
- **Domain test:** the deciding quantity is the health-economics projection of a vertical integration's
  spending effect, professional price convergence plus referral capture into hospital outpatient departments,
  and the field's own method for the capture half is a capture model estimated on closed acquisitions and
  moderated by the benefit design that decides what a referral costs the patient.
- **Swap:** "which of two depots will hold more stock after the merger, projected from last year's movements"
  has no benefit design standing between the owner and the patient, so there is nothing for the capture rate
  to be conditional on and nothing to transport across a changed mix; the task stops making sense.
- **Layer 1:** claims at header and line grain with replacement and void submissions, a layout revision
  between submission years, identifiers that do not line up (NPIs, billing TINs, CMS certification numbers),
  coordination-of-benefits copies across two carriers, the 30 June 2025 paid-through cutoff, NPI reassignment
  spans with Northpoint's orthopedists moving one at a time, Brown counted as Brightwater under 4.02(e), the
  Medicare Advantage file excluded under 4.02(b), and a group taxonomy reported on every one of a practice's
  claim lines. Each is what these systems produce, and none decides the call.
- **Layer 2:** the capture rate is transported from closed acquisitions to a projection population whose
  benefit-design mix is different, so the estimand is the share expected under each member's product as that
  product stands in the projection year, not a blend of the mix the history happened to hold.
- **Decisive step:** recognising that the share a referral moves is gated by the acquiring system's tier
  placement under the member's product, that the placements changed (Bayfield places Ledgestone first from
  plan year 2025, Norbridge placed Wolf River first from 2024), and that the share is therefore 86 per cent or
  nil rather than any pooled blend of them.
- **Not semantics:** every field, code and definition reads the same on both routes. The rule's terms, the
  claim layouts, the void and replacement codes, the paid-through cutoff and the ownership register are read
  correctly by the analyst test, and the wrong answer still comes out, because what differs is the population
  the capture rate is estimated over and carried to, not the meaning of anything in the files.
- **Not rule application:** no filed sentence says what differs between products, names tier placement, or
  tells the analyst to look at the tier filings. 4.04 and 4.05 file the estimand's unit (a service, a product,
  the projection year) and 4.05 files the estimation sample; the gating variable, the natural experiment that
  identifies it and the 2026 placements are the analyst's to find, and R4 of the ladder shows that finding the
  unit without finding the gate still files close at $1.633 million.
- **Analyst test:** a strong analyst who conforms every claim, span, ownership change and rate exhibit
  correctly and reads the regulation correctly measures the shift on the closed acquisitions, finds a capture
  share that reproduces each of them, applies it to Brightwater's referrals and files close at $1.4 to
  $1.6 million, because the history's mix of benefit designs is not the projection population's.
- **Estimand:** rule 4.04 and 4.04(b), that every baseline service is projected as the same service for the
  same member under the same product delivered in the projection year, and moves in the share expected for
  that service under the member's product as the product stands in the projection year, with 4.05 fixing the
  estimation sample and the whole-per-cent rounding.
- **No decoy:** nothing is planted to be caught. No figure in the pack is wrong, no memo argues the wrong
  answer, no artifact ranks the two outcomes, and the difficulty survives deleting every number that is not an
  input: the HCRIS extract is a genuine non-input distractor, not a trap.
- **No certified replay:** no published figure in the pack states the projection, the increase or either
  exhibit, so the method cannot be recovered by reproducing one.
- **Lesson:** a rate estimated on closed cases is only the rate the decision needs where the cases' mix
  matches the population the decision funds; when a filed estimand says "for this member, under this product,
  in the projection year", the mix is the estimand and not a nuisance to average over.

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
| SF13 | what the expected share is a share of | one share for each service and product, the share expected under that product as it stands in the projection year (86 per cent where the product places Ledgestone first or has no tiers, nil where second) | one share pooled over the whole estimation set (44 per cent); one share per service line pooled across products (arthroscopy 37, echo 44, GI 55, imaging 41, lab 41 per cent); the share under the member's product at the placement the product held in the baseline years | close, $1.5 million either way ($0.9 million referred pooled or by line, $1.6 million at the historical placement) | rule 4.04(b), the share expected "for that service under the member's product as the product stands in the projection year", and rule 4.05, "A share is estimated for a service and a product ... the office does not estimate one share across products" |
| SF14 | Bayfield's terms (Exhibit C, sheet Bayfield terms) | whole per cent of the CY2025 Medicare amount (405 per cent for imaging, 155 echocardiography, 160 endoscopy, 115 arthroscopy, 230 laboratory) | the column's value read as a per cent where it was stored as the multiple (4.05 per cent of Medicare, the reading the stage 4 judge raised on a93914356) | close, about $0.64 million | the column holds 405, 155, 160, 115 and 230 under its header "Percent of Medicare", the sheet's first line pays "the percentage below of the Medicare amount", and checks.py asserts that reading prices every Bayfield code at the agreement's rate and reproduces the referred increase |
| SF15 | a patient (both exhibits, "how many commercial patients"; A2 and A3, "each person is one patient") | the person behind the member keys: a second plan's key whose claims report the visits another key's claims report, priced on that claim's member liability, with one birth year, sex and ZIP, and a second record whose facility claim reports a service the same carrier paid under another key with one birth year, sex and ZIP, are that member's | each member key a person; birth year, sex and ZIP alone; the carrier with birth year, sex and ZIP; one service under two carriers only | not the call: every figure high (1 to 451); every figure low (3 to 5,413); Exhibit 2 every figure low and Exhibit 1 ten low, two high, one landing; Exhibit 1 the golden's and Exhibit 2 the member keys' | C1, asserted (convergence_checks): every matching that reads the claims' services across carriers and at one carrier, the golden's pricing link included, files the golden's twenty figures; the others split one person or merge different people, which the claims show (a second plan pays on the first's liability, one carrier pays one service twice) |
| SF16 | living in the two counties | the ZIP on the eligibility span of the claim's key and product that covers the date of service | the member's ZIP at any time in 2024 | not the call: Exhibit 1 up to 19 high, Exhibit 2 up to 6 | A2 ("while residing in the two counties", "the eligibility span that covers the date of service"), A3 |
| SF17 | the gastroenterology and orthopaedic practices | a practice whose physicians all hold the specialty in the provider files | the practice's name | same call: Manitowoc Digestive Care and Shoreline Orthopaedic Associates either way | same call (A2's last sentence) |
| SF18 | each independent practice there other than Brightwater | each number billing 2024 office visits at locations in the two counties that no hospital system owns or controls, read from the register as in A4, Brightwater's apart | a clinically integrated network's participant (Harbor Lakes Clinic) counted in or out | same call: no network participant bills a visit in the two counties | same call (A4: participation is not control) |
| SF19 | Ledgestone's physicians | billing under a number Ledgestone owns or controls on the date: Ledgestone Medical Group's and Mishicot Family Practice's (affiliated, controlled) | Ledgestone Medical Group's number only | not the call: Ledgestone primary care 2,432 to nil | A4 ("affiliated, controlled") and the register |
| SF20 | specialty | the classification of the physician's own taxonomy in the carriers' provider files | the claim's rendering taxonomy | not the call: Kinnickinnic +157, -219, -422, -306 | A2 ("as the carriers' provider files record it rather than as a claim reports it") |
| SF21 | saw in the office | in person: 99202 to 99215 at a location in the two counties, not at place of service 10 or with modifier 95 | telehealth visits counted | not the call: up to 134 high | A2 |
| SF22 | the practice that referred | the practice whose number the referring physician billed under on the date (the NPI reassignment history) | the provider file's billing number | same call: the same figures (no independent practice's physician changed number in 2024) | same call (4.02(e)) |
| SF23 | the patients each practice referred | every commercial resident of the two counties whose service a physician of the practice referred | only the residents the practice saw in the office in 2024 (Exhibit 1's) | not the call: every figure low (56 to 826) | the prompt names the residents ("commercial patients living in those counties"), and A3 defines the referred patients without an office visit |
| SF24 | 2024 | every 2024 date of service, whenever paid | rule 4.03's runout | not the call: 0 to 33 low | A2 and A3 ("whenever paid") |
| SF25 | physicians | doctors of medicine or of osteopathic medicine | Mishicot's nurse practitioner counted | same call: the same figures (she holds no specialty and her patients see its physicians) | same call (A4) |
| SF26 | the latest version | net of voids, a replacement over its original | every version as filed | same call: the same figures (a corrected visit keeps its patient; no independent practice's referral is replaced or voided) | same call (A2, A3) |
| SF27 | the system or practice a visit counts for | the one under whose taxpayer identification numbers the visit's claim was billed: Brightwater's gastroenterologist, open-ended under Brightwater's number and, from 6 February 2023, Kinnickinnic Physician Network's, has his Kinnickinnic-billed patients in Kinnickinnic's gastroenterology and his Brightwater-billed ones in no exhibit cell | every visit of a physician whose reassignment history holds the system's number; every visit on a day he billed a visit under the system's number; a physician holding two numbers at once left out | not the call: Kinnickinnic gastroenterology 520, 311 or 174 against 219, every other figure unchanged | A2 ("A visit counts for the system or the practice under whose taxpayer identification numbers its claim was billed"), as rule 4.03 counts a target practice's services billed under its taxpayer identification numbers |

The stump is none of these readings: every row lands the golden's call or is refused by the cited rule,
and `generator/checks.py` asserts each (SF1 to SF14 on the call; SF15 to SF27 on the exhibits, where "not the call"
names the figures the reading files and the cited sentence or the records refuse it). SF13 was added on 2026-10-16, when the house review
returned the build: the rule as first shipped left the share's unit of analysis unfiled, so a reader who
executed 4.05's own sentence over the set 4.05 defines reached $1.5 million and close, and the reading that
reaches the golden was closed in this note by the records rather than by a quotable sentence. The unit of
analysis is part of the estimand, which `determinism-check` section 1 requires filed literally, so it is now
filed at authority in 4.04(b) and 4.05. What is still not filed, and still the whole difficulty, is what
differs between products: that the acquiring system's tier placement under the member's product gates whether
the referral moves, that the placements change (Bayfield places Ledgestone first from plan year 2025, Norbridge
placed Wolf River first from 2024), and that the share is 86 per cent or nil rather than any blend of them.
The ladder's own arithmetic shows the pin costs the call nothing: R4, the share product by product or by tier
at the 2024 placements, still files $1.633 million and close.

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
| 10 | Rounding path | the expected share in whole per cent first (4.05), then sum in dollars and round each graded figure once | the parts sit $2,700 or more inside their $10,000 bins (arthroscopy, $237,732, the tightest) and the total $40,795 inside its $0.1 million bin (asserted at $1,000 and $20,000); the exhibits are whole counts of patients, rounded nowhere (the twenty differ and none is a round hundred, asserted) |
| 11 | Tie-break | none | no ties exist |
| 12 | Maturity | baseline runout to 30 June 2025 | filed; late-paid claims sit only on ask rows (zero-count asserted) |
| 13 | Order of operations | reprice, then sum | commutes |
| 14 | Row order | none | C1: two row orders give the same bytes (asserted) |
| 15 | Duplicate resolution | latest version of a claim (replacement over original, void removes both) | filed (4.02(c): latest version, net of voids); the claims carry the X12 frequency codes (1, 7, 8; layout 2.4's O, R, V), every replacement and void names its claim and every void carries negative units and amount (asserted); C1: no replacement or void on the main rows |
| 16 | Identity normalisation | NPI as the physician key, TIN as the billing entity, facility NPI to system through the directory | C1: Ledgestone's three sites share one chargemaster, so the site a moved referral lands at cannot move its price |
| 17 | Netting | net change (a referral moving off a dearer site lowers spending) | filed (4.06: with-transaction spending less baseline) |
| 18 | Dimensional units | dollars; units of one on every main-row line | C1 asserted |
| 19 | Code semantics | claim frequency codes, place of service, product to tier by plan year, ZIP to county | the frequency codes as in row 15; place of service 10 and modifier 95 filed in A2; ZIP to county filed in appendix A6 (asserted through the extractor the golden and the verifier use); product to tier from the placement file and the product reference's tiered_network flag |
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
- No control total, published figure or reconciliation column ships; provenance and row counts live in
  `metadata.json` only.

## Ask sheet

The asks are the review's two standing exhibits. Rule 4.07 says the preliminary review states the projected
increase, its professional and referred parts, and the exhibits the market oversight unit maintains in its
technical appendix; appendix A2 and A3 define them. Each is a count an all-payer claims analyst reports for a
notice review: how many lakeshore patients each system's and each independent practice's physicians see, and how
many patients each independent practice sends to outpatient facilities. Both count people on rows outside the main
call's population and neither needs the call or its construction, so the cracker and the mirror file the same
exhibit figures. Each turns on one judgment that no field announces and the rows force: which member keys are one
person.

Main block (recommendation and critical components): the call; the 2026 increase in $ millions to one
decimal; the parts 4.07 names (professional $610,000, referred $1,600,000); the 86 per cent measured on the
earlier acquisitions; Bayfield's first-tier placement of Ledgestone from plan year 2025. The cracker keeps
all of it. The mirror (R4) keeps the professional part, which is right on every rung (`r` about 3).

**Ask 1, Exhibit 1 (appendix A2 and A4): the commercial patients living in Manitowoc and Kewaunee counties whom
Ledgestone's and Kinnickinnic's physicians saw in person in 2024, by specialty, and whom each independent practice's
physicians saw (13 figures).**
- Golden: Ledgestone primary care 2,432, gastroenterology 57, orthopaedic surgery 133, cardiovascular disease
  117; Kinnickinnic 5,967, 219, 422 and 306; Algoma Family Health 1,716, Kewaunee Area Clinic 1,751, Manitowoc
  Digestive Care 539, Rapids Road Family Medicine 3,140, Shoreline Orthopaedic Associates 1,597.
- H18 home: a standing exhibit of the same review (4.07), the patient base each system and each independent
  practice holds in the lakeshore, which the referral shift and any later purchase draw on; the call does not turn
  on it. Use: the Attorney General's health care division reads it with the call.
- Primary device (D7, the true key elsewhere: one person under two member keys at two carriers): 1,230 members are
  covered twice, under their own plan and as a spouse or child under a second carrier's plan, and the second
  carrier's professional claim for a visit follows the first carrier's payment, priced on what the first left the
  member to pay. The database's person index linked 301 of the 1,210 with lines on file; for the other 909 the second
  carrier's spans and claims sit under a member key of their own (one carrier, relationship spouse or child, the
  member's birth year, sex and ZIP), 783 of them holding 3,031 professional lines (2,128 office visits) and no
  facility line. Counted on the member keys, each of those people is two patients in every cell where the second
  plan paid a visit. Key uniqueness, exact duplicates, the amount identity on every row and the claim-to-eligibility
  join all pass, because each copy joins its own key's span. Only a cut across keys finds it: a claim under one key
  that reports the visit another key's claim reports (date, code, modifier, rendering physician, billing number,
  units) to another carrier, priced on exactly that claim's member liability, with both keys giving one birth year,
  sex and ZIP that day. Fair handling (golden.link_members; the verifier's own code agrees; asserted against the
  people the simulation generated): link the keys so, then count A2's way.
- Over-cleaning half: a person key on birth year, sex and ZIP merges different patients (every figure 4 to 5,413
  low); the one-carrier cleanup (one carrier, birth year, sex and ZIP) merges different patients at one carrier and
  leaves the second plans' keys apart, two errors running opposite ways (ten figures 5 to 4,000 low, two 1 high, and
  Ledgestone gastroenterology lands, recorded rather than tuned).
- Pin test: A2 pins in person, the codes, the location, residence on the date, the year, whenever paid, the specialty
  source, the latest version, the number a visit counts for and each person once; A4 pins physicians and control.
  The device sits in the one dimension the pins leave open, which keys are one person.
- Hazards: H3 control, H4 residence, H6 physicians (a no-op), H7 telehealth, H8 copies under one key (a no-op on
  people), H9 group taxonomy, H10 Ledgestone's corrections (a no-op on people), H11 a physician under two numbers
  (settled by A2's attribution sentence).
- Path: eight files (the 2024 professional claims, the eligibility spans, the product reference, the carriers'
  provider file, the provider ownership register, the notice for Exhibit A and Brightwater's number, the technical
  appendix A2, A4 and A6, rule OHCCR 4.02) and twenty-one columns (submitter_code, claim_frequency_code,
  member_id, product_id, service_from_date, procedure_code, procedure_modifier_1, procedure_modifier_2,
  place_of_service, quantity, allowed_amount, member_liability_amount, rendering_provider_npi, billing_provider_tin,
  service_facility_zip, coverage_start, coverage_end, birth_year, sex, member_zip, primary_taxonomy).
- Stops (make.py prints each, checks.py asserts each), in patients, Ledgestone primary care, gastroenterology,
  orthopaedic surgery, cardiovascular disease; Kinnickinnic the same; then Algoma, Kewaunee Area Clinic, Manitowoc
  Digestive Care, Rapids Road and Shoreline:
  - member keys as the files give them (the cracker): +145, +2, +6, +6; +451, +9, +23, +25; +137, +142, +35, +236,
    +118
  - the claim's taxonomy: Kinnickinnic +157, -219, -422, -306, every other figure unchanged
  - telehealth counted: +91, 0, 0, 0; +134, +5, +16, +8; +37, +30, +6, +131, +33
  - residence not read: +11, +1, +1, 0; +19, +2, +2, +1; +12, +5, +1, +9, +14
  - nurse practitioners counted, versions as filed: no figure moves (asserted)
  - every combination of the four (11 pipelines): none lands back on a figure one of its errors moves.
- Realism: dual coverage is ordinary in commercial claims, a second carrier's claim follows the first carrier's
  payment, and an all-payer database's person index that fails to link a dependent's record under a second carrier
  to the person's own record is the commonest identity fault in multi-payer data.

**Ask 2, Exhibit 2 (appendix A1 and A3): the commercial patients living in the two counties whom each independent
practice referred for outpatient imaging in 2024, and whom the gastroenterology and orthopaedic practices referred
for endoscopy and arthroscopy (7 figures).**
- Golden: imaging, Algoma Family Health 171, Kewaunee Area Clinic 164, Manitowoc Digestive Care 59, Rapids Road
  Family Medicine 266, Shoreline Orthopaedic Associates 742; Manitowoc Digestive Care's endoscopy 865; Shoreline's
  arthroscopy 234.
- H18 home: the second standing exhibit (4.07), the outpatient flow each independent practice directs, the flow a
  system's next purchase would draw on; the call does not turn on it.
- Primary device (D7, the true key elsewhere: one person under two member records at one carrier): 125 members
  hold a second member record at their own carrier, opened with their enrolment and never merged, and one of their
  2024 outpatient services, referred by an independent practice, was billed under it as well and paid again, each
  claim adjudicated on its own record's cost sharing. The second records hold 133 facility lines, one claim each;
  124 of those people fall in an exhibit cell, one in eighteen of the 2,294 people the independent practices
  referred. Counted on the member keys, each of them is two patients in the cell. The battery passes:
  keys are unique, no row repeats another even without the claim number (or the member key: the second claim's
  cost sharing and paid date are its own), every claim joins a span, and the second record's spans repeat the
  member's own from 1 January, as every key's coverage starts. Only a cut by service finds it: two keys of one
  carrier whose facility claims report one service (date, code, modifier, facility, referring provider, units),
  with one birth year, sex and ZIP that day. Fair handling (golden.link_records; the verifier's own code agrees;
  asserted against the people the simulation generated): such keys are one person, then count A3's way.
- Over-cleaning half: the careful solver's natural cleanup of duplicate records (one carrier, birth year, sex and
  ZIP) merges different patients at one carrier (every figure 2 to 162 low), and a person key on birth year, sex and
  ZIP alone merges more (3 to 418 low); a duplicate check run without the member key finds nothing while it keeps the
  cost sharing, and without it folds different patients' identical services in the busier cells (Shoreline's imaging
  -13, Manitowoc Digestive Care's endoscopy -33, Shoreline's arthroscopy -2) while the four smaller imaging cells
  land.
- Pin test: A3 pins the line (A1), the facility claims, residence on the date, the year, whenever paid, the latest
  version, the referring physician's practice on the date (4.02(e)) and each person once; the device sits in which
  keys are one person.
- Hazards: H1 versions (a no-op), H2 late payment, H4 residence, H5 RT and LT lines (a no-op on people).
- Path: nine files (the 2024 facility claims, the eligibility spans, the product reference, the NPI reassignment
  history, the carriers' provider file for the practices' names, the provider ownership register, the notice for
  Brightwater's number, the technical appendix A1, A3 and A6, rule OHCCR 4.02) and seventeen columns
  (submitter_code, claim_frequency_code, original_claim_control_number, member_id, product_id, service_from_date,
  procedure_code, procedure_modifier_1, quantity, service_facility_npi, referring_provider_npi, coverage_start,
  coverage_end, birth_year, sex, member_zip, billing_tin).
- Stops, in patients, imaging for Algoma, Kewaunee Area Clinic, Manitowoc Digestive Care, Rapids Road and Shoreline,
  then Manitowoc Digestive Care's endoscopy and Shoreline's arthroscopy:
  - member keys as the files give them (the cracker): +8, +9, +1, +16, +35, +47, +8
  - residence not read: +1, 0, 0, +1, +3, +6, +2
  - versions as filed: no figure moves (asserted)
  - the one combination (the cracker with residence not read): off every figure.
- Realism: a carrier's enrolment system opens a second record when an enrolment is keyed twice, and a facility that
  registers the patient against the other record bills the service under it; the carrier pays both until a recovery
  audit, and the second adjudication applies that record's own accumulators.

**Hazards (cross-cutting).**

| Hazard | What it is | Ask 1 | Ask 2 |
|---|---|---|---|
| H1 versions | Kinnickinnic's referrals to its Manitowoc hospital: replacements (code 7) and voids in error with rebills (code 8), the X12 values the claims carry | none | none (no independent practice's referral is replaced or voided; asserted) |
| H2 late payment | two self-funded groups' fourth-quarter claims paid in July and August 2025, inside the extract | A2 counts whenever paid; a runout read in drops 0 to 33 patients | 0 to 9 patients |
| H3 control | Mishicot under Ledgestone (register and Exhibit A) | Ledgestone primary care to nil on Ledgestone Medical Group's number only (Mishicot's are all of them) | none |
| H4 residence | 4 per cent of the other lakeshore members move, spans cut at the move | not read: up to 19 patients | up to 6 |
| H5 RT and LT | bilateral knee films and arthroscopies on two lines | none | none (one patient) |
| H6 physicians | Mishicot's nurse practitioner (A4: physicians only) | none (no specialty, and her patients see its physicians; asserted) | none |
| H7 telehealth | place of service 10 or modifier 95 (A2) | counted: up to 134 patients | none |
| H8 copies under one key | the second carrier's claims of the 301 members the person index linked | none (one key, one patient) | none |
| H9 group taxonomy | Kinnickinnic's business office reports its family-medicine code for every physician it bills (A2) | from the claim: +157, -219, -422, -306 | none |
| H10 Ledgestone's corrections | replacements citing Ledgestone's own account number in the original-claim reference | none (a corrected visit keeps its patient) | none |
| H11 a physician under two numbers | Brightwater's gastroenterologist also bills under Kinnickinnic Physician Network's number, both open (closure row 1) | A2 counts each visit for the number its claim was billed under; read by his reassignment history Kinnickinnic gastroenterology is 520, by his billing days 311, without him 174 (SF27) | none |

**Referees.** The eligibility file: every second plan's key holds one carrier's spans as a spouse or child, with the
birth year, sex and ZIP of the member its claims link it to, and every second record's spans repeat its member's
own. The carriers' provider file: one taxonomy per NPI across every carrier. Neither hands over a count: the
eligibility file counts nothing and the provider file ranks nothing.

**No marker, no oracle.** The second plans' claims carry frequency code 1 and fill every column as first claims do;
a second plan's key is a dependent with one carrier, as about 19,600 other keys are, its coverage starting on 1
January as every key's does. A second record holds one facility claim and no professional claim, as about 7,960
other keys do; its spans start on 1 January like every key's, and its claim carries its own cost sharing and paid
date. No control total ships.

**The separation line.** Zero device and hazard rows in the main call's population, asserted by count: no
main-call member is covered twice or keyed twice; Brightwater's professional rows are originals; no second record's
claim is a main-call row; the second plans' copies are professional claims only, so the facility referrals R1 reads
and the 2024 Ledgestone site prices of the grid's second column do not move. The only keys one carrier's claims join
beyond the second records are one pair of Brightwater's own patients, namesakes on one service, in no exhibit cell
(asserted: they move no figure). `generator/main_call_ref.json`, written from the build before the ask layer, holds
every main row, every reference file the call reads whole (Exhibit C by its rates) and every main figure;
checks.py asserts the current build reproduces it.

**Cracker sheet.**

| Ask figures | n | The cracker's path (lands R5, runs the battery, executes A1 to A4 and 4.02 on the member keys as filed) | Cracker |
|---|---|---|---|
| Exhibit 1, Ledgestone's and Kinnickinnic's patients by specialty | 8 | each person under a second plan's key counted twice: +145, +2, +6, +6; +451, +9, +23, +25 | miss |
| Exhibit 1, each independent practice's patients | 5 | the same: +137, +142, +35, +236, +118 | miss |
| Exhibit 2, the independent practices' referred patients | 7 | each person with a second record counted twice: +8, +9, +1, +16, +35, +47, +8 | miss |

**Mirror sheet.**

| Ask figures | n | The mirror's path (stops at R4, then reads A1 to A4 on the member keys as filed) | Mirror |
|---|---|---|---|
| Exhibit 1, both blocks | 13 | the same figures as the row above it | miss |
| Exhibit 2 | 7 | the same figures | miss |

Measured by: generator/ceiling.py, on target.zip (md5 02e9335058bbd8a9d816bbbef030e481): the cracker and the mirror
on their own code apart from golden.py, which agrees with golden.py's route on the member keys as filed; the full
includer reproduces figures.json exactly, 20 of 20.

Mirror leakage: 0.0 per cent of ask weight (the mirror stops at R4 and reads both exhibits as the cracker does).

Pair ceiling: 28.5 (measured, the worse of the ask sheet's weighting, 38 / 7 / 55 with r = 3, at 27.5, and the
comparable one with r = 5; the cracker 38 + 7 + 0 = 45, the mirror 3 + 7 + 0 = 10; two careful responses on the call,
45.0 each).

The honest exposure (ceiling.py prints each route on the call beside the mirror): a response that reconstructs the
people under any carrier keeps all twenty, 100.0 and a pair of 56.0; across two carriers only it keeps Exhibit 1's
thirteen, 80.8 and 46.4; the duplicate check without the member key and without the cost sharing keeps four of
Exhibit 2's imaging cells, 56.0 and 34.0, and with the cost sharing nothing; the one-carrier cleanup keeps Ledgestone
gastroenterology alone, 47.8 and 29.9; a person key on birth year, sex and ZIP keeps nothing. Criteria: the call, the
increase, four critical components, twenty exhibit figures and two instruction criteria, 28.

## Pack plan

| File | Format | Rows | Role |
|---|---|---|---|
| `apcd_op_facility_claims_2024.csv` | CSV | 67,449 | spine: 2024 commercial outpatient facility claims for the directory's facilities, layout 3.1, paid through 31 August 2025 (a service paid twice under a member's two records at one carrier among them) |
| `apcd_op_facility_claims_2021_2023.csv` | CSV | 31,568 | the acquired practices' physicians' referrals 2021 to 2023, layout 2.4 |
| `apcd_professional_claims_2024.csv` | CSV | 73,099 | professional claims performed in Manitowoc and Kewaunee counties, 2024, a second plan's claims under its own member key where the person index did not link it |
| `apcd_eligibility_spans.csv` | CSV | 103,388 | member spans 2021 to 2024, cut at product, benefit period and address, one set per carrier for members covered twice (under a second key where the person index did not link them), and a second record's spans beside its member's |
| `apcd_product_reference.csv` | CSV | 14 | product, carrier, line of business, tiered network flag |
| `network_tier_placements_2020_2026.json` | JSON | | each tiered product's placement of each system by plan year, from the carriers' form filings |
| `provider_ownership_register.csv` | CSV | 21 | notices of material change and annual registrations |
| `npi_reassignment_history.csv` | CSV | 246 | physician to billing TIN spans |
| `carrier_provider_file.csv` | CSV | 1,042 | carrier-submitted provider records, name variants across carriers |
| `facility_directory.csv` | CSV | 20 | facility NPI, system, type, county |
| `N25-014_notice_of_material_change.pdf` | PDF | | the notice with Exhibits A and B |
| `N25-014_exhibit_C_ledgestone_rates.xlsx` | XLSX | | Ledgestone's facility rates by carrier (Bayfield in whole per cent of the Medicare amount by category, under a "Percent of Medicare" header) and professional schedule |
| `cms_opps_clfs_2025_wisconsin.csv` | CSV | 21 | the Medicare amounts the Bayfield terms reference |
| `ohccr_rule_4_preliminary_review.pdf` | PDF | | the rule (estimand, criterion, threshold) |
| `market_oversight_technical_appendix.pdf` | PDF | | service lines, the two exhibits (patients seen, patients referred), physicians and joining, the unit's ZIP-to-county assignment (A6) |
| `hcris_hospital_outpatient_extract_fy2023.csv` | CSV | 6 | distractor: cost report outpatient lines, costs and charges |
| `apcd_medicare_advantage_facility_claims_2024.csv` | CSV | 5,200 | distractor: Medicare Advantage claims for the same referrers, outside the commercial estimand |

17 files, four formats (CSV, JSON, PDF, XLSX), the eligibility spans at 103,388 rows, two distractors
named in `metadata.json` only. No file describes the data: provenance and row counts are in `metadata.json`. No filed document says that referrals follow tiers, that the share
depends on a plan's placement, or that placements change what an acquisition does.

## Assertion regime

`generator/checks.py` runs every assertion on each build (the count is in `pipeline.json`), and
`generator/verify.py` recomputes every graded figure from `target/` alone with csv, json, openpyxl and
pypdf, sharing no code with the generator: the answer and every component; every rung and its distance to
the threshold (each wrong rung 8 per cent or more below, the nearest at 16.5 per cent; the answer 10.5 per
cent above); the 24-cell correction grid; the records' structure (the tier model within two points of
every practice-year, every model outside the tier family 8 or more points off one; every finer cell,
every practice and Norbridge's Tiered EPO at Wolf River before and after plan year 2024 stating 86 and
nil); the estimator corridor; the semantic fork table, SF1 to SF14; the rule filing no selection
criterion; every graded figure's distance to its bin edge; the clean-data test; zero device and hazard
rows in the main population; the main call reproduced byte for byte against `main_call_ref.json`; both
exhibits' goldens against the people the simulation generated, the cracker off every figure, every stop moving a
figure and every no-op moving none, every combination of mishandlings (11 on Exhibit 1, one on Exhibit 2) off
every figure one of its errors moves; the two primaries (every second plan's key in the files linked back to its
member by the claims alone and no other key, holding only professional claims of one carrier as a spouse or child;
every second record linked back by its one facility claim, its spans its member's from the start, its claim on its
own cost sharing so that no line repeats it but for the member key, the only other one-carrier join a pair of
Brightwater's own patients that moves no figure; each primary alone accounting for every figure of its exhibit the
cracker misses); the person readings of SF15 (every matching that reads the claims' services files the golden's
twenty, the device and its over-cleaning halves off them); the asks' fork rows SF16 to SF26; the referees (one
taxonomy per NPI in the provider file, a second carrier's span under every second-plan claim); the
distractor-deletion test; the realism sweep (no two facilities with one count, no constant monthly series, no
recurring monthly totals, no round headline figure, the twenty patient counts all different and none a round
hundred); the input gates;
the submission's figures and the house checks; the prompt as one plain-text paragraph; two consecutive
builds byte-identical and the zip member for member; no shipped file or sheet describes the data, by name
or by content (no document names more than a fifth of a data file's columns), with the appendix's A6
ZIP-to-county assignment and the claims' own version codes asserted where the closures now live. The generator writes `generator/figures.json` and
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
- No Brightwater, acquired-practice or Ledgestone Medical Group patient-pool member has a second plan, and no
  second plan's facility claim is in the extract (the second carriers' facility claims are their recoveries).
  Forced by the separation line (the main call reads those members' rows, and the R1 rung and the grid's
  2024-price column read Ledgestone's facility referrals and site prices); mitigation: 1,230 lakeshore and
  Sheboygan members carry two plans, with second-plan professional claims at every lakeshore office, Ledgestone's
  and Kinnickinnic's included.
- One lakeshore commercial member in nine carries a second plan, and the person index left three in four of
  those dependents' second-carrier records unlinked. High but within what commercial populations of
  two-earner households and an index that matches dependents on their own identifiers produce; kept at the rates
  the earlier ask layer forced, at which the smallest Exhibit 1 cell (Ledgestone's gastroenterology) holds two such
  people.
- 125 members hold a second record at their own carrier, each with one facility claim, every one a service an
  independent practice referred. A carrier's duplicate records would spread across its membership; here they sit
  where Exhibit 2 counts them, since a second record elsewhere moves no graded figure. Each second record holds its
  member's coverage from the start, and its claim was paid 31 to 80 days after the first.
- Exhibit 1's and Exhibit 2's people are drawn apart: most of an independent practice's 2024 referred patients had
  no 2024 office visit with it in the extract (Shoreline's imaging, 615 of 742; Manitowoc Digestive Care's
  endoscopy, 826 of 865). A referral can follow an earlier visit or come by direct access, but a reader of both
  exhibits may find the overlap thin; the simulation draws a practice's referrals and its visits from its patients
  independently.
- Ledgestone's coding review corrected about a quarter of its two offices' 2024 lakeshore visits, and a
  correction is made only where the visit is the member's one visit that day with that carrier and number.
  The share was forced by the earlier Exhibit 2's direction discipline; it now moves no exhibit figure (a
  corrected visit keeps its patient) and stays as Layer 1 mess (H10).
- Exhibit C's facility rates are one chargemaster times a constant factor per carrier (Norbridge's are
  1.06 of Cedarbrook's on every code). The rates are main-call inputs, frozen through the ask-layer pass;
  a revision that may move the call can give each carrier its own negotiated schedule.
- Kinnickinnic's visiting specialists see patients in Manitowoc but their lakeshore patients' outpatient
  referrals are not in the extract's lakeshore rows. Accepted: no exhibit counts their referrals, and the
  Sheboygan rows carry their referral pattern.

## Stopping rule

Stump power is measured by the portal alone. A portal result where two responses land the call (proceed, with a
2026 figure inside the 2.2 bin) re-roots the build. A result with the call held and the top two at or over 70 goes
to the ask-only revision (`/fix-rubric`), and a determinism finding to `/fix-determinism`; neither moves the
decisive rung.

## Leak check

`leak.py --asof 2025-10-21` (the pack's export date) returns REVIEW with no LEAK, each line answered:
- `014` in the notice: the notice number N25-014, which the prompt names.
- 'Ledgestone Health' and 'Brightwater Medical Group' beside decision vocabulary in the notice: the
  certification block of the filing under review; both parties are named in the prompt.
- `4.05` and `4.06` in the rule: the rule's own section numbers, which the submission cites.
- Design-note vocabulary in the appendix and the rule (nine of the sweep's 25 terms each) and in the notice (three:
  carrier, service, exhibit): the field's ordinary nouns (product, history, records, service, carrier, member,
  projection, system, and the notice's own Exhibits A to C); no document connects tiers with referrals, the share
  that moves or the projection year, the rule files no selection criterion, the appendix's A2 and A3 define the
  patients each exhibit counts and the number a visit counts for, and say nothing of member keys, second plans or
  second records (the carriers appear only as the source of a physician's taxonomy), and A6 assigns ZIP codes to
  counties.
- Ranking artifacts: the carriers' provider file names seven of the twelve answer-set names (the systems and the
  independent practices) beside NPIs, billing numbers and taxonomy codes, one row per provider and carrier; the tier
  placements name the three systems beside tier numbers by product and plan year (a main-call input); the register
  names the practices beside numbers and dates. None counts a patient or ranks anything on either exhibit; the
  facility directory (INFO) lists facilities by system.
- Prompt gate, the rounding opener 'give' over the corpus quota: the call sentence's own rounding clause, frozen with
  the call by this repair; a corpus-window shell effect.

The isolated leak read on the replaced asks is the main thread's: its copy is the cut pack of 2026-11-01 with A2's
attribution sentence (target.zip md5 02e9335058bbd8a9d816bbbef030e481) and the prompt as filed.

Two isolated leak reads ran on the earlier asks, on the stage 3 pack and again after the appendix pins. Neither quoted a sentence for the decisive step,
found no file that ranks or answers, no file that exists only to help, no figure that reads as the answer,
and both called all nine REVIEW lines harmless. Their literal readings of 4.02 to 4.06 execute to the golden. Their
literal reading of those exhibits counted claim units and took specialty from the claim's taxonomy, the
cracker's path that ask sheet designed for (the second read named the provider file as a competing source;
the judge took it, from the records). Rulings on the first read's other points:
- Exhibit definitions without a paid-date cut, version netting stated only for spending, and
  "Internal Medicine, Gastroenterology" read as internal medicine: closed in the appendix (A2 and A3 count
  every 2024 date of service whenever paid, on the latest version net of voids; A3 maps each specialty to
  its NUCC codes and defines a physician's specialty as the classification of the physician's taxonomy).
  Hazards only; no figure moved.
- The export manifest's "lakeshore physicians" on the Medicare Advantage file: reworded to the two counties
  (the manifest itself no longer ships).
- Bayfield's percent-of-Medicare cells (4.05 shown as 405 per cent under the 0% format) and the CY2025
  amounts for a 2026 projection: harmless; the workbook stores percentages as Excel does, and 4.04 does
  not trend prices, so the filed CY2025 amounts are the only ones a literal reader can apply (the judge
  executed both the same way). Superseded on 2026-11-01: with no dictionary in the pack the stage 4 judge read the stored 4.05 as a second reading, and the column now holds whole per cent (SF14).
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

Later passes (`determinism_check_report_pass2.md`, `determinism_check_report_pass3.md`) read the asks this note no
longer carries. The asks were replaced on 2026-11-01 (pipeline.json `returned`).

Judge pass 5 (2026-11-01, on cdfe56c7cc749f93ba72279d4034d1e4, isolated, literal reading first): NOT_DETERMINISTIC,
FIX_NOW on one supplementary figure. The main call is forced and reproduces; every other exhibit figure reproduces;
each exhibit has one count of patients; "independent practice there" has one reading; Gate G forecasting,
analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical. The open cell was Kinnickinnic
gastroenterology: Brightwater's gastroenterologist (NPI 1451989697) is open-ended under Brightwater's number and
Kinnickinnic Physician Network's, and his reassignment history, his billing days or his exclusion gave 520, 311 or 174
against the golden's 219. Closed by the judge's WHAT, which moves no figure: A2 now says "A visit counts for the system
or the practice under whose taxpayer identification numbers its claim was billed." (SF27, asserted through both PDF
extractors, every Exhibit 1 figure filing under it). The judge rated the person merge on Exhibit 1 forced for a
rigorous solver and the build's second-weakest point; its optional pin (stating the merge in A2 and A3) would file the
asks' devices and is not taken. The readings a judge may raise on the asks are rows SF15 to SF27, each computed in
checks.py.

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
- 2026-10-14, after shipping: the prompt's "That turns on the increase in commercial spending the deal will cause in 2026 ... Put the call and that increase ... Give the increase to one decimal". Rejected on the house-fix register's H23: "the increase the deal will cause" presupposes a rise, a fact only the analysis establishes (rule 4.06's projected increase may be zero or less); it reads "how much the deal will change commercial spending in 2026", "that change" and "the change", every figure, file and rounding kept, and the reader re-run on the repaired prompt (clean on the prompt; its Q6 repeats read 1's view that 4.04 and 4.05 leave the call to rule application, against the judge's analytical, an open concern for the author).
- Returned 2026-10-16 by the house review, with both in-task determinism judges passing (gates A to G pass,
  F strong, the measured response a valid stump at an 11 per cent rubric) and the review nevertheless right on
  the determinism axis: rule 4.05 shipped as a complete recipe whose literal execution gives the other answer,
  which `determinism-check` section 1 bans outright, and both judges had closed the fork by argument rather
  than by a quotable sentence (this note closed it with "the records"). Repaired as a determinism fix with the
  call, the ladder and every graded figure frozen: the share's unit of analysis filed in 4.04(b) and 4.05, the
  cross-carrier duplicate filed in A2, the taxonomy source filed in A3, and the tier filings' purpose line no
  longer saying it is kept for another report. Not taken, and rebutted in the covering note: filing the tier
  stratification itself, which the review proposed and which would make the decisive step rule application; the
  claim that the exhibit figures are uncommitted, which block 4 of the submission has always carried; and the
  claim that the duplicate and taxonomy conventions were unpinned, which A2 and A3 already settled in terms
  both judges used. A filed back-test, the review's third suggestion, was refused because task457 in the same
  lane already ships one and an organ may not appear in consecutive builds.
- 2026-11-01, in-house re-check under the new leak gate (LEAK on `apcd_extract_data_dictionary.pdf`, which
  named all 50 columns of the files, and `export_manifest.csv`): the pack shipped a data dictionary (both claim
  layouts field by field, the 2.4 to 3.1 crosswalk, frequency, place-of-service and taxonomy codes, file scopes,
  ZIP to county) and an export manifest (each file's description, source, date and row count). Both are
  dropped. Provenance and row counts live in `metadata.json` only; the ZIP-to-county assignment, the one thing
  the exhibits cannot close without it (real lakeshore ZIPs straddle county lines), is filed once in the
  appendix as A6, the unit's own assignment (old A6 Sources is A7, no longer citing a dictionary); version
  handling stays filed in 4.02(c) and A2 and is closed by the claims' own X12 codes (asserted); place of service
  10, modifier 95 and the specialty codes were already in A3; the layout crosswalk, column glosses, file scopes
  and the relationship codes are left to the files (none is a main-call fork, and the ask devices stay
  unstated). The call, the stump, the ladder, every graded figure and the golden are byte-identical.
- 2026-11-01, the rubric repair (in-house: ceiling.py measured the cracker at 20 of 20 and the pair at 83.5).
  The second-plan copies under one member key (D1), Exhibit 1's primary and Exhibit 2's shared device: the
  10-16 determinism repair filed their handling in A2 and A3 ("one service however many carriers were
  billed for it", "A visit reported to more than one carrier is one visit"), so a response executing the
  appendix removed every copy. Kept as hazard H8; replaced by the person index's unlinked second keys (D7),
  which those sentences, executed on the member key, leave in.
- 2026-11-01, the rubric repair: Kinnickinnic's group taxonomy on its claims (an attribute at the wrong
  level), Exhibit 2's primary: A3's 10-16 sentence ("as the carriers' provider files record it rather than
  as a claim reports it") handed every response its remedy. Kept as hazard H9; replaced by Ledgestone's
  corrected claims citing its own account number (D2 versions), which A3's latest-version sentence,
  executed by the references, leaves counted twice.
- 2026-11-01: Exhibit C's Bayfield column as shipped through a93914356, 4.05, 1.55, 1.60, 1.15 and 2.30
  stored as Excel percentages (shown as 405% under a 0% format) beneath "Percent of Medicare". With the
  dictionary gone the stage 4 judge read 4.05 per cent of Medicare as a second reading (about $0.64 million,
  close). The column now holds 405, 155, 160, 115 and 230 under the same header and the readers take the
  value over 100; every rate is identical, and main_call_ref.json now digests Exhibit C by the rates the
  call reads (one digest from the old file's old reading and the new file's new one).
- 2026-11-01: the new devices at their first settings (half of the members with a second plan unlinked, at
  one member in eighteen with a second plan; a twelfth of Ledgestone's visits corrected; its lakeshore
  clinics still billing second plans). The cracker missed all twenty figures, but the combination test
  found pipelines landing back in a bin: the second keys missed with the runout in Kewaunee imaging and
  endoscopy, or with the over-cleaner in Manitowoc arthroscopy, and Ledgestone's orthopaedic and cardiology
  shares with telehealth and the runout. Raised to one in nine with a second plan, three in four unlinked, a
  quarter of Ledgestone's visits corrected and its clinics' second plans dropped; all 432 pipelines then miss.
- 2026-11-01, the pass-4 convergence repair: the stage 4 judge found the supplementary exhibits' person and
  replacement readings open (a second member key matched on birth year, sex and ZIP alone, with the service, or
  with the pricing; a replacement whose reference names no claim matched on the code, the physician or the
  number). Closed by C1 (pack.separate_namesakes, every matching that reads the services converging), after which
  the honest careful solver, executing the appendix's carrier and version sentences as worded with its natural
  de-duplication, kept all twenty exhibit figures (pair 82.5 and 83.5): the devices were spent, because the filed
  sentences pointed at the very cut that cracks them.
- 2026-11-01, the replaced asks: Exhibit 1 as residents' services by county and line with Brightwater's referred
  share (12 figures) and Exhibit 2 as Brightwater's and Ledgestone's shares of the office visits by specialty (8
  figures), with A2's and A3's carrier sentences ("one service however many carriers were billed for it", "a visit
  reported to more than one carrier is one visit"). Replaced by the review's patient exhibits: the patients each
  system's specialties and each independent practice saw (13 figures), and the patients each independent practice
  referred (7 figures), each person once and no sentence on carriers, keys or records. Ledgestone's corrections
  (D2) move no patient count and stay as hazard H10; the second plans' facility claims leave the extract so that
  each exhibit carries one device (the second plans' keys, professional only, and the second records at one
  carrier, facility only).
- 2026-11-01, the second records' first cut: opened at a 2024 re-enrolment (coverage from the first of the service
  month) and paid again on the first claim's exact amounts. They were the only keys whose coverage began after
  January, and a duplicate check run without the member key found every one, landing Exhibit 2 whole. Now each
  opens with its member's enrolment and its claim carries its own record's cost sharing; the same check finds none,
  and without the cost sharing it lands four smaller imaging cells and over-cleans three.
- 2026-11-01, the first prompt for Exhibit 2 ("how many of those residents each of those practices referred"):
  "those residents" also read as the practice's own Exhibit 1 patients, every figure 56 to 826 lower. Reworded to
  "how many commercial patients living in those counties each of those practices referred" (SF23).
- 2026-11-01: Algoma Family Health and Kewaunee Area Clinic drew one count (1,716 patients each) at the first
  build of the patient exhibits; Kewaunee Area Clinic's professional volume moved from 0.9 to 0.93 of its
  physicians' base, and the twenty counts now differ.
- 2026-11-01, judge pass 5 on cdfe56c7: A2 left the number a visit counts for to A4's physicians on a date, so
  Brightwater's gastroenterologist, open-ended under Brightwater's and Kinnickinnic Physician Network's numbers, gave
  Kinnickinnic gastroenterology 520 (his reassignment history), 311 (his billing days) or 174 (left out) against the
  golden's 219. A2 now files the WHAT, "A visit counts for the system or the practice under whose taxpayer
  identification numbers its claim was billed.", as rule 4.03 counts a target practice's services; no figure moved.
