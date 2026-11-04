# task476 design note: Cinder Fork Timber Company's 2027 salvage marking

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first. Architecture 4, a
re-root drawn 2026-11-04 after architecture 3 (energy-based groundwater extraction) was abandoned at the stage-4 re-judge on Gate C, G and H passing;
architectures 1 to 3 are in the card's lineage with their shells, and architecture 2's shipped pack (5a46ee5a) stays at
the portal, pending, until this build replaces it at ship.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task476.json` (architecture v4), registered 2026-11-04T07:13:28Z;
  `guard.py check` WARN only (identity_resolution's semantics risk, answered under `## Three rules`; Gate G
  etl_conformance and the question form after task461 v3 and task192 v4). Structural matches differentiated on the card
  (task482's twelfth architecture). The window before the card: task461 v3, task192 v4, task193 v3, so G10 and G3 as
  the decisive pattern, the forums customer_or_counterparty, operations_desk and line_manager_or_team, the forcing events
  audit_or_inspection, shift_or_daily_cycle and period_close, the organisation families other, local_government and
  utility_or_infrastructure, and emissions-inventory were off the table. Nearest driver task455 at 0.08.
- **Seed:** ET33's number, re-rooted three times; nothing of any earlier world is kept.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data
  Extraction & Conformation (ETL). The forestry office reconciles its CFI database (the 2006 to 2021 cycles), the
  contract crews' 2026 export with its September height return, the plot register and the stand table into one fate for
  every tree tallied live in 2021, and the board marks the stands the salvage policy names.
- **Shape:** 15, fields conformed to one schema: every 2021 live tree's 2026 fate, and for every stand the Policy 7.4
  share, the 2026 live basal area per acre and the 2026 net Scribner volume per acre.
- **Strategy:** identity_resolution. Each 2021 tree's fate depends on finding it in the 2026 tally, and where the 2024
  underburns loosened its tag the 2026 crews marked it not found and tallied it again under a new tag; the decisive step
  links it back by plot, azimuth and distance, species and a diameter no newcomer could reach. Decisive generator G5
  (the survivor's record is provided elsewhere in the same file, as a new tree), with G12 (a missing record read as a
  record of death). Gate G etl_conformance.
- **World:** United States, a fictional tree farm in California's northern Sierra Nevada. Cinder Fork Timber Company, a
  family-owned sawmill company, measures permanent fifth-acre plots every five years; its board adopted a salvage
  policy in 2026 that marks a stand when its 2021 to 2026 mortality reaches 15 per cent of its 2021 live basal area. Five
  stands were underburned in fall 2024, two stands carry fir engraver and pine beetle mortality, and a 2025 lightning
  fire burned through one more. Personas from `guard.py names --geo "United States" --seed 476`: Tamara Larson
  (forestry manager), Brandon Freeman (inventory forester), Nicholas Wolf (board chair).
- **Forcing fact:** the board sets the 2027 salvage marking program at its December 2026 meeting, before the 2027
  operating season opens; the quantity is the closed 2021 to 2026 remeasurement (retrospective, because the policy
  measures the cycle just closed).
- **Forum and forcing event:** board_of_directors (the board adopts the marking program), season_or_peak (the 2027
  operating season). Organisation manufacturer; role operations_director (the forestry manager runs the timberland).
  Context artifact register (the plot register).
- **Data-native sentence:** Cinder Fork's tags are aluminium, nailed at breast height, and the 2024 underburns charred
  boles above that height on the burned plots, so about a third of the surviving trees of 9 inches and more there lost their
  tags; the 2026 contract crews, working from the 2021 tree list, marked each untagged tree's old number not found and
  tallied the tree again as added, and a new tree of 14 inches on a plot measured in 2016 and 2021 cannot be ingrowth.
- **The WHAT screen.** Population: the trees tallied live in 2021 on each stand's plots. Outcome: whether each is tallied
  live in 2026 (not cut). Window: the 2021 and 2026 measurements. Unit: basal area at 2021 diameter. Comparison: the
  stand's 2021 live basal area, against 15 per cent. The decisive step settles none of them: it is how a tree whose tag
  failed is found in the 2026 tally.
- **Deliverables:** `tree_fates_2021_2026.csv` (every 2021 live tree's fate and its 2026 record) and
  `salvage_marking_2027.pdf` (the board's marking list with every stand's share, live basal area and net volume).
- **Sources (all constructed, declared in `metadata.json`):** `inventory/cfi_database.sqlite`, the company's
  FieldCruise backend (cycles 2006 to 2021: `cycle`, `plot`, `plot_visit`, `tree` with the stem map, `tree_meas` with
  27,106 rows); `inventory/trf_cfi_remeasurement_2026.csv`, the contract crews' 2026 export (one record per listed tag
  plus the added trees); `inventory/trf_height_revisit_2026-09.csv`, the crews' September return for heights;
  `inventory/plot_register.xlsx`, the forester's register with the mapped conditions; `inventory/species_codes.csv`;
  `gis/stand_table_2026.csv`; `inventory/cfi_field_manual_rev2026.pdf` (plots, codes, the volume rules and Table 1);
  `policy/salvage_marking_policy_2026.pdf` (Board Policy 7.4, the pin); `operations/prescribed_burn_reports_2024.pdf`;
  `operations/juniper_saddle_fire_report_2025.pdf`; and the two distractors,
  `operations/aerial_detection_survey_2025.csv` and `markets/delivered_log_prices_2026q3.csv`.
- **Abstraction sentence:** "members of one cohort whose identifiers were destroyed between two counts reappear in the
  second count as newcomers under new identifiers, and an identifier join counts each as an exit and an entry." The
  nearest card is task455 (shipped, pending; driver score 0.08, `guard.py heart` WARN with no BLOCK on 11-04): there an
  administrative identifier is replaced by registration, a register field records part of the continuity, and the
  decisive step reads many-to-many member flows between accounts from the old unit's side, a direction choice over a
  ranked slate. Here the identifier is physically destroyed, no field, flow or shared member records anything, and the
  identity is one-to-one from a position and a size that only the earlier count's stem map and the later count's own
  measurements hold; the sentence a reviewer would write for both ("re-keyed units count as exits and entries") names
  the setting, not the step, and the steps differ (a flow direction against a spatial and allometric match). No other
  card on `guard.py mechanisms --objective etl` reissues an identifier between two counts of one physical cohort
  (task482's twelfth architecture re-attributes a load by flow; 236 joins one specimen under two keys inside one event;
  175, 179 and 196 link across organisations on shared quasi-identifiers).
- **As-of:** 2026-11-04, the memo's date before the December board meeting; the pack's records run to 2026-10-01.

## Survivor anatomy

Actor: a tree's identity across the two measurements has no column where its tag failed: the 2026 record of a re-tagged
survivor carries a new tag and the code for an added tree, and its link to the 2021 record is a relation between rows
in two files (the same plot, a position within 2 feet, the same species, a larger diameter) that nothing stores.

Link: the link is read by placing every 2026 added record on the 2021 stem map of its plot (azimuth and distance in the
database's `tree` table against the 2026 export's own azimuth and distance), a spatial comparison across two systems
that no key offers and no sentence invites.

Reflex: the field's remeasurement join (tree by plot and tag number, a 2021 live tree without a live 2026 record under
its tag counted as lost) sits at rung 0 and marks the five underburned stands with CF-112, CF-138 and CF-152.

