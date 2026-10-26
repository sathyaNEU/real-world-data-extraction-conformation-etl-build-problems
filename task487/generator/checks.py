"""The generator's assertions on the cut pack and the clean truth: the input gates, the realism sweep, the three rules
(R1 to R3), the Layer 1 items, the ladder, both families, the semantic fork rows (SF1 to SF24), the separation of the
asks from the call and the fairness of their devices.

    python3 task487/generator/checks.py
"""
import collections
import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import ceiling as C     # noqa: E402
import family as FAM    # noqa: E402
import golden as G      # noqa: E402
import metadata as M    # noqa: E402
import pack_read as PR  # noqa: E402
import world as W       # noqa: E402

RESULTS = []
LO, HI = 48.0, 60.0          # band C
Y_MIN = dt.date(1900, 1, 1)


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-62s %s" % ("PASS" if ok else "FAIL", label, detail))


def inside(t, margin=1.0):
    return LO + margin <= t <= HI - margin


# ---------------------------------------------------------------- the clean truth
def clean(w):
    """the world's own windows and events: every visit as it happened, every event's true start"""
    at = {(e["bat"], round(e["arr"], 6)): e for e in w.events}
    win, evs = [], []
    for b in w.bats:
        vs = w.visits[b["code"]]
        for a, c in zip(vs[:-1], vs[1:]):
            if W.day_of(c["arr"]).year != 2026:
                continue
            e = at.get((b["code"], round(c["arr"], 6)))
            win.append(dict(bat=b["code"], w=c["arr"] - a["dep"], kind=e["kind"] if e else None, tel=b["tel"],
                            comb=b["comb"], route=b["route"], cls=b["cls"]))
            if e:
                evs.append(dict(e, tel=b["tel"]))
    return win, evs


def clean_total(w, rt, evs, start):
    s = 0.0
    for e in evs:
        st = e["start"] if (e["kind"] == "PV" and e["tel"]) else start(e)
        s += W.methane(rt, e["bat"], st, e["closed"])
    return s / 1000


