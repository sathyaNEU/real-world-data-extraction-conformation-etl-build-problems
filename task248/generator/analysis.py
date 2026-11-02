"""Every rung, the golden and the asks, computed from target/ alone (no generator state)."""
import csv, json, os, sys, datetime as dt
import numpy as np
from zoneinfo import ZoneInfo
from openpyxl import load_workbook

CHI = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
SEASON = (dt.datetime(2026, 4, 1), dt.datetime(2026, 11, 1))
K = {"REC-90 ethanol-free": 0.00068, "E10 unleaded": 0.00069, "Diesel": 0.00046}
POSK = {"REC-90 NE": "REC-90 ethanol-free", "E10 87": "E10 unleaded", "MARINE DSL": "Diesel"}
LIMIT = 25.0


def rcsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def loc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(CHI).replace(tzinfo=None)


def lt(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def hat(h, knots):
    h = np.asarray(h, dtype=float)
    B = np.zeros((len(h), len(knots)))
    for j, k in enumerate(knots):
        v = np.zeros(len(h))
        if j > 0:
            l = knots[j - 1]; mk = (h >= l) & (h <= k); v[mk] = (h[mk] - l) / (k - l)
        else:
            v[h <= k] = 1.0
        if j < len(knots) - 1:
            r = knots[j + 1]; mk = (h >= k) & (h <= r); v[mk] = (r - h[mk]) / (r - k)
        else:
            v[h >= k] = 1.0
        B[:, j] = v
    return B


class Pack:
    def __init__(self, target):
        self.t = target
        wb = load_workbook(os.path.join(target, "tank_register.xlsx"), data_only=True)
        ws = wb["Register"]
        rows = list(ws.iter_rows(values_only=True))
        hi = [i for i, r in enumerate(rows) if r and r[0] == "Tank"][0]
        hdr = rows[hi]
        self.reg = {}
        for r in rows[hi + 1:]:
            if not r or not r[0]:
                continue
            d = dict(zip(hdr, r))
            self.reg[d["Tank"]] = {"marina": d["Marina"], "product": d["Product"], "cap": d["Capacity (gal)"],
                                   "D": float(d["Diameter (in)"]), "L": float(d["Length (in)"]), "chart": d["Chart no."],
                                   "re": float(d["Reorder height (in)"]), "half": float(d["Half-full height (in)"]),
                                   "fill": float(d["Normal fill height (in)"])}
        self.charts = {}
        for r in rcsv(os.path.join(target, "tank_charts.csv")):
            self.charts.setdefault(r["chart_no"], []).append((float(r["height_in"]), float(r["gallons"])))
        for k in self.charts:
            a = np.array(sorted(self.charts[k]))
            self.charts[k] = (a[:, 0], a[:, 1])
        self.setup = rcsv(os.path.join(target, "atg_tank_setup.csv"))
        wb = load_workbook(os.path.join(target, "dock_piping.xlsx"), data_only=True)
        prow = list(wb.active.iter_rows(values_only=True))
        hi = [i for i, r in enumerate(prow) if r and r[0] == "Marina"][0]
        self.piping = {(r[0], r[2]): r[4] for r in prow[hi + 1:] if r and r[0]}
        self.name2tanks = {}
        for tid, g in self.reg.items():
            self.name2tanks.setdefault(g["marina"], []).append(tid)

    def chart(self, tid, h):
        hh, gg = self.charts[self.reg[tid]["chart"]]
        return np.interp(h, hh, gg)

    def tid_for(self, console, tank, when_local):
        for s in self.setup:
            if s["console_sn"] == console and int(s["tank"]) == int(tank):
                a = dt.datetime.strptime(s["in_service_from"], "%Y-%m-%d")
                b = dt.datetime.strptime(s["in_service_to"], "%Y-%m-%d") if s["in_service_to"] else dt.datetime(2100, 1, 1)
                if a <= when_local < b + dt.timedelta(days=1):
                    return s["marina_tank_ref"]
        return None

    def tid_by_console(self, console, tank):
        cand = [s["marina_tank_ref"] for s in self.setup if s["console_sn"] == console and int(s["tank"]) == int(tank)]
        return cand[0] if len(cand) == 1 else cand

    # ---------------- gauge records ----------------
    def inventory(self, redate=True):
        """rows per register tank: (local time, seq, height, temp, gross, tc, water); storm-reset rows re-dated on
        the console's sequence chain"""
        raw = rcsv(os.path.join(self.t, "atg_inventory_2026.csv"))
        by_ct = {}
        for r in raw:
            by_ct.setdefault((r["console_sn"], int(r["tank"])), []).append(r)
        out = {}
        for (cs, tn), rows in by_ct.items():
            rows.sort(key=lambda r: int(r["record_seq"]))
            times = [lt(r["reading_time"]) for r in rows]
            bad = [i for i, t in enumerate(times) if t.year != 2026]
            if bad and redate:
                i0, i1 = bad[0], bad[-1]
                nxt = times[i1 + 1]           # first reading after the clock was set
                off = (nxt - dt.timedelta(hours=2)) - times[i1]
                for i in bad:
                    times[i] = times[i] + off
            for r, t in zip(rows, times):
                if t.year != 2026:
                    continue
                tid = self.tid_for(cs, tn, t)
                out.setdefault(tid, []).append((t, int(r["record_seq"]), float(r["height_in"]), float(r["temp_f"]),
                                                float(r["gross_gal"]), float(r["tc_gal_60f"]), float(r["water_in"])))
        for k in out:
            out[k].sort()
        return out

    def deliveries(self):
        out = {}
        for r in rcsv(os.path.join(self.t, "atg_deliveries_2026.csv")):
            s, e = lt(r["start_time"]), lt(r["end_time"])
            tid = self.tid_for(r["console_sn"], r["tank"], s)
            out.setdefault(tid, []).append({"start": s, "end": e, "h0": float(r["start_height_in"]), "h1": float(r["end_height_in"]),
                                            "T0": float(r["start_temp_f"]), "T1": float(r["end_temp_f"]),
                                            "g0": float(r["start_gross_gal"]), "g1": float(r["end_gross_gal"]),
                                            "n0": float(r["start_tc_gal_60f"]), "n1": float(r["end_tc_gal_60f"])})
        return out

    def bols(self):
        out = {}
        names = {g["marina"].upper(): g["marina"] for g in self.reg.values()}
        for r in rcsv(os.path.join(self.t, "bols_2026.csv")):
            m = names[r["ship_to"]]
            tid = [k for k in self.name2tanks[m] if k.split("-")[1] == r["tank_ref"][2:]][0]
            out.setdefault(tid, []).append({"t": dt.datetime.strptime(r["drop_time"], "%m/%d/%Y %H:%M"),
                                            "net": float(r["net_gal_60f"]), "gross": float(r["gross_gal"]),
                                            "temp": float(r["product_temp_f"]), "bol": r["bol_no"]})
        return out

    def sales_legacy(self):
        out = {}
        for r in rcsv(os.path.join(self.t, "dock_sales_legacy_2026.csv")):
            tid = self.piping[(r["store_name"], r["disp_hose"])]
            out.setdefault(tid, []).append((dt.datetime.strptime(r["sale_time"], "%m/%d/%Y %H:%M:%S"), float(r["gallons"]), r["product"]))
        for k in out:
            out[k].sort()
        return out


def build_obs(pk, tid, inv, dls, bls, sales, season=True, use_dlv_points=False):
    """intervals (hs, he, d, S) and deliveries (hs, he, d, bol) in net gallons at 60 F"""
    k = K[pk.reg[tid]["product"]]
    lo, hi = SEASON if season else (dt.datetime(2026, 1, 1), dt.datetime(2027, 1, 1))
    rows = [r for r in inv.get(tid, []) if lo <= r[0] < hi]
    D = [d for d in dls.get(tid, []) if lo <= d["start"] < hi]
    st = np.array([s[0].timestamp() for s in sales.get(tid, [])])
    sg = np.array([s[1] for s in sales.get(tid, [])])
    pts = [(r[0], r[2], r[3], r[5]) for r in rows]
    if use_dlv_points:
        for d in D:
            pts.append((d["start"], d["h0"], d["T0"], d["n0"]))
            pts.append((d["end"], d["h1"], d["T1"], d["n1"]))
        pts.sort()
    spans = [(d["start"].timestamp(), d["end"].timestamp()) for d in D]
    hs, he, dd, SS = [], [], [], []
    for a, b in zip(pts[:-1], pts[1:]):
        ta, tb = a[0].timestamp(), b[0].timestamp()
        if tb - ta > 2.1 * 3600 or tb <= ta:
            continue
        if any(x < tb and y > ta for x, y in spans) and not (use_dlv_points and any(abs(x - ta) < 1 and abs(y - tb) < 1 for x, y in spans)):
            continue
        if use_dlv_points and any(abs(x - ta) < 1 and abs(y - tb) < 1 for x, y in spans):
            continue
        m = (st > ta) & (st <= tb)
        Tm = (a[2] + b[2]) / 2.0
        Sn = float(sg[m].sum()) * (1 - k * (Tm - 60.0))
        hs.append(a[1]); he.append(b[1]); dd.append(b[3] - a[3] + Sn); SS.append(Sn)
    dhs, dhe, ddd, bn = [], [], [], []
    for d in D:
        cand = [b for b in bls.get(tid, []) if d["start"] - dt.timedelta(hours=3) <= b["t"] <= d["start"] + dt.timedelta(minutes=30)]
        if not cand:
            continue
        b = cand[0]
        m = (st > d["start"].timestamp()) & (st <= d["end"].timestamp())
        Tm = (d["T0"] + d["T1"]) / 2.0
        Sn = float(sg[m].sum()) * (1 - k * (Tm - 60.0))
        dhs.append(d["h0"]); dhe.append(d["h1"]); ddd.append(d["n1"] - d["n0"] + Sn - b["net"]); bn.append(b["net"])
    return (np.array(hs), np.array(he), np.array(dd), np.array(SS)), (np.array(dhs), np.array(dhe), np.array(ddd), np.array(bn))


def three(c_at):
    lower = c_at[1] - c_at[0]; upper = c_at[2] - c_at[1]; full = c_at[2] - c_at[0]
    return lower, upper, full


def fit_hat(pk, tid, iv, dl, step=3.0, use_del=True, meter=True, mfix=None):
    hs, he, dd, SS = iv
    dhs, dhe, ddd, bn = dl
    g = pk.reg[tid]
    lo = float(np.floor(min(hs.min(), he.min()))); hi_ = float(np.ceil(max(hs.max(), he.max())))
    knots = np.unique(np.concatenate([np.arange(lo, hi_ + step, step), [g["re"], g["half"], g["fill"]]]))
    knots = knots[(knots >= lo - 1e-9) & (knots <= hi_ + step)]
    Xi = (hat(he, knots) - hat(hs, knots))[:, 1:]
    y = dd.copy()
    if mfix is not None:
        y = y - mfix / (1 + mfix) * SS * 0 - (SS - SS / (1 + mfix))
        meter = False
    A = [np.hstack([Xi, SS[:, None]]) if meter else Xi]
    Y = [y]
    if use_del and len(ddd):
        Xd = (hat(dhe, knots) - hat(dhs, knots))[:, 1:]
        A.append(np.hstack([Xd, np.zeros((len(ddd), 1))]) if meter else Xd)
        Y.append(ddd)
    A = np.vstack(A); Y = np.concatenate(Y)
    coef = np.linalg.solve(A.T @ A + 1e-7 * np.eye(A.shape[1]), A.T @ Y)
    Bg = hat(np.array([g["re"], g["half"], g["fill"]]), knots)[:, 1:]
    c = Bg @ coef[:Bg.shape[1]]
    return three(c), (float(coef[-1]) if meter else None)


def fit_geom(pk, tid, iv, dl, exact=True):
    """a probe offset delta and a chart scale eps: c(h) = chart(h) - (1 - eps) * chart(h - delta) (exact), or its
    first-order form eps * chart(h) + delta * dchart/dh; plus a dock meter term"""
    hs, he, dd, SS = iv
    dhs, dhe, ddd, bn = dl
    g = pk.reg[tid]
    hh, gg = pk.charts[g["chart"]]
    V = lambda h: np.interp(h, hh, gg)
    dV = lambda h: (V(h + 0.25) - V(h - 0.25)) / 0.5
    def cfun(h, delta, eps):
        if exact:
            return V(h) - (1 - eps) * V(h - delta)
        return eps * V(h) + delta * dV(h)
    best = None
    for delta in np.arange(-3.0, 3.0001, 0.01):
        Xi = np.column_stack([cfun(he, delta, 0) - cfun(hs, delta, 0), V(he) - V(hs), SS])
        Xd = np.column_stack([cfun(dhe, delta, 0) - cfun(dhs, delta, 0), V(dhe) - V(dhs), np.zeros(len(ddd))])
        # c = A0(delta) + eps * V (exact form is linear in eps after expansion: V(h)-V(h-d)+eps V(h-d))
        if exact:
            Xi[:, 1] = V(he - delta) - V(hs - delta); Xd[:, 1] = V(dhe - delta) - V(dhs - delta)
        A = np.vstack([Xi, Xd]); Y = np.concatenate([dd, ddd])
        # first column has a fixed coefficient of 1: move it to the left side
        Yr = Y - A[:, 0]
        B = A[:, 1:]
        coef, res, *_ = np.linalg.lstsq(B, Yr, rcond=None)
        rss = float(((Yr - B @ coef) ** 2).sum())
        if best is None or rss < best[0]:
            best = (rss, delta, coef)
    _, delta, coef = best
    eps, m = coef[0], coef[1]
    hts = np.array([g["re"], g["half"], g["fill"]])
    c = cfun(hts, delta, 0) + eps * (V(hts - delta) if exact else V(hts))
    return three(c), float(m), float(delta), float(eps)


def cycles(pk, tid, inv, dls, sales, m_hat):
    """anchored misstatement between the register heights read passage by passage (interpolated crossings)"""
    g = pk.reg[tid]
    k = K[g["product"]]
    lo, hi = SEASON
    rows = [r for r in inv.get(tid, []) if lo <= r[0] < hi]
    D = [d for d in dls.get(tid, []) if lo <= d["start"] < hi]
    st = np.array([s[0].timestamp() for s in sales.get(tid, [])]); sg = np.array([s[1] for s in sales.get(tid, [])])
    # cumulative true outflow (net) from the start, and the gauge tc, at each reading; split at deliveries
    segs, cur = [], []
    di = 0
    Ds = sorted(D, key=lambda d: d["start"])
    for r in rows:
        while di < len(Ds) and Ds[di]["start"] <= r[0]:
            if cur:
                segs.append(cur)
            cur = []
            di += 1
        cur.append(r)
    if cur:
        segs.append(cur)
    res = {"lower": [], "upper": [], "full": []}
    for seg in segs:
        if len(seg) < 3:
            continue
        cum = [0.0]
        for a, b in zip(seg[:-1], seg[1:]):
            msk = (st > a[0].timestamp()) & (st <= b[0].timestamp())
            Tm = (a[3] + b[3]) / 2.0
            cum.append(cum[-1] + float(sg[msk].sum()) / (1 + m_hat) * (1 - k * (Tm - 60.0)))
        h = np.array([x[2] for x in seg]); tc = np.array([x[5] for x in seg]); cum = np.array(cum)
        def at(H):
            # first crossing downward through height H
            for i in range(len(h) - 1):
                if h[i] >= H > h[i + 1]:
                    f = (h[i] - H) / (h[i] - h[i + 1])
                    return tc[i] + f * (tc[i + 1] - tc[i]), cum[i] + f * (cum[i + 1] - cum[i])
            return None
        A, Bm, C = at(g["fill"]), at(g["half"]), at(g["re"])
        # misstatement between heights = chart change - true change = (tc2 - tc1) + outflow between
        if Bm and C:
            res["lower"].append(-((C[0] - Bm[0]) + (C[1] - Bm[1])))
        if A and Bm:
            res["upper"].append(-((Bm[0] - A[0]) + (Bm[1] - A[1])))
        if A and C:
            res["full"].append(-((C[0] - A[0]) + (C[1] - A[1])))
    return tuple(float(np.mean(res[x])) if res[x] else float("nan") for x in ("lower", "upper", "full")), {x: len(res[x]) for x in res}


def largest(parts):
    labels = ["reorder and half-full", "half-full and normal fill", "reorder and normal fill"]
    i = int(np.argmax(np.abs(parts)))
    return abs(parts[i]), labels[i]


def r0_monthly(pk, tid, inv, dls, bls, sales):
    """FS-3 4.1: closing against opening plus deliveries less sales, within 1 per cent of sales plus 130"""
    k = K[pk.reg[tid]["product"]]
    rows = inv.get(tid, [])
    fails, worst = 0, 0.0
    for mo in range(4, 11):
        a = dt.datetime(2026, mo, 1); b = dt.datetime(2026, mo + 1, 1)
        ra = [r for r in rows if r[0] >= a]; rb = [r for r in rows if r[0] >= b]
        if not ra or not rb:
            continue
        t0, t1 = ra[0][0], rb[0][0]
        dl = sum(x["net"] for x in bls.get(tid, []) if t0 <= x["t"] < t1)
        sold = sum(s[1] for s in sales.get(tid, []) if t0 < s[0] <= t1) * (1 - k * (np.mean([ra[0][3], rb[0][3]]) - 60.0))
        os_ = rb[0][5] - (ra[0][5] + dl - sold)
        allowed = 0.01 * sold + 130
        worst = max(worst, abs(os_) / allowed)
        fails += abs(os_) > allowed
    return fails, worst


# ---------------- the asks ----------------
def ask_days(pk, inv=None, redate=True, by_current=False, utc_days=False):
    """local days of 2026 with no inventory reading per register tank"""
    raw = rcsv(os.path.join(pk.t, "atg_inventory_2026.csv"))
    by_ct = {}
    for r in raw:
        by_ct.setdefault((r["console_sn"], int(r["tank"])), []).append(r)
    latest = {}
    for s in pk.setup:
        key = (s["site_id"], int(s["tank"]))
        if key not in latest or s["in_service_from"] > latest[key]["in_service_from"]:
            latest[key] = s
    seen = {}
    for (cs, tn), rows in by_ct.items():
        rows.sort(key=lambda r: int(r["record_seq"]))
        times = [lt(r["reading_time"]) for r in rows]
        utcs = list(times)
        bad = [i for i, t in enumerate(times) if t.year != 2026]
        if bad and redate:
            i1 = bad[-1]
            off = (times[i1 + 1] - dt.timedelta(hours=2)) - times[i1]
            for i in bad:
                times[i] = times[i] + off
                utcs[i] = utcs[i] + off
        for r, t, u in zip(rows, times, utcs):
            day = (u if utc_days else t)
            if day.year != 2026:
                continue
            if by_current:
                tid = latest[(r["site_id"], tn)]["marina_tank_ref"]
            else:
                tid = pk.tid_for(cs, tn, t)
            seen.setdefault(tid, set()).add(day.date())
    year = {dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)}
    return {tid: len(year - seen.get(tid, set())) for tid in pk.reg}


