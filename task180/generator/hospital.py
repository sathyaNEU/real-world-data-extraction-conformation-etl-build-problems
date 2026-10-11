"""Turn the simulated world into hospital contacts and diagnoses as the patient registry records them.

From 4 February 2019 (LPR3) every stay at a department is a contact with a start and an end to the minute, a
priority (acute or planned) and a contact type (physical or virtual); a patient who moves from the emergency
department to a ward, or between wards, gets one contact per department. Before that date (LPR2) inpatient
stays and emergency room visits are records with an admission date and hour and a discharge date, and
outpatient care is one record per course spanning all its visits. Times are minutes from 1 January 2018."""
import numpy as np

import sim as S
import world as W

MIN_DAY = 1440


def _hours(r, n, lo=7, hi=23):
    """Arrival minute of day: mostly daytime and evening."""
    h = np.clip(r.normal(14.5, 4.0, n), lo, hi - 0.01)
    return np.floor(h * 60).astype(np.int64)


class Builder:
    def __init__(self, P):
        self.P = P
        self.cols = {k: [] for k in ("pid", "start", "end", "dept", "prio", "ctype", "group", "stay")}
        self.next_stay = 0
        self.dx = {k: [] for k in ("cid", "code", "type")}
        self.n = 0
        r = W.rng("hospital", "home")
        hosp = []
        for reg, w in zip(W.REGIONS, W.REGION_W):
            hosp += [(h, w / len(W.HOSPITALS[reg])) for h in W.HOSPITALS[reg]]
        p = np.array([x[1] for x in hosp])
        self.hosp_codes = np.array([x[0] for x in hosp])
        self.home = r.choice(len(hosp), size=len(P["cohort"]), p=p / p.sum())

    def stays(self, n):
        out = np.arange(self.next_stay, self.next_stay + n)
        self.next_stay += n
        return out

    def add(self, pid, start, end, specialty, prio, ctype, group, stay=None):
        """Vectorised: one contact per element; returns the contact ids. stay: the hospital stay each contact
        belongs to (contacts of one stay are linked by transfer); a new stay per contact when None."""
        n = len(pid)
        self.cols["stay"].append(self.stays(n) if stay is None else np.asarray(stay, np.int64))
        ids = np.arange(self.n, self.n + n)
        self.n += n
        dept = np.array([int(W.SPECIALTY_DEPT[s]) for s in np.broadcast_to(specialty, (n,))], np.int64) \
            if not np.isscalar(specialty) else np.full(n, int(W.SPECIALTY_DEPT[specialty]), np.int64)
        shak = self.hosp_codes[self.home[pid]].astype(np.int64) * 1000 + dept
        self.cols["pid"].append(np.asarray(pid, np.int64))
        self.cols["start"].append(np.asarray(start, np.int64))
        self.cols["end"].append(np.asarray(end, np.int64))
        self.cols["dept"].append(shak)
        self.cols["prio"].append(np.broadcast_to(np.asarray(prio, np.int8), (n,)).copy())
        self.cols["ctype"].append(np.broadcast_to(np.asarray(ctype, np.int8), (n,)).copy())
        self.cols["group"].append(np.full(n, group, np.int8))
        return ids

    def diag(self, cid, codes, dtype):
        cid = np.asarray(cid, np.int64)
        codes = np.broadcast_to(np.asarray(codes, object), cid.shape)
        self.dx["cid"].append(cid)
        self.dx["code"].append(np.asarray(codes, object))
        self.dx["type"].append(np.full(len(cid), dtype, object))

    def done(self, death_min):
        C = {k: np.concatenate(v) for k, v in self.cols.items()}
        D = {k: np.concatenate(v) for k, v in self.dx.items()}
        keep = separate_stays(C, death_min)
        # no contact starts after the extract's last day, at or after death, or while the person is abroad
        dead, away, back = OUT[0]
        pid, st = C["pid"], C["start"]
        keep &= (st < (W.D_END + 1) * MIN_DAY) & (st < death_min[pid]) & ~((st >= away[pid]) & (st < back[pid]))
        # a stay whose contacts would fall on both sides of the change of record structure (4 February 2019) is left out
        sw = W.D_LPR3 * MIN_DAY
        u, inv = np.unique(C["stay"], return_inverse=True)
        first = np.full(len(u), np.iinfo(np.int64).max)
        last = np.full(len(u), np.iinfo(np.int64).min)
        np.minimum.at(first, inv[keep], st[keep])
        np.maximum.at(last, inv[keep], st[keep])
        keep &= ~((first < sw) & (last >= sw))[inv]
        newid = np.cumsum(keep) - 1
        C = {k: v[keep] for k, v in C.items()}
        dk = keep[D["cid"]]
        D = {k: v[dk] for k, v in D.items()}
        D["cid"] = newid[D["cid"]]
        return C, D


