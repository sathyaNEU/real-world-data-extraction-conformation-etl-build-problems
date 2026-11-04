"""task489 generator checks: the three rules on the clean truth, the ladder, the slug regimes, every semantic fork
row asserted over its readings, bin clearance, the asks' careful route, the separation line, the input gates and the
realism sweep. run() prints one line per assertion and returns True when every one passes."""
import csv
import datetime as dt
import json
import math
import os
import re

import numpy as np

import sim as S
import world as W

D = dt.timedelta
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    return bool(cond)


def edge(v, u):
    return u / 2.0 - abs(v - round(v / u) * u)


# ------------------------------------------------------------------------------------------------ golden variants
def variant(wd, window="prod", per_cycle="maker", x="2026", scf=W.SCF_TO_M3, auto="counter", dedup=True,
            attrib="true", slug="daily", start=0.0, cmp="ge", day_by="open"):
    """Each pad's intermittent-vent methane (t) with one convention changed; every other part as the golden."""
    camp = wd["survey"]["lcs"]
    survey_pc = {}
    for m in W.LC_MODELS:
        rows = [c for c in camp if c["model"] == m and c["cycles"] > 0]
        survey_pc[m] = sum(c["scf"] for c in rows) / sum(c["cycles"] for c in rows)
    if window == "prod":
        w0, w1 = W.WINDOW_START_UTC, W.WINDOW_END_UTC
    elif window == "cal":
        w0 = dt.datetime(2026, 1, 1, tzinfo=W.TZ).astimezone(W.UTC)
        w1 = dt.datetime(2027, 1, 1, tzinfo=W.TZ).astimezone(W.UTC)
    else:
        w0, w1 = dt.datetime(2026, 1, 1, tzinfo=W.UTC), dt.datetime(2027, 1, 1, tzinfo=W.UTC)
    label_uwi = {w["name"]: w["uwi"] for w in wd["wells"]}
    out = {}
    for s in wd["sites"]:
        xx = {"2026": s["x2026"], "2025": s["x2025"], "mean": (s["x2026"] + s["x2025"]) / 2.0}[x]
        tot = 0.0
        for sep in s["seps"]:
            pc = W.LC_MODELS[sep["model"]]["scf_per_cycle"] if per_cycle == "maker" else survey_pc[sep["model"]]
            kgc = pc * scf * xx * W.CH4_KG_PER_M3
            p = wd["prod"][sep["uwi"]]
            liq = p["cond"] + p["water"]
            if sep["auto"] and auto == "counter":
                rows = wd["counters"][sep["uwi"]]
                inside = [v for t, v in rows if w0 <= t <= w1]
                n = sum((b - a) % 65536 for a, b in zip(inside, inside[1:]))
            elif sep["group"] == "F" or (sep["auto"] and auto == "volume"):
                n = float(liq.sum()) / sep["band"]
            else:
                cyc = [c for c in wd["cycles"] if (dedup is False or not c["resent"])
                       and ((attrib == "true" and c["uwi"] == sep["uwi"]) or
                            (attrib == "label" and label_uwi.get(c["label"]) == sep["uwi"]))
                       and c["result"] == "ARRIVE" and w0 <= c["open_utc"] < w1]
                by = {}
                for c in cyc:
                    t = c["open_utc"] + (D(seconds=c["travel_s"]) if day_by == "arrival" else D(0))
                    day = S.local_naive(t - D(hours=W.PROD_DAY_HOUR)).date()
                    by[day] = by.get(day, 0) + 1
                lvl, n = start * sep["band"], 0
                if slug == "annual":
                    a_tot = sum(by.values())
                    s_ann = float(liq.sum()) / a_tot if a_tot else 0.0
                for d, day in enumerate(W.DAYS):
                    a = by.get(day, 0)
                    if a == 0:
                        continue
                    sl = s_ann if slug == "annual" else float(liq[d]) / a
                    for _ in range(a):
                        lvl += sl
                        if (lvl >= sep["band"] - 1e-12) if cmp == "ge" else (lvl > sep["band"] + 1e-12):
                            n += 1
                            lvl = 0.0
            tot += n * kgc
        out[s["code"]] = tot / 1000.0
    return out


