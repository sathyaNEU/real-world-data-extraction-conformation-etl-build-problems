# AD12 — How many significant attack campaigns the annual regulatory return states, when the detectors record alarm episodes on prefixes and the rules count campaigns against customers

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · network security operations |
| Mirrors | Counting incidents at the unit a regulator or service agreement defines when monitoring fires per resource (security-incident reporting at cloud providers, outage counts for service credits where one incident raises thousands of alarms, integrity-incident counts at Meta) |
| Decision shape | One figure committed at a date: the FY2026 count of significant attack campaigns in the return due to the communications regulator on 31 October 2026 |
| Committed call | Significant attack campaigns, April 2025 to March 2026, as a whole number |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the unit the decision counts is not stored (E02), pinned by the published control set, with a sampling rate validated on one link and applied to another at the lower rung (E17) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #13 validates on one population, applies to another · #1 reports a failed back-test, ships anyway |
| Calibration form | Published control set with a reproduction clause: the eight quarterly counts and 24 sector cells published in the FY2024 and FY2025 returns, which any count method must reproduce |
| Driving force | The rules count campaigns against customers, and the detectors record alarm episodes against prefixes. Building a campaign means mapping each alarm's destination to the customer holding that address on that day, through the address plan's dated assignment history, and merging a customer's alarms while they recur. That collapses floods spread across many prefixes and turns pulse-wave attacks, each burst too short to count, into campaigns long enough to be significant, so the count rises. Only that construction reproduces the published returns. |

## 1. Situation

A transit provider's security operations team files an annual return with the communications regulator, due 31 October, stating the
number of significant attack campaigns in the financial year. The rules define a campaign as a continuing attack on one customer, and a
significant one as a campaign that peaked at 10 Gbps or lasted 60 minutes or more. The team's guidance says the method used for a return
must reproduce every count published in the two previous returns. The pack carries both detector feeds' alarm episodes for FY2024 to FY2026,
the sampled flow records, both links' interface counters, the address plan's current assignments and assignment history, and the two
published returns.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each alarm, each flow, each interface counter, each assignment and both published returns. The SOC
  manager's alarm episodes are real alarm episodes. Nothing reported is overturned; the difficulty is that the unit the return counts exists
  in no file.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. Counting significant alarm episodes after collapsing the duplicate feed and scaling each link's flows
  correctly, the natural complete pipeline, still lands 16.6% low.
* **Instrument repair.** Make the detectors perfect; they already are. A better detector still alarms per destination prefix per minute,
  and no detector knows which customer held an address that day or where one campaign ends.
* **Lens swap.** The naive count is of alarm episodes on prefixes; the answer counts campaigns against customers, a different population of
  objects built from many episodes, with its own significance test.

## 3. The driving force

A strong solver counts significant alarm episodes, notices the regional link acquired last year samples its flows at 1 in 250 rather than
the main link's 1 in 1,000 and rescales it, collapses the duplicate episodes the redundant detector pair records, and reaches a clean 610
that every check it writes passes. It is counting rows. A campaign is an attack on a customer: a flood that hit 14 of one customer's
prefixes at once is one campaign, and a pulse-wave attack of 8-minute bursts against one customer over six hours is one campaign that lasted
six hours, though no single burst lasted ten minutes or reached 10 Gbps. Building campaigns needs the customer that held each destination
address on the day of the alarm, from the address plan's dated history, because 9% of attacked prefixes changed hands in the year. It then
needs a customer's alarms merged while they recur, and significance tested on the campaign. Floods collapse by 94; pulse waves add 215.
Nothing in the pack builds campaigns, and only campaigns reproduce the published returns.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Significant alarm episodes per destination prefix, both detector feeds, every flow scaled by the main link's 1 in 1,000 | 1,108, +51.6% | The detector output as recorded, scaled by the collector guide's rate | The regional link's interface counters: scaling its flows by 1,000 reproduces four times its measured bytes, because its routers sample 1 in 250 |
| 1 | Each link's flows scaled by its own sampling rate | 842, +15.2% | A rate validated against the main link's counters, now calibrated per link | The detector guide: the redundant pair records every episode twice with identical start minutes |
| 2 | Hygiene: duplicate episodes collapsed | 610, −16.6% | Clean, correctly scaled and deduplicated; every control total on the alarm side ties | The published returns: episode counts reproduce none of the eight published quarters and run 17% under their total |
| 3 | **Decisive:** each alarm mapped to the customer holding its address that day, a customer's alarms merged while they recur, significance tested on the campaign | **731** | — | — |

