"""Write the data files of the task453 pack from the simulated world (sim.py). Each file is cut the way its producing
system exports it: the Vital Statistics Agency's permit extract, the Fund's member register, the City of Halbrook's
and Shoreline Memorial Group's receivables, the independent crematoria's fee returns, the cremator controllers'
cycle export, the abatement plants' logs and the agency's deaths table. The PDFs are written by docs.py."""
import csv
import datetime as dt
import math
from zoneinfo import ZoneInfo

import numpy as np

import sim
import world as W

FILES = W.FILES
ET = ZoneInfo(W.TZ_NAME)
UTC = dt.timezone.utc
HST = 0.13

REGIONS = ["Halbrook Region", "Larchmere Region", "South Shore", "Orrinsford Valley", "Lakeland", "Northern", "Wexley Valley"]
REGION_OF = {"CM-0417": 0, "CM-0738": 0, "CM-0283": 0, "CM-0659": 1, "CM-1347": 1, "CM-1182": 2, "CM-2034": 2,
             "CM-1768": 2, "CM-2409": 2, "CM-0372": 3, "CM-2163": 3, "CM-0896": 4, "CM-0514": 4, "CM-2087": 4,
             "CM-1925": 5, "CM-1471": 5, "CM-1633": 5, "CM-1590": 6, "CM-2251": 6, "CM-0941": 6}
MUNICIPALITY = {"CM-0417": "Halbrook", "CM-1182": "Fenwick Harbour", "CM-0659": "Larchmere", "CM-2034": "Stannard Bay",
                "CM-0738": "Halbrook", "CM-1590": "Wexley", "CM-2251": "Hollinsbrook", "CM-0896": "Corbett Narrows",
                "CM-1347": "Ashgrove", "CM-0372": "Tallis Creek", "CM-1925": "Dunmore Falls", "CM-2163": "Bellhaven",
                "CM-0514": "Kestrel Lake", "CM-1768": "Port Alder", "CM-2409": "Sorrel Bay", "CM-0283": "Wynford",
                "CM-1471": "Brackenridge", "CM-2087": "Ravensmoor", "CM-0941": "Elderton", "CM-1633": "Glenmora"}
OPENED = {"CM-0417": "1974-06-03", "CM-1182": "1988-09-12", "CM-0659": "1969-04-21", "CM-2034": "1996-02-05",
          "CM-0738": "2002-10-14", "CM-1590": "1991-05-27", "CM-2251": "2009-03-16", "CM-0896": "1983-07-11",
          "CM-1347": "1999-11-29", "CM-0372": "1978-08-08", "CM-1925": "2004-06-21", "CM-2163": "1993-01-18",
          "CM-0514": "2011-05-02", "CM-1768": "1985-03-25", "CM-2409": "2007-09-17", "CM-0283": "1979-11-05",
          "CM-1471": "2014-02-24", "CM-2087": "2001-06-11", "CM-0941": "1972-10-02", "CM-1633": "2016-08-29"}
SUPPLIER = {"CM-0417": "Ferrovent Systems", "CM-1182": "Halcyon Filtration", "CM-0659": "Ferrovent Systems",
            "CM-2034": "Halcyon Filtration", "CM-0738": "Ferrovent Systems", "CM-1590": "Brightwater Thermal",
            "CM-2251": "Halcyon Filtration"}


def _rng(tag):
    return np.random.default_rng([W.SEED, 77, sum(ord(c) * (i + 1) for i, c in enumerate(tag))])


def facility_no(ci, d):
    c = W.CREMATORIA[ci]
    if c[0] == "CM-1590" and d < W.WEXLEY_RENUMBERED:
        return W.WEXLEY_OLD_FACILITY
    return c[1]


