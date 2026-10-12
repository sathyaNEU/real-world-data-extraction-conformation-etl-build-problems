# task449 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task449.json`, registered 2026-10-12 (guard WARNs three_rules.strategy_risk and repeat.gate_g, answered below).
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data Extraction & Conformation (ETL). The seed's world is complaint operations; of the ETL lane's six client task types only record linkage fits it, so the swap is of the method and the deciding quantity is the linkage field's own: a share estimated through linked records corrected for the links that are wrong.
- **Seed:** ET06 (`analytical_tasks/07_data_extraction_conformation/ET06_cfpb-complaint-taxonomy-break-change-point.md`), header and Situation only: a complaint-handling operation sizing permanent analysts against overtime after an industry event, from complaint data that includes the CFPB's. The seed's taxonomy-seam trap is data semantics and is not used as the decisive step; the pitfall is re-found from how the program's matters are tied to cardholder accounts.
- **Shape:** other. The call is one integer with three components (the sustained base, the failure's matters a week, the social care desk's share of them); the criteria come from two monthly series the committee reads beside the headcount (the matters open at each month end, January to September, charted, and the flex hours worked each month), each a device-carrying construction (arithmetic in the ask sheet). Shape 03 was dropped because the verified channels' bridge lines are exact for every response, and 04 because a headroom figure at every team size moves bin with the base estimator.
- **Strategy:** identity_resolution (the reliability of an entity link), decided as an estimate under false links, not as a match.
- **World:** Fenwright Contact Services runs the card complaint desk of Bellcroft Bank, a regional card issuer with about 1.6 million open card accounts, under an annual statement of work: a dedicated team billed per analyst-month and an hourly flex line (overtime and agency analysts). Bellcroft's ACH payment processor, Meridel Payment Systems, failed on 8 to 10 May 2026: cardholder payments made in those three days posted three to five business days late, late fees and interest were charged and some late payments were reported to the credit bureaus. Under Bellcroft's processing agreement, Meridel reimburses the handling of complaint matters arising from the failure, as the agreement's incident schedule defines them. Fenwright's workforce planning standard sizes the next contract year's dedicated team on the sustained base: the mean weekly new matters over the last eight complete weeks before the budget, less the matters arising from a processor or vendor incident, at 27.5 matters per analyst-week. Bellcroft's complaint steering committee approves the 2027 headcount with the program budget in October; the last eight complete weeks run from 3 August to 27 September 2026.
- **Forum and forcing event:** committee_or_panel (Bellcroft's complaint steering committee), budget_or_appropriation (the 2027 program budget). Organisation professional_services, role capacity_planner. Personas from `guard.py names --geo "United States" --seed 449`: Catherine Schneider (Fenwright's workforce planning lead), Stacy Fernandez (the social care desk lead).
- **Data-native sentence:** the failure moved about a quarter of the program's new matters onto the one channel whose account is a guess: from 18 May the social care desk opened a matter for each complaint post and attached the first cardholder the name-and-city search returned, so for a poster whose name and city match several cardholders the attached account is the poster's only one time in k and otherwise carries the portfolio's incident rate, not the poster's.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution 1 (propagate linkage error to the estimate; false links attenuate, missed links select; shortcut: links above a cutoff as truth): the false-link half, carried into a share read through an attached account, with each attachment's reliability set by how many cardholders share the poster's name and city.
  - `stumping/references/strategies.md` F10 (identity resolution: no hold, use it as Layer 1 or a lower rung): no identity is resolved here and no join is the move; every matter keeps the account the desk attached, and the decisive step is the estimate taken under that link's error.
  - `stumping/references/strategies.md` Part 6 (a move visible in the schema, a reflex correction): the matching count k is a column, but the move (inverting the dilution of the attached accounts' incident share) is no row predicate, and the reflexes (the verified channels' share carried over, every social-care incident-family matter counted as the failure's, social-care matters dropped) each land on a named wrong team.
- **Same-puzzle and abstraction:** the card was drawn with G3 (record versus operation) as the decisive generator, which repeated task101's gap, generator and decision type and task126 v1's gap, generator and Gate G; both are differentiated on the card. At build the decisive generator was put first as what it is, G17 (statistical rigor: the share estimated under link error), with G3 second for the record-versus-poster mess, which clears both collisions. Nearest drivers: task500 v2 (0.06, a change reaching untouched units through a household link), task109 v2 (compilation rules grouping rows), task1 (a per-segment conversion rate). Stripped of nouns, none reads a characteristic through a first-of-k link and inverts the dilution toward the population's rate.
- **Guard WARN three_rules.strategy_risk (identity_resolution):** the analyst test below reads every field (the account basis, the number of matching cardholders, the attached account) and applies every rule (the incident schedule to the matter's account, the planning standard's run rate) and still files the wrong team; the step that decides is an estimate under link error, not a reading or a rule.
- **Guard WARN repeat.gate_g (task448):** task448's Gate G is a coverage estimator's post-strata; here it is the estimator of a share read through attachments that are right one time in k. Same label, different mechanism.

## Default path

1. Take the case system's matters first opened in the last eight complete weeks before the budget month (Monday 3 August to Sunday 27 September 2026, Eastern), across the six intake channels: about 1,450 new matters a week (fixed at build).
2. Flag each matter that arises from the failure under Schedule 7: its problem code one of the schedule's four (a payment not posted or posted late, a late fee, interest, a late payment reported to a credit bureau) and the matter's card account, the account the case system holds for it, in Meridel's affected-payment file.
3. Subtract the flagged matters from the new matters: the sustained base, about 1,085 a week (fixed at build).
4. Divide by 27.5 matters per analyst-week and round up.

Ends on: 40 dedicated analysts for 2027 (a sustained base of about 1,085 new matters a week; fixed at build).
Golden: 35 dedicated analysts for 2027 (a sustained base of about 950 new matters a week; fixed at build).

## Stump sentence

The default path files 40 dedicated analysts because step 2 reads each social-care matter's incident status off the account the social care desk attached, the first of the k cardholders whose name and city match the poster's display name, which is the poster's own account only one time in k and otherwise an unrelated cardholder's, affected at the portfolio's 4 per cent; recovered from each attachment's one-in-k reliability, about four in five of the social-care matters in the schedule's problem families arise from the failure, the sustained base is about 950 new matters a week and the team is 35 (figures fixed at build).

## Three rules

Task type: General Statistics & Data Science / data-integration-record-linkage-entity-resolution, serving the ETL objective (six intake channels' matters, the social care desk's search records and the processor's affected-payment file conformed into the sustained base the standard sizes the team on).
Domain test: the share of linked records that carry a characteristic, when one class of links is right only one time in k, is what record linkage estimates under false links (the Lahiri and Larsen and Chambers corrections, or the subsample whose links are certainly right), not what the linked values say; with the correction replaced by the plain join of the attached account the sustained base rises by about 135 matters a week and the team from 35 to 40.
Swap: in General Statistics the swap is of the method: hand the same call to an analyst who treats the attached account as the matter's account and the deciding quantity, the name-and-city matters arising from the failure, comes out at about 107 a week against about 240; without the linkage-error estimate there is no sustained base to size on, so the call does not survive the swap.
Layer 1: six channels' matters in one register with their own source references; the social care desk's search records in JSON lines with UTC post times against the register's Eastern opening times; account references in two formats across the register and Meridel's file; returned and re-presented payments in Meridel's file; the complaint code list against Schedule 7's four codes; a status history in which a reopened matter keeps its number; Fenwright's time records carrying other programs' overtime; two staffing agencies' timesheets in their own layouts (inventory below).
Layer 2: false links attenuate: a name-and-city matter's attached account carries the poster's own status with weight 1/k and an unrelated cardholder's at the portfolio rate otherwise, so the share arising from the failure is estimated from the links that are certainly right (a search that returned one cardholder) or by inverting the dilution, never read off the links or imputed from the matters whose posters chose to verify.
Decisive step: estimating, for the social care desk's name-and-city matters under Schedule 7's four codes, the share whose poster's own account had an affected payment, from the matters whose search returned one cardholder (or by inverting each attachment's one-in-k reliability against the portfolio rate), and carrying that share to every such matter; nothing filed names the share, the dilution or the subsample.
Not semantics: every field read right (account_basis NAME_CITY means the account came from a name-and-city search, results_returned is how many cardholders it returned, the attached account is the first returned) still leaves the number of those matters arising from the failure to be estimated; the analyst who reads all of it and keeps the attachment as the best link there is files 40, and the one who imputes from the verified social matters files 34.
Not rule application: Schedule 7 defines a covered matter by the cardholder's own account and the standard deducts covered matters; no filed rule or procedure says how a matter whose cardholder's account is uncertain is counted, so executing every rule leaves the estimate open, and the default and imputation paths both execute every rule and file wrong teams.
Analyst test: a strong analyst who conforms the six channels, joins the social care desk's search records, applies Schedule 7's four codes and affected-payment test to each matter's attached account and divides by the standard's 27.5 matters per analyst-week files 40 dedicated analysts (a base of about 1,085); one who distrusts the name-and-city attachments and carries over the verified social matters' share files 34 (figures fixed at build).
Estimand: the standard's sustained base, the mean weekly matters first opened in the eight complete weeks (Monday to Sunday, Eastern) before the month the budget is set, less the matters arising from a processor or vendor incident as the incident's agreement defines the matters it covers (Schedule 7: a complaint under one of four codes made by a cardholder whose account had an affected payment); filed in Fenwright's workforce planning standard WPS-3 (sections 3 and 4) and Schedule 7 (section 7.2).
No decoy: no document, memo, figure or stakeholder carries the wrong team or base; the operations log holds no counts; no filed sentence tells the analyst to read the attached account as the cardholder's.
No certified replay: no closed or certified figure blesses the attachment join or the imputation; neither Meridel's file nor the portfolio report ties to anything under one handling only.
Lesson: a characteristic read through an uncertain link is diluted toward the population's rate, so it is estimated from the links that are certainly right or by inverting the dilution, never read off the links or imputed from the members who chose to verify; the builds on file count under linkage probabilities (task253) or complete a list's capture (task448), and none corrects a linked attribute for false links.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the attached account taken as the cardholder's (default) | the dictionary says a name-and-city account is the first cardholder the search returned | the account sits on the matter | yes (join the account) | no | no | no | readable |
| R1 every name-and-city matter under the four codes counted as the failure's | no | no | yes (when in doubt, count it) | no | no | no | readable |
| R2 the verified social matters' share carried to the name-and-city matters | no | account_basis splits them | yes (impute from the verified) | no | no | one ratio | readable |
| R3 every verified channel's share under the four codes carried over | no | account_basis | yes (impute from the verified) | no | no | one ratio | readable |
| R4 (decisive) the one-match links' share (or the inverted dilution) carried to every name-and-city matter | no: no document names a share, a dilution, a subsample or a correction | no: results_returned sits in the social desk's JSON search records, reached only through the post-to-matter join, and a filter on it gives a share, not the base | no: every reflex (join, count all, impute from the verified) lands wrong | no control scores the share | the battery does not find it | no: a construction (join, estimate, carry, deduct) | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | arising from the failure | Schedule 7's covered matter: one of the four codes, made by a cardholder whose own account had an affected payment | (a) the matter's attached account in Meridel's file; (b) any complaint about the failure, the cardholder's account aside; (c) only matters Bellcroft can claim (a confirmed account) | (a) is the default path's method, not a reading: 40; (b) and (c) move the base (asserted) | Schedule 7 section 7.2 ("made by a cardholder whose account"); the dictionary (a name-and-city account is the first search result); WPS-3 deducts the matters the agreement "covers", and claims are section 7.4 |
| SF2 | new matters | matters first opened in the week; a reopened matter keeps its number and opening and is not new; a duplicate merged into another is not new | REOPENED events counted as openings; merged duplicates counted | reopens: base up, a wrong team (asserted); merged duplicates: same call, same bins (asserted) | WPS-3 section 2 |
| SF3 | the eight weeks | the eight complete Monday-to-Sunday weeks before the month the budget is set: 3 August to 27 September 2026 | the eight weeks to the pull (to 4 October) | same call, same bins (asserted) | WPS-3 section 3.1; the budget month in the ops log |
| SF4 | the week's clock | the matter's opening time in Eastern time | the social post's UTC creation time | same call, same bins (asserted) | WPS-3 section 3.1 (Eastern); the register's opened_at |
| SF5 | affected payment | a payment Meridel received 8 to 10 May 2026 that posted late; a returned payment never posted | returned payments counted | same call, same bins (asserted) | Schedule 7 section 7.1 |
| SF6 | rounding | the team is the ceiling of the unrounded base over 27.5; the base and the failure's matters a week rounded once to the nearest 10 | the base rounded before dividing | same call (asserted) | WPS-3 section 4.2; the prompt |
| SF7 | the estimator | the one-match share carried to all name-and-city matters under the four codes | the dilution inverted against the portfolio rate; the posterior sum; a regression on 1/k | same call, same bins, the share within half a point (asserted) | C1 |
| SF8 | the portfolio rate | affected accounts over open accounts at 30 April 2026 | open accounts at 31 May; payments in place of accounts | same call, same bins (asserted) | C3: the inversion's base moves under 1 a week across the range |
| SF9 | the mean | total over the eight weeks divided by eight | mean of the weekly counts | identical | arithmetic |
| SF10 | the four codes | PAY-01, FEE-01, FEE-02 and CRB-01 as Schedule 7 lists them | every code in the code list's payments, fees and credit-reporting families | same call, same bins (asserted) | Schedule 7 section 7.2 |

## Ladder

As built; `generator/checks.py` asserts every rung by name and `verify.py` recomputes the golden from the bundle alone.

| Rung | Method | The failure's matters a week | Base | Team | Dies to |
|---|---|---|---|---|---|
| R0 (default) | the attached account as the cardholder's | 366.5 | 1,083.1 | 40 | the one-match matters, whose attachment is right: 80 per cent (478 of 597) carry an affected payment, against 36 per cent of all 2,395 name-and-city attachments |
| R1 | every name-and-city matter under the four codes | 559.5 | 890.1 | 33 | a fifth of the one-match matters carry none |
| R2 | the DM-verified social matters' share (0.887) carried | 525.5 | 924.1 | 34 | the posters who verify are the ones after a refund; the one-match matters show 80 per cent |
| R3 | every verified channel's share under the four codes (0.617) carried | 444.8 | 1,004.8 | 37 | the phone and digital matters' mix is not the social posters' |
| R4 (golden) | the one-match share (0.801; the inversion 0.799, the regression and posterior 0.800) carried | 499.8 | 949.8 | 35 | none |

- **Separation.** Five rungs, five teams (40, 33, 34, 37, 35); R0 and R3 above the golden, R1 and R2 below.
- **Margins.** Every rung's base sits 10 or more matters a week inside its team's bin (asserted); the golden's 949.8 sits 14.8 above 935 and 12.7 below 962.5, and 4.8 inside its nearest-10 bin.
- **Worth.** The decisive move takes the name-and-city matters arising from the failure from 106.4 a week (R0) to 239.7; R2 and R3 put them at 265.5 and 184.7.
- **Grid.** Two choices: correct the name-and-city attachments or not, and whose share stands in (the one-match links, the inversion, the verified social, all verified, none, all counted). Every cell but one-match or inversion files a wrong team (asserted). A partial correction lands wrong too: the share from searches returning one or two cardholders (0.664) files 37.
- **Dominance.** The golden's share and R2's differ by 0.086 over 299 matters a week (25.7 a week, asserted 20 or more); R3's by 0.184 (55.1 a week); each moves a bin.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | matters first opened in the window on any channel; the deduction's members are the cardholders' own covered matters, the name-and-city matters with an unknown cardholder account included | WPS-3 section 3.1 and Schedule 7 section 7.2; SF1, SF2 |
| 2 | Unit of account | one matter (one cardholder's complaint about one problem) | WPS-3 section 2; the register's grain |
| 3 | Attribution window | the matter's first opening, Eastern, Monday to Sunday | WPS-3 section 3.1; SF4 C1 on the post's UTC time (asserted) |
| 4 | As-of dating | the register and status history as pulled 9 October 2026; a later reopening keeps the opening date | the manifest; SF2 |
| 5 | Version basis | Meridel's affected-payment file as delivered once | not applicable: one delivery, no revision |
| 6 | Denominator | eight weeks | SF9 identical |
| 7 | Weighting | one share over all name-and-city matters under the four codes in the window, pooled over weeks | C1: the one-match share, the inversion and the posterior sum agree (asserted) |
| 8 | Window length | eight weeks | WPS-3 section 3.1 |
| 9 | Boundary inclusivity | Monday 00:00 to Sunday 23:59:59 Eastern | C1: the matters within an hour of either edge, counted either way, keep the bins (asserted) |
| 10 | Rounding path | the team from the unrounded base; the base and the failure's matters a week rounded once | WPS-3 section 4.2; the prompt; SF6 |
| 11 | Tie-break | none needed | the base 12 or more inside its bin (asserted) |
| 12 | Maturity and censoring | a matter opened in the window counts at its opening whatever happened after; every matter carries its code from opening | the register's grain; SF2 |
| 13 | Order of operations | conform, join the search records, apply the four codes, estimate the share, deduct, average, divide, round up | C4: the share estimated over every name-and-city matter before the code filter files a wrong team (asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a merged duplicate is not a new matter | WPS-3 section 2; SF2, neutral (asserted) |
| 16 | Identity normalisation | account references BCF plus twelve digits in the register, fourteen zero-padded digits in Meridel's file | every affected account matches once normalised (asserted); semantics, never the stump |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | matters for the call; hours in Ask A | Ask A's ledgered device only |
| 19 | Code and status semantics | Schedule 7's four codes; account_basis; dm_verified | dictionary semantics, never the stump |
| 20 | Integerisation | the estimated count is not an integer; the base is rounded once and the team rounded up | SF6 |
| 21 | Clause scope | WPS-3's deduction covers every channel; Schedule 7's definition covers every matter and its claims clause only claims | SF1 |
| 22 | Forward window contents | the 2027 team is sized on the window's sustained base because the incident's matters will not recur (WPS-3's own reason) | WPS-3 section 3.2 |

## Literal reader

Executed word for word, WPS-3 fixes the matters (first opened in the eight complete Eastern weeks before the budget month), the deduction (matters arising from a processor or vendor incident as the incident's agreement defines the matters it covers: Schedule 7's covered matters, one of four codes made by a cardholder whose account had an affected payment), the rate and the rounding up. For a name-and-city matter the dictionary says the attached account is the first cardholder the search returned, so the literal deduction asks whether the poster's own account was affected, which no field holds: how that count is made is HOW, and the records force it (the one-match matters' share, the inverted dilution and the posterior sum agree, asserted). The wrong teams come from easy methods on the same literal quantity (the attachment read as the cardholder's account, the verified share imputed), never from another reading.

## Oracles

None. No shipped figure ties to the base, the failure's matters or the share: the operations log holds no counts, the portfolio report gives open accounts only, Meridel's file lists payments, the complaint-line call volumes (a distractor) count calls, and the CFPB's public extract (a distractor) counts complaints by the CFPB's own dates.

## Ask sheet

**Ask A: flex hours by month.** Figures: the flex hours worked on the desk in each month from January to September 2026, Fenwright analysts' overtime and agency analysts' hours together (nine, nearest 10). H18 home: the flex line the committee approves beside the dedicated team, an input reconciled to the statement of work's flex definition. Use: the committee sets the 2027 flex line with the headcount. Construction: Fenwright's overtime segments on the Bellcroft program from its time records, and each agency's hours from its timesheets, in the month worked. Primary device: D3, units set per source: Treadwell & Oake's timesheet export writes a shift's hours as hours and minutes after a point (7.45 is seven hours and forty-five minutes) while Marlowby Staffing and Fenwright write decimal hours; only the start and end times on the same rows, and the absence of any Treadwell fraction above .59, show it, and the naive sum runs 14.9 to 25.7 hours low every month. Hazards: overtime Fenwright analysts worked on another client's program (the program code, seen); one Marlowby week re-sent inside a later export (exact duplicate rows, seen). Path: Fenwright's time records, both agencies' timesheets, the statement of work excerpt, the field dictionary, the manifest, the operations log (seven files, eleven columns). Stops: Treadwell's hours read as decimals (every month low), other programs' overtime kept (January, March, July and August high), the re-sent week kept (June high by 490), the golden. Realism: staffing platforms export hours and minutes with a point as often as decimal hours, and an agency booked for evening coverage all year bills every month.

**Ask B: matters open at each month end.** Figures: the matters the desk had open at the end of each month from January to September 2026 (nine, nearest 10), charted in the memo. H18 home: the capacity case, the backlog the dedicated team carries. Use: the committee sees the surge's backlog and its fall. Construction: each matter's open spells from the status history (opened, closed, reopened, closed again), counted at 23:59 Eastern on each month's last day. Primary device: D8, an anchor on the current record: the register's closed_at is a reopened matter's latest closure, so a matter closed, reopened and closed again reads as open through its closed spell; only the status history shows the spell (the naive count runs 64 to 326 high every month). Hazards: duplicates closed on merging (status MERGED, seen); matters opened before 1 October 2025 were worked to closure in the previous system (the manifest's coverage line, seen). Path: the register, the status history, the dictionary, the manifest, the operations log (five files, nine columns). Stops: the register's opened and closed times (every month high), the golden. Realism: case systems keep one closed date on the matter and the history in an audit table.

Main population zero-counts (asserted): the main call reads no timesheet, no time record, no status history and no closed_at (deleting them moves nothing); no Treadwell row and no reopened spell enters the main call's computation; the two asks share no file with a device.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, nine monthly flex-hour figures | sums the hours columns as exported (Treadwell's hours and minutes read as decimal hours), after dropping the re-sent week and other programs' overtime: every month 14.9 to 25.7 hours low (790, 670, 760, 720, 3,430, 4,120, 3,440, 2,830, 2,170 filed as 770, 660, 740, 700, 3,410, 4,100, 3,420, 2,810, 2,150) | miss |
| B, nine month-end open counts | counts matters opened by the month end whose closed_at is later or blank: every month 64 to 326 high | miss |

Mirror leakage: 5 per cent (the mirror, stopping at R2's 34, makes the cracker's ask errors and keeps one chart criterion, the chart's layout, of about 21 ask-side criteria).

Pair ceiling: 33.5 (planning weights 38 / 7 / 55 with the call and its two components as the main block and r = 5; the cracker keeps the main block and one chart criterion, 38 + 7 + 55 x 1/21 = 47.6; the mirror keeps r, instruction-following and the chart criterion, 5 + 7 + 2.6 = 14.6; (47.6 + 14.6) / 2 = 31.1, plus 2.4 for a second chart criterion either may keep).

Criteria: the call, the base, the failure's matters a week, the social care desk's share (a critical component), nine month-end figures, about three chart criteria, nine monthly flex figures and two files: about 27.

## Layer 1 inventory

| Item | System | File | Mishandled | Effect (to assert) |
|---|---|---|---|---|
| six channels, six source-reference formats | the case system's intake | the register | references read as matter ids | none: the register's matter number is the key |
| social posts' UTC creation times | the social platforms' API | the social care export | the week taken from the post time | same call, same bins (SF4) |
| nested search records in JSON lines | the social care tool | the social care export | flattened without the search block | the decisive step needs it; no main mess |
| account references in two formats | Bellcroft's account system and Meridel's | the register, Meridel's file | joined raw | zero matches, loud; normalised, every affected account matches |
| returned and re-presented payments | Meridel's ACH processing | Meridel's file | returned payments kept | same call, same bins (SF5) |
| complaint codes against Schedule 7's four | the desk's code list | the code list, the register | whole families taken | same call, same bins (SF10) |
| merged duplicates | the desk's merge step | the register, status history | counted as new | same call, same bins (SF2) |
| reopened matters keep their number | the case system | the status history | REOPENED counted as new | a wrong team (SF2, ruled out by WPS-3) |
| other programs' overtime | Fenwright's time system | the time records | kept | Ask A only (hazard) |
| re-sent agency week | Marlowby's export | Marlowby's timesheets | kept | Ask A only (hazard) |

## Pre-ship check

- **Three rules.** Domain: the record-linkage estimate of a share read through links that are right one time in k (the client's pattern: propagate linkage error to the estimate), the swap of method moving the team from 35 to 40. Two layers: the inventory above, every item what the case system, the social care tool, Meridel, the time system or an agency writes, and the false-link correction. Decisive step analytical: on the clean truth the default path files 40 and the decisive step alone 35, each lower single correction stays wrong (R3a and R3b asserted).
- **Gates.** 17 files in 4 formats (csv, jsonl, pdf, xlsx); the status history at 159,488 rows and the register at 77,145; two distractors (the complaint line's weekly call statistics and the CFPB's public extract) whose deletion moves nothing; 94 checks; `verify.py` PASS from the bundle alone; two builds byte-identical; `figures_check.py` exit 0; `leak.py` REVIEW with no LEAK; `guard.py surface` with no promoted pair; `heart` WARN (the two answered in Draw).
- **Realism.** Week counts all different; month-end and flex figures tuned into their bins by moving closures within three days of a month end and overtime quarter-hours, never by changing a matter; the 2026 team (32) is the standard's answer on the pre-failure base; the other client renamed from a name one letter off a real brand; the dictionary and folder contents laid out apart from task448's.

## Leak check

- `leak.py` REVIEW with no LEAK: the planning rate filed in WPS-3, contract and standard vocabulary; an IVR column renamed to the telephony report's own headers (ASA, AHT) after the first sweep.
- Reader, one isolated pass on the stage 4 pack: questions 1, 2 and 4 none; question 3 named the operations log's 18 May entry as a staged hint (reworded to the practice change alone, and the log given its ordinary entries); question 5 executed WPS-3 3.1 and 4.2 with Schedule 7 7.1 and 7.2 as the estimand and named Schedule 7 7.4's confirmed-account wording as a possible reading (SF1, asserted: WPS-3 deducts the covered matters of 7.2, 7.4 governs claims); question 6 analytical when the name-and-city matters are estimated, and flagged the account join as unstated (the dictionary now gives both formats). Realism tells fixed: the CFPB extract no longer matches the register's CFPB count (its own range from January 2025, unpublished complaints left out), the operations log's entries. Full read in `leak_check_report.md`.

## Determinism judge

- Pass 1 (2026-10-12): DETERMINISTIC, FIX_NOW on hygiene alone: Marlowby's export id for the placement's last week postdated the pull (fixed: sent the day after the placement ended, asserted against the folder contents' date). All six committed answers reproduced (500, 950, 35; the month-end counts; the flex hours); the competing routes the judge ran file 40 (attachments at face value), 44 (confirmed accounts only), 53 (no deduction), and 34 (inversion with a zero portfolio rate, ruled out by the portfolio file). Gate G statistical_rigor, analytical_non_defect, sole_data_defect no (borderline note: on clean attachments the call reduces to a join); Gate H domain pass, layers pass, decisive step analytical. Report: `determinism_check_report.md`.

## Tried and rejected

- 2026-10-12, draw 1 (never registered): counting new matters as the expected number under the matching engine's probabilities (the sum over contacts of one minus each contact's match probability) instead of the engine's link decisions or a cutoff. Rejected before registering: the lesson, count by summed posterior probabilities rather than by classified decisions, is task253's (shipped 10-12), and a model that learned it solves this unchanged.
- 2026-10-12, draw 1 alternative: continuations hidden among contacts the engine cannot link, imputed from the linkable contacts of the same channel. Rejected: a capture rate measured where both observations exist and carried within strata is task448's driver, by the same author one build earlier.
- 2026-10-12, draw 1 alternative: new matters overstated just after a vendor transition because the matcher's history starts there, corrected by the previous vendor's closures and a time-to-return distribution. Rejected: a pool held outside the register sending inflow by a hazard since an event is task134's driver.
- 2026-10-12, draw 1 alternative: coincidental joins growing with the number of candidate matters searched (the database-search effect), separated by the join rate's dependence on block size. Rejected: the own predecessor sits inside every continuation's block, so the continuation share and the coincidence rate are not separately identified without a model the files would have to state.
- 2026-10-12, draw 1 alternative: social-care matters re-attributed to an affected same-name cardholder because the complaint's subject points to the writer. Rejected: the roster join on surname and ZIP is visible in the schema once the tie-break is filed, which makes the decisive rung readable.