Back-test: the textbook route validates: the tag join is complete (every one of the 6,859 tags tallied live in 2021 has
exactly one 2026 record, L, D, C or M, and no 2026 status record is orphaned), and the burned stands' 21.5 to 27.2 per
cent read as ordinary underburn mortality beside bole char heights of 6 to 10 feet in the burn reports.

Second use: every file the step reads is read for its own reason: the database for the 2021 population and diameters,
the 2026 export for every 2026 fate and figure, the register for the plots' stands and areas; the stem map is the
inventory's own relocation record.

Shock: the movement the step recovers reads as explained: underburns kill trees, so the burned stands' 21.5 to 27.2 per
cent needs no explaining, and the golden set is not an interval of any shipped statistic (on the tag join's shares
CF-160 and CF-129 rank above CF-112; on the not-found counts CF-138 and the burned stands lead).

Pins: the WHAT is filed in Board Policy 7.4 section 2 in the board's own genre (trees tallied live at the previous
measurement that are not tallied live at the remeasurement, other than trees recorded as cut, as a share of that basal
area, over the plot conditions mapped to the stand); no filed sentence names a tag, a position or a match, and the
manual's codes say what the crew did with a tag (M not found, N added), never what a tree is.

## Default path

1. Read the 2021 cycle from `cfi_database.sqlite` (`tree_meas`, status L) and the 2026 export; conform the keys (the
   export's zero-padded plot and tag strings to integers) and species (FIA codes to the company's through
   `species_codes.csv`).
2. Join each 2021 live tree to its 2026 record by plot and tag, the field's remeasurement join: every 2021 tag finds one
   record (L, D, C or M) and the N records are trees added in 2026.
3. Count each 2021 live tree with no live record under its tag (D or M) as lost, cut trees aside, and sum 2021 basal
   area by the stand of the tree's plot condition through the plot register, over the stand's 2021 live basal area.
4. Mark the stands at 15 per cent or more.

Ends on: eight stands marked, CF-104, CF-118, CF-129, CF-144 and CF-160 (the five underburned stands, 21.5 to 27.2 per
cent) with CF-112, CF-138 and CF-152.

Golden: three stands marked, CF-112, CF-138 and CF-152.

## Stump sentence

The default path joins the 2021 and 2026 tallies by plot and tag, counts every 2021 live tree without a live 2026
record under its tag as lost, and marks eight stands (CF-104, CF-118, CF-129, CF-144 and CF-160 at 21.5 to 27.2 per cent
with CF-112, CF-138 and CF-152), because it never asks whether the added trees of 9 inches and more standing where a
tree was not found are those trees tagged again; placed on the 2021 stem map they are, the burned stands lost 3.5 to
5.6 per cent, and three stands are marked.

## Three rules

- Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), serving Data
  Extraction & Conformation (ETL): two inventory snapshots of the same physical trees conformed into one 2026 fate per
  tree tallied live in 2021.
- Domain test: the deciding quantity is each stand's 2021 to 2026 loss of 2021 live basal area on remeasured permanent
  plots, a components-of-change estimate the field builds by deterministic record linkage of the two measurements on
  plot and tag number.
- Swap: replace the per-tree identity with a summary of the crews' status codes (M and D as lost, N as additions) and
  the call moves from three stands to eight; the deciding object is the tree pair across the two snapshots, so the GSDS
  swap of method changes the call, and a generic sort or filter of the codes cannot file it.
- Layer 1: two collectors' schemas (FieldCruise's integer plots, tags and company species codes against the contract
  export's padded strings and FIA codes, the species list crosswalking them); the stem map held once per tree in the
  database while the 2026 crews measure positions afresh; plots mapped into two conditions since 2021, the register
  giving shares and the trees a condition id; heights blank for the smoke week of July 20 to 24, returned in a
  separate September file; cut trees from the 2023 road clearing; a 2012 thinning's cut records and earlier deaths in
  the history; tags thrown away from the company's bags leaving gaps; trees the 2021 crew passed over; found tags
  entered beside an added tag. Each is written by its system and none is placed to be caught.
- Layer 2: identity resolution across two snapshots of one cohort where the identifier was destroyed for a subset and
  reissued; the choice that flips the call is whether a 2026 record coded as added is the same tree as a 2021 record
  coded not found, settled by the units' own attributes rather than the key.
