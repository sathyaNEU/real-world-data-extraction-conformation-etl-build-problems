"""The pair ceiling and mirror leakage, scored on the cut pack (supplemental-stumping Part 0 and 1.1).

Each response is a complete pipeline run on target/; an ask figure is kept when it equals the golden at the asked
rounding (one decimal). The cracker landed the call, ran the hygiene battery (one record per housing unit and quarter,
county 59041 split by ZIP, both code lists) and executed every filed definition on the disposition codes; the mirror
stops at the most attractive wrong rung of the call and handles the asks the same way; the full includer also reads
the frame log, as it stood at each visit.

    python3 task259/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

CALL_ON, CALL_OFF, IF = 38.0, 5.0, 7.0
ASK = 55.0


def kept(r, G):
    hits = sum(round(r[a]["rr"], 1) == round(G[a]["rr"], 1) for a in A.AREAS)
    hits += sum(round(r[a]["nc"], 1) == round(G[a]["nc"], 1) for a in A.AREAS)
    return hits / 16.0


def main():
    L = A.load(os.path.join(os.path.dirname(HERE), "target"))
    G = A.ask_rates(L)
    stops = {
        "filed scope executed, a restore clearing every removal of its unit (cracker and mirror)":
            A.ask_rates(L, frame="unit_void"),
        "codes as recorded, the address file never consulted": A.ask_rates(L, frame="none"),
        "address file read as it stood at the visit": A.ask_rates(L, frame="asof"),
        "address file replayed in date order (full includer)": A.ask_rates(L),
        "rows counted as recorded": A.ask_rates(L, frame="none", dedup=False),
        "county 59041 sent whole to Silver Creek": A.ask_rates(L, split041="03"),
        "golden": G,
    }
    for k, r in stops.items():
        print("%-75s kept %5.1f%%" % (k, 100 * kept(r, G)))
    Lc = kept(stops["filed scope executed, a restore clearing every removal of its unit (cracker and mirror)"], G)
    Ls = Lc
    Lf = kept(stops["address file replayed in date order (full includer)"], G)
    pair = ((CALL_ON + IF + ASK * Lc) + (CALL_OFF + IF + ASK * Ls)) / 2
    pair_full = ((CALL_ON + IF + ASK * Lf) + (CALL_OFF + IF + ASK * Lf)) / 2
    print("Pair ceiling: %.1f" % pair)
    print("Pair ceiling with full includers on both sides: %.1f" % pair_full)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Ls))
    return 0 if pair <= 60 and 100 * Ls < 50 else 1


if __name__ == "__main__":
    sys.exit(main())