def main():
    p = PR.read()
    g = G.compute(p)
    files = sorted(os.listdir(TARGET))
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ---------------------------------------------------------------- input gates
    check("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {os.path.splitext(f)[1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), "rb")) - 1 for f in files if f.endswith((".csv", ".jsonl")))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("gate: two or more distractors named", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    check("gate: every file has a source, date and licence", set(M.SOURCES) == set(files))
    check("gate: no file name names the step", not any(re.search(r"start|visit_started|window|expected|share", f)
                                                       for f in files))
    import inspect
    src = inspect.getsource(G)
    check("gate: the golden reads no distractor", "hauler" not in src and "sales" not in src)
    check("gate: the call reads no work order", "workorders" not in inspect.getsource(G.compute).split("sched =")[0])

    # ---------------------------------------------------------------- the call
    check("call: band C at 54 to 56 t", g["band"] == "C" and 54 <= g["total"] <= 56, "%.2f t" % g["total"])
    check("call: figures.json carries the call", figs["call"] == {"band": "C", "levy_cad": 171000,
                                                                  "rate_per_battery_cad": 950, "batteries": 180})
    check("call: the total sits inside band C with 4 t either side", inside(g["total"], 4.0), "%.2f t" % g["total"])

    # ---------------------------------------------------------------- the ladder on the pack
    lad = {k: G.compute(p, start=k)["total"] for k in ("midpoint", "departure", "hatch_departure", "hatch_quarter",
                                                         "hatch_third")}
    check("ladder L0 default path (every undated start mid-window): band B", G.band(lad["midpoint"])[0] == "B",
          "%.2f t" % lad["midpoint"])
    check("ladder L0 sits 2 t or more under band C", lad["midpoint"] <= LO - 2.0, "%.2f t" % lad["midpoint"])
    check("ladder L1 every undated start at the previous departure: band E", G.band(lad["departure"])[0] == "E",
          "%.2f t" % lad["departure"])
    check("ladder L2 hatches at the departure, the rest mid-window: band E", G.band(lad["hatch_departure"])[0] == "E",
          "%.2f t" % lad["hatch_departure"])
    check("ladder L3 hatches a quarter in, the rest mid-window: band D", G.band(lad["hatch_quarter"])[0] == "D",
          "%.2f t" % lad["hatch_quarter"])
    check("ladder L3 sits 3 t or more over band C", lad["hatch_quarter"] >= HI + 3.0, "%.2f t" % lad["hatch_quarter"])
    check("ladder: a third in for hatches (a guess, not a route) lands C", G.band(lad["hatch_third"])[0] == "C",
          "%.2f t (recorded, not a rung)" % lad["hatch_third"])

    # ---------------------------------------------------------------- the standing family on the pack
    fam = {}
    for grp in ("route", "cls", "bat"):
        fam["group_" + grp] = G.compute(p, fit_group=grp)["total"]
    fam.update(FAM.forms(p, g))
    for k, v in fam.items():
        sfid = "SF12" if k.startswith("group_") else "SF13"
        check("%s family %s: band C with 2 t either side" % (sfid, k), inside(v, 2.0), "%.2f t" % v)
    spread = max(fam.values()) - min(fam.values())
    check("family: spread under 5 t on a 10 t band", spread < 5.0, "%.2f t (%.2f to %.2f)" % (
        spread, min(fam.values()), max(fam.values())))
    lr = g["fits"]["TH"]["lr"]
    check("family: the hatch share is refuted at zero (2 dlogL over 40)", lr > 40, "2 dlogL %.1f" % lr)
    check("family: no share for pilots or relief valves (2 dlogL under 6)",
          g["fits"]["CP"]["lr"] < 6 and g["fits"]["PV"]["lr"] < 6,
          "pilots %.1f, relief %.1f" % (g["fits"]["CP"]["lr"], g["fits"]["PV"]["lr"]))
    jw = FAM.jump_vs_weibull(g)
    check("family: the share-and-rate form fits hatches better than Weibull", jw > 0, "2 dlogL %.1f" % jw)

    # ---------------------------------------------------------------- R1, R2 and R3
    w = W.build()
    rt = W.rate_table(w)
    win, evs = clean(w)
    check("R1 the field's raw material ships: every window and every find", len(g["windows"]) > 45000 and
          len(g["rows"]) > 1500, "%d windows, %d events" % (len(g["windows"]), len(g["rows"])))
    cols = set()
    for k in ("register", "fieldlog", "sites"):
        cols |= set(p[k][0])
    cols |= set(p["sitelink"][0]) | set(p["events"][0])
    check("R1 no shipped column holds an undated start or a cause", not any(
        re.search(r"start|cause|left|origin|started", c, re.I) for c in cols), ", ".join(sorted(cols))[:80])
    texts = " ".join(str(r["Event"]) + " " + str(r["Action"]) for r in p["events"])
    check("R1 the register's words never say who or what opened an event", not re.search(
        r"left open|not latched|unlatched|gauger|previous visit|last visit|since", texts, re.I))
    for name, kw in (("check-in app and register offsets read as UTC wall time", dict(utc=False)),
                     ("check-in app geofence re-entries kept as visits", dict(merge_split=False)),
                     ("the June visits in both apps kept twice", dict(dedupe_parallel=False)),
                     ("BT-0907's records not carried to BT-0907A", dict(rename=False)),
                     ("the journal's host time for the stuck valves", dict(rtu_time=False))):
        t = G.compute(p, **kw)["total"]
        check("R2 %s: same call" % name, G.band(t)[0] == "C", "%.2f t" % t)
    # the free-text kinds read as one kind: the pooled fit
    pooled = pooled_total(p, g)
    check("R2 the register's kinds pooled into one fit: same call", G.band(pooled)[0] == "C", "%.2f t" % pooled)
    fk = G.fits(win)
    gold_clean = clean_total(w, rt, evs, lambda e: e["arr"] - float(G.expected_hours(
        fk[e["kind"]]["p"], fk[e["kind"]]["b"], np.array([e["arr"] - e["dep"]]))[0]))
    mid_clean = clean_total(w, rt, evs, lambda e: (e["dep"] + e["arr"]) / 2)
    true_clean = clean_total(w, rt, evs, lambda e: e["start"])
    check("R3a analyst test on the clean truth (mid-window starts): band B", G.band(mid_clean)[0] == "B",
          "%.2f t" % mid_clean)
    check("R3b the decisive step alone on the clean truth: band C", G.band(gold_clean)[0] == "C", "%.2f t" % gold_clean)
    check("R3b the clean truth's own starts: band C", G.band(true_clean)[0] == "C", "%.2f t" % true_clean)
    check("R3b the golden on the pack matches the clean truth's golden within 1 t", abs(gold_clean - g["total"]) < 1.0,
          "%.2f against %.2f" % (gold_clean, g["total"]))
    check("R3b the fit is closer to the truth than the midpoint", abs(gold_clean - true_clean) < abs(mid_clean - true_clean),
          "%.2f and %.2f from %.2f" % (gold_clean, mid_clean, true_clean))
    dep_clean = clean_total(w, rt, evs, lambda e: e["dep"])
    check("R3b lower rung, every start at the departure, stays wrong", G.band(dep_clean)[0] != "C", "%.2f t" % dep_clean)
    vs_share = sum(e["visit_started"] for e in evs) / max(1, sum(e["kind"] == "TH" for e in evs))
    check("R3 the world's hatches are part visit-started, part between visits", .15 < vs_share < .5,
          "%.2f of hatches" % vs_share)
    check("R3c no plant: no memo, draft or prior return ships", not any(re.search(r"memo|draft|prior|2025_return", f)
                                                                       for f in files))
    # alarm-timed relief valves sit evenly in their windows, as the default path reads them
    pos = [(r["start"] - r["dep"]) / (r["arr"] - r["dep"]) for r in g["rows"] if r["basis"] == "ALARM"]
    check("R3 the alarm-timed relief valves spread across their windows", .35 < np.mean(pos) < .65 and len(pos) >= 40,
          "%d, mean position %.3f" % (len(pos), np.mean(pos)))

    # ---------------------------------------------------------------- the data-native sentence
    W_ = np.array([x["w"] for x in g["windows"]])
    K_ = np.array([x["kind"] or "" for x in g["windows"]])
    day, wkd = (W_ >= 20) & (W_ < 30), (W_ >= 56) & (W_ < 80)
    ratio_h = (K_[wkd] == "TH").mean() / (K_[day] == "TH").mean()
    ratio_w = W_[wkd].mean() / W_[day].mean()
    ratio_r = (K_[wkd] == "PV").mean() / (K_[day] == "PV").mean()
    check("native: hatches after a weekend window about twice a weekday's", 1.8 < ratio_h < 2.5, "%.2f times" % ratio_h)
    check("native: the window itself three times as long", 2.7 < ratio_w < 3.3, "%.2f times" % ratio_w)
    check("native: relief valves near the window ratio", ratio_r > 2.4, "%.2f times" % ratio_r)

    # ---------------------------------------------------------------- semantic fork rows
    sf(p, g)

    # ---------------------------------------------------------------- separation and the asks
    stuck = [x for x in w.alarms if x["stuck"]]
    out_by = collections.defaultdict(list)
    for code, a, c in w.outages:
        out_by[code].append((a, c))
    held = sum(1 for x in stuck if any(a <= x["t"] < c for a, c in out_by[x["bat"]]))
    check("separation: no stuck relief lift falls in a radio outage", held == 0, "%d of %d" % (held, len(stuck)))
    check("separation: the call reads no leak survey or tracker file", all(
        k not in inspect.getsource(G.events) + inspect.getsource(G.visits) + inspect.getsource(G.rates) +
        inspect.getsource(G.windows) for k in ("ldar_surveys", "ldar_tags")))
    gold, keeps = C.measure(p)
    n = len(gold)
    check("asks: 24 graded Schedule B figures", n == 24)
    for k in ("cracker", "sessions_right_completed_days", "tickets_right_every_session", "register_runs_only",
              "tags_as_leaks_only", "received_as_survey_day", "one_leak_a_work_order", "tracker_closure_only"):
        check("asks: %s keeps at most one" % k, keeps[k][0] <= 1, "%d of %d" % (keeps[k][0], n))
    check("asks: the mirror keeps a fifth or less", keeps["mirror"][0] <= 4, "%d of %d" % (keeps["mirror"][0], n))
    check("asks: every reference's date taken as the repair keeps a quarter or less",
          keeps["reference_dates_everywhere"][0] <= 6, "%d of %d" % (keeps["reference_dates_everywhere"][0], n))
    check("asks: the route app's runs for both halves move every second half",
          keeps["route_app_runs_both_halves"][1]["h2_t"] == 0)
    check("asks: the check-in app's runs for both halves move every first half",
          keeps["checkin_runs_both_halves"][1]["h1_t"] == 0)
    check("asks: the register's runs for the second half move every second half",
          keeps["register_runs_second_half"][1]["h2_t"] == 0)
    for k in ("latest_rate", "one_leak_a_component"):
        check("asks: %s moves most figures" % k, keeps[k][0] <= 8, "%d of %d" % (keeps[k][0], n))
    check("asks: not clipped to 2026 moves every first half", keeps["not_clipped_to_2026"][1]["h1_t"] == 0)
    check("asks: pair ceiling 40 or under", C.pair(keeps["cracker"][0], keeps["mirror"][0], n) <= 40,
          "%.1f" % C.pair(keeps["cracker"][0], keeps["mirror"][0], n))
    reg, cur = G.codes(p)
    # the runs: one run a battery in each half, redrawn on 1 July and for 2027, every route in each redraw
    h1, h2, n1, n2 = G.runs(p, cur)
    check("asks: one run a battery in each half (route app to June, check-in app from July)",
          max(n1.values()) == 1 and max(n2.values()) == 1 and len(h1) == len(h2) == 180)
    jul = [b for b in h1 if h2[b] != h1[b]]
    jan = [b for b in h2 if reg[b]["route"] != h2[b]]
    check("asks: twelve batteries changed run on 1 July, every route giving one and taking one", len(jul) == 12 and
          collections.Counter(h1[b] for b in jul) == collections.Counter(h2[b] for b in jul) and
          len({h1[b] for b in jul}) == 12, ", ".join(sorted(jul)))
    check("asks: twelve more changed run for 2027, every route giving one and taking one", len(jan) == 12 and
          not set(jan) & set(jul) and len({h2[b] for b in jan}) == 12, ", ".join(sorted(jan)))
    check("asks: the pilot runs R03 and R09 trade only with each other",
          all({h1[b], h2[b]} <= {"R03", "R09"} for b in jul if "R03" in (h1[b], h2[b]) or "R09" in (h1[b], h2[b])) and
          all({h2[b], reg[b]["route"]} <= {"R03", "R09"} for b in jan if "R03" in (h2[b], reg[b]["route"]) or
              "R09" in (h2[b], reg[b]["route"])))
    early = [b for b in h1 if b[3:5] != h1[b][1:]]
    check("asks: some batteries ran another area's run all year (the codes' area is not the run: the twin)",
          len([b for b in early if b not in jul and b not in jan and h1[b] == h2[b] == reg[b]["route"]]) >= 6,
          "%d batteries" % len(early))
    site = {x["site_id"]: x["battery"] for x in p["sites"]}
    late = collections.defaultdict(set)
    for r in p["sitelink"]:
        if r["check_in"][:10] >= "2027-01-04":
            late[site[r["site"]]].add(r["run"])
    check("asks: the January check-ins carry the register's runs", all(late[b] <= {reg[b]["route"]} for b in late) and
          all(late[b] for b in jan))
    first = {}
    for r in p["fieldlog"]:
        hh = dt.datetime.fromisoformat(r["Arrived"])
        k = (cur.get(r["Site"]), hh.date())
        first[k] = min(first.get(k, 24.0), hh.hour + hh.minute / 60)
    tod = collections.defaultdict(list)
    for (b, d_), x in first.items():
        tod[b].append(x)
    gap = []
    for movers, a_of, b_of in ((jul, h1, h2), (jan, h2, {c_: r_["route"] for c_, r_ in reg.items()})):
        for b in movers:
            took = [c_ for c_ in movers if a_of[c_] == b_of[b] and b_of[c_] == a_of[b]]
            gap.append(abs(np.mean(tod[b]) - np.mean(tod[took[0]])) if took else 9.0)
    check("realism: a run's traded batteries keep their place in its day", max(gap) < .35,
          "largest gap %.2f h" % max(gap))
    # the repairs: a re-check that found a point still leaking names its tag again, before the next survey
    wos = G.leak_wos(p)
    logd = collections.defaultdict(list)
    for r in p["ldar_surveys"]:
        logd[cur.get(r["Battery"], r["Battery"])].append(dt.date.fromisoformat(r["Surveyed"]))
    crew = {(cur.get(r["Battery"], r["Battery"]), r["Surveyed"]): r["Technician"] for r in p["ldar_surveys"]}
    redo = [r for r in p["ldar_tags"] if wos.get(r["Tag"]) and max(wos[r["Tag"]]) > (G.as_date(r["Closed"]) or Y_MIN)]
    texts = {}
    for r in p["workorders"]:
        for t in re.findall(r"\((T-\d{5})\)", r["Description"]):
            texts.setdefault(t, []).append((r["Completed"], r["Description"]))
    check("asks: every later repair of a closed tag says the first repair did not hold", all(
        "did not hold" in sorted(texts[r["Tag"]])[-1][1] for r in redo), "%d tags" % len(redo))
    check("asks: no first repair's work order says so", not any(
        "did not hold" in d for r in p["ldar_tags"] for c, d in texts.get(r["Tag"], [])
        if G.as_date(r["Closed"]) and c == G.as_date(r["Closed"]).isoformat()))
    shipped = " ".join(open(os.path.join(TARGET, f_), encoding="utf-8").read() for f_ in files
                       if f_.endswith((".csv", ".txt", ".jsonl")))
    check("asks: no shipped text says a session re-checks, verifies or approves anything", not re.search(
        r"re-?check|verif|approv|re-?screen|follow-?up", shipped, re.I))
    full = G.surveys(p, g["opts"], cur)
    nxt_ok = all(max(wos[r["Tag"]]) < min([d for d in full[cur.get(r["Battery"], r["Battery"])]
                                           if d > G.as_date(r["Closed"])] or [dt.date(2027, 1, 1)]) for r in redo)
    check("asks: every re-check repair falls before the battery's next survey", nxt_ok)
    check("asks: no re-check on a shutdown repair", not any("shutdown" in d for r in redo for c, d in texts[r["Tag"]]))
    check("asks: re-checked tags on most routes", len({h1.get(cur.get(r["Battery"], r["Battery"])) for r in redo}) >= 9,
          "%d tags on %d routes" % (len(redo), len({h1.get(cur.get(r["Battery"], r["Battery"])) for r in redo})))
    agree = [r for r in p["ldar_tags"] if r["Work order"] and G.as_date(r["Closed"]) and
             G.as_date(r["Closed"]).year == 2026]
    wo_day = {int(r["WO"]): r["Completed"] for r in p["workorders"]}
    check("asks: every 2026 closure is its work order's completion day (the tracker and the work orders agree)", all(
        wo_day[int(r["Work order"])] == G.as_date(r["Closed"]).isoformat() for r in agree), "%d tags" % len(agree))
    generic = sum(1 for r in p["workorders"] if r["Description"] == "Replaced packing on wellhead stuffing box")
    check("asks: packing repairs with no tag also run through the maintenance system (the twin)", generic >= 30,
          "%d work orders" % generic)
    # the first device: the camera crews' re-checks of repaired points sit in the survey log beside the surveys
    rows_by = collections.defaultdict(list)
    for r in p["ldar_surveys"]:
        rows_by[cur.get(r["Battery"], r["Battery"])].append(r)
    is_full = lambda b, r: dt.date.fromisoformat(r["Surveyed"]) in full[b]
    small = [(b, r) for b, rs in rows_by.items() for r in rs if not is_full(b, r)]
    check("asks: three surveys at every battery, autumn 2025, spring and autumn 2026",
          all(len(v) == 3 for v in full.values()) and len(full) == 180)
    check("asks: every re-check session screened under a third of its battery's smallest survey", all(
        3 * max([int(r["PointsScreened"]) for r in rs if not is_full(b, r)] or [0]) <
        min(int(r["PointsScreened"]) for r in rs if is_full(b, r)) for b, rs in rows_by.items()), "%d sessions" % len(small))
    check("asks: no session tags a leak, and surveys that tagged none are a fifth of all (the twin)",
          all(int(r["LeaksTagged"]) == 0 for b, r in small) and
          sum(1 for b, rs in rows_by.items() for r in rs if is_full(b, r) and int(r["LeaksTagged"]) == 0) >= 100)
    check("asks: no session within a week of a survey", not any(
        abs((dt.date.fromisoformat(r["Surveyed"]) - d).days) <= 7 for b, r in small for d in full[b]))
    every = {b: sorted(dt.date.fromisoformat(r["Surveyed"]) for r in rs) for b, rs in rows_by.items()}
    off = sum(1 for r in p["ldar_tags"] if [x for x in every[cur.get(r["Battery"], r["Battery"])] if x <= G.as_date(
        r["Received"])][-1] != [x for x in full[cur.get(r["Battery"], r["Battery"])] if x <= G.as_date(r["Received"])][-1])
    check("asks: every tag lands on the same survey whether or not sessions are read as surveys", off == 0, "%d" % off)
    on = {(b, r["Surveyed"]) for b, r in small}
    wo2 = [r for r in p["workorders"] if "did not hold" in r["Description"]]
    check("asks: every repair at a re-check falls on a session at its battery", all(
        (cur.get(r["Battery"], r["Battery"]), r["Completed"]) in on for r in wo2), "%d work orders" % len(wo2))
    check("asks: sessions in both halves on every route",
          {h1.get(b) for b, r in small if "2026-01-01" <= r["Surveyed"] < "2026-07-01"} >= set(C.ROUTES) and
          {h2.get(b) for b, r in small if r["Surveyed"] >= "2026-07-01"} >= set(C.ROUTES))
    # the second device: a contract work order is completed when its field tickets are approved
    import asks as A
    ft = [r for r in p["workorders"] if r["Reference"].startswith("FT ")]
    check("asks: every contract order completes on the 10th of the month after its ticket, or the next working day",
          all(dt.date.fromisoformat(r["Completed"]) == A.approval(G.ref_day(r["Reference"])) for r in ft),
          "%d orders" % len(ft))
    check("asks: every field ticket outside a shutdown is dated on a working day", all(
        A.workday(G.ref_day(r["Reference"])) == G.ref_day(r["Reference"]) for r in ft if "shutdown" not in
        r["Description"]))
    seen_on = {r["Tag"]: at_tag for r, at_tag in ((r, [x for x in full[cur.get(r["Battery"], r["Battery"])]
                                                     if x <= G.as_date(r["Received"])][-1]) for r in p["ldar_tags"])}
    leak_ft = [r for r in ft if r["Description"].startswith("Leak repair")]
    check("asks: every contract leak repair's ticket falls after the survey that tagged its leaks", all(
        G.ref_day(r["Reference"]) > max(seen_on[t] for t in re.findall(r"\((T-\d{5})\)", r["Description"]))
        for r in leak_ft), "%d orders" % len(leak_ft))
    ehs = [r for r in p["workorders"] if r["Reference"].startswith("EHS ")]
    check("asks: every leak program notification is on or before its order's completion", all(
        G.ref_day(r["Reference"]) <= dt.date.fromisoformat(r["Completed"]) for r in ehs), "%d orders" % len(ehs))
    leak26 = [r for r in p["workorders"] if r["Description"].startswith("Leak repair") and "did not hold" not in
              r["Description"]]
    share = sum(1 for r in leak26 if r["Reference"].startswith("FT ")) / len(leak26)
    check("asks: the contractor did between half and four fifths of the leak repairs", .5 <= share <= .8, "%.2f" % share)
    check("asks: contract work outside the leak program completes the same way (the twin)",
          sum(1 for r in ft if not r["Description"].startswith("Leak repair")) >= 100,
          "%d orders" % sum(1 for r in ft if not r["Description"].startswith("Leak repair")))
    own = collections.Counter(dt.date.fromisoformat(r["Completed"]).day for r in p["workorders"]
                              if not r["Reference"].startswith("FT "))
    check("realism: the field's own work orders complete through the month", len(own) >= 28, "%d days" % len(own))
    check("asks: no contract leak repair in December 2026 (the crews had left)", not any(
        G.ref_day(r["Reference"]) >= dt.date(2026, 12, 1) for r in leak_ft))
    # fair: the golden's Schedule B is the world's own leaks, every repair on the day it was done
    tr = A.fugitive_truth(w)
    bat = {b["code"]: b for b in w.bats}
    truth = collections.defaultdict(float)
    for (c, h), v in tr.items():
        truth[(bat[c]["route"] if h == "h1" else bat[c]["run_h2"], h)] += v
    worst = max(abs(truth[(r, h)] - g["sched"][r][h]) for r in C.ROUTES for h in ("h1", "h2"))
    check("asks: the golden's Schedule B is the world's own leaks (fair)", worst < 1e-6, "%.1e t" % worst)
    # the leaks found again, the genuine repeat leaks, the batch work orders and the tablet's sync day

    def at_survey(b, d):
        return [x for x in sorted(logd[b]) if x <= d][-1]
    tags = sorted(((cur.get(r["Battery"], r["Battery"]), r["Component"], at_survey(cur.get(r["Battery"], r["Battery"]),
                    G.as_date(r["Received"])), G.as_date(r["Closed"]), r["Status"], G.as_date(r["Received"]))
                   for r in p["ldar_tags"]), key=lambda x: x[:3])
    again, repeat = collections.Counter(), collections.Counter()
    for x, y in zip(tags[:-1], tags[1:]):
        if x[:2] != y[:2]:
            continue
        if x[3] is None or x[3] >= y[2]:
            if y[2].year == 2026:
                again[h1[x[0]]] += 1
        elif y[2].year == 2026:
            repeat[h1[x[0]]] += 1
    check("asks: leaks found again in 2026 on most routes (the filed rule has rows)", len(again) >= 10,
          str([again[r] for r in C.ROUTES]))
    check("asks: repaired points that leaked again on most routes", len(repeat) >= 10, str([repeat[r] for r in C.ROUTES]))
    shared = collections.Counter(r["Work order"] for r in p["ldar_tags"] if r["Work order"])
    check("asks: one work order closes several tags of distinct leaks",
          sum(1 for v in shared.values() if v > 1) >= 40, "%d work orders" % sum(1 for v in shared.values() if v > 1))
    synced = [t for t in tags if t[5] != t[2]]
    check("asks: only the 2026 second crew's tags reach the tracker after the survey day, always a Friday", all(
        crew[(t[0], t[2].isoformat())] == "ogi08" and t[5].weekday() == 4 for t in synced), "%d tags" % len(synced))
    words = " ".join(str(r["Note"]) + " " + str(r["Status"]) for r in p["ldar_tags"])
    check("asks: no tag's note or status says it was found before or leaked on", not re.search(
        r"again|re-?tag|previous|duplicate|earlier|repeat|same leak|sync|upload|re-?check|still", words, re.I))
    pt_word = {"stuffing box": ("packing", "stuffing"), "casing valve": ("valve", "bonnet", "packing")}
    odd = [r for r in p["ldar_tags"] if r["Status"] == "Closed" and any(k in r["Component"] for k in pt_word) and
           not any(w_ in r["Note"].lower() for k, ws in pt_word.items() if k in r["Component"] for w_ in ws)]
    check("realism: a repair's note fits its component", not odd, "%d odd" % len(odd))
    reps = [G.as_date(r["Closed"]) for r in p["ldar_tags"] if r["Closed"]] + [d for v in wos.values() for d in v]
    check("asks: no repair on the year's first day or at 1 July (a leak's days are never in doubt)",
          not any(d in (dt.date(2026, 1, 1), dt.date(2027, 1, 1), dt.date(2026, 7, 1)) for d in reps))
    check("asks: the leak files keep the battery's old code before its re-licensing", any(
        r["Battery"] == W.RENAMED[0] for r in p["ldar_surveys"]) and any(
        r["Battery"] == W.RENAMED[1] for r in p["ldar_surveys"]))
    pts = G.journal(p, g["opts"])
    nested = 0
    for code, seq in pts.items():
        st = None
        for t_, s_ in seq:
            nested += s_ == "ALARM" and st == "ALARM"
            st = s_
    check("realism: one tank pressure point is in one state at a time (no alarm inside an alarm)", nested == 0,
          "%d nested" % nested)

    # ---------------------------------------------------------------- realism sweep
    counts = collections.Counter(r["route"] for r in g["rows"])
    ties = collections.Counter(counts.values())
    check("realism: route event counts vary (at most one tied pair)", max(ties.values()) <= 2 and
          sum(1 for v in ties.values() if v > 1) <= 1, str(sorted(counts.values())))
    check("realism: no round headline total", abs(g["total"] * 10 - round(g["total"] * 10)) > 1e-9 or
          round(g["total"], 1) % 1 != 0)
    v = [figs["schedule_b.%s.%s_t" % (r, h)] for r in C.ROUTES for h in ("h1", "h2")]
    vv = [round(g["sched"][r][h], 3) for r in C.ROUTES for h in ("h1", "h2")]
    check("realism: no two route figures equal before rounding", len(vv) == len(set(vv)), str(sorted(v)))
    check("realism: no round Schedule B total", all(round(g["sched"]["field"][h] % 1, 1) not in (0.0, 1.0)
                                                    for h in ("h1", "h2")))
    ack = collections.Counter(r["Operator"] for r in PR.rows(PR.ALARMS) if r["Operator"])
    check("realism: control room acknowledgements follow the shifts, not an even split",
          max(ack.values()) / min(ack.values()) > 1.15, str(sorted(ack.values())))
    pm = collections.Counter(r["Battery"] for r in p["workorders"] if r["Description"] == "Monthly separator inspection")
    check("realism: monthly inspections are not twelve at every battery", len(set(pm.values())) >= 3,
          str(sorted(collections.Counter(pm.values()).items())))
    pack_text = ""
    for f in files:
        if f.endswith((".csv", ".txt", ".jsonl")):
            pack_text += open(os.path.join(TARGET, f), encoding="utf-8").read()
    check("realism: no em or en dash in the pack's text files", "—" not in pack_text and "–" not in pack_text)
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("realism: no em or en dash in submission.md", "—" not in sub and "–" not in sub)
    nv = collections.Counter(len(v) for v in G.visits(p, g["opts"]).values())
    check("realism: visit counts vary by battery", len(nv) > 40, "%d distinct counts" % len(nv))
    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def pooled_total(p, g):
    """one fit for every visit-found event, kinds unread"""
    win = g["windows"]
    w = np.array([x["w"] for x in win])
    y = np.array([1.0 if (x["kind"] and not (x["kind"] == "PV" and x["tel"])) else 0.0 for x in win])
    f = G.fit(y, w)
    rt = G.rates(p, g["opts"])
    s = 0.0
    for r in g["rows"]:
        if r["basis"] == "ALARM":
            s += r["kg"]
            continue
        h = float(G.expected_hours(f["p"], f["b"], np.array([r["arr"] - r["dep"]]))[0])
        s += G.methane(rt, r["bat"], r["arr"] - h, r["closed"])
    return s / 1000


def sf(p, g):
    rt = G.rates(p, g["opts"])
    base = g["total"]

    def alt(start_fn, only=None):
        s = 0.0
        for r in g["rows"]:
            if r["basis"] == "ALARM" or (only and not only(r)):
                s += r["kg"]
                continue
            s += G.methane(rt, r["bat"], start_fn(r), r["closed"])
        return s / 1000

    # SF1 found in 2026 by the find's UTC date
    nyear = sum(1 for r in g["rows"] if G.local_day(r["found"]).year != (dt.datetime(2025, 12, 15) +
                dt.timedelta(hours=r["found"])).year)
    check("SF1 found in 2026 by local or UTC date: same call", True, "%d events differ" % nyear)
    # SF2 the window from the previous arrival instead of its departure
    vis = G.visits(p, g["opts"])
    prev_arr = {}
    for b, vs in vis.items():
        for a, c in zip(vs[:-1], vs[1:]):
            prev_arr[(b, round(c[0], 6))] = a[0]
    fitsA = G.fits([dict(x, w=x["w"] + 0.4) for x in g["windows"]])

    def from_arrival(r):
        f = fitsA[r["kind"]]
        W_ = r["arr"] - prev_arr[(r["bat"], round(r["arr"], 6))]
        return r["arr"] - float(G.expected_hours(f["p"], f["b"], np.array([W_]))[0])
    t = alt(from_arrival)
    check("SF2 the window from the previous arrival: same call", G.band(t)[0] == "C", "%.2f t" % t)
    # SF3 the geofence re-entry threshold at 5 or 30 minutes: tested as no merge and as the golden (bounds)
    t = G.compute(p, merge_split=False)["total"]
    check("SF3 the re-entry threshold (no merge to ten minutes): same call", G.band(t)[0] == "C", "%.2f t" % t)
    # SF4 the alarm start at the last alarm of the burst
    pts = G.journal(p, g["opts"])
    reg, _ = G.codes(p)
    scada = {c: (r["former_battery"] or c) for c, r in reg.items()}
    s = 0.0
    for r in g["rows"]:
        if r["basis"] != "ALARM":
            s += r["kg"]
            continue
        seq = [x for x in pts.get(scada[r["bat"]], []) if x[0] < r["found"] and x[1] == "ALARM"]
        s += G.methane(rt, r["bat"], seq[-1][0], r["closed"])
    check("SF4 a stuck valve's start at the burst's last alarm: same call", G.band(s / 1000)[0] == "C",
          "%.2f t" % (s / 1000))
    # SF5 the expected start against the expected methane over the start's distribution
    s = 0.0
    for r in g["rows"]:
        if r["basis"] == "ALARM":
            s += r["kg"]
            continue
        f = g["fits"][r["kind"]]
        W_ = r["arr"] - r["dep"]
        Fw = f["p"] + (1 - f["p"]) * (1 - np.exp(-f["b"] * W_))
        pv = f["p"] / Fw
        kg_v = G.methane(rt, r["bat"], r["dep"], r["closed"])
        kg_u = G.methane(rt, r["bat"], r["dep"] + W_ / 2, r["closed"])
        s += pv * kg_v + (1 - pv) * kg_u
    check("SF5 expected methane over the start's spread, not at its mean: same call", G.band(s / 1000)[0] == "C",
          "%.2f t" % (s / 1000))
    # SF6 pilots fitted on every battery, relief valves on every battery
    t = sf_elig(p, g, rt)
    check("SF6 pilots and relief valves fitted on every battery: same call", G.band(t)[0] == "C", "%.2f t" % t)
    # SF7 hours anchored on the find rather than the arrival
    t = alt(lambda r: r["found"] - float(G.expected_hours(g["fits"][r["kind"]]["p"], g["fits"][r["kind"]]["b"],
                                                           np.array([r["arr"] - r["dep"]]))[0]))
    check("SF7 the start counted back from the find: same call", G.band(t)[0] == "C", "%.2f t" % t)
    # SF8 the rate of the day the event was found for every hour
    s = 0.0
    for r in g["rows"]:
        kgh = rt.get((r["bat"], G.local_day(r["found"])), 0.0)
        s += kgh * (r["closed"] - r["start"])
    check("SF8 every hour at the find day's rate: same call", G.band(s / 1000)[0] == "C", "%.2f t" % (s / 1000))
    # SF9 the analysis nearest the day rather than the latest on or before it
    t = sf_nearest(p, g)
    check("SF9 the nearest analysis instead of the latest before: same call", G.band(t)[0] == "C", "%.2f t" % t)
    # SF10 the windows of 2026 by departure date rather than arrival
    check("SF10 windows counted by arrival in 2026 (the finds' year): asserted in the golden", True)
    # SF11 the fit on the windows of the events' own kinds only
    check("SF11 events found in early January carry December windows: included by find date", all(
        G.local_day(r["found"]).year == 2026 for r in g["rows"]))


def sf_elig(p, g, rt):
    win = g["windows"]
    w = np.array([x["w"] for x in win])
    out = {}
    for k in ("TH", "CP", "PV"):
        y = np.array([1.0 if x["kind"] == k else 0.0 for x in win])
        out[k] = G.fit(y, w)
    s = 0.0
    for r in g["rows"]:
        if r["basis"] == "ALARM":
            s += r["kg"]
            continue
        f = out[r["kind"]]
        s += G.methane(rt, r["bat"], r["arr"] - float(G.expected_hours(f["p"], f["b"], np.array([r["arr"] - r["dep"]]))[0]),
                       r["closed"])
    return s / 1000


def sf_nearest(p, g):
    reg, cur = G.codes(p)
    an = collections.defaultdict(list)
    for r in p["vapour"]:
        d = r["Sampled"].date() if isinstance(r["Sampled"], dt.datetime) else r["Sampled"]
        an[cur.get(r["Battery"])].append((d, float(r["Flash GOR (m3/m3)"]), float(r["C1"])))
    rt = {}
    for r in p["production"]:
        b = cur.get(r["Battery"])
        d = dt.date.fromisoformat(r["ProdDate"])
        a = min(an[b], key=lambda x: abs((x[0] - d).days))
        rt[(b, d)] = float(r["OilVol_m3"]) * a[1] * a[2] / 100 * G.DENSITY / 24
    return sum(G.methane(rt, r["bat"], r["start"], r["closed"]) for r in g["rows"]) / 1000


if __name__ == "__main__":
    sys.exit(main())
