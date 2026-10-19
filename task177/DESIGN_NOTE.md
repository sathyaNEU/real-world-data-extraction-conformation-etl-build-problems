# task177 design note

**Status: stage 4 round 1 fixed, waiting on the round 2 readers and the re-judge (2026-10-19), architecture 1 in a
new world.** Round 1 on target.zip 2c536aaa: the judge DETERMINISTIC / APPROVE (26.0, one rate 39.7, the trailing
13.7, every ask count); both scored readers missed the call (11 and 13 per cent) and kept 5 and 14 of the 24 ask
figures. The repair re-sited ask B's primary (the vendor's support desk in the staff console), made the widget's clock
move every month of ask A (employers' month-end filings), and filed release 4.0's resolution for every channel (plan
1.3), the judge's one weak fork; the call, the stump and every call-side figure are unchanged and asserted against the
judged pack (the J block in checks.py). The
seed FC48 world (drop-off recycling bins) died at stage 1 on measurement before any card was filed (its record is kept
below under `## Seed world` and in `## Tried and rejected`). The redraw was handed the cell psychology-behavioral-science
/ decision-making-computational-behavioral-modeling and searched it by prototype on 2026-10-19: goals as reference
points (A) and drift-diffusion speed-accuracy adaptation (E) died on measurement and on the library test, a dozen more
on paper, and the imposed-contact learning discount (F) held. Prototypes are in the session scratchpad (r177/proto).

## Draw

| Item | The draw |
|---|---|
| Card | `cards/task177.json`, registered at the DRAWN commit (e886198) through the round's serial lock |
| Pairing | `psychology-behavioral-science` (client domain), task type `decision-making-computational-behavioral-modeling` (serves Forecasting), objective Forecasting |
| World | Prairie Works Manitoba (fictional), a provincial employment and income assistance service; jobseekers on a claim check in every 14 days and ask questions in between, by calling the claimant line or through its digital assistant, Ask Prairie Works (app, web, and a voice service the claimant queue's overflow transfers calls to) |
| Decision | the March and April 2027 usage tiers for Ask Prairie Works, due on the vendor's order form by 8 January 2027 (`purchase_order_or_contract`); the head of contact services signs it (`line_manager_or_team`); the forecast comes from Digital Channels (`policy_adviser`) |
| Call | the share of the contacts that jobseekers on the register on 3 January 2027 start themselves from 1 March to 25 April 2027 that they start in Ask Prairie Works, after release 4.0 has answered every claimant-line call from 4 January to 28 February: **26 per cent** (whole per cent) |
| Shape | `02`, a forecast for the window after the assistant-first weeks; the criteria come from the call, its two components and the 24 monthly cells of the asks (employers' conversations and our own staff and test conversations in each month of 2026), with the two files |
| Decision type / unit | `quantity_figure` / `rate_or_share` |
| Mechanism | gap population then time; pattern none, decisive G16 (the learning model the record selects), G7 (the assistant-first window) and G17 (the profile interval) supporting; Gate G `method_or_model_selection`; strategy `forecast_method_backtest`; Layer 2 `forecast_uncertainty`, pattern `psychology-behavioral-science/decision-making-computational-behavioral-modeling/3` |
| Calibration / context artifact | none / other (the vendor's usage-tier order form; the rollout plan is the governing document that files the dates, the routing, the check-in and what a contact is) |
| Deliverables | `assistant_share_forecast_mar_apr_2027.xlsx`, `assistant_first_aftermath_note.docx` |
| People | Loretta Rodgers (head of contact services), Sabrina Ward (Digital Channels), drawn with `guard.py names --geo "Manitoba, Canada" --seed 177 --n 30` |

**Data-native sentence.** The claimant queue's overflow sends phone-minded jobseekers to the assistant only in a few
dozen Monday-morning episodes, so the record holds eleven thousand contacts a jobseeker did not choose but never a run
of them, and a learner fitted to the whole record, where they are one assistant experience in six, back-tests well
while weighing them like chosen ones.

**The library test.** The cell's cards are the textbook route: a reinforcement-learning model of each jobseeker's
contact-by-contact channel choices compared on held-out choices (card 1), its parameters recoverable (card 2),
simulated to check it reproduces the behaviour (card 3). Applied as the cards state it, with one learning rate, it
files 40 per cent. The judgment beyond the cards, which the data settle, is which experiences teach: a contact the
jobseeker was sent to by the overflow moves their later choices about a fifth as far as one they chose (the split
beats one rate by 1,419 log-likelihood units and "transfers teach nothing" by 93), and the assistant-first weeks are
made of such contacts. The judgment without the learning model (next-contact rates after transfers, a Markov chain
split by route) misses too; the two together give the golden.

**Measured on the pack** (`generator/checks.py`, 413,866 contacts, 11,154 transfers): the golden 26.05 (edge distance
0.45 of a point); one learning rate 39.99; transfers teaching nothing 20.10; no learning 13.64; transfers learned at
the chosen rate (clean truth) 41.08; a pooled last-four logistic 29.68; a pooled first-order Markov chain 30.39; a pull
to the last channel met 28.20 (133 log-likelihood units worse); contacts at each jobseeker's own 2026 rate with the
check-in ignored 23.99. The golden's family: 25.76 to 26.13 (a second simulation seed, starting values estimated,
fitted on the planning population only, fitted to 31 October, no overflow from 1 March, questions at each jobseeker's
own rate, claims closing at the register's rate); one standard error of the transfer rate either way 25.61 and 26.49.
On the clean truth: one rate 39.89, the split 25.95, the world's own expected window 25.81. The record selects the
learning model: fitted to January to October, the split predicts November and December's 68,677 choices better than
one rate by 382 log-likelihood units and better than every reduced form (a last-one, last-four or last-eight logistic,
transfers pooled or apart; a Markov chain, pooled or apart) by 1,419 to 3,763, while one rate still predicts their
share at 14 per cent against 14 observed.

**The world after the screen** (fixed before the pack was cut, each change recorded with its reason): outcomes are
recorded by each system (an adviser's wrap-up, queue abandonment, the voice session's end state) rather than derived
from repeat contacts, because repeats make the contact count depend on the outcome and the count model became a
forecast fork of about a point; contacts are the plan's fortnightly check-in plus questions at one rate, so the
window's contacts per jobseeker are known rather than forecast; the lean is common to every jobseeker and claims
close at one rate, so the planning population's own fit, the full fit and the closures converge; the world's draw
(d7 of eight, the one whose family spread was smallest at scale 1.5) and the acceptance count (2,041 of 2,400, set
by the re-centre rule: the family centred in its whole per cent) were fixed last.

**Guard (2026-10-19).** WARN only. `overuse.org_family`: a public employment service is honestly a government agency,
and no government-agency build on file turns on a learning model of its clients' choices. `repeat.gate_g` and
`overuse.gate_g` (method_or_model_selection): the decisive step is honestly the selection of a learning model the
record settles; task269's is a reliability decision study, another pairing, gap and generator. `test.same_puzzle_older`
and `test.same_driver_older` are answered by the card's differentiation lines (task70, task104, task134, task168,
task463, task501).

**Sources, one line each.** Cards 1 to 3 of the task type give the family and the default path's route, never the
stump (stumping 1.3). task501's driver pools two regimes and rebuilds a static matrix from the season's own days;
here that static rebuild is a wrong rung, and the imposed rate sits inside a jointly fitted learning model. task148
censors a latent patience; nothing is censored here. task137 is a contact-centre world on a repricing share; the
decision, organisation, country and driver differ.

## Default path

1. Rebuild each jobseeker's contacts: calls to the claimant line from `contact_legs_2026.csv` keyed by the case number
   on the call's first leg (legacy codes through `telephony_migration_codes.xlsx`), conversations in the app or on the
   web from `assistant_sessions_2026.jsonl` through the assistant accounts in `contact_details_crosswalk.csv`, each
   conversation's outcome its last session's end state, each overflow transfer's outcome its voice session's.
2. Fit the field's reinforcement-learning model of channel choice to every contact by maximum likelihood: one value
   per channel moved by one learning rate after every contact towards its outcome, a softmax with a lean and a pull to
   the last choice; fitted to January to October it predicts 14 per cent of November and December's own contacts in
   the assistant, against 14 per cent observed.
3. Take the jobseekers on the register on 3 January 2027 (`claims_register_2026.csv`) from their end-of-record state
   and simulate the plan's weeks: every call met by release 4.0 resolving 2,041 of 2,400 to 28 February, then the line
   back to advisers with the 2026 transfer share, check-ins every 14 days, other contacts at the 2026 rate.
4. Read the share of their own contacts started in the assistant from 1 March to 25 April.

Ends on: 40 per cent
Golden: 26 per cent

## Stump sentence

One learning rate fitted to every contact and simulated through the assistant-first weeks files 40 per cent; the
overflow transfers in the record, the only contacts a jobseeker did not choose, move their later choices about a fifth
as far as a conversation they opened, so eight weeks of release 4.0 answering their calls convert far fewer of them
and the share is 26 per cent.

## Three rules

Task type: decision-making-computational-behavioral-modeling in psychology-behavioral-science, which serves Forecasting & Predictive Modeling: a reinforcement-learning model of each jobseeker's contact-by-contact choices, fitted by likelihood, compared out of sample and simulated forward.
Domain test: the deciding quantity is how far a contact the jobseeker did not choose moves their later channel choice against one they chose, a learning rate for imposed experiences inside a fitted reinforcement-learning model, which is the free-against-forced choice distinction of the field's own learning studies.
Swap: with servers for jobseekers ("the share of requests a server pool sends to the new cache after eight weeks of forced routing") nothing learns from what it was sent to, the agency term has nothing to act on, and the forecast collapses to a routing sum.
Layer 1: the platform's leg export in UTC with the legacy platform's codes and merged IVR-and-queue leg before the 6 July cutover; the vendor's session export with no zone marker and conversations split into sessions; case numbers keyed in the IVR against assistant accounts through the case system's contact details, with changed and shared phone numbers; outcomes recorded three ways; the workforce team's overflow log beside the transfers; staff and test accounts in the export; claims opening and closing; each mishandled alone leaves the call at 26 (R2 in checks.py).
Layer 2: forecast_uncertainty, card 3 of the task type (the winning model must reproduce the behaviour): the learning model has to separate chosen from imposed experiences before it is simulated through a window made of imposed ones, and the record's 11,154 transfers settle the separate rate by likelihood.
Decisive step: estimating a separate learning rate for the contacts the jobseeker did not choose (the overflow transfers) inside the jointly fitted model, and carrying it to the assistant-first weeks' calls.
Not semantics: every field, code and definition read right (transfers identified, their outcomes linked, the plan's definitions applied) still leaves one learning rate fitted to every contact, which files 40 per cent; nothing in the pack says chosen and imposed contacts differ.
Not rule application: no filed rule or procedure says how an experience moves a choice; the plan files the dates, the routing, the check-in and what a contact is, and executing all of them with the textbook one-rate model files 40 per cent.
Analyst test: a strong analyst who rebuilds every contact, maps the codes, links the transfers' outcomes, fits a reinforcement-learning model with one learning rate by likelihood, checks it on held-out contacts and simulates the assistant-first weeks files an assistant share of 40 per cent for March and April, where the share is 26 per cent.
Estimand: the prompt files the population (jobseekers on the register on 3 January 2027), the outcome (the share of the contacts they start themselves that they start in Ask Prairie Works), the window (1 March to 25 April 2027) and the unit (a whole per cent); the rollout plan's 5.1 and 5.2 file what starting a contact is and that a conversation counts once.
No decoy: nothing is planted to be caught; no memo, draft, briefing, vendor estimate or stakeholder figure states a share, no file computes a forecast, and the acceptance test reports release 4.0's own resolution, a filed input every route uses.
No certified replay: no published or certified figure reproduces the method; the learning rates are recovered from the jobseekers' own records by likelihood, and no shipped figure is a function of them.
Lesson: an experience a person did not choose teaches them less than one they chose, so a period that imposes an option converts fewer people than a learner fitted to a record of mostly chosen experiences predicts; no build on file turns on a learning rate for imposed experiences.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| Contacts rebuilt across the two exports | plan 5.1, 5.2; dictionary | caller_entered, call_ref, conversation_id | yes | none | the joins | no | readable |
| One-rate learning model fitted and back-tested (card route) | none | none | the field's textbook | none | no | no | readable |
| The plan's weeks simulated with release 4.0's acceptance share | plan 1.3, 2.1 to 4.1; acceptance summary | none | yes | none | no | no | readable |
| (decisive) A separate learning rate for the contacts the jobseeker did not choose | none: the plan routes calls and never says what a transfer teaches | the transfer is a routing fact on the queue leg; nothing marks how much it teaches | one rate for every contact is the reflex | none: no file scores a model | no sweep reaches it | no: a jointly fitted rate, not a ratio of counts | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | contacts jobseekers start themselves | calls they make to the claimant line, conversations they open in the app or on the web | callbacks the service makes | same call (callbacks are not in the exports) | plan 5.1 |
| SF2 | starting a contact in Ask Prairie Works | opening a conversation in the app or on the web; an overflow transfer is a call | transfers counted as assistant starts | 27 | plan 5.1 ("on the phone by calling the claimant line") |
| SF3 | a conversation over several sessions | one contact, its last session's outcome | each session a contact | same call (26.30, R2) | plan 5.2 |
| SF4 | jobseekers on our register on 3 January 2027 | claims open that day | every claim in the register | another population | the prompt's date |
| SF5 | jobseekers joining after 3 January | not in the population | included | another population | the prompt's date |
| SF6 | the window's edges | Manitoba dates, 1 March to 25 April | UTC dates | same call (26.05) | converges |
| SF7 | what the assistant-first weeks route | every call reaching Claimant Services; the app as before | the app's conversations counted as imposed | another call | plan 2.1, 2.3 |
| SF8 | release 4.0's resolution | the acceptance test, 2,041 of 2,400 | the test's intents reweighted to the 2026 mix | same call (26.05) | converges |
| SF9 | the phone's resolution in 2027 | the 2026 record | July to December only | same call (26.07) | converges |
| SF10 | overflow after 1 March | the 2026 transfer share | none | same call (25.99) | plan 3.2 |
| SF11 | contacts in the window per jobseeker | check-ins every 14 days from the claim's opening, other questions at the 2026 rate | each jobseeker's own 2026 rate | 24 | plan 4.1 |
| SF12 | rounding | the unrounded share rounded once, halves away | rounding the weeks first | same call | the prompt's rounding sentence |
| SF13 | the order of a jobseeker's contacts | start times on one clock (legs UTC, sessions Manitoba time) | both read as one clock unconverted | same call (26.04, R2) | converges |
| SF14 | a call keyed by its caller | the case number keyed on its first leg | the caller's number through the contact details | same call (26.07, R2) | converges |
| SF15 | release 4.0's resolution of the conversations jobseekers open | the acceptance test's rate, as for calls | the 2026 assistant's rate (0.501) kept for the app and the web | 16 | plan 1.3 |
| SF16 | a transfer's outcome after 1 March | release 4.0 on the voice service at the acceptance rate | the 2026 voice service's rate (0.496) | same call (25.98) | plan 1.3; converges |

## Ladder

| Rung | Route | Figure (whole per cent) | Dies to |
|---|---|---|---|
| 0 | one learning rate for every contact, back-tested and simulated (the default path) | 40 | the split's 1,419 log-likelihood units; the transfers' own next-choice rates |
| 1 | no learning: the last eight weeks of 2026 carried | 14 | the 2026 series itself (35 per cent in January falling to 14) and the plan's weeks |
| 1 | transfers teach nothing | 20 | the record, by 93 log-likelihood units |
| 2 | a pooled last-four logistic, or a pooled first-order Markov chain, of the choice | 30, 30 | the held-out choices (November and December, fitted to October): 1,612 and 3,763 log-likelihood units behind the split |
| 2 | a pull to the last channel met rather than chosen | 28 | the record, by 133 units |
| 2 | each jobseeker's own 2026 contact rate, check-in ignored | 24 | plan 4.1 |
| 3 | (decisive) a separate rate for transfers, fitted jointly | 26 | the answer |

Worth: rung 0 sits 14 points above the golden, every other route 2 or more whole points from it; the golden's family
spans 25.76 to 26.13 and one standard error of the transfer rate 25.61 to 26.49, all printing 26. The reflexes split
both ways (no learning and teaching nothing below; one rate, the reduced forms and the wrong perseveration above), so
no single correction walks the default path to the answer.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | jobseekers with a claim open on 3 January 2027, nobody joining later | the prompt; SF4, SF5 |
| 2 Unit of account | a contact (a call, a conversation) | plan 5.1, 5.2; SF1 to SF3 |
| 3 Attribution window | a contact in the window by the day it starts, Manitoba time | the prompt; SF6 converges |
| 4 As-of dating | the record to 3 January 2027, the plan's dates after it | the exports' coverage (manifest), the plan |
| 5 Version basis | release 4.0 at its acceptance share on every channel; the phone as in 2026 | plan 1.2, 1.3, the summary; SF8, SF9, SF16 converge, SF15 ruled out |
| 6 Denominator | every contact the population starts in the window | plan 5.1 |
| 7 Weighting | contacts, not jobseekers | the prompt's "share of the contacts" |
| 8 Window length | the fit on the whole record | C3: fitted to 31 October or on the population only, same figure |
| 9 Boundary inclusivity | 1 March to 25 April inclusive; open on 3 January inclusive | the prompt; C1 |
| 10 Rounding path | once, at the end | the prompt; SF12 |
| 11 Tie-break | none arises | not applicable to a single share |
| 12 Maturity and censoring | claims closing in the window drop out | C3: closures at the register's rate, same figure |
| 13 Order of operations | the learning runs in each jobseeker's start-time order | SF13 converges |
| 14 Row order | file order irrelevant; contacts sorted by start | C1 |
| 15 Duplicate resolution | a conversation's sessions collapse to one | plan 5.2 |
| 16 Identity normalisation | case number keyed in the IVR; accounts through the contact details | dictionary; SF14 converges |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | contacts and shares | not applicable |
| 19 Code and status semantics | legacy and new codes, end states | `telephony_migration_codes.xlsx`, dictionary; never the stump |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | the plan's routing applies to the Claimant Services queue only | plan 2.1, 2.2 |
| 22 Forward window contents | the plan's weeks: release 4.0 on every call to 28 February, advisers from 1 March with the overflow | plan 2 to 4; the acceptance summary |

## Literal reader

The method is open and forced by the record: the reinforcement-learning family beats every reduced form on held-out
choices by 1,419 log-likelihood units or more, and inside it the separate transfer rate beats one rate by 382 held
out (1,419 on the whole record) and "transfers teach nothing" by 93. Executed word for word, the prompt fixes the
population, window, outcome and rounding, and the plan's 1.3 and 2.1 to 5.2 fix release 4.0's resolution on every
channel, the routing, the check-in and what a contact is; every reading the text leaves open (the window's clock, the
intents' weighting, the phone's period, the overflow from 1 March, a transfer's outcome after it, the fit's data, the
starting values, the closures) gives 26 per cent on the pack (SF6 to SF14 and SF16, the family rows in checks.py), and
the readings that do not (transfers as assistant starts, each jobseeker's own contact rate, the 2026 assistant's rate
kept for the conversations jobseekers open) each violate a quotable sentence of the plan.

## Oracles

- `overflow_episodes_2026.csv`: marks exactly the calls the legs mark as transferred (asserted); it confirms which
  contacts were imposed, never how much they teach, and ties under every reading.
- `vendor_invoices_2026.xlsx`: each month's billed tier band and the supplier's GST/HST number; the bands are too
  coarse to reconcile any count, so they tie under every handling of the asks' devices, and the number is ask B's
  referee for the second organisation in the staff console.
- `release4_acceptance_summary.pdf`: release 4.0's resolution, an input every route uses alike.
- `export_manifest.csv`: each file's coverage; it ranks nothing.
- None ranks the forecast or confirms a learning model.

## Ask sheet

**Main call's declared row population:** the claimant line's calls keyed with a case number (their legs in
`contact_legs_2026.csv`), the voice sessions their transfers met, the app and web conversations under accounts linked
to a case in `contact_details_crosswalk.csv`, the register, the plan and the acceptance summary. Device and hazard rows
in it: 0 (asserted, SEPARATION: no employer account and no account ever typed staff links to a case; the employer
widget's rows and the staff console's are their own channels). The round 1 repair touched none of it: the files the
call reads and no ask touches, and the call's own session rows, are the judged pack's byte for byte (J in checks.py).

**Ask A. For each month of 2026, the conversations employers held with Ask Prairie Works** (12 figures, whole
conversations). Golden: 945, 1,040, 1,555, 1,686, 1,850, 1,852, 1,660, 1,399, 1,838, 1,794, 1,799, 1,203.
- H18 home: a component of the March and April chat tiers the order commits to; employers' conversations ride the
  same tier as jobseekers'.
- Basis: the asking sentence (a conversation once, in the month it started, Manitoba time); plan 5.2.
- Primary A2 (D8 a clock against the month boundary, a per-source clock; silent): the employer portal's widget, built
  by the vendor's integration partner, writes UTC with no zone marker where every other channel writes Manitoba time.
  Employers' wage-subsidy claims fall due on each month's last day and many are filed that evening and into the
  night, so read as Manitoba time those conversations fall in the next month and every month moves, by 4 to 33
  (January -15, February -5, March -21, April +6, May +27, June -33, July +6, August -6, September +19, October +4,
  November -31, December +9). Fair: the widget's hours (employer conversations peaking at 15:00 to 17:00 read as
  local, and the month-end filings at 00:00 to 05:00 on the 1st) and the employer line's calls a few minutes after an
  abandoned conversation (UTC on the legs, the widget's own minute) show it. Silent: the dictionary describes started
  as when the session started, for every channel.
- A1 (D5 out-of-scope rows known only by structure, D9 totals invariant; found by both round 1 readers, so a hazard
  now): Digital Channels tests the employer portal under five test employer accounts registered to Prairie Works
  Manitoba's own business number (812447093, the customer's business number on the order form); counted as employers
  every month is high by 39 to 76.
- Hazards: sessions (a conversation reopened after a timeout keeps its conversation_id; plan 5.2 and the dictionary
  pin it).
- Stops (each a complete pipeline, `cracker.py`): natural 0 of 12; the business number found (both round 1 readers)
  0 of 12; the clock found 0 of 12; both found 12 of 12.
- Span: the session export, the order form, the employer line's legs, the dictionary, the plan (5 files).
- Realism: departments test their own portals under their own registration; an integration partner's widget logging
  UTC beside a vendor's local-time export is how mixed integrations really ship; claims due on a month's last day are
  filed that evening.

**Ask B. For each month of 2026, the conversations our own staff and test accounts held** (12 figures, whole
conversations). Golden: 1,256, 1,148, 1,326, 1,171, 1,163, 1,217, 1,332, 1,161, 1,224, 1,208, 1,252, 1,244.
- H18 home: the other component of the chat tiers; the vendor bills internal use like any other, and not its own
  support desk's.
- Primary B2 (D5 out-of-scope rows known only by structure, D9 a name agreement that lies; silent): Riverlot's support
  desk works in the tenant's staff console under seven accounts of its own (its daily checks, the days around each
  release, the cases the service raises), typed staff like ours. Ours carry Prairie Works Manitoba's business number
  in org_ref; the desk's carry Riverlot's (724906318, the supplier's GST/HST number on every invoice in
  `vendor_invoices_2026.xlsx`), on 572 of the console's 13,623 sessions. Counted as our staff, every month is high by
  29 to 71. Fair: the console carries two business numbers, the order form's customer and the invoices' supplier.
  Silent: the type is staff on every one of them, the dictionary describes org_ref for employer accounts only, and
  nothing else in the pack names the desk.
- B1 (D2 a label stored before a silent switch; one round 1 reader found it through the accounts' later staff rows,
  so a hazard now): the training team's practice accounts and Digital Channels' test accounts on the app and the web
  were created through the claimant sign-up and typed claimant until the vendor's release 3.4 re-typed them staff on
  14 September 2026; counted by type, January to September are low by 39 to 124.
- A1 shared: the test employers' conversations are our own test use, low by 39 to 76 in every month without it.
- Hazards: the staff console (staff all year), sessions against conversations.
- Stops: natural 0 of 12; the business number found (round 1 reader A) 0 of 12; the business number and every account
  ever typed staff (round 1 reader B) 0 of 12; the business number and the vendor's desk 3 of 12 (October to
  December); all three 12 of 12.
- Span: the session export, the order form, the invoices, the crosswalk, the dictionary (5 files).
- Realism: a vendor's support staff work inside a customer's tenant under their own organisation's accounts; a
  platform records each staff user's organisation; a type-only migration leaves the re-typed accounts without one.

**Hazard table:** sessions (both asks, every month, pinned); the employer widget's clock (ask A every month, by 4 to
33); the own business number (both asks, every month, 39 to 76); the vendor's support desk (ask B every month, 29 to
71); the re-typed accounts (ask B, January to September, 39 to 124).

