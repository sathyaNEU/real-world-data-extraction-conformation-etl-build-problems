"""Every graded figure, computed from the shipped files under target/ only, and the routes the ceiling scores."""
import os
import numpy as np
import pandas as pd
import ladder as L
import asks

D0 = pd.Timestamp("2020-10-01")
NEW_SUP = "Brekke Power Products"
CHANGES = {"G": "Restoration switching template SO-7 revision", "R": "Heat pump connections without a load study",
           "D": "Riser termination replacements suspended", "E": "Animal guard programme ended",
           "F": "Transformer supplier change"}


def mins(s):
    return (pd.to_datetime(s) - D0).dt.total_seconds() / 60.0


def load(T):
    P = {}
    reg = pd.read_excel(os.path.join(T, "system_register_2026-09-30.xlsx"), sheet_name=None)
    sec, cw, rc = reg["sections"], reg["gis_crosswalk"], reg["reclosing_devices"]
    old2new = dict(zip(cw.old_section_id, cw.section_id))
    ev = pd.read_csv(os.path.join(T, "outage_events_fy2022-fy2026.csv"), dtype=str, keep_default_na=False)
    F = pd.DataFrame({"sec": ev.section_id.map(lambda x: old2new.get(x, x)), "start": mins(ev.start_local), "end": mins(ev.end_local),
                      "level": np.where(ev.device_type == "XFMR", "transformer", "section"), "xf": ev.transformer_id,
                      "ci": ev.customers_interrupted.astype(int), "cause": ev.cause_code, "planned": ev.planned == "Y",
                      "site": ev.structure_id, "riser": ev.structure_id, "feeder": ev.feeder, "device": ev.device_id,
                      "wo": ev.work_order})
    P["F"] = F
    wx = pd.read_csv(os.path.join(T, "hq_substation_temperature_hourly.csv"))
    loc = pd.to_datetime(wx.time_utc.str.replace("Z", ""), utc=True).dt.tz_convert(asks.TZ).dt.tz_localize(None)
    dm = wx.value.groupby((loc.dt.normalize() - D0).dt.days).mean()
    P["daymean"] = dm
    P["daymin"] = wx.value.groupby((loc.dt.normalize() - D0).dt.days).min()
    dr = pd.read_excel(os.path.join(T, "daily_reliability_fy2021-fy2026.xlsx"), sheet_name=None)
    leg, oms = dr["Legacy OMS to Feb 2023"], dr["OMS daily"]
    a = pd.Series(leg["SAIDI Hrs"].values * 60.0, index=(pd.to_datetime(leg.Date, format="%m/%d/%Y") - D0).dt.days.values)
    b = pd.Series(oms.saidi_min.values, index=(pd.to_datetime(oms.date) - D0).dt.days.values)
    daily = pd.concat([a, b]).sort_index()
    P["tmed"], P["med"] = L.med_days(daily)
    rb = pd.read_excel(os.path.join(T, "heat_pump_rebates_fy2024-fy2026.xlsx"))
    rb = rb[rb.load_study == "waived"]
    rb["xf"] = rb.service_transformer.str.replace("T-", "T", regex=False)
    P["rebate_xf"] = ((pd.to_datetime(rb.connected) - D0).dt.days).groupby(rb.xf).min().to_dict()
    al = pd.read_excel(os.path.join(T, "asset_programme_lists_2022-2026.xlsx"), sheet_name=None)
    P["sites_2026"] = set(al["animal_guards"].structure_id[al["animal_guards"].list_year == 2026])
    rr = al["riser_replacements"]
    P["risers_2025"] = set(rr.riser_structure_id[rr.list_year == 2025])
    un = pd.read_parquet(os.path.join(T, "transformer_units.parquet"))
    nu = un[(un.supplier == NEW_SUP) & (pd.to_datetime(un.fitted) >= "2026-02-01")]
    P["unit_fit"] = ((pd.to_datetime(nu.fitted) - D0).dt.days).groupby(nu.transformer_id).min().to_dict()
    P["sec"], P["rc"] = sec, rc
    P["members"] = int(sec.members.sum())
    P["T"] = T
    return P


