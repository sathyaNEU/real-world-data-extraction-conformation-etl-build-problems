# task249 design note

## Draw

Card `cards/task249.json`, architecture 4 (v1 to v3 in lineage), re-rooted 2026-10-19 at the author's request: after
architecture 3 was spent at stage 4, four candidates were written (handoffs/perssathya.md) and the author chose the
first, Product Analytics on a browser's cookie cap. Verdict: WARN, no BLOCK. Each WARN, answered: repeat.gate_g and
overuse.gate_g (method_or_model_selection, after task269 v2 and in 7 of the last 12): it is the honest label, the
decisive step chooses the comparison pool a replayed rule is applied to; statistical_rigor alone is not legal and no
other mechanism is true of this step. The structural tests are differentiated in the card against task233 (v1, v2),
task458, task256, task262, task267, task465 and task54, each a transported or conditioned rate with another
mechanism. The axis bans were redrawn once before filing, and each replacement is the truer label rather than merely
the passing one: the forcing event from launch_or_rollout (task268) to period_close, because what forces the call now
is the fourth quarter's close (the kit quotes the quarter just closed), not the kit's printing; the decisive pattern
from E to none with G14 first, because G14 (does the pooled rate apply to this pool) is the move itself and pattern E
is G14's own form. Nearest driver 0.04.

- **Pairing.** Product Analytics / metric-definition-measurement-science, a task type serving Data Quality
  Monitoring, the lane's least used cell (two builds). The object is the health of a published audience metric, each
  local edition's monthly unique browsers counted by the analytics tag's cookie; the call is a monitoring decision:
  which editions' figures go into the 2029 media kit with the measurement note the group's audience policy requires
  when a figure overstates the edition's browsers by more than a quarter.
- **The seed.** DQ22 gave only the objective (which monitored units fail a quality tolerance); its world and its
  pitfall are not carried.
- **Niche.** A German regional newspaper group publishes twelve local editions on one website with a metered
  paywall: five metered articles a calendar month free, then a registration wall for a free reader account; print
  subscribers activate digital access with their subscriber number. The analytics tag keeps its identifier in a
  first-party cookie written from the page's script and refreshed on every page view. WebKit browsers (Safari on a
  Mac, and every browser on an iPhone or iPad) shorten a script-written cookie to seven days from its last write, so a
  reader who comes back after more than seven days arrives with a new identifier and is counted again that month. The
  paywall keeps its meter in the same kind of storage.
- **The call.** Which editions' average monthly unique browsers for October to December 2028 carry the measurement
  note in the 2029 media kit (the policy's tolerance: the reported figure above the edition's browsers by more than
  25 per cent).
- **Shape.** 10, a scorecard: the twelve editions against the tolerance (the list of eight, the four without, the
  count), and two figures the kit quotes for every edition from systems the call never reads (24 ask figures): 38
  criteria or more. Only the set and the count are graded on the call: the licensed estimators of each edition's
  browsers spread about a point, so no per-edition overstatement is a graded figure. Decision designation_set, answer
  set_of_items, question form which.
- **Strategy.** causal_design: the conditioning set of a transport, attributes the cap cannot change in, the cap's
  own consequence out. G14 decisive (does the replayed reset rate of browsers whose cookies persist apply to the
  capped pool), G6 supporting (print subscribers, who read online weekly and skew to Apple devices, shift the pools'
  composition), G16 supporting (which comparison pool the replay runs on); gap population (which browsers stand in for
  the capped ones); Gate G method_or_model_selection; calibration gold_standard_subsample (the reader-account service's
  device register, exact browser identity for signed-in readers); context artifact monitoring_export (the analytics
  platform's monthly report); Layer 2 family estimand_identification, pattern
  own:transporting-revisit-behaviour-across-a-cookie-cap-conditioned-only-on-what-the-cap-cannot-change.
- **Forum, event, organisation.** customer_or_counterparty (advertisers buy on the kit's figures), period_close (the
  quarter just closed), media_or_publishing. Role compliance_or_audit (the head of audience data certifies the kit's
  figures).
- **People** (`guard.py names --geo Germany --seed 249`, locale de_DE): Nadin Schleich, head of audience data, who
  asks; Karl-Hans Schenk, web analytics engineer; Eugenia Oderwald, paywall and reader accounts; Almut Ladeck, ad
  sales. None appears in the prompt.
- **Data-native sentence.** The tag counts identifiers, not browsers, and on WebKit an identifier lasts only until
  the reader stays away for more than seven days, so the overcount is set by how readers space their visits, which the
  capped browsers cannot show and the other browsers record in full; but the paywall's meter sits in the same
  capped storage, so on WebKit it resets with the cookie and spares the weekly and occasional readers the
  registration wall their counterparts on other browsers meet, and sign-in, the status that looks like the obvious
  thing to hold fixed, is itself a product of the cap.
- **As-of.** Monday 15 January 2029, after the quarter's close and before the kit goes to advertisers on
  1 February 2029.
- **Sources.** The client's Layer 2 patterns for metric definition (a metric validated against its own measurement
  process; mix shift masquerading as behaviour change); WebKit's tracking prevention (script-written cookies capped at
  seven days since 2019), the measurement practice of replaying an identifier rule on persistent histories, and the
  causal rule against conditioning on a consequence of the exposure. No build on file carries an identifier cap or
  conditions a transport on what the cap leaves untouched (nearest drivers 0.04); task127's unshipped second layer
  and a task194 rejection condition a hospital cohort on an outcome, another construction.

