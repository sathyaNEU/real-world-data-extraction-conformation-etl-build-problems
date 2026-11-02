# task483 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

The number was re-tasked by the author on 2026-11-01 from Data Extraction & Conformation (ETL) to Opportunity Sizing &
Decision Support, retirement not taken, after architecture 1 (the College Scorecard-style workforce value designation)
came back on the portal's determinism block of 10-28 and the 11-01 draw found no ETL ground left. `START_HERE.md` is
not edited: the range fixes which objective a number belongs to and nothing else, and the card and the ledger carry
the real objective.

Architecture 2, drawn 2026-11-02 (Opportunity Sizing & Decision Support; Pharmacology, Pharmacoepidemiology &
Safety): Hollinbrook Health Federation, a GP federation owned by its member practices in an English county area,
places the two stewardship pharmacists of its 2027-28 UTI pathway in two of its primary care networks for the year.
Each pharmacist works with one network's practices to move first courses for uncomplicated lower urinary tract
infection in women aged 16 to 64 off other antibiotics and onto the federation's first-line nitrofurantoin. The
pathway specification places them where that move stops the most first courses meeting an organism the laboratory
reports resistant to the drug given, priced on the networks' 2026 first courses.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task483.json` (architecture v2; architecture v1 in `lineage` with its
  fate and its prompt shell in `lineage_shells`), filed 2026-11-02; `guard.py validate` 306 cards, 0 invalid. `guard.py
  check` on the registered card: WARN only without task202 v6, PASS with it. The warnings answered: `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection in task190 and in five of the
  last twelve): the honest mechanism, since the call turns on which estimate of a drug's resistance the data entitle,
  and the FINE-numbers move is new (a culture sent because a course failed, not a covariate, a band or a fit);
  `test.same_driver_older` against task308 v3 (objective, G14, method_or_model_selection) answered by the card's
  differentiation (task308 conditions availability on the hours priced; here the record itself is made by the outcome).
- **Axes drawn against the window** (task232, task190 and task456 live at the draw; task202 v6 registered on its own
  branch at 00:23Z on 11-02 and is treated as in the window): forum line_manager_or_team (the federation's clinical
  director places the pharmacists; committee_or_panel, executive_team, funder_or_donor and trustees_or_governors are in
  the window, and no committee decides a placement inside a contract the federation already holds); forcing event
  launch_or_rollout (the pathway's 2027-28 year starts on 1 April 2027); organisation cooperative_or_member_body (a GP
  federation is owned by its member practices). Redrawn after task202 v6 filed programme_officer and filed_standard:
  role compliance_or_audit (the federation's antimicrobial stewardship lead audits antibiotic prescribing against the
  federation's guideline, which is the work this placement rests on, so the family is the honest one rather than a
  passing one) and context artifact register (the federation's member practice register, its own master list of
  practices, codes and networks with the 2026 merger, over which the placement is laid; the pathway specification
  stays the governing document of `Pins:`); question form where (a placement asks where the pharmacists go, and
  which repeats task202's form). The registered card re-checked with task202 v6 in place: PASS. The structural signature was redrawn before
  filing: population first with G14 repeats task445 inside the batch and population with G6 repeats nine older builds,
  while the honest reading of the gap is objective (gap 3: the laboratory's resistance rates are correct for the
  cultures it receives and are not the rate the placement is scored on), population second.
- **Pairing:** Pharmacology, Pharmacoepidemiology & Safety, task type `benefit-risk-assessment`, which serves
  Opportunity Sizing & Decision Support: the coverage side of an empiric antibiotic's benefit-risk (the first courses a
  drug gives against an organism it cannot treat) sized network by network as the mismatched first courses the
  pathway would stop, pool (each network's 2026 first courses on other drugs) to realisable (the mismatches that moving
  them to nitrofurantoin removes). The never-built pairing pharmacology by Opportunity Sizing; no antibiotic or
  antimicrobial resistance build is on file in any objective.
- **The decision and the quantity:** which two networks get the 2027-28 pharmacists (a slate of two under a cap of two).
  For each network: its 2026 first courses for uncomplicated lower UTI in women aged 16 to 64 on each antibiotic other
  than nitrofurantoin, and the mismatched first courses that moving them would have stopped (each course's chance of
  meeting a resistant organism, less nitrofurantoin's). Forward facing: the placement is for April 2027 to March 2028;
  the 2026 courses are the specification's planning basis, filed.
- **Shape:** `01`, a ranked list under a cap: each network's off-guideline first courses by drug and its mismatched
  courses stopped, the two named, the runner-up and the gap; the asks on records the call never reads (fixed at
  stage 2); the chart's named parts; the files.
- **Strategy:** `population_selection` (the evidence the coverage is read on is a sample selected by the outcome);
  Gate G `method_or_model_selection`; gap objective then population; pattern none; generators G14 (conditioned yield:
  the laboratory's rate is conditioned on how a culture came to be sent), G6 (the cultured infections' composition),
  G9. Layer 2 family `estimand_identification` (selection on the outcome), pattern `own:empiric coverage read on the
  cultures taken before any course, not on every culture the laboratory receives`. No calibration organ.
- **World:** Hollinbrook Health Federation (member practices in seven primary care networks: Kesterby, Ashwell Vale,
  Morrow Cross, Tamsey, Stanbridge North, Upper Lode and Brackenholt; two Stanbridge North practices merge under one
  code in 2026), the county's pathology network laboratory, the ICB that commissions the pathway. People from
  `guard.py names --geo "United Kingdom" --seed 483`: Josephine James (the federation's antimicrobial stewardship lead)
  and Andrew Gibson (the laboratory's consultant microbiologist). They author documents; neither appears in the prompt.
- **Forcing fact:** the pharmacists start on 1 April 2027 and stay in their networks for the year.
- **Data-native sentence:** a GP sends a urine culture after a first course fails far more often than at a first
  consultation, so the laboratory's isolates are drawn mostly from the infections the federation's current first
  courses failed on, and one culture reports the organism against every drug at once; nitrofurantoin's and
  trimethoprim's failed courses therefore send the laboratory the organisms resistant to them (Proteus, Klebsiella,
  the resistant E. coli) and few of the Staphylococcus saprophyticus first infections that pivmecillinam cannot treat,
  and only the cultures sent before any UTI antibiotic in the episode sample the infections a first course meets.
- **Abstraction sentence:** a choice's failure share among the cases a first choice treats is read from records made
  mostly after a first choice has failed, so the current choices' own failures fill the record with the cases they
  fail on and shrink every alternative's apparent gain; read on the records made before any choice was given, the
  comparison reverses. Against the nearest approved and delivered builds: task269 v5 samples audit occasions on a
  common cause of the outcome (shift staffing) and repairs it by modelling compliance on that cause; task128 reads an
  effect on the days an operating constraint assigned it; task303 removes a shared loss logged at every sibling unit;
  task264 weights intercept respondents by their visit frequency. None has a record made by the outcome it measures,
  and the sentence cannot be written against any of them.
- **The WHAT screen.** Population: each network's 2026 first courses for uncomplicated lower UTI in women aged 16 to 64
  on an antibiotic other than nitrofurantoin (filed). Outcome: the course meets an organism the laboratory reports
  resistant to the drug (filed). Unit: a first course. Window: calendar 2026 courses; the 2024 to 2026 cultures.
  Comparison: the same course on nitrofurantoin. The decisive step settles none of them: it is which cultures estimate
  the chance a first course meets a resistant organism, a method the WHAT leaves to the analyst.
- **Same-puzzle and same-driver tests:** (objective, G14, ranked_slate_under_cap) and (objective, G14,
  method_or_model_selection) against the last twelve builds, lineage included: none; task308 v3 (older) differentiated
  on the card.
- **Sources, one line each:**
  - NICE NG109 (lower UTI, antimicrobial prescribing): nitrofurantoin first choice for non-pregnant women; send a urine
    culture when symptoms do not improve or recur after treatment, not routinely at a first presentation under 65;
  - CLSI M39 (cumulative antibiograms): first isolate per patient per period, the standard construction for empiric
    guidance;
  - urinary isolates from routine laboratory data over-represent treatment failures and complicated infections, so
    surveillance resistance runs above the resistance of uncomplicated community infections;
  - pivmecillinam has no useful activity against Staphylococcus saprophyticus or enterococci; Proteus mirabilis is
    intrinsically resistant to nitrofurantoin; EUCAST expert rules report intrinsic resistance as resistant.

## Default path

1. Read the pathway specification: the pharmacists go to the two networks whose 2026 first courses on antibiotics other
   than nitrofurantoin would have met the most organisms resistant to the drug given beyond what the same courses on
   nitrofurantoin would have met.
2. Conform the GP issue extract: the six UTI antibiotics under their brand, generic and strength names, women aged 16
   to 64, first courses as the specification defines them, the merged Stanbridge North practices under their network.
3. Count each network's 2026 first courses by drug.
4. Build the federation's community urine antibiogram from the laboratory export the way CLSI M39 builds one: women
   aged 16 to 64, first isolate per woman per organism a year, every organism, each drug's resistant share, expert-rule
   resistance counted as resistant.
5. Price each off-guideline course at its drug's resistance less nitrofurantoin's, sum by network, take the two
   largest.

Ends on: Kesterby and Ashwell Vale, whose courses on other antibacterials are mostly trimethoprim; the antibiogram
reads nitrofurantoin at 19.0 per cent of 7,352 first isolates and pivmecillinam at 21.2, so moving pivmecillinam,
fosfomycin, cefalexin or co-amoxiclav courses to nitrofurantoin looks worth almost nothing or less (Kesterby 34.1,
Ashwell Vale 26.9, then Upper Lode 10.0, Morrow Cross 8.9 and Tamsey 4.7).

Golden: Morrow Cross and Tamsey, about 70 mismatched first courses stopped each (73.3 and 67.5 unrounded), runner-up
Kesterby about 50 (47.5). Read on the 4,658 cultures sent at a first course's own consultation, nitrofurantoin meets a
resistant organism in 5.4 per cent of first courses, pivmecillinam in 13.1 and fosfomycin in 9.9.

## Stump sentence

The default path prices each off-guideline first course at its antibacterial's resistance in the federation's 2024 to
2026 community urine antibiogram for women aged 16 to 64, first isolate per woman and organism a year, where
nitrofurantoin reads 19.0 per cent because a culture follows nearly every failed course and nitrofurantoin's failures
send the laboratory the organisms resistant to it, so moving pivmecillinam and fosfomycin courses to nitrofurantoin
looks worthless and the pharmacists go to Kesterby and Ashwell Vale for their trimethoprim; read on the cultures sent
at a first course's own consultation, nitrofurantoin is 5.4 per cent against pivmecillinam's 13.1 and fosfomycin's 9.9,
and Morrow Cross and Tamsey stop the most mismatched first courses.

## Three rules

Task type: benefit-risk-assessment (Pharmacology, Pharmacoepidemiology & Safety), which serves Opportunity Sizing &
Decision Support: the coverage side of an empiric antibiotic's benefit-risk, sized as the mismatched first courses the
pathway would stop in each network, from the pool of its 2026 first courses on other drugs to what moving them to
nitrofurantoin removes.

Domain test: the quantity that decides is each drug's chance of meeting an organism the laboratory reports resistant
among the infections a first course treats, the empiric-coverage estimate antimicrobial stewardship builds first-line
choices on from laboratory susceptibility results, and the field's own construction of it (the cumulative antibiogram,
first isolate per patient a year) is the easy route that lands wrong here.

Swap: "which two branches should the debt advisers sit in, each loan product priced at its default share among the
accounts the collections team opened" stops making sense at once: a collections file is opened only after a default,
so it holds no record made before anything failed, and it reports one product's outcome; a urine culture reports the
organism against every drug at once, so the current drug's failures move every alternative's rate through the
organisms they send, and a presentation culture exists only because primary care sometimes cultures a first infection.

Layer 1: the pathology network's export in the laboratory's own organism and antibiotic codes, susceptibilities as S, I
and R with the expert-rule R for intrinsic resistance, mixed growth and no significant growth results, a specimen
received twice; the GP issue extract with brand, generic, strength and modified-release names, acute and repeat
issues, quantities and durations, and two Stanbridge North practices merged under one code in 2026; collection,
receipt and report dates against issue dates. Each is how those systems write records; none is placed to be caught.

Layer 2: estimand identification under selection on the outcome: the laboratory's isolates are a sample selected by
treatment failure, so the drugs' resistance in it is conditioned on how each culture came to be sent, and the
methodological choice that flips the call is reading each drug's coverage on the cultures sent before any course.

Decisive step: estimating each drug's chance of meeting a resistant organism among the infections a first course treats
from the urine cultures taken at a first consultation, before any UTI antibiotic in the episode, instead of from every
community culture the laboratory reported, as a cumulative antibiogram is built.

Not semantics: with every organism code, susceptibility entry, date and drug name read correctly, the cumulative
antibiogram still gives the cultured isolates' rates; no field, code or definition marks a culture as sent at a first
consultation or after a failed course, which takes the culture's place in the woman's prescribing history.

Not rule application: no filed rule, standard or procedure says which cultures estimate a first course's chance of
meeting a resistant organism; the specification files the outcome, the courses, the pricing and the placement, and
executing every filed rule on the laboratory's cultures as they come files Kesterby and Ashwell Vale. Measured on the
cut pack (`checks.py`): the enumerated family (the antibiogram for women 16 to 64, for all women, for everyone, for E.
coli only, on every isolate, on every requester; the second-course route; the cultures at the consultation; the
failure-weighted estimator over every culture) spreads nitrofurantoin's chance from 4.2 to 20.9 per cent and names two
slates, Kesterby and Ashwell Vale on all seven laboratory and outcome routes; the standing family (the cultures at the
first course's consultation under every window from the day of issue to two days either side, which select the same
4,658 cultures, and the failure-weighted estimator) spreads it from 5.4 to 5.5 per cent, names one slate and keeps
every network's nearest-10 figure; nothing loud rules the antibiogram out, only the filed WHAT's "a first course".

Analyst test: the strong analyst prices each off-guideline drug at its resistance in the federation's community urine
cultures from women aged 16 to 64, first isolate per woman a year, and files Kesterby and Ashwell Vale (the default
path's `Ends on:`, 34.1 and 26.9 against Upper Lode's 10.0), while the cultures sent at a first course's consultation
file Morrow Cross and Tamsey (73.3 and 67.5 against Kesterby's 47.5); `checks.py` executes both on the cut pack and the
clean truth.

Estimand: filed in `uti_pathway_specification_2027-28.pdf` (sections 2 to 4): each network's first courses for lower
UTI in women aged 16 to 64 issued in calendar 2026 on a pathway antibacterial other than nitrofurantoin, each counted at
its antibacterial's chance of meeting an organism the laboratory reports resistant (one federation figure per
antibacterial over 2024 to 2026) less nitrofurantoin's; the pharmacists go to the two networks with the most mismatched
courses stopped.

No decoy: nothing is planted to be caught: the cultures sent after a failed course are there because GPs culture
failures as NICE advises; no antibiogram report, memo, draft, briefing or stakeholder figure ships to carry the wrong
answer, and no document ranks the networks.

No certified replay: no published resistance rate, certified count or closed placement is in the pack to reproduce;
the method is not recovered from any figure.

Lesson: a laboratory's resistance rates describe the infections it is sent, and a drug's own failures send it the
organisms resistant to it while one culture reports every drug, so the current first courses' failures distort every
alternative's rate as well; the coverage a first course gets is read on the cultures taken before anything was given.
No build on file covers antimicrobial resistance or evidence made by the outcome it measures.

## Survivor anatomy

Actor: the deciding property (whether a culture was sent at a first consultation or after a course failed) is a column
in neither the laboratory export nor the issue extract; it is the culture's place in the woman's prescribing history, a
relation between a specimen's collection date and her UTI antibiotic issues across two files.

Link: the signal is read through a cross-file comparison the field's method never asks for (a cumulative antibiogram
de-duplicates isolates and never looks at prescriptions); the pseudonymised NHS number is shared, but no clause names
the comparison and nothing invites it.

Reflex: the field's named construction for empiric coverage, the CLSI M39 cumulative antibiogram (first isolate per
patient a year), sits at rung 1 and files the default slate; the obvious population filters (women 16 to 64, community
requests, E. coli only) stay on it.

Back-test: the textbook route validates: the antibiogram's rates hold steady across 2024, 2025 and 2026, every
laboratory construction (all ages, everyone, every isolate, every requester, E. coli alone) and the outcome route of
second courses name the same two networks, because the culturing practice and the drug mix behind them did not change,
so no trend, cross-section or second method refutes it.

Second use: the issue extract carries the pool (each network's 2026 courses by drug) and the asks; the laboratory export
carries any coverage figure and the asks; deleting the decisive step leaves both files in the pack.

Shock: the movement the step recovers reads as ordinary: nitrofurantoin's laboratory rate sits inside the range English
laboratories publish for urinary coliforms, and the golden slate is not the top two networks on any shipped statistic
(asserted at the build: not by off-guideline courses, by trimethoprim, by pivmecillinam or by any one drug).

Pins: the WHAT is filed in the federation's pathway specification, a service specification in the organisation's own
genre (the outcome, the courses, the pricing and the placement rule); no filed sentence names which cultures, the first
consultation, the prescribing history, the antibiogram or a window for the cultures.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the cumulative antibiogram (women 16 to 64, community, first isolate a year), each course at its drug's resistance less nitrofurantoin's | specification 3.2 "the chance that a first course on it meets": fires toward the laboratory's results | the culture export's antibiotic columns | CLSI M39 first isolate: fires | none | none | one group-by | readable |
| R1, the antibiogram widened or narrowed (all ages, everyone, E. coli only, every isolate, every requester) | none | the same columns | the field's surveillance tables: fires | none | none | one filter | readable |
| R2, each drug's share of first courses followed by another course (the outcome route) | none | the issue extract's dates | treatment failure as the outcome: fires | none | none | one self-join | readable |
| R3, the cultures sent at a first course's own consultation, before any course can have failed, each drug's resistant share of them (decisive) | none: the specification files the chance a first course meets a resistant organism, not which cultures measure it | none: no column marks a culture as sent at a first consultation or after a failed course | none: the antibiogram is the field's construction and de-duplicates isolates without looking at prescriptions | none | none | a join of each culture to the woman's issues across two files by pseudonym and date | silent |

R3 is silent: every culture in the export is a valid report of a real infection, the antibiogram's rates are stable and
plausible for English urinary isolates, and the outcome route agrees with it; the culture's place in the woman's
prescribing history is a relation across two files that no field, document or rule names.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | first course | acute issue, pathway antibacterial, lower UTI problem, woman 16 to 64 at issue, none in the 28 days before | repeat issues counted | same call (no repeat issue to a woman aged 16 to 64) | specification 2.1 "an acute issue" |
| SF2 | the 28 days before | issues from 1 to 28 days before | 14, 21, 35 or 42 days | same call (asserted) | specification 2.1 |
| SF3 | pregnancy | courses linked to a pregnancy problem are not pathway courses, nor their cultures in the estimate | pregnancy-linked cultures added | same call (asserted) | specification 2.1, the code list's "No" |
| SF4 | a culture at the consultation | collected the day of the first course's issue | the day before to the day after, two days either side | same call, the same 4,658 cultures (C1, asserted) | same call |
| SF5 | resistant | R, including expert-rule R; S and I not | I counted as R | same call (no pathway antibacterial reports I) | specification 3.1 |
| SF6 | the chance | per culture, no growth and mixed growth carrying no resistant organism | per isolate | same call (asserted); figures change | specification 3.1 |
| SF7 | a network's courses | the registered practice's network as the register gives it for 2027-28 | the issuing organisation, the hub apart | same call (asserted) | specification 2.2 |
| SF8 | the hub | hub courses and their cultures belong to the registered practice | hub cultures left out of the estimate | same call (asserted) | specification 2.2 |
| SF9 | the estimator | each drug's resistant share of the cultures at the consultation | every culture tied to a first course weighted by its episode's chance of being cultured given whether a second course followed | same call, every nearest-10 figure the same (asserted) | same call |
| SF10 | the chance for a drug | taken over all first courses, whichever antibacterial each was issued | read only on the first courses issued that antibacterial | same call and runner-up (asserted); four networks' nearest-10 figures move | specification 3.2 "taken over all the federation's first courses whichever antibacterial each was in fact issued" (added after the stage 4 judge's FIX_NOW) |
| SF13 | a course below nitrofurantoin's chance | counts against the network | floored at zero | same call (asserted) | specification 4.1 |
| SF15 | de-duplication | each first course's culture counts | a woman's first culture each year only (CLSI) | same call (asserted) | specification 3.2 "the chance that a first course" |
| SF18 | a second pot | one culture per first course, the first registered | both pots | same call (asserted) | same call |

## Ladder

Measured on the cut pack and asserted in `checks.py` (mismatched first courses stopped, 2026 basis).

| Rung | Each drug's chance from | Nitrofurantoin | Slate | Second over third |
|---|---|---|---|---|
| R0 (default) | the antibiogram, women 16 to 64, first isolate a year (7,352 isolates) | 19.0 | Kesterby 34.1, Ashwell Vale 26.9 | 2.69 over Upper Lode |
| R1 | the antibiogram for all women, everyone, E. coli only, every isolate, every requester | 4.2 to 20.9 | Kesterby and Ashwell Vale | 2.0 to 3.2 |
| R2 | the share of first courses followed by another course | 12.0 | Kesterby and Ashwell Vale | 1.0 and up |
| R3 (golden) | the cultures at the first course's consultation (4,658) | 5.4 | Morrow Cross 73.3, Tamsey 67.5 | 1.42 over Kesterby 47.5 |

Dominance: the golden pair's edge on R3 (Tamsey over Kesterby, 20.0 courses) against the default pair's edge on R0
(Ashwell Vale over Upper Lode, 16.9) is 1.18 in absolute courses and 1.42 against 2.69 in ratio; the separation holds
on the clean truth (every episode's organism) at the margin `checks.py` prints. The golden pair is not the top two on
any single shipped statistic (Shock, asserted): Stanbridge North has the most courses on other antibacterials, Morrow
Cross and Upper Lode the most pivmecillinam, Tamsey and Stanbridge North the most fosfomycin.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | first courses as specification 2.1 defines them; women 16 to 64 at issue | filed |
| 2 Unit of account | a first course; the chance per culture | filed (3.1, 3.2, 4.1) |
| 3 Attribution window | courses by issue date in 2026; cultures by collection date 2024 to 2026 | filed (2.3, 3.2) |
| 4 As-of dating | networks as the register gives them for 2027-28 | filed (2.2) |
| 5 Version basis | the export as shipped, one laboratory report a specimen | C1 (no amended report) |
| 6 Denominator | every culture at a first course's consultation | filed (3.1) |
| 7 Weighting | one figure for the federation | filed (3.2); SF9 converges |
| 8 Window length | the day of issue; up to two days either side | C1 (SF4) |
| 9 Boundary inclusivity | 28 days before, 16 and 64 inclusive | filed; C1 (SF2) |
| 10 Rounding path | courses stopped computed unrounded, each network rounded to the nearest 10 once | filed in the prompt; asserted stable across the standing family |
| 11 Tie-break | none needed (margin 1.42) | C1 |
| 12 Maturity and censoring | a 2026 course's culture is in the export (export pulled 6 January 2027) | C1 |
| 13 Order of operations | estimate, then price, then sum | filed (4.1) |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | second pots: one culture per course | C1 (SF18) |
| 16 Identity normalisation | the pseudonym both extracts carry | the systems' own key |
| 17 Netting against gross | a course below nitrofurantoin counts against the network | filed (4.1); C1 (SF13) |
| 18 Dimensional units | courses and chances | units in the data |
| 19 Code and status semantics | the code lists' antibacterials and problems; R, S and I | the code lists; filed (3.1) |
| 20 Integerisation | none | C1 |
| 21 Clause scope | the specification's courses only | filed |
| 22 Forward window contents | 2027-28 placement on the 2026 basis | filed (2.3) |

## Literal reader

Executed on paper and on the cut pack: every filed sentence read word for word lands the golden courses and pricing;
the one open term is the estimate of each drug's chance, which the specification files as "the chance that a first
course on it meets an organism the laboratory reports resistant"; read literally, a culture sent after a first course
failed measures a failed course's infection, and the cultures that measure first courses are those at the first
course's consultation, which every window and the failure-weighted estimator select or reproduce (SF4, SF9). No literal
reading reaches the antibiogram's slate without substituting the isolates' resistance for the chance a first course
meets.

## Oracles

None: no shipped figure ties only under the golden, no antibiogram, published rate, prior placement or closed figure
is in the pack, and the register and code lists answer their own questions. The distractors (the ICB's prescribing
indicators, community C. difficile cases, the registered-list file) rank nothing on the decision question.

## Ask sheet

One ask, fourteen figures: for women aged 65 and over and men aged 16 and over, each network's patients with a 2026
urine culture from a member practice or the hub that grew an enterococcus, and that grew an Enterobacter (a component
of the pharmacists' wider advice, on rows the main call never reads). Device: the laboratory changed system on 7
September 2026; the old system coded the Enterobacter cloacae complex ENTC and enterococci ENTE, the new one codes the
enterococci ENTC and the Enterobacter ECLO, and the shipped code table is the new system's (a code reissued to another
organism, D7, with the old system's whole-panel reporting leaving no per-row contradiction). Recoverable from the data:
the old ENTC isolates are all amoxicillin and co-amoxiclav resistant, which no enterococcus is, ENTE appears only
before the change and ECLO only after. Separation: no ask specimen is in the main call's population, and blanking every
organism code leaves every main-call figure unchanged (asserted).

| Ask row | Golden | Cracker reading | Cracker |
|---|---|---|---|
| Enterococcus by network (7 figures) | 84 to 143 | every ENTC read as the table's enterococcus, ENTE by its letters | miss |
| Enterobacter by network (7 figures) | 31 to 53 | ECLO alone, the old ENTC counted as enterococci | miss |

Pair ceiling: 28.5 (landed call 45.0, best miss 12.0; the cracker keeps 0 of 14 ask figures on pack digest
0add17a8f4c9dc60)

Mirror leakage: 0.0 per cent of ask weight (the mirror handles the ask as the cracker does)

Measured by: generator/ceiling.py, run on the cut pack

## Layer 1 inventory

- The culture export spans two laboratory systems (go-live 7 September 2026): H-prefixed accession numbers and
  dd/mm/yyyy dates before, the new numbering and ISO dates after, the result wording of each, and organism codes the
  current code table only partly covers (the pathology network's own systems).
- One row per organism a specimen grew, a row with no organism for no significant growth and mixed growth, S, I and R
  with expert-rule R for intrinsic resistance, and agents the new system's reporting rules suppress (the laboratory).
- A practice sometimes sends two pots from one consultation, each registered (the laboratory).
- Requests from the antenatal clinic, the emergency department, the assessment unit and wards beside the practices'
  and the hub's; children's bag and clean-catch urines; catheter specimens (the hospital and community requesters).
- The issue extract from EMIS and SystmOne practices and the hub: each system's product names, dosage texts typed in
  several styles, acute and repeat issues, suspensions for children, prophylaxis templates, the problems issues were
  linked to, and Stanbridge Road's records under Hollin Lane from 1 July 2026 (the clinical systems and the merger).

## Pre-ship check

- Generator checks 86 of 86, `verify.py`, two byte-identical builds, `figures_check.py` (47 figures, none absent),
  `precut.py` exit 0, `voice-check.py` PASS, `ceiling.py` (every cracker row missed, pair ceiling 28.5).
- `leak.py` REVIEW on three lines, each innocent: the specification shares the call's vocabulary because it is the
  placement's governing document and names no network; its overlap with the stump paragraph is five generic words;
  the register lists the networks beside list sizes and ranks nothing on the decision question.
- `guard.py heart` WARN (Gate G method_or_model_selection repeating task190 and in five of the last twelve, answered
  in `## Draw`); `guard.py surface` promotes task270, task465, task264 (surface at the corpus top 1 per cent) and
  task308 (the same-driver signature, differentiated on the card) for the author's adjudicated read.
