# task448 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task448.json`, registered 2026-10-12 (guard WARN repeat.gate_g, answered below).
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / Data Extraction & Conformation (ETL). The ETL lane has six client task types; this seed's world (HMDA lender volumes) sits in administrative-data quality, where the deciding quantity, each lender's true volume when the register misses whole producers, is what official statistics estimates by dual-system estimation.
- **Seed:** ET05 (`analytical_tasks/07_data_extraction_conformation/ET05_hmda-lender-market-share-composite-key.md`), header and Situation only: the HMDA world, a lender league table and a decision taken from it. The seed's two-part-key and purchased-loan traps are data semantics and rule application, so neither is used; the pitfall is re-found from the data.
- **Shape:** 01, ranked list under a cap (the five lenders recruited first, in order, each with its two-year volume).
- **Strategy:** composition_mix. The second list's capture is a mix over recording routes, and the registered producers and the missing producers hold different mixes.
- **World:** a statewide homeownership nonprofit in Kansas runs a down-payment assistance program through participating lenders. For 2027 it extends the program to eight non-metropolitan central Kansas counties (Saline, McPherson, Dickinson, Marion, Rice, Ottawa, Ellsworth, Lincoln) and recruits first the five lenders that made the most home-purchase first-lien mortgages there in 2024 and 2025. HMDA covers a depository only if it has an office in a metropolitan area, so the local banks and credit unions headquartered in these counties never report. The nonprofit buys a county recorder vendor feed of purchase-money mortgages for the eight counties.
- **Forum and forcing event:** board_of_directors (the nonprofit's board approves the 2027 recruitment list), vote_or_meeting (the December board meeting). Organisation nonprofit_or_charity, role research_desk (the research and data manager prepares the list). Personas from `guard.py names --geo "United States" --seed 448`: Laura Cohen, Maxwell Ewing.
- **Data-native sentence:** HMDA drops every lender with no office in a metropolitan area, and the recorder vendor flags a purchase mortgage only when it can pair it with the deed, which it does for closings that record the two in one package and often fails to do for lenders that record their own mortgage afterwards, so the lenders the register misses are the ones the second list undercounts.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, census-register-administrative-data-quality 1 (dual-system estimates within post-strata, after erroneous enumerations): teaches that one pooled Lincoln-Petersen on raw counts is biased when capture is heterogeneous and correlated across sources; here the register's misses are whole producers (zero capture), so the second list's capture measured on the overlap is carried to them by recording route, and the erroneous enumerations are the vendor's non-purchase pairings and re-recordings.
  - `stumping/references/strategies.md` Part 6: a move visible in the schema and a reflex correction are dead, so the stratifier is no column (route is built from the paired document numbers and dates) and county, charter and year stratification each land wrong.
- **Same-puzzle and abstraction:** gap population, pattern E and Gate G method_or_model_selection repeat seven older builds (task30, task31, task500 v2, task53 v2, task57 v19, task69 v2, task76 v2), each differentiated on the card. Nearest drivers: task62 (a unit's count completed from a second register that is complete for what it holds, a union), task229 v3 (a counting point's pass rate), task230 v2 (a detector's hit rate falling as targets get rarer). Stripped of nouns, none has a register missing whole producers completed from a second list whose capture differs by filing route and is measured only on the producers both lists hold.
- **Guard WARN repeat.gate_g (task185):** task185 selects a value-dependent conversion between two measuring devices for an anomaly count; here the selection is a coverage estimator's post-strata. Different mechanism, same Gate G label.

## Default path

1. Download the Kansas HMDA loan-level files for 2024 and 2025 and keep originated loans (action_taken 1) for home purchase (loan_purpose 1), first liens (lien_status 1), on properties in the eight counties.
2. Count the loans by LEI over the two years and name each LEI from the reporter panel.
3. Rank the lenders and take the five largest as the lenders to recruit first.

Ends on: recruit the five largest HMDA reporters, two national nonbanks, two regional banks and a third nonbank (prototype: 610, 515, 415, 335 and 318 loans over the two years; the generator fixes the names and figures).
Golden: two local lenders HMDA never sees are among the five (prototype: a Salina bank about 565 and a central Kansas credit union about 455, behind the largest nonbank at 610 and ahead of a regional bank at 415).

## Stump sentence

The default path recruits the five largest HMDA reporters (prototype: 610, 515, 415, 335 and 318) because step 1 counts only the lenders HMDA covers, and HMDA's location test drops every bank and credit union with no metropolitan office; counted from the recorder feed at the feed's capture for their own recording route (about 0.60, against about 0.97 for closings that record the mortgage with the deed), a Salina bank and a central Kansas credit union are among the five largest lenders in the region.

## Three rules

Domain test: completing an administrative register that misses whole classes of producers by dual-system estimation against a second, incomplete source, within post-strata where that source's capture is homogeneous and after its erroneous enumerations, is official statistics' coverage-measurement method; with another field's nouns (a credit model's default rates, a pricing grid) there is no register coverage or capture to estimate, and the task stops reading the same.
Analyst test: a strong analyst who conforms the LAR and the recorder feed, resolves the mortgagee names and removes the feed's non-purchase recordings sees that HMDA misses the rural lenders, measures the feed's capture against the reporters' HMDA counts and scales the rural lenders' feed counts by it; the pooled capture (about 0.88) leaves the credit union below the fifth reporter, because the route it records by is captured at about 0.60.
Layer 1: two activity years of the HMDA public loan-level layout with every action and purpose, purchased loans and rounded amounts; eight county files from one recorder vendor with schema drift between deliveries; mortgagee names as indexed (MERS nominee phrasing, abbreviations, suffixes) resolved through an alias register; the vendor's purchase flag carrying refinances recorded with a quitclaim deed, re-recorded mortgages and seller-financed notes; the HMDA reporter panel and a state lender register; a parcel-to-tract crosswalk on 2020 tracts.
Layer 2: the second list's capture is not one number; it is homogeneous only within recording routes, so it is estimated on the reporters within each route and carried to each non-reporting lender by its own route, after the erroneous enumerations leave both lists.

## Readability screen

To be written at design (stage 2).

## Semantic fork table

To be written at design (stage 2).

## Ladder

Prototype (scratchpad `t448/proto.py`), to be fixed at design: HMDA only names five reporters; HMDA plus the feed unscaled, and the feed scaled by the pooled capture (0.88), add the Salina bank but not the credit union; capture by charter type mixes routes; route capture with the erroneous enumerations kept puts a trust-refinancing bank in; only route capture after the erroneous enumerations gives the golden five.

## Closure table

To be written at design (stage 2).

## Literal reader

To be written at design (stage 2).

## Oracles

To be written at design (stage 2).

## Ask sheet

To be written at design (stage 2).

## Tried and rejected

- A bank's CRA officer picking a peer group (the seed's decision), drawn 2026-10-12: the guard's ban.org_family (financial_institution, task185) blocked it; the decision moved to a homeownership nonprofit recruiting participating lenders, which keeps the league table and needs the unregistered rural lenders even more.
- A committee as the deciding forum: ban.forum against task181 v4; the nonprofit's board decides.
