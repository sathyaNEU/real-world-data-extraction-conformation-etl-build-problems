"""Every figure the task owes, computed from the shipped bundle alone (target/), and every rung of the ladder.

    python3 task200/generator/solve.py [target]
"""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pack import F  # noqa: E402

LONDON = "Europe/London"
TEAMS = ["Arden", "Brook", "Cleve", "Dene", "Esk", "Fell"]
CUTOFF = pd.Timestamp("2027-07-01")


def _p(target, key):
    return os.path.join(target, F[key])


# ----------------------------------------------------------------------------------------------- loading
def roster(target):
    r = pd.read_excel(_p(target, "roster"), sheet_name="Roster")
    r["Staff no"] = r["Staff no"].astype(int)
    r["ID badge"] = r["ID badge"].astype(int).astype(str)
    r["Pier B TIP operator"] = r["Pier B TIP operator"].astype(str).str.zfill(3)
    return r


def badge_staff(target, events, ros, use_register=True):
    """staff number for each screen event's badge: the badge valid on the event's date in the ID Centre register, or
    (use_register False) the roster's current badge only"""
    if not use_register:
        m = dict(zip(ros["ID badge"], ros["Staff no"]))
        return events.Badge.map(m)
    reg = pd.read_csv(_p(target, "badges"), dtype=str, keep_default_na=False)
    reg["issued"] = pd.to_datetime(reg.issued, format="%d/%m/%Y")
    reg["cancelled"] = pd.to_datetime(reg.cancelled.replace("", None), format="%d/%m/%Y")
    day = events.t.dt.tz_convert(LONDON).dt.tz_localize(None).dt.normalize()
    out = pd.Series(np.nan, index=events.index)
    for b, g in reg.groupby("badge_no"):
        idx = events.index[events.Badge == b]
        if not len(idx):
            continue
        for _, row in g.iterrows():
            ok = (day[idx] >= row.issued) & ((day[idx] < row.cancelled) if pd.notna(row.cancelled) else True)
            out[idx[ok.values]] = int(row.staff_no)
    return out


def tip_with_duplicates(target, ros):
    return tip(target, ros, dedupe=False)


def tip(target, ros, dedupe=True):
    parts = []
    for k in ("ct24", "ct25", "ct26"):
        d = pd.read_csv(_p(target, k), dtype=str, keep_default_na=False)
        parts.append(d)
    ct = pd.concat(parts, ignore_index=True)
    n_raw = len(ct)
    if dedupe:
        ct = ct.drop_duplicates().reset_index(drop=True)
    ct["ts"] = pd.to_datetime(ct.projection_utc, utc=True)
    login2staff = dict(zip(ros["CT login"], ros["Staff no"]))
    ct["who"] = "CT:" + ct.operator_login
    ct["staff"] = ct.operator_login.map(login2staff)
    ct["area"] = "Central"
    ct["image"] = ct.tip_image
    ct["cls"] = ct.threat_class.str.title().replace({"Ied": "IED"})
    ct["res"] = ct.result.map({"HIT": "hit", "MISS": "miss", "CANCELLED": "cancelled"})
    ct["seq"] = np.arange(len(ct))
    pb = pd.read_csv(_p(target, "pb"), dtype=str, keep_default_na=False, skiprows=3)
    loc = pd.to_datetime(pb.Date + " " + pb.Time, format="%d/%m/%Y %H:%M:%S")
    pb["ts"] = loc.dt.tz_localize(LONDON, ambiguous="raise", nonexistent="raise").dt.tz_convert("UTC")
    op2staff = dict(zip(ros["Pier B TIP operator"], ros["Staff no"]))
    pb["staff"] = pb.Operator.str.zfill(3).map(op2staff)
    pb["area"] = "Pier B"
    pb["image"] = pb.Image
    pb["cls"] = pb.Class.map({"A": "IED", "B": "Firearm", "C": "Knife", "D": "Other"})
    pb["res"] = pb.Result.map({"H": "hit", "M": "miss", "X": "cancelled"})
    pb["seq"] = np.arange(len(pb)) + len(ct)
    # one person, one history: a member who screened in both areas is the same staff number in both systems
    ct["person"] = ct.staff.map(lambda v: "S%d" % v if pd.notna(v) else None).fillna(ct.who)
    pb["person"] = pb.staff.map(lambda v: "S%d" % v if pd.notna(v) else None).fillna("PB:" + pb.Operator)
    cols = ["ts", "seq", "person", "staff", "area", "image", "cls", "res"]
    allp = pd.concat([ct[cols], pb[cols]], ignore_index=True).sort_values(["ts", "seq"]).reset_index(drop=True)
    shown = allp.res != "cancelled"
    allp["k"] = -1
    allp.loc[shown, "k"] = allp[shown].groupby(["person", "image"]).cumcount().values
    allp["cum_area"] = -1
    allp.loc[shown, "cum_area"] = allp[shown].groupby(["person", "area"]).cumcount().values
    allp["year"] = allp.ts.dt.tz_convert(LONDON).dt.year
    team = dict(zip(ros["Staff no"], ros["Team"]))
    allp["team"] = allp.staff.map(team)
    allp.attrs["ct_raw_rows"] = n_raw
    return allp


