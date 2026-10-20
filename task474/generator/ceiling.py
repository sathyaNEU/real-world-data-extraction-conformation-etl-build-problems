"""The pair ceiling on Part 0's weights (38 recommendation and critical components, 7 instructions, 55 asks), with the
cracker and the mirror each run as code.

The cracker lands the call (the golden's allocation, five-year averages and 2020-2022 figures) and runs the careful
path on the asks: it dedups the twice-received upload, keeps services dated in FY2026, reads the extract's town for
each row, counts distinct client numbers per agency and council, and sums the energy assistance amounts on the rows. The mirror stops at the most attractive wrong rung on the main block (each rung
tried, the best kept) and takes the same ask path. A figure is a hit at the asking sentence's rounding.

    python3 ceiling.py            scored on the generator's own copies (design stage)
    python3 ceiling.py --pack DIR scored on a cut pack, through verify.py's own readers
"""
import sys

import methods as M
import world as W

W_MAIN, W_INSTR, W_ASKS = 38.0, 7.0, 55.0


def main_figures(ser):
    s = M.summary(ser)
    out = {}
    for r in W.REGION_NAMES:
        out["amount." + r] = M.rnd(s["amount"][r], M.ROUND_AMOUNT)
        out["avg." + r] = M.rnd(s["avg"][r], M.ROUND_PEOPLE)
        for y in W.LEGACY_YEARS:
            out["y%d.%s" % (y, r)] = M.rnd(ser[r][y], M.ROUND_PEOPLE)
    return out


def ask_figures(res):
    out = {}
    for r in W.REGION_NAMES:
        out["carry." + r] = M.rnd(res["carry"][r], 100)
        out["people." + r] = int(res["people"][r])
        out["energy." + r] = M.rnd(res["energy"][r], 100)
    return out


def careful_ask_path(balances=None):
    """The cracker's ask path, executed on the rows the pack ships: everything the extract invites, nothing it does
    not (the resent upload dropped, FY2026 by service date, the extract's town and client numbers as they stand, the
    energy assistance amounts on the rows)."""
    import asks as A
    import askpaths as AP
    import pack as P
    return AP.figures(P.extract_rows(), P.audit_rows(), P.conversion_rows(), balances or A.BALANCES,
                      **AP.STOPS["careful"])


def score(gold, got):
    keys = list(gold)
    hits = sum(1 for k in keys if got.get(k) == gold[k])
    return hits, len(keys)


def run(verbose=True):
    import asks as A
    routes = M.routes()
    gold_main = main_figures(routes["G"])
    gold_ask = ask_figures(A.golden())
    crack_ask = ask_figures(careful_ask_path())
    ah, an = score(gold_ask, crack_ask)
    cracker = W_MAIN + W_INSTR + W_ASKS * ah / an
    best = None
    for name, ser in routes.items():
        if name in M.GOLDEN_FAMILY + ("G_piece",):
            continue
        mh, mn = score(gold_main, main_figures(ser))
        # the call itself (the nine amounts as one allocation) is one criterion the mirror misses
        s = W_MAIN * (mh / (mn + 1)) + W_INSTR + W_ASKS * ah / an
        if verbose:
            print("  mirror %-22s main %2d/%d  score %.1f" % (name, mh, mn, s))
        if best is None or s > best[1]:
            best = (name, s, mh, mn)
    pair = (cracker + best[1]) / 2
    leak = 100.0 * ah / an
    if verbose:
        print("cracker: main %d/%d, asks %d/%d -> %.1f" % (len(gold_main), len(gold_main), ah, an, cracker))
        for k in sorted(gold_ask):
            if crack_ask.get(k) == gold_ask[k]:
                print("   cracker keeps", k, gold_ask[k])
        print("best mirror: %s %.1f (main %d/%d)" % best[:1] + (best[1], best[2], best[3]) if False else
              "best mirror: %s %.1f (main %d/%d)" % (best[0], best[1], best[2], best[3]))
        print("mirror leakage: %.1f per cent of ask weight" % leak)
        print("pair ceiling: %.1f" % pair)
    return dict(pair=pair, cracker=cracker, mirror=best, leak=leak, ask_hits=ah, ask_n=an)


if __name__ == "__main__":
    run()
