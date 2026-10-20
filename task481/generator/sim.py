"""task481 simulation. Every assault victim, robbery incident and homicide incident reported to the Ellsmere Police
Department from January 2021 to September 2026, each with the Return A line the Records Division's clerks score it under
and the NIBRS offense the new records system records, plus the other offenses the extract carries from October 2024.
Victims are drawn month by month from the world's expected volumes; the kinds the two systems treat differently are
latent and never shipped."""
import datetime as dt

import numpy as np

import world as W

ROB_LINE = {"11": "3A", "12": "3A", "13": "3A", "15": "3A", "20": "3B", "30": "3C", "35": "3C", "40": "3D"}
KIND_WEAPON = {
    "fire_hit": (("11", 0.22), ("12", 0.58), ("13", 0.08), ("15", 0.12)),
    "fire_miss": (("11", 0.20), ("12", 0.55), ("13", 0.07), ("15", 0.18)),
    "knife": (("20", 1.0),),
    "other_weapon": (("30", 0.62), ("35", 0.30), ("90", 0.08)),
    "pw_serious": (("40", 1.0),), "pw_minor": (("40", 1.0),), "threat": (("", 1.0),),
    "dv_serious": (("40", 1.0),), "dv_strang": (("85", 1.0),), "dv_minor": (("40", 1.0),),
    "dv_threat": (("", 1.0),),
}
DV_WEAPON = (("12", 0.28), ("11", 0.12), ("20", 0.35), ("30", 0.15), ("35", 0.10))
LINE_OF_WEAPON = {"11": "4A", "12": "4A", "13": "4A", "15": "4A", "20": "4B", "30": "4C", "35": "4C", "90": "4C"}
SERIOUS = (("B", 0.30), ("L", 0.30), ("I", 0.12), ("U", 0.14), ("T", 0.06), ("O", 0.08))
MINOR = (("M", 0.62), ("N", 0.38))
STREET_PLACES = (("13", 0.34), ("20", 0.18), ("03", 0.09), ("18", 0.12), ("07", 0.05), ("12", 0.05), ("23", 0.04),
                 ("25", 0.13))
DV_PLACES = (("20", 0.88), ("13", 0.04), ("18", 0.04), ("14", 0.04))
FAMILY = (("BG", 0.24), ("SE", 0.12), ("XR", 0.08), ("XS", 0.03), ("CS", 0.03), ("PA", 0.12), ("CH", 0.12),
          ("SB", 0.10), ("OF", 0.06), ("GP", 0.02), ("GC", 0.02), ("IL", 0.02), ("SP", 0.02), ("SC", 0.02), ("SS", 0.01),
          ("CF", 0.01))
STREET_REL = (("AQ", 0.36), ("ST", 0.30), ("OK", 0.12), ("FR", 0.08), ("NE", 0.05), ("RU", 0.07), ("EE", 0.01),
              ("ER", 0.01))

# Other offenses carried by the extract from October 2024: NIBRS code, Return A line (blank when not on Return A),
# expected a month, the victim type mix.
OTHER = (
    ("220", "5A", 118, "I"), ("220", "5B", 61, "B"), ("220", "5C", 22, "I"),
    ("23H", "6", 520, "I"), ("23F", "6", 290, "I"), ("23C", "6", 180, "B"), ("23D", "6", 60, "B"), ("23G", "6", 25, "I"),
    ("240", "7A", 205, "I"), ("240", "7B", 36, "B"), ("240", "7C", 22, "I"),
    ("11A", "2", 24, "I"), ("11D", "", 21, "I"), ("100", "", 6, "I"), ("200", "", 9, "B"),
    ("290", "", 410, "I"), ("35A", "", 160, "S"), ("35B", "", 70, "S"), ("26A", "", 95, "I"), ("26F", "", 55, "I"),
    ("280", "", 18, "S"), ("520", "", 44, "S"), ("90Z", "", 210, "S"), ("90D", "", 85, "S"), ("90C", "", 30, "S"),
    ("13B", "", 0, "I"),
)


def months(first=W.SIM_FIRST, last=W.EXTRACT_LAST):
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def pick(r, pairs):
    vals, ps = zip(*pairs)
    ps = np.array(ps, float)
    return vals[r.choice(len(vals), p=ps / ps.sum())]


def days_in(y, m):
    return ((dt.date(y + (m == 12), m % 12 + 1, 1)) - dt.date(y, m, 1)).days


