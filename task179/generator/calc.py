"""The golden and the routes around it, computed from the shipped files under target/ only."""
import datetime as dt
import os
import numpy as np
import pandas as pd
import core as C

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
DAY0 = dt.date(2026, 5, 25)
COMPLETE = dt.date(2026, 10, 11)
BASE0 = dt.date(2026, 8, 31)
CUT_FROM = dt.date(2026, 11, 2)
WIN0, WIN1 = dt.date(2026, 11, 30), dt.date(2026, 12, 27)
CUT = 0.5


def day(d):
    return (d - DAY0).days


def parse_date(s):
    s = str(s).strip()
    if not s or s == "nan":
        return None
    if "-" in s:
        return dt.date.fromisoformat(s[:10])
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def load(target=TARGET):
    ll = pd.read_csv(os.path.join(target, "tvd_line_list_dunmarrow_2026-10-18.csv"), dtype=str,
                     encoding="utf-8-sig", keep_default_na=False)
    ch = pd.read_csv(os.path.join(target, "tvd_transmission_links_2026-10-18.csv"), dtype=str, keep_default_na=False)
    return ll, ch


def cases_table(ll, dedup=True):
    c = ll[ll["classification"].isin(["Confirmed", "Probable"])].copy()
    c["onset"] = [day(parse_date(x)) for x in c["date_of_onset"]]
    c["notif"] = [day(parse_date(x)) for x in c["date_of_notification"]]
    alias = {}
    if dedup:
        conf = c[c["sample_id"] != ""].sort_values(["notif", "case_number"], kind="stable")
        first = {}
        keep = []
        for r in conf.itertuples():
            if r.sample_id in first:
                alias[r.case_number] = first[r.sample_id]
            else:
                first[r.sample_id] = r.case_number
        c = c[~c["case_number"].isin(alias)]
    return c, alias


def pairs(c, ch, alias, last_day):
    onset = dict(zip(c["case_number"], c["onset"]))
    s = [alias.get(x, x) for x in ch["Source person"]]
    t = [alias.get(x, x) for x in ch["Target person"]]
    pi, pj = [], []
    seen = set()
    for a, b in zip(s, t):
        if a in onset and b in onset and (a, b) not in seen:
            seen.add((a, b))
            if onset[b] <= last_day:
                pi.append(onset[a])
                pj.append(onset[b])
    pi, pj = np.array(pi), np.array(pj)
    return pi, pj, pj - pi


def daily_counts(c, last_day):
    on = c["onset"].values
    return np.bincount(on[on <= last_day], minlength=last_day + 1).astype(float)


def the_call(target=TARGET, gi="trunc_gamma", growth="ols_daily", dedup=True, last=None):
    ll, ch = load(target)
    c, alias = cases_table(ll, dedup)
    T = day(COMPLETE) if last is None else last
    pi, pj, lags = pairs(c, ch, alias, T)
    lags_ok = lags >= 1
    pi, pj, lags = pi[lags_ok], pj[lags_ok], lags[lags_ok]
    daily = daily_counts(c, day(COMPLETE))
    if gi == "trunc_gamma":
        w, _ = C.fit_lags(lags, pi, T, "gamma", True)
    elif gi == "trunc_weibull":
        w, _ = C.fit_lags(lags, pi, T, "weibull", True)
    elif gi == "trunc_lognorm":
        w, _ = C.fit_lags(lags, pi, T, "lognorm", True)
    elif gi == "npmle":
        w = C.reverse_time_npmle(lags, pi, T)
    elif gi.startswith("complete"):
        k = int(gi.split("_")[1])
        w = C.empirical(lags[pi <= T - k])
    elif gi == "naive_gamma":
        w, _ = C.fit_lags(lags, pi, T, "gamma", False)
    elif gi == "naive_empirical":
        w = C.empirical(lags)
    elif gi == "literature":
        w = C.dgamma_pmf(15.3, 9.3)
    b0, b1 = day(BASE0), day(COMPLETE)
    if growth == "ols_daily":
        r = C.growth_rate(daily, b0, b1)
    elif growth == "poisson_daily":
        r = C.growth_rate_poisson(daily, b0, b1)
    elif growth == "ols_weekly":
        wk = np.array([daily[d:d + 7].sum() for d in range(b0, b1 + 1, 7)])
        r = float(np.polyfit(np.arange(len(wk)) * 7.0, np.log(wk), 1)[0])
    R = C.R_from_growth(r, w)
    x = C.project(daily, b1, R, w, CUT, day(CUT_FROM), day(WIN1))
    total = float(x[day(WIN0):day(WIN1) + 1].sum())
    weekly = [float(x[day(WIN0) + 7 * k: day(WIN0) + 7 * k + 7].sum()) for k in range(4)]
    return {"total": total, "weekly": weekly, "R": R, "r": r, "mean_si": C.mean_of(w), "n_pairs": int(len(lags)),
            "n_cases": int((c["onset"] <= b1).sum()), "series": x}


