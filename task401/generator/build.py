"""task401 build: the world and staffing, the pack under target/, the golden from target/, the checks, the
deliverables under golden/, submission.md, metadata.json and target.zip.

    python3 build.py            full build
    python3 build.py --pack     world and pack only
"""
import hashlib
import json
import os
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
import pack
import staffing as St
import world as Wd


def zip_target():
    T = os.path.join(TASK, 'target')
    Z = os.path.join(TASK, 'target.zip')
    with zipfile.ZipFile(Z, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(T)):
            zi = zipfile.ZipInfo('target/' + f, date_time=(2026, 6, 15, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(T, f), 'rb').read())
    return hashlib.sha256(open(Z, 'rb').read()).hexdigest()


def main():
    t0 = time.time()
    w = Wd.World()
    st = St.Staffing(w)
    pack.write_all(w, st)
    print('pack %.0fs' % (time.time() - t0))
    if '--pack' in sys.argv:
        return
    import checks
    import deliver
    import golden
    import meta
    import writeup
    F = golden.run()
    F['screens20'] = json.load(open(os.path.join(HERE, 'screens20.json')))
    F['paper'] = dict(max_marks=Wd.PAPER_MAX, secure_mark=Wd.SECURE)
    F = json.loads(json.dumps(F, default=str))
    fails = checks.run(F, w, st)
    json.dump(F, open(os.path.join(HERE, 'figures.json'), 'w'), indent=1, sort_keys=True)
    deliver.run(F)
    writeup.run()
    meta.run()
    print('target.zip', zip_target())
    print('build %.0fs, checks failed: %d' % (time.time() - t0, len(fails)))
    if fails:
        sys.exit(1)


if __name__ == '__main__':
    main()
