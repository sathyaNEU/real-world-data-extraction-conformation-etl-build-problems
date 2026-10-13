"""Rindal County Public Health's West Nile virus case log for 2026, as the county epidemiologist shared it with the
district on Monday 17 August: every notification to date, with the residence section and the zone she keeps for each
case from the zone list the district sent her in March 2025."""
import datetime as dt

import world as W

LOG = "WNV_human_case_log_2026.xlsx"
D = dt.date

# locally acquired symptomatic cases: (2026 zone, residence (x, y) or None to draw, onset window, presentation)
CASES = [
    ("Coulee Hills", None, (D(2026, 6, 28), D(2026, 7, 6)), "Fever"),
    ("Coulee Hills", None, (D(2026, 7, 3), D(2026, 7, 11)), "Neuroinvasive"),
    ("Coulee Hills", None, (D(2026, 7, 7), D(2026, 7, 14)), "Fever"),
    ("Coulee Hills", None, (D(2026, 7, 10), D(2026, 7, 17)), "Neuroinvasive"),
    ("Coulee Hills", None, (D(2026, 7, 13), D(2026, 7, 20)), "Fever"),
    ("Coulee Hills", None, (D(2026, 7, 16), D(2026, 7, 22)), "Fever"),
    ("Coulee Hills", None, (D(2026, 7, 19), D(2026, 7, 25)), "Neuroinvasive"),
    ("South Prairie", (13, 3), (D(2026, 7, 18), D(2026, 7, 24)), "Fever"),
    ("South Prairie", (14, 2), (D(2026, 7, 22), D(2026, 7, 29)), "Neuroinvasive"),
    ("South Prairie", None, (D(2026, 7, 27), D(2026, 8, 2)), "Fever"),
    ("South Prairie", None, (D(2026, 8, 1), D(2026, 8, 6)), "Fever"),
    ("Riverside South", (19, 8), (D(2026, 7, 26), D(2026, 8, 1)), "Neuroinvasive"),
    ("Riverside South", (22, 10), (D(2026, 7, 30), D(2026, 8, 5)), "Fever"),
    ("Riverside South", None, (D(2026, 8, 2), D(2026, 8, 7)), "Fever"),
    ("North Bottoms", (19, 15), (D(2026, 7, 12), D(2026, 7, 19)), "Fever"),
    ("North Bottoms", None, (D(2026, 7, 23), D(2026, 7, 30)), "Neuroinvasive"),
    ("North Bottoms", None, (D(2026, 7, 31), D(2026, 8, 5)), "Fever"),
    ("Old Town", None, (D(2026, 7, 26), D(2026, 8, 1)), "Neuroinvasive"),
    ("Old Town", None, (D(2026, 7, 30), D(2026, 8, 4)), "Fever"),
    ("Westbrook", (13, 14), (D(2026, 8, 1), D(2026, 8, 5)), "Fever"),
    ("Westbrook", None, (D(2026, 8, 3), D(2026, 8, 7)), "Neuroinvasive"),
    ("Maple Ridge", (8, 18), (D(2026, 6, 22), D(2026, 6, 29)), "Fever"),
    ("Maple Ridge", (9, 17), (D(2026, 7, 8), D(2026, 7, 15)), "Fever"),
    ("Airport East", None, (D(2026, 7, 20), D(2026, 7, 27)), "Fever"),
    ("Airport East", None, (D(2026, 7, 29), D(2026, 8, 4)), "Neuroinvasive"),
]
# presumptive viremic blood donors (asymptomatic, found by blood-bank screening): zone, donation window
DONORS = [("Westbrook", (D(2026, 7, 28), D(2026, 8, 3))), ("South Prairie", (D(2026, 7, 21), D(2026, 7, 27))),
          ("North Bottoms", (D(2026, 8, 4), D(2026, 8, 8)))]
# residents infected on trips; two late-May onsets reported in June; suspected cases ruled out on convalescent serum;
# patients admitted in Lindgaard County and notified there too (zone, index of the zone's case)
TRAVEL = [("Old Town", (D(2026, 7, 24), D(2026, 7, 29)), "Travel: Minnesota (lake cabin, 18 to 25 July)"),
          ("Maple Ridge", (D(2026, 7, 12), D(2026, 7, 16)), "Travel: Montana (river trip, 4 to 11 July)")]