- Rubric arithmetic (shape 01): seven networks by two figures (courses on other antibacterials, mismatched courses
  stopped to the nearest 10), the two networks and the runner-up, the chart and its marked networks, the two files, and
  the ask's fourteen patient counts: 33 criteria or more.
- Stage 4, leak reader (Sonnet, medium, isolated copies of prompt.txt and target/): no leak on the pre-fix pack and
  again on the final pack (`leak_check_report.md`); question 6 answers an analytical choice both times. Its realism note
  (monthly issues without a seasonal swing) ruled harmless: the monthly spread is about twice Poisson and the
  consultation process has no season by design.
- Stage 4, determinism judge pass 1 (`determinism_check_report.md`): DETERMINISTIC, FIX_NOW on specification 3.2 read
  as conditional on the antibacterial issued (the slate and runner-up held, four nearest-10 figures moved). Fixed in the
  generator in one pass: 3.2 files the chance "taken over all the federation's first courses whichever antibacterial
  each was in fact issued" (SF10, asserted), and the ask names Enterobacter cloacae in place of an Enterobacter (the
  judge's Klebsiella aerogenes reading). Pass 2 (`determinism_check_report_pass2.md`): DETERMINISTIC, APPROVE; residual
  low-grade forks left open by choice: the course-to-culture window (the decisive HOW, data-separated: cultures sit at
  0 or 3 to 13 days, so windows of 0 to 2 days give the golden; naming the consultation culture would hand over the
  stump), the ask's system boundary keyed by collection date rather than by accession (a few cells by one or two
  patients), and age at the culture against the maximum 2026 age (one patient in one cell).

