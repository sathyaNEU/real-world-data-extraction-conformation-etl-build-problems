"""task401 build: the world, the pack under target/, the golden and the checks, the deliverables, target.zip.

    python3 build.py            full build
    python3 build.py --pack     world and pack only
"""
import os, sys, json, time, zipfile, hashlib, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
import world as W
import pack


def zip_target():
    T = os.path.join(TASK, 'target'); Z = os.path.join(TASK, 'target.zip')
    with zipfile.ZipFile(Z, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(T)):
            zi = zipfile.ZipInfo('target/' + f, date_time=(2026, 3, 16, 9, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(T, f), 'rb').read())
    return hashlib.sha256(open(Z, 'rb').read()).hexdigest()


def main():
    t0 = time.time()
    out, at = W.simulate(W.SEED, W.P0)
    print('world %.0fs' % (time.time() - t0))
    side = pack.write_all(out, at)
    print('pack %.0fs' % (time.time() - t0))
    cache = os.path.join(HERE, '.truth.pkl')
    win = lambda c: int(((c >= W.WIN0) & (c < W.WIN1)).sum())
    truth = {k: win(out['all']['cancel_w']) - win(out['no' + k]['cancel_w']) for k in 'ABCDE'}
    pickle.dump(dict(truth=truth, paid=side['paid'], till=side['till_truth'], house=side['house'],
                     world=dict(cancel_w=out['all']['cancel_w'], jw=at['jw'], legacy=at['legacy'])), open(cache, 'wb'))
    if '--pack' in sys.argv:
        return
    import golden, checks, deliver, writeup, meta
    F = golden.run()
    checks.run(F)
    deliver.run(F)
    writeup.run(F)
    meta.run()
    print('target.zip', zip_target())


if __name__ == '__main__':
    main()
