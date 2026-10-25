"""The main call's records, as the PHN's extraction tool and the team's case log hold them: the active patient extract,
the smoking-status history, the practices and the 2025 Eastern Shore call log. Recording noise (ex-smokers entered as
never smoked, same-day re-entries and corrections) and the two clinical systems' vocabularies are applied here."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

import params as P
import world as W


def key(pid):
    return hashlib.sha1(("ct-phn-%d" % pid).encode()).hexdigest()[:12]


def system_on(pr, practice_id, d):
    row = pr.set_index("practice_id").loc[practice_id]
    if row.migrated and W.date_of(d) < dt.date.fromisoformat(row.migrated):
        return "MD"
    return row.system


def entries(pr, pat, rec, rng):
    """Every status entry the practices made: one row per entry, with its clinical system's wording."""
    rec = rec.copy()
    n = len(rec)
    obs = rec.true.values.copy()                      # 1 smoker, 0 ex-smoker, -1 never
    as_never = (obs == 0) & (rng.uniform(size=n) < P.EX_AS_NEVER)
    obs = np.where(as_never, -1, obs)
    rec["obs"] = obs
    # entry time within the consultation day
    rec["minute"] = rng.integers(8 * 60, 18 * 60, n)
    extra = []
    dup = rng.uniform(size=n) < P.DUP_SAMEDAY
    cor = rng.uniform(size=n) < P.CORRECT_SAMEDAY
    for j in np.flatnonzero(dup):
        r = rec.iloc[j]
        extra.append((r.pid, r.day, r.true, r.obs, min(18 * 60 + 30, r.minute + int(rng.integers(2, 40)))))
    for j in np.flatnonzero(cor):
        r = rec.iloc[j]
        wrong = int(rng.choice([v for v in (1, 0, -1) if v != r.obs]))
        extra.append((r.pid, r.day, r.true, wrong, max(8 * 60, r.minute - int(rng.integers(3, 25)))))
    if extra:
        rec = pd.concat([rec, pd.DataFrame(extra, columns=["pid", "day", "true", "obs", "minute"])], ignore_index=True)
    rec = rec.sort_values(["pid", "day", "minute"], kind="stable").reset_index(drop=True)
    # wording by the practice's clinical system on the day; Best Practice's smoker detail held per patient
    prac = pat.practice_id.values[rec.pid.values]
    detail = rng.choice(3, len(pat), p=P.BP_DETAIL)
    flip = rng.uniform(size=len(rec)) < 0.10
    other = rng.choice(3, len(rec), p=P.BP_DETAIL)
    words = []
    prs = pr.set_index("practice_id")
    mig = {p: dt.date.fromisoformat(m) for p, m in prs.migrated.items() if m}
    sysof = prs.system.to_dict()
    for j in range(len(rec)):
        p = prac[j]
        s = sysof[p]
        if p in mig and W.date_of(rec.day.values[j]) < mig[p]:
            s = "MD"
        o = rec.obs.values[j]
        v = P.VOCAB[s]
        if o == 1:
            d = other[j] if flip[j] else detail[rec.pid.values[j]]
            words.append(v["S"][d] if s == "BP" else v["S"][0])
        elif o == 0:
            words.append(v["E"])
        else:
            words.append(v["N"])
    rec["status"] = words
    rec["system"] = None
    return rec


