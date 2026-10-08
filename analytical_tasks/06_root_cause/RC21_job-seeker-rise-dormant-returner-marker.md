# RC21 — Which cause of the rise in active job-seekers gets the professional network's product bet, when most seekers never say why they are looking

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · two-sided marketplace supply and demand |
| Mirrors | Supply-side diagnostics at job and professional platforms (LinkedIn, Indeed, Upwork), where the rise in active seekers is attributed by an optional self-reported reason that the largest group almost never fills in |
| Decision shape | Which of N root causes gets the fix: the year's one product bet on the job-seeker side |
| Committed call | The cause the bet targets, and the share of the year's rise in active job-seekers it accounts for, in thousands of members |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E19 (a latent attribution marker: dormant accounts reactivated before the open-to-work switch), pinned by settled partner lists, with E33 (the population a flag suggests: open-to-work flags against the dated active-seeker rule) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #17 guesses an attribution the data can settle · #5 takes the population a flag or filter suggests · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: six partnership launches in the product change log, each with its partner's member list and their timelines before and after |
| Driving force | The reason a member is looking is an optional field; laid-off members fill it in more than half the time and people returning from a career break one time in twenty. Read through the field, the rise looks like layoffs, then a hiring freeze. Returners leave a consistent trace instead: an account dormant for a year or more, reactivated, with a profile update and the open-to-work switch inside thirty days. That trace reproduces every member on the returnship partners' lists and assigns 470,000 of the rise to them. |

## 1. Situation

A professional network's active job-seekers rose by 1.20 million members this year, from 4.8 million to 6.0 million. The recruiting-products team says
a layoff wave is under way; the research lead says job-finding has collapsed in a hiring freeze; the chief product officer thinks graduates are
flooding in. The company will place one product bet on the job-seeker side: outplacement partnerships (A), employer posting incentives to lift
hiring (B), early-career tools (C), a returnship programme (D) or career-move tools for voluntary changers (E). The planning template says how the
cause is chosen. The product change log records every past partnership launch.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the open-to-work flags, the optional reasons, applications, logins, profile edits, the research
  definition of an active seeker and the partner lists. The layoffs, the hiring slowdown and the graduates are all real. Nothing reported is
  overturned; most members never recorded why they were looking, and the data can settle it.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the licensed basis. The flow decomposition with self-reported reasons still names the hiring
  freeze, and the reason field still looks like the only source of reasons.
* **Instrument repair.** Make the reason field mandatory from tomorrow: this year's rise was recorded without it, and the bet is judged on this
  year. The behavioural trace already in the logs settles the reasons the field never captured.
* **Lens swap.** The naive split assigns reasons to the members who stated one and scales them up; the answer assigns every member by what
  they did, which moves 0.37 million members into a group the stated reasons barely contain.

## 3. The driving force

A strong solver distrusts the open-to-work flag, because members forget to switch it off, and uses the research definition (applied in the last
30 days or switched on in the last 90). It decomposes the rise into flows: lower job-finding accounts for 0.36 million, and inflows for the rest,
split by reason. The reason is an optional field filled by 30% of members. Laid-off members fill it 55% of the time, graduates 60%, returners from
a career break 5%. Scaling stated reasons up hands the unknown 70% to whoever states most, and the hiring freeze stays on top. Returners can be
identified anyway: an account dormant for at least twelve months, reactivated, followed by a profile update and the open-to-work switch within
thirty days. The six partnership launches in the change log come with partner lists, settled records of who was laid off and who was returning
from a break, and the dormancy trace reproduces every returnship list while the layoff trace (a cluster of colleagues ending positions at the
same employer in the same fortnight) reproduces every outplacement list. Assigned by trace, returners account for 0.47 million of the rise.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Rise in open-to-work flags by stated reason, scaled to the whole rise | A, layoffs (595k) | The recruiting team's own view, from the profile's own field | The research definition: an active seeker applied in the last 30 days or switched on in the last 90, and 0.9M flags are stale |
| 1 | Rise in active seekers by the dated definition, by stated reason, scaled | C, graduates (410k) | The research team's own population, with stale flags gone | The stock rose partly because fewer seekers left: job-finding fell, which no reason field can show |
| 2 | Flow decomposition: lower job-finding against inflows, inflows split by stated reason | B, hiring freeze (360k) | Flows and hazards rather than counts, with every member in the population | The partner lists: stated reasons reproduce 31% of the members on the six settled lists |
| 3 | **Decisive:** inflows assigned by behavioural trace (dormancy for returners, colleague clusters for layoffs), the rest by stated reason | **D, returners (470k)** (4th of 5 on rung 0) | — | — |

* **Position table.** D ranks 4th on rungs 0 and 1 and 5th on rung 2, and leads only rung 3. Rung leaders beat their runners-up by 2.02×,
  1.24×, 1.26× and 1.31×.
* **Discriminator dominance.** The hiring freeze carries a 3.56× lead into rung 3 (360k against 101k). The trace multiplies returners'
  inflow by 4.65 and leaves the outflow component unchanged, an edge of 4.65×, above the required 1.2 × 3.56 = 4.28; the net margin is 1.31×.
* **Partial correction priced (L3).** A solver who fills missing reasons from the stated mix within each experience band still hands returners
  a stated-reason share and names B. One who treats every reactivated account as a returner, without the dormancy length, sweeps in members
  back from short absences and names D at 640k, 36% high, while reproducing only 2 of 6 lists.
