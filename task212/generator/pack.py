"""task212 documents, plans, distractors, goldens, metadata and the zip (called from build.py)."""
import json
import os
import datetime as dt
import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
import docs
import world

V_TARGET = 161600   # Ribarroja's planned parcels a week over peak weeks 48 to 52 (checks.py asserts the bin)
# CS-FIN 07, section 2: a flat-rate case's grain and its approval basis (checks.py and verify.py read it back)
FLAT_RATE_CASE = ("A business account on flat-rate terms opens one case for all the damaged cartons of a consignment, "
                  "under the tracking number of its first carton, and Customer Service approves it at the account's "
                  "rate for each damaged carton.")


def _tbl(rows, widths, head=True, size=8.2):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", size), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (-1, -1), 2.5)]
    if head:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8"))]
    t.setStyle(TableStyle(st))
    return t


def programme(path):
    body, h, t, small = docs.styles()

    def story():
        s = [Paragraph("Sortation engineering survey programme, peak 2026", t),
             Paragraph("Brújula Paquetería, Network Operations. Issued 14 October 2026 by Julieta Barranco, head of hub "
                       "engineering. Applies to the six sortation hubs.", small), Spacer(1, 5)]
        s += [Paragraph("1. The survey", h),
              Paragraph("Each year before the peak, hub engineering and the sorter maker's field technician survey the "
                        "sortation equipment of one hub: induction, merges, transfers, the sorter and its chutes. The team "
                        "inspects, adjusts and repairs over three sorting nights, standing the sorter down for parts of "
                        "each night. One survey slot is available before the 2026 peak, in the three weeks from 2 to 20 "
                        "November 2026.", body),
              Paragraph("2. Which hub", h),
              Paragraph("The survey goes to the hub whose own sortation equipment damaged the most parcels per 10,000 "
                        "parcels inspected in the routine audits of its regional outbound cages built on the sorting "
                        "nights of 1 July to 30 September 2026, measured against the damage the same parcels would suffer "
                        "across the network's six hubs.", body),
              Paragraph("Where the damage the same parcels would suffer can be estimated more than one way, the estimate "
                        "with the lowest Bayesian information criterion (BIC) on the quarter's routine audits stands.",
                        body),
              Paragraph("Parcels inspected and damaged parcels are as the outbound cage audit procedure records them: a "
                        "parcel found in the cage at a routine audit is inspected, and a parcel the auditor records as "
                        "damaged under any damage code is damaged. A cage belongs to the sorting night printed on its "
                        "label.", body),
              Paragraph("3. What the survey is worth", h),
              Paragraph("The repairs stop the damage the hub's own sortation equipment does. A survey's worth is the "
                        "damaged parcels a week its repairs stop over the peak: the hub's own equipment damage per "
                        "10,000 parcels inspected, applied to the parcels the 2026 peak plan has the hub sorting a week, "
                        "averaged over peak weeks 48 to 52.", body),
              Paragraph("4. Timetable", h),
              _tbl([["Step", "Date"], ["Quarter's audits closed", "9 October 2026"],
                    ["Hub chosen and maker's technician booked", "30 October 2026"],
                    ["Survey nights", "2 to 20 November 2026"], ["Peak weeks", "48 to 52 (23 November to 27 December)"]],
                   [90 * mm, 70 * mm]),
              Spacer(1, 6),
              Paragraph("The 2025 survey went to Basauri. Its report is filed with this programme.", small)]
        return s
    docs.pdf(path, "Sortation engineering survey programme, peak 2026", "Julieta Barranco", docs.stamp(2026, 10, 14), story)


