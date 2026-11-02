"""Independent verifier: recompute every graded figure from target.zip with its own readers (pdftotext for the handbook,
pandas for the records), its own exposure split and its own Poisson fit, and compare with figures.json.

    python3 task137/generator/verify.py [path/to/target.zip]
"""
import collections
import datetime as dt
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(os.path.dirname(HERE), "target.zip")
MON = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)


def lastsun(y, m):
    d = dt.date(y, m, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def summer(d):
    return int(lastsun(d.year, 3) <= d < lastsun(d.year, 10))


def band(h):
    return sum(h >= e for e in (4, 7, 9, 15, 19, 22))


def main(zp=ZIP):
    fails = []
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(zp) as z:
        z.extractall(tmp)
    names = os.listdir(tmp)
    root = os.path.join(tmp, names[0]) if len(names) == 1 and os.path.isdir(os.path.join(tmp, names[0])) else tmp

    def f(pat):
        return os.path.join(root, [x for x in os.listdir(root) if re.search(pat, x)][0])
    # handbook table by pdftotext
    txt = subprocess.run(["pdftotext", "-layout", f(r"handbook"), "-"], capture_output=True, text=True).stdout
    sun, blocks = {}, []
    for line in txt.splitlines():
        m = re.match(r"\s*(\d+) (\w{3})(?: to (\d+) (\w{3}))?\s+((?:\d\d:\d\d\s*){8})$", line)
        if m:
            a = (MON[m.group(2)], int(m.group(1)))
            b = (MON[m.group(4)], int(m.group(3))) if m.group(3) else a
            t = [int(x[:2]) * 60 + int(x[3:]) for x in m.group(5).split()]
            for j, dep in enumerate(["CRA", "GAT", "CAR", "DAR"]):
                sun[(dep, len(blocks))] = (t[2 * j] / 60.0, t[2 * j + 1] / 60.0)
            blocks.append((a, b))

    def blk(d):
        md = (2, 28) if (d.month, d.day) == (2, 29) else (d.month, d.day)
        return next(k for k, (a, b) in enumerate(blocks) if a <= md <= b)
    # register
    reg = pd.read_excel(f(r"fleet_register"), sheet_name="Trucks")
    dmap = {"Cra": "CRA", "Gat": "GAT", "Car": "CAR", "Dar": "DAR"}
    reg["key"] = reg["Registration"].str.replace(" ", "").str.upper()
    depot = dict(zip(reg.key, reg["Depot"].str[:3].map(dmap)))
    sensors = dict(zip(reg.key, reg["Forward sensors"]))
    # telematics
    a = pd.read_csv(f(r"gridtrak.*2023-10"), dtype=str)
    b = pd.read_csv(f(r"gridtrak.*2026-09"), dtype=str)
    ra = pd.DataFrame({"key": a["Vehicle"].str.upper(), "day": pd.to_datetime(a["Date"], format="%d/%m/%Y").dt.date,
                       "on": a["First Ignition On (UTC)"].map(lambda s: int(s[:2]) * 60 + int(s[3:])),
                       "off": a["Last Ignition Off (UTC)"].map(lambda s: int(s[:2]) * 60 + int(s[3:])),
                       "km": a["Distance (mi)"].astype(float) * 1.609344})
    rb = pd.DataFrame({"key": b["registration"].str.replace(" ", "").str.upper(), "day": pd.to_datetime(b["day_utc"]).dt.date,
                       "on": b["ignition_on_utc"].str[11:13].astype(int) * 60 + b["ignition_on_utc"].str[14:16].astype(int),
                       "off": b["ignition_off_utc"].str[11:13].astype(int) * 60 + b["ignition_off_utc"].str[14:16].astype(int),
                       "km": b["distance_km"].astype(float)})
    runs = pd.concat([ra[~ra.day.isin(set(rb.day))], rb])
    runs = runs[runs.day <= dt.date(2026, 9, 30)]

    def split(day, dep, a0, b0, km):
        off = summer(day)
        rise, sett = sun[(dep, blk(day))]
        rise, sett = rise + off, sett + off
        pts = sorted(set([a0, b0] + [float(h) for h in range(math.floor(a0) + 1, math.ceil(b0))] +
                         [x for x in (rise, sett) if a0 < x < b0]))
        out = []
        for x, y in zip(pts[:-1], pts[1:]):
            mid = (x + y) / 2
            out.append((band(int(mid)), int(mid < rise or mid > sett), km * (y - x) / (b0 - a0), day.month, (day.month - 1) // 3 + 1))
        return out
    expo = collections.defaultdict(float)
    for r in runs.itertuples():
        off = summer(r.day)
        for bd, dk, km, _, _ in split(r.day, depot[r.key], r.on / 60 + off, r.off / 60 + off, r.km):
            expo[(bd, dk)] += km
    # claims
    lst = pd.read_excel(f(r"claims_listing"), header=4)
    lst = lst[lst["Claim no."].astype(str).str.startswith("RVM")]
    tr = lst[(lst["Vehicle"] == "HGV 7.5t") & ~lst["Status"].astype(str).str.startswith("Closed") & (lst["Status"] != "Withdrawn")]
    tr = tr[pd.to_datetime(tr["Incident date"]).dt.date <= dt.date(2026, 9, 30)]
    cnt = collections.Counter()
    for r in tr.itertuples():
        d = pd.Timestamp(r[3]).date()
        hh = int(str(r[4])[:2]) + int(str(r[4])[3:5]) / 60
        k = r[5].replace(" ", "").upper()
        rise, sett = sun[(depot[k], blk(d))]
        off = summer(d)
        cnt[(band(int(hh)), int(hh < rise + off or hh > sett + off))] += 1
    # Poisson log-linear fit on the band x light table by IRLS
    cells = sorted(expo)
    y = np.array([cnt.get(c, 0) for c in cells], float)
    lk = np.log(np.array([expo[c] for c in cells]))
    bands = sorted({c[0] for c in cells})
    Xm = np.array([[1.0] + [1.0 if c[0] == bb else 0.0 for bb in bands[1:]] + [float(c[1])] for c in cells])
    beta = np.zeros(Xm.shape[1])
    beta[0] = math.log(y.sum() / np.exp(lk).sum())
    for _ in range(50):
        mu = np.exp(Xm @ beta + lk)
        beta = beta + np.linalg.solve(Xm.T @ (Xm * mu[:, None]), Xm.T @ (y - mu))

    def rate(bd, dk):
        v = beta[0] + (beta[1 + bands.index(bd) - 1] if bd != bands[0] else 0.0) + beta[-1] * dk
        return math.exp(v)
    # the 2027 schedule
    rt = pd.read_excel(f(r"route_schedule"), sheet_name="Routes")
    cal = pd.read_excel(f(r"route_schedule"), sheet_name="Calendar 2027")
    days = [pd.Timestamp(x).date() for x in cal.loc[cal["Deliveries"] == "Yes", "Date"]]
    qs = collections.defaultdict(float)
    ss = collections.defaultdict(float)
    for r in rt.itertuples():
        a0 = int(str(r[6])[:2]) + int(str(r[6])[3:5]) / 60
        dur = int(str(r[7]).split(":")[0]) + int(str(r[7]).split(":")[1]) / 60
        for d in days:
            for bd, dk, km, mo, q in split(d, r[2], a0, a0 + dur, float(r[8])):
                qs[q] += km * rate(bd, dk)
                ss["apr_sep" if 4 <= mo <= 9 else "other"] += km * rate(bd, dk)
    year = sum(qs.values())
    # the asks
    jobs = pd.read_csv(f(r"brantwick_jobs"), dtype=str).set_index("Job No")
    apl = pd.read_csv(f(r"ap_ledger"), dtype=str)
    status = dict(zip(lst["Claim no."], lst["Status"].astype(str)))
    own = {k: (v.split()[-1] if v.startswith("Closed - duplicate of") else k) for k, v in status.items()}
    row = lst.set_index("Claim no.")
    grp = apl.groupby(["Supplier Ref", "Invoice Date", "Description", "Net"]).size()
    outlay = collections.defaultdict(float)
    for (job, idate, desc, net), n in grp.items():
        cl = own[jobs.loc[job, "Claim Ref"]]
        k = str(row.loc[cl, "Registration"]).replace(" ", "").upper()
        cap = 2 if (desc == "ADAS calibration" and sensors[k] == "Camera and radar") else 1
        outlay[cl] += min(n, cap) * float(net)
    b1 = collections.defaultdict(float)
    for cl, v in outlay.items():
        d = pd.Timestamp(row.loc[cl, "Incident date"]).date()
        k = str(row.loc[cl, "Registration"]).replace(" ", "").upper()
        per = (("2025H1" if d.month <= 6 else "2025H2") if d.year == 2025 else
               ("2026H1" if d.year == 2026 and d.month <= 6 else None))
        if per:
            b1["%s %s" % (depot[k], per)] += v
    bank = pd.read_csv(f(r"recovery_account"), dtype=str)
    ins = sorted(set(lst["Third-party insurer"].dropna()))
    first = {i.split()[0].upper(): i for i in ins}
    a1 = collections.defaultdict(float)
    for r in bank[bank["Type"] == "BAC"].itertuples():
        payer = first.get(r.Description.split()[0])
        if not payer:
            continue
        d = pd.to_datetime(r.Date, format="%d/%m/%Y").date()
        amt = float(r._4)
        m = re.search(r"RVM\d{6}", r.Description)
        if m:
            cl = own[m.group(0)]
        else:
            hits = []
            for cl2, x in row.iterrows():
                if x["Third-party insurer"] != payer or x["Fault"] not in ("Non-fault", "Split") or cl2 not in outlay:
                    continue
                if pd.Timestamp(x["Incident date"]).date() >= d:
                    continue
                sh = [1.0] if x["Fault"] == "Non-fault" else [0.75, 2 / 3, 0.5, 1 / 3, 0.25]
                if any(abs(round(outlay[cl2] * s + 1e-9, 2) - amt) < 0.005 for s in sh):
                    hits.append(cl2)
            if len(hits) != 1:
                fails.append("receipt %s %s matched %d claims" % (r.Date, r.Description, len(hits)))
                continue
            cl = hits[0]
        d0 = pd.Timestamp(row.loc[cl, "Incident date"]).date()
        q = "%dQ%d" % (d0.year, (d0.month - 1) // 3 + 1)
        a1[q] += amt
    F = json.load(open(os.path.join(HERE, "figures.json")))

    def chk(lab, cond, det=""):
        print(("PASS " if cond else "FAIL ") + lab + (": %s" % det if det != "" else ""))
        if not cond:
            fails.append(lab)
    chk("V1 2027 claims %.1f against %.1f" % (year, F["claims_2027_unrounded"]), abs(year - F["claims_2027_unrounded"]) < 0.5
        and int(50 * round(year / 50)) == F["claims_2027"])
    for k in ("apr_sep", "other_months"):
        val = ss["apr_sep" if k == "apr_sep" else "other"]
        chk("V2 2027 %s %.1f" % (k, val), int(50 * round(val / 50)) == F["claims_2027_%s" % k]
            and abs(val - F["claims_2027_%s_unrounded" % k]) < 0.5)
    for k, v in F["recoveries_unrounded"].items():
        chk("V3 recoveries %s %.2f" % (k, a1[k]), abs(a1[k] - v) < 0.01 and int(100 * round(a1[k] / 100)) ==
            F["recoveries_by_collision_quarter"][k])
    for k, v in F["repair_cost_unrounded"].items():
        chk("V4 repair cost %s %.2f" % (k, b1[k]), abs(b1[k] - v) < 0.01 and int(100 * round(b1[k] / 100)) ==
            F["repair_cost_by_depot"][k])
    print("verify: %d failures" % len(fails))
    return len(fails)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else ZIP) else 0)
