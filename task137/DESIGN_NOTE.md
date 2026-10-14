# task137: Kaimai Building Society, the agent-hours to book with Harbourline for the January to March 2027 term deposit maturity calls (architecture 1, round 2)

Private, never ships. A wave 2 build numbered from seed FC08: the seed's world, decision and quantity are kept (a
deposit-taker's maturity calls made by an outsourced contact centre booked in agent-hours, take-or-pay, a quarter ahead,
on a list fixed at the booking deadline); its architecture (dialling rules withheld from the contract and recovered from
the vendor's acknowledgements) is not used. Round 2 (2026-10-14) answers the 10/10 audit (COMPLIANT_WEAK): round 1's
decisive step, the share conditioned on each deposit's repricing drop, was the strong model's reflex and the field's
textbook model, a locked-rate-by-term logit landed the golden bin without reading a card, the locked-rate rung sat one
bin under, Ask B's migration file announced its overlap, Ask A's clause signalled its device and the swap test passed
only narrowly. The decisive step moves to a choice a solver who already conditions on the drop still gets wrong: the
class of the money (what a new-money special won, against member money that rolls on the posted card), a reason only
deposit repricing behaviour has. The rate path, the specials and both asks are re-cut; the prompt's ask wording changes.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task137.json`, architecture v1, registered 2026-10-12, round 2 fields edited in place 2026-10-14 (the round-1 driver kept in `lineage`); `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | banking-credit-financial-risk / deposit-liquidity-behaviour (a client domain): how term deposit holders behave at maturity, by the stability class of their money and the repricing gap, is the deciding quantity |
| Objective | Forecasting & Predictive Modeling: the agent-hours the January to March 2027 list will use, a campaign not yet begun, forecast from the seven closed campaigns |
| Shape | other: the call and its components (the hours, the hours for each maturity month), the note's opening and chart, and two asks on rows the call never reads (14 and 4 figures); about 28 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (agent-hours, to the nearest 250) |
| Mechanism | gap time (a lapsing term: a special's premium lapses at the deposit's first maturity, and the coming list is the first maturity of a cohort the past never matured at its drop), then population; pattern E (a conditioned yield, no column naming the conditioning property); generators G14 (the share of conversations that go to the retention offer, conditioned on the class of money) then G6 (the coming list is 58 per cent special money at a drop the past met almost only with member money); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `field_method` (deposit liquidity behaviour's stability segmentation: rate-driven money a special won against member money); `own:special-money-runoff-at-first-maturity` (banking has no library patterns) |
| Furniture | forum `committee_or_panel` (the Deposits Committee approves the block, procedure 6.2), forcing event `purchase_order_or_contract` (the take-or-pay block order is due Friday 20 November 2026), organisation family `cooperative_or_member_body`, role family `product_manager`, context artifact `planning_thread` (Harbourline's request for the block order and the society's reply), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `harbourline_dial_log_2025q1-2026q3.csv`, the contact centre's dial records: one row per dial on a released case, December 2024 to September 2026 (269,175 rows); constructed |
| Deliverables | `td_booking_q1_2027.xlsx` (the booking by maturity month with its basis, the two asks, a notes sheet), `td_booking_note_q1_2027.docx` (a one-page note opening with the block and charting it by maturity month) |
| People | drawn at round 1 with `guard.py names --geo "New Zealand" --seed 137 --n 30`: Hazel Johnstone (term deposits product manager), Stuart Waller (head of deposits, chairs the Deposits Committee), Suzanne Wallis (Harbourline account manager), Joseph Herd (customer data steward), Sienna Stewart (treasury pricing analyst), Ashton Findlay (Harbourline workforce planner); none appears in the prompt |

**Guard.** `guard.py check` on the round-2 card: WARN, one finding. `repeat.gate_g` (`forecasting` in one of the last
two builds, task130): the key is honest, because the decisive step is how the forward share of long conversations is
forecast, per class of money, and task130's mechanism (a claims-made window costed by report lag) shares nothing with
it. A first round-2 card with the gap reordered to population first blocked on `test.same_driver` (population, E,
forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
order for a lapsing premium (Tried and rejected). The bans run against the builds before the slot's registration, as
at round 1.

**Same-puzzle and same-driver tests.** Gap time, pattern E, decision `quantity_figure`, Gate G `forecasting`: no build
in the last twelve carries the four. The older carriers (task117, task37, task44, task97) and task138 are differentiated
on the card in the round-2 terms.

**Abstraction test.** Stripped of nouns, the driver is: a behavioural share at a one-off repricing is a mixture of two
kinds of unit, those a temporary price premium brought in, which take the costly path at their first repricing whatever
the price change, and long-standing units, which take it in proportion to the change; conditioned on the price change
alone, the share is read off a past in which the forward pool's change was met almost only by long-standing units. The
nearest drivers on file: round 1 of this slot (0.14, the price change alone, now lineage, differentiated), task35's
lineage (0.08, a filed floor on per-order value), task84 (0.05, a composite key). By structure, the F5 composition
builds: task95 (a yield split by a stand's age at first thinning, a class recovered by differencing two dated events,
the blended rate the default) and task20 (a unit's fence against its lead time, two units moving class at renewal).
Here the default is not a blended rate but the field's own covariate model, which already conditions on the price
change; the class is how the unit's money was won, rebuilt from its price against its entry cohort's floor; no unit
moves class; and the two classes respond to the price change in different shapes (flat against rising). Both are
differentiated on the card.

**Data-native sentence.** Kaimai funded itself through the rate cycle with new-money specials (one rate for every
amount, half a point or more above the posted card), so every campaign list mixes member money that has rolled on the
card with money a special won from other deposit-takers; at its first maturity the special's money went to the
retention offer at nearly nine conversations in ten whatever its drop, member money in proportion to its drop; January
to March 2027 is 58 per cent the 2023 four-year special's money meeting a 1.65-point drop as the card turns up, a drop at
which past conversations, almost all about member money, went to the offer about a third of the time.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: composition builds task95 (a class by
age at first thinning) and task20 (a fence against lead time), the hazard builds (134), selection on the outcome (124),
a claims window (130), a recycling term (501), a campaign yield per untapped member (136), a replay from a rebuilt state
(138): none conditions a behavioural share on how the unit's money was won. `stumping/references/strategies.md` F5: the
family is legal when the split is absolute, confounders are controlled by construction and the property is rebuilt from
a history, never read off a column; the property here is new to the family. `stumping/references/client/
two-layer-task-design.md`: banking has no library patterns, so the pitfall comes from `field_method`, here the
stability segmentation every deposit liquidity model makes (rate-driven against stable money). The audit's measured
routes for round 1 (the round-2 brief): the locked-rate-by-term logit, the additive logit and per-term linear fits, now
rivals in `checks.py`. The seed's header (FC08) for the world only.

**World.** Kaimai Building Society is a mutual deposit-taker headquartered in Tauranga, most of its funding on term
deposit (one- to five-year terms). At maturity a term deposit reinvests for the same term at the posted rate in force on
its maturity date unless the holder has given other instructions (the Term Deposit Terms, clause 9.2, cited in procedure
5.1). ALCO sets the posted card each quarter. Through the cycle the society raised money with new-money specials, one
rate for every amount and no other offer: the four-year special at 5.65 per cent in January to March 2023, the
three-year at 6.00 in July to September 2023, the two-year at 6.30 in October to December 2023, the one-year at 6.35 in
April to June 2024 and 5.45 in October to December 2024, and one-year specials at 5.10, 4.75 and 4.45 in the first three
quarters of 2025; no shipped file names a special, which shows only as a block of deposits at one rate above their
cohort's posted rate. The cards fell through 2025, the curve steepened through 2026 as the market priced a turn, and the
January to March 2027 card runs from 3.20 per cent for one year to 4.20 for five (4.00 for four years). Since January
2025 Harbourline Contact Services, a Palmerston North contact centre, has made the society's maturity calls under a
statement of work (HCS-KBS-2025-01): each quarter the society lists the term deposits of NZ$25,000 or more maturing in
it with no maturity instruction on file at the list cut, releases each to Harbourline 21 days before its maturity date
unless the holder has instructed in the meantime, and Harbourline works the case under the SOW's dialling rules until a
conversation, exhaustion of every callable number, withdrawal or maturity. Harbourline bills agent time at fixed minutes
per event (1.5 for each dial that does not reach the holder, 8 for each conversation, 22 for each conversation that goes
to the retention offer) against a quarterly take-or-pay block the society books, in multiples of 250 hours, by the 20th
of the second month before the quarter; hours beyond the block are billed at the block rate plus 35 per cent. The
retention procedure (version 4) books the hours the quarter's list is forecast to need, to the nearest 250, drawing on
every campaign closed under the SOW, and the Deposits Committee approves the block before it is sent.

As-of dates: the January to March 2027 list was cut on 2 November 2026 (18,400 term deposits, 10,697 of them the 2023
four-year special's deposits at 5.65 per cent); ALCO approved the January to March 2027 card (four years 4.00 per cent)
and it sits in the draft campaign brief issued 3 November 2026; Harbourline's last close-out (July to September 2026)
arrived on 21 October 2026; the request is made on 4 November 2026; the block order is due on Friday 20 November 2026.

## Default path

1. Read the SOW (the minutes billed per event, the dialling rules, the take-or-pay block in multiples of 250) and the
   retention procedure (the list, the release 21 days before maturity unless the holder has instructed, no release
   without a callable number, the booking of the hours the list is forecast to need from every closed campaign).
2. Take the 18,400 deposits on the January to March 2027 list, normalise their holders' phone numbers and wash them
   against the do-not-call register: each case's callable numbers by type, and the 464 cases left with none.
3. From the seven closed campaigns (the release log, the dial log and the close-outs), price dialling per mix of
   callable number types: the dials that do not reach the holder and the chance of a conversation per released case,
   and the 95.2 per cent of listed deposits with a callable number that reach release.
4. Condition the past share of conversations that went to the retention offer on each deposit's drop from its locked
   rate to the card for its term on its maturity date (the field's repricing-gap model: 0.25-point bands of drop, or a
   logistic in the drop, with or without term), and read the list's drops against the January to March 2027 card in the
   draft brief; or carry the share pooled, from the latest campaign, by term, trended, by locked rate or by whether
   the deposit sat on an earlier list.
5. Price each expected conversation at 8 minutes plus 14 times its share, sum over the list and round to the nearest
   250.

Ends on: 4,250 agent-hours (4,267.1 with the share by 0.25-point band of drop; 4,284.7 with a logistic in the drop;
4,213.9 with the pooled share; 4,278.7 by locked rate; 4,686.4 with the drop and term in one logistic, booked 4,750;
4,472.1 with a logistic of the locked rate by term, booked 4,500; 3,821.7 by term, booked 3,750).
Golden: 5,250 agent-hours (5,280.9; 1,250, 2,000 and 2,000 by maturity month: the share conditioned on the class of
the money and its drop).

## Stump sentence

A competent solver washes the numbers, prices dialling per mix of callable numbers from the seven closed campaigns,
conditions the past share of conversations that went to the retention offer on each deposit's drop from its locked rate
to the card it reinvests at and books 4,250 agent-hours; the step that lands it there is reading that share
off every past conversation at the drop instead of off the conversations about the same class of money: 10,697 of the
18,400 deposits are money the 2023 four-year special won at 5.65 per cent, and money a special won went to the offer at
87 per cent at its first maturity whatever its drop, where past conversations at the special's 1.65-point drop, almost
all about member money, went to the offer about a third of the time: the golden is 5,250.

## Three rules

- **Task type:** Banking, Credit & Financial Risk, deposit-liquidity-behaviour (serves Forecasting): the agent-hours the
  January to March 2027 maturity list will use, forecast from how each class of money behaved at the seven closed
  campaigns' maturities.
- **Domain test:** the deciding quantity is the share of reached holders whose maturity conversation goes to the
  retention offer, which deposit liquidity behaviour forecasts by the stability class of the money (rate-driven money a
  new-money special won against member money that rolls on the posted card) as well as by the repricing gap at maturity;
  the field's own segmentation decides the call.
- **Swap:** "book renewal-call hours for 18,400 insurance policies, the retention desk's share set by the premium
  change" keeps a price-shock model but loses what decides here: a deposit's drop is the market's, since every
  deposit-taker's card falls and rises with the cash rate, so it sends member money almost nowhere, and what leaves at
  first maturity whatever the drop is money that moved banks for a special's premium over a posted card; a cash-rate
  cycle, a posted card by term and new-money specials have no renewal-desk equivalent.
- **Layer 1:** realistic mess across the pack, none of it deciding the call (asserted, R2): past lists in two
  core-banking layouts (per cent and decimal rates, dashed and plain account numbers, comma-grouped principal), the dial
  log in UTC with vendor codes, release files listing callable numbers by type, mixed-format phone numbers against a
  dated do-not-call register, posted cards in quarterly PDF briefs whose layout changes in 2026; on the ask paths,
  maturity proceeds paid through the society's maturity settlement account with the matured deposit named only in the
  payments narrative, a holdings view repeating joint accounts, a frozen certificate register beside a migration log
  that misses the certificates moved by hand, and certificate principal carrying interest capitalised at migration.
- **Layer 2:** `field_method`, estimation under a mix shift in the field's own segmentation: the share of
  conversations that go to the retention offer is a mixture of two classes of money with different behaviour at first
  maturity, and the coming list's mix (58 per cent special money) sits far from the past mix at its drop (under 15 per
  cent), so the share is carried per class and per band of drop, not off every conversation at the drop, pooled, by
  term, by campaign, by locked rate or by a model fitted on the list's own columns.
- **Decisive step:** classing each deposit by the money it holds (a rate 0.40 points or more above the lowest rate of
  the same list's deposits of its term opened in the same quarter: money a special won) and reading each class's own
  share at its drop, which puts the 10,697 deposits of the 2023 four-year special at the 88 per cent past special money
  met at the same drop, not the third of all past conversations there.
- **Not semantics:** no field, code or definition flips the call: the rates, terms, opening dates, disposition codes and
  minute rates read the same on every route; the class is a construction across each list's cohorts that no column,
  code or document names (the product column says Term Deposit or TD for every deposit), and the drop is the same
  covariate on the default path and the golden.
- **Not rule application:** procedure 6.1 says only that the booking is the forecast need drawn from every closed
  campaign, to the nearest 250; no filed sentence names a special, a class of money, a rollover rate or any link between
  how a deposit was won and the retention offer, so executing every filed rule (SOW minutes, dialling rules, release,
  wash, reinvestment default, rounding) still leaves the share's conditioning open.
- **Analyst test:** washing every number, pricing dialling per callable mix with the release share and conditioning
  the retention share on the repricing drop books 4,250 (4,267.1), as do the pooled share (4,213.9), the latest
  campaign's and the share by locked rate; a logistic in the drop and term books 4,750 (4,686.4), the audit's
  locked-rate-by-term logit 4,500 (4,472.1), the share by term 3,750, a trend 4,500 and the share split by whether the deposit sat on an earlier list 4,250
  (4,278.7), every route at least two bins
  under the golden 5,250 (5,280.9), asserted on the generator's clean truth (R3a).
- **Estimand:** the agent-hours the SOW bills (1.5 minutes per non-reaching dial, 8 per conversation, 22 per
  retention-offer conversation) that the 18,400 deposits on the list cut on 2 November 2026 will use, by maturity month,
  to the nearest 250, drawn from every closed campaign (procedure 6.1, SOW schedules 2 and 2.2, the prompt).
- **No decoy:** no memo, draft, past booking, forecast, share by class or share by drop ships, and no document mentions a
  special (asserted, R1); the treasury outlook's flat rollover on balances and Harbourline's staffing proposal are
  declared distractors that argue no hours; the close-outs report what each campaign did and tie under every basis.
- **No certified replay:** the method is not recovered from certified figures: no published share or booking exists to
  reproduce; the class is rebuilt from the lists' own rates and opening dates, and the seven campaigns' outcomes separate
  the bases (special money at 80 per cent or more in every campaign, term and drop it met; member money rising with the
  drop in every campaign; the two classes 30 points or more apart in every shared band).
- **Lesson:** a deposit book carries two kinds of money, and the money a special won leaves at its first maturity
  whatever its drop because it came for the premium, while member money leaves in proportion to the drop; a list whose
  largest cohort is a special's money needs about a quarter more agent time than the share by drop books, and no
  build on file conditions a behavioural share on how the unit's money was won.
- **Stump class:** analytical. The decisive step is what the forward share is conditioned on, the class of money beside
  the drop; no plant, no field read and no filed rule decides, and every rule in the pack is executed the same way on
  the default path and the golden.

## Readability screen

Rungs as climbed (Ladder). The six tests: 1 a filed sentence names the decisive quantity or sends the solver looking;
2 a column, key or marker makes it a predicate or a header-found join; 3 an opponent reflex; 4 a control or corpus
scores the bases or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a
reported figure.

| Rung (the step that refuses the rung below) | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1: price dialling per mix of callable numbers from the release log and dial log, with the release share (refuses rung 0's hours per listed deposit of the latest campaign) | the SOW's dialling rules name callable numbers and the six-dial limit | the release log lists each case's callable numbers and types | stratifying by a visible attribute is a reflex | none | no | a group-by and a weighted sum | readable |
| R2: the share conditioned on each deposit's drop from its locked rate to the card for its term on its maturity date, or carried pooled, by term, by campaign, trended, by locked rate, by first listing or by a model fitted on the list's columns (refuses the pooled share) | no | the locked rate is on each list and the card in each brief | the field's repricing-gap model is the strong solver's reflex (the round-1 audit and judge found it unprompted) | none | no | a join and a group-by | readable |
| R3 (decisive): the share conditioned on the class of the money (a rate 0.40 or more above the lowest rate of its term and opening quarter on its list: money a special won) beside the drop, the coming list's 10,697 special deposits read off past special money at their drop | no sentence names a special, a class of money, a rollover rate or any link between how a deposit was won and the retention offer (asserted: no document carries the word special) | no column holds the class: the product column reads Term Deposit or TD on every row, and the class needs the lowest rate of each term and opening quarter across a whole list | not an opponent default: its reflexes condition on the drop, term, locked rate, campaign, trend, principal, first listing or a fitted model on the list's columns, and each lands 11 to 30 per cent short; tree models on the same columns (scratch) 21 to 24 per cent short | no control scores the bases: no published share by class or drop, the treasury outlook's rollover is flat and on balances, and the close-outs tie under every basis | the battery never touches it | a mixture split by a class built across rows, then a per-class conditioned share, not one ratio | silent |

The screen holds on R3 because the only sentences about rates are what a deposit reinvests at (procedure 5.1, read the
same on every path) and the retention offer's limits, the lists carry no product code for a special, and the drop, the
covariate a strong solver reaches for, already looks like the field's whole model: within its band the class is a
second axis the drop reflex never splits.

## Semantic fork table

One row per term in the main ask and per convention the main computation needs, then the asks' readings. The stump
(what the share is conditioned on) is not a reading and has no row: every route computes the same literal estimand, the
hours the list will use under the SOW, and only the data's structure separates them (Literal reader). Every row is
asserted in `generator/checks.py`.

| SF | Term or convention | Golden reading | Alternative and the call under it | Ruled out by |
|---|---|---|---|---|
| SF1 | agent-hours | the minutes the SOW bills per event, over 60 | logged agent time on shift | SOW schedule 2.1 (agent time is billed per event at the stated minutes); no shift or roster data ships |
| SF2 | book | the hours the quarter's list is forecast to need (the expected hours), to the nearest 250 | a smaller block that minimises expected cost under take-or-pay with the 35 per cent overage | procedure 6.1 (the society books the hours the list is forecast to need, rounded to the nearest 250 hours); SOW 2.2 (multiples of 250) |
| SF3 | the 18,400 deposits on the list | each listed deposit a case, one per holder | a holder's other deposits as extra cases | procedure 3.3; asserted that no holder has two listed deposits |
| SF4 | deposits maturing in each of the three months | the calendar month of the contractual maturity date | the month in which the dialling falls | the prompt's own words; every deposit's hours go to its maturity month |
| SF5 | callable number | a number held at the cut and not on the do-not-call register at the cut | a number registered after the cut | both extracts are dated the cut and no register entry, withdrawal or contact point is dated after it (C1, asserted) |
| SF6 | the rate a deposit reinvests at | the card for its term in force on its maturity date, as the quarter's campaign brief carries it | the card in force at release | procedure 5.1 and the brief's section 3; every listed deposit matures in January to March 2027, so one card applies (C1, asserted) |
| SF7 | which closed campaigns | all seven | the latest four, 2025 only or 2026 only | procedure 6.1; each subset files the same bins anyway (C3, asserted) |
| SF8 | the share's estimator | the share of past conversations of the same class in the same 0.25-point band of drop | bands of 0.2, 0.25 or 0.5 points at any offset by class, a logistic or isotonic fit within each class, special money pooled, one logistic in the drop and the class with or without their product | C3, asserted: every member files the same booking and months; a linear probability fit is refused (it falls below zero at the past's negative drops, where thousands of member conversations ran at 0.1 per cent) |
| SF9 | dialling estimator | per mix of callable number types | per ordered configuration, per count only, or a per-number fit of the dialling rules with withdrawals | C3, asserted |
| SF10 | a deposit with no callable number | not released, no hours | released and closed at once | procedure 4.3; the same zero |
| SF11 | deposits instructed before release | the past share of listed deposits with a callable number kept from release by the holder's instruction | every deposit with a callable number released | procedure 4.2; the release log's reasons; released without it, the hours land a bin high (asserted) |
| SF12 | withdrawals and maturity in the dialling window | inside the per-mix yields (past cases closed by withdrawal) | modelled apart | the per-number model with a withdrawal rate files the same bins (C3, asserted) |
| SF13 | rounding | the unrounded total once to the nearest 250; each month from its own unrounded hours | months rounded and summed | the prompt and procedure 6.1; the rounded months add to the rounded booking, and every graded figure sits at least 40 hours from an edge (asserted) |
| SF14 | the retention conversation | dispositions RTK and RTW, billed at 22 minutes | any conversation that mentions rates | SOW schedules 3 and 2 |
| SF15 | a dial that does not reach the holder | NOA, BSY, VML, DIS and WNG, at 1.5 minutes | wrong party as a conversation | SOW schedules 2 and 3 |
| SF16 | the dialling calendar | no listed deposit has fewer dialling days between release and maturity than the six dials per number need | maturity truncating dials | C1, asserted over every maturity date |
| SF17 | a deposit's term | the list's term | term from the start and maturity dates | the same on every row (C1, asserted) |
| SF18 | Ask A: a deposit that moved part of its principal into a new term deposit and paid the rest out | counted, at the part on term deposit 30 days after maturity | counted only when kept whole (every count and amount low); at its whole principal (every amount 3.2 to 3.7 per cent high); at the new deposit's whole principal, new money included (every amount 0.9 to 1.1 per cent high) | the prompt's wording: how much of the principal on its list was still on term deposit, and from how many of its deposits; executed on the extracts it files the golden (asserted) |
| SF19 | Ask A: principal switched into an investment certificate | not on term deposit | counted as kept | same answer: no listed deposit's principal reaches a certificate (C1, asserted) |
| SF20 | Ask A: principal paid into the holder's other term deposit | on term deposit with us, so counted | only a term deposit opened that day counts | same answer: every payment of a listed deposit's principal into a term deposit goes to one opened that day (C1, asserted) |
| SF21 | Ask A: the unit counted | per deposit, the list's grain | per holder; or a deposit counted kept when its holder opened any term deposit within 30 days | same answer per holder (C1, asserted); a holder's other new deposit is new money, not the deposit's principal (the wording), and that reading puts every count 30 to 56 high (asserted) |
| SF22 | the class of money (a convention of the golden's construction) | a rate 0.40 points or more above the lowest rate of the same list's deposits of its term opened in the same quarter | any gap from 0.30 to 0.45; the posted rate of the opening quarter where a brief carries it; the cohort's mode or mean as the base | C1, asserted: no premium sits between 0.25 and 0.50, so every gap from 0.30 to 0.45 classes the same deposits on every list, and each cohort's lowest rate equals its brief's posted rate wherever a brief covers the opening quarter; the mode is refused because the four-year cohort of January to March 2023 is mostly the special, so its mode classes the special as member money |
| SF23 | Ask B: a certificate both on the platform's register and in the core | counted once, at the core's principal | at the register's principal (every month 120,000 to 165,000 dollars low); in both (high) | the register is the platform's at 30 June 2026 and the holdings view the core's at the cut (extract notes); every core certificate matches exactly one register certificate on issue date, maturity date, rate and term, and for every logged migration that match is the logged certificate (asserted) |
| SF24 | Ask B: the quarter's total not on the list | the quarter's maturing principal less the list's principal | the principal of the accounts the list does not carry | same answer: every listed deposit sits in the holdings view at the same principal and maturity (C1, asserted) |
| SF25 | Ask B: a joint deposit | its principal once | once per holder | a deposit's principal matures once; the holdings view repeats an account's whole principal under each holder (asserted: every repeated account carries one principal) |

SF18 to SF21 are Ask A's readings, SF23 to SF25 Ask B's; SF22 is the class's construction, closed by convergence.

## Ladder

Measured on the built pack (`generator/checks.py` asserts every rung and rival at least 8 per cent under the golden,
at least two bins under its booking and off every graded month).

| Rung | Construction | Hours | Off the golden | Booked |
|---|---|---|---|---|
| R0 | the latest campaign's billed minutes per listed deposit times 18,400 | 4,239.7 | minus 20 per cent | 4,250 |
| R1 | dialling per mix of callable numbers and the release share, the pooled retention share (21 per cent) | 4,213.9 | minus 20 per cent | 4,250 (months 1,000, 1,500, 1,750) |
| R2a | R1 with the share by 0.25-point band of drop (the repricing-gap reflex; the special's band ran at about a third) | 4,267.1 | minus 19 per cent | 4,250 (months 1,000, 1,500, 1,750) |
| R2a' | R1 with a logistic in the drop; with the drop and term; by drop band within term; isotonic in the drop | 4,284.7; 4,686.4; 4,260.9; 4,250.0 | minus 19; minus 11; minus 19; minus 20 per cent | 4,250; 4,750; 4,250; 4,250 |
| R2b | R1 with the share by locked rate (0.25-point bands); within term; a logistic of the locked rate by term (the audit's route); term plus locked rate; per-term linear | 4,278.7; 3,731.0; 4,472.1; 3,839.4; 3,693.6 | minus 19; minus 29; minus 15; minus 27; minus 30 per cent | 4,250; 3,750; 4,500; 3,750; 3,750 |
| R2c | R1 with each term's share; the latest campaign's; each term's from the latest campaign; the campaigns' trend; each term's trend | 3,821.7; 4,247.0; 3,879.6; 4,416.5; 3,912.3 | minus 28; minus 20; minus 27; minus 16; minus 26 per cent | 3,750; 4,250; 4,000; 4,500; 4,000 |
| R2d | R1 with the drop and the locked rate, the drop and the principal, the drop and the rate against its cohort's mean (logistics) | 4,225.9; 4,288.7; 4,267.8 | minus 20; minus 19; minus 19 per cent | 4,250 |
| R2e | R1 with the share by band of drop for deposits on their first list against those listed before; a logistic in the drop by first listing | 4,278.7; 4,288.4 | minus 19; minus 19 per cent | 4,250 |
| R3 (golden) | R1 with the share conditioned on the class of money and the drop | 5,280.9 (months 1,206.9, 2,013.3, 2,060.7) | | 5,250 (months 1,250, 2,000, 2,000) |

- **Rung 0 (default):** the latest campaign's hours per listed deposit. Dies to the release log: the coming list's
  holders carry another mix of callable numbers and its deposits another mix of money.
- **Rung 1 (the obvious correction):** dialling priced per mix with the release share, the pooled share. Dies to the
  seven campaigns: their shares run from 9 to 27 per cent, and the list's deposits meet drops and cards no campaign's mix
  carried.
- **Rung 2 (the sophisticated wrong ones):** the share conditioned on the repricing drop (the field's textbook model,
  which the round-1 audit measured as the strong solver's reflex), or by term, locked rate, campaign, trend or a fitted
  model on the list's columns. Each dies to the class: within every band of drop, past conversations about money a
  special won went to the offer 30 points or more above the rest, in every campaign and term where specials matured, and
  the coming list is mostly special money at a drop the past met almost only with member money.
- **Rung 3 (decisive):** the share per class and band of drop: the 10,697 special deposits at their 1.65-point drop take
  the 88 per cent past special money met in the same band; member money keeps its own share at its own drop.
- **Margins and flip:** the nearest wrong rung (the drop and term in one logistic) sits 11.3 per cent under the golden
  and two bins below; every other rival 15 to 30 per cent. The booking and its three months fall a bin only if the
  special deposits' share at their drop were under 0.80 (against 0.88), and every past special cell of 200
  conversations or more (by campaign, term and drop) ran 0.86 to 0.88 (asserted).
- **Position and dominance:** every rung below R3 lands under the golden; over R1's pooled 21 per cent, R2 moves the
  list's forward share by at most 15 points (the drop and term logistic), R3 by 33 (to 54); no correction short of R3
  reaches the golden's bins, and no two of them combine to it: the nearest carries the special deposits at 57 per cent
  against the class's 88.
- **Grid:** every rival basis (22, `calc.rival_shares`) by the dialling estimators and the release share: every cell
  without the class lands at least 11 per cent under the golden; every class cell with the release share lands in the
  golden's bins (40 members, C3); the class without the release share lands 5.0 per cent over and a bin high (5,545.5,
  booked 5,500; a second error, refused by procedure 4.2).
- **Worth, on the graded figures:** the booking and all three monthly figures move with R3 (every month carries special
  deposits); no rung below it files any of the four.

### Margins

The thinnest margin is upward: the 40-member corridor runs 5,216.0 (one logistic in the drop and the class) to 5,302.6,
72.4 hours under the 5,375 line and 91.0 over the 5,125 line, and every member files 5,250 and the three months
(asserted); the months run 1,194.9 to 1,212.8 (69.9 over the 1,125 line), 1,986.5 to 2,020.3 and 2,034.6 to 2,069.4
(55.6 under the 2,125 line). The golden itself sits 94.1 hours inside its bin, its months 81.9, 111.7 and 64.3.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 18,400 deposits on the January to March 2027 list as cut on 2 November 2026; no deposit joins after the cut | procedure 3.1 and 3.3; the list file |
| 2 | Unit of account | one case per listed deposit, one per holder; hours are billed minutes over 60 | SF1, SF3 |
| 3 | Attribution window | every dial on a listed deposit belongs to the list, whatever month it falls in | SF4 |
| 4 | As-of dating | list, contact points and register at 2 November 2026; the card for January to March 2027 maturities in the draft brief | the extract names, the brief |
| 5 | Version basis | one close-out per closed campaign; one register edition; one brief per quarter | one edition ships of each |
| 6 | Denominator | the retention share is per conversation, not per case or per dial | SOW schedule 2 bills per conversation |
| 7 | Weighting | yields weighted by the coming list's mixes; the share applied deposit by deposit, by its class and drop | SF8, SF9, SF22 |
| 8 | Window length | the seven closed campaigns | SF7 (procedure 6.1, and C3) |
| 9 | Boundary inclusivity | drop bands and the class's gap; the NZ$25,000 listing threshold is the society's, already applied | SF8 and SF22 (C1, C3); procedure 3.1 |
| 10 | Rounding path | once, at the end, for the booking and each month, to the nearest 250 | SF13, asserted |
| 11 | Tie-break | none arises | a sum |
| 12 | Maturity and censoring | only closed campaigns: every released case carries a close-out | asserted |
| 13 | Order of operations | wash, mix, release share, yields, class, share, sum | each step commutes with the others except the wash, which precedes the mix |
| 14 | Row order | no step depends on it | sums and group-bys |
| 15 | Duplicate resolution | one release-log row per listed deposit, one close-out per released case, one row per dial | asserted in checks |
| 16 | Identity normalisation | account numbers dashed in 2025, unpunctuated from 2026; phone numbers in local and E.164 forms | the extract notes; normalised joins asserted complete |
| 17 | Netting against gross | none | does not arise |
| 18 | Dimensional units | rates in per cent on the 2025 lists, decimals from 2026; minutes against hours | the list headers and extract notes; SOW schedule 2 |
| 19 | Code and status semantics | disposition codes; release-log reasons | SOW schedule 3; the extract notes |
| 20 | Integerisation | none (expected hours) | does not arise |
| 21 | Clause scope | one SOW and one billing schedule for every campaign since January 2025 | SOW clause 1.1 |
| 22 | Forward window contents | the coming list, its holders' numbers, the register and the card are all filed; no dial on it exists yet | the extracts and the brief |

## Literal reader

Executed word for word on the built pack: the prompt asks how many agent-hours to book for the 18,400 deposits on the
January to March 2027 list; the procedure books the hours the list is forecast to need, to the nearest 250, drawing on
every campaign closed under the SOW (6.1), releases each deposit 21 days before maturity unless the holder has
instructed or no number is callable (4.2, 4.3), and the SOW bills each dial and conversation at fixed minutes (schedules
2 and 3) under the dialling rules (schedule 1). The forecast needs, per deposit, the expected dials that do not reach the
holder, the chance of a conversation and the chance that a conversation goes to the retention offer; the first two come
from the closed campaigns per mix of callable numbers, the third from the closed campaigns' conversations. Every reading
of every term is a row of the fork table and lands on the golden or is refused by a quoted sentence; every estimator in
the corridor files 5,250 (1,250, 2,000, 2,000). The default's figure is the same estimand computed with the share read
off every past conversation at the drop (or pooled, by term, by locked rate), which the seven campaigns contradict (in
every band of drop the conversations about money a special won ran 30 points or more above the rest, in every campaign
where both matured), so it is the easy method on the same literal estimand, not another reading of it.

## Oracles

- The campaign briefs: each quarter's card and the retention offer's limits; inputs every route reads the same way; no
  share, no hours, no special.
- The close-outs and the dial log: the past campaigns' events; every basis reproduces them (they are what happened), so
  none ties only under the golden.
- The treasury funding outlook (distractor): term funding balances by month and one flat 82 per cent rollover
  assumption on balances; no conversation share, no class, no hours.
- Harbourline's 2027 staffing proposal (distractor): team sizes, shift patterns, the hourly rate and a capacity well
  above any route's hours; no forecast of the society's hours, and none of the golden's figures.
- No published share by class or by drop, no past forecast, no booking memo and no rule of thumb for the block ships, so
  nothing ties only under the golden or only under the default.

## Ask sheet

The main call's declared row population: every row of the January to March 2027 list, the 2025 and 2026 lists, the
release log, the dial log, the close-outs, the contact points, the do-not-call register, the eight campaign briefs, the
SOW and the procedure. Device and hazard rows in it: 0 (asserted: the call's figures are unchanged with every ask file
deleted, and the asks read no file the call reads except the lists, device-free). The asks read the account event
extract, the member transfers extract, the term holdings view, the legacy certificate register, the migration batches
and the extract notes; Ask A reads the past lists for its population and Ask B the coming list for its last figure.
Each ask is a measure the campaigns or the book carry that the call does not turn on; neither is keyed to the call, its
construction or its figures; the two share no primary device and no primary file. No sentence in the pack adjudicates a
device: the extract notes describe each file's fields and scope only.

**Ask A. For each campaign from January to March 2025 to July to September 2026, how much of the principal on its list
was still on term deposit with the society 30 days after maturity, and from how many of its deposits** (7 amounts to
the nearest NZ$1,000, 7 counts; 14 figures).
- H18 home: the audit trail of what the calls the block pays for have kept on term (a measure every closed campaign
  carries that the booking, which forecasts hours, does not turn on); use: the Deposits Committee reads the block beside
  what the calls have kept.
- Golden: NZ$497,825,000 from 6,700 deposits; NZ$537,491,000 from 7,186; NZ$532,430,000 from 7,226; NZ$536,002,000 from
  7,172; NZ$562,096,000 from 7,591; NZ$557,067,000 from 7,494; NZ$573,831,000 from 7,765.
- Construction: per listed deposit, a REINVEST on its own account at that maturity and no BREAK or CLOSE in the 30 days
  after keeps its principal; otherwise the payments the society's maturity settlement account made that day naming the
  deposit in the narrative (the payments system's reference format, bank-branch-account-suffix) into term deposits
  opened that day and still open at 30 days, at the amount paid. The wording (how much of the principal on its list,
  and from how many of its deposits) counts a deposit that kept any part, at that part, without naming a partial move.
- Primary device (D7, the true key elsewhere, a reference string): a holder who changes term or amount at maturity does
  not reinvest on the old account; the core pays the old account out and opens a new term deposit, and the payments
  system pays the proceeds from its maturity settlement account with the old account named only inside the narrative.
  Read on the deposit's own account, every such change counts as money gone; a transfer from the old account, the
  natural join, finds nothing (asserted: the round-1 direct link files exactly the own-account read).
- Over-cleaning half: counting any term deposit the same holder opened within 30 days of maturity brings in new money
  from other banks (the events extract covers the holders' new term deposits, the new-money ones among them).
- Hazards: partial changes (part to a new term deposit, part paid to savings) and new money added to the new deposit
  (amounts); reinvested deposits broken within 30 days; accounts listed again a year later (an unanchored REINVEST counts
  a later year's renewal); account numbers dashed on the 2025 lists and in the narratives, unpunctuated in the extracts.
- C1 (asserted): no kept deposit is broken or closed between day 25 and day 35 after maturity; no savings account pays
  into a new term deposit; every listed deposit has a MATURE event at its maturity date; no deposit both reinvests and
  pays out at one maturity; every maturity payment leaves through the settlement account with its deposit's reference.
- Span (5 files, 12 columns): the 2025 and 2026 lists (account, principal, maturity date), the account events (account,
  event type, event date), the member transfers (from account, to account, amount, value date, narrative), the extract
  notes.
- Stops (measured): own account only (the cracker, and the direct-transfer join), every count 19 to 22 per cent low and
  every amount 17 to 19 per cent low; same-holder matching, every count 30 to 56 high and every amount 3.7 to 4.7 per
  cent high; payments followed at the new deposit's whole principal, every amount 0.9 to 1.1 per cent high (counts land);
  a partial move at the deposit's whole principal, every amount 3.2 to 3.7 per cent high (counts land); counted only
  when kept whole, every count 8 to 10 per cent low; no 30-day survival check, every count 116 to 152 high; a REINVEST
  found anywhere on the account, every 2026 figure high (2025 lands). Every golden amount sits at least NZ$150 from a
  rounding edge (a partial change of term's split moves a multiple of NZ$100 in the generator when a campaign would sit
  within NZ$150 of one).
- Realism: a core that books a change of term as a closed deposit and a new one, with a payments system paying maturity
  proceeds through a settlement account under a reference, is ordinary.

**Ask B. How much principal on term deposits and investment certificates together matures across the society in each
month of January to March 2027, and how much of the quarter's total is not on the list** (4 amounts to the nearest
NZ$1,000).
- H18 home: a qualifier of the call (how much of the maturing book the booked hours work on), from the maturity book
  the list was cut from, on rows outside the list; use: the note's line on what the campaign covers.
- Golden: January NZ$415,506,000, February NZ$646,816,000, March NZ$672,944,000; not on the list NZ$214,491,000.
- Construction: the core holdings view's deposits and certificates maturing in the month, once per account at the
  core's principal, plus the legacy register's certificates maturing in the month that are not in the core (not
  MIGRATED in the batches, and matching no core certificate on issue date, maturity date, rate and term); the list's
  principal taken off the quarter's total.
- Primary device (D1, the same records under two sources, the key incomplete): the platform's register (30 June 2026)
  still lists every certificate; the migration batches moved most of them to the core under new account numbers, and
  the operations team moved the certificates the batch loader rejected by hand, outside the batches. Every moved
  certificate sits in the holdings view as KIC; the hand-moved ones have no batch row, so the register less the batches'
  MIGRATED certificates, the careful solver's dedup, still double counts them; they are found only by matching the
  core's certificates to the register on issue date, maturity date, rate and term (unique, asserted).
- Second device (D2, an attribute at another vintage): at migration the interest accrued since each certificate's last
  anniversary was added to its principal in the core, so the register's principal is stale for every moved
  certificate; keeping the register whole and dropping the core's certificates, the other natural dedup, lands low.
- Hazards: the holdings view lists each account under each holder, the account's whole principal on each row (D6);
  certificates deferred in one batch and moved in a later one punish a rule keyed on DEFERRED.
- Span (5 files, 11 columns): the holdings view (account, product, principal, int_rate, term, start date, maturity date),
  the legacy register (certificate number, principal, rate, issue date, maturity date, term), the migration batches
  (certificate number, status), the coming list (principal), the extract notes.
- Stops (measured): rows summed and both sources added, every figure 15 to 18 per cent high and the part off the list
  more than doubled; once per account with the register added whole, NZ$5.3 to 6.5 million high a month; once per
  account with the register less the batches' moves (the careful dedup), NZ$0.32 to 0.78 million high a month and
  NZ$1.8 million on the part off the list; the register for every certificate with the core's certificates dropped,
  NZ$120,000 to 165,000 low a month; core only, NZ$0.5 to 1.5 million low; the DEFERRED and unbatched certificates added,
  high. Every golden figure sits at least NZ$150 from a rounding edge (an unlisted, sole-held deposit's principal is
  shifted by a multiple of NZ$50 in the generator when a figure would sit within NZ$150 of one).
- Realism: a customer-centric holdings view repeats an account under each holder, a migration in batches leaves a
  frozen legacy register and a manual exception path beside it, and a conversion that capitalises accrued interest is
  ordinary.

**Hazard table.**

| Hazard | Asks moved | Per-ask movement (measured) |
|---|---|---|
| Account number formats (dashed in lists and narratives, unpunctuated in extracts) | A | none once normalised; an unnormalised join drops every 2025 deposit and every payment |
| Partial changes and new money in the new deposit | A | every amount, 0.9 to 3.7 per cent |
| Breaks within 30 days | A | every count and amount |
| Accounts listed again a year later | A | every 2026 figure |
| Joint holders in the holdings view | B | every figure |
| Re-batched and deferred certificates | B | every figure |
| Interest capitalised at migration | B | every figure on the register-first dedup |

**Referee.** None needed: no designed disagreement between two systems is arbitrated by a third file.

**The cracker sheet.** The cracker filed the golden hours and months, ran the hygiene battery (keys unique, no exact
duplicates, every join matched, no fan-out) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 7 amounts and 7 counts | each listed deposit's own account, and transfers out of it: reinvested and open at 30 days, or gone | a change of term at maturity reinvests through a new account, paid from the settlement account under a narrative reference | miss |
| Ask B, 4 amounts | the holdings view once per account after the key check, the register added less the batches' moved certificates | the certificates moved by hand sit in both sources with no batch row, joined only on issue date, maturity, rate and term | miss |
| Note's chart and opening (recommendation block) | the booking and the monthly hours | carried by the main call, scored with it | outside |

The mirror sheet (the same response stopped at R2a, the drop) differs from the cracker sheet only on the recommendation
criteria, so no ask is coupled to the call.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 36 recommendation (the booking, the three months, the note's opening), 9
instruction following (the two files, the chart's named parts), 55 asks over 18 figures (about 3.1 each). With r = 4 (the
chart's structure and the note a wrong call keeps) and each top response keeping about 8 per cent of the ask weight:
C = 36 + 9 + 4.4 = 49.4 for the cracker, S = 4 + 9 + 4.4 = 17.4 for the mirror, the pair 33.4. The most obvious device
is Ask B's (the batches file announces a migration, and a count of the core's certificate accounts against it shows
the ones moved by hand): cracked by the cracker, it adds 11.2 (4 figures, 22 per cent of the ask weight) and the pair
rises to 39.0; with both top responses on the call and no device cracked, 49.4. Ask A's link sits inside a payments
narrative under a settlement account that no join the solver runs reaches, and its natural repair (the holder's new
deposits) lands high; a response that finds the narrative link takes Ask A's 14 figures (the pair would then be 52.7),
which is why Ask A carries an over-cleaning half and Ask B is the smaller ask.

Pair ceiling: 39.0

## Prompt

`prompt.txt` (voice-check.py exit 0, 863 characters): how many agent-hours to book for the 18,400 deposits on the
January to March 2027 list; td_booking_q1_2027.xlsx with the hours for the deposits maturing in each month, Ask A for
the seven campaigns (how much of the principal on its list was still on term deposit 30 days after maturity, and from
how many of its deposits) and Ask B for the quarter's maturities (each month, and the quarter's total not on the list);
td_booking_note_q1_2027.docx opening with the booking and charting the hours by maturity month; hours to the nearest
250, deposits whole and dollars to the nearest thousand, in the last sentence. It names no method, convention, input
file, standard or person, and nothing about rates, drops, specials or the retention offer; round 1's counting clause is
gone.

## Build record

- Round 1 (shipped 2026-10-12): the drop architecture, DETERMINISTIC and APPROVE on its re-judge; its two judge
  reports stay in the folder as round 1's evidence and describe the round-1 pack, not this one. Never on the portal;
  superseded at round 2 by the 10/10 audit (Tried and rejected).
- Round 2 generator: `task137/generator/build.py` (world, sim, book, pack, docs, postprocess, calc, asks, golden,
  writeup, checks, verify); world, sim, book, pack, docs, asks, calc, golden, writeup, checks and verify re-cut for the
  class of money, the new rate path and specials, the settlement account and the hand-moved certificates. Seeded per
  purpose (`world.rng`), fixed mtimes, office containers and PDFs normalised to the fiction's owners and stamps.
- Pack: 27 files in 6 formats (csv, pdf, docx, eml, txt, xlsx); the dial log 269,175 rows; target.zip 10.5 MB.
- Checks: 604 assertions, among them the three-rules block on the clean truth (R1, R2 per mess item, R3a, R3b, R3c),
  every SF row, the rungs and 22 rival bases each at least two bins under the golden and off every month, the
  40-member corridor, the flip, the domain claims the note and write-up make, both asks' goldens, stops and C1
  conditions, separation and distractor deletion, the realism sweep and the goldens against figures.json, all green;
  `verify.py` 34 checks (csv, pypdf, openpyxl; no generator import) green from the bundle alone.
- Two consecutive builds byte-identical: target, golden, metadata.json, figures.json and target.zip (sha256
  e9d6e93637fe658acbc03425898c8a8d79a6b3e4c47d36238c0cb3c4c655d5c9); target.zip equal to target/ by name and content
  (27 members, no folder).
- `figures_check.py task137`: exit 0, 111 figures. `voice-check.py task137`: PASS (863 characters).
- `guard.py surface task137`: exit 0; five pairs promoted on card axes only (task138 back to back, task117, task37,
  task97, task44), each differentiated on the card, surface overlap 0.075 to 0.093; the people the pack names are the
  card's. `guard.py heart task137`: WARN (`repeat.gate_g` against task130, answered under Guard). `guard.py validate`:
  clean. Container audit (`scrub_producer_metadata.py`): target and golden clean.
- `precut.py task137`: exit 0, 49 checks, 0 FAIL, 0 WARN (status BUILD, so strict; `voice-check.py` PASS inside it).
- `leak.py task137 --asof 2026-11-04`: REVIEW, no LEAK, sweeps 1, 2, 5, 6, 7, 8 and 11 clean. Each REVIEW line is
  harmless: 4.00 in the staffing proposal is a shift time (4.00 pm) and in the January to March 2027 brief the posted
  four-year rate, an input every route reads; the briefs, the SOW and the extract notes carry 10 to 12 of the call's 15
  distinctive words because they are the domain's own nouns (agent-hours, Harbourline, term deposits, maturity, list),
  not its figure or its step; the documents carry 3 or 4 of the 25 stump-paragraph terms, each in its own sense (the
  SOW's overage premium, the retention offer's 0.25-point limit, a holder's change of term or amount, the society's
  members), and none names a special, a class of money or a rate against its cohort; the dates after 4 November 2026
  are maturity dates of deposits and certificates still running (the coming list, the holdings view, the register and
  the events extract's maturity_date column; every event and value date is on or before 31 October 2026).
- Stage 4 (the leak reader and the determinism judge) is not run in this pass: the main session spawns both on this
  pack.

## Pre-ship check

1. Domain: a building society's quarterly take-or-pay booking of agent-hours for the calls to holders of maturing term
   deposits; the quantity that decides is the share of reached holders whose conversation goes to the 22-minute
   retention offer, which deposit liquidity behaviour forecasts by the stability class of the money (what a new-money
   special won against member money rolling on the posted card) beside the repricing gap. With another field's nouns
   there is no cash-rate-driven posted card that every deposit-taker moves together, and no premium that lapses at a
   deposit's first maturity, for the share to turn on.
2. Real work, nothing planted: past lists in two core-banking layouts (per cent rates, dashed account numbers and
   comma-grouped principal through 2025; decimal rates and unpunctuated numbers after the January 2026 upgrade), the
   contact centre's dial log in UTC with its own disposition codes and case references, release files listing each
   case's callable numbers, phone numbers in mixed New Zealand formats washed against a register with recorded and
   withdrawn dates, the posted cards inside each quarter's campaign brief; on the ask paths maturity proceeds paid
   through the society's settlement account under a narrative reference, a holdings view listing joint deposits under
   each holder, a frozen certificate register beside a migration log that misses the certificates moved by hand, and
   certificate principal carrying interest capitalised at migration; each what these systems produce, none deciding
   the call (R2, asserted).
3. The flip is a method choice: conditioning the share of conversations that go to the retention offer on the class of
   the money beside its drop; every rule in the pack (the SOW's minutes and dialling rules, the release 21 days before
   maturity, the do-not-call wash, the reinvestment default, the booking to the nearest 250) is executed the same way
   on the default path and the golden, and no document names a special or a class.
4. The analyst test holds on the built pack: dialling per mix with the release share and the share by band of drop
   books 4,250 (4,267.1), as do the pooled share, the latest campaign's, the share by locked rate, a logistic or
   isotonic fit in the drop and the share split by first listing; the drop and term in one logistic books 4,750
   (4,686.4), the audit's locked-rate-by-term logit 4,500 (4,472.1), the share by term 3,750; every one of 22 rival
   bases at least two bins under the golden 5,250 (5,280.9) and off all three months, asserted on the clean truth and
   the pack.
5. One defensible answer: procedure 6.1 and the SOW's schedules file the estimand and every convention; every fork row
   is asserted (SF1 to SF25); the class converges for every gap from 0.30 to 0.45 and each covered cohort's lowest rate
   is its brief's posted rate (SF22); the 40-member corridor files the booking and the three months; the booking holds
   for any special share down to 0.80, under every past special cell (0.86 to 0.88).
6. No decoy: no file states a forward share, an hours forecast, a past booking or a share by class or drop; the
   close-outs report what each campaign did and tie under every basis; the treasury funding outlook (a flat rollover
   on balances) and Harbourline's 2027 staffing proposal (a capacity and a rate, no hours for the society) are the
   declared distractors; no memo or voice argues for a share or a basis.
7. Nothing hidden and recovered: the class is rebuilt from two columns every route reads (each list's rate and opening
   date) against the lowest rate of its term and opening quarter; no rule is withheld, no certified figure pins the
   share, and the procedure sends the forecast to every closed campaign without naming a method.
8. A new lesson: a deposit book holds two kinds of money, and the money a special won goes to the retention offer at
   its first maturity whatever its drop while member money goes in proportion to its drop, so a list whose largest
   cohort is a special's money needs about a quarter more agent time than the share by drop books; no build on
   file conditions a behavioural share on how the unit's money was won (`guard.py heart` WARN on `repeat.gate_g` only,
   answered under Guard).

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
- Forum `line_manager_or_team` (the head of deposits signing the block order alone): task136 moved its forum to the same
  key after this card was registered, and `ban.forum` blocked; the Deposits Committee now approves the block.
- Write-up figures rounded coarser than they read: the list's retention-offer share to the nearest 5 per cent (60,
  against 62.1) and its non-reaching dials to the nearest 500 (67,500, against 67,354.8); the judge read both as wrong.
  Now whole per cent and nearest 100 (62, 67,400), with freeze.py allowing the two keys
  (`components.retention_share_pct`, `steps.non_reaching_dials`); the Final Recommendation and Critical Components move
  only by that 60 to 62.
- The judge's wording for the Ask A clause (a deposit counts if any of its maturity proceeds were in a society term
  deposit, its principal the amount in term deposit then): "maturity proceeds" is the transfer extract's narrative and
  points at Ask A's device, and "the amount on term deposit then" reads as the new deposit's whole balance, new money
  included (the whole-principal stop). Filed as: counting a deposit if any of its principal was, and only the part that
  was.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because its decisive step, the share of
  conversations going to the retention offer conditioned on each deposit's drop from its locked rate to the card, was
  the strong model's reflex and the field's textbook model: a logistic of the retention outcome on term with a separate
  locked-rate slope per term booked about 5,496 hours, inside the golden's 5,500 bin, without reading any card; the
  share by locked rate sat one bin under; Ask B's migration batches file announced the overlap and an account-level
  dedup against it cracked the ask; Ask A's clause (a deposit counted if any of its principal was kept, and only that
  part) signalled the partial-move device; and the swap test passed only narrowly (insurance renewals priced off a rate
  card read almost the same). Round 2 keeps the world, the call and the asks' populations and moves the decisive step
  to the class of the money, a reason only deposit repricing behaviour has.
- A market-gap stump for round 2 (each deposit's locked rate against a published market rate for its term and opening
  month, the deposits far above the market leaving): the market table made the premium a visible column and the step
  one join (readability tests 2 and 6); the class is rebuilt from each list's own cohorts instead, with no table naming
  it.
- Other round-2 candidates for the decisive step, dropped at the draw: the term structure of the card alone (still the
  drop, read term by term, the reflex the audit measured); the best card across terms as the rate a deposit is compared
  with (a second reading of the rate it reinvests at, a fork and never a stump); money above the Depositor Compensation
  Scheme's per-depositor cover leaving at maturity (a filed limit executed on a visible principal column, rule
  application read off the schema).
- Round 2's first prototype kept round 1's January to March 2027 card (four years 3.15 per cent, so the special's drop
  was 2.50 points): past special money dominated the 2.50 band, so the share by drop alone booked near the golden, and
  the locked-rate-by-term logit carried the special's deposits at about 0.8. The 2027 card was turned up (four years
  4.00, a drop of 1.65), a band in which past conversations are 89 per cent member money.
- The card's gap reordered to population first: `guard.py check` blocked on `test.same_driver` (population, E,
  forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
  order for a premium that lapses at first maturity.
- January's share of the 2023 four-year special's sales at 0.242: January's hours sat near a rounding edge and the drop
  and term logistic landed January's bin (1,250); the sales by month are now 0.184, 0.408 and 0.408, January's golden
  1,206.9 and that rival's January 1,000.
- Ask B at six figures (each month's maturing principal on and off the list): with Ask B the most obvious device, the
  cracker's pair ceiling rose to 41; cut to four figures (the three months and the quarter's part not on the list),
  39.0.
- Ask A's device as a posting date (D8, maturity proceeds posted on the next business day): the hygiene battery's
  unmatched-join count found it at once; moved to the payments system's settlement account with the matured deposit
  named only in the narrative (D7).
- The write-up's past share for member money (15 per cent, 14.57 unrounded) and all past conversations' share in the
  special's band (35 per cent, 34.55): both within 0.07 of a rounding edge; dropped from figures.json, the write-up, the
  note and the workbook, the band given by class instead (88 and 28 per cent, 0.24 and 0.18 from an edge).
- The note's chart title "Seven in ten hours are conversations, most of them retention offers": under the round-2
  shares January's conversations go to the offer 45 per cent of the time and the retention offer's minutes are under
  half the talk in January and March; retitled to the measured two-thirds (0.665 to 0.693, asserted).
- Band shares as a Critical Component (88 against 28 per cent at drops of 1.50 to 1.75): a corridor member (special
  money pooled, a logistic within each class) never computes them; the component keeps the class's 87 per cent and the
  bands stay in the steps.
