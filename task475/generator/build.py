"""Builds task475 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
generator/figures.json, metadata.json, target.zip and submission.md.

    python3 task475/generator/build.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import warnings
import zipfile

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import deliver as GD  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

SOURCES = {
    "export": "IBCP e-marking platform, export of Paper 2 marks of record for the May and November 2026 series, "
              "pulled 30 November 2026",
    "may_reg": "IBCP legacy examinations system, candidate register for the May 2026 sitting, exported 3 August 2026 "
               "at the portal migration",
    "nov_reg": "IBCP candidate portal, entries for the November 2026 sitting, pulled 30 November 2026",
    "requests": "IBCP candidate portal, candidate request log (API export), 3 August to 30 November 2026",
    "centres": "IBCP Examinations Office, examination centre directory",
    "reviews": "IBCP enquiries CRM, results review requests for the May 2026 sitting",
    "invoices": "IBCP finance system, accounts receivable invoices to corporate accounts, 2026",
    "accounts": "IBCP finance system, corporate account register",
    "regs": "IBCP Council, Certifier Accreditation Examination Regulations, version 3",
    "paper": "IBCP Examinations Office, Paper 2 question paper, November 2026 sitting",
    "minutes": "IBCP Examinations Committee, minutes of the meeting of 18 June 2026 (draft for confirmation)",
    "history": "IBCP Examinations Office, accreditation results by sitting, 2019 to May 2026",
    "venues": "IBCP Examinations Office, venue holds for the 2027 sittings",
}
COVERS = {
    "export": "one row per mark of record entered for a part of a question, both 2026 series",
    "may_reg": "candidates entered for the May 2026 sitting, either paper",
    "nov_reg": "one row per paper entered for the November 2026 sitting",
    "requests": "requests candidates sent through the portal for the November 2026 sitting",
    "centres": "examination centres, open and closed",
    "reviews": "review requests on May 2026 Paper 2 results, with payment details",
    "invoices": "invoices raised to corporate accounts in 2026",
    "accounts": "corporate accounts and their agreed rates",
    "regs": "the examination regulations and the fee schedule",
    "paper": "the November 2026 Paper 2 question paper",
    "minutes": "the May 2026 results meeting",
    "history": "candidates examined and accredited at past sittings",
    "venues": "venues held for the May and November 2027 sittings",
}


def metadata(counts):
    return {
        "task": P.TASK,
        "architecture": 2,
        "as_of": P.ASOF.isoformat(),
        "decision": "the November 2026 Paper 2 results the Examinations Committee approves, each optional question "
                    "moved as the examination regulations require, with the centres' withdrawals, absences and "
                    "May sitters and the May 2026 review outcomes and refunds",
        "deliverables": [P.RESULTS_CSV, P.PAPER_DOCX],
        "files": {P.FILES[k]: {"source": SOURCES[k], "covers": COVERS[k], "date": P.EXPORT_DAY.isoformat(),
                               "license": "synthetic, CC0, built for this task",
                               "role": "distractor" if k in P.DISTRACTORS else "evidence"} for k in P.FILES},
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "distractor_notes": {
            P.FILES["history"]: "candidates examined and accredited at earlier sittings; relevant to the committee's "
                                "view of the sitting, unused by the solution",
            P.FILES["venues"]: "venue holds for the 2027 sittings by centre; relevant to the centres, unused by the "
                               "solution",
        },
        "largest_file": {"name": P.FILES["export"], "rows": counts["export"]},
        "row_counts": {P.FILES[k]: v for k, v in sorted(counts.items())},
    }


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = (os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen"))
    w = W.build()
    counts = pack.build_pack(w, target)
    GD.write_all(target, golden, gen)
    with open(os.path.join(base, "metadata.json"), "w") as fh:
        json.dump(metadata(counts), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=P.STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    da, db = one_build(a), one_build(b)
    if da != db:
        bad = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        print("NOT byte-identical:", bad)
        sys.exit(1)
    print("two builds byte-identical over %d files" % len(da))
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
        for fn in os.listdir(dst):
            st = os.stat(os.path.join(a, sub, fn))
            os.utime(os.path.join(dst, fn), (st.st_mtime, st.st_mtime))
    shutil.copy(os.path.join(a, "gen", "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    import writeup
    writeup.main()
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
