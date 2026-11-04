"""The ask layer's ceiling on the cut pack (supplemental-stumping Part 5). Two responses, each scored figure by figure
against the golden at the prompt's rounding:

  cracker  lands the call (the dockets' previous delivery for every distillate load), runs the hygiene battery
           (shadow rows and cancelled transactions out, the dockets' UTC converted, the stock account's 06:00 dips
           rolled back to midnight on the terminal's clock), walks the diesel header through the shift log's change entries
           (read on their shift date and time, as the log prints them), takes the transfers from the log's meter
           readings, and executes the protocol's tank method on the tank register's seals; it never opens the VRU
           controller's event log.
  mirror   stops at the field's per-product loading equation (rung 0) and works the asks the same careful way.

Scoring on 38 (the call and its components), 7 (instruction following) and 55 (the asks, equal weight per figure):
C = 38 + 7 + 55 Lc for the cracker, S = r + 7 + 55 Ls for the mirror, r its share of the call's figures.

    python3 task461/generator/ceiling.py task461/target
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G   # noqa: E402
import world as W    # noqa: E402


def r1(v):
    return round(v, 1)


def sheet(target):
    gold = G.compute(target)
    # ------------------------------------------------ the asks, the careful route
    crack_gain, _ = G.stock_account(target, night_shift_dates=False, with_returns=False, dip_offset=False)
    crack_tank = G.tank_voc(target, seal_history=False)
    rows = []
    for tk in W.TANKS:
        for qi in range(1, 5):
            gv, cv = round(gold["gain"][(tk, qi)]), round(crack_gain[(tk, qi)])
            rows.append(("A", "%s Q%d gain (kL)" % (tk, qi), cv, gv, cv == gv))
    for tk in W.TANKS:
        gv, cv = round(gold["tanks"][tk]), round(crack_tank[tk])
        rows.append(("B", "%s 2026 VOC (kg)" % tk, cv, gv, cv == gv))
    keep = sum(1 for r in rows if r[4]) / len(rows)
    by_ask = {}
    for a in ("A", "B"):
        rr = [r for r in rows if r[0] == a]
        by_ask[a] = (sum(1 for r in rr if r[4]), len(rr))
    # ------------------------------------------------ the call, the mirror's share
    r0 = gold["load"]["R0"]
    main = []
    for qi in range(1, 5):
        main.append(("VRU-1 Q%d" % qi, True))
        for bay in (4, 5):
            main.append(("BAY-%d Q%d" % (bay, qi), r1(r0.get((bay, qi), 0.0)) == r1(gold["quarters"][("BAY-%d" % bay, qi)])))
    mirror_total = sum(r0.values()) + sum(gold["stack"].values())
    main += [("total", r1(mirror_total) == r1(gold["total"])), ("exceeded", (mirror_total > W.LIMIT_T) == gold["over"]),
             ("excess", False), ("distillate bays", False), ("switched volume", False), ("VRU-1 year", True)]
    r = 38.0 * sum(1 for _, k in main if k) / len(main)
    cracker = 38 + 7 + 55 * keep
    mirror = r + 7 + 55 * keep
    return dict(rows=rows, keep=keep, by_ask=by_ask, cracker=cracker, mirror=mirror, r=r,
                pair=(cracker + mirror) / 2, mirror_leakage=100 * keep, mirror_total=mirror_total)


def main(target):
    s = sheet(target)
    print("| Ask figure | Cracker (06:00 dips on the terminal clock, calendar-dated header changes, no VRU-1 returns, the register's current seals and vents) | Golden | Cracker |")
    print("|---|---|---|---|")
    for a, name, cv, gv, hit in s["rows"]:
        print("| %s: %s | %s | %s | %s |" % (a, name, cv, gv, "hit" if hit else "miss"))
    for a, (k, n) in s["by_ask"].items():
        print("ask %s: the cracker keeps %d of %d" % (a, k, n))
    print("Pair ceiling: %.1f (cracker %.1f on the call, mirror %.1f off it at %.1f t; r %.1f)" % (
        s["pair"], s["cracker"], s["mirror"], s["mirror_total"], s["r"]))
    print("Mirror leakage: %.1f per cent of ask weight" % s["mirror_leakage"])
    return s


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
