"""The shipped records behind the call: the CRM's 2026 interaction export, the seasonal roster with the 2027 recall,
the HR history of every expert-season, the old ticketing system's weekly agent reports and the 2027 demand plan.
Each is written the way the system that keeps it writes it."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import world as W

F_CRM = "crm_expert_interactions_2026.csv"
F_ROSTER = "seasonal_expert_roster_2027.xlsx"
F_HISTORY = "seasonal_expert_history.csv"
F_OLD_A = "ticketing_agent_weekly_2021_2022.csv"
F_OLD_B = "ticketing_agent_weekly_2023_2025.csv"
F_DEMAND = "demand_plan_2027.xlsx"

QUEUE_NAME = {0: "Live Experts EN", 1: "Live Experts FR"}
CHANNEL_NAME = {0: "Video", 1: "Chat", 2: "Phone"}
DISP_NAME = {0: "Resolved", 1: "Customer to complete steps", 2: "Senior review requested", 3: "Callback arranged"}
TEAMS_EN = ["EN-%02d" % k for k in range(1, 31)]
TEAMS_FR = ["FR-01", "FR-02", "FR-03"]


def local_dt(day_ord, hours):
    d = dt.date.fromordinal(int(day_ord))
    secs = int(round(hours * 3600))
    return dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(seconds=secs)


def to_utc_e(day_ord, hours):
    return K.to_utc(local_dt(day_ord, hours), -5)


# ------------------------------------------------------------------------------------------------- the people
def assign_teams(people):
    """Teams per season: experts spread over the English teams, a few per team from each class."""
    R = K.rng("teams")
    for e in people:
        e.team = {}
    for y in K.SEASONS_OLD + [K.SEASON_CRM, K.SEASON_PLAN]:
        for queue, teams in (("EN", TEAMS_EN), ("FR", TEAMS_FR)):
            members = [e for e in people if y in e.seasons and e.queue == queue]
            order = R.permutation(len(members))
            for k, i in enumerate(order):
                members[i].team[y] = teams[k % (24 if queue == "EN" and y < 2026 else len(teams))]


def recall_status(people):
    """Every 2026 expert's answer to the 2027 recall."""
    R = K.rng("recall")
    out = {}
    for e in people:
        if K.SEASON_CRM not in e.seasons:
            continue
        if K.SEASON_PLAN in e.seasons:
            out[e.emp] = "Confirmed"
        else:
            u = R.random()
            out[e.emp] = "Declined" if u < 0.62 else ("No response" if u < 0.9 else "Not invited")
    return out


def roster_rows(people, recall):
    rows = []
    for e in people:
        if K.SEASON_CRM not in e.seasons:
            continue
        cls = e.cls if e.first == K.SEASON_CRM else ""
        gl = e.golive.isoformat() if e.first == K.SEASON_CRM else ""
        rows.append({"Employee No": e.emp, "Queue": e.queue, "Team 2026": e.team.get(K.SEASON_CRM, ""),
                     "First Season": e.first, "Seasons Worked": len([s for s in range(e.first, 2027)
                                                                      if s in e.seasons or s < 2021]),
                     "2026 Class": cls, "2026 Go-Live": gl, "2027 Recall": recall[e.emp]})
    rows.sort(key=lambda r: (r["Queue"], r["Employee No"]))
    return rows


def history_rows(people):
    rows = []
    for e in people:
        for y in sorted(set(e.seasons)):
            if y > K.SEASON_CRM:
                continue
            first_here = (y == e.first)
            rows.append({"employee_no": e.emp, "old_agent_code": e.old_code or "", "season": y, "queue": e.queue,
                         "team": e.team.get(y, ""), "first_season": e.first,
                         "class": e.cls if first_here and e.cls else "",
                         "go_live": e.golive.isoformat() if first_here and e.golive else ""})
    rows.sort(key=lambda r: (r["season"], r["queue"], r["employee_no"]))
    return rows


