"""Every rung of the ladder, the golden call and the asks, computed from target/ alone (no world state).

    python3 analysis.py <target_dir>
"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np

TZ = ZoneInfo("America/Halifax")
UTC = ZoneInfo("UTC")
Q0 = dt.datetime(2026, 10, 1, 0, 0, tzinfo=TZ)
Q1 = dt.datetime(2027, 1, 1, 0, 0, tzinfo=TZ)
LINE = 99.0

FILES = {
    "standard": "PI-2_price_integrity_standard_rev3.pdf",
    "hourly": "pos_hourly_item_scans_2026Q4.csv",
    "movement": "price_change_item_movement_2026Q4.csv",
    "printer": "label_printer_fleet_jobs_2026-10-01_2026-12-31.jsonl",
    "checks": "thursday_changeover_checks_Q4-2026.xlsx",
    "audits": "price_audit_results_2026Q4.csv",
    "stores": "store_directory_2027-01.xlsx",
    "desk": "service_desk_adjustments_Q4_2026.xlsx",
    "overrides": "pos_price_overrides_2026Q4.csv",
    "adplan": "flyer_ad_plan_wk40-wk53_2026.csv",
    "pricefile": "weekly_price_change_releases_2026Q4.xlsx",
    "adsales": "flyer_item_daily_units_2026Q4.csv",
    "corrections": "price_corrections_2026Q4.csv",
}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def xlsx_rows(path, sheet=None, header_row=1):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        if sheet and ws.title != sheet:
            continue
        it = ws.iter_rows(values_only=True)
        hdr = None
        for k, row in enumerate(it, start=1):
            if hdr is None:
                if k == header_row or (row and row[0] in ("Store", "Store #", "Release")):
                    if row and row[0] in ("Store", "Store #", "Release"):
                        hdr = list(row)
                continue
            if row is None or all(v is None for v in row):
                continue
            out.append(dict(zip(hdr, row)) | {"_sheet": ws.title})
    return out


class Pack:
    def __init__(self, target):
        self.t = target
        p = lambda k: os.path.join(target, FILES[k])
        # directory: the three names a store goes by
        self.dir = xlsx_rows(p("stores"), "Stores")
        self.by_name = {d["Store"]: int(d["Store #"]) for d in self.dir}
        self.by_dev = {d["Label printer"]: int(d["Store #"]) for d in self.dir}
        self.stores = sorted(int(d["Store #"]) for d in self.dir)
        # POS hourly scans
        self.hourly = defaultdict(dict)
        for r in rows(p("hourly")):
            self.hourly[(int(r["store_no"]), dt.date.fromisoformat(r["business_date"]))][int(r["hour_start"][:2])] = \
                int(r["item_scans"])
        # changed items' Thursday units
        self.U = defaultdict(int)
        self.changed = defaultdict(set)
        self.co_dates = set()
        for r in rows(p("movement")):
            d = dt.date.fromisoformat(r["changeover_date"])
            s = int(r["store_no"])
            self.U[(s, d)] += int(r["units_changeover_thursday"])
            self.changed[(s, d)].add(r["upc"])
            self.co_dates.add(d)
        self.co_dates = sorted(self.co_dates)
        # printer fleet: the price change batch each store printed for each changeover
        self.batch = {}
        with open(p("printer"), encoding="utf-8") as f:
            jobs = [json.loads(x) for x in f if x.strip()]
        for j in jobs:
            m = re.match(r"PCB (\d{2}[A-Z]{3}\d{2})", j["job_name"])
            if not m or j["status"] != "COMPLETED":
                continue
            d = dt.datetime.strptime(m.group(1).title(), "%d%b%y").date()
            s = self.by_dev[j["device"]]
            t = dt.datetime.fromisoformat(j["printed_local"]).astimezone(TZ)
            self.batch[(s, d)] = (t, int(j["labels"]))
        self.jobs = jobs
        # Thursday changeover checks
        self.checks = []
        for r in xlsx_rows(p("checks")):
            if r.get("Store") in (None, "Store"):
                continue
            d = r["Visit date"]
            d = d.date() if isinstance(d, dt.datetime) else d
            hh, mm = str(r["Time checked"]).split(":")[:2]
            t = dt.datetime(d.year, d.month, d.day, int(hh), int(mm), tzinfo=TZ)
            self.checks.append((self.by_name[r["Store"]], t, str(r["EAN"]), float(r["Label price"]),
                                float(r["Register price"])))
        # weekly random audits
        self.audits = []
        for r in rows(p("audits")):
            t = dt.datetime.strptime(r["audit_started"], "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
            self.audits.append((self.by_name[r["store"]], t, r["ean"], float(r["shelf_price"]),
                                float(r["register_price"]), r["audit_id"]))

    def T(self, s):
        return sum(v for (st, d), hrs in self.hourly.items() if st == s for v in hrs.values())

    def week_of(self, d):
        """the changeover Thursday that opened the flyer week containing date d"""
        best = None
        for c in self.co_dates:
            if c <= d:
                best = c
        return best


# ----------------------------------------------------------------------------------------------- the pace
def fit_pace(pk, per_store=False):
    """labels a minute, from the Thursday checks taken after the store printed its batch: the share of checked
    labels still showing the old price falls from 1 at the print to 0 when the batch is up (MLE on a grid)."""
    obs = defaultdict(list)
    for (s, t, ean, lab, reg) in pk.checks:
        d = t.date()
        if (s, d) not in pk.batch:
            continue
        P_, L = pk.batch[(s, d)]
        m = (t - P_).total_seconds() / 60.0
        if m <= 0:
            continue
        stale = abs(lab - reg) > 0.004
        obs[s if per_store else 0].append((m, L, stale))
    out = {}
    grid = np.arange(1.0, 12.0, 0.01)
    for key, ob in obs.items():
        m = np.array([o[0] for o in ob])
        L = np.array([o[1] for o in ob])
        y = np.array([o[2] for o in ob])
        best, bl = None, -1e18
        for rr in grid:
            q = np.clip(1 - m * rr / L, 0, 1)
            q = np.clip(q, 1e-4, 1 - 1e-4)
            ll = np.sum(np.where(y, np.log(q), np.log(1 - q)))
            if ll > bl:
                bl, best = ll, rr
        out[key] = float(best)
    return out


def q_hour(hour, P_, L, rate, mode="ramp", within="uniform"):
    """share of a changed item's scans in clock hour `hour` that met the old label"""
    d = P_.date() if P_.hour >= 12 or True else P_.date()
    def q_at(tau):
        m = (tau - P_).total_seconds() / 60.0
        if m < 0:
            return 1.0
        if mode == "instant":
            return 0.0
        dur = L / rate
        if mode == "end":
            return 1.0 if m < dur else 0.0
        return max(0.0, 1.0 - m / dur)
    return q_at, None


