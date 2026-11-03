"""The 2026 world of Kettle River Research's telephone centre, simulated once from the seed.

Every answered outbound call is drawn with its truth (person or machine, the household's greeting style, the
household's state), the detector's result, and what followed; the inbound switch receives what people and machine
owners do afterwards. The clean truth stays in the returned dict for checks.py and never ships."""
import numpy as np
import pandas as pd

import params as P

CENTRAL = "America/Chicago"
MONTH_PROFILES = {
    "KR-2615": [0.02, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.12, 0.20, 0.24, 0.10, 0.04],
    "KR-2618": [0.11, 0.12, 0.12, 0.11, 0.08, 0.02, 0.01, 0.06, 0.11, 0.11, 0.09, 0.06],
    "KR-2622": [0.16, 0.16, 0.13, 0.07, 0.03, 0.03, 0.03, 0.03, 0.05, 0.07, 0.11, 0.13],
    "KR-2656": [0.10, 0.14, 0.16, 0.16, 0.16, 0.14, 0.10, 0.04, 0, 0, 0, 0],
}


def calling_days(rng):
    days = pd.date_range(f"{P.YEAR}-01-02", f"{P.YEAR}-12-30", freq="D")
    days = days[days.dayofweek < 6]                                   # Monday to Saturday
    closed = {"2026-01-01", "2026-05-25", "2026-07-04", "2026-09-07", "2026-11-26", "2026-12-24", "2026-12-25"}
    return days[~days.strftime("%Y-%m-%d").isin(closed)]


USED = set()
OPEN = set(calling_days(None))


def _numbers(rng, area, used):
    out = []
    for a in area:
        while True:
            e = int(rng.integers(201, 990))
            if e in (555, 911, 411, 611):
                continue
            x = f"{a}{e:03d}{int(rng.integers(0, 10000)):04d}"
            if x not in used:
                used.add(x)
                out.append(x)
                break
    return np.array(out)


def project_frame(rng, spec, k):
    job, name, client, n_ans, m, L, p_imm, p_vm, aband, away = spec
    n_cases = int(n_ans * 0.42)
    first = rng.choice(sum(P.AREA_CODES.values(), []), size=n_cases)
    home = np.array([next(s for s, codes in P.AREA_CODES.items() if c in codes) for c in first])
    phone = _numbers(rng, first, USED)
    states = home.copy()
    moved = rng.random(n_cases) < away
    el_states, el_w = zip(*P.ELSEWHERE)
    states[moved] = rng.choice(el_states, size=moved.sum(), p=np.array(el_w) / sum(el_w))
    long_greet = rng.random(n_cases) < L
    machine_home = rng.random(n_cases) < min(0.85, m * 1.1)          # households whose phone a machine answers often
    case_new = np.array([f"{job[3:]}-{x:06d}" for x in rng.choice(np.arange(100000, 999999), n_cases, replace=False)])
    case_old = np.array([f"C{x:07d}" for x in rng.choice(np.arange(1000000, 9999999), n_cases, replace=False)])
    released = pd.Timestamp(f"{P.YEAR}-01-02") + pd.to_timedelta(rng.integers(0, 300, n_cases), unit="D")
    return pd.DataFrame(dict(job=job, case_new=case_new, case_old=case_old, phone=phone, state=states,
                             home_state=home, moved=moved, long_greet=long_greet, machine_home=machine_home,
                             released=released.normalize()))


