# DA40 — Which county hosts the nearby-marketplace pilot, when four candidates look 100% local only because the release drops small pairs

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · local marketplace features |
| Mirrors | Ranking markets on a share computed from a release that drops small cells (social-graph releases with minimum-count floors, app analytics with privacy thresholds, ads reach estimates), where several markets reach 100% only because their small cells were dropped |
| Decision shape | Which of N gets one scarce thing: the nearby-marketplace pilot launches in one of ten metro counties (changed from one figure; see the report) |
| Committed call | The pilot county, and the share of its users' friendship links within 100 miles, to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a saturated tie questioned rather than broken (measured #19), with a suppressed cell recovered from a published total inside the tie-break at rung 2 (measured #24) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #24 treats an unpublished figure as unknown · #4 never tests its reading against the control |
| Calibration form | Pilot log: last year's local-groups pilot, with the local link share filed for each of its eight counties |
| Driving force | The pair file releases only county pairs with at least 500 links. Every pair within 100 miles clears that bar, and many distant pairs do not, so four candidates whose distant ties are spread thin show 100% local on the released pairs. The charter's tie-break by verified sellers then picks among them. The county totals file, a second file of record, holds every link, and against it the four fall to 53% to 84%. |

## 1. Situation

A social platform will pilot a nearby-marketplace feed in one of ten metro counties. Its charter picks the county whose users have the
largest share of friendship links within 100 miles, breaking ties toward more verified sellers. The pack holds the county-pair link file
(released for pairs with at least 500 links), the county totals file, county centroids, the verified-seller counts (counties under 50
sellers suppressed, metro-area totals published), the charter, and last year's local-groups pilot log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each released pair, each county total, each seller count. Nobody ranks the candidates and nothing
  reported is overturned. The difficulty is a 100% that four counties share.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the growth team's note. Shares on the released pairs still tie four counties at 100% and the
  documented tie-break still decides.
* **Instrument repair.** Release every pair however small: the totals file already holds the answer's denominator. The difficulty is
  reading a tie at the maximum as unsettled, not filling a gap.
* **Lens swap.** The naive share's denominator is the released links; the answer's is every link the county's users hold. Different
  populations of links, and different counties win.

## 3. The driving force

A strong solver drops the unweighted index for link shares, computes each county's share within 100 miles on the released pairs, and
finds Corran, Dunmore, Fennick and Glenarm all at 100.0%. The charter has a tie-break, so it applies it: verified sellers. Two of the four
have suppressed seller counts, which the metro-area totals recover, and the tie goes to Glenarm. But a share of exactly 100% for four
large counties means their distant links are missing, not absent. The release drops pairs under 500 links, and a metro whose distant
friends are scattered across hundreds of small counties loses all of them. The totals file counts every link. Against it Glenarm holds
53%, Corran 60%, Dunmore 72% and Fennick, the smallest of the four, 84%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Mean pair index within 100 miles ÷ mean over all released pairs | A, Ashbourne (1.22× Bexley) | The release's own index, read as a closeness score | The charter ranks on the share of links, not on an index |
| 1 | Link share within 100 miles on released pairs; four counties tie at 100.0%; tie-break on visible seller counts | C, Corran (sellers 1.24× Fennick; Dunmore and Glenarm suppressed) | The charter's measure and the charter's tie-break | The seller file: metro-area totals fix the two suppressed counts |
| 2 | The same tie, broken with suppressed seller counts recovered from metro totals (Dunmore 410, Glenarm 760) | G, Glenarm (sellers 1.25× Corran) | Every count in the tie-break now known | The totals file: every candidate's total links exceed its released links, Glenarm's by 89% |
| 3 | **Decisive:** link share within 100 miles against each county's total links | **F, Fennick (84.0%, 1.17× Dunmore)** (5th of 10 on rung 0) | — | — |

* **Position table.** Fennick is 5th on rung 0. On rungs 1 and 2 it shares the 100% tie but is the smallest of the four on sellers,
  users, population and links, so the charter's tie-break and every size-based alternative place it last of the four. It leads only rung 3.
* **Discriminator dominance.** Glenarm leads rung 2 on a tie (carried advantage 1.00 on the share). Against totals, Fennick keeps 0.84 of
  its released share and Glenarm 0.53, an edge of 1.58×, against the 1.2 × 1.00 = 1.20 needed (1.32× headroom). The product, 1.58, is
  Fennick's lead over Glenarm on rung 3.
* **Partial correction priced (L3).** A solver who adds the unreleased links to the numerator as well as the denominator keeps the tie at
  100% and names Glenarm again. One who bounds the unreleased links by the release floor (under 500 links per missing pair) instead of
  the totals file overstates Fennick's missing links and names Dunmore at 1.12× Fennick. No half lands on Fennick.
