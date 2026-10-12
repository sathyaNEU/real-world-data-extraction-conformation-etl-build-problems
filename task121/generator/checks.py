"""Assertions on the built pack: the rungs and their margins, the fork grid, every semantic fork row (SF1 to SF15),
the clearances, the separation of the ask devices from the season's events, every ask stop and the cracker's and
the mirror's sheets, the realism sweep and the input gates."""
import collections
import csv
import datetime as dt
import math
import os
import re

import analysis as AN
import asks as AK
import core
import docs as D
import logic as L
import pack as P

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def margin(sc, order):
    a, b = sc[order[0]], sc[order[1]]
    return a / b if b > 0 else float("inf")


def ladder(F):
    O, E = F["count"]
    order, sc = L.pick(O, E, "count")
    ok(order[0] == "landfill" and margin(sc, order) >= 1.15, "R0: the landfill on counts, margin %.2f" % margin(sc, order))
    ok(order.index("compost") >= 2, "R0: the compost facility third or lower on counts")
    O1, E1 = F["all"]
    order1, sc1 = L.pick(O1, E1, "ratio")
    ok(order1[0] == "render" and margin(sc1, order1) >= 1.15, "R1: the rendering plant on the all-hours ratio")
    ok(sc1["compost"] < 1.0 and order1.index("compost") >= 3, "R1: the compost facility at or below one, near the foot")
    O3, E3 = F["same"]
    for metric in ("excess", "ratio"):
        o3, s3 = L.pick(O3, E3, metric)
        ok(o3[0] == "compost" and o3[1] == "render", "R3 %s: compost, then rendering" % metric)
        ok(margin(s3, o3) >= 1.5, "R3 %s margin %.2f" % (metric, margin(s3, o3)))
        need = 1.15 if metric == "ratio" else 2.0
        ok(s3[o3[1]] >= need * s3[o3[2]], "R3 %s: the rival clear of the third (%.2f against %.2f)"
           % (metric, s3[o3[1]], s3[o3[2]]))
    # R2: the description tally names the landfill
    d = F["desc"]
    ok(max(d, key=d.get) == "landfill" and d["landfill"] >= 1.5 * sorted(d.values())[-2], "R2: descriptions name the landfill")
    # every same-hours variant converges (SF11)
    for mode in ("same", "month", "pm1", "incl"):
        O, E = F[mode]
        for metric in ("excess", "ratio"):
            o, s = L.pick(O, E, metric)
            ok(o[:2] == ["compost", "render"] and s[o[0]] >= 1.3 * s[o[1]], "SF11 %s %s" % (mode, metric))


def fork_grid(F):
    met, held, evs = F["met"], F["held"], F["events"]
    hw = {"vector": F["hw"], "scalar": AN.hourly(met, held, "scalar")}
    cells = []
    for mode in ("count", "all", "same"):
        for center in (False, True):
            for convert in (True, False):
                for meth in ("vector", "scalar"):
                    O, E = L.compare(evs, hw[meth], mode, convert=convert, center=center)
                    metric = {"count": "count", "all": "ratio", "same": "excess"}[mode]
                    o, s = L.pick(O, E, metric)
                    cells.append((mode, center, convert, meth, o[0]))
                    if mode == "same":
                        ok(o[0] == "compost", "fork grid: same-hours cell %s" % str(cells[-1]))
                    else:
                        ok(o[0] in ("landfill", "render", "mush"), "fork grid: cell %s names %s" % (str(cells[-1][:4]), o[0]))
    ok(len(cells) == 24, "fork grid of 24 cells")
    return cells


