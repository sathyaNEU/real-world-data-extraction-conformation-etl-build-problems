# task214 handoff: paused by the author

**Status: PAUSED (2026-11-08), on the author's word. No session is working on it, and nothing resumes without the author.**
Wave 8, Anomaly Detection & Diagnostics. Architecture 2, stage 1 (draw); nothing is registered for architecture 2. Batch
branch `claude/jolly-hypatia-06c61h`. The detailed next action is `pipeline.json` `resume`. The draw record is in
`DESIGN_NOTE.md` (`## Architecture 2 draw record`), and every dead approach is in `## Tried and rejected`.

## Where it stands

### Before architecture 1

Seed AD37's world (a bank's private-cloud batch platform with speculative backups) was set aside:
- its only honest Anomaly Detection home was General Statistics, which task212 held;
- its first candidate fell to a per-record host-by-night reader.

### Architecture 1: spent at stage 4

- **Domain:** Epidemiology, disease-surveillance-outbreak-anomaly-detection.
- **The world:** the Kotare District water supply and a spring 2027 cryptosporidiosis outbreak.
- **The call:** take boundary main WM55081 out of service before the feed main renewal, at 189.5 per 100,000
  resident-days.
- **Why it died:** the judge returned SEND_BACK on Gate H, decisive_step rule_application.
  - The outbreak team's terms of reference filed the whole procedure, and "received the asset's water for most of that
    day" steered anyone who read every rule to the right method.
  - The main call was forced and reproduced exactly. Unfiling the procedure would have left the estimand open on exactly
    what the decisive step recognised.
- **Records:** `determinism_check_report_arch1.md` and `pipeline.json` `lineage_v1`. Its generator is in git history
  (last at commit db8475f, `task214/generator/`).

### Architecture 2: current, stage 1

- **The cell:** environmental-monitoring-exceedance (Physical & Environmental Sciences). The pairing probes legal;
  differentiate test.same_puzzle_older against task270 v10.
- **The decisive step:** each groundwater exceedance is read against that well's own running maximum of the logged water
  level (logger system) at its lab sample date (lab system).
  - A fixed store in the ground answers only when groundwater climbs past every earlier height, and is then spent.
  - A continuing source answers every time groundwater returns.
  - The golden has no threshold, and no earlier build or slot note resembles it.
- **Dead worlds:**
  - Energy grid reliability (load hidden behind bypassed meters): the golden chained change-point detection, a regression
    and thresholds, so it moved with defensible settings.
  - World 2, a county council's closed landfills. Candidates G2 and G3 had the golden right on 4 of 4 seeds and 20
    readers wrong, but the true site's own exceedance history, read through a pre-window fit's residuals, showed.
- **World 1, a retired US coal plant's ash units:** candidate G1 died after two revisions, because a level-plus-year fit
  reached the true unit on 3 or 4 of 4 seeds. One candidate is left in this world.
- **Candidate 4 (world 1, "arrangement only"):** drafted in `generator/prototype/world4.py`, never screened.
  - The true unit's well C sits beside the river, and its highest level is a spring 2019 flood crest that only the
    logger records.
  - Both units recover alike after the production wells stop on 15 June 2023, and both exceed once a year from 2024.
  - The lab file alone shows the two units alike; only the logger's running maximum at each lab date separates them.
  - The first draft had three faults:
    - C exceeded about three times a year;
    - the D wells' natural background crossed the limit;
    - no D well made a new high in 2024.
  - The revision's parameters are written in the design note's paragraph "The arrangement as drafted"; they are not
    applied yet.
- **Conflict and protest event data** (the other cell in this build's partition) offered nothing honest even on paper:
  practices that must be filed or withheld, one-lag chains, and spent reporting-effort mechanisms.

## What needs to be done going forward

1. **Apply candidate 4's revision** from the design note's paragraph "The arrangement as drafted" to
   `generator/prototype/world4.py`.
2. **Inspect seeds 1 to 3** with `generator/prototype/inspect4.py`. Confirm:
   - C and every D well exceed once in each year from 2024 to 2027, and never before;
   - no lab sample catches C's flood crest, and the crest stands above all of C's window levels;
   - each D well's spring peaks are new highs.
   The ties between the units must be ordinary noise with a recorded cause (the production wells stopping), never exact
   copies.
3. **Write the screen harness.** Start from `generator/prototype/screens3.py`, which currently imports world3, the
   landfill world, so retarget it. Add:
   - every reader that killed G1 to G3;
   - the per-borehole statistics and the lowest-correlation reader;
   - recovery-size and window-trend discounts;
   - running maxima since the shutdown and over 365 and 730 days, and the running maximum of the field level at
     sampling;
   - the literal executions of the filed WHAT, and fit parity.
4. **Run all six screens on 4 seeds, then 20.**
   - **If it fails:** world 1 is spent too, and this cell has no live world left. Draw another world or cell under
     Anomaly Detection, outside the domains task212 and other recent builds hold.
   - **If it passes:**
     - draw personas with `guard.py names`;
     - put the card through `guard.py check` (with the differentiation line against task270 v10), `register`, then
       `check` again;
     - move architecture 1 into the card's lineage;
     - commit DRAWN;
     - carry on through design (precut exit 0), build (every free gate) and stage 4 (the leak reader and the
       determinism judge together, on Sonnet at medium effort).
5. **Before every guard run,** merge `claude/jolly-hypatia-06c61h` and copy any batch4 card your tree lacks into the
   cards folder, untracked.

## Binding lessons (from this build and its siblings)

- **Gate H:** a governing document may file the estimand but never the procedure. Assert that the literal execution of
  every filed sentence, and a careful replay of every stated fact, both land wrong. task213's playbook is the pattern:
  it defined a ring and never said how control shows.
- **Golden shape:** the golden is a deterministic construction with no threshold, keyed to each unit's own history
  across two systems.
- **No linear aggregates:** a decisive exposure that is a linear aggregate (a share, a mean, a cell rate) is adjusted
  away by careful readers. The decoy and the true unit share every aggregate and differ only in how their records are
  arranged.
- **Asks:** each ask rides a reconstruction across two systems that no sentence states.
  - An unmarked duplicate or an inferred join with no key is a fork.
  - Generated times keep causal order.
  - The cracker and the full includer each keep at most two fifths of the ask figures.
- **PDFs:** Word documents exported by LibreOffice Writer (`officepdf.py`, as in task482 on main). Producer LibreOffice,
  Creator Writer, a real Subject, the organisation as author, and no round-hour issue times. Never name the issuing
  organisation as the producer.
- **Prompt:** one question first, with at most one templating signal (files up front, steps, stacked questions, a
  closing list of documents, a dictated method, lists, UK spelling).
