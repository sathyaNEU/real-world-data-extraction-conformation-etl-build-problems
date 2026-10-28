"""The generator's assertions on the built pack: input gates, the realism sweep, the three rules (R1 to R3c), the
ladder and the golden's family, every semantic fork row (SF1 to SF14), the ask's devices and the separation line.
run() returns the rows and raises if any fails."""
from __future__ import annotations

import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd
from pypdf import PdfReader

import bureau as BU
import pack as PK
import params as P
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def _num(s):
    m = re.findall(r"\d+", str(s))
    return int(m[-1]) if m else None


def _const_step(values):
    v = sorted({x for x in values if x is not None})
    if len(v) < 5:
        return False
    d = np.diff(v)
    return len(set(d.tolist())) == 1


def pdf_text(path):
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def run(shipped, aux, F, ex, target):
    rows = []

    def ok(label, cond, detail=""):
        rows.append((label, bool(cond), detail))

    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    # ---- input gates
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(len(shipped["kshetra"]), len(shipped["collectpro"]))
    ok("G3 a file of 25,000 or more rows", big >= 25000, "%d rows" % big)
    ok("G4 two or more distractors declared", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    bad = [f for f in files if re.search(r"readme|dictionary|manifest|notes|schema|codebook|distractor", f, re.I)]
    ok("G5 no file describes the data or names a distractor", not bad, ", ".join(bad) or "none")
    import openpyxl
    sheets = openpyxl.load_workbook(os.path.join(target, PK.FILES["portfolio"]), read_only=True).sheetnames
    ok("G6 no notes or readme sheet", not any(re.search(r"note|readme|about", s, re.I) for s in sheets),
       ", ".join(sheets))
    # ---- realism sweep
    pt = shipped["pool_tape"]
    ids = {
        "loan_id": [_num(x) for x in pt.loan_id], "member_id": [_num(x) for x in pt.member_id],
        "group_id": [_num(x) for x in pt.group_id],
        "field_officer_id": [_num(x) for x in shipped["centre_master"].field_officer_id],
        "account_no": [_num(x) for x in shipped["cic"].account_no.head(5000)],
    }
    claims = pd.read_csv(os.path.join(target, PK.FILES["claims"]))
    ids["claim_no"] = [_num(x) for x in claims.claim_no]
    for b in sorted({c[:3] for c in shipped["centre_master"].centre_code}):
        ids["centre_code_" + b] = [_num(x) for x in shipped["centre_master"].centre_code if x.startswith(b)]
    const = [k for k, v in ids.items() if _const_step(v)]
    ok("RZ1 no id column runs on one constant step", not const, ", ".join(const) or "none")
    per_branch = pt.branch_code.value_counts()
    ok("RZ2 no two branches carry the same pool count", per_branch.is_unique, str(per_branch.to_dict()))
    tot = int(pt.principal_outstanding_inr.sum())
    ok("RZ3 no round headline total", tot % 1000 != 0 and len(pt) % 100 != 0, "%d loans, INR %d" % (len(pt), tot))
    shapes = {re.sub(r"[A-Z][a-z]+", "W", n).count("W") for n in shipped["cic_directory"].institution}
    ok("RZ4 lender names take more than two shapes", len(shapes) > 2, str(sorted(shapes)))
    fo = shipped["centre_master"].field_officer_id.tolist()
    periodic = any(all(fo[i] == fo[i + k] for i in range(len(fo) - k)) for k in range(1, 40))
    ok("RZ5 field officers are not dealt round-robin", not periodic, "%d centres" % len(fo))
    issuers = {PK.FILES["policy"]: ("Prachi Valley", dt.date(2025, 4, 28)),
               PK.FILES["term_sheet"]: ("Tamralipta", dt.date(2027, 1, 8)),
               PK.FILES["guardrails"]: ("Tamralipta", dt.date(2025, 5, 2)),
               PK.FILES["field_update"]: ("Prachi Valley", dt.date(2026, 11, 18))}
    for f, (who, when) in issuers.items():
        r = PdfReader(os.path.join(target, f))
        md = r.metadata
        cd = str(md.get("/CreationDate", ""))
        y, m, d = int(cd[2:6]), int(cd[6:8]), int(cd[8:10])
        ok("RZ6 %s: producer is its issuer and dated on its own date" % f[:24],
           who in str(md.get("/Producer", "")) and who in str(md.get("/Author", "")) and dt.date(y, m, d) == when,
           "%s %s" % (md.get("/Producer"), cd))
        txt = pdf_text(os.path.join(target, f))
        later = [x for x in re.findall(r"\b(\d{1,2}) (January|February|March|April|May|June|July|August|September|"
                                       r"October|November|December) (20\d\d)\b", txt)
                 if dt.datetime.strptime(" ".join(x), "%d %B %Y").date() > when
                 and not (f == PK.FILES["term_sheet"]) and not (f == PK.FILES["policy"] and x[1] == "May")]
        ok("RZ7 %s states no date after its own" % f[:24], not later, str(later))
    ks_max = pd.to_datetime(shipped["kshetra"].meeting_date).max().date()
    ok("RZ8 no ledger row after the cut-off", ks_max <= P.CUTOFF, str(ks_max))
    rep = pd.to_datetime(shipped["cic"].date_reported).max().date()
    ok("RZ9 no bureau report after the cut-off", rep <= P.CUTOFF, str(rep))
    # ---- three rules
    mc, rv, fam, ab = ex["mc"], ex["rv"], ex["fam"], ex["ab"]
    led = mc["led"]
    ok("R1a the golden reads the member-by-meeting ledger", len(led) == len(shipped["kshetra"]) + len(shipped["collectpro"]),
       "%d rows" % len(led))
    cols = " ".join(c.lower() for k, v in shipped.items() for c in v.columns)
    ok("R1b no shipped column holds a group count, a probability or a forecast",
       not re.search(r"support_count|carried|group_state|probab|forecast|\bpd\b|expected", cols), "columns clean")
    ok("R2a two platforms: the Kshetra months alone leave the call", S_round(F["family_month_True_kshetra_last_3"]) == F["call"],
       "%.1f" % F["family_month_True_kshetra_last_3"])
    raw = shipped.copy()
    mm = shipped["migmap"]
    raw["migmap"] = mm[mm.entity != "GROUP"]
    mc_raw = S.main_call(raw)
    ok("R2b CollectPro's centre-scoped group numbers read raw leave the call", S_round(mc_raw["gold"]) == F["call"],
       "%.1f" % mc_raw["gold"])
    gm = mc["gm"]
    lastmeet = gm[gm.date <= pd.Timestamp(P.CUTOFF)].groupby("group").date.max()
    gap = (pd.Timestamp(P.CUTOFF) - lastmeet.reindex(pt.group_id.unique())).dt.days
    ok("R2c holiday moves leave every pool group a meeting in the fortnight before the cut-off", gap.max() <= 16,
       "max gap %d days" % gap.max())
    ok("R2d the portfolio report, the bureau, the KYC and the field update are not read by the call",
       set(S.CALL_INPUTS) == {"pool_tape", "kshetra", "collectpro", "migmap"}, ", ".join(S.CALL_INPUTS))
    ok("R3a analyst test: the member's own posting files a wrong answer", F["rival_own_posting_printed"] != F["call"],
       "%s against %s" % (F["rival_own_posting_printed"], F["call"]))
    ok("R3b the decisive step alone files the golden; each lower rung stays wrong",
       F["call"] == 300 and F["rival_roll_rate_printed"] != F["call"] and F["rival_group_any_printed"] != F["call"],
       "roll %s, own %s, any %s, golden %s" % (F["rival_roll_rate_printed"], F["rival_own_posting_printed"],
                                             F["rival_group_any_printed"], F["call"]))
    ks = shipped["kshetra"]
    blocks = ks.assign(m=pd.to_datetime(ks.meeting_date).dt.to_period("M")).groupby(["branch_code", "m"]).txn_type.apply(
        lambda s: tuple(s.value_counts().sort_index()))
    ok("R3c no copied block: no two branch-months carry the same postings", blocks.is_unique, "%d branch-months" % len(blocks))
    fu = pdf_text(os.path.join(target, PK.FILES["field_update"]))
    ok("R3c no stakeholder figure: the field update carries no rate, share or forecast", not re.search(r"per cent|%", fu),
       "clean")
    # ---- the ladder and the family
    ok("L1 rungs print where the design says", (F["rival_roll_rate_printed"], F["rival_own_posting_printed"],
                                                F["rival_group_any_printed"], F["call"]) == (100, 100, 200, 300)
       and F["rival_carried_all"] >= 800,
       "%s %s %s %s %s" % (F["rival_roll_rate"], F["rival_own_posting"], F["rival_group_any"], F["call_unrounded"],
                           F["rival_carried_all"]))
    clear = min(F["call_unrounded"] - 250, 350 - F["call_unrounded"])
    ok("L2 the golden clears its bin's edges by 20 or more", clear >= 20, "%.1f" % clear)
    if fam:
        out = {k: v for k, v in fam.items() if not (250 <= v < 350)}
        ok("L3 every member of the golden's family prints 300", not out and len(fam) == 32,
           "%d members %.1f to %.1f" % (len(fam), min(fam.values()), max(fam.values())))
        ok("L4 the family's nearest edge is 15 or more away", min(min(fam.values()) - 250, 350 - max(fam.values())) >= 15,
           "%.1f" % min(min(fam.values()) - 250, 350 - max(fam.values())))
    ok("L5 the record's contrast: two carried at one meeting against two at different meetings",
       F["contrast_same_pct"] >= 8 * max(F["contrast_apart_pct"], 0.1),
       "%.1f per cent against %.1f" % (F["contrast_same_pct"], F["contrast_apart_pct"]))
    ok("L6 the default path sits a full bin below the golden", F["call_unrounded"] - F["rival_own_posting"] >= 100,
       "%.1f" % (F["call_unrounded"] - F["rival_own_posting"]))
    # ---- semantic forks
    lf = mc["lf"]
    cur = S.asof_frame(led, lf, gm, pd.Timestamp(P.CUTOFF), mhp=True)
    ok("SF1 the pool tape is every loan current at the cut-off and past the holding period", set(cur.index) == set(pt.loan_id),
       "%d against %d" % (len(cur), len(pt)))
    cp = shipped["collectpro"]
    part = ((ks.paid_inr != 0) & (ks.paid_inr != ks.due_inr)).sum() + ((cp.COLLN != 0) & (cp.COLLN != cp.DEMAND)).sum()
    ok("SF2 no part payment, so every days-past-due reading agrees", part == 0, "%d" % part)
    ok("SF3 the outcome date is a month end 181 days after the cut-off",
       (P.OUTCOME + dt.timedelta(days=1)).day == 1 and (P.OUTCOME - P.CUTOFF).days == P.HORIZON_DAYS == 181, "")
    sup = ks[ks.txn_type == "GRP_SUPP"]
    ok("SF4 a co-member's payment is paid in full by someone else", (sup.paid_inr == sup.due_inr).all() and
       (sup.paid_by_member_id != sup.member_id).all(), "%d rows" % len(sup))
    for sf, key in (("SF5", "family_meeting_True_all_last_3"), ("SF7", "family_month_True_all_last_two_3"),
                    ("SF8", "family_month_True_all_last_2"), ("SF9", "family_month_True_kshetra_last_3"),
                    ("SF10", "family_month_False_all_last_3")):
        ok("%s %s prints the call" % (sf, key), S_round(F[key]) == F["call"], "%.1f" % F[key])
    ok("SF6 the history's horizon is the call's", P.HORIZON_DAYS == (P.OUTCOME - P.CUTOFF).days, "")
    stopped = led[led.txn == "NOT_PAID"].groupby("loan").date.min()
    later_sup = led[(led.txn == "GRP_SUPP")].join(stopped.rename("first_np"), on="loan")
    ok("SF11 no co-member payment after a loan's first unpaid instalment",
       not (later_sup.date > later_sup.first_np).any(), "")
    ok("SF12 the call is the expected count to the nearest 100", F["call"] == S_round(F["call_unrounded"]), "")
    ok("SF13 the call holds with the cut-off's own meetings left out", F["sf_cutoff_meetings"] > 0 and
       S_round(F["sf_cutoff_strict"]) == F["call"], "%.1f, %d groups met on the cut-off" % (F["sf_cutoff_strict"],
                                                                                         F["sf_cutoff_meetings"]))
    for col in ("district", "branch", "cycle"):
        ok("SF14 the call holds with the history's rates by %s" % col,
           S_round(F["sf_grain_%s" % col]) == F["call"], "%.1f" % F["sf_grain_%s" % col])
    # ---- the ask
    bt = aux["bureau_truth"]
    bor = ab["borrower"].set_index("member_id")
    agree = sum(bool(bor.loc[m, "breach"]) == v["breach"] for m, v in bt.items())
    ok("A1 the golden handling reproduces every borrower's truth", agree == len(bt), "%d of %d" % (agree, len(bt)))
    for name, key, lk in (("bureau summary", "summary_n", None), ("member codes", "codes_n", "codes_l"),
                          ("stale rows kept", "stale_n", "stale_l"), ("successor only", "succ_only_n", "succ_only_l")):
        miss_n = all(ab[key].get(b, 0) != ab["gold_n"].get(b, 0) for b in ab["gold_n"].index)
        miss_l = True if lk is None else all(abs(ab[lk].get(b, 0) - ab["gold_l"].get(b, 0)) >= 0.1
                                             for b in ab["gold_l"].index)
        ok("A2 %s misses every branch" % name, miss_n and miss_l, "")
    cic = shipped["cic"]
    mf = cic[cic.account_type.isin(BU.MF_TYPES) & (cic.account_status == "ACTIVE")]
    g = mf.groupby(["inquiry_ref", "member_code", "date_opened", "sanctioned_amount"])
    pairs = g.filter(lambda x: len(x) > 1)
    stale_ok = pairs.groupby(["inquiry_ref", "member_code", "date_opened", "sanctioned_amount"]).date_reported.apply(
        lambda s: (s == "2026-03-13").sum() == 1 and len(s) == 2).all()
    ok("A3 every same-loan pair is one current report and one left at 13 March 2026", bool(stale_ok) and
       (pairs.member_code == "SFB0014").all(), "%d pairs" % (len(pairs) // 2))
    flips = {}
    for m, v in bt.items():
        if v["lenders"] < 4 and v["debt"] <= 200000 < v["debt_with_stale"]:
            b = pt.set_index("member_id").loc[m, "branch_code"]
            flips[b] = flips.get(b, 0) + 1
    ok("A4 every branch has three or more borrowers the stale rows push over the line",
       len(flips) == 14 and min(flips.values()) >= 3, str(flips))
    ok("A5 separation: no ask device row sits in the call's files", set(S.CALL_INPUTS).isdisjoint({"cic", "cic_directory",
                                                                                                     "kyc"}), "")
    ok("A6 every graded ask figure is a whole count or INR lakh to one decimal", all(
        float(F["ask_lakh_%s" % b]) == round(F["ask_lakh_%s" % b], 1) for b in ab["gold_n"].index), "")
    # ---- misc
    ok("M1 one pool loan per member", pt.member_id.is_unique, "")
    dup = led.duplicated(["loan", "inst"]).sum()
    ok("M2 one ledger row per loan and instalment", dup == 0, "%d" % dup)
    ok("M3 no persona or personal name in any document", all(not re.search(r"\b(Mr|Mrs|Ms|Shri|Smt)\b",
                                                                            pdf_text(os.path.join(target, f)))
                                                             for f in files if f.endswith(".pdf")), "")
    failed = [r for r in rows if not r[1]]
    return rows, failed


def S_round(v):
    return int(round(v / 100.0) * 100)
