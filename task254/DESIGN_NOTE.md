# task254 design note

## Verdict (spec-update design pass, 2026-10-11)

Architecture 2 does not pass the stage 2 gate under main's current spec, and the spec-update brief's stop rule applies: nothing in this note is to be rebuilt. There are three findings. Each is argued in its own section below, and every figure is recomputed from the built pack (`target/` at efe84a7, through the parsers in `generator/verify.py`).

1. **As shipped, the golden is not the literal answer** (`## Literal reader`, SF1). Annex 7 files the window over "the risk's reactions in treated patients" (5.1), and has it "estimated from the post-marketing time to onset data of section 3 and section 4 without fitting a parametric model" (5.2). Executed word for word, that is the cut of the reactions on file: ILD month 16 (80 per cent month 7). Month 20 holds only if the population is read to include the reactions not yet begun at the DLP, and no shipped sentence says so. That is the task445 failure, and it makes the designed stump one of the readings of the population term.
2. **Filed the only way the spec allows, there is no stump** (`## Default path`, `## Readability screen`). Suppose 5.1 states outright that the reactions of patients on treatment at the DLP that had not begun by it are in the population. Then every solver who executes the clause knows the reported series is short, and every natural correction files 9 and 20:
   - courses at least 480 to 930 days old at the DLP;
   - the 2023 starters;
   - weighting each reaction by the share of courses started early enough to show it;
   - the reverse-time product-limit.

   Only cut-offs under 480 days miss (16 to 19). Those cut-offs are shorter than the naive window itself and than the onsets visible to day 693. The default path ends on the golden, and the decisive rung is readable (a filed sentence names the gap, and the correction is a reflex).
3. **The ask layer fails the cracker sheet** (`## Ask sheet`).
   - Ask A is the call's own estimator on five other risks, and an annex 7 clause adjudicates every one of its devices.
   - Ask B is device-only, every one of its devices is a PSUR section 5 counting rule, and the supply channel overview names the hospital channel.
   - The cracker banks every ask figure and the mirror banks Ask B whole. The pair ceiling is 70.1.

The decisive step could survive only by moving from recognising the truncation to how the reactions still to begin are completed, the way task445 loop 1 moved its stump to the completion basis. That is a new decisive step on new data, so it is left to the re-root decision and is not drawn here.

The sections below state architecture 2 as it would have to be filed, which is how `precut.py` reads it. `## Architecture 2 as built` keeps the record of the generator (green at efe84a7, 64,603 assertions, two builds byte-identical). Architecture 1 is condensed in `## Tried and rejected`.

## Draw

The card is `task254` v2 (`.claude/skills/fingerprint/cards/task254.json`), drawn and filed with `guard.py register` on 2026-10-11.
- `guard.py check` returned WARN `repeat.gate_g`, answered at the draw: this build's step is an estimator choice for a case-only series, where task253's is a nonresponse weighting class.
- The stage 5 pooled heart check returned WARN only, and the clone pre-flight was CLEAN (`clone_check_report_task254.md`).
- Lineage: v1 (fire planning bands), spent at stage 2.

This pass does not change the draw.

1. Pairing: Pharmacology, Pharmacoepidemiology & Safety / other: time-to-onset characterisation of identified risks for routine risk minimisation / Descriptive & Distribution Analysis.
2. Niche: a Danish specialty pharmaceutical company's drug safety department sets the routine monitoring windows for each identified risk of Lyrevo (RVB-417), an oral immunomodulator launched in April 2023. The windows go in the RMP update filed with PSUR 6 (data lock 30 September 2026): the months of treatment by which 80 and 95 per cent of the risk's reactions have begun. The call is the ILD 95 per cent month, golden month 20 (80 per cent month 9), which ends pulmonary monitoring for patients treated from January 2027.
3. Gate G: method_or_model_selection; strategy maturity_censoring; gap time over population; pattern none; generators G16, G12. Layer 2: estimation_fit, `own:right-truncated-time-to-onset-in-a-post-marketing-case-series`.
4. Shape 14, cuts of a distribution: 2 cuts x 6 risks. The ILD 95 per cent cell is the call and the ILD 80 per cent cell its critical component. Deliverables: `rmp_monitoring_windows_2027.xlsx` and `onset_windows_by_risk.svg`.
5. Personas, drawn with `guard.py names --geo "Denmark" --seed 254`: Pernille Rasmussen (EU QPPV, the requester) and Lasse Christoffersen (safety data lead on the export, the field guide and annex 7).
6. Sources read:
   - The exemplars Replenishment Cover Standards (mean 0.13; p50 and p90 cuts of a lead-time distribution, tier by tier) and CDFI Award Compliance (mean 0.39; a lag that differs by segment), taken for the cut furniture and the per-segment lag only, since both rest on a rule withheld behind published controls.
   - `layer2-rigor-patterns.md`, which has no right-truncated time-to-onset entry, hence the `own:` pattern. Its nearest entry, nowcasting recent weeks with the reporting-delay distribution, corrects a count, not a distribution of onset.
   - Layer 1 from the safety-database and supply techniques of `layer1-messiness.md`.

Data-native sentence: a drug in its fourth year on the market has most of its patients starting recently, because uptake grows as each country launches and reimbursement widens. So when the safety database is locked, the late reactions of most treated patients are still to come. A case-only series can contain only reactions that have begun, and each case's time to onset is bounded by how long that patient has been treated.

Forward window: the windows go into the RMP that governs prescribing from 2027. Each window is a cut of the distribution of time to onset, not a forecast of 2027 case counts.

## Default path

This is the pipeline a competent analyst builds without thinking, with annex 7 filed the only way literal determinism allows: 5.1 states outright that the reactions of patients on treatment at the DLP that had not begun by it are in the population. The figures are from the built pack.

1. Reads the prompt and annex 7: the window is the first 30-day month by the end of which at least 95 per cent of the ILD reactions in treated patients have begun (5.1, 3.3), counting the ones not yet begun at the DLP, with no parametric model (5.2).
2. In `lyrevo_line_listing_PSUR6_DLP20260930.csv`, keeps each case's version of record (the latest received on or before 30 September 2026), drops cases first received after it and study reports (1.2, 1.3), merges duplicates to their master case in `duplicate_register_PSUR6.xlsx` (2.1), and maps preferred terms with the v4 sheet of `rmp_term_list_version_4.xlsx`, one reaction per case and risk, the earliest onset (2.2, 2.3).
3. Builds courses from `lyrevo_dosage_lines_PSUR6.csv` (3.2) and counts time to onset from the first dose of the course in which each reaction began, complete dates only (3.1, 3.4): 541 ILD reactions, with onsets visible to day 693.
4. Reads the cuts off those 541 reactions (80 per cent month 7, 95 per cent month 16) and sees they cannot be the filed quantity: 37 per cent of the ILD reactions come from courses less than a year old at the DLP, so the reactions still to begin belong to recent starters and are the long ones.
5. Corrects the way the opponent does by reflex, with any of three constructions: keeping only the courses old enough to have shown every visible onset (started at least 693 days, or 24 months, before the DLP); weighting each reaction by one over the share of courses started early enough to show it; or running the reverse-time product-limit. Each files 80 per cent at month 9 and 95 per cent at month 20, and so does every cohort cut-off from 480 to 930 days.

Ends on: month 20
Golden: month 20

As shipped, without the outright clause, step 4 has nothing to answer and the path stops at month 16. Month 16 is then the literal execution of annex 7, not an easy method applied to a stated estimand (`## Literal reader`). So 16 against 20 was a fork on SF1, never a stump.

## Stump sentence

As designed (card `task254` v2): a competent solver keeps the version of each case current at the lock, merges duplicate reports through the register, maps reactions to risks with the RMP term list, computes every reaction's time to onset from the first dose of its course wherever both dates are complete, and reads the 80 and 95 per cent months per risk straight off the reported reactions, filing the ILD window at month 16 against month 20; the step that lands them there is treating the reported times to onset as the distribution of onset, when over half of all patients started in the twelve months before the lock and their later reactions have not begun yet, so the series under-represents exactly the onsets that set the 95 per cent cut.

Month 16 is what annex 7 as shipped returns when read literally (SF1). Under the legal filing the default path ends on month 20, and no sentence of this form can be written.

## Three rules

Domain test: holds. The call turns on the time-to-onset distribution of each identified risk, estimated from a case series bounded by each patient's time on a recently launched drug. That is the pharmacovigilance analysis that sets how long routine monitoring runs after a patient starts treatment. With another field's nouns there is no course start, onset, monitoring schedule or case series, and the task stops reading the same.
Analyst test: fails under both filings. As shipped, an analyst who cleans the data and reads every rule correctly, 5.1 and 5.2 word for word, files month 16. That is annex 7's literal answer, so the gap to month 20 is a reading of the population term (data semantics, banned as the decisive step). Filed outright, the same analyst corrects for the reactions still to begin with any standard construction and files month 20, so no easy route lands elsewhere.
Layer 1: case versions in an export run six days after the DLP; duplicate reports linked only in a register; partial dates; courses in a separate dosage-line file, with restarts, dose changes and short pauses; a PSP laboratory feed with units and limits per laboratory; a revised term list; study and literature cases in the same export; supply split between wholesaler sell-in and 3PL hospital call-offs counted in shipper cases; national article codes resolved through a product master and an xEVMPD XML; credit notes and zero-value lines. Each is something a safety database, a PSP vendor or a 3PL actually produces.
Layer 2: right truncation of a case-only series: a reaction is in the database only once it has begun, so every case is bounded by its own time on treatment at the DLP. Once the estimand says outright that the reactions still to begin are in the population, this pitfall carries no stump, because the correction is the opponent's reflex and every form of it converges on the golden by construction.