# ------------------------------------------------------------------------------------------------- the CRM export
CRM_COLS = ["Interaction ID", "Case Number", "Queue", "Channel", "Interaction Type", "Topic", "Started (UTC)",
            "Ended (UTC)", "Talk Seconds", "After-Contact Work Seconds", "Handled By", "Disposition"]


def connect_seconds(recs):
    """Seconds from the expert accepting a contact to the conversation beginning: the video platform takes a while
    to bring both sides in, chat and phone hardly any."""
    R = K.rng("connect")
    u = R.random(len(recs))
    ch = recs["channel"]
    return np.where(ch == 0, 6 + 22 * u, np.where(ch == 1, 1 + 3 * u, 2 * u))


def crm_rows(recs, staff, delay=None):
    """The CRM's interaction export. Returns the rows and each record's Interaction ID by record index."""
    delay = connect_seconds(recs) if delay is None else delay
    order = np.lexsort((recs["start"], recs["day"]))
    R = K.rng("crm_ids")
    # case numbers in the order cases open
    first_t = {}
    for i in order:
        c = int(recs["case"][i])
        if c not in first_t:
            first_t[c] = len(first_t)
    base_case = 412800
    case_no = {}
    k = base_case
    for c, rank in sorted(first_t.items(), key=lambda kv: kv[1]):
        k += 1 + int(R.integers(0, 3))
        case_no[c] = "CS-26-%07d" % k
    inter = 18_204_000
    rows = []
    ids = {}
    for i in order:
        r = recs[i]
        inter += 1 + int(R.integers(0, 4))
        e = staff[int(r["expert"])]
        st = to_utc_e(r["day"], float(r["start"]) + float(delay[i]) / 3600)
        en = to_utc_e(r["day"], r["end"])
        wrap = int(round(float(r["wrap"])))
        talk = int(round((en - st).total_seconds())) - wrap
        ids[int(i)] = "INT-%09d" % inter
        rows.append([
            ids[int(i)], case_no[int(r["case"])], QUEUE_NAME[int(r["queue"])], CHANNEL_NAME[int(r["channel"])],
            "New case" if r["pos"] == 1 else "Follow-up", W.TOPICS[int(r["topic"])][0], K.iso_z(st), K.iso_z(en),
            talk, wrap, e.emp, DISP_NAME[int(r["disp"])]])
    return rows, ids


# ------------------------------------------------------------------------------------------------- old system
OLD_A_COLS = ["Season", "Week Starting", "Agent Code", "Team", "New Tickets", "Follow-up Tickets", "Handle Time"]
OLD_B_COLS = ["season", "week_start", "agent_code", "team", "tickets_new", "tickets_followup", "handle_minutes"]


