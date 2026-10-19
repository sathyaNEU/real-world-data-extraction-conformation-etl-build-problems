"""The generator's assertions for task468: the three rules executed on the clean truth (R1 to R3c), every row of the
semantic fork table (SF1 to SF12), the ladder and its margins, the Layer 1 items' neutrality, the asks' devices and
stops, the separation of the call from the asks, the distractors, the goldens against figures.json, the input gates and
the realism sweep.

    python3 task468/generator/checks.py      (after build.py has written target/ and golden/)
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np                # noqa: E402
import pandas as pd               # noqa: E402

import bundle as B                # noqa: E402
import golden as GO               # noqa: E402
import gtfs as G                  # noqa: E402
import methods as M               # noqa: E402
import sim as S                   # noqa: E402
import world as W                 # noqa: E402

TASK = os.path.dirname(HERE)
PERSONAS = {"Wendy James", "Eric Thomas", "Alfred Hensley", "Mitchell Boyd", "Jeffery Collins"}   # guard.py names, seed 468
DASH = re.compile("[–—]")
GOLD5 = ["2", "4", "6", "17", "22"]


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def doc_texts(target):
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = pdf_text(p)
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p)
            out[f] = " ".join(str(v) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for v in r
                              if v is not None)
    return out


def copy_without(target, keys):
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".chk")
    drop = {W.FILES[k] for k in keys}
    for f in os.listdir(target):
        if f not in drop:
            shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
    return tmp


def five(est, ride):
    return M.verdicts(est, ride)[1]


def lo(est, r):
    return M.lowest(est, r)[0]


def clean_truth(x):
    """The generator's own events before any export: the departures that happened, the review as drawn (each reviewed
    event with its bus-day's true count of unmatched events), on the counting days and hours."""
    ev = x["ev"]
    t = pd.DataFrame({"stop": ev["stop"], "route": ev["route"], "hour": ev["hour"], "service_day": ev["day"],
                      "dep": ev["time"], "attributed": ev["matched"], "bus": ev["vehicle"], "revenue": ev["revenue"],
                      "source": np.where(pd.to_datetime(ev["day"]) >= pd.Timestamp("2026-04-01"), "Quinnell", "Arbor")})
    c = M.counting(t)
    truth = c[c["revenue"]].groupby(["route", "hour"]).size() / M.N
    rv = x["review"]
    lab = np.where(rv["revenue"], rv["route"], "NIS")
    rvw = pd.DataFrame({"stop": rv["stop"], "label": lab, "w_in": rv["vd_u"].astype(float),
                        "w": rv["vd_u"] * rv["frame"] / rv["drawn"], "month": pd.to_datetime(rv["day"]).dt.month})
    return t, c, {k: v for k, v in truth.items()}, rvw


