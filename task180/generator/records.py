"""Write the registry extract as the national health data service delivers it: the prescription registry's
dispensings, the patient registry's contacts and diagnoses in both record structures, the civil registration
extract, the Agency's matched comparator extract, the ATC/DDD index and the national population and admission
counts."""
import csv
import datetime as dt

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import hospital as H
import sim as S
import world as W

PRESCRIPTIONS = "prescription_registry_2018-2026.parquet"
CONTACTS = "patient_registry_contacts_2018-2026.parquet"
DIAGNOSES = "patient_registry_diagnoses_2018-2026.parquet"
CIVIL = "civil_registration_extract.csv"
MATCHED = "matched_comparators.csv"
ATC = "atc_ddd_index_2026.csv"
POPULATION = "population_and_admissions_2022-2025.csv"

MIN_DAY = H.MIN_DAY
EPOCH_NP = np.datetime64("2018-01-01T00:00", "m")


def iso(n):
    return W.date_of(n).isoformat()


def pnrs(P):
    return np.array([W.pseudonym(i) for i in range(len(P["cohort"]))], object)


# ------------------------------------------------------------------ prescriptions

def write_prescriptions(path, world, pnr):
    disp, ns = world["disp"], world["nsaid"]
    pid = np.r_[disp["pid"], ns["pid"]]
    day = np.r_[disp["day"], ns["day"]]
    vnr = np.r_[disp["vnr"], ns["vnr"]].astype(object)
    apk = np.r_[disp["apk"], ns["apk"]].astype(np.int64)
    sub = np.r_[disp["substance"], ns["substance"]].astype(object)
    code = {s: W.atc_on(s, W.D_END) for s in set(sub.tolist())}
    atc = pd.Series(sub).map(code).to_numpy(object)
    atc = np.where((sub == "corinurad") & (day < W.D_CODE), "M04AX02", atc).astype(object)
    vs = pd.Series(vnr)
    size = vs.map({v: p["size"] for v, p in W.PACK.items()}).to_numpy(np.int32)
    strength = vs.map({v: float(p["strength"]) for v, p in W.PACK.items()}).to_numpy(float)
    vol = vs.map({v: round(W.ddd_per_pack(v), 2) for v in W.PACK}).to_numpy(float)
    order = np.lexsort((atc, day, pnr[pid]))
    t = pa.table({
        "pnr": pa.array(pnr[pid][order].tolist(), pa.string()),
        "eksd": pa.array((np.datetime64("2018-01-01", "D") + day[order]).astype("datetime64[D]"), pa.date32()),
        "atc": pa.array(atc[order].tolist(), pa.string()),
        "vnr": pa.array(vnr[order].tolist(), pa.string()),
        "apk": pa.array(apk[order], pa.int16()),
        "packsize": pa.array(size[order], pa.int16()),
        "strnum": pa.array(strength[order], pa.float64()),
        "strunit": pa.array(["mg"] * len(order), pa.string()),
        "volume": pa.array(vol[order], pa.float64()),
        "voltypetxt": pa.array(["DDD"] * len(order), pa.string()),
    })
    pq.write_table(t, path, compression="zstd", row_group_size=250_000, use_dictionary=True)
    return t.num_rows


# ------------------------------------------------------------------ contacts and diagnoses

