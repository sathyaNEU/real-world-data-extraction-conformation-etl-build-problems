"""task159 cracker and mirror, run on the cut pack: the pair ceiling and the mirror's leakage.

The cracker lands the call (the backlog behind full trains, the spring's eight-car Line 5), runs the hygiene battery
(keys, duplicates, unmatched joins, units and clocks converted) and executes every filed definition on the fields it
holds: the escalators' directions and speeds from the station elements inventory, the elevators' outages from the
work orders. The mirror stops at the default path (the counted mid-week peaks carried by entries) and is as careful
on the asks. Each response is scored on a rubric modelled on the generated one: the call and its components 35, the
instructions 7, the asks 58 shared equally over every ask figure and the chart's parts.

    python3 cracker.py [target]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C  # noqa: E402

TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")

W_CALL, W_IF, W_ASK = 35.0, 7.0, 58.0
MAIN = [("call", 12.0)] + [("weekday %s" % w, 2.2) for w in C.WD] + [("posted all week", 4.0),
                                                                     ("posted Tuesday to Thursday", 4.0),
                                                                     ("COR-5W not posted", 4.0)]
CHART_PARTS = 2       # both directions drawn for every complex and labelled; the title


def main_score(fc, gold):
    t, per, posts = C.tally(fc)
    gt, gper, gposts = gold
    s = 0.0
    s += 12.0 if t == gt else 0.0
    s += sum(2.2 for w in C.WD if per[w] == gper[w])
    five = sorted(c for c in posts if posts[c] == C.WD)
    gfive = sorted(c for c in gposts if gposts[c] == C.WD)
    three = sorted(c for c in posts if posts[c] == ["Tue", "Wed", "Thu"])
    gthree = sorted(c for c in gposts if gposts[c] == ["Tue", "Wed", "Thu"])
    s += 4.0 if five == gfive else 0.0
    s += 4.0 if three == gthree else 0.0
    s += 4.0 if posts["COR-5W"] == [] else 0.0
    return s


def ask_score(a, b, ga, gb):
    """Figures kept (a hit within half a unit of the stated rounding) and the ask points they carry."""
    n = 14 + 7 + 1 + CHART_PARTS
    per = W_ASK / n
    keep = 0
    rows = []
    ka = sum(1 for cx in C.WATCH_COMPLEXES for i in (0, 1) if abs(a[cx][i] - ga[cx][i]) < 0.5)
    kb = sum(1 for cx in C.WATCH_COMPLEXES if abs(round(b[cx], 1) - round(gb[cx], 1)) < 0.05)
    chart_content = 1 if ka == 14 else 0
    keep = ka + kb + chart_content + CHART_PARTS
    rows.append(("Ask A", ka, 14))
    rows.append(("Ask B", kb, 7))
    rows.append(("chart content", chart_content, 1))
    rows.append(("chart parts", CHART_PARTS, CHART_PARTS))
    return keep * per, rows, keep, n


def main():
    M = C.Model(TARGET)
    gfc = M.forecast()
    gold = C.tally(gfc)
    ga, gb = C.ask_a(TARGET), C.ask_b(TARGET)
    r0 = C.default_path(M)
    routes_a = {"natural": C.ask_a(TARGET, "natural"), "dir_only": C.ask_a(TARGET, "dir_only"),
                "speed_only": C.ask_a(TARGET, "speed_only"), "golden": ga}
    routes_b = {"work_orders": C.ask_b(TARGET, "work_orders"), "monitoring": C.ask_b(TARGET, "monitoring"),
                "golden": gb}
    out = []
    for who, fc in (("cracker", gfc), ("mirror", r0)):
        m = main_score(fc, gold)
        pts, rows, keep, n = ask_score(routes_a["natural"], routes_b["work_orders"], ga, gb)
        total = m + W_IF + pts
        out.append((who, m, pts, total))
        print("%-8s call and components %5.1f of %.0f; instructions %.0f; asks %5.1f of %.0f (%d of %d criteria: %s)"
              " -> %5.1f" % (who, m, W_CALL, W_IF, pts, W_ASK, keep, n,
                             ", ".join("%s %d/%d" % r for r in rows), total))
    pair = (out[0][3] + out[1][3]) / 2
    leak = out[1][2] / W_ASK * 100
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % leak)
    # one device cracked at a time: each ask still needs its second
    m = main_score(gfc, gold)
    worst = 0.0
    for name, ra, rb in (("A1 directions from the controllers' log", "dir_only", "work_orders"),
                         ("A2 speeds from the asset register", "speed_only", "work_orders"),
                         ("B1 faults from the monitoring", "natural", "monitoring")):
        pts, rows, keep, n = ask_score(routes_a[ra], routes_b[rb], ga, gb)
        tot = m + W_IF + pts
        worst = max(worst, (tot + out[1][3]) / 2)
        print("cracker cracking %-40s asks %5.1f (%s) -> %5.1f; pair %5.1f" % (
            name, pts, ", ".join("%s %d/%d" % r for r in rows), tot, (tot + out[1][3]) / 2))
    print("Pair with the most obvious device cracked: %.1f" % worst)
    print("Both top responses on the call, no device cracked: %.1f" % (out[0][3]))
    return pair, leak, worst


if __name__ == "__main__":
    main()
