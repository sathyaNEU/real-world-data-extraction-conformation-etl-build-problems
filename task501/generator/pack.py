"""Writes the data files of the task501 pack from the observed world. Documents are in docs.py."""
import csv
import json
import os
import zipfile
from datetime import date, datetime, timedelta

import numpy as np
import openpyxl
from openpyxl.styles import Font

import world as W
import observe as O

T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
STAMP = (2027, 1, 5, 7, 40, 0)
CORE_TIMES = {"fondsregister_2026-12-31.xlsx": ("2015-05-11T07:20:00Z", "2026-12-31T15:12:00Z"),
              "kapitalkonten_revidiert_2021-2025.xlsx": ("2022-05-19T08:02:00Z", "2026-06-18T12:37:00Z"),
              "richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx": ("2026-08-27T13:05:00Z", "2026-09-25T07:48:00Z")}
AUDITORS = {"US": "Hendricks Morgan LLP", "GB": "Castellane Audit LLP", "DE": "Reinhart Treuhand GmbH", "FR": "Cabinet Vauclair",
            "CH": "Brauchli & Partner AG", "SE": "Lindqvist Revision AB", "NO": "Lindqvist Revision AB", "DK": "Lindqvist Revision AB",
            "IE": "Castellane Audit LLP"}
LEGAL_FORM = {"US": "Delaware LP", "GB": "English LP", "DE": "GmbH & Co. KG", "FR": "FPCI", "CH": "KmGK", "SE": "Kommanditbolag",
              "NO": "Kommandittselskap", "DK": "K/S", "IE": "ILP"}

LEDGER = "kapitalabrufe_ausschuettungen_2015-2026.csv"
REGISTER = "fondsregister_2026-12-31.xlsx"
FXFILE = "fx_referenzkurse_tagesende.csv"
CUSTODY = "programmkonto_lindenhof_2025-2026.csv"
AUDITED = "kapitalkonten_revidiert_2021-2025.xlsx"
NAVREG = "nav_register_quartal.csv"
HOLDINGS = "look_through_bestaende_2016-2026.csv"


def fmt(d):
    return d.isoformat()


def fix_zip_times(path, stamp=STAMP, core=None):
    """Rewrite an OOXML container with every entry stamped at the export time, same order, same bytes; with core, also set
    the document's created and modified instants (docProps/core.xml), which the writing library takes from the clock."""
    import re
    src = zipfile.ZipFile(path)
    items = [(zi, src.read(zi.filename)) for zi in src.infolist()]
    src.close()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for zi, data in items:
            if core and zi.filename == "docProps/core.xml":
                x = data.decode("utf-8")
                for tag, val in (("created", core[0]), ("modified", core[1])):
                    x = re.sub(r"(<dcterms:%s[^>]*>)[^<]*(</dcterms:%s>)" % (tag, tag), r"\g<1>%s\g<2>" % val, x)
                data = x.encode("utf-8")
            nz = zipfile.ZipInfo(zi.filename, date_time=stamp)
            nz.compress_type = zipfile.ZIP_DEFLATED
            nz.external_attr = zi.external_attr
            out.writestr(nz, data)


PDF_INFO = {"term_sheet_lindenhof_standby_2027.pdf": ("20261209083000", "20261209083000", "Privatbank Lindenhof AG"),
            "stiftungsrat_protokoll_auszug_2026-09-24.pdf": ("20260930091500", "20261001134000", None),
            "halbjahresbericht_privatmarkt_2025-H1.pdf": ("20250911122200", "20250916081000", None)}


def fix_pdf_info(path, created, modified, producer=None):
    """Equal-length substitution in a scrubbed PDF's information dictionary (xref offsets unchanged): the document's own
    creation and modification instants, and for a document received from outside, its sender as producer."""
    import re
    b = open(path, "rb").read()
    n = len(b)
    b = re.sub(rb"/CreationDate \(D:\d{14}", b"/CreationDate (D:" + created.encode(), b, count=1)
    b = re.sub(rb"/ModDate \(D:\d{14}", b"/ModDate (D:" + modified.encode(), b, count=1)
    if producer:
        m = re.search(rb"/Producer \(([^)]*)\)", b)
        old = m.group(1)
        new = producer.encode()
        assert len(new) <= len(old) + 0, (old, new)
        b = b[:m.start(1)] + new + b")" + b" " * (len(old) - len(new)) + b[m.end(1) + 1:]
    assert len(b) == n
    open(path, "wb").write(b)


