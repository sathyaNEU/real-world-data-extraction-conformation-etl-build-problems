"""Build task163: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte and deleted.

    python3 task163/generator/build.py              everything
    python3 task163/generator/build.py --out DIR    the pack only, into DIR
    python3 task163/generator/build.py --zip        also cut target.zip from the pack (at ship)

The company's size is calibrated by a fixed rule: the share multiplier starts at 1 and is rescaled, at most six times,
by the ratio of 2,302 to the midpoint of the plan line's construction family, stopping at the first value within 3 of
2,302 (else the closest). Every business keeps its own random streams whatever the size, so a rescale adds or drops
businesses at the margin and moves nothing else. The rule puts the family inside the central half of its bin at a
non-round value; it never searches seeds."""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as CA           # noqa: E402
import common as K          # noqa: E402
import company as CO        # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
PACK_DONE = (2026, 10, 15, 16, 48, 0)                       # FP&A assembled the pack, Eastern time
MTIME = calendar.timegm((2026, 10, 15, 20, 48, 0, 0, 0, 0))  # the same moment, UTC
TARGET_MID = 2302.0


class MemPack:
    """The October release, the share tab and the change log held in memory in calc's shapes."""

    def __init__(self, W, share):
        pub = R.published(W, "2026-10")
        self.bfs = {}
        for (usps, name, sa, t), v in pub.items():
            key = (usps, name, sa)
            if key not in self.bfs:
                self.bfs[key] = np.full(CA.NMON, np.nan)
            if t < CA.NMON:
                self.bfs[key][t] = v
        self.share = {s: {"count": c, "base": b, "share": c / b} for s, (c, b) in share.items()}
        import datetime as dt
        self.changes = {s: (dt.date(*WD.LAUNCH[s]), dt.date(*WD.RETIRE[s])) for s in WD.REFORM}


def share_table(W, C):
    cnt, base = R.counts_2025(C), R.share_base(W)
    return {s.usps: (cnt[s.usps], base[s.usps]) for s in WD.STATES}


def family_mid(P):
    v = np.array(list(CA.family(P).values()))
    return 0.5 * (v.min() + v.max()), v.min(), v.max()


class Built:
    pass


def world(quiet=True):
    B = Built()
    B.W = WD.simulate()
    scale, best = 1.0, None
    for it in range(7):
        C = CO.build(B.W, scale)
        share = share_table(B.W, C)
        mid, lo, hi = family_mid(MemPack(B.W, share))
        if not quiet:
            print("  calibration %d: scale %.4f, family %.1f to %.1f, midpoint %.1f" % (it, scale, lo, hi, mid))
        if best is None or abs(mid - TARGET_MID) < abs(best[0] - TARGET_MID):
            best = (mid, scale, C, share)
        if abs(mid - TARGET_MID) <= 3 or it == 6:
            break
        scale *= TARGET_MID / mid
    B.mid, B.scale, B.C, B.share = best
    return B


def build_data(out, B):
    p = lambda f: os.path.join(out, f)
    W, C = B.W, B.C
    n = {}
    js, n[R.F_BFS] = R.bfs_json(W)
    with open(p(R.F_BFS), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(js)
    n[R.F_BFS_APR] = K.write_csv(p(R.F_BFS_APR), R.BFS_APR_COLS, R.bfs_april_rows(W))
    n[R.F_ACCOUNTS] = K.write_csv(p(R.F_ACCOUNTS), R.ACCOUNT_COLS, R.account_rows(C))
    n[R.F_XWALK] = K.write_csv(p(R.F_XWALK), R.XWALK_COLS, R.crosswalk_rows(C))
    leg, cur = R.wage_rows(C)
    n[R.F_LEGACY] = K.write_csv(p(R.F_LEGACY), R.LEGACY_COLS, leg, crlf=True)
    n[R.F_WAGES] = K.write_csv(p(R.F_WAGES), R.WAGES_COLS, cur)
    n[R.F_REG] = K.write_csv(p(R.F_REG), R.REG_COLS, R.registration_rows(C))
    n[R.F_SUTA] = K.write_csv(p(R.F_SUTA), R.SUTA_COLS, R.suta_rows(C))
    n[R.F_TERR] = K.write_csv(p(R.F_TERR), R.TERR_COLS, R.territory_rows())
    n[R.F_NES] = K.write_csv(p(R.F_NES), R.NES_COLS, R.nes_rows(W))
    return n


def build(out, quiet=False, B=None):
    os.makedirs(out, exist_ok=True)
    B = B or world(quiet)
    n = build_data(out, B)
    DOC.write_all(out, B.share)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-48s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
                                              ("%d rows" % n[f]) if f in n else ""))
    return B, n


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip(root):
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=PACK_DONE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    B, n = build(target)
    print("  scale %.4f, family midpoint %.1f" % (B.scale, B.mid))
    import json
    with open(os.path.join(HERE, "calibration.json"), "w") as fh:
        json.dump({"scale": B.scale, "family_mid": round(B.mid, 3)}, fh, indent=1)
        fh.write("\n")
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="b163_", dir=TASK)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"),
                         os.path.join(tmp, "submission.md"))
            s1 = digest(target) == digest(os.path.join(tmp, "target"))
            s2 = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            s3 = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"),
                                                                               "rb").read()
            s4 = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"),
                                                                                "rb").read()
            same = s1 and s2 and s3 and s4
            print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (s1, s2, s3, s4))
        finally:
            shutil.rmtree(tmp)
    if a.zip:
        z = cut_zip(TASK)
        print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    if r1.returncode or r2.returncode or not same:
        sys.exit(1)


if __name__ == "__main__":
    main()
