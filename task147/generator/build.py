"""Build task147: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task147/generator/build.py              everything
    python3 task147/generator/build.py --out DIR    the pack only, into DIR"""
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
import calc as C            # noqa: E402
import cast as CA           # noqa: E402
import common as K          # noqa: E402
import distract as DS       # noqa: E402
import docs as DOC          # noqa: E402
import ops2026 as O         # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2027, 7, 1, 7, 41, tzinfo=dt.timezone.utc)      # 08:41 on 1 July at the desk
F_MANIFEST = "folder_contents.csv"


class World:
    pass


def world():
    Wd = World()
    Wd.W = WD.simulate()
    Wd.B = R.bookings(Wd.W)
    Wd.S = O.season(Wd.B)
    Wd.acc, Wd.badges, Wd.truth_b, Wd.staff_badge = O.access(Wd.S)
    Wd.audit = R.night_audit(Wd.B)
    return Wd


ACCESS_COLS = ["event_time", "reader", "badge", "holder", "direction"]
BADGE_COLS = ["date", "badge", "issued_to", "company", "issued_at", "issued_by", "returned"]


def manifest_rows():
    return [
        [R.F_EXTRACT, "Property management system", "2027-07-01", "Reservations with arrivals from 01/01/2022",
         "Reservations"],
        [R.F_AMEND, "Property management system", "2027-07-01", "Date and guest-count changes to those reservations",
         "Reservations"],
        [R.F_NOTES, "Property management system", "2027-07-01", "Notes on the reservation extract", "Reservations"],
        [R.F_CODES, "Property management system", "2027-07-01", "Rate, channel and market codes", "Reservations"],
        [R.F_AUDIT, "Night audit", "2027-07-01", "Daily statistics, 01/01/2022 to 30/06/2027", "Front office"],
        [R.F_FEST, "Festival office", "2027-03-18", "Festival dates by edition, 2015 to 2027", "Sales office"],
        [R.F_DIARY, "Sales office", "2027-06-29", "City events 2022 to 2027", "Sales office"],
        [DOC.F_HK04, "Rooms Division standards", "2025-03-21", "Festival season staffing standard, issue 3",
         "Rooms Division"],
        [C.TASKS_F, "Housekeeping app", "2027-06-28", "Room tasks, 27/07/2026 to 30/08/2026", "Housekeeping"],
        [C.USERS_F, "Housekeeping app", "2027-06-28", "App users and groups as at the export", "Housekeeping"],
        [C.HR_F, "HR system", "2027-06-28", "Housekeeping staff as at 28/06/2027", "HR and Payroll"],
        [C.TS_F, "Brennock Hospitality Staffing", "2026-09-08", "Timesheets, weeks ending 26/07/2026 to 06/09/2026",
         "Housekeeping"],
        [C.PAY_F, "Payroll", "2027-06-28", "Room attendants' overtime lines, pay periods 14 to 19 of 2026",
         "HR and Payroll"],
        [C.ACCESS_F, "Staff access system", "2027-06-29", "Badge events, staff entrance and loading bay, August 2026",
         "Security"],
        [C.BADGE_F, "Reception", "2027-06-29", "Day badges issued, August 2026", "Front office"],
        [DOC.F_INVOICE, "Brennock Hospitality Staffing", "2026-08-19", "Invoice for the 2026 block", "Accounts"],
        [DOC.F_AGREEMENT, "Brennock Hospitality Staffing", "2025-03-14", "Framework agreement, 2025 to 2027",
         "Rooms Division"],
        [DS.F_SHOP, "Rate shopping service", "2027-06-30", "Competitors' public rates, 26/07/2027 to 29/08/2027",
         "Reservations"],
        [DS.F_SURVEY, "Callowfort Tourism", "2027-02-12", "Monthly hotel occupancy survey, 2019 to 2026",
         "Sales office"],
    ]


