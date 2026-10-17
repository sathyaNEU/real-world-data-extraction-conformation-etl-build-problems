"""task156 ask worlds: the records only the supplemental asks read.

- The paid moderation team's 2026 shifts (the WFM system), its assignment history and the six moves of July and August
  2026 (Ask B).
- Every moderator flag raised in July, August and September 2026 (the moderator tool), with the decision reviews of
  the quarter (Ask A).
- Every question moved between sites in 2021 to 2023 (the moderators' migration log), which the old monthly workbook
  counted on both sites (Ask C).

The main call reads none of these records; its flags are the moderator tool's daily summary, built from the same
daily counts the per-flag records expand."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

TORONTO_OFFSET = {}   # filled lazily: UTC offset hours on a date (EST -5, EDT -4)


def toronto_offset(d):
    """Hours behind UTC in Toronto on date d (DST from the second Sunday of March to the first Sunday of November)."""
    y = d.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return 4 if mar <= d < nov else 5


# ------------------------------------------------------------------------------------------------- the paid team
# 2026 allocation by site (FTE the council funded for 2026, from its 2025 figures) and the moves of summer 2026
ALLOC_2026 = {"web": 6.0, "mobile": 2.0, "data": 4.0, "databases": 3.5, "devops": 3.5, "gamedev": 1.5,
              "security": 3.0, "embedded": 2.0, "scicomp": 1.5}
MOVES = [  # (from, to, effective date) six moderators moved to the sites whose queues grew
    ("web", "security", dt.date(2026, 7, 6)),
    ("mobile", "embedded", dt.date(2026, 7, 13)),
    ("data", "scicomp", dt.date(2026, 7, 20)),
    ("databases", "security", dt.date(2026, 8, 3)),
    ("devops", "embedded", dt.date(2026, 8, 10)),
    ("gamedev", "scicomp", dt.date(2026, 8, 17)),
]
WFM_SITE_LABEL = {"web": "Frontend & Web", "mobile": "Mobile Apps", "data": "Data & ML", "databases": "Databases",
                  "devops": "Ops & Cloud", "gamedev": "Game Development", "security": "Security",
                  "embedded": "Embedded & Hardware", "scicomp": "Scientific Computing"}
SHIFT_KINDS = {"day": (8, 0), "late": (15, 30), "night": (23, 0)}    # local start; every shift 8 paid hours
CORRECTED_WEEK = (dt.date(2026, 5, 4), dt.date(2026, 5, 10))
HOLIDAYS_ON = {dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 4, 3), dt.date(2026, 5, 18),
               dt.date(2026, 7, 1), dt.date(2026, 8, 3), dt.date(2026, 9, 7)}


class Moderator:
    pass


def paid_team():
    """The moderators on the paid team during 2026: employee number, contract (full or part time), shift kind, the
    site they were assigned to on each day, and their worked shifts from January to September 2026."""
    r = K.rng("team")
    mods = []
    num = 4100 + int(r.integers(10, 60))
    for site in K.SITES:
        fte = ALLOC_2026[site]
        n_full = int(math.floor(fte))
        parts = int(round((fte - n_full) / 0.5))
        for k in range(n_full + parts):
            m = Moderator()
            num += int(r.integers(3, 29))
            m.emp = "QM%05d" % num
            m.home = site
            m.contract = 1.0 if k < n_full else 0.5
            m.kind = ["day", "late", "night"][k % 3]
            m.moves = []
            mods.append(m)
    # the six moves: the first full-time moderator of each source site moves
    for src, dst, eff in MOVES:
        cand = [m for m in mods if m.home == src and m.contract == 1.0 and not m.moves]
        m = cand[0]
        m.moves.append((eff, dst))
    for m in mods:
        m.assign = [(dt.date(2023, 1, 1) if True else None, m.home)]
        for eff, dst in m.moves:
            m.assign.append((eff, dst))
    # shifts
    start, end = dt.date(2026, 1, 1), K.HIST_END
    for m in mods:
        rr = K.rng("shifts", m.emp)
        week_days = [0, 1, 2, 3, 4] if m.contract == 1.0 else [0, 2, 4]
        if m.kind == "night":
            week_days = [6, 0, 1, 2, 3] if m.contract == 1.0 else [6, 1, 3]
        leave = set()
        for _ in range(3):   # three one-week blocks of leave, not in the corrected week
            while True:
                w0 = start + dt.timedelta(days=int(rr.integers(14, 250)))
                w0 -= dt.timedelta(days=w0.weekday())
                if not (w0 <= CORRECTED_WEEK[1] and w0 + dt.timedelta(days=6) >= CORRECTED_WEEK[0]):
                    break
            for k in range(7):
                leave.add(w0 + dt.timedelta(days=k))
        m.shifts = []
        d = start
        while d <= end:
            if d.weekday() in week_days and d not in leave and d not in HOLIDAYS_ON:
                if rr.random() > 0.035:          # sick days and swaps
                    h0, mi = SHIFT_KINDS[m.kind]
                    st = dt.datetime(d.year, d.month, d.day, h0, mi)
                    hrs = 8.0
                    if rr.random() < 0.06:
                        hrs = float(rr.choice([4.0, 6.0, 9.0, 10.0]))   # short days and overtime
                    m.shifts.append(dict(day=d, start=st, end=st + dt.timedelta(hours=hrs + 0.5), hours=hrs))
            d += dt.timedelta(days=1)
    # every quarter-end night must be worked by someone on a night pattern at every site with a night moderator
    return mods


def site_on(m, d):
    s = m.home
    for eff, dst in m.assign[1:]:
        if d >= eff:
            s = dst
    return s


def corrected_lines(mods):
    """The May corrections: eight moderators' week of 4 to 10 May re-sent after a payroll query. Returns, per
    moderator employee number, the corrected hours of each shift in the week (some shifts change by an hour or two)."""
    r = K.rng("corrections")
    pick = [m for m in mods if any(CORRECTED_WEEK[0] <= s["day"] <= CORRECTED_WEEK[1] for s in m.shifts)]
    pick = sorted(pick, key=lambda m: m.emp)
    idx = sorted(r.choice(len(pick), size=8, replace=False))
    out = {}
    for i in idx:
        m = pick[int(i)]
        fix = {}
        for s in m.shifts:
            if CORRECTED_WEEK[0] <= s["day"] <= CORRECTED_WEEK[1]:
                fix[s["day"]] = s["hours"] + float(r.choice([1.0, -1.0, 1.0, 0.0, 2.0]))
        out[m.emp] = fix
    return out


# ------------------------------------------------------------------------------------------------- Q3 flags
REASONS = [("spam", 0.31), ("rude_or_abusive", 0.08), ("not_an_answer", 0.22), ("very_low_quality", 0.14),
           ("ai_generated", 0.11), ("plagiarism", 0.03), ("needs_moderator", 0.11)]
# median hours to a paid moderator's first action in Q3 2026, by site and month (the three short sites slower)
MEDIAN_H = {"web": 3.1, "mobile": 3.4, "data": 3.0, "databases": 3.3, "devops": 3.2, "gamedev": 3.6,
            "security": 6.2, "embedded": 6.8, "scicomp": 7.4}
MONTH_DRIFT = {7: 0.94, 8: 1.00, 9: 1.07}
REVIEW_SHARE = 0.042
ESCALATE_H = 90.0
TOOL_PULL = dt.datetime(2026, 10, 8, 5, 38, 21)     # the moderator tool's export run, UTC
CLOSED_SHARE = 0.062
Q3 = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))


def flags_q3(W, mods):
    """Every flag raised in July to September 2026: the daily counts are the world's (the summary the main call reads
    is built from the same counts), each flag's raise time, first action, decision review and export time."""
    first_id = 51000000 + int(K.rng("flagbase").integers(1000, 90000))
    rows, reviews = [], []
    fid = first_id
    q3_days = [d for d in K.days(*Q3)]
    by_site_mods = {}
    for d in q3_days:
        for s in K.SITES:
            by_site_mods.setdefault((s, d), [m.emp for m in mods if site_on(m, d) == s])
    for d in q3_days:
        di = W.day_index[d]
        day_rows = []
        for s in K.SITES:
            S = W.sites[s]
            n = int(S.flags[di])
            r = K.rng("flagday", s, d.isoformat())
            n_closed = int(S.flag_closed[di])
            secs = np.sort(r.choice(86400, size=n, replace=True)) if n else []
            kinds = np.array([0] * n)
            closed_idx = set(r.choice(n, size=n_closed, replace=False).tolist()) if n_closed else set()
            reasons = r.choice(len(REASONS), size=n, p=[p for _, p in REASONS]) if n else []
            for j in range(n):
                raised = dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(secs[j]))
                rec = dict(site=s, raised=raised, reason=REASONS[int(reasons[j])][0],
                           post_type="answer" if r.random() < 0.62 else ("question" if r.random() < 0.8 else "comment"),
                           post_id=int(r.integers(78_000_000, 79_400_000)),
                           flagger=int(r.integers(120_000, 31_000_000)))
                if j in closed_idx:
                    rec["first"] = raised + dt.timedelta(minutes=float(r.exponential(85.0)) + 1.0)
                    rec["by"] = "system"
                    rec["outcome"] = "closed_post_deleted"
                    rec["review"] = None
                else:
                    med = MEDIAN_H[s] * MONTH_DRIFT[d.month]
                    hrs = math.exp(math.log(med) + float(r.normal(0.0, 1.05)))
                    if hrs > ESCALATE_H:         # a flag left this long is escalated to the shift lead and taken
                        hrs = ESCALATE_H + hrs % 7.0
                    rec["first"] = raised + dt.timedelta(hours=hrs)
                    pool = by_site_mods[(s, d)] or by_site_mods[(s, d)]
                    rec["by"] = pool[int(r.integers(0, len(pool)))] if pool else "QM04999"
                    rec["outcome"] = "helpful" if r.random() < 0.83 else "declined"
                    if r.random() < REVIEW_SHARE:
                        opened = rec["first"] + dt.timedelta(hours=float(r.uniform(6.0, 60.0)))
                        closed = opened + dt.timedelta(hours=float(r.uniform(18.0, 110.0)))
                        final = rec["outcome"]
                        if r.random() < 0.31:
                            final = "declined" if final == "helpful" else "helpful"
                        rec["review"] = dict(opened=opened, closed=closed, first_outcome=rec["outcome"], final=final,
                                             why=str(r.choice(["flagger appeal", "post owner appeal", "quality sample"],
                                                              p=[0.38, 0.27, 0.35])),
                                             reviewer=None)
                        rec["outcome"] = final
                    else:
                        rec["review"] = None
                day_rows.append(rec)
        day_rows.sort(key=lambda x: (x["raised"], x["site"]))
        for rec in day_rows:
            fid += int(1 + (rec["post_id"] % 3 == 0))
            rec["flag_id"] = fid
            rows.append(rec)
            if rec["review"]:
                reviews.append(rec)
    # reviewers are senior moderators: the longest-serving full-time moderator at each of three sites
    seniors = [m.emp for m in sorted(mods, key=lambda m: m.emp)[:3]]
    for k, rec in enumerate(reviews):
        rec["review"]["reviewer"] = seniors[k % 3]
    # the export ran on the morning of 8 October: a review opened after it does not exist yet, and one still open has
    # no close, no final outcome and has not re-marked its flag
    for rec in reviews:
        R = rec["review"]
        if R["opened"] > TOOL_PULL:
            rec["review"] = None
            rec["outcome"] = R["first_outcome"]
        elif R["closed"] > TOOL_PULL:
            R["closed"] = None
            R["final"] = None
            R["reviewer"] = None
            rec["outcome"] = R["first_outcome"]
    return rows


