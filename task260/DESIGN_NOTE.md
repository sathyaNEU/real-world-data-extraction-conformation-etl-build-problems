# task260 design note

Merrowdale Breast Screening Service: which AI reading-support tool to license for 2027, from three reader studies.

## Draw

- **Card:** `cards/task260.json`, registered 2026-10-15. Biomedical & Clinical Research, task type
  medical-imaging-reader-study-evaluation (how accurately film readers read screening mammograms with and without an AI
  tool, and whether the difference holds for the service's readers and examinations), objective Descriptive &
  Distribution Analysis; shape 01 (three tools on one score, the gain, behind a gate, the interval above zero, with a
  cap of one adoption); decision pick_one_of_n (one tool, or unaided reading kept); gap population (what the interval
  speaks for: the service's film readers and screening examinations, not the panel and the study set); pattern none,
  G16 then G17; Gate G signal_vs_noise_or_hold; strategy uncertainty_hold.
- **World:** Merrowdale Breast Screening Service, a fictional breast screening service in England, invites women aged
  50 to 71 every three years and reads about 45,000 screening studies a year at four static sites and three mobile
  units, with 26 film readers (consultant radiologists, consultant and advanced practitioner radiographers, breast
  clinicians) double reading every examination. In 2026 it ran one reader study per AI reading-support tool on
  ReadPoint, a fictional reader-study platform: Velmora Detect (February and March), Quintara Mammo (April to June) and
  Ardelle Breast (July to September). In each study ten of the service's film readers (the panels overlap) read the
  same 300 examinations from the service's 2019 to 2022 archive (75 histology-confirmed cancers, screen-detected or
  interval, and 225 examinations normal at the next round) twice, unaided and with the tool, at least four weeks
  apart, half the panel aided first; each reading records a probability of malignancy (0 to 100) and a recall
  decision. The service's AI evaluation panel (forum committee_or_panel) picks one tool for a two-year licence from 1
  April 2027 (forcing event purchase_order_or_contract) under its evaluation protocol: the largest gain in the
  readers' average area under the empirical ROC curve among tools whose two-sided 95 per cent interval lies above zero
  for the service's film readers reading its screening examinations, else unaided double reading stays.
- **People** (guard.py names --geo UK --seed 260; Laura Atkinson skipped for a first name used in task255): Hayley
  Kelly, the service's clinical director, who chairs the evaluation panel; Darren Jenkins, AI evaluation lead (role
  family procurement_lead), who owns the protocol; Eileen Walton, research radiographer, who ran the three studies;
  Gary Pritchard, procurement manager; Leonard Hilton (Quintara), Jemma Barnes (Ardelle) and Kim Summers (Velmora),
  the vendors' account managers.
- **Data-native sentence:** each study is fully crossed, so every reader's gain is measured on one shared set of 300
  examinations and every examination's effect is measured through one shared panel of ten; Quintara's gain swings from
  reader to reader (some readers lean on its prompts and gain a lot, others read worse with it) and Velmora's sits in
  the examinations its own case score moves for every reader (readers defer heavily to a score weaker than their own
  reads), so an interval that resamples only the examinations admits Quintara and one that resamples only the readers
  admits Velmora, and only an interval carrying both (Obuchowski-Rockette or DBM) leaves Ardelle's smaller, steady gain
  as the one that holds.
- **Guard:** WARN overuse.shape (01 in 3 of the last 12, never in the last two): the call ranks three tools on one
  score behind a gate with one adoption, a ranked list under a cap of one, and no other shape carries a pick behind a
  statistical gate. WARN repeat.question_form (which, against task458): the call is a pick among three tools or none,
  and a pick asks which (guide-to-prompt 3). Gate G was redrawn from method_or_model_selection (the signature
  population, G16, method_or_model_selection is spent in task134 v1, task104, task501 and task70) to
  signal_vs_noise_or_hold, which is what carries the stump: each tool's gain judged against the noise of the right
  populations. Context artifact redrawn from filed_standard (task257) to operations_log (the ReadPoint exports carry
  the call). Nearest driver 0.05 (task255, lineage).
