# task196 design note

Kelverstone Mutual sets Castlegate Payments' scam incidence index for the indemnity year beginning
1 October 2027. Architecture 2. Owner oviya13ya, wave 4.

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task196.json`, v2, registered 2026-10-17, verdict WARN |
| Pairing | banking-credit-financial-risk / `fraud-aml-detection`, objective anomaly-detection |
| Niche | sizing the scam cases a payment firm's own detection never sees, from its payments' matches against the scheme's register of reported mule accounts |
| Shape | 03, bridge between two totals: the member's recorded case count walked to its estimated true case count, one reconciling line at a time |
| Strategy | `other`, capture interference (the honest vocabulary key, `causal_design`, was taken by task197 five minutes before this card filed; the mechanism is named in the card's notes) |
| Gap, generators, Gate G | population and time; G12 decisive, then G3 and G17; `method_or_model_selection` |
| Layer 2 | `estimand_identification`, pattern `own:contaminated-second-capture` |
| Decision type | `quantity_figure`, answer unit a rate, question form how-many, opening move question-first |
| World | United Kingdom, GBP, a mutual indemnity association owned by its twelve member payment firms; trustees decide at a meeting (`trustees_or_governors` / `vote_or_meeting` / `cooperative_or_member_body`) |
| Forum and forcing event | the trustees' meeting of 14 July 2027, at which Castlegate's triennial review falls due |
| People | Lydia Page, Caleb Ramsey, Debra Dawson, all from `guard.py names --geo GB --seed 196` |

**Data-native sentence.** In this pack a scam case can be sighted twice, once by the member that sent the
payment and once by the scheme's register of beneficiary accounts other firms have reported, and the second
sighting exists for 238 of Castlegate's 358 doubly-sighted cases only because Castlegate itself asked the
receiving firm to return the money after it had already opened the case, so the overlap the two-source
estimator divides by is mostly Castlegate's own work coming back to it.

**Sources read, one line each.**

- `analytical_tasks/02_anomaly_detection/AD19` seed: world, decision and quantity only (a body adopting a
  fleet-wide rule), and nothing of its mechanism, which was decoy-era.
- `guide-to-prompt/references/domains/README.md`: the client taxonomy. Fourteen task types serve anomaly
  detection and none of them is in actuarial-science-insurance, which is why the assigned ground could not
  carry the objective and the pairing moved to the nearest serving task type.
- `guide-to-prompt/references/shapes/03-bridge-between-two-totals.md`: the bridge's criteria come from each
  reconciling item, and the items must be discoverable from the pack rather than listed anywhere. Taken; the
  adjudication-rule seam of its worked prompts is not, because there is no candidate source to adopt here.
- `stumping/references/strategies.md` Part 2 (the laws) and Part 6 (the deaths): L1, L4, L5, L7 and L8 are
  answered below. The one adjacent death is **recovering what an instrument could not observe (89 v6, the
  judge repairs the instrument)**, answered in `## Literal reader`.
- `determinism-check` and `references/forcing-the-answer.md`: the estimand's five parts are filed, the
  comparison among them; the method is forced by the data, with C1 and C4 doing the closing.
- `supplemental-stumping` Part 0: the pair arithmetic was solved in `generator/ceiling.py` before a single
  ask was drafted, and it sized the construction layer.

## Default path

The pipeline a competent analyst builds from the question's words and the files' grain.

1. Read `governance/indemnity_standard.pdf`: the index for the indemnity year beginning 1 October 2027 is
   the incidence of scam cases among the member's customers over the scheme year ended 31 March 2027,
   whether or not the member's own systems recorded them, per million payments sent.
2. Filter `claims/case_register_2024_2027.csv` to Castlegate, cover class APP scam, payment date inside the
   scheme year: 400 cases.
3. Take Castlegate's payments sent from the revised quarterly returns in
   `returns/member_quarterly_returns.xlsx`, converting the thousands column on the pre-2024/25 layout:
   23.04 million payments.
4. Read the population clause again, see that unrecorded cases are in it, and reach for the pack's second
   sighting of the same cases: `scheme/member_payment_matches.csv`, Castlegate's payments that match an
   account on `scheme/mule_account_register.csv`, 445 matched payments, of which 358 are also in the case
   register and 87 are not.
