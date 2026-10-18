"""task247 figures and write-up: every figure the goldens, figures.json and submission.md carry, computed once from the
shipped pack (solve.py), and the write-up drafted from them."""
import datetime as dt
import json
import os

import numpy as np
import pandas as pd

import params as P
import solve

WORD = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
        9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen"}


def _list(vals):
    vals = list(vals)
    return ", ".join(vals[:-1]) + " and " + vals[-1] if len(vals) > 1 else vals[0]


def repeat_runs(target, F):
    """runs of a wide colony written on consecutive metres with the same genus, diameter and condition, by observer"""
    df = pd.read_csv(os.path.join(target, F["survey"]))
    df = df[(df.sheet == "S") & (df.max_diameter_cm >= 100)]
    runs = {}
    for (site, tr, sh, who), g in df.groupby(["site_code", "transect", "sheet", "observer"]):
        g = g.sort_values(["metre", "line"])
        prev = []
        for r in g.itertuples(index=False):
            key = (r.genus, r.max_diameter_cm, r.condition)
            if any(k == key and m == r.metre - 1 for k, m in prev):
                runs[who] = runs.get(who, 0) + 1
            prev.append((key, r.metre))
    wide = df.groupby("observer").size().to_dict()
    return runs, wide


def gps_offsets(target, F):
    """for each trip, the hours between the logged retrieval time and the logger's own step out of the water (the first
    reading of the cooler on deck): the reading-to-reading jump nearest the retrieval"""
    dep = pd.read_csv(os.path.join(target, F["deployments"]), dtype={"serial": str})
    rd = pd.read_csv(os.path.join(target, F["readings"]), dtype={"serial": str})
    rd["t"] = pd.to_datetime(rd.datetime_local)
    out = {}
    for r in dep.itertuples(index=False):
        if not isinstance(r.retrieved, str):
            continue
        z = pd.Timestamp(r.retrieved)
        x = rd[(rd.serial == r.serial) & (rd.t >= z - pd.Timedelta(hours=9)) & (rd.t <= z + pd.Timedelta(hours=3))]
        if len(x) < 4:
            continue
        x = x.sort_values("t")
        jumps = x.temperature_c.diff().values[1:]
        k = int(np.argmax(jumps))
        step = x.t.values[k + 1]
        lag = (z - pd.Timestamp(step)).total_seconds() / 3600.0
        trip = (r.retrieved_from, z.strftime("%Y-%m"))
        out.setdefault(trip, []).append(lag)
    return {"%s %s" % k: [round(min(v), 2), round(max(v), 2), len(v)] for k, v in sorted(out.items(), key=lambda kv: kv[0][1])}


def figures(target, F):
    pk, b, rows = solve.solve(target, F)
    ru, c = pk.rungs()
    var = pk.variants(b)
    bt = pk.backtest(b)
    S = pk.survey()
    H = pk.logger_hours()
    decl_dhw = {}
    wb = pd.read_excel(os.path.join(target, F["bulletins"]), header=3)
    wb = wb[(wb["Analysis day"] >= solve.SEASON[0].isoformat()) & (wb["Analysis day"] <= solve.SEASON[1].isoformat())]
    for code in pk.codes:
        decl_dhw[code] = float(wb[wb["Site"] == code]["DHW"].max())
    sites = []
    for k, r in enumerate(rows):
        vals = [var[n][k] for n in var] + [r["dhw"]]
        sites.append(dict(code=r["site"], name=r["name"], region=r["region"], declared=r["declared"],
                          declared_dhw=round(decl_dhw[r["site"]], 1), dhw=r["dhw_round"], dhw_exact=round(r["dhw"], 2),
                          dhw_range=[round(min(vals), 2), round(max(vals), 2)], level=r["level"], verdict=r["verdict"],
                          survey=r["level"] == "Alert Level 2",
                          prevalence=round(S[r["site"]][0], 1), colonies=S[r["site"]][1], hours=H[r["site"]]))
    call = [s["code"] for s in sites if s["survey"]]
    rung_lists = {k: [pk.codes[i] for i in range(len(pk.codes)) if v[i] >= P.AL2] for k, v in ru.items()}
    rung_dhw = {k: [round(x, 2) for x in v] for k, v in ru.items()}
    runs, wide = repeat_runs(target, F)
    return dict(call=call, count=len(call), sites=sites, clear_sky=round(b, 2), clear_sky_exact=round(b, 4),
                rungs=rung_lists, rung_dhw=rung_dhw, constants=dict(b_fill=round(c["b_fill"], 3),
                                                                    b_all=round(c["b_all"], 3), k1=round(c["k1"], 2)),
                backtest={k: dict(rmse=round(v[0], 3), hot_mean=round(v[1], 3), days=v[2], hot_days=v[3])
                          for k, v in bt.items()},
                repeats=dict(runs=runs, wide=wide, total=sum(runs.values())), gps=gps_offsets(target, F),
                hot_low={k: round(-v[1], 3) for k, v in bt.items()}, hot_low_2dp={k: round(-v[1], 2) for k, v in bt.items()},
                conventions=dict(overlap_years=[2018, 2026], hot_anomaly_c=0.6, kelvin=273.15, window_days=P.WINDOW,
                                 wide_colony_cm=100, small_colony_cm=10, depth_band_m=2, gps_hours=5,
                                 hotspot_min_c=P.HS_MIN, levels=[P.AL1, P.AL2]))


