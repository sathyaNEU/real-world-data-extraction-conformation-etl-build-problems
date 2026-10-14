"""task452's assertions (architecture 2), run on every build: the input gates, the golden from the bundle against the
generator's truth, every wrong route by name, the convergence of the design's own implementations, the margins, every
semantic-fork row, the three-rules block on the clean truth, mess neutrality, the ask's stops and cracker, the
separation of the ask from the main call, the distractors' deletion test and the realism sweep."""
import json
import math
import os
import re

import numpy as np
import pandas as pd

import golden as GD
import interp as I
import landscape as L
import mapping as MP
import methods as M
import pack as P
import world as W

RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def offered(area):
    return M.emission_reductions(area)["offered_t"]


def run(target, golden_dir, world=None, meta_path=None):
    RESULTS.clear()
    X = world["golden"] if world and "golden" in world else GD.compute(target)
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}
    truth_pts = world["pts"] if world else I.points()

    # ---------------------------------------------------------------- input gates
    ok("gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    ok("gate: a file of 25,000 rows or more", world["counts"]["poly"] >= 25000, world["counts"]["poly"])
    dis = meta.get("distractor_files", [])
    ok("gate: two or more distractors in metadata.json", len(dis) >= 2 and all(d in files for d in dis), dis)
    ok("gate: no file name says distractor or answer", not any(re.search("distract|answer|known_issue|trap", f)
                                                                for f in files))
    ok("gate: every pack file has a source and licence in metadata.json",
       sorted(x["path"] for x in meta.get("files", [])) == files and all(x.get("license") for x in meta["files"]))

    # ---------------------------------------------------------------- the golden, from the bundle
    Ah = {s: v[0] for s, v in X["strata"].items()}
    ok("golden: the strata areas read from the design report are the generator's", Ah == {
        s: int(round(v)) for s, v in L.strata_areas().items()}, Ah)
    ok("golden: every point's conformed class equals the interpreters' truth",
       dict(zip(X["pts"].plot_id, X["pts"].ref)) == {p["plot_id"]: p["ref"] for p in truth_pts})
    truth_area = M.design_area(truth_pts, Ah)
    ok("golden: the design estimate from the bundle equals the generator's", abs(X["area"] - truth_area) < 1e-6,
       "%.2f" % X["area"])
    ok("golden: the area of deforestation is 122,900 ha", X["er"]["area_ha"] == 122_900)
    ok("golden: 23,229,780 tonnes offered for USD 116,148,900", X["er"]["offered_t"] == 23_229_780 and
       X["er"]["payment_usd"] == 116_148_900)
    edge = abs((X["area"] / 100) % 1 - 0.5) * 100
    ok("bins: the area sits 20 ha or more from a hundred-hectare rounding edge", edge >= 20, "%.1f ha" % edge)

    # ---------------------------------------------------------------- the design's own implementations converge (C1, C3)
    st = pd.read_excel(os.path.join(target, P.FILES["stats"]), header=3)
    conc = pd.read_csv(os.path.join(target, P.FILES["conc"]), dtype=str)
    prog = set(conc.loc[conc.accounting_area == "program", "district_2025"])
    st = st[st.district_2025.isin(prog)]
    Af = {f: float(st[c].sum()) for f, c in (("FD", "deforestation 2024-2025 (ha)"), ("FF", "stable forest (ha)"),
                                             ("FN", "non-forest (ha)"))}
    exact = L.strata_areas()
    pixel = {s: round(v / W.PIXEL_HA) * W.PIXEL_HA for s, v in exact.items()}
    impl = {"published whole hectares": M.design_area(truth_pts, Ah),
            "unrounded pixel areas": M.design_area(truth_pts, pixel),
            "Horvitz-Thompson by point": float(sum(Ah[p["stratum"]] / W.N_SAMPLE[p["stratum"]] for p in truth_pts
                                                   if p["ref"] == "D")),
            "post-stratified to the final map, design weights": M.poststratified_area(truth_pts, Ah, Af)}
    ok("C3: every design-consistent implementation reports 122,900 ha and offers the same tonnes",
       len({M.reported(v) for v in impl.values()}) == 1 and len({offered(v) for v in impl.values()}) == 1,
       {k: round(v, 1) for k, v in impl.items()})

    # ---------------------------------------------------------------- the wrong routes, by name
    tb = M.textbook_area(truth_pts, Af)
    ua = M.map_user_accuracy(truth_pts, Af)
    mp = M.map_area(Af)
    raw = M.raw_share(truth_pts)
    routes = {"R0 final map area": mp, "R1' final map times its user's accuracy": ua,
              "R1 (default) error matrix on the final map's classes": tb, "raw share of points": raw}
    ok("R1 (default): the textbook estimator on the final map's classes files about 172,000 ha and 3,382,582 tonnes",
       166_000 < tb < 178_000 and offered(tb) == 3_382_582, "%.0f ha, %d t" % (tb, offered(tb)))
    ok("R0: the final map's own area files 73,225 ha and 43,484,518 tonnes", abs(mp - sum(X["map_fd"].values())) < 0.01
       and round(mp) == 73_225 and offered(mp) == 43_484_518, "%.2f" % mp)
    ok("R1': the final map times its user's accuracy files another amount", offered(ua) not in (
        X["er"]["offered_t"], offered(mp), 0), "%.0f ha, %d t" % (ua, offered(ua)))
    ok("raw share: every point weighted alike files no reductions", offered(raw) == 0, "%.0f" % raw)
    ok("ladder: every route offers another amount, and every route but the raw share offers some",
       len({offered(v) for v in routes.values()} | {X["er"]["offered_t"]}) == 5 and
       all(offered(v) != X["er"]["offered_t"] for v in routes.values()) and
       sum(offered(v) > 0 for v in routes.values()) == 3, {k: offered(v) for k, v in routes.items()})
    ok("dominance: the default route sits 40,000 ha or more above the golden, the map's area 40,000 ha below",
       tb - X["area"] >= 40_000 and X["area"] - mp >= 40_000, "%.0f, %.0f" % (tb - X["area"], X["area"] - mp))

    # ---------------------------------------------------------------- the three rules, executed on the clean truth
    heads = open(os.path.join(target, P.FILES["main"]), encoding="utf-8").readline()
    ok("R1 the field's raw material ships: 4,000 interpreted reference points with their strata",
       world["counts"]["main"] == 4000 and "stratum" in heads)
    ok("R1 no shipped column holds a point's weight, a design estimate or a reference class",
       not re.search(r"(?i)weight|estimate|ref_class|reference_class", heads), heads.strip())
    clean = [dict(p, ref=p["true"]) for p in truth_pts]
    ok("R3a analyst test: on the clean truth the error matrix on the final map's classes offers 3,382,582 tonnes",
       offered(M.textbook_area(clean, Af)) == 3_382_582)
    ok("R3b the decisive step alone: the same points on the sampling strata offer 23,229,780 tonnes",
       offered(M.design_area(clean, Ah)) == X["er"]["offered_t"])
    ok("R3b the first correction alone (the final map's own area) offers another amount", offered(mp) != X["er"][
        "offered_t"])
    main = pd.read_csv(os.path.join(target, P.FILES["main"]))
    block = main[["lc_2024", "canopy_2024", "lc_2025", "canopy_2025", "loss_year", "loss_month"]].astype(str)
    dup = block.duplicated(keep=False) & (main.change == "loss")
    ok("R3c no copied block: loss points repeat their interpretation no more often than chance",
       dup.mean() < 0.06, "%.3f" % dup.mean())

    # ---------------------------------------------------------------- Layer 1, every mess item neutral (R2)
    r2 = {}

    def as_forest(codes, canopy):
        q = [dict(p) for p in truth_pts]
        for p in q:
            f24 = p["lc24"] in codes and p["cc24"] in canopy
            f25 = p["lc25"] in codes and p["cc25"] in canopy
            p["ref"] = "N" if not f24 else ("F" if f25 else ("D" if p["loss_year"] in (2024, 2025) else "N"))
        return M.design_area(q, Ah)
    r2["plantations"] = as_forest((1, 2, 4), ("C", "D"))
    r2["woodland"] = as_forest((1, 2, 3), ("B", "C", "D"))
    for key, label in (("plantations", "plantations read as forest"),
                       ("woodland", "woodland at 10 per cent canopy read as forest")):
        ok("R2 mess: %s leaves the area and the offer unchanged" % label, abs(r2[key] - X["area"]) < 1e-6)
    shipped = pd.read_csv(os.path.join(target, P.FILES["main"]), dtype={"district": str})

    def bundle_area(df):
        ref = [GD.reference_class(int(a), b, int(c), d, (int(e) if pd.notna(e) else None)) for a, b, c, d, e in
               zip(df.lc_2024, df.canopy_2024, df.lc_2025, df.canopy_2025, df.loss_year)]
        wts = [Ah[s_] / W.N_SAMPLE[s_] for s_ in df.stratum]
        return float(sum(wt for wt, r in zip(wts, ref) if r == "D"))
    r2["main alone"] = bundle_area(shipped)
    ok("R2 mess: the main campaign alone, the adjudication ignored, leaves the area unchanged (read from the shipped "
       "export)", abs(r2["main alone"] - X["area"]) < 1e-6, "%.1f" % r2["main alone"])
    qcf = pd.DataFrame(json.load(open(os.path.join(target, P.FILES["qc"]), encoding="utf-8")))
    qcf["plot_id"] = qcf.id_parcela.str.replace("LFM26/", "LFM26-", regex=False)
    over = shipped.set_index("plot_id").copy()
    for r in qcf.itertuples():
        over.loc[r.plot_id, ["lc_2024", "canopy_2024", "lc_2025", "canopy_2025", "loss_year"]] = [
            GD.ES_LC[r.cobertura_2024], GD.ES_CANOPY[r.dosel_2024], GD.ES_LC[r.cobertura_2025],
            GD.ES_CANOPY[r.dosel_2025], r.anio_perdida]
    r2["qc wherever"] = bundle_area(over.reset_index())
    ok("R2 mess: the quality-control labels used wherever they exist leave the area unchanged (read from the "
       "ministry's Spanish export)", abs(r2["qc wherever"] - X["area"]) < 1e-6, "%.1f" % r2["qc wherever"])
    early = shipped[shipped.remarks.str.contains(r"cleared 20(?:1|2[0-3])", regex=True)]
    ok("R2 mess: clearings before 2024 noted in the remarks sit on land that was not forest in January 2024, so no "
       "reading of the remarks adds them to the period", len(early) > 0 and not early.lc_2024.isin(W.FOREST_CODES).any()
       and early.loss_year.isna().all(), "%d points" % len(early))
    ok("R2 mess: the 2019 and 2025 district layers touch only the district asks: the call sums every point whatever "
       "its district", abs(sum(X["by_d"].values()) - X["area"]) < 1e-6 and len(set(X["pts"].district)) == 12)

    # ---------------------------------------------------------------- the semantic fork table
    ok("SF1: the reporting period is two years: the reference level emissions are 89,410,300 t; one year would offer "
       "nothing", X["er"]["rl_t"] == 2 * 89_950 * 497.0 == 89_410_300 and 89_950 * 497.0 < X["er"]["monitored_t"])
    unrounded = math.floor((2 * W.RL_HA_YEAR - X["area"]) * W.EF * 0.82)
    ok("SF2: the area is stated to the nearest hundred hectares before the emission factor applies; the unrounded area "
       "would offer another amount", X["er"]["monitored_t"] == 122_900 * 497.0 and unrounded != X["er"]["offered_t"],
       "%d t unrounded" % unrounded)
    ok("SF3: the buffer is 18 per cent of the reductions and the fraction of a tonne is dropped (exact here: same call "
       "under any rounding)", X["er"]["offered_t"] == math.floor(X["er"]["er_t"] * 0.82) ==
       round(X["er"]["er_t"] * 0.82))
    ok("SF4: the payment is USD 5.00 a tonne offered; on the reductions before the buffer it would be another amount",
       X["er"]["payment_usd"] == 5 * X["er"]["offered_t"] and 5 * X["er"]["er_t"] != X["er"]["payment_usd"])
    ok("SF5: the area of deforestation is the reference sample's estimate (plan 4.1); the final map's own area offers "
       "another amount", offered(mp) != X["er"]["offered_t"])
    ok("SF6: deforestation is forest on 1 January 2024 and other land on 31 December 2025: no loss point outside "
       "the period, and clearings before 2024 sit on land that was not forest", all(
           p["loss_year"] in (2024, 2025) for p in truth_pts if p["change"] == "loss") and all(
           p["ref"] == "N" for p in truth_pts if p["kind"] == "cleared before 2024"))
    ok("SF7: forest is the plan's definition (30 per cent canopy, plantations excluded): plantations or woodland read "
       "as forest give the same area", abs(r2["plantations"] - X["area"]) < 1e-6 and abs(r2["woodland"] - X["area"]) < 1e-6)
    ok("SF10: the accounting area is the twelve districts on the 2019 layer: every reference point is in one",
       {p["district"] for p in truth_pts} == set(W.DCODE))
    ratio_d = {}
    for c in W.DCODE:
        m = (X["pts"].district == c).values
        land = float(st.loc[st.district_2025.map(dict(zip(conc.district_2025, conc.district_2019))) == c,
                            "total (ha)"].sum())
        ratio_d[c] = land * (w_all := X["pts"].weight.values)[m].dot(X["pts"].y.values[m]) / w_all[m].sum()
    ok("SF11: each district's area is its points' part of the accounting area's estimate (plan 4.5); the ratio to the "
       "district's land area files another figure in ten or more districts",
       sum(GD.hundred(ratio_d[c]) != GD.hundred(X["by_d"][c]) for c in W.DCODE) >= 10 and
       abs(sum(X["by_d"].values()) - X["area"]) < 1e-6,
       "%d of 12" % sum(GD.hundred(ratio_d[c]) != GD.hundred(X["by_d"][c]) for c in W.DCODE))
    ok("SF16: a point's reference class is the main campaign with the adjudicated fields applied; the main campaign "
       "alone or the quality-control labels wherever they exist give the same area",
       abs(r2["main alone"] - X["area"]) < 1e-6 and abs(r2["qc wherever"] - X["area"]) < 1e-6)
    # the interval under the design's own variants and under post-stratification to the final map (design weights)
    w_, y_, f_, s_ = (X["pts"].weight.values, X["pts"].y.values, X["pts"].map_class_v2.values,
                      X["pts"].stratum.values)
    code = {"FD": "DEF", "FF": "BOS", "FN": "NOB"}
    Afc = {code[k]: v for k, v in Af.items()}
    Nh = {k: w_[f_ == k].sum() for k in Afc}
    yb = {k: (w_[f_ == k] * y_[f_ == k]).sum() / Nh[k] for k in Afc}
    z_ = np.array([Afc[f_[i]] / Nh[f_[i]] * (y_[i] - yb[f_[i]]) for i in range(len(y_))])
    ps_area = sum(Afc[k] * yb[k] for k in Afc)
    ps_se = math.sqrt(sum(Ah[h] ** 2 * z_[s_ == h].var(ddof=1) / (s_ == h).sum() for h in Ah))
    se_n = math.sqrt(sum(Ah[h] ** 2 * y_[s_ == h].mean() * (1 - y_[s_ == h].mean()) / (s_ == h).sum() for h in Ah))
    variants = {"z 1.6449, n - 1": (X["lo"], X["hi"]), "z 1.645, n": (X["area"] - 1.645 * se_n, X["area"] + 1.645 * se_n),
                "t 3,997 df": (X["area"] - 1.64523 * X["se"], X["area"] + 1.64523 * X["se"]),
                "about the reported 122,900": (122_900 - GD.Z90 * X["se"], 122_900 + GD.Z90 * X["se"]),
                "post-stratified": (ps_area - GD.Z90 * ps_se, ps_area + GD.Z90 * ps_se)}
    tt = lambda v: int(10_000 * math.floor(v / 10_000 + 0.5))
    ok("SF8: the 90 per cent interval to the nearest ten thousand hectares is 100,000 to 140,000 under every variant "
       "of the design's variance and under post-stratification, each bound 1,000 ha or more from an edge",
       {(tt(a), tt(b)) for a, b in variants.values()} == {(100_000, 140_000)} and
       min(abs(v % 10_000 - 5_000) for ab in variants.values() for v in ab) >= 1_000,
       {k: "%.0f to %.0f" % v for k, v in variants.items()})
    edges = [abs((v / 100) % 1 - 0.5) * 100 for v in X["by_d"].values()]
    ok("SF9: every district's area sits 10 ha or more from a hundred-hectare rounding edge", min(edges) >= 10,
       "%.1f" % min(edges))

    # ---------------------------------------------------------------- the ask: deforestation patches by district
    poly = pd.read_parquet(os.path.join(target, P.FILES["poly"]))
    to19 = dict(zip(conc.district_2025, conc.district_2019))
    pp = poly[poly.district_2025.isin(prog)].copy()
    pp["d19"] = pp.district_2025.map(to19)
    pp["share"] = pp.area_ha / pp.patch_ha
    back = {v: k for k, v in W.D2025.items()}
    back[W.SPLIT_NEW[0]] = "05"
    true_all, true_small, true_big = ({c: 0 for c in W.DCODE} for _ in range(3))
    for pt in MP.patches():
        d19 = back[pt["district"]]
        if d19 in W.DCODE:
            true_all[d19] += 1
            true_small[d19] += pt["pix"] * W.PIXEL_HA < 1
            true_big[d19] += pt["pix"] * W.PIXEL_HA >= 5
    ok("ask: the patch counts equal the generator's patches, in all, under 1 ha and of 5 ha or more",
       X["patches_all"] == true_all and X["small"] == true_small and X["patches"] == true_big,
       "%d, %d and %d" % (sum(true_all.values()), sum(true_small.values()), sum(true_big.values())))
    whole = max(abs(v - round(v)) for v in list(pp.groupby("d19").share.sum()) +
                list(pp[pp.patch_ha >= 5].groupby("d19").share.sum()) +
                list(pp[pp.patch_ha < 1].groupby("d19").share.sum()))
    ok("ask: each district's polygon shares sum to whole patches (the count is exact from the file)", whole < 1e-6,
       "%.1e" % whole)
    ok("ask: patches are delivered in several polygons (tiles and quarters)", len(pp) > 1.25 * sum(true_all.values()),
       "%d polygons, %d patches" % (len(pp), sum(true_all.values())))

    golden_sets = (X["patches_all"], X["small"], X["patches"])

    def stop(label, frame, area_col="patch_ha"):
        """a counting route: every polygon row of `frame` that survives the route's deduplication is one patch"""
        sets = (frame, frame[frame[area_col] < 1], frame[frame[area_col] >= 5])
        got = [f.groupby("d19").size().to_dict() for f in sets]
        miss = [sum(g.get(c, 0) != t[c] for c in W.DCODE) for g, t in zip(got, golden_sets)]
        tot = all(sum(g.values()) != sum(t.values()) for g, t in zip(got, golden_sets))
        ok("ask stop '%s' misses all twelve districts on all three counts and every total" % label,
           miss == [12, 12, 12] and tot, "%d, %d and %d of 12; totals %s" % tuple(miss + [
               ", ".join(format(sum(g.values()), ",") for g in got)]))
    stop("polygons counted as patches", pp)
    stop("polygons deduplicated on the patch area", pp.drop_duplicates(["d19", "patch_ha"]))
    stop("polygons deduplicated on the patch area within the 2025 district",
         pp.drop_duplicates(["district_2025", "patch_ha"]))
    stop("polygons deduplicated on the patch area and first detection",
         pp.drop_duplicates(["district_2025", "patch_ha", "first_detected"]))
    stop("polygons deduplicated on the patch area and tile", pp.drop_duplicates(["district_2025", "patch_ha", "tile"]))
    stop("polygons sized by their own area", pp, area_col="area_ha")
    no06 = pp[pp.district_2025 != W.SPLIT_NEW[0]]
    ok("ask hazard: leaving out Nueva Esperanza misses La Esperanza on all three counts",
       round(no06.share[no06.d19 == "05"].sum()) != X["patches_all"]["05"] and
       round(no06.share[(no06.d19 == "05") & (no06.patch_ha < 1)].sum()) != X["small"]["05"] and
       round(no06.share[(no06.d19 == "05") & (no06.patch_ha >= 5)].sum()) != X["patches"]["05"])
    hl = poly[~poly.district_2025.isin(prog)]
    ok("ask hazard: the highland districts outside the accounting area move both totals",
       round((hl.area_ha / hl.patch_ha).sum()) > 0 and round((hl.area_ha / hl.patch_ha)[hl.patch_ha >= 5].sum()) > 0)
    ok("SF12: each district of the patch counts is a 2019 district: La Esperanza counts Nueva Esperanza's (LT-06) "
       "polygons too", X["patches_all"]["05"] == round(pp.share[pp.district_2025.isin(["LT-05", "LT-06"])].sum()))
    ok("SF13: a patch is the connected area of change whose area every one of its polygons carries (the dictionary's "
       "patch_ha), counted once however many polygons deliver it", whole < 1e-6 and len(pp) > sum(true_all.values()))
    ok("SF14: no patch measures exactly 1 ha or 5 ha (areas are whole 30 m pixels: 0.99 or 1.08, 4.95 or 5.04 ha), so "
       "each size class's boundary counts the same patches whichever side holds it",
       not ((poly.patch_ha > 0.995) & (poly.patch_ha < 1.075)).any() and
       not ((poly.patch_ha > 4.955) & (poly.patch_ha < 5.035)).any())
    ok("SF15: the totals are the accounting area's twelve districts; the highland districts lie outside it (the "
       "concordance's accounting_area)", set(conc.loc[conc.accounting_area == "outside", "district_2025"]) ==
       {W.D2025[c] for c, _, _ in W.HIGHLANDS} and not pp.district_2025.str.startswith("SR").any())
    ok("ask: the main call reads no polygon (the call is unchanged with the polygon file deleted)",
       X["er"]["offered_t"] == offered(M.design_area(truth_pts, Ah)))
    ok("ask: the final map's polygons sum to its mapped deforestation in every district",
       max(abs(pp.area_ha[pp.d19 == c].sum() - X["map_fd"][c]) for c in W.DCODE) < 0.01)

    # ---------------------------------------------------------------- distractors and realism
    used = {P.FILES[k] for k in ("main", "adj", "intersect", "stats", "poly", "conc", "design")}
    ok("distractors: the forest inventory and the fire hotspots are read by no step", not (
        set(meta.get("distractor_files", [])) & used))
    ok("realism: no two districts share an estimated area, a patch count or a mapped area",
       len({round(v) for v in X["by_d"].values()}) == W.R and len(set(X["patches"].values())) == W.R and
       len(set(X["patches_all"].values())) == W.R and len(set(X["small"].values())) == W.R and
       len({round(v) for v in X["map_fd"].values()}) == W.R)
    ok("realism: the headline figures are not round", X["er"]["offered_t"] % 1000 != 0 and
       X["er"]["payment_usd"] % 1000 != 0)
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                       ".claude", "skills", "fingerprint", "cards", "task452.json")))
    ok("realism: every persona in the pack is on the card", set(W.PEOPLE.values()) <= set(card["world"]["people"]))
    raw_b = b"".join(open(os.path.join(target, f), "rb").read() for f in files if f.endswith((".pdf", ".xlsx")))
    ok("realism: containers carry no writing library's name", not re.search(rb"ReportLab|reportlab|openpyxl|matplotlib",
                                                                          raw_b))
    txt = "".join(open(os.path.join(target, f), encoding="utf-8").read() for f in files if f.endswith(".csv"))
    docs_text = "".join(GD.pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf"))
    ok("realism: no em or en dash in any text file or document", not re.search("[–—]", txt + docs_text))
    ok("realism: no document names the estimator, a weight or the default route",
       not re.search(r"(?i)weight|estimator|Horvitz|Olofsson|Stehman|error matrix|post-strat", docs_text))
    figs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok("figures.json: the call as computed", figs["offered_t"] == X["er"]["offered_t"] and
       figs["payment_usd"] == X["er"]["payment_usd"] and figs["area_ha"] == X["er"]["area_ha"])

    bad = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    print("checks: %d, failed %d" % (len(RESULTS), len(bad)))
    return not bad