## Architecture 1 record (spent 2026-10-28)

Architecture 1 (Data Extraction & Conformation; Survey Research & Official Statistics, census-register-administrative-data-quality) shipped 2026-10-23 and came back on the portal's determinism block of 2026-10-28; the fork was the stump, so no closure shipped (its `## Tried and rejected` lines). Its built state (generator, reports, prompt, write-up, goldens and target.zip) is at commit 16515cc and left the task tree with the architecture 2 draw. Its design as it stood:

Architecture 1, drawn 2026-10-23 from seed ET40 (the
world, the decision and the quantity kept, the pitfall found again from the data under the 10/10 rules): a state
workforce board deciding whether a multi-campus community college system keeps its workforce-value designation for the
2027-28 grant year, which needs at least 75 per cent of the system's completers in programs that pass the board's
tests.

### Draw (architecture 1)

- **Card:** `.claude/skills/fingerprint/cards/task483.json` (architecture v1), registered 2026-10-23 after a pull,
  `check` re-run on the filed card: WARN only (strategy risk answered under `## Three rules`; government_agency
  overused across the corpus, the honest organisation here). `test.same_driver_older` against task39 (objective, G19,
  etl_conformance) is answered by the card's differentiation: task39 recovers a stop rule from a corpus of settled
  disputes; nothing here is recovered from a corpus.
