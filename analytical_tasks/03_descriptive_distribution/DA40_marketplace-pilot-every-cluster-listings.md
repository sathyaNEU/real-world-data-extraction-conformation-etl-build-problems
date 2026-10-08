# DA40 — Which metro county gets the nearby-marketplace pilot, when a town's feed lives only if every neighbourhood sees enough listings

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · local marketplace features |
| Mirrors | Launching a local network product where one thin sub-area sinks the whole unit (delivery zones where one district's empty shelves end a store's subscriptions, ride-hail cities where one starved neighbourhood breaks reliability, community groups where one idle chapter stalls the rest), so averages over the unit pick the wrong launch |
| Decision shape | Which of N gets one scarce thing: the nearby-marketplace pilot launches in one of ten metro counties (changed from one figure; see the report) |
| Committed call | The pilot county, and the users the feed would sustain trading for there, in thousands |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units (E30) recovered from the pilot log, with suppressed seller counts recovered from published metro totals at rung 2 (measured #24) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #7 uses the ready-made measure · #24 treats an unpublished figure as unknown · #4 never tests its reading against the control |
| Calibration form | Pilot log: last year's local-groups pilot, 60 town groups in six counties, each with its neighbourhood clusters' first-month listings, its sellers and link share, and its weekly trades at 90 days |
| Driving force | A local feed lasts only where every neighbourhood sees enough nearby listings. In last year's pilot, a town's group kept trading only if each of its neighbourhood clusters had at least 30 listings a week within 5 miles in its first month, and one starved cluster took the whole group down. Link shares, seller counts and mean listings all have flat loss curves on the pilot. The minimum is a construction over clusters and listing locations that no county figure carries, and the counties that lead on links and sellers have their listings piled into downtown clusters. |

## 1. Situation

A social platform will pilot a nearby-marketplace feed in one of ten metro counties. Its charter sends the pilot where the feed will
sustain local trading for the most users, judged on last year's local-groups pilot. The pack holds the county-pair link file, user counts
by neighbourhood cluster, the geography file, the town table of verified sellers (towns under 50 sellers suppressed, metro totals
published), the listings file with every active listing's location, the account and verification extracts, the charter, and the pilot
log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each link count, each cluster's users, each published seller count and metro total, each listing
  and each pilot outcome. Nobody ranks the candidates on the charter's basis and nothing reported is overturned. The difficulty is which
  towns a feed can sustain.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the growth team's ranking. Sellers per user, with the suppressed counts recovered, still send
  the pilot to Glenarm.
* **Instrument repair.** Suspect: the town seller table, with towns under 50 sellers suppressed. Published in full, rung 1 returns rung
  2's Glenarm and rung 2 is unchanged; rung 0 uses the complete link file and still names Ashbourne. The listings file and the cluster
  counts are complete, and the minimum over clusters is a law recovered from the complete pilot log, so the answer stays Fennick and the
  construction is still needed.
* **Lens swap.** The naive ranking judges each county by its average connectedness or supply; the answer counts only users in towns
  where every cluster clears, a different population of users.

## 3. The driving force

A strong solver knows local links alone do not make a market. It weighs supply, counting verified sellers per user by town, and recovers
the suppressed towns' counts from the published metro totals, so Glenarm leads. Then it back-tests on last year's pilot, and every
average stalls: link share predicts 41 of 60 groups, sellers per user 44, mean listings per cluster 46. The groups that died shared
something no average shows: one neighbourhood cluster with almost nothing nearby to buy. In the pilot, a town's group kept trading only
where every cluster had at least 30 listings a week within 5 miles in its first month, 60 of 60. Glenarm's listings are piled into two
downtown clusters and its suburbs are starved; Fennick's are spread across every cluster. Counted that way, Fennick sustains trading for
410,000 users.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Users in towns whose local link share is at least 85%, the growth team's proxy | A, Ashbourne (520k, 1.22× Bexley) | The release's own measure of local connectedness | The pilot log: link share predicts 41 of 60 groups' outcomes |
| 1 | Users in towns with at least 2.0 verified sellers per 1,000 users, suppressed towns failing | C, Corran (470k, 1.24× Fennick) | Supply and demand together, on the published table | The seller file: metro totals fix every suppressed town's count |
| 2 | The same, suppressed counts recovered from the metro totals | G, Glenarm (590k, 1.26× Corran) | Every count in the table now known | The pilot log: seller and mean-listing laws predict 44 and 46 of 60 groups |
| 3 | **Decisive:** users in towns whose every neighbourhood cluster had at least 30 listings a week within 5 miles | **F, Fennick (410k, 1.17× Dunmore)** (5th of 10 on rung 0) | — | — |

* **Position table.** Fennick ranks 5th on rung 0 (350k), 2nd on rung 1 (380k, 1.24× behind Corran, its only second place) and 4th on
  rung 2 (380k), and leads only rung 3.
* **Discriminator dominance.** Glenarm carries 1.55× into rung 3 (590k against 380k). The minimum keeps 0.25 of Glenarm's users and raises
  Fennick's 1.08×, an edge of 4.24×, against the 1.2 × 1.55 = 1.86 needed (2.28× headroom). The product, 4.24 / 1.55 = 2.73, is Fennick's
  lead over Glenarm on rung 3; Dunmore is runner-up at 350k.
* **Partial correction priced (L3).** A solver who takes the mean listings per cluster instead of the minimum names Glenarm at 1.27×
  Fennick (520k). One who takes the minimum but counts only listings inside each cluster names Dunmore at 1.18× Fennick (330k against
  280k). No half lands on Fennick.
* **Grid.** Law (local link share; sellers per user with suppressed towns failing or recovered; mean or minimum weekly listings per
  cluster, counted inside the cluster or within 5 miles) = 7 cells. Six name Ashbourne, Corran, Glenarm or Dunmore; only the 5-mile
  minimum names Fennick.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter judges on the pilot's outcome. The pilot log records clusters, listings and trades. No document says
   one starved cluster ends a group, or gives a threshold or a radius.
2. **Pattern B, a law with a flat-loss field of rivals.** The minimum of first-month weekly listings within 5 miles, at 30, returns 60 of
   60 pilot outcomes. Mean listings per cluster return at most 46 at any threshold, sellers per user 44 and link share 41. The law is a
   construction: listings within 5 miles of each cluster's centroid counted week by week, then the minimum taken over a town's clusters.
3. **No arithmetic symptom.** Cluster users sum to county totals, listings tie to the marketplace's counts, and recovered seller counts tie
   to every metro total.
4. **Not a row predicate.** A town's verdict depends on every cluster's count of listings within 5 miles, each built from thousands of
   listing locations.
5. **The enumeration is arithmetic.** No column marks a cluster as starved or a town as sustainable.
6. **No cutover date.** One pilot cohort and one month's listings, with nothing stepping.
7. **Survives deletion.** With every voice removed, recovered sellers per user still send the pilot to Glenarm.

## 6. The calibration corpus

* **Form.** The pilot log: 60 local groups in towns across six counties last year, each with its neighbourhood clusters, first-month
  weekly listings within 5 miles of each, its sellers and link share, and its weekly trades at 90 days.
* **What it certifies.** That supply matters, which every seller law confirms in part.
* **What pins the law.** The absolute split: every group whose clusters all cleared 30 sustained 20 or more trades a week, and every group
  with one cluster below 25 fell under 12.
* **Twin pair.** Towns T-12 and T-37 match on users (24,000), local link share, verified sellers and mean weekly listings per cluster
  (52). Their trades a week at 90 days were 22 and 11 (2.0×): one of T-37's five clusters saw 6 listings a week within 5 miles.
* **Resemblance points at the decoy.** On every county column, Glenarm resembles the pilot's busiest sustained towns.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the pilot goes to the county where the feed will sustain local trading for the most users, judged on last
  year's local-groups pilot, with ties broken toward more verified sellers. The geography file fixes the neighbourhood clusters.
* **Empirical pins.** The law, its threshold and its radius, from the pilot log.
* **Voices.** The growth lead: "Local friendship is what makes a nearby feed work, and Ashbourne's users are the most local." The seller
  programme manager: "Sellers are the supply; count verified sellers."
* **Licensed wrong basis.** The charter records that the growth team ranks counties on local link share and will present that ranking at
  the launch review.

## 8. Determinism by construction

* **Clusters.** Every user belongs to one cluster in the geography file, and every town's clusters are listed.
* **Threshold.** No cluster's first-month weekly listings within 5 miles lie between 25 and 35 in any candidate town.
* **Radius.** Listings are counted within 5 miles of each cluster's population-weighted centroid; none lies within 0.2 miles of the line.
* **Seller recovery.** Each metro area has exactly one suppressed town, so its seller count is exact.

## 9. Prompt sketch and deliverables

> The nearby feed pilots in one county next quarter, and growth tells me Ashbourne's users are the most local. Tell me which county gets
> the pilot and how many users the feed would sustain trading for there, in thousands, in a line for the launch review. Send
> `pilot_county.xlsx`, a chart `cluster_listings.png`, and a one-page `pilot_choice.pdf`.

* `pilot_county.xlsx` — sustained users for all ten candidates under each rung, the account sheet (ask A), the verification sheet
  (ask B) and the pilot table (ask C).
* `cluster_listings.png` — each candidate town's clusters as dots of weekly listings within 5 miles, the 30-listing line drawn, starved
  clusters ringed, each county's sustained users in the margin, and the chosen county marked.
* `pilot_choice.pdf` — the committed county, its sustained users, and why the leaders on links and sellers fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each candidate, the median age of active accounts. *Device:* reactivated accounts keep their
  creation date and log a reactivation date, as the account note documents; ageing them from creation overstates four counties.
* **Ask B (device-carried).** For each candidate, the median days from a seller's first verification attempt to approval. *Device:*
  timed-out attempts are retried under the same case ID with an attempt counter; counting attempts as cases overstates three counties.
* **Ask C (validity).** Each candidate's sustained users under each of the four rungs, and the pilot outcomes each of the four laws
  returns.
* **Decoupling.** Clearing the minimum over clusters changes no figure in asks A or B.

## 11. Rubric arithmetic

10 candidates (ask A) + 10 candidates (ask B) + 10 × 4 rung figures and 4 law counts (ask C) + the committed county, its sustained users
and its margin + 5 named chart parts + 3 files ≈ 75 criteria.

## 12. World-building constraints

* Sustained users (thousands): rung 0 Ashbourne 520, Bexley 425, Corran 400, Dunmore 380, Fennick 350, Glenarm 330; rung 1 Corran 470,
  Fennick 380, Bexley 370, Ashbourne 360, Dunmore 300, Glenarm 280; rung 2 Glenarm 590, Corran 470, Dunmore 440, Fennick 380; rung 3
  Fennick 410, Dunmore 350, Corran 300, Bexley 260, Ashbourne 240, Glenarm 150.
* Pilot outcomes returned: minimum within 5 miles 60, mean listings 46, sellers per user 44, link share 41. T-12 and T-37 match on every
  town column.
* Partial cells: Glenarm 520 (mean listings); Dunmore 330 against Fennick 280 (listings inside each cluster).
* Reactivation dates and verification attempts never touch a listing, a cluster or a seller count.
