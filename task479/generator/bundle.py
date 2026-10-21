"""Read the cut pack the way an analyst would, and run every route the design names on it: the golden's and each
wrong rung's. Nothing here reads world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the conformed Monitor reports, the register, the crosswalk and the Department's reports
    estimate(b, route)      each county's tax year 2025 receipts on the Department's basis under a route
    qualify(b, est)         the counties at or above the 6 per cent floor
    ask_a(b, county_from)   January to August 2026 occupancy and average daily rate by county
    ask_b(b, link)          the January 2018 panel's properties still reporting in August 2026, and their rooms share"""
import calendar
import csv
import datetime as dt
import os
import re

import numpy as np

FILES = {
    "legacy": "tla_monitor_reports_2018-01_to_2022-03.csv",
    "current": "tla_monitor_reports_2022-04_to_2026-09.csv",
    "register": "tla_monitor_properties_2026-10-02.csv",
    "xwalk": "innsight_property_id_crosswalk_2022-04.csv",
}
BENCH = list(range(2018, 2025))
THRESHOLD = 0.06
FUND = 1_800_000
ROUTES = ("ols", "ols_revised", "ols_2021", "mean_change", "last_change", "half_step",
          "flat_2024", "mean_ratio", "pooled_drift", "dept_persist", "log_linear")
GOLDEN_FAMILY = ("ols", "ols_revised", "ols_2021", "mean_change", "last_change")


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _pdf_text(path):
    import pypdf
    return "\n".join(pg.extract_text() for pg in pypdf.PdfReader(path).pages)


def _dor_rows(txt):
    """The county rows of one report: {county: (code or None, [the numbers after the name])}."""
    toks = [t.strip() for t in txt.splitlines() if t.strip()]
    rows = {}
    for i, t in enumerate(toks):
        if re.fullmatch(r"[A-Z][a-z]+(?: [A-Z][a-z]+)?", t) and i + 3 < len(toks) and re.fullmatch(r"-?[\d,]+", toks[i + 1]):
            code = toks[i - 1] if re.fullmatch(r"\d\d", toks[i - 1]) else None
            nums = []
            for u in toks[i + 1:i + 6]:
                if re.fullmatch(r"-?[\d,.]+%?", u):
                    nums.append(u)
                else:
                    break
            if t != "State":
                rows[t] = (code, nums)
    return rows


def read_dor(target):
    """Each report's first print for its tax year and its revised prior year, by county, in dollars."""
    first, revised, code = {}, {}, {}
    for y in BENCH:
        txt = _pdf_text(os.path.join(target, "tdor_taxable_lodging_receipts_ty%d.pdf" % y))
        mult = 1000 if "thousands of dollars" in txt else 1
        rows = _dor_rows(txt)
        assert len(rows) == 16, (y, sorted(rows))
        for c, (cd, nums) in rows.items():
            vals = [int(v.replace(",", "")) for v in nums if not v.endswith("%")]
            cur, prev = (vals[0], vals[1]) if mult == 1000 else (vals[1], vals[2])
            first[(c, y)] = cur * mult
            if y > 2018:
                revised[(c, y - 1)] = prev * mult
            if cd:
                code[cd] = c
    return first, revised, sorted({c for c, _ in first}), code


def load(target):
    reg = _csv(os.path.join(target, FILES["register"]))
    first, revised, counties, code = read_dor(target)
    # legacy: the latest received report per property and month; county names in one case
    leg = {}
    for r in _csv(os.path.join(target, FILES["legacy"])):
        mm, yy = r["Report Month"].split("/")
        when = dt.datetime.strptime(r["Received"], "%m/%d/%Y %H:%M")
        key = (r["Property ID"], int(yy), int(mm))
        if key not in leg or when >= leg[key]["when"]:
            leg[key] = {"id": r["Property ID"], "name": r["Property Name"], "county": r["County"].title(),
                        "y": int(yy), "m": int(mm), "avail": int(r["Rooms Available"]), "sold": int(r["Rooms Sold"]),
                        "rev": float(r["Room Revenue"]), "when": when}
    cur = {}
    for r in _csv(os.path.join(target, FILES["current"])):
        yy, mm = r["period"].split("-")
        when = r["submitted_at_utc"]
        key = (r["prop_id"], int(yy), int(mm))
        if key not in cur or when >= cur[key]["when"]:
            cur[key] = {"id": r["prop_id"], "county": code[r["county_code"]], "y": int(yy), "m": int(mm),
                        "avail": int(r["avail_room_nights"]), "sold": int(r["sold_room_nights"]),
                        "rev": int(r["room_revenue_cents"]) / 100.0, "when": when}
    xw = {r["legacy_property_id"]: r["innsight_prop_id"] for r in _csv(os.path.join(target, FILES["xwalk"]))}
    return {"reg": reg, "leg": leg, "cur": cur, "first": first, "revised": revised, "counties": counties,
            "xwalk": xw, "code": code}


