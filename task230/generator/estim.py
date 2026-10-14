"""Every figure the task owes, computed from the files under target/ (pandas): the release's coding bias by sub-major
group on the golden route and on every rung of the ladder, and the two asks."""
import os
from datetime import date, datetime

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

import params as P
import world as W

G = W.GROUPS


def load(target):
    f = lambda n: os.path.join(target, n)
    stu = pd.read_csv(f("census2026_coding_quality_study.csv"), dtype=str, keep_default_na=False)
    reg = pd.read_csv(f("census2026_receipt_register.csv"), dtype=str, keep_default_na=False)
    vis = pd.read_csv(f("field_visit_log_jun_oct_2026.csv"), dtype=str, keep_default_na=False)
    ext = pq.read_table(f("census2026_occupation_coding_extract.parquet")).to_pandas()
    eds = pd.read_csv(f("enumeration_districts_2026.csv"), dtype=str, keep_default_na=False)
    staff = pd.read_csv(f("coding_staff_register.csv"), dtype=str, keep_default_na=False)
    moves = pd.read_csv(f("coding_staff_movements_2026.csv"), dtype=str, keep_default_na=False)
    ts = pd.read_csv(f("coding_timesheets_21sep_01nov2026.csv"), dtype=str, keep_default_na=False)
    return dict(stu=stu, reg=reg, vis=vis, ext=ext, eds=eds, staff=staff, moves=moves, ts=ts)


def routes(D, closing="questionnaire"):
    """each form's response route: online, paper, follow-up household member, follow-up proxy"""
    reg = D["reg"].copy()
    vis = D["vis"]
    if closing in ("questionnaire", "sr_as_followup"):
        done = vis[vis.outcome_code.isin(["10", "20"]) & (vis.questionnaire_id != "")]
        done = done.drop_duplicates("questionnaire_id")[["questionnaire_id", "outcome_code"]]
        reg = reg.merge(done, on="questionnaire_id", how="left")
    elif closing == "any_proxy":
        px = set(vis.address_id[vis.outcome_code == "20"])
        reg["outcome_code"] = np.where(reg.address_id.isin(px), "20", "10")
    elif closing == "last_call":
        last = vis[vis.outcome_code.isin(["10", "20"])].sort_values(["address_id", "visit_time"]).drop_duplicates(
            "address_id", keep="last")[["address_id", "outcome_code"]]
        reg = reg.merge(last, on="address_id", how="left")
    elif closing == "first_call":
        first = vis[vis.outcome_code.isin(["10", "20"])].sort_values(["address_id", "visit_time"]).drop_duplicates(
            "address_id", keep="first")[["address_id", "outcome_code"]]
        reg = reg.merge(first, on="address_id", how="left")
    reg["route"] = np.where(reg.capture_mode == "ONLINE", "O", np.where(reg.capture_mode == "PAPER", "P",
                            np.where(reg.outcome_code == "20", "FP", "FS")))
    if closing == "sr_as_followup":
        sr = set(vis.address_id[vis.outcome_code == "60"])
        reg.loc[reg.address_id.isin(sr) & reg.capture_mode.isin(["ONLINE", "PAPER"]), "route"] = "FS"
    return reg


def _grp(codes):
    return np.array([G.index(c[:2]) for c in codes])