def place_calls(rng, spec, frame, days):
    """answered calls for one project: when, to which case, and what the line did"""
    job, name, client, n_ans, m, L, p_imm, p_vm, aband, away = spec
    prof = np.array(MONTH_PROFILES.get(job, [1 / 12] * 12))
    prof = prof / prof.sum()
    months = rng.choice(np.arange(1, 13), size=n_ans, p=prof)
    out_days = []
    for mo in range(1, 13):
        k = (months == mo).sum()
        md = days[days.month == mo]
        if k:
            out_days.append(rng.choice(md, size=k))
    dd = pd.to_datetime(np.concatenate(out_days)) if out_days else pd.to_datetime([])
    dd = pd.Series(dd).sort_values().reset_index(drop=True)
    sat = dd.dt.dayofweek.values == 5
    period = np.where(sat, "weekend", np.where(rng.random(len(dd)) < 0.62, "evening", "day"))
    start_h = np.select([period == "weekend", period == "evening"], [10.0, 16.0], 9.0)
    span_h = np.select([period == "weekend", period == "evening"], [6.0, 4.98], 4.5)
    secs = (start_h + rng.random(len(dd)) * span_h) * 3600
    placed = dd + pd.to_timedelta(np.floor(secs), unit="s")
    case_idx = rng.integers(0, len(frame), size=len(dd))
    df = pd.DataFrame(dict(job=job, placed=placed, period=period, case_idx=case_idx))
    df = df.sort_values(["case_idx", "placed"]).reset_index(drop=True)
    # the dialer never rings a number twice inside four hours: push a second ring to the next day's same slot
    gap = df.groupby("case_idx")["placed"].diff()
    clash = gap.notna() & (gap < pd.Timedelta(hours=4))
    df.loc[clash, "placed"] = df.loc[clash, "placed"] + pd.Timedelta(days=1)
    df = df[df["placed"].dt.year == P.YEAR]
    df["placed"] = df["placed"].where(df["placed"].dt.dayofweek < 6, df["placed"] + pd.Timedelta(days=1))
    df = df[df["placed"].dt.normalize().isin(days)].sort_values("placed").reset_index(drop=True)   # never on a closed day
    fr = frame.iloc[df["case_idx"].values].reset_index(drop=True)
    n = len(df)
    mach_p = np.where(fr["machine_home"].values, min(0.95, m * 1.3), m * 0.5)
    is_machine = rng.random(n) < mach_p
    q = np.where(fr["long_greet"].values, P.Q_LONG, P.Q_SHORT)
    amd_machine = np.where(is_machine, rng.random(n) < P.P_MACHINE_CLASSED, rng.random(n) < q)
    month_ab = aband * (0.6 + 0.8 * rng.random(12))
    abandoned = (~amd_machine) & (~is_machine) & (rng.random(n) < month_ab[df["placed"].dt.month.values - 1])
    df["phone"] = fr["phone"].values
    df["case_new"] = fr["case_new"].values
    df["case_old"] = fr["case_old"].values
    df["state"] = fr["state"].values
    df["is_machine"] = is_machine
    df["amd_machine"] = amd_machine
    df["abandoned"] = abandoned
    df["p_imm"], df["p_vm"] = p_imm, p_vm
    return df


OUTCOMES = ["COMPLETE", "PARTIAL", "REFUSAL", "CALLBACK", "INELIGIBLE", "LANGUAGE", "HANGUP", "DNC"]
OUT_P = [0.20, 0.04, 0.30, 0.25, 0.06, 0.01, 0.12, 0.02]


def outcomes(rng, df):
    n = len(df)
    out = np.full(n, "", dtype=object)
    out[df["amd_machine"].values] = "AMD_MACHINE"
    out[df["abandoned"].values] = "ABANDONED"
    agent_mach = (~df["amd_machine"].values) & df["is_machine"].values
    out[agent_mach] = "AGENT_MACHINE"
    live = (out == "")
    out[live] = rng.choice(OUTCOMES, size=live.sum(), p=OUT_P)
    df["outcome"] = out
    # one completed interview per case: later rings to a completed case become callbacks the case manager would
    # never place; drop them
    comp = df["outcome"].eq("COMPLETE")
    first_done = df[comp].groupby(["job", "case_new"])["placed"].min().rename("done_at")
    df = df.join(first_done, on=["job", "case_new"])
    df = df[df["done_at"].isna() | (df["placed"] <= df["done_at"])].drop(columns="done_at")
    dup = df["outcome"].eq("COMPLETE") & df.duplicated(["job", "case_new", "outcome"], keep="first")
    df.loc[dup, "outcome"] = "CALLBACK"
    return df.reset_index(drop=True)


APPT_OUT = ["COMPLETE", "PARTIAL", "REFUSAL", "CALLBACK", "HANGUP", "AGENT_MACHINE"]
APPT_P = [0.36, 0.05, 0.14, 0.18, 0.05, 0.22]