def procedure(path):
    body, h, t, small = docs.styles()

    def story():
        s = [Paragraph("Outbound cage audit procedure, version 4", t),
             Paragraph("Quality, Brújula Paquetería. Version 4 from 1 August 2026 (damage code list renewed). "
                       "Owner: María Vélez, network quality lead.", small), Spacer(1, 5)]
        s += [Paragraph("1. Routine audits", h),
              Paragraph("Each morning the quality team at the delivery depots audits regional outbound cages that "
                        "arrived from the hub overnight, about ten cages per hub for each sorting night. The auditor "
                        "empties the cage on the bench, scans each parcel against the cage's load list and records its "
                        "condition: OK, DAMAGED with a damage code, or NOT FOUND for a parcel on the load list that is "
                        "not in the cage. A parcel recorded NOT FOUND has not been inspected.", body),
              Paragraph("The load list is the cage's LOAD scans in the hub's cage build log. The cage label prints the "
                        "hub number, the sorting night and a serial; the audit records the sorting night from the label "
                        "as the build date.", body),
              Paragraph("2. Check audits", h),
              Paragraph("A supervisor re-audits about one cage in twenty-five to check the auditor's work. A check "
                        "audit does not replace the routine audit, and its lines are not counted as inspections.", body),
              Paragraph("3. Damage codes", h),
              Paragraph("Any damage code records a damaged parcel. The list was renewed on 1 August 2026; handhelds "
                        "keep the list they were loaded with until depot IT reloads them.", body)]
        rows = [["Damage", "Code from 1 August 2026", "Code until 31 July 2026"],
                ["Crushed or deformed", "AP", "D1"], ["Torn", "RO", "D2"], ["Wet or stained", "HU", "D3"],
                ["Open or seal broken", "AB", "D4"], ["Punctured", "PE", "D5"]]
        s += [_tbl(rows, [55 * mm, 45 * mm, 45 * mm])]
        return s
    docs.pdf(path, "Outbound cage audit procedure v4", "Maria Velez", docs.stamp(2026, 7, 24), story)


def claims_note(path):
    body, h, t, small = docs.styles()

    def story():
        s = [Paragraph("Damage claims: quarterly reporting by hub", t),
             Paragraph("Customer Service and Finance, Brújula Paquetería. Note CS-FIN 07, issued 2 July 2026.", small),
             Spacer(1, 5)]
        s += [Paragraph("1. Which hub a claim belongs to", h),
              Paragraph("A damaged parcel is charged to the hub that sorted it on the night it was collected, the "
                        "first hub sort in the parcel's tracking history, and belongs to the quarter of that sorting "
                        "night. Sorting nights are dated by the evening they start, in Spanish time.", body),
              Paragraph("2. What counts", h),
              Paragraph("A damaged parcel counts once, however many cases are opened on it. %s A parcel's claim "
                        "counts as approved when Customer Service first approves a case on it. For the quarter's "
                        "report, claims approved and money paid up to and including 20 October count." % FLAT_RATE_CASE,
                        body),
              Paragraph("3. The money", h),
              Paragraph("The cost of a claim is the money paid to the claimant: by bank transfer in the weekly payment "
                        "run for business accounts, and as a refund to the card the sender paid with for private "
                        "senders, made through the card gateway. A transfer the payee's bank returns is not paid until "
                        "it is made again. Amounts are in euros.", body)]
        return s
    docs.pdf(path, "Damage claims: quarterly reporting by hub", "Finance", docs.stamp(2026, 7, 2), story)


def stoppage_standard(path):
    body, h, t, small = docs.styles()

    def story():
        s = [Paragraph("Sorter stoppage reporting standard", t),
             Paragraph("Network Engineering, Brújula Paquetería. Standard ENG-11, revision 2, from 1 January 2026. "
                       "Owner: Marcelo Castrillo, network maintenance manager.", small), Spacer(1, 5)]
        s += [Paragraph("1. A stoppage", h),
              Paragraph("A sorter stoppage is a spell in which the hub's sorter stands still during a sorting night, "
                        "from the moment it stops to the moment it runs again, whichever record shows it. Each spell "
                        "counts once.", body),
              Paragraph("2. The sorting night", h),
              Paragraph("A sorting night runs from 20:30 to 05:00 Spanish time and is dated by the evening it starts. "
                        "A quarter's stoppages are those of its sorting nights.", body),
              Paragraph("3. Hours stood", h),
              Paragraph("Hours stood are the lengths of a quarter's stoppages added together, in hours.", body)]
        return s
    docs.pdf(path, "Sorter stoppage reporting standard ENG-11", "Marcelo Castrillo", docs.stamp(2025, 12, 19), story)


