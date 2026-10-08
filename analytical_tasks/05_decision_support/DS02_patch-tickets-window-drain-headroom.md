# DS02 — How to split 300 patch tickets across six production estates, when payments can only drain four hosts at a time

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · platform security operations |
| Mirrors | Remediation capacity allocated on risk while the estate's own change capacity binds (Google and Meta fleet patching under drain budgets, AWS and Azure maintenance windows that must keep N+1 at peak, payment-platform change freezes) |
| Decision shape | An allocation under a cap: next month's 300 change tickets across six estates |
| Committed call | Tickets per estate, and the exploitable host exposures the split takes out next month, to the nearest ten |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · measured #10's architecture (a limit in an operational register, applied in the figure), with Pattern B for the per-window headroom rule the acknowledgements pin and finer controls (#12) at rung 2 |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #10 notes a binding limit as a risk · #12 stops at the first control that passes · #2 counts file rows instead of the real unit · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the hosting provider's acknowledgements of 412 change requests over six months, each accepted, part-accepted or declined against a window |
| Driving force | The cap counts tickets. What payments and checkout can absorb is counted in host drains per maintenance window, and a window may drain only what keeps the estate one rack above the forecast peak of that window's own hours. Payments' windows sit on its evening peak, so it can drain four hosts at a time, 96 reboots next month, enough for five package updates. No file states that number. It is built from the capacity register, the hourly forecast and the window calendar, and only that construction reproduces all 412 of the provider's acknowledgements. |

## 1. Situation

A cloud platform's vulnerability office gets 300 change tickets a month from the patch crews. A ticket is one package update on one
estate, and it fixes every CVE in that package on every host carrying it. Next month the office allocates tickets on exploitable
exposure for the first time, replacing the old even spread by CVSS band. Six estates compete: payments, checkout, search, media, internal
tools and the data pipeline. Payments and checkout run in a colocation the hosting provider operates, and the provider schedules their
drains. The CISO wants the bulk of the tickets on payments, where the worst exposure sits.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the scanner results, the exploitability
  scores, the CMDB, the office's close-out, the drain tool's parallelism setting and the provider's acknowledgements. The CISO
  is right that payments holds the most exploitable exposure. The difficulty is that a ticket counts against the cap but completes only
  if its hosts can be drained inside a window, and nobody counts that.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CISO's view and the close-out. Ranking package updates by exploitable exposure still sends 88 tickets to
  payments, and nothing in the ticket data fails.
* **Instrument repair.** The suspect file is the CMDB, which still lists retired hosts beside their re-imaged successors. Resolved, rung 0
  lands on rung 1's 7,630 (+89%), and rungs 1 and 2 stay at 7,630 and 6,690. The scanner's exploit flag and the drain tool's parallelism
  setting are correct records of other attributes (a public exploit, a tool limit), and no file records drains per window, so rung 2's
  6,690 stands and the answer still needs the drains built from the register, the forecast and the calendar.
* **Lens swap.** The naive figure is exposure on the tickets cut. The answer is exposure on the tickets that can complete inside next
  month's windows: a different set of tickets in a forward month, not the same plan read another way.

## 3. The driving force

