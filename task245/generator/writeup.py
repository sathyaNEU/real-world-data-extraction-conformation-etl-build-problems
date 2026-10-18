"""task245 figures and write-up: every figure the goldens, figures.json and submission.md carry, computed once from the
shipped pack (solve.py), and the write-up drafted from them."""
import json

import numpy as np

import estim as E
import params as P
import solve

BEARING_HALF = 22.5
BEARING_HOURS = 6


def bearing(code):
    import sim
    st = P.STATIONS[P.CODES.index(code)]
    return sim.bearing_to_terminal(st[4], st[5])


def evidence(A, code):
    """the station's lost days and the wind: lost days, those with six or more hours whose reported wind direction lies
    within 22.5 degrees of the bearing to the terminal (calm and missing hours never count), and on its valid days with
    that wind its mean against the mean of the day's median of the other stations' valid daily means"""
    i = P.CODES.index(code)
    xv, valid = A["xv"], A["valid"]
    dm, vd = E.daily(xv, valid)
    phi = A["bearing"][code]
    off = np.abs(((A["theta_reported"] - phi + 180) % 360) - 180)
    on = (np.nan_to_num(off, nan=360.0) <= BEARING_HALF).reshape(P.DAYS, 24).sum(1) >= BEARING_HOURS
    lost = ~vd[i]
    o = [j for j in range(len(P.CODES)) if j != i]
    with np.errstate(all="ignore"):
        med = np.nanmedian(np.where(vd[o], dm[o], np.nan), 0)
    sel = vd[i] & on
    return dict(lost_days=int(lost.sum()), lost_bearing=int((lost & on).sum()),
                valid_bearing_share=round(100.0 * (vd[i] & on).sum() / vd[i].sum(), 1),
                bearing_station=round(float(np.mean(dm[i][sel])), 1), bearing_network=round(float(np.nanmean(med[sel])), 1),
                bearing_days=int(sel.sum()))


def figures(target, F):
    A = solve.answer(target, F)
    R = A["R"]
    wind = [k for k in R if k.startswith("wind")]
    no2, no2_naive = solve.no2_means(target, F), solve.no2_means(target, F, fits="none")
    dep, dep_lab = solve.deposition(target, F), solve.lab_rates(target, F)
    dm, vd = E.daily(A["xv"], A["valid"])
    call = E.call(R)
    st = []
    for i, s in enumerate(P.STATIONS):
        code = s[0]
        rec = dict(code=code, name=s[1], operator="Thornmouth Borough Council" if s[2] == "TBC" else "Thornmouth Bulk Terminal",
                   valid_days=int(vd[i].sum()), valid_count=int(R["valid_days"][i]), year_count=int(R[E.REFERENCE][i]),
                   family=[int(min(R[k][i] for k in wind)), int(max(R[k][i] for k in wind))],
                   interval=[int(min(R[k][i] for k in wind)) - 1, int(max(R[k][i] for k in wind)) + 1], note=code in call,
                   pro_rata=round(float(R["pro_rata"][i]), 1),
                   no2=round(no2[code], 1) if code in no2 else None, dep=int(round(dep[s[1]])) if s[2] == "TBT" else None,
                   no2_export=round(no2_naive[code], 1) if code in no2 else None,
                   dep_lab=int(round(dep_lab[s[1]])) if s[2] == "TBT" else None)
        if code in call:
            rec.update(evidence(A, code))
            rec["rebuilt_above"] = rec["year_count"] - rec["valid_count"]
        st.append(rec)
    rungs = {k: [P.CODES[i] for i in range(len(P.CODES)) if R["valid_days"][i] <= 35 and
                 (R[k][i] > 50 if k.startswith("p904") else R[k][i] > 35)]
             for k in R if not k.startswith("wind") and k != "valid_days"}
    noted = [r for r in st if r["note"]]
    ev = dict(lost_days=sum(r["lost_days"] for r in noted), lost_bearing=sum(r["lost_bearing"] for r in noted),
              valid_days=sum(r["valid_days"] for r in noted), valid_bearing=sum(r["bearing_days"] for r in noted))
    cst = dict(procedure_sections=["3", "5.1", "5.2", "5.3"], daily_valid_hours=18, limit=50, allowed=35, sectors=[4, 8, 12, 16, 36], speed_band=4.0, wet_mm=0.2,
               min_cell_hours=5, bearing_half=BEARING_HALF, bearing_hours=BEARING_HOURS, no2_logger=solve.logger_fits(target, F)["TH1"][1],
               no2_basis=P.NO2_PER_PPB, lab_area=round(solve.lab_area(target, F), 4),
               frisbee_mm=solve.frisbee_mm(target, F), frisbee_area=round(solve.frisbee_area(target, F), 4))
    return dict(call=call, stations=st, rungs=rungs, reference=E.REFERENCE, readings=len(wind), evidence=ev, constants=cst)