def bias_table(D, reg=None, weights="design"):
    """per route: the study's weighted counts of write-ins coded to each group under the rule they were coded under,
    under the 0.80 rule, and put in each group by the reference coding; the coded and still-to-code write-ins"""
    reg = routes(D) if reg is None else reg
    stu = D["stu"].merge(reg[["doc_id", "route"]], on="doc_id", how="left")
    assert stu.route.notna().all()
    w = stu.selection_interval.astype(float).values
    sc = stu.autocoder_score.astype(float).values
    prod = stu.production_code.values
    new = np.where(sc >= P.NEW_ACCEPT, stu.autocoder_code.values, prod)
    g_ref, g_old, g_new = _grp(stu.reference_code.values), _grp(prod), _grp(new)
    ext = D["ext"].merge(reg[["doc_id", "route"]], on="doc_id", how="left")
    nc = ext.route.value_counts().to_dict()
    nr = reg.groupby("route").occupation_writeins.apply(lambda s: s.astype(int).sum()).to_dict()
    K = len(G)
    R = {}
    for r in P.ROUTES:
        m = (stu.route == r).values
        ww = w[m].copy()
        if weights == "poststrat" and m.any():
            ww = ww * nc.get(r, 0) / ww.sum()
        if weights == "unweighted":
            ww = np.ones(m.sum()) * (nc.get(r, 0) / max(m.sum(), 1))
        t = np.bincount(g_ref[m], weights=ww, minlength=K)
        R[r] = dict(t=t, do=np.bincount(g_old[m], weights=ww, minlength=K) - t,
                    dn=np.bincount(g_new[m], weights=ww, minlength=K) - t,
                    co=np.bincount(g_old[m], weights=ww, minlength=K), cn=np.bincount(g_new[m], weights=ww, minlength=K),
                    nc=float(nc.get(r, 0)), n=float(nr.get(r, 0)), sw=float(ww.sum()))
        R[r]["m"] = R[r]["n"] - R[r]["nc"]
    return R


def carry(R, key, groups, denom="ref", factor="coded"):
    """the coded part as studied, and the still-to-code part carried from the studied write-ins of its own groups"""
    D = sum(R[r]["do"] for r in R)
    T = sum(R[r]["t"] for r in R)
    for rs in groups:
        m_ = sum(R[r]["m"] for r in rs)
        n_ = sum(R[r]["nc"] if factor == "coded" else R[r]["sw"] for r in rs)
        if m_ <= 0:
            continue
        D = D + sum(R[r][key] for r in rs) * m_ / n_
        T = T + sum(R[r]["t"] for r in rs) * m_ / n_
    if denom == "coded_less_net":
        C = sum(R[r]["co"] for r in R)
        for rs in groups:
            m_ = sum(R[r]["m"] for r in rs)
            n_ = sum(R[r]["nc"] for r in rs)
            if m_ > 0:
                C = C + sum(R[r]["cn" if key == "dn" else "co"] for r in rs) * m_ / n_
        T = C - D
    return 100 * D / T


def rungs(D, reg=None, weights="design"):
    R = bias_table(D, reg, weights)
    allr = [list(P.ROUTES)]
    bt = [["O", "P"], ["FS", "FP"]]
    each = [[r] for r in P.ROUTES]
    Dc = sum(R[r]["do"] for r in R)
    Tc = sum(R[r]["t"] for r in R)
    return dict(default=100 * Dc / Tc, rule=carry(R, "dn", allr), bt_old=carry(R, "do", bt), bt_new=carry(R, "dn", bt),
                route_old=carry(R, "do", each), golden=carry(R, "dn", each),
                golden_sw=carry(R, "dn", each, factor="sw"), golden_cd=carry(R, "dn", each, denom="coded_less_net")), R


def flags(b, line=P.WARNING):
    return sorted(G[i] for i, v in enumerate(b) if abs(v) > line)


# ------------------------------------------------------------------------------------------------ the asks
def _dt(s):
    return pd.to_datetime(s, format="%Y-%m-%d %H:%M")


def assignments(moves):
    """each person's spells in a team, rebuilt from the movements log: (staff_no, coder_id, team, first day, last day)"""
    out = []
    mv = moves.copy()
    mv["d"] = pd.to_datetime(mv.effective_date)
    for s_, g in mv.sort_values(["d", "movement"]).groupby("staff_no", sort=True):
        cur = None
        for _, r in g.iterrows():
            if r.movement == "STARTED":
                cur = [s_, r.coder_id, r.team_to, r.d]
            elif r.movement == "TRANSFERRED":
                out.append((cur[0], cur[1], cur[2], cur[3], r.d - pd.Timedelta(days=1)))
                cur = [s_, r.coder_id, r.team_to, r.d]
            elif r.movement == "LEFT":
                out.append((cur[0], cur[1], cur[2], cur[3], r.d))
                cur = None
        if cur is not None:
            out.append((cur[0], cur[1], cur[2], cur[3], pd.Timestamp("2099-12-31")))
    return pd.DataFrame(out, columns=["staff_no", "coder_id", "team", "f", "t"])


