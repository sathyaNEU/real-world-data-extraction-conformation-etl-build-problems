"""The pair ceiling on the cut pack (supplemental-stumping Part 0 and 5): modelled responses scored on 38, 7 and 55.

    python3 task307/generator/ceiling.py

Three ask blocks of seven unit figures: A generation, B starts, C trips, each since the start of 2016. Three silent
devices: S the old historian's slot wiring before each station's RTU replacement (moves A and B), Q the restarts inside
one clock hour after a quick trip, which the hourly record cannot show and the governors count (moves B), and L the
line trips that disconnect every unit generating at the station, logged against the line alone (moves C).
cracker: lands the call (pitting per hour in the restricted band) and runs the battery: the two exports stacked on UTC
         with the overlap counted once and the autumn hours kept, the old tags through the 2023 tag map as given, starts
         read from the hourly record, trips as the units' own breaker trips in the protection log
mirror:  the default path's call (pitting per running hour, the peaker set aside), the same battery on the asks
Every ask figure is scored against the golden, a hit being the golden's value at the stated rounding.
"""
import hashlib
import json
import os
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'battery'
HANDLING = {  # name: (series swap, starts mode, trips mode)
    'battery': ('map', 'hourly', 'unit_rows'),
    'S only (slots re-assigned)': ('golden', 'hourly', 'unit_rows'),
    'Q only (quick restarts added)': ('map', 'golden', 'unit_rows'),
    'L only (line trips on the units generating)': ('map', 'hourly', 'golden'),
    'S and Q': ('golden', 'golden', 'unit_rows'),
    'S and L': ('golden', 'hourly', 'golden'),
    'Q and L': ('map', 'golden', 'golden'),
    'all three (full includer)': ('golden', 'golden', 'golden'),
    'over-handler: every unit trip added to the starts': ('golden', 'all', 'golden'),
    'over-handler: line trips on every unit of the station': ('golden', 'golden', 'station_all'),
    'over-handler: every protection-operated row a trip': ('golden', 'golden', 'operated_rows'),
}


def ask_hits(D, F, handling, cache):
    swap, sm, tm = HANDLING[handling]
    if swap not in cache:
        cache[swap] = V.series(D, swap=swap)[0]
    gen, starts, trips = V.asks(cache[swap], D, starts_mode=sm, trips_mode=tm)
    A = F['asks']
    blocks = {
        'A': sum(V.rnd(gen[u], 100) == A['generation_2016_2026_mwh'][u] for u in A['generation_2016_2026_mwh']),
        'B': sum(starts[u] == A['starts_2016_2026'][u] for u in A['starts_2016_2026']),
        'C': sum(trips[u] == A['trips_2016_2026'][u] for u in A['trips_2016_2026']),
    }
    return blocks, sum(blocks.values()), 3 * len(A['generation_2016_2026_mwh'])


def total(on, kept):
    return (38 if on else 5) + 7 + 55 * kept


def main():
    D = V.load()
    F = json.load(open(os.path.join(HERE, 'figures.json'), encoding='utf-8'))
    digest = hashlib.sha256(open(os.path.join(os.path.dirname(HERE), 'target.zip'), 'rb').read()).hexdigest()[:12]
    cache = {}
    S_map = V.series(D, swap='map')[0]
    print('pack target.zip sha256 %s' % digest)
    picks = {}
    for name, mode in (('cracker', 'rz'), ('mirror', 'run')):
        rows, order = V.call(D, S_map, mode)
        picks[name] = order[0]
        print('%-8s call %s (%s)' % (name, order[0], 'on' if order[0] == F['call']['chosen'] else 'off'))
    keep = {}
    for h in HANDLING:
        blocks, hits, n = ask_hits(D, F, h, cache)
        keep[h] = hits / n
        print('asks, %-56s A %d/7, B %d/7, C %d/7: %2d of %d kept (%.1f per cent)' % (h, blocks['A'], blocks['B'], blocks['C'],
                                                                                    hits, n, 100 * hits / n))
    on_c = picks['cracker'] == F['call']['chosen']
    on_m = picks['mirror'] == F['call']['chosen']
    pair = (total(on_c, keep[BASE]) + total(on_m, keep[BASE])) / 2
    single = max(keep[h] for h in ('S only (slots re-assigned)', 'Q only (quick restarts added)',
                                   'L only (line trips on the units generating)'))
    full = keep['all three (full includer)']
    print('cracker %.1f, mirror %.1f, pair on the battery: %.1f' % (total(on_c, keep[BASE]), total(on_m, keep[BASE]), pair))
    print('largest share one device keeps: %.1f per cent of ask weight' % (100 * single))
    print('pair, both on one single finding, one on the call: %.1f' % ((total(True, single) + total(False, single)) / 2))
    two = max(keep[h] for h in ('S and Q', 'S and L', 'Q and L'))
    print('pair, the cracker on two findings (%.1f per cent), the mirror on one: %.1f'
          % (100 * two, (total(True, two) + total(False, single)) / 2))
    print('pair, one full includer on the call, the mirror on the battery: %.1f' % ((total(True, full) + total(False, keep[BASE])) / 2))
    print('pair, both full includers, one on the call: %.1f' % ((total(True, full) + total(False, full)) / 2))
    print('pair, both on the call, each on one single finding: %.1f' % total(True, single))
    ceil = max((total(True, single) + total(False, single)) / 2, (total(True, two) + total(False, single)) / 2,
               (total(True, full) + total(False, keep[BASE])) / 2)
    print('Pair ceiling: %.1f (the worst of: each on one finding, the cracker on two and the mirror on one, one full '
          'includer beside the battery mirror)' % ceil)
    print('Mirror leakage: %.1f per cent of ask weight' % (100 * keep[BASE]))
    # the ask ladder's other stops on generation
    for label, kw in (('natural read (tag map, overlap twice)', dict(swap='map', overlap='twice')),
                      ('over-cleaner (tag map, local labels de-duplicated)', dict(swap='map', dst='label')),
                      ('slots re-assigned, overlap twice', dict(swap='golden', overlap='twice'))):
        S = V.series(D, **kw)[0]
        gen = V.asks(S)[0]
        hits = sum(V.rnd(gen[u], 100) == F['asks']['generation_2016_2026_mwh'][u] for u in gen)
        print('stop: %-52s A %d of 7' % (label, hits))


if __name__ == '__main__':
    main()