def year26(allp):
    t = allp[(allp.year == 2026) & (allp.res != "cancelled") & allp.team.notna()].copy()
    t["hit"] = (t.res == "hit").astype(int)
    return t


# ----------------------------------------------------------------------------------------------- the call
def order_of(series):
    return list(series.sort_values(kind="mergesort").index)


def main_call(allp):
    t = year26(allp)
    raw = t.groupby("team").hit.mean()
    first = t[t.k == 0].groupby("team").hit.agg(["sum", "size", "mean"])
    met = t[t.k > 0].groupby("team").hit.agg(["sum", "size", "mean"])
    share_first = (t.k == 0).groupby(t.team).mean()
    return dict(t=t, raw=raw, first=first, met=met, share_first=share_first,
                golden_order=order_of(first["mean"]), raw_order=order_of(raw))


def rung_dprime(t, clear, hours, trays_per_hour=150.0):
    from scipy.stats import norm
    raw = t.groupby("team").hit.mean().reindex(TEAMS)
    fa = (clear.reindex(TEAMS) / (hours.reindex(TEAMS) * trays_per_hour)).astype(float)
    return pd.Series(norm.ppf(raw.values) - norm.ppf(fa.values), index=TEAMS)


def _logit(y, X):
    import statsmodels.api as sm
    return sm.Logit(y, X).fit(disp=0, maxiter=200)


def design(t, k=False, practice=False):
    X = pd.get_dummies(t.team).reindex(columns=TEAMS, fill_value=0).astype(float)
    pb = (t.area == "Pier B").astype(float).values
    # the screening area enters only where it is not one team's own column
    if not np.array_equal(pb, X["Fell"].values):
        X["pierb"] = pb
    for c in ("IED", "Firearm", "Knife"):
        X[c] = (t.cls == c).astype(float).values
    if practice:
        X["log_practice"] = np.log1p(t.cum_area.values.astype(float))
    if k:
        for kk in (1, 2, 3):
            X["met%d" % kk] = (t.k.values >= kk).astype(float)
    return X


def model_rates(t, k=False, practice=False):
    """each team's predicted chance read on the airport's whole 2026 mix of projections (threat classes, practice to
    date, screening area where it is not the team's own column), and, where the model knows the earlier meetings, as if
    every projection were a first meeting"""
    X = design(t, k=k, practice=practice)
    m = _logit(t.hit.values.astype(float), X.values)
    out = {}
    for team in TEAMS:
        Z = X.copy()
        for tt in TEAMS:
            Z[tt] = 1.0 if tt == team else 0.0
        if "pierb" in Z:
            Z["pierb"] = 0.0
        if k:
            for kk in (1, 2, 3):
                Z["met%d" % kk] = 0.0
        p = 1.0 / (1.0 + np.exp(-(Z.values @ m.params)))
        out[team] = float(p.mean())
    return pd.Series(out)


