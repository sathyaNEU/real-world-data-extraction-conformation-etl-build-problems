# task118 · Which desk gets the headline squad, net of the tests each desk already runs (realises analytical_tasks note OS01)

Source note: `analytical_tasks/04_opportunity_sizing/OS01_headline-squad-renderable-click-share.md`. The note is the idea and this build is its first realisation. Its decision and world are kept; its decisive rung is kept as rung 3, and a new decisive rung sits above it because the fingerprint guard blocks the note's own (see Changes and Tried and rejected).

## Draw

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? pending batch registration   Verdict: PASS
  Shape: 09, funnel or chain of stages   Gate G mechanism: decomposition_attribution
  Gap: objective (Gap 3) decisive; rule (Gap 4) at rung 2 and population (Gap 2) at rung 1 below it
  Pattern: none at the decisive rung (G5 carries it); C carries rung 3, B rung 2
  Domain: Marketing & Consumer Research (marketing-consumer-research)   Subdomain (enumerated): media-audience-measurement
  Objective: Opportunity Sizing & Decision Support (opportunity-sizing-decision)
  Pairing repeated from last build? no (task117 is supply-chain-logistics x forecasting, task116 product-analytics x opportunity-sizing-decision)
  Stakeholder role: managing editor, who places the newsroom's one headline-testing squad (operations_director)
  Context-artifact type: filed_model (the 2027 audience plan, each desk's clicks carried forward at last year's source mix)
  Calibration form: realised_outcome_roster (the change log of the squad's seven closed embeddings, realised incremental clicks against matched desks)
  Decision type: pick_one_of_n (named_option), with the desk's sized incremental clicks graded
  Decisive mechanism: G5 provision elsewhere, the gain each desk already banks through its own self-serve tests
  Generators: G5 decisive (rung 4), G8 (rung 3, platform-drawn share), G16 (rung 2, change-log shrinkage), G2 (rungs 0 to 1, vertical against desk)
  Furniture: forum committee_or_panel (the newsroom's planning meeting) · forcing event launch_or_rollout (the squad's January move) · org family media_or_publishing
  World: Bightline News, a national digital publisher with a Brisbane metro edition (Australia, AUD)
  People (guard.py names --geo Australia --seed 118, draw order): Corey Cox, managing editor and requester · Kayla Torres, head of audience,
    the prompt's one belief (the squad belongs where the readers are) · Nina Franklin, experimentation lead · Lisa Jennings, editor-in-chief,
    whose office presents the dashboard basis (the licensed wrong basis) · Jason Anderson, squad lead · Natalie Benjamin, audience data engineer
  Spine (planned): pageviews_by_source_age_2025-10_2026-09.parquet, about 2.5 million rows, one row per article x click-source surface x age band, synthetic
  Deliverables: squad_placement_2027.docx (the call, the runner-up, why the others lose, the desk chain chart)
                squad_placement_2027.xlsx (every desk through every stage, the change-log back-test, the ask tables)
  Opening move: stakes-first
  Criteria arithmetic: 6 desks x 4 chain figures (platform-drawn clicks, drawn clicks on headlines the desk does not test itself,
    shrunk lift, incremental clicks) = 24; call, its figure, runner-up and margin = 4; back-test hits for raw and shrunk lift = 2;
    chart parts = 5; files = 2; 37 before the ask layer
  Repeats from prior builds: none (PASS against 112 filed cards, and PASS with sibling pilot task117 filed first)
As-of date: 2026-10-19
```

**Similarity claim.** No prior build is a one-of-N placement decided by netting out the gain each candidate already banks through its own use of the same intervention; the guard passes it against every filed card and against task117 in draw order, and the nearest driver on file scores 0.10 (task69 v3).

## Stump sentence

A competent solver rebuilds each desk's winning lift from the test archive, shrinks it as the seven closed embeddings require, counts only the clicks that start on surfaces that show the tested headline, and names Local·metro; the step that lands them there is never asking who ran the tests behind each desk's lift, which the archive's test owners joined to the newsroom staff list answer: Local·metro's own editors already test the headlines that carry most of its platform clicks, so most of the gain the squad was sized on is already in the plan.

## Decisive rung

Measured trap: **#13 Validates on one population, applies to another**, decided 3 of the client's 64 measured tasks, 2 of them under 0.50. The change log certifies shrunk lift times platform-drawn clicks on seven desks that had never run a test of their own (app-exclusive desks were never given the self-serve tool), and the solver carries that certified construction to desks whose own editors already test the headlines carrying most of their traffic. Behind it, **#11 Beats the headline trap, misses the quiet one** (4 of 64, 2 under 0.50): a solver who refutes the readers belief, shrinks, and builds the platform-drawn share treats the last step as routine.

Not drawn from the top four: their architecture needs a corpus that refutes the obvious construction, and this ladder keeps the note's blind corpus, so the measured record behind the decisive rung is thinner and the ask layer has to hold the pair.

Open for the design stage: what the squad adds on a headline its desk already tests. Close it by convergence (squad-run and desk-run tests on matched headlines landing on the same shrunk lift), not by a filed sentence, which would make the solver ask the decisive question.

## Nearest exemplars

1. *Staff the FY26 pod on County Sheriffs, whose detention authorities lift the county seat market to 142,288* (Product Analytics, go-to-market vertical selection), measured mean **0.47** (0.44, 0.60, 0.52, 0.42). One scarce team placed on the vertical with the largest serviceable market; the model found the hidden population and still left it out (#5), and read a product closure as a market exit (#23).
2. *Fund LC-12 Time-Deposit Rescue for the Q1 lifecycle budget, not the win-back list* (lifecycle campaign prioritisation), measured mean **0.50** (0.54, 0.58, 0.54, 0.55). One campaign funded on contactable audience times pilot rate; the model beat the headline decoy and mis-built the quiet audience (#11).

Organ neighbour: *Merge the copied prospecting campaigns on 1 July* (paid user acquisition), mean 0.58, prices its effect from seven change-log natural experiments, the same organ form as this build's seven closed embeddings, and the model never used them (#25). Both nearest exemplars sit near 0.5 because the model reaches the right family of construction and loses one quiet step, which is this ladder's bet too.

## Guard

Verdict: **PASS** against the 112 filed cards, and PASS with sibling pilot task117 filed first. No WARN outstanding.

BLOCKs cleared on the way, each by redrawing the axis named:
- ban.pairing (product-analytics x opportunity-sizing-decision, task116): domain moved to marketing-consumer-research/media-audience-measurement.
- ban.pattern C (task116), test.same_puzzle_older (six builds), test.same_driver_older (task38 v3): decisive rung moved to G5; the note's C rung kept as rung 3.
- ban.calibration (pilot_log label, task116): realised_outcome_roster, the label task28 v2 gave the same organ.
- ban.artifact (monitoring_export, task116): the requester works from the audience plan (filed_model); the experimentation dashboard still ships.
- ban.forum (executive_team, task115): committee_or_panel, the newsroom planning meeting.
- test.same_puzzle (time, G7, pick_one_of_n, task105 v1): the operating-window candidate dropped.

WARNs answered:
- people.first (Jennifer, task101): cleared by taking the next names in the seed-118 draw order, not by typing a name.

Batch note: task119, task120, task121 and task122 also declare committee_or_panel, so task118 blocks task119 on forum at registration and those four block one another anyway.

## Changes from the source note

1. Domain: Product Analytics · experimentation-measurement becomes Marketing & Consumer Research · media-audience-measurement, because ban.pairing blocks product-analytics x opportunity-sizing-decision against task116.
2. Decisive rung: the note's rung 3 (shrunk lift times platform-drawn clicks, pattern C) stays as rung 3 but no longer decides. A new rung 4 nets out the gain each desk already banks through its own self-serve tests (G5), because pattern C is banned against task116 and its signature and driver are spent (task25, task26, task28, task35, task38, task53; driver of task38 v3 and task28 v2).
3. Answer: the note's answer Local·metro becomes the stump's wrong answer, and the ladder grows from four rungs to five. The new answer desk and every figure in the note's section 12 are retuned at the design stage.
4. World: desk editors run their own headline tests through a self-serve tool, the archive records each test's owner, and a newsroom staff list maps owners to desks or the squad. App-exclusive desks never had the tool, so the change log stays blind to the new rung as it already was to the drawn share.
5. Requester and voices: the managing editor asks; the note's audience director becomes the head of audience holding the readers belief; the experimentation lead and the editor-in-chief's dashboard basis keep their roles. Personas drawn with the guard; geography set to Australia (the note names none).
6. Context artifact: the requester works from the 2027 audience plan (filed_model); the experimentation dashboard export stays in the pack.
7. Deliverables: three files (`squad_placement.xlsx`, `desk_click_gain.png`, `squad_memo.pdf`) become two (`squad_placement_2027.docx` with the chain chart inside, `squad_placement_2027.xlsx`), avoiding the default PDF, chart and workbook trio and the html+xlsx set sibling task121 already holds.
8. Shape: the note's grid arithmetic (about 63 criteria across four bases) becomes shape 09, each desk's chain stage by stage, 37 before the ask layer.
9. Calibration label: the change log is recorded as realised_outcome_roster.
10. As-of date fixed at 2026-10-19, with a click year of October 2025 to September 2026 (the note gives none).

## Tried and rejected

- The note's own decisive rung, shrunk lift times platform-drawn clicks (pattern C, gap objective, decomposition_attribution): blocked at the draw by ban.pattern C against task116, test.same_puzzle_older against six builds and test.same_driver_older against task38 v3, and its driver (a reachable share of each candidate's magnitude certified by closed interventions) is task38 v3's and task28 v2's, so it can sit at rung 3 but cannot carry the stump.
- A G7 operating-window rung (a winner earns only on platform clicks after its fixed test window closes, invisible to the evergreen app-exclusive embeddings): blocked by test.same_puzzle (time, G7, pick_one_of_n) against task105 v1, a timing driver the portal already solved, and an in-window same_puzzle takes no differentiation.
