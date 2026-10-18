"""Every figure, read from the shipped pack alone: each ground's haddock stock by year from the autumn survey (the
golden, its variants and the lower rungs), the members' catch rates (the default path), and the two asks with each
handling a response might take."""
import csv
import datetime as dt
import os
from collections import defaultdict

import numpy as np

import common as K

YEARS = K.YEARS


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load(pack):
    import openpyxl
    p = lambda k: os.path.join(pack, K.FILES[k])
    D = {k: read_csv(p(k)) for k in ("grid", "paper", "elog", "survey", "factors", "notes", "ledger")}
    wb = openpyxl.load_workbook(p("members"), read_only=True)
    sheet = lambda n: [r for r in wb[n].iter_rows(values_only=True)]
    rows = sheet("Vessels")
    D["vessels"] = [dict(zip(rows[0], r)) for r in rows[1:]]
    rows = sheet("Registration history")
    D["history"] = [dict(zip(rows[0], r)) for r in rows[1:]]
    rows = sheet("Licences")
    D["licences"] = [dict(zip(rows[0], r)) for r in rows[1:]]
    wb.close()
    D["cells"] = {r["cell"]: r for r in D["grid"]}
    D["cell_rs"] = {(r["rectangle"], r["sub_square"]): r["cell"] for r in D["grid"]}
    return D


# ---------------------------------------------------------------------------------------------- the survey
def locate(D):
    """Each survey tow's cell, found from its shot position and the grid's bounds."""
    g = D["grid"]
    lat_n = np.array([float(r["lat_north"]) for r in g])
    lat_s = np.array([float(r["lat_south"]) for r in g])
    lon_w = np.array([float(r["lon_west"]) for r in g])
    lon_e = np.array([float(r["lon_east"]) for r in g])
    out = []
    for t in D["survey"]:
        la, lo = float(t["shot_lat"]), float(t["shot_lon"])
        k = np.nonzero((la < lat_n) & (la >= lat_s) & (lo >= lon_w) & (lo < lon_e))[0]
        assert len(k) == 1, t
        out.append(g[int(k[0])]["cell"])
    return out


def tows(D):
    if "_tows" not in D:
        cells = locate(D)
        T = []
        for t, c in zip(D["survey"], cells):
            cell = D["cells"][c]
            T.append(dict(year=int(t["survey_year"]), station=t["station"], ground=cell["ground"], band=cell["depth_band"],
                          code=t["ground_code"], depth=int(t["depth_m"]), kg=float(t["haddock_kg"]), n=int(t["haddock_n"]),
                          cell=c))
        D["_tows"] = T
    return D["_tows"]


def band_areas(D, weights="area"):
    A = defaultdict(float)
    for r in D["grid"]:
        A[(r["ground"], r["depth_band"])] += float(r["area_km2"]) if weights == "area" else 1.0
    return A


def survey_index(D, weights="area", missed="drop", moved="keep", measure="kg", stat="mean", band_by="cell"):
    """Each ground's stock by year: the mean haddock catch per tow in each depth band, weighted by the band's share
    of the ground's stock area (weights='area'); 'cells' weights bands by their count of cells; 'tows' is the plain
    mean of the ground's tows."""
    T = tows(D)
    if band_by == "depth":
        T = [dict(t, band="A" if t["depth"] < 100 else ("B" if t["depth"] < 140 else "C")) for t in T]
    if moved == "drop":
        years = defaultdict(set)
        for t in T:
            years[t["station"]].add(t["year"])
        full = {s for s, ys in years.items() if len(ys) >= len(YEARS) - 1}
        T = [t for t in T if t["station"] in full]
    val = (lambda t: t["kg"]) if measure == "kg" else (lambda t: t["n"])
    if stat == "geo":
        f = lambda xs: float(np.exp(np.mean(np.log(np.array(xs) + 1.0))) - 1.0)
    else:
        f = lambda xs: float(np.mean(xs))
    by = defaultdict(list)
    for t in T:
        by[(t["ground"], t["year"], t["band"])].append(val(t))
    if missed == "impute":
        # the station missed in 2020 carried at its own other years scaled by its band's 2020 level
        st = defaultdict(dict)
        for t in T:
            st[t["station"]][t["year"]] = (t["ground"], t["band"], val(t))
        for s, ys in st.items():
            if 2020 not in ys and min(ys) == 2019 and max(ys) == 2026:
                g, b, _ = ys[2019]
                others = [s2 for s2, y2 in st.items() if y2.get(2019, (None, None))[0:2] == (g, b) and 2020 in y2 and s2 != s]
                lvl20 = np.mean([st[s2][2020][2] for s2 in others])
                lvl = np.mean([np.mean([st[s2][y][2] for y in ys if y != 2020 and y in st[s2]]) for s2 in others])
                own = np.mean([v[2] for y, v in ys.items()])
                by[(g, 2020, b)].append(own * lvl20 / lvl if lvl > 0 else 0.0)
    A = band_areas(D, weights if weights != "tows" else "area")
    out = {}
    for g in K.GROUND_NAMES:
        out[g] = {}
        for y in YEARS:
            if weights == "tows":
                xs = [x for b in K.BANDS for x in by[(g, y, b)]]
                out[g][y] = f(xs)
            else:
                tot = sum(A[(g, b)] for b in K.BANDS)
                out[g][y] = sum(A[(g, b)] * f(by[(g, y, b)]) for b in K.BANDS) / tot
    return out