OUT = [None]   # per person, in minutes: the day of death, the day of emigration and the day of return
GROUP = {"fall": 1, "aki": 2, "pancreatitis": 3, "acute": 4, "injury": 5, "condition": 6, "outpatient": 7,
         "followup": 8}
EVENT_GROUPS = (1, 2, 3)
GAP = 48 * 60


def stay_spans(C):
    sid = C["stay"]
    u, inv = np.unique(sid, return_inverse=True)
    lo = np.full(len(u), np.iinfo(np.int64).max)
    hi = np.full(len(u), np.iinfo(np.int64).min)
    np.minimum.at(lo, inv, C["start"])
    np.maximum.at(hi, inv, C["end"])
    pid = np.zeros(len(u), np.int64)
    pid[inv] = C["pid"]
    ev = np.zeros(len(u), bool)
    np.logical_or.at(ev, inv, np.isin(C["group"], EVENT_GROUPS))
    fu = np.zeros(len(u), bool)
    np.logical_or.at(fu, inv, C["group"] == GROUP["followup"])
    acute = np.zeros(len(u), bool)
    np.logical_or.at(acute, inv, C["prio"] == 1)
    return u, inv, pid, lo, hi, ev, fu, acute


def _near(pid_a, lo_a, hi_a, pid_b, lo_b, hi_b):
    """For each span a: is any span b of the same person within GAP minutes of it (or overlapping)?"""
    order = np.lexsort((lo_b, pid_b))
    pb, lb, hb = pid_b[order], lo_b[order], hi_b[order]
    key_b = pb * 10 ** 10 + lb
    # the last b starting at or before a's end plus GAP, scanned back over a few neighbours
    pos = np.searchsorted(key_b, pid_a * 10 ** 10 + hi_a + GAP, side="right") - 1
    near = np.zeros(len(pid_a), bool)
    for back in range(0, 6):
        j = pos - back
        ok = j >= 0
        jj = np.where(ok, j, 0)
        same = ok & (pb[jj] == pid_a)
        near |= same & (hb[jj] + GAP >= lo_a) & (lb[jj] <= hi_a + GAP)
    return near


