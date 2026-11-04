"""Independent verifier: reads only target/ and figures.json, on its own code path (no generator module but the file
names), and recomputes every graded figure. Every format the pack ships is read back, each with a positive
control on the same extractor."""
import csv
import datetime as dt
import json
import math
import os
import re
import statistics
import sys

N = [0]


def ok(name, cond, detail=""):
    if not cond:
        raise AssertionError("verify %s: %s" % (name, detail))
    N[0] += 1


def t99(df):
    from scipy.stats import t
    return float(t.ppf(0.99, df))


def upl(vals):
    y = [math.log(v) for v in vals]
    n = len(y)
    m = sum(y) / n
    s = statistics.stdev(y)
    return math.exp(m + t99(n - 1) * s * math.sqrt(1 + 1 / n))


def s3(x):
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    return ("%%.%df" % max(d, 0)) % round(x, d)


def loc(s):
    m = re.fullmatch(r"MW-0*(\d+)(R?)", s.strip())
    return "MW-%s%s" % (m.group(1), m.group(2)) if m else s.strip()


def season(d):
    return "%d-%s" % (d.year, "APR" if d.month in (4, 5) else "OCT")


def run(tgt, figpath):
    N[0] = 0
    F = json.load(open(figpath))
    names = sorted(os.listdir(tgt))
    edd_a = [n for n in names if n.startswith("tamarack_edd")][0]
    edd_b = [n for n in names if n.startswith("ridgeline_edd")][0]
    gauge = [n for n in names if "gauging" in n][0]
    points = [n for n in names if "monitoring_points" in n][0]
    purge = [n for n in names if n.startswith("fieldlog_purge")][0]
    calib = [n for n in names if n.startswith("fieldlog_calibration")][0]
    sap = [n for n in names if "SAP" in n][0]
    fsp = [n for n in names if "FS-03" in n][0]

    # ---- the plan's filed sentences, read back through the same extractor
    from pypdf import PdfReader
    sap_text = " ".join(p.extract_text() for p in PdfReader(os.path.join(tgt, sap)).pages)
    sap_text = re.sub(r"\s+", " ", sap_text)
    ok("pdf.sap_positive_control", "Background water quality is the quality of groundwater that the landfill has not affected" in sap_text)
    ok("pdf.sap_window", "from April 2018 through the April event" in sap_text)
    ok("pdf.sap_percentile", "99th percentile" in sap_text)
    ok("pdf.sap_names_no_mechanism", not re.search(r"revers|pumping|well field|drawdown", sap_text, re.I))
    fs_text = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(tgt, fsp)).pages))
    ok("pdf.fs03_positive_control", "1.91 per cent per degree" in fs_text)
    ok("pdf.fs03_purge_definition", "pump controller's volume counter" in fs_text)

    # ---- indicators from both laboratories
    ind = {}
    for r in csv.DictReader(open(os.path.join(tgt, edd_a), encoding="utf-8")):
        if r["Sample_Type"] != "N" or r["Reportable"] != "Y" or not r["Location"].startswith("MW"):
            continue
        k = {"Chloride": "chloride", "Sodium, Dissolved": "sodium", "Boron, Dissolved": "boron"}.get(r["Parameter"])
        if not k:
            continue
        v = float(r["Result"]) * (1000.0 if k == "boron" else 1.0)
        d = dt.datetime.strptime(r["Sample_Date"], "%m/%d/%Y").date()
        ind[(loc(r["Location"]), season(d), k)] = v
    for r in csv.DictReader(open(os.path.join(tgt, edd_b), encoding="utf-8"), delimiter="\t"):
        if r["sample_type_code"] != "N" or r["reportable_result"] != "Yes" or not r["sys_loc_code"].startswith("MW"):
            continue
        k = {("Chloride", "N"): "chloride", ("Sodium", "D"): "sodium", ("Boron", "D"): "boron"}.get(
            (r["chemical_name"], r["fraction"]))
        if not k:
            continue
        d = dt.date.fromisoformat(r["sample_date"][:10])
        ind[(loc(r["sys_loc_code"]), season(d), k)] = float(r["result_value"])
    ok("edd.both_labs_read", len(ind) > 500, len(ind))

    # ---- heads and the boundary relation
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(tgt, points), read_only=True)
    surv = {}
    for row in list(wb["Survey"].iter_rows(values_only=True))[1:]:
        surv.setdefault(row[0], []).append((str(row[1])[:10], float(row[3])))
    ok("xlsx.survey_positive_control", any(x[0] == "2022-06-14" for x in surv["MW-1"]))
    head = {}
    for r in csv.DictReader(open(os.path.join(tgt, gauge), encoding="utf-8")):
        toc = sorted(x for x in surv[r["location"]] if x[0] <= r["date"])[-1][1]
        head[(r["location"], r["event"])] = round(toc - float(r["dtw_ft_btoc"]), 2)
    bnd = {"MW-1": "PZ-1", "MW-2": "PZ-2", "MW-3": "PZ-3"}
    events = sorted({e for (_, e) in head}, key=lambda s: (s[:4], s[5:] != "APR"))
    bg_events = events[:-1]
    rev = {(w, e): head[(w, e)] < head[(bnd[w], e)] for w in bnd for e in events}
    nrev = {w: sum(rev[(w, e)] for e in bg_events) for w in bnd}
    ok("heads.reversed_counts", nrev["MW-1"] == F["reversed_events"]["MW-1"] and nrev["MW-2"] == F["reversed_events"]["MW-2"]
       and nrev["MW-3"] == 0, nrev)

    # ---- limits, counts, call
    lim, cnt = {}, {}
    for k in ("chloride", "sodium", "boron"):
        vals = [v for (w, e, kk), v in ind.items() if kk == k and w in bnd and e in bg_events and not rev[(w, e)]]
        lim[k] = upl(vals)
        cnt[k] = len(vals)
        ok("limit.%s" % k, s3(lim[k]) == F["limits"][k], (s3(lim[k]), F["limits"][k]))
        ok("count.%s" % k, cnt[k] == F["background_n"][k], (cnt[k], F["background_n"][k]))
        allv = [v for (w, e, kk), v in ind.items() if kk == k and w in bnd and e in bg_events]
        ok("default_limit.%s" % k, s3(upl(allv)) == F["default_limits"][k])
        ok("window.%s" % k, len(allv) == F["window_n"][k])
    wells = ["MW-4", "MW-5R", "MW-6", "MW-7", "MW-8", "MW-9", "MW-10", "MW-11"]
    last = events[-1]
    call = [w for w in wells if any(ind[(w, last, k)] > lim[k] for k in lim)]
    ok("call", call == F["call"], (call, F["call"]))
    for w in wells:
        for k in lim:
            ok("october.%s.%s" % (w, k), s3(ind[(w, last, k)]) == F["october"]["%s %s" % (w, k)])
            ok("october_exceed.%s.%s" % (w, k), (ind[(w, last, k)] > lim[k]) == (k in F["exceed"][w]))
    default_call = [w for w in wells if any(ind[(w, last, k)] > upl([v for (ww, e, kk), v in ind.items()
                                                                    if kk == k and ww in bnd and e in bg_events])
                                            for k in lim)]
    ok("default_path_answer", default_call == F["default_path_answer"], default_call)

    # ---- the field asks, from the sampler's entries and the day's calibration of the meter that took them
    cal = list(csv.DictReader(open(os.path.join(tgt, calib), encoding="utf-8")))
    reports_at_25 = {}
    for r in cal:
        if r["sensor"] != "Conductivity":
            continue
        T, exp = float(r["std_temperature_c"]), float(r["expected_value"])
        at_25 = r["reading_units"] == "uS/cm at 25 C"
        # positive control on every conductivity entry: the value it should read is the standard's 1413 at 25 C, or,
        # reported at the standard's own temperature, 1413 times 1 + 0.0191 (T - 25)
        ok("calib.expected_value_matches_units.%s.%s.%s" % (r["cal_date"], r["meter_sn"], r["check_type"][:3]),
           abs(exp - (1413 if at_25 else 1413 * (1 + 0.0191 * (T - 25)))) <= 0.6, (r, exp))
        key = (r["cal_date"], r["meter_sn"])
        if key in reports_at_25:
            ok("calib.end_of_day_agrees.%s.%s" % key, reports_at_25[key] == at_25)
        reports_at_25[key] = at_25
    # the chain of custody's collection minute for each October primary, local time in Wisconsin, to UTC: daylight
    # time runs from the second Sunday of March to the first Sunday of November
    def central_to_utc(s):
        t = dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
        y = t.year
        mar = dt.datetime(y, 3, 8) + dt.timedelta(days=(6 - dt.date(y, 3, 8).weekday()) % 7, hours=2)
        nov = dt.datetime(y, 11, 1) + dt.timedelta(days=(6 - dt.date(y, 11, 1).weekday()) % 7, hours=2)
        return t + dt.timedelta(hours=5 if mar <= t < nov else 6)
    rows = list(csv.DictReader(open(os.path.join(tgt, purge), encoding="utf-8")))
    oct_days = sorted({r["visit_date"] for r in rows if r["visit_date"].startswith("2026-10")})
    ok("purge.three_october_days", len(oct_days) == 3)
    ok("purge.no_sample_marker", not any(r["remark"] not in ("", "decon rinse", "bottles filled, pump off") for r in rows))
    coc = {}
    for r in csv.DictReader(open(os.path.join(tgt, edd_b), encoding="utf-8"), delimiter="\t"):
        if r["sample_type_code"] == "N" and r["sys_loc_code"].startswith("MW") and r["sample_date"][:10] in oct_days:
            coc.setdefault(loc(r["sys_loc_code"]), set()).add(central_to_utc(r["sample_date"]))
    ok("coc.one_time_per_well", all(len(v) == 1 for v in coc.values()) and len(coc) == 11, coc)
    coc = {w: min(v) for w, v in coc.items()}
    spc, vol = {}, {}
    for d in oct_days:
        rs = sorted((r for r in rows if r["visit_date"] == d), key=lambda r: r["entry_utc"])
        meter, stop, start, at = "", 0.0, {}, {}
        for r in rs:
            if r["remark"].startswith("decon") or r["remark"].startswith("bottles"):
                stop = float(r["controller_l"])
                continue
            meter = r["meter_sn"] or meter
            start.setdefault(r["location"], stop)
            if dt.datetime.strptime(r["entry_utc"], "%Y-%m-%dT%H:%M:%SZ") <= coc[r["location"]]:
                at[r["location"]] = (r, meter)
        for w, (r, m) in at.items():
            c = float(r["spc_us_cm"])
            ok("calib.meter_calibrated_that_day.%s.%s" % (d, m), (d, m) in reports_at_25)
            if not reports_at_25[(d, m)]:
                c /= 1 + 0.0191 * (float(r["temperature_c"]) - 25)
            spc[w] = c
            vol[w] = (float(r["controller_l"]) - start[w]) / 3.785411784
    ok("asks.eleven_wells", len(spc) == 11 and len(vol) == 11)
    for w in spc:
        ok("ask.spc.%s" % w, int(round(spc[w])) == F["spc_25c"][w], (w, spc[w], F["spc_25c"][w]))
        ok("ask.purge.%s" % w, "%.1f" % round(vol[w], 1) == F["purge_gal"][w], (w, vol[w], F["purge_gal"][w]))
        c = round(spc[w])
        ok("bin.spc.%s" % w, 0.5 - abs(spc[w] - c) >= 0.1, spc[w])
        c = round(vol[w], 1)
        ok("bin.purge.%s" % w, 0.05 - abs(vol[w] - c) >= 0.01, vol[w])

    # ---- the other formats read back
    js = json.load(open(os.path.join(tgt, [n for n in names if n.endswith(".json")][0])))
    ok("json.precip_read", len(js["data"]) > 3000)
    ok("txt.edd_b_large", sum(1 for _ in open(os.path.join(tgt, edd_b), encoding="utf-8")) - 1 >= 25000)
    return N[0]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print(run(os.path.join(os.path.dirname(here), "target"), os.path.join(here, "figures.json")))
