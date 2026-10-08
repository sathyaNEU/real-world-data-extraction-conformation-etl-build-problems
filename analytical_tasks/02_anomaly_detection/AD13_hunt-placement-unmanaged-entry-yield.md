# AD13 — Which university division gets the two-week threat hunt, when hunts find footholds only behind movement that came in from devices nobody manages

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · university information security |
| Mirrors | Sending a scarce hunt or audit where it will find something, when its yield depends on how the activity entered rather than how much of it there was (threat hunts in Google and Microsoft enterprise tenants with unmanaged-device access, fraud sweeps at payment companies split by onboarding channel, abuse investigations at marketplaces split by account origin) |
| Decision shape | Which of N gets one scarce thing: the external hunt team's single two-week engagement next term |
| Committed call | The one division the hunt team works in |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · conditioned yield (E05): past hunts found footholds only behind lateral movement that entered through sessions from unmanaged devices, a property reached through the VPN log; the confirmed rate with suppressed cells recovered from published margins, and a tie the scorecard's rounding saturates (E21), at the lower rungs |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #7 uses the ready-made measure · #13 validates on one population, applies to another · #19 breaks a big tie instead of questioning it |
| Calibration form | Counterparty acknowledgement file: the incident-response provider's line-level acknowledgements for six divisions, its quarterly matrix for all eight, and its acknowledged findings from the 14 hunts it ran across the consortium's universities in the last two years |
| Driving force | The policy sends the hunt where it is expected to find the most attacker footholds, and every careful reading ranks divisions on confirmed lateral movement, which puts Treasury on top once its suppressed cells are recovered. The provider's own hunt reports say where footholds are: behind movement that entered through a session from an unmanaged device, 0.62 per such confirmed case, and nowhere else, because managed endpoints clean what lands on them. Joining each confirmed case to the VPN session it came through gives the Library 8.1 expected footholds; Treasury, which admits managed devices only, has at most 0.6. |

## 1. Situation

A university's central security office can bring an external threat-hunting team in for two weeks next term, and the team works in one
division. The security policy sends the hunt where it is expected to find the most attacker footholds; the SOC's guidance note ranks
divisions for hunts on confirmed lateral movement per 1,000 accounts over the last two quarters. The SOC's detector raises alerts;
escalations go to the outsourced incident-response provider, which confirms or closes them, line by line for six divisions and, for the
two privacy-restricted divisions, Treasury and Human Resources, only as a quarterly matrix of rates by division, functional group and
campus. The pack carries the alerts and escalations, the SOC's scorecard and triage log, the directory's account counts, the VPN session
log, the network access register, the criticality register and the provider's file, including its acknowledged hunt findings.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the alerts, the scorecard, the triage log, every acknowledgement and printed cell, every VPN
  session's device posture and every past hunt finding. Treasury's confirmed rate really is the university's highest. Nothing reported is
  overturned and no stakeholder read is corrected; the difficulty is that the hunt's yield depends on how movement entered, not on how much
  there was.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the guidance note. Ranking divisions on confirmed lateral movement, the natural reading of
  where attackers are, still names Treasury once its cells are recovered.
* **Instrument repair.** Suspect file: the provider's matrix, which prints cells of one to four cases as "<5". Printed in full, rung 2's
  recovery becomes a lookup and still names Treasury, and rungs 0 and 1 are unchanged; the conditioned yield is still needed. No file claims
  to record where a hunt will find footholds, and the VPN log records every session's device posture.
* **Lens swap.** The naive population is every confirmed case; the answer's is the cases that entered through unmanaged-device sessions, a
  different population of cases, 87% of the Library's and at most one of Treasury's eight.

## 3. The driving force

