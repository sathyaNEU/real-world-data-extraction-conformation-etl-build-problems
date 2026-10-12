# Clone check: task228 pre-flight (architecture 2) against every build, 2026-10-11

## Verdict

No Exact, Same seed, Dataset or Template finding against any build. One Track B keying finding: the card keys G3 as the decisive code, which `vocab.json` and `stumping` 6.2 do not support. Keyed honestly as G16 (method selection), task228 repeats the decisive code of task134, the draw immediately before it. That is a Part 6.1 standing ban, and the guard enforces it as a BLOCK. Both builds are in flight, with no ledger row on either side.

## Scope and coverage

**Resolved scope.** This is a pre-flight on task228, architecture 2 (branch `perssathya/task228-guardrail-alert-metric`, HEAD 74b3e5f at the start of the audit, 94ad962 by its end; see below), against every build on file, with no window: task1 to task229 as fingerprinted. Draw order comes from `guard.py recent`. All the neighbours were drawn on 2026-10-11 and are ordered by task number: task130, task133 and task134 come before task228, and task229 comes after it. This is pass 4 for the number and the first pass on architecture 2. Passes 1 to 3 judged architecture 1, and their reports are untouched.

**Funnel.**
- **Extract.** The cache was stale on arrival: it was written from `/home/user/wt133` and held neither task228 nor task229. I re-extracted it in place, giving 128 build cards. 18 were fingerprinted from this checkout (task117 to task131, task133, task228, task229). The other 110 (task1 to task113) were carried from an earlier checkout, and this run cannot re-verify them. The refresh of `.claude/skills/clone-check/.cache/fingerprints.json` is left uncommitted.
- **Screen.** `fingerprint.py screen --focus task228`: 126 builds screened, 125 pairs with task228, **0 promoted**.
  - No hard tell: no byte-identical file, same-seed table or shared invented name.
  - No surface route: the top score is 0.090, at the 90th percentile.
  - No mechanism route: no card meets task228 on more than two of three mechanism axes. The only two that meet it on two (task73, task92) are not draw neighbours.
- **Guard.** `guard.py check task228` and `guard.py heart task228` both PASS, with one NOTE: `test.same_driver_older` against task107 v2, differentiated on the card. The nearest driver, stump or ledger text scores 0.05 (task229). The guard compared the card with all 131 cards on file, lineage included.
- **Adjudicated: 12 pairs.**
  - The draw neighbours task130, task133, task134 and task229 (its card on main plus the re-file).
  - task107 v2, the guard's NOTE.
  - The surface-nearest builds task131, task104, task48, task57 and task93.
  - task73 and task92, the only cards meeting task228 on two mechanism axes.
- **How they were adjudicated.** All in this thread. The `Agent` tool is not available in this run, so no per-pair subagents were spawned. I read:
  - every card in full;
  - task228's prompt, design note, submission and target listing;
  - the draw and stump sections of the design notes on disk for task130, task131, task133 and task229;
  - task229's `target.zip` listing (names only);
  - the ledger rows.

  No golden file was opened.
- **Left unread: 113 screened pairs.** None was promoted or named. Beyond the screen, three mechanical sweeps covered them:
  - the card mechanism scoring, which found nothing above two axes;
  - the guard's heart sweep of task228's driver, concrete driver and stump against every card, lineage driver and ledger row (max 0.05);
  - a keyword sweep for measurement-error language (own error, comparator or reference error, collocation, attenuation, errors in variables, latent or unobserved signal) across every card driver, concrete driver, stump, lineage driver and the shipped ledger. No build on file turns on separating a unit's own error from a comparator's.

**Mechanism coverage (126 screened).**
- 104 have a card mechanism (90 native, 14 back-fitted).
- 5 have a design note only (3 back-fitted).
- 17 are unavailable (all back-fitted, task36 and earlier) and were checked on Track A only.

Beyond the screen, task134 was compared by card through the guard.

