"""Read the shipped pack the way an analyst would and compute the golden, every rung the ladder names and the routes
the ask sheet prices (the careful route that misses each ask's device, and the mirror's)."""
import glob
import os

import numpy as np
import pandas as pd

LETTERS = dict(C="COMPLETE", P="PARTIAL", R="REFUSAL", B="CALLBACK", I="INELIGIBLE", L="LANGUAGE", H="HANGUP",
               D="DNC", A="AMD_MACHINE", X="ABANDONED", AA="AGENT_MACHINE")
ZONES = {"Eastern": "America/New_York", "Central": "America/Chicago", "Mountain": "America/Denver",
         "Mountain (Arizona)": "America/Phoenix", "Pacific": "America/Los_Angeles"}
# the North American numbering plan's own assignment of the area codes the pack's numbers carry (public knowledge)
AREA_STATE = {"218": "MN", "320": "MN", "507": "MN", "612": "MN", "651": "MN", "763": "MN", "952": "MN",
              "608": "WI", "715": "WI", "515": "IA", "712": "IA", "701": "ND", "605": "SD",
              "480": "AZ", "602": "AZ", "520": "AZ", "239": "FL", "941": "FL", "727": "FL", "561": "FL",
              "619": "CA", "760": "CA", "949": "CA", "303": "CO", "719": "CO", "212": "NY", "718": "NY", "914": "NY",
              "214": "TX", "512": "TX", "312": "IL", "847": "IL"}
NEW_CASE = r"^\d{4}-\d{6}$"


def digits(s):
    return s.astype(str).str.replace(r"\D", "", regex=True).str[-10:]


def load_calls(target):
    parts = []
    for p in sorted(glob.glob(os.path.join(target, "dialer_exports", "*.csv"))):
        d = pd.read_csv(p, dtype=str, keep_default_na=False)
        if "CallID" in d.columns:
            d = pd.DataFrame({"call_id": d["CallID"], "job": d["JobNo"], "phone": digits(d["Phone"]), "case": d["CaseID"],
                              "placed": pd.to_datetime(d["CallStart"], format="%m/%d/%Y %H:%M:%S"),
                              "amd": d["AMD"].map({"M": "MACHINE", "H": "LIVE"}), "agent": d["AgentID"],
                              "outcome": d["Disp"].map(LETTERS), "talk": d["TalkSec"].astype(int),
                              "wrap": d["WrapSec"].astype(int),
                              "ended": pd.to_datetime(d["CallEnd"], format="%m/%d/%Y %H:%M:%S")})
        else:
            d = pd.DataFrame({"call_id": d["call_id"], "job": d["job"], "phone": digits(d["dialed_number"]),
                              "case": d["case_number"], "placed": pd.to_datetime(d["placed_at"]), "amd": d["amd_result"],
                              "agent": d["agent"], "outcome": d["outcome"], "talk": d["talk_seconds"].astype(int),
                              "wrap": d["wrap_seconds"].astype(int), "ended": pd.to_datetime(d["ended_at"])})
        parts.append(d)
    raw = pd.concat(parts, ignore_index=True)
    calls = raw.drop_duplicates("call_id").sort_values(["placed", "call_id"]).reset_index(drop=True)
    return raw, calls


def load_inbound(target):
    d = pd.read_csv(os.path.join(target, "inbound_switch_2026.csv"), dtype=str, keep_default_na=False)
    d["started"] = pd.to_datetime(d["started"])
    d["phone"] = np.where(d["caller"].str.startswith("+1"), digits(d["caller"]), "")
    return d


def projects(target):
    reg = pd.read_excel(os.path.join(target, "project_register_2027.xlsx"), header=2, dtype=str)
    return reg[reg["Job"].astype(str).str.startswith("KR-")].reset_index(drop=True)


def line_jobs(reg):
    return {"+1" + digits(pd.Series([x]))[0]: j for x, j in zip(reg["Caller-ID line"], reg["Job"])}


def load_cases(target):
    s = pd.read_csv(os.path.join(target, "case_records_2026.csv"), dtype=str, keep_default_na=False)
    s["phone"] = digits(s["phone"])
    return s


def parse_hhmm(s):
    """hours.minutes, 4.30 being four and a half hours"""
    x = pd.to_numeric(s, errors="coerce")
    whole = np.floor(x + 1e-9)
    return whole + (x - whole) * 100.0 / 60.0


def load_hours(target, hhmm=True):
    a = pd.read_csv(os.path.join(target, "interviewer_hours_2026_h1.csv"), dtype=str, keep_default_na=False)
    a = pd.DataFrame({"date": pd.to_datetime(a["Work Date"], format="%m/%d/%Y"), "interviewer": a["Employee"],
                      "project": "KR-" + a["Job Code"], "start": a["Time In"], "h": pd.to_numeric(a["Hours"])})
    b = pd.read_csv(os.path.join(target, "interviewer_hours_2026_h2.csv"), dtype=str, keep_default_na=False)
    b = pd.DataFrame({"date": pd.to_datetime(b["shift_date"]), "interviewer": b["employee"], "project": b["cost_code"],
                      "start": b["clock_in"], "h": parse_hhmm(b["paid_hours"]) if hhmm else pd.to_numeric(b["paid_hours"])})
    t = pd.concat([a, b], ignore_index=True)
    t["t0"] = t["date"] + pd.to_timedelta(t["start"] + ":00")
    t["t1"] = t["t0"] + pd.to_timedelta(t["h"], unit="h")
    return t.reset_index(drop=True)


