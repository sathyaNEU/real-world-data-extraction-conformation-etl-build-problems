"""task269's golden deliverables and their figures: osce2027_station_plan.xlsx (the number of stations with the
reliability at every number from 12 to 18, the case bank's eligible cases by blueprint domain, the eligible
examiners by site and session) and osce2027_reliability_chart.png; generator/figures.json and metadata.json."""
import json
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A
import common as K
import postprocess as PP
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = {s[0]: s[1] for s in K.SITES27}
SESS_NAME = dict(K.SESSIONS)


def figures(w):
    y = W.station_marks(w["marks"])
    L = A.ladder(y, w["seed"])
    g = L["golden"]
    v = L["v"]
    tot = sum(v[k] for k in ("p", "s", "ps", "rs", "e"))
    a = W.bank_truth(w["bank"])
    b = W.examiners_truth(w["examiners"])
    fig = {
        "call": {"stations": g["stations"], "below": g["stations"] - 1,
                 "reliability_committed": "%.3f" % g["at"][g["stations"]],
                 "reliability_below": "%.3f" % g["at"][g["stations"] - 1], "unrounded_need": round(g["need"], 3)},
        "reliability": {str(n): "%.3f" % g["at"][n] for n in K.SETTINGS},
        "components": {k: round(float(v[k]), 3) for k in ("p", "s", "ps", "rs", "e")},
        "shares": {k: round(100 * float(v[k]) / tot, 1) for k in ("p", "s", "ps", "rs", "e")},
        "total_variance": round(float(tot), 3),
        "ladder": {
            "R0_alpha12": "%.3f" % L["R0"]["alpha12"], "R0_stations": int(np.ceil(L["R0"]["need"])),
            "R1_alpha_lead12": "%.3f" % L["R1"]["alpha_lead"], "R1_alpha_second12": "%.3f" % L["R1"]["alpha_second"],
            "R1_crossed12": "%.3f" % L["R1"]["g_crossed12"],
            "R1_stations": int(np.ceil(max(L["R1"]["need_lead"], L["R1"]["need_second"], L["R1"]["need_crossed"]))),
            "R2_alpha12": "%.3f" % L["R2"]["alpha"], "R2_half_stations": int(np.ceil(L["R2"]["half"])),
            "R3_stations": int(np.ceil(L["R3"]["need"])),
        },
        "ask_a": {d: list(a[d]) for d in K.DOMAINS},
        "ask_b": {"%s %s" % k: int(n) for k, n in b.items()},
        "candidates_2026": int(y.shape[0]),
        "standard": "%.2f" % K.STANDARD, "rooms": K.ROOMS27,
        "results_2026": {"passed": w["pass"][0], "not_passed": w["pass"][1]},
    }
    return fig


