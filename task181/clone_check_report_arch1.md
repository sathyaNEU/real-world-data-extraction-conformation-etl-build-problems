# Clone check: pre-flight, task181 against the whole corpus (pass 1), 2026-10-11

## Verdict
CLEAN for task181: no Exact, Same seed, Dataset or Template finding and no Shape echo. The one promoted pair, task103, is `clean_shares_components` on Track B and carries no Track A finding. The worst tier touching task181 is Idiom: it carries two corpus habits, the "what I need" ask carrier and the `extract_log_<date>.txt` provenance name. Batch level, not task181: Strategy monoculture, with the certified-record decoy in 7 of the 12 builds ending at task181 against a cap of 3.

**Stage 5 gate (`build-pipeline`).**
- The adjudicated pre-flight returns no Exact, Same seed, Dataset or Template finding, so its half of the gate holds.
- The two Idiom notes go to the author and are not looped on.
- The heart half is recorded in `task181/pipeline.json` as WARN, no BLOCK (`repeat.gate_g`, `overuse.gate_g`). This pass did not run `guard.py`.

## Scope and coverage

**Mode and scope.**
- Pre-flight on task181, architecture 1: a credit union's card fraud team sizing a card reissue. The decisive move re-screens the counterfeit victims that the dominant compromise point leaves unexplained.
- It was compared against every other build with the window ignored. The screen reports "all builds".
- This is pass 1: no clone check report existed for task181.

**Version checked.**
- **Card:** `cards/task181.json` at 46d3476 (07:09). That commit added only `stump_class`, `analyst_test` and `domain_test`. None of the thirteen fields the screen reads changed after my first extract (06:58).
- **Prompt and submission:** as at 441133a, unchanged since.
- **Pack:** 13 files under `target/`, last written at 06:32.
- **Design note:** as at 46d3476, including its new line differentiating task180's architecture 2.
- **Concurrent commits.** The 07:07 merge from `origin/main` (cfd29bc) changed skills and guidelines only. It added no build and no card, and did not touch the ledger, `fingerprint.py`, `clone-check/SKILL.md`, `clone-auditor.md` or the stage 5 gate.
- **Re-run.** After 46d3476 I re-extracted and re-ran the screen. The JSON output was byte-identical (sha256) to the first run.

**Extract.**
- **127 cards.**
  - 17 were fingerprinted from disk: task117 to task131, task181 and task229.
  - 110 were carried over from builds fingerprinted on another checkout (`/Users/saa/...`).
  - All 125 builds that have a card file match today's card files exactly on the mechanism fields (0 drifted). task112 and task113 have no card file.
- **Stale cache.** The tracked cache was written at 06:18. It held neither task181 nor the 06:54 rebuild of task229.
- **How I handled it.**
  - A side copy would have gone in the scratchpad, which is under /tmp, and this run was barred from /tmp. So I extracted in place.
  - After the last script run I restored `.claude/skills/clone-check/.cache/fingerprints.json` to its committed state with `git restore`. The pre-run file matched HEAD; sha256 was checked before and after.
  - `.claude/skills/fingerprint/.cache/people.json` was already modified before this run, and this run did not touch it (same sha256 before and after).
  - The untracked `cards/task180.json` was here before the run and was left alone.
- **The repo is untouched apart from this report.**

**Screen.**
- `fingerprint.py screen --focus task181` covered 125 screenable builds (task1 and task2 have neither a prompt nor a pack), so 124 pairs.
- The pairs were ranked against the 7,750-pair corpus baseline: mean surface 0.0545, with the 99th-percentile route starting at 0.1047.
- **Promoted: 1 pair, task103 against task181,** by percentile alone.
  - Surface 0.143, the 99.4th percentile; 46 corpus pairs score higher.
  - **Carried by:** flat layout (1.0), format overlap (0.57) and an identical deliverable species (pdf+xlsx).
  - **Not shared:** no file name, bytes, schema, numeric signature, invented name, prompt shingle, ask construction or write-up text.
  - **Track B:** only the decisive-gap label (`population`). No mechanism route promoted it.
