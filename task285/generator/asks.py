"""task285 ask worlds: the address register and the 2022 floor survey (ask 1), the July 2021 closures (ask 2),
the 2026 Flood Ready ledger (ask 3). Clean truth plus the records each system writes. Deterministic.
"""
import math
import random
from datetime import datetime, timedelta

import world as W

R = random.Random(W.SEED * 7 + 1)

STREETS = ["Main Street", "Church Lane", "Mill Lane", "Beck Side", "Green Lane", "Station Road", "The Green",
           "Back Lane", "Low Road", "High Street", "Water Lane", "Bridge End", "Holme Lane", "Ings Lane",
           "School Lane", "Croft Road", "Kirk Gate", "West End", "Garth Close", "Ferry Lane", "Riverside",
           "Sandholme", "Carr Lane", "Willow Bank", "Dale View", "Fold Lane", "Moor View", "Cross Lane"]
POSTCODE_AREA = "HB"
FLOOD_PARISHES = {  # parish -> share of its dwellings set in the storage area nearest its village
    "Hollinside": 0.55, "Ravelsby Bridge": 0.48, "Lunnerby": 0.41, "Whinnerby": 0.18, "Yarrowcote": 0.26,
    "Hepplewick": 0.31, "Tolmarsh": 0.22, "Burnishaw": 0.14, "Cottergill": 0.62, "Upper Quarnell": 0.11,
    "Hawkesbridge South": 0.07, "Nettlecote": 0.06, "Wrennick": 0.12, "Quernby Moor": 0.09, "Highfold": 0.16,
    "Hawkesbridge North": 0.03, "Owlthwaite": 0.05,
}
# parishes whose riverside dwellings carry levels from the 2008 riverside survey (Quarnell Navigation Datum)
SURV08 = {"Whinnerby", "Yarrowcote", "Hepplewick", "Tolmarsh", "Cottergill", "Hawkesbridge South", "Upper Quarnell",
          "Burnishaw", "Nettlecote", "Quernby Moor", "Wrennick", "Hawkesbridge North", "Hollinside", "Owlthwaite"}
BLOCKS = {"Hawkesbridge South": 5, "Hepplewick": 2, "Cottergill": 1, "Yarrowcote": 1, "Hollinside": 1,
          "Ravelsby Bridge": 1, "Lunnerby": 1, "Whinnerby": 1, "Tolmarsh": 1, "Burnishaw": 1, "Hawkesbridge North": 2,
          "Highfold": 1}
NONRES = ["CR01", "CR02", "CO01", "CC04", "CI01", "CR11", "CL06", "CZ01"]
# each parish's address stream, by parish code
PARISH_STREAM = {"E04014101": 1035, "E04014102": 1250, "E04014103": 851, "E04014104": 818, "E04014105": 1261, "E04014106": 939, "E04014107": 816, "E04014108": 1133, "E04014109": 936, "E04014110": 964, "E04014111": 607, "E04014112": 727, "E04014113": 805, "E04014114": 795, "E04014115": 684, "E04014116": 1154, "E04014117": 1787, "E04014118": 1795}


def _uprn(i):
    return 100051000000 + 37 * i + (i * i) % 29 + (i % 7) * 3


def village_sa(parish):
    node = W.PARISH_NODE[parish]
    x, y = W.NODES[node]
    return W.sa_at(x, y)


def nearest_sa_for(parish):
    """storage area holding the parish's riverside or beckside dwellings."""
    sa = village_sa(parish)
    if sa:
        return sa
    x, y = W.NODES[W.PARISH_NODE[parish]]
    best = None
    for s, poly in W.SA_POLY.items():
        cx = sum(p[0] for p in poly) / 4
        cy = sum(p[1] for p in poly) / 4
        d = (cx - x) ** 2 + (cy - y) ** 2
        if best is None or d < best[0]:
            best = (d, s)
    return best[1]


def point_in(sa, rnd):
    poly = W.SA_POLY[sa]
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    for _ in range(200):
        x, y = rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys))
        if W.in_poly(x, y, poly):
            return x, y
    return sum(xs) / 4, sum(ys) / 4


