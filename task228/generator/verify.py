"""Independent verifier: reads only the files under target/ (csv, json, pyarrow, openpyxl and pypdf; no pandas, no
generator state) and recomputes the call, every check's record, the hold line, the reconciliation's agreement with the
register's labels and the installs that sent from SDK 9.4.1 still on it each day, then compares them with figures.json."""
import csv
import json
import os
import re
from math import floor, sqrt

import pyarrow.parquet as pq
from openpyxl import load_workbook
from pypdf import PdfReader

Z = 2.5758293035489
STD_N = 10000
NAMES = {"gap": "Gap sessions", "dup": "Duplicate sessions", "late": "Late sessions", "epu": "Events per install",
         "share": "Treatment share"}
TYPES = ["telemetry loss", "duplicate delivery", "late delivery", "consent loss"]


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


class Arm:
    __slots__ = ("n", "y", "yy", "e", "ee", "x", "xx", "xy")

    def __init__(self):
        self.n = 0
        self.y = self.yy = self.e = self.ee = 0.0
        self.x = {m: 0.0 for m in ("gap", "dup", "late")}
        self.xx = {m: 0.0 for m in ("gap", "dup", "late")}
        self.xy = {m: 0.0 for m in ("gap", "dup", "late")}

    def add(self, s, g, d, l, ev):
        self.n += 1
        self.y += s
        self.yy += s * s
        self.e += ev
        self.ee += ev * ev
        for m, x in (("gap", g), ("dup", d), ("late", l)):
            self.x[m] += x
            self.xx[m] += x * x
            self.xy[m] += x * s


def read_registry(target):
    """the experiment registry as the platform wrote it"""
    with open(os.path.join(target, "experiment_registry_2026.json"), encoding="utf-8") as f:
        return json.load(f)