**Referee:** the order form's business number (whose accounts the test employers and our console are) and the
invoices' supplier GST/HST number (whose the desk's are), the only records of either.

Pair ceiling: 28.5 (the cracker lands the call with every filed rule and both handlings the round 1 readers found,
and keeps 0 of 24 ask figures; the mirror, off the call with the business number, keeps 0 of 24; a cracker finding
the vendor's desk as well, or the widget's clock instead, keeps 12 of 24, a ceiling of 42.3)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/cracker.py

| Ask | Cracker sheet (every filed rule, recorded month, the business number, every account ever typed staff) | Hits | Verdict |
|---|---|---|---|
| Ask A, employers' conversations, twelve months | employer channel less the business number's accounts, recorded month | 0 of 12 | miss |
| Ask B, our own staff and test conversations, twelve months | console, accounts ever typed staff and the business number's employer accounts | 0 of 12 | miss |

## Leak sweep

`leak.py --asof 2027-01-04` on the round 2 pack: REVIEW, four lines, no LEAK (earlier sweeps of this pack's round 1
cut, taking their term list from earlier drafts of this note, returned the same kinds of line). Each, harmless:
- Sweep 3, January's employer count 945 appears in the rollout plan: it is the exchange of the claimant line's number
  (204-945-0100), not a count.