def rungs(allp, A, B):
    t = year26(allp)
    out = {}
    out["R0 raw"] = t.groupby("team").hit.mean()
    out["R1 dprime"] = rung_dprime(t, B["golden"], A["golden"])
    out["R2 logit area class"] = model_rates(t)
    out["R3 logit practice"] = model_rates(t, practice=True)
    out["R4 central only"] = t[t.area == "Central"].groupby("team").hit.mean()
    out["G first meetings"] = t[t.k == 0].groupby("team").hit.mean()
    out["G member mean"] = t[t.k == 0].groupby(["team", "staff"]).hit.mean().groupby("team").mean()
    out["G logit met"] = model_rates(t, k=True)
    return out


# ----------------------------------------------------------------------------------------------- ask A: screen time
def ct_sessions(target):
    d = pd.read_csv(_p(target, "ctpos"), dtype=str, keep_default_na=False)
    d["on"] = pd.to_datetime(d.logon_utc, utc=True)
    d["off"] = pd.to_datetime(d.logoff_utc, utc=True)
    return d


def pb_events(target):
    e = pd.read_csv(_p(target, "pbev"), dtype=str, keep_default_na=False)
    loc = pd.to_datetime(e.Date + " " + e.Time, format="%d/%m/%Y %H:%M:%S")
    e["t"] = loc.dt.tz_localize(LONDON, ambiguous="raise", nonexistent="raise").dt.tz_convert("UTC")
    e["n"] = np.arange(len(e))
    return e


def union_seconds(df, key):
    tot = {}
    for who, g in df.sort_values([key, "on", "off"]).groupby(key, sort=True):
        s = 0.0
        cur0 = cur1 = None
        for a, b in zip(g.on, g.off):
            if cur1 is None or a > cur1:
                if cur1 is not None:
                    s += (cur1 - cur0).total_seconds()
                cur0, cur1 = a, b
            elif b > cur1:
                cur1 = b
        if cur1 is not None:
            s += (cur1 - cur0).total_seconds()
        tot[who] = s
    return pd.Series(tot)


def pb_logged(e, route="golden"):
    """logged-on intervals at the Pier B screens. golden: a log-on lasts until the operator's own log-off, the next
    log-on at that screen or the screen's shutdown, whichever comes first. own: until the operator's own log-off at
    that screen or the shutdown. paired: only log-ons with their own log-off before the next log-on."""
    rows = []
    for scr, g in e.sort_values(["t", "n"]).groupby("Screen", sort=True):
        cur = None
        for ev, badge, t in zip(g.Event, g.Badge, g.t):
            if ev == "LOGON":
                if cur is not None:
                    if route == "golden":
                        rows.append((cur[0], cur[1], t))
                        cur = None
                    elif route == "paired":
                        cur = None
                if route == "own":
                    rows.append(["open", badge, t, None, scr])
                cur = (badge, t)
            elif ev == "LOGOFF":
                if route == "own":
                    for rr in rows[::-1]:
                        if rr[0] == "open" and rr[1] == badge and rr[4] == scr:
                            rr[0] = "done"
                            rr[3] = t
                            break
                elif cur is not None and cur[0] == badge:
                    rows.append((cur[0], cur[1], t))
                    cur = None
            elif ev == "SHUTDOWN":
                if route == "own":
                    for rr in rows:
                        if rr[0] == "open" and rr[4] == scr:
                            rr[0] = "done"
                            rr[3] = t
                elif cur is not None and route == "golden":
                    rows.append((cur[0], cur[1], t))
                cur = None
    if route == "own":
        rows = [(b, a, c) for _s, b, a, c, _x in rows if c is not None]
    d = pd.DataFrame(rows, columns=["badge", "on", "off"])
    return d


