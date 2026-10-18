"""The records the two decoupled asks read, and their goldens: the 2025-26 pilot's work orders, the GIS unit change log
(every change, pilot and otherwise) with the unit serials, the pilot's cost lines, and the outage management system's
transformer outage lines for the 2026 summer.

Ask A (the pilot close-out, Railyard, Canal and Brookside): transformers replaced, nameplate kVA added, cost per
transformer replaced. Ask B (every district): the customer-hours of the outages caused by transformers failing in
service from 1 June to 30 September 2026, and the customers those outages kept off for more than eight hours."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K
import world as W

PDT = pd.Timedelta(hours=7)                 # Pacific daylight time is UTC less seven hours all summer
WIN_LO, WIN_HI = pd.Timestamp("2026-06-01"), pd.Timestamp("2026-10-01")


# ------------------------------------------------------------------------------------------------- serials
def serial(r, year):
    return "%s%02d-%06d" % ("HKEPG"[int(r.integers(5))], year % 100, int(r.integers(0, 10 ** 6)))


def unit_changes(T):
    """Every unit change from 1 January 2024 to the pull, one row each, in date order, with the serial chain."""
    r = K.rng("serials")
    tx = T.tx
    rows = []
    for x in T.pilot.itertuples():
        rows.append((x.ti, pd.Timestamp(x.date), x.kva_old, x.kva_new, "PTR", x.wo_ti, bool(x.second), True))
    for x in T.corr.itertuples():
        rows.append((x.ti, pd.Timestamp(x.date), x.kva_from, x.kva_to, "PTR", x.wo_ti, False, False))
    for x in T.fail.itertuples():
        d = T.fail_restored[int(x.ti)]
        rows.append((x.ti, d.normalize(), x.kva_old, x.kva_new, "FAIL", -1, False, True))
    for x in T.other.itertuples():
        rows.append((x.ti, pd.Timestamp(x.date), x.kva_from, x.kva_to, x.kind, -1, False, x.kind in ("MAINT", "LOAD")))
    C = pd.DataFrame(rows, columns=["ti", "date", "kva_from", "kva_to", "reason", "wo_ti", "second", "new_unit"])
    C = C.sort_values(["date", "ti", "reason"]).reset_index(drop=True)
    # the serial chain: the unit in service on 1 January 2024, then each new unit
    first_year = r.integers(1972, 2024, len(tx))
    cur = {int(t): serial(r, int(y)) for t, y in zip(tx["ti"], first_year)}
    T.unit_year0 = dict(zip(tx["ti"].astype(int), first_year.astype(int)))
    rem, ins = [], []
    for x in C.itertuples():
        a = cur[x.ti]
        b = serial(r, x.date.year) if x.new_unit else a
        rem.append(a)
        ins.append(b)
        cur[x.ti] = b
    C["removed_serial"], C["installed_serial"] = rem, ins
    T.serial_now = cur
    return C


# ------------------------------------------------------------------------------------------------- work orders
CREWS = {"Railyard": ["RY-L1", "RY-L2", "RY-L4", "CC-07"], "Canal": ["CN-L1", "CN-L3", "CC-07", "CC-11"],
         "Brookside": ["BK-L2", "BK-L3", "CC-11"]}
NOWORK_NOTES = ["Unit on pole is %s kVA per nameplate, no change made. Map correction sent.",
                "Existing %s kVA matches load, closed no work. GIS to update size.",
                "Already a %s, GIS showed smaller. No changeout.", "", ""]
CANC_NOTES = ["Customer would not allow access to rear easement.", "Pole in joint replacement job, transformer to go with it.",
              "Cancelled, backyard pad blocked by new pool construction.", "Duplicate of another order on this location.",
              "Easement dispute, referred to land dept."]
SECOND_NOTES = ["Also changed out %s on same feeder.", "2nd unit %s done same outage.", "", "", "Did %s while there."]
SUB_NOTES = ["No %s in stock, set %s.", "Set %s per stores (%s back ordered).", ""]


def work_orders(T, C):
    """The pilot's work orders, numbered in the order they were raised (across the three districts), with the
    crews' closing remarks."""
    r = K.rng("work-orders")
    wos = T.wos.sort_values(["date", "ti"]).reset_index(drop=True)
    num = 41702300 + np.cumsum(r.integers(1, 38, len(wos)))
    wos["wo_number"] = num
    by_ti = dict(zip(wos["ti"], wos["wo_number"]))
    loc = dict(zip(T.tx["ti"], T.tx["loc"]))
    rem = []
    inst = {(x.ti): x.kva_new for x in T.pilot.itertuples()}
    for x in wos.itertuples():
        note = ""
        if x.kind == "NOWORK":
            note = NOWORK_NOTES[int(r.integers(len(NOWORK_NOTES)))]
            if "%s" in note:
                note = note % fmt_kva(float(T.tx.loc[x.ti, "kva"]))
        elif x.kind == "CANC":
            note = CANC_NOTES[int(r.integers(len(CANC_NOTES)))]
        else:
            parts = []
            if x.second_ti >= 0:
                s = SECOND_NOTES[int(r.integers(len(SECOND_NOTES)))]
                if s:
                    parts.append(s % ("T%d" % loc[x.second_ti]))
            if inst[x.ti] != x.plan_to:
                s = SUB_NOTES[int(r.integers(len(SUB_NOTES)))]
                if s:
                    parts.append(s % (fmt_kva(x.plan_to), fmt_kva(inst[x.ti])) if s.startswith("No") else
                                 s % (fmt_kva(inst[x.ti]), fmt_kva(x.plan_to)))
            note = " ".join(parts)
        rem.append(note)
    wos["remarks"] = rem
    wos["status"] = np.where(wos["kind"] == "CANC", "CANC", "COMP")
    wos["crew"] = [str(r.choice(CREWS[d])) for d in wos["district"]]
    # cancelled orders are closed some days after they were raised
    wos["status_date"] = [d + dt.timedelta(days=int(r.integers(2, 20))) if k == "CANC" else d
                          for d, k in zip(wos["date"], wos["kind"])]
    T.wo_of_ti = by_ti
    C["wo_number"] = [("" if (w < 0 or s) else str(by_ti[w])) if rs == "PTR" else "" for w, s, rs in
                      zip(C["wo_ti"], C["second"], C["reason"])]
    return wos


