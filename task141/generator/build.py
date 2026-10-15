"""Build task141: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task141/generator/build.py              everything
    python3 task141/generator/build.py --out DIR    the pack only, into DIR"""
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
EXPORT_STAMP = dt.datetime(2026, 10, 2, 13, 40, tzinfo=dt.timezone.utc)   # 09:40 in Garrison, the extracts assembled

FILES = [
    (K.DRAFT, "Local bail policy for pretrial release: revision for 2027, draft for consultation of 6 October 2026",
     "Office of the Senior Resident Superior Court Judge"),
    (K.POLICY24, "Local bail policy for pretrial release, effective 1 July 2024", "Office of the Senior Resident "
     "Superior Court Judge"),
    (K.GUIDE, "Pretrial Assessment Scale, version 2: scoring guide", "Dorrance County Pretrial Services"),
    (K.FA_LEGACY, "Initial appearances on new charges, 1 October 2021 to 3 March 2024, one row per appearance",
     "Clerk of Superior Court, legacy court system"),
    (K.FA_NEW, "Initial appearances on new charges, 4 March 2024 to 30 September 2026, one row per appearance",
     "Clerk of Superior Court, case management system"),
    (K.FA_CHARGES, "The charges at those appearances from 4 March 2024, one row per charge, with the case each is filed "
     "in", "Clerk of Superior Court, case management system"),
    (K.SCREENS, "Pretrial Assessment Scale screens, 1 October 2021 to 30 September 2026, one row per screen",
     "Pretrial Services screening system"),
    (K.JAIL, "Detention center bookings, 1 October 2021 to 30 September 2026, one row per booking", "Sheriff's Office "
     "jail management system"),
    (K.ARRESTS, "Arrests in North Carolina of every defendant in the first-appearance exports, 1 October 2021 to "
     "30 September 2026", "State arrest repository, extract requested by Pretrial Services, run 2 October 2026"),
    (K.CASES, "Criminal case index: every district and superior court case filed from 1 October 2021, with its "
     "disposition", "Clerk of Superior Court, case management system"),
    (K.EVENTS, "Court events, 1 October 2025 to 30 September 2026", "Clerk of Superior Court, case management system"),
    (K.EM, "Electronic monitoring invoice lines, October 2025 to September 2026", "Sentry Point Monitoring, monthly "
     "invoices to Dorrance County"),
    (K.HALSEY, "Halsey County inmate housing invoices, November 2025 to September 2026", "Halsey County Sheriff's "
     "Office, monthly invoices to the Sheriff's Office"),
    (K.CROSSWALK, "Offense code crosswalk, legacy to new system", "Clerk of Superior Court"),
    (K.ROSTER, "Magistrates of Dorrance County, 2021 to 2026, and the duty shifts", "Office of the Chief Magistrate"),
    (K.JAIL_CODES, "Jail booking types, release types and facilities", "Sheriff's Office"),
    (K.COURT_CODES, "Court codes: conditions, dispositions, events", "Clerk of Superior Court"),
    (K.CJAC, "Criminal Justice Advisory Council, jail population report for 2025", "Sheriff's Office for the Council"),
    (K.CRIME, "Reported offenses by Dorrance County agencies, 2019 to 2025", "Criminal Justice Advisory Council"),
]


