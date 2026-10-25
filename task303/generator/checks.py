"""task303 assertions on the built pack (and, where the generator knows more, on its record): the input gates, the call
and its ladder, the standing family, every semantic fork row, the separation of the asks' devices from the call's
rows, each device's forcing figure and every ask path missing, every graded figure's distance to its bin's edge.

    python3 task303/generator/checks.py <target dir>     (exit 0 clean, 1 on any failure)
"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs as FG
import params as P
import solve as S

FAILS = []


def ok(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("FAIL", msg)


def edge(v, u):
    return (u / 2 - abs(v - round(v / u) * u)) / u


def gates(target):
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "input gate: %d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "input gate: formats %s" % sorted(fmts))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gate: largest csv %d rows" % big)
    ok(set(files) == set(P.FILES.values()), "the pack is the declared file list")


def call(pk):
    g, d = pk.call(True), pk.call(False)
    og = sorted(S.CAND, key=lambda f: -g[f])
    od = sorted(S.CAND, key=lambda f: -d[f])
    ok(og[0] == "F-205" and g["F-205"] / g[og[1]] >= 1.5, "golden F-205 clears %s by %.2f" % (og[1], g["F-205"] / g[og[1]]))
    ok(od[0] == "F-112" and d["F-112"] / d[od[1]] >= 1.4, "default F-112 clears %s by %.2f" % (od[1], d["F-112"] / d[od[1]]))
    ok(od.index("F-205") == 2, "the default puts F-205 third")
    # the standing family: every shared-minute construction files the same figures
    fam = pk.family()
    ok(len({tuple(FG.rnd(v[f], 100) for f in S.CAND) for v in fam.values()}) == 1, "standing family spread zero")
    for k, v in fam.items():
        ok(max(S.CAND, key=lambda f: v[f]) == "F-205", "family member %s names F-205" % k)
    # the ladder's reflex rungs and where each lands
    rungs = {"every interruption, every device": (pk.call(False, devices=("Feeder breaker", "Line recloser", "Fuse",
                                                                          "Transformer"),
                                                   causes=tuple(S.LEG_CAUSE.values())), "F-112"),
             "every backbone ticket, every cause": (pk.call(False, causes=tuple(S.LEG_CAUSE.values())), "F-112"),
             "line reclosers only": (pk.call(False, devices=("Line recloser",)), "F-301"),
             "per backbone mile": ({f: d[f] / pk.inv[f]["Three-phase backbone (miles)"] for f in S.CAND}, "F-112"),
             "per customer": ({f: d[f] / pk.inv[f]["Customers (31 Dec 2025)"] for f in S.CAND}, "F-112"),
             "major event days kept": (pk.call(False, med=False), "F-112")}
    for k, (v, want) in rungs.items():
        ok(max(S.CAND, key=lambda f: v[f]) == want, "rung %s lands on %s" % (k, want))
    return g, d


def separation(pk):
    """no device row in the call's population, and nothing on the storm days that shows a loss of supply"""
    ok(all("." not in t["raw"] for t in pk.tickets if t["sys"] == "legacy" and t["device"] in S.BACKBONE),
       "SEP1: no backbone ticket carries a handheld duration")
    restored, _ = pk.crew_times()
    cur = {t["tkt"]: t for t in pk.tickets if t["sys"] == "current"}
    ok(all(cur[k]["med"] for k in restored), "SEP2: every crew record is a major event day ticket")
    moved = [t for t in cur.values() if t["tkt"] in restored and t["end"] != restored[t["tkt"]].astimezone(S.UTC)]
    ok(all(t["med"] for t in moved), "SEP3: every restoration the desk entered late is on a major event day")
    c23 = [t for t in cur.values() if t["med"]]
    fl = pk.shared_flags(c23)
    ok(not any(f and t["device"] == "Feeder breaker" for t, f in zip(c23, fl)),
       "SEP4: no storm-day breaker ticket opened with every sibling feeder in 2023 to 2025")
    ok(all(not t["med"] or t["sys"] == "current" or t["day"].year < 2023 for t in pk.tickets), "SEP5: years by system")
    # SEP6: the handheld tickets' dates move no call figure, read either way
    base = pk.call(True)
    keep = pk.tickets
    pk.tickets = pk._tickets("golden", "naive")
    alt = pk.call(True)
    pk.tickets = keep
    ok(all(FG.rnd(alt[f], 100) == FG.rnd(base[f], 100) for f in S.CAND),
       "SEP6: the call files the same six figures with OUT_DT read as the day every ticket began")
    return restored, moved


