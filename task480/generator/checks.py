"""The generator's assertions on the built pack and golden: the call and every rung, every semantic fork of the
fork table (SF ids), the three-rules block on the clean truth, the asks' devices and fairness, the separation line,
the shock and oracle screens, and the input gates."""
import json
import os
import sys

import numpy as np
import pandas as pd

import asks as A
import golden as G
import guard_people as GP
import methods as M
import sim as S
import world as W

FAIL = []
N = [0]


def check(ok, msg):
    N[0] += 1
    if not ok:
        FAIL.append(msg)


def sets(e):
    return {k: tuple(n for n in W.CODE if v[n] >= W.LINE) for k, v in e.items()}


def main(t, gdir):
    names = [m[1] for m in W.MUNIS]
    gold_set = ("City of Dunmore", "City of Juniper", "Town of Cedar Run")
    default_set = ("City of Dunmore", "City of Juniper", "Town of Maple Ford")
    e = M.rungs(t)
    s = sets(e)
    fam = G.FAMILY
    # the call and the ladder
    for k in fam:
        check(s[k] == gold_set, "golden family member %s files %s" % (k, s[k]))
    check(s["place"] == default_set, "the default (2020 persons per dwelling) files %s" % (s["place"],))
    check(s["vintage"] == gold_set[:2] + ("Town of Cedar Run", "Town of Maple Ford"), "vintage files %s" % (s["vintage"],))
    check("Town of Cedar Run" not in s["trend"], "the trend rung keeps Cedar Run out")
    check("Town of Cedar Run" not in s["type"], "the type rung keeps Cedar Run out")
    for k in ("place", "trend", "type", "vintage"):
        check(s[k] != gold_set, "rung %s lands the golden" % k)
    cr, mf = "Town of Cedar Run", "Town of Maple Ford"
    check(min(e[k][cr] for k in fam) >= W.LINE + 300, "Cedar Run's golden margin under 300")
    check(max(e[k][mf] for k in fam) <= W.LINE - 300, "Maple Ford's golden margin under 300")
    check(e["place"][cr] <= W.LINE - 200 and e["place"][mf] >= W.LINE + 300, "the default's margins")
    for n in names:
        if n in (cr, mf):
            continue
        for k in [q for q in e if q not in ("age3_x",)]:
            if n in gold_set:
                check(e[k][n] >= W.LINE + 2000, "%s near the line on %s" % (n, k))
            elif k != "type":
                check(e[k][n] <= W.LINE - 400, "%s near the line on %s" % (n, k))
    # the truth agrees with the golden, and the analyst test on the clean truth (dataset-generation 7.1)
    tr = S.truth()
    check(tuple(n for n in W.CODE if tr[n] >= W.LINE) == gold_set, "the truth's set")
    w = S.world()
    occ20, size20 = S.households(W.C2020)
    x20, x26 = S.yfrac(W.C2020), S.yfrac(W.EST)
    hp20, hu20, hu26 = {}, {}, {}
    for u in w["units"]:
        if S.standing(u, x20):
            m = S.muni_on(u, W.C2020)
            m = "Village of Ivydale" if m == W.IVY_TOWN[1] else m
            hp20[m] = hp20.get(m, 0) + int(size20[u["uid"]])
            hu20[m] = hu20.get(m, 0) + 1
        if S.standing(u, x26):
            hu26[u["muni"]] = hu26.get(u["muni"], 0) + 1
    gq26 = {}
    for f, ty, m, era, v in S.gq_on(W.EST):
        gq26[m] = gq26.get(m, 0) + v
    clean = {n: hu26[n] * hp20[n] / hu20[n] + gq26.get(n, 0) for n in names}
    check(tuple(n for n in W.CODE if clean[n] >= W.LINE) == default_set,
          "the analyst test on the clean truth files the default set")
    # the semantic forks of the main call, each asserted to leave the call (fork table)
    variants = {"SF2": ("june30",), "SF5": ("gq_beds",), "SF6": ("gq_2020",), "SF8": ("final_only",),
                "SF9": ("expired_too",), "SF10": ("drop_year0",), "SF11": ("year_start",), "SF12": ("year_end",)}
    for sf, opts in variants.items():
        ev = M.rungs(t, opts)
        sv = sets(ev)
        check(all(sv[k] == gold_set for k in fam), "%s moves the golden family: %s" % (sf, {k: sv[k] for k in fam}))
        check(sv["place"] == default_set, "%s moves the default" % sf)
    # SF1: residents are household members plus group quarters residents (the statement, 2)
    st = open(os.path.join(t, W.FILES["method"]), "rb").read()
    check(len(st) > 1000, "the program statement is written")
    # SF3: boundaries in force on 1 July 2026: the 2021 annexation counts in Juniper
    check(any(r[2] == "2021-03-01" for r in __import__("pack").boundary_rows()), "SF3 the 2021 annexation is filed")
    # SF4: 10,000 or more against more than 10,000: no estimate within one resident of the line
    check(all(abs(e[k][n] - W.LINE) > 1 for k in e for n in names), "SF4 an estimate on the line")
    # SF7: the regression on household population (P15_001N), not total population with the survey added again
    ev = M.rungs(t, ("total_pop",))
    check(sets(ev)["age"] == gold_set, "SF7 the total-population regression moves the call")
    # SF13: no 2026 completion left out: the roll alone still files the golden on the 8-band profile
    ev = M.rungs(t, ("no_2026",))
    check(sets(ev)["age"] == gold_set, "SF13 the roll alone moves the 8-band call")
    # the backcast separates the families with margin
    f = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    for y in (2010, 2000):
        check(f["backcast_mape_age_%d" % y] * 2 < f["backcast_mape_place_%d" % y], "the backcast does not separate (%d)" % y)
        check(f["backcast_mape_age_%d" % y] * 3 < f["backcast_mape_vintage_%d" % y], "vintage not separated (%d)" % y)
    # the asks: fair, silent, every figure moved by its device, and outside the call's population
    bg, bn = A.births(t)
    dg, dn, dc = A.deaths(t)
    for n in names:
        check(abs(bg[n] - bn[n]) >= 3, "SF15 births device too thin in %s" % n)
        check(abs(dg[n] - dn[n]) >= 3, "SF17 deaths code device too thin in %s" % n)
        check(abs(dg[n] - dc[n]) >= 3, "SF16 deaths city reading too close in %s" % n)
    check(sum(bg.values()) == sum(bn.values()), "births lost in the naive reading")
    bb = pd.read_csv(os.path.join(t, W.FILES["births"]), dtype=str, keep_default_na=False)
    bb = bb[A.in_window(bb["CHILD_DOB"])]
    twins = int((bb["PLURALITY"] == "2").sum())
    check(twins > 0 and twins % 2 == 0, "SF18 twins are two records, one per infant (%d records)" % twins)
    st_txt = __import__("subprocess").run(["pdftotext", os.path.join(t, W.FILES["method"]), "-"], capture_output=True,
                                          text=True).stdout
    check("each live-born child one birth" in " ".join(st_txt.split()), "SF18 the statement counts each live-born child")
    b = pd.read_csv(os.path.join(t, W.FILES["births"]), dtype=str, keep_default_na=False)
    check(set(b["RES_CITY"].map(A.city_to_muni).dropna().index) == set(b.index), "SF14 a written city that names no municipality")
    d = pd.read_csv(os.path.join(t, W.FILES["deaths"]), dtype=str, keep_default_na=False)
    pre = d[pd.to_datetime(d["DATE_OF_DEATH"]) < pd.Timestamp(W.EDRS_SWITCH)]
    check((pre["RES_MCD_CODE"].str[-5:].map(W.NAME) == pre["RES_CITY"].map(A.city_to_muni)).all(),
          "SF17 the pre-2026 code is the written city's")
    post = d[pd.to_datetime(d["DATE_OF_DEATH"]) >= pd.Timestamp(W.EDRS_SWITCH)]
    check((post["RES_MCD_CODE"].str[-5:].map(W.NAME) == A.by_address(t, post, "RES_STREET")).all(),
          "SF17 the 2026 code is the address's")
    # the truth of the asks: the address-point reading is the simulated residence
    births, deaths = S.vital()
    lo, hi = S.yfrac(W.VITAL_FROM), S.yfrac(W.VITAL_TO) + 1 / 366.0
    tb = {}
    for ev_ in births:
        if lo <= ev_["when"] < hi:
            m = w["units"][ev_["uid"]]["muni"]
            tb[m] = tb.get(m, 0) + (2 if ev_["twin"] else 1)
    check(all(tb.get(n, 0) == bg[n] for n in names), "births golden is not the truth: %s" % {n: (tb.get(n, 0), bg[n]) for n in names})
    td = {}
    for ev_ in deaths:
        if lo <= ev_["when"] < hi:
            m = w["units"][ev_["uid"]]["muni"] if ev_["uid"] is not None else [g[2] for g in W.GQ if g[0] == ev_["gq"]][0]
            td[m] = td.get(m, 0) + 1
    check(all(td.get(n, 0) == dg[n] for n in names), "deaths golden is not the truth")
    # shock: the golden set is no interval of a shipped or derived sort
    h = M.census_hist(t)
    sorts = {"2020 population": {n: h[2020].loc[n, "Total population"] for n in names},
             "2010 population": {n: h[2010].loc[n, "Total population"] for n in names},
             "dwellings 2026": M.hu(t, M.xf(W.EST)), "births": bg, "deaths": dg,
             "dwellings added since 2020": {n: M.hu(t, M.xf(W.EST))[n] - h[2020].loc[n, "Housing units"] for n in names}}
    for k, v in sorts.items():
        top = tuple(sorted(sorted(names, key=lambda n: -v[n])[:3]))
        check(top != tuple(sorted(gold_set)), "shock: the golden set is the top three by %s" % k)
    # the people in the pack are the drawn personas
    ok, extra = GP.ok()
    check(ok, "personas outside the draw: %s" % extra)
    # input gates
    files = os.listdir(t)
    check(len(files) >= 10, "fewer than 10 files")
    check(len({f_.rsplit(".", 1)[1] for f_ in files}) >= 3, "fewer than 3 formats")
    rows = sum(1 for _ in open(os.path.join(t, W.FILES["roll"]))) - 1
    check(rows >= 25000, "the roll under 25,000 rows")
    # the golden workbook carries the call and the asks
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(gdir, G.REGISTER)).active
    reg = {ws.cell(row=r, column=2).value: (ws.cell(row=r, column=6).value, ws.cell(row=r, column=7).value,
                                            ws.cell(row=r, column=8).value) for r in range(5, 5 + len(names))}
    for n in names:
        check(reg[n] == ("Yes" if n in gold_set else "No", bg[n], dg[n]), "register row %s" % n)
    print("checks: %d run, %d failed" % (N[0], len(FAIL)))
    for x in FAIL:
        print("  FAIL", x)
    return not FAIL


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
