"""Write the evidence pack (target/) from the truth in world.py. Each file is written the way its source system
writes it; nothing here describes the data."""
import csv
import datetime as dt
import os
import re
import zipfile

import params as P
import world as W

D = dt.date
TD = dt.timedelta
FIXED_ZIP_TIME = (2026, 10, 16, 8, 30, 0)


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
def amr(path, w):
    rows = sorted(w["amr_rows"], key=lambda r: (r[1], r[0]))
    out = []
    for r in rows:
        ser, d, de, dv, ts, tr, re_, rv, st = r
        out.append([ser, d.isoformat(), de, None if dv is None else "%.2f" % dv,
                    None if ts is None else "%.1f" % ts, None if tr is None else "%.1f" % tr,
                    re_, "%.2f" % rv, st])
    write_csv(path, ["meternummer", "datum_utc", "energie_kwh", "volume_m3", "t_aanvoer_gem_c", "t_retour_gem_c",
                     "telwerk_energie_kwh", "telwerk_volume_m3", "status"], out)
    return len(out)


def register(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Aansluitingen"
    head = ["aansluitnummer", "object", "adres", "postcode", "plaats", "wijk", "categorie", "bouwjaar",
            "gecontracteerd_vermogen_kw", "aansluitdatum", "net", "status"]
    ws.append(head)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    conns = sorted(w["conns"], key=lambda c: c["nr"])
    for c in conns:
        st = c["adres"].rsplit(" ", 1)[0]
        ws.append([c["nr"], c["object"], c["adres"], postcode(st), P.CITY, c["wijk"], c["cat"], c["bouwjaar"],
                   c["kw"], c["aansluitdatum"], P.NETWORK, "in bedrijf"])
    for r in ws.iter_rows(min_row=2, min_col=10, max_col=10):
        r[0].number_format = "dd-mm-yyyy"
    ws2 = wb.create_sheet("Meters")
    ws2.append(["aansluitnummer", "meternummer", "metertype", "geplaatst", "verwijderd", "stand_bij_plaatsing_kwh",
                "stand_bij_verwijdering_kwh", "uitlezing"])
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    mrows = []
    for c in conns:
        if c["gen"] == "A":
            mrows.append([c["nr"], c["serial_legacy"], "MC 602 qp %s" % _qp(c), c["aansluitdatum"], c["migration"],
                          None, int(round(c["leg_end_kwh"])), "drive-by"])
            end26 = c.get("exchange26")
            mrows.append([c["nr"], c["serial_amr"], "MC 603 qp %s (revisie)" % _qp(c), c["migration"],
                          end26[0] if end26 else None, int(c["amr_begin_kwh"]),
                          c.get("exchange26_old_end") if end26 else None, "AMR"])
        else:
            end26 = c.get("exchange26")
            mrows.append([c["nr"], c["serial_legacy"], "MC 603 qp %s" % _qp(c), c["aansluitdatum"],
                          end26[0] if end26 else None, None, c.get("exchange26_old_end") if end26 else None,
                          "AMR (module %s)" % c["migration"].strftime("%d-%m-%Y")])
        if c.get("exchange26"):
            xd, nser, nbeg, f = c["exchange26"]
            mrows.append([c["nr"], nser, "MC 603 qp %s" % _qp(c), xd, None, c["exchange26_new_begin"], None, "AMR"])
    for r in mrows:
        ws2.append(r)
    for r in ws2.iter_rows(min_row=2, min_col=4, max_col=5):
        for cell in r:
            cell.number_format = "dd-mm-yyyy"
    for sh, widths in ((ws, [14, 36, 26, 10, 10, 14, 11, 9, 14, 13, 15, 11]), (ws2, [14, 12, 24, 12, 12, 16, 18, 22])):
        for i, wdt in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, "%s Netbeheer" % P.HEATCO_SHORT, "Aansluitregister Warmtenet West", dt.datetime(2026, 10, 1, 7, 40))
    wb.save(path)
    normalise_zip(path, "2026-10-01T07:40:00Z")
    return len(conns), len(mrows)


def _qp(c):
    q = c["kw"] / (1.163 * 40)
    for v in (1.5, 2.5, 3.5, 6, 10, 15, 25):
        if q <= v * 0.9:
            return ("%g" % v).replace(".", ",")
    return "40"


