"""The golden deliverables from the shipped pack: the Center's estimates register for 1 July 2026 (a workbook) and the
chart of each municipality's estimate against the urban tier line (an SVG), with generator/figures.json."""
import json
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import asks as A
import methods as M
import postprocess as PP
import world as W

REGISTER = "tamarack_municipal_estimates_2026.xlsx"
CHART = "urban_tier_estimates_2026.svg"
FAMILY = ("age", "age10", "age5", "age3", "curve", "age_x", "age10_x", "age5_x", "age3_x")


def r100(v):
    return int(round(v / 100.0)) * 100


def compute(t):
    e = M.rungs(t)
    gold = e["age"]
    names = [m[1] for m in W.MUNIS]
    hu26 = M.hu(t, M.xf(W.EST))
    gq = M.gq2026(t)
    bg, bn = A.births(t)
    dg, dn, dc = A.deaths(t)
    tier = [n for n in names if gold[n] >= W.LINE]
    fam = {n: (min(e[k][n] for k in FAMILY), max(e[k][n] for k in FAMILY)) for n in names}
    return dict(e=e, gold=gold, names=names, hu26=hu26, gq=gq, births=bg, births_city=bn, deaths=dg, deaths_code=dn,
                deaths_city=dc, tier=tier, fam=fam, t=t)


def write_register(path, X):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estimates 1 July 2026"
    ws["A1"] = "%s: municipal population estimates for 1 July 2026" % W.COUNTY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("For certification to the Secretary of Transportation for the 2027 aid year (Municipal Road Aid Act, "
                "s. 84.27). Residents rounded to the nearest hundred; the urban tier is read from the unrounded estimate.")
    ws["A2"].font = Font(size=9, italic=True)
    hdr = ["FIPS code", "Municipality", "Dwellings, 1 July 2026", "Group quarters residents", "Residents, 1 July 2026",
           "Urban tier, 2027", "Resident births, Jul 2025 to Jun 2026", "Resident deaths, Jul 2025 to Jun 2026"]
    thin = Side(style="thin", color="8A9AA8")
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2F4858")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[4].height = 44
    order = sorted(X["names"], key=lambda n: (n.split(" ")[0] != "City", n.split(" ")[0] != "Village", n))
    row = 5
    for n in order:
        vals = [W.CODE[n], n, X["hu26"][n], X["gq"].get(n, 0), r100(X["gold"][n]), "Yes" if n in X["tier"] else "No",
                X["births"][n], X["deaths"][n]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=row, column=j, value=v)
            c.border = Border(bottom=thin)
            if j in (3, 4, 5, 7, 8):
                c.number_format = "#,##0"
            if j == 6:
                c.alignment = Alignment(horizontal="center")
                if v == "Yes":
                    c.font = Font(bold=True, color="1F6F5C")
        row += 1
    ws.cell(row=row, column=2, value="%s total" % W.COUNTY).font = Font(bold=True)
    for j, key in ((3, "hu26"), (4, "gq"), (7, "births"), (8, "deaths")):
        c = ws.cell(row=row, column=j, value=sum(X[key].get(n, 0) for n in X["names"]))
        c.number_format = "#,##0"
        c.font = Font(bold=True)
    c = ws.cell(row=row, column=5, value=r100(sum(X["gold"].values())))
    c.number_format = "#,##0"
    c.font = Font(bold=True)
    for col, wdt in zip("ABCDEFGH", [10, 22, 12, 12, 12, 10, 14, 14]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "C5"
    ws.cell(row=row + 2, column=1, value=("Household residents: each dwelling standing on 1 July 2026 at the persons the "
                                          "2020 block groups show for dwellings of its type and age. Group quarters: "
                                          "the Center's 2026 survey.")).font = Font(size=9)
    ws.cell(row=row + 3, column=1, value=("Births and deaths: State Registrar's resident files, by the municipality the "
                                          "residence address lies in on the county address points.")).font = Font(size=9)
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["estimates"][0], W.PEOPLE["estimates"][0], "2026-10-26T14:05:00Z",
                       "2026-10-29T21:12:40Z", excel=True, company="State " + W.DEPT)


