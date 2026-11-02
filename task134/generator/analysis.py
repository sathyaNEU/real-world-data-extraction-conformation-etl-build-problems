"""Every graded figure and every rung, computed from the shipped files in target/ alone (the golden's own path).

The notice is parsed for the centreline, the widths and the berth corners; the certificates give each area's in-situ
maintenance; the surveys give the natural bed beside each part; the load log, the revision, the sampling workbook and
the lab results give the asks.
"""
import csv
import datetime as dt
import math
import os
import re

import numpy as np
from openpyxl import load_workbook

from io_util import pdf_text

CERTS = "maintenance_dredging_certificates_2016-2026.xlsx"
SURV_A = "holmwood_channel_surveys_2016-2023.csv"
SURV_B = "seaward_channel_surveys_2023-2026.csv"
NOTICE = "notice_to_mariners_03-2026.pdf"
LICENCE = "marine_licence_L2021-00317_v2.pdf"
LOADS = "dunmarsh_load_log_2023-2026.csv"
REVISION = "FE_dry_solids_revision_20260330.csv"
SAMPLING = "sediment_sampling_2025-2026.xlsx"
LAB = "aldern_results_FEN26.csv"

REACH_NAMES = ["Outer Channel", "Fend Roads", "Middle Reach", "Inner Reach", "Turning Basin"]
BERTH_NAMES = ["North Quay Berth 1", "North Quay Berth 3", "Container Terminal Berth 5"]
NEW_DEPTH = 14.3


class Notice:
    def __init__(self, tdir):
        txt = pdf_text(os.path.join(tdir, NOTICE)).split("\n")
        self.wp = []
        for i, line in enumerate(txt):
            if re.fullmatch(r"W\d", line.strip()):
                self.wp.append((float(txt[i + 1]), float(txt[i + 2]), float(txt[i + 3])))
        self.parts = {}
        for i, line in enumerate(txt):
            if line.strip() in REACH_NAMES:
                m = re.match(r"([\d.]+) to ([\d.]+)", txt[i + 1])
                self.parts[line.strip()] = dict(c0=float(m.group(1)), c1=float(m.group(2)), width=float(txt[i + 2]),
                                                depth=float(txt[i + 3]))
        self.berths = {}
        for line in txt:
            m = re.match(r"(North Quay Berth \d|Container Terminal Berth 5): ([\d ;]+)\. (.*)", line)
            if m:
                pts = [tuple(float(v) for v in p.split()) for p in m.group(2).split(";")]
                dm = re.search(r"([\d.]+) m", m.group(3))
                self.berths[m.group(1)] = dict(corners=pts, depth=float(dm.group(1)) if dm else None)
        m = re.search(r"([\d.]+) m below Ordnance Datum Newlyn", "\n".join(txt))
        self.cd_below_odn = float(m.group(1))
        self.WP = np.array([[w[1], w[2]] for w in self.wp])
        self.CH = np.array([w[0] for w in self.wp])

    def chain_offset(self, E, N):
        E = np.asarray(E, float)
        N = np.asarray(N, float)
        best = np.full(E.shape, np.inf)
        s_out = np.zeros(E.shape)
        t_out = np.zeros(E.shape)
        for i in range(len(self.WP) - 1):
            a, b = self.WP[i], self.WP[i + 1]
            d = b - a
            L = math.hypot(*d)
            ux, uy = d / L
            px, py = E - a[0], N - a[1]
            u = px * ux + py * uy
            uc = np.clip(u, 0, L)
            dist = np.hypot(E - (a[0] + uc * ux), N - (a[1] + uc * uy))
            cross = ux * py - uy * px
            better = dist < best - 1e-9
            best = np.where(better, dist, best)
            s_out = np.where(better, self.CH[i] + u / 1000.0, s_out)
            t_out = np.where(better, -cross, t_out)
        return s_out, t_out

    def part_of(self, s, t):
        """The maintained reach or basin a point lies in, or None."""
        for name in REACH_NAMES:
            p = self.parts[name]
            if p["c0"] <= s <= p["c1"] and abs(t) <= p["width"] / 2.0:
                return name
        return None


