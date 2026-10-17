# task237 design note

Architecture 1, wave 3, seed DQ10 (whether a translated questionnaire passes the release gate on reliability): the
seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Psychology &
Behavioral Science, psychometric measurement and scale validation, Data Quality Monitoring & Alerting. The Survey
Research Centre at Marlowe University runs a province's Community Connections Survey, whose core measure is the
twelve-item Belonging and Connection Scale (BCS-12: six statements worded towards connectedness and six away from it,
alternating, answered on a five-point agreement scale; BCS02, BCS04, BCS06, BCS08, BCS10 and BCS12 are reverse-scored).
For wave 6 the centre translated the BCS-12 into ten more languages and piloted each version with one of two fieldwork
vendors (an online panel, Nesscroft Panels, for six; interviewer-administered CAPI, Fernlow Research, for four). Its
translation and adaptation standard (TAS-4) gates every new version on the reliability of its total score in the pilot:
released for the wave's fieldwork at 0.80 or more, held for cognitive interviews and a second pilot from 0.70, sent back
for retranslation below 0.70. The standard defines the reliability as the share of the total score's variance, across
the pilot's valid completes who answered all twelve items, that is due to differences in connectedness. The translation
quality lead signs off the ten decisions on Monday 1 March 2027, three weeks before the wave 6 fieldwork launches.

## Draw

Card `cards/task237.json` (architecture 1, registered 2026-10-17). Guard verdict PASS (the third persona redrawn from
the en_CA pool after two first names met older builds).

- **Pairing.** Psychology & Behavioral Science / psychometric-measurement-scale-validation, serving Data Quality
  Monitoring & Alerting (the domain index lists this task type under DD and DQ). Never built before on this objective;
  not banned against the last three builds (task236, task264, task156). The object is the quality of each language
  version's data as a measure (whether its scores measure connectedness reliably enough to field), the call a release
  gate. task257 (a psychometric DD build) counts dimensions under lopsided splits; nothing here repeats it.
- **Niche.** Negatively worded items behave differently across translations: where a language renders negation in a
  way respondents answer by its form as well as its content, the six negatively worded items take on a shared wording
  factor of their own. That variance is common to those items, so it raises the items' agreement, and it is not
  connectedness.
- **The call.** For each of the ten new language versions: release for the wave 6 fieldwork, hold for a second pilot,
  or rework (retranslate). Forward facing: the decisions govern the wave 6 fieldwork, which has not started.
- **Shape.** 07, a grid of cells: ten versions, each with its decision, its valid pilot completes and its pilot mean
  score (30 cells), the chart's parts (4 to 5), the two critical components and the files: about 37 criteria. Decision
  designation_set, answer set_of_items, question form what.
- **Strategy.** decomposition_attribution with G17 decisive (the measurement model the data supports: the score's
  common variance split into the trait's part and the wording factor's) and G16 supporting (the reliability
  coefficient chosen to match the standard's quantity); Gate G decomposition_attribution; calibration none; context
  artifact register (the translation register); layer 2 family field_method, pattern
  own:trait-share-under-a-wording-method-factor.
- **Forum, event, organisation.** line_manager_or_team (the translation quality lead signs off; no committee),
  launch_or_rollout (the wave 6 fieldwork), university_or_school (a university survey research centre).
- **People** (`guard.py names --geo Canada --seed 237`): Tara Bauer, translation quality lead, who signs off the
  decisions; Rodney Fernandez, translation coordinator, who keeps the translation register; Cindy Stein, pilot
  fieldwork manager, who receives the vendors' files.
- **Deliverables.** `bcs12_wave6_release_decisions.csv` (one row per version: the decision, the valid pilot completes
  and the pilot mean score) and `bcs12_wave6_release_chart.png` (each version against the release bands).
- **Data-native sentence.** In six of the ten translations the six negatively worded items share variance with each
  other that they do not share with the six positively worded ones, so the items' average agreement (alpha) and a
  one-factor model both count that wording variance as connectedness; the standard's quantity is the trait's share of
  the score, which only a model giving the negatively worded items their own wording factor recovers.
- **As of.** Monday 1 March 2027 (the vendors' final files of Friday 26 February 2027; the wave 6 fieldwork launches on
  Monday 22 March 2027).

Sources, one line each (what it teaches; how this build differs):
- Psychometric practice on reverse-keyed method effects (bifactor and correlated-uniqueness models, omega
  hierarchical): negatively worded items often form a method factor, stronger in some languages and samples; here it
  is the decisive structure of a translation gate, not a validation study's finding.
- Seed DQ10: the world, the decision and the quantity only; its pitfall (alpha against congeneric omega) is a wrong
  rung here.
- Spent on this objective (`guard.py mechanisms`): task229 (a convex conversion of a daily mean), task231 (a rate over
  active units with late exits), task232 (transmission from delayed mixed outcomes), task230 (a late channel's net
  classification bias), task228 (variance at the randomised unit), task233 (a missing-not-at-random departure),
  task234 (a source's output from a share a loss cannot move), task235 (a missing event censored until its device's
  next contact), task236 (a capture share against an independent fixed-protocol sample). None separates a composite's
  variance into its target attribute and a second source shared by a subset of its components.

## Default path

1. Read the translation and adaptation standard: each version's reliability (the share of its total score's variance
   due to differences in connectedness) on its pilot's valid completes who answered all twelve items, against the
   bands 0.80 and 0.70.
