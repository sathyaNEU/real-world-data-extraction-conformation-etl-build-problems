"""Assertions on the built pack and the world it came from: the three rules executed (the easy routes file the named
wrong book on the pack, the decisive step files the golden, the world's own 2027 agrees), the standing family and its
bins, the ladder, every semantic fork row (SF1 to SF20), the Layer 1 items moving nothing, the ask devices and their
stops, the pair ceiling, separation and the input gates.

    python3 task304/generator/checks.py <target dir>
"""
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pair
import params as P
import solve as S
import world as W

FTB, HLTV, SO, BTL = P.ORDER
F = P.FILES
# the figures the design note states, asserted against the pack
NOTE = None
N = 0


def ok(cond, msg):
    global N
    if cond:
        N += 1
    else:
        FAILED.append(msg)
        print("FAIL", msg, flush=True)


FAILED = []


def ten(v):
    return int(round(v / 10.0) * 10)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def r1(d):
    return {P.SHORT[k]: round(v, 1) for k, v in d.items()}


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def truth_2027(seed=P.SEED):
    """the clean truth: the world carried on through 2027, each book's first entries among the accounts on the book at
    30 September 2026 that are not with the recoveries team"""
    w = W.World(seed).run()
    pop = (w.status == 0) & (w.orig_m <= W.SNAP) & ~w.lit
    first = np.full(w.n, -1)
    rng = np.random.default_rng(seed + 1000)
    prev = w.k.copy()
    for m in range(W.SNAP + 1, W.ym(2027, 12) + 1):
        w.step(m, rng)
        hit = pop & (first < 0) & (w.k >= 2) & (prev < 2) & (m >= W.ym(2027, 1))
        first[hit] = m
        prev = w.k.copy()
    ext = pop & (w.ext_m >= W.ym(2026, 1))
    return ({P.BOOKNAME[b]: int(((first >= 0) & (w.book == j)).sum()) for j, b in enumerate(P.BOOKS)},
            int(((first >= 0) & ext).sum()))


def without(target, keys):
    """a copy of the pack with the named files removed"""
    d = tempfile.mkdtemp()
    for f in os.listdir(target):
        if f not in [F[k] for k in keys]:
            shutil.copy(os.path.join(target, f), os.path.join(d, f))
    return d



def realism(target, ok):
    """the realism sweep and the three rules executed (dataset-generation sections 7 and 7.1)"""
    import pyarrow.parquet as pq
    h = pd.read_parquet(os.path.join(target, F["history"]),
                        columns=["account_number", "book", "period", "arrears_balance", "account_status"])
    live = h[h.account_status == "Live"].drop_duplicates()
    cnt = live.groupby(["book", "period"]).size().unstack(0).loc["2024-01":]
    runs = (cnt.diff().iloc[1:] == 0).sum()
    ok(int(runs.max()) <= 2, "realism: no book's live count repeats month on month (%d)" % int(runs.max()))
    bk = pd.read_parquet(os.path.join(target, F["book"]), columns=["book"])
    sizes = bk.book.value_counts()
    ok(all(v % 100 for v in sizes), "realism: no book holds a round number of accounts")
    a = h[(h.period >= "2024-01") & (h.arrears_balance > 0)].drop_duplicates()
    paths = a.sort_values(["account_number", "period"]).groupby("account_number").apply(
        lambda d: tuple(zip(d.period, d.arrears_balance.round(2))))
    long_paths = paths[paths.map(len) >= 4]
    ok(long_paths.duplicated().sum() == 0, "R3c: no account's arrears path is a copy of another's")
    ct = pd.read_csv(os.path.join(target, F["contacts"]))
    ok(ct.groupby("contact_reason").calls_answered.nunique().min() >= 10, "realism: contact volumes move month to month")
    lit = pd.read_csv(os.path.join(target, F["litigation"]), dtype=str)
    blocks = lit.groupby("claim_number").action.apply(tuple)
    ok(blocks.value_counts().iloc[0] < 0.5 * len(blocks), "realism: no one action sequence makes up half the claims")
    names = set(open(os.path.join(target, F["dictionary"])).read().split(","))
    ok(not any(w in " ".join(names).lower() for w in ("extension", "extended", "forborne", "concession", "charter")),
       "R1: no field names the term increase")
    cols = set()
    for f in os.listdir(target):
        if f.endswith(".parquet"):
            cols |= set(pq.read_schema(os.path.join(target, f)).names)
        elif f.endswith(".csv"):
            cols |= set(pd.read_csv(os.path.join(target, f), nrows=1).columns)
    ok(not any(k in c for c in cols for k in ("ext", "forb", "conc", "charter", "hazard", "risk")),
       "R1: no shipped column holds the deciding quantity")
    ok(pq.ParquetFile(os.path.join(target, F["history"])).metadata.num_rows >= 25000,
       "R1: the account-month history the forecast runs on ships")


