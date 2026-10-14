"""Assemble the operating records from the simulated census: identifiers, the receipt register, the coding calendar and
the clerical coders, the coding extract, the coding quality study, the follow-up visit log (with the tablets that re-sent
their history), the coding staff register and the coding timesheets."""
from datetime import date, datetime, timedelta

import numpy as np

import params as P
import sim
import world as W

HOLIDAYS = {date(2026, 6, 1), date(2026, 8, 3), date(2026, 10, 26)}
MODE = {"O": "ONLINE", "P": "PAPER", "FS": "FIELD", "FP": "FIELD"}
MODE_CODE = {"O": "ONL", "P": "PAP", "FS": "FUP", "FP": "FUP"}


def study_select(S, Cd):
    """systematic selection inside each load batch (a day's loads of one capture mode), separately on each coding path:
    every k-th record in document order from the batch's start"""
    route = S["p_route"]
    coded = S["coded"]
    n = len(route)
    mode = np.where(route == "O", 0, np.where(route == "P", 1, 2))
    bkey = mode * 100000 + S["p_bdate"]
    order = np.lexsort((np.arange(n), bkey))
    order = order[coded[order]]
    bk_o = bkey[order]
    bstart = np.r_[True, bk_o[1:] != bk_o[:-1]]
    bid = np.cumsum(bstart) - 1
    self_bt = np.isin(route[order], ["O", "P"])
    pc = (Cd["path_old"] == "C")[order]
    sel = np.zeros(n, bool)
    w = np.zeros(n, int)
    for isC in (False, True):
        ind = (pc == isC).astype(np.int64)
        cs = np.cumsum(ind)
        base = np.r_[0, cs[:-1]][bstart][bid]
        rank = cs - ind - base
        k = np.where(self_bt, P.STUDY_K[("SELF", "C" if isC else "A")], P.STUDY_K[("NRFU", "C" if isC else "A")])
        start = (bk_o * 2654435761 + (7 if isC else 3)) % 997 % k
        pick = (ind == 1) & ((rank % k) == start)
        sel[order[pick]] = True
        w[order[pick]] = k[pick]
    return sel, w


def working_days(d0, d1):
    out = []
    d = d0
    while d <= d1:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += timedelta(days=1)
    return out


# ------------------------------------------------------------------------------------------------ the coding roster
# (staff_no, coder_id, team, contract, from, to); a coder who moves team has a row per assignment; a temporary coder id
# returns to the pool when its holder leaves and is issued to the next starter
ROSTER = [
    ("S40112", "OC101", 1, "PERMANENT", date(2026, 5, 4), None),
    ("S40118", "OC102", 1, "PERMANENT", date(2026, 5, 4), date(2026, 10, 18)),
    ("S40118", "OC102", 3, "PERMANENT", date(2026, 10, 19), None),
    ("S41207", "OC201", 1, "TEMPORARY", date(2026, 5, 4), None),
    ("S41213", "OC202", 1, "TEMPORARY", date(2026, 5, 18), None),
    ("S40125", "OC103", 2, "PERMANENT", date(2026, 5, 4), None),
    ("S40131", "OC104", 2, "PERMANENT", date(2026, 5, 4), date(2026, 10, 11)),
    ("S40131", "OC104", 5, "PERMANENT", date(2026, 10, 12), None),
    ("S41220", "OC203", 2, "TEMPORARY", date(2026, 5, 4), None),
    ("S41236", "OC204", 2, "TEMPORARY", date(2026, 5, 4), date(2026, 10, 11)),
    ("S41236", "OC204", 5, "TEMPORARY", date(2026, 10, 12), None),
    ("S41242", "OC205", 2, "TEMPORARY", date(2026, 6, 1), date(2026, 10, 9)),
    ("S41391", "OC205", 4, "TEMPORARY", date(2026, 10, 19), None),
    ("S40144", "OC105", 3, "PERMANENT", date(2026, 5, 4), None),
    ("S40150", "OC106", 3, "PERMANENT", date(2026, 5, 4), None),
    ("S41255", "OC206", 3, "TEMPORARY", date(2026, 5, 11), date(2026, 10, 2)),
    ("S41384", "OC206", 1, "TEMPORARY", date(2026, 10, 13), None),
    ("S41261", "OC207", 3, "TEMPORARY", date(2026, 5, 11), date(2026, 10, 26)),
    ("S41261", "OC207", 4, "TEMPORARY", date(2026, 10, 27), None),
    ("S40163", "OC107", 4, "PERMANENT", date(2026, 5, 4), None),
    ("S40179", "OC108", 4, "PERMANENT", date(2026, 5, 4), None),
    ("S41278", "OC208", 4, "TEMPORARY", date(2026, 5, 18), date(2026, 10, 4)),
    ("S41278", "OC208", 1, "TEMPORARY", date(2026, 10, 5), None),
    ("S41284", "OC209", 4, "TEMPORARY", date(2026, 6, 15), None),
    ("S40186", "OC109", 5, "PERMANENT", date(2026, 5, 4), None),
    ("S40192", "OC110", 5, "PERMANENT", date(2026, 5, 4), None),
    ("S41297", "OC210", 5, "TEMPORARY", date(2026, 5, 4), date(2026, 10, 16)),
    ("S41402", "OC210", 2, "TEMPORARY", date(2026, 10, 22), None),
    ("S41303", "OC211", 5, "TEMPORARY", date(2026, 6, 1), None),
    ("S41319", "OC212", 3, "TEMPORARY", date(2026, 7, 6), None),
]
SHIFT = {1: (8 * 60, 16 * 60 + 30), 2: (8 * 60, 16 * 60 + 30), 3: (14 * 60, 22 * 60 + 30), 4: (14 * 60, 22 * 60 + 30),
         5: (22 * 60, 30 * 60 + 30)}
