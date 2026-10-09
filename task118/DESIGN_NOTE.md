# task118 · Which desk gets the headline squad, net of the tests each desk already runs (realises analytical_tasks note OS01)

Source note: `analytical_tasks/04_opportunity_sizing/OS01_headline-squad-renderable-click-share.md`. The note is the idea and this build is its first realisation. Its decision and world are kept; its decisive rung is kept as rung 3, and a new decisive rung sits above it because the fingerprint guard blocks the note's own (see Changes and Tried and rejected).

## Draw

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? yes, registered 2026-10-09 after checkpoint A (go)   Verdict: PASS
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

Design-stage changes (this stage), each with its reason in Settlements or Tried and rejected:

11. Answer: **Culture·national**, 1,250,000 extra clicks in 2027 (unrounded target 1,252,000), runner-up Local·metro at 800,000 (808,000 unrounded), gap 450,000 (444,000 unrounded).
12. Every click figure graded to the nearest 50,000, not the note's 10,000.
13. The shape-09 chain stays whole in the golden workbook and in the chart, but the prompt grades only its terminal stage per desk; the intermediate stages are not requested figures.
14. Ask layer re-cut for H18: the note's ask A (headline corrections) kept as the standards exposure; ask B (newsletter click-to-open) retired; ask C (every rung basis) retired, its back-test half kept; a readers block added that answers the prompt's one belief.
15. The self-serve tool's tests enter the archive from the October 2025 web CMS migration; the squad's tests come from the app testing engine since 2019.
16. The 2027 plan holds every desk at the twelve months to September 2026.

Build-stage changes (stage 3), each with its reason in the Build record or Tried and rejected:

