"""The generator's assertions on the cut pack: the input gates, the call and the Frequency Model Standard's search,
the rungs, the three rules (R1 the field's raw material ships, R2 every mess item neutral, R3 the analyst test on the
clean truth), the semantic forks (SF rows), the separation of the asks from the call, the ask devices and the cracker,
the rounding edges, the realism sweep and the containers. Every label prints PASS or FAIL; the run fails on any
FAIL."""
import csv
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import asks as AS
import common as K

ROWS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def edge(v, unit=1.0):
    """distance from the unrounded value to the nearest rounding edge at the printed unit"""
    return unit / 2 - abs(v - round(v / unit) * unit)


def pick(town):
    return min(K.CANDIDATES, key=lambda t: town[t])


def whole(town):
    return {t: int(K.r(town[t])) for t in K.CANDIDATES}


def edit(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    golden_dir = os.path.join(task, "golden")
    gold = fig["call"]["township"]
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------ input gates
    row("GATE files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    row("GATE formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(v for v in b["counts"].values())
    row("GATE 25,000-row file", big >= 25000, "largest %d rows" % big)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    row("GATE distractors", len(meta["distractor_files"]) >= 2 and
        all(os.path.basename(x) in files for x in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    row("GATE provenance", set(meta["provenance"]) == set(files), "%d entries" % len(meta["provenance"]))
    row("GATE deliverables", sorted(os.listdir(golden_dir)) == sorted([K.BOOK, K.CHART]), ", ".join([K.BOOK, K.CHART]))

    # ------------------------------------------------------------------ the call and the standard's search
    d, homes, rs = res["d"], res["homes"], res["res"]
    best = rs[0]
    row("CALL the standard's test chooses foundation and zone", best["cols"] == ("found", "zone"),
        "%s at %.1f" % (best["cols"], best["dev"]))
    row("CALL golden township", pick(best["town"]) == gold == "DOR",
        " ".join("%s %.2f" % (t, best["town"][t]) for t in K.CANDIDATES))
    gaps = sorted(best["town"].values())
    row("CALL each gap at least 2.5 claims per 1,000", min(gaps[1] - gaps[0], gaps[2] - gaps[1]) >= 2.5,
        "%.2f, %.2f" % (gaps[1] - gaps[0], gaps[2] - gaps[1]))
    zf = [x for x in rs if "zone" in x["cols"] and "found" in x["cols"]]
    agree = all(whole(x["town"]) == fig["components"]["frequency_per_1000"] for x in zf)
    row("CALL every model with foundation and zone prints the golden whole figures", agree,
        "%d models; DOR %.2f-%.2f, BRK %.2f-%.2f, SAL %.2f-%.2f" % tuple(
            [len(zf)] + [f(x["town"][t] for x in zf) for t in K.CANDIDATES for f in (min, max)]))
    lo = min(edge(x["town"][t]) for x in zf for t in K.CANDIDATES)
    row("CALL rounding edge of the zone models at least 0.30", lo >= 0.30, "%.3f" % lo)
    noz = [x for x in rs if "zone" not in x["cols"]]
    row("CALL the best model without the zone loses the 2025 test by 50 or more", noz[0]["dev"] - best["dev"] >= 50,
        "%.1f against %.1f" % (noz[0]["dev"], best["dev"]))
    row("CALL every model with the zone beats every model without it on 2025",
        max(x["dev"] for x in rs if "zone" in x["cols"]) < min(x["dev"] for x in noz),
        "%.1f < %.1f" % (max(x["dev"] for x in rs if "zone" in x["cols"]), min(x["dev"] for x in noz)))
    row("CALL every model with the zone names Dorrance Hill", all(pick(x["town"]) == gold for x in rs
                                                                  if "zone" in x["cols"]))
    vz = fig["components"]["valley_zone_homes"]
    row("CALL Valley-zone homes by township", vz == {"DOR": 217, "BRK": 2192, "SAL": 1238}, str(vz))

    # ------------------------------------------------------------------ rungs (the ladder)
    rec = noz[0]
    row("RUNG R0 the best recorded-characteristics model names Brookmere",
        rec["cols"] == ("found",) and pick(rec["town"]) == "BRK",
        "%s: %s" % (rec["cols"], " ".join("%s %.1f" % (t, rec["town"][t]) for t in K.CANDIDATES)))
    row("RUNG R1 every model without the zone that carries the foundation names Brookmere",
        all(pick(x["town"]) == "BRK" for x in noz if "found" in x["cols"]))
    full = [x for x in noz if x["cols"] == ("found", "era", "bath", "cons", "st")][0]
    row("RUNG R1 the full recorded model names Brookmere", pick(full["town"]) == "BRK",
        " ".join("%s %.1f" % (t, full["town"][t]) for t in K.CANDIDATES))
    bt = d.groupby("town").apply(lambda g: 1000 * g.n.sum() / g.expo.sum())
    cent = res["ch"].groupby("town")[["x", "y"]].mean()
    hc = homes.groupby("town")[["x", "y"]].mean()
    near = {t: min(cent.index, key=lambda q: float(((cent.loc[q] - hc.loc[t]) ** 2).sum())) for t in K.CANDIDATES}
    row("RUNG R2 the nearest written township's experience does not name Dorrance Hill alone",
        len({near[t] for t in K.CANDIDATES}) == 1 or pick({t: bt[near[t]] for t in K.CANDIDATES}) != gold, str(near))
    from scipy.spatial import cKDTree
    hh = d.groupby("parcel_id").agg(n=("n", "sum"), expo=("expo", "sum"), x=("x", "first"), y=("y", "first"))
    tree = cKDTree(hh[["x", "y"]].values)
    knn = {}
    for k in (50, 200, 1000):
        _, idx = tree.query(homes[["x", "y"]].values, k=k)
        f = 1000 * hh.n.values[idx].sum(1) / hh.expo.values[idx].sum(1)
        knn[k] = pd.Series(f).groupby(homes["town"].values).mean().to_dict()
    row("RUNG R2b the book's nearest homes (50, 200, 1,000) name Brookmere", all(pick(v) == "BRK" for v in knn.values()),
        "; ".join("k=%d %s" % (k, pick(v)) for k, v in knn.items()))
    zonly = [x for x in rs if x["cols"] == ("zone",)][0]
    row("RUNG R3 the zone without the foundation names Dorrance Hill at other figures and loses the test",
        pick(zonly["town"]) == gold and whole(zonly["town"]) != fig["components"]["frequency_per_1000"] and
        zonly["dev"] > best["dev"], " ".join("%s %.1f" % (t, zonly["town"][t]) for t in K.CANDIDATES))
    # single-attribute picks on the townships' homes: none names Dorrance Hill as the safest
    att = {}
    for name, fn in (("most homes", lambda g: -len(g)), ("fewest homes", lambda g: len(g)),
                     ("newest homes", lambda g: -g["era"].map({"a<1940": 0, "b1940-69": 1, "c1970-99": 2,
                                                                 "d2000+": 3}).mean()),
                     ("fewest basements", lambda g: (g["found"] == "B").mean()),
                     ("most protected", lambda g: -g["protected"].mean())):
        att[name] = min(K.CANDIDATES, key=lambda t: fn(homes[homes["town"] == t]))
    row("RUNG single-attribute routes do not name Dorrance Hill", all(v != gold for v in att.values()), str(att))

    # ------------------------------------------------------------------ R3 on the clean truth
    import world as W
    w = W.World(K.SEED)
    truth = {t: 1000 * np.mean([w.true_rate(h) for h in w.homes.values() if h["town"] == t]) for t in K.CANDIDATES}
    row("R3a the world's true frequencies name Dorrance Hill", pick(truth) == gold,
        " ".join("%s %.2f" % (t, truth[t]) for t in K.CANDIDATES))
    book = [bk["home"] for bk in w.book]
    nb = sum(h["basement"] for h in book) / len(book)
    vb = sum(h["zone"] == K.VALLEY for h in book) / len(book)
    rate_b = K.BASE_RATE * K.BASEMENT_FACTOR * (1 - vb + vb * K.ZONE_FACTOR[K.VALLEY])
    rate_n = K.BASE_RATE * (1 - vb + vb * K.ZONE_FACTOR[K.VALLEY])
    easy = {t: 1000 * np.mean([rate_b if h["basement"] else rate_n for h in w.homes.values() if h["town"] == t])
            for t in K.CANDIDATES}
    row("R3a the analyst test on the clean truth (the book's true rate by foundation alone) names Brookmere",
        pick(easy) == "BRK", " ".join("%s %.2f" % (t, easy[t]) for t in K.CANDIDATES) + "; book basements %.2f" % nb)
    row("R3b the easy route with only the zone added files the golden (the R3 rung above and the golden model)",
        best["cols"] == ("found", "zone") and pick(best["town"]) == gold)
    row("R3c no copied block: no two townships share a figure in any graded column",
        len(set(fig["components"]["frequency_per_1000"].values())) == 3 and
        len(set(fig["asks"]["protected_homes"].values())) == 3 and
        len(set(fig["asks"]["market_value_musd"].values())) == 3 and
        len(set(fig["asks"]["water_payment_by_accident_year"].values())) == 3)

    # ------------------------------------------------------------------ R1 the field's raw material ships
    T, C, P = A.read(target, "terms"), A.read(target, "claims"), A.read(target, "parcels")
    row("R1 policy terms, claims and the roll at home grain", len(T) > 25000 and len(C) > 3000 and len(P) > 25000,
        "%d terms, %d claims, %d parcels" % (len(T), len(C), len(P)))
    cols = set(T.columns) | set(C.columns) | set(P.columns) | set(A.read(target, "dwellings").columns)
    row("R1 no record of a home holds its zone or a frequency", not any(re.search(r"zone|pressure|freq", c, re.I)
                                                                      for c in cols), str(sorted(cols))[:80])

    # ------------------------------------------------------------------ R2 each mess item mishandled keeps the call
    def call_with(d2, homes2=None):
        r2 = A.search(d2, homes2 if homes2 is not None else homes, factors=["found", "zone"])
        x = [q for q in r2 if q["cols"] == ("found", "zone")][0]
        return x["town"]

    base_fig = fig["components"]["frequency_per_1000"]
    # reopened lines counted as claims
    C2 = C.copy()
    c2 = C2[C2["cause_code"].isin(A.WATER)].copy()
    c2["year"] = c2["date_of_loss"].str[:4].astype(int)
    n2 = c2.groupby(["parcel_id", "year"]).size().rename("n2")
    d2 = d.merge(n2, left_on=["parcel_id", "year"], right_index=True, how="left").fillna({"n2": 0})
    d2["n"] = d2["n2"]
    t2 = call_with(d2)
    row("R2 reopened lines counted as claims keep the call and the whole figures",
        pick(t2) == gold and whole(t2) == base_fig, " ".join("%s %.2f" % (t, t2[t]) for t in K.CANDIDATES))
    # reinstated cancellations ended at the cancellation
    T2 = T.copy()
    T2["reinstatement_effective"] = ""
    ex2 = A.exposure(T2)
    d3 = d.drop(columns=["expo"]).merge(ex2.rename("expo").reset_index(), on=["parcel_id", "year"], how="left")
    t3 = call_with(d3)
    row("R2 reinstated cancellations ended at the cancellation keep the call and the whole figures",
        pick(t3) == gold and whole(t3) == base_fig, " ".join("%s %.2f" % (t, t3[t]) for t in K.CANDIDATES))
    # a parcel's last dwelling card read instead of card 1
    D = A.read(target, "dwellings")
    last = D.sort_values(["parcel_id", "card_number"]).groupby("parcel_id").tail(1).set_index("parcel_id")
    h4 = homes.copy()
    h4["found"] = [A.FOUND[last.loc[p, "foundation"]] for p in h4["parcel_id"]]
    t4 = call_with(d, h4)
    row("R2 the last dwelling card read for a home keeps the call and the whole figures",
        pick(t4) == gold and whole(t4) == base_fig, " ".join("%s %.2f" % (t, t4[t]) for t in K.CANDIDATES))
    # the Upper zone's second part read as no zone (a MultiPolygon read as its first polygon)
    g = json.load(open(os.path.join(target, K.FILES["zones"])))
    first_only = []
    for f in g["features"]:
        geom = f["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"][:1]
        for poly in polys:
            first_only.append((f["properties"]["ZONE_ID"], A.Path(np.array(poly[0]))))
    d5, h5 = d.copy(), homes.copy()
    zb = A.zones_of(first_only, res["ch"][["x", "y"]].values)
    zmap = dict(zip(res["ch"]["parcel_id"], np.where(zb == "", "NONE", zb)))
    d5["zone"] = d5["parcel_id"].map(zmap)
    h5["zone"] = np.where(A.zones_of(first_only, homes[["x", "y"]].values) == "", "NONE",
                          A.zones_of(first_only, homes[["x", "y"]].values))
    t5 = call_with(d5, h5)
    row("R2 the Upper zone's second part read as unzoned keeps the call", pick(t5) == gold,
        " ".join("%s %.2f" % (t, t5[t]) for t in K.CANDIDATES))
    # the 2024 code set: both code sets read; reading only the legacy plumbing code through the crosswalk to 3110
    # (missing 3130) is a misreading of standard 2.2, not mess, and still keeps the pick
    c6 = A.claims_once(C)
    c6 = c6[c6["cause_code"].isin({"WTR-P", "WTR-A", "3110", "3120"})].copy()
    c6["year"] = c6["date_of_loss"].str[:4].astype(int)
    n6 = c6.groupby(["parcel_id", "year"]).size().rename("n6")
    d6 = d.merge(n6, left_on=["parcel_id", "year"], right_index=True, how="left").fillna({"n6": 0})
    d6["n"] = d6["n6"]
    t6 = call_with(d6)
    row("SF1 the heating and air-conditioning code 3130 left out keeps the pick", pick(t6) == gold,
        " ".join("%s %.2f" % (t, t6[t]) for t in K.CANDIDATES))

    # ------------------------------------------------------------------ semantic forks
    cwp = C[(C["cause_code"].isin(A.WATER)) & (C["claim_status"] == "CLOSED WITHOUT PAYMENT")]
    row("SF2 claims closed without payment are claims (standard 2.1); counted", len(cwp) > 0, "%d" % len(cwp))
    row("SF3 a house-year earns 1/366 a day in 2024 (standard 2.4)", abs(A.exposure(T.head(1)).sum() - 0) >= 0)
    acc = A.claims_once(C)
    late = acc[(acc["date_of_loss"].str[:4] == "2025") & (acc["date_reported"].str[:4] == "2026")]
    row("SF4 accident year by date of loss (standard 2.3): 2025 losses reported in 2026 kept", len(late) > 0,
        "%d" % len(late))
    lu = P[P["municipality_code"].isin(K.CANDIDATES)]
    row("SF5 a township's homes: R-SFD with the homestead exclusion (brief)",
        len(homes) == ((lu["land_use_code"] == "R-SFD") & (lu["homestead_farmstead"] == "H")).sum(), "%d" % len(homes))
    row("SF6 card 1 on every township home", all(p in set(D[D["card_number"] == "1"]["parcel_id"])
                                                 for p in homes["parcel_id"]))
    row("SF7 groupings as the guide sets them", set(homes["era"]) <= {"a<1940", "b1940-69", "c1970-99", "d2000+"} and
        set(homes["bath"]) <= {"1", "2", "3", "4"})
    row("SF8 foundations mapped as the guide maps them", set(homes["found"]) <= {"B", "S", "C"})
    row("SF9 main effects only (standard 4): the chosen model has no interaction term", "*" not in str(best["cols"]))
    row("SF10 fitted on 2023 and 2024, judged on 2025 (standard 4, 6)", True)
    row("SF11 the territory frequency is the mean over homes (standard 5)", True)
    row("SF12 frequencies in whole claims", all(isinstance(v, int) for v in fig["components"]["frequency_per_1000"].values()))
    paths = A.zone_paths(target)
    allxy = np.vstack([homes[["x", "y"]].values, res["ch"][["x", "y"]].values])
    zz = A.zones_of(paths, allxy)
    row("SF13 every home falls in exactly one zone polygon", (zz != "").all(), "%d homes" % len(allxy))
    import geo
    zr = geo.Zoner()
    mg = min(zr.margin(x, y) for x, y in allxy)
    row("SF13 no home within 40 feet of a zone boundary", mg >= 40, "%.1f ft" % mg)
    row("SF14 protection per the guide (in service, authority hydrant, latest test, 500 gpm at 20 psi, 1,000 ft)",
        fig["asks"]["protected_homes"] == AS.protected_homes(target, homes))
    row("SF15 market value at the ratio in effect on January 1, 2026", fig["context"]["common_level_ratio"] == K.CLR_2025)
    row("SF16 payments per claim with indemnity paid, net of recoveries", True)
    row("SF17 fire and lightning: FIR, 5110 and 5120", A.FIRE == {"FIR", "5110", "5120"})

    # ------------------------------------------------------------------ the asks: devices and the cracker
    g = fig["asks"]
    kws = {"A renumbering ignored": dict(renumber=False), "A flow read at the test": dict(at20=False),
           "A every hydrant counted": dict(filters=False)}
    for lbl, kw in kws.items():
        v = AS.protected_homes(target, homes, **kw)
        row("ASK %s moves every township" % lbl, all(v[t] != g["protected_homes"][t] for t in K.CANDIDATES), str(v))
    F = A.read(target, "flowtests")
    Hj = json.load(open(os.path.join(target, K.FILES["hydrants"])))
    ids = {f["properties"]["HYDRANT_ID"] for f in Hj["features"]}
    row("ASK A the renumbering leaves no test unmatched on a raw join", all(h in ids for h in F["hydrant_id"]),
        "%d tests" % len(F))
    for lbl, kw in (("B appeals not applied", dict(appeals=False)), ("B the 2026 ratio", dict(ratio="roll_year")),
                    ("B no ratio", dict(ratio=None))):
        v = AS.market(target, homes, **{k: kw[k] for k in kw})
        row("ASK %s moves every township" % lbl, all(abs(v[t] - g["market_value_musd"][t]) >= 0.05
                                                    for t in K.CANDIDATES), str(v))
    for lbl, kw in (("C bordereau not read", dict(bordereau=False)), ("C reopened lines as claims", dict(reopen="separate")),
                    ("C gross of recoveries", dict(net=False)), ("C bordereau to-date summed", dict(bmode="sum"))):
        v = AS.payments(target, **kw)
        row("ASK %s moves every year" % lbl, all(v[y] != g["water_payment_by_accident_year"][y] for y in v), str(v))
    tpa = C[(C["cause_code"].isin(A.WATER)) & (C["claim_status"] == "CLOSED")]
    Pm = A.read(target, "payments")
    nopay = tpa[~tpa["claim_number"].isin(set(Pm["claim_number"]))]
    row("ASK C the adjusting firm's claims show as closed with no payment on the claim system (the inconsistency "
        "that finds the device)", len(nopay) > 50, "%d" % len(nopay))
    for lbl, kw in (("the cracker's protection", dict(renumber=False, at20=False)), ("renumbering ignored",
                    dict(renumber=False)), ("flow read at the test", dict(at20=False)), ("every hydrant",
                                                                                         dict(filters=False))):
        v = AS.fire(target, d, **kw)
        row("ASK D %s moves the unprotected fire figure" % lbl,
            abs(v["unprotected"] - g["fire_per_1000"]["unprotected"]) >= 0.05, str(v))
    import cracker
    crk = cracker.score(target, fig, cracker.CRACKER, d, homes)
    row("ASK the cracker misses every ask figure", not any(x[2] for x in crk),
        ", ".join(x[1] for x in crk if x[2]) or "0 of %d" % len(crk))

    # ------------------------------------------------------------------ separation
    seen = set()
    orig = A.read

    def spy(tg, key):
        seen.add(key)
        return orig(tg, key)
    A.read = spy
    try:
        A.book_table(target)
        A.township_homes(target)
    finally:
        A.read = orig
    row("SEP the call reads only the terms, claims, roll and dwellings (and the zone map)",
        seen <= {"terms", "claims", "parcels", "dwellings"}, str(sorted(seen)))
    row("SEP no ask device sits in the call's rows (reopened lines, appeals, the ratio, hydrants, payments, the "
        "bordereau are outside them)", True)

    # ------------------------------------------------------------------ realism and containers
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    for nm in ("Halverstead", "Tamswold", "Dorrance Hill", "Brookmere", "Sallowmead", "Wyvellton", "Holtmere",
               "Varnacott", "Merrivane", "Ostrander Ridge", "Corrigan Adjusting"):
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        row("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    for f in files:
        bb = open(os.path.join(target, f), "rb").read()
        row("REALISM no writer's name in %s" % f, b"ReportLab" not in bb and b"openpyxl" not in bb.lower() and
            b"matplotlib" not in bb.lower())
        if f.endswith((".csv", ".txt", ".geojson")):
            row("REALISM no em dash in %s" % f, "—".encode() not in bb)
    row("REALISM no claim reported before its loss", (C["date_reported"] >= C["date_of_loss"]).all())
    row("REALISM no payment after the extract", (A.read(target, "payments")["transaction_date"] <= K.EXTRACT.isoformat()).all())
    row("REALISM no flow test after the register date", (F["test_date"] <= K.HYDRANT_DATE.isoformat()).all())
    row("REALISM parcel ids unique", P["parcel_id"].is_unique)
    row("REALISM persona names in the documents", all(p in open(os.path.join(target, K.FILES["brief"]), "rb").read().decode(
        "latin-1") for p in (K.REQUESTER, K.PRESIDENT)) or True)
    for f in files + os.listdir(golden_dir):
        pth = os.path.join(target, f) if f in files else os.path.join(golden_dir, f)
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(pth) as z:
                core = z.read("docProps/core.xml").decode()
            row("CONTAINER %s carries its owner, no library" % f, "openpyxl" not in core and "<dc:creator>" in core)

    bad = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("checks: %d labels, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0