- **Redrawn at the draw, and why the labels are the honest ones.** The window moved twice while the card was written.
  First government_agency, programme_officer and shape 10 were in it (task171 v4, task176 v2, task274 v2), so the
  first form had the system's own institutional research office as the analyst (university_or_school, research_desk,
  shape 07). The pull before registration brought task275 and put university_or_school, research_desk, shape 07, G2
  and G3 in the window (task179 v3, task173 v3, task275) while government_agency and programme_officer left it. The
  board's grant programs office is the honest analyst in any case: it holds its grant completers' wage records under
  the grant's participant agreement and has only the state's public outcomes release for degree programs, which is
  exactly the data reality the decisive step lives in. Shape 16: each program's test is one indicator of the system's
  share. Generator G19 (the board's standard reads a program's median and a completer's work on one day; the records
  hold cells' percentiles and quarters' pay), G16 second.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: two administrative sources, the state outcomes release (each campus's program by completion cohort:
  completers with earnings and five earnings percentiles, cells under 10 suppressed) and the employer-quarter wage
  records of the board's short-term grant completers, conformed with the system's campus completer extracts into the
  board's designation file, one row per program with its test figure and whether it passes.
- **The decision and the quantity:** the board's Career Training Grant pays tuition only at designated providers. The
  designation for 2027-28 renews when at least 75 per cent of the provider's 2024-25 completers are in programs that
  pass: a degree or long-certificate program passes when its completers' median earnings in the third calendar year
  after completion (award years 2020-21 and 2021-22, every campus that offers it, pooled) are at or above the board's
  benchmark; a short-term program (under 600 clock hours) passes when at least 70 per cent of its July 2024 to June 2025
  grant completers were working for an employer on the 180th day after the day they completed. The quantity is the
  system's share; the call is whether the designation renews or lapses, with each program's figure and result.
  Forward facing: the designation decides which programs the grant pays for through 2027-28.
- **Shape:** `16`, indicators into one score: about ten degree programs' pooled medians and about ten short-term
  programs' day-180 shares, each passing or not, the system's share against 75 per cent, the program nearest each line
  and its shortfall; asks on records the call never reads (fixed at stage 2), a chart's named parts and the files.
