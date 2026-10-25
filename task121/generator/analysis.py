"""The golden, computed from the shipped files alone: each questionnaire linked to the train it was handed out on
and to the conditions of the respondent's own journey, the fall in the share satisfied attributed to the four
drivers through those conditions, and the plan's baselines for the four weeks ending 19 September 2026."""
import difflib
import os
import re

import numpy as np
import pandas as pd

import common as K

NAME_TO_CODE = {}


def station_coder(stations):
    names = {r.crs_code: r.station_name for r in stations.itertuples()}
    canon = {re.sub(r"[^a-z]", "", n.lower()): c for c, n in names.items()}
    short = {"marlvale": "MVC", "marlvalecent": "MVC", "mvalecentral": "MVC", "marlvalec": "MVC",
             "ashcombepkwy": "ASP", "ashcombe": "ASP", "stcleerrd": "STC", "stcleer": "STC", "marlvalenth": "MVN",
             "marlvalesth": "MVS", "holbeck": "HBK", "farnley": "FRN", "wexleyx": "WXC", "trevose": "TRV",
             "pennick": "PNB", "carrow": "CRW", "radley": "RDL"}

    def code(text):
        t = str(text).strip()
        if t.upper() in names:
            return t.upper()
        k = re.sub(r"[^a-z]", "", t.lower())
        if k in canon:
            return canon[k]
        if k in short:
            return short[k]
        m = difflib.get_close_matches(k, list(canon), n=1, cutoff=0.85)
        return canon[m[0]] if m else None
    return code


def load(target):
    p = lambda k: os.path.join(target, K.FILES[k])
    D = {}
    D["resp"] = pd.read_csv(p("responses"), dtype={"board_station_code": str, "alight_station_code": str})
    D["field"] = pd.read_csv(p("fieldwork"))
    D["tt"] = pd.read_csv(p("timetable"), dtype=str)
    D["mv"] = pd.read_csv(p("movements"), dtype=str)
    D["lw"] = pd.read_csv(p("loadweigh"), dtype={"passengers_est": int, "vehicle": str, "unit_no": str})
    D["form"] = pd.read_csv(p("formations"), dtype={"unit_no": str})
    D["units"] = pd.read_excel(p("fleet"), sheet_name="Units", dtype={"Unit": str})
    D["mods"] = pd.read_excel(p("fleet"), sheet_name="Modifications", dtype={"Unit": str})
    D["crew"] = pd.read_csv(p("crew_worked"), dtype=str)
    D["roster"] = pd.read_csv(p("crew_roster"), dtype=str)
    D["amend"] = pd.read_csv(p("crew_amend"), dtype=str)
    D["fares"] = pd.read_csv(p("fares"))
    D["stations"] = pd.read_csv(p("stations"))
    return D


def mins(hhmm):
    h, m = str(hhmm).split(":")
    return int(h) * 60 + int(m)


def seats_on(D, unit, date):
    """A unit's standard seats on a date: the register's figure, or the seats after a modification once the unit
    has returned to traffic."""
    if "_seats" not in D:
        D["_seats"] = {r.Unit: int(r._4) for r in D["units"].itertuples()}
        D["_mods"] = {}
        for r in D["mods"].itertuples():
            D["_mods"].setdefault(r.Unit, []).append((str(r._4), int(r._5)))
    seats = D["_seats"][unit]
    for back, after in D["_mods"].get(unit, []):
        if date >= back:
            seats = after
    return seats


def train_index(D):
    """(timetable, headcode, days, origin, origin departure) -> the train's calls; a date's timetable is Dec24 before
    14 December 2025 and Dec25 from then."""
    tt = D["tt"].copy()
    tt["call_seq"] = tt["call_seq"].astype(int)
    trains = {}
    for uid, g in tt.groupby("train_uid", sort=False):
        g = g.sort_values("call_seq")
        first = g.iloc[0]
        key = (first["timetable"], first["headcode"], first["days_run"], first["station"], first["dep"])
        trains[key] = dict(uid=uid, group=first["service_group"], calls=list(g["station"]),
                           arr=list(g["arr"]), dep=list(g["dep"]))
    return trains