def team_on(asg, key, ids, days):
    """the team each (id, day) belongs to"""
    out = []
    for i, d in zip(ids, days):
        m = asg[(asg[key] == i) & (asg.f <= d) & (asg.t >= d)]
        out.append(m.team.iloc[0] if len(m) == 1 else ("" if len(m) == 0 else "AMBIGUOUS"))
    return np.array(out, object)


def ask_teams(D, mode="golden"):
    """write-ins each team's coders coded in October (clerical path, coded_at in October, the coder's team that day) and
    the hours its staff logged on occupation coding (OCC lines whose shift started in October, the person's team that
    day); the wrong modes: the current register read for the whole month, a team lead's correction lines dropped, lines
    taken by the date entered"""
    ext = D["ext"]
    asg = assignments(D["moves"])
    cur = D["staff"][D["staff"].role == "CODER"].copy()
    cur["f"] = pd.to_datetime(cur.started)
    cur["t"] = pd.to_datetime(cur.left.replace("", "2099-12-31"))
    c = ext[(ext.coding_path == "CLERICAL") & (ext.coded_at >= "2026-10-01") & (ext.coded_at < "2026-11-01")]
    days = c.coded_at.dt.normalize()
    if mode == "current":
        # the register's team for each coder id, its holder found by the register's own started and left dates
        team = team_on(cur.rename(columns={"f": "f", "t": "t"}), "coder_id", c.coder_id.values, days)
    else:
        team = team_on(asg, "coder_id", c.coder_id.values, days)
    written = pd.Series(team).value_counts().to_dict()
    ts = D["ts"]
    t = ts[(ts.activity == "OCC") & (ts.work_date >= "2026-10-01") & (ts.work_date <= "2026-10-31")].copy()
    if mode == "drop_negative":
        t = t[t.hours.astype(float) > 0]
    if mode == "entered_on":
        t = ts[(ts.activity == "OCC") & (ts.entered_on >= "2026-10-01") & (ts.entered_on <= "2026-10-31")].copy()
    tdays = pd.to_datetime(t.work_date)
    if mode == "current":
        tteam = t.staff_no.map(dict(zip(cur.staff_no, cur.team))).fillna("").values
    else:
        tteam = team_on(asg, "staff_no", t.staff_no.values, tdays)
    hours = pd.Series(t.hours.astype(float).values).groupby(tteam).sum().to_dict()
    return {k: (int(written.get(k, 0)), round(float(hours.get(k, 0.0)), 2)) for k in W.TEAMS}


def ask_regions(D, mode="golden"):
    """follow-up calls made in September by region (the call's own time, each call once) and how many of them made no
    contact (outcome 31); the wrong modes: a dedupe on the call number, an address-and-day dedupe, the sync time"""
    vis = D["vis"]
    eds = D["eds"]
    reg_of = dict(zip(eds.ed_code, eds.region_name))
    v = vis[vis.outcome_code != "60"].copy()
    if mode in ("golden", "synced"):
        # a replacement tablet's first sync re-sent calls already stored: the same call at the same address and minute
        v = v.sort_values(["synced_at", "visit_id"]).drop_duplicates(["address_id", "visit_time", "outcome_code"],
                                                                      keep="first")
    elif mode == "key_dedupe":
        v = v.sort_values(["synced_at", "visit_id"]).drop_duplicates(["address_id", "visit_no"], keep="first")
    elif mode == "day_dedupe":
        v = v.assign(d=v.visit_time.str[:10]).sort_values(["synced_at", "visit_id"]).drop_duplicates(
            ["address_id", "d", "outcome_code"], keep="first")
    when = v.synced_at if mode == "synced" else v.visit_time
    oc = v[(when >= "2026-09-01") & (when < "2026-10-01")]
    calls = oc.ed_code.map(reg_of).value_counts().to_dict()
    nc = oc[oc.outcome_code == "31"].ed_code.map(reg_of).value_counts().to_dict()
    return {name: (int(calls.get(name, 0)), int(nc.get(name, 0))) for _, name, _ in W.REGIONS}