def semantic_forks(F):
    met, held, evs, hw = F["met"], F["held"], F["events"], F["hw"]
    rows, ocs, poly = F["rows"], F["ocs"], F["poly"]
    O, E = F["count"]
    ok(L.pick(O, E, "count")[0][0] == "landfill", "SF1: counting upwind events names the landfill")
    ok("does not" in D.procedure_text() and "show which source did" in D.procedure_text(), "SF1: the procedure's caution")
    ok("not a finding of its source" in D.procedure_text(), "SF2: descriptions are not findings")
    # SF3: the season by received time gives the same call
    gold = F["gold_rows"]
    rr = [dict(household=r["household"], noticed=r["noticed_local"], lat=r["lat"], lon=r["lon"]) for r in gold
          if r["noticed_local"] is not None and core.SEASON0 <= r["received_t"].date() <= core.SEASON1]
    O3, E3 = L.compare(L.events(rr), hw, "same")
    ok(L.pick(O3, E3)[0][0] == "compost", "SF3: received-time season, same call")
    edge = [r for r in gold if r["noticed_local"] is not None and any(
        abs((r["noticed_local"] - x).total_seconds()) < 6 * 3600 for x in (dt.datetime(2026, 5, 1), dt.datetime(2026, 10, 1)))]
    ok(not edge, "SF3: no complaint within six hours of either season edge")
    # SF4: complaints instead of events
    cc = [dict(household=r["household"] + str(i), noticed=r["noticed_local"], lat=r["lat"], lon=r["lon"])
          for i, r in enumerate(gold) if r["noticed_local"] is not None and core.in_season(r["noticed_local"])]
    O4, E4 = L.compare(L.events(cc), hw, "same")
    ok(L.pick(O4, E4)[0][0] == "compost", "SF4: complaints counted one by one, same call")
    # SF5: the contact as the household
    c5 = [dict(household=r["contact_id"], noticed=r["noticed_local"], lat=r["lat"], lon=r["lon"]) for r in gold
          if r["noticed_local"] is not None and core.in_season(r["noticed_local"])]
    O5, E5 = L.compare(L.events(c5), hw, "same")
    ok(L.pick(O5, E5)[0][0] == "compost", "SF5: contact key, same call")
    # SF6 to SF10 and SF15
    for name, kw, h in (("SF6", dict(convert=False), hw), ("SF7", {}, AN.hourly(met, held, "scalar")),
                        ("SF10", dict(bearing=core.bearing_planar), hw), ("SF9", dict(deg=22.5), hw),
                        ("SF15", {}, AN.hourly(met, None))):
        O6, E6 = L.compare(evs, h, "same", **kw)
        ok(L.pick(O6, E6)[0][:2] == ["compost", "render"], "%s: same call and rival" % name)
    # SF8: calm hours given their vector direction
    hw8 = {k: (max(v[0], core.CALM_MS), v[1], v[2]) if v else None for k, v in hw.items()}
    O8, E8 = L.compare(evs, hw8, "same")
    ok(L.pick(O8, E8)[0][0] == "compost", "SF8: calms with a direction, same call")
    O10, _ = L.compare(evs, hw, "count", bearing=core.bearing_planar)
    ok(O10 == F["O"], "SF10: planar bearings give the same counts")
    # SF5b: the household as the address string, its upper case, or the geocode; the window's edge either way
    def ev_by(keyf, strict=False):
        rr = [dict(household=keyf(r), noticed=r["noticed_local"], lat=r["lat"], lon=r["lon"]) for r in gold
              if r["noticed_local"] is not None and core.in_season(r["noticed_local"])]
        if strict:
            save = core.EVENT_WINDOW
            core.EVENT_WINDOW = save - dt.timedelta(microseconds=1)
            out = L.events(rr)
            core.EVENT_WINDOW = save
            return out
        return L.events(rr)
    for nm, kf, st in (("raw", lambda r: r["address"], False), ("upper", lambda r: r["address"].upper().strip(), False),
                       ("geocode", lambda r: (round(r["lat"], 6), round(r["lon"], 6)), False),
                       ("strict window", lambda r: r["household"], True)):
        e5 = ev_by(kf, st)
        ok(len(e5) == F["n_events"] and L.compare(e5, hw, "count")[0] == F["O"], "SF5b %s: the same events" % nm)
    # SF12: the rival on the call's footing
    ok(F["rival"] == "render", "SF12: the closest rival is the rendering plant")
    # SF13: five facilities in the list
    ok(len(core.FKEYS) == 5, "SF13: five permitted sources")
    # SF14: the airport is not the record: the procedure says so
    ok("airport" in D.procedure_text() and "not used for the" in D.procedure_text(), "SF14: the procedure excludes the airport")
    # SF15: held-vane hours give no source upwind either way at the events
    hw_raw = AN.hourly(met, None)
    for e in evs:
        d, h = L.event_hour(e)
        if (d, h) in held:
            a, b = hw.get((d, h)), hw_raw.get((d, h))
            ok((a is None or a[0] < core.CALM_MS) and (b is None or b[0] < core.CALM_MS), "SF15 event in a held hour")


def clearances(F):
    for e in F["events"]:
        d, h = L.event_hour(e)
        w = F["hw"].get((d, h))
        if w is None:
            continue
        ok(abs(w[0] - core.CALM_MS) >= 0.03, "calm clearance at %s" % ((d, h),))
        if w[0] < core.CALM_MS:
            continue
        for f in core.FKEYS:
            for bf in (core.bearing_deg, core.bearing_planar):
                b = bf(e["lat"], e["lon"], core.FAC[f]["lat"], core.FAC[f]["lon"])
                ok(abs(core.angdiff(w[1], b) - 30.0) >= 0.25 and abs(core.angdiff(w[1], b) - 22.5) >= 0.25,
                   "edge clearance %s %s" % ((d, h), f))
    for (d, h) in [(dt.date(2026, 4, 30), 23), (dt.date(2026, 5, 31), 23), (dt.date(2026, 6, 30), 23),
                   (dt.date(2026, 7, 31), 23), (dt.date(2026, 8, 31), 23), (dt.date(2026, 9, 30), 23)]:
        w = F["hw"].get((d, h))
        ok(w is not None and w[0] >= core.CALM_MS, "month-opening hour %s usable and not calm" % d)


