"""The independent verifier: reads only the shipped pack and the goldens, on its own code path (nothing from the
generator's modules), and recomputes the call, its components and every ask figure, reading back every format the
pack ships (xlsx, csv, pdf, docx) with a positive control on each document it quotes."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
import openpyxl
from pypdf import PdfReader
from scipy.optimize import brentq, least_squares
from scipy.special import exp1

FAILS = []


def ok(label, cond, detail=""):
    if not cond:
        FAILS.append((label, detail))
        print("VERIFY FAIL  %s  %s" % (label, detail))


def text(path):
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def find(folder, pattern):
    hits = [f for f in os.listdir(folder) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(folder, hits[0])


def bst(t):
    y = t.year
    ls = lambda m: (lambda x: x - dt.timedelta(days=(x.weekday() + 1) % 7))(dt.date(y, m, 31))     # noqa: E731
    return dt.datetime.combine(ls(3), dt.time(1)) <= t < dt.datetime.combine(ls(10), dt.time(1))


def to_local(t_utc):
    return t_utc + dt.timedelta(hours=1) if bst(t_utc) else t_utc


def from_local(t_loc):
    g = t_loc - dt.timedelta(hours=1)
    return g if bst(g) else t_loc


def gridref(s):
    m = re.match(r"SJ (\d{5}) (\d{5})", s)
    return 300000 + int(m.group(1)), 300000 + int(m.group(2))


def theis(r2, t, T, S):
    return exp1(r2 * S / (4 * T * t)) / (4 * math.pi * T)


def main(target, golden):
    FAILS.clear()
    # ---------------------------------------------------------------------------------------------- the test
    wb = openpyxl.load_workbook(find(target, r"crt_june2014"), read_only=True, data_only=True)
    fs = list(wb["Field sheet"].iter_rows(values_only=True))
    on_local = dt.datetime.strptime(fs[1][1], "%d/%m/%Y %H:%M")
    ok("test field sheet: pump on is in BST", fs[1][2] == "BST")
    on = from_local(on_local)
    q = np.mean([float(r[4]) for r in fs[7:] if r and r[2] == "BH2" and r[4] not in (None, "")]) * 86.4
    survey = {}
    with open(find(target, r"site_survey"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            survey.setdefault(r["point"], (float(r["easting"]), float(r["northing"])))
    e0, n0 = survey["BH2"]
    data = []
    for ob in ("OB1", "OB2", "OB3"):
        rows = list(wb[ob].iter_rows(values_only=True))
        hdr = {str(r[0]): r[1] for r in rows[:6] if r and r[0]}
        body = rows[7:]
        if ob == "OB3":
            ok("OB3 logger: kPa on local time", "kPa" in str(hdr.get("Pressure unit")) and "BST" in str(hdr.get("Time zone")))
            tt = [from_local(dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M")) for r in body]
            lv = np.array([float(r[1]) for r in body]) / 9.80665
        else:
            ok("%s logger: metres on UTC" % ob, hdr.get("Clock") == "UTC")
            tt = [dt.datetime.strptime(r[0] + " " + r[1], "%Y-%m-%d %H:%M:%S") for r in body]
            lv = np.array([float(r[2]) for r in body])
        tm = np.array([(x - on).total_seconds() / 86400.0 for x in tt])
        pre = lv[(tm > -1 / 24.0) & (tm <= 0)].mean()
        m = (tm > 1 / 1440.0) & (tm <= 3.0)
        e, n = survey[ob]
        data.append(((e - e0) ** 2 + (n - n0) ** 2, tm[m], pre - lv[m]))

    def res(p):
        T, S = math.exp(p[0]), math.exp(p[1])
        return np.concatenate([q * theis(r2, t, T, S) - s for r2, t, s in data])
    f = least_squares(res, [math.log(100.0), math.log(1e-3)])
    T, S = math.exp(f.x[0]), math.exp(f.x[1])
    # ---------------------------------------------------------------------------------------------- letter and geology
    letter = text(find(target, r"pre-application"))
    flat = re.sub(r"\s+", " ", letter)
    ok("letter read back: the test sentence", "measured from its rest water level in April 2015" in flat)
    prot = []
    for name in ("Lower Hay Farm", "Kilnbrook Nurseries", "Hollin Bank Golf Club"):
        m = re.search(re.escape(name) + r".*?(SJ \d{5} \d{5})\s+(\d+\.\d{2})\s+(\d+\.\d{2})", flat)
        ok("letter: %s row" % name, m is not None)
        e, n = gridref(m.group(1))
        prot.append((name, (e - e0, n - n0), float(m.group(3))))
    geo = re.sub(r"\s+", " ", text(find(target, r"geology")))
    ok("geology read back: the structure paragraph", "Coldharbour Fault" in geo)
    m = re.search(r"Windle Cross road at (SJ \d{5} \d{5}) and the disused mineral railway at (SJ \d{5} \d{5})", geo)
    ok("geology: two points on the fault", m is not None)
    a = np.array(gridref(m.group(1)), float) - (e0, n0)
    c = np.array(gridref(m.group(2)), float) - (e0, n0)
    d = (c - a) / np.linalg.norm(c - a)
    img = 2 * (a + np.dot(-a, d) * d)
    t_tot = (dt.date(2039, 4, 1) - dt.date(2015, 4, 1)).days
    t_new = (dt.date(2039, 4, 1) - dt.date(2027, 4, 1)).days

    def dd(qn, xy, image=True):
        r2 = xy[0] ** 2 + xy[1] ** 2
        ri2 = (xy[0] - img[0]) ** 2 + (xy[1] - img[1]) ** 2
        s = 1200 * theis(r2, t_tot, T, S) + (qn - 1200) * theis(r2, t_new, T, S)
        if image:
            s += 1200 * theis(ri2, t_tot, T, S) + (qn - 1200) * theis(ri2, t_new, T, S)
        return s
    lim = {name: brentq(lambda x: dd(x, xy) - av, -1e5, 1e6) for name, xy, av in prot}
    worst = min(lim, key=lim.get)
    largest = math.floor(lim[worst] / 100.0) * 100
    at1800 = {name: int(math.floor(dd(1800, xy) + 0.5)) for name, xy, _ in prot}
    th = {name: brentq(lambda x: dd(x, xy, False) - av, -1e5, 1e6) for name, xy, av in prot}
    # ---------------------------------------------------------------------------------------------- the long record
    rt = text(find(target, r"abstraction_returns"))
    mnames = {dt.date(2000, m, 1).strftime("%B"): m for m in range(1, 13)}
    ret = {}
    for mname, y, v in re.findall(r"^(%s) (\d{4})\s*\n\s*([\d,]+)\s*$" % "|".join(mnames), rt, re.M):
        k = (int(y), mnames[mname])
        nd = ((dt.date(k[0] + (k[1] == 12), k[1] % 12 + 1, 1)) - dt.date(*k, 1)).days
        ret[k] = float(v.replace(",", "")) / nd
    ok("returns read back: April 2015 to March 2026, every month", len(ret) == 132 and min(ret) == (2015, 4) and
       max(ret) == (2026, 3), str(len(ret)))
    casing = {}
    with open(find(target, r"site_survey"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["casing_top_maod"]:
                casing.setdefault(r["point"], []).append(float(r["casing_top_maod"]))
    wx = {}
    for r in csv.DictReader(open(find(target, r"windle_cross"), encoding="utf-8")):
        d_ = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        wx.setdefault((d_.year, d_.month), []).append(float(r["Level (mAOD)"]))
    wx = {k: float(np.mean(v)) for k, v in wx.items()}
    obl = {}
    for r in csv.DictReader(open(find(target, r"ob_monthly_levels"), encoding="utf-8")):
        y, m = map(int, r["month"].split("-"))
        ct = casing[r["borehole"]][1] if (r["borehole"] == "OB2" and (y, m) >= (2020, 3)) else casing[r["borehole"]][0]
        obl.setdefault(r["borehole"], {})[(y, m)] = ct - float(r["mean_depth_to_water_m_btoc"])
    steps = sorted(ret)

    def model(xy, k, image):
        mid = dt.datetime(*k, 1) + dt.timedelta(days=((dt.date(k[0] + (k[1] == 12), k[1] % 12 + 1, 1)) -
                                                       dt.date(*k, 1)).days / 2.0)
        s_, prev_ = 0.0, 0.0
        for st_ in steps:
            t0 = dt.datetime(*st_, 1)
            if t0 >= mid:
                break
            age = (mid - t0).total_seconds() / 86400.0
            r2 = xy[0] ** 2 + xy[1] ** 2
            u = theis(r2, age, T, S)
            if image:
                u += theis((xy[0] - img[0]) ** 2 + (xy[1] - img[1]) ** 2, age, T, S)
            s_ += (ret[st_] - prev_) * u
            prev_ = ret[st_]
        return s_
    resid = {True: [], False: []}
    for ob in ("OB1", "OB2", "OB3"):
        e, n = survey[ob]
        xy = (e - e0, n - n0)
        ks = sorted(k for k in obl[ob] if k in wx)
        lev = np.array([obl[ob][k] - (wx[k] - wx[(2015, 4)]) for k in ks])
        for image in (True, False):
            pred = np.array([model(xy, k, image) for k in ks])
            resid[image].append(lev - (np.mean(lev + pred) - pred))
    rms_c = float(np.sqrt(np.mean(np.concatenate(resid[True]) ** 2)))
    rms_u = float(np.sqrt(np.mean(np.concatenate(resid[False]) ** 2)))
    # ---------------------------------------------------------------------------------------------- goldens
    figs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok("verify: the long record's misfits, closed and unbounded", round(rms_c, 2) == figs["rms_closed_m"] and
       round(rms_u, 2) == figs["rms_unbounded_m"], "%.4f %.4f" % (rms_c, rms_u))
    note = re.sub(r"\s+", " ", text(os.path.join(golden, "bh2_licence_variation_note.pdf")))
    ok("verify: largest quantity", largest == figs["call_largest_m3d"] == 1300, "%s" % largest)
    ok("verify: limiting borehole", worst == figs["call_limiting"])
    ok("verify: drawdowns at 1,800", all(at1800[n] == figs["at1800_%s_m" % n.split()[0].lower()] for n in at1800), str(at1800))
    ok("verify: T and S", int(round(T)) == figs["T_m2d"] and round(S * 1e4, 1) == figs["S_e4"], "%.2f %.3e" % (T, S))
    ok("verify: the unbounded aquifer limits at Kilnbrook Nurseries near 2,600",
       min(th, key=th.get) == "Kilnbrook Nurseries" and abs(min(th.values()) - 2600) < 50, str({k: round(v) for k, v in th.items()}))
    ok("golden note states the call", "Apply for 1,300 cubic metres a day." in note)
    for name in at1800:
        ok("golden note row %s" % name, re.search(re.escape(name) + r" \d+\.\d{2} %d " % at1800[name], note) is not None)
    # ---------------------------------------------------------------------------------------------- ask A
    tel = list(csv.DictReader(open(find(target, r"telemetry"), encoding="utf-8")))
    day = {}
    l3 = {}
    prev = None
    for r in tel:
        loc = to_local(dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%MZ"))
        day[loc.date()] = day.get(loc.date(), 0.0) + float(r["fm1_flow_ls"]) * 0.9
        reg = float(r["fm_l3_register_m3"])
        if prev is not None:
            l3[(loc.year, loc.month)] = l3.get((loc.year, loc.month), 0.0) + reg - prev
        prev = reg
    ev = list(csv.DictReader(open(find(target, r"controller_events"), encoding="utf-8")))
    runs = []
    st = None
    for r in ev:
        t = dt.datetime.strptime(r["timestamp"], "%d/%m/%Y %H:%M:%S")
        if r["event"] == "PUMP START":
            st = t
        elif r["event"] == "PUMP STOP" and st is not None:
            runs.append((st, t))
            st = None
    wb = openpyxl.load_workbook(find(target, r"bulk_tickets"), read_only=True, data_only=True)
    seen = set()
    add = {}
    unmatched = 0
    for ws in wb.worksheets:
        for r in list(ws.iter_rows(values_only=True))[4:]:
            if not r or not r[0] or not str(r[0]).isdigit():
                continue
            key = (ws.title,) + tuple(r)
            if key in seen:
                continue
            seen.add(key)
            d0 = dt.datetime.strptime(r[1], "%d/%m/%Y").date()
            hi, mi = map(int, r[3].split(":"))
            ho, mo = map(int, r[4].split(":"))
            dd0 = d0 + dt.timedelta(days=1 if hi < 12 else 0)
            t_in = dt.datetime.combine(dd0, dt.time(hi, mi))
            t_out = dt.datetime.combine(dd0, dt.time(ho, mo)) + dt.timedelta(seconds=59)
            if t_out < t_in:
                t_out += dt.timedelta(days=1)
            hit = [x for x in runs if t_in <= x[0] <= t_out]
            if len(hit) != 1:
                unmatched += 1
                continue
            add[hit[0][0].date()] = add.get(hit[0][0].date(), 0.0) + float(r[5]) / 1000.0
    ok("ask A: every ticket on one pump run", unmatched == 0, str(unmatched))
    months_a = [(2026, m) for m in range(4, 10)]
    months = [(2025, m) for m in range(4, 13)] + [(2026, m) for m in range(1, 4)]
    gold = {row["month"]: row for row in csv.DictReader(open(os.path.join(golden, "bh2_returns_check.csv"), encoding="utf-8"))}
    ok("ask A: the returns check holds April to September 2026", sorted(gold) == ["%04d-%02d" % k for k in months_a],
       str(sorted(gold)))
    for y, m in months_a:
        days = [dt.date(y, m, 1) + dt.timedelta(days=i) for i in range(31) if (dt.date(y, m, 1) + dt.timedelta(days=i)).month == m]
        vol = sum(day.get(x, 0.0) + add.get(x, 0.0) for x in days)
        over = sum(1 for x in days if day.get(x, 0.0) + add.get(x, 0.0) > 1200)
        lab = "%04d-%02d" % (y, m)
        ok("ask A %s volume" % lab, int(math.floor(vol / 100 + 0.5) * 100) == int(gold[lab]["volume_taken_m3"]) ==
           figs["askA_volume_%04d_%02d" % (y, m)], "%.1f" % vol)
        ok("ask A %s days" % lab, over == int(gold[lab]["days_over_1200_m3"]) == figs["askA_days_%04d_%02d" % (y, m)], str(over))
    # ---------------------------------------------------------------------------------------------- ask B
    sku = {r[0]: float(r[2]) for r in list(openpyxl.load_workbook(find(target, r"sku_master"), read_only=True,
                                                                   data_only=True).active.iter_rows(values_only=True))[1:]}
    wts = {}
    for r in csv.DictReader(open(find(target, r"qc_fill"), encoding="utf-8")):
        t = dt.datetime.strptime(r["sample_time"], "%d/%m/%Y %H:%M").date()
        if r["line"] == "L3" and r["result"] == "PASS" and dt.date(2025, 4, 1) <= t <= dt.date(2026, 3, 31):
            wts.setdefault(r["material"], []).append(float(r["net_fill_g"]))
    size = dict(sku)
    for k, w in wts.items():
        size[k] = round(np.median(w) / 1.0015 / 50.0) * 50.0
    ok("ask B: the 75cl still glass filled at 750 ml in the year", size["BSG-1101"] == 750.0 and sku["BSG-1101"] == 700.0)
    lit = {}
    for r in csv.DictReader(open(find(target, r"bottling_runs"), encoding="utf-8")):
        if r["line"] == "L3" and r["order_type"] == "PROD":
            t = dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M")
            lit[(t.year, t.month)] = lit.get((t.year, t.month), 0.0) + int(r["qty_good"]) * size[r["sku"]] / 1000.0
    for y, m in months:
        v = l3[(y, m)] * 1000.0 / lit[(y, m)]
        lab = dt.date(y, m, 1).strftime("%B %Y")
        ok("ask B %s" % lab, round(v, 2) == figs["askB_l3_%04d_%02d" % (y, m)] and ("%s %.2f" % (lab, v)) in note,
           "%.4f" % v)
    # ---------------------------------------------------------------------------------------------- formats
    import docx
    brief = "\n".join(p.text for p in docx.Document(find(target, r"line5_project_brief")).paragraphs)
    ok("docx read back: the brief's need sentence", "about 1,800 cubic metres" in brief)
    ok("pdf read back: the licence's day condition", "a day is a period of 24 hours beginning at midnight" in
       re.sub(r"\s+", " ", text(find(target, r"abstraction_licence"))))
    ok("pdf read back: the returns", "Return of water abstracted" in text(find(target, r"abstraction_returns")))
    print("verify: %s (largest %d at %s; T %.1f, S %.3e; ask A and ask B recomputed from the pack)" % (
        "PASS" if not FAILS else "FAIL %d" % len(FAILS), largest, worst, T, S))
    if FAILS:
        raise SystemExit("verify failed")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(os.path.join(task, "target"), os.path.join(task, "golden"))