* **Grid.** Measure (index, released share, totals share) × tie-break (visible sellers, recovered sellers) gives 4 distinct cells, since
  the totals share leaves no tie. Three name Ashbourne, Corran or Glenarm; only the totals share names Fennick.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The release note gives the 500-link floor as a privacy rule. The charter gives a tie-break without saying ties
   can be artefacts. No document links the floor to the share.
2. **Pattern B, reproduction in the pilot log.** Shares against county totals reproduce all eight filed pilot shares to 0.1 points; shares
   on released pairs reproduce 3 of 8, the three counties with no missing pairs, and overstate the other five. The reconciliation is a
   construction: released within-100 links over a total from another file, with the 100-mile split confirmed by the floor.
3. **No arithmetic symptom.** Released pairs reconcile to the release's row count, totals reconcile to the platform's published user
   statistics, and a 100% share raises no error.
4. **Not a row predicate.** Each share needs a sum over released pairs within 100 miles and a denominator from a different file.
5. **The enumeration is arithmetic.** No column records how many links a county lost to the floor.
6. **No cutover date.** One release, and nothing steps.
7. **Survives deletion.** With every voice removed, the tie still forms and the tie-break still names Glenarm.

## 6. The calibration corpus

* **Form.** The local-groups pilot log: eight counties, each with the local link share the team filed in its launch memo and the released
  pairs of that year.
* **What it certifies.** That the charter's measure is a share of links, which takes a solver to rung 1.
* **What pins the denominator.** The five filed shares only the totals file reproduces.
* **Twin pair.** Pilot counties Harrowby and Lenwick match on released links within and beyond 100 miles and on user base. Their filed
  shares are 82.0% and 41.0% (2.0×): Lenwick's users hold half their links in pairs below the floor.
* **Resemblance points at the decoy.** On every released column, Glenarm resembles Harrowby, the pilot's best local county.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the pilot goes to the county whose users hold the largest share of friendship links within 100 miles, with
  ties broken toward more verified sellers. Distances run between population-weighted centroids.
* **Empirical pins.** The denominator, from the pilot log.
* **Voices.** The growth lead: "Four counties at 100% local is the best problem to have; let the tie-break do its job." The trust and
  safety lead: "Sellers are what make a local feed work."
* **Licensed wrong basis.** The charter records that the partnerships team ranks markets on the release's pair index and will present
  that ranking at the launch review.

## 8. Determinism by construction

* **Floor.** Every candidate pair within 100 miles carries more than 2,000 links, so the floor never cuts a local pair.
* **Seller recovery.** Each metro area has exactly one suppressed county, so its seller count is exact.
* **Distances.** No released pair lies within 5 miles of the 100-mile line.
* **Totals.** The totals file counts each link once per county, the same convention as the pair file.

## 9. Prompt sketch and deliverables

> The nearby feed pilots in one county next quarter, and growth tells me four counties already look 100% local, so the tie-break will
> settle it. Tell me which county hosts the pilot and what share of its users' friendship links lie within 100 miles, to one decimal, in
> a line for the launch review. Send `pilot_county.xlsx`, a chart `local_share.png`, and a one-page `pilot_choice.pdf`.

* `pilot_county.xlsx` — the share build for all ten candidates, the listings sheet (ask A), the neighbourhood sheet (ask B) and the
  rung table (ask C).
* `local_share.png` — each candidate's share on released pairs beside its share against totals as a dumbbell chart, the four tied
  counties highlighted at 100%, the gap labelled with the missing links, and the chosen county marked.
* `pilot_choice.pdf` — the committed county, its share, and why the tie was not settled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each candidate, the median price of listings in last year's local-groups pilot. *Device:*
  relisted items keep their listing ID with a relist counter, as the listings note documents; counting each relist as a listing
  understates medians in four counties.
* **Ask B (device-carried).** For each candidate, the share of users with at least one friend in the same postcode district. *Device:* the
  district file uses delivery districts, and the crosswalk maps them to the census districts the user file uses; joining on the raw code
  misattributes 12% of users.
* **Ask C (validity).** Each candidate's figure under each of the four rungs, and the pilot log's reproduction count under each share.
* **Decoupling.** Clearing the totals reconciliation changes no figure in asks A or B.

## 11. Rubric arithmetic

10 candidates (ask A) + 10 candidates (ask B) + 10 × 4 rung figures and 2 reproduction counts (ask C) + the committed county, its share
and its margin + 5 named chart parts + 3 files ≈ 73 criteria.

## 12. World-building constraints

* Released shares: Corran, Dunmore, Fennick and Glenarm 100.0%; Bexley 82%, Ashbourne 76%, all others below 80%. Totals shares: Fennick 84,
  Dunmore 72, Bexley 70, Ashbourne 66, Corran 60, Glenarm 53.
* Verified sellers: Glenarm 760 and Dunmore 410 (suppressed, recovered), Corran 610, Fennick 492.
* Pilot log: totals reproduce 8 of 8, released pairs 3 of 8. Harrowby and Lenwick match on every released column.
* Relist counters and district codes never touch a pair, a total or a seller count.
