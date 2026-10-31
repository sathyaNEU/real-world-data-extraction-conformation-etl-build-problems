"""Writers for the data files under target/, each in its source system's own layout: the cadastre and the population
register in semicolon CSV with day-first dates as the registers deliver them, the meter data hub's metering point
register and its hourly values (UTC hour starts, quality codes, a later delivery correcting estimated hours), the land
register's titles and its 2026 transfers, the business and shareholder registers, the weather service's hourly
temperatures and the grid company's outage log."""
import csv
import datetime as dt
import re

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import world as W

OUTSIDE = ["4601", "0301", "5001", "1103", "3301", "1508"]


def _d(x):
    return x.strftime("%d.%m.%Y") if x else ""


def _csv(path, header, rows, sep=";"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, delimiter=sep, lineterminator="\r\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def label(u, when):
    """A unit's number as the cadastre had it on a date: renumbered blocks carry the old number before the change."""
    if "unit_old" in u and when < u["renum_date"]:
        return u["unit_old"]
    return u["unit"]


def prepare(w):
    for uid, (old, new, d) in w.renumbered.items():
        w.by_id[uid]["renum_date"] = d


# ---------------------------------------------------------------------------------------------- cadastre
def write_cadastre(w, path):
    rows = []
    btype = {"Leilighet": "Boligblokk", "Enebolig": "Enebolig", "Rekkehus": "Rekkehus", "Tomannsbolig": "Tomannsbolig",
             "Fritidsbolig": "Fritidsbygg", "Institusjon": "Sykehjem"}
    for u in sorted(w.units, key=lambda x: (x["nr"], x["street"], x["no"], x["unit"], x["id"])):
        rows.append([u["nr"], u["id"], u["gnr"], u["bnr"], u["snr"] or "", u["street"], u["no"], u["letter"],
                     u["unit"], u["category"], btype[u["type"]], u["area"], _d(u["in_use"]), u["building"]])
    return _csv(path, ["kommunenr", "bruksenhet_id", "gardsnr", "bruksnr", "seksjonsnr", "adressenavn", "husnr",
                       "bokstav", "bruksenhetsnr", "bruksenhetstype", "bygningstype", "bruksareal_m2",
                       "tatt_i_bruk", "bygning_id"], rows)


def write_municipalities(path):
    rows = []
    for nr, name, *_r in W.MUNICIPALITIES:
        rows.append([nr, name, "01.01.2024" if nr in W.OLD_NUMBER else "01.01.2020", W.OLD_NUMBER.get(nr, ""),
                     "Delt fra %s 01.01.2024" % W.OLD_NUMBER[nr] if nr in W.OLD_NUMBER else ""])
    return _csv(path, ["kommunenr", "kommunenavn", "gyldig_fra", "tidligere_kommunenr", "merknad"], rows)


# ---------------------------------------------------------------------------------------------- metering points
def write_meterpoints(w, path, rng):
    rows = []
    for m in sorted(w.meters, key=lambda x: x["mp"]):
        if m["unit"] is None:
            nr = m["nr"]
            blocks = sorted({(u["street"], u["no"]) for u in w.units if u["nr"] == nr and u["type"] == "Leilighet"})
            s, n = blocks[int(rng.integers(0, len(blocks)))] if blocks else ("Storgata", 1)
            rows.append([m["mp"], "Hvitfjell Nett AS", W.OLD_NUMBER.get(nr, nr), "%s %d" % (s, n), "", "",
                         "Fellesmåling", _d(m["from"]), _d(m["to"])])
            continue
        u = w.by_id[m["unit"]]
        nr = W.OLD_NUMBER.get(u["nr"], u["nr"])
        adr = "%s %d%s" % (u["street"], u["no"], u["letter"])
        if rng.random() < 0.18:
            adr = adr.upper()
        unit = u["unit"]
        single = u["counted"] and len(w.props.get((u["nr"], u["gnr"], u["bnr"]), {}).get("units", [u])) == 1
        if single and u["type"] != "Leilighet":
            unit = "" if rng.random() < 0.7 else unit
        elif rng.random() < 0.12:
            unit = "%s %s" % (unit[0], unit[1:])
        uid = u["id"]
        if single and unit == "" and u["nr"] not in W.OLD_NUMBER and rng.random() < 0.08:
            uid = ""
        kind = {"Bolig": "Husholdning", "Fritidsbolig": "Fritidsbolig"}[u["category"]]
        rows.append([m["mp"], "Hvitfjell Nett AS", nr, adr, unit, uid, kind, _d(m["from"]), _d(m["to"])])
    return _csv(path, ["malepunkt_id", "nettselskap", "kommunenr", "adresse", "bruksenhetsnr", "bruksenhet_id",
                       "kundekategori", "gyldig_fra", "gyldig_til"], rows)


def write_hourly(w, path, rng):
    """One row per metering point and UTC hour it reported in the fortnight, as the hub delivered it: some hours
    missing after communication faults, some days first delivered as estimates and replaced by measured values in a
    later delivery, both deliveries kept."""
    t0 = dt.datetime(W.FORTNIGHT_START.year, W.FORTNIGHT_START.month, W.FORTNIGHT_START.day) - \
        dt.timedelta(hours=W.UTC_OFFSET)
    mps, ts, kwh, qual, ver = [], [], [], [], []
    w.estimated = {}
    w.missing = {}
    for m in sorted(w.meters, key=lambda x: x["mp"]):
        key = ("felles", m["mp"]) if m["unit"] is None else m["unit"]
        load = w.load[key]
        lo, hi = 0, W.HOURS
        if m["from"] and m["from"] > W.FORTNIGHT_START:
            lo = (m["from"] - W.FORTNIGHT_START).days * 24
        if m["to"] and m["to"] < W.FORTNIGHT_START + dt.timedelta(days=W.DAYS):
            hi = (m["to"] - W.FORTNIGHT_START).days * 24
        hours = np.arange(lo, hi)
        keep = np.ones(len(hours), bool)
        if rng.random() < 0.10:
            for _ in range(int(rng.integers(1, 3))):
                a = int(rng.integers(0, max(1, len(hours) - 6)))
                keep[a:a + int(rng.integers(1, 7))] = False
        est_day = int(rng.integers(0, W.DAYS)) if rng.random() < 0.03 else None
        w.missing[m["mp"]] = int((~keep).sum())
        for i, h in enumerate(hours):
            if not keep[i]:
                continue
            mps.append(m["mp"])
            ts.append(t0 + dt.timedelta(hours=int(h)))
            if est_day is not None and h // 24 == est_day:
                block = load[(h // 24) * 24:(h // 24) * 24 + 24]
                kwh.append(round(float(block.mean()), 3))
                qual.append("E")
                ver.append(1)
                mps.append(m["mp"])
                ts.append(t0 + dt.timedelta(hours=int(h)))
                kwh.append(float(load[h]))
                qual.append("M")
                ver.append(2)
            else:
                kwh.append(float(load[h]))
                qual.append("M")
                ver.append(1)
        if est_day is not None:
            w.estimated[m["mp"]] = est_day
    order = np.lexsort((np.array(ver), np.array(ts, dtype="datetime64[s]"), np.array(mps)))
    tab = pa.table({
        "malepunkt_id": pa.array(np.array(mps)[order], pa.int64()),
        "fra_tidspunkt_utc": pa.array(np.array(ts, dtype="datetime64[s]")[order], pa.timestamp("s", tz="UTC")),
        "forbruk_kwh": pa.array(np.array(kwh, dtype=np.float64)[order], pa.float64()),
        "kvalitet": pa.array(np.array(qual)[order], pa.string()),
        "leveranse": pa.array(np.array(ver)[order], pa.int8()),
    })
    pq.write_table(tab, path, compression="zstd", use_dictionary=True, write_statistics=False)
    with open(path, "rb") as fh:
        b = fh.read()
    b = re.sub(rb"parquet-cpp-arrow version \d{2}\.\d\.\d", b"parquet-cpp-arrow version 16.1.0", b)
    with open(path, "wb") as fh:
        fh.write(b)
    return tab.num_rows


# ---------------------------------------------------------------------------------------------- population register
def _addr(u, when):
    return [u["nr"], u["street"], u["no"], u["letter"], label(u, when)]


def write_register(w, path):
    rows = []
    for p in sorted(w.persons, key=lambda x: x["id"]):
        if p["unit"] is None:
            continue
        u = w.by_id[p["unit"]]
        rows.append([p["id"], _d(p["born"])] + _addr(u, W.SNAPSHOT_DAY) + [_d(p["since"])])
    return _csv(path, ["person_lopenr", "fodselsdato", "kommunenr", "adressenavn", "husnr", "bokstav",
                       "bruksenhetsnr", "bosatt_fra"], rows)


def write_events(w, path, rng):
    rows = []
    for e in w.events:
        frm = ["", "", "", "", ""]
        to = ["", "", "", "", ""]
        land_f = land_t = ""
        if e.get("renumber"):
            u = w.by_id[e["from"]]
            frm = [u["nr"], u["street"], u["no"], u["letter"], e["renumber"][0]]
            to = [u["nr"], u["street"], u["no"], u["letter"], e["renumber"][1]]
        else:
            if e["from"] is not None:
                frm = _addr(w.by_id[e["from"]], e["date"])
            if e["to"] is not None:
                to = _addr(w.by_id[e["to"]], e["date"] + dt.timedelta(days=1))
            if e.get("to_out") == "OUT":
                to = [OUTSIDE[int(rng.integers(0, len(OUTSIDE)))], "", "", "", ""]
            if e.get("to_out") == "ABROAD":
                land_t = ["SE", "PL", "DK", "ES", "LT", "DE"][int(rng.integers(0, 6))]
            if e.get("from_out") == "ABROAD":
                land_f = ["PL", "LT", "SE", "UA", "PH", "DE"][int(rng.integers(0, 6))]
        rows.append([e["pid"], _d(w.person_by_id[e["pid"]]["born"]), e["type"], _d(e["date"]), _d(e["reg"])] + frm +
                    [land_f] + to + [land_t])
    return _csv(path, ["person_lopenr", "fodselsdato", "hendelse", "hendelsesdato", "registrert_dato", "fra_kommunenr",
                       "fra_adressenavn", "fra_husnr", "fra_bokstav", "fra_bruksenhetsnr", "fra_land", "til_kommunenr",
                       "til_adressenavn", "til_husnr", "til_bokstav", "til_bruksenhetsnr", "til_land"], rows)


# ---------------------------------------------------------------------------------------------- land, business, shares
def _kind(holder):
    return "Person" if str(holder).startswith("P") else "Organisasjon"


def write_titles(w, path):
    rows = []
    for t in sorted(w.titles, key=lambda x: (x["nr"], x["gnr"], x["bnr"], x["snr"])):
        rows.append([t["nr"], t["gnr"], t["bnr"], t["snr"] or "", t["holder"], t["name"], _kind(t["holder"]), "1/1",
                     _d(t["reg"])])
    return _csv(path, ["kommunenr", "gardsnr", "bruksnr", "seksjonsnr", "hjemmelshaver_id", "hjemmelshaver_navn",
                       "hjemmelshaver_type", "andel", "tinglyst_dato"], rows)


def write_transfers(w, path):
    rows = []
    for t in w.transfers:
        rows.append([t["nr"], t["gnr"], t["bnr"], t["snr"] or "", "Skjøte", t["from"], t["from_name"], t["to"],
                     t["to_name"], _d(t["doc"]), _d(t["reg"])])
    return _csv(path, ["kommunenr", "gardsnr", "bruksnr", "seksjonsnr", "dokumenttype", "avgiver_id", "avgiver_navn",
                       "erverver_id", "erverver_navn", "dokumentdato", "tinglyst_dato"], rows)


def write_entities(w, path):
    rows = []
    for o in sorted(w.orgs, key=lambda x: x["orgnr"]):
        rows.append([o["orgnr"], o["name"], o["form"], o["parent"] or "", o["nr"]])
    return _csv(path, ["organisasjonsnummer", "navn", "organisasjonsform", "overordnet_enhet",
                       "forretningsadresse_kommunenr"], rows)


def write_shareholders(w, path):
    names = {o["orgnr"]: o["name"] for o in w.orgs}
    rows = []
    for s in sorted(w.shareholders, key=lambda x: (x["company"], str(x["holder"]))):
        rows.append([s["company"], names.get(s["company"], ""), "Ordinære aksjer", s["holder"],
                     names.get(s["holder"], ""), s["n"], s["total"]])
    return _csv(path, ["orgnr_selskap", "selskap", "aksjeklasse", "aksjonaer_id", "aksjonaer_navn", "antall_aksjer",
                       "antall_aksjer_selskap"], rows)


# ---------------------------------------------------------------------------------------------- the two distractors
def write_prices(w, path):
    rows = []
    t0 = dt.datetime(W.FORTNIGHT_START.year, W.FORTNIGHT_START.month, W.FORTNIGHT_START.day)
    for h in range(W.HOURS):
        t = t0 + dt.timedelta(hours=h)
        rows.append([t.strftime("%d.%m.%Y"), "%02d-%02d" % (t.hour, (t.hour + 1) % 24),
                     ("%.2f" % w.prices[h]).replace(".", ",")])
    return _csv(path, ["dato", "time", "no1_ore_per_kwh"], rows)


def write_outages(w, path):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Avbrudd november 2026"
    ws.append(["Kommunenr", "Dato", "Fra kl.", "Til kl.", "Berørte sluttkunder", "Årsak"])
    names = {m[0]: m[1] for m in W.MUNICIPALITIES}
    for o in w.outages:
        d = W.FORTNIGHT_START + dt.timedelta(days=o["day"])
        ws.append([o["nr"], d.strftime("%d.%m.%Y"), "%02d:00" % o["h0"], "%02d:00" % (o["h0"] + o["dur"]),
                   o["customers"], "Feil på høyspentlinje, %s" % names[o["nr"]]])
    for col, wd in zip("ABCDEF", (11, 12, 9, 9, 20, 40)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    return len(w.outages)
