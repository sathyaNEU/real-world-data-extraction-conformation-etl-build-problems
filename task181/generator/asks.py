"""The three summer 2026 measures computed from the pack in target/, with the wrong paths the ask sheet names.

Ask 1, en-route ATFM delay per flight: the flights that entered the sector in the local summer are the
denominator; the numerator is each flown flight's ATFM delay (its most penalising regulation's slot delay) when that
regulation is an en-route regulation on the sector. A plan in the slot list that never reached the flight data
(re-filed or cancelled) carries no delay of a flight.

Ask 2, hours open alone: the configuration log (local time) against the configuration table in force at each moment,
revision 8 (operations manual, 26 March 2026) until the logged entry for revision 9 at 06:00 on 14 July 2026, revision
9 (the current table) after.

Ask 3, ACAS RA encounters: advisory reports in the local summer, two reports naming the same two aircraft in the same
sector within ten minutes being one encounter."""
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd
import pdfplumber

import models as M
import world as W


def season_utc(year):
    return tuple(int(x.timestamp()) for x in W.season(year))


def _ts(series):
    return M._sec(series)


# ----------------------------------------------------------------------------------------------- ask 1
def delay(target, rec=None):
    rec = rec or M.fdps(target)
    tv, _ = M.register(target)
    slots = pd.read_csv(os.path.join(target, "nm_slot_allocations_2026-05_2026-09.csv"), dtype={"ifplid": str})
    regs = pd.read_csv(os.path.join(target, "nm_regulations_2026-05_2026-09.csv"))
    reg_tv = regs.drop_duplicates("regulation_id").set_index("regulation_id")["traffic_volume"].to_dict()
    reg_kind = regs.drop_duplicates("regulation_id").set_index("regulation_id")["location_type"].to_dict()
    a, b = season_utc(2026)
    trav = pd.DataFrame({"ifplid": rec["ifplid"], "sec": rec["sec"], "t0": rec["t0"]})
    trav = trav[(trav["t0"] >= a - 86400 * 40) & (trav["t0"] < b + 86400 * 40)]
    insea = trav[(trav["t0"] >= a) & (trav["t0"] < b)]
    den = insea.groupby("sec")["ifplid"].nunique().to_dict()
    entry = {(r.ifplid, r.sec): r.t0 for r in trav.itertuples()}
    flown = set(rec["ifplid"])
    slots["flew"] = slots["ifplid"].isin(flown)
    slots["tv"] = slots["regulation_id"].map(reg_tv)
    slots["kind"] = slots["regulation_id"].map(reg_kind)
    slots["sec"] = slots["tv"].map(lambda x: W.SECTORS.index(tv[x]) if x in tv else -1)
    slots["eobt_s"] = _ts(slots["eobt"])

    def per_flight(df):
        top = df.sort_values(["ifplid", "slot_delay_min"], ascending=[True, False]).drop_duplicates("ifplid")
        return top

    def attribute(top, season_by="entry"):
        num = {s: 0.0 for s in range(8)}
        for r in top.itertuples():
            if r.kind != "En-route" or r.sec < 0:
                continue
            if season_by == "entry":
                t0 = entry.get((r.ifplid, r.sec))
                if t0 is None:
                    # a plan that never flew: the slot's own time
                    t0 = r.eobt_s + 1800
            elif season_by == "eobt_local":
                t0 = r.eobt_s
            else:
                t0 = r.eobt_s
            ok = (a <= t0 < b) if season_by != "utc" else (int(pd.Timestamp("2026-06-01", tz="UTC").timestamp()) <= t0 <
                                                            int(pd.Timestamp("2026-09-01", tz="UTC").timestamp()))
            if ok:
                num[r.sec] += r.slot_delay_min
        return {s: num[s] / den[s] for s in range(8)}

    out = {}
    out["golden"] = attribute(per_flight(slots[slots["flew"]]))
    out["every_plan"] = attribute(per_flight(slots))                       # the cracker: plans that never flew kept
    out["every_row"] = {s: v for s, v in attribute(slots.assign(ifplid=slots.index.astype(str))).items()}
    enr = slots[slots["flew"] & (slots["kind"] == "En-route")]
    out["en_route_rows_only"] = attribute(per_flight(enr))
    cs = slots.assign(d=slots["eobt"].str[:10]).sort_values(["callsign", "d", "slot_delay_min"],
                                                              ascending=[True, True, False])
    cs = cs.drop_duplicates(["callsign", "d", "regulation_id"])
    top_cs = cs.drop_duplicates(["callsign", "d"])
    out["callsign_day"] = attribute(top_cs)
    # the season read by each delayed flight's off-block time rather than its sector entry: every regulation runs in
    # the day, so the two readings take the same flights
    out["golden_by_eobt"] = attribute(per_flight(slots[slots["flew"]]), season_by="eobt_local")
    out["den"] = {s: int(den[s]) for s in range(8)}
    out["n_never_flew_rows"] = int((~slots["flew"]).sum())
    out["n_rows"] = int(len(slots))
    return out


