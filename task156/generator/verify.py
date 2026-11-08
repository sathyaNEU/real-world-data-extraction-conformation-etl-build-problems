"""Independent verifier: reads only target/ and golden/, on its own code path (pandas readers, its own spell and
cluster logic, its own day-step forecast), and recomputes the call, the rate route's set and every ask figure.
python3 task156/generator/verify.py"""
import os
import re
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
BAD = []


def check(cond, msg):
    print(("ok    " if cond else "DIFF  ") + msg)
    if not cond:
        BAD.append(msg)


def ie(s, fmt):
    return pd.to_datetime(s, format=fmt).dt.tz_localize("Europe/Dublin").dt.tz_convert("UTC")


def text(pdf):
    return subprocess.run(["pdftotext", "-layout", os.path.join(T, pdf), "-"], capture_output=True, text=True).stdout


def main():
    sched = text("concession_agreement_schedules_4_and_6.pdf")
    flat = re.sub(r"\s+", " ", sched)
    check("The Availability Standard is 99 per cent" in flat, "Schedule 4 reads back: the standard (positive control)")
    check("any high-power charge point will fall below the Availability Standard" in flat and "approved renewal programme" in flat,
          "Schedule 4 reads back: clause 4.6's listing rule and asset base")
    check("from connection to disconnection" in flat and "counted once, in the month in which it began" in flat and
          "the energy the charge point's meter registered" in flat, "Schedule 6 reads back: a charge and its energy")
    prog = text("asset_renewal_programme_2027.pdf")
    rows = re.findall(r"^\s*(NM\d{3})\s+.+?\s+(\d{2}/\d{2}/\d{4})\s+(Yes|No)\b", prog, re.M)
    check(len(rows) == 12, "the programme's table reads back: %d hubs" % len(rows))
    works = {c: pd.Timestamp(pd.to_datetime(d + " 09:30", format="%d/%m/%Y %H:%M")).tz_localize("Europe/Dublin").tz_convert("UTC")
             for c, d, _ in rows}
    newu = {c: y == "Yes" for c, _, y in rows}

    reg = pd.read_excel(os.path.join(T, "charge_point_register.xlsx"), sheet_name=None)
    cp, hubs = reg["Charge points"], reg["Hubs"]
    alias = dict(zip(cp["Previous ID (to 09/06/2025)"], cp["Charge point ID"]))
    alias.update(dict(zip(cp["Charge point ID"], cp["Charge point ID"])))
    hub_of = dict(zip(cp["Charge point ID"], cp["Hub code"]))
    model = dict(zip(cp["Charge point ID"], cp["Model"]))
    comm = {k: pd.Timestamp(v).tz_localize("Europe/Dublin").tz_convert("UTC") + pd.Timedelta(hours=11)
            for k, v in zip(cp["Charge point ID"], cp["Commissioned"])}
    t0 = pd.Timestamp("2023-01-01", tz="UTC")
    end = pd.Timestamp("2026-11-01", tz="UTC")
    st = pd.read_csv(os.path.join(T, "connector_status_history_2023-2026.csv"))
    st["k"] = st["charge_point_id"].map(alias)
    st["t"] = pd.to_datetime(st["timestamp_utc"], utc=True)
    st = st.sort_values(["k", "t"])
    st = st[st["status"] != st.groupby("k")["status"].shift()]
    sp = {}
    for k, g in st.groupby("k"):
        ts, ss = list(g["t"]), list(g["status"])
        sp[k] = [(ts[i], ts[i + 1] if i + 1 < len(ts) else end, ss[i]) for i in range(len(ts)) if ss[i] != "Available"]
    ex = {c: [] for c in hubs["Hub code"]}
    visits27 = {c: [] for c in hubs["Hub code"]}
    ppm = pd.read_excel(os.path.join(T, "planned_maintenance_schedule.xlsx"), sheet_name=None)
    for name, df in ppm.items():
        if "Visit 1" in df.columns:
            for _, r in df.iterrows():
                for c in [x for x in df.columns if str(x).startswith("Visit")]:
                    if pd.notna(r[c]):
                        d = pd.Timestamp(r[c]).strftime("%Y-%m-%d")
                        a, b = r["Window"].split("-")
                        ex[r["Hub code"]].append((pd.Timestamp(d + " " + a).tz_localize("Europe/Dublin").tz_convert("UTC"),
                                                  pd.Timestamp(d + " " + b).tz_localize("Europe/Dublin").tz_convert("UTC") + pd.Timedelta(minutes=30)))
        else:
            for _, r in df.iterrows():
                d = pd.Timestamp(r["Visit date"]).strftime("%Y-%m-%d")
                w = (pd.Timestamp(d + " " + r["Window from"]).tz_localize("Europe/Dublin").tz_convert("UTC"),
                     pd.Timestamp(d + " " + r["Window to"]).tz_localize("Europe/Dublin").tz_convert("UTC") + pd.Timedelta(minutes=30))
                (visits27 if name.startswith("2027") else ex)[r["Hub code"]].append(w)
    dso = pd.read_csv(os.path.join(T, "supply_interruptions_2023-2026.csv"))
    dso["s"] = ie(dso["interruption_start_irish_time"], "%Y-%m-%d %H:%M")
    dso["e"] = ie(dso["supply_restored_irish_time"], "%Y-%m-%d %H:%M")
    years = (end - t0).total_seconds() / (365 * 86400.0)
    dso_rate = dso.groupby("hub_code").size().reindex(hubs["Hub code"], fill_value=0) / years
    for _, r in dso.iterrows():
        ex[r["hub_code"]].append((r["s"], r["e"] + pd.Timedelta(minutes=30)))

    # pillar power-downs: every unit at a hub that was up going Offline within six minutes of the first
    clusters, ups, hangs, faults = {}, {}, {}, {}
    for c in hubs["Hub code"]:
        ks = [k for k in hub_of if hub_of[k] == c]
        offs = sorted((a, k) for k in ks for a, b, s in sp.get(k, []) if s == "Offline")
        out, i = [], 0
        while i < len(offs):
            j = i
            while j + 1 < len(offs) and (offs[j + 1][0] - offs[i][0]).total_seconds() <= 360:
                j += 1
            mem = set(k for _, k in offs[i:j + 1])
            if len(mem) >= 2:
                a0 = offs[i][0]
                up = set(k for k in ks if comm[k] <= a0 and not any(a < a0 - pd.Timedelta(seconds=60) < b and s in ("Offline", "Faulted")
                                                                    for a, b, s in sp.get(k, []) if a < a0))
                if up <= mem:
                    out.append((a0, offs[j][0]))
            i = j + 1
        clusters[c] = out
        for k in ks:
            if model[k] != "HX150":
                continue
            u, h, f, prev = [], [], [], None
            for a, b, s in sp.get(k, []):
                if s == "Faulted":
                    f.append((a, b))
                elif s == "Offline":
                    if prev is not None and prev[2] == "Faulted" and abs((prev[1] - a).total_seconds()) <= 1:
                        u.append(b)
                    elif any(c0 - pd.Timedelta(seconds=5) <= a <= c1 + pd.Timedelta(seconds=5) for c0, c1 in out):
                        u.append(b)
                    elif (b - a).total_seconds() >= 3 * 3600 or any(a + pd.Timedelta(minutes=30) < c0 < b for c0, _ in out):
                        h.append((a - pd.Timedelta(seconds=750), b))
                        u.append(b)
                prev = (a, b, s)
            ups[k], hangs[k], faults[k] = [x for x in u if x < end], h, f
    expo, ev = np.zeros(401), np.zeros(401)
    for k in ups:
        marks = sorted([(t, 0) for t in ups[k]] + [(a, 1) for a, _ in hangs[k]] + [(a, 2) for a, _ in faults[k]])
        last = None
        for t, kind in marks + [(end, 3)]:
            if last is not None:
                tau = (t - last).total_seconds() / 86400.0
                n = int(min(tau, 400))
                expo[:n] += 1
                if n < 400:
                    expo[n] += tau - n
                if kind == 1:
                    ev[min(n, 400)] += 1
                last = None
            if kind == 0:
                last = t
    h5 = np.zeros(401)
    for b0 in range(0, 90, 5):
        h5[b0:b0 + 5] = ev[b0:b0 + 5].sum() / expo[b0:b0 + 5].sum() if expo[b0:b0 + 5].sum() else 0
    h5[90:] = ev[90:].sum() / expo[90:].sum()
    check(ev[:75].sum() == 0 and ev.sum() >= 60, "the life table: %d hangs, the first on day %d since power-up" % (ev.sum(), np.nonzero(ev)[0].min()))

    # the day-step forecast, this verifier's own
    from scipy.stats import gamma
    nov = pd.Timestamp("2026-11-01", tz="UTC")
    y27 = pd.Timestamp("2027-01-01", tz="UTC")
    ndays = 426
    side, naive = {}, {}
    for c in hubs["Hub code"]:
        ks = [k for k in hub_of if hub_of[k] == c]
        hx = [k for k in ks if model[k] == "HX150"]
        calls = []
        for k in ks:
            s_ = sp.get(k, [])
            for i in range(len(s_) - 1):
                if s_[i][2] == "Faulted" and s_[i + 1][2] == "Offline" and abs((s_[i + 1][0] - s_[i][1]).total_seconds()) <= 1:
                    calls.append((s_[i][1] - s_[i][0]).total_seconds() / 86400.0)
        hd = [(b - a).total_seconds() / 86400.0 for k in hx for a, b in hangs[k]]
        att = float(np.mean(calls + hd))
        yrs = {k: (end - max(t0, comm[k])).total_seconds() / (365 * 86400.0) for k in hx}
        frate = sum(len(faults[k]) for k in hx) / sum(yrs.values())
        reps = []
        for k in hx:
            s_ = sp.get(k, [])
            for i in range(len(s_) - 1):
                if s_[i][2] == "Faulted" and s_[i + 1][2] == "Offline":
                    reps.append((s_[i + 1][1] - s_[i][0]).total_seconds() / 86400.0)
        rep = float(np.mean(reps)) if reps else 1.5
        comms = []
        for k in hx:
            hs = set(a for a, _ in hangs[k])
            co = [(b - a).total_seconds() for a, b, s in sp.get(k, []) if s == "Offline" and (b - a).total_seconds() < 3 * 3600
                  and not any(c0 - pd.Timedelta(seconds=5) <= a <= c1 + pd.Timedelta(seconds=5) for c0, c1 in clusters[c])
                  and a - pd.Timedelta(seconds=750) not in hs]
            comms.append(sum(co) / 86400.0 / yrs[k])
        other = [c0 for c0, _ in clusters[c] if not any(a <= c0 <= b + pd.Timedelta(hours=1) for a, b in ex[c])]
        orate = len(other) / years
        oiso = []
        for k in hx:
            for a, b, s in sp.get(k, []):
                if s == "Offline" and any(abs((a - c0).total_seconds()) <= 600 for c0 in other):
                    oiso.append((b - a).total_seconds() / 86400.0)
        iso_days = orate * (float(np.mean(oiso)) if oiso else 0.0)
        exd = sum(((b - a).total_seconds()) for a, b in visits27[c]) / 86400.0 + dso_rate[c] * (
            float(((dso[dso.hub_code == c]["e"] - dso[dso.hub_code == c]["s"]).dt.total_seconds().mean() if (dso.hub_code == c).any() else 3600) + 1800) / 86400.0)
        j = np.arange(60) + 0.5
        rel = 1 - gamma.sf(j, 3, scale=att / 3.0) / np.maximum(gamma.sf(j - 1, 3, scale=att / 3.0), 1e-12)
        vdays = set(int((a - nov).total_seconds() // 86400) for a, _ in visits27[c])
        wday = int((works[c] - nov).total_seconds() // 86400) if c in works else None
        units = [(k, False) for k in hx] + ([("new", True)] if newu.get(c) else [])
        res = []
        for k, new in units:
            start = (works[c] + pd.Timedelta(hours=5)) if new else (ups[k][-1] if ups[k] else comm[k])
            k0 = int(min(400, max(0, (nov - start).total_seconds() // 86400)))
            pu, ph = np.zeros(401), np.zeros(60)
            pu[k0] = 1.0
            hung = 0.0
            for d in range(ndays):
                if d in vdays or d == wday:
                    pu, ph = np.concatenate([[pu.sum() + ph.sum()], np.zeros(400)]), np.zeros(60)
                else:
                    q = dso_rate[c] / 365.0 + (orate / 365.0 if (wday is None or d < wday) else 0.0)
                    m = q * (pu.sum() + ph.sum())
                    pu, ph = pu * (1 - q), ph * (1 - q)
                    pu[0] += m
                fm = frate / 365.0 * pu.sum()
                pu = pu * (1 - frate / 365.0)
                pu[0] += fm
                nh = (pu * h5).sum()
                pu = pu * (1 - h5)
                pu = np.concatenate([[0.0], pu[:-1]]) + np.concatenate([np.zeros(400), [pu[-1]]])
                rl = (ph * rel).sum()
                ph = np.concatenate([[nh], (ph * (1 - rel))[:-1]])
                pu[0] += rl
                if d >= int((y27 - nov).total_seconds() // 86400):
                    hung += ph.sum()
            cm = float(np.mean(comms))
            iso = 0.0 if (c in works or new) else iso_days
            res.append(1 - (hung + frate * rep + cm + iso) / (365.0 - exd))
            if not new:
                rate_h = len(hangs[k]) / yrs[k]
                hdt = float(np.mean([(b - a).total_seconds() / 86400.0 for a, b in hangs[k]])) if hangs[k] else att
                naive.setdefault(c, []).append(1 - (rate_h * hdt + len(faults[k]) / yrs[k] * rep + cm + iso) / (365.0 - exd))
        side[c] = min(res)
    call = sorted(c for c, v in side.items() if v < 0.99)
    nset = sorted(c for c, v in naive.items() if min(v) < 0.99)
    g = pd.read_csv(os.path.join(GOLD, "hub_availability_2027.csv"))
    gset = sorted(g[g["below_99_per_cent_2027"] == "Yes"]["hub_code"])
    check(call == gset, "the call: the verifier's own day-step forecast lists %d hubs, the golden %d (%s)" % (len(call), len(gset),
          "same" if call == gset else "differ: %s" % sorted(set(call) ^ set(gset))))
    check(min(abs(v - 0.99) for v in side.values()) > 0.002, "no verifier forecast sits on the line (closest %.2f points)"
          % (100 * min(abs(v - 0.99) for v in side.values())))
    check(len(nset) == 5 and set(nset) <= set(gset), "the rate route lists %d hubs: %s" % (len(nset), ", ".join(nset)))

    s = pd.read_csv(os.path.join(T, "charging_sessions_2026.csv"), dtype={"id_tag": str})
    s = s.drop_duplicates("session_id")
    s["a"] = pd.to_datetime(s["start_time_utc"], utc=True)
    s["b"] = pd.to_datetime(s["stop_time_utc"], utc=True)
    s = s[s["charge_point_id"].map(model) == "HX150"].sort_values(["charge_point_id", "connector_id", "a", "session_id"])
    grp = s.groupby(["charge_point_id", "connector_id"])
    cont = (s["meter_start_wh"] > grp["meter_stop_wh"].shift()) | ((s["a"] - grp["b"].shift()).dt.total_seconds().between(0, 5))
    s["charge"] = (~cont).cumsum()
    ch = s.groupby("charge").agg(cp=("charge_point_id", "first"), a=("a", "first"), m0=("meter_start_wh", "first"),
                                 m1=("meter_stop_wh", "last"))
    ch = ch[(ch.m1 > ch.m0) & (ch.a >= pd.Timestamp("2026-01-01", tz="Europe/Dublin")) & (ch.a < pd.Timestamp("2026-11-01", tz="Europe/Dublin"))]
    ch["hub"] = ch["cp"].map(hub_of)
    n = ch.groupby("hub").size()
    e = ch.assign(wh=ch.m1 - ch.m0).groupby("hub")["wh"].sum()
    gi = g.set_index("hub_code")
    nn = sum(int(n.get(c, 0)) == int(gi.loc[c, "charges_jan_oct_2026"]) for c in gi.index)
    ne = sum(float(Decimal(e.get(c, 0) / 1e6).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)) == float(gi.loc[c, "energy_jan_oct_2026_mwh"])
             for c in gi.index)
    check(nn == 30 and ne == 30, "the asks: %d of 30 charges figures and %d of 30 energy figures reproduce" % (nn, ne))
    print("\n%d disagreements" % len(BAD))
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