* **Figure shape.** The two corrections walk the figure down; the decisive move reverses them. Per-rung offsets are +51.6%, +15.2% and
  −16.6%, and the answer sits between the early stops and the late one, so the two failure directions lie on opposite sides.
* **Partial correction priced (L3).** A solver who builds campaigns from the address plan's current assignments lands at 655 (−10.4%),
  because alarms on the 9% of prefixes that changed hands are credited to their present holders. A solver who builds campaigns but tests
  significance on each episode before merging keeps the floods' collapse and loses the pulse waves, landing at 516 (−29.4%).
* **Grid.** Sampling rate (one or per link) × duplicates (kept or collapsed) × unit (prefix episode, prefix campaign, customer campaign on
  current assignments, customer campaign on dated assignments) × significance (episode or campaign) gives the cells. Every cell with one
  rate or duplicates kept sits at least 23.8% above; prefix-level campaigns land at 580 (−20.7%). The nearest wrong cell is current
  assignments at −10.4%, and it needs the dated history left unread.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules define a campaign in words, as a continuing attack on one customer. No document says how alarms become
   campaigns, where one ends, or that an address's customer is the one holding it on the day.
2. **The corpus pins a construction, not a menu.** Customer campaigns on dated assignments reproduce all 8 published quarters and all 24
   sector cells exactly; current assignments reproduce 5 of 8 quarters, prefix-level campaigns 2, episodes none, and episodes miss in one
   direction (under) every quarter. The unit is a construction: a campaign exists only after a dated join to the address history and a
   time-ordered merge within customer, and no file stores one.
3. **No arithmetic symptom.** Episodes tie to the detector logs, flows tie to interface counters once scaled per link, and the address plan's
   history is complete; every episode belongs to exactly one campaign.
4. **Not a row predicate.** It needs a dated join from destination address to customer, an ordering of each customer's alarms in time, a
   merge across gaps, and a campaign-level peak and duration.
5. **The enumeration is arithmetic.** Within a campaign a customer's alarms recur within 8 hours; between campaigns no customer is attacked
   again within 3 days, so every merge gap from 9 to 70 hours builds the same campaigns.
6. **No cutover date.** Floods and pulse waves run through all three years; the only dated event, the regional link's acquisition, sits in
   the rung below.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The FY2024 and FY2025 returns as published: significant campaigns in each of the eight quarters, and by customer sector (12
  sectors, 24 cells). The guidance makes exact reproduction of every published count the condition of using a method.
* **What it pins.** Per-link scaling, collapsed duplicates, dated customer campaigns and campaign-level significance reproduce all 32
  published figures. Episode counts reproduce no quarter and fall 17% short of the two years' total.
* **Twin pair.** FY2025 Q2 and FY2025 Q4 are identical on every alarm-side column: significant episodes (142), prefixes attacked, attack
  minutes and peak distribution. The published counts are 61 and 30 (2.03×): Q2's episodes were pulse waves against few customers, merging
  into long campaigns; Q4's were floods across many prefixes of few customers, collapsing.
* **Every rule exercised.** One FY2024 quarter holds a campaign spanning a prefix's change of holder, so the dated join is tested; one sector
  cell holds a campaign whose bursts never reach 10 Gbps but last seven hours, so campaign-level significance is tested.
