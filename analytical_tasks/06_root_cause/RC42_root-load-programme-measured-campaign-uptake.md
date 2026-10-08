# RC42 — Which programme the root operators fund against doubled query load, when past campaigns show who actually acts

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · platform load and client behaviour |
| Mirrors | Load-reduction programmes at large platforms (Google, Cloudflare and Akamai resolver and API traffic, a mobile SDK multiplying calls, smart-TV firmware polling a CDN), where the programme with the biggest target is not the one that removes the most load, because past outreach shows which counterparties act and how much load they carry |
| Decision shape | Which of N root causes gets the fix: one programme this year, five aimed at five sources of root query growth |
| Committed call | Fund the negative-caching outreach to the 40 largest ISP resolvers, which takes 22.6B queries a day off the root next year, 1.79× the next programme |
| Gap · Pattern | Gap 4 (rule) at the decisive rung, Gap 2 (population) at rung 2 · measured #25 (each programme's effect measured from the pilot log's past campaigns, weighted by the adopters' load, instead of assumed), with measured #13 at rung 2 (signature shares validated on one letter's captures, applied to letters with different footprints) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #25 assumes an effect the log could measure · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Pilot log: the caucus's log of 23 past campaigns over six years (6 negative-caching outreach, 5 local-root, 4 firmware, 3 browser-vendor requests, 5 scrubbing contracts), each with its targeted sources and their root queries before and after |
| Driving force | Each programme's target is sized correctly once attack floods leave the probe signature and the one captured letter's signature shares are recalibrated to every letter's footprint. Sized at the adoption each sponsor expects, firmware outreach leads. But a programme removes only the load its counterparties actually take off, and the pilot log measured that in 23 past campaigns. Weighted by each adopter's pre-campaign root load, the effects are stable: firmware campaigns removed 12% of targeted leakage, local-root campaigns 20%, the browser vendor's changes 60% and negative-caching outreach 66%, because the largest resolvers are the ones that switch it on. Counting adopters instead of their load halves that last figure. On measured effects, negative-caching outreach takes 22.6B queries a day off the root. |

## 1. Situation

Daily queries to the root servers doubled in two years, to about 100B a day across the thirteen letters. The root operators' caucus can fund
one programme this year, aimed at one source of the growth: scrubbing contracts against attack floods, a request to the browser vendor to
remove its intranet-redirect probe, outreach to router makers whose firmware leaks local search suffixes, outreach to the 40 largest ISP
resolvers to switch on aggressive negative caching, or a campaign for local copies of the root zone at the 20 largest resolvers. The charter
funds the programme that takes the most daily queries off the root next year. Each sponsor has filed a proposal stating its target sources
and the adoption it expects, without a removal figure.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the per-letter metrics, the one letter's query-name captures, the source aggregates, the
  sponsors' proposals and the pilot log. The probes, the leaks and the floods are all real, and no one's reading of their own figures is
  overturned. The difficulty is how much each programme will actually remove.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the sponsors' expectations and every voice. Sized on its target at full adoption, firmware outreach still leads,
  and only the pilot log's measured effects change the order.
* **Instrument repair.** Suspect: only one letter publishes full query captures, so every signature share comes from one footprint. Repair:
  full captures at every letter, then a source classifier on every query. Rungs 0, 1 and 2 then all name firmware outreach (27.0), because
  the exact targets replace the scaled ones and the floods are classified at source; none names negative-caching outreach, which every lower
  rung sizes at its sponsor's expected adoption (4.6). The pilot log and the source aggregates are complete, and a campaign's realised removal
  is a load-weighted before-and-after construction that no row records, so the decisive construction is still needed.