def falls(index, latest=K.LATEST, base="avg", pooled=None):
    out = {}
    for g, ix in index.items():
        b = np.mean([ix[y] for y in K.BASE]) if base == "avg" else pooled[g]
        out[g] = 1.0 - ix[latest] / b
    return out


def pooled_base(D, weights="area"):
    """The base as one stratified mean over the three base years' tows pooled."""
    T = tows(D)
    A = band_areas(D, weights)
    out = {}
    for g in K.GROUND_NAMES:
        tot = sum(A[(g, b)] for b in K.BANDS)
        out[g] = sum(A[(g, b)] * np.mean([t["kg"] for t in T if t["ground"] == g and t["band"] == b and t["year"] in K.BASE])
                     for b in K.BANDS) / tot
    return out


def call(f):
    order = sorted(f, key=lambda g: -f[g])
    return dict(order=order, pick=order[0], runner=order[1], gap=f[order[0]] - f[order[1]],
                margin=f[order[0]] / f[order[1]] if f[order[1]] > 0 else float("inf"))


# ---------------------------------------------------------------------------------------------- the logbooks
def pln_to_rss(D):
    hist = defaultdict(list)
    for h in D["history"]:
        hist[h["PLN"]].append((h["RSS no"], h["Registered from"], h["Registered to"]))
    return hist


def _as_date(x):
    if x is None or isinstance(x, dt.date) and not isinstance(x, dt.datetime):
        return x
    return x.date()


def records(D):
    """Every logbook record on the live-weight and hours basis: (year, ground, cell, vessel, month, hours, live kg)."""
    if "_rec" in D:
        return D["_rec"]
    hist = pln_to_rss(D)
    out = []
    for r in D["paper"]:
        cell = D["cells"][D["cell_rs"][(r["rectangle"], r["sub_square"])]]
        day = dt.date.fromisoformat(r["landed"])
        v = r["vessel_pln"]
        for rss, a, b in hist.get(v, []):
            if _as_date(a) <= day and (b is None or day <= _as_date(b)):
                v = rss
        out.append((day.year if day.year in YEARS else int(r["departed"][:4]), cell["ground"], cell["cell"], v,
                    int(r["departed"][5:7]), float(r["hours_fished"]), float(r["haddock_kg"])))
    for r in D["elog"]:
        cell = D["cells"][r["cell"]]
        s = dt.datetime.strptime(r["haul_start_utc"], "%Y-%m-%dT%H:%MZ")
        e = dt.datetime.strptime(r["haul_end_utc"], "%Y-%m-%dT%H:%MZ")
        out.append((s.year, cell["ground"], cell["cell"], r["vessel_rss"], s.month, (e - s).total_seconds() / 3600,
                    float(r["had_gutted_kg"]) * 1.17))
    D["_rec"] = out
    return out


def cpue_index(D, how="nominal"):
    R = records(D)
    out = {}
    for g in K.GROUND_NAMES:
        rs = [r for r in R if r[1] == g and r[0] in YEARS and r[5] > 0]
        out[g] = {}
        if how == "nominal":
            for y in YEARS:
                sel = [r for r in rs if r[0] == y]
                out[g][y] = sum(r[6] for r in sel) / sum(r[5] for r in sel)
        elif how == "cells":
            area = {r["cell"]: float(r["area_km2"]) for r in D["grid"]}
            for y in YEARS:
                agg = defaultdict(lambda: [0.0, 0.0])
                for r in rs:
                    if r[0] == y:
                        agg[r[2]][0] += r[6]
                        agg[r[2]][1] += r[5]
                out[g][y] = sum(area[c] * a[0] / a[1] for c, a in agg.items()) / sum(area[c] for c in agg)
        elif how == "glm":
            rs = [r for r in rs if r[6] > 0]
            Y = np.log(np.array([r[6] / r[5] for r in rs]))
            cols, X = [], []
            for key, idx in (("y", 0), ("c", 2), ("v", 3), ("m", 4)):
                lv = sorted({r[idx] for r in rs})
                for j, l in enumerate(lv):
                    if key != "y" and j == 0:
                        continue
                    cols.append((key, idx, l))
            M = np.zeros((len(rs), len(cols)))
            pos = {(k, l): j for j, (k, i, l) in enumerate(cols)}
            for i, r in enumerate(rs):
                for key, idx in (("y", 0), ("c", 2), ("v", 3), ("m", 4)):
                    j = pos.get((key, r[idx]))
                    if j is not None:
                        M[i, j] = 1.0
            beta = np.linalg.lstsq(M, Y, rcond=None)[0]
            for y in YEARS:
                out[g][y] = float(np.exp(beta[pos[("y", y)]]))
    return out


