"""Every student-level record the pack ships, built from the world: the platform's eligibility file, the roster
uploads in each state's own codes, the student crosswalk, the assessment delivery system's sessions and scored
responses, and the contractor's plausible values (fitted here exactly as the technical report describes)."""
import datetime as dt

import numpy as np

import world as W
import irt

# the districts' clocks in the testing window (daylight time); Arizona keeps standard time
UTC_OFFSET = {"NC": -4, "OH": -4, "GA": -4, "TN": -5, "CO": -6, "AZ": -7}
RE_ROSTERED = (17, 44)              # district positions whose student information system changed in January 2026
SPRING_UPLOAD = dt.date(2026, 2, 13)
FALL_UPLOAD = dt.date(2025, 9, 15)
APRIL_UPLOAD = dt.date(2026, 4, 10)
WINDOW = (dt.date(2026, 4, 13), dt.date(2026, 5, 22))

# each state's prior-test performance levels by band (Table 5 of the technical report), and its roster codes
LEVELS = {
    "NC": ("EOG", [["Not Proficient"], ["Level 3"], ["Level 4"], ["Level 5"]]),
    "OH": ("OST", [["Limited"], ["Basic"], ["Proficient"], ["Accomplished", "Advanced"]]),
    "GA": ("Georgia Milestones", [["Beginning Learner"], ["Developing Learner"], ["Proficient Learner"],
                                  ["Distinguished Learner"]]),
    "TN": ("TCAP", [["Below"], ["Approaching"], ["Met Expectations"], ["Exceeded Expectations"]]),
    "CO": ("CMAS", [["Did Not Yet Meet", "Partially Met"], ["Approached"], ["Met"], ["Exceeded"]]),
    "AZ": ("AASA", [["Minimally Proficient"], ["Partially Proficient"], ["Proficient"], ["Highly Proficient"]]),
}
CODES = {   # (economic disadvantage yes, no), (English learner yes, no), (disability yes, no)
    "NC": (("EDS", ""), ("LEP", ""), ("EC", "")),
    "OH": (("Y", "N"), ("L", ""), ("Y", "N")),
    "GA": (("F", "N"), ("Y", "N"), ("Y", "N")),
    "TN": (("ED", ""), ("EL", ""), ("Y", "")),
    "CO": (("Free", "Not Eligible"), ("NEP", ""), ("IEP", "")),
    "AZ": (("1", "0"), ("1", "0"), ("SPED", "")),
}


