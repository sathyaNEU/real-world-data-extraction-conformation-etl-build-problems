"""Score the ask layer against the cracker and the mirror, on the cut pack, as code.

The cracker is the one `supplemental-stumping` Part 1.1 defines: the response that landed the call, ran the
hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out, count ties) and **executed
every filed rule it points at**, which here means plan 5.1 for a process figure read off the plant's own
counters, plan 3.1, 3.2, 4.1 and 4.2 for the level and its valid minutes, and plan 4.3 for tonality. It
takes the records at face value: the channel named for the blowers' air is the air, and the quarter hours
the historian did not record are the ones it wrote no row for.

What it does not do is the step no filed sentence performs. The plant's three blowers are metered twice,
because the third was tied into the main downstream of the header's meter, and the records settle it: the
air per cubic metre the works treats holds steady week to week on the two meters together and swings by a
quarter on the header alone, and each counter carries its own rate channel and nothing else. And the
historian holds rows that are the quarter hour before them written again, which its own counters give away
by standing still while the air flows.

The mirror stops at the most attractive wrong rung, the statistical background of the position's own
record, so it loses the construction layer and answers the rest exactly as the cracker does.

Run: python3 cracker.py            (after build.py, from the generator directory)
"""
import csv
import datetime as dt
import json
import os

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"),
                     encoding="utf-8"))

WEEKS = [dt.date(2026, 8, 31) + dt.timedelta(days=7 * i) for i in range(6)]
DAY_START, DAY_END = 7, 19
ASK_WEIGHT = 55.0          # the generated rubric's ask share, points
REC_LANDED = 38.0          # recommendation and critical components, a landed call
REC_MISSED = 5.0           # what a wrong call keeps of them
INSTRUCTION = 7.0


def rows(name):
    with open(os.path.join(T, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def windows():
    """Per position, its weekday assessment windows in local time, off the deployment record."""
    out = {}
    for d in rows("meter_deployments_2026.csv"):
        a = dt.datetime.strptime(d["deployed_at"], "%Y-%m-%d %H:%M")
        b = dt.datetime.strptime(d["collected_at"], "%Y-%m-%d %H:%M")
        for k in range((b.date() - a.date()).days + 1):
            day = a.date() + dt.timedelta(days=k)
            if day.weekday() > 4:
                continue
            lo = dt.datetime(day.year, day.month, day.day, DAY_START)
            hi = dt.datetime(day.year, day.month, day.day, DAY_END)
            if lo >= a and hi <= b:
                out.setdefault(d["position_code"], []).append((lo, hi))
    return out


def historian():
    """The historian's rows by stamp, as the cracker reads them: every row it wrote is a record."""
    out = {}
    for r in rows("scada_15min_2026.csv"):
        out[dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")] = r
    return out


def face_value(hist, lo, hi):
    """The cracker's three figures over a window: the air off the channel named for the blowers, and the
    quarter hours the historian wrote no row for, counted and in their longest run."""
    air = float(hist[hi]["blower_air_total_knm3"]) - float(hist[lo]["blower_air_total_knm3"])
    n, cur, longest = 0, 0, 0
    t = lo + dt.timedelta(minutes=15)
    while t <= hi:
        if t not in hist:
            n += 1
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0
        t += dt.timedelta(minutes=15)
    return air, n, longest


def cracker_positions():
    hist, wins = historian(), windows()
    out = {}
    for code, w in wins.items():
        air, n, longest = 0.0, 0, 0
        for lo, hi in sorted(w):
            a, n2, l2 = face_value(hist, lo, hi)
            air += a
            n += n2
            longest = max(longest, l2)
        out[code] = {"air": round(air, 1), "unrecorded": n, "longest": longest}
    return out


def cracker_weeks():
    hist = historian()
    out = {}
    for i, wk in enumerate(WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        b = a + dt.timedelta(days=7)
        air, n, longest = face_value(hist, a, b)
        out[i] = {"air": int(round(air)), "unrecorded": n, "longest": longest}
    return out


def score():
    cp, cw = cracker_positions(), cracker_weeks()
    gp_air = FIG["blower_air_knm3"]
    gp_unrec = FIG["unrecorded_quarter_hours"]
    gp_run = FIG["longest_unrecorded_run"]
    gw = {int(k): v for k, v in FIG["weekly_plant"].items()}

    asks = []           # (ask figure group, criteria, cracker hits)
    asks.append(("A1 the fourteen specific levels", 14, 14))
    asks.append(("A1 the five, the sixth and the margin", 3, 3))
    asks.append(("A1 the ranked chart", 4, 4))
    asks.append(("A2 the blower air behind each level", 14,
                 sum(1 for c in gp_air if abs(cp[c]["air"] - gp_air[c]) <= 0.05)))
    asks.append(("A2 the blower air, six weeks", 6,
                 sum(1 for i in range(6) if cw[i]["air"] == gw[i]["blower_air_knm3"])))
    asks.append(("A3 the quarter hours not recorded, per position", 14,
                 sum(1 for c in gp_unrec if cp[c]["unrecorded"] == gp_unrec[c])))
    asks.append(("A3 the quarter hours not recorded, six weeks", 6,
                 sum(1 for i in range(6) if cw[i]["unrecorded"] == gw[i]["unrecorded_quarter_hours"])))
    asks.append(("A3 the longest run of them, per position", 14,
                 sum(1 for c in gp_run if cp[c]["longest"] == gp_run[c])))
    asks.append(("A3 the longest run of them, six weeks", 6,
                 sum(1 for i in range(6) if cw[i]["longest"] == gw[i]["longest_unrecorded_run"])))
    asks.append(("A4 the tone summary", 3, 3))

    n = sum(a[1] for a in asks)
    construction = {"A1 the fourteen specific levels", "A1 the five, the sixth and the margin",
                    "A1 the ranked chart"}
    ck = sum(a[2] for a in asks)
    mr = sum(a[2] for a in asks if a[0] not in construction)

    print("%-46s %9s %9s" % ("ask figure group", "criteria", "cracker"))
    for name, crit, h in asks:
        print("%-46s %9d %9s" % (name, crit, "%d hit" % h if h else "all miss"))
    print("%-46s %9d %9d" % ("total", n, ck))
    lc, ls = ck / float(n), mr / float(n)
    C = REC_LANDED + INSTRUCTION + lc * ASK_WEIGHT
    S = REC_MISSED + INSTRUCTION + ls * ASK_WEIGHT
    print("\ncracker: keeps %d of %d ask criteria (%.3f of ask weight) -> %.1f" % (ck, n, lc, C))
    print("   mirror keeps %d (%.3f) -> %.1f;  pair %.1f;  mirror leakage %.1f per cent"
          % (mr, ls, S, (C + S) / 2.0, 100.0 * ls))
    return {"pair": round((C + S) / 2.0, 1), "leakage": round(100.0 * ls, 1), "criteria": n,
            "cracker_keeps": ck, "mirror_keeps": mr,
            "device_rows": [(a[0], a[1], a[2]) for a in asks if a[0] not in construction
                            and not a[0].startswith("A4")]}


if __name__ == "__main__":
    score()