def main_figures(P, **kw):
    F, med = P["F"], P["med"]
    out = {"G": L.golden_switching(F, med, **kw), "R": L.replay_heat_pumps(F, med, P["rebate_xf"]),
           "E": L.replay_guards(F, med, P["sites_2026"]), "D": L.replay_risers(F, med, P["risers_2025"]),
           "F": L.replay_supplier(F, med, P["unit_fit"])}
    return out


FROSTS = [("none", None, None, None)] + [("day mean <= %d C on the %s day" % (t, on), "mean", t, on)
                                         for t in (0, -2, -3, -5) for on in ("trip's", "outage's")] + \
         [("day minimum <= 0 C on the %s day" % on, "min", 0, on) for on in ("trip's", "outage's")]
PAIRINGS = ("the section's own devices, previous record", "every record of the section, previous record",
            "the section's latest restoration before a trip at either level")
NETTING = (("fiscal 2025 staged era", (L.Y1, L.G_DAY)), ("staged era from fiscal 2022", (L.day("2021-10-01"), L.G_DAY)),
           ("not netted", None))


def _tables(F):
    sec = F[F.level == "section"]
    S = sec.sort_values(["sec", "start"]).copy()
    g = S.groupby("sec"); S["pend"] = g.end.shift(1); S["pstart"] = g.start.shift(1)
    A = F.sort_values(["sec", "start"]).copy()
    g = A.groupby("sec"); A["pend"] = g.end.shift(1); A["pstart"] = g.start.shift(1)
    R = sec[["sec", "start", "end"]].rename(columns={"start": "pstart", "end": "pend"}).sort_values("pend")
    B = pd.merge_asof(F.reset_index().sort_values("start"), R, left_on="start", right_on="pend", by="sec",
                      direction="backward").set_index("index")
    return {PAIRINGS[0]: (S, sec), PAIRINGS[1]: (A, F), PAIRINGS[2]: (B, sec)}


