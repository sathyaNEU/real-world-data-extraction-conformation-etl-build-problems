# task119: the region's one external mortality review, realising analytical_tasks note AD01

Source note: `analytical_tasks/02_anomaly_detection/AD01_mortality-review-transfer-chain-origin.md`. This build is the
note's first realisation and keeps its decision, mechanism and world except where the guard or the skills forced a
change (listed below). Stage 1 (draw) only: the ladder, the closure table, the ask sheet and the prompt come at stage 2.

```
DRAW  (independent draws, checked with ../.claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? pending batch registration
      (scratch card: <scratchpad>/cards/task119.json)          Verdict: WARN
  Shape: other   (8 trusts x 4 operational figures = 32, 4 constructions x 2 back-test figures = 8,
                  the trust, its excess, the runner-up and the margin = 4, 5 named chart parts, 3 files:
                  about 52 criteria; not 01, because nothing is ranked under a cap)
  Gate G mechanism: decomposition_attribution, with method_or_model_selection support
  Gap: population (Gap 2: a spell is a row, the unit is a pathway of spells), then rule (Gap 4)
  Pattern: B (the national retry log pins the chain construction); strategy S7 (every screen is right
           and the answer is what nothing flags)
  Domain: Policy & Education (policy-education)   Subdomain (enumerated): public-administration
  Objective: Anomaly Detection & Diagnostics (anomaly-detection)
  Pairing repeated from last build? no (task116 is product-analytics x opportunity-sizing-decision;
           this pairing was last built as task25)
  Stakeholder role: head of quality surveillance at a regional health board (compliance_or_audit)
  Context-artifact type: published_series (the national mortality indicator publication: each trust's
           monthly indicator with its funnel banding and four contextual series, 36 months)
  Calibration form: retry_or_revision_log (national rapid-review retry log from the four neighbouring
           regions: 34 reviews closed 2021 to 2025, 47 attempts, each with its confirmed avoidable deaths)
  Decision type: pick_one_of_n (named_option)   Scoring unit: per resolved case (a confirmed avoidable death)
  Decisive mechanism: spells linked across trusts on the regional patient key wherever an emergency
           admission follows a discharge elsewhere within hours, each chain's death credited to the trust
           where the chain began and set against the first spell's modelled risk, remit segment only,
           latest four quarters (generators G2 grain, G16 method selection, G6 composition at the decoys)
  Repeats from prior builds: none on a banned axis; geography England repeats task116 (WARN, answered);
           (population, B, decomposition_attribution) repeats task44 v1 and task64 v1 lineage (differentiated)
  Forum: committee_or_panel (the board's quality committee)   Forcing event: audit_or_inspection (the
           engagement's fieldwork opens 1 April 2027)   Org family: hospital_or_health_provider
  Spine (planned): apc_episodes_region_202307_202606.parquet, one consultant episode inside one admitted
           spell at one of eight trusts, patient x spell x episode, about 900,000 rows, synthetic
  World: United Kingdom, England, a fictional NHS region of eight acute trusts (labelled A to H as in the
           note until stage 2 names them); GBP; invented names carried from the note: Kellow Bridge,
           Sandmere, Fenwold (trusts in the neighbouring regions' retry log)
  People (guard.py names --geo "United Kingdom, England" --seed 119, locale en_GB):
           Andrea Davey, head of quality surveillance (the requester)
           Norman Scott, chair of the quality committee (the funnel belief)
           Howard Singh, regional clinical lead for acute medicine (the weekend belief, social layer only)
           Diana Smith, information manager (the regional extract and its dictionary)
           Sharon Banks, national rapid-review programme coordinator (the retry log)
           Benjamin Davies, lead reviewer at the external review provider
  Deliverables (planned): external_mortality_review_2027-28.docx (the committee paper that commits),
           review_allocation_workings.xlsx (the workings and the ask sheets),
           review_allocation_by_trust.png (the visual)
  Opening move (planned): question-first
  Committed call: the one acute trust whose non-elective adult medical care the review team examines in
           2027-28. Forward facing (a window that has not opened) but not a forecast: the decisive
           practice runs steadily through all 36 months, so the latest four quarters stand for the
           engagement year and the tag stays Anomaly Detection.
  Windows: 36 months to 30 June 2026; latest four quarters July 2025 to June 2026; extract taken
           14 August 2026 (45 days after the last discharge; death registration lags at most 14 days).
  As-of date: 2026-10-02
```

Similarity claim: no prior build is a which-of-N placement decided by linking one key's records across units into
paths and crediting each path's outcome to the unit where it began, because the nearest by insight, task72 v2, credits
transferred participants to their origin subaward under a filed clause on a dated, visible change of hands, and task48
v2 recovers a population its monitor cannot see at a two-sided pair grain, while here no clause states the crediting, no
field marks a transfer and the paths exist only after a self-join on the patient key at a hand-over gap.

