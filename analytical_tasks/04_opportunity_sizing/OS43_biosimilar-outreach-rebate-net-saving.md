# OS43 — How a health plan spends 1,500 biosimilar outreach contacts, when the pilot's saving per switch was measured where no rebate exists

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · health-plan drug purchasing |
| Mirrors | Switching savings sized at list price when the incumbent pays back part of what it charges (cloud migrations priced without the incumbent's committed-spend credits, procurement moves away from suppliers whose year-end volume rebates exceed the unit-price gap, carrier switches that forfeit loyalty rebates) |
| Decision shape | An allocation under a cap: 1,500 pharmacist outreach contacts this year across six reference biologics, one contact per member |
| Committed call | Contacts per biologic, and the drug spend the plan avoids this year, to the nearest $100,000 |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · E17 (a per-switch saving validated on clinic-billed infusions, where no rebate exists, applied to self-injected pharmacy-benefit biologics whose reference products return 15% to 45% of their cost through PBM rebates), with E19 below it (outreach-driven switches told apart from hospital clinics' whole-panel formulary switches by their one-week clustering) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #17 guesses an attribution the data can settle · #7 uses the ready-made measure |
| Calibration form | Pilot log: last year's outreach pilot, 1,200 prescriber contacts at 30 clinics on the two clinic-billed infusions, each with its outcome, claims-verified switch date and the plan's paid amounts before and after |
| Driving force | A switch saves the plan the reference's net cost less the biosimilar's. On the pharmacy benefit the reference's maker pays back 15% to 45% of its price through PBM rebates that never appear on a claim. The pilot's gross saving per switch reproduced all 312 settled switches, because both pilot molecules are clinic-billed infusions, where rebates do not exist. Carried to self-injected B2, it prices a switch at $73,000 a year; net of its 35% rebate the switch saves $22,250. Only the quarterly rebate statements, divided over each product's claims, put the contacts where the savings are. |

## 1. Situation

A regional health plan's pharmacy team contacts prescribers to move members from six reference biologics to their biosimilars. Its two
clinical pharmacists can make 1,500 contacts this year, and each contact concerns one member. Two of the biologics are infusions that
clinics buy and bill on the medical benefit (B3, B4); four are self-injected and dispensed on the pharmacy benefit (B1, B2, B5, B6). Last
year's pilot made 1,200 contacts on the two infusions. Finance books drug spend as the plan's ledger records it. The pharmacy director
expects the biggest savings where list prices are highest.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the price files, the claims, the pilot log, the vendor's invoice and the rebate statements. The
  pharmacy director is right that list prices are highest on the self-injected drugs. Nothing reported is overturned. The difficulty is
  that a pilot saving measured where no rebate exists does not price a switch where one does.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and every voice. The pilot's per-switch formula still reproduces 312 of 312 settled
  switches, and no document says it fails anywhere.
* **Instrument repair.** Suspect files: the pilot log, which counts every switch within 60 days with no field for its cause, and the price
  file the pilot used, superseded on 1 January. Repaired, rungs 0 and 1 become rung 2 and name B2 ($29,200 a contact). Claims and rebate
  statements are complete, and the pilot molecules carry no rebate however well they are recorded, so the rebate netting is still needed for
  B3.
* **Lens swap.** Pharmacy-benefit members whose reference cost is partly repaid are a different population from the clinic-billed members
  the pilot measured, not the same members under another lens.

## 3. The driving force

A strong solver prices each switch from the plan's current price file and refuses the pilot's headline yield. Hospital clinics switch whole
panels by formulary decision, so it credits outreach only with switches the vendor's settled invoice pays for. It then applies the pilot's
saving per switch, the reference's annual cost less the biosimilar's. The formula reproduces every settled pilot switch to the dollar and
names B2. But both pilot molecules are clinic-billed infusions, and the four self-injected biologics are paid through the pharmacy benefit.
There, each reference's maker pays the plan a quarterly rebate through the PBM: 20% of B1's cost, 35% of B2's, 45% of B5's and 15% of
B6's. No biosimilar carries one. Rebates arrive as remittances by product and quarter, posted against drug spend in finance's ledger, and no
claim shows them. A switch from B2 removes $145,000 of claims cost and $50,750 of rebate, and adds $72,000 of biosimilar cost: it saves
$22,250, not $73,000. Net of rebates, the clinic-billed B3 is the best use of a contact.

## 4. The ladder

| Rung | Construction (saving per contact, a year; contacts filled by value up to each biologic's members) | Names (ranked first) and saving | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Pilot's reported yield (55%) × the pilot's gross gap per switch, at the price file the pilot used | A, B1, $57,200 (1.21× B4); $85.8M, +316.5% | The pilot's own formula and its own success rate | The price file in force from 1 January: B1's reference cut its list price from $118,000 to $42,000 a year, so its gap is $28,000 |
| 1 | The same at current prices | B, B4, $47,300 (1.18× B2); $68.1M, +230.6% | Validated formula, current prices | The vendor's settled invoice pays for 312 of the pilot's 660 switches: the other 348 were hospital clinics moving whole panels within one week |
| 2 | Outreach-driven yield by setting (40% in offices, 12% in hospital clinics), switches attributed by their one-week clustering | C, B2, $29,200 (1.96× B3); $35.2M, +70.9% | The pilot's formula, applied with the yield the money settled | The PBM's rebate statements: the plan recovers 35% of B2's reference cost, 45% of B5's, 20% of B1's and 15% of B6's, and no biosimilar carries a rebate |
| 3 | **Decisive:** saving per switch = reference cost × (1 − its rebate share) − biosimilar cost, the share from the quarterly statements divided over each product's claims | **E, B3, $14,880 (1.17× B4)** (4th of 6 on rung 0); **$20,598,400** | — | — |

* **The answer.** B3 700 contacts and B4 800, none to the self-injected biologics, avoiding $20,598,400 of drug spend, committed as
  $20,600,000.
* **Position table.** B3 ranks 4th on rung 0, 3rd on rung 1 and 2nd on rung 2 (1.96× behind B2), and leads only rung 3. Rung leaders beat
  their runners-up by 1.21×, 1.18×, 1.96× and 1.17×.
* **Discriminator dominance.** B2 carries a 1.96× lead into rung 3 ($29,200 against $14,880). Its net saving is 0.305 of its gross gap and
  B3's is 1.00, an edge of 3.28×, which is 1.39 times the required 1.2 × 1.96 = 2.36.
* **Figure shape.** Every correction walks the saving down (−20.6%, −48.3%, −41.5%), and the answer is the minimum cell of the grid.
* **Partial correction priced (L3).** Every half-netted rebate keeps B2 first. Netting the plan-wide rebate share (15% of gross pharmacy
  spend) gives B2 $20,500 a contact against B3's $14,880 (1.38×) and $27.4M (+32.9%). Taking each product's rebate share off the gap,
  rather than off the reference's cost, gives B2 $18,980 (1.28×) and $26.0M (+26.3%), because it misses the rebate on the part of B2's
  price that the biosimilar still costs.
* **Grid.** Prices (pilot file, current) × yield (reported, outreach-driven by setting) × saving (gross, net of rebates) = 8 cells. Every
  non-answer cell puts B1, B4 or B2 first and sits at least 70% above the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one saving formula. The rebate statements are a finance remittance file, and no document
   connects rebates to switching or says which biologics carry them.
2. **Corpus blind for a computable reason.** *In every pilot switch the reference carried no rebate, because both pilot molecules are
   infusions that clinics buy and bill on the medical benefit, where PBM rebates do not exist.* The gross formula reproduces all 312 settled
   switches' savings to the dollar, and the rebate shares are zero for every row it ever met.
3. **No arithmetic symptom.** Claims, members, pilot savings and the vendor's invoice reconcile on every rung, and the rebate remittances
   tie to the ledger whichever saving a solver uses.
4. **Not a row predicate.** A switch's net saving needs each reference's quarterly rebate dollars divided over that product's claims, a
   share no claim carries.
5. **The enumeration is arithmetic.** No column holds a net price, and no claim holds a rebate.
6. **No cutover date.** B1's 1 January list cut is the dated decoy, killed at rung 1. Rebate shares have run within a point of their annual
   level for four quarters.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** 1,200 contacts at 30 clinics (15 office practices, 15 hospital outpatient clinics) on B3 and B4, each with the contact's
  outcome, the claims-verified switch date, the plan's paid amounts for twelve months either side, and the vendor's audited invoice.
* **What it certifies.** The saving per switch (reference cost less biosimilar cost), which reproduces all 312 settled switches, and the
  outreach-driven yields: 240 of 600 office contacts (40%) and 72 of 600 hospital-clinic contacts (12%).
* **The latent attribution (E19).** The pilot counted 660 switches within 60 days of a contact (55%). At nine hospital clinics every
  patient on the molecule switched within the same seven days, contacted or not; those 348 are formulary switches, and only excluding them
  reproduces the vendor's invoice.
* **What it is blind to.** Rebates (above).
* **Twin pair (free training instance).** Two years ago the PBM moved the plan's members on two insulins, I-1 and I-2, to biosimilars on
  its own formulary. The two are identical on every column a lookup reaches: list price ($3,600 a year), biosimilar price ($1,200),
  members switched (400 each), prescriber mix and pharmacy channel. Net of the reference makers' rebates, which the ledger posts by
  product and quarter, a switch saved $960 on I-1 and $1,860 on I-2, 1.94× apart, because the PBM returned 40% of I-1's cost and 15% of
  I-2's. Only the rebate statements, joined by product, separate them. The switches were the PBM's, outside the pilot, and the plan's
  annual report booked them gross, so the rebates changed nothing anyone priced. On B1, B2, B5 and B6 the same rebates decide.
* **Resemblance points at the decoy.** By prescriber type and gross gap, B2 resembles the pilot's best office practices, so a solver
  transferring the pilot's saving per switch by resemblance carries it to B2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme is scored on the drug spend the plan avoids this year, as finance books it. A member is contacted once, and
  members are those with a reference claim in the last 90 days. The price file in force on 1 January prices the year.
* **Empirical pins.** Outreach-driven yields by setting, from the pilot and the vendor's invoice; rebate shares by product, from four
  quarters of statements.
* **Voices.** The pharmacy director: "The highest list prices are where biosimilars pay off." The medical director: "Hospital clinics switch
  fastest; give them the outreach."
* **Licensed wrong basis.** The pharmacy committee's charter records that the state regulator's biosimilar report compares plans on gross
  claims savings and will see that basis.

## 8. Determinism by construction

* **Clustering.** Every hospital clinic's switches on a molecule fall either within one seven-day window (90% or more of its patients) or
  scattered, never between, so any cluster rule from 70% to 95% returns the same 348.
* **Rebate shares.** Each product's share is within one point of its annual level in every quarter, so quarterly, annual and rolling
  shares rank the biologics identically.
* **Members.** Pools of 2,000, 900, 700, 1,100, 600 and 600 members are exact under the 90-day rule, and no member holds two references.
* **Fill boundary.** B4 ($12,728 a contact) beats B6 ($10,960) by 1.16× for the last 800 contacts.
* **Rounding.** $20,598,400 sits $48,400 from the nearest $100,000 rounding boundary.

## 9. Prompt sketch and deliverables

> Our two pharmacists can make 1,500 biosimilar outreach contacts this year across the six biologics, and our pharmacy director thinks the
> highest list prices are where they pay off. Tell me how many contacts go to each biologic and how much drug spend that avoids this year, to
> the nearest $100,000, in a form I can take to the pharmacy committee. Send `outreach_allocation.xlsx`, a chart `saving_per_contact.png`,
> and a one-page `pharmacy_committee_note.pdf`.

* `outreach_allocation.xlsx`: the six biologics under the four rung bases, the fill, the prior-authorisation sheet (ask A) and the
  prescriber sheet (ask B).
* `saving_per_contact.png`: for each biologic, gross and net saving per contact as paired horizontal bars, a vertical line where the 1,500
  contacts run out, each bar labelled with its benefit channel and rebate share, and the chosen allocation highlighted.
* `pharmacy_committee_note.pdf`: the committed allocation, the spend avoided and the basis the regulator's report uses.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each biologic, the median days last year from a new prescription to its prior-authorisation
  approval, and the share pended at least once. *Device:* a pended request keeps its request ID and adds a status row, and the approval date
  is the final status row, per the authorisation guide. Taking the first row understates the wait by six days for the three biologics
  under step therapy.
* **Ask B (device-carried).** For each biologic, the number of distinct prescribers last year and the share of members whose prescriber
  changed. *Device:* the provider file issues a new record ID when a prescriber moves practice, and one prescriber is one NPI, per the
  provider data guide. Counting record IDs overstates prescribers by 12%.
* **Ask C (validity).** Each biologic's saving per contact under each of the four rung bases, and the pilot's reproduction: 660 switches
  counted, 312 settled, and the gross formula's 312 of 312.
* **Decoupling.** Clearing the rebate netting changes no figure in asks A or B, and neither touches claims, members or rebates.

## 11. Rubric arithmetic

6 biologics × 2 (ask A) + 6 × 2 (ask B) + 6 × 4 bases + 3 pilot figures (ask C) + 6 contact counts, the spend avoided and the fill-boundary
margin + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Annual cost per member, reference now / biosimilar / rebate share / members: B1 $42,000 (pilot file $118,000) / $14,000 / 20% / 2,000;
  B2 $145,000 / $72,000 / 35% / 900; B3 $52,000 / $12,000 / none / 700 (10% hospital clinics); B4 $126,000 / $40,000 / none / 1,100 (90%
  hospital clinics); B5 $44,000 / $10,000 / 45% / 600; B6 $44,000 / $10,000 / 15% / 600. Plan-wide rebates are 15% of gross pharmacy
  spend.
* Yields: reported 55%; outreach-driven 40% in offices and 12% in hospital clinics.
* Rung leaders B1, B4, B2 and B3 with margins of 1.21×, 1.18×, 1.96× and 1.17×. Both half-netted rebates name B2 (1.38× and 1.28×), and
  all eight grid cells name as stated.
* Insulins I-1 and I-2, switched by the PBM two years ago, are identical on every claims column; their net savings per switch were $960
  and $1,860, at rebates of 40% and 15%.
* Authorisation status rows and provider record IDs never touch claims, members or rebate statements.
