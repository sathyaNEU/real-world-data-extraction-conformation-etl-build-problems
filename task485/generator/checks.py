"""task485's generator checks, run on the cut pack in target/ and on the clean truth world.build() holds.

    python3 task485/generator/checks.py

The R block executes the client's three rules (dataset-generation 7.1); the SF block asserts every row of the design
note's semantic fork table; the rest are the rungs, the ask devices and their separation from the main call, the bin
edges of every graded figure, the input gates and the realism sweep. Exit 1 on any FAIL."""
import collections
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import analysis as A   # noqa: E402
import pdftext         # noqa: E402
import world as W      # noqa: E402

ROWS = []
GOLD_PICKS = {"GLP-1 receptor agonists": "Velantro", "SGLT2 inhibitors": "Empriva", "Long-acting insulins": "Glarvia",
              "Direct oral anticoagulants": "Apiqor", "Inhaled corticosteroid and LABA combinations": "Brezara",
              "Adalimumab products": "adalimumab-kvrn"}
DEFAULT_PICKS = dict(GOLD_PICKS, **{"GLP-1 receptor agonists": "Liraquent", "Long-acting insulins": "insulin glargine-qmrt",
                                    "Inhaled corticosteroid and LABA combinations": "Saltiva"})
ASOF = dt.date(2026, 10, 19)
PEOPLE = {"Maria Burgess", "Brenda Cook", "Timothy Peterson", "Alyssa Fletcher"}


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def r10(x):
    return int(round(x / 10.0)) * 10


def band_dist(x):
    """Distance from x to the nearest edge of its ten-dollar band (an edge sits at every multiple of 10 plus 5)."""
    return 5.0 - abs(x - 10.0 * round(x / 10.0))


def picks_of(pk, net):
    return {c: v["pick"] for c, v in pk.picks(net).items()}


# ---------------------------------------------------------------- the clean truth (no export, no mess)
def truth(w):
    """Every rung on the clean truth: each claim's own rebate, the claims never reversed, one account code."""
    P = w.products
    fqs = [f[0] for f in W.FQ]
    live = [c for c in w.claims if not c["rev"]]
    units, cost, reb = collections.defaultdict(float), collections.defaultdict(float), collections.defaultdict(float)
    cell, rcell = collections.defaultdict(float), collections.defaultdict(float)
    for c in live:
        k, u = c["key"], c["qty"] / P[c["key"]]["per30"]
        units[k] += u
        cost[k] += c["ingr"]
        reb[k] += c["rebate"]
        if c["eligible"]:
            cell[(k, c["acc"], W.fq_of(c["d"]))] += u
            rcell[(P[k]["mfr"], c["acc"], W.fq_of(c["d"]))] += c["rebate"]
    keys = [k for k in P if units[k] > 0]
    by_m = collections.defaultdict(list)
    for k in keys:
        by_m[P[k]["mfr"]].append(k)
    rev_m = {m: sum(reb[k] for k in ks) for m, ks in by_m.items()}

    def net(rebates):
        return {P[k]["brand"]: (cost[k] - rebates.get(k, 0.0)) / units[k] for k in keys if P[k]["cls"] in W.REVIEWED}

    def prorata(basis):
        out = {}
        for m, ks in by_m.items():
            wts = {k: (cost[k] if basis == "cost" else units[k]) for k in ks}
            s = sum(wts.values())
            for k in ks:
                out[k] = rev_m[m] * wts[k] / s
        return out

    def fit(inscope=False):
        out = {}
        for m, ks in by_m.items():
            ks = [k for k in ks if not inscope or P[k]["cls"] in W.REVIEWED]
            if not ks:
                continue
            cells = [(a, f) for a in W.ACC for f in fqs]
            X = np.array([[cell[(k, a, f)] for k in ks] for a, f in cells])
            Y = np.array([rcell[(m, a, f)] for a, f in cells])
            beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
            for k, b in zip(ks, beta):
                out[k] = b * sum(cell[(k, a, f)] for a, f in cells)
        return out
    classes = {name: [P[k]["brand"] for k in keys if P[k]["cls"] == c] for c, name in W.CLASSES}

    def picks(n):
        return {c: min(bs, key=lambda b: n[b]) for c, bs in classes.items()}
    return dict(true=net(reb), gross=net({}), default=net(prorata("cost")), units=net(prorata("units")),
                fit=net(fit()), inscope=net(fit(True)), picks=picks)