* **Resemblance points at the decoy.** FY2026's episode profile most resembles FY2025 Q4's, the quarter whose campaigns collapsed most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The rules: a campaign is a continuing attack on one customer; a significant campaign peaked at 10 Gbps or lasted 60
  minutes or more. The team's guidance: a return's method reproduces every count published in the two previous returns. The address plan's
  documentation: an assignment history records every change of holder with its effective date.
* **Empirical pins.** The merge gap and campaign-level significance, from the published returns.
* **Voices.** The SOC manager: "Every alarm episode is its own attack as far as the pager is concerned." The head of network security: "The
  acquired network's routers are the same kit as ours."
* **Licensed wrong basis.** The rules note that the industry association's benchmark counts attack events per targeted prefix and will
  publish members' figures on that basis.

## 8. Determinism by construction

* **Merge gap.** The empty band from 8 hours to 3 days makes the gap immaterial.
* **Assignment.** Every change of holder takes effect at midnight and no alarm falls within an hour of one, so day-level and minute-level
  joins agree.
* **Duplicates.** The two feeds record identical start minutes, so collapsing is an exact key match.
* **Sampling.** Each link's rate is fixed for the year, and per-link scaling reproduces its interface counters within 0.4%.
* **Year.** Campaigns are dated by first alarm; none straddles 1 April at either end of the year.

## 9. Prompt sketch and deliverables

> The regulator's annual return is due on 31 October and has to state how many significant attack campaigns we had in FY2026. Our SOC
> manager treats every alarm episode as its own attack. Give me the number for the return, as a whole number, with `regulator_return.xlsx`
> holding the sheets below, the chart `campaign_build.png`, and a one-page `return_cover_note.pdf`.

* `regulator_return.xlsx` — the campaign build by quarter and sector, the notification sheet (ask A), the scrubbing sheet (ask B) and the
  reproduction table (ask C).
* `campaign_build.png` — a waterfall from FY2026's raw episodes to the filed count (rescaling, duplicates, floods collapsed, pulse waves
  merged), with the published FY2025 quarters plotted against each construction as an inset and the twin quarters labelled.
* `return_cover_note.pdf` — the committed count and how it reconciles to the episodes the SOC sees.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 customer sectors, customers sent a mitigation notice in FY2026 and the median
  minutes from first alarm to notice. *Device:* a notice to a parent account covers every subsidiary account beneath it, as the notification
  policy states, and the notice log records only the parent. Counting notified accounts from the log misses subsidiaries in four sectors.
  The campaign build never reads the notice log.
* **Ask B (device-carried).** For each month of FY2026, cleaned traffic the scrubbing centre returned, in terabytes. *Device:* the centre's
  report counts returned bytes inside the GRE tunnels with encapsulation overhead included, per its reporting note. Reading the report as
  customer traffic overstates every month by the overhead share of its packet mix.
* **Ask C (validity).** For each of the four rung constructions, the published quarterly counts it reproduces out of 8.
* **Decoupling.** Clearing the campaign construction changes no figure in asks A or B.

## 11. Rubric arithmetic

12 sectors × 2 (ask A) + 12 months (ask B) + 4 constructions (ask C) + the committed count, the floods collapsed and the pulse-wave
campaigns added + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Rung figures are 1,108 / 842 / 610 / 731. Every grid cell sits at least 10.4% from the answer; the episode-significance partial lands at
  516.
* Campaign construction removes 94 by collapsing floods and adds 215 pulse-wave campaigns; 9% of attacked prefixes changed holder in the
  year, none within an hour of an alarm.
* The regional link samples 1 in 250 all year; the main link 1 in 1,000.
* FY2025 Q2 and Q4 are identical on every alarm-side column; their published counts are 61 and 30.
* Notices to parent accounts and GRE overhead never touch the alarm feeds, the flows or the address plan.