- Sweep 3, the rollout plan carries 8 of 10 words of the committed call: they are the plan's own nouns for the
  estimand it files (jobseekers, the register, contacts they start, March and April); the plan states no share, no
  count and no forecast for any window.
- Sweep 4, the acceptance summary carries window, routing and jobseeker: its test window, the assistant-first routing
  its voice conversations followed, and what jobseekers asked in 2026; it reports release 4.0's resolution only.
- Sweep 4, the prompt's question carries two terms of the note: they name what is counted and the routing the question
  conditions on, which the prompt has to state; neither names the learning model or the transfers.

## Seed world (FC48), set aside on 2026-10-18

**The seed world, as it stood.** Wave 8, new, Forecasting, seed FC48:
thirty unstaffed recycling drop-off points opened in December and January with 15 bins of 1,100 litres each
(ten on the coast, twenty in town, five of them in the Larchmere enclave round the lake), a July standard
(a point gets enough bins that its forecast July average weekly fill is at most 80 per cent of its bins),
weekly emptying logs carrying each bin's fill and any side waste, and a bin order due at the manufacturer by
15 March. The world, the decision and the quantity were kept; the seed's own mechanisms (the standard's "of
like demand" read as a filed method, the dashboard's district indices deciding as a decoy, a holiday-home
flag read off the property register) were set aside. Two decisive steps were screened on code, both forms of
the brief's comparison-group idea, and neither held. No architecture is live. This note holds the screen
record only; it carries none of the `precut.py` sections, because no design exists. The prototypes stay in
the session scratchpad (b177/proto).

