# AD41 — Which prize series gets proctored mode next season, when one series' moves were scored by a shallower engine

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · online game integrity |
| Mirrors | Integrity teams deciding where a costly protection goes when one population's detector signal is quietly degraded by how its data was processed (anti-cheat rollouts at Riot and Valve, invalid-traffic detection at Google where one traffic source is logged at lower fidelity, spam detection where one client reports truncated metadata) |
| Decision shape | Which of N gets one scarce thing: the season's single proctored-mode deployment (webcam, screen share and live move-time review) goes to one of five prize series |
| Committed call | The series that gets proctored mode, and the prize money it protects from assisted play over the season |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the quiet second trap (one series analysed at lower depth, which compresses its residuals), with a mixed segment split through the entry table (prize divisions) below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #6 treats a mixed segment all one way · #4 never tests its reading against the control |
| Calibration form | Pilot log: last season's proctored-mode pilot on two series, with every flagged account and the fair-play committee's filed decision |
| Driving force | Everyone beats the loud trap: accuracy rises with skill, so scores must be residuals against rating, time control and colour. The quiet one is in how moves were scored. The 960 Series is analysed by the fallback client-side engine at depth 12 where every other series is analysed at depth 20, and shallower analysis inflates everyone's move losses and squeezes an engine user's residual toward the crowd. Only the analysis job log, joined game by game, shows it, and only expectation tables built per depth reproduce the pilot's 23 confirmed 960 cases. |

## 1. Situation

An online chess platform runs five prize series, from a titled arena to a 960 series, with $310,000 in prizes next season. Its fair-play
team can run proctored mode (webcam, screen share and live review of move times) on one series, which the pilot showed catches about nine
in ten assisted players before prizes are paid. The fair-play plan sends it where it protects the most prize money from assisted play, valued
on this season's results. The team holds every analysed game with per-move evaluations, the analysis job log (engine, depth and host for
each game), the entry table with each entrant's prize division, the series terms and the pilot log. The community manager is sure the
titled arena is the problem.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the evaluations at the depth each game was analysed, the accuracy figures, the residual screen, the
  entries and the committee's decisions. The fair-play lead is right that the screen is calibrated on millions of games. Nothing is
  overturned; the difficulty is that one series' evaluations come from a different instrument setting, recorded in a file the screen never
  reads.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the community manager's view and the best-five list. A residual screen with division-correct prize money still
  names C.
* **Instrument repair.** Run every game at depth 20 and the quiet trap disappears, but that is a new analysis the team cannot run before the
  decision; the shipped evaluations are exact for the depth they record, and recognising which games carry which depth is the difficulty.
* **Lens swap.** The naive population of assisted accounts is the one a pooled expectation flags; the answer's adds 960 accounts that only a
  depth-matched expectation reveals, a different set of accounts and a different series.

## 3. The driving force

A strong solver rejects raw and best-five accuracy, builds expected move loss by rating band, time control and colour, aggregates game
residuals per account with √n scaling, and values each series by the prize money its high-scoring accounts won, splitting prizes by division
through the entry table. Every step is correct and the loud trap is beaten. The analysis job log records that the server cluster does not
analyse 960 starting positions, so the 960 Series falls back to a client-side engine at depth 12. Shallow evaluations miss tactics, so
everyone's measured move loss rises, the 960 expectation absorbs it, and an assisted player's edge over the crowd is halved. A pooled
expectation table (or one built by time control and rating only) leaves 960 looking like the cleanest series. Building the expectation per
analysis depth, a join from each game to its job record, doubles the 960 Series' assisted prize money, and the pilot log, whose 960 confirmed
cases the pooled screen mostly misses, is the control that shows it.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Accounts on the best-five accuracy screen × their prize winnings ($k): A 74, B 61, C 52, D 45, E 38 | A, the titled arena | The current screen and the obvious place to look | The expectation table: accuracy rises steeply with rating, and A's flagged accounts score as expected for their band |
| 1 | Residuals against rating, time control and colour, aggregated per account; prize money won by accounts over the review line, series pool treated as one: B 66, C 52, D 41, E 34, A 19 | B | The loud trap beaten with a proper expectation | The entry table and series terms: B's prizes split into an Open division ($40k) and an under-2000 division ($8k), and B's high scorers sit in the under-2000 division |
| 2 | The same with prize money assigned by division through the entry table: C 50, E 36, D 33, B 28, A 18 | C | Expectation-adjusted and division-correct | The analysis job log: every 960 Series game was analysed client-side at depth 12 |
| 3 | **Decisive:** expectation built per analysis depth as well, prize money by division: E 71, C 50, D 33, B 28, A 18 | **E, the 960 Series** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.39×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.21×, 1.27×, 1.39× and 1.42×.
* **Discriminator dominance.** C carries a 1.39× advantage into rung 3. E's assisted prize money rises 1.97× when its expectation is built at
  its own depth while C's is unchanged, so the net is 1.97 / 1.39 = 1.42×.
* **Partial correction priced (L3).** A solver who notices the 960 Series is different but builds its expectation by variant instead of by
  depth gets the same compressed residuals, because every 960 game is depth 12, and still names C. A solver who rescales 960 residuals by the
  ratio of standard deviations, without rebuilding expectations, recovers half the effect (E at 53) and still names C.
