"""Assertions for task451, run on the built pack (and on the generator's clean truth where the three rules ask for it):
the input gates, the golden read from the files against the simulated truth, the ladder's named threes, the
convergence of every attribution of a commingled fund's payments, the semantic fork rows SF1 to SF12, the three rules
executed, each Layer 1 item mishandled, the asks and their devices, the separation line, the bins, the realism and
hygiene sweeps, and the goldens against figures.json."""
import copy
import csv
import json
import os
import re
import sys
import zipfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C       # noqa: E402
import docs as DC      # noqa: E402
import golden as G     # noqa: E402
import pack as P       # noqa: E402
import reader as RD    # noqa: E402
import world as W      # noqa: E402

RESULTS = []
GOLD = ["Rwanda", "Kenya", "Mali"]


def ok(cond, label, detail=""):
    RESULTS.append((bool(cond), label, detail))
    print("  %s  %-78s %s" % ("ok  " if cond else "FAIL", label, detail))


def three(v):
    return sorted(C.top3(v)[0])


def dist(v):
    """How far a reading sits from the golden three: the best country outside it over the weakest inside it."""
    return max(v[c] for c in W.NAMES if c not in GOLD) / min(v[c] for c in GOLD)


def call(rows, fx, register, **kw):
    rows = C.dedup(rows) if not kw.get("nodedup") else rows
    mrefs = C.member_refs(register)
    ps = C.held_when_paid(rows, fx, mrefs, kw.get("method", "pro_rata"))
    sh = C.activity_shares(rows, fx, mrefs, pay_share=ps)
    return C.spending_by_country(rows, fx, sh)


def edge(v, places=1):
    """Distance from a value to the nearest rounding edge at the given places."""
    s = v * 10 ** places
    return abs((s - int(s)) - 0.5) / 10 ** places


def doc_text(target):
    from pypdf import PdfReader
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = " ".join(" ".join(pg.extract_text() for pg in PdfReader(p).pages).split())
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            out[f] = " ".join(str(c) for ws in wb for row in ws.iter_rows(values_only=True) for c in row if c is not None)
        elif f.endswith((".txt", ".xml")):
            out[f] = open(p, encoding="utf-8").read()
    return out


