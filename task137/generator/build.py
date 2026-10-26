"""Build task137's pack under target/ from the world, then the golden figures, the deliverables and the write-up.

    python3 build.py            # target/, figures.json, golden/, submission.md, then checks.py
    python3 build.py --pack     # target/ only
"""
import argparse
import csv
import datetime as dt
import io
import os
import shutil
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as WD          # noqa: E402
import pack as PK           # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402

SEED, BTP_MAIN, HUB_LAM, SHOCK_SD = 8111, 1600.0, 290.0, 0.010
CJU_STREAM = 8          # the remand files' own random stream (handover minutes, the cases keyed to a first arrest)
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")

F_ARR = "calderwick_police_arrests_2021-04_2026-09.csv"
F_POL = "police_uk_street_crime_2025-26.csv"
F_LOOK = "lsoa21_to_ward_lookup.csv"
F_ALLOC = "custody_suite_allocation_2027.xlsx"
F_MODEL = "custody_demand_model_v2.pdf"
F_BRIEF = "tanner_street_hub_planning_brief.docx"
F_CJU = "cju_remand_files_2025-03_2026-04.csv"
F_HC = "custody_healthcare_contacts_2025-26.csv"
F_ESTATE = "custody_estate_register_2026.xlsx"
F_POP = "ward_population_mid-2024.csv"
F_LIC = "late_night_licences_2026.csv"
F_BH = "bank-holidays.json"
FILES = [F_BRIEF, F_MODEL, F_ALLOC, F_ARR, F_POL, F_LOOK, F_CJU, F_HC, F_ESTATE, F_POP, F_LIC, F_BH]
DISTRACTORS = [F_ESTATE, F_POP, F_LIC, F_BH]
MTIME = {F_ARR: "2026-10-06 08:41", F_POL: "2026-06-04 14:12", F_LOOK: "2024-07-22 09:30", F_ALLOC: "2026-09-10 16:05",
         F_MODEL: "2026-06-11 16:20", F_BRIEF: "2026-10-20 10:47", F_CJU: "2026-10-12 11:18", F_HC: "2026-04-14 09:02",
         F_ESTATE: "2026-09-01 12:30", F_POP: "2025-07-15 09:30", F_LIC: "2026-10-01 15:44", F_BH: "2026-10-19 08:55"}


def iso_z(t_local):
    return PK.to_utc(t_local).strftime("%Y-%m-%dT%H:%M:00Z")