def build_register():
    """Every address: dict rows (truth fields prefixed t_)."""
    rows = []
    i = 0
    for code, parish, node, dw in W.PARISHES:
        rnd = random.Random(PARISH_STREAM[code] * 131 + W.SEED)
        vx, vy = W.NODES[node]
        spread = 1.4 if parish.startswith("Hawkesbridge") else 0.55
        share = FLOOD_PARISHES.get(parish, 0.0)
        sa_f = nearest_sa_for(parish) if share else None
        n_blocks = BLOCKS.get(parish, 0)
        # dwellings close to the council tax count, the register running a little over (new builds, empties)
        target = dw + rnd.randint(-6, 14)
        streets = rnd.sample(STREETS, 9 if spread < 1 else 22)
        out_code = "%s%d" % (POSTCODE_AREA, 2 + (int(code[-2:]) % 7))
        blocks_left = n_blocks
        made = 0
        k = 0
        while made < target:
            k += 1
            in_flood = sa_f is not None and rnd.random() < share
            if in_flood:
                x, y = point_in(sa_f, rnd)
                if math.hypot(x - vx, y - vy) > 2.5:
                    x, y = vx + rnd.uniform(-0.3, 0.3), vy + rnd.uniform(-0.3, 0.3)
                    if W.sa_at(x, y) != sa_f:
                        in_flood = False
            else:
                for _ in range(50):
                    x, y = vx + rnd.gauss(0, spread), vy + rnd.gauss(0, spread)
                    if W.sa_at(x, y) is None:
                        break
            x, y = round(x, 3), round(y, 3)
            sa = W.sa_at(x, y)
            peak = W.peak_stage(sa) if sa else None
            # true ground level (mAOD, ODN): floodplain dwellings sit near the peak, others on higher ground
            if sa:
                ground = round(peak - rnd.uniform(-0.55, 1.35), 2)
                # no dwelling sits exactly at the peak: a floor within a centimetre of it is moved off it
                for off in (W.DEFAULT_THRESHOLD, 0.08, 0.12, 0.2, 0.25, 0.3, 0.35, 0.4):
                    if abs(ground + off - peak) < 0.012:
                        ground = round(ground + 0.03, 2)
            else:
                ground = round(46.0 + 0.9 * (vy - 0.5) * 3 - 0.35 * vx + rnd.uniform(0, 6), 2)
            street = streets[k % len(streets)] if rnd.random() < 0.8 else rnd.choice(streets)
            pc = "%s %d%s%s" % (out_code, rnd.randint(1, 9), chr(65 + rnd.randint(0, 25)), chr(65 + rnd.randint(0, 25)))
            src = "LIDAR19"
            r = rnd.random()
            if sa and parish in SURV08 and r < 0.46:
                src = "SURV08"
            elif r < 0.08:
                src = "GPS16"
            elif r < 0.16:
                src = "SURV11"
            elif r < 0.27:
                src = "LIDAR19-I"
            built = 2025 if rnd.random() < 0.025 else rnd.choice([1890, 1925, 1958, 1972, 1986, 2003, 2014])
            if blocks_left and sa and rnd.random() < 0.08:
                # a block of flats: parent shell plus children, two to four floors, two to four flats a floor
                blocks_left -= 1
                floors = rnd.randint(2, 4)
                per = rnd.randint(2, 4)
                parent = _uprn(i); i += 1
                bname = rnd.choice(["Mill House", "Riverside Court", "Beck View", "Granary Wharf", "Holme Court",
                                    "Ferry House", "Quarnell Court", "Weir View"])
                bno = rnd.randint(2, 60)
                thr = round(rnd.uniform(0.12, 0.42), 2)
                if abs(ground + thr - peak) < 0.012:
                    thr = round(thr + 0.03, 2)
                rows.append(dict(uprn=parent, parent=None, cls="PP", sao="", pao="%s" % bname, street=street,
                                 parish=parish, code=code, x=x, y=y, ground=ground, src=src, built=built,
                                 t_floor=None, t_sa=sa, t_dwelling=False, block=parent, flat_floor=None, pc=pc))
                n_flat = 0
                for f in range(floors):
                    for u in range(per):
                        n_flat += 1
                        fu = _uprn(i); i += 1
                        rows.append(dict(uprn=fu, parent=parent, cls="RD06", sao="FLAT %d" % n_flat, pao=bname,
                                         street=street, parish=parish, code=code, x=x, y=y, ground=ground, src=src,
                                         built=built, t_floor=round(ground + thr + 2.9 * f, 2), t_sa=sa,
                                         t_dwelling=True, block=parent, flat_floor=f, pc=pc))
                        made += 1
                continue
            if rnd.random() < 0.075:
                cls = rnd.choice(NONRES)
                dwelling = False
            else:
                cls = rnd.choices(["RD02", "RD03", "RD04", "RD08", "RD03"], [30, 28, 34, 4, 2])[0]
                dwelling = True
            thr = round(rnd.uniform(0.08, 0.40), 2)
            if sa and abs(ground + thr - peak) < 0.012:
                thr = round(thr + 0.03, 2)
            no = rnd.randint(1, 140)
            rows.append(dict(uprn=_uprn(i), parent=None, cls=cls, sao="", pao=str(no), street=street, parish=parish,
                             code=code, x=x, y=y, ground=ground, src=src, built=built,
                             t_floor=round(ground + thr, 2), t_sa=sa, t_dwelling=dwelling, block=None, flat_floor=None,
                             pc=pc))
            i += 1
            if dwelling:
                made += 1
    # Hawkesbridge West merged into Hawkesbridge North (April 2025): some records keep the old code
    rnd = random.Random(W.SEED + 19)
    for r_ in rows:
        if r_["parish"] == "Hawkesbridge North" and rnd.random() < 0.31:
            r_["code_shown"] = W.OLD_PARISH[0]
        else:
            r_["code_shown"] = r_["code"]
    # register ground level as recorded: SURV08 on Quarnell Navigation Datum (0.42 below ODN)
    for r_ in rows:
        r_["ground_rec"] = round(r_["ground"] - W.DATUM_SHIFT, 2) if r_["src"] == "SURV08" else r_["ground"]
    return rows