def build(rng=None):
    rng = np.random.default_rng(P.SEED_PILOT)
    pr, pat, sw, rec = W.simulate()
    ent = entries(pr, pat, rec, rng)
    # active at the extract: everyone but the Eastern Shore leavers, and in each candidate sub-region the patients with
    # no status ever recorded whom the practices archived in their 2026 list cleanse
    active = pat.leave.values > W.E_DAY
    blank = ~np.isin(pat.pid.values, ent.pid.values)
    rng_c = np.random.default_rng(P.SEED_WORLD + 11)
    for g in P.CAND:
        idx = np.flatnonzero((pat.reg.values == g) & blank & active)
        active[rng_c.choice(idx, int(rng_c.integers(140, 960)), replace=False)] = False
    keys = np.array([key(p) for p in pat.pid])
    # first seen at the practice
    fs = np.where(pat.reg_day.values > 0, pat.reg_day.values,
                  -rng.integers(1, 17 * 365, len(pat)))
    last = ent.groupby("pid").tail(1).set_index("pid")
    ab = lambda a: ("%d-%d" % (int(a // 5 * 5), int(a // 5 * 5 + 4))) if a < 85 else "85+"
    ext = pd.DataFrame({
        "patient_key": keys, "practice_id": pat.practice_id.values,
        "sub_region": [P.NAME[g] for g in pat.reg.values],
        "age_band": [ab(a) for a in pat.age.values], "sex": pat.sex.values,
        "first_seen": [W.date_of(d).isoformat() for d in fs],
        "chronic_condition_review": np.where(pat.ltc.values, "Y", "N")})
    ext["smoking_status"] = [last.status[p] if p in last.index else "" for p in pat.pid]
    ext["smoking_status_date"] = [W.date_of(last.day[p]).isoformat() if p in last.index else "" for p in pat.pid]
    ext = ext[active].sort_values(["practice_id", "patient_key"]).reset_index(drop=True)
    hist = ent[active[ent.pid.values]].copy()
    hist = pd.DataFrame({
        "patient_key": keys[hist.pid.values], "practice_id": pat.practice_id.values[hist.pid.values],
        "recorded_at": [(dt.datetime.combine(W.date_of(d), dt.time(m // 60, m % 60))).strftime("%Y-%m-%d %H:%M")
                        for d, m in zip(hist.day.values, hist.minute.values)],
        "smoking_status": hist.status.values})
    prt = pr.copy()
    prt["sub_region"] = [P.NAME[g] for g in prt.reg]
    prt["clinical_system"] = [P.SYSTEMS[s] for s in prt.system]
    prt["previous_system"] = [P.SYSTEMS["MD"] if m else "" for m in prt.migrated]
    prt["system_changed"] = [m or "" for m in prt.migrated]
    prt["active_patients_18_plus"] = prt.practice_id.map(ext.practice_id.value_counts()).fillna(0).astype(int)
    prt = prt[["practice_id", "sub_region", "clinical_system", "previous_system", "system_changed",
               "active_patients_18_plus"]]
    return dict(pr=pr, pat=pat, sw=sw, rec=rec, ent=ent, ext=ext, hist=hist, practices=prt, keys=keys)


SMOKER_WORDS = {"Daily smoker", "Weekly smoker", "Irregular smoker", "Smoker"}


def pilot(R, rng=None):
    """The 2025 Eastern Shore list (current smokers at 31 January 2025 on the January roll) and the team's calls."""
    rng = np.random.default_rng(P.SEED_PILOT + 7)
    pat, sw, ent = R["pat"], R["sw"], R["ent"]
    e = ent[(pat.reg.values[ent.pid.values] == "P") & (ent.day.values <= W.L_DAY)]
    lastp = e.groupby("pid").tail(1)
    lst = lastp[lastp.status.isin(SMOKER_WORDS)].copy()
    n = len(lst)
    # working days of the calling year, spread evenly, in list order by practice
    wd = pd.bdate_range(P.PILOT_CALLS[0], P.PILOT_CALLS[1])
    wd = wd[~wd.isin(pd.to_datetime(P.HOLIDAYS_2025))]
    lst = lst.sample(frac=1.0, random_state=int(rng.integers(1, 10 ** 6))).reset_index(drop=True)
    call_day = np.array([W.day(d.date()) for d in wd[np.floor(np.arange(n) * len(wd) / n).astype(int)]])
    still = W.true_state(pat, sw, lst.pid.values, call_day) == 1
    reached = rng.uniform(size=n) < P.REACH
    attempts = np.where(reached, rng.choice([1, 2, 3], n, p=[0.55, 0.30, 0.15]), 3)
    qd = reached & still & (rng.uniform(size=n) < P.QUIT_DATE)
    qdate = call_day + rng.integers(0, 15, n)
    # four weeks after a quit date: abstinence follows the team's support, not the background process
    abst = qd & (rng.uniform(size=n) < P.ABSTAIN)
    ltfu = qd & ~abst & (rng.uniform(size=n) < P.LTFU)
    outcome = np.where(~reached, "Not reached", np.where(~still, "Not a current smoker",
                       np.where(qd, "Quit date set", "Declined support")))
    four = np.where(qd, np.where(abst, "Not smoking", np.where(ltfu, "Lost to follow-up", "Smoking")), "")
    log = pd.DataFrame({
        "patient_key": R["keys"][lst.pid.values],
        "practice_id": pat.practice_id.values[lst.pid.values],
        "list_status": lst.status.values,
        "list_status_date": [W.date_of(d).isoformat() for d in lst.day.values],
        "call_date": [W.date_of(d).isoformat() for d in call_day],
        "attempts": attempts, "outcome": outcome,
        "quit_date": [W.date_of(d).isoformat() if q else "" for d, q in zip(qdate, qd)],
        "four_week_status": four})
    log = log.sort_values(["call_date", "practice_id", "patient_key"]).reset_index(drop=True)
    return log, lst.pid.values, call_day, still, reached, qd, abst
