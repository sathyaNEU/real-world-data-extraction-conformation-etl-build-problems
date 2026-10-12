"""Rebuild task116's evidence pack from the register and the seeded world, then assert it."""
import sys
import time
from pathlib import Path

from reportlab import rl_config

rl_config.invariant = 1

import assemble
import cast
import pack
import seal
from world import Register

TASK = Path(__file__).resolve().parent.parent
TARGET = TASK / "target"


def build(target=TARGET):
    t0 = time.time()
    reg = Register()
    c = cast.Cast(reg).run()
    A = assemble.Assembly(reg, c).build()
    main_roles = ("decoy", "answer", "behind", "contender", "filler", "pilot")
    A.main_uids = set(u for u, r in c.role.items() if r in main_roles)
    A.uid_of = {reg.group_name[u]: u for u in c.pilot}
    A.usage_tweak = {}
    A.on_tallybridge = set()
    out = pack.write(target, reg, A)
    import golden_calc as G
    A.on_tallybridge = set(G.schools_on_tallybridge(G.load(target))["urn"])
    import settle
    rounds = settle.settle(target, reg, A, lambda: pack.write(target, reg, A))
    print("settled in %d rounds" % rounds)
    seal.seal(target)
    print("built %s in %.0fs" % (target, time.time() - t0))
    return reg, c, A, out


if __name__ == "__main__":
    tgt = Path(sys.argv[1]) if len(sys.argv) > 1 else TARGET
    reg, c, A, out = build(tgt)
    import asserts
    asserts.run(tgt, reg, c, A, out)