def write_ledger(obs):
    rng = np.random.RandomState(W.SEED * 17)
    rows = []
    for r in sorted(obs["records"], key=lambda x: (x["notice_date"], x["notice_id"], x["fund"].fund_id)):
        f = r["fund"]
        for i, (lt, ref, desc, amt) in enumerate(r["lines"], 1):
            ccy = f.ccy
            d = desc
            if r["source"] == "clerk":
                if rng.rand() < 0.015:
                    ccy = ccy.lower()
                if rng.rand() < 0.03:
                    d = d + "  "
                if rng.rand() < 0.02:
                    d = d.upper()
                ent = datetime.combine(r["notice_date"] + timedelta(days=int(rng.randint(0, 3))), datetime.min.time()) + \
                    timedelta(hours=int(rng.randint(8, 18)), minutes=int(rng.randint(0, 60)))
            else:
                ent = datetime.combine(W.add_bdays(r["notice_date"], 1), datetime.min.time()) + timedelta(hours=6, minutes=int(rng.randint(5, 50)))
            if ent.date() > W.EXTRACT_RUN - timedelta(days=1):
                ent = datetime.combine(W.EXTRACT_RUN - timedelta(days=1), datetime.min.time()) + timedelta(hours=17, minutes=int(rng.randint(0, 50)))
            rows.append([r["notice_id"], f.fund_id, f.code, r["type"], fmt(r["notice_date"]), fmt(r["value_date"]), r["status"], i, lt, ref, d,
                         ccy, f"{amt:.2f}", ent.strftime("%Y-%m-%d %H:%M"), r.get("remarks", "")])
    with open(os.path.join(T, LEDGER), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["notice_id", "fund_id", "fund_code", "notice_type", "notice_date", "value_date", "status", "line_no", "line_type",
                    "investment_ref", "description", "currency", "amount", "entered_at", "remarks"])
        w.writerows(rows)
    return len(rows)


