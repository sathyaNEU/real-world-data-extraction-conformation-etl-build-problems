"""Build task482: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task482/generator/build.py            everything
    python3 task482/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task482/generator/build.py --pack-only
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)


def build_pack(out, e):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["pool"] = P.write_csv(f("pool"), P.POOL_COLS, P.pool_rows(e))
    n["map27"] = P.write_csv(f("map27"), P.MAP27_COLS, P.map27_rows(e))
    n["layout26"] = P.write_csv(f("layout26"), P.LAYOUT_COLS, P.layout26_rows(e))
    n["kts"] = P.write_csv(f("kts"), P.KTS_COLS, P.kts_rows(e), crlf=True)
    n["ng_att"] = P.write_csv(f("ng_att"), P.NG_ATT_COLS, P.ng_att_rows(e))
    n["ng_resp"] = P.write_csv(f("ng_resp"), P.NG_RESP_COLS, P.ng_resp_rows(e))
    n["reports"] = P.write_csv(f("reports"), P.REPORT_COLS, P.report_rows(e))
    n["xwalk"] = P.write_csv(f("xwalk"), P.XWALK_COLS, P.xwalk_rows(e))
    n["centres"] = P.write_csv(f("centres"), P.CENTRE_COLS, P.centre_rows(e))
    n["headcount"] = P.write_csv(f("headcount"), P.HEADCOUNT_COLS, P.headcount_rows(e))
    DC.write_review(f("review"), e)
    DC.write_outcomes(f("outcomes"), e)
    DC.write_report(f("report"), e)
    DC.write_policy(f("policy"))
    DC.write_dictionary(f("dictionary"), n)
    PP.normalize_pdf(f("report"), b"D:20270205093012-06'00'", b"D:20270205093012-06'00'")
    PP.normalize_pdf(f("policy"), b"D:20260626141507-05'00'", b"D:20260626141507-05'00'")
    PP.normalize_pdf(f("dictionary"), b"D:20270204161944-06'00'", b"D:20270204161944-06'00'")
    PP.normalize_ooxml(f("review"), W.PEOPLE["director"], "Office of Assessment and Placement",
                       "2026-04-02T15:10:00Z", "2027-01-29T20:41:37Z", excel=True, company=W.SYSTEM)
    PP.normalize_ooxml(f("outcomes"), "Institutional Research", "Institutional Research", "2027-01-12T16:02:00Z",
                       "2027-01-26T14:55:12Z", excel=True, company=W.SYSTEM)
    return n


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def stamp(folder, when=(2027, 2, 5, 10, 15, 0)):
    import time
    t = time.mktime((*when, 0, 0, -1))
    for root, _, files in os.walk(folder):
        for fn in files:
            os.utime(os.path.join(root, fn), (t, t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args()
    e = W.everything()
    n = build_pack(os.path.join(TASK, "target"), e)
    stamp(os.path.join(TASK, "target"))
    big = max(n.items(), key=lambda t: t[1])
    print("pack: %d files, largest %s (%d rows)" % (len(os.listdir(os.path.join(TASK, "target"))), P.FILES[big[0]], big[1]))
    if a.pack_only:
        return 0
    import golden as G
    import metadata as MD
    import writeup as WU
    G.main(os.path.join(TASK, "target"))
    WU.main()
    MD.write(os.path.join(TASK, "metadata.json"), n)
    stamp(os.path.join(TASK, "golden"), (2027, 2, 9, 16, 40, 0))
    rc = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")]).returncode
    rv = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")]).returncode
    if rc or rv:
        print("checks %d, verify %d" % (rc, rv))
        return 1
    if a.fast:
        return 0
    first = digest(os.path.join(TASK, "target"))
    gfirst = digest(os.path.join(TASK, "golden"))
    e2 = W.everything()
    build_pack(os.path.join(TASK, "target"), e2)
    stamp(os.path.join(TASK, "target"))
    G.main(os.path.join(TASK, "target"))
    stamp(os.path.join(TASK, "golden"), (2027, 2, 9, 16, 40, 0))
    same = first == digest(os.path.join(TASK, "target")) and gfirst == digest(os.path.join(TASK, "golden"))
    print("%s  two consecutive builds byte-identical (target and golden)" % ("PASS" if same else "FAIL"))
    if not same:
        return 1
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(os.path.join(TASK, "target"))):
            zi = zipfile.ZipInfo(fn, date_time=(2027, 2, 5, 10, 15, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(TASK, "target", fn), "rb").read())
    print("zip: %s (%s)" % (zp, hashlib.md5(open(zp, "rb").read()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