# ---------------------------------------------------------------- permits
def permits(rows):
    """One record per cremation permit returned to the agency in the window. Permits are numbered in the order the
    agency issued them, on registering the death; a crematorium returns the permit once the cremation is done."""
    rng = _rng("permits")
    recs = []
    for k, r in enumerate(rows):
        reg = r["death"] + dt.timedelta(int(rng.integers(1, 6)))
        ret = r["cremation"] + dt.timedelta(int(rng.integers(1, 13)))
        home = REGION_OF[r["code"]]
        u = rng.random()
        region = REGIONS[home] if u < 0.86 else ("Out of province" if u > 0.988 else REGIONS[int(rng.integers(0, 7))])
        a = r["age"]
        pl = rng.random()
        if a >= 80:
            place = "Long-term care home" if pl < 0.38 else ("Hospital" if pl < 0.80 else ("Private residence" if pl < 0.97 else "Other"))
        elif a >= 18:
            place = "Hospital" if pl < 0.55 else ("Private residence" if pl < 0.82 else ("Long-term care home" if pl < 0.93 else "Other"))
        else:
            place = "Hospital" if pl < 0.82 else ("Private residence" if pl < 0.95 else "Other")
        if a == 0:
            age, unit = int(rng.integers(1, 12)), "M"
        else:
            age, unit = a, "Y"
        recs.append({"k": k, "reg": reg, "ret": ret, "region": region, "place": place, "age": age, "unit": unit,
                     "u": float(rng.random())})
    order = sorted(range(len(recs)), key=lambda i: (recs[i]["reg"], recs[i]["u"]))
    seq, regseq = {}, {}
    for i in order:
        y = recs[i]["reg"].year
        seq[y] = seq.get(y, 0) + 1 + int(rng.random() < 0.02)        # a permit spoiled and reissued now and then
        regseq[y] = regseq.get(y, 0) + int(rng.integers(1, 4))      # every death registered is numbered, not only these
        recs[i]["permit_no"] = "%02d-%06d" % (y % 100, seq[y] + 1180 * (y == 2025) + 38 * (y == 2027))
        recs[i]["reg_no"] = "%d-%07d" % (y, regseq[y] + 41000 * (y == 2025) + 2900 * (y == 2027))
    keep = [i for i in order if sim.D0 <= recs[i]["ret"] and dt.date(2025, 12, 1) <= recs[i]["ret"] <= dt.date(2027, 1, 31)]
    out = []
    for i in keep:
        p, r = recs[i], rows[recs[i]["k"]]
        out.append({"permit_no": p["permit_no"], "death_registration_no": p["reg_no"],
                    "date_of_death": r["death"].isoformat(), "sex": r["sex"], "age": p["age"], "age_unit": p["unit"],
                    "residence_region": p["region"], "place_of_death": p["place"],
                    "crematorium_facility_no": facility_no(r["ci"], r["cremation"]),
                    "date_of_cremation": r["cremation"].isoformat(), "permit_returned_on": p["ret"].isoformat(),
                    "_k": p["k"]})
    return out


