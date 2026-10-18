"""task246 golden pipeline, run on the shipped pack only: the zones' figures from the readings and from the children's
own arm circumference, the measurement notes, and the asks (each zone's household response rate, crude death rate and
under-five death rate). Functions take the target folder and the file map."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import estim as E
import params as P

ZONE_CODE = {name: code for code, name, *_r in P.ZONES}


def _p(target, F, k):
    return os.path.join(target, F[k])


def _dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def completed_months(dob, day):
    m = (day.year - dob.year) * 12 + (day.month - dob.month)
    if day.day < dob.day:
        m -= 1
    return m


def sample(target, F):
    s = pd.read_csv(_p(target, F, "sample"))
    return {int(r.cluster): ZONE_CODE[r.zone] for r in s.itertuples()}, s


def sheet(path, name, header_row=1):
    return pd.read_excel(path, sheet_name=name, header=header_row - 1)


# ------------------------------------------------------------------ who read each child
def roster(target, F):
    """(partner, team) -> anthropometrist name before the change, and the dated changes of anthropometrist"""
    t = sheet(_p(target, F, "teams"), "Teams")
    base = {(r.Partner, int(r.Team)): (r.Anthropometrist, r._5) for r in t.itertuples()}
    ch = sheet(_p(target, F, "teams"), "Changes during the round")
    joins = []
    for r in ch.itertuples():
        txt = str(r.Change)
        if "joined team" in txt and "as anthropometrist" in txt:
            name = txt.split(" (")[0]
            code = txt.split("(")[1].split(")")[0]
            joins.append((r.Partner, int(r.Team), _dmy(r.Date), name, code))
    return base, joins


def on_duty(base, joins, partner, team, day):
    who = base[(partner, team)]
    for p, tm, d, name, code in joins:
        if p == partner and tm == team and day >= d:
            who = (name, code)
    return who


def readings(target, F, dedupe=True, age="completed", muac_range=True, ages=(6, 59)):
    """one row per eligible child: zone, MUAC (mm), oedema, the anthropometrist on duty, the day. The options are the
    readings the fork table weighs: dedupe (each child once), age ('completed' months, or 'days' over 30.4375),
    muac_range (the recording-error rule), ages (the eligible ages)"""
    zone, _ = sample(target, F)
    base, joins = roster(target, F)
    out = []
    a = pd.read_csv(_p(target, F, "ncha_anthro"), dtype={"measles": str})
    if dedupe:
        a = a.drop_duplicates(subset=["cluster", "hh_no", "child_no"], keep="first")
    for r in a.itertuples():
        day = dt.date.fromisoformat(r.today)
        dob = _dmy(r.dob)
        am = completed_months(dob, day) if age == "completed" else int((day - dob).days / 30.4375)
        out.append(("NCHA", int(r.team), int(r.cluster), int(r.hh_no), int(r.child_no), day, am, float(r.muac_mm),
                    r.oedema == "y"))
    b = sheet(_p(target, F, "prk_anthro"), "Children")
    for r in b.itertuples():
        day = _dmy(r.Date)
        out.append(("PRK", int(r.Team), int(r.Cluster), int(r.HH), int(r._5), day, int(r._7), float(r._11) * 10.0,
                    int(r.Oedema) == 1))
    df = pd.DataFrame(out, columns=["partner", "team", "cluster", "hh", "line", "day", "age", "muac", "oedema"])
    if dedupe:
        df = df.drop_duplicates(subset=["partner", "cluster", "hh", "line"])
    df = df[(df.age >= ages[0]) & (df.age <= ages[1])]
    if muac_range:
        df = df[(df.oedema) | ((df.muac >= 75) & (df.muac <= 220))]
    df = df.copy()
    df["zone"] = df.cluster.map(zone)
    df["measurer"] = [on_duty(base, joins, p, t, d)[0] for p, t, d in zip(df.partner, df.team, df.day)]
    df["session"] = np.where(df.day < P.REFRESHER, 1, 2)
    return df


def test_table(target, F):
    """(measurer name, session, child, r1, r2, reference) for every anthropometrist, and the supervisor's readings"""
    base, joins = roster(target, F)
    code_name = {v[1]: v[0] for v in base.values()}
    for p, tm, d, name, code in joins:
        code_name[code] = name
    a = pd.read_csv(_p(target, F, "ncha_test"))
    sup = a[a.measured_by == "SUPERVISOR"].pivot_table(index=["session", "test_child"], columns="reading",
                                                         values="muac_mm").reset_index()
    ref = {(int(r.session), r.test_child): (float(r[1]), float(r[2])) for _, r in sup.iterrows()}
    rows = []
    for (who, s, c), g in a[a.measured_by != "SUPERVISOR"].groupby(["measured_by", "session", "test_child"]):
        r1 = float(g[g.reading == 1].muac_mm.iloc[0])
        r2 = float(g[g.reading == 2].muac_mm.iloc[0])
        rows.append((code_name[who], int(s), c, r1, r2, float(np.mean(ref[(int(s), c)]))))
    for s, title in ((1, "Session 1 (10 Jun)"), (2, "Session 2 (28 Jun)")):
        w = sheet(_p(target, F, "prk_test"), title, header_row=4)
        for _, r in w.iterrows():
            c = r["Child"]
            refv = (float(r["Supervisor 1st"]) * 10.0 + float(r["Supervisor 2nd"]) * 10.0) / 2.0
            for col in w.columns:
                if col.endswith(" 1st") and not col.startswith("Supervisor"):
                    name = col[:-4]
                    rows.append((name, s, c, round(float(r[col]) * 10.0, 1), round(float(r[name + " 2nd"]) * 10.0, 1), refv))
    sups = [(s, c, v[0], v[1]) for (s, c), v in ref.items()]
    return rows, sups


