"""Writes the data files of the task501 pack from the simulated world. Documents are in docs.py."""
import csv
import json
import os
from datetime import date, datetime, timedelta

import numpy as np
import openpyxl
from openpyxl.styles import Font

import sim

T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
AUDITORS = {"US": "Hendricks Morgan LLP", "GB": "Castellane Audit LLP", "DE": "Reinhart Treuhand GmbH", "FR": "Cabinet Vauclair",
            "CH": "Brauchli & Partner AG", "SE": "Lindqvist Revision AB", "NO": "Lindqvist Revision AB", "DK": "Lindqvist Revision AB",
            "IE": "Castellane Audit LLP"}


def fmt(d):
    return d.isoformat()


def fix_zip_times(path, stamp=(2026, 10, 1, 7, 40, 0)):
    """Rewrite an OOXML container with every entry stamped at the export time, same order, same bytes."""
    import zipfile
    src = zipfile.ZipFile(path)
    items = [(zi, src.read(zi.filename)) for zi in src.infolist()]
    src.close()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for zi, data in items:
            nz = zipfile.ZipInfo(zi.filename, date_time=stamp)
            nz.compress_type = zipfile.ZIP_DEFLATED
            nz.external_attr = zi.external_attr
            out.writestr(nz, data)


def fx_lookup(fx_rows):
    table = {r[0]: (r[1], r[2]) for r in fx_rows}
    days = sorted(table)

    def get(d, ccy):
        if ccy == "CHF":
            return 1.0
        while d not in table:
            d -= timedelta(days=1)
        return table[d][0] if ccy == "USD" else table[d][1]
    return get


def apply_cancellations(funds):
    """Twelve call notices withdrawn by the manager and reissued under a new number a few days later."""
    rng = np.random.RandomState(sim.SEED * 13)
    calls = [(f, n) for f in funds for n in f.notices if n["type"] == "CAPITAL_CALL" and date(2019, 1, 1) <= n["notice_date"] < date(2026, 1, 1)]
    recent = [(f, n) for f in funds for n in f.notices if n["type"] == "CAPITAL_CALL" and date(2026, 1, 1) <= n["notice_date"] <= date(2026, 8, 31)]
    picks = [calls[k] for k in sorted(rng.choice(len(calls), 9, replace=False))] + [recent[k] for k in sorted(rng.choice(len(recent), 3, replace=False))]
    for f, n in picks:
        shift = int(rng.randint(2, 6))
        new = dict(n)
        new["notice_id"] = n["notice_id"] + "R"
        new["notice_date"] = sim.bday(n["notice_date"] + timedelta(days=shift))
        new["value_date"] = sim.bday(n["value_date"] + timedelta(days=shift))
        if new["notice_date"].month == 12 and new["value_date"].month == 1:
            new["value_date"] = sim.bday_back(date(new["notice_date"].year, 12, 30))
        new["status"] = "ISSUED"
        new["remarks"] = f"reissue of {n['notice_id']}"
        n["status"] = "CANCELLED"
        n["remarks"] = f"withdrawn by manager; reissued as {new['notice_id']}"
        f.notices.append(new)


