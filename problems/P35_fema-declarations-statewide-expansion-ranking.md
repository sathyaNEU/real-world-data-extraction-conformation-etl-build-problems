# P35 — Repeat-disaster counties across a FEMA region: "Statewide" rows, program flags and distinct disasters

| Field | Value |
|---|---|
| Domain | Emergency management / hazard mitigation planning / public-sector analytics |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (15 counties for a regional mitigation initiative) |
| Core technique | Expanding aggregate designations (statewide) to member units; counting distinct events rather than rows; program- and type-based filtering; county-equivalent conformance across states |
| Trap family (honest data) | Statewide rows left unexpanded (or expanded to the wrong county list); rows counted instead of distinct disasters; emergency/fire declarations included; biological (pandemic) declarations not excluded |
| Primary sources | OpenFEMA Disaster Declarations Summaries (v2), Census county reference files |

## 1. The real-world project

A FEMA regional office funds a multi-state **repeat-impact mitigation initiative** for the **15 counties** (or county
equivalents) with the most major disaster declarations including Public Assistance over 2004–2023. The analyst counted
rows per county name in the declarations dataset. Counties in a state that often receives statewide PA declarations
barely appeared; a county with many amended declarations appeared twice under two spellings.

## 2. The business decision (one deterministic recommendation)

**Which 15 counties in the region receive the initiative, and which county is 16th?**

Rules (initiative method):

* Declarations: `declarationType = DR`, `declarationDate` in 2004-01-01 … 2023-12-31, `paProgramDeclared = 1`,
  `incidentType ≠ Biological`.
* County identity = 5-digit FIPS (`fipsStateCode` + `fipsCountyCode`). A row with county code `000` ("Statewide") applies to
  **every county-equivalent in that state's county list in effect on the declaration date** (reference file in folder).
  Tribal-area designations are not counted toward counties.
* Count = number of **distinct `disasterNumber`** per county (multiple rows per disaster/county count once).
* Rank descending; ties broken by the most recent qualifying declaration date (later first), then by FIPS.

## 3. Why this gets overlooked in real projects

* "Statewide" designations look like a special place name, not a broadcast to all counties; they are dropped or matched to
  nothing.
* Declarations are amended (programs added, areas added); row counts overstate disasters.
* Name-based grouping (`designatedArea`) splits counties across "(County)", "(Parish)", "(Borough)", "(City)" variants and
  merges same-named counties across states.
* The 2020 pandemic produced a major disaster declaration for every state; leaving it in adds a constant within states
  but not across states with territories or tribes, and it is excluded by the method anyway.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `DisasterDeclarationsSummaries.csv` | CSV | ~65–70k | OpenFEMA | U.S. Gov public domain | Designations |
| 2 | `DisasterDeclarationsSummaries.json` (region extract via API) | JSON | ~10–15k | OpenFEMA API | Public domain | Same; cross-check |
| 3 | `FemaWebDisasterDeclarations.csv` | CSV | ~5k | OpenFEMA | Public domain | Disaster-level attributes |
| 4 | `openfema_declarations_data_dictionary.pdf` | PDF | — | FEMA | Public domain | Field semantics (statewide, tribal) |
| 5 | `national_county2020.txt` | Pipe-delimited | ~3.2k | Census | Public domain | County-equivalents list |
| 6 | `county_changes_2004_2023.csv` | CSV | ~10 | Census substantial-changes pages | Public domain | Lists in effect by date |
| 7 | `fema_regions.csv` | CSV | ~56 | FEMA | Public domain | Region → states |
| 8 | `initiative_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `PublicAssistanceFundedProjectsSummaries.csv` (optional) | CSV | ~0.2M | OpenFEMA | Public domain | Context only |

## 5. Deterministic solution path

1. Filter declarations; exclude biological; keep PA-declared DRs in the region's states.
2. Expand statewide rows to all county-equivalents in effect on each declaration date; drop tribal rows.
3. Build (county FIPS, disasterNumber) distinct pairs; count per county.
4. Rank with tie-breaks; top 15 + 16th.
5. Contrast: unexpanded statewide; row counts; name grouping.

## 6. The traps

**Trap A — statewide unexpanded.** Counties in states with frequent statewide PA declarations fall out of the 15.

**Trap B — rows instead of distinct disasters.** Amended disasters double count.

**Trap C — names instead of FIPS.** Splits and merges counties.

**Trap D — EM/FM or biological included.** Changes counts and cross-state ranking.

## 7. Why the data is honest

OpenFEMA publishes FEMA's official designations; statewide and tribal designations are documented values. The method
defines how to count.

## 8. Draft task prompt (prose)

> The regional mitigation initiative goes to the fifteen counties with the most PA-declared major disasters from 2004
> through 2023, counted the way our initiative method describes. Using the OpenFEMA files and county references in the
> folder, rank every county in the region and tell me the fifteen and the sixteenth. Produce `repeat_impact_ranking.csv`
> (county FIPS, name, state, distinct disasters, of which via statewide designations, most recent declaration, rank) and
> `repeat_impact_chart.png`, ranked bars for the top twenty-five split into county-specific and statewide-derived
> declarations with the cut after fifteen. Add a one-page `initiative_memo.pdf` naming the fifteen, the margin at the cut,
> and which counties would have been selected if statewide designations had been ignored.

## 9. Deliverables

* `repeat_impact_ranking.csv`, `repeat_impact_chart.png`, `initiative_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 15 counties + 16th + tie-break; counts for top 25 (spot-check ~10); statewide-derived counts; unexpanded alternative.

## 11. Golden-output checklist

* Filters; statewide expansion by date; distinct disasters; FIPS identity; tie-breaks; decision stated.

## 12. Build notes (scope tuning)

* Choose a multi-state region where one state has frequent statewide PA declarations; confirm Trap A changes ≥ 3 of 15.
* Freeze the OpenFEMA download (`lastRefresh`), as records are updated.
