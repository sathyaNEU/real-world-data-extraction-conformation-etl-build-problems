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
REV_AREA = "06"           # the area whose 2025 population control was revised before the 2026Q3 final weights
REV_FACTOR = 1.0637


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


def build_ids(W, rng):
    """Frame ids, the old system's case ids and the new system's case ids, all drawn, none sequential."""
    n = len(W["addresses"])
    fr = rng.choice(np.arange(10_000_000, 99_999_999), size=n, replace=False)
    old = rng.choice(np.arange(1_000_000, 9_999_999), size=n, replace=False)
    new = rng.choice(np.arange(100_000_000, 999_999_999), size=n, replace=False)
    ids = {}
    for a, f, o, nw in zip(W["addresses"], fr, old, new):
        ids[a["aid"]] = dict(frame="FR%08d" % f, old="TH%07d" % o, new="H%09d" % nw)
    return ids


def case_id(ids, aid, q):
    return ids[aid]["new"] if world.QUARTERS.index(q) >= world.QUARTERS.index(world.MIGRATION_Q) else ids[aid]["old"]


def controls(rng):
    """Adults 16 and over by area, age group and sex (July 2025 estimates), as the state demographer issues them."""
    base = np.array([0.155, 0.168, 0.162, 0.150, 0.160, 0.205])
    ctl = {}
    for code, name, ctys, adults_k, ms, ash in world.AREAS:
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
        n_iss = len(hs)
        w0 = W["frame_size"][area] / n_iss
        elig = [h for h in hs if h["outcome"] != "INELIGIBLE"]
        comp = [h for h in elig if h["outcome"] == "COMPLETE"]
        adj = len(elig) / len(comp)
        for h in comp:
            hw[(h["aid"], q)] = w0 * adj
    out = {}
    for q in world.QUARTERS:
        cells = {}
        for p in W["persons_q"]:
            if p["q"] != q:
                continue
            key = (p["area"], agegroup(p["age"]), p["sex"])
            cells.setdefault(key, []).append(p)
        for key, ps in cells.items():
            tot = sum(hw[(p["aid"], q)] for p in ps)
            f = ctl[key] / tot
            for p in ps:
                out[(p["aid"], p["line"], q)] = hw[(p["aid"], q)] * f
    return out


