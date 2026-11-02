"""Pair ceiling on the cut pack: the cracker (lands the call, runs the hygiene battery) and the mirror (stops at the
default path) scored figure by figure against the golden's ask answers. Weights 38 / 7 / 55 (supplemental Part 0)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def score(golden, route):
    hit = tot = 0
    for k, v in golden.items():
        g = v if isinstance(v, list) else [v]
        r = route[k] if isinstance(route[k], list) else [route[k]]
        for a, b in zip(g, r):
            tot += 1
            hit += int(abs(a - b) < 0.5)
    return hit, tot


def main(target=None):
    target = target or os.path.join(TASK, "target")
    rms, tpo, codes = A.read_rms(target), A.read_tpo(target), A.read_codes(target)
    polys26 = A.read_geojson(target, "patrol_districts_2026.geojson")
    stref = A.read_station_reference()
    fare = A.read_fare_codes(target)
    gt = A.GTFS(target)
    cache = {}
    gold = {"A": A.ask_a(rms, tpo, codes, polys26, stref, fare), "B": A.ask_b(target, codes), "C": A.ask_c(gt, cache=cache)}
    # The cracker: UTC read in Mountain time, reports matched across the two systems, 2025 offences placed by
    # coordinates, calendar exceptions applied, pickups only; codes joined on the published code list alone and
    # the feed's stop_times read without expanding frequencies.txt.
    gt_flat = A.GTFS(target)
    gt_flat.expand = False
    crack = {"A": A.ask_a(rms, tpo, codes, polys26, stref, fare, date_aware=False),
             "B": A.ask_b(target, codes, date_aware=False),
             "C": A.ask_c(gt_flat, cache={})}
    # The full includer: every handling the golden uses except the frequency templates.
    full = {"A": gold["A"], "B": gold["B"], "C": crack["C"]}
    # The mirror: the default path's response; districts as recorded, codes on the published list, no matching of
    # reports referred without a file number, stop_times by service date without frequencies.
    mirror = {"A": A.ask_a(rms, tpo, codes, polys26, stref, fare, redistrict=False, date_aware=False, dedupe=False),
              "B": A.ask_b(target, codes, date_aware=False, local_window=False),
              "C": A.ask_c(gt_flat, by_service_date=True, cache={})}
    out = {"asks": {}}
    tot_all = 0
    keep = {"crack": 0, "full": 0, "mirror": 0}
    for k in ("A", "B", "C"):
        h_c, n = score(gold[k], crack[k])
        h_f, _ = score(gold[k], full[k])
        h_m, _ = score(gold[k], mirror[k])
        out["asks"][k] = {"figures": n, "cracker_hits": h_c, "full_includer_hits": h_f, "mirror_hits": h_m}
        tot_all += n
        keep["crack"] += h_c
        keep["full"] += h_f
        keep["mirror"] += h_m
    Lc = keep["crack"] / tot_all
    Lf = keep["full"] / tot_all
    Ls = keep["mirror"] / tot_all
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    out.update({"ask_figures": tot_all, "cracker_keep": round(Lc, 4), "full_includer_keep": round(Lf, 4),
                "mirror_keep": round(Ls, 4), "landed_score": round(C, 1), "missed_score": round(S, 1),
                "pair_ceiling": round((C + S) / 2, 1),
                "pair_if_both_land": round((C + 38 + 7 + 55 * Ls) / 2, 1),
                "mirror_leakage_pct": round(100 * Ls, 1)})
    json.dump(out, open(os.path.join(HERE, "ceiling.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