## Readability screen

The ladder's rungs under the legal filing (`## Default path`), against the six tests of `stumping` Part 2.1. As shipped, rung 5 is silent on all six tests, but SF1 is then open and month 16 is the literal answer. No filing leaves rung 5 silent and SF1 closed at once.

| Rung | 1 filed sentence | 2 schema | 3 reflex correction | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| 1 Weibull fitted to the reported onsets (13) | fires: annex 7 5.2 rules out a parametric model | no | no | no | no | no | readable |
| 2 cuts read off the reported onsets (16) | fires: the refiled 5.1 puts the reactions not yet begun at the DLP in the population, and the reported series lacks them | no | no | no | no | no | readable |
| 3 courses started before 2026 (18) | no | no | fires: the reflex correction keeps courses old enough for the visible tail (onsets to day 693), which overshoots this cut-off | no | no | no | readable |
| 4 courses at least a year old at the DLP (19) | no | no | fires: as rung 3; every cut-off from 480 days files 20 | no | no | no | readable |
| 5 (decisive) each case bounded by its own time on treatment at the DLP (20) | fires: the refiled 5.1 names the reactions not yet begun, the gap this rung closes | no (each bound is the course start against the DLP; no column holds it) | fires: once the gap is named, a mature cohort, weighting by the share of courses old enough and the reverse-time product-limit are the opponent's default corrections, and all file 20 | no | no | no | readable |

## Semantic fork table

One row per term of the main ask and per convention the ILD computation depends on, as built. SF1 is the architecture's crux: it closes only under the refiling that kills the stump, and as shipped nothing closes it (`## Literal reader`). The ids are not in `generator/checks.py`, because no rebuild follows from this pass.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the risk's reactions in treated patients" (annex 7 5.1), the window's population | every reaction that begins during a course in a patient treated up to the DLP, including those that had not begun by the DLP | the reactions in the safety database at the DLP | month 16 (80 per cent month 7) | only annex 7 5.1 refiled outright ("including the reactions of patients on treatment at the DLP that had not begun by it"), which makes rung 5 readable; as shipped nothing rules it out, and 5.2 reads to it |
| SF2 | "month of treatment" | 30-day months counted from day 1, the first dose of the reaction's course (3.1, 3.3) | calendar months of 30.4375 days | same call | same call: every day-level cut sits at least 7 days inside its month and above the calendar-month reading (built) |
| SF3 | "by which 95 per cent have begun" | the first month by the end of which at least 95 per cent have begun (5.1) | the month holding the interpolated quantile | same call | same call (C1, asserted) |
| SF4 | "interstitial lung disease reactions" | preferred terms mapped to ILD in term list v4, in force at the DLP (2.2) | term list v3 | same call | same call: the v3 to v4 change touches no ILD term |
| SF5 | case unit | one reaction per case, the earliest onset, duplicates merged to the register's master (2.1, 2.3) | every report, or every mapped term, counted | same call | same call: duplicate pairs carry identical ILD dates (C1, asserted) |
| SF6 | as-of version | the latest version received on or before the DLP (1.2) | the latest version delivered in the 6 October export | same call | same call: post-lock versions change no ILD date (C1, asserted) |
| SF7 | case scope | post-marketing cases first received by the DLP (1.2, 1.3) | study cases or post-lock cases kept | same call | same call: inert for every window (C1, asserted) |
| SF8 | dates | complete onset and course-start dates only (3.4) | partial dates imputed to day 1 or day 15 | same call | same call (C1, asserted) |
| SF9 | course and origin | dosing with no gap of more than 28 days, where a dose change is not a new course (3.2), counted from the course's first dose | every dosage line a course, or the first dose ever as origin | same call | same call: no ILD case has a restart, escalation or pause before onset (asserted) |
| SF10 | the truncation bound | days from the course's first dose to the DLP | the DLP less a reporting delay of 0 to 60 days | same call | same call (C3 corridor, asserted) |
| SF11 | "without fitting a parametric model" (5.2) | a non-parametric estimate | a Weibull or lognormal fit, truncated or not | month 13 or 15 | annex 7 5.2 |

## Ladder

The ladder as built (ILD: the month of the 95 per cent cut, with the 80 per cent month in brackets). Under the shipped annex 7, rung 2 is the literal answer, not a wrong stop (SF1), and the survival properties below (the first above all) held only while SF1 stayed open. Under the legal filing, rungs 3 and 4 are the only wrong stops left, and the opponent's correction overshoots both (`## Default path`).

