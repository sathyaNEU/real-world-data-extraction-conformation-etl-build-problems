"""Write the bundle under target/ from the clean truth in world.py.

Every file is written the way the producing system would export it; nothing here describes the data.
"""
import datetime
import os

import numpy as np
import openpyxl

import common
import docs
import world

AGEGROUPS = [(16, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 120)]
OCC_SOC = {11: "11-0000", 13: "13-0000", 15: "15-0000", 25: "25-0000", 29: "29-0000", 35: "35-0000",
           37: "37-0000", 41: "41-0000", 43: "43-0000", 47: "47-0000", 49: "49-0000", 51: "51-0000",
           53: "53-0000"}
REV_AREA = "06"           # the area whose July 2025 adult estimate the State Demographer revised before 2026Q3's reissue
REV_FACTOR = 1.0637
PARALLEL_END = datetime.date(2026, 5, 31)   # the old CAPI system stayed open for interviewers until this date
REF = world.REF_QUARTERS


def agegroup(age):
    for i, (lo, hi) in enumerate(AGEGROUPS):
        if lo <= age <= hi:
            return i
    return len(AGEGROUPS) - 1


def mt_offset(d):
    """Mountain time offset from UTC in hours on a date (2025 and 2026 daylight saving rules)."""
    dst = {2025: (datetime.date(2025, 3, 9), datetime.date(2025, 11, 2)),
           2026: (datetime.date(2026, 3, 8), datetime.date(2026, 11, 1))}[d.year]
    return -6 if dst[0] <= d < dst[1] else -7


def qidx(q):
    return world.QUARTERS.index(q)