**The structural sentence, and the first thing to read.** The graded object is a small sum of ceilings: at
each point the bins to add are the July fill over 0.8, rounded up, less 15, floored at nil, so a point that
will need 20 to 30 bins in July carries 5 to 15 of them in the answer and every per cent of error in its
July forecast moves its share of the answer two to three per cent. Each new point's forecast rests on its
own 10 to 13 winter weeks (about 2.5 per cent at a weekly noise of 8 per cent) and on its peers'
July-to-winter ratio, which runs 2 to 6 per cent apart from peer to peer within one kind of catchment. So
the right family's own members disagree by a median of 2.4 to 3.2 bins at a holiday point, which rules out
grading any point's bins, and the total moves 2.7 to 3.9 per cent under a redraw of the weekly noise. A bin
wide enough to hold the family with one sigma and a quarter-bin margin is a fifth to a third of the answer,
and at that width a flat summer uplift near the golden's own implied factor lands, along with the partly right
readings (the size or nearest-point peers, the half-term alone, the holiday points pooled). Thirty points
are too few for the lever this decision has against that noise.

**The registration finding.** The comparison-group step is honestly `composition_mix` (a district rate that
does not fit a point whose kind no column names, the kind rebuilt from the point's own winter history:
strategies F5, and task124 labelled a kind read from records the same way). task165 registered
`composition_mix` at 14:10 and task173 carries it in the queue, so the step could not be registered beside
either; `forecast_method_backtest` would have passed the guard and was not used. The window after task165's
registration (task201, task247, task165) also banned every honest forcing event, organisation and role this
world offers: the forcing event `season_or_peak` (task201, task247) and `purchase_order_or_contract`
(task165), the organisation `utility_or_infrastructure` (task201; a waste contractor running the network,
SIC 2007 section E) and `local_government` (task165), and the role `field_unit_lead` (task201, task247) and
`operations_director` (task165).

