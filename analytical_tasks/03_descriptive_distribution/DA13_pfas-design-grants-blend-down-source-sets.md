# DA13 — How far $36 million of PFAS design grants reaches, when an entry point's water is a mixture and not every source over the line needs treating

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · public water-infrastructure grant administration |
| Mirrors | Sizing remediation on the share of a blended stream that must be treated (refiners and grain elevators blending off-spec lots with clean stock to meet a contract spec, food supply chains reworking only the lots a blend cannot absorb, cloud data teams sizing the reprocessing a blended dataset needs to clear a quality bar), where every off-spec input looks like a unit to fix |
| Decision shape | An allocation under a cap: grants in priority order until the next one does not fit $36 million, each at $2.4 million per MGD of treatment capacity, capped at $6 million a system |
| Committed call | The funded systems with each grant in dollars, and the number of systems the fund reaches |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · E31, a mixture rather than a constant: each entry point's water is a mixture of its sources by the pumping log's shares, so a system's treatment capacity is not its capacity over the line but the smallest set of whole sources whose treatment brings every blend to 4.0 ng/L, the unique set that reproduces every 2026 grant at zero tolerance; with E21 (a saturated priority score broken by the lowest-consistent rule) below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #19 breaks a big tie instead of questioning it · #8 papers over a failed reproduction |
| Calibration form | Prior-period close-out: the 2026 grant cycle's close-out, each funded system's confirmed maximum, treated sources, treatment capacity and grant |
| Driving force | The fund's grants buy treatment capacity, and a system's water is a mixture at each entry point: a source adds its concentration times its share of the flow. Where two sources over 4.0 ng/L feed one entry point with clean water, treating the hotter one can bring the blend under the line, and the other source, still over 4.0 ng/L in its own water, needs nothing. No per-source rule reproduces the 2026 close-out. The smallest set of whole sources that brings every entry point's blend to 4.0 ng/L reproduces all 11 grants at zero tolerance. Applied to 2027, it shrinks seven grants, and the $36 million reaches 11 systems instead of 6. |

## 1. Situation

A state revolving fund has $36 million for PFAS treatment-design grants in 2027. The fund's rule scores each system on its confirmed
maximum PFOA or PFOS at any entry point, as a multiple of 4.0 ng/L capped at 4, with ties broken by population served, larger first.
Grants go down the list until the next grant does not fit, each at $2.4 million per MGD of treatment capacity at sources whose own water
exceeds 4.0 ng/L, up to $6 million a system; a treated source is treated whole. Twenty systems have scored detections. The pack holds the
national monitoring results by entry point, the state's confirmation resamples, quarterly results for every source, each system's
source and entry-point inventory with its pumping log (each source's share of each entry point's flow), and the 2026 cycle's close-out.
The board approves the list on 18 February.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each monitoring result, each confirmation sample, the source results, the pumping logs and the
  2026 close-out. Every source the natural build would fund really is over 4.0 ng/L in its own water, and nobody's reading of their own
  numbers is overturned. The difficulty is how much capacity a system must treat to bring its water under the line.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the grants manager's and the system operators' views and the federal partner's licensed basis. The source
  results still show 21 sources over the line in the capped systems, and sizing on every one of them is still the plain reading of the
  rule.
* **Instrument repair.** Clean-data test. The suspect file is the national monitoring release, which the state's confirmation resamples
  supersede at four systems' entry points. Repair it by carrying each confirmed value. Rung 0 then funds rung 1's six systems, and rungs 1
  and 2 stay at 6 and 7. No other file is suspect: the source results cover every source in every quarter, and the pumping log,
  capacities and populations are complete and current. The answer stays 11. Sizing each grant on the smallest set of whole sources that
  brings every entry point's blend to 4.0 ng/L is still needed, because the capacity a system must treat is a design quantity that no
  instrument records.
