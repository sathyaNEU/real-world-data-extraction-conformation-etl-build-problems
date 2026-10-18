# task196 design note

Kelverstone Mutual sets Castlegate Payments' scam incidence index for the indemnity year beginning
1 October 2027. Architecture 2. Owner oviya13ya, wave 4.

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task196.json`, v2, registered 2026-10-17, verdict WARN |
| Pairing | banking-credit-financial-risk / `fraud-aml-detection`, objective anomaly-detection |
| Niche | sizing the scam cases a payment firm's own detection never sees, from its payments' matches against the scheme's register of reported mule accounts |
| Shape | 03, bridge between two totals: the member's recorded incidence walked to its estimated true incidence, one reconciling line at a time, every line in index units |
| Strategy | `other`, capture interference (the honest vocabulary key, `causal_design`, was taken by task197 five minutes before this card filed; the mechanism is named in the card's notes) |
| Gap, generators, Gate G | population and time; G12 decisive, then G3 and G17; `method_or_model_selection` |
| Layer 2 | `estimand_identification`, pattern `own:contaminated-second-capture` |
| Decision type | `quantity_figure`, answer unit a rate, question form how-many, opening move question-first |
| World | United Kingdom, GBP, a mutual indemnity association owned by its twelve member payment firms; trustees decide at a meeting (`trustees_or_governors` / `vote_or_meeting` / `cooperative_or_member_body`) |
| Forum and forcing event | the trustees' meeting of 14 July 2027, at which Castlegate's triennial review falls due |
| People | Lydia Page, Caleb Ramsey, Debra Dawson, all from `guard.py names --geo GB --seed 196`, each a signatory and none of them a voice |
| Dates | evidence base closes 31 March 2027; every extract pulled 2 July 2027, which is the as-of for `leak.py` sweep 9; trustees meet 14 July 2027; the index applies to the indemnity year from 1 October 2027 |
| Pack | 19 files, four formats (csv, xlsx, pdf, txt); the spine is `case_register_2024_27.csv` at 18,283 rows, the volume gate is met by `case_payments.csv` at 33,865 rows and `mule_account_register.csv` at 29,988; three declared distractors |

**Data-native sentence.** In this pack a scam case can be sighted twice, once by the member that sent the
payment and once by the scheme's register of beneficiary accounts other firms have reported, and the second
sighting exists for 125 of Castlegate's 282 doubly-sighted cases only because Castlegate itself asked the
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
   22.23 million payments.
4. Read the population clause again, see that unrecorded cases are in it, and reach for the pack's second
   sighting of the same cases: `member_payment_matches.csv`, Castlegate's payments that match an account on
   `mule_account_register.csv`, 395 matched payments, of which 282 are also in the case register and 113 are
   not.
5. Run the two-source estimate on those three counts: 400 x 395 / 282 = 560.3 cases.
6. Divide by the volume and round as the question asks: 507.1 / 22.2333 = 22.74, so 23 cases per million
   payments.
7. Build the bridge and the chart from the same two numbers for the other three review-group members, and
   file the index.

**Ends on:** 25 cases per million payments (560.3 cases, 25.200 per million before rounding), and a bridge whose reconciling line reads as the
unrecorded cases the matches imply.

**Golden:** 31 cases per million payments (687.9 cases, 30.940 per million before rounding), the
two-source estimate run against the 270 registrations that no fund-return request of Castlegate's
preceded, of which 157 are also in its own case register.

## Stump sentence

The solver files 25 cases per million payments for Castlegate because it treats every one of the 395
matches between Castlegate's payments and the scheme's mule register as a second, independent sighting of
the case, when 125 of the 282 matches that are also its own cases exist only because Castlegate asked the
receiving firm to return the money after opening the case, so the overlap it divides by is partly its own
work and what neither channel saw comes out at about a quarter of its true size, 47.3 cases against
174.9 on the same observed union of 513.

## Three rules

**Task type:** fraud-aml-detection in banking-credit-financial-risk, which serves anomaly detection in the
client taxonomy; the build does what fraud analytics does when it sizes undetected loss.

**Domain test:** the deciding quantity is the detection coverage of a payment firm's own fraud controls and
the case count it implies, estimated by capture-recapture against the counterparty side's own mule-account
reporting, with the independence of the two captures tested against the firm's own recall activity, which is
how fraud and financial-crime analytics sizes what its monitoring missed.

**Swap:** "Castlegate's customers suffered 31 scam cases per million payments against the 18 its own
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
independent channel is the 270 mule registrations that no recall request of Castlegate's preceded, found by
attributing each registration through `members/recall_requests.csv`, not by any rule about registration
dates.

**Not semantics:** every field read correctly still leaves the easy route on 25. The class code, the cover
definition, the payment date, the volume units and the register's status codes are all read right in the
default path; nothing in the mule register says who caused a registration, the registering party is the
receiving firm on both the independent and the self-produced rows, and no column separates them.

**Not rule application:** no filed rule or procedure names a channel pairing, an independence test, an
estimator or the recall log's role. The standard files the estimand and the evidence base and stops. A solver
that executes every stated rule in the pack, including the standard's own definitions and the scheme's
reimbursement rules, files 25.

**Analyst test:** a strong analyst reads the standard, matches every Castlegate payment to the mule register,
counts 400 cases, 395 matched payments and 282 in both, runs the two-source estimate and files 25 cases
per million payments, which is wrong because 125 of those 282 registrations were raised by receiving firms
only after Castlegate's own fund-return request, so the two sightings are not independent.

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
| 0 the two-source estimate on every match (23) | the population clause sends the solver looking for a second sighting | the match extract is a header-found join on the payment reference | yes, the first move once unrecorded cases are in scope | none | ties everywhere | one ratio | readable |
| 1 exclude registrations dated inside a fortnight of the case (26) | nothing | two date columns, one per file | yes, a lag histogram is the independence check | none | no | no | readable |
| 2 exclude every registration dated after the case (40) | nothing | the same two date columns | yes, the thorough version of rung 1 | none | no | no | readable |
| 3 (decisive) attribute each registration through the member's own fund-return request log (31) | no clause names the log, independence, a channel pairing or an estimator | no column marks a self-produced registration; the registering party is the receiving firm on both kinds, and the log is a third file joined on the payment reference, then compared on dates | no: every reflex on the obvious chain lands on 25, 26 or 40 | none shipped | the battery's sweeps pass on every rung | no | silent |

**Why rung 3 is silent when rungs 1 and 2 are not.** The registration-lag spike is meant to be found: 114
of Castlegate's 395 matches register within six days of its own case opening, against 6.9 expected if the
register were independent of the case, and that pattern is visible from the two date columns alone. It
tells a solver the captures are dependent, and it does not tell it the estimate: the two constructions it
supports land at 26 and 40, and nothing in the pack selects a window between them. Only the recall log
attributes each registration to a cause, and the log is unannounced: no sentence points at it, its columns
are named for what the firm does (`request_sent_date`, `funds_returned`, `destination_firm_type`) and never
for what the estimate needs, and the standard's evidence-base clause names the case registers and the mule
register without naming it.

**Reflex sweep, measured on the cut pack.** Pool the members and take the book's own recorded rate: 13.29
per million. Take the book's rung 0: 14.56. Stratify rung 0 on every visible attribute of the matched
payments, by payment channel: 22.79, by destination firm type: 22.73. Trend its recorded rate across the
four scheme years: 18.16. Shrink its rung 0 toward the book's at a credibility of 0.8: 21.10, at 0.5:
18.65. Run the hygiene battery and repair everything it finds: 25.200, unchanged. Every figure here is the
value before rounding, every one is more than 6 per cent from the golden, and none of them prints 31.

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "scam case" | cover class APP scam only | both cover classes, scam and unauthorised | a different index, asserted in `checks.py` | standard clause 2.1 defines the cover as authorised push payment reimbursements; the register's class code is in the dictionary |
| SF2 | "its customers" | cases on payments the member's own customers sent | cases where the member received the funds | a different index, asserted | standard clause 4.2 says "its own customers sent"; the register holds a sending-side flag and the dictionary defines it |
| SF3 | window attribution | the payment date falls in the scheme year | the case open date, or the notification date | same call | standard clause 4.2, "arising from payments its own customers sent in the scheme year", and C1 as well: the open-date window selects 397 cases against the filed 400 and prints the same 31 (30.708), asserted in `checks.py`, so no reading of the window moves the call |
| SF4 | "payments sent" | the revised quarterly return's payments-sent field | faster payments only; payments to new payees only | a different index; the basis is filed | standard clause 4.2 names the return field; the return's own header defines it |
| SF5 | "whether or not recorded" | the population includes cases no system holds | only recorded cases | 18 (17.991) | standard clause 4.2's own words; a recorded-only reading answers a different question |
| SF6 | the index year | the indemnity year beginning 1 October 2027 takes the scheme year ended 31 March 2027 | re-measure on the current part-year | not computable, the base is filed as at 31 March 2027 | standard clause 4.3 |
| SF7 | rounding | the index to the nearest whole case per million payments, the shares to one decimal, once at the end | rounded per member then averaged; the index carried to one decimal | 31 either way; 30.9 at one decimal | the asking sentence states each rounding once and names the figures it governs, and C1: the index is one ratio per member, so no averaging path exists |
| SF8 | "a case" | counted once however many payments it covers | counted per payment | a different index, asserted | standard clause 4.2, "counted once a case however many payments it covers" |
| SF9 | matched payment | the account reference normalised as the feed note files it, digits with the account number padded back to eight | the raw string, which drops the accounts whose number starts with a zero | same call: the call reads the match extract's own registration date and case reference and never joins to the register | C1 asserted in `checks.py` and `verify.py`: the filed normalisation selects all 8,588 match rows, a raw join selects fewer, and the index is identical either way |
| SF10 | register status | registered and expired registrations count | exclude expired | same call | C1: no matched payment's account carries status expired or withdrawn, asserted at zero |
| SF12 | the two-source estimate | plain Petersen, 400 x 270 / 157 = 687.9 cases, 30.940 per million | Chapman 686.8 (30.890); Bailey 686.1 (30.858); continuity-corrected Petersen 687.3 (30.915); the conditional maximum likelihood estimate 687 (30.900); and the same estimate written as the independent channel over a capture probability read off the member's own cases, which can be taken off every own case (30.940), off the cases it asked the receiving firm about (30.935) or off the cases it never asked about (30.947); the observed union 513 (23.073) quoted as a lower bound | 31 under all eight forms; 23 under the union bound | C1 asserted in `checks.py` and again in `verify.py` on the shipped bytes: the eight forms span 0.29 per cent of the figure and every one prints 31, and the three capture-probability readings agree to four decimal places (0.392405, 0.392500, 0.392562) because the independent capture is assigned at the same rate inside every subset an analyst can cut, so no choice of subset crosses the printed bin; the union is not an estimator of the filed population but the count of cases the two channels did record, which clause 4.2's own words exclude |
| SF13 | a registration that predates its own payment | counts: the register is a standing list and the account was already on it | drop them, on the reading that a second sighting must postdate the event | same call | C1 alone, with no sentence anywhere in the pack: 167 of the 270 independent registrations predate their payment and the share is the same on both sides of the overlap (0.618 of the member's own cases against 0.619 of the rest), so dropping every one of them divides a smaller numerator by a proportionally smaller overlap and prints 31 (30.885), asserted in `checks.py` and `verify.py`. The feed note's sentence stating the persistence fact was deleted after the second leak read: the convergence had already closed the row, so the sentence bought nothing and pointed at the method (the single-use test) |
| SF14 | the quarter an indemnity line belongs to (ask 4) | the quarter the case the line pays closed in, which the asking sentence pins: "the indemnity the advices settled, by member tier and the 2026/27 quarter each case closed in" | the quarter of the advice that pays the line; the line's own month field read as a settlement month of its own | the advice quarter gives a different set of sixteen figures, 320,142.56 apart on the Q1 total; the line's own month gives the same sixteen | C1 asserted in `checks.py` and again in `verify.py` on the shipped bytes: every one of the 6,416 detail lines carries the month its own case closed in the register, 0 disagreeing, so the register's `closed_date` and the line's own month are one basis and not two. The advice's month is not a reading of the asking sentence at all, because the sentence dates each case by its own closure and the register dates it: 35 lines sit on an advice raised in a later quarter than their case closed |
| SF15 | the grain the sixteen figures sit at (ask 4) | the case, pinned by "each case" in the asking sentence | the advice detail line; the advice | the line grain gives the same sixteen figures; the advice grain differs on 16 of 16 | asserted: each case's lines carry one closure quarter and one tier, so the 3,662 lines roll up to 3,627 cases without moving a figure, while the advice grain holds the same 2,984,362.84 over the year and attributes 486,513.00 of it to the quarter its advice was raised in |
| SF16 | "member tier" (ask 4) | the contribution tier in `member_register.csv` | the tier the advice itself carries | same figures | C1: all 288 advices carry the tier the register carries, 0 disagreeing, asserted in `checks.py` and `verify.py` |
| SF17 | "the indemnity the advices settled" (ask 4) | `indemnity_paid_gbp` on the advice detail lines, which the dictionary defines as the amount the advice settled for that case | the register's `reimbursed_amount_gbp` on the same cases; the same net of the recovery credits the ledger posts later | the register column differs on 12 of 16 figures and the netting on 16 of 16 | the asking sentence names what the advices settled, and standard clause 5.2 credits a recovery against its case at the date the funds arrive rather than in an advice; both alternatives computed and asserted as different quantities, the register short by the 486,513.00 of top-up it does not carry |
| SF11 | "preceded" | the recall request's date is strictly earlier than the registration date | same-day counts as preceding | same call | C1: no matched payment has a recall request dated the same day as the registration, asserted at zero |

## Ask 4's basis and grain, enumerated

The re-judge read Gate G PASS, Gate H PASS, Gate F strong with no lever needed, Gates B and D PASS and the
main call forced with every critical component to the penny, and failed Gates C and E on **ask 4 alone**.
`determinism-check` sends an architecture back on Gate G or Gate H, the two gates that say the build is the
wrong build, so a Gate C and E failure confined to one supplementary ask is an ask-layer repair and spends
no architecture. This section is that repair: the asking sentence now carries the basis and the grain, and
no graded figure anywhere in the build moved.

**The defect.** The clause read "each line in the quarter it settles in", and the pack holds a settlement
month at two grains: on the advice (288 rows) and on the advice's own detail lines (6,416 rows). 35 detail
lines, all unauthorised fraud, carry a month earlier than the advice that pays them, which is the month that
case first settled, so both grains were licensed readings of one phrase and all sixteen graded figures
differed between them. The judge also held that the detail-month reading, read as a claim about when the
mutual settled, puts up to four advices into one member-cover-month, which clause 5.1 forbids.

**The wording.** Before: `Also unauthorised-fraud indemnity by member tier per 2026/27 quarter, each line in
the quarter it settles in, totals unrounded;`  After: `Also unauthorised-fraud indemnity the advices settled,
by member tier and the 2026/27 quarter each case closed in, totals unrounded;` The prompt is 997 characters
and its call sentence is byte-identical. The basis is now an event the register dates once (the case closed)
rather than a field the workbook carries twice, and the grain is the case. Clause 5.1 is satisfied rather
than contested: nothing claims four advices settled in one month, only that four advices pay lines on cases
that closed in one quarter, which is what a prior-period top-up is.

**Every basis the pack makes plausible for the period side**, each computed on the cut pack over the
sixteen graded figures (`generator/checks.py`, `generator/verify.py`, and the table reproduced by
`generator/ceiling.py --forcing`):

| Basis | Q1 total | Figures off the golden | Worst gap | Admitted by the pinned wording |
|---|---|---|---|---|
| the case's `closed_date` in `case_register_2024_27.csv`, scheme-year quarters | 984,521.08 | 0 of 16 | 0.00 | **yes, this is the golden** |
| the detail line's own `settlement_month` | 984,521.08 | 0 of 16 | 0.00 | yes, and it converges: the same month on 6,416 of 6,416 lines |
| the advice's `settlement_month`, lines summed under it | 664,378.52 | 16 of 16 | 320,142.56 on the Q1 total | no: the sentence dates each case by its own closure, and 35 lines sit on an advice raised a quarter later |
| the advice's `advice_date`, advice totals summed under it | 664,378.52 | 16 of 16 | 320,142.56 on the Q1 total | no, same reason, and this is the natural read the device rides on |
| the case's `payment_date` | 813,976.84 | 16 of 16 | 259,848.83 on the Q4 total | no: "closed in", not sent in |
| the case's `notified_date` | 842,965.43 | 16 of 16 | 233,187.43 on the Q4 total | no: "closed in", not recorded in |
| calendar quarters on the closure date | 596,560.32 | 16 of 16 | 387,960.76 on the Q1 total | no: a 2026/27 quarter is a quarter of the scheme year ended 31 March 2027 (clauses 4.2 and 4.3), and the recovery statement's own four quarters reproduce only on that convention |

**Every grain**, same figures: the case (the golden, 3,627 cases), the detail line (identical, 3,662 lines,
because each case's lines carry one closure quarter and one tier) and the advice (16 of 16 off, the rollup).
The three grains hold the same 2,984,362.84 of unauthorised indemnity over the year, so the difference
between them is attribution and never an unexplained amount: every one of the 288 advices ties to the sum of
its own detail lines and every `case_lines` equals its own row count.

**Every amount side:** `indemnity_paid_gbp` on the detail lines, which the dictionary defines as the amount
the advice settled for that case (the golden); `advice_total_gbp`, the same money one grain up; the
register's `reimbursed_amount_gbp` on the same cases, which differs on 12 of 16 figures because it does not
carry the 486,513.00 of prior-period top-up the advices paid, and which the sentence excludes by naming what
the advices settled; and those lines net of the recovery credits the ledger posts later, which differs on 16
of 16 and which clause 5.2 excludes by crediting a recovery against its case at the date the funds arrive
rather than in an advice. **Every tier side:** the register's contribution tier and the tier the advice
carries agree on all 288 advices.

So the pinned wording admits exactly one answer, reachable two ways on the basis and two ways on the grain,
and the committed sixteen figures are that answer unchanged.

**Why this basis and not the other two that would also close the fork.** A pin is paid for, and the two
obvious pins pay with the ask's whole difficulty. "Each line in the quarter its own settlement month states"
names the line-level field, so the natural read becomes a group-by of the detail sheet and the device dies.
"Each line in the quarter of the advice that settles it" makes the advice-grain rollup the golden, which is
the natural read itself, so every figure goes free and all sixteen change. On Part 0's weights the cost is
measurable: with ask 4 free to the response that lands the call the pair ceiling goes from 37.4 to 43.9, and
free to both responses to 50.3, against a gate of 40; deleting the ask rather than defending it leaves 52
criteria and a pair of 40.1, so there is no sizing escape and the ask has to keep a device. The pinned basis
keeps it: the closure quarter is not a column of the advices workbook, so a response working at the advice
grain still files 664,378.52 against 984,521.08 on the Q1 total and misses 16 of 16. The device is now the
grain rather than the reading, which is the shape `supplemental-stumping` Part 6 names as the one an
inconsistency nothing in the pack invites buys: a rollup above its own parts, found only by reconciling
amounts across grains, which no column description asks for and no sweep performs. The residual exposure is
stated rather than hidden: a response that executes the pinned basis literally, joining each line to the
register's `closed_date`, lands the ask. That is the honest ceiling of a grain device, and it is why the ask
sheet's cracker row for ask A reads miss on the measured natural read and not on an argument.

**What the pin governs and what it must leave alone.** It governs the sixteen unauthorised-fraud indemnity
figures and nothing else. The figures sitting next to it are ask 5's twelve notification counts and twelve
reported values, keyed to the notification dates in the quarter to 30 June 2027, and ask 6's fifteen recovery
shares, keyed to scam-reimbursement cases closed in each 2025/26 quarter: the clause reaches neither, because
it is scoped to what the advices settled on the unauthorised cover in 2026/27, and both are asserted
unchanged (`freeze.py check --mode rubric` reports 0 ask figures moved, and `checks.py` and `verify.py`
reproduce all 39 of their figures). The phrase "cases closed in the quarter" is the pack's own, from the
dictionary's definition of the recovery statement's stated column, so ask 4 and ask 6 share the
organisation's convention while their devices stay distinct: ask 4's is the advice grain's rollup, ask 6's is
a statement true only in its own scope.

**The 35 rows stay, and the measurement is why.** The question was whether the data can support a single
forced reading. It can: the line's own month is the month its case closed in the register on 6,416 of 6,416
detail lines, 0 disagreeing, so the field corroborates the pinned basis instead of competing with it, and
the pattern is the Layer 1 mess a monthly settlement run produces when the recoveries team closes an earlier
quarter off. Changing them would have moved sixteen graded figures to repair a sentence. What changed instead
is one clause of the prompt, one line of the write-up's block 4, the basis line on the golden's indemnity
sheet, and the assertions. `target.zip` is byte-identical to the pack the judge read, md5
58fea759d25de0f25cd583ff70449695 over 19 members, which is the scope proof.

## Ladder

| Rung | Analysis | Figure | Dies to |
|---|---|---|---|
| none | the recorded register count, the question not answered | 18 (17.991) | the population clause in the standard |
| 0 | two-source estimate on all 395 matches | 25 (25.200) | the registration-lag spike |
| 1 | exclude registrations inside a fortnight of the case | 27 (26.642) | the receiving firms' own cadences: the e-money and correspondent registrations fall outside a fortnight, so 83 of the 125 self-produced rows survive the cut |
| 2 | exclude every registration dated after the case | 36 (35.669) | the recall log: 42 of the independent registrations also post-date the case, every one of them on a case the member never asked about, and the log says no request of Castlegate's preceded them |
| 3 | attribute through the fund-return request log: 270 independent registrations, 157 of them cases | **31** (30.940) | nothing |

**Position and dominance.** The golden is bracketed: 18, 25 and 27 below, 36 above, so no half-applied
correction lands on it (L5). On the values before rounding the nearest wrong cell is 26.642, 13.9 per cent
away, well above the 6 per cent floor, and the next is 35.669 at 15.3 per cent. Every correction below the
decisive rung walks one way, 17.991 to 25.200 to 26.642 to 35.669 at 1.401x, 1.057x and 1.339x, and the
decisive move is the only one that reverses, coming back from 35.669 to 30.940 at 0.867x. Because it is the
only reversal no pair of half-applied corrections cancels onto it; the partial applications of rung 2 are
the date-window family, swept below. The golden's printed cell is mid-bin: 30.940 against a bin centre of
31 and a width of 1, so the distance to the nearest edge is 0.440 against the 0.3 floor, and all eight
licensed forms print the same 31 (SF12).

**Grid.** Four channel constructions x three window attributions (SF3) x two volume readings (SF4) = 24
cells, every cell computed in `generator/checks.py`, each distinct and each mapped to the sentence it
violates. The date-only family is a one-parameter family: as the exclusion window widens from nothing to
unbounded the estimate rises monotonically from 25.2 to 34.5, and the receiving firms' three registration
cadences (same day for a clearing bank, a fortnightly batch for an e-money institution, about six weeks
for a correspondent) make it step across the golden's printed bin instead of resting in it. Every whole-day
window from 0 to 120 is swept in `generator/checks.py` and again in `verify.py`, and the measured result is
stronger than the assertion the design needed: **no whole-day window at all prints the golden's integer
except 42**, and no window a shipped word names or a person would reach for comes near it, the named set
printing 25, 25, 25, 26, 26, 27, 27, 27, 30, 30, 30, 32, 33, 34 and 35 at 0, 1, 2, 3, 5, 7, 10, 14, 21, 28,
30, 45, 60, 90 and 120 days. Forty-two days is named by no clause, column or convention in the pack, so the
golden is reachable through the attribution and not through a date parameter anybody files. The family is
also bounded away from the golden at its near end: because the request gap holds every independent
registration at least 22 days ahead of the request that follows it, a window of 1, 2, 3, 5, 7, 14 or 21
days reclassifies no row at all and prints the golden exactly, which is asserted window by window.

**Worth, on the graded figure.** The decisive rung moves the graded figure from 27 to 31 and the graded
name is not an entity but the figure itself, so there is no name-without-figure escape (500 v1's finding).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | filed in clause 4.2, unrecorded cases stated as in scope; C1 on class and side selection, row counts asserted |
| 2 | Unit of account | the case, filed as counted once however many payments it covers (SF8); the denominator's unit is a payment |
| 3 | Attribution window | the payment date, filed (SF3); C4, the two rivals computed at 20.9 and 20.4 and each mapped to clause 4.2 |
| 4 | As-of dating | the case population is the scheme year ended 31 March 2027 and the evidence base is as it stands when the review is prepared, both filed in clause 4.2; the trustees' pack says the same, that the reviews are prepared from the evidence base as pulled for the meeting on 2 July 2027, and the prompt's own second sentence says the scheme year closed on 31 March while the register feed runs to that pull. C4: cutting the register at the scheme year end is computed at 32.522 and prints 33, and clause 4.2's own words bar it |
| 5 | Version basis | the revised quarterly return supersedes the preliminary one, filed in the return's own cover sheet; C1, the two vintages differ only for two quarters of one member outside the review group |
| 6 | Denominator | payments sent, the return's named field, filed (SF4); C4 at 25.6 and 34.1 |
| 7 | Weighting | none: a count over a count, no pooling across members in the index |
| 8 | Window length | one scheme year, filed in clause 4.2; the mule register's history is used only to date registrations |
| 9 | Boundary inclusivity | "preceded" strictly earlier (SF11); C1, nothing on the boundary, asserted at zero same-day pairs |
| 10 | Rounding path | once at the end, the index to the nearest whole case per million payments and the shares to one decimal, both in the asking sentence; the case estimate stays an exact ratio of integers until the division, and the printed unit is filed by clause 4.4 and restated in the asking sentence, and all eight licensed forms agree to one decimal as well (30.9), so the figure is determinate at the stated unit and at the finer one (SF12) |
| 11 | Tie-break | none: one figure per member, no ranking in the call |
| 12 | Maturity and censoring | the base is as at 31 March 2027 and the index year mapping is filed, so late notification cannot move it; asserted that no row in the quarter-to-30-June file arises from a payment inside the call's window |
| 13 | Order of operations | the bridge's presentation order is filed in the mutual's reporting template; the index is one ratio, order-free |
| 14 | Row order | C1, asserted identical over six permutations of every input file |
| 15 | Duplicate resolution | C1: no matched payment's account carries two registrations, asserted at zero; exact duplicate rows in the match extract resolved by the filed key |
| 16 | Identity normalisation | account references are padded in the register and unpadded in the match extract; C1 (SF9), the filed normalisation selects every match row and the call never joins to the register, asserted |
| 17 | Netting against gross | not applicable to a count; recoveries are amounts and sit outside the call's path, which reads no amount column |
| 18 | Dimensional units | payment volumes in thousands on the pre-2024/25 layout and units after; C4, the unconverted reading computed at 21,500 per million, absurd by three orders and ruled out by the return's header |
| 19 | Code and status semantics | the register's status codes are in the dictionary; C1 (SF10), no matched payment is expired or withdrawn, asserted at zero |
| 20 | Integerisation | the case estimate is not rounded before the division; the printed figure rounds once |
| 21 | Clause scope | clause 4.2 scopes the index to one member, not to the book; the book-wide reading computed at 10.4 and ruled out by the clause |
| 22 | Forward window contents | the index is a rate, so the indemnity year's volumes are not an input and no driver file is needed; the register's notified volumes serve the asks only |

## Literal reader

A reader who executes clause 4.2 and 4.3 word for word, inferring nothing, must estimate the incidence of
cases the member's systems may not hold, from the two sources the clause names, and every reading of every
term in the fork table returns 31: the recorded-only reading (18) is refused by the clause's own words, the
three window readings and the two volume readings are each refused by a quoted sentence, and the
normalisation, status and same-day readings converge on identical row counts. The method is forced by the
data, not by a filed criterion: the only parameter-free construction of an independent capture channel is
the fund-return log's attribution, the two date-only constructions are computed at 26 and 40 and neither is
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
- **The match extract.** Its 8,588 rows tie under every normalisation (SF9), and they tie for every rung alike, because each rung reads the same rows and differs only in which of them counts as an independent sighting.
- **`reference/national_app_scam_statistics.csv`** (declared distractor): published per million pounds of
  payment value, not per million payments, and the pack carries no value-to-count conversion, so it ties
  under no reading and nominates nothing.
- **`reference/aml_alert_summary.csv`** (declared distractor): alert volumes per member per quarter, a
  plausible coverage proxy that the solution never reads; it is uncorrelated with detection coverage in the
  shipped data by construction, asserted, so it cannot be used to back into the answer.
- No corpus, no back-test, no closed-year outturn, no prior index, no worked example. Nothing in the pack
  states or implies 18, 23, 26, 31 or 40, or any of the values behind them.

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

**The sizing sweep, verbatim from `generator/ceiling.py`.**

```
construction layer                                 N      Lc      Ls  cracker    pair
all twelve members indexed, recorded column gr    88   0.375   0.239     65.6    45.4
all twelve members indexed                        76   0.276   0.118     60.2    39.4
review group of four indexed, recorded column     80   0.312   0.263     62.2    44.3
review group of four indexed (shipped)            68   0.191   0.132     55.5    37.4
review group of four, no chart criteria           62   0.113   0.048     51.2    32.9
```

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
| A | the indemnity the advices settled on unauthorised fraud, for each of the four quarters of 2026/27 by the quarter each case closed in and each of the three member tiers, to the nearest pound, plus each quarter's total taken from the unrounded tier amounts | 16 | D6 grain, a rollup above its own parts: the mutual settles monthly by advice and a third of the unauthorised advices pay a prior-period top-up on a case that closed in an earlier quarter, so the advice's own month is not its cases' closure month and only a reconciliation of the advice total against its own lines, case by case, finds it. The asking sentence pins the basis (the quarter the case closed in) and the grain (the case), so the closure quarter is not a column of the workbook the natural read works in | amounts in pence on the 2023/24 extract, recoveries as later credit rows, the 2024/25 template change | `settlement_advices_2026_27.xlsx` (advices and advice detail) plus `case_register_2024_27.csv` for the closure dates and `case_payments.csv`, 11 columns on the path | measured on the cut pack by `ceiling.py --forcing` and `ask_stops_build.py`: the advice grain reads 664,378.52 against the golden 984,521.08 on the Q1 total, a gap of 320,142.56 against a rounding of 1, and 16 of 16 figures print differently, the narrowest of them by 5,278.73 |
| B | for each of the twelve members, the scam cases notified in the quarter to 30 June 2027 and the value they reported, to the nearest pound | 24 | D5 scope, a silently partial extract: the Q1 notification file was cut on 20 June and the 21 to 30 June notifications sit in the quarter-end supplementary file, while each member's own Q1 return states a case count the main extract's rows do not reach, so only a return-against-extract reconciliation finds the gap | case references allocated per member and scheme year, a quarter that straddles the mutual's own year end, the returns workbook's own vintage column | `notifications_2027_28_q1.csv`, `notifications_2027_28_q1_supplementary.csv` and the returns workbook's Q1 sheet, 9 columns | measured on the cut pack: the main extract alone reads 405,985 against the golden 460,362 on Brindlemere's reported value, the widest of the twenty-four, a gap of 54,377 against a rounding of 1, and 24 of 24 figures move, the narrowest of them by a whole case (Pelbury's 14 against 15) |
| C | for each of the three recovery routes and each quarter of 2025/26, the share of the reimbursed amount recovered on cases closed in that quarter, from the case-level credits, to one decimal, plus each route's total over the same four quarters | 15 | D9 a control total true only in its own scope: the statement counts a recovery in the quarter the money arrived rather than the quarter the case closed in, and states the repatriation route net of that route's own agent charge, so its route shares sum to its own stated total while disagreeing with the case-level credits | recoveries posted as later credit rows with their own value dates, cases closing across a quarter boundary, the 2023/24 extract's pence amounts | `recovery_statement_2025_26.csv` plus `case_payments.csv`, 10 columns | measured on the cut pack: the statement reads 2.3 against the golden 15.1 per cent on the Q2 beneficiary recall figure, a gap of 12.8 against a rounding of 0.1, and 15 of 15 figures move, the narrowest of them by 0.5 of a point |

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
advice's own detail tab with the register's closure dates on its unauthorised-fraud rows (ask A), the
member's quarterly return case count (ask B) and the case-level credit rows (ask C). None of them states an
ask's answer, and none sits inside the call's declared population: the call reads the register's APP-scam
rows inside the scheme year and ask A reads its unauthorised-fraud rows, asserted by count.

### Cracker sheet

The cracker landed the call, ran the hygiene battery (key uniqueness, exact duplicates, unmatched joins,
fan-out, count ties), executed every filed rule the pack points at and matched every control and published
figure. A hit is within half the stated rounding.

**The thirteen figures the cracker keeps, and why.** `ceiling.py` scores the cracker at 13 of 68, and those
thirteen are named here so the sheet and the measurement tell one story: the four review-group indices (C1),
the three lines of the named member's bridge (C3) and the six named parts of the review group's chart (C4).
All thirteen are the construction layer, which is the decisive construction's own output on a segment the
trustees want anyway, so a response that lands the call has them by definition. They are sized against the
pair arithmetic rather than defended with devices, which is what the sweep above does. The table below is the
55 device figures, every one of which the cracker misses.

| Ask figure | What the cracker computes | Why it misses | Cracker |
|---|---|---|---|
| A, each quarter x tier indemnity | sums the advices by their own settlement month, on the reading that the advice for a month settles the cases that closed in it; nets the credit rows it finds, converts the pence export | that reading is true of 3,627 of the 3,662 lines and false of 35: the advice is a rollup above its own parts, and only a reconciliation of each advice total against its own case lines finds it. Nothing names it, no column description asks for it and the hygiene battery does not reconcile amounts across grains. Measured: 664,378.52 against 984,521.08 on the Q1 total | miss |
| A, each quarter's total | the same sum one level up | carries the same attribution, in every quarter of the year | miss |
| B, cases notified per member | the main Q1 extract, deduplicated, references resolved | the 21 to 30 June notifications are in a second file no sweep asks for, and the main extract is internally consistent | miss |
| B, value reported per member | the same extract's payment amounts | the same missing rows carry the value, so every member's figure is short | miss |
| C, recovery share per route per quarter | the recovery statement's own route and quarter columns | the statement's quarter is the quarter the money arrived and the repatriation route is stated net of its agent charge, and it reconciles to its own stated total either way | miss |
| C, each route's year total | the statement's own year column | the same scope difference | miss |

**Blind-response test.** The widest graded component is ask B's twenty-four figures. A response applying one
flat rate per million payments to every member's volume reproduces none of the twelve counts within half a
unit and none of the twelve values; a constant response reproduces none; an all-nil response none. Nothing
in the component is recoverable without reading both extracts, so it measures the work.

## Checks answered

**`leak.py --asof 2027-07-02`: REVIEW, no LEAK.** Sweep 9 clean after two date fixes in the generator
(cases opened within twelve days of the extract now carry no closed date, and an unauthorised recovery
credit that would value after the extract is not posted). The three remaining REVIEW classes:

- **Sweep 3, fourteen answer figures.** All of them are the pack's own identifiers and clause numbers
  colliding with short figures the sweep lifted from the submission: the member codes KM-101 to KM-124
  against the three-digit substrings of the write-up's bracketed codes, and the standard's clause numbers
  4.4 and 5.1 against two of ask C's percentages. No golden figure of four digits or more appears anywhere
  under `target/`, which is the sweep's own test.
- **Sweep 4, three documents carrying stump-paragraph terms.** Four or five of twenty-five, and every one
  of them is a noun of the fiction (payment, members, scheme, trustees, reference, extract). The terms that
  would name the move, independence, capture, attribution, sighting, overlap, Petersen, are swept for
  separately in `checks.py` and `verify.py` and appear in no shipped document.
- **Sweep 6, five files naming most members beside numbers.** The register, the returns, the two
  notification extracts and the trustees' pack hold member codes beside volumes, case counts and joining
  dates. None states an incidence, an index or a rate, which is asserted: no three-digit graded figure
  appears in the pack's documents and no number in them sits beside a case or index word.

**`guard.py surface`: one named tell, fixed; one pair answered.** The prompt shared the rare construction
"give the shares to one decimal" with task231 and now opens that sentence on a different verb. The
promoted pair task194 against task196 is promoted because both cards carry G12, and `surface` reads that as
a decisive pattern the draw should have caught; the card now carries an explicit `differentiation` entry for
task194 so a reviewer reads the distinction off the card rather than off this note. The two gaps are
opposite kinds: task194's events have happened and the record codes them late, so developing the series'
own two vintages recovers them and every event eventually appears; task196's events never enter any record,
and the decisive step is that most of the overlap between the two capture channels exists only because the
firm's own recall request produced the second channel's rows, which no later vintage would ever reveal. The
driver score agrees:
task194's G12 is a count that crystallises after the period it belongs to, read through two vintages of the
same series; this build's G12 is a count of events that never entered the record at all, recovered from the
overlap of two channels, and the two drivers score 0.06. Re-run on the final pack, `surface` also promoted three pairs on one table
with an identical column set, which was `data_dictionary.csv` carrying the generic header
`file,field,definition` shared with task198. The dictionary is furniture the input gates require rather than
anything that drives the stump, but a shared header is a shared string, so the header now reads
`extract,column,definition` in the mutual's own idiom and the finding is gone: promoted pairs fall from 14
to 11 and the identical-column-set count to zero. The remaining promoted pairs carry no shared string,
no shared persona and no shared mechanism; they are the corpus's ordinary top-percentile surface noise.

**`guard.py heart`: WARN, no BLOCK.** The two WARNs are the Gate G mechanism's overuse across the batch and
the objective's, both answered in `## Draw`. The one BLOCK the batch produced, `ban.artifact` against
task197's `register`, was a wrong key rather than a repeated organ and is re-keyed `planning_thread` in
`## Tried and rejected`; `guard.py check` and `heart` both return WARN at exit 0 on the re-keyed card.