def stale_scans(pk, rate, mode="ramp", within="uniform", profile="day", rate_by_store=None):
    out = defaultdict(float)
    detail = {}
    for s in pk.stores:
        for d in pk.co_dates:
            hrs = pk.hourly.get((s, d))
            if not hrs or (s, d) not in pk.batch:
                continue
            P_, L = pk.batch[(s, d)]
            rr = rate_by_store.get(s, rate) if rate_by_store else rate
            U = pk.U[(s, d)]
            hs = sorted(hrs)
            if profile == "day":
                w = np.array([hrs[h] for h in hs], float)
            elif profile == "uniform":
                w = np.ones(len(hs))
            else:   # the store's average Thursday profile over the quarter
                acc = defaultdict(float)
                for dd in pk.co_dates:
                    for h, v in pk.hourly.get((s, dd), {}).items():
                        acc[h] += v
                w = np.array([acc[h] for h in hs], float)
            w = w / w.sum()
            tot = 0.0
            for h, wh in zip(hs, w):
                base = dt.datetime(d.year, d.month, d.day, h, tzinfo=TZ)
                if within == "mid":
                    taus = [base + dt.timedelta(minutes=30)]
                else:
                    taus = [base + dt.timedelta(minutes=0.5 + k) for k in range(60)]
                vals = []
                for tau in taus:
                    m = (tau - P_).total_seconds() / 60.0
                    if m < 0:
                        vals.append(1.0)
                    elif mode == "instant":
                        vals.append(0.0)
                    elif mode == "end":
                        vals.append(1.0 if m < L / rr else 0.0)
                    else:
                        vals.append(max(0.0, 1.0 - m * rr / L))
                tot += wh * float(np.mean(vals))
            out[s] += U * tot
            detail[(s, d)] = U * tot
    return out, detail