def build(out, quiet=False, Wd=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    Wd = Wd or world()
    B, S = Wd.B, Wd.S
    counts = {}
    counts[R.F_EXTRACT] = K.write_csv(p(R.F_EXTRACT), R.EXTRACT_COLS, R.extract_rows(B))
    counts[R.F_AMEND] = K.write_csv(p(R.F_AMEND), R.AMEND_COLS, R.amendment_rows(B))
    R.write_notes(p(R.F_NOTES))
    DOC.write_codes(p(R.F_CODES))
    DOC.write_audit(p(R.F_AUDIT), Wd.audit)
    R.write_festival(p(R.F_FEST))
    DOC.write_diary(p(R.F_DIARY), R.diary())
    DOC.write_hk04(p(DOC.F_HK04))
    counts[C.TASKS_F] = K.write_csv(p(C.TASKS_F), O.TASK_COLS, O.task_rows(S))
    counts[C.USERS_F] = K.write_csv(p(C.USERS_F), O.USER_COLS, O.user_rows(S))
    DOC.write_hr(p(C.HR_F), O.hr_rows(S))
    DOC.write_timesheets(p(C.TS_F), O.timesheet_rows(S))
    counts[C.PAY_F] = K.write_csv(p(C.PAY_F), O.PAY_COLS, O.payroll_rows(S), crlf=True)
    counts[C.ACCESS_F] = K.write_csv(p(C.ACCESS_F), ACCESS_COLS,
                                     [[O.fmt(t), rd, b, h, dr] for t, rd, b, h, dr in Wd.acc], crlf=True)
    counts[C.BADGE_F] = K.write_csv(p(C.BADGE_F), BADGE_COLS,
                                    [[x["date"].isoformat(), x["badge"], x["name"], x["company"],
                                      x["issued"].strftime("%H:%M"), x["by"], "Y"]
                                     for x in sorted(Wd.badges, key=lambda x: (x["date"], x["issued"], x["badge"]))])
    DOC.write_invoice(p(DOC.F_INVOICE), O.invoice(S))
    DOC.write_agreement(p(DOC.F_AGREEMENT))
    full = [K.dd(i) for i in range(K.di(K.season_nights(K.YEAR)[0]), K.di(K.season_nights(K.YEAR)[-1]) + 1)
            if Wd.W.booked[i] >= K.CAP]
    DOC.write_rateshop(p(DS.F_SHOP), DS.shop_rows(set(full)), DS.HOTELS)
    counts[DS.F_SURVEY] = K.write_csv(p(DS.F_SURVEY), DS.SURVEY_COLS, DS.survey_rows())
    K.write_csv(p(F_MANIFEST), ["file", "system", "taken_or_received", "covers", "kept_by"], manifest_rows())
    P = K.PEOPLE
    PP.normalize_pdf(p(DOC.F_HK04), b"D:20250321101418+00'00'", b"D:20250321101418+00'00'")
    PP.normalize_pdf(p(DOC.F_AGREEMENT), b"D:20250314154402+00'00'", b"D:20250314154402+00'00'")
    PP.normalize_pdf(p(DOC.F_INVOICE), b"D:20260819093127+01'00'", b"D:20260819093127+01'00'")
    PP.normalize_ooxml(p(R.F_CODES), "PMS", CA.RES_AGENTS[0], "2027-07-01T05:13:02Z", "2027-07-01T05:13:02Z",
                       excel=True)
    PP.normalize_ooxml(p(R.F_AUDIT), "Night audit", "Georgina Eustace", "2022-01-02T03:41:10Z",
                       "2027-07-01T02:58:37Z", excel=True)
    PP.normalize_ooxml(p(R.F_DIARY), CA.RES_AGENTS[0], CA.RES_AGENTS[2], "2021-11-29T10:05:44Z",
                       "2027-06-29T15:22:08Z", excel=True)
    PP.normalize_ooxml(p(C.HR_F), P["payroll"], P["payroll"], "2027-06-28T13:40:51Z", "2027-06-28T13:52:19Z",
                       excel=True)
    PP.normalize_ooxml(p(C.TS_F), P["agency"], P["agency"], "2026-07-27T08:12:40Z", "2026-09-08T11:31:05Z",
                       excel=True, company="Brennock Hospitality Staffing")
    PP.normalize_ooxml(p(DS.F_SHOP), "Rate shop", "Rate shop", "2027-06-30T06:02:11Z", "2027-06-30T06:02:11Z",
                       excel=True)
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    Wd.counts = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return Wd


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
    Wd = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    G = DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                os.path.join(root, "generator", "figures.json"), Wd=Wd)
    stamp = dt.datetime(2027, 7, 1, 9, 26, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return Wd, G


def main():
    import checks as CK
    import verify as V
    Wd, G = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), Wd=Wd, G=G,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), os.path.join(TASK, "generator", "figures.json"))
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
            d1, d2 = digest(os.path.join(TASK, "target")), digest(os.path.join(tmp, "target"))
            g1, g2 = digest(os.path.join(TASK, "golden")), digest(os.path.join(tmp, "golden"))
            raise SystemExit("second build differs: target %s, golden %s, %s; %s" % (
                same_t, same_g, same, [f for f in d1 if d1[f] != d2.get(f)] + [f for f in g1 if g1[f] != g2.get(f)]))
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