def ladder(D):
    f = {}
    f["R0"] = falls(cpue_index(D, "nominal"))
    f["R1"] = falls(cpue_index(D, "glm"))
    f["R1v"] = falls(cpue_index(D, "cells"))
    f["R2"] = falls(survey_index(D, weights="tows"))
    f["R3"] = falls(survey_index(D))
    return f


# ---------------------------------------------------------------------------------------------- Ask A
def member_plns(D, current_only=False):
    if current_only:
        return {v["PLN"]: (dt.date(1900, 1, 1), None) for v in D["vessels"]}
    out = {}
    for h in D["history"]:
        out.setdefault(h["PLN"], []).append((_as_date(h["Registered from"]), _as_date(h["Registered to"])))
    return out


def ask_a(D, handling="golden"):
    """Each port's haddock landed by members from 1 January to 30 September 2026 (by landing date), tonnes live
    weight and value at first sale. Handlings: golden, plain (the export as it stands, members by current letters),
    session (one note a buyer a landing), lots (identical lots on a note collapsed), current (golden, current letters
    only), issued (golden, by the note's issue date)."""
    fac = {(r["species_code"], r["presentation_code"]): float(r["factor_to_live"]) for r in D["factors"]}
    if handling in ("plain", "current"):
        cur = {v["PLN"] for v in D["vessels"]}
        is_member = lambda pln, day: pln in cur
    else:
        valid = member_plns(D)
        is_member = lambda pln, day: any(a <= day and (b is None or day <= b) for a, b in valid.get(pln, []))
    notes = defaultdict(list)
    for r in D["notes"]:
        notes[r["note_no"]].append(r)
    keep = set(notes)
    if handling not in ("plain",):
        groups = defaultdict(list)
        for no, ls in notes.items():
            h = ls[0]
            groups[(h["buyer_reg"], h["vessel_pln"], h["landing_date"], h["port"])].append(no)
        for key, nos in groups.items():
            if len(nos) < 2:
                continue
            if handling == "session":
                last = max(nos, key=lambda n: (notes[n][0]["issued"], n))
                keep -= set(nos) - {last}
                continue
            sig = lambda n: tuple(sorted((l["species"], l["presentation"], l["grade"], l["boxes"], l["weight_kg"]) for l in notes[n]))
            bysig = defaultdict(list)
            for n in nos:
                bysig[sig(n)].append(n)
            for s, ns in bysig.items():
                if len(ns) > 1:
                    last = max(ns, key=lambda n: (notes[n][0]["issued"], n))
                    keep -= set(ns) - {last}
    out = {p: [0.0, 0.0] for p in K.PORT_NAMES}
    lo, hi = "2026-01-01", "2026-09-30"
    for no in keep:
        ls = notes[no]
        if handling == "lots":
            seen, kept = set(), []
            for l in ls:
                k = (l["species"], l["presentation"], l["grade"], l["boxes"], l["weight_kg"])
                if k not in seen:
                    seen.add(k)
                    kept.append(l)
            ls = kept
        for l in ls:
            if l["species"] != "HAD":
                continue
            day = l["issued"] if handling == "issued" else l["landing_date"]
            if not (lo <= day <= hi):
                continue
            if not is_member(l["vessel_pln"], dt.date.fromisoformat(l["landing_date"])):
                continue
            out[l["port"]][0] += float(l["weight_kg"]) * fac[(l["species"], l["presentation"])] / 1000
            out[l["port"]][1] += float(l["value_gbp"])
    return {p: (v[0], v[1]) for p, v in out.items()}


# ---------------------------------------------------------------------------------------------- Ask B
def ask_b(D, handling="golden", day="2026-09-30"):
    """Each pool's haddock quota left on 30 September 2026: every ledger entry effective that day or before, the
    pool-level copy of the 1 January allocation taken once. Handlings: golden, plain (every entry), blank (every entry
    without a licence dropped), posted (by posting date), cancel (a lease cancelled later taken out from the start)."""
    rows = D["ledger"]
    cancelled = {r["reference"].replace(" cancelled", "") for r in rows if r["reference"].endswith(" cancelled")}
    out = {p: 0.0 for p in K.POOL_CODES}
    for r in rows:
        when = r["posted"] if handling == "posted" else r["effective"]
        if when > day:
            continue
        blank = r["licence"] == ""
        if handling != "plain" and blank and r["type"] == "allocation":
            continue
        if handling == "blank" and blank:
            continue
        if handling == "cancel" and r["reference"] in cancelled:
            continue
        out[r["pool"]] += float(r["tonnes"])
    return out
