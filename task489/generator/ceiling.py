"""The pair ceiling on the cut pack (supplemental-stumping Parts 0, 1.1 and 5), through the verifier's own readers.
The cracker lands the call and takes the careful route on the asks: each logged non-arrival once (by controller
serial and cycle count) on the host's well label over the production days; the survey's bleed readings joined to the
register by pad and tag, makers' ratings otherwise, every stint and isolation the work orders date. The mirror stops
at rung 1 (each separator's liquid over its level band, counted cycles where SCADA counts) and takes the same route
on the asks. Each figure is a hit within the prompt's rounding; planning weights 38 / 7 / 55.

    python3 task489/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verify as V   # noqa: E402


def careful_nonarrivals(B):
    seen, out = set(), {}
    for r in B["cyc"]:
        k = (r["controller_sn"], int(r["cycle_count"]))
        if k in seen:
            continue
        seen.add(k)
        t = V.local(r["valve_open_local"])
        if V.WIN0 <= t < V.WIN1 and r["result"] == "NO ARRIVAL":
            out[r["well"]] = out.get(r["well"], 0) + 1
    return out


def main(target, golden):
    res = V.main(target, golden)
    B = res["B"]
    rows = []
    cn = careful_nonarrivals(B)
    for w in sorted(res["na"]):
        rows.append(("P: %s cycles without an arrival" % w, cn.get(w, 0), res["na"][w]))
    cb = V.bleed_by_maker_area(B, V.bleed(B, "tag"))
    for k in sorted(res["bma"]):
        rows.append(("B: %s, %s (kg)" % k, int(V.rnd(cb.get(k, 0.0))), int(V.rnd(res["bma"][k]))))
    print("| Ask figure | Cracker (logged non-arrivals once by host label; survey by pad and tag) | Golden | Cracker |")
    print("|---|---|---|---|")
    kept = 0
    for name, got, want in rows:
        hit = got == want
        kept += hit
        print("| %s | %s | %s | %s |" % (name, got, want, "hit" if hit else "miss"))
    lc = kept / float(len(rows))
    # the mirror's call components: pads and controllers it gets right at rung 1
    vol_kg = V.lc_kg(B, V.lc_cycles(B, "volume", res["cyc"]))
    vol_t = V.pad_tonnes(B, vol_kg)
    n_main = len(res["kg"]) + len(res["pt"]) + 1
    m_main = sum(1 for k in res["kg"] if int(V.rnd(vol_kg[k])) == int(V.rnd(res["kg"][k]))) + \
        sum(1 for p in res["pt"] if V.rnd(vol_t[p], 2) == V.rnd(res["pt"][p], 2)) + (res["sets"]["volume"] == res["call"])
    r = 38.0 * m_main / n_main
    cr = 38 + 7 + 55 * lc
    mr = r + 7 + 55 * lc
    print("asks: the cracker keeps %d of %d figures" % (kept, len(rows)))
    print("Pair ceiling: %.1f (cracker %.1f on the call, mirror %.1f off it at rung 1, %d of %d call criteria; r %.1f)"
          % ((cr + mr) / 2, cr, mr, m_main, n_main, r))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lc))
    return (cr + mr) / 2, lc


if __name__ == "__main__":
    here = os.path.dirname(HERE)
    main(os.path.join(here, "target"), os.path.join(here, "golden"))
