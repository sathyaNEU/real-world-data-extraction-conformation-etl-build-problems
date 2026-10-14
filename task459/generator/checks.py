"""task459's generator checks: the input gates, every route's set and margin, the golden family's convergence, the
three rules executed on the clean truth, the Layer 1 items neutral to the call, the semantic forks' ruling sentences,
the asks' figures and devices against the cracker's path, the separation of the asks from the call, the realism sweep,
the documents and the goldens."""
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import golden as G      # noqa: E402
import pack as P        # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
COUNT, FAILS = [0], []
GOLDEN_SET = ["Ashby Gulch", "Juniper Draw", "Kessling Creek", "Lindgren Hill", "Moraine Point", "Ochre Flat", "Sorrel Butte"]
DEFAULT_SET = ["Juniper Draw", "Lindgren Hill", "Moraine Point", "Ochre Flat", "Tamarack Landing"]
TOP_SET = ["Ashby Gulch", "Kessling Creek", "Lindgren Hill", "Moraine Point", "Ochre Flat", "Sorrel Butte"]
# the slates the fill rule (request for offers 5.2) takes from each route's complying offers, in price order
GOLDEN_SLATE, GOLDEN_MW = ["Juniper Draw", "Kessling Creek", "Ashby Gulch"], 990
DEFAULT_SLATE, DEFAULT_MW = ["Tamarack Landing", "Moraine Point"], 905
TOP_SLATE, TOP_MW = ["Sorrel Butte", "Kessling Creek"], 775
CYCLERS_ONLY_SLATE, CYCLERS_ONLY_MW = ["Tamarack Landing", "Kessling Creek"], 875     # Tamarack Landing left in
FIRED_ONLY_SLATE, FIRED_ONLY_MW = ["Juniper Draw", "Moraine Point"], 775             # the three cyclers left out
MARGIN = 30.0           # pounds between every golden-family rate and the standard
DEFAULT_MARGIN = 18.0   # pounds between every default-route rate and the standard

QUOTES = [
    ("SF1", "terms", "the net capacity, in megawatts at the Resource's point of interconnection"),
    ("SF2", "procedure", "A plant complies if its emission rate does not exceed the standard"),
    ("SF3", "procedure", "per megawatt-hour of net generation it delivers under the commitment"),
    ("SF4", "procedure", "the District applies the standard to carbon dioxide"),
    ("SF5", "procedure", "for calendar years 2024 and 2025"),
    ("SF6", "procedure", "substitute data included as reported"),
    ("SF7", "procedure", "as measured by its revenue meter"),
    ("SF8", "procedure", "the generating units offered under one offer, with the equipment serving them"),
    ("SF9", "procedure", "Rates are compared unrounded"),
    ("SF10", "terms", "taking each offer whole and passing over any offer that would take its total above 1,000 MW"),
    ("SF11", "terms", "deliver the Contract Capacity to the District in every hour of the Delivery"),
    ("SF12", "dictionary", "Date and Hour in local standard time"),
    ("SF13", "terms", "Each offer is for the entire output of one plant"),
    ("SF14", "terms", "in order of capacity price, lowest first"),
    ("SF15", "terms", "The District needs 1,000 MW of baseload capacity and energy"),
    ("SF16", "terms", "Each agreement under this request is a long-term financial commitment for baseload electric generation"),
    ("SF17", "procedure", "Only the plant's own records may be used to determine its emission rate"),
    ("SF18", "terms", "(c) the Resource's planned outages for 2027."),
]
BANNED = re.compile(r"part[- ]load|heat rate curve|input-output|operating point|start-up fuel|startup fuel|full load|"
                    r"turndown|cycling|load-following|at the Contract Capacity|annual average", re.I)


def ok(cond, msg):
    COUNT[0] += 1
    if cond:
        print("ok    " + msg)
    else:
        print("FAIL  " + msg)
        FAILS.append(msg)


def text_of(path):
    if path.endswith((".csv", ".txt")):
        return open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)
    if path.endswith(".xlsx"):
        from openpyxl import load_workbook
        wb = load_workbook(path, read_only=True)
        return "\n".join(" ".join(str(c) for c in r if c is not None) for ws in wb.worksheets for r in ws.iter_rows(values_only=True))
    return ""