2. Build each version's valid pilot completes from the two vendors' files, reverse-score BCS02, BCS04, BCS06, BCS08,
   BCS10 and BCS12, and take the covariance of the twelve item scores over those who answered every item.
3. Estimate each version's reliability with Cronbach's alpha (or omega from a one-factor model) and apply the bands.

Ends on: 6 of the 10 versions wrong (the Mandarin, Tagalog, Arabic, Vietnamese and Korean versions released and the
Cantonese version held, where the trait's share puts the first four and the Korean version on hold and the Vietnamese
and Cantonese versions to rework; alpha releases eight of the ten).

Golden: release the Punjabi, Spanish and Persian versions; hold the Mandarin, Tagalog, Arabic and Korean versions;
rework the Cantonese, Urdu and Vietnamese versions.

## Stump sentence

A competent solver gates each version on Cronbach's alpha or a one-factor omega and files 6 of the 10 versions wrong
(Ends on: the Mandarin, Tagalog, Arabic, Vietnamese and Korean versions released and the Cantonese version held); the
step that lands it there is taking the score's whole common variance for connectedness when, in those six
translations, the negatively worded items share a wording factor that the standard's quantity leaves out.

## Three rules

- **Task type:** psychology-behavioral-science / psychometric-measurement-scale-validation, which serves Data Quality
  Monitoring & Alerting; the object is whether each translated version's data measure the trait reliably enough to
  field, and the call is the release gate.
- **Domain test:** the quantity that decides is each version's share of total-score variance due to the trait (omega
  hierarchical) under the measurement model its pilot responses support, with a reverse-keyed wording factor separated
  from connectedness: the field's own reliability analysis for a scale with mixed item keying.
- **Swap:** with meters or wards for items there are no negatively worded statements, no translation that changes how
  negation is answered and no latent trait to separate from a response style; the decisive analysis has nothing to act
  on.
- **Layer 1:** two vendors' layouts (a wide online panel export and a long interviewer-administered file keyed by sample
  case); missing-answer codes that differ by vendor (9, -8, -9, blank or no row for not reached); panel retakes under
  fresh entry ids, some from second accounts the panel merged afterwards; screen-outs, partials and soft-launch entries
  in the panel export; interviews the vendor's back-check could not confirm, their cases reissued to other interviewers;
  cases revisited after a break-off; pretest interviews in the CAPI file; respondents who left in the background questions after the module. Each is how
  the system that writes it behaves; none is placed to be caught, and none moves a decision (R2, asserted).
- **Layer 2:** field_method, the trait's share of the score under the measurement model the data supports: alpha, a
  one-factor omega and omega total from a model with the wording factor each count the wording variance as
  connectedness where the factor is present.
- **Decisive step:** modelling each version's item responses with a wording factor on the negatively worded items
  (or their correlated residuals) where the data show one, and taking the trait's share of the total score's variance
  from that model rather than the items' whole common variance.