def appointments(rng, df, frame):
    """a respondent who asks to be called back on another of the household's lines at a time they name: the
    appointment is dialed by the interviewer in preview mode (no detection, never abandoned) to a number the client's
    sample record does not hold; a second line kept from an earlier home carries that state's area code"""
    cb = df[df["outcome"].eq("CALLBACK") & df["job"].ne(P.ONE_OFF[0])]
    cases = cb.drop_duplicates(["job", "case_new"])
    pick = cases.sample(frac=P.APPT_SHARE, random_state=int(rng.integers(1e9))).sort_values(["job", "case_new"])
    n = len(pick)
    kept = rng.random(n) < P.APPT_KEPT
    codes = np.empty(n, dtype=object)
    home_codes = sum(P.AREA_CODES.values(), [])
    codes[~kept] = rng.choice(home_codes, size=(~kept).sum())
    st = rng.choice(list(P.KEPT_CODES), size=kept.sum(), p=P.KEPT_FROM)
    codes[kept] = [rng.choice(P.KEPT_CODES[s]) for s in st]
    alt = _numbers(rng, codes, USED)
    rows = []
    for k, (_, r) in enumerate(pick.iterrows()):
        n_calls = 1 + int(rng.random() < 0.35)
        day = r["placed"].normalize()
        for j in range(n_calls):
            day = day + pd.Timedelta(days=int(rng.integers(1, 6)))
            while day not in OPEN and day.year == P.YEAR:
                day = day + pd.Timedelta(days=1)
            if day.year != P.YEAR:
                break
            sat = day.dayofweek == 5
            period = "weekend" if sat else "evening"          # "call me after work"
            start_h, span_h = {"weekend": (10.0, 6.0), "evening": (16.0, 4.98), "day": (9.0, 4.5)}[period]
            placed = day + pd.Timedelta(seconds=int((start_h + rng.random() * span_h) * 3600))
            rows.append(dict(job=r["job"], placed=placed, period=period, case_idx=-1, phone=alt[k],
                             case_new=r["case_new"], case_old=r["case_old"], state=r["state"], is_machine=False,
                             amd_machine=False, abandoned=False, p_imm=r["p_imm"], p_vm=r["p_vm"], appt=True))
    ap = pd.DataFrame(rows)
    ap["outcome"] = rng.choice(APPT_OUT, size=len(ap), p=APPT_P)
    ap["is_machine"] = ap["outcome"].eq("AGENT_MACHINE")
    df = pd.concat([df.assign(appt=False), ap], ignore_index=True).sort_values(["placed", "job", "phone"])
    # one completed interview per case, whichever line it was completed on
    comp = df["outcome"].eq("COMPLETE")
    first_done = df[comp].groupby(["job", "case_new"])["placed"].min().rename("done_at")
    df = df.join(first_done, on=["job", "case_new"])
    df = df[df["done_at"].isna() | (df["placed"] <= df["done_at"])].drop(columns="done_at")
    dup = df["outcome"].eq("COMPLETE") & df.duplicated(["job", "case_new", "outcome"], keep="first")
    df.loc[dup, "outcome"] = "CALLBACK"
    return df.reset_index(drop=True)


def late_appointments(rng, df):
    """some respondents name a time after the evening session: the interviewer rings them after 9 pm"""
    ap = np.flatnonzero(df["appt"].values & df["period"].eq("evening").values)
    late = ap[rng.random(len(ap)) < P.APPT_LATE]
    day = df["placed"].values[late].astype("datetime64[D]")
    df.loc[df.index[late], "placed"] = pd.to_datetime(day) + pd.to_timedelta(21 * 3600 + rng.integers(60, 2400, len(late)), unit="s")
    return df


def on_the_hour(placed, states):
    """calls that ring at 8:00:00 or 21:00:00 sharp in the household's own clock"""
    out = np.zeros(len(placed), dtype=bool)
    loc = pd.Series(pd.to_datetime(placed)).dt.tz_localize(CENTRAL)
    st = pd.Series(states).map(P.STATE_TZ).values
    for zone in pd.unique(st):
        ix = np.flatnonzero(st == zone)
        lt = loc.iloc[ix].dt.tz_convert(zone)
        out[ix] = (((lt.dt.hour == 8) | (lt.dt.hour == 21)) & (lt.dt.minute == 0) & (lt.dt.second == 0)).values
    return out