def _when(day, hour, minute, off):
    """A local clock time on a date as an ISO 8601 UTC stamp."""
    t = dt.datetime(day.year, day.month, day.day, hour, minute) - dt.timedelta(hours=off)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def build():
    """Students of the 58 districts with their records, and the shipped tables."""
    r0 = np.random.default_rng(W.SEED + 11)
    n_all = sum(int(W.POOL["rostered"][dd["pool"]]) for dd in W.DISTRICTS)
    sid_pool = r0.permutation(np.arange(4100000, 4100000 + 3 * n_all))
    tt_pool = r0.permutation(np.arange(100000, 100000 + 4 * n_all))
    sess_pool = r0.permutation(np.arange(7000000, 7000000 + 3 * n_all))
    take = {"sid": 0, "tt": 0, "sess": 0}

    def nxt(k, pool):
        v = int(pool[take[k]]); take[k] += 1
        return v

    by_state = {}
    for dd in W.DISTRICTS:
        by_state.setdefault(dd["state"], []).append(dd["j"])
    parts = []
    elig_rows, roster_rows, xwalk_rows, sess_rows, resp_rows = [], [], [], [], []
    item_id = {(m, k): "LS%d%02d" % (m + 1, 11 + 7 * k + m) for m in range(W.N_MOD) for k in range(W.N_ITEM)}
    for dd in W.DISTRICTS:
        j, d, st = dd["j"], dd["pool"], dd["state"]
        s = W.students(d)
        y, mods = W.responses(s)
        r = np.random.default_rng(W.SEED * 100 + d)
        n = len(s["g"])
        elig, tested = s["eligible"].astype(bool), s["tested"].astype(bool)
        # not reached at the end of the second module; omitted items the student could not answer
        admin = np.ones((n, 2, W.N_ITEM), np.int8)
        nr = (r.random(n) < 0.03) & tested
        nk = r.integers(1, 4, n)
        for i in np.where(nr)[0]:
            admin[i, 1, W.N_ITEM - nk[i]:] = 0
        omit = (r.random((n, 2, W.N_ITEM)) < 0.04) & (y == 0) & (admin == 1)
        left = (~elig) & (~tested) & (r.random(n) < 0.5)            # left the district before 1 May
        lessons = np.where(elig, r.integers(20, 161, n), np.where(left, r.integers(0, 61, n), r.integers(0, 20, n)))
        late = r.random(n) < 0.08
        first_day = dt.date(2025, 8, int(r.integers(4, 14)))
        enrolled = [first_day + dt.timedelta(days=int(r.integers(30, 220))) if late[i] else first_day for i in range(n)]
        left_on = [first_day + dt.timedelta(days=int(r.integers(60, 250))) if left[i] else None for i in range(n)]
        mover = (~left) & (r.random(n) < 0.015) & (np.array(enrolled) < dt.date(2026, 3, 1))
        sids = [nxt("sid", sid_pool) for _ in range(n)]
        old_sids = [nxt("sid", sid_pool) for _ in range(n)] if j in RE_ROSTERED else None
        tts = [nxt("tt", tt_pool) for _ in range(n)]
        test_day0 = WINDOW[0] + dt.timedelta(days=int(r.integers(0, 25)))
        off = UTC_OFFSET[st]
        ab_tested = tested & (r.random(n) < 0.05)
        ab_untested = (~tested) & (~left) & (r.random(n) < 0.25)
        form_ids = ["F%02d" % (f + 1) for f in s["form"]]
        ed_c, el_c, sw_c = CODES[st]
        test_name, levels = LEVELS[st]
        moved_on = {i: dt.date(2025, 10, 6) + dt.timedelta(days=int(r.integers(0, 130))) for i in np.where(mover)[0]}
        cut_day = dt.date(2026, 1, 12)
        for i in range(n):
            sid = "S%d" % sids[i]
            tt = "CT%d" % tts[i]
            start = moved_on.get(i, enrolled[i])
            two_ids = old_sids is not None and start < cut_day and (left_on[i] is None or left_on[i] > cut_day)
            # eligibility: the current roster record, a superseded record for re-rostered students, and the
            # origin district's record for students who moved in
            # a re-rostered student's lessons sit on the record that logged them: those before the January change
            # on the superseded ID, the rest on the current one; the eligibility flag reads the two together
            before = int(lessons[i] * r.uniform(0.25, 0.5)) if two_ids else 0
            elig_rows.append(dict(partner_id=dd["partner_id"], student_id=sid, grade=W.GRADES[s["g"][i]],
                                  enrolled_on=start, withdrawn_on=left_on[i],
                                  rostered_2026_05_01="N" if left[i] else "Y", lessons=int(lessons[i]) - before,
                                  eligible="Y" if elig[i] else "N"))
            if two_ids:
                elig_rows.append(dict(partner_id=dd["partner_id"], student_id="S%d" % old_sids[i],
                                      grade=W.GRADES[s["g"][i]], enrolled_on=start, withdrawn_on=cut_day,
                                      rostered_2026_05_01="N", lessons=before, eligible="N"))
                xwalk_rows.append(dict(student_id="S%d" % old_sids[i], test_taker_id=tt, partner_id=dd["partner_id"],
                                       linked_on=max(start, dt.date(2025, 9, 2)), source="Roster sync"))
            xwalk_rows.append(dict(student_id=sid, test_taker_id=tt, partner_id=dd["partner_id"],
                                   linked_on=dt.date(2026, 1, 13) if two_ids else max(start, dt.date(2025, 9, 2)),
                                   source="Roster sync"))
            if i in moved_on:
                others = [k for k in by_state[st] if k != j]
                o = W.DISTRICTS[others[int(r.integers(len(others)))]]
                elig_rows.append(dict(partner_id=o["partner_id"], student_id=sid, grade=W.GRADES[s["g"][i]],
                                      enrolled_on=first_day, withdrawn_on=moved_on[i] - dt.timedelta(days=3),
                                      rostered_2026_05_01="N", lessons=int(r.integers(4, 40)), eligible="N"))
            # each student's latest roster upload: the spring upload, the April upload of students who enrolled
            # after it, the fall upload of students who left before it
            if left_on[i] is not None and left_on[i] <= SPRING_UPLOAD:
                up = FALL_UPLOAD
            elif start > SPRING_UPLOAD:
                up = APRIL_UPLOAD
            else:
                up = SPRING_UPLOAD
            b = s["band"][i]
            lev = "" if b == 4 else levels[b][int(r.integers(len(levels[b])))]
            roster_rows.append(dict(state=st, partner_id=dd["partner_id"], student_id=sid,
                                    grade=W.GRADES[s["g"][i]], econ=ed_c[0] if s["ed"][i] else ed_c[1],
                                    el=el_c[0] if s["el"][i] else el_c[1], swd=sw_c[0] if s["iep"][i] else sw_c[1],
                                    prior_test="" if b == 4 else "%s %s" % (test_name, "Science" if r.random() < 0.5
                                                                            else "Mathematics"),
                                    prior_level=lev, upload_date=up))
            # sessions: an abandoned attempt (partial, never scored), then the submitted session
            day = test_day0 + dt.timedelta(days=int(r.integers(0, 9)))
            while day.weekday() >= 5:
                day += dt.timedelta(days=1)
            hh, mm = int(r.integers(8, 14)), int(r.choice([0, 5, 10, 15, 20, 30, 35, 40, 45, 50]))
            if ab_tested[i] or ab_untested[i]:
                k = int(r.integers(1, 7 if ab_tested[i] else 9))
                aday = day
                if ab_tested[i]:            # the student sat again on a later day and submitted
                    day = day + dt.timedelta(days=int(r.integers(1, 4)))
                    while day.weekday() >= 5:
                        day += dt.timedelta(days=1)
                    day = min(day, WINDOW[1])
                sess = "SN%d" % nxt("sess", sess_pool)
                sess_rows.append(dict(session_id=sess, test_taker_id=tt, form_id=form_ids[i], status="Abandoned",
                                      started=_when(aday, hh, mm, off), submitted="", items=k))
                th = s["theta"][i]
                for q in range(k):
                    jj, kk = divmod(q, W.N_ITEM)
                    m = mods[i, jj]
                    p = 1 / (1 + np.exp(-W.A[m, kk] * (th - W.B[m, kk])))
                    sc = int(r.random() < p)
                    resp_rows.append((sess, q + 1, item_id[(m, kk)], "Answered", sc))
            if tested[i]:
                sess = "SN%d" % nxt("sess", sess_pool)
                dur = int(r.integers(24, 52))
                sess_rows.append(dict(session_id=sess, test_taker_id=tt, form_id=form_ids[i], status="Submitted",
                                      started=_when(day, hh, mm, off),
                                      submitted=_when(day, hh + (mm + dur) // 60, (mm + dur) % 60, off),
                                      items=int(admin[i].sum())))
                for q in range(2 * W.N_ITEM):
                    jj, kk = divmod(q, W.N_ITEM)
                    m = mods[i, jj]
                    if not admin[i, jj, kk]:
                        resp_rows.append((sess, q + 1, item_id[(m, kk)], "Not reached", None))
                    elif omit[i, jj, kk]:
                        resp_rows.append((sess, q + 1, item_id[(m, kk)], "Omitted", 0))
                    else:
                        resp_rows.append((sess, q + 1, item_id[(m, kk)], "Answered", int(y[i, jj, kk])))
        parts.append(dict(j=np.full(n, j), g=s["g"], ed=s["ed"], el=s["el"], iep=s["iep"], band=s["band"],
                          theta=s["theta"], eligible=elig, tested=tested, y=y, mods=mods, admin=admin,
                          tt=np.array(["CT%d" % t for t in tts]), state=np.full(n, W.STATES.index(st))))
    c = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    c["dist"] = c["j"]; c["D"] = len(W.DISTRICTS)
    return dict(c=c, elig=elig_rows, roster=roster_rows, xwalk=xwalk_rows, sessions=sess_rows, responses=resp_rows,
                item_id=item_id)


def tested_view(c):
    """The tested students only, with the likelihood of their scored responses."""
    t = c["tested"]
    v = {k: (val[t] if isinstance(val, np.ndarray) and len(val) == len(t) else val) for k, val in c.items()}
    ll = irt.loglik(v["y"], v["mods"], v["admin"])
    v["ll"] = ll
    v["L"] = irt.norm_lik(ll)
    return v


def contractor(v):
    """Caldrith's population model (grade, state, prior band, economic disadvantage, English learner, disability) on
    every tested student, and five plausible values per student on the reporting scale."""
    allm = np.ones(len(v["g"]), bool)
    w, gam, s2 = irt.lr_em(v["L"], irt.X_of(v, "vendor", allm))
    pv = irt.to_scale(irt.draw_pv(w, W.VENDOR_SEED))
    return dict(w=w, gamma=gam, s2=float(s2[0]), pv=pv)