- Decisive step: recognising that on these plots the tag is not a stable identifier, and that the added trees of 9
  inches and more standing where a tree was not found are those trees with new tags, from the stem map (a position
  within 2 feet, the same species, five years of growth).
- Not semantics: reading every field and code right (M not found, N added, the condition ids, the FIA crosswalk, the
  padded keys, the policy's population) still leaves the tag join on eight stands, because the codes record what the
  crew did with each tag and no field or definition says which added trees stood in 2021.
- Not rule application: no filed rule or procedure matches a 2026 record to a 2021 tree, so executing Policy 7.4 and
  the manual on the tag join files the eight stands. Measured spread of the enumerated family on the set: the tag join
  8 stands, not-found trees set aside 2, passed-over trees taken into 2021 8, plot netting 3, stem-map matching 3;
  standing family once the records are read: stem-map matching (48 of 48 tolerance settings, 2 to 6 feet, four growth
  windows, species on or off, one linkage; spread zero on the set and on every share) and plot netting (same set,
  cannot write the per-tree fates). The tag join stands outside it because the records refute it, quietly: 371 trees
  of 9 to 30 inches it calls lost have an added record of their species within 2 feet of them, and nothing but that
  cross-file spatial comparison says so.
- Analyst test: a strong analyst who reads every field and rule correctly joins 2021 to 2026 by plot and tag, counts
  dead and not-found trees as lost under Policy 7.4, and marks eight stands (CF-104, CF-118, CF-129, CF-144 and CF-160
  with CF-112, CF-138 and CF-152).
- Estimand: Board Policy 7.4 section 2 (`policy/salvage_marking_policy_2026.pdf`): population, the trees tallied live at
  the 2021 measurement on the plot conditions mapped to the stand (closed, nothing unobserved); outcome, not tallied live
  at the 2026 remeasurement, trees recorded as cut aside; unit, basal area at 2021 diameter; comparison, 15 per cent or
  more of the stand's 2021 live basal area; window, the 2021 measurement to the 2026 remeasurement.
- No decoy: nothing is planted to be caught: the not-found and added codes are the crews' own records of what they
  found; no memo, briefing, draft or stakeholder figure argues the eight stands; no block is copied; the burn and fire
  reports describe operations and never mortality.
- No certified replay: no certified or published figure exists to reproduce; the pack ships no mortality, stocking or
  volume summary at any grain, so the method is not recovered by matching a total.
- Lesson: an identifier join between two counts of one physical population is only as good as the identifier's
  survival; where the identifier can be destroyed and reissued, the second count's additions are reconciled against the
  first count's losses by the units' own attributes before any loss rate is filed, and no build on file teaches it.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 the tag join (eight stands) | no | no | yes, the field's remeasurement join | no | no | no | no | readable |
| 1 not-found trees set aside (two stands) | yes, M reads not found | yes, the status column | yes, missing is not dead | no | yes | no | no | readable |
| 2 passed-over trees taken into 2021 (eight stands) | no | yes, the N code | yes, the missed-tree convention | no | no | no | no | readable |
| 3 (decisive) added trees placed on the 2021 stem map (three stands) | no, no sentence names a tag, a position or a match | no, no column marks a re-tally or a prior tag | no, the reflex is rung 0 and lands on eight | no, no control or summary ships | no, the battery finds no duplicate row, orphan key or bad code | no, a per-tree spatial comparison across two files | no, the stem map and the 2026 positions are the inventory's relocation records | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "15 per cent or more" | share at or above 15 | above 15 | same call | same call: no stand within 9.4 points of the line |
| SF2 | "trees tallied live at its previous measurement" | the 2021 cycle's L records | also the trees the 2021 crew passed over, taken into 2021 | same call | Policy 7.4 section 2, "tallied live at its previous measurement"; same call (9 trees) |
| SF3 | "not tallied live at the remeasurement" for a tree not found | counted (no live record of the tree) | set aside from both sides | two stands, CF-138 dropped | Policy 7.4 section 2: both sides are "the trees tallied live at its previous measurement", and a tree not found is not tallied live |
| SF4 | "other than trees recorded as cut" | out of the lost side, inside the 2021 side | out of both | same call | Policy 7.4 section 2 (the denominator is every tree tallied live); same call |
| SF5 | basal area | 0.005454 times DBH squared (manual section 2) | pi over 576 | same call, same shares | same call (the constant cancels in a share) |
| SF6 | "the previous measurement" | the 2021 cycle | each tree's latest record to 2021 | same population | same call (6,859 trees either way) |
| SF7 | "the plot conditions mapped to the stand" | each tree to its condition's stand | whole plots to the register stand | same call | manual section 1 and Policy 7.4 section 2; same call |
| SF8 | the share's arithmetic | ratio of tree sums per stand | mean of plot shares | same call | Policy 7.4 section 2 (basal area over basal area); same call |
| SF9 | "stand" | the register's stand ids | the stand table's ids | same call | same call (one set of 22) |
| SF10 | "the remeasurement" | the 2026 export's statuses | with the September revisit | same call | same call (the revisit carries heights only) |
| SF11 | the comparison's rounding | unrounded share against 15 | the share at one decimal | same call | same call |
| SF12 | a tree entered under its found tag and under an added tag | live | live (both records are live) | same call | same call (160 trees live on every route) |

## Ladder

| Rung | Route | Set | Dies to | Carrying files |
|---|---|---|---|---|
| 0 | tag join, D and M lost | CF-104, CF-112, CF-118, CF-129, CF-138, CF-144, CF-152, CF-160 | 371 added trees of 9 to 30 inches stand within 2 feet of not-found trees of their species | database `tree`, 2026 export |
| 1 | not-found trees set aside | CF-112, CF-152 | Policy 7.4 section 2 counts a tree not found as not tallied live (CF-138 falls to 8.2) | policy |
| 2 | added trees of 7.5 inches and more read as passed over in 2021 and taken into 2021 | the eight of rung 0 | the same stem-map fact: the trees "passed over" stand on not-found trees | database `tree`, 2026 export |
| 3 | added trees placed on the 2021 stem map | CF-112, CF-138, CF-152 | (golden) | database, export, register |

- **Margins:** under the golden every stand sits 9.4 points or more from the line (CF-118 at 5.6, CF-152 at 34.3, CF-112
  at 27.0, CF-138 at 59.0); under the tag join every burned stand is over 21.4 (6.4 points or more over the line); under
  rung 1 CF-138 is at 8.2. Every stand that is neither burned nor killed by beetles or fire stays under 11 per cent on every
  route.
- **Worth of the decisive step:** 17.9 points or more on each burned stand (up to 23.5); the set moves by five stands.
- **Position and dominance:** a designation set, so no rank; the decisive step alone moves the tag join to the golden
  (R3b), and no cheap route (tag join, not-found aside, passed-over) lands it (G8). Plot netting lands the set, as a
  member of the standing family that cannot write the fates.
- **Pricing sequence:** (1) the residue the WHAT leaves is the identity of each added tree, a method with no knob: every
  tolerance from 2 to 6 feet gives one linkage (partners within 2 feet, every other tree 6 feet or more away);
  (2) the call needs each burned stand down 6.5 points or more and the 371 re-tallied trees move each by 17.9 points or
  more (up to 23.5);
  (3) the one-group-by route is the tag join and files eight; counting added trees per stand does not recover the
  golden, because 604 of the 1,135 added records are new trees; (4) nothing is estimated: the step replays recorded
  positions, so there is no standard error to price; (5) the answer is a verdict per stand 9.4 points or more from the
  line; (6) no variance is corrected; (7) the linked pairs are exact and hand nothing over, since no column marks them;
  (8) the reflex sweep runs as code in `checks.py` (R3b, G8): tag join, not-found aside, passed-over, plot netting and
  linking from the not-found trees.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | trees tallied live in 2021 on the stand's plot conditions | Policy 7.4 section 2; closed cycle, nothing unobserved; SF2, SF6 |
| 2 Unit of account | the tree, its basal area at 2021 DBH; the stand for the call | Policy 7.4 section 2 |
| 3 Attribution window | 2021 measurement to 2026 remeasurement | Policy 7.4 section 2; every record inside its cycle's field dates |
| 4 As-of dating | the 2026 remeasurement as delivered | one export and one height return, nothing dated after 2026-10-01 |
| 5 Version basis | one 2026 export, the database as stored | C1: the revisit carries heights only (SF10) |
| 6 Denominator | basal area of every tree tallied live in 2021, cut trees inside | Policy 7.4 section 2; SF4 same call |
| 7 Weighting | ratio of tree sums per stand | Policy 7.4 section 2; SF8 same call |
| 8 Window length | five years | Policy 7.4 section 2 names 2021 and 2026 |
| 9 Boundary inclusivity | 15 per cent or more | C1: nothing within 9.4 points (SF1) |
| 10 Rounding path | shares, basal areas and volumes rounded at the stand | the prompt's closing sentence; A6: per-tree basal area to the thousandth moves nothing, net volume is whole board feet per tree |
| 11 Tie-break | none needed | L1: no added record has two candidate trees |
| 12 Maturity and censoring | closed remeasurement | every 2021 tag carries a 2026 status (the crews' list) |
| 13 Order of operations | identity first, then conditions, then sums; volume by logs, class, table, cull | manual section 3 for the volume order; C1 for the rest |
| 14 Row order | none | C1: joins and sums are order-free |
| 15 Duplicate resolution | a tree entered under two tags counted once | C1 on the call (SF12); the asks' device |
| 16 Identity normalisation | padded keys to integers; FIA to company species codes | the species list; R2: species check on or off gives one linkage |
| 17 Netting against gross | per-tree fates, no netting | plot netting gives the same set (G8 note) |
| 18 Dimensional units | inches, feet, square feet per acre, board feet | manual: Table 1 in tens of board feet, basal area constant |
| 19 Code and status semantics | L D C M N as the manual lists them | manual section 2 codes; SF3 by the policy; never the stump |
| 20 Integerisation | whole board feet per tree | cull in tens of per cent (A6); rounding at the stand |
| 21 Clause scope | section 2 per stand per remeasurement | Policy 7.4 section 2 second sentence |
| 22 Forward window contents | none | retrospective quantity: the cycle the policy measures is closed |

## Literal reader

Executed word for word, Policy 7.4 section 2 counts a 2021 tree as lost only when no live 2026 record of that tree
exists, and the records show which added trees are 2021 trees (each within 2 feet of a not-found tree of its species and
nine inches or more across, every other tree 6 feet or more away, one linkage at every tolerance from 2 to 6 feet);
every other reading of a term is SF1 to SF12, each ruled out by a quoted sentence or the same call, so the literal
reading files CF-112, CF-138 and CF-152.

## Oracles

- `operations/aerial_detection_survey_2025.csv` (distractor): beetle polygons over CF-112 and CF-152 and light
  activity elsewhere; ties under the tag join and the golden (both mark the beetle stands), arbitrates nothing.
- `operations/prescribed_burn_reports_2024.pdf`: char heights and holding; consistent with the tag join's fire
  mortality and with the golden; ranks nothing.
- `operations/juniper_saddle_fire_report_2025.pdf`: the CF-138 overstory largely killed; ties under the tag join and the
  golden, contradicts only rung 1.
- `gis/stand_table_2026.csv`: treatments and plot counts; identical under every route.
- No control ties only under the golden; no summary of any graded quantity ships.

## Ask sheet

- **Ask B, every stand's 2026 live basal area per acre** (22 figures, one decimal). H18 home: a component of the call's
  case, the stocking each stand carries into the 2027 season, which Policy 7.4 section 3 asks the board to see. Primary
  device (D1, identity): 160 trees the crews entered twice, under the tag they found loose and under the added tag they
  had already nailed, at one position with one diameter, height and cull; no field marks them, a tag dedupe cannot see
  them, and the linkage that finds the re-tallied trees never examines them, because they stand on trees that were found.
  Hazards: the mapped conditions (a stand's area includes the second-condition shares of its neighbours' plots, manual
  section 1), the padded keys. Path: the 2026 export (status, dbh, cond_id, azimuth, distance), the database `tree`
  (stem map), the register (stand and both shares): 3 files, 10 columns. Stops: entries kept (every stand up 0.5 to 20
  square feet), whole plots (every stand a mapped condition touches), golden. Realism: crews tally an untagged tree,
  then find its tag at the base and record the tree under it too. Pin test: the manual's per-acre sentence fixes the
  area, and no pin names the entries.
- **Ask C, every stand's 2026 net Scribner volume per acre** (22 figures, nearest 10 board feet). H18 home: the same
  stand case (the merchantable timber left). Primary device: the same found-tag entries (law 9, one real cause feeding
  two devices), every stand 30 board feet or more; second device (D4, absence): heights blank for the plots measured July
  20 to 24, returned in `trf_height_revisit_2026-09.csv` (7 stands); hazards: the half-log rule, the six-log cap, the
  2-inch class, Table 1 in tens of board feet, cull, black oak. Path: the export, the revisit, the manual's Table 1, the
  register, the species list: 5 files, 13 columns. Stops: entries kept, revisit ignored, tens dropped, cull dropped,
  nearest half log, golden. Pin test: the manual files every volume rule; no pin names the entries or the revisit.
- **Zero-counts:** found-tag entries among the 2021 fates the call reads: 0 (A5, SF12); revisit rows in the call: 0.
- **Hazard table:** mapped conditions move Ask B on every stand they touch (22) and Ask C likewise; the revisit moves
  Ask C on 7 stands; the volume rules move Ask C on every stand; none moves the call (R2).
- **Referee:** none; the asks have no control total.

| Cracker sheet | Figures | Cracker keeps | Verdict |
|---|---|---|---|
| Ask B, 2026 live basal area per acre | 22 | 0 of 22 | miss |
| Ask C, 2026 net volume per acre | 22 | 0 of 22 | miss |

- Mirror leakage: 0.0 per cent of ask weight (the mirror, at the tag join, keeps 0 of 44 ask figures and 0 of 22 shares)
- Pair ceiling: 27.5 (cracker 45.0 on the call with every share and the CSV, mirror 10.0); the full includer that also
  merges the found-tag entries scores 100.0 and the pair with it on the call is 55.0
- Measured by: generator/ceiling.py

## Pre-ship check

- [ ] precut.py exit 0; checks.py and verify.py green; two byte-identical builds; figures_check.py exit 0
- [ ] leak.py on the cut pack; the realism sweep and the scrub; guard.py surface and heart; the card current
- [ ] golden-realism on both deliverables; reduce-house-fixes pass; submission.md from figures.json
- leak.py REVIEW, sweep 3 (manual): Table 1's tens of board feet (107, 152, 163 and the like) coincide with stand
  numbers; a printed volume table, harmless.
- leak.py REVIEW, sweep 3 (burn and fire reports): the reports name the units they burned (the five burned stands, which
  the golden does not mark, and CF-138, marked on every route); operational facts that rank nothing, harmless.
- leak.py REVIEW, sweep 3 (policy): 7.4 is the policy's number, harmless.
- leak.py REVIEW, sweep 4: the manual's and the policy's shared words (record, remeasurement, inventory, section,
  previous) are the WHAT's own nouns; neither document names a tag, a position or a match, harmless.

## Tried and rejected

- 2026-10-20, at the draw: the seed's moves (overlapping periods, a GEOID match, point estimates) as the decisive step;
  each is a filed fact or a reading here and sits on a lower rung. A period-specific population weight for split
  tracts' children was screened and set aside: it is task474's driver (a coarse total split by a period-specific
  indicator), and for a pure split any common weight leaves the child's rate equal to the parent's.
- 2026-10-20, architecture 1 spent at stage 4 (judge pass 1 SEND_BACK, Gate H rule_application; reader B landed the
  call and all 140 tract figures in about two minutes): a split 2020 tract's 2014 to 2018 rate rebuilt from the 2010
  block groups that tile it. The rebuild is exact arithmetic on published estimates, so once guidelines 3.2 files the
  estimand as the rate for the area the 2020 tract covers, the block-group table and the block relationship file
  leave only execution; without the sentence the unit is unfiled. No position holds both gates (the WHAT screen's
  own case), so the number re-roots. Ask A's reopened cases were also read straight off the event history, and the
  prompt's "median" contradicted guidelines 4.2's average.
- 2026-10-20, architecture 2 stage 4 readers 1 and 2 (pack 543b59b9): both missed the call on the default path
  (the midpoint start: Ashby, Elmwood and Ivers) and every repair-cost figure, and both took all 12 interruption
  figures by joining each ticket's address to its meters. That device kept as a hazard; Ask B's primary re-sited to
  the shared service lines. Reader 1 also read "local" as Eastern time: guidelines 2.2 now names Central time.
- 2026-10-20, architecture 2 stage 4 reader 3 (pack 5a46ee5a, shipped): missed the call (the midpoint start) and all
  24 ask figures.
- 2026-11-01, architecture 2 spent at the re-check's stage 4 (judge pass 4 NOT_DETERMINISTIC, SEND_BACK, Gate C/E
  underspecified_objective; Gate G method_or_model_selection, Gate H analytical): guidelines 2.2 file a start only for
  the called leaks, and a surveyed leak's start at the find, the previous survey, the midpoint or the seasonal
  expectation designates 0, 12, 3 or 5 districts with nothing filed ruling out the midpoint; the sentence that would
  close the fork names the decisive step, so the fork is the stump and no pin repairs it. The re-check's free-gate
  repair (the extract notes out of the pack, leak.py sweeps 1 and 12 LEAK; "our 12 districts" out of the prompt;
  survivor anatomy written, precut 61 checks, 0 WARN) went green on every free gate with no graded figure moved and
  is not shipped; the shipped pack (5a46ee5a) stays at the portal, pending.
- 2026-11-04, architecture 3 draw (the re-root after architecture 2's 11-01 SEND_BACK, run as a background agent of
  the orchestrating session, under its stop rule of forty screens across five task types): 55 candidates screened across
  the six task types that serve ETL, each with a default path ending wrong, the swap test, the survivor anatomy and the
  bin test on paper, the strongest priced in code; none clears guard.py check and the three rules together, so no card
  is registered and nothing is cut. The window at the draw is task276, task461 v2 and task193: emissions-inventory
  BLOCKs on ban.pairing and ban.subdomain against task461 v2, and the strategies binding_constraint, other and
  population_selection are banned against the three; probe cards on the other five cells clear every axis, so what
  refuses them is the mechanism, line by line below (S3.1 to S3.52, three lines holding two or more screens). Read beside task464 architecture 5's cell map
  (10-27), task479's screens 1 to 16 and task461 v2's screens 1 to 12, none of which is re-screened here.
- S3.1, the strongest, emissions-inventory, written in full. Default path: each 2026 load at a terminal's uncontrolled
  distillate bays charged by the loading-loss equation at the loaded product's own true vapour pressure (submerged
  loading, dedicated normal service), about 0.0165 lb per 1,000 gal, which files every rack far under a 10-tonne
  control threshold. Golden: a compartment whose previous load was petrol delivered through a Stage I station's vapour
  balance returns holding saturated petrol vapour, so diesel loaded into it at an uncontrolled bay pushes out about 9
  lb per 1,000 gal; the switch-loaded compartments read from each trailer's own load sequence across the main rack's
  automation export and the distillate rack's older meter system. Swap: holds (no vapour space, displacement or vapour
  balance in another field's nouns). Anatomy: Actor, Link (two systems, trailer identifiers crosswalked), Reflex,
  Back-test (the vapour combustion unit's test confirms saturation at the petrol bays), Second use, Shock and Pins all hold
  on paper. Bin: priced in proto_switch.py (session scratchpad, three seeds, six terminals): rung 0 files 0.2 to 0.8
  tonnes per rack, the compartment-history golden 10 to 125, the trailer-level shortcuts (any petrol in 2026; any
  petrol on the previous load) 2.0 and 1.6 times the golden. Dead the same hour, before any card: task461 v2 registered
  this mechanism at 03:18Z (its driver: a transfer into a container pushes out whatever the container held, so the
  release is set by the container's previous use), so the step is that build's, its honest strategy (other) is banned
  against it, and the cell is barred besides.
- S3.2, emissions-inventory, an anaerobic digester's gas holder venting at its relief valve only once a CHP outage has
  filled the holder's free volume (storage with memory): without a holder level log or a production meter the free
  volume at each outage is unidentified (Gate B); with either, the venting is one subtraction of metered flows (the
  linear death) or a row predicate on the level column (readability test 2); and its abstraction sits beside task479
  v7's (gas above a device's capacity leaving untreated).
- S3.3, emissions-inventory, prescribed and savanna fire emissions with fuel load by years since the last fire on each
  piece of ground: the field's savanna method already reads fuel age from the fire scar history (the golden is the
  method), and a within-year reburn needs a fuel load at age zero no table files (Gate B).
