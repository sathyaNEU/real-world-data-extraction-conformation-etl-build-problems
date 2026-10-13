"""The bureau's monthly fuel sales survey, the November 2026 submission log, and the two asks they carry.

The sales survey frame gives every station a survey reference. When a station closes and leaves the frame, its
reference is freed and can be given to a station that opens later; the frame snapshot then shows only the new holder,
while the returns the closed station filed under that reference still sit in the survey file with the name its
operator typed. Returns are revised now and then (the latest revision stands) and a few arrive after the month's
processing run and are processed with the next month.

The submission log holds every price change the platform received in November 2026, all grades, with its channel: a
brand's pricing desk submits the stations it prices through its own system, in the same minutes for all of them;
dealers submit from the forecourt terminal, some through a dealer group's or a software vendor's system, and now and
then by hand on the portal."""
import calendar
import datetime as dt
import math

import numpy as np

import market as M
import world as W

MONTHS = [dt.date(2026, m, 1) for m in range(1, 11)]
ASK_MONTHS = MONTHS[:3]


def rng(*key):
    return np.random.default_rng([W.SEED, 400] + [int(k) for k in key])


def month_end(m):
    return dt.date(m.year, m.month, calendar.monthrange(m.year, m.month)[1])


SEASON = {1: 0.86, 2: 0.83, 3: 0.95, 4: 1.0, 5: 1.06, 6: 1.12, 7: 1.18, 8: 1.16, 9: 1.03, 10: 0.98}


OPERATOR_FAMILY = ["Abernethy", "Baptiste", "Carvalho", "Dempster", "Easterbrook", "Fairweather", "Galloway",
                   "Hargreaves", "Ingram", "Jardine", "Kilbride", "Lachance", "Macaulay", "Nakamura", "Ostrowski",
                   "Pelletier", "Quinlan", "Rasmussen", "Sandhu", "Thibodeau", "Underhill", "Valois", "Whitlock",
                   "Yarrow", "Zelinski", "Ashdown", "Belcourt", "Corrigan", "Desrosiers", "Ellwood", "Forsythe",
                   "Gillies", "Hawthorne", "Iverson", "Keegan", "Lindqvist", "Morrissette", "Norquay", "Ouellette",
                   "Prendergast", "Rourke", "Sauvé", "Tolliver", "Vandermeer", "Wainwright", "Kowalczyk", "Dhaliwal"]
OPERATOR_FORM = ["Fuels Ltd.", "Holdings Inc.", "Petroleum Services Ltd.", "& Sons Ltd.", "Enterprises Inc.",
                 "Gas Bar Ltd.", "Service Centre Inc.", "Retail Ltd."]
ABBR = (("Street", "St"), ("Road", "Rd"), ("Avenue", "Ave"), ("Highway", "Hwy"), ("Drive", "Dr"), ("Lane", "Ln"))


def operator(s):
    """the business that runs a dealer or commission station, as it names itself on its returns"""
    g = np.random.default_rng([W.SEED, 400, 9, s.uid])
    return "%s %s" % (OPERATOR_FAMILY[int(g.integers(0, len(OPERATOR_FAMILY)))],
                      OPERATOR_FORM[int(g.integers(0, len(OPERATOR_FORM)))])


def reporting_name(s, m):
    """the reporting unit as the return names it: the brand's retail company for a site it runs, the operator's
    business otherwise, the station's own name when unbranded"""
    b = s.brand_on(max(m, s.opened))
    if b == W.INDEPENDENT:
        nm = s.indep_name
    elif s.model_on(max(m, s.opened)) == "COCO":
        nm = dict((c, o) for c, _, o, _ in W.BRANDS)[b]
    else:
        nm = operator(s)
    return nm.upper() if s.style == 1 else nm


def site_address(s):
    """the site as the respondent types it"""
    a = "%s, %s" % (s.street, W.AREA_NAME[s.area])
    if s.style == 1:
        return a.upper()
    if s.style == 2:
        for x, y in ABBR:
            a = a.replace(x, y)
        return a
    if s.style == 3:
        return a.replace(", ", " ") + " "
    return a