def write_target(W, tdir):
    rng = W["rng_ops"]
    os.makedirs(tdir, exist_ok=True)
    ids = build_ids(W, rng)
    ctl = controls(rng)
    wts = weights(W, ctl)
    W["ids"], W["ctl"], W["wts"] = ids, ctl, wts

    # ---- person file (the analysis extract the bureau builds each quarter) ----
    rows = []
    for p in sorted(W["persons_q"], key=lambda r: (world.QUARTERS.index(r["q"]), case_id(ids, r["aid"], r["q"]), r["line"])):
        emp = p["lfs"] in (1, 2)
        if emp:
            h = 20 + int(rng.integers(0, 15)) if p["pt"] else 35 + int(rng.integers(0, 16))
            if rng.random() < 0.38:
                h = 40 if not p["pt"] else 20
            if not p["self_rep"] and rng.random() < 0.06:
                h = -9
            hrs = h
            occ = OCC_SOC[p["occ"]]
            mjh = 1 if p["mjh_rep"] == 1 else 2
        else:
            hrs, occ, mjh = -1, "", -1
        if p["lfs"] == 4:
            want = p["want"]
        elif p["lfs"] == 3 and world.QUARTERS.index(p["q"]) >= world.QUARTERS.index(world.MIGRATION_Q):
            want = 1          # the 2026 instrument asks every adult without work whether they want a job
        else:
            want = -1
        rows.append([p["q"], case_id(ids, p["aid"], p["q"]), p["line"], p["age"], p["sex"], p["rel"],
                     p["area"], p["lfs"], hrs, occ, mjh, p["resp_line"], want])
    common.write_csv(os.path.join(tdir, "HES_PERSON_2025Q1_2026Q3.csv"),
                     ["SURVEY_QTR", "CASEID", "LINENO", "AGE", "SEX", "RELREF", "HES_AREA", "LFSTAT", "HRSMAIN",
                      "OCCMAJ", "MJH", "RESPLINE", "WANTJOB"], rows)

    # ---- household disposition file (field operations extract, both CAPI systems) ----
    hrows = []
    W["parallel"] = []
    W["reissued"] = []
    mig = world.QUARTERS.index(world.MIGRATION_Q)
    for h in W["hh_q"]:
        q = h["q"]
        qi = world.QUARTERS.index(q)
        yr, mo = world.FIELD_MONTH[q]
        new = qi >= mig
        cid = case_id(ids, h["aid"], q)
        day = int(rng.integers(9, 25))
        dt = datetime.date(yr, mo, day)
        intv = "I%03d" % (100 + (int(world.area_index()[h["area"]]) * 37 + int(rng.integers(0, 29))) % 900)
        if h["outcome"] == "INELIGIBLE":
            kind = h["vacant_kind"]
            first_vac = kind != "NOT_A_DWELLING" and (h["wave"] - 1 + h["entry"]) == next(
                a["vacant_from"] for a in [W["addr_by_id"][h["aid"]]])
            if first_vac and rng.random() < 0.62:
                code = 216 if new else 3          # the interviewer found no one at home
            else:
                code = {"VACANT": 223, "DEMOLISHED": 224, "NOT_A_DWELLING": 225}[kind] if new else \
                       {"VACANT": 5, "DEMOLISHED": 6, "NOT_A_DWELLING": 6}[kind]
            hrows.append([q, cid, ids[h["aid"]]["frame"], "RG%s" % _entry_label(h["entry"]), h["wave"],
                          h["county"], h["zip"], code, dt.isoformat(), "", "", intv, ""])
            continue
        if h["outcome"] == "COMPLETE":
            slot = h["slot"]
            if slot == "SAT":
                while dt.weekday() != 5:
                    dt = dt + datetime.timedelta(days=1)
                hh, mm = int(rng.integers(10, 16)), int(rng.integers(0, 60))
            else:
                while dt.weekday() >= 5:
                    dt = dt + datetime.timedelta(days=1)
                if slot == "EVE":
                    hh, mm = int(rng.integers(17, 21)), int(rng.integers(0, 60))
                else:
                    hh, mm = int(rng.integers(10, 16)), int(rng.integers(0, 60))
            local = datetime.datetime(dt.year, dt.month, dt.day, hh, mm)
            utc = local - datetime.timedelta(hours=mt_offset(dt))
            mode = "CAPI-T" if rng.random() < 0.21 and h["wave"] > 1 else "CAPI-P"
            if h.get("refusal_converted"):
                d0 = dt - datetime.timedelta(days=int(rng.integers(5, 12)))
                hrows.append([q, cid, ids[h["aid"]]["frame"], "RG%s" % _entry_label(h["entry"]), h["wave"],
                              h["county"], h["zip"], 213 if new else 2, d0.isoformat(), "", "", intv, ""])
                W["reissued"].append((h["aid"], q))
            hrows.append([q, cid, ids[h["aid"]]["frame"], "RG%s" % _entry_label(h["entry"]), h["wave"],
                          h["county"], h["zip"], 201 if new else 1, dt.isoformat(),
                          utc.strftime("%Y-%m-%dT%H:%M:00Z"), mode, intv, h["n_adults"]])
            if qi == mig and h["wave"] > 1 and rng.random() < 0.075:
                # parallel-run fortnight: the old system logged the same interview under its own case id
                hrows.append([q, ids[h["aid"]]["old"], ids[h["aid"]]["frame"], "RG%s" % _entry_label(h["entry"]),
                              h["wave"], h["county"], h["zip"], 1, dt.isoformat(),
                              utc.strftime("%Y-%m-%dT%H:%M:00Z"), mode, intv, h["n_adults"]])
                W["parallel"].append(h["aid"])
            continue
        code = (213 if new else 2) if h["outcome"] == "REFUSED" else \
               ((216 if new else 3) if rng.random() < 0.78 else (219 if new else 4))
        hrows.append([q, cid, ids[h["aid"]]["frame"], "RG%s" % _entry_label(h["entry"]), h["wave"],
                      h["county"], h["zip"], code, dt.isoformat(), "", "", intv, ""])
    hrows.sort(key=lambda r: (world.QUARTERS.index(r[0]), r[2], r[8], r[7]))
    common.write_csv(os.path.join(tdir, "HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv"),
                     ["SURVEY_QTR", "CASEID", "FRAMEID", "ROTGRP", "WAVE", "CTY", "ZIP", "DISPO", "DISPO_DATE",
                      "START_UTC", "MODE", "INTV_ID", "NUM_ADULTS"], hrows)

    # ---- the CAPI migration crosswalk: every case live in both systems at the change ----
    xrows = []
    for a in W["addresses"]:
        live = [a["entry"] + w for w in range(4)]
        if (mig - 1) in live and mig in live:
            xrows.append([ids[a["aid"]]["old"], ids[a["aid"]]["new"], "2026-04-27"])
    xrows.sort()
    common.write_csv(os.path.join(tdir, "HES_CASEID_CROSSWALK_CAPI2026.csv"),
                     ["OLD_CASEID", "NEW_CASEID", "MIGRATED_ON"], xrows)

    # ---- frame maintenance log ----
    frows = []
    W["frame_deleted_q"] = {}
    for a in W["addresses"]:
        if a["vacant_from"] is not None and 0 <= a["vacant_from"] < len(world.QUARTERS) + 4:
            vq = a["vacant_from"]
            if vq < len(world.QUARTERS):
                yr, mo = world.FIELD_MONTH[world.QUARTERS[vq]]
                eff = datetime.date(yr, mo, 1) - datetime.timedelta(days=int(rng.integers(8, 40)))
            else:
                eff = datetime.date(2026, 9, 1) + datetime.timedelta(days=int(rng.integers(10, 50)))
            reason = "VACANT-6M" if a["vacant_kind"] == "VACANT" else "DEMOLISHED"
            frows.append([ids[a["aid"]]["frame"], a["county"], a["zip"], "DELETE", eff.isoformat(), reason, "FIELD"])
            W["frame_deleted_q"][a["aid"]] = vq
    # deletions entered in error and restored before the next field period
    W["restored"] = []
    occ = [a for a in W["addresses"] if a["occupied0"] and a["vacant_from"] is None]
    pick = rng.choice(len(occ), size=46, replace=False)
    for k in sorted(pick):
        a = occ[k]
        qs = [a["entry"] + w for w in range(4) if 0 <= a["entry"] + w < len(world.QUARTERS)]
        if not qs:
            continue
        qd = qs[int(rng.integers(0, len(qs)))]
        yr, mo = world.FIELD_MONTH[world.QUARTERS[qd]]
        eff = datetime.date(yr, mo, 1) - datetime.timedelta(days=int(rng.integers(20, 50)))
        rst = eff + datetime.timedelta(days=int(rng.integers(6, 18)))
        frows.append([ids[a["aid"]]["frame"], a["county"], a["zip"], "DELETE", eff.isoformat(), "VACANT-6M", "USPS"])
        frows.append([ids[a["aid"]]["frame"], a["county"], a["zip"], "RESTORE", rst.isoformat(), "OCCUPIED", "FIELD"])
        W["restored"].append(a["aid"])
    # the rest of the frame's routine traffic (addresses never in sample)
    cty_zip = [(a["county"], a["zip"]) for a in W["addresses"]]
    for k in range(2614):
        cz = cty_zip[int(rng.integers(0, len(cty_zip)))]
        act = rng.choice(["ADD", "DELETE", "ADD", "SPLIT"], p=[0.52, 0.30, 0.10, 0.08])
        d = datetime.date(2024, 7, 1) + datetime.timedelta(days=int(rng.integers(0, 820)))
        reason = {"ADD": "NEW-CONSTRUCTION", "DELETE": rng.choice(["DEMOLISHED", "VACANT-6M", "DUPLICATE"]),
                  "SPLIT": "UNIT-SPLIT"}[str(act)]
        frows.append(["FR%08d" % int(rng.integers(10_000_000, 99_999_999)), cz[0], cz[1], str(act), d.isoformat(),
                      str(reason), str(rng.choice(["USPS", "LISTING", "FIELD"]))])
    frows.sort(key=lambda r: (r[4], r[0], r[3]))
    common.write_csv(os.path.join(tdir, "HES_FRAME_MAINTENANCE_2024-07_2026-09.csv"),
                     ["FRAMEID", "CTY", "ZIP", "ACTION", "EFFECTIVE", "REASON", "SOURCE"], frows)

    # ---- disposition code table ----
    codes = [["1", "PAPI/CAPI v3", "Interview, complete", "I"], ["2", "PAPI/CAPI v3", "Refusal", "R"],
             ["3", "PAPI/CAPI v3", "No one home", "NC"], ["4", "PAPI/CAPI v3", "Other noninterview", "O"],
             ["5", "PAPI/CAPI v3", "Vacant", "NE"], ["6", "PAPI/CAPI v3", "Demolished or not a housing unit", "NE"],
             ["201", "CAPI 2026", "Complete interview", "I"], ["213", "CAPI 2026", "Refusal", "R"],
             ["216", "CAPI 2026", "No one at home after all contacts", "NC"],
             ["219", "CAPI 2026", "Other eligible, no interview", "O"], ["223", "CAPI 2026", "Vacant", "NE"],
             ["224", "CAPI 2026", "Demolished", "NE"], ["225", "CAPI 2026", "Not a housing unit", "NE"]]
    common.write_csv(os.path.join(tdir, "HES_DISPOSITION_CODES.csv"),
                     ["CODE", "INSTRUMENT", "LABEL", "AAPOR_GROUP"], codes)

    # ---- final weights workbook, one sheet per quarter plus the revised 2026Q3 sheet ----
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    W["wts_rev"] = {}
    for q in world.REF_QUARTERS + ["2026Q3 rev"]:
        ws = wb.create_sheet(q)
        ws.append(["CASEID", "LINENO", "FWGT"])
        qq = q.split()[0]
        ps = sorted([p for p in W["persons_q"] if p["q"] == qq],
                    key=lambda r: (case_id(ids, r["aid"], qq), r["line"]))
        for p in ps:
            w = wts[(p["aid"], p["line"], qq)]
            if q.endswith("rev") and p["area"] == REV_AREA:
                w = w * REV_FACTOR
            if q.endswith("rev"):
                W["wts_rev"][(p["aid"], p["line"])] = round(w, 2)
            ws.append([case_id(ids, p["aid"], qq), p["line"], round(w, 2)])
    common.xlsx_props(wb, "LMIB Survey Operations", "HES final weights")
    path = os.path.join(tdir, "HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx")
    wb.save(path)
    common.normalise_zip(path)

    # ---- workforce areas workbook (areas, the split county, population controls) ----
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Areas"
    ws.append(["WDA", "Workforce area", "Counties (FIPS)", "Local board"])
    boards = {"01": "Capital Region Workforce Board", "02": "Northern Basin WDB", "03": "Silver Creek Workforce Council",
              "04": "High Plains Workforce Partnership", "05": "Upper River WDB",
              "06": "Southwest Lakes Employment & Training", "07": "Eastern Prairie WIB",
              "08": "Timber Country Workforce Alliance"}
    for code, name, ctys, *_ in world.AREAS:
        ws.append([code, name, ", ".join("59" + c for c in ctys), boards[code]])
    ws2 = wb.create_sheet("County 59041")
    ws2.append(["ZIP", "WDA"])
    for z in world.SPLIT_ZIPS_03:
        ws2.append([z, "03"])
    for z in world.SPLIT_ZIPS_07:
        ws2.append([z, "07"])
    ws3 = wb.create_sheet("Adults 16+ Jul 2025")
    ws3.append(["WDA", "Age group", "Male", "Female"])
    for code, *_ in world.AREAS:
        for g, (lo, hi) in enumerate(AGEGROUPS):
            lab = "%d-%d" % (lo, hi) if hi < 120 else "%d+" % lo
            ws3.append([code, lab, ctl[(code, g, 1)], ctl[(code, g, 2)]])
    common.xlsx_props(wb, "TDLI Workforce Programs", "Workforce areas 2026")
    path = os.path.join(tdir, "TDLI_WORKFORCE_AREAS_2026.xlsx")
    wb.save(path)
    common.normalise_zip(path)

    # ---- distractors ----
    write_distractors(W, tdir, rng)

    # ---- documents ----
    docs.write_documents(W, tdir)
    common.set_mtime(tdir)
    return W


