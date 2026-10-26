"""The goldens: the board paper's workbook (agency_township_2027.xlsx) and its chart
(water_claims_by_township_2027.png), and generator/figures.json, every figure the write-up states, computed from
the shipped pack by analysis.py."""
import json
import os

import numpy as np

import analysis as A
import common as K

NAME = {t: K.TOWN_NAME[t] for t in K.CANDIDATES}
INK, MUTED, SURFACE, PICK, OTHER, LINE = "#0b0b0b", "#52514e", "#fcfcfb", "#2a78d6", "#b9b8b2", "#3d3c39"


def figures(r):
    best = r["best"]
    town = {t: int(K.r(best["town"][t])) for t in K.CANDIDATES}
    order = sorted(K.CANDIDATES, key=lambda t: best["town"][t])
    pick, runner = order[0], order[1]
    noz = [x for x in r["res"] if "zone" not in x["cols"]][0]
    d = r["d"]
    homes = r["homes"]
    levels = {c: sorted(set(d[c])) for c in best["cols"]}
    rel = {}
    for c in best["cols"]:
        for i, lv in enumerate(levels[c][1:]):
            pos = 1 + sum(len(levels[cc]) - 1 for cc in best["cols"][:best["cols"].index(c)]) + i
            rel["%s=%s vs %s" % (c, lv, levels[c][0])] = K.r(float(np.exp(best["params"][pos])), 2)
    book = 1000.0 * d["n"].sum() / d["expo"].sum()
    fig = {
        "call": {"township": pick, "name": NAME[pick], "runner_up": runner, "runner_up_name": NAME[runner],
                 "gap_per_1000": town[runner] - town[pick]},
        "components": {
            "frequency_per_1000": town,
            "valley_zone_homes": {t: int((homes[homes["town"] == t]["zone"] == K.VALLEY).sum()) for t in K.CANDIDATES},
            "homes": {t: int((homes["town"] == t).sum()) for t in K.CANDIDATES},
            "chosen_model": list(best["cols"]),
            "deviance_2025_chosen": K.r(best["dev"], 1),
            "deviance_2025_best_recorded_only": K.r(noz["dev"], 1),
            "best_recorded_only_model": list(noz["cols"]),
        },
        "asks": {
            "protected_homes": {t: int(homes[homes["town"] == t]["protected"].sum()) for t in K.CANDIDATES},
            "market_value_musd": r["market"],
            "water_payment_by_accident_year": r["pay"],
            "fire_per_1000": {"unprotected": r["fire"]["unprotected"]},
        },
        "context": {
            "book_frequency_per_1000": int(K.r(book)),
            "book_house_years": K.r(d["expo"].sum(), 1),
            "book_water_claims": int(d["n"].sum()),
            "relativities": rel,
            "recorded_only_frequency_per_1000": {t: K.r(noz["town"][t], 1) for t in K.CANDIDATES},
            "common_level_ratio": r["clr"],
        },
        "references": {"rounding": "frequencies whole per 1,000 house-years; market values to 0.1 million dollars; "
                                    "payments whole dollars; the fire frequency to 0.1 per 1,000 house-years",
                       "dates": [2023, 2024, 2025, 2026, 2027],
                       "standard_sections": [2.1, 2.4],
                       "cause_codes": [3110, 3120, 3130, 5110, 5120],
                       "nfpa_standard": 291, "nfpa_exponent": 0.54},
    }
    return fig