def read_certificates(tdir, reissue="latest"):
    """Monthly certificate rows mapped to area names: list of (month date, area, dry solids, in-situ m3, certificate)."""
    wb = load_workbook(os.path.join(tdir, CERTS), read_only=True, data_only=True)
    codes = {}
    for row in wb["Area codes"].iter_rows(min_row=2, values_only=True):
        codes[row[0]] = row[1]
    rows = []
    for ws in wb.worksheets:
        if ws.title == "Area codes":
            continue
        for row in ws.iter_rows(min_row=5, values_only=True):
            if not row or row[0] is None:
                continue
            month = row[0].date() if isinstance(row[0], dt.datetime) else row[0]
            area = codes.get(row[1], row[1])
            rows.append(dict(month=month, area=area, loads=row[2], tds=float(row[3]), vol=float(row[4]), cert=str(row[5])))
    if reissue == "latest":
        keep = {}
        for r in rows:
            k = (r["month"], r["area"])
            if k not in keep or r["cert"] > keep[k]["cert"]:
                keep[k] = r
        rows = sorted(keep.values(), key=lambda r: (r["month"], r["area"]))
    return rows


def record_mean(tdir, window="licence", reissue="latest"):
    """Each area's mean yearly in-situ volume over the licence years 2016-17 to 2025-26 (October 2016 to September 2026)."""
    rows = read_certificates(tdir, reissue)
    if window == "licence":
        lo, hi = dt.date(2016, 10, 1), dt.date(2026, 9, 1)
    elif window == "financial":
        lo, hi = dt.date(2016, 4, 1), dt.date(2026, 3, 1)
    elif window == "pre2021":
        lo, hi = dt.date(2016, 10, 1), dt.date(2021, 3, 1)
    else:
        raise ValueError(window)
    years = (hi.year - lo.year) + (hi.month - lo.month + 1) / 12.0
    tot = {}
    for r in rows:
        if lo <= r["month"] <= hi:
            tot[r["area"]] = tot.get(r["area"], 0.0) + r["vol"]
    return {a: v / years for a, v in tot.items()}


def read_surveys(tdir, which=("A", "B")):
    """(E, N, depth below CD, contractor, date) arrays from both contractors, the ODN elevations converted."""
    nt = Notice(tdir)
    E, N, Z, C = [], [], [], []
    if "A" in which:
        with open(os.path.join(tdir, SURV_A), newline="") as f:
            for r in csv.DictReader(f):
                z = float(r["DEPTH_M_BCD"])
                if z <= -99:
                    continue
                E.append(float(r["EASTING"]))
                N.append(float(r["NORTHING"]))
                Z.append(z)
                C.append(0)
    if "B" in which:
        with open(os.path.join(tdir, SURV_B), newline="") as f:
            for r in csv.DictReader(f):
                E.append(float(r["x_osgb36"]))
                N.append(float(r["y_osgb36"]))
                Z.append(-float(r["z_m_odn"]) - nt.cd_below_odn)
                C.append(1)
    return np.array(E), np.array(N), np.array(Z), np.array(C)


def natural_bed(tdir, buffer=50.0, stat="mean", which=("A", "B"), cache={}):
    """The natural bed depth beside each reach and the basin: survey cells beyond the maintained width plus the buffer,
    within 300 m of it (the basin from its open south side)."""
    key = (tdir, buffer, stat, which)
    if key in cache:
        return cache[key]
    nt = Notice(tdir)
    E, N, Z, C = read_surveys(tdir, which)
    s, t = nt.chain_offset(E, N)
    out = {}
    for name in REACH_NAMES:
        p = nt.parts[name]
        half = p["width"] / 2.0
        ins = (s >= p["c0"]) & (s < p["c1"]) if name != "Turning Basin" else (s >= p["c0"]) & (s <= p["c1"])
        if name == "Turning Basin":
            m = ins & (t < -(half + buffer)) & (t >= -(half + 300.0))
        else:
            m = ins & (np.abs(t) > half + buffer) & (np.abs(t) <= half + 300.0)
        v = Z[m]
        out[name] = float(np.mean(v) if stat == "mean" else np.median(v))
    cache[key] = out
    return out


def call(tdir, buffer=50.0, stat="mean", window="licence", reissue="latest", which=("A", "B"), held_now=None):
    """The golden: each deepened part's record mean scaled by its depth below the natural bed, new over now."""
    V = record_mean(tdir, window, reissue)
    nat = natural_bed(tdir, buffer, stat, which)
    nt = Notice(tdir)
    parts = {}
    for name in REACH_NAMES:
        h0 = nt.parts[name]["depth"] if held_now is None else held_now
        parts[name] = V[name] * (NEW_DEPTH - nat[name]) / (h0 - nat[name])
    parts["Berth pockets"] = sum(V[b] for b in BERTH_NAMES)
    return dict(parts=parts, total=sum(parts.values()), V=V, nat=nat)


