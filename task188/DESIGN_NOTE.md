# task188 design note

Architecture 2 (re-root 2026-11-03). Architecture 1, the West Nile virus spray zone, is spent and stays at the portal
as shipped on 2026-10-13; its record is under `## Architecture 1 record` and every screen since is in
`## Tried and rejected`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task188.json`, architecture v2, drawn and filed 2026-11-03; v1 moved to
  the card's lineage as spent. `guard.py check`: PASS, no WARN, nearest drivers 0.06 (task27, task66, task120 v3) and
  0.05 (task196 v2, task89 v12).
- **Pairing:** Banking, Credit & Financial Risk, task type `fraud-aml-detection` (serves AD), a cell holding one live
  card (task196, scam incidence by two capture channels). The draw moved here after three passes on 2026-11-01 and a
  fourth on 2026-11-03 screened every other Anomaly Detection cell dead (`## Tried and rejected`).
- **Niche:** Harlow Reach Credit Union, a fictional credit union in the Lower Mainland of British Columbia. Its
  Business Services team, the first line that holds the business members' relationships, performs the enhanced due
  diligence the AML/ATF compliance programme requires on the members it classes as cash-intensive (full-service and
  limited-service restaurants, cafes, convenience and grocery retailers, bars, nail and beauty salons, car washes, coin
  laundries, mobile food vendors). Each January it reviews the segment on the year just closed and refers to the
  Financial Intelligence Unit (the Unit), the second line, the members that meet the programme's case acceptance test:
  the cash a member paid into its accounts over the calendar year against the cash its trade with its customers
  produced.
