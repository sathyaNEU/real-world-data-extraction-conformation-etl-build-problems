"""The pair ceiling. The cracker lands the call (each area built from its block groups' counts, cut groups split by
census-day housing units) and reads the asks the careful way: meals by the provider responsible for the client, each
code at its meals, the duplicated client-day items collapsed to one (the hygiene reflex), and active clients by the
provider area of their block, the state's deaths joined on the roster's registry number. The mirror stops at the block
sum and reads the asks the same way. Weights 38 / 7 / 55: each of the twelve census counts 38/12; each of the twelve
service figures 55/12. The sensitivity lines add one find at a time.

    python3 task486/generator/ceiling.py     exit 0 at 40 or under
"""
import sys

import asks as A
import methods as M
import world as W
from bundle import Bundle

W_CALL, W_INSTR, W_ASK = 38.0 / 12, 7.0, 55.0 / 12


def call_keep(b, route):
    n = 0
    for which in ("60", "75"):
        g = M.area_counts(b.blocks, b.rel, "bg_hu", which)
        r = M.area_counts(b.blocks, b.rel, route, which, b.points)
        n += sum(M.r10(r[a]) == M.r10(g[a]) for a in W.AREAS)
    return n


def ask_keep(b, meals_kw, active_kw):
    gm, ga = A.meals(b.deliveries, b.clients), A.active(b.clients, b.episodes, b.links, b.deaths)
    m = A.meals(b.deliveries, b.clients, **meals_kw)
    a = A.active(b.clients, b.episodes, b.links, b.deaths, **active_kw)
    return sum(m[x] == gm[x] for x in W.AREAS) + sum(a[x] == ga[x] for x in W.AREAS)


CAREFUL = (dict(dedup="all"), dict(chain=False))
LADDER = [("+ the two-meal plan (replays collapsed, second meals kept)", (dict(), dict(chain=False))),
          ("+ the registry's earlier numbers", (dict(dedup="all"), dict())),
          ("+ both (the golden)", (dict(), dict()))]


def main(quiet=False):
    b = Bundle()
    mirror_call = W_CALL * call_keep(b, "block_sum")
    base = ask_keep(b, *CAREFUL)
    cracker = 38.0 + W_INSTR + W_ASK * base
    mirror = mirror_call + W_INSTR + W_ASK * base
    pair = (cracker + mirror) / 2
    if not quiet:
        print("the mirror (block sum) keeps %d of the 12 census counts" % call_keep(b, "block_sum"))
        print("the careful service reading keeps %d of 12 service figures" % base)
        print("cracker %.2f, mirror %.2f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
            cracker, mirror, pair, 100.0 * base / 12))
        for lab, kw in LADDER:
            k = ask_keep(b, *kw)
            c2 = 38.0 + W_INSTR + W_ASK * k
            m2 = mirror_call + W_INSTR + W_ASK * k
            print("sensitivity %s: keeps %d of 12; cracker %.1f, pair %.1f with the mirror reading carefully, "
                  "%.1f with both finding it" % (lab, k, c2, (c2 + mirror) / 2, (c2 + m2) / 2))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
