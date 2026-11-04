"""Every other row the export holds: the nutrient and physico-chemical suites, the abstraction
programme's nitrate, the quality-control samples and the versions the laboratories reissued."""
import datetime as dt
import random

import world as W

RNG_BASE = W.SEED * 7


def op_points():
    """the district's operational network: nutrients and physico-chemical only, no pesticide suite"""
    out = []
    for i, place in enumerate(W.OP_PLACES):
        catch = W.OPERATIONAL_CATCHMENTS[i % len(W.OPERATIONAL_CATCHMENTS)]
        out.append(("ARW-%04d" % (2000 + i * 7 + 3), "%s at %s" % (catch, place), catch))
    return out


def compliance_points():
    out = []
    for (name, code, old, catch, area, target, points) in W.WATER_BODIES:
        for (suffix, lab, pf, place) in points:
            out.append(("ARW-" + suffix, place, name, code, lab, pf))
    return out


def _nutrient_level(code, det, month, rng):
    seed = sum(ord(c) for c in code)
    base = {"NH4N": 0.045, "TON": 3.6, "OPO4": 0.038, "CL": 21.0, "SO4": 13.5}[det]
    swing = {"NH4N": 0.55, "TON": 0.35, "OPO4": 0.48, "CL": 0.16, "SO4": 0.18}[det]
    season = 1.0 + swing * (0.6 if month in (11, 12, 1, 2) else -0.35 if month in (6, 7, 8) else 0.05)
    return base * (0.55 + (seed % 90) / 60.0) * season * (1.0 + rng.gauss(0.0, 0.17))


def _physico_level(code, det, month, rng):
    seed = sum(ord(c) for c in code)
    table = {"COND": (320.0, 0.22), "PH": (7.4, 0.03), "DO": (10.4, 0.12), "TEMP": (10.5, 0.45),
             "SS": (9.5, 0.6), "ALK": (105.0, 0.3), "TURB": (4.6, 0.7), "COLOUR": (38.0, 0.45)}
    base, sd = table[det]
    if det == "TEMP":
        base = 10.5 + 5.6 * (1 if month in (6, 7, 8) else -1 if month in (12, 1, 2) else 0) * 0.8
    return base * (0.8 + (seed % 70) / 160.0) * (1.0 + rng.gauss(0.0, sd * 0.30))


def nutrient_rows():
    """monthly nutrient suite at every compliance and operational point"""
    rng = random.Random(RNG_BASE + 11)
    pts = [(c, pl, wb) for (c, pl, wb, _code, _lab, _pf) in compliance_points()]
    pts += [(c, pl, wb) for (c, pl, wb) in op_points()]
    rows = []
    for (code, place, wb) in pts:
        lab = "TAS" if (sum(ord(ch) for ch in code) % 2 == 0) else "KGL"
        for (y, m) in W.MONTHS:
            for det in (["NO3"] if lab == "TAS" else ["NO3N"]) + W.NUTRIENTS:
                if det == "NO3":
                    val = _nutrient_level(code, "TON", m, rng) * W.NO3_FACTOR
                    method, units = "TAS-IC-ANI-02", "mg/l"
                elif det == "NO3N":
                    val = _nutrient_level(code, "TON", m, rng)
                    method, units = "KGL-CF-NUT-03", "mg/l"
                else:
                    val = _nutrient_level(code, det, m, rng)
                    method = "TAS-IC-ANI-02" if det in ("CL", "SO4", "OPO4") and lab == "TAS" else \
                             "KGL-CF-NUT-03" if lab == "KGL" else "TAS-IC-ANI-02"
                    units = "mg/l"
                rl = W.METHODS[method]["rl"]
                rows.append({"point": code, "place": place, "wb": wb, "year": y, "month": m,
                             "det": det, "value": max(val, 0.0), "rl": rl,
                             "det_flag": max(val, 0.0) >= rl, "method": method, "units": units,
                             "lab": W.METHODS[method]["lab"], "suite": "NUT"})
    return rows


def physico_rows():
    """fortnightly physico-chemical suite, the bulk of the export"""
    rng = random.Random(RNG_BASE + 23)
    pts = [(c, pl, wb) for (c, pl, wb, _code, _lab, _pf) in compliance_points()]
    pts += [(c, pl, wb) for (c, pl, wb) in op_points()]
    rows = []
    for (code, place, wb) in pts:
        for (y, m) in W.MONTHS:
            for half in (0, 1):
                for det in W.PHYSICO:
                    val = _physico_level(code, det, m, rng)
                    rows.append({"point": code, "place": place, "wb": wb, "year": y, "month": m,
                                 "half": half, "det": det, "value": max(val, 0.0), "rl": 0.0,
                                 "det_flag": True, "method": "TAS-FLD-PHY-01",
                                 "units": W.DETERMINANDS[det][1], "lab": "TAS", "suite": "PHY"})
    return rows


def abstraction_rows():
    """the source protection programme: nitrate every fortnight at the six raw-water points.

    Two laboratories serve it and they report nitrate under different determinands, one as the
    nitrate ion and one as nitrogen. The water services section submits its own samples to the
    laboratory under its own client code while the laboratory also numbers the authority's
    round, so a run of samples reaches the export twice under two client codes.
    """
    rng = random.Random(RNG_BASE + 37)
    rows = []
    for (code, name, catch, level, lab) in W.ABSTRACTIONS:
        det = "NO3" if lab == "TAS" else "NO3N"
        method = "TAS-IC-ANI-02" if lab == "TAS" else "KGL-CF-NUT-03"
        for (y, m) in W.MONTHS:
            for half in (0, 1):
                season = 1.0 + 0.30 * (0.9 if m in (11, 12, 1, 2) else -0.5 if m in (6, 7, 8) else 0.1)
                as_no3 = level * season * (1.0 + rng.gauss(0.0, 0.11))
                val = as_no3 if det == "NO3" else as_no3 / W.NO3_FACTOR
                rows.append({"point": code, "place": name, "wb": catch, "year": y, "month": m,
                             "half": half, "det": det, "value": max(val, 0.0), "rl": W.METHODS[method]["rl"],
                             "det_flag": True, "method": method, "units": "mg/l",
                             "lab": W.METHODS[method]["lab"], "suite": "ABS", "as_no3": max(as_no3, 0.0),
                             "dual": False})
        for (y, m) in W.MONTHS[6:10]:        # October 2025 to January 2026, the section's own run
            for half in (0, 1):
                src = [r for r in rows if r["point"] == code and r["year"] == y
                       and r["month"] == m and r["half"] == half and not r["dual"]]
                if src and (sum(ord(c) for c in code) + m + half) % 4 != 1:
                    d = dict(src[0]); d["dual"] = True
                    rows.append(d)
    return rows


def qc_rows(field_rows):
    """blanks, duplicates and spikes, run on the laboratories' own schedule"""
    rng = random.Random(RNG_BASE + 53)
    out = []
    for i, r in enumerate(field_rows):
        if i % 23 == 0:
            q = dict(r)
            q["qc"] = W.QC_TYPES[(i // 23) % len(W.QC_TYPES)]
            if q["qc"].endswith("BLANK"):
                q["value"], q["det_flag"] = 0.0, False
            elif q["qc"] == "MATRIX_SPIKE":
                q["value"], q["det_flag"] = r["value"] + (r["rl"] * 20 if r["rl"] else 10.0), True
            else:
                q["value"] = r["value"] * (1.0 + rng.gauss(0.0, 0.05))
            out.append(q)
    return out