* **Lens swap.** The two reads fund different systems and different sources: 6 systems on every source over the line, against 11 on the
  sources each entry point's blend needs treated. Ashby, Lindmoor and Tarrant Mills each keep a well over 4.0 ng/L untreated.

## 3. The driving force

A strong solver scores each system on confirmed maxima. It sees sixteen systems tie at the cap on the national results, applies the
fund's lowest-consistent rule against the confirmation resamples (which breaks four of the ties, as last year's close-out confirms), and
sizes each grant on the sources whose own water exceeds 4.0 ng/L. It checks the 2026 close-out: every score reproduces, and seven of 11
grants. One more reproduces once it drops a source over the line that feeds only an entry point under it. Three stay too high. Each of
the three had two sources over 4.0 ng/L feeding one entry point with clean water, and its grant equals the capacity of one of them. At an
entry point a source adds its concentration times its share of the flow. A 6.0 ng/L well carrying 45% of an entry point's water adds 2.7
ng/L, under the line on its own once its partner is treated. The capacity a system must treat is the smallest set of whole sources that
brings every entry point's blend to 4.0 ng/L, and that reproduces all 11 grants exactly. In 2027 it shrinks seven grants, and the fund
reaches 11 systems.

## 4. The ladder

| Rung | Construction | Lands on (systems funded) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | National monitoring maxima, capped score, population tie-break, grant on every source whose own water exceeds 4.0 ng/L | 7 (Brennan, Riverton, Kestrel Bay, Dunmore, Ashby, Lindmoor, Wren Hill) | The fund's score, tie-break and source rule applied as written to the national results | The close-out: its scores reproduce only on the lower of monitoring and confirmation (11 of 11, against 6 of 11 on monitoring maxima) |
| 1 | Confirmed maxima by the lowest-consistent rule (E21) | 6 (Riverton, Ashby, Lindmoor, Pine Hollow, Cedar Bluff, Corbel) | Every 2026 score reproduces, and the four monitoring-only systems fall out of the cap | The close-out: Elm Fork's 2026 grant left out a well over 4.0 ng/L that feeds only an entry point under the line |
| 2 | Grant on sources over 4.0 ng/L that feed an entry point over it | 7 (rung 1 and Tarrant Mills) | 8 of 11 close-out grants reproduce, and the rule's purpose, the water people drink, reads naturally | The close-out: the other three 2026 grants each equal the smallest set of whole sources that brings every entry point's blend to 4.0 ng/L |
| 3 | **Decisive:** grant on the smallest set of whole sources whose treatment brings every entry point's blend to 4.0 ng/L, from the pumping log's shares (E31) | **11** | — | — |

* **Figure shape.** The answer is bracketed. Every rung below funds 6 or 7 systems, giving Ashby, Lindmoor and Tarrant Mills capped
  grants their blends do not need and leaving Oxbow, Fenwick, Hollis Creek and Greyford unfunded. Every over-application
  funds 13 or 14. The answer's list is Riverton $4.80 million, Ashby $3.60 million, Lindmoor $4.08 million, Pine Hollow $4.32 million,
  Cedar Bluff $2.16 million, Corbel $3.84 million, Tarrant Mills $3.60 million, Oxbow $2.64 million, Fenwick $1.92 million, Hollis Creek
  $3.36 million and Greyford $1.44 million: $35.76 million.
* **Partial correction priced (L3).** Dropping only the sources that feed an entry point under the line is rung 2 (7 systems).
  Treating only the hottest source at each entry point over the line leaves Lindmoor and Pine Hollow at 5.4 and 8.1 ng/L and funds 13,
  adding Maple Run and Wexley. Letting part of a source's flow bypass treatment, which the rule forbids and the close-out refutes (0 of
  11), funds 14, adding Maple Run, Wexley and Dunmore. Sizing correctly on monitoring maxima funds 9, with Brennan, Kestrel Bay, Dunmore and Wren Hill funded
  and Corbel cut. None of them funds the answer's list.
