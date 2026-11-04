"""Build task401: the pack into <task>/target and generator/figures.json from the golden solution.

    python3 task401/generator/build.py            cut target/, write figures.json and target.zip
    python3 task401/generator/build.py --out DIR  cut the pack only, into DIR
"""
import argparse, hashlib, json, os, shutil, sys, warnings
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
warnings.filterwarnings('ignore')
import numpy as np  # noqa: E402
import pack, docs, golden, world as W  # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_MTIME = 1792396800      # 2026-10-19 00:00:00 UTC, the pack's export date
MONTHS = ['2024-10', '2024-11', '2024-12', '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07',
          '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03']


def digest(folder):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(folder)):
        h.update(fn.encode()); h.update(open(os.path.join(folder, fn), 'rb').read())
    return h.hexdigest()


def cut(out, seed=W.SEED):
    if os.path.isdir(out):
        shutil.rmtree(out)
    U = pack.cut(out, seed)
    docs.write_all(out, U['snaps'], np.random.default_rng(seed + 77))
    for fn in os.listdir(out):
        os.utime(os.path.join(out, fn), (EXPORT_MTIME, EXPORT_MTIME))
    return U


def make_zip(target):
    import zipfile
    path = os.path.join(TASK, 'target.zip')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 19, 9, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), 'rb').read())
    return path


def figures(target):
    F = golden.solve(target)
    A = F['ask_a']
    fig = dict(
        call=('Thornlea Dairy\'s night-time acid whey discharges, not the aeration control or the works\' capacity: every '
              'exceedance day of the winter fell on the first or second day after one, so pre-treatment at the dairy '
              'reaches them and the nitrification upgrade reaches none'),
        exc_window=F['exc_window'], exc_prior=F['exc_prior'], dairy_reach=F['dairy_reach'], other_reach=F['other'],
        upgrade_reach=F['other'], upgrade_cost_m=14.2, standard_mg_l=0.6,
        exc_by_month_window={m: sum(1 for d in F['exc_days'] if d.startswith(m)) for m in MONTHS[13:]},
        exc_by_month_prior={m: sum(1 for d in F['exc_days_prior'] if d.startswith(m)) for m in MONTHS[1:6]},
        events_window=F['events_window'], fe_on_exc=round(F['fe_on_exc'], 1),
        ask_a={k: dict(volume=int(round(v['volume'])), ot=int(round(v['ot'])), st=int(round(v['st'])),
                       volume_raw=v['volume'], ot_raw=v['ot'], st_raw=v['st'], n=v['n'])
               for k, v in A.items()})
    json.dump(fig, open(os.path.join(HERE, 'figures.json'), 'w'), indent=1, sort_keys=True, default=float)
    return fig, F


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out')
    a = ap.parse_args()
    if a.out:
        cut(a.out); print(digest(a.out)); sys.exit(0)
    target = os.path.join(TASK, 'target')
    cut(target)
    fig, F = figures(target)
    print('target digest', digest(target))
    zp = make_zip(target)
    print('target.zip sha256', hashlib.sha256(open(zp, 'rb').read()).hexdigest())
    print(json.dumps({k: fig[k] for k in ('exc_window', 'exc_prior', 'dairy_reach', 'other_reach', 'events_window', 'fe_on_exc')}))
