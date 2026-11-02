"""The two supplemental asks for task121, each a month-by-month measure from September 2025 to August 2026, read
from files the main call never opens: the arrest reviews against the CAD's answer times (Ask B) and the 911 call
handling equipment's call detail (Ask C). Each function takes the handling as arguments, so the ladder's other stops
are the same code with one argument changed."""
import statistics

import pandas as pd

import common as K
import pack as P


def _months(ts):
    return list(zip(ts.dt.year, ts.dt.month))


def minsec_seconds(v):
    """a time keyed as minutes and seconds without the colon (205 for 2:05) back to seconds"""
    return v if v < 100 else (v // 100) * 60 + v % 100


def tcpr(target, from_answer=True, primary_only=True, keyed="reviewer"):
    """Ask B: the median seconds from answer to the first coached compression, arrests by month of answer.
    keyed: "reviewer" reads the times of the reviewer who keys minutes and seconds without the colon as minutes and
    seconds; None takes every time as seconds; "all" reads every reviewer's times that way; "drop" leaves that
    reviewer's reviews out"""
    d = P.load(target)
    r = d["tcpr"].copy()
    if primary_only:
        r = r[r["review_type"] == "Primary"]
    r = r[r["first_compression_s"] != ""].copy()
    r["fc"] = r["first_compression_s"].astype(int)
    mine = r["reviewer"] == K.MINSEC_REVIEWER
    if keyed == "reviewer":
        r.loc[mine, "fc"] = r.loc[mine, "fc"].map(minsec_seconds)
    elif keyed == "all":
        ok = r["fc"] % 100 < 60
        r.loc[ok, "fc"] = r.loc[ok, "fc"].map(minsec_seconds)
    elif keyed == "drop":
        r = r[~mine].copy()
    c = d["calls"].set_index("incident_no")
    r["answered"] = P.local(r["incident_no"].map(c["call_answered"]))
    r["started"] = P.local(r["recording_started"])
    if from_answer:
        r["s"] = (r["started"] + pd.to_timedelta(r["fc"], unit="s") - r["answered"]).dt.total_seconds()
    else:
        r["s"] = r["fc"].astype(float)
    r["m"] = _months(r["answered"])
    out = {}
    for ym in K.MONTHS:
        v = r.loc[r["m"].apply(lambda x: x == ym), "s"].tolist()
        out[ym] = K.r0(statistics.median(v))
    return out


def passed_calls(h):
    """a record that arrives the second an earlier record on the same trunk group from the same number was released:
    the call passed from the position that answered it to another, not a call arriving at the centre"""
    ends = set(zip(h["trunk_group"], h["ani"], h["released_utc"]))
    return pd.Series([(t, a, x) in ends for t, a, x in zip(h["trunk_group"], h["ani"], h["arrived_utc"])],
                     index=h.index)


def answering(target, trunks_911_only=True, local_months=True, abandoned_out=True, passed="out"):
    """Ask C: the share of 911 calls answered within 15 seconds of arriving, by month answered (per cent).
    passed: "out" leaves out the records of calls passed between positions; "kept" counts every record; "window"
    counts a number's records on a trunk group within ten minutes of its last one as one call"""
    d = P.load(target)
    h = d["che"].copy()
    tg = d["trunks"]
    if trunks_911_only:
        keep = set(tg.loc[tg["description"].str.startswith("911"), "trunk_group"])
        h = h[h["trunk_group"].isin(keep)]
    h["arr"] = pd.to_datetime(h["arrived_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    h["rel"] = pd.to_datetime(h["released_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    h["ans"] = pd.to_datetime(h["answered_utc"].replace("", None), format="%Y-%m-%dT%H:%M:%SZ")
    if passed == "out":
        h = h[~passed_calls(h)].copy()
    elif passed == "window":
        h = h.sort_values(["trunk_group", "ani", "arr"])
        prev = h.groupby(["trunk_group", "ani"])["rel"].shift(1)
        h = h[~((h["arr"] - prev).dt.total_seconds() <= 600)].copy()
    when = h["ans"].fillna(h["arr"])
    if local_months:
        cdt = ((when >= pd.Timestamp("2025-03-09 08:00")) & (when < pd.Timestamp("2025-11-02 07:00"))) | \
              ((when >= pd.Timestamp("2026-03-08 08:00")) & (when < pd.Timestamp("2026-11-01 07:00")))
        loc = when - pd.to_timedelta(cdt.map({True: 5, False: 6}), unit="h")
    else:
        loc = when
    h["m"] = _months(loc)
    h["wait"] = (h["ans"] - h["arr"]).dt.total_seconds()
    out = {}
    for ym in K.MONTHS:
        x = h[h["m"].apply(lambda v: v == ym)]
        if abandoned_out:
            x = x[x["abandoned"] == "N"]
            share = 100.0 * (x["wait"] <= K.STANDARD_ANSWER).sum() / len(x)
        else:
            share = 100.0 * ((x["abandoned"] == "N") & (x["wait"] <= K.STANDARD_ANSWER)).sum() / len(x)
        out[ym] = K.r1(share)
    return out


def golden(target):
    return dict(B=tcpr(target), C=answering(target))


def stops(target):
    return dict(
        B_times_as_keyed=tcpr(target, keyed=None),
        B_seconds_as_recorded=tcpr(target, from_answer=False, keyed=None),
        B_calibration_kept=tcpr(target, primary_only=False),
        B_every_reviewer_read=tcpr(target, keyed="all"),
        B_reviewer_left_out=tcpr(target, keyed="drop"),
        C_passed_calls_kept=answering(target, passed="kept"),
        C_same_number_ten_minutes=answering(target, passed="window"),
        C_ten_digit_kept=answering(target, trunks_911_only=False),
        C_utc_months=answering(target, local_months=False),
        C_abandoned_counted=answering(target, abandoned_out=False),
    )