- **Not semantics:** the default path reads every field, code and rule right (valid completes built, items reversed,
  the standard's definition of reliability read correctly) and still files 6 of the 10 versions wrong; what it gets
  wrong is the measurement model, which no field states.
- **Not rule application:** the standard files the quantity (the share of the score's variance due to connectedness),
  the population (the pilot's valid completes who answered every item) and the bands; no rule names a coefficient or a
  model, and executing every stated rule still leaves the estimation.
- **Analyst test:** a strong analyst who builds the valid completes, reverses the six negatively worded items, reads
  the standard's definition correctly and estimates it with Cronbach's alpha or a one-factor omega files 6 of the 10
  versions wrong (Ends on: the Mandarin, Tagalog, Arabic, Vietnamese and Korean versions released and the Cantonese
  version held).
- **Estimand:** TAS-4 s.6 (in the pack) fixes the population (each version's valid pilot completes who answered all
  twelve items), the outcome (the total score as s.5 scores it), the quantity (the share of its variance due to
  differences between those respondents in connectedness) and the comparison (the bands at 0.80 and 0.70, unrounded).
- **No decoy:** nothing is planted: no memo, earlier report, vendor summary or figure states a version's reliability
  or a decision; the translation register records the translation process only.
- **No certified replay:** no certified or published reliability for a new version exists for a method to reproduce;
  the manual's English figure is the source version's.
- **Lesson:** a composite's agreement is not its target attribute's share when a subset of its parts shares a second
  source; no build on file separates a translated scale's trait from a wording factor before gating it.

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) Cronbach's alpha on each version's full answerers: 6 wrong | s.6 defines reliability, the word every analyst reads as alpha | the items ship row by row | yes, the reliability coefficient | the manual's English reliability (0.90) is one number for the source version and scores no method | no | one formula on a covariance matrix | readable |
| 1 omega from a single factor (congeneric loadings): the same 6 wrong | s.6's "due to differences ... in connectedness" invites a factor model | the items | yes, the textbook correction to alpha | none | no | a factor model, then a ratio | readable |
| 2 omega total from a model with the wording factor, or a correlated positive and negative factor model: the same 6 wrong | none names the wording factor | the keying alternates, so the two item sets are visible | partly: a model fitter sees the misfit and adds the factor, then takes all common variance | none | no | a model, then a ratio | readable |
| 2 the positively worded items alone: 4 wrong (Punjabi held; Mandarin, Tagalog, Vietnamese released) | none | the keying | yes, dropping the items that misbehave | none | no | a single factor on six items | readable |
| 3 (decisive) the trait's share with the wording factor separated (omega hierarchical from a bifactor model, or a single factor with the negatively worded items' residuals correlated) | s.6 files the quantity (variance due to connectedness) and names no coefficient or model; the manual says the twelve items formed a single factor in English, a fact of the source version | no column holds a reliability, a factor or a loading; nothing marks the six affected versions | no: the reflexes take the score's common variance as the trait (alpha, a single factor) or drop half the scale | no control scores a coefficient | no | not linear: a two-factor model per version, the general factor's loadings summed and squared over the score's model variance | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the population of s.6 | the version's valid completes who answered all twelve items | every valid complete with their answered items (pairwise covariances) | same call | s.6 ("who answered all twelve items"); same call (asserted) |
| SF2 | the item scores' association | covariances of the five-point scores | polychoric correlations of the answers | same call (every version 0.02 or more from an edge) | same call (asserted) |
| SF3 | the model separating the wording factor | bifactor: connectedness on all twelve items, a wording factor on the six negatively worded items, orthogonal | a single factor with the six items' residuals correlated; the moment estimator (positively worded items' factor, the negatively worded items' covariance with it) | same call | same call (asserted) |
| SF4 | the fitting method | maximum likelihood | unweighted least squares | same call | same call (asserted) |
| SF5 | the comparison with the bands | unrounded | at two decimals | same call: every version 0.046 or more from an edge | s.6 ("compared unrounded"); same call (asserted) |
| SF6 | "connectedness" | the attribute the scale measures, the single factor of the source version | connectedness and the wording factor together (all common variance) | the default path's answer: the wording factor read as connectedness | manual s.1 ("The BCS-12 measures connectedness") and s.4 ("the twelve items formed a single factor"); the wording factor adds nothing in the four other versions (asserted): a factor that comes with some translations is the translation's, not the attribute's |
| SF7 | the total score | the twelve item scores summed with BCS02 to BCS12 even items reversed | the raw answers summed | not a reliability of the scored total | s.5 ("the item score is 6 minus the answer") |
| SF8 | unanswered items | 9, -8 and -9 leave the item unanswered | codes read as answers | the respondent leaves the full answerers either way | s.5; codebook |
| SF9 | the bands | 0.80 or more release; 0.70 to under 0.80 hold; under 0.70 rework | edges assigned the other way | same call (no version within 0.046 of an edge) | s.6 table |
| SF10 | the unit | each version on its own pilot | versions pooled by vendor or language family | not the standard's gate | s.6 ("A version's reliability"); prompt |
| SF11 | the covariance's divisor | n - 1 | n | same call | same call (asserted) |
| SF12 | how the reliability is estimated | open: the analysis | a coefficient named by a rule | no rule names one | the standard names no coefficient or model (asserted) |
| SF13 | an online entry's date for the pilot window | the Eastern date it started | the Eastern date it ended | same: every entry starts and ends on one Eastern date (asserted) | s.4; dictionary ("Dates are Eastern dates ... unless a field says UTC") |
| SF14 | a panel member's "first" valid complete | the earliest by time | earliest by start against earliest by end | same: every later completion by the same member starts after the earlier one ends (asserted) | s.4 |

## Ladder

Four rungs, each a defensible estimate of a score's reliability, each dying to one fact of the data (figures measured
on the cut pack, asserted in `checks.py`; versions in the register's order pa, zh-Hans, yue, tl, ar, es, ur, vi, fa,
ko).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | Cronbach's alpha | 0.852, 0.866, 0.754, 0.871, 0.855, 0.880, 0.595, 0.850, 0.888, 0.857: release eight, hold Cantonese, rework Urdu: 6 wrong | a single factor fails in the six affected versions (RMSEA 0.060 to 0.182 against 0.028 or less elsewhere): the negatively worded items covary beyond connectedness |
| 1 | omega from a single factor | 0.853, 0.867, 0.751, 0.872, 0.855, 0.880, 0.597, 0.822, 0.888, 0.857: the same 6 wrong | the same misfit: the single factor absorbs the wording variance |
| 2 | omega total from the model with the wording factor; the positively worded items alone | omega total 0.856, 0.880, 0.779, 0.886, 0.866, 0.890, 0.616, 0.896, 0.897, 0.870: the same 6 wrong; positively worded items 0.759, 0.810, 0.606, 0.811, 0.775, 0.805, 0.413, 0.839, 0.824, 0.790: 4 wrong | omega total counts the wording factor's variance, which s.6 leaves out; the six positively worded items are not the twelve-item score s.6 gates |
| 3 (golden) | omega hierarchical from the bifactor model | 0.855, 0.754, 0.534, 0.747, 0.754, 0.879, 0.591, 0.543, 0.888, 0.752: release pa, es, fa; hold zh-Hans, tl, ar, ko; rework yue, ur, vi | |

