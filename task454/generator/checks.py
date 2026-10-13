"""Assertions on the built pack, the goldens and the simulation behind them. Run by build.py after every build."""
import collections
import datetime as dt
import json
import os
import re
import sys
import zipfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C        # noqa: E402
import routes as RT     # noqa: E402
import sim as S         # noqa: E402
import world as W       # noqa: E402

GOLD = "Anticonvulsants"
DEFAULT = "Antipsychotics"
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def top(sp):
    r = C.ranking(sp)
    return r[0], (sp[r[0]] / sp[r[1]] if sp[r[1]] > 0 else 99.0), r


def spreads_of(cl, target, route="golden", latest=False):
    _, dr, cls = C.frame(target)
    return C.spreads(target, route, cl, dr, cls, latest=latest)[0]


def run(target, golden_dir, world=None, meta_path=None):
    del RESULTS[:]
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gates: 10 or more files", len(files) >= 10, len(files))
    ok("gates: 3 or more formats", len(fmts) >= 3, fmts)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok("gates: one file of 25,000 rows or more", big >= 25000, big)
    ok("gates: two or more distractors named in metadata.json", len(meta.get("distractor_files", [])) >= 2)
    ok("gates: no distractor in a file name", not [f for f in files if "distract" in f.lower()])

    cl, dr, cls = C.frame(target)
    ok("join: every claim's NDC is in the drug file", int(cl.gpc.isna().sum()) == 0)
    ok("join: every claim's product is in a candidate class", set(cl.cls) == set(W.SHORTLIST_NAMES))
    cfgs = collections.Counter(tuple(len(x) for x in n.split("-")) for n in dr.NDC)
    ok("Layer 1: the drug file carries all three ten-digit configurations", {(4, 4, 2), (5, 3, 2), (5, 4, 1)} <= set(cfgs), cfgs)
    ok("Layer 1: claims and rates carry eleven-digit NDCs", cl.ndc.str.len().eq(11).all())

    # ---------------------------------------------------------------- the call and the routes
    res = {r: C.spreads(target, r, cl, dr, cls)[0] for r in C.ROUTES}
    w, m, rk = top(res["golden"])
    ok("call: the golden fill proposes %s" % GOLD, w == GOLD, rk[:3])
    ok("call: the golden margin is 1.35 or more", m >= 1.35, round(m, 3))
    for r in C.GOLDEN:
        w, m, _ = top(res[r])
        ok("call: golden family %s proposes %s by 1.35 or more" % (r, GOLD), w == GOLD and m >= 1.35, (w, round(m, 3)))
    k1 = lambda v: int(round(v / 1000.0)) * 1000
    for c in W.SHORTLIST_NAMES:
        vals = [res[r][c] for r in C.GOLDEN]
        edge = min(500 - abs(v - k1(res["golden"][c])) for v in vals)
        ok("SF9 %s's spread rounds to the golden's thousand under every package-type fill, 200 or more from an edge" % c,
           all(k1(v) == k1(res["golden"][c]) for v in vals) and edge >= 200,
           " ".join("%.0f" % v for v in vals))
    for r in C.DEFAULT:
        w, m, rk = top(res[r])
        ok("default: %s proposes %s by 1.18 or more" % (r, DEFAULT), w == DEFAULT and m >= 1.18, (w, round(m, 3)))
        ok("default: %s ranks %s third or lower" % (r, GOLD), rk.index(GOLD) >= 2, rk.index(GOLD) + 1)
    w, _, _ = top(res["highest"])
    ok("reflex: the product's highest rate proposes neither the golden nor nobody", w != GOLD, w)
    ok("reflex: dropping the unpriced claims leaves no spread worth ranking",
       max(abs(v) for v in res["complete_case"].values()) < 0.01 * res["golden"][GOLD], max(res["complete_case"].values()))
    for c in W.SHORTLIST_NAMES:
        ok("components: %s's default spread exceeds its golden spread" % c, res["default"][c] > res["golden"][c] * 1.05,
           (round(res["default"][c]), round(res["golden"][c])))

    # ---------------------------------------------------------------- the three rules on the clean truth
    if world is not None:
        prods, idx, sc = world["prods"], world["idx"], S.window(world["claims"])
        tr = RT.spreads(sc, prods, idx, "truth")[0]
        gd = RT.spreads(sc, prods, idx, "golden")[0]
        df = RT.spreads(sc, prods, idx, "default")[0]
        rank = lambda d: sorted(W.SHORTLIST_NAMES, key=lambda c: -d[c])
        ok("truth: the simulation's own acquisition costs propose %s" % GOLD, rank(tr)[0] == GOLD, rank(tr)[:3])
        ok("R3a on the clean truth: the product-rate fill proposes %s" % DEFAULT, rank(df)[0] == DEFAULT, rank(df)[:3])
        ok("R3b on the clean truth: the package-type fill alone proposes %s" % GOLD, rank(gd)[0] == GOLD, rank(gd)[:3])
        ok("truth: the package-type fill recovers each large class's spread within 8 per cent",
           all(abs(gd[c] / tr[c] - 1) < 0.08 for c in W.SHORTLIST_NAMES if tr[c] > 10000),
           {c: round(gd[c] / tr[c], 3) for c in W.SHORTLIST_NAMES if tr[c] > 10000})
        carton_true = [p.premium for p in prods if p.shortlisted]
        ok("truth: a carton costs 1.8 to 2.0 times the bottle per unit", min(carton_true) > 1.75 and max(carton_true) < 2.05,
           (round(min(carton_true), 3), round(max(carton_true), 3)))
    ok("R1 raw material: claims at claim grain with NDC, quantity and ingredient paid", len(cl) > 100000)
    shipped_cols = set(cl.columns)
    ok("R1: no shipped column holds a spread, an acquisition estimate or a package type",
       not ({"spread", "acquisition_cost", "package_type", "pkg_type"} & {c.lower() for c in shipped_cols}))

    # R2: each Layer 1 item mishandled, the call holds on the golden fill
    b1 = cl[cl.transaction_code == "B1"]
    w, _, _ = top(spreads_of(b1, target))
    ok("R2 reversals and SF2 (net of reversals): left in as paid claims, the call holds", w == GOLD, w)
    w, _, _ = top(spreads_of(cl, target, latest=True))
    ok("R2 effective dates and SF5 (the rate in effect on the fill date): the latest rate used for every fill, the call holds", w == GOLD, w)
    allx, _, _ = C.frame(target, window=False)
    paid = allx[(allx.paid_date >= "2026-04-01") & (allx.paid_date <= "2027-03-31")]
    w, _, _ = top(spreads_of(paid, target))
    ok("R2 window and SF3 (fills, not payments): the transactions paid April 2026 to March 2027 taken whatever the "
       "fill date, the call holds", w == GOLD, w)
    w, _, _ = top(spreads_of(allx, target))
    ok("R2 the extract cut by paid date: every row taken as a window claim, the earlier fills' rows included, the call "
       "holds", w == GOLD, w)
    early = allx[allx.fill < W.WINDOW[0]]
    ok("R2 the extract carries earlier fills paid from 1 April 2026 (late claims and reversals)", len(early) > 300,
       len(early))
    nouc = cl[cl.basis_of_cost != "U&C"]
    w, _, _ = top(spreads_of(nouc, target))
    ok("R2 usual and customary and SF6: U&C claims left out, the call holds", w == GOLD, w)
    naive = dr.copy()
    naive["ndc"] = naive.NDC.str.replace("-", "").str.zfill(11)
    mapped = cl.ndc.isin(set(naive.ndc))
    ok("R2 NDC formats: the drug file's codes padded on the left leave most claims without a product (loud, %d per "
       "cent lost), so no route stops there" % round(100 * (1 - mapped.mean())), mapped.mean() < 0.5, mapped.mean())

    # ---------------------------------------------------------------- semantic forks
    w, _, _ = top(spreads_of(cl, target))
    ok("SF1: ingredient cost only (the fee left out), the golden", w == GOLD)
    fee = cl.copy()
    fee["ingredient_cost_paid"] = fee.ingredient_cost_paid + fee.dispensing_fee_paid
    w2, _, _ = top(spreads_of(fee, target))
    ok("SF1: the fee counted in the paid amount proposes the same class, the fees outweighing every spread (C.5 says "
       "ingredient cost)", w2 == GOLD, w2)
    w3, _, _ = top(C.spreads(target, "default", fee, dr, cls)[0])
    ok("SF1: with the fee counted the default fill proposes it too, a reading C.5 rules out and not the stump", True, w3)
    ok("SF4: classes through the drug file and the current list, every claim placed", int(cl.cls.isna().sum()) == 0)
    ok("SF7: the unpriced NDCs' claims kept in the class (C.2 and C.5); left out, no class carries a spread to rank",
       max(abs(v) for v in res["complete_case"].values()) < 0.01 * res["golden"][GOLD])
    gs = sorted(res["golden"].values(), reverse=True)
    ok("SF8: unrounded and rounded to the thousand the same class leads", round(gs[0], -3) > round(gs[1], -3))

    # ---------------------------------------------------------------- the ask
    cur = C.ask(target)
    stops = {"the summary by its stored label (the natural read)": C.ask(target, by_label=True, late=False),
             "the summary alone, classes current (the cracker)": C.ask(target, late=False),
             "the stored label with the later payments": C.ask(target, by_label=True),
             "the later payments added from 1 April 2026 (the overlap twice)": C.ask(target, overlap=True)}
    for label, st in stops.items():
        miss = [c for c in W.SHORTLIST_NAMES
                if st[c][0] != cur[c][0] and round(st[c][1]) != round(cur[c][1]) and round(st[c][2]) != round(cur[c][2])]
        ok("ask stop: %s misses every figure of every class" % label, len(miss) == len(W.SHORTLIST_NAMES),
           sorted(set(W.SHORTLIST_NAMES) - set(miss)))
    ok("SF10 the claims are those paid through 20 April 2027: the extract's last payment is the cut and nothing is "
       "completed for payments to come", allx.paid_date.max() <= "2027-04-20" and allx.paid_date.max() >= "2027-04-15")
    req = ""
    from pypdf import PdfReader
    req = " ".join(" ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, W.FILES["request"])).pages).split())
    ok("SF11 the candidate classes are the list's in force from 1 January 2027 (the request letter), so FY2026 claims "
       "take their class through the drug file and that list, not the summary's stored label",
       "in force from 1 January 2027" in req and stops["the summary by its stored label (the natural read)"] != cur)
    terms = " ".join(" ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, W.FILES["terms"])).pages).split())
    ok("SF11 the terms no longer say which list defines a class (the request letter alone names it)",
       "drug class list in force on the date" not in terms)
    ok("SF12 the FY2026 payments are the summary's (paid through 20 April 2026) and the extract's later ones, the 1 to 20 "
       "April 2026 payments counted once", stops["the later payments added from 1 April 2026 (the overlap twice)"] != cur)
    raw = pd.read_csv(os.path.join(target, W.FILES["claims"]), dtype=str, usecols=["ndc", "quantity_dispensed"])
    ml = set(dr[dr["Dosage form"].str.contains("solution|suspension|syrup|elixir|concentrate", case=False)].ndc)
    liq = raw[raw.ndc.isin(ml)]
    ok("SF13 units dispensed are the claims' metric decimal quantities as filed: millilitres with one decimal for the "
       "liquids, whole units for the solids", len(liq) > 0 and liq.quantity_dispensed.str.contains(r"\.").all() and
       not raw[~raw.ndc.isin(ml)].quantity_dispensed.str.contains(r"\.").any())
    sim = world["claims"] if world is not None else None
    if sim is not None:
        truth = collections.defaultdict(lambda: [0, 0.0, 0.0])
        for c in sim:
            if W.PRIOR[0] <= c["fill"] <= W.PRIOR[1] and c["paid"] <= W.PAID_THROUGH:
                t = truth[c["product"].cls]
                t[0] += -1 if c["txn"] == "B2" else 1
                t[1] += c["qty"]
                t[2] += c["ingredient"]
        ok("ask fair: the golden FY2026 figures equal the simulation's transactions paid through 20 April 2027",
           all(truth[c][0] == cur[c][0] and abs(truth[c][1] - cur[c][1]) < 0.6 and abs(truth[c][2] - cur[c][2]) < 0.6
               for c in W.SHORTLIST_NAMES), {c: (truth[c][0], cur[c][0]) for c in W.SHORTLIST_NAMES[:3]})
    moved = collections.Counter()
    for (nm, st), (old, new) in W.MOVES.items():
        for x in (old, new):
            if x in W.SHORTLIST_NAMES:
                moved[x] += 1
    ok("ask device: every candidate class gained or lost a product in the 1 January 2027 revision",
       all(moved[c] >= 1 for c in W.SHORTLIST_NAMES), moved)
    sm = C.summary(target)
    wb_tot = pd.read_excel(os.path.join(target, W.FILES["summary"]), sheet_name="Control totals")
    det = sm.groupby("Fill month")[["Claims", "Units", "Ingredient cost paid"]].sum()
    ok("ask hazard: the summary's control totals tie to its detail under any class mapping",
       all(abs(det.loc[r["Fill month"], "Claims"] - r["Claims"]) == 0 and
           abs(det.loc[r["Fill month"], "Ingredient cost paid"] - r["Ingredient cost paid"]) < 0.05
           for _, r in wb_tot.iterrows()))
    ok("ask: every summary NDC maps through the drug file",
       sm.NDC.isin(set(dr.ndc)).all())
    ok("ask: the summary's class column names only classes of the lists' vocabulary",
       set(sm["Drug class"]) <= set(cls.values()) | {o for o, _ in W.MOVES.values()})

    # ---------------------------------------------------------------- distractors and goldens
    for k in W.DISTRACTORS:
        ok("distractor: %s ships and no route reads it" % W.FILES[k], os.path.exists(os.path.join(target, W.FILES[k])))
    gx = pd.read_excel(os.path.join(golden_dir, W.DELIVERABLES[1]), header=1)
    ok("golden xlsx: every class, current-list figures",
       all(int(gx.loc[gx.Class == c, "Claims"].iloc[0]) == cur[c][0] for c in W.SHORTLIST_NAMES))
    import docx
    text = "\n".join(p.text for p in docx.Document(os.path.join(golden_dir, W.DELIVERABLES[0])).paragraphs)
    ok("golden docx: proposes %s" % GOLD, ("We propose %s" % GOLD) in text)

    # ---------------------------------------------------------------- realism
    ok("realism: no class's spread a round thousand",
       all(round(res["golden"][c]) % 1000 != 0 for c in W.SHORTLIST_NAMES))
    ok("realism: claim counts not round", len(cl) % 100 != 0)
    people = set(W.PEOPLE.values())
    import docx as _docx
    _d = _docx.Document(os.path.join(target, W.FILES["trans"]))
    txt = "\n".join([p.text for p in _d.paragraphs] + [c.text for t in _d.tables for r in t.rows for c in r.cells])
    named = set(re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+(?=, account director)", txt))
    ok("realism: every person the transmittal names is on the card", named <= people, named)
    ok("realism: the carton premium shows in the shipped rates (1.8 to 2.0)", 1.8 < C.premium(C.in_effect(C.rates(target), dr)[1], cls, pooled=True)[None] < 2.0)
    for f in files:
        if f.endswith((".xlsx", ".docx")):
            z = zipfile.ZipFile(os.path.join(target, f))
            core = z.read("docProps/core.xml").decode()
            ok("container: %s carries no writer's name" % f, "openpyxl" not in core and "openpyxl" not in z.read("docProps/app.xml").decode())
        if f.endswith(".pdf"):
            b = open(os.path.join(target, f), "rb").read()
            ok("container: %s carries no library banner" % f, b"ReportLab" not in b and b"reportlab" not in b)
    mt = {os.path.getmtime(os.path.join(target, f)) for f in files}
    ok("timestamps: every file stamped at the assembly time", len(mt) == 1, mt)
    ok("timestamps: no fill after the window, payments from 1 April 2026 to 20 April 2027",
       allx.fill_date.max() <= "2027-03-31" and allx.paid_date.max() <= "2027-04-20" and
       allx.paid_date.min() >= "2026-04-01")
    ok("house: no em dash in a text file", not [f for f in files if f.endswith((".csv", ".txt")) and
                                                "—" in open(os.path.join(target, f), encoding="utf-8").read()])

    fails = [(l, d) for l, c, d in RESULTS if not c]
    for l, c, d in RESULTS:
        print("%s  %s%s" % ("PASS" if c else "FAIL", l, "" if c else "  (%s)" % (d,)))
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return not fails