def weather(path, w):
    wx = w["wx"]
    rows = [["LKS", d.strftime("%Y%m%d"), int(tg), int(tn), int(tx)] for d, tg, tn, tx in
            zip(wx["days"], wx["tg"], wx["tn"], wx["tx"])]
    write_csv(path, ["station", "YYYYMMDD", "TG", "TN", "TX"], rows)
    return len(rows)


def scada(path, w):
    rows = [[t.strftime("%Y-%m-%d %H:%M"), "%.1f" % f, "%.1f" % ts, "%.1f" % tr, "%.3f" % q, "%.1f" % p1, "%.1f" % p2]
            for t, f, ts, tr, q, p1, p2 in w["scada"]]
    write_csv(path, ["tijdstip_utc", "debiet_m3h", "t_aanvoer_c", "t_retour_c", "warmte_mwh", "pomp_1_kw", "pomp_2_kw"],
              rows, delim=";")
    return len(rows)


def schedule(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Fasering"
    ws.append(["Aardgasvrij Weidehaven 2027-2028", None, None, None, None, None, None, None, None, None, None, None])
    ws.append(["Stand 30-09-2026", None, None, None, None, None, None, None, None, None, None, None])
    ws.append([])
    head = ["complexnr", "complex", "adressen", "postcode", "bouwjaar", "type", "woningen", "energielabel",
            "ketelhuis", "gas_ean", "fase", "aansluiten_gepland"]
    ws.append(head)
    for cell in ws[4]:
        cell.font = Font(bold=True)
    ws["A1"].font = Font(bold=True, size=12)
    for b in w["blocks"]:
        par = "even" if b["from"] % 2 == 0 else "oneven"
        ws.append([int(b["code"]), "%s %d-%d" % (b["street"], b["from"], b["to"]),
                   "%s %d t/m %d (%s)" % (b["street"], b["from"], b["to"], par), postcode(b["street"]), b["bouwjaar"],
                   b["type"], b["dwellings"], b["label"], "KH-%s" % b["code"][-3:], b["ean_current"], b["phase"],
                   b["date"]])
    for r in ws.iter_rows(min_row=5, min_col=12, max_col=12):
        r[0].number_format = "dd-mm-yyyy"
    for r in ws.iter_rows(min_row=5, min_col=10, max_col=10):
        r[0].number_format = "@"
    for i, wdt in enumerate([10, 24, 34, 10, 9, 12, 9, 12, 10, 21, 6, 18]):
        ws.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, P.PEOPLE["corp"], "Fasering aardgasvrij", dt.datetime(2026, 9, 30, 15, 5))
    wb.save(path)
    normalise_zip(path, "2026-09-30T13:05:00Z")
    return len(w["blocks"])


def revised(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultaten"
    ws.append(["Warmteverliesberekening NEN-EN 12831, Weidehaven aardgasvrij 2027-2028"])
    ws.append(["Revisie 2, 18-09-2026. Ontwerpbuitentemperatuur -10 C. Afgifte: bestaande tweepijps radiatoren, "
               "ontwerp 90/70 C. %s, %s" % (P.CONSULT, P.PEOPLE["consult"])])
    ws.append([])
    ws.append(["object", "complex", "woningen", "bouwlagen", "gbo_m2", "nachtverlaging_K", "transmissie_kw",
               "ventilatie_kw", "opwarmtoeslag_kw", "ontwerpwarmteverlies_kw"])
    for cell in ws[4]:
        cell.font = Font(bold=True)
    ws["A1"].font = Font(bold=True, size=12)
    order = sorted(w["blocks"], key=lambda b: (b["street"], b["from"]))
    for b in order:
        tr, ve, op = b["split"]
        ws.append(["%s %d-%d" % (b["street"], b["from"], b["to"]), "WH%s" % b["code"], b["dwellings"], b["storeys"],
                   b["gfa"], b["setback_K"], tr, ve, op, b["load"]])
    for i, wdt in enumerate([24, 9, 9, 10, 9, 16, 14, 13, 16, 22]):
        ws.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, P.PEOPLE["consult"], "Warmteverliesberekening rev2", dt.datetime(2026, 9, 18, 11, 20))
    wb.save(path)
    normalise_zip(path, "2026-09-18T09:20:00Z")
    return len(order)