- **Margins.** Every version sits 0.046 or more from a band edge on the golden (Mandarin and Arabic 0.754 against
  0.80); the correlated-residual estimate (Urdu 0.635), the moment estimator (Urdu 0.629) and polychoric correlations
  (0.545 to 0.903) keep every version in its band, each 0.02 or more from an edge (SF2 to SF4).
- **Position and dominance.** Every easy route files 4 or 6 versions wrong; only the trait's share with the wording
  factor separated lands the golden, and the decisive step alone (the wording factor separated, nothing else changed)
  moves the default path to it on the clean truth (R3b). The generating model's own trait shares put every version in
  the golden's band.
- **Grid.** The default moves 6 of 10 cells, every rung 4 or 6.
- **Worth.** Counted on the decisions, never on an intermediate; no graded figure is a reliability.

## Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | each version's valid pilot completes who answered all twelve items | TAS-4 s.4 and s.6 (SF1) |
| 2 | Unit of account | the respondent's total score | s.5, s.6 (SF7) |
| 3 | Attribution window | each version's pilot fieldwork dates in the register | s.4; register |
| 4 | As-of dating | the vendors' final files of 26 February 2027; sign-off 1 March 2027 | README |
| 5 | Version basis | TAS-4 in force from 1 September 2026; the register as kept | standard header; register |
| 6 | Denominator | the total score's variance over the population | s.6 |
| 7 | Weighting | none: unweighted pilot completes | s.6 |
| 8 | Window length | each version's own pilot dates | register |
| 9 | Boundary inclusivity | 0.80 or more release, 0.70 to under 0.80 hold, under 0.70 rework, unrounded | s.6 (SF5, SF9) |
| 10 | Rounding path | decisions on unrounded shares; the pilot mean score rounded half up to two decimals once | s.6; prompt |
| 11 | Tie-break | none: each version on its own | s.6 (SF10) |
| 12 | Maturity and censoring | every pilot closed before the files; no interview after its pilot | register; C1 |
| 13 | Order of operations | valid completes, item scores, full answerers, covariance, model, share, band | s.4 to s.6 |
| 14 | Row order | irrelevant | C1 |
| 15 | Duplicate resolution | a panel member once, at their first valid complete (merged accounts one member); a reissued case's interviews judged each on its own back-check | s.4; dictionary |
| 16 | Identity normalisation | version codes from the survey link and the register; panel members through the ledger | dictionary; codebook |
| 17 | Netting against gross | none | s.4 |
| 18 | Dimensional units | item scores 1 to 5, totals 12 to 60, shares of variance | s.5, s.6 |
| 19 | Code and status semantics | 9, -8, -9 unanswered; blank or no row not reached; status and RESULT the interview's, not the module's | codebook (SF8) |
| 20 | Integerisation | completes are integers | C1 |
| 21 | Clause scope | the ten new versions in the register | prompt; register |
| 22 | Forward window contents | none: the decisions govern the wave 6 fieldwork from 22 March | README |