def main():
    pk = A.Pack(TARGET)
    D = pk.D
    g = pk.golden()
    gnet = g["net"]
    gold = picks_of(pk, gnet)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    w = W.build()
    T = truth(w)

    # ================================================================ R1 to R3c: the three rules on the clean truth
    hdr_claims = open(os.path.join(TARGET, A.FILES["claims"]), encoding="utf-8").readline().strip().split(",")
    check("R1a the claims carry the field's raw material (ingredient cost, quantity, NDC, date of service, account)",
          {"ingredient_cost_paid", "quantity_dispensed", "ndc", "date_of_service", "group_id"} <= set(hdr_claims))
    check("R1b no claims column holds a rebate or a net cost", not any(re.search("rebate|net", h) for h in hdr_claims),
          ",".join(hdr_claims))
    drug_hdr = list(next(iter(D["drug"].values())).keys())
    check("R1c the drug file carries no price, rebate or net cost column",
          not any(re.search("rebate|net|price|wac|awp|cost", h, re.I) for h in drug_hdr), ",".join(drug_hdr))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TARGET, A.FILES["stmt_2026Q1"]), read_only=True)
    shdr = [r for r in wb["Remittance"].iter_rows(values_only=True) if r and r[0] == "Manufacturer"][0]
    check("R1d the statements carry each manufacturer's remittance by account and service period, no product column",
          list(shdr) == ["Manufacturer", "Account", "Account Name", "Line Type", "Service Period", "Rebate Amount (USD)"]
          and not any(re.search("ndc|product|drug", str(h), re.I) for h in shdr))
    resid = []
    fqs = [f[0] for f in A.FQS]
    for lab in pk.labelers:
        bs = pk.brands_of[lab]
        X = np.array([[pk.cell[(b, a, f)] for b in bs] for a in pk.accts for f in fqs])
        Y = np.array([pk.reb[(lab, a, f)] for a in pk.accts for f in fqs])
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        resid.append(float(np.max(np.abs(X @ beta - Y))))
    check("R1e the decisive computation reads every manufacturer's 16 account-quarter cells and fits them to the cent",
          max(resid) < 0.01, "largest cell residual %.4f" % max(resid))

    # R2: each Layer 1 item mishandled, the golden method's call (and where named, every net cost) holds
    ndcs = [r["ndc"] for r in csv.DictReader(open(os.path.join(TARGET, A.FILES["claims"]), encoding="utf-8"))]
    hy = [n for n in ndcs if "-" in n]
    unmatched = [n for n in ndcs if n.replace("-", "") not in D["drug"]]
    check("R2a NDC layouts: both layouts ship and a plain hyphen strip maps every claim row to the drug file",
          hy and len(hy) < len(ndcs) and not unmatched, "%d hyphenated of %d, %d unmatched" % (len(hy), len(ndcs), len(unmatched)))
    us = [r["date_of_service"] for r in csv.DictReader(open(os.path.join(TARGET, A.FILES["claims"]), encoding="utf-8"))
          if "/" in r["date_of_service"]]
    dayfirst_fail = sum(1 for s in us if int(s.split("/")[1]) > 12)
    check("R2b date layouts: US dates ship beside ISO dates and a day-first reading fails outright on the US rows",
          us and dayfirst_fail > 1000, "%d US dates, %d impossible day-first" % (len(us), dayfirst_fail))

    def variant(**opt):
        pk.setup(**opt)
        n = pk.net(pk.fit()[0])
        pk.setup()
        return n
    codes = variant(accounts="codes")
    check("R2c account renumbering: the fit on the raw old and new group codes prints every net cost unchanged",
          max(abs(codes[b] - gnet[b]) for b in pk.compared) < 0.01)
    keep = variant(netting="keep")
    check("R2d reversals: reversed claims left in, the call holds (policy 3.4 removes them; net costs move)",
          picks_of(pk, keep) == gold, "largest move %.1f" % max(abs(keep[b] - gnet[b]) for b in pk.compared))
    cur = variant(remit="cur")
    stq = variant(remit="statement")
    check("R2e prior period lines: current lines only, or every line on its statement's quarter, the call holds",
          picks_of(pk, cur) == gold and picks_of(pk, stq) == gold,
          "largest moves %.1f and %.1f" % (max(abs(cur[b] - gnet[b]) for b in pk.compared),
                                           max(abs(stq[b] - gnet[b]) for b in pk.compared)))
    fy25_lines = [l for l in D["stmt"] if l["fq"] is None]
    check("R2f fiscal 2025 lines ship (the April to June 2025 statement and its adjustments) and fall outside every "
          "fiscal 2026 cell by their service period", len(fy25_lines) > 50 and
          all(l["svc"] in ("Apr-Jun 2025", "Jan-Mar 2025") for l in fy25_lines))
    stmt_names = sorted({l["mfr"] for l in D["stmt"]})
    labels = sorted({v["Labeler Name"] for v in D["drug"].values()})
    mapped = {n: [lb for lb in labels if A.norm_mfr(lb) == A.norm_mfr(n)] for n in stmt_names}
    check("R2g manufacturer names: no statement name equals a labeler name and each maps to exactly one",
          not set(stmt_names) & set(labels) and all(len(v) == 1 for v in mapped.values())
          and len({v[0] for v in mapped.values()}) == len(stmt_names))
    comp = variant(compounds="in")
    ncomp = sum(1 for c in pk.claims if c["compound"])
    check("R2h compound claims: counted in the fit, every net cost unchanged", ncomp > 0 and
          max(abs(comp[b] - gnet[b]) for b in pk.compared) < 0.01, "%d compound claims" % ncomp)
    days = variant(units="days")
    check("R2i package units: 30-day supplies taken as days supply over 30, the call holds (policy 4.1 fixes the "
          "quantity; net costs move)", picks_of(pk, days) == gold)
    by_no = {c["no"]: c for c in D["claims_all"]}
    rows = list(csv.DictReader(open(os.path.join(TARGET, A.FILES["claims"]), encoding="utf-8")))
    layout = {r["claim_number"]: ("/" in r["date_paid"]) for r in rows}
    cross = sum(1 for r in rows if r["claim_status"] == "R" and layout[r["reversal_of"]] != layout[r["claim_number"]])
    orphan = sum(1 for r in rows if r["claim_status"] == "R" and r["reversal_of"] not in by_no)
    check("R2j two platform layouts: reversal rows written in another layout than their originals still resolve by "
          "claim number", cross > 0 and orphan == 0, "%d cross-layout reversals, %d orphans" % (cross, orphan))
    saved = D["network"], D["roster"]
    D["network"], D["roster"] = {}, []
    pk.setup()
    blind = pk.net(pk.fit()[0])
    D["network"], D["roster"] = saved
    pk.setup()
    check("R2k the ask devices (network history, reissued person codes) sit outside the main call: with the network "
          "file and the roster emptied every net cost is unchanged", max(abs(blind[b] - gnet[b]) for b in pk.compared) < 1e-9)

    # R3a / R3b on the clean truth and on the pack
    check("R3a analyst test on the clean truth: pro rata by ingredient cost files Liraquent, insulin glargine-qmrt "
          "and Saltiva", T["picks"](T["default"]) == DEFAULT_PICKS, str(T["picks"](T["default"])))
    check("R3a the same default from the pack files the same wrong set", picks_of(pk, pk.net(pk.prorata())) == DEFAULT_PICKS)
    check("R3b the decisive step alone (the fit in place of the split) files the golden on the clean truth",
          T["picks"](T["fit"]) == GOLD_PICKS and T["picks"](T["true"]) == GOLD_PICKS)
    check("R3b the fit on the clean truth equals each product's true net cost to the cent",
          max(abs(T["fit"][b] - T["true"][b]) for b in T["true"]) < 0.01)
    check("R3b the pack's golden equals the clean truth's net cost to the cent (the export is lossless)",
          max(abs(gnet[b] - T["true"][b]) for b in pk.compared) < 0.01)
    for lab, n in (("gross ingredient cost", T["gross"]), ("pro rata by 30-day supplies", T["units"]),
                   ("the fit on the compared products alone", T["inscope"])):
        check("R3b one rung below, %s, still files a wrong set" % lab, T["picks"](n) != GOLD_PICKS)
    # R3c: no plant
    texts = {f: pdftext.text(os.path.join(TARGET, f)) for f in os.listdir(TARGET) if f.endswith(".pdf")}
    brands = list(gnet)
    ranked = [f for f, t in texts.items() if any(b in t for b in brands) and re.search(r"\$\s?\d|\d,\d{3}\.\d\d", t)]
    check("R3c no shipped artifact ranks the compared products: no document that names one carries a money figure",
          not ranked, ",".join(ranked))
    series = collections.defaultdict(lambda: [0] * 12)
    for c in w.claims:
        m = (c["d"].year - 2025) * 12 + c["d"].month - 7
        series[(c["key"], c["acc"])][m] += 1
    dup = len(series) - len({tuple(v) for v in series.values()})
    check("R3c no copied block: no two product-account monthly series are identical", dup == 0, "%d duplicates" % dup)
    memo = [f for f, t in texts.items() for sent in re.split(r"(?<=[.?!])\s+", t) for b in brands
            if b in sent and re.search(r"recommend|prefer|propose|favou?r", sent, re.I)]
    check("R3c no decoy memo or draft carrying an answer: no document puts a compared product beside a preference",
          not memo, ",".join(sorted(set(memo))))

    # ================================================================ SF rows (design note's semantic fork table)
    check("SF1 the fiscal year is 1 July 2025 to 30 June 2026: every claim's service date falls in it and the last "
          "quarter's statement was remitted 18 September 2026",
          all(dt.date(2025, 7, 1) <= c["dos"] <= dt.date(2026, 6, 30) for c in D["claims_all"]) and
          "Remittance date: September 18, 2026" in str(list(load_workbook(os.path.join(TARGET, A.FILES["stmt_2026Q2"]),
                                                                          read_only=True)["Remittance"].iter_rows(values_only=True))[4]))
    paid = variant(window="paid")
    check("SF2 claims filled in the year read by date paid instead: same call, every net cost in its band",
          picks_of(pk, paid) == gold and all(r10(paid[b]) == r10(gnet[b]) for b in pk.compared))
    net_rows = sum(1 for r in rows if r["claim_status"] == "R")
    check("SF3 a reversal row nets its claim; the reversed claim and its reversal both leave the count",
          net_rows == len(D["reversed"]) and len(pk.claims) == len(D["claims_all"]) - len(D["reversed"]))
    fee = variant(cost="ingr_fee")
    plan = variant(cost="plan")
    check("SF4 the cost basis: with dispensing fees the bands hold; plan paid after cost sharing moves every band and "
          "is ruled out by policy 3.2 (before member cost sharing, without dispensing fees); the call holds under all",
          all(r10(fee[b]) == r10(gnet[b]) for b in pk.compared) and picks_of(pk, plan) == gold and
          "before member cost sharing and without dispensing fees" in texts[A.FILES["policy"]])
    check("SF5 the rebates on those claims are every line whose service period is a fiscal 2026 quarter; current "
          "lines only or statement quarters keep the call", picks_of(pk, cur) == gold and picks_of(pk, stq) == gold and
          sum(1 for l in D["stmt"] if l["fq"] and l["kind"] != "Current Quarter") > 10)
    check("SF6 the 30-day supply is the clinical review's quantity (policy 4.1): days supply over 30 keeps the call",
          picks_of(pk, days) == gold and len(pk.per30) == len(pk.compared))
    check("SF7 the products compared are the clinical review's Table 1, every one carried on the claims",
          sorted(pk.compared) == sorted(gnet) and all(pk.u30[b] > 0 for b in pk.compared) and len(pk.classes) == 6)
    check("SF8 each statement manufacturer is one labeler and no labeler two statement names (one mapping, R2g)",
          len(set(D["mfr_map"].values())) == len(D["mfr_map"]))
    acct_picks = {}
    for a in A.ACC_ORDER:
        n = {}
        for b in pk.compared:
            u = sum(pk.cell[(b, a, f)] for f in fqs)
            cst = sum(pk.cell_cost[(b, a, f)] for f in fqs)
            n[b] = (cst - g["rate"][b] * u) / u
        acct_picks[a] = picks_of(pk, n)
    check("SF9 the list is the Plan's: every employer account on its own prefers the same products",
          all(v == gold for v in acct_picks.values()))
    check("SF10 rounding to the nearest ten dollars: every net cost sits at least 4 dollars inside its band",
          min(band_dist(gnet[b]) for b in pk.compared) >= 4.0,
          "nearest %.2f" % min(band_dist(gnet[b]) for b in pk.compared))
    qn = {}
    for b in pk.compared:
        vals = []
        for f in fqs:
            u = sum(pk.cell[(b, a, f)] for a in A.ACC_ORDER)
            cst = sum(pk.cell_cost[(b, a, f)] for a in A.ACC_ORDER)
            vals.append((cst - g["rate"][b] * u) / u)
        qn[b] = float(np.mean(vals))
    check("SF11 the year as one ratio of totals or the mean of its quarters: same call, every band", picks_of(pk, qn) == gold
          and all(r10(qn[b]) == r10(gnet[b]) for b in pk.compared))
    check("SF12 compound claims: no compared product carries one", not any(c["compound"] and c["brand"] in gnet
                                                                        for c in D["claims_all"]))
    partial = [c for c in pk.claims if c["brand"] in gnet and abs(c["qty"] / pk.per30[c["brand"]] -
                                                                  round(c["qty"] / pk.per30[c["brand"]])) > 1e-9]
    check("SF13 every compared claim dispenses whole 30-day supplies, so no partial-supply convention arises",
          not partial, "%d partial" % len(partial))
    gaps = [v["gap"] for v in g["picks"].values()]
    check("SF14 no tie: the nearest runner-up sits at least 40 dollars above the preferred product",
          min(gaps) >= 40, "nearest gap %.2f" % min(gaps))

    # ================================================================ rungs, margins and the golden family
    for c, b in GOLD_PICKS.items():
        check("golden %s: %s" % (c, b), gold[c] == b)
    for c, v in g["picks"].items():
        check("golden margin %s runner-up over preferred at least 1.15x" % c, v["ratio"] >= 1.15, "%.3f" % v["ratio"])
    rung = {"gross": pk.net({}), "default": pk.net(pk.prorata()), "cellwise": pk.net(pk.prorata(cellwise=True)),
            "units": pk.net(pk.prorata(basis="units")), "inscope": pk.net(pk.fit(brands=set(pk.compared))[0])}
    want = {"gross": ["Dulmira", "Canivo", "insulin glargine-qmrt", "Ravelta", "Saltiva", "adalimumab-kvrn"],
            "default": [DEFAULT_PICKS[c] for c in A.CLASS_ORDER], "cellwise": [DEFAULT_PICKS[c] for c in A.CLASS_ORDER],
            "units": ["Liraquent", "Empriva", "Deglutra", "Apiqor", "Saltiva", "adalimumab-kvrn"],
            "inscope": ["Velantro", "Canivo", "Glarvia", "Apiqor", "Vilaro", "adalimumab-kvrn"]}
    for k, n in rung.items():
        got = [picks_of(pk, n)[c] for c in A.CLASS_ORDER]
        check("rung %s files %s" % (k, ", ".join(want[k])), got == want[k], ", ".join(got))
    fam = {"cost basis": pk.net(pk.fit(basis="cost")[0]), "quarters pooled": pk.net(pk.fit(accounts=False)[0]),
           "raw group codes": codes, "date paid": paid, "with compounds": comp}
    for lab, n in fam.items():
        check("golden family, %s: every net cost in its golden band" % lab,
              all(r10(n[b]) == r10(gnet[b]) for b in pk.compared),
              "largest move %.2f" % max(abs(n[b] - gnet[b]) for b in pk.compared))
    # non-negative least squares and the fit by account alone (annual)
    from scipy.optimize import nnls
    nn, ann = {}, {}
    for lab in pk.labelers:
        bs = pk.brands_of[lab]
        X = np.array([[pk.cell[(b, a, f)] for b in bs] for a in pk.accts for f in fqs])
        Y = np.array([pk.reb[(lab, a, f)] for a in pk.accts for f in fqs])
        beta, _ = nnls(X, Y)
        Xa = np.array([[sum(pk.cell[(b, a, f)] for f in fqs) for b in bs] for a in pk.accts])
        Ya = np.array([sum(pk.reb[(lab, a, f)] for f in fqs) for a in pk.accts])
        ba, *_ = np.linalg.lstsq(Xa, Ya, rcond=None)
        for b, x, y in zip(bs, beta, ba):
            nn[b], ann[b] = x * pk.u30[b], y * pk.u30[b]
    for lab, rb in (("non-negative least squares", nn), ("accounts over the year", ann)):
        n = pk.net(rb)
        check("golden family, %s: every net cost in its golden band" % lab,
              all(r10(n[b]) == r10(gnet[b]) for b in pk.compared))
    check("default margin: Velantro sits above Liraquent and Dulmira under the split (the wrong rung is not a near tie "
          "in insulin and inhalers)", rung["default"]["Velantro"] > rung["default"]["Dulmira"] and
          rung["default"]["Deglutra"] / rung["default"]["insulin glargine-qmrt"] >= 1.15 and
          rung["default"]["Vilaro"] / rung["default"]["Saltiva"] >= 1.15)
    check("the cheap routes that reach the golden: one (the fit on every product of each manufacturer)",
          sum(picks_of(pk, n) == gold for n in rung.values()) == 0)

    # ================================================================ the asks
    rates = A.exhibit_rates(TARGET)
    check("Exhibit C rates read from the agreement", rates == {"RETAIL30": 196.0, "RETAIL90": 560.0, "MAIL": 585.0,
                                                               "SPECIALTY": 1330.0}, str(rates))
    gq = pk.guarantee(rates)
    fq_file = pk.guarantee(rates, channel=pk.channel_file)
    hosp = [n for n, r in D["network"].items() if r["NETWORK"] == "SPECIALTY" and
            any(c["npi"] == n and c["fee"] > 0 for c in pk.claims)]
    pre = [c for c in pk.claims if c["npi"] in hosp and c["fee"] > 0]
    post = [c for c in pk.claims if c["npi"] in hosp and c["fee"] == 0]
    check("ask A device: three pharmacies the network file lists as specialty carry the retail dispensing fee until "
          "30 April 2026 and none after", len(hosp) == 3 and pre and post and max(c["dos"] for c in pre) < dt.date(2026, 5, 1)
          <= min(c["dos"] for c in post), "%d retail-fee claims, %d after" % (len(pre), len(post)))
    moved = sum(int(round(gq[k]["guarantee"])) != int(round(fq_file[k]["guarantee"])) for k in fqs)
    check("ask A device moves every quarter's guarantee and shortfall", moved == 4 and
          all(round(gq[k]["shortfall"]) != round(fq_file[k]["shortfall"]) for k in fqs))
    check("ask A golden: a shortfall in Apr-Jun 2026 alone; the network file read as of every date puts one in all four",
          [k for k in fqs if gq[k]["shortfall"] > 0] == ["FQ4"] and all(fq_file[k]["shortfall"] > 0 for k in fqs))
    stmt_rem = pk.guarantee(rates, remit="statement")
    check("ask A hazard: remittances read by statement differ from the service-period sums in every quarter",
          all(round(stmt_rem[k]["remitted"]) != round(gq[k]["remitted"]) for k in fqs[:3]))
    edge = [abs(v - round(v)) for k in fqs for v in (gq[k]["remitted"], gq[k]["shortfall"])]
    check("ask A dollar figures sit at least five cents from a half dollar", all(abs(e - 0.5) > 0.05 for e in edge),
          str([round(e, 2) for e in edge]))
    roster = D["roster"]
    fam_rows = collections.defaultdict(list)
    for r in roster:
        fam_rows[r["cardholder_id"]].append(r)
    by_legacy = {r["legacy_cardholder_id"]: r["cardholder_id"] for r in roster if r["legacy_cardholder_id"]}
    old_pairs = {(c["card"], c["pc"], c["dob"], c["sex"]) for c in D["claims_all"] if c["dos"] < dt.date(2026, 1, 1)}
    moved_pc = 0
    for card, pc, dob, sex in old_pairs:
        new = by_legacy.get(card)
        if new:
            hit = [r for r in fam_rows[new] if A.parse_date(r["birth_date"]) == dob and r["gender"] == sex]
            if hit and hit[0]["person_code"] != pc:
                moved_pc += 1
    check("ask B device: dependants whose person code changed at the 1 January 2026 renumbering fill on both sides",
          moved_pc > 200, "%d old identities under another code" % moved_pc)
    check("ask B device: the roster links only subscribers to their old cardholder number",
          all(r["relationship_code"] == "E" for r in roster if r["legacy_cardholder_id"]) and
          sum(1 for r in roster if r["legacy_cardholder_id"]) > 20000)
    twins = sum(1 for rows_ in fam_rows.values() if len({(r["birth_date"], r["gender"]) for r in rows_}) < len(rows_))
    check("ask B fair: within every family birth date and gender name one member, so the match is unique", twins == 0)
    mem = pk.members()

    def crack(c):
        if c["dos"] >= dt.date(2026, 1, 1):
            return ("N", c["card"], c["pc"])
        new = by_legacy.get(c["card"])
        return ("N", new, c["pc"]) if new else ("O", c["card"], c["pc"])
    cm = pk.members({c["no"]: crack(c) for c in D["claims_all"]})
    nm = pk.members({c["no"]: (c["card"], c["pc"]) for c in D["claims_all"]})
    check("ask B: the carried person code misses at least 16 of 24 cells, the unlinked count every cell",
          sum(cm[k] != mem[k] for k in mem) >= 16 and all(nm[k] != mem[k] for k in mem),
          "%d and %d of 24" % (sum(cm[k] != mem[k] for k in mem), sum(nm[k] != mem[k] for k in mem)))
    check("separation: no ask device row reaches the main call (the call reads neither channel nor identity; R2k)",
          max(abs(blind[b] - gnet[b]) for b in pk.compared) < 1e-9)
    check("figures.json carries the golden's ask figures", all(figs["members.%s.%s" % k] == v for k, v in mem.items()) and
          all(figs["guar.%s.shortfall" % k] == int(round(gq[k]["shortfall"])) for k in fqs))

    # ================================================================ input gates, provenance, realism
    files = sorted(os.listdir(TARGET))
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("input gate: 3 or more formats", len(exts) >= 3, ",".join(sorted(exts)))
    nrows = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    check("input gate: a file of 25,000 rows or more", max(nrows.values()) >= 25000, str(nrows))
    check("input gate: two or more distractors named in metadata.json, none in a file name",
          len(meta["distractor_files"]) >= 2 and all(os.path.basename(p) in files for p in meta["distractor_files"]))
    check("every shipped file has a provenance record (source, date, licence)",
          sorted(os.path.basename(f["path"]) for f in meta["files"]) == files and
          all(f["source"] and f["date"] and f["licence"] for f in meta["files"]))
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += load_workbook(os.path.join(TARGET, f), read_only=True).sheetnames
    check("no readme, dictionary, notes or manifest file or sheet", not any(re.search(
        r"readme|dictionary|notes|manifest|schema|about", x, re.I) for x in files + sheets), ",".join(sheets))
    check("no file name carries an author word", not any(re.search(r"test|trap|decoy|answer|truth|device|golden", f, re.I)
                                                         for f in files))
    late = [c for c in D["claims_all"] if c["paid"] > dt.date(2026, 9, 30)]
    stamped = []
    for f in files:
        if f.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(TARGET, f)).read("docProps/core.xml").decode()
            stamped += re.findall(r"<dcterms:modified[^>]*>(\d{4}-\d\d-\d\d)", core)
    check("dates coherent: nothing paid after the 30 September 2026 extract cut, no file saved after the as-of date",
          not late and all(dt.date.fromisoformat(s) <= ASOF for s in stamped), "%d late, stamps %s" % (len(late), stamped))
    years = [int(y) for t in texts.values() for y in re.findall(r"\b(20\d\d)\b", t)]
    check("no document dated past 2027 or mentioning the golden's figures", max(years) <= 2027 and not any(
        str(figs["net." + b]) in t for t in texts.values() for b in pk.compared if figs["net." + b] > 999))
    check("PDF read-back: every document's text decodes (ASCII85 and Flate)", all(len(t) > 500 for t in texts.values()),
          str({f: len(t) for f, t in texts.items()}))
    allnames = set(re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", " ".join(texts.values())))
    people = {n for n in allnames if n.split()[0] in {"Maria", "Brenda", "Timothy", "Alyssa", "Tim"}}
    check("personas are the drawn ones only", people <= PEOPLE, ",".join(sorted(people)))
    tool = []
    for f in files + [os.path.join("..", "golden", x) for x in os.listdir(os.path.join(TASK, "golden"))]:
        b = open(os.path.join(TARGET, f), "rb").read()
        if f.endswith((".xlsx", ".pptx")):
            z = zipfile.ZipFile(os.path.join(TARGET, f))
            b = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps"))
        if re.search(rb"openpyxl|python-pptx|reportlab|ReportLab|xlsxwriter", b):
            tool.append(f)
    check("containers scrubbed of toolchain names", not tool, ",".join(tool))
    qcount = collections.Counter((c["acct"], c["fq"]) for c in pk.claims)
    check("realism: no two account-quarters carry the same claim count", len(set(qcount.values())) == len(qcount))
    amts = [l["amount"] for l in D["stmt"]]
    check("realism: no round remittance amounts", sum(1 for a in amts if abs(a) >= 1000 and a == round(a, -2)) == 0)
    ing = [c["ingr"] for c in pk.claims]
    check("realism: ingredient costs are not round", sum(1 for x in ing if x == round(x)) < 0.02 * len(ing))
    shares = [mem[k] for k in mem]
    check("realism: member counts are not all distinct multiples of ten",
          sum(1 for x in shares if x % 10 == 0) < len(shares) / 3)
    check("realism: the roster has no duplicate member id", len({r["member_id"] for r in roster}) == len(roster))
    check("realism: every pharmacy NPI passes the Luhn check with the 80840 prefix",
          all(_npi_ok(n) for n in D["network"]))

    # ================================================================ graded figures against their bins
    for b in pk.compared:
        check("bin %s: %d, %.2f from its band edge" % (b, r10(gnet[b]), band_dist(gnet[b])), band_dist(gnet[b]) >= 4.0
              and figs["net." + b] == r10(gnet[b]))
    for lab, n in (("current lines only", cur), ("statement quarters", stq)):
        moved_bins = [b for b in pk.compared if r10(n[b]) != r10(gnet[b])]
        check("non-compliant reading, %s: the call holds; bands moved: %s" % (lab, ", ".join(moved_bins) or "none"),
              picks_of(pk, n) == gold and len(moved_bins) <= 3)

    fails = [r for r in ROWS if not r[1]]
    for lab, ok, det in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", lab, ("  [%s]" % det) if det and not ok else ""))
    print("%d checks, %d FAIL" % (len(ROWS), len(fails)))
    return 1 if fails else 0


def _npi_ok(npi):
    digits = "80840" + npi[:9]
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10 == int(npi[9])


if __name__ == "__main__":
    sys.exit(main())
