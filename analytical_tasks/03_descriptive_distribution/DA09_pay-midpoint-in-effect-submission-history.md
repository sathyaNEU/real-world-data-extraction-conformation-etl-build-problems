# DA09 — The base-pay midpoint a tech employer posts for Data Engineer III, when the salary platform's "current" record is current at the extract, not on the benchmark date

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · labour markets and compensation benchmarking |
| Mirrors | Band refreshes and pay-transparency postings priced from self-reported salary platforms (Levels.fyi-style sharing and survey panels used at Google, Meta, Amazon and Microsoft), where a respondent's latest record reflects raises after the date the band is meant to describe |
| Decision shape | One figure committed at a date: the midpoint filed in the pay-transparency posting system for the bands taking effect on 1 April 2027 |
| Committed call | The Data Engineer III base-pay midpoint (US national), in dollars to the nearest $1,000 |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E33, the pay records in effect on the benchmark date, which the platform's is_current flag does not mark, with E07 (respondents raked to the workforce) and the company's level crosswalk below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another · #7 uses the ready-made measure · #14 coarsens the segment it was asked about |
| Calibration form | Pilot log: last year's market-band pilot for three role families, with each build's respondents, weights and filed midpoint |
| Driving force | The salary platform marks each respondent's most recent submission as current at the extract (1 March 2027). The band is set on base pay in effect on 1 October 2026. A third of the in-scope respondents submitted again after that date, mostly job changers into AI-lab roles with raises of a quarter or more. The is_current filter is clean, one row per respondent, and matches the platform's own counts, yet it prices the band on pay nobody earned on the benchmark date. Pay in effect is each respondent's latest submission on or before that date: a group-and-rank over the submission history. |

## 1. Situation

A software company refreshes its engineering pay bands each year. Its compensation policy sets each band's midpoint at the market median
base pay for the job's family and level, in the US workforce, as in effect on the benchmark date of 1 October 2026. The market is read
from a salary-sharing platform's licensed extract, taken 1 March 2027. The extract holds every submission since 2024, each with a
respondent ID, employer, title, the platform's normalised level, state, years of experience, base pay, submission date and an is_current
flag. The pack also holds the OEWS employment margins, the company's job-architecture crosswalk (employer × title to company level), the
platform's methodology page, and the pilot log. Postings switch to the new bands on 1 April.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each submission reports what the respondent was paid when they submitted, the flag marks the
  latest one exactly as documented, and the margins and crosswalk are right. Nobody's reading of their own numbers is overturned. The
  difficulty is which of each respondent's records describes the benchmark date.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of rewards' view and the recruiters' licensed basis. The is_current filter still gives a clean table
  of one row per respondent that ties to the platform's published respondent counts, and raking it is still the competent build.
* **Instrument repair.** Make every submission perfect; each already reports its own date's pay. Pay on a past date is fixed by which
  record was standing on that date, a selection across a respondent's history that no single record, however accurate, makes.
* **Lens swap.** The two reads describe different moments. The is_current records describe pay at the extract, a third of them after a
  job change. The answer describes pay standing on 1 October 2026.

## 3. The driving force

A strong solver maps titles to the company's levels through the crosswalk and rakes respondents to OEWS employment by state group and
experience band, trimming weights as the policy says. It keeps each respondent's current record, as the platform does. Each step can be
checked: the pilot log's three filed midpoints reproduce exactly under this build. But the pilot's extract was taken on its own benchmark
date, so its current records were the ones in effect. This year's extract was taken five months after the benchmark date, and 34% of the
in-scope respondents have submissions after 1 October 2026, mostly job changes into AI-lab roles at raises of 20% to 100%. Their current
records describe pay they were not earning on the benchmark date. Pay in effect is each respondent's latest submission on or before that
date, which takes ranking each respondent's history by date and cutting at 1 October. At III, that moves the raked median from $186,000
to $166,000.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | is_current records at the platform's level III, unweighted median | $230,000 (+38.4%) | The platform's own respondent set and level, as its published tables use them | The OEWS margins: respondents over-represent two high-pay metros and early-career engineers against the US workforce |
| 1 | Same records raked to OEWS state group × experience band, weights trimmed per the policy (E07) | $206,000 (+24.3%) | The population the policy names, reached the standard way | The company's crosswalk: big-tech titles the platform calls III are level IV in the company's architecture |
| 2 | Raked, with level from the company's crosswalk | $186,000 (+12.0%) | Reproduces all three of the pilot log's filed midpoints exactly | The submission history: 34% of in-scope respondents' current records are dated after 1 October 2026, and each has an earlier record standing on that date |
| 3 | **Decisive:** each respondent's latest submission on or before 1 October 2026, crosswalked and raked | **$166,000** | — | — |