# ------------------------------------------------------------------------------------------------ reflex routes (checks)
def _load_date(lb):
    return pd.to_datetime("20" + lb.str[-6:], format="%Y%m%d")


def reflex_recent(D, weeks=4):
    """carry the still-to-code follow-up write-ins from the follow-up batches loaded in the last weeks before the coding
    front, under the 0.80 rule (self-response from self-response)"""
    reg = routes(D)
    R = bias_table(D, reg)
    stu = D["stu"].merge(reg[["doc_id", "route"]], on="doc_id")
    fu = stu[stu.batch_type == "FOLLOW-UP"].copy()
    ld = _load_date(fu.load_batch)
    last = ld.max()
    rec = fu[ld > last - pd.Timedelta(days=7 * weeks)]
    w = rec.selection_interval.astype(float).values
    sc = rec.autocoder_score.astype(float).values
    new = np.where(sc >= P.NEW_ACCEPT, rec.autocoder_code.values, rec.production_code.values)
    K = len(G)
    t = np.bincount(_grp(rec.reference_code.values), weights=w, minlength=K)
    dn = np.bincount(_grp(new), weights=w, minlength=K) - t
    Dn = sum(R[r]["do"] for r in R)
    Tn = sum(R[r]["t"] for r in R)
    m_fu = R["FS"]["m"] + R["FP"]["m"]
    Dn = Dn + dn * m_fu / w.sum()
    Tn = Tn + t * m_fu / w.sum()
    m_s = R["O"]["m"] + R["P"]["m"]
    n_s = R["O"]["nc"] + R["P"]["nc"]
    Dn = Dn + (R["O"]["dn"] + R["P"]["dn"]) * m_s / n_s
    Tn = Tn + (R["O"]["t"] + R["P"]["t"]) * m_s / n_s
    return 100 * Dn / Tn


def reflex_trend(D):
    """fit each group's follow-up net error rate (0.80 rule) and reference rate on the load date and read them at the
    still-to-code follow-up forms' mean received date"""
    reg = routes(D)
    R = bias_table(D, reg)
    stu = D["stu"].merge(reg[["doc_id", "route"]], on="doc_id")
    fu = stu[stu.batch_type == "FOLLOW-UP"].copy()
    x = (_load_date(fu.load_batch) - pd.Timestamp("2026-06-22")).dt.days.values.astype(float)
    w = fu.selection_interval.astype(float).values
    sc = fu.autocoder_score.astype(float).values
    new = np.where(sc >= P.NEW_ACCEPT, fu.autocoder_code.values, fu.production_code.values)
    gref, gnew = _grp(fu.reference_code.values), _grp(new)
    coded_docs = set(D["ext"].doc_id)
    rem = reg[(reg.capture_mode == "FIELD") & ~reg.doc_id.isin(coded_docs)]
    xr = (pd.to_datetime(rem.received_date) - pd.Timestamp("2026-06-22")).dt.days.values.astype(float)
    nr = rem.occupation_writeins.astype(int).values
    x0 = float((xr * nr).sum() / nr.sum())
    K = len(G)
    Dn = sum(R[r]["do"] for r in R)
    Tn = sum(R[r]["t"] for r in R)
    m_fu = R["FS"]["m"] + R["FP"]["m"]
    X = np.vstack([np.ones_like(x), x]).T
    for i in range(K):
        yd = (gnew == i).astype(float) - (gref == i).astype(float)
        yt = (gref == i).astype(float)
        bd = np.linalg.lstsq(X * np.sqrt(w)[:, None], yd * np.sqrt(w), rcond=None)[0]
        bt = np.linalg.lstsq(X * np.sqrt(w)[:, None], yt * np.sqrt(w), rcond=None)[0]
        Dn[i] += (bd[0] + bd[1] * x0) * m_fu
        Tn[i] += (bt[0] + bt[1] * x0) * m_fu
    m_s = R["O"]["m"] + R["P"]["m"]
    n_s = R["O"]["nc"] + R["P"]["nc"]
    Dn = Dn + (R["O"]["dn"] + R["P"]["dn"]) * m_s / n_s
    Tn = Tn + (R["O"]["t"] + R["P"]["t"]) * m_s / n_s
    return 100 * Dn / Tn