def run(target, golden, world=None, meta_path=None):
    print("task451 checks")
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else None
    # ------------------------------------------------------------------------------------------ input gates ----
    nrows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok(len(files) >= 10, "input gate: ten or more files", str(len(files)))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gate: three or more formats",
       ",".join(sorted({f.rsplit(".", 1)[1] for f in files})))
    ok(max(nrows.values()) >= 25000, "input gate: one file of 25,000 rows or more", str(max(nrows.values())))
    if meta:
        ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
           "input gate: two distractors named in metadata.json", ", ".join(meta["distractor_files"]))
        ok(not any("distract" in f.lower() for f in files), "input gate: no file named as a distractor")
    L = RD.load(target)
    rows, fx, reg, registry = L["rows"], L["fx"], L["register"], L["registry"]
    R = C.readings(rows, fx, reg)
    gold, gsh, ssh = R["golden"]
    # ------------------------------------------------------------------------- the files against the truth ----
    if world is not None:
        R0 = C.readings(C.rows_from_world(world), world["fx"], [dict(ref=W.M[k]["ref"], prev=W.M[k]["prev"]) for k in W.MEMBER_KEYS])
        ok(all(max(abs(R0[n][0][c] - R[n][0][c]) for c in W.NAMES) < 1e-9 for n in R),
           "every reading from the files equals the simulated truth", "%d readings" % len(R))
    # ------------------------------------------------------------------------------------------- the call ----
    top, margin = C.top3(gold)
    ok(sorted(top) == sorted(GOLD), "the call: Rwanda, Kenya and Mali", ", ".join(top))
    ok(margin >= 1.20, "the call: the third leads the fourth by 1.20x or more", "%.3f over %s" % (margin, sorted(gold, key=lambda c: -gold[c])[3]))
    ok(abs(gsh - 0.317) < 5e-5, "the global fund's 2025 grants carried the members' 31.7 per cent", "%.5f" % gsh)
    ok(abs(ssh - (4.59 / 29.80 + 17.84 / 29.80 * 0.317)) < 5e-5, "the Sahel fund's 2025 grants carried 34.4 per cent", "%.5f" % ssh)
    # --------------------------------------------------------------------------------------------- the ladder ----
    NAMED = {"same_year": ["Mali", "Rwanda", "Uganda"], "lifetime": ["Kenya", "Rwanda", "Uganda"],
             "cum_before_pay": ["Kenya", "Rwanda", "Tanzania"], "prior_year": ["Kenya", "Rwanda", "Tanzania"],
             "golden_one": ["Kenya", "Rwanda", "Tanzania"], "same_year_one": ["Kenya", "Rwanda", "Uganda"],
             "lifetime_one": ["Kenya", "Rwanda", "Uganda"], "none": ["Kenya", "Rwanda", "Tanzania"],
             "pay": ["Kenya", "Nepal", "Rwanda"], "over": ["Mali", "Rwanda", "Uganda"], "s_full": ["Mali", "Niger", "Rwanda"],
             "mean_annual": ["Kenya", "Rwanda", "Uganda"]}
    for nm, want in NAMED.items():
        v = R[nm][0]
        ok(three(v) == want and dist(v) >= 1.12, "rung %s: %s, 1.12x or more from the golden three" % (nm, ", ".join(want)),
           "%s, %.3f" % (", ".join(three(v)), dist(v)))
    ok(R["same_year"][1] > 0.74 and R["same_year"][2] > 0.60, "R0 the year's share: 74.6 and 60.1 per cent",
       "%.4f %.4f" % R["same_year"][1:])
    ok(len({tuple(three(R[n][0])) for n in ("same_year", "lifetime", "cum_before_pay")} | {tuple(sorted(GOLD))}) == 4,
       "R0, R1, R2 and the golden name four different threes")
    # grid: two depths by five share bases, the golden three in one cell
    cells = {}
    mrefs = C.member_refs(reg)
    drows = C.dedup(rows)
    for base, (gy, sy) in {"year": ([2025], [2025]), "every": ([2023, 2024, 2025], [2024, 2025, 2026]),
                           "previous": ([2024], [2024])}.items():
        for rec in (True, False):
            g, s = C.fund_shares_simple(drows, fx, mrefs, gy, sy, rec)
            if base == "previous":
                s = C.fund_shares_simple(drows, fx, mrefs, [2023], [2024], rec)[1]
            cells[(base, rec)] = three(C.spending_by_country(drows, fx, C.activity_shares(drows, fx, mrefs, fund_share={C.GREF: g, C.SREF: s})))
    g, s = C._cum_before(drows, fx, mrefs)
    cells[("before", True)] = three(C.spending_by_country(drows, fx, C.activity_shares(drows, fx, mrefs, fund_share={C.GREF: g, C.SREF: s})))
    s1 = C.fund_shares_simple(drows, fx, mrefs, [2023, 2024], [2024, 2025], False)[1]
    cells[("before", False)] = three(C.spending_by_country(drows, fx, C.activity_shares(drows, fx, mrefs, fund_share={C.GREF: g, C.SREF: s1})))
    cells[("held", True)] = sorted(top)
    cells[("held", False)] = three(R["golden_one"][0])
    ok(sum(1 for v in cells.values() if v == sorted(GOLD)) == 1 and len(cells) == 10,
       "grid: two depths by five share bases, the golden three in one cell", str(sorted(cells.items())))
    # ------------------------------------------------------------------------ SF5: every attribution agrees ----
    ps = {m: C.held_when_paid(drows, fx, mrefs, m) for m in ("pro_rata", "fifo", "lifo")}
    keys25 = [k for k in ps["pro_rata"] if k[2].year == 2025]
    ok(all(abs(ps["pro_rata"][k] - ps[m][k]) < 1e-9 for m in ("fifo", "lifo") for k in keys25),
       "SF5 C1: pro rata, first in first out and last in first out give every 2025 payment the same member share",
       "%d payments" % len(keys25))
    for m in ("fifo", "lifo"):
        v = call(rows, fx, reg, method=m)
        ok(max(abs(v[c] - gold[c]) for c in W.NAMES) < 1e-9, "SF5 the golden under %s" % m)
    gpay = [r for r in drows if r["rep"] == C.GREF and r["ttype"] == "3" and r["tdate"].year == 2025]
    grec = [r for r in drows if r["rep"] == C.GREF and r["ttype"] == "1" and r["tdate"].year == 2025]
    ok(max(r["tdate"] for r in gpay) < min(r["tdate"] for r in grec),
       "SF5 the global fund's 2025 collection arrived after its last 2025 payment",
       "%s before %s" % (max(r["tdate"] for r in gpay), min(r["tdate"] for r in grec)))
    g23 = sum(C.usd(r, fx) for r in drows if r["rep"] == C.GREF and r["ttype"] == "1" and r["tdate"].year == 2023)
    g24p = sum(C.usd(r, fx) for r in drows if r["rep"] == C.GREF and r["ttype"] == "3" and r["tdate"].year == 2024)
    ok(abs(g23 - g24p) < 0.01, "SF5 the global fund paid out its 2023 collection in full in 2024", "%.2f %.2f" % (g23, g24p))
    s24r = sum(C.usd(r, fx) for r in drows if r["rep"] == C.SREF and r["ttype"] == "1" and r["tdate"].year == 2024)
    s24p = sum(C.usd(r, fx) for r in drows if r["rep"] == C.SREF and r["ttype"] == "3" and r["tdate"].year == 2024)
    ok(abs(s24r - s24p) < 0.01, "SF5 the Sahel fund paid out its 2024 round in full in 2024", "%.2f %.2f" % (s24r, s24p))
    # --------------------------------------------------------------------------------------- the fork table ----
    ok(len(reg) == 6 and not any(r["prov_ref"] in mrefs for r in drows if r["rep"] not in (C.GREF, C.SREF) and r["ttype"] == "1"
                                 and r["prov_ref"] in {p["ref"] for p in W.PARTNERS.values()}),
       "SF1 six members on the register; no partner or other donor is a member")
    # SF2: for the funds' money, the funds' 2025 payments by country equal the grantees' 2025 spending
    fund_exp = {c: 0.0 for c in W.NAMES}
    fund_pay = {c: 0.0 for c in W.NAMES}
    shares = C.activity_shares(drows, fx, mrefs, pay_share=ps["pro_rata"])
    for r in drows:
        if r["tdate"].year != 2025:
            continue
        if r["ttype"] == "4" and r["funding"] and r["funding"][0] in (C.GREF, C.SREF):
            for iso, pct in C.countries_of(r):
                fund_exp[W.NAME_OF[iso]] += C.usd(r, fx) * shares[r["aid"]] * pct / 100
        if r["ttype"] == "3" and r["rep"] in (C.GREF, C.SREF) and r["hierarchy"] == "2":
            sh = ps["pro_rata"][(r["rep"], r["aid"], r["tdate"], round(r["value"], 2))]
            for iso, pct in C.countries_of(r):
                fund_pay[W.NAME_OF[iso]] += C.usd(r, fx) * sh * pct / 100
    ok(max(abs(fund_exp[c] - fund_pay[c]) for c in W.NAMES) < 1.0, "SF2 the funds' money: their 2025 payments by country equal "
       "the grantees' 2025 spending (each grant spent in the year paid)", "%.4f" % max(abs(fund_exp[c] - fund_pay[c]) for c in W.NAMES))
    ok(three(R["pay"][0]) == ["Kenya", "Nepal", "Rwanda"], "SF2 the members' payments as spending: Rwanda, Nepal and Kenya")
    exp25 = [r for r in drows if r["ttype"] == "4" and r["tdate"].year == 2025]
    ok(all((r["vdate"] or r["tdate"]).year == 2025 for r in exp25), "SF3 every 2025 expenditure has its value date in 2025")
    ok(three(R["none"][0]) != sorted(GOLD) and three(R["golden_one"][0]) != sorted(GOLD) and three(R["over"][0]) != sorted(GOLD),
       "SF4 the donor view, one fund deep and the funds counted in full each miss the golden three")
    # SF6: the conversion date and basis
    avg = {c: {} for c in fx}
    for c in fx:
        for y in (2023, 2024, 2025, 2026):
            vals = [v for d, v in fx[c].items() if d.year == y]
            avg[c][y] = sum(vals) / len(vals)
    fx_avg = {c: {d: avg[c][d.year] for d in fx[c]} for c in fx}
    v_avg = call(rows, fx_avg, reg)
    ok(three(v_avg) == sorted(GOLD), "SF6 the year's average rate: the same call", ", ".join(three(v_avg)))
    rows_td = [dict(r, vdate=None) for r in rows]
    ok(three(call(rows_td, fx, reg)) == sorted(GOLD), "SF6 the transaction date's rate: the same call")
    # SF7: a multi-country activity wholly in its first country
    rows_first = [dict(r, countries=r["countries"][:1] and [(r["countries"][0][0], 100.0)]) for r in rows]
    ok(three(call(rows_first, fx, reg)) == sorted(GOLD), "SF7 multi-country activities in their first country: the same call")
    ok(margin >= 1.20, "SF8 no tie at the third place", "%.3f" % margin)
    pool = [r for r in drows if r["aid"].endswith("-POOL")]
    ok(all(not r["countries"] for r in pool), "SF9 the funds' pooled activities name no country (the transfer is in no country)")
    ok(all(r["countries"] or r["tcountry"] for r in exp25), "SF10 every 2025 expenditure has a country")
    pubs = {r["rep"] for r in drows}
    find = C.org_resolver(registry)
    published = {find(x) for x in pubs}
    paid = {r["recv_ref"] for r in drows if r["ttype"] == "3" and (r["rep"] in mrefs or r["rep"] in (C.GREF, C.SREF))
            and r["tdate"].year == 2025}
    ok(all(find(x) in published for x in paid), "SF11 every organisation the members and the funds paid in 2025 publishes",
       "%d receivers" % len(paid))
    ok(not any(r["ttype"] == "4" and r["rep"] in mrefs for r in drows), "SF12 no member reports expenditure of its own")
    ok(sum(1 for r in drows if r["ttype"] == "4" and r["tdate"].year == 2025 and r["rep"] in (C.GREF, C.SREF)) == 0,
       "SF12 the funds report no expenditure of their own")
    # ----------------------------------------------------------------------------------------- three rules ----
    ok(any(r["ttype"] == "4" for r in rows) and any(r["ttype"] == "1" and r["rep"] == C.GREF for r in rows),
       "R1 the field's raw material ships: transactions, the funds' receipts and payments")
    hdr = open(os.path.join(target, P.FILES["datastore"]), encoding="utf-8").readline().lower()
    ok(not re.search(r"member|share|attribut|imput", hdr), "R1 no shipped column holds a member share or an imputed amount")
    # R2: each Layer 1 item mishandled leaves the call
    rows_usd = [dict(r, ccy=r["ccy"] or "USD") for r in rows]
    ok(three(call(rows_usd, fx, reg)) == sorted(GOLD), "R2 a currency left to the activity default read as US dollars: the same call")
    ok(three(call(rows_first, fx, reg)) == sorted(GOLD), "R2 multi-country percentages ignored: the same call")
    reg_nolegacy = [dict(m, prev=None) for m in reg]
    ok(three(call(rows, fx, reg_nolegacy)) == sorted(GOLD), "R2 the member's previous identifier unmapped: the same call")
    rows_scr = [dict(r, recv_ref=(r["recv_ref"] + "-X") if r["recv_ref"] and r["rep"] in mrefs else r["recv_ref"]) for r in rows]
    ok(three(call(rows_scr, fx, reg)) == sorted(GOLD), "R2 receivers under other identifiers: the same call")
    rows_dup = rows + [r for r in rows if r["source"] in ("gxml", "sxml") and r["hierarchy"] == "2"]
    ok(three(call(rows_dup, fx, reg)) == sorted(GOLD), "R2 the funds' grant activities read twice (files and Datastore): the same call")
    rows_inc = rows + [dict(r, ttype="4") for r in rows if r["ttype"] == "1" and r["rep"] not in (C.GREF, C.SREF)
                       and r["tdate"].year == 2025 and r["prov_ref"] in mrefs and False]
    # R3: the analyst test on the clean truth
    if world is not None:
        truth = C.rows_from_world(world)
        R3 = C.readings(truth, world["fx"], [dict(ref=W.M[k]["ref"], prev=W.M[k]["prev"]) for k in W.MEMBER_KEYS])
        ok(three(R3["same_year"][0]) == ["Mali", "Rwanda", "Uganda"],
           "R3a the default path on the clean truth, every filed rule applied: Rwanda, Uganda and Mali")
        ok(three(R3["golden"][0]) == sorted(GOLD), "R3b the default path with only the decisive step changed: the golden")
        ok(all(three(R3[n][0]) != sorted(GOLD) for n in ("lifetime", "cum_before_pay", "prior_year", "golden_one")),
           "R3b each lower rung's single correction leaves a wrong three")
    D = doc_text(target)
    allt = " ".join(D.values()).lower()
    ok(not re.search(r"held when|balance|money held|paid out .{0,20}following year|in arrears|carry.{0,20}share", allt),
       "R3c no shipped text states a fund's balance, cash cycle or which money a grant used")
    ok(not re.search(r"(rwanda|kenya|mali)[^.]{0,80}(first|top|lead|highest)", allt), "R3c no shipped document ranks the countries")
    # ----------------------------------------------------------------------------------------------- the asks ----
    b = C.ask_pipeline(rows, fx, reg)
    bn = C.ask_pipeline(rows, fx, reg, drop_superseded=False)
    c_ = C.ask_orgs(rows, reg, registry)
    cn = C.ask_orgs(rows, reg, registry, resolve=False)
    ok(all("%.1f" % b[k] != "%.1f" % bn[k] for k in W.NAMES), "Ask B device: the old copies move every country's figure",
       "min gap %.2f" % min(bn[k] - b[k] for k in W.NAMES))
    ok(all(c_[k] != cn[k] for k in W.NAMES), "Ask C device: identifiers counted move every country's count",
       "%s" % [cn[k] - c_[k] for k in W.NAMES])
    old = C.superseded(drows)
    ok(len(old) == 13 and all(r["updated"].date() == W.OLD_DATASET_UPDATED.date() for r in drows if r["aid"] in old)
       and max(r["tdate"] for r in drows if r["aid"] in old) <= W.OLD_DATASET_UPDATED.date(),
       "Ask B the old copies: 13 activities, last updated 14 June 2024, nothing dated after", str(len(old)))
    ok({W.NAME_OF[r["countries"][0][0]] for r in drows if r["aid"] in old} == set(W.NAMES), "Ask B the old copies cover all 13 countries")
    ok(all(any(f(x) == f(y) for f in (find,) for x in (d[3],) for y in (d[5],)) for d in W.DEVICE_ORGS),
       "Ask C the publisher list joins each re-registered organisation's two identifiers")
    # the separation line: the main call reads no commitment, no member payment, no old copy, no receiver identifier
    rows_noold = [r for r in rows if r["aid"] not in old]
    ok(max(abs(call(rows_noold, fx, reg)[c] - gold[c]) for c in W.NAMES) < 1e-9, "separation: deleting the old copies moves no main figure")
    rows_nomp = [r for r in rows if not (r["rep"] in mrefs and r["ttype"] in ("2", "3") and r["countries"])]
    ok(max(abs(call(rows_nomp, fx, reg)[c] - gold[c]) for c in W.NAMES) < 1e-9,
       "separation: deleting the members' commitments and payments to organisations moves no main figure")
    ok(max(abs(call(rows_scr, fx, reg)[c] - gold[c]) for c in W.NAMES) < 1e-9, "separation: receiver identifiers move no main figure")
    # bins: every graded figure clear of a rounding edge
    e_a = min(edge(gold[c]) for c in W.NAMES)
    e_b = min(edge(b[c]) for c in W.NAMES)
    ok(e_a >= 0.005, "bins: every Ask A figure at least USD 5,000 from a rounding edge", "%.4f" % e_a)
    ok(e_b >= 0.005, "bins: every Ask B figure at least USD 5,000 from a rounding edge", "%.4f" % e_b)
    ok(edge(100 * gsh) >= 0.01 and edge(100 * ssh) >= 0.01, "bins: both fund shares clear of a rounding edge",
       "%.3f %.3f" % (100 * gsh, 100 * ssh))
    # ----------------------------------------------------------------------------------- realism and hygiene ----
    ok(len({round(gold[c], 2) for c in W.NAMES}) == 13, "realism: no two countries with the same figure")
    ok(max(r["tdate"] for r in drows) <= W.EXTRACT_TO, "realism: nothing dated after the extract's end")
    upd = {}
    for r in drows:
        upd.setdefault(r["aid"], [r["updated"], r["tdate"]])
        upd[r["aid"]][1] = max(upd[r["aid"]][1], r["tdate"])
    ok(all(u.date() >= t for u, t in upd.values()), "realism: every activity updated on or after its latest transaction")
    ok(all(u <= W.PULL for u, _ in upd.values()), "realism: every activity updated before the pull")
    ids = [r["aid"] for r in drows if r["source"] == "datastore"]
    ok(len(set(ids)) == len({(r["aid"], r["rep"]) for r in drows if r["source"] == "datastore"}),
       "hygiene: one reporting organisation per activity identifier")
    dsrows = [r for r in rows if r["source"] == "datastore"]
    keys = [(r["aid"], r["ttype"], r["tdate"], r["value"], r["prov_ref"], r["recv_ref"]) for r in dsrows]
    ok(len(keys) == len(set(keys)), "hygiene: no exact duplicate row in the extract")
    for f_ in files:
        bb = open(os.path.join(target, f_), "rb").read()
        ok(not re.search(rb"(?i)reportlab|openpyxl|python-pptx|matplotlib", bb), "H1 no writer's name in %s" % f_)
        ok("—".encode() not in bb, "standing rule: no em dash in %s" % f_)
    for f_ in os.listdir(golden):
        bb = open(os.path.join(golden, f_), "rb").read()
        if f_.endswith(".pptx"):
            with zipfile.ZipFile(os.path.join(golden, f_)) as z:
                bb = b" ".join(z.read(n) for n in z.namelist() if not n.endswith(".png"))
        ok(not re.search(rb"(?i)openpyxl|python-pptx|matplotlib", bb), "H1 no writer's name in golden %s" % f_)
        ok("—".encode() not in bb, "standing rule: no em dash in golden %s" % f_)
    people = re.findall(r"(Lesley Hunter|Lee Sykes|Gail Dobson|Kieran Patel)", " ".join(D.values()))
    ok(len(people) >= 3, "realism: the personas in the pack are the drawn ones", str(sorted(set(people))))
    # ------------------------------------------------------------------------------------- the deliverables ----
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ok(sorted(fig["call"]) == sorted(GOLD), "figures.json: the call")
    with open(os.path.join(golden, G.CSV), newline="") as fh:
        got = list(csv.DictReader(fh))
    ok(len(got) == 13 and [g_["country"] for g_ in got] == W.NAMES, "csv: one row per country, 13 rows")
    ok(all(g_["members_money_spent_2025_usd_m"] == "%.1f" % gold[g_["country"]] for g_ in got), "csv: Ask A figures")
    ok(all(g_["committed_not_paid_2026_06_30_usd_m"] == "%.1f" % b[g_["country"]] for g_ in got), "csv: Ask B figures")
    ok(all(int(g_["organisations_paid_directly_2025"]) == c_[g_["country"]] for g_ in got), "csv: Ask C counts")
    ok(all(fig["spent_2025_usd_m"][k] == "%.1f" % gold[k] for k in W.NAMES), "figures.json: Ask A figures agree with the csv")
    from pptx import Presentation
    prs = Presentation(os.path.join(golden, G.PPTX))
    body = " ".join(sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame)
    body += " " + " ".join(c.text for s in prs.slides for sh in s.shapes if sh.has_table for r in sh.table.rows for c in r.cells)
    ok(all(c in body for c in GOLD), "pptx: the three countries named")
    ok(all(fig["spent_2025_usd_m"][c] in body for c in GOLD), "pptx: the three countries' figures")
    ok(fig["global_fund_member_share_pct"] in body and fig["sahel_fund_member_share_pct"] in body, "pptx: both fund shares")
    ok(sum(1 for s in prs.slides for sh in s.shapes if sh.shape_type == 13) == 1, "pptx: the chart of every country")
    ok(len(prs.slides) == 4, "pptx: four slides")
    if meta:
        ok(set(meta["distractor_files"]) == {P.FILES[k] for k in P.DISTRACTORS}, "distractors: metadata names both")
    ok(all(("SF%d" % i) in open(__file__).read() for i in range(1, 13)), "every SF row SF1 to SF12 asserted here")
    nfail = sum(1 for c, _, _ in RESULTS if not c)
    print("task451 checks: %d passed%s" % (len(RESULTS) - nfail, (", %d FAILED" % nfail) if nfail else ""))
    if nfail:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    import sim
    TASK = os.path.dirname(HERE)
    run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=sim.simulate(), meta_path=os.path.join(TASK, "metadata.json"))
