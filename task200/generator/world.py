"""The clean truth: Brackenford Airport's screeners, their shifts, every screen session, every threat image
projection with its true outcome model, every tray reject and search, and every certification sitting.

Nothing here is written to target/. pack.py writes the organisation's exports from these frames, with the mess
its systems really produce; solve.py reads only the exports."""
import datetime as dt
import heapq
import math
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import params as P

LONDON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc


def _rng(tag):
    return np.random.default_rng([P.SEED, sum(ord(c) * (i + 7) for i, c in enumerate(tag))])


def expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def logit(p):
    return math.log(p / (1 - p))


# ----------------------------------------------------------------------------------------------- people
def people():
    r = _rng("people")
    rows = []
    staff_nos = r.choice(np.arange(20150, 48990), size=200, replace=False)
    badges = r.choice(np.arange(1104, 9987), size=200, replace=False)
    logins = r.choice(np.arange(102, 2999), size=200, replace=False)
    opnos = r.choice(np.arange(104, 989), size=200, replace=False)
    k = 0
    for t in P.TEAMS:
        n_now, n_new, n_left = P.SIZE[t], P.STARTERS_2026[t], P.LEAVERS[t]
        for j in range(n_now + n_left):
            leaver = j >= n_now
            starter = (not leaver) and j >= n_now - n_new
            if starter:
                start = dt.date(2026, 1, 12) + dt.timedelta(days=int(r.integers(0, 230)))
            else:
                # most members long in post; a few joined during the CT years
                y = r.random()
                if y < 0.72:
                    start = dt.date(2008, 3, 1) + dt.timedelta(days=int(r.integers(0, 5300)))
                else:
                    start = dt.date(2023, 2, 1) + dt.timedelta(days=int(r.integers(0, 900)))
            left = None
            if leaver:
                left = dt.date(2024, 7, 1) + dt.timedelta(days=int(r.integers(0, 880)))
                if left <= start + dt.timedelta(days=120):
                    left = start + dt.timedelta(days=150)
            skill = logit(P.NOVEL[t]) + r.normal(0, P.SKILL_SD)
            rows.append(dict(staff_no=int(staff_nos[k]), badge=int(badges[k]), login="SCR%04d" % int(logins[k]),
                             op_no=int(opnos[k]),
                             team_end=t, start=start, left=left, skill=skill,
                             supervisor=(j == 0), contract="PT" if r.random() < 0.14 else "FT"))
            k += 1
    df = pd.DataFrame(rows)
    # team moves during 2026: an Arden and a Dene member swap teams in April, an Esk member joins Fell in June
    df["team_before"] = df.team_end
    df["move_date"] = pd.NaT
    cur = df[df.left.isna() & ~df.supervisor & (df.start < dt.date(2025, 6, 1))]
    a = cur[cur.team_end == "Arden"].index[3]
    d = cur[cur.team_end == "Dene"].index[2]
    e = cur[cur.team_end == "Cleve"].index[4]     # a Cleve member at year end who was in Esk until June
    df.loc[a, ["team_before", "team_end"]] = ["Arden", "Dene"]
    df.loc[d, ["team_before", "team_end"]] = ["Dene", "Arden"]
    df.loc[e, "team_before"] = "Esk"
    df.loc[a, "move_date"] = pd.Timestamp("2026-04-06")
    df.loc[d, "move_date"] = pd.Timestamp("2026-04-06")
    df.loc[e, "move_date"] = pd.Timestamp("2026-06-15")
    # ID badges replaced during 2026 (lost or damaged): the old number stops on the day the new one is issued
    df["old_badge"] = pd.NA
    df["badge_change"] = pd.NaT
    df["badge_reason"] = ""
    spare = [int(b) for b in badges[k:k + 10]]
    pick = [cur[cur.team_end == "Fell"].index[1], cur[cur.team_end == "Fell"].index[6], cur[cur.team_end == "Esk"].index[5],
            cur[cur.team_end == "Brook"].index[7]]
    when = ["2026-03-17", "2026-08-04", "2026-05-26", "2026-10-13"]
    why = ["REPLACEMENT (LOST)", "REPLACEMENT (DAMAGED)", "REPLACEMENT (LOST)", "REPLACEMENT (LOST)"]
    for i, (pid, w, y) in enumerate(zip(pick, when, why)):
        df.loc[pid, "old_badge"] = int(df.loc[pid, "badge"])
        df.loc[pid, "badge"] = spare[i]
        df.loc[pid, "badge_change"] = pd.Timestamp(w)
        df.loc[pid, "badge_reason"] = y
    # skill belongs to the person: the movers keep the skill drawn with their year-end team
    return df.reset_index(drop=True)