* **Grid.** Population (flags, dated rule) × decomposition (stock, flows) × reasons (stated, banded, trace) gives ten feasible builds; the
  flag builds name A, the dated stock builds C, the flow builds with stated or banded reasons B, and only flows with the trace name D.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The data dictionary calls the reason field optional; the change log describes each partnership. No document says
   returners can be identified, or by what.
2. **The corpus pins a construction, not a menu.** The dormancy trace reproduces both returnship lists in full and the colleague-cluster trace
   all four outplacement lists; stated reasons reproduce 31% of listed members, banded imputation 44%. The traces need logins, profile edits and
   colleagues at the same employer, ordered in time; nothing in them is a single column.
3. **No arithmetic symptom.** Flows reconcile to the stock change exactly (1.20M) under every assignment; members, flags and applications tie.
4. **Not a row predicate.** Dormancy is a gap between logins; a layoff cluster is a group of colleagues whose position end dates fall in one
   fortnight; both need ordered histories and other members' records.
5. **The enumeration is arithmetic.** No column says "returner"; 470,000 are built from activity logs.
6. **No cutover date.** Returners arrived steadily across the year; the dated events (two large layoff announcements in the spring) are the
   recruiting team's decoy.
7. **Survives deletion.** With every voice gone, the flow decomposition with stated reasons still names the hiring freeze.

## 6. The calibration corpus

* **Form.** Six partnership launches in the product change log (four outplacement partners, two returnship partners), each with the partner's
  list of enrolled members, their reasons as the partner recorded them, and the members' platform timelines before and after enrolment.
* **What it pins.** The traces (above), and that stated reasons under-represent returners by a factor of ten.
* **Twin pair.** March and September carried the same number of open-to-work switches, the same stated-reason mix, the same applications and
  the same mix of account types. Returner inflows were 52,000 and 25,000 (2.1×), because March followed the annual school-year transition when
  career-break members return. Only the dormancy trace separates the months.
* **Resemblance points at the decoy.** This year's surge in open-to-work switches matches the 2020 layoff wave in the change log on timing,
  sectors and stated reasons.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The planning template: the bet targets the cause behind the largest share of the year's rise in active job-seekers,
  decomposed by flows. The research data dictionary's dated definition of an active seeker.
* **Empirical pins.** The two traces, from the partner lists.
* **Voices.** The head of recruiting products: "Look at the open-to-work spikes; this is a layoff wave." The research lead: "Job-finding has
  fallen off a cliff. It's a hiring freeze."
* **Licensed wrong basis.** The template records that the public-policy team reads the rise through the government's displaced-worker series
  and will present it as layoffs.

## 8. Determinism by construction

* **Dormancy.** At least twelve months without a login; the dormancy distribution has no mass between 7 and 12 months for reactivated
  open-to-work members, so the cut does not move the answer.
* **Clusters.** Twenty or more colleagues at one employer ending positions within one fortnight; the clusters are separated from ordinary
  turnover by an empty band between 6 and 20.
* **Flows.** Monthly inflow and outflow hazards on the dated population, combined by Shapley over the five components; the components sum to the
  stock change.
* **Precedence.** A member matching both traces is a layoff; 1,200 members do, too few to move any rank.
* **Rounding.** Thousands of members; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Active job-seekers on the platform are up 1.2 million this year and we get one product bet on the seeker side. Our CPO is convinced graduates
> are flooding in. Tell me which cause we build for and how much of the rise it accounts for, in thousands of members, as one line for the
> planning review. Send `seeker_rise_case.xlsx` and a chart `rise_by_cause.png`.

* `seeker_rise_case.xlsx` — the five causes under each construction, the postings sheet (ask A), the subscriptions sheet (ask B) and the partner
  reproduction (ask C).
* `rise_by_cause.png` — a stacked bar of the 1.20M rise by cause under stated reasons and under the traces, side by side, with an inset
  histogram of months dormant before reactivation and the chosen cause labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month and each of four employer size bands, new job postings. *Device:* an employer refreshing
  a posting creates a new id with a refresh-of pointer, as the posting schema documents; counting ids overstates postings for the two largest
  bands, which refresh weekly.
* **Ask B (device-carried).** For each month and plan, new premium subscriptions on the seeker side. *Device:* annual plans billed monthly
  write a charge row each month with a plan-term field, as the billing schema documents; counting charges as new subscriptions inflates the
  annual plan twelvefold.
* **Ask C (validity).** For each of the six partner lists, members reproduced under stated reasons, banded imputation and the traces; and each
  cause's share under each rung construction.
* **Decoupling.** Clearing the traces changes no figure in asks A or B.

## 11. Rubric arithmetic

12 months × 4 bands (ask A) + 12 months × 3 plans (ask B) + 6 lists × 3 rules + 5 causes × 4 constructions (ask C) + the chosen cause, its share
and the runner-up's + 5 named chart parts + 2 files ≈ 135 criteria.

## 12. World-building constraints

* Rise of 1.20M: lower job-finding 0.36M; inflows A 0.20M, C 0.10M, D 0.47M, E 0.07M by trace.
* Reason fill rates: layoffs 55%, graduates 60%, voluntary 50%, returners 5%; rung figures as in section 4.
* 0.9M stale open-to-work flags; dormancy gap empty between 7 and 12 months; layoff clusters separated by an empty band from 6 to 20.
* March and September identical on every flag, reason, application and account-type column.
* Posting refreshes and billing rows touch no seeker's activity log.
