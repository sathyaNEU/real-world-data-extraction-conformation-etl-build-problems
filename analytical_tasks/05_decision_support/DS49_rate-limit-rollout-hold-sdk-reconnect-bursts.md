# DS49 — Whether per-client rate limits roll out next quarter, when the burst the gateway allows was validated on the old mobile SDK

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · API platform reliability |
| Mirrors | Sizing throttles and quotas on traffic replays that no longer describe the clients who will hit them (token-bucket limits at API platforms, autoscaler burst headroom at cloud providers, fulfilment-centre intake caps sized before a carrier changes its batching) |
| Decision shape | Hold, forced by a blocking quantity: roll out per-client token-bucket limits at a named burst size in next quarter's change window, or hold the rollout to the following window |
| Committed call | Roll out at a named burst size or hold, with the deciding figure: the worst client tier's throttled share of legitimate requests next quarter at the largest burst the gateway allows, as a percentage to two decimals |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · E17, validated on one population and applied to another (the replay reproduces all nine past limiter rollouts, but next quarter's mobile traffic is 78% on SDK v5, whose reconnect replays burst three times harder), with a binding limit applied in the figure (E14) at rung 1 |
| Gate G mechanism | binding_constraint, with signal_vs_noise_or_hold |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #3 stops at a close but inexact match |
| Calibration form | Change-log natural experiments: nine past limiter rollouts with four weeks of request traces either side and the measured throttled share, and the four-week SDK v5 beta on 5% of devices |
| Driving force | A token bucket throttles bursts, and the replay that sizes it is exact on every past rollout. But mobile devices replay their offline queues on reconnect, and SDK v5, which a forced upgrade puts on 78% of devices next quarter, sends up to 200 queued requests in two seconds where v4 trickled them. The gateway caps the burst at 60. At 60, the replay on last month's traffic passes every tier; calibrated to next quarter's SDK mix, mobile throttles 0.34%, more than three times the policy's 0.1%. |

## 1. Situation

A field-inspection software company runs a public API used by its web dashboard, customers' integrations and its mobile apps, which
inspectors use offline on site and sync when they reconnect. Abuse is rising, and the platform team wants per-client token-bucket limits
(refill 10 requests a second) in next quarter's change window. The change policy rolls a limit out only if every client tier keeps
throttled legitimate requests at or under 0.1% at a burst size the gateway can hold; otherwise the rollout waits a quarter. Engineering's
proposal sizes the burst from per-minute peaks.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the gateway's request logs, the change log's nine rollouts, the v5 beta traces, the device registry,
  the release plan and the gateway capacity register. No stakeholder read is overturned: the new SDK does batch, and per-minute peaks did
  size past limits. The difficulty is which traffic the limit will meet.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete engineering's proposal and every voice. A per-tier replay of last month's traffic, capped at the gateway's 60,
  still passes every tier and still rolls out.
* **Instrument repair.** No file the ladder uses is suspect: the gateway logs every request to the millisecond, the device registry maps
  every device to its SDK on every day, and the nine rollouts and the v5 beta are complete traces. Recording last month's traffic more
  finely leaves rung 0 at 20, rung 1 at 85 and rung 2 rolling out at 60, because 95% of last month's mobile devices ran v4. Next quarter's
  78% v5 mix is a forward population built from the release plan, so the calibration by SDK version is still needed.
* **Lens swap.** The naive read and the answer differ in population and moment: last month's devices, 95% on v4, against next quarter's,
  78% on v5, through a join to the device registry.

## 3. The driving force

A strong solver drops engineering's per-minute rule, which the change log shows understating throttling, replays every client's requests
through the bucket tier by tier, and finds that mobile needs a burst of 85 to stay at 0.1%. The gateway capacity register allows 60, so it
applies the limit in the figure rather than noting it: at 60, last month's traffic throttles mobile 0.09%, web 0.01% and integrations
0.04%. Every tier passes, and the replay is the method that reproduces all nine past rollouts. But last month's mobile traffic came from
devices 95% on SDK v4. The release plan ends v4 on 1 July, and the forced upgrade puts 78% of next quarter's mobile traffic on v5. The
change log's v5 beta, four weeks on 5% of devices, shows what v5 does on reconnect: it replays the whole offline queue at once. Replayed
at 60, v5 devices throttle 0.41% and v4 devices 0.07%. Weighted to next quarter's mix, mobile throttles 0.34%, and no burst the gateway
allows brings it to 0.1%.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Engineering's proposal: burst = 99th-percentile requests per minute ÷ 60 × 2 | Roll out at 20 | The platform's established sizing rule, and its own team's figure | The change log: the per-minute rule predicted 0.1% or less in all nine past rollouts, and four throttled more than 1%; replaying requests through the bucket reproduces all nine |
| 1 | Replay of last month's legitimate requests, tier by tier; the smallest burst keeping every tier at 0.1% | Roll out at 85 (set by mobile) | The policy's test, by the method the change log certifies | The gateway capacity register: at a 10-per-second refill, a client's burst may not exceed 60 tokens |
| 2 | The cap applied in the figure: replay at 60, tier by tier | Roll out at 60: mobile 0.09%, integrations 0.04%, web 0.01% | Every tier passes at the largest burst the gateway allows | The release plan and the beta: v4 ends on 1 July, 78% of next quarter's mobile traffic will be v5, and the change log's v5 beta throttles 0.41% at 60 |
| 3 | **Decisive:** mobile calibrated by SDK version through the device registry, v4 and v5 traces replayed at 60 and weighted to next quarter's mix | **Hold: mobile throttles 0.34% at 60, against 0.1%** | — | — |