def set_of(t):
    return sorted(c for c, v in t.items() if v > W.LINE_T)


def spread_set(wd, tr):
    """SF16's ruled-out reading: each cycle's liquid reaching the separator over the afterflow instead of with the
    plunger, drained by a mid-range 1 in valve (4 m3/h)."""
    import physics as PH
    ev = PH.events(wd)
    gkg = {row["sep"]["lc_tag"]: row["kg"]["golden"] for row in tr["lc"]}
    pads = {}
    c = 4.0 / 3600.0
    for sp in wd["seps"]:
        kg = gkg[sp["lc_tag"]]
        if sp["group"] != "F":
            lvl, is_open, n, top, t = 0.0, False, 0, 0.0, None
            for ta, q, v, af in ev[sp["uwi"]]:
                af = max(af, 60.0)
                if t is not None and ta > t:
                    lvl, is_open, m, top = PH._phase(lvl, is_open, 0.0, ta - t, sp["band"], c, top)
                    n += m
                lvl, is_open, m, top = PH._phase(lvl, is_open, q / af, af, sp["band"], c, top)
                n += m
                t = ta + af
            kg = n * sp["kpc"]
        pads[sp["site"]] = pads.get(sp["site"], 0.0) + kg / 1000.0
    return set_of(pads)


# ------------------------------------------------------------------------------------------------ the run
def run(target, golden, wd=None, n=None, g=None, meta_path=None, fig_path=None):
    RESULTS.clear()
    wd = wd or S.simulate()
    tr = g["tr"] if g else S.truth(wd)
    gold = tr["sets"]["golden"]
    st = tr["site_t"]
    names = {s["code"]: s["name"] for s in wd["sites"]}

    # R1 the field's raw material ships, the deciding quantity does not
    with open(os.path.join(target, W.FILES["cycles"])) as f:
        head = f.readline().strip().split(",")
    ok("R1 the cycle history ships each cycle with its result, counters and times (the slugs' raw material)",
       {"cycle_count", "arrival_count", "valve_open_local", "result"} <= set(head), str(head))
    allheads = []
    for fn in os.listdir(target):
        if fn.endswith(".csv"):
            with open(os.path.join(target, fn)) as f:
                allheads += f.readline().lower().strip().split(",")
    ok("R1 no shipped column holds a dump count, a slug or a band for an unautomated separator",
       not any(re.search(r"slug|band|dumps?_(?:est|count)|cycles_per", h) for h in allheads), "")
    # R3a the analyst test: the field's volume-over-band count (counters where fitted) files a wrong set
    ok("R3a the volume-over-band route files a wrong set on the clean truth", tr["sets"]["r1"] != gold,
       "%s against %s" % (tr["sets"]["r1"], gold))
    ok("R3a the arrival route files a wrong set on the clean truth", tr["sets"]["label"] != gold, str(tr["sets"]["label"]))
    ok("R3a the survey-rate route files a wrong set", tr["sets"]["ef"] != gold, str(len(tr["sets"]["ef"])))
    ok("R3a condensate-only route files a wrong set", tr["sets"]["cond_only"] != gold, str(tr["sets"]["cond_only"]))
    # R3b the decisive step alone: the volume route with only slug-against-band changed lands the golden
    ok("R3b min(arrivals, liquid over band) per day files the golden set", tr["sets"]["min_rule"] == gold, "")
    ok("R3b arrivals over ceil(band / slug) per day files the golden set", tr["sets"]["ceil_rule"] == gold, "")
    ok("R3b volume over band for the small-slug wells with one dump per arrival for the big-slug wells files the golden",
       tr["sets"]["ps_volume"] == gold, "")
    # R2 every Layer 1 item is real and neutral: the golden method with each item mishandled keeps the call
    r2 = {
        "R2 the host's local clock: cycles and counters taken by local calendar day": variant(wd, window="cal"),
        "R2 the host's local clock read as UTC calendar days": variant(wd, window="utc"),
        "R2 outage re-sends: every row the host loaded counted": variant(wd, dedup=False),
        "R2 moved controller units read under the host's lagging label": variant(wd, attrib="label"),
        "R2 the makers' scf at 60 F converted at 0.0283168 m3": variant(wd, scf=0.0283168),
        "R2 the 2025 analysis taken for the 2026 one": variant(wd, x="2025"),
    }
    for k, t in r2.items():
        ok(k + ": same call", set_of(t) == gold, str(set_of(t)))
    # the 16-bit dump counter: every natural reading of the wrap gives the same call
    ctr = {}
    for sep in wd["seps"]:
        if not sep["auto"]:
            continue
        rows = wd["counters"][sep["uwi"]]
        inside = [v for t, v in rows if W.WINDOW_START_UTC <= t <= W.WINDOW_END_UTC]
        incs = [b - a for a, b in zip(inside, inside[1:])]
        ctr[sep["uwi"]] = {"golden": sum(i % 65536 for i in incs), "mod": (inside[-1] - inside[0]) % 65536,
                           "drop_wrap_hour": sum(i for i in incs if i >= 0), "raw": inside[-1] - inside[0],
                           "wrapped": any(i < 0 for i in incs)}
    ok("R2 counter wrap: no automated separator passes 65,536 dumps in the year",
       all(v["golden"] < 65536 for v in ctr.values()), str(max(v["golden"] for v in ctr.values())))
    ok("R2 counter wrap: the raw year difference is negative on every wrapped counter (an impossible count)",
       all((v["raw"] < 0) == v["wrapped"] for v in ctr.values()), "")
    for mode in ("mod", "drop_wrap_hour"):
        tot = {}
        for row in tr["lc"]:
            sep = row["sep"]
            nd = ctr[sep["uwi"]][mode] if sep["auto"] else row["dumps"]["golden"]
            tot[sep["site"]] = tot.get(sep["site"], 0.0) + nd * sep["kpc"] / 1000.0
        ok("R2 counter wrap read as %s: same call" % mode, set_of(tot) == gold, str(set_of(tot)))
    labels = {c["label"] for c in wd["cycles"]}
    import pack as P0
    tags = [P0.counter_tag(sp) for sp in wd["seps"] if sp["auto"]]
    ok("R2 keys resolve exactly: every host label is a register well name, every counter tag one vessel",
       labels <= {w["name"] for w in wd["wells"]} and len(set(tags)) == len(tags), "")
    ok("R2 the November repeated hour falls inside one production day (the day turns at 08:00)",
       W.PROD_DAY_HOUR > 2, "")
    ok("R2 renumbered, replaced and relocated devices are bleed devices only (they move ask B, never the call)",
       all(b["kind"] in ("PC", "TC") for b in wd["bleeds"]), "")
    ok("R2 the volumetric adjustment journal posts gas only (no liquid the call reads moves)",
       all(p["product"] == "GAS" for p in wd["ppa"]), "")
    # R3c no plant: no memo, draft, briefing or stakeholder figure ships, and no copied block in the allocations
    flist = sorted(os.listdir(target))
    ok("R3c no plant: no memo, draft, briefing, email or minutes in the pack",
       not any(re.search(r"memo|draft|brief|email|minutes|note", f, re.I) for f in flist), str(flist))
    blocks = set()
    dup = False
    for sp in wd["seps"]:
        lq = np.round(wd["prod"][sp["uwi"]]["cond"] + wd["prod"][sp["uwi"]]["water"], 1)
        for i in range(0, 365 - 14, 7):
            b = tuple(lq[i:i + 14])
            if len(set(b)) >= 5 and b in blocks:
                dup = True
            blocks.add(b)
    ok("R3c no plant: no 14-day block of liquid repeats across wells or weeks", not dup, "")
    # physics: the makers' control logic run on the shipped inflow, over the plausible box, files the golden
    import physics as PH
    sw = PH.sweep(wd, tr)
    grp = {sp["lc_tag"]: sp["group"] for sp in wd["seps"]}
    kpc = {sp["lc_tag"]: sp["kpc"] for sp in wd["seps"]}
    gkg = {row["sep"]["lc_tag"]: row["kg"]["golden"] for row in tr["lc"]}
    ok("physics: the sheets' logic on the shipped inflow files the 8 pads in every corner (SF17 drain 1.5 to 7 m3/h "
       "for a 1 in valve and 3 to 25 for 2 in, slug speed 0.6 to 1.6 of the trip's average; SF18 afterflow liquid 0 "
       "to 15 per cent; SF19 effective band 0.9 to 1.1)", all(r["set"] == gold for r in sw) and len(sw) == 24,
       str([(r["band"], r["drain"], r["speed"], r["af_share"]) for r in sw if r["set"] != gold][:3]))
    ok("physics: every big-slug controller opens once per arrival in every corner",
       all(v["n"] == round(gkg[t] / kpc[t]) for r in sw for t, v in r["lc"].items() if grp[t] == "PB"), "")
    worst = max(abs(v["kg"] - gkg[t]) for r in sw if r["band"] == 1.0 for t, v in r["lc"].items())
    ok("physics: every plunger controller's kilograms keep their bin in every corner at the register's band",
       all(round(v["kg"]) == round(gkg[t]) for r in sw if r["band"] == 1.0 for t, v in r["lc"].items()),
       "worst shift %.3f kg" % worst)
    marg = PH.slug_rate_margin(wd)
    ok("physics: every big-slug separator's slug comes off the tubing faster than its dump valve can drain, at the "
       "slowest arrival and the fastest valve (1.25 times or more)", min(a / b for a, b in marg.values()) >= 1.25,
       "%.2f" % min(a / b for a, b in marg.values()))
    tops = {}
    for r in sw:
        for t, v in r["lc"].items():
            tops[t] = max(tops.get(t, 0.0), v["top"])
    rooms = {sp["lc_tag"]: PH.vessel_room(sp) for sp in wd["seps"]}
    ok("physics: every vessel holds its highest level below the high level shutdown in every corner",
       all(tops[t] < rooms[t] for t in tops), "%.3f m3" % min(rooms[t] - tops[t] for t in tops))
    overlaps = 0
    by_w = {}
    for c in wd["cycles"]:
        if not c["resent"]:
            by_w.setdefault(c["uwi"], []).append(c)
    for cs in by_w.values():
        cs.sort(key=lambda c: c["open_utc"])
        for a, b in zip(cs, cs[1:]):
            if (b["open_utc"] - a["open_utc"]).total_seconds() < (a["travel_s"] or 0) + a["afterflow_min"] * 60:
                overlaps += 1
    ok("physics: each plunger cycle's travel and afterflow end before the next opening", overlaps == 0, str(overlaps))
    flowing = {sp["lc_tag"] for sp in wd["seps"] if sp["group"] == "F"}
    for scale in (0.98, 1.02):
        t_sc = {}
        for row in tr["lc"]:
            sp = row["sep"]
            t_sc[sp["site"]] = t_sc.get(sp["site"], 0.0) + row["kg"]["golden"] * (scale if sp["lc_tag"] in flowing else 1.0) / 1000.0
        ok("physics: the call holds with every flowing controller at %.2f of liquid over band (the five counters bound "
           "the drain-time effect)" % scale, set_of(t_sc) == gold, str(set_of(t_sc)))
    for b in PH.BAND_SCALE:
        r1b, lab = {}, {}
        for row in tr["lc"]:
            sp = row["sep"]
            dr = row["dumps"]
            vol = dr.get("counter", dr["volume"] / b)
            r1b[sp["site"]] = r1b.get(sp["site"], 0.0) + vol * sp["kpc"] / 1000.0
            arr = dr["arrivals"] if dr["arrivals"] is not None else vol
            lab[sp["site"]] = lab.get(sp["site"], 0.0) + arr * sp["kpc"] / 1000.0
        ok("physics: at %.1f of the band neither liquid over band nor one dump per arrival files the golden" % b,
           set_of(r1b) != gold and set_of(lab) != gold, "%d / %d" % (len(set_of(r1b)), len(set_of(lab))))
    ok("SF16 the liquid comes to surface with the plunger (PCX-300 specification); spread over the afterflow it would "
       "file another set, a reading the specification's operation paragraph rules out",
       spread_set(wd, tr) != gold, "")
    # ladder: who each wrong route adds, and the margins
    big = set(tr["sets"]["r1"]) - set(gold)
    dry = set(tr["sets"]["label"]) - set(gold)
    ok("ladder: the volume route adds three pads and drops none", len(big) == 3 and set(gold) <= set(tr["sets"]["r1"]),
       str(sorted(big)))
    ok("ladder: the arrival route adds three other pads and drops none", len(dry) == 3 and not (dry & big)
       and set(gold) <= set(tr["sets"]["label"]), str(sorted(dry)))
    ok("ladder: the big-slug pads carry plunger wells whose slugs exceed the band, the dry pads plunger wells far under it",
       all(any(sp["group"] == "PB" for sp in next(s for s in wd["sites"] if s["code"] == c)["seps"]) for c in big)
       and all(any(sp["group"] == "PS" for sp in next(s for s in wd["sites"] if s["code"] == c)["seps"]) for c in dry), "")
    lo_in = min(st[c]["golden"] for c in gold)
    hi_out = max(v["golden"] for c, v in st.items() if c not in gold)
    ok("margin: every pad in the conversion vents 0.62 t or more (kept from the first cut)", lo_in >= 0.62, "%.3f" % lo_in)
    ok("margin: every pad out vents 0.412 t or less (kept from the first cut)", hi_out <= 0.4125, "%.4f" % hi_out)
    ok("margin: each big-slug pad sits 0.55 t or more under the volume route", min(st[c]["r1"] for c in big) >= 0.55,
       "%.3f" % min(st[c]["r1"] for c in big))
    ok("margin: each dry pad sits 0.60 t or more under the arrival route", min(st[c]["label"] for c in dry) >= 0.60,
       "%.3f" % min(st[c]["label"] for c in dry))
    ok("dominance: the decisive step moves each flipped pad by 1.4x or more",
       all(st[c]["r1"] / st[c]["golden"] >= 1.4 for c in big) and all(st[c]["label"] / st[c]["golden"] >= 1.4 for c in dry), "")
    ok("ladder: the survey-rate route drops golden pads (it reads device-hours, not cycles)",
       bool(set(gold) - set(tr["sets"]["ef"])), str(sorted(set(gold) - set(tr["sets"]["ef"]))))
    # slug regimes on the shipped volumes
    worst_pb, worst_ps = 9.0, 0.0
    for sep in wd["seps"]:
        if sep["group"] == "F":
            continue
        p = wd["prod"][sep["uwi"]]
        a = wd["plan"][sep["uwi"]]["arrivals"]
        for d in range(365):
            if a[d] > 0 and (p["cond"][d] + p["water"][d]) > 0:
                r = (p["cond"][d] + p["water"][d]) / a[d] / sep["band"]
                if sep["group"] == "PB":
                    worst_pb = min(worst_pb, r)
                else:
                    worst_ps = max(worst_ps, r)
    ok("regime: every big-slug well's slug is 1.5 bands or more on every producing day", worst_pb >= 1.5 - 1e-9, "%.3f" % worst_pb)
    ok("regime: every small-slug well's slug is under 0.07 of a band on every producing day", worst_ps < 0.07, "%.4f" % worst_ps)
    # no column partitions the decisive property: plunger type, vessel bore and controller model all mix big and small slugs
    for attr, f in (("plunger type", lambda sp, w: w["plunger"]), ("bore", lambda sp, w: sp["bore"]),
                    ("controller span", lambda sp, w: sp["span"]), ("controller model", lambda sp, w: sp["model"]),
                    ("dump valve", lambda sp, w: sp["valve"]), ("tubing", lambda sp, w: w["tubing"])):
        pb = {f(sp, w) for sp, w in zip(wd["seps"], wd["wells"]) if sp["group"] == "PB"}
        ps = {f(sp, w) for sp, w in zip(wd["seps"], wd["wells"]) if sp["group"] == "PS"}
        ok("no partition: %s takes values shared by big-slug and small-slug wells" % attr, bool(pb & ps),
           "%s / %s" % (sorted(map(str, pb)), sorted(map(str, ps))))
    area = {s["code"]: s["area"] for s in wd["sites"]}
    ok("no partition: the conversion pads and each wrong route's added pads span both areas",
       len({area[c] for c in gold}) == 2 and len({area[c] for c in big | dry}) == 2 and
       len({area[c] for c in big}) == 2 and len({area[c] for c in dry}) == 2, "")
    # the semantic fork table, each row's readings
    forks = {
        "SF3 production days against local calendar days": variant(wd, window="cal"),
        "SF3 production days against UTC calendar days": variant(wd, window="utc"),
        "SF4 the maker's gas per cycle against the survey's measured per cycle": variant(wd, per_cycle="survey"),
        "SF5 the 2026 analysis against the 2025 analysis": variant(wd, x="2025"),
        "SF5 the 2026 analysis against the mean of both": variant(wd, x="mean"),
        "SF6 0.02826 m3 per scf against 0.0283168": variant(wd, scf=0.0283168),
        "SF7 counted cycles against liquid over band on the automated separators": variant(wd, auto="volume"),
        "SF8 each cycle once against every row the host loaded": variant(wd, dedup=False),
        "SF9 moved controllers on their wells against the host's labels": variant(wd, attrib="label"),
        "SF10 each day's slug against the year's mean slug": variant(wd, slug="annual"),
        "SF11 the level empty at the year's start against full": variant(wd, start=0.999),
        "SF13 a dump at the upper setting against only above it": variant(wd, cmp="gt"),
        "SF14 arrivals dated by valve open against by arrival": variant(wd, day_by="arrival"),
    }
    for k, t in forks.items():
        ok(k + ": same call", set_of(t) == gold, str(set_of(t)))
    ok("SF2 more than 0.5 t against 0.5 t or more: no pad within 0.05 t of the line",
       min(abs(v["golden"] - W.LINE_T) for v in st.values()) >= 0.05, "")
    ok("SF1 pads are the register's pads, one reporting facility each: same call",
       len({s["code"] for s in wd["sites"]}) == len(wd["sites"]), "")
    ok("SF12 two-phase separators dump condensate and water together; condensate alone is a wrong reading (rung)",
       tr["sets"]["cond_only"] != gold, "")
    ok("SF15 the intermittent-vent population is the register's level controllers only",
       all(sp["lc_tag"].startswith("LC-") for sp in wd["seps"]), "")
    # bins: every graded figure clear of its rounding edge under the decisive step's alternative executions
    worst = 9.0
    for row in tr["lc"]:
        vals = [row["kg"][k] for k in ("golden", "min_rule", "ceil_rule", "ps_volume")]
        if len({round(v) for v in vals}) > 1:
            worst = -1.0
        worst = min(worst, edge(row["kg"]["golden"], 1.0))
    ok("bins: every controller's kg keeps its whole-kg bin under every execution, 0.1 kg or more from an edge",
       worst >= 0.1, "%.3f" % worst)
    worst = 9.0
    for c, v in st.items():
        vals = [v[k] for k in ("golden", "min_rule", "ceil_rule", "ps_volume")]
        if len({round(x, 2) for x in vals}) > 1:
            worst = -1.0
        worst = min(worst, edge(v["golden"], 0.01))
    ok("bins: every pad's tonnes keeps its two-decimal bin, 0.001 t or more from an edge", worst >= 0.001, "%.5f" % worst)
    bt = S.bleed_truth(wd)
    bma = S.bleed_by_maker_area(bt, wd)
    ok("bins: every maker-area bleed total 0.1 kg or more from a whole-kg edge", min(edge(v, 1.0) for v in bma.values()) >= 0.1,
       "%.3f" % min(edge(v, 1.0) for v in bma.values()))
    # the asks: the careful route misses every figure
    na = S.nonarrival_truth(wd)
    name_of = {w["uwi"]: w["name"] for w in wd["wells"]}
    seen, crack = set(), {}
    for c in wd["cycles"]:
        k = (c["serial"], c["cycle_no"])
        if k in seen:
            continue
        seen.add(k)
        if W.WINDOW_START_UTC <= c["open_utc"] < W.WINDOW_END_UTC and c["result"] == "NO ARRIVAL":
            crack[c["label"]] = crack.get(c["label"], 0) + 1
    ok("ask P: the careful route (logged non-arrivals, each row once, host labels) misses every well",
       all(crack.get(name_of[u], 0) != v for u, v in na.items()), "")
    ok("ask P: aborted openings reach every plunger well", all(any(a["uwi"] == u for a in wd["aborted"]) for u in na), "")
    ok("ask P: no aborted opening sits within three hours of a window end or a unit change",
       all(S.clear_of_edges(a["near_utc"], wd["spans"][a["uwi"]]) for a in wd["aborted"]), "")
    # ask B careful route: survey by pad and tag against the register's current tags, rated otherwise
    import pack as P
    reg = P.register_state(wd)
    meas = {(m["site"], m["tag"]): m["scf_h"] for m in wd["survey"]["bleeds"]}
    area = {s["code"]: s["area"] for s in wd["sites"]}
    ck = {}
    for h in wd["bleed_hist"].values():
        site = next(s for s in wd["sites"] if s["code"] == h["site"])
        live = [d for d in reg if d["serial"] == h["serial"] and d["site"] == h["site"]]
        tag = live[0]["tag"] if live and h["to"] >= dt.datetime(2027, 1, 1, 8) else h["tag"]
        rate = meas.get((h["site"], tag), W.BLEED_MODELS[h["model"]]["scf_per_h"])
        kgv = rate * S.bleed_hours(h) * W.SCF_TO_M3 * site["x2026"] * W.CH4_KG_PER_M3
        k = (W.BLEED_MODELS[h["model"]]["maker"], area[h["site"]])
        ck[k] = ck.get(k, 0.0) + kgv
    ok("ask B: the careful route misses every maker-area total", all(round(ck.get(k, 0)) != round(v) for k, v in bma.items()),
       str({k: (round(v), round(ck.get(k, 0))) for k, v in bma.items()}))
    # separation line: the call's rows carry no ask device or hazard
    pb_uwis = {sp["uwi"] for sp in wd["seps"] if sp["group"] == "PB"}
    moved = {sp for spans in [wd["spans"]] for u, sl in spans.items() if len(sl) > 1 for sp in [u]}
    ok("separation: no outage re-send sits on a big-slug well's arrivals", not any(c["resent"] and c["uwi"] in pb_uwis
                                                                                  for c in wd["cycles"]), "")
    ok("separation: no moved controller unit ran a big-slug well", not (moved & pb_uwis), "")
    ok("separation: no continuous-bleed device is an intermittent-vent controller", all(b["kind"] in ("PC", "TC") for b in wd["bleeds"]), "")
    # input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big_rows = max(n.values()) if n else 0
    ok("gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("gate: 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
    ok("gate: a file of 25,000 rows or more", big_rows >= 25000, str(big_rows))
    meta = json.load(open(meta_path)) if meta_path else {}
    ok("gate: two or more distractors declared and shipped", len(meta.get("distractor_files", [])) >= 2 and
       all(d in files for d in meta.get("distractor_files", [])), str(meta.get("distractor_files")))
    ok("gate: no file describes the data", not any(re.search(r"readme|dictionary|manifest|notes|codebook", f, re.I) for f in files), "")
    ok("gate: no file name names the stump", not any(re.search(r"slug|band|trap|known_issue", f, re.I) for f in files), "")
    # realism sweep
    serials = sorted(int(sp["serial"].split("-")[1]) for sp in wd["seps"])
    steps = {b - a for a, b in zip(serials, serials[1:])}
    ok("realism: controller serials are not an arithmetic sequence", len(steps) > 3, "")
    liq = [tuple(np.round(wd["prod"][sp["uwi"]]["water"][:40], 1)) for sp in wd["seps"]]
    ok("realism: no two wells share a block of daily water", len(set(liq)) == len(liq), "")
    tot = [round(st[c]["golden"], 2) for c in st]
    ok("realism: no two pads share an intermittent-vent figure", len(set(tot)) == len(tot), "")
    ok("realism: every document date on or before the as-of date", all(o["created"].date() <= W.AS_OF for o in wd["orders"]), "")
    pad_codes = [s["name"] for s in wd["sites"]]
    ok("realism: the register's pad order is not alphabetical", pad_codes != sorted(pad_codes), "")
    ok("realism: counters wrap inside the year on at least one automated separator",
       any(any(b < a for (t0, a), (t1, b) in zip(rows, rows[1:])) for rows in wd["counters"].values()), "")
    # figures.json agrees with the truth
    if fig_path and os.path.exists(fig_path):
        fig = json.load(open(fig_path))
        ok("figures: the call in figures.json is the golden set", fig["call"] == sorted(names[c] for c in gold), "")
        ok("figures: every plunger well's non-arrivals in figures.json", len(fig["nonarrivals"]) == len(na), "")
    # positive control and absence check on a shipped PDF, through the verifier's extractor
    import verify as V
    std = V.pdf_text(os.path.join(target, W.FILES["standard"]))
    ok("control: the standard's text extracts (positive control on the clause the call needs)",
       "production day" in std.lower() and "0.678" in std, str(len(std)))
    flat = re.sub(r"\s+", " ", std).lower()
    ok("absence: the standard names no slug, band or arrival", not re.search(r"slug|\bband\b|arrival", flat), "")
    sheets = " ".join(re.sub(r"\s+", " ", V.pdf_text(os.path.join(target, W.FILES[k]))).lower()
                      for k in ("sheet_corrigan", "sheet_aldous", "sheet_brannick"))
    VB = V.load(target)
    ok("control: each maker's sheet extracts to its rated gas per cycle and its bleed",
       VB["per_cycle"] == {m: v["scf_per_cycle"] for m, v in W.LC_MODELS.items()} and
       VB["bleed_rate"] == {m: v["scf_per_h"] for m, v in W.BLEED_MODELS.items()}, str(VB["per_cycle"]))
    pcx = re.sub(r"\s+", " ", V.pdf_text(os.path.join(target, W.FILES["sheet_trellick"]))).lower()
    ok("control: the PCX-300 specification says the plunger brings the liquid above it to surface as it arrives",
       "brings that liquid to surface ahead of it as it arrives" in pcx, "")
    ok("absence: the PCX-300 specification names no separator, level, dump, band or slug",
       not re.search(r"separator|\blevel|dump|\bband|slug", pcx), "")
    ok("absence: no maker's sheet states a dump valve's flow capacity", not re.search(r"m3/h|gpm|capacity", sheets), "")
    ok("absence: no sheet turns liquid volume into dump cycles", not re.search(r"cycles per (?:day|hour)|liquid (?:rate|volume) (?:divided|over)|"
                                                                         r"bbl/d|m3/d per cycle", sheets), "")
    good = all(r[1] for r in RESULTS)
    for label, passed, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if passed else "FAIL", label, ("  [%s]" % detail) if (detail and not passed) else ""))
    print("checks: %d of %d pass" % (sum(r[1] for r in RESULTS), len(RESULTS)))
    return good