HOUR_STREET = np.array([6, 5, 4, 3, 2, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7], float)
HOUR_DV = np.array([5, 4, 3, 2, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 7, 7, 7, 7, 6], float)


def when(r, y, m, dv):
    d = int(r.integers(1, days_in(y, m) + 1))
    h = int(r.choice(24, p=(HOUR_DV if dv else HOUR_STREET) / (HOUR_DV if dv else HOUR_STREET).sum()))
    return dt.datetime(y, m, d, h, int(r.integers(0, 60)), int(r.integers(0, 60)))


def report_delay(r, kind):
    """Minutes from the offense to the report: most within the hour; domestic victims often days later."""
    u = r.random()
    if kind.startswith("dv"):
        if u < 0.62:
            return int(r.integers(4, 90))
        if u < 0.86:
            return int(r.integers(90, 60 * 30))
        if u < 0.985:
            return int(r.integers(60 * 30, 60 * 24 * 21))
        return int(r.integers(60 * 24 * 21, 60 * 24 * 150))
    if u < 0.80:
        return int(r.integers(2, 75))
    if u < 0.96:
        return int(r.integers(75, 60 * 24))
    if u < 0.995:
        return int(r.integers(60 * 24, 60 * 24 * 10))
    return int(r.integers(60 * 24 * 10, 60 * 24 * 90))


def age(r, kind):
    if kind.startswith("dv"):
        return int(np.clip(r.normal(33, 10), 14, 79))
    return int(np.clip(r.gamma(5.2, 5.6) + 8, 13, 88))


def _choice(r, pairs, n):
    vals, ps = zip(*pairs)
    ps = np.array(ps, float)
    idx = r.choice(len(vals), size=n, p=ps / ps.sum())
    return [vals[i] for i in idx]


def _times(r, y, m, n, dv):
    days = r.integers(1, days_in(y, m) + 1, size=n)
    hp = (HOUR_DV if dv else HOUR_STREET) / (HOUR_DV if dv else HOUR_STREET).sum()
    hours = r.choice(24, size=n, p=hp)
    mins = r.integers(0, 60, size=n)
    secs = r.integers(0, 60, size=n)
    return [dt.datetime(y, m, int(d), int(h), int(mi), int(se)) for d, h, mi, se in zip(days, hours, mins, secs)]


def _delays(r, kind, n):
    u = r.random(n)
    if kind.startswith("dv"):
        cuts = ((0.62, 4, 90), (0.86, 90, 60 * 30), (0.985, 60 * 30, 60 * 24 * 21), (1.01, 60 * 24 * 21, 60 * 24 * 150))
    elif kind in ("robbery", "homicide"):
        cuts = ((1.01, 2, 120),)
    else:
        cuts = ((0.80, 2, 75), (0.96, 75, 60 * 24), (0.995, 60 * 24, 60 * 24 * 10), (1.01, 60 * 24 * 10, 60 * 24 * 90))
    out = np.empty(n, dtype=np.int64)
    lo_u = 0.0
    for cu, a, b in cuts:
        sel = (u >= lo_u) & (u < cu)
        out[sel] = r.integers(a, b, size=int(sel.sum()))
        lo_u = cu
    return out


def _ages(r, kind, n):
    if kind.startswith("dv"):
        return np.clip(r.normal(33, 10, size=n), 14, 79).astype(int)
    return np.clip(r.gamma(5.2, 5.6, size=n) + 8, 13, 88).astype(int)


