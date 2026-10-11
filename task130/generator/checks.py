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
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import pandas as pd
import pypdf
from openpyxl import load_workbook

import world as W
import sim as SM
import acuity as AC
import build as B
import catalog as K
import estimators as E
import tune_table

TASK = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
CONC_MED, CONC_RX = 0.26, 0.24      # the largest member's share of a bid tier's year, medical and pharmacy
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


def pdf_info(path):
    r = pypdf.PdfReader(path)
    return {k: str(v) for k, v in r.metadata.items()}


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
    check(not any(f.endswith("_extract_dictionary.txt") for f in files), "the readme is named in the district's idiom")
    check(sorted(x["path"] for x in meta["input_files"]) == files, "metadata lists every shipped file")
    size = sum(os.path.getsize(os.path.join(TGT, f)) for f in files)
    check(size < 75e6, "pack under 75 MB")
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
    graded = set(r[1] for k in ("bid", "final") for r in L[k])

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
    check(all(n[t] >= 12 for t in T) and all(G["bid_tiers"][t] >= 12 for t in T), "every tier holds enough members")
    check(G["zero26"] == 0, "every enrolled member has 2026 member months")
    rep("lists: final tiers %s, bid tiers %s, draft tiers %s, %d members differ between draft and final" % (
        [n[t] for t in T], [G["bid_tiers"][t] for t in T], [G["draft_n"][t] for t in T], drift))

    # ------------------------------------------------------------ file conventions (Layer 1 resolved one way)
    md = F.med
    raw = pd.read_csv(os.path.join(TGT, "medical_claim_lines_2025-01_2027-02.csv"), dtype=str, keep_default_na=False)
    paidl = md[md.denial_reason_code == ""]
    tot = paidl.deductible_amount + paidl.copay_amount + paidl.coinsurance_amount + paidl.plan_paid_amount
    check(((paidl.allowed_amount - tot).abs() < 0.005).all(), "allowed = cost sharing + plan paid on every paid line")
    check((raw.loc[raw.denial_reason_code != "", "allowed_amount"] == "").all(), "denied lines carry no allowed amount")
    check((raw.loc[raw.denial_reason_code != "", "plan_paid_amount"] == "0.00").all(), "denied lines pay nothing")
    claims = set(md.claim_number)
    refs = md.loc[md.claim_frequency_code.isin(["7", "8"]), "original_claim_number"]
    check(refs.isin(claims).all(), "every replacement and void names a claim in the file")
    by = md.groupby("claim_number").allowed_amount.sum()
    voids = md[md.claim_frequency_code == "8"].groupby("claim_number").original_claim_number.first()
    check(all(abs(by[v] + by[o]) < 0.005 for v, o in voids.items()), "voids net their claims to zero")
    rx = F.rx
    check((rx.member_id != "").all(), "every PBM row links to a member through employee number, person code and date")
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

    # ------------------------------------------------------------ P2: exact duplicates are denied, none paid twice
    acted_on = set(raw.loc[raw.claim_frequency_code.isin(["7", "8"]), "original_claim_number"])
    c1 = raw[(raw.claim_frequency_code == "1") & (raw.denial_reason_code == "") & ~raw.claim_number.isin(acted_on)]
    sig = c1.groupby("claim_number").agg(m=("member_id", "first"), d=("first_date_of_service", "first"),
                                         p=("procedure_code", "|".join), x=("modifier", "|".join),
                                         r=("revenue_code", "|".join), a=("allowed_amount", "|".join))
    dup = sig.duplicated(["m", "d", "p", "x", "r", "a"]).sum()
    check(dup == 0, "no service paid twice on two original claims (%d)" % dup)
    n18 = raw[raw.denial_reason_code == "18"].claim_number.nunique()
    check(n18 >= 200, "exact duplicate submissions are denied with reason 18")
    rep("P2: %d exact duplicate submissions denied with reason 18; no service is paid on two original claims" % n18)

    # ------------------------------------------------------------ P3: the bid members counted two ways agree
    apr = {t: [m for m in G["members"]["bid"][t] if F.mm(m, dt.date(2025, 4, 1), dt.date(2025, 4, 30)) == 1] for t in T}
    an_apr = E.tier_pmpm(F, apr, W.ANALOG_START, W.ANALOG_END)
    for t in T:
        check(abs(an_apr[t][0] - G["an"][t][0]) < 1e-9 and abs(an_apr[t][1] - G["an"][t][1]) < 1e-9,
              "tier %d: every bid member by member months equals the members enrolled on 1 April 2025" % t)
    gone = [m for t in T for m in G["members"]["bid"][t] if m not in apr[t]]
    check(all(F.mm(m, W.ANALOG_START, W.ANALOG_END) == 0 for m in gone), "no bid member leaves and returns inside the year")
    rep("P3: %d bid members left before 1 April 2025 and none returned; counting all 140 by member months gives the same "
        "figures as counting the members enrolled on 1 April 2025" % len(gone))

    # ------------------------------------------------------------ P4: every transaction inside the stated window
    check(rx.proc.min() >= dt.date(2025, 1, 1) and rx.proc.max() <= W.PAID_THROUGH, "PBM processing window")
    check(md.paid.min() >= dt.date(2025, 1, 1) and md.paid.max() <= W.PAID_THROUGH, "medical paid window")
    rep("P4: PBM transactions processed %s to %s; medical claims paid %s to %s" % (rx.proc.min(), rx.proc.max(),
                                                                                md.paid.min(), md.paid.max()))

    # ------------------------------------------------------------ P1: birth-month claims and the first-day rule
    ag = pdf_text(os.path.join(TGT, "care_management_services_agreement_schedule_c.pdf"))
    check("incurred by a member while the member is covered under the Plan" in ag, "Schedule C: claims incurred while covered")
    check("whether or not the month in which it is incurred is a Member Month" in ag, "Schedule C: non-member-month claims count")
    nm = []
    for grp, (a, b) in ((G["members"]["final"], (dt.date(2026, 1, 1), dt.date(2026, 12, 31))),
                        (G["members"]["bid"], (W.ANALOG_START, W.ANALOG_END))):
        for t in T:
            for m in grp[t]:
                first = min(s for s, e in F.spans[m])
                if a <= first <= b and first.day != 1:
                    amt = md[(md.member_id == m) & (md.d0 >= first) & (md.d0 < W.add_months(dt.date(first.year, first.month, 1), 1))]
                    nm.append((m, t, first, round(float(amt.allowed_amount.sum()), 2)))
    rep("P1: graded members whose coverage starts after the first of a month in the window: %s" % nm)

    # ------------------------------------------------------------ R1: claims fit the patient
    elx = el.sort_values("span_start").drop_duplicates("member_id", keep="last").set_index("member_id")
    md["sex"] = md.member_id.map(elx.sex)
    dob = pd.to_datetime(md.member_id.map(elx.birth_date)).dt.date
    md["age"] = [d0.year - b.year - ((d0.month, d0.day) < (b.month, b.day)) for d0, b in zip(md.d0, dob)]
    live = md[md.claim_frequency_code != "8"]
    bad = live[(live.procedure_code == "84153") & ((live.sex == "F") | (live.age < 40))]
    check(len(bad) == 0, "PSA only for men from 40")
    bad = live[live.diagnosis_code_1.isin(["Z00.129", "Z00.121", "Z00.110", "Z00.111"]) & (live.age >= 18)]
    check(len(bad) == 0, "child health examinations only for children")
    bad = live[live.procedure_code.isin(["99381", "99382", "99383", "99384", "99391", "99392", "99393", "99394"]) & (live.age >= 18)]
    check(len(bad) == 0, "child preventive codes only for children")
    bad = live[live.procedure_code.isin(["99385", "99386", "99387", "99395", "99396", "99397"]) & (live.age < 18)]
    check(len(bad) == 0, "adult preventive codes only for adults")
    bad = live[live.diagnosis_code_1.isin(["Z00.00", "Z00.01"]) & (live.age < 18)]
    check(len(bad) == 0, "adult examinations only for adults")
    bad = live[live.diagnosis_code_1.str.startswith("H66") & (live.age >= 18)]
    check(len(bad) == 0, "otitis media coded for children")
    adult_only = r"^(I1|I2|I4|I5|I6|E11|E78|E66|M17|M16|M19|M48|M51|M54|N40|N52|R73|F17|F10|G45|L97|K57|C)"
    bad = live[live.diagnosis_code_1.str.match(adult_only) & (live.age < 12)]
    check(len(bad) == 0, "adult chronic diagnoses never on young children (%s)" % bad.diagnosis_code_1.value_counts().head(3).to_dict())
    female = r"^(O|Z34|Z3A|Z39|N7[0-7]|N8|N9[0-5]|B37.3|Z01.41|Z30.4|C50)"
    check(len(live[live.diagnosis_code_1.str.match(female) & (live.sex == "M")]) == 0, "female diagnoses only for women")
    check(len(live[live.procedure_code.isin(["76856", "76830", "58558", "58300", "58571", "58661", "77067", "59400", "59510",
                                             "76801", "76805", "76811", "76815", "76817"]) & (live.sex == "M")]) == 0,
          "female procedures only for women")
    check(len(live[live.diagnosis_code_1.str.match(r"^(C61|N40|N52)") & (live.sex == "F")]) == 0, "male diagnoses only for men")
    check(len(live[live.procedure_code.isin(["55250", "55866", "55700", "54150"]) & (live.sex == "F")]) == 0,
          "male procedures only for men")
    nicu = live[live.revenue_code.isin(["0172", "0173", "0174"])]
    check((nicu.age == 0).all() and nicu.diagnosis_code_1.str.match(r"^(P|Z38)").all(), "NICU stays are newborns with neonatal diagnoses")
    ip = live[(live.bill_type.str[:2] == "11") & (live.denial_reason_code == "")]
    replaced = set(md.loc[md.claim_frequency_code.isin(["7", "8"]), "original_claim_number"])
    stays = ip[~ip.claim_number.isin(replaced)].drop_duplicates("claim_number")
    overl = 0
    for m, g in stays.groupby("member_id"):
        s = sorted(zip(g.first_date_of_service, g.last_date_of_service))
        overl += sum(1 for i in range(1, len(s)) if s[i][0] < s[i - 1][1])
    check(overl == 0, "no member is in two hospital stays at once")
    rep("R1: PSA, preventive, child, female, male and neonatal codes all fit the member's age and sex; %d inpatient "
        "stays, none overlapping" % len(stays))

    # ------------------------------------------------------------ R2: catalogues and their skew
    cl = raw.drop_duplicates("claim_number")
    n_npi, n_proc, n_dx = raw.billing_npi.nunique(), raw[raw.procedure_code != ""].procedure_code.nunique(), cl.diagnosis_code_1.nunique()
    n_ndc, n_ph = rx.NDC.nunique(), rx.PHARMACY_NPI.nunique()
    check(n_npi >= 150 and n_proc >= 250 and n_dx >= 300 and n_ndc >= 200 and n_ph >= 30, "realistic catalogues")
    vc = cl.diagnosis_code_1.value_counts()
    check(0.15 <= vc.head(10).sum() / vc.sum() <= 0.5 and vc.iloc[0] / vc.iloc[50] >= 8, "diagnosis frequencies are skewed")
    pv = rx.PHARMACY_NPI.value_counts()
    check(pv.head(5).sum() / pv.sum() >= 0.3, "a few pharmacies carry much of the volume")
    signature = {"em_ed": r"^9928[1-5]$", "cataract": r"^66984$", "chole": r"^4756[23]$", "colonoscopy": r"^4537[89]|^4538[05]$",
                 "arthroplasty": r"^27447$|^27130$", "dialysis": r"^9096[0-2]$", "sleep": r"^95810$"}
    prof = raw[(raw.claim_type == "P") & (raw.procedure_code != "")]
    fam = {k: set(prof[prof.procedure_code.str.match(v)].billing_npi) for k, v in signature.items()}
    multi = [x for x in set().union(*fam.values()) if sum(x in s for s in fam.values()) > 1]
    check(not multi, "no professional group bills two specialties' signature services")
    rep("R2: %d billing NPIs, %d procedure codes, %d principal diagnoses, %d NDCs, %d pharmacies; top ten diagnoses carry "
        "%.0f%% of claims" % (n_npi, n_proc, n_dx, n_ndc, n_ph, 100 * vc.head(10).sum() / vc.sum()))

    # ------------------------------------------------------------ R3: the calendar
    office = cl[cl.procedure_code.isin(["99212", "99213", "99214", "99215", "99203", "99204", "99205"]) & (cl.place_of_service == "11")]
    od = pd.to_datetime(office.first_date_of_service).dt.date
    check(sum(1 for d in od if d.weekday() == 6) == 0, "no office visits on Sundays")
    check(sum(1 for d in od if d in W.CLINIC_CLOSED) == 0, "no office visits on the holidays the clinics close")
    check(sum(1 for d in od if d.weekday() == 5) / len(od) < 0.08, "few office visits on Saturdays")
    runs = set(W.CHECK_RUNS)
    check(set(md.paid) <= runs, "every payment on an Ellery check run")
    rxd = Counter(d.weekday() for d in rx.dos)
    check(rxd[6] < 0.6 * rxd[5] < 0.6 * rxd[0], "pharmacy fills dip at the weekend")
    er = cl[(cl.bill_type == "131") & cl.claim_number.isin(raw[raw.revenue_code == "0450"].claim_number)]
    erd = Counter(pd.to_datetime(er.first_date_of_service).dt.weekday)
    check(min(erd.values()) > 0.7 * max(erd.values()), "emergency visits every day of the week")
    rep("R3: %d payment dates, all Ellery check runs; office visits Monday to Saturday %s; pharmacy fills by weekday %s" % (
        md.paid.nunique(), [sum(1 for d in od if d.weekday() == k) for k in range(6)], [rxd[k] for k in range(7)]))

    # ------------------------------------------------------------ R4: adjudication
    al = raw[(raw.allowed_amount != "") & (raw.claim_frequency_code != "8")]
    a_, b_ = al.allowed_amount.astype(float), al.billed_amount.astype(float)
    check((a_ <= b_ + 0.001).all(), "allowed never above billed")
    eq = ((a_ - b_).abs() < 0.001) & (a_ > 0)
    check(0.003 <= eq.mean() <= 0.05, "some lines allowed at a low billed charge")
    inst = al[al.claim_type == "I"]
    rep_amt = inst.groupby("claim_number").allowed_amount.apply(lambda s: s[s.astype(float) > 0].duplicated().any()).sum()
    check(rep_amt == 0, "no facility claim repeats one allowed amount across its revenue lines")
    recv = [dt.date(2000 + int(x[:2]), 1, 1) + dt.timedelta(days=int(x[2:5]) - 1) for x in cl.claim_number]
    lag = np.array([(dt.date.fromisoformat(p) - r).days for p, r in zip(cl.paid_date, recv)])
    check(lag.min() >= 1 and (lag >= 30).mean() >= 0.03 and lag.max() <= 130, "receipt to payment spreads out, pended claims included")
    # join residue: person codes and birth dates that changed, none on a graded member
    naive = {}
    for r in el.sort_values("span_start").itertuples(index=False):
        naive[(int(r.employee_number), r.person_code)] = r.member_id
    rx_naive = pd.Series([naive.get((int(c), p), "") for c, p in zip(rx.CARDHOLDER_ID, rx.PERSON_CD)], index=rx.index)
    moved = rx[rx_naive != rx.member_id]
    check(1 <= len(moved) <= 200, "a few fills belong to dependents whose person code changed")
    check(not (set(moved.member_id) | set(rx_naive[moved.index])) & set(p for t in T for p in G["members"]["final"][t])
          and not (set(moved.member_id) | set(rx_naive[moved.index])) & set(p for t in T for p in G["members"]["bid"][t]),
          "no graded member's fills move between the two joins")
    xdob = xw.assign(d=pd.to_datetime(xw.birth_date, format="%m/%d/%Y").dt.strftime("%Y-%m-%d"))
    xdob["e"] = xdob.member_id.map(elx.birth_date)
    corr = xdob[xdob.d != xdob.e]
    check(3 <= len(corr) <= 12 and not set(corr.member_id) & (set(m for t in T for m in G["members"]["bid"][t]) |
                                                             set(m for t in T for m in G["members"]["final"][t])),
          "a few corrected birth dates, none on a graded member")
    rep("R4: allowed at billed on %.1f%% of lines; receipt to payment median %d days, %.1f%% at 30 days or more, longest %d; "
        "%d fills move between a latest-span join and a join on the span in effect; %d corrected birth dates; none on a "
        "graded member" % (100 * eq.mean(), np.median(lag), 100 * (lag >= 30).mean(), lag.max(), len(moved), len(corr)))

    # ------------------------------------------------------------ R6: tiers fit the dependents enrolled
    badt = 0
    for emp, g in el.groupby("employee_number"):
        for s, tier in zip(g.span_start, g.coverage_tier):
            cov = g[(g.span_start <= s) & ((g.span_end == "") | (g.span_end >= s))]
            sp, ch = (cov.relationship == "SPS").any(), (cov.relationship == "DEP").any()
            want = "FAM" if sp and ch else "ES" if sp else "EC" if ch else "EE"
            badt += tier != want
    check(badt == 0, "every span's coverage tier fits the dependents enrolled (%d)" % badt)

    # ------------------------------------------------------------ the golden, two ways
    base = G["base"]
    gold = {}
    for t in T:
        for k in (0, 1):
            gold[("f26", t, k)] = G["f26"][t][k]
            gold[("base", t, k)] = base[t][k]
    m_, r_ = G["prog"]
    tot_ = G["prog_total"]
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
    figs = list(gold.values()) + [m_, r_, tot_]
    margins = [0.5 - abs(v - round(v)) for v in figs]
    check(min(margins) >= 0.18, "every graded figure sits clear of its rounding boundary")
    check(round(m_) + round(r_) == round(tot_), "the rounded parts add to the rounded total")
    t4 = 1.1342
    for t in T:
        check(round(base[t][0] / W.TREND_MED ** 2 * t4) == round(base[t][0]), "a trend factor shown to 4 places rounds alike")
    check(round(sum(n[t] * base[t][0] / W.TREND_MED ** 2 * t4 for t in T) / 140) == round(m_), "programme alike at 1.1342")
    rep("bins: closest graded figure sits %.2f from a rounding boundary; %d centring adjustments, largest $%.2f" % (
        min(margins), len(tune_table.TUNE), max(abs(v) for v in tune_table.TUNE.values()) / 100 if tune_table.TUNE else 0))
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
    check(r0 >= 2.0 * g, "persistence at least twice the golden")
    for k in ("R1", "R3a", "R4a"):
        check(abs(rk[k] / g - 1) >= 0.05, "%s moves the programme total by 5 per cent" % k)
    for name, tab in G["rung_tiers"].items():
        for t in T:
            for k in (0, 1):
                # dividing by twelve months a member is the golden itself in a tier where everyone counted stayed the year
                if name == "R4a" and G["an_detail"][t][1] == 12 * G["bid_tiers"][t]:
                    continue
                if name == "R4b" and G["an_detail"][t][1] == 12 * G["r4b_n"][t]:
                    continue
                if name == "R4c" and G["an_detail"][t][1] == G["r4c_n"][t]:
                    continue
                check(round(tab[t][k]) != round(base[t][k]), "%s lands on no golden tier figure" % name)
    for k in ("R3b", "R5b", "R6c", "pooled", "regression", "R0c", "R4c", "R7", "R9"):
        check(round(rk[k]) != round(g), "%s does not land on the golden total" % k)
    for name, tab in G["rung_tiers"].items():
        for k in (0, 1):
            pk = sum(n[t] * tab[t][k] for t in T) / 140
            check(round(pk) != round(G["prog"][k]), "%s lands on neither programme figure (%s %.2f)" % (name, k, pk))
    # the magnitude floor: a rung within 5 per cent of the golden total misses every tier cell and both programme figures
    near = [k for k in G["rung_tiers"] if k in rk and abs(rk[k] / g - 1) < 0.05]
    for k in near:
        tab = G["rung_tiers"][k]
        cells = [(t, j) for t in T for j in (0, 1)
                 if not (k == "R4c" and G["an_detail"][t][1] == G["r4c_n"][t])
                 and not (k == "R4a" and G["an_detail"][t][1] == 12 * G["bid_tiers"][t])
                 and not (k == "R4b" and G["an_detail"][t][1] == 12 * G["r4b_n"][t])]
        check(all(round(tab[t][j]) != round(base[t][j]) for t, j in cells), "%s, within 5 per cent, misses every tier cell" % k)
    check(r0 >= 2.0 * g and all(G["rung_tiers"]["R0"][t][0] > 1.5 * base[t][0] for t in T), "persistence stays far off")
    rep("ladder (programme total, change from the golden $%.2f):" % g)
    for k in ("R0", "R0c", "R1", "R2", "R3a", "R3b", "R4a", "R4b", "R4c", "R5a", "R5b", "R6a", "R6b", "R6c", "R7", "R9",
              "pooled", "regression"):
        rep("  %-10s %10.2f  %+7.1f%%" % (k, rk[k], 100 * (rk[k] / g - 1)))
    rep("  rungs within 5 per cent of the golden, every tier cell and both programme figures missed: %s" % (near or "none"))

    # ------------------------------------------------------------ the forks the second reader sized, each closed
    FK, fk = G["fork_tiers"], G["forks"]
    ag = pdf_text(os.path.join(TGT, "care_management_services_agreement_schedule_c.pdf"))
    bcover = " ".join(str(x) for r in load_workbook(os.path.join(TGT, "northcourt_rfp_2025-07_stratification_2024_claims.xlsx"),
                                                    data_only=True)["Cover"].iter_rows(values_only=True) for x in r if x)
    # 1. pharmacy carried forward at its own 2026 level: the record shows it is not persistent, and it lands well off
    rx_p = sum(n[t] * FK["R0p"][t][1] for t in T) / 140
    check(rx_p >= 1.10 * r_, "pharmacy persistence at least 10 per cent off the golden pharmacy (%.2f)" % (rx_p / r_))
    check(abs(fk["R0p"] / g - 1) >= 0.10, "bid medical with own-trend pharmacy at least 10 per cent off the total")
    check(all(round(FK["R0p"][t][1]) != round(base[t][1]) for t in T), "pharmacy persistence lands on no tier cell")
    rx_up = sum(1 for t in T if G["f26"][t][1] > 1.03 * G["f25"][t][1])
    check(rx_up >= 3, "the enrolled members' pharmacy rose into 2026 in most tiers (%d)" % rx_up)
    rep("fork 1, pharmacy: own 2026 pharmacy carried forward $%.2f against $%.2f (%+.1f%%); with the bid members' medical "
        "$%.2f (%+.1f%% on the total); enrolled members' pharmacy 2025 to 2026 by tier %s" % (
            rx_p, r_, 100 * (rx_p / r_ - 1), fk["R0p"], 100 * (fk["R0p"] / g - 1),
            ["%.0f to %.0f" % (G["f25"][t][1], G["f26"][t][1]) for t in T]))
    # 2. the window: the bid's own programme year, three months after its claims year, as the agreement's is
    check("1 April 2025 to 31 March 2026" in bcover and "savings measured on the programme year's claims" in bcover,
          "the RFP list's cover gives the proposed programme year and that savings run on it")
    check("stratified on claims incurred in calendar year 2026" in ag and "1 April 2027 to 31 March 2028" in ag,
          "Schedule C: the list's claims year and the Programme Year three months after it")
    check(abs(rk["R2"] / g - 1) >= 0.04, "calendar 2025 lands at least 4 per cent off (%.1f%%)" % (100 * (rk["R2"] / g - 1)))
    rep("fork 2, window: calendar 2025 trended 27 months $%.2f (%+.1f%%), every tier cell missed" % (
        rk["R2"], 100 * (rk["R2"] / g - 1)))
    # 3. attrition: every listed member counts for the months enrolled
    check("A member who is enrolled for part of the period is included for the Member Months in which the member is "
          "enrolled" in ag, "Schedule C.1(c): partial-period members count")
    rep("fork 3, attrition: full-year members only $%.2f (%+.1f%%), ruled out by Schedule C.1(c)" % (
        rk["R4c"], 100 * (rk["R4c"] / g - 1)))
    # 4. credibility: tier by tier
    check("A Baseline PMPM is determined separately for each Risk Tier, from the experience of members in that Risk "
          "Tier" in ag, "Schedule C.1(h): a baseline per tier from its own tier's experience")
    sh = {}
    for t in T:
        al = F.allowed(G["members"]["bid"][t], W.ANALOG_START, W.ANALOG_END)
        tm, tr = sum(v[0] for v in al.values()), sum(v[1] for v in al.values())
        sh[t] = (max(v[0] for v in al.values()) / tm, max(v[1] for v in al.values()) / tr)
    check(max(sh[t][0] for t in T) <= CONC_MED and max(sh[t][1] for t in T) <= CONC_RX,
          "no single member dominates a tier's year (%s)" % sh)
    rep("fork 4, credibility: pooled level spread by the enrolled members' 2026 relativities $%.2f (%+.1f%%), tier 1 medical "
        "$%.0f against $%.0f; largest member's share of a bid tier's year, medical %s, pharmacy %s" % (
            rk["R7"], 100 * (rk["R7"] / g - 1), G["rung_tiers"]["R7"][1][0], base[1][0],
            [round(sh[t][0], 2) for t in T], [round(sh[t][1], 2) for t in T]))
    # 5. run-out: the paid-through basis is filed; the three-month basis moves only medical
    check("taken on claims paid through the Data Cut-Off Date" in ag, "Schedule C.1(h): experience paid through the cut-off")
    check(all(FK["R8"][t][1] == G["an"][t][1] * W.TREND_RX ** 2 for t in T), "pharmacy has no run-out: identical either way")
    moved = [t for t in T if round(FK["R8"][t][0]) != round(base[t][0])]
    rep("fork 5, run-out: claims paid by 30 June 2026 move medical by %s and pharmacy by nothing; tiers whose whole-dollar "
        "medical moves %s; ruled out by Schedule C.1(h)" % (
            ["%+.2f" % (FK["R8"][t][0] - base[t][0]) for t in T], moved))

    # ------------------------------------------------------------ realism the second reader asked for
    ipc = raw[raw.bill_type.str.startswith("11")]
    sets = ipc.groupby("claim_number").revenue_code.apply(lambda x: frozenset(x))
    check(sets.nunique() >= 300, "inpatient revenue lines follow the stay (%d distinct sets)" % sets.nunique())
    edx = sum(1 for x in sets if {"0450", "0730", "0320"} <= x) / len(sets)
    check(edx <= 0.15, "ED, EKG and chest film only where the stay calls for them (%.2f)" % edx)
    dx1 = ipc.drop_duplicates("claim_number").set_index("claim_number").diagnosis_code_1
    op = [x for x in sets.index if dx1[x].startswith(("K35", "K81"))]
    check(op and sum("0360" in sets[x] for x in op) / len(op) >= 0.8, "appendicitis and cholecystitis stays carry the operation")
    nic = ipc[ipc.revenue_code.isin(["0172", "0173", "0174"])].drop_duplicates("claim_number")
    for r_n in nic.itertuples(index=False):
        ga = r_n.diagnosis_code_2 if r_n.diagnosis_code_1.startswith("Z38") else r_n.diagnosis_code_1
        los = (dt.date.fromisoformat(r_n.last_date_of_service) - dt.date.fromisoformat(r_n.first_date_of_service)).days
        if ga.startswith("P07.2"):
            check(los >= 63, "an extremely preterm baby stays about three months (%s, %d days)" % (ga, los))
        elif ga in ("P07.31", "P07.32", "P07.33", "P07.34"):
            check(los >= 21, "a very preterm baby stays weeks (%s, %d days)" % (ga, los))
    unc = 0
    for r_n in md[md.allowed_amount != 0].drop_duplicates("claim_number").itertuples(index=False):
        if not any(s_ <= r_n.d0 <= e_ for s_, e_ in F.spans[r_n.member_id]):
            unc += 1
    check(unc == 0, "no allowed claim on a day the member is not covered (%d)" % unc)
    check((raw.denial_reason_code == "27").sum() >= 20, "services after coverage ended are denied with reason 27")
    gaps = sum(1 for m_, sp_ in F.spans.items() for i in range(1, len(sp_))
               if (sorted(sp_)[i][0] - sorted(sp_)[i - 1][1]).days > 1)
    cob = (el.employee_class == "COB").sum()
    check(gaps >= 20 and cob >= 50, "eligibility carries gaps and COBRA continuation (%d gaps, %d COB spans)" % (gaps, cob))
    rday = Counter((dt.date(2000 + int(x[:2]), 1, 1) + dt.timedelta(days=int(x[2:5]) - 1)).weekday() for x in cl.claim_number)
    check(rday.most_common(1)[0][0] == 0 and (rday[5] + rday[6]) / sum(rday.values()) < 0.06,
          "claims are logged on business days, Monday busiest")
    late = cl[(pd.to_datetime(cl.first_date_of_service).dt.year == 2025) & (cl.paid_date >= "2027-01-01")]
    check(len(late) >= 10 and (late.paid_date >= "2027-02-01").any(), "some 2025 claims were adjusted in 2027 (%d)" % len(late))
    flist = load_workbook(os.path.join(TGT, "northcourt_stratification_2026_claims_final.xlsx"), data_only=True)["Members"]
    frows = list(flist.iter_rows(values_only=True))
    teams = Counter(r_n[7] for r_n in frows[1:] if r_n[0] is not None)
    rn = [teams[k] for k in ("RN Team A", "RN Team B", "RN Team C")]
    hc = [teams[k] for k in ("Health Coach Team 1", "Health Coach Team 2")]
    check(len(set(rn)) > 1 and len(set(hc)) > 1 and sum(rn) + sum(hc) == 140, "care teams follow the plan's rule, not a rota")
    pg = [p.extract_text() for p in pypdf.PdfReader(os.path.join(TGT, "renewal_letter_2027-28.pdf")).pages]
    check("Michael Perry, FSA, MAAA" in pg[0] and "Sincerely" in pg[0], "the renewal letter signs on its first page")
    check("/s/ Deborah Johnson" in ag and "/s/ Sandra Lopez" in ag and "/s/ Phillip Alvarado" in ag, "conformed signatures")
    check(all(len(p.extract_text()) > 200 for p in pypdf.PdfReader(os.path.join(TGT, "care_management_services_agreement_schedule_c.pdf")).pages),
          "no blank page in the agreement excerpt")
    rep("realism: %d distinct inpatient revenue-code sets; ED+EKG+chest film on %.0f%% of stays; %d of %d appendicitis and "
        "cholecystitis stays operated; %d eligibility gaps, %d COBRA spans; receipts by weekday %s; %d 2025 claims adjusted in "
        "2027; care teams %s" % (sets.nunique(), 100 * edx, sum("0360" in sets[x] for x in op), len(op), gaps, cob,
                                 [rday[k] for k in range(7)], len(late), dict(teams)))

    # ------------------------------------------------------------ magnitudes the brief asks for (simulation only)
    def mmS(p, a, b):
        c, d = 0, dt.date(a.year, a.month, 1)
        while d <= b:
            if d >= a and p.covered_on(d):
                c += 1
            d = W.add_months(d, 1)
        return c

    ev_by = defaultdict(list)
    for ev in S.events:
        ev_by[ev[0]].append(ev)

    def sim_pmpm(pids, a, b):
        med = rxs = 0.0
        for pid in pids:
            for ev in ev_by[pid]:
                if a <= ev[1] <= b:
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
    check(0.15 <= rm <= 0.45, "medical regresses to well under half its selection-year level in real terms")
    check(0.6 <= rr <= 0.92, "pharmacy regresses too, less than medical (%.3f)" % rr)
    fin_sim = set(pid_of[m] for t in T for m in G["members"]["final"][t])
    f26s = sim_pmpm(fin_sim, dt.date(2026, 1, 1), dt.date(2026, 12, 31))
    fpy = sim_pmpm(fin_sim, W.PROG_START, W.PROG_END)
    frr = fpy[1] / W.TREND_RX ** 1.25 / f26s[1]
    check(frr <= 0.95, "the enrolled members' own pharmacy falls after 2026 in real terms (%.3f)" % frr)
    fin_pids = {t: set(pid_of[m] for m in G["members"]["final"][t]) for t in T}
    # the memo's account of the enrolled members' 2026 and the chart's title hold on the data
    named = {"an operation": lambda k, dx: k in ("admit_surgery", "joint"), "a heart attack": lambda k, dx: dx.startswith("I21"),
             "a stroke": lambda k, dx: k == "admit" and dx.startswith("I63"),
             "pneumonia": lambda k, dx: k == "admit" and dx.startswith("J18"), "a cancer course": lambda k, dx: k in ("chemo", "radiation"),
             "a premature birth": lambda k, dx: k == "nicu", "a hepatitis C cure": lambda k, dx: dx == "hcv"}
    fin_all = set().union(*fin_pids.values())
    who = defaultdict(set)
    big = set()
    for ev in S.events:
        if ev[0] in fin_all and dt.date(2026, 1, 1) <= ev[1] <= dt.date(2026, 12, 31):
            info = ev[6] if isinstance(ev[6], dict) else {}
            dx = "hcv" if ev[3] == "R" and info.get("drug") in ("epclusa", "mavyret") else info.get("dx", "")
            for label, f in named.items():
                if f(ev[4], dx):
                    who[label].add(ev[0])
            if ev[3] == "M" and (ev[4] in SM.STAY_KINDS or ev[4] in ("chemo", "radiation")):
                big.add(ev[0])
    mtext = " ".join(p.text for p in memo.paragraphs)
    listed = re.search(r"for most it was the year of (.+?) that will not repeat", mtext).group(1)
    listed = [x.strip() for x in re.split(r",| or ", listed) if x.strip()]
    check(all(len(who[x]) >= 2 for x in listed) and set(listed) == {k for k in named if len(who[k]) >= 2},
          "the memo names every one-off event at least two enrolled members had in 2026, and only those (%s)" % listed)
    check(len(big) > 70, "most enrolled members had a hospital stay or a cancer course in 2026 (%d)" % len(big))
    import golden as GD
    title = GD.chart_title({"base": base, "f26": G["f26"]})
    med_half = all(base[t][0] < 0.5 * G["f26"][t][0] for t in T)
    check(("under half" in title) == med_half and all(base[t][0] < G["f26"][t][0] for t in T),
          "chart title: medical baselines against 2026 (%s)" % title)
    below = sum(1 for t in T if base[t][1] < G["f26"][t][1])
    check(("every tier too" in title) == (below == 4) and ("three tiers of four" in title) == (below == 3)
          and ("both ways" in title) == (below in (1, 2)), "chart title: pharmacy against 2026 (%d tiers below)" % below)
    rep("memo: %d of the 140 had a hospital stay or a cancer course in 2026 (%s)" % (
        len(big), ", ".join("%s %d" % (k, len(v)) for k, v in who.items())))
    tru = {t: sim_pmpm(fin_pids[t], W.PROG_START, W.PROG_END) for t in T}
    truth = sum(n[t] * (tru[t][0] + tru[t][1]) for t in T) / 140
    pooled_truth = sim_pmpm(set().union(*fin_pids.values()), W.PROG_START, W.PROG_END)
    check(abs(g / truth - 1) <= 0.15, "golden within 15 per cent of the untreated programme year")
    rep("regression to the mean, bid members (simulation, real terms): medical %.2f, pharmacy %.2f of the 2024 level "
        "(2024 medical $%.0f, pharmacy $%.0f PMPM); the enrolled members' own pharmacy runs at %.2f of its 2026 level in "
        "the programme year" % (rm, rr, b24[0], b24[1], frr))
    rep("simulated untreated 2027-28 outcome of the enrolled members: $%.2f by tier weights (medical $%.2f, pharmacy $%.2f); "
        "pooled $%.2f; golden/truth %.3f; persistence/truth %.2f" % (
            truth, sum(n[t] * tru[t][0] for t in T) / 140, sum(n[t] * tru[t][1] for t in T) / 140,
            pooled_truth[0] + pooled_truth[1], g / truth, r0 / truth))
    for t in T:
        rep("  tier %d truth medical $%.0f pharmacy $%.0f (%d member months)" % (t, tru[t][0], tru[t][1], tru[t][2]))
    rep("cost-only regression alternative: $%.2f, %+.1f%% from the golden, %+.1f%% from the truth" % (
        rk["regression"], 100 * (rk["regression"] / g - 1), 100 * (rk["regression"] / truth - 1)))
    plan25 = G["letter"]["med_comp"][2025] / G["letter"]["mm"][2025], G["letter"]["rx"][2025] / G["letter"]["mm"][2025]
    check(420 <= plan25[0] <= 560 and 120 <= plan25[1] <= 190, "plan-wide 2025 cost is realistic")
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
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in meta["distractor_files"]:
            os.symlink(os.path.join(TGT, f), os.path.join(tmp, f))
    G2, _ = E.figures(tmp)
    check(abs(G2["prog_total"] - g) < 1e-9 and G2["base"] == base and G2["f26"] == G["f26"], "golden unchanged without the distractors")
    shutil.rmtree(tmp)
    rep("no-move: deleting the four distractors (%s) leaves every graded figure unchanged" % ", ".join(meta["distractor_files"]))

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
    for phrase in ("enrolled in the Plan on the first day of the month", "first date of service", "without completion",
                   "weighted by the number of Enrolled Members", "midpoint of the Programme Year"):
        check(phrase in ag, "Schedule C states %r" % phrase)
    check("Deborah Johnson" in ag and "Chair, School Board" in ag and "Sandra Lopez" in ag, "the Chair signs for the District")
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
        check("—" not in t, "no em dash in %s" % f)
        for word in ("regress", "persistence", "selection bias", "selected for", "control group", "comparison group",
                     "analog", "toward the mean", "mean revers"):
            check(word not in t.lower(), "%s does not say %r" % (f, word))
    plan = alltext["northcourt_implementation_plan_2027-28.pdf"].lower()
    check("$" not in plan and not re.search(r"\d+(\.\d+)? ?(per cent|%)", plan), "the implementation plan carries no amounts")
    for word in ("baseline", "acuity", "stratif", "score", "saving", "cost", "select", "highest", "forecast", "expected", "claims history"):
        check(word not in plan, "the implementation plan does not mention %r" % word)
    cover = [r for r in load_workbook(os.path.join(TGT, "northcourt_rfp_2025-07_stratification_2024_claims.xlsx"),
                                      data_only=True)["Cover"].iter_rows(values_only=True)]
    ctext = " ".join(str(x) for r in cover for x in r if x)
    check("evaluation of RFP 2025-07 only" not in ctext and "only" not in ctext.lower().split("confidential")[-1],
          "the bid list's cover gives no reason it should not be in the folder")
    for pin in ("Northcourt Acuity Model 4.2", "Tier 1: %.1f and above" % W.TIERS[0][1], "1 April 2025 to 31 March 2026",
                "enrolled on 1 January 2025", "eligibility as of 1 January 2025"):
        check(pin in ctext, "the bid list's cover keeps %r" % pin)

    # ------------------------------------------------------------ containers
    # PDFs: the District and its consultant convert Word documents with LibreOffice; the stop-loss carrier's policy
    # system and Northcourt's client portal print HTML with Chromium. Each keeps the producer that wrote it.
    engines = {"care_management_services_agreement_schedule_c.pdf": "LibreOffice", "renewal_letter_2027-28.pdf": "LibreOffice",
               "stop_loss_policy_2027.pdf": "Skia", "northcourt_implementation_plan_2027-28.pdf": "Skia"}
    for f in files:
        p = os.path.join(TGT, f)
        if f.endswith(".pdf"):
            blob = open(p, "rb").read()
            info = pdf_info(p)
            check(info.get("/Producer", "").startswith(engines[f]), "%s keeps its own producer (%s)" % (f, info.get("/Producer")))
            if engines[f] == "LibreOffice":
                check(info.get("/Creator") == "Writer", "%s: LibreOffice Writer" % f)
            else:
                check("Chrome/" in info.get("/Creator", ""), "%s: printed by Chromium" % f)
            check(b"/FontFile2" in blob and b"/StructTreeRoot" in blob and b"/BaseFont/Helvetica" not in blob
                  and b"/BaseFont/Times-Roman" not in blob, "%s embeds its fonts and is tagged" % f)
            for m in re.findall(rb"D:(\d{4})(\d\d)(\d\d)", blob):
                day = dt.date(int(m[0]), int(m[1]), int(m[2]))
                check(dt.date(2024, 12, 1) <= day <= W.ASOF, "%s stamped inside the setting (%s)" % (f, day))
            for sig in (b"ReportLab", b"reportlab", b"python-docx", b"openpyxl"):
                check(sig not in blob, "%s carries no library signature" % f)
        elif f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                names = z.namelist()
                check("docProps/app.xml" not in names and b"docProps/app.xml" not in z.read("_rels/.rels")
                      and b"app.xml" not in z.read("[Content_Types].xml"),
                      "%s claims no application that did not write it" % f)
                props = z.read("docProps/core.xml")
                for sig in (b"openpyxl", b"python-docx", b"LibreOffice", b"Microsoft"):
                    check(sig not in props, "%s carries no writer signature" % f)
                cr = re.search(rb"<dcterms:created[^>]*>([^<]+)<", props).group(1).decode()
                mo = re.search(rb"<dcterms:modified[^>]*>([^<]+)<", props).group(1).decode()
                c_, m2 = dt.datetime.fromisoformat(cr.rstrip("Z")), dt.datetime.fromisoformat(mo.rstrip("Z"))
                check(c_ <= m2 and dt.date(2024, 12, 1) <= c_.date() <= W.ASOF, "%s exported inside the setting" % f)
                local = (m2.replace(tzinfo=dt.timezone.utc).astimezone(
                    __import__("containers").central(m2)).timetuple()[:6])
                local = local[:5] + (local[5] // 2 * 2,)
                check(all(i.date_time == local for i in z.infolist()), "%s entries carry the export time" % f)
                check(not any(i.date_time[0] == 1980 for i in z.infolist()), "%s has no default entry dates" % f)
    for f in os.listdir(GLD):
        with zipfile.ZipFile(os.path.join(GLD, f)) as z:
            names = z.namelist()
            props = b"".join(z.read(x) for x in names if x.startswith("docProps/"))
            check(b"python-docx" not in props and b"openpyxl" not in props, "golden %s carries its author" % f)
            check(not any(x.endswith("thumbnail.jpeg") for x in names), "no template thumbnail")
            check(names[0] == "[Content_Types].xml" and names[-1] == "docProps/app.xml", "golden %s parts in Office order" % f)
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        with zipfile.ZipFile(zp) as z:
            check(sorted(z.namelist()) == files, "target.zip holds the %d files at its top level and nothing else" % len(files))
            for f in files:
                check(z.read(f) == open(os.path.join(TGT, f), "rb").read(), "target.zip carries %s as built" % f)
        rep("target.zip: %d entries, contents identical to target/" % len(files))
    rep("%d assertions passed" % N_ASSERT[0])


if __name__ == "__main__":
    main()