A strong solver distrusts raw alert volume, sees through the scorecard's rounded 100% shares to the triage log's exact counts, and moves
to the provider's confirmations, the guidance note's basis. Treasury's and Human Resources' cells are printed "<5", but each restricted
division is the only blank on its campus, so the solver recovers them from the campus margins at the matrix's convention: Treasury had 8
cases on 900 accounts, 8.89 per 1,000, the university's highest. Each step is competent. But the policy asks where the hunt will find
footholds, and the provider has hunted fourteen times. Its findings sit behind one kind of movement only: movement that entered through a
VPN session from an unmanaged device, where the attacker's first foothold is a personal laptop no endpoint agent sees, so persistence is
planted on the first university host it reaches. Movement that starts on a managed endpoint is cleaned there. Joining each confirmed case
to the VPN session its source account held at the time gives the conditioning property. The Library's part-time staff and student
assistants work from their own laptops: 13 of its 15 cases came in that way, 8.1 expected footholds. Treasury's network admits managed
devices only, apart from one auditors' jump host, so its footholds are bounded by its one unmanaged-source escalation.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lateral-movement alerts per 1,000 accounts, last two quarters | A, Research Computing (70.0; 1.33× C) | The SOC's detector, normalised for size | The provider's acknowledgements: 71% of A's escalations were closed as administrator activity |
| 1 | The scorecard's triage true-positive share, printed to the whole percent; four divisions at 100%; the policy's tie-break (criticality tier, then accounts) | B, Estates (tier 1, 6,200 accounts against F's 400) | An outcome measure, the documented tie-break applied | The triage log: under the policy's rule that a figure is the lowest value consistent with every file of record, B's printed 100% is 199 of 200, and only F's 16 of 16 is exact |
| 2 | The guidance note's basis: confirmed lateral movement per 1,000 accounts, the restricted cells recovered from the campus margins at the matrix's convention | D, Treasury (8.89; 1.19× F) | The provider's own confirmations, nothing invented for the blanks, the note's basis exactly | The provider's hunt reports: across 14 hunts, footholds were found only behind movement that entered through unmanaged-device sessions, 0.62 per such case, and none behind any other |
| 3 | **Decisive:** expected footholds, 0.62 for each confirmed case whose source session (VPN log, at the case's time) was on an unmanaged device; the restricted divisions bounded by their unmanaged-source escalations | **E, Library and Learning Services (8.1)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (41.2), 8th on rung 1 (83%) and 5th on rung 2 (4.41), and leads only rung 3, 1.63× H, Student
  Services (5.0). Intermediate leaders hold margins of 1.33×, the tie-break's tier and accounts, and 1.19×.
* **Discriminator dominance.** Treasury carries a 2.01× advantage over E into rung 3 (8.89 against 4.41 per 1,000). The conditioned yield
  turns E's rate into 8.1 footholds (×1.83) and Treasury's into at most 0.62 (×0.07), an edge of 26 against the 1.2 × 2.01 = 2.42
  required, 10.8× headroom.
* **Partial correction priced (L3).** A solver who applies the hunts' pooled yield, 0.21 footholds per confirmed case, names A (6.5 against
  B's 4.6, 1.41×; E 3.2), because A has the most cases. A solver who reads posture from the device inventory's current enrolment, after
  September's drive brought the Library's laptops under management, cuts E to 1.9 and names H (5.0 against A's 4.3). A solver who
  conditions correctly but ranks footholds per 1,000 accounts names H (3.1 against E's 2.4, 1.31×). No half lands on E.
* **Grid.** Basis (alerts, triage share, confirmed rate, pooled yield, conditioned yield) × posture source (none, current inventory, VPN
  session) × scale (count or per 1,000) gives the cells: alerts name A, triage B, confirmed rates Treasury, pooled yields A, every
  current-inventory cell H, and the per-1,000 conditioned cell H. Only the session-conditioned count names E, and the nearest wrong cell
  (H) needs only the per-1,000 scale.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy names footholds; the guidance note names confirmed rates. Nothing says a hunt's yield depends on how
   movement entered, and the hunt reports list findings, not their cause.
2. **The corpus pins a construction, not a menu.** The session-conditioned yield reproduces the footholds of 14 of 14 hunts within one;
   the pooled yield reproduces 5, the confirmed rate's ranking 4, and both rivals miss every hunt with a skewed entry mix in the direction
   of its mix. The property is a construction: a case's source account, matched to the VPN session it held at the case's time, and that
   session's posture, with no column on the case carrying it.
3. **No arithmetic symptom.** Cases tie to the matrix and the line-level file, sessions to the VPN concentrator's counts, hunts to their
   reports; every rung reconciles.
4. **Not a row predicate.** It needs each confirmed case joined to a time-bounded VPN session, a posture per session, a yield per class from
   the hunt corpus, and a bound from escalations where cases are restricted.
5. **The enumeration is arithmetic.** Expected footholds per division are computed; no field carries them.
6. **No cutover date.** Unmanaged access runs through both quarters; the only dated event, September's enrolment drive, sits under a
   partial reading.
7. **Survives deletion.** With every voice and the guidance note removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The provider's file: line-level acknowledgements for the six unrestricted divisions, the quarterly matrix for all eight with
  "<5" for cells of one to four cases, and its acknowledged findings from 14 hunts across the consortium's universities, each with the
  hunted division's confirmed cases and their source sessions.
* **What it pins.** Footholds per confirmed case: 0.62 behind unmanaged-device entry, 0.00 behind managed (14 of 14 hunts within one
  foothold); the matrix's convention, cases over start-of-quarter accounts to two decimals, from the line-level divisions.
* **Twin pair.** Hunts HU-03 and HU-08 are identical on the hunted division's confirmed cases (14), alerts, accounts and triage share.
  HU-03 found 9 footholds and HU-08 4 (2.25×): 80% of HU-03's cases had entered through unmanaged-device sessions and 35% of HU-08's.
* **Every rule exercised.** One hunt was in a division with no unmanaged access and found nothing on 20 confirmed cases; one hunted
  division had re-enrolled devices mid-quarter, so posture at the session, not today's, is tested.
* **Resemblance points at the decoy.** By confirmed rate and alert profile, Treasury most resembles HU-03's division, the corpus's largest
  find.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The security policy: the hunt goes to the division where it is expected to find the most attacker footholds; a figure is
  the lowest value consistent with every file of record; ties go to the higher criticality tier, then to more accounts. The network access
  register: which devices each division's segments admit.
* **Empirical pins.** The yields by entry posture, from the hunt corpus; the matrix's rate convention, from the line-level divisions.
* **Voices.** The SOC lead: "The detector knows where the movement is; send the hunt where it fires hardest." The provider's account
  manager: "Restricted divisions are too small to matter, which is why their cells are suppressed."
* **Licensed wrong basis.** The SOC's guidance note ranks divisions for hunts on confirmed lateral movement per 1,000 accounts, and the
  policy records that the insurer reads hunt placements on that basis.

## 8. Determinism by construction

* **Sessions.** Every confirmed case's source account held exactly one VPN session or none at the case's time; cases with no session
  entered on campus from managed endpoints.
* **Bound.** Treasury's and Human Resources' unmanaged-source escalations (one and none) bound their footholds whatever the provider
  confirmed, and the bound is far below every unrestricted division above them.
* **Window.** The two quarters are filed; either quarter alone keeps E first by at least 1.4×.
* **Yield.** The hunt corpus's split is absolute: no hunt found a foothold behind a managed-entry case.

## 9. Prompt sketch and deliverables

> We can bring the external hunt team in for two weeks next term, and it works in one division. The SOC lead would send it wherever the
> lateral-movement detector fires hardest. Tell me the division, in a line for the security committee, with `hunt_placement.xlsx` holding
> the sheets below, the chart `entry_posture.png`, and a one-page `committee_note.pdf`.

* `hunt_placement.xlsx` — the division build with every recovered cell, each confirmed case's entry posture and the expected footholds, the
  MFA sheet (ask A), the phishing sheet (ask B) and the hunt back-test (ask C).
* `entry_posture.png` — the eight divisions' confirmed cases as bars split by entry posture, expected footholds as markers, Treasury's
  bound drawn as a cap, the 14 hunts' footholds against their unmanaged-entry cases as an inset, and the chosen division highlighted.
* `committee_note.pdf` — the committed division and why the confirmed-rate ranking and its leader are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each division, privileged accounts without multi-factor enrolment at quarter end, as a count
  and as a share of its people with privileged access. *Device:* the directory lists a person's standard and administrative accounts
  separately, linked by an owner ID, as its schema documents. Counting accounts as people overstates the share in the three divisions where
  administrators hold several accounts. The hunt placement uses account counts only as the matrix's denominators.
* **Ask B (device-carried).** For each month of the two quarters, phishing emails staff reported and the share the mail team confirmed
  malicious. *Device:* the report button files one report per recipient, and the mail team's log groups a campaign's reports under one
  campaign ID. Counting reports as emails overstates every month with a large campaign.
* **Ask C (validity).** For each of the four rung constructions and the pooled yield, the hunts whose footholds it reproduces within one,
  out of 14.
* **Decoupling.** Clearing the entry-posture split changes no figure in asks A or B.

## 11. Rubric arithmetic

8 divisions × 2 (ask A) + 6 months × 2 (ask B) + 5 constructions (ask C) + the committed division, its expected footholds and the margin
over H + 5 named chart parts + 3 files ≈ 44 criteria.

## 12. World-building constraints

* Accounts: A 9,800, B 6,200, C 3,900, D (Treasury) 900, E (Library) 3,400, F (HR) 400, G (Legal and Compliance) 2,400, H 1,600.
  Half-year confirmed cases: 31, 22, 20, 8, 15, 3, 6, 8; unmanaged-entry cases: 7, 2, 6, at most 1, 13, 0, 3, 8.
* Treasury 4 and 4 cases, HR 2 and 1, all printed "<5"; each is the only blank on its campus (City: A, D; Park: B, E, F).
* Rung leaders are A, B, D, E; E leads rung 3 by 1.63× over H. Pooled yield names A; current enrolment and per-1,000 scaling name H.
* Scorecard: A 300 of 301, B 199 of 200, C 200 of 201 and F 16 of 16 print 100%; B and F are tier 1.
* Hunts HU-03 and HU-08 are identical on every division-level column but their entry mix.
* Owner-linked accounts and campaign-grouped phishing reports never touch the cases, the sessions or the hunt findings.