**What was not checked, or was checked against something stale.**
- **task134** has no prompt, target or design note on this checkout. Its folder holds only the FC05 seed it was redrawn away from. Track B was read from its card; Track A is not available.
- **task130**: the folder on disk is the spent v2 (Tenter House), while the card is v3 (registered 07:57 UTC). Track A was screened against v2 and Track B was read from v3.
- **task229** ships `target.zip` and no `target/`, which the screen does not profile. Its target was compared by file name from the zip listing only. Its card as filed on main has no `stump_class`, `analyst_test` or `domain_test`. A scratch copy re-filed to general-statistics-data-science / missing-data-censoring-measurement-error BLOCKs on those three fields in `guard.py check`. That is task229's own matter, not a collision with task228.
- **main holds task228's architecture-1 card** (product analytics, `population_selection`, G13 decisive). task229's stage 4 copied it in at 03:06 UTC. task134 (registered on main at 08:10 UTC) and task229's rework are guarded on main against that spent architecture, not against architecture 2. This is the stale-card failure in `fingerprint` Part 4, and it is why neither draw could see the task134 collision below.
- **The build moved during this audit.** From 09:41 UTC another process changed task228, and at 09:46 UTC committed the changes as 94ad962:
  - it modified `task228/generator/{build,docs,golden,postprocess}.py`, `task228/DESIGN_NOTE.md`, `task228/metadata.json`, `task228/leak_check_report.md` and `task228/pipeline.json`;
  - it rebuilt `task228/target/`.

  The changes answer the leak reader's LEAK on NS-03 s.2.1 by dropping the sentence that named the products' own errors, and add an OOXML realism scrub. The commit does not touch the card, the prompt or the submission, and the design note's DRAW block and ladder are unchanged. I adjudicated 74b3e5f and then re-read the 94ad962 diff. The estimand stays filed, and the decisive rung and every card key are unchanged, so no verdict below depends on which version is read. The cache's task228 surface was extracted from the 74b3e5f cut. The rebuild renamed no file, and no neighbour shares a file name with task228 under either cut. This audit wrote only this report and the cache refresh.

## In batch against earlier builds

In pre-flight the batch is task228 alone. There is no collision, on either track, with any build the ledger records as approved or delivered. None of the twelve adjudicated neighbours carries such a status:
- task130, task131, task133, task134 and task229 have no ledger row. START_HERE lists task133 and task229 as shipped and task134 as in build, but the ledger has not recorded any of it.
- task104 has no ledger row.
- task48's only row records round 1 solved exactly and the build rejected by the author.
- task57's v23 row, task73's world-ten row, task92's v4 row and task93's v3 row record each build and no portal result.
- task107's v2 row records it retired on 2026-10-04, with the portal result "not stumped".

The one Track B finding is against task134, which is in flight.

## Track A findings, reviewer visible

None.

- **Surface-nearest pairs** (task131 at 0.090; task104, task48, task57, task93 and task133 at 0.089). They score only on folder layout and overlapping format sets. Every other axis is zero: no shared file name, schema, row count, numeric signature, invented name, persona, masked prompt wording, ask skeleton, deliverable species or write-up phrasing. This is proximity, not a finding.
- **task229.** No shared base name. Both packs carry a numbered standard (`NS-03_reference_stations_rev2.docx`, `MDS-STD-114_firmware_read_health_r3.pdf`), a register workbook and an export note. That is corpus idiom (see below), not a pair surface.
- **task123** (drawn 2026-10-08) asks for the same deliverable triple (docx, csv, png) and shares nothing else. A lone shared species is not a Shape echo.
- **`voice-check.py task228`.** The opening move is constraint-first, shared with task124 (2 of the last 12). No carrier phrase and no unlisted repeated run. The prompt is 267 words against a batch median of 256.
- The guard's name and people rules are clean.

## Track B findings, mechanism

### task228 against task134: keyed honestly, the decisive code repeats one draw back

**The decisive rung.** The design note's ladder and the submission's step 4 agree on it:
- the answer estimates each station's own random error by triple collocation of station, retrieval and model;
- rungs 0 to 2 rank stations on the unbiased error against the retrieval, the model, the better of the two, or their mean.