def which_tt(date):
    return "Dec24" if date < K.TIMETABLE_CHANGE.isoformat() else "Dec25"


def days_label(date):
    """The timetable a date runs: bank holidays in England run the Sunday timetable."""
    import datetime as dt
    d = dt.date.fromisoformat(date)
    if d in K.BANK_HOLIDAYS:
        return "SUN"
    wd = d.weekday()
    return "SUN" if wd == 6 else ("SAT" if wd == 5 else "MO-FR")


def journeys(D, late_at="station", legs="journey", seats_by="formed", codes_only=False, vehicles="all"):
    """One row per returned questionnaire with its train, its stations coded and the four conditions of the
    respondent's journey. The keywords are the checks' alternative readings: lateness at the train's destination,
    the busiest leg of the whole run, the leading unit's seats, coded stations only, one vehicle per class 166."""
    code = station_coder(D["stations"])
    trains = train_index(D)
    resp = D["resp"].copy()
    if codes_only:
        resp = resp[resp["board_station_code"].notna() & resp["alight_station_code"].notna()]
    fw = D["field"].set_index("batch_id")
    lwd = D["lw"]
    if vehicles == "first":
        lwd = lwd[lwd["vehicle"].isna() | lwd["vehicle"].astype(str).str.endswith("-1")]
    lw = lwd.groupby(["run_date", "headcode", "station", "departed"], as_index=False)["passengers_est"].sum()
    lw_key = {(r.run_date, r.headcode, r.station): r.passengers_est for r in lw.itertuples()}
    form = D["form"]
    units = {}
    for r in form.itertuples():
        units.setdefault((r.run_date, r.headcode), []).append(r.unit_no)
    mv = D["mv"]
    arr = {(r.run_date, r.train_uid, r.station): (r.wtt_time, r.recorded_time) for r in mv[mv["event_type"] == "ARRIVAL"].itertuples()}
    crewed = set(zip(D["crew"]["work_date"], D["crew"]["headcode"]))
    fares = {}
    for r in D["fares"].itertuples():
        pct = (r.fare_from_04jan2026_pence / r.fare_before_pence - 1.0) * 100.0
        fares[(r.from_station, r.to_station, r.ticket_type)] = pct
        fares[(r.to_station, r.from_station, r.ticket_type)] = pct
    out = []
    for r in resp.itertuples():
        b = fw.loc[r.batch_id]
        date = b["fieldwork_date"]
        key = (which_tt(date), b["train_headcode"], days_label(date), b["origin_station"], b["origin_dep"])
        t = trains[key]
        bs = r.board_station_code if isinstance(r.board_station_code, str) and r.board_station_code else code(r.board_station_written)
        als = r.alight_station_code if isinstance(r.alight_station_code, str) and r.alight_station_code else code(r.alight_station_written)
        i, j = t["calls"].index(bs), t["calls"].index(als)
        us = units[(date, b["train_headcode"])]
        seats = sum(seats_on(D, u, date) for u in (us if seats_by == "formed" else us[:1]))
        span = range(i, j) if legs == "journey" else range(0, len(t["calls"]) - 1)
        loads = [lw_key.get((date, b["train_headcode"], t["calls"][x])) for x in span]
        crowded = max(x for x in loads if x is not None) > seats
        at = als if late_at == "station" else t["calls"][-1]
        pl, ac = arr.get((date, t["uid"], at), arr[(date, t["uid"], als)])
        late = late_by(ac, pl) >= K.LATE_MIN
        unstaffed = (date, b["train_headcode"]) not in crewed
        fare = fares[(bs, als, r.ticket_type)] if r.wave == "Spring 2026" else 0.0
        out.append(dict(serial=r.serial, wave=2025 if r.wave == "Spring 2025" else 2026, group=t["group"],
                        board=bs, alight=als, crowded=int(crowded), late=int(late), unstaffed=int(unstaffed),
                        fare=fare, q1=r.q1_overall, weight=r.weight, band=b["time_band"]))
    J = pd.DataFrame(out)
    J["sat"] = np.where(J["q1"].isna(), np.nan, (J["q1"] >= 4).astype(float))
    return J


