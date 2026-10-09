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

## Position table

| Rung | Leader (margin) | Culture·national rank | Behind #1 by |
|---|---|---|---|
| 0 | Politics·national (1.61x) | 5th (Local·metro 4th by 1.5%) | 4.33x |
| 1 | Sport·metro (1.22x) | 6th | 2.26x |
| 2 | Business·national (1.27x) | 5th | 2.24x |
| 3 | Local·metro (1.65x) | 3rd | 2.07x |
| 4 | Culture·national (1.55x) | 1st | |

Leads no intermediate rung; 2nd on none; no rung margin under 1.15x (the thinnest is rung 1 at 1.22x). Rung 4 order: Culture·national 1.252M, Local·metro 0.808M, Business·national 0.698M, Sport·national 0.648M, Sport·metro 0.602M, Politics·national 0.552M; adjacent desks at least 1.07x apart and the runner-up 1.158x over the third.

## Discriminator dominance

Local·metro carries **2.067x** over Culture·national into rung 4 (2.82M against 1.37M). Culture's edge on the decisive axis, the share of its platform clicks on headlines its editors do not test (0.917 against 0.286), is **3.203x**; 3.203 / 2.067 = **1.550**, above the 1.2 floor. Against Business·national, the rung-2 and rung-3 runner-up: carried 1.255x, edge 2.252x, ratio 1.794.

## Correction grid

Toggles: lift basis (dashboard vertical, desk raw, desk shrunk, vertical-pooled shrunk) x click base (all, all but partner apps, platform-drawn) x netting (none, click-weighted, by article count, only tests whose variant won) = 4 x 3 x 4 = 48 cells, every one computed on paper at the targets below and rebuilt cell by cell in the generator. Leader by cell, netting none / click / count / won-only:

| Lift basis | All clicks | All but partner apps | Platform-drawn |
|---|---|---|---|
| Dashboard vertical | Pol / Pol / Pol / Pol | Pol / Pol / Pol / Pol | Loc / Pol / Pol / Pol |
| Desk raw | SpM / SpM / SpM / SpM | SpM / SpM / SpM / SpM | SpM / SpM / SpM / SpM |
| Desk shrunk | Bus / Bus / Bus / Bus | Bus / Bus / Bus / Bus | Loc / **Cul (answer)** / Loc / Loc |
| Vertical-pooled shrunk | Pol / Pol / Pol / Pol | Bus / SpN / Bus / Bus | Loc / Cul* / Loc / Loc |

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

