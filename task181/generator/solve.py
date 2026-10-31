"""The golden, computed from target/ alone: the Centre's procedures and infections, each consultant against the
upper control limit, the trace from every operation's instrument sets to the steriliser load that last reprocessed
them, and the asks. Every route the checks price is a parameter here."""
import bisect
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402

F = {"ops": "theatre_operations_2022_2027.csv", "ssi": "ssi_surveillance_2022_2027.csv",
     "scans": "instrument_tracking_scans_2027.csv", "cycles": "steriliser_cycles_2027.csv",
     "equip": "cssd_equipment_log_2026_2027.xlsx", "register": "cssd_set_register_2027.xlsx"}
DEPTH_RANK = {"Superficial incisional": 1, "Deep incisional": 2, "Organ/space": 3}
CODE_MAP = {"GS-41": "GS-14"}


def load(target=C.TARGET):
    p = lambda k: os.path.join(target, F[k])
    ops = pd.read_csv(p("ops"), dtype=str)
    ssi = pd.read_csv(p("ssi"), dtype=str)
    scans = pd.read_csv(p("scans"), dtype=str)
    cyc = pd.read_csv(p("cycles"), dtype=str)
    return dict(ops=ops, ssi=ssi, scans=scans, cycles=cyc, target=target)


def repair_time(target=C.TARGET):
    """The steriliser 3 repair's return to service, from the CSSD equipment log (local time)."""
    ws = load_workbook(os.path.join(target, F["equip"]), read_only=True)["Log"]
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "S3" and str(row[3]).startswith("Vacuum pump replaced"):
            return dt.datetime.strptime(str(row[4]), "%Y-%m-%d %H:%M")
    raise ValueError("no S3 repair in the log")


def procedures(D, merge_addons=True, map_codes=True, seq1=True, drop_returns=True):
    o = D["ops"]
    o = o[(o["status"] == "Completed") & (o["surveillance_category"].isin(C.PROCS))].copy()
    if drop_returns:
        o = o[o["return_to_theatre"] != "Y"]
    if seq1:
        o = o[o["procedure_seq"] == "1"]
    o["knife"] = pd.to_datetime(o["knife_to_skin"])
    o["close"] = pd.to_datetime(o["wound_closure"])
    o["anaes"] = pd.to_datetime(o["anaesthetic_start"])
    if merge_addons:
        # one operation, one procedure: an add-on booked on its own carries the same patient, theatre and incision
        o = o.sort_values(["ur_number", "theatre", "knife", "booking_no"])
        o = o.drop_duplicates(["ur_number", "theatre", "knife"], keep="first")
    o["consultant"] = o["responsible_consultant"].map(lambda c: CODE_MAP.get(c, c) if map_codes else c)
    o["minutes"] = (o["close"] - o["knife"]).dt.total_seconds() / 60
    o["idx"] = [C.risk_index(int(a), {"Clean": 1, "Clean-contaminated": 2, "Contaminated": 3, "Dirty": 4}[w], m, k)
                for a, w, m, k in zip(o["asa_class"], o["wound_class"], o["minutes"], o["surveillance_category"])]
    o["expected"] = [C.expected_rate(k, i) for k, i in zip(o["surveillance_category"], o["idx"])]
    o["day"] = o["knife"].dt.date
    return o.reset_index(drop=True)


def infections(D, procs, link="booking", attribute="procedure", window=True):
    """Confirmed infections, latest record version, each linked to its procedure and counted once at its deepest."""
    s = D["ssi"]
    s = s.copy()
    s["record_version"] = s["record_version"].astype(int)
    s = s.sort_values(["infection_id", "record_version"]).drop_duplicates("infection_id", keep="last")
    s = s[s["status"] == "Confirmed"]
    pk = procs.set_index("booking_no")
    by_ur = {}
    for i, r in procs.iterrows():
        by_ur.setdefault((r["ur_number"], r["surveillance_category"]), []).append((r["day"], i))
    rows = []
    for _, r in s.iterrows():
        i = None
        if link == "booking" and isinstance(r["booking_no"], str) and r["booking_no"] in pk.index:
            i = procs.index[procs["booking_no"] == r["booking_no"]][0] if False else int(np.where(
                procs["booking_no"].values == r["booking_no"])[0][0])
        else:
            od = dt.date.fromisoformat(r["operation_date"])
            cands = by_ur.get((r["ur_number"], r["surveillance_category"]), [])
            near = [(d, k) for d, k in cands if 0 <= (d - od).days <= 3] if link != "exact" else \
                [(d, k) for d, k in cands if d == od]
            if near:
                i = min(near)[1]
        if i is None:
            continue
        pr = procs.loc[i]
        days = (dt.date.fromisoformat(r["onset_date"]) - pr["day"]).days
        if window and not (0 <= days <= (90 if pr["implant"] == "Y" else 30)):
            continue
        rows.append((i, DEPTH_RANK[r["depth"]], r["consultant_code"]))
    best = {}
    for i, d, c in rows:
        best[i] = max(best.get(i, 0), d)
    return best


