"""The pack's documents, short and in their owners' voices."""
import datetime as dt
import os
import shutil
import subprocess
import tempfile

import docx
import openpyxl
from docx.shared import Cm, Pt
from openpyxl.styles import Alignment, Font, PatternFill

import zlib

import world as W

SCOPES = ["Replace feeder protection, %d bays", "Protection and control panel replacement (%d feeder bays)",
          "Feeder relay replacement, %d bays, with panel rewiring", "P&C rebuild with new control building (%d bays)",
          "Replace VPR-340 feeder relays (%d) and RTU", "Feeder protection upgrade, %d bays, IEC 61850 station bus"]


def _doc(author, title, created, font="Calibri"):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = font
    st.font.size = Pt(10.5)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.59), Cm(27.94)
        s.left_margin = s.right_margin = Cm(2.3)
        s.top_margin = Cm(1.9)
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.created = created
    cp.modified = created
    cp.revision = 4
    cp.comments = cp.keywords = cp.subject = cp.category = ""
    return d


def _p(d, text, bold=False, size=None, after=4, italic=False):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(after)
    return p


def _pdf(d, out_path, stem):
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, stem + ".docx")
    d.save(src)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.move(os.path.join(tmp, stem + ".pdf"), out_path)
    shutil.rmtree(tmp)


def procedure_docx(path):
    d = _doc("Kurt Allison", "AM-PC-014 Obsolete protection spares: final-buy sizing", dt.datetime(2025, 11, 3, 14, 5))
    _p(d, "Tamarack Hydro Distribution  |  Asset Management, Protection & Control", size=8.5, italic=True)
    _p(d, "AM-PC-014  Obsolete protection spares: final-buy sizing", bold=True, size=14, after=2)
    _p(d, "Revision 3, issued 3 November 2025. Owner: P&C Asset Planning. Approver: Director, Asset Management.", size=9, after=10)
    sections = [
        ("1. Purpose",
         ["When a manufacturer withdraws a protection relay or one of its replaceable modules, we place one last-time "
          "buy. This procedure sets how that buy is sized so that the relays still in service can be kept running until "
          "the Protection Renewal Programme replaces them."]),
        ("2. Scope",
         ["Replaceable modules of protection relays and controllers that are covered by an end-of-life notice. It does not "
          "cover whole-relay spares, which are held under AM-PC-009."]),
        ("3. Support period",
         ["3.1 A relay is supported from the stock count date until its substation's renewal scheme is commissioned. Use "
          "the approved Protection Renewal Programme current at the stock count date. A relay is counted for every month "
          "up to, but not including, the commissioning month shown for its substation.",
          "3.2 A relay at a substation with no scheme in the programme period is supported to the end of the programme "
          "period (December 2035 in the 2026 programme)."]),
        ("4. Expected failures",
         ["4.1 Module failures are corrective work orders (work type CM or EM) on a relay of the type concerned whose "
          "failed component is the module, with status COMP or CLOSE. Cancelled work orders and logistics work orders "
          "(work type LOG) are not failures.",
          "4.2 Failure rates are set by relay age band: 0 to 9, 10 to 14, 15 to 19, 20 to 24, 25 to 29, and 30 years and "
          "over. A relay's age is its age in completed years on the first day of a month, measured from its installation "
          "date in the asset register; a failure takes the relay's age on the first day of the month it occurred.",
          "4.3 The failure rate for a band is the number of module failures in the work-order history in the band "
          "divided by the relay-years in service in the band. Relay-years are counted in relay-months: a relay "
          "counts for a month if it is in service on the first day of that month.",
          "4.4 Expected failures over the support period are the band rates applied to the relay-months each relay "
          "will spend in each band, from the stock count date to the end of its support."]),
        ("5. Available modules",
         ["Available modules are those serviceable on hand at all stores and depots, plus modules at the manufacturer "
          "for repair that the end-of-life notice says will be returned. Quarantined modules are not available until they "
          "pass bench test and are excluded from the count."]),
        ("6. The buy",
         ["6.1 Module demand over the support period is treated as Poisson with mean equal to the expected failures.",
          "6.2 Buy the smallest whole number of manufacturer lots for which the probability that available modules plus "
          "the buy cover all demand over the support period is at least 95 per cent.",
          "6.3 The sizing goes to the Director, Asset Management for signature with the lot count, the cover it gives, "
          "the expected failures by year and the cost."]),
    ]
    for head, paras in sections:
        _p(d, head, bold=True, size=11, after=3)
        for t in paras:
            _p(d, t, after=5)
    _p(d, "Revision history: rev 1 (2019) issued; rev 2 (2022) EAM work-order source; rev 3 (2025) Poisson cover test "
          "replaces the 20 per cent contingency.", size=8.5, italic=True, after=0)
    d.save(path)


def eol_pdf(path):
    d = _doc("Veldtek Protection Systems", "End-of-life notice EOL-2026-07: VPR-340", dt.datetime(2026, 8, 20, 9, 0), font="Arial")
    _p(d, "Veldtek Protection Systems Inc.  ·  2200 Meadowvale Blvd, Mississauga ON", size=8, italic=True)
    _p(d, "Product end-of-life notice EOL-2026-07", bold=True, size=13, after=2)
    _p(d, "20 August 2026", after=10)
    _p(d, "To: customers operating VPR-340 feeder protection relays", after=8)
    body = [
        "The VPR-340 relay was withdrawn from sale in 2018. Its power supply module, part VPR340-PSU-02, depends on "
        "components that our suppliers have now discontinued, and we will build one final production run.",
        "Last-time-buy orders for VPR340-PSU-02 must reach us by 15 December 2026. Modules are sold in lots of 25 at "
        "CAD 1,965.00 per module (CAD 49,125.00 per lot), delivery by 31 March 2027. No orders are accepted after the "
        "final run.",
        "Repair service for VPR340-PSU-02 ends with this notice. Modules already received at our repair centre under an "
        "open RMA, and modules received by 15 December 2026, will be repaired or replaced and returned. Repair is not "
        "available after that date.",
        "The other replaceable cards of the VPR-340 (processor, input/output and display) remain available until "
        "further notice.",
        "Questions to your Veldtek account manager, or to Veldtek Lifecycle Services through the customer portal.",
    ]
    for t in body:
        _p(d, t, after=6)
    _pdf(d, path, "eol")


