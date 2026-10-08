# DS45 — Which three legacy API versions stay running next year, when an integration is stranded by any one operation without a successor

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · developer platform version lifecycle |
| Mirrors | Retiring old platform versions on usage telemetry dominated by machines (SaaS API version sunsets at Stripe, Twilio and Salesforce, minimum OS and SDK versions at Apple and Google, interpreter support windows in open-source libraries), where the harm of retiring a version is set by its least replaceable operation |
| Decision shape | An allocation under a cap: next year's budget keeps three of the seven legacy API versions running; the other four retire in March |
| Committed call | The three versions kept, and the annual recurring revenue their retention protects, in $ millions to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · E30, a minimum over sub-units (an integration migrates cleanly only if every operation it uses has a successor, operations built from path templates and the request mode), with finer controls separating constructions (E16) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #12 stops at the first control that passes · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Gold-standard subsample: last year's v1 retirement audit, 400 keys sampled at random from v1's traffic and hand-reviewed by the partner team (owner, integration, production or machine traffic, and whether the integration migrated cleanly or was stranded) |
| Driving force | Retiring a version costs only the integrations that cannot move. An integration moves cleanly only if every operation it uses has a successor in v6, and one missing operation pins it, however rarely it is called. Traffic, keys and even the revenue on a version all point at the newest, busiest versions, where nearly everything has a successor. The audit reproduces only at the grain of the operation, which exists in no column: it is a path template plus the request's mode. |

## 1. Situation

A document-signing platform runs its current API, v6, alongside seven legacy versions (v2.0 to v5.0). Next year's budget funds three
legacy maintenance squads, so three versions stay and four retire in March. The retirement policy keeps the versions whose retirement
would strand the most annual recurring revenue. The traffic dashboard ranks versions by calls, and the head of platform wants to keep the
busiest. Last year the platform retired v1 and had its partner team audit what happened.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the call log, the key registry, the account revenue table, the changelog's successor map and the v1
  audit. No stakeholder read is overturned: the busiest versions are busy, and the revenue on them is real. The difficulty is which of that
  revenue a retirement actually strands.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and every voice. Revenue on each version, built from integrations, still ranks v5.0, v4.1 and
  v3.1 first.
* **Instrument repair.** No file the ladder uses is suspect: the call log, key registry, successor map and audit are complete, and every
  write call carries its mode. Even with every call labelled as person-driven or machine, rung 0 stays on v3.1, v2.0 and v4.1 and rung 1
  only moves onto rung 2's v5.0, v4.1 and v3.1. Integrations and operations are entities no row records, so the operation-grain minimum is
  still needed.
* **Lens swap.** The naive read and the answer differ in population: every integration on a version, against the integrations that use at
  least one operation without a successor, a set built operation by operation.

## 3. The driving force

A strong solver discards raw calls, which are dominated by synthetic monitors and test suites, builds integrations from the key registry,
keeps production traffic, and values each version by the revenue of the integrations on it. That keeps v5.0, v4.1 and v3.1, the versions
most customers use. But a retirement loses only the integrations that cannot move, and the v1 audit shows which those were: of 212
production integrations, 151 migrated cleanly within the notice period and 61 were stranded. The 61 are exactly the integrations that used
at least one operation the successor map leaves without a v6 equivalent, however seldom: a monthly audit-trail export, a bulk void, an
envelope sent with SMS authentication. Operations are not endpoints. The map lists them as a path template with a mode, and POST
/envelopes has a successor except in its SMS-authentication mode. The newest versions are busy and almost entirely mapped; the old,
quiet versions hold the integrations that cannot leave.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Calls by version over 90 days, the traffic dashboard; keep the three busiest; revenue of every account calling them | v3.1, v2.0 and v4.1; $38.4M (+225%) | The platform's own usage view, and v3.1 leads by 1.22× | The key registry's notes: synthetic-monitor keys and sandbox keys carry no customer traffic, and the policy counts customer revenue only |
| 1 | Production keys only, monitors and sandbox removed; revenue of accounts with production calls on each version | v4.1, v5.0 and v2.0; $33.0M (+180%) | The documented exclusions, and the audit's total of 212 production integrations reproduced | The audit's 400 key-level labels: production keys reproduce 301 of them; customers' uptime checkers and rotated keys sit inside the total |
| 2 | Integrations built from the effective-dated key registry, kept where they write on at least five days in 90 (the construction that reproduces all 400 labels); every integration on a retiring version counted at risk | v5.0, v4.1 and v3.1; $30.7M (+160%) | The right population, matched record by record to the audit | The audit's outcomes: 151 of v1's 212 integrations migrated cleanly, so revenue on a version is not revenue stranded |
| 3 | **Decisive:** an integration is stranded only if some operation it used, a path template with its request mode, has no successor in the map, the law that reproduces all 212 audited outcomes; keep the three versions stranding the most revenue | **v2.1, v4.0 and v3.0; $11.8M** (v2.1 5th of seven on rung 0) | — | — |