* **Figure shape.** Every correction walks the figure down, and the answer is the minimum cell. A posting priced at any rung above it
  overstates the market and pushes every Data Engineer III salary review upward.
* **Partial correction priced (L3).** A solver who drops respondents whose current record post-dates the benchmark date, instead of
  replacing it with their standing record, loses the job changers' pre-move pay, which sat mostly below the median (people move because
  they are underpaid), and lands at $185,000 (+11.4%) even after re-raking. A solver who ages current records back to the benchmark date with the platform's pay index lands at $183,000
  (+10.2%), because the index tracks raises in post, not job changes.
* **Grid.** Level map (platform or crosswalk) × weighting (unweighted or raked) × record (current or in effect) gives 8 cells. The
  nearest non-answer cells sit at +11.0% (platform level, raked, in effect) and +11.3% (crosswalk, unweighted, in effect).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy names the benchmark date. The platform's methodology page defines is_current as "the respondent's
   most recent submission", accurately. No document says the two moments differ, or how a record in effect is chosen.
2. **Corpus blind for a computable reason.** *In every pilot build the extract was taken on the benchmark date itself, so each
   respondent's most recent submission was the one in effect.* The pilot's three filed midpoints reproduce under rungs 2 and 3 alike, and
   certify the crosswalk, the raking and the trimming.
3. **No arithmetic symptom.** One row per respondent, counts tied to the platform's published tables, weights meeting every margin. The
   is_current table is complete and clean.
4. **Not a row predicate.** The record in effect is a rank within each respondent's history, cut at a date. No column marks it, and the
   flag marks a different record for a third of respondents.
5. **The enumeration is arithmetic.** 1,412 of 4,150 in-scope respondents take a different record, found only by ranking their
   histories.
6. **No cutover date.** Job changes run continuously through the extract window, and no pay series steps on any date.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, is_current is still how the platform presents its data.

## 6. The calibration corpus

* **Form.** The pilot log of last year's market-band pilot: for Data Engineer, ML Engineer and SRE at level III, the extract used (taken
  on that year's benchmark date), the respondents kept, the crosswalked levels, the raked and trimmed weights, and the filed midpoint for
  each.
* **What it certifies.** The crosswalk, the raking margins and the trimming rule. All three filed midpoints reproduce exactly. Without
  the crosswalk, ML Engineer misses by $14,000. Untrimmed, SRE misses by $6,000.
* **What it is blind to.** The record in effect (above).
* **Twin pair.** Respondents R-20817 and R-31544 have identical current records: same employer, title, crosswalked level, state,
  experience band and base pay ($228,000), both submitted on 14 January 2027. On 1 October 2026 their standing records were $228,000 and
  $114,000 (2.0×), because R-31544 moved from a non-tech analytics job in December. Only their histories separate them.
* **Resemblance points at the decoy.** This year's in-scope respondents most resemble the pilot's by state and experience mix, and the
  pilot's current records were the ones in effect.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The compensation policy: "A band's midpoint is the market median base pay for its family and level in the US
  workforce, as in effect on the benchmark date of 1 October 2026, stated to the nearest $1,000." The policy: "Respondents are raked to
  OEWS employment by state group and experience band; weights above five times the median are capped and the sample re-raked once." The
  job-architecture crosswalk assigns company levels to employer-title pairs. The weighted median is the smallest pay with cumulative
  weight of at least half.