| Rung | Construction the solver builds | The gap it leaves open | ILD 95% (80%) | vs answer |
|---|---|---|---|---|
| 1 | Weibull fitted to the reported times to onset (pharmacovigilance's habitual time-to-onset summary), cuts read off the fit | the series read as complete, and a one-hump shape forced on a long-tailed distribution | 13 (8) | -35% |
| 2 | Empirical cuts of the reported times to onset, every reaction with complete dates, after versions, duplicates, term mapping, courses and scope are all handled correctly | time: the later reactions of everyone treated less than about 23 months have not begun, so long onsets are missing in proportion to recent uptake | 16 (7) | -20% |
| 3 | Rung 2 after dropping courses started in 2026 (under nine months on treatment at the lock) | the same gap for patients treated 9 to 23 months, still most of the remaining patient-time | 18 (8) | -10% |
| 4 | Rung 2 keeping only courses started at least 12 months before the lock | the same gap for patients treated 12 to 23 months | 19 (8) | -5% |
| 5 (answer) | Each case bounded by its own potential time on treatment at the lock, days from its course's first dose to 30 September 2026 (the reverse-time product-limit estimate for a right-truncated series), equal to the empirical cut over courses started at least as long before the lock as the longest observed onset | none | **20 (9)** | |

Partial moves priced:
- A parametric fit with the truncation inside the likelihood is the parametric half-step: the truncated Weibull files 15 (80 per cent at 10); the truncated lognormal has no usable maximum (the fit runs off to cuts past month 200). Annex 7 section 5 rules both out (no parametric model) and so does the data: the reported ILD onsets carry an early peak in months 2 to 3, the body to month 11 and a long tail, a shape no two-parameter family follows. The built tail is continuous: every month from 1 to 22 holds reported ILD onsets, and the longest is day 693.
- Courses started at least 18 months before the lock (not yet mature, since the longest ILD onset is day 693): built at 20 (9), the answer's months; recorded and never treated as the answer's evidence. Courses started at least 36 months before the lock hold 14 ILD reactions and also read 20 (9), recorded.
- Hygiene slips (latest delivered version kept, duplicates unmerged, partial dates imputed to day 1 or day 15, study cases or post-lock cases kept, term list v3 rows used, onset counted from the first dose ever, every dosage line a course) move neither ILD month of the answer (C1, asserted under the estimator, under the estimator with a bound 60 days shorter, and on every mature cut-off).
- A truncation time taken from a case's own stop date collapses the risk sets (most ILD cases stop because of the reaction): built, a bound at every recorded stop, the withdrawals the reaction caused included, files 21 with the 80 per cent cut at month 20, an estimate no reader keeps; recorded, not priced. A bound at a course end the reaction did not cause (a later discontinuation after DOSE NOT CHANGED) is part of the rigorous family and converges (C1).

Survival properties: (1) not written: no file states that the series is bounded by time on treatment or names a maturity rule, and annex 7 defines what is measured, never how the distribution is estimated; (2) no corpus: no published, certified or prior window anywhere in the pack, so nothing can be recovered by replay; (3) no arithmetic symptom: rung 2 reconciles to every count the pack offers; (4) not a row predicate: each case's bound is its own course start against the lock and the estimate is a product over risk sets, or a cohort cut-off chosen from the longest onset; (5) no cutover date and no event to align on; (6) survives deletion: every number in the pack is correct, so there is nothing wrong to delete.

Measured on the built pack (`onset_days` from `verify.py`, run on `target/`): the ILD 95 per cent month by cohort cut-off, keeping courses at least L days old at the DLP.

| L (days) | ILD 95 per cent month |
|---|---|
| 90 to 120 | 16 |
| 150 to 210 | 17 |
| 240 to 273 | 18 (the 2026 starters dropped) |
| 300 to 450 | 19 (a year on treatment) |
| 480 to 930 | 20 (266 down to 62 reactions) |

Three more constructions also file 9 and 20: the 2023 starters (38 reactions), the weighting by the share of courses started early enough to show each onset, and the reverse-time product-limit. Reported ILD onsets by 30-day month run to month 24, with 10 in month 20 against 6 and 2 either side (the tell under `## Tried and rejected`).

### Windows, every risk (built; months, answer against the reported-cuts rung)

| Risk | 80% answer | 95% answer | 80% rung 2 | 95% rung 2 | Reactions in the estimate | Longest onset | Answer cuts (day) |
|---|---|---|---|---|---|---|---|
| Interstitial lung disease | 9 | 20 | 7 | 16 | 541 | day 693 | 250, 585 |
| Herpes zoster | 11 | 21 | 8 | 16 | 1,608 | day 704 | 310, 613 |
| Serious infections | 7 | 18 | 5 | 11 | 1,835 | day 698 | 188, 527 |
| Venous thromboembolism | 6 | 16 | 5 | 11 | 765 | day 635 | 159, 467 |
| Hepatotoxicity | 4 | 9 | 3 | 8 | 1,465 | day 386 | 98, 250 |
| Neutropenia | 3 | 8 | 2 | 7 | 1,339 | day 324 | 68, 221 |

Every one of the 12 cells moves between rung 2 and the answer (asserted; neutropenia carries extra mass in months 1 and 2 so its rung 2 reads 2). Zoster sits at 21, one month off ILD, so the two curves never share a window. Starts: 92,940 courses from launch, 56.3 per cent in the twelve months before the lock and 16.9 per cent at least 24 months before it.

### Convergence family (C1), asserted in the generator and in the independent verifier

For every risk and both cuts, all of the following land on the same month (asserted in `checks.py`; the estimator and the mature cuts recomputed in `verify.py`). Every member runs in numpy and pandas alone:
- the reverse-time product-limit estimate on days (each reaction's risk set is the reactions with onset on or before the day and truncation time on or after it), truncation time = days from the course's first dose to the lock inclusive, read as the smallest 30-day month whose cumulative share reaches the cut and as the month holding the interpolated quantile;
- the same estimate on 30-day months, the truncation time binned down (the last complete month) and up (the month holding the lock);
- the same with every truncation time shortened by each whole number of days from 0 to 60 (the reporting-delay corridor, C3: a reaction has to be received by the lock, so the true bound sits a reporting delay inside the lock);
- the same with each case's window ending at the lock or at a course end the reaction did not cause, whichever comes first (the dosage lines record such a discontinuation for about 30 per cent of DOSE NOT CHANGED cases);
- inverse-probability-of-observation weighting: each reaction weighted by one over the share of courses started early enough to show its onset, the start distribution taken from every case's therapy start in the listing or from the course starts;
- the empirical cut over courses started at least L days before the lock, for every L from the risk's longest onset to 913 days (30 months; the round 24 months, 730 days, inside it), and over courses started in 2023, under all 13 numpy quantile definitions;
- each of the above with any one hygiene slip: duplicates unmerged, study cases kept, post-lock cases kept, term list v3, partial dates imputed to day 1 or day 15, and for ILD also the latest delivered version, the onset counted from the first dose ever and every dosage line a course (each slip asserted under the estimator, the estimator with a bound 60 days shorter, and every mature cut-off under two quantile definitions);
- every mapped term counted as a reaction (a misapplication of the one-reaction rule): asserted under the estimator, recorded on the mature cut-offs (0 cut-offs off the answer for every risk).

Bin centring (built): every member lands inside the answer month; each day-level product-limit cut sits at least 7 days inside its month (built minimum: days 68, 98 and 188, each the eighth day of its month) and above the calendar-month reading (30.4375 days a month); the share at the end of the month before the answer is at least 0.5 points under the cut level and the share at the end of the answer month at least 0.5 points over it. Tightest built margins: hepatotoxicity 95 per cent at 93.73 per cent by the end of month 8 (1.27 points under), serious infections 95 per cent at 96.35 per cent by the end of month 18 (1.35 over); ILD 93.06 per cent by month 19 and 97.83 per cent by month 20. Courses started at least 30 months before the lock hold 69 ILD reactions and the 2023 starters 38, the two tightest members; the 36-month cohort (14) is recorded only.

## Closure table

The 22 axes as built, with axes 1, 12 and 22 restated for the verdict (SF1).

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | post-marketing cases (spontaneous, solicited including the PSP, literature) first received on or before 30 September 2026; study cases out (annex 7 section 1); study and post-lock cases inert for every window (C1), they move only the rates. As shipped, no file says whether the window's population holds the reactions not yet begun at the DLP (SF1 open, literal answer month 16); the only legal closure states them in outright, which makes the decisive rung readable |
| 2 | Unit of account | one reaction per case per risk, the earliest onset mapped by the term list, cases merged to the register's master (annex 7 section 2); duplicate pairs carry identical ILD dates (C1) |
| 3 | Attribution window | the course in which the reaction began; course = run of dosing with no gap over 28 days, a dose change is not a course (annex 7 section 3); no ILD case has a restart, escalation or pause before onset (C1), the other risks carry the course device (Ask A) |
| 4 | As-of dating | the case as it stood at the lock, the latest version received on or before 30 September (annex 7 section 1); post-lock versions change no ILD date (C1) and move non-ILD onsets (hazard H1) |
| 5 | Version basis | RMP term list v4, in force at the lock; the v3 to v4 change touches zoster and serious-infection terms only (Ask A), no ILD term |
| 6 | Divisor | reporting rate = cases over patient-years times 1,000; patient-years from units supplied through every channel (PSUR section 5 method) |
| 7 | Weighting | each case's reaction counts once in its risk's distribution; no exposure weighting (annex 7 sections 2 and 5) |
| 8 | Measurement window | launch (3 April 2023) to the lock for the windows and the cumulative rate; 1 October 2025 to 30 September 2026 for the interval rate (prompt) |
| 9 | Boundary inclusivity | at least p per cent (annex 7 section 5); month 1 = days 1 to 30; the lock day counts; a 28-day gap continues a course; every graded cut centred so a strict reading lands the same month (asserted) |
| 10 | Rounding path | days unrounded, the month taken at the cut; rates and patient-years unrounded until the end, then one decimal and nearest 10; binned and unbinned estimates converge (C1) |
| 11 | Tie-break | none; quantile cuts and sums only |
| 12 | Maturity and censoring | as built, each case bounded by its own potential time on treatment at the lock, equal by construction to the empirical cut over courses older than the longest onset (C1); as shipped the axis turns on a reading of SF1, and under the legal filing every natural truncation-aware construction converges on the answer, so the axis closes and carries no stump |
| 13 | Order of operations | versions, then duplicates, then term mapping, then the one-reaction rule, then onset; commutative by construction for every graded figure (asserted) |
| 14 | Row order | none |
| 15 | Duplicate resolution | the register's master case; identical ILD dates on both reports (C1); unmerged duplicates move only the rates |
| 16 | Identity normalisation | case numbers consistent across listing, dosage lines, register and PSP feed (the feed also carries its own patient reference, linked one to one); national article codes in mixed formats resolve through the product master (Ask B) |
| 17 | Netting | credit notes net against supply; replacement and PSP starter packs are supply (PSUR section 5 method, Ask B) |
| 18 | Dimensional units | one tablet = one patient-day for both strengths; 365.25 days a year; packs of 28 or 84; shipper cases of 10 packs; ALT in U/L or µkat/L, neutrophils in 10^9/L or cells/µL per laboratory (Asks A and B) |
| 19 | Code semantics | report type, primary source, action taken and seriousness codes defined in the field guide |
| 20 | Integerisation | none beyond the month ceiling the annex defines |
| 21 | Clause scope | the laboratory onset rule covers hepatotoxicity and neutropenia reactions identified from a laboratory value only (annex 7 section 4); the one-reaction rule is per case per risk |
| 22 | Forward window contents | the window governs patients starting from January 2027 for a whole course, which only the prompt's framing implies; as shipped no file says the window's population runs past the DLP (SF1), and stating it outright is the legal filing |

## Literal reader

As shipped, executed word for word, annex 7 5.1 ("the first month of treatment by the end of which at least 95 per cent of the risk's reactions in treated patients have begun"), estimated per 5.2 "from the post-marketing time to onset data of section 3 and section 4 without fitting a parametric model", is the cut of the reactions on file: ILD month 16 (80 per cent month 7), not the golden month 20 (month 9). No shipped sentence puts the reactions not yet begun at the DLP into the population, so the golden rests on an inference, which is the task445 failure. Refiled outright, the literal execution is month 20, and the easy method (the reported cuts) visibly falls short of the clause. So every solver who executes the clause corrects, and every correction it reaches for files month 20: no reading is left and no stump is left.

The stage 4 reader took exactly the as-shipped path: it read annex 7's rules as the whole method and took the cut off the reported reactions. Its disposition logged that as evidence that the decisive step is silent. Under the current stage 4 gate it is the opposite finding: the filed sentences it quoted (5.1, 5.2) execute literally to month 16, not to the golden.

## Oracles

Main call: none. No published, certified or prior window ships, and no trial time-to-onset summary, Weibull table or corpus either; nothing in the pack reproduces month 16 or month 20.

Ask layer: `finance_net_sales_by_market_quarter.xlsx` is the one referee. Its French, Italian and Spanish revenue sits far above what their sell-in packs would earn, which arbitrates whether sell-in is the whole supply without stating a unit count.

The ask layer falls on the documents that adjudicate its devices, not on oracles. Annex 7 sections 1.2, 3.2 and 4.2 decide every Ask A device. The PSUR section 5 counting rules, the supply channel overview and the call-off header decide every Ask B device (`## Ask sheet`).

## Ask sheet

The ask layer as built is two asks and the chart, read here against `supplemental-stumping` Part 1. The device tables, ladders and hazard table are under `### The ask layer as built` below.

- **Ask A**, the 80 and 95 per cent months of the other five identified risks (10 cells). It is the call's own truncation-aware estimator, run on rows the call never reads, so it is keyed to the construction (Part 1.2, ban 4). Its devices are A-D1 course restarts, A-D2 dose changes and short pauses, and A-D3 laboratory-dated onsets with units per laboratory, with hazards H1 to H3. An annex 7 clause the call already reads adjudicates every one of them (ban 1):
  - 3.2: the course and its 28-day gap;
  - 4.2: the first sample meeting the case definition, with the PSP laboratory register's units and limits;
  - 1.2: the version of record;
  - 1.3: the study cases.
- **Ask B**, each risk's reporting rate per 1,000 patient-years from launch and for the interval, with the patient-years under each and the launch total split by strength (16 figures). It is device-only, and every device is a PSUR section 5 counting rule (ban 1): every channel; tablets per presentation from the xEVMPD; returns credited and deducted; free-of-charge deliveries counted; supply to the DLP; one tablet one patient-day; 365.25 days. Two devices are also named outright:
  - B-D1: `market_supply_channels.xlsx` gives the FR, IT and ES hospital pharmacy channel as "3PL against regional tender call-offs", with its data source and "Hospital-only dispensing for most patients".
  - B-H2: the call-off header reads "Quantities in shipper cases (1 case = 10 packs)".
- **The chart**, `onset_windows_by_risk.svg`: cumulative onset per risk, each 95 per cent window marked, the ILD month in the title. It is keyed to the call (Part 1.4).

Cracker sheet: the response that lands both ILD months, runs the hygiene battery and executes every filed rule.

| Ask | Figures | What the cracker does | Cracker |
|---|---|---|---|
| A, the other five risks' windows | 10 cells | its own estimator on each risk, with courses per 3.2, laboratory onsets per 4.2 and the register, and versions per 1.2 | hit |
| B, reporting rates | 12 rates | the section 5 rules, both channels from the overview, case counts per 1.2, 1.3 and 2.1 | hit |
| B, patient-years | 4 totals | the same supply build, with shipper cases from the header | hit |
| Chart | about 4 parts | windows and title from its own estimate | hit |

Mirror sheet, the same response at rung 2 (the reported cuts): Ask A 0 of 10, Ask B 16 of 16 (device-only, every rule executed), chart about 1 of 4. That is about 57 per cent of the ask weight, so the mirror alone trips the 35 per cent ask gate.

Pair ceiling: 70.1 (cracker 38 + 7 + 55 x 30/30 = 100.0; mirror 2 + 7 + 55 x 17/30 = 40.2; planning weights 38 / 7 / 55 over the 30 ask criteria of the stage 2 arithmetic)

Deferred from the leak reader and never repaired; these matter only to a re-root that keeps this world:
- Ten duplicate links are dated after the DLP and move two herpes zoster cases (annex 7 1.2 against 2.1).
- Seventeen exact duplicate sell-in return rows (66 packs) can be read either as a double extraction or as separate credit notes.
- The rates come out differently on rounded and on unrounded patient-years.

The reader's realism tells are in `leak_check_report.md`.

### The ask layer as built (its pair arithmetic is superseded by the cracker sheet above)

Two asks plus the chart, both asks decoupled from the ILD call in computation and inside it in decision (H18), each multi-dimensional and device-carried, no primary device family shared.

**Ask A: the 80 and 95 per cent months of the other five identified risks (10 cells).** Construction layer: the same truncation-aware estimate on each risk's own reactions, rows the ILD call never reads, so a truncation-blind response is wrong on all ten. Device layer, by risk:

| Device | Family | Risks | Root cause | Organ pair (structural / documentary) | Wrong path, direction |
|---|---|---|---|---|---|
| A-D1 course restarts (primary) | D7, the key lives in another file | serious infections (built: 25% of the reactions in the estimate), herpes zoster (23%) | treatment is interrupted during a serious infection or zoster episode and resumed; a later reaction begins in the restarted course; a restart follows a gap of at least 34 days and a pause lasts at most 25, so every gap before an onset clears the annex's 28 days on either side and any convention near it (more than 28 or 28 and over, days between or days without a dose) builds the same courses | dosage-line history / annex 7 section 3 and the field guide's definition of the listing's therapy start (first dosage line) | origin at the first dose ever: windows longer (built: infection 15/21 against 7/18, zoster 17/25 against 11/21) |
| A-D2 dose changes and short pauses are not courses (over-cleaning half of A-D1) | D7 | VTE (built: 29% of the reactions in the estimate step up from 15 to 30 mg two to seventeen weeks before onset, 2% pause), zoster 6% step-ups and 14% pauses, serious infections 6% and 12%, hepatotoxicity 3% and 2%, neutropenia 2% and 1% | dose escalation after week 4; pauses of 5 to 25 days without a dose for surgery or dental work, starting between day 10 and day 150 of the course, more often the longer the patient has been treated before onset | dosage-line history / annex 7 section 3 | every dosage line a course: windows shorter (built: VTE 4/11 against 6/16, zoster 10/20, infections 6/16) |
| A-D3 laboratory-dated onsets with units per laboratory (primary) | D3 units per source, with D4 (onset absent from the listing) | hepatotoxicity and neutropenia (built: 230 of the 292 hepatotoxicity reactions from day 85 and 147 of the 193 neutropenia reactions, the PSP-monitored ones) | after the hospital's first 12 weeks the patient support programme runs the three-monthly blood tests through contracted laboratories; its solicited reports carry no reporter onset date, the values arrive in the PSP feed; French, Italian and one Munich laboratory report neutrophils per mm3, cell/µL or /µl against a case definition in 10^9/L, and ALT is judged against each laboratory's own upper limit (µkat/L at the Nordic central laboratory), so the hepatotoxicity path turns on the dating and the grade, the neutropenia path on the unit as well | PSP laboratory feed and laboratory register (unit, ULN by sex) / annex 7 section 4 and its case definitions (ALT over 3 x ULN; neutrophils under 1.0 x 10^9/L) | blank-onset reactions dropped, or units ignored so the qualifying sample is missed: windows shorter (the dropped reactions are the late ones); first value over 1 x ULN (grade 1) as onset: onsets earlier (over-corrected stop) |

Hazards on Ask A: H1 post-lock follow-ups that complete a partial onset or correct it by 3 to 40 days (non-ILD cases only), built as the PSP vendor's reconciliation batch received 2 October 2026 (solicited cases) and ordinary follow-ups 1 to 6 October: targeted corrections, laboratory-only reactions included, move onsets from inside each answer month to just before it, so the latest delivered version files every cell a month early, and background corrections move onsets both ways away from every month edge; H1b, ten reactions per non-ILD risk added by a follow-up after the lock; H2 cases first received 1 to 6 October 2026; H3 study cases (the PASS registry). Every Ask A cell sits under its primary device plus H1 at least.

Ask A ladder, built (80 / 95 per cent months; every stop asserted off the answer on both cells, one recorded exception):

| Stop | Path | Zoster | Infections | VTE | Hepatotoxicity | Neutropenia |
|---|---|---|---|---|---|---|
| 1 natural read | origin and onsets as the listing gives them, reported cuts | 12 / 20 | 11 / 17 | 5 / 11 | 3 / 3 | 2 / 3 |
| 2 half device | courses built (and laboratory onsets dated), reported cuts | 8 / 16 | 5 / 11 | 3 / 7 (every line a course) | 3 / 8 | 2 / 7 |
| 3 right method, device missed | truncation-aware, origin at the first dose ever; or laboratory reactions dropped; or units ignored | 17 / 25 | 15 / 21 | | 3 / 4 | 2 / 7 |
| 4 over-corrected | truncation-aware, every dosage line a course; or onset at the first grade-1 sample | 10 / 20 | 6 / 16 | 4 / 11 | 3 / 7 | 3 / 7 |
| 5 latest delivered version | truncation-aware, post-lock follow-ups kept | 10 / 20 | 6 / 17 | 5 / 15 | 3 / 8 | 2 / 7 |
| answer | courses, laboratory onsets, truncation-aware, version at the lock | 11 / 21 | 7 / 18 | 6 / 16 | 4 / 9 | 3 / 8 |

Direction discipline (asserted): for each cell, every combination of {truncation-blind or aware, each device mishandled or not, version at the lock or latest} other than the answer's own lands off the answer. The one recorded exception: neutropenia's 80 per cent cell under first-grade-1 dating stays at month 3, because no PSP sample is taken before day 85 and the 80 per cent cut sits at day 68; its 95 per cent cell moves to 7.

**Ask B: each risk's reporting rate per 1,000 patient-years, from launch and for the twelve months to the lock, to one decimal, with the patient-years under each (nearest 10) and the launch total split by strength (16 figures).** Device-only: no figure depends on the truncation step.

| Device | Family | Root cause | Organ pair | Wrong path |
|---|---|---|---|---|
| B-D1 absent hospital channel (primary) | D4 | in France, Italy and Spain Lyrevo is hospital-dispensed and delivered by the 3PL against regional tender call-offs, outside the wholesaler sell-in feed the commercial team reports from | tender call-off file and market supply-channel table / PSUR section 5 method (every unit supplied to patients, every channel) | sell-in only (built): patient-years 15.3% low from launch and 24.3% low in the interval, every rate 18 and 32% high |
| B-H1 pack size through a two-hop chain | D7 | national article codes in mixed formats (Nordic varenummer, PZN with leading zeros dropped in the German wholesaler's extract, CIP13, AIC, CN, GTIN) | product master (national code to EU presentation) and xEVMPD presentations XML (pack size, strength) / section 5 method | every pack read as 28 tablets (built): patient-years 29.9% low |
| B-H2 shipper cases | D3 units per source | the 3PL counts in shipper cases of 10 packs (unit stated once in the call-off file's header block) | call-off file header / section 5 method | cases read as packs (built): hospital channel 10 times low, patient-years 13.8% low |
| B-H3 returns netted, free goods kept (with the over-cleaning half) | D1 netting | credit notes for returns; zero-value lines for replacement packs and PSP starter packs | document-type field / section 5 method | gross of returns (built): 1.3% high; zero-value lines dropped: 7.8% low |
| B-H4 supply after the lock | D8 cutoff | both supply extracts run on 6 October, the same run that put post-lock cases in the safety export | delivery and invoice dates / section 5 method (supply to the data lock point) | supply to 6 October (built): patient-years 1.2% high from launch, 2.0% in the interval |
| B-H5 one tablet a day for both strengths | D3 | the WHO defined daily dose is 15 mg, the 30 mg tablet is still one daily dose | product master / section 5 method (patient-days = tablets) | mg over DDD: 30 mg tablets counted twice (built): patient-years 37.5% high |

Case-count hazards under every rate: H1 (a post-lock follow-up that adds a reaction does not count), H2 (cases received after the lock), H3 (study cases) and H4 (register duplicates). Every Ask B figure sits under at least two devices. Asserted: every one of the 127 subsets of the seven supply mishandlings moves all 16 figures out of their bins (the one exemption: the 15 mg patient-years under the mg-over-DDD reading alone, which a 15 mg tablet cannot move); each count hazard moves every rate it touches (H1 adds no ILD reaction, so it moves the ten non-ILD rates); term list v3 counts the same cases as v4; every rate computed on the rounded patient-years rounds the same; every patient-year figure at least 1.5 from its nearest-10 edge and not a round hundred; every rate at least 0.015 from its rounding edge (tightest: VTE from launch 11.1655, zoster from launch 23.7334).

Ask B ladder (launch-to-lock patient-years, built):

| Stop | Path | Patient-years | vs answer |
|---|---|---|---|
| 1 natural read | sell-in only, every pack 28 tablets, gross, to 6 October | 44,618 | -39.8% |
| 2 half device | sell-in with chain pack sizes, returns netted | 62,814 | -15.3% |
| 3 channel found, unit missed | plus call-offs read as packs | 63,949 | -13.8% |
| 4 over-cleaned | every channel, zero-value lines dropped | 68,382 | -7.8% |
| 5 dose arithmetic | every channel, 30 mg tablet as two DDDs | 101,997 | +37.5% |
| answer | every channel, chain pack sizes, shipper cases, returns netted, free goods in, supply to 30 September, one tablet a day, 365.25 days | 74,157.0 (74,160) | |

Built answers: patient-years 74,160 from launch (46,320 on 15 mg, 27,840 on 30 mg) and 44,010 in the interval. Rates per 1,000 patient-years, launch and interval: ILD 8.1 and 8.3 (603 and 364 cases), herpes zoster 23.7 and 24.2 (1,760 and 1,065), serious infections 27.2 and 27.2 (2,017 and 1,197), VTE 11.2 and 11.2 (828 and 493), hepatotoxicity 20.5 and 20.5 (1,520 and 903), neutropenia 18.8 and 18.5 (1,393 and 813). The stage 2 target of about 65,500 patient-years moved to 74,160 because the hospital share of the FR, IT and ES markets went from 70 to 80 per cent and PSP bridging packs from 0.16 to 1.4 per new patient, the two changes that cleared the supply-subset cancellations (Tried and rejected).

**The chart** (onset_windows_by_risk.svg): cumulative onset by month for each of the six risks, each 95 per cent window marked, a title giving the ILD month. It carries the decisive construction (coupled), about four criteria.

**Hazard table**

| Hazard | Root cause | Moves |
|---|---|---|
| H1 post-lock follow-up versions | the safety export was run on 6 October to catch cases received by the lock but entered after it; the PSP vendor's reconciliation batch arrived on 2 October | Ask A (onsets of the five non-ILD risks), Ask B (case counts where a follow-up adds a reaction, ten per non-ILD risk) |
| H2 cases first received after the lock | same run | Ask B counts, the interval rates most (every post-lock case would fall in the interval), Ask A (marginal, asserted) |
| H3 study cases | PASS registry reports processed in the same database | Ask B counts, Ask A (marginal) |
| H4 register duplicates | physician and patient reports, literature reports of spontaneous cases | Ask B counts |
| B-H4 supply after the lock | the 6 October run of both supply extracts | Ask B patient-years and every rate |

**Separation line.** The ILD call's declared row population: ILD reactions (term list v4 ILD terms) on the case version current at the lock, first received on or before the lock, report type spontaneous, solicited or literature, master cases only, complete course start and onset, single course before onset. Zero-counts asserted in the generator and written into the ledger at stage 3: A-D1 and A-D2 rows inside it 0 (no ILD case has a restart, escalation or pause before onset); A-D3 rows 0 (ILD is never laboratory-dated); post-lock versions that change an ILD date 0; supply rows 0 (other files). Hazard rows inside it 0: post-lock ILD cases, study ILD cases, ILD duplicates and partial-date ILD reactions all sit outside it, and the generator asserts the ILD months unchanged with each one wrongly let in. The organs the asks need sit in the dosage lines, the PSP feed and register, the supply files and the section 5 method; annex 7 carries only the definitions the call itself uses.

**Referee.** finance_net_sales_by_market_quarter.xlsx: net sales in EUR by market and quarter, byte-clean. French, Italian and Spanish revenue sits far above what their sell-in packs would earn, which arbitrates whether the sell-in feed is the whole supply without handing over a unit count.

**Use test and H18.** Ask A: the RMP team keys every risk's windows into the RMP's routine risk minimisation (the monitoring schedule per risk), the same table the ILD month sits in; it is the other measure the deliverable carries for every candidate, computed off the ILD rows. Ask B: the frequency the RMP states beside each risk's time to onset in the risk characterisation, and the exposure the PSUR files in section 5; a component of each risk's case, computed from supply and case counts. Who acts: Pernille Rasmussen signs the RMP update as QPPV and PRAC assesses it.

**Pair arithmetic** (planning weights 38 / 7 / 55; criteria below):
- Cracker (lands both ILD months): 38 + 7 + 55 x Lc. Expected ask credit: Ask A 4 of 10 (method right, at least one of courses, laboratory onsets and post-lock versions missed on most cells), Ask B 1 of 16 (one missed supply device moves every figure), chart 3 of 4: Lc = 8/30 = 0.27, C = 59.7.
- Mirror (rung 2): r about 2 (only a "one month, not a range" style criterion survives), 7, Ask A 0.5 of 10, Ask B 1 of 16, chart 1 of 4: Ls = 2.5/30 = 0.08, S = 13.6.
- Pair: 36.6 with one cracker in the top two; about 14 to 20 with none. Bar 50, target 40. The weak point is Ask B against a meticulous solver that executes every filed supply rule; the solver round measures it, and the repair is in this layer (deeper silence on the channel and the unit), never in the ladder.

**Criteria arithmetic.** Shape 14 cuts: 2 cuts x 6 risks = 12 (the ILD 95 per cent cell is the call, the ILD 80 per cent cell its critical component, ten cells are Ask A); Ask B: 6 rates x 2 windows + 2 patient-year totals + 2 strength totals = 16; chart parts about 4; instruction following about 3 (both files, whole months, decimals). About 35 before the generator splits the recommendation statement.

## Builder brief

None. The spec-update brief's stop rule applies, so no rebuild follows from this pass. Everything stays as built at efe84a7: the generator, `target/`, `target.zip`, the goldens, `submission.md`, `metadata.json`, `prompt.md` and the card. No `prompt.txt` is written for an architecture that cannot pass the gate. Whoever re-roots the number starts from `## Tried and rejected`.

## Architecture 2 as built (the record until the re-root)

This section records what the stage 2 design and the stage 3 build fixed. Its pair arithmetic, pre-ship claims and strongest-solver test are superseded by the sections above.

### Decision, call and estimand, as filed

- **The call (forward):** the month of treatment by which 95 per cent of interstitial lung disease (ILD) reactions have begun, the month at which the RMP update filed with the PSUR locked on 30 September 2026 ends pulmonary monitoring for patients treated from January 2027. **Target: month 20.** Critical component: the ILD 80 per cent month, **target month 9**.
- **The estimand** (prompt and RMP annex 7): for each identified risk, the distribution of the day of the course on which that risk's reactions begin, counted from the first dose of the course in which the reaction began (day 1), cut at 80 and 95 per cent and stated as the first 30-day month by the end of which at least that share has begun. The prompt's framing (a patient starting now, monitoring that stops at the filed month) makes it a property of a whole course. Annex 7 states every convention and says nothing about how the distribution is estimated beyond "without fitting a parametric model".
- **Change from the draw:** the grid is the 80 and 95 per cent cuts for the six risks (12 cells), not 50, 80 and 95. The median does not move under truncation for the two early-onset risks (hepatotoxicity and neutropenia), so it would hand a truncation-blind response free criteria; the reporting-rate ask replaces those criteria.

### Gate G

Litmus: no reported number is overturned and no stakeholder conclusion is corrected. Every case, date, version and term mapping in the safety database is correct; the difficulty is that a case-only series is right-truncated by each patient's time on treatment at the lock, which no file reports and no field flags. `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`. Deletion test: there is no wrong number to delete; with every summary removed the line listing still offers an onset date and a course start on every row. Instrument test: the database observes exactly what it should, reactions that began and were reported by the lock; the late onsets it lacks have not happened yet, so no repair of a file or of the instrument exists short of waiting, and the estimator is the analysis. Lens-swap test: the naive cut and the answer are not one population under two lenses; the naive cut describes the reactions of patients treated long enough to have had them, the answer describes reactions in treated patients.

### Forks on the main call, as built

| Rival | What closes it |
|---|---|
| Parametric fit (Weibull, lognormal, mixture), with or without the truncation | Annex 7 section 5 (no parametric model) and the long tail; built: Weibull on the reported onsets 13 (8), truncated Weibull 15 (10), truncated lognormal no usable maximum |
| Onset distribution under continuous exposure (discontinuation-adjusted hazard) | Not estimable from the pack (supply volumes only, no patient-level time on treatment) and not annex 7's estimand (reactions that begin during a course) |
| Bound taken from a case's stop date | Stop dates are mostly the withdrawal the reaction caused; the bound is the potential time on treatment at the lock. Built: every recorded stop as a bound files 21 with the 80 per cent cut at month 20 for ILD (collapsed risk sets); a stop the reaction did not cause is a legitimate bound and converges (C1) |
| Cohorts or countries differing | The onset distribution is identical for every start week and market by construction; below month 6 the cuts of 2023, 2024 and 2025 starters agree, which any solver can check |
| Reporting delay | C3 corridor, 0 to 60 days |
| Inverse-probability weighting or a mature cohort in place of the product-limit estimate | Same months by construction (C1), every cut-off from the longest onset to 913 days, 13 quantile definitions |
| Month length, origin, cut rule | Annex 7 sections 3 and 5 (30-day months from day 1; first month by the end of which at least p per cent have begun) |

### Deliverables (fixed at stage 2)

1. `rmp_monitoring_windows_2027.xlsx`: the workbook the RMP team keys from; a windows sheet (six risks by 80 and 95 per cent months, the ILD month as the filed call), a frequency sheet (rates from launch and for the interval, the patient-years under each, the strength split).
2. `onset_windows_by_risk.svg`: cumulative onset by month for each risk, each 95 per cent window marked, title with the ILD month.

xlsx plus svg clears `repeat.deliverables`; no text deliverable, because the QPPV writes the RMP prose herself and the request is for the numbers she keys and the picture PRAC reads.

### Prompt as shipped (prompt.md)

In `task254/prompt.md`, 907 characters, 157 words, one paragraph, opening move stakes-first (reopened at stage 4, below):

> Every patient that reaches the month of treatment we file comes off pulmonary monitoring from January. PRAC wants that month justified in Lyrevo's RMP update, which goes with the PSUR locked on 30 September 2026, and I sign it as QPPV. Give me the month of treatment by which 95 per cent of interstitial lung disease (ILD) reactions have begun. For each of our six identified risks I also need the months by which 80 and 95 per cent of reactions have begun, in whole months of treatment. Then each risk's reporting rate per 1,000 patient-years, from launch and for the twelve months to the lock, to one decimal, with the patient-years under each to the nearest 10 and the launch total split by strength. All of it goes in rmp_monitoring_windows_2027.xlsx. Draw onset_windows_by_risk.svg as well: cumulative onset by month for every risk, each 95 per cent window marked, and a title that gives the ILD month.

`voice-check.py 254`: no flag (919 characters, 20.1 words a sentence, a sentence under 8 words, one rounding tag, no "because"). Bare run over the batch: no unlisted repeats; question-first is 3 of the last 12, and neither of the last two prompts (task229 calendar-first, task253 constraint-first) opens this way. Nothing in it names follow-up, uptake, maturity or a method; no colleague is quoted.

Stage 4 reopening: the pooled heart check (main's cards plus every in-flight card on other branches) returned WARN `repeat.opening`, question-first against task253's redrawn prompt, so the opening became stakes-first (the filed month is where every patient comes off pulmonary monitoring), stated without a direction so it signposts neither an early nor a late month; Lyrevo moved into the second sentence. Every ask, unit and rounding is unchanged; `voice-check.py 254` clean, the only stakes-first opening in the batch. WARN `repeat.gate_g` (method_or_model_selection, as task230): the mechanism family repeats, the driver does not (right-truncated time to onset against a staggered-rollout comparison pool; heart nearest 0.11, this slot's own v1).

### Stage 3 file plan

| # | File | Role | Format | Grain | Size |
|---|---|---|---|---|---|
| 1 | `lyrevo_line_listing_PSUR6_DLP20260930.csv` | spine: the safety database export (run 6 October 2026) | CSV | case version x reaction: case_no, version_no, version_receipt_date, initial_receipt_date, report_type, primary_source, country, sex, age_years, therapy_start_date, therapy_stop_date, reaction_pt, onset_date (full or partial), serious flags, outcome, outcome_date, action_taken | 44,858 rows |
| 2 | `lyrevo_dosage_lines_PSUR6.csv` | courses (A-D1, A-D2) | CSV | case x dosage line: start, stop, daily dose, dose unit (mg or tablet), strength, line end | 23,354 rows |
| 3 | `psp_lab_feed_2023-2026.csv` | laboratory onsets (A-D3) | CSV | sample: psp_patient_ref, case_no, sample_date, analyte, value, unit, lab_code | 8,090 rows |
| 4 | `psp_laboratory_register.xlsx` | units and ULN per laboratory, analyte and sex | XLSX | laboratory x analyte | 27 rows, plus a notes sheet |
| 5 | `duplicate_register_PSUR6.xlsx` | master and duplicate case links | XLSX | link | 455 rows |
| 6 | `rmp_term_list_version_4.xlsx` | MedDRA preferred term to safety concern, identified and potential; v3 to v4 change log sheet | XLSX | term | 123 rows; change log 7 |
| 7 | `RVB-417_RMP_annex7_methods.pdf` | the methods annex, sections 1 to 6 as in the closure table; Lasse Christoffersen as author | PDF | document | 2 pages |
| 8 | `safety_export_field_guide.pdf` | the data dictionary for files 1 to 3 | PDF | document | 2 pages |
| 9 | `sellin_wholesaler_monthly_2023-2026.csv` | retail supply | CSV | wholesaler x market x month x national code x billing type: quantity in packs, net value | 3,293 rows |
| 10 | `tender_calloffs_FR_IT_ES_2025-2026.xlsx` | hospital supply (B-D1, B-H2), header block stating the unit | XLSX | call-off line | 2,461 rows under a five-line header block |
| 11 | `product_master_national_codes.csv` | national code to EU presentation, strength, WHO DDD | CSV | code | 64 rows |
| 12 | `xevmpd_presentations_RVB-417.xml` | EU presentation to pack size and strength (EU/1/23/1754/001 to 004) | XML | presentation | 4 records |
| 13 | `market_supply_channels.xlsx` | which channel supplies each market, from when, and its data source | XLSX | market x channel | 23 rows |
| 14 | `PSUR6_section5_exposure_method.docx` | exposure method: every channel, free goods in, returns netted, one tablet a patient-day for both strengths, 365.25 days, supply to the data lock point | DOCX | document | 2 pages |
| 15 | `finance_net_sales_by_market_quarter.xlsx` | the referee | XLSX | market x quarter | 124 rows |
| 16 | `medinfo_enquiries_2023-2026.xlsx` | distractor: Medical Information enquiry log (topics include ILD monitoring questions) | XLSX | enquiry | 2,057 rows, plus standard responses |
| 17 | `literature_screening_PSUR6.csv` | distractor: weekly literature search hits and their assessment; every valid case it names is already in the listing | CSV | hit | 2,343 rows |
| 18 | `signal_tracker_2026.xlsx` | distractor: validated signals and their status, no windows and no rankings | XLSX | signal | 29 rows |
| 19 | `PSUR6_data_package_log.txt` | provenance: each extraction run (system, query, run time, rows, operator), source and licence notes | TXT | run | short |
| (task folder) | `task254/metadata.json` | pack metadata outside `target/`: sources, dates, licence (CC0, constructed for this task), distractors 16 to 18 named, the referee named, the input gates | JSON | pack | short |

Gates (built): 19 files in `target/`; 6 formats (CSV, XLSX, PDF, DOCX, XML, TXT); largest file 44,858 rows (the line listing); 3 distractors named in `task254/metadata.json` and never in a file name or anywhere under `target/`; every file a system's or a team's real output; provenance in files 19 and 20. Deliverables 2.

Generator construction, for the stage 3 agent:
1. Start cohorts by week from 3 April 2023 to 28 September 2026. Markets and launches: DK 2023-04-03, DE 2023-05-08, SE 2023-06-05, NO 2023-06-12, FI 2023-09-04, NL 2024-03-04, BE 2024-06-03, AT 2024-09-02, FR 2025-02-03, IT 2025-05-05, ES 2025-09-01, PL 2025-11-03, PT 2026-01-05. Steady weekly starts DK 21, DE 200, SE 36, NO 18, FI 16, NL 50, BE 34, AT 26, FR 240, IT 205, ES 165, PL 110, PT 34, each ramping linearly over 43 weeks: about 93,000 starts, 56 per cent in the 12 months before the lock, 17 per cent at least 24 months before it. Start days spread across each week.
2. Cases per risk at a fixed share of starts (ILD 1.0, serious infections 3.0, zoster 3.0, hepatotoxicity 2.0, neutropenia 1.8, VTE 1.2 per cent; ILD and VTE may come down for realism only if the C1 family still converges), onset days (built) from a monthly-mass shape per risk (a monotone cubic through the cumulative monthly masses in `core.RISK_PARAMS`, support to day 705 for ILD), assigned by a low-discrepancy sequence in start order; the courses within 60 days of being as old as the risk's longest onset are then reordered by a greedy herding pass under per-course caps (no onset past its own truncation time), so every mature cut-off and every quantile reading lands on the answer, while the product-limit estimate, whose risk set at day s is the reactions with onset on or before s less those truncated before s, is unchanged by any such reordering. Every other attribute (reporting delay, partial dates, flags) draws on its own seeded stream. A reaction exists in the database when its onset plus a reporting delay (lognormal, median 18 days for spontaneous and solicited reports, 9 for PSP laboratory reports, 150 for literature) falls on or before the lock; receipts 1 to 6 October are the post-lock cases (H2).
3. Non-case reactions (headache, nausea, acne, upper respiratory infection and the like) and the potential risks fill the listing to about 45,000 rows; about 1.75 versions a case.
4. ILD cases: one dosage line from the first dose (a withdrawal stop on or after onset where the drug was stopped), follow-ups that never change a date. Other risks: the A-D1, A-D2 and A-D3 populations at the shares in the ask sheet; PSP-dated reactions are built at 79 per cent of the hepatotoxicity and 76 per cent of the neutropenia reactions from day 85 (the rest are symptomatic or outside the PSP markets and carry a reporter onset date), with three-monthly samples from day 85, the first qualifying sample on the reaction's true onset day, grade 1 values before it in some cases.
5. Texture on every path at realistic rates and inert for every window: partial dates (about 7 per cent of onsets, 2 per cent of starts), duplicates (about 3 per cent of cases, identical dates), study cases (about 4 per cent), literature cases.
6. Supply: sell-in for the retail channel of every market (built: FR, IT and ES retail 20 per cent of their volume), call-offs in shipper cases for the FR, IT and ES hospital channel; presentations 15 mg x 28, 15 mg x 84, 30 mg x 28, 30 mg x 84; credit notes, replacement packs and PSP bridging packs at zero value (1.4 bridging packs a new patient where a market runs the scheme); extracts to 6 October 2026; persistence (58 per cent on treatment at 12 months) and launch stock build as texture; built 74,160 patient-years from launch and 44,010 in the interval.
7. Assertions in the generator and in an independent verifier that reads only `target/`: the C1 family and bin centring for all 12 cells; the five ILD rungs and their months; every cell's rung 2 off its answer; every Ask A stop and every direction-discipline subset off its answer; every Ask B stop and subset outside its bins; the zero-counts; the clean-data and lens-swap tests; the input gates; two consecutive builds byte-identical.

Personas: Pernille Rasmussen (QPPV, the requester; she appears in no document as a voice), Lasse Christoffersen (safety data lead, the field guide and annex 7's author, the extraction log's operator). No other person is named.

### Leak check (stage 4)

`leak.py --asof 2026-10-06`, first run LEAK on one file name: `rmp_term_list_v4.xlsx` (sweep 1 reads `_v<digit>` as author vocabulary); renamed `rmp_term_list_version_4.xlsx` in `pack.py` and `verify.py` and in the write-up, rebuilt (64,603 assertions, byte-identical). Second run REVIEW, no LEAK. Each REVIEW line answered:
- Annex 7 carries 7 of 11 distinctive words of the call: they are the estimand's own words (month of treatment, 95 per cent, interstitial lung disease, pulmonary monitoring) in sections 5.1 and 5.2; it states no month and no figure.
- Annex 7, the PSUR section 5 exposure method and the export field guide carry the sweep's stump terms (reported, reaction, safety, course, population, method, patients): the sweep drew its vocabulary from architecture 1's paragraphs as well as this one's; a direct grep of every document for the truncation vocabulary (truncat, censor, maturity, observable, cohort, time on treatment, not yet begun, tail, reverse, product-limit, Kaplan) finds nothing but the field guide's case follow-up versions.
- `signal_tracker_2026.xlsx` carries dates after 6 October: planned review and due dates on open signals, forward by design.

Reader pass 1 (Sonnet, isolated): no sentence names the decisive step (the reader itself read the annex's rules as the whole method and took the cut off the reported reactions, the stump path); no ranking or answer file; no main-call fork. Deferred to stage 6b: the `market_supply_channels.xlsx` comment and data_source columns that announce Ask B's channel device; the ask forks (post-DLP duplicate links moving two herpes zoster cases, 17 exact duplicate sell-in return rows, rounded against unrounded patient-years under the rates); the realism tells listed in `leak_check_report.md`.

### Guard verdict and WARN answers (draw)

`guard.py check` returned WARN with one finding and the card was filed with `guard.py register` on 2026-10-11, before any ladder was written. WARN answered, `repeat.gate_g` (method_or_model_selection against task253): it is the honest label for an estimator choice. task253's decisive step is the class a survey's nonresponse adjustment is made within, a weighting choice on a sample frame; this build's is the estimator for a case-only series truncated by each patient's follow-up. They share no Layer 2 pattern, strategy, data structure or domain. Nearest driver on file 0.11 (this slot's own v1); every other driver sits at 0.06 or below. The provisional deliverable set (xlsx and svg) clears `repeat.deliverables`, which png and xlsx drew against task253.

## Tried and rejected

- Seed DA04 as written: the area-burned weighting recovered against a 2024 audit corpus built blind to boundary-crossing fires, with twin planning units, two voices and the federal partners' licensed basis. Rejected because a corpus engineered to confirm the wrong rung is the certified-record decoy the guard blocks, the voices and licensed basis are decoys, and the annual reports' origin-based acres would ship as a reconciling series that blesses the wrong method; the decisive construction is kept and restated as an analytical apportionment with the estimand filed.
- Stage 2, the v1 decisive rung: the footprint overlay against origin attribution (80 per cent boundary about 2,690 against about 1,680). Rejected because "acres burned on state-protected land", which every precise standard and the filed weighting clause must state, already poses the question of where each fire's acres burned. Section-tabulated perimeters against a section-keyed map then answer it with one join. The strongest solver overlays every perimeter at once and files the golden, so only Layer 1 hygiene (escaped burns, blank-key duplicates) is left to stop it.
- Stage 2, splitting the overlay into an easy half (the state's own fires re-weighted by footprint, about 1,520) and a hard half (outside-origin fires that ran in, 2,690). Rejected because it is the same pattern in two directions, and a land-centric overlay of the whole atlas collapses the two halves into one step. Moving the federal footprints into a separate file only turns the decisive step into finding a file.
- Stage 2, the plan-year footprint: restating every 2011 to 2025 perimeter onto the map in force for 2027, as an as-if or on-levelling step that defeats the effective-dating reflex of using the map in force at discovery. Rejected because, left unpinned, it forks against the literal as-of reading of "acres burned on state-protected land, 2011 to 2025". Pinning it in the prompt fixes the population, which is banned there, and pinning it in a filed standard makes a filed rule decide.
- Stage 2, lightning complexes ranked as one merged footprint rather than as their member incidents. Rejected because members-as-fires stays defensible unless a filed definition fixes the unit, which is rule application, and linking members to the complex footprint puts identity resolution on the decisive path.
- Stage 2, change of support (burned acres by section against responsibility by quarter-quarter section, with areal weighting in split sections), and GIS acres against the official final size apportioned by GIS share. Rejected because the data supports no determinate rigorous answer beyond what convergence by construction closes (every split section a fire touched burned whole; GIS acres within 0.5 per cent of final size), and once those are closed nothing is left to stump.
- Stage 2, three more candidates: unburned islands inside perimeters, per-agency jurisdictional acreage on mutual-aid reports, and a contract-season window on the acres. Rejected because each one either flips only on reading a field or a definition correctly (data semantics) or opens an estimand fork.
- Architecture 1 (planning bands on burned area apportioned to protection zones by final perimeter rather than placed at the point of origin): spent at stage 2, because the precise estimand names the overlay and gives the step no stump power. Any precise statement of acres burned on state-protected land sends the solver to overlay every perimeter, a single join over section-tabulated footprints, so only Layer 1 hygiene stood between the strongest solver and the golden. The card keeps it in `lineage`.
- Re-root draw, the v1 designer's idea of daily concurrent large fires with large classified by eventual final size (a look-ahead error). Rejected because any precise statement of large on a given day either names the daily size (the step becomes a reading) or is the final-size class itself (then there is no error), and it keeps the wildfire domain the re-root was meant to leave.
- Re-root draw, left truncation of spells converted at a case-system go-live (time in care, tenancy or claim duration measured from the original start with converted survivors counted from day 0). Rejected because it is survivorship, `population_selection`, which `ban.strategy` blocks against task228 in the last three.
- Re-root draw, competing exits read as censoring (one minus Kaplan-Meier against the cumulative incidence). Rejected as the lesson task134 already teaches on its main call.
- Re-root draw, multivariate accommodation (per-dimension central percentile bands against the share of users every adjustment fits). Rejected because the precise estimand, the share of users all adjustments fit, poses the joint check itself, which is the architecture 1 failure in another form.
- Re-root draw, death-registration delays with inquest deaths still unregistered at the extract. Rejected because the object is a registration process's timeliness, which reads as Data Quality Monitoring or official statistics (survey research with descriptive is banned against task253), not as a Descriptive analysis of a substantive distribution.
- Re-root draw, insurance report lags, chargeback label delay and advertising conversion lag. Rejected because each field analyses exactly this with lag triangles or maturity windows by habit, so the decisive step is the field's reflex rather than a step a strong solver skips.
- Re-root draw, noise-inflated spreads of small-unit rates (the distribution of true rates across units). Rejected because the rigorous estimators (moment deconvolution, variance-matched shrinkage, posterior means) disagree on the cut, so the answer forks.
- Re-root draw, statistics read off change-of-state logs as if every logged reading were an equal slice of time. Rejected as a grain step (`grain_or_unit`, banned against task229) whose irregular timestamps a diligent solver checks anyway.
- Stage 2 (architecture 2), the 50 per cent cut in the grid. Dropped because the median of the two early-onset risks (hepatotoxicity, neutropenia) does not move under truncation, so it hands a truncation-blind response free criteria; the 80 and 95 per cent cuts move for all six risks.
- Stage 2, the number of cases each risk's windows rest on as an ask. Dropped because it depends on the estimator: a truncation-aware solver who keeps only mature courses rests the windows on fewer cases than one using the product-limit estimate on all of them, so the count forks.
- Stage 2, case counts per risk as separately graded figures beside the rates. Dropped because the count hazards (post-lock cases, study cases, register duplicates, the version at the lock) are all filed rules a meticulous solver executes, so the six counts leak to both top responses; the counts stay inside the rates, where the supply devices hold them.
- Stage 2, an E2B XML channel (a licensing partner's cases, or EudraVigilance downloads not yet loaded) as an ask device. Dropped because a missing random subset of cases does not move a truncation-aware estimate, so it bites only the truncation-blind response, and its ILD cases would sit inside the call's row population.
- Stage 2, windows for important potential risks as the construction-on-a-segment ask. Dropped because malignancy and MACE have no bounded onset (no 95 per cent cut is identifiable within 42 months of follow-up), and the only device found for the tuberculosis path was a draft term list, which is a decoy document.
- Stage 2, a PSP enrolment file (new patients by month), a pivotal-trial time-to-onset listing or a Weibull signal-detection table in the pack. Dropped because the enrolment file hands over the uptake curve and a rival exposure-weighted estimator, and the other two are records that agree with the truncated answer (trial follow-up stops at 52 weeks), which reads as a filed basis for the wrong method.
- Stage 2, onset support past 24 months for ILD. Dropped because the natural two-year cohort restriction then lands one month short of a mature estimate, a near miss a judge could read as a second defensible answer; with support ending by month 24, every cut-off at or past the longest onset is mature and converges.
- Stage 2, windows in weeks. Dropped because the product-limit estimate and the mature-cohort cuts disagree by one to four weeks at the 95 per cent tail even under exact construction; 30-day months give each cut a bin wide enough to centre.
- Stage 3, three-component lognormal onset mixtures (the stage 2 prototype). Rejected because the gap between the body and the tail left ILD months 12 to 15 almost empty and the mature cut-offs disagreed across quantile definitions; replaced by monthly-mass shapes tuned per risk.
- Stage 3, one low-discrepancy sequence family for every attribute (onset quantile, reporting delay, partial-date flag). Rejected because the irrational steps were correlated (the square root of 5 is twice the golden ratio less one; the square root of 7 sits close to the golden ratio), so delays and partial dates followed the onset quantile, a structure no safety database has; every attribute other than the onset quantile now draws on its own seeded stream.
- Stage 3, herding only the courses at least as old as the risk's longest onset. Rejected because the courses between the longest onset and the support's end stayed uncontrolled and broke the mature cut-offs between them; the herded zone runs from 60 days short of the support with a cap per course (onset within its own truncation time), which leaves the product-limit estimate unchanged.
- Stage 3, short pauses spread over the whole course with one chance per case. Rejected because the every-line-a-course path then left the zoster and serious-infection 95 per cent cells on the answer; pauses now start between day 10 and day 150 with a chance that grows with time on treatment before onset, and VTE step-ups sit two to seventeen weeks before onset.
- Stage 3, post-lock follow-ups on reporter-dated reactions only. Rejected because the latest-version path could not move the hepatotoxicity 95 per cent cell (too few late reporter-dated onsets); the PSP vendor's reconciliation batch now dates laboratory-only reactions too.
- Stage 3, a 70 per cent hospital share in France, Italy and Spain with 0.16 bridging packs a new patient. Rejected because two supply-subset mishandlings cancelled into the answer's nearest-10 bin; the hospital share is 80 per cent, bridging packs 1.4 a new patient, and invoices carry the quantity later credited, after which all 127 subsets clear every bin.
- Stage 3, the every-mapped-term misapplication asserted on the mature cut-offs as well as the estimator. Rejected because with a 12 per cent second ILD term and a bound 60 days short it moved the ILD 80 per cent cell and one serious-infection cut-off; the second ILD term is 7 per cent, and the reading is asserted on the estimator and recorded on the cut-offs (none off the answer).
- Stage 3, mapping post-onset interruption gaps of 26 to 33 days to 25 or 34 days. Rejected because it left a hole and two spikes in the gap histogram that no dosing record shows; only gaps before an onset need to clear the 28-day rule (pauses run 5 to 25 days and restarts follow 34 days or more), so post-onset gaps are left as drawn.
- Spec-update design pass (2026-10-11), architecture 2 under literal determinism. Annex 7 as shipped (5.1 "the risk's reactions in treated patients"; 5.2 "estimated from the post-marketing time to onset data ... without fitting a parametric model") executes word for word to the cut of the reactions on file: ILD 95 per cent month 16 (80 per cent month 7). The golden month 20 therefore rested on reading the population as including the reactions not yet begun at the DLP, which no file states, so the stump was one of the readings. This is the task445 "managers that file" failure; the draw's estimand test had passed a statement that left those members implicit. Filed outright, the clause hands every solver the incompleteness of the series, and every natural correction lands the golden. Measured on the built pack, these all file 9 and 20: cohort cut-offs from 480 to 930 days, the 2023 starters (38 reactions), weighting each reaction by the share of courses started early enough to show it, and the reverse-time product-limit. Only cut-offs under 480 days miss (16 to 19), and they are shorter than both the naive window and the onsets visible to day 693. The default path ends on the golden and the decisive rung is readable (filed sentence, reflex correction), so `precut.py` cannot pass honestly. Stopped under the brief's stop rule, with the decisive step not redesigned here: moving it to how the reactions still to begin are completed, as task445 loop 1 moved its stump to the completion basis, would be a new decisive step on new data.
- Spec-update design pass, the ask layer against the cracker sheet. Ask A (the other five risks' 80 and 95 per cent months) is the call's own truncation-aware estimator on other rows, so it is keyed to the construction. An annex 7 clause the call already reads adjudicates each of its devices (3.2 courses; 4.2 laboratory onsets with the register's units and limits; 1.2 the version of record), so the cracker banks all ten cells. Ask B (rates and patient-years from supply) is device-only, and every device is a PSUR section 5 counting rule. The hospital channel is named in `market_supply_channels.xlsx` (its data_source and comment columns) and the shipper-case unit in the call-off header. So the cracker and the mirror both bank all sixteen figures; the mirror keeps about 57 per cent of the ask weight (over the 35 per cent ask gate) and the pair ceiling is 70.1. A re-root that keeps this world needs ask devices that no filed sentence adjudicates and no column announces.
- Stage 3 generator, the per-risk monthly-mass onset shapes. Each shape carries a secondary hump in that risk's own 95 per cent answer month: ILD mass 4.2 at month 20 against 2.13 and 1.17 either side, and likewise zoster 21, serious infections 18, VTE 16, hepatotoxicity 9, neutropenia 8. So the reported ILD onsets cluster in month 20 (10 against 6 and 2 either side); a hump placed in the answer bin to centre a cut is itself a tell. Also never repaired:
  - the leak reader's realism tells: python-docx template traits, hand-set PDF producers, call-off numbers in steps of 3 and weekend deliveries, constant net unit values, 22 distinct Medical Information questions, one author on five documents;
  - its deferred ask forks: ten duplicate links dated after the DLP moving two zoster cases, 17 exact duplicate sell-in return rows, and rounded against unrounded patient-years under the rates.