def report_2025(path):
    body, h, t, small = docs.styles()

    def story():
        s = [Paragraph("Sortation engineering survey 2025: Basauri", t),
             Paragraph("Hub engineering, Brújula Paquetería. Survey nights 3 to 6 and 10 to 12 November 2025. Report "
                       "dated 21 April 2026.", small), Spacer(1, 5)]
        s += [Paragraph("Findings", h),
              Paragraph("The transfer plate between merge 2 and the sorter loop was worn at its leading edge and stood "
                        "4 mm proud of the trays; boxes crossing it at speed took a knock on the lower corner. Two chute "
                        "gates at chutes 31 and 32 closed late. Smaller items: one induction belt slipping, a scanner "
                        "window needing cleaning.", body),
              Paragraph("Work done", h),
              Paragraph("Transfer plate replaced and set flush; chute gates 31 and 32 re-timed; induction belt 2 "
                        "re-tensioned; scanner arch cleaned and recalibrated by the maker's technician.", body),
              Paragraph("Audited damage at Basauri before and after", h),
              _tbl([["Basauri routine audits", "Parcels inspected", "Damaged", "Per 10,000"],
                    ["July to September 2025", "24,112", "391", "162.2"],
                    ["January to March 2026", "23,604", "288", "122.0"]], [55 * mm, 35 * mm, 30 * mm, 30 * mm]),
              Spacer(1, 5),
              Paragraph("The fall in audited damage came within a fortnight of the work and held through the first "
                        "quarter. Basauri was chosen on the July to September 2025 audits under the 2025 programme.",
                        body)]
        return s
    docs.pdf(path, "Sortation engineering survey 2025: Basauri", "Julieta Barranco", docs.stamp(2026, 4, 21), story)


def plan_xlsx(path):
    p = docs.peak_plan(V_TARGET)
    wide = p.pivot_table(index=["iso_week", "basis"], columns="hub", values="parcels").reset_index()
    names = {h[0]: h[2] for h in docs.HUB_ROWS}
    wide = wide.rename(columns=names)[["iso_week", "basis"] + [names[h] for h in world.HUB_KEYS]]
    docs.sheet_xlsx(path, [("Weekly parcels", wide)], "Planificacion", "2026-10-09T11:20:00Z", "Peak plan 2026",
                    widths={"iso_week": 9, "basis": 8}, numfmt={names[h]: "#,##0" for h in world.HUB_KEYS})
    return p


def visits_xlsx(path, seed):
    r = np.random.default_rng(seed + 61)
    rows = []
    notes = ["routine inspection, no findings", "chain lubricated, tray pins checked", "belt tension checked",
             "scanner arch cleaned", "tilt coils tested", "chute gate timing checked", "drive gearbox oil sampled",
             "safety circuit tested", "induction photocells aligned", "software patch installed"]
    for h in world.HUB_KEYS:
        for m in range(1, 11):
            d = dt.date(2026, m, 1) + dt.timedelta(days=int(r.integers(2, 25)))
            while d.weekday() > 4:
                d += dt.timedelta(days=1)
            rows.append((d.isoformat(), docs.HUB_ROWS[world.HUB_KEYS.index(h)][2], "preventive",
                         float(r.choice([4.0, 4.5, 5.0, 6.0, 7.5, 8.0])), str(r.choice(notes))))
    v = pd.DataFrame(rows, columns=["visit_date", "hub", "visit_type", "technician_hours", "notes"]).sort_values(
        ["visit_date", "hub"]).reset_index(drop=True)
    docs.sheet_xlsx(path, [("Visits", v)], "Field Service", "2026-10-20T08:00:00Z", "Service visits 2026",
                    widths={"notes": 40, "hub": 16})
    return v


