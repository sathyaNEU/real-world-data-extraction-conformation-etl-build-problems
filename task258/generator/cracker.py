"""The cracker and mirror sheets on the cut pack: the cracker lands the call, runs the hygiene battery and executes
every filed rule; on the asks it reads the hero slot off the beacons' own URLs but counts every request served on it
(200 and 304 alike) from the image hosts' log alone, and files each live hero under the DAM's collection column. The
mirror stops at the most attractive wrong rung, the field method (the level and the first-paint floor on every slow
own-image load), and does the asks as the cracker does. Scored figure by figure against generator/figures.json.

    python3 task258/generator/cracker.py"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402

TASK = os.path.dirname(HERE)


def score(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    eg = AN.egress(target, statuses=(200, 304), with_legacy=False)
    heroes = AN.hero_images(target, "property")
    nov = AN.page_loads(target)
    R = AN.rungs(nov, AN.effect(AN.engagement_frame(target)))
    field = {n: round(AN.round_to(R.loc[n, "field"], 1e5) / 1e6, 1) for n in AN.NAMES}
    rows = []
    for n in AN.NAMES:
        rows.append(("A gigabytes %s" % n, AN.round_to(eg[n]["gb"], 1), fig["egress_gb"][n]))
        rows.append(("A dollars %s" % n, AN.round_to(eg[n]["aud"], 1), fig["egress_aud"][n]))
        rows.append(("B hero images %s" % n, heroes[n], fig["hero_images"][n]))
    crack_asks = [(a, got, want, got == want) for a, got, want in rows]
    c_rows = [("C loads moved %s" % n, field[n], fig["loads_moved_m"][n]) for n in AN.NAMES]
    n_ask = len(rows) + len(c_rows) + 1                     # the chart's marked property counts once
    kept_c = sum(r[3] for r in crack_asks) + len(c_rows) + 1  # the cracker lands the call, so Ask C and the chart
    kept_m = sum(r[3] for r in crack_asks) + sum(got == want for _, got, want in c_rows)
    lc, lm = kept_c / n_ask, kept_m / n_ask
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * lm
    return crack_asks, c_rows, lc, lm, (crack + mirror) / 2


if __name__ == "__main__":
    asks, c_rows, lc, lm, pair = score(os.path.join(TASK, "target"))
    for name, got, want, hit in asks:
        print("%-22s cracker %-8s golden %-8s %s" % (name, got, want, "HIT" if hit else "miss"))
    for name, got, want in c_rows:
        print("%-22s mirror  %-8s golden %-8s %s" % (name, got, want, "same" if got == want else "off"))
    print("cracker keeps %.1f per cent of the ask figures (Ask C and the chart only); mirror leakage %.1f per cent; "
          "pair ceiling %.1f" % (100 * lc, 100 * lm, pair))