**The taxonomy finding.** The deciding quantity, each catchment's July population present against its
winter population, sits honestly in sociology-demography `population-estimation-demographic-projection` (F):
a seasonal population read from a symptomatic series, the waste itself, against catchments of like mix. The
literal home, urban-regional-science `municipal-service-demand-resource-allocation` (F), is task165's pairing
in the window.

**The repeat screen.** `guard.py recent`, `mechanisms --objective forecasting` and `slots` ran before any
card. `slots` on both candidate drivers, and on peers, analogs, summer, holiday, half-term, seasonality,
second homes, lets, owners, occupancy, cold start, like demand, comparable sites, seasonal index district,
summer uplift and drop-off bins, found no slot that spent a peer-seasonality or holiday-response mechanism;
the hits were words in unrelated notes. The closest card by mechanism is task124 (a unit's kind read from
its group's surviving records), the same family by its label.


## Tried and rejected

- **Candidate 1: peers read from each point's winter response to Christmas and the February half-term,
  three kinds of catchment** (residents, coastal villages with some lets, holiday cottages; the Larchmere
  enclave holiday cottages inside the Town district, the coast's villages and cottages mixed along the
  shore; prototypes `world4.py`, `p6.py`, `screen177.py`, whose output `screen177.out` is byte-identical over
  two runs; seeds 1 to 3 fixed before outcomes). Killed at stage 1 on measurement: the right family will not
  hold whole bins at any point, and at the width the total needs, a flat uplift and the partly right readings
  land.
  - The world: 140 mature points with two years of weekly emptyings (the Coast district 26 villages with
    some lets, 16 cottage sites and 12 residential estates; the Town district 76 residential villages and
    estates, 6 forest-lodge sites and 4 villages with some lets) and 30 new points opened 7 to 21 December
    (on the coast 5 villages, 3 cottage sites and 2 estates; in town 15 residential points and the five at
    Larchmere), the cottage points at 70 to 80 per cent of their 15 bins in an ordinary January week, the
    coastal villages at 60 to 73 and the residential points at 57 to 63. Weekly fill is the point's
    catchment (residents on a resident calendar with the Christmas packaging peak, holiday occupants on a
    school-holiday occupancy calendar) times a weekly noise of 8 per cent, with a 4 per cent summer factor of
    the point's own.
  - The golden (each new point's mean over its own weeks times the mean July-to-same-weeks ratio of its 8
    nearest mature points on the two winter responses): 153, 146 and 156 bins to add (truth 146, 144, 144).
    The right family (4 to 12 nearest, median, log and raw features, a silhouette-chosen k-means, local and
    quadratic regressions, the Christmas response alone, the whole weekly profile, a two-calendar
    decomposition, the true kind's mean) runs 135 to 157, 124 to 148 and 144 to 160, so -12 to +3 per cent,
    -15 to +1 and -8 to +3 of the golden; the k-means and the quadratic fit are the low members. One sigma
    over 12 redraws of the weekly noise is 4.4, 4.9 and 4.3 bins (2.8 to 3.3 per cent).
  - Per point the family spreads a median of 3.1 bins needed (3.11, 3.06, 3.15) and up to 5.8 to 6.3 at the
    non-residential points, against a whole bin, so no point's bins can be graded.
  - The reflexes, as shares of the golden: the district's own ratio -56 to -62 per cent, the dashboard's
    monthly index -56 to -62, every mature point's ratio -67 to -71, the 1, 3, 5 or 8 nearest points -55 to
    -69, a fit on distance to the coast -58 to -65, the Coast district's ratio borrowed for every
    holiday-looking point -36 to -44, the last July at the nearest point -78 to -83, a flat 1.25 -31 to -37, a
    flat 1.5 +33 to +34, a flat 2.0 +173 to +182, peers of like size -24, -30 and -4. The behavioural readings
    sit inside the family: the holiday-looking points pooled -12, -8 and -3, the top-ratio peers -1, +3 and +9,
    the half-term alone -5, -10 and -3. The decisive split is one obvious split (holiday or not), so it
    reads off the new points' own winter weeks once anyone looks.
  - The flat factor's total climbs about 40 to 46 bins per 0.1 and crosses the golden at 1.37 to 1.38
    (T(1.35) 145, 132 and 145; T(1.40) 166, 153 and 163), so 1.35 and 1.40 sit within 7 to 14 bins of it.
  - The back-test (each mature point forecast from its own winter 2025-26 against its July 2026, every other
    point as the pool) rejects the rivals by a visible margin: RMS log error 0.056 to 0.066 for the nearest
    peers on the two responses against 0.21 to 0.23 for the district, 0.26 to 0.27 for all points and 0.21 to
    0.22 for the three nearest points, and on the points whose kind is unlike their district 0.047 to 0.071
    against 0.43 to 0.46. Separation was never the problem.
  - Determinism at the total: rounding to 10, 20 or 25 bins, the family leaves the golden's bin in every
    seed but one (seed 3 at 25), and there one sigma breaks the quarter-bin margin; rounding to 50 holds the
    family and the margin in seeds 1 and 3 (in seed 2 the k-means leaves the bin), and puts the flat 1.35
    and 1.40, the pooled holiday points, the top-ratio peers and the half-term alone inside the golden's bin
    in every seed (and the size peers in seed 3).
  - The eda6c8c screens, as code on the clean truth: dispersion does not apply (a level; the July ratio's
    coefficient of variation within a kind is 0.031 to 0.036 for the cottages and 0.028 to 0.029 for the
    villages); variance-only passes (the golden is 2.28, 2.61 and 2.36 times the district route); the
    common-exposure subset, every filter and divide on a visible attribute (district, all points, nearest
    points, distance to the coast, size, the Coast district for the holiday-looking), misses by 24 to 71 per
    cent except the size peers in seed 3 (-4); truncation direction does not apply (overflow is logged as
    side waste and counted).
- **Candidate 2: the same reading with lets told from second homes** (the Larchmere enclave holiday lets;
  owner-used second-home villages on the coast and inland, emptier in winter and so steeper into July, as
  the lure a holiday-peer reading takes; the coast's new points lets and estates; same prototypes and seeds,
  the same output file). Killed at stage 1 on measurement for the same reason; the bracket it builds does
  not survive the width the noise needs.
  - The world: 148 mature points (the Coast district 30 villages, 14 let sites, 8 second-home hamlets and 12
    estates; the Town district 70 villages and estates, 10 second-home villages and 4 lodge sites) and the
    same 30 new points, the 13 holiday points lets. Lets fill at the half-term nearly as much as at Christmas;
    second homes fill at Christmas and hardly at the half-term (a winter response of about 3.3 to 3.9 at
    Christmas and 1.3 at the half-term, against about 2.3 to 2.5 and 1.9 to 2.1 for lets), so only the two
    responses together tell them apart.
  - The golden 236, 233 and 238 bins (truth 238, 231, 223); the family -5 to +2, -6 to +2 and -2 to +2 per
    cent of it; one sigma 8.9, 6.2 and 9.3 bins (2.7 to 3.9 per cent); per point a median spread of 2.4, 3.2
    and 3.1 bins needed and up to 4.6 to 7.9.
  - The bracket held in shape: the holiday-looking points pooled +28 to +39 per cent and the top-ratio peers
    +32 to +42 over the golden, the district -44 and the Coast district's ratio borrowed for the lake -31 to
    -33 under it. The rest: every mature point -48 to -52, the nearest 3 points -36 to -49, the distance fit
    -43 to -48, a flat 1.25 -41 to -43, a flat 1.5 +4 to +8, a flat 2.0 +100 to +103, the nearest point -53,
    -15 and -1, the size peers +3, -15 and -33, the half-term alone -1 to +1 (the back-test rejects it at RMS
    0.24 to 0.28, yet it lands on these new points, because none of them is a village or a hamlet).
  - The flat factor crosses the golden at 1.46 to 1.47, so 1.5 sits 4 to 8 per cent over it, inside any bin
    the noise allows.
  - The back-test: 0.057 to 0.065 for the nearest peers on the two responses against 0.35 to 0.36 for the
    district and 0.13 to 0.15 for the pooled holiday points, and on the off-district kinds 0.060 to 0.068
    against 0.62 to 0.64.
  - Determinism at the total: no rounding of 10, 20, 25 or 50 bins holds the family with one sigma inside a
    quarter-bin margin in any seed; inside the golden's bin sit a flat 1.45 to 1.55 at every rounding in
    some seed, the half-term alone at 10, 20 and 50 in every seed, the size peers in seed 1 and the nearest
    point in seed 3.
  - The eda6c8c screens: dispersion does not apply (the within-kind coefficient of variation is 0.022 to 0.040
    for lets and 0.044 to 0.063 for second homes); variance-only passes (1.77 to 1.79 times the district
    route); the common-exposure subset misses by 15 to 53 per cent except the nearest point in seed 3 (-1) and
    the size peers in seed 1 (+3); truncation direction does not apply.
- **The per-point requirement, measured on both.** Whole bins at each point need every defensible member of
  the family within a quarter-bin of the golden at 20 to 30 bins needed, about 1 per cent of the July
  forecast, which would take a within-kind ratio spread near 1 per cent and a weekly noise near 3 per cent:
  lockstep series. At the realistic 2 to 6 per cent and 8 per cent the members spread 2.4 to 3.2 bins.
- **The prototypes before the screen** (`p1.py` to `p11.py`) moved the parameters the same way and found
  the same wall: with the holiday points at 35 to 50 per cent of their bins in winter the totals were 30 to
  100 bins and one sigma 7 to 21 per cent; a beach-car-park kind made the two-response family split 62 to
  165 on one seed because a village's and a beach's winter responses coincide; a lets enclave among
  second-home lures with a mixed coast let the district route land by cancellation (the coast's villages
  over, the lake under).
- **Paper screens, not coded.**
  - The new points' ramp as households find them: FC04's station-maturity driver, task133's seed.
  - Each mature peer's July completed past its capacity from the peers that never overflowed: task168's
    driver.
  - The two Julys normalised for weather: a lever of 8 to 12 per cent on July fill, inside the bin the noise
    needs.
  - The school summer holiday's start: it falls within the same few days of late July in England in 2025,
    2026 and 2027, so no lever.
  - Deposits diverted from nearby mature points: the winter split carries into July, so no lever.
  - Dwellings times a kind's yield per dwelling: determinate per point only if every point captures the same
    share of its catchment, which is lockstep; with capture varying, the point's own winter level beats it
    out of sample.
  - The total July weekly fill in place of bins to add: a flat uplift lands, because the sum runs over the
    residential points too.

- **Redraw screen, 2026-10-19, candidate A: goals as reference points.** An activity-rewards programme raises
  its daily step goal (7,500 to 10,000) and pays a weekly reward for three goal-days (prototype `a_goal.py`,
  seeds 1 to 3, 3,000 members, 26 weeks, 13 forecast weeks). Killed on the library test and the round's G14
  ban. Truth 15,409, 15,150 and 15,762 weekly rewards (sigma 0.33 to 0.35 per cent); the share of weeks with
  three days at the new goal (default) -36.2, -36.3, -35.4 per cent; the current reward rate carried +78, +82,
  +76; the pile at the old goal read over every day (the card-literate route) -12.5, -12.3, -11.3 (stretch 0.44
  to 0.45 against 0.63 to 0.65 on days the reward was still in play, 32 per cent of days dead); the pile read on
  live days -2.4, -1.4, -0.8. The live-day rule leaves the forecast itself unchanged and fixes only the estimate
  of the stretch, an absolute split no column names (pattern E, G14); the band's carriage between two goal
  levels moves about 9 per cent on paper; the pile itself is what a card-literate reader looks for.
- **Candidate E: drift-diffusion speed-accuracy adaptation.** A selection test tightens its per-item limit
  from 10 to 6 seconds, an older 6-second version on another item bank in the record (prototype `e_ddm.py`,
  seeds 1 to 3, 2,000 candidates by 40 items, the 6-second boundary 0.75 of the unhurried one). Killed: at a
  70 per cent cut the truth passes 94.8, 95.4 and 93.8 per cent and truncating the current response times at
  6 seconds lands within 1.3, 0.8 and 1.4 per cent (mean accuracy 0.817 against 0.822: the slow responses
  truncation drops are the low-drift ones, so the totals coincide); only at a cut near the top does truncation
  miss (+26 to +29 per cent at a 0.75 boundary, +105 to +112 at 0.60), and there the lever is the DDM transport
  itself, the field's textbook route, on a tail share carrying 5 per cent relative noise; the old version timed
  out 1.9 to 2.2 per cent, so the censoring a careful fit adds is a negligible lever that card 3 catches.
- **Killed on paper the same day.** Hot-stove learning after an improvement (the card's learning model already
  updates only the chosen option, so the card lands; a lag-1 outcome logit sits near the golden over one
  quarter). Pooling titration answers whose offers followed the respondent's own earlier answers (the field
  scores each respondent's indifference point, which is the golden). Reference-dependent income targeting
  across a gig day (labour economics by taxonomy, as task157 found; a reduced form on own earnings lands;
  under 20 per cent on hours). A screener's criterion moving with prevalence (needs a gold-standard subsample;
  in range a regression on prevalence lands, out of range a fork). Every rate-by-state design carried to a new
  state mix (reference prices, the disposition effect, forgetting by gap, returns after a deferral, projection
  bias, streak breaks: honestly G14 or composition_mix). Notification habituation (task83's driver, rejected in
  task122's note). Peak-end follow-up (recognisable; lever about 24 per cent). Goal-gradient loyalty cards
  (lever about 4 per cent). Compromise and decoy menus (famous; past introductions land). The magnitude effect
  (amount as a covariate lands). Partition dependence in fund menus (the default fund dilutes it;
  identification only across employers). The description-experience gap in fare enforcement (past changes
  land). Bold against timid play under a stake cap (the pile at break-even plus a session simulation is the
  card-literate route, and players' time budgets reopen task148's censored-patience driver). A delivery promise
  as the reference point of learning (under 10 per cent on totals, a product-analytics home). A learner-share
  recruitment forecast (the analysis file's selection is a WHAT; a fatigue bend is G13).
- **F's own dead settings** (`f_forced.py`, `f_forced3.py`). With 1.4 imposed contacts per customer (six weeks
  at a contact a month) no learning lands within 1.4 per cent. With overflow on 6 per cent of contacts,
  redirects are 30 per cent of assistant experiences and the pooled reduced forms (a last-four logistic and a
  first-order Markov chain) cross the truth for imposed-to-chosen ratios of 0.25 to 0.40 (seed 1: -3 and -3 per
  cent at 0.35, -7 and -7 at 0.40); the draw keeps overflow at 2 per cent of calls (redirects about a tenth of
  assistant experiences) and the ratio near a fifth, where every pooled route misses by 10 per cent or more.
- **Stage 2 and 3 settings that moved the call when read another way** (measured on the d1 and d7 packs before the
  world was fixed; prototypes in r177/proto, g2 to g10):
  - Resolution derived from a repeat contact on the same topic within seven days: the contact count then depends on
    the outcome, and contacts simulated at each claimant's 2026 rate against repeats that follow failures moved the
    share about a point. Outcomes are recorded by each system instead.
  - Contacts at a gamma-distributed rate per claimant: each claimant's observed rate put the share 6.7 per cent under
    the truth (new claimants with no contact drop out, and a lucky count weighs a more phone-leaning state). The
    plan's fortnightly check-in fixes the window's contacts.
  - A lean spread across claimants (sd 0.4) and two claim lengths: the population-only fit, the full fit, the
    closures and estimated starting values spread 24.9 to 27.9 per cent. A common lean and one claim length converge
    them.
  - Scale 1.0 (9,000 claims open at the launch, 7,240 transfers): one standard error of the transfer rate moved the
    share 0.53 points and a fit to 31 October 0.55. Scale 1.5 brings them to 0.44 and 0.08.
  - 12 per cent of chat conversations split into sessions: counting every session as a contact moved the share 1.9
    points. At 1 per cent it moves 0.25.
  - Queue abandonment at 4 per cent: dropping abandoned calls moved the share 0.36 points. At 2.5 per cent it moves
    0.33, inside the bin.
  - Eight draws at scale 1.5: the family's farthest member 0.25 to 0.43 points from the golden, the pooled logistic
    1.3 to 2.6 points above it; d7 taken (0.28 and 1.95), the acceptance count then set to 2,041 of 2,400 to centre the
    family in its whole per cent.
  - The vendor first named Conversa Systems Inc., a word from real conversational-assistant firms (house fix H21);
    renamed Riverlot Dialogue Inc. before any reader saw it.
  - The write-up printing the fitted rates (0.398 and 0.078) and the gains to the unit: the transfer rate's estimate is
    0.07850, on the third decimal's rounding edge, the defensible fits put it at 0.077 to 0.079 and the chosen rate at
    0.397 to 0.398, and the teaching-nothing gain is 92.52. The write-up carries what every defensible fit shares (the
    transfers' rate about a fifth of the chosen rate, ratios 0.193 to 0.200; the gain over one rate more than 1,300 on
    the whole record, 1,419 with fixed starting values and 1,383 with them estimated); the workbook keeps the golden's
    own fit at two decimals.
  - Ask B's primary on the re-typed accounts (round 1, target.zip 2c536aaa): one reader collected every account that
    ever appears as staff and counted it staff all year (12 of 12 own-use months), and after the 14 September re-type
    those accounts read as staff anyway, so the other reader kept October to December. Re-sited onto the vendor's
    support desk in the staff console, which moves every month and which neither reader's path reaches; the re-typed
    accounts stay as a hazard.
  - Ask A's clock on the employers' ordinary evenings only (round 1): no employer conversation crossed February's
    boundaries on balance (31 January and 28 February both Saturdays) nor July's (30 June and 31 July crossing in equal
    numbers), and both readers kept those two months with the clock unconverted. Employers' month-end filings now move
    every month; of twelve draws of their own stream (a to l) only k moves every month by 4 or more, and k was taken.
  - The plan silent on release 4.0's resolution outside calls (round 1): the judge read 2.1 as filing the acceptance
    rate for the claimant line only, and the 2026 assistant's rate (0.501) kept for the app and the web files 16. Plan
    1.3 now files the planning assumption for every channel, the voice service's transfers after 1 March included
    (25.98 at the 2026 voice rate, the same call).
