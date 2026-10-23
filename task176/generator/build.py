"""Build task176: the evidence pack into <task>/target, the golden workbook into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build
into a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task176/generator/build.py              everything
    python3 task176/generator/build.py --pack-only  the pack, golden and write-up, no checks"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C      # noqa: E402

TASK = os.path.dirname(HERE)
ZIP_STAMP = (2027, 1, 12, 16, 40, 0)
MTIME = calendar.timegm((2027, 1, 12, 21, 40, 0, 0, 0, 0))


def supply_stats(homes):
    at = dt.date(2026, 9, 30)
    yr0 = dt.date(2025, 10, 1)
    regs = {r: dict(homes=0, places=0, opened=0, closed=0) for r in C.REGIONS}
    gopen = gaw = 0
    for h in homes:
        reg = C.COUNTY_REGION[h.county]
        if h.lic <= at and (h.close is None or h.close > at):
            regs[reg]["homes"] += 1
            regs[reg]["places"] += h.cap
            if h.grant:
                gopen += 1
        if yr0 <= h.lic <= at:
            regs[reg]["opened"] += 1
        if h.close is not None and yr0 <= h.close <= at:
            regs[reg]["closed"] += 1
        if h.grant:
            gaw += 1
    tot = {k: sum(regs[r][k] for r in regs) for k in ("homes", "places", "opened", "closed")}
    return dict(regions=regs, total=tot, grant_awards=gaw, grant_open=gopen)


def write_pack(out):
    import asks as A
    import docs as D
    import pack as P
    import postprocess as PP
    import tables as T
    import world as W
    os.makedirs(out, exist_ok=True)
    homes = W.simulate()
    ident = P.Identity(homes)
    n = {}
    n[C.F_LIC] = P.write_licences(os.path.join(out, C.F_LIC), homes, ident)
    n[C.F_XW] = P.write_crosswalk(os.path.join(out, C.F_XW), homes, ident)
    n[C.F_WS] = P.write_worksheets(os.path.join(out, C.F_WS), homes, ident)
    n[C.F_GRANT] = T.write_grants(os.path.join(out, C.F_GRANT), P.grant_rows(homes, ident))
    cc = A.Ccap(homes, ident)
    n[C.F_CCAP] = C.write_csv(os.path.join(out, C.F_CCAP), A.CCAP_HEAD, A.ccap_rows(cc))
    cf = A.Cacfp(homes, ident)
    n[C.F_CACFP] = C.write_csv(os.path.join(out, C.F_CACFP), A.CACFP_HEAD, A.cacfp_rows(cf))
    vs = A.Visits(homes, ident)
    n[C.F_VIS] = C.write_csv(os.path.join(out, C.F_VIS), A.VIS_HEAD, A.visit_rows(vs))
    n[C.F_CTY] = P.write_lookup(os.path.join(out, C.F_CTY))
    n[C.F_QRIS] = T.write_qris(os.path.join(out, C.F_QRIS), homes, ident)
    n[C.F_MRS] = T.write_market_rates(os.path.join(out, C.F_MRS))
    D.write_rules(os.path.join(out, C.F_RULES))
    D.write_policy(os.path.join(out, C.F_POL))
    D.write_supply(os.path.join(out, C.F_SUP), supply_stats(homes))
    T.write_dictionary(os.path.join(out, C.F_DICT))
    T.write_manifest(os.path.join(out, C.F_MAN), n)
    for f, who, when in ((C.F_GRANT, "Grants Management", "2027-01-06T15:02:00Z"),
                         (C.F_MRS, "Supply and Planning", "2025-08-14T18:20:00Z")):
        PP.stamp_ooxml(os.path.join(out, f), who, who, when, when, company=C.DEPT)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return n, dict(homes=homes, ident=ident, ccap=cc, cacfp=cf, visits=vs)


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
            zi = zipfile.ZipInfo(f, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def full(root, quiet=False):
    target = os.path.join(root, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n, world = write_pack(target)
    if not quiet:
        for f in sorted(os.listdir(target)):
            print("  %-48s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), ("%d rows" % n[f]) if f in n else ""))
    gen = os.path.join(root, "generator") if root != TASK else HERE
    os.makedirs(gen, exist_ok=True)
    if os.path.exists(os.path.join(HERE, "deliver.py")):
        import deliver
        import metadata
        if os.path.isdir(os.path.join(root, "golden")):
            shutil.rmtree(os.path.join(root, "golden"))
        deliver.main(target, os.path.join(root, "golden"), os.path.join(gen, "figures.json"),
                     os.path.join(root, "submission.md"))
        metadata.write(root)
    return world


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-only", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    full(TASK)
    if a.pack_only:
        return
    target = os.path.join(TASK, "target")
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    if r1.returncode or r2.returncode:
        sys.exit("checks %d verify %d" % (r1.returncode, r2.returncode))
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="t176_rebuild_")
        try:
            full(tmp, quiet=True)
            mine = {k: v for k, v in digest(TASK).items() if k.split(os.sep)[0] in ("target", "golden")
                    or k in ("submission.md", "metadata.json", os.path.join("generator", "figures.json"))}
            theirs = digest(tmp)
            diff = [k for k in mine if mine[k] != theirs.get(k)]
            print("rebuild: %d files compared, %d differ%s" % (len(mine), len(diff), (": " + ", ".join(diff)) if diff else ""))
            if diff:
                sys.exit(1)
        finally:
            shutil.rmtree(tmp)
    print("zip:", cut_zip(TASK))


if __name__ == "__main__":
    main()
