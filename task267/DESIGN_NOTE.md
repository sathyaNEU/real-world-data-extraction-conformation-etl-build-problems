# task267 design note

Architecture 1, drawn 2026-10-17 (wave 4, Descriptive lane, sathay3012). Seed DA17's annuity world was worked at the draw and set aside (`## Build record

- Generator: `common`, `world` (the clean truth: venues, events, adults and their diabetes, the encounters, the 2026 referrals and the evaluation draw, the OGTTs and the typed program IDs, on their own random streams), `askworld` (the analyzers' assignments, schedule, runs and the run database's downloads; the laboratory's invoices and credit memos), `records` (the exports), `docs` (the protocol, the notes, the maker's error reference, the manifest), `analysis` (every figure from the shipped pack), `deliver` (the goldens, figures.json, metadata.json), `checks` (447 assertions), `verify` (independent, pandas, the rules parsed from the candidates file), `build`. Seed 285 chosen at the draw from a search over 300 worlds of the same process (299 landed as designed); no row is edited after it is drawn.
- Pack: 14 files (CSV, TXT, XLSX, PDF); the encounters 39,484 rows, the run database 51,094; distractors the post-event feedback cards and the region's 2024 community health assessment (`metadata.json`).
- Gates: checks green, `verify.py` agrees, two builds byte-identical, `figures_check.py` 107 of 107, container audit clean on the pack and the goldens, `target.zip` cut from the final build. The memo renders on one page; the workbook prints one page wide per sheet.
- leak.py (2027-01-18): REVIEW, every line harmless. Sweep 3: 120 appears in the OGTT extract's column GLU_120MIN_MGDL, the two-hour sample's minutes. Sweep 4: the protocol and the notes use the program's own words (random glucose, the evaluation draw, everyone screened, results) and name no weight, estimator or verification bias.
- guard.py surface: two surface overlaps fixed (the manifest's column set was task266's, now file_name, description, supplied_by, extract_date, extent; the prompt's rounding sentence shared task256's and task450's construction, rewritten); the remaining promotions are card keys (the gap key population, pick_one_of_n, the pairing two builds back, G14 with task233, task256, task262, task465 and task54), each answered by the card's differentiation lines.
- guard.py heart at stage 3: WARN only (repeat.gate_g and overuse.gate_g against task192 v3 and task182 v2, repeat.question_form against task182 v2, answered at the draw); nearest drivers task257 and task57 v20 at 0.07.

## Pre-ship check

- Rule 1: the call turns on each referral rule's sensitivity for undiagnosed diabetes among everyone screened, a diagnostic accuracy estimate under partial verification (the OGTT reached everyone the 2026 rule referred and a random fifth of the rest), the verified adults weighted back through the referral groups; a warehouse's pallet rules have no reference test given through an older rule's signals and a random draw, so the task no longer reads the same.
- Rule 2: the mess (an event's re-sent tablet rows, later screenings under the same program ID, program IDs as the service center typed them, month/day/year dates, incomplete tests, missed appointments, tests at a center in another area) is how the program's and the laboratory's systems hold their records, and each item mishandled leaves the call or fails loudly (asserted, R2); the decision rests on the estimator, Layer 2.
- Rule 3: no memo, decoy or planted block; no field or code read differently flips the call (the default path reads every field correctly); no filed rule says how to estimate a rule's sensitivity among everyone screened, and executing the protocol on the default path files the 2026 rule plus an HbA1c of 6.0 (asserted on the clean truth).

## Tried and rejected`); the slot draws a new world in the same objective. Sallowfield Health, a regional health system in a US state, runs a community diabetes screening program: mobile events at churches, workplaces, community centres and county fairs across its Ostervale service region, where adults without a diabetes diagnosis answer a risk questionnaire (a score from 0 to 10) and give a fingerstick for a random glucose and a point-of-care HbA1c. In the 2026 season (38,601 adults, 2 March to 20 November) the screening tablet referred for a 75 g oral glucose tolerance test (OGTT) everyone scoring 6 or more or with a random glucose of 140 mg/dL or more, and, for the season's evaluation, a random fifth of everyone it did not refer; about four in five referred people kept the appointment. The OGTT is the reference: diabetes when the fasting glucose is 126 mg/dL or more or the two-hour glucose 200 mg/dL or more. Before the 2027 season opens, the program loads one referral rule into the tablets from six candidates; its protocol takes the rule that refers the fewest people screened among the rules that find at least 85 of every 100 people with undiagnosed diabetes among everyone screened, and keeps the 2026 rule when none does. The call is forward facing: the rule runs the 2027 season.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task267.json`, architecture v1, registered 2026-10-17, the set-aside DA17 draw kept in its lineage with its fate. The health system is a health provider (`hospital_or_health_provider`); the program director sets the rule with the program's medical director, no formal forum (`line_manager_or_team`); the 2027 season's opening forces it, the rule being loaded into the tablets before the first event (`launch_or_rollout`); the requester is the program director (`operations_director`); the context artifact is the 2026 season's close-out report (`close_out_summary`); no calibration organ (the random fifth is the second phase of the season's own sampling, not a separate settled corpus). `guard.py check` before register, after a pull: BLOCKs on the calibration form, forum and forcing event against task192 v3 and task182 v2 (filed in parallel) cleared by redrawing those three axes (a random fifth that is part of the design, not a calibration corpus; the director and medical director deciding; the season's launch); WARNs answered below.
2. Pairing: Biomedical & Clinical Research (client domain) / diagnostic-biomarker-accuracy / Descriptive & Distribution Analysis. The task type's own object, a test's sensitivity in the population tested when the reference standard reached only part of it, decides the call (the client's rigor pattern biomedical-clinical-research/diagnostic-biomarker-accuracy/1, partial verification); the setting is a health system's community screening program.
3. Niche: a community screening program whose reference test followed its own referral rule plus a random fifth of everyone else, choosing the next season's referral rule among candidates the old verification design was never built around.
4. Call and shape: which of six referral rules the 2027 tablets carry (`pick_one_of_n`, question form which). Shape 10 (a scorecard of metric against threshold): each rule's sensitivity among everyone screened against the 85 per cent target, with each rule's share of those screened it refers.
5. Gate G `method_or_model_selection` (the estimator the season's two-phase verification design entitles against the complete-case reading), strategy `population_selection` (the participants with an OGTT result were selected by the old rule's own signals), decisive generator G14 (the tested participants' diabetes rate carries to the untested only within the 2026 referral groups), then G12 (a missing OGTT is a non-answer, not a negative) and G16 (the weighting the design entitles).
6. Data-native sentence: the 2026 tablets sent everyone the old rule flagged (a questionnaire score of 6 or more or a random glucose of 140 mg/dL or more) and a random fifth of everyone else to the OGTT, so who has a reference result depends on the old rule's signals; the people with undiagnosed diabetes whom the old rule does not flag, a third or more of all cases and milder ones, reach a result only through the random fifth, each standing for about six others, and every candidate that contains the old rule finds nearly every case among the tested.
7. Sources, one line each:
   - The client's rigor library, diagnostic-biomarker-accuracy pattern 1 (partial verification biases accuracy; Begg-Greenes or inverse probability of verification weighting): this build's verification follows another rule's signals, not the candidate's own result, so the textbook correction by the candidate's result is not the design's estimator.
   - task260 in this lane (a breast screening service's reader study, readers and examinations both random): another screening decision, a different object (variance of an AUC across readers), nothing verified partially.
   - task233 (a gold-standard follow-up carrying a missing-against-imputed departure as an odds ratio): a follow-up sample of missing values; here no departure is modelled, the verification probabilities being known by design.
   - task264 and task261 in this lane (survey weights, replicate variance): weighting by inverse probabilities is the shared device; here it is the field's verification correction for a diagnostic accuracy estimate, its strata the old referral rule's groups.
   - task265 and task266 in this lane (survival with late entry; competing exits): no time-to-event structure here.
8. People, drawn with `guard.py names --geo "united states" --seed 267`: Aaron Bradley (director of the community screening program, the requester), Ariel Tucker (the program's medical director, who owns the screening protocol), Bryan Gardner (data manager, author of the extract notes), Matthew Garcia (the program analyst who writes the goldens). The suggestion list filters names already on file, so a rerun now omits these four. Invented names (Sallowfield, Orlenby, Fenwater, Drummery, Pellowmoor, Quessly, Thessler, Glyquant) screened against geonamescache's places, counties, states and countries and a curated list of small places (H21, asserted); sites and tablets carry codes.
9. WARNs answered: `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, against task192 v3 and task182 v2, 6 of the last 12): it is the honest mechanism here (two readings of the season's OGTT results, the design deciding between them), and the batch varies elsewhere (a diagnostic accuracy estimate under partial verification, a pick, shape 10, a health provider); `repeat.question_form` (which, against task182 v2): the decision is a pick among six named rules, so the question asks which.

## Default path

1. Read the protocol: the 2027 rule must find at least 85 of every 100 people with undiagnosed diabetes among everyone screened, and among those that do, the rule that refers the fewest people screened is used.
2. Take each adult's first screening of the 2026 season from the tablets' event exports, join the reference laboratory's OGTT results through the program ID the patient service center typed, and classify each completed OGTT (fasting 126 mg/dL or more, or two-hour 200 or more).
3. For each candidate rule, the sensitivity: among the participants whose OGTT shows diabetes, the share the rule flags; the referral share: the share of everyone screened the rule flags.
4. The rule with the lowest referral share among those at 85 per cent or more.

Ends on: the 2026 rule plus an HbA1c of 6.0 per cent or more, about 93 per cent sensitivity among the tested with about a quarter of those screened referred (the simulation at the draw; built figures replace these).
Golden: an HbA1c of 5.7 per cent or more or a random glucose of 120 mg/dL or more, about 90 per cent among everyone screened with about 36 per cent referred; the 2026 rule plus an HbA1c of 6.0 or more reads about 77 per cent among everyone screened, and an HbA1c of 5.7 or more alone about 81.

## Stump sentence

The default path recommends the 2026 rule plus an HbA1c of 6.0 per cent or more, at about 93 per cent sensitivity among the participants with an OGTT result and the fewest referrals above the 85 per cent target, because the OGTT went to everyone the 2026 rule referred and to only a random fifth of everyone else, so a rule containing the 2026 rule finds nearly every case among the tested; weighting each tested participant by the inverse of the OGTT rate in their 2026 group puts that rule at about 77 per cent among everyone screened and makes an HbA1c of 5.7 per cent or more or a random glucose of 120 mg/dL or more, at about 90 per cent, the rule with the fewest referrals that meets the target.

## Three rules

Task type: diagnostic-biomarker-accuracy (Biomedical & Clinical Research), which serves Descriptive & Distribution Analysis in the taxonomy; the setting is a health system's community diabetes screening program.
Domain test: the deciding quantity is each referral rule's sensitivity for undiagnosed diabetes among everyone screened, a diagnostic accuracy estimate under partial verification, the reference test (the OGTT) having reached everyone the old rule referred and a random fifth of the rest, estimated by weighting each verified participant by the inverse of the verification rate in their referral group; reading it among the verified, as an ordinary two-by-two table, changes which rule the program uses.
Swap: "which of six pallet-scan rules a warehouse loads for 2027, the one checking the fewest pallets that catches 85 per cent of damaged pallets" keeps a rule and a target, but loses the reference test given by a risk questionnaire and a glucose reading, the milder undiagnosed cases those signals miss, and the random fifth that alone reaches them, so the selection the call turns on has nothing to attach to and the task no longer reads the same.
Layer 1: the tablets' encounter export, where a tablet that lost its connection re-sends an event's rows (exact repeats of the encounter ID) and an adult screened again later in the season carries the same program ID with no referral; the laboratory's OGTT extract, pipe-delimited, keyed by its own accession, the program ID as the patient service center typed it from the referral letter (hyphen or leading zero dropped, lower case, digits only), dates month/day/year, an incomplete test when the two-hour sample was not taken, a missed appointment leaving no row, tests at a service center outside the adult's area. Each is how the program's and the laboratory's systems hold their records; nothing is placed to be caught, and each mishandled leaves the call where it was or fails loudly (asserted, R2).
Layer 2: estimation_fit (weighting a partially verified sample back to the population screened): the share the target asks for is over everyone screened, and the familiar two-by-two table of the verified returns the share among people the old rule selected; the choice moves every rule's sensitivity and changes the rule the program uses.
Decisive step: each verified participant weighted by the inverse of the OGTT completion rate in their 2026 group (referred by the 2026 rule, or not referred and drawn into the random fifth), the two-phase design's estimator of sensitivity among everyone screened, in place of the sensitivity read among the participants with an OGTT result.
Not semantics: an analyst who reads every field correctly (a missing OGTT as not tested, the referral flag as the 2026 rule, the evaluation draw as the random fifth) still builds the ordinary two-by-two table from the people with a result, which is how accuracy is read when everyone has the reference test; nothing on that route misreads a field, the error is in whom the table represents.
Not rule application: the protocol files the target (85 of every 100 people with undiagnosed diabetes among everyone screened), the reference standard and the choice among qualifying rules; no filed rule says how to estimate a rule's sensitivity among everyone screened from the OGTT results the season holds, and executing every filed rule on the default path recommends the 2026 rule plus an HbA1c of 6.0 or more.
Analyst test: a strong analyst who takes each adult's first screening, joins the OGTT results, reads a missing OGTT as not tested and applies the target computes each rule's sensitivity among the participants with an OGTT result and ends on the default path's answer, the 2026 rule plus an HbA1c of 6.0 per cent or more at about 93 per cent, because among the tested nearly every case was flagged by the 2026 rule.
Estimand: the screening protocol files the population (every adult screened in the 2026 season, once, at the first screening), the outcome (undiagnosed diabetes as the OGTT defines it, for every one of them, whether or not they had the test), the unit (the person screened), the comparison (85 of every 100 people with diabetes flagged) and the choice (the fewest referrals among qualifying rules, else the 2026 rule).
No decoy: no memo, prior evaluation, vendor sheet or dashboard gives a rule's sensitivity; the season's close-out report counts people screened, referred, tested and found by site and month, a question it answers correctly; no file argues for a rule.
No certified replay: no shipped file states a candidate's sensitivity or a figure the wrong method reproduces; the protocol files the quantity and leaves the estimator to the analysis.
Lesson: when the reference test reached people through another rule's signals and a random draw, a candidate's accuracy among the tested is not its accuracy among everyone screened, and the random draw's members stand for the many they were drawn from; no build on file teaches partial verification (task233 carries a missing-data departure, task264 survey weights).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 untested adults counted as free of diabetes (the default path's variant read off the season's case list) | the protocol's target counts every adult screened "whether or not they had the test", the OGTT's verdict being the one the test would give | the referral column, the OGTT results file | a confirmed-case list is how a screening season is usually counted | none | none | one ratio per rule | readable |
| R1 sensitivity among the participants with a complete OGTT (the default path) | no sentence names an estimator; the protocol says who was offered the test and why, which reads as the design of the season, not as an instruction about the table | the referral column with values RULE, EVAL and NONE | the ordinary two-by-two table of a test against its reference | none | none | one ratio per rule | readable |
| R2 sensitivity among the evaluation fifth alone (a random sample, so read as unbiased) | the protocol's population is everyone screened; the fifth was drawn only among the adults the 2026 rule did not refer | the EVAL value | use the random sample | none | none | one ratio per rule | readable |
| R3 the textbook correction, each rule's tested positives and negatives weighted by the rule's own test rates | none | none | the verification-bias correction taught for a test whose own result decided who was verified | none | none | none | readable |
| (decisive) each tested adult weighted by the inverse of the complete-test rate in their 2026 group (referred by the rule, or not referred and drawn into the fifth) | none: the protocol files the population, the reference and the target, and says who was offered the test; no document speaks of weights, verification bias or an estimator | the referral column reads as the tablet's log, not as a stratum | the two-by-two table is the reflex; the textbook correction conditions on the candidate's own result | no shipped figure states a rule's sensitivity; the close-out counts people screened, referred, tested and found | program IDs unique per adult after the first screening, OGTT accessions unique, every typed program ID joins once normalised; nothing for the battery to find | a weighted sum over two groups of the tested adults' diabetes and flags; no ratio of shipped figures | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | adult screened | each adult once, at the first screening of the season | every screening encounter | same call | the protocol's "each adult counts once, at the first screening of the season"; same call asserted |
| SF2 | undiagnosed diabetes | an OGTT with a fasting glucose of 126 mg/dL or more or a two-hour glucose of 200 or more | fasting only; two-hour only | different shares | the protocol's reference sentence names both values with "or" |
| SF3 | an OGTT result | a complete test, both samples taken | an incomplete test read on its fasting value | same call | the protocol's "a test counts when both samples were taken"; same call asserted |
| SF4 | people with undiagnosed diabetes (the target's denominator) | every adult screened whose OGTT would show diabetes, tested or not | the adults with a complete OGTT that shows diabetes | R1, R0 | the protocol's target sentence: "among everyone screened in the season, whether or not they had the test" |
| SF5 | the share it would have referred (the referral share) | the share of all adults screened the rule flags on their first screening's values | the share of encounters; of the tested | same call | the protocol's choice sentence; same call asserted for encounters |
| SF6 | the target | at least 85.0 per cent | more than 85 | same call | no rule within 1.5 points of 85 (asserted) |
| SF7 | the 2026 rule | a score of 6 or more or a random glucose of 140 mg/dL or more, as the tablet flagged it | recomputed from the fields | same call | the flag equals the recomputed rule on every encounter (asserted) |
| SF8 | a rule's inputs | the score, fingerstick glucose and point-of-care HbA1c the tablet recorded at the first screening | a later screening's values; a laboratory HbA1c | same call | the protocol; no laboratory HbA1c ships; same call asserted on the later values |
| SF9 | the evaluation fifth | drawn by the tablet among the adults the 2026 rule did not refer, one in five | read as a fifth of everyone | different weights | the protocol's draw sentence; the EVAL count is a fifth of the not-referred (asserted) |
| SF10 | the OGTT's link to the screening | the test that followed the adult's first screening (one referral per adult per season) | any test in the season | same call | the protocol's "an adult already screened this season is not referred or drawn again"; one accession per adult (asserted) |
| SF11 | ties in the referral share | none | none | none arises | no two qualifying rules within 0.5 points (asserted) |
| SF12 | the weights' rates | each group's complete tests over its adults | the draw's nominal one in five, every referred adult tested | same call | the weighted estimate with nominal rates gives the same rule (asserted) |
| SF13 | rounding | shares to one decimal from the unrounded estimate, the target compared unrounded | shares rounded first | same call | no share within 0.015 of a rounding edge, none within 1.5 of the target (asserted) |
| SF14 | none qualifies | the 2026 rule stays | none | not reached | a rule qualifies (asserted) |
| SF15 | service area and event type | one estimate over the season | per area | same call | the protocol's one target over everyone screened; the per-area weighted estimate gives the same rule (asserted) |

## Ladder

Built figures (seed 285; `checks.py` asserts every pick and margin), sensitivity per cent among everyone screened unless the rung says otherwise, and the referral share; rules in order of referral share:

| Rung | Construction | HbA1c 6.0 | 2026 rule or HbA1c 6.0 | HbA1c 5.7 | Score 5 | HbA1c 5.7 or glucose 120 | HbA1c 5.5 | Rule chosen | What kills it |
|---|---|---|---|---|---|---|---|---|---|
| Referral share | every adult screened, first screening (38,601) | 8.5 | 24.5 | 28.1 | 35.6 | 35.9 | 48.7 | | |
| R0 and R1 (default) | among the adults with a complete OGTT; counting the untested as free of diabetes gives the same sensitivity, the untested adding no case | 56.5 | 93.5 | 83.2 | 73.1 | 94.2 | 93.7 | 2026 rule or HbA1c 6.0 | the tested are the 2026 rule's referrals and a fifth of the rest; a rule containing the 2026 rule finds nearly every tested case |
| R2 | among the evaluation fifth alone | 37.5 | 37.5 | 69.2 | 25.0 | 84.2 | 90.0 | HbA1c 5.5 | the fifth was drawn only among the not-referred |
| R3 (a route) | each rule's own tested rates (the textbook correction) | 44.2 | 77.3 | 78.0 | 49.2 | 92.1 | 91.8 | HbA1c 5.7 or glucose 120 | converges here: verification followed the 2026 rule, and the data happen to agree |
| Routes | the 2026 group crossed with the rule's flag; the group by service area; by month; the draw's nominal rates | 50.3 to 50.9 | 76.9 to 77.2 | 79.1 | 59.0 to 59.4 | 91.2 to 91.3 | 92.6 | HbA1c 5.7 or glucose 120 | none |
| Golden | each adult with a complete OGTT weighted by the inverse of the complete-test rate in their 2026 group | 50.9 | 77.1 | 79.1 | 59.0 | 91.3 | 92.6 | HbA1c 5.7 or glucose 120 | none |

Position and separation: the default path's rule is second by referral share and the golden's fifth; the decisive move takes the 2026 rule plus an HbA1c of 6.0 down 16.4 points (93.5 to 77.1) and walks every rule one way (asserted). The golden's rule sits 6.3 points above the target; the rules referring fewer adults sit 5.9 (HbA1c 5.7), 7.9 (the default's rule), 26.0 (score 5) and 34.1 (HbA1c 6.0) under it; among the tested, the default's rule sits 8.5 above and the one rule referring fewer (HbA1c 6.0) 28.5 under. No golden share or referral share within 0.015 of a rounding edge, none within 1.5 of the target, no two qualifying rules within 0.5 points of share (asserted). On the clean truth (every adult's diabetes known to the generator) the rule is the same, every golden sensitivity within 3 points of the true one (asserted). Worth: the decisive step is the whole stump; the textbook correction and every finer weighting land on the golden's rule (routes, asserted).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every adult screened in the 2026 season, once, at the first screening | filed: the protocol |
| 2 Unit of account | the adult | filed: the protocol; program IDs |
| 3 Attribution window | the 2026 season (2 March to 20 November 2026) and the OGTT that followed each referral, up to the extract | filed: the protocol and the notes; C1: every OGTT follows its referral (asserted) |
| 4 As-of dating | the extracts of January 2027 | C1: no OGTT for a 2026 referral after the extract (asserted) |
| 5 Version basis | one extract of each kind | C1: no superseded file ships |
| 6 Denominator | adults with undiagnosed diabetes among everyone screened, tested or not | filed: the protocol; the estimator is the decisive step; C4 against R0, R1, R2 |
| 7 Weighting | each tested adult stands for the adults of their 2026 group | the design forces it (the decisive step) |
| 8 Window length | one season | filed |
| 9 Boundary inclusivity | at least 85.0 per cent qualifies; thresholds inside the rules inclusive (6.0 or more, 120 or more) | filed: the protocol and the candidate rules |
| 10 Rounding path | unrounded shares against the target, reported to one decimal | filed: the protocol |
| 11 Tie-break | the fewest referrals among qualifying rules | filed; C1: no two qualifying rules within 0.5 points (asserted) |
| 12 Maturity and censoring | OGTTs not kept are missing within the group's draw, not negative | the decisive step; the notes |
| 13 Order of operations | first screening, then rules, then the weighted shares | C1 |
| 14 Row order | none | C1: asserted over permutations |
| 15 Duplicate resolution | an adult's later screenings dropped | filed: the protocol; C1: same call asserted with every encounter |
| 16 Identity normalisation | the program ID the patient service center typed, normalised to the tablet's form | C4: every complete OGTT joins one adult (asserted); unnormalised, a share of tests is lost across both groups (same call asserted) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | mg/dL for glucose, per cent for HbA1c | C1: every value in range for its unit (asserted) |
| 19 Code and status semantics | referral values RULE, EVAL and NONE; OGTT status | dictionary: the notes |
| 20 Integerisation | a named rule | C1 |
| 21 Clause scope | the protocol's 2027 choice sentence | filed |
| 22 Forward window contents | the 2027 season's referral rule chosen on the 2026 season's adults | filed: the protocol |

## Literal reader

Executed word for word, the protocol counts each adult screened in the 2026 season once, at the first screening; it defines undiagnosed diabetes by the OGTT (a fasting glucose of 126 mg/dL or more or a two-hour glucose of 200 or more, a test counting when both samples were taken) for every adult screened, whether or not they had the test; it says the tablet offered the test to every adult the 2026 rule referred and to one in five of the others, drawn at random; and it takes for 2027 the candidate that refers the fewest adults among those that would have referred at least 85 per cent of the adults with undiagnosed diabetes among everyone screened. The share among everyone screened is not observed for the adults who were not tested; the one estimate the season's record supports lets each adult with a complete test stand for the adults of their own group (referred, or not referred), at the inverse of that group's rate of complete tests, which gives the golden. The share among the tested (R1) and the untested counted free of diabetes (R0) estimate another population than the one the target names; the fifth alone (R2) is the not-referred only; SF1, SF3, SF5, SF7, SF8, SF10, SF12 and SF15 converge, asserted.

## Oracles

- No shipped file states a rule's sensitivity, a referral share or a ranking of the rules; the candidate rules file lists each rule's logic as the tablet would run it.
- The season's close-out report counts, by month and service area, adults screened, return visits, referred, drawn, tested and found with diabetes; each count ties under every handling of the decisive step, and none is a share of the people with diabetes.
- Ask referees: none ships. No file states a cartridge count by analyzer, a stock count, a statement total or a monthly billed amount; each ask's device is found only by an inconsistency inside its own records (below).

## Ask sheet

The asks are decoupled from the call: neither reads the screening values or the OGTT results the call reads (Ask B reads only the OGTT extract's accession column, which the call never reads), and the call computes identically with every ask file deleted (asserted). Both are the season's records the review workbook carries beside the rule. The notes, which the call reads, describe no ask file beyond who supplied it (asserted: no device word).

**Ask A. How many HbA1c test cartridges each of the program's twelve analyzers used over the season (12 figures).**
- H18 home: the audit trail of the point-of-care HbA1c every HbA1c candidate rule runs on (the risk-score rule needs none), from the units' runs to the analyzers the program owns.
- Use: the review workbook's supplies sheet; the 2027 cartridge order starts from it.
- Path: gq200_run_log_2026.csv (serial_number, run_started, run_type, sample_id, result_pct, error_code, cartridge_lot), analyzer_asset_register.xlsx (Asset tag, Serial number, In service from, In service to), gq200_error_codes.pdf (code, where it is raised, the one-cartridge sentence), the notes (the season's dates), event_calendar_2026.csv (hours and analyzers, the cross-file evidence): five files, fifteen columns.
- Primary device (D1, the same records under two key schemes): Biomedical Engineering's run database holds every download of the units' memories, skipping a row whose serial and run time it already holds. The docking software stamped local time until its upgrade on 3 August 2026 and the unit's UTC clock after it, so every run a unit still held when it was downloaded again after the upgrade (the season-end download for every unit, the A09 and A11 units' downloads before they went to the maker, the loaner's second loan) sits in the database twice, the second copy four hours later with every other field the same: 8,651 runs, every analyzer between 74 and 1,182 of them in the season. No exact duplicate, serial and run time unique, every serial in the register: the battery finds nothing (asserted). Found only by the inconsistency inside the records: a sample's identical result four hours after itself, two controls a day doubled, copies stamped hours after their event closed (asserted on the event calendar).
- Its over-cleaning half: a result of 6.5% or more is repeated on a fresh cartridge minutes later before it is given (344 genuine same-sample pairs); counting a sample's identical rows once a day drops them.
- Hazards: the two replaced units and the loaner serve their tags by date (grouping by serial misplaces A04, A05, A09 and A11); a run stopped at the cartridge check takes no cartridge (the maker's reference, filed); controls take one; the pre-season training day (24 February) on four analyzers.
- Stops (built, totals against 41,713): every row on its tag 51,094 (each analyzer 149 to 1,266 high); error rule and season applied, every row kept 50,207 (each 74 to 1,182 high, the cracker); result rows only 49,378; rows alike but for the run time counted once a day 41,538 (each 9 to 20 low); copies removed, every error counted 42,405 (each 41 to 69 high); copies removed, the training day kept 41,750 (A01, A02, A03 and A06 high); the answer 41,713. Lazy delta 9,381.
- Realism: point-of-care analyzers keep a run memory that overlaps from one download to the next, docking software changes its time convention at an upgrade, and a database that deduplicates on serial and time cannot see one run under two clocks.

**Ask B. For each month of the season, what the laboratory billed, net of its credits, for the OGTTs done that month, and the part for tests of adults screened (18 figures, dollars).**
- H18 home: the reference test the call reads, reconciled to the laboratory's billing (what the verification the call rests on cost, month by month).
- Use: the review workbook's laboratory sheet.
- Path: thessler_invoice_lines_2026.csv (document_number, document_type, line, accession, service_date, amount_usd, applies_to), ogtt_results_2026.txt (ACCESSION): two files, eight columns.
- Primary device (D6, an event's quantity on every line it covers): the laboratory's credit memos credit one to four invoice lines each, and its account export carries the memo's whole amount on every memo line: 140 memos on 269 lines, 72 of them on two to four lines. Summing the export as it stands credits those tests two to four times over and puts every month's figures 654.50 to 2,772.00 dollars low (asserted on all eighteen). Found only by the inconsistency inside the export: a memo line larger than the invoice line it applies to, accessions netting below zero (asserted).
- Hazards: lines resubmitted on the same or the next invoice (283 accessions billed twice, most credited later), tests credited in full when the specimen was not tested, tests billed a month late, credits posted after the month of the test, other patients' tests on the program's account (196 accessions absent from the program's OGTT results).
- Stops (built): charges by the month billed (each figure 808.50 low to 2,348.50 high); charges by the month done, credits left out (423.50 to 1,963.50 high); credit memo lines at the amounts exported (654.50 to 2,772.00 low, the cracker); the same by the month billed; one charge per accession, credits applied (385.00 to 2,040.50 low); every billed test counted as the program's (each month's second figure high); the answer, $435,088.50 net, $428,274.00 for adults screened.
- Realism: credit memos apply to several lines, an export that flattens a memo onto its lines repeats the memo's amount, billing systems resubmit lines, and a health system's clinics share an account number.

Main population zero-counts: device and hazard rows in the encounters, the OGTT results' program IDs, statuses and glucose values, the protocol and the candidate rules: 0 (asserted: the call identical with every ask file deleted, the main files' columns unchanged).

| Hazard | Asks moved | Per-ask delta (built) |
|---|---|---|
| replaced units and the loaner, by date | A | A04, A05, A09 and A11 when grouped by serial |
| errors at the cartridge check | A | each analyzer 41 to 69 high when every error counts |
| the training day | A | A01, A02, A03 and A06 high |
| repeats on a fresh cartridge | A | each analyzer 9 to 20 low when a sample's identical rows count once a day |
| invoice month against the month done | B | each figure 808.50 low to 2,348.50 high |
| credits left out | B | each figure 423.50 to 1,963.50 high |
| other patients' tests | B | each month's figure for adults screened high |

Referee: none (Oracles).

| Ask figure | Cracker (lands the call, runs the battery: exact duplicates, key uniqueness on serial and run time and on accession lines, unmatched serials and accessions; executes the maker's error rule, the asset register by date and the season's dates) |
|---|---|
| A, each analyzer's cartridges (12) | miss (each 74 to 1,182 high) |
| B, each month's net billing (9) | miss (each 654.50 to 2,772.00 low) |
| B, each month's part for adults screened (9) | miss (each 654.50 to 2,772.00 low) |

Mirror leakage: 0 per cent of the ask weight (the mirror takes the same reads on both asks; `checks.py` asserts the cracker's path misses every ask figure).
Pair ceiling: 32 (the cracker about 45 on the call, its components and instruction-following, none of the asks; the mirror about 18, the six referral shares and instruction-following; about 40 if the generated rubric grades the twelve rule figures as asks; to be rerun on the generated rubric).

## Tried and rejected`); the slot draws a new world in the same objective. Sallowfield Health, a regional health system in a US state, runs a community diabetes screening program: mobile events at churches, workplaces, community centres and county fairs across its Ostervale service region, where adults without a diabetes diagnosis answer a risk questionnaire (a score from 0 to 10) and give a fingerstick for a random glucose and a point-of-care HbA1c. In the 2026 season (38,601 adults, 2 March to 20 November) the screening tablet referred for a 75 g oral glucose tolerance test (OGTT) everyone scoring 6 or more or with a random glucose of 140 mg/dL or more, and, for the season's evaluation, a random fifth of everyone it did not refer; about four in five referred people kept the appointment. The OGTT is the reference: diabetes when the fasting glucose is 126 mg/dL or more or the two-hour glucose 200 mg/dL or more. Before the 2027 season opens, the program loads one referral rule into the tablets from six candidates; its protocol takes the rule that refers the fewest people screened among the rules that find at least 85 of every 100 people with undiagnosed diabetes among everyone screened, and keeps the 2026 rule when none does. The call is forward facing: the rule runs the 2027 season.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task267.json`, architecture v1, registered 2026-10-17, the set-aside DA17 draw kept in its lineage with its fate. The health system is a health provider (`hospital_or_health_provider`); the program director sets the rule with the program's medical director, no formal forum (`line_manager_or_team`); the 2027 season's opening forces it, the rule being loaded into the tablets before the first event (`launch_or_rollout`); the requester is the program director (`operations_director`); the context artifact is the 2026 season's close-out report (`close_out_summary`); no calibration organ (the random fifth is the second phase of the season's own sampling, not a separate settled corpus). `guard.py check` before register, after a pull: BLOCKs on the calibration form, forum and forcing event against task192 v3 and task182 v2 (filed in parallel) cleared by redrawing those three axes (a random fifth that is part of the design, not a calibration corpus; the director and medical director deciding; the season's launch); WARNs answered below.
2. Pairing: Biomedical & Clinical Research (client domain) / diagnostic-biomarker-accuracy / Descriptive & Distribution Analysis. The task type's own object, a test's sensitivity in the population tested when the reference standard reached only part of it, decides the call (the client's rigor pattern biomedical-clinical-research/diagnostic-biomarker-accuracy/1, partial verification); the setting is a health system's community screening program.
3. Niche: a community screening program whose reference test followed its own referral rule plus a random fifth of everyone else, choosing the next season's referral rule among candidates the old verification design was never built around.
4. Call and shape: which of six referral rules the 2027 tablets carry (`pick_one_of_n`, question form which). Shape 10 (a scorecard of metric against threshold): each rule's sensitivity among everyone screened against the 85 per cent target, with each rule's share of those screened it refers.
5. Gate G `method_or_model_selection` (the estimator the season's two-phase verification design entitles against the complete-case reading), strategy `population_selection` (the participants with an OGTT result were selected by the old rule's own signals), decisive generator G14 (the tested participants' diabetes rate carries to the untested only within the 2026 referral groups), then G12 (a missing OGTT is a non-answer, not a negative) and G16 (the weighting the design entitles).
6. Data-native sentence: the 2026 tablets sent everyone the old rule flagged (a questionnaire score of 6 or more or a random glucose of 140 mg/dL or more) and a random fifth of everyone else to the OGTT, so who has a reference result depends on the old rule's signals; the people with undiagnosed diabetes whom the old rule does not flag, a third or more of all cases and milder ones, reach a result only through the random fifth, each standing for about six others, and every candidate that contains the old rule finds nearly every case among the tested.
7. Sources, one line each:
   - The client's rigor library, diagnostic-biomarker-accuracy pattern 1 (partial verification biases accuracy; Begg-Greenes or inverse probability of verification weighting): this build's verification follows another rule's signals, not the candidate's own result, so the textbook correction by the candidate's result is not the design's estimator.
   - task260 in this lane (a breast screening service's reader study, readers and examinations both random): another screening decision, a different object (variance of an AUC across readers), nothing verified partially.
   - task233 (a gold-standard follow-up carrying a missing-against-imputed departure as an odds ratio): a follow-up sample of missing values; here no departure is modelled, the verification probabilities being known by design.
   - task264 and task261 in this lane (survey weights, replicate variance): weighting by inverse probabilities is the shared device; here it is the field's verification correction for a diagnostic accuracy estimate, its strata the old referral rule's groups.
   - task265 and task266 in this lane (survival with late entry; competing exits): no time-to-event structure here.
8. People, drawn with `guard.py names --geo "united states" --seed 267`: Aaron Bradley (director of the community screening program, the requester), Ariel Tucker (the program's medical director, who owns the screening protocol), Bryan Gardner (data manager, author of the extract notes), Matthew Garcia (the program analyst who writes the goldens). The suggestion list filters names already on file, so a rerun now omits these four. Invented names (Sallowfield, Orlenby, Fenwater, Drummery, Pellowmoor, Quessly, Thessler, Glyquant) screened against geonamescache's places, counties, states and countries and a curated list of small places (H21, asserted); sites and tablets carry codes.
9. WARNs answered: `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, against task192 v3 and task182 v2, 6 of the last 12): it is the honest mechanism here (two readings of the season's OGTT results, the design deciding between them), and the batch varies elsewhere (a diagnostic accuracy estimate under partial verification, a pick, shape 10, a health provider); `repeat.question_form` (which, against task182 v2): the decision is a pick among six named rules, so the question asks which.

## Default path

1. Read the protocol: the 2027 rule must find at least 85 of every 100 people with undiagnosed diabetes among everyone screened, and among those that do, the rule that refers the fewest people screened is used.
2. Take each adult's first screening of the 2026 season from the tablets' event exports, join the reference laboratory's OGTT results through the program ID the patient service center typed, and classify each completed OGTT (fasting 126 mg/dL or more, or two-hour 200 or more).
3. For each candidate rule, the sensitivity: among the participants whose OGTT shows diabetes, the share the rule flags; the referral share: the share of everyone screened the rule flags.
4. The rule with the lowest referral share among those at 85 per cent or more.

Ends on: the 2026 rule plus an HbA1c of 6.0 per cent or more, about 93 per cent sensitivity among the tested with about a quarter of those screened referred (the simulation at the draw; built figures replace these).
Golden: an HbA1c of 5.7 per cent or more or a random glucose of 120 mg/dL or more, about 90 per cent among everyone screened with about 36 per cent referred; the 2026 rule plus an HbA1c of 6.0 or more reads about 77 per cent among everyone screened, and an HbA1c of 5.7 or more alone about 81.

## Stump sentence

The default path recommends the 2026 rule plus an HbA1c of 6.0 per cent or more, at about 93 per cent sensitivity among the participants with an OGTT result and the fewest referrals above the 85 per cent target, because the OGTT went to everyone the 2026 rule referred and to only a random fifth of everyone else, so a rule containing the 2026 rule finds nearly every case among the tested; weighting each tested participant by the inverse of the OGTT rate in their 2026 group puts that rule at about 77 per cent among everyone screened and makes an HbA1c of 5.7 per cent or more or a random glucose of 120 mg/dL or more, at about 90 per cent, the rule with the fewest referrals that meets the target.

## Three rules

Task type: diagnostic-biomarker-accuracy (Biomedical & Clinical Research), which serves Descriptive & Distribution Analysis in the taxonomy; the setting is a health system's community diabetes screening program.
Domain test: the deciding quantity is each referral rule's sensitivity for undiagnosed diabetes among everyone screened, a diagnostic accuracy estimate under partial verification, the reference test (the OGTT) having reached everyone the old rule referred and a random fifth of the rest, estimated by weighting each verified participant by the inverse of the verification rate in their referral group; reading it among the verified, as an ordinary two-by-two table, changes which rule the program uses.
Swap: "which of six pallet-scan rules a warehouse loads for 2027, the one checking the fewest pallets that catches 85 per cent of damaged pallets" keeps a rule and a target, but loses the reference test given by a risk questionnaire and a glucose reading, the milder undiagnosed cases those signals miss, and the random fifth that alone reaches them, so the selection the call turns on has nothing to attach to and the task no longer reads the same.
Layer 1: the tablets' encounter export, where a tablet that lost its connection re-sends an event's rows (exact repeats of the encounter ID) and an adult screened again later in the season carries the same program ID with no referral; the laboratory's OGTT extract, pipe-delimited, keyed by its own accession, the program ID as the patient service center typed it from the referral letter (hyphen or leading zero dropped, lower case, digits only), dates month/day/year, an incomplete test when the two-hour sample was not taken, a missed appointment leaving no row, tests at a service center outside the adult's area. Each is how the program's and the laboratory's systems hold their records; nothing is placed to be caught, and each mishandled leaves the call where it was or fails loudly (asserted, R2).
Layer 2: estimation_fit (weighting a partially verified sample back to the population screened): the share the target asks for is over everyone screened, and the familiar two-by-two table of the verified returns the share among people the old rule selected; the choice moves every rule's sensitivity and changes the rule the program uses.
Decisive step: each verified participant weighted by the inverse of the OGTT completion rate in their 2026 group (referred by the 2026 rule, or not referred and drawn into the random fifth), the two-phase design's estimator of sensitivity among everyone screened, in place of the sensitivity read among the participants with an OGTT result.
Not semantics: an analyst who reads every field correctly (a missing OGTT as not tested, the referral flag as the 2026 rule, the evaluation draw as the random fifth) still builds the ordinary two-by-two table from the people with a result, which is how accuracy is read when everyone has the reference test; nothing on that route misreads a field, the error is in whom the table represents.
Not rule application: the protocol files the target (85 of every 100 people with undiagnosed diabetes among everyone screened), the reference standard and the choice among qualifying rules; no filed rule says how to estimate a rule's sensitivity among everyone screened from the OGTT results the season holds, and executing every filed rule on the default path recommends the 2026 rule plus an HbA1c of 6.0 or more.
Analyst test: a strong analyst who takes each adult's first screening, joins the OGTT results, reads a missing OGTT as not tested and applies the target computes each rule's sensitivity among the participants with an OGTT result and ends on the default path's answer, the 2026 rule plus an HbA1c of 6.0 per cent or more at about 93 per cent, because among the tested nearly every case was flagged by the 2026 rule.
Estimand: the screening protocol files the population (every adult screened in the 2026 season, once, at the first screening), the outcome (undiagnosed diabetes as the OGTT defines it, for every one of them, whether or not they had the test), the unit (the person screened), the comparison (85 of every 100 people with diabetes flagged) and the choice (the fewest referrals among qualifying rules, else the 2026 rule).
No decoy: no memo, prior evaluation, vendor sheet or dashboard gives a rule's sensitivity; the season's close-out report counts people screened, referred, tested and found by site and month, a question it answers correctly; no file argues for a rule.
No certified replay: no shipped file states a candidate's sensitivity or a figure the wrong method reproduces; the protocol files the quantity and leaves the estimator to the analysis.
Lesson: when the reference test reached people through another rule's signals and a random draw, a candidate's accuracy among the tested is not its accuracy among everyone screened, and the random draw's members stand for the many they were drawn from; no build on file teaches partial verification (task233 carries a missing-data departure, task264 survey weights).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 untested adults counted as free of diabetes (the default path's variant read off the season's case list) | the protocol's target counts every adult screened "whether or not they had the test", the OGTT's verdict being the one the test would give | the referral column, the OGTT results file | a confirmed-case list is how a screening season is usually counted | none | none | one ratio per rule | readable |
| R1 sensitivity among the participants with a complete OGTT (the default path) | no sentence names an estimator; the protocol says who was offered the test and why, which reads as the design of the season, not as an instruction about the table | the referral column with values RULE, EVAL and NONE | the ordinary two-by-two table of a test against its reference | none | none | one ratio per rule | readable |
| R2 sensitivity among the evaluation fifth alone (a random sample, so read as unbiased) | the protocol's population is everyone screened; the fifth was drawn only among the adults the 2026 rule did not refer | the EVAL value | use the random sample | none | none | one ratio per rule | readable |
| R3 the textbook correction, each rule's tested positives and negatives weighted by the rule's own test rates | none | none | the verification-bias correction taught for a test whose own result decided who was verified | none | none | none | readable |
| (decisive) each tested adult weighted by the inverse of the complete-test rate in their 2026 group (referred by the rule, or not referred and drawn into the fifth) | none: the protocol files the population, the reference and the target, and says who was offered the test; no document speaks of weights, verification bias or an estimator | the referral column reads as the tablet's log, not as a stratum | the two-by-two table is the reflex; the textbook correction conditions on the candidate's own result | no shipped figure states a rule's sensitivity; the close-out counts people screened, referred, tested and found | program IDs unique per adult after the first screening, OGTT accessions unique, every typed program ID joins once normalised; nothing for the battery to find | a weighted sum over two groups of the tested adults' diabetes and flags; no ratio of shipped figures | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | adult screened | each adult once, at the first screening of the season | every screening encounter | same call | the protocol's "each adult counts once, at the first screening of the season"; same call asserted |
| SF2 | undiagnosed diabetes | an OGTT with a fasting glucose of 126 mg/dL or more or a two-hour glucose of 200 or more | fasting only; two-hour only | different shares | the protocol's reference sentence names both values with "or" |
| SF3 | an OGTT result | a complete test, both samples taken | an incomplete test read on its fasting value | same call | the protocol's "a test counts when both samples were taken"; same call asserted |
| SF4 | people with undiagnosed diabetes (the target's denominator) | every adult screened whose OGTT would show diabetes, tested or not | the adults with a complete OGTT that shows diabetes | R1, R0 | the protocol's target sentence: "among everyone screened in the season, whether or not they had the test" |
| SF5 | the share it would have referred (the referral share) | the share of all adults screened the rule flags on their first screening's values | the share of encounters; of the tested | same call | the protocol's choice sentence; same call asserted for encounters |
| SF6 | the target | at least 85.0 per cent | more than 85 | same call | no rule within 1.5 points of 85 (asserted) |
| SF7 | the 2026 rule | a score of 6 or more or a random glucose of 140 mg/dL or more, as the tablet flagged it | recomputed from the fields | same call | the flag equals the recomputed rule on every encounter (asserted) |
| SF8 | a rule's inputs | the score, fingerstick glucose and point-of-care HbA1c the tablet recorded at the first screening | a later screening's values; a laboratory HbA1c | same call | the protocol; no laboratory HbA1c ships; same call asserted on the later values |
| SF9 | the evaluation fifth | drawn by the tablet among the adults the 2026 rule did not refer, one in five | read as a fifth of everyone | different weights | the protocol's draw sentence; the EVAL count is a fifth of the not-referred (asserted) |
| SF10 | the OGTT's link to the screening | the test that followed the adult's first screening (one referral per adult per season) | any test in the season | same call | the protocol's "an adult already screened this season is not referred or drawn again"; one accession per adult (asserted) |
| SF11 | ties in the referral share | none | none | none arises | no two qualifying rules within 0.5 points (asserted) |
| SF12 | the weights' rates | each group's complete tests over its adults | the draw's nominal one in five, every referred adult tested | same call | the weighted estimate with nominal rates gives the same rule (asserted) |
| SF13 | rounding | shares to one decimal from the unrounded estimate, the target compared unrounded | shares rounded first | same call | no share within 0.015 of a rounding edge, none within 1.5 of the target (asserted) |
| SF14 | none qualifies | the 2026 rule stays | none | not reached | a rule qualifies (asserted) |
| SF15 | service area and event type | one estimate over the season | per area | same call | the protocol's one target over everyone screened; the per-area weighted estimate gives the same rule (asserted) |

## Ladder

Built figures (seed 285; `checks.py` asserts every pick and margin), sensitivity per cent among everyone screened unless the rung says otherwise, and the referral share; rules in order of referral share:

| Rung | Construction | HbA1c 6.0 | 2026 rule or HbA1c 6.0 | HbA1c 5.7 | Score 5 | HbA1c 5.7 or glucose 120 | HbA1c 5.5 | Rule chosen | What kills it |
|---|---|---|---|---|---|---|---|---|---|
| Referral share | every adult screened, first screening (38,601) | 8.5 | 24.5 | 28.1 | 35.6 | 35.9 | 48.7 | | |
| R0 and R1 (default) | among the adults with a complete OGTT; counting the untested as free of diabetes gives the same sensitivity, the untested adding no case | 56.5 | 93.5 | 83.2 | 73.1 | 94.2 | 93.7 | 2026 rule or HbA1c 6.0 | the tested are the 2026 rule's referrals and a fifth of the rest; a rule containing the 2026 rule finds nearly every tested case |
| R2 | among the evaluation fifth alone | 37.5 | 37.5 | 69.2 | 25.0 | 84.2 | 90.0 | HbA1c 5.5 | the fifth was drawn only among the not-referred |
| R3 (a route) | each rule's own tested rates (the textbook correction) | 44.2 | 77.3 | 78.0 | 49.2 | 92.1 | 91.8 | HbA1c 5.7 or glucose 120 | converges here: verification followed the 2026 rule, and the data happen to agree |
| Routes | the 2026 group crossed with the rule's flag; the group by service area; by month; the draw's nominal rates | 50.3 to 50.9 | 76.9 to 77.2 | 79.1 | 59.0 to 59.4 | 91.2 to 91.3 | 92.6 | HbA1c 5.7 or glucose 120 | none |
| Golden | each adult with a complete OGTT weighted by the inverse of the complete-test rate in their 2026 group | 50.9 | 77.1 | 79.1 | 59.0 | 91.3 | 92.6 | HbA1c 5.7 or glucose 120 | none |

Position and separation: the default path's rule is second by referral share and the golden's fifth; the decisive move takes the 2026 rule plus an HbA1c of 6.0 down 16.4 points (93.5 to 77.1) and walks every rule one way (asserted). The golden's rule sits 6.3 points above the target; the rules referring fewer adults sit 5.9 (HbA1c 5.7), 7.9 (the default's rule), 26.0 (score 5) and 34.1 (HbA1c 6.0) under it; among the tested, the default's rule sits 8.5 above and the one rule referring fewer (HbA1c 6.0) 28.5 under. No golden share or referral share within 0.015 of a rounding edge, none within 1.5 of the target, no two qualifying rules within 0.5 points of share (asserted). On the clean truth (every adult's diabetes known to the generator) the rule is the same, every golden sensitivity within 3 points of the true one (asserted). Worth: the decisive step is the whole stump; the textbook correction and every finer weighting land on the golden's rule (routes, asserted).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every adult screened in the 2026 season, once, at the first screening | filed: the protocol |
| 2 Unit of account | the adult | filed: the protocol; program IDs |
| 3 Attribution window | the 2026 season (2 March to 20 November 2026) and the OGTT that followed each referral, up to the extract | filed: the protocol and the notes; C1: every OGTT follows its referral (asserted) |
| 4 As-of dating | the extracts of January 2027 | C1: no OGTT for a 2026 referral after the extract (asserted) |
| 5 Version basis | one extract of each kind | C1: no superseded file ships |
| 6 Denominator | adults with undiagnosed diabetes among everyone screened, tested or not | filed: the protocol; the estimator is the decisive step; C4 against R0, R1, R2 |
| 7 Weighting | each tested adult stands for the adults of their 2026 group | the design forces it (the decisive step) |
| 8 Window length | one season | filed |
| 9 Boundary inclusivity | at least 85.0 per cent qualifies; thresholds inside the rules inclusive (6.0 or more, 120 or more) | filed: the protocol and the candidate rules |
| 10 Rounding path | unrounded shares against the target, reported to one decimal | filed: the protocol |
| 11 Tie-break | the fewest referrals among qualifying rules | filed; C1: no two qualifying rules within 0.5 points (asserted) |
| 12 Maturity and censoring | OGTTs not kept are missing within the group's draw, not negative | the decisive step; the notes |
| 13 Order of operations | first screening, then rules, then the weighted shares | C1 |
| 14 Row order | none | C1: asserted over permutations |
| 15 Duplicate resolution | an adult's later screenings dropped | filed: the protocol; C1: same call asserted with every encounter |
| 16 Identity normalisation | the program ID the patient service center typed, normalised to the tablet's form | C4: every complete OGTT joins one adult (asserted); unnormalised, a share of tests is lost across both groups (same call asserted) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | mg/dL for glucose, per cent for HbA1c | C1: every value in range for its unit (asserted) |
| 19 Code and status semantics | referral values RULE, EVAL and NONE; OGTT status | dictionary: the notes |
| 20 Integerisation | a named rule | C1 |
| 21 Clause scope | the protocol's 2027 choice sentence | filed |
| 22 Forward window contents | the 2027 season's referral rule chosen on the 2026 season's adults | filed: the protocol |

## Literal reader

Executed word for word, the protocol counts each adult screened in the 2026 season once, at the first screening; it defines undiagnosed diabetes by the OGTT (a fasting glucose of 126 mg/dL or more or a two-hour glucose of 200 or more, a test counting when both samples were taken) for every adult screened, whether or not they had the test; it says the tablet offered the test to every adult the 2026 rule referred and to one in five of the others, drawn at random; and it takes for 2027 the candidate that refers the fewest adults among those that would have referred at least 85 per cent of the adults with undiagnosed diabetes among everyone screened. The share among everyone screened is not observed for the adults who were not tested; the one estimate the season's record supports lets each adult with a complete test stand for the adults of their own group (referred, or not referred), at the inverse of that group's rate of complete tests, which gives the golden. The share among the tested (R1) and the untested counted free of diabetes (R0) estimate another population than the one the target names; the fifth alone (R2) is the not-referred only; SF1, SF3, SF5, SF7, SF8, SF10, SF12 and SF15 converge, asserted.

## Oracles

- No shipped file states a rule's sensitivity, a referral share or a ranking of the rules; the candidate rules file lists each rule's logic as the tablet would run it.
- The season's close-out report counts, by month and service area, adults screened, return visits, referred, drawn, tested and found with diabetes; each count ties under every handling of the decisive step, and none is a share of the people with diabetes.
- Ask referees: none ships. No file states a cartridge count by analyzer, a stock count, a statement total or a monthly billed amount; each ask's device is found only by an inconsistency inside its own records (below).

## Ask sheet

The asks are decoupled from the call: neither reads the encounters' screening values or the OGTT results as the call does, and the main population (the encounters file, the OGTT results for screened adults, the protocol, the candidate rules) carries zero device rows (asserted: the call computes identically with every ask file deleted). Both asks are the season's records the review workbook carries beside the rule.

**Ask A. How many HbA1c test cartridges each of the program's twelve analysers used in the 2026 season (twelve figures).**
- H18 home: the audit trail of the point-of-care HbA1c the call reads, from the analysers' run logs to the cartridge stock count.
- Use: the review workbook's supplies sheet; the 2027 cartridge order starts from it.
- Path: the analysers' run log (serial number, run time, run type, result or error code, cartridge lot), the asset register (asset tag, serial number, in service from and to), the analyser's error code reference (which errors are raised before a cartridge is inserted), the event calendar (the season's days), the protocol (the season's dates), the notes: six files, about fourteen columns.
- Primary device (D7, the true key elsewhere): the run log is keyed by the unit's serial number, and the program counts its analysers by asset tag; two analysers were replaced mid-season by units that took over the same asset tag, and a loaner unit served two asset tags at different times, so runs grouped by serial land on the wrong analyser or on none.
- Secondary (a stated rule, legal in an ask): an error raised before the cartridge is inserted uses no cartridge, one raised after it uses one; the error code reference says which.
- Hazards: control runs (two levels each event day) use cartridges; runs at a pre-season training day fall outside the season.
- Stops (design): result rows by serial; every run row by serial; every run row by the serial's tag ignoring dates; the error rule misapplied (every error counted); the training day kept; the answer.
- Realism: point-of-care analysers log by serial, programs track assets by tag, and replacement units take the tag of the unit they replace.

**Ask B. For each month of the 2026 season, how many OGTTs the laboratory billed the program for, and how many of those were tests of adults the program screened (eighteen figures).**
- H18 home: the reference test the call reads, reconciled to the laboratory's billing.
- Use: the review workbook's laboratory sheet.
- Path: the laboratory's invoice lines (invoice, invoice date, line, accession, service date, test code, amount), the OGTT results file (accession, program ID), the encounters (program IDs), the notes: four files, about twelve columns.
- Primary device (D1, a resubmission under a fresh line): the laboratory's billing system resubmits a line it believes rejected, under a new line number on a later invoice, and credits the duplicate on a later invoice when the program queries it, so lines and tests differ and the credit sits in another month.
- Secondary (D5, scope known by structure): the health system's clinic drew OGTTs on the program's requisition stock and the laboratory billed them to the program's account; their accessions are not in the program's results extract.
- Hazard: invoice month against month of service.
- Stops (design): lines by invoice month; lines by month of service; duplicates kept; credits netted in the month they post; the clinic's tests kept as the program's; the answer.
- Realism: laboratory billing resubmits and credits lines across invoices, and requisition stock is shared within a health system.

Main population zero-counts: device and hazard rows in the encounters, the OGTT results for screened adults, the protocol and the candidate rules: 0 (asserted).

| Hazard | Asks moved | Per-ask delta (design) |
|---|---|---|
| control runs | A | every analyser low when dropped |
| the pre-season training day | A | four analysers high when kept |
| invoice month against service month | B | March to November shifted by a month's late lines |
| credits posted in a later month | B | the credited months low when netted where they post |

Referee: the cartridge stock count for Ask A (program-wide), the laboratory's statement total for Ask B (net, not by month); none ties only under the golden, and no file states a cartridge count by analyser or a monthly test count.

| Ask figure | Cracker (lands the call, runs the battery, executes the protocol and the notes) |
|---|---|
| A, each analyser's cartridges used (12) | miss |
| B, each month's OGTTs billed and those for adults screened (18) | miss |

Mirror leakage: 0 per cent of ask weight (the mirror stops at R1 on the call and takes the same natural reads on the asks; `checks.py` asserts the cracker's path hits no ask figure).
Pair ceiling: 32 (cracker 45 on the call and instruction-following plus 3 for the chart, 0 of the asks; mirror 5 plus 7 plus 3 for the chart's form; to be rerun on the generated rubric).

## Tried and rejected

- Seed DA17, an annuity insurer's size-banded rates for six markets, worked at the draw 2026-10-17 and never registered: the world serves the Descriptive objective only through sociology-demography's life-table task type (a third sociology-demography Descriptive build after task262 and task266, the actuarial mortality-longevity task type serving forecasting only); the seed's contract-against-annuitant grain is identity resolution, a reading, banned as the decisive step; its analytical stump, deaths notified late for small pensions estimated from the notification delays, would file an estimate of the not-yet-observed in the governing document for a second consecutive build after task266's Policy 3.3.
- A tuberculosis active case-finding campaign choosing its 2027 triage test (the same partial-verification move, sputum tested by the old algorithm and a random twentieth), worked at the draw 2026-10-17 and set aside before the card was filed: at about one per cent prevalence the random sample of the untriggered holds a handful of cases, so every weighted sensitivity rests on about six people and moves several points between draws of the same process; the any-abnormality chest X-ray also met the target under every estimator, the textbook correction included.
- The first ask devices, set aside at stage 3 on 2026-10-17: Ask A turned on the asset register's dates, the maker's error rule and the training day, Ask B on resubmitted lines with their credits, the clinic's tests and the invoice month; each is a filed rule or a battery step the careful solver executes, and the cracker sheet hit all thirty figures. The cartridge stock count and the laboratory's statement total planned as referees were oracles and never shipped.
- Requisition numbers linking the OGTT extract to the invoices, set aside at stage 3 on 2026-10-17: a requisition number on the clinic's tests marked them, and on the program's duplicated the accession join; the invoices carry accessions only.
- Ask B in tests rather than dollars, set aside at stage 3 on 2026-10-17: counting accessions with a charge left, row against row, escapes the memo amounts, while every dollar figure carries them.
- The names Ostervale, Lindqvale, Cressfield and Elverston, set aside at stage 3 on 2026-10-17: two letters or fewer from Osterville, Lindale, Crossfield and Everton (H21); Orlenby, Thessler, Drummery and Pellowmoor clear the screen, and no figure moved.
