# FC29 — Which AI product gets the new 240-GPU cluster, when the close-out's per-request cost is a share of a session prefill that next quarter's books will divide differently

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · generative-AI serving capacity |
| Mirrors | Assigning new accelerator capacity across AI products (chat, coding and agent products at model providers, Meta's inference fleet, cloud GPU reservations), where the planning ratio of GPU time per request quietly embeds each product's requests per session |
| Decision shape | Which of N gets one scarce thing: the 240-GPU cluster arriving in January, for the first quarter, to one of six products |
| Committed call | The product the cluster goes to, and that product's Q1 peak-week GPU shortfall, to the nearest 10 GPUs |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S6 (a correct share carried onto a different book), with a binding limit applied in the figure (measured #10) at rung 1 |
| Gate G mechanism | forecasting, with binding_constraint and decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Prior-period close-out: the capacity team's quarterly close-outs for Q1–Q3 (per product: requests, GPU-hours, GPU-seconds per request, peak-week GPUs) |
| Driving force | A request's GPU cost in the close-out is its share of the session's cached prefill (the document, tool manifest or repository context) plus its own decode, correct for the quarter that produced it. Doc Q&A's new bulk-report tenants send 1.5 requests per document against the interactive tenants' 9, so each of their requests carries six times the prefill the close-out's average implies, while Agents' sessions lengthen from 8 requests to 20 and go the other way. Nothing labels the fixed part: it shows only when requests are ranked within their sessions in the serving log. |

## 1. Situation

A model provider's serving platform runs six products: consumer chat, a code assistant, agents, document Q&A for enterprises, a batch
summarisation API and a voice assistant. A 240-GPU cluster lands in January and, for the first quarter, goes whole to one product. The
capacity policy sends new capacity where it will relieve the largest peak-week shortfall in GPUs. Every quarter the capacity team
publishes a close-out of what each product consumed. Document Q&A signed eleven enterprise tenants for bulk report generation starting
in January; two of them have run as pilots since October. The cluster's spec register gives its memory and batch configuration.

## 2. Gate G: why this is legal

* **Litmus.** Every figure in the pack is correct: the close-outs, the serving log, the contracted volumes, the spec register. The
  close-out's GPU-seconds per request are exact for the quarter they describe, and no stakeholder's reading of their own numbers is
  overturned. The difficulty is that next quarter's books divide the same fixed costs over different numbers of requests.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the capacity lead's view and every voice. Forward requests at the close-out's cost per request is still
  the natural build, it still reproduces every closed quarter, and it still names Agents.
* **Instrument repair.** Imagine a close-out that split every product's GPU time into prefill and decode. The Q1 shortfall would still
  have to be rebuilt from Q1's sessions and requests, because the bulk tenants' book has not run yet.
* **Lens swap.** The naive read and the answer price different books: Q3's sessions and requests against Q1's, where one product's
  requests per session fall sixfold and another's more than double.

## 3. The driving force

A strong solver takes each product's contracted and trended Q1 requests, prices them at the close-out's GPU-seconds per request, nets the
current allocation, and checks the result against the closed quarters, where the same carry reproduced every product to within 2%. It
then applies the spec register's sequence-length limit and the policy's production-only rule. Every step is correct. The close-out's
cost per request, though, is the session's prefill divided over the requests that shared it, plus each request's own decode. In Q3 a
Doc Q&A user asked nine questions of each uploaded document, so a request carried a ninth of the document's prefill. The bulk tenants
send one report request per document and a follow-up half the time: each request carries two thirds of a document. The serving log
shows it only when requests are grouped by session and ranked: the first request in a session costs several times the rest. Rebuilt as
sessions × prefill plus requests × decode, Doc Q&A's Q1 need is 2.6 times what the carried cost says.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Q1 requests × close-out GPU-seconds per request − current allocation; the cluster relieves min(240, shortfall) | C, Agents (240 against 160, 1.50×) | The capacity team's own planning ratio, reproduced on every closed quarter | The spec register: at the configured batch the cluster serves sequences up to 32,768 tokens, and 85% of Agents' GPU time runs on longer ones |
| 1 | Only the shortfall the cluster can serve counts, as the policy requires | B, Code assistant (1.33×) | The binding limit applied in the figure, not noted as a risk | The job register tags 12% of the code assistant's Q3 GPU-hours as internal evaluation runs, and the policy counts production traffic only |
| 2 | Hygiene: production traffic only | F, Voice assistant (1.33×) | Servable, production-only and reconciled to the job register | The serving log: within each session the first request carries the cached prefill, and Q1's requests per session differ from Q3's |
| 3 | **Decisive:** Q1 need rebuilt as sessions × per-session prefill + requests × per-request decode, each recovered by ranking requests within sessions | **D, Document Q&A** (5th of 6 on rung 0) | — | — |

* **Position table.** Document Q&A ranks 5th on rung 0 (shortfall 70), 4th on rung 1 and 3rd on rung 2, and leads only rung 3. Rung
  leaders beat their runners-up by 1.50×, 1.33×, 1.33× and 2.00×.
* **Discriminator dominance.** The voice assistant carries a 1.71× advantage into rung 3 (shortfall 120 against 70). The rebuild
  multiplies Doc Q&A's shortfall 8.9× (70 to 621) and leaves the voice assistant's unchanged, an edge of 8.9× against the 2.06× that
  1.2 × 1.71 requires. The product, (1/1.71) × 8.9 = 5.2×, is the ratio of shortfalls; the cluster can relieve only 240 of Doc Q&A's, so
  the margin on the policy's measure is 240 against 120, 2.00×.
* **Partial correction priced (L3).** Pricing Q1 at November's cost per request, the latest month, catches the two pilots and the
  lengthening agent sessions only as far as November: Doc Q&A's shortfall reads 119 and the voice assistant still leads. Rebuilding the
  agents' density, the visible trend, without the bulk tenants' density also names the voice assistant.
* **Grid.** Servability (ignored, applied) × production filter (off, on) × cost basis (Q3 per request, November per request, session
  rebuild) = 12 cells. The eight cells without the rebuild name Agents, the code assistant or the voice assistant. All four rebuild
  cells name Doc Q&A at 621, because Doc Q&A is fully servable and has no evaluation traffic; the nearest wrong shortfall for it is a
  rebuild that applies the bulk density to every Doc Q&A tenant (1,295, +108%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The close-out reports GPU-seconds per request and nothing about sessions. No document says the prefill is
   cached per session, and the contracts state volumes in requests.
2. **Corpus blind to the shift.** *In every closed quarter no product's requests per session moved by more than 3%, because every
   product's session pattern was stable until the agent and bulk-report launches; so carrying a quarter's cost per request forward
   reproduced the next quarter's GPU-hours to within 2% for every product.* The close-outs certify the carry exactly where it cannot fail.
3. **No arithmetic symptom.** Q3's shares sum to Q3's GPU-hours under either decomposition, requests reconcile to the log, and the
   allocation and spec figures tie on every rung.
4. **Not a row predicate.** The fixed part needs requests grouped by session and ranked within it, a per-product recovery of prefill and
   decode, and a forward count of sessions as well as requests.
5. **The enumeration is arithmetic.** No column says "prefill" or "cached"; the bulk tenants' density comes from the two pilots'
   sessions in the serving log.
6. **No cutover date.** The bulk contracts start in January but step nothing in the pack's outcome series; the pilots have run quietly
   since October inside a product whose totals barely moved.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The quarterly close-outs for Q1, Q2 and Q3: per product, requests, GPU-hours, GPU-seconds per request and peak-week GPUs.
* **What it certifies.** Rung 0's carry: each quarter's cost per request, applied to the next quarter's requests, reproduces that
  quarter's GPU-hours to within 2% for all six products, so a solver who back-tests is confirmed.
* **What it is blind to.** Density change (above). The close-outs carry no session counts at all.
* **Twin pair.** Doc Q&A tenants Halvorsen Insurance and Mereway Logistics are identical in the Q3 close-out's tenant appendix
  (requests, GPU-hours, GPU-seconds per request) and in their contracted Q1 requests. Their Q1 need differs 2.05×, because Mereway, one
  of the October pilots, now sends three documents in ten as one-call bulk reports (1.5 requests per document) while Halvorsen sends
  every document to the interactive desk (9 per document). Only the session-level rebuild separates them.
* **Resemblance points at the decoy.** By product mix and request growth, Q1 most resembles Q3, a quarter the carried cost reproduces to
  within 1%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capacity policy: new capacity goes where it relieves the largest peak-week shortfall in GPUs, counting only
  production traffic the new capacity can serve. The spec register: the cluster's memory, model and batch configuration. The commitments
  ledger: contracted Q1 requests per enterprise tenant.
* **Empirical pins.** Per-session prefill and per-request decode for each product, from requests ranked within sessions. Each product's
  Q1 requests per session: the trend for agents and the October pilots for bulk tenants.
* **Voices.** The capacity lead: "The close-out makes it obvious that Agents needs it; their requests are growing fastest." The Doc Q&A
  product manager: "Bulk reports are one call per document. If anything they're lighter than chat." The platform director: "Our cost
  per request has been the most reliable number we publish."
* **Licensed wrong basis.** The capacity policy records that finance prices every product's capacity plan at the close-out's cost per
  request and will review the decision on that basis.

## 8. Determinism by construction

* **Session ranking.** Every session's first request carries its full prefill and later requests carry none, so per-session prefill and
  per-request decode are recovered exactly whether the solver ranks by timestamp or by sequence number.
* **Forward density.** Agents' requests per session rose linearly from 8 to 14 between July and November and the Q1 trend reaches 20
  under a linear or log-linear fit alike; the pilots have run at exactly 1.5 since October.
* **Servability.** No product's traffic sits between 30,000 and 36,000 tokens, so the 32,768 limit selects the same requests under any
  reading of the batch arithmetic.
* **Peak week.** Every product's Q1 peak week is the second week of January under any of the past three years' weekly profiles.
* **Rounding.** Doc Q&A's shortfall (621) sits inside the 620 bin, away from its edges.

## 9. Prompt sketch and deliverables

> The new 240-GPU cluster lands in January, and for the first quarter it goes to one product. Our capacity lead says the close-out makes
> it obvious that Agents needs it. Name the product that gets the cluster and its peak-week GPU shortfall for the quarter, to the
> nearest 10 GPUs, in a sentence I can put to the capacity council. Send `cluster_case.xlsx` with the build and the sheets below, a chart
> `q1_shortfall.png`, and a one-page `cluster_decision.pdf`.

* `cluster_case.xlsx` — the shortfall build for all six products, the latency sheet (ask A) and the tenant sheet (ask B).
* `q1_shortfall.png` — paired horizontal bars per product: Q1 peak-week shortfall under the carried cost and under the session rebuild,
  with the cluster's 240-GPU line, the non-servable share of Agents hatched, and the chosen product annotated with its shortfall.
* `cluster_decision.pdf` — the committed product and shortfall, and why each of the other five is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six products and each month of Q3, the p95 time to first token. *Device:*
  streaming responses log the first-token event in the stream-events table, while the request table's latency field is time to
  completion, as the observability guide documents; reading the request table overstates time to first token for the four streaming
  products. Latency enters no part of the capacity build.
* **Ask B (device-carried).** For each product, the paying enterprise tenants at the end of October and of November. *Device:* a tenant
  that consolidated its workspaces survives under one tenant ID with the retired IDs in the tenant-merge map, as the account guide
  documents; counting raw IDs overstates tenants at three products. No merged tenant is a Doc Q&A pilot or a bulk tenant.
* **Ask C (validity).** The GPUs the cluster would relieve for each product under each of the four rung constructions.
* **Decoupling.** Clearing the session rebuild changes no figure in asks A or B.

## 11. Rubric arithmetic

6 products × 3 months (ask A) + 6 × 2 (ask B) + 6 products × 4 constructions (ask C) + the committed product, its shortfall and the
runner-up's margin + 5 named chart parts + 3 files ≈ 65 criteria.

## 12. World-building constraints

* Q1 shortfalls under the carried cost (GPUs): Agents 360, code assistant 160, voice 120, consumer chat 90, Doc Q&A 70, batch API 60.
  85% of Agents' GPU time is on sequences above 32,768 tokens; 12% of the code assistant's Q3 GPU-hours are evaluation runs.
* Prefill share of Q3 GPU time: Doc Q&A 0.70, Agents 0.60, code assistant 0.50, chat 0.30, voice 0.20, batch 0.05. Requests per session,
  Q3 to Q1: Doc Q&A interactive 9 to 9, bulk tenants 1.5 (45% of Doc Q&A's Q1 requests), Agents 8 to 20, all others unchanged.
* Rebuilt Q1 shortfalls: Doc Q&A 621, voice 120, chat 90, code assistant 69, batch 60, Agents 0.
* Rung leaders Agents, code assistant, voice, Doc Q&A, with margins of 1.50×, 1.33×, 1.33×, 2.00×.
* The twin tenants are identical on every close-out and commitments column.
* Streaming events and tenant merges touch no request, session or GPU-hour in the build.
