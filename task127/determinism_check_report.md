# determinism-check report, task127, 2026-10-10

Pass 1, ordered by the `/build` pipeline at stage 6. There was no `target.zip` in the folder, so the unzipped `target/` was copied fresh to `/tmp/determinism-check-task127-20261010T031900Z-0b87c3c5/target/` (byte-identical, checked with `diff -rq`). This harness has no Agent tool, so the judge pass ran in the orchestrator's own context rather than in a spawned thread. Isolation was kept by ordering instead. Before `verdict.md` was written, the only things read were that scratch path, the inlined blocks (`judge_inputs.md`) and `guidelines/determinism_judge_system_prompt.md` (v3, applied in full). The design note, `metadata.json` and `golden/` were opened only after the verdict was fixed, and the solver reports were not read at all. The cross-batch reference check was not run because it falls outside the allow-list. If you want a full-strength isolated thread, re-invoke from a harness that provides the Agent tool.

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Gate C fails on the main recommendation and on every committed answer copied from it: board-note asks 1 and 2, the CSV's Uplands and total rows, and the SVG's Uplands bar, unallocated bar and title. Step 5 spreads each co-op's feeder-capped installs over the pilot's install calendar in proportion, which leaves only 74.2 of Uplands' 296.8 capped installs in the spring window. Participation terms section 3 says "An install proceeds only where the feeder has that capacity remaining", so the capped Uplands feeders (UP-101 with room for 36, UP-104 with room for 40) fill in date order. All of their spring demand (31.0 and 18.8) proceeds, spring meter orders rise to 105.1, and the crew clears them before the autumn surge. Read that way, Uplands sets 201.3 meters by 31 December, which gives **200 slots, 1,200 placed and 600 unallocated** instead of 170, 1,170 and 630. The governing label is competing_defensible_answer. The shipped terms lean toward the date-order branch, so the golden's own figure is the weaker reading. Lakes also sits 1.3 to 3.7 meters from a rounding line under either reading (margin_or_boundary_fragility, secondary).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot install rate, propane furnace | 3 in 38 | 339 / 4,294 = 3/38 (`pilot_rebates_2026.xlsx` heating_system_replaced over survey weights, rules section 2 filter) | yes |
| Pilot install rate, electric resistance | 1 in 32 | 44 / 1,408 = 1/32 | yes |
| Pilot install rate, propane boiler | 1 in 95 | 29 / 2,755 = 1/95; the three rates fit all 18 neighbourhood-by-system cells exactly | yes |
| Qualifying homes 2027 (Sara Duncan's claim) | Uplands most | Uplands 11,500, North Shore 9,640, Valley 9,180, Lakes 7,600, Riverbend 6,300, Pinewood 5,600 | yes (the claim is true) |
| Table H1 propane plus electricity | not claimed | reproduces exactly from the microdata (Valley largest at 32,424) | yes |
| Feeder-capped installs | 161, 182, 418, 297, 342, 80 | 161.43, 181.77, 418.00, 296.78, 341.62, 79.64 (`hosting_capacity_nov2026.xlsx` kW / 5, `area_feeder_map.csv`) | yes |
| Lakes crew saturated throughput | 10.50 a day | 525 / 50 working days, 8 Jul to 5 Oct 2025 (10.49 with the last day included) | yes |
| Uplands crew saturated throughput | 8.74 a day | 411 / 47 = 8.745 (8.729 inclusive) | yes |
| Lakes standing work | 8.06 a day | 1,636 / 203 = 8.059 (8.04 to 8.06 across six windows) | yes |
| Uplands standing work | 6.99 a day | 1,419 / 203 = 6.990 (6.99 to 7.00) | yes |
| Spare, Lakes and Uplands | 2.44, 1.75 | 2.441, 1.755 | yes |
| Lakes meters set by 31 Dec | 239 | 238.70 on the golden's proportional spread; 243.73 if capped feeders fill in date order | yes on the golden's method |
| Uplands meters set by 31 Dec | 171 | 170.45 to 170.75 proportional; 201.32 in date order | yes on the golden's method; not forced |
| Five-day crews set every meter | yes | spare needed a day: NS 1.83, V 2.07, R 3.88, P 0.90; best-month spare: 7.05, 7.33, 8.80, 2.22 | yes |
| 2027 slots | NS 160, V 180, L 240, U 170, R 340, P 80 | same on the golden's method; U 200 in date order | Uplands not forced |
| Slots placed / unallocated | 1,170 / 630 | 1,170 / 630 proportional; 1,200 / 600 date order | not forced |
| Co-op taking the most, lead over next | Riverbend 340, 100 ahead of Lakes | holds under every reading | yes |
| CSV North Shore row | 160, $16,962, 23.6%, $326,400, 82 | identical | yes |
| CSV Valley row | 180, $16,952, 23.8%, $295,200, 74 | identical | yes |
| CSV Lakes row | 240, $14,786, 29.7%, $143,800, 32 | identical | yes |
| CSV Uplands row | 170, $15,062, 29.2%, $121,000, 27 | cost, share, paid and installs identical; slots fork to 200 | partly |
| CSV Riverbend row | 340, $16,794, 24.0%, $290,800, 72 | identical | yes |
| CSV Pinewood row | 80, $14,263, 31.7%, $219,000, 49 | identical | yes |
| CSV total row | 1,170, $16,170, 25.7%, $1,396,200, 336 | money and installs identical; slots fork to 1,200 | partly |
| SVG 2026 pilot installs | R 92, L 40, V 88, U 32, NS 100, P 60 | identical | yes |
| SVG unallocated bar and title total | 630; "1,170 of 1,800 placed" | fork to 600 and 1,200 | not forced |

The cost and payment figures were checked against the invoice of record (latest accepted version), the IN-1126 export's repeated indoor-head lines counted once, the Schedule B amount with the income addition, `cleared_at` converted from UTC to Central up to 30 November, and the 24 returned ACH payments in `bank_returns_2026.json` taken out. No install is part-paid at the cutoff.

## Competing answers that survived
1. **How capped installs fall in time (decisive).** If the capped total is spread over the pilot calendar in proportion (the golden's step 5), the split is NS 160, V 180, L 240, U 170, R 340, P 80, so 1,170 placed and 630 unallocated. If capped feeders fill in date order until their filed room is used (participation terms section 3, with hosting filings refiled monthly as room is used), Uplands gets 200, so 1,200 placed and 600 unallocated. Across 66 estimation variants each (capacity window, standing window, two-decimal or exact spare, the batch's own clearing rate, spring orders rounded down, exact or up), Uplands lands on 170 every time on the first reading and 200 every time on the second. No shipped file says hosting room is reserved by window or that installs are rationed across windows. That rule is what was supposed to close this fork, and it does not exist.
2. **Lakes on the rounding line (margin).** Lakes holds 240 in 65 of 66 variants on the proportional reading. The low variant, 234.9, uses the batch's own clearing rate (119/50) with spring orders rounded down, which gives 230. On the date-order reading Lakes holds 240 in 62 of 66. The high variant, 245.3, uses spring orders at the nearest integer (110) and a 2025 to 2026 standing window, which gives 250. Nothing in the pack pins the estimation choices that close this.

The judge also tested three other answers, and each fails on a shipped rule:
- The feeder-capped split with Lakes first (420, 1,480 placed) ignores rules section 4.
- Sharing all 1,800 on uncapped installs (2,437 expected) ignores terms section 3.
- Uplands first on qualifying homes is the wrong lens.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 19 | yes |
| Distinct formats | 3 or more | 6: csv 6, pdf 5, xlsx 4, txt 2, json 1, docx 1 | yes |
| Largest file | 25,000+ rows or a large database | `field_orders_2025_2026.csv`, 27,451 rows | yes |
| Distractors declared and unlabelled | 2+ in `metadata.json`, never labelled in the pack | `weatherization_grants_2026.csv`, `feeder_upgrades_2027_2028.pdf`; no file name or text under `target/` labels either | yes |
| Distractors unused but relevant | same world, worth weighing | weatherization register covers the same co-ops and neighbourhoods; reinforcement schedule adds hosting room on NS-411, VA-205, UP-101, PW-601; the solution uses neither | yes |
| A distractor that moves a graded figure is ruled out by a shipped fact | reproduces and is ruled out | applying the reinforcement kW would lift capped installs to NS 401, V 353, U 385, P 200; every in-service date is Q2 to Q4 2028, programme year 2 ends 31 Dec 2027, and capacity is refiled only when the work is energised | yes |
| Deliverable count | 1 to 3 | 3 (docx, csv, svg) | yes |
| Format family | none required | not assessed | yes |
| Multi-dimensional asks | no stacked lookups | CSV covers 6 co-ops x 5 figures plus a total row; SVG has 13 labelled bars plus title; board note gives split, leader and lead | yes |
| Golden deliverables present | every named file | all three in `golden/`; figures match `submission.md` (and inherit the Uplands fork) | yes |
| Units and rounding stated | every ask | slots in tens; share to one decimal; "Dollars are whole dollars" stands as its own sentence after the CSV ask rather than inside it | yes, with a note |
| Prompt shape and the 25-criteria floor | identifiable shape, 25+ criteria | shape 05, allocation to a fixed total; about 50 gradable figures (7 split lines, 2 board-note facts, 35 CSV cells, 6 pilot bars, unallocated bar, title) | yes |
| Realism | nothing reads as LLM-generated; goldens read as work products | the pack fails (templated survey counts, round totals, exact-fit pilot rates, the "constructed for this exercise" line); the goldens read as a director's paper, a finance load file and a chart | no (pack) |

## Gate G reconciliation
The judge's classification matches the design note on all four fields. The judge has mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no. The design note (`## Decisive rung` and `### Gate G`) has binding_constraint with forecasting supporting, analytical_non_defect, no and no. The build reads the same shape from outside as from inside, so Gate G gives no send-back signal. The judge did not name either declared distractor as the surface read. It treated Sara Duncan's claim (true: Uplands has 11,500 qualifying homes, the most) and the Table H1 state-match basis (reproduces exactly) as correct-number lens reads, which the design note lists as a voice and the licensed wrong basis.

There are two drifts between the note and the pack:
- The note's pins list ("an install proceeds only where the feeder has room"; "the forward calendar shape (pilot dates)") never says how a capped feeder's room is used across the two windows. That gap is where the Gate C fork lives.
- The note's voices paragraph still names "Anthony Bentley, outreach director" believing Uplands has more "propane and electric homes". The prompt and trustees paper carry Sara Duncan and "qualifying homes".

## Stump power (Gate F)
Stump power on the main call is high. The decisive rung is rules section 4 (a rebate is earned at the meter set, and slots lapse on 31 December) meeting the Monday-to-Thursday crews' saturated throughput. That throughput is visible only in the July 2025 MXCH batch, and it has to absorb the 75 percent of installs that land between 25 September and 30 November. A model that checks annual crew capacity (2.44 a day over about 200 days exceeds 418) or stops at the feeder caps commits to Lakes first at 420 with 1,480 placed. The per-heating-system rates (a pooled or per-co-op rate misranks the co-ops) and the feeder join are secondary rungs.

The judge named these too-easy signals:
- Part of the Uplands stump currently works for the wrong reason, through the unpinned cap-timing fork.
- The CSV asks run on hygiene devices that strong models routinely clear: UTC versus Central clearing, returned ACH, unaccepted invoice versions, and repeated indoor-head lines.
- `field_definitions.txt` labels `cleared_at` as UTC.

## Findings, ranked
1. **The Uplands slots, total placed and unallocated count are not forced** (Gate C, competing_defensible_answer).
   - Where: `cooperative_participation_terms.pdf` section 3, plus `hosting_capacity_nov2026.xlsx` UP-101 (180 kW), UP-104 (200 kW) and LA-302 (390 kW).
   - What it affects: `submission.md` step 5 and all three goldens.
   - Change: re-cut the generator so that no feeder served by the Lakes or Uplands crew binds. Year-end meter sets then no longer depend on how capped room meets the calendar. Pinning the date-order rule in the terms is the alternative, but it leaves finding 2 open.
2. **Lakes sits on a rounding line** (margin_or_boundary_fragility). It is 238.7 on one reading and 243.7 on the other, against band edges at 235 and 245, and 5 of 132 variants leave 240. Change: re-centre Lakes' and Uplands' year-end meter sets (crew spare, autumn volume or the spring share) at least 3 meters inside their tens band under every variant listed above, and assert that in the generator.
3. **The decision data shows synthetic templating.**
   - In `heat_survey_2025_households.csv`, four neighbourhoods in four co-ops carry the identical eligible weighted triple ER 160, PB 300, PF 700 (Loon Point, Elm Park, Sauk Flats, Birch Hollow), and two carry 300, 420, 300 (Sawmill Corners, Flint Prairie).
   - 83 percent of the neighbourhood eligible cells are multiples of 10, and the 2027 qualifying totals are round hundreds (11,500, 7,600, 6,300, 5,600).
   - In `pilot_rebates_2026.xlsx`, three rates fit all 18 cells exactly.
   - In `field_orders_2025_2026.csv`, the Monday-to-Thursday crews' standing work is flat every month, and the batch days alternate exactly between 10 and 11.

   Change: de-template the neighbourhood counts and add month-to-month variation to standing work while keeping the decisive figures. This changes what solvers see.
4. **Authoring disclosure.** `about_these_files.txt` ends with "fictional and were constructed for this exercise". Change: strip that sentence. It is an in-house fix and does not reveal the trap.
5. **Provenance and temporal nits.**
   - Every PDF has CreationDate 2026-12-11 and Producer "Minnesota Clean Heat Fund", including the installers' group price guide and the terms signed in January.
   - `trustees_paper_17dec2026.docx` is marked internal, yet the manifest licenses it CC0-1.0.
   - The pull date is 10 December in `field_definitions.txt` but 11 December in the manifest and the trustees paper.
   - All 24 returns in `bank_returns_2026.json` are R02.

   Change: align these in the generator.
6. **Rebate-share wording.** In `prompt.md`, "the rebate as a share of that cost" reads as a ratio of averages. A mean of per-install ratios moves every row at one decimal (Lakes 32.3 against 29.7). Change: write "the average rebate as a share of that average cost" in the same rework.
7. **Design note drift.** `DESIGN_NOTE.md` voices section: replace the Anthony Bentley line with the shipped Sara Duncan claim. Also record the cap-timing fork under `## Tried and rejected`.

## Next action for the author
Re-cut the generator so that none of the Lakes or Uplands feeders binds (LA-302, UP-101 and UP-104 do today). Before you regenerate the pack and goldens, re-centre both co-ops' year-end meter sets at least 3 meters inside their tens band. Under the pipeline a SEND_BACK takes this build back through the build stage, and it needs a fresh solver round and judge pass.
