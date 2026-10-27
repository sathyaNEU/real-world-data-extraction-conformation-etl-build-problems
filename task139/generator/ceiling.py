"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out, the
as-of join) and executes every filed rule (contract terms 5, rate manual 6); the mirror stops at the call's most
attractive wrong rung and takes each ask's natural read. Each keeps an ask figure when its handling lands within half a
unit of the figure's rounding (the nearest dollar, a whole contract).

    python3 task139/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks as AK          # noqa: E402
import golden as G         # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
WEIGHT = {"A": 9, "B": 8}


def figures(a, b):
    out = {}
    for q in AK.QA:
        out[('A', q, 'n')] = a[q]['n']
        out[('A', q, 'refund')] = round(a[q]['refund'])
        out[('A', q, 'lien')] = round(a[q]['lien'])
    for q in AK.QB:
        out[('B', q, 'received')] = round(b[q]['received'])
        out[('B', q, 'outstanding')] = round(b[q]['outstanding'])
    return out


def run():
    P = G.read(TARGET)
    gold = figures(AK.ask_a(P, TARGET), AK.ask_b(P, TARGET))
    # the cracker: the first request received cancels (terms 5), a lienholder's payoff request joined on its VIN as of
    # the date received (the contract in force on that VIN); the three bordereau layouts read, cents to dollars, the
    # independents on VIN and day-first sale date, a contract remitted twice kept once, then the bank's returns taken
    # off the payments they match
    crack = figures(AK.ask_a(P, TARGET, 'vin_asof'), AK.ask_b(P, TARGET, 'dedupe_first'))
    # the mirror: the requests that carry a contract number, every bordereau line as received
    mirror = figures(AK.ask_a(P, TARGET, 'drop_unmatched'), AK.ask_b(P, TARGET, 'include_returned'))

    def keep(sheet):
        k = {a: 0 for a in WEIGHT}
        for key, v in sheet.items():
            if abs(v - gold[key]) <= 0.5:
                k[key[0]] += 1
        return k
    kc, km = keep(crack), keep(mirror)
    tot = sum(WEIGHT.values())
    lc = sum(kc.values()) / tot
    ls = sum(km.values()) / tot
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * ls
    return dict(cracker=kc, mirror=km, Lc=lc, Ls=ls, pair=(C + S) / 2, mirror_leak=100 * ls)


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