* **Empirical pins.** The trimming and crosswalk, as reproduced by the pilot.
* **Voices.** The head of rewards: "The platform is the best market data we've ever had. Use its figures as they come." The recruiting
  lead for data roles: "Candidates are quoting us AI-lab offers every week, and the band has to see them."
* **Licensed wrong basis.** The policy records that the recruiting team benchmarks offers on the platform's current records and will
  bring its own midpoint to the sign-off.

## 8. Determinism by construction

* **Late joiners.** Respondents whose first submission post-dates the benchmark date (6% of the extract) have no record standing on it.
  Excluding them, or using their first record, moves the median by under $1,000.
* **Same-day records.** No respondent has two submissions on one date, so "latest on or before" is unique.
* **Raking.** The policy fixes the margins and the trim. Iterating to 0.1% or 0.01% margin fit files the same thousand.
* **Rounding.** The weighted median at rung 3 ($165,820) sits clear of a thousand boundary, and no other construction lands within $500
  of one.

## 9. Prompt sketch and deliverables

> Our pay-transparency postings switch to the 2027 bands on 1 April, and the first one I have to sign off is the base-pay midpoint for
> Data Engineer III. Our head of rewards trusts the salary platform's figures as they come. Give me the midpoint to the nearest thousand
> dollars, as the line that goes in the posting system, and send `band_build.xlsx` with the sheets below, plus `pay_in_effect.png`.

* `band_build.xlsx` — the respondent build, the four rung constructions with each one's pilot reproduction (ask C), the offer sheet
  (ask A) and the equity sheet (ask B).
* `pay_in_effect.png` — the weighted cumulative distribution of Data Engineer III base pay under current records and records in effect,
  the two medians labelled, the 1 October 2026 cut marked on an inset timeline of submissions, and the twin respondents annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** The company's offer acceptance rate for engineering roles in each of the six state groups in
  each quarter of 2026. *Device:* an offer revised after negotiation creates a new offer record on the same requisition and candidate,
  with a revision number, as the applicant-tracking guide documents. Counting revisions as offers understates acceptance by 9 to 22
  points in 17 of the 24 cells.
* **Ask B (device-carried).** Median new-hire equity grant value for each of the four engineering families at levels III and IV in 2026.
  *Device:* grants are recorded in units, and the plan values them at the grant date's fair value from the valuation table, as the equity
  plan documents. Valuing units at the latest price overstates every cell by 31% to 58%.
* **Ask C (validity).** The midpoint under each of the four rung constructions, with each construction's reproduction of the pilot's
  three filed midpoints.
* **Decoupling.** The applicant-tracking system and the equity ledger share no row with the salary extract. Clearing the record-in-effect
  rule changes no figure in asks A or B.

## 11. Rubric arithmetic

6 state groups × 4 quarters (ask A) + 4 families × 2 levels (ask B) + 4 constructions × 2 (ask C) + the committed midpoint, the respondents
re-recorded and the twin pair's standing pay + 4 named chart parts + 2 files ≈ 49 criteria.

## 12. World-building constraints

* 4,150 in-scope respondents at crosswalked level III. 1,412 have current records dated after 1 October 2026, at a median raise of 26%
  over their standing records.
* Medians by rung are $230,000 / $206,000 / $186,000 / $166,000. The other grid cells are $205,000, $207,000, $184,000 and $185,000. The
  partial cells are $185,000 (dropping) and $183,000 (index-aged). The job changers' standing records sit mostly below the median.
* The pilot's three extracts were taken on their benchmark date. Its filed midpoints reproduce exactly under the crosswalk and the
  trimmed raking.
* R-20817 and R-31544 are identical on every current-record column.
* The applicant-tracking system and the equity ledger touch no salary-extract row.