**The dictionary is read back by the verifier.** `data_dictionary.csv` carries the conventions the call
leans on (SF1's cover class, SF8's one case however many legs, SF4's thousands against units) and no
assertion had ever opened it from the shipped bytes, so `verify.py` now reads it through its own csv reader
and asserts those three sentences as its positive control on that same reader, with a non-zero extraction
length and the decisive-step sweep run on the same extracted text. An empty extraction fails the assertion
rather than satisfying it.

**The judge's readings, each closed in the data rather than by a sentence.** The determinism judge
returned NOT_DETERMINISTIC on eight findings and the author held the architecture, because every one of
them closes by fixing data or by making a stated sentence true rather than by filing the estimator or the
attribution. What changed: the request gap now holds every independent registration at least 22 days ahead
of the request that follows it, so the band the judge reclassified is empty and a 1, 2, 3, 5, 7, 14 or
21-day window prints the golden exactly; the pre-payment registrations are a real body of 167 rows whose
share is equal on both sides of the overlap, so dropping them prints 31 (SF13); the independent capture is
assigned at the same rate inside every subset of the member's own cases, so the capture probability read off
the cases it never asked about agrees with the one read off all of them to four decimals and the sixth form
prints 31 (SF12); the overlap itself is up from 120 to 157; the prompt's own second sentence, clause 4.2 and
the trustees' pack now say the same thing about the evidence date; ask 6's route totals cover the same four
quarters as its rows; and ask 4's quarter totals are pinned to the unrounded tier amounts, which changes two
of the four. The two documents and the two register defects the reader found are fixed in the writers.

**`target.zip` is cut by the house cutter**, `generator/archive.py` copied from task192, so every entry
carries a fixed 1980 timestamp and the zip's bytes cannot move between rebuilds.

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
- **A headline printing exactly 30 per million**: the first whole-case design point put the golden on a
  round integer, which `determinism-check` section 3 and the dataset checks both refuse because a round
  graded figure reads as a constructed one. The design point moved to 22.23 million payments, which prints
  31 on a value of 30.94, 0.44 from the bin edge. Nothing was cut when it moved.
- **Asserting one estimator pair rather than the family**: Chapman against plain Petersen caught the
  one-decimal straddle, but a two-source capture estimate has more licensed forms than two. All five that the
  data does not close are now enumerated in SF12 with their values, and the observed union is ruled out by
  clause 4.2's own words rather than left as an unnamed rival.
- **Case references drawn at random**: the first cut allocated each case a random five-digit reference, so
  references collided inside a member and scheme year and the fund-return log merged two cases wherever one
  did. The bundle then reproduced 161 independent sightings against the world's 207 and the index came out
  at 39 rather than 31. References are now drawn without replacement from the member's own block, asserted
  distinct.
- **An independent registration that a fund-return request precedes**: the first cut placed those
  registrations in the days after the case opened without regard to the request, so sixteen of them
  post-dated a request and the shipped-data rule disagreed with the golden. The request dates are now
  settled first and an independent registration lands before the request or before the case, asserted at
  zero violations pack-wide.
- **`hash()` on a member code for an unindexed member's volume**: the string hash is salted per process, so
  two builds differed in nine files. Replaced with the build's own seeded stream, and two consecutive
  builds are now byte-identical.
- **A byte-level substitution over the PDF producer string**: the writing library escapes the parentheses
  inside its own producer value, so a regex over it left an unbalanced dictionary and `pdfplumber` could no
  longer open either document. The substitution now scans with the escape rule and keeps the byte length,
  and the verifier reopening both documents is the control on it.
- **Ask B's second figure as a closure count**: measured on the cut pack, the device moved eleven of
  twenty-four figures, because the quarter's tail carried few closures, so a response reading the main
  extract alone would have kept the other thirteen. Replaced with the value reported, which every missing
  row moves: 24 of 24 figures now move.
- **A prior-period adjustment on three named advices**: measured at three of sixteen figures moved, which
  left thirteen free to any response. The adjustment now falls where the recoveries team closes an earlier
  quarter off, about a third of the unauthorised advices across every month and tier, and all sixteen move.
- **Ask B's forcing figure as first written** (the main extract reads 271,508 against 335,982 on Garnock's
  reported value, a gap of 64,474): the figures were carried over from the cut before the design point moved
  to 22.23 million payments, and re-measuring the device on the shipped bundle gives a different widest cell.
  The device itself is unchanged and still moves 24 of 24 figures; the cell now reads Brindlemere's value,
  405,985 against 460,362, a gap of 54,377, with the narrowest moved figure a single whole case. Asks A and C
  were re-measured in the same pass and their cells were already right (A 16 of 16, widest 256,440 on the Q1
  total; C 15 of 15, widest 7.8 points on Q2 beneficiary recall).
