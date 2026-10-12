# task128 design note

Architecture 3, re-rooted on 2026-10-12 in oviya1301's wave 1. Architecture 1 (whole-host rebuild valuation in an online travel platform's patch tickets) was solved by the in-house plain solver on 2026-10-10; architecture 2 (one change request per drain window) shipped and came back FAILED_TO_STUMP, and was spent at the wave-1 re-root because its decisive step read a filed rule and IT patch remediation has no client task type serving Opportunity Sizing. A first architecture-3 draw (a pet insurer's older-dog renewal increases) was withdrawn on the guard. Their lines stay in the last section of this note, in the card's lineage and in git history; the v2 generator, pack and write-up have left the tree, and `solver_rounds/` stays as the record of the v2 rounds.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task128.json`, architecture "v3 (architecture 3, re-root at wave 1: which collections centre's overflow earns a sixth team, or none)", registered 2026-10-12, `guard.py check` PASS with no WARN. Banking, Credit & Financial Risk, task type `collections-recovery` (the client task type serving Opportunity Sizing); objective Opportunity Sizing & Decision Support; shape 01 (five centres ranked under a cap of one team, with none on the same footing); decision `pick_one_of_n`; strategy `causal_design`; gap population, then objective; decisive mechanism G5 (the cure a call is credited with is met elsewhere: the customers it reaches pay anyway, and the accounts it misses include ones no call could reach), then G8 and G16; gate `signal_vs_noise_or_hold` (the call is a hold forced by a computed blocking quantity); calibration none; layer 2 `estimand_identification`, `own:capacity-overflow-natural-experiment-for-early-stage-collections-calls`.
- **World:** Ferncliffe Trust Bank, a Canadian bank with about 1.6 million credit card accounts, runs early-stage collections from five centres (Thunder Bay, Sudbury, Kingston, London, Winnipeg). Its 19 billing cycles each have a collections day, the cycle's business day of the month, when the cycle's accounts that reached 30 days past due load to their centre's dialler list; accounts on an arrangement, in a dispute, deceased, insolvent or on a business card are held off the list. The team works the list in load order until the shift ends; the dialler skips records on the bank's do-not-call file or with no dialable number; records it never reaches get the protocol's letter. Twice a month the two cycles that carry the 2024 student-card campaign swamp the teams, London's most. The credit policy funds a new team (the budget's standard team, rated at 400 accounts dialled a day) only where its calls would have prevented at least 694 rolls to 90 days past due on the past year's lists ($1,183,000 over the $1,705 the bank books on a roll, rounded up). Forum executive_team (the chief risk officer and the head of retail operations sign it), forcing event vote_or_meeting (the December executive meeting), organisation financial_institution, role operations_director (the director of collections operations). Personas from `guard.py names --geo Canada --seed 128`: Elizabeth Marquez, Gabriel Ross, Kathryn Gray (Samantha Pittman skipped on the first-name rule against task447).
- **Data-native sentence:** a centre's team works its 30-day list in the card platform's extract order and stops when the shift ends, so on the campaign cycles' collections days the bottom of the list is never reached and a call is as good as random between the records above and below the day's last dial; but the dialler decides whether it can dial a record only when it reaches it, so the records it skipped as undiallable are marked only above that line, and the records left at shift end carry their own share of undiallable accounts, unmarked.
- **Sources, one line each.** `strategies.md` F9 (causal design: interference, a contaminated arm, regression to the mean, a pool-dependent rate; no measured hold, 131 shipped on interference): this build's arm is contaminated by one-sided non-compliance in a natural experiment from capacity, not by interference. Seed DS04 (unbuilt, a utility's arrears-outreach team): the world and the insight that overflow is the only fair comparison; this build drops the seed's verification subsample and its requester's hunch, moves it to a bank's card collections and adds the dial-time suppression that makes the clean-looking comparison wrong. The client's estimand-and-identification family (selection on the outcome, the right counterfactual). `measured-drivers.md`, the held group's conjunctions (team plan allowance, replenishment cover): the suppressed records set aside, the same-day restriction and the new team's daily capacity each land a centre alone; only all three hold.
- **Same-puzzle test:** gap population, decisive G5, decision `pick_one_of_n`, gate `signal_vs_noise_or_hold`: no build in the last twelve, lineage included, shares the triple (guard PASS on `test.same_puzzle` and `test.same_driver`); this slot's own v1 and v2 were (objective, rule, binding_constraint), so the decisive rung has moved.
- **Abstraction test against the nearest drivers.** task103 v1 (0.07, one contact serving several units under a standing authorization): there the record of contact misstates the unit; here the record is right and the comparison is the question. task180 v3 lineage (0.05, channelling against a self-controlled comparison): there each person is their own control over time; here records on one day's list are compared across a capacity line. task121 v3 (0.05, the same clock hours on other days): there exposure is set against itself on other days; here the arm the dialler reached keeps the records it could not dial.
- **Arithmetic:** prototyped in the scratchpad, then fixed by the generator (`generator/sim.py`, hashed per-account draws so a parameter moves only the draws it touches): five centres, 1.6 million accounts, 19 business-day cycles, the campaign on cycles 04 and 13, every rung below as built and asserted in `checks.py`.

## Default path

1. Take every 30-day entry in the delinquency history for July 2025 to June 2026, listed or held, at each centre (a held entry's centre from the account's other list records), and mark each as called if the dialler placed a call to it on its list day.
2. Mark each entry's outcome from the delinquency history: 90 or more days past due on its cycle date two months later, or not.
3. Compare the roll rates of called and uncalled entries by centre, adjusted for the behaviour score.
4. Take each centre's difference as the rolls a call prevents and multiply it by the accounts the new team would dial there, its 400 a day on the days the team left accounts at shift end.
5. Fund the centre with the most rolls prevented, which clears the policy's 694.

Ends on: fund London, at about 2,315 rolls prevented a year (as built).
Golden: no centre; London's 495 is the most, 199 short of 694 (as built; 500 and 200 at the nearest 100).

## Stump sentence

The default path funds London at about 2,315 rolls prevented a year because step 3 compares called with uncalled 30-day entries in the delinquency history, pooled over the year, when the uncalled are the accounts the protocol holds off the list, the records the dialler skipped as undiallable and the records left at shift end on the campaign cycles' days, all of which roll more for reasons a call does not change; read on the same lists, with the skipped records kept beside the records the dialler reached and the new team held to its 400 dials a day, London's team would have prevented about 495 rolls, the most of any centre and short of 694, and no centre gets the team.

## Three rules

Domain test: collections strategy is funded on incremental cures against a counterfactual, the champion-challenger tests a bank runs or, where it runs none, the natural experiments its capacity hands it on the days a team cannot finish its list; the deciding quantity here (rolls to 90 days past due a second team's calls would prevent on the accounts it would take) is the one collections analytics estimates, and with another field's nouns there is no dial-time suppression, no 30-to-90 roll and no cycle-day list, so the task stops reading the same.
Analyst test: a strong analyst who cleans the lists, the call detail and the delinquency history and reads the policy right finds the capacity overflow and compares, on each over-capacity list, the accounts dialled with the accounts left at shift end, setting the records the dialler skipped as undiallable aside because no team can call them; that funds London at about 981 rolls a year against the 694 the policy needs, because the records left at shift end still hold their share of undiallable accounts, which roll far more, while the dialled side has had them removed.
Layer 1: five centres' dialler list exports in load order with each record's final result in two code sets either side of a dialler upgrade, attempt-grain call detail with the QA team's test calls, the platform's 30-day entries with hold codes, a delinquency history by cycle date with re-aged and charged-off accounts, a capacity log by centre and day with a dialler version and London's two pods merging, an arrangement system extract carrying each balance in its account's own currency, the treasury's daily booking rates, and the protocol, the policy and the budget.
Layer 2: a call's effect from a capacity natural experiment with one-sided non-compliance (estimand_identification): every record above the day's last dial against every record below it on the same list, the skipped records kept on the reached side, scaled to a dial and sized on the dials a second team could make.

## Readability screen

The six tests (`stumping` 2.1) on each rung; every rung is a complete sizing of the five centres against 694.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 platform 30-day entries, called against uncalled, pooled, score-adjusted (the default path) | the protocol files the holds | the entry file is the natural population | yes | no | no | no | readable |
| R1 dialler lists, dialled against not dialled, pooled | no | the result codes | yes: called against not called | no | no | yes | readable |
| R2 over-capacity lists, dialled against left at shift end, skipped records set aside, same list day | the protocol's letter goes to records left at shift end | blank results mark the overflow | yes: undiallable records are set aside as no team can call them | no | no | no | readable |
| R3 reached (dialled or skipped) against left at shift end, pooled over the year's lists | no | the result codes | yes: one pooled comparison | no | no | no | readable |
| R4 R5's effect sized on every diallable account left at shift end, London uncapped | the budget files the team's 400 a day | no | no | no | no | yes | readable |
| R5 (decisive) reached against left at shift end on the same list, per dial, sized on the new team's dials | no: nothing says the records left at shift end hold undiallable accounts | no: the skip codes sit only on records the dialler reached | no: the reflex sets the skipped records aside or counts them as uncalled | no | no | no | silent |

Exposure: every reader who finds the overflow asks how to compare the two sides of the line; what stays silent is that the dialler decides a record is undiallable only when it reaches it, so the skip codes exist on one side only. A reader who tabulates result codes by position against the day's last dial sees no skip code below it; that is the route to R5, and it is the exposure this design accepts. The new team's capacity (R4) and the same-day restriction (R3) are readable conjuncts, each landing London alone.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | roll to 90 days past due | 90 or more days past due on the account's cycle date two months after the list day | ever 90 or more within 120 days; at the next cycle date | figures move, same call (asserted) | the policy's definition |
| SF2 | the July 2025 to June 2026 lists | records on list days 2 July 2025 to 25 June 2026 (1 July is a holiday; cycle 19 is the last list day of June) | cycle dates or outcome dates in the window; CP-14 6.2's latest year of lists whose rolls are known at the pull (August 2025 to July 2026) | same call (C1: every record's list day is its cycle's collections day, asserted; the policy's year keeps every centre's bin, London 532, asserted) | the prompt names the lists; C1 |
| SF3 | rolls the new team's calls would have prevented | each dial the new team would have made on the year's lists times a dial's effect | the rolls the existing teams' calls prevented; rolls per 100 accounts | London moves out of its bin | the policy and the prompt name the new team |
| SF4 | the new team's dials | the budget's 400 accounts dialled a day, each day it has records left to dial | the centre's own team's capacity; attempts rather than accounts | London moves out of its bin | the budget line's rating |
| SF5 | centre | the list's centre code | the register's servicing centre | same call (C1: every list record's centre is its account's centre, asserted) | C1 |
| SF6 | the skipped records | the new team's dialler skips the same records (the bank-wide do-not-call file, the dialler's number check) | a second team would dial them | London's figure moves, same call | the protocol |
| SF7 | rounding | each centre's rolls from unrounded figures to the nearest 100 | the effect rounded first | same bins (asserted) | the prompt |
| SF8 | test records | the QA team's test calls are not accounts (no entry, no history) | counted as dials | same call (asserted) | no history row |
| SF9 | re-listed accounts | each list record is a unit with its own outcome | one record per account | same call (asserted) | C1 |
| SF10 | the bar | at least 694 rolls, inclusive (CP-14 6.5: $1,183,000 over $1,705, rounded up) | strictly more than 694; the unrounded 693.8 | same call | the golden's largest centre is far below it |
| SF11 | estimating a dial's effect | reached against left at shift end within each list day, per dial | regression with list-day effects with and without the behaviour score; list-day weighted means; one comparison pooled over the over-capacity days; the instrumental-variable form | same bin on every centre (asserted) | asserted in checks.py |
| SF12 | a day with fewer diallable records left than 400 | the new team dials every one | it dials 400 regardless | same call | C1: every centre but London stays under 0.8 of 400 on every over-capacity day, London over 1.5 (asserted) |

## Ladder

Five wrong sizings and the golden, each reproducible from the raw files, as built (`checks.py` L1 to L6, M4, SF11). Rolls a year the new team's calls would have prevented, against the policy's 694.

| Rung | Method | London | Kingston | Winnipeg | Sudbury | Thunder Bay | Call | Dies to |
|---|---|---|---|---|---|---|---|---|
| R0 (default) | every 30-day entry, listed or held, called against uncalled, pooled, score-adjusted, times the new team's dials | 2,315 | | | | | London | the holds and skips in the uncalled (the protocol, the result codes) |
| R1 | dialler lists, dialled against not dialled, pooled | 2,305 | 960 | 1,161 | 732 | 595 | London | the skips in the uncalled; the campaign cycles' days |
| R2 | over-capacity lists, dialled against left at shift end, skipped records set aside, same list day | 981 | 358 | 462 | 243 | 194 | London | the undiallable accounts left at shift end, unmarked |
| R3 | reached against left at shift end, pooled over the year's lists | 1,830 | 599 | 709 | 433 | 382 | London | the campaign accounts behind every record left at shift end |
| R4 | R5's effect on every diallable account left at shift end | 1,114 | 204 | 204 | 103 | 99 | London | the budget's 400 a day |
| R5 (decisive, golden) | reached against left at shift end on the same list, per dial, on the new team's dials | 495 | 204 | 204 | 103 | 99 | none | none |

- **Position and margin.** The golden's largest centre is London at 495 (500 at the nearest 100), 0.71 of 694; every wrong rung funds London at 1.4 times the bar or more (R2 981 the nearest; its day-weighted and pooled forms 968 and 991; R2b 1,095; R0b, contacted against not contacted, 1,629). Every centre's golden sits mid-bin at the nearest 100 with the whole estimator family inside it (SF11: London 474 to 523, Kingston 182 to 219, Winnipeg 192 to 207, Sudbury 95 to 106, Thunder Bay 94 to 105; nearest family member at least 24 rolls from a bin edge).
- **Grid.** Three corrections, the skipped records kept on the reached side (K), the same list day (D) and the new team's daily capacity (C): K, D and C together give 495; K and D without C 1,114 (R4); K and C without D 1,830 (R3); D and C without K 981 (R2); every cell missing two or three files a larger London figure (asserted, L5). The effect left per listed record instead of per dial gives London 408, the same call in another bin (L6).
- **Worth.** K moves London from 981 to 495, C from 1,114 to 495, D from 1,830 to 495; R1 and R0 sit above them all. The decisive move is K: it is the only one no filed sentence, column or reflex hands over.
- **The hold.** The blocking quantity is London's 495 against 694, reproduced; every centre fails for a named reason (its rolls short of 694); the prompt licenses none on the same footing; the default path names London; what would have made a pick: a dial's effect at London of about 7.2 rolls per 100 dials (694 over its 9,600 dials) rather than 5.2.
- **The binding.** London's diallable records left exceed the new team's 400 on every one of its 24 days (1.75 times at the least), every other centre's stay under 0.8 of 400 on every day (Winnipeg 0.77 at the most), so the per-day cap is never borderline (M2, M3).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | records on each centre's 30-day lists on list days 2 July 2025 to 30 June 2026; QA test calls are not list records | the prompt and the protocol; C1 (test calls carry no list record, asserted) |
| 2 | Unit of account | a list record (an account on a list day) | the policy counts rolls by listed account; C1 on re-listings (SF9) |
| 3 | Attribution window | the list day | the prompt names the lists |
| 4 | As-of dating | outcomes on the cycle date two months after the list day, all before the 9 October 2026 pull | asserted: the latest outcome date is 31 August 2026 |
| 5 | Version basis | results as the dialler exported them | C1: no record re-exported |
| 6 | Denominator | the new team's dials (a dial's effect times dials) | the policy and the budget (SF3, SF4) |
| 7 | Weighting | within list day; every reasonable weighting lands in the same bin | SF11, asserted |
| 8 | Window length | one year of lists | the prompt |
| 9 | Boundary inclusivity | 1 July 2025 is a holiday and the first list day is 2 July; the last list day in the year is 25 June 2026 (cycle 19), nothing on 26 to 30 June | C1, asserted (SF2) |
| 10 | Rounding path | each centre's rolls from unrounded figures to the nearest 100 | the prompt; asserted |
| 11 | Tie-break | none: a hold, and London's figure leads the next centre by more than a bin | asserted |
| 12 | Maturity and censoring | every record in the year has its two-month outcome in the history | asserted: no record in the window lacks its cycle date two months on |
| 13 | Order of operations | a dial's effect, the new team's dials, the product, the comparison with 694 | linear |
| 14 | Row order | sums and means only | C1 |
| 15 | Duplicate resolution | re-listings are separate records; no record repeats | C1, asserted |
| 16 | Identity normalisation | account numbers across the lists, the history, the entries and the register | the extracts' keys; every list record joins its history (asserted) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | rolls; accounts dialled a day | the budget's unit (SF4) |
| 19 | Code and status semantics | blank: not reached at shift end; DNC and NDN: skipped by the dialler; every other code: dialled | the dictionary; the codes' meaning is filed and never the stump |
| 20 | Integerisation | rolls rounded to 50 per centre | the prompt |
| 21 | Clause scope | the policy's rule applies centre by centre | the policy |
| 22 | Forward window contents | 2027 is sized on the July 2025 to June 2026 lists | the policy's sizing basis and the prompt |

## Literal reader

Executed word for word, the prompt and the policy fix one quantity per centre: the rolls to 90 days past due (90 or more days past due on the account's cycle date two months after its list day) that the new team's calls would have prevented on the centre's lists of July 2025 to June 2026, the new team dialling up to the budget's 400 accounts a day, set against the policy's 694. No sentence says how a call's effect is estimated or which records form the comparison: those are HOW, and the records force them (the list order is unrelated to the outcome, the overflow happens only on the campaign cycles' days, and the dialler marks a record undiallable only when it reaches it), so only the same-list comparison with the skipped records on the reached side reproduces the counterfactual. Every literal reading of the quantity is one number per centre; the easy answer (London funded) comes from easy methods on the same literal quantity, never from another reading.

## Oracles

None. No shipped figure ties to a call's effect: the capacity log's daily counts tie to the lists on every path, the protocol and the policy carry no effect estimate, no earlier test of the early-stage calls ships, and the budget's 400 is a capacity, not a result.

## Ask sheet

Main block (recommendation and critical components): the call (no centre), each centre's rolls the new team would have prevented (the five components), London's as the largest, and the chart of the five against 694. The cracker keeps all of it; the mirror (R2) keeps only the chart's bar line.

**Ask A: right-party contacts per 100 accounts dialled, and promises to pay per 100 right-party contacts, by centre (10 figures, one decimal).**
- H18 home: what a call achieves at each centre, beside the funding decision in the executive memo; the call does not turn on it.
- Primary device (D2, a label stored before a silent switch): the dialler upgrade (the Ontario centres on 20 October 2025, Winnipeg on 17 November 2025) reused result code AR: before, an arrangement agreed with the customer; after, an answering machine with a recorded message, arrangements moving to the new code ARR. The result-code list in use describes the current dialler only; the old AR records carry an agent and minutes of talk in the call detail, and the arrangement extract holds an arrangement set up that day on each.
- Over-cleaning half: AR read as a contact throughout.
- Hazards: the QA team's test calls in the call detail (no list record); the old dialler's AM code (answering machine), absent from the current list.
- Path: list export (results), call detail (agent, talk seconds), result-code list, capacity log (dialler version), arrangement extract, data dictionary: six files, about ten columns.
- Stops (as built, A3, A4, HZ1, HZ2): the current code list read back, contacts 3.2 to 3.7 per 100 low at every centre and promises per contact 2.2 to 3.4 high; AR a contact throughout, contacts 10.3 to 12.2 high and promises 6.2 to 7.9 low; Winnipeg on Ontario's upgrade day, contacts 0.8 low; the QA test calls counted, contacts 0.6 to 1.2 off; each outside the golden's one-decimal bin at every centre it touches. Golden: contacts 49.3 (London) to 57.2 (Kingston), promises 36.4 (Sudbury) to 41.2 (Thunder Bay), each within 0.005 of its bin centre.
- Realism: dialler vendors reuse two-letter result codes across versions, and a code list kept for the dialler in use describes the current version only.

**Ask B: balances placed on payment arrangements set up by each centre's team in the year, CAD (5 figures, nearest 100,000).**
- H18 home: what the teams already place on arrangements at each centre, beside the funding; the call does not turn on it.
- Primary device (D3, a missing currency read as the house's): the arrangement system keeps each arrangement's balance in its account's own currency, and about one arrangement in 25 is on a US-dollar Visa account; no column says so. The register's product code names the US-dollar card, and the delinquency history carries the same accounts' balances in Canadian dollars.
- Hazard: arrangements set up on the collections day against arrangements keyed in the following days for the same list record (both counted by set-up date in the year).
- Path: arrangement extract, register, delinquency history, treasury booking rates, data dictionary: five files, about nine columns.
- Stops (as built, B2, B4): US-dollar balances read as CAD, every centre low by 68,000 to 173,000 (Thunder Bay 6,944,308 against 7,012,003); US-dollar arrangements dropped, every centre lower still; each outside the golden's bin. Treasury's month-average and year-average rates keep every bin (B3). Golden: 7,000,000 (Thunder Bay) to 16,000,000 (Winnipeg), each 4,000 to 15,000 off its bin centre.
- Realism: card platforms keep a US-dollar card's balances in US dollars and report them in Canadian dollars only in the general ledger; an arrangement system that never needed a currency column is ordinary.

**Hazards (cross-cutting).**

| Hazard | What it is | Ask A | Ask B |
|---|---|---|---|
| HZ1 dialler upgrade date by centre | the Ontario centres and Winnipeg switched four weeks apart | moves every centre's contacts if one date is used | none |
| HZ2 QA test calls | test calls to the QA line in the call detail | moves contacts if counted | none |
| HZ3 currency | US-dollar card balances | none | moves every centre |

**Referees.** Ask A: the call detail's agent and talk seconds, the arrangement extract. Ask B: the delinquency history's Canadian-dollar balances. None hands over a level.

**No marker, no oracle.** The AR records before and after the upgrade carry the same code and sit in the same columns; the US-dollar arrangements carry no currency and their accounts appear in every file as every other account does. No control total ties under one handling only.

**The separation line.** Zero device and hazard rows in the main call's population, asserted by count: the code switch moves no record between dialled, skipped and left (AR is a dial outcome before and after); the currency touches only the arrangement extract; the test calls carry no list record.

**Cracker sheet.**

| Ask figures | n | The cracker's path (lands R5, runs the battery, executes every filed rule) | Cracker |
|---|---|---|---|
| Ask A, contacts per 100 accounts dialled | 5 | maps results by the current code list; the old AR arrangements read as machines | miss |
| Ask A, promises per 100 contacts | 5 | the same contacts as denominator | miss |
| Ask B, balances on arrangements | 5 | sums the extract's balances as CAD | miss |

Mirror leakage: 5 per cent (the mirror keeps one chart criterion, the 694 line, of about 21 ask criteria).

Pair ceiling: 37.7 (planning weights 38 / 7 / 55 with the five centres' rolls as the critical components and r = 5; ask criteria: ten contact figures, five balances, about four chart criteria and two memo lines; the cracker keeps the chart and memo, 38 + 7 + 55 x 6/21 = 60.7, the mirror the 694 line, 5 + 7 + 55 x 1/21 = 14.6).

The honest exposure: a response that lands the hold and also finds the code switch and the US-dollar balances keeps the asks, and two such responses would fail the bar. Criteria: the call, five centres' rolls, ten contact figures, five balances, about four chart criteria, two memo lines and three files, about 30.

## Leak check

`leak.py --asof 2026-10-09` REVIEW, no LEAK (stage 3). Each REVIEW line, harmless:
- Sweep 3, 694 in the credit policy: the funding line itself, filed once in CP-14 6.5 and named by the prompt as "the policy's funding line"; it is the bar, not an answer.
- Sweeps 3 and 4, the call's and the stump paragraph's words in the protocol, the policy and the field reference (centre, team, early-stage, budget, line, records, reached, dialler): the documents' own vocabulary; none says which records form the comparison or that the records left at shift end hold undiallable accounts.
- Sweep 9, 144 first instalment dates after 9 October 2026 in the arrangement extract: arrangements set up in late September schedule their first instalment in October and November; forward-looking schedule dates, allowed.

Reader's pass (stage 4, once, on the 700 build): nothing names the decisive step, nothing ranks the centres, no file exists only to help; its question-5 sentences (CP-14 6.2 to 6.5, protocol 2.3, 3.1 and 3.2, the list grain) execute to the golden's quantity and leave the comparison open, as designed.
- Fixed: the field reference listed CAMPAIGN_ID under the list export, which carries none (R9 now asserts every field the reference lists is a column of its file); the register's scope note for the history now separates the entry months from the cycle dates; the funding line divided to exactly 700 ($1,183,000 over $1,690) and read as tuned, so the loss per roll is $1,705 and the line 694 (693.8 rounded up), no centre's rounded figure or gap moving.
- Harmless: AM, the old dialler's machine code, is absent from the reference's code table, which lists the current dialler's codes (Ask A's device; a legacy code missing from a rewritten reference is ordinary). CP-14 6.5's "Where no centre reaches it, the budget line is returned" is the funding rule's own else-clause; the prompt already licenses none ("if anywhere") and the default path still funds London. 6.3 with charged-off or current accounts: the history's grain statement says no row means current, and every charge-off row is 180 days past due or more, so neither can be a roll two months after a 30-day list. The budget notes, the headcount workbook and the list-day spikes (the campaign cycles) are ordinary exports.
- Second read (final build): nothing names the move, ranks the centres or reads as the answer. Fixed: the register's list-day span ended 25 Sep 2026, the export runs to 28 Sep (R10 asserts the span against the export). Harmless: the contacts ask's "accounts dialled" (the field reference files account-days and the workforce log ties to the lists' dialled records on all 1,995 centre-days); cycles 04 and 13 carrying about eight times the other cycles' history rows (every VSD account bills on one of them, visible in PRODUCT_CD).
- Judge (stage 4, on the 700 build): DETERMINISTIC, APPROVE; every figure reproduced (London 494.7, Kingston 203.8, Winnipeg 204.0, Sudbury 103.2, Thunder Bay 98.6), six estimator variants and CP-14 6.2's own year in the same bins; its two optional notes (CP-14 dated before the budget it quotes; a Kingston pilot dated after Kingston's upgrade) applied; its third (list AM in the code table) declined, it would file Ask A's device. No rounded figure moved, so no re-judge.

## Tried and rejected

- The note's own decisive rung (drains per window from the capacity register, the hourly forecast and the window calendar) as the decisive move: the SRE standard states the N+1 rule in a sentence and the acknowledgements reproduce 412 of 412 only under it, so a plain solver builds it from a stated rule plus a corpus that refutes the rung below; its driver also sits beside task106's shared-pool driver. Kept as the stop rung.
- A data-cluster maintenance cycle (each November ticket reaches only the nodes recommissioned inside the month): task50 v4's insight (a forward service order truncated by the funded window) under new nouns although text similarity read 0.06, and guard BLOCK test.same_driver_older against task87 v9 on (time, G7, binding_constraint).
- Exempting standby or idle-colour colocated hosts from the drain limit: constructible from the capacity register's serving-capacity definition and the SRE standard, and it is a class of honest records excluded from a constraint, the shape task58 v3 and v4 lost on Gate G.
- Reboot sharing among the office's own tickets on one host in one window: reads as task98 v2's driver (demand that rides on a unit already consumed), and the acknowledgements can be blind to it only if no record shows sharing, which leaves a sentence the solver executes.
- Office packages riding other teams' scheduled drains (the kernel team's rotation): provision elsewhere (task118, task36) plus a forecast of another team's rotation.
- An update pulling dependency upgrades that fix other packages: needs package-manager behaviour from outside the bundle, or a closed-ticket record that refutes the stop rung.
- Fix-availability gates (an internal mirror's soak, an extended-support entitlement, an end-of-life successor package): a status-word eligibility gate a solver executes in one join once any sentence raises it, or a correction to what the scanner reports.
- Hosts made clean as the scored unit: task87 v8's conjunctive coverage.
- Re-introduction on autoscaled estates and scan-confirmed closure: both turn on how taken out is read (a flow against a month-end state) or on the scanner as an instrument.
- Keeping counterparty_acknowledgement, budget_or_appropriation and service-operations-sla at registration: blocked against task126 and task127 (filed after this draw) and, for the subdomain, against task129 drafted in parallel; redrawn to closed_decision_corpus, launch_or_rollout and field-service-maintenance.
- The drain tool's parallelism setting as rung R2 (a filed concurrency figure between no limit and the window rule): whether it binds depends on whether two requests share a drained host, a fork the stop rung must not carry; kept as a declared distractor and a swept rival in the acknowledgement back-test, and the day's-peak reading of the headroom clause took the rung.
- Leaving reboot sharing unpinned at the stop rung: a stop-rung solver who packs many tickets onto each drained host approaches the answer's colocated figure without the decisive move; the acknowledgements now refute sharing through overlapping requests.
- The 3a colocated answer as built (one ticket per colocated estate on the package most drained hosts carry): no package was open on every top-96 or top-120 host, so under standard s.3 one ticket could not name the hosts it was credited with; replaced at 3b by an October glibc advisory on the C library every el9 host carries, the highest-scoring colocated finding.
- Acknowledgement host lists drawn at random from the drain pools (3a): accepted hosts did not share their latest window with in_service_since, which argued against the rebuild the decisive rung rests on; replaced at 3b by binding every host's in_service_since to its latest accepted window.
- Round 1 plain solver (2026-10-10) landed 1/1/76/75/77/70 for 13,362: the decisive rung (R4, drain values the whole host) was read straight off the host inventory, in the solver's words "a drained host is rebuilt from the current image. Hosts rebuilt after a CVE's disclosure don't carry it, so draining clears every finding on the host" (path step 4). Binding in_service_since to each host's latest accepted window (3b) plus no finding predating it makes the rebuild a lookup, not a construction; the silent-rung architecture failed here, harden loop 1 must break that per-host date coincidence.
- Harden loop 1 (2026-10-10), the architecture that died: R4 as a silent per-host rebuild rung with the office free to pick which hosts each colocated ticket drains. The solver's path step 4, "a drained host is rebuilt from the current image. Hosts rebuilt after a CVE's disclosure don't carry it, so draining clears every finding on the host. The best use is the 96 payments and 120 checkout hosts with the most exposures", completed in one lookup (in_service_since equal to the latest accepted window), and its own note named the assumption it never tested ("the folder doesn't say which hosts the provider drains. I assumed the hosts with the most exposures go first"). Loop 1 attacks that assumption, not the rebuild.
- Stage 6 fix 1 (2026-10-10), the declared distractor `drain_orchestrator_config.yaml` carrying `rebuild_from: current_platform_image`: it was the only explicit statement of the decisive rebuild, so a declared distractor carried the decisive rung and the litmus line "no file states it" was false; key replaced by a neutral `drain_timeout_minutes`, slide 1 now cites the `in_service_since` identity.
- Stage 6 fix 1, a vendor advisory feed with one record per package (first_published taken from the first crew ticket seen, latest_revision 21 days later): two search tickets keyed a release date that equalled their package's latest_revision, a targeted re-dating moved the search card row to 27.0 days and 8 over (judge Gate C). A dictionary pin alone was rejected because the visible coincidence would still argue against it; the feed now carries one record per advisory, every crew date is exactly one advisory's first_published, and no crew date equals any revision date (asserted).
- Stage 6 fix 1, pinning the cloud ticket's hosts in the data dictionary: the dictionary is field semantics for shipped files and sits below the standard, whose s.3 ("below its fixed version") licensed every host with any open finding on the package (112 against 10 at rank 300); pinned in standard s.3 itself instead.
- Stage 6 fix 1, the close-out back-test as built in 3a: closed-finding CVEs could be published after their ticket's cut day, so 126 rows had no score on the cut day and the PDF's 891 did not recompute (801 on the exact cut-day score); the verifier hid it by taking the maximum score to date and asserting only that 12 cells existed. Now every closed CVE is published before its cut, CVEs are shared across hosts and estates, the verifier reads the exact cut-day score and matches all 12 printed cells.

- v2 (the ticket's reach), spent at the wave-1 re-root (2026-10-12): its decisive step read a filed rule (a ticket rides one change request and a request is for one window), which is rule application and banned as the decisive step; its strategy repeated task127's binding constraint; and IT patch remediation has no client-domain task type that serves Opportunity Sizing (business-operations-analytics maps only to general statistics, human factors and healthcare delivery), so the number re-roots in a new world.
- Draw candidate, seed DS04 (an arrears-outreach team placed by the overflow comparison, a hold): guard BLOCK on `ban.strategy` causal_design (task121), `ban.role` programme_officer, `ban.forum` board_of_directors and `ban.forcing_event` budget_or_appropriation (task124); its decisive step is causal identification, which this window bans.
- Draw candidate, a heat-health home-check service placed by summer deaths averted net of mortality displacement (epidemiology): guard BLOCK `test.same_puzzle_older` and `test.same_driver_older` against task122 v2; it is task122's borrowed-orders driver (an in-period gain partly borrowed from the weeks after, netted over the window) in other nouns, and an event study around the dated heat episodes shows the shortfall.
- Draw candidate, a home insurer's growth partnership sized by its marginal 1-in-200 annual loss (catastrophe accumulation): guard clean and the driver unused, but the appetite names the book's 1-in-200 and the catalogue's event key makes the joint a header-found join, so a cat-literate solver computes the joint tail by reflex and the call would land on most strong runs.
- Draw candidate, a pension fund's 2027 mandate with a short-history candidate rebuilt from factor exposures (quantitative finance): guard BLOCK `test.same_driver` (time, G16, method_or_model_selection) against task254 v2 and task446 v2, and the missing pre-launch months are found by the hygiene battery.
- Draw candidate, appraisal-smoothed returns de-smoothed before the risk budget: whether to de-smooth turns on reported against economic losses, which is a reading of the objective, so a fork on the main call.
- Draw candidate, a hidden population sized by capture-recapture for an outreach team: its honest strategy key is population_selection, banned against task124 in this window.
- Draw candidate, a yield per unit of effort projected against the stock already removed (depletion): no client-domain task type serving Opportunity Sizing has it as its standard method; in collections the liquidation curve is the standard and would be a competing defensible answer.
- This world as a dial (one older-dog book, five allowed increases): the result curve is flat at its peak (0.05 to 0.4 SEK million between the best two settings on a 2 to 5 SEK million gain), so another defensible lapse or cost model moves the argmax, a fork; re-cut as a designation set over five breed-group books, where the books' signs separate by about SEK 2.8 million or more on the prototype.
- The same world with leavers counted at the book's average cost but anti-selection carried by sales channel: that is seed DS27's mechanism; the build keeps captivity by an ongoing condition, rebuilt from claims, and no channel effect.
- First architecture-3 draw (2026-10-12, registered 08:52 and withdrawn): a Swedish pet insurer's five older-dog breed-group books, which take their indicated 2027 renewal increase, decided by pricing the dogs an increase sheds at their own claims cost (owners of dogs under treatment for a condition no other insurer covers stay, owners of healthy dogs leave). Guard BLOCK on `ban.strategy` composition_mix, `ban.pattern` G6 and `ban.forum` line_manager_or_team against task125 v2, registered thirty minutes earlier and ahead in draw order (the check ran before pulling it); no honest relabel exists, since the mechanism is a mix shift by selection (composition_mix or population_selection, both banned in this window); and its actuarial-science-insurance / pricing-ratemaking-credibility pair blocks task130 v4. Prototype arithmetic kept for a later window: with leavers at their own cost two of five books lose SEK 3.6 to 4.2 million on their increase while every shortcut keeps all five.
- Draw candidates on the way to architecture 3's second draw (2026-10-12): a hidden population sized by capture-recapture (population_selection, banned against task124), a depletion yield (no client task type has it as its method), the pet-insurance renewal world as a dial (a flat optimum, a fork) or carried by sales channel (seed DS27's mechanism); the second draw takes seed DS04's collections overflow into a bank.
- Over-capacity days from list size with a persistent partition order and mixed day types (Monday merges, the campaign cycles, capacity shocks), architecture 3 prototype (2026-10-12): the same-list estimators (day effects with and without the score, day-weighted means, Mantel-Haenszel, pooled, instrumental variable) spread 13 to 52 per cent on a centre's figure, so no rounding held every reasonable estimator in one bin; replaced by 19 business-day cycles (no merges), overflow only on the campaign cycles' collections days, a stratified extract order and hashed per-account draws.
- Day-level risk built so the pooled comparison over the over-capacity days became a rung (seasonal risk with Monday merges): it landed 25 to 30 per cent above the same-list figure, between the golden's bin and the funding line, a fork on the figures rather than a rung; the pooled comparison over the year's lists is the rung instead (R3), and within the over-capacity days pooling converges (SF11).
- Each centre's rolls graded to the nearest 50: London's estimator family spans 49 rolls, too wide for a 50 bin; graded to the nearest 100.
- The workforce log carrying the dialler's daily right-party contacts: the old dialler counted its arrangement code as a contact, so the column tied only under the golden's reading of the AR switch, an oracle for Ask A; the log carries seats, hours, records loaded and accounts dialled only.
- A new team rated at 560 dials a day: London's least overflow day (about 920 diallable records) left the cap binding by too little for the uncapped sizing to reach 1.3 times the bar; rated at 400, binding by 1.75 at the least.
- Golden arrangement totals tuned onto round hundred-thousands: a five-figure sum within a dollar of 7,000,000 reads tuned; each centre now sits 4,000 to 15,000 off its bin centre.
- The task123 extract register's column set (file, provided_by, extracted, rows, covers): `guard.py surface` promoted the pair on an identical column set; the register is now the bank's own (SEQ, OBJECT_NAME, SOURCE_SYSTEM, PULL_DT, RECORD_CT, SCOPE_NOTE) under the name CMI_EXTRACT_REGISTER_20261009.csv.