A strong solver deduplicates the host records, recovers the exploitability rule the close-out pins and fills the cap greedily with the
richest package updates. Each step is competent, and payments and checkout take 198 tickets. The drain tool's parallelism setting (48 and
60 hosts at once, a tool limit) says those tickets fit, and so does any headroom read at average load. Neither is the rule the provider
applies. The SRE standard keeps every estate one failure domain (a rack of 40 hosts) above the forecast peak during maintenance. Payments'
windows fall on its evening peak, which leaves 44 hosts of headroom and so four concurrent drains. At eight drain cycles per window and
three windows, that is 96 reboots. Checkout gets 120. With 2.4 and 2.0 exploitable exposures per reboot, the two estates can take out 470
exposures between them, five and six tickets' worth. Every further ticket sent there completes in a later month. The constrained split
moves 187 tickets to search, media, tools and the data pipeline.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Fill 300 tickets by exploitable host exposure, using the scanner's exploit-available flag and raw CMDB host records | 8,250 (+104%); payments 66, checkout 100 | The office's own data, ranked on its own objective | The re-image link table: media and the data pipeline still list retired records for half their fleets |
| 1 | Hygiene: retired records resolved through the re-image links | 7,630 (+89%); payments 81, checkout 120 | Clean hosts, every count reconciles to the capacity register's host totals | The close-out's per-estate and per-month figures: the flag matches the quarter total and only 2 of the 6 estate figures |
| 2 | Exploitability as the close-out pins it, EPSS of at least 0.10 on the day the ticket is cut (#12) | 6,690 (+65%); payments 88, checkout 110 | Reproduces all nine close-out figures, and the drain tool's parallelism setting says the plan fits | The acknowledgements: only per-window forecast-peak headroom reproduces all 412 requests, and it gives payments 96 reboots next month |
| 3 | **Decisive:** drains per window from the capacity register, the hourly forecast and the window calendar; fill each estate's reboots, then re-spend the cap | **4,050; payments 5, checkout 6, search 71, media 102, tools 31, data pipeline 85** | — | — |

* **Figure shape.** Every correction walks the figure down, by 7.5%, 12.3% and then 39.5%. The answer is bracketed. Every under-corrected
  cell lands at least 13.5% above. The half-insight below lands 49.8% low on rung 2's split.
* **Partial correction priced (L3).** A solver who checks the limit against the tool's parallelism setting or against headroom at average load finds
  slack and keeps rung 2's split and figure unchanged (#10). A solver who applies the true limit as a haircut and does not re-spend the
  freed tickets keeps all six of rung 2's ticket counts and reports 2,030 (−49.8%).
* **Grid.** Exploitability (flag, cut-day EPSS) × host records (raw, resolved) × limit (none or a slack reading, per-window
  re-optimised, per-window haircut) gives 12 cells. The nearest wrong cell is 13.5% above (flag, resolved, re-optimised) and costs one
  error, the flag that the close-out's estate figures refuse. The nearest below is 13.4% (flag, raw, haircut) and costs three.
* **Why the split flips.** Payments' best package update carries 2.8× the exposure of search's best (50 against 18). After its 96 reboots,
  payments' marginal exposure per ticket next month is zero, against at least 9 in every receiving estate.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The SRE standard states the N+1-at-peak principle for maintenance in general. No document converts it into drains
   per window or links it to the ticket cap, and the only concurrency figure in the pack is the drain tool's parallelism setting, which is slack.
2. **No sweepable corpus nominates it.** The acknowledgements pin the rule as a construction. Per-window forecast-peak headroom reproduces
   412 of 412. The best rival, the tool's parallelism setting, reproduces 351, and average-load headroom 318. Every rival miss accepts what the provider
   declined. *In every month of the file the office's tickets to payments and checkout stayed under 14, because tickets were spread by CVSS
   band, so no office ticket was ever declined.* The file's 31 declines all sit on other teams' requests.
3. **No arithmetic symptom.** Tickets sum to 300, host records reconcile to the register, exposures tie to the scanner, and the tool's
   parallelism setting reports slack.
4. **Not a row predicate.** Drains per window need the window's hours joined to the hourly forecast, the peak taken over those hours, the
   rack reserve subtracted and the result multiplied by drain cycles. A per-estate allocation is then re-optimised against the shared cap.
5. **The enumeration is arithmetic.** Which tickets complete is computed from reboots per estate. No column flags a ticket as unabsorbable.
6. **No cutover date.** Payments' evening peak recurs every day, and the limit has always existed. It binds now because the allocation
   rule changed, and no outcome series steps.
7. **Survives deletion.** No wrong number exists to delete, and the tool's parallelism setting still reports slack.

## 6. The calibration corpus

* **Form.** The provider's acknowledgements: 412 change requests over six months for the two colocated estates. Each carries the hosts
  requested, the window, the hosts accepted and any deferral or decline reason.
* **What it pins.** A request is accepted up to the drains that keep the estate one rack above the forecast peak of the window's hours,
  counting drains already accepted in the window. 412 of 412 under that rule, against 351, 318 and 296 for the tool's setting, average-load
  headroom and a flat 10% of hosts.
* **What it is blind to.** Payments flooded with office tickets (above): it never happened.
* **Twin pair.** Two payments requests are identical on every column: 8 hosts, a Tuesday 20:00–24:00 window, the same tool setting, the same
  month and the same submitting team. The provider accepted 8 of one and 4 of the other, 2× apart. The second window held the month-end
  settlement peak (91% forecast utilisation against 84%), and only per-window forecast headroom separates them.
* **Every rule exercised.** Thirty-eight requests landed in windows that already held accepted drains, which tests the "together with" clause.
  Nineteen windows spanned an hour boundary where the forecast rose, which tests the peak over the window's hours.
* **Resemblance points at the decoy.** Payments' acknowledgement history (accepted almost everywhere) looks like the estates with slack.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The vulnerability standard: tickets go where they take out the most exploitable exposure. The SRE standard: maintenance
  never takes an estate below one failure domain of headroom at its forecast peak. The runbook: one drain cycle is 30 minutes. One
  sentence each, in three documents.
* **Empirical pins.** The exploitability rule, from the close-out's nine figures. The headroom rule, from the acknowledgements.
* **Voices.** The CISO: "Payments carries our worst exposure; that's where the tickets go." The SRE lead: "Our windows have always taken what
  the office sent." The office manager: "A ticket we cut is exposure we've dealt with."
* **Licensed wrong basis.** The vulnerability standard records that the audit committee reads the plan as exposure ticketed and will see that
  table.

## 8. Determinism by construction

* **Drain arithmetic.** Rack size (40 hosts), window lengths and the 30-minute cycle are filed. Forecast peaks fall mid-hour bin, so hourly
  or quarter-hourly maxima give the same four and five concurrent drains.
* **Reboot sharing.** A host carrying several ticketed packages is drained once per window. Exposures per reboot (2.4, 2.0) are computed from
  the scanner join, and drain order inside the cap does not change the total.
* **Exploitability.** The cut-day EPSS rule reproduces all nine close-out figures. Thresholds of 0.08 to 0.12 give the same split, because
  no package update's EPSS falls in that band.
* **Integer tickets.** The cap is filled exactly. The marginal ticket in each receiving estate beats the next candidate by at least 0.6
  exposures, so tie conventions cannot move a ticket.

## 9. Prompt sketch and deliverables

> Our patch crews take 300 change tickets next month and I have to split them across the six production estates by Friday. The CISO wants
> the bulk on payments, where our worst exposure sits. Give me the split, estate by estate, and how many exploitable host exposures it
> takes out, to the nearest ten. Send `ticket_split.xlsx`, a chart `exposure_removed.png`, and a one-page `patch_plan.docx`.

* `ticket_split.xlsx` — the split and its build, the deployment sheet (ask A), the perimeter sheet (ask B) and the basis sheet (ask C).
* `exposure_removed.png` — paired bars per estate (exposure on tickets cut, exposure completable next month), each estate's reboot capacity
  as a marker, the 300-ticket split annotated on the axis, and a title stating the finding.
* `patch_plan.docx` — the committed split, its figure, and why payments gets five tickets.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six estates, the median and 90th-percentile days from a vendor's package release
  to its deployment over the last two quarters. *Device:* a rollback re-deploys the prior version as a new deployment row carrying a
  `rollback_of` reference, as the deployment log's dictionary documents. Counting rollbacks as deployments shortens the median in media and
  checkout by four to six days.
* **Ask B (device-carried).** For each estate, the distinct internet-facing services on last month's perimeter scan. *Device:* the scan
  records IP and port, and services published on both IPv4 and IPv6 virtual IPs appear twice. The load-balancer pool table maps both to one
  service, and counting rows overstates four estates by 30–45%.
* **Ask C (validity).** The close-out's nine figures under each of three exploitability rules (hits of nine), and the six-estate split under
  each rung's construction.
* **Decoupling.** Clearing the drain limit changes no figure in asks A or B. Deployment rows and perimeter records never enter the split.

## 11. Rubric arithmetic

6 estates × 2 (ask A) + 6 services counts (ask B) + 3 hit counts + 4 constructions × 6 estates (ask C) + the committed split (6 counts) and
its figure + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Payments: 1,400 hosts, evening-peak windows leaving 44 hosts of headroom, rack of 40, three 4-hour windows, so 96 reboots. Checkout:
  four 3-hour windows at five concurrent drains, so 120 reboots. Exposures per reboot are 2.4 and 2.0. The tool's parallelism setting is 48 and 60,
  and average-load headroom exceeds 700 hosts.
* Rung figures 8,250 / 7,630 / 6,690 / 4,050. The haircut cell is 2,030 on rung 2's split. Every cell of the 12-cell grid sits at least
  13.4% from the answer.
* Media and the data pipeline re-imaged about half their fleets in the last 30 days, so retired records inflate their exposure by 1.5×.
  The scanner flag inflates checkout by 1.25× and search by 1.35×, and matches the close-out's quarter total exactly.
* The acknowledgement file: 412 requests, 31 declines and 26 part-acceptances, none of them on office tickets. The twin requests are
  identical on every column.
* Rollback rows and perimeter records never touch scanner results, CMDB records, tickets or drains.