5. Run the two-source estimate on those three counts: 400 x 445 / 358 = 497.2 cases.
6. Divide by the volume and round as the question asks: 497.2 / 23.04 = 21.6, so 22 cases per million payments.
7. Build the bridge and the chart from the same two numbers for the other three review-group members, and
   file the index.

**Ends on:** 22 cases per million payments (497.2 cases, 21.6 before rounding), and a bridge whose reconciling line reads as the
unrecorded cases the matches imply.

**Golden:** 30 cases per million payments (690.0 cases, 29.95 before rounding), the two-source estimate run against the 207
registrations that no recall request of Castlegate's preceded, of which 120 are also in its case register.

## Stump sentence

The solver files 22 cases per million payments for Castlegate because it treats every one of the 445
matches between Castlegate's payments and the scheme's mule register as a second, independent sighting of
the case, when 238 of the 358 matches that are also its own cases exist only because Castlegate asked the
receiving firm to return the money after opening the case, so the overlap it divides by is its own work and
the estimate of what neither channel saw comes out less than half its true size.

## Three rules

**Task type:** fraud-aml-detection in banking-credit-financial-risk, which serves anomaly detection in the
client taxonomy; the build does what fraud analytics does when it sizes undetected loss.

**Domain test:** the deciding quantity is the detection coverage of a payment firm's own fraud controls and
the case count it implies, estimated by capture-recapture against the counterparty side's own mule-account
reporting, with the independence of the two captures tested against the firm's own recall activity, which is
how fraud and financial-crime analytics sizes what its monitoring missed.

**Swap:** "Castlegate's customers suffered 30 scam cases per million payments against the 17 its own
register holds, because its systems see 58 per cent of them." Put workplace injury claims at member
employers or crop hail at member farms in place of scam reimbursements and there is no counterparty
institution holding a second record of the same loss event, no central register of the accounts that
received it, and no recall request of the firm's own to contaminate that register, so the second capture
channel cannot be formed and the quantity that decides the call does not exist.

**Layer 1:** the member return changes layout at the 2024/25 scheme year and moves payment volumes from
thousands to units, the mutual's indemnity year to 30 September runs against the scheme year to 31 March and
the calendar-year regulatory return, mule account references are padded and cased differently in the
register and in the match extract, Garnock Exchange joins part way through 2022/23, a preliminary and a
revised quarterly return overlap for two quarters, the trustees' pack carries its membership table inside a
PDF, and recoveries post as later credit rows against the original case. Each is what the mutual's own
systems produce; none is placed to be caught and none touches which registrations are an independent
sighting.

**Layer 2:** `estimand_identification`. The quantity is identified only through a capture channel that the
member's own detection cannot have produced, and the choice of what counts as that channel decides the
answer.

**Decisive step:** a capture is only a capture if the firm's own detection cannot have caused it, so the
independent channel is the 207 mule registrations that no recall request of Castlegate's preceded, found by
attributing each registration through `members/recall_requests.csv`, not by any rule about registration
dates.

**Not semantics:** every field read correctly still leaves the easy route on 22. The class code, the cover
definition, the payment date, the volume units and the register's status codes are all read right in the
default path; nothing in the mule register says who caused a registration, the registering party is the
receiving firm on both the independent and the self-produced rows, and no column separates them.

**Not rule application:** no filed rule or procedure names a channel pairing, an independence test, an
estimator or the recall log's role. The standard files the estimand and the evidence base and stops. A solver
that executes every stated rule in the pack, including the standard's own definitions and the scheme's
reimbursement rules, files 22.

**Analyst test:** a strong analyst reads the standard, matches every Castlegate payment to the mule register,
counts 400 cases, 445 matched payments and 358 in both, runs the two-source estimate and files 22 cases
per million payments, which is wrong because 238 of those 358 registrations were raised by receiving firms
only after Castlegate's own recall request, so the two sightings are not independent.

