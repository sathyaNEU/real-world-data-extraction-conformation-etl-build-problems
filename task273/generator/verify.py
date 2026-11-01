"""Independent verifier: reads only target/ and figures.json, on its own code path, and recomputes every graded
figure. PB9's footprint is measured here as the dip in each neighbour's daily level over the constant-rate days
against the week before and after (not by the generator's regression), the existing bores' response by a
per-bore regression on summer days only, and each council meter's bore by its zero days against SCADA outages.

    python3 task273/generator/verify.py      # exit 1 on any mismatch
"""
import base64
import csv
import json
import math
import os
import re
import sys
import zlib
from collections import defaultdict
from datetime import date, datetime, timedelta

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
BORES = ["PB%d" % k for k in range(1, 9)]
MONTHS = [12, 1, 2, 3]
MNAME = {12: "December", 1: "January", 2: "February", 3: "March"}
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("  " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


def rows_after(path, first):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    k = next(i for i, l in enumerate(lines) if l.startswith(first))
    return list(csv.reader(lines[k:]))


def pdf_strings(path):
    """Every string drawn with Tj on the PDF's pages: each content stream ASCII85- then Flate-decoded."""
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\s*\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        txt = raw
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2])
            txt = zlib.decompress(raw)
        except Exception:
            pass
        out += [s.decode("latin-1") for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", txt, re.S)]
    return " ".join(out)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    files = os.listdir(T)
    pick = lambda p: os.path.join(T, [f for f in files if f.startswith(p)][0])

    # register and plan (xlsx)
    wb = load_workbook(pick("kaitanga_bore_register"), data_only=True)
    rr = list(wb["Bores"].iter_rows(values_only=True))
    h = rr[0]
    reg = {r[0]: dict(zip(h, r)) for r in rr[1:]}
    mp = {b: reg[b]["Ground RL (m, Moturiki 1953)"] + reg[b]["MP above ground (m)"] for b in reg}
    mol = {b: reg[b]["Minimum operating level (m bmp)"] for b in reg}
    kw = {r[0]: r[2] for r in list(wb["Pumps"].iter_rows(values_only=True))[1:]}
    check("register read back (xlsx)", len(reg) == 9 and "PB9" in reg)
    pl = load_workbook(pick("kaitanga_summer_bore_plan"), data_only=True).active
    plan = {m: {} for m in MONTHS}
    for r in pl.iter_rows(values_only=True):
        if r and r[0] in reg:
            for k, m in enumerate(MONTHS):
                plan[m][r[0]] = float(r[k + 1])
    check("plan read back (xlsx)", len(plan[2]) == 9 and abs(plan[2]["PB9"] - 4.40) < 1e-9)

    # the governing documents (pdf)
    std = pdf_strings(pick("SWS-03"))
    check("standard read back (pdf): the design drought", "1 December 2019 to 31 March 2020" in std)
    check("standard read back (pdf): the test", "no production bore" in std and "minimum" in std)
    per = pdf_strings(pick("MRC_water_permit"))
    check("permit read back (pdf): Schedule 1 meters", "WM-30455" in per and "WM-35874" in per)

    # MB1
    mb = {}
    for r in rows_after(pick("MRC_MB1"), "Date,")[1:]:
        mb[datetime.strptime(r[0], "%d/%m/%Y").date()] = float(r[1])
    dmin = {}
    for m in MONTHS:
        y = 2019 if m == 12 else 2020
        dmin[m] = min(v for d, v in mb.items() if d.year == y and d.month == m)

    # SCADA daily (dedupe exact repeats)
    seen, Q, L, H = set(), defaultdict(dict), defaultdict(dict), defaultdict(dict)
    for r in rows_after(pick("kaitanga_bores_daily"), "date_local,")[1:]:
        key = tuple(r)
        if key in seen:
            continue
        seen.add(key)
        d = date.fromisoformat(r[0])
        b = "PB%d" % int(re.sub(r"\D", "", r[1])[-2:])
        Q[b][d] = int(r[2]) / 1000.0
        if r[3]:
            L[b][d] = float(r[3])
        H[b][d] = float(r[4])

    # PB9 test: hourly, UTC -> NZDT (UTC+13 throughout October)
    q9 = defaultdict(float)
    test = rows_after(pick("PB9_logger"), "Date,")[1:]
    stat, cr = [], []
    for r in test:
        t = datetime.fromisoformat(r[0] + " " + r[1]) + timedelta(hours=13)
        q9[t.date()] += float(r[3]) * 3600 / 1e6
        if r[4] == "static":
            stat.append((t, float(r[2])))
        if r[4] == "constant rate":
            cr.append((t, float(r[2]), float(r[3])))
    cr_days = sorted(d for d, v in q9.items() if v > 4.0)
    check("PB9 constant-rate days found", len(cr_days) >= 6, str(len(cr_days)))

    def resid(b, d):
        """Level less what the bore's own take and MB1 explain, by the bore's own fit on the 30 days either side."""
        return mp[b] - L[b][d] - mb[d]

    # existing bores: summer-day regression on every bore's take, outside the test window
    days = sorted(d for d in mb if all(d in Q[b] and d in L[b] for b in BORES) and d.month in (11, 12, 1, 2, 3, 4)
                  and q9.get(d, 0.0) == 0.0)
    X = np.array([[1.0] + [Q[b][d] for b in BORES] for d in days])
    coef = {}
    for b in BORES:
        y = np.array([resid(b, d) for d in days])
        coef[b], *_ = np.linalg.lstsq(X, y, rcond=None)

    # PB9 footprint: each neighbour's residual (after its own and its neighbours' takes) on the full test days
    # against the 7 days before and after
    a9 = {}
    full = [d for d in cr_days if q9[d] > 4.3]
    near = [d for d in sorted(mb) if (full[0] - timedelta(days=8)) <= d < full[0] - timedelta(days=1)
            or full[-1] + timedelta(days=1) < d <= full[-1] + timedelta(days=8)]
    for b in BORES:
        def r2(d):
            return resid(b, d) - coef[b][0] - sum(coef[b][1 + k] * Q[c][d] for k, c in enumerate(BORES))
        inn = [r2(d) / q9[d] for d in full if d in L[b] and all(d in Q[c] for c in BORES)]
        out = [r2(d) for d in near if d in L[b] and all(d in Q[c] for c in BORES)]
        a9[b] = -(np.mean(inn) - np.mean(out) / np.mean([q9[d] for d in full]))
    # PB9's own drawdown per ML/d and its static level, by reciprocity carried to the plan
    s0_t, s0 = stat[0]
    late = [x for x in cr if x[0] >= cr[-1][0] - timedelta(hours=24)]
    c9 = (np.mean([x[1] for x in late]) - s0) / (np.mean([x[2] for x in late]) * 86400 / 1e6)

    lev = {}
    for m in MONTHS:
        q = plan[m]
        for b in BORES:
            rl = dmin[m] + coef[b][0] + sum(coef[b][1 + k] * q[c] for k, c in enumerate(BORES)) - a9[b] * q["PB9"]
            lev[(b, m)] = mp[b] - rl
        d0 = s0_t.date()
        rl9 = (mp["PB9"] - s0) + (dmin[m] - mb[d0]) - c9 * q["PB9"] - sum(a9[c] * (q[c] - Q[c][d0]) for c in BORES)
        lev[("PB9", m)] = mp["PB9"] - rl9
    half = lambda v: math.floor(v * 2 + 0.5) / 2
    for b in BORES:
        for m in MONTHS:
            k = "%s %s" % (b, MNAME[m])
            check("lowest level " + k, half(lev[(b, m)]) == fig["lowest_level_m_bmp"][k],
                  "%.3f vs %s" % (lev[(b, m)], fig["lowest_level_m_bmp"][k]))
    fails = ["%s %s" % (b, MNAME[m]) for b in BORES + ["PB9"] for m in MONTHS if lev[(b, m)] > mol[b]]
    check("the call: failing bores and months", fails == fig["call"]["failing"], str(fails))
    check("PB9 holds", all(lev[("PB9", m)] <= mol["PB9"] for m in MONTHS) == fig["pb9_holds"])
    for b in ("PB3", "PB4"):
        check("PB9 drawdown on " + b, half(a9[b] * 4.40) == fig["pb9_drawdown_on_neighbour_m"][b],
              "%.3f" % (a9[b] * 4.40))

    # council meters: each meter's bore is the SCADA bore whose zero-take days match its zero days
    tele = rows_after(pick("MRC_permit_meter"), "MeterID,")[1:]
    by = defaultdict(list)
    for r in tele:
        by[r[0]].append((datetime.fromisoformat(r[1]), float(r[2])))

    def dst(nzst):
        y = nzst.year
        s = datetime(y, 9, 30)
        s -= timedelta(days=(s.weekday() + 1) % 7)
        e = datetime(y, 4, 1)
        e += timedelta(days=(6 - e.weekday()) % 7)
        return nzst >= s + timedelta(hours=2) or nzst < e + timedelta(hours=2)
    vol = defaultdict(lambda: defaultdict(float))     # local quarter-hour start -> m3 (the repeated hour adds)
    mday = defaultdict(lambda: defaultdict(float))
    for mid, seq in by.items():
        seq.sort()
        for (t0, v0), (t1, v1) in zip(seq, seq[1:]):
            dv = v1 - v0
            if dv < -1000:
                dv += 1_000_000.0
            start = t1 - timedelta(minutes=15)
            loc = start + timedelta(hours=1) if dst(start) else start
            mday[mid][loc.date()] += dv / 1000.0
            vol[mid][loc] += dv
    assign = {}
    for mid, s in mday.items():
        ds = sorted(s)[1:-1]
        best = min(BORES, key=lambda b: sum(abs(s[d] - Q[b].get(d, 0.0)) for d in ds) / len(ds))
        assign[mid] = best
    check("meter matching covers every bore", set(assign.values()) == set(BORES), str(assign))
    qb = [(date(2025, 7, 1), date(2025, 9, 30)), (date(2025, 10, 1), date(2025, 12, 31)),
          (date(2026, 1, 1), date(2026, 3, 31)), (date(2026, 4, 1), date(2026, 6, 30))]
    meters = defaultdict(float)
    for mid, ser in vol.items():
        for t, v in ser.items():
            for k, (a, b) in enumerate(qb, 1):
                if a <= t.date() <= b:
                    meters[(assign[mid], k)] += v / 1000.0
    for (b, k), v in sorted(meters.items()):
        check("permit meter %s Q%d" % (b, k), round(v, 1) == fig["permit_meter_ml"]["%s Q%d" % (b, k)],
              "%.2f" % v)

    # electricity: UTC to local, multiplier by meter serial, shared boards by run hours x motor kW
    icpreg = list(csv.DictReader(open(pick("kaitanga_icp_meter_register"), encoding="utf-8")))
    mult = {r["meter_serial"]: float(r["multiplier"]) for r in icpreg}
    owner = {}
    for r in icpreg:
        m = re.findall(r"Bore (\d)", r["installation"])
        if m:
            owner[r["icp"]] = ["PB%s" % x for x in m]
        elif r["installation"].startswith("PB"):
            owner[r["icp"]] = [r["installation"][:3]]
    kwh = defaultdict(float)
    for r in csv.DictReader(open(pick("pump_icp_interval"), encoding="utf-8")):
        u = datetime.strptime(r["interval_start_utc"], "%Y-%m-%dT%H:%MZ")
        n = u + timedelta(hours=12)
        loc = n + timedelta(hours=1) if dst(n) else n
        kwh[(r["icp"], loc.date())] += float(r["reg_advance"]) * mult[r["meter_serial"]]
    energy = defaultdict(float)
    for (icp, d), v in kwh.items():
        bs = owner.get(icp)
        if not bs or bs == ["PB9"]:
            continue
        k = next((i for i, (a, b) in enumerate(qb, 1) if a <= d <= b), None)
        if k is None:
            continue
        if len(bs) == 1:
            energy[(bs[0], k)] += v
        else:
            w = {b: H[b].get(d, 0.0) * kw[b] for b in bs}
            tot = sum(w.values())
            for b in bs:
                energy[(b, k)] += v * w[b] / tot if tot else 0.0
    for (b, k), v in sorted(energy.items()):
        got = int(round(v / meters[(b, k)]))
        check("electricity %s Q%d" % (b, k), got == fig["energy_kwh_per_ml"]["%s Q%d" % (b, k)],
              "%.2f" % (v / meters[(b, k)]))
    print("%d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