- **Pairing and shape:** the field's own analysis decides (multi-reader multi-case ROC analysis of a fully crossed
  reader study against a histology-confirmed reference standard), the objective is how reader accuracy and its gain are
  distributed over readers and examinations (the client taxonomy files reader-study evaluation under Descriptive &
  Distribution Analysis), and the call is a pick among three behind a gate (shape 01). Criteria: the call, each tool's
  gain and verdict, the reason each excluded tool fails, each tool's count of readers who did better with it, the
  asks' per-site and per-tool figures, and the chart's parts.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution`: task253 shrank small noisy
  unit averages (one random factor, a count below a line), task257 counted dimensions on latent correlations, task255,
  task256, task258 and task259 spent tails, conditional distributions, threshold crossings and carried levels; none
  builds an interval over two crossed random factors. `guard.py mechanisms --gate-g signal_vs_noise_or_hold`: task186
  tests each unit's change against noise that carries a cycle shared within a place (one shared component left out of
  a within-unit test) and task128 reads a contact's effect where queues outran the team; this build crosses two random
  factors and each one-factor interval admits a different tool. The client's reader-study pattern 1 (readers and cases
  both random; shortcut pooled ROC and DeLong) gives the family; this build's own version is the three-way split, in
  which the smallest gain is the only one that holds. The client's exemplars carry no reader study.
- **Seed:** DA10 (a credit-union association's 60 merger-readiness engagements shared among leagues by projected small
  credit-union exits) gave the lane's number only: its quantity is a projected exit count shared by a stated rule, a
  forecast the Descriptive lane does not own, and its natural step (a credit union's size class now against when the
  panel first saw it) reads as the size definition once the estimand is filed, so it would be semantics; the world is
  redrawn, as task255 to task257 redrew theirs.
- **Forward facing:** the call picks the tool the service's readers use in 2027 and 2028, a window not yet open; the
  deciding quantity is each tool's gain for the service's readers and examinations, estimated from the 2026 studies.

## Default path

1. Stack the three studies' ReadPoint exports (the third in the platform's newer layout), keep each reading's final
   revision, drop the practice cases at the start of each session, and join each study's case list for the reference
   standard (cancer or normal).
2. For each reader and condition, compute the area under the empirical ROC curve of the probability-of-malignancy
   ratings (Mann-Whitney, ties counted half).
3. Each tool's gain is the panel's average aided area minus its average unaided area.
4. For each tool's 95 per cent interval, bootstrap the study's 300 examinations (cancers and normals resampled
   separately, the ten readers kept as they are) and take the 2.5th and 97.5th percentiles of the gain; DeLong's test
   on the readers' average area gives the same verdicts.
5. Keep the tools whose interval lies above zero (Quintara and Ardelle; Velmora's crosses zero) and adopt the one with
   the larger gain.

Ends on: Quintara Mammo (the largest gain whose interval clears zero with the panel held fixed, about 0.045 against Ardelle's 0.028)
Golden: Ardelle Breast (the only tool whose interval stays above zero once readers and examinations are both treated as samples of the service's; Quintara's and Velmora's cross zero)

## Stump sentence

The default path bootstraps each study's examinations with its ten readers held fixed and files Quintara Mammo, whose
interval clears zero and whose gain is the largest that does; the step that lands it there is treating the panel as
the only readers the decision is about, when the protocol's interval is for the service's film readers reading its
screening examinations and Quintara's gain swings from reader to reader, so only an interval that carries both
readers and examinations as samples (Obuchowski-Rockette or DBM) shows that Ardelle Breast's smaller, steady gain is
the one that holds; the opposite one-factor interval (a paired t-test across the readers) files Velmora Detect.

## Three rules

Task type: medical-imaging-reader-study-evaluation (Biomedical & Clinical Research), which serves Descriptive & Distribution Analysis in the client taxonomy.
Domain test: The deciding quantity is each tool's gain in the readers' average area under the empirical ROC curve of their malignancy ratings against a histology-confirmed reference standard, judged by its multi-reader multi-case interval (Obuchowski-Rockette or DBM, readers and examinations both random), the reader-study field's own analysis of a fully crossed design.
Swap: "Which of three grading apps should a school district adopt, by the gain in its teachers' average marking accuracy whose interval clears zero?" keeps a pick and an interval but loses the ROC area of each reader's malignancy ratings against histology, the enriched cancer set and the fully crossed reader-by-examination design the interval is built on, so the task no longer reads the same.
Layer 1: ReadPoint's export layout changing between platform versions (renamed columns, the probability as a fraction, the recall decision in words), resubmitted readings exported beside the final revision, practice cases at the start of every session outside the study set, per-study pseudonymous reader ids and UTC timestamps on the call's path; on the asks' path the imaging system's migration and its parallel run, mobile units recorded under their own codes and re-hosted mid-year, and technical repeats recorded as separate studies of one screening episode; each is what these systems produce and none is placed to be caught.
Layer 2: field_method, the reader-study field's own method: each study is fully crossed, so every reader's gain is measured on one shared set of examinations and every examination's effect through one shared panel, and an interval speaks for the service's readers and examinations only when it carries both reader and examination sampling (Obuchowski-Rockette or DBM).
Decisive step: Judging each tool's gain with an interval that treats the ten panel readers and the 300 study examinations both as random samples of the service's film readers and screening examinations (Obuchowski-Rockette or DBM), because Quintara's gain varies from reader to reader and Velmora's sits in the examinations its score moves for every reader, and each looks precise when only the other factor is resampled.
Not semantics: Every export, case list and protocol clause read correctly still leaves the analyst building an interval, and the bootstrap over examinations with the panel fixed, DeLong's test, or a paired t-test across the readers are each a correct reading of every field; no field, code or definition says how the interval is built.
Not rule application: The protocol states the outcome, the comparison, the populations and the 95 per cent level and leaves the interval's construction to the analyst; executing every stated rule with either one-factor interval files Quintara or Velmora, and no filed rule decomposes the gain's variance into its reader and examination parts.
Analyst test: A strong analyst who cleans the exports and reads every rule correctly computes each reader's area with and without each tool, bootstraps the examinations with the readers held fixed, and files Quintara Mammo, the default path's answer (executed on the generator's clean ratings in checks.py); a paired t-test across the readers instead files Velmora Detect.
Estimand: The gain in the readers' average area under the empirical ROC curve of their probability-of-malignancy ratings, aided minus unaided, with its two-sided 95 per cent interval, for the service's film readers reading the service's screening examinations; adopt the largest gain whose interval lies wholly above zero, else keep unaided double reading (ai_evaluation_protocol_v2.pdf, sections 3 and 4).
No decoy: Nothing is planted: no vendor, study or interim report states a gain, an interval or a verdict, the vendors' product summaries carry standalone accuracy on their own datasets (another quantity), and no record is copied, withheld or written to carry the wrong answer.
No certified replay: No certified or published result exists for a method to reproduce; the verdicts are forced by the ratings' own structure, where every interval with readers and examinations both random (Obuchowski-Rockette with jackknife or DeLong covariances, DBM, a two-way bootstrap) admits Ardelle alone.
Lesson: A fully crossed reader study measures every reader on the same examinations, so an interval that resamples one factor treats the other's variation as fixed and admits whichever tool's gain that factor carries; the field's multi-reader multi-case analysis carries both, and no build on file teaches two crossed random factors (task186 adds one shared within-place cycle, task253 shrinks noisy unit averages).

## Tried and rejected

- One fully crossed study of four conditions (unaided and the three tools) on the same readers and examinations,
  rejected at the draw: the textbook Obuchowski-Rockette or DBM analysis of four conditions pools the variance
  components across them, so every pairwise interval has one width and the largest gain qualifies first; a pooled
  analysis could never pick the smallest gain, and the design forked between pooled and pairwise analyses. Each tool
  now has its own two-condition study, as a sequential procurement runs them, so no pooling exists.
- Velmora's lift drawn as a mixture of lifted and lowered cancers, rejected in the prototype: lowering a visible cancer
  costs more area than lifting a subtle one gains, so the net gain went negative across seeds; replaced by readers
  deferring heavily to Velmora's own case score, which is weaker than their own reads.
- Panels of 18 and 12 readers, rejected in the prototype: a gain that fails a test across readers needs a reader
  spread near 0.1 in area with 18 readers; ten readers, the protocol's panel size, needs about 0.08.
