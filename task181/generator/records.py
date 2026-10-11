"""The data files of the pack, built from the simulated world: the line-list extract, the postcode
workbook, the respiratory admissions extract, the birth records, the antenatal vaccination register,
the school rosters and the influenza extract."""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import sim as S
import world as W

DAY = dt.timedelta(days=1)
LINE_LIST = "pertussis_notifications_2019-2026.csv"
LL_COLUMNS = ["notification_id", "received_utc", "condition", "person_id", "sex", "dob", "postcode", "specimen_date",
              "onset_date", "notifying_lab", "test", "result", "case_status", "mrn", "school_or_childcare", "school_role"]
RESULT = {"PCR": "Bordetella pertussis DNA detected", "Culture": "Bordetella pertussis isolated",
          "Serology": "B. pertussis IgA antibody detected"}
TEST = {"PCR": "PCR", "Culture": "Culture", "Serology": "Serology (IgA)"}
SCHOOL_FIELDS_FROM = dt.date(2026, 9, 1)


def utc_stamp(t):
    return t.astimezone(W.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def line_list_rows(world):
    rows = []
    for c in world["cases"]:
        for i, n in enumerate(c["notifications"]):
            if n["recv"] > W.EXTRACT_LOCAL:
                continue
            sd = n["spec"].date()
            interviewed = c["notifications"][0]["recv"].date() >= SCHOOL_FIELDS_FROM
            rows.append(dict(
                _recv=n["recv"], received_utc=utc_stamp(n["recv"]), condition="Pertussis", person_id=c["person"],
                sex=c["sex"], dob=c["dob"].isoformat(), postcode=c["postcode"], specimen_date=sd.isoformat(),
                onset_date=c["onset"].isoformat() if c["onset"] else "",
                notifying_lab=W.HOSP_LAB if n["route"] == "H" else W.PRIV_LAB, test=TEST[n["test"]],
                result=RESULT[n["test"]], case_status=S.status_for(n["test"], sd),
                mrn="%08d" % c["mrn"] if c["mrn"] else "",
                school_or_childcare=(c["school_text"] or "") if interviewed else "",
                school_role=(c["role"] or "") if interviewed else ""))
    rows.sort(key=lambda r: (r["_recv"], r["person_id"], r["specimen_date"]))
    return rows


def assign_ids(*row_sets):
    """The state system numbers notifications across every condition and unit, in the order received."""
    allrows = sorted((row for rows in row_sets for row in rows),
                     key=lambda r: (r["_recv"], r["condition"], r["person_id"], r["specimen_date"]))
    r = W.stream("notification_ids")
    nid = 2_847_300
    for row in allrows:
        nid += int(r.integers(9, 260))
        row["notification_id"] = "N%08d" % nid


def write_line_list(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=LL_COLUMNS, lineterminator="\r\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return len(rows)


# ------------------------------------------------------------------ the postcode workbook

CONCORDANCE = "postcode_lga_concordance.xlsx"


def _widths(ws, widths):
    for i, wdt in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt


def write_concordance(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Postcode to LGA"
    ws["A1"] = "Residential postcode to local government area, Southern Inland PHU lookup"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("The unit's lookup of residential postcodes to local government areas. RATIO is the share of the "
                "postcode's usual residents living in that LGA. Maintained by Cassandra Dawson; last checked 14/07/2026.")
    hdr = ["POSTCODE", "LOCALITIES", "LGA_NAME", "STATE", "RATIO"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5EE")
    for pc, loc, lga, ratio in sorted(W.CONCORDANCE, key=lambda r: (r[0], r[2])):
        ws.append([pc, loc, lga, "VIC" if pc.startswith("3") else "NSW", ratio])
    for row in ws.iter_rows(min_row=5, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.00"
    ws.freeze_panes = "A5"
    _widths(ws, [11, 70, 24, 7, 8])
    ws2 = wb.create_sheet("LGA population")
    ws2["A1"] = "Population by local government area"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2["A2"] = "Census 2021 usual residents; estimated resident population at 30 June 2025."
    ws2.append([])
    ws2.append(["LGA_NAME", "UNIT_AREA", "CENSUS_2021_URP", "ERP_2025"])
    for c in ws2[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5EE")
    for a in W.AREA_NAMES:
        ws2.append([a, "Y", W.POP[a], W.ERP[a]])
    for a in sorted(W.NEIGHBOUR_POP):
        ws2.append([a, "N", W.NEIGHBOUR_POP[a][0], W.NEIGHBOUR_POP[a][1]])
    for row in ws2.iter_rows(min_row=5, min_col=3, max_col=4):
        for c in row:
            c.number_format = "#,##0"
    ws2.freeze_panes = "A5"
    _widths(ws2, [24, 11, 17, 12])
    wb.properties.creator = W.PEOPLE["data_officer"]
    wb.properties.lastModifiedBy = W.PEOPLE["data_officer"]
    wb.properties.created = dt.datetime(2023, 2, 6, 23, 12, 40)
    wb.properties.modified = dt.datetime(2026, 7, 14, 5, 31, 9)
    wb.save(path)


# ------------------------------------------------------------------ Medicare numbers

def medicare(rng):
    """A valid-format Medicare card number: 8-digit identifier (first digit 2 to 6), check digit, issue."""
    d = [int(rng.integers(2, 7))] + [int(x) for x in rng.integers(0, 10, size=7)]
    w = [1, 3, 7, 9, 1, 3, 7, 9]
    chk = sum(a * b for a, b in zip(d, w)) % 10
    issue = int(rng.integers(1, 6))
    return "".join(map(str, d)) + str(chk) + str(issue)


def spaced(card):
    return "%s %s %s" % (card[:4], card[4:9], card[9])


# ------------------------------------------------------------------ births, mothers and the register

BIRTHS = "birth_records_2024-2026.csv"
REGISTER = "antenatal_vaccinations_2019-2026.parquet"
BIRTH_FACILITY = {"Wagga Wagga": "Wagga Wagga Hospital", "Griffith": "Griffith Hospital", "Leeton": "Griffith Hospital",
                  "Narrandera": "Wagga Wagga Hospital", "Murrumbidgee": "Griffith Hospital", "Hay": "Griffith Hospital",
                  "Edward River": "Deniliquin Hospital", "Junee": "Wagga Wagga Hospital",
                  "Cootamundra-Gundagai": "Wagga Wagga Hospital", "Snowy Valleys": "Tumut Hospital"}


def _dates_between(rng, a, b, n):
    span = (b - a).days
    return [a + DAY * int(x) for x in rng.integers(0, span + 1, size=n)]


def build_mothers_and_births(world):
    """Every pregnancy in the district since 2017 that reaches the register or the birth records, with
    the infant cases' own births placed among them."""
    r = W.stream("births")
    ids = world["ids"]
    used_cards = set()

    def card():
        while True:
            c = medicare(r)
            if c not in used_cards:
                used_cards.add(c)
                return c

    pregnancies = []
    lo, hi = dt.date(2019, 1, 1), dt.date(2027, 3, 31)          # pregnancies still in progress included
    n_days = (hi - lo).days + 1
    weights = np.array([W.POP[a] for a in W.AREA_NAMES], float)
    for i in range(n_days):
        d = lo + DAY * i
        for _ in range(int(r.poisson(2950 / 365.25))):
            area = W.AREA_NAMES[int(r.choice(len(W.AREA_NAMES), p=weights / weights.sum()))]
            pregnancies.append(dict(birth=d, area=area, district=r.random() < 0.72))
    # the infant cases' mothers
    infant_cases = [c for c in world["cases"] if c.get("infant") or (c["age"] < 1 and c["dob"] >= dt.date(2024, 1, 1))]
    designed = {}
    for c in infant_cases:
        designed[c["person"]] = c
    births, mothers = [], []
    for p in pregnancies:
        p["mother"] = None
    # mothers: most have one pregnancy in the window, some two or three
    pool = []
    for p in sorted(pregnancies, key=lambda x: x["birth"]):
        if pool and r.random() < 0.22:
            cand = [m for m in pool if (p["birth"] - m["last"]).days > 420 and m["area"] == p["area"]]
            if cand:
                m = cand[int(r.integers(0, len(cand)))]
                m["last"] = p["birth"]
                p["mother"] = m
                continue
        m = dict(card=card(), irn=int(r.choice([1, 1, 1, 2, 3])), dob=p["birth"] - DAY * int(r.integers(19 * 365, 42 * 365)),
                 area=p["area"], last=p["birth"])
        pool.append(m)
        p["mother"] = m
    for c in infant_cases:
        inf = c.get("infant") or {}
        vacc = inf.get("vacc") or ("A" if r.random() < 0.6 else "E")
        m = dict(card=card(), irn=1, dob=c["dob"] - DAY * int(r.integers(22 * 365, 38 * 365)), area=c["area"] or "Wagga Wagga",
                 last=c["dob"])
        p = dict(birth=c["dob"], area=c["area"] or "Wagga Wagga", district=True, mother=m, case=c, vacc=vacc)
        pregnancies.append(p)
        if vacc == "C":
            pregnancies.append(dict(birth=c["dob"] - DAY * int(r.integers(560, 900)), area=p["area"], district=True,
                                    mother=m, previous_of=c["person"], vacc="A"))
    for p in pregnancies:
        p["gest"] = int(r.choice([36, 37, 38, 38, 39, 39, 39, 40, 40, 40, 41, 35, 34])) if not p.get("case") else int(r.choice([38, 39, 40]))
        p["edd"] = p["birth"] + DAY * int((40 - p["gest"]) * 7 + r.integers(-3, 4))
    return pregnancies, r


def doses_for(p, r):
    """Antenatal doses recorded for one pregnancy."""
    out = []
    birth, gest = p["birth"], p["gest"]
    start = birth - DAY * (7 * gest)
    vacc = p.get("vacc")
    if vacc is None:
        yr = birth.year
        p_dtpa = {2019: 0.74, 2020: 0.77, 2021: 0.78, 2022: 0.76, 2023: 0.75, 2024: 0.79, 2025: 0.81, 2026: 0.82, 2027: 0.82}[yr]
        if r.random() < p_dtpa:
            wk = float(np.clip(r.normal(27.5, 3.2), 18, gest - 0.5))
            out.append(("dTpa", start + DAY * int(wk * 7)))
        if r.random() < 0.52:
            wk = float(r.uniform(10, gest - 1))
            out.append(("Influenza", start + DAY * int(wk * 7)))
        if dt.date(2021, 8, 1) <= birth <= dt.date(2023, 12, 31) and r.random() < 0.45:
            out.append(("COVID-19", start + DAY * int(r.uniform(12, gest - 1) * 7)))
        if birth >= dt.date(2025, 4, 1) and r.random() < 0.38:
            out.append(("RSV", start + DAY * int(r.uniform(28, min(36, gest - 0.5)) * 7)))
        return out
    if vacc == "A":
        out.append(("dTpa", start + DAY * int(r.uniform(24, 30) * 7)))
        if r.random() < 0.5:
            out.append(("Influenza", start + DAY * int(r.uniform(14, 30) * 7)))
    elif vacc == "B":
        out.append(("dTpa", birth - DAY * int(r.integers(8, 12))))
    elif vacc == "D":
        out.append(("Influenza", start + DAY * int(r.uniform(26, 31) * 7)))
    return [x for x in out if x[1] < birth]


BRANDS = {"dTpa": ["Boostrix", "Adacel"], "Influenza": ["Vaxigrip Tetra", "Fluarix Tetra", "Afluria Quad"],
          "COVID-19": ["Comirnaty", "Spikevax"], "RSV": ["Abrysvo"]}
PROVIDERS = ["General practice", "Antenatal clinic", "Community pharmacy", "Aboriginal Medical Service"]


def write_register(path, pregnancies, r):
    import pyarrow as pa
    import pyarrow.parquet as pq
    rows = []
    for p in sorted(pregnancies, key=lambda x: (x["birth"], x["mother"]["card"])):
        for antigen, d in doses_for(p, r):
            if d > dt.date(2026, 10, 2) or d < dt.date(2018, 7, 1):
                continue
            m = p["mother"]
            start = p["birth"] - DAY * (7 * p["gest"])
            rows.append(dict(medicare_card=spaced(m["card"]), irn=m["irn"], mother_dob=m["dob"], dose_date=d,
                             antigen=antigen, vaccine_brand=BRANDS[antigen][int(r.integers(0, len(BRANDS[antigen])))],
                             gestation_weeks_at_dose=round((d - start).days / 7.0, 1), estimated_due_date=p["edd"],
                             provider_type=PROVIDERS[int(r.choice(4, p=[0.58, 0.27, 0.12, 0.03]))],
                             lhd_resident="Y" if p["district"] else "N"))
    rows.sort(key=lambda x: (x["dose_date"], x["medicare_card"], x["antigen"]))
    for i, row in enumerate(rows):
        row["record_id"] = "ANV%07d" % (310000 + i * 3 + int(r.integers(0, 3)))
    cols = ["record_id", "medicare_card", "irn", "mother_dob", "dose_date", "antigen", "vaccine_brand",
            "gestation_weeks_at_dose", "estimated_due_date", "provider_type", "lhd_resident"]
    table = pa.Table.from_pydict({c: [row[c] for row in rows] for c in cols},
                                 schema=pa.schema([("record_id", pa.string()), ("medicare_card", pa.string()),
                                                   ("irn", pa.int8()), ("mother_dob", pa.date32()), ("dose_date", pa.date32()),
                                                   ("antigen", pa.string()), ("vaccine_brand", pa.string()),
                                                   ("gestation_weeks_at_dose", pa.float32()), ("estimated_due_date", pa.date32()),
                                                   ("provider_type", pa.string()), ("lhd_resident", pa.string())]))
    pq.write_table(table, path, compression="snappy", row_group_size=8192)
    return len(rows)


def write_births(path, pregnancies, world, r):
    ids = world["ids"]
    rows = []
    for p in pregnancies:
        if not (dt.date(2024, 1, 1) <= p["birth"] <= dt.date(2026, 9, 30)) or not p["district"] or p.get("previous_of"):
            continue
        twins = 2 if (not p.get("case") and r.random() < 0.012) else 1
        for k in range(twins):
            c = p.get("case")
            mrn = c["mrn"] if c else ids.mrn()
            sex = c["sex"] if c else ("F" if r.random() < 0.487 else "M")
            bw = int(np.clip(r.normal(3380 - 160 * (40 - p["gest"]), 430), 1450, 5100))
            age = (p["birth"] - p["mother"]["dob"]).days / 365.25
            ag = "<20" if age < 20 else "20-24" if age < 25 else "25-29" if age < 30 else "30-34" if age < 35 else "35-39" if age < 40 else "40+"
            area = p["area"]
            pc = (c["postcode"] if c else draw_pc(area, r))
            rows.append(dict(facility=BIRTH_FACILITY.get(area, "Wagga Wagga Hospital"), baby_mrn="%08d" % mrn,
                             birth_date=p["birth"].isoformat(), sex=sex, plurality=twins, gestation_weeks=p["gest"],
                             birthweight_g=bw, mother_medicare_no=p["mother"]["card"] + str(p["mother"]["irn"]),
                             mother_age_group=ag, mother_postcode=pc))
    rows.sort(key=lambda x: (x["birth_date"], x["facility"], x["baby_mrn"]))
    for i, row in enumerate(rows):
        row["birth_id"] = "B%s-%05d" % (row["birth_date"][:4], i + 1)
    cols = ["birth_id", "facility", "baby_mrn", "birth_date", "sex", "plurality", "gestation_weeks", "birthweight_g",
            "mother_medicare_no", "mother_age_group", "mother_postcode"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\r\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return len(rows)


def draw_pc(area, r):
    opts = W.HOME_POSTCODES[area]
    w = np.array([x[1] for x in opts])
    return opts[int(r.choice(len(opts), p=w / w.sum()))][0]


# ------------------------------------------------------------------ respiratory admissions

ADMISSIONS = "respiratory_admissions_2019-2026.csv"
DX = {
    "J21.9": "Acute bronchiolitis, unspecified", "J18.9": "Pneumonia, unspecified", "J06.9": "Acute upper respiratory infection, unspecified",
    "P22.1": "Transient tachypnoea of newborn", "A37.0": "Whooping cough due to Bordetella pertussis",
    "A37.9": "Whooping cough, unspecified", "J20.9": "Acute bronchitis, unspecified", "J45.9": "Asthma, unspecified",
    "J05.0": "Acute obstructive laryngitis [croup]", "J10.1": "Influenza with other respiratory manifestations, seasonal influenza virus identified",
    "J11.1": "Influenza with other respiratory manifestations, virus not identified", "J44.1": "Chronic obstructive pulmonary disease with acute exacerbation, unspecified",
    "U07.1": "COVID-19, virus identified", "J96.0": "Acute respiratory failure", "J69.0": "Pneumonitis due to food and vomit",
    "J22": "Unspecified acute lower respiratory infection", "J12.1": "Respiratory syncytial virus pneumonia",
}
DX_BY_AGE = {
    "infant": [("J21.9", 0.55), ("J18.9", 0.09), ("J06.9", 0.12), ("J22", 0.08), ("J12.1", 0.06), ("J20.9", 0.05), ("A37.9", 0.05)],
    "child": [("J45.9", 0.33), ("J18.9", 0.18), ("J06.9", 0.13), ("J05.0", 0.12), ("J10.1", 0.08), ("J11.1", 0.04), ("J20.9", 0.07), ("J22", 0.05)],
    "adult": [("J18.9", 0.32), ("J45.9", 0.14), ("J44.1", 0.12), ("J10.1", 0.09), ("J11.1", 0.03), ("J20.9", 0.12), ("J22", 0.12), ("J96.0", 0.03), ("A37.0", 0.03)],
    "older": [("J44.1", 0.36), ("J18.9", 0.33), ("J69.0", 0.06), ("J10.1", 0.08), ("J11.1", 0.03), ("J96.0", 0.06), ("J22", 0.08)],
}


def _covid_share(d):
    if d < dt.date(2020, 3, 1):
        return 0.0
    if d < dt.date(2021, 12, 1):
        return 0.06
    if d < dt.date(2023, 1, 1):
        return 0.22
    if d < dt.date(2024, 1, 1):
        return 0.12
    return 0.06


def write_admissions(path, world):
    r = W.stream("admissions")
    ids = world["ids"]
    lo, hi = dt.date(2019, 1, 1), dt.date(2026, 10, 4)
    patients = []
    weights = np.array([W.POP[a] for a in W.AREA_NAMES], float)
    for _ in range(16500):
        area = W.AREA_NAMES[int(r.choice(len(W.AREA_NAMES), p=weights / weights.sum()))]
        band = r.choice(["infant", "child", "adult", "older"], p=[0.03, 0.17, 0.38, 0.42])
        patients.append(dict(mrn=ids.mrn(), area=area, band=band, sex="F" if r.random() < 0.5 else "M",
                             pc=draw_pc(area, r), born=lo - DAY * int(r.integers(0, 365 * 92)) if band != "infant" else None))
    rows = []
    n_days = (hi - lo).days + 1
    caseload = np.array([1.0 + 0.55 * np.cos(2 * np.pi * ((lo + DAY * i).timetuple().tm_yday - 200) / 365.25) for i in range(n_days)])
    for i in range(n_days):
        d = lo + DAY * i
        lam = 10.6 * caseload[i] * (0.72 if dt.date(2020, 4, 1) <= d <= dt.date(2021, 6, 30) else 1.0)
        for _ in range(int(r.poisson(lam))):
            p = patients[int(r.integers(0, len(patients)))]
            band = p["band"]
            if r.random() < _covid_share(d) and band != "infant":
                code = "U07.1"
            else:
                opts = DX_BY_AGE[band]
                w = np.array([x[1] for x in opts])
                code = opts[int(r.choice(len(opts), p=w / w.sum()))][0]
            if band == "infant":
                age = 0
            elif band == "child":
                age = int(r.integers(1, 15))
            elif band == "adult":
                age = int(r.integers(15, 65))
            else:
                age = int(r.integers(65, 98))
            rows.append(adm_row(r, p["mrn"], W.AREA_FACILITY[p["area"]] if r.random() < 0.7 else "Wagga Wagga Hospital",
                                p["sex"], age, p["pc"], d, code))
    # admissions of the notified cases: the designed infants, and some of the other cases around their specimen
    for c in world["cases"]:
        if not c["mrn"]:
            continue
        inf = c.get("infant")
        spec = c["spec"].date()
        fac = W.AREA_FACILITY.get(c["area"], "Wagga Wagga Hospital")
        if inf:
            if inf["adm"] == "A":
                rows.append(adm_row(r, c["mrn"], fac if c["area"] not in ("Junee", "Cootamundra-Gundagai", "Narrandera") else "Wagga Wagga Hospital",
                                    c["sex"], 0, c["postcode"], spec + DAY * inf["adm_off"], "A37.0", stay=(3, 9)))
            elif inf["adm"] == "B":
                code = "P22.1" if inf["adm_off"] < 0 else "J21.9"
                rows.append(adm_row(r, c["mrn"], fac, c["sex"], 0, c["postcode"], spec + DAY * inf["adm_off"], code, stay=(2, 5)))
            continue
        if c["spec"].date() > dt.date(2026, 10, 2):
            continue
        p_adm = 0.32 if c["age"] < 1 else 0.06 if c["age"] < 5 else 0.025 if c["age"] < 60 else 0.08
        if r.random() < p_adm:
            off = int(r.integers(-2, 6))
            ad = spec + DAY * off
            if ad <= dt.date(2026, 10, 3):
                rows.append(adm_row(r, c["mrn"], fac, c["sex"], int(c["age"]), c["postcode"], ad, "A37.0" if c["age"] < 1 or r.random() < 0.7 else "J18.9"))
    rows = [x for x in rows if x["_adm"] <= hi]
    rows.sort(key=lambda x: (x["_adm"], x["facility"], x["mrn"]))
    for i, row in enumerate(rows):
        row["episode_id"] = "%s%06d" % (row["_adm"].strftime("%y"), 100000 + i)
    cols = ["episode_id", "facility", "mrn", "sex", "age_years", "postcode", "admission_date", "separation_date",
            "principal_diagnosis", "diagnosis_description", "care_type", "urgency", "separation_mode"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\r\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return len(rows)


def adm_row(r, mrn, fac, sex, age, pc, d, code, stay=None):
    los = int(r.integers(stay[0], stay[1] + 1)) if stay else int(min(30, r.gamma(1.6, 2.4)))
    sep = d + DAY * los
    mode = "Discharged home" if r.random() < 0.9 else ("Transferred to another hospital" if r.random() < 0.7 else "Died")
    if age < 15 and mode == "Died":
        mode = "Discharged home"
    return dict(_adm=d, facility=fac, mrn=str(int(mrn)), sex=sex, age_years=age, postcode=pc,
                admission_date=d.strftime("%d/%m/%Y"), separation_date=sep.strftime("%d/%m/%Y") if sep <= dt.date(2026, 10, 4) else "",
                principal_diagnosis=code, diagnosis_description=DX[code], care_type="Acute",
                urgency="Emergency" if r.random() < 0.93 else "Planned", separation_mode=mode if sep <= dt.date(2026, 10, 4) else "")


# ------------------------------------------------------------------ school rosters

ROSTERS = "school_rosters_term3_2026.xlsx"
SHEET = {"banna": "Banna Avenue PS", "kooyoo": "Kooyoo Street PS", "wollundry": "Wollundry PS",
         "bolton": "Bolton Park HS", "blowering": "Blowering Road PS", "canal": "Canal Road PS",
         "hurley": "Hurley Street PS", "twynam": "Twynam Street PS", "fernleigh": "Fernleigh Road PS"}
RECEIVED = {"banna": "2026-09-30", "kooyoo": "2026-10-01", "wollundry": "2026-09-17", "bolton": "2026-09-23",
            "blowering": "2026-09-25", "canal": "2026-09-16", "hurley": "2026-09-08", "twynam": "2026-09-29",
            "fernleigh": "2026-09-14"}


def write_rosters(path, world):
    r = W.stream("rosters")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    students = {k: [] for k in SHEET}
    taken = set()
    for c in world["cases"]:
        if c.get("school") in SHEET and c.get("role") == "Student":
            students[c["school"]].append(c)
        taken.add((c["dob"], c["sex"], c["postcode"]))
    # sheets in the order the rosters came in (the workbook was built up over the term)
    for key in sorted(SHEET, key=lambda k: (RECEIVED[k], SHEET[k])):
        sheet = SHEET[key]
        _, name, sector, addr, town, lga, enrol = W.SCHOOL[key]
        ws = wb.create_sheet(sheet)
        ws["A1"] = name
        ws["A1"].font = Font(bold=True, size=12)
        meta = [("Sector", sector), ("Address", "%s, %s NSW" % (addr, town)), ("LGA", lga),
                ("Enrolment (Term 3 2026)", enrol), ("Roster received", "%s (%s)" % (
                    dt.date.fromisoformat(RECEIVED[key]).strftime("%d/%m/%Y"), W.PEOPLE["nurse"]))]
        for i, (k, v) in enumerate(meta, start=2):
            ws.cell(row=i, column=1, value=k).font = Font(bold=True)
            ws.cell(row=i, column=2, value=v)
        hdr = ["student_no", "year", "class", "dob", "sex", "home_postcode"]
        for j, h in enumerate(hdr, start=1):
            c = ws.cell(row=8, column=j, value=h)
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="E4E4E4")
        high = "High" in name
        years = list(range(7, 13)) if high else ["K"] + list(range(1, 7))
        pcs = [p for p, _ in W.HOME_POSTCODES[lga]] if lga in W.HOME_POSTCODES else ["2650"]
        clean = W.CLEAN_POSTCODES[lga]
        recs = []
        for _ in range(enrol - len(students[key])):
            while True:
                y = years[int(r.integers(0, len(years)))]
                yi = 0 if y == "K" else y
                age = 5.3 + yi + float(r.uniform(0, 1))
                dob = dt.date(2026, 9, 1) - DAY * int(age * 365.25)
                rec = [y, dob, "F" if r.random() < 0.5 else "M", clean[int(r.integers(0, len(clean)))]]
                if (rec[1], rec[2], rec[3]) not in taken:
                    break
            recs.append(rec)
        for c in students[key]:
            age = (dt.date(2026, 9, 1) - c["dob"]).days / 365.25
            yi = int(max(0, min(12, round(age - 5.8))))
            y = yi if (high and yi >= 7) or (not high and 1 <= yi <= 6) else (7 if high else ("K" if yi < 1 else 6))
            recs.append([y, c["dob"], c["sex"], c["postcode"]])
        recs.sort(key=lambda x: (0 if x[0] == "K" else int(x[0]), x[1]))
        base = int(r.integers(41000, 88000))
        for i, (y, dob, sex, pc) in enumerate(recs, start=9):
            cls = "%s%s" % (y, "ABCD"[int(r.integers(0, 3 if enrol > 250 else 2))])
            ws.cell(row=i, column=1, value=base + (i - 9) * 7 + int(r.integers(0, 5)))
            ws.cell(row=i, column=2, value=y)
            ws.cell(row=i, column=3, value=cls)
            ws.cell(row=i, column=4, value=dob).number_format = "dd/mm/yyyy"
            ws.cell(row=i, column=5, value=sex)
            ws.cell(row=i, column=6, value=pc)
        ws.freeze_panes = "A9"
        _widths(ws, [24, 26, 8, 12, 6, 14])
    wb.properties.creator = W.PEOPLE["nurse"]
    wb.properties.lastModifiedBy = W.PEOPLE["nurse"]
    wb.properties.created = dt.datetime(2026, 9, 8, 3, 2, 51)
    wb.properties.modified = dt.datetime(2026, 10, 1, 6, 48, 13)
    wb.save(path)
    return {k: len(v) for k, v in students.items()}


# ------------------------------------------------------------------ influenza notifications (2026)

INFLUENZA = "influenza_notifications_2026.csv"
FLU_RESULTS = [("Influenza A(H3N2) RNA detected", 0.46), ("Influenza A(H1N1)pdm09 RNA detected", 0.21),
               ("Influenza A virus RNA detected (not subtyped)", 0.13), ("Influenza B virus RNA detected", 0.20)]


def write_csv(path, rows, cols):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\r\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return len(rows)


FLU_COLUMNS = ["notification_id", "received_utc", "condition", "person_id", "sex", "dob", "postcode", "specimen_date",
               "onset_date", "notifying_lab", "test", "result", "case_status"]


def influenza_rows(world):
    r = W.stream("influenza")
    ids = world["ids"]
    lo, hi = dt.date(2026, 1, 1), dt.date(2026, 10, 4)
    rows = []
    weights = np.array([W.POP[a] for a in W.AREA_NAMES], float)
    for i in range((hi - lo).days + 1):
        d = lo + DAY * i
        doy = d.timetuple().tm_yday
        lam = 0.9 + 21.0 * np.exp(-0.5 * ((doy - 212) / 24.0) ** 2)
        for _ in range(int(r.poisson(lam))):
            area = W.AREA_NAMES[int(r.choice(len(W.AREA_NAMES), p=weights / weights.sum()))]
            visitor = r.random() < 0.04
            pc = W.VISITOR_POSTCODES[int(r.integers(0, len(W.VISITOR_POSTCODES)))][0] if visitor else draw_pc(area, r)
            dd = d
            if dd.weekday() == 6 and r.random() < 0.7:
                dd = dd + DAY
            route = "P" if r.random() < W.PRIVATE_SHARE[area] * 0.8 else "H"
            if route == "P" and dd.weekday() == 6:
                dd = dd + DAY
            if route == "P":
                # Inland Pathology runs influenza PCR at its regional laboratory: the daily van, a result next day
                t = S.collection_time(dd, "P", r)
                rd = dd + DAY * int(r.choice([1, 1, 2, 2, 3]))
                while rd.weekday() == 6 or rd in W.HOLIDAYS:
                    rd += DAY
                recv = S.plus_minutes(rd, 9 * 60 + r.random() * 540)
            else:
                t = S.collection_time(dd, "H", r)
                recv = S.hospital_received(t, area, S.draws(r))
            if recv > W.EXTRACT_LOCAL:
                continue
            age = float(r.choice([r.uniform(0, 5), r.uniform(5, 18), r.uniform(18, 65), r.uniform(65, 95)], p=[0.16, 0.24, 0.38, 0.22]))
            res = FLU_RESULTS[int(r.choice(4, p=[x[1] for x in FLU_RESULTS]))][0]
            onset = (dd - DAY * int(r.integers(1, 6))).isoformat() if r.random() < 0.55 else ""
            rows.append(dict(_recv=recv, received_utc=utc_stamp(recv), condition="Influenza", person_id=ids.person(),
                             sex="F" if r.random() < 0.52 else "M", dob=(dd - DAY * int(age * 365.25)).isoformat(), postcode=pc,
                             specimen_date=dd.isoformat(), onset_date=onset,
                             notifying_lab=W.HOSP_LAB if route == "H" else W.PRIV_LAB, test="PCR", result=res,
                             case_status="Confirmed"))
    rows.sort(key=lambda x: (x["_recv"], x["person_id"]))
    return rows
