"""Search the world seeds for a ladder that holds: the ash-anchored balance names a three whose line clears the fourth,
the subsidence route and the level-aligned cores name the three compression units, equal total mass a clay-rich three,
the fixed depth none of the golden three as a set, and every wrong route's line clears its fourth."""
import sys

import common as K
import world as W

GOLD = {c for c, r in W.ROLE_OF.items() if r in ("G", "B1", "B2")}
COMP = {c for c, r in W.ROLE_OF.items() if r in ("D", "A", "F3")}
CLAY = {c for c, r in W.ROLE_OF.items() if r in ("C", "F2", "F6")}
G1 = [c for c, r in W.ROLE_OF.items() if r == "G"][0]


def score(seed):
    w = W.World(seed)
    L, ur = W.ladder(w)
    ok = (set(L["ash"]["top3"]) == GOLD and set(L["subsidence"]["top3"]) == COMP and set(L["level"]["top3"]) == COMP
          and set(L["mass"]["top3"]) == CLAY and set(L["fixed"]["top3"]) != GOLD
          and L["subsidence"]["order"].index(G1) in (3, 4))
    m = min(L["ash"]["line"] / 1.30, L["subsidence"]["line"] / 1.15, L["level"]["line"] / 1.15,
            L["mass"]["line"] / 1.15)
    return ok, m, L, ur


if __name__ == "__main__":
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, 40)
    good = []
    for s in range(lo, hi):
        ok, m, L, ur = score(s)
        tag = "OK" if ok else "--"
        print(s, tag, "margin %.3f" % m, " ".join("%s %.2f" % (k, L[k]["line"]) for k in ("ash", "subsidence",
                                                                                             "level", "mass")),
              "G1 on subsidence #%d" % (L["subsidence"]["order"].index(G1) + 1), flush=True)
        if ok:
            good.append((m, s))
    good.sort(reverse=True)
    print("best:", good[:8])
