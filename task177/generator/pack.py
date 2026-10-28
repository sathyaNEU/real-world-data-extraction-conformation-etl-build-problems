"""The data room Prachi Valley Microfinance opened for Tamralipta Bank, built from the simulated book.

tables() returns the shipped tables as DataFrames plus the truth the generator keeps for itself; write() puts the
tables and documents into a folder. Every shipped row before the cut-off comes from the simulation; nothing after
the cut-off is shipped."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import bureau as BU
import docs as DOCS
import geo as GEO
import params as P
import world as W

PFX = {"KND": 11, "PTM": 12, "RJN": 13, "JSP": 21, "TRT": 22, "ERS": 23, "BDK": 31, "CHB": 32, "BLS": 41,
       "BST": 42, "JJR": 51, "BNJ": 52, "SLP": 61, "NIA": 62}


def principal_after(amount, n):
    r = P.RATE_PA / 26.0
    a = amount * r / (1 - (1 + r) ** (-P.INSTALMENTS))
    a = round(a, 0)
    bal = float(amount)
    for _ in range(int(n)):
        interest = round(bal * r, 2)
        bal = round(bal - (a - interest), 2)
    return max(bal, 0.0)


def dmy(d, sep="-"):
    return d.strftime("%d" + sep + "%m" + sep + "%Y")


def tables(w=None):
    w = w or W.simulate()
    rng = np.random.default_rng(P.SEED_PACK)
    centres = w["centres"]
    cdates = w["cdates"]
    burn = w["burn"]
    L = pd.DataFrame(w["loans"]).set_index("id")
    members = pd.DataFrame(w["members"]).set_index("id")
    groups = pd.DataFrame(w["groups"]).set_index("id")
    R = pd.DataFrame(w["rows"], columns=["ti", "ci", "grp", "mem", "loan", "inst", "due", "post", "payer"])
    R["date"] = [cdates[c][t] for c, t in zip(R.ci, R.ti)]
    R = R[R.date <= P.CUTOFF].reset_index(drop=True)
    # identifiers: Kshetra ids for every entity, CollectPro ids for the ones the old platform saw
    cen = pd.DataFrame(centres)
    gaps = rng.integers(1, 4, size=len(cen))
    cen["seq"] = pd.Series(gaps).groupby(cen.branch.values).cumsum().values + 2
    cen["centre_code"] = [f"{b}{s:03d}" for b, s in zip(cen.branch, cen.seq)]
    cen["legacy_centre"] = [f"{b}/{s:03d}" for b, s in zip(cen.branch, cen.seq)]
    mem_ids = {}
    leg_mem = {}
    used = set()
    for m in sorted(set(R.mem) | set(R.payer[R.payer >= 0])):
        while True:
            x = int(rng.integers(1_000_000, 9_999_999))
            if x not in used:
                used.add(x)
                break
        mem_ids[m] = f"M{x:07d}"
    loan_ids, leg_loan = {}, {}
    grp_slot = groups["slot"].to_dict()
    slots = w["slots"]
    group_ids = {g: f"G{centres[slots[grp_slot[g]]['centre']]['branch']}{g:05d}" for g in groups.index}
    # loan ids carry the branch prefix; legacy ids carry the branch code
    br_of_loan = {}
    for l, ci in zip(R.loan, R.ci):
        br_of_loan.setdefault(l, centres[ci]["branch"])
    loan_ids = {l: f"JL{PFX[b]:02d}{l:08d}" for l, b in br_of_loan.items()}
    seq = {}
    br_of_mem = {}
    for m, ci in zip(R.mem, R.ci):
        br_of_mem.setdefault(m, centres[ci]["branch"])
    for m, b in sorted(br_of_mem.items()):
        seq[b] = seq.get(b, 0) + int(rng.integers(1, 4))
        leg_mem[m] = f"PV/{b}/{seq[b]:06d}"
    lseq = {}
    for l, b in sorted(br_of_loan.items()):
        lseq[b] = lseq.get(b, 0) + int(rng.integers(1, 3))
        leg_loan[l] = f"{b}JL{lseq[b]:07d}"
    fo_pool = {}
    used_fo = set()
    for b in sorted({c["branch"] for c in centres}):
        n_fo = int(rng.integers(18, 31))
        ids = []
        while len(ids) < n_fo:
            x = int(rng.integers(1000, 9999))
            if x not in used_fo:
                used_fo.add(x)
                ids.append(f"FO{x:04d}")
        fo_pool[b] = ids
    fo_of_centre = {ci: fo_pool[c["branch"]][int(rng.integers(0, len(fo_pool[c["branch"]])))]
                    for ci, c in enumerate(centres)}
    R["centre_code"] = cen.centre_code.values[R.ci]
    R["branch"] = [centres[c]["branch"] for c in R.ci]
    old = R[R.date < P.MIGRATION]
    new = R[R.date >= P.MIGRATION]
    slot_no = {g: slots[grp_slot[g]]["slot"] for g in groups.index}
    collectpro = pd.DataFrame({
        "MTG_DT": [dmy(d, "/") for d in old.date],
        "BR": old.branch.values,
        "CENTRE": cen.legacy_centre.values[old.ci],
        "GRP": [slot_no[g] for g in old.grp],
        "MEM_CODE": [leg_mem[m] for m in old.mem],
        "LOAN_AC": [leg_loan[l] for l in old.loan],
        "INST": old.inst.values,
        "DEMAND": old.due.astype(int).values,
        "COLLN": np.where(old.post == "NP", 0, old.due.astype(int).values),
        "MODE": old.post.map({"SELF": "SELF", "GS": "GS", "NP": "NIL"}).values,
        "PAID_BY": [leg_mem[p] if (p >= 0 and po != "NP") else "" for p, po in zip(old.payer, old.post)],
        "FO": [fo_of_centre[c] for c in old.ci],
    })
    kshetra = pd.DataFrame({
        "meeting_date": pd.to_datetime(new.date).dt.date,
        "branch_code": new.branch.values,
        "centre_code": new.centre_code.values,
        "group_id": [group_ids[g] for g in new.grp],
        "member_id": [mem_ids[m] for m in new.mem],
        "loan_id": [loan_ids[l] for l in new.loan],
        "instalment_no": new.inst.values.astype("int16"),
        "due_inr": new.due.astype("int32").values,
        "paid_inr": np.where(new.post == "NP", 0, new.due.astype(int).values).astype("int32"),
        "txn_type": new.post.map({"SELF": "OWN", "GS": "GRP_SUPP", "NP": "NOT_PAID"}).values,
        "paid_by_member_id": [mem_ids[p] if (p >= 0 and po != "NP") else None for p, po in zip(new.payer, new.post)],
        "field_officer_id": [fo_of_centre[c] for c in new.ci],
    })
    # the migration map: every member, loan and group CollectPro held at 31 March 2025 and Kshetra took over
    mig_m = sorted(set(old.mem) & set(new.mem))
    mig_l = sorted(set(old.loan) & set(new.loan))
    mig_g = sorted(set(old.grp) & set(new.grp))
    migmap = pd.concat([
        pd.DataFrame({"entity": "MEMBER", "collectpro_id": [leg_mem[m] for m in mig_m],
                      "kshetra_id": [mem_ids[m] for m in mig_m]}),
        pd.DataFrame({"entity": "LOAN", "collectpro_id": [leg_loan[l] for l in mig_l],
                      "kshetra_id": [loan_ids[l] for l in mig_l]}),
        pd.DataFrame({"entity": "GROUP",
                      "collectpro_id": [f"{cen.legacy_centre.values[slots[grp_slot[g]]['centre']]}-{slot_no[g]}" for g in mig_g],
                      "kshetra_id": [group_ids[g] for g in mig_g]}),
    ], ignore_index=True)
    # the pool: every loan current at the cut-off, disbursed on or before 1 October 2026
    last = R.groupby("loan").agg(ci=("ci", "first"), grp=("grp", "first"), mem=("mem", "first"),
                                 paid=("post", lambda s: int((s != "NP").sum())),
                                 unpaid=("post", lambda s: int((s == "NP").sum())), last_inst=("inst", "max"))
    disb_date = {}
    for l in last.index:
        di = int(L.loc[l, "disb"]) - burn
        ci = int(last.loc[l, "ci"])
        disb_date[l] = cdates[ci][di] if di >= 0 else (P.HIST_START - dt.timedelta(days=14 * (-di)))
    last["disbursed"] = pd.Series(disb_date)
    last["amount"] = L.loc[last.index, "amount"].values
    last["inst_amt"] = L.loc[last.index, "inst"].values
    last["cycle"] = L.loc[last.index, "cycle"].values
    open_ = last[(last.unpaid == 0) & (last.last_inst < P.INSTALMENTS)]
    pool = open_[open_.disbursed <= P.CUTOFF - dt.timedelta(days=P.MHP_DAYS)].copy()
    # a loan's last meeting must be its group's last meeting on or before the cut-off (a stopped group's loans have
    # unpaid rows and are already out)
    pool["principal"] = [round(principal_after(a, n), 0) for a, n in zip(pool.amount, pool.last_inst)]
    pool["next_due"] = [next(d for d in cdates[int(ci)] if d > P.CUTOFF) for ci in pool.ci]
    geo_v, gp_now, reorg, declared = GEO.build(centres, P.SEED_GEO)
    pool = pool.sort_values(["ci", "grp", "mem"])
    pool_tape = pd.DataFrame({
        "loan_id": [loan_ids[l] for l in pool.index],
        "member_id": [mem_ids[m] for m in pool.mem],
        "branch_code": [centres[int(c)]["branch"] for c in pool.ci],
        "branch": [centres[int(c)]["branch_name"] for c in pool.ci],
        "district": [centres[int(c)]["district"] for c in pool.ci],
        "centre_code": cen.centre_code.values[pool.ci.astype(int)],
        "group_id": [group_ids[g] for g in pool.grp],
        "loan_cycle": pool.cycle.values,
        "product": "JLG-24F",
        "disbursed_on": [dmy(d) for d in pool.disbursed],
        "sanctioned_inr": pool.amount.astype(int).values,
        "instalments": P.INSTALMENTS,
        "instalment_inr": pool.inst_amt.astype(int).values,
        "instalments_paid": pool.last_inst.astype(int).values,
        "principal_outstanding_inr": pool.principal.astype(int).values,
        "next_due_on": [dmy(d) for d in pool.next_due],
        "dpd_at_cutoff": 0,
    })
    # KYC for the pool's members: village, GP and block as recorded at enrolment
    enrol = {}
    for m in pool.mem:
        j = members.loc[m, "joined"] - burn
        ci = int(pool.loc[pool.mem == m, "ci"].iloc[0])
        if j >= 0:
            enrol[m] = cdates[ci][j]
        else:
            enrol[m] = P.HIST_START - dt.timedelta(days=int(rng.integers(30, 2600)))
    kyc_rows = []
    for l in pool.index:
        m = int(pool.loc[l, "mem"])
        ci = int(pool.loc[l, "ci"])
        v = geo_v[ci]
        gp = v["gp_now"] if enrol[m] >= P.MIGRATION else v["gp_old"]
        kyc_rows.append(dict(member_id=mem_ids[m], cic_ref="KY%010d" % int(rng.integers(10 ** 9, 10 ** 10 - 1)),
                             enrolled_on=dmy(enrol[m]), village=v["village"], gram_panchayat=gp, block=v["block"],
                             district=v["district"], centre_code=cen.centre_code.values[ci]))
    kyc = pd.DataFrame(kyc_rows)
    # the bureau's portfolio review of the pool's borrowers
    bpool = [dict(member_id=r.member_id, cic_ref=r.cic_ref, district=r.district, branch=pt.branch_code,
                  principal=int(pt.principal_outstanding_inr), sanctioned=int(pt.sanctioned_inr),
                  disbursed=dt.datetime.strptime(pt.disbursed_on, "%d-%m-%Y").date())
             for r, pt in zip(kyc.itertuples(), pool_tape.itertuples())]
    brow, btruth = BU.build(bpool, P.SEED_BUREAU)
    cic = pd.DataFrame(brow)
    for c in ("date_opened", "date_reported"):
        cic[c] = [d.isoformat() for d in cic[c]]
    cic["date_closed"] = [d.isoformat() if d else "" for d in cic.date_closed]
    cdir = pd.DataFrame(BU.directory())
    centre_master = pd.DataFrame({
        "centre_code": cen.centre_code, "collectpro_centre": cen.legacy_centre, "branch_code": cen.branch,
        "village": [geo_v[i]["village"] for i in range(len(cen))],
        "meeting_day": [cdates[i][0].strftime("%A") for i in range(len(cen))],
        "field_officer_id": [fo_of_centre[i] for i in range(len(cen))],
    })
    aux = dict(w=w, R=R, pool=pool, fo_pool=fo_pool, pool_tape=pool_tape, mem_ids=mem_ids, loan_ids=loan_ids, group_ids=group_ids,
               leg_mem=leg_mem, leg_loan=leg_loan, geo=geo_v, gp_now=gp_now, reorg=reorg, declared=declared,
               bureau_truth=btruth, cen=cen)
    shipped = dict(pool_tape=pool_tape, kshetra=kshetra, collectpro=collectpro, migmap=migmap, kyc=kyc, cic=cic,
                   cic_directory=cdir, centre_master=centre_master)
    return shipped, aux


if __name__ == "__main__":
    import time
    t0 = time.time()
    s, a = tables()
    for k, v in s.items():
        print(k, v.shape)
    print("pool", len(a["pool"]), "%.1fs" % (time.time() - t0))


FILES = {
    "pool_tape": "pool_tape_PVM_2026-12_cutoff_20261231.csv",
    "kshetra": "kshetra_collections_2025-04_to_2026-12.parquet",
    "collectpro_a": "collectpro_collections_FY2023-24.csv",
    "collectpro_b": "collectpro_collections_FY2024-25.csv",
    "migmap": "kshetra_migration_map_20250401.csv",
    "kyc": "member_kyc_pool_20261231.csv",
    "centre_master": "centre_master_20261231.csv",
    "cic": "cic_portfolio_review_PVM_20261231.csv",
    "cic_directory": "cic_member_directory_202612.csv",
    "policy": "pvm_jlg_operating_policy_v6.pdf",
    "term_sheet": "tb_term_sheet_PVM-2026-12.pdf",
    "guardrails": "tb_cpn_mf07_microfinance_guardrails.pdf",
    "field_update": "pvm_field_update_cyclone_2026-11.pdf",
    "portfolio": "pvm_portfolio_report_FY2024-25_to_FY2026-27.xlsx",
    "claims": "pvm_credit_life_claims_2023-2026.csv",
    "postings": "pvm_field_officer_postings_2026.csv",
}


def portfolio_report(aux, path):
    """The MFI's monthly MIS by branch: active borrowers, gross loan portfolio (INR lakh), PAR 30 and PAR 90 (per cent
    of GLP) and collection efficiency (per cent), month ends from April 2024, one sheet per fiscal year; Kshetra's
    report from FY2025-26 adds a column and reorders the block."""
    import openpyxl
    from openpyxl.styles import Font
    R = aux["R"]
    w = aux["w"]
    L = pd.DataFrame(w["loans"]).set_index("id")
    centres = w["centres"]
    br = np.array([c["branch"] for c in centres])
    R2 = R.assign(br=br[R.ci])
    R2["d"] = pd.to_datetime(R2.date)
    fnp = R2[R2.post == "NP"].groupby("loan").d.min()
    months = pd.date_range("2024-04-30", "2026-12-31", freq="ME")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    names = [b[0] for b in P.BRANCHES]
    bname = {b[0]: b[1] for b in P.BRANCHES}
    for fy, (a, z) in {"FY2024-25": ("2024-04-01", "2025-03-31"), "FY2025-26": ("2025-04-01", "2026-03-31"),
                       "FY2026-27": ("2026-04-01", "2027-03-31")}.items():
        ws = wb.create_sheet(fy)
        ws["A1"] = "Prachi Valley Microfinance Pvt Ltd: branch portfolio report, " + fy
        ws["A1"].font = Font(bold=True)
        ws["A2"] = "INR lakh; PAR and collection efficiency in per cent; month-end figures"
        new = fy != "FY2024-25"
        hdr = (["Month", "Branch", "Branch name", "Active borrowers", "GLP (INR lakh)", "PAR 30 %", "PAR 90 %",
                "Collection efficiency %"] if not new else
               ["Month", "Branch", "Active borrowers", "GLP (INR lakh)", "Collection efficiency %", "PAR 30 %",
                "PAR 90 %", "Write-off in month (INR lakh)"])
        ws.append([])
        ws.append(hdr)
        for m in months[(months >= pd.Timestamp(a)) & (months <= pd.Timestamp(z))]:
            upto = R2[R2.d <= m]
            last = upto.sort_values("d").groupby("loan").tail(1)
            open_l = last[(last.inst < P.INSTALMENTS) | (last.post == "NP")]
            fu = open_l.loan.map(fnp)
            dpd = (m - fu).dt.days.where(fu <= m, 0).fillna(0)
            wo = dpd >= P.WRITE_OFF_DPD
            amt = L.loc[open_l.loan, "amount"].values
            frac = np.clip(1 - open_l.inst.values / P.INSTALMENTS, 0, 1)
            glp = amt * frac
            mon = R2[(R2.d > m - pd.offsets.MonthEnd(1)) & (R2.d <= m)]
            for b in names:
                sel = (open_l.br == b).values & ~wo.values
                g = glp[sel].sum()
                p30 = glp[sel & (dpd.values >= 30)].sum()
                p90 = glp[sel & (dpd.values >= 90)].sum()
                mm = mon[mon.br == b]
                ce = 100.0 * (mm.post != "NP").sum() / max(len(mm), 1)
                nb = int(open_l[sel].mem.nunique())
                wol = glp[(open_l.br == b).values & wo.values & (dpd.values < P.WRITE_OFF_DPD + 31)].sum() / 1e5
                if not new:
                    ws.append([m.strftime("%b-%y"), b, bname[b], nb, round(g / 1e5, 2), round(100 * p30 / g, 2),
                               round(100 * p90 / g, 2), round(ce, 1)])
                else:
                    ws.append([m.strftime("%Y-%m"), b, nb, round(g / 1e5, 2), round(ce, 1), round(100 * p30 / g, 2),
                               round(100 * p90 / g, 2), round(wol, 2)])
    wb.properties.creator = "Prachi Valley Microfinance MIS"
    wb.properties.lastModifiedBy = "Prachi Valley Microfinance MIS"
    wb.save(path)
    DOCS.fixed_xlsx(path)


def distractors(aux, rng):
    """Credit-life claims settled on members' deaths, and field officers' postings; neither is read by the answer."""
    w = aux["w"]
    members = pd.DataFrame(w["members"])
    left = members[members.left.notna()].sample(n=140, random_state=int(rng.integers(0, 10 ** 6)))
    nos = 310100 + np.cumsum(rng.integers(1, 9, size=len(left)))
    deaths = sorted(P.HIST_START + dt.timedelta(days=int(rng.integers(0, 1270))) for _ in range(len(left)))
    claims = pd.DataFrame({
        "claim_no": ["CL%06d" % x for x in nos],
        "member_ref": ["PVM%07d" % int(rng.integers(1_000_000, 9_999_999)) for _ in range(len(left))],
        "date_of_death": [d.isoformat() for d in deaths],
        "claim_intimated": [(d + dt.timedelta(days=int(rng.integers(5, 60)))).isoformat() for d in deaths],
        "sum_assured_inr": [int(rng.integers(40, 81)) * 1000 for _ in range(len(left))],
        "insurer": [str(rng.choice(["Navodaya Life Insurance", "Sarvottam Life Insurance"])) for _ in range(len(left))],
    })
    claims["settled_inr"] = [int(round(s * rng.uniform(0.45, 1.0), -1)) for s in claims.sum_assured_inr]
    # the register is the export of 8 January 2027: a death not yet intimated is not in it, and a claim intimated in
    # the last thirty days is still open
    export = P.CUTOFF + dt.timedelta(days=8)
    claims = claims[claims.claim_intimated <= export.isoformat()].copy()
    recent = claims.claim_intimated > (export - dt.timedelta(days=30)).isoformat()
    claims["settled_inr"] = claims.settled_inr.astype("Int64").mask(recent)
    posts = []
    for b, ids in sorted(aux["fo_pool"].items()):
        for f in ids:
            posts.append(dict(field_officer_id=f, branch_code=b,
                              posted_from=(dt.date(2024, 4, 1) + dt.timedelta(days=int(rng.integers(0, 700)))).isoformat(),
                              designation=str(rng.choice(["Field Officer", "Field Officer", "Senior Field Officer"])),
                              centres_assigned=int(rng.integers(6, 27))))
    return claims, pd.DataFrame(posts).sort_values(["branch_code", "posted_from"]).reset_index(drop=True)


def write(out, shipped=None, aux=None):
    if shipped is None:
        shipped, aux = tables()
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(P.SEED_PACK + 1)
    n = {}

    def csv(key, df):
        df.to_csv(os.path.join(out, FILES[key]), index=False, lineterminator="\n")
        n[FILES[key]] = len(df)
    csv("pool_tape", shipped["pool_tape"])
    ks = shipped["kshetra"].copy()
    ks.to_parquet(os.path.join(out, FILES["kshetra"]), index=False, compression="zstd")
    n[FILES["kshetra"]] = len(ks)
    cp = shipped["collectpro"]
    d = pd.to_datetime(cp.MTG_DT, format="%d/%m/%Y")
    csv("collectpro_a", cp[d < pd.Timestamp("2024-04-01")])
    csv("collectpro_b", cp[d >= pd.Timestamp("2024-04-01")])
    csv("migmap", shipped["migmap"])
    csv("kyc", shipped["kyc"])
    csv("centre_master", shipped["centre_master"])
    csv("cic", shipped["cic"])
    csv("cic_directory", shipped["cic_directory"])
    pt = shipped["pool_tape"]
    DOCS.operating_policy(os.path.join(out, FILES["policy"]))
    DOCS.term_sheet(os.path.join(out, FILES["term_sheet"]), len(pt), pt.principal_outstanding_inr.sum() / 1e5)
    DOCS.guardrails(os.path.join(out, FILES["guardrails"]))
    DOCS.field_update(os.path.join(out, FILES["field_update"]))
    portfolio_report(aux, os.path.join(out, FILES["portfolio"]))
    claims, posts = distractors(aux, rng)
    csv("claims", claims)
    csv("postings", posts)
    return n
