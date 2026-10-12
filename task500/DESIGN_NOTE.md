# task500 design note

Root-Cause Analysis, re-rooted. The author asked for a root-cause build "in data science", left the domain open and
ruled out anything bio-related. v1 (Supply Chain & Logistics, a container terminal) was solved on the portal; the author
widened the re-root to any accepted domain. v2 (K-12) was solved on the portal too; the author asked for a third
Root-Cause draw and chose to go to the portal without an in-house solver round. Card:
`.claude/skills/fingerprint/cards/task500.json` (v3; v2 and v1 in lineage).

## PORTAL LOG

- P1, v1, 2026-10-10: Stumped Check 1 failed. Both responses named the Rijnpendel shuttle with 15 of the 28 late
  sailings saved; one cited instruction 4.3. Neither differed from the golden. "Both landing", so the slot re-rooted at
  stage 1.
- P2, v2, 2026-10-11: Stumped Check 1 failed. Both responses named MV-25-01 with 156 and full-day kindergarten at 41;
  one called it the later start "spilling over onto younger siblings". At ceiling under the v2 stopping rule, so no
  repair is licensed; the next step is the author's (re-root or stop).

## DRAW (v3, 2026-10-11)

| Axis | Draw |
|---|---|
| Domain / subdomain | economics / public-finance (Economics x Root-Cause has never been built) |
| Niche | an invented state's fiscal 2026 lodging tax receipts shortfall against the adopted forecast, put on one of five changes in the year-end revenue variance statement |
| Objective | Root-Cause Analysis (the statement names the change that drove a closed year's shortfall and the dollars it accounts for; retrospective by nature, because the forcing event is the year-end variance statement itself) |
| Shape | 03, bridge between two totals: forecast to actual receipts, each change's attributed effect as a reconciling item and the residual |
| Decision | root_cause_named (the change, with its dollars) |
| Gap / pattern / generators | rule then population / B / G16 decisive (method selection), G6 below (class-controlled comparison), G15 rival-killer (the platform collection change is a reclassification) |
| Gate G mechanism | method_or_model_selection: the office's standing matched-reference attribution method, whose construction no document gives in full, is pinned only by reproducing the per-filer reference figures of two certified prior statements |
| Calibration | closed_decision_corpus: the certified fiscal 2024 and fiscal 2025 variance statements, produced by the same standing method, each with its per-filer reference table |
| Context artifact | published_series (the monthly receipts series and the adopted forecast) |
| Role / forum / forcing event / org family | statistical_office_head (director of the state's office of revenue analysis) / council_or_assembly (the legislature's joint finance committee) / period_close (fiscal year-end statement) / research_or_statistics_office |
| Spine | lodging_tax_returns_fy2023-fy2026.csv, one monthly return of one filer |
| People | Thomas Valentine, Erica Lynch, Joseph Osborne, Rachel Erickson, Paul Crane (`guard.py names --geo "United States" --seed 500`) |
| Deliverables | fy2026_lodging_tax_variance.pptx (briefing with the bridge chart), fy2026_lodging_reference_matches.csv (each touched filer's matched reference) |
| Guard | PASS, registered. Rule/B/method selection repeats twelve older builds and task36's Calderstone lineage; each carries a differentiation line on the card (they recover a rate, a gate, a span, a date convention or a precedence rule; v3 recovers the counterfactual construction itself). Nearest driver 0.11 (this slot's v2) |

**Device source.** The matched-reference construction is the client's stabilisation-award device (held at 0.33: many
coupled steps, controls from two closed cycles, the solver failed the controls, said so, and named a winner anyway),
reused on a fresh scenario. It is the measured top architecture (trap 1 decided 11 of 64 client tasks, 9 under 0.50).

**Litmus.** Every figure is correct: returns are recorded as filed, the forecast is the adopted one, the two certified
statements are what the method produced. No stakeholder's number is overturned; the trap is the solver measuring each
change with its own comparison. surface_read_dependency: no. stumping_family: analytical_non_defect.
sole_data_defect: no.

## Stump sentence

A competent solver lines the five changes up against the monthly shortfall, compares each change's filers with the untouched ones by property class, sees the downtown hotels fall furthest after the convention center closed, and files the closure as the cause with its class-controlled dollars; the step that lands it there is measuring each change with its own comparison instead of the office's standing matched-reference method, which reproduces the two certified variance statements only when each filer is matched to same-size peers outside its region, aligned to its own effective month and drawn from a pool screened at each peer's own window with a cap on reuse, and under that method the downtown fall is the business-travel slump every large hotel shared while the long-stay exemption carries the shortfall.

## First-moves test (on paper, before any data)

The five changes, each with a direct touched group a filer column identifies (no odd one out, filter 1): the
convention center closure (downtown hotels, September), the long-stay exemption (extended-stay properties, January),
county-option rate cuts (two counties, October), platform collection for short-term rentals (host filings move to the
platforms, August), an airline hub reduction (airport-corridor hotels, November).