def _rows(fig):
    return {s["code"]: s for s in fig["stations"]}


WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven"}


def _names(rows):
    return ", ".join("%s (%s)" % (s["name"], s["code"]) for s in rows[:-1]) + " and %s (%s)" % (rows[-1]["name"], rows[-1]["code"])


def _list(vals):
    return ", ".join(vals[:-1]) + " and " + vals[-1]


def golden_content(fig):
    S = _rows(fig)
    noted = [S[c] for c in fig["call"]]
    k, rest = WORD[len(noted)], WORD[len(S) - len(noted)]
    q5, q6 = S["TH5"], S["TH6"]
    ev = fig["evidence"]
    paras = [
        "<b>%s stations cannot be reported as meeting the PM10 24-hour objective for 2027: %s.</b> Each counted 35 or "
        "fewer days above 50 µg/m³ among its valid daily means (%s) but more than 35 over the whole year once its "
        "days without a valid daily mean are counted (%s), so under AQ-QP-04 section 5.2 their results go into the ASR "
        "with the data-capture note. The other %s stations carry no note." % (
            k.capitalize(), _names(noted), _list(["%d" % s["valid_count"] for s in noted]),
            _list(["%d" % s["year_count"] for s in noted]), rest),
        "The days these %s lost are not like the days they reported. Their TEOMs stopped as the terminal's dust reached "
        "them and stayed down until the next round: the wind blew from the terminal for six hours or more on %d of their "
        "%d lost days, against %d of their %d valid days, and on those valid days they averaged %s µg/m³ against a "
        "network median of %s. The lost hours are rebuilt from the other stations' median that hour plus each station's "
        "own response to the wind (sector, speed, wet or dry day) on its valid hours; every usual variant of that rebuild "
        "keeps all %s above 35 (lowest %d) and every other station at or under 35." % (
            k, ev["lost_bearing"], ev["lost_days"], ev["valid_bearing"], ev["valid_days"],
            _list(["%.1f" % s["bearing_station"] for s in noted]), _list(["%.1f" % s["bearing_network"] for s in noted]),
            k, min(s["family"][0] for s in noted)),
        "Scaling the valid-day count by data capture would put Market Street and Westholme Avenue over 35 (%.1f and %.1f) "
        "and none of the %s: those two lost long stretches in quiet spells (the Market Street resurfacing works, the "
        "Westholme Avenue analyser away for repair), and rebuilt they reach %d and %d." % (
            q5["pro_rata"], q6["pro_rata"], k, q5["year_count"], q6["year_count"]),
    ]
    return dict(stations=fig["stations"], call=fig["call"],
                title="%s PM10 stations take the data-capture note for 2027" % k.capitalize(),
                chart_title="%s stations' lost days take them past 35" % k.capitalize(),
                paras=paras,
                footnote="Days above 50: valid daily means (18 or more valid hours, GMT days). Whole year: the same days plus "
                         "the rebuilt days without a valid daily mean (section 5.1); ranges in the workbook. NO2 and deposition "
                         "figures for the audit are in the workbook.")


def write_figures(path, fig):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")


