"""Independent verifier for task263: reads only the bundle (target/), on its own code path (pandas, pypdf, a normal-
equations solve per entry point and analyte), and recomputes the call, every grant, the walk, the rungs below the
golden and the ask; compares them with generator/figures.json. Exit 0 when everything agrees.

    python3 task263/generator/verify.py task263/target"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
FUND, RATE, CAP = 36_000_000, 2_400_000, 6_000_000


def plan(target):
    pdf = [f for f in os.listdir(target) if f.startswith("iup_2027") and f.endswith(".pdf")][0]
    text = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, pdf)).pages)
    rows = re.findall(r"(?m)^\s*(\d{1,2})\s*\n(\d{7})\s*\n(.+?)\s*\n(\w+)\s*\n\s*([\d,]+)\s*\n\s*(\d+)\s*$", text)
    out = [dict(rank=int(a), pws=b, name=c.strip(), county=d) for a, b, c, d, e, f in rows]
    assert [p["rank"] for p in out] == list(range(1, 21)), [p["rank"] for p in out]
    return out


def inventory(target):
    """The source facility inventory's Facilities sheet, as this verifier reads it."""
    return pd.read_excel(os.path.join(target, "source_facility_inventory_2026.xlsx"), sheet_name="Facilities",
                         dtype={"pws_id": str, "facility_id": str})