def badge_at(pp, pid, when):
    """the ID badge a person tapped with on a date"""
    row = pp.loc[pid]
    if pd.notna(row.badge_change) and pd.Timestamp(when).tz_localize(None) < row.badge_change:
        return int(row.old_badge)
    return int(row.badge)


def team_on(person, day):
    if pd.notna(person.move_date) and pd.Timestamp(day) < person.move_date:
        return person.team_before
    return person.team_end


# ----------------------------------------------------------------------------------------------- shifts and sessions
def _workday(team, day):
    return (day.toordinal() + P.TEAM_OFFSET[team]) % P.CYCLE < 4


def sessions(pp):
    """Every screen session, as the operator really sat at the screen (start and end UTC), with the area and screen.

    Central Search: twelve remote screening workstations serving eight CT lanes. Pier B: three legacy X-ray screens.
    One operator per screen at a time; a screener rests at least 25 minutes between sessions."""
    r = _rng("sessions")
    rows = []
    day = min(P.CT_START, P.PB_START)
    persons = list(pp.itertuples(index=True))
    leave = {}
    for pr in persons:
        leave[pr.Index] = set()
    for y in (2023, 2024, 2025, 2026):
        for pr in persons:
            n = int(P.LEAVE_DAYS + r.integers(-6, 7))
            first = dt.date(y, 1, 1).toordinal()
            last = dt.date(y, 12, 31).toordinal()
            for o in r.choice(np.arange(first, last + 1), size=n, replace=False):
                leave[pr.Index].add(int(o))
    while day <= P.END:
        cyc = (day.toordinal() + 3) % P.CYCLE
        for area in ("C", "B"):
            if (area == "B" and day < P.PB_START) or (area == "C" and day < P.CT_START):
                continue
            screens = ["WS%02d" % i for i in range(1, 13)] if area == "C" else ["PB1", "PB2", "PB3"]
            free = {s: 0.0 for s in screens}         # minutes after local midnight when the screen is next free
            crew = []
            for pr in persons:
                if day < pr.start or (pr.left is not None and day >= pr.left):
                    continue
                if day.toordinal() in leave[pr.Index]:
                    continue
                t = team_on(pr, day)
                if not _workday(t, day):
                    continue
                at_b = t == "Fell"
                crew.append((pr, t, at_b))
            # Pier B is Fell's alone (P.ESK_PIERB_PER_DAY is zero): no other team screens on the legacy library
            esk = [c for c in crew if c[1] == "Esk"] if P.ESK_PIERB_PER_DAY[1] > 0 else []
            if esk:
                k = int(r.integers(P.ESK_PIERB_PER_DAY[0], P.ESK_PIERB_PER_DAY[1] + 1))
                pick = set(int(i) for i in r.choice(len(esk), size=min(k, len(esk)), replace=False))
                crew = [(c[0], c[1], True) if (c[1] == "Esk" and esk.index(c) in pick) else c for c in crew]
            here = [c for c in crew if c[2] == (area == "B")]
            close = 15 * 60 + 30 if area == "B" else 22 * 60
            heap = []
            for pr, t, _b in here:
                if area == "B":
                    shift0 = 5 * 60 + float(r.integers(-10, 11))
                else:
                    early = (cyc + P.TEAM_OFFSET[t]) % 2 == 0
                    shift0 = (3 * 60 + 40 if early else 12 * 60 + 30) + float(r.integers(-15, 16))
                n = int(r.integers(P.SESSIONS_PER_SHIFT[0], P.SESSIONS_PER_SHIFT[1] + 1))
                if pr.supervisor:
                    n = int(r.integers(3, 5))
                heapq.heappush(heap, (shift0 + float(r.uniform(8, 45)), pr.Index, t, n))
            while heap:
                want, pid, t, left_n = heapq.heappop(heap)
                order = sorted(screens, key=lambda s_: (free[s_] > want, -free[s_] if free[s_] <= want else free[s_], s_))
                s_ = order[0]
                st = max(want, free[s_] + float(r.uniform(0.2, 2.5)))
                dur = float(r.normal(*P.SESSION_MIN))
                while dur < 9 or dur > 20:
                    dur = float(r.normal(*P.SESSION_MIN))
                en = st + dur
                if en > close:
                    continue
                free[s_] = en
                rows.append((pid, t, area, s_, day, st, en))
                if left_n > 1:
                    heapq.heappush(heap, (en + float(np.clip(r.normal(*P.GAP_MIN), 25, 80)), pid, t, left_n - 1))
        day += dt.timedelta(days=1)
    df = pd.DataFrame(rows, columns=["pid", "team_then", "area", "screen", "day", "m0", "m1"])
    base = pd.to_datetime(df.day)
    # wall-clock local times (no session runs between 00:00 and 03:00, so neither clock change is ambiguous here)
    for col, m in (("start", df.m0), ("end", df.m1)):
        local = (base + pd.to_timedelta(m, unit="m")).dt.round("s")
        df[col] = local.dt.tz_localize(LONDON, ambiguous="raise", nonexistent="raise").dt.tz_convert(UTC)
    df = df.sort_values(["start", "screen"]).reset_index(drop=True)
    df["sid"] = np.arange(len(df))
    # Central: each workstation's queue serves one lane, and for part of some sessions a second lane as well
    rl = _rng("lanes")
    isc = (df.area == "C").values
    l1 = rl.integers(1, 9, len(df))
    df["lane1"] = np.where(isc, ["C%d" % v for v in l1], df.screen.values)
    mux = isc & (rl.random(len(df)) < P.MULTIPLEX_P)
    step = rl.integers(1, 8, len(df))
    df["lane2"] = np.where(mux, ["C%d" % (1 + (a - 1 + b) % 8) for a, b in zip(l1, step)], "")
    span = (df.end - df.start).dt.total_seconds().values
    a = rl.uniform(0.0, 0.45, len(df))
    b = rl.uniform(0.0, 0.25, len(df))
    df["mux_on"] = df.start + pd.to_timedelta(np.round(span * a), unit="s")
    df["mux_off"] = df.end - pd.to_timedelta(np.round(span * b), unit="s")
    df["mux"] = mux
    return df