- **Nearest not promoted:**
  - task131 0.096 (95.7th percentile);
  - task57 and task93 0.094;
  - task109 0.091;
  - task85 and task90 0.090.
  - All of these scores come from flat layout and format mix.

**Draw order.**
- The screen measures "consecutive" by task number, and the numbering jumps from task131 to task180.
- In the guard's draw order (drawn date, then number), task181's predecessors are:
  - task180, one back;
  - task131, two back;
  - task130, three back.
- task228 and task229 were drawn the same day, after it.
- I applied the consecutive-only routes to those neighbours with the screen's own functions. **None fires:**
  - task131: 95.7th percentile (the consecutive route needs the 97th); decisive gap only.
  - task130: 87.2nd percentile; decision type only.
  - task229: no pack profile on this checkout; decisive gap only.
  - task180: see below.

**Builds the screen cannot see.**
- task114, task115, task116, task180 and task228 have cards but no build on this checkout and no cache entry.
- I scored them with the screen's own `track_b_cards`. No route fires:
  - task114: nothing shared.
  - task115: the context-artifact type only (`close_out_summary`).
  - task116 and task228: the decisive gap only.
- **task180, one back in draw order.**
  - **Stale card here.** The `task180.json` in this worktree (untracked) is architecture 1, which its own lineage records as spent at round 1. Scored anyway, it shares the decisive gap only (driver overlap 0.043).
  - **Live card.** Architecture 2 (transformer dissolved-gas analysis, attributing main-tank acetylene to its source) is on branch `oviya13ya/task180-revenue-protection` at e2dfc69. I read it through git and did not copy it.
  - **Shared with the live card:** the objective (anomaly detection), Gate G `decomposition_attribution`, the decisive gap and the gap list (population, rule), pattern `none`, calibration `none`, and the decisive rule filed with no decoy.
  - **Different:**
    - the decisive code (G6 against G8);
    - the decision (a count against a ranked slate under a cap);
    - the shape (18 against 01);
    - the domain;
    - the deliverables (pdf+xlsx against docx+csv).
  - **Score.** One of three core axes collides. Card-driver overlap is 0.079 against the 0.40 line. No route fires even with task180 treated as the immediately previous build. **Not adjudicated in this pass.**
  - **task180's own record.** Its pre-flight on that branch records this pair adjudicated `clean_shares_components`, from task181's card only. task181's design note at 46d3476 now carries the differentiation: a population-level mixture is screened again after the dominant source explains its victims, against one unit's gas attributed between two sources by the gas it arrives with.
  - No Track A was possible: task180's prompt and pack are not on this checkout.

**Pairs adjudicated: 1 (task103), in this thread.**
- No Agent tool was available in this invocation, so I ran the adjudicator's procedure here:
  - each build's decisive move, with the domain nouns stripped;
  - each ordered path;
  - the position of the shared moves;
  - then the verdict, tier, track and axis.
- **task181 evidence:** card, prompt, submission, design note and pack listing, all read in full.
- **task103 evidence:**
  - its card (driver, stump, lineage, differentiation lines);
  - its ledger rows;
  - the cached prompt fingerprint (masked sentence openings, deliverables, invented names);
  - the cached submission (seven solution steps, critical components, recommendation);
  - the cached pack listing (19 files).
- **Not read:** task103's design note and full prompt are on another checkout. Its card's mechanism is taken from that design note (native labels).
- No golden file of either build was opened. task181's figures come from its submission and design note, and task103's from its cached recommendation and its card.
- `clone-check/SKILL.md` and `clone-auditor.md` were read in full at the start and are unchanged since 02:40. The tiers below come from that file.

**Pairs left unread: 123 of the 124 screened, plus the 5 card-only builds. None was promoted.**
- 21 partners carry two core axes, and none is consecutive by number or by draw order, so no route reaches them:
  - 20 share the decisive gap with the decision type (`quantity_figure`);
  - task68 shares the decisive gap with G6. It is the only other card whose decisive code is G6: a matched panel of continuing units across identity successions.
