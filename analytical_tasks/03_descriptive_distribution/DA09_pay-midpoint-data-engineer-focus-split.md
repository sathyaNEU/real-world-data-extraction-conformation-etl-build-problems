# DA09 — The base-pay midpoint a tech employer posts for Data Engineer III, when the salary platform files ML data engineers in the same family

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · labour markets and compensation benchmarking |
| Mirrors | Pricing a job from a salary platform whose job-family label mixes roles a company's job architecture separates (Levels.fyi-style focus tags, survey job matching at Google, Meta, Amazon and Microsoft, where data engineering and ML-infrastructure data work sit in different job families with different bands) |
| Decision shape | One figure committed at a date: the midpoint filed in the pay-transparency posting system for the bands taking effect on 1 April 2027 |
| Committed call | The Data Engineer III base-pay midpoint (US national), in dollars to the nearest $1,000 |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E29, the platform's Data Engineering family split by each respondent's primary focus (the profile table) as the company's job architecture moves ML data work into its ML family, with E07 (respondents raked to the OEWS workforce) and the company's level crosswalk below it, and a pilot log blind to the split (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #13 validates on one population, applies to another · #7 uses the ready-made measure · #14 coarsens the segment it was asked about |
| Calibration form | Pilot log: last year's market-band pilot for three role families, with each build's respondents, weights and filed midpoint |
| Driving force | The platform files every data engineer under one Data Engineering family. The company's job architecture prices training-data and feature-pipeline work in its ML family, and only the platform's profile table, which records each respondent's primary focus, says who does that work. 1,060 of the 4,150 respondents at crosswalked level III name ML data as their primary focus, at a median base of $236,000. No title, employer tag or level separates them: 62% work at large tech companies under plain Data Engineer titles. The crosswalked, raked family median is a correct market figure for a population that includes them, and the company's Data Engineer III is the population without them. |

## 1. Situation

A software company refreshes its engineering pay bands each year. Its compensation policy sets each band's midpoint at the market median
base pay for the job and level, in the US workforce, as in effect on the benchmark date of 1 October 2026. The market is read from a
salary-sharing platform's licensed extract, taken on the benchmark date. The extract holds each respondent's current record (employer,
title, the platform's family and normalised level, employer level code, state, years of experience, base pay). The pack also holds the
platform's profile table (each respondent's primary focus), the OEWS employment margins, the company's job architecture with its job
definitions, the level crosswalk (employer × level code to company level), the platform's methodology page and the pilot log. Postings
switch to the new bands on 1 April.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each record reports what the respondent was paid on the benchmark date, the family label is the
  platform's own taxonomy applied as documented, and the profiles, margins and crosswalk are right. Nobody's reading of their own numbers
  is overturned. The difficulty is which respondents hold the company's job.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of rewards' view and the recruiters' licensed basis. The Data Engineering family is still the
  platform's answer to "data engineers", the crosswalked and raked build still reproduces the pilot, and the profile table still sits
  unjoined.
* **Instrument repair.** Clean-data test. No file is suspect. The extract was taken on the benchmark date, so each current record is the
  one in effect, and every field is filled. The family label is a correct field for a different attribute (the platform's taxonomy, not
  the company's job). The profile table carries a primary focus on every profile, and the crosswalk maps levels, complete, in one version.
  Nothing is left to fill, correct or replace. Rung 0 returns $230,000, rung 1 $206,000 and rung 2 $186,000. The answer stays $158,000,
  and the split by primary focus is still needed, because the company defines its job by work that no extract column names.
* **Lens swap.** The two reads describe different populations: the platform's Data Engineering family, 4,150 respondents at III,
  against the company's Data Engineer job, 3,090 of them. The 1,060 ML data engineers are in one and not the other.

## 3. The driving force

A strong solver maps employer level codes to the company's levels through the crosswalk and rakes respondents to OEWS employment by
state group and experience band, trimming weights as the policy says. It takes the platform's Data Engineering family as the job, as the
platform's own tables do. Each step can be checked: the pilot log's three filed midpoints reproduce exactly under this build. But the
pilot priced ML Engineer, SRE and Security Engineer, and the job architecture splits none of those platform families. It does split this
one. The company's Data Engineer builds and operates pipelines and platforms; training-data and feature-pipeline work for machine-learning
models is an ML Engineer (data) job, banded in the ML family. The platform files both under Data Engineering, and at large tech companies
both carry the title Data Engineer. Only the profile table, joined on respondent ID, records each respondent's primary focus. A quarter
of the family names ML data, and they are the best-paid quarter. At III, removing them moves the raked median from $186,000 to $158,000.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The platform's Data Engineering family at its level III, unweighted median | $230,000 (+45.6%) | The platform's own respondent set, family and level, as its published tables use them | The OEWS margins: respondents over-represent two high-pay metros and early-career engineers against the US workforce |
| 1 | Same respondents raked to OEWS state group × experience band, weights trimmed per the policy (E07) | $206,000 (+30.4%) | The population the policy names, reached the standard way | The company's crosswalk: big-tech codes the platform calls III are level IV in the company's architecture |
| 2 | Raked, with level from the company's crosswalk | $186,000 (+17.7%) | Reproduces all three of the pilot log's filed midpoints exactly | The job architecture: ML data work belongs to the ML family, and 1,060 in-scope profiles name ML data as their primary focus |
| 3 | **Decisive:** respondents whose primary focus is pipelines and platforms (profile join), crosswalked and raked (E29) | **$158,000** | — | — |

* **Figure shape.** Every correction walks the figure down, and the answer is the minimum cell. A posting priced at any rung above it
  prices the company's Data Engineer III on ML-infrastructure pay and pushes every salary review in the job upward.
* **Partial correction priced (L3).** A solver who splits on the platform's AI-lab employer tag catches the 24% of ML data engineers who
  work at AI labs, drops the pipeline engineers there, and lands at $177,000 (+12.0%). One who splits on "ML" or "AI" in the title catches
  18% of them and lands at $181,000 (+14.6%). Neither reaches the plain-titled ML data engineers at large tech companies.
* **Grid.** Level map (platform or crosswalk) × weighting (unweighted or raked) × population (platform family or profile split) gives 8
  cells. The nearest non-answer cells sit at $176,000 (+11.4%: crosswalk, unweighted, split) and $178,000 (+12.7%: platform level, raked,
  split).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says the midpoint is the market median for the job and level. The job architecture defines each job by
   its work. The platform's methodology page says the family comes from title keywords and the employer's job function. No document says
   the platform's family mixes two company jobs, or that the profile table's primary focus is where the line falls.
2. **Corpus blind for a computable reason.** *In every pilot build the platform's family and the company's job held the same respondents,
   because the pilot priced ML Engineer, SRE and Security Engineer, and the job architecture splits none of those families.* The pilot's
   three filed midpoints reproduce under rungs 2 and 3 alike, and certify the crosswalk, the raking and the trimming.
3. **No arithmetic symptom.** One row per respondent, counts tied to the platform's published tables, weights meeting every margin. The
   family is complete and clean, and the ML data engineers' pay sits inside the family's range.
4. **Not a row predicate.** The split needs a join to the profile table and a reading of the job architecture's definitions. No extract
   column carries the focus, and the title, the employer tag and the level each catch less than a quarter of the ML data engineers.
5. **The enumeration is arithmetic.** 1,060 of 4,150 in-scope respondents leave the population, found only through the profile join.
6. **No cutover date.** The platform's family and the job architecture have both stood for years, and no pay series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the family is still how the platform presents its data.

## 6. The calibration corpus

* **Form.** The pilot log of last year's market-band pilot: for ML Engineer, SRE and Security Engineer at level III, the extract used, the
  respondents kept, the crosswalked levels, the raked and trimmed weights, and the filed midpoint for each.
* **What it certifies.** The crosswalk, the raking margins and the trimming rule. All three filed midpoints reproduce exactly. Without the
  crosswalk, ML Engineer misses by $14,000. Untrimmed, SRE misses by $6,000.
* **What it is blind to.** The job split (above).
* **Twin pair.** Lumen Ledger, a payments company, and Orrery Systems, a cloud company, are identical on every extract column at
  crosswalked III: 64 Data Engineering respondents each, the same state and experience mix, the same median base pay of $214,000. In the
  company's Data Engineer job they hold 58 and 29 respondents (2.0×), because half of Orrery's data engineers name ML data as their
  primary focus. Only the profile join separates them.
* **Resemblance points at the decoy.** This year's Data Engineering family most resembles the pilot's ML Engineer family by employer and
  metro mix, a family the architecture leaves whole.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The compensation policy: "A band's midpoint is the market median base pay for its job and level in the US workforce,
  as in effect on the benchmark date of 1 October 2026, stated to the nearest $1,000." The policy: "Respondents are raked to OEWS
  employment by state group and experience band; weights above five times the median are capped and the sample re-raked once." The job
  architecture's definitions: "Data Engineer: builds and operates data pipelines and data platforms. ML Engineer (data): builds
  training-data and feature pipelines for machine-learning models." The crosswalk assigns company levels to employer level codes. The
  weighted median is the smallest pay with cumulative weight of at least half.
* **Empirical pins.** The trimming and the crosswalk, as reproduced by the pilot.
* **Voices.** The head of rewards: "The platform is the best market data we've ever had. Use its figures as they come." The recruiting
  lead for data roles: "Candidates are quoting us AI-lab offers every week, and the band has to see them."
* **Licensed wrong basis.** The policy records that the recruiting team benchmarks offers on the platform's Data Engineering family
  table and will bring its own midpoint to the sign-off.

## 8. Determinism by construction

* **Focus.** Every profile carries exactly one primary focus from the platform's fixed list, and the profile table joins one-to-one to
  the extract's respondents.
* **Raking.** Every construction rakes the respondents it keeps to the policy's margins and trims as the policy says. Iterating to 0.1%
  or 0.01% margin fit files the same thousand.
* **Records.** The extract was taken on the benchmark date, and no respondent has two records on one date, so the current record is
  unique and in effect.
* **Rounding.** The weighted median at rung 3 ($158,370) sits clear of a thousand boundary, and no other construction lands within $500
  of one.

## 9. Prompt sketch and deliverables

> Our pay-transparency postings switch to the 2027 bands on 1 April, and the first one I have to sign off is the base-pay midpoint for
> Data Engineer III. Our head of rewards trusts the salary platform's figures as they come. Give me the midpoint to the nearest thousand
> dollars, as the line that goes in the posting system, and send `band_build.xlsx` with the sheets below, plus `data_engineer_pay.png`.

* `band_build.xlsx` — the respondent build, the four rung constructions with each one's pilot reproduction (ask C), the offer sheet
  (ask A) and the equity sheet (ask B).
* `data_engineer_pay.png` — the weighted cumulative distribution of level III base pay for the platform's family and for the company's
  job, the two medians labelled, the ML data engineers drawn in a separate colour, and the twin employers annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** The company's offer acceptance rate for engineering roles in each of the six state groups in
  each quarter of 2026. *Device:* an offer revised after negotiation creates a new offer record on the same requisition and candidate,
  with a revision number, as the applicant-tracking guide documents. Counting revisions as offers understates acceptance by 9 to 22
  points in 17 of the 24 cells.
* **Ask B (device-carried).** Median new-hire equity grant value for each of the four engineering families at levels III and IV in 2026.
  *Device:* grants are recorded in units, and the plan values them at the grant date's fair value from the valuation table, as the equity
  plan documents. Valuing units at the latest price overstates every cell by 31% to 58%.
* **Ask C (validity).** The midpoint under each of the four rung constructions, with each construction's reproduction of the pilot's
  three filed midpoints, and the twin employers' respondent counts in the company's job.
* **Decoupling.** The applicant-tracking system and the equity ledger share no row with the salary extract or the profile table.
  Clearing the focus split changes no figure in asks A or B.

## 11. Rubric arithmetic

6 state groups × 4 quarters (ask A) + 4 families × 2 levels (ask B) + 4 constructions × 2 and 2 twin counts (ask C) + the committed
midpoint + 4 named chart parts + 2 files ≈ 49 criteria.

## 12. World-building constraints

* 4,150 Data Engineering respondents at crosswalked level III: 3,090 with primary focus on pipelines and platforms, 1,060 on ML data
  (median base $236,000; 62% at large tech companies, all titled plain Data Engineer, 24% at AI labs and 14% elsewhere; 18% carry ML or
  AI in the title).
* Medians by rung are $230,000 / $206,000 / $186,000 / $158,000. The other grid cells are $207,000, $199,000, $176,000 and $178,000. The
  partial cells are $177,000 (AI-lab tag) and $181,000 (title keywords).
* The pilot's three families are not split by the job architecture. Its filed midpoints reproduce exactly under the crosswalk and the
  trimmed raking.
* Lumen Ledger and Orrery Systems are identical on every extract column at III; 58 and 29 of their respondents hold the company's job.
* The applicant-tracking system and the equity ledger touch no salary-extract or profile row.