def wmean(x, w):
    m = ~np.isnan(x)
    return float(np.sum(x[m] * w[m]) / np.sum(w[m]))


def shares(J):
    out = {"overall": {}, "groups": {}}
    for wave in (2025, 2026):
        s = J[J["wave"] == wave]
        out["overall"][wave] = 100 * wmean(s["sat"].values, s["weight"].values)
        for g in K.GROUP_ORDER:
            sg = s[s["group"] == g]
            out["groups"].setdefault(g, {})[wave] = 100 * wmean(sg["sat"].values, sg["weight"].values)
    out["fall"] = out["overall"][2025] - out["overall"][2026]
    return out


DRIVERS = [("crowding", "crowded"), ("punctuality", "late"), ("on-board staffing", "unstaffed"), ("fares", "fare")]


def attribute(J, how="pooled", controls=False):
    """Each driver's points of the fall: the change in the share of journeys meeting it (the fare change in
    per cent for fares) times its effect on the chance of being satisfied, estimated by weighted least squares
    on the respondents of both waves with a wave term (pooled), or on one wave's respondents."""
    import statsmodels.api as sm
    S = J[~J["sat"].isna()].copy()
    w = S["weight"].values
    d = {}
    for name, col in DRIVERS:
        x = S[col].values.astype(float)
        d[col] = np.average(x[S["wave"] == 2026], weights=w[S["wave"] == 2026]) - \
            np.average(x[S["wave"] == 2025], weights=w[S["wave"] == 2025])
    cols = [c for _, c in DRIVERS]
    if how == "pooled":
        X = [S[c].values.astype(float) for c in cols] + [(S["wave"] == 2026).values.astype(float)]
        if controls:
            for g in K.GROUP_ORDER[1:]:
                X.append((S["group"] == g).values.astype(float))
            for bnd in K.TIME_BANDS[1:]:
                X.append((S["band"] == bnd).values.astype(float))
        m = sm.WLS(S["sat"].values, sm.add_constant(np.column_stack(X)), weights=w).fit()
        beta = dict(zip(cols, m.params[1:1 + len(cols)]))
    else:
        msk = (S["wave"] == how).values
        use = [c for c in cols if not (how == 2025 and c == "fare")]
        m = sm.WLS(S["sat"].values[msk], sm.add_constant(np.column_stack([S[c].values[msk].astype(float) for c in use])),
                   weights=w[msk]).fit()
        beta = dict(zip(use, m.params[1:]))
        if "fare" not in beta:
            beta["fare"] = attribute(J)["beta"]["fare"]
    pts = {name: -beta[col] * d[col] * 100 for name, col in DRIVERS}
    return dict(points=pts, beta=beta, delta=d)


def call(J):
    sh = shares(J)
    at = attribute(J)
    pts = at["points"]
    top = max(pts, key=pts.get)
    return dict(shares=sh, points=pts, top=top, top_points=int(np.floor(pts[top] + 0.5)),
                unexplained=sh["fall"] - sum(pts.values()), delta=at["delta"], beta=at["beta"])


# ------------------------------------------------------------------ the plan's baselines (asks)
def latest_days():
    return [d.isoformat() for d in K.WINDOWS["latest"]]