- 41 partners share the decisive-gap label. The highest card-driver overlap is 0.065 (task57).
- **Vocabulary sweep.** I swept every card driver, concrete driver, stump, note and lineage driver, and the ledger's full text, for the move's vocabulary:
  - **Terms:** residual, explained away, unexplained, dominant source, second source, two sources, mixture, co-visit, common point, set aside, re-screen, sequential attribution, set cover.
  - **Result:** every hit uses the words in another sense: a statistical residual, a residual group, a second supply source, a second data feed.
  - **Nearest construction:** task75's, a second arrival channel found as the residual between two counts of one period. That is an accounting residual, not a re-screen of unexplained cases. It is not promoted and was not adjudicated.

**Mechanism coverage, over the 124 other screened builds.**
- **Track B from both cards:** 102 pairs.
- **Track A only:** 22 pairs.
  - 17 partners have no mechanism layer: task3 to task10, task13 to task15, task18, task19, and task21 to task24.
  - 5 are note-only: task16, task17, task20, task112 and task113.
  - 20 of the 22 still carry a card driver sentence. On the screen's driver measure the highest is 0.067 (task4).
- **Back-fitted labels:** 34 partners (task36 and earlier). 14 of them have a card mechanism layer: task11, task12, and task25 to task36.

**Track A coverage gaps.**
- **Pack-level Track A** ran on 108 of the 124.
  - task3, task10, task117 to task129 and task229 have no profiled pack on this checkout (`target.zip` or nothing). Against those 16, file names, hashes, schemas and numeric signatures were not compared, only wording.
  - **Mitigation.** I compared task181's file names with the `metadata.json` file lists of task117 to task129 and with task229's `target.zip` member names (read without extracting). No file name is shared. The `extract_log` stem is shared with task124 and task229 (see Corpus habits).
- **Prompt and write-up.** Prompt-level Track A ran on 111 partners; 13 have no prompt in the cache. Write-up phrasing ran on 110.

**Status.**
- The ledger has rows for task25 to task108 only (79 builds).
- **Genuinely approved:** task25, task27, task28, task29, task30, task33, task34 and task35.
- **False positives.** The screen's "delivered or approved" on task48 and task72 are regex hits in fiction text ("one group-by delivered the conclusion"; "service delivered under").
- **No ledger row.** task109 onwards, task181 included, have no row, so their status is unknown on the record. Their own `pipeline.json` files record task117, task119, task130, task131 and task229 as delivered to the author, with no portal result.

## In batch against earlier builds
- Pre-flight has no window, so every pair is task181 against another build. The screen labels them "in batch" only because focus mode widens the window.
- **No hit against an approved or delivered build.**