def ask_tests(pk, redate=True, dedupe=True, utc_months=False):
    rows = rcsv(os.path.join(pk.t, "atg_leak_tests_2026.csv"))
    by = {}
    for r in rows:
        key = (r["console_sn"], int(r["tank"]), int(r["test_no"]))
        by.setdefault(key, []).append(r)
    tests = []
    for key, rs in by.items():
        rs.sort(key=lambda r: int(r["rec_id"]))
        if dedupe:
            tests.append((key, rs[0], rs))
        else:
            for r in rs:
                tests.append((key, r, [r]))
    # dates: a test's own (first) logged time when it is 2026 and is not a later re-poll; else from the sequence
    per_ct = {}
    for key, r, rs in tests:
        per_ct.setdefault(key[:2], []).append((key[2], r, rs))
    dated = []
    for ct, lst in per_ct.items():
        lst.sort(key=lambda x: x[0])
        anchor = {}
        for no, r, rs in lst:
            t = loc(r["logged_utc"])
            if t.year == 2026 and t.weekday() == 6 and t.hour >= 21:
                anchor[no] = t
        for no, r, rs in lst:
            t = loc(r["logged_utc"])
            if utc_months:
                t = dt.datetime.strptime(r["logged_utc"], "%Y-%m-%dT%H:%M:%SZ")
            if not redate:
                d = t
            elif no in anchor and not utc_months:
                d = anchor[no]
            else:
                prev = [a for a in anchor if a < no]
                nxt = [a for a in anchor if a > no]
                if prev:
                    a = max(prev); d = anchor[a] + dt.timedelta(days=7 * (no - a))
                elif nxt:
                    a = min(nxt); d = anchor[a] - dt.timedelta(days=7 * (a - no))
                else:
                    d = t
            if d.year != 2026:
                continue
            tid = pk.tid_for(ct[0], ct[1], d)
            dated.append((tid, d, r["result"]))
    passed = {(tid, d.month) for tid, d, res in dated if res == "PASS"}
    out = {}
    for tid, g in pk.reg.items():
        miss = sum(1 for mo in range(1, 13) if (tid, mo) not in passed)
        out.setdefault(g["marina"], 0)
        out[g["marina"]] += miss
    return out


