# DA23 — How an open-source security fund shares 60 maintainer stipends, when one repository can publish four hundred dependent packages

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Nonprofit & Grant-making · open-source security funding |
| Mirrors | Ranking libraries, APIs or creators by how many others depend on them, when one organisation ships hundreds of separately counted artefacts (npm and Maven monorepo families, SDK packages split per service at cloud vendors, app bundles published per region in app stores), so counts of dependent artefacts overstate the projects that depend |
| Decision shape | An allocation under a cap: 60 maintainer stipends to the eligible packages with the most dependents, no more than 20 from one ecosystem, reported as stipends per ecosystem |
| Committed call | Stipends per ecosystem in whole numbers summing to 60, headed by Maven's |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E02, the dependent project (a source repository), which no dependency row records, pinned by Pattern B on the 2026 close-out, with E25 (Maven's withheld per-artifact downloads, bounded by namespace totals) and the dumps' exact counts behind the "10,000+" display below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #2 counts file rows instead of the real unit · #24 treats an unpublished figure as unknown · #3 stops at a close but inexact match · #19 breaks a big tie instead of questioning it |
| Calibration form | Prior-period close-out: the 2026 fund's close-out, its 60 funded packages with certified dependents, certified downloads and eligibility |
| Driving force | The fund counts dependents as its 2026 certification did, and only one construction reproduces all 60 certified counts: distinct dependent projects, read from each dependent package's source repository. The registries count packages. Monorepo families publish hundreds of packages from one repository (an SDK with a package per cloud service, a framework split into plugins), and each family's packages all declare the same few libraries. Counted as packages, Maven's and npm's libraries swell and Maven fills its 20; counted as projects, PyPI's libraries, mostly one package per repository, lead, and Maven falls to 12. |

## 1. Situation

An open-source security foundation pays one-year stipends to maintainers of critical packages. For 2027 it has 60, and the fund's rules
send them to the eligible packages with the most dependents, no more than 20 from one ecosystem, across npm, PyPI, Maven, crates and
RubyGems, counting dependents as the 2026 certification counted them. A package is eligible when it is downloaded more than a million
times a month. The pack holds each registry's API snapshot (dependents and downloads as displayed, with large counts shown as
"10,000+"), each ecosystem's dependency dump (every current release's declared dependencies and its source repository), Maven Central's
namespace download tables, the 2026 close-out and the fund's rules. The board signs off on 25 February 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the displays, the dumps, the namespace tables and the close-out. A registry's dependents count is
  a true count of dependent packages, and nobody's reading of their own numbers is overturned. The difficulty is what one dependent is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the programme director's view, the analyst's view and the steering group's basis. Every registry still
  counts dependent packages, and the dumps still give one row per package.
* **Instrument repair.** Clean-data test. Two files are suspect: the APIs' dependents display, truncated at "10,000+", and Maven's
  per-artifact downloads, withheld below each namespace's top three. Repair both (print every count and every download): rung 1's
  tie-break disappears and it lands with rung 2 on exact package counts (Maven 20), rung 0 is unchanged (Maven 2), and the answer stays
  Maven 12, because counting projects is still needed. No other file is suspect: every package in the dumps carries its source
  repository.
* **Lens swap.** The two reads count different units: 41 million declared dependencies from 2.9 million packages, against the 1.7 million
  source repositories that publish them.

## 3. The driving force

A strong solver ranks the eligible packages by the registries' dependents counts and finds 214 tied at "10,000+". It bounds Maven's
withheld downloads from its namespace tables for eligibility, and, rather than break the tie on downloads, counts each tied package's
dependents exactly from the dumps. Maven's tied libraries then run to 61,000 dependents and fill its 20. But the rules count dependents as
the 2026 certification did, and the close-out's certified counts sit below the package counts for 37 of its 60 packages. The difference
is monorepo families. An SDK that publishes a package for each of 380 cloud services, or a framework split into 500 plugins, is one
project whose packages all declare the same handful of libraries. Each dump row carries its source repository, and counted as distinct
repositories, every certified count reproduces. Java's and JavaScript's most-used libraries are leaned on by such families; Python's are
leaned on by one-package projects.