def entry_label(e):
    y = 2025 + (e // 4)
    return "RG%02dQ%d" % (y % 100, e % 4 + 1)


def build_ids(W, rng):
    """Frame ids, the old system's case ids and the new system's case ids, all drawn, none sequential."""
    n = len(W["addresses"])
    fr = 10_000_000 + rng.choice(89_999_999, size=n, replace=False)
    old = 1_000_000 + rng.choice(8_999_999, size=n, replace=False)
    new = 100_000_000 + rng.choice(899_999_999, size=n + 3000, replace=False)
    ids = {}
    for a, f, o, nw in zip(W["addresses"], fr, old, new[:n]):
        ids[a["aid"]] = dict(frame="FR%08d" % f, old="TH%07d" % o, new="H%09d" % nw)
    W["spare_new"] = ["H%09d" % x for x in new[n:]]
    return ids


def case_id(ids, aid, q, entry):
    """The case id a unit carries in a quarter: the new system's from 2026Q2; a unit that entered on the new system
    never had an old id."""
    return ids[aid]["new"] if qidx(q) >= qidx(world.MIGRATION_Q) or entry >= qidx(world.MIGRATION_Q) else ids[aid]["old"]


def controls(rng):
    """Adults 16 and over by area, age group and sex (July 2025 estimates), the weighting's population controls."""
    base = np.array([0.155, 0.168, 0.162, 0.150, 0.160, 0.205])
    ctl = {}
    for code, name, ctys, adults_k, ms, ash, _p1 in world.AREAS:
        tilt = rng.normal(0, 0.012, size=len(base))
        sh = np.clip(base + tilt, 0.08, 0.3)
        sh = sh / sh.sum()
        for g, s in enumerate(sh):
            male = 0.5 + rng.normal(0, 0.012) - (0.04 if g == 5 else 0.0)
            tot = adults_k * 1000 * s
            ctl[(code, g, 1)] = int(round(tot * male))
            ctl[(code, g, 2)] = int(round(tot * (1 - male)))
    return ctl


def weights(W, ctl):
    """The survey's final weights per quarter: base weight, eligible-nonresponse adjustment, post-stratification."""
    issued = {}
    for h in W["hh_q"]:
        issued.setdefault((h["q"], h["area"]), []).append(h)
    hw = {}
    for (q, area), hs in issued.items():
        w0 = W["frame_size"][area] / len(hs)
        elig = [h for h in hs if h["outcome"] != "INELIGIBLE"]
        comp = [h for h in elig if h["outcome"] == "COMPLETE"]
        adj = len(elig) / len(comp)
        for h in comp:
            hw[(h["aid"], q)] = w0 * adj
    out = {}
    for q in world.QUARTERS:
        cells = {}
        for p in W["persons_q"]:
            if p["q"] == q:
                cells.setdefault((p["area"], agegroup(p["age"]), p["sex"]), []).append(p)
        for key, ps in cells.items():
            f = ctl[key] / sum(hw[(p["aid"], q)] for p in ps)
            for p in ps:
                out[(p["aid"], p["line"], q)] = hw[(p["aid"], q)] * f
    return out


def field_day(rng, q, slot=None):
    """A visit or interview date in the quarter's field period (the two weeks after the reference week)."""
    yr, mo = world.FIELD_MONTH[q]
    d12 = datetime.date(yr, mo, 12)
    sat = d12 + datetime.timedelta(days=(5 - d12.weekday()) % 7)     # the Saturday ending the reference week
    while True:
        d = sat + datetime.timedelta(days=1 + int(rng.integers(0, 15)))
        if slot == "SAT" and d.weekday() != 5:
            continue
        if slot in ("EVE", "DAY") and d.weekday() >= 5:
            continue
        return d


def write_target(W, tdir):
    rng = W["rng_ops"]
    os.makedirs(tdir, exist_ok=True)
    ids = build_ids(W, rng)
    ctl = controls(rng)
    wts = weights(W, ctl)
    W["ids"], W["ctl"], W["wts"] = ids, ctl, wts
    mig = qidx(world.MIGRATION_Q)
    A = W["addr_by_id"]

    # ---- person file (the estimation extract the bureau builds each quarter) ----
    rows = []
    for p in sorted(W["persons_q"], key=lambda r: (r["qi"], case_id(ids, r["aid"], r["q"], A[r["aid"]]["entry"]),
                                                  r["line"])):
        if p["lfs"] in (1, 2):
            if p["pt"]:
                h = 20 if rng.random() < 0.30 else 12 + int(rng.integers(0, 23))
            else:
                h = 40 if rng.random() < 0.42 else 35 + int(rng.integers(0, 21))
            if rng.random() < (0.045 if not p["self_rep"] else 0.006):
                h = -9
            hrs, occ, mjh = h, OCC_SOC[p["occ"]], (1 if p["mjh_rep"] == 1 else 2)
        else:
            hrs, occ, mjh = -1, "", -1
        rows.append([p["q"], case_id(ids, p["aid"], p["q"], A[p["aid"]]["entry"]), p["line"], p["age"], p["sex"],
                     p["rel"], p["area"], p["lfs"], hrs, occ, mjh, p["resp_line"], p["want"]])
    common.write_csv(os.path.join(tdir, "HES_PERSON_2025Q1_2026Q3.csv"),
                     ["SURVEY_QTR", "CASEID", "LINENO", "AGE", "SEX", "RELREF", "HES_AREA", "LFSTAT", "HRSMAIN",
                      "OCCMAJ", "MJH", "RESPLINE", "WANTJOB"], rows)

    # ---- household dispositions (field operations extract, both CAPI systems) ----
    # Noncontacts (and a few interviews) in the reference year at units the frame deleted in error and restored
    # only after the visit.
    ref_nc = [h for h in W["hh_q"] if h["q"] in REF and h["outcome"] == "NONCONTACT"]
    ref_cp = [h for h in W["hh_q"] if h["q"] in REF and h["outcome"] == "COMPLETE" and not h.get("refusal_converted")]
    err_after = set()
    for code, *_ in world.AREAS:
        nc = [h for h in ref_nc if h["area"] == code and A[h["aid"]]["vacant_from"] is None]
        for k in rng.choice(len(nc), size=int(rng.integers(25, 37)), replace=False):
            err_after.add((nc[k]["aid"], nc[k]["q"]))
        cp = [h for h in ref_cp if h["area"] == code and A[h["aid"]]["vacant_from"] is None]
        for k in rng.choice(len(cp), size=int(rng.integers(2, 6)), replace=False):
            err_after.add((cp[k]["aid"], cp[k]["q"]))
    W["err_after"] = err_after

    hrows = []
    W["copies"], W["reissues"], W["visit_date"], W["vac_nc"] = [], [], {}, []
    for h in W["hh_q"]:
        q, qi, aid = h["q"], h["qi"], h["aid"]
        new = qi >= mig
        a = A[aid]
        cid = case_id(ids, aid, q, a["entry"])
        base = [q, cid, ids[aid]["frame"], entry_label(a["entry"]), h["wave"], "59" + h["county"], h["zip"]]
        intv = "I%03d" % (101 + 40 * world.area_index()[h["area"]] + int(rng.integers(0, 34)))
        if h["outcome"] == "INELIGIBLE":
            d = field_day(rng, q)
            kind = h["vacant_kind"]
            if kind == "NOT_A_DWELLING":
                code = 225 if new else 6
            elif qi == a["vacant_from"] and rng.random() < 0.62:
                code = 216 if new else 3      # the interviewer found no one at home
                W["vac_nc"].append((aid, q))
            else:
                code = (223 if kind == "VACANT" else 224) if new else (5 if kind == "VACANT" else 6)
            W["visit_date"][(aid, q)] = d
            hrows.append(base + [code, d.isoformat(), "", "", intv, ""])
            continue
        if h["outcome"] == "COMPLETE":
            d = field_day(rng, q, h["slot"])
            if h["slot"] == "EVE":
                hh, mm = int(rng.integers(17, 21)), int(rng.integers(0, 60))
            else:
                hh, mm = int(rng.integers(9, 17)), int(rng.integers(0, 60))
            local = datetime.datetime(d.year, d.month, d.day, hh, mm)
            utc = local - datetime.timedelta(hours=mt_offset(d))
            tel = h["wave"] > 1 and rng.random() < 0.21
            mode = ("CAPI-T" if tel else "CAPI-P") if new else ("TEL" if tel else "PV")
            W["visit_date"][(aid, q)] = d
            if h.get("refusal_converted"):
                d0 = d - datetime.timedelta(days=int(rng.integers(3, 8)))
                hrows.append(base + [213 if new else 2, d0.isoformat(), "", "", intv, ""])
                if new:
                    # the new system reissues a converted refusal to a senior interviewer as a case of its own
                    rid = W["spare_new"].pop()
                    W["reissues"].append((aid, q, rid))
                    base = [q, rid] + base[2:]
                    intv = "I%03d" % (101 + 40 * world.area_index()[h["area"]] + 34 + int(rng.integers(0, 4)))
            hrows.append(base + [201 if new else 1, d.isoformat(), utc.strftime("%Y-%m-%dT%H:%M:00Z"), mode, intv,
                                 h["n_adults"]])
            if qi == mig and a["entry"] < mig and rng.random() < 0.075 and d <= PARALLEL_END:
                # the same interview keyed into the old system while it stayed open, synced a day or more later
                up = d + datetime.timedelta(days=int(rng.integers(1, 4)))
                hrows.append([q, ids[aid]["old"], ids[aid]["frame"], entry_label(a["entry"]), h["wave"],
                              "59" + h["county"], h["zip"], 1, up.isoformat(), "", "TEL" if tel else "PV", intv,
                              h["n_adults"]])
                W["copies"].append((aid, q))
            continue
        d = field_day(rng, q)
        W["visit_date"][(aid, q)] = d
        if h["outcome"] == "REFUSED":
            code = 213 if new else 2
        else:
            code = (216 if new else 3) if (rng.random() < 0.80 or (aid, q) in err_after) else (219 if new else 4)
        hrows.append(base + [code, d.isoformat(), "", "", intv, ""])
    hrows.sort(key=lambda r: (qidx(r[0]), r[2], r[8], str(r[7])))
    common.write_csv(os.path.join(tdir, "HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv"),
                     ["SURVEY_QTR", "CASEID", "FRAMEID", "ROTGRP", "WAVE", "CTY", "ZIP", "DISPO", "DISPO_DATE",
                      "START_UTC", "MODE", "INTV_ID", "NUM_ADULTS"], hrows)
    W["hrows"] = hrows

    # ---- the CAPI migration crosswalk: every case live in both systems at the change ----
    xrows = []
    for a in W["addresses"]:
        if a["entry"] <= mig - 1 and a["entry"] + 3 >= mig:
            xrows.append([ids[a["aid"]]["old"], ids[a["aid"]]["new"], "2026-04-27"])
    xrows.sort()
    common.write_csv(os.path.join(tdir, "HES_CASEID_CROSSWALK_CAPI2026.csv"),
                     ["OLD_CASEID", "NEW_CASEID", "MIGRATED_ON"], xrows)

    # ---- frame maintenance log ----
    frows = []
    sample_frames = {ids[a["aid"]]["frame"] for a in W["addresses"]}
    for a in W["addresses"]:
        vq = a["vacant_from"]
        if vq is None:
            continue
        if 0 <= vq < len(world.QUARTERS):
            first = W["visit_date"].get((a["aid"], world.QUARTERS[vq]))
            if first is None:
                continue
            eff = first - datetime.timedelta(days=int(rng.integers(12, 60)))
        elif vq < 0:
            eff = datetime.date(2024, 7, 1) + datetime.timedelta(days=int(rng.integers(5, 150)))
        else:
            continue
        reason = "VACANT" if a["vacant_kind"] == "VACANT" else "DEMOLISHED"
        src = "USPS" if (reason == "VACANT" and rng.random() < 0.55) else "FIELD"
        frows.append([ids[a["aid"]]["frame"], "59" + a["county"], a["zip"], "DELETE", eff.isoformat(), reason, src])
    # deletions entered in error: most restored before the next visit, some only after it
    occ = [a for a in W["addresses"] if a["occupied0"] and a["vacant_from"] is None]
    W["err_before"] = []
    err_units = {aid for aid, q in err_after}
    for k in sorted(rng.choice(len(occ), size=44, replace=False)):
        a = occ[k]
        if a["aid"] in err_units:
            continue
        qs = [world.QUARTERS[a["entry"] + w] for w in range(4) if 0 <= a["entry"] + w < len(world.QUARTERS)]
        qs = [q for q in qs if (a["aid"], q) in W["visit_date"]]
        if not qs:
            continue
        q = qs[int(rng.integers(0, len(qs)))]
        v = W["visit_date"][(a["aid"], q)]
        eff = v - datetime.timedelta(days=int(rng.integers(30, 70)))
        rst = eff + datetime.timedelta(days=int(rng.integers(6, 20)))
        frows.append([ids[a["aid"]]["frame"], "59" + a["county"], a["zip"], "DELETE", eff.isoformat(), "VACANT", "USPS"])
        frows.append([ids[a["aid"]]["frame"], "59" + a["county"], a["zip"], "RESTORE", rst.isoformat(),
                      "DELETED IN ERROR", "FIELD"])
        W["err_before"].append((a["aid"], q))
    for aid, q in sorted(err_after):
        a = A[aid]
        v = W["visit_date"][(aid, q)]
        eff = v - datetime.timedelta(days=int(rng.integers(10, 45)))
        rst = v + datetime.timedelta(days=int(rng.integers(5, 30)))
        frows.append([ids[aid]["frame"], "59" + a["county"], a["zip"], "DELETE", eff.isoformat(), "VACANT", "USPS"])
        frows.append([ids[aid]["frame"], "59" + a["county"], a["zip"], "RESTORE", rst.isoformat(),
                      "DELETED IN ERROR", "FIELD"])
    # the rest of the frame's traffic, addresses never in sample
    cz = sorted({("59" + a["county"], a["zip"]) for a in W["addresses"]})
    used = set(sample_frames)
    for k in range(2840):
        while True:
            fid = "FR%08d" % int(rng.integers(10_000_000, 99_999_999))
            if fid not in used:
                used.add(fid)
                break
        c, z = cz[int(rng.integers(0, len(cz)))]
        act = str(rng.choice(["ADD", "DELETE", "SPLIT"], p=[0.58, 0.34, 0.08]))
        d = datetime.date(2024, 7, 1) + datetime.timedelta(days=int(rng.integers(0, 822)))
        if act == "ADD":
            reason = str(rng.choice(["NEW CONSTRUCTION", "LISTING"], p=[0.7, 0.3]))
            src = str(rng.choice(["USPS", "LISTING"]))
        elif act == "DELETE":
            reason = str(rng.choice(["VACANT", "DEMOLISHED", "DUPLICATE"], p=[0.55, 0.25, 0.20]))
            src = "USPS" if reason == "VACANT" and rng.random() < 0.6 else "FIELD"
        else:
            reason, src = "UNIT SPLIT", "LISTING"
        frows.append([fid, c, z, act, d.isoformat(), reason, src])
        if act == "DELETE" and reason == "VACANT" and rng.random() < 0.07:
            r = d + datetime.timedelta(days=int(rng.integers(5, 90)))
            if r <= datetime.date(2026, 9, 30):
                frows.append([fid, c, z, "RESTORE", r.isoformat(), "DELETED IN ERROR", "FIELD"])
    frows.sort(key=lambda r: (r[4], r[0], r[3]))
    common.write_csv(os.path.join(tdir, "HES_FRAME_MAINTENANCE_2024-07_2026-09.csv"),
                     ["FRAMEID", "CTY", "ZIP", "ACTION", "EFFECTIVE", "REASON", "SOURCE"], frows)
    W["frows"] = frows

    # ---- disposition code table ----
    codes = [["1", "CAPI v3", "Interview", "I"], ["2", "CAPI v3", "Refused", "R"],
             ["3", "CAPI v3", "No one home", "NC"], ["4", "CAPI v3", "Other noninterview, occupied", "O"],
             ["5", "CAPI v3", "Vacant", "NE"], ["6", "CAPI v3", "Demolished or not a housing unit", "NE"],
             ["201", "CAPI 2026", "Complete interview", "I"], ["213", "CAPI 2026", "Refusal", "R"],
             ["216", "CAPI 2026", "No one at home after all contacts", "NC"],
             ["219", "CAPI 2026", "Other eligible, no interview", "O"], ["223", "CAPI 2026", "Vacant", "NE"],
             ["224", "CAPI 2026", "Demolished", "NE"], ["225", "CAPI 2026", "Not a housing unit", "NE"]]
    common.write_csv(os.path.join(tdir, "HES_DISPOSITION_CODES.csv"), ["CODE", "INSTRUMENT", "LABEL", "AAPOR_GROUP"],
                     codes)

    # ---- final weights workbook, one sheet per quarter plus the reissued 2026Q3 sheet ----
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for sheet in REF + ["2026Q3 rev"]:
        ws = wb.create_sheet(sheet)
        ws.append(["CASEID", "LINENO", "FWGT"])
        q = sheet.split()[0]
        ps = sorted([p for p in W["persons_q"] if p["q"] == q],
                    key=lambda r: (case_id(ids, r["aid"], q, A[r["aid"]]["entry"]), r["line"]))
        for p in ps:
            w = wts[(p["aid"], p["line"], q)]
            if sheet.endswith("rev") and p["area"] == REV_AREA:
                w = w * REV_FACTOR
            ws.append([case_id(ids, p["aid"], q, A[p["aid"]]["entry"]), p["line"], round(w, 2)])
    common.xlsx_props(wb, "LMIB Survey Operations", "HES final weights")
    path = os.path.join(tdir, "HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx")
    wb.save(path)
    common.normalise_zip(path)

    # ---- workforce areas workbook ----
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Areas"
    ws.append(["WDA", "Workforce area", "Counties (FIPS)", "Local board"])
    boards = {"01": "Capital Region Workforce Board", "02": "Northern Basin WDB", "03": "Silver Creek Workforce Council",
              "04": "High Plains Workforce Partnership", "05": "Upper River WDB",
              "06": "Southwest Lakes Employment and Training", "07": "Eastern Prairie WIB",
              "08": "Timber Country Workforce Alliance"}
    for code, name, ctys, *_ in world.AREAS:
        ws.append([code, name, ", ".join("59" + c for c in ctys), boards[code]])
    ws2 = wb.create_sheet("County 59041")
    ws2.append(["ZIP", "WDA"])
    for z in sorted(world.SPLIT_ZIPS_03 + world.SPLIT_ZIPS_07):
        ws2.append([z, "03" if z in world.SPLIT_ZIPS_03 else "07"])
    common.xlsx_props(wb, "TDLI Workforce Programs", "Workforce development areas 2026")
    path = os.path.join(tdir, "TDLI_WORKFORCE_AREAS_2026.xlsx")
    wb.save(path)
    common.normalise_zip(path)

    write_distractors(W, tdir, rng)
    docs.write_documents(W, tdir)
    common.set_mtime(tdir)
    return W


def write_distractors(W, tdir, rng):
    # establishment jobs by area and sector, 2025 annual averages
    sectors = [("11", "Agriculture, forestry, fishing and hunting"), ("21", "Mining"), ("23", "Construction"),
               ("31-33", "Manufacturing"), ("42", "Wholesale trade"), ("44-45", "Retail trade"),
               ("48-49", "Transportation and warehousing"), ("52", "Finance and insurance"),
               ("54", "Professional and technical services"), ("61", "Educational services"),
               ("62", "Health care and social assistance"), ("72", "Accommodation and food services"),
               ("81", "Other services"), ("92", "Public administration")]
    rows = []
    for code, name, ctys, adults_k, *_ in world.AREAS:
        jobs = adults_k * 1000 * (0.58 + rng.normal(0, 0.03))
        mix = rng.dirichlet(np.ones(len(sectors)) * 6)
        for (s, sn), m in zip(sectors, mix):
            emp = int(round(jobs * m))
            rows.append([code, s, sn, int(max(3, round(emp / (11 + rng.gamma(2.0, 4.0))))), emp,
                         int(round(emp * (52 * (930 + rng.normal(0, 160)))))])
    common.write_csv(os.path.join(tdir, "QCEW_WDA_SECTOR_2025.csv"),
                     ["WDA", "NAICS", "SECTOR", "ESTABLISHMENTS", "AVG_EMPLOYMENT", "TOTAL_WAGES_USD"], rows)
    # local area unemployment statistics, monthly, the 2025 months benchmarked in March 2026
    rows = []
    months = [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 10)]
    for code, name, ctys, adults_k, ms, ash, _p1 in world.AREAS:
        lf0 = adults_k * 1000 * (0.63 + rng.normal(0, 0.02))
        ur0 = 3.1 + rng.normal(0, 0.5)
        for i, (y, m) in enumerate(months):
            seas = 0.35 * np.cos(2 * np.pi * (m - 2) / 12)
            ur = max(1.8, ur0 + seas + rng.normal(0, 0.12))
            lf = int(round(lf0 * (1 + 0.0015 * i + rng.normal(0, 0.002))))
            status = "B" if y == 2025 else ("R" if (y, m) < (2026, 8) else "P")
            unemp = int(round(lf * ur / 100))
            rows.append(["%04d-%02d" % (y, m), code, lf, lf - unemp, unemp, "%.1f" % (100 * unemp / lf), status])
    common.write_csv(os.path.join(tdir, "LAUS_WDA_MONTHLY_2025-07_2026-09.csv"),
                     ["PERIOD", "WDA", "LABOR_FORCE", "EMPLOYMENT", "UNEMPLOYMENT", "UNEMP_RATE", "STATUS"], rows)