def no_straddle(placed, answered, states):
    """the dialer's pacing never starts a ring in the last seconds before 8:00 or 21:00 in the household's clock and
    has it answered after: such a ring is answered before the hour turns"""
    placed = pd.Series(pd.to_datetime(placed)).reset_index(drop=True)
    answered = pd.Series(pd.to_datetime(answered)).reset_index(drop=True)
    st = pd.Series(states).map(P.STATE_TZ).values
    lp = pd.Series(np.zeros(len(placed)))
    shift_p = np.zeros(len(placed))
    new_ring = (answered - placed).dt.total_seconds().values.copy()
    for zone in pd.unique(st):
        ix = np.flatnonzero(st == zone)
        a = placed.iloc[ix].dt.tz_localize(CENTRAL).dt.tz_convert(zone)
        b = answered.iloc[ix].dt.tz_localize(CENTRAL).dt.tz_convert(zone)
        for h in (8, 21):
            edge = a.dt.normalize() + pd.Timedelta(hours=h)
            hit = ((a < edge) & (b >= edge)).values
            gap = (edge - a).dt.total_seconds().values
            j = ix[hit]
            g = gap[hit]
            shift_p[j] = np.where(g < 2, 2, 0)
            new_ring[j] = g + shift_p[j] - 1
    p2 = placed - pd.to_timedelta(shift_p, unit="s")
    a2 = p2 + pd.to_timedelta(new_ring, unit="s")
    return p2.values, a2.values, (a2 - answered).dt.total_seconds().values


def timings(rng, df):
    n = len(df)
    ring = rng.integers(4, 26, n)
    df["answered"] = df["placed"] + pd.to_timedelta(ring, unit="s")
    talk = np.zeros(n)
    o = df["outcome"].values
    talk = np.select([o == "COMPLETE", o == "PARTIAL", o == "REFUSAL", o == "CALLBACK", o == "INELIGIBLE",
                      o == "LANGUAGE", o == "HANGUP", o == "DNC", o == "AGENT_MACHINE"],
                     [rng.integers(780, 1700, n), rng.integers(300, 900, n), rng.integers(25, 110, n),
                      rng.integers(45, 160, n), rng.integers(60, 240, n), rng.integers(20, 70, n),
                      rng.integers(5, 40, n), rng.integers(20, 80, n), rng.integers(8, 30, n)], 0)
    wrap = np.where(talk > 0, rng.integers(12, 75, n), 0)
    msg = np.where(np.isin(o, ["AMD_MACHINE", "ABANDONED"]), rng.integers(22, 31, n), 0)
    detect = np.where(df["amd_machine"].values, rng.integers(2, 5, n), 2)
    connected = talk > 0
    df["connected"] = df["answered"] + pd.to_timedelta(np.where(connected, detect, 0), unit="s")
    df.loc[~connected, "connected"] = pd.NaT
    df["talk"] = talk.astype(int)
    df["wrap"] = wrap.astype(int)
    df["ended"] = df["answered"] + pd.to_timedelta(detect + talk + msg, unit="s")
    return df