* **Grid.** Score (monitoring or confirmed) × sizing (every source over the line, sources at entry points over it, smallest whole-source
  set, partial flow) gives 8 cells, funding 6 to 14 systems. Only confirmed scores and the smallest whole-source set fund the answer's
  11. The nearest wrong cells fund 9 (monitoring, smallest set) and 12 (monitoring, partial flow), each a different list.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule funds treatment capacity "at sources whose own water exceeds 4.0 ng/L", a treated source treated whole.
   The inventory records the pumping shares for operations. No document says the capacity is what the blend needs, or that a source over
   the line may go untreated.
2. **Reproduction, and why it is a construction.** The smallest whole-source set reproduces all 11 grants of the 2026 close-out at zero
   tolerance. Every source over the line reproduces 7, sources at entry points over the line 8, and partial-flow sizing none. Every miss
   of the first two is too high, so neither reconciles on the cycle's total. The reproducing quantity is the solution of each entry
   point's blend against its sources' shares, a set chosen over every source of the system together. No per-source flag, threshold or
   constant fraction reaches it.
3. **No arithmetic symptom.** Results, confirmations, source samples and pumping shares all reconcile: each entry point's confirmed result
   equals its sources' blend to the reporting precision, and every grant closes to the dollar under every rung.
4. **Not a row predicate.** Whether a source over the line needs treatment depends on its share of each entry point it feeds and on which
   other sources are treated. The set is solved per system, not read per row.
5. **The enumeration is arithmetic.** 21 sources over the line in the 12 capped systems come down to 14 that must be treated, found by
   solving the blends.
6. **No cutover date.** The pumping schedules are fixed year-round, the sources' results are stable, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, every source over the line still looks like a source to
   fund.

## 6. The calibration corpus

* **Form.** The 2026 cycle's close-out: each funded system's monitoring maximum, confirmation result, confirmed score, treated sources,
  treatment capacity and grant.
* **What it certifies and pins.** The lowest-consistent rule (E21): the 2026 scores reproduce only on the lower of monitoring and
  confirmation, 11 of 11 against 6. And the sizing: 11 of 11 grants only on the smallest whole-source set (above).
* **Twin pair.** Birchfield and Coldwater, both funded in 2026, are identical on every monitoring and confirmation column: one entry
  point confirmed at 18.0 ng/L, population 58,200, capacity 2.0 MGD, two sources over the line of 0.9 MGD each. Birchfield's two wells
  (22.0 and 18.0 ng/L) both had to be treated; Coldwater's (34.0 and 6.0 ng/L) needed only the first, because the second adds 2.7 ng/L to
  the blend. Their grants were $4.32 million and $2.16 million (2.0×). Only the source results and the pumping log separate them.
* **Resemblance points at the decoy.** By score, size and capacity, the 2027 blending systems most resemble the close-out's eight
  single-source grantees, whose grants equal their capacity over the line.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund's rule: "A system's priority score is its confirmed maximum PFOA or PFOS at any entry point as a multiple of
  4.0 ng/L, capped at 4; ties are broken by population served, larger first; a confirmed maximum is the lowest value consistent with every
  result on file." The rule: "Grants fund treatment capacity at sources whose own water exceeds 4.0 ng/L, at $2.4 million per MGD, up to
  $6 million a system, in priority order; a treated source is treated whole; a grant is made in full or not at all, and when the next
  grant does not fit, the round closes."
* **Empirical pins.** The lowest-consistent rule's application and the sizing, from the close-out.
* **Voices.** The grants manager: "The score cap and the population tie-break settle the order. That's why we wrote them." The operators'
  association: "Every well over the line is a well our members have to treat."
* **Licensed wrong basis.** The rule records that the federal partner sizes design costs on all capacity over the line and will publish
  its own estimate for each system.

## 8. Determinism by construction

* **Shares.** Each system runs a fixed pumping schedule, so each source's share of each entry point's flow is constant through the year,
  and the close-out reproduces on those shares.
