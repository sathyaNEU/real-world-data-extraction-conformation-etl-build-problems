"""The pair ceiling on the cut pack (supplemental-stumping Part 0 and 5): two modelled responses scored on 38, 7 and 55.

    python3 task307/generator/ceiling.py

cracker: lands the call (pitting per hour in the restricted band), stacks the two historian exports on UTC with the
         overlap counted once and the autumn hours kept, maps the old tags through the 2023 tag map as given
mirror:  the default path's call (pitting per running hour, the peaker set aside), the same careful ask handling
Every ask figure is scored for both rows against the golden, a hit being the golden's value at the stated rounding.
"""
import hashlib
import json
import os
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))


def score(D, S, mode, F):
    rows, order = V.call(D, S, mode)
    gen, starts = V.asks(S)
    hits, n, detail = 0, 0, []
    for u in F['asks']['generation_2016_2026_mwh']:
        g = V.rnd(gen[u], 100) == F['asks']['generation_2016_2026_mwh'][u]
        s = starts[u] == F['asks']['starts_2016_2026'][u]
        hits += g + s
        n += 2
        detail.append('%s gen %s, starts %s' % (u, 'hit' if g else 'miss', 'hit' if s else 'miss'))
    return order[0], hits, n, detail


def main():
    D = V.load()
    F = json.load(open(os.path.join(HERE, 'figures.json'), encoding='utf-8'))
    digest = hashlib.sha256(open(os.path.join(os.path.dirname(HERE), 'target.zip'), 'rb').read()).hexdigest()[:12]
    S_map, _ = V.series(D, swap='map')
    res = {}
    for name, mode in (('cracker', 'rz'), ('mirror', 'run')):
        pick, hits, n, detail = score(D, S_map, mode, F)
        on = pick == F['call']['chosen']
        L = hits / n
        total = (38 if on else 5) + 7 + 55 * L
        res[name] = (pick, on, hits, n, L, total, detail)
    print('pack target.zip sha256 %s' % digest)
    for name, (pick, on, hits, n, L, total, detail) in res.items():
        print('%-8s call %s (%s), asks %d of %d kept (%.1f per cent), score %.1f' % (name, pick, 'on' if on else 'off', hits, n,
                                                                                     100 * L, total))
        for d in detail:
            print('          ' + d)
    pair = (res['cracker'][5] + res['mirror'][5]) / 2
    # the full includer reads the old slots against the logged outages and re-assigns them before each RTU replacement
    S_full, _ = V.series(D, swap='golden')
    pick, hits, n, _ = score(D, S_full, 'rz', F)
    full = 38 + 7 + 55 * hits / n
    worst = max((full + res['mirror'][5]) / 2, (res['cracker'][5] + 5 + 7 + 55 * hits / n) / 2)
    print('full includer (on the call, slots re-assigned): asks %d of %d kept, score %.1f' % (hits, n, full))
    print('pair, battery cracker and mirror: %.1f' % pair)
    print('pair, one of the two a full includer: %.1f' % worst)
    print('pair, both full includers, one on the call: %.1f' % ((full + 5 + 7 + 55 * hits / n) / 2))
    print('Pair ceiling: %.1f' % max(pair, worst))
    print('Mirror leakage: %.1f per cent of ask weight' % (100 * res['mirror'][4]))
    # the ask ladder's other stops, scored on the asks alone
    for label, kw in (('natural read (tag map, overlap twice)', dict(swap='map', overlap='twice')),
                      ('over-cleaner (tag map, local labels de-duplicated)', dict(swap='map', dst='label')),
                      ('slots re-assigned, overlap twice', dict(swap='golden', overlap='twice')),
                      ('golden handling', dict(swap='golden'))):
        S, _ = V.series(D, **kw)
        _, hits, n, _ = score(D, S, 'rz', F)
        print('stop: %-52s asks %d of %d' % (label, hits, n))


if __name__ == '__main__':
    main()