def rungs(tdir):
    """Every rung of the ladder on the shipped data."""
    V = record_mean(tdir)
    nat = natural_bed(tdir)
    nt = Notice(tdir)
    berths = sum(V[b] for b in BERTH_NAMES)
    out = {}
    out["R0 carry"] = sum(V[n] for n in REACH_NAMES) + berths
    out["R1 depth ratio"] = sum(V[n] * NEW_DEPTH / nt.parts[n]["depth"] for n in REACH_NAMES) + berths
    ey = 0.0
    for n in REACH_NAMES:
        h0, hn = nt.parts[n]["depth"], NEW_DEPTH
        e = lambda h: 1.0 - (nat[n] / h) ** 2.5
        ey += V[n] * e(hn) / e(h0)
    out["R2 trapping efficiency"] = ey + berths
    # R3: one line of yearly infill per square metre on held depth across every maintained area
    xs, ys = [], []
    areas = {}
    for n in REACH_NAMES:
        p = nt.parts[n]
        areas[n] = (p["c1"] - p["c0"]) * 1000.0 * p["width"]
        xs.append(p["depth"])
        ys.append(V[n] / areas[n])
    for b in BERTH_NAMES:
        cs = nt.berths[b]["corners"]
        a = math.hypot(cs[1][0] - cs[0][0], cs[1][1] - cs[0][1]) * math.hypot(cs[2][0] - cs[1][0], cs[2][1] - cs[1][1])
        xs.append(nt.berths[b]["depth"])
        ys.append(V[b] / a)
    slope = float(np.polyfit(xs, ys, 1)[0])
    out["R3 pooled depth regression"] = sum(V[n] + slope * (NEW_DEPTH - nt.parts[n]["depth"]) * areas[n] for n in REACH_NAMES) + berths
    # the golden's own family members
    g = call(tdir)
    out["golden"] = g["total"]
    k = {n: V[n] / areas[n] / (nt.parts[n]["depth"] - nat[n]) for n in REACH_NAMES}
    kc = sum(V[n] / areas[n] * (nt.parts[n]["depth"] - nat[n]) for n in REACH_NAMES) / sum((nt.parts[n]["depth"] - nat[n]) ** 2 for n in REACH_NAMES)
    out["golden, common k"] = sum(V[n] + kc * (NEW_DEPTH - nt.parts[n]["depth"]) * areas[n] for n in REACH_NAMES) + berths
    return out, dict(V=V, nat=nat, k=k, kc=kc, areas=areas, slope=slope)


# ---------------- asks ----------------

def site_boxes(tdir):
    txt = pdf_text(os.path.join(tdir, LICENCE))
    boxes = {}
    cur = None
    lines = txt.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        m = re.match(r"(Fend Spit|Wenning Deep) \((FS|WD)\)", ln)
        if m:
            cur = m.group(1)
            boxes[cur] = []
        m2 = re.match(r"(\d+) ([\d.]+)' N", ln)
        if m2 and cur:
            m3 = re.match(r"(\d+) ([\d.]+)' E", lines[i + 1].strip())
            boxes[cur].append((int(m2.group(1)) + float(m2.group(2)) / 60.0, int(m3.group(1)) + float(m3.group(2)) / 60.0))
            i += 1
        i += 1
    return {k: (min(p[0] for p in v), max(p[0] for p in v), min(p[1] for p in v), max(p[1] for p in v)) for k, v in boxes.items()}


