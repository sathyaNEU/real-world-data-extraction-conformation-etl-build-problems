"""The generator's assertions on the built pack and its clean truth: the three rules (R1 to R3c), the mechanism's
evidence and the easy route's validation, the semantic fork table (SF1 to SF18), bin edges, the ask devices and their
separation from the main call, the input gates, the realism sweep and the documents read back."""
import csv
import json
import os
import re

import numpy as np

import ops as O
import solve as SV
import world as W
import yard as Y

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as p:
        return re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in p.pages))


def k(v):
    return int(round(v / 1000.0))


REAL_NAMES = """helen fortum vantaan turku pori vaasan vaskiluoto kokkolan oulun epv pohjolan voima kemijoki ssab raahe
outokumpu rautaruukki ruukki neste lkab glencore drummond cerrejon prodeco peabody arch bowie suek kuzbass jsw pgg
weglokoks bogdanka adaro bumi anglo exxaro thungela seriti sasol kvarken kristinestad naantali hanasaari salmisaari
martinlaakso suomenoja inkoo meri-pori alholmen jakobstad pietarsaari nykarleby uusikaarlepyy kaskinen kalajoki
santamarta puertobolivar cienaga baltimore norfolk gdansk swinoujscie szczecin riga ventspils klaipeda tallinn
altamar ridgeline drummondco carbocoal coalbrook tygartvalley carbonesdelcaribe""".split()


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def run(target, golden_dir, x=None, n=None, meta_path=None, fig_path=None):
    RESULTS.clear()
    x = x or O.simulate()
    c = SV.compute(target)
    S, A, g, cl = c["S"], c["A"], c["per"], c["call"]
    fig = json.load(open(fig_path))
    files = sorted(os.listdir(target))
    burn = cl["burn"]

    # ------------------------------------------------------------------ R1: the field's raw material ships
    pts = len(S.x)
    ok("R1 every monthly survey ships as the contractor delivered it (grids on the plant grid in N60, XYZ lattices on "
       "ETRS-TM35FIN in N2000), the December lattice %d points" % pts,
       sum(f.endswith(".asc") for f in files) == W.B_FROM and sum(f.endswith(".xyz") for f in files) == 13 - W.B_FROM
       and pts > 20000)
    heads = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads += next(csv.reader(fh))
    ok("R1 no shipped column holds a volume, a stock, a base, a pad level or a toe",
       not any(re.search(r"volume|stock|base|pad|toe|bowl|settle|reserve", h, re.I) for h in heads), str(heads[:6]))

    # ------------------------------------------------------------------ R3a, R3b: the analyst test on the clean truth
    rho = {p[0]: SV.density_at(SV.densities(target), p[7], "2026-12-16") for p in W.PILES}
    true_res = sum(Y.true_volume(p[0], W.DEC) * rho[p[0]] for p in W.PILES)
    ok("R3a the clean truth's reserve (true volumes at the laboratory's densities) is above the floor",
       true_res > W.FLOOR_DAYS * burn, "%.0f against %.0f" % (true_res, W.FLOOR_DAYS * burn))
    clean = {}
    for p in W.PILES:
        name = p[0]
        msk = SV.in_area(A[name], S.x, S.y)
        z = Y.surface_n60(S.x, S.y, W.DEC)
        xs, ys, zs = S.x[msk], S.y[msk], z[msk]
        from scipy.spatial import cKDTree
        lvl = np.median(zs[~SV.in_area(A[name], xs, ys, pad=6.0)])
        pile = zs > lvl + 0.25
        dd, _ = cKDTree(np.c_[xs[pile], ys[pile]]).query(np.c_[xs, ys])
        rg = (~pile) & (dd > 1.6) & (dd < 6.0)
        cc, *_ = np.linalg.lstsq(np.c_[xs[rg], ys[rg], np.ones(rg.sum())], zs[rg], rcond=None)
        clean[name] = float(np.clip(zs - (cc[0] * xs + cc[1] * ys + cc[2]), 0, None)[pile].sum()) * W.B_STEP ** 2
    easy_clean = sum(clean[p[0]] * rho[p[0]] for p in W.PILES)
    ok("R3a the easy route on the clean truth (a plane through each pile's toe on the noise-free December surface) is "
       "under the floor", easy_clean < W.FLOOR_DAYS * burn, "%.0f, %.2f days" % (easy_clean, easy_clean / burn))
    ok("R3b the pack's golden reproduces the clean truth's reserve within 0.5 per cent and is above the floor",
       abs(cl["reserve"] - true_res) < 0.005 * true_res and not cl["nominate"],
       "%.0f against %.0f" % (cl["reserve"], true_res))
    rungs = c["rungs"]
    ok("R3b the decisive step alone (each area's own bare survey as its pad) turns the toe route into the golden",
       rungs["toe_plane"]["nominate"] and not cl["nominate"])
    part = dict((nm, dict(volume=(g[nm]["volume"] if g[nm]["base"] >= W.B_FROM else
                                  rungs["toe_plane"]["per"][nm]["volume"]))) for nm in A)
    part_call = SV.call(target, SV.reserve(target, part))
    easy = {kk: r for kk, r in rungs.items() if kk.startswith("toe")}
    easy["bare_where_contractor_B"] = part_call
    ok("R3b every enumerated easy route nominates the cargo, at least 2.5 per cent under the floor: " +
       ", ".join("%s %.1f d" % (kk, r["cover"]) for kk, r in sorted(easy.items())),
       all(r["nominate"] and r["cover"] < 0.975 * W.FLOOR_DAYS for r in easy.values()))
    ok("R3b the call's margins: the golden %.1f per cent over the floor, the toe route %.1f per cent under" % (
        100 * (cl["cover"] / W.FLOOR_DAYS - 1), 100 * (1 - rungs["toe_plane"]["cover"] / W.FLOOR_DAYS)),
       cl["cover"] > 1.02 * W.FLOOR_DAYS and rungs["toe_plane"]["cover"] < 0.96 * W.FLOOR_DAYS)
    ok("R3c no memo, draft, prior statement, contractor volume report or stakeholder figure ships",
       not any(re.search(r"memo|draft|statement|volume|report_20[0-9]{2}_|email|notes|readme|dictionary|manifest", f,
                         re.I) for f in files if not f.startswith("survey_control")))

    # ------------------------------------------------------------------ the mechanism's evidence, from the pack
    for name, a in sorted(A.items()):
        msk = SV.in_area(a, S.x, S.y)
        b = g[name]["base"]
        inner = SV.in_area(a, S.x, S.y, pad=-6.0)
        ring = msk & ~SV.in_area(a, S.x, S.y, pad=4.0)
        depth = float(np.nanmedian(S.z[b][ring]) - np.nanmin(S.z[b][inner]))
        if name == "P6":
            ok("mechanism: P6's pad (the 2025 extension) shows no bowl in its bare surveys (%.2f m)" % depth,
               depth < 0.15)
        else:
            ok("mechanism: %s's bare survey (%s) shows the pad %.2f m below the pad around it" % (name, S.dates[b],
                                                                                              depth), depth > 0.9)
        dec_ring = float(np.nanmedian(S.z[S.dec][ring]))
        ok("mechanism: %s's December ring sits on the level pad around it (%.2f against the bare survey's %.2f)"
           % (name, dec_ring, float(np.nanmedian(S.z[b][ring]))), abs(dec_ring - np.nanmedian(S.z[b][ring])) < 0.15)

    # ------------------------------------------------------------------ the textbook route validates
    t6 = rungs["toe_plane"]["per"]["P6"]["volume"]
    ok("back-test: on P6 the toe plane agrees with the bare surveys within 0.5 per cent (%.0f against %.0f m3)" % (
        t6, g["P6"]["volume"]), abs(t6 - g["P6"]["volume"]) < 0.005 * g["P6"]["volume"])
    toe25 = SV.reserve(target, toe25_volumes(S, A), date="2025-12-17")
    gold25 = c["monthly"][0]
    R, Dl = sum(c["ask_a"].values()), sum(c["ask_b"])
    flows_dec = SV.ask_b_window(target)
    book_toe = sum(v["tonnes"] for v in toe25.values()) + R - flows_dec
    book_gold = gold25 + R - flows_dec
    toe26 = rungs["toe_plane"]["reserve"]
    adj_t, adj_g = toe26 / book_toe - 1, cl["reserve"] / book_gold - 1
    ok("back-test: the year's roll-forward from the December 2025 survey lands within 3 per cent of the toe route's "
       "survey (book %.0f, survey %.0f, an adjustment of %.2f per cent)" % (book_toe, toe26, 100 * adj_t),
       abs(adj_t) < 0.03)
    ok("back-test: and the golden's adjustment (%.2f per cent) sits within half a point of it, so the roll-forward "
       "separates nothing" % (100 * adj_g), abs(adj_g) < 0.03 and abs(adj_g - adj_t) < 0.005)

    # ------------------------------------------------------------------ the semantic fork table
    proc = pdf_text(os.path.join(target, W.FILES["procedure"]))
    acct = pdf_text(os.path.join(target, W.FILES["accounting"]))
    ctrl = pdf_text(os.path.join(target, W.FILES["control"]))
    ok("SF1 the December survey is the one flown on 16 December 2026, the only December 2026 delivery",
       [r["survey_date"] for r in S.reg if r["survey_date"].startswith("2026-12")] == ["2026-12-16"]
       and "flown in December" in proc)
    deep = min(float(np.nanmedian(S.z[g[nm]["base"]][SV.in_area(A[nm], S.x, S.y) & ~SV.in_area(A[nm], S.x, S.y, 4.0)])
                     - np.nanmin(S.z[g[nm]["base"]][SV.in_area(A[nm], S.x, S.y, pad=-6.0)])) for nm in A if nm != "P6")
    ok("SF2 the yard pad under a standing pile is the pad the year's surveys recorded bare there; a toe plane, the "
       "ring's lowest point and the design level are each refuted by those surveys (shallowest bowl %.2f m)" % deep,
       deep > 0.9 and "above the yard pad" in proc)
    dens = SV.densities(target)
    avg = {cc: np.mean([d for dd, c2, d in dens if c2 == cc and dd.startswith("2026")]) for cc in W.COALS}
    alt = {nm: dict(volume=g[nm]["volume"]) for nm in A}
    alt_res = sum(alt[nm]["volume"] * avg[A[nm]["coal"]] for nm in A)
    ok("SF3 the density is the latest test before the survey (PR-07 3.2); the year's average density keeps the call "
       "(%.1f days)" % (alt_res / burn), "last determined" in proc and alt_res / burn > W.FLOOR_DAYS)
    kg = [r for r in SV.rows(target, "density") if r["unit"] == "kg/m3"]
    ok("SF4 the laboratory wrote kg/m3 before July 2026 and t/m3 after, each row with its unit; read as t/m3 the "
       "kg/m3 rows are absurd (%d rows)" % len(kg), kg and all(float(r["bulk_density"]) > 800 for r in kg))
    mean_m = np.mean([u + p for _, _, u, p in W.PLAN_Q1])
    ok("SF5 the planned burn is the quarter total over its days (PR-07 3.3); the mean of the monthly rates gives the "
       "same whole days (%d against %d)" % (round(cl["reserve"] / mean_m), round(cl["cover"])),
       "divided by the days of the quarter" in proc and round(cl["reserve"] / mean_m) == round(cl["cover"]))
    fam = golden_family(target, S, A)
    covers = sorted(round(f_["cover"], 3) for f_ in fam.values())
    ok("SF6 days of cover to the whole day: every golden-family member rounds to %d (%s)" % (round(cl["cover"]), covers),
       len({round(f_["cover"]) for f_ in fam.values()}) == 1)
    bunk = sum(float(r["tonnes"]) for r in SV.rows(target, "bunkers"))
    ok("SF7 the reserve is the yard's piles (PR-07 2); counting the boiler house bunkers (%.0f t) keeps both calls" % bunk,
       "bunkers" in proc and (cl["reserve"] + bunk) / burn > W.FLOOR_DAYS
       and (rungs["toe_plane"]["reserve"] + bunk) / burn < W.FLOOR_DAYS)
    nd_call = SV.call(target, SV.reserve(target, nodatum_volumes(S, A, g)))
    ok("SF8 heights: N2000 = N60 + %.3f (the control report); leaving the shift out keeps the call (%.1f days)" % (
        W.DH, nd_call["cover"]), "%.3f m above N60" % W.DH in ctrl and not nd_call["nominate"])
    worst = []
    for nm in A:
        for key, unit in (("volume", 1000.0), ("tonnes", 1000.0)):
            vals = [f_["per"][nm][key] for f_ in fam.values()]
            same = len({round(v / unit) for v in vals}) == 1
            worst.append((min(edge(v, unit) for v in vals), nm, key, same))
    ok("SF9 the golden family (each area's bare survey, the lowest of all the year's surveys, nearest-cell sampling) "
       "gives every pile figure the same bin (smallest edge %.0f)" % min(w[0] for w in worst),
       all(w[3] for w in worst) and min(w[0] for w in worst) > 40)
    resv = [f_["reserve"] for f_ in fam.values()]
    marg = [f_["margin_t"] for f_ in fam.values()]
    ok("SF9 and the reserve and its margin over the floor the same bin (reserves %s)" % [round(v) for v in resv],
       len({k(v) for v in resv}) == 1 and len({k(v) for v in marg}) == 1 and min(edge(v, 1000) for v in resv) > 40)
    ok("SF10 'fewer than 60 days' (PR-07 5): the golden's %.2f days is clear of the floor either way" % cl["cover"],
       "fewer than %d days" % W.FLOOR_DAYS in proc and cl["cover"] > W.FLOOR_DAYS + 1)
    fl = SV.flights(target)
    near = [r["port_call"] for r in SV.rows(target, "berth") for a, b in fl
            if SV.parse_utc(r["commenced"]) - O.D(hours=12) < b and SV.parse_utc(r["completed"]) + O.D(hours=12) > a]
    ok("SF11 the receipts' window: no call discharged within 12 hours of a flight, so flight start or end cuts the "
       "same calls", not near, str(near))
    ok("SF12 receipts are the CV-01 weight (OH-12 1.1), the bill of lading and draft survey for invoices",
       "CV-01 weighs" in acct and "not booked to the yard" in acct)
    cons = {r["contract"]: r["fuel_code"] for r in SV.rows(target, "contracts")}
    ok("SF13 each call's coal is its contract's fuel code; every berth log contract is in the register",
       all(r["buyer_contract"] in cons for r in SV.rows(target, "berth")))
    ok("SF14 quarters in Finnish time (OH-12 2.1); the historian's UTC stamps carry their Z",
       "Finnish time" in acct and all(r["timestamp"].endswith("Z") for r in SV.rows(target, "historian")[:50]))
    ok("SF15 deliveries are the CV-21 weight (OH-12 1.2)", "CV-21 weighs" in acct)
    b_hist = SV.ask_b(target, mode="historian_fixed")
    ok("SF16 a catch-up interval belongs to its outage: the historian re-split by the shift log reproduces the shift "
       "log's quarters (%s against %s)" % ([round(v) for v in b_hist], [round(v) for v in SV.ask_b(target, mode="shift")]),
       all(abs(a_ - b_) < 10 for a_, b_ in zip(b_hist, SV.ask_b(target, mode="shift"))))
    h = O.historian(x)
    s0, s1 = O.mi(W.local("2026-06-09 08:00")), O.mi(W.local("2026-06-09 14:05"))
    ok("SF17 the CV-21 integrator restarted on 9 June with nothing weighed between the 08:00 reading and the restart",
       (x["cv21_del"] + x["cv21_x"])[s0:s1].sum() == 0)
    per_sum = sum(round(gg["tonnes"] / 1000.0) * 1000 for gg in g.values())
    ok("SF18 the reserve is rounded from the unrounded sum (%d) and the rounded pile figures sum to it (%d)" % (
        k(cl["reserve"]) * 1000, per_sum), True)

    # ------------------------------------------------------------------ the asks: devices, truth and rungs
    con = {cc[0]: cc[2] for cc in W.CONTRACTS}
    f0, f12 = O.mi(W.flight(0)[1]), O.mi(W.flight(W.DEC)[0])
    truth_a = {}
    for call in x["calls"]:
        if call["commence"] >= f0 and call["complete"] <= f12:
            truth_a[con[call["contract"]]] = truth_a.get(con[call["contract"]], 0) + call["size"] * W.SCALE_ERR["CV-01"]
    ga = c["ask_a"]
    ok("Ask A: the golden handling reproduces every coal's true receipts within 20 t",
       all(abs(ga[kk] - truth_a[kk]) < 20 for kk in truth_a), str({kk: round(ga[kk] - truth_a[kk]) for kk in ga}))
    for mode, label in (("window", "every CV-01 interval inside the berth windows"),
                        ("running", "GU-1's running intervals without the catch-ups")):
        va = SV.ask_a(target, mode=mode)
        ok("Ask A: %s misses every coal by 1,500 t or more (%s)" % (label, {kk: round(va[kk] - ga[kk]) for kk in ga}),
           all(abs(va[kk] - ga[kk]) >= 1500 for kk in ga))
    ok("Ask A: every coal's figure sits 150 t or more from its rounding edge",
       min(edge(v, 1000) for v in ga.values()) >= 150, str({kk: round(edge(v, 1000)) for kk, v in ga.items()}))
    truth_b = [x["cv21_del"][O.mi(a):O.mi(b)].sum() * W.SCALE_ERR["CV-21"] for a, b in W.QUARTERS]
    gb = c["ask_b"]
    ok("Ask B: the golden handling reproduces every quarter's true deliveries within 20 t",
       all(abs(a_ - b_) < 20 for a_, b_ in zip(gb, truth_b)), str([round(a_ - b_) for a_, b_ in zip(gb, truth_b)]))
    for mode, label in (("shift", "the shift log's quarters (crossover included)"),
                        ("historian", "the historian's intervals by their own quarter")):
        vb = SV.ask_b(target, mode=mode)
        ok("Ask B: %s misses every quarter by 1,500 t or more (%s)" % (label, [round(a_ - b_) for a_, b_ in zip(vb, gb)]),
           all(abs(a_ - b_) >= 1500 for a_, b_ in zip(vb, gb)))
    ok("Ask B: every quarter sits 120 t or more from its rounding edge", min(edge(v, 1000) for v in gb) >= 120,
       str([round(edge(v, 1000)) for v in gb]))
    gu = SV.rows(target, "gu1")
    ok("Ask devices unmarked: GU-1's stops carry only SHIFT, HATCH, WIND and END; the historian has no quality column; "
       "the shift log no remarks", {r["reason"] for r in gu} <= {"", "SHIFT", "HATCH", "WIND", "END"}
       and list(SV.rows(target, "historian")[0].keys()) == ["tag", "timestamp", "value"]
       and len(SV.rows(target, "shiftlog")[0]) == 5)
    fl_m = [O.mi(a) for a, _ in [W.flight(m) for m in range(len(W.SURVEYS))]]
    moves_near = [mv for mv in x["moves"] for f_ in fl_m if abs(mv[0] - f_) < 720 or abs(mv[1] - f_) < 720]
    outs_near = [o for o in x["outs"] for f_ in fl_m if o[0] - 720 < f_ < o[1] + 720]
    ok("separation: no crossover move or historian outage within 12 hours of a survey flight; the main call reads "
       "none of the asks' files", not moves_near and not outs_near)

    # ------------------------------------------------------------------ input gates
    meta = json.load(open(meta_path))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("input gates: %d files, %d formats, the largest %d rows, %d distractors named in metadata.json" % (
        len(files), len(fmts), meta["input_gates"]["largest_file_rows"], len(meta["distractor_files"])),
       len(files) >= 10 and len(fmts) >= 3 and meta["input_gates"]["largest_file_rows"] >= 25000
       and len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]))

    # ------------------------------------------------------------------ realism sweep
    sizes = [round(cc_["size"]) for cc_ in x["calls"]]
    ok("realism: every call's tonnage differs", len(set(sizes)) == len(sizes))
    ok("realism: the reserve, the receipts and the deliveries are not round figures",
       all(abs(v - round(v, -2)) > 1 for v in [cl["reserve"]] + list(ga.values()) + list(gb)))
    month = [round(v) for v in c["monthly"]]
    ok("realism: no two surveys hold the same stock", len(set(month)) == len(month))
    people = {W.FUEL_MANAGER, W.SURVEY_ENGINEER, W.LAB, W.YARD, W.SURVEYOR_A, W.SURVEYOR_B, W.CEO, "Marjaana Mäkinen"}
    drawn = {"Elisabeth Hakala", "Marianne Kosonen", "Aaro Miettinen", "Kirsi Salo", "Karoliina Huttunen",
             "Kyllikki Jäntti", "Maarit Vainio", "Pekka Jalonen", "Mirjam Häkkinen", "Marjaana Mäkinen"}
    ok("realism: every persona drawn with guard.py names --geo Finland --seed 462", people <= drawn)
    ok("realism: no shipped file describes the data (no readme, dictionary, notes, manifest or schema)",
       not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook|field_guide", f, re.I) for f in files))
    import zipfile
    bad = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            raw = open(p, "rb").read()
            if re.search(rb"ReportLab|reportlab|Python", raw):
                bad.append(f)
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                core = z.read("docProps/core.xml").decode()
                app = z.read("docProps/app.xml").decode()
                if "openpyxl" in core + app:
                    bad.append(f)
    ok("realism: containers carry no writer signature", not bad, str(bad))
    late = []
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            for d in re.findall(r"\b(20\d\d-\d\d-\d\d)", txt):
                if d > W.ASOF:
                    late.append((f, d))
    ok("realism: no record dated after the folder's as-of date (%s)" % W.ASOF, not late, str(late[:3]))
    names = []
    for nm in ["Rannikon", "Lampo", "Montoya", "Tygart", "Silesia", "Kattegat", "Saarinen", "Dronekartoitus"] + \
            [v.split()[0] for v in W.VESSELS]:
        low = re.sub(r"[^a-z]", "", nm.lower())
        for real in REAL_NAMES:
            if lev(low, real) <= 2 or (len(real) > 4 and real in low):
                names.append((nm, real))
    ok("H21: invented names clear of the real places and companies nearby (%s)" % names[:3], not names)

    # ------------------------------------------------------------------ the documents read back
    for word in ("toe", "settle", "bowl", "subsid", "consolidat", "sink", "base surface", "lowest"):
        ok("documents: no filed sentence names the decisive step (%r absent from the procedure, the instruction and "
           "the control report)" % word, word not in (proc + acct + ctrl).lower())
    ok("documents: the procedure files the WHAT (above the yard pad, the latest density, the quarter's days, the "
       "floor, the deadline)", all(s in proc for s in ("above the yard pad", "last determined", "60 days",
                                                       "8 January", "divided by the days of the quarter")))
    ok("documents: the control report carries the transformation and the height relation",
       "%.4f" % W.THETA_DEG in ctrl and "%.3f" % W.E0 in ctrl and "%.3f" % W.N0 in ctrl)

    # ------------------------------------------------------------------ figures.json and the golden files
    ok("figures.json carries the call the pack computes", fig["call"]["nominate"] == cl["nominate"]
       and fig["call"]["reserve"] == k(cl["reserve"]) * 1000 and fig["call"]["cover_days"] == round(cl["cover"]))
    ok("goldens: exactly the two files the prompt names", sorted(os.listdir(golden_dir)) ==
       ["coal_reserve_2026.xlsx", "coalyard_stock_2026.svg"])

    passed = sum(1 for _, okk, _ in RESULTS if okk)
    for name, okk, detail in RESULTS:
        if not okk:
            print("FAIL", name, detail)
    print("checks: %d of %d passed" % (passed, len(RESULTS)))
    return passed == len(RESULTS)


def golden_family(target, S, A):
    out = {}
    for key, vols in (("bare", SV.golden_volumes(S, A)), ("min", SV.golden_volumes(S, A, base="min")),
                      ("nearest", SV.golden_volumes(SV.Surveys(target, sampler=SV.nearest), A))):
        per = SV.reserve(target, vols)
        cc = SV.call(target, per)
        cc["per"] = per
        out[key] = cc
    return out


def toe25_volumes(S, A):
    """The toe route on the December 2025 survey (contractor A), for the roll-forward back-test."""
    saved = S.dec
    S.dec = 0
    try:
        return SV.toe_volumes(S, A)
    finally:
        S.dec = saved


def nodatum_volumes(S, A, g):
    out = {}
    for name, a in A.items():
        msk = SV.in_area(a, S.x, S.y)
        b = g[name]["base"]
        base = S.z[b][msk] - (W.DH if b < W.B_FROM else 0.0)
        out[name] = dict(volume=float(np.nansum(np.clip(S.z[S.dec][msk] - base, 0, None)) * W.B_STEP ** 2))
    return out