- **`register` as the context-artifact key**: `guard.py heart` returned BLOCK on `ban.artifact` once task197
  registered `register` eight minutes before this card, and the key was wrong anyway. The pack's context
  artifact is the trustees' meeting pack (an agenda, a minutes reference and the membership position at
  31 March 2027, issued by the secretariat on 2 July 2027, proposing no index), which is `planning_thread`;
  `register` described only the membership table printed inside it. The pack's actual registers are not
  context artifacts, since `mule_account_register.csv` is the second capture channel the call reads and
  `member_register.csv` is a lookup. Re-keyed, and heart returns WARN with no BLOCK.
- **A prompt at 994 characters**: six characters of headroom under the 1,000 gate would not survive any
  stage-3 edit. Trimmed to 971 with no figure, unit, deliverable or rounding requirement dropped, by
  shortening five phrases ("one decimal place" to "one decimal", "a title stating the finding" to "titled on
  the finding", two redundant articles, and a semicolon for "and" in the second sentence). The prompt gate
  passes on all twelve checks.
- **The dictionary's generic header** (`file,field,definition`): `guard.py surface` on the final pack
  promoted three pairs on it as a table with an identical column set, shared with task198. It is required
  furniture rather than a driver of the stump, but a shared header is still a shared string, so it was
  re-cut as `extract,column,definition` in the mutual's own idiom. The writer, the one check that reads it
  and the new verifier read-back moved with it; the identical-column-set finding is now zero.
- **Grading the review group's payments-sent counts in block 4**: the Deliverable Answers block stated each
  review-group member's recorded cases, indexed cases and payments sent beside its index. The recorded and
  indexed values are the asked chart's own two series, so they stay, but the payments count is the index's
  denominator and no sentence in the prompt asks for it, which makes it a graded figure with no asking
  sentence to fix its basis or rounding (`determinism-check` section 5). The four payments counts are out of
  block 4. Castlegate's stays in the Final Recommendation and in step 3, where it is the recommendation's
  working rather than an answer the rubric owes, and the deliverable file keeps the column as ungraded
  context. `figures_check.py` falls from 98 figures to 94 and the pair ceiling does not move, because those
  counts were never rubric criteria: C1 is the four indices.
- **"Our data stops at 31 March 2027" in the prompt** (judge finding 1): the extracts run to the 2 July
  pull and the trustees' pack dated the evidence base to 31 March, so the prompt's own sentence was false
  and cutting the register at the year end was a defensible reading worth a different figure. The window is
  one of the five parts of the WHAT, so it is filed rather than argued: the prompt now says the scheme year
  closed 31 March 2027 and the register feed runs to the 2 July pull, the pack says the reviews are prepared
  from the evidence base as pulled for the meeting, and clause 4.2's "as it stands when the review is
  prepared" was already there. Cutting at the year end is computed at 32.522, prints 33 and is barred by the
  clause, asserted both ways.
- **The near-miss cluster one to five days ahead of each request** (judge finding 2): the first cut put 45
  per cent of a requested case's independent registration in the days between the case opening and the
  request going out, which made "treat a registration up to two days before the request as request-linked" a
  defensible reading. The cluster is gone from the generator rather than ruled out by a sentence: an
  independent registration either follows no request at all or precedes one by at least 22 days, measured at
  a minimum lead of exactly 22 and an empty one-to-five-day band, and the seven window readings from 1 to 21
  days now print the golden exactly.
- **Removing the pre-payment registrations** (judge finding 3): the honest reading is that they count, since
  the register is a standing industry list and an account stays on it, so they were kept and made
  unambiguous instead. The feed note states the persistence fact, and the share that predates its payment is
  held equal on both sides of the overlap (0.618 against 0.619) so that dropping all 167 of them divides a
  smaller numerator by a proportionally smaller overlap and prints the same 31. Removing them was rejected
  because it would have forced the independent capture to correlate with the report lag, which breaks the
  capture-rate agreement the sixth estimator form turns on.
- **Closing the sixth estimator form by widening the overlap alone** (judge finding 4): the overlap was
  widened, 120 to 157, but the measured cause of the crossing was that the capture probability read off the own
  cases the member never asked about (34 of 109 on the judged pack) differed from the one read off all 400
  by sampling noise, and volume alone only shrinks that. The capture is now assigned at the same rate inside every subset an
  analyst can cut, so the three readings, now on 158, 242 and all 400 own cases, agree to four decimal places by construction and all eight licensed
  forms print 31 with a span of 0.29 per cent. **Widening the overlap further was rejected on measurement:**
  the ladder's spread comes from the overlap being small against the channel, and at an overlap of 180 rung 2
  fell to 32.5, inside 5 per cent of the golden and in the neighbouring printed bin. The request share was
  cut from 0.72 to 0.60 in the same pass to hold rung 2 out at 35.669.
- **Ask 6's route total over every closed case** (judge finding 5): the total was taken over all 2025/26
  cases with a closed date while the rows were taken over the four quarters, so 921 cases closed after
  31 March 2026 sat in the total and in no row and the two could not be reconciled. The total now covers the
  same four quarters as the rows, the asking sentence pins the population, the credit basis and what the
  total covers, and the reconciliation is asserted from the quarters' own numerators and denominators.
- **Ask 4's unstated rounding order** (judge finding 6): the rounded tier figures did not sum to the rounded
  quarter total on two of the four quarters. The asking sentence now pins the total to the unrounded tier
  amounts, and the pin is load bearing rather than decorative: Q1 reads 664,379 on that basis against 664,378
  on the other, and Q3 614,872 against 614,873, both asserted.
- **The trustees' pack's February 2027 register feed change** (judge finding 7): nothing in the pack
  described it and the judge found no discontinuity in volumes, in the request-induced share or in the lags
  by month, so the sentence was a stated fact the data contradicted. Taken out. The feed note keeps the
  zero-padding convention, which is a legitimate antidote, and loses the sentence explaining what a blank
  case reference means, which was the ask device's own mechanics.
- **Wrenhall Pay at tier A on a volume that does not support it, and one report reason for the whole
  register** (judge finding 8, from the reader): the tier now states that it is held from the 2024 review,
  which is what a triennial cycle does and what the register's own review field already implied, and the
  member rows of the mule register draw their report reason the way the industry rows always did, so the
  column carries three reasons rather than one.
- **The unexplained residual inside the settlement advice totals** (re-judge finding 1): 49 of 144
  unauthorised-fraud advices carried a total above the sum of their own detail lines, at ratios of 1.15 to
  8.40 and 815,234.74 across the year, while `case_lines` equalled the detail row count on all 288 advices,
  so the detail said it was complete and the total said otherwise and nothing in the pack explained the
  difference. That is a generator bug in the costume of messiness, not authentic mess. The prior-period
  adjustment is now one of the advice's own detail lines carrying the month it settles in, so **every one of
  the 288 advices ties to the sum of its lines and every `case_lines` matches its row count**, asserted.
  Measured on both bases afterwards: the advice-total reading and the own-month reading still differ, by
  640,285.12 across the year, but every pound of that is now the quarter a line belongs to rather than an
  unexplained residual, so the asking sentence pins the grain the way ask 3 pins its population (SF14). The
  prompt clause was not reached for first, and it is only there because the bases still differ.
- **The walk in whole cases** (re-judge finding 2): the index survives every licensed form, 30.842 to
  30.974 against a bin edge at 30.500, but the whole-case walk did not, running 686 to 689 indexed and 286
  to 289 not held, so three of the eight forms printed a different walk. Restated in index units, where it
  is **18, 13 and 31 under all eight forms** (one distinct walk, asserted, against three distinct whole-case
  walks), and the two lines add to the index. The asking sentence changed with it, which is what makes this
  pass a rerun.
- **Saltmarch Pay's index 0.091 from its printed bin edge** (not a judge finding; the author raised it from
  the judge's own margins table): the member volume was derived from the design's own counts while the index
  is read off the counts as built, so the printed index drifted by the rounding between them. The review
  group's volumes now come from the realised estimate, and **every review-group index is mid-bin: 0.440,
  0.390, 0.380 and 0.430** against the 0.30 floor, with Castlegate's two walk lines at 0.491 and 0.449.
  The distance is asserted per member rather than for the named member alone.
- **The feed note's standing-list sentence** (second leak read): added in the previous pass to make the
  pre-payment registrations unambiguous, and deleted here. The reader landed the call exactly and quoted it
  as the clearest hint aimed at the analyst. The deletion test settles it: dropping every pre-payment
  registration prints 31 by convergence with the sentence gone, so the sentence closed nothing and only
  pointed at the method. The export manifest's `what_it_omits` commentary went with it, for the same reason.
- **"Not a rule on the registration date" beside a step that was one** (re-judge, small): the Final
  Recommendation rejected a registration-date rule while step 5 described the decisive step as a comparison
  of the registration date against the request date. The step now says what it does, which is attributing
  each match to a cause through the request log; no figure moves.
- **The writing library's epoch date in both PDFs** (re-judge, small): `/CreationDate` and `/ModDate` read
  `D:20000101000000` against a 2027 fiction. The scrub now substitutes the pull date at the same byte
  length, so the rebuild stays identical, and the verifier reopening both documents is the control on it.
- **`causal_design` as the strategy label**: the honest key for capture interference, taken by task197 five
  minutes before this card filed, so the card carries `other` with the mechanism named in its notes rather
  than a negotiated axis.
- **Ask 4's basis read off a field name rather than an event** (re-judge pass 3, findings C and E, repaired
  here): the clause said "each line in the quarter it settles in" while the workbook carries a settlement
  month at two grains, so the phrase had two licensed readings and all sixteen figures differed between them
  by up to 320,142.56, with 486,513.00 of indemnity moving between quarters. Rejected as unrepairable by
  argument: the enumeration above shows seven plausible period bases, and a sentence that names a field the
  pack holds twice can never admit one of them. The sentence now names the event, the quarter the case closed
  in, which the register dates once. Gate C and Gate E are answered by the enumeration rather than by a
  preference between the two tables.