def forcing(pk, restored, moved):
    # ask A: each storm restoration in the outage system is either the desk's late entry, in its sessions and at least a
    # quarter hour after the crew's restore, or the crew's Restored time as it arrived, to the minute
    eastern, _ = pk.crew_times("eastern")
    late = [(t, restored[t["tkt"]]) for t in moved if t["end"] > restored[t["tkt"]].astimezone(S.UTC)]
    synced = [t for t in pk.tickets if t["tkt"] in restored and t["end"] == eastern[t["tkt"]].astimezone(S.UTC)]
    ok(len(late) > 1000, "FA1: %d storm tickets the desk closed late" % len(late))
    ok(all(t["end"] >= r.astimezone(S.UTC) + dt.timedelta(minutes=15) for t, r in late),
       "FA2: every late entry is at least a quarter hour after the crew's restore")
    hrs = set(P.BATCH_HOURS)
    lag = [min(k for k in range(0, 4) if (t["end"].astimezone(S.ET) - dt.timedelta(hours=k)).hour in hrs)
           for t, r in late]
    ok(max(lag) <= 1, "FA3: every late entry falls within two hours of a session's start (latest %d)" % max(lag))
    ok(len(late) + len(synced) == len(restored),
       "FA4: %d late entries and %d storm tickets carrying the crew's time as it arrived make all %d"
       % (len(late), len(synced), len(restored)))
    # the contract crews' devices: read as Eastern local time, every contract crew's En route on a storm day in
    # daylight saving time comes before the storm desk gave it the job, and no other crew's ever does
    by = defaultdict(dict)
    for r in pk.crew:
        by[(r["job_id"], r["crew_id"])][r["status"]] = r
    early, n_edt, n_est, other, gold = 0, 0, 0, 0, 0
    for st in by.values():
        if "Assigned" not in st or "En route" not in st:
            continue
        a, e = pk.stamp(st["Assigned"], "eastern"), pk.stamp(st["En route"], "eastern")
        contract = st["Assigned"]["crew_type"] == "Contract line crew"
        if contract and a.dst():
            n_edt += 1
            early += e < a
        elif contract:
            n_est += e < a
        else:
            other += e < a
        gold += pk.stamp(st["En route"]) < pk.stamp(st["Assigned"])
    ok(n_edt > 500 and early == n_edt and n_est == 0 and other == 0 and gold == 0,
       "FA5: read as Eastern local time, %d of %d contract crews on daylight-saving storm days are en route before the "
       "desk gave them the job, %d in standard time, %d other crews; on the devices' standard time, %d"
       % (early, n_edt, n_est, other, gold))
    # ask B: every handheld entry is hours and minutes, dated the day the crew closed it
    dec = [t["raw"] for t in pk.tickets if t["sys"] == "legacy" and "." in t["raw"]]
    ok(len(dec) > 1000 and all(len(x.split(".")[1]) == 2 and int(x.split(".")[1]) <= 59 for x in dec),
       "FB1: %d decimal DUR_MIN, none past .59" % len(dec))
    whole = [int(t["raw"]) for t in pk.tickets if t["sys"] == "legacy" and "." not in t["raw"]]
    ok(min(whole) > 5, "FB2: every whole-minute DUR_MIN is more than five minutes")

    def breaks(tk):
        leg = sorted((t for t in tk if t["sys"] == "legacy"), key=lambda t: (t["tkt"][:2], int(t["tkt"][3:])))
        out = [b for a, b in zip(leg, leg[1:]) if a["tkt"][:2] == b["tkt"][:2] and b["start"] < a["start"]]
        out += [t for t in leg if int(t["tkt"][:2]) != t["start"].year % 100]
        return out
    gb, nb = breaks(pk.tickets), breaks(pk._tickets("golden", "naive"))
    ok(not gb and len(nb) > 100 and all("." in t["raw"] or "." in pk_prev(pk, t)["raw"] for t in nb),
       "FC1: the ticket numbers run in the order the interruptions began with a handheld ticket dated the day it closed "
       "(%d breaks); read as the day it began, %d breaks" % (len(gb), len(nb)))
    return len(late), len(dec), len(nb)


