## Tags

**Domain:** Energy systems and utilities (grid reliability and outage analysis).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Kampvliet (VKF-KPV) comes out of the frequency containment reserve portfolio for the November 2026 delivery month and takes the month's re-prequalification slot.** Its realised response gain is 72 per cent of the gain its contract requires, 11 percentage points below Reiderland at 83 per cent. Not Zwartewater, which the undisturbed level puts furthest below contract, its recorded power at the last second before each episode at which the published frequency was still inside the dead band being its own programme unwinding a morning discharge through the deviation. Not Reiderland, which the period setpoint puts furthest below contract because its programme traverse is still running at the second the response is read.

## 2. Critical Components

1. Kampvliet's realised response gain is **72** per cent of contracted gain over **134** qualifying under-frequency episodes
2. The runner-up Reiderland is **83** per cent, a gap of **11** percentage points
3. Each site's programme traverse runs for a fixed span from the settlement period boundary, recovered from the settlement period boundaries at which the site held no reserve commitment: **90** seconds at Kampvliet and **300** seconds at Terborgh
4. **3** sites sit below the standard's 90 per cent tolerance

## 3. Step-by-Step Solution

1. Took every qualifying under-frequency episode from the published one-second frequency in system_frequency_1s_extracts.csv, at or below 49.920 Hz for 15 or more consecutive seconds per clause 2 of the reserve performance standard.
2. Scoped each episode to the sites contracted for that settlement period in fcr_block_commitments.csv and dropped the block parts the control platform event log records as withdrawn from reserve, leaving 911 site-episode pairs the archive carries a recording of the extreme second for.
3. Recovered each site's programme traverse from vkf_highres_archive.sqlite at the settlement period boundaries at which the site held no reserve commitment: the span from the boundary to the new setpoint in site_programme_15min.csv is a constant of the site's controller, 90 seconds at Kampvliet.
4. Took each site's delivered response at an episode's extreme second as its recorded power less its programme traverse at that second, over the deviation beyond the 10 mHz dead band and over its contracted gain, which is its contracted FCR capacity in asset_register.xlsx divided by 0.190 Hz per clause 2 of the technical conditions.
5. Averaged the per-episode ratios with equal weight for each site: Kampvliet 72 per cent, Reiderland 83 per cent, Hoogezand 88 per cent, Nieuwveen 91 per cent.
6. Ran the same episodes against the undisturbed level, each site's recorded power at the last second before the episode at which the published frequency was still inside the 10 mHz dead band, and against the period setpoint: the undisturbed level puts Zwartewater furthest below contract and the period setpoint puts Reiderland, so neither basis names Kampvliet for the slot, because each credits a site with whatever its own programme did during the deviation.
7. Applied clause 3 of the standard: 3 sites are outside the 90.0 per cent tolerance and the single monthly test slot goes to the site furthest below contract.
8. Recommended withdrawing Kampvliet for the November 2026 delivery month.

## 4. Deliverable Answers

### response_determination.md

1. Site withdrawn for the November 2026 delivery month: Kampvliet (VKF-KPV).
2. Its realised response gain: 72 per cent of contracted gain.
3. Runner-up: Reiderland (VKF-RDL) at 83 per cent.
4. Gap: 11 percentage points.

### site_response_scorecard.xlsx

1. Realised response gain, qualifying under-frequency episodes and whether the site falls below the 90 per cent tolerance, nine sites in gain order, gains to the nearest whole per cent and counts whole:
   - Kampvliet (VKF-KPV): 72 per cent, 134 episodes, below tolerance yes
   - Reiderland (VKF-RDL): 83 per cent, 152 episodes, below tolerance yes
   - Hoogezand (VKF-HGZ): 88 per cent, 152 episodes, below tolerance yes
   - Nieuwveen (VKF-NWV): 91 per cent, 111 episodes, below tolerance no
   - Dollardkust (VKF-DLK): 93 per cent, 144 episodes, below tolerance no
   - Oosterhout (VKF-OOS): 95 per cent, 39 episodes, below tolerance no
   - Meppelerdiep (VKF-MPD): 97 per cent, 30 episodes, below tolerance no
   - Zwartewater (VKF-ZWT): 99 per cent, 73 episodes, below tolerance no
   - Terborgh (VKF-TRB): 101 per cent, 76 episodes, below tolerance no
2. Realised response gain and episode count on the qualifying over-frequency episodes, nine sites in site order:
   - Dollardkust (VKF-DLK): 92 per cent, 20 episodes
   - Hoogezand (VKF-HGZ): 87 per cent, 150 episodes
   - Kampvliet (VKF-KPV): 73 per cent, 20 episodes
   - Meppelerdiep (VKF-MPD): none, 0 episodes
   - Nieuwveen (VKF-NWV): 89 per cent, 71 episodes
   - Oosterhout (VKF-OOS): 96 per cent, 15 episodes
   - Reiderland (VKF-RDL): 81 per cent, 20 episodes
   - Terborgh (VKF-TRB): 98 per cent, 66 episodes
   - Zwartewater (VKF-ZWT): 94 per cent, 69 episodes
3. Reserve capacity hours held available and the shortfall against commitment, six delivery blocks, MWh to one decimal place:
   - Block 1 (00:00-04:00): held available 542.0, shortfall 18.0
   - Block 2 (04:00-08:00): held available 1151.0, shortfall 17.0
   - Block 3 (08:00-12:00): held available 1407.1, shortfall 20.9
   - Block 4 (12:00-16:00): held available 352.9, shortfall 7.1
   - Block 5 (16:00-20:00): held available 1615.5, shortfall 26.5
   - Block 6 (20:00-24:00): held available 244.2, shortfall 7.8
4. Energy delivered above programme and below programme in the settlement periods the site held no delivery-block commitment for, nine sites in site order, MWh to one decimal place:
   - Dollardkust (VKF-DLK): above 22.0, below 46.8
   - Hoogezand (VKF-HGZ): above 8.2, below 18.6
   - Kampvliet (VKF-KPV): above 10.9, below 21.9
   - Meppelerdiep (VKF-MPD): above 9.8, below 16.1
   - Nieuwveen (VKF-NWV): above 10.9, below 28.0
   - Oosterhout (VKF-OOS): above 9.3, below 22.2
   - Reiderland (VKF-RDL): above 11.6, below 17.4
   - Terborgh (VKF-TRB): above 15.3, below 22.1
   - Zwartewater (VKF-ZWT): above 16.3, below 49.5
   - Portfolio: above 114.4, below 242.6 (each rounded once from the unrounded period sums per clause 5, so not the sum of the rounded rows)
5. Bar chart of the under-frequency realised gains by site on the Scorecard sheet, one bar per site in gain order, with the tolerance line drawn across at 90 per cent and the axis titled in per cent of contracted gain.