def chart(path, fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams["font.family"] = "DejaVu Sans"
    rcParams["svg.hashsalt"] = "task271"
    f = fig["components"]["frequency_per_1000"]
    book = fig["context"]["book_frequency_per_1000"]
    order = sorted(K.CANDIDATES, key=lambda t: f[t])
    fg, ax = plt.subplots(figsize=(7.6, 4.3), dpi=150)
    fg.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ys = np.arange(len(order))[::-1]
    for y, t in zip(ys, order):
        ax.barh(y, f[t], height=0.56, color=PICK if t == fig["call"]["township"] else OTHER, edgecolor=SURFACE,
                linewidth=2)
        ax.text(f[t] + 0.35, y, "%d" % f[t], va="center", ha="left", fontsize=10.5, color=INK,
                fontweight="bold" if t == fig["call"]["township"] else "normal")
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s %s" % (K.TOWN_NAME[t], dict((c, k) for c, n, k in K.TOWNS)[t]) for t in order],
                       fontsize=10, color=INK)
    ax.axvline(book, color=LINE, linewidth=1.4, linestyle=(0, (4, 3)))
    ax.text(book + 0.25, ys[0] + 0.48, "Our book, 2023 to 2025: %d" % book, fontsize=8.8, color=MUTED, va="bottom")
    ax.set_xlim(0, max(f.values()) * 1.18)
    ax.set_ylim(-0.6, len(order) - 0.15)
    ax.set_xlabel("Non-weather water claims per 1,000 house-years, at our 2023 to 2025 experience", fontsize=9,
                  color=MUTED)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c2")
    ax.tick_params(axis="x", colors=MUTED, labelsize=8.5)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)
    p = fig["call"]
    fg.suptitle("%s's homes would bring the fewest non-weather water claims" % p["name"], x=0.02, ha="left",
                fontsize=12.2, color=INK, fontweight="bold", y=0.975)
    ax.set_title("Owner-occupied single-family homes on the 2026 roll, each at the Frequency Model Standard's\n"
                 "chosen model (foundation and water supply zone)", loc="left", fontsize=8.3, color=MUTED, pad=8)
    fg.text(0.02, 0.018, "Source: Halverstead Mutual policy and claim extracts of August 31, 2026; Tamswold County "
                         "certified 2026 roll;\nTamswold County Water Authority pressure zones (November 2025).",
            fontsize=7.2, color=MUTED, va="bottom")
    fg.subplots_adjust(left=0.24, right=0.97, top=0.79, bottom=0.22)
    fg.savefig(path, facecolor=SURFACE, metadata={"Software": None})
    plt.close(fg)