**Estimand:** filed in `governance/indemnity_standard.pdf` clause 4.2: "the incidence of scam cases arising
from payments its own customers sent in the scheme year ended 31 March 2027, whether or not the member's
systems recorded them, counted once a case however many payments it covers, per million payments sent as
reported on the member's revised quarterly returns, estimated on the mutual's evidence base at that date,
being the members' case registers and the scheme's mule-account register"; clause 4.3 maps it to the
indemnity year beginning 1 October 2027. Population, outcome, window, unit and comparison are all in those
two sentences, and the decisive step is none of the five.

**No decoy:** nothing is planted. The recall requests are what a firm does when it tries to get a victim's
money back, the registrations that follow them are the receiving firms doing their own reporting, and no
memo, draft, briefing or stakeholder figure argues for any answer. The trustees' pack carries facts and no
verdict, no prior index and no commentary on Castlegate.

**No certified replay:** there is no corpus, no back-test, no calibration file and no closed-year outturn in
the pack (`calibration_form: none`). The method is not recovered by reproducing any certified figure; it is
forced by the shipped recall log and by arithmetic on the shipped dates.

**Lesson:** a model learns that a second sighting is only evidence when the first sighting cannot have caused
it, and that the fix is attribution through the operational record rather than a rule about dates. No build
on file teaches it: task456 combines records independent by construction, task462 scales detections by a
size-dependent detection probability, and task194 counts events that arrive late rather than events that
never arrive.

## Readability screen

Six tests per rung: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene battery, 6 linear.

| Rung | 1 filed | 2 schema | 3 reflex | 4 bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the two-source estimate on every match (22) | the population clause sends the solver looking for a second sighting | the match extract is a header-found join on the payment reference | yes, the first move once unrecorded cases are in scope | none | ties everywhere | one ratio | readable |
| 1 exclude registrations dated 0 to 2 days after the case (24) | nothing | two date columns, one per file | yes, a lag histogram is the independence check | none | no | no | readable |
| 2 exclude every registration dated after the case (43) | nothing | the same two date columns | yes, the thorough version of rung 1 | none | no | no | readable |
| 3 (decisive) attribute each registration through the member's own recall-request log (30) | no clause names the log, independence, a channel pairing or an estimator | no column marks a self-produced registration; the registering party is the receiving firm on both kinds, and the log is a third file joined on the payment reference, then compared on dates | no: every reflex on the obvious chain lands on 22, 24 or 43 | none shipped | the battery's sweeps pass on every rung | no | silent |

**Why rung 3 is silent when rungs 1 and 2 are not.** The registration-lag spike is meant to be found: 143 of
Castlegate's 445 matches register within two days of its own case opening, against about seven expected if
the register were independent of the case, and that pattern is visible from the two date columns alone. It
tells a solver the captures are dependent, and it does not tell it the estimate: the two constructions it
supports land at 24 and 43, and nothing in the pack selects a window between them. Only the recall log
attributes each registration to a cause, and the log is unannounced: no sentence points at it, its columns
are named for what the firm does (`request_sent_date`, `funds_returned`, `destination_firm_type`) and never
for what the estimate needs, and the standard's evidence-base clause names the case registers and the mule
register without naming it.

