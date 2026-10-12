# Clone check: pre-flight, task131 against the whole corpus, 2026-10-10

## Verdict
CLEAN for task131 (no Track A finding, no live Track B finding). Worst tier touching task131 is a Template match against a dead row, task131 against the abandoned ledger-row-41 draw (task41 lineage, never built), which is history and not a redraw. Separately, at batch level the certified-record decoy stands at 9 in the last 12 builds against a cap of 3. That is a Strategy monoculture finding, and task131 is not one of the nine.

## Scope and coverage
- **Mode and scope.** Pre-flight on task131 against every other build, with no window. Extract re-run at the start of this check (125 cards, 123 with a prompt or target), then `fingerprint.py screen --focus task131`.
- **Builds compared: 125.**
  - The mechanical screen covered 122 of them (task1 to task130, less task1 and task2, which have no prompt or target in the cache, and less task114 to task116, see below).
  - task114, task115 and task116 have fingerprint cards. Their folders are not on this checkout and they were never in the carried-over cache, so the screen cannot see them. I compared them against task131 by hand from the cards on both tracks: drivers, deliverables, spine, invented names and people. No pack-level Track A was possible for them.
  - task99 is excluded as a scratch slot, which is correct: its card records it as the R5 state of task31's world.
- **Pairs screened: 122. Promoted by the screen: 0.**
- **Pairs adjudicated: 7, all promoted by the auditor and not by the screen.** They are task41 (ledger-row-41 draw, lineage), task107 (v2, lineage), task122, task116, task88, task83 and task118. I also ran a card-level surface check on task115, which shares the domain and the shape. I promoted these because the screen's mechanism route cannot fire for this card:
  - task131's pattern is `none`, so the pattern axis can never collide.
  - With the pattern axis dead, gap plus decision family is the most a pair can collide on, and that promotes only between consecutive builds.
  - The driver route is a lexical Jaccard. It scored the nearest semantic match (the task41 lineage draw) at 0.05.
  - So I ran a vocabulary sweep over every card driver, every lineage driver and the ledger's mechanism cells (randomisation, interference, spillover, sibling, displacement, cannibalisation, netting, saturation), and adjudicated each pair it surfaced.
- **Pairs left unread: 118.** None was promoted. The top surface neighbours (task109 and task90 at the 96th percentile, task45 and task30 at the 89th) score on flat layout and format mix only, which is corpus idiom.
- **How the reading was done.** No subagent tool was available in this thread, so I adjudicated here from the cards, the ledger, task131's design note and task122's design note. I opened no golden, submission or answer key beyond what the design notes state.
- **Mechanism coverage, over the 123 screened builds including task131:**
  - 101 have a card mechanism layer and 5 are note-only.
  - 17 have no mechanism layer (task3 to task10, task13 to task15, task18, task19 and task21 to task24).
  - 34 carry back-fitted labels.
  - Track B was scored on 100 pairs. 22 pairs were checked on Track A only (the 17 above plus task16, task17, task20, task112 and task113). The card-driver sweep reached task6, task21 and task24 in that set, and none shares the driver.
- **Staleness.** task117 to task131 were re-extracted from disk. task3 to task113 are fingerprints carried over from another checkout (`/Users/saa/...`). They cannot be refreshed or checked for staleness here.
- **Status.** The ledger runs to task108. task109 to task131 have no ledger row, so their status is unknown on the record.

## In batch against earlier builds
No hit against an approved or delivered build. The only approved build among the near neighbours is task30, at the 89th surface percentile. It is not promoted, shares only a flat layout and the format mix, and differs in decision and driver. No exclusion-level exposure exists for task131.

## Track A findings, reviewer visible
None.
- No byte-identical files, no same-seed tables and no shared invented name. "Talwerk" appears on no other card.
- None of task131's 12 personas shares a first or last name with any card on file.
- The target avoids the habit file names: it carries no `data_dictionary`, `export_manifest` or `provenance` file, and its field-notes role is named `crm_extract_field_notes.md`.
- `voice-check.py 131`: opening move question-first (2 of the last 12, with task127). No carrier wording or unlisted repeated runs. 254 words against a batch median of 252.
- task115 (same domain, shape 07, pick one of N, executive_team) differs on the deliverable species (pdf+xlsx against docx+png), the opening move (rule-first), the spine grain (store x week x line against card x ISO week), the calibration organ (existing book actuals against none) and the world (Ireland, EUR). That is not a Shape echo.
- task122 (same objective, shape 07, pick one of N, executive_team, register) differs on the deliverables (ipynb+png), the opening move (deliverable-first), the calibration organ (pilot_log against none) and the Gate G mechanism. That is two shared outline axes, below Shape echo.