SHIFT_SHARE = {1: 0.235, 2: 0.215, 3: 0.18, 4: 0.17, 5: 0.20}


def active(day):
    """roster rows active on a coding day: (staff_no, coder_id, team)"""
    return [(s, c, t) for s, c, t, _, f, e in ROSTER if f <= day and (e is None or day <= e)]


def coding_calendar(S, Cd, rng):
    """each coded record's coding day (first in, first out from 4 May to 13 November), its coded_at (local time) and, on
    the clerical path, its coder; the night team's shift runs past midnight into the next calendar day"""
    route = S["p_route"]
    coded = S["coded"]
    n = len(route)
    mode = np.where(route == "O", 0, np.where(route == "P", 1, 2))
    q = np.lexsort((np.arange(n), mode, S["p_bdate"]))
    q = q[coded[q]]
    days = working_days(P.CODING_START, P.EXTRACT)
    cap = 1 + 0.10 * np.sin(np.arange(len(days)) / 3.1) + rng.normal(0, 0.05, len(days))
    cum = np.cumsum(cap) / cap.sum()
    pos = (np.arange(len(q)) + 0.5) / len(q)
    di = np.minimum(np.searchsorted(cum, pos), len(days) - 1)
    day_of = np.full(n, -1)
    day_of[q] = di
    path = Cd["path_old"]
    team_u = rng.random(n)
    mins_u = rng.random(n)
    who_u = rng.random(n)
    tcum = np.cumsum([SHIFT_SHARE[t] for t in (1, 2, 3, 4, 5)])
    team = np.minimum(1 + np.searchsorted(tcum, team_u * tcum[-1]), 5)
    # the night team does not work the night before a non-working day
    nights_off = set()
    for k, d in enumerate(days):
        nxt = d + timedelta(days=1)
        if nxt.weekday() >= 5 or nxt in HOLIDAYS:
            nights_off.add(k)
        # CODA closes for month-end processing on the night of the last working day of each month
        if k + 1 < len(days) and days[k + 1].month != d.month:
            nights_off.add(k)
    base = np.array([(datetime(d.year, d.month, d.day) - datetime(2026, 1, 1)).total_seconds() / 60 for d in days])
    minute = np.zeros(n)
    coder = np.full(n, "", object)
    isA = coded & (path == "A")
    # the autocoder runs as a nightly batch from about 01:00, first in first out, a second or two a write-in; every
    # save is stamped to the second (a stream of its own, so no other draw moves)
    tr = np.random.default_rng(P.SEED + 71)
    run_start = 60 + tr.integers(0, 25, len(days))
    pace = tr.uniform(1.4, 2.6, len(days))
    order = np.empty(n, dtype=np.int64)
    order[q] = np.arange(len(q))
    idxA = np.where(isA)[0]
    for k in range(len(days)):
        jj = idxA[day_of[idxA] == k]
        if not len(jj):
            continue
        jj = jj[np.argsort(order[jj], kind="stable")]
        secs = np.floor(np.arange(len(jj)) * pace[k] + tr.uniform(0, pace[k], len(jj)))
        minute[jj] = base[k] + run_start[k] + secs / 60.0
    isC = np.where(coded & (path == "C"))[0]
    night_off = np.array([day_of[j] in nights_off for j in isC])
    team[isC[night_off & (team[isC] == 5)]] = 3
    for k, d in enumerate(days):
        on = {t: [c for s_, c, tt in active(d) if tt == t] for t in (1, 2, 3, 4, 5)}
        jj = isC[day_of[isC] == k]
        for t in (1, 2, 3, 4, 5):
            m = jj[team[jj] == t]
            if not len(m):
                continue
            pool = on[t] or [c for v in on.values() for c in v]
            coder[m] = np.array(pool, object)[np.minimum((who_u[m] * len(pool)).astype(int), len(pool) - 1)]
            a, b = SHIFT[t]
            minute[m] = base[k] + a + 20 + (mins_u[m] * (b - a - 50)).astype(int)
    isC_all = coded & (path == "C")
    minute[isC_all] = minute[isC_all] + tr.integers(0, 60, int(isC_all.sum())) / 60.0
    coded_at = np.array([datetime(2026, 1, 1) + timedelta(seconds=int(round(x * 60))) if c else None
                         for x, c in zip(minute, coded)], object)
    return day_of, coded_at, coder, days, team