def write_spine(funds):
    rng = np.random.RandomState(sim.SEED * 17)
    rows = []
    for f in funds:
        for n in sorted(f.notices, key=lambda x: (x["notice_date"], x["notice_id"])):
            for i, (lt, ref, desc, amt) in enumerate(n["lines"], 1):
                ccy = f.ccy
                if rng.rand() < 0.015:
                    ccy = ccy.lower()
                d = desc
                if rng.rand() < 0.03:
                    d = d + "  "
                if rng.rand() < 0.02:
                    d = d.upper()
                entered = datetime.combine(n["notice_date"] + timedelta(days=int(rng.randint(0, 3))), datetime.min.time()) + timedelta(hours=int(rng.randint(8, 18)), minutes=int(rng.randint(0, 60)))
                if entered.date() > sim.EXTRACT:
                    entered = datetime.combine(sim.EXTRACT, datetime.min.time()) + timedelta(hours=16)
                rows.append([n["notice_id"], f.fund_id, f.code, n["type"], fmt(n["notice_date"]), fmt(n["value_date"]), n["status"], i, lt, ref, d, ccy, f"{amt:.2f}", entered.strftime("%Y-%m-%d %H:%M"), n.get("remarks", "")])
    rows.sort(key=lambda r: (r[4], r[0], r[7]))
    with open(os.path.join(T, "kapitalabrufe_ausschuettungen_2015-2026.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["notice_id", "fund_id", "fund_code", "notice_type", "notice_date", "value_date", "status", "line_no", "line_type", "investment_ref", "description", "currency", "amount", "entered_at", "remarks"])
        w.writerows(rows)
    return len(rows)


def write_register(funds):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fonds"
    hdr = ["fund_id", "fund_code", "fund_name", "manager", "strategy", "vintage", "currency", "commitment", "first_close", "final_close", "admission_date", "investment_period_end", "term_end", "recycling_months", "recycling_basis", "domicile", "legal_form", "lei", "status"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    legal = {"US": "Delaware LP", "GB": "English LP", "DE": "GmbH & Co. KG", "FR": "FPCI", "CH": "KmGK", "SE": "Kommanditbolag", "NO": "Kommandittselskap", "DK": "K/S", "IE": "ILP"}
    for f in funds:
        ws.append([f.fund_id, f.code, f.name, f.manager, f.strategy, f.vintage, f.ccy, f.commitment, f.first_close, f.final_close, f.first_close, f.ip_end, f.term_end, 18, "return of capital, during the investment period", f.domicile, legal[f.domicile], f.lei, "committed" if f.first_call_month is None or not f.notices else "active"])
    ws2 = wb.create_sheet("Strategien")
    ws2.append(["strategy", "label_en", "label_de"])
    de = {"BO": "Buyout", "GR": "Wachstumskapital", "PC": "Privatkredit", "IN": "Infrastruktur"}
    for k, v in sim.STRATEGIES.items():
        ws2.append([k, v, de[k]])
    ws3 = wb.create_sheet("Hinweise")
    ws3.append(["Fondsregister Privatmarktprogramm, Stand 30.09.2026. Gepflegt durch Rechnungswesen (N. Amrein). Statische Vertragsdaten gemaess LPA und Side Letter (inkl. Recycling-Klausel: Rueckfluesse aus Beteiligungen, die innert recycling_months nach Ersterwerb realisiert werden, erhoehen waehrend der Investitionsperiode die offene Zusage wieder); keine Bewertungen, keine Kapitalkontostaende."])
    wb.save(os.path.join(T, "fondsregister_2026-09-30.xlsx"))
    fix_zip_times(os.path.join(T, "fondsregister_2026-09-30.xlsx"))


def write_investments(funds):
    rows = []
    for f in funds:
        for iv in f.investments:
            rows.append([f.fund_id, iv.ref, iv.company, iv.country, iv.sector, iv.instrument, fmt(iv.initial_date), f"{iv.cost:.2f}",
                         iv.status, fmt(iv.exit_date) if iv.status != "HELD" else "", fmt(min(sim.EXTRACT, iv.exit_date if iv.status != "HELD" else sim.EXTRACT))])
    rows.sort(key=lambda r: (r[0], r[6], r[1]))
    with open(os.path.join(T, "beteiligungsverzeichnis_2026-09-30.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fund_id", "investment_ref", "company", "country", "sector_nace", "instrument", "initial_investment_date", "cost_to_date", "status", "realisation_date", "last_update"])
        w.writerows(rows)
    return len(rows)


def audited_cells(funds):
    """One row per fund and audited year-end 2021 to 2025: the controls."""
    cells = []
    for f in funds:
        if f.first_call_month is None or not f.notices:
            continue
        for y in range(2021, 2026):
            fy = date(y, 12, 31)
            first = min(n["notice_date"] for n in f.notices if n["type"] == "CAPITAL_CALL")
            if first > fy:
                continue
            contrib = sum(l[3] for n in f.notices if n["type"] == "CAPITAL_CALL" and n["status"] == "ISSUED" and n["notice_date"] <= fy for l in n["lines"])
            dist = sum(l[3] for n in f.notices if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED" and n["notice_date"] <= fy for l in n["lines"])
            ivs = {iv.ref: iv for iv in f.investments}
            rec = sum(l[3] for n in f.notices if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED" and n["notice_date"] <= fy
                      for l in n["lines"] if l[0] == "RETURN_OF_CAPITAL" and ivs[l[1]].recallable > 0)
            nav = f.nav_q.get((y, 4), 0.0)
            cells.append(dict(fund=f, fy=fy, contrib=round(contrib, 2), dist=round(dist, 2), nav=nav, unfunded=round(f.commitment - contrib + rec, 2), rec=round(rec, 2)))
    return cells


def write_audited(funds, cells):
    rng = np.random.RandomState(sim.SEED * 19)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kapitalkonten"
    ws.append(["fund_id", "fund_code", "fy_end", "currency", "commitment", "contributions_since_inception", "distributions_since_inception", "nav_fy_end", "unfunded_commitment", "auditor", "opinion_date", "source_document"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for cell in sorted(cells, key=lambda c: (c["fy"], c["fund"].fund_id)):
        f = cell["fund"]
        od = date(cell["fy"].year + 1, int(rng.randint(3, 7)), int(rng.randint(2, 28)))
        ws.append([f.fund_id, f.code, cell["fy"], f.ccy, f.commitment, cell["contrib"], cell["dist"], cell["nav"], cell["unfunded"], AUDITORS[f.domicile], od, f"{f.code} audited financial statements FY{cell['fy'].year}, capital account of {sim.ORG}"])
    ws2 = wb.create_sheet("Erfassung")
    ws2.append(["Erfasst aus den revidierten Jahresabschluessen der Fonds (Kapitalkonto der Pensionskasse Werdinsel), Betraege in Fondswaehrung. Erfassung N. Amrein, letzte Ergaenzung 11.06.2026 (FY2025). FY2026-Abschluesse liegen erst ab Maerz 2027 vor."])
    wb.save(os.path.join(T, "kapitalkonten_revidiert_2021-2025.xlsx"))
    fix_zip_times(os.path.join(T, "kapitalkonten_revidiert_2021-2025.xlsx"))


def write_nav_register(funds, fx_get):
    rng = np.random.RandomState(sim.SEED * 23)
    late_q2 = {"PKW-F-113", "PKW-F-128", "PKW-F-140"}     # three Q2 2026 statements not yet received
    rows = []
    for f in funds:
        for (y, q), nav in sorted(f.nav_q.items()):
            if y < 2019:
                continue
            pe = sim.month_end(sim.month_index(y, q * 3))
            if q == 4:
                lag = int(rng.randint(95, 140))
                stype = "annual audited"
            else:
                lag = int(rng.randint(42, 88))
                stype = "quarterly report"
            if (y, q) == (2026, 2) and f.fund_id in late_q2:
                lag = int(rng.randint(100, 130))
            received = sim.bday(pe + timedelta(days=lag))
            if received > sim.EXTRACT:
                continue
            booking = sim.bday(received + timedelta(days=int(rng.randint(1, 4))))
            rate = fx_get(booking, f.ccy)
            rows.append([f.fund_id, fmt(pe), stype, f"{nav:.2f}", f.ccy, fmt(received), fmt(booking), f"{rate:.4f}", f"{nav * rate:.2f}", f"{f.code} {stype} {pe.isoformat()}"])
    rows.sort(key=lambda r: (r[1], r[0]))
    with open(os.path.join(T, "nav_register_quartal.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fund_id", "period_end", "statement_type", "nav_fund_ccy", "currency", "received_date", "booking_date", "fx_rate_booked", "nav_chf_booked", "source_ref"])
        w.writerows(rows)
    return len(rows), late_q2


def write_fx(fx_rows):
    with open(os.path.join(T, "fx_referenzkurse_tagesende.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rate_date", "USDCHF", "EURCHF", "source"])
        for d, u, e in fx_rows:
            w.writerow([fmt(d), f"{u:.4f}", f"{e:.4f}", "custodian reference rate 16:00 Zurich"])
    return len(fx_rows)
