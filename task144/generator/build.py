"""Build task144: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task144/generator/build.py              everything
    python3 task144/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK           # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)

MAN_COLS = ["file", "holds", "system", "period", "extracted_by", "extracted_on", "size"]
MANIFEST = [
    (K.EV25, "Star events (schema v5) of the October 2026 shortlist and of each repository the Sluis lottery "
             "spotlighted, in each repository's first 100 days public", "Grachtwerk events warehouse, star_events_v5",
     "events 2024-12-08 to 2026-03-01", K.PEOPLE["data"], "2026-09-28"),
    (K.EV26, "Star events (schema v6), same repositories", "Grachtwerk events warehouse, star_events",
     "events 2026-03-02 to 2026-09-27", K.PEOPLE["data"], "2026-09-28"),
    (K.ROLLUP, "Daily external first stars by surface for every repository shortlisted for Sluis",
     "Grachtwerk events warehouse, rollup repo_daily_external_stars", "each repository's days 1 to 100, to 2026-09-27",
     K.PEOPLE["data"], "2026-09-28"),
    (K.ACCOUNTS, "Account snapshot", "Grachtwerk accounts service, nightly snapshot", "as at 2026-09-27 23:59 UTC",
     K.PEOPLE["data"], "2026-09-28"),
    (K.MEMBERS, "Organisation memberships of the shortlisted repositories' owners", "Grachtwerk accounts service",
     "as at 2026-09-27", K.PEOPLE["data"], "2026-09-28"),
    (K.REPOS, "Repositories shortlisted for Sluis, January 2025 to October 2026", "Grachtwerk API, repositories",
     "as at 2026-09-27", K.PEOPLE["data"], "2026-09-28"),
    (K.CROSSWALK, "Star surface codes, schema v5 to v6", "Grachtwerk events warehouse documentation", "schema change "
     "of 2026-03-02", K.PEOPLE["data"], "2026-03-02"),
    (K.LOTTERY, "Sluis spotlight lottery log", "Growth team workbook", "issues January 2025 to October 2026",
     K.PEOPLE["growth"], "2026-09-24"),
    (K.MEMO, "Featuring memo: how the spotlight is chosen from October 2026", "Sluis editorial", "from the October "
     "2026 issue", K.PEOPLE["editor"], "2026-09-15"),
    (K.PW_CAMP, "Postwerk campaign report, Grachtwerk account", "Postwerk export", "sends 2026-04-01 to 2026-06-01",
     K.PEOPLE["editor"], "2026-06-03"),
    (K.PW_LINKS, "Postwerk link report by subscriber, Grachtwerk account", "Postwerk export",
     "sends 2026-04-01 to 2026-06-01", K.PEOPLE["editor"], "2026-06-03"),
    (K.RM_CAMP, "Relaymark campaign export, Grachtwerk account", "Relaymark API export", "sends 2026-06-02 to "
     "2026-09-27", K.PEOPLE["editor"], "2026-09-28"),
    (K.RM_LINKS, "Relaymark click log, Grachtwerk account", "Relaymark API export", "clicks to 2026-09-27",
     K.PEOPLE["editor"], "2026-09-28"),
    (K.NOMS, "October 2026 Sluis nomination form responses", "Grachtwerk forms", "2026-09-01 to 2026-09-20",
     K.PEOPLE["editor"], "2026-09-21"),
    (K.RENAMES, "Repository renames in 2026", "Grachtwerk API, repository events", "2026-01-01 to 2026-09-27",
     K.PEOPLE["data"], "2026-09-28"),
    (K.TRAFFIC, "Repository page traffic of the October 2026 shortlist by referrer group", "Grachtwerk traffic "
     "insights", "2026-08-24 to 2026-09-27", K.PEOPLE["data"], "2026-09-28"),
    (K.TRENDING, "Daily trending lists for Go, Python, Rust and TypeScript", "Grachtwerk explore service",
     "2026-08-24 to 2026-09-27", K.PEOPLE["data"], "2026-09-28"),
    (K.DICTIONARY, "Field definitions for these files", "Data engineering", "this extract", K.PEOPLE["data"],
     "2026-09-28"),
]


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or WD.simulate()
    counts = {}
    v5, v6 = R.ev_rows(W)
    counts[K.EV25] = K.write_csv(p(K.EV25), R.EV25_COLS, v5)
    counts[K.EV26] = K.write_csv(p(K.EV26), R.EV26_COLS, v6)
    counts[K.ROLLUP] = K.write_csv(p(K.ROLLUP), R.ROLL_COLS, R.rollup_rows(W))
    counts[K.MEMBERS] = K.write_csv(p(K.MEMBERS), R.MEM_COLS, R.member_rows(W))
    counts[K.CROSSWALK] = K.write_csv(p(K.CROSSWALK), R.XW_COLS, R.crosswalk_rows(), crlf=True)
    repos = R.repo_records(W)
    with open(p(K.REPOS), "w", encoding="utf-8") as fh:
        json.dump(repos, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    counts[K.REPOS] = len(repos)
    # the ask side
    camps = AK.build_sends(W)
    counts[K.PW_CAMP] = _write_semicolon(p(K.PW_CAMP), AK.PW_CAMP_COLS, AK.pw_camp_rows(W, camps))
    counts[K.PW_LINKS] = _write_semicolon(p(K.PW_LINKS), AK.PW_LINK_COLS, AK.pw_link_rows(W, camps))
    rm = AK.rm_campaigns(W, camps)
    with open(p(K.RM_CAMP), "w", encoding="utf-8") as fh:
        json.dump(rm, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    counts[K.RM_CAMP] = len(rm["campaigns"])
    counts[K.RM_LINKS] = K.write_csv(p(K.RM_LINKS), AK.RM_LINK_COLS, AK.rm_link_rows(W, camps))
    counts[K.NOMS] = K.write_csv(p(K.NOMS), AK.NOM_COLS, AK.build_nominations(W), crlf=True)
    counts[K.RENAMES] = K.write_csv(p(K.RENAMES), AK.REN_COLS, AK.rename_rows(W))
    counts[K.TRAFFIC] = K.write_csv(p(K.TRAFFIC), AK.TRAFFIC_COLS, AK.traffic_rows(W))
    counts[K.TRENDING] = K.write_csv(p(K.TRENDING), AK.TRENDING_COLS, AK.trending_rows(W))
    # the account snapshot covers every account the files above name
    counts[K.ACCOUNTS] = R.write_accounts(p(K.ACCOUNTS), W, R.referenced_accounts(W, W.nominator_accounts))
    DOC.write_memo(p(K.MEMO))
    DOC.write_lottery(p(K.LOTTERY), W)
    counts[K.DICTIONARY] = DOC.write_dictionary(p(K.DICTIONARY))
    PP.normalize_ooxml(p(K.LOTTERY), K.PEOPLE["growth"], K.PEOPLE["growth"], "2024-12-11T09:14:52Z",
                       "2026-09-24T13:41:07Z", excel=True, company=K.ORG)
    PP.normalize_pdf(p(K.MEMO), b"D:20260915103412+02'00'", b"D:20260915103412+02'00'")
    sizes = sizes_of(out, counts)
    rows = []
    for f, what, src, cover, by, on in MANIFEST:
        rows.append({"file": f, "holds": what, "system": src, "period": cover, "extracted_by": by,
                     "extracted_on": on, "size": sizes[f]})
    counts[K.MANIFEST] = K.write_csv(p(K.MANIFEST), MAN_COLS, rows, crlf=True)
    stamp = K.PACK_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    W.counts = counts
    W.camps = camps
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return W


def _write_semicolon(path, cols, rows):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\r\n")
    w.writerow(cols)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def _n(k, word):
    return "%d %s%s" % (k, word, "" if k == 1 else "s")


def sizes_of(out, counts):
    from pypdf import PdfReader
    got = {f: _n(n, "row") for f, n in counts.items()}
    got[K.REPOS] = "%d repositories" % counts[K.REPOS]
    got[K.RM_CAMP] = _n(counts[K.RM_CAMP], "campaign")
    got[K.MEMO] = _n(len(PdfReader(os.path.join(out, K.MEMO)).pages), "page")
    got[K.LOTTERY] = "2 sheets"
    got[K.DICTIONARY] = "1 page"
    return got


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = (2026, 9, 28, 8, 42, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(folder, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MDT
    W = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
    MDT.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return W


def main():
    import checks as CK
    import verify as V
    W = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), W=W, meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        same["target.zip"] = open(cut_zip(TASK), "rb").read() == open(cut_zip(tmp), "rb").read()
        if not (same_t and same_g and all(same.values())):
            dt_ = digest(os.path.join(TASK, "target"))
            d2 = digest(os.path.join(tmp, "target"))
            diff = [f for f in dt_ if dt_.get(f) != d2.get(f)]
            raise SystemExit("second build differs: target %s %s, golden %s, %s" % (same_t, diff, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, figures.json and target.zip "
          "(sha256 %s; target.zip sha256 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
