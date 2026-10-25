"""The ask files: the state Quitline's monthly referral report to the PHN (2023 to 2025), the 2025 team's dialler
export and its roster. None of these rows is read by the main call.

Quitline labels each referring practice with the PHN sub-region its directory holds, which it took from the PHN in
2023 and never updated after the PHN realigned its sub-regions to the new council boundaries on 1 July 2025, and it
names practices as its own directory spells them. The dialler is hosted in Brisbane and stamps every leg in Australian
Eastern Standard Time all year, while the team in New South Wales works to local time, an hour ahead of the stamps
before 6 April and from 5 October 2025. When a coach hands an answered call to the nurse, the dialler writes the
nurse's leg as a second row that starts inside the first, and the first leg's duration runs to the end of the call."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

# the 1 July 2025 realignment moved four practices round a cycle: (current sub-region, size rank in it, sub-region
# before July 2025), a large practice and a small one alternately so every candidate's count moves
MOVED = [("B", 0, "A"), ("C", -1, "B"), ("D", 0, "C"), ("A", -1, "D")]
DST_END, DST_START = dt.datetime(2025, 4, 6, 3, 0), dt.datetime(2025, 10, 5, 2, 0)   # NSW clock changes in 2025
TRANSFER = 0.16            # answered calls a coach hands to the nurse

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


def aest(local):
    """The dialler's stamp for a New South Wales local time."""
    if DST_END <= local < DST_START:
        return local
    return local - dt.timedelta(hours=1)


AGENTS = [("QO-N1", (8, 30), (17, 0)), ("QO-C1", (8, 30), (17, 0)), ("QO-C2", (11, 0), (19, 30))]


def dialler(log, rng):
    """Every leg the dialler logged for the team's 2025 calls, from the case log's attempts and outcomes; the hidden
    columns (_local, _leg) are the truth and never ship."""
    first = P.PILOT_CALLS[0]
    rows = []
    for r in log.itertuples():
        d = dt.date.fromisoformat(r.call_date)
        k = int(r.attempts)
        reached = r.outcome != "Not reached"
        days = [d]
        for _ in range(k - 1):
            prev = (pd.Timestamp(days[0]) - pd.offsets.BDay(int(rng.integers(1, 5)))).date()
            days.insert(0, max(prev, first))
        drawn = []
        for j, dd in enumerate(days):
            ai = int(rng.choice(3, p=[0.30, 0.30, 0.40]))
            ag, (h0, m0), (h1, m1) = AGENTS[ai]
            a, b = h0 * 60 + m0, h1 * 60 + m1 - 12
            if ag == "QO-C2" and rng.uniform() < 0.62:
                a = 17 * 60
            drawn.append([dd, ag, int(rng.integers(a, b)), int(rng.integers(0, 60))])
        # attempts that fall on one day run in order through the working day, 25 minutes or more apart, each made by
        # someone on shift at that time
        for dd in sorted({x[0] for x in drawn}):
            idx = [j for j, x in enumerate(drawn) if x[0] == dd]
            if len(idx) < 2:
                continue
            k = len(idx)
            span = (19 * 60 + 15) - (8 * 60 + 30) - 25 * (k - 1)
            ts = np.sort(rng.integers(0, span, k)) + 8 * 60 + 30 + 25 * np.arange(k)
            for j, t in zip(idx, ts):
                drawn[j][2] = int(t)
                if t >= 16 * 60 + 48:
                    drawn[j][1] = "QO-C2"
                elif t < 11 * 60 and drawn[j][1] == "QO-C2":
                    drawn[j][1] = AGENTS[int(rng.integers(0, 2))][0]
        for j, (dd, ag, t, sec) in enumerate(drawn):
            local = dt.datetime.combine(dd, dt.time(t // 60, t % 60, sec))
            ans = (j == len(days) - 1) and reached
            if ans:
                talk = int(rng.integers(240, 1500))
                res = "Answered"
            else:
                talk = int(rng.integers(15, 75))
                res = str(rng.choice(["No answer", "Voicemail", "Busy"], p=[0.55, 0.38, 0.07]))
            rows.append([r.patient_key, ag, local, talk, res, "call"])
            if ans and ag != "QO-N1" and rng.uniform() < TRANSFER / 0.70:
                # the coach hands over to the nurse partway through; the first leg's duration covers the whole call
                off = int(rng.integers(90, max(120, talk - 120)))
                rows.append([r.patient_key, "QO-N1", local + dt.timedelta(seconds=off), talk - off, "Answered", "leg"])
    df = pd.DataFrame(rows, columns=["patient_key", "agent_id", "_local", "duration_s", "result", "_leg"])
    df["started"] = [aest(x).strftime("%Y-%m-%d %H:%M:%S") for x in df._local]
    df = df.sort_values(["started", "patient_key"], kind="stable").reset_index(drop=True)
    df.insert(0, "leg_id", np.arange(700001, 700001 + len(df)))
    return df[["leg_id", "patient_key", "agent_id", "started", "duration_s", "result", "_local", "_leg"]]


def roster():
    return pd.DataFrame([
        ("QO-N1", "Clinical nurse consultant", "Monday to Friday", "08:30", "17:00", "2025-02-03", "2025-11-28"),
        ("QO-C1", "Quit coach", "Monday to Friday", "08:30", "17:00", "2025-02-03", "2025-11-28"),
        ("QO-C2", "Quit coach", "Monday to Friday", "11:00", "19:30", "2025-02-03", "2025-11-28")],
        columns=["agent_id", "role", "days", "shift_start", "shift_end", "from", "to"])