def bst(t):
    y = t.year

    def last_sunday(month):
        d = dt.datetime(y, month, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d.replace(hour=1)
    return t + dt.timedelta(hours=1) if last_sunday(3) <= t < last_sunday(10) else t


def ds_fractions(tdir):
    wb = load_workbook(os.path.join(tdir, SAMPLING), read_only=True, data_only=True)
    out = []
    for row in wb["Area summary"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        comp = row[1].date() if isinstance(row[1], dt.datetime) else row[1]
        out.append((comp, row[3], float(row[4])))
    return out


def ask_a(tdir, site_by="position", revision=True, clock="local", hired=True, campaign="completed"):
    """Wet tonnes placed at each site in each quarter of the licence year 2025-26."""
    codes = {}
    wb = load_workbook(os.path.join(tdir, CERTS), read_only=True, data_only=True)
    for row in wb["Area codes"].iter_rows(min_row=2, values_only=True):
        codes[row[0]] = row[1]
    boxes = site_boxes(tdir)
    fr = ds_fractions(tdir)
    rev = {}
    with open(os.path.join(tdir, REVISION), newline="") as f:
        for r in csv.DictReader(f):
            rev[r["trip_ref"]] = float(r["dry_solids_t_revised"])
    loads = []
    with open(os.path.join(tdir, LOADS), newline="") as f:
        for r in csv.DictReader(f):
            loads.append(r)
    # trip references: the Fend Endeavour's loads numbered by local day in loading order
    seq = {}
    for r in sorted(loads, key=lambda r: r["loading_start_utc"]):
        if r["vessel"] != "Fend Endeavour":
            continue
        tl = dt.datetime.strptime(r["loading_start_utc"], "%Y-%m-%dT%H:%M:00Z")
        ld = bst(tl).date()
        seq[ld] = seq.get(ld, 0) + 1
        r["trip_ref"] = "FE%s/%d" % (ld.strftime("%y%m%d"), seq[ld])
    out = {}
    monthly = {}
    for r in loads:
        td = dt.datetime.strptime(r["dump_start_utc"], "%Y-%m-%dT%H:%M:00Z")
        tl = bst(td) if clock == "local" else td
        if not (dt.datetime(2025, 10, 1) <= tl < dt.datetime(2026, 10, 1)):
            continue
        q = {10: 1, 11: 1, 12: 1, 1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4}[tl.month]
        if site_by == "position":
            la, lo = float(r["dump_lat"]), float(r["dump_lon"])
            site = None
            for name, (a0, a1, o0, o1) in boxes.items():
                if a0 <= la <= a1 and o0 <= lo <= o1:
                    site = name
            assert site is not None, r["load_ref"]
        else:
            site = r["planned_site"]
        if r["dry_solids_t"]:
            tds = float(r["dry_solids_t"])
            if revision and r.get("trip_ref") in rev:
                tds = rev[r["trip_ref"]]
        else:
            if not hired:
                continue
            vh, rho = float(r["hopper_m3"]), float(r["mixture_density_t_m3"])
            tds = vh * 2.65 * (rho - 1.025) / 1.625
        area = codes[r["area"]]
        month0 = dt.date(tl.year, tl.month, 1)
        cand = [(c, f) for c, a, f in fr if a == area and (c < month0 if campaign == "completed" else True)]
        comp, f = max(cand)
        wet = tds / f
        out[(site, q)] = out.get((site, q), 0.0) + wet
        monthly[(site, tl.year, tl.month)] = monthly.get((site, tl.year, tl.month), 0.0) + wet
    return out, monthly


def lab_samples(tdir, hg="convert"):
    vals = {}
    with open(os.path.join(tdir, LAB), newline="") as f:
        for r in csv.DictReader(f):
            v = float(r["result"])
            if r["determinand"] == "Mercury" and r["units"] == "ug/kg" and hg == "convert":
                v = v / 1000.0
            vals.setdefault(r["client_ref"], {})[r["determinand"]] = v
    return vals


def ask_b(tdir, part_by="position", qa="pair", hg="convert"):
    """Each reach's and the basin's mean cadmium, mercury, lead and copper (mg/kg dry weight) in the 2026 samples."""
    nt = Notice(tdir)
    wb = load_workbook(os.path.join(tdir, SAMPLING), read_only=True, data_only=True)
    plan = {}
    for row in wb["Station plan"].iter_rows(min_row=2, values_only=True):
        if row[0]:
            plan[row[0]] = row[1]
    field = []
    for row in wb["Field log 2026"].iter_rows(min_row=2, values_only=True):
        if row[0]:
            d = row[2].date() if isinstance(row[2], dt.datetime) else row[2]
            hh, mm = str(row[3]).split(":")
            field.append(dict(ref=row[0], station=row[1], t=dt.datetime(d.year, d.month, d.day, int(hh), int(mm)),
                              E=float(row[4]), N=float(row[5])))
    vals = lab_samples(tdir, hg)
    prim = [x for x in field if x["station"] != "QA"]
    dups = [x for x in field if x["station"] == "QA"]
    pairs = {}
    for d in dups:
        best = min(prim, key=lambda p: math.hypot(p["E"] - d["E"], p["N"] - d["N"]) + abs((p["t"] - d["t"]).total_seconds()) / 60.0)
        pairs[best["ref"]] = d["ref"]
    groups = {}
    for p in prim:
        if part_by == "position":
            s, t = nt.chain_offset([p["E"]], [p["N"]])
            part = nt.part_of(float(s[0]), float(t[0]))
        else:
            part = plan[p["station"]]
        if part not in REACH_NAMES:
            continue
        v = dict(vals[p["ref"]])
        if qa == "pair" and p["ref"] in pairs:
            dv = vals[pairs[p["ref"]]]
            v = {k: 0.5 * (v[k] + dv[k]) for k in v}
        groups.setdefault(part, []).append(v)
        if qa == "separate" and p["ref"] in pairs:
            groups[part].append(dict(vals[pairs[p["ref"]]]))
    out = {}
    for part, vs in groups.items():
        for det in ("Cadmium", "Mercury", "Lead", "Copper"):
            out[(part, det)] = float(np.mean([v[det] for v in vs]))
    return out