- **Pinning the basis on the line's own settlement month, the committed reading stated plainly**: it closes
  the fork and kills the ask. The clause would name the detail sheet's own column, so the natural read
  becomes a group-by of that column and the device goes free; on Part 0's weights that is a pair of 43.9 with
  the response that lands the call keeping it and 50.3 with both responses keeping it, against a gate of 40.
  Rejected for that measurement.
- **Pinning the basis on the advice that pays the line, which the judge called the better-grounded reading**:
  rejected for the same arithmetic and worse. The advice-grain rollup is the natural read itself, so the ask
  becomes a 288-row group-by, every figure goes free, and all sixteen committed figures change. Deleting the
  ask instead was also computed and also fails, at 52 criteria and a pair of 40.1, so the ask has to keep a
  device and the basis has to sit where the workbook cannot answer it.
- **Changing the 35 rows** (the alternative this repair was asked to price): rejected on the measurement. The
  line's own month is the month its case closed in the register on 6,416 of 6,416 detail lines, 0 disagreeing,
  so the rows support a single forced reading and the field corroborates the pinned basis instead of
  competing with it. Changing them would have moved sixteen graded figures to repair one sentence;
  `target.zip` is byte-identical to the pack the judge read, md5 58fea759d25de0f25cd583ff70449695 over 19
  members.
- **A silent primary rebuilt inside the advices workbook, to replace the one the pin was feared to spend**:
  drafted and held, not built. A partial detail sheet completed from the register repeats ask B's primary
  (a silently partial extract found against a control); a withdrawn-and-reissued advice breaks clause 5.1's
  one advice per cover per month, which the battery's key-uniqueness sweep reads as a work order; a tier
  carried at the wrong vintage moves only the twelve tier cells and leaves the four quarter totals free,
  because a quarter total is invariant to the tier split. None was needed: the pinned basis leaves the rollup
  live at 16 of 16 figures, measured, and the residual exposure (a response that joins the register's closure
  dates lands the ask) is written into the ask sheet rather than argued away.
- **Freeze mode for this repair**: both run and both recorded. `--mode determinism` PASS at exit 0, which is
  the stronger of the two here because this repair moves no graded figure at all; `--mode rubric` PASS at
  exit 0 with its own WARN, "nothing on the ask side moved", which is the correct reading of a repair that
  changed an asking sentence's basis and grain while every figure it governs stayed where it was. The
  snapshot was taken before the first edit, and was neither retaken nor suppressed.