def ask_gallons(pk, shadow="match", grade_basis="price", settle=True):
    """2026 dock gallons by marina and product. shadow: 'match' drops the new system's rows before the legacy
    export ends (its shadow copy of the card sales), 'both' keeps both, 'new' drops the legacy rows from the
    shadow start. grade_basis: 'price' reads each new row's product from its price, 'table' from the grade table"""
    leg = rcsv(os.path.join(pk.t, "dock_sales_legacy_2026.csv"))
    price_of = {}
    for r in leg:
        price_of[round(float(r["price"]), 2)] = POSK[r["product"]]
    newrows = []
    with open(os.path.join(pk.t, "dock_sales_2026-11-09_2026-12-31.jsonl"), encoding="utf-8") as f:
        for line in f:
            newrows.append(json.loads(line))
    def sale_time(j):
        t = loc(j["ts"])
        if settle and j["tender"] == "CARD":
            return dt.datetime(t.year, t.month, t.day) - dt.timedelta(days=1) + dt.timedelta(hours=12)
        return t
    first_new = min(sale_time(j) for j in newrows)
    last_legacy = max(dt.datetime.strptime(r["sale_time"], "%m/%d/%Y %H:%M:%S") for r in leg)
    out = {}
    for r in leg:
        t = dt.datetime.strptime(r["sale_time"], "%m/%d/%Y %H:%M:%S")
        if shadow == "new" and t >= first_new:
            continue
        key = (r["store_name"], POSK[r["product"]])
        out[key] = out.get(key, 0.0) + float(r["gallons"])
    grades = {(r["site"], int(r["grade"])): (r["site_name"], POSK[r["description"]]) for r in rcsv(os.path.join(pk.t, "pos_grades.csv"))}
    for j in newrows:
        t = sale_time(j)
        if shadow == "match" and t <= last_legacy:
            continue
        if t.year != 2026:
            continue
        name, prod = grades[(j["site"], j["grade"])]
        if grade_basis == "price":
            prod = price_of[round(float(j["ppg"]), 2)]
        key = (name, prod)
        out[key] = out.get(key, 0.0) + float(j["gal"])
    return out


