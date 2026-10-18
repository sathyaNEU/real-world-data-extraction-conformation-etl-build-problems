"""task161 independent verifier: reads only the shipped bundle (target/ and golden/), on its own code path
(pandas for the exports, pdftotext for the documents, its own projection and block test), and recomputes the
call, the default path, the per-account monthly fall, A1 and A2, then compares them with figures.json and the
golden workbook. It imports nothing from the generator.

    python3 verify.py [target] [golden]
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import warnings
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("America/Los_Angeles")
DAY = dt.timedelta(days=1)
OCEAN_TEU = {"22G1": 1.0, "42G1": 2.0, "45G1": 2.0, "L5G1": 2.25}
RACKS, BLOCK, LINE, SAT = 40000, 4000, 0.75, 0.40


def pdf(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                              text=True, check=True).stdout)


def local_date(stamp):
    return pd.to_datetime(stamp, utc=True).dt.tz_convert(TZ).dt.date


def months_between(a, b):
    out, (y, m) = [], a
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + (m == 12), m % 12 + 1)
    return out


def step_month(k, n):
    y, m = k
    t = y * 12 + (m - 1) + n
    return (t // 12, t % 12 + 1)


def mdays(k):
    a = dt.date(k[0], k[1], 1)
    b = dt.date(*step_month(k, 1), 1)
    return [a + DAY * i for i in range((b - a).days)]


class Pack:
    def __init__(self, target):
        self.t = target
        f = lambda n: os.path.join(target, n)
        cl = pd.read_excel(f("client_master_2026-12.xlsx"), sheet_name="Clients")
        cl["key"] = cl["Client ID"].fillna(cl["Legacy code(s)"].str.split(",").str[0].str.strip())
        self.clients = cl
        legacy = {}
        for _, r in cl.iterrows():
            for code in str(r["Legacy code(s)"]).split(","):
                if code.strip() and code.strip() != "nan":
                    legacy[code.strip()] = r["key"]
        lg = pd.read_csv(f("wms1_inv_daily_20190401-20220930.txt"), sep="|")
        lg["d"] = pd.to_datetime(lg["BUS_DT"], format="%m/%d/%Y").dt.date
        lg["k"] = lg["CLIENT"].map(legacy)
        assert lg["k"].notna().all()
        lg = lg[lg["d"] < dt.date(2022, 9, 12)].groupby(["k", "d"])[["CLOSE_PLT", "SHIP_PLT"]].sum().reset_index()
        nt = pd.read_csv(f("wms_inventory_nightly_20220913_20261207.csv"))
        nt["d"] = [x - DAY for x in local_date(nt["snapshot_utc"])]
        self.nightly = nt
        nb = nt.groupby(["client_id", "d"])["on_hand_pallets"].sum().reset_index()
        ob = pd.read_csv(f("wms_outbound_daily_20220912_20261206.csv"))
        ob["d"] = pd.to_datetime(ob["ship_date"]).dt.date
        self.last = max(nb["d"])
        self.first = min(lg["d"])
        self.days = [self.first + DAY * i for i in range((self.last - self.first).days + 1)]
        self.ix = {d: i for i, d in enumerate(self.days)}
        n = len(self.days)
        self.oh, self.sh = {}, {}
        for _, c in cl.iterrows():
            k = c["key"]
            start = c["Contract start"].date()
            end = c["Contract end"].date() if not pd.isna(c["Contract end"]) else None
            o = np.full(n, np.nan)
            s = np.zeros(n)
            a = lg[lg["k"] == k]
            for d, v, sv in zip(a["d"], a["CLOSE_PLT"], a["SHIP_PLT"]):
                o[self.ix[d]] = v
                s[self.ix[d]] += sv
            b = nb[nb["client_id"] == k]
            for d, v in zip(b["d"], b["on_hand_pallets"]):
                o[self.ix[d]] = v
            q = ob[ob["client_id"] == k]
            for d, v in zip(q["d"], q["pallets_shipped"]):
                s[self.ix[d]] += v
            for i, d in enumerate(self.days):
                if d < start or (end is not None and d > end):
                    o[i] = 0.0
            o = pd.Series(o).ffill().fillna(0.0).to_numpy()      # Sundays carry Saturday's close
            self.oh[k], self.sh[k] = o, s
        self.current = [r["key"] for _, r in cl.iterrows() if pd.isna(r["Contract end"])]
        adv = pdf(f("yv_client_advisories_2019-2026.pdf"))
        self.adv_dates = sorted({dt.datetime.strptime(x, "%d %B %Y").date()
                                 for x in re.findall(r"(\d{1,2} [A-Z][a-z]+ \d{4}) \|", adv)})
        steps = sorted({dt.datetime.strptime(x, "%d %B %Y").date() for x in
                        re.findall(r"on or after (?:12:01 a\.m\. E[DS]T on )?(\d{1,2} [A-Z][a-z]+ \d{4})", adv)})
        self.steps = [x for x in steps if x <= self.last]
        self.future = [x for x in steps if x > self.last]
        self.full = [k for k in months_between((self.first.year, self.first.month), (self.last.year, self.last.month))
                     if mdays(k)[-1] <= self.last]
        rc = pd.read_csv(f("wms_inbound_receipts_20220912_20261206.csv"))
        rc["ts"] = pd.to_datetime(rc["received_at_utc"], utc=True)
        rc["d"] = local_date(rc["received_at_utc"])
        self.rc = rc.sort_values("ts", kind="mergesort")
        mf = pd.read_excel(f("avila_delivery_manifest_2024-03_2026-12.xlsx"), sheet_name="Deliveries", header=3)
        self.mf = mf
        self.notices = self._notices()

    def _ppb(self, days=90):
        lo = self.last - DAY * (days - 1)
        r = self.rc[(self.rc["d"] >= lo) & (self.rc["d"] <= self.last)]
        src = self.mf.groupby("Trailer")["Pallets"].apply(list).to_dict()
        pal, box, seen = {}, {}, {}
        for c, typ, eq, p, d in zip(r["client_id"], r["equipment_type"], r["equipment_id"], r["pallets"], r["d"]):
            if typ in OCEAN_TEU:
                pal[c] = pal.get(c, 0) + p
                if eq in seen and (d - seen[eq]).days <= 3:
                    seen[eq] = d
                    continue
                seen[eq] = d
                box[c] = box.get(c, 0) + 1
            elif eq in src:
                pal[c] = pal.get(c, 0) + sum(src[eq])
                box[c] = box.get(c, 0) + len(src[eq])
        return {c: pal[c] / box[c] for c in box}

    def _notices(self):
        tk = pd.read_excel(os.path.join(self.t, "dec2026_inbound_booking_tracker.xlsx"), sheet_name="Dec arrivals",
                           header=4)
        ppb = self._ppb()
        out = {}
        for _, r in tk.iterrows():
            due = r["Due at DC"].date()
            if due <= self.last:
                continue
            boxes = sum(0 if pd.isna(r[h]) else int(r[h]) for h in ("20'", "40'", "40' HC", "45'"))
            p = r["Pallets (customer notice)"]
            p = float(p) if not pd.isna(p) else boxes * ppb[r["Client ID"]]
            out[r["Client ID"]] = out.get(r["Client ID"], 0.0) + p
        return out

    # --------------------------------------------------------------------------- monthly views and normal stock
    def monthly(self, keys):
        P, S = {}, {}
        for k in self.full:
            ii = [self.ix[d] for d in mdays(k)]
            P[k] = float(sum(self.oh[c][ii].mean() for c in keys))
            S[k] = float(sum(self.sh[c][ii].sum() for c in keys))
        return P, S

    def blocked(self):
        out = set()
        for st in self.steps + [dt.date(2027, 1, 1)]:
            for j in range(-3, 6):
                out.add(step_month((st.year, st.month), j))
        return out

    def cover(self, P, S, since=(2023, 7)):
        bad = self.blocked()
        v = [P[k] / (0.5 * (S[k] + S[step_month(k, 1)])) for k in self.full
             if k not in bad and k >= since and step_month(k, 1) in S and S[k] > 0]
        return float(np.median(v)) if len(v) >= 6 else None

    @staticmethod
    def normal_fn(cover, S):
        ks = sorted(S)
        pts = [(dt.date(k[0], k[1], 15), cover * 0.5 * (S[k] + S[step_month(k, 1)])) for k in ks
               if step_month(k, 1) in S and S[k] is not None and S[step_month(k, 1)] is not None]
        base = pts[0][0]
        x = np.array([(a - base).days for a, _ in pts], float)
        y = np.array([b for _, b in pts])
        return lambda d: float(np.interp((d - base).days, x, y))

    def grow(self, S):
        last = months_between((2025, 12), (2026, 11))
        return sum(S[k] for k in last) / sum(S[(k[0] - 1, k[1])] for k in last)

    def fc(self, S):
        g = self.grow(S)
        return {k: S[(k[0] - 1, k[1])] * g for k in [(2026, 12)] + [(2027, m) for m in range(1, 8)]}


def episodes(pk, o, s, nf):
    out = []
    for st in pk.steps:
        i0 = pk.ix[st]
        later = [d for d in pk.adv_dates if d > st]
        stop = pk.ix.get(min(later)) if later else None
        pre = [pk.days[i] for i in range(i0 - 7, i0)]
        n0 = np.mean([nf(d) for d in pre])
        e0 = np.mean([o[pk.ix[d]] - nf(d) for d in pre])
        if e0 < 0.12 * n0:
            continue
        xs, ys, cum = [], [], 0.0
        for i in range(i0, min(len(pk.days), i0 + 240, stop if stop is not None else 10 ** 9)):
            cum += s[i]
            e = o[i] - nf(pk.days[i])
            if e <= 0.25 * e0:
                break
            xs.append(cum)
            ys.append(e0 - e)
        if len(xs) >= 15:
            out.append((float(np.polyfit(xs, ys, 1)[0]), xs[-1], len(xs)))
    return out


def weights(days, hol):
    return np.array([0.0 if d.weekday() == 6 or d in hol else (SAT if d.weekday() == 5 else 1.0) for d in days])


def block_test(total):
    O = np.maximum(np.asarray(total) - RACKS, 0)
    U = [float(np.clip(O - BLOCK * k, 0, BLOCK).sum() / (BLOCK * len(O))) for k in range(6)]
    n = 0
    while n < 6 and U[n] >= LINE:
        n += 1
    return n, U, O


def close31(pk, k, fc, nf):
    dec = mdays((2026, 12))
    hol = {dt.date(2026, 12, 24), dt.date(2026, 12, 25)}
    w = weights(dec, hol)
    rest = sum(wi for d, wi in zip(dec, w) if d > pk.last)
    oh31 = pk.oh[k][pk.ix[pk.last]] + pk.notices.get(k, 0.0) - fc[(2026, 12)] * rest / w.sum()
    return oh31, max(0.0, oh31 - nf(dt.date(2026, 12, 31)))


def window_days(fc):
    hol = {dt.date(2027, 1, 1), dt.date(2027, 5, 31)}
    out = []
    for m in range(1, 7):
        ds = mdays((2027, m))
        w = weights(ds, hol)
        out.append((ds, fc[(2027, m)] * w / w.sum()))
    return out


def the_call(pk):
    per = {}
    pooled = []
    for k in pk.current:
        P, S = pk.monthly([k])
        cv = pk.cover(P, S)
        eps = episodes(pk, pk.oh[k], pk.sh[k], pk.normal_fn(cv, S))
        per[k] = (P, S, cv, eps)
        pooled += [e[0] for e in eps]
    total = np.zeros(6)
    info = {}
    for k in pk.current:
        P, S, cv, eps = per[k]
        if eps:
            s = sum(e[0] * e[1] for e in eps) / sum(e[1] for e in eps)
        else:
            s = float(np.median(pooled))
        fc = pk.fc(S)
        nf = pk.normal_fn(cv, {**S, **fc})
        oh31, e = close31(pk, k, fc, nf)
        info[k] = {"s": s, "e31": e, "eps": eps, "fc": fc, "cv": cv}
        for m, (ds, daily) in enumerate(window_days(fc)):
            vals = []
            for d, x in zip(ds, daily):
                e = max(0.0, e - s * x)
                vals.append(nf(d) + e)
            total[m] += np.mean(vals)
        info[k]["e30jun"] = e
    return block_test(total), total, info


def the_fade(pk):
    """The default path: the book's excess over its normal stock faded at the earlier rushes' half-life."""
    keys = list(pk.oh)
    P, S = pk.monthly(keys)
    bad = pk.blocked()
    v = [P[k] / (0.5 * (S[k] + S[step_month(k, 1)])) for k in pk.full if k not in bad and step_month(k, 1) in S]
    nf = pk.normal_fn(float(np.median(v)), S)
    oh = sum(pk.oh[c] for c in keys)
    sh = sum(pk.sh[c] for c in keys)
    hls = []
    for st in pk.steps:
        i0 = pk.ix[st]
        later = [d for d in pk.adv_dates if d > st]
        stop = pk.ix.get(min(later)) if later else len(pk.days)
        es = []
        for i in range(i0, min(stop, i0 + 240)):
            e = oh[i] - nf(pk.days[i])
            es.append(e)
            if e <= 0.05 * nf(pk.days[i]):
                break
        es = np.array(es)
        t = np.arange(len(es)) / 30.4
        ok = es > 0.05 * max(es[0], 1)
        if ok.sum() >= 15:
            b = np.polyfit(t[ok], np.log(es[ok]), 1)[0]
            hls.append(np.log(0.5) / b if b < 0 else np.inf)
    hl = float(np.median(hls))
    Pc, Sc = pk.monthly(pk.current)
    cv = pk.cover(Pc, Sc)
    fc = pk.fc(Sc)
    nfc = pk.normal_fn(cv, {**Sc, **fc})
    dec = mdays((2026, 12))
    w = weights(dec, {dt.date(2026, 12, 24), dt.date(2026, 12, 25)})
    rest = sum(wi for d, wi in zip(dec, w) if d > pk.last) / w.sum()
    oh31 = sum(pk.oh[c][pk.ix[pk.last]] for c in pk.current) + sum(pk.notices.get(c, 0.0) for c in pk.current) - \
        fc[(2026, 12)] * rest
    E = max(0.0, oh31 - nfc(dt.date(2026, 12, 31)))
    lam = 0.5 ** (1.0 / hl)
    total, j = [], 0
    for m in range(1, 7):
        vals = []
        for d in mdays((2027, m)):
            j += 1
            vals.append(nfc(d) + E * lam ** (j / 30.4))
        total.append(np.mean(vals))
    return block_test(total), hl


def monthly_fall(pk, info):
    total = np.zeros(6)
    for k in pk.current:
        x = info[k]
        rate = float(np.median([e[0] * e[1] / max(1, e[2]) * 30.4 for e in x["eps"]])) if x["eps"] else 0.0
        P, S = pk.monthly([k])
        nf = pk.normal_fn(x["cv"], {**S, **x["fc"]})
        j = 0
        for m in range(6):
            vals = []
            for d in mdays((2027, m + 1)):
                j += 1
                vals.append(nf(d) + max(0.0, x["e31"] - rate * j / 30.4))
            total[m] += np.mean(vals)
    return block_test(total)


def backtest(pk, info, horizon=90):
    """Each earlier rush left out in turn: each account's excess path after the step predicted from its other rushes
    by the burn share (shipment-weighted) and by a half-life (median of the others' log-linear fits)."""
    tot = {"burn": 0.0, "fade": 0.0}
    per = {}
    for k in pk.current:
        x = info[k]
        P, S = pk.monthly([k])
        nf = pk.normal_fn(x["cv"], S)
        o, sh = pk.oh[k], pk.sh[k]
        paths, fits = {}, {}
        for st in pk.steps:
            i0 = pk.ix[st]
            pre = [pk.days[i] for i in range(i0 - 7, i0)]
            n0 = np.mean([nf(d) for d in pre])
            e0 = np.mean([o[pk.ix[d]] - nf(d) for d in pre])
            if e0 < 0.12 * n0:
                continue
            later = [d for d in pk.adv_dates if d > st]
            stop = pk.ix.get(min(later)) if later else 10 ** 9
            fx, fy, cum = [], [], 0.0
            for i in range(i0, min(len(pk.days), i0 + 240, stop)):
                cum += sh[i]
                e = o[i] - nf(pk.days[i])
                if e <= 0.25 * e0:
                    break
                fx.append(cum)
                fy.append(e0 - e)
            if len(fx) < 15:
                continue
            es, cs, ts, cum = [], [], [], 0.0
            for i in range(i0, min(i0 + horizon, stop, len(pk.days))):
                cum += sh[i]
                es.append(o[i] - nf(pk.days[i]))
                cs.append(cum)
                ts.append(i - i0 + 1)
            paths[st] = (e0, np.array(es), np.array(cs), np.array(ts))
            fits[st] = (float(np.polyfit(fx, fy, 1)[0]), fx[-1])
        for st in paths:
            others = [q for q in paths if q != st]
            if not others:
                continue
            s_ = sum(fits[q][0] * fits[q][1] for q in others) / sum(fits[q][1] for q in others)
            hls = []
            for q in others:
                e0q, eq, _, tq = paths[q]
                okq = eq > 0.05 * e0q
                if okq.sum() >= 10:
                    b = np.polyfit(tq[okq] / 30.4, np.log(eq[okq]), 1)[0]
                    hls.append(np.log(0.5) / b if b < 0 else 50.0)
            e0, es, cs, ts = paths[st]
            act = np.maximum(es, 0.0)
            pb = np.maximum(0.0, e0 - s_ * cs)
            pf = e0 * 0.5 ** (ts / 30.4 / float(np.median(hls))) if hls else e0 + 0 * ts
            for name, pr in (("burn", pb), ("fade", pf)):
                err = float(np.abs(pr - act).mean())
                tot[name] += err
                per[(st, name)] = per.get((st, name), 0.0) + err
    return tot, per


def ask2(pk):
    seen, teu = {}, {}
    for eq, typ, d in zip(pk.rc["equipment_id"], pk.rc["equipment_type"], pk.rc["d"]):
        if typ not in OCEAN_TEU:
            continue
        if eq in seen and (d - seen[eq]).days <= 3:
            seen[eq] = d
            continue
        seen[eq] = d
        teu[(d.year, d.month)] = teu.get((d.year, d.month), 0.0) + OCEAN_TEU[typ]
    src = pk.mf.groupby("Trailer")["ISO Type"].apply(list).to_dict()
    for eq, typ, d in zip(pk.rc["equipment_id"], pk.rc["equipment_type"], pk.rc["d"]):
        if typ == "53DV" and eq in src:
            teu[(d.year, d.month)] = teu.get((d.year, d.month), 0.0) + sum(OCEAN_TEU[x] for x in src[eq])
    la = pd.read_csv(os.path.join(pk.t, "pola_container_stats_2026.csv"))
    lb = pd.read_csv(os.path.join(pk.t, "polb_teu_stats_2026.csv"))
    names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
    out = {}
    for i, nm in enumerate(names):
        a = int(la.loc[la["Month"] == "%s 2026" % nm, "Loaded Imports"].iloc[0])
        b = int(lb.loc[(lb["Year"] == 2026) & (lb["Month"] == nm[:3].upper()), "Inbound Loaded"].iloc[0])
        t = teu[(2026, i + 1)]
        out["%s 2026" % nm] = (t, 100.0 * t / (a + b))
    return out


def main(target, golden):
    fails = []

    def ok(label, cond, note):
        print("  %s  %-4s %s" % ("PASS" if cond else "FAIL", label, note))
        if not cond:
            fails.append(label)

    F = json.load(open(os.path.join(HERE, "figures.json")))
    pol = pdf(os.path.join(target, "space_planning_policy_rev4.pdf"))
    off = pdf(os.path.join(target, "ridley-ames_bldg-b_overflow_blocks_2026-11-19.pdf"))
    dic = pdf(os.path.join(target, "wms_export_dictionary_v3.pdf"))
    ok("V0", "40,000 rack positions" in pol and "at least three quarters of its position-months" in pol and
       "mean of each day's closing stock in the month" in pol and "$1,100,000 per block for the term" in off and
       "Blocks are let whole and for the whole term" in off and "close of the business day just ended" in dic,
       "pdftotext reads the policy's sections 3 and 4, the offer and the dictionary's run line (positive control)")
    pk = Pack(target)
    ok("V1", pk.steps == [dt.date(2019, 9, 1), dt.date(2025, 4, 5), dt.date(2025, 8, 7)] and
       pk.future == [dt.date(2027, 1, 1)] and pk.last == dt.date(2026, 12, 6),
       "the advisories' steps %s, the step ahead %s, the last close %s" % (pk.steps, pk.future, pk.last))
    (n, U, O), total, info = the_call(pk)
    ok("V2", n == F["call"]["blocks"] == 2 and [round(100 * u, 1) for u in U] == F["components"]["block_use_pct"],
       "the call recomputed: %d blocks, block uses %s per cent" % (n, [round(100 * u, 1) for u in U]))
    mon = ["January", "February", "March", "April", "May", "June"]
    ok("V3", {"%s 2027" % m: int(round(x)) for m, x in zip(mon, O)} == F["components"]["overflow"],
       "monthly overflow above the 40,000 rack positions %s" % [int(round(x)) for x in O])
    seas = ["PD2047", "PD2052", "PD2058", "PD2102", "PD2108"]
    e31 = sum(round(info[k]["e31"]) for k in pk.current)
    ok("V4", e31 == F["components"]["excess_31dec"] and sum(round(info[k]["e31"]) for k in seas) ==
       F["components"]["seasonal_excess_31dec"] and sum(round(info[k]["e30jun"]) for k in pk.current) ==
       F["components"]["excess_30jun"] and int(sum(pk.oh[k][pk.ix[pk.last]] for k in pk.current)) ==
       F["components"]["on_hand_6dec"],
       "on hand at the close of 6 December %d; excess at 31 December %d (the five seasonal accounts %d); left at 30 "
       "June %d" % (sum(pk.oh[k][pk.ix[pk.last]] for k in pk.current), e31,
                    sum(round(info[k]["e31"]) for k in seas), sum(round(info[k]["e30jun"]) for k in pk.current)))
    (nf_, Uf, _), hl = the_fade(pk)
    ok("V5", nf_ == 0 and round(hl, 2) == F["rivals"]["fade_half_life_months"],
       "the default path: half-life %.2f months, %d blocks (block 1 used %.0f per cent)" % (hl, nf_, 100 * Uf[0]))
    nm_, Um, _ = monthly_fall(pk, info)
    ok("V6", nm_ == 1 == F["rivals"]["per_account_fall_blocks"], "each account's own monthly fall: %d block" % nm_)
    jan = [pk.ix[d] for d in mdays((2026, 1))]
    five = int(sum(pk.sh[k][jan].sum() for k in seas))
    ok("V7", five == F["components"]["five_jan2026_shipments"] and five < 0.5 * sum(info[k]["e31"] for k in seas),
       "the five seasonal accounts shipped %d pallets in January 2026, under half of their excess at 31 December" % five)
    tot = sum(pk.oh[k] for k in pk.current)
    nov = [pk.ix[d] for d in mdays((2026, 11))]
    dec = [pk.ix[d] for d in mdays((2026, 12)) if d in pk.ix]
    flat = {name: block_test([float(v)] * 6)[0] for name, v in
            (("close", tot[pk.ix[pk.last]]), ("november", tot[nov].mean()), ("december", tot[dec].mean()))}
    ok("V12", all(v >= 3 for v in flat.values()), "today's stock held flat files a block more: %s" % flat)
    bt, per = backtest(pk, info)
    rushes = sorted({x[0] for x in per})
    ahead = sum(1 for st in rushes if per[(st, "burn")] < per[(st, "fade")])
    ok("V13", bt["burn"] <= 0.70 * bt["fade"] and ahead >= 2,
       "leave-one-out on the earlier rushes: burn %.0f against fade %.0f; the burn ahead on %d of %d (%s)" %
       (bt["burn"], bt["fade"], ahead, len(rushes),
        ", ".join("%s %.0f/%.0f" % (st, per[(st, "burn")], per[(st, "fade")]) for st in rushes)))
    a2 = ask2(pk)
    ok("V8", all(int(round(a2[k][0])) == F["a2_teu"][k] and "%.3f" % a2[k][1] == F["a2_share"][k] for k in a2),
       "A2 recomputed: %s" % {k: (int(round(v[0])), "%.3f" % v[1]) for k, v in a2.items()})
    edge = min(min(0.5 - abs(t - round(t)), (0.0005 - abs(s - round(s, 3))) * 1000) for t, s in a2.values())
    ok("V9", edge >= 0.25, "every A2 figure a quarter cell or more from its rounding edge (%.2f of a cell)" % edge)
    gw = pd.read_excel(os.path.join(golden, "overflow_blocks_h1_2027.xlsx"), sheet_name=None, header=None)
    ok("V10", "take 2 of the 6 blocks" in str(gw["Blocks"].iloc[3, 0]) and "Off-rack 6 Dec" not in gw,
       "the golden workbook carries the call")
    ch = pdf(os.path.join(golden, "port_share_2026.pdf"))
    ok("V11", all("{:,} TEU".format(F["a2_teu"][k]) in ch for k in a2) and all(F["a2_share"][k] + "%" in ch for k in a2),
       "the chart labels every bar with its TEU and share")
    print("verify: %d failed" % len(fails))
    if fails:
        raise SystemExit("verify failed: " + ", ".join(fails))


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden"))
