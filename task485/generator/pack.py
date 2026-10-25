"""Cut task485's pack from the world: the electoral management systems' property electorate reports (the old system's
for the 2021 and 2022 registers, the new system's for 2023 to 2026), the 2023 migration's property cross-reference,
the address register extract, the council's completions monitoring and housing trajectory, the 2024 polling district
review schedule and the ward list."""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment

import alterations as AL
import world as W

D = dt.date
REG_DATE = {Y: D(Y, 12, 1) for Y in range(2014, 2033)}
LLPG_DATE = D(2026, 10, 12)
MIGRATION = D(2022, 3, 7)                   # the new system live; Electra's last export ran on 4 March 2022
SWITCH_OFF = D(2022, 3, 4)
OLD_YEARS, NEW_YEARS = (2020, 2021), (2022, 2023, 2024, 2025)
REVIEW_YEAR = 2023                          # the 2023 polling district review takes effect on the 2023 register
TOWN = {"LAB": "Lorrimere", "LCA": "Lorrimere", "LNO": "Lorrimere", "LWE": "Lorrimere", "CCE": "Caldenstow",
        "CPK": "Caldenstow"}
CLASS_HOUSE = ["RD02", "RD03", "RD04"]       # detached, semi-detached, terraced
CLASS_FLAT = "RD06"                         # self-contained flat
CLASS_PARENT = "PP"                         # property shell (a building holding flats)


