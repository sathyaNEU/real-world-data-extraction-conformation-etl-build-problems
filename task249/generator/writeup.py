"""figures.json and submission.md, drafted from the solved pack."""
import json
import os
import nodes as N
import params as P
import solve

STATION = {c: n.replace("Mencia", "Mencía") for c, n, _, _ in P.ANALYSERS}


def figures(target, F):
    pk, sp, pull = solve.solve(target, F)
    pairs = solve.analyser_pairs(pk)
    slopes = [v[0] for v in pairs.values()]
    ratio = max(abs(v[1] - 1) for v in pairs.values())
    ols = pk.pulled(pk.spans("ols_h", hours=None))
    allh = pk.pulled(pk.spans("dm", hours=None))
    G = {
        "span": sp, "pull": pull, "town": {c: m.replace("Mencia", "Mencía") for c, m, _, _ in N.NODES},
        "capture": pk.ask_a(), "md8": pk.ask_b(),
        "pairs": (min(slopes), max(slopes), ratio), "ols_n": len(ols), "ols_pull": ols,
        "rom_pull": pk.pulled(pk.spans("rom", hours=None)), "olsd_pull": pk.pulled(pk.spans("ols_d", hours=None)),
        "allh_pull": allh,
    }
    return pk, G


def write_figures(path, G):
    out = {
        "call": "%d nodes to the bench at the June 2028 round" % len(G["pull"]),
        "pull_list": {c: G["pull"][c] for c in sorted(G["pull"])},
        "pull_count": len(G["pull"]), "low_count": sum(v == "low" for v in G["pull"].values()),
        "high_count": sum(v == "high" for v in G["pull"].values()),
        "band": [0.85, 1.15], "window": "6 April to 31 May 2028 (local)",
        "analyser_pair_slopes": [round(G["pairs"][0], 2), round(G["pairs"][1], 2)],
        "analyser_spread_agreement": round(G["pairs"][2], 3), "allhours_list": sorted(G["allh_pull"]), "allhours_count": len(G["allh_pull"]), "afternoon_hours": [12, 17],
        "paired_slope_list": {c: G["ols_pull"][c] for c in sorted(G["ols_pull"])}, "paired_slope_count": G["ols_n"],
        "capture_hours": G["capture"], "capture_total": sum(G["capture"].values()), "quarter_hours": 2208,
"ppb_to_ugm3": 1.996, "conventions": [36, 4, 8, 2027, 2028, 4.2, 19, 25, 9],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)


def submission(G):
    pull = sorted(G["pull"])
    low = [c for c in pull if G["pull"][c] == "low"]
    high = [c for c in pull if G["pull"][c] == "high"]
    nm = lambda c: "%s (%s)" % (c, G["town"][c])
    olsx = sorted(set(G["ols_pull"]) - set(pull))
    olsm = sorted(set(pull) - set(G["ols_pull"]))
    cap = "\n".join("| %s | %s | %s |" % (c, G["town"][c], format(G["capture"][c], ",")) for c in N.CODES)
    return f"""# task249 submission

## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: a regional air research centre's 36 low-cost ozone nodes, each read against the regional network's four reference analysers for drift in its span).
**Analytical objective:** Data Quality Monitoring & Alerting (which nodes' ozone data have drifted outside the quality plan's span band, and so which nodes go on the pull list for recalibration at the June 2028 round).

## 1. Final Recommendation

**Take {len(pull)} nodes down for the bench at the June round: {", ".join(pull)}.**

{", ".join(nm(c) for c in low)} read low and {", ".join(nm(c) for c in high)} read high: each node's span over the eight weeks to 31 May 2028 (6 April to 31 May, local time) lies outside 0.85 to 1.15. The other 28 nodes stay up and get the inlet cleaning.

Read over every hour of the eight weeks, the hill villages' nodes mislead: at night the plain's ozone is lost under the surface inversion while Navalcuerno, Santa Cruz de Alcorna, Campillo de Mencía and Quintanar de Alcorna stand above it and keep theirs, so their hourly spread is narrower than the analysers' for reasons that are not the head's. Every all-hours comparison reads a healthy hill node low and a hill node drifted high as healthy: the slope on paired hours against each node's nearest analyser gives {G["ols_n"]} nodes ({", ".join(sorted(G["ols_pull"]))}), and the spreads over all hours, which correct that slope's attenuation, give {len(G["allh_pull"])} ({", ".join(sorted(G["allh_pull"]))}). In the convective afternoon the comarca shares one ozone, so each node's span is read on the hours starting 12:00 to 17:00 local, against the four analysers' pooled hours over the same afternoons.

## 2. Critical Components

1. The span is read against the regional network's four analysers (QA plan v3, sections 4 and 5) on the afternoon hours (12:00 to 17:00 local starts): the standard deviation of the node's accepted hourly ozone over those hours divided by the standard deviation of the analysers' pooled provisional hours over the same hours, both in ppb.
2. Over all hours the analysers' paired slopes run **{G["pairs"][0]:.2f} to {G["pairs"][1]:.2f}** while their spreads agree within **{G["pairs"][2]:.3f}**; the hill nodes' all-hours spreads fall below their afternoon spreads.
3. **{len(pull)}** nodes lie outside the band: **{len(low)}** below 0.85 and **{len(high)}** above 1.15.

## 3. Step-by-Step Solution

1. Node export: records sent twice after a link drop counted once (the latest received), OZ19B's records read as OZ19's (maintenance log, 9 to 25 January 2028), accepted readings by each node's firmware (status 0 before its 4.2 date in the maintenance log; status 0 or 1 from it, firmware 4.2 release note), OZN-B half-hours averaged into hours.
2. Window: the hours starting 6 April 2028 00:00 to 31 May 2028 23:00 local time (Europe/Madrid), 22:00 UTC on 5 April to 21:00 UTC on 31 May.
3. Analysers: the provisional release, P-flagged hours with a value; hora is the hour ending, UTC+1 (station sheet); micrograms per cubic metre to ppb over 1.996 (20 degrees C).
4. Span: on the window's hours starting 12:00 to 17:00 local, each node's standard deviation of its accepted hourly ozone over the standard deviation of the four analysers' pooled hours; outside 0.85 to 1.15 goes on the list.
5. Data capture (QA plan section 6): per node, the local hours from 1 November 2027 00:00 to 31 January 2028 24:00 (CET, UTC+1) with at least one accepted reading, steps 1's handling of duplicates, OZ19B and firmware.

## 4. Deliverable Answers

### ozone_nodes_june_2028_round.xlsx

**Pull list:** {", ".join(f"{c} ({G['pull'][c]})" for c in pull)}; {len(pull)} nodes.

**Hours with an accepted reading, 1 November 2027 to 31 January 2028:**

| Node | Municipality | Hours |
|---|---|---|
{cap}

### june_2028_pull_list.pdf

The list as above ({", ".join(low)} reading low; {", ".join(high)} reading high), and a chart of every node's span against the band of 0.85 to 1.15, the eight nodes outside it marked.
"""