def lane_at(ss_rows, ts, r):
    """the lane a projection or a reject came from: the queue's own lane, or inside the two-lane window either lane"""
    in2 = ss_rows.mux.values & (ts.values >= ss_rows.mux_on.values) & (ts.values < ss_rows.mux_off.values)
    pick2 = in2 & (r.random(len(ts)) < 0.5)
    return np.where(pick2, ss_rows.lane2.values, ss_rows.lane1.values)


# ----------------------------------------------------------------------------------------------- libraries
def libraries():
    r = _rng("library")
    ct_ids = r.choice(np.arange(10000, 99999), size=P.N_CT_IMAGES, replace=False)
    both = r.choice(np.arange(1000, 4999), size=P.N_PB_IMAGES + P.N_PB_ADD, replace=False)
    pb_ids, add_ids = both[:P.N_PB_IMAGES], both[P.N_PB_IMAGES:]
    cats = [c for c, _ in P.CATEGORY_MIX]
    w = [p for _, p in P.CATEGORY_MIX]
    out = []
    for area, ids, loaded in (("C", ct_ids, P.CT_START), ("B", pb_ids, P.PB_START), ("B", add_ids, P.PB_ADD)):
        c = r.choice(cats, size=len(ids), p=w)
        d = r.normal(0, P.DIFF_SD, size=len(ids))
        for i, cc, dd in zip(ids, c, d):
            code = ("CT6-%05d" % i) if area == "C" else ("PB-%04d" % i)
            out.append((area, code, cc, float(dd + P.CATEGORY[cc]), loaded))
    return pd.DataFrame(out, columns=["area", "image", "category", "difficulty", "loaded"])


