"""task484's assertions on the cut pack and on the generator's clean truth: the input gates, the three rules (R1 the
raw material, R2 every Layer 1 item mishandled, R3a the analyst test, R3b the decisive step alone, R3c no plant), the
ladder, the standing family and its bins, every semantic fork row (SF1 to SF18), the asks, the separation line, the
documents' positive controls and the realism sweep.

    python3 task484/generator/checks.py          (after build.py)
"""
import collections
import copy
import csv
import datetime as dt
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import world as W   # noqa: E402

N, FAILS = [0], []


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def whole(x):
    return int(math.floor(x + 0.5))


def edge(v, u):
    return u / 2.0 - abs(v - round(v / u) * u)


def zones_pm(inv, p):
    return [inv["zone"][z]["pm"] for z in p["zones"]]


def fy_homes(p):
    s0 = dict(G.SEASON)
    G.SEASON.update({t: (dt.date(t, 7, 1), dt.date(t + 1, 6, 30)) for t in (2023, 2024, 2025)})
    h = G.propane_homes(p)
    G.SEASON.update(s0)
    return h


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    p = G.load(T)
    homes = G.propane_homes(p)
    gold = G.inventory(p, homes=homes)
    dflt = G.inventory(p, "default")
    Z = p["zones"]
    GOLD = ["Valley Floor South", "East Bench", "West Bench"]

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(T))
    check("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    check("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3,
          ",".join(sorted({f.rsplit(".", 1)[1] for f in files})))
    big = max(sum(1 for _ in open(os.path.join(T, f), "rb")) for f in files if f.endswith((".csv", ".txt")))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    check("gate: two or more distractors, shipped, named in metadata.json", len(dis) >= 2 and all(
        os.path.basename(d) in files for d in dis), ", ".join(dis))
    check("gate: no file name says distractor", not any("distract" in f for f in files))

    # ------------------------------------------------------------ the call
    check("call: the golden names Valley Floor South, East Bench and West Bench", gold["over"] == GOLD, str(gold["over"]))
    check("call: figures.json carries the same set", figs["call"]["over"] == GOLD)
    check("call: the fund divides evenly", p["fund"] % 3 == 0 and figs["call"]["share"] == p["fund"] // 3)
    margins = {z: gold["zone"][z]["pm"] - p["allot"][z] for z in Z}
    check("call: every zone 4.4 tons or more from its allotment", min(abs(m) for m in margins.values()) >= 4.4,
          " ".join("%.2f" % margins[z] for z in Z))

    # ------------------------------------------------------------ R1: the field's raw material ships
    tk = rows("wapiti_propane_tickets")
    check("R1a the tickets are deliveries at the account, gallons to the tenth", set(tk[0]) == {
        "ticket_no", "account_no", "delivery_date", "gallons", "product", "truck"})
    heads = " ".join(open(os.path.join(T, f)).readline().lower() for f in files if f.endswith(".csv"))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, G.find(T, "halvard_coop_propane")), read_only=True)
    coop_head = " ".join(str(c) for ws in wb.worksheets for r in ws.iter_rows(min_row=3, max_row=3, values_only=True)
                         for c in r).lower()
    lay = open(os.path.join(T, G.find(T, "coldwater_export_record_layout"))).read().lower()
    check("R1b no propane file carries an appliance field and no registry field a fuel (positive control: the "
          "layouts read back)", "member account" in coop_head and "tkt-ref" in lay and
          not any(w in h for h in (coop_head, lay, open(os.path.join(T, G.find(T, "wapiti_propane_accounts"))).readline().lower(),
                                   open(os.path.join(T, G.find(T, "wapiti_propane_tickets"))).readline().lower())
                  for w in ("stove", "appliance", "device")) and "fuel" not in
          open(os.path.join(T, G.find(T, "solid_fuel_device_registry"))).readline().lower())
    check("R1c no shipped column states a season's wood burned after 2024-25",
          "2025_26" not in heads and "amount_burned_2024_25" in heads)
    check("R1d the golden reads every residential propane account in the zones in all three seasons",
          len(homes) == sum(1 for a in p["acct"].values() if a["cls"] == "RES" and a["zone"]) and
          all(min(h["g"].values()) > 0 for h in homes), "%d accounts" % len(homes))

    # ------------------------------------------------------------ R3a the analyst test, R3b the decisive step alone
    check("R3a the default path (the survey carried) names Valley Floor South alone", dflt["over"] == ["Valley Floor South"],
          " ".join("%.2f" % x for x in zones_pm(dflt, p)))
    hdd = p_hdd()
    l1 = G.inventory(p, "default", scale=hdd)
    check("R3a the default at the degree days (%.5f) names Valley Floor South alone" % hdd, l1["over"] == dflt["over"])
    check("R3b the default with only the switch added files the golden", gold["over"] == GOLD)
    ups = sorted(set(z for u in range(0, 400) for z in [tuple(zz for zz in Z if dflt["zone"][zz]["pm"] * (1 + u / 1000.0)
                                                                > p["allot"][zz])]))
    check("R3b no uniform uplift of the default (0 to 40 per cent) files the golden set",
          tuple(GOLD) not in ups, "%d distinct sets" % len(ups))
    first = sorted(Z, key=lambda z: p["allot"][z] / dflt["zone"][z]["pm"])
    check("R3b Valley Floor North goes over before either bench under any uplift",
          first.index("Valley Floor North") < first.index("East Bench") and
          first.index("Valley Floor North") < first.index("West Bench"),
          " ".join("%s %.1f%%" % (z, 100 * (p["allot"][z] / dflt["zone"][z]["pm"] - 1)) for z in first))

    # ------------------------------------------------------------ the world's truth
    homes_w, devices = W.build()
    temps = W.temperatures()
    W.survey(devices)
    tr = collections.Counter()
    for d in devices:
        if W.in_use(d, 2025):
            tr[d.home.zone] += W.tons_of(d.cl, W.wood_2025(d, d.home, temps)) * W.CLASSES[d.cl][4] / 2000
    truth_over = [W.ZNAME[z] for z in W.ZC if tr[z] > W.ALLOTMENT[z]]
    check("truth: the world's true burning names the golden set", truth_over == GOLD,
          " ".join("%.2f" % tr[z] for z in W.ZC))
    check("truth: the world's degree days are equal to 0.02 per cent", abs(temps["hdd"][2025] / temps["hdd"][2024] - 1) < 2e-4)
    check("truth: no thrift at the homes without a heating appliance (the world's demand is weather only)",
          all(h.s == 0.0 for h in homes_w if h.fuel == "propane" and (not h.devices or W.CLASSES[h.devices[0].cl][3] is None)))

    # ------------------------------------------------------------ the standing family and its bins
    fy = fy_homes(p)
    fam = dict(golden=gold, pooled=G.inventory(p, homes=homes, R="pool"), no_change=G.inventory(p, homes=homes, R=1.0),
               gallons=G.inventory(p, homes=homes, form="level"), fireplaces_out=G.inventory(p, homes=homes, fpl_comp=False),
               fill_years=G.inventory(p, homes=fy))
    for name, inv in fam.items():
        check("family: %s files the golden set at the golden's whole tons" % name,
              inv["over"] == GOLD and [whole(x) for x in zones_pm(inv, p)] == [figs["zones"][z]["pm"] for z in Z],
              " ".join("%.2f" % x for x in zones_pm(inv, p)))
    for z in Z:
        vals = [inv["zone"][z]["pm"] for inv in fam.values()]
        b = whole(gold["zone"][z]["pm"])
        clear = min(min(vals) - (b - 0.5), (b + 0.5) - max(vals))
        check("bin: %s whole tons hold every member (clearance %.2f)" % (z, clear), clear >= 0.25)
        ex = [inv["zone"][z]["pm"] - dflt["zone"][z]["pm"] for inv in fam.values()]
        be = whole(ex[0])
        check("bin: %s propane component whole tons hold every member" % z,
              min(min(ex) - (be - 0.5), (be + 0.5) - max(ex)) >= 0.12 and be == figs["zones"][z]["extra_pm"])
    spread = max(max(inv["zone"][z]["pm"] for inv in fam.values()) - min(inv["zone"][z]["pm"] for inv in fam.values())
                 for z in Z)
    check("family: the standing family spans 0.25 tons or less in every zone", spread <= 0.25, "%.3f" % spread)
    cells_ok = all(len({whole(inv["cells"][k]["pm"]) for inv in fam.values()}) == 1 for k in gold["cells"])
    check("family: every zone and SCC cell's PM2.5 prints the same whole tons under every member", cells_ok)

    # ------------------------------------------------------------ the comparison's design
    for z in Z:
        trt = [h for h in homes if h["zone"] == z and h["cls"]]
        comp = [h for h in homes if h["zone"] == z and h["cls"] is None]
        r = lambda hs, a, b: sum(h["g"][a] for h in hs) / sum(h["g"][b] for h in hs)
        check("design: %s groups moved alike 2023-24 to 2024-25 (within 0.01)" % z,
              abs(r(trt, 2024, 2023) - r(comp, 2024, 2023)) < 0.01,
              "%.4f against %.4f" % (r(trt, 2024, 2023), r(comp, 2024, 2023)))
        dl = [h["g"][2024] - h["g"][2023] for h in trt]
        dc = [h["g"][2024] - h["g"][2023] for h in comp]
        lv = sum(dl) / len(dl) - sum(dc) / len(dc)
        se = math.sqrt(var(dl) / len(dl) + var(dc) / len(dc))
        check("design: %s the gallon form fails the same check (z %.1f)" % (z, lv / se), lv / se > 4.0)
        check("design: %s homes without a heating appliance took 0.99 to 1.01 of their 2024-25 gallons" % z,
              0.99 < r(comp, 2025, 2024) < 1.01, "%.4f" % r(comp, 2025, 2024))
        check("design: %s homes with one took 20 per cent less or more" % z, r(trt, 2025, 2024) < 0.8,
              "%.4f" % r(trt, 2025, 2024))

    # ------------------------------------------------------------ R2: every Layer 1 item, mishandled
    q = copy.deepcopy(p)
    raw = rows("heating_survey_2024_25_responses")
    for x, rr in zip(q["survey"], raw):
        if rr["unit"] == "pickup loads":
            x["units"] = float(rr["amount_burned_2024_25"]) / 3
    check("R2a pickup loads at a third of a cord: the call (SF6)", G.inventory(q, homes=homes)["over"] == GOLD)
    for x, rr in zip(q["survey"], raw):
        if rr["unit"] == "bags (40 lb)":
            x["units"] = float(rr["amount_burned_2024_25"]) * 50 / 2000.0
    check("R2b bags read at 50 pounds as well: the call", G.inventory(q, homes=homes)["over"] == GOLD)
    q2 = copy.deepcopy(p)
    q2["registry"] = [dict(d, removed=None) for d in p["registry"]]
    check("R2c every registry row counted, removed devices too: the call",
          G.inventory(q2, homes=G.propane_homes(q2))["over"] == GOLD)
    check("R2c the same mishandling leaves the default on Valley Floor South alone",
          G.inventory(q2, "default")["over"] == ["Valley Floor South"])
    posted = posted_homes(p)
    check("R2d Coldwater's transaction date read as the delivery date for the residential accounts: the call and "
          "every whole ton", [whole(x) for x in zones_pm(G.inventory(p, homes=posted), p)] ==
          [figs["zones"][z]["pm"] for z in Z])
    pooled_out = G.switch(p, homes + outside_homes(p), R="pool")
    check("R2e accounts outside the maintenance area in a pooled comparison: the ratio moves under 0.001",
          abs(pooled_out[Z[0], "R"] - G.switch(p, homes, R="pool")[Z[0], "R"]) < 0.001)
    comm = commercial_in_comparison(p, homes)
    check("R2f commercial accounts in the comparison: the call and every whole ton (SF15)",
          comm["over"] == GOLD and [whole(x) for x in zones_pm(comm, p)] == [figs["zones"][z]["pm"] for z in Z])
    check("R2g the 2020-2024 ACS release in place of the 2019-2023: ask B only (the call reads no Census file)",
          not any("acs" in k for k in p))
    bad_geo = [k for k, a in p["acct"].items() if a["cls"] == "RES" and a["geo"] and a["geo"] not in p["zone_of"]
               and not k.startswith(("L", "C", "H"))]
    check("R2h every residential account in the zones matches exactly one parcel", not bad_geo and len(
        {a["geo"] for a in p["acct"].values() if a["cls"] == "RES" and a["zone"]}) == len(homes))

    # ------------------------------------------------------------ R3c no plant, and the realism sweep
    tot = [whole(gold["zone"][z]["pm"]) for z in Z]
    check("R3c no two zones' appliance counts equal", len({sum(gold["cells"][z, c]["n"] for c in p["scc_of"]) for z in Z}) == 5)
    check("R3c no zone total on a round number", all(t % 10 for t in tot), str(tot))
    seq = [float(x["gallons"]) for x in tk[:5000]]
    check("R3c no repeated block of ticket gallons", len(set(tuple(seq[i:i + 6]) for i in range(0, 4994))) > 4900)
    check("R3c no extract carries a date after its pull", max(dt.date.fromisoformat(x["status_date"]) for x in
                                                               rows("solid_fuel_device_registry") if x["status_date"])
          <= dt.date(2026, 5, 15) and max(dt.datetime.strptime(x["delivery_date"], "%m/%d/%Y").date() for x in tk)
          <= dt.date(2026, 6, 30))
    check("R3c every persona is the card's", personas_ok())

    # ------------------------------------------------------------ the semantic fork table
    lp = propane_pm(p, homes)
    check("SF1 residential propane combustion's PM2.5 added to each zone: the same call",
          [z for z in Z if gold["zone"][z]["pm"] + lp[z] > p["allot"][z]] == GOLD,
          " ".join("%.2f" % lp[z] for z in Z))
    check("SF2 the fill-year comparison: the call and every whole ton",
          [whole(x) for x in zones_pm(fam["fill_years"], p)] == [figs["zones"][z]["pm"] for z in Z])
    act = collections.Counter((d["zone"], d["cls"]) for d in p["registry"] if d["removed"] is None)
    check("SF3 the devices Active at the extract are the devices in use in 2025-26", act == G.counts(p))
    check("SF4 whole tons against the allotments: the same call",
          [z for z in Z if whole(gold["zone"][z]["pm"]) > p["allot"][z]] == GOLD)
    check("SF5 every device's burn_zone field is its parcel's zone in the parcel list",
          all(p["zone_of"].get(d["geo"]) == d["zone"] for d in p["registry"]))
    check("SF6 pickup loads at a third of a cord keep the call (R2a)", True)
    pooled = pooled_survey(p, homes)
    check("SF7 classes pooled across zones: another set (ruled out by the methods note)", pooled["over"] != GOLD,
          str(pooled["over"]))
    unw = unweighted(p, homes)
    check("SF8 unweighted survey means: the call and every whole ton",
          unw["over"] == GOLD and [whole(x) for x in zones_pm(unw, p)] == [figs["zones"][z]["pm"] for z in Z])
    check("SF9 the survey at the degree days or as reported: every whole ton",
          [whole(x) for x in zones_pm(G.inventory(p, homes=homes, scale=hdd), p)] == [figs["zones"][z]["pm"] for z in Z])
    check("SF10 pooled, no change, gallons and fireplaces out: the call and every whole ton",
          all(fam[k]["over"] == GOLD for k in ("pooled", "no_change", "gallons", "fireplaces_out")))
    check("SF11 the tool gives fireplaces no heating efficiency", p["eff"]["FPL"] is None and all(
        p["eff"][c] for c in p["scc_of"] if c != "FPL"))
    fuel = rows("heating_fuel_equivalents")
    check("SF12 the fuel sheet carries one propane efficiency", sum(1 for x in fuel if x["fuel"] == "Propane") == 1)
    check("SF13 one heat content for propane, 91,500 Btu a gallon", {x["btu_per_unit"] for x in fuel if
                                                                     x["fuel"] == "Propane"} == {"91500"})
    check("SF14 the tool's cord and pellet energy and tons per cord read back", all(abs(a_ - b_) < 1e-6 * b_ for a_, b_ in
                                                                                   zip((p["cord_btu"], p["pellet_btu"], p["tpc"]),
                                                                                       (18.5e6, 16.4e6, 1.163))))
    check("SF15 commercial accounts in the comparison keep the call (R2f)", comm["over"] == GOLD)
    check("SF16 every residential account in the zones has deliveries in all three seasons",
          all(min(h["g"].values()) > 0 for h in homes))
    floor = floored(p, homes)
    check("SF17 a home's shortfall floored at zero: the call and every whole ton",
          floor["over"] == GOLD and [whole(x) for x in zones_pm(floor, p)] == [figs["zones"][z]["pm"] for z in Z])
    check("SF18 the ordinance divides the fund equally", "divided equally among those zones" in G.pdf_text(T, "maintenance_plan"))

    # ------------------------------------------------------------ the asks and the separation line
    a, ap = G.ask_a(p), G.ask_a(p, "posted")
    for z in Z:
        check("ask A %s: gallons mid-bin and the posted read misses both figures" % z,
              edge(a[z]["gal"], 100) >= 10 and edge(a[z]["nox"], 0.01) >= 0.0007 and
              round(ap[z]["gal"] / 100) != round(a[z]["gal"] / 100) and round(ap[z]["nox"], 2) != round(a[z]["nox"], 2),
              "%.1f against %.1f" % (a[z]["gal"], ap[z]["gal"]))
    b = G.ask_b(p)
    bc, bl = G.ask_b(p, split="code"), G.ask_b(p, release="acs5_2020_2024")
    for c, scc in p["scc_of"].items():
        check("ask B %s: mid-bin, the code join and the latest release miss both figures" % scc,
              edge(b[c]["app"], 1) >= 0.15 and edge(b[c]["pm"], 0.1) >= 0.015 and
              whole(bc[c]["app"]) != whole(b[c]["app"]) and round(bc[c]["pm"], 1) != round(b[c]["pm"], 1) and
              whole(bl[c]["app"]) != whole(b[c]["app"]) and round(bl[c]["pm"], 1) != round(b[c]["pm"], 1))
    stmt = {k for k, ds in p["deliv"].items() if k.startswith("C") and any(post and post != d for d, g, post in ds)}
    check("separation: every Coldwater account posting off its delivery date is commercial",
          stmt and all(p["acct"][k]["cls"] == "COM" for k in stmt), "%d accounts" % len(stmt))
    check("separation: the device rows sit in every zone", {p["acct"][k]["zone"] for k in stmt} == set(Z))

    # ------------------------------------------------------------ the documents, with positive controls
    plan = G.pdf_text(T, "maintenance_plan")
    check("doc: the plan files the estimand (positive control)", "emitted from the wood burned that season by the "
          "wood-burning appliances in use" in plan)
    check("doc: no plan sentence says how a season's wood burned is estimated", "survey" not in plan.lower())
    meth = G.pdf_text(T, "heating_survey_2024_25_methods")
    check("doc: the survey note scopes its estimates to 2024-25 (positive control)",
          "estimate of the wood burned in the 2024-25 heating season" in meth)
    tool = G.pdf_text(T, "montana_rwc_tool")
    check("doc: the tool documentation reads back its table (positive control)", "not a heating appliance" in tool)
    allp = " ".join([plan, meth, tool] + [open(os.path.join(T, f), errors="replace").read()
                                          for f in files if f.endswith(".txt")])
    for w in ("price", "switch", "substitut", "displac"):
        check("doc: no shipped document or layout says %s" % w, w not in allp.lower())
    print("\n%d checks, %d failed%s" % (N[0], len(FAILS), (": " + "; ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0


def rows(prefix):
    with open(os.path.join(T, G.find(T, prefix)), newline="") as f:
        return list(csv.DictReader(f))


def var(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def p_hdd():
    t = rows("khlv_daily_temperatures")
    h = collections.Counter()
    for x in t:
        if not x["tmax_f"]:
            continue
        d = dt.date.fromisoformat(x["date"])
        s = G.season_of(d)
        if s:
            h[s] += max(0.0, 65 - (float(x["tmax_f"]) + float(x["tmin_f"])) / 2)
    return h[2025] / h[2024]


def posted_homes(p):
    q = copy.deepcopy(p)
    q["deliv"] = {k: [(post or d, g, post) for d, g, post in ds] for k, ds in p["deliv"].items()}
    return G.propane_homes(q)


def outside_homes(p):
    out = []
    for k, a in p["acct"].items():
        if a["cls"] == "RES" and a["zone"] is None:
            out.append(dict(k=k, zone=None, cls=None, fpl=False, g={t: G.season_gallons(p, k, t) for t in G.SEASON}))
    return out


def commercial_in_comparison(p, homes):
    extra = []
    for k, a in p["acct"].items():
        if a["cls"] == "COM" and a["zone"]:
            extra.append(dict(k=k, zone=a["zone"], cls=None, fpl=False, g={t: G.season_gallons(p, k, t) for t in G.SEASON}))
    return G.inventory(p, homes=homes + extra)


def pooled_survey(p, homes):
    m0 = G.survey_means
    G.survey_means = lambda p_, small=10, pooled=False, weighted=True: m0(p_, small, True, weighted)
    try:
        return G.inventory(p, homes=homes)
    finally:
        G.survey_means = m0


def unweighted(p, homes):
    m0 = G.survey_means
    G.survey_means = lambda p_, small=10, pooled=False, weighted=True: m0(p_, small, pooled, False)
    try:
        return G.inventory(p, homes=homes)
    finally:
        G.survey_means = m0


def floored(p, homes):
    s0 = G.switch

    def sw(p_, homes_, R="zone", form="ratio", fpl_comp=True):
        out = s0(p_, homes_, R, form, fpl_comp)
        for z in p_["zones"]:
            for c in p_["scc_of"]:
                trt = [h for h in homes_ if h["zone"] == z and h["cls"] == c]
                out[z, c] = sum(max(0.0, h["g"][2024] * out[z, "R"] - h["g"][2025]) for h in trt)
        return out
    G.switch = sw
    try:
        return G.inventory(p, homes=homes)
    finally:
        G.switch = s0


def propane_pm(p, homes):
    pm = collections.Counter()
    f = p["ef_lp"]["Residential propane combustion", "PM2.5"]
    for h in homes:
        pm[h["zone"]] += h["g"][2025] * p["btu_gal"] / 1e6 * f / 2000.0
    return pm


def personas_ok():
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task484.json")))
    people = set(card["world"]["people"])
    text = " ".join(G.pdf_text(T, pre) for pre in ("maintenance_plan", "heating_survey_2024_25_methods", "montana_rwc_tool"))
    found = {n for n in (W.PEOPLE.values()) if n in text}
    return found <= people and found


if __name__ == "__main__":
    sys.exit(main())