## Stump sentence

A competent solver rebuilds the funnel on the remit's non-elective adult medical spells, removes the palliative and
hospice-unit spells, runs a risk-adjusted CUSUM over the latest twelve months, back-tests it at 23 of the 34 closed rapid
reviews, treats the misses as review noise and sends the engagement to the trust running the weekend stroke diversion
(C); the step that lands it there is crediting every death to the trust of the patient's last spell, the indicator's own
convention and the episode file's grain, so it never self-joins spells across trusts on the patient key and never sees
that the deaths the late-transferring district general hospital (E) exports to four receivers belong to the chains it
begins.

## Decisive rung

Measured trap #2, counts file rows instead of the real unit (`_measured.md`: decided 11 of 64 client tasks, 7 of them
under 0.50, established), gated by #1, reports a failed back-test, ships anyway (11 of 64, 9 under 0.50). The unit the
remit scores ("the avoidable deaths its reviewers confirm in the reviewed trust's care") is a pathway of spells that
began at the trust, which no file stores; it is built by linking rows, and only that construction reproduces the
published control set (34 of 34 retry-log reviews), while the obvious trust-level screens reproduce most but not all
(segment funnel 19, segment CUSUM 23). The note's #18, joins only on the visible key (2 of 64, 1 under 0.50,
emerging), names how the link is made and #14, coarsens the segment it was asked about (3 of 64, 1 under 0.50), sits at
rung 1.

## Nearest exemplars

* Hospital Uncompensated Care Policy, "Award the 2026 grant to Hermann Area District Hospital, not Stroud Regional
  Medical Center" (Policy & Education), measured mean 0.26 over 4 runs. One hospital chosen on a construction that has
  to reproduce two certified prior cycles; the model built a construction that missed the controls, said so, and named
  a winner anyway (trap #1).
* Medicare Billing Integrity Review, "Refer NPI 1508302506 for the review year 2024 level-mix records review" (filed
  under Policy & Education), measured mean 0.18 over 4 runs. One provider referred for a records review; the share
  settles only after each provider's summary total is reconciled to its detail rows, and the model broke a 111-way tie
  instead (trap #19).

## Guard

Verdict against the corpus: WARN (`guard.py check`, exit 0). BLOCKs met while drawing and how each was cleared:
test.same_driver on (population, B, method_or_model_selection) against task109 inside the batch and task66, task67 and
task86 lineage, cleared by filing decomposition_attribution as the primary Gate G label (the note's own support
mechanism); ban.artifact monitoring_export against task116, cleared with published_series; ban.forcing_event
vote_or_meeting, purchase_order_or_contract and budget_or_appropriation against task115, task114 and task116, cleared
with audit_or_inspection; ban.shape 01 against task116, cleared with other.

* WARN repeat.geography (United Kingdom, England, against task116): kept, because the world is the note's own (English
  acute trusts and the national mortality indicator); the region, trusts and personas are fictional and no other
  furniture axis repeats task116, though task105, task111 and task116 already put three of the last twelve builds in
  Britain.
* NOTE test.same_driver_older (population, B, decomposition_attribution against task44 v1 and task64 v1 lineage):
  differentiated on the card; task44 v1 converts volume to hours through two corpus-recovered standards and task64 v1
  picks a shape rule from a menu, while here the decisive move is a construction with no menu that re-credits outcomes
  between candidates.
* Avoided before filing: repeat.opening (constraint-first, task116) by planning question-first; overuse.org_family
  (government_agency, 21 builds) by hospital_or_health_provider. No people rule fired.

## Changes from the source note

1. Gate G primary label is decomposition_attribution with method_or_model_selection support (the note has them the
   other way round), because (population, B, method_or_model_selection) is blocked by test.same_driver against task109
   inside the batch, and the decisive move is crediting correctly counted deaths to the trust where the pathway began.
2. The five flags come from the national mortality indicator publication's per-trust series (published_series)
   instead of the board's own monitor export, because monitoring_export is banned against task116. Each flag stays
   correct, labelled as a description of the last 36 months, and high somewhere for a documented reason.
3. The forcing event is the engagement's fieldwork start on 1 April 2027 (audit_or_inspection), because the planning
   meeting, the contract and the funding round are each banned against one of the last three builds.
4. Deliverables renamed after the decision: `allocation_note.docx`, `review_allocation.xlsx` and `pathway_deaths.png`
   become `external_mortality_review_2027-28.docx`, `review_allocation_workings.xlsx` and
   `review_allocation_by_trust.png`, because "pathway" in a prompted file name points at the decisive construction.
5. Opening move planned as question-first; the note's sketch opens constraint-first, which repeats task116.
6. Labelling only: the decisive rung is named as measured trap #2 gated by #1; the note lists #14, #1 and #18 without
   naming the decisive one.

## Tried and rejected
