"""task481 methods: the restatement and its rivals, computed from the shipped tables only (the extract's rows, the
Return A tallies, the Domestic Violence Unit's log), so the checks, the golden and the verifier share one reading."""
import collections
import datetime as dt

import world as W

AGG = ("4A", "4B", "4C", "4D")
ROB = ("3A", "3B", "3C", "3D")
DUAL = ((2024, 10), (2024, 11), (2024, 12))
JAN_SEP = tuple((2024, m) for m in range(1, 10))
MONTHS_2024 = tuple((2024, m) for m in range(1, 13))
MONTHS_2025 = tuple((2025, m) for m in range(1, 13))
E = {c: i for i, c in enumerate(["incident_number", "report_datetime_utc", "incident_date", "incident_hour",
                                  "offense_seq", "offense_code", "attempt_complete", "location_code", "weapon_force_1",
                                  "victim_seq", "victim_type", "victim_age", "victim_sex", "injury_1",
                                  "relationship_1", "ucr_summary_class", "cleared_by", "clearance_date"])}
D = {c: i for i, c in enumerate(["case_no", "rms_incident", "report_date", "case_opened", "offense_category",
                                  "ucr_line", "nibrs_offense", "relationship", "victim_sex", "victim_age",
                                  "lethality_screen", "case_status"])}
_cache = {}


def local_month(stamp, utc=True):
    """The local (y, m) of an extract stamp; utc=False reads the stamp's date as if it were local."""
    key = (stamp, utc)
    if key not in _cache:
        t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
        if utc:
            t = t.replace(tzinfo=dt.timezone.utc).astimezone(W.TZ)
        _cache[key] = (t.year, t.month)
    return _cache[key]


def is_dv(rel):
    return rel in W.DV_RELATIONSHIPS


def nibrs_13a(rows, utc=True):
    c = collections.Counter()
    for r in rows:
        if r[E["offense_code"]] == "13A":
            c[local_month(r[E["report_datetime_utc"]], utc)] += 1
    return c


def dual_tables(rows, utc=True):
    """The October to December 2024 victims by summary class: totals and 13A, the simple-assault class split by
    domestic relationship; the 13A victims the hierarchy left unscored, by the incident's scored offense."""
    tot, to13a = collections.Counter(), collections.Counter()
    inc_codes = collections.defaultdict(set)
    for r in rows:
        if local_month(r[E["report_datetime_utc"]], utc) in DUAL:
            inc_codes[r[E["incident_number"]]].add(r[E["offense_code"]])
    rob_inc, hom_vic = set(), 0
    for r in rows:
        if local_month(r[E["report_datetime_utc"]], utc) not in DUAL:
            continue
        cls, code = r[E["ucr_summary_class"]], r[E["offense_code"]]
        if cls in AGG or cls == "4E":
            key = cls if cls != "4E" else ("4E_dv" if is_dv(r[E["relationship_1"]]) else "4E_non")
            tot[key] += 1
            if code == "13A":
                to13a[key] += 1
        elif cls == "NS" and code == "13A":
            codes = inc_codes[r[E["incident_number"]]]
            key = "hid_hom" if "09A" in codes else "hid_rob"
            to13a[key] += 1
        if code == "120" and cls in ROB:
            rob_inc.add(r[E["incident_number"]])
        if code == "09A" and cls == "1A":
            hom_vic += 1
    tot["hid_rob"], tot["hid_hom"] = len(rob_inc), hom_vic
    return tot, to13a


def dvu_4e(dvu, months=JAN_SEP):
    c = collections.Counter()
    for d in dvu:
        y, m = int(d[D["report_date"]][:4]), int(d[D["report_date"]][5:7])
        if (y, m) in months and d[D["ucr_line"]] == "4E" and d[D["case_status"]] != "UNFOUNDED":
            c[(y, m)] += 1
    return c