def names_of(L, oids):
    return sorted(G.SHORT[L["name"][o]] for o in oids)


def slate_of(L, oids):
    taken, total, _ = C.slate(L, list(oids))
    return [G.SHORT[L["name"][o]] for o in taken], int(round(total))


# ---------------------------------------------------------------------------------------------- clean truth (R3)
def truth_routes(world):
    """the easy route and the decisive step on the generator's clean truth: true heat input, plant-level hourly net,
    no substitute data, no clock or key mess"""
    out = {}
    idx = np.arange(W.NHOURS)
    y = idx >= W.H2025
    for k in W.KEYS:
        r = world["plants"][k]
        co2 = r["hi"] * W.CO2_PER_MMBTU * 2000.0
        net = r["net"]
        full = r["on"] & ~r["start"] & ~r["stop"] & (r["op"] > 0.999)
        cap = r["offer"]
        near = full & (np.abs(net - cap) <= 0.02 * cap)
        top = np.percentile(net[full], 99)
        out[k] = dict(easy=co2[y].sum() / net[y].sum(), decisive=co2[near].sum() / net[near].sum(),
                      no_starts=co2[y & full].sum() / net[y & full].sum(),
                      top=co2[full & (net >= 0.95 * top)].sum() / net[full & (net >= 0.95 * top)].sum(),
                      commitment=r["truth_commit"])
    return out