## Literal reader

Executed word for word, TAS-4 and the prompt fix the candidates (the register's ten versions), the population (s.4's
valid completes: 18 or older, within the version's pilot dates, the end of the BCS-12 module reached in that version,
a panel member once at their first valid complete, an interview the back-check reports not confirmed left out; s.6's
full answerers among them), the outcome (s.5's total score), the quantity (s.6: the share of the score's variance due
to differences between those respondents in connectedness) and the bands. Executed, s.6 leaves one question for the
analysis: how much of each version's score variance is connectedness, which no file states. Alpha and a single factor
answer it with all the items' common variance; in six versions the six negatively worded items share variance among
themselves that a single factor cannot carry (a wording factor adds nothing in the other four), and the manual records connectedness as the
source version's single factor, so the trait's share is the general factor's share with that wording factor
separated. Every estimator of that share (bifactor, correlated residuals, moments, polychoric) gives the same ten
decisions; every reading of a term in the fork table gives the same call or violates a quoted sentence. The asks
execute s.4 and s.5; the difficulty there is how each vendor's records come to exist, not the words.

## Oracles

- No control, published figure or certified reliability ships for a new version: nothing reports a version's
  reliability, alpha, loading, factor or decision, and no field marks a version as affected.
- The technical manual's English reliability (the source version's validation sample) is one figure for a different
  version; it scores no method and ties under every one.
- Wave 5 results by region for the English and French versions, and Nesscroft Panels' paradata (distractors, named in
  `metadata.json`): neither carries a new version's answers; the wave 5 means (43 to 45) are another population and
  another mode, and the paradata's durations are not in the standard.
- The translation register is process history (translators, review dates, pilot dates, notes on single items); its
  notes on negatively worded items sit in versions with no wording factor (asserted).

## Ask sheet

Two asks, 20 figures, decoupled from the call: the call reads each version's full answerers' item covariances; the
asks read every valid complete (count) and their total scores (mean), through how each vendor's records come to exist.