def simulate(seed=W.SEED):
    """Return the victims (assault victims, and the victims of robbery and homicide incidents) and the incidents as
    dicts. Victims are drawn by month of occurrence and belong to the month they were reported."""
    r = np.random.default_rng(seed)
    victims, incidents = [], []

    def add_incident(kind, at, rep, place):
        unf = r.random() < (0.045 if kind in ("assault_dv", "assault") else 0.025)
        incidents.append({"iid": len(incidents) + 1, "kind": kind, "occurred": at, "reported": rep, "place": place,
                          "unfounded": bool(unf)})
        return len(incidents)

    for y, m in months(dt.date(2020, 12, 1), W.EXTRACT_LAST):
        yy = max(y, 2021)
        for kind in W.STREET_KINDS + W.DV_KINDS:
            n = int(r.poisson(W.expected(kind, yy, m)))
            if not n:
                continue
            dv = kind in W.DV_KINDS
            pair_p = 0.07 if kind in ("fire_hit", "fire_miss", "knife", "other_weapon") else 0.035
            pairs = r.random(n) < pair_p
            ats = _times(r, y, m, n, dv)
            delays = _delays(r, kind, n)
            places = _choice(r, DV_PLACES if dv else STREET_PLACES, n)
            weapons = _choice(r, DV_WEAPON if kind == "dv_weapon" else KIND_WEAPON[kind], n)
            ages = _ages(r, kind, n)
            sexes = r.random(n) < (0.83 if dv else 0.36)
            rels = _choice(r, FAMILY if dv else STREET_REL, n)
            sev = r.random(n)
            ser = _choice(r, SERIOUS, n)
            mino = _choice(r, MINOR, n)
            hit = _choice(r, (("O", 0.5), ("I", 0.2), ("L", 0.3)), n)
            legacy_u = r.random(n)
            k = 0
            while k < n:
                size = 2 if (pairs[k] and k + 1 < n) else 1
                at = ats[k]
                rep = at + dt.timedelta(minutes=int(delays[k]))
                iid = add_incident("assault_dv" if dv else "assault", at, rep, places[k])
                for j in range(k, k + size):
                    weapon = weapons[j]
                    if kind == "fire_hit":
                        injury = hit[j]
                    elif kind in ("pw_serious", "dv_serious"):
                        injury = ser[j]
                    elif kind in ("knife", "other_weapon", "dv_weapon"):
                        injury = ser[j] if sev[j] < 0.55 else mino[j]
                    elif kind in ("threat", "dv_threat", "fire_miss"):
                        injury = "N"
                    else:
                        injury = mino[j]
                    if kind in ("fire_hit", "fire_miss", "knife", "other_weapon", "dv_weapon"):
                        line = LINE_OF_WEAPON[weapon]
                    else:
                        acc, line = 0.0, None
                        for ln, sh in W.LEGACY[kind].items():
                            acc += sh
                            if legacy_u[j] < acc:
                                line = ln
                                break
                        line = line or list(W.LEGACY[kind])[-1]
                    a = int(ages[j])
                    if j > k and a == victims[-1]["age"] and ("F" if sexes[j] else "M") == victims[-1]["sex"]:
                        a += 1
                    victims.append({"iid": iid, "kind": kind, "dv": dv, "line": line, "nibrs": W.NIBRS[kind],
                                    "weapon": weapon, "injury": injury, "rel": rels[j], "age": a,
                                    "sex": "F" if sexes[j] else "M", "vtype": "I"})
                k += size
        # robbery incidents: the robbery victim and, in some, an assault victim besides
        n = int(r.poisson(W.BASE["robbery"] * W.season("robbery", m) * W.level("robbery", yy, m)))
        if n:
            ats = _times(r, y, m, n, False)
            delays = _delays(r, "robbery", n)
            weapons = _choice(r, (("12", 0.30), ("11", 0.08), ("15", 0.02), ("20", 0.10), ("30", 0.06), ("35", 0.02),
                                  ("40", 0.42)), n)
            places = _choice(r, (("13", 0.40), ("05", 0.12), ("07", 0.10), ("18", 0.14), ("20", 0.12), ("24", 0.12)), n)
            u = r.random((n, 6))
            ages = _ages(r, "robbery", n)
            ages2 = _ages(r, "robbery", n)
            ser = _choice(r, SERIOUS, n)
            mino = _choice(r, MINOR, n)
            for j in range(n):
                iid = add_incident("robbery", ats[j], ats[j] + dt.timedelta(minutes=int(delays[j])), places[j])
                business = places[j] in ("05", "07", "24") and u[j, 0] < 0.8
                victims.append({"iid": iid, "kind": "robbery", "dv": False, "line": ROB_LINE[weapons[j]],
                                "nibrs": "120", "weapon": weapons[j], "injury": mino[j] if u[j, 1] < 0.3 else "N",
                                "rel": "ST", "age": int(ages[j]), "sex": "F" if u[j, 2] < 0.38 else "M",
                                "vtype": "B" if business else "I"})
                if u[j, 3] < W.ROB_EXTRA:
                    for e in range(1 + (u[j, 4] < 0.1)):
                        w2 = weapons[j]
                        victims.append({"iid": iid, "kind": "rob_extra", "dv": False, "line": ROB_LINE[w2],
                                        "nibrs": "13A", "weapon": w2,
                                        "injury": ser[j] if (w2 == "40" or u[j, 5] < 0.5) else "N",
                                        "rel": "ST", "age": int(ages2[j]) + e, "sex": "F" if u[j, 2] > 0.6 else "M",
                                        "vtype": "I"})
        # homicide incidents: the dead and, in some, the wounded
        n = int(r.poisson(W.BASE["homicide"] * W.season("homicide", m) * W.level("homicide", yy, m)))
        if n:
            ats = _times(r, y, m, n, False)
            delays = _delays(r, "homicide", n)
            places = _choice(r, (("13", 0.45), ("20", 0.35), ("18", 0.12), ("03", 0.08)), n)
            weapons = _choice(r, (("12", 0.62), ("11", 0.18), ("20", 0.10), ("40", 0.05), ("30", 0.05)), n)
            u = r.random((n, 4))
            rels = _choice(r, STREET_REL, 2 * n)
            ages = _ages(r, "homicide", 2 * n)
            hit = _choice(r, (("O", 0.5), ("I", 0.2), ("L", 0.3)), n)
            for j in range(n):
                iid = add_incident("homicide", ats[j], ats[j] + dt.timedelta(minutes=int(delays[j])), places[j])
                for d in range(1 + (u[j, 0] < 0.06)):
                    victims.append({"iid": iid, "kind": "homicide", "dv": False, "line": "1A", "nibrs": "09A",
                                    "weapon": weapons[j], "injury": "", "rel": rels[2 * j + d], "age": int(ages[2 * j + d]),
                                    "sex": "F" if u[j, 1] < 0.18 else "M", "vtype": "I"})
                if u[j, 2] < W.HOM_EXTRA:
                    taken = {v["age"] for v in victims[-3:] if v["iid"] == iid}
                    for e in range(1 + (u[j, 3] < 0.45)):
                        a = int(ages[2 * j + 1]) + e
                        while a in taken:
                            a += 1
                        taken.add(a)
                        victims.append({"iid": iid, "kind": "hom_extra", "dv": False, "line": "1A", "nibrs": "13A",
                                        "weapon": weapons[j], "injury": hit[j], "rel": rels[2 * j + 1 - e % 2],
                                        "age": a, "sex": "M" if (u[j, 1] + 0.3 * e) % 1 < 0.75 else "F",
                                        "vtype": "I"})
    return victims, incidents