def write_figures(path, fig):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")


def _site(fig, code):
    return next(s for s in fig["sites"] if s["code"] == code)


def golden_content(fig):
    sites = fig["sites"]
    on = [s for s in sites if s["survey"]]
    raised = [s for s in on if s["verdict"] == "raises"]
    kept = [s for s in on if s["verdict"] == "confirms"]
    up1 = [s for s in sites if s["verdict"] == "raises" and s["level"] == "Alert Level 1"]
    paras = [
        "<b>The November survey goes to %s sites: %s.</b> Each will reach Alert Level 2 for the 2027 season on the "
        "reprocessed record, with a season maximum of %s degree Celsius weeks. %s were declared at Alert Level 2 in the "
        "bulletins and are confirmed; %s were declared at Alert Level 1 and are raised." % (
            WORD[len(on)], _list(["%s %s" % (s["code"], s["name"]) for s in on]),
            _list(["%d (%s)" % (s["dhw"], s["code"]) for s in on]),
            _list([s["code"] for s in kept]), _list([s["code"] for s in raised])),
        "The southern sites' heat came under almost unbroken cloud from mid-August into September, and on a day "
        "without a satellite observation the near-real-time analysis lets the last observed anomaly fade toward the "
        "climatology, so the bulletins counted few HotSpots there. The estimate takes the analysis's clear-sky warm difference (%.2f degrees "
        "Celsius against the reprocessed record, 2018 to 2026) out of the observed days and fills every other day from "
        "the observed days either side, as the reprocessed analysis will with the passes and in situ records that came "
        "later. Over 2018 to 2026 that refill reproduces the reprocessed record on the days the analysis did not observe "
        "to %.3f degrees (root mean square), against %.3f for the record corrected by its mean differences." % (
            fig["clear_sky"], fig["backtest"]["refill"]["rmse"], fig["backtest"]["flag"]["rmse"]),
        "%s more sites rise from no alert to Alert Level 1 (%s); no site is lowered. The 2023 survey baseline and the "
        "loggers' hours at or above each site's maximum monthly mean are in the workbook." % (
            WORD[len(up1)].capitalize(), _list(["%s %s" % (s["code"], s["name"]) for s in up1])),
    ]
    return dict(sites=sites, call=fig["call"], paras=paras, clear_sky=fig["clear_sky"], backtest=fig["backtest"],
                title="%s sites for the November post-bleaching survey" % WORD[len(on)].capitalize(),
                chart_title="%s sites reach Alert Level 2; the bulletins declared %s" % (
                    WORD[len(on)].capitalize(), WORD[len(kept)]),
                footnote="Declared: the highest DHW in the season's weekly bulletins (near-real-time analysis). Expected: "
                         "the season maximum the reprocessed record will give, from the near-real-time observed days "
                         "less the clear-sky difference with the other days filled between them. Alert Level 1 at 4 and "
                         "Alert Level 2 at 8 degree Celsius weeks (methods note v3, sections 3 to 6).")