**How the card's keys fit that rung.** Judged against `vocab.json`, `stumping` Parts 1 and 2 and the generator definitions in 6.2, not by what the guard accepts.

- **`gap: objective` is honest.** Gap 3 is "the reported metric is correct and is not what the decision is scored on". The unbiased error against a reference is the field's standard validation figure, computed correctly from clean data. NS-03 s.2.1 scores something else: the station's own error against the unobserved truth. Nothing in the pack reports the naive figure, so this is not a surface read in a constraint costume.
- **`pattern: none` is honest.** No A to E pattern carries the rung. There is no past-against-forward, no rule recovered from a corpus, no serviceable share, no two grains and no conditioned yield.
- **`stump_strategy: decomposition_attribution` is honest.** Triple collocation splits each pairwise disagreement's variance into the three sources' error variances, and the covariances of the shared signal decide the split. That is "an outcome split across components, where overlap decides the split", and no other strategy family fits better. `decisive_rule_filed: true`, `official_decoy: false` and `validated_decoy: false` match the design note, both before and after the s.2.1 edit in 94ad962.
- **The decisive code G3 is not honest.** Because the pattern is `none`, the decisive code stands in for the pattern in every ban.
  - **What G3 means.** G3 is "record versus operation": a filed label or record names one party, and independent physical signatures show another. Section 6.2 says to "ship a label column and two or three independent physical signatures of the true owner".
  - **Why it does not fit.** task228 ships no record that charges the error to anyone. The "record" in the card's reading is the solver's own naive computation. Every other build keyed G3-decisive (task82, task101, task107 v2, task121, task126) is a literal ownership or identity record.
  - **Why G16 fits.** 6.2 defines G16 as "two or more defensible methods are available, they disagree on the answer, and exactly one survives a property of the data the pack makes checkable". The rung matches it to the letter:
    - the design note's ladder is a ladder of estimators, and its rung 0 is "the standard in-situ validation metric";
    - the estimators disagree (1, 2, 2 and 4 of the eight);
    - only triple collocation survives the references' own documented, cell-dependent errors;
    - the estimand is pinned by a filed standard, and `gate_g` method_or_model_selection reads "the right one pinned by validation or a standard".
  - **Why the card's case against G16 fails.** The card rejects G16 because "nothing chooses among a menu of estimators scored on a holdout". That reads G16 more narrowly than 6.2 does: 6.2 lists a holdout as only one of several kinds of discriminating evidence. task134 keys G16 for the same structure: Kaplan-Meier against cumulative incidence, pinned by the estimand, with calibration form none.
  - **The rule for two fitting keys.** `fingerprint` Part 4 says that where two keys fit, use the one a reviewer would use. A reviewer reads triple collocation against a single-reference error as an estimator choice.
  - **G17 is not a way round it.** A card keyed G17-decisive passes the guard, but 6.2 makes G17 supporting only.
- **Keys that carry no ban.**
  - `gate_g` decomposition_attribution is defensible, and method_or_model_selection fits at least as well.
  - The G13 lower rung (current probe only) is the step the design note itself calls rung-neutral cleaning. G4 (attribution at transition) would describe it better than G13.
  - `context_artifact: planning_thread` is defensible, because the campaign plan carries the eight slots. NS-03 plays the role task229's card keys as `filed_standard`. If task228 were re-keyed that way, the ban would fall on task229 as the later draw.

**What the honest key does.** I checked scratch copies of the card (nothing registered):
- with G16 decisive, the guard BLOCKs on `ban.pattern` against task134;
- with `gate_g` method_or_model_selection as well, it adds a `repeat.gate_g` WARN against task134.

Axis bans take no differentiation.

**Is it the same driver?** No, so this is not a Template.
- task134's driver is the probability of an event within a fixed horizon, with incomplete follow-up and competing exits. The share observed so far understates it, Kaplan-Meier with the competing exits censored overstates it, and only the cumulative incidence sizes the allocation.
- task228's driver is each unit's own error against an unobserved signal. Every comparison available carries the comparator's error, and three independent measurements identify each error from their covariances.

