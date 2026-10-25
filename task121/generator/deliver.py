"""The goldens: halwick_progress8_walk_2022_2024.xlsx and halwick_progress8_walk.png, and generator/figures.json,
every figure read back from the shipped files."""
from __future__ import annotations

import json
import os
from decimal import ROUND_HALF_UP, Decimal

import analysis as A
import common as K


def half_up(x, nd=0):
    if nd:
        return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))
    return int(Decimal(repr(float(x))).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def p1(x):
    v = half_up(x, 1)
    return "0.0" if v == 0 else "%.1f" % v


def results(target):
    D = A.load(target)
    E = A.pupils(D)
    w = A.walk(E)
    two = A.walk(E, classify=("secondary",))
    feed = feeders(D, E)
    return dict(D=D, E=E, walk=w, default=two, feeders=feed, att=A.attendance(D), res=A.results(D))


def feeders(D, E):
    """The seven primaries that each send Halwick more than 5 per cent of its pupils, by name, with their pupils'
    Progress 8 at Halwick and at the borough's other secondaries."""
    R = D["register"]
    name = {}
    for r in R.itertuples():
        if r.phase == "Primary" and r.status == "Open":
            name[r.urn] = r.establishment_name
            if r.predecessor_urn:
                name[r.predecessor_urn] = r.establishment_name
    H = E[E.ks4_school == A.FOCAL_NAME]
    share = H.ks2_school.value_counts() / len(H)
    top = [s for s in share.index if share[s] > 0.05]
    rows = []
    for s in top:
        g = E[E.ks2_school == s]
        rows.append(dict(school=name[s.split(":")[1]], share=100.0 * float(share[s]),
                         n_halwick=int((g.ks4_school == A.FOCAL_NAME).sum()),
                         n_elsewhere=int((g.ks4_school != A.FOCAL_NAME).sum()),
                         p8_halwick=float(g[g.ks4_school == A.FOCAL_NAME].p8.mean()),
                         p8_elsewhere=float(g[g.ks4_school != A.FOCAL_NAME].p8.mean())))
    G = E[E.ks2_school.isin(top)]
    O = E[~E.ks2_school.isin(top)]
    pooled = dict(share=100.0 * float(share[top].sum()), p8_elsewhere=float(G[G.ks4_school != A.FOCAL_NAME].p8.mean()),
                  n_elsewhere=int((G.ks4_school != A.FOCAL_NAME).sum()),
                  p8_halwick=float(G[G.ks4_school == A.FOCAL_NAME].p8.mean()),
                  p8_others_at_halwick=float(O[O.ks4_school == A.FOCAL_NAME].p8.mean()),
                  n_others_at_halwick=int((O.ks4_school == A.FOCAL_NAME).sum()))
    return dict(rows=rows, pooled=pooled)


def figures(res):
    w, two = res["walk"], res["default"]
    T = res["E"][res["E"].trust]
    H = res["E"][res["E"].ks4_school == A.FOCAL_NAME]
    big = A.largest(w)
    walk = {k: p1(w[k]) for k in ("gap", "att", "dis", "own", "rem")}
    sentence = ("No: the academy's own effect accounts for almost none of Halwick's Progress 8 gap to the trust "
                "(%s of %s points); the largest item is the remainder (%s), the shortfall its pupils bring from the "
                "seven primary schools that send it most of its intake, ahead of attendance (%s) and disadvantage "
                "(%s)" % (walk["own"], walk["gap"], walk["rem"], walk["att"], walk["dis"]))
    fe = res["feeders"]
    return {
        "call": {"verdict": "no", "largest": big, "largest_name": A.ITEM_NAME[big], "sentence": sentence},
        "walk": walk,
        "walk_unrounded": {k: round(float(w[k]), 4) for k in ("gap", "att", "dis", "own", "rem")},
        "trust_p8": "%.2f" % half_up(T.p8.mean(), 2), "halwick_p8": "%.2f" % half_up(H.p8.mean(), 2),
        "pupils": {"halwick": int(len(H)), "trust": int(len(T)), "borough": int(len(res["E"]))},
        "default_path": {k: p1(two[k]) for k in ("gap", "att", "dis", "own", "rem")},
        "model": {"b_absence": "%.3f" % half_up(w["b_abs"], 3), "b_disadvantaged": "%.2f" % half_up(w["b_dis"], 2),
                  "absence_halwick": "%.2f" % half_up(w["abs_h"], 2), "absence_trust": "%.2f" % half_up(w["abs_t"], 2),
                  "disadvantaged_halwick_pct": "%.1f" % half_up(100 * w["dis_h"], 1),
                  "disadvantaged_trust_pct": "%.1f" % half_up(100 * w["dis_t"], 1),
                  "walk_3dp": {k: "%.3f" % half_up(w[k], 3) for k in ("gap", "att", "dis", "own", "rem")}},
        "feeders": {"count": len(fe["rows"]), "share_of_halwick": half_up(fe["pooled"]["share"]),
                    "p8_elsewhere": "%.2f" % half_up(fe["pooled"]["p8_elsewhere"], 2),
                    "p8_at_halwick": "%.2f" % half_up(fe["pooled"]["p8_halwick"], 2),
                    "p8_others_at_halwick": "%.2f" % half_up(fe["pooled"]["p8_others_at_halwick"], 2),
                    "names": [r["school"] for r in fe["rows"]]},
        "filed_constants": {"persistent_absence_threshold_pct": 10, "severe_absence_threshold_pct": 50,
                            "year_10": 10, "year_11": 11},
        "annex_a": {k: {"pa": "%.1f" % half_up(v["pa"], 1), "sa": "%.1f" % half_up(v["sa"], 1), "pupils": v["n"]}
                    for k, v in sorted(res["att"].items())},
        "annex_b": {k: {"a8": "%.1f" % half_up(v["a8"], 1), "ebacc": "%.1f" % half_up(v["ebacc"], 1),
                        "pupils": v["n"]} for k, v in res["res"].items()},
    }


# ------------------------------------------------------------------ the chart
def chart_png(path, fig, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("LiberationSans-Regular", "LiberationSans-Bold"):
        font_manager.fontManager.addfont("/usr/share/fonts/truetype/liberation/%s.ttf" % f)
    plt.rcParams["font.family"] = "Liberation Sans"
    w, wu = fig["walk"], fig["walk_unrounded"]
    T = res["E"][res["E"].trust]
    start = float(T.p8.mean())
    steps = [("Attendance", wu["att"], w["att"]), ("Disadvantage", wu["dis"], w["dis"]),
             ("Halwick's own\neffect", wu["own"], w["own"]),
             ("Remainder: what its\npupils bring from\nprimary school", wu["rem"], w["rem"])]
    fg, ax = plt.subplots(figsize=(9.2, 5.4), dpi=150)
    ink, grey, accent, muted = "#1d2733", "#8a949e", "#b4532a", "#5b7c99"
    ax.bar(0, start, color=grey, width=0.6)
    ax.text(0, start - 0.012, fig["trust_p8"], ha="center", va="top", fontsize=10, color=ink)
    level = start
    for i, (lab, v, label) in enumerate(steps, start=1):
        col = accent if lab.startswith("Remainder") else muted
        ax.bar(i, v, bottom=level, color=col, width=0.6)
        ax.text(i, level + min(v, 0) - 0.012, label, ha="center", va="top",
                fontsize=10.5, color=ink, fontweight="bold" if col == accent else "normal")
        ax.plot([i - 0.7, i - 0.3], [level, level], color=grey, lw=0.8)
        level += v
    end = level
    ax.bar(len(steps) + 1, end, color=grey, width=0.6)
    ax.text(len(steps) + 1, end - 0.012, fig["halwick_p8"], ha="center", va="top", fontsize=10, color=ink)
    ax.set_xticks(range(len(steps) + 2))
    ax.set_xticklabels(["Trust average"] + [s[0] for s in steps] + ["Halwick"], fontsize=9.2, color=ink)
    ax.axhline(0, color=ink, lw=0.8)
    ax.set_ylabel("Progress 8 points", fontsize=10, color=ink)
    ax.set_ylim(min(end, start) - 0.18, 0.08)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=ink, labelsize=9)
    ax.grid(axis="y", color="#e2e6ea", lw=0.6)
    ax.set_axisbelow(True)
    fg.suptitle("Halwick's Progress 8 gap is mostly what its pupils bring with them, not the academy's own effect",
                x=0.02, ha="left", fontsize=12.5, fontweight="bold", color=ink)
    ax.set_title("Walk from the trust average to Halwick, pupils finishing key stage 4 in 2022 to 2024, Progress 8 "
                 "points; the four steps to one decimal", loc="left", fontsize=9.3, color="#46525e")
    fg.text(0.02, 0.012, "Source: Brantholme KS2 to KS4 transfer file, %s pupils with Progress 8 at the borough's 14 "
                         "secondaries. Fixed effects for each secondary and each key stage 2 school,\nwith the year 11 "
                         "absence rate and disadvantage. Bars drawn to the unrounded items. Larkhollow Data and "
                         "Assessment." % format(fig["pupils"]["borough"], ","), fontsize=7.6, color="#5c6670")
    fg.tight_layout(rect=(0, 0.05, 1, 0.97))
    fg.savefig(path, metadata={"Software": None})
    plt.close(fg)


# ------------------------------------------------------------------ the workbook
def workbook(path, fig, res):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ink = "1D2733"
    head_fill = PatternFill("solid", fgColor="E4EAE6")
    thin = Side(style="thin", color="B8C0C8")
    bold = Font(bold=True, color=ink)
    note = Font(italic=True, color="56616C", size=9)

    def header(ws, row, cells):
        for j, v in enumerate(cells, start=1):
            c = ws.cell(row=row, column=j, value=v)
            c.font = bold
            c.fill = head_fill
            c.border = Border(bottom=thin)
            c.alignment = Alignment(wrap_text=True, vertical="top")

    w = fig["walk"]
    ws = wb.active
    ws.title = "Walk"
    ws["A1"] = "Halwick's Progress 8 gap to the trust is mostly what its pupils bring from primary school"
    ws["A1"].font = Font(bold=True, size=13, color=ink)
    ws["A2"] = ("Pupils finishing key stage 4 in 2022, 2023 and 2024 with a Progress 8 score; the walk in Progress 8 "
                "points to one decimal place, as Paper 6 asks")
    ws["A2"].font = Font(italic=True, color="56616C")
    header(ws, 4, ["Item", "Progress 8 points", "How it is measured"])
    rows = [("Trust average", fig["trust_p8"], "All %s pupils at the eight academies, pooled" % format(fig["pupils"]["trust"], ",")),
            ("Attendance", w["att"], "Effect of the year 11 absence rate, times Halwick's average rate less the trust's"),
            ("Disadvantage", w["dis"], "Effect of being disadvantaged, times Halwick's share less the trust's"),
            ("The academy's own effect", w["own"], "Halwick's own effect less the trust's pupil-weighted average"),
            ("The remainder", w["rem"], "What Halwick's pupils bring from the schools they came from"),
            ("Halwick", fig["halwick_p8"], "All %s Halwick pupils, pooled" % format(fig["pupils"]["halwick"], ",")),
            ("Gap (Halwick less trust)", w["gap"], "The four items above add to it")]
    for i, (a, b, c) in enumerate(rows, start=5):
        ws.cell(row=i, column=1, value=a)
        ws.cell(row=i, column=2, value=float(b)).number_format = "0.00" if a in ("Trust average", "Halwick") else "0.0"
        ws.cell(row=i, column=3, value=c)
        if a in ("The remainder", "Gap (Halwick less trust)"):
            ws.cell(row=i, column=1).font = bold
            ws.cell(row=i, column=2).font = bold
    ws["A13"] = ("Largest item: the remainder. The academy's own effect is %s of the %s gap. Effects are estimated on all "
                 "%s pupils at the borough's fourteen secondaries, with a fixed effect for each secondary and for each "
                 "school where pupils sat key stage 2, unshrunk, as Paper 6 sets out." % (w["own"], w["gap"],
                                                                                          format(fig["pupils"]["borough"], ",")))
    ws["A13"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A13:C13")
    ws.row_dimensions[13].height = 48
    fe = res["feeders"]
    header(ws, 15, ["Primary school (where pupils sat key stage 2)", "Share of Halwick's pupils (%)",
                    "Pupils at Halwick", "Pupils at other secondaries", "Progress 8 at Halwick",
                    "Progress 8 at other secondaries"])
    r = 16
    for x in fe["rows"]:
        ws.cell(row=r, column=1, value=x["school"])
        ws.cell(row=r, column=2, value=half_up(x["share"], 1)).number_format = "0.0"
        ws.cell(row=r, column=3, value=x["n_halwick"])
        ws.cell(row=r, column=4, value=x["n_elsewhere"])
        ws.cell(row=r, column=5, value=half_up(x["p8_halwick"], 2)).number_format = "0.00"
        ws.cell(row=r, column=6, value=half_up(x["p8_elsewhere"], 2)).number_format = "0.00"
        r += 1
    po = fe["pooled"]
    ws.cell(row=r, column=1, value="The seven together").font = bold
    ws.cell(row=r, column=2, value=half_up(po["share"], 1)).number_format = "0.0"
    ws.cell(row=r, column=4, value=po["n_elsewhere"])
    ws.cell(row=r, column=5, value=half_up(po["p8_halwick"], 2)).number_format = "0.00"
    ws.cell(row=r, column=6, value=half_up(po["p8_elsewhere"], 2)).number_format = "0.00"
    ws.cell(row=r + 1, column=1, value="Halwick's pupils from every other school")
    ws.cell(row=r + 1, column=3, value=po["n_others_at_halwick"])
    ws.cell(row=r + 1, column=5, value=half_up(po["p8_others_at_halwick"], 2)).number_format = "0.00"
    ws.cell(row=r + 3, column=1, value="Source: Brantholme KS2 to KS4 transfer file; school names from the borough's "
                                       "establishment register (converted academies under their current name).")
    ws.cell(row=r + 3, column=1).font = note
    for col, wd in zip("ABCDEF", (46, 16, 62, 16, 14, 18)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"

    wa = wb.create_sheet("Annex A attendance")
    wa["A1"] = "Annex A: persistent and severe absence by academy, 2025/26"
    wa["A1"].font = Font(bold=True, size=12, color=ink)
    header(wa, 3, ["Academy", "Pupils counted", "Persistent absence (%)", "Severe absence (%)"])
    for i, k in enumerate(A.TRUST_NAMES, start=4):
        v = fig["annex_a"][k]
        wa.cell(row=i, column=1, value=k)
        wa.cell(row=i, column=2, value=v["pupils"])
        wa.cell(row=i, column=3, value=float(v["pa"])).number_format = "0.0"
        wa.cell(row=i, column=4, value=float(v["sa"])).number_format = "0.0"
    wa.cell(row=13, column=1, value="Each academy counts its pupils' sessions while on its roll; a pupil who moved "
                                    "between academies counts at each. Year 11: autumn and spring terms only.")
    wa.cell(row=13, column=1).font = note
    for col, wd in zip("ABCD", (36, 16, 22, 20)):
        wa.column_dimensions[col].width = wd
    wa.freeze_panes = "A4"

    wr = wb.create_sheet("Annex B results")
    wr["A1"] = "Annex B: average Attainment 8 and EBacc entry by academy, 2026 cohort"
    wr["A1"].font = Font(bold=True, size=12, color=ink)
    header(wr, 3, ["Academy", "Pupils in the cohort", "Average Attainment 8", "EBacc entry (%)"])
    for i, k in enumerate(A.TRUST_NAMES, start=4):
        v = fig["annex_b"][k]
        wr.cell(row=i, column=1, value=k)
        wr.cell(row=i, column=2, value=v["pupils"])
        wr.cell(row=i, column=3, value=float(v["a8"])).number_format = "0.0"
        wr.cell(row=i, column=4, value=float(v["ebacc"])).number_format = "0.0"
    wr.cell(row=13, column=1, value="Results from the summer 2025 series (year 10 entries) and the summer 2026 series; "
                                    "for English, maths and EBacc subjects the first entry counts.")
    wr.cell(row=13, column=1).font = note
    for col, wd in zip("ABCD", (36, 20, 22, 18)):
        wr.column_dimensions[col].width = wd
    wr.freeze_panes = "A4"

    wn = wb.create_sheet("Notes")
    notes = ["Prepared for Paper 6 (Board of Trustees, 9 December 2026) by %s, Data and Assessment." % K.PEOPLE["data"],
             "Walk: estimated on the council's transfer file, all %s pupils with a Progress 8 score at the borough's "
             "fourteen secondaries in 2021/22 to 2023/24." % format(fig["pupils"]["borough"], ","),
             "Model: Progress 8 on the year 11 absence rate and the disadvantaged flag, with a fixed effect for each "
             "secondary and for each school where a pupil sat key stage 2 (academy converters read through their "
             "predecessor URN; schools outside the borough as recorded).",
             "The academy's own effect: Halwick's secondary effect less the trust's average, weighted by the trust's "
             "%s pupils." % format(fig["pupils"]["trust"], ","),
             "Read alone, Progress 8 and a model of pupils within secondaries put %s of the gap on the academy itself; "
             "the same primaries' pupils at the other secondaries show the shortfall is theirs." % (
                 fig["default_path"]["own"]),
             "Rounding: the walk to one decimal place of a Progress 8 point; averages to two; rates to one."]
    for i, t in enumerate(notes, start=1):
        wn.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    wn.column_dimensions["A"].width = 120
    wb.properties.creator = K.PEOPLE["data"]
    wb.save(path)


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    res = results(target)
    fig = figures(res)
    workbook(os.path.join(golden, K.GOLDEN), fig, res)
    chart_png(os.path.join(golden, K.CHART), fig, res)
    return fig, res
