# determinism-check report, task122, 2026-10-09

Pass 1, licensed by `/build` stage 6. Scratch: `/tmp/determinism-check-task122-20261009T215046Z/` (`judge_brief.md`, `verdict.md`, work files).

**Run note.** This harness exposes no Agent tool, so the judge brief could not go to an isolated `general-purpose` thread. It ran in the orchestrator's own context under the same allow-list:

- only a fresh copy of `target/` plus the extracted blocks;
- the v3 judge prompt applied as written;
- every figure recomputed with pandas;
- `verdict.md` written before `metadata.json`, `DESIGN_NOTE.md`, `golden/` or anything under `solver_rounds/` was opened.

What this loses against a real thread: the judge had already read the whole `submission.md` (Tags included) and the repo's `CLAUDE.md`. Treat it as a full pass with weaker isolation, and re-invoke in a harness with the Agent tool once the build is rebuilt.

## Verdict
DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: single_conceptual_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: no

## Why
Every committed answer reproduces and is forced once the charter's own definitions are applied:

- **Lift** is all orders the arm's buyers place during the test (charter 2.2). On that basis the velocity boost (HC-33) falls from 7.96 in session to 3.30 by day 6.
- **Carousel order rate** counts every order placed from the arm's tiles (charter 2.4). The field reference's seven-day keep-off rule makes the join exact. On that count the session-sequence model (HC-34) sits 3.77% below Blend v7 in app 0-29.

That leaves HC-37 at 5.70 and HC-33 at 3.30 as the only policies clearing all three launch conditions.

