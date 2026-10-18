#!/usr/bin/env python3
"""task198 golden deliverables and figures.json, computed from the shipped bundle.

Runs verify.py's own bundle pipeline (so nothing here can produce a figure the pack cannot),
then writes golden/ and generator/figures.json.

    python3 task198/generator/make_golden.py
"""
import contextlib
import io
import json
import os
import sys
import zipfile
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GOLD = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

EXPORT_DT = datetime(2026, 5, 8, 16, 30, 0)
FIXED_ZIP_DT = (2026, 5, 8, 16, 30, 0)


def pipeline():
    src = open(os.path.join(HERE, "verify.py")).read().split('print("\\n%d assertions')[0]
    ns = {"__name__": "golden", "__file__": os.path.join(HERE, "verify.py")}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "verify", "exec"), ns)
    return ns


def fix_zip(path, app="Microsoft Excel"):
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    tmp = path + ".tmp"
    drop = {"docProps/thumbnail.jpeg"}
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename in drop:
                continue
            if info.filename == "_rels/.rels":
                data = re.sub(rb"<Relationship[^>]*thumbnail\.jpeg[^>]*/>", b"", data)
            if info.filename in ("docProps/core.xml", "docProps/app.xml"):
                data = re.sub(rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
                              EXPORT_DT.strftime("%Y-%m-%dT%H:%M:%SZ").encode(), data)
                data = re.sub(rb"<Application>[^<]*</Application>",
                              ("<Application>%s</Application>" % app).encode(), data)
                data = re.sub(rb"<dc:description>[^<]*</dc:description>",
                              b"<dc:description></dc:description>", data)
            ni = zipfile.ZipInfo(info.filename, date_time=FIXED_ZIP_DT)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            z.writestr(ni, data)
    os.replace(tmp, path)
    ts = EXPORT_DT.timestamp()
    os.utime(path, (ts, ts))