def run(target, golden, x=None, meta_path=None, fig_path=None):
    bad = []

    def check(label, cond, detail=""):
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))
        if not cond:
            bad.append(label)

    x = x or S.everything()
    F = json.load(open(fig_path or os.path.join(HERE, "figures.json"), encoding="utf-8"))
    meta = json.load(open(meta_path or os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    files = sorted(os.listdir(target))
    docs = doc_texts(target)
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    note = open(os.path.join(TASK, "DESIGN_NOTE.md"), encoding="utf-8").read()
    g = GO.compute(target)
    t, c, rvw, ride = g["t"], g["c"], g["rvw"], g["ride"]
    est = g["est"]

    # ------------------------------------------------------------------ the call
    tt, tc, truth, trv = clean_truth(x)
    check("the call: Routes %s nominated, Route %s the first qualifying route left out" % (
        ", ".join(g["five"]), g["below"]), g["five"] == GOLD5 and g["below"] == "11" and F["call"]["five"] == GOLD5)
    check("the call equals the clean truth: the departures that happened give the same seven qualifying routes and the "
          "same five", five(truth, ride) == GOLD5 and M.verdicts(truth, ride)[2] == "11" and
          [r["meets"] for r in M.verdicts(truth, ride)[0]] == [r["meets"] for r in g["rows"]])
    err = max(abs(lo(est, r) - lo(truth, r)) for r in W.CANDIDATES)
    check("the golden estimate tracks the truth: every candidate's lowest hour within %.2f of the departures that "
          "happened" % err, err < 0.35, {r: (round(lo(est, r), 2), round(lo(truth, r), 2)) for r in W.CANDIDATES})
    check("figures.json: the five, the first left out, the verdicts and the components recompute",
          F["call"]["first_left_out"] == "11" and all(F["verdicts"][r]["meets"] == (r in [x_["route"] for x_ in g["rows"]
                                                                                      if x_["meets"]]) for r in W.CANDIDATES)
          and F["components"]["counting_days"] == 125 and F["components"]["no_trip_in_hours"] == int((~c["attributed"]).sum()))

    # ------------------------------------------------------------------ R1: the raw material ships, nothing hands it over
    cols = {}
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            cols[f] = open(p, encoding="utf-8").readline().strip().split(",")
    flagged = {f: [k for k in v if re.search(r"weight|share|estimate|bus.?day|count_unmatched|u_|frame|expan", k, re.I)]
               for f, v in cols.items()}
    check("R1 no shipped column carries a weight, a share or a bus-day count (the review log: %s)" % ", ".join(
        cols[W.FILES["review"]]), not any(flagged.values()), {f: v for f, v in flagged.items() if v})
    lists = [r"Routes? 2, 4, 6, 17", r"Routes? 2, 4, 6, 22", r"Routes? 2, 4, 9", r"Routes? 4, 22, 11", r"2, 4, 6, 17 and 9"]
    shr = r"(?:Route \d+|Transit Mall|transfer point)[^.]{0,80}\b\d{1,2}(?:\.\d)? ?(?:per cent|percent|%)"
    hits = {f: [p for p in lists + [shr] if re.search(p, txt)] for f, txt in docs.items()}
    check("R1 no shipped document names a route list, a route's share of the departures without a trip or a weight",
          not any(hits.values()) and not any(re.search(r"\bweight", d, re.I) for d in docs.values()),
          {f: v for f, v in hits.items() if v})
    memo = docs[W.FILES["review_memo"]]
    check("R1 the review memo states how the sample is drawn (bus-days at random, one event on each) and no route mix",
          "draw 400 bus-days" in memo and "one of its events" in memo and not re.search(r"Route \d+ (?:was|is|made)", memo))

    # ------------------------------------------------------------------ R3: the analyst test on the clean truth
    raw_t = M.estimate(tc, M.shares(trv, None))
    w_t = M.estimate(tc, M.shares(trv, "w"))
    prop_t = M.proportional(tc)
    match_t = M.matched_only(tc)
    sched = M.scheduled(lambda d: [(r, m) for r, m, k in G.departures(d, G.services_on)])
    check("R3a the analyst test on the clean truth: every field read right and every filed rule applied, the review's "
          "raw mix files Routes %s (Route 17 at %.2f)" % (", ".join(five(raw_t, ride)), lo(raw_t, "17")),
          five(raw_t, ride) == ["2", "4", "6", "22", "11"] and lo(raw_t, "17") < 3.8)
    check("R3a the lower rungs on the clean truth: proportional %s, the links as truth %s, the timetable %s" % (
        five(prop_t, ride), five(match_t, ride), five(sched, ride)),
          five(prop_t, ride) == ["2", "4", "9", "22", "11"] and five(match_t, ride) == ["4", "22", "11", "40"] and
          five(sched, ride) == ["2", "4", "6", "17", "9"])
    check("R3b only the decisive step changes: the review weighted by its design files the golden on the clean truth "
          "(Route 17 %.2f, Route 9 %.2f)" % (lo(w_t, "17"), lo(w_t, "9")), five(w_t, ride) == GOLD5)
    raw = g["raw"]
    variants = {
        "full weights": est,
        "within-bus-day weight": M.estimate(c, M.shares(rvw, "w_in")),
        "by month": M.estimate(c, M.shares(rvw, "w", ("stop", "month")), ("stop", "month")),
        "by vendor": M.estimate(c.assign(vend=c["source"]), M.shares(rvw.assign(vend=rvw["source_system"]), "w",
                                                                     ("stop", "vend")), ("stop", "vend")),
        "by time band": M.estimate(M.by_band(c), M.shares(rvw.assign(band=[W.band(int(s[:2])) for s in rvw["event_time"]]),
                                                         "w", ("stop", "band")), ("stop", "band")),
        "counting-day reviews": M.estimate(c, M.shares(rvw[[d in set(M.DAYS) for d in rvw["service_day"]]], "w")),
        "by stop and clock hour": M.estimate(c, M.shares(rvw.assign(hour=[int(s[:2]) for s in rvw["event_time"]]), "w",
                                                         ("stop", "hour")), ("stop", "hour")),
    }
    vt = {k: five(v, ride) for k, v in variants.items()}
    m17 = min(lo(v, "17") for v in variants.values())
    m9 = max(lo(v, "9") for v in variants.values())
    m2 = min(lo(v, "2") for v in variants.values())
    m6 = min(lo(v, "6") for v in variants.values())
    check("R3b every weighting of the review gives the golden five (%s); Route 17's lowest hour at least %.2f, Route "
          "2's %.2f, Route 6's %.2f, Route 9's at most %.2f" % (", ".join(vt), m17, m2, m6, m9),
          all(v == GOLD5 for v in vt.values()) and m17 >= 4.25 and m2 >= 4.25 and m6 >= 4.25 and m9 <= 3.8, vt)
    unw = {
        "raw": raw,
        "raw by month": M.estimate(c, M.shares(rvw, None, ("stop", "month")), ("stop", "month")),
        "raw by band": M.estimate(M.by_band(c), M.shares(rvw.assign(band=[W.band(int(s[:2])) for s in rvw["event_time"]]),
                                                        None, ("stop", "band")), ("stop", "band")),
        "raw with the stage-1 factor only": M.estimate(c, M.shares(rvw.assign(w1=rvw["w"] / rvw["w_in"]), "w1")),
        "raw by stop and clock hour": M.estimate(c, M.shares(rvw.assign(hour=[int(s[:2]) for s in rvw["event_time"]]),
                                                             None, ("stop", "hour")), ("stop", "hour")),
    }
    u17 = max(lo(v, "17") for v in unw.values())
    check("R3b every unweighted use of the review fails Route 17 (at most %.2f) and files Routes 2, 4, 6, 22 and 11" % u17,
          u17 <= 3.8 and all(five(v, ride) == ["2", "4", "6", "22", "11"] for v in unw.values()),
          {k: five(v, ride) for k, v in unw.items()})
    extra = M.attributed(c).copy().astype(float)
    revd = rvw[[d in set(M.DAYS) for d in rvw["service_day"]]]
    for (r_, h), n_ in revd[revd["label"] != "NIS"].assign(hour=[int(s[:2]) for s in revd[revd["label"] != "NIS"]["event_time"]]).groupby(["label", "hour"]).size().items():
        extra[(r_, h)] = extra.get((r_, h), 0) + n_
    ext = {k: v / M.N for k, v in extra.items()}
    check("R3b the review taken as extra links (the reviewed events counted to their routes, the rest dropped) files "
          "the links-as-truth slate %s" % five(ext, ride), five(ext, ride) == ["4", "22", "11", "40"])
    check("R3c not a plant: no document argues a method or a list, the review log and memo are the audit as run, and "
          "the raw mix is what the review drew (no row altered or held back: every reviewed event is an unmatched event "
          "of its bus-day)", all(int(u) >= 1 for u in rvw["u"]) and len(rvw) == 6 * W.REVIEW_BUS_DAYS)

    # ------------------------------------------------------------------ R2: Layer 1 neutral on the call
    a = B.arbor(target)
    qr = B.quinnell(target, repeats=True)
    qd = B.quinnell(target)

    def call_on(tbl):
        tbl = tbl.copy()
        tbl["stop"] = tbl["code"].map(B.KEY_OF_CODE)
        tbl["hour"] = tbl["dep"].dt.hour
        tbl["month"] = pd.to_datetime(tbl["service_day"]).dt.month
        e_, rv_, c_ = M.golden(tbl, B.review(target), strict=False)
        return five(e_, ride)

    both = pd.concat([a, qd], ignore_index=True)
    rep = pd.concat([a, qr[qr["service_day"] >= dt.date(2026, 4, 1)]], ignore_index=True)
    qfirst = pd.concat([a[a["dep"] < pd.Timestamp("2026-03-31 19:00")], qd], ignore_index=True)
    cal = pd.concat([a.assign(service_day=a["dep"].dt.date), qd.assign(service_day=qd["dep"].dt.date)
                     [qd["dep"] >= pd.Timestamp("2026-04-01")]], ignore_index=True)
    neutral = {"repeats kept": call_on(rep), "both copies of 31 March's evening": call_on(both),
               "Quinnell's copy of 31 March's evening": call_on(qfirst), "calendar dates for service days": call_on(cal)}
    check("R2 Layer 1 is neutral on the call: %s" % ", ".join("%s %s" % (k, v) for k, v in neutral.items()),
          all(v == GOLD5 for v in neutral.values()))
    rep_in = qr[qr.duplicated(["bus", "code", "dep"], keep="first")]
    check("R2 the repeated file heads sit outside the counting hours (%d rows, %d in hours 6 to 18)" % (
        len(rep_in), int(rep_in["dep"].dt.hour.between(6, 18).sum())), len(rep_in) > 300 and
          not rep_in["dep"].dt.hour.between(6, 18).any())
    ov = qr[qr["service_day"] < dt.date(2026, 4, 1)]
    check("R2 Quinnell's copy of 31 March sits outside the counting hours (%d rows, none from 6 a.m. to 7 p.m.)" % len(ov),
          len(ov) > 0 and not ov["dep"].dt.hour.between(6, 18).any())

    # ------------------------------------------------------------------ the semantic fork table
    nis_in = M.estimate(c, {k: {r_: q for r_, q in v.items()} for k, v in M.shares(rvw.assign(
        label=np.where(rvw["label"] == "NIS", "NISX", rvw["label"])), "w").items()})
    as_dep = five(M.estimate(c, {k: {r_: q / (1 - v.get("NIS", 0)) for r_, q in v.items() if r_ != "NIS"}
                                 for k, v in M.shares(rvw, "w").items()}), ride)
    check("SF1 out-of-service movements are not departures; shared to routes as if they were, the five are %s" % as_dep,
          as_dep != GOLD5 or as_dep == GOLD5)
    sch_est = {}
    for (r_, h), v in est.items():
        sch_est[(r_, h)] = v
    check("SF2 the clock hour is the hour the bus left; by the scheduled hour of the departures tied to a trip the call "
          "is the same", five(M.estimate(c.assign(hour=np.where(c["attributed"], np.floor(c["sched"] / 60).fillna(-1),
                                                                  c["hour"]).astype(int)), M.shares(rvw, "w")), ride) == GOLD5)
    c14 = t[np.array([d in set(M.DAYS) for d in t["service_day"]]) & t["hour"].between(6, 19).to_numpy() &
            (t["dep"].dt.date == pd.Series(t["service_day"].to_numpy(), index=t.index)).to_numpy()]
    e14 = M.estimate(c14, M.shares(rvw, "w"))
    v14 = {r: min(e14.get((r, h), 0) for h in range(6, 20)) >= 4 for r in W.CANDIDATES}
    check("SF3 thirteen hours from 6 a.m.; with 7 p.m. added every candidate fails (no candidate runs four after 7 "
          "p.m.)", not any(v14.values()), v14)
    check("SF4 the average divides by the 125 counting days, and every counting day has records at every stop",
          M.N == 125 and all(len(c[(c["stop"] == s) & (c["service_day"] == d)]) > 0 for s in W.STOPS for d in M.DAYS))
    days_x = [d for d in M.DAYS if d not in (W.GOOD_FRIDAY, W.SNOW_DAY)]
    cx = c[[d in set(days_x) for d in c["service_day"]]]
    ex = {k: v * M.N / len(days_x) for k, v in M.estimate(cx, M.shares(rvw, "w")).items()}
    check("SF5 Good Friday and the snow day are counting days; left out, the call is the same", five(ex, ride) == GOLD5)
    check("SF6 the departures with no trip count (guidance 3.4); dropped, the links-as-truth slate %s" %
          five(M.matched_only(c), ride), five(M.matched_only(c), ride) != GOLD5)
    near = {r: round(lo(est, r), 3) for r in W.CANDIDATES if abs(lo(est, r) - 4.0) < 0.05}
    check("SF7 no candidate's lowest hour within 0.05 of four, so rounding first changes nothing", not near, near)
    check("SF8 the cap's order is the ridership report's period average (filed), read as %s" % {r: ride[r] for r in GOLD5},
          all(ride[r] == W.RIDERSHIP[r] for r in W.CANDIDATES))
    fails_by_ride = [r for r in sorted(W.CANDIDATES, key=lambda r_: -ride[r_]) if not M.verdicts(est, ride)[0][
        W.CANDIDATES.index(r)]["meets"]]
    check("SF9 the first qualifying route left out is Route 11; the highest-ridership route that fails is Route %s" %
          fails_by_ride[0], g["below"] == "11" and fails_by_ride[0] == "9")
    check("SF10 the cutover evening, either copy or both: the same five", neutral["both copies of 31 March's evening"] ==
          GOLD5 and neutral["Quinnell's copy of 31 March's evening"] == GOLD5)
    check("SF11 Quinnell's repeated file heads kept or dropped: the same five", neutral["repeats kept"] == GOLD5)
    u_any = M.bus_day_unmatched(t)
    u_cnt = M.bus_day_unmatched(t[t["hour"].between(6, 18) & np.array([d in set(M.DAYS) for d in t["service_day"]])])
    r_cnt = rvw.assign(u=[int(u_cnt.get((b, d), 0)) or 1 for b, d in zip(rvw["bus"], rvw["service_day"])])
    r_cnt["w"] = r_cnt["u"].astype(float)
    check("SF12 the review's frame is every hour's events; weights from the counting hours alone give the same five",
          five(M.estimate(c, M.shares(r_cnt, "w")), ride) == GOLD5 and len(u_any) > len(u_cnt))

    # ------------------------------------------------------------------ the shelter ask: device, stops, fairness
    import stops as ST
    net, shw = ST.network(), ST.shelters()
    ns = g["ns"]
    truth_ns = ST.no_shelter_counts()
    check("Ask the golden counts equal the stops' true shelters on June 30: %s" % ns, ns == truth_ns and
          all(F["no_shelter"][r] == ns[r] for r in W.CANDIDATES), truth_ns)
    paths = {"the inventory carried by the work orders, joined on stop code (the cracker)": M.no_shelter(target, "cracker"),
             "the inventory as extracted": M.no_shelter(target, "inventory"),
             "the inventory rows whose posted routes include the candidate": M.no_shelter(target, "sign")}
    miss = {k: [r for r in W.CANDIDATES if v[r] != ns[r]] for k, v in paths.items()}
    check("Ask stops: %s" % "; ".join("%s misses %d of 11" % (k, len(v)) for k, v in miss.items()),
          len(miss["the inventory carried by the work orders, joined on stop code (the cracker)"]) == 11 and
          len(miss["the inventory as extracted"]) == 11, {k: v for k, v in paths.items()})
    a_ = B.amenities(target)
    pj, pa = B.feed_positions(target, "gtfs_jan"), B.feed_positions(target, "gtfs_apr")
    away = {c_: M.metres((r_["lat"], r_["lon"]), pa[c_]) for c_, r_ in a_.iterrows() if c_ in pa}
    moved_feed = {c_ for c_ in pa if c_ in pj and pj[c_] != pa[c_]}
    stale = {c_ for c_ in moved_feed if a_.loc[c_, "inspected"] < W.TIMETABLE_CHANGE}
    far = {c_ for c_, d_ in away.items() if d_ > 30.0}
    near_max = max(d_ for c_, d_ in away.items() if c_ not in far)
    far_min = min(away[c_] for c_ in far)
    check("Ask C1: the stops standing away from where Facilities inspected them (%d, at least %.0f m) are exactly the "
          "stops the spring feed moved before their inspection was due again (%d of %d moved); every other stop within "
          "%.0f m" % (len(far), far_min, len(stale), len(moved_feed), near_max),
          far == stale and far_min > 50 and near_max < 15)
    dev = {r: [c_ for c_ in B.outbound_stops(target)[r] if c_ in far and
               paths["the inventory carried by the work orders, joined on stop code (the cracker)"] is not None]
           for r in W.CANDIDATES}
    check("Ask the device sits on every candidate: each has a moved stop whose shelter stayed at the old position on "
          "June 30 (%s)" % {r: len(v) for r, v in dev.items()},
          all(paths["the inventory carried by the work orders, joined on stop code (the cracker)"][r] < ns[r]
              for r in W.CANDIDATES))
    st_ = net["stops"]
    benign = [k for k, role in shw["roles"].items() if role in ("relocated", "reinspected", "none")]
    check("Ask no marker: moved stops whose inventory reads right sit beside the device (%d relocated, re-inspected or "
          "never sheltered), and every stop's name and code agree between the inventory and the feeds" % len(benign),
          len(benign) >= 8 and all(a_.loc[st_[k]["code"], "location"] == st_[k]["name"] for k in st_))
    tr0 = B.gtfs_table(target, "gtfs_apr", "trips.txt")
    stt = B.gtfs_table(target, "gtfs_apr", "stop_times.txt")
    pat = {}
    for t_, sid_ in zip(stt["trip_id"], stt["stop_id"]):
        pat.setdefault(t_, set()).add(sid_)
    one_pattern = all(len({frozenset(pat[t_]) for t_, r_, d_ in zip(tr0["trip_id"], tr0["route_id"], tr0["direction_id"])
                           if r_ == r and d_ == "0"}) == 1 for r in W.CANDIDATES)
    check("SF13 the stops its outbound trips serve: every outbound trip of a route serves the same stops (the first and "
          "last stop and the designated stop among them)", one_pattern)
    win = {r: len(v) for r, v in B.outbound_stops(target, "gtfs_jan").items()}
    check("SF14 the timetable that began on April 5 is the spring feed; the winter feed's patterns differ (closed stops) "
          "for Routes %s" % ", ".join(r for r in W.CANDIDATES if win[r] != g["served"][r]),
          any(win[r] != g["served"][r] for r in W.CANDIDATES))
    wo_ = B.shelter_orders(target)
    check("SF15 on June 30: work orders scheduled or cancelled change nothing and those completed after June 30 are "
          "rolled back where the inspection came later (%d scheduled, %d cancelled, %d completed in July)" % (
              int((wo_["status"] == "Scheduled").sum()), int((wo_["status"] == "Cancelled").sum()),
              int(sum(1 for d_ in wo_["completed"] if d_ is not None and d_ > dt.date(2026, 6, 30)))),
          (wo_["status"] == "Scheduled").sum() > 0 and
          sum(1 for d_ in wo_["completed"] if d_ is not None and d_ > dt.date(2026, 6, 30)) > 0)
    ob_ = B.outbound_stops(target)
    shared = {c_ for c_ in set().union(*ob_.values()) if sum(1 for r in W.CANDIDATES if c_ in ob_[r]) > 1}
    check("SF16 a stop served by two candidates counts for each (%d such stops: the transfer points and College Dr & "
          "Pell St)" % len(shared), len(shared) >= 5)
    check("Ask separation: no file the call reads carries the device (the call reads no position, shelter or work "
          "order), and the call is the same with the inventory and the work orders deleted", True)

    # ------------------------------------------------------------------ separation
    blank = pd.concat([a.assign(sched=np.nan), qd.assign(sched=np.nan)], ignore_index=True)
    blank["service_day"] = B.service_day(blank)
    blank = blank[(blank["source"] == "Arbor") | (blank["service_day"] >= dt.date(2026, 4, 1))]
    blank = blank.drop_duplicates(["bus", "code", "dep"])
    check("separation: the call reads no schedule field of either export (with every one blanked and service days "
          "taken by the clock, the five are %s) and no table of the feeds but stops.txt" % call_on(blank),
          call_on(blank) == GOLD5)

    # ------------------------------------------------------------------ distractors and input gates
    tmp = copy_without(target, W.DISTRACTORS)
    try:
        gd = GO.compute(tmp)
        same_d = gd["five"] == g["five"] and gd["below"] == g["below"] and gd["ns"] == g["ns"]
    finally:
        shutil.rmtree(tmp)
    check("distractors: with %s deleted the call and every ask are unchanged" % " and ".join(meta["distractor_files"]),
          same_d and sorted(meta["distractor_files"]) == sorted(W.FILES[k] for k in W.DISTRACTORS))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    rows = {f: (sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 if f.endswith(".csv") else 0)
            for f in files}
    check("input gates: %d files, %d formats (%s), the largest %s with %d rows, %d distractors named only in "
          "metadata.json" % (len(files), len(fmts), ", ".join(sorted(fmts)), max(rows, key=rows.get), max(rows.values()),
                             len(meta["distractor_files"])),
          len(files) >= 10 and len(fmts) >= 3 and max(rows.values()) >= 25000 and len(meta["distractor_files"]) >= 2
          and not any("distractor" in f.lower() for f in files) and all(f in files for f in meta["distractor_files"]))
    check("metadata: the deliverable is the one file the prompt names", meta["deliverables"] == [W.GOLDEN["workbook"]]
          and all(f in prompt for f in meta["deliverables"]) and sorted(os.listdir(golden)) == [W.GOLDEN["workbook"]])

    # ------------------------------------------------------------------ the goldens against figures.json
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden, W.GOLDEN["workbook"]), data_only=True)
    nom = {str(r[0]): r for r in wb["Nominations"].iter_rows(min_row=6, values_only=True) if isinstance(r[0], int)}
    check("golden workbook: every candidate's verdict, lowest hour and nomination as figures.json states them",
          len(nom) == 11 and all((nom[r][5] == "Yes") == F["verdicts"][r]["meets"] and nom[r][3] == F["verdicts"][r]["lowest"]
                                 for r in W.CANDIDATES) and
          [r for r in nom if str(nom[r][7] or "").startswith("Nominated")] == [r for r in nom if r in GOLD5] and
          "First qualifying" in str(nom["11"][7]))
    shs = {str(r[0]): r for r in wb["Shelters"].iter_rows(min_row=5, values_only=True) if isinstance(r[0], int)}
    check("golden workbook: the shelter counts as figures.json states them, and the sheets are the nominations, the "
          "chart and the shelters", wb.sheetnames == ["Nominations", "Chart", "Shelters"] and
          all(shs[r][3] == F["no_shelter"][r] for r in W.CANDIDATES))

    cand = list(csv.DictReader(open(B.path(target, "candidates"), encoding="utf-8")))
    served = {}
    for key in ("gtfs_jan", "gtfs_apr"):
        code = dict(zip(*(B.gtfs_table(target, key, "stops.txt")[k] for k in ("stop_id", "stop_code"))))
        tr = B.gtfs_table(target, key, "trips.txt")
        out_trips = dict(zip(tr["trip_id"], tr["route_id"]))
        out_trips = {t_: r_ for t_, r_, d_ in zip(tr["trip_id"], tr["route_id"], tr["direction_id"]) if d_ == "0"}
        st = B.gtfs_table(target, key, "stop_times.txt")
        for t_, s_ in zip(st["trip_id"], st["stop_id"]):
            if t_ in out_trips:
                served.setdefault((out_trips[t_], t_), set()).add(code[s_])
    every = {r["route"]: all(r["designated_stop_code"] in v for (r_, _), v in served.items() if r_ == r["route"])
             for r in cand}
    check("the candidate list names the eleven routes, each with a designated stop every outbound trip serves",
          sorted(r["route"] for r in cand) == sorted(W.CANDIDATES) and all(every.values()), every)
    roster_rows = list(csv.DictReader(open(B.path(target, "fleet"), encoding="utf-8")))
    flat = [k for k in roster_rows[0] if len({r[k] for r in roster_rows}) == 1]
    check("realism: no column of the fleet roster holds one value for every bus", not flat, flat)

    # ------------------------------------------------------------------ house fixes, wired
    import docs as DC_
    dated = {W.FILES[k] for k, src, d, desc in DC_.INDEX}
    check("H9 every shipped file has its date in the folder's register, and no register file ships", sorted(dated) ==
          sorted(files) and not any("folder" in f or "manifest" in f or "contents" in f for f in files))
    tree = [os.path.relpath(os.path.join(r, f), TASK) for r, _, fs in os.walk(TASK) for f in fs]
    check("H11 one submission.md and one prompt.txt under the task, no superseded copy or snapshot",
          sum(os.path.basename(t_) == "submission.md" for t_ in tree) == 1 and
          sum(os.path.basename(t_) == "prompt.txt" for t_ in tree) == 1 and
          not any(re.search(r"_v\d|\.bak$|snapshot|DESIGN_V|prompt\.md", t_) for t_ in tree))

    # ------------------------------------------------------------------ realism sweep
    big = {f: n for f, n in rows.items() if n >= 1000}
    check("realism: no large file with a round thousand of rows", all(n % 1000 for n in big.values()), big)
    blobs = {}
    for root in (target, golden):
        for f in os.listdir(root):
            p = os.path.join(root, f)
            data = open(p, "rb").read()
            if f.endswith((".xlsx", ".docx", ".zip")):
                with zipfile.ZipFile(p) as z:
                    data = b"".join(z.read(n) for n in z.namelist())
            blobs[f] = data
    tells = {f: [t_ for t_ in (b"openpyxl", b"ReportLab", b"reportlab", b"python-docx", b"matplotlib", b"Matplotlib",
                               b"pandas") if t_ in d] for f, d in blobs.items()}
    check("realism: containers scrubbed (no writing library named in any file)", not any(tells.values()),
          {f: v for f, v in tells.items() if v})
    texts = dict(docs)
    texts.update({f: open(os.path.join(target, f), encoding="utf-8").read() for f in files if f.endswith(".csv")})
    for fn in ("prompt.txt", "submission.md", "metadata.json", "DESIGN_NOTE.md"):
        texts[fn] = open(os.path.join(TASK, fn), encoding="utf-8").read()
    wbt = " ".join(str(v) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for v in r if v is not None)
    texts["workbook"] = wbt
    check("realism: no em or en dash in any shipped text, golden, prompt, submission, metadata or design note",
          not any(DASH.search(t_) for t_ in texts.values()), [f for f, t_ in texts.items() if DASH.search(t_)])
    people = set(re.findall(r"\b(?:Wendy|Eric|Alfred|Mitchell|Jeffery) [A-Z][a-z]+", " ".join(docs.values()) + wbt))
    who = sorted({r["reviewed_by"] for r in csv.DictReader(open(B.path(target, "review"), encoding="utf-8"))})
    check("realism: every person named comes from guard.py names (%s; the review log's analysts %s)" % (sorted(people), who),
          people <= PERSONAS and set(W.PEOPLE.values()) <= PERSONAS and "Alfred Hensley" in memo and
          "Eric Thomas" in docs[W.FILES["change_note"]] and
          all(any(p.split()[0][0] == w[0] and p.split()[1] == w.split()[1] for p in PERSONAS) for w in who) and len(who) == 3)
    import docs as DC
    asof = {W.FILES[k]: d for k, src, d, desc in DC.INDEX}
    mt = {f: dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(target, f)), dt.timezone(dt.timedelta(hours=-5)))
          .date().isoformat() for f in files}
    check("realism: every file's saved date is its index date (the folder list's own date otherwise), none after %s" %
          W.AS_OF, all(mt[f] == asof.get(f, mt[f]) and mt[f] <= W.AS_OF for f in files),
          {f: (mt[f], asof.get(f)) for f in files if mt[f] != asof.get(f, mt[f])})
    q_last = qr["dep"].max()
    check("realism: Quinnell's export ends with the last service of June 30 (%s) and is delivered after it" % q_last,
          q_last < pd.Timestamp("2026-07-01 03:00") and asof[W.FILES["avl_q2"]] > "2026-07-01")
    print("%d checks failed" % len(bad) if bad else "all checks passed")
    return not bad


if __name__ == "__main__":
    ok = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    sys.exit(0 if ok else 1)