def reflex_recode_all(D):
    """the 0.80 rule applied to every write-in, the coded ones too, carried by route"""
    R = bias_table(D)
    Dn = sum(R[r]["dn"] * R[r]["n"] / R[r]["nc"] for r in R)
    Tn = sum(R[r]["t"] * R[r]["n"] / R[r]["nc"] for r in R)
    return 100 * Dn / Tn


def within_route_trend(D):
    """the slope of the follow-up proxy and household-member studied write-ins' net error rate on the load date, and the
    pooled follow-up slope, for the groups the carry moves most"""
    reg = routes(D)
    stu = D["stu"].merge(reg[["doc_id", "route"]], on="doc_id")
    fu = stu[stu.batch_type == "FOLLOW-UP"].copy()
    fu["wk"] = (_load_date(fu.load_batch) - pd.Timestamp("2026-06-22")).dt.days // 14
    fu["w"] = fu.selection_interval.astype(float)
    fu["px"] = (fu.route == "FP").astype(float)
    by = fu.groupby("wk").apply(lambda g: pd.Series({"px": (g.px * g.w).sum() / g.w.sum(), "n": g.w.sum()}))
    return by


def carry_finer(D, cols):
    """the golden carry inside finer cells: route by region, route by proxy respondent (a check that the grain is not a
    fork)"""
    reg = routes(D).merge(D["eds"][["ed_code", "region_code"]], on="ed_code")
    vis = D["vis"]
    px = vis[(vis.outcome_code == "20") & (vis.questionnaire_id != "")].drop_duplicates("questionnaire_id")[
        ["questionnaire_id", "proxy_respondent"]]
    reg = reg.merge(px, on="questionnaire_id", how="left")
    reg["cell"] = reg.route + "|" + reg[cols].fillna("").astype(str).agg("|".join, axis=1)
    stu = D["stu"].merge(reg[["doc_id", "cell"]], on="doc_id")
    ext = D["ext"].merge(reg[["doc_id", "cell"]], on="doc_id")
    nc = ext.cell.value_counts()
    nr = reg.groupby("cell").occupation_writeins.apply(lambda s: s.astype(int).sum())
    w = stu.selection_interval.astype(float).values
    sc = stu.autocoder_score.astype(float).values
    new = np.where(sc >= P.NEW_ACCEPT, stu.autocoder_code.values, stu.production_code.values)
    gr, go, gn = _grp(stu.reference_code.values), _grp(stu.production_code.values), _grp(new)
    K = len(G)
    D_, T_ = np.zeros(K), np.zeros(K)
    for cell, idx in stu.groupby("cell").indices.items():
        ww = w[idx]
        t = np.bincount(gr[idx], weights=ww, minlength=K)
        f = (nr.get(cell, 0) - nc.get(cell, 0)) / nc.get(cell, 1)
        D_ += np.bincount(go[idx], weights=ww, minlength=K) - t + (np.bincount(gn[idx], weights=ww, minlength=K) - t) * f
        T_ += t + t * f
    return 100 * D_ / T_