- **Strategy:** `grain_or_unit` (the records sit at a coarser grain than the standard reads, twice); Gate G
  `etl_conformance`; gap `objective` (a cell's median and a quarter's pay are correct for what they record and are
  not the program median and the day's work status the designation is scored on); pattern none; generators G19, G16.
  Layer 2 family `estimation_fit`, pattern `own:a program median rebuilt from its cells' released percentiles, and a
  day's work status dated from a job's pay inside its first or last quarter`. No calibration organ.
- **The conjunction, sized at the build.** Each half moves a different set of programs: the degree half moves programs
  whose campuses or cohorts earn very differently (a completer-weighted mean of cell medians sits above the pooled half
  point when the cells are far apart and skewed by part-year earners); the short-term half moves programs whose
  completers often leave a first job in the months before day 180 or start one after it inside the same quarter. The
  generator sizes the halves so that the default path, the degree half corrected alone and the short-term half
  corrected alone each leave the system's share at or above 75 per cent, and only both corrections together put it
  below: a partial fix files the same wrong call as no fix. Measured on the cut pack: the default 83.83 per cent (1,208
  of 1,441 completers), the degree half alone 76.89 (1,108), the short-term half alone 77.79 (1,121), the golden 70.85
  (1,021). Medical Assisting (100 completers) carries the degree half and the Commercial Driver License program (87)
  the short-term half.
- **World:** an unnamed U.S. Mountain West state; its State Workforce Development Board and the board's grant programs
  office; Larkspur Basin Community College, four campuses (Fennimore and Ridgefield on the older student system, Copper
  Flats and Antelope Springs on the newer one); the State Education and Workforce Data Center, which publishes the
  outcomes release. People from `guard.py names --geo
  "United States" --seed 483`: Kathryn Petersen (the board's grant programs manager) and Rodney Randall (the research
  center's release lead).
- **Forcing fact:** the board votes the 2027-28 designations in March 2027 and the grant's 2027-28 appropriation is
  committed to designated providers' programs from July 2027.
- **Forum and forcing event:** funder_or_donor, budget_or_appropriation. Organisation government_agency; role
  programme_officer.
- **Data-native sentences:** (1) the outcomes release publishes each campus's program by cohort as its completers with
  earnings and their 10th, 25th, 50th, 75th and 90th percentile earnings, because the research center releases cells
  and never the program's pooled record; a program offered at a metro campus and a rural campus, or by a large cohort
  and a small one, has cells whose medians lie far apart, and its completers' median is the half point of the cells'
  pooled distribution, which the cells' medians averaged by completers overstate. (2) a wage record is one employer's
  pay to one person in one calendar quarter, so the day a job began or ended inside a quarter is written nowhere; a job
  that began or ended in the quarter holding a completer's 180th day shows only part of a quarter's pay there, and that
  pay against the same job's pay in a full quarter dates the start or the exit.
- **Default path and golden, by name:** degree programs' cell medians averaged by completers, and short-term
  completers counted as working on day 180 on any pay in the quarter holding it, keep the designation; the pooled half
  points and the dated jobs let it lapse. Names and figures are set at the build.
- **The WHAT screen.** Population: the system's programs, their 2020-21 and 2021-22 degree completers with earnings
  and their 2024-25 short-term grant completers. Outcome: median earnings in the third calendar year after the award
  year; working for an employer on the 180th day after completion. Unit: dollars; a completer. Window: the stated award
  years and days. Comparison: the benchmark, 70 per cent, 75 per cent. The decisive step settles none of them: it is
  how a program's median is computed from released cells and how a day's work status is read from quarterly pay, which
  no filed rule or procedure states.
- **Sources, one line each:**
  - published postsecondary earnings outcomes (the Census Bureau's Post-Secondary Employment Outcomes and state
    longitudinal data system dashboards) release cells as counts and percentiles, never pooled records;
  - the medians of parts do not combine into the median of the whole; a grouped or percentile release is pooled through
    each part's distribution (the median of a mixture);
  - administrative job-flow statistics (the Quarterly Workforce Indicators) read job starts and exits from employer
    quarter wage records by whether the same employer paid the person in the adjacent quarters, and a partial quarter's
    pay against a full quarter's measures the share of the quarter worked.
- **Same-puzzle and same-driver tests:** (objective, G19, renew_replace_lapse) and (objective, G19, etl_conformance)
  against the last twelve builds, lineage included: no match in the last twelve; task39 differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns: task229 v3 passes a day's mean through a convex
  conversion; task457 reads a period's amount from a report covering only part of it; task177 v2 times an intervention
  against a unit's recurring decision; task476 starts an interval-censored onset from a seasonal profile carried from
  another record; task477 re-dates a total by its payment schedules' weekdays; task123 allocates a billing period's
  total to months by an activity indicator. Here no total is allocated or re-dated: one half pools released
  distributions where the default averages their half points, the other dates a job's start or exit from that job's own
  pay in the quarter that holds the day the standard reads.

### Default path (architecture 1)

1. Read the board's Workforce Value Designation Standard: a credit program passes on its completers' median earnings
   in the third full calendar year after the award year, every campus and both award years taken as one group, at or
   above USD 34,200 in 2025 dollars; a short-term program passes when at least 70 per cent of its grant completers were
   working for an employer on the 180th day after completing; the designation renews at 75 per cent of the 2024-25
   completers of tested programs in passing programs.
2. Conformed the two completion extracts (two student systems, two layouts, two ID formats), the outcomes release's
   two editions (a wide workbook coded by the awards' CIP codes, a long file coded by current CIP 2020 codes, other
   colleges and other years-after rows, Paralegal Studies' cells suppressed), the roster and the wage records (amended
   reports superseding originals, other providers' participants) to one program list through the inventory.
3. Took each credit program's median as its campus-by-cohort cells' medians averaged by completers with earnings, the
   2024 medians in 2025 dollars.
4. Counted a grant completer as working on day 180 when the wage records show pay from any employer in the calendar
   quarter that holds day 180.
5. Applied the tests and summed the 2024-25 completers in passing programs.

Ends on: the designation renews, 84 per cent of the system's 2024-25 completers in passing programs (1,208 of 1,441),
Medical Assisting passing at 36 thousand dollars and the Commercial Driver License program at 91 per cent.

Golden: the designation lapses, 71 per cent (1,021 of 1,441): Medical Assisting's pooled median is 33 thousand dollars,
under the benchmark, and the Commercial Driver License program's day-180 share is 63 per cent, under 70; each
correction alone leaves the share at 77 or 78 per cent.

### Stump sentence (architecture 1)

The default path averages each credit program's campus-by-cohort medians by completers and counts a short-term
completer as working on day 180 whenever any employer paid them in the quarter holding that day, and keeps the
designation at 84 per cent; but Medical Assisting's rural campus pays its completers a tight 30 thousand dollars while
its two metro campuses' completers, many of them part-year, spread from 13 to 66, so the program's pooled median (33
thousand) sits under the line its averaged median (36) clears, and 22 of the CDL program's 79 grant completers left their
first carrier weeks before day 180 and started at the next weeks after it, still drawing that quarter's partial pay,
so the jobs dated from their own pay put the CDL share at 63 per cent; with both the designation lapses at 71 per cent,
and either correction alone leaves it at 77 or 78.

### Three rules (architecture 1)

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics), a task type serving
Data Extraction & Conformation (ETL): an outcomes release of campus-by-cohort cells and a set of employer-quarter wage
records, conformed with two campus completion extracts, the grant roster and the program inventory into the board's
designation file.

Domain test: the call turns on two quantities administrative employment statistics estimate from outcome releases and
employer wage records, a program's median earnings as the half point of its cells' released distributions pooled by
completers, and a completer's work status on the 180th day dated from a job's pay in its first or last quarter against
its pay in a full quarter (the job-flow reading of quarterly wage records).

Swap: "which wards keep their accreditation because their patients' median stay is under four days and 70 per cent
were at home on the 180th day" reads differently at once, because a hospital's records are dated claims and unit
stays: no released cell hides the ward's pooled stay and no quarter hides the day a patient went home.

Layer 1: the two completion extracts in two student systems' layouts (a workbook with seven-digit IDs and SIS program
codes, a CSV with LB numbers, dashed state IDs and numeric program IDs); the outcomes release in two editions whose
layout and coding changed (a wide workbook under a two-line title coded by the awards' own CIP codes, Information
Technology and Criminal Justice under their pre-2022 codes, and a long CSV coded by current CIP 2020 codes), other
colleges' and other years-after rows in both, Paralegal Studies' cells suppressed; employer-quarter wage rows in which
an amended report supersedes the original, other providers' participants and pre-program jobs; the roster's withdrawals
and the cohorts before and after the window. Each is how the producing system writes its records; nothing is placed to
be caught, and none moves the call when handled the obvious way (asserted: the CIP recodes missed, the CPI factor
missed, amended reports summed or ignored, untested programs counted or grant completers used as weights all leave the
call where it is).

Layer 2: estimation that fits the data's structure, twice: a median of a pooled population from its parts' released
distributions rather than their medians, and an event date inside a reporting period from the period's partial amount
against a full period's.

Decisive step: rebuilding each credit program's earnings distribution from its cells' five percentiles and taking the
pooled half point, and dating each short-term completer's job starts and exits inside the quarter that holds day 180
from that job's pay there against its pay in a full quarter; the share crosses 75 per cent only when both are done.

Not semantics: a solver who reads every field right (the release's cells are campus by cohort, percentiles are of
earnings among completers with earnings, wage rows are pay per employer per quarter, the completion date is the
section's last day) still averages the cells' medians and still reads pay in the quarter as work on the day, because
no field holds a pooled median or a start date.

Not rule application: no filed rule says how a group's median is computed from released cells or how a day's status is
read from quarterly pay. Measured on the cut pack. The degree half's enumerated family (cells' medians averaged,
unweighted or their median, the percentile points pooled as a sample, a log-normal through each cell's five points,
and the interpolations) spreads the graded figures 1,919 to 4,789 dollars, Medical Assisting 32,411 to 37,100; the
standing family (every interpolation through the released percentiles: straight in dollars, straight in log dollars,
monotone cubic, any tail anchors) spreads 69 to 149 dollars and files one whole-thousand cell for every program. The
short-term half's enumerated family (pay in the quarter, the second quarter after exit, earnings floors of 500, 1,000
and 2,500 dollars, beginning-, end- and full-quarter employment, the position-chosen point-in-time measure, a
day-proportional share, a half-quarter pay threshold, a person-level pay ratio) spreads the CDL figure 59 to 91 per
cent, 31.6 points; the standing family (the job-level pay ratio against the adjacent full quarter, the full quarters'
mean, the two beside the partial one or the job's median quarter, a pay-lag correction of 0, 7 or 14 days, a calendar
or a 91-day quarter: twenty-four variants) spreads it by zero on every program.
What rules out the rest is the data, never a clause: the log-normal misses a released percentile by up to 57.7 per
cent (a median 7.7 at each cell's worst point), the percentile points pooled as a sample do not pass through the cells'
own percentiles, and the 31 jobs that put 22 CDL completers in the quarter route's count paid a median 20 per cent of
their own full quarter there (8 to 67), the mark of a job that ended or began inside the quarter.

Analyst test: with every field read and the board's standard applied, the easy route averages the cells' medians and
counts pay in the day-180 quarter as work on day 180, and files the designation as renewed at 84 per cent; the golden
lapses it at 71 (asserted by `checks.py` on the generator's clean truth and on the cut pack).

Estimand: the board's Workforce Value Designation Standard (in the pack, sections 3 to 5) fixes the population (the
program's completers in award years 2020-21 and 2021-22 across every campus, as the release counts them with
earnings; the grant participants who completed a section ending from 1 July 2024 to 30 June 2025), the outcomes
(median earnings in the third full calendar year after the award year, every campus and both award years taken as one
group, in 2025 dollars; working for an employer on the 180th day after the section's last day), the units, the windows
and the comparisons (USD 34,200, 70 per cent, 75 per cent of the 2024-25 completers of tested programs).

No decoy: nothing is planted to be caught; no memo, draft, briefing, dashboard or stakeholder figure argues for the
averaged medians or for pay in the quarter, and no shipped artifact ranks the programs on the tests.

No certified replay: no certified or published figure is reproduced to recover a method; the release's percentiles are
the data the pooled median is built from, not controls for a hidden rule.

Lesson: a median of a pooled population comes from its parts' distributions, not their medians, and a status on one
day inside a reporting period is read from a record's partial amount against a full one; no build on file teaches the
first (no pooled-median screen in any slot note), and the nearest teach allocating a period's total by an indicator
(task123) or starting an onset from a seasonal profile (task476), not dating a job from its own partial pay.

### Readability screen (architecture 1)

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the cells' medians averaged by completers; any pay in the quarter holding day 180 (the default path: renews at 84) | standard 3.1's "median annual earnings" beside a release of medians; 4.2's wage records: fires | the release's Median column; the wage rows' year and quarter: fires | dashboards weight cell medians; the federal performance measure counts wages in a quarter: fires | none | none | one weighted mean; one join and a filter | readable |
| R1, the cells' medians unweighted or their median; the second quarter after exit; an earnings floor in the quarter | none | the same columns | the federal second-quarter measure; substantial-earnings floors: fires | none | none | one group-by | readable |
| R2, beginning-, end- or full-quarter employment (same employer in the adjacent quarters), or the one nearer day 180 | none | the wage rows by employer and quarter | the job-flow statistics' point-in-time measures: fires | none | none | one self-join on employer | readable |
| R3, the percentile points pooled as a sample, or a log-normal through each cell's points | none | five percentile columns invite a distribution | fit a distribution to quantiles: fires | none | none | one sort, or one regression per cell | readable |
| R4, a day-proportional share of a partial quarter, a half-quarter pay threshold, or a person-level pay ratio | none | the wage amounts | interpolate by position: fires | none | none | one formula per completer | readable |
| R5, each cell's distribution rebuilt through its five released percentiles and the pooled half point solved (decisive) | none: the standard files the group's median, not how a release of cells yields it | none: no column holds a program's median or a pooled count at a value | none: the field's habit is to weight the cells' medians | none: the release publishes no program-level figure to reconcile to | none | a root of a weighted sum of piecewise functions | silent |
| R6, each job paid in the quarter holding day 180 dated from its pay there against its own full quarter, start or exit (decisive) | none: the standard files the day, and a wage record as a quarter's pay | none: no start or end date anywhere in the grant's records | none: the field's habit is to read employment from wages in a quarter | none: no file dates any job | none | a per-job ratio no column suggests | silent |

R5 is silent: averaging the cells' medians by completers is what published dashboards do and the averaged figure is a
plausible median for every program; nothing in the pack computes a pooled distribution or names one. R6 is silent: the
grant's records date nothing but sections, every wage row is a well-formed quarter's pay, and the default path's
counts reconcile (every completer with pay in the quarter is counted once).

### Semantic fork table (architecture 1)

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a credit program's earnings figure | the median of the group's earnings, every campus's published cells and both award years taken as one group | the cells' medians averaged, unweighted or their median | renews (the default) | standard 3.1, "taken as one group": a group's median is a point of the group's distribution, which a mean of its parts' medians is not; asserted |
| SF2 | the third full calendar year after the award year | 2024 for 2020-21, 2025 for 2021-22, the release's three-years-after rows | the release's one- or five-years-after rows | not a live reading | standard 3.1's parenthesis and the technical notes' earnings year; asserted |
| SF3 | 2025 dollars | 2024 earnings times 1.0294, 2025 earnings as published | no adjustment | same call; six figures move | standard 3.2; asserted |
| SF4 | a suppressed cell | left out; Paralegal Studies has no published cell and is not tested | imputed | same call | standard 3.4; asserted |
| SF5 | a program's CIP code across editions | the 2024 edition's pre-2022 codes for Information Technology and Criminal Justice joined through the inventory | those two programs' 2020-21 cells missed | same call | the inventory's earlier-CIP column and the technical notes' coding; asserted |
| SF6 | the 180th day after the day they completed | the section's last day plus 180 days | plus 179 (the completion day counted as day 1) | same call, same figures | asserted: no completer's job starts or ends within 24 days before or 14 days after day 180 |
| SF7 | the day a participant completes | the roster's section end for the participant's section | the campus extract's completion date | same call, same figures | standard 4.1; the two agree for every grant completer; asserted |
| SF8 | working for an employer on the 180th day | a job covered by unemployment insurance running on that day | any wages reported in the quarter holding it | renews (the default) | standard 4.1, "on the 180th day", and 4.2, "a wage record is the wages ... in one calendar quarter": a quarter's pay is not a day's work; asserted |
| SF9 | an amended wage report | replaces the original for the same participant, employer and quarter | the original kept; both summed | same call, same figures | standard 4.2; asserted |
| SF10 | grant completers | the roster's participants with exit reason Completed in sections ending 1 July 2024 to 30 June 2025 | the campus extracts' short-term completers | same call | standard 4.1 ("Career Training Grant participants"); asserted |
| SF11 | at least 20 grant completers | Forklift and Material Handling (18) not tested | tested on its 20 completers in the extracts | same call | standard 4.4; asserted |
| SF12 | a program's 2024-25 completers | the completion extracts' completers at every campus, grant participants or not | the grant completers for short-term programs | same call (70.68 and 83.73) | standard 5.2; asserted |
| SF13 | programs not tested | in neither the numerator nor the denominator | in the denominator as not passing | same call (69.31 and 82.01) | standard 5.2; asserted |
| SF14 | comparing a figure with its line | as computed, before rounding | the rounded figure | same call | standard 5.3; asserted: the nearest figures are 1,143 dollars and 6.7 points from their lines |
| SF15 | which test a program takes | credit programs (Medical Assisting and Paralegal Studies certificates of 34 and 32 credits included) the earnings test; clock-hour programs the placement test | a certificate read as short-term | not a live reading | standard 2.2 ("of one academic year (30 credits) or more") and the inventory's lengths; asserted |
| SF16 | ask A's year | the sessions dated 1 July 2024 to 30 June 2025 | the sessions of the sections that ended in the year | ask figures only | the asking sentence ("attended from July 2024 to June 2025"); asserted |
| SF17 | ask A's hours | each session's time read as hours and minutes after the point, the repeated rows once | decimal hours; the repeated week kept | ask figures only | C4 separate: every program's full sessions are whole hours, and of the entries a late arrival or early departure cut short none runs past 59 after the point and every one is a whole five minutes; the repeated rows are the same participant, section, date and time twice; asserted |
| SF18 | ask B's principal | every subsidized and unsubsidized dollar the completer borrowed at the college in any award year: each disbursement before July 2024, returns netted, and each 2024-25 loan's amount once; the median and the total over the program's completers who borrowed | the rows summed as exported; one amount per loan in every year; the 2024-25 award year alone; the parent PLUS loans | ask figures only | the asking sentence ("all the Direct Subsidized and Unsubsidized Loan principal they borrowed at the college") and the cost of attendance's annual limits and installments: two rows of a 2024-25 subsidized loan summed run past the subsidized annual limit for over a thousand borrowers, one row never does; asserted |
| SF19 | rounding | each figure from its unrounded value, rounded once, halves up | per line or per cell | same call, same figures | asserted: no graded figure within a tenth of a rounding unit of an edge |

### Ladder (architecture 1)

Measured on the cut pack and asserted in `checks.py` (the share of the 1,441 completers of tested programs in passing
programs; the line is 75).

| Rung | Credit programs | Short-term programs | Share | Call |
|---|---|---|---|---|
| R0 (default) | cells' medians averaged | any pay in the day-180 quarter | 83.83 | renews |
| R1 | unweighted or median of medians | second quarter after exit; floors of 500 to 2,500 | 83.83 | renews |
| R2 | averaged | beginning-, end-, position-chosen or full-quarter employment; prorated; half-quarter; person ratio | 75.85 to 83.83 | renews |
| R3 (one half) | pooled through the percentiles | any pay in the quarter, and every R1, R2 and R4 reading but full-quarter | 76.89 | renews |
| R4 (other half) | averaged, unweighted or median of medians | each job dated from its own pay | 77.79 | renews |
| R5 (golden) | pooled through the percentiles (straight, log or monotone cubic) | each job dated from its own pay (twenty-four variants) | 70.85 | lapses |

Two routes off the ladder also lapse, and neither files the golden: full-quarter employment with pooled medians
(68.91, Phlebotomy failing at 64 per cent and every short-term figure moved), and the crude poolings (the percentile
points as a sample, a log-normal) with dated jobs (70.85, six to ten of the eleven credit figures moved).
The default path's error is one-sided: it passes two programs the records fail (Medical Assisting, 100 completers, and
the CDL program, 87). Margins: the golden 4.15 points under the line, each one-half fix 1.89 and 2.79 over it, the
default 8.83 over; every rung's share is fixed by whole-program pass and fail sets, so no rung sits within a completer
of the line.

### Closure table (architecture 1)

| Axis | Reading | Move |
|---|---|---|
| 1 Population | credit programs: the release's published cells for award years 2020-21 and 2021-22 at every campus; short-term: the roster's completers of sections ending in the window | filed (standard 3.1, 3.4, 4.1); C1 |
| 2 Unit of account | a program; a completer within it | the question names the program; SF15 |
| 3 Attribution window | award years 2020-21 and 2021-22; sections ending 1 July 2024 to 30 June 2025; 2024-25 completers | filed (3.1, 4.1, 5.2); C1, no section ends on a boundary |
| 4 As-of dating | the editions and records as shipped (October 2026) | the files' own ranges; C1 |
| 5 Version basis | an amended wage report replaces the original | filed (4.2); SF9 asserted |
| 6 Denominator | the share: completers of tested programs; the placement figure: grant completers | filed (5.1, 5.2, 4.1); SF12, SF13 asserted |
| 7 Weighting | the cells pooled by completers with earnings; programs weighted by 2024-25 completers | filed ("taken as one group"; 5.1); SF1, SF12 |
| 8 Window length | the third full calendar year after the award year; the 180th day | filed (3.1, 4.1); SF2, SF6 |
| 9 Boundary inclusivity | at or above the benchmark; 70 and 75 per cent or more | filed; C1, nothing within 1,143 dollars or 1.89 points of a line |
| 10 Rounding path | lines compared unrounded; figures rounded once | filed (5.3); SF14, SF19 asserted |
| 11 Tie-break | none: no figure on its line | C1, asserted margins |
| 12 Maturity and censoring | every completer's day 180 and the next two quarters inside the wage records (to 2026 Q2) | C1, asserted |
| 13 Order of operations | 2024 earnings into 2025 dollars before pooling; supersede amended reports before dating | filed (3.2, 4.2); C1 (pooling is invariant to the order once each cell is converted) |
| 14 Row order | none: every figure is a set computation | asserted over shuffled rows |
| 15 Duplicate resolution | amended over original wage reports; a person once per program in the release | filed (4.2; technical notes); SF9 |
| 16 Identity normalisation | programs through the inventory (SIS codes, numeric IDs, CIP before and after 2022, grant program IDs); students by state ID with or without dashes | the inventory; C1, every row joins; SF5 |
| 17 Netting against gross | none on the main path; ask B's returns net against their loan | SF18 |
| 18 Dimensional units | dollars of 2024 and 2025; per cent | filed (3.2); SF3 |
| 19 Code and status semantics | exit reason Completed; suppression S; loan types old and new | dictionary and file semantics; never the stump; SF10, SF4 |
| 20 Integerisation | completer counts whole; shares of whole counts | C1 by construction |
| 21 Clause scope | the earnings test for credit programs, the placement test for clock-hour programs | filed (2.2); SF15 |
| 22 Forward window contents | the designation governs 2027-28; the call rests on closed records | not live: the standard's tests read closed records |

### Literal reader (architecture 1)

Executed word for word, the prompt and standard sections 3 to 5 ask for each credit program's median earnings with
every campus and both award years taken as one group, among completers the release counts with earnings, and for each
short-term program's share of grant completers working on the 180th day after their section's last day, then the
share of 2024-25 completers of tested programs in passing programs. Neither the group's median nor anyone's status on
a day is published: the release carries campus-by-cohort cells and the wage records carry quarters' pay, so the
literal estimand is unobserved on both halves and is estimated from the records. The standing estimators agree on the
graded figures (every interpolation through the released percentiles files one whole-thousand cell per program; the
24 job-level pay-ratio variants file one count per program), and every reading of every term in the fork table
files the same call or is ruled out by a quoted sentence. The golden is the literal estimand's estimate, not a reading
of a term.

### Oracles (architecture 1)

None ties only under the golden. No file publishes a program's pooled median, a pooled share at the benchmark or any
completer's start or exit date; the release's percentiles and the wage amounts are the data the golden is built from,
and every route reads them. No file ranks the programs on their tests or reports the system's share. For the asks: the
attendance export is not summarised by program anywhere and states no session's length, the inventory's clock hours
are one participant's schedule (the referee that separates the readings of a session's time without handing over any
program's total); the loan export carries no column of a loan's amount beside its disbursements' amounts, and no file
states a completer's principal.

### Ask sheet (architecture 1)

Two asks, both on files the call never reads: the college's attendance export for the grant's participants (ask A);
the college's Direct Loan disbursements and its cost-of-attendance statement (ask B). Zero device rows sit in the
call's population: the attendance and the loans are read by no step of the call, and the roster and completion
extracts they join to are read by the call only for counts the devices do not touch (asserted, X1 and X2).

- **Ask A, each short-term program's clock hours its grant participants attended from July 2024 to June 2025, whole
  hours (11 figures).** H18 home: the instruction the grant bought, program by program, beside the outcomes it is
  judged on. User: the board's grant office, reporting training hours delivered under the grant. Primary device: D3
  units set per source, hours and minutes in a decimal column (the attendance system writes a session's time as hours
  and minutes after a point; nothing in the export or the documents says so). Every program meets in whole-hour
  sessions, so a full session reads the same either way and a completer at every session totals the inventory's clock
  hours under both readings; the device lives in the sessions a late arrival or early departure cut short (a tenth of
  them, each cut by a whole five minutes), whose entries never run past 59 after the point: read as decimal hours the
  figures fall 2 to 45 hours short. Hazards: the export appends the week of 3 March 2025 a second time at its end
  (exact duplicates), late enrollees and leavers attend only part of a section, the sessions of sections that
  straddle the year's ends. Files and columns: the attendance export (participant, course reference number, session
  date, hours), the roster (participant, program, course reference number, section dates, enrolled on, exit date),
  the inventory (clock hours). Stops: the times as decimal hours (0 of 11), the repeated week kept (3), both (0), the
  sections that ended in the year (4 or fewer), the completers' sessions alone (0), the golden.
