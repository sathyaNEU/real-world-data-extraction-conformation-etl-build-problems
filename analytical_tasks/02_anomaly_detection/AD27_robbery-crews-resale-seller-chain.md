# AD27 — How many robbery crews are behind the spring rise, and which ground each series team covers

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Demographic & Social Science · urban crime analysis |
| Mirrors | Trust-and-safety teams sizing coordinated abuse by the accounts that cash out rather than by where it surfaces (marketplace fraud rings linked through payout accounts at Amazon and eBay, coordinated-inauthentic-behaviour takedowns at Meta linked through shared infrastructure, card-testing rings linked through the merchants they settle at) |
| Decision shape | A structure the body adopts: how many series teams the summer plan stands up and which districts each one covers, scored on whether each team holds exactly one offender group |
| Committed call | The number of new series teams and the districts each covers, signed into the summer deployment plan on 30 May |
| Gap · Pattern | Gap 2 (population: the unit is the offender group, not the area) over Gap 4 (rule) · an implicit join through a second identifier, with Pattern B (the settled ledger pins the linkage) and a suppressed cell bounded by a rounded published share and its published base below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #18 joins only on the visible key · #24 treats an unpublished figure as unknown · #4 never tests its reading against the control |
| Calibration form | Settled-transaction ledger: the property-recovery ledger of 31 robbery series closed by charges in 2023–2025, with every recovered phone's resale transaction |
| Driving force | A crew is the people who rob, and the people who rob are the people who sell. A crew's MO signature follows the ground it works (moped snatches on D7's streets, platform robberies at the D9 station), and a space-time scan sees two districts as two clusters. The phones taken in D7 and D9 are sold at buy-back kiosks by the same four people, which shows only through incident → item IMEI → resale transaction → seller → that seller's other transactions → their IMEIs → their incidents. That chain, and no area-based linkage, reproduces all 31 settled series. |

## 1. Situation

Phone robberies in districts 7 to 10 rose 38% in the twelve weeks to 3 May. The deputy chief signs the summer deployment plan on 30 May, and
department policy gives every offender group behind a rise its own series team (a sergeant and six detectives, funded from patrol overtime).
The crime analysis unit holds the incident extract with each report's property items and coded MO signature, the state's resale ledger of
every phone bought by a licensed kiosk or dealer, and the property-recovery ledger of closed series. The D8 commander wants the weight on
the university corridor. The juvenile unit believes the new cluster at the D9 rail station is a juvenile group.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the incident counts, the MO signatures (each a true record of how a robbery was done), the kiosk
  transactions and the records division's juvenile table. No one's reading of their own numbers is overturned, and the commander is right
  that D8 is busy. The difficulty is that the unit the plan funds is an offender group, and no file is keyed on it.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the department's hotspot map. A space-time scan confirmed by MO signature still returns three
  district series, and still splits one crew in two.
* **Instrument repair.** Suspect files: the property sub-table's IMEI field (blank for 26% of incidents) and the records division's
  suppressed beat-level juvenile cells. Capture every IMEI and publish every beat cell: rung 0 still names {D8, D10}; rung 1 no longer hands
  the station cluster to the juvenile unit and names {D7, D8, D9}; rung 2 still names {D7, D8, D9}. The MO signature records how a robbery
  was done, a different attribute from who did it, so using it for linkage is an ordinary rung. The seller chain is still needed: no perfect
  incident record says who sold the phone.
