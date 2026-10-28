"""task270 independent verifier: recomputes every graded figure from the shipped bundle alone (target/), by its own
route (pandas, interval arithmetic, its own replay), and compares with figures.json and submission.md.

    python3 verify.py <task_dir>"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree

DISTRICTS = ["Calderstow", "Tollesham", "Wrenfold", "Hollinbury", "Pelmarsh", "Altmoor", "Skirwold"]
RURAL = ["61", "62", "63", "64", "71", "72", "73", "74"]
EPOCH = pd.Timestamp("2026-01-01 00:00:00")
N_MIN = 525600


def secs(series):
    return ((pd.to_datetime(series) - EPOCH) / pd.Timedelta(seconds=1)).astype(np.int64).to_numpy()


def london_to_utc_min(series):
    """Local clock minutes to UTC minutes: summer time from 01:00 UTC on 29 March to 01:00 UTC on 25 October 2026."""
    t = ((pd.to_datetime(series) - EPOCH) / pd.Timedelta(minutes=1)).astype(np.int64).to_numpy()
    a = (pd.Timestamp("2026-03-29 02:00") - EPOCH) // pd.Timedelta(minutes=1)
    b = (pd.Timestamp("2026-10-25 02:00") - EPOCH) // pd.Timedelta(minutes=1)
    return np.where((t >= a) & (t < b), t - 60, t)


def _hm(x):
    h, m = divmod(int(x), 60)
    return "{} hour{} {} minute{}".format(h, "" if h == 1 else "s", m, "" if m == 1 else "s")


def main(task):
    tg = os.path.join(task, "target")
    J = lambda f: os.path.join(tg, f)
    F = json.load(open(os.path.join(task, "generator", "figures.json"), encoding="utf-8"))
    fails = []

    def check(label, ok, detail=""):
        print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % detail) if detail else ""))
        if not ok:
            fails.append(label)

    # ----------------------------------------------------------------------------------------- network and homes
    nodes = pd.read_csv(J("routing_network_nodes.csv"))
    links = pd.read_csv(J("routing_network_links.csv"))
    ix = pd.Series(np.arange(len(nodes)), index=nodes.node_id)
    a = ix[links.from_node].to_numpy(); b = ix[links.to_node].to_numpy()
    both = links.one_way.to_numpy() == "N"
    rows = np.r_[a, b[both]]; cols = np.r_[b, a[both]]; w = np.r_[links.drive_time_s, links.drive_time_s[both]]
    G = coo_matrix((w, (rows, cols)), shape=(len(nodes), len(nodes))).tocsr()
    D = dijkstra(G, directed=True)
    tree = cKDTree(nodes[["easting", "northing"]].to_numpy(float))
    addr = pd.read_csv(J("address_register_extract.csv"), dtype={"uprn": str})
    oa = pd.read_excel(J("output_area_lookup.xlsx"), sheet_name="OA21 to LAD")
    addr = addr.merge(oa.rename(columns={"OA21CD": "output_area"}), on="output_area", how="left")
    homes = addr[addr.class_code.str.startswith("RD")].copy()
    homes["node"] = tree.query(homes[["easting", "northing"]].to_numpy(float))[1]
    hn = homes.groupby(["node", "LAD22NM"]).size().unstack(fill_value=0).reindex(columns=DISTRICTS, fill_value=0)
    dnodes = hn.index.to_numpy()
    H = hn.to_numpy(float)
    tot = H.sum(0)
    # ----------------------------------------------------------------------------------------- fleet
    st = pd.read_excel(J("fleet_and_stations_2026.xlsx"), sheet_name="Stations", dtype={"Station code": str})
    ap = pd.read_excel(J("fleet_and_stations_2026.xlsx"), sheet_name="Appliances", dtype={"Station code": str})
    st["node"] = tree.query(st[["Easting", "Northing"]].to_numpy(float))[1]
    ap = ap.merge(st[["Station code", "node"]], on="Station code")
    calls = ap["Call sign"].tolist()
    home = ap.node.to_numpy()
    turn = np.where(ap["Crewed by"].to_numpy() == "Wholetime", 120.0, 300.0)
    reach = {t: (D[:, dnodes] + t) <= 600.0 for t in (120.0, 300.0)}
    # ----------------------------------------------------------------------------------------- the log
    log = pd.read_csv(J("mobilising_resource_log_2026.csv"), dtype={"status_code": str, "call_sign": str},
                      keep_default_na=False)
    log["t"] = secs(log.time_utc)
    grid = pd.DataFrame({"t": np.arange(N_MIN, dtype=np.int64) * 60})
    free = np.zeros((N_MIN, len(calls)), bool)
    pos = np.zeros((N_MIN, len(calls)), np.int64)
    code_at = {}
    for e, c in enumerate(calls):
        g = log[log.call_sign == c]
        s = g[g.event == "Status"][["t", "status_code"]].sort_values("t", kind="stable")
        m = pd.merge_asof(grid, s, on="t", direction="backward")
        code_at[c] = m.status_code.fillna("").to_numpy()
        free[:, e] = code_at[c] == "1"
        v = g[g.event != "Status"][["t", "event", "easting", "northing"]].copy()
        v["out"] = (v.event != "Arrived base").astype(int)
        v["node"] = tree.query(v[["easting", "northing"]].astype(float).to_numpy())[1] if len(v) else []
        v = v.sort_values("t", kind="stable")
        m = pd.merge_asof(grid, v[["t", "out", "node"]], on="t", direction="backward")
        out = m.out.fillna(0).to_numpy() == 1
        pos[:, e] = np.where(out, m.node.fillna(-1).to_numpy(), home[e]).astype(np.int64)
    # cover, minute by minute, in blocks
    S = np.where(free, pos, -1)
    keys, inv = np.unique(S, axis=0, return_inverse=True)
    inv = inv.ravel()
    weight = np.bincount(inv, minlength=len(keys))
    acc = np.zeros(len(DISTRICTS))
    for k0 in range(0, len(keys), 2500):
        blk = keys[k0:k0 + 2500]
        cov = np.zeros((len(blk), len(dnodes)), bool)
        for e in range(len(calls)):
            p = blk[:, e]
            ok = p >= 0
            cov[ok] |= reach[turn[e]][p[ok]]
        acc += weight[k0:k0 + 2500] @ (cov.astype(float) @ H)
    cover = acc / N_MIN / tot * 100.0
    named = [d for d, v in zip(DISTRICTS, cover) if v < 75.0]
    check("the named districts", named == F["call"], ", ".join(named))
    for d, v in zip(DISTRICTS, cover):
        check("%s cover %s per cent" % (d, F["cover"][d]), str(int(np.floor(v + 0.5))) == F["cover"][d], "%.3f" % v)
    # ----------------------------------------------------------------------------------------- ask A
    bk = pd.read_csv(J("oncall_availability_bookings_2026.csv"), dtype=str)
    bk["f"] = london_to_utc_min(bk.available_from); bk["to"] = london_to_utc_min(bk.available_to)
    bk["en"] = pd.to_datetime(bk.entered)
    crew = pd.read_excel(J("oncall_crew_register_2026.xlsx"), sheet_name="Crew", dtype=str)
    rc = pd.read_excel(J("oncall_crew_register_2026.xlsx"), sheet_name="Role changes", dtype=str)
    promo = {r["Staff number"]: (pd.Timestamp(r["Effective from"]) - EPOCH) // pd.Timedelta(minutes=1)
             for _, r in rc.iterrows()}
    oic_now = set(crew[crew.Role.isin(["Crew Commander", "Watch Commander"])]["Staff number"])
    for sc in RURAL:
        b = bk[bk.station_code == sc]
        n = np.zeros(N_MIN + 1, np.int64)
        o = np.zeros(N_MIN + 1, np.int64)
        for sid, g in b.groupby("staff_number"):
            # newest entry first: a booking stands where no later-entered booking of the same firefighter overlaps it
            g = g.sort_values("en", ascending=False, kind="stable")
            kept = []
            for _, r in g.iterrows():
                if all(r.to <= k[0] or r.f >= k[1] for k in kept):
                    kept.append((r.f, r.to))
            for f0, t0 in kept:
                f0, t0 = max(0, f0), min(N_MIN, t0)
                if t0 <= f0:
                    continue
                n[f0] += 1; n[t0] -= 1
                if sid in promo:
                    p0 = max(f0, promo[sid])
                    if p0 < t0:
                        o[p0] += 1; o[t0] -= 1
                elif sid in oic_now:
                    o[f0] += 1; o[t0] -= 1
        n = np.cumsum(n)[:N_MIN]; o = np.cumsum(o)[:N_MIN]
        off = code_at[sc + "P1"] == "8"
        x = int((off & (n >= 4)).sum()); y = int((off & (n >= 4) & (o == 0)).sum())
        want = F["ask_a"][sc]
        check("ask A %s %s; %s" % (sc, want["off_run_4plus"], want["no_oic"]),
              want["off_run_4plus"] == _hm(x) and want["no_oic"] == _hm(y), "%d / %d minutes" % (x, y))
    # ----------------------------------------------------------------------------------------- ask C
    inc = pd.read_csv(J("incident_records_2022_2026.csv"), dtype={"uprn": str}, keep_default_na=False)
    com = addr[addr.class_code.str.startswith("C")][["uprn", "LAD22NM"]]
    fa = inc[inc.classification.isin(["A01", "FAA"])].merge(com, on="uprn", how="inner")
    fa["call"] = pd.to_datetime(fa.call_time); fa["closed"] = pd.to_datetime(fa.closed_time)
    fa = fa.sort_values(["uprn", "call"], kind="stable")
    prev_closed = fa.groupby("uprn")["closed"].transform(lambda s: s.cummax().shift(1))
    fa["new"] = prev_closed.isna() | (fa.call > prev_closed)
    act = fa[fa.new].groupby("LAD22NM").size().reindex(DISTRICTS, fill_value=0)
    prem = com.groupby("LAD22NM").size().reindex(DISTRICTS, fill_value=0)
    for d in DISTRICTS:
        rate = act[d] / prem[d] * 100.0
        want = F["ask_c"][d]
        check("ask C %s %s actuations, %s per 100" % (d, want["actuations"], want["per_100"]),
              str(int(act[d])) == want["actuations"] and "%.1f" % (np.floor(rate * 10 + 0.5) / 10) == want["per_100"],
              "%d, %.4f" % (act[d], rate))
    # ----------------------------------------------------------------------------------------- the write-up
    sub = open(os.path.join(task, "submission.md"), encoding="utf-8").read()
    check("the write-up names the call", all(d in sub.split("## 2.")[0] for d in F["call"]), "")
    for d in DISTRICTS:
        check("the write-up states %s's cover" % d, re.search(r"%s: %s per cent" % (d, F["cover"][d]), sub) is not None)
    # ----------------------------------------------------------------------------------------- the documents, read back
    from pypdf import PdfReader

    def pdf_text(f):
        return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(J(f)).pages))
    std = pdf_text("emergency_cover_standard_2027.pdf")
    check("the standard reads back (control: its title)", "Emergency cover standard" in std, "%d chars" % len(std))
    for phrase in ("classification codes beginning RD", "free at the start of that minute could reach it within ten "
                   "minutes", "Turnout is two minutes for an engine crewed by wholetime firefighters and five minutes",
                   "Available (status code 1)", "the 525,600 minutes from 00:00 UTC on 1 January 2026",
                   "below 75 per cent is named in the plan"):
        check("the standard files: %s" % phrase, phrase in std)
    pol = pdf_text("oncall_duty_system_policy.pdf")
    check("the policy reads back (control: its title)", "On-call duty system" in pol, "%d chars" % len(pol))
    check("the policy files the crewing rule", "four or more of its station's firefighters are booked available" in pol
          and "an LGV driver and two breathing apparatus wearers" in pol)
    cab = pdf_text("cabinet_report_crmp_2027_2031.pdf")
    check("the cabinet report reads back (control: its title)", "Community Risk Management Plan 2027 to 2031" in cab,
          "%d chars" % len(cab))
    check("the cabinet report defines non-domestic premises and the false alarms counted",
          "classification codes beginning C" in cab and "A01 up to 31 March 2024 and FAA from 1 April 2024" in cab)
    print("%d failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
