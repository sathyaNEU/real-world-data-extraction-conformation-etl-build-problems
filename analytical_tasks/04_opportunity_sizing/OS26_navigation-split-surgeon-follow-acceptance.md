# OS26 — How a health plan splits 4,800 navigations across ten procedure groups, when members follow their surgeon and not the price list

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · health-plan network purchasing |
| Mirrors | Re-routing demand to a cheaper supplier when the buyer follows a relationship the price comparison cannot see (cloud workloads that move region only when the owning team already runs there, freight lanes that follow the shipper's broker, enterprise purchases that stay with the procurement contact's preferred vendor) |
| Decision shape | An allocation under a cap: 4,800 navigations bought from a vendor, split across ten outpatient procedure groups |
| Committed call | The split of the 4,800 navigations by procedure group, and the plan-year savings in allowed dollars that split buys |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield: a navigation converts only where the ordering surgeon already operates at a lower-priced site in the member's choice set), with E02 below it (the unit the cap counts is a case, not a claim line) |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #6 treats a mixed segment all one way |
| Calibration form | Counterparty acknowledgement file: the receiving sites' booking acknowledgements for all 2,240 navigations in last year's two-county pilot |
| Driving force | A member moves only if their surgeon moves with them. In the pilot, 918 of the 1,505 navigations whose ordering surgeon already operated at a lower-priced site in the member's 30-mile choice set converted, and 0 of the other 735. That property is not a column: it is a statistic over each surgeon's own case history across sites. The pilot's endoscopists split their lists between sites; the forward region's endoscopists almost all operate at one expensive hospital, so the group the pilot ranks first converts least. |

## 1. Situation

A regional commercial health plan has bought 4,800 navigations from a navigation vendor for next plan year. A navigator calls a member with
an upcoming outpatient procedure and offers a lower-priced in-network site at no extra cost-share. The vendor needs a split of the 4,800
across ten procedure groups, because it trains and staffs navigators by group. Six lower-priced hospitals and surgery centres have
acknowledged next year's tier-1 rates. Last year a pilot in two counties navigated 2,240 members, and the receiving sites acknowledged every
booking. The network director wants the navigations concentrated on endoscopy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the claims, the tier-1 rates, the pilot's acknowledgements and its acceptance by group. Nobody's
  number is overturned and no stakeholder read is refuted. The difficulty is which acceptance applies to next year's referrals in a region
  whose surgeons work differently from the pilot counties'.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the vendor's claim about its record. The pilot's own group acceptance still ranks
  endoscopy first, and no document mentions surgeons in connection with navigation.
* **Instrument repair.** No file is suspect. The claims carry every line with its rendering surgeon, the tier-1 rates and all 2,240
  acknowledgements are complete, and member addresses are current. Nothing is blank, stale or narrower than it claims, so rungs 0, 1 and 2
  still return MRI, arthroscopy and endoscopy. A ten-times-larger pilot keeps the group rates right for the pilot counties and wrong for a
  region whose surgeon mix by group is inverted, so the shared-surgeon construction is still needed for cataract.
* **Lens swap.** The pilot counties' referrals last year and the forward region's referrals next year are different populations at
  different moments. The answer rests on the forward population's surgeon mix, which no lens on the pilot can supply.

## 3. The driving force

A strong solver builds cases from claim lines, prices each group's gap at the acknowledged tier-1 rates, and replaces the pooled pilot
acceptance with each group's own pilot acceptance. Each step is correct, and the result sends 2,600 navigations to endoscopy, the group
with the best pilot record. But the acknowledgement outcomes split absolutely on a property of a different entity. A member converts only
when the surgeon who ordered the procedure has performed at least one case at a receiving site inside the member's choice set. That is a
two-hop construction: case → ordering surgeon → that surgeon's two-year case history by site → the member's 30-mile set of receiving sites.
Group acceptance is therefore 0.61 times the group's shared-surgeon share. That share was 0.95 for endoscopy in the pilot counties and is
0.15 in the forward region, where nearly every endoscopist operates only at the expensive teaching hospital. Cataract runs the other way,
from 0.44 to 0.80.