def ask_hours(target, ros, ct_route="union", pb_route="golden", register=True):
    c = ct_sessions(target)
    c = c[c.on.dt.tz_convert(LONDON).dt.year == 2026]
    if ct_route == "union":
        cs = union_seconds(c, "login")
    else:
        cs = ((c.off - c.on).dt.total_seconds()).groupby(c.login).sum()
    e = pb_events(target)
    b = pb_logged(e, pb_route)
    b = b[b.on.dt.tz_convert(LONDON).dt.year == 2026].reset_index(drop=True)
    staff = badge_staff(target, b.rename(columns={"badge": "Badge"}).assign(t=b.on), ros, register)
    staff_team = dict(zip(ros["Staff no"], ros["Team"]))
    bt = staff.map(lambda v: staff_team.get(int(v)) if pd.notna(v) else None)
    bs = ((b.off - b.on).dt.total_seconds()).groupby(bt).sum()
    login_team = dict(zip(ros["CT login"], ros["Team"]))
    hrs = pd.Series(0.0, index=TEAMS)
    for k, v in cs.items():
        if k in login_team:
            hrs[login_team[k]] += v
    for k, v in bs.items():
        if k in hrs.index:
            hrs[k] += v
    return hrs / 3600.0


# ----------------------------------------------------------------------------------------------- ask B: clear searches
def ask_clear(target, ros, split=True, by="reject", register=True):
    s = pd.read_csv(_p(target, "search"), dtype=str, keep_default_na=False)
    s["taken"] = pd.to_datetime(s.taken_local, format="%Y-%m-%d %H:%M:%S").dt.tz_localize(
        LONDON, ambiguous="raise", nonexistent="raise").dt.tz_convert("UTC")
    s["clear"] = s.outcome.isin(["NF", "CLEAR"])
    s = s[s.clear]
    if split:
        s = s.assign(tray=s.tray_tag.str.split(";")).explode("tray")
    else:
        s = s.assign(tray=s.tray_tag.str.split(";").str[0])
    rj = pd.read_csv(_p(target, "rej"), dtype=str, keep_default_na=False)
    rj["t"] = pd.to_datetime(rj.reject_utc, utc=True)
    e = pb_events(target)
    pbr = e[e.Event == "REJECT"][["t", "Tray", "Badge"]].rename(columns={"Tray": "tray"})
    c = ct_sessions(target)
    login_team = dict(zip(ros["CT login"], ros["Team"]))
    s = s.reset_index(drop=True)
    s["q"] = np.arange(len(s))
    s["tray"] = s.tray.astype(object)
    rj["tray_tag"] = rj.tray_tag.astype(object)
    rj["workstation"] = rj.workstation.astype(object)
    pbr = pbr.assign(tray=pbr.tray.astype(object))
    c["workstation"] = c.workstation.astype(object)
    # the latest reject of the same tray before the search was taken
    cs = s[s.area == "Central"].sort_values("taken")
    r1 = rj.rename(columns={"tray_tag": "tray"}).sort_values("t")
    m = pd.merge_asof(cs, r1[["t", "tray", "workstation"]], left_on="taken", right_on="t", by="tray",
                      direction="backward", allow_exact_matches=False)
    m = m.dropna(subset=["t"])
    # who was logged on at that workstation then: the workstation's rows merged into one interval per log-on
    w = workstation_spans(c)
    w["workstation"] = w.workstation.astype(object)
    m = m.sort_values("t")
    m["workstation"] = m.workstation.astype(object)
    m2 = pd.merge_asof(m, w, left_on="t", right_on="on", by="workstation", direction="backward")
    m2 = m2[m2.off > m2.t]
    teams_c = m2.login.map(login_team)
    bs = s[s.area == "Pier B"].sort_values("taken")
    mb = pd.merge_asof(bs, pbr.sort_values("t"), left_on="taken", right_on="t", by="tray", direction="backward",
                       allow_exact_matches=False).dropna(subset=["t"])
    staff_team = dict(zip(ros["Staff no"], ros["Team"]))
    mb = mb.reset_index(drop=True)
    sb = badge_staff(target, mb, ros, register)
    teams_b = sb.map(lambda v: staff_team.get(int(v)) if pd.notna(v) else None)
    allteams = pd.concat([teams_c, teams_b]).dropna()
    return allteams.value_counts().reindex(TEAMS, fill_value=0).astype(int)


