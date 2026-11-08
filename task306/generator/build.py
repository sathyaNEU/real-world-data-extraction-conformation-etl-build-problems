"""Build task306's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip, then run the checks and the verifier.

    python3 task306/generator/build.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import docs as DC    # noqa: E402
import golden as GD  # noqa: E402
import pack as PK    # noqa: E402
import world as W    # noqa: E402

STAMP = (2027, 1, 6, 8, 30, 0)
SOURCES = {
    "programme": "the federation's medicines safety programme specification agreed with the integrated care board",
    "protocols": "the federation's deprescribing review search and review protocols",
    "closeout": "the pharmacist team's pilot close-out report",
    "pilot": "the pharmacist team's deprescribing outcome log",
    "register": "the federation's member practice register",
    "registrations": "the linked registration history extract (pseudonymised)",
    "courses": "the practices' clinical systems' repeat medication courses extract",
    "issues": "the practices' clinical systems' prescription issue extract",
    "problems": "the practices' clinical systems' problem list extract for the protocols' code clusters",
    "letters": "the shared care record's feed of the two trusts' medicine letters",
    "lookup": "the federation's hospital number to pseudonym linkage table",
    "workflow": "the practices' document workflow log of received hospital documents",
    "hub": "the pharmacist hubs' booking system export",
    "groups": "the hub team's group session attendance register",
    "activity": "the practices' clinical systems' pharmacist consultation extract",
    "lists": "the federation's monthly registered list size extract",
    "epact": "the integrated care board's ePACT2 prescribing summary",
    "falls": "the integrated care board's emergency admissions extract for falls in people aged 65 and over",
}
DATES = {"programme": "2026-11-18", "protocols": "2025-12-08", "closeout": "2027-01-05", "epact": "2026-11-20"}


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    f = lambda k: os.path.join(out, PK.FILES[k])
    T = W.build()
    n = PK.write_data(T, f)
    DC.write_docs(f, out)
    t = __import__("datetime").datetime(*STAMP).timestamp()
    for k in PK.FILES:
        os.utime(f(k), (t, t))
    return n


def metadata(n, fig):
    rows = {k: n[k] for k in n}
    big = max(rows, key=lambda k: rows[k])
    meta = {"task": "task306", "architecture": 5, "as_of": "2027-01-06",
            "files": {PK.FILES[k]: {"source": SOURCES[k], "date": DATES.get(k, "2027-01-06"),
                                    "license": "synthetic, CC0, generated for this task",
                                    "role": "distractor" if k in PK.DISTRACTORS else "evidence"}
                      for k in PK.FILES},
            "distractors": [PK.FILES[k] for k in PK.DISTRACTORS],
            "distractor_notes": {
                PK.FILES["epact"]: "prescribing volume by practice and BNF section; relevant to the size of each "
                                   "review's pool but unused, since eligibility is the protocol's search",
                PK.FILES["falls"]: "falls admissions by network; relevant to harm but unused, since the specification "
                                   "files the harm rates"},
            "largest_file": {"name": PK.FILES[big], "rows": rows[big]},
            "rows": {PK.FILES[k]: rows[k] for k in rows},
            "deliverables": [GD.PAPER, GD.CSV],
            "stated_inputs": {"40.0": "the pilot's six-month off rate for review A, as the close-out report states it"},
            "call": fig["call"], "runner_up": fig["runner_up"], "gap": fig["gap"]}
    return meta


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden = os.path.join(base, "target"), os.path.join(base, "golden")
    n = build_pack(target)
    fig = GD.write_all(target, golden, base)
    json.dump(fig, open(os.path.join(base, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(n, fig), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base), fig


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(prefix="t306a-"), tempfile.mkdtemp(prefix="t306b-")
    ha, fig = one_build(a)
    W._CACHE.clear()
    hb, _ = one_build(b)
    same = ha == hb
    print("two builds byte-identical:", same, "(%d files)" % len(ha))
    if not same:
        for k in sorted(set(ha) | set(hb)):
            if ha.get(k) != hb.get(k):
                print("  differs:", k)
        sys.exit(1)
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.rmtree(a)
    shutil.rmtree(b)
    zp = os.path.join(TASK, "target.zip")
    cut_zip(os.path.join(TASK, "target"), zp)
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    print("call", fig["call"], "runner-up", fig["runner_up"], "gap", fig["gap"])
    for script in ("checks.py", "verify.py"):
        p = os.path.join(HERE, script)
        rc = subprocess.call([sys.executable, p])
        print(script, "exit", rc)
        if rc:
            sys.exit(rc)


if __name__ == "__main__":
    main()