## 4. The ladder

| Rung | Construction | Names (group ranked first) and figure | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Claim lines as units, tier-1 gaps, pooled pilot acceptance 0.41, greedy fill of 4,800 by value per navigation | A, MRI (1.26× arthroscopy); $1.27M, −33.6% | Every input is filed and correct, and the fill respects the cap and each group's volume | The vendor contract and the acknowledgement file count a navigation as one member's procedure day at one site; the pilot's 2,240 reproduce from claims only at that grain |
| 1 | Hygiene: lines rolled up to cases (member × site × day), same acceptance | B, arthroscopy (1.21× endoscopy); $3.42M, +78.5% | The unit now matches the contract and the acknowledgements, and every count reconciles | Pilot acceptance runs from 0.27 (cataract) to 0.58 (endoscopy), so one pooled rate misprices every group |
| 2 | Each group's own pilot acceptance × its tier-1 gap per case | C, endoscopy (1.41× arthroscopy); $4.09M, +113.7% | Group-specific, causal, correctly costed and reproduced by the pilot in every group | The acknowledgements split 918 of 1,505 against 0 of 735 on the ordering surgeon's sites, and the forward region's surgeon mix differs by group |
| 3 | **Decisive:** acceptance 0.61 × each group's forward shared-surgeon share, built from base-year claims through the surgeon's site history and the member's choice set; refill the cap | **E, cataract (1.40× hernia); $1.91M** (4th of 10 on rung 0) | — | — |

* **The answer.** Cataract 1,400, hernia 800, MRI 1,300 and arthroscopy 1,300 navigations; nothing to endoscopy. Savings $1,910,000.
* **Position table.** Cataract ranks 4th on rung 0, 5th on rung 1 and 6th on rung 2, and leads only rung 3. It is never 2nd. Rung leaders
  beat their runners-up by 1.26×, 1.21×, 1.41× and 1.40×.
* **Discriminator dominance.** Endoscopy carries a 3.11× value-per-navigation lead over cataract into rung 3 (985 against 317). Cataract's
  shared-surgeon share rises from 0.44 to 0.80 (×1.82) while endoscopy's falls from 0.95 to 0.15 (×0.158), an edge of 11.5×. That is
  3.1 times the required 1.2 × 3.11 = 3.73.
* **Sign discipline.** The two corrections walk the figure up (+78.5% at rung 1, +113.7% at rung 2) and the decisive move reverses it to
  $1.91M. A solver who stops anywhere short over-promises savings to the council.
* **Partial correction priced (L3).** A solver who sees that acceptance depends on the surgeon but applies the region-wide shared share
  (0.541) to every group keeps the rung-1 order, arthroscopy first by 1.21× over endoscopy, and lands at $2.75M (+43.6%), further from the
  answer than rung 0. A solver who conditions on surgeons but carries the pilot counties' shares reproduces rung 2 exactly, endoscopy first
  by 1.41×. The rung-2 plan's realised savings under the true acceptance is $0.90M, which is the comparison the note has to state.
* **Grid.** Unit (line, case) × price (current receiving price, tier-1 rate) × acceptance (pooled, group pilot, surgeon-conditioned) = 12
  cells, and no non-answer cell reproduces the answer's split. The nearest is line grain with group pilot acceptance at −15.3%, led by MRI.
  The decisive conditioning at current receiving prices lands at −24.5%, led by hernia (1.11× cataract) with sleep studies in the split,
  because the receiving sites' tier-1 discount is deepest on cataract. Every other cell is more than 30% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** No document connects surgeons to navigation. The acknowledgement file has no surgeon field, and the vendor's service
   description talks only about members and sites.
2. **The corpus pins the conditioning only through a join.** The acknowledgement file carries navigation number, group, origin site,
   receiving site and outcome. In every pilot group the group's own acceptance reproduces its outcomes exactly, because the pilot's surgeon
   mix is the pilot's own. The 0-against-61 split appears only after the claim-side join to each surgeon's site history, so every group-by
   the file supports shows a gradient (0.27 to 0.58) and never the split.