def workstation_spans(c):
    rows = []
    for (ws, lg), g in c.sort_values(["workstation", "login", "on"]).groupby(["workstation", "login"], sort=True):
        cur0 = cur1 = None
        for a, b in zip(g.on, g.off):
            if cur1 is None or a > cur1:
                if cur1 is not None:
                    rows.append((ws, lg, cur0, cur1))
                cur0, cur1 = a, b
            elif b > cur1:
                cur1 = b
        if cur1 is not None:
            rows.append((ws, lg, cur0, cur1))
    return pd.DataFrame(rows, columns=["workstation", "login", "on", "off"]).sort_values("on").reset_index(drop=True)


# ----------------------------------------------------------------------------------------------- ask C: certificates
def ask_certs(target, ros, route="golden"):
    """golden: every certification a rostered screener holds, the LMS's passes with each EXT-IIC on its assessment date
    in the centre's list, and the centre's certificates the LMS does not yet hold, by candidate staff number; joined:
    the LMS's passes with each EXT-IIC dated through its certificate reference, nothing else; lms: the LMS's passes on
    their LMS dates; lms_plus: the LMS dates, with the centre's certificates the LMS does not yet hold added"""
    lms = pd.read_excel(_p(target, "lms"), sheet_name="Assessments")
    lms["Staff no"] = lms["Staff no"].astype(int)
    cen = pd.read_csv(_p(target, "certs"), dtype=str, keep_default_na=False)
    cen_date = dict(zip(cen.certificate_no, pd.to_datetime(cen.assessment_date, format="%d/%m/%Y")))
    cert = lms[lms["Course code"].isin(["IIC", "EXT-IIC"]) & (lms.Result == "PASS")].copy()
    if route in ("golden", "joined"):
        cert["day"] = [cen_date[ref] if code == "EXT-IIC" else d for code, ref, d in
                       zip(cert["Course code"], cert["Certificate ref"].fillna(""), cert["Completed"])]
    else:
        cert["day"] = cert["Completed"]
    cert = cert[["Staff no", "day"]]
    if route in ("golden", "lms_plus"):
        held = set(lms["Certificate ref"].fillna(""))
        extra = cen[~cen.certificate_no.isin(held)]
        cert = pd.concat([cert, pd.DataFrame({"Staff no": extra.candidate_staff_no.astype(int).values,
                                              "day": pd.to_datetime(extra.assessment_date, format="%d/%m/%Y").values})],
                         ignore_index=True)
    last = cert.groupby("Staff no").day.max()
    exp = last.map(lambda d: d.replace(year=d.year + 3))
    team = dict(zip(ros["Staff no"], ros["Team"]))
    out = pd.Series(0, index=TEAMS)
    for sno, x in exp.items():
        if sno in team and x < CUTOFF:
            out[team[sno]] += 1
    return out


def solve(target):
    ros = roster(target)
    allp = tip(target, ros)
    M = main_call(allp)
    A = {"golden": ask_hours(target, ros), "cracker": ask_hours(target, ros, "rows", "golden", register=False),
         "mirror": ask_hours(target, ros, "rows", "paired", register=False),
         "union_roster": ask_hours(target, ros, "union", "golden", register=False),
         "rows_register": ask_hours(target, ros, "rows", "golden", register=True)}
    B = {"golden": ask_clear(target, ros), "cracker": ask_clear(target, ros, split=False, register=False),
         "mirror": ask_clear(target, ros, split=False, register=True),
         "split_roster": ask_clear(target, ros, split=True, register=False)}
    C = {"golden": ask_certs(target, ros), "lms": ask_certs(target, ros, "lms"),
         "joined": ask_certs(target, ros, "joined"), "lms_plus": ask_certs(target, ros, "lms_plus")}
    R = rungs(allp, A, B)
    return dict(roster=ros, tip=allp, main=M, A=A, B=B, C=C, rungs=R)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    S = solve(t)
    M = S["main"]
    print("golden order", M["golden_order"])
    print(M["first"].round(4))
    print("raw", M["raw"].round(4).to_dict())
    for k, v in S["rungs"].items():
        print("%-22s" % k, [x for x in v.sort_values(kind="mergesort").index], v.round(3).to_dict())
    for k, v in S["A"].items():
        print("A", k, v.round(1).to_dict())
    for k, v in S["B"].items():
        print("B", k, v.to_dict())
    for k, v in S["C"].items():
        print("C", k, v.to_dict())
