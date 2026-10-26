"""The goldens from the shipped pack: the coaching wards workbook (the funded wards and every ward's 2025-26 baseline on
the grant's two outcome measures) and the compliance chart; and generator/figures.json, every figure the write-up
states."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import analysis as A   # noqa: E402
import asks as AK      # noqa: E402
import common as K     # noqa: E402

BLUE, ORANGE, INK, INK2, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e2dc", "#fcfcfb"


def compute(target):
    g = A.golden(target)
    F = g["F"]
    comp = A.components(F)
    sh, s = F["shifts"], F["sess"]
    short = sh["req"] > 1.1 * sh["worked"]
    ss = s["req"] > 1.1 * s["worked"]
    rung = A.rungs(F)
    ak = AK.golden(target)
    fig = {
        "call": {"funded": g["funded"], "count": len(g["funded"]),
                 "not_funded": [c for c in K.WARD if c not in g["funded"]],
                 "checks": {c: ("Yes" if c in g["funded"] else "No") for c in K.WARD}},
        "components": {
            "audits_as_they_stand": {c: K.r1(100 * rung["R0d"][c]) for c in K.WARD},
            "audits_lowest_other_ward": K.r1(100 * min(rung["R0d"][c] for c in K.WARD if c != "9B")),
            "care_hours_on_shifts_over_10_per_cent_short": K.r1(100 * sh.loc[short, "req"].sum() / sh["req"].sum()),
            "audited_moments_on_shifts_over_10_per_cent_short": K.r1(100 * s.loc[ss, "m"].sum() / s["m"].sum()),
            "compliance_on_those_shifts": K.r1(100 * s.loc[ss, "c"].sum() / s.loc[ss, "m"].sum()),
            "compliance_on_other_audited_shifts": K.r1(100 * s.loc[~ss, "c"].sum() / s.loc[~ss, "m"].sum()),
            "day_shifts": int(len(sh)), "audited_day_moments": int(s["m"].sum()),
        },
        "asks": {
            "A": {"hobsi": {c: int(ak["A"]["n"][c]) for c in K.WARD},
                  "rate_per_10000_obd": {c: ak["A"]["rate"][c] for c in K.WARD},
                  "occupied_bed_days": {c: int(ak["A"]["bed_days"][c]) for c in K.WARD}},
            "B": {"litres": {c: ak["B"]["litres"][c] for c in K.WARD},
                  "litres_per_1000_obd": {c: ak["B"]["rate"][c] for c in K.WARD}},
            "C": {"litres": {c: ak["C"]["litres"][c] for c in K.WARD},
                  "litres_per_1000_obd": {c: ak["C"]["rate"][c] for c in K.WARD}},
        },
        "threshold": K.BENCHMARK, "max_coaches": K.MAX_COACHES,
        "parameters": {"bands": [1.05, 1.15, 1.25, 1.35], "short_cut_per_cent": 10, "onset_hours": 48,
                       "pump_litres": 0.5, "carton_litres": 2.4, "soap_cartridge_litres": 0.8, "per_bed_days_a": 10000,
                       "per_bed_days_b": 1000},
    }
    res = dict(g=g, comp=comp, rungs=rung, asks=ak, est=g["est"])
    return fig, res


def write_workbook(path, fig):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Wards"
    head = ["Ward", "Ward name", "Coaching nurse 2027", "Hospital-onset BSI 2025-26",
            "Occupied bed days 2025-26", "HOBSI per 10,000 occupied bed days", "Hand rub put out 2025-26 (L)",
            "Hand rub per 1,000 occupied bed days (L)", "Hand soap put out 2025-26 (L)",
            "Hand soap per 1,000 occupied bed days (L)"]
    ws.append(head)
    a, b, s = fig["asks"]["A"], fig["asks"]["B"], fig["asks"]["C"]
    for c in K.WARD:
        ws.append([c, K.WARD_NAME[c], fig["call"]["checks"][c], a["hobsi"][c], a["occupied_bed_days"][c],
                   a["rate_per_10000_obd"][c], b["litres"][c], b["litres_per_1000_obd"][c], s["litres"][c],
                   s["litres_per_1000_obd"][c]])
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="5A2A52")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[1].height = 45
    for row in ws.iter_rows(min_row=2):
        row[4].number_format = "#,##0"
        row[5].number_format = "0.0"
        row[6].number_format = "#,##0.0"
        row[7].number_format = "0.0"
        row[8].number_format = "#,##0.0"
        row[9].number_format = "0.0"
        if row[2].value == "Yes":
            row[2].font = Font(bold=True)
    for col, w in zip("ABCDEFGHIJ", (7, 30, 12, 12, 12, 14, 13, 14, 13, 14)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C2"
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    n = wb.create_sheet("Notes")
    for line in ["Hand Hygiene Coaching Grant 2027: wards funded and the 2025-26 baseline.",
                 "Coaching nurse 2027: wards whose staff performed hand hygiene at fewer than 80 per cent of the "
                 "moments on their AM and PM shifts in 2025-26 (terms 2.1 to 2.4).",
                 "Hospital-onset BSI: episodes under the hospital's surveillance definitions (version 3), attributed "
                 "to the ward the patient was on when the culture was collected.",
                 "Hand rub put out: bottles issued to the ward's cost centre less returns, and the dispenser refills "
                 "fitted on the ward, each refill counted once.",
                 "Hand soap put out: soap pump bottles issued to the ward's cost centre, and the 800 mL cartridges "
                 "fitted to the ward's sink dispensers, each cartridge counted once.",
                 "Occupied bed days: midnight census, 1 July 2025 to 30 June 2026; Ward 6A includes S1A from "
                 "2 February 2026.",
                 "Sources: the hospital's application pack of 4 November 2026 (audit application export, acuity and "
                 "roster extracts, laboratory and patient administration extracts, store issues, the cleaning "
                 "contractor's dispenser rounds)."]:
        n.append([line])
    n.column_dimensions["A"].width = 120
    wb.save(path)


def write_chart(path, est, funded):
    order = sorted(K.WARD, key=lambda c: est[c])
    fig, ax = plt.subplots(figsize=(8.6, 6.2), dpi=150)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ys = list(range(len(order)))[::-1]
    for y, c in zip(ys, order):
        ax.barh(y, 100 * est[c] - 60, left=60, height=0.62, color=ORANGE if c in funded else BLUE, zorder=2,
                linewidth=0)
    ax.axvline(K.BENCHMARK, color=INK2, linestyle=(0, (4, 3)), linewidth=1.4, zorder=3)
    ax.text(K.BENCHMARK + 0.3, len(order) - 0.35, "National benchmark 80%", color=INK2, fontsize=8.5, va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s  %s" % (c, K.WARD_NAME[c]) if not K.WARD_NAME[c].startswith("Ward") else
                        "%s  %s" % (c, K.WARD_SPEC[c].split(" (")[0]) for c in order], fontsize=8.6, color=INK)
    ax.set_xlim(60, 95)
    ax.set_ylim(-0.7, len(order) + 0.2)
    ax.set_xlabel("Hand hygiene performed, share of the moments on AM and PM shifts (%)", fontsize=8.8, color=INK2)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.tick_params(axis="both", length=0, colors=INK2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ORANGE, label="Coaching nurse funded for 2027"),
                       Patch(color=BLUE, label="No coaching nurse")], loc="upper right", bbox_to_anchor=(1.0, 0.93),
              frameon=False, fontsize=8.5)
    fig.suptitle("%s wards fall below the 80%% benchmark on day-shift hand hygiene, 2025-26" %
                 {4: "Four", 5: "Five", 6: "Six"}.get(len(funded), str(len(funded))), x=0.02, ha="left", fontsize=12,
                 color=INK, fontweight="bold")
    fig.text(0.02, 0.915, "Share of the moments on each ward's AM and PM shifts at which staff performed hand "
             "hygiene, the gold auditors'\nsessions carried across every shift by its worked nursing hours against "
             "its patients' required care hours", fontsize=8.4, color=INK2, va="top")
    fig.text(0.02, 0.012, "Source: hand hygiene audit application, patient acuity system and rostering system, "
             "1 July 2025 to 30 June 2026. Ward 6A includes S1A from 2 February 2026.", fontsize=7.2, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.905))
    fig.savefig(path, dpi=150, facecolor=SURF, metadata={"Software": None})
    plt.close(fig)


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    fig, res = compute(target)
    write_workbook(os.path.join(golden, K.GOLDEN), fig)
    write_chart(os.path.join(golden, K.CHART), res["est"], fig["call"]["funded"])
    return fig, res


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