def separation(F):
    """The ask devices put no row into the season's events: the events are the same with the app resends, the
    January carry-over, the app's UTC rows and the routed calls handled or not."""
    rows, ocs, poly = F["rows"], F["ocs"], F["poly"]
    base = [(e["household"], e["noticed"]) for e in F["events"]]
    for kw in (dict(resends=False), dict(utc=False), dict(imported=False), dict(district=False), dict(key="household"),
               dict(key="contact")):
        ev = AN.season_events(AN.clean(rows, ocs, poly, **kw))
        ok([(e["household"], e["noticed"]) for e in ev] == base, "separation: season events unchanged under %s" % kw)
    imp = [r for r in rows if r["received_t"].date() == dt.date(2026, 1, 6)]
    ok(len(imp) >= 38, "the carry-over is in the export")
    ok(all(not core.in_season(r["noticed_t"]) for r in rows if r["channel"] == "App" and r["noticed_t"] > r["received_t"]),
       "no UTC app row reads into the season")


def asks(F):
    gold_a, stops_a = AK.ask_a(F)
    ok(gold_a == F["months"], "ask A golden")
    ok(len(set(gold_a)) == 9, "ask A: no two months alike")
    for k, v in stops_a.items():
        ok(v != gold_a, "ask A stop differs: %s" % k)
    gold_c, stops_c = AK.ask_c(F)
    ok(gold_c == (F["usable"], F["calm"]), "ask C golden")
    ok(len(set(gold_c[0])) == 5 and len(set(gold_c[1])) == 5, "ask C: no two months alike")
    ok(stops_c["standard-time months"] == gold_c, "ask C: local and standard-time months converge")
    ok(stops_c["held-vane records read as wind (the V flag trusted)"][0] != gold_c[0], "ask C: held-vane stop moves usable")
    cr = AK.cracker(F)
    gold = dict(A=gold_a, C_usable=gold_c[0], C_calm=gold_c[1])
    kept = AK.kept(gold, cr)
    ok(all(v == 0 for v in kept.values()), "cracker misses every ask cell: %s" % kept)
    strong = AK.months_contact_dedup(F["rows"], F["poly"])
    hits = sum(int(a == b) for a, b in zip(strong, gold_a))
    ok(hits <= 1, "the stronger battery keeps at most one month (%d)" % hits)
    for k in ("one report once by household and time noticed, carry-over and UTC handled",
              "one report once by contact and time noticed, carry-over and UTC handled"):
        h = sum(int(a == b) for a, b in zip(stops_a[k], gold_a))
        ok(h == 0, "%s: misses every month (%d kept)" % (k, h))
    return gold, cr, kept, hits


def devices(F):
    """The ask devices as the records carry them: every month has a re-registered resend and a household whose two
    people gave the same time, both inside the district; a resend's text is a strict prefix of the report it
    repeats; two people's reports never contain each other's words; nothing else shares a household and a time."""
    gold = F["gold_rows"]
    allin = [r for r in AN.clean(F["rows"], F["ocs"], F["poly"], resends=False) if r["noticed_local"] is not None]
    groups = collections.defaultdict(list)
    for r in allin:
        groups[(r["household"], r["noticed"])].append(r)
    rereg, same = collections.Counter(), collections.Counter()
    for k, g in groups.items():
        if len(g) < 2:
            continue
        g = sorted(g, key=lambda r: (r["received_t"], r["complaint_no"]))
        first = g[0]["description"].strip().lower()
        for r in g[1:]:
            t = r["description"].strip().lower()
            if t in first:
                ok(len(t) < len(first) and first.startswith(t), "resend %s: a strict prefix" % r["complaint_no"])
                ok(r["channel"] == "App" and g[0]["channel"] == "App", "resends come from the app")
                if r["contact_id"] != g[0]["contact_id"]:
                    rereg[r["noticed_local"].month] += 1
            else:
                ok(all(t not in x["description"].strip().lower() and x["description"].strip().lower() not in t
                       for x in g if x is not r), "two people's words apart at %s" % r["complaint_no"])
                same[r["noticed_local"].month] += 1
    for m in range(1, 10):
        ok(rereg[m] >= 1, "month %d has a resend under a new app registration" % m)
        ok(same[m] >= 1, "month %d has two people in one household giving the same time" % m)
    # a re-registered app keeps its new registration
    regs = [r for r in F["rows"] if r["channel"] == "App"]
    later = collections.Counter(r["contact_id"] for r in regs)
    ok(sum(1 for c, n in later.items() if n >= 2) >= 20, "app registrations used more than once")
    return rereg, same