The send-back comes from Gate G, not from Gates A to E. What wins the call is recognising that the logger's in-session reads mislead on the charter's metrics, and flipping away from them. Those reads are `ordered_tiles`, the archive's `in_session_orders`, and Fabian Stoffel's "the log bears it out" case for the velocity boost. That is the banned surface-read-rejection type: a single_conceptual_flip, two links deep, with the taxonomy label banned_stumping_type.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CC1: archive back-test, per-session propensity weights (carousel_experiment_archive.xlsx) | 9 of 9 within 0.25 | 9 of 9; HT, Hajek and post-stratified agree; largest miss T1 7.73 vs 7.9. Rivals: naive 3/9, per-render replay 3/9 (it reproduces the published offline estimates), per-render weighted 6/9 | yes |
| CC2: HC-34 carousel order rate vs Blend v7, app 0-29, every tile order | 3.8% below | 3.77% below (56.51 vs 58.73 per 1,000); on `ordered_tiles` only 0.96% below | yes |
| CC2: HC-31 same, web 730+ | 2.5% below | 2.51% below (56.41 vs 57.86); on `ordered_tiles` 2.74% below | yes |
| CC3: HC-36 fresh tiles per 100, per served ranking | 8.8 | 8.84 (per render 15.59) | yes |
| CC3: HC-39 lift | 1.4 | 1.39 | yes |
| CC4: HC-33 lift over the test vs in session | 3.3 vs 8.0 | 3.30 (identical at every horizon from 6 to 21 days) vs 7.96 | yes |
| CC5 and main call: HC-37 lift | 5.7 | 5.70 (5.68 on the slot's planned cell mix) | yes |
| Notebook ask 1 | HC-37, 5.7 | HC-37, 5.70 | yes |
| Notebook ask 2 | HC-33 3.3, gap 2.4 | HC-33 3.30, gap 2.40 | yes |
| Notebook ask 3, HC-31 (app 0-29 to 730+, then web) | 9.7 10.8 10.6 10.1, 10.9 9.2 11.2 -1.6 | 9.69 10.79 10.59 10.11, 10.91 9.21 11.19 -1.61 | yes |
| Notebook ask 3, HC-33 | 4.3 9.1 2.5 3.1, 1.6 8.4 1.3 2.1 | 4.29 9.11 2.49 3.11, 1.59 8.41 1.29 2.09 | yes |
| Notebook ask 3, HC-34 | -0.7 15.0 15.4 15.8, 9.4 13.3 12.9 15.9 | -0.71 15.01 15.41 15.81, 9.41 13.31 12.89 15.89 | yes |
| Notebook ask 3, HC-36 | 6.4 8.7 7.5 7.4, 2.4 7.4 6.1 4.5 | 6.39 8.69 7.51 7.41, 2.39 7.41 6.11 4.49 | yes |
| Notebook ask 3, HC-37 | 8.6 9.8 7.4 7.4, 6.3 9.7 7.9 6.5 | 8.59 9.81 7.39 7.41, 6.29 9.69 7.91 6.51 | yes |
| Notebook ask 3, HC-39 | 4.5 2.6 2.3 0.8, 0.5 1.9 1.7 1.9 | 4.49 2.59 2.29 0.81, 0.51 1.91 1.71 1.89 | yes |
| Notebook ask 4, HC-31 | 16,500 orders, EUR 22,500 | 16,474.2, 22,511.0 | yes |
| Notebook ask 4, HC-33 | 8,500, EUR 10,100 | 8,518.6, 10,111.7 | yes |
| Notebook ask 4, HC-34 | 25,700, EUR 35,600 | 25,716.0, 35,609.0 | yes |
| Notebook ask 4, HC-36 | 12,900, EUR 17,500 | 12,924.6, 17,513.5 | yes |
| Notebook ask 4, HC-37 | 14,800, EUR 20,500 | 14,789.8, 20,520.0 | yes |
| Notebook ask 4, HC-39 | 3,600, EUR 5,000 | 3,584.5, 4,984.4 | yes |
| PNG ask 2: hatched cells | HC-31 web 730+, HC-34 app 0-29 | the only two cells more than 1.5% below Blend v7 | yes |
| PNG asks 3 and 4: outlined row, title | HC-37, +5.7 | HC-37, 5.70 | yes |
| Context, not claimed: other lifts | n/a | HC-31 6.56, HC-34 9.84, HC-36 5.07 (same in session and over the test) | n/a |

**How the fee grid is built.** It uses tariff KB-2026-02 (0.80 plus 5% of the price paid after an accepted offer still inside its 48-hour window), net of 21% VAT, with every order charged.

**Why every order is charged:**

- Finance's protected orders equal card and iDEAL captures plus every uncaptured shipped order, exactly, by month and platform. So balance-paid purchases are covered.
- Pickup capture goes from about 50% to 7,033 of 7,033 on and after 21 September 2026.

**Every element of the method is decisive.** Each of the following scores 0 of 48 cells: VAT-inclusive fees, asking price, captured orders only, pickups only as captured, historic fees, KB-2027-01.

**How the totals are built.** They use the R2 table for 2026-W01 to W12, the app arm from W03 (release 27.1 on 18 January 2027), and 10% of sessions per cell. First-release bands, ungated app traffic, or an app start in W02 each score 0 of 6. The 0.4% bot-filter adjustment changes no total.

## Competing answers that survived
None. Every fork closed on a shipped rule. These closed, but they are where the build is thinnest:

| Fork | Answers it produces | What closes it |
|---|---|---|
| HC-33 lift: in session vs over the test | HC-33 at 7.96 wins, vs HC-37 at 5.70 | Charter 2.2 and the prompt's "extra orders". Charter 5.2 governs only condition (a), which HC-33 clears either way |
| Guardrail: `ordered_tiles` vs every tile order | HC-34 passes at -0.96% and wins at 9.84, vs fails at -3.77% | Charter 2.4 plus the seven-day rule. The margin is two orders (Finding 4) |
| Fresh share: per render vs per served ranking | HC-36 passes at 15.59, vs fails at 8.84 | `fresh_listing_commitment_2026.docx`: "We count per served ranking" |
| Outcome horizon | 6 to 21 days: identical. 3 days or less: HC-33 leads (6.21). 28 days on fully observed sessions: HC-37 2.08, HC-33 0.31. 42 days: HC-37 -2.53, HC-33 7.50 | Only the extract ending 21 days after the last session, plus the plateau. No document pins the horizon (Finding 3) |
| Estimator | Per-render weighted: HC-33 7.35 beats HC-37 5.78. Replay and naive scores are confounded by cell mix | Charter 5.2 back-test: 9 of 9 only for per-session weights |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in pack | 10 or more | 23 | yes |
| Distinct formats | 3 or more | 9 (csv, parquet, xlsx, docx, pdf, md, txt, json, ics) | yes |
| Large file | one file of 25,000+ rows, or a large database | render log 404,100 rows (orders 366,056, payments 317,519) | yes |
| Distractors declared | 2 or more in metadata.json, none labelled in `target/` | 3 declared (search tests, seller survey, pricing minutes); no name or content labels them | yes |
| Distractors relevant and unused | same world, something a solver weighs | all three unused by the solution. The search tests carry a search velocity boost and a freshness boost; the survey covers fresh listings and pickup; the minutes cover fees | yes |
| Distractor answering a graded figure is ruled out | reproduces, and a shipped fact rules it out | none answers the call or a graded figure; the search lifts are per 1,000 searches under their own charter (charter 1) | yes |
| Deliverable count | 1 to 3 | 2 (ipynb, png) | yes |
| Format family | none required | Code and Visual, not graded | n/a |
| Asks multi-dimensional | no stacked lookups | 6 x 8 fee grid, per-policy totals in two units, runner-up with gap | yes |
| Golden deliverables present | every named golden | both in `golden/`. Notebook executed (12 of 12 cells counted, no errors) and opens on the answer; the PNG carries every PNG ask | yes |
| Unit and rounding stated | inside the sentence that asks | main ask yes. The gap ask has neither. Grid and totals take their rounding from the trailing sentence | partial |
| Prompt shape and 25 criteria | identifiable shape, 25+ | shape 07, grid of cells: 48 cells + 12 totals + call, figure, runner-up, gap + 4 PNG parts = 68 | yes |
| Realism | nothing reads as generated; goldens read as a work product | goldens read as a work product. The pack's order data and the docx and PDF metadata read as constructed (Findings 3 and 7) | no |

## Gate G reconciliation
| Flag | Judge | Design note (Gate G line, marked "unchanged" through harden loop 3) |
|---|---|---|
| mechanism | single_conceptual_flip | decomposition_attribution, with method_or_model_selection at rungs 1 and 2 |
| stumping_family | surface_read_rejection | analytical_non_defect |
| surface_read_dependency | yes | no |
| sole_data_defect | no | no |

Three of four flags disagree. There are two reasons the outside reading differs from the inside one.

1. **The decisive rung moved and the Gate G line did not.**
   - Since harden loop 1 the decisive rung has been the guardrail count. The note files it as its own measured trap #7, "Uses the ready-made measure", and says `ordered_tiles` "is right for what it says".
   - In v3 terms that is single_conceptual_flip ("fails even when the stated number is arithmetically correct and only the lens is wrong"). The post-session orders it misses are the "coverage/join gap" that v3 lists under planted_defect_flip.
   - The note kept its line by widening decomposition_attribution to "each order attributed to the tiles and the test that produced it", and by declaring it not a lens swap. v3's decomposition is a mix vs rate vs volume split of a correctly reported movement, so it will not read it that way.
2. **The note's litmus is false on the shipped pack.**
   - The note says no stakeholder conclusion is overturned and "no shipped artifact ranks the six policies on any basis". It also says there is no roll call because none of the people is a voice in the prompt.
   - `planning_thread_carousel_slot.txt` is that roll call. Fabian Stoffel wants the slot for the velocity boost on what the log shows for its pinned tiles. Kayleigh Zeemans "would not put it up against the velocity boost for this slot". The answer overturns both.

**What it implies.** From the inside the build reads as decomposition. From the outside it reads as a two-link rejection of the logger's in-session read, with a stakeholder pick as bait. This is the mismatch that most reliably predicts a send-back.

**Distractors.** `metadata.json` declares `search_ranking_tests_2026H1.xlsx`, `seller_survey_fresh_listings_2026Q2.csv` and `pricing_committee_minutes_2026-10-06.docx`. The judge named none of them as the surface read, so there is no too-load-bearing-distractor finding. The artifact that does rank the candidates wrongly, the planning thread, is undeclared, and it cannot be declared: it is the bait the stump runs on, and a declared distractor is never the stump.

## Stump power (Gate F)
Stump power is high for the main call, but it is the wrong type.

- A strong model that takes the carousel order rate from `ordered_tiles` keeps HC-34 eligible and commits to it at 9.8.
- One that scores lift on in-session orders (the archive's own outcome) commits to HC-33 at 8.0.

**Too-easy signals sit on the FINE-numbers layers:**

- Tygo Knoers' "the archive has never missed with session weights" pre-answers the estimator choice.
- The commitment's per-served-ranking sentence pre-answers the fresh-listing grain.
- The field reference's "The session is the draw unit" restates it.

**The ask layer carries real FINE-numbers difficulty.** It sits in:

- KB-2026-02 net of VAT;
- valid-offer pricing;
- balance-paid purchases;
- the Checkout 3 pickups (HC-36's fee row swings from about +6 to about -12 per 1,000 if pickups are charged only as captured);
- the R2 bands and the 18 January app start.

Each single departure scores 0 of 48 cells or 0 of 6 totals.

## Findings, ranked
1. **Gate G, banned stumping type (SEND_BACK).**
   - *Where:* `home_carousel_render_log_2026-06-22_2026-09-20.csv` (`ordered_tiles`), `carousel_experiment_archive.xlsx` (`in_session_orders`), `experimentation_charter_home_surfaces.pdf` 2.2 and 2.4, `planning_thread_carousel_slot.txt`.
   - *What:* the call is won by swapping the logger's in-session lens for the charter's: lift over the test (HC-33 7.96 to 3.30) and every order from the served tiles (HC-34 -0.96% to -3.77%).
   - *Change:* rebuild the decisive rung on a FINE-numbers shape where every reported read is right and the difficulty is analysis. The build already carries the nearest one: the slot forecast. The 18 January app start, the R2 tenure bands and each cell's lift could be made to decide between two eligible policies. The archive back-test is the other candidate, if Tygo's "session weights" line comes out. Keep the call forced and assert it in the generator.
2. **The planning thread ranks the candidates and is not a declared distractor.**
   - *Where:* `planning_thread_carousel_slot.txt`.
   - *What:* Fabian Stoffel ("I'd want the slot", "the log bears it out") and Kayleigh Zeemans ("I would not put it up against the velocity boost for this slot") rank HC-33 over HC-37 on the decision question, and the answer overturns both. This breaks the house Gate G rule and contradicts the design note's litmus.
   - *Change:* strike both preferences, or rewrite them so neither expresses a preference among the six.
3. **The order data read as constructed, and the horizon is forced only by that construction.**
   - *Where:* `orders_enrolled_buyers_2026-06-01_2026-10-11.parquet`.
   - *What:* within 21 days either side of each logged session, background orders fall in exact hundreds per channel per day bucket and cancel across arms. Five of six policies therefore have identical lifts to two decimals from in-session through day 21.
   - *Noise:* a per-session bootstrap gives a standard error near 13 per 1,000 on HC-37's lift, and near 15 on the HC-37 minus HC-33 gap. One more week of unbalanced background moves HC-37 from 5.70 to 2.08.
   - *More synthetic tells:* Blend v7 serves exactly 13.0 fresh tiles per 100 in all eight cells, and HC-37 exactly 21.4. Every fee cell lands within 0.015 of a one-decimal value.
   - *Change:* regenerate the background with realistic noise across the whole extract, and re-assert the call under it. If the call does not survive, the margins are too thin for the data. If the horizon is meant to be 21 days, write it into a shipped document.
4. **HC-34's guardrail breach is two orders wide.**
   - *What:* HC-34 has 69 tile orders in app 0-29 under both counts. The breach comes from Blend v7's five post-session tile orders (171 to 176), which move the threshold from 68.6 to 70.6 orders.
   - *Design note:* it records that this cell's in-session lift was tuned from -1.30 to -0.20 per 1,000 so the logger count passes HC-34.
   - *Change:* the margin is thin but clean under the charter's point-estimate rule, and it will not survive a noisier regeneration. Widen it in the generator if the guardrail stays in the ladder.
5. **Too-easy signals on the FINE layers.** Tygo Knoers' thread line pre-answers the estimator, and the commitment's grain sentence pre-answers the fresh-listing count. If the rebuild leans on the archive back-test, the thread line goes.
6. **Units and rounding (`prompt.md`).**
   - *What:* "the gap between the two" carries neither unit nor rounding. The fee grid and the totals take their rounding from the trailing "Rates to one decimal, totals to the nearest hundred."
   - *Change:* state unit and rounding inside each asking sentence, e.g. "and the gap between the two, in extra orders per 1,000 carousel sessions to one decimal".
7. **Hygiene that does not affect the stump** (FIX_NOW-class on its own):
   - both docx files report 0 words, characters and paragraphs in `docProps/app.xml`;
   - both PDFs carry Producer "Vouwlijn" and CreationDate 2026-10-14, against pulled dates of 1 June and 1 September;
   - `extract_register_slot_review.md` closes on "Nothing in the folder has been edited after export", which reads as authoring reassurance;
   - `ranking_policy_register.json` says HC-34 and HC-37 re-rank after every render, while `carousel_logger_field_reference.md` says every render repeats the session's ranking.
8. **Process.** This pass ran without an isolated thread (see the run note). After the rebuild, re-invoke in a harness that has the Agent tool, so the judge never reads `submission.md` whole.

## Next action for the author
Rewrite the decisive rung in `DESIGN_NOTE.md` around a FINE-numbers shape before touching the generator. The slot forecast the build already carries is the nearest candidate. Do it in the same pass that strikes Fabian Stoffel's and Kayleigh Zeemans' preferences from the planning thread.