3. **No arithmetic symptom.** Lines, cases, navigations, acknowledgements and allowed dollars reconcile on every rung, and the pilot ties to
   the vendor's invoices.
4. **Not a row predicate.** The property belongs to a different entity: a statistic over the ordering surgeon's 24-month case history by
   site, matched against the member's choice set (member address to site distances). It is then rolled up to a forward share by group.
5. **The enumeration is arithmetic.** No column says "surgeon also operates at a receiving site". Forward acceptance per group is a computed
   share over 13,600 base-year cases.
6. **No cutover date.** Surgeons' site patterns are stable across the three base years, and no series steps.
7. **Survives deletion.** Remove every voice: the group acceptance still points at endoscopy and the split is still two joins away.

## 6. The calibration corpus

* **Form.** The receiving sites' booking acknowledgements for every pilot navigation: booked, completed, declined by member, or declined
  for no slot. There are 2,240 navigations, 918 completed, and 0 declined for no slot.
* **What it certifies.** The case grain (pilot completions reproduce from claims only as member × site × day) and each group's in-sample
  acceptance. A solver who back-tests rungs 1 and 2 against it is confirmed.
* **The absolute split (O2).** 0 of 735 navigations converted where the ordering surgeon had no case at a receiving site in the member's
  choice set. 918 of 1,505 (61.0%) converted where the surgeon had one, in every group and both counties. No surgeon in the pilot had
  between one and three receiving-site cases, so lookback length does not move the split.
* **Twin pair.** Pilot origins Bramwell Community and Ferris Lake Medical are identical on group mix, origin prices, distance to the nearest
  receiving site, member age mix and navigations (214 each). Acceptance was 0.58 at Bramwell and 0.26 at Ferris Lake, 2.2× apart. Their
  surgeons' shared shares are 0.95 and 0.43, and no origin- or group-level rate reproduces both.
* **Resemblance points at the decoy.** The forward region's endoscopy origins match the pilot's endoscopy origins on volume, price and
  member mix. Pilot endoscopy had the best acceptance on file.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The vendor contract fixes 4,800 navigations for the plan year, a navigation being one member's procedure day at one site.
  The programme charter scores the programme on the plan-year reduction in allowed dollars on navigated cases. The member-communications
  policy offers navigation to every referral in an allocated group, in arrival order, until the group's allocation is used. The network
  adequacy standard defines a member's choice set as in-network sites within 30 miles of home.
* **Empirical pins.** The 0.61 conversion and the conditioning property come from the acknowledgements joined to claims. Forward shared
  shares come from base-year claims.
* **Voices.** The network director: "Endoscopy is where our money goes, so that's where navigation belongs." The vendor's account lead: "Our
  acceptance has held in every market we've worked in." That is true of the pilot counties.
* **Licensed wrong basis.** The charter records that the employer council's actuary prices steering programmes on pilot acceptance by group
  and will present that basis at the council.

## 8. Determinism by construction

* **Lookback.** Every surgeon with a receiving-site case has one in the last 12 months, so 12-, 24- and 36-month lookbacks return the same
  surgeon set.
* **Choice-set radius.** No member in the ten groups lives between 27 and 33 miles from any receiving site, so 25-, 30- and 35-mile radii
  return the same choice sets.
* **Arrival order.** Shared and non-shared referrals arrive interleaved in every group, so the first n navigations carry the group's shared
  share to within one point at every n.
* **Fill boundary.** The answer's fill ends exactly at a group boundary (1,400 + 800 + 1,300 + 1,300). The first unfunded group, cystoscopy,
  sits 1.17× below arthroscopy, so no tie decides the split.
* **Receiving capacity.** Acknowledged capacity exceeds completions under every rung's allocation by at least 30%, so it never binds.
* **Maturity.** The base year closed 15 months before the extract. No claim line posted after month 6 of run-out, so the three base years
  are complete and flat to within 1%.