def build_survey(rows):
    """2022 property flood resilience survey: houses by UPRN, blocks by parent UPRN with ground-floor flats."""
    rnd = random.Random(W.SEED + 22)
    rg = random.Random(W.SEED + 23)    # the surveyors' own ground levels (GNSS, to Ordnance Datum Newlyn)

    def g_meas(g):
        return round(g + max(-0.07, min(0.07, rg.gauss(0, 0.03))), 2)
    out = []
    n = 0
    blocks = {}
    for r_ in rows:
        if r_["block"] is not None and r_["cls"] == "RD06":
            blocks.setdefault(r_["block"], []).append(r_)
    for r_ in rows:
        if r_["t_sa"] is None or r_["built"] >= 2023:
            continue
        if r_["cls"] == "PP":
            kids = blocks[r_["uprn"]]
            ground_kids = [k for k in kids if k["flat_floor"] == 0]
            n += 1
            out.append(dict(ref="PFR22-%04d" % (1000 + 7 * n + n % 5), uprn=r_["uprn"], addr="%s, %s" % (r_["pao"], r_["street"]),
                            parish=r_["parish"], floor=ground_kids[0]["t_floor"], ground=g_meas(r_["ground"]),
                            units=", ".join(k["sao"].title() for k in ground_kids), storeys=len(set(k["flat_floor"] for k in kids)),
                            surveyed=datetime(2022, 3, 1) + timedelta(days=rnd.randint(0, 200))))
        elif r_["t_dwelling"] and r_["cls"] != "RD06" and rnd.random() < 0.58:
            n += 1
            out.append(dict(ref="PFR22-%04d" % (1000 + 7 * n + n % 5), uprn=r_["uprn"], addr="%s %s" % (r_["pao"], r_["street"]),
                            parish=r_["parish"], floor=r_["t_floor"], ground=g_meas(r_["ground"]), units="",
                            storeys=rnd.choice([1, 2, 2, 2, 3]),
                            surveyed=datetime(2022, 3, 1) + timedelta(days=rnd.randint(0, 200))))
    return out