if __name__ == "__main__":
    for gi in ["trunc_gamma", "trunc_weibull", "npmle", "trunc_lognorm", "complete_50", "complete_60", "naive_gamma", "naive_empirical", "literature"]:
        o = the_call(gi=gi)
        print("%-16s total %8.0f R %.3f mean %.2f pairs %d cases %d" % (gi, o["total"], o["R"], o["mean_si"], o["n_pairs"], o["n_cases"]))
    for g in ["poisson_daily", "ols_weekly"]:
        o = the_call(growth=g); print(g, round(o["total"]), round(o["R"], 3))


def variant(kind, target=TARGET):
    """Routes around the golden for the screens: Layer 1 mishandlings and reflexes."""
    ll, ch = load(target)
    T = day(COMPLETE)
    if kind == "no_dedup":
        c, alias = cases_table(ll, dedup=False)
    else:
        c, alias = cases_table(ll, dedup=True)
    if kind == "with_noncases":
        c2 = ll[ll["classification"].isin(["Confirmed", "Probable", "Not a case"])].copy()
        c2["onset"] = [day(parse_date(x)) for x in c2["date_of_onset"]]
        c2["notif"] = [day(parse_date(x)) for x in c2["date_of_notification"]]
        c = c2[~c2["case_number"].isin(alias)]
    chv = ch
    if kind == "drop_low":
        chv = ch[ch["Certainty level"] != "Low"]
    lastp = T
    if kind == "trunc_at_extract":
        lastp = day(dt.date(2026, 10, 18))
    pi, pj, lags = pairs(c, chv, alias, lastp)
    ok = lags >= 1
    pi, pj, lags = pi[ok], pj[ok], lags[ok]
    if kind == "drop_recent_created":
        cr = {}
        for a, b, d in zip(ch["Source person"], ch["Target person"], ch["Created on"]):
            cr[(alias.get(a, a), alias.get(b, b))] = day(dt.date.fromisoformat(d))
    daily = daily_counts(c, T)
    if kind == "naive_drop_last14":
        m = pj <= T - 14
        w = C.empirical(lags[m])
    elif kind in ("naive",):
        w = C.empirical(lags)
    else:
        w, _ = C.fit_lags(lags, pi, lastp, "gamma", True)
    r = C.growth_rate(daily, day(BASE0), T)
    R = C.R_from_growth(r, w)
    x = C.project(daily, T, R, w, CUT, day(CUT_FROM), day(WIN1))
    return float(x[day(WIN0):day(WIN1) + 1].sum()), R, C.mean_of(w)


ASK_ZONES = ["Tamberlow", "Quillmarsh", "Kettlebank North", "Brindlecourt"]
WK37, WK39_END = dt.date(2026, 9, 7), dt.date(2026, 9, 27)


def load_contacts(target=TARGET):
    rg = pd.read_csv(os.path.join(target, "contact_registry_dunmarrow_w36-w42.csv"), dtype=str,
                     encoding="utf-8-sig", keep_default_na=False)
    for col in ("date_listed", "date_last_exposure", "follow_up_end", "status_date"):
        rg[col] = [parse_date(x) for x in rg[col]]
    rg["age_years"] = rg["age_years"].astype(int)
    rg["days_seen"] = rg["days_seen"].astype(int)
    return rg