def main(target, quick=False):
    out = {}
    H, B = S.load(target)
    g = S.main_call(target, H, B)
    rates, av = g["rates"], g["avoided"]
    out["golden"] = r1(av)
    out["entries"] = {P.SHORT[k]: round(v, 1) for k, v in g["entries"].items()}
    ok(g["book"] == FTB, "R3b: the decisive step alone (the term increase as a state) files the first-time buyer book")
    ok(ten(av[FTB]) == 10 and av[HLTV] < 5 and av[SO] < 5 and av[BTL] < 5, "the golden's bins")
    ok(edge(av[FTB], 10) > 2 and 5 - av[HLTV] > 0.4, "the golden's figures sit inside their bins")
    order = sorted(P.ORDER, key=lambda b: -av[b])
    ok(order[1] == HLTV, "High LTV is the next best")
    # ---- R1 executed: the easy routes on the pack file High LTV; the ladder's lower rungs too --------------------------
    easy = {}
    for label, kw in S.EASY:
        r = S.main_call(target, H, B, **kw)
        easy[label] = r1(r["avoided"])
        ok(r["book"] == HLTV, "R3a: easy route %s files High LTV" % label)
        ok(r["avoided"][FTB] < 5 and r["avoided"][HLTV] < 5, "easy route %s bins" % label)
    out["easy"] = easy
    st, pc = S.rung_stock(H, B, rates), S.rung_pace(H, rates)
    out["R0"], out["R1"] = r1(st), r1(pc)
    ok(max(st, key=st.get) == HLTV and max(pc, key=pc.get) == HLTV, "the stock and this year's pace file High LTV")
    # ---- the standing family: every member files the first-time buyer book in the 10 bin, High LTV under 5 -------
    fam = {}
    if not quick:
        for label, kw in S.FAMILY:
            r = S.main_call(target, H, B, **kw)
            fam[label] = round(r["avoided"][FTB], 1)
            ok(r["book"] == FTB, "family member %s files the first-time buyer book" % label)
            ok(ten(r["avoided"][FTB]) == 10, "family member %s: first-time buyer in the 10 bin (%.1f)" % (label, r["avoided"][FTB]))
            ok(r["avoided"][HLTV] < 5, "family member %s: High LTV under 5" % label)
        out["family"] = fam
        out["family_range"] = [min(fam.values()), max(fam.values())]
        out["family_n"] = len(fam)
    # ---- the world's own 2027 agrees with the golden's direction -----------------------------------------------------
    if not quick:
        tr, tr_ext = truth_2027()
        tav = {b: P.EFFECT * tr[b] * rates[b] for b in P.ORDER}
        out["truth_avoided"] = r1(tav)
        ok(max(tav, key=tav.get) == FTB, "the world's own 2027 files the first-time buyer book")
        ok(tr_ext > 0.5 * tr[FTB], "the extended accounts carry most of the first-time buyer book's 2027 entries")
    # ---- R3: no field marks an extension; the plan files no method --------------------------------------------------
    hist_cols = list(pd.read_parquet(os.path.join(target, F["history"])).columns)
    ok(not any(re.search(r"ext|forb|charter|concession|flag", c, re.I) for c in hist_cols), "no column marks a concession")
    plan = pdf_text(os.path.join(target, F["plan"]))
    ok("extension" not in plan.lower() and "charter" not in plan.lower(), "the plan names no extension")
    # ---- Layer 1 items move nothing -------------------------------------------------------------------------------
    if not quick:
        Hd, Bd = S.load(target, dedupe=False)
        ok(S.main_call(target, Hd, Bd)["book"] == FTB, "R2: the re-sent month rows kept: same call")
        fx, fd = S.ext_facts(H, B), S.ext_facts(Hd, Bd)
        ok(all(fx[k] == fd[k] for k in ("ftb_raised_2026", "raised_2024", "behind_8m", "behind_by_asof"))
           and all(round(fx[k]) == round(fd[k]) for k in ("years_added_median", "pay_rise_extended", "pay_rise_kept")),
           "the re-sent month rows kept: the term increase facts unchanged")
        Hs, Bs = S.load(target, strip=False)
        ok(S.main_call(target, Hs, Bs)["book"] == FTB, "R2: product codes read with their dashes: same call")
        Hb, _ = S.load(target, extra=("balance",))
        same = Hb.account_number.eq(Hb.account_number.shift()).to_numpy()
        cap = same & (Hb.balance.to_numpy() > np.where(same, Hb.balance.shift().fillna(0), 0) + 1)
        capped = set(Hb.account_number[cap])
        out["capitalised_accounts"] = len(capped)
        ok(len(capped) > 50, "capitalisations present")
        r = S.main_call(target, H[~H.account_number.isin(capped)], B)
        ok(r["book"] == FTB, "R2: capitalised accounts out of the fit: same call")
    # ---- SF rows ---------------------------------------------------------------------------------------------------
    policy = pdf_text(os.path.join(target, F["policy"]))
    pilot = pdf_text(os.path.join(target, F["pilot"]))
    ok("for the whole of 2027" in plan and "during 2027" in plan, "SF1: calendar 2027 filed")
    ok("rounded down" in policy and "Payments in arrears is the arrears balance" in policy and "section 2 of the Arrears" in plan, "SF2: payments in arrears filed")
    if not quick:
        r = S.main_call(target, H, B, once=False)
        out["SF3_every_entry"] = r1(r["avoided"])
        ok(r["book"] == FTB, "SF3: every entry counted, same call")
    ok("in the first month of the year it does so" in plan, "SF3: once, filed")
    first_period = pd.read_parquet(os.path.join(target, F["history"]), columns=["account_number", "period"]).groupby("account_number").period.min()
    ok(first_period.max() <= "2026-08", "SF4: no account opened after the book's date")
    ok("The book is the accounts on it at 30 September 2026" in plan, "SF4: filed")
    ok("with no allowance for accounts that close during the year" in plan, "SF21: filed")
    if not quick:
        r = S.main_call(target, H, B, attrition=True)
        out["SF21_closures_netted"] = r1(r["avoided"])
        ok(r["book"] == FTB, "SF21: accounts netted for closing first, same call")
    if not quick:
        r = S.main_call(target, H, B, recoveries_out=False)
        ok(r["book"] == FTB, "SF5: recoveries accounts kept in, same call")
    ok("already in litigation or with a receiver appointed at that date are left with the recoveries team" in plan, "SF5 filed")
    # SF6: the printed planning rates reproduce from the history and the register
    E = S.entries_table(H)
    lo, hi = 2022 * 12, 2025 * 12 + 2
    e1 = E[(E.m >= lo) & (E.m <= hi)].groupby("account_number").first().reset_index()
    reg = S.register(target)
    pm = reg.groupby("account_number").date.min()
    pmm = e1.account_number.map(pm)
    pmm = pmm.dt.year * 12 + pmm.dt.month - 1
    e1["y"] = (pmm >= e1.m) & (pmm - e1.m <= 18)
    rec = e1.groupby("book").y.mean()
    for b in P.ORDER:
        ok(abs(round(100 * rec[b], 1) - round(100 * rates[b], 1)) < 1e-9, "SF6: %s planning rate reproduces" % b)
    ok("%d per cent of its expected 2027 borrowers taken on times its planning rate" % round(100 * P.EFFECT) in plan,
       "SF7: the effect filed")
    adj = {b: av[b] / P.EFFECT * 0.5 for b in P.ORDER}
    ok(max(adj, key=adj.get) == FTB, "SF7: another effect size scales every book alike, same call")
    ok(all(abs(av[b] - round(av[b])) > 1e-6 for b in P.ORDER), "SF8: possessions avoided are expected values")
    ok(all(ten(P.EFFECT * round(g["entries"][b]) * rates[b]) == ten(av[b]) for b in P.ORDER),
       "SF8: whole borrowers taken on give the same figures")
    ok(order[1] == sorted(P.ORDER, key=lambda b: -g["entries"][b])[1], "SF9: the next best on the pool too")
    ok(max(g["entries"].values()) < 1900 and "1,900 new cases a year" in plan, "SF10: capacity never binds")
    for b in P.ORDER:
        ok(ten(P.EFFECT * round(g["entries"][b], -1) * rates[b]) == ten(av[b]), "SF11: rounding path, %s" % b)
    # ---- the asks: golden values, the stops, the devices, the pair ---------------------------------------------------
    A = pair.lit_stops(target)
    Bst = pair.loss_stops(target)
    out["askA"] = {k: {P.SHORT[b]: [v[b]["orders"], v[b]["suspended"], v[b]["open"]] for b in P.ORDER[:3]}
                   for k, v in A.items() if k != "snapshot_stage_open"}
    out["askA_snapshot"] = {P.SHORT[b]: v for b, v in A["snapshot_stage_open"].items()}
    out["askB"] = {k: {P.SHORT[b]: [v[b]["sold"], v[b]["at_loss"], None if v[b]["avg_loss"] != v[b]["avg_loss"]
                                    else int(round(v[b]["avg_loss"] / 100.0) * 100)] for b in P.ORDER[:3]}
                   for k, v in Bst.items()}
    gA, gB = A["golden"], Bst["golden"]
    ok("A claim stays open until it is withdrawn, the order is discharged or set aside, or the property is taken into possession" in policy, "SF12 filed")
    ok("A possession order stays in force until it is varied (the new order takes its place)" in policy, "SF13 filed")
    lit = pd.read_csv(os.path.join(target, F["litigation"]), dtype={"account_number": str})
    ok(len(lit) > lit.drop_duplicates(["claim_number", "action_date", "action", "detail"]).shape[0], "SF14: per-defendant lines present")
    bk_of = S.account_books(target)
    ok(not (lit.account_number.map(bk_of) == BTL).any(), "SF15: no buy-to-let claim in the litigation file")
    ok("any surplus" not in policy and "the surplus is paid to the borrower and the loss is nil" in policy, "SF17 filed")
    dic = pd.read_csv(os.path.join(target, F["dictionary"]))
    ok(dic.description.str.contains("a corrected statement is re-sent in full with the next number").any(), "SF18 filed")
    import pyarrow.parquet as pq
    for f in sorted(os.listdir(target)):
        if f.endswith(".parquet"):
            cols = pq.read_schema(os.path.join(target, f)).names
        elif f.endswith(".csv") and f != F["dictionary"]:
            cols = pd.read_csv(os.path.join(target, f), nrows=1).columns.tolist()
        else:
            continue
        ok(dic[dic.file == f].field.tolist() == cols, "H9: the dictionary lists every field of %s in order" % f)
    ok("one of our four lending books" in plan, "SF19: the four books named")
    for b in P.ORDER[:3]:
        gv = gB[b]
        ok(gv["sold"] > 0 and edge(gv["avg_loss"], 100) > 20, "ask B %s average loss sits inside its bin" % b)
    sales_raw = pd.read_csv(os.path.join(target, F["sales"]))
    ok([c for c in sales_raw.columns if "date" in c] == ["completion_date"], "SF16: one date on a sale")
    two = sales_raw[sales_raw.statement == 2]
    one = sales_raw[sales_raw.statement == 1].set_index("sale_ref")
    ok((two.set_index("sale_ref").completion_date == one.completion_date.reindex(two.sale_ref)).all(),
       "SF16: a corrected statement keeps its completion date")
    _, sdet = S.losses(target)
    for b in P.ORDER[:3]:
        x = sdet[sdet.book == b]
        ok(int((x.debt > x.sale_price - x.selling_costs).sum()) == gB[b]["at_loss"], "SF20: at a loss, %s" % b)
    # ask A's primary: a re-sealed order follows the claim's previous order with the same terms and no hearing between
    for b in P.ORDER[:3]:
        ok(A["reseal_counted"][b]["orders"] > gA[b]["orders"], "ask A primary moves the orders, %s" % b)
    ok(A["same_terms_dropped"][FTB]["orders"] < gA[FTB]["orders"] or A["same_terms_dropped"][HLTV]["orders"] < gA[HLTV]["orders"],
       "ask A interior: genuine variations on the same terms after a hearing")
    ok(A["no_register"][FTB]["open"] > gA[FTB]["open"], "ask A construction: the register closes claims")
    # ask B's primary: one sale per account, the debt every loan part's
    for b in P.ORDER[:3]:
        sl, gv = Bst["statement_register_last"][b], gB[b]
        ok(sl["sold"] > gv["sold"] and (sl["at_loss"] != gv["at_loss"] or round(sl["avg_loss"], -2) != round(gv["avg_loss"], -2)),
           "SF22, ask B primary moves the sales and the losses, %s" % b)
    rg = S.register(target)
    twin = rg[rg.duplicated("account_number", keep=False)]
    ok(len(twin) > 0 and (twin.groupby("account_number").date.nunique() == 1).all(), "SF22, ask B: a loan part shares its possession date")
    Hb = pd.read_parquet(os.path.join(target, F["history"]), columns=["account_number", "period", "balance", "arrears_balance"]).drop_duplicates()
    Hb["m"] = Hb.period.str[:4].astype(int) * 12 + Hb.period.str[5:7].astype(int) - 1
    pmonth = rg.groupby("account_number").date.min()
    gap = []
    for acct, debt in rg[rg.account_number.isin(twin.account_number)].groupby("account_number").debt_at_possession.sum().items():
        pm = pmonth[acct].year * 12 + pmonth[acct].month - 1
        row = Hb[(Hb.account_number == acct) & (Hb.m == pm - 1)]
        if len(row):
            gap.append(debt - float(row.balance.iloc[0] + row.arrears_balance.iloc[0]))
    ok(len(gap) > 10 and 0 <= np.median(gap) < 6000, "ask B: the loan parts' debts sum to the account's balance and arrears plus costs (median gap %.0f)" % np.median(gap))
    res = pair.ceiling(target)
    out["pair"] = round(res["pair"], 1)
    out["mirror"] = round(100 * res["keep"], 1)
    ok(res["pair"] <= 60 and res["keep"] < 0.35, "pair ceiling and mirror leakage")
    # ---- separation: the call reads none of the recoveries files and none of the distractors ------------------------
    if not quick:
        d = without(target, ("litigation", "sales", "receivers", "possessions", "hpi", "contacts", "appetite", "ratecard"))
        r = S.main_call(d)
        ok(r["book"] == FTB and abs(r["avoided"][FTB] - av[FTB]) < 1e-9, "separation: the call without the recoveries files and distractors")
        shutil.rmtree(d)
    # ---- realism and gates -----------------------------------------------------------------------------------------
    ok(reg.date.max() <= pd.Timestamp(P.ASOF), "register within the as-of date")
    sales = pd.read_csv(os.path.join(target, F["sales"]))
    ok(sales.completion_date.max() <= P.ASOF and lit.action_date.max() <= P.ASOF, "sales and litigation within the as-of date")
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    import pyarrow.parquet as pq
    ok(pq.ParquetFile(os.path.join(target, F["history"])).metadata.num_rows >= 25000, "input gates: a large file")
    ok(not pq.ParquetFile(os.path.join(target, F["history"])).schema_arrow.metadata, "parquet carries no pandas schema block")
    m = re.search(r"Support team \(even\) (\d+) (\d+) \(([\d.]+)%\) (\d+) \(([\d.]+)%\) Usual collections \(odd\) (\d+) (\d+) \(([\d.]+)%\) (\d+)", pilot)
    ok(m is not None, "pilot table readable")
    tl, ul = int(m.group(2)) / int(m.group(1)), int(m.group(7)) / int(m.group(6))
    ok(0.62 < tl / ul < 0.78, "pilot: four payments behind about twice the planning cut less often (%.2f)" % (tl / ul))
    ok(("about %d per cent less often" % (int(round((1 - tl / ul) * 20)) * 5)) in pilot, "pilot: the stated cut matches the table")
    ok(100 * P.EFFECT < 0.5 * int(round((1 - tl / ul) * 20)) * 5, "pilot: the planning cut is under half the stated cut in arrears")
    out["pilot_ratio"] = round(tl / ul, 2)
    import build as BD
    pt = BD.pilot_table(pd.read_parquet(os.path.join(target, F["history"])),
                        pd.read_csv(os.path.join(target, F["litigation"]), dtype={"account_number": str}),
                        pd.read_csv(os.path.join(target, F["receivers"]), dtype={"account_number": str}))
    ok([pt[k] for k in ("team_n", "team_four", "team_claim", "usual_n", "usual_four", "usual_claim")]
       == [int(m.group(i)) for i in (1, 2, 4, 6, 7, 9)], "pilot table reproduces from the records")
    realism(target, ok)
    if NOTE is not None:
        for k, v in NOTE.items():
            ok(out.get(k) == v, "note figure %s: note %s, pack %s" % (k, v, out.get(k)))
    print("checks: %d passed, %d failed" % (N, len(FAILED)))
    if FAILED:
        raise AssertionError("; ".join(FAILED))
    return out


if __name__ == "__main__":
    o = main(sys.argv[1], quick="--quick" in sys.argv)
    print(json.dumps(o, indent=1, default=str)[:6000])