# ---- the main call -------------------------------------------------------------------------------------------------

def returns(calls, inbound):
    """each inbound call from a dialed number (its legs collapsed to the first), tied to the latest outbound call to
    that number"""
    first = inbound[(inbound["leg"] == "1") & inbound["phone"].ne("")].sort_values("started")
    out = calls[["call_id", "job", "phone", "ended", "outcome"]].sort_values("ended")
    m = pd.merge_asof(first, out, left_on="started", right_on="ended", by="phone", direction="backward")
    m = m[m["call_id"].notna()].copy()
    m["delay_min"] = (m["started"] - m["ended"]).dt.total_seconds() / 60.0
    return m


def main_call(calls, inbound, jobs, window_min=20.0, pooled=False, any_delay=False, ret=None):
    ret = returns(calls, inbound) if ret is None else ret
    if not any_delay:
        ret = ret[ret["delay_min"] <= window_min]
    g = calls[calls["job"].isin(jobs)]
    n_am = g[g["outcome"].eq("AMD_MACHINE")].groupby("job").size().reindex(jobs).fillna(0).astype(int)
    n_ab = g[g["outcome"].eq("ABANDONED")].groupby("job").size().reindex(jobs).fillna(0).astype(int)
    r_am = ret[ret["outcome"].eq("AMD_MACHINE")].groupby("job").size().reindex(jobs).fillna(0).astype(int)
    r_ab = ret[ret["outcome"].eq("ABANDONED")].groupby("job").size().reindex(jobs).fillna(0).astype(int)
    t = pd.DataFrame(dict(job=jobs, n_am=n_am.values, n_ab=n_ab.values, r_am=r_am.values, r_ab=r_ab.values,
                          answered=g.groupby("job").size().reindex(jobs).values))
    if pooled:
        t["share"] = (t["r_am"] / t["n_am"]) / (t["r_ab"].sum() / t["n_ab"].sum())
    else:
        t["share"] = (t["r_am"] / t["n_am"]) / (t["r_ab"] / t["n_ab"])
    t["off"] = t["share"] >= 0.10
    return t


def machine_share(calls, jobs):
    g = calls[calls["job"].isin(jobs)]
    return g.groupby("job")["outcome"].apply(lambda x: (x == "AMD_MACHINE").mean()).reindex(jobs)


# ---- ask A: calling hours ------------------------------------------------------------------------------------------

def household_state(calls, cases, route="golden"):
    """the called household's state: its case record, reached by the number dialed, by the case number the dialer
    wrote after the upgrade, or, for a number the record does not hold before the upgrade, through the same case's
    other calls; the careful route falls back on the area code there, the mirror on the area code wherever the
    number is not in the record"""
    by_phone = dict(zip(cases["phone"], cases["address_state"]))
    by_case = dict(zip(cases["case_number"], cases["address_state"]))
    st = calls["phone"].map(by_phone)
    new = calls["case"].str.match(NEW_CASE)
    if route in ("golden", "cracker"):
        st = st.where(st.notna() | ~new, calls["case"].map(by_case))
    if route == "golden":
        # the old case numbers restart in every project, so a case is its job and its number
        key = calls["job"] + "/" + calls["case"]
        learned = pd.DataFrame({"key": key, "st": st})[~new & st.notna()].drop_duplicates("key")
        st = st.where(st.notna(), key.map(dict(zip(learned["key"], learned["st"]))))
    else:
        st = st.where(st.notna(), calls["phone"].str[:3].map(AREA_STATE))
    return st


def calling_hours(calls, cases, zones, jobs, route="golden", arizona_dst=False, return_rows=False):
    g = calls[calls["job"].isin(jobs)].copy()
    g["state"] = household_state(g, cases, route).values
    zmap = dict(zip(zones["state"], zones["time_zone"].map(ZONES)))
    if arizona_dst:
        zmap = {k: ("America/Denver" if v == "America/Phoenix" else v) for k, v in zmap.items()}
    g["zone"] = g["state"].map(zmap)
    loc = g["placed"].dt.tz_localize("America/Chicago", ambiguous="NaT", nonexistent="NaT")
    hour = np.full(len(g), np.nan)
    pos = np.arange(len(g))
    for z, idx in g.groupby("zone").groups.items():
        lt = loc.loc[idx].dt.tz_convert(z)
        hour[pos[g.index.get_indexer(idx)]] = (lt.dt.hour + lt.dt.minute / 60.0 + lt.dt.second / 3600.0).values
    g["local_hour"] = hour
    g["outside"] = (g["local_hour"] < 8) | (g["local_hour"] >= 21)
    if return_rows:
        return g
    return g.groupby("job")["outside"].sum().reindex(jobs).fillna(0).astype(int)