def person_ids(rg, mode="golden"):
    """Group listings into people. golden: the exact person key, then a provincial paper listing joined to a
    tablet listing of the same source case, household, initials and sex, listed within a day, age within three
    years. exact: the exact key only. loose: household, initials and sex, age ignored."""
    key_exact = list(zip(rg["district"], rg["household_code"], rg["initials"], rg["sex"], rg["age_years"]))
    if mode == "ids":
        return list(rg["contact_id"])
    if mode == "loose":
        return list(zip(rg["district"], rg["household_code"], rg["initials"], rg["sex"]))
    pid = list(key_exact)
    if mode == "exact":
        return pid
    tab = rg[rg["follow_up_team"] == "LMR"]
    idx = {}
    for i, r in zip(tab.index, tab.itertuples()):
        idx.setdefault((r.source_case_number, r.household_code, r.initials, r.sex), []).append((i, r.date_listed, r.age_years))
    pos = {i: k for k, i in enumerate(rg.index)}
    for i, r in zip(rg.index, rg.itertuples()):
        if r.follow_up_team != "PHD":
            continue
        for j, dl, ag in idx.get((r.source_case_number, r.household_code, r.initials, r.sex), []):
            if abs((r.date_listed - dl).days) <= 1 and abs(r.age_years - ag) <= 3 and ag != r.age_years:
                pid[pos[i]] = key_exact[pos[j]]
                break
    return pid


def ask_contacts(target=TARGET, mode="golden", per_record=False):
    rg = load_contacts(target)
    rg = rg.assign(pid=person_ids(rg, mode))
    out = {}
    for z in ASK_ZONES:
        sub = rg[rg["district"] == z]
        first = sub.groupby("pid")["date_listed"].min()
        people = first[(first >= WK37) & (first <= WK39_END)].index
        s2 = sub[sub["pid"].isin(set(people))]
        if per_record:
            done = (s2["status"] == "Follow-up completed").mean()
            out[z] = (len(s2), 100 * done)
            continue
        last_end = s2.groupby("pid")["follow_up_end"].transform("max")
        fin = s2[s2["follow_up_end"] == last_end]
        comp = fin.groupby("pid")["status"].apply(lambda v: (v == "Follow-up completed").any())
        out[z] = (int(len(people)), float(100 * comp.mean()))
    return out


def load_mobile_lab(target=TARGET):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "tamberlow_field_lab_pcr_w36-w42.xlsx"), read_only=True)
    rows = []
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = next(it)
        for r in it:
            rows.append(dict(zip(head, r)))
    df = pd.DataFrame(rows)
    f = lambda s: dt.datetime.strptime(s, "%d/%m/%Y %H:%M")
    df["coll"] = df["Collected"].map(f)
    df["rec"] = df["Received at lab"].map(f)
    df["res"] = df["Result time (analyser)"].map(f)
    return df


def ask_lab(target=TARGET, shift_h=1.0, final="last"):
    df = load_mobile_lab(target)
    d = df[df["Reason"] == "Diagnostic"].copy()
    d["res"] = d["res"] + dt.timedelta(hours=shift_h)
    d = d.sort_values(["Sample no.", "res"], kind="stable")
    g = d.groupby("Sample no.").tail(1) if final == "last" else d.groupby("Sample no.").head(1)
    g = g.assign(h=[(a - b).total_seconds() / 3600 for a, b in zip(g["res"], g["coll"])],
                 wk=[x.isocalendar()[1] for x in g["coll"]])
    out = {}
    for wk in (38, 39, 40, 41):
        s = g[g["wk"] == wk]["h"]
        out[wk] = (float(np.mean(s)), float(100 * (s <= 24).mean()), int(len(s)))
    return out


def cartridge_run_minutes(target=TARGET):
    """The cartridge run time as the data dictionary states it."""
    import openpyxl
    import re
    wb = openpyxl.load_workbook(os.path.join(target, "data_dictionary_tvd_response_2026-10.xlsx"), read_only=True)
    for row in wb["Tamberlow field laboratory"].iter_rows(values_only=True):
        m = re.search(r"runs (\d+) minutes", str(row[1]))
        if m:
            return int(m.group(1))
    raise ValueError("run time not found in the dictionary")