def submission(fig):
    sites = fig["sites"]
    on = [s for s in sites if s["survey"]]
    raised = [s for s in on if s["verdict"] == "raises"]
    kept = [s for s in on if s["verdict"] == "confirms"]
    up1 = [s for s in sites if s["verdict"] == "raises" and s["level"] == "Alert Level 1"]
    R = fig["rungs"]
    bt = fig["backtest"]
    nm = {s["code"]: s["name"] for s in sites}
    lines = []
    w = lines.append
    w("# task247 submission")
    w("")
    w("## Tags")
    w("")
    w("**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance: a reef station's coral "
      "bleaching heat-stress watch on near-real-time and reprocessed satellite sea surface temperature).")
    w("**Analytical objective:** Data Quality Monitoring & Alerting (which reef sites' 2027 alert levels, declared "
      "weekly on the near-real-time record, stand on the reprocessed record of reference, and so which sites the "
      "November post-bleaching survey visits).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Send the November post-bleaching survey to %s sites: %s.**" % (
        WORD[len(on)], _list(["%s %s" % (s["code"], s["name"]) for s in on])))
    w("")
    w("Their expected 2027 season maxima on the reprocessed record are %s degree Celsius weeks, all at Alert Level 2: "
      "%s confirm the bulletins' Alert Level 2 and %s raise their declared Alert Level 1." % (
          _list(["%d" % s["dhw"] for s in on]), _list([s["code"] for s in kept]), _list([s["code"] for s in raised])))
    w("")
    w("Not the bulletins' %s (%s), which leave out the southern sites: on every cloud-filled day the near-real-time "
      "analysis let the last observed anomaly fade toward the climatology, and under the August cloud over the south "
      "that took most of their HotSpots out. Not the %s a correction by the past mean differences of observed "
      "and filled days keeps (%s): on hot filled days the analysis reads %.2f degrees low, which the mean difference of "
      "all filled days (%+.3f) does not restore." % (
          WORD[len(R["as issued"])], _list(R["as issued"]), WORD[len(R["flag"])], _list(R["flag"]),
          -bt["flag"]["hot_mean"], fig["constants"]["b_fill"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. The near-real-time analysis runs **%.2f degrees Celsius** warm of the reprocessed record on the days it "
      "observed, 2018 to 2026." % fig["clear_sky"])
    w("2. On the 2018 to 2026 days it did not observe, refilling each gap from the observed days either side reproduces "
      "the reprocessed record to **%.3f degrees** root mean square and **%+.3f** on hot days (anomaly above 0.6), against "
      "**%.3f** and **%+.3f** for the record corrected by the mean differences of observed and filled days." % (
          bt["refill"]["rmse"], bt["refill"]["hot_mean"], bt["flag"]["rmse"], bt["flag"]["hot_mean"]))
    w("3. The bulletins' declared levels for the season: **%s**." % "; ".join(
        "%s %s" % (s["code"], s["declared"]) for s in sites))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    steps = [
        "Near-real-time extract: the latest issue of each pixel and day (a later issue replaces the earlier, user guide "
        "section 3), the flag read by each row's version (from version 3.2, 2 observed and 1 not; before, 1 and 0), "
        "pixels to sites by the register; no analysis was issued for 17 June 2027.",
        "Reprocessed record in kelvin less 273.15; on the 2018 to 2026 days the near-real-time analysis observed it "
        "runs %.2f degrees warm of the reprocessed record (%.4f)." % (fig["clear_sky"], fig["clear_sky_exact"]),
        "On a day it did not observe, the near-real-time value is the climatology plus the last observed anomaly fading "
        "day by day, so it understates a lasting warm anomaly: on 2018 to 2026 hot days it did not observe it reads "
        "%.3f low, and %.3f after the flag-mean correction, while refilling from the observed days either side leaves "
        "%+.3f (root mean square %.3f against %.3f)." % (-bt["as issued"]["hot_mean"], -bt["flag"]["hot_mean"],
                                                          bt["refill"]["hot_mean"], bt["refill"]["rmse"],
                                                          bt["flag"]["rmse"]),
        "Each site's 2027 record: the observed days less %.2f, every other day (not observed, or not issued) by "
        "straight-line interpolation of the anomaly against the climatology file between the observed days either "
        "side; HotSpots of 1.0 degree or more above the register's maximum monthly mean, DHW the 84-day sum over 7, the "
        "season maximum over 1 June to 31 October (methods note sections 3 and 4)." % fig["clear_sky"],
        "Levels at 4 and 8 and each site's verdict against the highest level its season bulletins gave (sections 5 and "
        "6): %s confirmed, %s raised, none lowered." % (WORD[sum(s["verdict"] == "confirms" for s in sites)],
                                                       WORD[sum(s["verdict"] == "raises" for s in sites)]),
        "The 2023 survey: sheets S, transects within 2 m of the register's survey depth, annex genera of 10 cm or more; "
        "a colony of 100 cm or more written on consecutive metres of one sheet with the same genus, diameter and "
        "condition is one colony (the protocol records each colony once: %s wrote %d such repeats, the other observers "
        "none); prevalence is pale, partly bleached and bleached over all colonies." % (
            _list(sorted(fig["repeats"]["runs"])), sum(fig["repeats"]["runs"].values())),
        "Loggers: each logger's readings while it was in the water, the log's times being the boat's GPS (the Cozumel "
        "II's showed UTC on its trips of August 2025 and April 2026, five hours ahead of the loggers' local clocks: its "
        "loggers leave the water five hours before the logged time), June to October 2024 to 2026 in local time, one "
        "reading an hour, at or above the register's maximum monthly mean.",
        "The survey list is the %s sites at Alert Level 2." % WORD[len(on)],
    ]
    for j, st in enumerate(steps, 1):
        w("%d. %s" % (j, st))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### reef_heat_stress_2027.xlsx")
    w("")
    w("1. Each site's expected 2027 season maximum on the reprocessed record (whole degree Celsius weeks), its alert "
      "level and its verdict against the declared level, 16 rows in the register's order:")
    for s in sites:
        w("   - %s %s: %d; %s; %s (declared %s)" % (s["code"], s["name"], s["dhw"], s["level"], s["verdict"],
                                                  s["declared"]))
    w("2. Each site's bleaching prevalence in the 2023 survey (per cent to one decimal) and the colonies it rests on:")
    for s in sites:
        w("   - %s: %.1f, %d colonies" % (s["code"], s["prevalence"], s["colonies"]))
    w("3. Each site's hours at or above its maximum monthly mean at its logger, June to October 2024 to 2026:")
    for s in sites:
        w("   - %s: %d" % (s["code"], s["hours"]))
    w("")
    w("### survey_list_note_2027.pdf")
    w("")
    w("- The survey list, %s sites (%s), and a chart of each site's declared and expected season maximum against the "
      "Alert Level 1 and Alert Level 2 lines, the raised sites marked." % (WORD[len(on)], _list([s["code"] for s in on])))
    w("")
    return "\n".join(lines)