def write_chart(path, X):
    order = sorted(X["names"], key=lambda n: -X["gold"][n])
    W_, top, left, bar, gap = 760, 92, 178, 22, 9
    H = top + len(order) * (bar + gap) + 70
    xmax = 16000
    sx = lambda v: left + (W_ - left - 40) * v / xmax
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
           'font-family="Helvetica, Arial, sans-serif">' % (W_, H, W_, H),
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<text x="24" y="34" font-size="17" font-weight="bold" fill="#1d2b36">Tamarack County: estimated residents on '
           '1 July 2026</text>',
           '<text x="24" y="56" font-size="12" fill="#43525e">Three municipalities reach the 10,000 line for the 2027 '
           'urban tier: Juniper, Dunmore and Cedar Run</text>']
    for v in range(0, xmax + 1, 2000):
        x = sx(v)
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e3e8ec" stroke-width="1"/>' % (x, top - 8, x, H - 52))
        out.append('<text x="%.1f" y="%d" font-size="10" fill="#5b6b77" text-anchor="middle">%s</text>'
                   % (x, H - 36, "{:,}".format(v)))
    for i, n in enumerate(order):
        y = top + i * (bar + gap)
        v = X["gold"][n]
        fill = "#1f6f5c" if n in X["tier"] else "#9fb0bc"
        out.append('<text x="%d" y="%d" font-size="11.5" fill="#1d2b36" text-anchor="end">%s</text>'
                   % (left - 10, y + bar - 6, n))
        out.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s"/>' % (sx(0), y, sx(v) - sx(0), bar, fill))
        out.append('<text x="%.1f" y="%d" font-size="10.5" fill="#1d2b36">%s</text>'
                   % (sx(v) + 5, y + bar - 6, "{:,}".format(r100(v))))
    xl = sx(W.LINE)
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#b5432d" stroke-width="2" stroke-dasharray="6 4"/>'
               % (xl, top - 14, xl, H - 52))
    out.append('<text x="%.1f" y="%d" font-size="11" fill="#b5432d">10,000: urban tier (s. 84.21 (6))</text>'
               % (xl + 6, top - 18))
    out.append('<text x="24" y="%d" font-size="10" fill="#5b6b77">Residents rounded to the nearest hundred. Dwellings '
               'standing on 1 July 2026 at the persons per dwelling the 2020 block groups show by type and age; group '
               'quarters from the 2026 survey.</text>' % (H - 14))
    out.append('</svg>')
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


def figures(X):
    e = X["e"]
    names = X["names"]
    rnd = lambda d: {n: int(round(d[n])) for n in names}
    f = {
        "call": X["tier"], "call_short": [W.SHORT[n] for n in X["tier"]],
        "estimate_r100": {n: r100(X["gold"][n]) for n in names},
        "estimate": rnd(X["gold"]),
        "family_min": {n: int(round(X["fam"][n][0])) for n in names},
        "family_max": {n: int(round(X["fam"][n][1])) for n in names},
        "family_min_r10": {n: int(round(X["fam"][n][0] / 10.0)) * 10 for n in names},
        "family_max_r10": {n: int(round(X["fam"][n][1] / 10.0)) * 10 for n in names},
        "rungs": {k: rnd(v) for k, v in e.items()},
        "rung_sets": {k: [W.SHORT[n] for n in names if v[n] >= W.LINE] for k, v in e.items()},
        "rung_r100": {k: {n: r100(v[n]) for n in names} for k, v in e.items()},
        "dwellings_2026": {n: int(X["hu26"][n]) for n in names},
        "gq_2026": {n: int(X["gq"].get(n, 0)) for n in names},
        "births": X["births"], "deaths": X["deaths"],
        "births_by_written_city": X["births_city"], "deaths_by_code": X["deaths_code"],
        "births_total": sum(X["births"].values()), "deaths_total": sum(X["deaths"].values()),
        "county_estimate_r100": r100(sum(X["gold"].values())),
        "line": W.LINE, "act_section": "84.21", "age_band_bounds": [lo for lo, hi in M.AGEB],
        "land_use_codes": sorted(M.LU_TYPE), "year_built_placeholder_as": 1900,
        "default_county": int(round(sum(e["place"].values()))), "golden_county": int(round(sum(X["gold"].values()))),
    }
    import numpy as np
    bc = M.backcast(X["t"])
    for y in (2010, 2000):
        for k, v in bc[y].items():
            f["backcast_mape_%s_%d" % (k, y)] = round(float(np.mean([abs(x) for x in v.values()])), 1)
            f["backcast_max_%s_%d" % (k, y)] = round(float(max(abs(x) for x in v.values())), 1)
    f["backcast"] = {str(y): {k: {m: round(x, 1) for m, x in v.items()} for k, v in bc[y].items()} for y in (2010, 2000)}
    return f


def build(gdir, t, figs=None):
    if os.path.exists(gdir):
        for fn in os.listdir(gdir):
            os.remove(os.path.join(gdir, fn))
    else:
        os.makedirs(gdir)
    X = compute(t)
    write_register(os.path.join(gdir, REGISTER), X)
    write_chart(os.path.join(gdir, CHART), X)
    f = figures(X)
    if figs:
        with open(figs, "w") as fh:
            json.dump(f, fh, indent=1, sort_keys=True)
            fh.write("\n")
    return X, f