def metadata(FILES, DELIVERABLES, task):
    src = "Synthetic, generated by task212/generator for this task (no real dataset); licence CC0"
    desc = {
        "findings": "audit app findings: one line per parcel in each audited outbound cage, July to September 2026 sorting nights",
        "headers": "audit app headers: routine and check audits of outbound cages",
        "build_log": "hub sorter control systems' cage build log for the audited cages (UTC)",
        "dws": "dimension and weight scanners at hub induction, audited parcels (local time with offset)",
        "manifest": "shipment lines as senders' integrations sent them, audited parcels",
        "accounts": "commercial team's accounts register",
        "hubs": "network operations hub register",
        "plan": "operations planning: weekly parcels sorted, quarter actuals and peak plan 2026",
        "programme": "Network Operations survey programme, peak 2026",
        "procedure": "Quality's outbound cage audit procedure, version 4",
        "report2025": "hub engineering report on the 2025 survey at Basauri",
        "cases": "customer service case export of damage claims, pulled 23 October 2026",
        "transfers": "treasury's weekly claims transfer runs, 2026",
        "refunds": "card gateway settlement report of refunds, 1 July to 22 October 2026 (UTC)",
        "tracking": "tracking history of every parcel with a damage case (UTC)",
        "terms": "commercial team's list of business accounts on flat-rate damage terms",
        "claims_note": "Customer Service and Finance note on quarterly claims reporting",
        "events": "sorter historian event log, sorting nights of the quarter (UTC)",
        "orders": "maintenance management system: sorter work orders",
        "standard": "Network Engineering sorter stoppage reporting standard",
        "visits": "sorter maker's field service visit log, 2026",
    }
    return {
        "task": task,
        "decision": "which hub gets the one sortation engineering survey slot before the 2026 peak, and the damaged "
                    "parcels a week its repairs stop over peak weeks 48 to 52",
        "deliverables": list(DELIVERABLES.values()),
        "distractor_files": ["target/" + FILES["report2025"], "target/" + FILES["visits"]],
        "stated_inputs": ["10,000"],
        "files": {("target/" + FILES[k]): {"description": v, "source": src, "date": "2026-10-27", "licence": "CC0-1.0"}
                  for k, v in desc.items()},
        "organisation": "Brujula Paqueteria (invented); the six hub towns are real places",
        "setting_date": "2026-10-29",
    }


def finish(S, acc, FILES, DELIVERABLES, TGT, GLD, TASK, HERE, PACK_MTIME, GOLD_MTIME):
    p = lambda k: os.path.join(TGT, FILES[k])
    programme(p("programme"))
    procedure(p("procedure"))
    claims_note(p("claims_note"))
    stoppage_standard(p("standard"))
    report_2025(p("report2025"))
    plan_xlsx(p("plan"))
    visits_xlsx(p("visits"), world.SEED)
    import golden
    F = golden.compute(S)
    golden.workbook(os.path.join(GLD, DELIVERABLES["workbook"]), F)
    golden.note(os.path.join(GLD, DELIVERABLES["note"]), F)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump({k: v for k, v in F.items() if not k.startswith("_")}, f, indent=1, sort_keys=True)
    import writeup
    writeup.main()
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(FILES, DELIVERABLES, os.path.basename(TASK)), f, indent=1)
    for d, mt in ((TGT, PACK_MTIME), (GLD, GOLD_MTIME)):
        for fn in sorted(os.listdir(d)):
            os.utime(os.path.join(d, fn), (mt, mt))
    cut_zip(TGT, TASK, PACK_MTIME)


def cut_zip(TGT, TASK, mtime):
    import zipfile
    out = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(TGT)):
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 27, 9, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TGT, fn), "rb").read())
    os.utime(out, (mtime, mtime))
