"""Write the evidence pack (target/) of architecture 3 from the truth in world.py. Each file is written the way its source system
writes it; nothing here describes the data."""
import csv
import datetime as dt
import os
import re
import zipfile

import numpy as np

import params as P
import world as W

D = dt.date
TD = dt.timedelta
FIXED_ZIP_TIME = (2026, 10, 19, 8, 30, 0)


# ------------------------------------------------------------------------------------------------- helpers
def write_csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=delim, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(["" if v is None else v for v in r])


def normalise_zip(path, when="2026-10-01T07:40:00Z", app="Microsoft Excel"):
    """Rewrite an OOXML container with fixed member times and order and the document dates set to the export's own
    date, so two builds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + when.encode() + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + when.encode() + rb"\g<2>",
                          data)
        fixed.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in fixed:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def xlsx_props(wb, creator, title, when):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = title


def postcode(street):
    h = sum(ord(ch) * (i + 7) for i, ch in enumerate(street))
    num = 2981 + h % 17
    letters = "ABCDEGHJKLMNPRSTVWXZ"
    return "%d %s%s" % (num, letters[h % 20], letters[(h // 20) % 20])


def nl_local(t_utc):
    return t_utc + TD(hours=W.nl_offset_hours(t_utc))


def utc_from_local(y, m, d, hh, mm=0):
    """UTC datetime for a Dutch local wall time (no ambiguous hours are used)."""
    loc = dt.datetime(y, m, d, hh, mm)
    for off in (2, 1):
        u = loc - TD(hours=off)
        if W.nl_offset_hours(u) == off:
            return u, off
    raise ValueError(loc)




# ------------------------------------------------------------------------------------------------- the files
def entry_day(p):
    d = D(p["birth"].year + 4, p["birth"].month, min(p["birth"].day, 28))
    while d.weekday() >= 5:
        d += TD(days=1)
    return d


def brp(path, w):
    rows = []
    for p in w["persons"]:
        hh = p["hh"]
        start = max(hh["since"], p["birth"])
        rows.append([p["pid"], hh["hid"], p["birth"].strftime("%d-%m-%Y"), p["sex"], hh["street"], hh["nr"], hh["add"],
                     hh["postcode"], hh["wijk"], start.strftime("%d-%m-%Y"),
                     hh["leave"].strftime("%d-%m-%Y") if hh["leave"] else ""])
    rows.sort(key=lambda r: (r[7], r[4], r[5], r[6], r[0]))
    write_csv(path, ["persoonsnummer", "huishoudnummer", "geboortedatum", "geslacht", "straatnaam", "huisnummer",
                     "huisletter", "postcode", "wijk", "datum_adres", "datum_vertrek"], rows, delim=";")
    return len(rows)


def pupil_numbers(rng, kids):
    old, new = {}, {}
    a = rng.choice(np.arange(1000, 9999), size=len(kids), replace=False)
    b = rng.choice(np.arange(10000, 99999), size=len(kids), replace=False)
    for i, p in enumerate(kids):
        old[p["pid"]] = "%04d" % int(a[i])
        new[p["pid"]] = "KW%05d" % int(b[i])
    return old, new


def roll(path, w):
    rng = np.random.default_rng(P.SEED + 400)
    kids = [p for p in w["kids"] if p.get("enrolled")]
    old, new = pupil_numbers(rng, kids)
    rows = []
    for Y in P.COUNT_YEARS:
        for p in W.roll(w["kids"], Y):
            hh = p["hh"]
            add = hh["add"]
            if add:
                add = add.lower() if rng.random() < 0.5 else ("-" + add if add.isdigit() else add)
            num = old[p["pid"]] if Y <= 2022 else new[p["pid"]]
            rows.append(["01-10-%d" % Y, num, p["birth"].isoformat(), hh["postcode"].replace(" ", ""), hh["nr"], add,
                         Y - p["entry_count"] + 1, entry_day(p).isoformat()])
    rows.sort(key=lambda r: (r[0][-4:], r[6], r[1]))
    write_csv(path, ["teldatum", "leerlingnummer", "geboortedatum", "postcode", "huisnummer", "toevoeging", "groep",
                     "datum_inschrijving"], rows, delim=";")
    return len(rows)


def schools(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Scholen"
    ws.append(["brin", "school", "bestuur", "denominatie", "adres", "wijk", "leerlingen_1okt2026", "groepen"])
    for c in ws[1]:
        c.font = Font(bold=True)
    n26 = len(W.roll(w["kids"], 2026))
    ws.append(["21KW", P.SCHOOL, P.BOARD, "openbaar", "Molenwiek 2", "Molenwijk", n26, 18])
    for brin, nm, bestuur, den, adr, wijk, n, g in (
            ("17AK", "OBS De Akker", P.BOARD, "openbaar", "Tarweveld 40", "De Akkers", 287, 12),
            ("09NP", "CBS Het Noorderlicht", "Stichting Christelijk Onderwijs Veenstreek", "protestants-christelijk",
             "Noorderhof 3", "Noorderpark", 331, 14),
            ("14MS", "RKBS Sint Maarten", "Stichting Katholiek Onderwijs Veenstreek", "rooms-katholiek",
             "Korenmolen 61", "Molenwijk", 218, 9),
            ("30DB", "Montessorischool De Boomgaard", "Vereniging Montessorionderwijs Veenhaven", "algemeen bijzonder",
             "Beukenlaan 118", "Noorderpark", 196, 8)):
        ws.append([brin, nm, bestuur, den, adr, wijk, n, g])
    for i, wdt in enumerate([7, 30, 40, 22, 16, 13, 18, 8]):
        ws.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, "Gemeente Veenhaven, afdeling Onderwijs", "Scholenoverzicht Veenhaven-Noord", dt.datetime(2026, 10, 12, 9, 5))
    wb.save(path)
    normalise_zip(path, "2026-10-12T07:05:00Z")


def gasreads(path, w):
    rows = []
    for ean, ser, t_loc, reg, kind in w["gas_reads"]:
        u, off = utc_from_local(t_loc.year, t_loc.month, t_loc.day, t_loc.hour, t_loc.minute)
        rows.append([ean, ser, t_loc.strftime("%Y-%m-%dT%H:%M:00") + ("+02:00" if off == 2 else "+01:00"), int(reg), kind])
    dup = [r for r in rows if r[2].startswith("2025-02-01")][0]
    rows.append(list(dup))
    rows.sort(key=lambda r: (r[2][:10], r[0], r[4] != "E"))
    write_csv(path, ["ean", "meternummer", "tijdstip", "meterstand_m3", "soort"], rows, delim=";")
    return len(rows)


def gasmaster(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Aansluitingen"
    ws.append(["ean", "adres", "postcode", "plaats", "omschrijving", "capaciteit", "status", "datum_in", "datum_uit",
               "reden_uit"])
    for c in ws[1]:
        c.font = Font(bold=True)
    desc = {"main": ("Molenwiek 2", "Basisschool De Kwikstaart, hoofdgebouw"),
            "annex": ("Molenwiek 4", "Basisschool De Kwikstaart, dependance")}
    eans = {}
    for m in w["gas_master"]:
        eans.setdefault(m["ean"], []).append(m)
    for ean in sorted(eans):
        segs = eans[ean]
        b = segs[0]["bld"]
        closed = [x for x in segs if x["reason"] == "reissue"]
        ws.append([ean, desc[b][0], "3841 KW", P.CITY, desc[b][1], segs[-1]["g"], "beeindigd" if closed else "actief",
                   min(x["from"] for x in segs), closed[0]["out"] if closed else None,
                   "capaciteitswijziging" if closed else None])
    ws2 = wb.create_sheet("Meters")
    ws2.append(["ean", "meternummer", "metertype", "geplaatst", "verwijderd", "beginstand_m3", "eindstand_m3", "reden"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for m in sorted(w["gas_master"], key=lambda m: (m["ean"], m["from"])):
        reason = {"reissue": "aansluiting heringedeeld", "exchange": "vervangingsprogramma", "": None}[m["reason"]]
        ws2.append([m["ean"], m["ser"], "%s balgenmeter" % m["g"], m["from"], m["out"],
                    None if m.get("begin") is None else int(m["begin"]), m["end"], reason])
    for sh, cols in ((ws, (8, 9)), (ws2, (4, 5))):
        for r in sh.iter_rows(min_row=2):
            for cc in cols:
                r[cc - 1].number_format = "dd-mm-yyyy"
            r[0].number_format = "@"
    for sh, widths in ((ws, [21, 14, 10, 10, 40, 10, 10, 12, 12, 22]), (ws2, [21, 13, 17, 12, 12, 13, 13, 26])):
        for i, wdt in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, P.GRIDOP, "Meterstamgegevens", dt.datetime(2026, 10, 1, 6, 15))
    wb.save(path)
    normalise_zip(path, "2026-10-01T04:15:00Z")


def bso_att(path, w):
    rows = [[d.strftime("%d-%m-%Y"), loc, fam, n, st] for d, loc, fam, n, st in w["bso_rows"]]
    write_csv(path, ["datum", "locatiecode", "gezinsnummer", "aantal_kinderen", "status"], rows, delim=";")
    return len(rows)


def bso_loc(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Locaties"
    ws.append(["locatiecode", "naam", "adres", "actief_vanaf", "actief_tot", "opmerking"])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.append(["BSO-KWS", "BSO De Kwikstaart", "Molenwiek 4", D(2016, 8, 22), D(2026, 10, 11), None])
    ws.append(["BSO-MLW", "BSO Molenwijk", "Korenmolen 59", D(2012, 1, 9), D(2026, 10, 11), None])
    ws.append(["BSO-MLW2", "BSO Molenwijk-Kwikstaart", "Molenwiek 4", D(2026, 10, 12), None,
               "samenvoeging BSO-KWS en BSO-MLW"])
    ws.append(["BSO-NP", "BSO Noorderpark", "Parkweg 12", D(2018, 8, 20), None, None])
    ws2 = wb.create_sheet("Contracten")
    ws2.append(["gezinsnummer", "kindnummer", "school", "groep", "contract_vanaf", "dagen_per_week"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    rng = np.random.default_rng(P.SEED + 3100)
    for p in w["bso_users"]:
        ws2.append([p["hh"]["hid"], "K" + p["pid"][-6:], "De Kwikstaart", 2026 - p["entry_count"] + 1,
                    D(int(rng.integers(2019, 2026)), int(rng.integers(1, 13)), 1), int(rng.integers(1, 6))])
    for i, p in enumerate(w["bso_others"]):
        ws2.append([p["hh"]["hid"], "K9%05d" % i, str(rng.choice(["RKBS Sint Maarten", "OBS De Akker"])),
                    int(rng.integers(1, 9)), D(int(rng.integers(2020, 2026)), int(rng.integers(1, 13)), 1),
                    int(rng.integers(1, 6))])
    for sh in (ws, ws2):
        for r in sh.iter_rows(min_row=2):
            for c in r:
                if isinstance(c.value, D):
                    c.number_format = "dd-mm-yyyy"
    for sh, widths in ((ws, [12, 28, 16, 14, 12, 32]), (ws2, [14, 12, 22, 7, 15, 15])):
        for i, wdt in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, P.PEOPLE["provider"], "Locaties en contracten", dt.datetime(2026, 11, 2, 8, 0))
    wb.save(path)
    normalise_zip(path, "2026-10-19T07:00:00Z")


def build(target):
    import docs
    os.makedirs(target, exist_ok=True)
    for fn in os.listdir(target):
        os.remove(os.path.join(target, fn))
    w = W.build()
    F = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    n = {"brp": brp(F["brp"], w), "roll": roll(F["roll"], w), "gasreads": gasreads(F["gasreads"], w),
         "bso_att": bso_att(F["bso_att"], w)}
    schools(F["schools"], w)
    gasmaster(F["gasmaster"], w)
    bso_loc(F["bso_loc"], w)
    docs.write_all(F, w)
    return w, n