## 9. Prompt sketch and deliverables

> Our vendor has sold us 4,800 navigations for next plan year, and I have to tell the employer council how we'll spend them and what they
> will save. Our network director is sure endoscopy is where they belong. Give me the split across the ten procedure groups and the savings
> in allowed dollars, rounded to the nearest $10,000, in one sentence I can paste into the council paper. Send `navigation_plan.xlsx`, a
> chart `navigation_value.png`, and a one-page `council_note.pdf`.

* `navigation_plan.xlsx`: the allocation and its savings by group, the receiving-site sheet (ask A) and the authorisation sheet (ask B).
* `navigation_value.png`: value per navigation by group as grouped bars under the pooled, group-pilot and surgeon-conditioned bases, sorted
  on the conditioned basis. It shows the 4,800 fill as a cumulative line, marks the funded groups, and annotates endoscopy's shared-surgeon
  share (0.95 in the pilot, 0.15 forward).
* `council_note.pdf`: the committed split, the savings figure, and the endoscopy-led plan's realised savings beside it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six receiving sites, acknowledged tier-1 capacity for each quarter of next year,
  and the share of it the committed split would use. *Device:* capacity acknowledgements are amended by superseding versions with a version
  number, and the latest version per site and quarter governs, as the acknowledgement specification says. Summing versions overstates
  capacity at four sites. Taking the first version understates it at two. Amendments only ever raise capacity, so no reading binds the main
  call.
* **Ask B (device-carried).** For each of the ten groups, median prior-authorisation turnaround in base-year working days, and the share of
  requests pended for information. *Device:* a pended request that is resubmitted gets a new request number, linked through an
  original-request field the authorisation guide documents. Counting resubmissions as new requests inflates volume by 14% and halves the
  measured turnaround in three groups. The main call never uses authorisations.
* **Ask C (validity).** Savings under each of the four rung bases, and the realised savings of the rung-2 allocation under
  surgeon-conditioned acceptance ($0.90M).
* **Decoupling.** Clearing the surgeon conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

10 groups × 2 (navigations, savings) + 6 sites × 4 quarters × 2 (ask A) + 10 groups × 2 (ask B) + 5 figures (ask C) + the committed total,
the cataract-over-hernia margin and the endoscopy comparison + 5 named chart parts + 3 files ≈ 104 criteria.

## 12. World-building constraints

* Pilot: 2,240 navigations, 1,505 with a shared surgeon (918 completed, 61.0%), 735 without (0 completed). Pooled acceptance 0.41.
  Pilot shared shares by group: endoscopy 0.95, MRI and upper GI 0.90, arthroscopy 0.56, hernia 0.51, cataract 0.44.
* Forward shared shares: endoscopy 0.15, upper GI 0.20, arthroscopy 0.22, hernia 0.48, MRI 0.70, cataract 0.80, CT and sleep studies 0.95.
  Region-wide 0.541.
* Tier-1 gaps per case: arthroscopy $2,050, endoscopy $1,700, hernia $1,400, upper GI $1,250, cataract $1,180, MRI $760. Lines per case:
  endoscopy 3.2, arthroscopy 3.4, hernia 3.0, upper GI 2.8, cataract 2.4, MRI 1.0.
* Forward cases at higher-priced origins total 13,600 (P/K 0.35), including cataract 1,400, hernia 800, MRI 1,300, arthroscopy 1,300 and
  endoscopy 2,600. At current receiving prices the gaps are cataract $700, arthroscopy $1,500, hernia $1,300 and cystoscopy $580.
* Rung figures are $1.27M / $3.42M / $4.09M / $1.91M. No other cell of the 12-cell grid lies within 15% of the answer.
* Bramwell and Ferris Lake are identical on every claims-side and acknowledgement-side column except the surgeons' site histories.
* Capacity amendments and authorisation resubmissions never touch the claims, the acknowledgements or the surgeon histories.
