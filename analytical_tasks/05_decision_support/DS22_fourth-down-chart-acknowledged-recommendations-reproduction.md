# DS22 — How the club's fourth-down chart splits its 100 cells, when only one model reproduces every recommendation the coaches acknowledged

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · in-game decision support for a professional football club |
| Mirrors | Replacing a vendor's decision model with an in-house one that must reproduce the vendor's logged recommendations, where past actions were chosen selectively (Google and Meta bid models taking over from a vendor's, Amazon price recommendations reviewed by category managers, ride-hailing surge recommendations accepted by operations) |
| Decision shape | Allocation: the 100 neutral-state cells of next season's chart (yards to go 1–10 × ten field-position bands) split among go, punt and kick |
| Committed call | The chart, reported as the number of go cells and the longest fourth down the chart goes for at midfield |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B with a reproduction clause (measured #1 and #3), with the decision unit built from play rows (#2) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #2 counts file rows instead of the real unit · #15 follows the requester's hunch over the rule |
| Calibration form | Counterparty acknowledgement file: the coaching staff's acknowledgements of 412 in-game recommendations from the departing vendor over three seasons, each with the vendor's displayed win probabilities and the staff's accept or override |
| Driving force | The club's analytics charter lets an in-house model replace the vendor only if it reproduces every displayed win probability in the acknowledgement log to 0.1 points, and the vendor's method is written nowhere. The obvious model, conversion fitted on situation and win probability from field position and clock, reproduces 287 of 412. All 412 reproduce only when conversion carries each offence's and defence's weekly strength rating and win probability carries the pre-game spread, decayed by time remaining, each joined from its own file. Coaches went for it when their offence was strong, so every model without strength overstates a neutral team's conversion, and the chart that reproduces the log goes for it in 24 cells, not 33. |

## 1. Situation

A professional football club's analytics department must hand the coaching staff next season's fourth-down chart for a neutral game state
(tied score, second quarter, average teams). The vendor that has supplied in-game recommendations for three seasons is leaving. The club holds
three seasons of league play-by-play, the league's weekly team strength ratings, the pre-game market lines, the league's official season
statistics, and the acknowledgement log: every recommendation the vendor's booth sent, the win probabilities it displayed for going,
punting and kicking, and whether the staff accepted it. The analytics charter allows an in-house model only if it reproduces the log. The
offensive coordinator wants the chart to "trust the numbers, they say go".

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the play-by-play, the observed conversion
  rates, the vendor's displayed values, the ratings, the lines and the official counts. The difficulty is that the method behind the log
  has to be recovered from it, and its decisive parts sit in two other files.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the coordinator's view and the observed conversion table. A situational conversion model with a standard win
  probability model still produces a confident chart with 33 go cells and reproduces 352 of 412 displayed values.
* **Instrument repair.** No file the ladder uses is suspect: the play-by-play holds every snap and no-play row, and the official
  statistics, the ratings, the lines and the acknowledgement log are complete and exact. Perfect tracking on every snap moves no rung (46,
  38 and 33 go cells), coaches still chose when to go, and the ratings-and-spread construction is still needed for 24.
* **Lens swap.** The naive chart uses the attempts teams chose to make. The answer uses conversion for an average offence against an average
  defence, a different population of attempts from the one the log records.

## 3. The driving force

A strong solver distrusts observed fourth-down rates, builds decisions from play rows, fits conversion on yards to go and field position
with third-down plays borrowed for power, and plugs it into a win probability model on score, clock and field position. Each step is
competent, and the chart goes for it in 33 cells. The charter then asks it to reproduce the log, and it gets 352 of 412, with misses that look
like rounding. They are not rounding. They cluster in games with lopsided spreads and mismatched units. The vendor's conversion model
carries the week's offensive and defensive strength ratings, and its win probability carries the pre-game spread, decayed in proportion to
time remaining. Only that construction reproduces all 412. It also changes the neutral chart. Strong offences made most of the attempts,
so a model without strength credits an average team with their conversions. At league-average strength, 4th-and-3 at midfield converts 49%,
not 56%, and the chart shrinks to 24 go cells.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Observed fourth-down conversion by yards to go and field position, counted over play rows, with punt and kick outcomes and a standard win probability table | 46 go cells; goes through 4th-and-6 at midfield | The club's own record, as the coordinator reads it | The official season statistics: 71 fourth-down attempts in three seasons, where the play rows hold 93, because pre-snap penalties and timeouts add rows to one decision |
| 1 | Decisions built from play rows (the snap that counts after any penalty or timeout), observed rates per decision (#2) | 38 go cells; through 4th-and-5 | The right unit, matching the official count exactly | The acknowledgement log: observed rates reproduce 41 of 412 displayed values |
| 2 | Situational conversion model with third-down borrowing, standard win probability; reproduces 352 of 412 (#3) | 33 go cells; through 4th-and-4 | The textbook selection correction, and 85% of the log matches | The charter's reproduction clause: every displayed value, and the 60 misses all sit in games with spreads of six points or more or rating gaps above 0.15 |
| 3 | **Decisive:** conversion with the week's offensive and defensive ratings, win probability with the pre-game spread decayed by time remaining; 412 of 412; chart at league-average ratings and no spread | **24 go cells; through 4th-and-3** | — | — |

* **Figure shape.** Every correction walks the chart smaller, 46 → 38 → 33 → 24 go cells (offsets −8, −5, −9), and the answer is the
  smallest chart in the grid. Every other cell is at least 8% larger.
* **Position.** No intermediate chart equals the answer, and the answer's midfield boundary (4th-and-3) appears on no earlier rung.
* **Partial correction priced (L3).** The spread without the ratings reproduces 371 of 412 and gives 28 go cells (+17%). The ratings without
  the spread reproduce 389 and give 27 (+13%). Both, fitted on play rows instead of decisions, reproduce 398 and give 26 (+8%). Each half
  lands on a larger chart, never on 24.
* **Grid.** Unit (rows, decisions) × conversion (observed, situational, situational with ratings) × win probability (standard, with spread)
  gives 12 cells and 11 distinct charts. Only decisions, ratings and spread reproduce 412 and give 24 cells. The nearest wrong cell is the
  full construction on play rows (26 cells, +8%), and it costs one omission: the decision unit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The vendor's documentation names "situational conversion and live win probability" and nothing more. No document
   says the ratings or the spread enter either model.
2. **The reproducing rule is a construction, not a menu.** Ratings in conversion and the decayed spread in win probability reproduce 412 of
   412 to 0.1 points. The best rival, the same construction on play rows, reproduces 398, and the situational model 352, with every miss
   overstating the favourite's gain from going. The winning rule has no parameter to scan: the ratings join by team and week, the spread by
   game, and its weight falls with the clock.
3. **No arithmetic symptom.** Play counts, attempts and conversions reconcile to the official statistics at rung 1 and after, and every model's
   probabilities sum to one.
4. **Not a row predicate.** It needs two joins to two files, a refitted conversion model, a time-decayed prior inside win probability, and the
   chart evaluated at average ratings and zero spread.
5. **The enumeration is arithmetic.** No column marks a cell as go; the 24 fall out of three win probabilities per cell.
6. **No cutover date.** Ratings and lines change every week, and nothing in any series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The acknowledgement log: 412 recommendations over three seasons, each with the game, the situation, the vendor's displayed win
  probabilities for go, punt and kick, the recommended action, and the staff's accept or override.
* **What it pins.** The construction (412 of 412 above). It also shows the selection: the staff accepted 81% of go recommendations when the
  club's offensive rating was in the league's top third and 34% when it was in the bottom third.
* **Twin pair.** Recommendations 117 and 288 are identical on every situational column: 4th-and-2 at the opponent's 38, second quarter,
  tied, two timeouts each. The displayed gains from going are +3.1 and +1.5 points (2.1×). Only the ratings and the spread separate them:
  game 117 had the club favoured by 7 with the league's fourth-best offence, game 288 the club an underdog by 3.
* **Every rule exercised.** The log holds recommendations after pre-snap penalties, in games with spreads from −10 to +10, and late in
  games where the decayed spread is near zero, so every part of the construction is tested.
* **Resemblance points at the decoy.** The neutral state resembles the log's even games, where the situational model matches best, so a
  solver checking only those recommendations is confirmed at rung 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The analytics charter: an in-house model replaces the vendor only if it reproduces every displayed value in the log to 0.1
  points. The chart is for a neutral state: tied, second quarter, league-average ratings, no spread. A fourth-down decision is the choice
  at the snap that counts. One sentence each.
* **Empirical pins.** The ratings and spread construction, from the log.
* **Voices.** The offensive coordinator: "Trust the numbers; they say go." The special-teams coordinator: "Our punt unit is worth more than
  people think." A veteran assistant: "Field position wins in this league."
* **Licensed wrong basis.** The charter records that the club's football committee reviews charts against observed conversion rates and
  will see that basis.

## 8. Determinism by construction

* **Unit.** A decision is the last snap of a fourth-down sequence that counts as a play; the official statistics confirm 71 decisions.
* **Ratings and lines.** One rating per team and week, and one closing line per game, so each join has one match.
* **Decay.** The spread enters win probability in proportion to the game time remaining, the only weighting that reproduces the log.
* **Cells.** Each cell takes the action with the highest win probability. No cell's top two actions lie within 0.3 points, so rounding
  moves no cell.
* **Neutral state.** League-average ratings and zero spread, as the charter defines it.

## 9. Prompt sketch and deliverables

> The vendor is gone after this season, and I need our own fourth-down chart for next year. Our offensive coordinator says trust the
> numbers, they say go. Give me the chart and tell me how many of its 100 cells say go and the longest fourth down we go for at midfield,
> in a line for the head coach. Send `fourth_down_chart.xlsx`, a chart image `go_map.png`, and a one-page `chart_memo.pdf`.

* `fourth_down_chart.xlsx` — the 100 cells with the three win probabilities and the chosen action, the build under each rung, the practice
  sheet (ask A), the availability sheet (ask B) and the reproduction sheet (ask C).
* `go_map.png` — a 10 × 10 heatmap of the chosen action by yards to go and field position under the final model, with the rung-2 chart's
  extra go cells outlined and the midfield boundary marked.
* `chart_memo.pdf` — the committed chart and why it goes for it less than the observed record suggests.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Two-minute-drill repetitions by position group and week of training camp. *Device:* walk-through
  sessions are logged as practice rows at zero tempo, as the practice log's guide documents. Counting them as repetitions inflates every
  group by a fifth.
* **Ask B (device-carried).** Days lost to injury per player by season. *Device:* a player moved from injured reserve to the active list and
  back carries one row per designation under one injury identifier. Counting rows double-counts eleven injuries.
* **Ask C (validity).** Each construction's hits against the log, and each rung's chart as go-cell counts and midfield boundary.
* **Decoupling.** Clearing the ratings and spread changes no figure in asks A or B. Practice and injury rows never enter a play, a
  decision or a win probability.

## 11. Rubric arithmetic

100 cells (the action in each) + 6 constructions' reproduction hits + 4 rungs × 2 (go cells, boundary) (ask C) + 12 camp weeks × 1 for
the offence (ask A) + 3 seasons (ask B) + the committed count and boundary + 4 named chart parts + 3 files ≈ 136 criteria.

## 12. World-building constraints

* Play rows 93 and decisions 71 for the club's fourth downs over three seasons. Go cells by rung: 46, 38, 33, 24; partials 28, 27 and 26.
  Midfield boundaries 4th-and-6, 5, 4 and 3.
* Reproduction of the 412 displayed values: observed rates 41, situational 352, spread only 371, ratings only 389, both on rows 398, both
  on decisions 412.
* At league-average ratings, 4th-and-3 at midfield converts 49%; the situational model without ratings says 56%. The staff accepted 81%
  of go recommendations in top-third offensive weeks and 34% in bottom-third weeks.
* Recommendations 117 and 288 are identical on every situational column. Practice and injury rows never touch play-by-play.