def ask1_golden(rows, survey):
    """dwellings per parish whose floor level is below their storage area's 2025 peak stage."""
    floor = {s["uprn"]: s["floor"] for s in survey}
    units = {s["uprn"]: set(u.strip().upper() for u in s["units"].split(",") if u.strip()) for s in survey if s["units"]}
    out = {}
    for r_ in rows:
        if not r_["t_dwelling"] or r_["t_sa"] is None:
            continue
        pk = W.peak_stage(r_["t_sa"])
        if r_["cls"] == "RD06":
            if r_["sao"].upper() not in units.get(r_["block"], set()):
                continue
            fl = floor[r_["block"]]
        else:
            fl = floor.get(r_["uprn"], r_["ground"] + W.DEFAULT_THRESHOLD)
        if pk > fl:
            out[r_["parish"]] = out.get(r_["parish"], 0) + 1
    return out


# ---------------------------------------------------------------------------------------------- ask 2
SECTIONS = [  # section id, road, location, barrier windows (local BST datetimes), police closure (UTC) or None
    ("HW21-07-01", "B5131", "Hollin Beck, Hollinside", [("2021-07-18 04:41", "2021-07-18 16:12"), ("2021-07-18 05:06", "2021-07-18 16:37")], ("2021-07-18 02:52", "2021-07-18 05:10")),
    ("HW21-07-02", "B5131", "Ravelsby Brook, Ravelsby Bridge", [("2021-07-18 06:20", "2021-07-18 12:08"), ("2021-07-18 13:01", "2021-07-18 19:31")], None),
    ("HW21-07-03", "B5131", "Lunnerby Beck, Lunnerby", [("2021-07-18 07:15", "2021-07-18 19:30"), ("2021-07-18 07:38", "2021-07-18 19:52")], ("2021-07-18 03:56", "2021-07-18 07:02")),
    ("HW21-07-04", "C2041", "Whinnerby Lane ford", [("2021-07-18 05:48", "2021-07-18 09:58")], ("2021-07-18 03:57", "2021-07-18 06:35")),
    ("HW21-07-05", "U4108", "Highfold Road, Cote Bridge", [("2021-07-18 06:02", "2021-07-18 09:47"), ("2021-07-18 10:31", "2021-07-18 12:47")], None),
    ("HW21-07-06", "C2045", "Hepplewick Road, Mill Bridge", [("2021-07-18 08:40", "2021-07-18 15:16"), ("2021-07-18 09:05", "2021-07-18 15:31")], ("2021-07-18 06:24", "2021-07-18 08:12")),
    ("HW21-07-07", "C2043", "Yarrowcote Road, Ings Bend", [("2021-07-18 09:12", "2021-07-18 15:55"), ("2021-07-18 16:40", "2021-07-18 21:53")], ("2021-07-18 07:20", "2021-07-18 09:30")),
    ("HW21-07-08", "C2047", "Tolmarsh Lane, Ford Bridge", [("2021-07-18 10:20", "2021-07-18 12:19")], ("2021-07-18 08:10", "")),
    ("HW21-07-09", "U4105", "Nettlecote Lane, Nettle Gill", [("2021-07-18 07:55", "2021-07-18 11:10"), ("2021-07-18 12:40", "2021-07-18 16:31")], None),
]


# the B5131 route closure, signed at both ends, over the three B5131 sections
ROUTE = ("HW21-07-10", "B5131", "Hollinside to Lunnerby", ("2021-07-18 05:40", "2021-07-18 20:41"),
         ("HW21-07-01", "HW21-07-02", "HW21-07-03"))

# a re-closure keyed by the duty officer to the closure reference of the previous entry in the log
REKEYED = {("HW21-07-07", 1): "HW21-07-06", ("HW21-07-05", 1): "HW21-07-04", ("HW21-07-09", 1): "HW21-07-08"}