def staff(rng, calls):
    """interviewer shifts per project-day-period, connected calls given to an interviewer on shift"""
    agents = [f"A{x:03d}" for x in range(101, 101 + 160)]
    conn = calls["connected"].notna()
    c = calls[conn].copy()
    c["date"] = c["placed"].dt.normalize()
    shifts = []
    sid = 0
    agent_free = {}
    groups = c.groupby(["date", "period", "job"])
    keys = sorted(groups.groups.keys())
    pair_of = {}
    for (date, period, job) in keys:
        k = len(groups.groups[(date, period, job)])
        need = max(1, int(np.ceil(k / 9.0)))
        for _ in range(need):
            shifts.append(dict(shift=sid, date=date, period=period, jobs=[job]))
            pair_of.setdefault((date, period), []).append(sid)
            sid += 1
    sh = pd.DataFrame(shifts)
    # a fifth of the shifts work a second project the same evening: merge pairs inside a date and period
    for (date, period), ids in pair_of.items():
        ids = [i for i in ids]
        rng.shuffle(ids)
        for a, b in zip(ids[0::2], ids[1::2]):
            if rng.random() < 0.40 and sh.at[a, "jobs"][0] != sh.at[b, "jobs"][0]:
                sh.at[a, "jobs"] = sh.at[a, "jobs"] + sh.at[b, "jobs"]
                sh.at[b, "jobs"] = []
    sh = sh[sh["jobs"].map(len) > 0].reset_index(drop=True)
    sh["shift"] = np.arange(len(sh))
    # interviewers: each takes at most one shift per date and period
    by_dp = {}
    for i, r in sh.iterrows():
        by_dp.setdefault((r["date"], r["period"]), []).append(i)
    agent_col = np.empty(len(sh), dtype=object)
    for (date, period), ids in by_dp.items():
        pool = rng.permutation(agents)
        for j, i in enumerate(ids):
            agent_col[i] = pool[j % len(pool)]
    sh["agent"] = agent_col
    sh["hours"] = np.select([sh["period"] == "weekend", sh["period"] == "evening"], [6.0, 5.0], 4.5)
    sh["hours"] = sh["hours"] + rng.choice([0, 0, 0, 0.25, 0.5, 0.75], len(sh))   # stayed on to finish a case
    # assign each connected call to a shift on its date and period covering its job
    lookup = {}
    for i, r in sh.iterrows():
        for j in r["jobs"]:
            lookup.setdefault((r["date"], r["period"], j), []).append(i)
    pick = np.empty(len(c), dtype=int)
    for t, (d, p_, j) in enumerate(zip(c["date"].values, c["period"].values, c["job"].values)):
        cands = lookup[(pd.Timestamp(d), p_, j)]
        pick[t] = cands[rng.integers(0, len(cands))]
    c["shift"] = pick
    calls["agent"] = ""
    calls["shift"] = -1
    calls.loc[conn, "agent"] = sh["agent"].values[pick]
    calls.loc[conn, "shift"] = pick
    # an interviewer who stays on for a late appointment is paid to the quarter hour after its wrap
    start_h = sh["period"].map({"day": 9.0, "evening": 16.0, "weekend": 10.0})
    c_end = c["placed"] + pd.to_timedelta(c["talk"] + c["wrap"] + 30, unit="s")
    need = ((c_end - c["date"]).dt.total_seconds() / 3600.0 - start_h.values[pick]).groupby(pick).max()
    need = np.ceil(need * 4) / 4
    later = need[need > sh["hours"].values[need.index]]
    sh.loc[later.index, "hours"] = later.values
    # training shifts: an evening of coaching booked to a project code, no calls
    weekday = np.flatnonzero(sh["period"].ne("weekend").values)
    tr_idx = rng.choice(weekday, size=int(len(sh) * 0.02), replace=False)
    train = sh.iloc[tr_idx].copy()
    train["shift"] = np.arange(len(sh), len(sh) + len(train))
    train["date"] = train["date"] + pd.Timedelta(days=0)
    train["period"] = "training"
    train["hours"] = 2.5                     # 13:30 to 16:00, between the day and evening shifts
    train["jobs"] = train["jobs"].map(lambda j: j[:1])
    return calls, sh, train