def pk_prev(pk, t):
    """the ticket numbered just before t in its year (an order break is the pair's later ticket)"""
    leg = sorted((x for x in pk.tickets if x["sys"] == "legacy"), key=lambda x: (x["tkt"][:2], int(x["tkt"][3:])))
    i = [x["tkt"] for x in leg].index(t["tkt"])
    return leg[i - 1] if i else t


def asks(pk):
    A, B = pk.storm(), pk.taps()
    for m in ("naive", "crew", "all_est", "pbl_all_year", "released", "repeated", "utc_day"):
        x = pk.storm(m)
        for f in S.CAND:
            ok(FG.rnd(x[f]["cmi"], 1000) != FG.rnd(A[f]["cmi"], 1000), "ask A %s %s cmi misses" % (m, f))
            ok(FG.rnd(x[f]["per"], 0.1) != FG.rnd(A[f]["per"], 0.1), "ask A %s %s per misses" % (m, f))
    for dur in ("golden", "hours", "minutes", "drop"):
        for date in ("golden", "naive", "all"):
            if (dur, date) == ("golden", "golden"):
                continue
            x = pk.taps(dur, date)
            for f in S.CAND:
                ok(FG.rnd(x[f]["year"], 10) != FG.rnd(B[f]["year"], 10), "ask B %s %s %s year misses" % (dur, date, f))
                ok(FG.rnd(x[f]["per"], 0.1) != FG.rnd(B[f]["per"], 0.1), "ask B %s %s %s per misses" % (dur, date, f))
    return A, B


def edges(g, A, B):
    figs = [("call " + f, g[f], 100) for f in S.CAND] + [("value", g["F-205"] * S.INCENTIVE, 1000),
            ("value from the stated figure", FG.rnd(g["F-205"], 100) * S.INCENTIVE, 1000)]
    figs += [("A cmi " + f, A[f]["cmi"], 1000) for f in S.CAND] + [("A per " + f, A[f]["per"], 0.1) for f in S.CAND]
    figs += [("B year " + f, B[f]["year"], 10) for f in S.CAND] + [("B per " + f, B[f]["per"], 0.1) for f in S.CAND]
    for k, v, u in figs:
        ok(edge(v, u) >= 0.07, "%s %.3f sits %.3f of a bin from the edge" % (k, v, edge(v, u)))
    return min(edge(v, u) for _, v, u in figs)