**The shared thing, with the domain nouns stripped.** In both builds the decisive rung is an estimator choice. The field's textbook estimator, run competently on clean data, is biased for the estimand that a filed standard or guidance defines, because the data carries a structure (exits that end the risk; a comparator with its own error). Only the field's specialist estimator recovers the estimand. That is the decisive-pattern family Part 6.1 bans reusing between consecutive builds. A reviewer holding the batch would see two adjacent builds that both turn on replacing the textbook estimator.

**Position.** The shared move is decisive in both builds. In task228 it is the top rung (rung 3, above three wrong estimators). In task134 it is the decisive rung (`generators` lists G16 first).

**Severity.** Neither side has a ledger row, so status on the ledger is unknown; START_HERE lists both as in build. The pair is consecutive: task134 is the draw immediately before task228 in `guard.py`'s order. Facts for the author:
- task228's architecture-2 draw, keyed G3 with G16 already weighed and rejected, was committed at 08:02 UTC on its branch.
- task134's card reached main at 08:10 UTC, so G3 was not chosen to dodge task134.
- task134 was checked on main against task228's spent architecture-1 card.
- `guard.py` orders same-date draws by task number, which places task134 first.

**Does the data survive?** Correcting the card's key moves no data, but it raises the BLOCK. On task228 the data does not survive a redraw of this axis: the pack, the per-season orthogonalised error construction and the 285 assertions in `checks.py` are all built around the triple-collocation rung.

**Axis to redraw.** The decisive pattern: task228's decisive code, which keyed honestly is G16.

### History, not a finding: task228 against task107 v2 (the guard's same-driver NOTE)

Under the card's keys, task228 shares task107 v2's decisive gap, decisive code and Gate G mechanism (objective, G3, decomposition_attribution). The drivers differ:
- task107 v2 scales a lottery pilot's assignment effect by a two-sided receipt contrast. It gets there through a join (timetable to staff directory to certification register) showing that the comparison arm also received the intervention.
- task228 separates a unit's own error from two comparators' errors.

Both rigorous methods can be read as instrumental-variable estimators; task228's design note says so of triple collocation. That is shared algebra, a component, not a driver. The card's differentiation line is accurate. task107 v2 is retired (ledger: retired 2026-10-04, portal result not stumped). Under the honest key (G16) the shared signature disappears.

## Clean, shares components by design

Every verdict here is `clean_shares_components`, with the driver difference named.

- **task130** (v3 card, three draws back, no ledger row).
  - Shares: the decisive gap label (objective first) and a filed-rules posture with no rival rule.
  - Its driver: regression to the mean in a cohort selected on an extreme, noisy outcome, forecast from an untreated cohort selected the same way a year earlier (pattern A, `forecast_method_backtest`). task228 separates instrument errors.
  - The rationed move-on lists of v2 and v2 loop 1, in its lineage, are further away still.
- **task133** (two back, no ledger row, START_HERE shipped).
  - Shares: Layer 2 family `field_method`, a filed rule, and no calibration organ.
  - Its driver: a cumulative default curve indexed from entry, conditioned on each unit's survival to date.
- **task134** (one back). Clean on the driver. The axis-ban finding above stands on its own.
- **task229** (one after; its card on main, plus the re-file to general-statistics-data-science / missing-data-censoring-measurement-error).
  - Shares: the objective (Data Quality Monitoring, which may repeat on its own), a filed numbered standard that states the measure and leaves the construction to the analyst, and a statistical-rigour decisive step.
  - Its driver: the unit a standard error is built over, because installations behind shared comms nodes fail together. task228's driver separates a unit's own error from the comparators' errors.
  - The re-file raises no axis ban against task228 (checked on a scratch copy).
  - **One condition.** Pattern 2 in the library for that task type (an error-prone measurement corrected with replicate or validation measurements that give its error variance) is task228's insight. If the rework moves task229's decisive rung onto it, task229 becomes a Template of task228 one draw apart. task229 is the later draw and would carry the finding, but its guard run on main would not catch it while main holds task228's architecture-1 card.
