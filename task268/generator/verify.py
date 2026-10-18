"""The independent verifier for task268: reads only the shipped pack, the goldens and figures.json, recomputes the call
and every graded figure its own way (pandas, no generator module), and checks every file states them alike.

    python3 task268/generator/verify.py task268/target"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
GOLDEN = os.path.join(os.path.dirname(HERE), "golden")


def main(pack):
    f = lambda n: os.path.join(pack, n)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def check(cond, what):
        if not cond:
            bad.append(what)

    # the call: each tow into its grid cell by position, band means weighted by the bands' areas
    grid = pd.read_csv(f("ground_grid_annex_a.csv"))
    sv = pd.read_csv(f("survey_tows_2019_2026.csv"))
    hit = ((sv.shot_lat.values[:, None] < grid.lat_north.values[None, :]) & (sv.shot_lat.values[:, None] >= grid.lat_south.values[None, :])
           & (sv.shot_lon.values[:, None] >= grid.lon_west.values[None, :]) & (sv.shot_lon.values[:, None] < grid.lon_east.values[None, :]))
    check((hit.sum(axis=1) == 1).all(), "every tow in exactly one cell")
    k = hit.argmax(axis=1)
    sv["ground"] = grid.ground.values[k]
    sv["band"] = grid.depth_band.values[k]
    check((grid.ground_code.values[k] == sv.ground_code.values).all(), "every tow on its own ground")
    area = grid.groupby(["ground", "depth_band"]).area_km2.sum()
    m = sv.groupby(["ground", "survey_year", "band"]).haddock_kg.mean().reset_index()
    m["w"] = [area[(g, b)] for g, b in zip(m.ground, m.band)]
    idx = m.groupby(["ground", "survey_year"]).apply(lambda d: (d.haddock_kg * d.w).sum() / d.w.sum(), include_groups=False)
    falls = {}
    for g in grid.ground.unique():
        base = np.mean([idx[(g, y)] for y in (2019, 2020, 2021)])
        falls[g] = 100 * (1 - idx[(g, 2026)] / base)
    order = sorted(falls, key=lambda g: -falls[g])
    gap = falls[order[0]] - falls[order[1]]
    check(order[0] == fig["call"]["ground"], "the call: %s" % order[0])
    check(order[1] == fig["call"]["runner_up"], "the runner-up: %s" % order[1])
    check(int(gap + 0.5) == fig["call"]["gap"], "the gap: %.2f" % gap)
    for g, v in falls.items():
        check(int(v + 0.5) == fig["falls"][g], "%s fall %.2f" % (g, v))

    # Ask A: members' haddock landed January to September 2026 by port
    sn = pd.read_csv(f("sales_notes_2026.csv"), dtype={"grade": str})
    hist = pd.read_excel(f("member_vessels.xlsx"), sheet_name="Registration history")
    fac = pd.read_csv(f("conversion_factors.csv")).set_index(["species_code", "presentation_code"]).factor_to_live
    hd = sn.groupby("note_no").agg(buyer=("buyer_reg", "first"), pln=("vessel_pln", "first"), day=("landing_date", "first"),
                                   port=("port", "first"), issued=("issued", "first"))
    sig = sn.sort_values(["species", "presentation", "grade", "boxes", "weight_kg"]).groupby("note_no").apply(
        lambda d: tuple(zip(d.species, d.presentation, d.grade.fillna(""), d.boxes, d.weight_kg)), include_groups=False)
    hd["sig"] = sig
    hd = hd.reset_index().sort_values(["issued", "note_no"])
    keep = hd.drop_duplicates(["buyer", "pln", "day", "port", "sig"], keep="last").note_no
    x = sn[sn.note_no.isin(keep) & (sn.species == "HAD") & (sn.landing_date >= "2026-01-01") & (sn.landing_date <= "2026-09-30")]
    hist["from"] = pd.to_datetime(hist["Registered from"]).dt.strftime("%Y-%m-%d")
    hist["to"] = pd.to_datetime(hist["Registered to"]).dt.strftime("%Y-%m-%d").fillna("9999-12-31")
    x = x.merge(hist[["PLN", "from", "to"]], left_on="vessel_pln", right_on="PLN")
    x = x[(x.landing_date >= x["from"]) & (x.landing_date <= x["to"])]
    x = x.assign(live=x.weight_kg * [fac[(s, p)] for s, p in zip(x.species, x.presentation)])
    for port, d in x.groupby("port"):
        t, v = d.live.sum() / 1000, d.value_gbp.sum()
        check(int(t + 0.5) == fig["ask_a"][port]["tonnes"], "Ask A %s tonnes %.3f" % (port, t))
        check(int(v + 0.5) == fig["ask_a"][port]["value"], "Ask A %s value %.2f" % (port, v))

    # Ask B: quota left by pool on 30 September 2026
    lg = pd.read_csv(f("quota_ledger_2026.csv"), dtype={"licence": str})
    lg = lg[lg.effective <= "2026-09-30"]
    lg = lg[~(lg.licence.isna() & (lg.type == "allocation"))]
    for pool, t in lg.groupby("pool").tonnes.sum().items():
        check(int(t + 0.5) == fig["ask_b"][pool], "Ask B %s %.3f" % (pool, t))

    # the goldens state the same figures
    wb = pd.read_excel(os.path.join(GOLDEN, "ground_closure_2027.xlsx"), sheet_name=None, header=None)
    gr = wb["Grounds"]
    rows = gr[gr[0].isin(list(falls))]
    for _, r in rows.iterrows():
        check(int(r[13]) == fig["falls"][r[0]], "workbook fall %s" % r[0])
    pt = wb["Ports"]
    for _, r in pt[pt[0].isin(list(fig["ask_a"]))].iterrows():
        check(int(r[1]) == fig["ask_a"][r[0]]["tonnes"] and int(r[2]) == fig["ask_a"][r[0]]["value"], "workbook port %s" % r[0])
    pl = wb["Pools"]
    for _, r in pl[pl[0].isin(list(fig["ask_b"]))].iterrows():
        check(int(r[2]) == fig["ask_b"][r[0]], "workbook pool %s" % r[0])
    from pptx import Presentation
    deck = Presentation(os.path.join(GOLDEN, "closure_committee_2027.pptx"))
    texts = " ".join(sh.text_frame.text for s in deck.slides for sh in s.shapes if sh.has_text_frame)
    check(("Close %s" % fig["call"]["ground"]) in texts, "the deck states the call")
    check(("%d points" % fig["call"]["gap"]) in texts, "the deck states the gap")
    charts = [sh.chart for s in deck.slides for sh in s.shapes if sh.has_chart]
    check(len(charts) == 1 and len(list(charts[0].plots[0].series)) == 7, "the deck's chart: six grounds and the base")
    if bad:
        print("verify FAILED:\n  " + "\n  ".join(bad))
        return 1
    print("verify: the call, the gap, %d falls, %d port figures and %d pools recomputed independently; goldens agree"
          % (len(falls), 2 * len(fig["ask_a"]), len(fig["ask_b"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