MAY = [("Coulee Hills", D(2026, 5, 27), D(2026, 6, 4)), ("South Prairie", D(2026, 5, 30), D(2026, 6, 9))]
RULED_OUT = [("Maple Ridge", (D(2026, 7, 20), D(2026, 7, 26))), ("Riverside South", (D(2026, 7, 27), D(2026, 8, 2))),
             ("Airport East", (D(2026, 7, 6), D(2026, 7, 12)))]
DUPLICATES = [("Coulee Hills", 3), ("Westbrook", 1)]

AGE = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]


def _pick_section(g, zone, used, res):
    cand = [(xy, n) for xy, n in sorted(res.items()) if W.zone2026(*xy) == zone and xy not in W.MOVED_2025
            and xy not in used]
    w = [n for _, n in cand]
    tot = float(sum(w))
    i = int(g.choice(len(cand), p=[x / tot for x in w]))
    return cand[i][0]


def _day(g, lo, hi):
    return lo + dt.timedelta(days=int(g.integers(0, (hi - lo).days + 1)))


def build():
    """Every row of the log, with the truth fields the checks need (prefixed by an underscore)."""
    res = W.residents()
    g = W.rng("cases")
    used = set()
    rows = []
    for k, (zone, xy, (lo, hi), pres) in enumerate(CASES):
        if xy is None:
            xy = _pick_section(g, zone, used, res)
        used.add(xy)
        onset = _day(g, lo, hi)
        rep = min(onset + dt.timedelta(days=int(g.integers(6, 13))), D(2026, 8, 14))
        rows.append(dict(_kind="case", _zone=zone, _xy=xy, onset=onset, event=onset, report=rep, pres=pres,
                         exposure="Rindal County", age=AGE[int(g.integers(1, 7))], sex="FM"[int(g.integers(0, 2))],
                         by=W.HEALTH, cls="Confirmed" if pres == "Neuroinvasive" or g.random() < 0.6 else "Probable"))
    for zone, (lo, hi) in DONORS:
        xy = _pick_section(g, zone, used, res)
        used.add(xy)
        don = _day(g, lo, hi)
        rows.append(dict(_kind="donor", _zone=zone, _xy=xy, onset=None, event=don, report=don + dt.timedelta(days=5),
                         pres="Asymptomatic blood donor", exposure="Rindal County", age=AGE[int(g.integers(0, 5))],
                         sex="FM"[int(g.integers(0, 2))], by=W.HEALTH, cls="Presumptive viremic donor"))
    for zone, (lo, hi), exp in TRAVEL:
        xy = _pick_section(g, zone, used, res)
        used.add(xy)
        onset = _day(g, lo, hi)
        rows.append(dict(_kind="travel", _zone=zone, _xy=xy, onset=onset, event=onset,
                         report=onset + dt.timedelta(days=9), pres="Fever", exposure=exp, age=AGE[int(g.integers(1, 5))],
                         sex="FM"[int(g.integers(0, 2))], by=W.HEALTH, cls="Confirmed"))
    for zone, (lo, hi) in RULED_OUT:
        xy = _pick_section(g, zone, used, res)
        used.add(xy)
        onset = _day(g, lo, hi)
        rows.append(dict(_kind="ruled_out", _zone=zone, _xy=xy, onset=onset, event=onset,
                         report=onset + dt.timedelta(days=int(g.integers(5, 9))), pres="Fever", exposure="Rindal County",
                         age=AGE[int(g.integers(0, 6))], sex="FM"[int(g.integers(0, 2))], by=W.HEALTH, cls="Not a case",
                         note="IgM negative on convalescent serum"))
    for zone, onset, specimen in MAY:
        xy = _pick_section(g, zone, used, res)
        used.add(xy)
        rows.append(dict(_kind="may", _zone=zone, _xy=xy, onset=onset, event=specimen,
                         report=specimen + dt.timedelta(days=4), pres="Fever", exposure="Rindal County",
                         age=AGE[int(g.integers(2, 6))], sex="FM"[int(g.integers(0, 2))], by=W.HEALTH, cls="Probable",
                         note="Onset from interview on %s" % (specimen + dt.timedelta(days=11)).strftime("%m/%d")))
    dups = []
    for zone, i in DUPLICATES:
        src = [r for r in rows if r["_kind"] == "case" and r["_zone"] == zone][i]
        dup = dict(src)
        dup.update(_kind="duplicate", _src=id(src), by=W.NEIGHBOUR_HEALTH, report=src["report"] - dt.timedelta(days=2),
                   note="Admitted in Lindgaard County")
        dups.append((dup, src))
    rows += [d for d, _ in dups]
    # state case IDs in order of first report; the duplicate shares its patient's ID
    order = sorted(range(len(rows)), key=lambda i: (rows[i]["report"], i))
    sid = {}
    n = 101
    for i in order:
        r = rows[i]
        if r["_kind"] == "duplicate":
            continue
        sid[id(r)] = "ND-26-%04d" % n
        n += 7 + (i % 5)
    for r in rows:
        if r["_kind"] != "duplicate":
            r["state_id"] = sid[id(r)]
    for d, src in dups:
        d["state_id"] = src["state_id"]
    for r in rows:
        r["section"] = W.section_label(*r["_xy"])
        r["label"] = W.zone2025(*r["_xy"])
    rows.sort(key=lambda r: (r["report"], r["state_id"], r["by"]))
    for k, r in enumerate(rows, 1):
        r["log_no"] = k
    return rows