- S3.4, emissions-inventory, cold-start excess read from each vehicle's gap since its previous trip: the soak curve is a
  filed MOVES or COPERT function (rule application) and the gap is a sort and a difference (readable).
- S3.5, emissions-inventory, haul-road dust control decaying with time since the water truck's last pass: AP-42
  13.2.2's watering equation is filed and linear in the interval and the traffic (the linear death), and the water
  truck's log against the dust plan is record against operation alone (G3, a lone defect flip).
- S3.6, emissions-inventory, at-berth auxiliary engines on shore power, with the ship's load above the connection's
  rating met by its own engines: the plug-in log is the field's input (a header-found join), and the capped variant is
  task479 v7's driver; S3.7, the same at airport stands with ground power and air: the same two deaths.
- S3.8, emissions-inventory, portable equipment moved between permitted sites, its hours attributed through the
  transport log: attribution at a transition (G4: a sub-period error cannot carry an annual figure) under a filed rule.
- S3.9, emissions-inventory, a storage tank switched from diesel to petrol service, its register naming only the current
  product: a stored label before a silent switch, task479's ask device D2 and data semantics as a main call.
- S3.10, emissions-inventory, a batch vessel's purge venting the solvent of the previous step's wash: task479's world
  (a closed-vent batch plant) and the EIIP vapour equations filed (rule application).