## Default path

The careful reflex, measured on the cut pack (`generator/solve.py`, route r3a; asserted in `checks.py` T2).

1. Read the audience policy (unique browsers per edition and Berlin month, the quarter as the average of its months,
   the note above 25 per cent), the tag's notes (WebKit's seven days) and the paywall notes.
2. Clean the export: automated traffic, the newsroom's addresses and the re-sent rows out, HKR read as HOL, Berlin
   months, WebKit as every iOS browser and Safari on the Mac.
3. Count each signed-in WebKit browser once from the sign-in register (its device_id).
4. Replay the seven-day rule on the signed-out identifiers of other browsers in the same edition, month and device
   class, and divide the signed-out WebKit identifiers by the identifiers per browser it gives.
5. Add the other browsers, average the three months, compare with the platform's reported average.

Ends on: 4 editions carry the note (Rhenhagen Stadt, Kirchbrunn, Hollerfeld, Mühlenstedt); Wiesbrück, Sonnweiler,
Grauheim and Lindenau fall under the line at 22.0 to 22.8 per cent.
Golden: 8 editions carry the note (Rhenhagen Stadt, Kirchbrunn, Wiesbrück, Hollerfeld, Sonnweiler, Mühlenstedt,
Grauheim, Lindenau), each at 26.9 per cent or more under every estimator of the family; the other four at 22.7 or less.

## Stump sentence

A competent solver counts the signed-in WebKit browsers once from the sign-in register and divides the signed-out
WebKit identifiers by the seven-day replay of signed-out readers on other browsers, filing 4 editions (Rhenhagen Stadt,
Kirchbrunn, Hollerfeld, Mühlenstedt) and leaving Wiesbrück, Sonnweiler, Grauheim and Lindenau under the 25 per cent
line, because the paywall meter sits in the same capped storage: on WebKit it restarts with the identifier, so weekly
and occasional readers there seldom meet the registration wall and stay signed out while their counterparts on other
browsers met it and registered, which makes sign-in a consequence of the cap that cannot be held fixed; the golden
replays the rule within edition, month and device class on every non-print reader of other browsers whether signed in
or not, holds only print subscribers apart (their access never depended on the meter) and files 8.

## Three rules