def forks(pk, g):
    """the semantic fork table's rows (DESIGN_NOTE.md), each closed by a filed sentence or converging"""
    base = {f: FG.rnd(g[f], 100) for f in S.CAND}
    # SF1 customer-minutes are customers interrupted times minutes (plan section 3): no other product is filed
    # SF2 major event days by the Eastern date the interruption began (notes): the UTC date moves the record
    rec_utc = [t for t in pk.tickets if t["start"].astimezone(S.UTC).date() not in pk.meds]
    ok(len(rec_utc) != len([t for t in pk.tickets if not t["med"]]), "SF2 the UTC date is a different population")
    # SF3 2019 to 2025 is the record in both exports: nothing outside it ships
    ok(all(2019 <= t["day"].year <= 2025 for t in pk.tickets), "SF3 every ticket is in 2019 to 2025")
    # SF4 vegetation, wind or wildlife: the legacy codes TREE, WIND, ANML map one to one
    ok({t["cause"] for t in pk.tickets} == set(S.LEG_CAUSE.values()), "SF4 the two systems' causes map one to one")
    # SF5 the backbone's devices: feeder breaker and line reclosers (notes); fuses and transformers are off it
    ok({t["device"] for t in pk.tickets} == {"Feeder breaker", "Line recloser", "Fuse", "Transformer"}, "SF5 devices")
    # SF6 a year is the seven-year sum over seven; per-year averages of the yearly sums give the same figure
    yr = defaultdict(lambda: defaultdict(int))
    fl = pk.shared_flags([t for t in pk.tickets if not t["med"]])
    for t, s in zip([t for t in pk.tickets if not t["med"]], fl):
        if not s and t["device"] in S.BACKBONE and t["cause"] in S.ADDRESSED:
            yr[t["feeder"]][t["day"].year] += t["customers"] * t["minutes"]
    ok(all(FG.rnd(0.9 * sum(yr[f][y] for y in range(2019, 2026)) / 7, 100) == base[f] for f in S.CAND),
       "SF6 the mean of the seven yearly figures is the figure")
    # SF7 nine in ten applied to the customer-minutes, or to the tickets: the same figure (a multiplier)
    # SF8 the shared-minute test with the feeders of the inventory's substation or of the tickets: same feeders
    subs = defaultdict(set)
    for t in pk.tickets:
        subs[t["sub"]].add(t["feeder"])
    ok(all(subs[s] == pk.subfeeders[s] for s in subs), "SF8 each substation's feeders agree in both sources")
    # SF9 tolerance and sibling count: the standing family (asserted in call(), spread zero)
    ok(len({tuple(FG.rnd(v[f], 100) for f in S.CAND) for v in pk.family().values()}) == 1, "SF9 the standing family")
    # SF10 restoration minutes from DUR_MIN for the call's rows are whole minutes in every reading
    ok(all("." not in t["raw"] for t in pk.tickets if t["sys"] == "legacy" and t["device"] in S.BACKBONE),
       "SF10 the call's legacy minutes are whole minutes")
    # SF11 the fall-back hour: a legacy local time in the repeated hour, read either way, files the same figure
    amb = [t for t in pk.tickets if t["sys"] == "legacy" and t["start"].fold == 0 and
           t["start"].replace(fold=1).utcoffset() != t["start"].utcoffset()]
    ok(all(not (t["device"] in S.BACKBONE and t["cause"] in S.ADDRESSED) or t["med"] for t in amb) or len(amb) < 5,
       "SF11 the repeated hour holds no call ticket that could move (%d tickets in it)" % len(amb))
    # SF12 the incentive on the rounded or the exact figure: the same thousand
    ok(FG.rnd(base["F-205"] * S.INCENTIVE, 1000) == FG.rnd(g["F-205"] * S.INCENTIVE, 1000),
       "SF12 the value is the same thousand from the rounded or the exact figure")
    # SF13 the candidates are the six in the plan's table
    ok(set(S.CAND) == {f for f in pk.inv if f in S.CAND}, "SF13 candidates")
    # SF1 customers served times minutes is another figure, ruled out by the plan's section 3
    served = defaultdict(int)
    for t, s in zip([t for t in pk.tickets if not t["med"]], fl):
        if not s and t["device"] in S.BACKBONE and t["cause"] in S.ADDRESSED:
            served[t["feeder"]] += pk.inv[t["feeder"]]["Customers (31 Dec 2025)"] * t["minutes"]
    ok(any(FG.rnd(0.9 * served[f] / 7, 100) != base[f] for f in S.CAND), "SF1 customers served is another figure")
    # SF7 nine in ten of the customer-minutes or of each ticket's: a multiplier, the same figure
    ok(all(abs(0.9 * (g[f] / 0.9) - g[f]) < 1e-6 for f in S.CAND), "SF7 the multiplier commutes")
    # SF14 an interruption that ran past midnight counts on the day it began (notes); clipping it is another figure
    past = [t for t in pk.tickets if not t["med"] and t["device"] in S.BACKBONE and t["cause"] in S.ADDRESSED
            and t["feeder"] in S.CAND and (t["start"] + dt.timedelta(minutes=t["minutes"])).date() > t["day"]]
    ok(len(past) > 0, "SF14 %d call tickets run past midnight, ruled by the notes' day rule" % len(past))
    # SF15 the 2.10 rate is per customer-minute a year (plan section 4, order section III)
    from docx import Document
    plan = " ".join(p_.text for p_ in Document(os.path.join(pk.dir, P.FILES["plan"])).paragraphs)
    ok("USD 2.10 for each customer-minute of sustained interruption a year" in plan, "SF15 the plan's rate")
    # SF16 every breaker ticket in a year carries that year's customers for its feeder
    yc = defaultdict(set)
    for t in pk.tickets:
        if t["device"] == "Feeder breaker":
            yc[(t["feeder"], t["day"].year)].add(t["customers"])
    ok(all(len(v) == 1 for v in yc.values()), "SF16 each feeder's breaker tickets carry one count a year")
    # SF17 ask A by the UTC date is another population (a stop)
    A, Au = pk.storm(), pk.storm("utc_day")
    ok(all(FG.rnd(A[f]["cmi"], 1000) != FG.rnd(Au[f]["cmi"], 1000) for f in S.CAND), "SF17 the UTC date moves ask A")
    # SF18 per customer interrupted is customer-minutes over customers; the mean ticket duration is another figure
    B = pk.taps()
    durs = defaultdict(list)
    for t in pk.tickets:
        if t["feeder"] in S.CAND and t["device"] == "Fuse" and not t["med"]:
            durs[t["feeder"]].append(t["minutes"])
    ok(all(FG.rnd(sum(durs[f]) / len(durs[f]), 0.1) != FG.rnd(B[f]["per"], 0.1) for f in S.CAND),
       "SF18 the mean ticket duration is another figure")
    # SF19 tap fuses only; with transformers it is another figure
    tx = defaultdict(int)
    for t in pk.tickets:
        if t["feeder"] in S.CAND and t["device"] in ("Fuse", "Transformer") and not t["med"]:
            tx[t["feeder"]] += t["customers"] * t["minutes"]
    ok(all(FG.rnd(tx[f] / 7, 10) != FG.rnd(B[f]["year"], 10) for f in S.CAND), "SF19 transformers make another figure")
    # SF20 the seven years over seven; the current system's three years over three is another figure
    c3 = defaultdict(int)
    for t in pk.tickets:
        if t["feeder"] in S.CAND and t["device"] == "Fuse" and not t["med"] and t["sys"] == "current":
            c3[t["feeder"]] += t["customers"] * t["minutes"]
    ok(all(FG.rnd(c3[f] / 3, 10) != FG.rnd(B[f]["year"], 10) for f in S.CAND), "SF20 three years is another figure")
    # SF21 ask A's days are the accepted days dated 2023 to 2025; the days accepted in dockets of 2023 to 2025 are others
    with open(os.path.join(pk.dir, P.FILES["meds"]), newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    dated = {r["event_date"] for r in rows if 2023 <= int(r["event_date"][:4]) <= 2025}
    docket = {r["event_date"] for r in rows if 2023 <= int(re.search(r"E-(\d{4})-", r["accepted_in"]).group(1)) <= 2025}
    ok(dated != docket, "SF21 the days dated 2023 to 2025 (%d) are not the days accepted in 2023 to 2025 dockets (%d)"
       % (len(dated), len(docket)))
    return True


def main(target):
    gates(target)
    pk = S.Pack(target)
    g, d = call(pk)
    restored, moved = separation(pk)
    n_late, n_dec, n_breaks = forcing(pk, restored, moved)
    A, B = asks(pk)
    m = edges(g, A, B)
    forks(pk, g)
    print("checks: %d failures; %d late storm entries, %d handheld durations, %d order breaks on the start-date "
          "reading, nearest edge %.3f of a bin" % (len(FAILS), n_late, n_dec, n_breaks, m))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
