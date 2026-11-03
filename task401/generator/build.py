"""Build task401: the pack into <task>/target and generator/figures.json from the golden solution.

    python3 task401/generator/build.py            cut target/ and write figures.json
    python3 task401/generator/build.py --out DIR  cut the pack only, into DIR
"""
import argparse, hashlib, json, os, shutil, sys, warnings
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
warnings.filterwarnings('ignore')
import pack, docs, golden  # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_MTIME = 1793952000      # 2026-11-06 00:00:00 UTC, the pack's export date


def digest(folder):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(folder)):
        h.update(fn.encode()); h.update(open(os.path.join(folder, fn), 'rb').read())
    return h.hexdigest()


def cut(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    U, _ = pack.cut(out)
    docs.write_all(out)
    for fn in os.listdir(out):
        os.utime(os.path.join(out, fn), (EXPORT_MTIME, EXPORT_MTIME))
    return U


def figures(target):
    F, L = golden.solve(target)
    r1 = lambda v: round(float(v), 1)
    fig = dict(
        call='the May 2025 quote journey relaunch: customers quoted on use they typed or on typical values whose meter '
             'point quantities cost more than their quote',
        share_h1_2025=r1(F['share_h1_2025']), share_h1_2026=r1(F['share_h1_2026']),
        fall_points=r1(F['share_h1_2025'] - F['share_h1_2026']),
        n_2025=F['n_2025'], n_2026=F['n_2026'],
        covered_sat_2025=r1(F['covered_sat_2025']), covered_sat_2026=r1(F['covered_sat_2026']),
        short_share_2025=r1(F['short_share_2025']), short_share_2026=r1(F['short_share_2026']),
        short_sat_2025=r1(F['short_sat_2025']), short_sat_2026=r1(F['short_sat_2026']),
        bridge={k: r1(v) for k, v in F['bridge'].items()},
        quote_share_of_fall_pct=round(100 * F['bridge']['quote'] / (F['share_h1_2025'] - F['share_h1_2026'])),
        ask_a=dict(counts=F['ask_a']['counts'], elec_gwh=round(F['ask_a']['elec_gwh'], 1), gas_gwh=round(F['ask_a']['gas_gwh'], 1),
                   elec_gwh_raw=F['ask_a']['elec_gwh'], gas_gwh_raw=F['ask_a']['gas_gwh']),
        ask_b=F['ask_b'], ask_c=F['ask_c'],
        raw=dict(share_h1_2025=F['share_h1_2025'], share_h1_2026=F['share_h1_2026']))
    json.dump(fig, open(os.path.join(HERE, 'figures.json'), 'w'), indent=1, sort_keys=True, default=float)
    return fig, F, L


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out')
    a = ap.parse_args()
    if a.out:
        cut(a.out); print(digest(a.out)); sys.exit(0)
    target = os.path.join(TASK, 'target')
    cut(target)
    fig, F, L = figures(target)
    print('target digest', digest(target))
    print(json.dumps({k: v for k, v in fig.items() if not k.startswith('ask') and k != 'raw'}, default=float))