def restate(rows, ra, dvu, split_dv=True, per_line=True, link=False, utc=True, dvu_months=None):
    """2024 restated by month: October to December as NIBRS counted them, January to September converted at the
    dual-coded months' rates. Returns (by month, rates, the bridge lines)."""
    tot, to13a = dual_tables(rows, utc)
    n13 = nibrs_13a(rows, utc)
    rate = {k: to13a[k] / tot[k] for k in tot if tot[k]}
    act = lambda ym, line: ra[ym][line][2]
    dv = dvu_4e(dvu) if dvu_months is None else dvu_months
    out, bridge = {}, collections.Counter()
    agg_q4 = sum(act(ym, l) for ym in DUAL for l in AGG)
    q4_13a = sum(n13[ym] for ym in DUAL)
    for ym in MONTHS_2024:
        if ym in DUAL:
            out[ym] = float(n13[ym])
            continue
        agg = sum(act(ym, l) for l in AGG)
        if link:
            out[ym] = agg * q4_13a / agg_q4
            continue
        v = 0.0
        if per_line:
            for l in AGG:
                v += rate[l] * act(ym, l)
                bridge["lost"] += (1 - rate[l]) * act(ym, l)
        else:
            p = sum(to13a[l] for l in AGG) / sum(tot[l] for l in AGG)
            v += p * agg
            bridge["lost"] += (1 - p) * agg
        e4 = act(ym, "4E")
        if split_dv:
            g = rate["4E_dv"] * dv[ym] + rate["4E_non"] * (e4 - dv[ym])
        else:
            g = (to13a["4E_dv"] + to13a["4E_non"]) / (tot["4E_dv"] + tot["4E_non"]) * e4
        v += g
        bridge["gained"] += g
        h = rate["hid_rob"] * sum(act(ym, l) for l in ROB) + rate["hid_hom"] * act(ym, "1A")
        v += h
        bridge["hidden"] += h
        out[ym] = v
    # the dual-coded months' own lines
    bridge["lost"] += sum(tot[l] - to13a[l] for l in AGG)
    bridge["gained"] += to13a["4E_dv"] + to13a["4E_non"]
    bridge["hidden"] += to13a["hid_rob"] + to13a["hid_hom"]
    return out, rate, bridge


IP_CODES = ("BG", "SE", "CS", "XR", "XS")
IP_LOG = ("Intimate partner (current)", "Intimate partner (former)")


THREAT_CODES = ("13C",)


def restate_grain(rows, ra, dvu, split=("4E",), rel=False, rob_lines=False, by=None):
    """2024 restated at a finer or coarser grain than the golden's: the lines in `split` converted separately for
    domestic and other victims, each January to September month at its own counts from the unit's log. The domestic
    victims split again by `by`: 'rel' (intimate partners and other family), 'category' (the unit's assault and threat
    categories), 'sex'; rel=True is by='rel'. rob_lines: the hidden robbery rate per robbery line."""
    by = by or ("rel" if rel else None)

    def group(dv, sub):
        return "non" if not dv else (sub if by else "dv")
    tot, k13 = collections.Counter(), collections.Counter()
    inc_codes, inc_rob = collections.defaultdict(set), {}
    for r in rows:
        if local_month(r[E["report_datetime_utc"]]) in DUAL:
            inc_codes[r[E["incident_number"]]].add(r[E["offense_code"]])
            if r[E["offense_code"]] == "120" and r[E["ucr_summary_class"]] in ROB:
                inc_rob[r[E["incident_number"]]] = r[E["ucr_summary_class"]]
    hom_vic = 0
    for r in rows:
        if local_month(r[E["report_datetime_utc"]]) not in DUAL:
            continue
        cls, code, rl = r[E["ucr_summary_class"]], r[E["offense_code"]], r[E["relationship_1"]]
        if cls in AGG or cls == "4E":
            sub = {"rel": "ip" if rl in IP_CODES else "fam",
                   "category": "threat" if code in THREAT_CODES else "assault",
                   "sex": r[E["victim_sex"]], None: None}[by]
            key = (cls, group(is_dv(rl), sub) if cls in split else "all")
            tot[key] += 1
            k13[key] += code == "13A"
        elif cls == "NS" and code == "13A":
            inc = r[E["incident_number"]]
            k13[("hom",) if "09A" in inc_codes[inc] else (("rob", inc_rob[inc]) if rob_lines else ("rob",))] += 1
        if code == "09A" and cls == "1A":
            hom_vic += 1
    for inc, line in inc_rob.items():
        tot[("rob", line) if rob_lines else ("rob",)] += 1
    tot[("hom",)] = hom_vic
    rate = {k: k13[k] / tot[k] for k in tot if tot[k]}
    log = collections.Counter()
    for d in dvu:
        ym = (int(d[D["report_date"]][:4]), int(d[D["report_date"]][5:7]))
        if ym in JAN_SEP and d[D["case_status"]] != "UNFOUNDED" and d[D["ucr_line"]] in split:
            sub = {"rel": "ip" if d[D["relationship"]] in IP_LOG else "fam",
                   "category": "threat" if d[D["offense_category"]].startswith("Threats") else "assault",
                   "sex": d[D["victim_sex"]], None: None}[by]
            log[(ym, d[D["ucr_line"]], group(True, sub))] += 1
    n13 = nibrs_13a(rows)
    total = float(sum(n13[ym] for ym in DUAL))
    for ym in JAN_SEP:
        for line in AGG + ("4E",):
            a = ra[ym][line][2]
            if line in split:
                subs = {"rel": ("ip", "fam"), "category": ("assault", "threat"), "sex": ("F", "M"), None: ("dv",)}[by]
                dv = {g: log[(ym, line, g)] for g in subs}
                total += sum(rate.get((line, g), 0.0) * n for g, n in dv.items())
                total += rate[(line, "non")] * (a - sum(dv.values()))
            else:
                total += rate[(line, "all")] * a
        if rob_lines:
            total += sum(rate.get(("rob", l), 0.0) * ra[ym][l][2] for l in ROB)
        else:
            total += rate[("rob",)] * sum(ra[ym][l][2] for l in ROB)
        total += rate[("hom",)] * ra[ym]["1A"][2]
    return total


