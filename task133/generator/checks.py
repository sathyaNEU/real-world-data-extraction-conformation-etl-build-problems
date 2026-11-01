"""Generator checks for task133 architecture 3, run on the installed target/ and the world's clean truth.

    python3 task133/generator/checks.py            # exit 1 on any failed assertion
"""
import csv
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TDIR = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402
import docs  # noqa: E402
import make_pack  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402
import world  # noqa: E402
import world_asks  # noqa: E402
from io_util import pdf_text  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + str(detail) + "]") if detail else ""))


def seg_bins(seg):
    return {s: R.rhu(seg[s] / 1e6, 1) for s in R.SEG_NAMES}


def same_call(res_entry, gold_total_bin, gold_seg_bins):
    t, seg, _ = res_entry
    return R.half_million(t) == gold_total_bin and seg_bins(seg) == gold_seg_bins


def edge_half(x_m):
    """Distance of a figure in NZD million from the nearest 0.5-million rounding edge (x.25, x.75)."""
    return min(abs(x_m - (k + 0.25)) for k in [i * 0.5 for i in range(-2, 80)])


def edge_tenth(x):
    return 0.05 - abs(x - round(x, 1))


def docx_text(path):
    from docx import Document
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


def main():
    files = sorted(os.listdir(TDIR))
    F = R.compute(TDIR)
    pk, res = A.ladder(TDIR)
    gtot = F["total_half_m"]
    gseg = F["seg_m1"]
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    std_text = docx_text(os.path.join(TDIR, docs.STANDARD))

    # ------------------------------------------------------------------ input gates
    check("gate: 10 or more files", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(TDIR, f), encoding="utf-8") as h:
                rows[f] = sum(1 for _ in h) - 1
    big = max(rows.values())
    check("gate: a file of 25,000 or more rows", big >= 25000, big)
    check("gate: the bulk file is lean (under 250,000 rows)", big < 250000, big)
    check("gate: two or more distractors named in metadata.json",
          len(meta["distractor_files"]) >= 2 and all(d["file"] in files for d in meta["distractor_files"]),
          [d["file"] for d in meta["distractor_files"]])
    bad_names = [f for f in files if re.search(r"readme|dictionar|notes|manifest|schema|test_|trap|decoy|answer|key_", f, re.I)]
    check("gate: no file describes the data or carries an author word in its name", not bad_names, bad_names)
    check("gate: the deliverables are named and exist in golden/",
          all(os.path.exists(os.path.join(TASK, "golden", d)) for d in meta["deliverables"]), meta["deliverables"])

    # ------------------------------------------------------------------ the three rules on the clean truth
    W = world.make()
    truth_payer = world.stressed_loss(W, lambda b: world.payer_change(b, W))
    truth_own = world.stressed_loss(W, world.own_change)
    check("R1 the field's raw material ships: one row per operating-account credit with the payer as the clearing "
          "system sends it, the register's BIC codes, the facility-level book",
          rows["operating_account_credits_2025-10_to_2026-09.csv"] >= 25000 and "bic_code" in open(
              os.path.join(TDIR, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv"), encoding="utf-8").readline()
          and rows["business_lending_book_2026-09-30.csv"] == sum(len(b["facs"]) for b in W.borrowers),
          rows["operating_account_credits_2025-10_to_2026-09.csv"])
    headers = []
    for f in files:
        if f.endswith(".csv"):
            headers += open(os.path.join(TDIR, f), encoding="utf-8").readline().strip().lower().split(",")
    deciding = [h for h in headers if re.search(r"payer|source_div|sales_change|stress|mix|counterparty_ind", h)]
    check("R2 the deciding quantity has no column: no file stores a borrower's payers' divisions or its sales change",
          not deciding, deciding)
    check("R3a the analyst test on the clean truth: the borrower's own-division path files a different bin from the "
          "path through its payers (NZD million, nearest 0.5)",
          R.half_million(truth_own) != R.half_million(truth_payer) and R.half_million(truth_payer) == gtot,
          "own %.3f -> %.1f, payers %.3f -> %.1f" % (truth_own / 1e6, R.half_million(truth_own), truth_payer / 1e6,
                                                   R.half_million(truth_payer)))
    cheap = ["R0_own_division", "R1_division_average_mix", "R2_acquirer_as_payer", "R3_more_severe_of_two",
             "V_count_weights", "V_households_at_retail"]
    landing = [k for k in cheap if same_call(res[k], gtot, gseg)]
    check("R3b cheap routes that land the call on the clean pack: none of the enumerated reflexes", not landing,
          {k: round(res[k][0] / 1e6, 3) for k in cheap})
    honest = ["V_legal_names_only", "V_government_as_O", "V_legacy_letters", "V_last_six_months"]
    check("R3b the defensible family lands the call: legal names only, public bodies as division O, the book's legacy "
          "codes, a six-month base", all(same_call(res[k], gtot, gseg) for k in honest),
          {k: round(res[k][0] / 1e6, 3) for k in honest})
    stressed_words = []
    for f in files:
        p = os.path.join(TDIR, f)
        if f.endswith(".csv"):
            txt = open(p, encoding="utf-8").read(200000)
        elif f.endswith(".docx"):
            txt = docx_text(p)
        elif f.endswith(".pdf"):
            txt = pdf_text(p)
        else:
            continue
        if f != docs.RURAL_PDF and re.search(r"stress[^\n]{0,80}NZD\s*[\d.,]+\s*(million|m\b)|NZD\s*[\d.,]+\s*million"
                                             r"[^\n]{0,80}stress", txt, re.I):
            stressed_words.append(f)
    check("R3c no decoy: no shipped file states a business-book stressed loss or ranks its segments (the rural "
          "summary is the rural book, a declared distractor)", not stressed_words, stressed_words)
    graded = [f"{gtot:.1f}"] + [f"{v:.1f}" for v in gseg.values()]
    hits = []
    for f in (docs.STANDARD, docs.RURAL_PDF):
        txt = docx_text(os.path.join(TDIR, f)) if f.endswith(".docx") else pdf_text(os.path.join(TDIR, f))
        hits += [(f, g) for g in graded if re.search(r"(NZD|\$)\s*%s(?![\d])|(?<![\d.])%s\s*(million|m\b)"
                                                    % (re.escape(g), re.escape(g)), txt)]
    check("R3c no certified replay: no governing or published document carries a graded figure of the call to "
          "reproduce", not hits, hits)

    # ------------------------------------------------------------------ semantic fork table
    t, seg, per = res["golden"]
    recomputed = 0.0
    for c in pk.cust.values():
        if c["grade"] == "D":
            continue
        ch, m, l = per[c["cust"]]
        pd = min(1.0, P.GRADE_PD[int(c["grade"])] / 100.0 * m)
        recomputed += sum(pd * P.LGD[f["security_code"]] * pk.ead(f) for f in c["facs"])
    check("SF1 stressed loss is PD x LGD x EAD summed over facilities (CR-ST-02 3.1)", abs(recomputed - t) < 0.01,
          round(recomputed))
    check("SF2 the stress year is the twelve months after the book date and Table 1 is a 12-month PD",
          docs.S_YEAR in std_text and "12-month probability of default" in std_text)
    oth = F["other_share_pct"]
    check("SF3 own sales are what the borrower's payers pay it: the receipts put %d per cent of trading credits with "
          "payers outside the borrower's division, and the own-division path files another bin" % oth,
          oth >= 40 and R.half_million(res["R0_own_division"][0]) != gtot and docs.S_PD in std_text
          and "own sales" in docs.S_PD and "the division's sales" in docs.S_SCEN,
          "R0 %.3f" % (res["R0_own_division"][0] / 1e6))
    check("SF4 credits that are not sales (transfers, GST refunds, claims, advances, interest) left in: same call",
          same_call(res["V_nonsales_included"], gtot, gseg), round(res["V_nonsales_included"][0] / 1e6, 3))
    check("SF5 the base is the year to the book date: a six-month base is the same call; the last quarter alone "
          "breaks the scenario's stated base year",
          same_call(res["V_last_six_months"], gtot, gseg) and "against the year to the book date" in docs.S_SCEN,
          round(res["V_last_quarter"][0] / 1e6, 3))
    with open(os.path.join(TDIR, "operating_account_credits_2025-10_to_2026-09.csv"), encoding="utf-8") as h:
        cred = list(csv.DictReader(h))
    ms = [r for r in cred if r["tran_type"] == "MS"]
    check("SF6 card settlement batches are cardholders' spending: every MS credit is a SETTLEMENT batch from one of "
          "two acquirers, and reading the acquirer as the payer files another bin",
          {r["particulars"] for r in ms} == {"SETTLEMENT"} and len({r["other_party"] for r in ms}) == 2
          and R.half_million(res["R2_acquirer_as_payer"][0]) != gtot, round(res["R2_acquirer_as_payer"][0] / 1e6, 3))
    check("SF7 public bodies at their own BIC division, or all at division O: same call",
          same_call(res["V_government_as_O"], gtot, gseg), round(res["V_government_as_O"][0] / 1e6, 3))
    check("SF8 the borrower's division from the NZBN register (CR-ST-02 4.1) or the book's legacy code letters: same call",
          same_call(res["V_legacy_letters"], gtot, gseg) and "own division on the NZBN register" in docs.S_SEG)
    check("SF9 payers matched on legal names only, without trading names: same call",
          same_call(res["V_legal_names_only"], gtot, gseg), round(res["V_legal_names_only"][0] / 1e6, 3))
    from openpyxl import load_workbook
    sc = load_workbook(os.path.join(TDIR, docs.SCENARIO), read_only=True)["Industry sales"]
    sc_head = [c for c in list(sc.iter_rows(min_row=4, max_row=4, values_only=True))[0] if c]
    check("SF10 sales weighted by count of credits instead of amount files another bin; the scenario states sales as "
          "amounts in NZD million", R.half_million(res["V_count_weights"][0]) != gtot
          and any("NZD million" in str(h) for h in sc_head), round(res["V_count_weights"][0] / 1e6, 3))
    priv = set()
    for r in cred:
        c = pk.cust.get(r["customer_no"])
        if c and r["tran_type"] == "DC":
            kind, _ = pk.classify(r, c)
            if kind == "PRIV":
                priv.add(r["other_party"])
    corp = [p for p in priv if re.search(r"\b(LTD|LIMITED|TRUST|HOLDINGS|GROUP)\b", p)]
    check("SF11 payments from individuals are household sales: no unmatched payer carries a company word, and leaving "
          "them out keeps the book total's bin", not corp and R.half_million(res["V_private_payers_left_out"][0]) == gtot,
          "%d unmatched payer names; private-out total %.3f" % (len(priv), res["V_private_payers_left_out"][0] / 1e6))
    check("SF12 household spending at the borrower's own division, not the retail path for every borrower (another bin)",
          R.half_million(res["V_households_at_retail"][0]) != gtot, round(res["V_households_at_retail"][0] / 1e6, 3))
    products = {f["product"] for f in pk.book}
    check("SF13 exposure at default: revolving products are exactly the overdraft and the revolving credit facility",
          P.REVOLVING <= products and docs.S_EAD in std_text, sorted(products))
    check("SF14 customers in risk grade D are outside the stress", F["n_default"] > 0 and docs.S_DEFAULT in std_text,
          F["n_default"])
    falls = [-per[c][0] for c in per]
    near = [x for x in falls if any(abs(x - e) < 0.02 for e in (5, 10, 15, 20, 25, 30))]
    check("SF15 no borrower's sales fall sits within 0.02 points of a Table 2 band edge", not near, len(near))
    capped = sum(1 for c in pk.cust.values() if c["grade"] != "D"
                 and P.GRADE_PD[int(c["grade"])] / 100.0 * per[c["cust"]][1] > 1.0)
    check("SF16 the 100 per cent cap on stressed PD binds for no borrower", capped == 0, capped)
    rises = sum(1 for x in falls if x <= 0)
    check("SF17 a borrower whose sales do not fall keeps its 12-month PD (multiplier 1)",
          all(per[c][1] == 1.0 for c in per if per[c][0] >= 0) and "keeps its 12-month probability" in docs.S_PD, rises)
    check("SF18 a borrower's segment follows its own division on the register (Table 4 covers every division held)",
          all(c["div"] in P.SEG_OF for c in pk.cust.values()))
    check("SF19 rounding: the book total sits 0.1 or more from a 0.5-million edge and every segment at least 0.04 from "
          "a 0.1-million edge", edge_half(t / 1e6) >= 0.1 and min(edge_tenth(seg[s] / 1e6) for s in R.SEG_NAMES) >= 0.04,
          "%.3f; %.3f" % (edge_half(t / 1e6), min(edge_tenth(seg[s] / 1e6) for s in R.SEG_NAMES)))

    a = F["ask_a"]
    wo_rows = list(csv.DictReader(open(os.path.join(TDIR, "write_offs_2023-10_to_2026-09.csv"), encoding="utf-8")))
    check("SF20 halves of the financial year to 30 September (CR-ST-02 2.3): write-offs and receipts fall in "
          "October to March or April to September", docs.S_FY in std_text and all(
              A.half(A._d(r["posting_date"])) in (None, "H1", "H2") for r in wo_rows))
    alt = alt_recovery_by_writeoff_half(TDIR)
    check("SF21 recoveries counted in the half received (CR-ST-02 4.2), not the half of the write-off (another set)",
          alt != F["ask_a_k"] and "in the half" in docs.S_NCL)
    gross = R.ask_a_detail(TDIR, agency_upload=True)["net"]
    check("SF22 the recovery is what the bank received: the agency's statement upload counted beside the remittance "
          "moves every cell", all(R.rhu(gross[k] / 1e3, 0) != F["ask_a_k"][k] for k in gross) and "received" in docs.S_NCL)
    pre = R.ask_a_detail(TDIR, pre_writeoff=True)["net"]
    check("SF23 only receipts on loans already written off: receipts before the first write-off moved cells",
          sum(R.rhu(pre[k] / 1e3, 0) != F["ask_a_k"][k] for k in pre) >= 8 and "already written off" in docs.S_NCL)
    check("SF24 the business book only: rural and commercial property write-offs are in the extract and outside CR-ST-02",
          {r["portfolio"] for r in wo_rows} == {"Business", "Rural", "Commercial property"} and docs.S_SCOPE in std_text)
    cm = {r["customer_no"]: r for r in csv.DictReader(open(os.path.join(TDIR, "customer_master_extract_2026-10-09.csv"),
                                                             encoding="utf-8"))}
    reg_nzbn = {r["nzbn"] for r in pk.reg}
    biz_wo = {r["customer_no"] for r in wo_rows if r["portfolio"] == "Business"}
    check("SF25 every written-off business customer reaches a register division through the customer master's NZBN",
          all(c in cm and cm[c]["nzbn"] in reg_nzbn for c in biz_wo), len(biz_wo))
    mg = R.ask_b_raw(TDIR, overrides=False)
    check("SF26 risk grade in force (an approved override while it is in force): the model grade alone moves bands",
          mg != F["ask_b"] and docs.S_GRADE in std_text)
    regs = []
    for f in ("default_register_business_FY2026.csv", "default_register_rural_FY2026.csv"):
        regs += list(csv.DictReader(open(os.path.join(TDIR, f), encoding="utf-8")))
    check("SF27 the registers hold only defaults dated 1 October 2025 to 30 September 2026",
          all(P.WIN_START <= A._d(r["default_date"]) <= P.WIN_END for r in regs), len(regs))
    snap = list(csv.DictReader(open(os.path.join(TDIR, "risk_grade_snapshot_2025-09-30.csv"), encoding="utf-8")))
    dn = sum(1 for r in snap if r["model_grade"] == "D")
    check("SF28 grade D customers at 30 September 2025 sit in no band (no band's count includes them)",
          dn > 0 and sum(n for n, d in F["ask_b"].values()) == len(snap) - dn, dn)
    check("SF29 each share is the band's defaults over the band's borrowers", all(
        F["ask_b_share"][k] == R.rhu(100.0 * d / n, 1) for k, (n, d) in F["ask_b"].items()) and "share of the band" in docs.S_BT)
    book_holder = {f["facility_no"]: f["customer_no"] for f in pk.book}
    moved = [r for r in regs if r["facility_no"] in book_holder and book_holder[r["facility_no"]] != r["customer_no"]]
    lead = R.ask_b_raw(TDIR, group_by_facility=False)
    check("SF30 a defaulted facility counts for the customer the lending book shows holding it: %d register rows sit "
          "under another customer's number, and the number as recorded moves every band" % len(moved),
          len(moved) > 0 and all(lead[k][1] != F["ask_b"][k][1] for k in lead))

    # ------------------------------------------------------------------ Layer 1 mess neutrality on the main path
    b2b_names = set()
    for r in cred:
        c = pk.cust.get(r["customer_no"])
        if c and r["tran_type"] == "DC":
            kind, _ = pk.classify(r, c)
            if kind == "B2B":
                b2b_names.add(r["other_party"])
    check("L1 payer names upper-cased and cut at 20 characters by the clearing system: every firm payer resolves to "
          "exactly one register entity", b2b_names and all(len(n) <= 20 and n == n.upper() for n in b2b_names),
          len(b2b_names))
    check("L1 trading names in the register: matching without them keeps the call",
          same_call(res["V_legal_names_only"], gtot, gseg))
    check("L1 legacy 1993 codes and blanks in the lending book's industry field: reading the letters keeps the call",
          same_call(res["V_legacy_letters"], gtot, gseg))
    blanks = sum(1 for f in pk.book if not f["industry_code"])
    legacy = sum(1 for f in pk.book if len(f["industry_code"]) == 5)
    check("L1 the industry field really is blank or legacy for part of the book", blanks > 0 and legacy > 0,
          "%d blank, %d legacy facility rows" % (blanks, legacy))
    check("L1 non-sales credits among trading credits: leaving them in keeps the call",
          same_call(res["V_nonsales_included"], gtot, gseg))
    check("L1 public bodies across divisions O, P and Q: reading them all as O keeps the call",
          same_call(res["V_government_as_O"], gtot, gseg))
    ltd = sum(1 for f in pk.book if f["customer_name"].endswith(" Ltd"))
    check("L1 customer names as Ltd or Limited in the book: own-account transfers still drop out (TFR rows excluded)",
          ltd > 0 and res["V_nonsales_included"][0] != res["golden"][0], ltd)

    # ------------------------------------------------------------------ ask separation and device mass
    tmp = tempfile.mkdtemp()
    try:
        main_files = ["business_lending_book_2026-09-30.csv", "operating_account_credits_2025-10_to_2026-09.csv",
                      "nzbn_extract_canterbury_otago_southland_2026-10-12.csv", docs.STANDARD, docs.SCENARIO]
        for f in main_files:
            shutil.copy(os.path.join(TDIR, f), tmp)
        pk2, res2 = A.ladder(tmp)
        check("separation: the call computes from its five files alone (every ask file deleted)",
              abs(res2["golden"][0] - t) < 0.01)
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        for f in files:
            if f not in [d["file"] for d in meta["distractor_files"]]:
                shutil.copy(os.path.join(TDIR, f), tmp)
        F2 = R.compute(tmp)
        check("distractor deletion: every graded figure unchanged with the distractors removed",
              F2["total_half_m"] == gtot and F2["seg_m1"] == gseg and F2["ask_a_k"] == F["ask_a_k"]
              and F2["ask_b"] == F["ask_b"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    loss_cust = {c["cust"] for c in W.loss_cos} | {p["cust"] for p in W.persons}
    in_main = sum(1 for r in cred if r["customer_no"] in loss_cust) + sum(1 for f in pk.book if f["customer_no"] in loss_cust)
    check("separation: zero ask device rows in the call's population (no written-off company or guarantor in the book "
          "or the credits)", in_main == 0, in_main)
    nog = R.ask_a_detail(TDIR, guarantors=False)["net"]
    dg = min(abs(nog[k] - a["net"][k]) for k in nog)
    check("device A1 guarantors' receipts on their personal cases move every net credit loss cell by NZD 3 thousand or "
          "more", dg >= 3000, round(dg))
    dag = min(abs(gross[k] - a["net"][k]) for k in gross)
    check("device A2 the agency's upload beside its remittance moves every cell by NZD 2 thousand or more", dag >= 2000,
          round(dag))
    norur = R.ask_b_raw(TDIR, rural=False)
    check("device B1 group cross-defaults under the lead's number move every band", all(lead[k][1] != F["ask_b"][k][1]
                                                                                        for k in lead))
    check("hazard B2 the rural register moves at least one band", any(norur[k] != F["ask_b"][k] for k in norur))
    nomerge = R.ask_b_raw(TDIR, merges=False)
    check("hazard B3 merged customer numbers move at least one band", any(nomerge[k] != F["ask_b"][k] for k in nomerge))
    da = min(abs((v / 1e3) % 1 - 0.5) for v in a["net"].values())
    check("edge: every net credit loss cell sits NZD 150 or more from its thousand-dollar rounding edge", da >= 0.15,
          round(da, 3))
    db = min(edge_tenth(100.0 * d / n) for n, d in F["ask_b"].values())
    check("edge: every default share sits 0.015 points or more from its rounding edge", db >= 0.015, round(db, 4))
    hon = min(min(edge_tenth(res[k][1][s] / 1e6) for s in R.SEG_NAMES) for k in honest)
    check("edge: under the defensible family every segment sits 0.015 or more inside its bin", hon >= 0.015, round(hon, 3))
    hont = min(edge_half(res[k][0] / 1e6) for k in honest)
    check("edge: under the defensible family the book total sits 0.1 or more from its 0.5-million edge", hont >= 0.1,
          round(hont, 3))
    check("truth: the clean truth's book total is in the golden's bin", R.half_million(truth_payer) == gtot,
          round(truth_payer / 1e6, 3))
    check("truth: ask A on the pack equals the world's net credit losses to the cent",
          all(abs(a["net"][k] - W.ask_a_truth[k]) < 0.01 for k in a["net"]))
    check("truth: ask B on the pack equals the world's back-test", F["ask_b"] == {k: tuple(v) for k, v in W.ask_b_truth.items()})
    shares = [R.rhu(100.0 * d / n, 1) for n, d in F["ask_b"].values()]
    check("realism: default shares rise with risk grade", all(shares[i] < shares[i + 1] for i in range(4)), shares)

    # ------------------------------------------------------------------ realism sweep
    def runs(nums):
        st = [b - a_ for a_, b in zip(nums, nums[1:])]
        return sum(1 for i in range(len(st) - 2) if st[i] == st[i + 1] == st[i + 2])
    custs = sorted(int(c) for c in pk.cust)
    check("realism: customer numbers carry no arithmetic run (three equal steps in a row)", runs(custs) == 0)
    facs = sorted(int(f["facility_no"][1:]) for f in pk.book)
    check("realism: facility numbers carry no arithmetic run", runs(facs) == 0)
    names = [r["entity_name"] for r in pk.reg]
    ph = [n for n in names if re.search(r"\b(Acme|Company [A-Z]|Example|Test|Sample|Foo|Placeholder)\b", n)]
    check("realism: no placeholder entity names", not ph, ph[:5])
    check("realism: register names unique", len(names) == len(set(names)))
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "fingerprint",
                                       "cards", "task133.json")))
    people = set(card["world"]["people"])
    creators = set()
    for f in files:
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(os.path.join(TDIR, f)) as z:
                core = z.read("docProps/core.xml").decode("utf-8")
            creators |= set(re.findall(r"<dc:creator>(.*?)</dc:creator>", core))
    check("realism: every document author is a persona from guard.py names on the card", creators <= people,
          sorted(creators - people))
    late = []
    for f in files:
        p = os.path.join(TDIR, f)
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(p) as z:
                core = z.read("docProps/core.xml").decode("utf-8")
            for d in re.findall(r"(\d{4}-\d{2}-\d{2})T", core):
                if d > "2026-10-16":
                    late.append((f, d))
    check("realism: no document is dated after the fiction's as-of date 2026-10-16", not late, late)
    totals = {}
    for r in cred:
        totals[r["customer_no"]] = totals.get(r["customer_no"], 0.0) + float(r["amount_nzd"])
    vals = [round(v) for v in totals.values()]
    check("realism: no two borrowers share a year's credit total", len(vals) == len(set(vals)))
    amts = [r["amount_nzd"] for r in cred if r["tran_type"] == "DC" and r["particulars"].startswith("INV")]
    dup = 1 - len(set(amts)) / len(amts)
    check("realism: repeated invoice payment amounts under 3 per cent (chance coincidence only)", dup < 0.03, round(dup, 4))
    tiny = sum(1 for r in cred if r["tran_type"] == "DC" and float(r["amount_nzd"]) < 5
               and r["customer_no"] in pk.cust and pk.classify(r, pk.cust[r["customer_no"]])[0] == "B2B")
    check("realism: no firm pays an invoice under NZD 5", tiny == 0, tiny)
    exact = [s for s in R.SEG_NAMES if round(F["seg"][s]) % 1000 == 0]
    check("realism: no segment's stressed loss is a round thousand in NZD", not exact, exact)
    check("realism: the book's actual net credit losses sit well below the stressed loss (stress at least 2.5 times)",
          F["total"] >= 2.5 * sum(a["net"].values()), round(F["total"] / sum(a["net"].values()), 2))
    check("realism: performing book in default at the book date under 4 per cent of customers",
          F["n_default"] / (F["n_default"] + F["n_perf"]) < 0.04, F["n_default"])
    import subprocess
    scrub = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                         "scrub_producer_metadata.py")
    for d in (TDIR, os.path.join(TASK, "golden")):
        out = subprocess.run([sys.executable, scrub, d, "--floor", "2026-06-01", "--ceiling", "2026-10-16"],
                             capture_output=True, text=True).stdout
        check("H1 no writer signature or out-of-band stamp in %s" % os.path.basename(d), "clean" in out, out.strip()[-120:])
    import pypdf
    strict = pypdf.PdfReader(os.path.join(TDIR, docs.RURAL_PDF), strict=True).pages[0].extract_text()
    layout = subprocess.run(["pdftotext", "-layout", os.path.join(TDIR, docs.RURAL_PDF), "-"], capture_output=True,
                            text=True).stdout
    check("H25 the rural PDF reads the same under a strict parser, pdftotext and the generator's own decoder",
          all("Rural book total" in t for t in (strict, layout, pdf_text(os.path.join(TDIR, docs.RURAL_PDF)))))
    cases = list(csv.DictReader(open(os.path.join(TDIR, "collections_cases_open_2026-09-30.csv"), encoding="utf-8")))
    ovw = load_workbook(os.path.join(TDIR, "grade_overrides_2024-2026.xlsx"), read_only=True).active
    late_rm = [r for r in ovw.iter_rows(min_row=2, values_only=True) if r[4] is not None and r[4].date() > P.EXPORT_DATE.date()]
    check("H16 no record dated after its extract: cases opened by 30 September 2026, override removals by the export",
          all(A._d(r["opened"]) <= P.WIN_END for r in cases) and not late_rm, (len(cases), len(late_rm)))
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
        zn = sorted(n.split("/", 1)[1] for n in z.namelist())
    check("bundle: target.zip holds exactly target/", zn == files)
    check("figures.json carries the call and every ask figure",
          figs["call"]["total_nzd_m_nearest_half"] == gtot and len(figs["ask_a_net_credit_losses_nzd_k"]) == 12
          and len(figs["ask_b_share_pct"]) == 5)
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    check("prompt names both deliverables and states no figure of the answer",
          all(d in prompt for d in meta["deliverables"]) and not re.search(r"\b11\.5\b|\b10\.0\b", prompt))

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("\n%d assertions, %d failed" % (len(RESULTS), n_fail))
    return 1 if n_fail else 0