def returns(sim):
    """survey returns: one per station a month it traded, a few revised and a few processed late"""
    g = rng(1)
    rows = []
    for s in sorted(sim["stations"], key=lambda s: s.uid):
        for m in MONTHS:
            days = W.days_between(m, month_end(m))
            open_days = sum(1 for d in days if s.open_on(d))
            if open_days == 0 or month_end(m) < s.frame_added:
                continue                  # not trading, or not yet on the survey frame
            base = s.size * SEASON[m.month] * open_days / len(days)
            reg = int(round(base * (1 + g.normal(0, 0.035))))
            prem = int(round(reg * g.uniform(0.08, 0.14)))
            dsl = int(round(reg * g.uniform(0.18, 0.42)))
            nxt = (m + dt.timedelta(days=32)).replace(day=1)
            late = g.random() < 0.045
            proc = nxt if late else m
            received = nxt + dt.timedelta(days=int(g.integers(2, 11))) if not late else \
                nxt + dt.timedelta(days=int(g.integers(16, 27)))
            rows.append({"sfn": s.sfn, "ref": m, "proc": proc, "rev": 1, "name": reporting_name(s, m),
                         "addr": site_address(s), "reg": reg, "prem": prem, "dsl": dsl, "received": received, "uid": s.uid})
            if g.random() < 0.06:
                f = 1 + g.choice([-1, 1]) * g.uniform(0.012, 0.05)
                rows.append({"sfn": s.sfn, "ref": m, "proc": proc if g.random() < 0.5 else nxt, "rev": 2,
                             "name": reporting_name(s, m), "addr": site_address(s), "reg": int(round(reg * f)),
                             "prem": prem,
                             "dsl": int(round(dsl * (1 + g.normal(0, 0.01)))),
                             "received": received + dt.timedelta(days=int(g.integers(9, 40))), "uid": s.uid})
    rows = [r for r in rows if r["received"] <= W.AS_OF]          # what had arrived when the extract was pulled
    rows.sort(key=lambda r: (r["proc"], r["received"], r["sfn"], r["rev"]))
    return rows


def frame(sim):
    """the frame snapshot at the extract: current holders of every reference, closed stations still on it"""
    out = []
    holders = {}
    for s in sim["stations"]:
        if getattr(s, "reissued_to", None):
            continue          # its reference now belongs to the station that opened later
        holders[s.sfn] = s
    for sfn, s in sorted(holders.items()):
        out.append({"sfn": sfn, "station": s.new_id or s.old_id,
                    "status": "active" if s.closed is None else "closed",
                    "since": s.frame_added, "closed": s.closed})
    return out


def litres_by_brand(sim, rets):
    """the golden for the litres ask: the latest revision of each return, on the station that held the reference in
    the return's month, under the brand that station carried that month (from its first day open in the month, since
    brands change on the first); litres"""
    by = {}
    latest = {}
    for r in rets:
        k = (r["sfn"], r["ref"])
        if k not in latest or r["rev"] > latest[k]["rev"]:
            latest[k] = r
    st = sim["by_uid"]
    for (sfn, m), r in latest.items():
        if m not in ASK_MONTHS:
            continue
        s = st[r["uid"]]
        b = s.brand_on(max(m, s.opened))
        if b not in W.CODES:
            continue
        by[(b, m)] = by.get((b, m), 0) + r["reg"]
    return {b: [by.get((b, m), 0) for m in ASK_MONTHS] for b in W.CODES}


def thousands(x):
    return int(math.floor(x / 1000.0 + 0.5))


# ---------------------------------------------------------------- the November 2026 submissions
NOV = (W.DAY_INDEX[dt.date(2026, 11, 1)], W.DAY_INDEX[W.LOG_END])