def old_rows(y, arr, staff):
    """One row per agent per week of season y: tickets the agent took by type and their handle time."""
    wk0 = K.monday(K.season_open(y))
    week = (arr["day"] - wk0.toordinal()) // 7
    out = {}
    for i in range(len(arr)):
        e = staff[int(arr["expert"][i])]
        code = e.old_code if e.kind != "vendor" else "EXT-%s" % e.emp.replace("HCS-", "")
        key = (int(week[i]), code)
        o = out.setdefault(key, [0, 0, 0.0, e])
        if arr["pos"][i] == 1:
            o[0] += 1
        else:
            o[1] += 1
        o[2] += float(arr["hsec"][i])
    rows = []
    for (w, code), (n_new, n_fu, secs, e) in sorted(out.items()):
        start = wk0 + dt.timedelta(7 * w)
        team = e.team.get(y, "") if e.kind != "vendor" else "HCS"
        if e.queue == "FR":
            team = e.team.get(y, "FR")
        if y <= 2022:
            hh = int(secs // 3600); mm = int(round((secs - 3600 * hh) / 60))
            if mm == 60:
                hh, mm = hh + 1, 0
            rows.append([y, start.strftime("%m/%d/%Y"), code, team, n_new, n_fu, "%d:%02d" % (hh, mm)])
        else:
            rows.append([y, start.isoformat(), code, team, n_new, n_fu, int(round(secs / 60))])
    return rows


# ------------------------------------------------------------------------------------------------- 2027 demand plan
def demand_plan_rows(F_target):
    """The demand plan's daily new expert cases for the English queue, 11 January to 31 May 2027, scaled so the
    deadline fortnight carries F_target."""
    y = K.SEASON_PLAN
    days = [K.season_open(y) + dt.timedelta(k) for k in range((K.season_close(y) - K.season_open(y)).days + 1)]
    raw = np.array([W.demand_curve(d, y, 1.0, "EN") for d in days])
    f0, f1 = K.fortnight(y)
    fmask = np.array([f0 <= d <= f1 for d in days])
    scale = F_target / raw[fmask].sum()
    vals = raw * scale
    # whole cases a day, the fortnight's sum held exactly at the target
    ints = np.floor(vals).astype(int)
    rem = vals - ints
    short = int(round(F_target - ints[fmask].sum()))
    idx = np.where(fmask)[0][np.argsort(-rem[fmask])][:short]
    ints[idx] += 1
    return days, ints


def demand_basis(F26, growth, history):
    """The demand plan's Basis sheet: each season's deadline fortnight and its new expert cases on the English
    queue (the old ticketing system to 2025, the CRM from 2026), and the 2027 figure."""
    rows = []
    for y, n in history:
        f0, f1 = K.fortnight(y)
        rows.append([y, K.deadline(y), f0, f1, n, "Ticketing system, new tickets" if y < K.SEASON_CRM else "CRM, new cases"])
    f0, f1 = K.fortnight(K.SEASON_PLAN)
    rows.append([K.SEASON_PLAN, K.deadline(K.SEASON_PLAN), f0, f1, None, "Forecast"])
    return rows


CSAT_COLS = ["Survey ID", "Interaction ID", "Sent (UTC)", "Responded (UTC)", "Overall satisfaction (1-5)",
             "Did the expert answer your question?", "How likely are you to recommend Ashdale Tax Live? (0-10)"]


def csat_rows(recs, ids, followed):
    """The post-contact survey: a sample of English-queue interactions get an email the next morning; some answer.
    followed: for each record, whether its case came back after it."""
    R = K.rng("csat")
    en = np.where(recs["queue"] == 0)[0]
    pick = en[R.random(len(en)) < 0.11]
    rows = []
    sid = 5_520_000
    for i in sorted(pick, key=lambda k: (int(recs["day"][k]), float(recs["end"][k]))):
        fol = bool(followed[i])
        if R.random() >= (0.15 if fol else 0.12):
            continue
        sent = to_utc_e(int(recs["day"][i]) + 1, 9.0 + float(R.uniform(0, 0.5)))
        resp = sent + dt.timedelta(minutes=int(R.integers(4, 60 * 30)))
        answered = R.random() >= (0.46 if fol else 0.09)
        sat = int(np.clip(round(R.normal(4.45 if answered else 3.0, 0.75)), 1, 5))
        nps = int(np.clip(round(R.normal(8.6 if answered else 5.8, 1.6)), 0, 10))
        sid += 1 + int(R.integers(0, 3))
        rows.append(["SV-%08d" % sid, ids[int(i)], K.iso_z(sent), K.iso_z(resp), sat, "Yes" if answered else "No", nps])
    return rows


RETURNS_COLS = ["Season", "Week Ending", "Live Returns Filed (000s)"]


def returns_rows():
    """Finance's weekly count of returns filed by Ashdale Tax Live customers, in thousands."""
    R = K.rng("returns")
    rows = []
    for y in K.SEASONS_OLD + [K.SEASON_CRM]:
        d = K.monday(K.season_open(y))
        while d <= K.season_close(y):
            days = [d + dt.timedelta(k) for k in range(7)]
            cases = sum(W.demand_curve(x, y, W.SCALE[y], "EN") for x in days if K.season_open(y) <= x <= K.season_close(y))
            ratio = 3.05 + 0.04 * (y - 2021)
            val = cases * ratio * float(np.exp(R.normal(0, 0.03))) / 1000
            rows.append([y, (d + dt.timedelta(6)).isoformat(), "%.1f" % val])
            d += dt.timedelta(7)
    return rows