# ------------------------------------------------------------------------------------------------- question moves
# per destination (the old system's site), the share of the questions living there now that were asked on another
# site and moved in, and where they came from
IN_SHARE = {"web": 0.0056, "mobile": 0.0068, "data": 0.0060, "databases": 0.0064, "devops": 0.0062,
            "gamedev": 0.0060, "graphics": 0.0072, "security": 0.0067, "embedded": 0.0065, "scicomp": 0.0070}
IN_FROM = {
    "web": [("mobile", 0.36), ("devops", 0.22), ("security", 0.20), ("data", 0.12), ("gamedev", 0.10)],
    "mobile": [("web", 0.62), ("gamedev", 0.20), ("embedded", 0.18)],
    "data": [("databases", 0.44), ("scicomp", 0.36), ("web", 0.20)],
    "databases": [("data", 0.50), ("devops", 0.50)],
    "devops": [("databases", 0.36), ("security", 0.34), ("web", 0.30)],
    "gamedev": [("graphics", 0.48), ("web", 0.30), ("mobile", 0.22)],
    "graphics": [("gamedev", 0.68), ("scicomp", 0.32)],
    "security": [("devops", 0.55), ("web", 0.45)],
    "embedded": [("scicomp", 0.42), ("devops", 0.30), ("mobile", 0.28)],
    "scicomp": [("data", 0.56), ("embedded", 0.30), ("graphics", 0.14)],
}