17. Golden prior: one normal prior fitted by maximum likelihood on every package. DerSimonian-Laird converges on it; the unweighted method of moments is refuted on the change log (2 of 7, worst 6.4%).
18. Ship rules: the national CMS instance and the app engine ship a variant that beats the control at 95 per cent one-sided; the Brisbane instance ships the leading variant once it is 80 per cent likely (z above 0.84). The tiny, gated Brisbane tests are what give Sport·metro and Politics·metro their raw lifts.
19. One true-lift distribution for every headline variant (mean -1.0%, sd 4.5%), web and app alike; desks differ by sample size, variant count and ship rule only.
20. Sport·metro: raw 10.81%, shrunk 0.39% (the design's 3.08% shrunk lift cannot coexist with an 11% raw lift under one distribution); rung-4 figure set to 100,400 (graded 100,000), planned clicks 104,669,888, rung 1 at 1.56x.
21. Politics·metro: 210 short tests, raw 7.85%, so the Politics dashboard figure is 4.69%.
22. Culture·national: 50 longer tests (about 6,200 clicks per package), raw 2.22%, shrunk 1.78%, factor 0.80 (designed 0.70), which keeps the dashboard-plus-netting cell on Politics·national (1.30x).
23. The squad's embeddings: app raw lifts 2.7% to 3.7% (designed 3.0% to 7.9%, unreachable under one distribution and a 95% gate), factors 0.26 to 0.77 as designed; twins #3 and #6 at 60 tests, 2.9%, 48.0M, realised 2.00x apart. Embedding #7's twelve October to December 2025 tests sit on base-year Wellness items in the spine.
24. Ask layer: HZ5 added (documents carried across at the 1 October 2025 CMS migration), on every desk's three correction figures.
25. Panel section codes re-cut so the careless current-code join pulls a section of a very different size; it moves extra per reader at five desks.
26. Readers targets moved to keep extra per reader mid-bin: Culture·national 1,412,000, Local·metro 617,000.
27. Pack: nineteen files in eight formats, named as in the Build record; the referee is a .docx bulletin and the social layer an .eml thread.
28. Write-up stage: Corey Cox's last message in the thread signs with his name and title, because the bare sign-off "Corey" above the quoted "On Thu" line read to `guard.py surface` as a second persona ("Corey On") sharing his first name; only the .eml and its bytes in metadata.json moved.

Hardening loop 1 changes (after solver round 1), each with its reason in the Build record or Tried and rejected:

29. The ask layer rebuilt on four silent primaries, with the main path untouched (its files are byte-identical to the pack round 1 solved): K-auto, drafts saved while an article is live, some already carrying the corrected headline ahead of the save that publishes it; K-entry, a live-blog entry's headline fixed in the entry under a note added to the blog; M1, scheduled articles the CMS published at `publish_at` with no save at that minute; R-back, the November 2025 to February 2026 history release issued on the 2026 section list. The stage-3 devices stay as hazards.
30. Organs: the export notes gain `publish_at` and the status line "Status recorded with the save", and the `doc_type` line says a post has a headline of its own; policy 7.4 reads "A headline correction is logged on the revision that publishes the corrected headline" and 7.5 covers live-blog entries; the panel workbook's release log carries R26-04H.
31. The referee made a false clean (measured trap #13): no fix carried ahead by a draft and no entry fix falls between 26 February and 3 April 2026, so the round-1 path ties to the bulletin's March figures (11 headline, 22 text) exactly as the standards rule does, and the two part at every desk over the year.
32. Golden medians moved to 86, 55, 89, 47, 102 and 119 minutes (Politics·national, Sport·metro, Business·national, Sport·national, Local·metro, Culture·national); counts, rates, readers and every main-path figure keep their stage-3 values.

## Gate G

**Gate G line.** decomposition_attribution (G5 netting over a G8 reachable base), with method_or_model_selection at rung 2 · surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no · the deletion test passes · not a lens swap.

- **Litmus.** No. Every figure in the pack is correct and nothing a stakeholder says about their own numbers is overturned: the dashboard's vertical averages, every test and package in the archive, the change log's realised gains, the click-source log and the 2027 plan all recompute. The difficulty is constructing what the squad would add over what each desk's own editors already achieve, a counterfactual increment that no file states and that the closed record cannot see.
- **Primary mechanism.** decomposition_attribution: each desk's sized gain splits into the part its own tests already bank (in the plan) and the part still available to the squad; the answer is the second component, built through a join to a different entity (the test's owner and the owner's team).
- **Deletion test.** Delete Kayla Torres's view, the experimentation lead's note, the editor-in-chief's dashboard basis and the dashboard export. The archive still ranks the desks by lift times clicks, the change log still certifies shrunk lift times planned clicks on seven desks with no self-testing, the field dictionary still makes the platform-drawn clicks the natural reachable base, and nothing says that a desk's own tests already bank part of that gain. Still hard.
- **Instrument repair, three depths.** Fill the gap: no main-path file is incomplete (every pageview carries a source, every test its packages and owner, every embedding its realised gain), so the repair is the identity and both the answer and the naive read are unchanged. Correct the semantics: pre-join each owner to its team inside the archive; rungs 0 to 3 still name Politics·national, Sport·metro, Business·national and Local·metro, and the netting is still a construction nobody is told to make (asserted: answer and naive unchanged, answer differs from naive). Replace the instrument: an instrument observing the decision's own quantity would be a closed embedding at a desk whose editors test their own headlines; none happened, so the change log is blind by history and not by defect, and every input the construction needs is already complete in the pack.
- **Lens-swap test.** Rung 3 and the answer are not one population under two lenses. The answer's base is a strict subset (platform clicks on articles carrying no archive test), selected through the owner-to-team join, and it removes 8.3% of Culture·national's rung-3 base and 71.4% of Local·metro's. The naive read is a construction the solver builds, not a figure the pack reports.
- **Pre-draw identity test.** `incremental(desk) = shrunk lift x platform clicks on articles the desk did not test`. The lift is fitted (corpus-certified), the platform class comes from a storage definition, and the untested set comes from a two-entity join; the identity closes over no filed quantity, and the term neither filed nor forced by any symptom is the untested set.
- **First-moves test.** The one-period group-by (desk lift times clicks) names Sport·metro; decomposing the closed embeddings (shrinkage) names Business·national; the natural reading of the charter's "incremental article clicks" (lift times clicks) names Business·national; the corpus back-test returns 7 of 7 for shrunk lift at rungs 2, 3 and 4 alike and refutes only the raw lift. None lands on Culture·national.
- **Corpus-direction test.** Under the natural path (rung 3, and rung 2) the corpus reproduces 7 of 7 within 2 per cent; it refutes only rung 1. It nets toward nothing and hands no direction to search in.

## Entity, unit of value and decision

**Entity.** Bightline News places one headline-testing squad for a calendar year and the charter scores it on the incremental article clicks it adds in the twelve months after it embeds, counted at the owning desk.

**Two quantities that both read as size.** A desk's winning lift times all its planned clicks (the measured gain) and its winning lift times the platform clicks on headlines its own editors do not already test (the gain still available). They rank the desks differently because the desks with the most platform clicks per click planned are the desks whose editors already test the headlines carrying them: Local·metro has 95% of its clicks on platform surfaces and tests the headlines behind 71.4% of those.

**Decision.** Exactly one desk from {Politics·national, Sport·metro, Business·national, Sport·national, Local·metro, Culture·national} for the squad's January to December 2027 embedding, with its incremental clicks for 2027. Shape from stumping Part 2: which of N gets one scarce thing.

**Forward facing.** The call commits to clicks in a year that has not opened; the objective stays Opportunity Sizing because the work is building the addressable pool (planned clicks) down to what the squad can realise (platform clicks on untested headlines times a certified lift), and that sizing drives the pick.

## Answer

**Culture·national, 1,250,000 extra article clicks in 2027** (unrounded target 1,252,000, mid-bin with 27,000 below and 23,000 above). Rank on the natural pipeline (rung 0): **5th of 6** (4th within 1.5% of Local·metro, so 4th or 5th under either tie-break). Margin over the runner-up Local·metro (808,000): **1.55x**, gap 444,000 unrounded, filed as 450,000.

## The ladder

Five rungs. Each rung is a complete pipeline, reproduces from the raw files, names a different desk, and falls to one shipped fact.

| Rung | Gap of the correction that reaches it | Construction | Names (margin) | Killed by (one shipped fact) | Why a careful analyst stops here |
|---|---|---|---|---|---|
| 0 | (natural pipeline) | The dashboard's average winning lift for the desk's vertical x the desk's 2027 planned clicks | **Politics·national** 16.87M (1.61x over Sport·national 10.50M) | The charter's shortlist names desks by vertical and edition and the archive carries each test's desk; the Politics vertical figure (4.02%) is carried by Politics·metro's 130 small tests at 8.3%, while Politics·national's own tests average 1.30% | It is the programme's own figure on the plan's traffic, the basis the editor-in-chief's office presents, and it agrees with the head of audience's readers view |
| 1 | population (G2) | Each desk's own average observed winning lift from the archive x planned clicks | **Sport·metro** 8.80M (1.22x over Business·national 7.20M) | The change log: raw lift x planned clicks overstates all seven closed embeddings by 1.30x to 3.57x (0 of 7 within 2%) | The right grain from the raw tests, and every shipped winner cleared significance ("a winner is a winner") |
| 2 | rule (G16) | Empirical-Bayes shrunk winning lift (one prior fitted on every package) x planned clicks | **Business·national** 6.12M (1.27x over Politics·national 4.81M) | The field dictionary's `canonical_headline` (stored at publication and carried in feeds, search and social metadata, newsletters and alerts) with the click-source log: 72% of Business·national's clicks start on surfaces that show the stored headline | Selection bias removed and certified by every closed embedding, 7 of 7; Business's large steady tests resemble embedding #3, the biggest realised gain on file |
| 3 | objective (G8, pattern C) | Shrunk lift x the 2027 clicks that start on platform-drawn surfaces (home, section fronts, app feed, related links) | **Local·metro** 2.82M (1.65x over Business·national 1.71M) | The archive's test owners joined to the newsroom staff list: every test behind Local·metro's lift was run by Local·metro's own staff, on articles carrying 71.4% of its platform clicks, and those winners already ship inside the clicks the plan carries forward | It finds the stored-headline fact the dictionary hides in a sentence about storage, it has beaten the readers decoy, the dashboard and the winner's curse, and the change log still reproduces 7 of 7 under it |
| 4 | objective (G5) | Shrunk lift x 2027 platform-drawn clicks on articles whose headline the desk's own editors did not test | **Culture·national** 1.252M (1.55x over Local·metro 0.808M) | (answer) | |

"A solver who does everything right up to rung 3 commits to Local·metro at about 2,800,000 extra clicks."

- Every rung names a different desk: yes (A, B, C, E, F). Rung carrying the stump: 4.
- **Seven survival properties of rung 4.** (1) Written in no shipped sentence: no document says the desk's own tests bank the gain, that a headline carries one test, or that the squad's increment is over the desk's testing; the charter says only "incremental article clicks ... counted at the owning desk". (2) No corpus nominates it: in all seven closed embeddings the untested share is 1.000. (3) No arithmetic symptom: owners all resolve, one test per article, every total ties under rungs 3 and 4. (4) Not a row predicate: it needs a property of a different entity (the owner's team) behind a join nothing signposts, aggregated click-weighted per desk. (5) Its enumeration is arithmetic over about 42,000 articles and their platform pageviews, with no column carrying it. (6) No cutover date: the web tests begin on the first day of the click year, so no series steps inside the window. (7) Survives the deletion above.
- **Worth of each rung on the graded quantity** (Culture·national's figure): rung 0 to 1, 0% (its vertical is its desk); 1 to 2, -30.0%; 2 to 3, -50.0%; 3 to 4, -8.3%. On the name, rung 3 to 4 removes 71.4% of Local·metro's figure.
- **Sign direction.** Every correction walks Culture's figure down; the answer is the minimum of Culture's figures across all 48 grid cells, so no half-applied construction reaches it from outside (proven-in-production L5).
- **Hardening loop 1: unchanged and re-asserted.** Round 1's plain solver stopped at rung 3 exactly as the stump sentence says and named the netting before declining it ("I also did not net off the testing the web desks already do themselves"), which stumping Part 10 reads as the decisive step refused, working as built. The loop changed one mechanism, the ask layer, so round 2 stays attributable; the main-path files are byte-identical to the pack round 1 solved and every rung, position, dominance and grid assertion re-ran green.

## Position table

| Rung | Leader (margin) | Culture·national rank | Behind #1 by |
|---|---|---|---|
| 0 | Politics·national (1.61x) | 5th (Local·metro 4th by 1.5%) | 4.33x |
| 1 | Sport·metro (1.22x) | 6th | 2.26x |
| 2 | Business·national (1.27x) | 5th | 2.24x |
| 3 | Local·metro (1.65x) | 3rd | 2.07x |
| 4 | Culture·national (1.55x) | 1st | |

Re-asserted at hardening loop 1 on the rebuilt pack (main path unchanged). Leads no intermediate rung; 2nd on none; no rung margin under 1.15x (the thinnest is rung 1 at 1.22x). Rung 4 order: Culture·national 1.252M, Local·metro 0.808M, Business·national 0.698M, Sport·national 0.648M, Sport·metro 0.602M, Politics·national 0.552M; adjacent desks at least 1.07x apart and the runner-up 1.158x over the third.

## Discriminator dominance

Local·metro carries **2.067x** over Culture·national into rung 4 (2.82M against 1.37M). Culture's edge on the decisive axis, the share of its platform clicks on headlines its editors do not test (0.917 against 0.286), is **3.203x**; 3.203 / 2.067 = **1.550**, above the 1.2 floor. Against Business·national, the rung-2 and rung-3 runner-up: carried 1.255x, edge 2.252x, ratio 1.794.

As built and re-asserted at hardening loop 1: Local·metro carries 2.039x against Culture's untested edge of 3.159x, ratio 1.550; Business·national 1.260x against 2.263x, ratio 1.795.

## Correction grid

Toggles: lift basis (dashboard vertical, desk raw, desk shrunk, vertical-pooled shrunk) x click base (all, all but partner apps, platform-drawn) x netting (none, click-weighted, by article count, only tests whose variant won) = 4 x 3 x 4 = 48 cells, every one computed on paper at the targets below and rebuilt cell by cell in the generator. Leader by cell, netting none / click / count / won-only:

| Lift basis | All clicks | All but partner apps | Platform-drawn |
|---|---|---|---|
| Dashboard vertical | Pol / Pol / Pol / Pol | Pol / Pol / Pol / Pol | Loc / Pol / Pol / Pol |
| Desk raw | SpM / SpM / SpM / SpM | SpM / SpM / SpM / SpM | SpM / SpM / SpM / SpM |
| Desk shrunk | Bus / Bus / Bus / Bus | Bus / Bus / Bus / Bus | Loc / **Cul (answer)** / Loc / Loc |
| Vertical-pooled shrunk | Bus / Bus / Bus / Bus (built; designed Pol) | Bus / Bus / Bus / Bus (built; designed Bus / SpN / Bus / Bus) | Loc / Cul* / Loc / Loc |

\* The vertical-pooled shrunk cell with click-weighted netting lands on the identical call (Culture's vertical is its desk, 1,252,000) and on different figures for Politics·national, Sport·metro and Sport·national, which violate the charter's desk grain; it is a convergent route to the call, not a second answer.

- **Partial corrections priced (L3).** Netting by article count names Local·metro (2.26M, 1.44x); netting only won tests names Local·metro (1.61M, 1.24x); netting all clicks without the platform step names Business·national (3.54M, 1.005x over Politics); netting all but partner apps names Business·national (2.16M, 1.13x); netting on raw lifts names Sport·metro (2.15M, 1.20x); removing only partner-app clicks names Business·national (3.98M, 1.34x).
- **Nearest wrong Culture figure.** 1,297,000 (won-only netting, +3.6%), then 1,348,000 (count netting, +7.7%) and 1,365,000 (rung 3, +9.0%); each sits in a cell naming another desk and in a different 50,000 bin, so reaching it also costs the name.

## Calibration corpus

- **Form.** The change log of the squad's seven closed embeddings (2019 to 2025), each with its desk, start month, tests run, average observed winning lift, the desk's planned clicks for the embedding year and the realised incremental clicks against matched desks, plus every one of the squad's tests and packages in the archive. The open 2026 embedding (Puzzles) is not in it.

| # | Year | Desk (app-exclusive) | Tests | Observed lift | Planned clicks | Shrinkage factor | Shrunk lift | Realised |
|---|---|---|---|---|---|---|---|---|
| 1 | 2019 | Games | 72 | 4.1% | 36.4M | 0.62 | 2.54% | 0.925M |
| 2 | 2020 | Wellness | 54 | 6.3% | 22.8M | 0.45 | 2.83% | 0.646M |
| 3 | 2021 | Puzzles | 60 | 5.2% | 48.0M | 0.77 | 4.00% | 1.922M |
| 4 | 2022 | Recipes | 88 | 3.7% | 41.5M | 0.70 | 2.59% | 1.075M |
| 5 | 2023 | Games | 66 | 7.9% | 39.2M | 0.28 | 2.21% | 0.867M |
| 6 | 2024 | Recipes | 60 | 5.2% | 48.0M | 0.38 | 1.98% | 0.948M |
| 7 | 2025 | Wellness | 58 | 3.0% | 27.6M | 0.74 | 2.22% | 0.613M |

(Realised gains carry measurement noise inside plus or minus 1.5% around shrunk lift x planned clicks; targets above, generator computes forward.)

- **What it certifies.** Shrinkage, the estimator and the click base. Shrunk lift (one normal prior fitted by maximum likelihood on every package; each test's shipped variant shrunk with its own sampling variance; control kept counts as zero; desk lift the test-weighted mean) x planned clicks reproduces **7 of 7 within 2%**, worst case at most 1.6%. Raw lift overstates all seven (1.30x to 3.85x as built, 0 of 7). A per-desk prior reproduces at most 3 of 7 (1 of 7 as built, missing in both directions). Any rule on the change-log columns alone fails the twins. Applying the lift only to clicks after the test concludes (age 2 hours and up) misses all seven by at least 8%.
- **Rival family swept (C2), each asserted with its miss count and worst miss:** raw lift; pooled prior by DerSimonian-Laird (agrees with maximum likelihood within 0.21% on every shortlisted desk but Sport·metro, 1.66% there, and every graded figure in the same bin, so it is convergent rather than refuted); pooled prior by unweighted method of moments (refuted: 2 of 7, worst 6.4%); per-desk prior; per-vertical prior; a global haircut fitted on the corpus; shrink every variant then take the maximum; impression-weighted and click-weighted desk means; post-test clicks only; absolute click-through points x impressions. Every refuted rival misses at least 2 of 7 by more than 3%.
- **Twin pair.** Embeddings #3 (Puzzles 2021) and #6 (Recipes 2024) match on every change-log column a lookup can see: app-exclusive, 60 tests, 5.2% observed lift, 48.0M planned clicks. Realised gains 1.922M and 0.948M, **2.03x apart**, because #3's tests ran on the app home module at large samples (factor 0.77) and #6's on a niche tab (0.38). Only package-level shrinkage separates them.
- **What it is blind to, and why (L1).** In every closed embedding the platform-drawn share and the desk-untested share are both 1.000, because the squad has only embedded with app-exclusive desks, whose items carry no web URL, feed entry, search listing, alert or newsletter, and whose editors were never given the self-serve tool. Rungs 2, 3 and 4 return identical predictions on all seven cases.
- **Resemblance nominates the decoy.** Business·national's tests (large samples, steady lifts) sit nearest embedding #3 on the test profile, and #3 is the largest realised gain on file, so a lookup by resemblance lands on Business·national (rung 2), never on Culture·national.
- **Every rule the golden composes has a breaking case:** shrinkage (all seven), the estimator (the twins, #5), the in-test clicks (all seven), the test-weighted mean (at least two cases). The two rules the corpus cannot test (platform class and netting) are the decisive rungs, and that blindness is the design.
- **No time trend** in realised over planned across the embeddings (non-monotone by year), so no decay rule fits.

## Pins and counter-pins

- **Filed pins.** Charter (governing, level 2): the squad embeds with one desk for a calendar year from January, tests that desk's headlines and ships each winner; it is judged on incremental article clicks in the twelve months after it embeds, counted at the owning desk; the shortlist table names the six desks by vertical and edition; the editor-in-chief's office reviews placement on the dashboard's average winning lift by vertical and will present it at the planning meeting (licensed wrong basis, a basis and an endorsement, no ranking). Field dictionary (level 4, field semantics): `canonical_headline` is stored at publication and carried in feeds, search and social metadata, newsletters and alerts; each source code with a plain description; `desk_code` is the owning desk; winning lift is the shipped variant's click-through over the control's, minus one, and zero when the control is kept. 2027 audience plan (filed model): desk clicks for 2027 held at the twelve months to September 2026, with no change assumed in where clicks come from.
- **Empirical pins.** The estimator (unique survivor family of the back-test, above). The platform share and the untested share are constructions from complete records, pinned by the records themselves.
- **Never filed, by design.** That a headline carries one test (visible only as a property of the archive: no article has two tests), that the desk's own tests bank their gain, and anything naming the self-serve tool in a document the main call reads. The web engine's provenance line says only that its tests start at the October 2025 CMS migration.
- **Counter-pins.** None. Swept at stage 3: no document at any level states lift x all clicks as the squad's measure, and the dashboard basis is recorded as what one office presents, below the charter's metric. Absolute statements are qualified with their grain.

## Settlements of the draw's open items

1. **What the squad adds on a headline its desk already tests.** Three readings: zero (the golden), a second lift stacked on the desk's winner (this is rung 3, the stump), and a squad premium over the desk's lift. Stacking is ruled out by the archive's structure (no article carries two tests) and by the charter's "incremental": the plan's clicks already include the desk's shipped winners. A premium has nothing to estimate it from: the generator draws every test's true lift from its desk's distribution whoever owns it, and the change log certifies that the archive's shrunk lift is what the squad realises per click. Closure C1 by construction, recorded as an axis below. No matched squad-run and desk-run tests ship (Tried and rejected says why), and no filed sentence closes it.
2. **H18 on the note's asks.** Ask A (headline corrections) kept and re-cut as the standards exposure beside the gain at every desk. Ask B (newsletter click-to-open) retired: its answer serves a newsletter decision with the squad call unmade; the email export ships as a distractor. Ask C (each desk under each rung basis) retired: it names the ladder in the prompt and hands the mirror the shallow cells; its back-test half kept as one figure.
3. **A corpus that refutes the naive path.** It does not: the corpus reproduces 7 of 7 under rungs 2, 3 and 4 and refutes only rung 1, which is the shallow rung it exists to certify. Corpus-direction test passed.
4. **The shape-09 chain against the pair ceiling.** The draw's 24 chain criteria would let the mirror (rung 3) keep the platform-clicks and lift stages and the cracker keep all four, which puts the one-cracker pair near 50 before any device. Settled by grading the terminal stage per desk and carrying the chain in the chart and the golden workbook, unrequested. The criteria arithmetic below replaces the draw's.
5. **Rounding.** Admissible prior fits move every click figure by up to 1%, about 12,500 clicks on Culture's figure, so 10,000 bins are not determinate; every click figure is graded to 50,000 and sits at least 15,000 inside its bin.

## Fork grid

Each toggle value outside the answer violates one shipped rule.

| Axis | Losing value | Shipped rule it violates |
|---|---|---|
| Lift grain | dashboard vertical, vertical-pooled | the charter names desks; the archive carries each test's desk |
| Lift method | raw; per-desk prior; per-vertical prior; global haircut; shrink then max; impression- or click-weighted means; absolute points | the change log (each misses at least 2 of 7 by more than 3%; raw misses 7 of 7) |
| Click base | all clicks; all but partner apps | the dictionary's `canonical_headline` (feeds, search, social, newsletters and alerts carry the stored headline) |
| In-test clicks | post-test clicks only | the change log (misses all seven by at least 8%) |
| Netting | none | the archive's owners and the staff list: the desk's own tests already ship their winners inside the plan's clicks |
| Netting weight | by article count | the charter's unit is clicks, so the banked share is click-weighted |
| Netting scope | only tests whose variant won | a desk tests a headline before its result is known; next year's coverage is every headline it tests |
| Base year | any trailing window inside the year | the plan's base year (filed); coverage has no monthly trend (asserted) |
| 2027 base | last year's actuals | converges: the plan holds every desk at the base year |
| Maturity | include running tests or the open embedding | the archive exports concluded tests only; the change log holds closed embeddings only |

## Deliverables and criteria arithmetic

Prompt shape 09: each desk followed from its 2027 clicks to the extra clicks the squad would add, the chain drawn in the chart and carried whole in the golden workbook.

1. `squad_placement_2027.docx` (text, the paper the meeting reads): opens on Culture·national and 1,250,000; the runner-up Local·metro and the gap 450,000; why each other desk loses (golden content, not requested); one script-rendered chart: every desk walked from its 2027 clicks to its extra clicks, ordered by extra clicks, the chosen desk and the runner-up marked, the gap labelled, a title naming the desk.
2. `squad_placement_2027.xlsx` (data, script-written): one row per desk with six graded measures; the chain sheet (planned, platform, platform on untested headlines, lift, extra), unrequested; the back-test sheet with its count.

**Planned criteria.** Recommendation block: the desk, its figure, the runner-up, the gap, and two or three critical components written rung-4-first at stage 3 (Culture's base, Local·metro's 71.4% already tested) = about 6. Instruction-following: two files, a row per desk, the chart in the paper = about 4. Asks: extra clicks per desk 6; average monthly readers 6; extra clicks per reader 6; headline corrections 6; their rate per 1,000 articles 6; median minutes to first headline correction 6; chart parts 5; back-test count 1 = 42. **Total about 52, over the 25 floor.** Distinct findings: the netted sizing, the readers picture, the standards record, the track record. Named-parts visual: yes. Breakdown at an explicit grain: one row per desk. Validity check: the back-test.

**Each ask fails under a wrong analytical path.** Extra clicks per desk: every rung below 4 files six wrong figures. Readers and extra per reader: codes read by period through the section history (round 1's path), every row read on the current list, or the superseded releases kept. Corrections, rate and minutes: every saved revision compared with the one before it, headline changes read only on the document carrying the note, or minutes timed from the first live save, on top of the stage-3 hazards (noted revisions, body corrections, posts as articles). Back-test: a raw-lift path reports 0 of 7.

**Over-determination.** No ask names a lift, a share, a surface or an owner, so the asked figures cannot be solved back for the untested share without the construction itself.

## Ask ledger (supplemental-stumping)

Rebuilt at hardening loop 1. Round 1's plain solver executed every stage-3 device by field or filed rule, so those devices stay only as hazards and the primaries below are constructions no field names.

**Main call's declared row population.** Files: the click-source spine, the test archive, the newsroom staff list, the 2027 plan, the change log, the field dictionary, the charter, the desk register (shared with the asks, carrying no device). Columns: spine `article_id, desk_code, source_code, pageviews` (age band read only for the in-test reading); archive `test_id, article_id, desk_code, owner_staff_id, package_id, variant, impressions, clicks, shipped`; staff list `staff_id, team_code, end_date`; plan `desk_code, clicks_2027`; change log, all columns. Window: October 2025 to September 2026 for the spine, all time for the archive and the change log. Entities: the six desks, plus every package for the prior fit. **Every device and hazard lives in files outside this list** (the CMS revision export and its field notes, the standards policy, the panel export and the panel workbook, the standards bulletin), so the separation is whole-file and the zero-counts are asserted per file; no main-path document mentions revisions, correction notes, posts, restores, autosaves, scheduling, live-blog entries, panel sections, taxonomies or restatements (grep asserted).

| Ask | Figures, unit, rounding | Pool | Construction layer | Device layer: primary; hazards | File path (causal) | Use, and how it enters the call (H18) |
|---|---|---|---|---|---|---|
| 1 Call furniture | runner-up; gap, clicks to 50,000 | A | rung 4 | none | spine, archive, staff list, plan, dictionary, change log, charter | component: the call's comparison |
| 2 Chart | 5 parts | A | rung 4 | none | as ask 1 | component: the call at a glance |
| 3a Row: extra clicks | per desk, clicks to 50,000 | A | rung 4 | none | as ask 1 | component: why each other desk loses |
| 3b Row: readers | per desk average monthly readers, nearest thousand | B | none | **R-back, the history release read on the list it was issued on** (D3); HZ2 restated April to June releases (D2); HZ3 Brisbane edition as its own panel site (metro desks); R1 codes reissued from March 2026 (D7) | panel export, panel workbook (current sections, section history, release log), desk register | component: puts Kayla Torres's measure beside the gain |
| 3c Row: extra per reader | per desk, one decimal | B (both layers) | rung 4 | R-back, HZ2, HZ3, R1 | as 3a plus 3b: 10 files | component: the squad's return per reader at each desk |
| 3d Row: headline corrections | per desk count over the twelve months | B | none | **K-auto, drafts saved while an article is live** (D2) and **K-entry, an entry's headline fixed under its live blog's note** (D7); S1 copied notes (D6), S2 body against headline (D3), HZ1 Brisbane restore (D7, metro desks), HZ5 migration copies (D2) | CMS revision export, its field notes, standards policy, desk register | component: the standards exposure the squad's headlines would sit under |
| 3e Row: rate per 1,000 articles | per desk, one decimal | B | none | K-auto, K-entry; HZ4 posts as documents (D6), never-live documents (D5), HZ1, HZ5, S1, S2 | as 3d | as 3d |
| 3f Row: median minutes to first headline correction | per desk, whole minutes, odd counts | B | none | **M1, scheduled articles the CMS published at `publish_at`** (D8), with K-auto and K-entry; S1, S2, HZ1, HZ5 | as 3d | as 3d: how fast a wrong headline comes down at each desk |
| 4 Back-test | count of 7 within 2% | A | rung 2 | none | change log, archive, plan | audit trail of the method behind the figure |

The workbook row (asks 3a to 3f) is one ask in the prompt, and its causal path touches 13 files (the six construction files and the charter, the desk register, the two panel files and the three CMS and standards files) and more than 15 columns, which is how the span floor is met; the standards measures on their own touch 4 files, stated plainly. No primary family repeats (D2, D7, D8, D3).

**Primaries, organs and root causes.**
- **K-auto, drafts saved while an article is live (counts, rates, minutes).** The CMS saves an editor's unpublished edits to a live article as `draft` revisions while the live version stands: 18.5% to 20.0% of articles at every web desk carry a draft saved after going live, most of them ahead of ordinary updates. Ahead of some headline corrections the draft already carries the corrected headline and the note arrives on the live save that publishes it (13, 3, 10, 15, 11 and 1 corrections at Politics·national, Sport·metro, Business·national, Sport·national, Local·metro and Culture·national); ahead of others the draft carries the headline and the note together. 88 of the 10,303 drafts saved after going live sit within six minutes ahead of a headline correction. Organs: the export notes' status line and policy 7.4 ("logged on the revision that publishes the corrected headline"). Wrong path: compare every revision with the one before it (round 1's path), which never sees a new note and a new `headline_sha1` on one revision for the first kind and logs the second kind minutes early. Root cause: the web CMS's autosave, the same system whose migration and restore feed HZ5 and HZ1.
- **K-entry, live-blog entry headlines (counts, rates, minutes).** A post has a headline of its own (export notes) and under 7.5 an entry's error is fixed in the entry while the note goes on the live blog, so an entry's headline correction is two saves on two documents in one minute: the post's new `headline_sha1` and the blog's new note. 3, 2, 3, 4, 2 and 1 such corrections at the six desks (one more at Politics·metro); three of the four note wordings name no headline. Wrong path: read headline changes only on the document carrying the note, which files the blog's note as a text correction.
- **M1, scheduled publication (minutes only).** 11,868 articles (26.7%) went live when the CMS published their scheduled revision at `publish_at`, with no save at that minute; their first live save is a later edit, and on 398 of the 403 live blogs among them an entry went live before the blog's first live save. 4,021 more were scheduled and then published early by hand, their first live save before `publish_at`. Organs: the export notes' `publish_at` line with the status line. Wrong path: minutes from the first live save (moves every median, never a count or a rate); over-cleaned path: every scheduled article live at `publish_at`, the hand-published ones included (moves the median at Politics·national, Sport·metro and Business·national).
- **R-back, the history release (readers, extra per reader).** R26-04H reran November 2025 to February 2026 on the 2026 content taxonomy and replaces the earlier releases for those months; the 2026 list starts with the March 2026 period (R26-04, "First release on the 2026 content taxonomy", and the section history's `valid_from` of 1 March 2026). Its 36 rows carry 2026 codes against pre-March periods, so the move that resolved R1 at stage 3, mapping every row through the section history by its period, files four months of each desk under another section while every row still joins exactly one history row. Organ: the release log's two notes. Wrong path: codes by period (round 1's path); over-cleaned paths: the history release left out, every row read on the current list.
- **Stage-3 devices, now hazards.** S1 copied notes, S2 body against headline (the `headline_sha1` rule), HZ1 the Brisbane restore, HZ4 posts as documents, HZ5 the migration's carried documents, never-live documents, R1 the March 2026 renumbering, HZ2 the restated April to June releases, HZ3 the Brisbane panel site. Round 1 resolved each by a field or a filed rule, so they set the floor of a careless path and carry no stump.

**Per-ask stops (generator computes each and asserts it outside the golden bin at every desk unless a desk list is given).** Counts: noted revisions; one per corrected article; notes naming the headline; notes naming a headline, title or heading; carried notes counted again; every new note a headline correction; any entry save paired with the note; per document with restored and migrated copies; migrated documents kept. Rates: noted revisions over all documents; posts in the denominator; migrated documents in the denominator; every document in the denominator; one per corrected article; per document. Minutes: first note of any kind; per document with copies; migrated documents kept; every scheduled article live at `publish_at` (three desks). Readers: codes by period through the section history; the current list; the history release left out; the first release per code; the restated release left out; the national site for Sport·metro (Sport·metro only). Partial corrections readings, each off the golden median at all six desks: round 1's path; published states and scheduling handled with entries ignored; published states and entries handled from the first live save (counts and rates right, medians wrong); published states only; scheduling and entries only; scheduling only; entries only. Counts and rates need K-auto and K-entry together; medians need all three.

**Referee (exactly one), a false clean by construction (D9; measured trap #13, validates on one population, applies to another).** The April standards bulletin gives March 2026's headline and text corrections across the seven web desks: 11 and 22. No fix carried ahead by a draft and no entry fix falls between 26 February and 3 April 2026, and no correction sits within 12 hours of a March boundary on either path, so round 1's path and the standards rule both reproduce 11 and 22; over the year they part at every desk (round 1's path counts 31, 13, 26, 23, 21 and 12 against 47, 18, 39, 42, 34 and 14). The lazy count of March noted revisions is 237. The referee confirms the hazards and hands over no primary.

**Pair arithmetic (Part 0), planning weights 38 / 7 / 55, 42 ask criteria at about 1.31 points each.**
- Cracker (lands Culture·national): keeps the recommendation block and instruction-following (45) plus the free block (extra clicks 6, chart 5, back-test 1 = 12 criteria) plus device leakage on 30 device criteria. Mirror (stops at rung 3, Local·metro): keeps r of about 3, instruction-following 7, chart about 1 and back-test 1, plus leakage on the 24 pure-device criteria; it loses the six extra-per-reader figures by construction.
- Simulated by reading (generator, `pair` record). Round 1's path keeps 2 of the cracker's 30 device criteria (extra per reader at Politics·national and Sport·metro, which stays in its bin on the wrong readers) and none of the mirror's: cracker 63.3, mirror 12.6, pair **37.9**. Catching K-auto, M1 or K-entry alone keeps the same figures (37.9 each). Catching R-back recovers readers and extra per reader: cracker 76.4, mirror 20.5, pair **48.4**, the layer's thinnest point (asserted under 50; every other reading asserted at or under 40). With no cracker in the top two the pair is about 13 to 21.
- The pass condition still rests on the ladder holding the field to at most one response on Culture·national, and on device leakage near round 1's path for both top responses. Readers and extra per reader rest on R-back alone once HZ2 and HZ3 are handled, which is twelve of the cracker's criteria.
- The proxy cannot show this layer: `grade.py` splits 58 ask points equally over block 4's five items, so the back-test item alone is 11.6 points and the three paper items carry desk names a wrong response repeats; a mirror on round 1's path scores about 41 to 43 on the proxy whatever the devices do (measured in the scratchpad on the rebuilt pack). The generated rubric grades each figure.
- Reachability (A1): the share of ask weight reachable from the landed call is 12 of 42, so a cracker banks about 0.30 + 0.60 x 0.29 before any device.

## 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | platform-drawn clicks on articles with no archive test; every non-squad test at a shortlisted desk is owned by that desk's staff (leavers carried with end dates) | C1: "any archive test" and "a test owned by the desk's staff" select the same articles and clicks at all six desks (asserted) |
| 2 | Unit of account | one click is one article pageview with its source surface; one desk is the owning desk | C1: every article carries one `desk_code` on all its rows and none changes desk (asserted) |
| 3 | Attribution window | the squad's 2027; clicks in January on December articles cannot carry its winners; the lift applies to every click on a tested headline, in-test hours included | C3: platform clicks on articles older than 7 days are under 1% at every desk, so the edge moves no desk's figure by more than 0.4%, inside its bin; the in-test reading is C2 (misses all seven by at least 8%) |
| 4 | As-of dating | the tester's team at test time | C1: no tester changed team in the window; current and as-of readings classify every test alike (asserted) |
| 5 | Version basis | one vintage of every main-path file | C1: single exports; the dashboard is one trailing-12-month cut |
| 6 | Divisor | the gain is a click count, so no share denominator enters the graded figure; ask rates name their denominators (per 1,000 articles, per average monthly reader) | C1 and the ask wording |
| 7 | Weighting | desk lift is the test-weighted mean of per-test shrunk lifts | C2: impression- and click-weighted means each miss at least 2 of 7 by more than 3% |
| 8 | Window length | desk lifts over every desk-run test (all inside the base year, the web engine's history starts at the migration); coverage over the plan's base year | C1 for lifts (only one window exists); filed base year for coverage, with no monthly trend (asserted) |
| 9 | Boundary inclusivity | "within 2 per cent" in the back-test | C4: shrunk cases at most 1.6% off, every rival's nearest case at least 3.5% off |
| 10 | Rounding path | click figures rounded once, at the end, to 50,000; lifts carried unrounded | bin: lifts rounded to two decimals land every desk in the same bin (asserted); every figure at least 15,000 inside its bin |
| 11 | Tie-break | none needed | C4: adjacent rung-4 desks at least 1.07x apart, runner-up 1.158x over the third |
| 12 | Maturity | concluded tests and closed embeddings only | C1: no test running at the cut; the open 2026 embedding is absent from the change log (asserted) |
| 13 | Order of operations | shrink the shipped variant, then average; netting and the platform filter on the same article rows | C2 for shrink-then-max (misses at least 2 of 7); C1 for netting and filter (they commute) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one test per article, one row per package, no duplicate key on any main-path file | C1 (asserted) |
| 16 | Identity normalisation | staff ids and desk codes share one format across files | C1: every owner resolves, every desk code matches (asserted) |
| 17 | Netting against gross | every desk-tested article netted whatever its result | C4: count-weighted and won-only netting both name Local·metro, and each breaks a stated rule (fork grid) |
| 18 | Dimensional units | relative lift (shipped over control, minus one) applied to clicks | C2: absolute points x impressions misses 7 of 7; clicks are pageviews by dictionary definition |
| 19 | Code semantics | the dictionary's storage definition puts every source code in exactly one class | filed; class sums asserted; the corpus is blind here by design |
| 20 | Integerisation | integer clicks, no allocation | C1 |
| 21 | Scope of a stated clause | "incremental article clicks in the twelve months after it embeds, counted at the owning desk" governs 2027 at one owner per article | C1 |
| 22 | Forward window contents | 2027 is the plan year, held at base-year clicks with no change in where clicks come from, and each desk keeps its base-year coverage | filed (plan) and C1 (no trend in coverage, asserted) |
| + | Prior fit | maximum likelihood on every package | C1: DerSimonian-Laird converges (every graded figure in the same bin, 7 of 7 on the corpus); C2: unweighted method of moments refuted (2 of 7, four misses over 3%) |
| + | The squad on a desk-tested headline | adds nothing | C1 by construction (Settlements 1) |
| + | Published state (asks 3d to 3f, hardening loop 1) | a revision readers saw: a live save, or a scheduled revision the CMS published before any live save; drafts are never published | filed: policy 7.4 ("the revision that publishes the corrected headline") with the export notes' status line; C1 for drafts that carry only an ordinary edit (no reading moves on them) |
| + | Going live (ask 3f) | the first published state: the first live save, or `publish_at` when the CMS published the scheduled revision first | filed: the `publish_at` line; C1: no draft between a scheduled save and its `publish_at`, every CMS-published article's first live save at least a minute after it, an entry live before the blog's first live save on 398 of 403 CMS-published blogs, and a hand-published article's first live save before its `publish_at` (asserted) |
| + | Entry pairing window (asks 3d to 3f) | an entry's headline fix and the blog's note in the same minute | C1: windows of 0, 1, 5, 10, 20 and 30 minutes file the golden count at every desk (asserted) |
| + | Section list per panel release (asks 3b, 3c) | each release read on the list it was issued on, R26-04H on the 2026 list | filed: the release log's R26-04 and R26-04H notes; every row joins exactly one list on either reading, so the notes decide and the arithmetic does not |
| + | Wording of a correction note | wording never decides; the `headline_sha1` rule does | C4: notes naming a headline, title or heading land outside the bin at every desk; 100 of 207 headline corrections carry a note naming none |

## Assertion plan (generator, then the independent verifier)

1. Rung 0 leader Politics·national, margin at least 1.20.
2. Rung 1 leader Sport·metro, margin at least 1.20.
3. Rung 2 leader Business·national, margin at least 1.20.
4. Rung 3 leader Local·metro, margin at least 1.20.
5. Rung 4 leader Culture·national, margin at least 1.45.
6. Adjacent rungs name different desks, re-run after every parameter change.
7. Culture·national 4th or 5th at rung 0, never 1st or 2nd at rungs 1 to 3.
8. Runner-up Local·metro, at least 1.15x over the third desk.
9. Dominance against Local·metro at least 1.2 (target 1.55).
10. Dominance against Business·national at least 1.2 (target 1.79).
11. All 48 grid cells computed, each leader asserted by name; only the answer cell and the vertical-pooled click-netting cell name Culture, the latter with the identical call figure.
12. Partial cells by name: count netting and won-only netting Local·metro; all-clicks and all-but-partner netting Business·national; raw-lift netting Sport·metro; partner-only removal Business·national.
13. Culture's answer figure is the minimum of its 48 cell figures.
14. Culture's nearest wrong figure at least 3.5% away, in another 50,000 bin, in a cell naming another desk.
15. The call figure at least 20,000 inside its 50,000 bin; every desk's figure and the gap at least 15,000 inside theirs.
16. Every extra-per-reader figure at least 0.015 inside its one-decimal bin; every rate at least 0.02; every median at least 0.2 minutes; every readers figure at least 150 readers inside its thousand.
17. Maximum likelihood against DerSimonian-Laird: every graded figure in the same bin, every shortlisted desk but Sport·metro within 0.5%; unweighted method of moments refuted on the change log.
18. Lifts rounded to two decimals: every click figure in the same bin.
19. Back-test: shrunk lift x planned clicks 7 of 7 within 2%, worst at most 1.6%.
20. Raw lift 0 of 7, overstating 1.30x to 3.57x.
21. Per-desk prior at most 3 of 7 (method of moments and maximum likelihood alike).
22. Every other swept rival at least 2 of 7 missed by more than 3%; the post-test reading misses 7 of 7 by at least 8%; family size and worst miss printed.
23. Twins identical on tests, observed lift, planned clicks and desk type; realised 2.03x apart (plus or minus 0.05).
24. Blindness: platform share and untested share both 1.000 in all seven embeddings.
25. Resemblance: Business·national's test profile nearest embedding #3, which has the largest realised gain.
26. No time trend in realised over planned across the embeddings.
27. One test per article across the archive.
28. Every app-desk test has a squad owner; no squad-owned test at a shortlisted desk; every shortlisted-desk test owner is on that desk's team.
29. Desk-tested shares of platform clicks within 0.5 points of target; no monthly trend; every month within 4 points of the year.
30. Spine totals per desk equal the plan's 2027 clicks to the click.
31. Platform shares within 0.5 points of target; every source code in exactly one class; app desks show platform codes only.
32. Platform clicks older than 7 days under 1% of every desk's platform clicks.
33. App desks' first-two-hours share of clicks at least 10% in the base year.
34. Clean-data test with owners pre-joined to teams: answer and rung-3 read unchanged, answer differs from rung 3.
35. Lens-swap test: the answer's base a strict subset of rung 3's, differing by at least 8% of platform clicks at every desk.
36. Separation: zero device and hazard rows in the main-path files; no main-path document contains the device vocabulary.
37. Every ask stop computed and outside the golden bin at every desk it names; the lazy path lands on stop 1 for every ask; seven partial corrections readings, round 1's path first, each off the golden median at all six desks, and each that misses a primary off every count and rate too.
38. Necessity matrix: K-auto, K-entry, S1, S2 and HZ5 move every desk's count, rate and median; M1 moves every median and no count or rate; HZ4 every rate; HZ1 the metro rates and Local·metro's median; never-live documents the metro rates; no device moves a main-path figure.
39. Pair simulation by reading: at or under 40 for round 1's path and for each single corrections primary caught; under 50 for R-back caught; the device asks recompute with every main-path file deleted, so no ask figure moves between the sheets except extra clicks and extra per reader.
40. Over-cleaner: every blanket rule lands on its designed over-cleaned stop.
41. Hygiene battery on every wrong path comes back clean: (doc_id, revision) unique, every parent and restored source resolves, `publish_at` on every scheduled revision and no other, every panel row joins one section-history row by period, the 63 repeated period-site-code keys resolved by the latest-release rule.
42. Corrected-article counts odd at every desk.
43. Pack gates: at least 10 files, at least 3 formats, the spine over 25,000 rows, at least 2 distractors named in `metadata.json`.
44. No shipped artifact ranks the desks on the decision question; the dashboard reports lift by vertical and is labelled as a record of concluded tests.
45. Prompt: no input file name, no trap word, the rounding convention sentence present.
46. Two consecutive builds byte-identical.
47. Device structure (hardening loop 1): the CMS published 20 to 35 per cent of articles at `publish_at`, with hand-published early cases; an entry live before the blog's first live save on at least 80 per cent of CMS-published blogs; a draft saved after going live on at least 12 per cent of articles at every desk, under a quarter of those drafts just ahead of a headline correction; entry fixes per desk as planned; at least one fix carried ahead by a draft at every shortlisted desk; neither kind between 26 February and 3 April 2026.
48. Referee: the bulletin's March figures reproduce under the standards rule and under round 1's path; outside March the two part at every desk; no correction within 12 hours of a March boundary on either path; the lazy March count at least 3x the bulletin.
49. Entry pairing converges for windows of 0 to 30 minutes; at least a quarter of headline corrections carry a note naming no headline, title or heading.
50. Every panel row joins the section history by period and the current list by code, so neither panel reading shows an orphan.

## World-building targets (the numbers the generator asserts)

| Desk | 2027 planned clicks | Raw lift | Shrunk lift | Factor | Desk-run tests | Platform share | Partner-app share | Other stored-headline share | Desk-tested share of platform clicks | Extra clicks 2027 | Avg monthly readers | Extra per reader |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Politics·national | 420M | 1.30% | 1.144% | 0.88 | 205 | 0.19 | 0.55 | 0.26 | 0.395 | 0.552M | 3,180k | 0.2 |
| Sport·metro | 80M | 11.0% | 3.08% | 0.28 | 150 | 0.55 | 0.05 | 0.40 | 0.556 | 0.602M | 470k | 1.3 |
| Business·national | 300M | 2.40% | 2.04% | 0.85 | 700 | 0.28 | 0.35 | 0.37 | 0.593 | 0.698M | 1,760k | 0.4 |
| Sport·national | 350M | 1.50% | 1.275% | 0.85 | 800 | 0.29 | 0.35 | 0.36 | 0.499 | 0.648M | 2,930k | 0.2 |
| Local·metro | 110M | 3.60% | 2.70% | 0.75 | 1,400 | 0.95 | 0.00 | 0.05 | 0.714 | 0.808M | 610k | 1.3 |
| Culture·national | 150M | 2.60% | 1.82% | 0.70 | 50 | 0.50 | 0.25 | 0.25 | 0.083 | 1.252M | 1,440k | 0.9 |

- Planned clicks are design targets in millions; the generator draws non-round values near them and every downstream figure is recomputed forward. Articles published in the base year about 9,000, 2,500, 8,000, 11,000, 7,000 and 4,000.
- Dashboard (test-weighted, trailing twelve months): Politics 4.02% (Politics·national 205 tests at 1.30%, Politics·metro 130 small tests at 8.3%), Sport 3.00% (Sport·metro 150 at 11.0%, Sport·national 800 at 1.5%), Business 2.40%, Local 3.60%, Culture 2.60%. Read as lift alone or as lift x clicks, the basis names Politics·national.
- Platform surfaces: web home, app home feed, web and app section fronts, related links inside articles. Stored-headline surfaces: search, Discover-style cards, partner news apps, social link cards, newsletters, alerts. Direct visits land on the home page, which is not an article pageview.
- Age bands at the click: 0 to 2 hours, 2 to 6, 6 to 24, 1 to 3 days, 3 to 7 days, over 7 days; tests conclude inside the first two hours.
- Corrections, readers and minutes are tuned at generation to the bin margins in the assertion plan.
- Ask-layer parameters at hardening loop 1 (`params.py`), desks in the order Politics·national, Business·national, Sport·national, Culture·national, Politics·metro, Sport·metro, Local·metro: own headline corrections 44, 36, 38, 13, 13, 16, 32 (second corrections 4, 2, 3, 1, 1, 1, 3); entry headline fixes 3, 3, 4, 1, 1, 2, 2 and entry text fixes 4, 2, 6, 1, 1, 2, 3, one per live blog; 36 per cent of articles drawn as scheduled and a quarter of those published early by hand; ahead of a headline correction, a draft carrying the new headline only at 0.34 and headline and note together at 0.20 (0.25 and none of the first kind in the quiet span, 26 February to 3 April 2026); the history release covers November 2025 to February 2026, published 24 April 2026, each section's 2024-list estimate a fixed factor (0.934 to 1.083) of its 2026-list one; a per-desk sub-seed for correction minutes, chosen so every partial reading misses each median by at least a minute.
- The package-level archive may be re-skinned from a licensed real archive at dataset-generation; these targets bind whatever the source.

## Pack plan (dataset-generation builds against this)

Main path: the click-source spine (parquet, about 2.5 million rows, all desks), the package-level test archive (csv), the newsroom staff list with leavers (xlsx), the 2027 audience plan (xlsx), the squad change log (xlsx), the field dictionary (md or pdf), the squad charter (pdf). Dimension: the desk register (csv: desk code, name, vertical, edition, web or app-exclusive), read by the main path and the asks alike and carrying no device. Context: the experimentation dashboard export (csv). Ask files: the CMS revision export for the six desks with its readme (csv plus txt), the standards policy (pdf), the panel monthly export (csv) and one panel workbook holding the section register and the release log (xlsx), the standards bulletin (the referee). Social: the planning thread (eml or md) with Nina Franklin's "a winner is a winner", Jason Anderson's belief that the squad does its best work where tests run big and steady and that a small desk like Culture would waste its year, and Natalie Benjamin's export notes; no voice supports Culture·national. Distractors (named in `metadata.json`): the syndication agreement with the partner news apps and the newsletter performance report; the squad's weekly report from the open 2026 embedding is a third candidate if the file count allows. About 18 files in at least 5 formats.

Hardening loop 1 changed only ask-path files: the CMS export gains `publish_at` (266,549 revisions), its field notes gain the status, `doc_type` and `publish_at` lines, the policy carries 7.4 and 7.5 as filed rules, the panel export gains R26-04H's 36 rows and the workbook's release log its note, and the bulletin's March figures follow the rebuilt record.

## Realism debts

1. App-exclusive desks have a platform share of exactly 1.000; forced by the corpus's blindness; mitigation: app-exclusive items have no URL, feed entry, search listing, alert or newsletter by product design, stated in the desk register.
2. Realised gains sit within 1.5% of shrunk lift x planned clicks even though tests run during the first two hours; forced by C2; mitigation: realised gains are measured against matched desks over a whole year.
3. Culture·national runs about 50 tests a year where the other web desks run 150 to 1,400; forced by dominance (its untested share has to stay above 0.9); mitigation: a features desk whose editors test only their biggest stories, and the squad lead calls it a small desk.
4. The web testing history starts at the October 2025 CMS migration; forced to collapse the desk-lift window fork; mitigation: a real migration, also the root cause of the CMS export's notes.
5. Desk testing coverage is flat month to month from October 2025; forced to close the forward-coverage fork; mitigation: the practice predates the archive's web history.
6. The plan holds every desk flat at the base year; forced to converge plan against actuals; mitigation: initiatives such as the squad are planned on top.
7. Sport·metro's raw winning lift is 11.0% and Politics·metro's 8.3%; forced by the margins at rungs 1 and 0; mitigation: small metro samples and the winner's curse.
8. Modest lifts mean the best desk gains about 1.25M clicks a year, under 1% of its clicks; realistic for headline testing and stated in the paper.
9. No fix carried ahead by a draft and no entry headline fix between 26 February and 3 April 2026 (hardening loop 1), where the rest of the year's rate would put several of the first; forced by the false-clean referee; mitigation: the gap shows only to a reader who already separates the two kinds of draft, drafts carrying headline and note together continue through the span, and entry fixes run one per live blog, a handful a year at each desk.

## Stopping rule

- **At ceiling:** two solver rounds or portal results in which a response lands Culture·national through the owner-to-team netting by different routes. The move then is to re-root the ask, not to repair the mechanism.
- **One more repair:** a single response landing Culture·national licenses one repair aimed at its route (lower the salience of the owner field or the staff list, or deepen the device layer), logged in Tried and rejected with the solver's own sentence.
- **A determinism repair, not a difficulty one:** two responses agreeing on the desk and splitting on the figure.
- **No repair:** a response reaching the call through the vertical-pooled cell (convergent).
- **Watch item for round 2 (hardening loop 1).** Round 1's plain solver named the netting and declined it. A skeptic that takes it puts one response on Culture·national, which the pair arithmetic absorbs (37.9 on round 1's device path, 48.4 if it also catches R-back); two responses on the call fail the build whatever the asks do, and the repair licensed then is the one above (lower the salience of the owner field or the staff list), not another device. A round in which the device asks fall again to field-by-field reading re-roots the ask layer rather than adding a fifth primary.

## Pack gates, portal log, determinism check

- Pack gates (built): 19 files, 8 formats, spine 2,324,291 rows, 2 distractors named in metadata.json; all asserted (Build record).
- Portal log: none yet.
- Determinism check: section A run at the ladder (litmus, mechanism, flags, no ranking artifact, 22 axes, bins, pins, decision pinned and method open, no metric in the prompt's own voice, stump sentence). Section B run at the generator (241 assertions, the independent verifier's 76 checks, two byte-identical builds) and re-run at hardening loop 1 on the rebuilt ask layer (304 assertions, 77 checks, two byte-identical builds, the five ask-layer axes added to the 22-axis table); section C runs at the end.

## Build record

Built 2026-10-09. `python3 task118/generator/build_pack.py` writes `target/` and `metadata.json` and runs the 304 assertions in `generator/checks.py` against the files as written (304 passed). `python3 task118/generator/verify_pack.py task118/target` is the independent verifier: it reads only the shipped files, shares no code with the generator (DuckDB over the parquet, a profile-likelihood prior fit, a walk of each document's published states in the CMS revisions, each panel release read on the section list it was issued on) and passed 77 of 77 checks. `python3 task118/generator/reproduce.py A B` built twice into the scratchpad: the 19 target files and metadata.json byte-identical, target mtimes equal; the task-folder build is byte-identical to both. Rebuilt at hardening loop 1 (same day, after solver round 1): the main-path files are byte-identical to the pack round 1 solved, and only the CMS export, its field notes, the standards policy, the panel export and workbook, the bulletin and the export log changed.

**Answer.** Culture·national, **1,250,000** extra article clicks in 2027 (unrounded 1,252,299, 22,701 inside its bin). Runner-up Local·metro 800,000 (808,110, 1.158x over Business·national); gap **450,000** (444,189). Back-test: the method gets **7 of 7** finished embeddings within 2% (worst 1.16%).

**Rungs** (unrounded clicks; leader's margin over second; Culture's place):

| Rung | Construction | Leader | Margin | Culture | Order |
|---|---|---|---|---|---|
| 0 | dashboard vertical lift x 2027 plan | Politics·national 17,645,513 | 1.71 | 5th, 3,404,153 | SpN 10,297,913; Bus 7,231,821; Loc 3,946,975; Cul; SpM 3,161,031 |
| 1 | desk raw lift x plan | Sport·metro 11,315,780 | 1.56 | 6th, 3,403,273 | Bus 7,243,525; Pol 5,444,476; SpN 5,301,752; Loc 3,952,100; Cul |
| 2 | shrunk lift x plan | Business·national 6,179,145 | 1.28 | 5th, 2,730,971 | Pol 4,812,794; SpN 4,505,856; Loc 2,948,259; Cul; SpM 412,173 |
| 3 | shrunk lift x platform-drawn clicks | Local·metro 2,792,947 | 1.62 | 3rd, 1,369,906 | Bus 1,726,554; Cul; SpN 1,297,878; Pol 913,383; SpM 227,556 |
| 4 | shrunk lift x platform clicks on headlines the desk did not test | Culture·national 1,252,299 | 1.55 | 1st | Loc 808,110; Bus 697,594; SpN 648,293; Pol 552,392; SpM 100,400 |

Lifts (per cent). Dashboard: Politics 4.69, Sport 3.02, Business 2.34, Local 3.44, Culture 2.22. Desk raw: Pol 1.4471, SpM 10.8109, Bus 2.3438, SpN 1.5548, Loc 3.4445, Cul 2.2194. Shrunk: Pol 1.2792, SpM 0.3938, Bus 1.9994, SpN 1.3214, Loc 2.5696, Cul 1.7810. Prior: maximum likelihood on 10,111 packages, mean -1.038%, sd 4.533%. Platform share and desk-tested share of platform clicks: Pol 0.1898 / 0.3952, SpM 0.5521 / 0.5588, Bus 0.2794 / 0.5960, SpN 0.2880 / 0.5005, Loc 0.9473 / 0.7107, Cul 0.5016 / 0.0859.

Dominance: Local·metro carries 2.039x into rung 4 against Culture's untested edge of 3.159x, ratio 1.550; against Business·national 1.260x carried, 2.263x edge, ratio 1.795. Lens swap: the answer's base is rung 3's base less 8.6% (Culture) to 71.1% (Local·metro).

Grid (48 cells, leaders asserted by name). Culture leads only the answer cell and the vertical-pooled click-netting platform cell (the identical 1,252,299); in every other cell Culture sits at least 1.177x behind the leader. Leaders: dashboard rows Politics·national except platform with no netting (Local·metro); raw rows Sport·metro; shrunk all-clicks and all-but-partner rows Business·national, platform row Local·metro / Culture / Local·metro / Local·metro; vertical-pooled rows Business·national except platform (as the shrunk row). Nearest wrong Culture figure 1,320,818 (won-only netting, +5.5%, bin 1,300,000, a Local·metro cell). Admissible variants landing every desk in the same bin: DerSimonian-Laird (largest move 1.66% at Sport·metro, 0.21% elsewhere), lifts rounded to two decimals, netting on tests owned by the desk's own staff, pre-window articles left out, 7-day-and-older platform clicks left out.

**Change log as built** (avg winning lift, planned clicks, realised): #1 Games 2019, 72 tests, 3.0%, 36.4M, 670,475; #2 Wellness 2020, 54, 3.1%, 22.8M, 325,071; #3 Puzzles 2021, 60, 2.9%, 48.0M, 1,064,693; #4 Recipes 2022, 88, 3.7%, 41.5M, 1,059,784; #5 Games 2023, 66, 2.7%, 39.2M, 272,464; #6 Recipes 2024, 60, 2.9%, 48.0M, 532,067; #7 Wellness 2025, 58, 3.2%, 27.6M, 670,864. Twins #3 and #6 identical on every column a lookup sees, realised 2.00x apart. Business·national's test profile is nearest #3, the largest realised gain.

Rivals (hits within 2% of 7; misses over 3%; worst): raw lift 0, 7, overstating 1.30x to 3.85x; unweighted method-of-moments prior 2, 4, 6.4%; per-desk prior 1, 6, 18.7% (maximum likelihood 1, 6, 15.4%); per-vertical prior 0, 6, 16.7% (3, 4, 15.0%); per-embedding prior 1, 5, 27.8% (2, 5, 29.0%); global haircut on raw lift (k 0.581) 0, 7, 123.9%; shrink every variant then take the maximum 0, 7, 75.0%; impression-weighted 2, 4, 16.6%; click-weighted 2, 5, 21.2%; post-test clicks only 0, 7, misses every case by 16% or more; absolute click-through points 0, 7, 92.2%. DerSimonian-Laird 7 of 7 (convergent). Fourteen rules swept.

**Asks** (graded figure, unrounded):

| Desk | Extra clicks | Avg monthly readers | Extra per reader | Headline corrections | Rate per 1,000 articles | Median minutes |
|---|---|---|---|---|---|---|
| Politics·national | 550,000 (552,392) | 3,180,000 (3,180,260) | 0.2 (0.1737) | 47 | 5.2 (9,007 articles, 5.2182) | 86 (43 corrected) |
| Sport·metro | 100,000 (100,400) | 470,000 (470,290) | 0.2 (0.2135) | 18 | 7.3 (2,463, 7.3082) | 55 (17) |
| Business·national | 700,000 (697,594) | 1,760,000 (1,760,310) | 0.4 (0.3963) | 39 | 4.9 (7,937, 4.9137) | 89 (37) |
| Sport·national | 650,000 (648,293) | 2,931,000 (2,930,720) | 0.2 (0.2212) | 42 | 3.8 (11,043, 3.8033) | 47 (39) |
| Local·metro | 800,000 (808,110) | 617,000 (616,760) | 1.3 (1.3103) | 34 | 4.9 (6,941, 4.8984) | 102 (31) |
| Culture·national | 1,250,000 (1,252,299) | 1,412,000 (1,412,240) | 0.9 (0.8867) | 14 | 3.6 (3,883, 3.6055) | 119 (13) |

Referee, a false clean: the April bulletin's March figures (11 headline corrections, 22 corrections to article text across the seven web desks) reproduce from the CMS export under the standards rule and under round 1's path alike; over the year the two part at every desk (round 1's path 31, 13, 26, 23, 21, 12 against 47, 18, 39, 42, 34, 14 at Pol, SpM, Bus, SpN, Loc, Cul); the lazy reading of March gives 237.

Ask stops (Pol, SpM, Bus, SpN, Loc, Cul). Counts: noted revisions 796, 291, 623, 745, 551, 242; one per corrected article 43, 17, 37, 39, 31, 13; notes naming the headline 9, 8, 7, 10, 12, 4; notes naming a headline, title or heading 18, 11, 19, 20, 22, 11; carried notes counted again 107, 42, 79, 111, 71, 33; every new note a headline correction 119, 45, 97, 107, 87, 35; any entry save paired with the note 51, 20, 41, 48, 37, 15; per document with restored and migrated copies 56, 26, 46, 48, 41, 22; migrated documents kept 56, 23, 46, 48, 38, 22. Rates: noted revisions over all documents 51.80, 64.34, 54.71, 30.09, 54.33, 41.72; posts in the denominator 3.15, 4.29, 3.55, 1.74, 3.62, 2.50; migrated documents in the denominator 5.03, 7.04, 4.73, 3.66, 4.72, 3.47; every document in the denominator 3.06, 3.98, 3.42, 1.70, 3.35, 2.41; one per corrected article 4.77, 6.90, 4.66, 3.53, 4.47, 3.35; per document 5.99, 9.81, 5.58, 4.19, 5.46, 5.46. Medians: first note of any kind 160.5, 122.5, 171, 140.5, 191, 141.5; per document with copies 67, 40, 76, 42, 58, 67; migrated documents kept 67, 41, 76, 42, 71, 67; every scheduled article live at `publish_at` 68, 43, 80 at Pol, SpM, Bus (the others unchanged). Readers: codes by period through the section history (round 1's path) 2,656,000, 585,000, 2,796,000, 2,537,000, 515,000, 1,917,000 (moves extra per reader at Bus, SpN, Loc, Cul); current list 3,368,000, 464,000, 1,853,000, 2,805,000, 628,000, 1,553,000; history release left out 3,137,000, 472,000, 1,750,000, 2,959,000, 606,000, 1,396,000; first release per code 3,285,000, 493,000, 1,829,000, 3,086,000, 634,000, 1,458,000; restated release left out 3,328,000, 492,000, 1,839,000, 3,058,000, 645,000, 1,475,000; national site for Sport·metro 2,931,000.

Partial corrections readings (count / rate / median). Round 1's path (every revision against the last, first live save, entries ignored): 31 / 3.44 / 53, 13 / 5.28 / 41, 26 / 3.28 / 80.5, 23 / 2.08 / 33, 21 / 3.03 / 60.5, 12 / 3.09 / 79. Published states only: counts 44, 16, 36, 38, 32, 13, medians 59.5, 40, 76, 37, 60, 89.5. Published states and scheduling: the same counts, medians 75.5, 43, 82, 43, 72, 99. Published states and entries from the first live save: the golden counts and rates, medians 61, 40, 83, 41, 67, 100. Entries only: counts 34, 15, 29, 27, 23, 13, medians 61, 42.5, 93, 35, 68.5, 89.5. Scheduling and entries: the same counts, medians 68, 62.5, 93, 43, 86, 99. Scheduling only: round 1's counts, medians 67, 49, 82, 37, 68.5, 79. The nearest partial median to a golden one is 4 minutes off (Business·national 93 against 89, Sport·national 43 against 47).

Necessity matrix: K-auto, K-entry, S1, S2 and HZ5 each move every desk's count, rate and median; M1 moves every median and no count or rate; HZ4 moves every rate; HZ1 moves Sport·metro's and Local·metro's rates and Local·metro's median; never-live documents move the two metro rates. No device moves a main-path figure, and the readers, corrections and main-call figures each recompute with the other paths' files deleted. Device counts: 11,868 articles published by the CMS at `publish_at` (26.7%), 4,021 published early by hand; fixes carried ahead by a draft 13, 3, 10, 15, 11, 1; entry headline fixes 3, 2, 3, 4, 2, 1; drafts after going live on 18.5% to 20.0% of articles at every web desk; entry pairing converges for windows of 0 to 30 minutes.

Pair simulation (planning weights 38 / 7 / 55, 42 ask criteria, r = 3), by reading. Round 1's path: cracker 63.3 (2 of 30 device criteria), mirror 12.6 (none), pair **37.9**. K-auto, M1 or K-entry caught alone: 37.9 each. R-back caught: cracker 76.4 (12 of 30), mirror 20.5 (6), pair **48.4**, asserted under 50 and recorded as the layer's thinnest point. At stage 3 the same filed-rules reading put the pair at 38.0 on paper and round 1 then kept every device figure, which is why the primaries moved to constructions no field names. `grade.py`'s proxy cannot see the layer: a mirror on round 1's path scores about 41 to 43 there whatever the devices do (Ask ledger).

**Pack.** Nineteen files, eight formats; spine 2,324,291 rows. Main path: `pageviews_by_source_age_2025-10_2026-09.parquet` (spine), `headline_tests_archive_2019-2026.csv` (14,131 package rows; 3,515 web and 505 app tests), `newsroom_staff_list_2026-10-12.xlsx`, `audience_plan_2027.xlsx` (filed model), `headline_squad_change_log.xlsx` (calibration), `audience_warehouse_field_reference.md` (dictionary), `headline_squad_2027_placement_brief.pdf` (governing: the pin and the licensed dashboard basis), `desk_register.csv`. Context: `experimentation_dashboard_export_2026-10-01.csv`. Asks: `cms_revisions_web_desks_2025-10_2026-09.csv` (266,549 revisions) and `cms_revisions_export_fields.txt`, `editorial_standards_s7_corrections.pdf`, `panel_monthly_audience_2025-10_2026-09.csv` and `panel_reference_workbook.xlsx`, `standards_bulletin_2026-04.docx` (referee). Social: `squad_placement_thread.eml`. Distractors (named in metadata.json only): `newsfold_syndication_agreement.pdf`, `newsletter_performance_2026-07_2026-09.csv`; every graded figure recomputes unchanged with both deleted. Provenance: `audience_data_export_log.csv` (set-equal to the shipped files). Producer audit clean (reportlab comment lines scrubbed with the house script, every other writer set in-fiction); mtimes 16 October 2026 09:00 AEST; no ISO date after 2026-10-19; no em dash. `leak.py` on a scratch copy: REVIEW, no LEAK (ordinary domain words in the field reference and the brief; the prompt's "should join" trips the join pattern). The fingerprint surface screen was not run at this stage.

**Write-up and ship checks (stage 3, 2026-10-09).** `python3 task118/generator/golden.py` reads only `target/` and writes `golden/squad_placement_2027.docx` (the paper: the call, the runner-up and gap, the desk chain chart rendered by matplotlib on a log axis, why the other five lose, readers and corrections table, three notes) and `golden/squad_placement_2027.xlsx` (Desks, Click chain, Back-test, Notes). It asserts every shortlisted-desk test is owned by that desk's staff, spine totals equal the plan, articles equal the spine's base-year articles, odd corrected-article counts, and the correction rule back-tested on the standards bulletin (March 2026: 11 headline and 22 text corrections across the seven web desks, bulletin 11 and 22); it prints the call (1,252,299, 1,250,000), runner-up and gap (444,189, 450,000), 7 of 7 back-test (worst 1.16%, raw lift 0 of 7) and the components (Culture·national shrunk lift 1.78%, platform share 50.2%, desk-tested share of platform clicks 8.6% against Local·metro's 71.1%, untested platform clicks 70,300,000). Every figure matches this record and the verifier's claims. The golden-realism pass ran after the figures froze (figures re-printed unchanged); the producer scrub and a docProps stamp of 19 October 2026 run inside golden.py, and two golden builds are byte-identical. Register pass: H1 clean on target and golden, H4 the golden folder holds exactly the two named files and the chart was opened, H6 the shrinkage rule back-tests 7 of 7 and the correction rule reproduces the bulletin, H8 citations resolve (editorial standards 7.4, the field reference, the Back-test sheet), H11 one submission.md and one prompt.md. After the thread fix: build_pack 241 of 241, verify_pack 76 of 76, leak.py REVIEW (no LEAK, five lines answered below), `guard.py surface` 0 promoted pairs and no people finding, `guard.py heart` PASS (nearest 0.10, task69 v3 lineage), `guard.py validate` 116 cards, 0 invalid.

**Hardening loop 1 (2026-10-09).** Ask layer rebuilt (Ask ledger), `submission.md` step 7 and block 4's six medians rewritten, golden notes rewritten for the published-state and issued-list rules. `build_pack.py` 304 of 304; `verify_pack.py` 77 of 77 (re-run after its docstring was corrected); `reproduce.py` two scratch builds byte-identical to each other and to the task folder (19 target files and metadata.json); two golden builds byte-identical to the task folder's. The golden prints the call, runner-up, gap, back-test and components unchanged and the six workbook rows above, and its March check ties to the bulletin. Register pass: H1 clean on target and golden (the two in-fiction PDF dates, 28 January 2025 and 24 June 2025, match the dates their bodies state); H2 and H3 every figure in the write-up and this note recomputes from the build log or the verifier, and step 7 says "new notes published with a changed headline"; H4 the golden folder holds the two named files; H8 7.4 and 7.5 exist as cited; H9 the export log is set-equal to the other 18 files, with the CMS and panel row counts updated; H11 one submission.md and one prompt.md; H15 the referee computed on round 1's population ties rather than reverses; H16 no date after 2026-10-19. `leak.py` REVIEW, no LEAK (the same five lines, answered below); `guard.py surface` 0 promoted pairs, personas the six on the card; `guard.py heart` PASS (nearest 0.10, task69 v3 lineage); `guard.py validate` 116 cards, 0 invalid. Metadata: 19 files listed with source, date and licence, byte sizes equal to the shipped files, the two distractors named.

**Stage-3 rebuild and ship checks (2026-10-09, after hardening loop 1).** `build_pack.py` 304 of 304; the 19 target files and metadata.json byte-identical to the pack before the rebuild; `verify_pack.py` 77 of 77. `golden.py` re-run from `target/` prints the call (1,252,299, 1,250,000), runner-up and gap (444,189, 450,000), back-test 7 of 7 (worst 1.16%, raw lift 0 of 7), the components (1.78%, 50.2%, 8.6% against 71.1%, 70,300,000), the six workbook rows and the March tie to the bulletin (11 and 22), all as recorded above. The chart palette is an ordered single-hue ramp (four chain stages), checked with the dataviz validator in ordinal mode: all checks pass. Golden-realism pass: the one change is print setup in the workbook (header rows repeat on Desks, Click chain and Back-test; every sheet has a print area, landscape and fit to width, Notes portrait), made in `golden.py`; figures re-printed unchanged, two golden builds byte-identical. Register pass: H1 clean on target and golden with the band 2024-01-01 to 2026-10-19; H2 and H3 every number in `submission.md` traces to the golden print or the paper (three non-figures: a file-name month, a trailing comma, the task number); H4 the golden folder holds exactly the two named files and the chart was opened; H6 7 of 7 and the bulletin tie; H8 clauses 7.1 to 7.8 in the policy, 7.4 and 7.5 cited; H11 one `submission.md` and one `prompt.md`, no backups or snapshots. `submission.md` unchanged (five blocks, every figure re-swept). `leak.py` REVIEW, no LEAK (the same five lines, answered below); `guard.py surface` 0 promoted pairs, personas the six on the card; `guard.py heart` PASS (nearest 0.10, task69 v3 lineage); `guard.py validate` 116 cards, 0 invalid; card answer, spine rows, deliverables and opening move confirmed against the submission and the pack.

## Leak review

`leak.py task118 --asof 2026-10-19`, stage 3 after the goldens and the write-up, again at hardening loop 1 after the rebuilt ask layer, and again on the stage-3 rebuild (pack byte-identical): REVIEW, no LEAK, the same five lines every time. Each line answered:
- 3, `editorial_standards_s7_corrections.pdf`, "7.3": the policy's clause number (section 7.3, how a correction is made), not Sport·metro's rate; the coincidence reveals nothing.
- 3, `headline_squad_2027_placement_brief.pdf`, six of nine call words: the brief states the decision (place the squad, 2027, incremental article clicks) and lists Culture·national as one of six shortlisted desks with no figure or ranking; it is the governing pin and names no desk as the answer.
- 4, `audience_warehouse_field_reference.md`, four stump terms (experimentation, dashboard, source, carries): ordinary field semantics; it defines `owner_staff_id` as who created the test and says nothing about a desk's own tests banking a gain, so it does not name the move.
- 4, `headline_squad_2027_placement_brief.pdf`, five stump terms (newsroom, incremental, experimentation, dashboard, decision): the charter's own wording of the metric and the licensed dashboard basis; no sentence about who runs a desk's tests or netting.
- 5, `prompt.md`, the committed-call sentence: the ask itself (which desk, extra clicks, nearest 50,000), not an announcement of any step.
- Hardening loop 1, read beyond the sweep: the new organs (the status, `doc_type` and `publish_at` lines, policy 7.4 and 7.5, the R26-04H note) are field semantics and filed rules on the ask paths; none says that a draft can carry a headline ahead of its publication, that a scheduled article goes live without a save, or that an entry's headline correction belongs to its desk's count, and the R26-04H note names the 2026 taxonomy without saying that its codes therefore mean something else than the section history gives for those months; no main-path file carries any of their vocabulary (asserted).

## Tried and rejected

- The note's own decisive rung, shrunk lift times platform-drawn clicks (pattern C, gap objective, decomposition_attribution): blocked at the draw by ban.pattern C against task116, test.same_puzzle_older against six builds and test.same_driver_older against task38 v3, and its driver (a reachable share of each candidate's magnitude certified by closed interventions) is task38 v3's and task28 v2's, so it can sit at rung 3 but cannot carry the stump.
- A G7 operating-window rung (a winner earns only on platform clicks after its fixed test window closes, invisible to the evergreen app-exclusive embeddings): blocked by test.same_puzzle (time, G7, pick_one_of_n) against task105 v1, a timing driver the portal already solved, and an in-window same_puzzle takes no differentiation.
- Grading every desk's four chain stages as requested figures (the draw's 24 chain criteria): the rung-3 mirror keeps the platform-clicks and lift stages (12 of 24) and the cracker all 24, so the one-cracker pair sits near 50 before any device ask; only the terminal stage is requested.
- The note's ask B, newsletter click-to-open with privacy-proxy opens: fails H18, because a person could act on it with the squad call unmade; its export ships as a distractor.
- The note's ask C as written, each desk's clicks under each of the four rung bases: names the ladder in the prompt and hands the mirror the shallow cells; only its back-test count survives.
- A workload ask (headlines a week the squad would test) and extra clicks per article: the workload puts each desk's article count beside its test count and nudges toward the netting; a per-article figure at whole-click precision inherits up to 1% of admissible shrinkage spread and cannot be binned.
- The committed figure to the nearest 10,000, the note's rounding: method of moments and maximum likelihood move Culture's figure by up to about 12,500 clicks, more than half a 10,000 bin; every click figure goes to 50,000.
- Matched squad-run and desk-run tests to close what the squad adds on a desk-tested headline: a closed embedding at a self-testing desk would let the change log see the netting and break its blindness, and squad loan tests at a shortlisted desk would blur who ran the tests; closed by construction instead.
- The advertising value of the extra clicks as a both-layer ask: at publisher yields the best desk's gain is worth tens of thousands of dollars against a six-person squad, which raises whether the squad should exist at all.
- A Culture·metro desk inside the Culture vertical to keep the dashboard-plus-netting cell off Culture: read as lift alone, the editor-in-chief's basis then names Local·metro; Politics·metro's raw lift at 8.3% keeps both readings of that basis on Politics·national and clears the cell.
- Method of moments as the golden prior: Sport·metro's and Politics·metro's tiny packages (about 120 clicks) bias the unweighted moments (mean -0.82% against -1.04% by maximum likelihood), Culture's figure moved 3.2% (out of its bin margin) and maximum likelihood failed the back-test 0 of 7; the golden became maximum likelihood, with DerSimonian-Laird convergent and method of moments refuted on the corpus.
- Raising the two small metro desks to about 350 clicks per package so the moment fits agree: the raw-lift netting cell then needs Sport·metro's rung-4 figure near 300,000, which the remaining spread between estimators cannot hold mid-bin, and rung 1 needs a 130M-click Sport·metro.
- Shipping the leader with no gate on the Brisbane instance: Local·metro ships 79% of its tests, its won-only share of platform clicks reaches 0.58 and the won-only netting cell names Culture at 1.07x; the Brisbane gate is 80 per cent (z above 0.84).
- Culture at 2,900 clicks per package (factor 0.70, raw 2.6%) with the gated Brisbane instance: the dashboard-plus-netting cell named Culture at 1.10x; Culture's tests lengthened (factor 0.80) and Politics·metro given 210 shorter tests.
- The design's lifts under one true-lift distribution: Sport·metro at 11% raw cannot keep a 3.08% shrunk lift, and the squad's raw lifts of 3.0% to 7.9% are out of reach through a 95% gate; built at 10.8% / 0.39% and 2.7% to 3.7%, with every ladder margin held through the solved planned clicks.
- The ask layer as designed (S1, S2, HZ1 to HZ4): with the export notes' and the standards policy's rules executed per document, the national desks' correction counts, rates and medians were all right and the pair simulated at 53.6; HZ5 (the migration's carried documents) brings the same reading to 38.0.
- Panel section codes reissued in alphabetical order: the careless join moved readers but left extra per reader in its bin at most desks; codes re-cut so the careless months read a section of very different size.
- Test sizes drawn independently of article size: 561 tests carried more clicks than their article's first-two-hours platform pageviews; tested-article sizes compressed and given an earlier platform profile, and the squad's in-window tests placed on enlarged lead items.
- The ask layer as shipped at stage 3 (S1, S2, HZ1 to HZ5, R1, HZ2, HZ3), round 1 plain solver: it missed the call at rung 3 exactly as the stump sentence says (Local·metro 2,800,000, runner-up Business·national) but scored 46.0 because it kept every device figure, readers, headline corrections, rate per 1,000 and median minutes at all six desks plus the back-test, by executing the filed rules per document in its own words: "merged documents recreated by the 14 Nov 2025 Brisbane restore into their originals. Dropped the 1,704 documents migrated from the old CMS", "a headline correction is a revision that adds a new correction note and changes headline_sha1, following standards s7.4. Notes copied forward to later revisions ... were not counted again", "Mapped section codes to desks through the Section history sheet ... using R26-07B's restated April to June 2026"; every primary and hazard falls to a field or a filed rule the solver reads, so device leakage is near 1.0 against the 0.10 the pair arithmetic needs. It also named rung 4 and declined it ("I also did not net off the testing the web desks already do themselves"), so the rung is visible though not taken.
- Hardening loop 1, the principle under the stage-3 ask layer: every primary and hazard adjudicated by a field or a filed rule on the ask's own path (the copied-note line, s7.4 with `headline_sha1`, `restored_from_doc`, `migrated_from`, `doc_type`, the section history's dates, the R26-07B release note), with two free confirmations beside them, the spine's per-desk article counts and the bulletin's March figures. A solver that reads every field executes each rule per document and then checks itself twice, in its own words "Story and live-blog counts match the article counts in the pageview data exactly" and "March 2026 (AEST) has 12 headline and 31 text corrections, matching the April standards bulletin exactly", so those devices stay only as hazards and the primaries move to constructions no field names: which revision published the headline, when a scheduled article went live, an entry's headline corrected under its live blog's note, and which section list a history release was issued on.
- Hardening loop 1's ask layer (primaries moved to which revision published the headline, scheduled go-live, live-blog entry headlines under the blog's note, and the section list a release was issued on), round 1 re-run as "round 2, plain" (38.0, main call missed at rung 3 on Local·metro 2,800,000 against Business·national 1,750,000): the round passes, but on the rung-3 extra-clicks tokens alone, because the solver again kept readers, headline corrections, rate per 1,000 and median minutes at all six desks plus the back-test, executing every new primary in its own words ("Go-live = first live save, or publish_at for a schedule that fired", "For live blogs, a note added to the blog in the same minute as a post headline change also counts", "Section codes are mapped by the taxonomy of the release ... including R26-04H") and confirming against the bulletin's March figures; device leakage stays near 1.0, so a solver that takes rung 4 keeps the whole xlsx row and the ask layer cannot hold the pair at round 2. It joined `owner_staff_id` to the staff list and saw every web test was desk-run, then declined the netting ("The files do not say whether a squad embedding adds to or replaces a desk's own testing"), so rung 4 is seen and refused, not silent.
- Round 3 (plain and skeptic together) on the hardening-loop ask layer: both missed the call at rung 3 on Local·metro (plain 2,800,000, skeptic 2,400,000 after re-applying the squad's 95% ship rule to every desk, runner-up Business·national 1,750,000 in both), proxies 46.5 and 36.8, average 41.65 with neither under 25, so the round does not pass. Neither path mentions `owner_staff_id` or the staff list this time, so rung 4 was silent and held. The asks did not: both kept readers at all six desks by catching R-back ("mapped section codes by release taxonomy ... 2026 codes for R26-04 onward, including the history release"), the skeptic kept every headline correction count and rate by catching K-auto, K-entry and M1 together ("Built the published sequence ... scheduled revisions at publish_at only if no later save came first ... plus live-blog entry notes matched to a post headline change in the same minute (16)"), the plain solver all but Local·metro's, and both kept the 7 of 7 back-test; only the medians held (timed from the entry going live rather than the blog), and the plain solver's notes list five of the six golden medians as its alternative. Device leakage stays near 1.0 for the second consecutive round, which under the Stopping rule re-roots the ask layer rather than adding a fifth primary.
- Hardening loop 2, the principle under hardening loop 1's ask layer: primaries that were constructions no field names (which revision published the headline, scheduled go-live, an entry's headline fixed under its blog's note in the same minute, the section list a history release was issued on), each still adjudicated by a sentence on the ask's own path that names its own construction (the status line, policy 7.4 and 7.5, the `publish_at` and `doc_type` lines, the R26-04H note "rerun on the 2026 content taxonomy"). A solver that reads every field note writes the construction from the sentence, in round 3's own words "Built the published sequence (live saves at saved_at; scheduled revisions at publish_at only if no later save came first ...) ... plus live-blog entry notes matched to a post headline change in the same minute (16)" and "mapped section codes by release taxonomy (old 2024 codes only for the R25-11 Oct 2025 release; 2026 codes for R26-04 onward, including the history release)", then confirms itself on the bulletin's March figures and the spine's article counts, so readers, counts and rates leaked at 5 or 6 of 6 for the second round running; the medians held only because both solvers timed an entry's fix from the entry going live rather than the blog, a reading choice and not a device. What dies is the organ that states its construction; what the round shows untouched is every assumption the solvers' own path makes and never checks: that a note and the headline fix it records arrive on one save (or one minute), and that the latest release per period is the record for every section in it.