def _dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def ask2_golden():
    out = {}
    for sid, road, loc, bars, pol in SECTIONS:
        spans = [(_dt(a), _dt(b)) for a, b in bars]
        if sid in ROUTE[4]:
            spans.append((_dt(ROUTE[3][0]), _dt(ROUTE[3][1])))
        if pol:
            # a police closure with no recorded opening ran until the highways barrier took it over
            end = _dt(pol[1]) + timedelta(hours=1) if pol[1] else min(_dt(a) for a, b in bars)
            spans.append((_dt(pol[0]) + timedelta(hours=1), end))
        spans.sort()
        merged = []
        for a, b in spans:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        out[sid] = sum((b - a).total_seconds() for a, b in merged) / 3600.0
    return out


# ---------------------------------------------------------------------------------------------- ask 3
AWARDS_2026 = [  # parish, award ref, award, variation (amount, ref) or None, payments: (date, method, amount, cheque or None)
    ("Hollinside", "FR26-003", 4200, None, [("2026-03-11", "BACS", 2940, None), ("2026-09-02", "BACS", 840, None)]),
    ("Ravelsby Bridge", "FR26-005", 3850, (650, "FR26-005-V1"), [("2026-03-11", "BACS", 3080, None), ("2026-07-21", "BACS", 650, None)]),
    ("Lunnerby", "FR26-007", 5600, None, [("2026-03-18", "CHQ", 4480, "004817")]),
    ("Whinnerby", "FR26-008", 2950, None, [("2026-03-18", "BACS", 2360, None), ("2026-09-30", "BACS", 295, None)]),
    ("Yarrowcote", "FR26-010", 3400, (900, "FR26-010-V1"), [("2026-04-02", "BACS", 2720, None), ("2026-08-14", "CHQ", 900, "004903")]),
    ("Burnishaw", "FR26-012", 4750, None, [("2026-04-02", "BACS", 3800, None), ("2026-10-06", "BACS", 712, None)]),
    ("Hepplewick", "FR26-013", 3100, None, [("2026-04-09", "CHQ", 2480, "004829")]),
    ("Tolmarsh", "FR26-015", 2600, (400, "FR26-015-V1"), [("2026-04-09", "BACS", 2080, None), ("2026-08-26", "BACS", 520, None)]),
    ("Cottergill", "FR26-016", 1850, None, [("2026-04-16", "BACS", 1480, None), ("2026-09-23", "BACS", 311, None)]),
    ("Wrennick", "FR26-018", 2300, None, [("2026-04-16", "BACS", 1840, None), ("2026-11-02", "BACS", 437, None)]),
    ("Upper Quarnell", "FR26-019", 2750, None, [("2026-04-23", "CHQ", 2200, "004861"), ("2026-10-14", "BACS", 418, None)]),
]
CANCELLED = {"004817", "004903"}       # stale cheques the bank returned and the Fund cancelled
# second instalments keyed to the parish's closed 2025 award reference
MISREF = {"Cottergill": "FR25-016", "Whinnerby": "FR25-009", "Tolmarsh": "FR25-014"}
# second instalments paid on the parish council's instruction to another payee, under the 2026 reference
PAYEE = {"Burnishaw": "P. Lees, Clerk to Burnishaw PC", "Hollinside": "Hollinside and District Village Hall",
         "Upper Quarnell": "Upper Quarnell Village Hall Committee"}


def ask3_golden():
    out = {}
    for parish, ref, amt, var, pays in AWARDS_2026:
        total = amt + (var[0] if var else 0)
        paid = sum(p[2] for p in pays if not (p[3] and p[3] in CANCELLED) and p[0] <= "2026-10-31")
        out[parish] = total - paid
    return out


if __name__ == "__main__":
    rows = build_register()
    sv = build_survey(rows)
    print(len(rows), "addresses", len(sv), "survey rows")
    print("ask1", ask1_golden(rows, sv))
    print("ask2", {k: round(v, 2) for k, v in ask2_golden().items()})
    print("ask3", ask3_golden())
