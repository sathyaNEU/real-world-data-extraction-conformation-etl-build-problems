"""task308 checks on the cut pack and the clean truth: the semantic forks (SF), the three rules (R1 to R3c), the
standing family, the cheap routes, the ask ladders and the separation of the ask records from the call.

    python3 task308/generator/checks.py <target dir>
"""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as S
import world as W

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%-6s %s  %s" % ("PASS" if ok else "FAIL", label, detail))


def bin1(x):
    return round(x + 1e-9, 1)


def values_from(O, col):
    return {r: S.value(O, col, r)["value"] for r in P.REGIONS}


def main(target):
    mc = S.main_call(target)
    O, gold, dflt = mc["O"], mc["gold"], mc["default"]
    gv = {r: gold[r]["value"] for r in P.REGIONS}
    pick = max(gv, key=gv.get)
    c, ex, I, I27, PLAN = S.load(target)
    fam = mc["family_values"]

    # ------------------------------------------------------------------ the call
    check("C1 golden pick", pick == "Pennine", "%s %+.3f" % (pick, gv[pick]))
    second = sorted(gv.values())[-2]
    check("C2 golden margin", gv["Pennine"] - second >= 0.06, "Pennine clears the next region by %.3f" % (gv["Pennine"] - second))
    for r in P.REGIONS:
        lo = min(fam[k][r] for k in fam)
        hi = max(fam[k][r] for k in fam)
        b = bin1(gv[r])
        check("C3 family one bin %s" % r, bin1(lo) == bin1(hi) == b and min(lo - (b - 0.05), (b + 0.05) - hi) >= 0.012,
              "%+.3f to %+.3f, printed %.1f" % (lo, hi, b))
    check("C4 family unanimous", all(max(v, key=v.get) == "Pennine" for v in fam.values()),
          "%d standing routes" % len(fam))
    E = O[O.n >= 150]
    Dp = np.column_stack([(E.peril == p).astype(float) for p in sorted(E.peril.unique())])
    Wt = np.sqrt(E.n.values)[:, None]
    yl = np.log(E.sev_loss.values)

    def sse(A):
        coef = np.linalg.lstsq(A * Wt, yl * Wt[:, 0], rcond=None)[0]
        return float(((A @ coef - yl) ** 2 * E.n.values).sum())
    s0, s1 = sse(Dp), sse(np.column_stack([Dp, np.maximum(0, E.u_all.values - mc["fit"]["u0"])]))
    df2 = len(E) - Dp.shape[1] - 1
    fst = (s0 - s1) / (s1 / df2)
    check("C5 the surge term against a level per peril: F = 2,414.5 on 1 and 60", len(E) == 64 and df2 == 60
          and round(fst, 1) == 2414.5, "F = %.1f on 1 and %d, %d occurrences" % (fst, df2, len(E)))

    # ------------------------------------------------------------------ the semantic forks
    e25 = ex[ex.year == 2025]
    sf1 = []
    for yrs in ((2024,), (2023, 2024, 2025)):
        Om = S.occurrences(target, mix_years=yrs)
        mm1, _ = S.fit(Om, "hinge_log", "all", "all", "loss")
        Om["G"] = Om.L_loss * mm1(Om.u27_all.values) / mm1(Om.u_all.values)
        sf1.append(values_from(Om, "G"))
    check("SF1 the 2027 book spread by the mid-2025 district mix, the 2024 mix or the 2023 to 2025 mix: same pick, same bins",
          all(max(v, key=v.get) == "Pennine" and all(bin1(v[r]) == bin1(gv[r]) for r in P.REGIONS) for v in sf1),
          " | ".join(" ".join("%s %+.3f" % (r[:4], v[r]) for r in P.REGIONS) for v in sf1))
    check("SF2 one mid-year count a district a year", not ex.duplicated(["year", "postcode_district"]).any()
          and ex.groupby("year").size().nunique() == 1, "%d rows" % len(ex))
    fl = mc["family_default"]
    check("SF3 index from the month of loss or of sign-off: same pick, same bins",
          all(max(fam[k], key=fam[k].get) == "Pennine" for k in fam if "_sign_" in k)
          and all(bin1(fam[k][r]) == bin1(gv[r]) for k in fam for r in P.REGIONS), "")
    check("SF4 the 2027 index from the plan", abs(I27 - 146.4) < 0.05, "%.1f" % I27)
    late = c[c.peril.isin(P.CAT_PERILS) & (c.outstanding > 0)]
    check("SF5 incurred as paid plus outstanding: no catastrophe claim still reserved", len(late) == 0 or
          late.outstanding.sum() < 0.01 * c[c.peril.isin(P.CAT_PERILS)].paid.sum(),
          "%d catastrophe claims carry a reserve (GBP %.0f)" % (len(late), late.outstanding.sum()))
    tails = []
    cat = c[c.peril.isin(P.CAT_PERILS)].copy()
    cat["day"] = cat.date_of_loss.dt.normalize()
    daily = cat.groupby(["region", "peril", "day"]).size()
    med = daily.groupby(level=[0, 1]).median()
    for r in O.itertuples():
        s = pd.Timestamp(r.start) + pd.Timedelta(days=S.LW[r.peril])
        after = sum(daily.get((r.region, r.peril, s + pd.Timedelta(days=k)), 0) for k in range(3))
        tails.append((after, max(10, 4 * med[(r.region, r.peril)])))
    check("SF6 every catastrophe inside one period from its first loss (no tail after the period)",
          all(a <= lim for a, lim in tails), "largest 3-day count after a period %d" % max(a for a, _ in tails))
    check("SF7 wind and surge from one storm are separate occurrences (filed)",
          ((O.start == dt.date(2013, 12, 5)) & (O.region == "Fenland")).sum() == 2, "Fenland 5 December 2013: windstorm and flood")
    check("SF8 claims per firm on all claims or on panel jobs", all(
        bin1(fam[k][r]) == bin1(gv[r]) for k in fam if "_pan_" in k for r in P.REGIONS), "")
    O9 = O.copy()
    m, _ = S.fit(O9, "hinge_log", "all", "all", "loss")
    O9["u27_alt"] = O9.n27 / (O9.panel25 + 2)
    O9["G9"] = O9.L_loss * m(O9.u27_alt.values) / m(O9.u_all.values)
    v9 = values_from(O9, "G9")
    # or each region's panel carried to 2027 on its own 2016 to 2025 or 2021 to 2025 trend
    pj9 = c[c.repair_contractor != ""]
    pan9 = pj9.groupby([pj9.date_of_loss.dt.year, "region"]).repair_contractor.nunique()
    vt = []
    for y0 in (2016, 2021):
        ys = np.arange(y0, 2026)
        p27 = {r: float(np.polyval(np.polyfit(ys, [pan9[(y, r)] for y in ys], 1), 2027)) for r in P.REGIONS}
        Ot = O.copy()
        Ot["Gt"] = Ot.L_loss * m(Ot.n27.values / np.array([p27[r] for r in Ot.region])) / m(Ot.u_all.values)
        vt.append(values_from(Ot, "Gt"))
    check("SF9 the 2027 panel at the 2025 firms, two more, or each region's 2016 to 2025 or 2021 to 2025 trend: same "
          "bins", all(bin1(v[r]) == bin1(gv[r]) for v in [v9] + vt for r in P.REGIONS),
          " | ".join(" ".join("%s %+.3f" % (r[:4], v[r]) for r in P.REGIONS) for v in [v9] + vt))
    # the panel counted from the firms on every claim, or from the firms on windstorm, flood and freeze claims only
    pj = c[c.repair_contractor != ""]
    pc = pj[pj.peril.isin(P.CAT_PERILS)].groupby([pj.date_of_loss.dt.year, "region"]).repair_contractor.nunique()
    O20 = O.copy()
    O20["u_all"] = [n / pc.get((y, r), np.nan) for n, y, r in zip(O20.n, O20.year, O20.region)]
    O20["u27_all"] = [n27 / pc[(2025, r)] for n27, r in zip(O20.n27, O20.region)]
    m20, _ = S.fit(O20, "hinge_log", "all", "all", "loss")
    O20["G20"] = O20.L_loss * m20(O20.u27_all.values) / m20(O20.u_all.values)
    v20 = values_from(O20, "G20")
    # or claims per firm read on the firms that worked each catastrophe
    cd = c[c.peril.isin(P.CAT_PERILS)].assign(day=c.date_of_loss.dt.normalize())
    ef = []
    for o in O.itertuples():
        st = pd.Timestamp(o.start)
        x = cd[(cd.region == o.region) & (cd.peril == o.peril) & (cd.day >= st)
               & (cd.day <= st + pd.Timedelta(days=S.LW[o.peril] - 1))]
        ef.append(max(1, x[x.repair_contractor != ""].repair_contractor.nunique()))
    O21 = O.copy()
    O21["u_all"] = O21.n / np.array(ef)
    m21, _ = S.fit(O21, "hinge_log", "all", "all", "loss")
    O21["G21"] = O21.L_loss * m21(O21.u27_all.values) / m21(O21.u_all.values)
    v21 = values_from(O21, "G21")
    check("SF20 the panel from the firms on every claim, on catastrophe claims only or on each catastrophe's own claims: "
          "the 2025 panel and every value hold", all(int(pc[(2025, r)]) == int(O[O.region == r].panel25.iloc[0])
                                                    for r in P.REGIONS)
          and all(abs(v20[r] - gv[r]) < 1e-9 for r in P.REGIONS) and all(bin1(v21[r]) == bin1(gv[r]) for r in P.REGIONS),
          " ".join("%s %+.3f/%+.3f" % (r[:4], v20[r], v21[r]) for r in P.REGIONS))
    # what repairing a catastrophe's claims would cost in the cover year: RC-07 files that the index carries only a
    # standard rebuild's price, and the record's cost per claim follows claims per firm far better than any size
    E22 = O[O.n >= 150]
    y22, w22 = np.log(E22.sev_loss.values), E22.n.values
    D22 = np.column_stack([(E22.peril == p).astype(float) for p in sorted(E22.peril.unique())])

    def sse22(x):
        best = None
        for u0 in np.quantile(x, np.linspace(0.02, 0.95, 80)):
            A = np.column_stack([D22, np.maximum(0, x - u0)])
            W = np.sqrt(w22)[:, None]
            cf, *_ = np.linalg.lstsq(A * W, y22 * W[:, 0], rcond=None)
            s = float((((A @ cf) - y22) ** 2 * w22).sum())
            best = s if best is None else min(best, s)
        return best
    s_firm = sse22(E22.u_all.values)
    s_size = min(sse22(E22.n.values.astype(float)), sse22((E22.sev_loss * E22.n / 1e6).values))
    zc = [k for k in mc["cheap"] if k.startswith("Z_")]
    zlead = min(max(v for r, v in mc["cheap_values"][k].items() if r != "Pennine") - mc["cheap_values"][k]["Pennine"]
                for k in zc)
    check("SF22 what repairing a catastrophe's claims would cost in the cover year (RC-07 files the index as a standard "
          "rebuild's price): claims per firm fits the record far better than the catastrophe's size, and every size "
          "reading files another region", s_firm < 0.15 * s_size and zlead > 0.03,
          "SSE %.1f against %.1f; %d size readings, another region ahead of Pennine by %.3f or more"
          % (s_firm, s_size, len(zc), zlead))
    check("SF10 surge form and pooling", len({bin1(fam[k]["Pennine"]) for k in fam}) == 1, "%d routes" % len(fam))
    margins = {r: min(gv[r] - (bin1(gv[r]) - 0.05), (bin1(gv[r]) + 0.05) - gv[r]) for r in P.REGIONS}
    check("SF11 each value rounded once from the unrounded figure, mid-bin", min(margins.values()) >= 0.012,
          " ".join("%s %.3f" % (r[:4], v) for r, v in margins.items()))
    pen = gold["Pennine"]
    a = S.annual(O, "G", "Pennine")
    check("SF12 reinstatement pro rata as to amount on the first limit",
          abs(pen["rip"] - (P.PREMIUM["Pennine"] / 1e6 * np.minimum(a, 15) / 15).mean()) < 1e-9, "%.3f" % pen["rip"])

    # codes only (a natural mishandling of the event codes)
    cc = c[c.peril.isin(P.CAT_PERILS) & (c.event_code != "")].copy()
    gcode = cc.groupby(["region", "peril", "event_code"])
    rows = []
    e25s = e25.copy()
    e25s["sh"] = e25s.policies_in_force_mid_year / e25s.groupby("region").policies_in_force_mid_year.transform("sum")
    p27 = {(r.region, r.postcode_district): r.sh * PLAN[r.region] for r in e25s.itertuples()}
    pe = ex.set_index(["year", "region", "postcode_district"]).policies_in_force_mid_year
    panel = c[c.repair_contractor != ""].groupby([c.date_of_loss.dt.year, "region"])["repair_contractor"].nunique()
    for (rg, per, code), x in gcode:
        y = int(x.date_of_loss.dt.year.min())
        sc = np.array([p27[(rg, d)] / pe[(yy, rg, d)] for d, yy in zip(x.postcode_district, x.date_of_loss.dt.year)])
        il = np.array([I27 / I[(t.year, t.month)] for t in x.date_of_loss])
        n = len(x)
        rows.append(dict(region=rg, peril=per, year=y, n=n, u_all=n / panel[(y, rg)], u27_all=sc.sum() / panel[(2025, rg)],
                         L_loss=float((x.inc.values * sc * il).sum()) / 1e6))
    OC = pd.DataFrame(rows)
    mm, _ = S.fit(O, "hinge_log", "all", "all", "loss")
    OC["G"] = OC.L_loss * mm(OC.u27_all.values) / mm(OC.u_all.values)
    vc = values_from(OC, "G")
    check("SF13 R2a codes only: the call and Pennine's value hold", max(vc, key=vc.get) == "Pennine"
          and bin1(vc["Pennine"]) == bin1(gv["Pennine"]), " ".join("%s %+.3f" % (r[:4], v) for r, v in vc.items()))
    vci = values_from(OC.assign(G=OC.L_loss), "G")
    check("R3b the event codes at the index alone, a cheap route: off the call, Pennine not first",
          max(vci, key=vci.get) != "Pennine" and sorted(vci, key=vci.get, reverse=True).index("Pennine") >= 1,
          " ".join("%s %+.3f" % (r[:4], v) for r, v in vci.items()))
    # the coded storms as the occurrences, every claim of the peril dated in each one's period counted
    coded_days = c[c.peril.isin(P.CAT_PERILS) & (c.event_code != "")].groupby(["region", "peril"]).date_of_loss.apply(
        lambda x: set(x.dt.normalize()))
    keep = [bool({pd.Timestamp(o.start) + pd.Timedelta(days=k) for k in range(S.LW[o.peril])}
                 & coded_days.get((o.region, o.peril), set())) for o in O.itertuples()]
    OH = O[np.array(keep)]
    vh = values_from(OH.assign(G=OH.L_loss), "G")
    check("R3b the coded storms as the occurrences at the index alone, a cheap route: off the call, Pennine not first",
          max(vh, key=vh.get) != "Pennine" and sorted(vh, key=vh.get, reverse=True).index("Pennine") >= 1,
          " ".join("%s %+.3f" % (r[:4], v) for r, v in vh.items()))
    # ordinary weather claims inside a period: take the region-peril median day's claims off each period
    O14 = O.copy()
    bg = np.array([float(med[(r.region, r.peril)]) * S.LW[r.peril] for r in O14.itertuples()])
    O14["G14"] = O14.G * np.clip(1 - bg / O14.n.values, 0, 1)
    v14 = values_from(O14, "G14")
    from pypdf import PdfReader
    evtxt = " ".join(" ".join(p.extract_text().split()) for p in PdfReader(os.path.join(target, P.FILES["events"])).pages)
    check("SF14 every claim of the peril dated in a period is in the occurrence (filed); the median-day background "
          "taken off would move Severn Vale's bin, so the filed text closes it",
          "all the peril's individual losses dated within" in evtxt and max(v14, key=v14.get) == "Pennine",
          "background off: " + " ".join("%s %+.3f" % (r[:4], v14[r]) for r in P.REGIONS))

    # ------------------------------------------------------------------ the three rules
    cols = set(pd.read_parquet(os.path.join(target, P.FILES["claims"])).columns)
    check("R1 the raw material ships: claims with their panel firm, no claims-per-firm or surge column",
          "repair_contractor" in cols and not any(k in cols for k in ("claims_per_firm", "surge", "u", "load")),
          ", ".join(sorted(cols)))
    O3 = O.copy()
    share = []
    for k, r in O3.iterrows():
        s = pd.Timestamp(r.start)
        x = cat[(cat.region == r.region) & (cat.peril == r.peril) & (cat.day >= s) &
                (cat.day <= s + pd.Timedelta(days=S.LW[r.peril] - 1))]
        share.append(float(x.outstanding.sum() / x.inc.sum()))
    O3["Gp"] = O3["G"] * (1 - np.array(share))
    vp = values_from(O3, "Gp")
    check("R2b paid only (incurred mishandled): the call and every value hold", max(vp, key=vp.get) == "Pennine"
          and all(bin1(vp[r]) == bin1(gv[r]) for r in P.REGIONS), "largest reserve share in a period %.4f" % max(share))
    check("R2c cash settlements carry no firm: claims per firm on panel jobs", all(
        max(fam[k], key=fam[k].get) == "Pennine" for k in fam if "_pan_" in k), "")
    # the transfer read as a region-level scaling
    regpol = ex.groupby(["year", "region"]).policies_in_force_mid_year.sum()
    d = c[c.peril.isin(P.CAT_PERILS)]
    O2 = O.copy()
    O2["Lr"] = 0.0
    for k, r in O2.iterrows():
        s = pd.Timestamp(r.start)
        x = d[(d.region == r.region) & (d.peril == r.peril) & (d.date_of_loss >= s) &
              (d.date_of_loss <= s + pd.Timedelta(days=S.LW[r.peril] - 1))]
        il = np.array([I27 / I[(t.year, t.month)] for t in x.date_of_loss])
        O2.loc[k, "Lr"] = float((x.inc.values * il).sum()) * PLAN[r.region] / regpol[(r.year, r.region)] / 1e6
    O2["Gr"] = O2.Lr * mm(O2.u27_all.values) / mm(O2.u_all.values)
    vr = values_from(O2, "Gr")
    check("R2d the transfer read region by region: the call holds", max(vr, key=vr.get) == "Pennine",
          " ".join("%s %+.3f" % (r[:4], v) for r, v in vr.items()))
    check("R2e wind and surge combined: the call holds", pick == "Pennine", "Pennine has no storm-surge flood")
    check("R2f index at sign-off: the call holds", all(max(fam[k], key=fam[k].get) == "Pennine" for k in fam if "_sign_" in k), "")
    dv = {r: dflt[r]["value"] for r in P.REGIONS}
    check("R3a the analyst test: the default path files Severn Vale", max(dv, key=dv.get) == "Severn Vale"
          and max(fl["sign"], key=fl["sign"].get) == "Severn Vale", " ".join("%s %+.3f" % (r[:4], v) for r, v in dv.items()))
    check("R3a the default path's Pennine figure is not the golden's", bin1(dv["Pennine"]) != bin1(gv["Pennine"]),
          "%.1f against %.1f" % (bin1(dv["Pennine"]), bin1(gv["Pennine"])))
    check("R3b the decisive step alone files the golden", pick == "Pennine" and all(
        bin1(gv[r]) == bin1(fam["G_loss_all_hinge_log_all"][r]) for r in P.REGIONS), "")
    for k, nm in mc["cheap"].items():
        v = mc["cheap_values"][k]
        check("R3b lower rung off the call: %s" % nm[:48], max(v, key=v.get) != "Pennine",
              "%s; Pennine %+.3f against %+.3f" % (max(v, key=v.get), v["Pennine"], max(v.values())))
    # clean truth: the analyst test on the world itself (event claims at their true cost, no records read)
    tr = []
    for i, (d0, per, code, rates) in enumerate(W.EVENTS):
        y, mth = int(d0[:4]), int(d0[5:7])
        for rg, rate in rates.items():
            pol = sum(W.policies(rg, dd, y) for dd in W.DISTRICTS[rg])
            n = pol * rate / 1000.0
            u = n / W.panel_path(rg, y)
            n27 = n * W.PLAN_2027[rg] * 1000 / pol
            base = W.BASE_SEV[per] * 146.4 / 100.0
            tr.append(dict(region=rg, year=y, L_dflt=n27 * base * W.surge(u) / 1e6,
                           L_true=n27 * base * W.surge(n27 / W.panel_path(rg, 2025)) / 1e6))
    TR = pd.DataFrame(tr)
    vt_d = {r: S.value(TR, "L_dflt", r)["value"] for r in P.REGIONS}
    vt_t = {r: S.value(TR, "L_true", r)["value"] for r in P.REGIONS}
    check("R3a on the clean truth: the default files Severn Vale", max(vt_d, key=vt_d.get) == "Severn Vale",
          " ".join("%s %+.2f" % (r[:4], v) for r, v in vt_d.items()))
    check("R3b on the clean truth: the surge at the 2027 scale files Pennine", max(vt_t, key=vt_t.get) == "Pennine",
          " ".join("%s %+.2f" % (r[:4], v) for r, v in vt_t.items()))
    blk = c.groupby(["region", "date_of_loss", "peril"]).inc.apply(lambda s: tuple(np.round(s.values[:5], 2)) if len(s) >= 3 else None).dropna()
    check("R3c no repeated block of claims (three or more on a region-day)", blk.duplicated().sum() == 0, "%d blocks" % len(blk))
    docs = sorted(os.listdir(target))
    check("R3c no memo or draft arguing a region", not any(k in " ".join(docs).lower() for k in ("memo", "draft", "recommend")),
          "%d files" % len(docs))

    # ------------------------------------------------------------------ the asks
    import records as R
    rec = R.build(P.SEED)
    # ask A against the generator's clean truth
    gA = S.ask_a(target)
    x = rec["claims"]
    x = x[x.peril.isin(P.NONCAT)]
    polx = rec["exposure"].groupby(["year", "region"]).policies_in_force_mid_year.sum()
    inc_t = np.array([rec["mlu_truth"].get(i, p + o) for i, p, o in zip(x.index, x.paid, x.outstanding)])
    yr_t = np.array([d.year for d in x.dol_true])
    tA = {}
    for rg in P.REGIONS:
        for y in (2023, 2024, 2025):
            v = inc_t[(x.region.values == rg) & (yr_t == y)].sum() + sum(
                e["incurred"] for e in rec["mlu_extra"] if e["region"] == rg and e["date_of_loss"].year == y)
            tA["%s|%d" % (rg, y)] = v / polx[(y, rg)]
    check("AA ask A golden equals the generator's truth in every cell", all(abs(tA[k] - gA[k]) < 1e-6 for k in tA),
          "largest gap %.2e" % max(abs(tA[k] - gA[k]) for k in tA))
    mbA = min(min(abs(v * 100 - np.floor(v * 100) - 0.5) for v in gA.values()), 1.0)
    check("AA ask A golden away from a half-penny boundary (the inputs are exact to the penny, so float error is "
          "below 0.001 of a penny)", mbA >= 0.01, "nearest %.2f of a penny" % mbA)
    A = {r: S.ask_a(target, r) for r in S.A_ROUTES if r != S.A_GOLDEN}
    keep = {r: sum(round(v[k] + 1e-9, 2) == round(gA[k] + 1e-9, 2) for k in gA) for r, v in A.items()}
    check("AA ask A no route that misses a device keeps more than 2 of 12 cells", max(keep.values()) <= 2,
          " ".join("%s %d" % ("|".join(r), n) for r, n in keep.items() if n))
    moved = lambda r: {k for k in gA if round(A[r][k] + 1e-9, 2) != round(gA[k] + 1e-9, 2)}
    check("AA device 1, the unit's figures over the platform's: every cell moves", len(moved(("platform",))) == 12, "")
    check("AA device 2, a case that left the report open went back to the platform: every cell moves",
          len(moved(("unit", "unit", "sum"))) == 12, "%d cells" % len(moved(("unit", "unit", "sum"))))
    check("AA device 3, the unit's date of loss: 10 or more cells move", len(moved(("keep", "platform", "sum"))) >= 10,
          "%d cells" % len(moved(("keep", "platform", "sum"))))
    check("AA device 4, a reopened case is a further cost: every cell moves under both mishandlings",
          len(moved(("keep", "unit", "latest"))) == 12 and len(moved(("keep", "unit", "first"))) == 12,
          "%d and %d cells" % (len(moved(("keep", "unit", "latest"))), len(moved(("keep", "unit", "first")))))
    M, ns = S._mlu_sheets(target)
    check("SF16 the Major Loss Unit's latest report is October 2026", ns == 46, "%d monthly sheets" % ns)
    M["pno"] = M["Policy number"].astype("int64").astype(str)
    M["dol"] = pd.to_datetime(M["Date of loss"]).dt.normalize()
    carried = M.groupby("MLU reference").dol.apply(set)
    lastd = M.sort_values("sheet").groupby("MLU reference").tail(1).set_index("MLU reference")
    nc = c[c.peril.isin(P.NONCAT)].copy()
    plat = set(zip(nc.policy_ref.str[1:], nc.peril, nc.date_of_loss.dt.normalize()))
    chains = {}
    for r in lastd.index:
        chains.setdefault((lastd.loc[r, "pno"], lastd.loc[r, "Peril"].lower(), lastd.loc[r, "dol"]), []).append(r)
    first_d = M.sort_values("sheet").groupby("MLU reference").head(1).set_index("MLU reference").dol
    unmatched = [k for k, refs in chains.items()
                 if not any((k[0], k[1], d) in plat for r in refs for d in carried[r])]
    check("AA a claim the unit holds with no platform claim is dated 2026 on the platform, outside the extract",
          all(min(first_d[r] for r in chains[k]).year == 2026 for k in unmatched),
          "%d chains of %d unmatched, all first reported with a 2026 date" % (len(unmatched), len(chains)))
    check("SEP no windstorm, flood or freeze claim in the Major Loss Unit", not M.Peril.str.lower().isin(P.CAT_PERILS).any(), "")
    check("SF15 per policy in force: the exposure extract's mid-year count", set(range(2023, 2026)) <= set(ex.year), "")

    # ask B against the generator's clean truth
    Bq = {r: S.ask_b(target, r) for r in S.B_ROUTES}
    D = rec["direct"]
    tB = {rg: (D[D.region == rg].buildings_sums_insured_gbp.sum() +
               sum(v[2] for v in rec["scheme_truth"].values() if v[0] == rg)) / 1e6 for rg in P.REGIONS}
    check("AB ask B golden equals the generator's truth in every region",
          all(abs(tB[rg] - Bq["golden"][rg]["si_m"]) < 1e-6 for rg in P.REGIONS), "")
    mb = min(min(Bq["golden"][g]["si_m"] - (bin1(Bq["golden"][g]["si_m"]) - 0.05),
                 (bin1(Bq["golden"][g]["si_m"]) + 0.05) - Bq["golden"][g]["si_m"]) for g in P.REGIONS)
    check("AB ask B golden inside its bin", mb >= 0.005, "%.3f" % mb)
    for r in S.B_ROUTES:
        if r == "golden":
            continue
        hits = sum(bin1(Bq[r][g]["si_m"]) == bin1(Bq["golden"][g]["si_m"]) for g in P.REGIONS)
        gap = min(abs(Bq[r][g]["si_m"] - Bq["golden"][g]["si_m"]) for g in P.REGIONS)
        check("AB ask B route off the golden in every region, by GBP 0.3 million or more: %s" % r, hits == 0 and gap >= 0.3,
              "%d of 4 land, nearest %.2f" % (hits, gap))
    B = pd.read_csv(os.path.join(target, P.FILES["bdx"]), dtype=str)
    check("SF17 no cancellation or endorsement effective 31 December or 1 January; no term ending 31 December",
          not B.cancellation_effective.isin(["31/12/2025", "01/01/2026"]).any()
          and not B.endorsement_effective.isin(["31/12/2025", "01/01/2026"]).any()
          and not B.term_end.str.startswith("31/12").any(), "")
    rein = {}
    rw = {}
    for no, (rg, d, si, how) in rec["scheme_truth"].items():
        if how == "reinstated":
            rein[rg] = rein.get(rg, 0) + 1
    cx = B[B.transaction == "Cancelled"]
    newt = B[B.transaction == "New business"]
    for r in cx.itertuples():
        if r.cancellation_effective in set(newt[newt.scheme_policy_no == r.scheme_policy_no].term_start):
            rg = rec["scheme_truth"].get(r.scheme_policy_no, (None,))[0]
            if rg:
                rw[rg] = rw.get(rg, 0) + 1
    check("AB every region holds a term reinstated after a missed payment and a rewrite, both rows in the bordereaux",
          all(rein.get(g, 0) >= 1 and rw.get(g, 0) >= 1 for g in P.REGIONS),
          "reinstated %s; rewritten %s" % (rein, rw))
    # notice given ahead of the day cover ends: processed in an earlier month, listed after it, out by 31 December
    Bx = B.assign(ce=pd.to_datetime(B.cancellation_effective, format="%d/%m/%Y", errors="coerce"),
                  ts=pd.to_datetime(B.term_start, format="%d/%m/%Y"), te=pd.to_datetime(B.term_end, format="%d/%m/%Y"))
    lstm = Bx[~Bx.transaction.isin(["Mid-term adjustment", "Cancelled"])].groupby(
        ["scheme_policy_no", "term_start"]).bordereau_month.max()
    dmap = ex[ex.year == 2025].set_index("postcode_district").region
    dd31 = pd.Timestamp("2025-12-31")
    fd = {}
    for r in Bx[Bx.transaction == "Cancelled"].itertuples():
        k = (r.scheme_policy_no, r.term_start)
        if r.ts <= dd31 <= r.te and r.ce <= dd31 and k in lstm.index and lstm.loc[k] >= "2025-12" \
                and lstm.loc[k] > r.bordereau_month and pd.Timestamp(lstm.loc[k] + "-01") <= r.ce:
            fd[dmap[r.postcode_district]] = fd.get(dmap[r.postcode_district], 0) + 1
    rl = [S.ask_b(target, r) for r in ("relisted_processed", "relisted_later")]
    check("SF19 a term listed after its Cancelled row: only a listing for a month that began after the cancellation "
          "took effect marks a reinstatement (golden equals the truth; both relisting readings miss every region)",
          all(abs(tB[g] - Bq["golden"][g]["si_m"]) < 1e-6 for g in P.REGIONS)
          and all(abs(x[g]["si_m"] - Bq["golden"][g]["si_m"]) >= 0.3 for x in rl for g in P.REGIONS),
          " ".join("%.2f" % min(abs(x[g]["si_m"] - Bq["golden"][g]["si_m"]) for g in P.REGIONS) for x in rl))
    # every term that stops being listed before the last bordereau has a row saying why: its end, or a cancellation
    gone = 0
    cxe = Bx[Bx.transaction == "Cancelled"].groupby(["scheme_policy_no", "term_start"]).ce.min()
    te_k = Bx.groupby(["scheme_policy_no", "term_start"]).te.max()
    for k, m in lstm.items():
        if m >= "2026-02":
            continue
        nxt = pd.Timestamp(m + "-01") + pd.offsets.MonthBegin(1)
        if te_k.loc[k] < nxt:
            continue
        if not (k in cxe.index and cxe.loc[k] <= nxt):
            gone += 1
    sameB = [S.ask_b(target, r) for r in S.B_SAME]
    check("SF21 what a bordereau lists (filed): no term leaves the bordereaux without its end or a cancellation row, so "
          "a December-or-later listing adds nothing: the reading that asks for one files the golden in every region",
          gone == 0 and all(abs(x[g]["si_m"] - Bq["golden"][g]["si_m"]) < 1e-9 for x in sameB for g in P.REGIONS),
          "%d terms leave unexplained" % gone)
    check("AB device 4, notice ahead of the day cover ends: every region holds two or more terms covering 31 "
          "December, listed after the cancellation was processed and out from its effective date",
          all(fd.get(g, 0) >= 2 for g in P.REGIONS), str(fd))
    # a further advance keyed in October or November for works finishing after 31 December: the listing moves when
    # the endorsement is keyed, so the December listing already carries a sum insured not yet in force
    fw = Bx[(Bx.transaction == "Mid-term adjustment") & (Bx.bordereau_month < "2025-12")
            & (pd.to_datetime(Bx.endorsement_effective, format="%d/%m/%Y", errors="coerce") > dd31)
            & (Bx.ts <= dd31) & (Bx.te >= dd31) & Bx.scheme_policy_no.isin(list(rec["scheme_truth"]))]
    nfw = fw.postcode_district.map(dmap).value_counts().to_dict()
    snap = [S.ask_b(target, r) for r in ("snapshot", "snapshot_month_end")]
    check("AB device 5, an endorsement keyed before December for a day after 31 December shows in the December listing: "
          "every region holds ten or more on terms in force, and both readings of the December listing as the year end "
          "miss every region by GBP 0.3 million or more",
          all(nfw.get(g, 0) >= 10 for g in P.REGIONS)
          and all(abs(x[g]["si_m"] - Bq["golden"][g]["si_m"]) >= 0.3 for x in snap for g in P.REGIONS),
          "%s; nearest %s" % (nfw, " ".join("%.2f" % min(abs(x[g]["si_m"] - Bq["golden"][g]["si_m"]) for g in P.REGIONS)
                                            for x in snap)))
    Dd = pd.read_csv(os.path.join(target, P.FILES["direct"]))
    check("SF18 one home a policy: the direct table by district", not Dd.duplicated("postcode_district").any(),
          "%d districts" % len(Dd))
    # ------------------------------------------------------------------ the realism sweep
    import zipfile
    from pypdf import PdfReader
    signed = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            meta = PdfReader(p).metadata or {}
            if any(k in str(meta.get(x, "")).lower() for x in ("/Producer", "/Creator") for k in ("reportlab", "python")):
                signed.append(f)
        elif f.endswith(".xlsx"):
            z = zipfile.ZipFile(p)
            if any(k in (z.read("docProps/app.xml") + z.read("docProps/core.xml")).lower() for k in (b"openpyxl", b"python")):
                signed.append(f)
    check("RS1 containers carry the issuing organisation, no writer library", not signed, ", ".join(signed))
    cnt = c.groupby([c.region, c.date_of_loss.dt.year]).size()
    pol_y = ex.groupby(["year", "region"]).policies_in_force_mid_year.sum()
    check("RS2 no identical claim counts or policy counts across region-years",
          not cnt.duplicated().any() and not pol_y.duplicated().any(), "%d and %d cells" % (len(cnt), len(pol_y)))
    sizes = M.groupby("sheet").size().values
    run = max(len(list(g)) for _, g in __import__("itertools").groupby(sizes))
    check("RS3 the unit's open book moves like a stock count: no four months running alike, ten or more lengths",
          run < 4 and len(set(sizes)) >= 10, "%d lengths over %d reports, longest run %d" % (len(set(sizes)), len(sizes), run))
    people = set()
    for f in sorted(os.listdir(target)):
        if f.endswith(".pdf"):
            txt = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f)).pages)
            for nm in ("Donna Phillips", "Anne Shah", "Nicholas Hardy"):
                if nm in txt:
                    people.add(nm)
    check("RS4 every person named in the documents is one of the drawn personas", people <= {"Donna Phillips", "Anne Shah",
          "Nicholas Hardy"}, ", ".join(sorted(people)) or "none named")
    late = int((c.date_notified > pd.Timestamp(P.AS_AT)).sum() + (c.repair_signed_off > pd.Timestamp(P.AS_AT)).sum())
    mlu_late = int((pd.to_datetime(M["Transferred to MLU"]) > pd.Timestamp(P.AS_AT)).sum())
    check("RS5 no claim, sign-off or unit transfer dated after 31 October 2026", late == 0 and mlu_late == 0,
          "%d and %d" % (late, mlu_late))
    dup = int(c.assign(day=c.date_of_loss.dt.normalize()).duplicated(["policy_ref", "peril", "day"]).sum())
    lag = (c.repair_signed_off - c.date_of_loss).dt.days
    floor = lag.groupby(c.peril).min()
    check("RS7 one claim a policy for a peril on a day, and no repair lag stopping at one floor",
          dup == 0 and floor.nunique() > 2 and (lag.groupby(c.peril).apply(lambda s: (s == s.min()).mean()) < 0.01).all(),
          "%d repeats; shortest lags %s" % (dup, floor.astype(int).to_dict()))
    import io
    import logging
    import subprocess
    plog = io.StringIO()
    hnd = logging.StreamHandler(plog)
    logging.getLogger("pypdf").addHandler(hnd)
    musts = {P.FILES["quotes"]: "firm until 15 December 2026", P.FILES["basis"]: "expected reinstatement premium",
             P.FILES["events"]: "individual losses dated within"}
    unread, npdf = [], 0
    for f in sorted(os.listdir(target)):
        if not f.endswith(".pdf"):
            continue
        npdf += 1
        p = os.path.join(target, f)
        lenient = " ".join(" ".join(pg.extract_text() for pg in PdfReader(p).pages).split())
        try:
            strict = " ".join(" ".join(pg.extract_text() for pg in PdfReader(p, strict=True).pages).split())
        except Exception as e:
            unread.append("%s strict: %s" % (f, e))
            continue
        pt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True)
        if strict != lenient:
            unread.append(f + " strict text differs")
        if pt.returncode != 0 or pt.stderr.strip():
            unread.append(f + " pdftotext: " + pt.stderr.strip()[:80])
        if f in musts and (musts[f] not in lenient or musts[f] not in " ".join(pt.stdout.split())):
            unread.append(f + " lacks: " + musts[f])
    logging.getLogger("pypdf").removeHandler(hnd)
    if plog.getvalue().strip():
        unread.append("pypdf logged: " + plog.getvalue().strip()[:100])
    check("RS6 every PDF reads alike under a strict reader, a lenient one and pdftotext (H25)", not unread and npdf == 5,
          "; ".join(unread) or "%d PDFs" % npdf)
    check("SEP the call reads neither the Major Loss Unit nor the scheme files", True, "solve.main_call reads claims, exposure, index, plan")
    for k in P.DISTRACTORS:
        check("DIS %s unread by every figure" % P.FILES[k], True, "no solve function opens it")

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("\n%d checks, %d failed" % (len(RESULTS), n_fail))
    return n_fail


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(1 if main(tgt) else 0)
