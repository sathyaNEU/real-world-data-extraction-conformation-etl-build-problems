"""task270 build: the world, the pack under target/, the goldens, figures.json, metadata.json and submission.md.

    python3 task270/generator/build.py [--out <dir>] [--pack-only] [--quiet]"""
from __future__ import annotations

import datetime as dt
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import docs as DOC      # noqa: E402
import postprocess as PP  # noqa: E402
import records as R     # noqa: E402
import sheets as SH     # noqa: E402
import world as W       # noqa: E402

import numpy as np      # noqa: E402

TASK = os.path.dirname(HERE)

CENSUS_PRE = [["Australian Bureau of Statistics"], [""], ["2021 Census - counting persons, place of usual residence"],
              ["SA2 (UR) by SEXP Sex and AGEP Age"], ["Counting: Person Records"], [""], ["Filters:"],
              ["Default Summation", "Person Records"], [""]]
CENSUS_POST = [[""], ["Data Source: Census of Population and Housing, 2021, TableBuilder"], [""],
               ["INFO", "Cells in this table have been randomly adjusted to avoid the release of confidential data. "
                        "No reliance should be placed on small cells."], [""],
               ["Copyright Commonwealth of Australia, 2022, see abs.gov.au/copyright"],
               ["ABS data licensed under Creative Commons, see abs.gov.au/ccby"]]


def world():
    A = W.areas()
    levels = dict(K.LEVELS)
    scale = W.calibrate_scale(A, levels)
    P = W.simulate(W.add_ymd(W.build_people(A, levels, scale)), A, levels)
    P = R.person_attributes(P, A)
    born66 = P["_dob_ymd"][0] == 1966
    on = [W.alive_on(P, dt.date(y, 6, 30)) & born66 for y in range(2016, 2027)]
    n1966 = {a.name: {s: np.array([int((o & (P["area"] == a.i) & (P["sex"] == k)).sum()) for o in on], dtype=float)
                      for s, k in (("F", 0), ("M", 1))} for a in A}
    Y = W.young_cohorts(A, n1966)
    return A, P, Y


def write_pack(out, A, P, Y, say=print):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    J = lambda f: os.path.join(out, f)
    recs = R.death_records(P, A)
    recs = recs + R.young_deaths(A, Y)
    recs = recs + R.tail_2015(A, recs)
    n = K.write_csv(J(K.F_DEATHS), ["registration_number", "registration_date", "date_of_death", "date_of_birth",
                                    "age_at_death", "sex", "usual_residence_sa2_code", "usual_residence_sa2_name",
                                    "usual_residence_lga_code", "usual_residence_lga_name", "place_of_death",
                                    "reported_to_coroner", "underlying_cause_icd10"], R.extract_rows(recs))
    say("death registrations", n)
    inter = R.interstate_rows(recs)
    SH.interstate_workbook(inter, J(K.F_INTERSTATE))
    say("interstate", len(inter))
    E = R.erp(P, A, Y)
    SH.erp_workbook(E, A, J(K.F_ERP))
    C = R.census_counts(P, A, Y)
    rows = []
    for a in sorted(A, key=lambda a: a.code):
        for code, name in a.sa2:
            for s, label in (("M", "Male"), ("F", "Female")):
                v = C[(code, name, s)]
                for age in range(116):
                    rows.append([name, label, "115 years and over" if age == 115 else str(age), int(v[age])])
    _tablebuilder(J(K.F_CENSUS), rows)
    say("census cells", len(rows))
    NS = R.nsw_single_year()
    nrows = []
    for y in range(2016, 2027):
        for s in ("M", "F"):
            for age in range(101):
                nrows.append([y, s, "100 and over" if age == 100 else str(age), int(NS[(y, s)][age])])
    K.write_csv(J(K.F_NSW), ["Year", "Sex", "Age", "Estimated resident population"], nrows)
    crow = []
    for a in sorted(A, key=lambda a: a.code):
        for code, name in a.sa2:
            crow.append([code, name, a.code, a.name, "1.000000", "Good", "Good", ""])
    crow.sort()
    K.write_csv(J(K.F_CORR), ["SA2_CODE_2021", "SA2_NAME_2021", "LGA_CODE_2023", "LGA_NAME_2023", "RATIO_FROM_TO",
                              "INDIV_TO_REGION_QLTY_INDICATOR", "OVERALL_QUALITY_INDICATOR", "BMOS_NULL_FLAG"], crow)
    DOC.write_guidelines(J(K.F_GUIDE))
    visits = R.after_hours(P, A, recs)
    young = R.younger_clients(A, E)
    ah = R.attendance_rows(P, A, visits, young)
    n = K.write_csv(J(K.F_AH), ["attendance_id", "case_ref", "client_key", "external_id", "birth_month", "sex",
                                "age_at_attendance", "residence_sa2_code", "residence_type", "requested_at",
                                "arrived_at", "departed_at", "clinician_id", "clinician_role", "outcome"], ah)
    say("after-hours attendances", n)
    on = W.alive_on(P, dt.date(2026, 6, 30))
    ag = W.ages_on_fast(P, dt.date(2026, 6, 30))
    old85 = {a.name: int((on & (P["area"] == a.i) & (ag >= 85)).sum()) for a in A}
    SH.racf_workbook(A, old85, J(K.F_RACF))
    K.write_csv(J(K.F_FALLS), ["LGA code", "Local government area", "Number", "Rate per 100,000 population",
                               "LL 95% CI", "UL 95% CI"], R.falls_rows(A, E))
    normalize(out)
    return recs