def submission(fig):
    S = _rows(fig)
    noted = [S[c] for c in fig["call"]]
    k, rest = WORD[len(noted)], WORD[len(S) - len(noted)]
    q5, q6 = S["TH5"], S["TH6"]
    ev, cst = fig["evidence"], fig["constants"]
    lines = []
    w = lines.append
    w("# task245 submission")
    w("")
    w("## Tags")
    w("")
    w("**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance: a borough air quality "
      "network's 2027 PM10 results against the 24-hour objective, each station's lost days counted).")
    w("**Analytical objective:** Data Quality Monitoring & Alerting (which stations' 2027 PM10 results carry the "
      "data-capture note into the Annual Status Report, with the NO2 annual mean at each council NO2 station and the dust "
      "deposition rate at each terminal gauge beside them).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**%s stations go into the 2027 Annual Status Report with the data-capture note: %s count %s days above 50 "
      "µg/m³ among their valid daily means but %s over the whole year once their lost days are rebuilt; the other "
      "%s carry no note.**" % (k.capitalize(), _names(noted), _list(["%d" % s["valid_count"] for s in noted]),
                               _list(["%d" % s["year_count"] for s in noted]), rest))
    w("")
    w("Their analysers stopped on the days the terminal's dust blew onto them (the wind came from the terminal for six "
      "hours or more on %d of their %d lost days, against %d of their %d valid days), so the lost days are rebuilt from "
      "the other stations' median and each station's own response to the wind. Not the count scaled by data capture, "
      "which notes Market Street and Westholme Avenue (%.1f and %.1f), whose long outages fell in quiet spells, and none "
      "of the %s. Not the lost days filled from the other stations alone, or by interpolation in time, which leave all %s "
      "at 35 or under." % (ev["lost_bearing"], ev["lost_days"], ev["valid_bearing"], ev["valid_days"], q5["pro_rata"],
                           q6["pro_rata"], k, k))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Whole-year days above 50 at the %s noted stations (accepted range): **%s**, more than 35 under every rebuild choice." % (
        k, "; ".join("%s %d (%d to %d)" % (s["code"], s["year_count"], s["interval"][0], s["interval"][1]) for s in noted)))
    w("2. Their days above 50 among valid daily means: **%s**, each 35 or fewer." %
      "; ".join("%s %d" % (s["code"], s["valid_count"]) for s in noted))
    w("3. Market Street and Westholme Avenue over the whole year: **%d and %d** (%d to %d, %d to %d), no note." % (
        q5["year_count"], q6["year_count"], q5["interval"][0], q5["interval"][1], q6["interval"][0], q6["interval"][1]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    steps = [
        "Hourly PM10 on one grid: the council's export (status R only) and the terminal's workbook (status OK only; UK "
        "clock time, hour beginning, moved to GMT hour ending, the repeated 01:00 of 31 October read as BST then GMT).",
        "Daily means of the valid hours where at least 18 are valid (AQ-QP-04 section 3) and, per station, the days above "
        "50 among them.",
        "The %s stations' lost days against the port's met mast: the reported wind direction was within 22.5 degrees of "
        "the bearing from the station to the stockyard centre (the register's grid references, the plan's centre) for six "
        "hours or more on %d of their %d "
        "lost days and %d of their %d valid days, and on those valid days they averaged %s against the other stations' "
        "median daily mean of %s." % (
            k, ev["lost_bearing"], ev["lost_days"], ev["valid_bearing"], ev["valid_days"],
            _list(["%.1f" % s["bearing_station"] for s in noted]), _list(["%.1f" % s["bearing_network"] for s in noted])),
        "Rebuild of every hour without a valid mean: the median of the other stations' valid hourly means that hour, plus "
        "the station's mean increment over that median in the hour's wind cell (16 sectors, speed under or at least 4 m/s, "
        "wet or dry day, a day being wet when the mast's rain totals more than 0.2 mm; a cell with fewer than five valid "
        "hours takes the sector's mean), taken from its valid hours; calm or missing directions take the nearest reported "
        "hour's.",
        "Whole-year count (section 5.1): the valid daily means plus, for each day without one, the mean of its valid and "
        "rebuilt hours; the accepted range is the lowest to highest count under the other rebuild choices (4, 8, 12, 16 or "
        "36 sectors or a smooth fit in the direction, with or without speed and rain, the council's background stations, "
        "the rural station or a station-and-hour fit as the background), a day either side.",
        "The note (section 5.2): %s, each with 35 or fewer valid-day exceedances and more than 35 over the year." %
        _list([s["code"] for s in noted]),
        "NO2 (section 5.3): each council NO2 station's valid hours, each hour once (a week the analyser's store sent twice "
        "dropped), the hours from its new logger's fitting in June (service log, converted at %.2f) multiplied by "
        "%.2f/%.2f." % (cst["no2_logger"], cst["no2_basis"], cst["no2_logger"]),
        "Deposition (plan revision 3, section 3): each terminal gauge's periods that started in 2027, the void period "
        "out, each period's total deposit over the collecting area of the gauge exposed then (the laboratory's %.4f m2 "
        "to the 7 June exchange, the %d mm Frisbee gauge's %.4f m2 from it, plan Annex A and service log) and its days, "
        "weighted by days." % (cst["lab_area"], cst["frisbee_mm"], cst["frisbee_area"]),
    ]
    for j, st in enumerate(steps, 1):
        w("%d. %s" % (j, st))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### thornmouth_pm10_2027_data_capture_review.xlsx")
    w("")
    w("1. Stations, 12 rows in the register's order: days above 50 ug/m3 over the whole of 2027 (accepted range) and the note:")
    for s in fig["stations"]:
        w("   - %s (%s): %d over the whole year (%d to %d); %s" % (
            s["name"], s["code"], s["year_count"], s["interval"][0], s["interval"][1], "note" if s["note"] else "no note"))
    w("2. NO2 annual mean 2027, ug/m3 to one decimal:")
    for s in fig["stations"]:
        if s["no2"] is not None:
            w("   - %s (%s) %.1f" % (s["name"], s["code"], s["no2"]))
    w("3. Dust deposition rate 2027, mg/m2 per day, whole number:")
    for s in fig["stations"]:
        if s["dep"] is not None:
            w("   - %s (%s) %d" % (s["name"], s["code"], s["dep"]))
    w("")
    w("### asr2027_pm10_data_capture_note.pdf")
    w("")
    w("- One page for the auditor: the %s noted stations, why their lost days count, and a chart of every station's "
      "days above 50 over its valid daily means (open) and over the whole year (filled) against the 35-day line, the %s "
      "noted stations marked." % (k, k))
    w("")
    return "\n".join(lines)