def timetabled(D, dates, days_of=None):
    """Every train in the working timetable for each date: (date, uid, schedule). days_of maps a date to the
    schedules it runs (the timetable's own rule by default: bank holidays run the Sunday schedules)."""
    days_of = days_of or days_label
    tt = D["tt"][D["tt"]["timetable"] == "Dec25"].copy()
    tt["call_seq"] = tt["call_seq"].astype(int)
    by = {}
    for uid, g in tt.groupby("train_uid", sort=False):
        g = g.sort_values("call_seq")
        by[uid] = dict(headcode=g.iloc[0]["headcode"], group=g.iloc[0]["service_group"], days=g.iloc[0]["days_run"],
                       calls=list(g["station"]), arr=list(g["arr"]), dep=list(g["dep"]))
    out = []
    for d in dates:
        lab = days_of(d)
        for uid, t in by.items():
            if t["days"] == lab:
                out.append((d, uid, t))
    return out


def calendar_days(date):
    import datetime as dt
    wd = dt.date.fromisoformat(date).weekday()
    return "SUN" if wd == 6 else ("SAT" if wd == 5 else "MO-FR")


def late_by(actual, planned):
    """Minutes after the planned time, across midnight: the train describer records the clock time only."""
    return (mins(actual) - mins(planned) + 720) % 1440 - 720


def ask_ontime(D, dates=None, midnight=True, base="timetable", days_of=None):
    """2.1 by service group: trains on time at the final destination as a share of the trains in the working
    timetable for the day. The keywords are the checks' mishandlings: clock times subtracted across midnight, the
    trains with movement rows as the base, the calendar's weekdays on the bank holiday."""
    dates = dates or latest_days()
    mv = D["mv"]
    arr = {(r.run_date, r.train_uid, r.station): r.recorded_time for r in mv[mv["event_type"] == "ARRIVAL"].itertuples()}
    ran = set(zip(mv["run_date"], mv["train_uid"]))
    res = {g: [0, 0] for g in K.GROUP_ORDER}
    for d, uid, t in timetabled(D, dates, days_of):
        if base == "ran" and (d, uid) not in ran:
            continue
        res[t["group"]][1] += 1
        a = arr.get((d, uid, t["calls"][-1]))
        if a is None:
            continue
        late = late_by(a, t["arr"][-1]) if midnight else mins(a) - mins(t["arr"][-1])
        if late < 5:
            res[t["group"]][0] += 1
    return {g: 100.0 * v[0] / v[1] for g, v in res.items()}, res


def covers(D, by="turn"):
    """The turns the crew controller's amendments covered: an entry logged in the morning covers the diagram's
    turn that day, one logged in the evening the next day's turn (the turn the original member of staff was
    rostered to, or the vacancy). by="date" reads every entry as covering its own date's turn."""
    import datetime as dt
    out = set()
    for r in D["amend"].itertuples():
        day = dt.date.fromisoformat(r.amend_date)
        if by == "turn" and mins(r.logged) >= 12 * 60:
            day += dt.timedelta(days=1)
        out.add((day.isoformat(), r.diagram))
    return out


def ask_staffed(D, dates=None, cover_by="turn", ran_by="any"):
    """2.2 by service group: trains that ran (in full or part) with on-board staff as a share of trains that ran.
    The keywords are the checks' mishandlings: amendments read by their log date or ignored, and only trains that
    reached their destination counted as having run."""
    dates = dates or latest_days()
    mv = D["mv"]
    if ran_by == "any":
        ran = set(zip(mv["run_date"], mv["train_uid"]))
    else:
        tt = D["tt"][D["tt"]["timetable"] == "Dec25"]
        last = {u: g.sort_values("call_seq", key=lambda x: x.astype(int)).iloc[-1]["station"] for u, g in tt.groupby("train_uid")}
        a = mv[mv["event_type"] == "ARRIVAL"]
        ran = {(r.run_date, r.train_uid) for r in a.itertuples() if last.get(r.train_uid) == r.station}
    covered = covers(D, by=cover_by) if cover_by else set()
    staffed = set()
    for r in D["roster"].itertuples():
        if r.status == "Rostered" or (r.roster_date, r.diagram) in covered:
            for hc in str(r.workings).split(";"):
                staffed.add((r.roster_date, hc))
    res = {g: [0, 0] for g in K.GROUP_ORDER}
    for d, uid, t in timetabled(D, dates):
        if (d, uid) not in ran:
            continue
        res[t["group"]][1] += 1
        if (d, t["headcode"]) in staffed:
            res[t["group"]][0] += 1
    return {g: 100.0 * v[0] / v[1] for g, v in res.items()}, res