def dealer_groups(sim):
    """dealer stations submitting through a dealer group's or a vendor's system: two of every brand, three unbranded"""
    g = rng(2)
    out = set()
    nov = dt.date(2026, 11, 1)
    for b in W.CODES + [W.INDEPENDENT]:
        c = [s for s in sim["stations"] if s.brand_on(nov) == b and s.open_on(nov) and not s.brand_priced_on(nov)]
        k = 3 if b == W.INDEPENDENT else 2
        for i in g.choice(len(c), size=k, replace=False):
            out.add(c[int(i)].uid)
    return out


def submissions(sim):
    """{rows}: every submission received in November 2026, all grades"""
    g = rng(3)
    groups = dealer_groups(sim)
    rows = []
    lo, hi = NOV
    dsl_rack = sim["rack"]["ULSD"]
    for s in sorted(sim["stations"], key=lambda s: s.uid):
        ev = [e for e in sim["events"][s.uid] if lo <= e[0] <= hi]
        if not ev:
            continue
        cur_d = None
        for k, minute, price in ev:
            d = W.DAYS[k]
            priced = s.brand_priced_on(d)
            ch = "API" if (priced or s.uid in groups) else ("PORTAL" if g.random() < 0.025 else "POS")
            rows.append((s, d, minute, "RUL", price, ch))
            if g.random() < 0.85:
                rows.append((s, d, minute, "PUL", price + s.diff_pul, ch))
        # diesel moves with its own rack, on the same pattern of minutes
        for k in range(lo, hi + 1):
            d = W.DAYS[k]
            if not s.open_on(d):
                continue
            tgt = int(round((M.latest(dsl_rack, d) * 100 + W.LEVY["diesel"][d.year] + 13.5 + s.base * 0.4)
                            * 1.05 * 10)) + int(round(g.normal(0, 1.5)))
            if cur_d is not None and abs(tgt - cur_d) < 3:
                continue
            priced = s.brand_priced_on(d)
            minute = M.BATCH[s.brand_on(d)][0] if priced else int(g.integers(330, 1290))
            ch = "API" if (priced or s.uid in groups) else ("PORTAL" if g.random() < 0.025 else "POS")
            rows.append((s, d, minute, "ULSD", tgt, ch))
            cur_d = tgt
    out = []
    for s, d, minute, grade, price, ch in rows:
        eff = W.to_utc(d, minute)
        rec = eff + dt.timedelta(seconds=int(g.integers(15, 200)) if ch != "PORTAL" else int(g.integers(300, 5400)))
        out.append({"station": M.station_id_on(s, d), "grade": grade, "eff": eff, "price": price, "channel": ch,
                    "received": rec, "uid": s.uid})
    out.sort(key=lambda r: (r["received"], r["station"], r["grade"]))
    g2 = rng(4)
    ids = np.cumsum(g2.integers(1, 4, len(out))) + 7_310_000
    for r, i in zip(out, ids):
        r["id"] = "S%08d" % int(i)
    return out


def priced_itself(sim, subs):
    """the golden for the scope ask: stations a brand prices itself on 1 December 2026, read from the November
    submissions. A brand's pricing desk pushes the prices of the stations it prices through the API at the same
    minutes of the day, so the brand's push times are the minutes of the day at which three or more of its stations
    submitted regular prices through the API, and a station counts when most of its regular-price changes came at its
    brand's push times"""
    from collections import defaultdict
    st = sim["by_uid"]
    pushers = defaultdict(set)
    per = defaultdict(list)
    for r in subs:
        if r["grade"] != "RUL":
            continue
        s = st[r["uid"]]
        key = (s.brand_on(r["eff"].date()), r["eff"].hour * 60 + r["eff"].minute)
        if r["channel"] == "API":
            pushers[key].add(r["uid"])
        per[r["uid"]].append(key)
    push = {k for k, v in pushers.items() if len(v) >= 3}
    out = {b: 0 for b in W.CODES}
    share = {}
    for uid, keys in per.items():
        b = st[uid].brand_on(W.SCOPE_DATE)
        if b not in W.CODES or not st[uid].open_on(W.SCOPE_DATE):
            continue
        sh = sum(1 for k in keys if k in push) / len(keys)
        share[uid] = sh
        if sh >= 0.5:
            out[b] += 1
    return out, share
