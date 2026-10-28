# Clone check: task162 (pre-flight, against the whole corpus), 2026-10-28

## Verdict
No Template or worse found. Worst tier: Shape echo (soft flag), task162 architecture 2 against task229 (Track B, family resemblance only). Pairs with task161 and task164 are clean, sharing components by design. Track A on architecture 2 is unavailable (no prompt or data exist yet).

## Scope and coverage
- Mode: pre-flight, task162 against every other build, window ignored.
- Important state of the folder: `pipeline.json` is DESIGN, architecture 2 (a water-company valve forecast, re-rooted 2026-10-28). The card (`cards/task162.json`) and `DESIGN_NOTE.md` describe architecture 2. `prompt.txt`, `submission.md`, `golden/`, `target.zip`, `metadata.json`, `generator/` (build.py, parallel.py, postprocess.py etc.) and the leak and determinism reports are still architecture 1 (the Tampere browser bug-triage staffing build, spent). So Track B was checked on architecture 2 from the card and note; the surface screen ran on architecture 1's files. Architecture 1 against its own lineage is not a finding.
- Extract: 304 cards (302 with prompt or target). Mechanism layer: 280 cards, 5 note-only, 17 unavailable. Task162 has a card (mechanism_source design_note) and a note. Task161, 164 and 229 all have cards.
- Screen: 302 builds, 301 pairs in scope, 3 promoted, 3 adjudicated, 0 left unread. Nearest non-promoted neighbours (task232, 123, 140, 118, 145, 242) sit at surface 0.089 to 0.093 with pattern 0 and no shared decision family; proximity only, not read.
- Adjudication was done by me reading the cards, design notes and prompts. No subagent was spawned because no Agent tool was available in this run.

## In batch against earlier builds
All three promoted builds are delivered per the ledger (SHIPPED, delivered 10-13 or 10-18, pending review), so any hit would be exclusion level. None reached Template. See below.

## Track A findings, reviewer visible
None for architecture 2 (nothing cut). For architecture 1's shipped files: no pair promoted on surface; best surface 0.093 (percentile 95, task232) with no shared surface element named. Not a finding.

## Track B findings, mechanism
No Template, Dataset or Same seed finding. Promoted pairs, adjudicated:

1. **task161 vs task162 (consecutive draws, both delivered per ledger).** Promoted on two of three mechanism axes (gap time and population, decision type quantity_figure). Task161's move: stock bought ahead of a cost step leaves only as each holder uses its own, so the excess is netted account by account at each account's own burn share. Task162's move: a capped device bites only in the readings where the uncapped value exceeds the setting, so its effect is replayed reading by reading. Different claims; gap is the only shared axis, and the pattern (both none) is the corpus default. Strategy (other vs binding_constraint), Gate G, domain, world and decision all differ. Tier: clean_shares_components. Task161's own note already records this near miss.
2. **task162 vs task164 (two apart, both delivered).** Promoted on same domain and objective pairing (energy-systems-utilities x forecasting) and gap time. Not consecutive (task163 is economics), so the standing ban does not fire, and subdomains differ (asset-condition-maintenance vs load-forecasting). Task164's move: a load's effect on a shared asset's peak is its full draw at the peak moments, not its window average. Task162's move: replay a valve setting against recorded pressures. Different claims, different strategy (grain_or_unit vs binding_constraint). Tier: clean_shares_components. Worth noting: energy-systems-utilities x forecasting already holds 7 builds.
3. **task162 vs task229 (distant, both delivered).** Promoted because gap, pattern and Gate G mechanism line up on the cards (time, G7, forecasting). The kinship is real: both turn on a water-network device whose within-day operation is invisible in a daily or annual aggregate, and both name G7 as the operating window. The decisive moves differ: task229 is Jensen's gap, a convex rating applied to a daily mean water level against the mean of the converted flows, remedy is build the day's flow and convert before averaging. Task162 is a clip that binds only in some readings, and the design note itself says averaging the replayed readings is harmless (the mean-pressure route lands within 2 per cent), so order of averaging is not the point; finding where the cap is slack is. Objective (data quality vs forecasting), decision, strategy (grain_or_unit vs binding_constraint), calibration and artifacts differ. Tier: Shape echo (soft), Track B, verdict clean_shares_components on the driver. The card's `differentiation.task229` already states this. If the author wants it sharper, the one axis is to keep the decisive step away from any averaging or conversion-order framing in the prompt and asks.

## Clean, shares components by design
- task161: G7/G13 and the same slot's forecasting shape 02, different driver (stock burn-down vs valve operating window).
- task164: same domain and objective, G7 window idea, different driver (coincident peak vs setting clip).
- task229: G7/G13, within-day operation of a water-network asset, different driver (convexity bias vs clipping).

## Strategy monoculture
Corpus of 304 cards: population_selection 36, composition_mix 35, other 33, grain_or_unit 29, decomposition_attribution 28, time_semantics 21, causal_design 19, maturity_censoring 19, withheld_rule_official_decoy 19, forecast_method_backtest 16, binding_constraint 14 (task162 is one; about 4.6 per cent), identity_resolution 12, withheld_rule_corpus_fit 9. No strategy is near a third. decisive_rule_filed true in 88, official_decoy 35, validated_decoy 38; the cap thresholds in the skill are per twelve and per batch, so over the whole corpus I give counts only. In builds 151 to 169, withheld-rule-with-official-decoy is 0, certified-record decoy 0; no build over the caps. Task162 itself is official_decoy false, validated_decoy false, decisive_rule_filed false.

## Corpus habits
From the screen: `data_dictionary` in 111 builds, `export_manifest` in 68, `readme` 18, `data_notes` 14, `provenance` 13. Deliverable pairs: pdf+csv 9, py 8, py+pdf 7, pdf+png 6. Two builds share a Main Ask opening "give me the single dollar figure we". Idioms, not findings.

## What to redraw
Nothing from this check. Items for the author's action (not clone findings):
1. Task162's folder is mixed: card and note are architecture 2, but prompt, submission, golden, target.zip, metadata, generator and the leak and determinism reports are architecture 1. The ledger row and screen status still read SHIPPED, delivered 10-18, pending review for architecture 1 while pipeline.json says DESIGN. Reconcile before the next `guard.py surface` or `/approve`, because the surface screen currently reads architecture 1's text.
2. Re-run this check as a Track A pass once architecture 2's prompt and pack are cut; the Track B result above stands on the card and note only.