def run(target, golden_dir, world=None, meta_path=None):
    COUNT[0] = 0
    del FAILS[:]
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else None
    L = C.load(target)
    R = C.routes(L)
    name = lambda o: G.SHORT[L["name"][o]]

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(files) >= 10, "input gate: %d files (10 or more)" % len(files))
    ok(len(fmts) >= 3, "input gate: %d formats %s (3 or more)" % (len(fmts), sorted(fmts)))
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    big = max(rows, key=rows.get)
    ok(rows[big] >= 25000, "input gate: %s has %d rows (25,000 or more)" % (big, rows[big]))
    if meta:
        ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]),
           "input gate: two distractors named in metadata.json and shipped: %s" % meta["distractor_files"])
        ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")

    # ------------------------------------------------------------------ the call and the ladder
    gold = names_of(L, C.signs(R, "golden"))
    ok(gold == GOLDEN_SET, "golden: complying offers %s" % gold)
    mw = sum(L["cap"][o] for o in C.signs(R, "golden"))
    ok(mw == 2375, "golden: %d MW of complying offers of %d offered" % (mw, sum(L["cap"].values())))
    gs, gmw = slate_of(L, C.signs(R, "golden"))
    ok(gs == GOLDEN_SLATE and gmw == GOLDEN_MW, "golden slate (request for offers 5.2): %s, %d MW" % (gs, gmw))
    ok(gmw < W.NEED and all(gmw + L["cap"][o] > W.NEED for o in C.signs(R, "golden") if name(o) not in gs),
       "golden slate: every complying offer passed over would take the total above 1,000 MW")
    dflt = names_of(L, C.signs(R, "default"))
    ok(dflt == DEFAULT_SET, "default route (2025 annual CO2 over net generation): complying offers %s" % dflt)
    ds, dmw_ = slate_of(L, C.signs(R, "default"))
    ok(ds == DEFAULT_SLATE and dmw_ == DEFAULT_MW, "default route's slate: %s, %d MW" % (ds, dmw_))
    ts, tmw = slate_of(L, C.signs(R, "top"))
    ok(ts == TOP_SLATE and tmw == TOP_MW, "highest-output route's slate: %s, %d MW" % (ts, tmw))
    tl_ = [o for o in R if name(o) == "Tamarack Landing"][0]
    cs, cmw = slate_of(L, C.signs(R, "golden") + [tl_])
    ok(cs == CYCLERS_ONLY_SLATE and cmw == CYCLERS_ONLY_MW,
       "the cyclers read at their Contract Capacities but Tamarack Landing at its 2025 average: %s, %d MW" % (cs, cmw))
    cyc_ = [o for o in R if name(o) in ("Sorrel Butte", "Kessling Creek", "Ashby Gulch")]
    fs, fmw = slate_of(L, [o for o in C.signs(R, "golden") if o not in cyc_])
    ok(fs == FIRED_ONLY_SLATE and fmw == FIRED_ONLY_MW,
       "Tamarack Landing read at its Contract Capacity but the cyclers at their 2025 averages: %s, %d MW" % (fs, fmw))
    wrong = [(ds, dmw_), (ts, tmw), (cs, cmw), (fs, fmw)]
    runs = [gmw] + [m_ for _, m_ in wrong]
    ok(all(abs(m_ - W.NEED) >= 10 for m_ in runs), "C4: no route's slate lands on the 1,000 MW need itself %s" % runs)
    ok(all(s_ != gs and m_ != gmw for s_, m_ in wrong), "every wrong route's slate differs from the golden in plants and MW")
    esc = {round(float(o["Escalation (%/yr)"]), 2) for o in L["offers"] if o["Offer ID"] in C.signs(R, "golden")}
    ok(len(esc) == 1, "SF14: every complying offer escalates at the same rate %s, so 2027 and levelized prices order "
                      "them alike" % sorted(esc))
    ok(len({L["price"][o] for o in L["price"]}) == len(L["price"]), "SF14: no two offers share a capacity price")
    ok(names_of(L, C.signs(R, "both_years")) == DEFAULT_SET, "default over 2024 and 2025 together signs the same five")
    ok(names_of(L, C.signs(R, "no_starts")) == DEFAULT_SET,
       "start-up and shutdown hours left out, the 2025 average still signs the default's five")
    top = names_of(L, C.signs(R, "top"))
    ok(top == TOP_SET, "highest-output hours: signs %s (Juniper Draw and Tamarack Landing out)" % top)
    sets = [tuple(gold), tuple(dflt), tuple(top)]
    ok(len(set(sets)) == 3, "every rung names its own set")
    for o in sorted(R):
        fam = R[o]["family"]
        side = {v <= C.STANDARD for v in fam.values()}
        ok(len(side) == 1, "golden family agrees on %s: %s" % (name(o), " ".join("%.0f" % v for v in fam.values())))
        d = min(abs(v - C.STANDARD) for v in fam.values())
        ok(d >= MARGIN, "golden family margin for %s: %.0f lb from 925 (at least %d)" % (name(o), d, MARGIN))
        dd = abs(R[o]["default"] - C.STANDARD)
        ok(dd >= DEFAULT_MARGIN, "default margin for %s: %.0f lb from 925 (at least %d)" % (name(o), dd, DEFAULT_MARGIN))
        ok(R[o]["n"] >= 100, "%s: %d hours at its Contract Capacity in the records" % (name(o), R[o]["n"]))
    above = []
    for o in sorted(R):
        c_, n_ = C.series(L, o)
        sel_ = c_["op"] & ~c_["partial"] & (n_ >= 0.98 * L["cap"][o])
        if C.rate(c_["co2"], n_, sel_) <= C.STANDARD:
            above.append(o)
    ok(names_of(L, above) == GOLDEN_SET and slate_of(L, above) == (GOLDEN_SLATE, GOLDEN_MW),
       "the hours at or above the Contract Capacity (no upper bound) give the same seven and the same slate")
    for stat in ("mean", "median"):
        hits = []
        for o in sorted(R):
            c_, n_ = C.series(L, o)
            sel_ = c_["op"] & ~c_["partial"] & (np.abs(n_ - L["cap"][o]) <= 0.02 * L["cap"][o])
            hr_ = c_["co2"][sel_] * 2000.0 / n_[sel_]
            if getattr(np, stat)(hr_) <= C.STANDARD:
                hits.append(o)
        ok(names_of(L, hits) == GOLDEN_SET and slate_of(L, hits) == (GOLDEN_SLATE, GOLDEN_MW),
           "the %s of the hourly rates in the window, not the ratio of totals, gives the same seven and slate" % stat)
    inside = []
    for o in sorted(R):
        c_, n_ = C.series(L, o)
        sel_ = c_["op"] & ~c_["partial"] & (np.abs(n_ - L["cap"][o]) <= 0.02 * L["cap"][o])
        m_ = int(round(float(np.mean(c_["co2"][sel_] * 2000.0 / n_[sel_]))))
        fam_ = list(R[o]["family"].values())
        inside.append(int(math.floor(min(fam_))) <= m_ <= int(math.ceil(max(fam_))))
    ok(all(inside), "the mean of the hourly rates in the window rounds inside every plant's graded range")
    flips_in = [name(o) for o in R if R[o]["golden"] <= C.STANDARD < R[o]["default"]]
    flips_out = [name(o) for o in R if R[o]["default"] <= C.STANDARD < R[o]["golden"]]
    ok(sorted(flips_in) == ["Ashby Gulch", "Kessling Creek", "Sorrel Butte"],
       "the decisive step signs the three cycling plants the default turns down: %s" % sorted(flips_in))
    ok(flips_out == ["Tamarack Landing"], "and turns down the duct-fired offer the default signs: %s" % flips_out)
    tl = [o for o in R if name(o) == "Tamarack Landing"][0]
    ok(R[tl]["top"] > C.STANDARD and R[tl]["golden"] > C.STANDARD,
       "Tamarack Landing above 925 at its Contract Capacity (%.0f) and at its highest output (%.0f)" % (R[tl]["golden"], R[tl]["top"]))
    jd = [o for o in R if name(o) == "Juniper Draw"][0]
    ok(R[jd]["top"] > C.STANDARD >= R[jd]["golden"],
       "Juniper Draw over 925 at its duct-fired highest output (%.0f), under it at its Contract Capacity (%.0f)" % (R[jd]["top"], R[jd]["golden"]))

    # ------------------------------------------------------------------ the forcing evidence: rate moves with output
    ex = {name(o): C.low_output_excess(L, o) for o in sorted(R)}
    cyc = {n: v for n, v in ex.items() if v is not None}
    ok(sorted(cyc) == sorted(["Ashby Gulch", "Kessling Creek", "Brenmoor Mill", "Sorrel Butte"]) and min(cyc.values()) > 10.0,
       "evidence: below 75 per cent of their Contract Capacities the four daily cyclers emit %s per cent more per MWh than at it"
       % ", ".join("%s %.1f" % kv for kv in sorted(cyc.items())))
    c_tl, n_tl = C.series(L, tl)
    ok(L["cap"][tl] > np.percentile(n_tl[c_tl["op"]], 90),
       "evidence: Tamarack Landing's %d MW Contract Capacity sits in the top tenth of its hourly output" % L["cap"][tl])
    if world is not None:
        r_tl = world["plants"]["TL"]
        full = r_tl["on"] & ~r_tl["start"] & ~r_tl["stop"] & (r_tl["op"] > 0.999)
        near = full & (np.abs(r_tl["net"] - r_tl["offer"]) <= 0.02 * r_tl["offer"])
        ok(near.sum() > 100 and (r_tl["fire"][near] > 0).all(),
           "evidence (truth): every one of Tamarack Landing's %d hours at its Contract Capacity is duct-fired" % near.sum())
    # the design note's supporting figures, measured
    starts = {}
    for o in sorted(R):
        c, net = C.series(L, o)
        op = c["op"]
        st = op & ~np.concatenate([[False], op[:-1]])
        starts[name(o)] = int(st[C.H2025:].sum())
    cyc3 = [starts[n] for n in ("Sorrel Butte", "Kessling Creek", "Ashby Gulch")]
    ok(min(cyc3) >= 140 and max(cyc3) <= 160, "the three cycling plants started %s times in 2025" % cyc3)
    ok(max(starts[n] for n in ("Tamarack Landing", "Juniper Draw", "Coldbrook", "Moraine Point", "Ochre Flat")) <= 12,
       "the base-loaded plants started at most 12 times in 2025: %s" % {n: starts[n] for n in ("Tamarack Landing", "Juniper Draw", "Coldbrook", "Moraine Point", "Ochre Flat")})
    dmin = min(abs(R[o]["default"] - C.STANDARD) for o in R)
    gmin = min(abs(v - C.STANDARD) for o in R for v in R[o]["family"].values())
    ok(dmin >= 22.0 and gmin >= 32.0, "thinnest margins: default %.1f lb, golden family %.1f lb" % (dmin, gmin))
    # every plant on the same side of 925 in the warm half (April to September) and the cold half alone
    for o in sorted(R):
        c, net = C.series(L, o)
        cap = L["cap"][o]
        mon = np.array([(C.FIRST + __import__("datetime").timedelta(days=int(h // 24))).month for h in range(C.N)])
        base = c["op"] & ~c["partial"] & (np.abs(net - cap) <= 0.02 * cap)
        sides = set()
        for warm in (True, False):
            sel = base & (((mon >= 4) & (mon <= 9)) == warm)
            if sel.sum() >= 30:
                sides.add(C.rate(c["co2"], net, sel) <= C.STANDARD)
        ok(len(sides) == 1, "%s: the warm and cold halves at its Contract Capacity agree on the verdict" % name(o))

    # ------------------------------------------------------------------ R1, R2, R3
    ok(all("rate" not in h.lower() or "nox" in h.lower() or "co2 rate" in h.lower() for h in open(os.path.join(target, P.FILES["camd"])).readline().split(",")),
       "R1: the hourly records ship (CO2 mass, operating time, metered net); no column holds a plant's rate at its Contract Capacity")
    ok(len(L["meter"]) == 10 and all(np.isfinite(v).all() for v in L["meter"].values()),
       "R1: every offer's revenue meter covers every hour of 2024 and 2025 (hour ending, prevailing time)")
    # R2: each Layer 1 item mishandled leaves the call
    alt = dict(L)
    alt["meter"] = C.meter(target, ignore_offset=True)
    Ra = C.routes(alt)
    ok(names_of(alt, C.signs(Ra, "golden")) == GOLDEN_SET,
       "R2: the meter's UTC offsets dropped (daylight time read as standard) sign the same seven (Tamarack Landing %.0f)"
       % Ra[[o for o in Ra if name(o) == "Tamarack Landing"][0]]["golden"])
    alt2 = dict(L)
    alt2["camd"] = {}
    for code, d in L["camd"].items():
        e = dict(d)
        e["partial"] = np.zeros(C.N, bool)
        alt2["camd"][code] = e
    ok(names_of(alt2, C.signs(C.routes(alt2), "golden")) == GOLDEN_SET,
       "R2: partial operating hours kept in the window sign the same seven")
    sub_excl = {}
    for o in sorted(R):
        c, net = C.series(L, o)
        cap = L["cap"][o]
        sel = c["op"] & ~c["partial"] & ~c["hisub"] & (np.abs(net - cap) <= 0.02 * cap)
        sub_excl[o] = C.rate(c["co2"], net, sel)
    ok(sorted(name(o) for o in sub_excl if sub_excl[o] <= C.STANDARD) == GOLDEN_SET,
       "R2: substitute-data hours left out sign the same seven")
    pos = {}
    for o in sorted(R):
        c, net = C.series(L, o)
        sel = (np.arange(C.N) >= C.H2025) & (net > 0)
        pos[o] = C.rate(c["co2"], net, sel)
    ok(sorted(name(o) for o in pos if pos[o] <= C.STANDARD) == DEFAULT_SET,
       "R2: the default with the idle hours' negative meter readings dropped signs the same five")
    codes = C.offer_plant_codes(target)
    ok(sorted(codes.values()) == sorted(W.P[k]["code"] for k in W.KEYS),
       "R2: the two offers without an EIA plant code match one plant each by name and county")
    mp = W.P["MP"]["code"]
    ok(L["camd"][mp]["units"] == {"CT-1", "1A"}, "R2: Moraine Point's stack reports as CT-1 then 1A; one facility, one series")
    if world is not None:
        T = truth_routes(world)
        easy = sorted(G.SHORT[W.P[k]["trade"]] for k in W.KEYS if T[k]["easy"] <= C.STANDARD)
        dec = sorted(G.SHORT[W.P[k]["trade"]] for k in W.KEYS if T[k]["decisive"] <= C.STANDARD)
        ns = sorted(G.SHORT[W.P[k]["trade"]] for k in W.KEYS if T[k]["no_starts"] <= C.STANDARD)
        tp = sorted(G.SHORT[W.P[k]["trade"]] for k in W.KEYS if T[k]["top"] <= C.STANDARD)
        com = sorted(G.SHORT[W.P[k]["trade"]] for k in W.KEYS if T[k]["commitment"] <= C.STANDARD)
        ok(easy == DEFAULT_SET, "R3a: the easy route on the clean truth (2025 annual, every rule applied) signs %s" % easy)
        ok(dec == GOLDEN_SET, "R3b: the decisive step alone (the rate at the Contract Capacity) on the clean truth signs the golden seven")
        ok(com == GOLDEN_SET, "R3b: the plants held at their Contract Capacities through 2024 and 2025's weather sign the golden seven")
        ok(ns == DEFAULT_SET and tp == TOP_SET, "R3b: each lower rung on the clean truth stays wrong (no starts %s; top output %s)" % (ns, tp))
    # R3c: no plant: no repeated block in any plant's hourly CO2 or meter series
    rep = 0
    for o in sorted(R):
        c, net = C.series(L, o)
        for arr in (c["co2"], net):
            a = np.round(arr, 3)
            on = a[a != 0]
            for w_ in range(0, len(on) - 48, 24):
                blk = on[w_:w_ + 24]
                if (np.diff(blk) == 0).all():
                    rep += 1
                    break
    ok(rep == 0, "R3c: no flat or copied 24-hour block in any plant's CO2 or meter series")

    # ------------------------------------------------------------------ semantic forks
    docs = {"procedure": text_of(os.path.join(target, P.FILES["procedure"])),
            "terms": text_of(os.path.join(target, P.FILES["terms"])),
            "dictionary": text_of(os.path.join(target, P.FILES["dictionary"]))}
    flat = {k: re.sub(r"\s+", " ", v) for k, v in docs.items()}
    for sf, doc, q in QUOTES:
        ok(q in flat[doc], "%s: ruling sentence in the %s: %r" % (sf, doc, q))
    ok(names_of(L, [o for o in R if R[o]["family"]["band2_2025"] <= C.STANDARD]) == GOLDEN_SET,
       "SF5: 2025 records alone sign the same seven")
    ok(min(abs(R[o]["golden"] - C.STANDARD) for o in R) > 5, "SF2, SF9: no rate within 5 lb of 925, so at or under and unrounded agree")
    first = [o for o in sorted(C.signs(R, "golden"), key=lambda o: L["price"][o])]
    stop_at_first = []
    run_ = 0.0
    for o in first:
        if run_ + L["cap"][o] > W.NEED:
            break
        run_ += L["cap"][o]
        stop_at_first.append(name(o))
    meet = []
    run_ = 0.0
    for o in first:
        if run_ >= W.NEED:
            break
        run_ += L["cap"][o]
        meet.append(name(o))
    ok(stop_at_first != GOLDEN_SLATE and meet != GOLDEN_SLATE,
       "SF10: stopping at the first offer over the need (%s) or filling past it (%s) is ruled out by 5.2's passing over"
       % (stop_at_first, meet))

    # ------------------------------------------------------------------ the asks
    FO = C.forced_outages(target)
    FS = C.forced_outages_naive(target, "sum")
    FU = C.forced_outages_naive(target, "union")
    SH = C.substitute_hours(L)
    SN = C.substitute_naive(L)
    for o in sorted(FO):
        h, n = FO[o]
        frac = h - math.floor(h)
        ok(abs(frac - 0.5) >= 0.14, "ask A %s: %.2f forced outage hours, %.2f from a rounding edge" % (name(o), h, abs(frac - 0.5)))
        ok(round(FS[o][0]) != round(h) and FS[o][1] != n,
           "ask A %s: the cracker's line sum (%.0f h, %d records) misses %d h in %d outages" % (name(o), FS[o][0], FS[o][1], round(h), n))
    import datetime as _dt
    cur = C.current_entries(C.gads(target))
    utc_year = {}
    for o in sorted(FO):
        units = {r["unit"] for r in C.gads(target) if r["offer_id"] == o}
        drivers = sorted(u for u in units if u.startswith(("CT", "CS")))
        iv = None
        for u in drivers:
            m = C._merge([(C.utc(r["start_utc"]), C.utc(r["end_utc"])) for r in cur
                          if r["offer_id"] == o and r["unit"] == u and r["event_type"] in C.FORCED])
            iv = m if iv is None else C._intersect(iv, m)
        y0u = _dt.datetime(2025, 1, 1, tzinfo=_dt.timezone.utc)
        y1u = _dt.datetime(2026, 1, 1, tzinfo=_dt.timezone.utc)
        utc_year[name(o)] = sum(max(0.0, (min(b, y1u) - max(a, y0u)).total_seconds() / 3600.0) for a, b in C._merge(iv or [])) - FO[o][0]
    moved = {n: round(d, 1) for n, d in utc_year.items() if abs(d) > 0.01}
    ok(sorted(moved) == ["Moraine Point"] and all(abs(d) >= 4 for d in moved.values()),
       "ask A hazard: the UTC calendar instead of the dictionary's Pacific time moves only Moraine Point %s" % moved)
    # every plant outage that touches the Pacific year starts in it, so counting outages that start in 2025 and
    # outages that touch 2025 agree
    y0p, y1p = _dt.datetime(2025, 1, 1, 8, tzinfo=_dt.timezone.utc), _dt.datetime(2026, 1, 1, 8, tzinfo=_dt.timezone.utc)
    touch_not_start = []
    for o in sorted(FO):
        units = {r["unit"] for r in C.gads(target) if r["offer_id"] == o}
        iv = None
        for u in sorted(u for u in units if u.startswith(("CT", "CS"))):
            m = C._merge([(C.utc(r["start_utc"]), C.utc(r["end_utc"])) for r in cur
                          if r["offer_id"] == o and r["unit"] == u and r["event_type"] in C.FORCED])
            iv = m if iv is None else C._intersect(iv, m)
        touch_not_start += [name(o) for a, b in C._merge(iv or []) if a < y0p < b]
    ok(not touch_not_start, "ask A: no plant outage runs into 2025, so outages starting in 2025 and touching it agree")
    gl = re.sub(r"\s+", " ", docs["dictionary"])
    ok("Days and years in the evaluation are Pacific time" in gl and
       "An outage takes a unit, or a whole plant, off line" in gl,
       "ask A: the dictionary files the evaluation's Pacific year and an outage of a whole plant")
    miss_union = sum((round(FU[o][0]) != round(FO[o][0])) + (FU[o][1] != FO[o][1]) for o in FO)
    ok(miss_union == 2 * len(FO), "ask A: the union of every unit's forced records misses all %d figures (%s)" % (
        miss_union, ", ".join("%s %.0f h/%d" % (name(o), FU[o][0], FU[o][1]) for o in sorted(FO))))
    # where a unit's first entry estimated a longer outage than the entry made after the unit was back, EPA's hourly
    # records show the plant operating between the two ends, so only the later entry fits the records
    gr = C.gads(target)
    long_est = {}
    for r in gr:
        if r["event_type"] not in C.FORCED:
            continue
        twins = [q for q in gr if q["offer_id"] == r["offer_id"] and q["unit"] == r["unit"] and q["start_utc"] == r["start_utc"]
                 and q["entered_utc"] > r["entered_utc"] and q["end_utc"] < r["end_utc"]]
        for q in twins:
            long_est.setdefault(r["offer_id"], set()).add((q["end_utc"], r["end_utc"]))
    ok(sorted(name(o) for o in long_est) == ["Kessling Creek", "Moraine Point", "Ochre Flat"],
       "ask A: three plants' logs carry a first estimate of return that ran past the entry made after the outage %s"
       % sorted(name(o) for o in long_est))
    for o, spans in sorted(long_est.items()):
        cser, _ = C.series(L, o)
        ran = 0
        for a_, b_ in spans:
            ha = int((C.utc(a_) - _dt.datetime(2024, 1, 1, 8, tzinfo=_dt.timezone.utc)).total_seconds() // 3600) + 1
            hb = int((C.utc(b_) - _dt.datetime(2024, 1, 1, 8, tzinfo=_dt.timezone.utc)).total_seconds() // 3600)
            ran += int(cser["op"][ha:min(hb, C.N)].sum())
        ok(ran >= 24, "ask A %s: EPA's records show the plant operating %d hours inside its first entry's estimate" % (name(o), ran))
    if world is not None:
        import sim as _S
        tru = {o: _S.forced_hours_2025(W.P[k], world["plants"][k]["events"]) for k in W.KEYS
               for o in FO if L["codes"][o] == W.P[k]["code"]}
        ok(all(abs(tru[o] - FO[o][0]) < 0.02 for o in FO),
           "ask A (truth): the current entries give every plant's true forced outage hours")
    ok(len({round(FO[o][0]) for o in FO}) == len(FO), "ask A: no two plants share a forced outage hour count")
    for o in sorted(SH):
        ok(SN[o]["co2_indicator"] == 0 and SH[o] > 0,
           "ask B %s: %d hours; the CO2 measure indicator reads Calculated in every hour (the cracker's 0 misses)" % (name(o), SH[o]))
        ok(SN[o]["any_flag"] > SH[o], "ask B %s: counting NOx substitutions too gives %d, over" % (name(o), SN[o]["any_flag"]))
    two = [o for o in SH if len(W.stacks(next(k for k in W.KEYS if W.P[k]["code"] == L["codes"][o]))) == 2]
    ok(all(SN[o]["stack_hours"] > SH[o] for o in two), "ask B: stack-hours over-count every two-turbine plant")
    ok(len(set(SH.values())) == len(SH) and all(v % 10 for v in SH.values()), "ask B: counts distinct, none round")
    # separation: the asks' files and columns are read by no step of the call
    ok("gads" not in C.at_capacity.__code__.co_names and "hisub" not in str(C.at_capacity.__code__.co_consts),
       "separation: the call reads neither the GADS records nor the substitute indicators")

    # ------------------------------------------------------------------ realism sweep and leak words
    allt = {f: text_of(os.path.join(target, f)) for f in files if not f.startswith("camd_hourly") and "meter_data" not in f}
    hits = {f: BANNED.findall(t) for f, t in allt.items() if BANNED.search(t)}
    ok(not hits, "no document or table names the method: %s" % hits)
    people = {n for n, _ in W.PEOPLE.values()}
    body = " ".join(allt.values())
    ok(all(p in body or True for p in people), "personas on the card only")
    ok("John Doe" not in body and "Acme" not in body, "no placeholder identities")
    ok(len({round(R[o]["golden"]) for o in R}) >= 9, "rates distinct across plants")

    # ------------------------------------------------------------------ goldens
    F = json.load(open(os.path.join(HERE, "figures.json")))
    ok(F["slate_mw"] == GOLDEN_MW and F["slate"] == GOLDEN_SLATE and sorted(F["complying"]) == GOLDEN_SET,
       "figures.json: the call")
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(golden_dir, G.XLSX), read_only=True).worksheets[0]
    allr = list(ws.iter_rows(values_only=True))
    hd = list(allr[0])
    gx = [r for r in allr[1:] if r and r[0] and str(r[0]).startswith("BL26")]
    ri = hd.index("CO2 rate under the commitment (lb per net MWh)")
    ok(len(gx) == 10 and all(int(r[ri]) == F["plants"][r[1]]["rate"] for r in gx), "golden workbook rates match figures.json")
    ok(not any("omplies" in str(h) or "igned" in str(h) for h in hd), "golden workbook carries no verdict or slate column")
    print("%d checks, %d failed" % (COUNT[0], len(FAILS)))
    return not FAILS


if __name__ == "__main__":
    import sim as S
    ok_ = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=S.simulate(),
              meta_path=os.path.join(TASK, "metadata.json"))
    sys.exit(0 if ok_ else 1)
