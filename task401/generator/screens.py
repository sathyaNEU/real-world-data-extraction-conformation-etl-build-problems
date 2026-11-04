"""The five go/no-go screens and the coordinator's added readers over redraws of the world (clean truth).
Usage: python3 screens.py [runs] [first_seed]. Prints one line a seed and a summary; checks.py reads summary()."""
import sys

import numpy as np

import readers as R
import world as Wd


def screen_seed(seed, params=None):
    w = Wd.World(seed, params)
    truth = w.truth_costs()
    g = R.golden(w)
    fam = R.golden_family(w)
    srt = sorted(g.values())
    top = max(g, key=g.get)
    reach = dict(A=w.sess[2026]['sat'].sum(), B=w.sess[2026]['sat'].sum(),
                 C=((w.sess[2026]['ygi'] == 2) & w.sess[2026]['sat']).sum(),
                 D=(w.sess[2026]['removed'] & w.sess[2026]['sat']).sum(),
                 E=(w.sess[2026]['split'] & w.sess[2026]['sat']).sum())
    pp = {k: g[k] / max(reach[k], 1) for k in g}
    ic, z = R.interaction_readers(w)
    cons = R.constructing_readers(w)
    runner = sorted(g, key=g.get)[-2]
    return dict(seed=seed, truth=truth, truth_top=max(truth, key=truth.get), golden=g, top=top,
                margin=(g['B'] / srt[-2]) if top == 'B' else 0.0, runner=runner,
                family_all_B=all(max(x, key=x.get) == 'B' for _, x in fam),
                family_B=[x['B'] for _, x in fam], family_runner=[sorted(x, key=x.get)[-2] for _, x in fam],
                first_look=R.first_look(w), careful=R.careful(w), interaction=ic, z=z, constructing=cons,
                literal=R.literal(w), per_pupil_top=max(pp, key=pp.get),
                mean=(w.sess[2025]['total'][w.sess[2025]['sat']].mean(), w.sess[2026]['total'][w.sess[2026]['sat']].mean()))


def summary(runs=20, first=0, params=None, verbose=False):
    rows = [screen_seed(s, params) for s in range(first, first + runs)]
    S = dict(runs=runs,
             truth_B=sum(r['truth_top'] == 'B' for r in rows),
             golden_B=sum(r['top'] == 'B' for r in rows),
             margin_min=min(r['margin'] for r in rows), margin_med=float(np.median([r['margin'] for r in rows])),
             margin_15=sum(r['margin'] >= 1.5 for r in rows),
             family_B=sum(r['family_all_B'] for r in rows),
             runner_A=sum(r['runner'] == 'A' for r in rows),
             first_look_wrong=sum(r['first_look'] != 'B' for r in rows),
             careful_wrong=sum(r['careful'] != 'B' for r in rows),
             interaction_wrong=sum(all(c != 'B' for c in r['interaction']) for r in rows),
             z_min=min(r['z'] for r in rows), z_max=max(r['z'] for r in rows),
             construct_i_wrong=sum(r['constructing'][0][1] != 'B' for r in rows),
             construct_ii_wrong=sum(r['constructing'][1][1] != 'B' for r in rows),
             literal_wrong=sum(all(x != 'B' for x in r['literal']) for r in rows),
             per_pupil_B=sum(r['per_pupil_top'] == 'B' for r in rows))
    if verbose:
        for r in rows:
            print('s%2d truth %s gold %s runner %s fam %s | FL %s CR %s INT %s z %.1f | CON %s | LIT %s | pp %s | mean %.1f->%.1f' % (
                r['seed'], r['truth'], {k: int(v) for k, v in r['golden'].items()}, r['runner'], r['family_all_B'],
                r['first_look'], r['careful'], r['interaction'], r['z'],
                [(a, b, round(c, 2)) for a, b, c in r['constructing']], r['literal'], r['per_pupil_top'], *r['mean']))
    return S, rows


if __name__ == '__main__':
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    first = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    S, _ = summary(runs, first, verbose=True)
    print(S)
    if len(sys.argv) > 3:
        import json
        json.dump({k: (float(v) if not isinstance(v, int) else v) for k, v in S.items()}, open(sys.argv[3], 'w'), indent=1)