def ask_standing(D, dates=None, mods=True, vehicles="all", bank_holiday=False, seats_by="formed", key="unit"):
    """2.3 by service group: for each weekday train due at Marlvale Central 07:00 to 09:59, the load-weigh
    passengers on departure from the station before it less the standard seats of the units formed, where more
    than nothing. The keywords are the checks' readings and mishandlings: the register's seats without the
    modifications, one class 166 vehicle per unit, every vehicle row summed (vehicles="sum"), the bank holiday's
    Sunday trains counted as a weekday's, the leading unit's seats only. Each unit's load is found by the unit, the station and the minute the train left
    it (key="unit"); key="headcode" sums the rows under the train's headcode."""
    import datetime as dt
    dates = dates or latest_days()
    lwd = D["lw"]
    if vehicles == "first":
        lwd = lwd[lwd["vehicle"].isna() | lwd["vehicle"].astype(str).str.endswith("-1")]
    lw = lwd.groupby(["run_date", "headcode", "station"], as_index=False)["passengers_est"].sum()
    lw_key = {(r.run_date, r.headcode, r.station): r.passengers_est for r in lw.itertuples()}
    lwu = lwd.groupby(["run_date", "unit_no", "station", "departed"], as_index=False)["passengers_est"].agg(
        ["sum", "max", "nunique", "count"]).reset_index()
    lw_unit = {}
    for r in lwu.itertuples():
        # a class 166 reports each vehicle; from the May 2026 fleet system move its feed writes the unit's estimate
        # on every vehicle row (the three rows agree), so the unit's load is one row's figure, not the sum
        same = r.count == 3 and r.nunique == 1 and r.run_date >= K.CREW_SYSTEM_MOVE.isoformat()
        lw_unit[(r.run_date, r.unit_no, r.station, r.departed)] = r.max if (same and vehicles != "sum") else r.sum
    dep = {(r.run_date, r.train_uid, r.station): r.recorded_time for r in D["mv"][D["mv"]["event_type"] == "DEPARTURE"].itertuples()}
    units = {}
    for r in D["form"].itertuples():
        units.setdefault((r.run_date, r.headcode), []).append(r.unit_no)
    mv = D["mv"]
    ran_to = {(r.run_date, r.train_uid) for r in mv[(mv["event_type"] == "ARRIVAL") & (mv["station"] == "MVC")].itertuples()}
    reg = {r.Unit: int(r._4) for r in D["units"].itertuples()}
    res = {g: 0 for g in K.INTO_MVC}
    trains = {g: 0 for g in K.INTO_MVC}
    for d, uid, t in timetabled(D, dates):
        day = dt.date.fromisoformat(d)
        if day.weekday() >= 5 or t["calls"][-1] != "MVC":
            continue
        if day in K.BANK_HOLIDAYS and not bank_holiday:
            continue
        a = mins(t["arr"][-1])
        if not (7 * 60 <= a <= 9 * 60 + 59):
            continue
        if (d, uid) not in ran_to:
            continue
        us = units[(d, t["headcode"])]
        if key == "unit":
            when = dep[(d, uid, t["calls"][-2])]
            got = [lw_unit.get((d, u, t["calls"][-2], when)) for u in us]
            n = None if any(x is None for x in got) else sum(got)
        else:
            n = lw_key.get((d, t["headcode"], t["calls"][-2]))
        if n is None:
            continue
        if seats_by == "lead":
            us = us[:1]
        seats = sum(seats_on(D, u, d) if mods else reg[u] for u in us)
        res[t["group"]] += max(0, n - seats)
        trains[t["group"]] += 1
    return res, trains