- S3.11, emissions-inventory, refinery fuel gas carbon content set by which units feed the header at the hour:
  task479 v7's abstraction (a shared stream's property set by coincident contributors).
- S3.12, emissions-inventory, vapour balancing between tanks, a filling tank's vapour taken up by an emptying tank only
  when the two coincide: the coincidence family (task479 v7).
- S3.13, emissions-inventory, leaks on delay of repair venting until the turnaround: architecture 2's world (leaks) and
  the protocol's leak duration rule.
- S3.14, emissions-inventory, storage pile wind erosion per disturbance period: AP-42 13.2.5 files the per-disturbance
  method (the library test).
- S3.15, emissions-inventory, truck vapour tightness lapsed at the load date: an as-of join on a shipped key (readable)
  under a filed capture factor (rule application).
- S3.16, emissions-inventory, a recirculating scrubber's removal falling with the solvent the liquid has absorbed since
  its last change-out: the efficiency against loading is a fitted curve (Gate C) or a vendor curve that names the
  quantity (readability test 1), task479's screen 16 fork.
- S3.17, emissions-inventory, a feed additive's methane reduction lost on the days the premix ran out between
  deliveries: the swap fails (a stock-out of any input reads the same) and the ration log against deliveries is G3
  alone.
- S3.18, emissions-inventory, a marine loading's displaced vapour by the vessel's arrival tank condition read from its
  previous voyage: AP-42 tabulates loading factors by arrival condition (filed) and the cargo inspector's report
  carries the condition (a column).
