"""The golden deliverable from the shipped pack alone, kelvane_provider_area_counts.xlsx, and generator/figures.json,
which carries every figure the write-up states. The readers here take the pack's files as they ship; the routes the
checks and the ceiling compare are run on the same readers."""
import collections
import csv
import datetime as dt
import json
import math
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import pack as P

XLSX = "kelvane_provider_area_counts.xlsx"
AS_OF = "2026-09-30"
FY = ("2025-10-01", "2026-09-30")
AREAS = ["Wickmoor City", "Fallowmere Town", "North Kelvane", "East Kelvane", "South Kelvane", "West Kelvane"]
TOWNS = AREAS[:2]
AGE60 = ["P12_%03dN" % k for k in list(range(18, 26)) + list(range(42, 50))]
AGE75 = ["P12_%03dN" % k for k in list(range(23, 26)) + list(range(47, 50))]
LABEL60 = {"60 and 61 years", "62 to 64 years", "65 and 66 years", "67 to 69 years", "70 to 74 years",
           "75 to 79 years", "80 to 84 years", "85 years and over"}
LABEL75 = {"75 to 79 years", "80 to 84 years", "85 years and over"}


# ---------------------------------------------------------------- readers
def _rows(path, skip=0):
    with open(path, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh)
        head = next(r)
        for _ in range(skip):
            next(r)
        return head, [x for x in r]


def _table(path, prefix):
    head, rows = _rows(path, skip=1)
    out = {}
    for x in rows:
        out[x[0].replace(prefix, "")] = dict(zip(head, x))
    return out


def load(target):
    f = lambda k: os.path.join(target, P.FILES[k])
    d = {"bg": _table(f("bgs"), "1500000US"), "tract": _table(f("tracts"), "1400000US"),
         "hu": {k: int(v["H1_001N"]) for k, v in _table(f("hu"), "1000000US").items()}}
    d["county"] = d["tract"].pop("0500000US57041")
    blk = collections.defaultdict(lambda: [0, 0])
    head, rows = _rows(f("blocks"))
    for g, sex, age, n in rows:
        if age in LABEL60:
            blk[g][0] += int(n)
        if age in LABEL75:
            blk[g][1] += int(n)
        blk[g].append(int(n))
    d["block"] = dict(blk)
    head, rows = _rows(f("assign"))
    d["assign_rows"] = rows
    cur, old = {}, {}
    for tb, area, code, frm, to in rows:
        g = "57041" + tb.zfill(10)
        if not to:
            cur[g] = area
        if frm <= "2016-07-01":
            old[g] = area
    d["area"], d["area_2016"] = cur, old
    head, rows = _rows(f("points"))
    pts = collections.Counter(r[3] for r in rows if r[5] == "Active")
    d["points"] = pts
    head, rows = _rows(f("roster"))
    d["roster"] = {r[0]: dict(zip(head, r)) for r in rows}
    head, rows = _rows(f("episodes"))
    d["episodes"] = [dict(zip(head, r)) for r in rows]
    head, rows = _rows(f("log"))
    d["log_head"], d["log"] = head, rows
    head, rows = _rows(f("items"))
    d["meals_per_item"] = {r[0]: int(r[2]) for r in rows}
    head, rows = _rows(f("deaths"))
    d["deaths"] = [dict(zip(head, r)) for r in rows]
    head, rows = _rows(f("links"))
    d["links"] = [dict(zip(head, r)) for r in rows]
    wb = openpyxl.load_workbook(f("providers"), read_only=True)
    ws = wb.worksheets[0]
    prov = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    d["provider"] = {r[2]: (r[0], r[1]) for r in prov}
    return d


# ---------------------------------------------------------------- the census counts
def _ages(rec, codes):
    return sum(int(rec[c]) for c in codes)


def census(d, route="bg_hu", which="60", areas=None):
    """{area: count} on the pack's files. Routes as methods.py: block_sum, bg_hu (the golden), tract_hu, bg_pop,
    bg_points; areas: the block-to-area map (the assignment in force by default)."""
    areas = areas or d["area"]
    codes = AGE60 if which == "60" else AGE75
    k = 0 if which == "60" else 1
    out = collections.Counter()
    if route == "block_sum":
        for g, a in areas.items():
            out[a] += d["block"][g][k]
        return out
    level, n = ("tract", 11) if route == "tract_hu" else ("bg", 12)
    members = collections.defaultdict(list)
    for g in areas:
        members[g[:n]].append(g)
    for u, blocks in members.items():
        total = _ages(d[level][u], codes)
        here = {areas[g] for g in blocks}
        if len(here) == 1:
            out[here.pop()] += total
            continue
        if route in ("bg_hu", "tract_hu"):
            w = [d["hu"][g] for g in blocks]
        elif route == "bg_pop":
            w = [sum(d["block"][g][2:]) for g in blocks]
        else:
            w = [d["points"].get(g, 0) for g in blocks]
        s = float(sum(w))
        for g, x in zip(blocks, w):
            out[areas[g]] += total * x / s
    return out