def other_offenses(seed=W.SEED):
    """Offenses other than assault, robbery and homicide, reported from January 2021: the extract carries those
    reported from October 2024, the Return A workbooks tally the Part I lines by month reported. Some protective-order
    violations, vandalism and burglaries are domestic and reach the Domestic Violence Unit's log."""
    r = np.random.default_rng(seed * 7 + 3)
    rows = []
    dv_share = {"90Z": 0.24, "290": 0.06, "220": 0.03}
    for y, m in months(dt.date(2020, 12, 1), W.EXTRACT_LAST):
        trend = {2020: 1.07, 2021: 1.06, 2022: 1.04, 2023: 1.02, 2024: 1.0, 2025: 0.98, 2026: 0.97}[y]
        for code, line, base, vt in OTHER:
            if not base:
                continue
            season = W.STREET[m - 1] ** (0.25 if code in ("23H", "23F") else 0.35)
            n = int(r.poisson(base * season * trend))
            if not n:
                continue
            ats = _times(r, y, m, n, False)
            dl = r.integers(5, 60 * 24 * 3, size=n)
            unf = r.random(n) < 0.02
            dv = r.random(n) < dv_share.get(code, 0.0)
            places = _choice(r, STREET_PLACES, n)
            rels = _choice(r, FAMILY, n)
            ages = _ages(r, "other", n)
            sexes = r.random(n)
            for j in range(n):
                rows.append({"code": code, "line": line, "occurred": ats[j],
                             "reported": ats[j] + dt.timedelta(minutes=int(dl[j])), "vtype": vt,
                             "place": "20" if dv[j] else places[j], "age": int(ages[j]) if vt == "I" else None,
                             "sex": ("F" if sexes[j] < (0.8 if dv[j] else 0.48) else "M") if vt == "I" else "",
                             "unfounded": bool(unf[j]), "dv": bool(dv[j]), "rel": rels[j] if dv[j] else ""})
    return rows