def main():
    ns = pipeline()
    QN, OBS, cells, cases = ns["QNAME"], ns["OBS"], ns["cells"], ns["cases"]
    CALL, CALL_FIG = ns["CALL"], ns["CALL_FIG"]
    implied, QUEUES = ns["implied"], ns["QUEUES"]
    A1, A2, A3, top10, TRU = ns["A1"], ns["A2"], ns["A3"], ns["top10"], ns["TRU"]
    tru_name = {}
    import re
    for m in re.finditer(r"((?:SC-\d{3}|RMT-000))\n([^\n]+)\n([\d,]+)", ns["tru_txt"]):
        tru_name[m.group(1)] = m.group(2)
    call_cases = sum(1 for c in cases.values() if c["fy"] == 2026 and c["q"] == CALL)
    order = [q for q, _ in sorted(OBS.items(), key=lambda kv: -kv[1])]
    os.makedirs(GOLD, exist_ok=True)

    # ---------------------------------------------------------------- figures.json
    fig = {
        "call": {
            "queue_code": CALL,
            "queue": QN[CALL],
            "fy2026_breach_share_pct": round(CALL_FIG, 1),
            "fy2026_cases_received": call_cases,
            "sentence": "Contribution queries (MS-CQ) takes the one process re-engineering review in "
                        "the first half of 2027; its FY2026 breach share is %.1f per cent on the "
                        "%d cases it received in the year." % (round(CALL_FIG, 1), call_cases),
        },
        "critical_components": {
            "fy2026_window": "1 April 2025 to 31 March 2026",
            "extract_date": "2026-04-30",
            "cases_in_window": sum(1 for c in cases.values() if c["fy"] == 2026),
            "carried_at_cutover_resolved": ns["superseded"],
            "call_quarterly_breach_share_pct": {
                "Q%d" % q: round(cells[(CALL, 2026, q)]["b"], 1) for q in (1, 2, 3, 4)},
            "call_staffed_positions_per_quarter": {
                "Q%d" % q: cells[(CALL, 2026, q)]["pos"] for q in (1, 2, 3, 4)},
            "level_ranking_leader": {"queue": QN[order[0]], "fy2026_breach_share_pct": round(OBS[order[0]], 1)},
            "call_rank_on_level": order.index(CALL) + 1,
        },
        "asks": {
            "ask1_cases_answered_late_fy2026": A1,
            "ask1_call_cases_received_fy2026": call_cases,
            "ask2_chargeable_cases_covered": {"Q%d" % q: A2[q] for q in sorted(A2)},
            "ask3_active_members": {p: A3[p][0] for p, _ in top10},
            "ask3_cases_per_1000": {p: A3[p][1] for p, _ in top10},
        },
        "rivals": {
            "level_leader": {"queue": QN[order[0]], "fy2026_breach_share_pct": round(OBS[order[0]], 1),
                             "fy2026_offered_load": round(cells[(order[0], 2026, 1)]["load"], 1),
                             "rostered_positions": cells[(order[0], 2026, 1)]["pos"]},
            "roster_swing": {"queue": QN[order[1]], "fy2026_breach_share_pct": round(OBS[order[1]], 1),
                             "fy2026_offered_load": round(cells[(order[1], 2026, 1)]["load"], 1),
                             "fy2026_positions": cells[(order[1], 2026, 1)]["pos"],
                             "fy2025_offered_load": round(cells[(order[1], 2025, 1)]["load"], 1),
                             "fy2025_positions": cells[(order[1], 2025, 1)]["pos"]},
            "third": {"queue": QN[order[2]], "fy2026_breach_share_pct": round(OBS[order[2]], 1)},
        },
        "steps": {
            "distinct_cases_in_record": len(cases),
            "cases_held_in_both_extracts": ns["superseded"],
            "cases_received_fy2026": sum(1 for c in cases.values() if c["fy"] == 2026),
            "cases_answered_late_fy2026": A1,
            "chargeable_cases_covered_fy2026": sum(A2.values()),
            "charge_lines_fy2026": len([r for r in ns["crows"] if ns["fqtr"](
                __import__("datetime").date.fromisoformat(r[1]))[0] == 2026]),
            "call_offered_load_fy2026": round(cells[(CALL, 2026, 1)]["load"], 1),
            "call_rostered_positions": cells[(CALL, 2026, 1)]["pos"],
        },
        "stated_in_the_pack": {
            "rate_denominator": 1000,
            "framework_clause_for_the_call": "4.2",
            "standard_clause_receipt": "2.1",
            "standard_clause_clock_starts": "3.1",
            "standard_clause_targets": "3.2",
            "standard_clause_working_day": "3.3",
            "standard_clause_member_days": "3.4",
            "standard_clause_unanswered_at_extract": "3.6",
            "call_target_working_days": ns["TARGET_WD"][CALL],
            "productive_minutes_per_rostered_day": ns["PROD_MIN"],
            "net_productive_factor": ns["NET_FACTOR"],
            "rostered_hours_per_position_per_day": 7.0,
        },
        "deliverables": {
            "fy2026_service_level_replay.xlsx": "quarterly service level by queue, the scheme charging "
                                                "quarters and the ten largest participating schemes",
            "queue_review_recommendation.docx": "the review candidate, its FY2026 breach share and its "
                                                "cases received",
            "queue_breach_shares_fy2026.png": "one bar per queue, FY2026 breach share",
        },
    }
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=2)
        fh.write("\n")

    # ---------------------------------------------------------------- workbook
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    wb.remove(wb.active)

    ws = wb.create_sheet("FY2026 by quarter")
    ws.append(["Member service level, cases received FY2026 (1 Apr 2025 to 31 Mar 2026)"])
    ws.append(["Case record extracted 30 Apr 2026. Clock per Member Service Standard issue 6, cl 3."])
    ws.append([])
    ws.append(["Queue", "Code", "Target (wd)", "Q1 received", "Q1 late", "Q2 received", "Q2 late",
               "Q3 received", "Q3 late", "Q4 received", "Q4 late", "FY2026 received",
               "FY2026 late", "FY2026 breach share %"])
    for q in order:
        row = [QN[q], q, ns["TARGET_WD"][q]]
        tot_n = tot_l = 0
        for k in (1, 2, 3, 4):
            c = cells[(q, 2026, k)]
            row += [c["n"], c["late"]]
            tot_n += c["n"]
            tot_l += c["late"]
        row += [tot_n, tot_l, round(100.0 * tot_l / tot_n, 1)]
        ws.append(row)
    ws.append([])
    tot_n = sum(cells[(q, 2026, k)]["n"] for q in QUEUES for k in (1, 2, 3, 4))
    ws.append(["Operation", "", "", "", "", "", "", "", "", "", "", tot_n, A1,
               round(100.0 * A1 / tot_n, 1)])
    ws["A1"].font = Font(bold=True)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.create_sheet("Candidate")
    ws.append(["Process re-engineering review candidate, H1 2027"])
    ws.append(["Selected under Service Assurance Framework issue 3, clause 4.2"])
    ws.append([])
    ws.append(["Queue", QN[CALL]])
    ws.append(["Queue code", CALL])
    ws.append(["FY2026 breach share %", round(CALL_FIG, 1)])
    ws.append(["FY2026 cases received", call_cases])
    ws.append(["Rank on FY2026 breach share", "%d of 9" % (order.index(CALL) + 1)])
    ws.append([])
    ws.append(["Quarter", "Cases received", "Answered late", "Breach share %", "Offered load",
               "Staffed positions"])
    for k in (1, 2, 3, 4):
        c = cells[(CALL, 2026, k)]
        ws.append(["FY2026 Q%d" % k, c["n"], c["late"], round(c["b"], 1), round(c["load"], 2), c["pos"]])
    ws.append([])
    ws.append(["Comparison, cl 4.2", "the same queue's FY2023 to FY2025 quarters at the same offered load"])
    ws.append(["Share those quarters reached %", round(implied(CALL, "load"), 1)])
    ws.append(["Standing above that, points", round(CALL_FIG - implied(CALL, "load"), 1)])
    ws["A1"].font = Font(bold=True)

    ws = wb.create_sheet("Scheme charging")
    ws.append(["Chargeable cases covered by the FY2026 scheme charges"])
    ws.append(["Recovered from each charge line at the Fee Schedule 2025-26 per case rate"])
    ws.append([])
    ws.append(["Financial quarter", "Chargeable cases covered"])
    for k in sorted(A2):
        ws.append(["FY2026 Q%d" % k, A2[k]])
    ws.append(["FY2026", sum(A2.values())])
    ws["A1"].font = Font(bold=True)

    ws = wb.create_sheet("Schemes")
    ws.append(["Ten largest participating schemes by FY2026 cases received"])
    ws.append(["Active members at 31 Mar 2026 per the trustee membership statement"])
    ws.append([])
    ws.append(["Scheme code", "Scheme", "FY2026 cases received", "Active members",
               "Cases per 1,000 active members"])
    for p, n in top10:
        ws.append([p, tru_name.get(p, p), n, A3[p][0], A3[p][1]])
    ws["A1"].font = Font(bold=True)

    ws = wb.create_sheet("Basis")
    for r in [["Basis of this workbook"], [],
              ["Window", "cases received 1 Apr 2025 to 31 Mar 2026 (FY2026)"],
              ["Population", "every case received in the window, including those unanswered at the extract"],
              ["Clock", "working days from the day after receipt, less days awaiting member information"],
              ["Working days", "weekends and Irish public holidays excluded"],
              ["Unanswered at extract", "late where the clock has already passed target, within target otherwise"],
              ["Case record", "Gemini and Orbit extracts, cases carried at the 1 Apr 2024 cutover counted once"],
              ["Orbit times", "converted from UTC to Irish local time before the receipt day is taken"],
              ["Offered load", "cases x standard minutes / (420 x 0.88 x working days), in positions"],
              ["Positions", "rostered FTE per quarter; FY2023 and FY2024 hours at 7.0 hours a position a day"],
              ["Charges", "cases covered = line charge / per case rate for the rate period"],
              ["Membership", "trustee statement per scheme; the register carries grouped sponsor returns"]]:
        ws.append(r)
    ws["A1"].font = Font(bold=True)

    # workbook affordances: frozen headers, widths to content, formats per column
    from openpyxl.utils import get_column_letter
    freeze = {"FY2026 by quarter": "A5", "Candidate": "A4", "Scheme charging": "A5",
              "Schemes": "A5", "Basis": "A2"}
    for wsx in wb.worksheets:
        if wsx.title in freeze:
            wsx.freeze_panes = freeze[wsx.title]
        widths = {}
        for row in wsx.iter_rows():
            for c in row:
                if c.value is not None:
                    widths[c.column] = min(46, max(widths.get(c.column, 9), len(str(c.value)) + 2))
        for col, w in widths.items():
            wsx.column_dimensions[get_column_letter(col)].width = w
        for row in wsx.iter_rows():
            for c in row:
                if isinstance(c.value, int) and abs(c.value) >= 1000:
                    c.number_format = "#,##0"
                elif isinstance(c.value, float):
                    c.number_format = "0.0"
    ws = wb["FY2026 by quarter"]
    for row in ws.iter_rows(min_row=5, min_col=14, max_col=14):
        for c in row:
            c.number_format = "0.0"
    ws.print_area = "A1:N16"
    ws.print_title_rows = "4:4"
    p = os.path.join(GOLD, "fy2026_service_level_replay.xlsx")
    pr = wb.properties
    pr.creator = "Member Operations"
    pr.lastModifiedBy = "Member Operations"
    pr.created = EXPORT_DT
    pr.modified = EXPORT_DT
    pr.title = "FY2026 service level replay"
    wb.save(p)
    fix_zip(p)

    # ---------------------------------------------------------------- chart
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    SURFACE, GRID, AXIS, INK, INK2 = "#fcfcfb", "#e1e0d9", "#898781", "#0b0b0b", "#52514e"
    BLUE, ORANGE = "#2a78d6", "#eb6834"      # validated with the dataviz palette validator
    labels = [QN[q] for q in order]
    obsv = [OBS[q] for q in order]
    impv = [implied(q, "load") for q in order]
    fig2, ax = plt.subplots(figsize=(9.8, 5.1), dpi=130)
    fig2.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    x = list(range(len(order)))
    cols = [ORANGE if q == CALL else BLUE for q in order]
    ax.bar(x, obsv, color=cols, width=0.6, zorder=3)
    ax.scatter(x, impv, marker="_", s=460, linewidths=1.8, color=INK2, zorder=4,
               label="share the queue's own FY2023 to FY2025 quarters at the same offered load reached")
    ax.bar(0, 0, color=BLUE, label="FY2026 breach share")
    ax.bar(0, 0, color=ORANGE, label="FY2026 breach share, review candidate")
    # selective direct labels: the candidate and the queues above it
    for i, q in enumerate(order):
        if i <= order.index(CALL):
            top = max(obsv[i], impv[i])
            ax.annotate("%.1f" % obsv[i], (i, top), textcoords="offset points", xytext=(0, 7),
                        ha="center", fontsize=8.6, color=INK)
    ax.set_ylabel("per cent of cases received answered later than target", fontsize=9, color=INK2)
    ax.set_title("Contribution queries answers 12.4 per cent of cases late where its own load and "
                 "roster have always produced 2.2",
                 fontsize=11, loc="left", color=INK, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=26, ha="right", fontsize=8.6, color=INK2)
    ax.tick_params(axis="y", labelsize=8.6, colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.set_ylim(0, max(obsv) * 1.22)
    ax.legend(loc="upper right", fontsize=8.2, frameon=False, labelcolor=INK2,
          bbox_to_anchor=(1.0, 1.02))
    ax.annotate("review candidate", (order.index(CALL), OBS[CALL]), textcoords="offset points",
                xytext=(26, 30), fontsize=8.6, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.9))
    fig2.text(0.012, 0.012, "Cases received 1 April 2025 to 31 March 2026. Member operations, "
              "Gemini and Orbit case extracts pulled 30 April 2026.", fontsize=7.4, color=AXIS)
    fig2.tight_layout(rect=(0, 0.03, 1, 1))
    png = os.path.join(GOLD, "queue_breach_shares_fy2026.png")
    fig2.savefig(png, facecolor=SURFACE, metadata={"Software": None, "Creation Time": None})
    plt.close(fig2)
    ts = EXPORT_DT.timestamp()
    os.utime(png, (ts, ts))

    # ---------------------------------------------------------------- memo
    import docx
    from docx.shared import Inches, Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_paragraph("Member Operations").bold = True
    h = d.add_paragraph()
    r = h.add_run("Contribution queries takes the first-half 2027 process re-engineering review")
    r.bold = True
    r.font.size = Pt(13)
    d.add_paragraph("For the service improvement response to the Pensions Authority "
                    "(SUP/2026/0418). 8 May 2026.")
    d.add_paragraph(
        "The review goes to %s. Its FY2026 breach share is %.1f per cent, on the %s cases it "
        "received between 1 April 2025 and 31 March 2026." % (QN[CALL], round(CALL_FIG, 1),
                                                              "{:,}".format(call_cases)))
    d.add_paragraph(
        "Clause 4.2 of the assurance framework picks the queue standing furthest above the share "
        "the same queue reached in those of its FY2023 to FY2025 quarters that carried the same "
        "offered load. %s carried 15.0 positions-equivalents of work against 16 rostered positions "
        "in each quarter of FY2026, against 14.7 to 15.0 on the same 16 positions in every quarter "
        "since FY2023, and its own "
        "quarters at that load answered %.1f per cent of cases late. It is now at %.1f per cent. "
        "Nothing in its workload or its roster changed." % (QN[CALL], implied(CALL, "load"),
                                                            round(CALL_FIG, 1)))
    d.add_paragraph(
        "Three queues answer a larger share late and none of them is the candidate. %s, at %.1f per "
        "cent, is below the %.1f per cent its own quarters at the same offered load reached. %s, at "
        "%.1f per cent, stands %.1f points above its own %.1f per cent, and %s, at %.1f per cent, "
        "%.1f points above its own %.1f per cent, against %.1f points for the candidate."
        % (QN[order[0]], round(OBS[order[0]], 1), round(implied(order[0], "load"), 1),
           QN[order[1]], round(OBS[order[1]], 1), round(OBS[order[1]] - implied(order[1], "load"), 1),
           round(implied(order[1], "load"), 1),
           QN[order[2]], round(OBS[order[2]], 1), round(OBS[order[2]] - implied(order[2], "load"), 1),
           round(implied(order[2], "load"), 1), round(CALL_FIG - implied(CALL, "load"), 1)))
    d.add_paragraph(
        "%s is the one to watch in that list. It ran five positions in FY2026 and in FY2023, and "
        "fourteen through FY2024 and FY2025, when the member data remediation programme carried nine "
        "temporary posts and close to three times the caseload. Its FY2026 quarters carried 4.7 "
        "positions-equivalents, which is what its FY2023 quarters carried on the same five positions, "
        "and those quarters answered between 17.9 and 27.8 per cent of cases late."
        % QN[order[1]])
    d.add_paragraph(
        "Recommendation: commission the H1 2027 review on %s. The workbook carries the quarterly "
        "position for all nine queues, the scheme charging reconciliation and the ten largest "
        "participating schemes by case load." % QN[CALL])
    note = d.add_paragraph(
        "Sources: Gemini and Orbit case extracts pulled 30 April 2026; rostered capacity record "
        "refreshed 17 April 2026; Work Measurement Standard 2022; Member Service Standard issue 6. "
        "Shares are of cases received in the year, not of cases closed in it, so they will not tie "
        "to the quarterly performance export, which reports on cases closed.")
    note.runs[0].font.size = Pt(8.5)
    p = os.path.join(GOLD, "queue_review_recommendation.docx")
    cp = d.core_properties
    cp.author = "Member Operations"
    cp.last_modified_by = "Member Operations"
    cp.created = EXPORT_DT
    cp.modified = EXPORT_DT
    cp.revision = 1
    cp.title = "Contribution queries takes the H1 2027 process review"
    cp.comments = ""
    cp.category = "Service improvement response"
    d.save(p)
    fix_zip(p, app="Microsoft Office Word")

    print("golden/ written:")
    for f in sorted(os.listdir(GOLD)):
        print("   %8d  %s" % (os.path.getsize(os.path.join(GOLD, f)), f))
    print("generator/figures.json written")


if __name__ == "__main__":
    main()