def trace(D, procs, repair, rule="any", aborted=False):
    """Each window operation's exposure: an item opened in theatre whose last steriliser load before the opening
    was a steriliser 3 load after the repair. rule: any item, tray (rigid containers) only, or s3_all (any S3 load)."""
    cyc = D["cycles"]
    cyc = cyc[(cyc["cycle_type"] == "Load") & ((cyc["result"] == "Pass") | aborted)]
    last = {}
    rep_utc = C.to_utc(repair)
    for st, start, items in zip(cyc["steriliser"], cyc["start_utc"], cyc["items"]):
        t = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        for b in str(items).split(";"):
            last.setdefault(b, []).append((t, st))
    for b in last:
        last[b].sort()
    keys = {b: [t for t, _ in v] for b, v in last.items()}
    rigid = None
    if rule == "tray":
        ws = load_workbook(os.path.join(D["target"], F["register"]), read_only=True)["Register"]
        rigid = {r[0] for r in ws.iter_rows(values_only=True) if r and r[3] == "Rigid container"}
    sc = D["scans"]
    sc = sc[sc["station"].str.startswith("THEATRE")]
    # the operation the scan belongs to: same patient and theatre, opened between the anaesthetic start less an hour
    # and wound closure (local)
    win = procs[(procs["day"] >= C.WIN0) & (procs["day"] <= C.WIN1)]
    ix = {}
    for i, r in win.iterrows():
        ix.setdefault((r["ur_number"], r["theatre"]), []).append((r["anaes"], r["close"], i))
    exposed = set()
    linked = set()
    for t, b, st, ur in zip(sc["scan_utc"], sc["barcode"], sc["station"], sc["ur_number"]):
        u = dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
        loc = C.to_local(u)
        th = st.replace("THEATRE ", "")
        for a, c, i in ix.get((ur, th), []):
            if a - dt.timedelta(minutes=60) <= loc <= c:
                linked.add(i)
                if b in keys:
                    k = bisect.bisect_left(keys[b], u) - 1
                    if k >= 0:
                        lt, lst = last[b][k]
                        hit = lst == "S3" and (lt >= rep_utc or rule == "s3_all")
                        if rule == "tray" and b not in rigid:
                            hit = False
                        if hit:
                            exposed.add(i)
    return exposed, linked


def consultant_table(procs, inf, exposed=None, method="naive", rr=None):
    win = procs[(procs["day"] >= C.WIN0) & (procs["day"] <= C.WIN1)]
    out = {}
    for c in C.CONSULTANTS:
        w = win[win["consultant"] == c]
        if method == "exclude":
            w = w[~w.index.isin(exposed)]
        e = float(w["expected"].sum())
        if method == "stratified":
            ex = w.index.isin(exposed)
            e = float(w["expected"][~ex].sum() + w["expected"][ex].sum() * rr)
        o = int(sum(i in inf for i in w.index))
        out[c] = dict(n=int(len(w)), expected=e, observed=o, limit=C.poisson_upper(e))
    return out


def referred(table):
    return sorted(c for c, v in table.items() if v["observed"] > v["limit"])


def exposure_rr(procs, inf, exposed):
    win = procs[(procs["day"] >= C.WIN0) & (procs["day"] <= C.WIN1)]
    ex = win.index.isin(exposed)
    o1, e1 = sum(i in inf for i in win.index[ex]), win["expected"][ex].sum()
    o0, e0 = sum(i in inf for i in win.index[~ex]), win["expected"][~ex].sum()
    return (o1 / e1) / (o0 / e0), int(ex.sum()), o1, e1, o0, e0


def ask_procedures(procs, years=(2022, 2023, 2024)):
    out = {}
    for c in C.CONSULTANTS:
        for y in years:
            out["%s %d" % (c, y)] = int(((procs["consultant"] == c) & (procs["knife"].dt.year == y)).sum())
    return out


def ask_infections(procs, inf, years=(2022, 2023, 2024)):
    out = {}
    yr = procs["knife"].dt.year
    for c in C.CONSULTANTS:
        for y in years:
            idx = procs.index[(procs["consultant"] == c) & (yr == y)]
            out["%s %d" % (c, y)] = int(sum(i in inf for i in idx))
    return out


def solve(target=C.TARGET):
    D = load(target)
    rep = repair_time(target)
    P = procedures(D)
    inf = infections(D, P)
    exposed, linked = trace(D, P, rep)
    naive = consultant_table(P, inf)
    gold = consultant_table(P, inf, exposed, "exclude")
    rr = exposure_rr(P, inf, exposed)
    strat = consultant_table(P, inf, exposed, "stratified", rr[0])
    return dict(D=D, P=P, inf=inf, exposed=exposed, linked=linked, repair=rep, naive=naive, gold=gold, strat=strat,
                rr=rr, ask_a=ask_procedures(P), ask_b=ask_infections(P, inf))


if __name__ == "__main__":
    S = solve()
    print("repair", S["repair"], "window procedures", int(((S["P"]["day"] >= C.WIN0) & (S["P"]["day"] <= C.WIN1)).sum()),
          "linked", len(S["linked"]), "exposed", len(S["exposed"]), "rr %.2f" % S["rr"][0])
    print("naive", referred(S["naive"]), "gold", referred(S["gold"]), "strat", referred(S["strat"]))
    for c in C.CONSULTANTS:
        n, g = S["naive"][c], S["gold"][c]
        print(c, "naive %d/%d (E %.1f)" % (n["observed"], n["limit"], n["expected"]),
              "gold %d/%d (E %.1f, n %d)" % (g["observed"], g["limit"], g["expected"], g["n"]))