# ----------------------------------------------------------------------------------------------- ask 2
def om_table(target):
    """Table 3.4-1 (revision 8) as the operations manual prints it."""
    _, names = M.register(target)
    rows = {}
    with pdfplumber.open(os.path.join(target, "HACC_OM_part3_ch4_sector_configuration.pdf")) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    for line in text.splitlines():
        m = re.match(r"^(C8|C7A|C7B|C6A|C6B|C5|N3|N2)\s+(\d)\s+(.+)$", line.strip())
        if m:
            groups = [[names[x.strip()] for x in g.split("+")] for g in m.group(3).split(", ")]
            assert len(groups) == int(m.group(2)), line
            rows[m.group(1)] = groups
    return rows


def current_table(target):
    df = pd.read_csv(os.path.join(target, "sector_configurations_current.csv"))
    out = {}
    for r in df.itertuples():
        out.setdefault(r.configuration, []).append(r.sectors.split("+"))
    return out


def hours_alone(target, which="golden", clock="local"):
    log = pd.read_csv(os.path.join(target, "sector_configuration_log_2026-05_2026-09.csv"), keep_default_na=False)
    rev8, rev9 = om_table(target), current_table(target)
    t = pd.to_datetime(log["log_time_local"]).dt.to_pydatetime()
    switch = None
    for k, rem in enumerate(log["remarks"]):
        if "revision 9" in rem:
            switch = t[k]
    start, end = dt.datetime(2026, 6, 1), dt.datetime(2026, 9, 1)
    if clock == "utc":
        start, end = start + dt.timedelta(hours=2), end + dt.timedelta(hours=2)
    out = {s: 0.0 for s in W.SECTORS}
    for k in range(len(t)):
        a2 = max(t[k], start)
        b2 = min(t[k + 1] if k + 1 < len(t) else dt.datetime(2026, 10, 1), end)
        if b2 <= a2:
            continue
        if which == "golden":
            tab = rev9 if t[k] >= switch else rev8
        elif which == "current":
            tab = rev9
        else:
            tab = rev8
        for g in tab[log["configuration"][k]]:
            if len(g) == 1:
                out[g[0]] += (b2 - a2).total_seconds() / 3600.0
    return out


# ----------------------------------------------------------------------------------------------- ask 3
def encounters(target, occ=None, how="golden"):
    occ = occ if occ is not None else M.occurrences(target)
    ra = occ[occ["occurrence_type"] == "ACAS RA"].copy()
    if how == "utc":
        a = int(pd.Timestamp("2026-06-01", tz="UTC").timestamp())
        b = int(pd.Timestamp("2026-09-01", tz="UTC").timestamp())
    else:
        a, b = season_utc(2026)
    ra = ra[(ra["ts"] >= a) & (ra["ts"] < b)].sort_values(["ts", "occurrence_no"])
    if how == "rows":
        return {s: int((ra["sec"] == k).sum()) for k, s in enumerate(W.SECTORS)}
    seen = []
    out = {s: 0 for s in W.SECTORS}
    for r in ra.itertuples():
        pair = frozenset((r.ac1_callsign, r.ac2_callsign))
        dup = any(p == pair and sec == r.sec and abs(ts - r.ts) <= 600 for p, sec, ts in seen)
        if not dup:
            out[W.SECTORS[r.sec]] += 1
        seen.append((pair, r.sec, r.ts))
    return out


def golden(target, rec=None, occ=None):
    d = delay(target, rec)
    return dict(delay=d, hours=hours_alone(target), hours_current=hours_alone(target, "current"),
                hours_rev8=hours_alone(target, "rev8"), hours_utc=hours_alone(target, clock="utc"),
                enc=encounters(target, occ), enc_rows=encounters(target, occ, "rows"),
                enc_utc=encounters(target, occ, "utc"))