GRAINS = {"the golden's grain (4e by domestic and other)": dict(),
          "every line by domestic and other": dict(split=("4A", "4B", "4C", "4D", "4E")),
          "4e by intimate partner, other family and other": dict(rel=True),
          "every line by intimate partner, other family and other": dict(split=("4A", "4B", "4C", "4D", "4E"),
                                                                         rel=True),
          "4e by domestic assaults, domestic threats and other": dict(by="category"),
          "every line by domestic assaults, domestic threats and other": dict(split=("4A", "4B", "4C", "4D", "4E"),
                                                                              by="category"),
          "4e by domestic victims' sex and other": dict(by="sex"),
          "4e by domestic and other, hidden robbery victims per robbery line": dict(rob_lines=True)}


def ladder(rows, ra, dvu, utc=True):
    """Every route the design names, as the change from 2024 to 2025 on the NIBRS basis."""
    n13 = nibrs_13a(rows, utc)
    y25 = sum(n13[ym] for ym in MONTHS_2025)
    pub24 = sum(ra[ym][l][2] for ym in MONTHS_2024 for l in AGG)
    res = {"published_2024": pub24, "nibrs_2025": y25, "raw": y25 / pub24 - 1}
    for name, kw in (("golden", {}), ("per_line", {"split_dv": False}), ("link", {"link": True}),
                     ("dv_pooled_agg", {"per_line": False}), ("pooled_all", {"per_line": False, "split_dv": False})):
        by_month, _, _ = restate(rows, ra, dvu, utc=utc, **kw)
        tot = sum(by_month.values())
        res[name + "_2024"] = tot
        res[name] = y25 / tot - 1
    q4_24 = sum(n13[ym] for ym in DUAL)
    q4_25 = sum(n13[(2025, m)] for m in (10, 11, 12))
    res["q4_to_q4"] = q4_25 / q4_24 - 1
    return res


# ------------------------------------------------------------------------------------------------ shootings
G = {c: i for i, c in enumerate(["gvr_id", "rms_number", "shot_datetime", "block", "inside_city", "victim_age",
                                  "victim_sex", "circumstance", "outcome", "entered", "analyst"])}
MEC = {c: i for i, c in enumerate(["me_case", "date_of_injury", "injury_location", "date_of_death", "age", "sex",
                                    "cause", "manner"])}
QUARTERS = tuple("%dQ%d" % (y, q) for y in (2023, 2024, 2025) for q in (1, 2, 3, 4))


def quarter_of(stamp):
    return "%sQ%d" % (stamp[:4], (int(stamp[5:7]) - 1) // 3 + 1)


def base_block(block):
    return block.split(" (")[0]


def shot_local(g, clock=True):
    """The shot time in Ellsmere local time: the rows the records system entered (from 1 October 2024) hold it in UTC,
    as that system stores every time; clock=False reads every row as stored."""
    s = g[G["shot_datetime"]]
    if clock and g[G["entered"]] >= "2024-10-01":
        t = dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).astimezone(W.TZ)
        return t.strftime("%Y-%m-%d %H:%M")
    return s