def write_register(funds):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fonds"
    hdr = ["fund_id", "fund_code", "fund_name", "manager", "strategy", "vintage", "currency", "commitment", "first_close", "final_close",
           "investment_period_end", "term_end", "management_fee_ip_pa", "domicile", "legal_form", "lei", "paying_agent", "status"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    for f in funds:
        # a final close still to come is not in the register
        ws.append([f.fund_id, f.code, f.name, f.manager, f.strategy, f.vintage, f.ccy, f.commitment, f.first_close,
                   f.final_close if f.final_close <= W.PLAN_DATE else None,
                   f.ip_end, f.term_end, round(f.fee_ip, 4), f.domicile, LEGAL_FORM[f.domicile], f.lei, f.paying_agent,
                   "active" if f.term_end > W.PLAN_DATE else "term ended"])
    for row in ws.iter_rows(min_row=2):
        for c in row:
            if hasattr(c.value, "year") and not isinstance(c.value, (int, float)):
                c.number_format = "yyyy-mm-dd"
        row[7].number_format = "#,##0"
    ws2 = wb.create_sheet("Strategien")
    ws2.append(["strategy", "label_en", "label_de"])
    for k, v in W.STRATEGIES.items():
        ws2.append([k, v, W.STRATEGY_DE[k]])
    ws3 = wb.create_sheet("Hinweise")
    for line in [
        "Fondsregister Privatmarktprogramm, Stand 31.12.2026. Gepflegt durch Rechnungswesen (N. Hess), bestaetigt durch Portfolio Management (T. Sigrist).",
        "Statische Vertragsdaten gemaess Limited Partnership Agreement und Side Letter; keine Bewertungen, keine Kapitalkontostaende.",
        "commitment: Zusage in Fondswaehrung. investment_period_end und term_end: as stated in the limited partnership agreement; no extension has been requested.",
        "Under every agreement in the programme, capital may be called after the end of the investment period only for follow-on investments in existing portfolio companies and for partnership expenses; the management fee is then deducted from proceeds.",
        "management_fee_ip_pa: Verwaltungsgebuehr p.a. auf der Zusage waehrend der Investitionsperiode.",
    ]:
        ws3.append([line])
    wb.save(os.path.join(T, REGISTER))
    fix_zip_times(os.path.join(T, REGISTER))


# the custodian's reference-rate table carries every currency it quotes against the franc; the programme's funds are in
# francs, dollars and euros. Crosses follow the market's own anchors (pegs for DKK and HKD), quoted per 1 or per 100 units.
OTHER_CCY = [  # code, unit, base, anchors of the cross against the base
    ("GBP", 1, "EUR", [(2015, 1, 1.29), (2015, 7, 1.40), (2016, 6, 1.24), (2016, 10, 1.11), (2018, 6, 1.13), (2020, 3, 1.09),
                      (2021, 6, 1.16), (2022, 9, 1.13), (2023, 12, 1.15), (2024, 9, 1.19), (2025, 6, 1.17), (2026, 12, 1.15)]),
    ("JPY", 100, "USD", [(2015, 1, 119.0), (2015, 6, 124.0), (2016, 9, 102.0), (2018, 6, 110.0), (2020, 3, 108.0), (2021, 6, 110.0),
                         (2022, 10, 148.0), (2023, 12, 142.0), (2024, 6, 160.0), (2025, 6, 145.0), (2026, 12, 151.0)]),
    ("SEK", 100, "EUR", [(2015, 1, 9.40), (2016, 12, 9.70), (2018, 9, 10.40), (2020, 3, 10.90), (2021, 6, 10.10), (2022, 9, 10.90),
                         (2023, 9, 11.80), (2024, 6, 11.30), (2025, 6, 11.00), (2026, 12, 10.85)]),
    ("NOK", 100, "EUR", [(2015, 1, 9.00), (2016, 1, 9.60), (2018, 6, 9.50), (2020, 3, 11.50), (2021, 6, 10.20), (2022, 9, 10.30),
                         (2023, 10, 11.80), (2024, 6, 11.50), (2025, 6, 11.60), (2026, 12, 11.70)]),
    ("DKK", 100, "EUR", [(2015, 1, 7.443), (2017, 6, 7.437), (2020, 3, 7.472), (2023, 6, 7.449), (2026, 12, 7.462)]),
    ("CAD", 1, "USD", [(2015, 1, 1.17), (2016, 1, 1.42), (2017, 9, 1.23), (2018, 12, 1.36), (2020, 3, 1.42), (2021, 6, 1.24),
                       (2022, 10, 1.37), (2023, 12, 1.33), (2024, 12, 1.43), (2025, 6, 1.37), (2026, 12, 1.38)]),
    ("AUD", 1, "USD", [(2015, 1, 0.81), (2016, 1, 0.70), (2018, 1, 0.80), (2020, 3, 0.60), (2021, 3, 0.77), (2022, 10, 0.63),
                       (2023, 12, 0.67), (2024, 9, 0.69), (2025, 6, 0.65), (2026, 12, 0.66)]),
    ("HKD", 100, "USD", [(2015, 1, 7.756), (2016, 6, 7.759), (2018, 6, 7.848), (2020, 6, 7.751), (2022, 9, 7.849), (2024, 6, 7.808),
                         (2026, 12, 7.785)]),
    ("SGD", 1, "USD", [(2015, 1, 1.32), (2015, 9, 1.42), (2017, 12, 1.34), (2020, 3, 1.43), (2021, 6, 1.33), (2022, 10, 1.43),
                       (2023, 12, 1.32), (2024, 6, 1.36), (2025, 6, 1.28), (2026, 12, 1.29)]),
]
INVERSE = {"JPY", "SEK", "NOK", "DKK", "CAD", "HKD", "SGD"}  # anchors are units of the currency per unit of the base


def _cross_path(days, anchors, vol, rng):
    pts = [(date(y, m, 1).toordinal(), v) for y, m, v in anchors]
    x = anchors[0][2]
    out = {}
    for d in days:
        o = d.toordinal()
        tgt = pts[-1][1]
        for (o0, v0), (o1, v1) in zip(pts, pts[1:]):
            if o0 <= o <= o1:
                tgt = v0 + (v1 - v0) * (o - o0) / max(o1 - o0, 1)
                break
        x += 0.10 * (tgt - x) + rng.normal(0, vol * tgt)
        out[d] = x
    return out


def write_fx(fx_rows):
    rng = np.random.RandomState(W.SEED * 41)
    days = [d for d, _, _ in fx_rows]
    base = {d: dict(USD=u, EUR=e) for d, u, e in fx_rows}
    vols = dict(GBP=0.0030, JPY=0.0040, SEK=0.0028, NOK=0.0032, DKK=0.00012, CAD=0.0026, AUD=0.0040, HKD=0.00025, SGD=0.0018)
    paths = {c: _cross_path(days, a, vols[c], rng) for c, _, _, a in OTHER_CCY}
    rows = []
    for d in days:
        quotes = [("USD", 1, base[d]["USD"]), ("EUR", 1, base[d]["EUR"])]
        for c, unit, b, _ in OTHER_CCY:
            x = paths[c][d]
            per_one = base[d][b] / x if c in INVERSE else base[d][b] * x
            quotes.append((c, unit, round(per_one * unit, 4)))
        for c, unit, v in sorted(quotes):
            rows.append([fmt(d), c, unit, f"{v:.4f}", "custodian reference rate 16:00 Zurich"])
    with open(os.path.join(T, FXFILE), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rate_date", "currency", "unit", "rate_chf", "source"])
        w.writerows(rows)
    return len(rows)


def write_custody(rows):
    seq = 0
    out = []
    bal = next(r["amount"] for r in rows if r["kind"] == "open")
    for r in sorted(rows, key=lambda x: (x["booking_date"], {"open": 0, "topup": 1, "call": 2, "facility": 3, "dist": 4, "sweep": 5,
                                                              "interest": 6, "fee": 7, "charge": 8}[x["kind"]], x["reference"])):
        seq += 1
        if r["kind"] != "open":
            bal += r["amount"]
        tref = r["transaction_ref"] or f"PM{r['booking_date'].year % 100:02d}-{900000 + seq:06d}"
        out.append([fmt(r["booking_date"]), fmt(r["value_date"]), r["text"], r["counterparty"], r["reference"], tref,
                    f"{r['amount']:.2f}" if r["kind"] != "open" else "", f"{bal:.2f}"])
    with open(os.path.join(T, CUSTODY), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Buchungsdatum", "Valuta", "Buchungstext", "Gegenpartei", "Referenz", "Transaktionsreferenz", "Betrag CHF", "Saldo CHF"])
        w.writerows(out)
    return len(out)


def audited_cells(funds):
    cells = []
    for f in funds:
        calls = [n for n in f.notices if n["type"] == "CAPITAL_CALL" and n["status"] == "ISSUED"]
        if not calls:
            continue
        first = min(n["value_date"] for n in calls)
        for y in range(2021, 2026):
            fy = date(y, 12, 31)
            if first > fy:
                continue
            contrib = sum(l[3] for n in calls if n["value_date"] <= fy for l in n["lines"])
            dist = sum(l[3] for n in f.notices if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED" and n["value_date"] <= fy for l in n["lines"])
            cells.append(dict(fund=f, fy=fy, contrib=round(contrib, 2), dist=round(dist, 2), nav=f.nav_q.get((y, 4), 0.0),
                              unfunded=round(f.commitment - contrib, 2)))
    return cells


def write_audited(funds, cells):
    rng = np.random.RandomState(W.SEED * 19)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kapitalkonten"
    ws.append(["fund_id", "fund_code", "fy_end", "currency", "commitment", "contributions_since_inception", "distributions_since_inception",
               "nav_fy_end", "unfunded_commitment", "auditor", "opinion_date", "source_document"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for cell in sorted(cells, key=lambda c: (c["fy"], c["fund"].fund_id)):
        f = cell["fund"]
        od = date(cell["fy"].year + 1, int(rng.randint(3, 7)), int(rng.randint(2, 28)))
        ws.append([f.fund_id, f.code, cell["fy"], f.ccy, f.commitment, cell["contrib"], cell["dist"], cell["nav"], cell["unfunded"],
                   AUDITORS[f.domicile], od, f"{f.code} audited financial statements FY{cell['fy'].year}, capital account of {W.ORG}"])
    for row in ws.iter_rows(min_row=2):
        row[2].number_format = "yyyy-mm-dd"
        row[10].number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("Erfassung")
    ws2.append(["Erfasst aus den revidierten Jahresabschluessen der Fonds (Kapitalkonto der Pensionskasse Werdinsel), Betraege in Fondswaehrung. "
                "Erfassung N. Hess, letzte Ergaenzung 18.06.2026 (FY2025). FY2026-Abschluesse liegen ab Maerz 2027 vor."])
    wb.save(os.path.join(T, AUDITED))
    fix_zip_times(os.path.join(T, AUDITED))
    return len(cells)


def write_nav_register(funds, fx):
    rng = np.random.RandomState(W.SEED * 23)
    rows = []
    for f in funds:
        for (y, q), nav in sorted(f.nav_q.items()):
            if y < 2019:
                continue
            pe = W.month_end(W.month_index(y, q * 3))
            if pe > W.PLAN_DATE:
                continue
            lag = int(rng.randint(95, 140)) if q == 4 else int(rng.randint(42, 92))
            if (y, q) == (2026, 3) and f.idx % 7 == 3:
                lag += 50  # a handful of managers report the third quarter late
            received = W.bday(pe + timedelta(days=lag))
            if received > W.EXTRACT_RUN - timedelta(days=1):
                continue
            booking = W.bday(received + timedelta(days=int(rng.randint(1, 4))))
            if booking > W.EXTRACT_RUN - timedelta(days=1):
                booking = W.bday_back(W.EXTRACT_RUN - timedelta(days=1))
            rate = fx.rate(booking, f.ccy)
            stype = "annual audited" if q == 4 else "quarterly report"
            rows.append([f.fund_id, fmt(pe), stype, f"{nav:.2f}", f.ccy, fmt(received), fmt(booking), f"{rate:.4f}", f"{nav * rate:.2f}",
                         f"{f.code} {stype} {pe.isoformat()}"])
    rows.sort(key=lambda r: (r[1], r[0]))
    with open(os.path.join(T, NAVREG), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fund_id", "period_end", "statement_type", "nav_fund_ccy", "currency", "received_date", "booking_date", "fx_rate_booked",
                    "nav_chf_booked", "source_ref"])
        w.writerows(rows)
    return len(rows)


def write_holdings(funds):
    """The managers' quarterly schedules of investments as loaded into the look-through system, 2017 to the third quarter of 2026."""
    rows = []
    rng = np.random.RandomState(W.SEED * 29)
    split = {}
    for f in funds:
        for iv in f.investments:
            # buyout, growth and infrastructure deals are often funded partly by a shareholder loan, reported as a line of its own
            if f.strategy != "PC" and rng.rand() < 0.62:
                split[iv.ref] = float(rng.choice([0.2, 0.25, 0.3, 0.35, 0.4]))
    for f in funds:
        for (y, q) in sorted(f.nav_q):
            if (y, q) < (2016, 1) or (y, q) > (2026, 3):
                continue
            qe = W.month_end(W.month_index(y, q * 3))
            for iv in f.investments:
                if iv.initial_date > qe:
                    continue
                if iv.exit_date is not None and iv.exit_date <= qe and iv.status != "HELD":
                    continue
                cost = sum(a for d, a in iv.tranches if d <= qe)
                prog = min(1.0, (qe - iv.initial_date).days / max(iv.hold_days, 1))
                fv = cost * (1.0 + (iv.multiple - 1.0) * prog ** 1.3)
                sl = split.get(iv.ref, 0.0)
                if sl:
                    lc, lv = round(cost * sl, 2), round(fv * sl, 2)
                    rows.append([f.fund_id, fmt(qe), iv.ref, iv.company, iv.country, iv.sector, iv.instrument, fmt(iv.initial_date),
                                 f"{cost - lc:.2f}", f"{fv - lv:.2f}", f.ccy])
                    rows.append([f.fund_id, fmt(qe), iv.ref, iv.company, iv.country, iv.sector, "Shareholder loan", fmt(iv.initial_date),
                                 f"{lc:.2f}", f"{lv:.2f}", f.ccy])
                else:
                    rows.append([f.fund_id, fmt(qe), iv.ref, iv.company, iv.country, iv.sector, iv.instrument, fmt(iv.initial_date),
                                 f"{cost:.2f}", f"{fv:.2f}", f.ccy])
    rows.sort(key=lambda r: (r[1], r[0], r[2]))
    with open(os.path.join(T, HOLDINGS), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fund_id", "report_date", "investment_ref", "company", "country", "nace_section", "instrument", "initial_investment_date",
                    "cost_to_date", "fair_value", "currency"])
        w.writerows(rows)
    return len(rows)
