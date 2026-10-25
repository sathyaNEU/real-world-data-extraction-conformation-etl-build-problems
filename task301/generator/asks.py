"""The ask files: the state Quitline's monthly referral report to the PHN (2023 to 2025) and the 2025 team's
dialler export. None of these rows is read by the main call.

Quitline labels each referring practice with the PHN sub-region its directory holds, which it took from the PHN in
2023 and never updated after the PHN realigned its sub-regions to the new council boundaries on 1 July 2025, and it
names practices as its own directory spells them. Each team member's dialler legs run one after another through the
shift, and the dialler writes a leg's record when its line is released, so the record's time is the end of the leg.
A patient who sets a quit date and wants Quitline's call-back service as well is transferred to Quitline on the call:
the coach dials Quitline and leaves, the dialler logs that transfer leg, and the patient's own leg stays open until
the patient hangs up, both lines released together."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

# the 1 July 2025 realignment moved four practices round a cycle: (current sub-region, size rank in it, sub-region
# before July 2025), a large practice and a small one alternately so every candidate's count moves
MOVED = [("B", 0, "A"), ("C", -1, "B"), ("D", 0, "C"), ("A", -1, "D")]

STREETS = ["Banksia", "Wattle", "Lyrebird", "Ironbark", "Kingfisher", "Bottlebrush", "Paperbark", "Riverbend",
           "Hilltop", "Seaview", "Station Street", "Harbourside", "Ridgeway", "Creekside", "Tallowwood", "Jacaranda",
           "Old Mill", "Bellview", "Grevillea", "Saltwater", "Coachwood", "Cedar Street", "Lagoon", "Pelican",
           "Waratah", "Heathcote Road", "Bluegum", "Coral Tree", "Myrtle", "Sandstone", "Lighthouse", "Kestrel",
           "Brolga", "Quandong", "Mountain View", "Valley", "Northside", "Southgate", "Westbury", "Eastlakes",
           "Marina", "Parkside", "Market Street", "Orchard", "Wetlands", "Dunes", "Headland", "Gully Road",
           "Ferntree", "Rosella", "Kurrawa", "Mallee", "Saltbush", "Oakdale", "Riverside", "Bayview", "Granite",
           "Tablelands", "Glenroy", "Wildflower", "Lakeside"]
KINDS = ["Medical Centre", "Family Practice", "General Practice", "Medical Practice", "Health Centre"]


def practice_names(pr, rng, entered_2023=()):
    """The PHN register's names, and the slightly different spellings Quitline's directory holds for some; the
    practices Quitline's directory took from the PHN's 2023 list (entered_2023) carry that list's spelling."""
    names, ql = {}, {}
    for i, p in enumerate(pr.practice_id):
        n = "%s %s" % (STREETS[i % len(STREETS)], KINDS[int(rng.integers(0, len(KINDS)))])
        names[p] = n
        u = rng.uniform()
        if u < 0.12:
            ql[p] = n.replace("Medical Centre", "Med Centre").replace("General Practice", "GP")
        elif u < 0.20:
            ql[p] = n.upper()
        elif u < 0.26:
            ql[p] = n + " Pty Ltd"
        else:
            ql[p] = n
        if p in entered_2023 and ql[p] == n:
            ql[p] = n.upper() if i % 2 else n + " Pty Ltd"
    return names, ql


def moved_practices(pr, ext):
    size = ext.practice_id.value_counts()
    out = {}
    for g, rank, old in MOVED:
        ids = sorted(pr[pr.reg == g].practice_id, key=lambda p: (-size.get(p, 0), p))
        out[ids[rank]] = old
    return out


def quitline(pr, ext, ql_names, rng):
    """Monthly referrals by referring practice and channel, with Quitline's own sub-region label."""
    moved = moved_practices(pr, ext)
    size = ext.practice_id.value_counts()
    rate = {"P": 0.85, "A": 0.60, "B": 1.25, "C": 0.95, "D": 1.10}     # referrals a month per 1,000 active adults
    rows = []
    for _, p in pr.iterrows():
        n = size.get(p.practice_id, 0)
        lam = rate[p.reg] * n / 1000.0 * np.exp(rng.normal(0, 0.25))
        label = P.NAME[moved.get(p.practice_id, p.reg)]
        for m in pd.period_range("2023-01", "2025-12", freq="M"):
            season = 1.0 + (0.35 if m.month == 1 else 0.0) + (0.15 if m.month in (5, 6) else 0.0)
            k = rng.poisson(lam * season)
            if k == 0:
                continue
            e = rng.binomial(k, 0.55 if m.year == 2023 else (0.68 if m.year == 2024 else 0.79))
            for ch, c in (("eReferral", e), ("Fax", k - e)):
                if c:
                    rows.append((str(m), ql_names[p.practice_id], label, ch, int(c)))
    q = pd.DataFrame(rows, columns=["month", "referring_practice", "phn_sub_region", "channel", "referrals"])
    return q.sort_values(["month", "phn_sub_region", "referring_practice", "channel"]).reset_index(drop=True)


AGENTS = [("QO-N1", (8, 30), (17, 0)), ("QO-C1", (8, 30), (17, 0)), ("QO-C2", (11, 0), (19, 30))]
QL_TRANSFER = 0.35         # patients setting a quit date who take Quitline's call-back service, transferred on the call
EVENING = 0.62             # share of QO-C2's attempts made from 5 pm


