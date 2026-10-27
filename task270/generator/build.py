"""Build task270: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks, the independent verifier and the cracker, then a second
full build into a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task270/generator/build.py              everything
    python3 task270/generator/build.py --scratch    the pack and goldens only, into the folders the environment names"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = time.mktime((2027, 1, 20, 16, 40, 0, 0, 0, -1))   # the afternoon the paper's analysis was pulled together
PDF_STAMPS = {K.F_STANDARD: (b"D:20261012101500+01'00'", b"D:20261012104200+01'00'"),
              K.F_DBTSTD: (b"D:20260706143000+01'00'", b"D:20260706151100+01'00'"),
              K.F_LDREPORT: (b"D:20250627092000+01'00'", b"D:20250627093400+01'00'"),
              K.F_PILOT: (b"D:20251203112500+00'00'", b"D:20251203115800+00'00'")}


def write_index(out, everyone):
    """The patient index extract: each patient number with its NHS number and date of birth."""
    rows = []
    for num, nhs, dob in everyone:
        rows.append([num, nhs, dob.strftime("%d/%m/%Y")])
    rows.sort(key=lambda z: z[0])
    with open(os.path.join(out, K.F_INDEX), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["patient_number", "nhs_number", "date_of_birth"])
        w.writerows(rows)
    return {K.F_INDEX: len(rows)}


def build_world():
    import hub
    import staff
    import world
    patients, extra = world.build()
    used = {p.number for p in patients + extra}
    hub_pts, refs = hub.build(used)
    people = staff.build()
    nhs, everyone = {}, []
    r = K.rng("index")
    for num in sorted({p.number for p in patients + extra} | {p.number for p in hub_pts}):
        n = K.nhs_number(r)
        while n in nhs.values():
            n = K.nhs_number(r)
        nhs[num] = n
        dob = dt.date(1958, 1, 1) + dt.timedelta(days=int(r.integers(0, 17000)))
        everyone.append((num, n, dob))
    return patients, extra, hub_pts, refs, people, nhs, everyone


def build_pack(out, golden, figs, sub):
    import deliver
    import docs
    import hub
    import postprocess as PP
    import records
    import staff
    os.makedirs(out, exist_ok=True)
    patients, extra, hub_pts, refs, people, nhs, everyone = build_world()
    n = {}
    prompts = records.prompt_rows(patients, extra)
    n.update(records.write_exports(out, prompts))
    n.update(records.write_enrolments(out, patients, extra))
    n.update(records.write_register(out, patients, extra))
    n.update(records.write_episodes(out, patients, extra, hub_pts))
    n.update(records.write_phq(out, patients, extra))
    n.update(hub.write_all(out, refs, nhs))
    n.update(write_index(out, everyone))
    n.update(staff.write_all(out, people))
    docs.write_pdfs(out, people)
    docs.write_paper(os.path.join(out, K.F_PAPER))
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(K.F_REGISTER), "Psychological Therapies Team", K.PEOPLE["director"], "2026-01-05T08:52:00Z",
                       "2027-01-06T15:31:00Z", excel=True, company=K.TRUST)
    PP.normalize_ooxml(p(K.F_CATALOGUE), "Learning and Development", "Learning and Development", "2025-03-20T10:14:00Z",
                       "2026-09-02T13:47:00Z", excel=True, company=K.TRUST)
    PP.normalize_docx(p(K.F_PAPER), K.PEOPLE["director"], K.PEOPLE["director"], "2027-01-14T09:05:00Z",
                      "2027-01-21T11:40:00Z", 7, 214, "paper270", company=K.TRUST)
    for f, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(p(f), c, m)
    for f in os.listdir(out):
        os.utime(p(f), (MTIME, MTIME))
    deliver.main(out, golden, figs, sub)
    return n


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip():
    target = os.path.join(TASK, "target")
    zpath = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 1, 20, 16, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", action="store_true")
    ap.add_argument("--quick", action="store_true", help="the pack and goldens only, no checks or second build")
    a = ap.parse_args()
    if a.scratch:
        root = os.path.dirname(K.TARGET)
        build_pack(K.TARGET, K.GOLDEN, os.path.join(root, "figures.json"), os.path.join(root, "submission.md"))
        return 0
    for d in (K.TARGET, K.GOLDEN):
        if os.path.isdir(d):
            shutil.rmtree(d)
    n = build_pack(K.TARGET, K.GOLDEN, os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    for f in sorted(os.listdir(K.TARGET)):
        print("  %-60s %10d bytes %s" % (f, os.path.getsize(os.path.join(K.TARGET, f)),
                                         ("%d rows" % n[f]) if f in n else ""))
    import metadata
    metadata.write(TASK)
    if a.quick:
        return 0
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")], capture_output=True, text=True)
    print("\n".join(l for l in r1.stdout.splitlines() if not l.startswith("PASS")))
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")])
    r3 = subprocess.run([sys.executable, os.path.join(HERE, "cracker.py")], capture_output=True, text=True)
    print(r3.stdout.splitlines()[-1] if r3.stdout else r3.stderr[-400:])
    tmp = tempfile.mkdtemp(prefix="b270_", dir=TASK)
    try:
        env = dict(os.environ, TASK270_TARGET=os.path.join(tmp, "target"), TASK270_GOLDEN=os.path.join(tmp, "golden"))
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "--scratch"], env=env, check=True)
        same = digest(K.TARGET) == digest(os.path.join(tmp, "target"))
        same_g = digest(K.GOLDEN) == digest(os.path.join(tmp, "golden"))
        same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
        same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"), "rb").read()
        print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
    finally:
        shutil.rmtree(tmp)
    z = cut_zip()
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    return 1 if (r1.returncode or r2.returncode or r3.returncode or not (same and same_g and same_f and same_s)) else 0


if __name__ == "__main__":
    sys.exit(main())