def make():
    USED.clear()
    rng = np.random.default_rng(P.SEED)
    days = calling_days(rng)
    specs = P.PROJECTS + [P.ONE_OFF]
    frames, calls = [], []
    for k, spec in enumerate(specs):
        fr = project_frame(rng, spec, k)
        frames.append(fr)
        calls.append(place_calls(rng, spec, fr, days))
    frame = pd.concat(frames, ignore_index=True)
    assert not frame["phone"].duplicated().any(), "a number sampled twice"
    c = pd.concat(calls, ignore_index=True).sort_values(["placed", "job", "phone"]).reset_index(drop=True)
    c = outcomes(rng, c)
    c = appointments(rng, c, frame)
    c = late_appointments(np.random.default_rng(P.SEED + 21), c)
    c = timings(rng, c)
    sharp = on_the_hour(c["placed"].values, c["state"].values)    # the dialer's pacing never lands on the second
    for col in ("placed", "answered", "connected", "ended"):
        c.loc[sharp, col] = c.loc[sharp, col] + pd.Timedelta(seconds=7)
    pl, an, moved = no_straddle(c["placed"].values, c["answered"].values, c["state"].values)
    c["placed"], c["answered"] = pl, an
    for col in ("connected", "ended"):
        c[col] = c[col] + pd.to_timedelta(moved, unit="s")
    ids = np.arange(5_400_000, 5_400_000 + len(c)) + rng.integers(0, 3, len(c)).cumsum()
    order = np.argsort(c["placed"].values, kind="stable")
    c["call_id"] = 0
    c.iloc[order, c.columns.get_loc("call_id")] = ids            # the dialer numbers its calls as it places them
    other = inbound_other(rng, c)
    other = pd.concat([other, line_interviews(np.random.default_rng(P.SEED + 31), c, other)], ignore_index=True)
    c = settled_on_the_line(c, other)
    # a second ring pushed past the four-hour floor onto another day keeps the dialing period it was paced in; the
    # dialer drops it rather than ring outside that day's own periods
    stray = (c["period"] == "weekend").values != (c["placed"].dt.dayofweek == 5).values
    full = c
    c = c[~stray].reset_index(drop=True)
    c, shifts, training = staff(np.random.default_rng(P.SEED + 3), c)
    truth_ret = inbound_returns(np.random.default_rng(P.SEED + 5), full)
    truth_ret = truth_ret[truth_ret["src_call"].isin(set(c["call_id"]))]
    inbound = clear_of_redials(pd.concat([truth_ret, other], ignore_index=True), c)
    inbound = inbound[inbound["started"] < pd.Timestamp(P.INBOUND_END)]
    inbound = inbound.sort_values(["started", "caller"]).reset_index(drop=True)
    reopen = reopens(np.random.default_rng(P.SEED + 9), c)
    frame, c, inbound, truth_ret, reopen = (relabel(x) for x in (frame, c, inbound, truth_ret, reopen))
    return dict(frame=frame, calls=c, shifts=shifts, training=training, inbound=inbound, returns=truth_ret,
                reopen=reopen, rng=rng)


# each project's caller-ID line, taken from the centre's block of direct lines as the project was set up
LINE_SUFFIX = ["0117", "0163", "0128", "0181", "0142", "0109", "0195", "0136", "0172", "0154", "0189", "0121", "0148",
               "0166"]
def _code(s):
    s = pd.Series(s, dtype=object)
    ok = s.str.len().eq(10)
    head = s.str[:3].map(P.RELABEL_CODE)
    return s.where(~(ok & head.notna()), head + s.str[3:]).values


def relabel(df):
    """the world's draw labels onto the states and area codes the frame really reaches (params.RELABEL_STATE)"""
    df = df.copy()
    for col in ("state", "home_state"):
        if col in df.columns:
            df[col] = df[col].replace(P.RELABEL_STATE)
    for col in ("phone", "caller"):
        if col in df.columns:
            df[col] = _code(df[col].astype(str).values)
    return df


LINES = {s[0]: "+1651555" + x for s, x in zip(P.PROJECTS + [P.ONE_OFF], LINE_SUFFIX)}
LINE_NAMES = {s[0]: "KRR " + s[1].split(" (")[0].replace(" Survey", "").replace(" Poll", " Poll").replace(" Study", "")
              for s in P.PROJECTS + [P.ONE_OFF]}


def _delay_prompt(rng, k):
    """a person who hears the recorded message presses redial: seconds after the line closes"""
    return 8 + np.exp(np.log(14) + 0.4 * np.clip(rng.standard_normal(k), -3, 3))


def _delay_late(rng, k):
    """a voicemail returned, or a person ringing back later in the day: hours after the call"""
    return 9000 + np.exp(np.log(2.5 * 3600) + 0.8 * rng.standard_normal(k))