def leg_times(rng, ans, xfer):
    """(result, seconds from the dial to the line's release, staff seconds, transfer leg seconds, wrap seconds)."""
    if not ans:
        res = str(rng.choice(["No answer", "Voicemail", "Busy"], p=[0.55, 0.38, 0.07]))
        sec = int(rng.integers(3, 11)) if res == "Busy" else int(rng.integers(18, 76))
        return res, sec, sec, 0, int(rng.integers(15, 61))
    ring = int(rng.integers(5, 26))
    if xfer:
        coach = ring + int(rng.integers(300, 1101))
        ql = int(rng.integers(8, 41)) + int(rng.integers(360, 1201))
        return "Answered", coach + ql, coach, ql, int(rng.integers(60, 241))
    sec = ring + int(rng.integers(240, 1501))
    return "Answered", sec, sec, 0, int(rng.integers(60, 301))


def place(items, t0, t1, rng, tail=None):
    """Start times (seconds after midnight) for items run one after another, every start in [t0, t1): the idle time is
    spread at random between them and, with tail, the last start falls about tail seconds before t1, the member working
    to the end of the shift and that call running past it. Items that do not fit are dropped from the end."""
    busy = [it["staff"] + it["wrap"] for it in items]
    while items and sum(busy[:-1]) > (t1 - t0) * 0.92:
        items, busy = items[:-1], busy[:-1]
    if not items:
        return [], []
    free = (t1 - t0) - sum(busy[:-1])
    n = len(items)
    if tail is None:
        g = rng.dirichlet(np.ones(n + 1)) * free
    else:
        slack = min(free, 60 + rng.exponential(tail))
        g = np.append(rng.dirichlet(np.ones(n)) * (free - slack), slack)
    t, starts = t0, []
    for bz, gap in zip(busy, g[:-1]):
        t += gap
        starts.append(int(t))
        t += bz
    return starts, items


def dialler(log, rng):
    """Every leg the dialler logged for the team's 2025 calls, from the case log's attempts and outcomes; the hidden
    columns (_start, _staff_s, _kind) are the truth and never ship."""
    first = P.PILOT_CALLS[0]
    by_day = {}
    for r in log.itertuples():
        d = dt.date.fromisoformat(r.call_date)
        k = int(r.attempts)
        reached = r.outcome != "Not reached"
        days = [d]
        for _ in range(k - 1):
            prev = (pd.Timestamp(days[0]) - pd.offsets.BDay(int(rng.integers(1, 5)))).date()
            days.insert(0, max(prev, first))
        for j, dd in enumerate(days):
            ans = (j == k - 1) and reached
            xfer = ans and r.outcome == "Quit date set" and rng.uniform() < QL_TRANSFER
            res, sec, staff, ql, wrap = leg_times(rng, ans, xfer)
            by_day.setdefault(dd, []).append(dict(pk=r.patient_key, res=res, sec=sec, staff=staff, ql=ql, wrap=wrap))
    rows = []
    for dd in sorted(by_day):
        items = by_day[dd]
        # one agent per patient that day; attempts to the same patient on one day go to the same agent
        agent_of = {}
        for it in items:
            if it["pk"] not in agent_of:
                agent_of[it["pk"]] = int(rng.choice(3, p=[0.30, 0.30, 0.40]))
        for ai, (ag, (h0, m0), (h1, m1)) in enumerate(AGENTS):
            mine = [it for it in items if agent_of[it["pk"]] == ai]
            rng.shuffle(mine)
            seen = {}
            for it in mine:
                it["occ"] = seen.get(it["pk"], 0)
                seen[it["pk"]] = it["occ"] + 1
            mine.sort(key=lambda it: it["occ"])
            # a member logs in, reads the day's list and starts dialling a few minutes into the shift
            s0, s1 = (h0 * 60 + m0) * 60 + int(rng.integers(180, 1080)), (h1 * 60 + m1) * 60
            if ag == "QO-C2":
                late = [it for it in mine if rng.uniform() < EVENING]
                early = [it for it in mine if all(it is not x for x in late)]
                while True:
                    st_e, early_ok = place(early, s0, 17 * 3600, rng, tail=300)
                    assert len(early_ok) == len(early), (dd, ag)
                    end_e = max([s + it["staff"] + it["wrap"] for s, it in zip(st_e, early_ok)] + [17 * 3600])
                    st_l, late_ok = place(late, end_e, s1, rng, tail=360)
                    if len(late_ok) == len(late):
                        break
                    # the evening cannot hold them all: the last one is made in the afternoon instead
                    early.append(late.pop())
                plan = list(zip(st_e, early_ok)) + list(zip(st_l, late_ok))
            else:
                st, ok = place(mine, s0, s1, rng, tail=300)
                assert len(ok) == len(mine), (dd, ag)
                plan = list(zip(st, ok))
            for s, it in plan:
                start = dt.datetime.combine(dd, dt.time()) + dt.timedelta(seconds=s)
                end = start + dt.timedelta(seconds=it["sec"])
                rows.append([it["pk"], ag, end, it["sec"], it["res"], start, it["staff"], "call"])
                if it["ql"]:
                    rows.append([it["pk"], ag, end, it["ql"], "Transferred",
                                 start + dt.timedelta(seconds=it["staff"]), 0, "transfer"])
    df = pd.DataFrame(rows, columns=["patient_key", "agent_id", "_end", "duration_s", "result", "_start", "_staff_s",
                                     "_kind"])
    df["date_time"] = df._end.dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.sort_values(["date_time", "patient_key", "_kind"], kind="stable").reset_index(drop=True)
    df.insert(0, "leg_id", np.arange(700001, 700001 + len(df)))
    return df[["leg_id", "patient_key", "agent_id", "date_time", "duration_s", "result", "_start", "_staff_s", "_kind"]]