def zones(target, F, **opts):
    df = readings(target, F, **opts)
    test, sups = test_table(target, F)
    T = E.test_stats(test)
    st2 = E.supervisor_tem2(sups)
    ZF = {}
    for z in P.ZCODES:
        d = df[df.zone == z]
        rest = d[~d.oedema]
        ZF[z] = E.zone_figures(rest.muac.values, list(rest.measurer), list(rest.session), int(d.oedema.sum()), T, st2)
    return ZF, T, df


def answer(target, F, **opts):
    ZF, T, df = zones(target, F, **opts)
    noted = E.noted(ZF, E.REFERENCE)
    lo = {z: min(ZF[z][k] for k in E.VARIANTS) for z in P.ZCODES}
    hi = {z: max(ZF[z][k] for k in E.VARIANTS) for z in P.ZCODES}
    return dict(ZF=ZF, T=T, df=df, noted=noted, lo=lo, hi=hi)


# ------------------------------------------------------------------ the asks
def form_v4_day(target, F):
    """the first fieldwork day the household form coded an absent household 4: from it, the households coded 4 at a
    first visit are the ones visited again (section 2: a household not at home is visited again, an empty dwelling is
    not); before it, those coded 3 are"""
    v = pd.read_csv(_p(target, F, "visits"))
    v["day"] = [_dmy(d) for d in v.date]
    again = set((int(r.cluster), int(r.hh_no)) for r in v[v.visit == 2].itertuples())
    first = v[(v.visit == 1) & v.outcome.isin([3, 4])]
    back = {}
    for r in first.itertuples():
        back.setdefault(r.day, set()).add(int(r.outcome) if (int(r.cluster), int(r.hh_no)) in again else -int(r.outcome))
    fours = sorted(d for d, s in back.items() if 4 in s)
    threes = sorted(d for d, s in back.items() if 3 in s)
    assert threes[-1] < fours[0], "the codes switch once"
    return fours[0]


V4_OUTCOME = {1: "interviewed", 2: "refused", 3: "empty", 4: "absent"}
V4_REASON = {1: "work", 2: "marriage", 3: "caregiver", 4: "died", 5: "school", 6: "livestock", 7: "household"}


def outcome_codes(target, F, codes="by_period"):
    """the outcome code each form version used. 'by_period' reads the codes before version 4 from which households
    the teams went back to (a household not at home at the first visit is visited again, an empty dwelling is not,
    protocol section 2); 'v4' reads every row with the version 4 codes the dictionary gives"""
    v = pd.read_csv(_p(target, F, "visits"))
    v["day"] = [_dmy(d) for d in v.date]
    if codes == "v4":
        return v, V4_OUTCOME, V4_OUTCOME
    day4 = form_v4_day(target, F)
    again = set((int(r.cluster), int(r.hh_no)) for r in v[v.visit == 2].itertuples())
    first = v[(v.visit == 1) & (v.day < day4) & v.outcome.isin([3, 4])]
    back = {int(r.outcome): 0 for r in first.itertuples()}
    tot = dict(back)
    for r in first.itertuples():
        tot[int(r.outcome)] += 1
        back[int(r.outcome)] += (int(r.cluster), int(r.hh_no)) in again
    absent = max(back, key=lambda k: back[k] / tot[k])
    v3 = {1: "interviewed", 2: "refused", absent: "absent", ({3, 4} - {absent}).pop(): "empty"}
    return v, v3, V4_OUTCOME