* **Position table.** The rung calls are roll-outs at 20, 85 and 60, then the hold; no call repeats. The hold appears only when the cap and
  the forward mix are both applied.
* **Blocking quantity.** At the largest burst the gateway allows, mobile throttles 0.34% of legitimate requests next quarter, 3.4× the
  policy's 0.1%. The hold is falsifiable: v5 devices throttling under 0.105% at 60, or a gateway allowing a burst of 140, where the forward
  mix throttles 0.09%, would have rolled the limit out.
* **Discriminator dominance.** Rung 2's mobile tier clears the line by 1.11× (0.09% against 0.1%). Calibrating to the forward mix
  multiplies its throttled share by 3.7× (0.34 against 0.09), against the required 1.2 × 1.11 = 1.33 and past the 1.73 that headroom
  asks, so it lands 3.4× over the line.
* **Partial correction priced (L3).** No half-applied calibration holds; each rolls out. Calibrating by SDK version but weighting to last
  month's 5% v5 share gives mobile 0.09% and rolls out at 60. Weighting to next quarter's mix but treating the gateway's 60 as a risk to
  note finds the burst v5 needs, 140, and rolls out there in breach of the register. Weighting to the forward mix but testing the tiers
  pooled, as engineering's dashboard does, gives 0.09% at 60 (mobile is a fifth of requests) and rolls out at 60.
* **Grid.** Sizing (per-minute rule, pooled replay, per-tier replay) × gateway cap (noted, applied) × mobile mix (last month, next
  quarter by SDK version) = 12 cells. The per-minute cells roll out at 20; the pooled cells at 34 or 52; per tier without the cap at 85 or
  140; per tier with the cap at 60 on last month's mix. Only per tier, the cap and the forward mix hold, at 0.34%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The release plan dates v4's end, the SDK notes say v5 batches, and the policy states the test. No document says v5
   bursts harder against a bucket, or that the replay's traffic is the wrong population.
2. **The change log certifies the method and shows the new population.** The replay reproduces all nine past rollouts' measured throttled
   shares within 0.005 points; the per-minute rule misses four, all low. The v5 beta is the one natural experiment with v5 at any scale,
   and its traces replay to 0.41% at 60. The calibration is a construction: device IDs in the gateway log joined to the device registry's
   SDK version, each version replayed, and the shares weighted by the release plan's forward mix.
3. **No arithmetic symptom.** Last month's replay passes every tier at 60 with room, the cap is respected, and every figure reconciles to
   the gateway's counts.
4. **Not a row predicate.** Throttling is a sequence property of each client's arrivals against a refilling bucket, and the forward share
   is a mix of two replayed populations.
5. **The enumeration is arithmetic.** No column holds a device's throttled share or next quarter's SDK.
6. **No cutover date.** No series the replay reads steps. v4's end-of-life sets next quarter's population, which the analysis must build;
   last month's traffic contains no change at all.
7. **Survives deletion.** No wrong number exists to delete. Without engineering's figure or any voice, the capped replay still rolls out.

## 6. The calibration corpus

* **Form.** The platform's change log: nine limiter rollouts over two years, each with four weeks of request traces before and after and
  the measured throttled share, and the SDK v5 beta, four weeks on 5% of mobile devices, with full traces.
* **What it certifies.** The replay (9 of 9) and v5's reconnect behaviour: queues of up to 200 requests sent within two seconds.
* **What it does not show.** Next quarter's mix, which the release plan and the published adoption curve for forced upgrades give: 78% of
  mobile requests on v5 over the quarter.