def panel(b):
    t = {}
    for src in (b["leg"], b["cur"]):
        for r in src.values():
            if r["y"] <= 2025:
                t[(r["county"], r["y"])] = t.get((r["county"], r["y"]), 0.0) + r["rev"]
    return t


def estimate(b, route):
    P = panel(b)
    F, R = b["first"], b["revised"]
    ys = np.array(BENCH, dtype=float)
    out = {}
    ratios = {c: np.array([F[(c, y)] / P[(c, y)] for y in BENCH]) for c in b["counties"]}
    pooled = np.mean([np.polyfit(ys, ratios[c], 1)[0] / ratios[c][-1] for c in b["counties"]])
    for c in b["counties"]:
        r = ratios[c]
        if route == "ols":
            k, a = np.polyfit(ys, r, 1)
            r25 = a + k * 2025
        elif route == "ols_revised":
            rv = np.array([(R[(c, y)] if (c, y) in R else F[(c, y)]) / P[(c, y)] for y in BENCH])
            k, a = np.polyfit(ys, rv, 1)
            r25 = (a + k * 2025) * F[(c, 2024)] / (R.get((c, 2024), F[(c, 2024)]))
        elif route == "ols_2021":
            k, a = np.polyfit(ys[3:], r[3:], 1)
            r25 = a + k * 2025
        elif route == "mean_change":
            r25 = r[-1] + np.mean(np.diff(r))
        elif route == "last_change":
            r25 = 2 * r[-1] - r[-2]
        elif route == "half_step":
            r25 = r[-1] + 0.5 * np.polyfit(ys, r, 1)[0]
        elif route == "log_linear":
            k, a = np.polyfit(ys, np.log(r), 1)
            r25 = np.exp(a + k * 2025)
        elif route == "flat_2024":
            r25 = r[-1]
        elif route == "mean_ratio":
            r25 = r.mean()
        elif route == "pooled_drift":
            r25 = r[-1] * (1 + pooled)
        elif route == "dept_persist":
            g = F[(c, 2024)] / R[(c, 2023)] - 1
            out[c] = F[(c, 2024)] * (1 + g)
            continue
        out[c] = r25 * P[(c, 2025)]
    return out


def growth(b, est):
    return {c: est[c] / b["first"][(c, 2024)] - 1 for c in est}


def qualify(b, est):
    g = growth(b, est)
    return sorted(c for c in g if g[c] >= THRESHOLD)


def fit_residuals(b):
    """Each county's largest absolute residual from the straight line and from the log-linear line, per cent."""
    P = panel(b)
    ys = np.array(BENCH, dtype=float)
    out = {}
    for c in b["counties"]:
        r = np.array([b["first"][(c, y)] / P[(c, y)] for y in BENCH])
        k, a = np.polyfit(ys, r, 1)
        lin = np.max(np.abs(r / (a + k * ys) - 1)) * 100
        k2, a2 = np.polyfit(ys, np.log(r), 1)
        lg = np.max(np.abs(r / np.exp(a2 + k2 * ys) - 1)) * 100
        out[c] = (lin, lg)
    return out


def backtest(b):
    """How carrying the last benchmark by the panel's growth would have done for each year 2019 to 2024 (first
    print over the carried figure, less one), per county."""
    P = panel(b)
    return {c: [b["first"][(c, y)] / (b["first"][(c, y - 1)] * P[(c, y)] / P[(c, y - 1)]) - 1 for y in BENCH[1:]]
            for c in b["counties"]}