**Reflex sweep.** Pool the members: 10.4 per million, wrong. Scale by volume: unchanged, wrong. Stratify on
every visible attribute of the matched payments (channel, destination firm type, value band): 21.3 to 21.9,
wrong. Trend the recorded counts: 18.1, wrong. Shrink Castlegate's recorded rate toward the book: 18.2,
wrong. Add the ombudsman file as a third source without the attribution: 22.8, wrong. Run the hygiene
battery and repair everything it finds: 21.6, unchanged. Every figure in this sweep is the value before
rounding and none of them prints 30.

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "scam case" | cover class APP scam only | both cover classes, APP and unauthorised | 61.2 | standard clause 2.1 defines the cover as authorised push payment reimbursements; the register's class code is in the dictionary |
| SF2 | "its customers" | cases on payments the member's own customers sent | cases where the member received the funds | 4.9 | standard clause 4.2 says "its own customers sent"; the register holds a sending-side flag and the dictionary defines it |
| SF3 | window attribution | the payment date falls in the scheme year | the case open date, or the notification date | 20.9, 20.4 | standard clause 4.2, "arising from payments its own customers sent in the scheme year" |
| SF4 | "payments sent" | the revised quarterly return's payments-sent field | faster payments only; payments to new payees only | 25.6, 34.1 | standard clause 4.2 names the return field; the return's own header defines it |
| SF5 | "whether or not recorded" | the population includes cases no system holds | only recorded cases | 17 | standard clause 4.2's own words; a recorded-only reading answers a different question |
| SF6 | the index year | the indemnity year beginning 1 October 2027 takes the scheme year ended 31 March 2027 | re-measure on the current part-year | not computable, the base is filed as at 31 March 2027 | standard clause 4.3 |
| SF7 | rounding | the index to the nearest whole case per million payments, the shares to one decimal, once at the end | rounded per member then averaged; the index carried to one decimal | 30 either way; 29.9 at one decimal | the asking sentence states each rounding once and names the figures it governs, and C1: the index is one ratio per member, so no averaging path exists |
| SF8 | "a case" | counted once however many payments it covers | counted per payment | 31.1 | standard clause 4.2, "counted once a case however many payments it covers" |
| SF9 | matched payment | account reference normalised, 445 rows | raw reference, 445 rows | same call | C1: every licensed normalisation (pad, case, strip) selects the same 445 payments and the same 358 cases, asserted on both counts |
| SF10 | register status | registered and expired registrations count | exclude expired | same call | C1: no matched payment's account carries status expired or withdrawn, asserted at zero |
| SF12 | the two-source estimate | the plain Lincoln-Petersen form, 400 x 207 / 120 | Chapman's bias-corrected form, 401 x 208 / 121 minus 1 | same call: 688.3 cases, 29.88 per million, printing 30 | C1 asserted on the cut pack: both forms print the same whole-case index, which is why the index is stated to the nearest whole case rather than to one decimal, where they would print 29.8 and 29.7 |
| SF11 | "preceded" | the recall request's date is strictly earlier than the registration date | same-day counts as preceding | same call | C1: no matched payment has a recall request dated the same day as the registration, asserted at zero |

## Ladder

| Rung | Analysis | Figure | Dies to |
|---|---|---|---|
| none | the recorded register count, the question not answered | 17 (17.36) | the population clause in the standard |
| 0 | two-source estimate on all 445 matches | 22 (21.58) | the registration-lag spike |
| 1 | exclude the 0 to 2 day spike window | 24 (24.49) | the member-caused tail: 95 of the 238 register later than two days |
| 2 | exclude every registration dated after the case | 43 (42.53) | the recall log: 60 of the independent registrations also post-date the case, and the log says no request of Castlegate's preceded them |
| 3 | attribute through the recall log: 207 independent registrations, 120 of them cases | **30** (29.95) | nothing |

