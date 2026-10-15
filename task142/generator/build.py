"""Build task142: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task142/generator/build.py              everything
    python3 task142/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)

MANIFEST = [
    (K.EPISODES, "Hospital in the Home episodes admitted 1 April 2024 to 30 September 2026, with separations",
     "Alliance data warehouse (Members' admitted episode returns)", "admissions 2024-04-01 to 2026-09-30",
     "Alliance data office", "2026-10-01"),
    (K.CENSUS, "Hospital in the Home census: each patient's days at home and the day's nurse visits",
     "Alliance census warehouse (nightly load from Members' HITH systems)", "2025-07-01 to 2026-09-30",
     "Alliance data office", "2026-10-01"),
    (K.CROSSWALK, "Program codes used to 30 June 2025 mapped to the July 2025 streams", "Alliance clinical governance",
     "admissions to 2025-06-30", "Alliance data office", "2025-07-01"),
    (K.CAMPUSES, "Members' campus codes with validity dates", "Department campus list, Alliance copy",
     "2019-07-01 onwards", "Alliance data office", "2025-03-03"),
    (K.STREAMDOC, "Program streams and visit schedule", "Alliance clinical governance", "admissions from 2025-07-01",
     "Clinical governance group", "2025-06-16"),
    (K.PATHWAY, "Bone and joint infection at home pathway, Northgate and Westmere", "Alliance clinical governance",
     "from 2026-10-01", "Northgate Health HITH", "2026-08-19"),
    (K.PLANS, "Members' Hospital in the Home operating plans 2026-27, revision 1", "Members' planning returns",
     "2026-07 to 2027-06", "Alliance HITH program office", "2026-10-14"),
    (K.CAPACITY, "In-house visit capacity return, January to March 2027", "Members' roster returns",
     "2027-01-01 to 2027-03-31", "Alliance HITH program office", "2026-10-19"),
    (K.SCHED2, "Bellbird agreement, Schedule 2 (Variation 9): the January to March 2027 block",
     "Executed agreement", "2027-01-01 to 2027-03-31", "Alliance HITH program office", "2026-10-02"),
    (K.SCHED34, "Bellbird agreement, Schedules 3 and 4 (Variation 8): fees, referrals and service levels",
     "Executed agreement", "from 2026-07-01", "Alliance HITH program office", "2026-07-03"),
    (K.BB_VISITS, "Bellbird visit records for the Alliance's patients", "Bellbird platform export",
     "visits 2026-07-01 to 2026-09-30 (Melbourne dates)", "Bellbird Home Nursing", "2026-10-05"),
    (K.PORTAL, "Referrals sent to Bellbird through the Alliance referral portal", "Alliance referral portal",
     "sent 2026-07-01 to 2026-09-30", "Alliance data office", "2026-10-02"),
    (K.REGISTER, "Bellbird intake line log", "Bellbird intake desk", "2026-01-01 to 2026-10-30",
     "Bellbird Home Nursing", "2026-10-30"),
    (K.ACCOUNTS, "Bellbird client accounts for the Alliance and its Members", "Bellbird accounts",
     "current", "Bellbird Home Nursing", "2026-10-05"),
    (K.CALENDAR, "Alliance finance calendar 2026-27 with Victorian public holidays", "Alliance finance",
     "2026-07-01 to 2027-06-30", "Alliance finance", "2026-06-12"),
    (K.DICTIONARY, "Field definitions for these files", "Alliance data office", "this set", "Alliance data office",
     "2026-11-02"),
    (K.SURVEY, "Hospital in the Home patient experience survey 2025-26", "Alliance quality team",
     "discharges 2025-07-01 to 2026-06-30", "Alliance quality team", "2026-08-21"),
    (K.BB_REPORT, "Bellbird service report to the Alliance, 2025-26", "Bellbird Home Nursing",
     "2025-07-01 to 2026-06-30", "Bellbird Home Nursing", "2026-07-28"),
    (K.DECLINED, "Referrals Bellbird declined in 2025-26, with reasons", "Bellbird platform export",
     "2025-07-01 to 2026-06-30", "Bellbird Home Nursing", "2026-07-28"),
]


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or WD.simulate()
    counts = {}
    counts[K.EPISODES] = K.write_csv(p(K.EPISODES), R.EP_COLS, R.episode_rows(W))
    counts[K.CENSUS] = K.write_csv(p(K.CENSUS), R.CEN_COLS, R.census_rows(W))
    counts[K.CROSSWALK] = K.write_csv(p(K.CROSSWALK), R.XW_COLS, R.crosswalk_rows(), crlf=True)
    counts[K.CAMPUSES] = K.write_csv(p(K.CAMPUSES), R.CAMPUS_COLS, R.campus_rows(), crlf=True)
    counts[K.BB_VISITS] = K.write_jsonl(p(K.BB_VISITS), R.BB_COLS, R.bb_rows(W))
    counts[K.PORTAL] = K.write_csv(p(K.PORTAL), R.PORTAL_COLS, R.portal_rows(W))
    counts[K.ACCOUNTS] = K.write_csv(p(K.ACCOUNTS), R.ACC_COLS, R.account_rows())
    counts[K.CALENDAR] = K.write_csv(p(K.CALENDAR), R.CAL_COLS, R.calendar_rows(), crlf=True)
    counts[K.DECLINED] = K.write_csv(p(K.DECLINED), R.DECL_COLS, R.declined_rows())
    DOC.write_schedule2(p(K.SCHED2))
    DOC.write_schedules34(p(K.SCHED34))
    DOC.write_streamdoc(p(K.STREAMDOC))
    DOC.write_pathway(p(K.PATHWAY))
    DOC.write_plans(p(K.PLANS), W)
    DOC.write_capacity(p(K.CAPACITY), W)
    DOC.write_register(p(K.REGISTER), W)
    DOC.write_dictionary(p(K.DICTIONARY))
    DOC.write_survey(p(K.SURVEY))
    DOC.write_bb_report(p(K.BB_REPORT))
    P = K.PEOPLE
    PP.normalize_docx(p(K.PATHWAY), P["ng_num"], P["ng_num"], "2026-07-28T03:12:00Z", "2026-08-19T05:41:00Z",
                      revision=7, total_time=163, seed="task142/pathway", title="Bone and joint infection at home pathway",
                      company=K.ALLIANCE)
    PP.normalize_ooxml(p(K.PLANS), P["requester"], P["requester"], "2025-05-20T23:31:16Z", "2026-10-14T04:08:52Z",
                       excel=True, company=K.ALLIANCE)
    PP.normalize_ooxml(p(K.CAPACITY), P["requester"], P["requester"], "2025-09-30T22:14:03Z", "2026-10-19T01:52:29Z",
                       excel=True, company=K.ALLIANCE)
    PP.normalize_ooxml(p(K.REGISTER), "Bellbird Intake", "Bellbird Intake", "2025-12-22T21:05:44Z",
                       "2026-10-30T06:17:58Z", excel=True, company=K.PROVIDER)
    PP.normalize_ooxml(p(K.DICTIONARY), P["data"], P["data"], "2025-08-04T00:21:37Z", "2026-11-01T23:46:11Z",
                       excel=True, company=K.ALLIANCE)
    PP.normalize_ooxml(p(K.SURVEY), "Quality Team", "Quality Team", "2025-10-08T02:44:19Z", "2026-08-21T05:03:35Z",
                       excel=True, company=K.ALLIANCE)
    PP.normalize_pdf(p(K.SCHED2), b"D:20261002143107+10'00'", b"D:20261002143107+10'00'")
    PP.normalize_pdf(p(K.SCHED34), b"D:20260703101844+10'00'", b"D:20260703101844+10'00'")
    PP.normalize_pdf(p(K.STREAMDOC), b"D:20250616152230+10'00'", b"D:20250616152912+10'00'")
    PP.normalize_pdf(p(K.BB_REPORT), b"D:20260728113356+10'00'", b"D:20260728113356+10'00'")
    sizes = sizes_of(out, counts, W)
    rows = []
    for f, what, src, cover, by, on in MANIFEST:
        rows.append({"file": f, "contents": what, "source_system": src, "covers": cover, "prepared_by": by,
                     "prepared_on": on, "rows_or_pages": sizes[f]})
    counts[K.MANIFEST] = K.write_csv(p(K.MANIFEST), R.MAN_COLS, rows, crlf=True)
    stamp = K.PACK_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    W.counts = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return W


def _n(k, word):
    return "%d %s%s" % (k, word, "" if k == 1 else "s")


def sizes_of(out, counts, W):
    """The manifest's rows_or_pages: the rows of each data file (a workbook's table rows, below its header and above
    any totals or notes; the plans, a sheet a Member) and the pages of each document."""
    import re
    import zipfile
    from pypdf import PdfReader
    got = {f: _n(n, "row") for f, n in counts.items()}
    for f in os.listdir(out):
        path = os.path.join(out, f)
        if f.endswith(".pdf"):
            got[f] = _n(len(PdfReader(path).pages), "page")
        elif f.endswith(".docx"):
            with zipfile.ZipFile(path) as z:
                pages = re.search(r"<Pages>(\d+)</Pages>", z.read("docProps/app.xml").decode()).group(1)
            got[f] = _n(int(pages), "page")
    got[K.PLANS] = _n(len(K.MEMBERS), "sheet")
    got[K.CAPACITY] = _n(len(K.MEMBERS), "row")
    got[K.REGISTER] = _n(len(W.reg), "row")
    got[K.DICTIONARY] = _n(len(DOC.DICT), "row")
    got[K.SURVEY] = _n(len(K.MEMBERS) * 4, "row")
    return got


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = (2026, 11, 3, 9, 14, 0)
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
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
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