def workbook(path, fig, r):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Townships"
    bold = Font(bold=True)
    thin = Side(style="thin", color="999999")
    p = fig["call"]
    f = fig["components"]["frequency_per_1000"]
    ws["A1"] = "2027 agency: the township"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Recommendation: open the 2027 agency in %s Borough. Its homes would bring %d non-weather water "
                "claims per 1,000 house-years at our 2023 to 2025 experience, against %d in %s and %d in %s." % (
                    p["name"], f[p["township"]], f[p["runner_up"]], p["runner_up_name"],
                    f[[t for t in K.CANDIDATES if t not in (p["township"], p["runner_up"])][0]],
                    K.TOWN_NAME[[t for t in K.CANDIDATES if t not in (p["township"], p["runner_up"])][0]]))
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:G2")
    ws.row_dimensions[2].height = 33
    hdr = ["Township", "Owner-occupied single-family homes", "Of which in the Valley zone",
           "Non-weather water claims per 1,000 house-years", "Protected homes", "Market value ($ millions)"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    order = sorted(K.CANDIDATES, key=lambda t: f[t])
    for t in order:
        ws.append([K.TOWN_FULL[t], fig["components"]["homes"][t], fig["components"]["valley_zone_homes"][t], f[t],
                   fig["asks"]["protected_homes"][t], fig["asks"]["market_value_musd"][t]])
    for row in ws.iter_rows(min_row=5, max_row=4 + len(order)):
        row[1].number_format = "#,##0"
        row[2].number_format = "#,##0"
        row[3].number_format = "0"
        row[4].number_format = "#,##0"
        row[5].number_format = "#,##0.0"
        if row[0].value.startswith(p["name"]):
            for c in row:
                c.fill = PatternFill("solid", fgColor="DCE9F7")
    ws.append([])
    ws.append(["Our book, 2023 to 2025", None, None, fig["context"]["book_frequency_per_1000"]])
    ws.cell(ws.max_row, 4).number_format = "0"
    ws.append([])
    notes = [
        "Frequency: the Frequency Model Standard's model for a territory we have not written, the mean over the "
        "township's homes of each home's frequency; homes are the owner-occupied single-family detached homes on the "
        "certified 2026 roll (land use R-SFD, homestead exclusion).",
        "Protected: an in-service Authority hydrant within 1,000 feet whose latest flow test shows 500 gpm at 20 psi "
        "(underwriting guide 2), from the Authority's register and test log of June 30, 2026.",
        "Market value: 2026 assessments after the 2026 appeal decisions, at the common level ratio in effect on "
        "January 1, 2026 (%.3f)." % fig["context"]["common_level_ratio"]]
    for n in notes:
        ws.append([n])
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=7)
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(ws.max_row, 1).font = Font(size=9, color="555555")
        ws.row_dimensions[ws.max_row].height = 30
    for col, w in zip("ABCDEFG", (26, 17, 15, 19, 12, 14, 4)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    m = wb.create_sheet("Model test")
    m["A1"] = "Frequency Model Standard section 4: fitted on accident years 2023 and 2024, judged on 2025"
    m["A1"].font = bold
    m.append(["Model (main effects)", "Poisson deviance, 2025"])
    for c in m[2]:
        c.font = bold
    shown = r["res"][:6] + [x for x in r["res"] if "zone" not in x["cols"]][:3]
    lab = {"found": "foundation", "era": "year built era", "bath": "full bathrooms", "cons": "construction",
           "st": "stories", "zone": "water supply zone"}
    for x in shown:
        m.append([", ".join(lab[c] for c in x["cols"]) or "none", K.r(x["dev"], 1)])
        m.cell(m.max_row, 2).number_format = "#,##0.0"
    m.append([])
    m.append(["Chosen: %s, refitted on 2023 to 2025. Relativities:" % ", ".join(lab[c] for c in r["best"]["cols"])])
    for k, v in fig["context"]["relativities"].items():
        c, rest = k.split("=")
        m.append(["%s %s" % (lab[c], rest), v])
        m.cell(m.max_row, 1).alignment = Alignment(indent=1)
        m.cell(m.max_row, 2).number_format = "0.00"
    m.column_dimensions["A"].width = 64
    m.column_dimensions["B"].width = 22

    b = wb.create_sheet("Book")
    b["A1"] = "Our book, accident years 2023 to 2025"
    b["A1"].font = bold
    b.append(["Accident year", "Average non-weather water claim payment ($)"])
    for c in b[2]:
        c.font = bold
    for y, v in fig["asks"]["water_payment_by_accident_year"].items():
        b.append([int(y), v])
        b.cell(b.max_row, 1).alignment = Alignment(horizontal="left")
        b.cell(b.max_row, 2).number_format = "#,##0"
    b.append([])
    b.append(["Fire and lightning, accident years 2023 to 2025", "Claims per 1,000 house-years"])
    for c in b[b.max_row]:
        c.font = bold
    b.append(["Homes the guide classes as unprotected (class 9 rate)", fig["asks"]["fire_per_1000"]["unprotected"]])
    b.cell(b.max_row, 2).number_format = "0.0"
    b.append([])
    b.append(["Payments: indemnity paid to date per claim with indemnity paid, net of recoveries, from the claim "
              "system and Corrigan Adjusting Services' bordereau, to August 31, 2026."])
    b.cell(b.max_row, 1).font = Font(size=9, color="555555")
    b.column_dimensions["A"].width = 58
    b.column_dimensions["B"].width = 26
    wb.save(path)


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    r = A.run(target)
    fig = figures(r)
    workbook(os.path.join(golden, K.BOOK), fig, r)
    chart(os.path.join(golden, K.CHART), fig)
    return fig, r


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