* **Precision.** Results are reported to 0.1 ng/L, and each source's four quarterly results agree to it. Every blend under its chosen set
  sits at least 0.3 ng/L under the line, and every smaller set leaves an entry point at least 1.3 ng/L over it, so no rounding changes a
  set. Each system's smallest set is unique.
* **Funding edge.** The money runs out after the 11th system with $0.24 million left. The 12th, Maple Run, needs $1.20 million, and no
  system further down needs less, so stopping and skipping give the same list.
* **Tie-break.** After the lowest-consistent rule, 12 systems remain at the cap, with populations distinct to the person.

## 9. Prompt sketch and deliverables

> The fund's 2027 PFAS design grants go to the board on 18 February, and $36 million will not reach every system on the list. Our grants
> manager believes the score cap and the population tie-break settle the order. Give me the funded systems with each grant in dollars,
> and how many systems the fund reaches, as the table the board approves, and send `pfas_grants.xlsx` with the build and the sheets
> below, plus `source_sets.png`.

* `pfas_grants.xlsx` — scores, sources and grants, each of the four rung constructions' funded lists (ask C), the bill sheet (ask A) and
  the service-line sheet (ask B).
* `source_sets.png` — for each system whose grant changes, each entry point's blend before and after its chosen set is treated against
  the 4.0 ng/L line, the funded list as a bar of cumulative dollars against the $36 million line under rungs 1 and 3, and Birchfield and
  Coldwater annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Monthly residential bill at 5,000 gallons for each of the twelve largest systems in the state.
  *Device:* five of them bill fixed charges every two months while charging usage monthly, as their rate schedules state. Treating the
  fixed charge as monthly overstates those five bills by $9 to $22.
* **Ask B (device-carried).** Lead service lines fully replaced in each of the eight regional offices' areas in 2023, 2024 and 2025.
  *Device:* the inventory records a partial replacement (utility side only) with status "replaced-partial", which the state's guidance
  does not count as a replacement. Counting it overstates 17 of the 24 cells.
* **Ask C (validity).** For the seven systems whose grant changes between rungs 1 and 3, the grant under each of the four rung
  constructions and the sources it is sized on, with Birchfield's and Coldwater's 2026 grants rebuilt.
* **Decoupling.** Rate schedules and the service-line inventory share no row with the monitoring, source or pumping data. Clearing the
  blend sizing changes no figure in asks A or B.

## 11. Rubric arithmetic

12 systems (ask A) + 8 offices × 3 years (ask B) + 7 systems × 4 constructions and 2 twin grants (ask C) + the funded count, the 11
grants and the funding edge + 4 named chart parts + 2 files ≈ 85 criteria.

## 12. World-building constraints

* 20 scored systems; 16 at the cap on monitoring maxima and 12 on confirmed maxima (Brennan, Kestrel Bay, Dunmore and Wren Hill fall
  out). The 12 capped systems hold 21 sources over the line, 14 of them in the smallest sets.
* Systems funded: 7 / 6 / 7 / 11 by rung; hottest source only 13; partial flow 14; monitoring with the smallest set 9; monitoring with
  partial flow 12.
* Blending systems: Ashby (36.0 and 12.0 ng/L wells with a clean well; treat the first), Lindmoor (44.0, 10.0 and 7.0; treat the first
  two), Cedar Bluff (34.0 and 6.0; the first), Tarrant Mills (48.0 and 11.0; the first), Hollis Creek (33.0 and 7.0; the first); Riverton
  and Fenwick each have a well over the line feeding only an entry point under it.
* The 2026 close-out holds 11 systems: the lowest-consistent rule reproduces 11 scores (monitoring maxima 6); grants reproduce 11 on the
  smallest set, 8 on sources at entry points over the line, 7 on every source over it, and none on partial flow.
* Birchfield and Coldwater are identical on every monitoring and confirmation column; their source results and shares differ.
* Rate schedules and the service-line inventory touch no monitoring row.
