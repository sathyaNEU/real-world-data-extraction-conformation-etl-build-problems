"""task247 independent verifier: recomputes every graded figure from the shipped bundle alone (no generator module is
imported) and checks figures.json, submission.md and the two goldens against it.

    python3 task247/generator/verify.py [target golden figures.json submission.md]
"""
import csv
import datetime as dt
import json
import os
import sys

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
F = {"sites": "watch_sites_register.csv", "clim": "srao_sst_daily_climatology_watch_pixels.csv",
     "nrt": "srao_nrt_sst_extract_watch_pixels_2018-01-01_2027-11-02.csv",
     "rep": "srao_reprocessed_sst_watch_pixels_2018_2026.csv", "bulletins": "heat_stress_bulletins_2027.xlsx",
     "deployments": "logger_log_2023-08_2027-04.csv", "pins": "logger_pin_register.csv",
     "readings": "logger_readings_from_2024-04-01.csv"}
LEVELS = ["No alert", "Alert Level 1", "Alert Level 2"]


def fail(msg):
    print("VERIFY FAIL:", msg)
    sys.exit(1)


def check(cond, msg):
    if not cond:
        fail(msg)


def rows(target, k):
    with open(os.path.join(target, F[k]), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def level(x):
    return LEVELS[2] if x >= 8 else (LEVELS[1] if x >= 4 else LEVELS[0])


def series(target):
    sites = rows(target, "sites")
    codes = [s["site_code"] for s in sites]
    pix = {s["pixel_id"]: s["site_code"] for s in sites}
    mmm = {s["site_code"]: float(s["mmm_c"]) for s in sites}
    d0, d1 = dt.date(2018, 1, 1), dt.date(2027, 11, 2)
    days = [d0 + dt.timedelta(i) for i in range((d1 - d0).days + 1)]
    di = {d.isoformat(): i for i, d in enumerate(days)}
    S, T = len(codes), len(days)
    latest = {}
    for r in rows(target, "nrt"):
        key = (r["pixel_id"], r["date"])
        if key not in latest or r["issued_utc"] > latest[key]["issued_utc"]:
            latest[key] = r
    nrt = np.full((S, T), np.nan)
    obs = np.zeros((S, T), bool)
    for (p, d), r in latest.items():
        k, i = codes.index(pix[p]), di[d]
        nrt[k, i] = float(r["sst_c"])
        obs[k, i] = int(r["obs_flag"]) == (2 if r["product_version"] == "3.2" else 1)
    rep = np.full((S, T), np.nan)
    for r in rows(target, "rep"):
        rep[codes.index(pix[r["pixel_id"]]), di[r["time"]]] = float(r["analysed_sst_k"]) - 273.15
    cl = {}
    for r in rows(target, "clim"):
        cl[(r["pixel_id"], int(r["month"]), int(r["day"]))] = float(r["clim_sst_c"])
    inv = {c: p for p, c in pix.items()}
    clim = np.array([[cl[(inv[c], d.month, d.day)] for d in days] for c in codes])
    return codes, sites, mmm, days, di, nrt, obs, rep, clim


def dhw(x, m):
    h = x - m
    h = np.where(h >= 1.0, h, 0.0)
    c = np.concatenate([[0.0], np.cumsum(h)])
    lo = np.maximum(0, np.arange(len(h)) - 83)
    return (c[1:] - c[lo]) / 7.0


def call(target):
    codes, sites, mmm, days, di, nrt, obs, rep, clim = series(target)
    past = np.array([d.year <= 2026 for d in days])
    both = past[None, :] & ~np.isnan(rep) & ~np.isnan(nrt)
    b = float(np.mean((nrt - rep)[both & obs]))
    season = np.array([dt.date(2027, 6, 1) <= d <= dt.date(2027, 10, 31) for d in days])
    idx = np.arange(len(days))
    out = {}
    for k, c in enumerate(codes):
        an = nrt[k] - b - clim[k]
        o = obs[k]
        full = clim[k] + np.where(o, an, np.interp(idx, idx[o], an[o]))
        out[c] = float(dhw(full, mmm[c])[season].max())
    return codes, sites, b, out


def declared(target, codes):
    wb = load_workbook(os.path.join(target, F["bulletins"]), read_only=True, data_only=True)
    ws = wb["Bulletins"]
    best = {c: 0 for c in codes}
    head = None
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Bulletin":
            head = list(r)
            continue
        if head is None or r[0] is None:
            continue
        day = str(r[head.index("Analysis day")])[:10]
        if "2027-06-01" <= day <= "2027-10-31":
            c = r[head.index("Site")]
            best[c] = max(best[c], LEVELS.index(r[head.index("Alert level")]))
    return {c: LEVELS[v] for c, v in best.items()}


def local_time(x):
    """a log time as written: one the log marks UTC is five hours ahead of the station's local time"""
    if x.endswith(" UTC"):
        return dt.datetime.strptime(x[:-4], "%Y-%m-%d %H:%M") - dt.timedelta(hours=5)
    return dt.datetime.strptime(x, "%Y-%m-%d %H:%M")


def pin_site(target, sites):
    """each log row's site, rebuilt day by day: on a service day the boat reaches four sites, north to south; a day whose
    pins read through the register as four consecutive sites in that order keeps the register, and on any other day
    the k-th pin reached is the k-th site of that day's stretch of coast, the stretch being the day's place in its
    trip. Returns the row's site and the tag map each scheme gives."""
    dep = rows(target, "deployments")
    reg = {r["pin"]: r["site_code"] for r in rows(target, "pins")}
    north = [s["site_code"] for s in sorted(sites, key=lambda s: -float(s["latitude"]))]
    P = local_time
    ev = []
    for i, r in enumerate(dep):
        ev.append((P(r["deployed"]), r["pin"], i, 0))
        if r["retrieved"]:
            ev.append((P(r["retrieved"]), r["pin"], i, 1))
    ev.sort()
    days = {}
    for t, pin, i, k in ev:
        days.setdefault(t.date(), []).append((t, pin, i, k))
    order = sorted(days)
    trip_day = {}
    for j, d in enumerate(order):
        trip_day[d] = 0 if j == 0 or (d - order[j - 1]).days > 3 else trip_day[order[j - 1]] + 1
    site, old = {}, {}
    for d in order:
        seq = []
        for t, pin, i, k in days[d]:
            if pin not in seq:
                seq.append(pin)
        stretch = north[4 * trip_day[d]:4 * trip_day[d] + 4]
        here = [reg[p] for p in seq] == stretch
        for t, pin, i, k in days[d]:
            s = reg[pin] if here else stretch[seq.index(pin)]
            if not here:
                old.setdefault(pin, set()).add(s)
            if k == 0:
                site[i] = s
            check(k == 0 or site[i] == s, ("a row's two stops read two sites", i))
    check(all(len(v) == 1 for v in old.values()), ("an earlier tag read as two sites", old))
    return [site[i] for i in range(len(dep))], {p: next(iter(v)) for p, v in old.items()}


def loggers(target, mmm, sites):
    dep = rows(target, "deployments")
    where, old = pin_site(target, sites)
    reads = {}
    for r in rows(target, "readings"):
        reads.setdefault(r["serial"], []).append((dt.datetime.strptime(r["datetime_local"], "%Y-%m-%d %H:%M"),
                                                  float(r["temperature_c"])))
    P = lambda s: dt.datetime.strptime(s.replace(" UTC", ""), "%Y-%m-%d %H:%M")
    # each trip's clock: the logger's step out of the water against the logged retrieval, read from the digits as
    # written; it has to agree with the log's own UTC mark
    lag = {}
    for r in dep:
        if not r["retrieved"]:
            continue
        z = P(r["retrieved"])
        x = [(t, v) for t, v in reads.get(r["serial"], []) if z - dt.timedelta(hours=9) <= t <= z + dt.timedelta(hours=3)]
        if len(x) < 4:
            continue
        j = max(range(1, len(x)), key=lambda i: x[i][1] - x[i - 1][1])
        lag.setdefault((r["retrieved_from"], r["retrieved"][:7]), []).append((z - x[j][0]).total_seconds() / 3600)
    offset = {k: (5 if np.median(v) > 3 else 0) for k, v in lag.items()}
    marked = {}
    for r in dep:
        for when, boat in (("deployed", "deployed_from"), ("retrieved", "retrieved_from")):
            if r[when]:
                marked.setdefault((r[boat], r[when][:7]), set()).add(5 if r[when].endswith(" UTC") else 0)
    check(all(len(v) == 1 for v in marked.values()), ("a trip with marked and unmarked times", marked))
    check(all(offset[k] == next(iter(marked[k])) for k in offset), ("the loggers' step against the UTC mark", offset))
    hours = {}
    for r, site in zip(dep, where):
        if not r["retrieved"]:
            continue
        a, z = local_time(r["deployed"]), local_time(r["retrieved"])
        m = mmm[site]
        hours[site] = hours.get(site, 0) + sum(
            1 for t, v in reads.get(r["serial"], []) if a <= t <= z and t.year in (2024, 2025, 2026)
            and 6 <= t.month <= 10 and v >= m)
    return hours, offset, old


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(p.extract_text() for p in PdfReader(path).pages).replace("\n", " ")


def main(target, golden, figpath, subpath):
    fig = json.load(open(figpath))
    sub = open(subpath, encoding="utf-8").read()
    codes, sites, b, est = call(target)
    decl = declared(target, codes)
    names = {s["site_code"]: s["site_name"] for s in sites}
    mmm = {s["site_code"]: float(s["mmm_c"]) for s in sites}
    n = 0
    check(abs(round(b, 2) - fig["clear_sky"]) < 1e-9, "the clear-sky difference")
    check("**%.2f degrees Celsius**" % b in sub, "the submission's clear-sky difference")
    on = [c for c in codes if est[c] >= 8]
    check(on == fig["call"] and fig["count"] == len(on), ("the call", on))
    n += 3
    S = {s["code"]: s for s in fig["sites"]}
    for c in codes:
        lv = level(est[c])
        v = "confirms" if lv == decl[c] else ("raises" if LEVELS.index(lv) > LEVELS.index(decl[c]) else "lowers")
        s = S[c]
        check(int(round(est[c])) == s["dhw"] and lv == s["level"] and v == s["verdict"] and decl[c] == s["declared"],
              ("site", c, est[c], lv, v))
        check(0.5 - abs(est[c] - round(est[c])) >= 0.2, ("edge", c, est[c]))
        check("   - %s %s: %d; %s; %s (declared %s)" % (c, names[c], int(round(est[c])), lv, v, decl[c]) in sub,
              ("submission line", c))
        n += 5
    hrs, off, old = loggers(target, mmm, sites)
    check(sorted(k for k, v in off.items() if v) == [("Cozumel II", "2025-08"), ("Cozumel II", "2026-04")], ("offsets", off))
    check(len(old) == 16 and old == {p: c for p, c in fig["pins_before_retag"].items()}, ("the earlier tags", old))
    for c in codes:
        check(hrs[c] == S[c]["hours"], ("ask B", c, hrs[c]))
        check("   - %s: %d" % (c, hrs[c]) in sub, ("ask B line", c))
        n += 2
    # the goldens carry the same figures
    wb = load_workbook(os.path.join(golden, "reef_heat_stress_2027.xlsx"), read_only=True, data_only=True)
    got = {r[0]: r for r in wb["Survey list"].iter_rows(min_row=5, values_only=True) if r[0] in codes}
    check(len(got) == 16, "the golden's 16 rows")
    for c in codes:
        r = got[c]
        check(r[3] == decl[c] and r[5] == int(round(est[c])) and r[6] == level(est[c]) and
              (r[8] == "Yes") == (est[c] >= 8), ("golden row", c))
    h = {r[0]: r for r in wb["Loggers"].iter_rows(min_row=4, values_only=True) if r[0] in codes}
    check("2023 survey" not in wb.sheetnames, "the golden carries no cut ask")
    for c in codes:
        check(h[c][2] == hrs[c], ("golden ask", c))
    n += 32
    # the shipped documents carry the filed sentences the call and the asks lean on
    docs = {"reef_heat_stress_watch_methods_v3.pdf": ["when that difference is positive", "HotSpots of 1.0 degree Celsius or more",
                                                     "84 days ending on that day", "Alert Level 1 when a site's DHW reach 4",
                                                     "runs from 1 June to 31 October", "highest alert level any of the bulletins",
                                                     "every site at Alert Level 2 for the season", "the day being the UTC day",
                                                     "the register's pixel_id", "the register's mmm_c"],
            "srao_nrt_sst_user_guide_v3_2.pdf": ["A later issue of a day replaces the earlier one", "from the issues of 15 July 2027",
                                                 "the day is the UTC day", "Values are in degrees Celsius",
                                                 "one row per pixel, day and issue"],
            "srao_reprocessed_sst_release_note_2027-05.pdf": ["analysed_sst, in kelvin"]}
    for f, phrases in docs.items():
        t = " ".join(pdf_text(os.path.join(target, f)).split())
        check(len(t) > 400, ("the extractor read the document", f, len(t)))
        for ph in phrases:
            check(ph in t, ("filed sentence", f, ph))
            n += 1
    # no shipped file describes the data (dataset-generation section 3): no readme, dictionary, codebook, manifest,
    # field notes or file list ships, by name; the documents above are the organisation's own and were read
    describing = ("readme", "dictionary", "codebook", "manifest", "field_notes", "fieldnotes", "definitions", "file_list",
                  "data_notes", "extract_notes", "export_notes", "schema")
    shipped = sorted(os.listdir(target))
    check(not [f for f in shipped if any(w in f.lower().replace("-", "_") for w in describing)], ("a describing file ships", shipped))
    check(not [f for f in shipped if f.lower().endswith((".md", ".txt"))], ("a notes file ships", shipped))
    eml = open(os.path.join(target, "survey_list_request_2027-11-03.eml"), encoding="utf-8").read()
    check("Alert Level 2 for the season" in " ".join(eml.split()), "the request")
    check("Date: Wed, 3 Nov 2027 08:05:12 -0500" in eml, "the request's own clock, the station's UTC-5")
    n += 4
    note = pdf_text(os.path.join(golden, "survey_list_note_2027.pdf"))
    for c in on:
        check(c in note, ("the note names", c))
    check("\u2014" not in sub and "\u2013" not in sub, "no dashes")
    n += len(on) + 1
    print("verify: %d checks passed" % n)
    return n


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 4:
        main(*a)
    else:
        main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
             os.path.join(TASK, "submission.md"))