1. Timing alignment: the shortfall steps down in September and again in January; the September step is the larger,
   so the event study points at the closure (decoy).
2. Touched against untouched, by class: downtown full-service hotels against all other full-service hotels still
   leaves the closure ahead, because most other full-service hotels are small and fell little in the slump; built to
   hold with class and region controls, asserted.
3. Magnitude ranking: the closure's touched base is the largest, so its dollars lead.
4. The platform change: host filings collapse, but platform filings rise by the same receipts, so a totals check kills
   it (rung 1, G15).

Filter 2: nothing filed asks for each change's affected population; the template grades each change's attributed
dollars. Filter 3: the certified statements are read on the natural path for last year's continuing effects in the
bridge. Filter 4: the method moves both the named change and the dollars.

Design constraints carried into stage 2: five to eight coupled choices in the construction; every single-choice
deviation reproduces most but not all certified per-filer figures (match counts written per choice before the pack is
cut); one clause in the office's procedure states the standing method governs this year's statement.

## ENTITY, DECISION, ANSWER (built)

An invented state's lodging tax (6% state rate plus a 2% county option, 3% in Prairie and Bluff until the October
2025 cut to 2.5%), 1,311 filers in eight regions, monthly returns fiscal 2023 to fiscal 2026 (57,577 lines). Every
property carries a business-travel dependence no column holds; it shapes the property's year (business months against
summer leisure) and sets how hard the September 2025 business-travel slump hits it. Downtown hotels are the most
business-dependent; resorts are the largest hotels outside downtown and barely felt the slump.

**ANSWER.** The long-stay exemption, -3,235 thousand (unrounded -3,234.66). Runner-up the convention center closure,
-2,108 (-2,107.52). County option cut -862, airline hub reduction -586, facilitator collection +123. Shortfall
against the adopted forecast 22,001 (245,572 forecast, 223,571 actual); no change accounts for -15,333.

## LADDER (measured)

| Rung | The analysis | Names | Killed by |
|---|---|---|---|
| R0a | Host returns stop in August 2025 | facilitator collection (a large loss) | the facilitators' returns carry the same receipts; together they rose (G15) |
| R0b | Event study on the monthly shortfall | the closure (the September step is the larger) | the step is shared by every business-dependent hotel |
| R1 | Touched against untouched: all, same class, same class and size, neighbouring region, balanced panel, class by month | the closure, -6.2M to -7.8M against -3.9M to -4.2M for the exemption | none of these comparison groups shares downtown's business dependence |
| R2 | Seasonality bands (summer share in 3, 5 or 10 bands) | the closure, -4.3M to -4.8M against -3.6M | a band is too coarse: downtown sits at its business end |
| R3 | The standing procedure as Appendix B pins it | **the long-stay exemption, -3,235** | survives |

Partial constructions: across profile matching with k 3 to 10, cap 0 to 3, a 24 or 12-month screen and a median or
mean, 66 of 96 standardised-profile constructions and 76 of 96 share-profile constructions name the exemption; raw
profiles name the closure. So the name is protected by whether a solver reaches profile matching at all, and the exact
construction pins only the count.

## FORKS CLOSED (asserted)

- Full grid of 10,368 rival constructions (class rule, own region, continuity 24/12/both years, standardised/share/raw
  profile, k 3 to 10, cap 0 to 3, order, median/mean/sum, own-month or fiscal-year window): exactly one reproduces all
  78 Appendix B figures. Nearest misses 63 (12-month screen), then 29, 28, 27. Single deviations 2 to 63 of 78.
- Every figure off its rounding edge by at least $10 in exact arithmetic (tightest: the runner-up, $24).
- No two of the closure, the exemption, the airline cut and facilitator collection touch a common filer; no
  extended-stay hotel downtown, on the airport corridor or in a cut county.
- Returns as originally filed; every return received by August 12 is in the extract; amendments live only in the
  treasury ledger.

## ASK SHEET

- Bridge (construction layer, inherits the method): five effects and the line no change accounts for.
- Reproduction count (78 of 78): the validity check the procedure requires; a solver who ships a partial reproduction
  reports a smaller number.
- Cash walk (devices, off the main path; the main call reads only the returns): collections 225,148 thousand from the
  treasury ledger, with penalty and interest excluded (1,610 thousand more if counted), each return's latest
  amendment only (every amendment counted moves it), refunds netted, and deposit dates rather than periods (reading
  by period moves it by more than $1M). Reconciling lines: fiscal 2026 periods not deposited by June 30 (21,938),
  earlier periods deposited in the year (23,830), amendments (84), refunds (400).
- Per-filer CSV (construction layer): 140 filers with actual and reference receipts, tax effect and reference filers.

## Leak and house notes