def write_workbook(path, fig):
    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="B4BDC3")
    head = PatternFill("solid", fgColor="DCE6F0")
    mark = PatternFill("solid", fgColor="E3EFE6")
    bold = Font(bold=True)
    note = Font(italic=True, size=9, color="4A4F54")
    n_call = fig["call"]["stations"]

    def header(ws, row, wrap=False):
        for c in ws[row]:
            if c.value is not None:
                c.font = bold
                c.fill = head
                c.border = Border(bottom=thin)
                c.alignment = Alignment(wrap_text=wrap, vertical="top")

    def notes(ws, row, lines):
        for k, t in enumerate(lines):
            c = ws.cell(row + k, 1, t)
            c.font = note
            c.alignment = Alignment(wrap_text=False)

    # the number, and the reliability it rests on
    ws = wb.active
    ws.title = "Stations"
    ws["A1"] = "Final OSCE 2027: %d stations" % n_call
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("The fewest stations at which the total mark ranks candidates with a reliability of at least "
                "%s (policy 4.3), with one examiner a station in each of the three circuits." % fig["standard"])
    ws["A4"], ws["B4"] = "Stations to set", n_call
    ws["A5"], ws["B5"] = "Rooms a site", fig["rooms"]
    for r in (4, 5):
        ws.cell(r, 1).font = bold
        ws.cell(r, 2).alignment = Alignment(horizontal="right")
    ws["B4"].fill = mark
    ws.append([])
    ws.append(["Stations", "Reliability of the total mark", "Meets %s" % fig["standard"]])
    top = ws.max_row
    header(ws, top)
    for n in K.SETTINGS:
        r = fig["reliability"][str(n)]
        ws.append([n, float(r), "Yes" if n >= n_call else "No"])
        ws.cell(ws.max_row, 2).number_format = "0.000"
        ws.cell(ws.max_row, 3).alignment = Alignment(horizontal="center")
        if n == n_call:
            for c in ws[ws.max_row]:
                c.fill = mark
    notes(ws, ws.max_row + 2, [
        "Reliability: the share of the variance among candidates' total marks that reflects differences in their "
        "clinical performance (policy 4.3), for a total over that many stations, each candidate marked by one "
        "examiner a station.",
        "From the variance components of the 2026 sitting's marks (Sources of variance): candidates / (candidates + "
        "(candidate by station + examiner within station + residual) / stations).",
        "Rounded to three decimals; the standard is met on the unrounded value."])
    ws.freeze_panes = ws.cell(top + 1, 1)
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 27
    ws.column_dimensions["C"].width = 12

    # the components the 2027 reliability is built from
    ws2 = wb.create_sheet("Sources of variance")
    ws2["A1"] = "Final OSCE May 2026: where the variance in one examiner's station mark comes from"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2["A2"] = ("84 candidates, 12 stations, the same two examiners at each station on both days; marks out of 20 "
                 "(policy 3.2), station 7's item 14 withdrawn (board of examiners, 14 May 2026, item 2).")
    ws2.append([])
    ws2.append(["Source", "Variance (marks out of 20, squared)", "Share (%)", "Error in 2027"])
    top2 = ws2.max_row
    header(ws2, top2)
    labels = [("p", "Candidates", "No: what the total mark measures"),
              ("s", "Stations (difficulty)", "No: every circuit runs the same stations"),
              ("ps", "Candidate by station", "Yes"),
              ("rs", "Examiner within station (stringency)", "Yes: candidates at a station meet different examiners"),
              ("e", "Residual", "Yes")]
    for k, lab, err in labels:
        ws2.append([lab, fig["components"][k], fig["shares"][k], err])
        ws2.cell(ws2.max_row, 2).number_format = "0.000"
        ws2.cell(ws2.max_row, 3).number_format = "0.0"
    ws2.append(["Total", fig["total_variance"], 100.0, None])
    ws2.cell(ws2.max_row, 2).number_format = "0.000"
    ws2.cell(ws2.max_row, 3).number_format = "0.0"
    for c in ws2[ws2.max_row]:
        c.font = bold
        c.border = Border(top=thin)
    notes(ws2, ws2.max_row + 2, [
        "Estimated by expected mean squares on the balanced design (candidates crossed with examiners nested in "
        "stations); every component positive.",
        "In 2026 an examiner's stringency moved every candidate at the station alike, so it did not enter the "
        "ranking; in 2027 it does."])
    ws2.freeze_panes = ws2.cell(top2 + 1, 1)
    ws2.column_dimensions["A"].width = 38
    ws2.column_dimensions["B"].width = 33
    ws2.column_dimensions["C"].width = 10
    ws2.column_dimensions["D"].width = 52

    # policy 4.4 against the bank
    ws3 = wb.create_sheet("Case bank")
    ws3["A1"] = "Cases that can be set at the May 2027 final OSCE (policy 4.4)"
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.append([])
    ws3.append(["Blueprint domain", "Cases that can be set", "Of which need a simulated patient"])
    top3 = ws3.max_row
    header(ws3, top3)
    for d in K.DOMAINS:
        ws3.append([d] + fig["ask_a"][d])
    ws3.append(["All domains", sum(fig["ask_a"][d][0] for d in K.DOMAINS), sum(fig["ask_a"][d][1] for d in K.DOMAINS)])
    for c in ws3[ws3.max_row]:
        c.font = bold
        c.border = Border(top=thin)
    notes(ws3, ws3.max_row + 2, [
        "Active (edits pending included), reviewed by the OSCE assessment group on or after 11 May 2024, and not "
        "set at a final OSCE sitting, main or supplemental, in 2025 or 2026.",
        "A case re-created under a new code at the November 2025 cut-over keeps the sittings of its retired record "
        "(cut-over report, section 2).",
        "Need a simulated patient: resources SP, or SP and task trainer. Case bank export of 30 November 2026."])
    ws3.freeze_panes = ws3.cell(top3 + 1, 1)
    ws3.column_dimensions["A"].width = 22
    ws3.column_dimensions["B"].width = 22
    ws3.column_dimensions["C"].width = 33

    # policy 5.2 against the register, the training record and the form
    ws4 = wb.create_sheet("Examiners")
    ws4["A1"] = "Examiners eligible at the 7 December 2026 allocation who offered each session (policy 5.2)"
    ws4["A1"].font = Font(bold=True, size=12)
    ws4.append([])
    ws4.append(["Site"] + [s[1] for s in K.SESSIONS])
    top4 = ws4.max_row
    header(ws4, top4, wrap=True)
    for site in [s[0] for s in K.SITES27]:
        ws4.append([SITE_NAME[site]] + [fig["ask_b"]["%s %s" % (site, s[0])] for s in K.SESSIONS])
    notes(ws4, ws4.max_row + 2, [
        "Active on the register, at an eligible grade, with the examiner training or a refresher attended on or "
        "after 7 December 2023 (training record).",
        "Each examiner's latest response to the availability form stands (form closed 27 November 2026).",
        "An examiner who offered several sessions is counted in each, so a row does not add to a head count."])
    ws4.freeze_panes = ws4.cell(top4 + 1, 2)
    ws4.column_dimensions["A"].width = 46
    for col in "BCDE":
        ws4.column_dimensions[col].width = 15
    ws4.row_dimensions[top4].height = 30
    for w_ in wb.worksheets:
        w_.page_setup.orientation = "landscape"
        w_.page_setup.fitToWidth = 1
        w_.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def write_chart(path, fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "task269"
    xs = K.SETTINGS
    ys = [float(fig["reliability"][str(n)]) for n in xs]
    n = fig["call"]["stations"]
    r = float(fig["reliability"][str(n)])
    fig_, ax = plt.subplots(figsize=(8.8, 5.2), dpi=110)
    ax.plot(xs, ys, color="#2f4a63", lw=2, zorder=3)
    ax.scatter([x for x in xs if x != n], [y for x, y in zip(xs, ys) if x != n], s=36, color="#2f4a63", zorder=4)
    for x, y in zip(xs, ys):
        if x != n:
            right = x == fig["rooms"]
            ax.annotate("%.3f" % y, (x, y), xytext=(-8 if right else 0, -15), textcoords="offset points",
                        ha="right" if right else "center", fontsize=8.5, color="#41505c")
    ax.scatter([n], [r], s=150, color="#1f6b4a", zorder=5)
    ax.annotate("%d stations: %.3f" % (n, r), (n, r), xytext=(-12, 16), textcoords="offset points", ha="right",
                fontsize=10.5, fontweight="bold", color="#1f6b4a")
    std = float(fig["standard"])
    ax.axhline(std, color="#b3412f", ls="--", lw=1.3, zorder=2)
    ax.text(11.65, std + 0.0012, "Standard %s (policy 4.3)" % fig["standard"], color="#b3412f", fontsize=9,
            va="bottom")
    ax.axvline(fig["rooms"], color="#6b6b6b", ls=":", lw=1.4, zorder=2)
    ax.text(fig["rooms"] - 0.08, 0.7445, "%d rooms a site" % fig["rooms"], color="#55595c", fontsize=9, ha="right",
            va="bottom")
    ax.set_xticks(xs)
    ax.set_xlim(11.5, 18.5)
    ax.set_ylim(0.74, 0.85)
    ax.set_yticks([0.74, 0.76, 0.78, 0.80, 0.82, 0.84])
    ax.set_yticklabels(["%.2f" % v for v in [0.74, 0.76, 0.78, 0.80, 0.82, 0.84]])
    ax.set_xlabel("Stations in the circuit")
    ax.set_ylabel("Reliability of the total mark")
    fig_.text(0.012, 0.965, "Final OSCE 2027: %d stations are the fewest that meet the %s standard"
              % (n, fig["standard"]), fontsize=12.5, fontweight="bold", color="#1d2830", va="top")
    fig_.text(0.012, 0.918, "One examiner a station in each of three circuits; from the variance components of the "
              "May 2026 marks (84 candidates, 12 stations)", fontsize=8.8, color="#4a4f54", va="top")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig_.text(0.01, 0.01, "Examinations Office, December 2026. Reliabilities to three decimals.", fontsize=7.8,
              color="#6b6f73")
    fig_.tight_layout(rect=(0, 0.03, 1, 0.88))
    fig_.savefig(path, metadata={"Software": None})
    plt.close(fig_)


def write(target, golden, w):
    fig = figures(w)
    # the policy's section numbers as the shipped policy carries them, for the write-up's citations
    import re
    import verify as V
    pol = V.pdf_text(os.path.join(target, K.FILES["policy"]))
    fig["policy_sections"] = sorted({float(m) for m in re.findall(r"(?<![\d.])(\d\.\d)(?= [A-Z])", pol)})
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    if os.path.exists(golden):
        for f in os.listdir(golden):
            os.remove(os.path.join(golden, f))
    else:
        os.makedirs(golden)
    xl = os.path.join(golden, "osce2027_station_plan.xlsx")
    write_workbook(xl, fig)
    PP.COMPANY = K.UNIVERSITY
    PP.normalize_ooxml(xl, K.PEOPLE["assessment"], K.PEOPLE["assessment"], "2026-12-03T09:12:40Z",
                       "2026-12-04T15:47:12Z", excel=True)
    write_chart(os.path.join(golden, "osce2027_reliability_chart.png"), fig)
    meta = {"task": "task269",
            "distractor_files": ["target/" + K.FILES[k] for k in ("sp_invoices", "feedback", "global")],
            "deliverables": ["osce2027_station_plan.xlsx", "osce2027_reliability_chart.png"],
            "stated_inputs": [],
            "call_files": [K.FILES[k] for k in ("marks", "stations", "examiners26", "minutes", "policy", "plan")],
            "ask_files": [K.FILES[k] for k in ("bank", "usage", "migration", "register", "availability", "training")],
            "distractor_notes": {K.FILES["sp_invoices"]: "the simulated patient agency's 2026 invoices: what the stations "
                                                    "cost, relevant to the size of the 2027 sitting and unused by "
                                                    "every answer",
                            K.FILES["feedback"]: "candidates' ratings of the 2026 stations: relevant to which cases "
                                                 "run well and unused by every answer",
                            K.FILES["global"]: "the examiners' global grades for every 2026 encounter: the same "
                                               "encounters' holistic judgement, relevant to how the stations "
                                               "performed and unused by every answer (policy 3.2 makes the "
                                               "checklist the station mark)"},
            "sources": {f: "constructed for this task (seeded generator); the university, its partner school, the "
                           "accreditation board and every person are fictional" for f in sorted(K.FILES.values())},
            "license": "original synthetic data, CC0", "as_at": K.PACK_DATE.isoformat()}
    json.dump(meta, open(os.path.join(os.path.dirname(target), "metadata.json"), "w"), indent=1)
    return fig