- S3.19, emissions-inventory, an anaerobic lagoon's volatile solids carried month to month and reset at each emptying:
  the monthly conversion is a filed rate model and the emptying dates against the nominal plan are G3 alone.
- S3.20, emissions-inventory, a hydropower reservoir's degassing at the turbines by intake depth: the dissolved methane
  profile is sampled monthly (a model of the measurement).
- S3.21, emissions-inventory, a coal pile's reclaim order setting the fired coal's carbon against the as-delivered
  analyses: the sampling basis is a filed monitoring rule (rule application) and a lag that moves only the year-end
  stock.
- S3.22, emissions-inventory, a crematorium's mercury by the decedents' dental cohort: a composition one survey table
  hands over (task482 architecture 8's screen).
- S3.23, payment-claims, an anaesthesiologist directing more than four concurrent cases, so the cases fall to
  supervision payment: a stated rule over a hard construction (rule application).
- S3.24, payment-claims, non-emergency transport trips shared in one vehicle: a filed shared-ride rate (rule) and a
  self-join on vehicle and time (readable).
- S3.25, payment-claims, a hospice's aggregate cap under the proportional method across providers: a filed regulation
  (rule application).
- S3.26, payment-claims, single-dose vial wastage rebuilt from doses and vial sizes against the reported discard lines:
  the refund basis is the filed discard reporting (rule), and finding under-reporting is anomaly detection.
- S3.27, payment-claims, a family's out-of-pocket maximum across the medical and pharmacy vendors' accumulators: rule
  application over an identity link.
- S3.28, payment-claims, short stays discharged home with home health inside three days paid as transfers: a filed
  transfer policy and a key join.
- S3.29, payment-claims, specialty drugs dispensed by the pharmacy and billed again under the medical benefit: duplicate
  detection (a planted defect as the call, and anomaly detection ground).
- S3.30, payment-claims, retroactive re-enrolment claims after the Medicaid unwinding: the completion family (task451,
  task479 v5).
- S3.31, payment-claims, charge compression under a department's cost-to-charge ratio: the swap fails (any department
  markup ratio reads the same).