def gasreads(path, w):
    rows = []
    for ean, ser, t_loc, reg, kind in w["gas_reads"]:
        u, off = utc_from_local(t_loc.year, t_loc.month, t_loc.day, t_loc.hour, t_loc.minute)
        stamp = t_loc.strftime("%Y-%m-%dT%H:%M:00") + ("+02:00" if off == 2 else "+01:00")
        rows.append([ean, ser, stamp, int(reg), kind])
    # the telemetry platform resent one month's batch for one meter
    dup = [r for r in rows if r[2].startswith("2026-04-01")][3]
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
    for cell in ws[1]:
        cell.font = Font(bold=True)
    seen = {}
    for m in w["gas_master"]:
        b = m["block"]
        if m["ean"] in seen:
            continue
        seen[m["ean"]] = m
    rows = []
    for ean, m in seen.items():
        b = m["block"]
        segs = [x for x in w["gas_master"] if x["ean"] == ean]
        closed = [x for x in segs if x["reason"] == "capaciteitswijziging"]
        din = min(x["in"] for x in segs)
        if closed:
            dout, reason, status = closed[0]["out"], "capaciteitswijziging", "beeindigd"
        else:
            dout, reason, status = None, None, "actief"
        cap = segs[-1]["g"]
        rows.append([ean, "%s %d" % (b["street"], b["from"]), postcode(b["street"]), P.CITY,
                     "ketelhuis %s %d-%d" % (b["street"], b["from"], b["to"]), cap, status, din, dout, reason])
    rows.sort(key=lambda r: r[0])
    for r in rows:
        ws.append(r)
    ws2 = wb.create_sheet("Meters")
    ws2.append(["ean", "meternummer", "metertype", "geplaatst", "verwijderd", "beginstand_m3", "eindstand_m3",
                "reden"])
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    mr = []
    for m in w["gas_master"]:
        typ = {"G25": "G25 balgenmeter", "G40": "G40 balgenmeter", "G65": "G65 rotormeter"}[m["g"]]
        reason = {"capaciteitswijziging": "aansluiting heringedeeld", "meterwissel": "vervangingsprogramma 2025-2026",
                  "": None}[m["reason"]]
        mr.append([m["ean"], m["ser"], typ, m["in"], m["out"], None if m.get("begin") is None else int(m["begin"]),
                   m["end"], reason])
    mr.sort(key=lambda r: (r[0], r[3]))
    for r in mr:
        ws2.append(r)
    for sh, cols in ((ws, (8, 9)), (ws2, (4, 5))):
        for r in sh.iter_rows(min_row=2):
            for c in cols:
                r[c - 1].number_format = "dd-mm-yyyy"
    for r in ws.iter_rows(min_row=2, max_col=1):
        r[0].number_format = "@"
    for r in ws2.iter_rows(min_row=2, max_col=1):
        r[0].number_format = "@"
    for sh, widths in ((ws, [21, 22, 10, 10, 34, 10, 10, 12, 12, 22]), (ws2, [21, 13, 17, 12, 12, 13, 13, 30])):
        for i, wdt in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = wdt
    xlsx_props(wb, P.GRIDOP, "Meterstamgegevens", dt.datetime(2026, 10, 1, 6, 15))
    wb.save(path)
    normalise_zip(path, "2026-10-01T04:15:00Z")
    return len(rows), len(mr)


def build(target):
    import docs
    os.makedirs(target, exist_ok=True)
    for fn in os.listdir(target):
        os.remove(os.path.join(target, fn))
    w = W.build()
    F = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    n = {}
    n["amr"] = amr(F["amr"], w)
    n["register"] = register(F["register"], w)
    n["weather"] = weather(F["weather"], w)
    n["scada"] = scada(F["scada"], w)
    n["schedule"] = schedule(F["schedule"], w)
    n["revised"] = revised(F["revised"], w)
    n["gasreads"] = gasreads(F["gasreads"], w)
    n["gasmaster"] = gasmaster(F["gasmaster"], w)
    n["legacy"] = legacy(F["legacy"], w)
    docs.write_all(F, w)
    return w, n


def legacy(path, w):
    rows = []
    for ser, d, val, unit, kind, tm in w["legacy"]:
        rows.append([ser, d.strftime("%d-%m-%Y"), tm, ("%.3f" % val).replace(".", ","), unit, kind])
    write_csv(path, ["meternummer", "opnamedatum", "opnametijd", "stand", "eenheid", "soort"], rows, delim=";")
    return len(rows)
