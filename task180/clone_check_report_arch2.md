# Clone check: pre-flight, task180 (architecture 2) against the whole corpus, 2026-10-11

## Verdict
CLEAN for task180: no Track A or Track B finding and no Shape echo. The worst tier touching task180 is Idiom (two corpus habits, below), and the batch carries a Strategy monoculture (certified-record decoy, 7 of 12) that task180 does not add to.

**Stage 5 gate (`build-pipeline`).** It holds:
- `guard.py heart task180` returns PASS (no BLOCK, no WARN).
- There is no Exact, Same seed, Dataset or Template finding.
- The two Idiom findings go to the author and are not looped on.
- The adjudicated pre-flight re-runs only if the driver changes. The leak-reader hardening that landed during this check (05:59) did not change it (see Version checked).

## Scope and coverage

**Mode and scope.**
- This is a pre-flight on task180, architecture 2 (a lines company choosing three transformers for internal inspection from dissolved gas analysis; the decisive move attributes main-tank acetylene to its source). It was compared against every other build with the window ignored, and the screen reports "all builds".
- Architecture 1 (revenue protection, screen grain) appears only in the card's lineage. It is not a comparison partner, because a build cannot clone its own ancestor.
- The orchestrating session asked for this run as the clone-auditor's pre-flight, and this report path is the one it named. Nothing existed at that path. Architecture 1's pre-flight stays at `clone_check_report_arch1.md`.

**Version checked.**
- The card is `cards/task180.json` (05:36, unchanged through the run).
- The prompt (04:25), the submission (05:42) and the pack (12 files, built 05:42) were checked as they stood.
- The design note was checked as committed at 5a14a69 (05:45).
- While this check ran, a concurrent session applied the leak reader's hardening. It is uncommitted and not yet rebuilt into `target/`. It removes:
  - ES-DGA-02's scope sentence 1.2 ("coding applies to gases generated in the main tank");
  - the compartment-sampling clause 3.6, and its mention in the revision history;
  - `dga_tap_changer_compartments_2021-2026.csv` from the pack.
- The card, driver, stump, answer, prompt and submission are unchanged by that edit, so this check stands for the hardened build. The rebuilt pack has one file fewer, and nothing in the current pack collided with anything, so Track A cannot get worse. The next `guard.py surface` will re-profile it.

**Extract and screen.**
- The repo cache was written at 05:44:31, a minute before the design note's committed write. Re-extracting changed only task180's design-note word count.
- I first ran `extract` in place. I then restored `.claude/skills/clone-check/.cache/fingerprints.json` byte for byte from a copy taken before the run (sha1 a92ea11e...), so it is back to its pre-run state.
- I then ran `extract --out` and `screen --cache` on a scratch copy. The screen output was identical both ways at full precision, in both text and JSON.
- **The repo is untouched apart from this report.**
- The cache holds 126 builds. The screen covers 124, because task1 and task2 have neither a prompt nor a pack. That gives 123 pairs.
- task114, task115, task116 and task181 have cards but no build on this checkout and no cache entry, so they were compared on their cards only:
  - Track B was scored with the screen's own `track_b_cards`.
  - No Track A was possible.
- task99 is excluded as the scratch slot, which is correct.

**Pairs promoted by the screen: 0.**
- **Surface baseline.** The corpus has 7,626 pairs with a mean surface score of 0.055. The 99th-percentile route sits at 0.1045.
- **Nearest neighbours.** task89 0.104 (98.85th percentile, under the route), task93 0.100, task95 0.097, task90 0.094, task72 0.093 and task51 0.093. All of it comes from flat layout and format mix. task89 and task95 also share the masked ask opening "What I need from you is the" (see Corpus habits).
- **Track B, on the cards.** The axes task180 shares:

  | Shared axis | Partners |
  |---|---|
  | Decisive gap `population` | 40 |
  | Gate G `decomposition_attribution` | 14 |
  | Context artifact | 6 |
  | Decision type | 3 (task51, task73, task92) |

  - No other card's decisive mechanism is G8, so there is no decisive-pattern collision.
  - No pair has two or more core axes: 58 have none and 43 have one.
  - The highest driver overlap is 0.093 (task117), against a 0.40 route.
