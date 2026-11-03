"""Stage-2 pricing harness for task402 (never shipped): prices every rung on the clean truth."""
import sys
import numpy as np
import pandas as pd
from datetime import date, timedelta
import world as W


def measure(w):
    """The national measure per referral, computed from contacts and scores as a solver would."""
    c = w.contacts
    t = c[(c.ctype == "treatment") & (c.attend == "attended")].merge(w.scores, on="cid", how="left")
    t = t.sort_values(["ref", "date", "cid"])
    g = t.groupby("ref")
    first = g.first()
    last = g.last()
    n = g.size().rename("n_treat_att")
    out = w.referrals.set_index("ref")[["received", "end", "end_reason"]].join(n, how="left")
    out["n_treat_att"] = out["n_treat_att"].fillna(0).astype(int)
    out["phq_first"] = first["phq9"]
    out["gad_first"] = first["gad7"]
    out["phq_last"] = last["phq9"]
    out["gad_last"] = last["gad7"]
    out["first_pid"] = first["pid"]
    out["last_pid"] = last["pid"]
    tr = w.truth.set_index("ref")
    out = out.join(tr[["step", "wait", "cohort", "start", "agency0", "broken", "broken_kind", "broken_at",
                       "handover_date", "cf_end", "left_list", "modality", "cf_rec", "a_date"]])
    out["finished"] = out.n_treat_att >= 2
    out["case"] = (out.phq_first >= 10) | (out.gad_first >= 8)
    out["fc"] = out.finished & out.case
    out["rec"] = out.fc & (out.phq_last <= 9) & (out.gad_last <= 7)
    out["fy"] = np.where((out.end >= W.FY25[0]) & (out.end <= W.FY25[1]), 25,
                         np.where((out.end >= W.FY24[0]) & (out.end <= W.FY24[1]), 24, 0))
    lc = c.sort_values(["ref", "date", "cid"]).groupby("ref").last()
    out["disch_pid"] = lc["pid"]
    kind = dict(zip(w.prac.pid, w.prac.kind))
    out["disch_kind"] = out.disch_pid.map(kind)
    out["first_kind"] = out.first_pid.map(kind)
    out["early"] = (out.n_treat_att >= 1) & (out.end_reason == "dropped_out")
    return out


def funnel(m):
    rows = []
    for fy in (24, 25):
        for st in (2, 3):
            s = m[(m.fy == fy) & (m.step == st)]
            rows.append(dict(fy=fy, step=st, ended=len(s), entered=int((s.n_treat_att >= 1).sum()),
                             finished=int(s.finished.sum()), fc=int(s.fc.sum()), rec=int(s.rec.sum()),
                             rate=round(100 * s.rec.sum() / max(1, s.fc.sum()), 1),
                             early=int(s.early.sum())))
    return pd.DataFrame(rows)


def landmark(br, ub):
    cf = 0.0
    for k, grp in br.groupby("broken_at"):
        base = ub[ub.n_treat_att >= max(1, k)]
        cf += len(grp) * base.rec.mean()
    return cf - br.rec.sum()


def landmark_band(br, ub):
    cf = 0.0
    bands = pd.cut(br.broken_at, [-1, 2, 5, 8, 99])
    for b, grp in br.groupby(bands, observed=True):
        lo = int(b.left) + 1
        base = ub[ub.n_treat_att >= max(1, lo)]
        cf += len(grp) * base.rec.mean()
    return cf - br.rec.sum()