- S3.32, payment-claims, global maternity care billed at delivery, so prenatal care rendered in 2026 is unbilled for
  continuing pregnancies: task482 v14's episodes recorded only at their end.
- S3.33, payment-claims, rebate accruals at the old market-share tier after a generic launch: the contract's tier table
  (rule) over a group-by.
- S3.34, payment-claims, network adequacy against the locations providers actually bill from: the swap fails (a store
  locator reads the same) and the directory against claims is G3 alone.
- S3.35, payment-claims, a claims case definition's positive predictive value by setting, recovered from the treatment
  fills only true cases produce: task241 v2's driver in claims nouns (the abstraction test).
- S3.36, payment-claims, auto-refill shipments inflating adherence after a therapy switch: the adherence measure's
  specification is filed (rule application) and the measure is pharmacology ground.
- S3.37, payment-claims, out-of-network claims in independent dispute resolution at year end: decided awards not yet
  paid are an inner join (rule application) and pending outcomes a fitted win rate (Gate C).
- S3.38, census-register, a communal establishment's register count capped at its licensed capacity: a plausibility
  edit (rule application), and the lesser-of prints the capacity on every bound row.
- S3.39, census-register, addresses geocoded to postcode centroids placed in the wrong small area: allocation across
  areas is task486's driver, and identical coordinates are readable.
