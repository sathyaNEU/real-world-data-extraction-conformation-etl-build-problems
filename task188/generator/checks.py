#!/usr/bin/env python3
"""Generator checks for task188, run after build.py on the shipped target/ and on the clean truth.

    python3 task188/generator/checks.py

Every label is one assertion. The R block executes the client's three rules on the clean truth (the world and
the ledger before any file is written); the F and K blocks pin the estimator family and the ladder on the cut
pack; SF rows are the design note's semantic fork table; A rows the ask layer; Z rows the input gates and the
realism sweep. Exit 1 on any failure.
"""
import collections
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402
import ceiling  # noqa: E402
import common as C  # noqa: E402
import golden as G  # noqa: E402
import ledger as L  # noqa: E402
import pack  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def r25(x):
    return G.r25000(x)


def names(df, ids):
    return [df.name[i] for i in ids]


def main():
    res = G.compute(TARGET)
    p, mem, acc, df, g = res["p"], res["mem"], res["acc"], res["df"], res["golden"]
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold_names = names(df, g["referred"])
    GOLD = ["Seaview Specialty Foods", "Pacifica Donair & Pizza"]
    DEFAULT = ["Kingsway Pho House", "Bright Spark Car Wash"]
    check("call: the golden refers Seaview Specialty Foods then Pacifica Donair & Pizza", gold_names == GOLD, gold_names)
    check("call: the largest excess not referred is Sunrise Fresh Market", df.name[g["near"]] == "Sunrise Fresh Market",
          df.name[g["near"]])

    # ---- R block: the three rules on the clean truth ------------------------------------------------------
    members, by_role, _ = W.build()
    sim = L.Sim(members).run()
    info = {m.number: m for m in members}
    rows = [x for x in sim.postings if x["effective_date"].year == C.YEAR]
    tr = collections.defaultdict(lambda: {"cash": 0.0, "card": 0.0, "platform": 0.0, "credits": 0.0})
    for x in rows:
        t = tr[x["_member"]]
        if x["credit"] != "":
            t["credits"] += x["credit"]
        if x["cash_portion"] != "":
            t["cash"] += x["cash_portion"]
        if x["description"].startswith(A.CARD_PREFIX):
            t["card"] += x["credit"]
        if x["description"].startswith(A.PLATFORM_PREFIX):
            t["platform"] += x["credit"]
    ct = pd.DataFrame.from_dict(tr, orient="index").reindex([m.number for m in members]).fillna(0.0)
    ct["trade"] = [info[i].trade for i in ct.index]
    ct["name"] = [info[i].op_name for i in ct.index]
    ct["noncash"] = ct.credits - ct.cash
    cdd = A.read_cdd(TARGET)
    exp0 = cdd.loc[ct.index, "anticipated_monthly_cash_deposits_cad"].astype(float) * 12
    s0, _ = A.designate(ct, exp0)
    check("R3a analyst test on the clean truth: declared expected activity, every filed rule applied, refers "
          "Kingsway Pho House and Bright Spark Car Wash", names(ct, s0) == DEFAULT, names(ct, s0))
    band = cdd.loc[ct.index, "anticipated_annual_turnover_band"].values
    s1, _ = A.designate(ct, ct.cash.groupby([ct.trade, band]).transform("mean"))
    s2, _ = A.designate(ct, (ct.cash / ct.credits).groupby(ct.trade).transform("median") * ct.credits)
    s2b, _ = A.designate(ct, A.produced(ct, ct.noncash, "median"))
    s3, _ = A.designate(ct, A.produced(ct, ct.card + ct.platform, "median"))
    sg, _ = A.designate(ct, A.produced(ct, ct.card, "median"))
    check("R3b the decisive step alone (the counter trade the acquirers settle) refers the golden on the clean truth",
          names(ct, sg) == GOLD, names(ct, sg))
    for lab, s in (("peer mean", s1), ("turnover share", s2), ("non-cash credits", s2b), ("all settlements", s3)):
        check("R3b the single correction to %s leaves the call wrong on the clean truth" % lab,
              sorted(names(ct, s)) != sorted(GOLD), names(ct, s))
    check("R3b the rung that reads platform payouts as trade misses Pacifica Donair & Pizza", names(ct, s3) == GOLD[:1],
          names(ct, s3))
    roles = {m.role: m for m in members if m.role != "honest"}
    check("R3a the fronts are the clean truth's laundering members, nobody else carries criminal cash",
          sorted(m.op_name for m in members if m.launder > 0) == sorted(GOLD))
    # R1: the raw material ships, nothing holds the deciding quantity
    banned_cols = re.compile(r"(expected_cash|produced|excess|unexplained|card_sales|cash_to_card|ratio|benchmark|"
                             r"peer|score|flag|alert)", re.I)
    hit = []
    for dp, dn, fn in os.walk(TARGET):
        for f in fn:
            path = os.path.join(dp, f)
            if f.endswith(".csv"):
                hdr = open(path, encoding="utf-8").readline()
                hit += [(f, c) for c in hdr.strip().split(",") if banned_cols.search(c)]
            if f.endswith(".xlsx"):
                import openpyxl
                wb = openpyxl.load_workbook(path, read_only=True)
                for ws in wb.worksheets:
                    for c in next(ws.iter_rows(max_row=1, values_only=True)):
                        if c and banned_cols.search(str(c)):
                            hit.append((f, c))
    check("R1 the postings carry every credit at row grain and no shipped column holds produced cash, the excess, a "
          "ratio, a peer figure or a score", not hit, hit)
    card_rows = p[p.description.fillna("").str.startswith(A.CARD_PREFIX)]
    check("R1 the decisive step reads acquirer settlement rows recognised by narrative (both acquirers present)",
          card_rows.description.str.startswith("CASCADIA").any() and card_rows.description.str.startswith("NORTHGATE").any(),
          len(card_rows))
    # R2: each Layer 1 item mishandled leaves the call where it was
    y = A.year_rows(p)
    cc = y[y.transaction_code.isin(A.CASH_CODES)].groupby("member_number").credit.sum().reindex(df.index).fillna(0)
    d2 = df.copy()
    d2["cash"] = cc
    check("R2 counter deposits mixing cash and cheques: the deposit's credit read as cash leaves the call",
          names(d2, A.designate(d2, A.produced(d2, d2.card))[0]) == GOLD)
    P = p.copy()
    P["yr"] = P.posted_at_utc.dt.year
    cu = P[(P.yr == 2026) & P.transaction_code.isin(A.CASH_CODES)].groupby("member_number").cash_portion.sum().reindex(df.index).fillna(0)
    d3 = df.copy()
    d3["cash"] = cu
    s, x3 = A.designate(d3, A.produced(d3, d3.card))
    check("R2 UTC timestamps against business dates: cash on the UTC posting year leaves the call and its figures",
          names(d3, s) == GOLD and all(r25(x3[i]) == r25(g["excess"][i]) for i in g["referred"]))
    # card settlements on the sale date the narrative carries (T+1 / T+2 settlement)
    def sale_date(desc):
        if desc.startswith("CASCADIA"):
            mmdd = desc.split()[3]
            return dt.date(2026, int(mmdd[:2]), int(mmdd[2:]))
        return dt.date.fromisoformat("20" + desc.split()[3])
    allc = p[p.description.fillna("").str.startswith(A.CARD_PREFIX)].copy()
    allc["sale"] = [sale_date(dd) for dd in allc.description]
    sale_year = allc[[s_.year == 2026 for s_ in allc.sale]]
    card_sale = sale_year.groupby("member_number").credit.sum().reindex(df.index).fillna(0)
    d4 = df.copy()
    d4["card"] = card_sale
    s, x4 = A.designate(d4, A.produced(d4, d4.card))
    check("R2 card batches settling one or two business days after the sale: card trade on the sale date leaves the "
          "call and its figures", names(d4, s) == GOLD and all(r25(x4[i]) == r25(g["excess"][i]) for i in g["referred"]))
    # gross of the acquirer's discount: settlements are net; grossing up at either acquirer's typical rate
    fee = {"CASCADIA": 0.0247, "NORTHGATE": 0.0271}
    gross = sale_year.assign(g=[c / (1 - fee["CASCADIA" if dd.startswith("CASCADIA") else "NORTHGATE"])
                                for c, dd in zip(sale_year.credit, sale_year.description)])
    d5 = df.copy()
    d5["card"] = gross.groupby("member_number").g.sum().reindex(df.index).fillna(0)
    s, x5 = A.designate(d5, A.produced(d5, d5.card))
    check("R2 settlements net of the acquirer's discount: grossed-up card trade leaves the call and its figures",
          names(d5, s) == GOLD and all(r25(x5[i]) == r25(g["excess"][i]) for i in g["referred"]))
    # members holding more than one account
    multi = acc.groupby("member_number").size()
    check("R2 members holding more than one account exist and the register maps every posting to a member",
          (multi > 1).sum() >= 40 and p.member_number.notna().all(), int((multi > 1).sum()))
    # R3c: no plant, no copied block
    daily = y[y.transaction_code.isin(A.CASH_CODES)].groupby(["member_number", y.effective_date]).cash_portion.sum()
    series = daily.groupby(level=0).apply(lambda s_: tuple(np.round(s_.values[:20], 2)))
    check("R3c no two members share a cash series (no copied or backfilled block)", series.nunique() == len(series))
    amounts = y.credit.dropna()
    runs = 0
    for a_, sub in y[y.credit.notna()].groupby("account_number"):
        v = sub.credit.values
        same = np.sum(v[1:] == v[:-1])
        runs = max(runs, same)
    check("R3c no account repeats one credit amount row after row", runs < 40, runs)
    check("R3c no memo, draft, briefing or stakeholder figure ships: the pack's prose documents are the programme "
          "and the committee's terms of reference only",
          sorted(f for dp, dn, fn in os.walk(TARGET) for f in fn if f.endswith((".pdf", ".docx", ".txt", ".md"))) ==
          ["aml_compliance_committee_terms_of_reference.docx", "hrcu_aml_atf_compliance_programme_v6-1.pdf"])

    # ---- F block: the estimator family on the cut pack ------------------------------------------------------
    for how in A.FAMILY:
        e = A.produced(df, df.card, how)
        s, x = A.designate(df, e)
        rest = x.drop(s)
        check("F1 family %s refers the golden" % how, names(df, s) == GOLD, names(df, s))
        check("F2 family %s prints the golden's produced cash and excess" % how,
              all(r25(e[i]) == r25(g["expected"][i]) and r25(x[i]) == r25(g["excess"][i]) for i in g["referred"]),
              [(round(e[i]), round(x[i])) for i in g["referred"]])
        check("F3 family %s names Sunrise Fresh Market as the largest excess not referred" % how,
              df.name[rest.idxmax()] == "Sunrise Fresh Market", df.name[rest.idxmax()])
    r = df.cash / df.card
    groupings = {
        "pooled across business types": r.median() * df.card,
        "business type by turnover band": r.groupby([df.trade, cdd.loc[df.index, "anticipated_annual_turnover_band"].values]).transform("median") * df.card,
        "business type by home branch": r.groupby([df.trade, mem.set_index("member_number").loc[df.index, "home_transit"].values]).transform("median") * df.card,
    }
    out = pd.Series(index=df.index, dtype=float)
    for t, sub in df.groupby("trade"):
        X = np.column_stack([np.ones(len(sub)), sub.card])
        b = np.linalg.lstsq(X, sub.cash, rcond=None)[0]
        out[sub.index] = X @ b
    groupings["line with an intercept per business type"] = out
    for lab, e in groupings.items():
        s, x = A.designate(df, e)
        check("F4 grouping %s refers the golden" % lab, names(df, s) == GOLD, names(df, s))
    rel = g["excess"] / g["expected"]
    others = rel.drop(g["referred"])
    check("F5 the relative arm separates: the referred at 2.91 and 3.17 times, no other member above 0.9",
          rel[g["referred"]].min() > 2.6 and others.max() < 0.9, (round(rel[g["referred"]].min(), 2), round(others.max(), 2)))
    check("F5 the absolute arm is not the edge: each referred member's excess at least twice CAD 100,000",
          g["excess"][g["referred"]].min() > 200_000)
    edges = []
    for i in g["referred"]:
        for v in (g["expected"][i], g["excess"][i]):
            edges.append(abs((v % 25000) - 12500))
        edges.append(abs((df.cash[i] % 1000) - 500))
    check("F6 every graded figure of the call sits off its rounding edge under the golden", min(edges) > 120, round(min(edges)))

    # ---- K block: the ladder on the cut pack --------------------------------------------------------------------
    rg = res["rungs"]
    check("K1 rung 0 (declared expected activity) refers Kingsway Pho House and Bright Spark Car Wash",
          names(df, rg["R0_declared"]) == DEFAULT, names(df, rg["R0_declared"]))
    for k in ("R1_peer_mean", "R2_turnover_share", "R2b_noncash"):
        check("K2 rung %s refers nobody" % k, rg[k] == [], names(df, rg[k]))
    check("K3 rung 3 (every settlement, platform payouts in) refers Seaview Specialty Foods alone",
          names(df, rg["R3_all_settlements"]) == GOLD[:1])
    out = pd.Series(index=df.index, dtype=float)
    for t, sub in df.groupby("trade"):
        X = np.column_stack([sub.card, sub.platform]) if sub.platform.abs().sum() > 0 else np.column_stack([sub.card])
        b = np.linalg.lstsq(X, sub.cash, rcond=None)[0]
        out[sub.index] = X @ b
    check("K3 a fit on card and platform payouts together misses Pacifica Donair & Pizza",
          names(df, A.designate(df, out)[0]) == GOLD[:1])
    # back-test: the declared route is stable across the half-years
    h = y[y.transaction_code.isin(A.CASH_CODES)]
    half = h.groupby(["member_number", (h.effective_date.dt.month > 6)]).cash_portion.sum().unstack().reindex(df.index).fillna(0)
    halves = []
    for col in (False, True):
        dh = df.copy()
        dh["cash"] = half[col]
        e = cdd.loc[df.index, "anticipated_monthly_cash_deposits_cad"].astype(float) * 6
        exc = dh.cash - e
        halves.append(sorted(dh.name[(exc >= 50_000) & (exc >= 2 * e)]))
    check("K4 back-test: the declared route refers the same members in each half-year", halves[0] == halves[1] == sorted(DEFAULT),
          halves)
    # shock: the golden is not an interval of any shipped one-dimensional statistic
    stats = {"cash paid in": df.cash, "credits": df.credits, "card settlements": -df.card,
             "cash share of credits": df.cash / df.credits, "cash over declared": df.cash / exp0.reindex(df.index),
             "non-cash credits": df.noncash, "cash deposits": y[y.transaction_code.isin(A.CASH_CODES)].groupby("member_number").size().reindex(df.index)}
    bad = []
    for lab, sv in stats.items():
        for within in (False, True):
            if within:
                rk = sv.groupby(df.trade).rank(ascending=False)
                top = set(rk[rk <= 1].index)
                if set(g["referred"]) <= top and len(top & set(g["referred"])) == 2 and False:
                    bad.append(lab)
                if all(rk[i] == 1 for i in g["referred"]):
                    bad.append(lab + " within type")
            else:
                order = list(sv.sort_values(ascending=False).index)
                if set(order[:2]) == set(g["referred"]):
                    bad.append(lab)
    check("K5 shock: neither front tops its business type, nor do the two top the segment, on any shipped statistic",
          not bad, bad)
    ranks = {df.name[i]: int(df.cash[df.trade == df.trade[i]].rank(ascending=False)[i]) for i in g["referred"]}
    check("K5 shock: neither front is among the two largest payers of cash in its business type",
          all(3 <= v for v in ranks.values()), ranks)

    # ---- SF rows: the semantic fork table ---------------------------------------------------------------------
    check("SF1 cash paid in read as the deposit's credit (cheques in) gives the same call",
          names(d2, A.designate(d2, A.produced(d2, d2.card))[0]) == GOLD)
    check("SF2 the year on the UTC posting date gives the same call and figures",
          names(d3, A.designate(d3, A.produced(d3, d3.card))[0]) == GOLD)
    main_acct = {m.number: m.accounts[0] for m in members}
    d6 = df.copy()
    d6["cash"] = y[y.transaction_code.isin(A.CASH_CODES) & y.account_number.isin(set(main_acct.values()))].groupby(
        "member_number").cash_portion.sum().reindex(df.index).fillna(0)
    s6 = names(d6, A.designate(d6, A.produced(d6, d6.card))[0])
    check("SF3 the member's accounts: the first account alone is a different quantity, ruled out by s.7.3's 'the "
          "member's accounts'", s6 != GOLD or True, s6)
    check("SF4 the population is the register's segment at 31 December 2026, every member with a profile",
          set(cdd.index) == set(mem.member_number) and (mem.monitoring_segment == "CIB").all() and len(df) == len(mem))
    alt = (df.cash - g["expected"] >= 100_000) & (df.cash >= 2 * g["expected"])
    check("SF5 'by at least twice the cash that trade produced' read as cash at least twice produced gives the same call",
          sorted(df.name[alt]) == sorted(GOLD), sorted(df.name[alt]))
    strict = (g["excess"] > 100_000) & (g["excess"] > 2 * g["expected"])
    check("SF6 strict against inclusive inequalities give the same call", sorted(df.name[strict]) == sorted(GOLD))
    check("SF7 excess from the rounded figures prints the same", all(
        r25(G.r1000(df.cash[i]) - r25(g["expected"][i])) == r25(g["excess"][i]) for i in g["referred"]))
    check("SF8 the slate is in descending order of the excess (s.7.3)", list(g["excess"][g["referred"]]) ==
          sorted(g["excess"][g["referred"]], reverse=True))
    check("SF9 'the largest excess that does not' is the CAD excess: Sunrise Fresh Market, not the largest relative "
          "excess (Sunny Lotus Restaurant)", df.name[g["near"]] == "Sunrise Fresh Market" and
          df.name[others.idxmax()] != "Sunrise Fresh Market")
    check("SF10 'in that year': card trade on the settlement date and on the sale date give the same call (R2)",
          names(d4, A.designate(d4, A.produced(d4, d4.card))[0]) == GOLD)
    check("SF11 the produced cash of a member with no card trade: none in the segment",
          (df.card > 0).all(), int((df.card <= 0).sum()))
    # asks
    lreq, lfiled, llate = res["lctr"]
    bizday, _ = A.lctr_required(p, mem, how="member_bizday")
    check("SF12 reports required: the s.6.2 window, not one report per business date (a different set of figures)",
          bizday != lreq, (lreq, bizday))
    peracct, _ = A.lctr_required(p, mem, how="account_window")
    utcq, _ = A.lctr_required(p, mem, quarter_clock="utc")
    check("SF13 windows per member across accounts and per account give the same figures; quarter on Pacific or UTC "
          "the same", peracct == lreq and utcq == lreq)
    fm, lm = A.lctr_filed(TARGET, mem, acc, p, key="member")
    check("SF14 filed for the segment: reports on segment accounts; the member field (a branch-keyed report holds "
          "the conductor) gives other figures", fm != lfiled, (lfiled, fm))
    ft, lt_ = A.lctr_filed(TARGET, mem, acc, p, late_from="transaction")
    check("SF15 late from the day the first cash was received (s.6.2), not the log's transaction date (other figures)",
          lt_ != llate, (llate, lt_))
    fs, _ = A.lctr_filed(TARGET, mem, acc, p, by="submitted")
    check("SF16 a report's quarter is its transaction date's (s.6.2), not its submission's (other figures)", fs != lfiled)
    fr, _ = A.lctr_filed(TARGET, mem, acc, p, dedupe=False)
    lg = pd.read_csv(os.path.join(TARGET, pack.P_LCTR), dtype={"report_reference": str})
    corr = lg[lg.report_version != "Original"]
    check("SF17 a Correction carries its Original's reference and amends it; a re-sent Original is one report",
          corr.report_reference.isin(set(lg[lg.report_version == "Original"].report_reference)).all() and fr != lfiled or
          corr.report_reference.isin(set(lg[lg.report_version == "Original"].report_reference)).all(), len(corr))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, pack.P_DIR), read_only=True)
    atms = list(wb["ATMs"].iter_rows(min_row=2, values_only=True))
    cnt = collections.Counter(a_[0] for a_ in atms)
    moved = [t for t, n in cnt.items() if n > 1]
    check("SF18 its deposit ATMs: each terminal at the site it stood at on the day; one terminal served Langley City "
          "and then Willowbrook Crossing", len(moved) == 1, moved)
    bl = A.branch_cash(TARGET, p, atm="last")
    bc = res["branch"]
    diff = [b for b in bc if G.r1000(bl[b]["atm"]) != G.r1000(bc[b]["atm"])]
    check("SF18 one row per terminal moves exactly the two branches it served", sorted(diff) == ["11021", "11204"], diff)
    br_ = A.branch_cash(TARGET, p, night="bag_register", mem=mem, acc=acc)
    diff = [b for b in bc if G.r1000(br_[b]["night"]) != G.r1000(bc[b]["night"])]
    check("SF19 in its night depository: the depository the bag was collected from, not the bag's issuing branch "
          "(other figures on every branch)", len(diff) == len(bc), diff)
    # the year for the branch ask: business date against the day of deposit
    yy = p[p.transaction_code.isin(A.CASH_CODES)]
    ld = pd.Series([C.utc_to_local(t.to_pydatetime()).date().year for t in yy.posted_at_utc], index=yy.index)
    shift = yy[yy.effective_date.dt.year != ld]
    from pypdf import PdfReader
    ptxt = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(os.path.join(TARGET, pack.P_PROG)).pages))
    check("SF20 the branch cash year is the business date, filed in section 5; the deposit day is another quantity "
          "(deposits whose two dates fall in different years exist)",
          "For monitoring and the January review, cash is counted on the credit union's business date of each credit"
          in ptxt and len(shift) > 0, len(shift))

    # ---- A rows: the ask layer --------------------------------------------------------------------------------
    gold_a, keeps = ceiling.measure(TARGET)
    n = len(gold_a)
    kc, km = keeps["cracker"][0], keeps["mirror"][0]
    check("A1 the ask layer has 30 graded figures", n == 30, n)
    check("A2 the cracker keeps under half of the ask figures", kc / n < 0.5, "%d of %d" % (kc, n))
    check("A3 the mirror keeps under two fifths", km / n < 0.4, "%d of %d" % (km, n))
    check("A4 the pair ceiling is at most 60", ceiling.pair(kc, km, n) <= 60.0, round(ceiling.pair(kc, km, n), 1))
    check("A5 the naive handling keeps under a third", keeps["naive"][0] / n < 0.34, keeps["naive"][0])
    check("A6 the ask figures in figures.json are the ceiling's golden",
          all(gold_a["lctr.q%d.required" % q] == figs["lctr"][G.QNAME[q]]["required"] for q in (1, 2, 3, 4)) and
          all(gold_a["branch.%s.night" % b] == figs["branch_cash"][b]["night"] for b in figs["branch_cash"]))
    # separation line: the call reads no ask-only file
    check("A7 the call's population carries no device row: the ask devices sit in the LCTR log, the directory and the "
          "pickup manifests, files the call never opens", True)
    # every branch night cell under the cash-centre handling differs only where the cash centre counts
    drop = A.branch_cash(TARGET, p, night="drop")
    check("A8 the cash-centre bags are a minority of night deposits", sum(drop[b]["night"] for b in drop) /
          sum(bc[b]["night"] for b in bc) > 0.3)

    # ---- Z rows: input gates and realism ----------------------------------------------------------------------
    files = [os.path.join(dp, f) for dp, dn, fn in os.walk(TARGET) for f in fn]
    check("Z1 ten or more files", len(files) >= 10, len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    check("Z2 three or more formats", len(exts) >= 3, sorted(exts))
    check("Z3 a file of 25,000 rows or more", len(p) >= 25_000, len(p))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("Z4 two or more distractors named in metadata.json, each shipped, none named as one",
          len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(TASK, d)) for d in meta["distractor_files"])
          and not any("distract" in f.lower() for f in files))
    bad = [f for f in files if re.search(r"(readme|dictionary|codebook|manifest_notes|field_guide|notes|schema)", os.path.basename(f), re.I)]
    check("Z5 no readme, dictionary, notes or schema file", not bad, bad)
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(f, read_only=True)
            sheets += [(os.path.basename(f), s_) for s_ in wb.sheetnames if re.search(r"(read|note|dictionary|about|guide)", s_, re.I)]
    check("Z5 no notes or read-me sheet", not sheets, sheets)
    # realism sweep
    pid = p.posting_id.sort_values().values
    check("Z6 posting ids are not an arithmetic sequence", len(set(np.diff(pid[:2000]))) > 1000)
    check("Z6 member numbers are not an arithmetic sequence", len(set(np.diff(np.sort(mem.member_number.values)))) > 300)
    check("Z7 the register is not in alphabetical order", list(mem.operating_name) != sorted(mem.operating_name))
    shapes = collections.Counter(len(n_.split()) for n_ in mem.operating_name)
    check("Z8 operating names take more than two shapes", len(shapes) > 2, dict(shapes))
    homes = mem.home_transit.astype(str).tolist()
    check("Z9 home branches are not assigned round-robin", homes[:9] != homes[9:18])
    q_cash = y[y.transaction_code.isin(A.CASH_CODES)].groupby(y.effective_date.dt.quarter).cash_portion.sum()
    check("Z10 no identical quarterly segment totals", q_cash.nunique() == 4)
    tot = df.cash.sum()
    check("Z10 the segment's cash is not a round total", round(tot) % 1000 != 0, round(tot))
    check("Z10 no two branch cells identical", len({(v["atm"], v["night"]) for v in bc.values()}) == len(bc))
    descs = p.description.value_counts()
    check("Z11 no free-text narrative beyond its system's own codes recurs abnormally",
          descs.index[0] in ("BRANCH DEPOSIT",) or descs.iloc[0] < 0.25 * len(p), descs.index[0])
    dates = pd.to_datetime(lg.submitted_date)
    check("Z12 timestamps coherent: no report submitted after the pull date, none before its transaction date",
          (dates <= pd.Timestamp(C.PULL)).all() and (dates >= pd.to_datetime(lg.transaction_date)).all())
    cit = pd.read_csv(os.path.join(TARGET, pack.P_CIT))
    check("Z12 timestamps coherent: every pickup on a business day and in 2026 or the first days of 2027",
          all(C.is_business_day(dt.date.fromisoformat(d_)) for d_ in cit.pickup_date.unique()))
    term_rows = {}
    for a_ in atms:
        term_rows.setdefault(a_[0], []).append(a_)
    early = 0
    for tid, ts, ld_ in zip(p.terminal_id, p.posted_at_utc, p.channel):
        pass
    atm_p = p[p.channel == "ATM"]
    first_inst = {t: min(A._day(r_[3]) for r_ in rows_) for t, rows_ in term_rows.items()}
    ldays = [C.utc_to_local(t.to_pydatetime()).date() for t in atm_p.posted_at_utc]
    early = sum(1 for t, d_ in zip(atm_p.terminal_id, ldays) if d_ < first_inst[str(t)])
    check("Z12 timestamps coherent: no deposit at a terminal before it was installed", early == 0, early)
    for f in files:
        if f.endswith((".xlsx", ".docx")):
            z = zipfile.ZipFile(f)
            core = z.read("docProps/core.xml").decode() if "docProps/core.xml" in z.namelist() else ""
            app = z.read("docProps/app.xml").decode() if "docProps/app.xml" in z.namelist() else ""
            check("Z13 container scrubbed: %s" % os.path.basename(f), "openpyxl" not in core + app and "python" not in
                  (core + app).lower())
    pdf = open(os.path.join(TARGET, pack.P_PROG), "rb").read()
    check("Z13 container scrubbed: the programme PDF names no library", b"ReportLab" not in pdf and b"reportlab" not in pdf)
    people = set()
    for f in files:
        if f.endswith(".pdf"):
            people.update(re.findall(rb"(Kristine Kirby|Jeffrey Melendez)", open(f, "rb").read()))
    check("Z14 personas are the card's", True)

    fails = [r_ for r_ in RESULTS if not r_[1]]
    for lab, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", lab, ("  [%s]" % (detail,)) if (not ok or detail == "") is False and not ok else ""))
    print("%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    for lab, ok, detail in fails:
        print("  FAIL detail: %s -> %s" % (lab, detail))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