* **Figure shape.** Every correction walks the protected figure down, and the answer is the minimum cell: every other construction credits
  retirement with revenue that would have migrated. Offsets: +225%, +180%, +160%.
* **Position table.** v2.1, which leads the answer, is 5th of seven on rung 0, 6th on rung 1 and 5th on rung 2; v4.0 is 6th, 5th and 4th;
  v3.0 7th, 7th and 6th. None of the three enters an intermediate set. Rung margins: v3.1 over v2.0 1.22×, v4.1 over v5.0 1.17×, v5.0
  over v4.1 1.52×, v2.1 over v4.0 1.23×, and at the cut v3.0 over v5.0 1.94×.
* **Discriminator dominance.** v3.1, rung 2's third, carries a 1.83× revenue advantage over v3.0 into rung 3 ($7.5M against $4.1M). v3.0
  keeps 0.76 of its rung-2 figure as stranded revenue and v3.1 0.19, an edge of 4.1×, against the required 1.2 × 1.83 = 2.2 and past the
  2.9 that headroom asks. v5.0 carries 3.4× and keeps 0.11 (edge 6.6× against 4.1); v4.1 carries 2.2× and keeps 0.11 (7.0× against 2.7).
* **Partial correction priced (L3).** No half-applied law keeps the answer's three. Applying the minimum at the grain of the endpoint, not
  the operation, misses the SMS-authentication integrations on v4.0 and keeps v2.1, v3.0 and v5.0 for $9.5M (−19.5%), v5.0 1.78× ahead
  of v4.0. Counting an integration stranded only when under 95% of its calls have a successor misses the monthly exports on v3.0 and keeps
  v2.1, v4.0 and v5.0 for $9.2M (−22%), v5.0 1.9× ahead of v3.0. Scaling each version's revenue by the share of its operations without a
  successor keeps v5.0, v2.1 and v4.1 for $9.3M (−21%), v5.0 1.4× ahead of v3.0. The operation-grain law run on production keys rather
  than integrations lets the uptime checkers on v2.0 in and keeps v2.1, v2.0 and v4.0 for $13.1M (+11%), v2.0 1.42× ahead of v3.0.
* **Grid.** Population (all calls, production keys, integrations) × stranding law (all at risk, operation share by version, call share
  under 95%, endpoint-grain minimum, operation-grain minimum) = 15 cells. Only integrations with the operation-grain minimum keep v2.1, v4.0
  and v3.0, at $11.8M; the nearest other figure is $13.1M (+11%), on production keys.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says to keep the versions whose retirement strands the most revenue. The changelog maps operations to
   successors. No document says what strands an integration, or that one unmapped operation is enough.
2. **The audit pins it, as a construction.** The operation-grain minimum reproduces all 212 audited outcomes. The endpoint-grain minimum
   reproduces 197, every miss an SMS-authentication sender counted as clean. Call-share thresholds from 80% to 99% reproduce between 179
   and 188, a flat curve no threshold rescues. The operation exists in no column: each logged path must be matched to its template and
   paired with the request's mode field before the minimum can be taken over an integration's window.
3. **No arithmetic symptom.** Calls reconcile to keys, keys to integrations, integrations to accounts and accounts to the revenue table
   under every rung, and every version's stranded revenue is positive and below its revenue at risk.
4. **Not a row predicate.** A call is never stranded on its own; the unit is an integration's whole set of operations over the window,
   assembled across rotated keys, and the test is a minimum over that set.
5. **The enumeration is arithmetic.** No column marks an integration as stranded or an operation as unmapped for a given mode.
6. **No cutover date.** The v1 retirement is a closed measurement instance; the decision rests on which operations each live integration
   uses, and no series the answer reads steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, revenue on each version still keeps the busiest versions.

## 6. The calibration corpus

* **Form.** The v1 retirement audit: 400 keys drawn at random from v1's last 90 days of traffic, each hand-reviewed for its owning account,
  its integration, whether its traffic was production or machine (monitors, test suites, uptime checkers), and, for the 212 production
  integrations, whether each migrated cleanly within the notice period or was stranded.
* **The salient control (E16).** The audit's total of 212 production integrations. Production keys deduplicated by account match it, and
  so does the registry construction; only the registry construction reproduces all 400 key-level labels.
* **What it pins.** The stranding law (above), 212 of 212 outcomes, and the registry construction of integrations, 400 of 400 labels.
* **Twin pair.** Two growth-tier accounts in the audit are identical on every column the audit and the logs show: $180k of revenue, three
  integrations each, the same SDK, the same call volume and the same twelve endpoints. One kept its $180k; the other fell to $90k (2.0×)
  when one of its integrations, which voided envelopes in bulk mode, could not move. Only the operation-grain minimum separates them.