* **Twin pair.** Two mobile customer accounts are identical on every column the gateway log shows: 300 devices, the same daily requests,
  the same per-minute 99th percentile and the same offline gaps. Replayed at 60 they throttle 0.05% and 0.10% (2.0×): one account's
  devices joined the v5 beta in its second week. Only the device registry's SDK version separates them.
* **Resemblance points at the decoy.** By tier and volume, the rollout most like this one is the integrations limit of last spring, which
  the replay sized exactly and which throttled 0.03%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The change policy: a limit rolls out only if every client tier (web, integrations, mobile) keeps throttled legitimate
  requests at or under 0.1% next quarter, at a burst the gateway capacity register allows; otherwise the rollout holds to the next window.
  The limiter specification: refill 10 a second, bucket starts full, excess requests rejected. The gateway capacity register: burst at
  most 60 tokens. The release plan: v4 ends on 1 July with a forced upgrade. Legitimate traffic excludes the crawler and abuse lists.
* **Empirical pins.** The replay, from the nine rollouts; v5's bursts, from the beta; next quarter's mix, from the release plan and the
  adoption curve.
* **Voices.** The platform lead: "Per-minute peaks have sized every limit we run." The mobile lead: "The new SDK batches, so it's gentler
  on the servers." The security lead: "We need limits in before the next scraping wave."
* **Licensed wrong basis.** The policy records that the change advisory board reviews the per-minute peak table.

## 8. Determinism by construction

* **Timestamps.** The gateway logs to the millisecond, so no tie convention enters the replay.
* **Mix.** The quarter-average v5 share is 78%; the end-of-quarter share, 95%, only raises the blocking quantity (to 0.39%).
* **Registry.** Every mobile device ID in the log maps to one SDK version on each day; devices that upgrade mid-quarter are split by date.
* **Rounding.** Mobile's forward share is 0.335% (0.78 × 0.41 + 0.22 × 0.07), reported as 0.34%, and every candidate burst from 20 to 60
  leaves it above 0.30%.

## 9. Prompt sketch and deliverables

> We want per-client rate limits live in next quarter's change window, before the next scraping wave. Engineering has sized the burst from
> our per-minute peaks. Tell me whether we roll the limits out, and at what burst, or hold them, with the figure that decides it as a
> percentage to two decimals, as the line for the change board. Send `rate_limit_decision.xlsx`, a chart `throttled_share_by_tier.png`,
> and a one-page `change_board_note.pdf`.

* `rate_limit_decision.xlsx` — each tier's throttled share under each rung construction with the replay's reproduction count (ask C), the
  error sheet (ask A) and the billing sheet (ask B).
* `throttled_share_by_tier.png` — throttled share against burst size from 20 to 150 for web, integrations, mobile on v4 and mobile on v5,
  as four curves, with the 0.1% line, the gateway's 60 and the forward-mix mobile curve labelled.
* `change_board_note.pdf` — the call, the blocking quantity, and what would let the limits roll out.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 30 days of last month, the gateway's server-error rate. *Device:* a request the
  gateway retries upstream is logged once per attempt with an attempt counter, as the gateway's log guide documents. Counting rows as
  requests overstates errors on the days an upstream service flapped.
* **Ask B (device-carried).** For each of the 40 largest integration customers, last month's billed API operations. *Device:* a batch
  request carries up to 100 operations and is billed per operation, as the pricing schedule sets out, while the gateway logs one request.
  Counting log rows understates the customers who batch.
* **Ask C (validity).** For each tier, the throttled share at bursts of 20, 60 and 85 on last month's traffic, mobile's share at 60 on
  next quarter's mix, and the replay's reproduction count on the nine rollouts.
* **Decoupling.** Clearing the SDK calibration changes no figure in asks A or B. Retry attempts and billed operations touch no client
  arrival sequence, device registry or change-log record.

## 11. Rubric arithmetic

30 days (ask A) + 40 customers (ask B) + 3 tiers × 3 bursts + 1 forward share + 1 reproduction count (ask C) + the hold, the blocking
quantity, its distance from the line and the falsifier + 5 named chart parts + 3 files ≈ 93 criteria.

## 12. World-building constraints

* Request shares: web 45%, integrations 35%, mobile 20%. Last month's mobile devices 95% v4, 5% v5; next quarter 78% v5 on average.
* Throttled share at a burst of 60: web 0.01%, integrations 0.04%, mobile 0.09% last month (v4 0.07%, v5 0.41%); mobile 0.34% next
  quarter. Bursts keeping every tier at 0.1%: 85 on last month's traffic, 140 on next quarter's; pooled: 34 and 52.
* Change log: nine rollouts reproduced within 0.005 points; the per-minute rule misses four, all low. The twin accounts match on every
  gateway column.
* Retry attempts and billed operations are independent of every main-call record.