# ----------------------------------------------------------------------------------------------- projections
def projections(pp, ss, lib):
    """Threat image projections inside each real session, their true outcome from the member's skill, the image's
    difficulty and how many times the member had met that image before."""
    r = _rng("tip")
    dur_h = (ss.end - ss.start).dt.total_seconds() / 3600.0
    n = r.poisson(P.TIP_PER_HOUR * dur_h.values)
    idx = np.repeat(ss.index.values, n)
    tp = ss.loc[idx, ["sid", "pid", "team_then", "area", "screen", "day", "start", "end", "lane1", "lane2", "mux",
                      "mux_on", "mux_off"]].reset_index(drop=True)
    frac = r.uniform(0.02, 0.98, len(tp))
    tp["ts"] = (tp.start + pd.to_timedelta(frac * (tp.end - tp.start).dt.total_seconds(), unit="s")).dt.round("s")
    tp["lane"] = lane_at(tp, tp.ts, r)
    # the image: drawn from the library loaded on that area's screens on that date
    ct = lib[lib.area == "C"].reset_index(drop=True)
    pb0 = lib[(lib.area == "B") & (lib.loaded == P.PB_START)].reset_index(drop=True)
    pball = lib[lib.area == "B"].reset_index(drop=True)
    img = np.empty(len(tp), dtype=object)
    isc = (tp.area == "C").values
    img[isc] = ct.image.values[r.integers(0, len(ct), isc.sum())]
    late = (~isc) & (pd.to_datetime(tp.day).values >= np.datetime64(P.PB_ADD))
    early = (~isc) & ~late
    img[early] = pb0.image.values[r.integers(0, len(pb0), early.sum())]
    img[late] = pball.image.values[r.integers(0, len(pball), late.sum())]
    tp["image"] = img
    tp = tp.merge(lib[["image", "category", "difficulty"]], on="image", how="left")
    tp["cancelled"] = r.random(len(tp)) < P.CANCEL_P
    tp = tp.sort_values(["ts", "pid", "image"]).reset_index(drop=True)
    shown = ~tp.cancelled
    tp["k"] = -1
    tp.loc[shown, "k"] = tp[shown].groupby(["pid", "image"]).cumcount().values
    skill = pp.skill.values[tp.pid.values]
    f = np.where(tp.k.values > 0, 1 - P.FAM_HALF ** tp.k.values.clip(min=0), 0.0)
    eta = skill - tp.difficulty.values + P.FAMILIARITY * f
    tp["p_hit"] = expit(eta)
    tp["f"] = f
    tp["rt_noise"] = r.normal(0, 0.38, len(tp))
    return tp


def outcomes(tp, salt):
    """the outcome of every shown projection, drawn on its own stream so the world's records stay fixed"""
    r = _rng("outcome:%d" % salt)
    u = r.random(len(tp))
    out = tp.copy()
    out["hit"] = (~out.cancelled).values & (u < out.p_hit.values)
    base = np.where(out.area.values == "C", 4.4, 3.9)
    rt = np.exp(np.log(base) - 0.10 * out.f.values + out.rt_noise.values)
    out["rt"] = np.where(out.hit.values, np.clip(rt, 0.9, 19.5), np.nan)
    return out


