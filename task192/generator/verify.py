"""Independent verifier: reads only target/, the goldens and figures.json, with its own parsers, and recomputes the
call and every graded figure a second way (customer by customer, from merged supply-loss episodes). Exit 1 on any
mismatch. It imports nothing from the generator."""
import bisect
import collections
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
from zoneinfo import ZoneInfo

import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
CT = ZoneInfo("America/Chicago")
FIVE = 300000
OUT = []


def check(label, cond, detail=""):
    OUT.append((label, bool(cond), str(detail)[:240]))


def epoch_ms(d):
    return int(d.timestamp() * 1000)


def t_utc(s):
    return epoch_ms(dt.datetime.fromisoformat(s.replace("Z", "+00:00")))


def t_wall(s):
    return epoch_ms(dt.datetime.strptime(s, "%m/%d/%Y %H:%M").replace(tzinfo=CT))


def t_scada(s):
    a, z = s.rsplit(" ", 1)
    return epoch_ms(dt.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f").replace(
        tzinfo=dt.timezone(dt.timedelta(hours=-5 if z == "CDT" else -6))))


def t_cst(s):
    return epoch_ms(dt.datetime.strptime(s, "%m/%d/%Y %H:%M:%S").replace(tzinfo=dt.timezone(dt.timedelta(hours=-6))))


def day(t):
    return dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).astimezone(CT).date()