def analyse(target):
    pk = Pack(target)
    inv = pk.inventory()
    dls = pk.deliveries()
    bls = pk.bols()
    sales = pk.sales_legacy()
    res = {"tanks": {}}
    for tid in pk.reg:
        iv, dl = build_obs(pk, tid, inv, dls, bls, sales)
        g = pk.reg[tid]
        Vfull = float(pk.chart(tid, g["fill"]) - pk.chart(tid, g["re"]))
        eps_d = float(dl[2].sum() / dl[3].sum()) if len(dl[3]) else 0.0
        r1 = abs(eps_d) * Vfull
        r1b = float(np.abs(dl[2]).mean()) if len(dl[2]) else 0.0
        r1b = abs(float(dl[2].mean())) if len(dl[2]) else 0.0
        r2, _ = fit_hat(pk, tid, iv, dl, 3.0, use_del=False, meter=False)
        gold, m_hat = fit_hat(pk, tid, iv, dl, 3.0, use_del=True, meter=True)
        g6, _ = fit_hat(pk, tid, iv, dl, 6.0, use_del=True, meter=True)
        iv2, dl2 = build_obs(pk, tid, inv, dls, bls, sales, use_dlv_points=True)
        gpts, _ = fit_hat(pk, tid, iv2, dl2, 3.0, use_del=True, meter=True)
        gex, m_ex, d_ex, e_ex = fit_geom(pk, tid, iv, dl, exact=True)
        gfo, _, _, _ = fit_geom(pk, tid, iv, dl, exact=False)
        cyc, ncyc = cycles(pk, tid, inv, dls, sales, m_hat)
        r0f, r0w = r0_monthly(pk, tid, inv, dls, bls, sales)
        res["tanks"][tid] = {
            "R0_fails": int(r0f), "R0_worst_share": r0w,
            "R1": r1, "R1_per_delivery": r1b, "eps_deliveries": eps_d, "n_deliveries": int(len(dl[3])),
            "R2": list(r2), "R2_largest": largest(r2)[0],
            "R2p": [r2[0], r2[1], eps_d * Vfull], "R2p_largest": largest([r2[0], r2[1], eps_d * Vfull])[0],
            "gold": list(gold), "gold_largest": largest(gold)[0], "gold_pair": largest(gold)[1], "m_hat": m_hat,
            "v_hat6": list(g6), "v_dlvpts": list(gpts), "v_geom_exact": list(gex), "v_geom_first": list(gfo),
            "v_cycles": list(cyc), "n_cycles": ncyc, "geom_delta": d_ex, "geom_eps": e_ex, "geom_m": m_ex,
            "n_intervals": int(len(iv[0])),
        }
    T = res["tanks"]
    res["golden_list"] = sorted(t for t in T if T[t]["gold_largest"] > LIMIT)
    res["R0_list"] = sorted(t for t in T if T[t]["R0_fails"] > 0)
    res["R1_list"] = sorted(t for t in T if T[t]["R1"] > LIMIT)
    res["R1b_list"] = sorted(t for t in T if T[t]["R1_per_delivery"] > LIMIT)
    res["R2_list"] = sorted(t for t in T if T[t]["R2_largest"] > LIMIT)
    res["R2p_list"] = sorted(t for t in T if T[t]["R2p_largest"] > LIMIT)
    for v in ("v_hat6", "v_dlvpts", "v_geom_exact", "v_geom_first", "v_cycles"):
        res[v + "_list"] = sorted(t for t in T if np.nanmax(np.abs(T[t][v])) > LIMIT)
    res["A1"] = ask_days(pk)
    res["A2"] = ask_tests(pk)
    res["A3"] = {"%s|%s" % k: v for k, v in ask_gallons(pk).items()}
    res["stops"] = {
        "A1_drop_reset": ask_days(pk, redate=False), "A1_current_setup": ask_days(pk, by_current=True),
        "A2_every_row": ask_tests(pk, redate=False, dedupe=False), "A2_no_redate": ask_tests(pk, redate=False),
        "A2_utc_months": ask_tests(pk, utc_months=True),
        "A3_both": {"%s|%s" % k: v for k, v in ask_gallons(pk, shadow="both").items()},
        "A3_new_overlap": {"%s|%s" % k: v for k, v in ask_gallons(pk, shadow="new").items()},
        "A3_grade_table": {"%s|%s" % k: v for k, v in ask_gallons(pk, grade_basis="table").items()},
        "A3_stamp_dates": {"%s|%s" % k: v for k, v in ask_gallons(pk, settle=False).items()},
    }
    return res, pk