ORDER = ["Fell", "Brook", "Dene", "Esk", "Arden", "Cleve"]


def _edge_pct(x):
    v = 100.0 * x
    return 0.5 - abs(v - round(v))


def outcome_ok(pp, tp):
    """the design's own conditions on the drawn outcomes: the first-meeting order and its margins, the every-
    projection score with Brook lowest and Fell in the middle, and every printed per-cent figure clear of its edge"""
    cur = pp[pp.left.isna()]
    team_of = dict(zip(cur.index, cur.team_end))
    t = tp[(tp.ts.dt.tz_convert(LONDON).dt.year == 2026) & ~tp.cancelled & tp.pid.isin(cur.index)]
    team = t.pid.map(team_of)
    first = t[t.k == 0].hit.groupby(team[t.k == 0]).mean()
    raw = t.hit.groupby(team).mean()
    met = t[t.k > 0].hit.groupby(team[t.k > 0]).mean()
    rep = (t.k > 0).groupby(team).mean()
    o = list(first.sort_values().index)
    gaps = np.diff(first.sort_values().values)
    rr = list(raw.sort_values().index)
    figs = list(first.values) + list(raw.values) + [met["Fell"]]
    return (o == ORDER and gaps.min() >= 0.03 and gaps[0] >= 0.045 and rr[0] == "Brook" and rr.index("Fell") in (2, 3)
            and min(_edge_pct(x) for x in figs) >= 0.06 and raw.sort_values().iloc[1] - raw.min() >= 0.03)


# ----------------------------------------------------------------------------------------------- rejects and searches
def rejects(pp, ss):
    """Trays an operator sent to the search position, with the search that followed."""
    r = _rng("rejects")
    s26 = ss[pd.to_datetime(ss.day).dt.year == 2026]
    dur_h = (s26.end - s26.start).dt.total_seconds() / 3600.0
    rate = s26.team_then.map(P.REJECT_PER_HOUR).values
    n = r.poisson(rate * dur_h.values)
    idx = np.repeat(s26.index.values, n)
    rj = ss.loc[idx, ["sid", "pid", "team_then", "area", "screen", "day", "start", "end", "lane1", "lane2", "mux",
                      "mux_on", "mux_off"]].reset_index(drop=True)
    frac = r.uniform(0.02, 0.98, len(rj))
    rj["ts"] = (rj.start + pd.to_timedelta(frac * (rj.end - rj.start).dt.total_seconds(), unit="s")).dt.round("s")
    rj["lane"] = lane_at(rj, rj.ts, r)
    trays_c = ["T%04d" % v for v in r.choice(np.arange(1000, 9999), 540, replace=False)]
    trays_b = ["B%03d" % v for v in r.choice(np.arange(100, 999), 170, replace=False)]
    rj["tray"] = [trays_c[i] if a == "C" else trays_b[j] for a, i, j in
                  zip(rj.area, r.integers(0, 540, len(rj)), r.integers(0, 170, len(rj)))]
    # queue at the search position, then the search; a tray is not rejected again before its search starts
    q = np.exp(np.log(150.0) + r.normal(0, 0.62, len(rj)))         # seconds waiting
    q = np.clip(q, 25, 1100)
    rj["search_start"] = (rj.ts + pd.to_timedelta(q, unit="s")).dt.round("s")
    rj["search_end"] = (rj.search_start + pd.to_timedelta(r.uniform(110, 400, len(rj)), unit="s")).dt.round("s")
    u = r.random(len(rj))
    rj["outcome"] = np.where(u < P.FIND_SHARE * 0.55, "PROHIBITED", np.where(u < P.FIND_SHARE, "RESTRICTED", "CLEAR"))
    rj = rj.sort_values(["ts", "tray"]).reset_index(drop=True)
    # a physical tray cannot be in two searches at once: drop the later reject when the same tray is still queued
    keep = np.ones(len(rj), dtype=bool)
    busy = {}
    for i, (tr, a, t0, t1) in enumerate(zip(rj.tray, rj.area, rj.ts, rj.search_end)):
        key = (a, tr)
        if key in busy and t0 <= busy[key] + pd.Timedelta(seconds=40):
            keep[i] = False
            continue
        busy[key] = t1
    rj = rj[keep].reset_index(drop=True)
    rj["search_id"] = ["S%06d" % v for v in (r.choice(np.arange(100000, 999999), len(rj), replace=False))]
    return rj


