# task486 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

Architecture 2, drawn 2026-10-21, re-rooted fresh after architecture 1 (a privacy-protected census release's small-area
counts for senior-services provider areas) was spent at stage 4 on the judge's SEND_BACK. The author's rule holds: no
retirement, a fresh rebuild. The new draw keeps the lane's objective and the task type and takes a new world.

## Draw

| Field | Value |
|---|---|
| Domain and task type | general-statistics-data-science / data-integration-record-linkage-entity-resolution (ETL) |
| Objective | Data Extraction & Conformation (ETL): six sources conformed into one count of people served, once each |
| Niche | resolving a privacy-preserving linkage service's pairwise findings across four Continuums of Care's HMIS exports, a domestic violence coalition's comparable database and a health care for the homeless clinic into the people the region served in FY2026, the count the 2027 regional fund is split on |
| World | the Calvera Valley region of an unnamed U.S. state: four counties (Calvera, Mardell, Ostry, Pellam), one Continuum of Care each, the Calvera Valley Homeless Data Partnership as the nonprofit HMIS lead and integrator, the counties' Regional Fund Committee |
| People | Kathleen Carlson (the Partnership's director of data, the requester), Joshua Bell (the state linkage unit's lead, redrawn on 2026-10-23 because Andrew appeared in task478), Gina Bryant (the Partnership's executive director); drawn with `guard.py names --geo us --seed 486` |
| Stakeholder | the Partnership's director of data, who heads the HMIS lead's data office (statistical_office_head) and prepares the 2027 allocation table for the Regional Fund Committee |
| Forum, forcing event | the Regional Fund Committee (committee_or_panel); the fiscal agent's 2027 contract renewals with each recipient, written at the adopted amounts from 1 January 2027 (purchase_order_or_contract) |
| The call | how much of the 2027 Calvera Valley Regional Homelessness Fund each Continuum and the DV coalition receive, under the committee's policy that splits the fund on the people each served in FY2026 (1 October 2025 to 30 September 2026), each person counted once across the region and placed with the Continuum of their latest FY2026 entry |
| Decision type, unit | allocation_to_total; currency, resting on counts of people |
| Shape | 03, bridge between totals: from the sources' client records active in FY2026, through the people the linkage resolves, to each recipient's count and dollars |
| Deliverables | `calvera_2027_fund_allocation.xlsx` (the allocation, the bridge, the asks); a chart if the bridge reads better drawn |
| Card | `.claude/skills/fingerprint/cards/task486.json`, architecture v2, first registered 2026-10-21 03:15 UTC, re-filed on 2026-10-23 at stage 2 against that day's window, architecture 1 in its lineage with its fate |
| Guard | re-filed 2026-10-23 against the window task483, task275, task179: the forcing event budget_or_appropriation and the role research_desk were banned, so both were redrawn to what the policy and the requester actually are (the fiscal agent renews each recipient's 2027 contract at the adopted amount, the event that makes the figure due now, the committee's meeting being the forum; the requester heads the Partnership's data office, the HMIS lead's own data function). WARN only: three_rules.strategy_risk (identity_resolution; answered in `## Three rules`), repeat.gate_g (etl_conformance beside task483: the mechanism here is the resolution of pairwise findings into persons, task483's was a register's grain), overuse.objective (the lane's objective) |
| Nearest drivers | task471 v3 lineage 0.07, task98 v2 lineage 0.06, task249 v4 lineage 0.06 (distinct identifiers after an idle expiry, recovered by replay: a different mechanism), task448 0.05; `slots` on the mechanism's words (transitive closure, connected components, unduplicated count) and on the setting's (homeless, Continuum, shelter, outreach, HMIS) returned nothing on file |

**The decisive step.** The state linkage unit compares client records from different sources on hashed identifiers and
reports each compared pair's score and finding (a link at 9.0 or above). It does not group records into people; the
Partnership does. A record that carries less identity, an outreach intake with an approximate date of birth or the DV
coalition's records (birth year only, by its confidentiality policy), scores as a link against every client of that name,
birth year and gender, so one such record can link to two different people. Merging every chain of links (connected
components, the generic step) then joins two clients one Continuum's own HMIS keeps apart. Resolving the findings so that
no person holds two client records of one source, each chain cut at its weakest link, restores them. The step is the
task type's own: the client library's Layer 2 pattern 3 for data integration (resolve pairwise matches into consistent
entities; summing or chaining pairwise links miscounts entities).

**Default path and golden (to be fixed in stage 2).** The default path reads every file right, takes the unit's links,
merges every chain and counts the merged groups active in FY2026: about one person in fifty short region-wide, most of it
in the downtown Continuum (Calvera), whose street outreach carries most of the approximate birth dates and whose names
concentrate most, so its share of the fund falls. The resolved count restores them. The figures and the ladder are set
by the stage 2 prototype.

**Stump sentence (draft).** Merging every record the linkage unit linked, directly or through other records, files the
region and Calvera short of the people they served in FY2026 and moves the 2027 fund away from Calvera, because records
carrying only a birth year link to every client of that name and year, so chains of links join people one Continuum's own
HMIS keeps apart.

**Data-native sentence.** A client record that gives only a birth year matches every client of the same name, year and
gender, so where two such clients sit in one Continuum a single partial record links to both.

**Retrospective count, forward call.** The fund is for 2027 contracts, a window not yet open; the quantity it is split on
is FY2026, closed on 30 September 2026, because the committee's policy files last fiscal year's people served as the
basis (the reason this build's deciding count looks back).

## Three rules

Draft at the draw; completed in stage 2 with the default path's figures.

Domain: the deciding quantity is the number of distinct people across six sources, estimated by resolving a linkage
service's pairwise findings into persons consistently with each source's own deduplication, the core of entity
resolution; with another setting's nouns the task still turns on that resolution, which is this task type's own analysis.
Layer 1: HMIS exports in the HUD CSV layout with one Continuum on an older destination list and date format, the DV
coalition's workbook with birth year only and its own codes, the clinic's encounter extract with homelessness flagged per
encounter, the pair file keyed by source-prefixed record keys across both fiscal years, approximate dates of birth under
data quality codes, open-ended night-by-night enrollments, projects moved between Continuums at a redraw.
Layer 2: pairwise links are not transitive; persons must hold no two records of one source, and a chain that would join
two is cut at its weakest link.
No decoy: nothing is planted; partial identities come from street outreach and the coalition's confidentiality policy,
and every link is the unit's honest pairwise finding.
Not semantics: reading every key, grain and code right still leaves the analyst with connected components and the short
count.
Not rule application: no shipped document says how links become people; the unit files pairwise findings and each source
files its own grain, and resolving them is the analysis.

## Tried and rejected

- 2026-10-21, the seed's world (ET43, U.S. pharmaceutical exports to Germany against Germany's imports from the U.S.):
  every lever is a filed concept (CIF against FOB valuation, country of origin against destination, recording date,
  classification) or an estimated rate small against the gap (freight margins by weight) or a composition rate of the kind
  task481 just spent (the asymmetry ratio by product mix, the re-dispatched share through Dutch hubs); dropped before any
  data was cut.
- 2026-10-21, survey research's census-register task type for this world: the honest home, but its ETL pairing was taken by
  task479's re-root (BLOCK ban.pairing, and ban.artifact on published_series); the build is filed in data integration.
- 2026-10-21, a single-area figure or a per-area allocation as the call: the allocation's decision type repeats task471's
  puzzle triple (population, none, allocation_to_total) and the per-dollar rounding cannot hold two unbiased estimators in
  one bin; the call is the census table itself, counts to the nearest ten.
- 2026-10-21, noise added to each cell at the block level with no structural zeros (the demonstration-data behaviour):
  four to five per cent of the county's residents landed in blocks with no housing, a symptom the hygiene battery flags
  and a share no production release would show; the release leaves such blocks empty, which also silences the device.
- 2026-10-21, block groups alike in age within a tract: the tract route then matched the golden on most counts and left
  two estimators in one bin for some and not others; block groups now differ in age within a tract, as they do, and the
  tract route is a rung (6 of 12 off).
- 2026-10-21, ask B's prior-number deaths left to chance: a death hazard spread over a decade put no unreported death under
  an earlier number in the four rural providers; the July 2026 review not held, and at least one such death per provider,
  give the device mass everywhere.
- 2026-10-21, each block's total held to its own precise count (as the production release holds block totals) with the
  age cells forced to it: on paper the drift between blocks turns into flattening inside each block toward the 46
  cells' even share, which moves a rural block's 60-and-over count only by the gap between its true share (about 31 per
  cent) and the cells' 35, a few residents per area against the 40 to 190 the per-cell processing moves; kept the
  per-cell processing, under which small blocks publish more residents than their housing would hold.
- 2026-10-21, architecture 1 (each provider area's census-day counts built from the release's block groups, cut groups split by census-day housing units, against the block sum), spent at stage 4: the judge returned NOT_DETERMINISTIC and SEND_BACK, competing_defensible_answer, because nothing shipped showed the published block counts biased, so the block sum read as a defensible estimate (Gates G and H passed); documenting the bias would leave the step to whoever reads the notes. Both scored readers filed the block sum (0 of 12) and kept all 12 service figures: the roster's meals_per_day capped the re-sent rows and the registry's links chained the earlier numbers, so both devices sat on the careful path.
- 2026-10-21, architecture 2 draw, screened before the entity-resolution step (each dead on file or on measurement):
  left truncation in an asset or licence register (task133's delayed entry, rejected again in task262, task257, task265);
  the oldest-old counted by extinct generations (task228); non-detects under several reporting limits (task189); triple
  collocation (task228); age heaping (task230's rejected draw); a lowered reporting threshold bridged by an overlap ratio
  (task481's conversion rates); a benchmark-to-indicator ratio carried past the last benchmark (task457's report against
  final); landfill first-order decay (task480's age-declining increments); load estimation from sparse samples (Jensen,
  task229); a staggered rollout of a measurement change (task453, and task480 v2's meter exchange in flight); pooled
  medians from brackets (the never-average reflex, task480's screen); degree-day temperature adjustment (fresh, but a
  per-unit degree-day regression is the textbook route and lands it); hedonic quality adjustment (the estimand's own words,
  constant quality, name the method, and the specification family forks); equipercentile against linear equating on random
  groups (task450's ground, a moderate stump); Fellegi-Sunter frequency weights (the linker's own error is task468's).
- 2026-10-21, architecture 2 draw, the card's first labels: population, G2 or G12 and method_or_model_selection repeat four
  older builds' signature (test.same_driver_older, test.same_puzzle_older against task142); relabelled G17 with G2 beside
  it and gate etl_conformance, the call being the region's conformed count with the resolution inside it. Then task251 v5
  entered the window and blocked local_government and operations_log: the integrator is the region's nonprofit HMIS lead
  and the context artifact the published point-in-time count.
- 2026-10-21, architecture 2 draw, the prototype (20,000 people over two fiscal years, half of the names drawn from a
  concentrated list): chaining every link left the region 387 short, 115 of the chained groups holding two records of one
  source and 112 holding two people with no such conflict. A merge with no conflict cannot be refuted by anything shipped,
  so the generator keeps every wrong link inside a conflict (no undetectable merge) and gives every partial record its own
  person among the records it links, or the resolved count would differ from the people served by a quantity no method
  can see.