- **Consecutive-only routes.** These cannot fire by number for task180, because its numeric neighbours (task178, task179, task181 and task182) have no build on the screen. I applied them by hand to its draw-order neighbours (task129, task130 and task131 before it, task181 after it). None would fire: nothing is at or above the 97th percentile, no pair has two core axes, and no decisive pattern, pairing or calibration form repeats.

**Label sensitivity, and the pairs this check promoted.**
- The label route is silent only because the card files pattern `none` with `G8` first. Two other keys fit at least as well:
  - G8's own vocabulary entry is "gap 3, pattern C".
  - The card's decisive gap, `population` (gap 2), is G3's family. The decisive rung is built the way G3 is: three independent physical signatures of the true source.
- I re-scored task180 with the screen's functions and with `guard.py check` on scratch copies of the card. The card itself is untouched.

  | Key | Screen would promote | `guard.py check` |
  |---|---|---|
  | As filed (population, none, G8 first) | nothing | PASS |
  | G3 first | task121, task101 (same-driver signature) | BLOCK `test.same_driver` against task121 (inside the twelve); BLOCK `_older` against task101 (undifferentiated) |
  | Pattern C, gap population | task116 (card only): gap, pattern and decision | BLOCK `test.same_puzzle_older` against task116; `test.same_driver_older` against lineage rows of task36 and task83 |
  | Pattern C, gap objective | task119 and task38 (same-driver), task92 (gap, pattern and decision) | BLOCK `test.same_driver` against task119 (inside the twelve); `_older` against task38; `same_puzzle_older` against task92 and lineage rows of task51 and task92 |
  | Strategy `decomposition_attribution` | not applicable | PASS |

- **Promoted by this check and adjudicated (7):**
  - task119, task121, task101, task38 and task92, each from the alternative keys above.
  - task116. As filed it already carries two core axes (gap and decision type), and under Pattern C it fails the full similarity test.
  - task181. It is the same-day sibling outside the screen, and the construction sweep also surfaced it.