Task type: metric-definition-measurement-science (Product Analytics), which serves Data Quality Monitoring.
Domain test: the deciding quantity is how many distinct browsers an analytics identifier count stands for when one browser family deletes the identifier after seven idle days, estimated the way audience measurement estimates it: the identifier rule replayed on the visit histories of browsers whose identifiers persist, matched on what the limit cannot change and pooled over what it changes.
Swap: "which of our twelve hospitals' monthly patient counts overstate their patients by more than a quarter" stops making sense: no wristband expires after seven days away while a visit quota kept in the same wristband decides who registers, so there is no capped identifier, no persistent comparison family and no status the cap produces.
Layer 1: the export's UTC times against Berlin months across the clock change of 29 October 2028; raw user agents beside the platform's parsed browser (Chrome on an iPhone parsed as Chrome though it runs on WebKit); the export job's re-sent rows of 21 November; the platform's bot flag and the newsroom's address range; Hollerfeld's content group re-coded on 1 November; account references hashed in the export and in clear in the register; the platform's report for the whole year beside the quarter's export; the paywall console's dates typed as German text; addresses that change as household lines reconnect and phones move between networks, and user agents that change with each browser release, so neither marks a browser. Each is written by the system named and each is neutral to the call (SF1 to SF4, SF6, SF8, SF11, asserted).
Layer 2: estimand_identification: browsers behind a capped identifier are recovered by replaying the cap on persistent histories, and the replay's comparison has to be matched on what the cap cannot change (edition, month, device class, a print subscription activated independently of the meter) and pooled over what it changes (sign-in, produced by the meter kept in the same capped storage).
Decisive step: transporting the replayed identifiers per browser within edition, month and device class from every non-print reader of other browsers to every non-print WebKit identifier, signed in or not, with print subscribers counted apart, rather than conditioning on sign-in (or taking the signed-in readers' own identifiers per device, or pooling print subscribers).
Not semantics: every field, browser string, clock and rule read correctly (the seven days, the meter, the tolerance, which browsers are WebKit, where the meter is kept) still leaves the choice of comparison; the step is that a status the cap itself produces cannot be held fixed, which no field, code or definition states.
Not rule application: the policy files the estimand (distinct browsers per edition and Berlin month, averaged over the quarter) and the tolerance, the tag's notes file the seven days; nothing files how the capped browsers are estimated, and executing every stated rule leaves the comparison open.
Analyst test: a strong analyst who reads everything correctly counts the signed-in WebKit browsers from the register and transports the replay of signed-out readers of other browsers to the signed-out WebKit identifiers, filing 4 editions and dropping Wiesbrück, Sonnweiler, Grauheim and Lindenau (22.0 to 22.8 per cent); checks.py T2 runs it on the pack and T1 confirms the World's own browsers file the golden 8.
Estimand: the audience policy, sections 2 to 4: for each edition and calendar month (Europe/Berlin) the browsers that loaded at least one of the edition's pages, a browser counted once however many identifiers it carried and in both editions when it read two, automated traffic and the newsroom out, averaged over October to December 2028, against the platform's users averaged the same way, the note above 25 per cent.
No decoy: nothing is planted; the platform's report is a correct count of identifiers and says so; no memo, draft or figure argues for a comparison; the paywall notes describe the meter as the paywall team would, for the data team.
No certified replay: no estimate of browsers per edition ships and the note is new in the 2029 policy, so no earlier kit carries one to reproduce.
Lesson: when a measurement cap also changes who ends up in a status, holding that status fixed compares unlike pools; condition the transport only on what the cap cannot touch. No build on file teaches it (task233 transports a nonresponse departure as odds, task458 corrects a trait-selected observation window, task262 a level-selected reliability).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the reported users as browsers: 0 editions | the platform's report | the report's users | yes, the published figure | none | no | read off | readable |
| 1 signed-in identifiers per device (register): 3 | the paywall notes' register | the register's device_id beside client_id | yes, the field's logged-in ratio | none | no | one ratio | readable |
| 2 the replay on every other browser, print pooled: 5 | the tag's notes | client_id and the parsed engine | yes, replay the rule where it is absent | none | no | one ratio per stratum | readable |
| 3 (default) sign-in held, signed-out by signed-out other browsers: 4 | the register and the tag's notes | user_ref empty or not | yes, like for like on every visible status | none | no | one ratio per stratum | readable |
| 4 signed-in from the register, signed-out by every other browser: 4 | the register | user_ref | yes, exact where known | none | no | one ratio per stratum | readable |
| 5 the WebKit share of signed-in devices as the browsers' share: 6 | the register | device_id and the engine | partly, a share from the gold standard | none | no | one share | readable |
| 6 (decisive) every non-print reader pooled over sign-in within edition, month and device class, print subscribers apart: 8 | no sentence says sign-in depends on the browser or names the comparison; the paywall notes say where the meter is kept and the tag's notes what WebKit does to script-written storage | origin sits in one column for print and registration alike; nothing marks a registration the cap produced | no, the reflex holds every visible status fixed | none ships; the print stratum's agreement (1.95 replayed against 1.99 counted) and the signed-in mismatch (1.57 against 1.24) exist only once computed | no | no | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a calendar month | Berlin (policy 2) | UTC | same call | asserted |
| SF2 | the replay's history | the browser's sessions across the site (the cookie is the domain's, tag notes) | within each edition | same call | asserted |
| SF3 | the re-sent rows of 21 November | dropped (tag notes) | kept | same call | asserted |
| SF4 | the newsroom's addresses | dropped (policy 2) | kept | same call | asserted |
| SF5 | the quarter's overstatement | the three-month averages compared (policy 2 and 3) | the mean of the monthly overstatements | same call | asserted |
| SF6 | a browser that read two editions | counted in both (policy 2) | counted once | same call | asserted |
| SF7 | WebKit | every iOS browser and Safari on the Mac (tag notes) | the parsed browser Safari only | no edition noted, ruled out | the tag notes: "on iPhone and iPad, the engine of every browser" |
| SF8 | the reported figure | the platform's report, HKR and HOL joined | recomputed from the export | converge | identical in every edition and month (checks C3) |
| SF9 | the comparison's strata | edition, month and device class | devices pooled | same call | asserted (C2) |
| SF10 | the estimator of identifiers per browser | the replayed runs | visits per browser | same call | asserted (C2) |
| SF11 | Hollerfeld's HKR rows | Hollerfeld's (tag notes, editions.csv) | a thirteenth group | ruled out | the tag notes and former_content_group |
| SF12 | the tolerance | more than 25 per cent (policy 4) | at or above | converge | no edition within 1.5 points of 25 under any estimator of the family (Grauheim 1.9 above under the visits ratio) |
| SF13 | a print subscriber's WebKit browser | one device (policy 2: a browser once) | each identifier | ruled out | policy 2 |
| SF14 | Ask A's moment | the end of 31 December in Berlin, 23:00 UTC (policy 6) | UTC midnight | BST +1, ruled out | policy 6 "Berlin time" |
| SF15 | Ask A's contact in two groups | counted in both (policy 6) | once | ruled out | policy 6 |
| SF16 | Ask A's pending contact | not a subscriber (policy 6: confirmed) | counted | ruled out | policy 6 |
| SF17 | Ask B's publication days | Monday to Saturday less the state's holidays (policy 5) | every weekday | ruled out | policy 5 and editions.csv's state |
| SF18 | Ask B's suspensions | a pause unsold, a forward or donation sold (policy 5) | every suspension unsold | ruled out | policy 5 |
| SF19 | Ask B's SATURDAY | Saturdays only (dictionary) | every day | ruled out | the dictionary |
| SF20 | Ask B's COMBI | one copy a day, the e-paper its own (policy 5, the dictionary) | its Digital Plus access counted again | ruled out | policy 5 "one for each paid subscription", the dictionary's COMBI, order_ref |
| SF21 | Ask B's trials | unpaid (policy 5) | counted | ruled out | policy 5 |
| SF22 | Ask B's single copies | delivered less returned by issue (policy 5) | delivered | ruled out | policy 5 |
| SF23 | the replay's span | identifiers per browser month by month | pooled over the quarter's three months | same call | asserted |

## Ladder

Six wrong rungs and the golden, each a defensible way to estimate the browsers behind the identifiers, each dying to one
fact the pack holds (per-edition overstatements on the cut pack from `generator/solve.py`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | the reported users taken as browsers | 0 editions | the tag's notes: WebKit renews the identifier after seven idle days |
| 1 | identifiers per signed-in WebKit device from the register, applied to every WebKit identifier | 3 (Kirchbrunn, Hollerfeld, Mühlenstedt) | signed-in WebKit readers are the frequent ones: 1.24 identifiers per device a month against 1.57 replayed on signed-in readers of other browsers |
| 2 | the replay on every other browser within edition, month and device class, print subscribers pooled | 5 (drops Kirchbrunn, Hollerfeld, Mühlenstedt) | print subscribers read weekly on Apple devices: 61 per cent of their signed-in devices are WebKit against 27 per cent of the others |
| 3 (default) | signed-in WebKit browsers from the register, signed-out identifiers by signed-out other browsers | 4 (drops Wiesbrück, Sonnweiler, Grauheim, Lindenau) | sign-in is selected differently by engine: the meter restarts with the identifier on WebKit, so 27 per cent of WebKit's non-print identifiers are signed in against 63 per cent elsewhere, and the signed-in mismatch above |
| 4 | signed-in from the register, signed-out by every other browser | 4 (the same four dropped) | the signed-out WebKit pool lacks the frequent readers the comparison keeps |
| 5 | the WebKit share of signed-in devices taken as the browsers' share | 7 (drops Kirchbrunn and Hollerfeld, adds Bergstetten) | the same selection, read as a share |
| 6 (golden) | every non-print reader of other browsers pooled over sign-in within edition, month and device class, print subscribers counted from the register | 8 | |

- **Margins.** Under the golden, the quarter-pooled replay, devices pooled, and the visits and page-view ratios (by device
  class or pooled), the eight sit at 26.9 per cent or more (Grauheim, under the visits and page-view ratios) and the other
  four at 22.7 or less (Bergstetten, visits with devices pooled). The sign-in rungs leave the four meter editions at 22.0 to 22.8 (rung 3) and 23.1 to 23.7
  (rung 4); the print-pooled rung leaves the print editions at 18.0 to 20.1.
- **Position.** No wrong rung files the eight; rungs 3 and 4 file Rhenhagen Stadt and the print editions, rung 2
  Rhenhagen Stadt and the meter editions.
- **Dominance.** The decisive step raises the meter editions' overstatement by 5.5 to 6.6 points against rung 3; the
  print step raises the print editions' by 9.7 to 10.1 against rung 2.
- **Grid.** UTC or Berlin months, the replay site-wide or by edition, the re-sent rows and the newsroom in or out, the
  quarter as averages or as monthly ratios, a two-edition browser once or twice: the eight every time (SF1 to SF6).
- **Worth.** Four editions' notes on the call; the World's own browsers file the same eight (T1).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the browsers that loaded an edition's pages in the month, automated traffic and the newsroom out (policy 2) |
| 2 | Unit of account | a browser, once however many identifiers (policy 2); a print subscriber's browser by its device (SF13) |
| 3 | Attribution window | October, November and December 2028, Berlin months (policy 2, SF1) |
| 4 | As-of dating | Monday 15 January 2029; the export of the quarter, the register and accounts as of that day |
| 5 | Version basis | the policy of 4 December 2028 (section 4 new); the tag's notes of 9 January 2029 |
| 6 | Denominator | the estimated browsers (policy 4: reported above browsers) |
| 7 | Weighting | the quarter as the average of its three months for both figures (policy 2 and 3, SF5) |
| 8 | Window length | three months |
| 9 | Boundary inclusivity | more than 25 per cent (SF12) |
| 10 | Rounding path | the comparison before rounding (policy 7) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | the quarter is closed; the export holds every session to 31 December |
| 13 | Order of operations | clean, classify the engine, link the register, replay, estimate by stratum, average, compare |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | the re-sent rows dropped (SF3) |
| 16 | Identity normalisation | HKR to HOL (SF11); client_id across the export, register and paywall log; user_ref hashed |
| 17 | Netting against gross | none |
| 18 | Dimensional units | seconds and days (seven days of 86,400 seconds) |
| 19 | Code and status semantics | origin's three values; outcome's three; the engine from os and browser (SF7) |
| 20 | Integerisation | a set and a count; the asks whole numbers (policy 7) |
| 21 | Clause scope | the note applies to the digital figure only (policy 4); sections 5 and 6 to the asks |
| 22 | Forward window contents | the 2029 kit quotes the fourth quarter of 2028 (policy 1) |

## Literal reader

Executing the prompt and the policy word for word: for each edition and Berlin month of the quarter, the browsers that
loaded its pages, once each however many identifiers, against the platform's users, averaged over the three months,
noted above 25 per cent. The browsers behind WebKit's identifiers are unobserved, which no sentence estimates; every
estimator that replays the seven-day rule on other browsers' histories within edition and month, transports it to
every non-print WebKit identifier whatever its sign-in, and counts print subscribers from the register files the eight
(by device class or devices pooled, runs replayed or visits per browser), and every convention row of the fork table
files the eight. The easy answers (4, 5, 3, 6 or none) come from an easy comparison on the same literal estimand, never
from another reading.

## Oracles

None for the call: no estimate of any edition's browsers, no earlier note and no ranking on overstatement ships. The
platform's report ties the reported figure under every handling. The print stratum's agreement (replayed 1.95
identifiers per browser a month against 1.99 counted on print subscribers' WebKit devices) and the signed-in mismatch
(1.57 against 1.24) are facts of the data that confirm the golden's comparison only once computed; no file states
either. For the asks, nothing referees either device: Ask A's link additions show only as clicked links and as
last changes no status event or preference-centre change explains, and Ask B's moved starts show only through the
numbers' entry order and the Digital Plus accesses' own starts; no file names a total.

## Ask sheet

**Ask A, each edition's newsletter subscribers at the end of 31 December 2028 (12 figures, exact).** H18: a measure
every edition carries in the kit beside the digital figure; the call reads no newsletter row. Use: the kit's newsletter
line, which ad sales quotes for sponsorships. Primary device: D5 (a silently partial log). The contact export is taken
on 15 January 2029 with its groups as they stand. The preference centre's log holds every change contacts made there,
with the groups before. The newsletters' one-click links, though, add a group without a preference-centre entry; they
come from the box under each newsletter from 7 November and from the new year's mailing of 3 to 14 January, each
offering a neighbouring edition. Each is recorded only as a clicked link in the activity log, among about 64,000
article clicks. The 906 links clicked after midnight add 35 to 139 subscribers to every edition that a reversal of the
status events and the preference centre's log keeps. Its over-cleaning half: the 458 links clicked before midnight
stand, and undoing every link addition takes 16 to 71 off every edition. Found only by inconsistencies the records
hold: a contact's last change in the export with no status event or preference-centre change at that moment, and
export groups that the preference centre's last change does not show. A clicked link at that moment explains both. The
golden equals the platform's own state at midnight, replayed forward from each sign-up (checks A0). Hazards:
- statuses changed after the cut-off (the activity log's first later status event implies the earlier status, and a
  click is not a status event);
- pending contacts and cleaned addresses;
- Berlin against UTC midnight (SF14);
- the preference centre's changes after midnight (the export's groups as they stand: +38 to +142).

Path: the contact export, the activity log, the preference centre's log, editions.csv (the link's edition name), the
policy, the dictionary (6 files; contact_id, status, groups, last_changed_utc, event, at_utc, link, changed_utc,
groups_before, name). Realism: newsletter platforms export current state, keep six months of activity and log a click
with its destination. One-click cross-subscription links are an ordinary newsletter feature, and a preference centre's
history holds only the preference centre's own changes.

**Ask B, each edition's average sold copies per publication day in the fourth quarter of 2028 (12 figures, whole
copies).** H18: a measure every edition carries in the kit; the call reads no circulation row. Use: the kit's print
line, on which local print packages are priced. Primary device: D8 (an anchor on a later record). From the circulation
system's release of 6 November 2028 until the fix of 14 December, its customer screen wrote the date a change of
address, bank details or payment was saved into the subscription's start date. So 451 subscriptions delivered for
years show a start between 6 November and 13 December, and counting from the start shown drops 9 to 59 copies a day
from every edition. Found only by inconsistencies the records hold, with nothing narrating the release and no column
marking the rows:
- subscription numbers are issued in order as subscriptions are entered (the dictionary), and these numbers sit among
  subscriptions started years before;
- the COMBI ones sit beside Digital Plus accesses that started years before.

Its over-cleaning half: subscriptions genuinely started in those weeks (December's gift subscriptions among them), taken
as before the quarter, add 19 to 71 to every edition. Fair: every moved subscription was delivered from before
1 October 2028, and the number order moves exactly the release's 451 (checks B1, against the generator's own starts).
The release re-dated only subscriptions still being delivered when the change was saved, so no record ends before it
starts; its evidence is cross-file only (16 suspensions before a shown start, 49 Digital Plus accesses before their
COMBI's).
Hazards:
- the COMBI's e-paper counted again (its Digital Plus access, order_ref Kombi and the sub_no; both round 1 readers met it);
- pauses against forwards and donations;
- SATURDAY on Saturdays;
- trials;
- the state's holidays (1 November in Rhineland-Palatinate);
- single copies by issue.

Path: subscriptions, suspensions, e-paper accesses, single copies, retail points, editions, the policy, the dictionary
(8 files; sub_no, product, copies, start_date, end_date, kind, from_date, to_date, plan, order_ref, price_eur,
delivered, returned, edition, state). Realism: a release that writes a change's date into a neighbouring field is an
ordinary circulation-system fault, and number order is how a circulation clerk dates a contract.

Main population zero-counts: the call reads the session export, the sign-in register and the accounts. No newsletter,
circulation, e-paper or single-copy row exists in them, and no ask file is read by the call (separation by file,
asserted by the solver's inputs).

| Hazard | Asks moved | Per-ask deltas |
|---|---|---|
| the link additions after midnight kept (D5, primary) | A | +35 to +139 |
| every link addition undone (its over-cleaning half) | A | -16 to -71 |
| the export's groups as they stand | A | +38 to +142 |
| UTC midnight | A | +1 at Bergstetten |
| the start dates as shown (D8, primary) | B | -9 to -59 |
| every start in the release's weeks before the quarter (its over-cleaning half) | B | +19 to +71 |
| the COMBI's e-paper counted again | B | +155 to +712 |
| SATURDAY every day | B | +195 to +726 |
| pauses ignored | B | +11 to +58 |
| no holidays | B | -14 to -51 |
| every suspension unsold | B | -6 to -30 |
| trials counted | B | +3 to +12 |

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed, both round 1 readers' repairs) | Verdict |
|---|---|---|
| Ask A, subscribers, all 12 editions | statuses and the preference centre's changes taken back from the logs, the link additions kept: every edition high | miss |
| Ask B, sold copies, all 12 editions | every filed rule executed, the Digital Plus accesses left out, the start dates as shown: every edition low | miss |

Measured by: generator/pair.py on the cut pack. The cracker keeps 0 of the 24 ask figures, and so do the mirror (the
same asks, off the call), the over-cleaner and the lazy path (the exports as they stand); a response meeting every
device keeps 24. The round 1 readers kept 23 and 24 of the earlier devices, and both devices above sit on paths
those two left unread (supplemental-stumping 1.1c).

Pair ceiling: 28.5 ((38 + 7 + 55 x 0) and (5 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Leak check

leak.py (as-of 2029-01-15): REVIEW, no LEAK; file names, author vocabulary, answer figures, announcements, ranking
artifacts, hidden content and the prompt gate clean. Each REVIEW line, answered:

- The dictionary, the tag's notes, the policy and the paywall notes carry the stump paragraph's nouns (browser, reader,
  device, register, identifier, sign-in): the fiction's own vocabulary; no sentence says sign-in depends on the
  browser, names a comparison pool or estimates browsers; the paywall notes' print line no longer says activation is
  independent of the meter (cut before stage 4: it pointed at the decisive step); harmless.
- `device` in the ad server's file and `device_id` in the sign-in register: the systems' own dimension and the account
  service's login-cookie id; harmless.
- Sixty-three suspension end dates after 15 January 2029: holiday pauses booked ahead to run into January, as a circulation
  system records them; none reaches the quarter's figures beyond 31 December; harmless.

## Retired

Retired on 2026-10-20 at the author's choice. Architecture 4 was spent at stage 4 round 3 under the two-reader rule:
reader 5 landed the call through an activity-stratified calibration on the signed-in WebKit browsers. Four
architectures are now spent on the number:

| Architecture | World | Spent |
|---|---|---|
| 1 and 2 | PES, a low-cost sensor network's drift pull list | each landed by the stage 4 reader |
| 3 | psychology, a verification check's genuine referral rate | landed by the reader with every ask figure |
| 4 | Product Analytics, WebKit's seven-day cookie cap and the media kit's measurement note | landed by one of five clean readers |

Architecture 4 passed every free gate. The judge returned DETERMINISTIC, APPROVE on all three packs, and both round 3
readers kept 0 of 24 ask figures. It was never shipped: `target.zip` 31ad0d1e and the goldens stay untracked, and the
generator rebuilds them. Every card is kept, and the architecture 4 card carries `architecture_spent`.

The lesson the number paid for: the cap selects through visit spacing, and an identifier's own session count records
most of that spacing. So any calibration stratified on activity recovers the conditioning set the easy route misses.
A transport stump is spent when the unit's own trace can reconstruct the selection that decides it.

## Tried and rejected

- Drift forecast from the cumulative particle load through an optical PM sensor (drift accrues with dose, not calendar
  time): the lesson is task46's (a rate law stationary only in cumulative service exposure), so the driver is spent.
- Seasonal confounding of a PM sensor's gain by humidity growth or aerosol type: the shape of task248's driver (a
  covariate moving over the year against a level comparison), one build earlier.
- An analyser ask (each analyser's 2027 days over 120 micrograms on the EU maximum daily 8-hour mean): every device it
  carried (span-check hours flagged N, the old analyser's parallel rows) is adjudicated by the station sheet, so the call-landing
  response executes it and keeps every figure; dropped for the node quarter's single silent device.
- Architecture 1 (each node's span read from its spread against the four distant analysers, the paired slope
  attenuated by the sites' partial hourly agreement): the stage 4 reader (medium effort, about two minutes) landed the
  call with an errors-in-variables slope instrumented by the other stations' mean, cued by plan 4's "true ozone
  concentration at its inlet", and kept all 36 ask figures after reading the vendor's firmware note. Regression dilution
  is textbook statistics, so the decisive step is readable to a strong model; and an ask one device deep falls to one
  document read. Realism tells it named: firmware dates cycling in ten-day steps, installation dates on a fixed
  five-week pattern, visit slots on a fixed cadence, the ES4104A analyser's model against its serial (T400 and API400E),
  head serials stepping by 37. The judge's pass on the same bundle: DETERMINISTIC (write-up wording only); its residual
  reading F1, the spread of the four stations' averaged series, gives 10 nodes, so architecture 2's write-up says the
  analysers' hours are pooled.
- Ask A on firmware 4.2's renumbered codes alone, the release note carrying a table of the codes up to 3.7 and from
  4.2: architecture 1's stage 4 reader read the note and kept 36 of 36. The note now gives 4.2's codes only (the records
  show the old meaning: before each node's update its status-1 records are the two warm-up hours after a restart), and
  the restart clocks stand beside it as a second primary, each moving all 36 figures alone.
- The firmware table without a date for OZ19 read as OZ19 never reaching 4.2: the spare's records after the 25 January
  rename lost their humid hours (OZ19 +89 against +18 to +24 elsewhere); OZ19 runs 4.2 from the spare's start at 11:00
  on 9 January, in the solver, the verifier and A1.
- Architecture 2 (each node's span read on the mixed afternoon hours, the hill villages above the night's surface
  layer): the stage 4 reader (Sonnet, medium, about four minutes) landed the call with a regression on the four
  analysers, the 900 m sites' night-time intercepts and the register's altitudes pointing it to the midday hours;
  the judge's pass on the same bundle was DETERMINISTIC, APPROVE, and Ask A held (0 of 36). A site's night-time
  decoupling shows in any residual by hour of day, so the decisive step is readable to a strong model.
- Architecture 3 draw, 2026-10-19, candidates that died before the card was filed: register coverage by dual-system
  estimation within post-strata after erroneous enumerations (task448 already runs capture estimated within route
  strata in the same task type); an adaptive item bank's drift under compromise read with purified anchors (filed as
  drift on the bank's scale, its literal reading is the contaminated thetas, so the estimand forks unless it names
  the purification, which files the method); rapid guessing read from item-specific response-time thresholds (the
  decisive step is a threshold choice, a coin flip in the client's measured runs); this world's forward referral rate
  under the SE-scaled rule (1.645 times the standard error of the difference: the rule's own scaling compresses every
  account into 2 to 9 per cent, too thin for a cap) and a fixed eight-point band (elite accounts at 40 to 60 per cent,
  no firm would adopt it, and a 2028 verification record would let a solver carry each account's empirical shortfall
  forward). The confidence-band rule on the verification score, with the check new in 2029, keeps the spread
  realistic and leaves no per-account history to carry.
- Ask A's highest weekly exposure of any item (four figures): any response that checks the attempts against the
  register keeps it whole, so the ask's weight sat on the one device a careful response can find; replaced by the
  count of items rested for 2029, which the suite moves as well, and the ask cut to five figures.
- Appeal outcomes recorded as later rows of the original case: each case's latest row, the habitual read of a decision
  log, filed the golden, so the impersonation ask carried no device. The desk now logs an appeal as a case of its own,
  as its own sheet would, and a sitting's standing is the latest decision across the candidate's cases.
- The synthetic suite's sittings labelled release 5.3.2 in the week of 3 July, before the release went live: a marker
  isolating the device rows in one week. They now carry the release in service, as the platform stamps every attempt.
- Shrinkage of each pool's top share with each candidate's reported error (Kelley's formula at the estimate) taken as a
  competing reading: it adds NVK, UJB and OJS, but the study's own top tenth of MAT-R scorers refutes it (it predicts
  their MAT-V a tenth of a logit lower than scored) while the shrinkage at the ability, the full posterior and the
  world's own truth all file the 15. Kept as a rung and stated in the write-up's critical components, so a judge sees
  the refutation in the shipped data.
- Architecture 3 (each account's 2029 referral share read through its shortlist's regression to the mean, MAT-R's
  error at the ability and the retest gain at the interval): the stage 4 reader (Sonnet, medium, about eleven
  minutes) landed the call with a latent-ability model (a tier prior deconvolved from the 2028 pool, Table 4.3's
  errors, the study's fitted gain), checked against the study's referral rates by interval and by MAT-R level, and
  kept all 19 ask figures, finding the 6,400 Monday-night identities outside the register, each candidate's latest
  case decision and the fresh booking references from release 5.3.2; the judge's pass on the same bundle was
  DETERMINISTIC, APPROVE. Selection on a noisy score is the textbook regression to the mean, a shrink the author file
  names as a reflex, so the decisive step is readable to a strong model, and three devices one cross-file check deep
  each fall to the hygiene battery. Realism tells it named: round plan counts and shortlist ratios, the suite's
  identical early-Monday timing and short sittings, uniform selection-day spreads, the study's fixed interval grid.
- Candidate 1 as offered to the author (signed-out visitors on other browsers as the comparison for signed-out WebKit identifiers): in a world without a meter it is the golden, and holding every visible status fixed is the careful opponent's reflex, so it would be landed by the first thorough reader; prototyped at the draw (proto3 and proto4 in the session scratchpad), the decisive step moved to what that reflex gets wrong, the sign-in the capped meter produces. A first cut of the print-subscriber skew modelled print readers as daily readers and moved nothing (the skew shifted the device-only route by 0.5 points): daily readers never reset, so print subscribers are drawn as the weekly and occasional online readers a print household is.
- The sign-in trap at the draw's weekly gaps (eight to nine days, two to three registration chances in ten on WebKit):
  the sign-in split fell only 2.6 points short of the golden on the meter editions, inside a reader's variant of it;
  weekly readers now come every eight to twelve days, so WebKit's meter almost never reaches the wall, and the gap is
  5.5 to 6.6 points.
- The hybrid (signed-in browsers from the register, signed-out identifiers by every other browser) at the draw's
  reader mix: within 1.5 points of the golden everywhere, because removing the few signed-in WebKit readers barely
  moves the pool's revisits; it lands the call unless the signed-in pool is large and frequent. A local edition's
  loyal core (daily and regular readers about a third of the month's browsers, registered on every engine) makes it
  fall 4.4 to 5.7 points short on the meter editions.
- Print-heavy editions under the line to catch the signed-in ratio: the ratio over-corrected them by only 2.5 points
  at a realistic print share; with the loyal core the ratio falls 10 points short on every non-print edition, so it
  needs no print-below rung, and those editions became ordinary unnoted ones.
- Ask B's primary as return slips dated by collection (weekly points covering the week before): the quarter starts on
  a Monday and ends on a Saturday, so a slip never straddles it and shifting every slip one publication day gives the
  exact answer; dropped for the COMBI's e-paper on the e-paper platform.
- Ask A's primary as contacts archived after the year's end and missing from the export: their groups at archiving
  would have to ship somewhere, which marks them; dropped for the export's current groups after the new year's mailing.
- A 0.6 scale world with 5.3 million sessions at full scale: the export reached 75 MB; the populations were scaled by
  0.6, daily readers' sessions a day trimmed, and the export sorted by identifier (3.0 million rows, 34 MB).

- Architecture 4, stage 4 round 1 (2026-10-19): reader 1 (Sonnet, medium, about thirteen minutes) landed the call without
  the decisive step. Every browser had carried one user-agent string and one address all quarter (3,048 prefixes,
  about 65 identifiers each), so chaining the anonymous WebKit identifiers within user agent, address and edition, each
  new one at least seven days after the chain's last session, matched the register's devices within 0.04 per cent and
  filed the golden's eight. Reader 2 fell on the trap (three editions, the signed-in ratio bridged by state). The judge's
  pass on the same bundle was DETERMINISTIC, APPROVE. The landing came through a construction defect, the browsers
  observable through a fingerprint no real export carries, not through the decisive step. Repaired in the generator:
  - Addresses now vary by session: household lines that reconnect (daily, weekly, monthly or fixed) inside each
    edition's region's provider blocks, mobile networks' shared pools, and office lines on weekday daytimes.
  - User agents are shared by version and move with each release at the browser's own lag; Safari's system token is the
    one Safari has reported since version 26.

  After the repair, reader 1's chain misses the register's devices by 24 to 64 per cent. Every chaining key fails its
  own check on the registered identifiers by 12 to 43 per cent and files 0, 4 or 9 editions (chain_test.py in the
  session scratchpad). The route table is byte for byte the same.
- Ask A's primary as the export's current groups after the new year's mailing, with the mailing's additions in the
  group-change log: both stage 4 readers reversed the log and kept all twelve figures (a change file over a base list,
  which the hygiene battery executes). The mailing's additions now come through the newsletters' one-click links,
  recorded only as clicks in the activity log among the article clicks; the preference centre's log does not hold them.
- Ask B's primary as the COMBI's e-paper counted again: both readers matched order_ref Kombi to the COMBI and kept every
  figure (one dictionary line and the reference settle it). It stays a hazard. The primary is now the circulation
  system's release of 6 November, which wrote the date of a saved change into the start date until the fix of
  4 December; only the numbers' entry order finds it.
- Realism tells the readers named:
  - Fixed: e-paper accesses starting in 1974, before the e-paper existed (each plan now starts no earlier than its
    launch); one order reference on two accesses (now unique); start dates spread evenly back to 1974 (now a tenure
    curve, with subscriptions older than the system carrying its go-live date).
  - Kept: 88 per cent of sessions signed in, which a registration wall after five free articles produces in frequent
    readers; Rhineland-Palatinate's editions print-heavy and Hesse's digital, a rural against commuter-belt geography.
- Stage 4 round 2 (2026-10-19, target.zip d00ed7b6): both readers missed the call. Reader 3 filed the default path's
  four (the signed-out replay with edition weights); reader 4 filed nine, Bergstetten marginal (signed-in readers
  reweighted by session count). The newsletter device held for both: each noticed 49 contacts whose groups the
  preference centre's log does not explain and left them as exported. Reader 4 kept all twelve sold-copies figures (12
  of 24, exit 1). It was cued by twelve subscriptions the release had re-dated past their own end date, an impossible
  record that a start-before-end check finds, then the numbers' entry order and the COMBI accesses' earlier starts. The
  judge: DETERMINISTIC, APPROVE. Repaired: the release re-dates only a subscription still delivered when the change is
  saved; customer numbers are unique (reader 3 found trials sharing a daily subscriber's number); retail points keep
  a weekly rest day or a holiday closure (reader 4: exactly 378 rows on every issue).
- Stage 4 round 3 (2026-10-19, target.zip 31ad0d1e, the final pack). Reader 6 missed the call: the sign-in split's
  four, with 0 of 24 ask figures. Reader 5 landed the call with 0 of 24 ask figures (exit 1). It calibrated each
  anonymous WebKit identifier's share of a browser on the signed-in WebKit browsers, stratified by edition, by whether
  the cookie predates the quarter, and by the identifier's sessions in the month (1, 2, 3, 4 or more), and filed the
  eight with Bergstetten at 24.2. Round 2's reader 4 took the same calibration with the strata pooled over editions and
  filed nine (Bergstetten 25.8). The light strata of the signed-in WebKit pool are mostly print subscribers, the
  readers whose sign-in the meter does not select, so the stratified calibration leans on the very population the
  golden validates on, without the reader naming it. The judge's pass on this pack: DETERMINISTIC, APPROVE (the 24 ask
  figures exact). The cap's selection runs through visit spacing, which an identifier's own session count partly
  shows, so any calibration stratified on activity recovers most of it. Four of five clean readers across rounds 1 to
  3 missed the call (one landing, one more within one marginal edition); round 1's other landing came through the
  repaired fingerprint. Under the two-reader rule a call any reader lands is spent. Hardening the ladder against one
  estimator is not a repair, so shipping as measured, a fifth architecture or retirement is the author's call.
- Architecture 4 as a whole (WebKit's seven-day cookie cap, the meter's selection of who signs in, the transport within
  edition, month and device class): spent at stage 4 round 3 when reader 5 landed the call. The cap selects through
  visit spacing, which an identifier's own session count records, so a calibration stratified on activity recovers the
  selection. The number was retired on 2026-10-20 at the author's choice.