## 4. The ladder

| Rung | Construction | Lands on (Maven's stipends) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The 60 most-downloaded packages, no more than 20 per ecosystem, withheld Maven downloads read as zero | 2 (−83.3%) | Downloads are the popularity measure every leaderboard uses | The fund ranks eligible packages by dependents |
| 1 | Eligible packages by the displayed dependents, ties broken by downloads, Maven's withheld downloads bounded by namespace totals (E25) | 9 (−25.0%) | The fund's rule and tie-break on the registries' own counts, every withheld figure bounded | The dumps: behind the 214 "10,000+" displays, package counts run from 10,004 to 61,000 |
| 2 | Dependents as exact package counts from the dumps | 20 (+66.7%) | The tie questioned and broken with exact counts | The close-out: package counts reproduce 23 of its 60 certified counts, every miss too high |
| 3 | **Decisive:** dependents as distinct source repositories of the dependent packages (E02) | **12** | — | — |

* **Figure shape.** The corrections walk Maven's share up and the decisive move reverses them. The full table is npm 15, PyPI 20, Maven
  12, crates 10, RubyGems 3. Rung 2 gives npm 12, PyPI 16, Maven 20, crates 9, RubyGems 3; rung 1 npm 20, PyPI 20, Maven 9, crates 8,
  RubyGems 3.
* **Partial correction priced (L3).** A solver who groups dependents by name prefix (npm scope, Maven group) instead of repository merges
  whole foundations' unrelated projects and gives Maven 6 (−50.0%). One who counts projects but leaves Maven's withheld downloads
  unknown makes most of Maven ineligible and gives it 5 (−58.3%). One who counts projects and ignores the per-ecosystem cap gives PyPI 27
  and Maven 10 (−16.7%), breaching the rule.
* **Grid.** Downloads (withheld as unknown or bounded) × dependents (displayed with tie-break, exact packages, projects) gives 6 cells,
  with Maven at 4, 9, 7, 20, 5 and 12. The nearest wrong cells are 9 (−25.0%) and 10 (−16.7%, uncapped).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules say dependents are counted as the 2026 certification counted them. The close-out states the certified
   counts, not how they were formed. The API documentation defines dependents as packages. No document mentions repositories.
2. **Reproduction, and why it is a construction.** Distinct source repositories reproduce all 60 certified counts. Package counts
   reproduce 23, name-prefix grouping 31, and every rival miss is too high, so no rival reconciles on the close-out's total. The
   reproducing count is a distinct-count over a field of the dependent rows, not of the package being ranked, and no parameter reaches
   it.
3. **No arithmetic symptom.** Below the ceiling, displays match the dumps' package counts exactly, downloads reconcile to namespace
   totals, and every package has one repository.
4. **Not a row predicate.** A package's count is the number of distinct repositories among all current releases that declare it, built
   across the whole dump.
5. **The enumeration is arithmetic.** 41 million declared dependencies collapse to project counts for 2.9 million packages.
6. **No cutover date.** Monorepo families have grown steadily, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the registries still count packages.

## 6. The calibration corpus

* **Form.** The 2026 close-out: 60 funded packages (2,000 to 9,999 dependents) with their certified dependents, certified monthly
  downloads and eligibility decision.
* **What it certifies.** The project count (60 of 60, above) and eligibility through bounded downloads: the 11 funded Maven artifacts
  with withheld downloads were certified at 1.2 to 3.8 million a month, each inside its bound, where treating withheld downloads as
  unknown reproduces 49 of 60 cases.
* **Twin pair.** linkwell (PyPI) and parsewise (npm) are identical on every column the APIs show and on their exact package counts: 21,400
  dependent packages, 3.1 million monthly downloads, four maintainers. linkwell's dependents come from 20,900 repositories and
  parsewise's from 10,300, because 11,000 of its dependents are members of monorepo families (2.0×). Every package-based rule ranks them
  together; under the rule linkwell ranks 19th and parsewise 88th.
* **Resemblance points at the decoy.** On downloads and maintainers, Maven's large libraries most resemble the close-out's largest awards.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund's rules: "Stipends go to eligible packages in order of dependents, no more than 20 from one ecosystem, with
  dependents counted as the fund's 2026 certification counted them from the ecosystems' dependency records. A package is eligible when it
  is downloaded more than a million times a month. Ties are broken by downloads." Maven Central's documentation describes its namespace
  tables.
* **Empirical pins.** The project count and bounded eligibility, from the close-out.
* **Voices.** The programme director: "Java runs the world's enterprises; its libraries are the critical ones." The analyst: "The
  registries publish dependents. Our job is to rank them."
* **Licensed wrong basis.** The rules record that the steering group's annual report ranks packages by registry dependents counts and
  will be read alongside the allocation.

## 8. Determinism by construction

* **Snapshot.** The APIs, the dumps and the namespace tables share one snapshot date, 31 January 2027.
* **Repositories.** Every package in the dumps carries one source repository, normalised to host, owner and name; a package's own
  repository never counts among its dependents.
* **Counting.** Current releases only, runtime dependencies. After project counting no two packages tie at the selection boundary.
* **Bounds.** Every withheld artifact's bound sits wholly above or below a million downloads.
* **Cap.** When an ecosystem reaches 20, the next package in order from another ecosystem takes the place. The cap binds for PyPI at
  rung 3.

## 9. Prompt sketch and deliverables

> The board signs off next year's maintainer stipends on 25 February: 60 of them, no ecosystem above 20. Our programme director believes
> Java's libraries are the critical ones. Tell me how many stipends each ecosystem gets, in a sentence for the board, and send
> `stipends_2027.xlsx` with the sheets below and a chart `dependents_by_unit.png`.

* `stipends_2027.xlsx` — the ranked eligible packages with displayed, package and project counts, the allocation under each rung's
  construction with the close-out reproduction (ask C), the advisories sheet (ask A) and the payments sheet (ask B).
* `dependents_by_unit.png` — the 214 packages displayed as "10,000+", plotted by package count against project count and coloured by
  ecosystem, with the 60th place under each count marked, linkwell and parsewise annotated, and each ecosystem's stipends under both.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Security advisories published per ecosystem and quarter, 2025–2026. *Device:* an advisory
  covering several packages is one record with a list of affected packages, as the advisory database's schema documents. Counting
  package rows overstates 23 of the 40 cells.
* **Ask B (device-carried).** Stipend payments by month in 2026. *Device:* stipends are paid monthly in arrears, and the payment file
  dates each payment on the day it leaves, not the month of work it covers, as the payments guide documents. Booking by payment date
  shifts every month by one and misstates 9 of the 12.
* **Ask C (validity).** Each ecosystem's stipends under each of the four rung constructions, each construction's reproduction count on the
  close-out, and linkwell's and parsewise's package and project counts.
* **Decoupling.** Advisories and payments share no row with the APIs, the dumps, the namespace tables or the close-out. Clearing the
  project count changes no figure in asks A or B.

## 11. Rubric arithmetic

5 ecosystems × 8 quarters (ask A) + 12 months (ask B) + 5 ecosystems × 4 constructions, 4 reproduction counts and 4 twin counts (ask C) +
the 5 committed stipend figures + 4 named chart parts + 2 files ≈ 89 criteria.

## 12. World-building constraints

* 214 packages display "10,000+": npm 92, PyPI 51, Maven 38, crates 21, RubyGems 12. Package counts run from 10,004 to 61,000.
* Allocations (npm / PyPI / Maven / crates / RubyGems): rung 0 20 / 20 / 2 / 11 / 7; rung 1 20 / 20 / 9 / 8 / 3; rung 2 12 / 16 / 20 / 9 /
  3; rung 3 15 / 20 / 12 / 10 / 3. Maven under the other cells: 4, 7 and 5; name-prefix grouping 6; uncapped projects 10 (PyPI 27).
* Close-out: projects 60/60, packages 23, name prefixes 31; 11 Maven artifacts with withheld downloads certified at 1.2 to 3.8 million.
* linkwell and parsewise are identical on every API column and in package count; 20,900 and 10,300 repositories.
* Advisories and payments touch no package count.