# ----------------------------------------------------------------------------------------------- certification
def assessments(pp):
    """Every image interpretation assessment sitting a screener took, and the external centre's certificates."""
    r = _rng("assess")
    rows, ext = [], []
    # in every team one or two long-serving members were last recertified at the assessment centre in late spring
    # 2024, and the centre's paperwork reached the LMS after the end of June
    forced = {}
    for t in P.TEAMS:
        pool = pp[(pp.team_end == t) & pp.left.isna() & (pp.start < dt.date(2020, 6, 1))].index.tolist()
        for pid in r.choice(pool, size=int(r.integers(1, 3)), replace=False):
            forced[int(pid)] = dt.date(2024, 4, 29) + dt.timedelta(days=int(r.integers(0, 55)))
    for pr in pp.itertuples(index=True):
        # the current certificate cycle: a certification at hire, then every three years
        when = pr.start + dt.timedelta(days=int(r.integers(20, 75)))
        if pr.Index in forced:
            target = forced[pr.Index]
            k = 0
            while target - dt.timedelta(days=int(365.25 * P.CERT_YEARS) * (k + 1)) > pr.start + dt.timedelta(days=20):
                k += 1
            when = target - dt.timedelta(days=int(365.25 * P.CERT_YEARS) * k)
        while True:
            is_target = pr.Index in forced and when == forced[pr.Index]
            external = is_target or ((when > pr.start + dt.timedelta(days=200)) and r.random() < P.EXTERNAL_P)
            # no certification sits within a few days either side of the end of June 2024
            if not is_target and dt.date(2024, 6, 26) <= when <= dt.date(2024, 7, 6):
                when = when + dt.timedelta(days=12)
            if not external and pr.Index not in forced and r.random() < 0.09:
                rows.append((pr.Index, "IIC", when, "FAIL", None))
                when = when + dt.timedelta(days=int(r.integers(9, 30)))
            if external:
                cert = "IIC-%06d" % int(r.integers(100000, 999999))
                lag = int(r.integers(P.ENTRY_LAG[0], P.ENTRY_LAG[1] + 1))
                if is_target:
                    lag = max(lag, (dt.date(2024, 7, 2) - when).days + int(r.integers(2, 16)))
                ext.append((pr.Index, cert, when, when + dt.timedelta(days=lag)))
                rows.append((pr.Index, "EXT-IIC", when + dt.timedelta(days=lag), "PASS", cert))
            else:
                rows.append((pr.Index, "IIC", when, "PASS", None))
            if is_target:
                break
            if pr.Index in forced:
                nxt = when + dt.timedelta(days=int(365.25 * P.CERT_YEARS))
                when = nxt
                continue
            nxt = when + dt.timedelta(days=int(365.25 * P.CERT_YEARS) - int(r.integers(5, 120)))
            if nxt > dt.date(2026, 12, 20):
                break
            when = nxt
        # the annual refresher, which renews nothing
        y0 = max(pr.start.year + 1, 2019)
        for y in range(y0, 2027):
            d = dt.date(y, 1, 1) + dt.timedelta(days=int(r.integers(30, 330)))
            if d >= pr.start and d <= dt.date(2026, 12, 15) and (pr.left is None or d < pr.left):
                rows.append((pr.Index, "IIR", d, "PASS" if r.random() > 0.04 else "FAIL", None))
    # screeners whose certificate runs out in the spring of 2027 can book their renewal at the assessment centre
    # early; two in different teams sat it in early December 2026, and the centre's paperwork reaches the LMS weeks
    # later, after the January export
    r2 = _rng("assess_late")
    latest = {}
    for pid, code, d, res, cert in rows:
        if res == "PASS" and code == "IIC":
            latest[pid] = max(latest.get(pid, d), d)
    for pid, cert, when, keyed in ext:
        latest[pid] = max(latest.get(pid, when), when)
    used = {x[1] for x in ext}
    cand = {}
    for pid, d in sorted(latest.items()):
        exp = d.replace(year=d.year + P.CERT_YEARS)
        if (pid not in forced and pd.isna(pp.loc[pid, "left"]) and not pp.loc[pid, "supervisor"]
                and dt.date(2027, 2, 15) <= exp <= dt.date(2027, 6, 1)):
            cand.setdefault(pp.loc[pid, "team_end"], []).append(pid)
    teams = sorted(cand)
    for t in r2.choice(teams, size=P.EARLY_RENEWALS, replace=False):
        pid = int(r2.choice(cand[t]))
        when = dt.date(2026, 12, 1) + dt.timedelta(days=int(r2.integers(0, 10)))
        lag = int(r2.integers(42, 61))
        cert = "IIC-%06d" % int(r2.integers(100000, 999999))
        while cert in used:
            cert = "IIC-%06d" % int(r2.integers(100000, 999999))
        used.add(cert)
        ext.append((pid, cert, when, when + dt.timedelta(days=lag)))
        rows.append((pid, "EXT-IIC", when + dt.timedelta(days=lag), "PASS", cert))
    a = pd.DataFrame(rows, columns=["pid", "code", "date", "result", "cert_no"])
    e = pd.DataFrame(ext, columns=["pid", "cert_no", "assessed", "keyed"])
    return a, e