def inbound_returns(rng, c):
    """what people and machine owners do after the dialer hangs up on them: people hung up on by the detector or
    abandoned ring the caller-ID line back within minutes or, a few, hours later; machine owners return the call from
    their voicemail hours later; a handful of screening households ring back at once"""
    rows = []
    am = c["outcome"].eq("AMD_MACHINE").values
    ab = c["outcome"].eq("ABANDONED").values
    person = ~c["is_machine"].values
    p_imm = c["p_imm"].values
    p_vm = c["p_vm"].values
    # one draw per call that heard the recorded message, in the order the dialer placed them
    heard = np.flatnonzero(am | ab)
    heard = heard[np.lexsort((c["phone"].values[heard], c["placed"].values[heard]))]
    u, u2 = np.ones(len(c)), np.ones(len(c))
    u[heard] = rng.random(len(heard))
    u2[heard] = rng.random(len(heard))
    hung_person = (am & person) | ab
    prompt = hung_person & (u < p_imm)
    late_person = hung_person & (~prompt) & (u2 < 0.04)
    screen = am & ~person & (u < 0.0003)
    vm = am & ~person & (~screen) & (u2 < p_vm)
    for mask, kind, delay in [(prompt, "prompt", _delay_prompt), (late_person, "late", _delay_late),
                              (screen, "screen", lambda r, k: 10 + 40 * r.random(k)), (vm, "voicemail", _delay_late)]:
        idx = np.flatnonzero(mask)
        d = delay(rng, len(idx))
        rows.append(pd.DataFrame(dict(src_call=c["call_id"].values[idx], kind=kind, job=c["job"].values[idx],
                                      caller=c["phone"].values[idx],
                                      started=c["ended"].values[idx] + pd.to_timedelta(np.floor(d), unit="s"))))
    out = pd.concat(rows, ignore_index=True)
    # nobody returns a call in the night: a return that would land after 22:00 or before 08:00 comes the next morning
    night = (out["started"].dt.hour >= 22) | (out["started"].dt.hour < 8)
    morning = out["started"].dt.normalize() + pd.to_timedelta(np.where(out["started"].dt.hour >= 22, 1, 0), unit="D")
    r2 = np.random.default_rng(P.SEED + 6)
    later = pd.to_timedelta(8 * 3600 + np.floor(r2.exponential(80 * 60, len(out))), unit="s")
    out.loc[night, "started"] = (morning + later)[night]
    return out


def clear_of_redials(inbound, c):
    """a household that rings the line for any reason but the recorded message it just heard does so more than two and
    a half hours after the dialer last rang it (its later calls come after an evening's or a morning's other business)"""
    inbound = inbound.copy()
    keep = inbound["kind"].isin(["prompt", "screen"]) | inbound["kind"].eq("test")
    out = c[["phone", "ended"]].dropna().sort_values("ended")
    for _ in range(5):
        x = inbound[~keep].reset_index().sort_values("started")
        m = pd.merge_asof(x, out.rename(columns={"phone": "caller"}), left_on="started", right_on="ended",
                          by="caller", direction="backward")
        near = m["ended"].notna() & ((m["started"] - m["ended"]) < pd.Timedelta(minutes=150))
        if not near.any():
            break
        idx = m.loc[near, "index"].values
        inbound.loc[idx, "started"] = (m.loc[near, "ended"] + pd.Timedelta(minutes=150)
                                       + pd.to_timedelta((m.loc[near, "started"] - m.loc[near, "ended"]).dt.total_seconds()
                                                         .values, unit="s")).values
    return inbound