**Main population:** the call's population is the valid completes who answered all twelve items; the ask devices'
handling leaves every decision where it is (each stop and the cracker's population, asserted R2): the call is
mess-neutral, never pristine. The partials past the module and the replacement interviews are valid completes and sit
in the call's population; dropping them moves no decision.

| Ask | Figures | H18 home | Use | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: each version's valid pilot completes | 10 | the audit trail of the decision: the pilot each decision stands on, which s.6 tells the quality lead to report | the sign-off's table | D5, the population a blanket exclusion destroys: the vendors' status describes the questionnaire (online status complete or partial, CAPI RESULT 1 or 2), s.4 the module; respondents who reached the end of the BCS-12 module and left in the background questions are valid completes the status filter drops. CAPI also D7, the true key elsewhere: Fernlow keys interviews by sample case, a case whose interview the back-check did not confirm is reissued to another interviewer, and the back-check log names the case and the checked interviewer, so a join on the case drops the replacement too | NCP retakes under fresh entry ids, some from second accounts merged afterwards (the ledger); soft-launch entries the evening before the pilot, dated the first day in UTC; switchers to English; partials inside the module; screen-outs; FLR pretest interviews; unconfirmed interviews; unreached back-checks kept | export (status, start_utc, ui_language_at_end, age, BCS01 to BCS12), ledger (panel_member_id, respondent_id, outcome, merged_into), CAPI long (case_id, interviewer_id, interview_date, variable, value), back-check log (case_id, interviewer_id, outcome), register (pilot_start, pilot_end), codebook, TAS-4 s.4, dictionary: 8 files, 15 columns | status filter (every version 7 to 18 low); back-check joined by case (CAPI 11 to 17 low); merged accounts apart (online 3 to 5 high); UTC dates (online 2 to 7 high); no online window (11 to 15 high); retakes (16 to 23 high); switchers (10 to 13 high); partials inside the module (9 to 26 high); pretest (33 to 41 high); unconfirmed (16 to 20 high); unreached dropped (31 to 35 low); the answer |
| B: each version's pilot mean score, two decimals | 10 | a measure every version carries that the decision does not turn on | the sign-off's table | the same population devices: the partials past the module are less connected, the replacements are new respondents | prorating one or two unanswered items; codes 9, -8, -9 read as answers | as A, plus TAS-4 s.5 and the codebook's codes | status filter (every version 0.01 to 0.20 off); back-check by case (CAPI 0.03 to 0.12 off); no prorating (0.26 to 0.75 high); codes as answers (every version 0.01 to 0.34 off); retakes, switchers, pretest, unconfirmed (0.01 to 0.26 off where they move); the answer |

- **Span:** eight files and 15 columns across the asks. The status device moves both asks in every version; the case
  device both asks in every CAPI version; the merged accounts A in every online version.
- **Shared hazards:** the status filter (A 7 to 18 low, B 0.01 to 0.20, every version); the case join (A 11 to 17 low,
  B 0.03 to 0.12, every CAPI version); the soft launch read in UTC (A 2 to 7 high, online).
- **Realism:** online panels mark an entry complete only on the questionnaire's last page; CAPI interviews carry the
  interviewer's outcome code; face-to-face vendors key interviews by sample case and reissue a case whose interview a
  back-check could not confirm; panels merge second accounts and move their points; vendors soft-launch links the
  evening before an agreed start.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A valid completes (10) | executes s.4 through the ledger, the window in Eastern time and the back-check log; its status filter keeps complete and RESULT 1 only, dropping every partial past the module (every version 7 to 18 low), and its back-check join on the log's key drops each reissued case's replacement (CAPI 11 to 17 low) | misses the same way | miss |
| B pilot mean score (10) | the same population, scored right: every version 0.01 to 0.20 off at two decimals | misses the same way | miss |

- **Cracker keeps:** under 0.05 of the ask figures (every figure turns on the status device; the CAPI rows on the case
  device too). The chart's parts sit on the call (the bands and the decisions), about a fifth of the ask weight if the
  generated rubric files them there. A solver that reads s.4's module end against the item columns and joins the
  back-check on case and interviewer lands both asks; the merged accounts and the soft launch remain on its path.
- Mirror leakage: 10 per cent of ask weight (the chart's frame and bands; the mirror's ask path is the cracker's).
- Pair ceiling: 38.7 (C = 38 + 7 + 55 x 0.20 = 56.0 with the chart's parts kept; S = 10 + 7 + 55 x 0.08 = 21.4, the
  mirror's four right decisions counted in r = 10; mean 38.7).

## Pre-ship check

1. Domain: the call stands on each version's share of total-score variance due to connectedness (omega hierarchical)
   under the measurement model its pilot data support, the six negatively worded items' wording factor separated;
   Cronbach's alpha and a one-factor omega release eight versions (6 of 10 wrong), omega total from the wording model
   files the same 6, the positively worded items alone 4. With meters or wards for items there are no negatively worded
   statements, no translation that changes how negation is answered and no latent trait to separate from a response
   style.
2. Two layers: Layer 1 (two vendors' layouts, missing codes by vendor, retakes and merged panel accounts, screen-outs,
   partials and soft-launch entries, switchers, pretest interviews, unconfirmed interviews and their reissued cases,
   respondents who left after the module) is neutral on the call, each item asserted (R2); Layer 2 is the trait's share
   with the wording factor separated, asserted alone to move the default path to the golden on the clean truth (R3b).
3. No banned stump decides: nothing is planted (no memo, draft, earlier report or figure states a reliability or a
   decision); not semantics (the default path reads every field right and files 6 wrong on the clean truth, R3a); not
   rule application (s.6 files the quantity, the population and the bands and names no coefficient or model, asserted on
   the standard's text).
4. Gate G: no shipped artifact ranks, scores or decides a version on reliability; the two distractors carry no new
   version's answers.
5. Determinism: the list grades each version's decision, valid pilot completes and pilot mean score; the decisions are
   the same under every estimator of the trait's share (bifactor, correlated residuals, moments, polychoric, unweighted
   least squares), every version 0.046 or more from a band edge on the golden; every mean 0.0015 or more from a
   two-decimal rounding edge; counts are integers. Judge pass r1 (the first build): DETERMINISTIC, APPROVE; Gate G
   method_or_model_selection, analytical, no surface read, not a sole data defect; Gate H domain pass, layers pass,
   decisive step analytical; stump power good; its one optional note (block 4's chart line described a wording-factor
   marking the prompt never asks for) was trimmed. Pass r2 (after the first realism fixes): DETERMINISTIC, APPROVE, the
   same gates; its two cosmetic notes: the prompt's "send back for retranslation" against the standard's "Rework" (the
   prompt now says "rework for retranslation") and the CSV's row order (the register's, ungraded). Pass r3 on the final
   build: DETERMINISTIC, APPROVE, the same gates (`determinism_check_report.md`); its open point (Urdu's single factor
   borderline on the absolute test, p 0.049) led critical component 1 and step 5 to state the wording factor's absence
   in the four versions (the factor test, p 0.37 to 0.71) rather than a single factor's fit.
6. Asks: A is moved in every version by the vendors' status against the module's end (7 to 18 low) and in every CAPI
   version by the back-check joined on the case (11 to 17 low); B in every version by the same (0.01 to 0.20 off at two
   decimals); no stop moves a decision (asserted).
7. Input gates: 12 files in four formats (csv, md, pdf, xlsx), the CAPI long file at 39,298 rows, two distractors
   named in metadata.json; 113 generator checks with the realism sweep; the verifier (its own valid-complete rules and
   its own bifactor fit) green; two builds byte-identical; figures_check 44 of 44; containers clean.
8. Duplicate guard: `guard.py heart` PASS (nearest 0.08, task181 and task135); `guard.py surface` promoted task236,
   task235, task234 and task233 (the same author's Data Quality builds: a README file name and the designation-set
   decision type, nothing in mechanism), for the author's adjudicated read.

## Leak check

leak.py REVIEW, no LEAK (--asof 2027-03-01), after the first run's two incidental lines were cleared (a golden count,
450, inside the manual's English sample size, now 2,416; a paradata column named device, now platform). Remaining
REVIEW lines, all harmless: the bands 0.80 and 0.70 sit in TAS-4's table (the filed comparison); the dictionary, the
readme, the manual and the standard carry the domain's own words (translation, reliability, connectedness, negatively
worded items, the English sample's single factor) without naming a wording factor or a coefficient.

Reader pass 1: Q1 none ("No sentence tells you HOW to estimate reliability"); Q2 none; Q3 none clearly, the incentive
ledger read as a possible solving aid for its merged rows (fixed: the readme and dictionary say it came with the panel's
invoice, the centre paying incentives at cost); Q4 none; Q5 s.4 to s.6 executed literally leave the estimator open (the
analysis); Q6 an analytical choice. On the asks it read the reissued cases' back-check join and the merged accounts as
settled by the dictionary, and the online partials that finished the module as "not clearly settled" (s.4 counts an
interview that "reached the end of the BCS-12 module", and the codebook's Questionnaire sheet puts the background
questions after it: settled by a literal reading, kept as the ask's device). Realism: online ages started at 21 and
piled at 89 and 92 (fixed: a smooth age distribution, online mean 45.9, 18 to 85); the versions' means sat close
together (fixed: each translation's own level of agreement, means 36.89 to 41.76); the standard defines reliability without naming a
coefficient (harmless: it files the quantity as classical reliability theory defines it, and naming a coefficient
would file the HOW); the reissued cases looked concentrated on one interviewer (checked: spread over six to nine
interviewers per version).

Reader pass 2 (after those fixes): Q1 none ("Nothing else tells you HOW"); Q2 none; Q3 none strictly (the incentive
ledger "a panel vendor would send ... with its invoice ... plausible"); Q4 none; Q5 the estimator left open; Q6 an
analytical choice. On the asks: the partials that finished the module count "literally" under s.4, though it called
RESULT against item presence open (kept: s.4's module end decides, read literally, and is the ask's device); a panel
member's first valid complete by start or by end time "partly open" (closed: every later completion by the same member
starts after the earlier one ends, SF14 asserted); the 400 minimum (every version has 450 or more valid completes).
Realism: online ages flat within bands (fixed: a smooth age distribution, 18 to 85, mean 45.9); a 2,400-second cap on
durations (fixed: entries over 40 minutes are timed out and redrawn); every case with two interviews a reissue after a
failed back-check, "a clean 55 of 55" (fixed: 22 of the 80 such cases are revisits after a break-off inside the module,
58 reissues); the dictionary's merge sentence mildly a hint (kept: it closes who a panel member is, SF table); fixed
points per outcome (kept: a panel pays a set incentive per outcome). The prompt's one change after pass 2 ("rework for
retranslation") passed leak.py's prompt gate and the voice check; no document changed, so no third read.

## Tried and rejected

- The seed's alpha against congeneric omega as the stump: with the bands at 0.70 and 0.80, unequal loadings move alpha
  under omega by 0.01 to 0.03, so the golden would sit within a rounding of a band edge, and a one-factor omega is a
  textbook reflex; it stays as a lower rung.
- Conditional measurement precision at a screening cut-off (graded response model per version): the decisive estimate
  needs an item response model the judge's sandbox cannot fit, and the scale is not used to screen.
- Reliability carried from each pilot sample to its language community's population (range restriction): the pilot
  cannot supply the population's variance, and population_selection is banned against task264.
- An eight-and-four keying (items 9 to 12 negatively worded) with five affected versions: the margins between the
  trait's share and alpha were thin, and unequal loadings within the four items moved alpha against omega near the
  edges; the six-and-six alternating keying the manual describes gives clean margins.
- Unconfirmed interviews as flat "agree" answers: they moved the Punjabi and Arabic decisions when counted (a Layer 1
  item deciding the call); regenerated as near-copies of the same interviewer's own interview, which leave every
  decision in place.
- Asks whose devices were all adjudicated by s.4's own clauses (retakes, switchers, partials, pretest, unconfirmed):
  a careful solver executes each clause and lands both asks; the asks now turn on how the records come to exist (the
  vendors' status against the module's end, the case key against the checked interviewer, merged accounts), with the
  clause-level items kept as hazards.
- The pilot mean score to one decimal: the population devices moved it by 0.01 to 0.19, inside one rounding for most
  versions; two decimals, the precision a pilot report gives a scale mean, makes every device a miss.