def nudge_hours(pp, ss):
    """keep each Central-only team's 2026 screen time clear of a tenth-of-an-hour edge: if a team's total sits within
    36 seconds of one, its last session of the year (a short one, nothing after it at that workstation that day)
    runs two minutes longer"""
    cur = pp[pp.left.isna()]
    team_of = dict(zip(cur.index, cur.team_end))
    for t in ("Arden", "Brook", "Cleve", "Dene"):
        for _ in range(3):
            m = ss[(pd.to_datetime(ss.day).dt.year == 2026) & (ss.area == "C") & ss.pid.map(team_of).eq(t)]
            h = (m.end - m.start).dt.total_seconds().sum() / 3600.0
            if 0.05 - abs(h - round(h, 1)) >= 0.01:
                break
            for i in m.sort_values("end", ascending=False).index:
                row = ss.loc[i]
                if (row.end - row.start).total_seconds() > 17 * 60:
                    continue
                later = ss[(ss.screen == row.screen) & (ss.day == row.day) & (ss.start > row.start)]
                if len(later) and (later.start.min() - row.end).total_seconds() < 300:
                    continue
                ss.loc[i, "end"] = row.end + pd.Timedelta(seconds=120)
                if ss.loc[i, "mux"]:
                    ss.loc[i, "mux_off"] = min(ss.loc[i, "mux_off"], ss.loc[i, "end"])
                break
    return ss


def run():
    pp = people()
    ss = nudge_hours(pp, sessions(pp))
    lib = libraries()
    tp0 = projections(pp, ss, lib)
    for salt in range(400):
        tp = outcomes(tp0, salt)
        if outcome_ok(pp, tp):
            break
    else:
        raise AssertionError("no outcome draw meets the design's conditions")
    tp.attrs["salt"] = salt
    rj = rejects(pp, ss)
    a, e = assessments(pp)
    return dict(people=pp, sessions=ss, library=lib, tip=tp, rejects=rj, assess=a, external=e)


if __name__ == "__main__":
    import time
    t0 = time.time()
    W = run()
    print({k: len(v) for k, v in W.items()}, "%.1fs" % (time.time() - t0))