def question_moves(W):
    """Questions moved between sites from 2021 to 2023. The world's daily questions are the questions that live on
    each site now, by the day first asked (the posts warehouse's basis); a moved question was asked on another site and
    lives on the site it moved to, so the moves are drawn into each destination from the questions living there."""
    r = K.rng("moves")
    moves = []
    for d in K.days(K.D0, K.OLD_END):
        di = W.day_index[d]
        for s in K.SITES:
            live = W.sites[s].q[di]
            dests = [(s, 1.0)]
            if s == "gamedev" and d < K.MERGER:
                dests = [("gamedev", 1.0 - K.GRAPHICS_SHARE), ("graphics", K.GRAPHICS_SHARE)]
            for dst, share in dests:
                k = int(r.poisson(live * share * IN_SHARE[dst]))
                srcs = [x for x in IN_FROM[dst] if not (x[0] == "graphics" and d >= K.MERGER)]
                tot = sum(p for _, p in srcs)
                for _ in range(k):
                    src = srcs[int(r.choice(len(srcs), p=[p / tot for _, p in srcs]))][0]
                    u = r.random()
                    lag = 0 if u < 0.58 else (int(r.integers(1, 4)) if u < 0.89 else int(r.integers(4, 46)))
                    t_ask = dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(r.integers(0, 86400)))
                    t_move = t_ask + dt.timedelta(days=lag, seconds=int(r.integers(1800, 30000)))
                    moves.append(dict(src=src, dst=dst, live=s, asked=t_ask, moved=t_move))
    moves.sort(key=lambda m: (m["asked"], m["src"]))
    qid = 40_000_000 + int(r.integers(1000, 50000))
    for m in moves:
        qid += int(r.integers(30, 260))
        m["qid_old"] = qid
    moves.sort(key=lambda m: (m["moved"], m["qid_old"]))
    nid = 52_000_000 + int(r.integers(1000, 9000))
    for m in moves:
        nid += int(r.integers(1, 9))
        m["qid_new"] = nid
    return moves