- **Ask B, each credit program's median and total, over its 2024-25 completers who borrowed, of all the Direct
  Subsidized and Unsubsidized Loan principal they borrowed at the college, nearest 10 dollars (24 figures).** H18 home: the debt side
  of the same completers' workforce value, a measure every credit program carries that the call does not turn on.
  User: the board's grant office and the college's consumer information. Primary device: D6 an event's quantity on
  every line it covers (the aid system that went live on 1 July 2024 writes the loan's gross amount for its award year
  on each of the loan's disbursements, in the GROSS_AMT column the old system filled with each disbursement's gross
  amount; the cost of attendance's annual limits and "disbursed in installments, normally one each semester" are the
  evidence: two rows of a 2024-25 subsidized loan summed run past the 4,500-dollar subsidized limit for 1,136 borrowers,
  one row never does), with its over-cleaning half (one amount per loan, or alike rows kept once, in every year halves
  the old system's two-installment loans). Hazards: returned disbursements as negative rows under status Returned,
  parent PLUS loans under two code sets, two ID formats for the state student ID, the cost of attendance's origination
  fee (the export's amounts are gross). Stops: the rows summed as exported (0 of 12 medians, 0 of 12 totals), one
  amount per loan in every year (0, 0), alike rows kept once (0, 0), the 2024-25 award year alone (0, 0), every amount
  read as net (0, 0), returned rows dropped (5 medians, 0 totals), parent loans kept (2 medians, 2 totals), the golden. Every program's borrower count is odd and every completer's principal a whole
  10 dollars, so each median is one completer's principal at the centre of its bin.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | the attendance export's sessions dated in fiscal 2025, exact duplicates dropped, each time read as decimal hours | miss |
| B | each completer's Subsidized and Unsubsidized rows as exported, returns netted, parent loans left out | miss |

Measured partial handlings on the cut pack: ask A keeps 11 of 11 once the session times are read as hours and minutes
and 3 of 11 if the repeated week is then kept; ask B keeps 24 of 24 once each 2024-25 loan counts once and 0 of 24 when
every loan counts once. A response that finds both devices scores 100; one that finds neither scores 45 on the call; one
that finds only ask A's keeps under a third of the 35 ask figures.

Pair ceiling: 28.5 (the cracker 38 + 7 with none of 35 ask figures, the mirror 5 + 7 with none).

Mirror leakage: 0.0 per cent of ask weight.

Measured by: generator/ceiling.py on the cut pack.

### Pre-ship check (architecture 1)

1. Domain: administrative employment statistics' own estimates from an outcomes release and employer-quarter wage
   records, a program's median earnings as the half point of its cells' released distributions pooled by completers
   and a completer's status on the 180th day dated from a job's pay inside its first or last quarter; with a hospital's
   nouns no released cell hides a pooled median and no quarter hides the day a job began or ended.
2. Real work, nothing planted: every Layer 1 item is what the producing system writes (two student systems' extracts,
   two release editions with the CIP recodes and Paralegal Studies' suppression, amended wage reports, the roster's
   withdrawals and the cohorts outside the window, the attendance export's minutes after the point and its re-sent
   week, the new aid system's annual amount on each disbursement); none is on the decisive step, and no ask device row
   sits in the call's population (X1 and X2).
3. The step that flips the call is analytical: pooling the released distributions and dating each job from its own
   partial pay; no clause makes either choice (standard 3.1 files the group taken as one and 4.1 the 180th day, not how
   a released cell becomes a median or a quarter's pay a day's status).
4. Analyst test: every field and rule read correctly, the averaged medians and any pay in the day-180 quarter file the
   designation as renewed at 84 per cent (asserted on the clean truth and on the pack); either correction alone files
   78 or 77, both together 71, lapsed.
5. The standard files the estimand (population, outcomes, windows, units and comparisons in sections 3 to 5) and no
   estimator; the standing family (every interpolation through the released percentiles with any tails, and the 24
   job-level pay-ratio variants) files one whole-thousand cell per credit program and one count per short-term program
   (G1, G3), and the asks' conventions are filed in their asking sentences or closed by the data (SF16 to SF18).
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest task266's stump at 0.07, task477's ledger row at 0.05 and task229 v3's driver
   at 0.07; task39 differentiated on the card.
8. Re-read against the built pack at stage 4: eight isolated readers over four rounds filed the designation as renewed
   at 77 per cent (the pooled medians with any pay in the quarter), and none dated a job from its own pay; the round 4
   readers on the shipped cut (zip 7d3d1845) kept 0 and 11 of the 35 ask figures (0 and 31.4 per cent).
9. Judge pass 1 DETERMINISTIC, FIX_NOW (ask A's counting and ask B's window not literally filed, the credit programs'
   year undefined, the CDL figure moved under two further dating references: ask A re-sited, ask B's window put in its
   asking sentence, standard 2.2's 30 credits filed, the dating family widened to 24 variants with every completer
   dated alike); passes 2 to 4 DETERMINISTIC, APPROVE, Gate G method_or_model_selection and analytical_non_defect,
   Gate H domain pass, layers pass, decisive step analytical. Pass 4, on the shipped cut, kept no competing answer and
   left two minor notes: the attendance export does not label its hours (the data forces hours and minutes, SF17), and
   the dating step sits near data semantics (it is the unit-of-analysis choice between a day inside the quarter and the
   quarter itself).

## Tried and rejected


- The seed's earnings-premium test alone, the pooled median rebuilt from each cell's quartiles (P25, P50, P75): on
  realistic skewed cells of 10 to 70 completers eight licensed reconstructions (log-normal and log-logistic through the
  quartiles, split log-normal, linear in dollars or log dollars, monotone spline, normal) spread 500 to 1,650 dollars
  on the pooled median, as wide as the naive error (0.4 to 5.8 per cent), so Gate C and Gate F could not both hold.
- The same with five released percentiles: the family tightens to 155 to 634 dollars, but the decisive step is then one
  choice a solver enumerates (average the cells' medians or rebuild them), the coin-flip shape of the client's measured
  tasks; kept only as one half of a conjunction.
- The release's count of completers at or above the benchmark per cell: the test becomes exact (a median clears the
  line when half the pooled completers do, and counts add), but the column hands the step to any solver who reads it,
  and the graded medians stop being computable.
- Earnings known only for aided (or SSN-linked) completers, reweighted to all completers: the reweighting is a reflex
  (task482 v2 and v5 readers weighted by reflex) and missing at random is untestable, so a literal judge can read the
  linked completers' median as the measure.
- Earnings released only above a full-time floor: recognising the floor is a field reading, and once recognised the
  quantile shift pushes the solver into distributions, so the pooling follows.
- Out-of-state work estimated for completers who moved to states outside the wage exchange: assumption-bound, no
  determinate golden.
- The day-180 placement test alone: once no deciding start or exit sits within 28 days of day 180 the job ratio is exact,
  but pay in the quarter then lands within 0 to 4 points of the golden unless exits fall early in the quarter and
  starts late in it, and day-proportional shares land near the golden whenever day 180 sits near a quarter's edge; kept
  only as the other half of the conjunction, with each program's completion calendar and job flows set so the halves
  carry the share.
- A late calendar for one of the CDL campuses (sections ending the last Friday of a quarter, day 180 late in the next
  quarter but one), so a half-quarter threshold would count the early leavers: their first jobs began the week after
  completing and so never had a full quarter before the quarter holding day 180, and no record dates them; dropped for
  a calendar putting day 180 on the quarter's first days.
- Phlebotomy and Pharmacy Technician as the traps for the strict readings (completers leaving shortly after day 180 and
  starting shortly before it inside the quarter): every strict reading then failed them, so full-quarter employment
  with the averaged medians filed the golden share to the decimal (71.3) and the golden call; rebuilt so only
  full-quarter employment fails Phlebotomy, at 64 per cent, and Medical Assisting's 100 completers keep that reading
  with the averaged medians on renews (75.85).
- An ask on each credit program's release coverage (completers with earnings over completers in the college's own
  2020-21 and 2021-22 records), its device the older student system dating awards by their posting: the extract's only
  date column would then be literally the award date, so a literal reader files the device's wrong answer.
- An ask on the grant's completion rates with a case-management migration closing open records as withdrawals: the
  record shape is the migration duplicates both top responses removed on the portal (16 rev 3).
- Borrower counts beside ask B's medians: every handling that leaves out parent loans and nets returns lands all 12,
  so the counts were free to the cracker; cut.
- Ask A's device a section's fee on every participant line of the board's line export from January 2025: the judge read
  the export's amounts summed as what the board paid (a fork, not a device), and reader A kept all 11 figures through
  the inventory's fee per section and the register; replaced by the invoice header's program on every old line and the
  hand-keyed invoices outside the register.
- Ask B's device the aid system writing disbursements net of the origination fee from July 2023: both readers grossed
  the amounts up from the cost of attendance's fee sentence and the cents the net amounts carried (12 of 12 each);
  replaced by the loan's amount on each of its disbursements from July 2024.
- Day-180 status accepted when the golden's job dating agreed with the simulation: the judge's two other references
  (the adjacent and far quarters averaged, the job's median quarter) moved the CDL figure 50 to 54 of 79 through exits
  whose far quarter was a few weeks' pay. Requiring every dating reading to agree and redrawing in the shared stream
  moved every later path and put the half-quarter threshold under the line for the CDL program (53 of 79, landing the
  call); kept with the four disagreeing completers redrawn from their own streams.
- Ask A's second devices, the old billing system writing the invoice header's program on every register line and the
  hand-keyed supplementary invoices outside the register: both round 2 readers compared each register line's program
  with its participant's program in the roster (507 and 434 lines flagged) and kept the CE invoices by their program
  ID, 11 of 11 each, while the call (77 per cent, renews) and ask B (0 of 12) held; the tuition reconciliation runs on
  three files that check one another line by line, so no device on its path stays silent. Replaced by each short-term
  program's clock hours attended, read from an attendance export that writes hours and minutes.
- Ask A's clock hours from sessions scheduled to the half hour (7.30 on every full session of six programs): both
  round 3 readers read the hours as hours and minutes, one from the 7.30 entries and one because only that reading
  gave the inventory's clock hours, 11 of 11 each; reader F also caught ask B (two subsidized rows of 4,500 over the
  4,500 limit), 23 of 23, while every reader of three rounds missed the call. Kept with whole-hour sessions, the
  minutes only in the sessions cut short, and ask B doubled to each program's median and total.
- The prompt without the standard's name: the portal's prompt check failed P6 on 2026-10-28 (no pass line, no renewal share and no renewal rule cited, and the reviewer saw no input files); the question now cites the State Workforce Development Board's Workforce Value Designation Standard by its title, the thresholds left in the standard and no ask, file, unit or rounding moved.
- Closing the portal's day-180 fork (determinism block of 2026-10-28, Gates C, D and E: the CDL program's day-180 status read from quarterly wage records as 47, 50, 65 or 72 of 79 grant completers, the last two passing and renewing the designation at 76.9 per cent) with a filed sentence: every closure spends the stump. The eight in-house readers and the portal's judge all pooled Medical Assisting's cells and missed only the dating (77 per cent, renews), so the judge's both-neighbours rule (which also moves CDL to 59 per cent), the golden's dating filed in standard 4.2, or a definition ruling out the quarter's pay each let that path land the call. The fork was the stump; back to design rather than shipped as a determinism fix.
- Re-root screens of 2026-10-31 for architecture 2 (ETL fixed by the number; the cells open to it are payment claims, IRT equating and seasonal adjustment, with emissions banned against task482 and record linkage and the census register refused by task464's measured map): register deduplication where duplicate clusters outnumber pairs (entity resolution, spent at task486 architecture 2 and measured worthless against the cutoff in task464's note); anchor items drifted by exposure (released-item drift, screened dead at task482's architecture 7 draw); rater severity drift on double-scored responses (spent at task471 architecture 2). None registered; the re-root waits on a mechanism outside task464's and task482's screened lists.
- Re-root screens of 2026-11-01 for architecture 2, window: a probe card on `survey-research-official-statistics / seasonal-adjustment-official-time-series-production` BLOCKs on `ban.pairing` against task456 v3 (survey research x ETL, registered 11-01), so both survey-research ETL cells are shut for this draw; probes on emissions inventory, payment claims, IRT equating and record linkage clear every axis ban (their only BLOCKs were the probe's own placeholder fields and its arbitrary gap-pattern-Gate G triple). Drawing a survey-research task type through the demographic-social-science house label would game that ban (task482's architecture 11 line), so it was not tried.
- Re-root screens of 2026-11-01, emissions inventory (open since task482 left the window), each dead before a harness: a vapour recovery unit's capacity binding on flash surges at tank batteries, the overflow summed hour by hour (the abstraction is task162's device replayed reading by reading, approved, with task156's overflows beside it); truck switch loading, distillate loaded into compartments that last carried gasoline displacing gasoline vapour (AP-42 5.2's equation takes P of the liquid loaded, so the literal standard files the default and the golden needs a correction it does not ask for, task482 architecture 15's withheld-rule lesson; filed physically the sentence names the step, and the previous cargo is one lag of a shipped column); start emissions by the preceding downtime (a permit's or maker's start definitions make it a stated rule, a fitted curve a covariate carry); pile wind erosion by inter-disturbance period (AP-42 13.2.5 files it); utilities' mutual consumption solved as a fixed point (task190's M1 measured reciprocal and direct allocation naming one unit 30 of 30; a CHP loop forks on the allocation method; a stated recursive definition is rule application); consumption-based grid factors by flow tracing (the exporter's mix forks between generation and availability, and the recursive definition is rule application); roof landings, manual gauging puffs, liquids unloading by accumulation and blowdowns by line pressure (filed AP-42 or Subpart W equations, task487's hatches); a service tank's sulfur through an emission control area changeover (the ship's fuel system decides the mixing model, a fork, in a port world); cooling-tower drift, stormwater buildup and washoff, pesticide emission potentials (filed models, forks, or task454's within-type costing).
- Re-root screens of 2026-11-01, payment claims, IRT equating and record linkage, each dead before a harness: deductible seasonality carried to the year (task482 v13's run-out), stockpiling before a formulary change (task463), a global obstetric fee spread over the pregnancy (task123), crossover lesser-of pricing, retroactive contract rates and provider-level recoupments (stated rules, or task482 architecture 11's screen), emergency visits on inpatient claims (a code reading), incident cases by lookback (task458); a disrupted test prorated against pattern-scored (task482 architecture 10's rescoring screen), superscoring's best of k (screened there), mode effects from schools that randomised mode (task445's and task474's unselected comparison), opt-outs (the 95 per cent participation rule), nominal against effective composite weights (a semantic fork); Fellegi-Sunter dependence among household members (card 2, set aside at task486), staggered measurement changes read by event study (task482 architecture 11's coding screen, the reflex), weighted least squares data reconciliation (filed it is rule application, unfiled a fork), historian deadband time weighting and logger clock drift (task486 architecture 3: fails the swap, spent), sampling-phase aliasing (task251's one-weekday counts, task249's set-aside), suppressed-cell and Frechet bounds (task465, task475; the independence product sits inside the bounds, so they never flip it), late filers imputed by an honest back-test and production allocated between well tests (no structural core, or a decline-model fork).
- The 2026-11-01 draw is therefore not filed: no mechanism outside task464's driver map, task482's and this note's screened lists, the slots' notes and the approved builds' abstractions survived, and none was registered. Unblocking is the author's call (`CLAUDE.md`, retirement and a ban waiver): a waiver for survey research x ETL against task456 v3, moving the number to another objective, or one of the borderline designs above shipped at its stated Gate H risk (switch loading is the least weak: physically large, unscreened, and pincered between the literal AP-42 reading and a pin that names the step).
- The number re-tasked by the author on 2026-11-01 from Data Extraction & Conformation (ETL) to Opportunity Sizing & Decision Support, retirement not taken, after architecture 1 came back on the 10-28 determinism block and the 11-01 draw found no ETL ground left; architecture 2 is drawn as an Opportunity Sizing build in a never-built pairing (pharmacology by Opportunity Sizing). START_HERE.md is not edited: the range fixes which objective a number belongs to and nothing else, and the card and the ledger carry the real objective.
- Architecture 2 draw screens of 2026-11-02, each dead before a harness on its slot-note or card record: marketing by Opportunity Sizing (a conjoint launch weighted by volume or distribution, latent classes the fit statistics reveal, a near-twin plan, a pilot calibration, the in-market population by contract timing: task174, task178, task301 and task309 notes; intercept respondents weighted by visit frequency: task264); pharmacology benefit-risk (the initiation bleeding spike on a one-year horizon, warfarin switchers as a covariate, a trial's 18-month delay with competing deaths: task301); collections (an existing-customer match on a bought portfolio: task301; a dialler's capacity days: task128); business operations through healthcare delivery (a fused wait: task127; a shared pool: task106; bursty queues: task178 and task198; a theatre list replay: task301); accounting through actuarial ground (a retention's truncated and censored severity: task255; credibility, development and on-levelling are the cards' named methods); economics left to task277's draw.
- Further 2026-11-02 screens, dead on the rules or the record: peak coincidence of a group's demand (task196, task164); a rate read against the observation effort behind it (task199); a renewal process restarting a wear curve (task132); a halo of complementary items lost with a delisted one (task302's world turned over); a share of a fixed pot under a filed formula (rule application); a radiopharmacy generator's decay through the week (the decay correction is the field's first move); rent arrears read at a snapshot of each tenant's monthly benefit cycle (a phase of a balance, time semantics, and an estimand that would have to name the step); a stewardship campaign's switches recognised as same-week bursts across a practice's patients (task303's simultaneity signature).
- The empiric first-line choice itself as the call (keep nitrofurantoin or move the first line to pivmecillinam or trimethoprim), set aside at the draw: the call is then the sign of one difference between two drugs' resistance, a Descriptive retag, while the pathway's placement in two networks makes the sized opportunity (the mismatched first courses each network's move stops) decide.
- An estimand naming the infections at a first presentation (or a 28-day window for the cultures), set aside at the draw: the sentence would name the step and make linking the cultures to the prescriptions an executed rule (task445 v2); the specification files the outcome, the courses and the pricing only, and which cultures estimate a first course's chance stays the analyst's.
- 2026-11-02, architecture 2 stage 2: an ask on older women's nitrofurantoin courses against an eGFR under 45 with the
  laboratory's switch from MDRD to CKD-EPI: the two equations differ by one to three units near 45 for women over 65, so
  the device moves almost no course, and filing the equation names the device.
- 2026-11-02, architecture 2 stage 2: an ask on men's short courses with SystmOne quantities in packs: a course of one
  tablet is found by inspection, so the discovery and the remedy are one act.
- 2026-11-02, architecture 2 stage 2: Enterobacter aerogenes coded EAER before the go-live and counted as a Klebsiella:
  the old name read literally files it as an Enterobacter, a semantics fork the judge would read two ways.
- 2026-11-02, architecture 2 stage 2: a Pharmacy First claims file: a failed pharmacy course makes the GP's next course
  look like a first course and its culture look like one sent at a first consultation, which moves the estimate.
- 2026-11-02, architecture 2 stage 2: the ENTC reissue with the old system's selective reporting: an enterococcus row
  carrying gentamicin and cefpodoxime contradicts its code on the row, which the hygiene battery re-derives; the old
  system now prints its whole panel for every organism.
- 2026-11-02, architecture 2 stage 3: each antibacterial's chance graded to the whole per cent: the failure-weighted
  estimator moves trimethoprim and cefalexin by one point, so only the placement, the pools and the nearest-10 courses
  stopped are graded; the world's seed was redrawn (483099) after the retune left a network's figure on a nearest-10
  line under the first seeds.
