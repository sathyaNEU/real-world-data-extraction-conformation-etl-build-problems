"""Stage-2 pricing harness for task402 (never shipped): prices every rung on the clean truth."""
import sys
import numpy as np
import pandas as pd
from datetime import date
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
    out = out.join(tr[["step", "wait", "start", "agency0", "broken", "broken_kind", "broken_at", "left_list",
                       "modality", "cf_rec"]])
    out["finished"] = out.n_treat_att >= 2
    out["case"] = (out.phq_first >= 10) | (out.gad_first >= 8)
    out["fc"] = out.finished & out.case
    out["rec"] = out.fc & (out.phq_last <= 9) & (out.gad_last <= 7)
    out["fy"] = np.where((out.end >= W.FY25[0]) & (out.end <= W.FY25[1]), 25,
                         np.where((out.end >= W.FY24[0]) & (out.end <= W.FY24[1]), 24, 0))
    # practitioner of the discharge: the practitioner of the last contact of any kind
    lc = c.sort_values(["ref", "date", "cid"]).groupby("ref").last()
    out["disch_pid"] = lc["pid"]
    kind = dict(zip(w.prac.pid, w.prac.kind))
    out["disch_kind"] = out.disch_pid.map(kind)
    out["first_kind"] = out.first_pid.map(kind)
    return out


def funnel(m):
    rows = []
    for fy in (24, 25):
        for st in (2, 3):
            s = m[(m.fy == fy) & (m.step == st)]
            rows.append(dict(fy=fy, step=st, ended=len(s), entered=int((s.n_treat_att >= 1).sum()),
                             finished=int(s.finished.sum()), fc=int(s.fc.sum()), rec=int(s.rec.sum()),
                             rate=round(100 * s.rec.sum() / max(1, s.fc.sum()), 1)))
    return pd.DataFrame(rows)


def price(m, w):
    res = {}
    f25 = m[m.fy == 25]
    f24 = m[m.fy == 24]
    s3_25 = f25[f25.step == 3]
    s3_24 = f24[f24.step == 3]
    started25 = s3_25[s3_25.n_treat_att >= 1]
    # ---------- default path ----------
    # C: early endings by wait band among started courses, plus leaving the list
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
    # A by the discharging practitioner's kind (the clinician KPI: rate on finished courses at caseness)
    fc = s3_25[s3_25.fc]
    ra = fc[fc.disch_kind == "agency"].rec.mean()
    re_ = fc[fc.disch_kind == "employed"].rec.mean()
    res["A_kpi_rates"] = (round(100 * ra, 1), round(100 * re_, 1))
    res["A_default"] = max(0.0, (re_ - ra) * (fc.disch_kind == "agency").sum())
    # A by the first practitioner's kind, per started course (the coarse route)
    fa = started25[started25.first_kind == "agency"]
    fe = started25[started25.first_kind == "employed"]
    res["A_first_kind"] = len(fa) * (fe.rec.mean() - fa.rec.mean())
    res["first_kind_rates"] = (round(100 * fa.rec.mean(), 1), round(100 * fe.rec.mean(), 1), len(fa), len(fe))
    # cross tab wait band x first kind (per started course)
    xt = started25.assign(longw=started25.wait >= 18).groupby(["longw", "first_kind"]).rec.agg(["mean", "size"])
    res["xtab"] = xt
    # B: step 2 telephone against video and face to face, rate on finished at caseness
    s2 = f25[(f25.step == 2) & f25.fc]
    ph = s2[s2.modality == "phone"]
    vf = s2[s2.modality.isin(["video", "face_to_face"])]
    res["B"] = len(ph) * (vf.rec.mean() - ph.rec.mean())
    res["B_rates"] = (round(100 * ph.rec.mean(), 1), round(100 * vf.rec.mean(), 1), len(ph), len(vf))
    # B against 2024-25 telephone (same modality, before telephone-first)
    s2_24 = f24[(f24.step == 2) & f24.fc]
    ph24 = s2_24[s2_24.modality == "phone"]
    res["B_vs24"] = len(ph) * (ph24.rec.mean() - ph.rec.mean())
    # D: digital after the switch against digital in 2024-25
    dg = s2[(s2.modality == "digital")]
    dg24 = s2_24[s2_24.modality == "digital"]
    res["D"] = len(dg) * (dg24.rec.mean() - dg.rec.mean())
    # E: groups withdrawn: 2024-25 group rate against 2025-26 telephone, times courses that would have been groups
    gr24 = s2_24[s2_24.modality == "group"]
    n_div = int(round(len(f25[(f25.step == 2) & f25.fc]) * (len(gr24) / max(1, len(s2_24))))) - \
        int((s2.modality == "group").sum())
    res["E"] = max(0, n_div) * (gr24.rec.mean() - ph.rec.mean())
    # ---------- golden: the broken courses ----------
    br = started25[(started25.broken == True) & (started25.broken_kind == "agency")]
    ub = started25[started25.broken != True]
    res["broken_n"] = len(br)
    res["broken_rec"] = int(br.rec.sum())
    # landmark counterfactual: unbroken courses still in treatment after k attended sessions
    cf = 0.0
    for k, grp in br.groupby("broken_at"):
        base = ub[ub.n_treat_att >= max(1, k)]
        cf += len(grp) * base.rec.mean()
    res["A_landmark"] = cf - br.rec.sum()
    # pooled: unbroken started courses
    res["A_pooled"] = len(br) * ub.rec.mean() - br.rec.sum()
    # unbroken agency-first courses only
    ua = ub[ub.first_kind == "agency"]
    res["A_agency_unbroken"] = len(br) * ua.rec.mean() - br.rec.sum()
    # landmark in bands (1-2, 3-5, 6-8, 9+)
    cf2 = 0.0
    bands = pd.cut(br.broken_at, [-1, 2, 5, 8, 99])
    for b, grp in br.groupby(bands, observed=True):
        lo = int(b.left) + 1
        base = ub[ub.n_treat_att >= max(1, lo)]
        cf2 += len(grp) * base.rec.mean()
    res["A_landmark_band"] = cf2 - br.rec.sum()
    # long waiters held by a therapist who stayed against short waiters (the direct path)
    ubl = ub[ub.wait >= 18]
    ubs = ub[ub.wait < 18]
    res["direct_long_vs_short"] = (round(100 * ubl.rec.mean(), 1), round(100 * ubs.rec.mean(), 1), len(ubl), len(ubs))
    res["C_golden"] = c_left + len(ubl) * (ubs.rec.mean() - ubl.rec.mean())
    # share of the broken courses broken before a second treatment appointment
    res["broken_before2"] = int((br.broken_at < 2).sum())
    # employed-departure handovers in 2025-26
    res["broken_employed"] = int(((started25.broken == True) & (started25.broken_kind == "employed")).sum())
    # where the broken courses are discharged
    res["broken_disch_kind"] = br.disch_kind.value_counts().to_dict()
    # all handovers counted (agency and employed) with the landmark
    bra = started25[started25.broken == True]
    cf3 = 0.0
    for k, grp in bra.groupby("broken_at"):
        base = ub[ub.n_treat_att >= max(1, k)]
        cf3 += len(grp) * base.rec.mean()
    res["A_all_handovers"] = cf3 - bra.rec.sum()
    return res


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else W.SEED
    w = W.simulate(seed)
    m = measure(w)
    print(funnel(m).to_string(index=False))
    r = price(m, w)
    for k, v in r.items():
        if k == "xtab":
            print(v)
        elif isinstance(v, float):
            print(f"{k:24s} {v:8.1f}")
        else:
            print(f"{k:24s} {v}")