def truth(rows):
    """Locally acquired symptomatic cases with onset 1 June to 15 August, one per patient, by 2026 zone."""
    seen = set()
    out = {z: [] for z in W.ZONES}
    for r in rows:
        if r["pres"] == "Asymptomatic blood donor" or r["exposure"] != "Rindal County" or r["onset"] is None or \
                r["cls"] == "Not a case":
            continue
        if not (W.SEASON_2026[0] <= r["onset"] <= W.SEASON_2026[1]):
            continue
        if r["state_id"] in seen:
            continue
        seen.add(r["state_id"])
        out[W.zone2026(*r["_xy"])].append(r["onset"])
    return out


def write(path, rows):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Cases"
    head = ["Log no", "State case ID", "Notified by", "Report date", "Event date", "Onset date", "Classification",
            "Clinical presentation", "Age group", "Sex", "Residence section", "Zone", "Exposure", "Notes"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([r["log_no"], r["state_id"], r["by"], r["report"], r["event"], r["onset"], r["cls"], r["pres"],
                   r["age"], r["sex"], r["section"], r["label"], r["exposure"], r.get("note") or None])
    for row in ws.iter_rows(min_row=2):
        for c in row[3:6]:
            c.number_format = "mm/dd/yyyy"
    widths = [7, 13, 34, 11, 11, 11, 24, 24, 9, 5, 16, 15, 44, 52]
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"
    rd = wb.create_sheet("Read me")
    lines = [
        "West Nile virus human case log, 2026 (working copy)",
        "Kept by %s, %s. Shared weekly with %s." % (W.PEOPLE["epi"][0], W.PEOPLE["epi"][1], W.DISTRICT),
        "",
        "One row per notification received. A patient notified by two health departments has two rows with one state "
        "case ID.",
        "Event date: the date the case is counted under for state reporting: the onset date when known at "
        "notification, otherwise the specimen collection date; for a blood donor, the donation date.",
        "Onset date: the date symptoms began, from the case interview.",
        "Clinical presentation: Neuroinvasive, Fever, or Asymptomatic blood donor (a presumptive viremic donor found "
        "by blood-bank screening).",
        "Residence section: public land survey section of the residence (township, range, section).",
        "Zone: the vector control district zone of the residence section, from the district's zone list of March "
        "2025.",
        "Classification: Confirmed or Probable under the national surveillance case definition, both reported as "
        "cases; Presumptive viremic donor, reported apart and not a case; Not a case (a notification ruled out on "
        "further testing).",
        "Exposure: Rindal County, or the place of travel where infection was likely acquired.",
    ]
    for ln in lines:
        rd.append([ln or None])
    rd.column_dimensions["A"].width = 120
    wb.save(path)