def _csv(path, header, rows, delim=",", crlf=True, pre=None):
    buf = io.StringIO()
    if pre:
        for line in pre:
            buf.write(line + ("\r\n" if crlf else "\n"))
    w = csv.writer(buf, delimiter=delim, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def month_date(mi, rng=None, day=None):
    y, m = W.ym(mi)
    if day is None:
        last = (D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
        day = int(rng.integers(1, last + 1)) if rng is not None else 15
    return D(y, m, day)


def attach(w, g, seed=W.SEED + 2):
    """the per-dwelling attributes every file reads: class, address line, postcode, in-use date, the old system's
    property reference, the new system's property id, overseas and attainer entries by register year"""
    rng = np.random.default_rng(seed)
    dw = w["dwellings"]
    blocks = g["blocks"]
    # postcodes: runs of about fifteen dwellings along a street
    pc_seq = {}
    sectors = {}
    for i, (c, n, cl, r, p) in enumerate(W.WARDS):
        sectors[c] = "LR%d" % (1 + i // 2)
    unit_letters = "ABDEFGHJLNPQRSTUWXYZ"
    for d in dw:
        key = (d["ward"], d["street"])
        pc_seq.setdefault(key, [])
    street_pc = {}
    used = set()
    for key in sorted(pc_seq):
        c, st = key
        n = sum(1 for d in dw if d["ward"] == c and d["street"] == st)
        units = []
        for _ in range(max(1, int(np.ceil(n / 15.0)))):
            for _t in range(500):
                pc = "%s %d%s%s" % (sectors[c], int(rng.integers(1, 10)), unit_letters[int(rng.integers(0, 20))],
                                    unit_letters[int(rng.integers(0, 20))])
                if pc not in used:
                    used.add(pc)
                    units.append(pc)
                    break
        street_pc[key] = units
    for d in dw:
        c = d["ward"]
        units = street_pc[(c, d["street"])]
        d["postcode"] = units[min(len(units) - 1, (d["number"] - 1) // 15 if d["block"] is None else 0)]
        town = TOWN.get(c, [x for x in W.WARDS if x[0] == c][0][1])
        if d["block"] is None:
            d["addr"] = "%d %s, %s" % (d["number"], d["street"], town)
            d["cls"] = CLASS_HOUSE[int(rng.integers(0, 3))] if d["site"] is None else ["RD02", "RD03", "RD04"][int(rng.choice(3, p=[.45, .4, .15]))]
        else:
            b = blocks[d["block"]]
            d["addr"] = "Flat %d, %s, %d %s, %s" % (d["flat"], b["name"], b["number"], d["street"], town)
            d["cls"] = CLASS_FLAT
        # the address register's in-use date: a settled dwelling's record from the register's load or its build;
        # a new dwelling's when it is first in use
        if d["site"] is None:
            d["inuse_date"] = D(int(rng.integers(1965, 2014)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            d["llpg_state_date"] = max(D(2003, 4, 1), d["inuse_date"])
        else:
            d["inuse_date"] = month_date(d["inuse"], rng)
            d["llpg_state_date"] = d["inuse_date"]
            d["done_date"] = month_date(d["done"], rng) if d["done"] <= W.mindex(*W.CUT) else None
            if d["done_date"] is not None and d["done_date"] > d["inuse_date"]:
                d["done_date"] = d["inuse_date"]
    # overseas electors registered at a qualifying address (settled stock) and attainers, by register year
    for d in dw:
        d["overseas"] = {}
        d["attainers"] = {}
    settled = [d for d in dw if d["site"] is None]
    for d in settled:
        if rng.random() < 0.012:
            start = int(rng.integers(2005, 2027))
            for Y in w["years"]:
                d["overseas"][Y] = 1 if Y >= start and rng.random() < 0.97 else 0
    for d in dw:
        eu = rng.random() < (0.03 if d["type"] == "house" else 0.07)
        d["eu"] = eu
        d["local_only"] = {}
        for Y in w["years"]:
            n = d["count"][Y]
            p = 0.045 if d["type"] == "house" else 0.012
            d["attainers"][Y] = 1 if (n >= 2 and rng.random() < p) else 0
            d["local_only"][Y] = n if eu else 0
    # system keys: the old system's property reference for every dwelling in use before the 2023 migration, the new
    # system's property id for every dwelling on its database
    refs = rng.choice(np.arange(100000, 999999), size=len(dw), replace=False)
    pids = rng.choice(np.arange(1000000, 9999999), size=len(dw), replace=False)
    for k, d in enumerate(dw):
        d["old_ref"] = int(refs[k]) if d["inuse_date"] <= SWITCH_OFF else None
        d["pid"] = "P%07d" % int(pids[k])
    return dict(street_pc=street_pc)


def ems_new(path, w):
    """the new system's property electorate report for the 2022 to 2025 registers: one row a property on its
    property database at each publication, in use by the register's last alteration"""
    rows = []
    for Y in NEW_YEARS:
        for d in w["dwellings"]:
            if d["inuse"] is not None and d["inuse"] > W.mindex(Y, 10):
                continue
            lg = d["count"][Y]
            pd = d["pd_new"] if Y >= REVIEW_YEAR else d["pd_old"]
            rows.append((REG_DATE[Y].isoformat(), pd, d["pid"], d["uprn"], d["addr"], d["postcode"], lg,
                         d["attainers"][Y], d["overseas"].get(Y, 0), d["local_only"][Y]))
    rows.sort(key=lambda r: (r[0], r[1], r[4]))
    _csv(path, ["register_date", "polling_district", "property_id", "uprn", "address", "postcode",
                "local_government_electors", "attainers", "overseas_electors", "local_franchise_only"], rows)
    return len(rows)


ELECTRA_TITLE = ["ELECTRA ELECTORAL MANAGEMENT SYSTEM", None, "LORRIMERE DISTRICT COUNCIL - ELECTORAL REGISTRATION OFFICER",
                 None, ""]


def ems_old(path, w, Y, idx=None, run="04/03/2022 17:52"):
    """the old system's property electorate report: a title block, then pipe-delimited rows by polling district and
    property reference, every entry counted in TOTAL with attainers and overseas electors broken out. The 2020
    register's report is from Electra's archive of it as published; the 2021 report is the register Electra held when
    it was switched off, with the notices of January to March 2022 applied"""
    pre = list(ELECTRA_TITLE)
    pre[1] = "PROPERTY ELECTORATE REPORT - REVISED REGISTER %s" % REG_DATE[Y].strftime("%d/%m/%Y")
    pre[3] = "RUN %s" % run
    rows = []
    live = idx is not None
    for k, d in enumerate(w["dwellings"]):
        if d["old_ref"] is None:
            continue
        if live:
            if d["inuse_date"] > SWITCH_OFF:
                continue
            lg, at, ov, lo = AL.held_at(w, idx, k, Y, SWITCH_OFF)
        else:
            if d["inuse"] is not None and d["inuse"] > W.mindex(Y, 10):
                continue
            lg, at, ov, lo = d["count"][Y], d["attainers"][Y], d["overseas"].get(Y, 0), d["local_only"][Y]
        rows.append((d["pd_old"], d["old_ref"], d["addr"].upper().replace(",", ""), d["postcode"], lg + at + ov, at, ov, lo))
    rows.sort(key=lambda r: (r[0], r[1]))
    _csv(path, ["PD", "PROPREF", "ADDRESS", "POSTCODE", "TOTAL", "ATTAINERS", "OVERSEAS", "LOCAL_ONLY"], rows,
         delim="|", pre=pre)
    return len(rows)


def _register_order(w):
    return sorted([k for k, d in enumerate(w["dwellings"]) if d["old_ref"] is not None],
                  key=lambda k: (w["dwellings"][k]["pd_old"], w["dwellings"][k]["street"], w["dwellings"][k]["number"],
                                 w["dwellings"][k].get("flat") or 0))


def _numbering(w, Y, order):
    """elector numbers on the register published 1 December Y: each polling district's entries numbered in street
    order, a property's electors first, then its attainers and overseas electors"""
    num, anchor, seq = {}, {}, {}
    ref = W.mindex(Y, 10)
    for k in order:
        d = w["dwellings"][k]
        if d["inuse"] is not None and d["inuse"] > ref:
            anchor[k] = "%s-%04d" % (d["pd_old"], seq.get(d["pd_old"], 0))
            continue
        pd = d["pd_old"]
        n = seq.get(pd, 0)
        for hi, h in enumerate(d["hh"]):
            if h.arrive <= ref < h.leave:
                for ai, a in enumerate(h.adults):
                    if a is not None and a <= Y:
                        n += 1
                        num[(k, hi, ai)] = "%s-%04d" % (pd, n)
        n += d["attainers"][Y] + d["overseas"].get(Y, 0)
        seq[pd] = n
        anchor[k] = "%s-%04d" % (pd, n)
    return num, anchor


def electra_notices(path, w, ev):
    """Electra's monthly notices of alteration from January 2021 to March 2022: one row an entry added to or deleted
    from the register, with the elector number it carries on the register"""
    order = _register_order(w)
    nums = {Y: _numbering(w, Y, order) for Y in (2020, 2021)}
    added, suffix = {}, {}
    rows = []
    for (k, act, day, mk, key, doa) in ev:
        nd = AL.notice_of(day)
        if nd is None:
            continue
        d = w["dwellings"][k]
        ry = day.year if day.month >= 11 else day.year - 1
        num, anchor = nums[ry]
        if act == "A":
            j = suffix.get((ry, k), 0) + 1
            suffix[(ry, k)] = j
            eno = "%s/%d" % (anchor[k], j)
            added[key] = eno
        else:
            eno = num.get(key) or added.get(key)
            assert eno is not None, key
        rows.append((nd.strftime("%d/%m/%Y"), d["pd_old"], eno, d["old_ref"], d["addr"].upper().replace(",", ""),
                     "ADD" if act == "A" else "DEL", {"Y": "", "F": "F", "K": "K", "": ""}[mk],
                     doa.strftime("%d/%m/%Y") if doa else ""))
    rows.sort(key=lambda r: (r[0][6:] + r[0][3:5] + r[0][:2], r[1], r[2]))
    pre = list(ELECTRA_TITLE)
    pre[1] = "NOTICES OF ALTERATION 04/01/2021 TO 01/03/2022"
    pre[3] = "RUN 04/03/2022 17:58"
    _csv(path, ["NOTICE", "PD", "ELECTOR_NO", "PROPREF", "ADDRESS", "ACTION", "FRANCHISE", "ATTAINS_18"], rows, delim="|",
         pre=pre)
    return len(rows)


def xref(path, w):
    rows = []
    for d in w["dwellings"]:
        if d["old_ref"] is None:
            continue
        rows.append((d["old_ref"], d["pid"], d["uprn"], "UPRN" if d["site"] is None or d["done"] < W.mindex(2019, 1) else "ADDRESS"))
    rows.sort()
    _csv(path, ["electra_propref", "property_id", "uprn", "match_basis"], rows)
    return len(rows)


NONRES = [("CR01", "shop"), ("CR02", "retail unit"), ("CO01", "offices"), ("CC03", "community hall"), ("CE01", "school"),
          ("CI01", "workshop"), ("CT08", "garage"), ("CL06", "public house"), ("CM02", "surgery"), ("CU01", "chapel")]


def llpg(path, w, g, seed=W.SEED + 3):
    """the address register extract, one row an address record (LPI) with its property's (BLPU) state, class,
    parent, ward and parish; dwellings, the buildings that hold flats, alternative and historical records, the plots
    already addressed on sites under way, and non-residential properties"""
    rng = np.random.default_rng(seed)
    dw = w["dwellings"]
    blocks = g["blocks"]
    rows = []
    parish = {}
    for c, n, cl, r, p in W.WARDS:
        for j in range(p):
            parish[(c, j)] = "" if c in TOWN else "P%s%d" % (c, j + 1)
    xy0 = {c: (440000 + 3000 * (i % 6), 360000 + 3000 * (i // 6)) for i, (c, *_r) in enumerate(W.WARDS)}

    def xy(c):
        x0, y0 = xy0[c]
        return int(x0 + rng.integers(0, 2600)), int(y0 + rng.integers(0, 2600))
    for k, b in enumerate(blocks):
        town = TOWN.get(b["ward"], [x for x in W.WARDS if x[0] == b["ward"]][0][1])
        x, y = xy(b["ward"])
        kids = [d for d in dw if d.get("block") == k and (d["inuse"] is None or d["inuse_date"] <= LLPG_DATE)]
        if not kids:
            continue
        sd = min(d["llpg_state_date"] for d in kids)
        rows.append([b["uprn"], "", 1, 2, sd.isoformat(), CLASS_PARENT, "", b["number"], b["name"], b["street"], town,
                     kids[0]["postcode"], b["ward"], parish[(b["ward"], b["pd"])], x, y])
    for d in dw:
        if d["inuse"] is not None and d["inuse_date"] > LLPG_DATE:
            continue
        town = TOWN.get(d["ward"], [x for x in W.WARDS if x[0] == d["ward"]][0][1])
        x, y = xy(d["ward"])
        par = blocks[d["block"]]["uprn"] if d["block"] is not None else ""
        sao = "Flat %d" % d["flat"] if d["block"] is not None else ""
        pao_t = blocks[d["block"]]["name"] if d["block"] is not None else ""
        rows.append([d["uprn"], par, 1, 2, d["llpg_state_date"].isoformat(), d["cls"], sao, d["number"], pao_t,
                     d["street"], town, d["postcode"], d["ward"], parish[(d["ward"], d["pd"])], x, y])
        if d["block"] is None and rng.random() < 0.018:
            rows.append([d["uprn"], "", 3, 2, d["llpg_state_date"].isoformat(), d["cls"], "", d["number"],
                         "%s %s" % (["Rose", "Ivy", "Fern", "Holly", "Stone", "Orchard"][int(rng.integers(0, 6))],
                                    ["Cottage", "House", "Lodge", "Villa"][int(rng.integers(0, 4))]),
                         d["street"], town, d["postcode"], d["ward"], parish[(d["ward"], d["pd"])], x, y])
    # plots addressed ahead of completion on the sites under way at the extract
    for d in dw:
        if d["inuse"] is None or d["inuse_date"] <= LLPG_DATE:
            continue
        if d["done"] <= W.mindex(2027, 6):
            town = TOWN.get(d["ward"], [x for x in W.WARDS if x[0] == d["ward"]][0][1])
            x, y = xy(d["ward"])
            par = blocks[d["block"]]["uprn"] if d["block"] is not None else ""
            sao = "Flat %d" % d["flat"] if d["block"] is not None else ""
            rows.append([d["uprn"], par, 6, 1, "", d["cls"], sao, d["number"], blocks[d["block"]]["name"] if d["block"] is not None else "",
                         d["street"], town, d["postcode"], d["ward"], parish[(d["ward"], d["pd"])], x, y])
    # non-residential properties and records closed before the extract
    seq = 200061000000
    for c, n, cl, r, p in W.WARDS:
        town = TOWN.get(c, n)
        streets = sorted(set(d["street"] for d in dw if d["ward"] == c and d["site"] is None))
        for _ in range(int(rng.integers(60, 160)) if c in TOWN else int(rng.integers(15, 45))):
            seq += int(rng.integers(1, 40))
            cls, nm = NONRES[int(rng.integers(0, len(NONRES)))]
            x, y = xy(c)
            st = streets[int(rng.integers(0, len(streets)))]
            j = int(rng.integers(0, p))
            rows.append([seq, "", 1, 2, D(int(rng.integers(2003, 2026)), int(rng.integers(1, 13)), 1).isoformat(), cls, "",
                         int(rng.integers(1, 200)), "", st, town, "", c, parish[(c, j)], x, y])
        for _ in range(int(rng.integers(3, 15))):
            seq += int(rng.integers(1, 40))
            x, y = xy(c)
            st = streets[int(rng.integers(0, len(streets)))]
            j = int(rng.integers(0, p))
            rows.append([seq, "", 8, 4, D(int(rng.integers(2008, 2026)), int(rng.integers(1, 13)), 1).isoformat(),
                         ["RD03", "RD04", "CR01", "CI01"][int(rng.integers(0, 4))], "", int(rng.integers(1, 120)), "",
                         st, town, "", c, parish[(c, j)], x, y])
    rows.sort(key=lambda r: (int(r[0]), r[2]))
    _csv(path, ["UPRN", "PARENT_UPRN", "LOGICAL_STATUS", "BLPU_STATE", "BLPU_STATE_DATE", "CLASSIFICATION", "SAO_TEXT",
                "PAO_START_NUMBER", "PAO_TEXT", "STREET_DESCRIPTOR", "TOWN_NAME", "POSTCODE_LOCATOR", "WARD_CODE",
                "PARISH_CODE", "X_COORDINATE", "Y_COORDINATE"], rows)
    return len(rows), parish


def site_meta(w, g, seed=W.SEED + 4):
    """each site's reference, planning reference, name and permission"""
    rng = np.random.default_rng(seed)
    dw = w["dwellings"]
    sites = W.all_sites()
    meta = []
    used = set()
    for si, (c, name, nh, nf, ph) in enumerate(sites):
        ks = [d for d in dw if d["site"] == si]
        first = min(ph)
        if first >= 2027:
            yr = int(rng.integers(2019, 2026)) if nh + nf > 300 else int(rng.integers(2023, 2026))
        else:
            yr = min(2026, max(2010, first - int(rng.integers(1, 4))))
        for _ in range(100):
            num = int(rng.integers(100, 2400))
            pref = "%02d/%05d/%s" % (yr % 100, num, "OUT" if nh + nf > 300 else "FUL")
            if pref not in used:
                used.add(pref)
                break
        if si >= len(W.SITES):
            st = ks[0]["street"] if ks else "unnamed"
            num0 = ks[0]["number"] if ks else 0
            name = {"infill": "Land adjoining %d %s" % (max(1, num0 - 1), st),
                    "former garage site": "Former garages, %s" % st,
                    "barn conversion": "Barns at %s" % st,
                    "conversion": "%d %s (conversion to flats)" % (num0, st)}[name]
        meta.append(dict(si=si, ward=c, name=name, ref="HLS%04d" % (si * 7 + 113), planning=pref, houses=nh, flats=nf,
                         phasing=ph))
    return meta


def tenure_beds(rng, typ):
    t = ["Market", "Market", "Market", "Market", "Market", "Market", "Market", "Affordable rent", "Shared ownership",
         "Social rent"][int(rng.integers(0, 10))]
    if typ == "house":
        b = int(rng.choice([2, 3, 4, 5], p=[0.2, 0.45, 0.28, 0.07]))
        ty = "Bungalow" if rng.random() < 0.05 else "House"
    else:
        b = int(rng.choice([1, 2], p=[0.45, 0.55]))
        ty = "Maisonette" if rng.random() < 0.06 else "Flat"
    return ty, b, t


def completions(path, w, meta, seed=W.SEED + 5):
    """the council's housing completions monitoring, one row a completed plot from 2014/15 to 30 September 2026"""
    rng = np.random.default_rng(seed)
    dw = w["dwellings"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Completions"
    ws.append(["Lorrimere District Council: housing completions monitoring, plot schedule"])
    ws.append(["Completions 1 April 2014 to 30 September 2026 (half-year return). Planning Policy, Housing Monitoring."])
    ws.append([])
    hdr = ["Site ref", "Site", "Ward", "Planning ref", "Plot", "UPRN", "Address", "Dwelling type", "Bedrooms", "Tenure",
           "Completion date", "Monitoring year"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    rows = []
    plot_no = {}
    for d in sorted([d for d in dw if d["site"] is not None and d["built"]], key=lambda d: (d["site"], d["done"], d["uprn"])):
        m = meta[d["site"]]
        plot_no[d["site"]] = plot_no.get(d["site"], 0) + 1
        ty, b, t = tenure_beds(rng, d["type"])
        y, mo = W.ym(d["done"])
        my = y if mo >= 4 else y - 1
        cd = d["done_date"]
        rows.append([m["ref"], m["name"], [x for x in W.WARDS if x[0] == d["ward"]][0][1], m["planning"],
                     plot_no[d["site"]], d["uprn"], d["addr"], ty, b, t, cd, "%d/%02d" % (my, (my + 1) % 100)])
        d["beds"], d["tenure"], d["dtype"] = b, t, ty
    rows.sort(key=lambda r: (r[10], r[0], r[4]))
    for r in rows:
        ws.append(r)
    for row in ws.iter_rows(min_row=5, min_col=11, max_col=11):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    widths = [10, 34, 20, 14, 6, 13, 52, 13, 9, 17, 15, 14]
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = "A5"
    wb.save(path)
    return len(rows)


def trajectory(path, w, meta, seed=W.SEED + 6):
    """the housing trajectory at 30 September 2026: every site with dwellings still to come, phased by monitoring
    year, and the sites with permission whose dwellings come after 2032/33"""
    rng = np.random.default_rng(seed)
    dw = w["dwellings"]
    years = list(range(2026, 2033))
    cols = ["2026/27 (1 Oct to 31 Mar)"] + ["%d/%02d" % (y, (y + 1) % 100) for y in years[1:]] + ["2033/34 onwards"]
    later = {"North Lorrimere urban extension": 810}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Trajectory"
    ws.append(["Lorrimere District Council: housing trajectory, base date 30 September 2026"])
    ws.append(["Sites with planning permission or allocated, dwellings still to be completed. Planning Policy."])
    ws.append([])
    hdr = ["Site ref", "Site", "Ward", "Planning ref", "Permission", "Status at 30/09/2026", "Houses", "Flats",
           "Total dwellings", "Completed to 30/09/2026"] + cols
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    out = []
    for m in meta:
        ks = [d for d in dw if d["site"] == m["si"]]
        done = sum(1 for d in ks if d["built"])
        fut = [d for d in ks if not d["built"]]
        extra = later.get(m["name"], 0)
        if not fut and not extra:
            continue
        by = {y: sum(1 for d in fut if d["plan_year"] == y) for y in years}
        houses = m["houses"] + (extra if m["houses"] else 0)
        flats = m["flats"]
        status = "Under construction" if done else ("Full permission, not started" if "FUL" in m["planning"] else "Outline permission")
        perm = "Full" if "FUL" in m["planning"] else "Outline"
        row = [m["ref"], m["name"], [x for x in W.WARDS if x[0] == m["ward"]][0][1], m["planning"], perm, status, houses,
               flats, houses + flats, done] + [by[y] for y in years] + [extra]
        out.append(row)
    # permissions whose dwellings all come after the trajectory's seventh year
    for name, ward, n in [("Land east of Selwar Common", "SEL", 240), ("Holme Ings farm", "BRE", 180),
                          ("Ketter Wold north", "KET", 320)]:
        out.append(["HLS%04d" % (900 + len(out)), name, [x for x in W.WARDS if x[0] == ward][0][1], "26/%05d/OUT" % int(rng.integers(100, 900)),
                    "Outline", "Outline permission", n, 0, n, 0] + [0] * len(years) + [n])
    out.sort(key=lambda r: (r[2], r[0]))
    for r in out:
        ws.append(r)
    ws.freeze_panes = "C5"
    for i, wd in enumerate([10, 36, 20, 14, 10, 26, 8, 8, 10, 12] + [11] * (len(cols))):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ns = wb.create_sheet("Notes")
    for line in [
        "Base date 30 September 2026. Completions to that date are from the completions monitoring plot schedule.",
        "Phasing is by monitoring year (1 April to 31 March); the 2026/27 column holds the dwellings expected from 1 October 2026 to 31 March 2027.",
        "Phasing is taken from developers' build programmes and the council's site visits, and completions in a year are assumed to fall evenly through it.",
        "Where a site holds houses and flats, the mix in each year follows the mix the site still has to build.",
        "Dwellings expected after 31 March 2033 are shown in a single column and are not phased.",
        "Prepared by Planning Policy for the Housing Land Supply Statement; not a forecast of population or electors."]:
        ns.append([line])
    ns.column_dimensions["A"].width = 140
    wb.save(path)
    return len(out)


PLACES = ["Village Hall", "Community Centre", "Church Hall", "Primary School", "Methodist Hall", "Scout Hut", "Sports Pavilion",
          "Memorial Hall", "Library", "Youth Centre"]


def pd_schedule(path, w, g, seed=W.SEED + 7):
    """the 2023 polling district review's schedule: each new district, its ward, polling place and the districts it
    replaces, with the streets the review moved"""
    rng = np.random.default_rng(seed)
    import geo as G
    rows = []
    moved = g["moved_streets"]
    for c, n, cl, r, p in W.WARDS:
        for j in range(p):
            new = g["new_code"][(c, j)]
            old = g["old_code"][(c, j)]
            nm = G.PD_NAMES[c][j]
            ins = sorted(st for (cc, st), (oj, nj) in moved.items() if cc == c and nj == j)
            outs = sorted(st for (cc, st), (oj, nj) in moved.items() if cc == c and oj == j)
            change = []
            if ins:
                frm = sorted(set(g["old_code"][(c, moved[(c, st)][0])] for st in ins))
                change.append("%s transferred from district %s" % (" and ".join(ins), "/".join(frm)))
            if outs:
                to = sorted(set(g["new_code"][(c, moved[(c, st)][1])] for st in outs))
                change.append("%s transferred to %s" % (" and ".join(outs), "/".join(to)))
            place = "%s %s" % (nm.split()[0], PLACES[int(rng.integers(0, len(PLACES)))])
            rows.append((new, nm, n, place, old, "; ".join(change) if change else "renamed, boundary unchanged"))
    _csv(path, ["district", "district_name", "ward", "polling_place", "replaces_district", "change"], rows)
    return len(rows)


def wards_file(path, g):
    rows = []
    for c, n, cl, r, p in W.WARDS:
        rows.append((c, n, cl, ";".join(g["new_code"][(c, j)] for j in range(p))))
    _csv(path, ["ward_code", "ward_name", "councillors", "polling_districts_2023_scheme"], rows)
    return len(rows)


def projections(path, w, seed=W.SEED + 8):
    """the statistics office's 2022-based sub-national population projections for the district, by age group"""
    rng = np.random.default_rng(seed)
    base = sum(d["count"][2022] for d in w["dwellings"]) / 0.80
    rows = []
    shares = {"0-15": 0.176, "16-17": 0.022, "18-64": 0.565, "65+": 0.237}
    g = 0.0068
    for y in range(2022, 2043):
        tot = base * (1 + g) ** (y - 2022)
        old = shares["65+"] + 0.0021 * (y - 2022)
        sh = {"0-15": shares["0-15"] - 0.0009 * (y - 2022), "16-17": shares["16-17"], "65+": old}
        sh["18-64"] = 1 - sum(sh.values())
        for a in ["0-15", "16-17", "18-64", "65+"]:
            rows.append(("mid-%d" % y, "Lorrimere", a, int(round(tot * sh[a] / 10.0) * 10)))
    _csv(path, ["year", "area", "age_group", "population"], rows)
    return len(rows)


BANDS = "ABCDEFGH"


def council_tax(path, w, seed=W.SEED + 10):
    """the valuation list's dwellings by council tax band and ward at 1 September 2025"""
    rng = np.random.default_rng(seed)
    cut = D(2025, 9, 1)
    tab = {}
    for d in w["dwellings"]:
        if d["inuse_date"] > cut:
            continue
        if d["type"] == "flat":
            b = BANDS[int(rng.choice(3, p=[0.55, 0.35, 0.10]))]
        else:
            b = BANDS[int(rng.choice(8, p=[0.08, 0.20, 0.28, 0.20, 0.13, 0.07, 0.035, 0.005]))]
        tab[(d["ward"], b)] = tab.get((d["ward"], b), 0) + 1
    rows = []
    for c, n, cl, r, p in W.WARDS:
        rows.append([c, n] + [tab.get((c, b), 0) for b in BANDS] + [sum(tab.get((c, b), 0) for b in BANDS)])
    _csv(path, ["ward_code", "ward_name"] + ["band_%s" % b for b in BANDS] + ["all_bands"], rows)
    return len(rows)


def field_guide(path, names):
    lines = [
        "LORRIMERE DISTRICT COUNCIL: DATA SUPPLIED FOR THE ELECTORAL REVIEW",
        "Electoral Services and Planning Policy, 12 October 2026. Contact: Donald Hayes, Electoral Services Manager.",
        "",
        "%s" % names["ems_new"],
        "  The current electoral management system's property electorate report for the revised registers of 1 December",
        "  2022, 2023, 2024 and 2025. One row a property on the system's property database at the register's publication.",
        "  register_date               publication date of the revised register",
        "  polling_district            polling district of the property on that register (the 2023 scheme from 2023)",
        "  property_id                 the system's property id",
        "  uprn                        the property's UPRN from the gazetteer",
        "  local_government_electors   entries for electors aged 18 or over on the publication date with the local",
        "                              government franchise",
        "  attainers                   entries for persons under 18 on the publication date",
        "  overseas_electors           overseas electors registered at the property for parliamentary elections only",
        "  local_franchise_only        of local_government_electors, those registered for local elections only",
        "",
        "%s, %s" % (names["ems_2020"], names["ems_2021"]),
        "  The Electra system's property electorate report for the revised registers of 1 December 2020 and 2021,",
        "  pipe-delimited after a title block, one row a property, by polling district (the scheme in force before 2023).",
        "  TOTAL counts every entry at the property; ATTAINERS and OVERSEAS are included in TOTAL; LOCAL_ONLY counts",
        "  the electors registered for local elections only.",
        "",
        "%s" % names["notices"],
        "  Electra's monthly notices of alteration, January 2021 to March 2022, pipe-delimited after a title block, one",
        "  row an entry added to (ADD) or deleted from (DEL) the register, with its elector number and property reference.",
        "  FRANCHISE F marks an overseas elector and K an elector registered for local elections only; ATTAINS_18 is the",
        "  date an attainer reaches 18.",
        "  The Electra files were exported when the system was replaced in March 2022.",
        "",
        "%s" % names["xref"],
        "  The cross-reference made when Electra's property database was migrated in March 2022: Electra's property",
        "  reference, the new system's property id and the UPRN, with the basis on which the UPRN was matched.",
        "",
        "%s" % names["llpg"],
        "  Extract of the local land and property gazetteer at 12 October 2026, one row an address record.",
        "  LOGICAL_STATUS 1 approved, 3 alternative, 6 provisional, 8 historical. BLPU_STATE 1 under construction,",
        "  2 in use, 4 no longer existing; BLPU_STATE_DATE the date the property's state last changed.",
        "  CLASSIFICATION: RD02 detached, RD03 semi-detached, RD04 terraced house, RD06 self-contained flat, PP a",
        "  building holding flats (the flats carry it as PARENT_UPRN); C codes are commercial and community properties.",
        "  WARD_CODE and PARISH_CODE are the administrative areas of the property (no parish in the two towns).",
        "",
        "%s" % names["completions"],
        "  Planning Policy's plot schedule of completed dwellings, 1 April 2014 to 30 September 2026, with the date",
        "  building control recorded each completion and the monitoring year (1 April to 31 March) it falls in.",
        "",
        "%s" % names["trajectory"],
        "  The housing trajectory at 30 September 2026 (see its Notes sheet).",
        "",
        "%s" % names["pd"],
        "  The 2023 polling district review: each district of the 2023 scheme with the district it replaces and the",
        "  streets the review moved between districts. Wards were not changed.",
        "",
        "%s" % names["wards"],
        "  The wards and numbers of councillors set by the 2014 electoral changes order, with each ward's districts.",
        "",
        "%s" % names["proj"],
        "  The statistics office's 2022-based sub-national population projections for the district.",
        "",
        "%s" % names["ctax"],
        "  Dwellings on the valuation list by council tax band and ward at 1 September 2025.",
        ""]
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