| Build | Record | Surface (percentile) | Track B on the cards |
|---|---|---|---|
| task25, task27, task28, task29, task30, task33 | ledger: approved | 0.085 at most (task30, 78th) | nothing shared |
| task34 | ledger: approved | 0.020 | decisive gap label only (back-fitted on task34's side) |
| task35 | ledger: approved | 0.080 | decision type only |
| task117 | no row; its `pipeline.json` records delivered 2026-10-09 | 0 (no pack on this checkout) | decision type only |
| task119 | no row; delivered 2026-10-10 | 0 (no pack on this checkout) | nothing shared |
| task130 | no row; delivered 2026-10-11 | 0.089 (87th) | decision type only |
| task131 | no row; delivered 2026-10-10 | 0.096 (95.7th) | decisive gap only |
| task229 | no row; shipped 2026-10-11 | 0 (pack only in `target.zip`) | decisive gap only |
| task103 (promoted) | ledger: live; v4 built and on disk with no portal result recorded; v1 and v2 retired; not recorded as approved or delivered | 0.143 (99.4th) | decisive gap only; adjudicated below |

- task181 has no ledger row, so its status is unknown on the record. Its `pipeline.json` puts it in build at stage 4, with `approved` and `delivered` null.
- No exclusion-level exposure exists for task181.

## Track A findings, reviewer visible
None.
- **Hard tells.** Across all 124 screened pairs there are:
  - no byte-identical files;
  - no same-seed tables;
  - no tables with an identical column set;
  - no shared target file names;
  - no shared invented names.
  - "Larchmere Credit Union", "Ferrier Creek Travel Plaza" and "Lombard Market" appear on no other card. No persona's full name appears on another card.
  - The only shared capitalised token is "Thursday" (task14, task39, task67 and task107), which is business vocabulary.
- **Prompt and write-up.**
  - The largest masked-prompt overlap is 0.0046 (task124), and the largest write-up overlap is 0.0046 (task131).
  - No ask construction, solution-step construction or sentence opening is shared with any build.
- **`voice-check.py task181`**, run over task122 to task131, task181 and task229:
  - No carrier wording on its list and no unlisted repeated run.
  - The prompt is 206 words, the shortest of the twelve (median 250; paid-out median 227). It runs 22.9 words a sentence, with a 40.3 per cent context share (flag 46.0), a longest paragraph of 99 words and no rounding tags.
  - It is the only PDF deliverable of the twelve.
  - Its opening is classified "other", a bucket holding 7 of the 12. The card files it as number-first.
- **People.**
  - First names recur: Stephanie in task101, task120 and task127 (task127 is inside the twelve), and Donna in task110.
  - The design note's `guard.py surface` record lists only Laurie Townsend and Brenda Figueroa in the cut pack, so the recurring names are on the card only and are not visible to a reviewer.
  - The prompt's "Nicholas" is on no other card.
- **task103, the promoted pair: below Shape echo.** The outline compared on the four axes in Part 3:

  | Outline axis | task103 | task181 | Shared |
  |---|---|---|---|
  | Ask sentence | "The one figure I need is ...", then "It may be none." | "The committee approves a number of cards. That number is what I need." | The carrier family only (corpus "what I need", 13 builds). No shared masked opening. |
  | Deliverable pair | A determination PDF that opens the board paper, plus a workings XLSX ("... will check the release against ...", "The same workbook carries the counts ...") | A request PDF whose page one gives the count, plus a trace XLSX ("So the fraud desk can check it, the same figures go in ...") | **Yes.** These are the only two builds whose deliverables are exactly pdf+xlsx, and the only two prompts whose sentence openings justify the workbook with a checker in that construction. |
  | Decision | Release or hold, with an amount that may be nil (`go_hold_or_stop`, currency); shape 17, periods around a change point | A count of cards to reissue (`quantity_figure`); shape 18, hypotheses versus evidence | No on the cards. Both close on one figure for a board. |
  | Calibration organ | Certified matrix (two certified winter determinations) | None | No |

  - **Also shared:**
    - both are set in Ontario with CAD figures (Canada and CAD appear on 4 cards, Ontario on 3);
    - both are a flat pack;
    - task103's four formats (csv, xlsx, md, pdf) are all among task181's seven;
    - both prompts carry a colleague's partial read in the context ("Our chair's own read is ..."; "Nicholas traced the first cases to the pumps ...").
  - **Reading.** One outline axis is shared in full, the deliverable pair. "No single one of these is a finding." The ask is the corpus carrier, not the same sentence, and the decision and the calibration organ differ. It is not a Track A finding: there is no hard tell and no shared name or wording.
  - This is the pair a reviewer holding both would set side by side on the surface (see Notes for the author).
- **task131, two back and delivered on its own record.** It is the nearest on-disk surface (0.096), from flat layout and format mix: task181's seven formats are seven of task131's eight. It also carries both of task181's Idiom habits (Corpus habits). That is idiom, not pair evidence.

## Track B findings, mechanism
None, live or history.
- No card shares task181's decisive gap, decisive code (G6) and decision type together.
- No card shares the gap, the decisive code and Gate G together, which is the same-driver signature.
- task68 is the only other card whose decisive code is G6 (composition shift). Its driver is a matched panel of continuing units across identity successions, with the basis recovered from a closed corpus of settled dispositions. It is not consecutive and carries two core axes, so it was not promoted.
- No card driver, stump or ledger cell states task181's move (see the vocabulary sweep under Scope and coverage).
- The nearest drivers by text are task180's live card at 0.079 and task57 at 0.065, both far under the 0.40 line.

## Clean, shares components by design

**task181's decisive move, with the domain nouns stripped.** Cases drawn from two independent sources are pooled. The dominant source's cases inflate every place they also passed through and push the second source down among ordinary places. Attributing cases to the strongest source first, and screening only the cases it leaves unexplained, finds the second source. The exposed population is the union of both sources' exposures, each over its own window.

**task181's path** (design note ladder, submission steps):
1. Victim cards and their first counterfeit use, from the case workbook. Re-opened cases change no victim and no date (Layer 1).
2. Exposure counted on contact reads only (entry modes 05, 80 and 90, via the codebook). This is rung texture: the draft card's driver, demoted.
3. **Rung 0:** the pooled common-point screen, with a 60-day lookback against the member base rate.
   - Lifts: the pump 38.78, the coffee counter 11.95, the car wash and the PIN pad 4.59 each.
   - Keeping every terminal above a threshold gives 1,139 or 502.
4. **Rung 1, the stump:** the pump alone gives 174. **Rung 1b:** the residual put down to travel also gives 174.
5. **Rung 2, decisive:** set the pump's 205 victims aside and screen the 78 left. The PIN pad read 47 of them (lift 17.13).
6. Each terminal's window, from the first to the last victim read (CP-14 s5).
7. Open cards read by contact inside either window, each card once: 174 + 228 - 15 = 387.
8. The asks:
   - losses by card type: dispute-form currency, one row per retrieval reference, recoveries net of amounts taken back;
   - refunds within ten business days: Eastern reporting day, the MS-3 holidays, a re-opened claim counted as the same claim.

**task103** (ledger: live, v4; not recorded as approved or delivered). Read from its card, ledger rows and cached submission. Its design note is on another checkout.
- **Its move, stripped.** A record of contact stands for one unit, while a standing authorization lets one contact serve further units, and each unit has one allowance a period. Whether an authorized unit was actually served is recorded only in the handed-over quantity, which decomposes into per-unit standard amounts. A contact's second contact in a period carries only units served for others. So the scored count is each contact plus the units its quantities show were served.
- **Not the same claim.**
  - task181 conditions a co-occurrence screen on a dominant source, across a mixture of sources.
  - task103 recovers units that no row records by decomposing a quantity under a one-allowance rule.
  - There is no mixture of sources in task103, and no quantity to decompose in task181.
- **Its path** (cached steps, card):
  1. The terms (weekly figure, baseline, run, per-unit amount), the declared week and the last full week before the extract.
  2. Rows of record: the later upload of a re-sent batch kept; rows with nothing handed over, and sites off the schedule, dropped (Layer 1).
  3. Visiting units per week. This reproduces both certified determinations exactly and gives no run, so a nil release (the certified record that blesses the wrong count).
  4. Each contact fanned out through the authorizations in force: CAD 370,656. This was v1's decisive move, now a wrong committed answer.
  5. Each handed-over quantity read as own allowance plus others': CAD 263,412. This was v2's decisive move, now the stump.
  6. **Decisive:** one allowance per unit per period, so a second contact in the period carries only others' units.
  7. The weekly series against the same weeks of prior years: the declared week does not clear, and a twelve-week run clears at 5,171.00 units above baseline.
  8. CAD 54 a unit over the run: CAD 279,234.
- **Shared components, and where each sits.**
  - **A rate-against-baseline screen.** In task181 it is rung 0, and it is run again at the decisive rung on a conditioned population. In task103 it is step 7, arithmetic after the decisive count. It carries the decisive rung in neither build: task181's decisive rung is which cases the screen runs on, and task103's is what is counted before the test.
  - **Record hygiene.** A re-sent batch is kept once in task103; re-opened cases and repeated retrieval references are counted once in task181. This is Layer 1 in both, on low rungs and in the asks.
  - **The labels.** Both carry Gate G `decomposition_attribution`, the decisive gap `population`, G16 and the anomaly-detection objective. task103 decomposes a quantity into per-unit allowances; task181 attributes cases to sources. The labels are shared; the operations are not.
- **Swap test.**
  - Running task181's move on task103 (explain away the dominant source, then re-screen the residual) changes nothing: there is one shock and no co-occurrence screen, so the count stays wrong.
  - Running task103's move on task181 (decompose a handed-over quantity under a one-allowance rule) has nothing to act on, and the pooled screen still buries the PIN pad.
- **Verdict:** `clean_shares_components`, Track B. Tier: Clean, shares components by design. Axis to redraw: none.

## Strategy monoculture
The batch is the 12 builds ending at task181 in the guard's draw order: task121, task122, task124, task125, task126, task127, task128, task129, task130, task131, task180 and task181.
- Counts are read from the cards.
- task180 is read from its live architecture 2 card (`stated_rule_hard_construction`). The stale architecture 1 card in this worktree files `grain_or_unit`. No capped count changes either way.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy` | 2 of 12 at most: `identity_resolution` (task121, task126), `decomposition_attribution` (task122, task181), `causal_design` (task124, task131), `binding_constraint` (task127, task128) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129.
  - Their own `pipeline.json` files record task121, task122, task125 and task127 as retired.
  - task124 (stage 3), task126 (stage 3) and task129 (stage 2) are live.
- **task181** files `decomposition_attribution`, with the decisive rule filed, no official decoy and no validated decoy, so it adds to neither capped count.
- **Same-day wave view** (the twelve ending at task229, so including task228 and task229): the certified-record decoy is at 5 of 12, still over the cap. Template: 0. Largest single strategy: 2.
- **Corpus-wide:** 47 of 131 cards carry the certified-record decoy, and 19 the withheld-rule template.
- **Not a Part 3 cap.** Gate G `decomposition_attribution` is in 5 of the twelve (task121, task122, task129, task180 and task181). That is the guard's overuse WARN, and task181's design note answers it.
- **Recorded on task180's side.**
  - task180's move also fits `decomposition_attribution`.
  - Filed that way, task181 would repeat the strategy of the build drawn immediately before it (`ban.strategy`), and the strategy would reach 3 of 12.
  - As filed (`stated_rule_hard_construction`), no ban fires.

## Corpus habits
- **The ask carrier. This is an Idiom finding that touches task181.**
  - "What I need (from you) is ..." carries the Main Ask in 12 builds: task89, task95, task97, task107, task108, task111, task120, task123, task124, task126, task128 and task131. task181's closer, "That number is what I need.", is the same carrier inverted, which makes 13.
  - It is in 5 of the draw-order twelve: task124, task126, task128, task131 and task181.
  - task180's pre-flight flagged the same carrier, and task180's prompt has since dropped it. That leaves task181 the next build carrying it, two draws after task131's "So what I need is the ...".
  - **The tools miss it:**
    - `voice-check.py` does not list it as a carrier;
    - the screen's ask parser does not recognise it (task181's parsed ask is empty);
    - masking turns "What I need" into "<e> need", so counts built on openings under-read it.
- **The provenance file name. This is an Idiom finding that touches task181.**
  - The provenance record is named on "extract" in 7 of the twelve:

    | Build | Provenance file |
    |---|---|
    | task121 | `warehouse_extract_register.csv` |
    | task122 | `extract_register_slot_review.md` |
    | task124 | `extract_log.md` |
    | task126 | `extract_notes.md` |
    | task128 | `extract_provenance_2026-10-23.md` |
    | task131 | `extract_log_2026-09-14.txt` |
    | task181 | `extract_log_2026-10-05.txt` |

  - The same-day task229 ships `extract_log_20261012.csv`.
  - task181's file is task131's construction exactly (stem, ISO date, `.txt`), two draws apart. Even the job time matches: 06:12:41 against 06:12:44.
  - The layouts differ: a source, file and rows table against timestamped OK lines.
  - task180 renamed its own `extract_log_2026-10-16.txt` to `AM-EXT-0412_run_report_2026-10-16.txt` after its pre-flight flagged it.
  - This is a file role, not pair evidence. The habit is the name.
- **File names from the screen.**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 33.
  - `data_notes` and `provenance` appear in 12 each.
  - `county_reference` appears in 4, and eight other names in 3 each.
  - task181 uses none of them. Its `fraud_desk_notes.md` fills the `*_notes` hand-off role that most builds fill.
- **Deliverable pairings.**
  - pdf+csv 9; py 8; py+pdf 7; pdf+png 6; pdf+xlsx 6; py+csv 5; py+xlsx 5; docx 4.
  - task103 and task181 are the only builds whose deliverables are exactly pdf+xlsx. task67, task70, task74 and task81 add a third file.
- **Mechanism family: attribution before acting.**
  - Gate G `decomposition_attribution` is in 5 of the twelve.
  - task180 (architecture 2) and task181 are back to back, both anomaly detection, and both decide by attributing an anomaly to its source before acting.
    - task180: a benign attached source, separated by co-movement and composition.
    - task181: a dominant source whose cases are explained away before a re-screen.
  - The moves differ, as task181's design note now says, but the last two draws reached for the same family.
  - Anomaly detection is in 3 of the twelve: task125, task180 and task181.
- **Setting.** Canada with CAD appears on 4 cards (task103, task108, task114 and task181), and Ontario on 3 (task103, task108 and task181). None of the others is in the last twelve.
- **Openings.** voice-check's "other" bucket holds 7 of its twelve: task125, task126, task128, task129, task130, task181 and task229.

## What to redraw
1. **Batch level, not task181.** The certified-record decoy axis (`validated_decoy`) is at 7 of 12 against a cap of 3. It is carried by task121, task122, task124, task125, task126, task127 and task129; of these, task124, task126 and task129 are not recorded as retired.
2. **task181, Idiom, one file name in the generator (no figure moves).** The provenance record's name, `extract_log_2026-10-05.txt`, which repeats task131's `extract_log_<date>.txt`.
3. **task181, Idiom, prompt only (no data moves).** The Main Ask's closer, "That number is what I need."

There is no Track A or Track B redraw for task181.

**Cost, from the stage 3 and 4 rules.**
- Renaming a file under `target/` means a rebuild through the stage 3 gates, then `leak.py`.
- Either change sends the leak reader back over the pack, because the reader runs again whenever a document under `target/` or the prompt has changed since its last read.

**Notes for the author.** None of these is a finding and none is a redraw.
- **task103's outline.**
  - The deliverable pair, with its checker-and-same-workbook sentence, is shared only by task103 and task181 in the corpus. Beside it sits the Ontario and CAD setting.
  - It is below Shape echo, because the ask, the decision and the calibration organ differ.
  - If more surface distance from task103 is wanted, the cheapest axis is the deliverable pair.
- **task180, one back.**
  - It shares the objective, Gate G, the decisive gap, pattern `none`, no calibration organ and no decoy with task181, and both drivers sit in the attribution family.
  - Neither pre-flight has read both builds in full. task180's run saw task181's card only, and this run saw task180's card only.
  - The screen does not promote the pair. If the author wants it read on both design notes, both builds have to be on one checkout.

**Coverage and tooling notes.** None of these is a finding against any build.
- **(a) Card-only builds.** The extract fingerprints only folders that hold a `prompt.md`. So task114 to task116, task180 and task228 never reach the screen, and the `task180.json` in this worktree is the spent architecture 1.
- **(b) Consecutive by number.** The screen's consecutive-only routes compare task numbers, so they miss draw-order neighbours across the task131 to task180 jump. They were applied here by hand.
- **(c) Unprofiled packs.** task117 to task129 and task229 have no profiled pack on this checkout, so file-level hard tells cannot reach the builds drawn just before task181. File names were checked against their metadata and zip listings instead.
- **(d) Status regex.** It reads fiction text as delivery status (task48, task72).
- **(e) Ask parser and masking.** The ask parser has no "What I need" in its verb list, and masking erases "What I", so the Main Ask comparison is blind to the corpus's commonest carrier.
- **(f) Driver-text route.** The 0.40 overlap line does not see the attribution family between task180's live card and task181 (0.079).