def response(target, F, codes="by_period"):
    """each zone's household response rate (protocol section 10): interviewed over selected less empty dwellings, a
    household's outcome its last visit's"""
    zone, _ = sample(target, F)
    v, v3, v4 = outcome_codes(target, F, codes)
    day4 = form_v4_day(target, F)
    out = {}
    for (c, h), g in v.groupby(["cluster", "hh_no"]):
        last = g.sort_values("visit").iloc[-1]
        out[(int(c), int(h))] = (v4 if last.day >= day4 else v3)[int(last.outcome)]
    res = {}
    for z in P.ZCODES:
        o = [x for (c, h), x in out.items() if zone[c] == z]
        res[z] = 100.0 * o.count("interviewed") / (len(o) - o.count("empty"))
    return res


def reason_codes(m, day4, codes="by_period"):
    """each member's reason for leaving. 'by_period' reads the codes before version 4 from who left: of the two codes
    version 4 gives to children who moved with their mother or caregiver and to deaths away from home, the earlier
    code that no one aged 15 or more holds is the move"""
    if codes == "v4":
        return [V4_REASON.get(int(x)) if pd.notna(x) else None for x in m.left_reason]
    early = m[(m.day < day4) & m.left_reason.isin([3, 4])]
    yrs = early.age / np.where(early.age_unit == "months", 12.0, 1.0)
    adult = {k: float((yrs[early.left_reason == k] >= 15).mean()) for k in (3, 4)}
    move = min(adult, key=adult.get)
    v3 = dict(V4_REASON)
    v3[move], v3[({3, 4} - {move}).pop()] = "caregiver", "died"
    return [None if pd.isna(x) else (V4_REASON if d >= day4 else v3)[int(x)] for x, d in zip(m.left_reason, m.day)]


def _members(target, F, dedupe=True):
    m = pd.read_csv(_p(target, F, "members"), dtype={"status": str})
    if dedupe:
        m = m.drop_duplicates(subset=["cluster", "hh_no", "line_no"], keep="first")
    m = m.copy()
    m["day"] = [dt.date.fromisoformat(d) for d in m.interview_date]
    return m


def mortality(target, F, codes="by_period", away=True, births_module=True, dedupe=True, age_unit=True):
    """each zone's crude and under-five death rates per 10,000 per day (protocol section 9). codes: how the reasons
    for leaving are read (reason_codes); away: count members entered as having left because they died away from home
    as deaths; births_module: add the newborns who died, kept on the births module; dedupe: drop a member listed twice
    on the same household; age_unit: read under-five ages in months"""
    zone, s = sample(target, F)
    sub = {int(r.cluster): r.sub_county for r in s.itertuples()}
    start = {k: v[0] for k, v in P.RECALL_START.items()}
    day4 = form_v4_day(target, F)
    m = _members(target, F, dedupe)
    why = reason_codes(m, day4, codes)
    u5 = (m.age_unit == "months").values if age_unit else (m.age < 5).values
    died_away = np.array([(st == "L") and (w == "died") for st, w in zip(m.status, why)]) if away else \
        np.zeros(len(m), bool)
    died = (m.status == "D").values | died_away
    left = (m.status == "L").values & ~died_away
    present = (m.status == "P").values
    jb = ((m.joined == "Yes") | (m.born == "Yes")).values
    hh = {}
    for r, pr, d, l, j, u in zip(m.itertuples(), present, died, left, jb, u5):
        k = (int(r.cluster), int(r.hh_no))
        e = hh.setdefault(k, dict(day=r.day, all=[0.0] * 4, u5=[0.0] * 4))
        for key, w in (("all", True), ("u5", bool(u))):
            if w:
                v = e[key]
                v[0] += pr
                v[1] += j
                v[2] += (l or d)
                v[3] += d
    if births_module:
        bt = pd.read_csv(_p(target, F, "births"))
        for r in bt[bt.outcome == "died"].itertuples():
            k = (int(r.cluster), int(r.hh_no))
            for key in ("all", "u5"):
                v = hh[k][key]
                v[1] += 1          # born in the recall period
                v[2] += 1          # and died in it
                v[3] += 1
    res = {}
    for z in P.ZCODES:
        num = {"all": 0.0, "u5": 0.0}
        den = {"all": 0.0, "u5": 0.0}
        for (c, h), e in hh.items():
            if zone[c] != z:
                continue
            days = (e["day"] - start[sub[c]]).days
            for key in ("all", "u5"):
                cur, j, ld, dead = e[key]
                num[key] += dead
                den[key] += (cur - 0.5 * j + 0.5 * ld) * days
        res[z] = (10000.0 * num["all"] / den["all"], 10000.0 * num["u5"] / den["u5"])
    return res