- **What it certifies.** Shrinkage, the estimator and the click base. Shrunk lift (one normal prior fitted by method of moments on every package; each test's shipped variant shrunk with its own sampling variance; control kept counts as zero; desk lift the test-weighted mean) x planned clicks reproduces **7 of 7 within 2%**, worst case at most 1.6%. Raw lift overstates all seven (1.30x to 3.57x, 0 of 7). A per-desk prior reproduces at most 3 of 7 and its misses run high. Any rule on the change-log columns alone fails the twins. Applying the lift only to clicks after the test concludes (age 2 hours and up) misses all seven by at least 8%.
- **Rival family swept (C2), each asserted with its miss count and worst miss:** raw lift; pooled prior by maximum likelihood (agrees with method of moments within 0.5% on every embedding and every desk, so it is convergent rather than refuted); per-desk prior; per-vertical prior; a global haircut fitted on the corpus; shrink every variant then take the maximum; impression-weighted and click-weighted desk means; post-test clicks only; absolute click-through points x impressions. Every refuted rival misses at least 2 of 7 by more than 3%.
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

**Each ask fails under a wrong analytical path.** Extra clicks per desk: every rung below 4 files six wrong figures. Readers and extra per reader: a code join on the current panel register or the superseded releases. Corrections, rate and minutes: counting noted revisions, keeping body corrections, or counting live-blog posts as articles. Back-test: a raw-lift path reports 0 of 7.

**Over-determination.** No ask names a lift, a share, a surface or an owner, so the asked figures cannot be solved back for the untested share without the construction itself.

## Ask ledger (supplemental-stumping)

**Main call's declared row population.** Files: the click-source spine, the test archive, the newsroom staff list, the 2027 plan, the change log, the field dictionary, the charter, the desk register (shared with the asks, carrying no device). Columns: spine `article_id, desk_code, source_code, pageviews` (age band read only for the in-test reading); archive `test_id, article_id, desk_code, owner_staff_id, package_id, variant, impressions, clicks, shipped`; staff list `staff_id, team_code, end_date`; plan `desk_code, clicks_2027`; change log, all columns. Window: October 2025 to September 2026 for the spine, all time for the archive and the change log. Entities: the six desks, plus every package for the prior fit. **Every device and hazard lives in files outside this list** (the CMS revision export and its readme, the standards policy, the panel export and the panel workbook, the standards bulletin), so the separation is whole-file and the zero-counts are asserted per file; no main-path document mentions revisions, correction notes, posts, restores, panel sections or restatements (grep asserted).

| Ask | Figures, unit, rounding | Pool | Construction layer | Device layer: primary; hazards | File path (causal) | Use, and how it enters the call (H18) |
|---|---|---|---|---|---|---|
| 1 Call furniture | runner-up; gap, clicks to 50,000 | A | rung 4 | none | spine, archive, staff list, plan, dictionary, change log, charter | component: the call's comparison |
| 2 Chart | 5 parts | A | rung 4 | none | as ask 1 | component: the call at a glance |
| 3a Row: extra clicks | per desk, clicks to 50,000 | A | rung 4 | none | as ask 1 | component: why each other desk loses |
| 3b Row: readers | per desk average monthly readers, nearest thousand | B | none | **R1 panel codes reissued** (D7); HZ2 restated April to June releases (D2); HZ3 Brisbane edition as its own panel site (metro desks) | panel export, panel workbook (section register and release log), desk register | component: puts Kayla Torres's measure beside the gain |
| 3c Row: extra per reader | per desk, one decimal | B (both layers) | rung 4 | R1, HZ2, HZ3 | as 3a plus 3b: 10 files | component: the squad's return per reader at each desk |
| 3d Row: headline corrections | per desk count over the twelve months | B | none | **S1 correction note carried on every later revision** (D6); S2 body against headline corrections (D3); HZ1 Brisbane restore (D7, metro desks) | CMS revision export, CMS export readme, standards policy, desk register | component: the standards exposure the squad's headlines would sit under |
| 3e Row: rate per 1,000 articles | per desk, one decimal | B | none | S1, S2; HZ4 live-blog posts as documents (D6); HZ1; scheduled-then-pulled documents (D5) | as 3d | as 3d |
| 3f Row: median minutes to first headline correction | per desk, whole minutes, odd counts | B | none | S1 (first appearance), S2, HZ1 (restored copies at minute 0) | as 3d | as 3d: how fast a wrong headline comes down at each desk |
| 4 Back-test | count of 7 within 2% | A | rung 2 | none | change log, archive, plan | audit trail of the method behind the figure |

The workbook row (asks 3a to 3f) is one ask in the prompt, and its causal path touches 13 files (the six construction files and the charter, the desk register, the two panel files and the three CMS and standards files) and more than 15 columns, which is how the span floor is met; the standards measures on their own touch 4 files, stated plainly.

**Devices, organs and root causes.**
- **R1, panel codes reissued.** The industry audience panel renumbered its sections from the March 2026 release and reused old numbers for different sections. Structural antidote: the section register's `valid_from` and `valid_to` with the publisher's desk code per section version; documentary antidote: the release log. Careless path: a join on code through the current register files pre-March months under other sections. Over-cleaning stop: dropping pre-March months (a seven-month average). Silent: every row parses and every join lands.
- **S1, correction note persistence.** The CMS carries `correction_note` forward on every later save until an editor clears it. Antidotes: the CMS export readme (structural: the note text and the first revision carrying it) and the standards policy (documentary: a headline correction is logged on the revision that changes the headline). Careless path: counting revisions with a note (overcounts at least 3x on every desk, most on live-blog desks). Over-cleaning stop: one correction per article (misses second corrections on 6% to 10% of corrected articles).
- **S2, body against headline corrections.** Notes cover both; a headline correction is a new note on a revision whose headline differs from the previous revision's. Careless path keeps body corrections (about 60% of notes); over-cleaning stop keeps only notes whose text says "headline".
- **HZ1, the 14 November 2025 Brisbane restore.** An outage on the Brisbane CMS instance; every metro document live at the time was restored under a new `doc_id` with `restored_from_doc`. Moves the metro desks' counts, rates and minutes. One root cause (the Brisbane edition's own infrastructure) also feeds HZ3, so it reaches two ask groups.
- **HZ2, restated releases.** The panel re-released April to June 2026 about 15% lower after a cross-device duplication fault; the later release is the version of record. Visible to a duplicate-key check, so a hazard only.
- **HZ4, posts as documents.** Live-blog posts are their own documents with a `parent_doc`; posts are not articles. Adds 35% to 120% to a desk's document count.