def write_permits(prows, path):
    cols = ["permit_no", "death_registration_no", "date_of_death", "sex", "age", "age_unit", "residence_region",
            "place_of_death", "crematorium_facility_no", "date_of_cremation", "permit_returned_on"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for p in prows:
            w.writerow([p[c] for c in cols])
    return len(prows)


# ---------------------------------------------------------------- register
def write_register(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Members"
    ws["A1"] = "Crematoria Mercury Fund: member crematoria"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Register checked 2027-01-15"
    hdr = ["fund_code", "crematorium", "operator", "municipality", "opened", "cremators", "abatement_plant",
           "abatement_commissioned", "plant_supplier"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    for c in sorted(W.CREMATORIA, key=lambda x: x[0]):
        code = c[0]
        plant = "AP1 (cremators 1 to %d)" % c[4] if c[4] > 1 else ("AP1 (cremator 1)" if c[8] != "U" else "None")
        if c[8] == "U":
            plant = "None"
        ws.append([code, c[2], c[3], MUNICIPALITY[code], dt.date.fromisoformat(OPENED[code]), c[4], plant,
                   dt.date.fromisoformat(c[9]) if c[9] else None, SUPPLIER.get(code)])
    for row in ws.iter_rows(min_row=5):
        for cell in row:
            if isinstance(cell.value, dt.date):
                cell.number_format = "yyyy-mm-dd"
    widths = [11, 36, 38, 17, 12, 10, 24, 22, 20]
    for i, wdt in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wdt
    ws2 = wb.create_sheet("Agency facility numbers")
    ws2.append(["fund_code", "agency_facility_no", "valid_from", "valid_to"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for c in sorted(W.CREMATORIA, key=lambda x: x[0]):
        if c[0] == "CM-1590":
            ws2.append([c[0], W.WEXLEY_OLD_FACILITY, dt.date.fromisoformat(OPENED[c[0]]),
                        W.WEXLEY_RENUMBERED - dt.timedelta(days=1)])
            ws2.append([c[0], c[1], W.WEXLEY_RENUMBERED, None])
        else:
            ws2.append([c[0], c[1], dt.date.fromisoformat(OPENED[c[0]]), None])
    for row in ws2.iter_rows(min_row=2):
        for cell in row:
            if isinstance(cell.value, dt.date):
                cell.number_format = "yyyy-mm-dd"
    for i, wdt in enumerate([11, 20, 12, 12]):
        ws2.column_dimensions[chr(65 + i)].width = wdt
    wb.save(path)
    return len(W.CREMATORIA)


# ---------------------------------------------------------------- receivables
H_CODES = {"CREM": ("BRV-CREM", "Cremation - adult"), "CRMC": ("BRV-CRMC", "Cremation - child (no fee)"),
           "DIRC": ("BRV-DIRC", "Direct cremation (no service)"), "CHAP": ("BRV-CHAP", "Chapel service (40 min)"),
           "CHPC": ("BRV-CHAP", "Chapel service (40 min) - child, no fee"),
           "XTND": ("BRV-XTND", "Chapel - additional 20 min"), "ORGN": ("BRV-ORGN", "Organist"),
           "WEBC": ("BRV-WEBC", "Webcast and recording"), "MEMB": ("BRV-MEMB", "Book of Remembrance entry"),
           "SCAT": ("BRV-SCAT", "Scattering - Garden of Remembrance"),
           "CERT": ("BRV-CERT", "Certificate of cremation - certified copy"), "URN": ("BRV-URN", "Urn"),
           "KEEP": ("BRV-KEEP", "Keepsake"), "MREF": ("BRV-MREF", "Medical referee fee (disbursement)"),
           "ADJ": ("BRV-ADJ", "Account adjustment")}
S_DESC = {"CREM": "Cremation", "CRMC": "Cremation - child", "DIRC": "Direct cremation", "CHAP": "Chapel 40 min",
          "CHPC": "Chapel 40 min (child)", "XTND": "Chapel extension 20 min", "ORGN": "Organist",
          "WEBC": "Webcast & recording", "MEMB": "Memorial book entry", "SCAT": "Garden scattering",
          "CERT": "Certified copy - cremation certificate", "URN": "Urn", "KEEP": "Keepsake jewellery",
          "MREF": "Medical referee fee - disbursement", "ADJ": "Credit - account"}
F_CODES = {"CREM": ("CRM", "Cremation"), "CRMC": ("CRM", "Cremation (child, no fee)"), "DIRC": ("DCR", "Direct cremation"),
           "CHAP": ("CHP", "Chapel service"), "CHPC": ("CHP", "Chapel service (child, no fee)"),
           "XTND": ("CHX", "Chapel extension"), "ORGN": ("ORG", "Organist"), "WEBC": ("WEB", "Webcast"),
           "MEMB": ("BOR", "Book of remembrance"), "SCAT": ("SCT", "Scattering"), "CERT": ("CRT", "Certificate copies"),
           "URN": ("GDS", "Goods - urn"), "KEEP": ("GDS", "Goods - keepsake"), "MREF": ("DSB", "Disbursement - medical referee"),
           "ADJ": ("ADJ", "Account adjustment")}
SITE = {"CM-0417": "HMC", "CM-0738": "OHC"}
LOCATION = {"CM-1182": "Fenwick Harbour", "CM-2034": "Stannard Bay", "CM-1768": "Port Alder", "CM-2409": "Sorrel Bay"}
CASE_PREFIX = {"CM-1182": "FH", "CM-2034": "SB", "CM-1768": "PA", "CM-2409": "SO"}
BOOK_FMT = {"CM-0659": "LCC-{y}-{n:05d}", "CM-1590": "WRC-{y}-{n:05d}", "CM-2251": "HFH{y}{n:04d}", "CM-0896": "CN{y}/{n:04d}",
            "CM-1347": "AG-{y}-{n:04d}", "CM-0372": "TC{y}-{n:04d}", "CM-1925": "DF{n:05d}", "CM-2163": "BH{y}-{n:04d}",
            "CM-0514": "KL-{n:05d}", "CM-0283": "WYN{y}{n:04d}", "CM-1471": "BCS-{y}-{n:04d}",
            "CM-2087": "RV{y}{n:04d}", "CM-0941": "EMC/{y}/{n:04d}", "CM-1633": "GL-{y}{n:04d}"}


def _item_key(ar, ln):
    child = ar["books"][ln["b"]]["child"]
    if child and ln["item"] == "CREM":
        return "CRMC"
    if child and ln["item"] == "CHAP":
        return "CHPC"
    return ln["item"]


def booking_refs(ar):
    """Each crematorium's own booking or case number, in booking order within each year."""
    refs, cnt = {}, {}
    for bk in sorted(ar["books"], key=lambda b: (b["ci"], b["posted"], b["b"])):
        code = W.CREMATORIA[bk["ci"]][0]
        y = bk["date"].year
        cnt[(code, y)] = cnt.get((code, y), 0) + 1
        n = cnt[(code, y)] + 14 * (y == 2025) * 40
        if code in SITE:
            refs[bk["b"]] = "%s-%02d-%05d" % (SITE[code], y % 100, n)
        elif code in CASE_PREFIX:
            refs[bk["b"]] = "%s%02d-%04d" % (CASE_PREFIX[code], y % 100, n)
        else:
            refs[bk["b"]] = BOOK_FMT[code].format(y=y % 100, n=n)
    return refs


def documents(ar):
    """The ledger documents in posting order: an invoice per booking (its lines), a credit per credit."""
    docs = []
    by_b = {}
    for i, ln in enumerate(ar["lines"]):
        by_b.setdefault(ln["b"], []).append(i)
    for bk in ar["books"]:
        if dt.date(2025, 12, 1) <= bk["posted"] <= sim.LAST_POSTING:
            docs.append(("INV", bk["posted"], bk["ci"], bk["home"], bk["b"], by_b[bk["b"]], None))
    for j, cr in enumerate(ar["credits"]):
        docs.append(("CRN", cr["posted"], cr["ci"], cr["home"], cr["b"], cr["lines"], j))
    docs.sort(key=lambda d: (d[1], d[0] != "INV", d[2], d[4] if d[4] is not None else -1, d[6] if d[6] is not None else -1))
    return docs


def _cust_numbers(ar, rng):
    """Customer numbers per ledger and funeral home."""
    out = {}
    for ledger in sorted({sim.ledger(ci) for ci in range(len(W.CREMATORIA))}):
        homes = sorted({ar["fds"][ci][fd] for ci in range(len(W.CREMATORIA)) if sim.ledger(ci) == ledger
                        for fd in range(len(ar["fds"][ci]))})
        base = int(rng.integers(100, 900))
        for j, h in enumerate(homes):
            out[(ledger, h)] = base + 7 * j + int(rng.integers(0, 6))
    return out


def ledger_rows(ar):
    """Every ledger row the three receivables files carry, with its ledger, in posting order."""
    rng = _rng("ledgers")
    refs = booking_refs(ar)
    cust = _cust_numbers(ar, rng)
    rows = []
    docno = {}
    for kind, posted, ci, home, b, lines, j in documents(ar):
        code = W.CREMATORIA[ci][0]
        led = sim.ledger(ci)
        docno[(led, kind)] = docno.get((led, kind), 0) + 1
        dno = docno[(led, kind)]
        if kind == "INV":
            for i in lines:
                ln = ar["lines"][i]
                rows.append({"ledger": led, "ci": ci, "code": code, "kind": "INV", "dno": dno, "posted": posted,
                             "home": home, "cust": cust[(led, home)], "ref": refs[ln["b"]], "service": ln["date"],
                             "item": _item_key(ar, ln), "qty": ln["qty"], "unit": ln["unit"],
                             "net": round(ln["amount"], 2), "i": i, "j": None})
        else:
            cr = ar["credits"][j]
            if cr["kind"] == "booking":
                ln = ar["lines"][cr["lines"][0]]
                rows.append({"ledger": led, "ci": ci, "code": code, "kind": "CRN", "dno": dno, "posted": posted,
                             "home": home, "cust": cust[(led, home)], "ref": refs[ln["b"]], "service": ln["date"],
                             "item": _item_key(ar, ln), "qty": -ln["qty"], "unit": ln["unit"],
                             "net": -round(ln["amount"], 2), "i": None, "j": j})
            else:
                rows.append({"ledger": led, "ci": ci, "code": code, "kind": "CRN", "dno": dno, "posted": posted,
                             "home": home, "cust": cust[(led, home)], "ref": "", "service": None, "item": "ADJ",
                             "qty": 1, "unit": -cr["amount"], "net": -round(cr["amount"], 2), "i": None, "j": j})
    return rows


def _tax(item, net):
    return 0.0 if item == "MREF" else round(net * HST, 2)


def write_ar_halbrook(lrows, ar, path):
    cols = ["doc_no", "doc_type", "posting_date", "site", "customer_no", "customer_name", "booking_ref", "service_date",
            "item_code", "item_description", "quantity", "unit_price", "net_amount", "hst_amount"]
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in lrows:
            if r["ledger"] != "halbrook":
                continue
            code, desc = H_CODES[r["item"]]
            pre = "INV" if r["kind"] == "INV" else "CRN"
            w.writerow(["%s-%06d" % (pre, 31000 + r["dno"] if pre == "INV" else 2400 + r["dno"]), r["kind"],
                        r["posted"].isoformat(), SITE[r["code"]], "C%05d" % r["cust"], ar["homes"][r["home"]],
                        r["ref"], r["service"].isoformat() if r["service"] else "", code, desc, r["qty"],
                        "%.2f" % r["unit"], "%.2f" % r["net"], "%.2f" % _tax(r["item"], r["net"])])
            n += 1
    return n


def write_ar_shoreline(lrows, ar, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Receivables"
    hdr = ["Location", "Date", "Type", "No.", "Customer", "Case No.", "Service Date", "Product/Service", "Qty", "Rate",
           "Amount", "Sales Tax"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    n = 0
    for r in lrows:
        if r["ledger"] != "shoreline":
            continue
        typ = "Invoice" if r["kind"] == "INV" else "Credit Memo"
        no = ("%d" % (60000 + r["dno"])) if r["kind"] == "INV" else ("CM%d" % (1500 + r["dno"]))
        ws.append([LOCATION[r["code"]], r["posted"], typ, no, ar["homes"][r["home"]], r["ref"] or None, r["service"],
                   S_DESC[r["item"]], r["qty"], round(r["unit"], 2), round(r["net"], 2), _tax(r["item"], r["net"])])
        n += 1
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "dd/mm/yyyy"
        row[6].number_format = "dd/mm/yyyy"
        for c in row[9:12]:
            c.number_format = "#,##0.00"
    for i, wdt in enumerate([16, 11, 12, 9, 34, 10, 12, 36, 6, 10, 11, 10]):
        ws.column_dimensions[chr(65 + i)].width = wdt
    ws.freeze_panes = "A2"
    wb.save(path)
    return n


def write_ar_members(lrows, ar, path):
    """The Fund's fee return: each independent crematorium's lines, lodged weekly."""
    cols = ["fund_code", "week_ending", "lodged_on", "record", "booking_ref", "service_date", "fd_account", "fd_name",
            "fee_code", "fee_description", "qty", "amount_ex_tax"]
    rng = _rng("returns")
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        out = []
        for r in lrows:
            if r["ledger"] in ("halbrook", "shoreline"):
                continue
            wk = r["posted"] + dt.timedelta((6 - r["posted"].weekday()) % 7)        # week ending Sunday
            lodged = wk + dt.timedelta(int(1 + (sum(map(ord, r["code"])) % 4)))
            code, desc = F_CODES[r["item"]]
            out.append((r["code"], wk, r["posted"], r["kind"], r["dno"], r["i"] or 0, r["j"] or 0,
                        [r["code"], wk.isoformat(), lodged.isoformat(), "FEE" if r["kind"] == "INV" else "CREDIT",
                         r["ref"], r["service"].isoformat() if r["service"] else "",
                         "%s-%03d" % (r["code"][3:], r["cust"] % 1000), ar["homes"][r["home"]], code, desc, r["qty"],
                         "%.2f" % r["net"]]))
        out.sort(key=lambda x: (x[1], x[0], x[2], x[3], x[4], x[5], x[6]))
        for x in out:
            w.writerow(x[7])
            n += 1
    return n


# ---------------------------------------------------------------- controller cycles and plant logs
def write_cycles(cyc, path):
    cols = ["fund_code", "cremator", "cycle_no", "cycle_type", "charge_et", "end_et", "gas_m3", "max_chamber_c"]
    n = 0
    cnt = {}
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for x in sorted(cyc, key=lambda x: (W.CREMATORIA[x["ci"]][0], x["start"], x["cremator"])):
            code = W.CREMATORIA[x["ci"]][0]
            cnt[(code, x["cremator"])] = cnt.get((code, x["cremator"]), 0) + 1
            w.writerow([code, x["cremator"], "%d%05d" % (x["cremator"], cnt[(code, x["cremator"])]), x["type"],
                        x["start"].strftime("%Y-%m-%d %H:%M"), x["end"].strftime("%Y-%m-%d %H:%M"),
                        "%.1f" % x["gas"], x["tmax"]])
            n += 1
    return n


def to_utc(t):
    return t.replace(tzinfo=ET).astimezone(UTC)


def write_plant(plants, path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    codes, plant, ts, kind, event, detail, temp = [], [], [], [], [], [], []
    for ci in sorted(plants, key=lambda i: W.CREMATORIA[i][0]):
        p = plants[ci]
        code = W.CREMATORIA[ci][0]
        recs = [(to_utc(t), 0, "READING", None, None, v) for t, v in p["temps"]]
        recs += [(to_utc(t), 1, "EVENT", e, d, None) for t, e, d in p["events"]]
        recs.sort(key=lambda r: (r[0], r[1]))
        for t, _, k, e, d, v in recs:
            codes.append(code)
            plant.append("AP1")
            ts.append(t)
            kind.append(k)
            event.append(e)
            detail.append(d)
            temp.append(v)
    tab = pa.table({"fund_code": pa.array(codes, pa.string()), "plant": pa.array(plant, pa.string()),
                    "logged_utc": pa.array(ts, pa.timestamp("s", tz="UTC")), "record": pa.array(kind, pa.string()),
                    "event": pa.array(event, pa.string()), "detail": pa.array(detail, pa.string()),
                    "inlet_temp_c": pa.array(temp, pa.float64())})
    pq.write_table(tab, path, compression="snappy", use_dictionary=True, write_statistics=False)
    return tab.num_rows


# ---------------------------------------------------------------- deaths (distractor)
def write_deaths(rows, path):
    """The agency's preliminary count of deaths registered in 2026, all dispositions, by region, age and sex."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    rng = _rng("deaths")
    groups = [(0, 0), (1, 14), (15, 44)] + [(lo, lo + 4) for lo in range(45, 90, 5)] + [(90, 200)]
    cnt = {}
    for r in rows:
        if r["death"].year != 2026:
            continue
        g = next(i for i, (lo, hi) in enumerate(groups) if lo <= r["age"] <= hi)
        reg = REGION_OF[r["code"]]
        cnt[(reg, g, r["sex"])] = cnt.get((reg, g, r["sex"]), 0) + 1
    wb = Workbook()
    ws = wb.active
    ws.title = "Deaths 2026"
    ws["A1"] = "Deaths registered in 2026 by health region of residence, age group and sex (preliminary)"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Vital Statistics Agency, extracted 2027-02-12. All dispositions. Out-of-province residents excluded."
    ws.append([])
    hdr = ["Health region", "Age group"] + ["Males", "Females", "Total"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    n = 0
    for reg in range(len(REGIONS)):
        for g, (lo, hi) in enumerate(groups):
            lab = "Under 1" if hi == 0 else ("%d and over" % lo if hi >= 200 else "%d to %d" % (lo, hi))
            vals = []
            for s in "MF":
                c = cnt.get((reg, g, s), 0)
                share = 0.70 + 0.05 * math.tanh((lo - 70) / 15.0)            # cremation's share rises with age
                if c:                                                        # never fewer than the cremations
                    vals.append(max(c, int(round(c / share + rng.normal(0, 2.0)))))
                else:
                    vals.append(int(rng.integers(0, 4)))
            ws.append([REGIONS[reg], lab, vals[0], vals[1], vals[0] + vals[1]])
            n += 1
    for i, wdt in enumerate([18, 12, 9, 9, 9]):
        ws.column_dimensions[chr(65 + i)].width = wdt
    wb.save(path)
    return n