def table(rel):
    with open(os.path.join(T, rel), newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    files = sorted(os.path.relpath(os.path.join(r, f), T) for r, _, fs in os.walk(T) for f in fs)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    # ------------------------------------------------------------ read-back of every format, with positive controls
    pdf = [f for f in files if f.endswith(".pdf")][0]
    text = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(os.path.join(T, pdf)).pages))
    check("pdf: the procedure reads back with its sections", "DRP-04" in text and "5 Overhead line patrol" in text)
    tmed = float(re.search(r"T\s?MED, is ([\d.]+) minutes", text).group(1))
    nsys = int(re.search(r"divided by ([\d,]+), the customers served", text).group(1).replace(",", ""))
    check("pdf: the threshold and denominator read back", tmed > 0 and nsys > 30000, (tmed, nsys))
    gj = json.load(open(os.path.join(T, "gis/substations.geojson")))
    check("geojson: five substations", len(gj["features"]) == 5)
    oms_wb = openpyxl.load_workbook(os.path.join(T, "oms/oms_outage_history_2025_2026.xlsx"), read_only=True)
    check("xlsx: the OMS export's three sheets", oms_wb.sheetnames == ["Legacy tickets", "Incidents", "Restoration Steps"])
    leg = [r for r in oms_wb["Legacy tickets"].iter_rows(min_row=2, values_only=True) if r[0]]
    inc = [r for r in oms_wb["Incidents"].iter_rows(min_row=2, values_only=True) if r[0]]
    stp = [r for r in oms_wb["Restoration Steps"].iter_rows(min_row=2, values_only=True) if r[0]]
    oms_wb.close()
    fr = openpyxl.load_workbook(os.path.join(T, "assets/feeder_register.xlsx"), read_only=True)
    feeders = {r[0]: r for r in fr["Feeders"].iter_rows(min_row=2, values_only=True) if r[0]}
    ren = [r for r in fr[fr.sheetnames[1]].iter_rows(min_row=2, values_only=True) if r[0]]
    fr.close()
    check("xlsx: sixteen feeders and the Cotter Road crosswalk", len(feeders) == 16 and len(ren) == 3)
    strokes = sum(1 for _ in open(os.path.join(T, "weather/lightning_strokes_2025_2026.csv"))) - 1
    check("csv: the stroke file holds 25,000 or more rows", strokes >= 25000, strokes)
    old_feeder = {r[0]: r[1] for r in ren}
    old_bkr = {r[2]: r[3] for r in ren}
    old_pt = {r[4]: r[5] for r in ren}
    nb = lambda d: old_bkr.get(d, d)
    # ------------------------------------------------------------ the register as dated rows, the customers
    reg = collections.defaultdict(list)
    point = {}
    for r in table("assets/protective_device_register.csv"):
        a = dt.date.fromisoformat(r["in_service_from"])
        b = dt.date.fromisoformat(r["in_service_to"]) if r["in_service_to"] else dt.date(2100, 1, 1)
        reg[nb(r["device_id"])].append((a, b, old_feeder.get(r["feeder"], r["feeder"]),
                                        nb(r["upstream_device"]) if r["upstream_device"] else None, r))
        if r["scada_point"]:
            point[r["scada_point"]] = nb(r["device_id"])
    for o, n in old_pt.items():
        point[o] = point[n]

    def at(dev, d):
        for a, b, f, up, r in reg[dev]:
            if a <= d <= b:
                return f, up, r
        return None, None, None

    trf = {r["transformer_id"]: (r["feeder"], nb(r["protective_device"])) for r in table("assets/distribution_transformers.csv")}
    sp = {}
    by_t = collections.defaultdict(list)
    for r in table("customers/service_points_2026-10-31.csv"):
        sp[r["service_point"]] = (r["transformer_id"], dt.date.fromisoformat(r["service_connected"]),
                                  dt.date.fromisoformat(r["service_disconnected"]) if r["service_disconnected"] else None,
                                  r["feeder"])
        by_t[r["transformer_id"]].append(r["service_point"])
    live = lambda s, d: sp[s][1] <= d and (sp[s][2] is None or sp[s][2] > d)
    cache = {}

    def below(dev, d):
        """Service points supplied through a device on a date."""
        if dev in sp:
            return {dev} if live(dev, d) else set()
        if dev in trf:
            return {s for s in by_t[dev] if live(s, d)}
        key = (dev, d)
        if key not in cache:
            outs = set()
            for tid, (_, pd) in trf.items():
                x = pd
                while x:
                    if x == dev:
                        outs.update(s for s in by_t[tid] if live(s, d))
                        break
                    x = at(x, d)[1]
            cache[key] = outs
        return cache[key]

    def feeder_of(dev, d):
        if dev in sp:
            return feeder_of(trf[sp[dev][0]][1], d)
        if dev in trf:
            return feeder_of(trf[dev][1], d)
        return at(dev, d)[0]

    # ------------------------------------------------------------ supply-loss intervals per customer
    kids = collections.defaultdict(list)
    for r in leg:
        if r[1]:
            kids[r[1]].append(r)
    tickets = []
    for r in leg:
        if r[1]:
            continue
        a, b = t_wall(r[5]), t_wall(r[6])
        st = [(t_wall(k[6]), int(k[7])) for k in kids[r[0]]]
        if st:
            st.append((b, int(r[7]) - sum(n for _, n in st)))
        tickets.append([nb(r[3]), r[4], a, b, st, int(r[7])])
    sts = collections.defaultdict(list)
    for r in stp:
        sts[r[0]].append((t_utc(r[2]), int(r[3])))
    for r in inc:
        tickets.append([r[2], r[3], t_utc(r[4]), t_utc(r[5]), sorted(sts.get(r[0], [])), int(r[6])])
    soe = collections.defaultdict(list)
    for r in table("scada/soe_breakers_reclosers_2025_2026.csv"):
        soe[point[r["point"]]].append((t_scada(r["time"]), r["state"]))
    for k in soe:
        soe[k].sort()
    starts_by_dev = collections.defaultdict(list)
    for tk in tickets:
        starts_by_dev[tk[0]].append(tk[2])
    for dev, seq in soe.items():
        t_open = None
        for t, s in seq:
            if s == "OPEN" and t_open is None:
                t_open = t
            elif s == "CLOSED" and t_open is not None:
                if t - t_open > FIVE and not any(abs(x - t_open) <= 120000 for x in starts_by_dev[dev]):
                    tickets.append([dev, "SCADA", t_open, t, [], None])
                t_open = None
    check("SOE: unticketed sustained openings found", any(tk[1] == "SCADA" for tk in tickets))
    ivs = collections.defaultdict(list)       # customer -> [start, end, ticket index]
    mism = 0
    stepped = []
    for k, (dev, kind, a, b, st, n) in enumerate(tickets):
        d = day(a)
        cust = below(dev, d)
        if n is not None and n != len(cust):
            mism += 1
        if st:
            stepped.append((k, cust))
        for c in cust:
            ivs[c].append((a, b, k))
    check("connectivity reproduces the OMS customer counts", mism == 0, mism)
    # merge each customer's intervals into episodes: overlapping or contiguous intervals are one loss of supply
    episodes = collections.defaultdict(list)    # customer -> [(start, end, first ticket)]
    for c, xs in ivs.items():
        xs.sort()
        cur = None
        for a, b, k in xs:
            if cur and a <= cur[1]:
                cur[1] = max(cur[1], b)
            else:
                if cur:
                    episodes[c].append(tuple(cur))
                cur = [a, b, k]
        episodes[c].append(tuple(cur))
    # daily system SAIDI: stepped tickets by their steps, the rest by episode length, on the day each began
    step_k = {k for k, _ in stepped}
    daily = collections.defaultdict(float)
    for k, cust in stepped:
        dev, kind, a, b, st, n = tickets[k]
        daily[day(a)] += sum(m * (t - a) for t, m in st) / 60000
    for c, eps in episodes.items():
        for a, b, k in eps:
            if k in step_k:
                continue
            daily[day(a)] += (b - a) / 60000
    meds = sorted(d for d, v in daily.items() if d.year == 2026 and v / nsys > tmed)
    check("major event days", [d.isoformat() for d in meds] == F["meds"], meds)
    inwin = lambda d: dt.date(2026, 1, 1) <= d <= dt.date(2026, 10, 31) and d not in set(meds)
    end = dt.date(2026, 10, 31)
    nt = collections.Counter(sp[s][3] for s in sp if live(s, end))
    cmi = collections.Counter()
    n_int = collections.Counter()
    for k, cust in stepped:
        dev, kind, a, b, st, n = tickets[k]
        if inwin(day(a)):
            cmi[feeder_of(dev, day(a))] += sum(m * (t - a) for t, m in st) / 60000
    for c, eps in episodes.items():
        for a, b, k in eps:
            if not inwin(day(a)):
                continue
            n_int[c] += 1
            if k not in step_k:
                dev = tickets[k][0]
                cmi[feeder_of(dev, day(a))] += (b - a) / 60000
    cemi = collections.Counter(sp[c][3] for c in n_int if live(c, end) and n_int[c] > 2)
    # ------------------------------------------------------------ momentary events, customer by customer
    events = []
    for dev, seq in soe.items():
        if at(dev, dt.date(2026, 6, 1))[2] is None or at(dev, day(seq[0][0]))[2]["device_type"] != "BREAKER":
            continue
        i = 0
        while i < len(seq):
            if seq[i][1] != "OPEN":
                i += 1
                continue
            t0 = seq[i][0]
            grp = [x for x in seq[i:] if x[0] <= t0 + FIVE]
            opens = [x for x in grp if x[1] == "OPEN"]
            closes = [x for x in grp if x[1] == "CLOSED"]
            if len(closes) >= len(opens):
                events.append((t0, dev))
            j = i + len(grp)
            while j < len(seq) and seq[j][1] != "OPEN":
                j += 1
            i = j
    logs = collections.defaultdict(list)
    for r in table("protection/recloser_control_events_2025_2026.csv"):
        logs[r["control"]].append((t_cst(r["time_cst"]), r["event"], r))
    for dev, seq in logs.items():
        seq.sort(key=lambda x: x[0])
        i = 0
        while i < len(seq):
            if seq[i][1] != "TRIP":
                i += 1
                continue
            t0 = seq[i][0]
            grp = [x for x in seq[i:] if x[0] <= t0 + FIVE]
            if not any(x[1] == "LOCKOUT" for x in grp) or any(x[1] == "CLOSE" for x in grp):
                events.append((t0, dev))
            j = i + len(grp)
            while j < len(seq) and seq[j][1] != "TRIP":
                j += 1
            i = j
    events.sort()
    ep_index = {c: ([e[0] for e in eps], eps) for c, eps in episodes.items()}
    last = {}
    mom = collections.Counter()
    for t0, dev in events:
        d = day(t0)
        tm = t0 - t0 % 60000
        n = 0
        for c in below(dev, d):
            if c in ep_index:
                st_, eps = ep_index[c]
                i = bisect.bisect_right(st_, t0 + FIVE) - 1
                hit = False
                while i >= 0:
                    a, b, k = eps[i]
                    if a < tm and t0 < b:
                        hit = True
                        break
                    if tm <= a <= t0 + FIVE:
                        hit = True
                        break
                    if b < t0 - 86400000 * 40:
                        break
                    i -= 1
                if hit:
                    continue
            if c in last and t0 - last[c] <= FIVE:
                continue
            last[c] = t0
            n += 1
        if inwin(d):
            mom[feeder_of(dev, d)] += n
    wrong = []
    for f, v in F["feeders"].items():
        s = round(cmi[f] / nt[f], 1)
        m = round(mom[f] / nt[f], 2)
        if nt[f] != v["nt"] or abs(s - v["saidi"]) > 1e-9 or abs(m - v["maifi"]) > 1e-9 or cemi[f] != v["cemi"]:
            wrong.append((f, nt[f], v["nt"], s, v["saidi"], m, v["maifi"], cemi[f], v["cemi"]))
    check("every feeder's SAIDI, MAIFI-E, CEMI-2 and customers served, recomputed customer by customer", not wrong, wrong[:4])
    # a negative control: the OMS's own counts summed without merging episodes give other SAIDI figures
    naive = collections.Counter()
    for dev, kind, a, b, st, n in tickets:
        if kind != "SCADA" and inwin(day(a)):
            naive[feeder_of(dev, day(a))] += (n or 0) * (b - a) / 60000
    missed = sum(1 for f, v in F["feeders"].items() if round(naive[f] / nt[f], 1) != v["saidi"])
    check("negative control: the OMS's counts times durations miss SAIDI on half the feeders or more", missed >= 8,
          missed)
    # ------------------------------------------------------------ the call
    rel = []
    for r in table("protection/feeder_relay_events_2025_2026.csv"):
        t = t_utc(r["utc_time"])
        if dt.date(2026, 8, 1) <= day(t) <= dt.date(2026, 10, 31):
            rel.append((nb(r["relay"]), t, r))
    rel.sort(key=lambda x: (x[0], x[1]))
    recs = []
    by_dev = collections.defaultdict(list)
    for dev, t, r in rel:
        by_dev[dev].append((t, r))
    mom_set = {(dev, t0) for t0, dev in events}
    ev_by_dev = collections.defaultdict(list)
    for t0, dev in events:
        ev_by_dev[dev].append(t0)
    for dev, xs in by_dev.items():
        evs = sorted(ev_by_dev.get(dev, []))
        for t, r in xs:
            if r["shot"] != "0":
                continue
            i = bisect.bisect_left(evs, t - 2000)
            if i < len(evs) and evs[i] <= t + 2000:
                ph = r["event_type"].split()[0]
                ph = ph[:-1] if ph.endswith("G") and len(ph) == 2 else ph
                cur = max(int(r["i%s_a" % p.lower()]) for p in ph)
                recs.append((feeder_of(dev, day(t)), dev, ph, cur, day(t)))
    for dev, seq in logs.items():
        evs = set(t0 for t0 in ev_by_dev.get(dev, []))
        phasing = at(dev, dt.date(2026, 10, 31))[2]["terminal_phasing"].split("-")
        for t, e, r in seq:
            if e == "TRIP" and t in evs and dt.date(2026, 8, 1) <= day(t) <= dt.date(2026, 10, 31):
                terms = [int(x) for x in r["fault_terminals"].replace("-G", "").split("-")]
                ph = "".join(sorted(phasing[k - 1] for k in terms))
                recs.append((feeder_of(dev, day(t)), dev, ph, int(round(float(r["fault_ka"]) * 1000)), day(t)))
    best = collections.Counter()
    grp = collections.defaultdict(list)
    for f, dev, ph, cur, d in recs:
        grp[(f, dev, ph)].append((cur, d))
    for (f, dev, ph), xs in grp.items():
        xs.sort()
        for i in range(len(xs)):
            best[f] = max(best[f], len({d for c, d in xs if xs[i][0] <= c <= xs[i][0] * 1.04}))
    order = sorted(best, key=lambda f: -best[f])
    check("the call and the runner-up", order[:2] == [F["call"], F["runner_up"]], order[:3])
    check("the two group sizes", (best[order[0]], best[order[1]]) == (F["call_group"]["n"], F["ru_group"]["n"]),
          (best[order[0]], best[order[1]]))
    # ------------------------------------------------------------ the goldens read back
    wb = openpyxl.load_workbook(os.path.join(TASK, "golden", "line_patrol_2026-11-09.xlsx"), read_only=True)
    s1 = {r[0]: r[1] for r in wb["Patrol assignment"].iter_rows(min_row=4, values_only=True) if r[0]}
    wb.close()
    check("golden workbook names the patrol feeder and the second choice", s1.get("Patrol feeder") == F["call"]
          and s1.get("Second choice") == F["runner_up"])
    svg = open(os.path.join(TASK, "golden", "reliability_2026.svg")).read()
    check("golden chart marks the patrol feeder and plots every feeder", "%s, patrol from 9 November" % F["call"] in svg
          and all(f in svg for f in F["feeders"]))
    for label, good, detail in OUT:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [" + detail + "]") if not good else ""))
    fails = [o for o in OUT if not o[1]]
    print("verify: %d checks, %d failed" % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