# ------------------------------------------------------------------------------------------------ ask A
def ask_a(b, county_from="register"):
    """January to August 2026 occupancy (per cent) and average daily rate (dollars) by county. county_from:
    'register' (the property's county in the register), 'report' (the county code on each report)."""
    regc = {r["prop_id"]: r["county"] for r in b["reg"]}
    s = {}
    for r in b["cur"].values():
        if r["y"] != 2026 or r["m"] > 8:
            continue
        c = regc[r["id"]] if county_from == "register" else r["county"]
        a = s.setdefault(c, [0, 0, 0.0])
        a[0] += r["avail"]
        a[1] += r["sold"]
        a[2] += r["rev"]
    return {c: (100.0 * v[1] / v[0], v[2] / v[1]) for c, v in s.items()}


def ask_a_raw(target, county_from="register"):
    """Ask A on every row as delivered, no resubmission resolved (the mirror's half-handled read)."""
    b = load(target)
    regc = {r["prop_id"]: r["county"] for r in b["reg"]}
    s = {}
    for r in _csv(os.path.join(target, FILES["current"])):
        yy, mm = r["period"].split("-")
        if int(yy) != 2026 or int(mm) > 8:
            continue
        c = regc[r["prop_id"]] if county_from == "register" else b["code"][r["county_code"]]
        a = s.setdefault(c, [0, 0, 0.0])
        a[0] += int(r["avail_room_nights"])
        a[1] += int(r["sold_room_nights"])
        a[2] += int(r["room_revenue_cents"]) / 100
    return {c: (100.0 * v[1] / v[0], v[2] / v[1]) for c, v in s.items()}


# ------------------------------------------------------------------------------------------------ ask B
def link(b, how="rooms"):
    """Legacy id to InnSight id: the crosswalk, and with how='rooms' every legacy property reporting in March 2022
    that the crosswalk misses matched to the InnSight property in the same county first reporting in April 2022
    with the same rooms (room-nights over the month's days), which the crosswalk also misses."""
    m = dict(b["xwalk"])
    if how == "crosswalk":
        return m
    regc = {r["prop_id"]: r["county"] for r in b["reg"]}
    mapped_new = set(m.values())
    lost = [r for (i, y, mo), r in b["leg"].items() if (y, mo) == (2022, 3) and i not in m]
    found = [r for (i, y, mo), r in b["cur"].items() if (y, mo) == (2022, 4) and i not in mapped_new]
    for r in lost:
        rooms = r["avail"] // 31
        cand = [f for f in found if regc[f["id"]] == r["county"] and f["avail"] // 30 == rooms]
        if how == "name":
            names = {x["prop_id"]: x["property_name"] for x in b["reg"]}
            cand = [f for f in found if names[f["id"]] == r["name"]]
        if len(cand) == 1:
            m[r["id"]] = cand[0]["id"]
    return m


def ask_b(b, how="rooms"):
    """Per county, for the properties reporting in January 2018 that still report in August 2026: the share of
    January 2018's panel rooms they hold, and the change in their rooms from January 2018 to August 2026, both per
    cent (rooms are a month's room-nights available over its days)."""
    m = link(b, how)
    aug = {i: r["avail"] / 31 for (i, y, mo), r in b["cur"].items() if (y, mo) == (2026, 8)}
    out = {}
    for (i, y, mo), r in b["leg"].items():
        if (y, mo) != (2018, 1):
            continue
        o = out.setdefault(r["county"], [0.0, 0.0, 0.0])
        rooms = r["avail"] / 31
        o[0] += rooms
        if m.get(i) in aug:
            o[1] += rooms
            o[2] += aug[m[i]]
    return {c: (100.0 * v[1] / v[0], 100.0 * (v[2] / v[1] - 1)) for c, v in out.items()}


def ask_b_unlinked(b):
    """The read with no linking: every property reporting in August 2026 against January 2018's panel rooms."""
    regc = {r["prop_id"]: r["county"] for r in b["reg"]}
    aug, base = {}, {}
    for (i, y, mo), r in b["cur"].items():
        if (y, mo) == (2026, 8):
            aug[regc[i]] = aug.get(regc[i], 0) + r["avail"] / 31
    for (i, y, mo), r in b["leg"].items():
        if (y, mo) == (2018, 1):
            base[r["county"]] = base.get(r["county"], 0) + r["avail"] / 31
    return {c: (100.0 * aug[c] / base[c], None) for c in base}