def baseline(pk, rate, per_store=False):
    """stray-label share: audit labels that were not a changed item still waiting for its new label"""
    num = defaultdict(int)
    den = defaultdict(int)
    for (s, t, ean, lab, reg, aid) in pk.audits:
        d = pk.week_of(t.date())
        upc = ean[1:] if len(ean) == 13 else ean
        if d is not None and upc in pk.changed.get((s, d), ()) and (s, d) in pk.batch:
            P_, L = pk.batch[(s, d)]
            if (t - P_).total_seconds() / 60.0 < L / rate + 5:
                continue
        key = s if per_store else 0
        den[key] += 1
        num[key] += abs(lab - reg) > 0.004
    return {k: num[k] / den[k] for k in den}, num, den


def accuracy(pk, stale, b, per_store=False):
    out = {}
    for s in pk.stores:
        T = pk.T(s)
        bb = b[s] if per_store else b[0]
        out[s] = 100.0 * (1.0 - (stale.get(s, 0.0) + bb * (T - stale.get(s, 0.0))) / T)
    return out


def rungs(pk):
    R = {}
    # rung 0: the random price audit, labels matching over labels checked
    m = defaultdict(int)
    n = defaultdict(int)
    for (s, t, ean, lab, reg, aid) in pk.audits:
        n[s] += 1
        m[s] += abs(lab - reg) <= 0.004
    R["r0_audit"] = {s: 100.0 * m[s] / n[s] for s in pk.stores}
    # rung 0b: every label the integrity team checked, audits and Thursday checks pooled
    m2, n2 = dict(m), dict(n)
    for (s, t, ean, lab, reg) in pk.checks:
        n2[s] += 1
        m2[s] += abs(lab - reg) <= 0.004
    R["r0b_pooled"] = {s: 100.0 * m2[s] / n2[s] for s in pk.stores}
    rate = fit_pace(pk)[0]
    b, _, _ = baseline(pk, rate)
    # rung 1: the Thursday checks' stale share carried to the changed items' Thursday scans (time-uniform)
    cs = defaultdict(int)
    cn = defaultdict(int)
    for (s, t, ean, lab, reg) in pk.checks:
        cn[s] += 1
        cs[s] += abs(lab - reg) > 0.004
    st1 = {s: cs[s] / cn[s] * sum(pk.U[(s, d)] for d in pk.co_dates) for s in pk.stores}
    R["r1_checkshare"] = accuracy(pk, st1, b)
    # rung 2: a chain-wide stale curve by Thursday clock hour from every check, on each store's own hourly scans
    hs = defaultdict(int)
    hn = defaultdict(int)
    for (s, t, ean, lab, reg) in pk.checks:
        hn[t.hour] += 1
        hs[t.hour] += abs(lab - reg) > 0.004
    curve = {h: hs[h] / hn[h] for h in hn}
    st2 = defaultdict(float)
    for s in pk.stores:
        for d in pk.co_dates:
            hrs = pk.hourly.get((s, d))
            if not hrs:
                continue
            tot = sum(hrs.values())
            st2[s] += pk.U[(s, d)] * sum(v / tot * curve.get(h, curve[max(curve)] if h > max(curve) else 1.0)
                                         for h, v in hrs.items())
    R["r2_clockcurve"] = accuracy(pk, st2, b)
    # the golden: each changeover's old labels from the store's own batch print time and the hanging pace,
    # on the store's own scans that Thursday by hour
    stg, det = stale_scans(pk, rate)
    R["golden"] = accuracy(pk, stg, b)
    R["golden_stale"] = dict(stg)
    R["rate"] = rate
    R["baseline"] = b[0]
    R["detail"] = det
    return R


