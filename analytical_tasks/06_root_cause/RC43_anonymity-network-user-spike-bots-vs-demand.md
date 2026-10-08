# RC43 — Estimated users from one country jumped fivefold overnight: a surge in circumvention demand, or automated clients?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Fake-user inflation of active-user metrics (bot sign-ups inflating DAU, scripted clients inflating installs, crawler traffic inflating sessions), where the estimator's assumptions break for non-human clients |
| Domain | Internet freedom / network measurement |
| Task shape | 18 · Hypotheses versus evidence (genuine circumvention demand, automated clients, measurement artefact → evidence lines: bridge vs relay users, pluggable-transport use, bandwidth per user, cross-country synchrony; the explanation the report adopts) |
| Core method | User estimates are derived from directory requests under an assumed requests-per-user rate; automated clients that bootstrap repeatedly or never browse break that assumption. Evidence lines: whether the rise is in directly connecting (relay) users or bridge users; whether pluggable transports grew; whether relay bandwidth used rose with users; whether the same jump appears simultaneously in many countries; whether the jump is a step on one day; classify with a deterministic rule |
| Analytical stump | The daily-user estimate is a model output, not a count of people. A fivefold step in one day, with no change in bridge or transport use and almost no change in bandwidth, is the signature of automated clients (botnets have done exactly this), not of people seeking to circumvent censorship, who would use bridges and transports and generate traffic. Treating the estimate as a headcount produces a policy story from an artefact |
| Primary sources | Tor Metrics — estimated users by country (relay and bridge), bridge users by pluggable transport, relay bandwidth history, censorship anomaly indicators |

## 1. The real-world situation

A digital-rights NGO drafting its annual report saw Tor Metrics' estimated daily users from one country rise from about 40,000 to 200,000 within a
week of a contested election. The draft attributed the surge to citizens circumventing new censorship. A reviewer warned that similar jumps in the
past were caused by botnets using Tor for command-and-control. The NGO needs to decide what it can publish.

## 2. The decision (one deterministic recommendation)

**The explanation the report adopts — genuine circumvention demand, automated clients, or inconclusive — from the evidence grid, with each line's
statistic.**

Rules (research memo):

* Data: Tor Metrics CSVs for the memo's country and window (60 days before the jump to 60 days after): relay users, bridge users, bridge users by
  transport; global relay users by country (all countries) for synchrony; relay bandwidth history (global, as no per-country bandwidth exists).
* Jump date: the day with the largest one-day increase in relay users in the window.
* Evidence lines:
  * E1 composition: share of the increase (post 14-day mean − pre 14-day mean) that is relay (direct) users; automated if ≥ 90%.
  * E2 transports: bridge users via pluggable transports change by < 20%; automated if true.
  * E3 bandwidth: global relay bandwidth used rises by < 2% while global relay users rise by ≥ 10%; automated if true.
  * E4 synchrony: ≥ 10 other countries show a ≥ 50% relay-user increase within ± 3 days of the jump date; automated if true.
  * E5 step shape: ≥ 80% of the increase occurs within 2 days; automated if true.
* Demand lines (each true supports genuine demand): bridge users rise ≥ 50%; transport users rise ≥ 50%; censorship anomaly flagged for the country
  in the window.
* Adopt "automated clients" if ≥ 4 automated lines hold and ≤ 1 demand line holds; "genuine demand" if ≥ 2 demand lines hold and ≤ 1 automated line
  holds; otherwise "inconclusive".

## 3. Why capable analysts get it wrong

* The user estimate is presented as a headcount.
* The timing coincides with a plausible political cause.
* Bridge and transport metrics are separate downloads.
* Synchrony across countries is visible only in the all-country file.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `userstats-relay-country.csv` | CSV | ~800k (country × day) | Tor Metrics | CC0 (Tor Metrics data; verify) | Relay users, all countries |
| 2 | `userstats-bridge-country.csv` | CSV | ~800k | Tor Metrics | CC0 | Bridge users |
| 3 | `userstats-bridge-transport.csv` | CSV | ~50k | Tor Metrics | CC0 | Users by pluggable transport |
| 4 | `bandwidth.csv` | CSV | ~5k | Tor Metrics | CC0 | Relay bandwidth advertised and used |
| 5 | `userstats-censorship-events.csv` | CSV | ~800k | Tor Metrics | CC0 | Anomaly indicators |
| 6 | `tor_user_estimation_tech_report.pdf` | PDF | — | Tor Project technical report | CC BY 3.0 (verify) | How users are estimated |
| 7 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2, country, window |
| 8 | `ngo_draft_section.pdf` | PDF | — | Task author | — | The circumvention narrative |

## 5. Deterministic solution path

1. Extract the country's series and the all-country file for the window; find the jump date.
2. Compute E1–E5 and the demand lines.
3. Apply the decision rule; contrast with the draft.

## 6. Wrong paths (method errors, not misreadings)

**A — estimate as headcount.** Narrative adopted without checking the estimator's assumptions.

**B — relay users only.** Bridges and transports, where censorship circumvention shows up, are ignored.

**C — country in isolation.** A global bot event looks like a local surge.

**D — monthly averages.** The step shape and timing are blurred.

## 7. Why the stump is analytical, not semantic

All lines are numeric thresholds on public series. The trap is treating a model-based estimate as a measurement when its behavioural assumption
fails.

## 8. Draft task prompt (prose)

> Our draft report says Tor use surged fivefold after the election because of censorship. Evaluate the research memo's evidence lines and tell me which
> explanation the data support. Provide `user_spike_evidence.csv` (line: statistic, threshold, holds?), `user_spike_panels.png`, and a one-page
> `report_language_decision.pdf`.

## 9. Deliverables

* `user_spike_evidence.csv` — automated and demand lines with statistics.
* `user_spike_panels.png` — relay, bridge, transport and bandwidth series with the jump date; synchrony map inset.
* `report_language_decision.pdf` — adopted explanation and suggested wording.

## 10. Where 25+ rubric criteria come from

* Jump date: 1.
* E1–E5 statistics and outcomes: 10.
* Demand lines (3) statistics and outcomes: 6.
* Decision rule applied: 2.
* Synchrony country list: 2.
* Contrast and wording: 2.
* Chart elements: 2+.

## 11. Golden-output checklist

* 14-day pre/post means; jump-date rule.
* Global bandwidth vs global users for E3.
* Decision thresholds as specified.

## 12. Build notes (scope tuning)

* Use a documented bot-driven jump (e.g., the 2013 global spike) for the chosen country, aligned with a real political event in the narrative only
  if one occurred; otherwise frame the NGO's trigger as "new blocking reports". Confirm ≥ 4 automated lines hold.