def fmt_kva(k):
    return ("%g" % k)


def other_order_numbers(T, C):
    r = K.rng("other-orders")
    nums = []
    for x in C.itertuples():
        if x.reason == "FAIL":
            nums.append("%d" % (46100000 + int(r.integers(0, 899999))))
        elif x.reason in ("MAINT", "LOAD"):
            nums.append("%d" % (43200000 + int(r.integers(0, 899999))))
        else:
            nums.append(x.wo_number)
    C["wo_number"] = nums
    lag = r.integers(1, 22, len(C))
    lag = np.where(C["second"].values, r.integers(12, 48, len(C)), lag)
    lag = np.where(C["reason"].values == "FAIL", r.integers(1, 12, len(C)), lag)
    C["posted"] = C["date"] + pd.to_timedelta(lag, unit="D")
    C.loc[C["posted"] > pd.Timestamp(K.AS_OF), "posted"] = pd.Timestamp(K.AS_OF) - pd.Timedelta(days=1)
    return C


# ------------------------------------------------------------------------------------------------- costs
MAT = {10.0: 1488.0, 15.0: 1726.0, 25.0: 2143.0, 37.5: 2689.0, 50.0: 3352.0, 75.0: 4612.0, 100.0: 5874.0}


def cost_lines(T, wos):
    """Every line charged to the pilot's internal order, as the general ledger holds it: crew labor, contract crew
    accruals reversed when the invoice posts, the transformer and its fittings, fleet, and a few lines posted to the
    wrong order and moved."""
    r = K.rng("costs")
    tx = T.tx
    rows = []
    inst = {}
    for x in T.pilot.itertuples():
        inst.setdefault(int(x.wo_ti), []).append((float(x.kva_new), x.ti))
    mount = dict(zip(tx["ti"], tx["mount"]))
    doc = [5100023000]

    def post(wo, elem, d, amt, ref=None):
        doc[0] += int(r.integers(1, 9))
        rows.append((wo, elem, d, round(float(amt), 2), ref or "%d" % doc[0]))

    for x in wos.itertuples():
        d = pd.Timestamp(x.status_date)
        if x.kind == "REPL":
            units = inst[x.ti]
            hours = r.uniform(4.5, 7.5) + 3.2 * (len(units) - 1)
            contract = x.crew.startswith("CC")
            labor = hours * (4 if not contract else 1) * (r.uniform(118, 134) if not contract else r.uniform(560, 640))
            if contract:
                acc_d = (d + pd.offsets.MonthEnd(0))
                post(x.wo_number, "CONTRACT-ACCR", acc_d, labor)
                post(x.wo_number, "CONTRACT-ACCR", acc_d + pd.Timedelta(days=1), -labor)
                post(x.wo_number, "CONTRACT", d + pd.Timedelta(days=int(r.integers(24, 61))), labor * r.uniform(0.97, 1.04))
            else:
                post(x.wo_number, "LABOR", d + pd.Timedelta(days=int(r.integers(0, 4))), labor)
            for k, t in units:
                m = MAT[k] * (1.56 if mount[t] == "PAD" else 1.0) * r.uniform(0.985, 1.02)
                post(x.wo_number, "MATL-XFMR", d - pd.Timedelta(days=int(r.integers(1, 9))), m)
            post(x.wo_number, "MATL-OTHER", d - pd.Timedelta(days=int(r.integers(0, 9))), r.uniform(160, 430) * len(units))
            post(x.wo_number, "FLEET", d + pd.Timedelta(days=int(r.integers(3, 12))), hours * r.uniform(41, 58))
        elif x.kind == "NOWORK":
            hours = r.uniform(1.5, 3.0)
            post(x.wo_number, "LABOR", d + pd.Timedelta(days=int(r.integers(0, 4))), hours * 4 * r.uniform(118, 134))
            post(x.wo_number, "FLEET", d + pd.Timedelta(days=int(r.integers(3, 12))), hours * r.uniform(41, 58))
        else:
            if r.random() < .6:
                post(x.wo_number, "LABOR", d - pd.Timedelta(days=int(r.integers(0, 6))), r.uniform(1.0, 2.5) * 2 * r.uniform(118, 134))
    L = pd.DataFrame(rows, columns=["wo_number", "cost_element", "posting_date", "amount", "document"])
    # lines posted to the wrong order, reversed and re-posted to the right one
    rr = K.rng("mispost")
    wos_all = wos["wo_number"].values
    extra = []
    for i in rr.choice(L.index.values, size=9, replace=False):
        x = L.loc[i]
        wrong = int(rr.choice(wos_all[wos_all != x.wo_number]))
        d0 = x.posting_date
        extra.append((wrong, x.cost_element, d0, x.amount, x.document))
        extra.append((wrong, x.cost_element, d0 + pd.Timedelta(days=int(rr.integers(5, 30))), -x.amount, x.document + "-R"))
        L.loc[i, "posting_date"] = d0 + pd.Timedelta(days=int(rr.integers(5, 30)))
        L.loc[i, "document"] = x.document + "-C"
    L = pd.concat([L, pd.DataFrame(extra, columns=L.columns)], ignore_index=True)
    L = L.sort_values(["posting_date", "document", "wo_number"]).reset_index(drop=True)
    L["fiscal_period"] = L["posting_date"].dt.strftime("%Y-%m")
    return L


