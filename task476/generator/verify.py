"""Independent verifier: reads only target/ and golden/ on its own code path (pandas, sqlite3, pdfplumber tables)
and recomputes every graded figure: each 2021 live tree's fate, each stand's share and the marking list, each
stand's 2026 live basal area and net volume per acre; then compares them with the golden files and figures.json."""
import json
import math
import os
import re
import sqlite3
import sys

import numpy as np
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))


def _half_up(v, unit):
    return math.floor(v / unit + 0.5) * unit


def recompute(target):
    con = sqlite3.connect(os.path.join(target, "inventory", "cfi_database.sqlite"))
    tree = pd.read_sql("SELECT * FROM tree", con)
    m21 = pd.read_sql("SELECT * FROM tree_meas WHERE cycle_yr = 2021 AND status = 'L'", con)
    con.close()
    t21 = m21.merge(tree, on="tag", how="left")
    t26 = pd.read_csv(os.path.join(target, "inventory", "trf_cfi_remeasurement_2026.csv"), dtype=str)
    for c in ("plot_id", "tag", "species_fia", "cond_id"):
        t26[c] = t26[c].astype(int)
    for c in ("dbh_in", "azimuth_deg", "dist_ft", "merch_ht_ft", "cull_pct"):
        t26[c] = pd.to_numeric(t26[c], errors="coerce")
    rev = pd.read_csv(os.path.join(target, "inventory", "trf_height_revisit_2026-09.csv"), dtype={"plot_id": int, "tag": int})
    reg = pd.read_excel(os.path.join(target, "inventory", "plot_register.xlsx"), sheet_name="Plots")
    spp = pd.read_csv(os.path.join(target, "inventory", "species_codes.csv"))
    fia2alpha = dict(zip(spp.fia_code, spp.company_code))
    hard = set(spp.loc[spp.group == "hardwood", "fia_code"])
    reg = reg.set_index("Plot")
    st1 = reg["Stand"].to_dict()
    st2 = reg["Cond 2 stand"].where(reg["Cond 2 stand"].notna(), None).to_dict()
    area = {}
    for p, r in reg.iterrows():
        area[r["Stand"]] = area.get(r["Stand"], 0) + 0.2 * r["Cond 1 share"]
        if isinstance(r["Cond 2 stand"], str):
            area[r["Cond 2 stand"]] = area.get(r["Cond 2 stand"], 0) + 0.2 * r["Cond 2 share"]

    def stand(p, c):
        return st1[p] if c == 1 else st2[p]

    # the manual's Table 1, read word by word on its own lines (not the golden's text regex)
    vol = {}
    with pdfplumber.open(os.path.join(target, "inventory", "cfi_field_manual_rev2026.pdf")) as pdf:
        for pg in pdf.pages:
            lines = {}
            for w in pg.extract_words():
                lines.setdefault(round(w["top"]), []).append(w)
            logs = None
            for top in sorted(lines):
                toks = [w["text"] for w in sorted(lines[top], key=lambda w: w["x0"])]
                if toks[0] == "DBH" and len(toks) == 12:
                    logs = [float(v) for v in toks[1:]]
                elif logs and len(toks) == 12 and all(t.isdigit() for t in toks):
                    vol[int(toks[0])] = {L: int(v) for L, v in zip(logs, toks[1:])}
    # stem-map identity of the added records
    rec = t26[t26.status != "N"].set_index("tag")
    added = t26[t26.status == "N"]
    t21["x"] = t21.dist_ft * np.sin(np.radians(t21.azimuth))
    t21["y"] = t21.dist_ft * np.cos(np.radians(t21.azimuth))
    by_plot = {p: g for p, g in t21.groupby("plot_no")}
    link, dup = {}, set()
    for r in added.itertuples():
        g = by_plot.get(r.plot_id)
        if g is None:
            continue
        x1, y1 = r.dist_ft * math.sin(math.radians(r.azimuth_deg)), r.dist_ft * math.cos(math.radians(r.azimuth_deg))
        dd = np.hypot(g.x - x1, g.y - y1)
        ok = g[(dd <= 3.0) & (g.spp == fia2alpha[r.species_fia]) & ((r.dbh_in - g.dbh_in) >= -0.4) &
               ((r.dbh_in - g.dbh_in) <= 3.2)]
        if len(ok) == 1:
            tg = int(ok.tag.iloc[0])
            s = rec.loc[tg, "status"]
            if s == "M":
                link[tg] = (int(r.tag), float(r.dbh_in))
            elif s == "L":
                dup.add((r.plot_id, int(r.tag)))
    fate = {}
    for r in t21.itertuples():
        s = rec.loc[r.tag, "status"]
        fate[r.tag] = "live" if (s == "L" or (s == "M" and r.tag in link)) else {"D": "dead", "C": "cut", "M": "missing"}[s]
    t21["stand"] = [stand(p, c) for p, c in zip(t21.plot_no, t21.cond)]
    t21["ba"] = 0.005454 * t21.dbh_in ** 2
    t21["lost"] = [fate[t] in ("dead", "missing") for t in t21.tag]
    sh = (t21[t21.lost].groupby("stand").ba.sum() / t21.groupby("stand").ba.sum()).fillna(0)
    sh = sh.reindex(sorted(area)).fillna(0)
    live = t26[t26.status.isin(["L", "N"])].copy()
    live = live[[not (p, t) in dup for p, t in zip(live.plot_id, live.tag)]]
    live["stand"] = [stand(p, c) for p, c in zip(live.plot_id, live.cond_id)]
    live["ba"] = 0.005454 * live.dbh_in ** 2
    hts = rev.set_index(["plot_id", "tag"]).merch_ht_ft.to_dict()

    def net(r):
        if r.dbh_in < 11.0 or r.species_fia in hard:
            return 0.0
        m = r.merch_ht_ft if not np.isnan(r.merch_ht_ft) else hts.get((r.plot_id, r.tag))
        if m is None or (isinstance(m, float) and np.isnan(m)):
            return 0.0
        lg = min(6.0, math.floor(m / 16.5 * 2) / 2)
        cls = 12 + 2 * int((r.dbh_in - 11.0) // 2)
        c = 0 if np.isnan(r.cull_pct) else r.cull_pct
        return vol[cls][lg] * 10 * (1 - c / 100.0)
    live["net"] = [net(r) for r in live.itertuples()]
    ba_ac = (live.groupby("stand").ba.sum() / pd.Series(area)).reindex(sorted(area))
    vol_ac = (live.groupby("stand").net.sum() / pd.Series(area)).reindex(sorted(area))
    return dict(fate=fate, link=link, dup=dup, share=sh, ba=ba_ac, vol=vol_ac, nvol=len(vol))


def main(target=None, gdir=None):
    task = os.path.dirname(HERE)
    target = target or os.path.join(task, "target")
    gdir = gdir or os.path.join(task, "golden")
    v = recompute(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    fails = []

    def chk(name, ok, detail=""):
        print("%s  V %s %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            fails.append(name)

    chk("volume table read as a table (positive control)", v["nvol"] == 20, "%d rows" % v["nvol"])
    marked = sorted(s for s, x in v["share"].items() if x >= 0.15)
    chk("marking list", marked == fig["marked"], str(marked))
    chk("shares", all("%.1f" % _half_up(100 * v["share"][s], 0.1) == fig["share_pct"][s] for s in fig["share_pct"]))
    chk("live basal area per acre", all("%.1f" % _half_up(v["ba"][s], 0.1) == fig["ba_ft2_ac"][s] for s in fig["ba_ft2_ac"]))
    chk("net volume per acre", all("{:,}".format(int(_half_up(v["vol"][s], 10))) == fig["vol_bf_ac"][s]
                                   for s in fig["vol_bf_ac"]))
    chk("linked and duplicate counts", len(v["link"]) == fig["retagged_linked"] and len(v["dup"]) == fig["found_tag_duplicates"],
        "%d linked, %d duplicates" % (len(v["link"]), len(v["dup"])))
    gf = pd.read_csv(os.path.join(gdir, "tree_fates_2021_2026.csv"))
    chk("golden CSV fates", len(gf) == len(v["fate"]) and all(v["fate"][t] == f for t, f in zip(gf.tag_2021, gf.fate_2026)),
        "%d rows" % len(gf))
    chk("golden CSV new tags", all((int(t26) == v["link"][t][0]) for t, t26 in zip(gf.tag_2021, gf.tag_2026.fillna(0))
                                   if t in v["link"]))
    with pdfplumber.open(os.path.join(gdir, "salvage_marking_2027.pdf")) as pdf:
        txt = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    rows = re.findall(r"^(CF-\d{3}) (\d+) .*? (\d+\.\d) (\d+\.\d) ([\d,]+)(?: Yes)?$", txt, re.M)
    chk("golden PDF stand table read back (positive control)", len(rows) == len(fig["share_pct"]), "%d rows" % len(rows))
    chk("golden PDF figures", all(fig["share_pct"][s] == a and fig["ba_ft2_ac"][s] == b and fig["vol_bf_ac"][s] == c
                                  for s, _, a, b, c in rows))
    chk("golden PDF names the stands to mark", all(s in txt.split("Figure 1")[0] for s in fig["marked"]))
    with pdfplumber.open(os.path.join(target, "policy", "salvage_marking_policy_2026.pdf")) as pdf:
        pol = " ".join((pg.extract_text() or "") for pg in pdf.pages)
    chk("policy carries the 15 per cent rule (positive control)", "15 per cent" in pol and "tallied live" in pol)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