def cut_groups(d):
    members = collections.defaultdict(list)
    for g, a in d["area"].items():
        members[g[:12]].append(g)
    return {u: sorted(b) for u, b in sorted(members.items()) if len({d["area"][g] for g in b}) > 1}


def r10(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


# ---------------------------------------------------------------- the service figures
def provider_of_client(d):
    return {c: d["area"][r["home_block"]] for c, r in d["roster"].items()}


def meals(d, cap="plan", by="client"):
    """FY2026 meals by provider area. cap: 'plan' (a client's hot meals on a day up to meals_per_day, any other code
    once), 'none' (every row) or 'all' (one row per client, day and code); by: 'client' or 'route'."""
    i = {c: k for k, c in enumerate(d["log_head"])}
    home = provider_of_client(d)
    route_area = {code: a for a, (code, name) in d["provider"].items()}
    groups = collections.OrderedDict()
    for r in d["log"]:
        if not (FY[0] <= r[i["delivery_date"]] <= FY[1]):
            continue
        groups.setdefault((r[i["client_id"]], r[i["delivery_date"]], r[i["item_code"]]), []).append(r)
    out = dict.fromkeys(AREAS, 0)
    for (c, day, item), rs in groups.items():
        if cap == "none":
            n = len(rs)
        elif cap == "all":
            n = 1
        else:
            n = min(len(rs), int(d["roster"][c]["meals_per_day"]) if item == "HOT" else 1)
        for r in rs[:n]:
            a = home[c] if by == "client" else route_area[r[i["provider_code"]]]
            out[a] += d["meals_per_item"][item]
    return out


def active(d, chain=True, cutoff=True, by="area"):
    """Clients with an episode open on 30 September 2026 and alive that day, by provider area."""
    to_current = {l["prior_participant_id"]: l["current_participant_id"] for l in d["links"]}
    died = set()
    for x in d["deaths"]:
        if cutoff and x["date_of_death"] > AS_OF:
            continue
        s = x["state_participant_id"]
        died.add(to_current.get(s, s) if chain else s)
    code_area = {code: a for a, (code, name) in d["provider"].items()}
    home = provider_of_client(d)
    out = dict.fromkeys(AREAS, 0)
    seen = set()
    for e in d["episodes"]:
        c = e["client_id"]
        if c in seen or not (e["enrolled"] <= AS_OF and (e["closed"] == "" or e["closed"] > AS_OF)):
            continue
        if d["roster"][c]["state_participant_id"] in died:
            continue
        seen.add(c)
        out[home[c] if by == "area" else code_area[e["provider_code"]]] += 1
    return out


# ---------------------------------------------------------------- figures
def compute(d):
    fig = {"areas": AREAS, "providers": {a: list(d["provider"][a]) for a in AREAS}}
    exact = {w: census(d, "bg_hu", w) for w in ("60", "75")}
    fig["counts"] = {w: {a: r10(exact[w][a]) for a in AREAS} for w in exact}
    fig["exact"] = {w: {a: round(exact[w][a], 3) for a in AREAS} for w in exact}
    fig["edge"] = {w: {a: round(5.0 - abs(exact[w][a] - r10(exact[w][a])), 3) for a in AREAS} for w in exact}
    fig["county"] = {"60": _ages(d["county"], AGE60), "75": _ages(d["county"], AGE75)}
    fig["county_rounded"] = {w: r10(fig["county"][w]) for w in fig["county"]}
    fig["routes"] = {r: {w: {a: r10(census(d, r, w)[a]) for a in AREAS} for w in ("60", "75")}
                     for r in ("block_sum", "bg_points", "bg_pop", "tract_hu", "bg_hu")}
    cut = cut_groups(d)
    whole = len({g[:12] for g in d["area"]}) - len(cut)
    rows = []
    for u, blocks in cut.items():
        areas = sorted({d["area"][g] for g in blocks}, key=AREAS.index)
        town, rural = areas[0], areas[-1]
        hu = {a: sum(d["hu"][g] for g in blocks if d["area"][g] == a) for a in areas}
        c60, c75 = _ages(d["bg"][u], AGE60), _ages(d["bg"][u], AGE75)
        part = lambda c, a: c * hu[a] / float(hu[town] + hu[rural])
        blk = lambda k, a: sum(d["block"][g][k] for g in blocks if d["area"][g] == a)
        rows.append({"bg": u, "tract": u[5:11], "town": town, "rural": rural, "hu_town": hu[town],
                     "hu_rural": hu[rural], "c60": c60, "c75": c75, "p60_town": part(c60, town),
                     "p60_rural": part(c60, rural), "p75_town": part(c75, town), "p75_rural": part(c75, rural),
                     "blk60_rural": blk(0, rural), "blk75_rural": blk(1, rural)})
    fig["cut"] = rows
    fig["n_cut"], fig["n_whole"] = len(rows), whole
    fig["cut_60"] = sum(r["c60"] for r in rows)
    fig["cut_75"] = sum(r["c75"] for r in rows)
    fig["cut_rural_60"] = r10(sum(r["p60_rural"] for r in rows))
    fig["cut_rural_75"] = r10(sum(r["p75_rural"] for r in rows))
    fig["cut_rural_blocks_60"] = sum(r["blk60_rural"] for r in rows)
    fig["cut_rural_blocks_75"] = sum(r["blk75_rural"] for r in rows)
    fig["meals"] = meals(d)
    fig["active"] = active(d)
    fig["meals_total"] = sum(fig["meals"].values())
    fig["active_total"] = sum(fig["active"].values())
    fig["default_north_60"] = fig["routes"]["block_sum"]["60"]["North Kelvane"]
    fig["n_bg"] = len({g[:12] for g in d["area"]})
    fig["age_cuts"] = [int(sorted(LABEL60)[0].split()[0]), int(sorted(LABEL75)[0].split()[0])]
    fig["exact_parts"] = {"cut_rural_60": sum(r["p60_rural"] for r in rows),
                          "cut_rural_75": sum(r["p75_rural"] for r in rows)}
    return fig


# ---------------------------------------------------------------- the workbook
THIN = Side(style="thin", color="A6A6A6")


def write_xlsx(path, fig):
    wb = openpyxl.Workbook()
    head = PatternFill("solid", fgColor="DCE6E8")
    bold = Font(bold=True)
    note = Font(italic=True, size=9, color="595959")
    count = "#,##0"
    ws = wb.active
    ws.title = "Area plan table"
    ws["A1"] = "Kelvane Area Agency on Aging"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "FY2027 area plan update: provider areas' census-day counts and FY2026 home-delivered meal figures"
    ws["A3"] = "Planning, 16 October 2026"
    ws["A3"].font = note
    cols = ["Provider area", "Provider", "Residents aged 60 and over, 1 April 2020",
            "Residents aged 75 and over, 1 April 2020", "Home-delivered meals, October 2025 to September 2026",
            "Active home-delivered meal clients, 30 September 2026"]
    ws.append([])
    ws.append(cols)
    for c in ws[5]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    for a in AREAS:
        ws.append([a, fig["providers"][a][1], fig["counts"]["60"][a], fig["counts"]["75"][a], fig["meals"][a],
                   fig["active"][a]])
    ws.append(["Kelvane County", None, sum(fig["counts"]["60"].values()), sum(fig["counts"]["75"].values()),
               fig["meals_total"], fig["active_total"]])
    for c in ws[12]:
        c.font = bold
        c.border = Border(top=THIN)
    for row in ws.iter_rows(min_row=6, max_row=12, min_col=3, max_col=6):
        for c in row:
            c.number_format = count
    ws["A14"] = "Census counts to the nearest ten; meals and clients whole. Sources and method on the Notes sheet."
    ws["A14"].font = note
    for col, w in zip("ABCDEF", (17, 30, 15, 15, 17, 17)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[5].height = 62
    ws.freeze_panes = "A6"

    ws2 = wb.create_sheet("Cut block groups")
    ws2.append(["Block groups the provider area boundaries cut (areas as drawn since 1 July 2023)"])
    ws2["A1"].font = bold
    ws2.append([])
    hdr = ["Block group", "Tract", "Town side", "Rural side", "Housing units, town side", "Housing units, rural side",
           "Residents 60+", "60+ to town side", "60+ to rural side", "Residents 75+", "75+ to town side",
           "75+ to rural side"]
    ws2.append(hdr)
    for c in ws2[3]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in fig["cut"]:
        ws2.append([r["bg"], r["tract"], r["town"], r["rural"], r["hu_town"], r["hu_rural"], r["c60"],
                    round(r["p60_town"], 1), round(r["p60_rural"], 1), r["c75"], round(r["p75_town"], 1),
                    round(r["p75_rural"], 1)])
    for row in ws2.iter_rows(min_row=4, max_row=3 + len(fig["cut"]), min_col=5, max_col=12):
        for c in row:
            c.number_format = "#,##0.0" if c.column_letter in "HIKL" else count
    last = 4 + len(fig["cut"])
    ws2.cell(row=last, column=1, value="Total").font = bold
    sums = [sum(r[k] for r in fig["cut"]) for k in ("hu_town", "hu_rural", "c60")] + \
        [round(sum(round(r[k], 1) for r in fig["cut"]), 1) for k in ("p60_town", "p60_rural")] + \
        [sum(r["c75"] for r in fig["cut"])] + \
        [round(sum(round(r[k], 1) for r in fig["cut"]), 1) for k in ("p75_town", "p75_rural")]
    for col, v in zip(range(5, 13), sums):
        letter = openpyxl.utils.get_column_letter(col)
        c = ws2.cell(row=last, column=col, value=v)
        c.font = bold
        c.number_format = "#,##0.0" if letter in "HIKL" else count
    ws2.cell(row=last + 2, column=1, value="Each cut block group's counts split by its blocks' census-day housing "
                                           "units (H1) on each side of the boundary.").font = note
    for col, w in zip("ABCDEFGHIJKL", (15, 9, 16, 14, 11, 11, 10, 10, 10, 10, 10, 10)):
        ws2.column_dimensions[col].width = w
    ws2.row_dimensions[3].height = 46
    ws2.freeze_panes = "A4"

    ws3 = wb.create_sheet("Notes")
    notes = [
        ("Census counts", "2020 Census DHC table P12 for block groups (dhc2020_kelvane_block_groups_p12.csv), residents "
                          "in households and group quarters. A block group wholly inside one provider area goes to "
                          "that area whole; the %d block groups the boundaries cut are split by their blocks' "
                          "census-day housing units (dhc2020_kelvane_blocks_h1.csv). Each area's count is rounded "
                          "once to the nearest ten." % fig["n_cut"]),
        ("Provider areas", "provider_area_blocks.csv, the row in force for each block (effective 1 July 2023 for the "
                           "blocks the 2023 redraw moved); TRACT_BLOCK read as ten digits."),
        ("Why block groups", "The release's block counts were noise-infused and then made non-negative and consistent "
                             "with their block group, which lifts the sparse blocks on the rural side of a cut group "
                             "and lowers the dense town blocks; adding blocks carries that into the area counts. The "
                             "block groups' own counts and the housing units, which the release holds exact, do not."),
        ("Meals", "hdm_route_delivery_log_fy2026.csv, delivery dates 1 October 2025 to 30 September 2026. Rows a tablet "
                  "sent again for the same client, day and item are counted once, except a client's second hot meal "
                  "on the two-meal plan (meals_per_day in the roster); packs at the meals they hold "
                  "(hdm_item_codes.csv); each meal under the provider of the client's home area, whichever route "
                  "carried it."),
        ("Active clients", "Episodes open on 30 September 2026 (hdm_service_episodes_2026-10-09.csv), less clients the "
                           "state's death match shows died on or before that day, under their current registry "
                           "number or an earlier number the registry links to it; by the provider of the client's "
                           "home area."),
    ]
    ws3.column_dimensions["A"].width = 18
    ws3.column_dimensions["B"].width = 100
    for k, (h, t) in enumerate(notes, 1):
        ws3.cell(row=k, column=1, value=h).font = bold
        c = ws3.cell(row=k, column=2, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws3.cell(row=k, column=1).alignment = Alignment(vertical="top")
    wb.save(path)


def main(target, gdir, fig_path):
    import postprocess as PP
    import world as W
    os.makedirs(gdir, exist_ok=True)
    d = load(target)
    fig = compute(d)
    path = os.path.join(gdir, XLSX)
    write_xlsx(path, fig)
    PP.normalize_ooxml(path, W.PEOPLE["planning"], W.PEOPLE["aging"], "2026-10-14T14:12:00Z",
                       "2026-10-16T20:47:31Z", excel=True, company=W.OFFICE)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
    return fig
