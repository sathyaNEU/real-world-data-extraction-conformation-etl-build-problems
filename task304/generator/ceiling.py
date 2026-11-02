"""task304 architecture 4: the pair ceiling, scored on the cut pack (target/) by running each response's handling stops.

The cracker lands the call, runs the hygiene battery and executes every filed rule: on ask A it reads EP-01 at the asset
list's current pack (five pairs) and every machine at the asset list's current site; on ask B it replays Schedule 3
(retests within 30 days, the confirming retest as the new reference, the hub at the retest from the transfers file).
The mirror stops at the job-based easy route on the call (each title at its zone) and handles the asks as the cracker
does. Scores use the 38 / 7 / 55 weights: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls, r the mirror's share of the main side."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402


def main():
    pk = AN.Pack(os.path.join(TASK, "target"))
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    hubs = AN.HUBS
    tab = pk.exposure_table()
    gold_c = pk.counts(tab)
    r0 = pk.rung_jobbased(tab)
    gold_a = pk.vending()
    gold_b = pk.audiometry()
    # ask rows
    crack_a = pk.vending(site_basis="current", pack_basis="current")
    crack_b = pk.audiometry()                      # Schedule 3 executed as filed
    ask_hits_c = sum(crack_a.get((h, m), 0) == gold_a.get((h, m), 0) for h in hubs for m in (7, 8, 9))
    ask_hits_c += sum(crack_b[h] == gold_b[h] for h in hubs)
    n_ask = 18 + 6
    Lc = ask_hits_c / n_ask
    Ls = Lc                                         # the asks are decoupled from the call
    # the mirror's main side: per-hub figures that happen to coincide under the job-based route, and the call
    main_crit = 2 * len(hubs) + 2                   # every hub's two figures, the hub, the runner-up
    mirror_main = sum((r0[h]["pool"] == gold_c[h]["pool"]) + (r0[h]["below"] == gold_c[h]["below"]) for h in hubs)
    r = 38.0 * mirror_main / main_crit
    C = 38 + 7 + 55 * Lc
    S = r + 7 + 55 * Ls
    pair = (C + S) / 2
    print("ask A cracker hits: %d of 18 (current pack and current site)" % sum(crack_a.get((h, m), 0) == gold_a.get((h, m), 0) for h in hubs for m in (7, 8, 9)))
    print("ask B cracker hits: %d of 6 (Schedule 3 executed)" % sum(crack_b[h] == gold_b[h] for h in hubs))
    print("mirror main-side hits: %d of %d -> r = %.1f" % (mirror_main, main_crit, r))
    print("cracker C = %.1f, mirror S = %.1f" % (C, S))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Ls))
    return pair, 100 * Ls


if __name__ == "__main__":
    main()