def nudge_costs(L, wos, n_by_district, need=0.26):
    """Keep each district's cost per replacement a quarter-dollar or more from a rounding edge: the district's last
    labor line takes the smallest cent adjustment that does it."""
    dist = dict(zip(wos["wo_number"], wos["district"]))
    for name, n in n_by_district.items():
        m = L["wo_number"].map(dist) == name
        tot = L.loc[m, "amount"].sum()
        i = L[m & (L.cost_element == "LABOR")].index[-1]
        for c in range(0, 100 * n):
            v = (tot + c / 100.0) / n
            if abs(v - np.floor(v) - 0.5) >= need:
                L.loc[i, "amount"] = round(L.loc[i, "amount"] + c / 100.0, 2)
                break
    return L


# ------------------------------------------------------------------------------------------------- outages
CAUSES = [("TREE", .27), ("ANML", .17), ("EQ-CUTOUT", .10), ("EQ-CONN", .09), ("VEH", .04), ("PLND", .14), ("UNK", .19)]
NEIGHBOUR = {"Foothill": "Highland", "Railyard": "Canal", "Canal": "Brookside", "Mission": "West Bluff",
             "West Bluff": "Kingsley", "Crestview": "Lakeside", "Lakeside": "Highland", "Sunrise": "Mission",
             "Sandhill": "Kingsley", "Kingsley": "Mission", "Highland": "Crestview", "Brookside": "Railyard"}