def _entry_label(e):
    qi = e
    y = 2025 + (qi // 4)
    qn = qi % 4 + 1
    return "%02dQ%d" % (y % 100, qn)


def write_distractors(W, tdir, rng):
    # QCEW-style establishment jobs by area and sector, 2025 annual average
    sectors = [("11", "Agriculture"), ("21", "Mining"), ("23", "Construction"), ("31-33", "Manufacturing"),
               ("42", "Wholesale"), ("44-45", "Retail"), ("48-49", "Transportation"), ("52", "Finance"),
               ("54", "Professional services"), ("61", "Education"), ("62", "Health care"),
               ("72", "Accommodation and food"), ("81", "Other services"), ("92", "Public administration")]
    rows = []
    for code, name, ctys, adults_k, *_ in world.AREAS:
        jobs = adults_k * 1000 * (0.58 + rng.normal(0, 0.03))
        mix = rng.dirichlet(np.ones(len(sectors)) * 6)
        for (s, sn), m in zip(sectors, mix):
            est = int(rng.integers(40, 900))
            rows.append([code, s, sn, est, int(round(jobs * m)), int(round(jobs * m * (980 + rng.normal(0, 140)) * 52))])
    common.write_csv(os.path.join(tdir, "QCEW_WDA_SECTOR_2025.csv"),
                     ["WDA", "NAICS", "SECTOR", "ESTABLISHMENTS", "AVG_EMPLOYMENT", "TOTAL_WAGES_USD"], rows)
    # UI wage records: workers paid by two or more employers in the quarter, by WDA of the primary employer
    rows = []
    W["ui_rate"] = {}
    for code, name, ctys, adults_k, ms, ash in world.AREAS:
        for q in ["2025Q4", "2026Q1", "2026Q2"]:
            workers = int(adults_k * 1000 * 0.52 * (1 + rng.normal(0, 0.01)))
            rate = 0.083 + 0.012 * ash * 10 - 0.010 * ms + rng.normal(0, 0.002)
            multi = int(round(workers * rate))
            rows.append([q, code, workers, multi])
            W["ui_rate"].setdefault(code, []).append(multi / workers)
    common.write_csv(os.path.join(tdir, "UI_WAGE_RECORDS_MULTIEMPLOYER_2025Q4_2026Q2.csv"),
                     ["QUARTER", "WDA_PRIMARY_EMPLOYER", "WORKERS_WITH_WAGES", "WORKERS_2PLUS_EMPLOYERS"], rows)