- **Forcing and forum:** the AML compliance committee's January meeting approves the quarter's investigations
  (`vote_or_meeting`, `committee_or_panel`); a credit union (`financial_institution`); the requester is the manager of
  Business Services (`portfolio_manager`, the holder of the segment's relationships). Redrawn at stage 2 from the Unit's
  lead (`compliance_or_audit`): task479 v7, registered nine minutes before this card in a parallel worktree, holds that
  family, so `ban.role` blocked. The first line is the honester owner and not merely the passing one: Canadian credit
  unions run periodic enhanced due diligence on higher-risk business members in the business line and escalate to the
  FIU, and the asks (branch after-hours cash, report timeliness on branch-keyed filings) are first-line measures.
  `guard.py check` WARNs answered: `repeat.deliverables` (docx, png and xlsx are what a first-line review sends a
  committee, a referral memo, a member workbook and one chart; task479's set is an emissions return) and
  `repeat.question_form` (the call gates each member, refer or not, so the form is `whether`; `which` sits over its
  corpus quota).
- **Call:** which cash-intensive business members Business Services refers to the Unit for enhanced investigation in
  the first quarter of 2027, with each one's 2026 cash paid in, the cash its trade produced and the difference.
- **Shape `other`:** a designation over the segment. Criteria arithmetic: the designated set (each referred member, 2),
  each referred member's three figures (6), the largest excess not referred (1), the workbook's cash paid in for every
  member (1), the chart with its parts (4), the files (3), each quarter's reports required, filed and late (12), each
  branch's after-hours cash through its deposit ATMs and in its night depository (18): 47. The workbook grades only
  what every estimator of produced cash prints alike (`## Judge pass 5 rulings`).
- **Strategy and mechanism:** `population_selection` (the exposure the cash is measured against: the counter trade a
  third party settles, not a peer group, a declaration or the account's own turnover); gap objective then population
  (the declared activity, the peer means and the turnover shares are correct records and are not what the test is
  scored on); decisive generator G14 (the trade's cash-to-card relation carried onto each member's own card trade),
  G3 beside it (the record of cash against the trading operation behind it); Gate G `decomposition_attribution` (each
  member's cash split into what its trade produced and the rest); calibration `none`; context `operations_log`.
- **Data-native sentence:** a member's cash comes only from its walk-in customers, whose other payments reach the
  account as its card acquirer's daily settlements under the acquirer's own narrative, while its declared expected
  activity, its peer band and its account's other credits are all things a front's owners set or supply, so the
  settled counter trade is the only measure of the member's business that the laundered money cannot move.
- **Abstraction sentence (the test of Part 6):** "one kind of inflow is judged against what the unit's own activity
  produces, and every benchmark taken from the unit's peers, its declarations or its other inflows moves with the
  anomaly, so only the activity a third party records in a separate channel, carried through the population's
  relation between that channel and the inflow, separates the anomaly from size." Held against every approved and
  shipped build, no reviewer would say it of one: task236 divides a count by an independent estimate of the same
  latent count (no relation between channels is estimated); task196 corrects a dependence between two capture
  channels; task199 reads a count against the effort that produced it; task310 (OPP) reads output a limit held back.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 35 builds, one line each on what bears on
  this cell): 103 a contact fanned out through authorisations; 104 a self-adapting scorer replayed; 119 waits a unit
  could have shortened; 182 each unit's lagged response to a shared driver; 196 two capture channels, the second made by
  the firm's own follow-up; 199 a count against the watchers' filing effort; 184 an indicator saturating with container
  size; 186 an own-history null under shared local cycles; 187 a capped curve averaged over a spread; 189 bounds from
  two laboratories' limits; 191 an extremum against a null extremum; 192 a classifier's transport; 193 sequence
  symmetry from first-receipt dates; 195 a paired interval; 197 a programme traverse; 204 an unsteady balance; 125 a
  first-visit cap; 180 detection in quiet hours; 181 crossings; 183 repeat failers; 185 a reading-dependent
  conversion. None benchmarks an inflow against a separately settled channel, and none in the banking cell.
- **People** (`guard.py names --geo canada --seed 188`): Kristine Kirby (the credit union's Chief Anti-Money
  Laundering Officer, who chairs the committee) and Jeffrey Melendez (the Unit's lead). Neither appears in the prompt.
- **Sources:** FINTRAC's large cash transaction reporting (CAD 10,000 or more in one transaction or within 24
  consecutive hours by or on behalf of one person or entity) and its money laundering indicators for cash-intensive
  businesses (cash takings inconsistent with the business's size and sales pattern; expected activity declared high at
  account opening); card acquiring practice (daily settlement of card sales net of the discount fee, one or two business
  days after the sale, under the acquirer's own narrative and merchant number); delivery platforms paying restaurants
  weekly, net of commission, for orders paid online. Every organisation, member, acquirer and platform in the pack is
  fictional.

## Default path

The pipeline a competent AML analyst builds from the question's words, the programme and the files' grain.

1. Read the programme's case acceptance section (7.3): the test is on the cash paid into the member's accounts in 2026,
   on the business date of each credit, against the cash its trade with its customers produced, an excess of CAD
   100,000 or more and at least twice the produced cash.
2. Total each segment member's 2026 cash paid in from the postings: the cash portion of counter deposits, coin
   deposits, ATM deposits and night deposits, across every account the register's accounts sheet maps to the member.
3. Take the cash its trade produced as what the member told the credit union its trade would produce, its CDD
   profile's anticipated monthly cash deposits times twelve: the field's standard measure of activity consistent with
   the customer's profile.
4. Cross-check against the peer route the monitoring scenarios use: the mean 2026 cash of the member's business type
   and declared turnover band, and the business type's usual cash share of the account's turnover.
5. Apply the test and file the members it refers.

**Ends on:** refer Kingsway Pho House and Bright Spark Car Wash, two honest members whose 2026 cash (CAD 237,252 and
174,160) is 3.5 and 3.6 times the expected activity they declared at their 2018 and 2019 reviews, and clear Seaview
Specialty Foods and Pacifica Donair & Pizza, whose cash sits at 0.93 of what they declared in 2025; the peer and
turnover-share cross-checks refer nobody.

**Golden:** refer Seaview Specialty Foods (CAD 477,000 paid in, about 125,000 produced, excess 350,000) and Pacifica
Donair & Pizza (299,000 paid in, about 75,000 produced, excess 225,000), each paying in about four times the cash its
counter trade produced, that trade read from its card acquirer's settlements through its own business type's
cash-to-card relation across the segment; the largest excess not referred is Sunrise Fresh Market's.

## Stump sentence

The solver refers Kingsway Pho House and Bright Spark Car Wash because it judges each member's 2026 cash against the
expected activity the member declared, or against its peers or the account's own turnover, and clears Seaview Specialty
Foods and Pacifica Donair & Pizza, whose declarations were set high in 2025 and whose network's business payments swell
their turnover, when only the walk-in trade their card acquirers settle shows that each paid in about four times the
cash its counter trade produced.

## Three rules

- **Task type:** banking-credit-financial-risk / fraud-aml-detection, which serves Anomaly Detection: separating
  laundered cash from the ordinary takings of a cash-intensive business is that task type's own work.
- **Domain test:** the deciding quantity is each business member's cash paid in beyond the cash its trade with its
  customers produced, the core quantity of cash-intensive business monitoring in anti-money-laundering work; with
  hospitals or megawatt-hours in place of takeaways and salons there are no tills, card terminals, acquirer
  settlements or placement of criminal cash, so the task stops making sense.
- **Swap:** "which hospitals should the inspectorate investigate for megawatt-hours beyond what their patient trade
  produces" has no tills, no card terminal settling the same counter's sales, no criminal cash to place and no
  declaration a front could inflate; the call does not survive the swap.
- **Layer 1:** the core banking system's postings with each processor's own narrative (two card acquirers with their
  own batch wording and merchant number formats, two delivery platforms paying weekly net of commission, business EFTs,
  mobile cheque deposits, owner and loan transfers); counter deposits that mix cash and cheques with the cash in its
  own field; UTC timestamps against Pacific business dates, ATM deposits after 18:00 posting to the next business date
  and night bags credited when counted, the next morning at three branches and later at Regional Cash Services; members
  holding more than one account, mapped through the register's accounts sheet; CDD profiles of different review
  vintages; a branch closed and another opened in June with an ATM moved under its own terminal number; an LCTR log
  mixing segment and other members' reports, Corrections, a re-sent Original and branch-keyed reports carrying the
  conductor's membership; a bag register (Regional Cash Services' item register) keeping the bags members withdrew
  worn out or reported lost beside the active ones, each with the day its status was set, a lost bag's replacement
  and the spares some members were issued; one bag carrying two accounts' deposit slips from one evening, listed once
  on the carrier's manifest and posted twice. Each comes from the system that makes it, none is placed to be caught,
  and every one mishandled leaves the call where it is (`checks.py` R2 rows).
- **Layer 2:** estimand_identification: the right counterfactual for a member's cash is the cash its own counter trade
  produces, measured through a channel the laundered money cannot reach, against the declared, peer and turnover
  benchmarks that all move with it.
- **Decisive step:** judging each member's cash against the cash its walk-in counter trade produces, that trade taken
  from the card acquirer settlements, the one record of the member's counter sales that a third party makes and that
  neither the laundered cash nor the network's payments can inflate, carried through its own business type's relation
  between cash and card across the segment.
- **Not semantics:** every field, code, narrative and definition read correctly (the cash portions, the channels, the
  settlements, the payouts, the declarations) still leaves the declared-activity, peer and turnover routes on Kingsway
  Pho House and Bright Spark Car Wash or on nobody, because those routes are computed correctly on correctly read
  data; no field says which benchmark the fronts' own money moves.
- **Not rule application:** no filed rule computes the cash a member's trade produced: the programme sets the test on
  it and leaves the estimate to the review, so executing every filed rule with the declared activity, the peer mean or
  the turnover share files the wrong set. The enumerated family (declared activity, peer mean, turnover share, non-cash
  credits, every settlement with platform payouts in, a joint fit on card and platform, the counter card trade under
  eight statistics and four groupings) names four different sets: the declared pair, nobody, Seaview alone and the
  golden pair. The standing family (the counter card trade under the eight statistics and four groupings) names one set
  in 12 of 12; under the eight statistics the produced cash spreads CAD 117,929 to 132,736 for Seaview and 69,982 to
  78,978 for Pacifica, every printed call figure inside one bin (`checks.py` F1 to F4, W1), and of the four groupings
  only one relation across every business type, which the record rejects (type carries 78 per cent of the variance,
  F7), moves a printed figure, Seaview's excess 51 dollars over its edge. What rules the rest out is quiet: no sentence; the domain fact
  that a delivery order is paid in the app and a business customer pays by EFT or cheque, and the data's own record
  that honest members' cash follows their card trade within each business type.
- **Analyst test:** a strong analyst who reads every field and the programme correctly takes the produced cash as the
  member's declared expected activity and refers Kingsway Pho House and Bright Spark Car Wash on their 2026 cash of CAD
  237,252 and 174,160, or as its type-and-band
  peers or its type's cash share of turnover and refers nobody, while Seaview Specialty Foods and Pacifica Donair &
  Pizza pass because their laundered cash and their network's business payments inflate exactly the measures those
  routes divide by (`checks.py` R3a on the clean truth).
- **Estimand:** filed in `compliance/hrcu_aml_atf_compliance_programme_v6-1.pdf` section 7.3 (case acceptance):
  population, the members of the cash-intensive business segment (section 3, the register's segment at 31 December
  2026); outcome, the cash paid into the member's accounts in the calendar year beyond the cash the member's trade with
  its customers produced in that year; window, calendar 2026 on the credit union's business date of each credit; unit,
  CAD per member; comparison, CAD 100,000 or more and at least twice the produced cash, presented in descending order
  of the excess.
- **No decoy:** nothing is planted to be caught: the declarations are the members' own review statements, the network
  payments are the fronts' ordinary layering, and no memo, draft, briefing or stakeholder figure argues for any member.
- **No certified replay:** no certified or published figure is reproduced to recover a method; the pack holds no
  control total of produced cash and no prior referral whose figures a method must match.
- **Lesson:** an anomaly's benchmark must be one it cannot move: a front's declarations, peers and turnover all rise
  with its laundered cash and its network's payments, so only the trade a third party settles in a separate channel,
  carried through the population's relation between that channel and cash, separates laundering from size; no build on
  file teaches it (the nearest, task236, divides by an independent estimate of the same latent count).

## Survivor anatomy

- **Actor:** the deciding property, how much cash a member's counter trade produces, has no column: the postings
  carry each credit's amount and narrative, the counter card trade is a sum of acquirer settlements recognised by their
  wording, and a business type's relation of cash to card exists only across the population.
- **Link:** the step reads each member's cash through its card acquirer's settlements, a comparison across payment
  channels that monitoring of cash never asks for, and keyed by nothing: the settlements carry the acquirer's own
  merchant number and wording, never a field saying card trade.
- **Reflex:** the field's own routes, the CDD profile's expected activity and the monitoring scenarios' peer group, sit
  at rungs 0 and 1 and refer Kingsway Pho House and Bright Spark Car Wash, or nobody.
- **Back-test:** the textbook route validates on the pack's own record: the members the declared-activity route
  refers on the year it refers on each half-year (`checks.py` K4), and the fronts sit inside their declarations, so a
  solver checking the route for stability finds it stable.
- **Second use:** every file the decisive step reads has its own reason to be in the pack: the postings are the spine of
  every figure and ask, the member register gives every route its business types and accounts, and nothing ships only
  for the card benchmark.
- **Shock:** the fronts are ordinary on every shipped statistic: Seaview twelfth of 48 grocers and Pacifica third of
  56 quick-service restaurants on cash paid in, both at 0.93 of their declarations, neither first in its type on cash,
  turnover, cash share, non-cash credits, card trade or deposit count, and the two never the segment's top two on any
  (`checks.py` K5).
- **Pins:** the WHAT is filed once, in the programme's case acceptance section in the credit union's own voice; no
  sentence names card trade, a channel, a ratio, a peer group or a declaration as the measure, so no filed sentence names
  what the stump rides on.

## Readability screen

Seven tests per rung: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene battery, 6 linear, 7 second use.
The reflex row is enumerated from the field's own vocabulary for expected cash (customer profile, peer group,
turnover share, cash intensity), not from the rungs beneath the decisive one.

| Rung | 1 filed | 2 schema | 3 reflex | 4 bench | 5 hygiene | 6 linear | 7 second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 declared expected activity (Kingsway Pho House, Bright Spark Car Wash) | section 4 records the anticipated cash deposits | a CDD column, one join | yes, actual against expected | none | no | one product | the profiles serve no other step | readable |
| 1 peer mean by business type and turnover band (nobody) | section 3 names the segment's types | two columns | yes, the scenario's peer group | none | no | a group mean | the register | readable |
| 2 business type's cash share of turnover (nobody) | nothing | credits are one sum | yes, cash intensity | none | no | a share | the postings | readable |
| 2b non-cash credits through the type's relation (nobody) | nothing | credits less cash | partly | none | no | one relation | the postings | readable |
| 3 every settlement, platform payouts in (Seaview alone) | nothing | two narratives per member | partly, trade read as all sales | none | no | one relation | the postings | readable |
| 4 (decisive) the counter card trade through the business type's cash-to-card relation | no clause names card trade, a channel, a ratio or a benchmark | no column marks a settlement as counter trade or holds the relation; two acquirers' wordings, net of their discount | no: the field's reflexes are rungs 0 and 1 | none shipped | the battery passes on every rung | no: a population relation estimated across the segment and carried to each member | the postings and register serve every route and every ask | silent |

**Reflex sweep, measured on the cut pack.** Declared activity refers the declared pair; the peer mean, the turnover
share and the non-cash relation refer nobody; every settlement with platform payouts in refers Seaview alone (Pacifica's
excess 181,412 at 1.54 times its produced cash, short of the twice arm); a joint fit on card and platform payouts per
business type refers Seaview alone. None prints the golden pair.

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "cash paid in" | the cash portion of counter, coin, ATM and night deposits | the deposit's whole credit, cheques in | same call | C1 asserted (`checks.py` SF1): the mobile cheque channel carries the large business cheques, so the counter's mixed deposits move no member across the test |
| SF2 | "in the calendar year" | the business date of each credit in 2026 | the UTC posting date | same call and figures | section 7.3, "counted on the credit union's business date of each credit"; C1 asserted |
| SF3 | "the member's accounts" | every account the register maps to the member | the first account alone | a different quantity | section 7.3's plural and section 6.2's "any of its accounts"; asserted as computed |
| SF4 | population | the register's segment at 31 December 2026, every member with a profile | members with a profile only; members active all year | same members | C1 asserted: every register member has a profile and is in the segment |
| SF5 | "by at least twice the cash that trade produced" | the excess at least twice the produced cash | cash at least twice the produced cash | same call | C1 asserted: outside the two referred, no member's excess reaches even its produced cash (the largest 0.76 of it) |
| SF6 | boundary inclusivity | "or more", "at least" | strict inequalities | same call | C1 asserted, nothing on either edge |
| SF7 | rounding path | each figure rounded once at the end | the excess from the rounded cash and produced | same figures | asserted (`checks.py` SF7) |
| SF8 | order of the slate | descending excess | descending relative excess | Pacifica first | section 7.3, "in descending order of the excess" |
| SF9 | "the member with the largest excess that does not" | the CAD excess among members not meeting the test | the largest relative excess (Sunny Lotus Restaurant) | another member | the excess is the CAD difference section 7.3 tests |
| SF10 | "produced in that year" | card settlements credited in 2026 | settlements on the sale date the batch narrative carries | same call and figures | C1 asserted (`checks.py` R2 and SF10) |
| SF11 | a member with no card trade | none in the segment | n/a | same call | asserted: every member has card settlements |
| SF12 | reports required | the section 6.2 window | one report per member and business date | other figures | section 6.2's window sentences |
| SF13 | the window's members and clock | per member across accounts, quarter on Pacific time | per account; quarter on UTC | same figures | C1 asserted |
| SF14 | "how many we filed for it" | reports on the segment's accounts | reports whose member field is a segment member | other figures | the report's account and amount are the segment account's cash for that business date; a branch-keyed report's member field holds the person who brought the cash, a membership not in the segment's register |
| SF15 | "how many late" | submitted more than 15 calendar days after the day, on Pacific time, the first cash the report covers was received | after the log's transaction date; after the UTC day of the receipt | other figures under each | section 6.2, "after the day, on Pacific time, on which the first cash it reports was received"; the log's transaction date is the business date the cash was credited (`checks.py` SF15, both readings) |
| SF16 | a filed report's quarter | the quarter of its transaction date | the quarter it went in | other figures | section 6.2, "a report to the quarter of the transaction date it reports" |
| SF17 | Corrections and re-sent Originals | one report per reference, on its first submission | every row a report (filed 20, 47, 48, 39; late 3, 8, 13, 10); a reference on its last submission (late 2, 8, 12, 10) | other figures under each | section 6.2, "each report has its own reference. A correction carries the reference of the report it amends; it is not a further report, and the amended report keeps the submission date of the original" (`checks.py` SF17, all three readings) |
| SF18 | "its deposit ATMs" | the terminals the directory lists under the branch, at the site each stood at on the day of the deposit | one row per terminal | other figures on Langley City and Willowbrook | the directory lists a terminal once per installation with its dates |
| SF19 | "in its night depository" | the depository the bag was dropped in: the counting branch, or the depository the armoured car collected it from that morning (the manifest's one listing of the bag on the pickup date equal to the posting's business date) | the branch that issued the bag; the member's home branch | other figures on every branch | the asking sentence's own words; the bag register records issue, not deposit |
| SF20 | "2026" for the branch cash | the business date | the day of deposit | other figures: the evening ATM deposits of 31 December credit on 4 January 2027 | the asking sentence, "each branch's segment cash credited on 2026 business dates", and section 5, "for monitoring and the January review, cash is counted on the credit union's business date of each credit" |
| SF21 | which listing places a cash-centre bag | the bag's one row on the manifest for that pickup date | the first or the last of two listings | same figures | C1 asserted (`checks.py` SF21): a bag is out from the evening it is dropped until it is counted, so the carrier lists it once on each pickup date (two deposits made one evening at one depository travel in one bag), every 2026 posting at transit 19004 joins exactly one listing, and the column equals the clean truth's depository to the dollar |
| SF22 | "every member's cash paid in" in the workbook | the cash paid in column for every member; produced cash and excess graded for the referred members only | every member's produced cash and excess | not graded: the within-type mean and totals move 100 and 115 of the other members' produced cash a bin and Sunrise Fresh Market's excess spans 425,000 to 500,000 over the eight statistics | the asking sentence asks the workbook for every member's cash paid in, a sum of shipped rows; produced cash and excess are asked for the members that qualify (`checks.py` SF22, W1, W2) |
| SF23 | the window for the first quarter of 2026, before version 6.1 took effect on 1 April | the section 6.2 window | the reporting module's one report per account and business date | another Q1 required count | section 1, "Section 6.2 restates, without change, the large cash transaction window and reporting rules in force since version 6.0 (April 2025)" (`checks.py` SF23) |
| SF24 | the terminal's site for a deposit credited on a 2026 business date | the site on the day of the deposit | the site on the business date the deposit credits | same figures | C1 asserted (`checks.py` SF24): the moved terminal took its last Langley City deposits on 26 June, credited by 29 June, was taken out on 30 June and went back into service at Willowbrook Crossing on 6 July, so no deposit's two dates fall at two sites |
| SF25 | where an installation ends: the 18 deposits (CAD 19,300) Langley City's lobby ATM took on the evening of 26 June, the branch's last day | inside the Langley City installation, whose removal the directory dates 30 June, the day the ATM and the night depository were taken out after their last deposits were credited on 29 June | the removal day not in force; the deposit's UTC day (27 June for all 18); the business date it credits (29 June for 15 of them) | same figures | C1 asserted (`checks.py` SF25, `verify.py`): the Pacific day, the UTC day and the business date, each with the removal day in force or not, place every 2026 ATM deposit in one installation and print Langley City's 1,278,000 and every other branch's figure; the same record dated on the branch's last day prints 1,257,000, 1,259,000, 1,263,000 or 1,278,000, and every manifest pickup from ND-9175 (the last on 29 June) falls before its removal |

## Ladder

| Rung | Analysis | Referred | Seaview excess | Pacifica excess | Dies to |
|---|---|---|---|---|---|
| 0 | declared expected activity times twelve | Kingsway Pho House, Bright Spark Car Wash | under its declaration | under its declaration | the declarations are the members' own statements, a front's set to cover its money |
| 1 | mean of the business type and declared turnover band | nobody | 14,896 | 20,019 | the band is the front's own declaration and the mean moves with large members |
| 2 | the type's median cash share of the account's credits | nobody | 81,126 | 25,910 | the network's business payments swell the fronts' credits |
| 2b | non-cash credits through the type's relation | nobody | not referred | not referred | the same payments are non-cash credits |
| 3 | card settlements and platform payouts through the type's relation | Seaview Specialty Foods | 359,801 | 181,412 (1.54 times) | a delivery order is paid in the app and produces no cash |
| golden | counter card trade through the type's cash-to-card relation | Seaview Specialty Foods, Pacifica Donair & Pizza | 355,022 (2.91 times) | 227,583 (3.17 times) | nothing |

**Position and dominance.** The golden pair is named by no rung below it, and rung 3 names half of it, so no
half-applied correction lands on it. Under the golden the referred sit at 2.91 and 3.17 times their produced cash and
no other member above 0.9 (`checks.py` F5), so the relative arm separates by more than three to one; the absolute arm
is passed at more than twice its CAD 100,000. Sunrise Fresh Market, the largest excess not referred (about CAD 475,000
at 0.75 times), is the nearest member on the absolute arm and the farthest on the relative one.

**Bins.** Every printed call figure sits inside one bin across the standing family: Seaview's produced cash 117,929
to 132,736 (125,000) and excess 344,211 to 359,018 (350,000), Pacifica's produced 69,982 to 78,978 (75,000) and excess
220,367 to 229,363 (225,000); cash paid in is a sum of shipped rows.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's segment at 31 December 2026 (section 3, 7.2); C1, every member with a profile (SF4) |
| 2 | Unit of account | the member across its accounts (SF3), filed in section 7.3 |
| 3 | Attribution window | calendar 2026 on the business date (sections 5 and 7.3); C1 against the UTC date (SF2) and the sale date (SF10); the branch cash in the asking sentence's own words, "credited on 2026 business dates" (SF20), the terminal's site converging on either date (SF24) and on the UTC day (SF25) |
| 4 | As-of dating | the register at 31 December 2026, the postings through the pull on 8 January 2027; no member joins or leaves in the year |
| 5 | Version basis | the CDD extract is one vintage and no rung of the golden reads it; the LCTR log's Corrections amend their Original and keep its submission date (section 6.2, SF17); programme v6.1 took effect on 1 April and section 1 files that section 6.2 restates the rules in force since version 6.0, so the window governs the whole year (SF23) |
| 6 | Denominator | not a rate: the test compares two CAD amounts |
| 7 | Weighting | the business type's relation is a median of members, C3: totals, means, trims, fits and the within-type groupings print the same call figures (F1 to F4, W1); one relation across every type moves Seaview's excess 51 dollars over its edge and the record rejects it (F7); the other members' figures are not graded (SF22) |
| 8 | Window length | one calendar year, filed |
| 9 | Boundary inclusivity | C1, nothing on either edge (SF6); an installation's end converges, the directory dating a fixture's removal on the day it was taken out, after its last credit (SF25) |
| 10 | Rounding path | once at the end, filed in the asking sentence; C1 for the excess from rounded parts (SF7) |
| 11 | Tie-break | none: two members, excesses 355,022 and 227,583 |
| 12 | Maturity and censoring | the year is closed; settlements of the last days' card sales credited in 2027 move no figure (SF10) |
| 13 | Order of operations | relation estimated per type, then carried to each member; C3 across the family |
| 14 | Row order | C1: every computation is a sum or a median over rows |
| 15 | Duplicate resolution | the postings carry unique ids; each report has its own reference, so the LCTR log's re-sent Original is one report and a Correction no further report (section 6.2, SF17); the pickup manifest lists each bag once per pickup date (SF21) |
| 16 | Identity normalisation | accounts map to members through the register; the LCTR log's account, not its member field (SF14) |
| 17 | Netting against gross | cash paid in is gross of withdrawals, filed ("paid into"); settlements are net of the discount, C1 grossed up (R2) |
| 18 | Dimensional units | CAD throughout; no currency or scale shift |
| 19 | Code and status semantics | cash codes and channels read from the postings; C1 on the cheque reading (SF1) |
| 20 | Integerisation | figures rounded once; ATM cash in five-dollar multiples and night cash in whole dollars, so every branch sum is an exact integer and its rounding cannot drift (Seaview and Pacifica's cash sit 447 and 155 dollars from their edges) |
| 21 | Clause scope | section 7.3 governs the call, section 6.2 the report counts; neither reaches the other |
| 22 | Forward window contents | the call commits the first quarter's investigations from the closed year; nothing forecast |

## Literal reader

A reader executing section 7.3 word for word must estimate, for every member of the segment, the cash its trade with
its customers produced in 2026, because no file states it; every term in the fork table returns the golden pair or is
refused by a quoted sentence. The method is not filed and is forced by the record: a delivery order paid in the app and
a business customer's EFT or cheque produce no cash, so the trade that produces cash is the walk-in counter trade, and
the one record of that trade a third party makes is the acquirer's settlement; carried through each business type's
relation, the standing family of statistics and groupings returns the same pair and the same printed figures (F1 to
F4). The asks run on section 6.2 and the asking sentence: each of their conventions is filed or converges (SF12 to
SF25). The workbook is asked for every member's cash paid in, a sum of shipped rows, and its produced cash and excess
are graded only where the question asks for them, for the members that qualify, which every estimator the record
licenses prints alike (SF22, W1).

## Oracles

- **The CDD profiles.** They confirm the default route rather than refuting it: the fronts sit inside their 2025
  declarations and the two stale declarations sit far below their members' cash.
- **The LCTR log.** It reports cash per account and business date for the asks; no golden figure of the call reads it,
  and it holds no figure that equals any member's annual cash, produced cash or excess.
- **`compliance/str_submissions_2025_2026.csv` and `compliance/fiu_case_register_2026.xlsx`** (declared distractors):
  the Unit's own reports and cases, none on the fronts, the near miss or the stale-declaration members, so they point
  at nothing.
- **`payments/international_wires_2026.csv`** (declared distractor): honest grocers' and restaurants' supplier and
  family wires; the fronts send none.
- No corpus, no back-test of the golden, no prior referral, no worked example. Nothing in the pack states or implies
  any produced cash figure.

## Ask sheet

The call's declared population is the segment's 2026 cash rows, card settlement rows and the register. Both asks read
ask-only files for their devices (the LCTR log, the branch directory's ATM history, the armoured car's pickup
manifests, the bag register), and no device row sits in the call's population: the postings are not altered for any
ask (A7).

- **Ask A, each 2026 quarter's large cash transaction reports the segment's cash required, filed and filed late (12
  figures).** H18 home: the Committee's quarterly reporting item in its terms of reference. Required follows section
  6.2's window, which the cracker executes. Filed carries a D7 device: a report keyed at a branch puts the conductor's
  own membership in the member field, so the segment's reports are found by their account, not their member field.
  Late carries a D8 device: section 6.2 runs the 15 days from the day the first cash was received, while the log's
  transaction date is the business date an evening ATM deposit was credited.
- **Ask B, each branch's segment cash credited on 2026 business dates through its deposit ATMs and in its night
  depository (18 figures).** H18
  home: the after-hours cash the branch network services, a component of the segment's cash. ATMs carry a D7 device
  (Langley City's lobby terminal reinstalled at Willowbrook Crossing under the same number, listed once per
  installation). Night carries a D6 device: bags counted at Regional Cash Services post at its transit, and only the
  armoured car's pickup manifest (bag and date, a bag listed once on each pickup date) says which depository each came
  from; the bag register says where it was issued, and keeps the bags members withdrew or lost.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | executes section 6.2's window, counts each reference once, finds the segment's reports by the log's member field and runs the 15 days from the log's transaction date | misses |
| B | places each ATM deposit at the terminal's site on the day and each cash-centre bag at the branch the bag register issued it from | misses |

Measured by: `generator/ceiling.py` on the cut pack.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive keeps | Cracker |
|---|---|---|---|---|---|
| A reports by quarter | 12 | 4 | 4 | 1 | misses |
| B after-hours branch cash | 18 | 9 | 7 | 7 | misses |

Over the 30 figures the cracker keeps 13 (43.3 per cent of ask weight), the mirror 11 (36.7 per cent), the naive
handling 8; reading the conductor key alone keeps 17, the receipt day alone 14, the manifest alone 22, every device 30.

Re-run on the pass 5 and pass 6 cuts: every keep is unchanged (pass 6 moved two removal dates in the directory,
which every handling reads alike, SF25). The three sentences pass 5 filed (a correction is no further report
and keeps the original's submission date, section 6.2 governs the whole of 2026, the branch cash is credited on 2026
business dates) are conventions both sheets already executed, so neither sheet moves. The workbook sits outside the 30
ask figures: it is now asked for every member's cash paid in (one criterion, a sum of shipped rows), and its produced
cash and excess are graded only for the referred pair, inside the call's criteria, so the rubric holds 47 criteria
and the ask weight is unchanged.

Pair ceiling: 50.5.
Mirror leakage: 36.7 per cent of ask weight.

## Leak sweep rulings

`leak.py --asof 2027-01-15` on the final cut (target.zip sha256 0611e6b3, after the pass 6 repair), verdict REVIEW, no
LEAK; sweeps 1, 2, 5, 7, 8 and 11 clean, and sweeps 3, 6, 9 and 12 the same lines as on eaf930e6. The pass 6 rulings
joined the note paragraphs sweep 4 draws its terms from, so its 25 terms now take in settlements, benchmark,
laundered, expected and report; no shipped document carries settlements, benchmark, laundered, expected, acquirer or
card.
- Sweep 3: the 53 hits on five-digit numbers are the branch transits (10342 to 11204), which every branch file carries
  as its key; "7.3" is the programme's own section number, in its revision note and in the terms of reference; the
  programme shares the call's words because the call is its own section 7.3 referral, and it names no member.
- Sweep 4: the programme and the terms of reference share ordinary words with the stump paragraph (counter, turnover,
  relation in "relationship", credit, section, activity, records, register in "member register", refers in "Business
  Services refers", report in "large cash transaction report", carries in "a correction carries the reference");
  neither names card trade, a channel, a ratio or a benchmark. The prompt's ask sentence carries "reports" (the large
  cash transaction reports Ask A counts) and "credited" (the business-date basis Ask B files), the asks' own words,
  and names nothing the call turns on.
- Sweep 6: the directory and the register name branches and members beside their own numbers (addresses, dates,
  member numbers); neither ranks anything on the referral question.
- Sweep 9: the CDD extract's `next_review_due` dates lie after the as-of date by their nature.
- Sweep 12: the five words (channel, opened, closed, credit, Regional Cash Services) are the programme's own words
  about its channels and its counting centre, not a gloss on any column.

## Leak reader rulings

The stage 4 reader on zip 0fcfaed0 (its answers in `leak_check_report.md`, `## Solver's-eye read`), each ruled
harmless in one line:
- Question 1, none: the closest it named is section 7.3, which files the test and not the estimate.
- Question 2, none: no file ranks or scores the members on the referral question.
- Question 3, none: no file exists only to help the analyst.
- Question 4, none: no figure or name reads as the answer.
- Question 5: sections 7.3 and 5 fix the cash paid in by business date and section 6.2 governs the ask counts, which
  executes to the golden's cash paid in; nothing files how produced cash is computed, the method open and forced by
  the data, as designed.
- Question 6: an analytical choice, produced cash estimated from the settlement streams that carry no cash, the step
  `## Three rules` names, so rule 3 holds from outside.
- The answer-figure sweep's lines: the transit codes, bag numbers and member numbers are identifiers every file keys
  on, not answers.
- The reader's two realism findings (the terms of reference on the writing library's stock template, every bag in
  the register Active) were fixed in the generator, not ruled harmless.

Re-read 3 on the pass 5 cut (target.zip sha256 eaf930e6; its answers in `leak_check_report.md`,
`## Solver's-eye read (re-read 3, 2026-11-03)`), no leak, each ruled in one line:
- Question 1: it quotes programme section 7.3, the filed case acceptance test, a WHAT (population, outcome, window,
  unit, comparison) and not the decisive step, which no clause names.
- Questions 2 to 4, none: no file ranks the members, none exists only to help the analyst, no figure or name reads as
  the answer.
- Question 6, analytical: the step `## Three rules` names, so rule 3 holds from outside on the final documents.
- The terms of reference's modified date, 2026-11-23, falls before the January 2027 extracts and inside the setting's
  timeline (a re-save of a document the committee approved in November 2025): harmless.

## Judge pass 5 rulings

The pass 5 FIX_NOW (`determinism_check_report_pass5.md`) closed in one generator pass, one line per ruling:
- Workbook: closed on the grading side, no estimator filed. The prompt asks the workbook for every member's cash paid
  in ("list in member_cash_review_2026.xlsx every member's cash paid in"); its graded cells are that column, the test
  column and the referred pair's three figures, which hold under each of 12 within-type estimators (`checks.py` W1,
  W2); the other members' produced cash and excess stay on the sheet as the review's working and are not asked or
  graded (SF22); Sunrise Fresh Market is graded by name alone, because its excess prints 425,000, 475,000 or 500,000
  across the eight statistics, so the bin the judge offered as stable is not.
- Branch cash: the asking sentence carries the date basis as a WHAT, "each branch's segment cash credited on 2026
  business dates" (SF20), and the terminal's site agrees on either date (SF24).
- First quarter: section 1 says "Section 6.2 restates, without change, the large cash transaction window and reporting
  rules in force since version 6.0 (April 2025)", the programme's own revision note, so the window governs all of 2026
  with no method filed (SF23).
- Corrections: no shipped sentence carried it and the figures do not hold either way (every row a report files 20,
  47, 48 and 39 with 3, 8, 13 and 10 late; a reference on its last submission files 2, 8, 12 and 10 late), so section
  6.2 files the WHAT: each report has its own reference, and a correction is no further report and keeps the
  original's submission date (SF17).
- Terms of reference: rebuilt with the Office theme part, the colour map in its settings, headings on the theme's
  fonts, and every zip member dated 2026-11-23 18:41:00, the save its property part records, the pack's own convention
  (each Office file's member times equal its core clock) (`checks.py` Z13, `verify.py`).
- Measured, frozen and left for the re-judge: one relation across every business type moves Seaview's excess to
  375,000 (362,551, 51 dollars over its edge), a grouping the record rejects (type carries 78 per cent of the variance
  of log cash per card dollar outside the referred, F7); a business type by home branch split names Crystal Farm
  Market as the largest excess not referred, while home branch carries 2.8 per cent of the within-type variance
  against 1.8 by chance over its eight branches (F8). No frozen figure moved.
- Scope: `freeze.py check task188 --mode determinism` passes against the snapshot taken before this pass (the call,
  the stump, the ladder, the default path, the call sentence, every Deliverable Answers number and every existing
  figures.json value unchanged; six workbook keys added); `--mode rubric` passes with no ask file moved.

## Judge pass 6 rulings

The re-judge on target.zip sha256 eaf930e6 (`determinism_check_report_pass6.md`): DETERMINISTIC, APPROVE; Gate H
domain pass, layers pass, decisive step analytical; Gate G no mismatch; Gate F good. One line per finding:
- Residual fork, Langley City's ATMs (1,278,000 with 26 June, the removal day, in force; 1,259,000 without it or on the
  UTC day): the golden carries 1,278,000, each deposit at the installation standing on its Pacific day. Closed in the
  organisation's own record and not in a sentence: the facilities directory dates the lobby ATM's removal on the day it
  was taken out, 30 June, after its last deposits were credited on 29 June, so all six readings print 1,278,000
  (SF25); on the old record they printed 1,257,000, 1,259,000, 1,263,000 and 1,278,000.
- The night depository carried the same record (removed 26 June with three pickups on 29 June, Langley City's night
  440,000 or 439,000 to a reader dropping them) and takes the same date, which the manifest's pickups now precede.
- Scope: two cells of the directory moved; every other shipped byte, the three goldens, metadata.json and figures.json
  are byte-identical to the approved cut; `freeze.py check task188 --mode determinism` passes against a snapshot of
  that cut, figures_check finds all 80 figures, the ask ceiling is unchanged (cracker 13 and mirror 11 of 30, pair
  ceiling 50.5); no method or sentence filed.
- The APPROVE stands without a re-judge: the repair moves no graded figure and alters no clause a gate turned on (the
  directory is an ask file the call never reads, and the closure is the one the judge asked for).
- Stump power note (a cash-to-card benchmark is a recognised AML technique), weighed against the ladder: the field's
  reflexes are the declared activity and the peer group (rungs 0 and 1), and a solver who builds expected cash from the
  settlements most readily takes every settlement a third party records, rung 3, which clears Pacifica (1.54 times its
  produced cash); only the counter trade names the pair. No change.
- The terms of reference's creation date, 2025-10-02, six weeks before the committee approved it on 14 November 2025:
  a draft precedes its approval; harmless.

## Pre-ship check

1. Domain: AML monitoring of cash-intensive businesses, each member's cash judged against the cash its counter trade
   produced; with another field's nouns there is no till, card terminal, acquirer settlement or criminal cash to place.
2. Real work, nothing planted: every Layer 1 item is what the credit union's systems write; each mishandled leaves the
   call where it is (`checks.py` R2 rows), and the asks' devices sit only in ask files (A7).
3. The step that flips the call is analytical: which record of the member's trade the laundered cash cannot move,
   carried through each business type's relation; no clause names it (the programme files the test, not the estimate).
4. Analyst test: the declared route, every rule applied, refers Kingsway Pho House and Bright Spark Car Wash on the clean
   truth (R3a); the decisive step alone refers the golden (R3b); each lower correction stays wrong.
5. The programme files the estimand (population, outcome, window on the business date, unit, comparison); the standing
   family prints the same pair in 12 of 12 and the same call figures under the eight statistics and the three
   within-type groupings (F1 to F4, W1; one relation across every type, which the record rejects, moves Seaview's
   excess, F7); the workbook grades only those cells (SF22); every convention row is asserted (SF1 to SF25).
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest driver 0.06 (task27, task66, task120 v3); `guard.py heart` WARN only
   (repeat.question_form, answered in `## Draw`).
8. Asks: 30 figures on files the call never reads for their devices; the cracker keeps 13 and the mirror 11 (pair
   ceiling 50.5, `ceiling.py`), unchanged by the stage 4 repairs of passes 4, 5 and 6.
9. The 10/10 rules re-read against the built pack (target.zip sha256 0611e6b3): the decisive step is still analytical
   (R3a and R3b on the clean truth; the reader's question 6 and the judge's Gate H both analytical, no split); the mess
   is still Layer 1 only (every R2 row leaves the call where it is, and pass 6 moved two facilities dates in an ask
   file the call never reads).
10. Every gate re-run on the final cut: checks.py 133 of 133, verify.py 80 of 80, two consecutive builds
   byte-identical, figures_check 80 figures with 0 absent, `freeze.py` determinism PASS against the approved cut,
   precut 61 checks with 0 FAIL and 0 WARN, voice-check PASS, leak.py REVIEW with no LEAK (ruled), `guard.py heart`
   WARN with no BLOCK, `guard.py surface` exit 0 with 0 pairs promoted.

## Architecture 1 record

Architecture 1 (drawn 2026-10-13, shipped 2026-10-13, at the portal and pending): Rindal County Vector Control
District's one aerial adulticide zone for Thursday 20 August 2026, judged by the estimated West Nile virus-infected
Culex females per CO2 trap-night in week 32; golden Westbrook at 2.3 by maximum likelihood on the CO2-trap pools
against the minimum infection rate's Riverside South. Judge: DETERMINISTIC, APPROVE (pass 3,
`determinism_check_report_pass3.md`, kept as evidence). Spent on measurement on 2026-10-21 and confirmed 2026-11-01:
the decisive estimator family names one zone of 12 licensed constructions, so the step is a reflex (the full
re-screen is in the git history of this note at commit 0c21d67 and in the card's lineage).

## Tried and rejected

- Seed AD11's own world (route-origin paging at a cloud platform, RPKI invalid against not-found): no client domain's
  Anomaly Detection task type does routing analysis, and General Statistics' multiple testing would make network
  operations a backdrop; rejected at the draw on the domain rule.
- Political science conflict event data (attacks on civilians estimated from the overlap of the commission's monitors
  and the media, multiple systems estimation): capture-recapture reads the same in epidemiology with two surveillance
  lists, so the swap test survives; rejected at the draw.
- Pharmacovigilance signal triage (co-reporting and masking in disproportionality): the comparison has to be filed for
  determinism and filing it names the decisive step; rejected at the draw.
- Legionnaires' source attribution (plume touchdown and where cases were exposed): root cause, not anomaly detection,
  and practice disinfects every tower in the area at once; rejected at the draw.
- Influenza positivity standardised by days from onset to swab: a measurement-condition normalisation, the lane's third
  after task180 (noise) and task187 (turbulence); rejected at the draw.
- A resident-weighted index (traps sited on the marsh rather than among residents): an estimand that names residents
  makes the solver ask where they live (readability test 1); rejected as the decisive step at the draw.
- Westbrook with eleven CO2 sites (22 trap-nights a week): the likelihood estimate's own bias put the likelihood,
  bias-corrected and Jeffreys-penalised figures up to 2.4 per cent apart, straddling a one-decimal bin in most draws;
  four sites added in the zone's untrapped sections (30 trap-nights) and the draw chosen with every variant inside one
  bin, asserted.
- A second load that re-entered every 1 to 14 June night (432 records, keyed by the pickup morning): half of them
  landed on a night the site had already run, with that night's own status and catch, so the ask had three defensible
  readings (keep the first entry, keep the second, keep both) and the leak reader found the fork. The load now brings
  back the June Tuesday nights only (206 records), every one on a Wednesday the protocol schedules for no zone but
  Maple Ridge's enhanced fortnight.
- Resuming architecture 1 after the wave 8 Gate F failure by moving the protocol's filed definitions (the plan in `pipeline.json`'s resume line): refused on measurement before any design work. The decisive step's estimator family returns 1 distinct designated zone of 12 licensed constructions on the shipped draw and 1.15 over 20 redraws, so the step is a reflex whatever the protocol says and rewording 3.1, 3.2, 3.6 and 4.1 cannot put content into it; the same family spreads the printed call figure 3.5 printed units, so the clauses were load-bearing for Gate C and not for Gate F (`generator/family_screen.py`, `## Gate F re-screen`).
- Re-siting the decisive step onto which pools stand for the CO2-caught females, or onto which trap-nights count: each settles a part of the estimand (the population, the denominator and unit), which `determinism-check` section 1 requires filed, so filing it is rule application and leaving it unfiled forks the main call; dead on the WHAT screen with no hardening available.
- Keeping the unequal-pool-size likelihood as the decisive construction on any redraw of this world: the lever and the ceiling are one quantity. Over 20 redraws the family splits on the designation in 3, and in those 3 the separation is 0.11 and 0.13 of the family's own spread; in the other 17 the family is unanimous. No setting makes the estimator choice both matter and be determinate, so the architecture is spent rather than mistuned.
- **(2026-10-25, measured) A blind reader landed the call and took 74.0 per cent of the ask figures.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **Westbrook on Thursday 20 August 2026 at 2.328 infected Culex females per CO2 trap-night**, with South Prairie at 1.811 as runner-up and a flip at 18.29 per 1,000, and hit **16 of 18 call figures and 71 of 96 ask figures**. It took the decisive step by naming the maximum-likelihood pooled-sample estimate over the minimum infection rate in one line, because pool size differs between the two laboratories, and it enumerated the rungs it had refused: MIR picks South Prairie, including gravid traps picks Old Town at 5.6, counting failed trap-nights changes nothing. It also parsed all 1,155 pools out of the county laboratory PDF because week 32 was not yet keyed into the database, and re-derived every case's zone from its residence section against the 2026 sections, finding the case log's own zone column disagrees on 8. Readability test 3: the pooled-sample MLE is the standard estimator in arbovirus surveillance, so refusing MIR is the reflex and not the insight.
- **(2026-11-01) Architecture 1 marked spent and a re-root to architecture 2 opened at stage 1; no candidate cleared the screens on paper, so nothing was carded.** Each was screened against `guard.py mechanisms --objective anomaly-detection`, `guard.py slots` on mechanism and setting nouns, and the neighbouring slots' notes:
  - Crime incidence hotspots (a force's burglary alert triage, each beat's excess read against its prolific offenders' periods at liberty, linked across the prison release list and the court remand list with no key): task182's architecture 8 screen already closed it (the custody nights are a clean subset, so a filter and a divide estimates the same quantity, and the swap reads the same with super-spreaders), and its section 8 closes the cell's other fifteen candidates; the forward form ("which beat records most over the squad's four weeks") is Forecasting, not this number's objective.
  - Pharmacovigilance, a self-controlled case series biased by event-dependent exposure: task180's landing record (the plain SCCS was enough); masking in disproportionality: task193's judge SEND_BACK and this slot's own earlier line.
  - Card fraud common point of purchase with the exposure window ending at the fraudster's first test transaction: task181's architecture 1 died on the co-visit subset check, and recognising card testing is a payments analyst's reflex (readability test 3).
  - Electricity theft by feeder energy balance with a stale connectivity model mirroring one feeder's excess as its neighbour's deficit: no client task type carries non-technical loss detection as Anomaly Detection (grid-reliability-outage-analysis is outages); the outage form normalises by faults per 100 km, the field's own metric, which no customer transfer moves.
  - River load against concentration below a discharge (dilution at low flow): load is the field's first move, a reflex.
  - Rail SPAD risk per approach at danger from the train describer and aspect logs: once the WHAT is filed per approach at danger the time-overlap join is the literal construction (rule application); left unfiled the denominator is the WHAT screen.
  - A GWAS locus inflated by cryptic relatedness: kinship QC is the field's standard step; a surgeon outlier attributed through the theatre log: a join on a shipped key.
  What is left for the next draw: a quantity forced by arithmetic from a file at another grain whose correction touches every record (task182 section 9's finding, which this pass reproduced on four more grounds), in an Anomaly Detection cell other than disease surveillance (banned against task232) and crime hotspots (enumerated closed).
- **(2026-11-01, second pass) The four Anomaly Detection cells left open by the first pass, four or more candidates each, every one drawn from what that cell's own systems do to the records and screened on paper (default path, swap, survivor anatomy, bin test); none clears, so nothing is carded.**
  - provider-quality-risk-adjustment. (1) Comorbidity coding depth, each hospital coding its own case mix, corrected by a look-back through the patient's admissions elsewhere: default path, the index-coded SMR, ends on the under-coding hospital; swap holds (coding, Charlson, 30-day deaths); dies on `Reflex:` and `Actor:`, the look-back is the field's own comorbidity practice and a self-join on the person key, task271 architecture 1 landed by both stage 4 readers and task273's architecture 4 screen. (2) Thirty-day deaths found only through the death register link: `Actor:` holds, but it is task468's linker-error driver. (3) Deaths credited to the hospital of first admission across transfers: the superspell is the published indicator's own construction, a reflex. (4) Expected deaths from last year's national model while mortality falls: the step rescales the comparison, which the WHAT screen makes rule application once filed and a fork when not; bin test fails, the rescaled SMRs move 0.04 to 0.06 against a 0.1 bin. (5) Observer-sampled compliance: task269's driver.
  - payment-claims-health-plan-analytics. (1) Void-and-replace adjustments inflating gross paid: the replacement carries the original claim number, a shipped key (`Link:`). (2) A member's other coverage ending, so the plan turns primary and paid rises: allowed amount, the field's first view, is untouched by primacy (a reflex). (3) A practice absorbing a retiring colleague's panel, new-patient visits billing higher: new against established is in the procedure code (`Actor:`, a column). (4) Time-based office visit levels against the appointment system's check-in and check-out times: the code's time threshold is a published rule, rule application. (5) Drug units against weight-based dosing: the plan holds no weights (Gate B, the input absent). (6) The lesser-of allowance: task198's driver.
  - exploratory-data-analysis-distribution-assessment. (1) Release results retested into compliance, a deficit just past the specification limit: the decisive evidence is the chromatography audit trail's unreported injections, a planted behaviour (rule 3), and without it the true batch distribution has to be deconvolved, an open family (Gate C). (2) Digit preference after an instrument change: task185's device conversion. (3) Results above the range reported as greater-than: task188-era censoring by instrument limit, spent. (4) Snapshots of work in progress: task182's length bias. (5) A mixture of two production routes: the route is on the batch record (`Actor:`, a column).
  - safety-incident-error-analysis. (1) Pressure ulcers first recorded on the ward a patient was transferred to: the national 72-hour attribution rule makes it rule application, and without it the stage-to-onset time is a free parameter (bin test fails). (2) Medication errors at night with no pharmacist to intercept them: rebuilding the unintercepted errors from the day's intercepts per order, raised to night orders, is task275's approved driver. (3) Incidents per dose from the administration record: a denominator, the WHAT screen. (4) Several staff reporting one event: task103's fan-out. (5) Severity regraded after review: task194's vintages. (6) Blood units travelling with transferred patients, unaccounted at the issuing site: the donation number is a universal key (`Link:`). (7) Falls per midnight-census bed-day on a ward turned short-stay: the answer flips on the denominator's definition, data semantics.
  The cell occupancy behind this: every Anomaly Detection task type in the taxonomy now has its native recording processes either spent on a card or slot note, closed by task182 section 8, or barred by the three rules. The next draw for this number needs an author's ruling (a cell outside the four named, such as environmental-monitoring-exceedance or conflict-protest-event-data-analysis, or the objective's quota reconsidered).
- **(2026-11-01, third pass) The last two Anomaly Detection cells, each candidate drawn from what the organisation's monitoring or event-coding systems do to the records; none clears, so nothing is carded.**
  - environmental-monitoring-exceedance. (1) A trade discharger's daily mass load from 24-hour time-proportional composites, where concentration and flow move together within the day and an online analyser's hourly profile rebuilds the flow-weighted load (default path, composite times daily flow, ends on the night-dumping discharger; `Actor:` and `Link:` hold, a time join of two process-control logs no clause invites, and the regulator's audit composites agree on the wrong reading): the strongest candidate of the pass, and already measured dead on record, task190 architecture 9 candidate P3 (the per-day flow-weighted mean rebuilt from the autosampler's aliquot log, dead on the floor's other horn), task204 (flow-weighted and diurnally weighted loads killed on the swap test, each reading the same in any field's nouns) and task198 (load estimation as a ratio of totals against a mean of ratios, task200's estimand death). A recorded measured death outranks a fresh prototype, so no prototype was run. (2) Storm-triggered autosampling, events sampled only once flow passes a trigger: the trigger setting sits in the sampler configuration (`Actor:`, a column), and the selection it makes is task180's detection threshold. (3) Passive samplers whose two- to four-week exposure periods straddle the compliance year: apportioning them is the periods-complete filter and divide task198 closed, and the bin test fails on the annual mean's first decimal. (4) A fenceline monitor's exceedances read by wind sector against a regional background: the nuisance estimated where the signal vanishes, closed by task201. (5) An analyser dropping out on its heaviest days: task245's informative outage. (6) Gaps filled by decay toward normal: task247.
  - conflict-protest-event-data-analysis. (1) Fatalities coded at the lowest credible estimate: a filed coding rule, rule application. (2) Events of unknown place coded to the province capital: the precision code is a column, data semantics. (3) A multi-day protest coded as one event per day: the unit of count, the WHAT screen and task103's fan-out. (4) Coverage driven by the watchers' own filing volume: task199. (5) Two monitoring lists overlapping, capture-recapture: this slot's own earlier line (the swap reads the same with two surveillance lists). (6) A machine-coded event classifier validated only on the opening months: task192. (7) Events backfilled into earlier weeks as reports arrive: task194's vintages.
  With this pass every Anomaly Detection task type in the taxonomy has been screened: 37 candidates across eight cells on 2026-11-01, each dead on a recorded measurement, the three rules, the WHAT screen, a column or key, a filed rule or a spent driver. What remains open for this number is the author's call: a waiver for a cell repeat (disease surveillance against task232's ban, or a spent driver re-sited), or the slot handed on.
- **(2026-11-03, fourth pass, under the author's instruction to proceed)** Eight candidates screened on paper before
  the draw, each with its default path, swap, anatomy and bin test; seven dead, the eighth carded:
  - A GWAS meta-analysis whose contributing cohorts share a control panel, so inverse-variance pooling as if
    independent inflates the loci the shared controls deviate on: the abstraction is task195's paired difference on
    shared units (shipped 10-17), and task200's slot killed it on the same test.
  - Fast-trip protection on fire-season days turning transient faults into sustained interruptions: the artifact is a
    policy counterfactual, and once the estimand is a fault count the step is reading the estimand (faults against
    interruptions), data semantics.
  - A drug's disproportionality inherited from a co-prescribed cause (the innocent bystander): task181 v1's pooled
    sources in other nouns, a pharmacovigilance reflex, and the comparator background is the estimand's comparison.
  - A business survey's ratio imputation under nonresponse that a flood made informative, read from later VAT returns:
    task275's re-imputation of the unobserved from a record about them (approved).
  - Estuarine sampling locked to a tidal phase: dead on the physics, since fortnightly fixed-time sampling drifts about
    37 minutes of tidal phase a visit and spreads over the whole cycle within a year; only a protocol cutover makes the
    artifact, which is the dated-cutover family.
  - Lightning outages normalised by strokes near each feeder's route: task182's own response to a shared driver, and the
    corridor radius is a free parameter the bin test fails on.
  - Restoration time inflated by a shared crew pool: the outage system records dispatch, so the queue is a column
    subtraction, and single-server queueing reads the same in any field (the swap fails).
  - Carded: a cash-intensive business member's cash judged against the counter trade its card acquirer settles.
- **(2026-11-03) Prototype iterations of the carded draw, each dead as built:** proto1 and proto2 put the fronts at
  their own trade's typical size, so the peer route flagged one of them (z 2.9) and large honest members' absolute
  excess (to CAD 385,000 at a 30 per cent cash share) beat the second front; the fronts were redrawn as small genuine
  traders whose total cash matches the band they declared. proto3 tested the absolute CAD threshold alone and let large
  honest members through, so the programme's test carries a relative arm (at least twice the produced cash). proto4
  held 17 of 20 worlds; the three that failed had a front whose own genuine cash-to-card ratio sat below its trade's, so
  laundering set as a multiple of its own cash fell near the relative arm; the generator sets each front's laundering
  against its trade's relation and asserts the margin. In every prototype a cash-intensity ranking within the trade
  put the takeaway front first while the test computed on turnover shares referred nobody: the call is the test's
  designation, never a ranking, so that ranking is no route to it.
- **(2026-11-03, stage 2 and 3) Ask and pack revisions before precut, each dead as first built:** an ask for each
  referred member's cash by quarter was keyed to the call (a split of the committed figure for the members a response
  refers, `supplemental-stumping` ban 4) and was cut; the branch counter channel was cut from the branch ask because the
  posting's own transit places every counter deposit, so it carried no device; the old LCTR lateness ran from the log's
  own transaction date, which the cracker executes, and now runs from the day the first cash was received (section 6.2);
  the large business cheques deposited with counter cash let a reading of the deposit's whole credit as cash refer two
  wholesale grocers (Westside Supermarket and Scarlet Farm Market), so members taking larger cheques scan them in the
  banking app and the reading leaves the call (R2); ATM deposits at Willowbrook terminals before their installation were
  impossible records, so terminals are chosen among those in service on the day, and Langley City's lobby terminal
  now moves to Willowbrook Crossing under its own number; the case register's numbers ran without a gap and now skip
  where a number was withdrawn; the LCTR log held exactly 1,000 rows and now holds 1,029.
- **(2026-11-03, stage 4) The pickup manifest listed one bag twice on one pickup date, 79 bag-days in all, 16 of them
  at two depositories (32 postings at transit 19004, all in 2026).** The ledger let a member reach for a bag that
  was still out: two accounts' deposits made one evening at two depositories, or a Friday bag and a holiday Monday
  bag both counted on the Tuesday. The judge found the night column reproduced only under keeping the last listing
  in file order, with other tie-breaks moving six branches by up to about 8 thousand. Rejected: filing a tie-break
  (a filed HOW) and adding a key to the posting (an easier device than the ask's). Fixed in the producing system's
  own way: a bag is out from its drop until it is counted, two deposits made one evening at one depository travel in
  one bag, a member whose every bag is out has a spare (12 issued), and the carrier lists each bag once per pickup;
  the random draws are untouched, so only 65 night-bag narratives changed and the night column now equals the clean
  truth to the dollar (`checks.py` SF21, Z15). Five night cells moved (Newton 1,494,000 to 1,493,000, Richmond Centre
  1,631,000 to 1,636,000, Coquitlam Centre 1,569,000 to 1,566,000, Uptown New Westminster 1,000,000 to 1,001,000,
  Willowbrook 488,000 to 487,000); nothing else in figures.json moved (5 of 103 keys). `freeze.py check task188 --mode
  determinism --allow` with the five night keys leaves one finding, the Deliverable Answers block moving, which that
  mode reports whenever any ask figure moves; `freeze.py check task188 --mode rubric` passes (the main call, the stump
  and every frozen figure unchanged, 5 ask figures moved). The same pass filed the due day's clock in section 6.2
  ("the day, on Pacific time, on which"): the UTC day of the same receipt filed 2, 3, 8 and 7 late against 2, 6, 11
  and 9 (`checks.py` SF15), which closes a fork without naming a method; rebuilt the terms of reference as a plain
  Word package; and gave the bag register its retired and lost bags, with status dates, on counter days.
- **(2026-11-03, judge pass 5) Three closures refused before the repair:** filing the produced-cash estimator or its
  comparison group (the median of cash per card dollar across same-type members) to close the workbook's fork files
  the HOW and turns the decisive step into rule application, so the fork was closed on the grading side; grading
  Sunrise Fresh Market's excess bin as a stable workbook cell fails on measurement (the eight statistics print it at
  425,000, 475,000 and 500,000); an SF row showing the Corrections inert fails on measurement (every row a report and
  a reference's last submission each move filed or late figures), so section 6.2 files the WHAT instead.
- **(2026-11-03, judge pass 6) Two closures of Langley City's removal day refused before the repair:** the judge's
  optional note row reading the removal day as in force, because the note is not shipped and the literal reader would
  still hold four readings (1,257,000 to 1,278,000); and a filed sentence that a terminal is in force on its removal
  day, which adds a counting convention for the reader to execute and leaves the UTC day and the business date open.
  Closed instead in the directory's own record, the removal dated on the day the fixtures were taken out (SF25).