def outages(T):
    """The OMS transformer outage lines for the summer export (16 May to 15 October 2026, UTC): one line per transformer
    de-energised in an event, the event's customers out on each of its lines. A failure on a fused tap or a loop often
    takes the tap's or loop's fuse, so its event covers every transformer on it; the others come back when the fuse is
    re-closed with the failed unit isolated, the failed unit's customers when its replacement is energised."""
    tx = T.tx.set_index("ti")
    r = K.rng("oms")
    T.fail_restored = {}
    nsp = tx["n_prem"].to_dict()
    lat_members = T.tx.groupby("lateral")["ti"].apply(list).to_dict()
    lat_of = tx["lateral"].to_dict()
    pk_day = (pd.Timestamp("2026-06-01") + pd.to_timedelta(tx["pkday2026"].astype(int), unit="D")).to_dict()
    pk_q = tx["pkq2026"].astype(int).to_dict()
    # boundary feeders: a crew from the neighbouring district answers
    feeders = T.tx.groupby(["district", "feeder"]).size().reset_index()[["district", "feeder"]]
    rb = K.rng("boundary")
    border = set((d, f) for d, f in zip(feeders["district"], feeders["feeder"]) if rb.random() < .07)
    events = []
    used = set()
    busy_ivals = {}
    rl = K.rng("fuse-ids")
    lat_ids = sorted(lat_members)
    fuse_no = dict(zip(lat_ids, 30000 + np.sort(rl.choice(np.arange(1, 69999), size=len(lat_ids), replace=False))[rl.permutation(len(lat_ids))]))

    def device(t, multi_line):
        if multi_line:
            return ("LF%05d" % fuse_no[lat_of[t]]) if tx.loc[t, "mount"] == "OH" else ("EF%05d" % fuse_no[lat_of[t]])
        return ("CO-T%d" % tx.loc[t, "loc"]) if tx.loc[t, "mount"] == "OH" else ("XF-T%d" % tx.loc[t, "loc"])

    def free(u, s, e):
        return all(e <= a or s >= b for a, b in busy_ivals.get(u, []))

    def book(ok):
        for u, s, e in ok:
            busy_ivals.setdefault(u, []).append((s, e))

    def overlaps_peak(t, s, e):
        p0 = pk_day[t] + pd.Timedelta(hours=16 + 0.25 * pk_q[t])
        return s < p0 + pd.Timedelta(minutes=15) and e > p0

    def dur_ok(h):
        return abs(h - 8.0) > 0.2

    # failures
    for x in T.fail.sort_values(["date", "hour"]).itertuples():
        t = int(x.ti)
        s = pd.Timestamp(x.date) + pd.Timedelta(hours=float(x.hour))
        s = s.floor("min")
        busy = 1.0 if not x.hot else float(r.uniform(1.6, 3.4))
        rep = float(np.clip(r.gamma(5.0, 0.85) * busy + 1.2, 2.2, 17.5))
        while not dur_ok(rep):
            rep += 0.35
        mt = tx.loc[t, "mount"]
        multi = r.random() < (0.50 if mt == "PAD" else 0.20)
        mates = [u for u in lat_members[lat_of[t]] if u != t and u not in used] if multi else []
        if mates:
            # with the tap or loop back on behind the failed unit's open fuse, the unit waits for a line truck with a
            # replacement on it
            rep += float(r.uniform(1.5, 5.0))
            while not dur_ok(rep):
                rep += 0.35
        lines = [(t, rep)]
        for u in mates:
            refuse = float(np.clip(r.gamma(3.0, 0.45) + 0.4, 0.5, 3.4))
            while not dur_ok(refuse):
                refuse += 0.25
            lines.append((u, refuse))
        ok = []
        for u, h in lines:
            e = s + pd.Timedelta(minutes=int(round(h * 60)))
            if u != t and (overlaps_peak(u, s, e) or not free(u, s, e)):
                continue
            ok.append((u, s, e))
        used.update(u for u, _, _ in ok)
        book(ok)
        T.fail_restored[t] = ok[0][2]
        events.append(("EQ-XFMR", ok, device(t, len(ok) > 1), tx.loc[t, "district"], tx.loc[t, "feeder"]))
    # the other causes, all summer (and the export's edges), with the September heat wave's overload operations
    n_other = int(0.021 * len(tx))
    pool = tx.index.values
    lo = pd.Timestamp("2026-05-16") - PDT
    span_min = int((pd.Timestamp("2026-10-15 23:59") - lo).total_seconds() // 60)
    for _ in range(n_other):
        t = int(r.choice(pool))
        c = CAUSES[int(r.choice(len(CAUSES), p=np.array([p for _, p in CAUSES]) / sum(p for _, p in CAUSES)))][0]
        if tx.loc[t, "mount"] == "PAD" and c in ("TREE", "ANML") and r.random() < .7:
            c = "EQ-CONN"
        s = (lo + pd.Timedelta(minutes=int(r.integers(0, span_min))) + PDT).floor("min")
        if c == "PLND":
            s = s.normalize() + pd.Timedelta(hours=float(r.choice([8, 8.5, 9, 9.5, 10, 13])))
        multi = r.random() < (0.35 if c in ("TREE", "PLND", "VEH") else 0.15)
        h0 = float(np.clip(r.gamma(2.6, 0.9) + 0.3, 0.4, 11.0)) if c != "PLND" else float(r.uniform(2, 6))
        mem = [u for u in lat_members[lat_of[t]]] if multi else [t]
        ok = []
        for u in mem:
            h = h0 if u == t else max(0.4, h0 * float(r.uniform(0.3, 1.0)))
            while not dur_ok(h):
                h += 0.3
            e = s + pd.Timedelta(minutes=int(round(h * 60)))
            if overlaps_peak(u, s, e) or not free(u, s, e):
                continue
            ok.append((u, s, e))
        if ok and t in [u for u, _, _ in ok]:
            book(ok)
            events.append((c, ok, device(t, len(mem) > 1), tx.loc[t, "district"], tx.loc[t, "feeder"]))
    heat_lo = pd.Timestamp(K.HEAT[2026][0])
    hot = T.tx[(T.tx.pk2026 / T.tx.kva_mid > 1.18) & ~T.tx.ti.isin(set(T.fail.ti))]
    for t in r.choice(hot["ti"].values, size=min(len(hot), int(0.42 * len(hot))), replace=False):
        t = int(t)
        s = (heat_lo + pd.Timedelta(days=int(r.integers(0, K.HEAT[2026][1])),
                                    hours=float(np.clip(r.normal(19.0, 1.1), 16.4, 22.5)))).floor("min")
        h = float(np.clip(r.gamma(2.2, 0.8) + 0.5, 0.6, 7.5))
        while not dur_ok(h):
            h += 0.3
        e = s + pd.Timedelta(minutes=int(round(h * 60)))
        if overlaps_peak(t, s, e) or not free(t, s, e):
            s = s + pd.Timedelta(days=1)
            e = e + pd.Timedelta(days=1)
            if overlaps_peak(t, s, e) or not free(t, s, e):
                continue
        book([(t, s, e)])
        events.append(("OL-XFMR", [(t, s, e)], device(t, False), tx.loc[t, "district"], tx.loc[t, "feeder"]))
    events.sort(key=lambda ev: (ev[1][0][1], ev[2]))
    rows = []
    eid = 2026051600
    for c, ok, dev, dist, fd in events:
        eid += int(r.integers(1, 6))
        cust = int(sum(nsp[u] for u, _, _ in ok))
        disp = NEIGHBOUR[dist] if (dist, fd) in border else dist
        for j, (u, s, e) in enumerate(ok):
            rows.append((eid, j + 1, "T%d" % tx.loc[u, "loc"], dev, s, e, c, cust, disp, u))
    O = pd.DataFrame(rows, columns=["event_id", "line", "xfmr_loc_id", "device_id", "start_local", "restored_local",
                                    "cause_code", "customers_out", "dispatch_district", "_ti"])
    O["outage_start_utc"] = O["start_local"] + PDT
    O["restored_utc"] = O["restored_local"] + PDT
    keep = (O["outage_start_utc"] >= pd.Timestamp("2026-05-16")) & (O["outage_start_utc"] < pd.Timestamp("2026-10-16"))
    return O[keep].reset_index(drop=True)


def ask_b_golden(T, O):
    tx = T.tx.set_index("ti")
    f = O[(O.cause_code == "EQ-XFMR") & (O.start_local >= WIN_LO) & (O.start_local < WIN_HI)].copy()
    f["sp"] = f["_ti"].map(tx["n_prem"])
    f["district"] = f["_ti"].map(tx["district"])
    f["hours"] = (f["restored_local"] - f["start_local"]).dt.total_seconds() / 3600.0
    ch = (f["sp"] * f["hours"]).groupby(f["district"]).sum().reindex(K.NAMES).fillna(0.0)
    over8 = f[f.hours > 8.0]["sp"].groupby(f[f.hours > 8.0]["district"]).sum().reindex(K.NAMES).fillna(0).astype(int)
    return ch, over8, f


def nudge_outages(T, O, need=0.26):
    """Keep each district's failure customer-hours a quarter-hour or more from a rounding edge: the district's last
    failure line takes the smallest whole-minute shift in its restoration that does it."""
    for _ in range(3):
        ch, over8, f = ask_b_golden(T, O)
        moved = False
        for name in K.NAMES:
            v = ch[name]
            if abs(v - np.floor(v) - 0.5) >= need:
                continue
            g = f[f.district == name]
            i = g.index[-1]
            sp = int(g.loc[i, "sp"])
            h = float(g.loc[i, "hours"])
            for m in range(1, 60):
                for sgn in (1, -1):
                    v2 = v + sgn * m * sp / 60.0
                    h2 = h + sgn * m / 60.0
                    if abs(v2 - np.floor(v2) - 0.5) >= need and abs(h2 - 8.0) > 0.2 and h2 > 0.3:
                        O.loc[i, "restored_local"] += pd.Timedelta(minutes=sgn * m)
                        O.loc[i, "restored_utc"] += pd.Timedelta(minutes=sgn * m)
                        moved = True
                        break
                else:
                    continue
                break
        if not moved:
            break
    return O