* **Grid.** Expectation (best-five, pooled, per depth) × prize assignment (one pool or by division) = 6 cells. Best-five cells name A, pooled
  cells name B or C, and only per-depth expectation with division prizes names E; per-depth with one pool names B.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The analysis job log records engine, depth and host per game as an operations record. No document says depth changes
   move loss or that 960 games are analysed differently.
2. **The quiet trap has its own control (Pattern B).** In the pilot log the committee confirmed 23 assisted accounts in the 960 Series and 14
   in series D. The per-depth screen flags 23 of 23 and 14 of 14; the pooled screen flags 9 of 23 and 14 of 14. The pooled screen's misses all
   run one way, so it under-counts the 960 total by 61%. The per-depth expectation is a stratified rebuild through a join, not a parameter to
   sweep.
3. **No arithmetic symptom.** Every game has evaluations on every move, move losses reproduce from the evaluations, and the 960 residuals
   are centred and scaled like every other series'.
4. **Not a row predicate.** It needs each game joined to its analysis job, expectation cells rebuilt by band, time control, colour and depth,
   residuals recomputed and re-aggregated per account.
5. **The enumeration is arithmetic.** Which 960 accounts are assisted is computed; no column marks shallow analysis on the game table.
6. **No cutover date.** The 960 Series has always fallen back to depth 12; nothing steps.
7. **Survives deletion.** Remove both voices and the best-five list, and the pooled residual screen is still the natural build.

## 6. The calibration corpus

* **Form.** The pilot log: last season's proctored-mode pilot on the 960 Series and series D, every account the proctors flagged and the
  fair-play committee's filed decision (confirmed assisted or cleared).
* **What it pins.** Proctoring's catch rate (0.90) and the per-depth construction (above). The absolute split: every confirmed account scores
  3.0 or more on the per-depth screen and every cleared account under 2.4, so the review line is threshold-free.
* **Twin pair.** Accounts rookfile_21 (960 Series) and kovacs_w88 (series D) have identical pooled scores (+2.1), ratings, game counts and raw
  accuracy. Their per-depth scores are +4.3 and +2.1, 2.0× apart; the committee confirmed rookfile_21 and cleared kovacs_w88. Only the depth
  join separates them.
* **Resemblance points at the decoy.** On the pooled screen, the 960 Series' score distribution matches series D's, the cleanest of the five.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fair-play plan: proctored mode goes where it protects the most prize money from assisted play, valued on this season's
  results. The series terms with each division's prizes. The analysis job log as the record of how each game was analysed. One sentence each.
* **Empirical pins.** The review line and the catch rate, from the pilot.
* **Voices.** The community manager: "The titled arena is where the money and the cheaters are." The fair-play lead: "Our residual screen is
  calibrated on millions of games; trust it."
* **Licensed wrong basis.** The plan records that the sponsor's integrity auditor measures each series by flagged accounts on the best-five
  screen and will review the decision on that basis.

## 8. Determinism by construction

* **Expectation cells.** Every rating band × time control × colour × depth cell holds at least 2,000 games, so no cell is thin.
* **Review line.** The pilot's gap from 2.4 to 3.0 is empty this season too, so any line in it flags the same accounts.
* **Prizes.** Each entrant has one division for the season in the entry table, and prize money is taken from the series terms.
* **Rounding.** Protected prize money is given to the nearest $1,000: E's $71k assisted × 0.90 = $64k, mid-bin.

## 9. Prompt sketch and deliverables

> We can run proctored mode on one prize series next season and five are asking for it. Our community manager is sure the titled arena is
> the problem. Tell me which series gets it and how much prize money it should keep away from assisted players over the season, to the
> nearest $1,000, in a line for the sponsor. Send `proctoring_case.xlsx`, a chart `depth_residuals.png`, and a one-page `series_memo.pdf`.

* `proctoring_case.xlsx` — the five series under each rung's basis (ask C), the entrant sheet (ask A) and the payout sheet (ask B).
* `depth_residuals.png` — account scores for the 960 Series under the pooled and per-depth expectations as two histograms, the review line
  drawn, the pilot's confirmed accounts marked, and each series' protected prize money in a side panel.
* `series_memo.pdf` — the committed series and figure, and why each other series falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each series, unique entrants this season and their median and 90th-percentile rating. *Device:*
  the entry table stores the username at entry, and the account register maps renamed usernames to one account ID; counting usernames
  double-counts renamed accounts in four series. The decision uses account IDs from the results table, never the entry usernames.
* **Ask B (device-carried).** For each series, prize money paid this season in cash and in store credit. *Device:* the payment ledger books
  store credit at face value, and the finance guide states it at a cash equivalent of 0.6; adding face values overstates three series. The
  decision values prizes from the series terms, never the ledger.
* **Ask C (validity).** Each series' figure under each of the four rung bases.
* **Decoupling.** Clearing the depth stratification and the division split changes no figure in asks A or B.

## 11. Rubric arithmetic

5 series × 3 (ask A) + 5 × 2 (ask B) + 5 × 4 bases (ask C) + the committed series, its protected prize money, the runner-up and the margin +
5 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.39× behind C) and 1st.
* All 960 Series games are depth 12; all others depth 20. Depth-12 move losses run 1.8× depth-20 losses for the same games in a 2,000-game
  side sample shipped with the job log.
* Pilot: 23 confirmed in the 960 Series, 14 in D; confirmed scores 3.0 and above, cleared under 2.4.
* rookfile_21 and kovacs_w88 are identical on every game-table column.
* Entry usernames and payment ledger rows never touch the results table, evaluations or the job log.