* **Resemblance points at the decoy.** By traffic, SDK mix and account tier, v5.0 most resembles v1 in its last year, when 71% of its
  integrations migrated cleanly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The retirement policy: three legacy versions are kept next year, those whose retirement would strand the most annual
  recurring revenue; the rest retire in March with six months' notice. The changelog's successor map, by operation (path template and
  mode). The key registry, effective-dated, with key-to-application links and the platform's synthetic-monitor and sandbox keys. The
  account revenue table.
* **Empirical pins.** The integration construction and the stranding law, from the audit.
* **Voices.** The head of platform: "The busiest versions are the ones customers can't live without." The developer-relations lead:
  "Customers move when we give them a date." The finance partner: "Every dollar on a retiring version is a dollar at risk."
* **Licensed wrong basis.** The policy records that the executive review receives the traffic dashboard's version ranking and will see
  that table.

## 8. Determinism by construction

* **Templates.** Every logged path matches exactly one operation template; templates do not overlap, and every write call since 2022
  carries the mode field.
* **Integrations.** The registry links every production key to one application at every date; the five-day write rule and four- to
  six-day alternatives give the same 400 labels.
* **Window.** Integrations are judged on the last 90 days; 60 and 120 days give the same three versions and move the figure by under
  $0.2M.
* **Rounding.** $11.8M is $11.82M before rounding; the third and fourth versions differ by $1.5M.

## 9. Prompt sketch and deliverables

> Next year's budget keeps three of our seven legacy API versions running, and the other four retire in March. Our head of platform wants
> to keep the busiest ones on the traffic dashboard. Tell me which three we keep and the annual revenue keeping them protects, in $
> millions to one decimal, as the line for the sunset plan. Send `version_retention.xlsx`, a chart `stranded_revenue.png`, and a one-page
> `sunset_plan.docx`.

* `version_retention.xlsx` — the seven versions under each rung construction with the audit reproduction counts (ask C), the support sheet
  (ask A) and the webhook sheet (ask B).
* `stranded_revenue.png` — for each version, revenue on it and revenue stranded by its retirement as paired bars, ordered, with the cut at
  three marked and the operations that strand the most revenue labelled on the three kept versions.
* `sunset_plan.docx` — the three versions kept, the protected revenue, and why the busiest versions retire.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of last year and each of the three account tiers, the median first-response time
  on support tickets. *Device:* a ticket merged into another keeps its own creation time but inherits the parent's first response, as the
  support-desk guide documents. Treating merged tickets as answered at their own first event understates response times in the busiest
  months.
* **Ask B (device-carried).** For each month of last year, the share of webhook events delivered on the first attempt. *Device:* each
  retry is logged as a new delivery row carrying the original event ID, as the webhook log's dictionary documents. Counting rows as events
  understates first-attempt delivery and double-counts failures.
* **Ask C (validity).** For each of the seven versions, the protected revenue under each of the four rung constructions, and the audit
  reproduction counts (of 212) for the endpoint-grain and operation-grain laws.
* **Decoupling.** Clearing the operation-grain minimum changes no figure in asks A or B. Support tickets and webhook deliveries touch no
  call, key, operation or revenue record.

## 11. Rubric arithmetic

12 months × 3 tiers (ask A) + 12 months (ask B) + 7 versions × 4 constructions + 2 reproduction counts (ask C) + the three versions, the
protected revenue and the margin at the cut + 5 named chart parts + 3 files ≈ 89 criteria.

## 12. World-building constraints

* Calls over 90 days (millions): v3.1 412, v2.0 338, v4.1 290, v5.0 262, v2.1 171, v4.0 158, v3.0 96. Revenue of accounts with production
  calls ($M): v4.1 12.6, v5.0 10.8, v2.0 9.6, v3.1 8.9, v4.0 7.4, v2.1 6.3, v3.0 4.4. Revenue of integrations: v5.0 14.0, v4.1 9.2, v3.1
  7.5, v4.0 6.8, v2.1 5.6, v3.0 4.1, v2.0 1.9. Stranded revenue: v2.1 4.8, v4.0 3.9, v3.0 3.1, v5.0 1.6, v3.1 1.4, v4.1 1.0, v2.0 0.6.
* Partial cells: endpoint grain v4.0 0.9, others unchanged; call share under 95% v2.1 4.1, v4.0 3.6, v5.0 1.5, v3.1 1.3, v3.0 0.8; share
  of unmapped operations v5.0 0.25, v2.1 0.55, v4.1 0.30, v4.0 0.40, v3.1 0.35, v3.0 0.60, v2.0 0.50; operation grain on production keys
  v2.0 4.4.
* Audit: 400 keys, 212 production integrations, 151 clean and 61 stranded; the twin accounts match on every audit and log column.
* Support tickets and webhook deliveries are independent of every main-call record.