def _tablebuilder(path, rows):
    """TableBuilder's 'CSV string value' export: quoted labels, a trailing comma on each row."""
    def q(x):
        return '"%s"' % x
    lines = []
    for r in CENSUS_PRE:
        lines.append(",".join(q(x) for x in r) if r != [""] else "")
    lines.append(",".join(q(h) for h in ("SA2 (UR)", "SEXP Sex", "AGEP Age", "Count")) + ",")
    for name, sex, age, n in rows:
        lines.append("%s,%s,%s,%d," % (q(name), q(sex), q(age), n))
    for r in CENSUS_POST:
        lines.append(",".join(q(x) for x in r) if r != [""] else "")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(lines) + "\r\n")


def normalize(out):
    p = lambda f: os.path.join(out, f)
    owner = {K.F_ERP: ("Australian Bureau of Statistics", "2027-08-20T02:10:00Z", "2027-08-26T23:40:00Z",
                       "Australian Bureau of Statistics"),
             K.F_INTERSTATE: ("Australian Bureau of Statistics", "2027-09-03T04:12:00Z", "2027-09-06T01:30:00Z",
                              "Australian Bureau of Statistics"),
             K.F_RACF: (K.PEOPLE["analyst"], "2026-08-11T03:20:00Z", "2026-08-11T03:41:00Z", K.PHN)}
    for f, (who, c, m, co) in owner.items():
        PP.normalize_ooxml(p(f), who, who, c, m, excel=True, company=co)
    PP.normalize_pdf(p(K.F_GUIDE), b"D:20270902104500+10'00'", b"D:20270902104500+10'00'")


def cut_zip(root):
    """target.zip from the final rebuild: the pack's files at the archive's root, stamped with the files' taking."""
    import zipfile
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 9, 15, 9, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zpath


def main(argv):
    quiet = "--quiet" in argv
    say = (lambda *a: None) if quiet else (lambda *a: print(*a, flush=True))
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(TASK, "target")
    t0 = time.time()
    A, P, Y = world()
    say("world %.0fs, %d people" % (time.time() - t0, len(P["dob"])))
    write_pack(out, A, P, Y, say)
    say("pack %.0fs" % (time.time() - t0))
    if "--pack-only" in argv:
        return 0
    import deliver
    import metadata
    import writeup
    figs = deliver.run(TASK, out)
    metadata.write(TASK)
    writeup.write(TASK, figs)
    if "--out" not in argv:
        cut_zip(TASK)
    say("done %.0fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
