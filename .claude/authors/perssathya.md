# Author: perssathya (developer 3)

Applies only to sessions run for this author (account email pers.sathya@gmail.com). A session run for
anyone else ignores this file. The first part holds the standing rules; the last section, `Where work
stopped`, is the resume point and is rewritten whenever work stops.

## Branches and shipping

- Every build goes on its own branch under the `perssathya/` prefix (`perssathya/taskNN-<slug>`);
  skill or rule edits go on `perssathya/skills-<slug>`. Never push to another prefix, and never rebase
  or force-push another session's branch.
- Pull `main` (merge it into the build branch) at every stage boundary that ships or picks up work.
- On ship, the commit message starts `SHIPPED (taskNNN): ` with the call, then a PR to `main`, merged.
- Keep the private status page current: https://claude.ai/artifact/EJXoU6JxGoZ1oZYKHmSLyt (task id,
  links to prompt, submission and zip, status SHIPPED, IN PROGRESS, PAUSED or QUEUED).

## Lane

- **Data Quality Monitoring & Alerting, task228 to task252.** Two builds in flight; the author may allow
  a third. When one ships, pick up the next lowest open number.
- **Never retire a task without asking the author.** Re-roots follow the pipeline. A re-root past the
  third architecture, a ban waiver, or a retirement is the author's call.

## Working rules (author directives)

- **Models and effort per role** (`build-pipeline`, Models and effort):
  - the designer (draw, ladder, the paper half of every hardening loop and re-root): Opus at max;
  - the builder and the duplicate-check auditor: Opus at medium;
  - the solver: Opus at high;
  - the leak reader and the judge: Sonnet at medium.
  Hardening loops and re-roots are a designer on paper first, then a fresh builder from its commit.
- **Read the stumping skill and always improvise on the stumping ideas.**
  - Write the default path first, and put the stump on it: the default construction itself is wrong.
    A reflex correction (stratify, reweight, shrink, add a control, cross-check references) is not a
    stump.
  - Aim at the opponent's blind spots (stumping, Part 0).
  - Couple the pitfall to the domain: the field's own method. Learn from the client's examples and from
    the builds whose solver missed; never template them.
  - Screen every rung (stumping 2.1). Before any "spent" or "no architecture" call, write at least four
    candidates, each with a default path and a screen. Harden by stumping Part 8's escalation, not by
    stacking more of the same move.
- **Isolation.** Leak readers and solvers run only in scratchpad sandboxes holding `prompt.txt` and
  `target/`. No brief, design text or result sits in the scratchpad while they run. Results and notes
  live outside the scratchpad, and anything worth keeping is committed, because the container is
  temporary. Never commit the derived guard caches. No em dashes.
- **Draw order.** The guard sorts same-date cards by task number, so a same-day re-root under a lower
  number sorts ahead of builds already filed. Check both neighbours by hand until the guard is fixed.

## Where work stopped (resume here)

Stopped by the author on 2026-10-12. Nothing is running. Nothing in this block has
shipped and held: task229's design 1 shipped (PR #18) and failed the portal's determinism QC.

**task229: architecture 3 (the number's last), paused mid-draw.**
- Branch `perssathya/task229-rework` at d0ce2fb.
- Designs 1 (firmware read health) and 2 (3PL stock-record accuracy) are spent. Design 2's round 1 was
  landed (proxy 97.9, every ask cracked), and its hardening loop 1 found no rung.
- Architecture 3 has a partial paper draft in `task229/DESIGN_NOTE.md`, under `## Architecture 3
  draft`: a city's permanent cycle-counter network (Urban & Regional Science). Counter capture falls as
  the flow rate rises, and traffic signals upstream bunch cyclists into short green-phase bursts, so a
  capture curve applied at the average rate passes counting points that fail.
- It has the draw, the default path, the stump sentence, the three rules and the deletion tests. The
  card is drafted but unregistered.
- **Resume:** a fresh designer finishes phase A under the improvise rules: screen, fork table, ladder,
  closure, literal reader, oracles, asks, prompt.txt, work order. It checks the card against the three
  cards before it on its registration day, registers, and gets precut.py to exit 0. Then the builder,
  the leak read and clone pre-flight together, and the solver.

**task230: architecture 2, round 1 held the main call; the ask-layer rebuild is not started.**
- Branch `perssathya/task230-event-volume-drop` at 7110c49.
- World: Tamralipta Data Services, a claims-capture centre in Kolkata (Human Factors & Ergonomics).
  Decisive step: first-pass detection falls as errors in the shared pool get rarer, the low-prevalence
  effect.
- Round 1 (Opus high) missed the call (proxy 62.7), but the asks leaked (5 of 6 items cracked, ask
  share 92 per cent).
- Author's decisions on 2026-10-12: waive the organisation-family ban (professional_services) against
  task445 only, and rename the deciding forum (committee_or_panel) to clear task446.
- **Resume, from `task230/pipeline.json`:**
  - The steps are in `paused.resume`, and the deferred list is in the last `solver_rounds` row.
  - A designer rebuilds the asks against round 1's cracker path.
  - It fixes QCP-04 4.1 to "the stream's own documents" and adds the SF row.
  - It applies the two furniture decisions and registers.
  - Then come the builder, a new leak read, a fresh solver round, 6b, the judge, and ship.

**task228: paused by the author.**
- Branch `perssathya/task228-guardrail-alert-metric` at 9120146.
- Design 1 (experiment-platform paging alert): its round-2 pass was on an earlier cut, and it failed
  the domain-coupling rule when revived.
- Design 2 (soil-moisture collocation) is spent: rounds 3 and 4 landed.
- Design 3 and design 4 (granted as an exception) found no architecture. Data-health estimator choices
  key G12 or G16, which task181, task182, task445 and task446 hold in the ban window.
- The card on file is design 2's.
- **Resume:** once task229 or task230 ships, a designer redraws architecture 4. It works under a G16
  waiver if the author grants one then, or without one if the window has moved.

**Approved by the author but not started.** Fix `guard.py`'s draw order on `main` so same-date cards
sort by registration time, and check that no shipped build's verdict changes. This is shared tooling:
PR it under `perssathya/skills-<slug>`.

**Lessons from this run.**
- Seven in-house rounds landed on reflex corrections or visible symptoms:
  - the comparison pool held to the engagement segment, then to eligible phones (task230 design 1);
  - collocation, then a second-station independence check (task228 design 2);
  - accrual since the last count, seen in the data (task229 design 2).
- The one that held (task230 design 2) used a domain effect the solver never modelled.
- The solver's hygiene executes these ask devices, so they are spent:
  - repeated-row dedup, and minutes logged per session;
  - change files over base lists, unit conversions and closed days;
  - effective-dated maps, and UTC against contract zones;
  - latest reviews, and band and indexation rules.