def variants(pk):
    rate = fit_pace(pk)[0]
    rates = fit_pace(pk, per_store=True)
    b, _, _ = baseline(pk, rate)
    bs, _, _ = baseline(pk, rate, per_store=True)
    V = {}
    for name, kw in [("ramp", {}), ("instant", {"mode": "instant"}), ("end", {"mode": "end"}),
                     ("mid", {"within": "mid"}), ("avgprofile", {"profile": "avg"}),
                     ("uniform_hours", {"profile": "uniform"}), ("store_pace", {"rate_by_store": rates})]:
        st, _ = stale_scans(pk, rate, **kw)
        V[name] = accuracy(pk, st, b)
    st, _ = stale_scans(pk, rate)
    V["store_baseline"] = accuracy(pk, st, bs, per_store=True)
    V["rate_lo"] = accuracy(pk, stale_scans(pk, rate * 0.85)[0], b)
    V["rate_hi"] = accuracy(pk, stale_scans(pk, rate * 1.15)[0], b)
    return V


# ----------------------------------------------------------------------------------------------- asks
def ask_payouts(target, by_name):
    """ask A: dollars each store paid out under the Scanner Price Accuracy Code in the quarter"""
    ov = rows(os.path.join(target, FILES["overrides"]))
    till = {}
    pay = defaultdict(float)
    for r in ov:
        if r["reason_code"] != "SC":
            continue
        t = dt.datetime.strptime(r["override_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(TZ)
        if not (Q0 <= t < Q1):
            continue
        s = int(r["store_no"])
        amt = (int(r["orig_price_cents"]) - int(r["override_price_cents"])) / 100.0
        pay[s] += amt
        till[(s, int(r["register"]), int(r["transaction"]), r["upc"])] = amt
    desk = xlsx_rows(os.path.join(target, FILES["desk"]))
    dup = 0
    for r in desk:
        if r.get("Reason") != "Scanner Code":
            continue
        t = r["Date / time"]
        if not (dt.datetime(2026, 10, 1) <= t < dt.datetime(2027, 1, 1)):
            continue
        s = by_name[r["Store"]]
        rec = str(r["Receipt #"])
        parts = re.split(r"[-/]", rec)
        if "/" in rec:
            txn, reg = int(parts[0]), int(parts[1])
        elif len(parts) == 3:
            reg, txn = int(parts[1]), int(parts[2])
        else:
            reg, txn = int(parts[0]), int(parts[1])
        upc = str(r["UPC"])[1:]
        amt = float(r["Refund $"])
        if (s, reg, txn, upc) in till and abs(till[(s, reg, txn, upc)] - amt) < 0.005:
            dup += 1          # the same payout, logged a second time by the approving supervisor
            continue
        pay[s] += amt
    return {s: round(v, 2) for s, v in pay.items()}, dup


def unit_price(qty, price):
    return price / qty


def ask_flyer(target, lead_only=False, release="REVISED", qty_aware=True, zone_units=True, corr="dated",
              match="family", unit_cents=False):
    """ask B: for each flyer week, the advertised UPCs that rang up at a price other than the flyer price, and the
    dollars customers paid above the flyer price that week. corr: 'dated' (a correction fixes the register from its
    effective date), 'none' (the release price all week), 'whole' (the correction taken for the whole week).
    match: how an assorted line's varieties are found ('family' by brand, product and size; 'price' by the lead's
    keyed price)."""
    ad = rows(os.path.join(target, FILES["adplan"]))
    rel = xlsx_rows(os.path.join(target, FILES["pricefile"]), release)
    keyed = {}
    adstart = defaultdict(list)
    for r in rel:
        d = r["Effective"]
        d = (d.date() if isinstance(d, dt.datetime) else d).isoformat()
        u11 = str(r["EAN"])[1:12]
        keyed[(d, u11, int(r["Zone"]))] = (int(r["Price qty"]), float(r["Price"]))
        if r["Change"] == "AD START" and int(r["Zone"]) == 1:
            adstart[d].append((u11, str(r["Description"])))
    fixes = defaultdict(list)
    for r in rows(os.path.join(target, FILES["corrections"])):
        fixes[(r["ean"][1:12], int(r["zone"].split()[1]))].append(
            (dt.date.fromisoformat(r["effective_at_open"]), int(r["price_qty"]), float(r["price"])))
    units = defaultdict(int)
    for r in rows(os.path.join(target, FILES["adsales"])):
        units[(r["flyer_start"], r["sales_date"], r["upc"][:11], int(r["price_zone"][1:]))] += int(r["units"])
    advertised = {}
    for r in ad:
        txt = r["ad_price"]
        m1 = re.match(r"^\$(\d+\.\d{2})$", txt)
        m2 = re.match(r"^(\d)/\$(\d+\.\d{2})$", txt)
        m3 = re.match(r"^(\d) for \$(\d+)$", txt)
        if m1:
            qty, pr = 1, float(m1.group(1))
        elif m2:
            qty, pr = int(m2.group(1)), float(m2.group(2))
        else:
            qty, pr = int(m3.group(1)), float(m3.group(2))
        d = r["flyer_start"]
        members = [r["upc_11"]]
        copy = r["ad_copy"]
        if copy.endswith(", assorted") and not lead_only:
            lead_desc = dict(adstart[d]).get(r["upc_11"], "").split()
            if match == "family" and len(lead_desc) == 4:
                members = [u for (u, desc) in adstart[d] if len(desc.split()) == 4 and
                           desc.split()[0] == lead_desc[0] and desc.split()[1] == lead_desc[1] and
                           desc.split()[3] == lead_desc[3]]
            elif match == "price":
                lead_k = keyed[(d, r["upc_11"], 1)]
                members = [u for (u, desc) in adstart[d] if keyed[(d, u, 1)] == lead_k and
                           desc.split()[0] == lead_desc[0]]
            if r["upc_11"] not in members:
                members.append(r["upc_11"])
        for u in members:
            advertised[(d, u)] = (qty, pr)
    cnt = defaultdict(int)
    over = defaultdict(float)
    for (d, u11), (q, p) in advertised.items():
        d0 = dt.date.fromisoformat(d)
        bad = False
        for z in (1, 2):
            kq0, kp0 = keyed[(d, u11, z)]
            fx = [f for f in fixes.get((u11, z), []) if d0 < f[0] <= d0 + dt.timedelta(days=6)]
            for j in range(7):
                day = d0 + dt.timedelta(days=j)
                kq, kp = kq0, kp0
                if fx and corr == "whole":
                    kq, kp = fx[-1][1], fx[-1][2]
                elif fx and corr == "dated" and day >= fx[-1][0]:
                    kq, kp = fx[-1][1], fx[-1][2]
                ku = kp / kq if qty_aware else kp
                au = p / q if qty_aware else p
                if unit_cents:      # a multi-buy's unit price taken to the cent, as the register rings one unit
                    ku, au = round(ku, 2), round(au, 2)
                if abs(ku - au) > 0.004:
                    bad = True
                    if ku > au + 0.004:
                        n_ = units[(d, day.isoformat(), u11, z)]
                        if not zone_units:
                            n_ = (units[(d, day.isoformat(), u11, 1)] + units[(d, day.isoformat(), u11, 2)]) / 2.0
                        over[d] += (ku - au) * n_
        cnt[d] += bad
    weeks = sorted({r["flyer_start"] for r in ad})
    return {d: cnt[d] for d in weeks}, {d: round(over[d], 2) for d in weeks}


def main(target):
    pk = Pack(target)
    R = rungs(pk)
    V = variants(pk)
    print("rate %.3f labels/min  baseline %.5f" % (R["rate"], R["baseline"]))
    names = ["r0_audit", "r0b_pooled", "r1_checkshare", "r2_clockcurve", "golden"]
    print("store " + " ".join("%13s" % n for n in names) + " | " + " ".join("%7s" % k[:7] for k in V))
    for s in pk.stores:
        print("%5d " % s + " ".join("%13.3f" % R[n][s] for n in names) + " | " +
              " ".join("%7.3f" % V[k][s] for k in V))
    for n in names:
        print(n, sorted(s for s in pk.stores if R[n][s] < LINE))
    for k in V:
        print("variant", k, sorted(s for s in pk.stores if V[k][s] < LINE))
    pays, dup = ask_payouts(target, pk.by_name)
    print("payouts", pays, "dups removed", dup)
    c, o = ask_flyer(target)
    print("flyer counts", c)
    print("flyer over", o)


if __name__ == "__main__":
    main(sys.argv[1])
