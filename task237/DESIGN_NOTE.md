# task237 design note

Architecture 1, wave 3, seed DQ10 (whether a translated questionnaire passes the release gate on reliability): the
seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Psychology &
Behavioral Science, psychometric measurement and scale validation, Data Quality Monitoring & Alerting. The Survey
Research Centre at Marlowe University runs a province's Community Connections Survey, whose core measure is the
twelve-item Belonging and Connection Scale (BCS-12: eight positively worded statements, four negatively worded ones,
answered on a five-point agreement scale). For wave 6 the centre translated the BCS-12 into ten more languages and
piloted each version with two fieldwork vendors. Its translation and adaptation standard gates every new version on
the reliability of its total score in the pilot: released for the wave's fieldwork at 0.80 or more, held for
cognitive interviews and a second pilot from 0.70, sent back for retranslation below 0.70. The standard defines the
reliability as the share of the total score's variance across the pilot's respondents that is due to differences in
their connectedness. The translation quality lead signs off the ten decisions before the wave 6 fieldwork launches.

## Draw

Card `cards/task237.json` (architecture 1, registered 2026-10-17). Guard verdict PASS (the third persona redrawn from
the en_CA pool after two first names met older builds).

- **Pairing.** Psychology & Behavioral Science / psychometric-measurement-scale-validation, serving Data Quality
  Monitoring & Alerting (the domain index lists this task type under DD and DQ). Never built before on this objective;
  not banned against the last three builds (task236, task264, task156). The object is the quality of each language
  version's data as a measure (whether its scores measure connectedness reliably enough to field), the call a release
  gate. task257 (a psychometric DD build) counts dimensions under lopsided splits; nothing here repeats it.
- **Niche.** Reverse-keyed items behave differently across translations: where a language renders negation in a way
  respondents answer by its form rather than its content, the four negatively worded items take on a shared wording
  factor of their own. That variance is consistent across items, so it raises the items' agreement, and it is not
  connectedness.
- **The call.** For each of the ten new language versions: release for the wave 6 fieldwork, hold for a second pilot,
  or rework (retranslate).
- **Shape.** 07, a grid of cells: ten versions, each with its decision and the per-version figures the asks owe.
  Decision designation_set, answer set_of_items, question form what.
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
- **Deliverables.** `bcs12_wave6_release_decisions.csv` (one row per version: the decision and the asks' figures) and
  `bcs12_wave6_release_chart.png` (each version against the release bands).
- **Data-native sentence.** In five of the ten translations the four negatively worded items share variance with each
  other that they do not share with the eight positively worded ones, so the items' average agreement (alpha) and a
  one-factor model both count that wording variance as connectedness; the standard's quantity is the trait's share of
  the score, which only a model giving the negatively worded items their own wording factor recovers.

Sources, one line each (what it teaches; how this build differs):
- Psychometric practice on reverse-keyed method effects (bifactor and correlated-uniqueness models, omega
  hierarchical): negatively worded items often form a method factor, stronger in some languages and samples; here
  it is the decisive structure of a translation gate, not a validation study's finding.
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
   due to differences in connectedness) in the pilot against the bands 0.80 and 0.70.
2. Build each version's valid pilot completes from the two vendors' files, reverse-score items 9 to 12 and form the
   total score.
3. Estimate each version's reliability with Cronbach's alpha (or omega from a one-factor model) and apply the bands.

Ends on: 5 of the 10 versions wrong (the Mandarin, Tagalog and Korean versions released and the Vietnamese version
released, the Cantonese version held, where the trait's share puts the first three on hold and the last two to
rework).

Golden: release the Punjabi, Spanish and Persian versions; hold the Mandarin, Tagalog, Korean and Arabic versions;
rework the Cantonese, Vietnamese and Urdu versions (to be confirmed on the tuned simulator).

## Stump sentence

A competent solver gates each version on Cronbach's alpha or a one-factor omega and files 5 of the 10 versions wrong
(Ends on: the Mandarin, Tagalog, Korean and Vietnamese versions released and the Cantonese version held); the step
that lands it there is taking the score's whole common variance for connectedness when, in those five translations,
the negatively worded items share a wording factor that the standard's quantity leaves out.

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
- **Layer 1:** two vendors' layouts (a wide online panel export and a long interviewer-administered file); missing
  answer codes that differ by vendor; panel retakes under fresh respondent ids; screen-outs and partials kept in the
  panel export; interviews that failed the vendor's back-check listed in a separate quality-control file. Each is how
  the system that writes it behaves; none is placed to be caught.
- **Layer 2:** field_method, the trait's share of the score under the measurement model the data supports: alpha, a
  one-factor omega and a two-factor omega that counts all common variance each mismeasure it where a wording factor is
  present.
- **Decisive step:** modelling each version's item responses with a wording factor on the negatively worded items
  (or their correlated residuals) where the data show one, and taking the trait's share of the total score's variance
  from that model rather than the items' whole common variance.
- **Not semantics:** the default path reads every field, code and rule right (valid completes built, items reversed,
  the standard's definition of reliability read correctly) and still files 5 of the 10 versions wrong; what it gets
  wrong is the measurement model, which no field states.
- **Not rule application:** the standard files the quantity (the trait's share of the score's variance), the
  population (the pilot's valid completes who answered every item) and the bands; no rule names a coefficient or a
  model, and executing every stated rule still leaves the estimation.
- **Analyst test:** a strong analyst who builds the valid completes, reverses items 9 to 12, reads the standard's
  definition correctly and estimates it with Cronbach's alpha or a one-factor omega files 5 of the 10 versions wrong
  (Ends on: the Mandarin, Tagalog, Korean and Vietnamese versions released and the Cantonese version held).
- **Estimand:** the standard (in the pack) fixes the population (each version's valid pilot completes who answered all
  twelve items), the outcome (the total score as scored), the quantity (the share of its variance due to differences in
  connectedness) and the comparison (the bands at 0.80 and 0.70).
- **No decoy:** nothing is planted: no memo, earlier report, vendor summary or figure states a version's reliability
  or a decision; the translation register records the translation process only.
- **No certified replay:** no certified or published reliability for a new version exists for a method to reproduce.
- **Lesson:** a composite's agreement is not its target attribute's share when a subset of its parts shares a second
  source; no build on file separates a translated scale's trait from a wording factor before gating it.

## Tried and rejected

- The seed's alpha against congeneric omega as the stump: with the bands at 0.70 and 0.80, unequal loadings move alpha
  under omega by 0.01 to 0.03, so the golden would sit within a rounding of a band edge, and a one-factor omega is a
  textbook reflex; it stays as a lower rung.
- Conditional measurement precision at a screening cut-off (graded response model per version): the decisive estimate
  needs an item response model the judge's sandbox cannot fit, and the scale is not used to screen.
- Reliability carried from each pilot sample to its language community's population (range restriction): the pilot
  cannot supply the population's variance, and population_selection is banned against task264.