**Position and dominance.** The golden is bracketed: 17, 22 and 24 below, 43 above, so no half-applied
correction lands on it (L5). On the values before rounding the nearest wrong cell is 24.49, 18.2 per cent
away, well above the 6 per cent floor, and the next is 42.53 at 42.0 per cent. The decisive move is the
largest of the four (plus 5.46 against plus 4.22 and plus 2.91 for the corrections below it), so it is not
the smallest move on the ladder (37's law). The golden's printed cell is mid-bin: 29.95 against a bin
centre of 30 and a width of 1, so the distance to the nearest edge is 0.45 against the 0.3 floor.

**Grid.** Four channel constructions x three window attributions (SF3) x two volume readings (SF4) = 24
cells, every cell computed in `generator/checks.py`, each distinct and each mapped to the sentence it
violates. The date-only family is a one-parameter family: as the exclusion window widens from two days to
unbounded the estimate rises monotonically from 24.49 to 42.53. Every whole-day window from 0 to 120 is
swept in `generator/checks.py`, and the assertion is the one the data can carry: no window a shipped word
names or a person would reach for prints 30, the sweep returning 24 at two days, 26 at a week, 28 at a
fortnight, 31 at a month, 33 at sixty days and 43 unbounded. The crossing sits at twenty-five to
twenty-eight days, which no clause, column or convention in the pack names, so the golden is reachable
through the attribution and not through a date parameter anybody files.

**Worth, on the graded figure.** The decisive rung moves the graded figure from 24 to 30 and the graded
name is not an entity but the figure itself, so there is no name-without-figure escape (500 v1's finding).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | filed in clause 4.2, unrecorded cases stated as in scope; C1 on class and side selection, row counts asserted |
| 2 | Unit of account | the case, filed as counted once however many payments it covers (SF8); the denominator's unit is a payment |
| 3 | Attribution window | the payment date, filed (SF3); C4, the two rivals computed at 20.9 and 20.4 and each mapped to clause 4.2 |
| 4 | As-of dating | the evidence base is as at 31 March 2027, filed in clause 4.2; every file carries its own extract date in `metadata.json` |
| 5 | Version basis | the revised quarterly return supersedes the preliminary one, filed in the return's own cover sheet; C1, the two vintages differ only for two quarters of one member outside the review group |
| 6 | Denominator | payments sent, the return's named field, filed (SF4); C4 at 25.6 and 34.1 |
| 7 | Weighting | none: a count over a count, no pooling across members in the index |
| 8 | Window length | one scheme year, filed in clause 4.2; the mule register's history is used only to date registrations |
| 9 | Boundary inclusivity | "preceded" strictly earlier (SF11); C1, nothing on the boundary, asserted at zero same-day pairs |
| 10 | Rounding path | once at the end, the index to the nearest whole case per million payments and the shares to one decimal, both in the asking sentence; the case estimate stays an exact ratio of integers until the division, and the printed unit is set from the estimator family's own spread (SF12) rather than from the quantity's natural precision |
| 11 | Tie-break | none: one figure per member, no ranking in the call |
| 12 | Maturity and censoring | the base is as at 31 March 2027 and the index year mapping is filed, so late notification cannot move it; asserted that no row in the quarter-to-30-June file arises from a payment inside the call's window |
| 13 | Order of operations | the bridge's presentation order is filed in the mutual's reporting template; the index is one ratio, order-free |
| 14 | Row order | C1, asserted identical over six permutations of every input file |
| 15 | Duplicate resolution | C1: no matched payment's account carries two registrations, asserted at zero; exact duplicate rows in the match extract resolved by the filed key |
| 16 | Identity normalisation | account references padded and cased differently; C1 (SF9), same 445 payments under every licensed normalisation, asserted on row and entity counts |
| 17 | Netting against gross | not applicable to a count; recoveries are amounts and sit outside the call's path, which reads no amount column |
| 18 | Dimensional units | payment volumes in thousands on the pre-2024/25 layout and units after; C4, the unconverted reading computed at 21,500 per million, absurd by three orders and ruled out by the return's header |
| 19 | Code and status semantics | the register's status codes are in the dictionary; C1 (SF10), no matched payment is expired or withdrawn, asserted at zero |
| 20 | Integerisation | the case estimate is not rounded before the division; the printed figure rounds once |
| 21 | Clause scope | clause 4.2 scopes the index to one member, not to the book; the book-wide reading computed at 10.4 and ruled out by the clause |
| 22 | Forward window contents | the index is a rate, so the indemnity year's volumes are not an input and no driver file is needed; the register's notified volumes serve the asks only |

## Literal reader

A reader who executes clause 4.2 and 4.3 word for word, inferring nothing, must estimate the incidence of
cases the member's systems may not hold, from the two sources the clause names, and every reading of every
term in the fork table returns 30: the recorded-only reading is refused by the clause's own words, the
three window readings and the two volume readings are each refused by a quoted sentence, and the
normalisation, status and same-day readings converge on identical row counts. The method is forced by the
data, not by a filed criterion: the only parameter-free construction of an independent capture channel is
the recall log's attribution, the two date-only constructions are computed at 24 and 43 and neither is
the golden, and the one-parameter family between them has no shipped value selecting its parameter, asserted
over every whole-day window from 0 to 120. The adjacent death on file is **89 v6, recovering what an
instrument could not observe, where the judge repaired the instrument**; this build differs in that the
recovery is an identity on three shipped integers rather than a model of the instrument, the channel's
independence is attributed by a shipped operational log rather than estimated, and the instrument's own
output (the 400 recorded cases) is not repaired by any rung: every rung reads the same 400 rows.

## Oracles

- **The revised quarterly returns' case-count field.** Confirms 400 recorded cases on every rung, because
  every rung reads the same register rows and differs only in which registrations count as a sighting (L1,
  L8). Blind to the decisive move for that structural reason, and the blindness is computable: the index's
  numerator is the only quantity that moves and no control holds it.
- **The match extract's own trailer count.** Ties to its 9,812 rows under every normalisation (SF9).
- **`reference/national_app_scam_statistics.csv`** (declared distractor): published per million pounds of
  payment value, not per million payments, and the pack carries no value-to-count conversion, so it ties
  under no reading and nominates nothing.
- **`reference/aml_alert_summary.csv`** (declared distractor): alert volumes per member per quarter, a
  plausible coverage proxy that the solution never reads; it is uncorrelated with detection coverage in the
  shipped data by construction, asserted, so it cannot be used to back into the answer.
- No corpus, no back-test, no closed-year outturn, no prior index, no worked example. Nothing in the pack
  states or implies 22, 24, 30 or 43, or any of the values behind them.

## Ask sheet

**Pair ceiling:** 37.4
**Mirror leakage:** 13.2 per cent of ask weight
**Measured by:** `generator/ceiling.py` (stage 2 on the designed stops; re-run with `--pack` on the cut
bundle at stage 3, reading `generator/ask_stops.json`)

**Both columns, from the script.** Ask criteria N = 68, being 13 construction and 55 device. The cracker
lands the call and keeps 13 of 68, 0.191 of the ask weight, scoring 55.5. The mirror stops at rung 2, keeps
9 of 68, 0.132 of the ask weight, scoring 19.3. Pair 37.4 against a gate of 40, leaving 2.6 of the portal's
regrade margin.

**What the sizing cut, and why.** The first sizing graded a per-member recorded case count for 2026/27,
twelve figures, and measured 45.4. That figure is a group-by on one file: every strong response banks it and
it was the only construction figure the mirror also kept, so it bought the cracker points and cost the
mirror nothing. It is cut. The index is now graded for the four review-group members rather than all twelve
(the mutual's triennial cycle covers a third of the membership, so the scoping is the standard's, not the
rubric's), and the recorded count appears once, as the opening line of the named member's bridge. The
twelve-member table still ships in the workbook, carrying the recorded column as context the write-up does
not grade. The script's sweep prints all five sizings: 45.4, 39.4, 44.3, **37.4** and 32.9.

**The ceiling is not bought with device mass.** Three device asks is the floor the ask spec allows and
this build has exactly three, each wide rather than stacked, so the 2.6 of slack under the gate comes from
the construction-layer cut and not from extra devices. The alternative sizing is on the record and costs
2.0: grading all twelve members' indices rather than the review group's four measures 39.4, which clears the
gate, and it was not taken because a ceiling that only just clears rests on every device holding, while the
review group of four is the indemnity standard's own triennial scoping rather than a number chosen for the
arithmetic. The twelve-member table still ships as ungraded context either way.

**Consequences of the cut, checked.** No graded figure outside the construction layer quotes a per-member
recorded count; no ask's wording presupposes a column the pack no longer carries, because the cut removed a
graded figure and no file or column; and the deliverable keeps the column, so nothing in the workbook or the
csv is left pointing at a figure the write-up does not state. The chart's recorded series is not the
cut figure returning: it covers the review group's four members, it is one of the six named chart parts
counted in C4, and the cut removed a graded table column rather than any column of the pack, so no ask can
presuppose data the bundle no longer carries. Re-checked at stage 3 against the goldens and `submission.md`
before `figures_check.py` runs, together with the rule that every graded figure is printed at the precision
its own asking sentence states, which no script checks.

### The construction layer

| id | Figures | Home (H18) | Landed call | Rung 2 response |
| C1 | the index for each of the four review-group members, to the nearest whole case per million payments | the call's own output on the trustees' review group | keeps 4 | miss |
| C3 | the named member's bridge, one line per reconciling item, three lines | the call's working | keeps 3 | keeps 3 |
| C4 | the review group's chart, named parts: the two series, the ordering, the highlighted member, the gap annotation, the title stating the finding | the decision read at a glance | keeps 6 | keeps 6 |

### The device asks

Each sits on rows outside the main call's declared population, which is Castlegate's and the other members'
APP-scam case-register rows inside the scheme year, the mule register, the match extract, the recall log, the
returns' payments-sent field and the member register. The call reads no amount column at all, so every
monetary quantity in the pack is outside its path.

| id | Ask | Figures | Primary device (silent) | Hazards shared | File and columns | Forcing figure (designed; measured at stage 3) |
|---|---|---|---|---|---|---|
| A | for each of the four quarters of 2026/27 and each of the three member tiers, the indemnity the mutual paid on unauthorised-fraud cases net of recoveries received by 31 March 2027, to the nearest pound, plus each quarter's total | 16 | D9 self-validation at a grain nothing names: each monthly settlement advice's total covers its own detail rows plus a residual adjustment line belonging to cases settled in an earlier quarter, so the advice is a rollup above its own parts for three months of the year and only a detail-against-total reconciliation per advice finds it | amounts in pence on the legacy export, recoveries as later credit rows, the 2024/25 template change | `settlements/settlement_advices.xlsx` plus `claims/case_transactions.csv`, 11 columns on the path | natural read 1,284,610 against golden 1,246,905 on the Q3 tier-2 figure, a gap of 37,705 against a rounding of 1 |
| B | for each of the twelve members, the number of scam cases notified in the quarter to 30 June 2027 and the number of those closed by that date | 24 | D5 scope, a silently partial extract: the Q1 notification file was cut on 20 June and the 21 to 30 June notifications sit in a supplementary file, while each member's own quarterly return states a case count that exceeds the main extract's rows for four members, so only a return-against-extract count reconciliation finds the gap | case references reissued across members, a notification withdrawn and reissued, two members' files in the pre-2024/25 layout | `notifications/q1_2027_28_notifications.csv`, its supplementary file and the returns workbook, 9 columns | natural read 31 against golden 47 cases on Netherby, a gap of 16 against a rounding of 1 |
| C | for each of the three recovery routes and each quarter of 2025/26, the share of the reimbursed amount recovered on cases closed in that quarter, to one decimal, plus each route's year total | 15 | D9 a control total true only in its own scope: the recovery statement's route totals are stated net of that route's own agent fee for the repatriation route alone, so the three route shares sum to the stated total while the repatriation share is understated against the case-level credits, and only summing credits by route across the two files finds it | recoveries keyed to the payment rather than the case, one case merged mid-year, a revised statement superseding the first | `settlements/recovery_statements.csv` plus `claims/case_transactions.csv`, 10 columns | natural read 12.4 against golden 18.9 per cent on the repatriation route, a gap of 6.5 against a rounding of 0.1 |

**Separation line.** Zero device rows and zero hazard rows inside the main call's declared population,
asserted by count in `generator/checks.py`: no device touches an APP-scam case-register row inside the scheme
year, the mule register, the match extract, the recall log or the returns' payments-sent field. Deleting
every device leaves the call's four rungs and every figure unchanged, asserted. No document the call reads
carries an ask's organ: the indemnity standard says nothing about settlement advices, notifications or
recovery routes.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| amounts in pence on the legacy export | A, C | A: 9 of 16 figures; C: 4 of 15 |
| recoveries posted as later credit rows | A, C | A: 12 of 16; C: 15 of 15 |
| the 2024/25 template change | A, B | A: 4 of 16; B: 6 of 24 |
| case references reissued across members | B, C | B: 8 of 24; C: 3 of 15 |

**Referee.** One byte-clean arbiter per designed disagreement, each handing over no level: the settlement
advice's own detail tab (ask A), the member's quarterly return case count (ask B) and the case-level credit
rows (ask C). None of them states an ask's answer and none is read by the call.

### Cracker sheet

The cracker landed the call, ran the hygiene battery (key uniqueness, exact duplicates, unmatched joins,
fan-out, count ties), executed every filed rule the pack points at and matched every control and published
figure. A hit is within half the stated rounding.

| Ask figure | What the cracker computes | Why it misses | Cracker |
|---|---|---|---|
| A, each quarter x tier indemnity | sums the advices, nets the credit rows it finds, converts the pence export | the residual adjustment line is inside the advice total and belongs to an earlier quarter; nothing names it and no sweep reconciles a rollup to its own detail | miss |
| A, each quarter's total | the same sum one level up | carries the same residual, three months of the year | miss |
| B, cases notified per member | the main Q1 extract, deduplicated, reissued references resolved | the 21 to 30 June notifications are in a second file the battery never asks for; the extract's own trailer agrees with its rows | miss |
| B, cases closed by 30 June per member | the same extract's closure flag | the same missing rows carry eleven closures | miss |
| C, recovery share per route per quarter | the recovery statement's route columns, cases closed in the quarter | the repatriation route's stated total is net of its agent fee and the case-level credits are gross; the three shares still sum to the stated total | miss |
| C, each route's year total | the statement's own year column | the same scope difference | miss |

**Blind-response test.** The widest graded component is ask B's twenty-four figures. A response applying one
flat closure rate to every member's notified count reproduces 3 of 24 within half a unit; a constant response
reproduces 1 of 24; an all-nil response 0 of 24. Under a quarter of the cells are recoverable without the
analysis, so the component measures the work.

## Tried and rejected

- **Architecture 1, an insurance experience rating** (frequency repeats for a member, severity does not, so
  the aggregate rate hides a frequency step): redrawn at stage 1 on 2026-10-17 before any file was cut. The
  deciding quantity was a pure premium with component-wise credibility, which is actuarial science's own
  instrument and not fraud and AML detection's, so the client's swap test passed with workplace injury claims
  or crop hail in place of scam reimbursements and the domain read as a backdrop (10/10 rule 1). Its ladder
  arithmetic (a 1.56x gap between the naive and the correct rate) is spent and its lineage sits on the card.
- **The actuarial pairing itself** (actuarial-science-insurance / reserving-development-triangles, the
  assigned ground): no task type in that domain serves anomaly detection, so `guard.py check` blocks the draw
  as `three_rules.task_type` and the three alternates named in the assignment (mortality-longevity,
  catastrophe-exposure-accumulation, reinsurance-capital) do not serve it either.
- **A member-level credibility stump inside architecture 1** (small members' rates are noisy, so rank on the
  shrunk rate): dropped at the draw because the decisive measure would have tracked unit size, which is the
  death on file at task57 (+0.98 correlation).
- **A filed back-test criterion to force the estimator** (the basis adopted is the one that comes closest to
  each closed year's outturn): dropped with architecture 1. It makes the decisive rung readable on test 4 and
  it needed a closed-year outturn file, which is a control bench the record kills; the data forces the method
  here instead, so `calibration_form` is `none`.
- **Three-source capture-recapture with a log-linear interaction term** (member register, mule register,
  ombudsman complaints): rejected on determinism. The model's MLE and the collapsed two-source estimate
  differ by sampling noise rather than by a reading, two defensible estimators would have printed different
  figures, and the ombudsman counts are too small to separate them.
- **Identifying the independent channel by a column** (a reporting-party or reason code in the mule
  register): rejected because it makes the decisive move a row predicate, which the readability screen's
  test 2 kills. The registering party is the receiving firm on both kinds of row, so no column can separate
  them and the recall log is the only route.
- **A date rule as the golden** (exclude registrations dated after the member's own case): kept as rung 2 at
  43 rather than as the answer, because the member-caused registrations run out to seventy days and sixty
  of the independent ones post-date the case, so no date rule recovers the channel.
- **Grading all twelve members' indices and the recorded-count column**: measured 45.4 and 44.3 in
  `generator/ceiling.py`, over the gate, and cut to the review group of four with the recorded column folded
  into the bridge's opening line.
- **`causal_design` as the strategy label**: the honest key for capture interference, taken by task197 five
  minutes before this card filed, so the card carries `other` with the mechanism named in its notes rather
  than a negotiated axis.