def separate_stays(C, death_min):
    """Hospital stays of one person never sit within 48 hours of each other unless linked by transfer: an event stay
    that would is moved three days later, a follow-up visit that would is dropped, and background contacts that would
    are dropped. So linking contacts within 1, 4, 12, 24 or 48 hours gives the same admissions and the same events."""
    for _ in range(6):
        u, inv, pid, lo, hi, ev, fu, acute = stay_spans(C)
        e = np.where(ev)[0]
        o = e[np.lexsort((lo[e], pid[e]))]
        clash = np.r_[False, (pid[o][1:] == pid[o][:-1]) & (lo[o][1:] - hi[o][:-1] < GAP)]
        if not clash.any():
            break
        move = np.zeros(len(u), bool)
        move[o[clash]] = True
        shift = np.where(move[inv], 3 * 1440, 0)
        C["start"] = C["start"] + shift
        C["end"] = C["end"] + shift
    # a clash left after those rounds (a chain of moves, or a long stay behind a short one) is settled against the
    # latest end of every earlier event stay of the same person
    for _ in range(60):
        u, inv, pid, lo, hi, ev, fu, acute = stay_spans(C)
        e = np.where(ev)[0]
        o = e[np.lexsort((lo[e], pid[e]))]
        po = pid[o].astype(np.int64)
        latest = np.maximum.accumulate(po * 10 ** 9 + hi[o]) - po * 10 ** 9
        clash = np.r_[False, (po[1:] == po[:-1]) & (lo[o][1:] - latest[:-1] < GAP)]
        if not clash.any():
            break
        move = np.zeros(len(u), bool)
        move[o[clash]] = True
        shift = np.where(move[inv], 3 * 1440, 0)
        C["start"] = C["start"] + shift
        C["end"] = C["end"] + shift
    u, inv, pid, lo, hi, ev, fu, acute = stay_spans(C)
    keep_stay = np.ones(len(u), bool)
    dead, away, back = OUT[0]
    out = (lo >= dead[pid]) | ((lo >= away[pid]) & (lo < back[pid])) | (lo >= (W.D_END + 1) * MIN_DAY)
    keep_stay &= ~out
    # follow-up visits: kept unless within 48 hours of an event stay or of an earlier follow-up
    e = np.where(ev & keep_stay)[0]
    f = np.where(fu)[0]
    keep_stay[f[_near(pid[f], lo[f], hi[f], pid[e], lo[e], hi[e])]] = False
    f = np.where(fu & keep_stay)[0]
    o = f[np.lexsort((lo[f], pid[f]))]
    for _ in range(6):
        clash = np.r_[False, (pid[o][1:] == pid[o][:-1]) & (lo[o][1:] - hi[o][:-1] < GAP)]
        if not clash.any():
            break
        keep_stay[o[clash]] = False
        o = o[~clash]
    prot = np.where((ev | fu) & keep_stay)[0]
    other = np.where(~ev & ~fu)[0]
    keep_stay[other[_near(pid[other], lo[other], hi[other], pid[prot], lo[prot], hi[prot])]] = False
    # background acute stays: the later of two within 48 hours goes
    ba = np.where(~ev & ~fu & acute & keep_stay)[0]
    o = ba[np.lexsort((lo[ba], pid[ba]))]
    for _ in range(6):
        clash = np.r_[False, (pid[o][1:] == pid[o][:-1]) & (lo[o][1:] - hi[o][:-1] < GAP)]
        if not clash.any():
            break
        keep_stay[o[clash]] = False
        o = o[~clash]
    # planned contacts within 48 hours of a kept acute stay go
    ka = np.where(acute & keep_stay)[0]
    pl = np.where(~acute & ~fu & keep_stay)[0]
    keep_stay[pl[_near(pid[pl], lo[pl], hi[pl], pid[ka], lo[ka], hi[ka])]] = False
    return keep_stay[inv]


def recorded_secondaries(B, P, r, pid, day, cid, kmax=2, exclude=None):
    """Secondary diagnoses: up to kmax of the person's conditions already on record by that day."""
    rec = P["rec"][pid]
    onfile = rec <= day[:, None]
    if exclude is not None:
        onfile[:, exclude] = False
    score = np.where(onfile, r.random(onfile.shape), -1.0)
    order = np.argsort(-score, axis=1)[:, :kmax]
    for j in range(kmax):
        c = order[:, j]
        ok = score[np.arange(len(pid)), c] > 0.35
        if not ok.any():
            continue
        codes = np.array([W.CONDITIONS[W.COND_NAMES[k]][3][0] for k in c[ok]], object)
        B.diag(cid[ok], codes, "B")


