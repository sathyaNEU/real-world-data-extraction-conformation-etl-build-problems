"""The salt search: fix the per-stream salts so every graded figure sits inside its bin under every member of the
golden family with room to spare, and the ladder's routes land outside. Run once when the world changes; the chosen
salts are written into world.SALT by hand and asserted by checks.py.

    python3 tune.py [n]       tries n salt pairs for the State Data Center and survey streams
"""
import importlib
import sys

import world as W


def evaluate():
    import sources as S
    import methods as M
    S.SDC_EST = S._sdc()          # the two salted streams; SNAP and the asks do not depend on them
    S.ACS = S._acs()
    R = M.routes()
    out = dict(ok=True, why=[])
    fam_amt = ("G_households",)     # G_piece is ruled out by rule 2.3 (town by town)
    sm = {k: M.summary(v) for k, v in R.items()}
    g = sm["G"]

    def edge(v, unit):
        c = unit * round(v / unit)
        return unit / 2 - abs(v - c)
    worst = 1e9
    for r in W.REGION_NAMES:
        a = g["amount"][r]
        sp = max(abs(sm[k]["amount"][r] - a) for k in fam_amt)
        e = edge(a, M.ROUND_AMOUNT)
        if e < sp + 800:
            out["ok"] = False
            out["why"].append("amount %s edge %.0f spread %.0f" % (r, e, sp))
        worst = min(worst, e - sp)
        av = g["avg"][r]
        sp = max(abs(sm[k]["avg"][r] - av) for k in fam_amt)
        e = edge(av, M.ROUND_PEOPLE)
        if e < sp + 4:
            out["ok"] = False
            out["why"].append("avg %s edge %.1f spread %.1f" % (r, e, sp))
        for y in W.LEGACY_YEARS:
            v = g["series"][r][y]
            sp = abs(sm["G_households"]["series"][r][y] - v)
            e = edge(v, M.ROUND_PEOPLE)
            if e < sp + 2.5:
                out["ok"] = False
                out["why"].append("cell %s %d edge %.1f spread %.1f" % (r, y, e, sp))
    r0 = sum(M.rnd(sm["R0_window"]["amount"][r], M.ROUND_AMOUNT) != M.rnd(g["amount"][r], M.ROUND_AMOUNT)
             for r in W.REGION_NAMES)
    if r0 < 6:
        out["ok"] = False
        out["why"].append("R0 misses only %d amounts" % r0)
    r7 = sum(M.rnd(sm["R7_midpoint"]["amount"][r], M.ROUND_AMOUNT) != M.rnd(g["amount"][r], M.ROUND_AMOUNT)
             for r in W.REGION_NAMES)
    if r7 < 3:
        out["ok"] = False
        out["why"].append("R7 misses only %d amounts" % r7)
    r8 = sum(M.rnd(sm["R8_additive"]["amount"][r], M.ROUND_AMOUNT) != M.rnd(g["amount"][r], M.ROUND_AMOUNT)
             for r in W.REGION_NAMES)
    if r8 < 2:
        out["ok"] = False
        out["why"].append("R8 misses only %d amounts" % r8)
    quiet = max(abs(S.sdc_latest("region", r, 2024) / S.sdc_latest("region", r, 2023) - 1) for r in W.REGION_NAMES)
    if quiet >= 0.02:
        out["ok"] = False
        out["why"].append("a region moves %.1f per cent from 2023 to 2024" % (100 * quiet))
    for k in R:
        if k in M.GOLDEN_FAMILY:          # piece pooling is ruled out by rule 2.2 (SF6); landing the call is welcome
            continue
        hits = sum(M.rnd(sm[k]["amount"][r], M.ROUND_AMOUNT) == M.rnd(g["amount"][r], M.ROUND_AMOUNT)
                   for r in W.REGION_NAMES)
        if hits == 9:
            out["ok"] = False
            out["why"].append("%s lands the call" % k)
    out["r0_misses"] = r0
    out["worst"] = worst
    return out


def asks_ok(n=400):
    """The asks' figures are records-fixed; keep each off its $100 bin edge and the careful path a clear miss in every
    council. The extract's rows and the asks' salt are fixed; the balances' salt is searched (it moves only the
    carry-ins)."""
    import asks as A
    import askpaths as AP
    import ceiling as C
    import pack as P
    e = lambda v, u: u / 2 - abs(v - u * round(v / u))
    ext, aud, conv = P.extract_rows(), P.audit_rows(), P.conversion_rows()
    for j in range(n):
        W.SALT["balances"] = j
        A.BALANCES = A.balances()
        ag = A.golden()
        ck = AP.figures(ext, aud, conv, A.BALANCES, **AP.STOPS["careful"])
        worst = min(e(ag["carry"][g], 100) for g in W.REGION_NAMES)
        gap = min(abs(round(ag["carry"][g], -2) - round(ck["carry"][g], -2)) for g in W.REGION_NAMES)
        pgap = min(abs(ag["people"][g] - ck["people"][g]) for g in W.REGION_NAMES)
        eworst = min(e(ag["energy"][g], 100) for g in W.REGION_NAMES)
        round_bal = any(A.BALANCES[c]["unspent"] % 100 == 0 for c in W.COUNTY_NAMES)
        if worst >= 8 and gap >= 300 and pgap >= 8 and eworst >= 8 and not round_bal:
            print("ASKS FOUND balances salt", j, "carry edge %.1f, carry gap %d, people gap %d, energy edge %.1f" % (
                worst, gap, pgap, eworst))
            return j
    print("none")


def main(n, start=0):
    for i in range(start, n):
        W.SALT.update({"sdc": i // 60, "acs": i % 60})
        res = evaluate()
        print(i, W.SALT, "OK" if res["ok"] else "--", res.get("r0_misses"), round(res.get("worst", 0)),
              "; ".join(res["why"][:3]))
        sys.stdout.flush()
        if res["ok"]:
            print("FOUND", W.SALT)
            return


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "asks":
        asks_ok()
    else:
        main(int(sys.argv[1]) if len(sys.argv) > 1 else 60, int(sys.argv[2]) if len(sys.argv) > 2 else 0)