- leak.py (asof 2026-08-14): REVIEW, no LEAK. A refund line of -289.23 equals one golden CSV cents figure by
  coincidence; the prior statements share variance-statement vocabulary with the call and name no fiscal 2026 change.
- guard surface: no byte-identical or same-seed tables; personas clean; the promoted pairs (task30, task55, task29,
  task71) are the card-level signature, each differentiated on the card.
- Container audit clean on target/ and golden/.

## STOPPING RULE (v3)

Written before any portal result: two responses naming the long-stay exemption with the graded dollars is at-ceiling
for this architecture and the slot.

## Tried and rejected

- Nonprofit funder, a portfolio metric drilled to one leaf with the counting unit pinned by reproducing a published
  series: this is the Tessel exemplar (client mean 0.36) in the same domain and shape, so a clone however new the nouns.
- Economics, a statistics office's average weekly earnings rebuilt under a reproduction gate and drilled by mix and
  rate: the loud rung is available but no quiet decisive rung behind it exists that is not another counting unit or
  filter population, which is task109's driver (unwritten compilation rules behind a published control set).
- Parcel hub, a sort wave held for a late feeder whose share of the wave crossed the hold line: the mechanism survives,
  the world does not. task36 is supply-chain RCA on delivery punctuality with dispatch waves and a night consolidation
  trailer in its furniture, so the surface would read as a repeat. Moved the mechanism to a deep-sea terminal.
- v1, the filed hold line crossed by block consolidation, its measure pinned by the desk's 108 closed hold-or-roll
  decisions (answer the Rijnpendel shuttle, 15 of 28): solved on the portal by both responses. The decisive rung sat off
  the path of both graded quantities. The shuttle was the one operator new in 2026 and the call log's remarks named it
  on every barge hold, so it led the natural pipeline (the position table had read rung 0 off the delay-code taxonomy,
  not off what the files name); and taking its held blocks off the late calls returns 15 whichever change a solver
  blames, so the measure of export load moved neither the name nor the count. Two exhausted shapes at once: a
  threshold crossing, and a cause that is the one thing present only in the later period.
- v2 draw a (withdrawn at the draw, never built): the line's scorecard port stay, its unit a port call across berth
  stays and its population the line's operated tonnage through a dated vessel annex, the two moves pinned by 24
  published monthly means. It is task109's driver whatever the nouns; the guard's text score (0.05) missed it, the
  mechanism read did not.
- v2 draw b (withdrawn at the draw, never built): late starts read as late arrivals, traced through the quay's berth
  sequence to another line's ship by a fixed hand-over gap. It is task111 v1's driver, and task111 v1 was solved on
  the portal by both responses.
- v2 draw c (withdrawn at the draw, never built): Policy & Education, a district's absence days against a certified
  baseline whose second key is the bus contractor's route tier. It passed the guard and the mechanism read, and failed
  the first-moves test: a group-against-rest cross-tab on the route tier names the cause with no baseline at all.
- v2 draw d (withdrawn at the draw, never built): grade 3-5 reading results falling because the new K-2 screener's
  students took the interventionists' fixed slots first. It is task88's driver whatever the nouns.
- v2 build, a boundary change as the fourth change: a moved neighbourhood is a visible column (address) that a
  cross-tab separates for free, and it sat beside the household link a solver would then find; replaced by the grades
  1-2 reading block.
- v2 build, a whole-school breakfast change as a rival: it applies to every student, so the template has no comparison
  group and it could never be scored or ruled out on the template's terms; replaced by the reading block (grades 1-2).
- v2 build, the Champions coordinator saying in the thread that the program's end caused the rise: a voice arguing for
  the decoy invites the refutation reflex and pushes a solver off it; the thread now names no cause.
- v2 build, B and C as plain code-filter and time-zone asks: every device was a filed rule a careful solver executes
  (work orders, not traps); added the half-day minutes, the ISS code, Ridgeline's conference-day rows, the GPS outage
  mornings and the pre-term dry runs so each figure sits under a silent device.
- v2 (household spillover of the later middle school start, 156, runner-up full-day kindergarten 41): solved on the
  portal by both responses, one naming the sibling spillover outright. The template asked for each change's affected
  students, so the one change that touched no K-5 student had only its indirect channel to write in that cell; that
  change was also the odd one in a closed list of five, which is the candidate a trained solver interrogates first;
  and the household file had no job on the natural path, so its one use was the decisive join (household size alone
  shows +1.1 to +8.4 points). Shipped to the portal without an in-house solver round, which would have found it.
- v3 first direction (never built): the risen figure's tabulation pinned by reproducing published means, the
  architecture of the client's journey-time cause. In its general form it is task109's driver (unwritten compilation
  rules behind a published control set, each alone reproducing fewer figures), the same reason v2's draw a was
  withdrawn; v3 recovers the attribution method instead of the figure's population.