**Per-ask stops (targets, generator computes forward and asserts each outside the bin).** Readers: code join on the current register / effective dates but original April to June releases kept / pre-March months dropped / national site used for metro desks / answer. Corrections rate: noted revisions over all documents / first appearances with body notes / one per article / posts in the denominator / answer. Minutes: last noted revision / body notes kept / restored copies kept / answer.

**Referee (exactly one).** The standards desk's monthly bulletin gives the shortlisted desks' combined headline-correction count for one month (March 2026), byte-clean; it arbitrates S1 and S2 for a solver who checks and hands over no desk's level.

**Pair arithmetic (Part 0), planning weights 38 / 7 / 55, 42 ask criteria at about 1.31 points each.**
- Cracker (lands Culture·national): keeps the recommendation block and instruction-following (45) plus the free block (extra clicks 6, chart 5, back-test 1 = 12 criteria) plus device leakage L on 30 device criteria. Mirror (stops at rung 3, Local·metro): keeps r of about 3 (a shallow critical component), instruction-following 7, chart about 1 and back-test 1, plus L on the 24 pure-device criteria; it loses the six extra-per-reader figures by construction.
- `55 x (Lc + Ls) <= 28 - r`: at L = 0.10, Lc = 0.357 and Ls = 0.105, so the pair averages **40.2**; at L = 0.12, **40.9**; at L = 0.20, 43.7. With no cracker in the top two (the two best rung-3 responses), the pair averages about **16 to 19**.
- The pass condition rests on three things, said plainly: the ladder holding the field to at most one response on Culture·national; device leakage at or under about 0.10 for both top responses, which is why every primary sits on the silent list; and the generated rubric grading the terminal stage of the chain, not its intermediate stages. If the rubric arrives grading the platform and lift stages, the mirror gains about 12 criteria and the fix is upstream in the prompt, not in this layer.
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
| + | Prior fit | method of moments on every package | C1: maximum likelihood within 0.5% on every desk, every graded figure in the same bin |
| + | The squad on a desk-tested headline | adds nothing | C1 by construction (Settlements 1) |

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
17. Method of moments against maximum likelihood: every desk's shrunk lift within 0.5%, every graded figure in the same bin.
18. Lifts rounded to two decimals: every click figure in the same bin.
19. Back-test: shrunk lift x planned clicks 7 of 7 within 2%, worst at most 1.6%.
20. Raw lift 0 of 7, overstating 1.30x to 3.57x.
21. Per-desk prior at most 3 of 7, misses running high.
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
37. Every ask stop computed and at least one bin outside the golden; the lazy path lands on stop 1 for every ask.
38. Necessity matrix: each device moves its ask figures outside their bins and nothing else.
39. Pair simulation: cracker and mirror sheets with the hygiene battery applied, pair at or under 40 at the measured leakage; no ask figure moves between the sheets except extra clicks and extra per reader.
40. Over-cleaner: every blanket rule lands on its designed over-cleaned stop.
41. Hygiene battery on every wrong path comes back clean.
42. Corrected-article counts odd at every desk.
43. Pack gates: at least 10 files, at least 3 formats, the spine over 25,000 rows, at least 2 distractors named in `metadata.json`.
44. No shipped artifact ranks the desks on the decision question; the dashboard reports lift by vertical and is labelled as a record of concluded tests.
45. Prompt: no input file name, no trap word, the rounding convention sentence present.
46. Two consecutive builds byte-identical.

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
- The package-level archive may be re-skinned from a licensed real archive at dataset-generation; these targets bind whatever the source.