def _cost(Tb, Q, med, W, dmin, fr, on, cause, staged):
    gap, dur = Tb.start - Tb.pend, Tb.pend - Tb.pstart
    pr = (gap >= 0) & (gap <= W) & (dur >= dmin) & ~(Tb.start // 1440).isin(med)
    if cause:
        pr &= Tb.cause == cause
    if fr is not None:
        pr &= ((Tb.pstart // 1440) if on == "outage's" else (Tb.start // 1440)).isin(fr)
    val = float(Tb.ci[pr & (Tb.start >= L.G_DAY * 1440) & (Tb.start < L.YE * 1440)].sum())
    if staged is None:
        return val
    q = ((Q.end - Q.start) >= dmin) & ~(Q.start // 1440).isin(med) & ~pr.reindex(Q.index, fill_value=False)
    if fr is not None:
        q &= ((Q.start // 1440) if on == "outage's" else (Q.end // 1440)).isin(fr)
    sp = pr & (Tb.start >= staged[0] * 1440) & (Tb.end < staged[1] * 1440)
    sq = q & (Q.start >= staged[0] * 1440) & (Q.end < staged[1] * 1440)
    rate = Tb.ci[sp].sum() / max(Q.ci[sq].sum(), 1)
    return val - rate * float(Q.ci[q & (Q.end >= L.G_DAY * 1440) & (Q.start < L.YE * 1440)].sum())


def variants(P):
    """The revision's cost under every operationalisation a solver who pairs might add: the pairing window (5 to 30
    minutes), the qualifying outage (30 to 120 minutes), a frost filter (none; a day mean at or below 0, -2, -3 or -5 C or
    a day minimum at or below 0 C, on the trip's day or the outage's start day, local dates), overload trips or every
    trip, the pairing sequence, and the netting. Returns {(window, length, frost, cause, pairing, netting): cost}."""
    F = P["F"][~P["F"].planned]
    tabs = _tables(F)
    sets = {}
    for name, kind, t, on in FROSTS:
        if kind is not None:
            s = P["daymean"] if kind == "mean" else P["daymin"]
            sets[name] = (set(s.index[s.values <= t]), on)
        else:
            sets[name] = (None, None)
    out = {}
    for pname, (Tb, Q) in tabs.items():
        for nname, staged in NETTING:
            for cause in ("OVLD", None):
                for fname, (fr, on) in sets.items():
                    for W in (5, 10, 15, 20, 30):
                        for dmin in (30, 60, 90, 120):
                            out[(W, dmin, fname, cause or "every cause", pname, nname)] = _cost(Tb, Q, P["med"], W, dmin, fr, on, cause, staged)
    return out


# ------------------------------------------------------------------ Ask A from the files
def scada_events(P, lockout_by="oms"):
    T = P["T"]
    op = pd.read_csv(os.path.join(T, "scada_reclosing_operations_fy2026.csv"))
    utc = pd.to_datetime(op.time_utc.str.replace("Z", ""), utc=True)
    op["t"] = (utc.dt.tz_convert(asks.TZ).dt.tz_localize(None) - D0).dt.total_seconds() / 60.0
    op["t_utc"] = (utc.dt.tz_localize(None) - D0).dt.total_seconds() / 60.0
    rc = P["rc"]
    rsec = dict(zip(rc.device_id[rc.type == "LINE RECLOSER"], rc.section_id[rc.type == "LINE RECLOSER"]))
    op["kind"] = np.where(op.device_id.str.startswith("CB-"), "B", "R")
    op["id"] = np.where(op.kind == "B", op.device_id.str[3:], op.device_id.map(rsec))
    # a device's operations within five minutes of a sequence's first trip are one sequence
    op = op.sort_values(["device_id", "t"]).reset_index(drop=True)
    seq = np.zeros(len(op), int); k = 0; start = -1e9; last = None
    for i, (d, t, o) in enumerate(zip(op.device_id.values, op.t.values, op.operation.values)):
        if d != last or (o == "TRIP" and t - start > 5.0) or (o == "CLOSE" and t - start > 5.0):
            k += 1; start = t
        last = d
        seq[i] = k
    op["seq"] = seq
    g = op.groupby("seq")
    first = g.t.min(); lastop = g.operation.last(); trips = g.operation.apply(lambda s: (s == "TRIP").sum())
    S = pd.DataFrame({"t": first, "t_utc": g.t_utc.min(), "kind": g.kind.first(), "id": g.id.first(), "dev": g.device_id.first(),
                      "last": lastop, "trips": trips, "t_last": g.t.max()})
    S = S[S.trips > 0]
    if lockout_by == "oms":
        F = P["F"]
        sus = F[(F.level == "section") & ~F.planned]
        lk = set()
        bydev = sus.groupby(P["F"].device[sus.index]).start.apply(list).to_dict()
        for i, r in S[S.kind == "R"].iterrows():
            if any(-1.0 <= st - r.t_last <= 1.0 for st in bydev.get(r.dev, [])):
                lk.add(i)
        S["lockout"] = S.index.isin(lk)
    else:
        S["lockout"] = S["last"] == "TRIP"
    return S, op


def feeder_history(P):
    """The register's feeder as at 30 September 2026, and each section's feeder before its recorded transfer (the outage
    system's XFER record: the section was taken off its old feeder and picked up from the new one at the record's end)."""
    F, sec = P["F"], P["sec"]
    cur = dict(zip(sec.section_id, sec.feeder))
    hist = {r.sec: (r.feeder, r.end) for r in F[F.cause == "XFER"].itertuples()}
    return cur, hist


def maifi_files(P, route="golden"):
    sec = P["sec"]
    members = dict(zip(sec.section_id, sec.members)); dist = dict(zip(sec.section_id, sec.district))
    dm = sec.groupby("district").members.sum()
    cur, hist = feeder_history(P)
    S, op = scada_events(P, "oms" if route == "golden" or route == "full" else "final")
    on_feeder = sec.groupby("feeder").section_id.apply(list).to_dict()
    out = {(d, q): 0.0 for d in dm.index for q in (1, 2, 3, 4)}
    if route == "norepair":
        tr = op[op.operation == "TRIP"]
        q = asks.quarter(pd.DatetimeIndex(D0 + pd.to_timedelta(tr.t_utc.values * 60, "s")))
        for k, i, qq in zip(tr.kind.values, tr.id.values, q):
            for s in (on_feeder.get(i, []) if k == "B" else [i]):
                out[(dist[s], qq)] += members[s]
        return {k: v / dm[k[0]] for k, v in out.items()}
    S = S[~S.lockout]
    qs = asks.quarter(asks.local_ts(S.t.values))
    if route == "cracker":
        for k, i, qq in zip(S.kind.values, S.id.values, qs):
            for s in (on_feeder.get(i, []) if k == "B" else [i]):
                out[(dist[s], qq)] += members[s]
        return {k: v / dm[k[0]] for k, v in out.items()}
    if route == "golden":
        def feeder_of(s, t):
            h = hist.get(s)
            return h[0] if (h and t < h[1]) else cur[s]
        by_feeder_time = {}
        allsec = list(sec.section_id)
    per = {}
    for k, i, t in zip(S.kind.values, S.id.values, S.t.values):
        if k == "B":
            if route == "golden":
                secs = [s for s in allsec if feeder_of(s, t) == i]
            else:
                secs = on_feeder.get(i, [])
        else:
            secs = [i]
        for s in secs:
            per.setdefault(s, []).append(t)
    for s, ts in per.items():
        start = -1e9
        for t in sorted(ts):
            if t - start > 5.0:
                start = t
                out[(dist[s], asks.quarter(asks.local_ts([t]))[0])] += members[s]
    return {k: v / dm[k[0]] for k, v in out.items()}


# ------------------------------------------------------------------ Ask B from the files
def crew_frame(P, route="golden"):
    """Restoration callout rows with their times. Every field at face value: order_type OUTAGE is restoration work, the
    entry is the latest for its employee, order and start, and a row's date is its work order's outage date (the foreman
    enters the week's time each Monday, so entered_at is the entry, not the work). The cracker and the full includer date
    each row by its entry; the no-repair reader keeps every entry."""
    c = pd.read_csv(os.path.join(P["T"], "crew_time_overtime_fy2026.csv"), dtype=str)
    if route != "norepair":
        c = c[c.status == "APPROVED"]
        c = c.sort_values("entered_at").groupby(["employee_id", "work_order", "start_time"], as_index=False).last()
    c = c[(c.pay_code == "CALLOUT") & (c.order_type == "OUTAGE")]
    hm = lambda s: s.str[:2].astype(int) * 60 + s.str[3:5].astype(int)
    st, en = hm(c.start_time), hm(c.end_time)
    if route == "golden":
        ostart = c.work_order.map(dict(zip(P["F"].wo, P["F"].start)))
        base = (ostart // 1440) * 1440 + st
        s = np.where(base < ostart, base + 1440, base)
    else:
        s = (mins(c.entered_at) // 1440) * 1440 + st
        s = s.values
    e = s + ((en - st) % 1440).values
    return pd.DataFrame({"emp": c.employee_id.values, "cls": c.job_class.values, "s": s, "e": e, "wo_type": c.order_type.values})


def callouts_files(P, route="golden"):
    R = crew_frame(P, route)
    return asks.callout_figures(R, route)


QN = {1: "Fiscal Q1 (Oct-Dec 2025)", 2: "Fiscal Q2 (Jan-Mar 2026)", 3: "Fiscal Q3 (Apr-Jun 2026)", 4: "Fiscal Q4 (Jul-Sep 2026)"}
MONTHS = ["Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026", "Jun 2026",
          "Jul 2026", "Aug 2026", "Sep 2026"]


def all_figures(T):
    P = load(T)
    m = main_figures(P)
    a = maifi_files(P, "golden")
    h, p = callouts_files(P, "golden")
    return P, m, a, h, p
