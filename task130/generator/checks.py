"""Assertions over the built task: run after build.py. Reads target/ and golden/ through estimators.py, reruns the
simulation for the figures the pack never ships (2024, the untreated 2027-28 year), and fails loudly on any breach.

    python3 checks.py [TASK_DIR]

Prints the measured magnitudes the design note's build record quotes."""
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pandas as pd
import pypdf
from openpyxl import load_workbook

import world as W
import sim as SM
import acuity as AC
import build as B
import estimators as E
import tune_table

TASK = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GLD = os.path.join(TASK, "golden")
T = (1, 2, 3, 4)
N_ASSERT = [0]
REPORT = []


def check(cond, msg):
    N_ASSERT[0] += 1
    if not cond:
        raise AssertionError(msg)


def rep(line):
    REPORT.append(line)
    print(line)


def pdf_text(path):
    """page text with every run of whitespace, line breaks included, read as one space"""
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in pypdf.PdfReader(path).pages))


def main():
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TGT))
    # ------------------------------------------------------------ input gates
    check(len(files) >= 10, "at least 10 files")
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check(len(fmts) >= 3, "at least 3 formats")
    nrows = {f: sum(1 for _ in open(os.path.join(TGT, f))) - 1 for f in files if f.endswith(".csv")}
    check(max(nrows.values()) >= 25000, "a file of 25,000 rows")
    check(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "distractors named")
    check(not any("distractor" in f.lower() for f in files), "no file named for its role")
    size = sum(os.path.getsize(os.path.join(TGT, f)) for f in files)
    check(size < 60e6, "pack under 60 MB")
    check(sorted(os.listdir(GLD)) == sorted(meta["deliverables"]) and 1 <= len(meta["deliverables"]) <= 3, "deliverables")
    rep("gates: %d files, formats %s, largest %s rows, %.1f MB, distractors %s" % (
        len(files), sorted(fmts), format(max(nrows.values()), ","), size / 1e6, meta["distractor_files"]))

    # ------------------------------------------------------------ the simulation (2024, 2027-28 and event-level truth)
    S = SM.simulate()
    L0 = AC.lists(S)
    B.apply_tune(S, tune_table.TUNE)
    L = AC.lists(S)
    for k in ("bid", "draft", "final"):
        check([r[:5] for r in L[k]] == [r[:5] for r in L0[k]], "centring left the %s list alone" % k)
    G, F = E.figures(TGT)
    n = G["n"]
    pid_of = {p.member_id: p.pid for p in S.people if p.member_id}

    # ------------------------------------------------------------ the lists in the files are the vendor's lists
    for k, fn in (("bid", "northcourt_rfp_2025-07_stratification_2024_claims.xlsx"),
                  ("draft", "northcourt_stratification_2026_claims_draft.xlsx"),
                  ("final", "northcourt_stratification_2026_claims_final.xlsx")):
        rows = E.read_list(os.path.join(TGT, fn))
        check([(r[0], r[1], r[2], r[3]) for r in rows] == [(x[0], x[2], x[3], x[4]) for x in L[k]], "%s list matches" % k)
        check(len(rows) == 140, "140 on the %s list" % k)
        for rank, ident, sc, t in rows:
            check(t == AC.tier_of(sc), "tier follows the stated floors")
    fin_ids = set(m for t in T for m in G["members"]["final"][t])
    dra_ids = set(m for t in T for m in G["members"]["draft"][t])
    drift = len(fin_ids - dra_ids)
    check(5 <= drift <= 25, "draft and final differ by a realistic number of members")
    check(15 <= n[1] <= 25 and 40 <= n[4] <= 50, "final tier sizes")
    check(15 <= G["bid_tiers"][1] <= 25 and 40 <= G["bid_tiers"][4] <= 58, "bid tier sizes")
    check(G["zero26"] == 0, "every enrolled member has 2026 member months")
    rep("lists: final tiers %s, bid tiers %s, draft tiers %s, %d members differ between draft and final" % (
        [n[t] for t in T], [G["bid_tiers"][t] for t in T], [G["draft_n"][t] for t in T], drift))

    # ------------------------------------------------------------ file conventions (Layer 1 resolved one way)
    md = F.med
    paidl = md[md.denial_reason_code == ""]
    tot = paidl.deductible_amount + paidl.copay_amount + paidl.coinsurance_amount + paidl.plan_paid_amount
    check(((paidl.allowed_amount - tot).abs() < 0.005).all(), "allowed = cost sharing + plan paid on every paid line")
    den = md[md.denial_reason_code != ""]
    raw = pd.read_csv(os.path.join(TGT, "medical_claim_lines_2025-01_2027-02.csv"), dtype=str, keep_default_na=False)
    check((raw.loc[raw.denial_reason_code != "", "allowed_amount"] == "").all(), "denied lines carry no allowed amount")
    check((raw.loc[raw.denial_reason_code != "", "plan_paid_amount"] == "0.00").all(), "denied lines pay nothing")
    claims = set(md.claim_number)
    refs = md.loc[md.claim_frequency_code.isin(["7", "8"]), "original_claim_number"]
    check(refs.isin(claims).all(), "every replacement and void names a claim in the file")
    by = md.groupby("claim_number").allowed_amount.sum()
    voids = md[md.claim_frequency_code == "8"].groupby("claim_number").original_claim_number.first()
    check(all(abs(by[v] + by[o]) < 0.005 for v, o in voids.items()), "voids net their claims to zero")
    rx = F.rx
    check((rx.member_id != "").all(), "every PBM row links to a member through employee number and person code")
    b1 = set(zip(rx[rx.TXN_CD == "B1"].RX_NBR, rx[rx.TXN_CD == "B1"].FILL_NBR, rx[rx.TXN_CD == "B1"].DATE_OF_SERVICE,
                 rx[rx.TXN_CD == "B1"].PHARMACY_NPI))
    b2 = rx[rx.TXN_CD == "B2"]
    check(all(k in b1 for k in zip(b2.RX_NBR, b2.FILL_NBR, b2.DATE_OF_SERVICE, b2.PHARMACY_NPI)), "every reversal has its claim")
    el = F.el
    spans_ok = True
    for m, g in el.groupby("member_id"):
        prev_end = None
        for s, e in zip(g.span_start, g.span_end):
            if prev_end is not None and (prev_end == "" or s <= prev_end):
                spans_ok = False
            prev_end = e
    check(spans_ok, "eligibility spans do not overlap")
    bid_rows = E.read_list(os.path.join(TGT, "northcourt_rfp_2025-07_stratification_2024_claims.xlsx"))
    check(all(r[1] in F.xw for r in bid_rows), "every bid member is in the conversion file")
    check(all(F.xw[r[1]] in F.spans for r in bid_rows), "every bid member has Ellery eligibility")
    xw = pd.read_csv(os.path.join(TGT, "tpa_conversion_crosswalk_2025-01-01.csv"), dtype=str, keep_default_na=False)
    check(xw.member_id.duplicated().sum() >= 5, "merged duplicate prior records present")
    check((xw.prior_member_suffix != xw.person_code).sum() >= 20, "reissued dependent numbers present")

    # ------------------------------------------------------------ the golden, two ways
    base = G["base"]
    gold = {}
    for t in T:
        for k in (0, 1):
            gold[("f26", t, k)] = G["f26"][t][k]
            gold[("base", t, k)] = base[t][k]
    m_, r_ = G["prog"]
    tot_ = G["prog_total"]
    # the simulation's own service amounts, no claim history at all, for the bid members' year
    an = defaultdict(lambda: [0.0, 0.0])
    bid_pids = {t: set(pid_of[m] for m in G["members"]["bid"][t]) for t in T}
    allbid = set().union(*bid_pids.values())
    for ev in S.events:
        if W.ANALOG_START <= ev[1] <= W.ANALOG_END and ev[0] in allbid:
            for comp in ev[5]:
                check(AC.paid_date(ev, comp) <= W.PAID_THROUGH, "the bid members' year is fully paid by the cut-off")
                an[ev[0]][0 if ev[3] == "M" else 1] += comp[2]
    for t in T:
        mm = G["an_detail"][t][1]
        sm = sum(an[p][0] for p in bid_pids[t]) / mm * W.TREND_MED ** 2
        sr = sum(an[p][1] for p in bid_pids[t]) / mm * W.TREND_RX ** 2
        check(abs(sm - base[t][0]) < 0.005 and abs(sr - base[t][1]) < 0.005, "tier %d baseline equals the claim-free truth" % t)
    rep("golden from the files equals the simulation's claim-free service amounts for the bid members' year, every tier")
    # every graded figure clear of its rounding boundary, both rounding paths of the total agree
    figs = list(gold.values()) + [m_, r_, tot_]
    margins = [0.5 - abs(v - round(v)) for v in figs]
    check(min(margins) >= 0.18, "every graded figure sits clear of its rounding boundary")
    check(round(m_) + round(r_) == round(tot_), "the rounded parts add to the rounded total")
    t4 = 1.1342
    for t in T:
        check(round(base[t][0] / W.TREND_MED ** 2 * t4) == round(base[t][0]), "a trend factor shown to 4 places rounds alike")
    check(round(sum(n[t] * base[t][0] / W.TREND_MED ** 2 * t4 for t in T) / 140) == round(m_), "programme alike at 1.1342")
    rep("bins: closest graded figure sits %.2f from a rounding boundary; %d centring adjustments, largest $%.2f" % (
        min(margins), len(tune_table.TUNE), max(abs(v) for v in tune_table.TUNE.values()) / 100))
    # the golden workbook carries the figures, whole dollars
    wb = load_workbook(os.path.join(GLD, "cohort_baseline_2027.xlsx"), data_only=True)
    ws = wb["Baseline"]
    for i, t in enumerate(T):
        row = [ws.cell(row=6 + i, column=j).value for j in range(1, 7)]
        check(row == ["Tier %d" % t, n[t], round(G["f26"][t][0]), round(G["f26"][t][1]), round(base[t][0]), round(base[t][1])],
              "workbook tier %d" % t)
    prow = [ws.cell(row=12, column=j).value for j in (2, 5, 6, 7)]
    check(prow == [140, round(m_), round(r_), round(tot_)], "workbook programme row")
    import docx
    memo = docx.Document(os.path.join(GLD, "baseline_certification_memo.docx"))
    first = [p.text for p in memo.paragraphs if p.text.strip()][1]
    check("${:,}".format(round(tot_)) in first.split(":")[0], "the memo opens with the total programme baseline")
    check("${:,}".format(round(m_)) in first and "${:,}".format(round(r_)) in first, "memo states medical and pharmacy")
    check(any(r.tag.endswith("drawing") for p in memo.paragraphs for r in p._p.iter()), "memo carries the chart")

    # ------------------------------------------------------------ the ladder
    rk = G["rungs"]
    g = tot_
    r0 = rk["R0"]
    check(r0 >= 2.2 * g, "persistence at least 2.2 times the golden")
    for k in ("R1", "R2", "R3a", "R4a", "R4b", "R6a", "R6b"):
        check(abs(rk[k] / g - 1) >= 0.05, "%s moves the programme total by 5 per cent" % k)
    same_r4b = []
    for name, tab in G["rung_tiers"].items():
        for t in T:
            for k in (0, 1):
                if name == "R4b" and G["an_detail"][t][1] == 12 * G["r4b_n"][t]:
                    same_r4b.append((t, k))      # nobody in the tier left during the year: twelve months each is the count
                    continue
                check(round(tab[t][k]) != round(base[t][k]), "%s lands on no golden tier figure" % name)
    rep("R4b (twelve months for each member still enrolled on 1 April 2025) equals the golden in tiers %s, where no member "
        "left during the year; R4a (twelve months for each listed member) differs in every tier" % sorted(set(t for t, k in same_r4b)))
    for k in ("R3b", "R5b", "R6c", "pooled", "regression", "R0c"):
        check(round(rk[k]) != round(g), "%s does not land on the golden total" % k)
    rep("ladder (programme total, change from the golden $%.2f):" % g)
    for k in ("R0", "R0c", "R1", "R2", "R3a", "R3b", "R4a", "R4b", "R5a", "R5b", "R6a", "R6b", "R6c", "pooled", "regression"):
        rep("  %-10s %10.2f  %+7.1f%%" % (k, rk[k], 100 * (rk[k] / g - 1)))

    # ------------------------------------------------------------ magnitudes the brief asks for (simulation only)
    def mmS(p, a, b):
        c, d = 0, dt.date(a.year, a.month, 1)
        while d <= b:
            if d >= a and p.covered_on(d):
                c += 1
            d = W.add_months(d, 1)
        return c

    def sim_pmpm(pids, a, b):
        med = rxs = 0.0
        for ev in S.events:
            if a <= ev[1] <= b and ev[0] in pids:
                for comp in ev[5]:
                    if ev[3] == "M":
                        med += comp[2]
                    else:
                        rxs += comp[2]
        mm = sum(mmS(S.people[p], a, b) for p in pids)
        return med / mm, rxs / mm, mm

    b24 = sim_pmpm(allbid, dt.date(2024, 1, 1), dt.date(2024, 12, 31))
    ban = sim_pmpm(allbid, W.ANALOG_START, W.ANALOG_END)
    rm = ban[0] / W.TREND_MED ** 1.25 / b24[0]
    rr = ban[1] / W.TREND_RX ** 1.25 / b24[1]
    check(0.25 <= rm <= 0.40, "medical regresses to a quarter to two fifths in real terms")
    check(rr >= 0.6, "pharmacy mostly persists")
    fin_pids = {t: set(pid_of[m] for m in G["members"]["final"][t]) for t in T}
    tru = {t: sim_pmpm(fin_pids[t], W.PROG_START, W.PROG_END) for t in T}
    truth = sum(n[t] * (tru[t][0] + tru[t][1]) for t in T) / 140
    pooled_truth = sim_pmpm(set().union(*fin_pids.values()), W.PROG_START, W.PROG_END)
    check(abs(g / truth - 1) <= 0.15, "golden within 15 per cent of the untreated programme year")
    rep("regression to the mean, bid members (simulation, real terms): medical %.2f, pharmacy %.2f of the 2024 level "
        "(2024 medical $%.0f, pharmacy $%.0f PMPM)" % (rm, rr, b24[0], b24[1]))
    rep("simulated untreated 2027-28 outcome of the enrolled members: $%.2f by tier weights (medical $%.2f, pharmacy $%.2f); "
        "pooled $%.2f; golden/truth %.3f; persistence/truth %.2f" % (
            truth, sum(n[t] * tru[t][0] for t in T) / 140, sum(n[t] * tru[t][1] for t in T) / 140,
            pooled_truth[0] + pooled_truth[1], g / truth, r0 / truth))
    for t in T:
        rep("  tier %d truth medical $%.0f pharmacy $%.0f (%d member months)" % (t, tru[t][0], tru[t][1], tru[t][2]))
    rep("cost-only regression alternative: $%.2f, %+.1f%% from the golden, %+.1f%% from the truth" % (
        rk["regression"], 100 * (rk["regression"] / g - 1), 100 * (rk["regression"] / truth - 1)))
    plan25 = G["letter"]["med_comp"][2025] / G["letter"]["mm"][2025], G["letter"]["rx"][2025] / G["letter"]["mm"][2025]
    check(450 <= plan25[0] <= 550 and 130 <= plan25[1] <= 180, "plan-wide 2025 cost is realistic")
    rep("plan-wide 2025 allowed PMPM: medical $%.2f, pharmacy $%.2f" % plan25)

    # ------------------------------------------------------------ clean-data test and lens swap
    clean_r0 = 0.0
    for t in T:
        p26 = sim_pmpm(fin_pids[t], dt.date(2026, 1, 1), dt.date(2026, 12, 31))
        clean_r0 += n[t] * (p26[0] * W.TREND_MED ** 1.25 + p26[1] * W.TREND_RX ** 1.25)
    clean_r0 /= 140
    check(clean_r0 > 2 * g, "with every claim clean and complete, persistence is still far off")
    overlap = len(set().union(*bid_pids.values()) & set().union(*fin_pids.values()))
    check(overlap < 70, "the answer's population is not the naive read's under another lens")
    rep("clean-data test: golden unchanged on claim-free data (above); persistence on complete, claim-free 2026 data $%.2f; "
        "%d members are on both the bid and the final list" % (clean_r0, overlap))
    # distractor deletion: the golden path never reads them
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in meta["distractor_files"]:
            os.symlink(os.path.join(TGT, f), os.path.join(tmp, f))
    G2, _ = E.figures(tmp)
    check(abs(G2["prog_total"] - g) < 1e-9 and G2["base"] == base and G2["f26"] == G["f26"], "golden unchanged without the distractors")
    shutil.rmtree(tmp)

    # ------------------------------------------------------------ documents recompute
    LF = G["letter"]
    txt = pdf_text(os.path.join(TGT, "renewal_letter_2027-28.pdf"))
    for v in (format(LF["mm"][2025], ","), format(LF["mm"][2026], ","), "${:,.0f}".format(LF["med_paid"][2026]),
              "${:,.0f}".format(LF["med_comp"][2026]), "${:,.0f}".format(LF["rx"][2026]), "${:,.2f}".format(LF["proj_med"]),
              "${:,.2f}".format(LF["proj_rx"]), "%.1f per cent on the current" % LF["rate_incr"]):
        check(v in txt, "renewal letter shows %s" % v)
    for mth in range(1, 13):
        check("%.3f" % LF["cf"][mth] in txt, "completion factor shown")
    check(3 <= LF["rate_incr"] <= 14, "a plausible rate increase")
    RB = E.rebate_figures(F)
    rw = load_workbook(os.path.join(TGT, "pbm_rebate_report_2026.xlsx"), data_only=True)["Summary"]
    vals = [[c for c in r] for r in rw.iter_rows(values_only=True)]
    qrows = [r for r in vals if r and isinstance(r[0], str) and re.fullmatch(r"Q\d 2026", r[0])]
    check([(r[1], r[3]) for r in qrows] == [(RB["brand"][q], RB["spec"][q]) for q in (1, 2, 3, 4)], "rebate counts recompute")
    sl = pdf_text(os.path.join(TGT, "stop_loss_policy_2027.pdf"))
    check(format(E.stoploss_census(F), ",") in sl, "stop-loss census recomputes")
    # the agreement states each convention once
    ag = pdf_text(os.path.join(TGT, "care_management_services_agreement_schedule_c.pdf"))
    for phrase in ("enrolled in the Plan on the first day of the month", "first date of service", "without completion",
                   "weighted by the number of Enrolled Members", "midpoint of the Programme Year"):
        check(phrase in ag, "Schedule C states %r" % phrase)
    alltext = {}
    for f in files:
        p = os.path.join(TGT, f)
        if f.endswith(".pdf"):
            alltext[f] = pdf_text(p)
        elif f.endswith(".txt"):
            alltext[f] = re.sub(r"\s+", " ", open(p).read())
    for phrase in ("on the first day of the month", "first date of service", "midpoint"):
        holders = [f for f, t in alltext.items() if phrase in t]
        check(holders == ["care_management_services_agreement_schedule_c.pdf"], "%r stated once, in Schedule C (%s)" % (phrase, holders))
    for f, t in alltext.items():
        check("\u2014" not in t, "no em dash in %s" % f)
        for word in ("regress", "persistence", "selection bias", "selected for", "control group", "comparison group",
                     "analog", "toward the mean", "mean revers"):
            check(word not in t.lower(), "%s does not say %r" % (f, word))

    # ------------------------------------------------------------ containers
    for f in files:
        p = os.path.join(TGT, f)
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                props = b"".join(z.read(x) for x in z.namelist() if x.startswith("docProps/"))
                check(all(i.date_time == (1980, 1, 1, 0, 0, 0) for i in z.infolist()), "fixed entry dates in %s" % f)
            blob = props
        elif f.endswith(".pdf"):
            blob = open(p, "rb").read()
        else:
            continue
        for sig in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib", b"LibreOffice"):
            check(sig not in blob, "%s carries no writer signature" % f)
        for d in re.findall(rb"(\d{4})-(\d\d)-(\d\d)T", blob) + [(m[0], m[1], m[2]) for m in re.findall(rb"D:(\d{4})(\d\d)(\d\d)", blob)]:
            day = dt.date(int(d[0]), int(d[1]), int(d[2]))
            check(dt.date(2024, 12, 1) <= day <= W.ASOF, "%s stamped inside the setting (%s)" % (f, day))
    for f in os.listdir(GLD):
        with zipfile.ZipFile(os.path.join(GLD, f)) as z:
            props = b"".join(z.read(x) for x in z.namelist() if x.startswith("docProps/"))
            check(b"python-docx" not in props and b"openpyxl" not in props, "golden %s carries its author" % f)
            check(not any(x.endswith("thumbnail.jpeg") for x in z.namelist()), "no template thumbnail")
    # the archive agrees with the tree it was cut from, by content
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        with zipfile.ZipFile(zp) as z:
            check(sorted(z.namelist()) == files, "target.zip holds the twelve files at its top level and nothing else")
            for f in files:
                check(z.read(f) == open(os.path.join(TGT, f), "rb").read(), "target.zip carries %s as built" % f)
        rep("target.zip: %d entries, contents identical to target/" % len(files))
    rep("%d assertions passed" % N_ASSERT[0])


if __name__ == "__main__":
    main()