def inbound_other(rng, c):
    """the line's other traffic: interviews done when the household calls in, opt-outs, questions, appointments set,
    and the weekly test calls quality assurance places from the firm's own extensions"""
    other = []
    done_cases = set(zip(c.loc[c["outcome"].eq("COMPLETE"), "job"], c.loc[c["outcome"].eq("COMPLETE"), "case_new"]))
    done = c[c["outcome"].isin(["CALLBACK", "REFUSAL", "PARTIAL"])]
    done = done[[(j, k) not in done_cases for j, k in zip(done["job"], done["case_new"])]]
    done = done.drop_duplicates(["job", "case_new"])
    for job, g in done.groupby("job"):
        k = max(8, int(len(g) * 0.035))
        pick = g.sample(n=min(k, len(g)), random_state=int(rng.integers(1e9)))
        lag = pd.to_timedelta(rng.integers(1, 9, len(pick)), unit="D") + pd.to_timedelta(
            rng.integers(9 * 3600, 20 * 3600, len(pick)), unit="s")
        st = pick["placed"].dt.normalize() + lag
        kind = rng.choice(["complete", "question", "optout", "callback_set"], size=len(pick), p=[0.32, 0.31, 0.12, 0.25])
        other.append(pd.DataFrame(dict(src_call=-1, kind=kind, job=job, caller=pick["phone"].values, started=st.values,
                                       case_new=pick["case_new"].values)))
    tests = pd.date_range(f"{P.YEAR}-01-05 08:40", f"{P.YEAR}-12-28 08:40", freq="7D")
    for job in LINES:
        other.append(pd.DataFrame(dict(src_call=-1, kind="test", job=job, caller="6517",
                                       started=tests + pd.Timedelta(minutes=int(rng.integers(0, 50))), case_new="")))
    return pd.concat(other, ignore_index=True)


def line_interviews(rng, c, other):
    """households that ring the line days after the dialer's last attempt and do the interview then"""
    out = []
    taken = set(zip(other["job"], other["case_new"]))
    for job, *_ in P.PROJECTS:
        g = c[c["job"] == job]
        done = set(g.loc[g["outcome"].eq("COMPLETE"), "case_new"])
        last = g.sort_values("placed").drop_duplicates("case_new", keep="last")
        last = last[last["outcome"].isin(["CALLBACK", "REFUSAL", "PARTIAL", "HANGUP"]) & ~last["case_new"].isin(done)]
        last = last[[(job, k) not in taken for k in last["case_new"]]]
        n = int(round(P.LINE_INTERVIEWS * len(done)))
        pick = last.sample(n=min(n, len(last)), random_state=int(rng.integers(1e9))).sort_values("case_new")
        st = pick["placed"].dt.normalize() + pd.to_timedelta(rng.integers(1, 9, len(pick)), unit="D") + pd.to_timedelta(
            rng.integers(9 * 3600, 20 * 3600, len(pick)), unit="s")
        out.append(pd.DataFrame(dict(src_call=-1, kind="complete", job=job, caller=pick["phone"].values,
                                     started=st.values, case_new=pick["case_new"].values)))
    return pd.concat(out, ignore_index=True)


def settled_on_the_line(c, other):
    """a case completed when the household called in, or that asked on the line not to be called, is closed in the
    case manager and the dialer never rings it again"""
    closed = other[other["kind"].isin(["complete", "optout"])][["job", "case_new", "started"]]
    closed = closed.rename(columns={"started": "closed_at"})
    c = c.merge(closed, on=["job", "case_new"], how="left")
    c = c[c["closed_at"].isna() | (c["placed"] < c["closed_at"])].drop(columns="closed_at")
    return c.sort_values(["placed", "call_id"]).reset_index(drop=True)


def reopens(rng, c):
    """a supervisor's verification callback on a completed case closes it as complete again, under a new call"""
    comp = c[c["outcome"].eq("COMPLETE")]
    k = int(len(comp) * P.REOPEN_SHARE)
    pick = comp.sample(n=k, random_state=int(rng.integers(1e9))).copy()
    pick["placed"] = pick["placed"] + pd.to_timedelta(rng.integers(*P.REOPEN_LAG, k), unit="D") + pd.to_timedelta(
        rng.integers(0, 3600, k), unit="s")
    pick = pick[pick["placed"].dt.year == P.YEAR]
    pick["agent"] = "SUP1"
    pick["talk"] = rng.integers(60, 400, len(pick))
    pick["wrap"] = rng.integers(20, 90, len(pick))
    pick["answered"] = pick["placed"] + pd.Timedelta(seconds=1)
    pick["connected"] = pick["answered"]
    pick["ended"] = pick["answered"] + pd.to_timedelta(pick["talk"], unit="s")
    pick["reopen"] = True
    return pick