- S3.40, census-register, dwellings read as vacant from low grid import when rooftop solar covers the load: the signs of
  life family (task471 architecture 4, task464 architecture 5's three arms) with the solar register an inner join.
- S3.41, census-register, cattle on the tracing system never reported dead, caught by the herd's whole-herd test: the
  exact arm (a second register confirming every unit is an inner join, rule application).
- S3.42, census-register, a dwelling's vacancy observed only at the annual canvass taken in each ward's own month:
  architecture 2's driver in census nouns (test.own_lineage and the abstraction).
- S3.43, census-register, an address survey's unknown-eligibility cases that are vacant: the signs of life family, and
  the eligibility share is a filed response-rate convention.
- S3.44, official time-series production, seasonally closed establishments imputed as open non-respondents in the
  accommodation statistics: the pincer; the closure is confirmed by a record (a nil tourist-tax return, an inner join,
  rule application) or inferred from the unit's own past closures, which a judge reads as a competing imputation that
  only a sentence naming the step closes (the fork is the stump), and the register's establishment type is a proxy.
- S3.45, official time-series production, product relaunches under new barcodes in a scanner-data index: identity
  resolution may not decide, and the field's relaunch linking is its own method.
- S3.46, official time-series production, job vacancies as a stock on the reference date against postings in the
  month: re-timing (task123).
- S3.47, official time-series production, electricity consumption gross of rooftop self-consumption: a modelled yield
  and self-consumption ratio (a model of the measurement).
- S3.48, official time-series production, rail journeys per season ticket re-estimated from gated stations' taps: the
  audit arm (a selected subsample carried to the ungated stations, its interval wider than the step).
- S3.49, official time-series production, single against double deflation of a volume index after an input price
  shock: the field's textbook method is the golden (1.1b); S3.50, a rent index as a stock or a flow: a WHAT fork; S3.51,
  outlet substitution in a matched-outlet price index: a contested method (Gate C).
- S3.52, item-response-theory-test-equating and data-integration, four screens: forms assigned by test centre rather
  than spiralled (the random-groups precondition) is card 3's method and the cell's conversion closure; testlet local
  dependence is a model fork; instructional-weeks norms are a conversion; namesakes over-merged by a master patient
  index, split where their stays overlap, is linkage error propagation (task449, task456, task468, task473) with a
  partial correction landing further away (law L3).
- The three strongest, for the orchestrating session: S3.1 (blocked by task461 v2's registration of the same driver and
  by the window), S3.44 (blocked by the ETL pincer and the fork-is-the-stump test), S3.35 (blocked by the abstraction
  test against task241 v2). What the draw leaves: the ETL ground outside emissions-inventory is closed on mechanism by
  this pass and the earlier maps; emissions-inventory reopens to a new physical mechanism (neither capacity, task479 v7,
  nor a container's previous use, task461 v2) once task461 v2 leaves the three-build window.
- 2026-11-04, S3.44 re-tested on the orchestrating session's ruling (C2 confirm and C1 converge priced in
  proto_s344.py, session scratchpad, four seeds, eight regions, six rival corrections): dead. With closure calendars
  stable year to year, the field's own seasonality-aware imputation (same month of last year's final times the
  stratum's year-on-year ratio, R0b) lands within 0.6 to 1.7 per cent of the truth and agrees with both closure-aware
  corrections (last winter's status, a multi-winter pattern), so the easy route sits inside the golden family and two
  corrections survive; with calendars shifting (establishments starting or stopping winter closure, a shock closing
  more this winter) every family misses by 10 to 36 per cent on its worst region and the back-test's best basis (a
  modelled closure probability, 8 to 13 per cent off) selects nothing with margin, because the deciding configuration
  (this winter's new closures) is out of sample. No C2 criterion or C1 world serves both horns.
- 2026-11-04, after the S3.44 re-test, on the orchestrating session's second ruling (move the world; any ETL task type,
  house domains accepted, a fresh physical or behavioural mechanism): the window moved to task461 v2, task193 v3 and
  task192 v4 at 04:24Z, freeing binding_constraint and banning grain_or_unit. Seven more screens died before the draw:
- S3.53, census-register, dual-system estimates short for young men because the census and the coverage survey miss
  the same men, corrected by the sex ratio that birth and migration records fix: task471 v5's driver (the abstraction
  test).
- S3.54, item-response-theory-test-equating, rapid guesses in a low-stakes interim test scored as wrong answers: the
  estimand (achievement) is the scoring model's own construct, so the sentence closing a judge's fork would say that
  answers given without engagement are not evidence (the fork is the stump), and the rapid-guess threshold is a knob.
- S3.55, data-integration in an accounting world, a subsidiary's income translated at the year's average rate across a
  mid-year devaluation: the standard's own rule (rates at the transaction dates) is the golden, so reading it flips
  the call (data semantics and rule application at once).
- S3.56, data-integration in a fleet world, off-road distance for a road-user charge refund from GPS tracks that
  under-read winding forest roads: two road-type factors fitted from the hubodometer totals is an estimation grouping
  (1.1c).
- S3.57, payment-claims, grace-period members retro-terminated after the eligibility snapshot: the premium ledger
  makes it an inner join under a filed grace rule, and without it a forecast of who pays (the pincer).
- S3.58, data-integration in a contact-centre world, offered calls that include the attempts the carrier blocked when
  every trunk was busy: the population (the WHAT screen).
- S3.59, data-integration in a facilities world, office occupancy from each room's carbon dioxide balance: a model of
  the measurement with free generation and ventilation rates (the pincer's sampled arm).
- The draw that followed (energy-based groundwater extraction converted at each hour's pumping head, S3.60) is the
  `## Draw` above; priced first in proto_lift.py (session scratchpad, six seeds): with each deep well tested once at
  the confined aquifer's late-summer low, the test's rate files the ranch 5 to 6 per cent short of the truth (the deep
  wells 8 to 9 per cent), run hours times tested flow 7 to 8 per cent, an average or the nearest of the tests about 5,
  and every conversion at the recorded head within about 1 per cent, the family agreeing to about 1 acre-foot on the
  ranch; with the allocation set 2.5 per cent under the golden, every easy route buys nothing and the golden family
  buys 380 to 400 acre-feet on every seed. A first cut with half the deep wells also tested in an earlier spring
  priced the averaging route inside the golden (the spring and summer tests bracket the season), so the pack ships
  one current test per pump and the superseded reports only for pumps replaced since.
- 2026-11-04, architecture 3 abandoned at the stage-4 re-judge (pass 2 NOT_DETERMINISTIC, competing_defensible_answer; the pass 1 FIX_NOW filing pass, target.zip 80bcc4b9, moved no figure): Gate C on the main call with Gates G and H passing, so by the gate table it was not spent; it was re-drawn rather than repaired because separating the two conversions needed a new data organ, a metered deep well, inside a 24 acre-foot decision margin. nothing shipped forced the head-adjusted conversion over holding each test's kWh per acre-foot constant. The reports' printed definitions say how the test-day figure was derived, not that energy converts at a moved head on other days, and the loggers show the head moved, which is not the same thing. The only metered wells were the upper-aquifer ones, where the candidates coincide (constant even fits them better, +0.7 against +1.1 per cent annual bias), while no deep well, where the methods diverge by about 6 per cent, was metered: constant files 15,020 and no purchase against the golden's 15,583 and 250, the golden 24 acre-feet inside its 50-acre-foot block. The rule it paid for: an open method needs shipped instances where the candidates diverge, separating them with margin, and a decision band wide against every candidate's spread. The second reader's realism tell: one sentence ("original bowls, 1998 installation; rebuild recommended") sat verbatim on reports from two different firms.
