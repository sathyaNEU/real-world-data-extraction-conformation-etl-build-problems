# task249 submission

## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: a regional air research centre's 36 low-cost ozone nodes, each read against the regional network's four reference analysers for drift in its span).
**Analytical objective:** Data Quality Monitoring & Alerting (which nodes' ozone data have drifted outside the quality plan's span band, and so which nodes go on the pull list for recalibration at the June 2028 round).

## 1. Final Recommendation

**Take 8 nodes down for the bench at the June round: OZ06, OZ17, OZ21, OZ25, OZ29, OZ32, OZ33, OZ34.**

OZ06 (Alcorna), OZ17 (Villarejo de Mencía), OZ21 (Navalcuerno), OZ25 (Hontanar de la Vega), OZ32 (Santa Cruz de Alcorna) read low and OZ29 (Villanueva de Alcorna), OZ33 (Campillo de Mencía), OZ34 (Campillo de Mencía) read high: each node's span over the eight weeks to 31 May 2028 (6 April to 31 May, local time) lies outside 0.85 to 1.15. The other 28 nodes stay up and get the inlet cleaning.

Read over every hour of the eight weeks, the hill villages' nodes mislead: at night the plain's ozone is lost under the surface inversion while Navalcuerno, Santa Cruz de Alcorna, Campillo de Mencía and Quintanar de Alcorna stand above it and keep theirs, so their hourly spread is narrower than the analysers' for reasons that are not the head's. Every all-hours comparison reads a healthy hill node low and a hill node drifted high as healthy: the slope on paired hours against each node's nearest analyser gives 9 nodes (OZ06, OZ17, OZ21, OZ22, OZ25, OZ31, OZ32, OZ35, OZ36), and the spreads over all hours, which correct that slope's attenuation, give 9 (OZ06, OZ17, OZ21, OZ22, OZ25, OZ29, OZ31, OZ32, OZ36). In the convective afternoon the comarca shares one ozone, so each node's span is read on the hours starting 12:00 to 17:00 local, against the four analysers' pooled hours over the same afternoons.

## 2. Critical Components

1. The span is read against the regional network's four analysers (QA plan v3, sections 4 and 5) on the afternoon hours (12:00 to 17:00 local starts): the standard deviation of the node's accepted hourly ozone over those hours divided by the standard deviation of the analysers' pooled provisional hours over the same hours, both in ppb.
2. Over all hours the analysers' paired slopes run **0.88 to 0.95** while their spreads agree within **0.005**; the hill nodes' all-hours spreads fall below their afternoon spreads.
3. **8** nodes lie outside the band: **5** below 0.85 and **3** above 1.15.

## 3. Step-by-Step Solution

1. Node export: records sent twice after a link drop counted once (the latest received), OZ19B's records read as OZ19's (maintenance log, 9 to 25 January 2028), accepted readings by each node's firmware (status 0 before its 4.2 date in the maintenance log; status 0 or 1 from it, firmware 4.2 release note), OZN-B half-hours averaged into hours.
2. Window: the hours starting 6 April 2028 00:00 to 31 May 2028 23:00 local time (Europe/Madrid), 22:00 UTC on 5 April to 21:00 UTC on 31 May.
3. Analysers: the provisional release, P-flagged hours with a value; hora is the hour ending, UTC+1 (station sheet); micrograms per cubic metre to ppb over 1.996 (20 degrees C).
4. Span: on the window's hours starting 12:00 to 17:00 local, each node's standard deviation of its accepted hourly ozone over the standard deviation of the four analysers' pooled hours; outside 0.85 to 1.15 goes on the list.
5. Data capture (QA plan section 6): per node, the local hours from 1 November 2027 00:00 to 31 January 2028 24:00 (CET, UTC+1) with at least one accepted reading, steps 1's handling of duplicates, OZ19B and firmware.

## 4. Deliverable Answers

### ozone_nodes_june_2028_round.xlsx

**Pull list:** OZ06 (low), OZ17 (low), OZ21 (low), OZ25 (low), OZ29 (high), OZ32 (low), OZ33 (high), OZ34 (high); 8 nodes.

**Hours with an accepted reading, 1 November 2027 to 31 January 2028:**

| Node | Municipality | Hours |
|---|---|---|
| OZ01 | Alcorna | 2,144 |
| OZ02 | Alcorna | 2,141 |
| OZ03 | Alcorna | 2,161 |
| OZ04 | Alcorna | 2,142 |
| OZ05 | Alcorna | 2,152 |
| OZ06 | Alcorna | 2,121 |
| OZ07 | Alcorna | 2,145 |
| OZ08 | Alcorna | 2,159 |
| OZ09 | Alcorna | 2,087 |
| OZ10 | Alcorna | 2,154 |
| OZ11 | Torralba del Campo | 2,145 |
| OZ12 | Torralba del Campo | 2,061 |
| OZ13 | Torralba del Campo | 2,153 |
| OZ14 | Torralba del Campo | 2,153 |
| OZ15 | Torralba del Campo | 2,134 |
| OZ16 | Villarejo de Mencía | 2,144 |
| OZ17 | Villarejo de Mencía | 2,117 |
| OZ18 | Villarejo de Mencía | 2,141 |
| OZ19 | Villarejo de Mencía | 2,104 |
| OZ20 | Villarejo de Mencía | 2,138 |
| OZ21 | Navalcuerno | 2,130 |
| OZ22 | Navalcuerno | 2,164 |
| OZ23 | Valdeolmos del Llano | 2,144 |
| OZ24 | Valdeolmos del Llano | 2,094 |
| OZ25 | Hontanar de la Vega | 2,142 |
| OZ26 | Hontanar de la Vega | 2,164 |
| OZ27 | Fresnedilla del Campo | 2,149 |
| OZ28 | Fresnedilla del Campo | 2,031 |
| OZ29 | Villanueva de Alcorna | 2,148 |
| OZ30 | Villanueva de Alcorna | 2,143 |
| OZ31 | Santa Cruz de Alcorna | 2,158 |
| OZ32 | Santa Cruz de Alcorna | 2,138 |
| OZ33 | Campillo de Mencía | 2,142 |
| OZ34 | Campillo de Mencía | 2,129 |
| OZ35 | Quintanar de Alcorna | 2,088 |
| OZ36 | Quintanar de Alcorna | 2,135 |

### june_2028_pull_list.pdf

The list as above (OZ06, OZ17, OZ21, OZ25, OZ32 reading low; OZ29, OZ33, OZ34 reading high), and a chart of every node's span against the band of 0.85 to 1.15, the eight nodes outside it marked.