* **Lens swap.** The naive structure partitions incidents by where they happened; the answer partitions them by who sold the proceeds. These
  are different populations of incidents (crew C's persistent D10 activity leaves, D7 and D9 join), not one population under two lenses.

## 3. The driving force

A strong solver discounts the hotspot map, runs a space-time permutation scan so that only interaction (high here and now against both
margins) counts as emerging, and confirms each cluster by MO signature. Every step is correct, and every step is keyed on place, because
the incident file is. The explicit key looks complete: every recovered phone is matched to its report by IMEI, one to one. The crew that
robs in D7 and D9 rides the rail line between them, snatches from mopeds in D7 and robs on the D9 platforms, and sells at kiosks in a third
district. Phones carry IMEIs on the property sub-table, the state's resale ledger records each purchase with the seller's ID, and the same
four sellers cash out phones from both districts. Building that chain and taking its connected components is a construction across two
files, and the property unit's recovery practice (match a held phone to its report by IMEI) is the only place the link is documented.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | CompStat hotspot read: beats over the department's twelve-week hotspot line | Two teams: D8 and D10 | The department's own map; D8 and D10 carry the most robberies | The 2023–2025 incident history: D10's spring level is the same every year, and its stadium detail already covers it |
| 1 | Space-time permutation scan (emerging only), with the D9 station cluster left to the juvenile unit because juvenile cells are suppressed | Two teams: D7 and D8 | The right detection method, and juvenile records are legally withheld from the unit | The records division's monthly release: D9's juvenile-suspect share of robberies, published to the whole per cent (3%), and its published count of 262 put D9's juvenile-suspect robberies at 7 to 9, so beat 931 holds at most 9 of its 98 |
| 2 | Scan with D9 restored as an adult cluster, each cluster confirmed by MO signature | Three teams: D7, D8, D9 | Three emerging clusters, each with one consistent MO | The settled ledger: MO linkage reproduces 14 of 31 settled series, and all 17 misses are crews that changed MO between districts |
| 3 | **Decisive:** link incidents through item IMEI → resale transaction → seller → the seller's other transactions, take connected components, keep the components inside emerging clusters | **Two teams: D7 with D9, and D8** | — | — |

* **Structure table.** The four rungs name four different partitions: {D8, D10}, {D7, D8}, {D7, D8, D9} and {D7+D9, D8}. No intermediate
  rung holds the answer's territory, and the answer's merged team appears on no rung below it. Three of the partitions have two teams, so
  the committed call is stated and graded team by team on territory, never on the count alone.
* **Partial correction priced (L3).** A solver who joins incidents to the resale ledger but links by kiosk instead of by seller merges
  crews A and B, which both cash out at the Riverside mall kiosks (96 of their 512 resales), and adopts one team for D7, D8 and D9: a team
  short, on a linkage that reproduces 11 of the 31 settled series. A solver who follows the seller chain but keeps linkage inside each
  district splits crew A at the D7–D9 line (its sellers' 249 resales divide 111 and 138) and adopts rung 2's three teams, a team too many.
  Neither holds the answer's merged D7–D9 team.
* **Grid.** Baseline (hotspot counts or scan) × juvenile claim (accepted or bounded) × linkage (MO signature, kiosk, seller) = 12 cells.
  Every cell without seller linkage names rung 0, 1 or 2's partition or the kiosk merge; seller linkage over hotspot zones keeps the D10
  team; with the juvenile claim accepted, D9 goes to the juvenile unit and seller linkage leaves rung 1's {D7, D8}. Only the scan
  population with the juvenile cells bounded and seller linkage names {D7+D9, D8}.
* **Component dominance.** The answer is not a ranking, so dominance is stated as separation: of crew A's 415 incidents, 307 carry an
  IMEI and 262 of those phones were resold; its four sellers account for 249 of the 262 (95%), with the other 13 sold by one-off buyers who
  link to nothing else. No 2026 seller ever sold a phone taken outside their own component.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The property unit's procedure says a held phone is matched to its report by IMEI, for return to the owner. No
   document links incidents to each other through sellers, and the series policy speaks only of offender groups.
2. **The corpus pins a construction, not a menu (Pattern B).** Seller-chain components reproduce all 31 settled series. The best rival,
   MO-signature linkage, reproduces 14; kiosk linkage 11; space-time clusters 9. The reproducing rule is a bipartite graph built across two
   files and projected onto incidents, and no document offers it as a candidate to sweep.
3. **No arithmetic symptom.** Incidents, items, IMEIs and resale transactions reconcile one to one; every incident carries one MO signature;
   the scan's margins tie to the extract under every partition.
4. **Not a row predicate.** It needs a join through the property sub-table to the ledger, a self-join on seller, and connected components
   over 1,460 incidents.
5. **The enumeration is arithmetic.** Crew membership is computed; no column names a crew, and no 2026 MO signature spans crew A's two
   districts.
6. **No cutover date.** Crew A has robbed in both districts since February with no step in any series; the rise is a level in two districts
   at once.
7. **Survives deletion.** Remove both voices and the hotspot map, and the district-keyed analysis remains the natural build.

## 6. The calibration corpus

* **Form.** The property-recovery ledger of 31 series closed by charges in 2023–2025: every member incident, every phone recovered through a
  resale hold, the resale transaction it was recovered from, and the series it was charged under.
* **What it pins.** Seller-chain components reproduce 31 of 31 memberships. MO-signature clusters split 17 cross-district series and return
  52 series against 31; kiosk linkage merges series that shared kiosks and returns 19. Each rival misses in one direction, so none
  reconciles on the count either.
* **Every rule exercised.** One settled series sold at four kiosks in three districts, so kiosk location cannot stand in for the seller. One
  settled seller also traded in his own phone, a transaction that links to no incident and merges nothing.
* **Twin pair.** Settled series 2024-11 and 2025-03 each appeared as two emerging clusters in non-adjacent districts, identical on incident
  counts, weeks active, suspect counts and their two MO clusters. 2024-11 was one crew and 2025-03 two, so one series against two, separated
  only by whether the sellers are shared.
* **Resemblance points at the decoy.** Of the seven settled cases with clusters in two non-adjacent districts, five were separate crews, so
  a nearest-case lookup votes for a team per district.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The series policy: each offender group behind a rise gets one series team, which works that group's incidents wherever
  they occur. The property unit's procedure on IMEI matching for recovery. One sentence each.
* **Empirical pins.** The linkage rule, from the settled ledger. The emerging test, from the analysis unit's standing scan settings.
* **Voices.** The D8 commander: "It always starts in the university corridor; put the weight there." The juvenile unit lieutenant: "That
  station cluster is our kids, not a series team's job."
* **Licensed wrong basis.** The crime-strategy directive records that the CompStat unit characterises series from its district hotspot map
  and will present the map at the planning meeting.

## 8. Determinism by construction

* **Seller identity.** The seller ID is a hash of the state identity number captured at the kiosk; every 2026 crew seller used one
  identity throughout, and no seller sold phones from two components.
* **Window and reach.** Components are the same over 8-, 12- and 16-week windows and with or without dealers outside the city, because
  every crew A and crew B sale happened at city kiosks.
* **Persistence.** Crew C's D10 component is non-emerging under every scan window from 8 to 16 weeks.
* **Coverage.** IMEIs are captured for 74% of incidents. Each crew component holds at least 120 linked incidents, so the unlinked quarter
  changes no team's territory.
* **The juvenile bound.** The claim fails at the bound's upper end (9 of 98, 9%), so no reading of the rounding or the suppressed beat cells
  restores it.

## 9. Prompt sketch and deliverables

> Before the summer plan is signed on the 30th I need to know how many robbery crews are behind this spring's rise and which ground each
> one works, because every crew gets its own series team. The D8 commander is convinced it all starts in the university corridor. Give me
> the number of teams and the districts each covers, as a line I can drop into the plan, with `crew_structure.xlsx`, a chart
> `crew_links.png`, and a one-page `deployment_memo.pdf`.

* `crew_structure.xlsx` — linked incidents per crew per district, the response-time sheet (ask A), the clearance sheet (ask B) and the
  reproduction table (ask C).
* `crew_links.png` — the linkage graph: incidents as nodes coloured by district, sellers as hubs, resale transactions as edges, the two
  emerging components outlined, crew C's persistent component greyed, and each component's weekly count annotated.
* `deployment_memo.pdf` — the committed structure and why each rung's structure falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of districts 7 to 10, the median and 90th-percentile response time to robbery-in-progress
  calls over the twelve weeks, and the number of upgraded calls. *Device:* a call upgraded to robbery-in-progress after a lower-priority
  dispatch carries two dispatch records, and the CAD guide says response time runs from the upgrade. Timing from the first dispatch
  inflates three districts. The crew structure never uses CAD data.
* **Ask B (device-carried).** For each district, the 2025 phone-robbery clearance rate and the number of 2025 clearances that close
  offences from earlier years. *Device:* the reporting guide counts a clearance in the year it happens, whatever year the offence was, so a
  same-year cohort rate misstates three districts.
* **Ask C (validity).** For each of the four rung structures, its hits on the 31 settled series and its team count.
* **Decoupling.** Clearing the seller linkage and the juvenile bound changes no figure in asks A or B.

## 11. Rubric arithmetic

4 districts × 3 (ask A) + 4 × 2 (ask B) + 4 structures × 2 (ask C) + the committed team count, each team's districts, the linked incidents
per crew and the juvenile bound + 5 named chart parts + 3 files ≈ 40 criteria.

## 12. World-building constraints

* 1,460 phone robberies in the extract: crew A 184 in D7 and 231 in D9 (98 at beat 931), crew B 402 in D8, crew C 286 in D10, 357
  unlinked background incidents.
* Crew A's IMEI-linked phones are sold by four sellers and crew B's by three; both cash out partly at the Riverside mall kiosks (96 of
  512 resales: A 262, B 250 from 296 IMEI-carrying incidents). No 2026
  seller crosses components. Crew A snatches from mopeds in D7 and robs on the platforms in D9, two MO signatures.
* The records division suppresses beat-level juvenile counts and publishes each district's juvenile-suspect share of robberies to the whole
  per cent with its robbery count: D9 3% of 262 (crew A's 231 and 31 background incidents), so 7 to 9 in D9 and at most 9 of beat 931's 98.
* The settled ledger holds 31 series; 17 crossed a district line. Twins 2024-11 and 2025-03 are identical on every visible column.
* CAD records and the 2025 clearance file never touch the incident extract, the property sub-table or the resale ledger.