if __name__ == "__main__":
    tgt = sys.argv[1]
    res, pk = analyse(tgt)
    T = res["tanks"]
    print("%-5s %6s %6s %6s %6s %6s | %6s %6s %6s %6s %6s %6s  %s" % ("tank", "R1", "R1b", "R2", "R2p", "GOLD", "hat6", "dpts", "gexa", "gfo", "cyc", "m_hat", "pair"))
    for t, v in T.items():
        f = lambda key: float(np.nanmax(np.abs(v[key])))
        print("%-5s %6.1f %6.1f %6.1f %6.1f %6.1f | %6.1f %6.1f %6.1f %6.1f %6.1f %+.4f  %s %s" % (t, v["R1"], v["R1_per_delivery"], v["R2_largest"], v["R2p_largest"], v["gold_largest"], f("v_hat6"), f("v_dlvpts"), f("v_geom_exact"), f("v_geom_first"), f("v_cycles"), v["m_hat"], v["gold_pair"], v["n_cycles"]))
    for k in ("golden_list", "R0_list", "R1_list", "R1b_list", "R2_list", "R2p_list", "v_hat6_list", "v_dlvpts_list", "v_geom_exact_list", "v_geom_first_list", "v_cycles_list"):
        print(k, res[k])
    print("A1", res["A1"]); print("A2", res["A2"]); print("A3", {k: round(v) for k, v in res["A3"].items()})