- **task131** (surface nearest, no ledger row).
  - Shares: only a numbered standard with a revision suffix.
  - Its driver: a lift measured at a randomised sub-unit carries spend moved from sibling sub-units that drew a different arm (interference).
- **task104** (no ledger row, drawn 2026-10-03, outside every ban window).
  - Shares: the monitoring neighbourhood and, under the honest key, the decisive G16.
  - Its driver: a self-adapting detector's log cannot show what a setting it never ran at would have flagged. A different claim.
- **task48** (v2 re-root).
  - Shares: Gate G decomposition_attribution.
  - Its driver: a population recovered only by aggregating to a two-sided pair grain, after every flag has been conditioned away.
- **task57** (v23). Its driver: a published source split into archives with different field names silently nulls a third of the records. No shared component.
- **task93** (v3). Its driver: a pay floor's cost tested per person per pay period, convex in the dial. No shared component.
- **task73** (world ten) and **task92** (v4).
  - Shares: these are the only cards meeting task228 on two mechanism axes (gap objective, `ranked_slate_under_cap`). A capped ranked slate is the prompt shape, which is a component.
  - Their drivers: both are binding-constraint slates. task73 turns on a monthly processing allocation under re-assigned review intervals; task92 on a capped counterfactual service applied on recovered receiving days.

## Strategy monoculture

The batch is the twelve builds in draw order ending at task228: task122, task124 to task131, task133, task134 and task228. task132 has no card.

- **One strategy in a third of the batch: none.** The largest shares are 2 of 12:
  - `decomposition_attribution` (task122, task228);
  - `causal_design` (task124, task131);
  - `binding_constraint` (task127, task128).

  Every other strategy carries one build.
- **Withheld rule with an official decoy: 0 of 12** (the cap is 2).
- **Certified-record decoy (`validated_decoy`): 6 of 12, over the cap of three.** The builds behind it are task122, task124, task125, task126, task127 and task129, all drawn 2026-10-09 to 2026-10-10, before the decoy retirement. task228 carries none, and neither does any build drawn since. In the twelve ending at task229 the count is 5, still over the cap.
- `official_decoy`: 1 of 12 (task122). Decisive rule left unfiled: 5 of 12 (task124, task125, task127, task130, task134).
- Under honest keys, the estimator-choice family (decisive G16) carries 2 of 12, task134 and task228, and they are adjacent. That is the Track B finding above, not a monoculture by the caps.

## Corpus habits

- **Pack file names.** `data_dictionary` appears in 61 builds, `export_manifest` in 33, `data_notes` in 12 and `provenance` in 12. task228 uses none of them.
- **The filed standard is named as a code with a revision suffix.** Examples:
  - `transport_costing_standard_ts-04_rev4` (task106)
  - `sp-04_volume_plan_and_copack_rev3` (task108)
  - `str-04_standard_obslugi_reklamacji_rev2` (task109)
  - `mp-3_measuring_offers_rev3` (task131)
  - `NS-03_reference_stations_rev2` (task228)
  - `MDS-STD-114_firmware_read_health_r3` (task229, zipped)

  Three of these are among the last six draws. The spec requires the filed rule; naming it this way is habit, and a reviewer holding the batch will notice it.
- **Deliverables.** `pdf+csv` leads the corpus pairings with 9 builds. Over the last twelve on disk:
  - there is no Code deliverable anywhere;
  - three builds sit at the three-file ceiling;
  - two of those three, task123 and task228, use the same docx, csv and png triple.
- **Openings.** Voice-check classes 7 of the last 12 opening moves as "other" and flags that as concentrated. The Main Ask opening "give me the single dollar figure we" appears in 2 builds.

## What to redraw

1. task228: the decisive pattern. Keyed honestly its decisive code is G16 (method selection), which task134 spent one draw earlier. The data does not survive.