def alt_recovery_by_writeoff_half(tdir):
    """The reading SF21 rules out: each recovery placed in the half of the customer's first write-off."""
    reg = A.read_csv(os.path.join(tdir, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv"))
    by_nzbn = {r["nzbn"]: r for r in reg}
    cm = {r["customer_no"]: r for r in A.read_csv(os.path.join(tdir, "customer_master_extract_2026-10-09.csv"))}
    wo = [r for r in A.read_csv(os.path.join(tdir, "write_offs_2023-10_to_2026-09.csv")) if r["portfolio"] == "Business"]
    first = {}
    for r in wo:
        d = A._d(r["posting_date"])
        first[r["customer_no"]] = min(first.get(r["customer_no"], d), d)
    cases = {r["case_no"]: r["customer_no"] for r in A.read_csv(os.path.join(tdir, "collections_cases_open_2026-09-30.csv"))}
    gmap = {r["guarantor_customer_no"]: r["guaranteed_customer_no"]
            for r in A.read_csv(os.path.join(tdir, "guarantees_register_2026-09-30.csv"))}
    net = {(s, h): 0.0 for s in R.SEG_NAMES for h in R.HALVES}

    def seg(c):
        return P.SEG_OF[by_nzbn[cm[c]["nzbn"]]["bic_code"][0]]
    for r in wo:
        h = A.half(A._d(r["posting_date"]))
        if h:
            net[(seg(r["customer_no"]), h)] += float(r["amount_nzd"])
    for r in A._xlsx_rows(os.path.join(tdir, "collections_receipts_FY2026.xlsx"), 3):
        if r["Receipt Type"] == "Agency collection":
            continue
        d = r["Receipt Date"].date() if hasattr(r["Receipt Date"], "date") else r["Receipt Date"]
        owner = cases[r["Case No"]]
        if cm[owner]["customer_type"] == "Personal":
            owner = gmap.get(owner)
            if owner is None:
                continue
        if owner not in first or d < first[owner]:
            continue
        h = A.half(first[owner])
        if h:
            net[(seg(owner), h)] -= float(r["Amount (NZD)"])
    return {k: R.rhu(v / 1e3, 0) for k, v in net.items()}


if __name__ == "__main__":
    sys.exit(main())
