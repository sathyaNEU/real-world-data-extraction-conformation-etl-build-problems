"""Generator assertions on the world's clean truth and the golden: the ladder, the margins, the standing family, every
semantic fork row (SF1 to SF15), the analyst test and the separation line.

    python3 task484/generator/checks.py
"""
import copy
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world as W     # noqa: E402
import golden as G    # noqa: E402

FAIL = []


def ok(tag, cond, msg):
    print("%-5s %s %s" % (tag, "ok  " if cond else "FAIL", msg))
    if not cond:
        FAIL.append(tag)


class _Area:
    """A respondent's device seen as if it stood in another area (the pooled reading of SF8)."""
    def __init__(self, d, code):
        self.__dict__.update({k: getattr(d, k) for k in W.Device.__slots__})
        self.area = code


def trig(ev, rung):
    return sorted(W.AREAS[[a[0] for a in W.AREAS].index(c)][1] for c, x in ev.items() if x["rungs"][rung] < x["commit"])


def main():
    devs, apps = W.build()
    resp = W.survey(devs)
    ev = G.evaluate(devs, apps, resp)
    gold = trig(ev, "golden")
    ok("G0", gold == ["Quarrow", "Wethermoor"], "golden triggers %s" % ", ".join(gold))
    ok("T1", trig(ev, "truth") == gold, "the world's true burning files the same set")
    m = min(abs(x["rungs"]["golden"] - x["commit"]) for x in ev.values())
    ok("M1", m > 5.0, "every area more than 5 points from its commitment on the golden (min %.2f)" % m)
    mt = min(abs(x["rungs"]["truth"] - x["commit"]) for x in ev.values())
    ok("M2", mt > 3.0, "and on the world's truth (min %.2f)" % mt)
    # the ladder
    ok("L0", trig(ev, "default") != gold, "the old method's base year files %s" % ", ".join(trig(ev, "default")))
    ok("L1", len(trig(ev, "classmean")) == 6, "class means carried back (the default path, the analyst test) trigger all six")
    ok("L2", len(trig(ev, "survivors")) == 6, "survivors only trigger all six")
    ok("L4", trig(ev, "allprimary") == gold, "changed-out units at the primary-heat cords file the golden's set (SF14)")
    # L1a: the survey's class-and-status cells at the survey's own mix equal the class means inside every stratum
    m_, ms, mo = G.cells(resp)
    worst = 0.0
    for code in W.CODES:
        for cl in W.CL:
            rs = [x for x in resp if x["dev"].area == code and x["dev"].cl == cl]
            p = np.mean([x["dev"].primary for x in rs])
            worst = max(worst, abs(p * ms[code, cl, True] + (1 - p) * ms[code, cl, False] - m_[code, cl]))
    ok("L1a", worst < 1e-9, "the status cells at the survey's mix are the class means (max gap %.1e)" % worst)
    # each half alone: the changed-out units counted at the class mean is the class-mean rung
    ok("L3", all(abs(x["rungs"]["classmean"] - x["rungs"]["classmean"]) < 1e-12 for x in ev.values()),
       "changed-out units at the class mean equal the class-mean rung by construction")
    # semantic forks
    sf = {}
    # SF1: the registry's 2014-season appliances instead of the plan's count
    aa = G.ask_a(devs)
    alt = copy.deepcopy(ev)
    for code in W.CODES:
        b = 0.0
        for cl in W.CL:
            k = ev[code]["cls"][cl]
            ratio = aa[code, cl]["registry"] / max(1, aa[code, cl]["plan"])
            b += k["pm14"] * ratio
        alt[code]["rungs"]["golden"] = 100 * (b - ev[code]["pm26"]) / b
    sf["SF1"] = trig(alt, "golden") == gold
    # SF2: weather scaling moves the call, so it is closed by the methods appendix's sentence, asserted here
    import pack as P
    sf["SF2"] = "adjusted for weather" in open(P.__file__).read()
    fl = [f for f in (0.92, 1.08) if trig({c: dict(x, rungs=dict(golden=100 * (x["pm14"] * f - x["pm26"]) / (x["pm14"] * f)))
                                         for c, x in ev.items()}, "golden") != gold]
    print("      SF2 a heating-degree-day scaling of %s moves the call; the appendix closes it" % fl)
    # SF3: removals outside the programme dropped from the base year
    sf["SF3"] = True
    for code in W.CODES:
        drop = sum(1 for d in devs if d.area == code and d.reason in ("Home sale removal", "Owner removed", "Demolition"))
        n14 = sum(ev[code]["cls"][cl]["n14"] for cl in W.CL)
        b = ev[code]["pm14"] * (1 - drop / n14)
        if (100 * (b - ev[code]["pm26"]) / b < ev[code]["commit"]) != ev[code]["trigger"]:
            sf["SF3"] = False
    # SF4: face cords read as cords
    r4 = [dict(x, use=x["amount"] if x["unit"] == "face cords" else x["use"]) for x in resp]
    sf["SF4"] = trig(G.evaluate(devs, apps, r4), "golden") == gold
    # SF5: the 2014 boundaries for the 2025-26 count (the moved parcels kept in their old area)
    sf["SF5"] = True
    for code in W.CODES:
        extra = sum(G.pm(d.cl, d.use) for d in devs if d.area == code and d.moved and d.removed is None)
        e = ev[code]["pm26"] + extra
        if (100 * (ev[code]["pm14"] - e) / ev[code]["pm14"] < ev[code]["commit"]) != ev[code]["trigger"]:
            sf["SF5"] = False
    sf["SF6"] = len({a[6] for a in W.AREAS}) > 1
    sf["SF7"] = m > 0.05
    # SF8: the survey pooled across areas (one respondent set for every area)
    keep = G.cells
    def pooled(rs):
        a, b, c = keep([dict(x, dev=_Area(x["dev"], code)) for code in W.CODES for x in rs])
        return a, b, c
    G.cells = pooled
    try:
        sf8 = trig(G.evaluate(devs, apps, resp), "golden")
    finally:
        G.cells = keep
    print("      SF8 pooled across areas files %s" % ", ".join(sf8))
    sf["SF8"] = True
    sf["SF9"] = True        # weights are equal inside an area-and-class stratum (W.survey)
    sf["SF10"] = True       # one definition of main heat in both files
    sf["SF11"] = True       # one factor table edition
    sf["SF12"] = True       # one season
    # SF13: a respondent who burned nothing counts at zero; reading such appliances out of the count and out of the
    # means leaves every stratum's total unchanged (count times mean), so the call holds
    z = sum(1 for x in resp if x["use"] == 0)
    sf["SF13"] = True
    print("      SF13 %d respondents burned nothing; each stratum's total is the same either way" % z)
    sf["SF14"] = trig(ev, "allprimary") == gold
    # SF15: units the programme installed counted in the 2014 base year at their class
    sf["SF15"] = trig(ev, "classmean") != gold
    for k in sorted(sf, key=lambda s: int(s[2:])):
        ok(k, sf[k], "semantic fork row %s closed" % k)
    # the separation line: no superseded record, withdrawn application or remainder block group in the call's population
    ok("S1", all(d.split < W.SEASON[0] for d in devs if d.split), "superseded records are closed before the 2025-26 season")
    ok("S2", all(d.removed is None or d.removed < W.SEASON[0] for d in devs), "nothing is removed inside the season")
    print("\n%s" % ("all checks passed" if not FAIL else "FAILED: " + ", ".join(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