def price(m, w):
    res = {}
    f25 = m[m.fy == 25]
    f24 = m[m.fy == 24]
    s3_25 = f25[f25.step == 3]
    s3_24 = f24[f24.step == 3]
    started25 = s3_25[s3_25.n_treat_att >= 1]
    # ---------- default path ----------
    p_rec_started = started25.rec.mean()
    long = started25[started25.wait >= 18]
    short = started25[started25.wait < 18]
    c_in = len(long) * (short.rec.mean() - long.rec.mean())
    left25 = s3_25.left_list.mean()
    left24 = s3_24.left_list.mean()
    c_left = (left25 - left24) * len(s3_25) * p_rec_started
    res["C_default"] = c_in + c_left
    res["C_default_in"] = c_in
    res["C_left"] = c_left
    fc = s3_25[s3_25.fc]
    ra = fc[fc.disch_kind == "agency"].rec.mean()
    re_ = fc[fc.disch_kind == "employed"].rec.mean()
    res["A_kpi_rates"] = (round(100 * ra, 1), round(100 * re_, 1))
    res["A_default"] = max(0.0, (re_ - ra) * (fc.disch_kind == "agency").sum())
    fa = started25[started25.first_kind == "agency"]
    fe = started25[started25.first_kind == "employed"]
    res["A_first_kind"] = len(fa) * (fe.rec.mean() - fa.rec.mean())
    res["first_kind_rates"] = (round(100 * fa.rec.mean(), 1), round(100 * fe.rec.mean(), 1), len(fa), len(fe))
    cells = {}
    for lw in (False, True):
        for k in ("employed", "agency"):
            g = started25[((started25.wait >= 18) == lw) & (started25.first_kind == k)]
            cells[("long" if lw else "short") + "_" + k] = (len(g), round(100 * g.early.mean(), 1) if len(g) else None,
                                                         round(100 * g.rec.mean(), 1) if len(g) else None)
    res["cells"] = cells
    s2 = f25[(f25.step == 2) & f25.fc]
    ph = s2[s2.modality == "phone"]
    vf = s2[s2.modality.isin(["video", "face_to_face"])]
    res["B"] = len(ph) * (vf.rec.mean() - ph.rec.mean())
    s2_24 = f24[(f24.step == 2) & f24.fc]
    ph24 = s2_24[s2_24.modality == "phone"]
    res["B_vs24"] = len(ph) * (ph24.rec.mean() - ph.rec.mean())
    dg = s2[(s2.modality == "digital")]
    dg24 = s2_24[s2_24.modality == "digital"]
    res["D"] = len(dg) * (dg24.rec.mean() - dg.rec.mean())
    gr24 = s2_24[s2_24.modality == "group"]
    n_div = int(round(len(f25[(f25.step == 2) & f25.fc]) * (len(gr24) / max(1, len(s2_24))))) - \
        int((s2.modality == "group").sum())
    res["E"] = max(0, n_div) * (gr24.rec.mean() - ph.rec.mean())
    # ---------- golden: the broken courses ----------
    br = started25[(started25.broken == True) & (started25.broken_kind == "agency")]
    ub = started25[started25.broken != True]
    res["broken_n"] = len(br)
    res["broken_rec"] = int(br.rec.sum())
    res["A_landmark"] = landmark(br, ub)
    res["A_landmark_band"] = landmark_band(br, ub)
    res["A_pooled"] = len(br) * ub.rec.mean() - br.rec.sum()
    ua = ub[ub.first_kind == "agency"]
    res["A_agency_unbroken"] = len(br) * ua.rec.mean() - br.rec.sum()
    res["A_agency_unbroken_lm"] = landmark(br, ua)
    ul = ub[ub.wait >= 18]
    res["A_longwait_unbroken"] = len(br) * ul.rec.mean() - br.rec.sum()
    res["A_longwait_unbroken_lm"] = landmark(br, ul)
    bra = started25[started25.broken == True]
    res["A_all_handovers"] = landmark(bra, ub)
    ue = ub[ub.first_kind == "employed"]
    res["A_lm_emp"] = landmark(br, ue)
    res["A_pooled_emp"] = len(br) * ue.rec.mean() - br.rec.sum()
    cov = started25[(started25.first_kind == "agency") & (started25.first_pid != "S3A-00")]
    res["A_cover_coarse"] = len(cov) * (fe.rec.mean() - cov.rec.mean())
    res["A_cover_coarse_lm"] = len(cov) * (ue.rec.mean() - cov.rec.mean())
    # 2024-25 courses as the comparison (same step, the year before)
    s3_24s = s3_24[s3_24.n_treat_att >= 1]
    res["A_vs_fy24_lm"] = landmark(br, s3_24s[s3_24s.broken != True])
    ubl = ub[ub.wait >= 18]
    ubs = ub[ub.wait < 18]
    res["direct_long_vs_short"] = (round(100 * ubl.rec.mean(), 1), round(100 * ubs.rec.mean(), 1), len(ubl), len(ubs))
    res["C_golden"] = c_left + len(ubl) * (ubs.rec.mean() - ubl.rec.mean())
    res["C_golden_lm"] = c_left + landmark(ubl.assign(broken_at=0), ubs) * -1 if False else c_left
    res["broken_before2"] = int((br.broken_at < 2).sum())
    res["broken_employed"] = int(((started25.broken == True) & (started25.broken_kind == "employed")).sum())
    res["broken_disch_kind"] = br.disch_kind.value_counts().to_dict()
    res["cf_end_max"] = str(br.cf_end.max())
    # breaks by handover date
    bd = br.groupby("handover_date").size().sort_index()
    res["breaks_last_date"] = (str(bd.index[-1]), int(bd.iloc[-1])) if len(bd) else None
    res["breaks_max_date"] = (str(bd.idxmax()), int(bd.max())) if len(bd) else None
    res["breaks_by_month"] = br.groupby(pd.to_datetime(br.handover_date).dt.month).size().to_dict()
    # within the long-wait cohort: early endings and recovery by wait band
    lw = started25[started25.wait >= 18]
    wb = pd.cut(lw.wait, [17, 21, 25, 29, 40])
    res["cohort_by_wait"] = {str(k): (len(g), round(100 * g.early.mean(), 1), round(100 * g.rec.mean(), 1))
                             for k, g in lw.groupby(wb, observed=True)}
    # timing route: agency-first courses by start month, early-ending rate
    ag = started25[started25.first_kind == "agency"]
    res["agency_by_start_month"] = {int(k): (len(g), round(100 * g.early.mean(), 1))
                                    for k, g in ag.groupby(pd.to_datetime(ag.start).dt.month)}
    return res


def caseloads(w):
    c = w.contacts
    a = c[(c.attend == "attended") & (c.ctype == "treatment") & (c.step == 3)].copy()
    a["wk"] = pd.to_datetime(a.date).dt.to_period("W")
    kind = dict(zip(w.prac.pid, w.prac.kind))
    a["kind"] = a.pid.map(kind)
    pw = a.groupby(["pid", "wk"]).size()
    out = {}
    for k in ("employed", "agency"):
        s = pw[pw.index.get_level_values(0).map(kind) == k]
        out[k] = (round(s.median(), 1), int(s.quantile(0.95)), int(s.max()))
    return out


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else W.SEED
    w = W.simulate(seed)
    m = measure(w)
    print(funnel(m).to_string(index=False))
    r = price(m, w)
    for k, v in r.items():
        if isinstance(v, float):
            print(f"{k:24s} {v:8.1f}")
        else:
            print(f"{k:24s} {v}")
    print("caseloads (median, p95, max sessions per therapist-week)", caseloads(w))
    print("agency therapists", int((w.prac.kind == "agency").sum()), "blocks", len(w.blocks))