def q1_rows(target):
    """service 1's install export, one dict a row as csv reads it"""
    with open(os.path.join(target, "install_summary_2026q1.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            yield r


def main(target, figures_path):
    fig = json.load(open(figures_path))
    p = lambda f: os.path.join(target, f)
    reg = read_registry(target)["experiments"]
    design = {e["key"]: e["design"]["treatment"] for e in reg}
    by_title = {norm(e["title"]): e["key"] for e in reg}
    wb = load_workbook(p("data_incident_register_2026.xlsx"), read_only=True)
    ws = wb["Register"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    regrows = [dict(zip(hdr, r)) for r in rows[1:]]
    inc = {by_title[norm(r["experiment"])] for r in regrows if r["scope"] == "experiment" and r["status"] == "confirmed"}
    arms = {}
    for r in q1_rows(target):
        a = arms.setdefault((r["exp_id"], "control" if r["variant"] == "A" else "treatment"), Arm())
        a.add(int(r["n_sessions"]), int(r["sessions_seq_gap"]), int(r["sessions_dup_ids"]), int(r["sessions_late"]),
              int(r["events"]))
    for q in ("install_summary_2026q2.parquet", "install_summary_2026q3.parquet"):
        t = pq.read_table(p(q)).to_pydict()
        for k, arm, s, g, d, l, ev in zip(t["experiment_key"], t["arm"], t["sessions"], t["gap_sessions"],
                                          t["duplicate_sessions"], t["late_sessions"], t["events_received"]):
            arms.setdefault((k, arm), Arm()).add(s, g, d, l, ev)
    keys = sorted({k for k, _ in arms})
    assert len(keys) == 82 and set(keys) == set(design)

    def ratio(a, m):
        n = a.n
        mx, my = a.x[m] / n, a.y / n
        vx = (a.xx[m] - n * mx * mx) / (n - 1)
        vy = (a.yy - n * my * my) / (n - 1)
        cxy = (a.xy[m] - n * mx * my) / (n - 1)
        r = mx / my
        return r, (vx - 2 * r * cxy + r * r * vy) / (my * my * n)

    held = {m: set() for m in NAMES}
    for k in keys:
        c, t = arms[(k, "control")], arms[(k, "treatment")]
        for m in ("gap", "dup", "late"):
            rc, vc = ratio(c, m)
            rt, vt = ratio(t, m)
            if (rt - rc) / sqrt(vc + vt) > Z:
                held[m].add(k)
        ec, et = c.e / c.n, t.e / t.n
        vec = (c.ee - c.n * ec * ec) / (c.n - 1)
        vet = (t.ee - t.n * et * et) / (t.n - 1)
        if (ec - et) / sqrt(vec / c.n + vet / t.n) > Z:
            held["epu"].add(k)
        n, pp = c.n + t.n, design[k]
        if (n * pp - t.n) / sqrt(n * pp * (1 - pp)) > Z:
            held["share"].add(k)
    none = [k for k in keys if k not in inc]
    cap = floor(0.02 * len(none) + 1e-9)
    rec = {m: (len(held[m] & inc), len(held[m] - inc)) for m in NAMES}
    okk = sorted([m for m in NAMES if rec[m][1] <= cap], key=lambda m: (-rec[m][0], rec[m][1]))
    pick = okk[0]
    # the line: per-install variance of the gap-session share over both arms of the experiments without an incident
    X = Y = XX = YY = XY = 0.0
    N = 0
    for k in none:
        for arm in ("control", "treatment"):
            a = arms[(k, arm)]
            X += a.x["gap"]; Y += a.y; XX += a.xx["gap"]; YY += a.yy; XY += a.xy["gap"]; N += a.n
    r = X / Y
    ss = XX - 2 * r * XY + r * r * YY
    s2 = ss / (N - 1) / (Y / N) ** 2
    line = 100 * Z * sqrt(2 * s2 / STD_N)
    # SF2: the reconciliation's confirmed findings are the register's confirmed experiments
    text = " ".join(pg.extract_text() for pg in PdfReader(p("reconciliation_summary_2026.pdf")).pages)
    confirmed = {m.group(1) for m in re.finditer(r"(AV-26-\d{3})\b(.*?)(confirmed|not confirmed)", text, re.S)
                 if m.group(3) == "confirmed"}
    assert confirmed == inc, (sorted(confirmed ^ inc))
    sdk = sdk941(target)
    # compare
    assert NAMES[pick] == fig["call"], (pick, fig["call"])
    assert "%.2f" % line == fig["line"], (line, fig["line"])
    for m in NAMES:
        assert (fig["record"][NAMES[m]]["incidents"], fig["record"][NAMES[m]]["none"]) == rec[m], (m, rec[m])
    assert NAMES[okk[1]] == fig["runner_up"]
    assert {d: v for d, v in fig["sdk941"].items()} == sdk, "SDK 9.4.1 installs differ"
    print("verify: call %s at %.4f points; records %s; SDK 9.4.1 installs still on it, 6 to 19 August: iOS %s; Android %s"
          % (pick, line, rec, [sdk[d]["ios"] for d in sorted(sdk)], [sdk[d]["android"] for d in sorted(sdk)]))


def sdk941(target):
    """the installs that sent from SDK 9.4.1 on a day from 3 to 6 August still on it at each day's end, read with pyarrow
    alone: a client ID first seen on 9.4.2 continuing an older client ID's sequence by one is that install"""
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    cph = ZoneInfo("Europe/Copenhagen")
    t = pq.read_table(os.path.join(target, "collector_client_summary_2026-08.parquet")).to_pylist()
    for r in t:
        r["fb"] = r["first_batch"].astimezone(cph)
        r["lb"] = r["last_batch"].astimezone(cph)
    by = {}
    for r in t:
        by.setdefault(r["client_id"], {})[r["sdk_version"]] = r
    lo, hi = datetime(2026, 8, 3, tzinfo=cph), datetime(2026, 8, 7, tzinfo=cph)
    pop = {c: v["9.4.1"]["platform"] for c, v in by.items() if "9.4.1" in v and v["9.4.1"]["fb"] < hi and v["9.4.1"]["lb"] >= lo}
    ends = {}
    for c, v in by.items():
        if "9.4.2" in v or not any(k != "9.4.2" for k in v):
            continue
        last = max((x for k, x in v.items()), key=lambda x: x["lb"])
        ends[(last["platform"], last["last_seq"])] = (c, last["lb"])
    switch = {}
    for c, v in by.items():
        if "9.4.2" in v:
            if any(k != "9.4.2" for k in v):
                switch[c] = v["9.4.2"]["fb"]
            else:
                n = v["9.4.2"]
                hit = ends.get((n["platform"], n["first_seq"] - 1))
                if hit and hit[1] < n["fb"]:
                    switch[hit[0]] = n["fb"]
    out = {}
    for k in range(6, 20):
        end = datetime(2026, 8, k, tzinfo=cph) + timedelta(days=1)
        cnt = {"ios": 0, "android": 0}
        for c, plat in pop.items():
            if not (c in switch and switch[c] < end):
                cnt[plat] += 1
        out["2026-08-%02d" % k] = cnt
    return out


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    main(os.path.join(os.path.dirname(here), "target"), os.path.join(here, "figures.json"))