def registry_records(C, D, hosp_codes):
    """Map the simulated contacts onto the two record structures. Returns contact and diagnosis columns."""
    lpr2 = C["start"] < W.D_LPR3 * MIN_DAY
    ed = (C["dept"] % 1000) == int(W.SPECIALTY_DEPT["Akutmedicin"])
    planned = C["prio"] == 3
    n = len(C["pid"])
    rows = {"pid": [], "kilde": [], "pattype": [], "kontakttype": [], "prioritet": [], "start": [], "end": [],
            "dept": [], "src": []}
    # LPR3 contacts, one per department stay
    m3 = ~lpr2
    rows["pid"].append(C["pid"][m3])
    rows["kilde"].append(np.full(m3.sum(), "LPR3", object))
    rows["pattype"].append(np.full(m3.sum(), None, object))
    rows["kontakttype"].append(np.where(C["ctype"][m3] == 1, "ALCA10", "ALCA00").astype(object))
    rows["prioritet"].append(np.where(C["prio"][m3] == 1, "ATA1", "ATA3").astype(object))
    rows["start"].append(C["start"][m3])
    end = C["end"][m3].astype(float)
    end[C["end"][m3] >= (W.D_END + 1) * MIN_DAY] = np.nan
    rows["end"].append(end)
    rows["dept"].append(C["dept"][m3])
    rows["src"].append(np.where(m3)[0])
    # LPR2 stays and emergency room visits: admission date and hour, discharge date
    m2 = lpr2 & ~planned
    rows["pid"].append(C["pid"][m2])
    rows["kilde"].append(np.full(m2.sum(), "LPR2", object))
    rows["pattype"].append(np.where(ed[m2], "3", "0").astype(object))
    rows["kontakttype"].append(np.full(m2.sum(), None, object))
    rows["prioritet"].append(np.full(m2.sum(), None, object))
    rows["start"].append((C["start"][m2] // 60) * 60)
    rows["end"].append(((C["end"][m2] // MIN_DAY) * MIN_DAY).astype(float))
    rows["dept"].append(C["dept"][m2])
    rows["src"].append(np.where(m2)[0])
    # LPR2 outpatient courses: one record per person and department, spanning its visits
    mo = np.where(lpr2 & planned)[0]
    key = C["pid"][mo] * 10 ** 8 + C["dept"][mo]
    order = np.lexsort((C["start"][mo], key))
    mo, key = mo[order], key[order]
    first = np.r_[True, key[1:] != key[:-1]]
    grp = np.cumsum(first) - 1
    g_first = mo[first]
    g_last = np.zeros(first.sum(), np.int64)
    np.maximum.at(g_last, grp, C["start"][mo])
    # a course ends at its last LPR2 visit (one still running at the change to LPR3 goes on as LPR3 contacts)
    g_end = (g_last // MIN_DAY) * MIN_DAY
    rows["pid"].append(C["pid"][g_first])
    rows["kilde"].append(np.full(len(g_first), "LPR2", object))
    rows["pattype"].append(np.full(len(g_first), "2", object))
    rows["kontakttype"].append(np.full(len(g_first), None, object))
    rows["prioritet"].append(np.full(len(g_first), None, object))
    rows["start"].append((C["start"][g_first] // MIN_DAY) * MIN_DAY)
    rows["end"].append(g_end.astype(float))
    rows["dept"].append(C["dept"][g_first])
    rows["src"].append(g_first)
    R = {k: np.concatenate(v) for k, v in rows.items()}
    # every simulated contact maps to the record that carries it (a course carries all its visits)
    rec_of = np.full(n, -1, np.int64)
    base = len(R["pid"]) - len(g_first)
    rec_of[R["src"][:base]] = np.arange(base)
    rec_of[mo] = base + grp
    # diagnoses follow their contact; a course takes its first visit's action diagnosis and the rest as secondary
    dc = rec_of[D["cid"]]
    code = D["code"]
    typ = D["type"].copy()
    in_course = dc >= base
    first_visit = np.zeros(n, bool)
    first_visit[g_first] = True
    demote = in_course & (typ == "A") & ~first_visit[D["cid"]]
    typ = np.where(demote, "B", typ)
    return R, dict(rec=dc, code=code, type=typ)


def write_contacts(cpath, dpath, C, D, hosp_codes, pnr):
    R, Dx = registry_records(C, D, hosp_codes)
    n = len(R["pid"])
    r = W.rng("records", "ids")
    # identifiers: LPR2 record numbers and LPR3 contact keys, in no meaningful order
    is2 = R["kilde"] == "LPR2"
    ids = np.empty(n, object)
    perm2 = r.permutation(is2.sum())
    ids[is2] = np.array(["%016d" % (3418000000000000 + 7919 * int(x) + 13) for x in perm2], object)
    perm3 = r.permutation((~is2).sum())
    ids[~is2] = np.array(["%d" % (95100000000 + 104729 * int(x) % 900000000000) for x in perm3], object)
    assert len(set(ids.tolist())) == n
    depts = np.unique(R["dept"])
    sor = {int(dc): W.sor_code("%07d" % dc) for dc in depts}
    shak = {int(dc): "%07d" % dc for dc in depts}
    dser = pd.Series(R["dept"])
    afd = np.where(is2, dser.map(shak).to_numpy(object), dser.map(sor).to_numpy(object)).astype(object)
    spec = {int(c): s for c, s in W.DEPARTMENTS}
    speciale = pd.Series(R["dept"] % 1000).map(spec).to_numpy(object)
    order = np.lexsort((ids, R["start"], pnr[R["pid"]]))
    start = EPOCH_NP + R["start"][order].astype("timedelta64[m]")
    endv = R["end"][order]
    end = np.where(np.isnan(endv), np.datetime64("NaT"), EPOCH_NP + np.nan_to_num(endv).astype(np.int64).astype("timedelta64[m]"))
    t = pa.table({
        "pnr": pa.array(pnr[R["pid"]][order].tolist(), pa.string()),
        "kontakt_id": pa.array(ids[order].tolist(), pa.string()),
        "kilde": pa.array(R["kilde"][order].tolist(), pa.string()),
        "pattype": pa.array(R["pattype"][order].tolist(), pa.string()),
        "kontakttype": pa.array(R["kontakttype"][order].tolist(), pa.string()),
        "prioritet": pa.array(R["prioritet"][order].tolist(), pa.string()),
        "starttid": pa.array(start.astype("datetime64[s]"), pa.timestamp("s")),
        "sluttid": pa.array(end.astype("datetime64[s]"), pa.timestamp("s")),
        "afdeling": pa.array(afd[order].tolist(), pa.string()),
        "speciale": pa.array(speciale[order].tolist(), pa.string()),
    })
    pq.write_table(t, cpath, compression="zstd", row_group_size=250_000, use_dictionary=True)
    # diagnoses: one row per record, code and type; a code that is a record's action diagnosis is not repeated
    # among its secondary diagnoses
    dx = pd.DataFrame({"kontakt_id": ids[Dx["rec"]], "diagnosekode": Dx["code"], "diagnosetype": Dx["type"]})
    dx = dx.drop_duplicates()
    act = dx[dx["diagnosetype"] == "A"][["kontakt_id", "diagnosekode"]].assign(_a=1)
    dx = dx.merge(act, on=["kontakt_id", "diagnosekode"], how="left")
    dx = dx[~((dx["diagnosetype"] == "B") & (dx["_a"] == 1))].drop(columns="_a")
    dx["kilde"] = np.where(dx["kontakt_id"].str.len() == 16, "LPR2", "LPR3")
    dx = dx.sort_values(["kontakt_id", "diagnosetype", "diagnosekode"], kind="stable")
    td = pa.table({
        "kontakt_id": pa.array(dx["kontakt_id"].tolist(), pa.string()),
        "kilde": pa.array(dx["kilde"].tolist(), pa.string()),
        "diagnosekode": pa.array(dx["diagnosekode"].tolist(), pa.string()),
        "diagnosetype": pa.array(dx["diagnosetype"].tolist(), pa.string()),
    })
    pq.write_table(td, dpath, compression="zstd", row_group_size=250_000, use_dictionary=True)
    return t.num_rows, td.num_rows


# ------------------------------------------------------------------ civil registration and the matched extract

def write_civil(path, P, pnr):
    n = len(P["cohort"])
    big = 10 ** 7
    rows = []
    r = W.rng("records", "old_immigration")
    old = (r.random(n) < 0.06) & (P["entry"] == 0) & (P["ret"] >= big)
    old_day = r.integers(W.day(dt.date(1972, 1, 1)), W.day(dt.date(2016, 12, 31)), n)
    for i in range(n):
        death = iso(P["death"][i]) if P["death"][i] < big else ""
        emig = iso(P["emig"][i]) if P["emig"][i] < big else ""
        imm = ""
        if P["ret"][i] < big:
            imm = iso(P["ret"][i])
        elif P["entry"][i] > 0:
            imm = iso(P["entry"][i])
        elif old[i]:
            imm = iso(old_day[i])
        rows.append((pnr[i], int(P["birth_year"][i]), "K" if P["female"][i] else "M", death, emig, imm))
    rows.sort()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["pnr", "foedselsaar", "koen", "doedsdato", "udvandringsdato", "indvandringsdato"])
        w.writerows(rows)
    return len(rows)


def write_matched(path, P, pnr):
    users = np.where((P["user_of"] >= 0) & (P["index"] >= 0) & np.isin(P["user_of"], [0, 2, 4]))[0]
    comp = np.where(P["matched_to"] >= 0)[0]
    by_user = {}
    for c in comp:
        by_user.setdefault(int(P["matched_to"][c]), []).append(int(c))
    sub_of = {0: "tasorexant", 2: "corinurad", 4: "velaglutide"}
    sets = sorted(users.tolist(), key=lambda u: (int(P["index"][u]), pnr[u]))
    r = W.rng("records", "sets")
    rows = []
    for k, u in enumerate(sets):
        sid = 400000 + 3 * k + int(r.integers(0, 3))
        sub = sub_of[int(P["user_of"][u])]
        d = iso(P["index"][u])
        rows.append((sid, sub, "bruger", pnr[u], d, int(P["birth_year"][u]), "K" if P["female"][u] else "M"))
        for c in sorted(by_user.get(u, []), key=lambda c: pnr[c]):
            rows.append((sid, sub, "sammenligning", pnr[c], d, int(P["birth_year"][c]), "K" if P["female"][c] else "M"))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["saet_id", "substans", "rolle", "pnr", "indeksdato", "foedselsaar", "koen"])
        w.writerows(rows)
    return len(rows)


# ------------------------------------------------------------------ the ATC/DDD index

def write_atc(path):
    rows = []
    for s, d in W.SUBSTANCES.items():
        for code, fra, til in d["codes"]:
            note = ""
            if code == "M04AX02":
                note = "Midlertidig kode; afløst af M04AB06 fra 2024-01-01"
            if code == "M04AB06":
                note = "Erstatter M04AX02"
            rows.append((code, s, fra.isoformat() if fra else "", til.isoformat() if til else "",
                         ("%g" % d["ddd"]).replace(".", ","), d["ddd_unit"], d["route"], note))
    for s, (code, ddd) in W.NSAIDS.items():
        rows.append((code, s, "", "", ("%g" % ddd).replace(".", ","), "mg", "O", ""))
    rows.sort()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";", lineterminator="\n")
        w.writerow(["atc", "substans", "gyldig_fra", "gyldig_til", "ddd", "enhed", "adm_vej", "bemaerkning"])
        w.writerows(rows)
    return len(rows)


# ------------------------------------------------------------------ population and national admissions

BANDS = [(20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69),
         (70, 74), (75, 79), (80, 84), (85, 89), (90, 94), (95, 104)]
POP_2022 = {  # thousands, men and women, 1 January 2022
    (20, 24): (189.3, 181.6), (25, 29): (212.8, 203.5), (30, 34): (191.4, 184.9), (35, 39): (171.2, 168.8),
    (40, 44): (176.5, 175.2), (45, 49): (196.1, 193.7), (50, 54): (205.8, 202.6), (55, 59): (199.4, 198.2),
    (60, 64): (174.6, 176.9), (65, 69): (159.7, 167.3), (70, 74): (151.2, 163.8), (75, 79): (114.9, 134.6),
    (80, 84): (64.8, 84.7), (85, 89): (29.6, 47.9), (90, 94): (9.8, 21.6), (95, 104): (1.7, 5.9)}


def national_rate(event, age, female):
    m = 1.0
    for c, f in W.EVENT_MULT[event].items():
        p0, slope, ffac, _, _ = W.CONDITIONS[c]
        p = min(0.9, p0 * np.exp(slope * (age - 70.0)) * (ffac if female else 1.0))
        m *= 1 + p * (f - 1)
    return float(W.base_rate(event, age, female)) * m


def write_population(path):
    r = W.rng("records", "population")
    rows = []
    for y in (2022, 2023, 2024, 2025):
        for (a, b) in BANDS:
            for sex, female in (("M", False), ("K", True)):
                base = POP_2022[(a, b)][1 if female else 0] * 1000
                drift = 1 + (y - 2022) * (0.012 if a >= 70 else (-0.004 if a < 60 else 0.003))
                pop = int(round(base * drift * r.uniform(0.997, 1.003)))
                mid = (a + min(b, 99)) / 2.0 + 0.5
                # a fall counts only when its emergency contact carries a fall code (about 95 per cent do)
                share = {"fall": 0.95, "aki": 1.0, "pancreatitis": 1.0}
                counts = [int(r.poisson(pop * national_rate(e, mid, female) * share[e]))
                          for e in ("fall", "aki", "pancreatitis")]
                label = "%d-%d" % (a, b) if b < 100 else "%d+" % a
                rows.append((y, label, sex, pop) + tuple(counts))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["aar", "aldersgruppe", "koen", "folketal_1_januar", "indlaeggelser_fald",
                    "indlaeggelser_akut_nyreskade", "indlaeggelser_akut_pancreatitis"])
        w.writerows(rows)
    return len(rows)