def cjac_monthly(W):
    """Calendar 2025 by month from the jail's records: bookings, releases, the mean and highest midnight count at the
    detention center (main building and annex)."""
    import calendar
    import numpy as np
    end_t = K.d2dt(K.EXTRACT_END + dt.timedelta(days=1))
    d0 = dt.date(2025, 1, 1)
    nd = 365
    diff = np.zeros(nd + 2, dtype=np.int64)
    books = np.zeros(13, dtype=np.int64)
    rels = np.zeros(13, dtype=np.int64)
    for j in W.jail_rows:
        if j["kind"] == "stay":
            s, e, bt, rt = j["s"]["start"], j["s"]["end"], j["s"]["btype"], j["s"]["rtype"]
        else:
            s, e, bt, rt = j["o"]["start"], j["o"]["end"], "OFA", j["o"]["rtype"]
        if bt in ("NEW", "OFA") and s.year == 2025:
            books[s.month] += 1
        if rt not in ("TRF", "BO", None) and e < end_t and e.year == 2025:
            rels[e.month] += 1
        # midnights strictly inside (s, e): the counts at 00:00 of each day after s's date up to e
        first = (s.date() + dt.timedelta(days=1) - d0).days
        last_day = e.date() if e > K.d2dt(e.date()) else e.date() - dt.timedelta(days=1)
        last = (last_day - d0).days
        a, b = max(first, 0), min(last, nd - 1)
        if a <= b:
            diff[a] += 1
            diff[b + 1] -= 1
    counts = np.cumsum(diff)[:nd]
    out = []
    for mth in range(1, 13):
        a = (dt.date(2025, mth, 1) - d0).days
        b = (dt.date(2025, mth, calendar.monthrange(2025, mth)[1]) - d0).days
        c = counts[a:b + 1]
        out.append((dt.date(2025, mth, 1).strftime("%B"), int(books[mth]), int(rels[mth]), float(c.mean()), int(c.max())))
    return out


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or WD.simulate()
    if not getattr(W, "ids_issued", False):
        R.ofa_and_orders(W)
        R.issue_ids(W)
        W.ids_issued = True
    counts = {}
    leg, new, chg = R.fa_rows(W)
    counts[K.FA_LEGACY] = K.write_csv(p(K.FA_LEGACY), R.FA_LEGACY_COLS, leg, crlf=True)
    counts[K.FA_NEW] = K.write_csv(p(K.FA_NEW), R.FA_NEW_COLS, new)
    counts[K.FA_CHARGES] = K.write_csv(p(K.FA_CHARGES), R.CHG_COLS, chg)
    counts[K.SCREENS] = K.write_csv(p(K.SCREENS), R.SCREEN_COLS, R.screen_rows(W))
    counts[K.JAIL] = K.write_csv(p(K.JAIL), R.JAIL_COLS, R.jail_rows(W))
    counts[K.ARRESTS] = K.write_csv(p(K.ARRESTS), R.ARREST_COLS, R.arrest_rows(W))
    counts[K.CASES] = K.write_csv(p(K.CASES), R.CASE_COLS, R.case_rows(W))
    counts[K.EVENTS] = K.write_csv(p(K.EVENTS), R.EVENT_COLS, R.event_rows(W))
    counts[K.EM] = K.write_csv(p(K.EM), R.EM_COLS, R.em_rows(W), crlf=True)
    W.halsey = R.halsey_stays(W)
    DOC.write_halsey(p(K.HALSEY), W, W.halsey)
    DOC.write_crosswalk(p(K.CROSSWALK))
    DOC.write_roster(p(K.ROSTER), W)
    DOC.write_code_lists(p(K.JAIL_CODES), p(K.COURT_CODES))
    DOC.write_policy24(p(K.POLICY24))
    DOC.write_draft(p(K.DRAFT))
    DOC.write_guide(p(K.GUIDE))
    if not hasattr(W, "cjac"):
        W.cjac = cjac_monthly(W)
    DOC.write_cjac_jail(p(K.CJAC), W, W.cjac)
    DOC.write_crime(p(K.CRIME))
    DOC.write_readme(p(K.README), FILES)
    P = K.PEOPLE
    PP.normalize_ooxml(p(K.DRAFT), P["srj"], P["srj"], "2026-09-21T14:12:09Z", "2026-10-06T15:48:31Z",
                       title="Local bail policy revision for 2027 (draft)", company="Dorrance County Superior Court")
    PP.normalize_ooxml(p(K.HALSEY), "Halsey County Sheriff", "Halsey County Sheriff", "2025-12-02T13:20:44Z",
                       "2026-10-01T12:05:10Z", excel=True, company="Halsey County Sheriff's Office")
    PP.normalize_ooxml(p(K.CROSSWALK), P["clerk"], P["clerk"], "2023-11-14T15:02:17Z", "2024-02-28T19:44:52Z",
                       excel=True, company="Dorrance County Clerk of Superior Court")
    PP.normalize_ooxml(p(K.ROSTER), P["chiefmag"], P["chiefmag"], "2021-06-30T12:11:35Z", "2026-09-28T13:29:03Z",
                       excel=True, company="Dorrance County Magistrates")
    PP.normalize_ooxml(p(K.CRIME), P["analyst"], P["analyst"], "2023-03-02T14:55:21Z", "2026-03-09T18:31:47Z",
                       excel=True, company="Dorrance County")
    PP.normalize_pdf(p(K.POLICY24), b"D:20240614103012-04'00'", b"D:20240614104455-04'00'")
    PP.normalize_pdf(p(K.GUIDE), b"D:20240301091534-05'00'", b"D:20240301092208-05'00'")
    PP.normalize_pdf(p(K.CJAC), b"D:20260209154110-05'00'", b"D:20260209154653-05'00'")
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    W.counts = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return W


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = EXPORT_STAMP.timetuple()[:6]
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
    import metadata as MD
    W = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
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