def shootings(gvr, me, deaths=True, township=True, dedup="person", events="place_time", clock=True):
    """Non-fatal shooting victims and the shootings they were hurt in, by quarter shot. deaths: drop the people the
    Medical Examiner's list shows died of the wound; township: leave out the blocks the log places outside the city
    (the township blocks the old database marked inside by the patrol beat); dedup: 'person' (same report number, time,
    age and sex), 'number' (one row a report number), None; events: 'place_time' (same block and minute) or 'number';
    clock: the records system's UTC shot times put in local time first."""
    died = set()
    if deaths:
        for d in me:
            loc = d[MEC["injury_location"]]
            if loc.endswith(", ELLSMERE"):
                died.add((d[MEC["date_of_injury"]], loc[: -len(", ELLSMERE")], str(d[MEC["age"]]), d[MEC["sex"]]))
    outside = {base_block(g[G["block"]]) for g in gvr if g[G["inside_city"]] == "N"} if township else set()
    seen, vic, ev = set(), collections.Counter(), collections.defaultdict(set)
    for g in gvr:
        if g[G["circumstance"]] != "ASSAULT" or g[G["inside_city"]] != "Y" or g[G["outcome"]] != "WOUNDED":
            continue
        if g[G["block"]] in outside:
            continue
        when = shot_local(g, clock)
        if (when[:10], g[G["block"]], str(g[G["victim_age"]]), g[G["victim_sex"]]) in died:
            continue
        if dedup == "person":
            key = (g[G["rms_number"]], when, str(g[G["victim_age"]]), g[G["victim_sex"]])
        elif dedup == "number":
            key = g[G["rms_number"]]
        else:
            key = g[G["gvr_id"]]
        if key in seen:
            continue
        seen.add(key)
        q = quarter_of(when)
        if q not in QUARTERS:
            continue
        vic[q] += 1
        ev[q].add((when, g[G["block"]]) if events == "place_time" else g[G["rms_number"]])
    return {q: vic[q] for q in QUARTERS}, {q: len(ev[q]) for q in QUARTERS}


# ------------------------------------------------------------------------------------------------ readers
MONTH_ABBR = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
              "Nov": 11, "Dec": 12}
OLD_LABEL = {"1a.": "1A", "1b.": "1B", "2.": "2", "a. Firearm": None}


def read_csv(path):
    import csv
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))[1:]


def read_return_a(path):
    """{(year, month): {line: [reported, unfounded, actual, cleared, cleared_juvenile]}} from one year's workbook, in
    either layout (the department's own form, or the state template with the line codes in column A)."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = {}
    order = ["1A", "1B", "2", "3", "3A", "3B", "3C", "3D", "4", "4A", "4B", "4C", "4D", "4E", "5", "5A", "5B", "5C",
             "6", "7", "7A", "7B", "7C"]
    for ws in wb.worksheets:
        mon, year = ws.title.split()
        key = (int(year), MONTH_ABBR[mon])
        rows = [r for r in ws.iter_rows(values_only=True)]
        start = next(i for i, r in enumerate(rows) if r and r[0] in ("Line", "Classification of offenses"))
        body = rows[start + 1: start + 1 + len(order)]
        table = {}
        for code, r in zip(order, body):
            vals = [v for v in r if isinstance(v, int)]
            table[code] = vals[-5:]
        out[key] = table
    return out


def restate_months(rows, ra, dvu, months, split_dv=True):
    """Any legacy months restated at the October to December 2024 rates (2023 and January to September 2024 for the
    chart)."""
    tot, to13a = dual_tables(rows)
    rate = {k: to13a[k] / tot[k] for k in tot if tot[k]}
    dv = dvu_4e(dvu, months)
    out = {}
    for ym in months:
        act = lambda line: ra[ym][line][2]
        v = sum(rate[l] * act(l) for l in AGG)
        if split_dv:
            v += rate["4E_dv"] * dv[ym] + rate["4E_non"] * (act("4E") - dv[ym])
        else:
            v += (to13a["4E_dv"] + to13a["4E_non"]) / (tot["4E_dv"] + tot["4E_non"]) * act("4E")
        v += rate["hid_rob"] * sum(act(l) for l in ROB) + rate["hid_hom"] * act("1A")
        out[ym] = v
    return out