def hhmm(mins):
    return "%d:%02d" % (mins // 60, mins % 60)


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        w.writerows(rows)


def make_world():
    W = WD.world(SEED, btp_main=BTP_MAIN, hub_lam=HUB_LAM, shock_sd=SHOCK_SD)
    C = WD.counts(W)
    rng = np.random.default_rng(SEED + 29)
    PK.lsoa_frame(W, rng)
    rows, incidents = PK.arrests(W, C, rng)
    PK.arrest_refs(rows, rng)
    files = PK.remand_files(rows, np.random.default_rng(SEED + 53 + CJU_STREAM))
    close = PK.moves(rows)
    btp = PK.btp_detainees(W, C, rng, close)
    hc = PK.healthcare(rows, btp, rng, close)
    pol = PK.street_crime(W, C, rng)
    return dict(W=W, C=C, rows=rows, files=files, btp=btp, hc=hc, pol=pol, close=close)


def validation_rows(rows):
    """The model's own back-test, as its note reports it: base 2024-25 with the change from 2021-22, against the
    arrest records for 2025-26, suite by suite (by the wards each suite serves)."""
    by = {}
    for r in rows:
        fy = PK.fy_local(r["t_arrest"])
        by.setdefault(WD.SUITE_NOW[r["ward"]], {}).setdefault(r["ward"], {}).setdefault(fy, 0)
        by[WD.SUITE_NOW[r["ward"]]][r["ward"]][fy] += 1
    out = []
    for s in WD.SUITES:
        fc = 0.0
        act = 0
        for w, d in by[s].items():
            ch = (d[2024] / d[2021]) ** (1 / 3) - 1
            ch = max(-0.10, min(0.10, ch))
            fc += d[2024] * (1 + ch)
            act += d[2025]
        out.append((s, fc, act, fc / act))
    return out


def write_pack(T, target=TARGET):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W, rows, files, hc, pol = T["W"], T["rows"], T["files"], T["hc"], T["pol"]
    wcode = PK.wards_codes()
    # the force's arrest records
    write_csv(os.path.join(target, F_ARR),
              ["arrest_ref", "custody_suite", "arrested_utc", "booked_in_utc", "ward_code", "ward", "offence_group",
               "age_band", "sex", "detention_hhmm", "outcome"],
              [[r["ref"], r["suite"], iso_z(r["t_arrest"]), iso_z(r["t_book"]), r["ward_code"], r["ward"], r["group"],
                r["age"], r["sex"], hhmm(r["mins"]), r["out"]] for r in rows], crlf=True)
    # data.police.uk street-level crime
    write_csv(os.path.join(target, F_POL), ["Crime ID", "Month", "Reported by", "Falls within", "Longitude", "Latitude",
                                            "Location", "LSOA code", "LSOA name", "Crime type", "Last outcome category",
                                            "Context"], pol)
    write_csv(os.path.join(target, F_LOOK), ["lsoa21_code", "lsoa21_name", "ward_code", "ward"],
              [[l["code"], l["name"], wcode[l["ward"]], l["ward"]] for l in W["lsoas"]])
    # the Criminal Justice Unit's remand files
    seq = {}
    cju = []
    for f in files:
        tch = PK.charge_time(f)
        yy = tch.year % 100
        key = (PK.SUITE_CODE[f["suite"]], yy)
        seq[key] = seq.get(key, 0) + 1
        cju.append(["52%s%05d%02d" % (key[0], 80 + 3 * seq[key], yy), f["linked"], f["suite"], tch.strftime("%d/%m/%Y %H:%M"),
                    PK.first_hearing(tch).strftime("%d/%m/%Y"), PK.COURT[f["suite"]],
                    f["handover"].strftime("%d/%m/%Y %H:%M")])
    write_csv(os.path.join(target, F_CJU), ["urn", "linked_arrest", "custody_suite", "charged", "first_hearing", "court",
                                            "handed_to_escort"], cju, crlf=True)
    # the healthcare provider's contact export
    write_csv(os.path.join(target, F_HC), ["contact_ref", "episode_ref", "suite", "clinician", "contact_type", "started",
                                           "ended", "outcome"],
              [[r["ref"], "E%07d" % r["ep"], r["team"], r["clin"], r["kind"], r["start"].strftime("%Y-%m-%d %H:%M"),
                r["end"].strftime("%Y-%m-%d %H:%M"), r["outcome"]] for r in hc])
    # documents
    val = validation_rows(rows)
    pct = DOC.write_model(os.path.join(target, F_MODEL), val)
    DOC.write_brief(os.path.join(target, F_BRIEF))
    DOC.write_allocation(os.path.join(target, F_ALLOC), wcode)
    DOC.write_estate(os.path.join(target, F_ESTATE))
    rng = np.random.default_rng(SEED + 41)
    write_csv(os.path.join(target, F_POP), ["ward_code", "ward_name", "local_authority", "all_ages", "aged_0_15",
                                            "aged_16_64", "aged_65_plus"], DOC.population_rows(W, rng, wcode))
    write_csv(os.path.join(target, F_LIC), ["licence_no", "premises", "ward", "ward_code", "latest_sun_thu", "latest_fri_sat",
                                            "capacity", "granted", "status"], DOC.licence_rows(rng, wcode), crlf=True)
    with open(os.path.join(target, F_BH), "w", encoding="utf-8") as fh:
        fh.write(DOC.bank_holidays())
    # containers carry their owners and in-fiction stamps
    PP.normalize_ooxml(os.path.join(target, F_BRIEF), DOC.PEOPLE["programme"], DOC.PEOPLE["programme"],
                       "2026-10-19T15:02:00Z", "2026-10-20T09:47:00Z", title="Tanner Street custody hub planning figure")
    PP.normalize_ooxml(os.path.join(target, F_ALLOC), "Custody Services", DOC.PEOPLE["custody"],
                       "2019-02-11T10:20:00Z", "2026-09-10T15:05:00Z", excel=True)
    PP.normalize_ooxml(os.path.join(target, F_ESTATE), "Estates", "Estates", "2017-05-02T08:15:00Z",
                       "2026-09-01T11:30:00Z", excel=True)
    PP.normalize_pdf(os.path.join(target, F_MODEL), b"D:20260611151200+01'00'", b"D:20260611152000+01'00'")
    for f, s in MTIME.items():
        ts = time.mktime(dt.datetime.strptime(s, "%Y-%m-%d %H:%M").timetuple())
        os.utime(os.path.join(target, f), (ts, ts))
    return dict(val=val, pct=pct)


def write_zip(target=TARGET, out=os.path.join(TASK, "target.zip")):
    """target.zip: the twelve files at the archive's root, in name order, each stamped with its own export time."""
    import zipfile
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(n, date_time=dt.datetime.strptime(MTIME[n], "%Y-%m-%d %H:%M").timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, n), "rb") as fh:
                z.writestr(zi, fh.read(), compresslevel=9)
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--zip", action="store_true", help="cut target.zip from target/ and stop")
    ap.add_argument("--target", default=TARGET)
    a = ap.parse_args(argv)
    if a.zip:
        print(write_zip(a.target))
        return 0
    t0 = time.time()
    T = make_world()
    info = write_pack(T, a.target)
    print("pack written to %s in %.1f s (validation within %d per cent)" % (a.target, time.time() - t0, info["pct"]))
    if a.pack:
        return 0
    import golden as GD
    figs = GD.main([a.target])
    print("figures.json: %d keys" % len(figs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