- **Also read on the cards: task25 and task28.** These are the approved Pattern C anomaly-detection builds. Under the Pattern C reading each shares gap and pattern with task180. The screen's rules would not promote them (two core axes, not consecutive), but I read them because they are approved.
- **Not promoted under any key, left unread.** Each of these has two core axes and is not consecutive:
  - task82 and task126 (G3 first);
  - task73 (G8's family and Pattern C);
  - task26, task32, task69, task94 and task105 (Pattern C, gap objective);
  - task75 (Pattern C, gap population).
- **Construction sweep.**
  - I searched every card driver, stump and lineage driver for task180's construction: leakage or carry-in, a neighbouring or second source, a signal made by ordinary operation, co-movement with operations, a composition ratio, explaining away.
  - Only task181 surfaced, plus an unrelated sense of "contaminated" in task83's lineage. The ledger's mechanism cells turned up nothing.
  - No other card is in the energy-systems-utilities domain.
- **Pairs left unread: 116 of the 123 screened.** No route promoted any of them under any key. task114 and task115 (card only) share no core axis with task180.

**How the reading was done.**
- **No subagent tool was available in this thread.** I adjudicated every pair here, in sequence, each from its own evidence. Each adjudication followed the procedure: the domain-stripped decisive move, the ordered path, the position of the shared moves, then the verdict, tier, track and axis.
- **Evidence per partner:**

  | Partner | What was read |
  |---|---|
  | task119, task121 | Card, prompt, submission, and the design note's draw, stump, decisive-rung and ladder sections. Pack listing from `metadata.json` and the `target.zip` member names, since there is no `target/` on this checkout. |
  | task38, task92, task101 | Card, ledger rows, and the cached submission (steps, critical components, recommendation), ask, deliverables and pack listing. Their folders live on another checkout (`/Users/saa/...`), so **their design notes and full prompts were not read here.** |
  | task116, task181 | Card only. task181's folder holds only its seed `START_HERE.md`. |
  | task25, task28 | Card and ledger row. |
  | task180 | Card, design note, prompt, submission and pack listing, in full. |

- No partner's golden or answer key was opened.
- The `clone-check` skill is not registered in this session's skill list. The tiers and the discrimination come from `.claude/skills/clone-check/SKILL.md`, read in full at the start of the run.

**Guard.**
- I ran `guard.py heart task180` directly. Its people index (05:44:36) was newer than every task folder, so it rewrote nothing; I checked the mtimes and `git status`.
- The verdict is PASS with no WARN.
- The nearest heart text scores 0.03 against every card driver, lineage driver, stump and ledger row. The nearest driver is task117 at 0.06. The BLOCK threshold is 0.30 and the WARN threshold 0.12.

**Mechanism coverage, over the 123 screened pairs.**
- **Track B from both cards: 101 pairs.** Of those partners, 14 carry back-fitted labels: task11, task12, and task25 to task36.
- **Track A only: 22 pairs.**
  - 17 partners have no mechanism layer: task3 to task10, task13 to task15, task18, task19, and task21 to task24.
  - 5 are note-only. task16, task17 and task20 have cards with no gap or pattern; task112 and task113 have no card.
  - The highest of these on surface is task112, at the 83rd percentile. That is far under the 98.5th-percentile route for "mechanism unknown, surface high".
- **Track B only, outside the screen:** task114, task115, task116 and task181, all card only.

**Pack-level Track A.**
- Pack-level Track A ran on 108 of the 123 partners.
- task3, task10 and task117 to task129 have no profiled pack on this checkout. task117 and task119 ship `target.zip` only.
- That gap includes nine of the eleven builds drawn just before task180.
- **Mitigation.** I compared the file lists in the `metadata.json` of task117 to task129, and the `target.zip` member names of task117 and task119 (read without extracting). None shares a file name with task180.
- No card's spine matches task180's spine file, entity, grain or row count.
- Prompt-level Track A ran on 110 partners (13 have no prompt here). Submission phrasing ran on 109.

**Staleness.**
- task117 to task131 and task180 were re-extracted from disk.
- task3 to task113 are fingerprints carried over from another checkout. Their cached card blocks match the current card files exactly: 0 differences.
- task112 and task113 have no card file.

## In batch against earlier builds
In pre-flight the batch is task180 alone, so every pair is task180 against another build. The screen labels them "in batch" only because focus mode widens the window. **No hit against an approved or delivered build.**

Status of each partner I read, from the ledger's status column. Where the ledger is silent, the status is unknown.

| Build | Ledger status | Other records |
|---|---|---|
| task119 | No row, so unknown. | Its `pipeline.json` records a determinism APPROVE, and stage 8 "delivered" (shipped to the author) on 2026-10-10, with no portal result. It is the partner most likely to end up delivered, and the closest relative found. |
| task121 | No row, so unknown. | Its `pipeline.json` and design note record it retired on 2026-10-10 and not submitted. |
| task101 (v1) | Live: built, no portal result. | Not recorded as approved or delivered. |
| task92 (v4) | Live: built, no portal result. | v1 to v3 are retired, solved on the portal. Not recorded as approved or delivered. |
| task38 (v3) | Live: rebuilt, awaiting a round. | v1 and v2 are retired. Not recorded as approved or delivered. |
| task116 | No row, so unknown. | Card only on this checkout. |
| task181 | No row, so unknown. | Card only on this checkout. Drawn the same day after task180 and in flight. |
| task25, task28 | **Approved.** | Read on the cards. |
| task180 | No row. | In build, at pipeline stage 4. |

No pair carries a finding, so none of these statuses moves the verdict.

## Track A findings, reviewer visible
None.

- **Hard tells.** None on any of the 123 pairs:
  - no byte-identical files and no same-seed tables;
  - no shared column sets and no shared rare file names;
  - no shared invented names. None of task180's twelve invented names appears on any other card.
- **Surface.** The scores are as above. Masked prompt-shingle overlap is 0.003 at most. The only shared sentence construction is the ask carrier (see Corpus habits).
- **People.**
  - No full name repeats.
  - **Donna.** Donna Carson, the requester, is named in the golden board paper. Her first name recurs once, from task110's Donna Ramirez, an older build. That is WARN level under the guard's name audit.
  - **Wendy.** Wendy Godfrey, the board chair, shares a first name with task125's Wendy Lyons, inside the twelve. She is on the card only and appears in no shipped task180 file.
  - The guard could not see either overlap on this checkout. Its people index is built from files on disk, and those two partner personas are not in it.
- **Geography.**
  - "New Zealand, Canterbury" is also task123's setting, ten builds back. The guard's geography rule reaches only three.
  - task123 is a philanthropic trust with no shared entity, place name or file. This is a note, not a finding.
- **`voice-check.py`, last 12 by number (task121 to task131, then task180).**
  - The prompt is 203 words, the shortest of the twelve. The median is 253 and the paid-out median is 227.
  - There is no carrier wording on the script's list and no unlisted repeated run.
  - The opening is classified "other", a bucket concentrated at 6 of 12; the card files it as calendar-first.
  - Two deliverables: docx + csv.
- **Shape echo: none.** The four outline axes are ask construction, deliverable species, decision shape and calibration organ. Against each adjudicated partner, at most one is shared; the detail is below.
  - The ranked-slate builds (task51, task73, task92 and task116) share only the decision shape.
  - The builds that share the ask carrier share nothing else of the four, beyond at most a docx file.

## Track B findings, mechanism
None.

- The seven pairs this check promoted are each Clean, shares components by design (below). None shares task180's decisive move.
- **History, not findings.** Under the Pattern C keys, the guard's older tests touch only dead lineage rows of other slots:
  - task36 Osterhout R1;
  - task83 v1;
  - task51 v4;
  - task92 v3.

  task180's own architecture 1 is lineage too. Nobody is sent to redraw over any of them.

## Clean, shares components by design

**task180's decisive move, with the domain nouns stripped:**

> A unit's monitored fault signal can contain a component carried in from an attached compartment whose ordinary operation makes it. A filed coding run on the raw signal ranks the units with a leaking neighbour worst. Attributing each unit's signal to its source removes them and leaves the internal faults. Two things settle the source: the signal's co-movement with the neighbour's operation count, and its composition.

**task180's path:**
1. Take each sample's report of record, and the base sample taken 330 or more days earlier.
2. Code every unit under the filed standard: preservation class, age band, levels, twelve-month increases and severity.
   - This is rung 1, and it names DSL-T1, LST-T2 and SBG-T2.
   - Rung 0 (the latest acetylene) is killed by the standard's 4.4.
3. **Attribute each unit's acetylene to its source, then code only what the main tank made. This is the decisive step.**
   - The evidence is the tap-changer type, the increments tracked against daily tap-change counts across rollovers and counter replacements, and the C2H2/H2 ratio.
   - Rungs 2 and 3 are partial attributions: dropping only the clearest leak, or dropping every in-oil unit. Each names a wrong slate.
4. Rank code 3 by severity and take three: SBG-T2, RLS-T2 and CGT-T1.
5. The asks:
   - operations since the last tap-changer service (rollovers against counter replacements, and a stale register field);
   - relative saturation at the latest sample (a UTC historian, and re-issued reports).

---

**task119 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task119's move.** A unit's correctly recorded long waits count against it where its own resource was in part held empty for its own scheduled work, even though the record shows that resource occupied throughout. Only the occupants' timeline in a second system reveals this. Every capacity measure excuses that unit, and it carries the most attributable events.
- **Not the same claim.**
  - task119 inculpates the unit every capacity measure excuses. It finds a self-inflicted cause behind an allocation record: assigned is not occupied.
  - task180 exculpates the units the filed coding ranks worst. It finds a benign outside origin inside a measurement: present is not made here.
  - The hidden fact differs, and so does the evidence: a timestamp join to the theatre system in task119, co-movement with a counter plus a gas ratio in task180. The correction runs in opposite directions.
  - A solver primed by task119 checks who held the beds, and that does not find a weeping barrier.
- **task119's path.**
  1. Deaths after long waits by referring trust (Lathingbury).
  2. Trusts with no level-3 beds are set aside.
  3. The 08:00 bed return.
  4. The minute-level census (Prideswick).
  5. Admissions during each wait, joined to referrals and the bureau audit.
  6. **Held beds dated against the theatre extract, giving Stennock at 27. This is the decisive step.**
- **Shared components.**
  - anomaly detection;
  - Gate G `decomposition_attribution`;
  - G3 and G8. G3 is decisive and G8 supporting in task119; G8 comes first and G3 second in task180;
  - a ladder in which each partial correction names a different wrong unit;
  - the `capacity_report` context artifact;
  - a docx board paper;
  - the furniture: `board_of_directors` deciding under `audit_or_inspection`. **Of the 36 cards that declare furniture, only these two carry that pair.**
- **Outline.** Only the docx paper is common, so this is not a Shape echo:
  - the ask is built differently (question-first, against "What I need from you is");
  - the deliverables differ (docx + xlsx + png against docx + csv);
  - the decision differs (one pick against a ranked slate of three);
  - the calibration differs (a revision log against none).
- **For the author.**
  - This is the nearest relative on file. It sits inside the same twelve and is the partner most likely to be delivered.
  - Under a Pattern C key it is the guard's `test.same_driver` BLOCK.
  - The design note's similarity claim names only task181. The "Not the same claim" points above belong beside it.

**task121 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task121's move.** Units the records file as newcomers belong to established accounts, reachable only through a three-file reference chain. A channel strips their stored state, so their loss is the largest current loss. Joined on the visible key, they read as harmless dilution, which every closed case confirms.
- **Not the same claim.**
  - task121 re-attaches records to their true owner and enlarges one candidate's loss. Nothing is removed from any total.
  - task180 nets a carried-in component out of a measurement and shrinks the worst candidates' severity.
- **task121's path.**
  1. Bot filter and weeks.
  2. **Token to member number to account, including the SOCIO-code route. This is the decisive step.**
  3. Each fix's population.
  4. Each sized against its own baseline: 51 against 18.
  5. Valued.
  6. The pick.
- **Shared components.**
  - G3, decisive in task121 and second in task180: independent signatures agreeing on the same records.
  - The decisive gap.
  - Gate G.
- **Outline.** None of the four axes is shared. task121 is an html + xlsx pick-one with a prior-period close-out and an options-first ask.
- **Status.** task121 is recorded as retired, so even a collision would have been history.

**task101 against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task101's move.** A threshold is cut from a distribution that the decision's own earlier payments have since entered, under their intermediaries' names. It has to be cut net of those payments. No closed setting can reveal that component, because every closed baseline ended before the first payment.
- **This is the closest construction on file.** In both builds, the decisive rung nets a carried-in component out of a correctly reported per-unit quantity before a filed rule is applied.
- **Not the same claim.**
  - task101's component is the decision-maker's own earlier intervention feeding back into its baseline. It is found through an identity link on a register, and it is hidden from a closed corpus by construction (a validated decoy).
  - task180's component is a neighbour's ordinary operation. It is found by co-movement and composition, with no corpus and no decoy.
  - The thing to see differs: the decision's own money sitting in the data, against a weeping barrier.
- **task101's path.**
  1. Dedupe.
  2. Place.
  3. Spread.
  4. Reproduce rounds one and two. This is the validated decoy.
  5. The naive line, £13.80.
  6. **Follow the Fund's money through the charity register. This is the decisive step.**
  7. Cut the line at £12.40.
  8. Bands and target.
  9. Against round two.
- **Shared components.**
  - G3, decisive in task101.
  - The decisive gap.
  - Gate G.
  - The net-out-before-the-rule family at the decisive rung, on different devices.
- **Outline.** None of the four axes is shared. task101 is a dial setting delivered as pptx + xlsx, calibrated on counterparty acknowledgements.
- **For the author.** Under a G3 key the guard asks for a differentiation line against task101. The "Not the same claim" points above are that line.

**task38 (v3) against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task38's move.** The decisive quantity is the share of each candidate's correctly reported magnitude that the single intervention can remove. It is built from a horizon filter crossed with a control attribute computed behind a join. The realisation rule is recovered from a closed corpus of past interventions. The winner ranks near the bottom on magnitude.
- **Not the same claim.**
  - task38's thing to see is a rule withheld from the pack and recovered by fitting a corpus: led credits falling due inside the window.
  - task180's is a physical origin, read from co-movement and composition under a filed standard.
  - What they share is Pattern C's frame: rank on what the intervention can reach, so the largest magnitude loses. That frame is a component.
- **task38's path.**
  1. The cycle.
  2. Compile it and reproduce RC-X.
  3. The section 3.1 list.
  4. Scope: six members.
  5. Leadership and the window.
  6. **Recompose the 33 closed directions and fit. This is the decisive step.**
  7. The twin pair.
  8. Rank.
  9. Direct.
- **Outline.** None of the four axes is shared. task38 is a pick-one, delivered as py + xlsx, calibrated on a closed decision corpus, with a different ask.

**task92 (v4) against task180.** Verdict: `clean_shares_components`, Track B. Axis to redraw: none.
- **task92's move.** A capped service is worth only what it removes on the days each candidate actually receives it, and those days are recovered from each candidate's whole history. Working the capped queue on those days, net of the second charge the service starts, re-ranks the slate.
- **Not the same claim.** task92 recovers an operating window from history (G7). task180 attributes a signal to its source.
- **Shared components.**
  - Shape 01, a ranked slate under a cap.
  - The C frame.
  - G8, second in task92 and first in task180.
- **task92's path.**
  1. The discharge lifts.
  2. Completion, and both clocks.
  3. The settled years reproduce the desk's ranking.
  4. Every-day collection.
  5. Three collections a day.
  6. Net the transfer between the clocks.
  7. **Delivery-day diaries from the whole history. This is the decisive step.**
  8. The four places.
- **Outline.** One of the four axes is shared, the decision shape. task92 delivers pdf + svg, calibrates on a settled ledger, and words its ask differently.

**task116 against task180.** Verdict: `clean_shares_components`, Track B, card only. Axis to redraw: none.
- **task116's move.** An offer to a group realises value only in groups whose members' purchases were all made by one decision-maker, which shows as one signatory recurring across the members' records. Every closed offer went to such a group, which makes it a validated decoy. The largest uncovered volumes sit in groups that buy one by one.
- **Not the same claim.** task116 recovers buying authority from signatories, meaning who can accept the offer. task180 recovers a measurement's physical origin.
- **Shared components.**
  - G8 first in both.
  - The decisive gap.
  - A ranked slate under a cap, in shape 01.
  - As filed, that is two core axes (gap and decision type). Under Pattern C it is the full similarity test.
- **Outline.** One of the four axes is shared, the decision shape. task116 delivers pptx + xlsx, calibrates on a pilot log, and opens constraint-first.

**task181 against task180.** Verdict: `clean_shares_components`, Track B, card only. Axis to redraw: none.
- **task181's move.** Victims of two independent sources are pooled, so the dominant source's victims make the places they also passed look like sources and push the second source down. Only two steps separate the second source: attributing victims to the strongest source first, then screening the residual. The exposed population is the union of both.
- **Not the same claim.**
  - In task181 the sources compete for the same victims. The stump is stopping after the first source: the solver never explains away the co-occurrence that hides a second source.
  - In task180 each unit's own signal has a second, benign origin. The stump is not attributing at all.
  - The design note already says this, correctly.
- **Shared components.**
  - anomaly detection;
  - the decisive gap;
  - Gate G `decomposition_attribution`;
  - calibration `none`;
  - the decisive rule filed, with no decoy;
  - drawn the same day, back to back.
- **Outline.** None of the four axes is shared. task181 is a quantity, delivered as pdf + xlsx, with a number-first opening.
- **For the author: this is the batch exposure.**
  - task180's move also fits the `decomposition_attribution` strategy ("an outcome split across causes"), which is task181's filed strategy.
  - Filed that way, task180 still passes its own check; I verified this.
  - But task181 would then repeat the strategy of the build drawn immediately before it, which is the guard's `ban.strategy`. That comes on top of the shared objective, decisive gap and Gate G.
  - That is task181's draw to answer. It is recorded here because the two will ship as neighbours.

**task25 and task28 (both approved), read on the cards. Both are clean.**
- **task28.**
  - Its driver is the share of each flagged excess that one intervention can reach, counted as records clustered in single-source batch events and pinned by a closed set of realised outcomes.
  - Shared with task180: anomaly detection, and the C/G8 frame, in which the worst flagged excess loses to the reachable share.
  - The thing to see differs. task28 clusters a real excess by its source, using a realised-outcome corpus. task180 finds a benign source producing a false fault signal, under a filed standard.
- **task25.**
  - Its driver adds records that a second source holds to the inflow, then ranks forward by recoverable lift.
  - It shares the C/G8 frame only.
- **Why they matter.**
  - Under a Pattern C key, task180 sits in the anomaly-detection-by-Pattern-C cell. The stumping skill's Part 2 lists that cell as spent on these two approved builds.
  - task180's distinctness rests on its origin-attribution discriminator.
  - The design note's six-point check, item 6, reads stronger than the corpus supports. It says "No earlier task teaches source attribution of a diagnostic signal before ranking", but task28 decomposes a flagged excess by source before ranking.
  - The claim that differentiates task180 is narrower: a benign coupled source, identified by co-movement and composition.

## Strategy monoculture
**Batch.** The last 12 builds in draw order ending at task180, counted from the cards' fields: task119, task121, task122, task124 to task131, and task180.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy` | max 2 of 12 | 4 (a third) | under |

- **The seven:** task121, task122, task124, task125, task126, task127 and task129.
  - All seven were drawn before the client's two-layer standard of 2026-10-11, which now blocks this decoy on any new draw.
  - task121, task122, task125 and task127 are recorded as retired in their own `pipeline.json`; the ledger is silent on all seven.
  - If the recorded-retired builds are dropped, the window takes in task115 to task118 and the count is still 7 of 12. Either way it is over the cap.
- **Strategies at 2 of 12:**
  - decomposition_attribution: task119, task122;
  - identity_resolution: task121, task126;
  - causal_design: task124, task131;
  - binding_constraint: task127, task128.
- **task180's own strategy.**
  - It files `stated_rule_hard_construction`, with the decisive rule filed, no official decoy and no validated decoy, so it adds to neither capped count.
  - It is the only build in the window with that strategy.
- **Ending the window at task181** (in flight): the count is unchanged at 7 of 12. If task180 were filed as `decomposition_attribution`, that strategy would reach 3 of 12 there (task122, task180, task181). That is the guard's overuse WARN, though still under a third.
- **Same as before.** Architecture 1's pre-flight counted 7 of 12 on the same window.

## Corpus habits
- **The ask carrier. This is an Idiom finding that touches task180.**
  - "What I need (from you) is ..." carries the Main Ask in 13 builds, going by the cached masked openings: task89, task95, task97, task107, task108, task111, task120, task123, task124, task126, task128, task131 and task180.
  - It is in 5 of the draw-order twelve: task124, task126, task128, task131 and task180.
  - The exact wording "What I need from you is the" appears in task89, task95, task120, task126 and task180.
  - `voice-check.py` misses it: the phrase is not on its carrier list, and three verbatim uses in twelve fall under its third-of-batch line.
  - The screen's ask parser has no "What I need" in its verb list, so the Main Ask comparison is blind for all thirteen builds.
- **The provenance file name. This is an Idiom finding that touches task180.**
  - The provenance record has moved from `export_manifest` (33 builds) to names built on `extract`. That accounts for 7 of the twelve:

    | Build | Provenance file |
    |---|---|
    | task121 | `warehouse_extract_register.csv` |
    | task122 | `extract_register_slot_review.md` |
    | task124 | `extract_log.md` |
    | task126 | `extract_notes.md` |
    | task128 | `extract_provenance_2026-10-23.md` |
    | task131 | `extract_log_2026-09-14.txt` |
    | task180 | `extract_log_2026-10-16.txt` |

  - task131 and task180 use the same `extract_log_<date>.txt` construction, back to back.
  - This is a file role, not pair evidence. The habit is the name.
- **File names from the screen.**
  - `data_dictionary` appears in 61 builds and `export_manifest` in 33.
  - `data_notes` and `provenance` appear in 12 each.
  - `county_reference` appears in 4, and eight other names in 3 each.
  - task180 uses none of these. A `*_notes` file, like task180's `oil_results_notes.md`, appears in 38 builds.
- **Deliverables.**
  - The commonest pairs of the first two extensions: pdf + csv 9, py 8, py + pdf 7, pdf + png 6, py + csv / py + xlsx / pdf + xlsx 5 each, docx 4.
  - A .docx paper ships in 6 of the twelve: task119, task125, task126, task127, task131 and task180.
  - docx + csv exactly appears in 3 builds: task82, task110 and task180.
- **Mechanism family.**
  - Gate G `decomposition_attribution` appears in 5 of the twelve ending at task180 (task119, task121, task122, task129 and task180). That is the guard's overuse line, and task181 follows it with the same mechanism.
  - Anomaly detection appears in 3 of the twelve (task119, task125 and task180), and task181 comes next.
- **Furniture.**
  - The `capacity_report` context artifact appears in 3 of the twelve: task119, task127 and task180.
  - `board_of_directors` with `audit_or_inspection` appears only in task119 and task180, of the 36 cards that declare furniture.
- **Openings.**
  - voice-check's "other" bucket holds 6 of the twelve: task125, task126, task128, task129, task130 and task180.
  - Calendar-first appears on the cards in 5 builds: task89, task108, task117, task128 and task180.
- **Geography.** New Zealand is the setting in 5 builds (task68, task81, task107, task123 and task180), and Canterbury in task123 and task180.

## What to redraw
1. **Batch, not task180.** The certified-record decoy axis (`validated_decoy`) stands at 7 of 12 against a cap of 3. It is carried by task121, task122, task124, task125, task126, task127 and task129. Of these, task124, task126 and task129 are the ones not recorded as retired.
2. **task180, Idiom, prompt only (no data moves).** The Main Ask's carrier sentence, "What I need from you is ...".
3. **task180, Idiom, one file name in the generator (no figure moves).** The provenance record's name, `extract_log_<date>.txt`, which repeats task131's.

There is no Track A or Track B redraw for task180.

**Notes for the author.** None of these is a finding, and none is a redraw.
- **Write the differentiation down.** Put one line each against task119, task101 and task121 into the design note's similarity claim, using the "Not the same claim" points above.
  - The label route is quiet only on the filed keys (pattern `none`, G8 first).
  - Either other honest key makes the guard BLOCK: against task119 (shipped to the author) or task121 (retired) inside the twelve, and against task101 without a differentiation line.
  - All three pairs were read here and are clean.
- **Narrow six-point check item 6.** Reword it to the benign coupled source identified by co-movement and composition. task28 (approved) already decomposes a flagged excess by source before ranking.
- **Watch task119 on furniture.** It is the nearest relative on file and the likeliest to be delivered. Its board-and-inspection furniture is unique to these two builds among the cards that declare it. If the author wants more distance, the cheapest axis is the deciding forum.

**Tooling notes.** None of these is a finding against any build.
- **Consecutive routes run on task numbers.** The screen's consecutive-only routes compare task numbers. A slot numbered far from its draw-order neighbours, as task180 is, never meets them. I applied the routes by hand here.
- **Ask parser.** The screen's ask parser does not recognise "What I need ..." asks, and 13 builds use them.
- **People index.** The guard's people index is built from files on disk. Personas of builds not on this checkout are invisible to its name audit; here that hid Donna (task110) and Wendy (task125).
- **Unprofiled packs.** Pack-level Track A is blind on this checkout for task117 to task129, because those packs are held in `target.zip` or not at all.
- **People-index rebuild.** Writing this report into `task180/` makes that folder newer than `.claude/skills/fingerprint/.cache/people.json`. The next `guard.py check`, `heart` or `surface` will therefore rebuild the index.
