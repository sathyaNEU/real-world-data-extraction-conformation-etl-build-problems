"""task148 ask layer against the careful solver's routes, on the cut pack.

    python3 task148/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The prompt's two asks
give 14 figures: Ask A, for each quarter of fiscal 2026, the wireless 911 calls placed from Halvorsen Township that
reached the agency and how many of them it transferred to Wexley County Emergency Communications (eight counts, kept
only when exact); Ask B, for each month from January to June 2026, the share of all abandoned 911 calls dialled back
within two minutes of the hang-up (six shares, kept when they print the golden's one decimal). The cracker sheet adds
the chart's two criteria: its twelve monthly values (they follow the call) and its 90 per cent line (form).

Every route is a complete pipeline over the cut pack, read here from the bundle alone (the call through the
verifier's bundle-only readers, the asks through this script's own), scored figure by figure against figures.json.

The cracker is the careful solver. It lands the call (Erlang A on the board's FY2028 forecast with the measured busy
time and the late shift's own patience over every one of its calls' waits), runs the hygiene battery (exact duplicate
rows; the test calls by both of each export's labels; the cutover days' calls in one export each; the i3 clock in UTC
and the legacy and desk clocks local, each checked against the data; the location records matched across the two
systems, the backup centre's under the i3 incident identifier; the callback numbers matched across the i3 log and the
desk log; the abandons no desk task names looked up by their number), applies every filed rule as worded (SOP 2.10
1.2 local quarters and months, 2.2 test calls out and transfers in, 6.2 a wireless call placed by the last handset
location received for it, 7.1 every abandoned 911 call however briefly the caller held on) and takes each ask on its
natural read: Ask A's calls placed inside the township as its GeoJSON geometry says (every part, the holes removed) and
transferred to the agency the ESInet directory names for the transfer URI; Ask B's abandon dialled back when the desk's
first dial to its number came at or after the hang-up and within two minutes, whichever task carried the dial.

The mirror stops at the default path (Erlang C, May to September) and takes each ask on the same natural read without
the battery: the location records joined on the i3 call identifier alone, the abandons linked to the desk's tasks by
the call that opened them. The full includer is the golden's own construction of every device the ask sheet names (A1
the boundary's hole and detached part, A3 Wexley's alternate URI, A4 the incident-keyed records, B4 the abandons
dialled through an administrative-line task, B2 the hang-up as the anchor, the desk's task open from the abandon that
opens it) and has to give back figures.json exactly, or the script exits 1: the route code's control. The stops are
the sheet's other wrong paths, each scored as a route; the sheet's earlier paper cracker (its S1 for Ask A, S7 for Ask
B) is printed as what it is, a narrowed route that skips the battery and the plain reading.

The pair is the ask sheet's formula: the cracker on the call C = 38 + 7 + 55 Lc, the mirror off it S = 5 + 7 + 55 Ls,
the pair (C + S) / 2, L the share of the sheet's 16 ask criteria kept, each criterion equal, and again with the chart's
two at the sheet's 10 per cent and the 14 figures sharing the rest. Pair ceiling is the worse of the two weightings.
The script modifies nothing and never runs inside the build."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as CA     # noqa: E402  (the mirror's Erlang C on the board's forecast)
import common as K    # noqa: E402
import verify as V    # noqa: E402  (the bundle-only readers: the calls, the forecast, Erlang A, the PDFs)

TASK = os.path.dirname(HERE)
TZ = "America/Chicago"
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 5.0      # the ask sheet's planning weights and a wrong call's r
CHART_SHARE = 0.10                             # the sheet's paper weight for the chart's two criteria
WEXLEY = "Wexley County Emergency Communications"
QUARTERS = ("Q1", "Q2", "Q3", "Q4")
MONTHS = ("January", "February", "March", "April", "May", "June")
FY28 = [(2027, m) for m in range(7, 13)] + [(2028, m) for m in range(1, 7)]
MONTH_NAME = {7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December", 1: "January",
              2: "February", 3: "March", 4: "April", 5: "May", 6: "June"}

# Ask A route: key (callid: the i3 call identifier alone; both: the incident identifier for the records the call
# identifier leaves unmatched), fix (last_handset, SOP 6.2; first: the routing record), geom (full: every part, holes
# removed; outer_first: the first part's outer ring), xfer (directory; name: URIs naming Wexley), quarter (local, SOP
# 1.2; utc), unit (calls; numbers: one per callback number a quarter)
CRACKER_A = dict(key="both", fix="last_handset", geom="full", xfer="directory", quarter="local", unit="calls")
MIRROR_A = dict(CRACKER_A, key="callid")
FULL_A = dict(CRACKER_A)
STOPS_A = {
    "S1 the sheet's paper cracker (first part's outer ring, URIs naming Wexley, the call identifier alone)":
        dict(geom="outer_first", xfer="name", key="callid"),
    "S2 the routing location (each call's first record)": dict(fix="first"),
    "S3 URIs naming Wexley": dict(xfer="name"),
    "S4 quarters by UTC date": dict(quarter="utc"),
    "S5 the call identifier alone (A4 unfound)": dict(key="callid"),
    "S6 URIs naming Wexley and the call identifier alone": dict(xfer="name", key="callid"),
    "A1 unfound alone (the first part's outer ring)": dict(geom="outer_first"),
    "HC1 one call per callback number a quarter": dict(unit="numbers"),
}
# Ask B route: link (number: the desk's first dial to the abandon's number at or after the hang-up, any task;
# number_open: the same through the task open at the hang-up, created no later than 30 seconds after it, the golden's
# construction; number911: the desk's 911 tasks alone; ref: the task whose call_ref is the abandon, the rest not
# dialled; ref_drop: the rest dropped), anchor (hangup; stamp: the task's created), clock (local with the zone's
# rules; fixed: Central standard time all year), misdials (in, SOP 7.1), unit (abandons; tasks), per_number, xin
CRACKER_B = dict(link="number", anchor="hangup", clock="local", misdials=True, unit="abandons", per_number=False,
                 xin=True)
MIRROR_B = dict(CRACKER_B, link="ref")
FULL_B = dict(CRACKER_B, link="number_open")
STOPS_B = {
    "S1 tasks keyed on the opening call, the unjoined not dialled back": dict(link="ref"),
    "S2 tasks keyed on the opening call, the unjoined dropped": dict(link="ref_drop"),
    "S3 opening-call keys, two minutes from the task's stamp": dict(link="ref", anchor="stamp"),
    "S4 the task log alone, tasks as the unit": dict(unit="tasks"),
    "S6 two minutes from the task's stamp (B2 unfound)": dict(anchor="stamp"),
    "S7 the sheet's paper cracker: the desk's 911 tasks alone (B4 unfound)": dict(link="number911"),
    "HB1 the desk's clock on a fixed offset": dict(clock="fixed"),
    "the abandons within 5 seconds left out": dict(misdials=False),
    "HC1 one abandon per callback number a month": dict(per_number=True),
    "HC3 the transferred-in abandons left out": dict(xin=False),
}


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling148-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


# ---------------------------------------------------------------------------------------------------- the pack
def load(folder):
    D = {}
    recs = [json.loads(x) for x in open(os.path.join(folder, V.I3), encoding="utf-8")]
    i3 = pd.DataFrame(recs)
    D["i3_raw"] = i3
    i3 = i3[i3["serviceType"] != "test"].copy()                       # SOP 2.2: test calls are not 911 calls
    for col in ("presented", "answered", "ended"):
        i3[col] = pd.to_datetime(i3[col], format="%Y-%m-%dT%H:%M:%S.%fZ", utc=True)
    i3["num"] = i3["callbackRef"].str.replace(r"^cb-", "", regex=True).str.lower()
    i3["transferTo"] = i3["transferTo"].fillna("")
    i3["xin"] = i3["referredBy"].notna() if "referredBy" in i3 else False
    D["i3"] = i3
    che = pd.read_csv(os.path.join(folder, V.CHE), dtype={"call_id": str, "method": str})
    D["che"] = che
    hand = che[che["method"] != "cell"].sort_values(["call_id", "seq"]).groupby("call_id").last()
    first = che.sort_values(["call_id", "seq"]).groupby("call_id").first()
    D["fix"] = {"last_handset": dict(zip(hand.index, zip(hand["longitude"], hand["latitude"]))),
                "first": dict(zip(first.index, zip(first["longitude"], first["latitude"])))}
    gj = json.load(open(os.path.join(folder, V.GEOJ), encoding="utf-8"))
    feat = [f for f in gj["features"] if f["properties"].get("NAME") == "Halvorsen Township"][0]
    g = feat["geometry"]
    D["polys"] = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    D["geom_type"] = g["type"]
    dr = pd.read_csv(os.path.join(folder, V.DIRC), dtype=str)
    D["wexley_uris"] = set(dr.loc[dr["agency"] == WEXLEY, "uri"])
    cb = pd.read_csv(os.path.join(folder, V.CB), dtype=str, keep_default_na=False)
    cb["num"] = cb["callback_number"].str.lower()
    D["cb_raw"] = cb
    return D


def desk_clock(cb, clock):
    """The callback log's created and first-dial stamps as UTC: local Central time read with the zone's rules, or on
    Central standard time all year."""
    zone = TZ if clock == "local" else "Etc/GMT+6"
    out = cb.copy()
    out["created_t"] = pd.to_datetime(out["created"]).dt.tz_localize(zone).dt.tz_convert("UTC")
    out["first_t"] = pd.to_datetime(out["first_dial"].where(out["first_dial"] != "", None)).dt.tz_localize(
        zone).dt.tz_convert("UTC")
    return out


# ---------------------------------------------------------------------------------------------------- the battery
def battery(folder, D):
    """The hygiene battery a careful analyst runs before the asks: (check, passed, detail)."""
    out = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, f), dtype=str, keep_default_na=False)
            out.append(("no exact duplicate rows in " + f, not df.duplicated().any(), "%d rows" % len(df)))
    lines = open(os.path.join(folder, V.I3), encoding="utf-8").read().splitlines()
    out.append(("no exact duplicate lines in " + V.I3, len(lines) == len(set(lines)), "%d lines" % len(lines)))
    raw = D["i3_raw"]
    t3 = (raw["disposition"] == "test-responder") == (raw["serviceType"] == "test")
    leg = pd.read_csv(os.path.join(folder, V.LEG), dtype=str, keep_default_na=False)
    tl = (leg["CALL_STATUS"] == "TST") == (leg["CLASS_OF_SVC"] == "TEST")
    out.append(("test calls: each export's two labels mark the same calls, left out (SOP 2.10 2.2)", bool(t3.all() and tl.all()),
                "%d i3, %d legacy" % ((raw["serviceType"] == "test").sum(), (leg["CALL_STATUS"] == "TST").sum())))
    lp = pd.to_datetime(leg["SEIZE_TIME"], format="%m/%d/%Y %H:%M:%S").dt.tz_localize(TZ).dt.tz_convert("UTC")
    i3p = pd.to_datetime(raw["presented"], format="%Y-%m-%dT%H:%M:%S.%fZ", utc=True)
    a = set(zip(lp.dt.floor("s").astype("int64"), leg["CBN_REF"].str.lower()))
    b = set(zip(i3p.dt.floor("s").astype("int64"), raw["callbackRef"].str.replace("cb-", "", regex=False)))
    out.append(("the cutover days: no call in both exports", not (a & b), "%d in both" % len(a & b)))
    wl = lp[leg["CLASS_OF_SVC"].isin(["WPH1", "WPH2"])].max()
    gap = (i3p.min() - wl).total_seconds()
    out.append(("clocks: the i3 log in UTC (every time carries Z), the legacy log local Central: its last wireless call "
                "runs into the i3 log's first", bool(raw["presented"].str.endswith("Z").all() and 0 < gap < 1800),
                "%.0f s apart read as local" % gap))
    che = D["che"]
    i3 = D["i3"]
    keys = set(che["call_id"])
    by_c, by_i = keys & set(i3["callId"]), keys & set(i3["incidentId"])
    out.append(("location records matched across the two systems: under the call identifier, or (the backup centre's) "
                "under the incident identifier, none under both and none unmatched", not (by_c & by_i)
                and len(by_c) + len(by_i) == len(keys), "%d keys: %d call, %d incident identifiers" % (
                    len(keys), len(by_c), len(by_i))))
    out.append(("the boundary read as its geometry says (%s: %d parts, %d holes)" % (
        D["geom_type"], len(D["polys"]), sum(len(p) - 1 for p in D["polys"])), D["geom_type"] in ("Polygon", "MultiPolygon"), ""))
    cb = desk_clock(D["cb_raw"], "local")
    t911 = cb[cb["line"] == "911"].merge(i3[["callId", "num", "ended"]], left_on="call_ref", right_on="callId", how="left")
    lag = (t911["created_t"] - t911["ended"]).dt.total_seconds()
    out.append(("callback numbers matched across the i3 log and the desk log (every 911 task's opening call carries cb- "
                "and the task's number)", bool((t911["num_y"] == t911["num_x"]).all()), "%d tasks" % len(t911)))
    out.append(("the desk's clock local Central with the zone's rules (every 911 task stamped 0 to 21 seconds after its "
                "opening hang-up)", bool(lag.between(0, 21).all()), "%.1f to %.1f s" % (lag.min(), lag.max())))
    ab = i3[(i3["disposition"] == "abandoned")]
    hl = ab["ended"].dt.tz_convert(TZ)
    ab = ab[(hl >= pd.Timestamp("2026-01-01", tz=TZ)) & (hl < pd.Timestamp("2026-07-01", tz=TZ))]
    unnamed = ab[~ab["callId"].isin(set(cb["call_ref"]))]
    found = unnamed["num"].isin(set(cb["num"]))
    out.append(("abandons no desk task names, looked up by their callback number", bool(found.all()),
                "%d of %d abandons, all with a task for their number" % (len(unnamed), len(ab))))
    return out


def filed_rules(folder):
    """The filed rules the cracker executes, read from the shipped SOP."""
    sop = V.pdf_text(os.path.join(folder, V.SOP))
    want = {"1.2": "The days, months, quarters and years the agency reports are local (Central) calendar dates.",
            "2.2": "Calls on the administrative lines are not 911 calls; neither are test calls.",
            "6.2": "a wireless call by the last handset location received for it.",
            "7.1": "Every abandoned 911 call is called back by the callback desk, however briefly the caller held on."}
    return {k: s in sop for k, s in want.items()}


# ---------------------------------------------------------------------------------------------------- the asks
def inside(lon, lat, polys, geom):
    parts = polys if geom == "full" else polys[:1]
    for p in parts:
        if V.winding(lon, lat, p[0]) and not (geom == "full" and any(V.winding(lon, lat, h) for h in p[1:])):
            return True
    return False


def ask_a(D, r):
    """{quarter: (reached, transferred)} for fiscal 2026."""
    w = D["i3"][D["i3"]["serviceType"] == "wireless"]
    zone = TZ if r["quarter"] == "local" else "UTC"
    loc = w["presented"].dt.tz_convert(zone)
    w = w[(loc >= pd.Timestamp("2025-07-01", tz=zone)) & (loc < pd.Timestamp("2026-07-01", tz=zone))]
    loc = w["presented"].dt.tz_convert(zone)
    fix = D["fix"][r["fix"]]
    key = w["callId"].where(w["callId"].isin(fix.keys()))
    if r["key"] == "both":
        key = key.fillna(w["incidentId"].where(w["incidentId"].isin(fix.keys())))
    q = ((loc.dt.month - 7) % 12) // 3 + 1
    if r["xfer"] == "directory":
        xf = w["transferTo"].isin(D["wexley_uris"])
    else:
        xf = w["transferTo"].str.lower().str.contains("wexley")
    hit = np.array([isinstance(k, str) and inside(fix[k][0], fix[k][1], D["polys"], r["geom"]) for k in key])
    out = {}
    for n, qq in enumerate(QUARTERS, start=1):
        s = hit & (q.values == n)
        if r["unit"] == "numbers":
            out[qq] = (int(w.loc[s, "num"].nunique()), int(w.loc[s & xf.values, "num"].nunique()))
        else:
            out[qq] = (int(s.sum()), int((s & xf.values).sum()))
    return out


def ask_b(D, r):
    """{month: share} for January to June 2026, by the local month of the hang-up."""
    cb = desk_clock(D["cb_raw"], r["clock"])
    i3 = D["i3"]
    lo, hi = pd.Timestamp("2026-01-01", tz=TZ), pd.Timestamp("2026-07-01", tz=TZ)
    if r["unit"] == "tasks":
        t = cb[cb["line"] == "911"]
        cl = t["created_t"].dt.tz_convert(TZ)
        t = t[(cl >= lo) & (cl < hi)]
        ok = (t["first_t"] - t["created_t"]).dt.total_seconds() <= 120.0
        m = t["created_t"].dt.tz_convert(TZ).dt.month
        return {MONTHS[k - 1]: float(ok[m == k].mean()) for k in range(1, 7)}
    ab = i3[i3["disposition"] == "abandoned"]
    if not r["xin"]:
        ab = ab[~ab["xin"]]
    if not r["misdials"]:
        ab = ab[(ab["ended"] - ab["presented"]).dt.total_seconds() > 5.0]
    hl = ab["ended"].dt.tz_convert(TZ)
    ab = ab[(hl >= lo) & (hl < hi)].sort_values("ended")
    if r["per_number"]:
        ab = ab.assign(mo=ab["ended"].dt.tz_convert(TZ).dt.month).drop_duplicates(["mo", "num"])
    pool = cb if r["link"] != "number911" else cb[cb["line"] == "911"]
    by_num = {k: g for k, g in pool[pool["first_t"].notna()].groupby("num")}
    by_ref = {row.call_ref: row for row in cb[cb["line"] == "911"].itertuples()}
    num, den = {}, {}
    for row in ab.itertuples():
        mo = row.ended.tz_convert(TZ).month
        hit = False
        if r["link"].startswith("number"):
            g = by_num.get(row.num)
            if g is not None:
                c = g[g["first_t"] >= row.ended]
                if r["link"] == "number_open":
                    c = c[c["created_t"] <= row.ended + pd.Timedelta(seconds=30)]
                if len(c):
                    k = c["first_t"].idxmin()
                    base = row.ended if r["anchor"] == "hangup" else c.loc[k, "created_t"]
                    hit = (c.loc[k, "first_t"] - base).total_seconds() <= 120.0
        else:
            tk = by_ref.get(row.callId)
            if tk is None:
                if r["link"] == "ref_drop":
                    continue
            elif not pd.isna(tk.first_t):
                base = row.ended if r["anchor"] == "hangup" else tk.created_t
                hit = (tk.first_t - base).total_seconds() <= 120.0
        den[mo] = den.get(mo, 0) + 1
        num[mo] = num.get(mo, 0) + int(hit)
    return {MONTHS[k - 1]: num.get(k, 0) / den[k] for k in range(1, 7)}


def keep_a(fig, gold):
    return {"%s %s" % (q, w): fig[q][j] == gold[q][j] for q in QUARTERS for j, w in enumerate(("reached", "transferred"))}


def keep_b(fig, gold):
    return {m: K.round_half_up(100.0 * fig[m], 1) == gold[m] for m in MONTHS}


# ---------------------------------------------------------------------------------------------------- the pair
def weights():
    crit = ["A %s %s" % (q, w) for q in QUARTERS for w in ("reached", "transferred")] + ["B " + m for m in MONTHS] + \
           ["chart values", "chart line"]
    equal = {c: 1.0 / len(crit) for c in crit}
    paper = {c: (CHART_SHARE / 2 if c.startswith("chart") else (1 - CHART_SHARE) / 14) for c in crit}
    return crit, {"each of the 16 criteria equal": equal, "the chart at the sheet's 10 per cent": paper}


def pair(kc, km, w):
    lc = sum(w[c] for c, v in kc.items() if v)
    ls = sum(w[c] for c, v in km.items() if v)
    c, s = REC + INS + ASK * lc, OFF + INS + ASK * ls
    return c, s, (c + s) / 2.0, lc, ls


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold_a = {q: (figs["ask_a"][q]["reached"], figs["ask_a"][q]["transferred_to_wexley"]) for q in QUARTERS}
    gold_b = {m: figs["ask_b"]["%s 2026" % m]["share_pct"] for m in MONTHS}
    gold_main = [figs["fiscal_2028_compliance_pct"]["%s %d" % (MONTH_NAME[m], y)] for y, m in FY28]
    gold_short = figs["call"]["months_short"]

    # the calls: the cracker's on the verifier's own path, the mirror's Erlang C on the default path
    df = V.load_calls(folder)
    busy = df.loc[~df["abandoned"], "busy"].mean()
    late = df[df["late"]]
    pat = late["wait"].sum() / late["abandoned"].sum()
    g = V.fy2028(folder, busy, pat)
    c_figs = [int(math.floor(100 * g[ym] + 0.5)) for ym in FY28]
    c_short = ["%s %d" % (MONTH_NAME[m], y) for y, m in FY28 if g[(y, m)] < 0.90]
    erl = CA.fy2028(CA.read_forecast(folder, V.FC), busy, pat, model="C")
    m_figs = [int(K.round_half_up(100 * erl[ym], 0)) for ym in FY28]
    m_short = ["%s %d" % (MONTH_NAME[m], y) for y, m in FY28 if erl[(y, m)] < 0.90]
    on_call = c_short == gold_short and c_figs == gold_main
    off_call = m_short != gold_short
    print("cracker's call (Erlang A, busy time %.1f s, the late shift's own patience %.1f s): %s short, July %d (%s)" % (
        busy, pat, ", ".join(c_short), c_figs[0], "lands the golden" if on_call else "MISSES"))
    print("mirror's call (the default path, Erlang C): %s short, July %d (%s)" % (
        ", ".join(m_short), m_figs[0], "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    D = load(folder)
    print("\nthe cracker's hygiene battery:")
    bat = battery(folder, D)
    for check, passed, detail in bat:
        print("  %-4s %s%s" % ("ok" if passed else "FAIL", check, (" (%s)" % detail) if detail else ""))
    rules = filed_rules(folder)
    print("the filed rules it executes, read from the shipped SOP 2.10: %s" % ", ".join(
        "%s %s" % (k, "found" if v else "MISSING") for k, v in rules.items()))
    if not all(p for _, p, _ in bat) or not all(rules.values()):
        print("the battery or a filed rule fails on the cut pack: the routes below are not the cracker's")
        return 1

    full_a, full_b = ask_a(D, FULL_A), ask_b(D, FULL_B)
    fa, fb = keep_a(full_a, gold_a), keep_b(full_b, gold_b)
    if not (all(fa.values()) and all(fb.values())):
        print("CONTROL FAILED: the full includer gives Ask A %d of 8, Ask B %d of 6: the route code does not reproduce "
              "figures.json" % (sum(fa.values()), sum(fb.values())))
        return 1

    routes = {"cracker": (CRACKER_A, CRACKER_B), "mirror": (MIRROR_A, MIRROR_B), "full includer (control)": (FULL_A, FULL_B)}
    res = {}
    for who, (ra, rb) in routes.items():
        a, b = ask_a(D, ra), ask_b(D, rb)
        res[who] = (a, b, keep_a(a, gold_a), keep_b(b, gold_b))
    print("\nAsk A, Halvorsen wireless calls reached and transferred to Wexley by fiscal 2026 quarter (figures.json in "
          "brackets):")
    for who, (a, _, ka, _) in res.items():
        print("  %-26s %s" % (who, "; ".join("%s %d/%d (%d/%d)" % (q, a[q][0], a[q][1], gold_a[q][0], gold_a[q][1])
                                              for q in QUARTERS)))
    print("Ask B, abandoned 911 calls dialled back within two minutes, per cent (figures.json in brackets):")
    for who, (_, b, _, kb) in res.items():
        print("  %-26s %s" % (who, "; ".join("%s %.1f (%.1f)" % (m[:3], K.round_half_up(100 * b[m], 1), gold_b[m])
                                              for m in MONTHS)))

    print("\nper route, figures kept (Ask A of 8, Ask B of 6, both of 14):")
    for who, (_, _, ka, kb) in res.items():
        print("  %-62s %d  %d  %d" % (who, sum(ka.values()), sum(kb.values()), sum(ka.values()) + sum(kb.values())))
    for nm, ch in STOPS_A.items():
        print("  %-62s %d  .  ." % ("Ask A stop: " + nm, sum(keep_a(ask_a(D, dict(CRACKER_A, **ch)), gold_a).values())))
    for nm, ch in STOPS_B.items():
        print("  %-62s .  %d  ." % ("Ask B stop: " + nm, sum(keep_b(ask_b(D, dict(CRACKER_B, **ch)), gold_b).values())))

    crit, W = weights()

    def criteria(who, call_figs):
        _, _, ka, kb = res[who]
        k = {"A " + c: v for c, v in ka.items()}
        k.update({"B " + c: v for c, v in kb.items()})
        k["chart values"] = call_figs == gold_main
        k["chart line"] = True
        return k
    kc, km = criteria("cracker", c_figs), criteria("mirror", m_figs)
    worst = []
    print()
    for wname, w in W.items():
        c, s, p, lc, ls = pair(kc, km, w)
        worst.append((p, ls))
        print("the sheet's formula, %s: cracker keeps %.1f%% (C %.1f), mirror %.1f%% (S %.1f), pair %.1f" % (
            wname, 100 * lc, c, 100 * ls, s, p))
    kept = sum(v for c_, v in kc.items() if not c_.startswith("chart"))
    print("\nCracker keeps: %d of 14 ask figures (Ask A %d of 8, Ask B %d of 6)" % (
        kept, sum(res["cracker"][2].values()), sum(res["cracker"][3].values())))
    print("Mirror leakage: %.1f per cent of ask weight (each criterion equal)" % (100 * worst[0][1]))
    print("Pair ceiling: %.1f (the worse of the two weightings)" % max(p for p, _ in worst))
    if kept:
        print("verdict: the careful solver keeps %d ask figures: the devices it resolves are spent, and the ask layer is "
              "owed a rework (not tuned here)" % kept)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
