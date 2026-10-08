# DA23 — How an open-source security fund shares 60 maintainer stipends, when the registries display every large dependents count as "10,000+"

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Nonprofit & Grant-making · open-source security funding |
| Mirrors | Ranking on a platform's displayed counts that stop at a ceiling ("10K+" or "1M+" installs and followers, "used by" counts on code hosts) when the decision needs the true value, and a documented tie-break then picks on the wrong signal (Google Play install bands, creator-fund rankings, package-popularity programmes at cloud vendors) |
| Decision shape | An allocation under a cap: 60 maintainer stipends to the eligible packages with the most dependents, no more than 20 from one ecosystem, reported as stipends per ecosystem |
| Committed call | Stipends per ecosystem in whole numbers summing to 60, headed by Maven's |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · E21, a saturated tie (214 packages displayed as "10,000+") broken by the fund's lowest-count-consistent rule through the ecosystems' dependency dumps, with E25 (Maven's withheld per-artifact downloads, bounded by namespace totals for eligibility) below it and a close-out blind to the display cap (L1) |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #24 treats an unpublished figure as unknown · #7 uses the ready-made measure · #12 stops at the first control that passes |
| Calibration form | Prior-period close-out: the 2026 fund's close-out, its 60 funded packages with certified dependents, certified downloads and eligibility |
| Driving force | The fund ranks eligible packages by dependents, and the registries' APIs, the source of every past close-out, display any count above 9,999 as "10,000+". 214 packages sit at that ceiling, and the fund's documented tie-break, downloads, fills npm's and PyPI's caps. But the rule takes the lowest count consistent with every dependency record, and the dumps count every package's dependents exactly. Behind the shared "10,000+", most of npm's tied packages have 10,000 to 15,000 dependents, while 31 of Maven's 38 have more than 25,000, because enterprise Java libraries sit beneath whole frameworks. Counted, Maven fills its 20. |

## 1. Situation

An open-source security foundation pays one-year stipends to maintainers of critical packages. For 2027 it has 60, and the fund's rules
send them to the eligible packages with the most dependents, no more than 20 from one ecosystem, across npm, PyPI, Maven, crates and
RubyGems. A package is eligible when it is downloaded more than a million times a month. The pack holds each registry's API snapshot
(dependents and downloads as displayed), each ecosystem's dependency dump (every current release's declared dependencies), Maven
Central's namespace download tables, the 2026 close-out and the fund's rules. The board signs off on 25 February 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the APIs' displays, the dumps, the namespace tables and the close-out. "10,000+" is a true
  statement about each tied package, and nobody's reading of their own numbers is overturned. The difficulty is that a ceiling is not a
  count.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the programme director's view, the analyst's view and the steering group's basis. 214 packages still display
  "10,000+", and the fund's rules still say how to break a tie.
* **Instrument repair.** A registry without a display ceiling would print the counts, but the dumps already hold every dependency, and
  the rule already asks for the lowest count consistent with them. The ceiling is a display convention, not an error.
* **Lens swap.** The two reads rank different quantities over the same packages: downloads among 214 tied packages, against exact
  dependents counted from the dumps, which run from 10,004 to 61,000.

## 3. The driving force

A strong solver reads the rules, ranks the eligible packages by the registries' dependents counts and finds 214 tied at "10,000+",
far more than 60. The rules say ties go by downloads, and npm's and PyPI's tied packages carry the largest downloads in software, so each
fills its 20. Maven's per-artifact downloads are withheld, but its namespace tables print each namespace's total and its three largest
artifacts, which bound the rest. Bounded, Maven's artifacts clear the eligibility line and take 9 stipends, and that construction
reproduces the whole 2026 close-out. But the tie is not real. The rules take the lowest count consistent with every dependency record,
and "10,000+" is consistent with any count above 9,999. The dumps fix each count exactly. Java's logging, collections and HTTP libraries
sit beneath entire frameworks, and 31 of Maven's 38 tied packages have more than 25,000 dependents. Most of npm's tied packages have
10,000 to 15,000.

## 4. The ladder