## Track B findings, mechanism
**task131 against task41, ledger-row-41 draw (Policy & Education outreach arms, lineage). Tier: Template. Severity: history.**
- **Status.** The ledger records this row as "drawing" only. No folder ever held it, and the task41 slot was rebuilt as the FSSF certification build. So the colliding side is a dead row that never shipped and never reached a solver or a reviewer.
- **Shared driver, domain nouns stripped.** A correctly measured unit-level randomised effect does not survive scale-up, because treated units take their gain from a fixed pool shared with untreated neighbours, and correcting for that displacement changes which of four arms to scale.
- **Position.** It is the decisive rung in both. The task41 draw's correction was a displacement fit on untreated units against local treatment density joined to a capacity roster. task131's correction is reading the effect on parent units whose sub-units all drew one arm (rung 3 of 3, after the net-margin and run-rate rungs).
- **Repair.** None. The data survives because no repair is owed. This is a record of an abandoned draw, and nobody should be sent to redraw task131 over it.
- **Note for the author.** The interference/displacement driver is now spent once, in task131. The guard's lexical driver overlap (0.05) does not see this kinship, so the next draw in this family has to be checked by hand.

No other Track B finding.

## Clean, shares components by design
- **task122** (ledger silent, status unknown on the record; its design note records retirement on 2026-10-10, not submitted).
  - Shared components: a test read as pick one of N under shape 07, and netting outcomes that only moved rather than were created.
  - In task122 that netting (orders brought forward in time) sits below the decisive rung. The stump sentence has the competent solver already doing it. In task131 the moved outcomes (across sibling sub-units) are the decisive rung. So the device has been demoted on one side, which is reuse.
  - Driver difference: task122 turns on an outcome record that truncates at a session boundary and miscredits returning units' outcomes. task131 turns on the randomisation unit not being the economic unit.
- **task107 v2** (retired 2026-10-04, history).
  - Shared component: a randomised comparison whose arms are not cleanly separated.
  - Driver difference: task107 v2's comparison arm received the treatment through reassigned practitioners, corrected by scaling with receipt on both sides. task131's outcomes move between sibling units sharing a budget, corrected by reading on uniformly assigned parents.
- **task116** (ledger silent, status unknown).
  - Shared component: grouping children under a parent and keeping the parents whose children all share one property. This enumeration step sits on the decisive rung in both, which makes it the closest pair here.
  - Driver difference: task116's insight is population selection (realisable value exists only where one decision-maker buys for the whole group). task131's is interference (the randomised sub-units share one budget). A solver primed by one is not primed for the other.
- **task88** (ledger: built, awaiting round 1, not delivered).
  - Shared component: netting gross gain against volume displaced from a fixed pool.
  - Driver difference: task88 turns on a forward period where capacity binds and the closed record never did. task131 turns on experimental design.
- **task83** (ledger: built, no portal result for the current architecture).
  - Shared components: a randomised holdout effect read on a subset, and gap population plus objective.
  - Driver difference: task83 reweights by a target pool whose mix on prior treatment history differs from the measurement corpus.
- **task118** (ledger silent, status unknown).
  - Shared: domain, the `causal_design` strategy label and pick one of N.
  - Driver difference: task118's measured gain is already banked by the unit's own trials.

## Strategy monoculture
Batch: the last 12 builds in draw order ending at task131, which are task123, task119, task121, task122, task124, task125, task126, task127, task128, task129, task130 and task131 (from the cards' fields).

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **9 of 12** | 3 | **over, Strategy monoculture finding** |
| Any one `stump_strategy` | max 2 of 12 (identity_resolution, binding_constraint, causal_design, decomposition_attribution) | 4 (a third) | under |

- **The nine builds carrying the certified-record decoy:** task121, task122, task123, task124, task125, task126, task127, task129 and task130.
- **Wider view.** Corpus-wide it is 48 of 127 tagged cards, and `guard.py coverage` agrees on 9 of the last 12. Dropping task122 and task130 from the window (both reported retired or failed, though the ledger is silent on each) pulls in task120 and task118, which both carry the flag, so the count stays far over the cap either way.
- **task131.** Its strategy is `causal_design` with the decisive rule filed, no official decoy and no validated decoy. It adds to neither capped count, and it is the second `causal_design` in the window (with task124).

## Corpus habits
- **File names:**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 33.
  - `data_notes` and `provenance` appear in 12 each.
  - `county_reference` appears in 4 builds.
  - `product_catalog`, `accounts`, `plan_catalog`, `metric_definitions`, `item_master`, `facility_register`, `site_master` and `sources_and_licences` appear in 3 each.
- **Deliverable pairings:**
  - pdf+csv appears in 10 builds, py alone in 8 and py+pdf in 7.
  - pdf+png appears in 6.
  - py+csv, py+xlsx and pdf+xlsx appear in 5 each.
  - docx alone appears in 4.
- **Ask opening.** "give me the single dollar figure we" appears in 2 builds.
- **Last 12 by voice-check.** No unlisted repeated word runs. Formats lean on png, xlsx and docx (5 of 12 each). tsv, json, parquet, jpg, py, sql and r are unused as deliverables.

## What to redraw
1. task131: nothing.
2. Batch, not task131: the certified-record decoy axis (`validated_decoy`), at 9 of 12 against a cap of 3, carried by task121, task122, task123, task124, task125, task126, task127, task129 and task130.

Tooling note, not a finding against any build. The screen's mechanism route is inert for a card whose pattern is `none`. It also does not see cards whose builds are absent from both the disk and the carried cache (task114 to task116 here). The certified-record cap is breached even though `guard.py` blocks a draw at the cap, which suggests those flags were filed or back-filled after the draws were checked.