## Pack plan (dataset-generation builds against this)

Main path: the click-source spine (parquet, about 2.5 million rows, all desks), the package-level test archive (csv), the newsroom staff list with leavers (xlsx), the 2027 audience plan (xlsx), the squad change log (xlsx), the field dictionary (md or pdf), the squad charter (pdf). Dimension: the desk register (csv: desk code, name, vertical, edition, web or app-exclusive), read by the main path and the asks alike and carrying no device. Context: the experimentation dashboard export (csv). Ask files: the CMS revision export for the six desks with its readme (csv plus txt), the standards policy (pdf), the panel monthly export (csv) and one panel workbook holding the section register and the release log (xlsx), the standards bulletin (the referee). Social: the planning thread (eml or md) with Nina Franklin's "a winner is a winner", Jason Anderson's belief that the squad does its best work where tests run big and steady and that a small desk like Culture would waste its year, and Natalie Benjamin's export notes; no voice supports Culture·national. Distractors (named in `metadata.json`): the syndication agreement with the partner news apps and the newsletter performance report; the squad's weekly report from the open 2026 embedding is a third candidate if the file count allows. About 18 files in at least 5 formats.

## Realism debts

1. App-exclusive desks have a platform share of exactly 1.000; forced by the corpus's blindness; mitigation: app-exclusive items have no URL, feed entry, search listing, alert or newsletter by product design, stated in the desk register.
2. Realised gains sit within 1.5% of shrunk lift x planned clicks even though tests run during the first two hours; forced by C2; mitigation: realised gains are measured against matched desks over a whole year.
3. Culture·national runs about 50 tests a year where the other web desks run 150 to 1,400; forced by dominance (its untested share has to stay above 0.9); mitigation: a features desk whose editors test only their biggest stories, and the squad lead calls it a small desk.
4. The web testing history starts at the October 2025 CMS migration; forced to collapse the desk-lift window fork; mitigation: a real migration, also the root cause of the CMS export's notes.
5. Desk testing coverage is flat month to month from October 2025; forced to close the forward-coverage fork; mitigation: the practice predates the archive's web history.
6. The plan holds every desk flat at the base year; forced to converge plan against actuals; mitigation: initiatives such as the squad are planned on top.
7. Sport·metro's raw winning lift is 11.0% and Politics·metro's 8.3%; forced by the margins at rungs 1 and 0; mitigation: small metro samples and the winner's curse.
8. Modest lifts mean the best desk gains about 1.25M clicks a year, under 1% of its clicks; realistic for headline testing and stated in the paper.

## Stopping rule

- **At ceiling:** two solver rounds or portal results in which a response lands Culture·national through the owner-to-team netting by different routes. The move then is to re-root the ask, not to repair the mechanism.
- **One more repair:** a single response landing Culture·national licenses one repair aimed at its route (lower the salience of the owner field or the staff list, or deepen the device layer), logged in Tried and rejected with the solver's own sentence.
- **A determinism repair, not a difficulty one:** two responses agreeing on the desk and splitting on the figure.
- **No repair:** a response reaching the call through the vertical-pooled cell (convergent).

## Pack gates, portal log, determinism check

- Pack gates (planned): about 18 files, at least 5 formats, spine about 2.5 million rows, 2 or 3 distractors.
- Portal log: none yet.
- Determinism check: section A run at the ladder (litmus, mechanism, flags, no ranking artifact, 22 axes, bins, pins, decision pinned and method open, no metric in the prompt's own voice, stump sentence). Sections B and C run at the generator and at the end.

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