| Rung | Construction | Lands on (Maven's stipends) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The 60 most-downloaded packages, no more than 20 per ecosystem, withheld Maven downloads read as zero | 2 (−90%) | Downloads are the popularity measure every leaderboard uses | The fund ranks eligible packages by dependents |
| 1 | Eligible packages by the APIs' dependents, ties by downloads, withheld Maven downloads treated as unknown and so ineligible | 4 (−80%) | The fund's rule on the registries' own counts | The close-out: 11 funded Maven artifacts with withheld downloads were certified above a million a month, inside the bounds their namespace tables give |
| 2 | Withheld Maven downloads bounded by the namespace total less its three printed artifacts (E25), for eligibility and the tie-break | 9 (−55%) | Reproduces every case of the 2026 close-out, eligibility included | The dependency dumps: behind the 214 "10,000+" displays, counts run from 10,004 to 61,000 |
| 3 | **Decisive:** dependents as the lowest count consistent with every dependency record, the dumps' exact counts (E21) | **20** | — | — |

* **Figure shape.** Every correction raises Maven's share, and the answer is the maximum cell, at the cap. The full table is npm 12, PyPI
  16, Maven 20, crates 9, RubyGems 3. Rung 2 gives npm 20, PyPI 20, Maven 9, crates 8, RubyGems 3; rung 1 npm 20, PyPI 20, Maven 4,
  crates 12, RubyGems 4.
* **Partial correction priced (L3).** A solver who counts the dumps but leaves withheld Maven downloads unknown makes most of Maven
  ineligible and gives it 7 (−65%), with crates 15. One who counts the dumps and drops the per-ecosystem cap gives Maven 31 (+55%),
  breaching the rule. One who uses the dumps only to order the tied packages among themselves gets the answer by the same arithmetic,
  because every package below the ceiling already displays its exact count.
* **Grid.** Downloads (withheld as unknown or bounded) × dependents (displayed with tie-break or lowest consistent) gives 4 cells, with
  Maven at 4, 9, 7 and 20, and rung 0 at 2. The nearest wrong cell is 9 (−55%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules say "the lowest count consistent with every dependency record" and give a tie-break. The API
   documentation describes "10,000+" as the display for large counts. No document says that the tie the display creates is not a tie
   under the rule.
2. **Corpus blind to the ceiling.** The close-out certifies eligibility, the bounds and the ranking exactly. *In every 2026 case the
   displayed count was the count of record, because the 2026 rules took packages with 2,000 to 9,999 dependents, all below the
   ceiling.* Run over the close-out, displayed and counted dependents give the same 60.
3. **No arithmetic symptom.** Displays match the dumps for every package below the ceiling, downloads reconcile to namespace totals, and
   the tie-break produces a clean ranking.
4. **Not a row predicate.** A package's count is the number of current releases across its ecosystem that declare it, built from the
   whole dump.
5. **The enumeration is arithmetic.** 214 counts are built from 41 million declared dependencies.
6. **No cutover date.** The display ceiling has always applied, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the rules still offer a tie-break for the tie the display
   makes.

## 6. The calibration corpus

* **Form.** The 2026 close-out: 60 funded packages with their certified dependents, certified monthly downloads and eligibility
  decision, and the 2026 rules.
* **What it certifies.** Eligibility through bounded downloads: the 11 funded Maven artifacts with withheld downloads were certified at
  1.2 to 3.8 million a month, each inside its bound and above the line. Treating withheld downloads as unknown drops all 11 and
  reproduces 49 of 60 cases. Downloads-first ranking reproduces 22.
* **What it is blind to.** The ceiling (above).
* **Twin pair.** Two PyPI packages, linkwell and parsewise, are identical on every column the APIs show: "10,000+" dependents, 3.1
  million monthly downloads, four maintainers, the same licence and release cadence. The dumps count 28,700 and 14,100 dependents
  (2.0×). Under the displays and the tie-break they are interchangeable. Under the rule linkwell ranks 23rd and parsewise 151st.
* **Resemblance points at the decoy.** On downloads and maintainers, npm's tied packages most resemble the 2026 close-out's largest
  awards.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund's rules: "Stipends go to eligible packages in order of dependents, no more than 20 from one ecosystem. A
  package's dependents are the number of packages whose current release declares it, taken as the lowest count consistent with every
  dependency record of its ecosystem. A package is eligible when it is downloaded more than a million times a month. Ties are broken by
  downloads." Maven Central's documentation describes its namespace tables.
* **Empirical pins.** Bounded downloads for eligibility, from the close-out.
* **Voices.** The programme director: "npm has more critical packages than any other ecosystem." The analyst: "Our rules already tell us
  how to break the tie."
* **Licensed wrong basis.** The rules record that the steering group's annual report ranks packages by downloads and will be read
  alongside the allocation.

## 8. Determinism by construction

* **Snapshot.** The APIs, the dumps and the namespace tables share one snapshot date, 31 January 2027.
* **Counting.** Current releases only, runtime dependencies, each declaring package counted once. Below the ceiling, the dumps reproduce
  every displayed count exactly.
* **Ties.** After the dumps' counts, no two packages tie at the selection boundary.
* **Bounds.** Every withheld artifact's bound sits wholly above or below a million downloads, and no two bounds overlap at rung 2's
  selection boundary.
* **Cap.** When an ecosystem reaches 20, the next package in order from another ecosystem takes the place. The cap binds for Maven at
  rung 3.

## 9. Prompt sketch and deliverables

> The board signs off next year's maintainer stipends on 25 February: 60 of them, no ecosystem above 20. Our programme director believes
> npm has more critical packages than any other ecosystem. Tell me how many stipends each ecosystem gets, in a sentence for the board,
> and send `stipends_2027.xlsx` with the sheets below and a chart `tied_packages.png`.

* `stipends_2027.xlsx` — the ranked eligible packages with displayed and counted dependents, the allocation under each rung's
  construction with the close-out reproduction (ask C), the advisories sheet (ask A) and the payments sheet (ask B).
* `tied_packages.png` — the 214 packages displayed as "10,000+", plotted by counted dependents and coloured by ecosystem, with the 60th
  place marked, linkwell and parsewise annotated, and each ecosystem's stipends under the tie-break and under the rule.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Security advisories published per ecosystem and quarter, 2025–2026. *Device:* an advisory
  covering several packages is one record with a list of affected packages, as the advisory database's schema documents. Counting
  package rows overstates 23 of the 40 cells.
* **Ask B (device-carried).** Stipend payments by month in 2026. *Device:* stipends are paid monthly in arrears, and the payment file
  dates each payment on the day it leaves, not the month of work it covers, as the payments guide documents. Booking by payment date
  shifts every month by one and misstates 9 of the 12.
* **Ask C (validity).** Each ecosystem's stipends under each of the four rung constructions, each construction's reproduction count on the
  close-out, and linkwell's and parsewise's displayed and counted dependents.
* **Decoupling.** Advisories and payments share no row with the APIs, the dumps, the namespace tables or the close-out. Clearing the
  rule's count changes no figure in asks A or B.

## 11. Rubric arithmetic

5 ecosystems × 8 quarters (ask A) + 12 months (ask B) + 5 ecosystems × 4 constructions, 3 reproduction counts and 2 twin counts (ask C) +
the 5 committed stipend figures + 4 named chart parts + 2 files ≈ 88 criteria.

## 12. World-building constraints

* 214 packages display "10,000+": npm 92, PyPI 51, Maven 38, crates 21, RubyGems 12. Counted dependents run from 10,004 to 61,000; 31
  of Maven's 38 exceed 25,000.
* Allocations (npm / PyPI / Maven / crates / RubyGems): rung 0 20 / 20 / 2 / 11 / 7; rung 1 20 / 20 / 4 / 12 / 4; rung 2 20 / 20 / 9 /
  8 / 3; rung 3 12 / 16 / 20 / 9 / 3; counted with withheld downloads unknown 13 / 18 / 7 / 15 / 7; uncapped Maven 31.
* Close-out: 60 packages at 2,000 to 9,999 dependents; 11 Maven artifacts with withheld downloads certified at 1.2 to 3.8 million.
  Reproduction: rung 2's construction 60/60, withheld-as-unknown 49, downloads-first 22.
* linkwell and parsewise are identical on every API column; 28,700 and 14,100 counted dependents.
* Advisories and payments touch no package count.