* **Lens swap.** The naive measure is each programme's target. The answer measures what the targeted counterparties took off in past
  campaigns, weighted by their load: a different population (the adopters' load) at a different moment (after a campaign, not before it).

## 3. The driving force

A strong solver sizes each programme on its target. It moves the attack-day floods out of the probe signature with a robust spike filter,
because random-label floods look like probes. It sees that the one letter with full captures sits mostly in front of European and North
American desktops, and it recalibrates the signature shares by region to every letter's published source mix. Home-router leakage turns out
to be the largest junk pool, and firmware outreach leads at the 100% update rate its sponsor expects. But the pilot log holds 23 past
campaigns with their targeted sources' root queries before and after, and they disagree with every sponsor. Router makers' firmware reached
few devices, and only 12% of the targeted leakage went away. The browser vendor's past changes took a year to reach 60% of installs. Local
root copies were taken up by the smaller resolvers and removed 20%. Negative-caching outreach was taken up by only 30% of the resolvers
asked, but they were the largest ones, carrying 70% of the targeted load, and with 95% efficacy the effect was 66% in all six campaigns.
At measured effects, negative caching removes 22.6B queries a day and scrubbing 12.6B.

## 4. The ladder

| Rung | Construction | Names (daily root queries removed next year, billions) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each target from the captured letter's query-name signatures, scaled to all letters, at its sponsor's expected adoption | Browser request (30.0, 2.86× local root's 10.5) | The sponsors' own expectations on the only letter with full captures | The spike filter: on attack days random-label floods match the probe signature, and 15B of the probe target is floods |
| 1 | Hygiene of the floods: attack-day excess (30-day rolling median and three MADs) moved from the probe signature to the attack target | Scrubbing (22.8, 1.52× the browser's 15.0) | Every signature now reflects its source | The per-letter aggregates: the captured letter's footprint is two-thirds European and North American desktops, and the other twelve letters see far more ISP and home-router junk |
| 2 | Signature shares calibrated by region and re-weighted to each letter's published source mix, at the sponsors' expected adoption | Firmware outreach (27.0, 2.03× scrubbing's 13.3) | Every letter's footprint reflected, and the floods out | The pilot log: past firmware campaigns removed 12% of the leakage they targeted, and past negative-caching campaigns 66% |
| 3 | **Decisive:** each programme's removal at the effect its past campaigns realised, the drop in targeted sources' root queries weighted by each adopter's pre-campaign load | **Negative-caching outreach (22.6, 1.79× scrubbing's 12.6)**, 5th on rung 0 | — | — |

* **Position table.** Negative-caching outreach ranks 5th on rungs 0, 1 and 2 (3.5, 3.5 and 4.6) and leads only rung 3. Rung margins are
  2.86, 1.52, 2.03 and 1.79.
* **Discriminator dominance.** Firmware outreach carries a 22.4B lead over negative caching into rung 3 (27.0 against 4.6). The measured
  effects take 23.8B from one and give 18.0B to the other, a 41.8B swing, 1.86× the carried lead. The floor is 1.2×, so the edge has 1.55×
  headroom.
* **Partial correction priced (L3).** A solver who measures past campaigns by the share of resolvers that adopted rather than by their load
  puts negative caching at 9.7 and names scrubbing at 12.6, 1.30× ahead. One who measures every programme except firmware, where the router
  makers' announced update commitment stands in, names firmware outreach at 27.0, 1.19× ahead. Neither half names negative caching.
* **Grid.** Flood hygiene (off, on) × letter calibration (off, on) × effect (sponsors' expectation, adopter count share, load-weighted) gives
  12 cells. Only the load-weighted effect on calibrated targets names negative caching, with or without the flood hygiene. Every other cell
  names the browser, scrubbing or firmware outreach. The nearest is the load-weighted effect on uncalibrated targets with the floods left in,
  which names the browser by 1.04×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot log records campaigns and their sources' queries. No document says a programme should be sized on past
   realised effects, or that adopters must be weighted by their load.
2. **Reproduction numbers.** The load-weighted effect reproduces the realised removal of all 23 campaigns within 3%. The best rival, the
   share of targeted resolvers that adopted, reproduces 6, the campaigns whose adopters happened to be average-sized. The construction joins
   each adopter to its pre-campaign root load in the source aggregates, so it is not a parameter a solver can sweep.
3. **No arithmetic symptom.** The per-letter metrics, captures and source aggregates reconcile on every rung, and the targets partition the
   junk exactly.
4. **Not a row predicate.** A realised effect is a ratio of load changes across a campaign's sources, weighted by a join to their earlier
   load, and it enters as a multiplier on a different year's target.
5. **The enumeration is arithmetic.** No field states a programme's effect. Each one is computed from its campaigns.
6. **No cutover date.** The campaigns span six years, and the next year's removal is a product of a target and a measured effect, not a step
   at any date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The caucus's pilot log: 23 campaigns over six years, each with its targeted sources, its close date and those sources' daily root
  queries in the four weeks before and the four weeks after.
* **What it certifies, and what it pins.** The realised effect of each kind of programme: 0.66 for negative-caching outreach, 0.20 for local
  root, 0.60 for browser-vendor changes, 0.12 for firmware and 0.90 for scrubbing, each stable within 3% across its campaigns once weighted by
  load.
* **The numbers.** 23 of 23 for the load-weighted effect, 6 of 23 for the adopter count share, and none for the sponsors' expectations.
* **Twin pair.** Negative-caching campaigns C-2 and C-5 each asked 20 resolvers, each got 6 adopters, and each targeted 30B of junk a day.
  C-2 removed 19.9B and C-5 9.7B (2.06×), because C-2's adopters carried 70% of the targeted load and C-5's 34%. Only load weighting
  reproduces both.
* **Resemblance points at the decoy.** The planned firmware campaign most resembles the log's router campaign of two years ago, the largest
  in the log by devices reached.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The caucus charter: "The caucus funds the one programme that takes the most daily queries off the root servers in the next
  year." The pilot log's header: "A campaign's realised removal is the change in its targeted sources' daily root queries between the four
  weeks before and the four weeks after its close." The metric definitions fix each per-letter series.
* **Empirical pins.** The spike filter's window and threshold come from the metric definitions' guidance. The region signature shares come
  from the captured letter's per-region captures, and each letter's source mix from its published aggregates.
* **Voices.** Operator engineer: "It's the browser; look at the random labels." Security lead: "Half of this growth is attack floods."
  Router working-group chair: "Our survey found leaking suffixes on every home router we tested." Outreach coordinator: "Resolver operators
  never act on our letters."
* **Licensed wrong basis.** The charter records that the caucus's annual report sizes programmes by their target at full adoption, and the
  board will see this year's choice on that basis.

## 8. Determinism by construction

* **Targets.** The region signature shares and each letter's source mix are published to three decimals, and every target moves by under
  0.2B under any rounding.
* **Floods.** Every attack day sits more than six MADs above its rolling median, so the three-MAD threshold and any reasonable window find the
  same days.
* **Campaigns.** No two campaigns overlapped in time or shared a targeted source, and none closed within eight weeks of another, so every
  before-and-after window is clean.
* **Horizon.** Every campaign's effect was complete within four weeks of its close and held flat for the following year, so next year's
  removal is the target times the measured effect.
* **Maturity.** The last campaign closed ten weeks before the extract.

## 9. Prompt sketch and deliverables

> Root queries doubled in two years and the caucus can fund one programme this year. One of our engineers is sure the browser's probes are
> behind all of it. Tell me which programme we fund, in a sentence for the caucus, with the daily root queries each of the five would take
> off the servers next year, in billions to one decimal. Send `programme_case.xlsx`, a chart `removal_by_programme.png`, and a one-page
> `caucus_decision.pdf`.

* `programme_case.xlsx` — the five programmes on every construction, the IPv6 sheet (ask A), the response-size sheet (ask B) and the
  pilot-log back-test (ask C).
* `removal_by_programme.png` — for each programme, a bar of its target with an inner bar of what it removes at the measured effect, the
  sponsors' expectation as a marker, and a title naming the funded programme.
* `caucus_decision.pdf` — the named programme and why each other programme removes less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the thirteen letters, the IPv6 share of unique sources in the last month. *Device:* the
  unique-sources metric reports IPv4 addresses, IPv6 addresses and IPv6 /64 prefixes in separate fields, and the metric definitions count an
  IPv6 source as a /64. Using raw addresses overstates the IPv6 share three- to fivefold at letters that see privacy-addressed resolvers.
  Source counts never enter a target or an effect.
* **Ask B (device-carried).** For each letter, mean response size in bytes last quarter. *Device:* the size metric is a histogram in 16-byte
  buckets labelled by their lower bound, and the definitions take each bucket's midpoint. Using the labels understates every mean by 8 bytes.
* **Ask C (validity).** For each of the 23 campaigns, the realised removal beside what your construction gives.
* **Decoupling.** Clearing the measured effects or the letter calibration changes no figure in asks A or B.

## 11. Rubric arithmetic

13 letters (ask A) + 13 letters (ask B) + 23 campaigns (ask C) + the named programme, the five removal figures and the winning margin + 5
named chart parts + 3 files ≈ 64 criteria.

## 12. World-building constraints

* Calibrated targets (billions a day): attack floods 14, browser probes 10, router leakage 27, junk through the 40 ISP resolvers 34, all
  queries from the 20 largest resolvers 35. On the captured letter scaled up they are 9, 30, 10, 26 and 35, with 15 of the probe target being
  floods.
* Sponsors' expected adoption: scrubbing 95%, browser 100%, firmware 100%, negative caching 13.5% (15% of resolvers at 90% efficacy) and
  local root 30%.
* Measured effects: 0.90, 0.60, 0.12, 0.665 and 0.20. Negative-caching adopters are 30% of resolvers asked and 70% of their load.
* C-2 and C-5 are identical on resolvers asked, adopters and targeted junk, and their adopters carry 70% and 34% of the load.
* Every rung's leader leads by at least 1.15×, and the decisive edge is 1.86× the carried lead.
* Source-count fields and size histograms never touch targets, floods or campaign windows.