def realism(F, target):
    ok(len(set(F["O"].values())) == 5, "facility counts all differ")
    ok(F["n_events"] % 10 != 0, "season events not a round count")
    txt = D.procedure_text() + D.README + D.FIELDS
    for name in re.findall(r"\b(Erica Schmitt|Alyssa White|Jerome Reed|Roy Heath)\b", txt):
        ok(name in ("Erica Schmitt", "Alyssa White", "Jerome Reed", "Roy Heath"), "personas from the card")
    for f in os.listdir(target):
        if f.endswith((".csv", ".txt", ".geojson")):
            s = open(os.path.join(target, f), encoding="utf-8").read()
            ok("\u2014" not in s and "\u2013" not in s, "no em or en dash in %s" % f)
    ok("\u2014" not in txt and "\u2013" not in txt, "no dash in documents")
    with open(os.path.join(target, P.FILES["complaints"]), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    last = max(dt.datetime.strptime(r["received"], "%Y-%m-%d %H:%M") for r in rows)
    ok(last <= core.EXPORT, "nothing in the export after the export")
    descs = collections.Counter(r["description"] for r in rows)
    ok(max(descs.values()) / len(rows) < 0.03, "no description dominates the log (%d)" % max(descs.values()))
    ok(len(descs) >= 0.6 * len(rows), "descriptions mostly the complainant's own (%d of %d)" % (len(descs), len(rows)))
    ok(len({r["contact_id"] for r in rows}) > 200, "many contacts")
    per = collections.Counter(r["contact_id"] for r in rows)
    mid = sum(1 for n in per.values() if 3 <= n <= 25)
    ok(mid >= 5, "contacts between the one-off and the nightly (%d)" % mid)
    pre = collections.Counter(c[:4] for c in per)
    ok(max(pre.values()) / len(per) < 0.9 and len(pre) <= 4, "contact numbers run in one sequence")
    # the maintenance log: no audit while the monitor was out, every audit says the vane was held
    with open(os.path.join(target, P.FILES["maint"]), encoding="utf-8") as f:
        mrows = list(csv.DictReader(f))
    for r in mrows:
        if r["work"].lower().startswith("monthly"):
            ok("held" in r["work"].lower(), "audit wording names the held vane")
            day = dt.date.fromisoformat(r["date"])
            ok(not (dt.date(2026, 6, 9) <= day <= dt.date(2026, 6, 11)), "no audit while the monitor was out")
    # the boundary: no complaint within 50 m of the line
    poly = F["poly"]
    for r in rows:
        lat, lon = float(r["latitude"]), float(r["longitude"])
        dmin = min(_seg_km(lat, lon, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))
        ok(dmin >= 0.05, "complaint %s %.3f km from the boundary" % (r["complaint_no"], dmin))


def _seg_km(lat, lon, a, b):
    kx = 111.0 * math.cos(math.radians(lat))
    px, py = (lon - a[1]) * kx, (lat - a[0]) * 111.0
    bx, by = (b[1] - a[1]) * kx, (b[0] - a[0]) * 111.0
    t = max(0.0, min(1.0, (px * bx + py * by) / (bx * bx + by * by)))
    return math.hypot(px - t * bx, py - t * by)


def bins(F):
    """The figures the write-up quotes sit clear of their rounding edges."""
    for f in core.FKEYS:
        for v in (F["E"][f], F["excess"][f], F["ratio"][f]):
            ok(abs((v * 10) % 1 - 0.5) >= 0.08, "%s %.4f clear of its one-decimal edge" % (f, v))
    for f in ("compost", "render"):
        v = F["all"][0][f] / F["all"][1][f]
        ok(abs((v * 100) % 1 - 0.5) >= 0.08, "%s all-hours ratio %.4f clear of its edge" % (f, v))


def gates(target, meta):
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a file of 25,000 rows")
    ok(len(meta["distractor_files"]) >= 2, "two or more distractors")
    for f in files:
        ok("distractor" not in f.lower() and "answer" not in f.lower(), "no tell in file names")


def run(F, target, meta):
    N[0] = 0
    ladder(F)
    cells = fork_grid(F)
    semantic_forks(F)
    clearances(F)
    separation(F)
    gold, cr, kept, hits = asks(F)
    devices(F)
    bins(F)
    realism(F, target)
    gates(target, meta)
    return N[0], cells, gold, cr, kept, hits