def wells_in(text, active):
    t = str(text).strip() if isinstance(text, str) else ""
    if not t:
        return None
    if re.match(r"(?i)^(all|both|plant)\b", t):
        return sorted(active)
    return sorted({int(n) for n in re.findall(r"\d+", t)})


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    P = plan(target)
    ids = {p["pws"] for p in P}
    inv = inventory(target)
    act = inv[(inv.status == "Active") & (inv.facility_type == "Well") & inv.pws_id.isin(ids)]
    cap = {}
    for _, f in act.iterrows():
        cap.setdefault((f.pws_id, f.entry_point), {})[int(f.facility_name.split()[-1])] = int(f.rated_capacity_gpm)
    res = pd.read_csv(os.path.join(target, "pfas_entry_point_results_2024-2026.csv"), dtype={"pws_id": str})
    res = res[res.pws_id.isin(ids) & res.sample_type.isin(["RT", "CO"]) & res.analyte.isin(["PFOA", "PFOS"])]
    res = res[res.collected_date.str[:4].isin(["2024", "2025"])]
    res = res[res.report_revision == res.groupby(["state_sample_no", "analyte"]).report_revision.transform("max")]
    res["v"] = np.where(res.result_sign == "<", res.reporting_limit / 2.0, res.result)
    wide = res.pivot_table(index=["state_sample_no", "pws_id", "sample_point"], columns="analyte", values="v").reset_index()
    rec = pd.read_csv(os.path.join(target, "pfas_field_collection_records_2024-2026.csv"), dtype={"pws_id": str})
    wide = wide.merge(rec[["state_sample_no", "sources_in_service"]], on="state_sample_no")
    levels = {}
    for (pws, ep), g in wide.groupby(["pws_id", "sample_point"]):
        w = cap[(pws, ep)]
        nos = sorted(w)
        X, Y = [], []
        for _, r in g.iterrows():
            on = wells_in(r.sources_in_service, nos)
            if on is None:
                continue
            tot = sum(w[n] for n in on)
            X.append([w[n] / tot if n in on else 0.0 for n in nos])
            Y.append([r.PFOA, r.PFOS])
        X, Y = np.array(X), np.array(Y)
        B = np.linalg.solve(X.T @ X, X.T @ Y)        # normal equations, both analytes at once
        for i, n in enumerate(nos):
            levels[(pws, ep, n)] = B[i]
    grant = {}
    for p in P:
        gpm = sum(cap[(pws, ep)][n] for (pws, ep, n), b in levels.items() if pws == p["pws"] and b.max() > 4.0)
        grant[p["name"]] = min(CAP, round(RATE * gpm * 1440 / 1e6))
    left, funded, stop = FUND, [], None
    for p in P:
        if grant[p["name"]] > left:
            stop = p["name"]
            break
        left -= grant[p["name"]]
        funded.append(p["name"])
    ok = True

    def same(label, a, b):
        nonlocal ok
        flag = a == b
        ok &= flag
        print("%-5s %s" % ("OK" if flag else "DIFF", label), "" if flag else (a, b))

    same("systems reached", len(funded), F["call"]["systems_reached"])
    same("first system not reached", stop, F["call"]["first_not_reached"])
    same("set-aside left", left, F["call"]["left"])
    same("every grant", grant, F["grants"])
    same("funded systems", funded, F["funded"])
    for key, v in F["levels"].items():
        m = re.match(r"(.+) (EP\d+) Well (\d+)$", key)
        pws = next(p["pws"] for p in P if p["name"] == m.group(1))
        b = levels[(pws, m.group(2), int(m.group(3)))]
        if [round(float(b[0]), 1), round(float(b[1]), 1)] != v:
            same("well level %s" % key, [round(float(b[0]), 1), round(float(b[1]), 1)], v)
    print("OK    every well's own PFOA and PFOS to one decimal" if ok else "")

    # the default path: each well given the average of its samples
    grant0 = {}
    for p in P:
        gpm = 0
        sub = wide[wide.pws_id == p["pws"]]
        for (pws, ep), w in cap.items():
            if pws != p["pws"]:
                continue
            for n in w:
                vals = [(r.PFOA, r.PFOS) for _, r in sub[sub.sample_point == ep].iterrows()
                        if (wells_in(r.sources_in_service, sorted(w)) or []).count(n)]
                if vals and max(np.mean([v[0] for v in vals]), np.mean([v[1] for v in vals])) > 4.0:
                    gpm += w[n]
        grant0[p["name"]] = min(CAP, round(RATE * gpm * 1440 / 1e6))
    left0, n0 = FUND, 0
    for p in P:
        if grant0[p["name"]] > left0:
            break
        left0 -= grant0[p["name"]]
        n0 += 1
    same("default path (average of the samples a well ran in) reaches 7", n0, 7)

    # The ask: 2025 water pumped by the listed systems' wells, by county and quarter. Each register meter once a
    # month; then, by the pump physics on this verifier's own reading of the rows, a wellhouse meter whose line goes
    # beyond its well's rated capacity for 24 hours of each day in service, which no shared meter explains, is taken
    # net of the one other well at its entry point that brings it within its pump in every month.
    mor = pd.read_csv(os.path.join(target, "monthly_operating_reports_2025.csv"), dtype={"pws_id": str, "facility_id": str})
    met = pd.read_csv(os.path.join(target, "source_meter_register_2026.csv"), dtype={"pws_id": str})
    wells = inv[inv.facility_type == "Well"].set_index("facility_id")
    county = {p["pws"]: p["county"] for p in P}
    mor = mor[mor.pws_id.isin(ids) & mor.facility_id.isin(wells.index)].copy()
    group = {}
    for _, m in met.iterrows():
        fs = str(m.facility_ids).split(";")
        if len(fs) > 1:
            for f in fs:
                group[f] = "+".join(sorted(fs))
    mor["meter_group"] = [group.get(f, f) for f in mor.facility_id]
    mor = mor.drop_duplicates(["meter_group", "report_month"]).copy()
    mor["gpm"] = mor.facility_id.map(wells.rated_capacity_gpm).astype(int)
    mor["ep"] = mor.facility_id.map(wells.entry_point)
    mor["most"] = mor.gpm * 1440 * mor.days_in_service
    vol = mor.set_index(["facility_id", "report_month"]).volume_gal
    net = mor.volume_gal.astype(float).copy()
    for f, g in mor.groupby("facility_id"):
        if f in group or not (g.volume_gal > g.most).any():
            continue
        peers = mor[(mor.pws_id == g.pws_id.iloc[0]) & (mor.ep == g.ep.iloc[0]) & (mor.facility_id != f)]
        fit = [o for o in peers.facility_id.unique()
               if all(r.volume_gal - vol.get((o, r.report_month), 0) <= r.most for _, r in g.iterrows())]
        one = len(fit) == 1
        ok &= one
        print("%-5s wellhouse meter on facility %s carries facility %s" % ("OK" if one else "DIFF", f, fit))
        for i, r in g.iterrows():
            net.at[i] = r.volume_gal - vol.get((fit[0], r.report_month), 0)
    mor["net"] = net
    mor["q"] = "Q" + ((mor.report_month.str[5:].astype(int) - 1) // 3 + 1).astype(str)
    a = (mor.groupby([mor.pws_id.map(county), "q"]).net.sum() / 1e6).round(1)
    got = {}
    for (c, q), v in a.items():
        got.setdefault(c, {})[q] = float(v)
    same("Ask: water pumped by county and quarter", got, {c: {q: float(v) for q, v in d.items()}
                                                         for c, d in F["ask_a"].items()})
    print("verify: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