def pick(r, codes, weights, n):
    w = np.asarray(weights, float)
    return np.array(codes, object)[r.choice(len(codes), size=n, p=w / w.sum())]


def build(world):
    P, ev = world["P"], world["ev"]
    B = Builder(P)
    death_min = np.where(P["death"] < 10 ** 7, P["death"] * MIN_DAY + 12 * 60, 10 ** 12)
    # no stay may start on the day of death or later, or while the person is abroad
    OUT[0] = (np.minimum(P["death"], 10 ** 7) * MIN_DAY, np.minimum(P["emig"], 10 ** 7) * MIN_DAY,
              np.minimum(P["ret"], 10 ** 7) * MIN_DAY)

    def clip_end(pid, end):
        return np.minimum(end, death_min[pid])

    # ---------------- falls: an emergency contact, a third admitted to a ward (some moved on to geriatrics)
    r = W.rng("hospital", "fall")
    pid, d = ev["fall"]
    n = len(pid)
    t0 = d * MIN_DAY + _hours(r, n)
    ed_end = t0 + r.integers(120, 420, n)
    inj = pick(r, W.FALL_INJURY, W.FALL_INJURY_W, n)
    fcode = pick(r, W.FALL_CODES, W.FALL_CODES_W, n)
    st = B.stays(n)
    ed = B.add(pid, t0, clip_end(pid, ed_end), "Akutmedicin", 1, 0, GROUP["fall"], st)
    B.diag(ed, inj, "A")
    has_w = r.random(n) < 0.95
    B.diag(ed[has_w], fcode[has_w], "B")
    recorded_secondaries(B, P, r, pid, d, ed, kmax=1)
    adm = r.random(n) < np.where(np.isin(inj, ["DS720", "DS721", "DS324", "DS220"]), 0.92, 0.18)
    a_pid, a_t, a_inj, a_f, a_d, a_st = pid[adm], ed_end[adm], inj[adm], fcode[adm], d[adm], st[adm]
    na = len(a_pid)
    w_start = a_t + r.integers(0, 45, na)
    w_end = w_start + (np.exp(r.normal(np.log(4.5 * MIN_DAY), 0.55, na))).astype(np.int64)
    spec = np.where(r.random(na) < 0.78, "Ortopædisk kirurgi", "Geriatri")
    wd = B.add(a_pid, w_start, clip_end(a_pid, w_end), spec, 1, 0, GROUP["fall"], a_st)
    B.diag(wd, a_inj, "A")
    keepf = r.random(na) < 0.55
    B.diag(wd[keepf], a_f[keepf], "B")
    recorded_secondaries(B, P, r, a_pid, a_d, wd, kmax=2)
    sec = (spec == "Ortopædisk kirurgi") & (r.random(na) < 0.12)
    s2 = w_end[sec] + r.integers(0, 40, sec.sum())
    e2 = s2 + (np.exp(r.normal(np.log(6 * MIN_DAY), 0.5, sec.sum()))).astype(np.int64)
    g2 = B.add(a_pid[sec], s2, clip_end(a_pid[sec], e2), "Geriatri", 1, 0, GROUP["fall"], a_st[sec])
    B.diag(g2, a_inj[sec], "A")
    # fracture clinic follow-up, planned
    fu = r.random(na) < 0.5
    k = np.where(fu, r.integers(1, 3, na), 0)
    rep = np.repeat(np.arange(na), k)
    fday = (w_end[rep] // MIN_DAY) + r.integers(14, 60, len(rep))
    ft = fday * MIN_DAY + _hours(r, len(rep), 8, 15)
    fid = B.add(a_pid[rep], ft, ft + r.integers(15, 45, len(rep)), "Ortopædisk kirurgi", 3, 0, GROUP["followup"])
    B.diag(fid, a_inj[rep], "A")
    wf = r.random(len(rep)) < 0.4
    B.diag(fid[wf], a_f[rep][wf], "B")

    # ---------------- acute kidney injury: most through the emergency department, some straight to a ward
    r = W.rng("hospital", "aki")
    pid, d = ev["aki"]
    n = len(pid)
    t0 = d * MIN_DAY + _hours(r, n)
    via_ed = r.random(n) < 0.66
    aki = pick(r, W.AKI_CODES, W.AKI_CODES_W, n)
    ed_end = t0 + r.integers(180, 840, n)
    st = B.stays(n)
    e_ids = B.add(pid[via_ed], t0[via_ed], clip_end(pid[via_ed], ed_end[via_ed]), "Akutmedicin", 1, 0, GROUP["aki"],
                  st[via_ed])
    ed_code = np.where(r.random(via_ed.sum()) < 0.5, aki[via_ed],
                       pick(r, ["DE869", "DR539", "DR410", "DR509"], [0.5, 0.25, 0.15, 0.1], via_ed.sum()))
    B.diag(e_ids, ed_code, "A")
    recorded_secondaries(B, P, r, pid[via_ed], d[via_ed], e_ids, kmax=1)
    w_start = np.where(via_ed, ed_end + r.integers(0, 50, n), t0)
    w_end = w_start + (np.exp(r.normal(np.log(5.5 * MIN_DAY), 0.5, n))).astype(np.int64)
    spec = np.where(r.random(n) < 0.68, "Intern medicin", "Nefrologi")
    w_ids = B.add(pid, w_start, clip_end(pid, w_end), spec, 1, 0, GROUP["aki"], st)
    B.diag(w_ids, aki, "A")
    hk = r.random(n) < 0.22
    B.diag(w_ids[hk], "DE875", "B")
    recorded_secondaries(B, P, r, pid, d, w_ids, kmax=2)
    sec = (spec == "Intern medicin") & (r.random(n) < 0.2)
    s2 = w_end[sec] + r.integers(0, 40, sec.sum())
    e2 = s2 + (np.exp(r.normal(np.log(4 * MIN_DAY), 0.5, sec.sum()))).astype(np.int64)
    n_ids = B.add(pid[sec], s2, clip_end(pid[sec], e2), "Nefrologi", 1, 0, GROUP["aki"], st[sec])
    B.diag(n_ids, aki[sec], "A")
    # nephrology outpatient follow-up after discharge, planned, the kidney injury as its action diagnosis
    fu = r.random(n) < 0.33
    fday = (w_end[fu] // MIN_DAY) + r.integers(21, 57, fu.sum())
    ft = fday * MIN_DAY + _hours(r, fu.sum(), 8, 15)
    f_ids = B.add(pid[fu], ft, ft + r.integers(20, 50, fu.sum()), "Nefrologi", 3, 0, GROUP["followup"])
    B.diag(f_ids, aki[fu], "A")

    # ---------------- acute pancreatitis
    r = W.rng("hospital", "pancreatitis")
    pid, d = ev["pancreatitis"]
    n = len(pid)
    t0 = d * MIN_DAY + _hours(r, n)
    via_ed = r.random(n) < 0.75
    pc = pick(r, W.PANC_CODES, W.PANC_CODES_W, n)
    gall = P["present"][pid, W.COND_NAMES.index("gallstones")]
    alc = P["present"][pid, W.COND_NAMES.index("alcohol")]
    pc = np.where(gall & (r.random(n) < 0.8), "DK851", np.where(alc & (r.random(n) < 0.8), "DK852", pc))
    ed_end = t0 + r.integers(240, 720, n)
    st = B.stays(n)
    e_ids = B.add(pid[via_ed], t0[via_ed], clip_end(pid[via_ed], ed_end[via_ed]), "Akutmedicin", 1, 0,
                  GROUP["pancreatitis"], st[via_ed])
    B.diag(e_ids, np.where(r.random(via_ed.sum()) < 0.4, pc[via_ed], "DR101"), "A")
    w_start = np.where(via_ed, ed_end + r.integers(0, 50, n), t0)
    w_end = w_start + (np.exp(r.normal(np.log(5 * MIN_DAY), 0.5, n))).astype(np.int64)
    w_ids = B.add(pid, w_start, clip_end(pid, w_end), "Mave- og tarmkirurgi", 1, 0, GROUP["pancreatitis"], st)
    B.diag(w_ids, pc, "A")
    B.diag(w_ids[gall], "DK802", "B")
    B.diag(w_ids[alc & ~gall], "DF102", "B")

    # ---------------- every person's other hospital life
    nP = len(P["cohort"])
    lo = P["entry"].astype(np.int64)
    hi = np.full(nP, W.D_END + 1, np.int64)
    npres = P["present"].sum(axis=1)
    age22 = S.age_at(P, W.day(W.dt.date(2022, 6, 30)))
    # background acute admissions
    r = W.rng("hospital", "acute")
    rate = 0.028 * np.exp(0.04 * (age22 - 60)) * (1 + 0.3 * npres)
    pid, d = _process(r, lo, hi, rate)
    pid, d = S.resident(P, pid, d)
    n = len(pid)
    t0 = d * MIN_DAY + _hours(r, n)
    kind = r.random(n)
    ed_only = kind < 0.33
    direct = kind > 0.8
    via_ed = ~direct
    code = pick(r, [c for c, _ in W.ACUTE_POOL], W.ACUTE_POOL_W, n)
    spec = np.array([dict(W.ACUTE_POOL)[c] for c in code], object)
    chf = P["present"][pid, W.COND_NAMES.index("chf")] & (r.random(n) < 0.3)
    copd = P["present"][pid, W.COND_NAMES.index("copd")] & (r.random(n) < 0.3)
    code = np.where(chf, "DI500", np.where(copd, "DJ441", code))
    spec = np.where(chf, "Kardiologi", np.where(copd, "Lungemedicin", spec))
    ed_end = t0 + r.integers(150, 600, n)
    st = B.stays(n)
    e_ids = B.add(pid[via_ed], t0[via_ed], clip_end(pid[via_ed], ed_end[via_ed]), "Akutmedicin", 1, 0,
                  GROUP["acute"], st[via_ed])
    B.diag(e_ids, code[via_ed], "A")
    recorded_secondaries(B, P, r, pid[via_ed], d[via_ed], e_ids, kmax=1)
    # a fall code on some syncope and dizziness stays: the fall is not the injury
    fallish = via_ed & np.isin(code, ["DR559", "DE869"]) & (age22[pid] > 65) & (r.random(n) < 0.12)
    B.diag(e_ids[fallish[via_ed]], pick(r, W.FALL_CODES, W.FALL_CODES_W, fallish.sum()), "B")
    ward = ~ed_only
    w_start = np.where(via_ed, ed_end + r.integers(0, 50, n), t0)[ward]
    w_end = w_start + (np.exp(r.normal(np.log(4 * MIN_DAY), 0.6, ward.sum()))).astype(np.int64)
    wp = pid[ward]
    w_ids = B.add(wp, w_start, clip_end(wp, w_end), spec[ward], 1, 0, GROUP["acute"], st[ward])
    B.diag(w_ids, code[ward], "A")
    recorded_secondaries(B, P, r, wp, d[ward], w_ids, kmax=3)
    # kidney injury arising during another illness: a secondary diagnosis, not the reason for the stay
    age_w = S.age_at({"birth_day": P["birth_day"][wp]}, d[ward])
    p_sec = np.minimum(0.35, 0.12 * P["mult_aki"][wp] * W.base_rate("aki", age_w, P["female"][wp]) /
                       W.base_rate("aki", 70.0, True))
    hit = r.random(len(wp)) < p_sec
    B.diag(w_ids[hit], pick(r, W.AKI_CODES, W.AKI_CODES_W, hit.sum()), "B")
    # injuries that were not falls
    r = W.rng("hospital", "injury")
    rate = np.where(age22 < 40, 0.03, 0.014) * np.ones(nP)
    pid, d = _process(r, lo, hi, rate)
    pid, d = S.resident(P, pid, d)
    n = len(pid)
    t0 = d * MIN_DAY + _hours(r, n)
    ids = B.add(pid, t0, clip_end(pid, t0 + r.integers(90, 300, n)), "Akutmedicin", 1, 0, GROUP["injury"])
    B.diag(ids, pick(r, ["DS610", "DS934", "DS525", "DS800", "DS010", "DT140", "DS635"],
                     [0.25, 0.2, 0.1, 0.15, 0.1, 0.1, 0.1], n), "A")
    B.diag(ids, pick(r, W.OTHER_INJURY_CAUSE, [0.4, 0.3, 0.15, 0.15], n), "B")
    # conditions: the first record and follow-up visits at the condition's clinic
    r = W.rng("hospital", "conditions")
    pp, cc = np.nonzero(P["present"])
    recd = P["rec"][pp, cc]
    first_ok = (recd >= lo[pp]) & (recd <= W.D_END)
    fpid, fday, fcond = pp[first_ok], np.floor(recd[first_ok]).astype(np.int64), cc[first_ok]
    fu_lo = np.maximum(np.ceil(recd), lo[pp]).astype(np.int64)
    span = np.maximum(0, W.D_END + 1 - fu_lo)
    k = r.poisson(0.2 * span / S.YEAR)
    rep = np.repeat(np.arange(len(pp)), k)
    upid = np.r_[fpid, pp[rep]]
    uday = np.r_[fday, fu_lo[rep] + np.floor(r.random(len(rep)) * span[rep]).astype(np.int64)]
    ucond = np.r_[fcond, cc[rep]]
    keep = S.resident_mask(P, upid, uday)
    upid, uday, ucond = upid[keep], uday[keep], ucond[keep]
    n = len(upid)
    t0 = uday * MIN_DAY + _hours(r, n, 8, 16)
    virt = r.random(n) < 0.14
    spec = np.array([W.CONDITIONS[W.COND_NAMES[c]][4] for c in ucond], object)
    ids = B.add(upid, t0, t0 + r.integers(15, 75, n), spec, 3, np.where(virt, 1, 0), GROUP["condition"])
    codes = np.array([W.CONDITIONS[W.COND_NAMES[c]][3][int(x * len(W.CONDITIONS[W.COND_NAMES[c]][3]))]
                      for c, x in zip(ucond, r.random(n))], object)
    B.diag(ids, codes, "A")
    recorded_secondaries(B, P, r, upid, uday, ids, kmax=1)
    # general outpatient visits
    r = W.rng("hospital", "outpatient")
    rate = 0.2 * np.exp(0.02 * (age22 - 60))
    pid, d = _process(r, lo, hi, rate)
    pid, d = S.resident(P, pid, d)
    n = len(pid)
    t0 = d * MIN_DAY + _hours(r, n, 8, 16)
    code = pick(r, [c for c, _ in W.OUTPATIENT_POOL], W.OUTPATIENT_POOL_W, n)
    spec = np.array([dict(W.OUTPATIENT_POOL)[c] for c in code], object)
    ids = B.add(pid, t0, t0 + r.integers(15, 60, n), spec, 3, np.where(r.random(n) < 0.12, 1, 0), GROUP["outpatient"])
    B.diag(ids, code, "A")
    C, D = B.done(death_min)
    return C, D, B.hosp_codes


def _process(r, lo, hi, rate):
    span = np.maximum(0, hi - lo)
    k = r.poisson(rate * span / S.YEAR)
    pid = np.repeat(np.arange(len(lo)), k)
    d = lo[pid] + np.floor(r.random(len(pid)) * span[pid]).astype(np.int64)
    return pid, d