# ------------------------------------------------------------------------------------------------ identifiers
def address_ids(n_a):
    return np.array(["AD%07d" % (2000000 + 3 * a + a % 3) for a in range(n_a)], object)


def questionnaire_ids(S, rng):
    """the questionnaire number each mode's form carries: online sessions, pre-printed paper forms, field forms"""
    n_a = S["n_a"]
    pre = {"O": "OL26", "P": "PQ26", "FS": "FQ26", "FP": "FQ26"}
    nums = rng.choice(np.arange(1000000, 9999999), size=n_a + 400, replace=False)
    q = np.full(n_a, "", object)
    for a in np.where(S["has_form"])[0]:
        q[a] = pre[S["route"][a]] + "%07d" % nums[a]
    return q, nums[n_a:]


def enumerators(S):
    n_eds = len(S["ed_code"])
    staff = np.array(["EN%04d" % (1012 + 7 * (e // 2) % 8000) for e in range(n_eds)], object)
    tabs = np.array(["TB%05d" % (40100 + 13 * (e // 2)) for e in range(n_eds)], object)
    return staff, tabs


OUTCOME = {"HH": "10", "PX": "20", "NC": "31", "RF": "32", "VAC": "40", "DEL": "50", "SR": "60"}
REPLACED = 2    # tablets replaced in September in each region; the replacement's first sync re-sent the last 14 days' calls


def visit_log(S, q_ids, spare_q, rng):
    """one row per doorstep call (and an administrative row when a self-response closes a case), with the tablet that
    recorded it; a replacement tablet's first sync re-sent the calls of the last 14 days under new call numbers"""
    staff, tabs = enumerators(S)
    a_ids = address_ids(S["n_a"])
    rows = []
    vis = S["visits"]
    # a proxy return replaced by a re-interview keeps its own questionnaire number, withdrawn at the re-interview
    sq = iter(spare_q)
    last_px = {}
    for i, (a, vn, day, mi, out, resp) in enumerate(vis):
        if out == "PX":
            last_px[a] = i
    replaced_px = {i for a, i in last_px.items() if S["reint"][a]}
    # an enumerator who finds nobody in may call again later the same day: the earlier call is a call of its own
    calls = {}
    for i, v in enumerate(vis):
        calls.setdefault(v[0], []).append(i)
    extra = {}
    for a, ii in calls.items():
        if len(ii) >= 6 or vis[ii[0]][4] == "SR":
            continue
        for i in ii:
            if vis[i][4] in ("NC", "RF", "HH", "PX") and vis[i][3] is not None and vis[i][3] > 840 and rng.random() < 0.035:
                extra[i] = max(540 + int(rng.integers(0, 40)), int(vis[i][3]) - int(rng.integers(180, 420)))
                break
    renum = {}
    for a, ii in calls.items():
        k = 0
        for i in ii:
            if vis[i][4] == "SR":
                continue
            if i in extra:
                k += 1
            k += 1
            renum[i] = k
    pre = []
    for i, (a, vn, day, mi, out, resp) in enumerate(vis):
        if i in extra:
            e = S["a_ed"][a]
            t = datetime(2026, 1, 1) + timedelta(days=int(day), minutes=extra[i])
            lag = 0 if rng.random() < 0.83 else int(rng.integers(1, 4))
            sync = datetime(2026, 1, 1) + timedelta(days=int(day) + lag,
                                                  minutes=int(min(max(mi + 25, 18 * 60) + rng.integers(0, 200), 1439)))
            pre.append([a, e, staff[e], renum[i] - 1, t, "31", "", "", tabs[e], sync])
    rows.extend(pre)
    for i, (a, vn, day, mi, out, resp) in enumerate(vis):
        vn = renum.get(i, vn)
        e = S["a_ed"][a]
        if out == "SR":
            t = datetime(2026, 1, 1) + timedelta(days=int(day), hours=9)
            rows.append([a, e, "", None, t, OUTCOME[out], "", q_ids[a], "", t + timedelta(minutes=int(rng.integers(5, 300)))])
            continue
        t = datetime(2026, 1, 1) + timedelta(days=int(day), minutes=int(mi))
        q = ""
        if out in ("HH", "PX"):
            q = "FQ26%07d" % next(sq) if i in replaced_px else q_ids[a]
        if out in ("HH", "PX") and i not in replaced_px:
            sday = int(S["rec"][a])
            if sday > day:
                sync = datetime(2026, 1, 1) + timedelta(days=sday, minutes=int(rng.integers(7 * 60, 12 * 60)))
            else:
                sync = datetime(2026, 1, 1) + timedelta(days=sday, minutes=int(min(max(mi + 30, 19 * 60) + rng.integers(0, 180), 1439)))
        else:
            lag = 0 if rng.random() < 0.83 else int(rng.integers(1, 4))
            sync = datetime(2026, 1, 1) + timedelta(days=int(day) + lag,
                                                  minutes=int(min(max(mi + 25, 18 * 60) + rng.integers(0, 200), 1439)))
        rows.append([a, e, staff[e], vn, t, OUTCOME[out], resp, q, tabs[e], sync])
    # tablets replaced in October
    sep1 = datetime(2026, 9, 1)
    by_ed = {}
    for r in rows:
        if r[2]:
            by_ed.setdefault(r[1], []).append(r)
    region = S["ed_region"]
    when_of = {}
    pick_eds = []
    for code, _, _ in W.REGIONS:
        cands = []
        for e, rr in sorted(by_ed.items()):
            if region[e] != code:
                continue
            when = datetime(2026, 9, 8) + timedelta(days=int(rng.integers(0, 18)), hours=int(rng.integers(8, 11)))
            lo = max(sep1, when - timedelta(days=14))
            n_oct = sum(1 for r in rr if lo <= r[4] < when)
            n_close = sum(1 for r in rr if lo <= r[4] < when and r[5] in ("10", "20"))
            if n_oct >= 6 and n_close >= 1:
                cands.append(e)
                when_of[e] = when
        pick_eds += list(rng.choice(cands, size=min(REPLACED, len(cands)), replace=False))
    pick_eds = sorted(pick_eds)
    replays = []
    new_tab = {}
    for k, e in enumerate(pick_eds):
        when = when_of[e]
        new_tab[e] = ("TB%05d" % (47100 + 7 * k), when)
        first_sync = when + timedelta(minutes=int(rng.integers(20, 90)))
        by_case = {}
        for r in by_ed[e]:
            by_case.setdefault(r[0], []).append(r)
        for a, rr in sorted(by_case.items()):
            recent = sorted([r for r in rr if when - timedelta(days=14) <= r[4] < when], key=lambda r: r[4])
            if not recent:
                continue
            top = max(r[3] for r in rr if r[4] < when and r[3] is not None)
            for j_, r in enumerate(recent):
                replays.append([r[0], r[1], r[2], top + 1 + j_, r[4], r[5], r[6], r[7], new_tab[e][0],
                                first_sync + timedelta(seconds=int(rng.integers(0, 900))), True])
            # the replacement tablet numbers the case's later calls after the re-sent ones
            for r in rr:
                if r[4] >= when and r[3] is not None:
                    r[3] = r[3] + len(recent)
    # after the replacement the enumerator's visits carry the new tablet
    for r in rows:
        if r[1] in new_tab and r[2] and r[4] >= new_tab[r[1]][1]:
            r[8] = new_tab[r[1]][0]
    for r in rows:
        r.append(False)
    allrows = rows + replays
    allrows.sort(key=lambda r: (r[9], r[4], r[0]))
    out = dict(visit_id=np.array(["V%08d" % (30000001 + i) for i in range(len(allrows))], object),
               a=np.array([r[0] for r in allrows]), e=np.array([r[1] for r in allrows]),
               staff_id=np.array([r[2] for r in allrows], object), visit_no=np.array([r[3] for r in allrows], object),
               visit_time=np.array([r[4] for r in allrows], object), outcome_code=np.array([r[5] for r in allrows], object),
               proxy_respondent=np.array([r[6] for r in allrows], object),
               questionnaire_id=np.array([r[7] for r in allrows], object), device_id=np.array([r[8] for r in allrows], object),
               synced_at=np.array([r[9] for r in allrows], object), replay=np.array([r[10] for r in allrows]))
    out["address_id"] = a_ids[out["a"]]
    out["ed_code"] = S["ed_code"][out["e"]]
    return out, new_tab


# ------------------------------------------------------------------------------------------------ write-ins
ABBREV = [("assistant", "asst"), ("manager", "mgr"), ("technician", "tech"), ("operator", "op"),
          ("supervisor", "supvr"), ("department", "dept")]


def writein(unit, vague, phrase, route, u_txt, u_title, u_style):
    if vague:
        texts = W.VAGUE_TEXT[phrase][1 if route == "FP" else 0]
        t = texts[min(int(u_txt * len(texts)), len(texts) - 1)]
    else:
        titles = W.TITLES[unit][1]
        t = titles[min(int(u_title * len(titles)), len(titles) - 1)]
        if route == "FP" and u_txt < 0.22:
            t = [t + " i think", "works as a " + t.lower(), t + " - not sure"][int(u_txt / 0.22 * 3) % 3]
    if route == "O":
        return t.lower() if u_style < 0.15 else t
    if route == "P":
        t = t.upper()
        if u_style < 0.03:
            for a, b in (("O", "0"), ("I", "1"), ("S", "5")):
                k = t.find(a, 1)
                if k > 0:
                    return t[:k] + b + t[k + 1:]
        return t
    t = t.lower()
    if u_style < 0.35:
        for a, b in ABBREV:
            t = t.replace(a, b)
    return t


# ------------------------------------------------------------------------------------------------ the tables
def build_tables(S, U, Cd, seed=P.SEED + 29):
    """every record the pack ships, as plain columns; the main call reads the register, the extract, the study and the
    visit log's closing outcomes, the asks read the coders' and the field's activity"""
    ss = np.random.SeedSequence(seed)
    r_id, r_cal, r_vis, r_ts, r_txt = [np.random.default_rng(x) for x in ss.spawn(5)]
    n_a = S["n_a"]
    a_ids = address_ids(n_a)
    q_ids, spare = questionnaire_ids(S, r_id)
    form = np.where(S["has_form"])[0]
    mode_i = np.array([{"O": 0, "P": 1, "FS": 2, "FP": 2}[S["route"][a]] for a in form])
    order = form[np.lexsort((form, mode_i, S["bdate"][form]))]
    doc = np.full(n_a, "", object)
    for i, a in enumerate(order):
        doc[a] = "D%08d" % (10400001 + i)
    ex = sim.dn(P.EXTRACT)
    batch = np.full(n_a, "", object)
    for a in form:
        if S["bdate"][a] <= ex:
            batch[a] = MODE_CODE[S["route"][a]] + "-" + sim.dd(S["bdate"][a]).strftime("%y%m%d")
    reg = dict(doc_id=doc[order], questionnaire_id=q_ids[order], address_id=a_ids[order],
               ed_code=S["ed_code"][S["a_ed"][order]], capture_mode=np.array([MODE[S["route"][a]] for a in order], object),
               received_date=np.array([sim.dd(S["rec"][a]) for a in order], object), load_batch=batch[order],
               usual_residents=S["n_res"][order], in_employment=S["n_emp"][order], occupation_writeins=S["n_w"][order],
               _a=order)
    # persons
    own = S["owner"]
    day_of, coded_at, coder, days, team = coding_calendar(S, Cd, r_cal)
    coded = S["coded"]
    sel, w = study_select(S, Cd)
    wk = np.array([((c.date() - P.CODING_START).days // 7 + 1) if c is not None else 0 for c in coded_at])
    pc = np.where(Cd["path_old"] == "A", "AUTO", "CLERICAL")
    ext_idx = np.where(coded)[0]
    ext_idx = ext_idx[np.lexsort((S["person_no"][ext_idx], np.array([doc[own[j]] for j in ext_idx])))]
    ext = dict(doc_id=np.array([doc[own[j]] for j in ext_idx], object), person_no=S["person_no"][ext_idx],
               load_batch=batch[own[ext_idx]], coding_week=wk[ext_idx], autocoder_code=Cd["sugg"][ext_idx],
               autocoder_score=Cd["score"][ext_idx], coding_path=pc[ext_idx], production_code=Cd["prod_old"][ext_idx],
               coder_id=coder[ext_idx], coded_at=coded_at[ext_idx], _p=ext_idx)
    st_idx = np.where(sel)[0]
    st_idx = st_idx[np.lexsort((S["person_no"][st_idx], np.array([doc[own[j]] for j in st_idx])))]
    u_style = r_txt.random(len(own))
    text = np.array([writein(S["p_unit"][j], Cd["vague"][j], Cd["phrase"][j], S["p_route"][j], U["txt"][j],
                             U["title"][j], u_style[j]) for j in st_idx], object)
    adj = np.where(U["adj"][st_idx] < np.where(Cd["vague"][st_idx], P.ADJUDICATED[1], P.ADJUDICATED[0]),
                   "ADJUDICATED", "AGREED")
    stu = dict(study_ref=np.array(["CQS%06d" % (100001 + i) for i in range(len(st_idx))], object),
               doc_id=np.array([doc[own[j]] for j in st_idx], object), person_no=S["person_no"][st_idx],
               load_batch=batch[own[st_idx]],
               batch_type=np.where(np.isin(S["p_route"][st_idx], ["O", "P"]), "SELF-RESPONSE", "FOLLOW-UP"),
               coding_path=pc[st_idx], selection_interval=w[st_idx], occupation_writein=text,
               autocoder_code=Cd["sugg"][st_idx], autocoder_score=Cd["score"][st_idx],
               production_code=Cd["prod_old"][st_idx], reference_code=Cd["ref"][st_idx], reference_basis=adj, _p=st_idx)
    V, new_tab = visit_log(S, q_ids, spare, r_vis)
    staff_reg, moves, ts = timesheets(ext, days, r_ts)
    return dict(reg=reg, ext=ext, stu=stu, vis=V, new_tab=new_tab, staff=staff_reg, moves=moves, ts=ts, doc=doc, a_ids=a_ids,
                q_ids=q_ids, sel=sel, w=w, coded_at=coded_at, coder=coder, team=team, day_of=day_of, days=days)


LEADS = [("S40017", 1), ("S40023", 2), ("S40038", 3), ("S40046", 4), ("S40059", 5)]
PROD = 14.0     # clerical occupation write-ins an hour, on average


def timesheets(ext, days, rng):
    """the coding staff register (everyone who has worked in census coding, with the team they are in or left from),
    the staff movements log since coding began, and
    the timesheet export for the three pay fortnights from 21 September (one row per person, shift start date and
    activity; a team lead's correction is a further line)"""
    asg = {}
    for s_, c, t, k, f, e in ROSTER:
        asg.setdefault(s_, []).append((f, e, c, t, k))
    staff_reg, moves = [], []
    for s_, rows_ in sorted(asg.items()):
        rows_.sort()
        prev = None
        for f, e, c, t, k in rows_:
            if prev is None:
                moves.append(dict(staff_no=s_, coder_id=c, movement="STARTED", team_from="", team_to="Coding Team %d" % t,
                                  effective_date=f))
            elif prev[3] != t:
                moves.append(dict(staff_no=s_, coder_id=c, movement="TRANSFERRED", team_from="Coding Team %d" % prev[3],
                                  team_to="Coding Team %d" % t, effective_date=f))
            prev = (f, e, c, t, k)
        f, e, c, t, k = rows_[-1]
        if e is not None:
            moves.append(dict(staff_no=s_, coder_id=c, movement="LEFT", team_from="Coding Team %d" % t, team_to="",
                              effective_date=e))
        staff_reg.append(dict(staff_no=s_, coder_id=c, team="Coding Team %d" % t, role="CODER", contract=k,
                              status="LEFT" if e is not None else "IN POST", started=rows_[0][0], left=e))
    for s_, t in LEADS:
        staff_reg.append(dict(staff_no=s_, coder_id="", team="Coding Team %d" % t, role="TEAM LEAD", contract="PERMANENT",
                              status="IN POST", started=date(2026, 5, 4), left=None))
        moves.append(dict(staff_no=s_, coder_id="", movement="STARTED", team_from="", team_to="Coding Team %d" % t,
                          effective_date=date(2026, 5, 4)))
    staff_reg.sort(key=lambda r: (r["team"], r["role"] != "TEAM LEAD", r["staff_no"]))
    moves.sort(key=lambda r: (r["effective_date"], r["staff_no"], r["movement"]))
    # write-ins coded per coder and shift
    w0, w1 = date(2026, 9, 21), date(2026, 11, 1)
    shift_n = {}
    day_index = {d: k for k, d in enumerate(days)}
    for c, t in zip(ext["coder_id"], ext["coded_at"]):
        if not c:
            continue
        d = t.date()
        if t.hour < 7:
            d = d - timedelta(days=1)
        if w0 <= d <= w1:
            shift_n[(c, d)] = shift_n.get((c, d), 0) + 1
    rows = []
    prod = {}
    for s, c, t, k, f, e in ROSTER:
        prod.setdefault(s, PROD * float(np.exp(rng.normal(0, 0.12))))
        for d in days:
            if not (w0 <= d <= w1) or d < f or (e is not None and d > e):
                continue
            n = shift_n.get((c, d), 0)
            occ = round(n / prod[s] * float(np.exp(rng.normal(0, 0.06))) * 4) / 4 if n else 0.0
            other = 0.25 * int(rng.integers(0, 4))
            trn = 3.5 if (d - f).days < 3 and f >= date(2026, 9, 1) else 0.0
            ind = max(0.5, 7.25 - occ - other - trn)
            for act, h in (("OCC", occ), ("IND", ind), ("QRY", other), ("TRN", trn)):
                if h > 0:
                    rows.append(dict(staff_no=s, work_date=d, activity=act, hours=h,
                                     entered_on=d + timedelta(days=int(rng.integers(0, 3))), note=""))
    for s, t in LEADS:
        for d in days:
            if w0 <= d <= w1:
                rows.append(dict(staff_no=s, work_date=d, activity="SUP", hours=7.25, entered_on=d, note=""))
    # supervisors' corrections: an hours line keyed twice, taken back with a negative line entered later
    corr = [("S40118", date(2026, 10, 7), -2.5, "OCC overclaimed 07/10, corrected by team lead"),
            ("S41220", date(2026, 10, 14), -3.0, "14/10 OCC was 3 hours over"),
            ("S40144", date(2026, 10, 21), -1.75, "entered in error"),
            ("S41284", date(2026, 10, 8), -2.25, "reverses duplicate OCC line of 08/10"),
            ("S41303", date(2026, 10, 27), -2.0, "OCC corrected for 27/10 shift"),
            ("S40125", date(2026, 9, 29), -1.5, "late correction for 29/09")]
    for s, d, h, note in corr:
        rows.append(dict(staff_no=s, work_date=d, activity="OCC", hours=h, entered_on=d + timedelta(days=int(rng.integers(5, 9))),
                         note=note))
        rows.append(dict(staff_no=s, work_date=d, activity="OCC", hours=-h, entered_on=d, note=""))
    rows.sort(key=lambda r: (r["work_date"], r["staff_no"], r["activity"], r["entered_on"]))
    return staff_reg, moves, rows