def programme_xlsx(path, prog, subs):
    wb = openpyxl.Workbook()
    names = dict(zip(subs["sub_code"], subs["sub_name"]))
    region = dict(zip(subs["sub_code"], subs["region"]))

    def sheet(ws, col, title):
        ws.append([title])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append([])
        hdr = ["Scheme", "Substation code", "Substation", "Region", "Scope", "Commissioning month"]
        ws.append(hdr)
        for j in range(1, len(hdr) + 1):
            ws.cell(row=3, column=j).font = Font(bold=True)
            ws.cell(row=3, column=j).fill = PatternFill("solid", fgColor="E3E9F2")
        live = prog[prog["retired_on"].isna()].copy()
        live["_k"] = [(d or dt.date(2099, 1, 1)) for d in live[col]]
        live = live.sort_values(["_k", "sub_code"], kind="mergesort")
        n = 0
        for _, r in live.iterrows():
            n += 1
            when = r[col].strftime("%b %Y") if r[col] is not None else "Not in programme period"
            bays = int(1 + (zlib.crc32(r["sub_code"].encode()) % 9))
            scope = SCOPES[zlib.crc32((r["sub_code"] + "s").encode()) % len(SCOPES)] % bays
            ws.append(["PRP-%03d" % n if r[col] is not None else "", r["sub_code"], names[r["sub_code"]],
                       region[r["sub_code"]], scope, when])
        for j, w in enumerate([10, 15, 22, 10, 48, 22], 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
        ws.freeze_panes = "A4"

    ws = wb.active
    ws.title = "Approved 2026"
    sheet(ws, "plan_2026", "Protection Renewal Programme 2026-2035, approved by the Board 19 March 2026")
    ws2 = wb.create_sheet("2025 plan (superseded)")
    sheet(ws2, "plan_2025", "Protection Renewal Programme, 2025 planning version (superseded by the approved 2026 programme)")
    ws3 = wb.create_sheet("Notes")
    notes = [
        "Commissioning month is the month the new protection panel is placed in service; the VPR-340 relays at that "
        "substation are removed from service in the same month.",
        "Substations rebuilt under the 2022-2025 station renewals no longer carry VPR-340 relays and are not listed.",
        "Substations marked 'Not in programme period' keep their VPR-340 relays beyond December 2035.",
        "The 2026 programme defers %d schemes and brings %d forward against the 2025 planning version." % (
            sum(1 for a, b in zip(prog["plan_2025"], prog["plan_2026"]) if a and b and b > a),
            sum(1 for a, b in zip(prog["plan_2025"], prog["plan_2026"]) if a and b and b < a)),
    ]
    for i, t in enumerate(notes, 1):
        ws3.cell(row=i, column=1, value=t)
    ws3.column_dimensions["A"].width = 120
    wb.save(path)


def dictionary_txt(path):
    txt = """TAMARACK HYDRO DISTRIBUTION - EAM EXTRACTS, PROTECTION & CONTROL
Extract run 2026-10-01 06:10 by the EAM reporting service (job PC_ASSET_WO_MONTHLY)

The asset management system (EAM) went live on 1 January 2021, replacing the legacy maintenance system.
Assets in service at go-live were loaded from the legacy asset list. Work-order history starts at go-live:
legacy work orders were archived with the old system and were not migrated.

protection_asset_register_2026-09-30.csv
  asset_id           EAM asset number
  model              relay or controller model
  manufacturer       manufacturer name as held in EAM
  function           protection function
  sub_code           substation code (see substations.csv)
  bay                bay or position in the substation
  serial_no          manufacturer serial number
  install_date       date the asset was placed in service (from the legacy asset list for assets loaded at go-live)
  status             IN SERVICE or RETIRED
  retired_date       date the asset was taken out of service (first day of the month for station rebuilds)
  region             operating region recorded on the asset at load (not maintained after go-live)
  Assets retired before go-live are not in EAM.

eam_work_orders_protection_2021-01_2026-09.csv
  wo_number          work-order number
  reported_date      date the work was raised
  completed_date     date the work was completed (blank while open)
  work_type          PM planned maintenance test, CM corrective, EM emergency corrective, INSP inspection,
                     MOD settings or firmware modification, LOG logistics (shipping, returns)
  status             INPRG in progress, COMP completed, CLOSE closed after review, CANC cancelled
  asset_id           EAM asset number (blank for substation-level inspections)
  sub_code           substation code
  region             operating region at the date the work was raised (regions reorganised 1 April 2024)
  failed_component   component recorded by the crew on corrective and logistics work (PSU power supply,
                     CPU processor, IO input/output card, DISP display, COMMS communications card)
  description        crew text
  crew               crew
  labour_hours       hours booked

substations.csv
  sub_code, sub_name, region (operating region from 1 April 2024), legacy_region (before 1 April 2024),
  station_type (TS transformer station, DS distribution station)

spares_stock_2026-09-30.csv
  Stores count at close of business 30 September 2026. stock_state: SERVICEABLE on the shelf, QUARANTINE awaiting
  bench test after return from site, AT REPAIR at the manufacturer under an open RMA.
"""
    open(path, "w").write(txt)