# ---- ask B: completed interviews -----------------------------------------------------------------------------------

def case_of(calls, cases):
    """every dialer row's case as the client's record numbers it (the household's sample record)"""
    by_phone = dict(zip(cases["phone"], cases["case_number"]))
    c = calls["phone"].map(by_phone)
    new = calls["case"].str.match(NEW_CASE)
    c = c.where(c.notna() | ~new, calls["case"].where(new))
    key = calls["job"] + "/" + calls["case"]
    learned = pd.DataFrame({"key": key, "c": c})[~new & c.notna()].drop_duplicates("key")
    return c.where(c.notna(), key.map(dict(zip(learned["key"], learned["c"]))))


def inbound_calls(inbound, first_leg_only=False):
    """one row per inbound call, its outcome the COMPLETE of any leg (or of the first leg alone)"""
    x = inbound[inbound["phone"].ne("")]
    if first_leg_only:
        x = x[x["leg"] == "1"]
    done = x.groupby("switch_call_id")["wrap_code"].apply(lambda w: (w == "COMPLETE").any())
    first = x[x["leg"] == "1"].set_index("switch_call_id")[["phone", "dialed_line", "started"]]
    out = first.join(done.rename("complete"), how="left").reset_index()
    return out[out["started"].dt.year == 2026]


def completes(calls, inbound, reg, cases, jobs, route="golden"):
    comp = calls[calls["outcome"].eq("COMPLETE") & calls["job"].isin(jobs)]
    lj = line_jobs(reg)
    if route == "invoiced":                       # every completed row the dialer wrote
        return comp.groupby("job").size().reindex(jobs).fillna(0).astype(int)
    if route == "cracker":                        # one per case number, plus the line's completes on its first leg
        a = comp.drop_duplicates(["job", "case"]).groupby("job").size().reindex(jobs).fillna(0)
        ib = inbound_calls(inbound, first_leg_only=True)
        ib = ib[ib["complete"]].assign(job=lambda d: d["dialed_line"].map(lj))
        return (a + ib.groupby("job").size().reindex(jobs).fillna(0)).astype(int)
    case = case_of(calls, cases)
    a = pd.DataFrame({"job": comp["job"], "case": case.loc[comp.index]})
    phone_case = pd.Series(case.values, index=calls["phone"].values)
    phone_case = phone_case[~phone_case.index.duplicated()]
    pc = dict(zip(cases["phone"], cases["case_number"]))
    pc.update({k: v for k, v in phone_case.items() if k not in pc and pd.notna(v)})
    ib = inbound_calls(inbound)
    ib = ib[ib["complete"]]
    b = pd.DataFrame({"job": ib["dialed_line"].map(lj), "case": ib["phone"].map(pc)})
    u = pd.concat([a, b]).dropna().drop_duplicates()
    return u.groupby("job").size().reindex(jobs).fillna(0).astype(int)


# ---- ask C: interviewer hours --------------------------------------------------------------------------------------

def hours(calls, ts, jobs, route="golden"):
    t = ts.copy()
    if route == "by_code":
        return t.groupby("project")["h"].sum().reindex(jobs).fillna(0)
    t["row"] = np.arange(len(t))
    c = calls[calls["agent"].ne("") & (calls["talk"] > 0)][["agent", "job", "placed", "talk", "wrap"]]
    c = c.assign(sec=c["talk"] + c["wrap"], date=c["placed"].dt.normalize())
    m = c.merge(t[["row", "interviewer", "date", "t0", "t1"]], left_on=["agent", "date"],
                right_on=["interviewer", "date"])
    m = m[(m["placed"] >= m["t0"]) & (m["placed"] < m["t1"])]
    per = m.groupby(["row", "job"])["sec"].sum().reset_index()
    per["share"] = per["sec"] / per.groupby("row")["sec"].transform("sum")
    per = per.merge(t[["row", "h"]], on="row")
    per["alloc"] = per["share"] * per["h"]
    return per.groupby("job")["alloc"].sum().reindex(jobs).fillna(0)


def solve(target):
    raw, calls = load_calls(target)
    inbound = load_inbound(target)
    reg = projects(target)
    jobs = list(reg["Job"])
    cases = load_cases(target)
    zones = pd.read_csv(os.path.join(target, "state_time_zones.csv"), dtype=str)
    ts = load_hours(target)
    S = dict(raw=raw, calls=calls, inbound=inbound, reg=reg, jobs=jobs, cases=cases, zones=zones, ts=ts)
    S["ret"] = returns(calls, inbound)
    S["main"] = main_call(calls, inbound, jobs, ret=S["ret"])
    S["askA"] = calling_hours(calls, cases, zones, jobs)
    S["askB"] = completes(calls, inbound, reg, cases, jobs)
    S["askC"] = hours(calls, ts, jobs)
    return S
