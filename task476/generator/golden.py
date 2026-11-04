"""The golden, computed from the pack alone (bundle.py): BP-1's 2026 record on the stage-discharge relation the season's
discharge measurements establish (Rating 7 as published until the 27 July storm's peak, Rating 7 on the post-storm
measurements' mean stage shift after it, the high-water segment from the 2023 rating memo above the table), daily means
on local days, Article 403's deviations, the shortfall and Article 404's monthly volumes; then the two deliverables and
generator/figures.json. Route arguments let checks.py and ceiling.py run the easy paths through the same code."""
import datetime as dt
import json
import math
import os

import bundle as B

AF_PER_CFS_DAY = 1.98347


def r1(v):
    return math.floor(v * 10 + 0.5) / 10


def r0(v):
    return int(math.floor(v + 0.5))


def r100(v):
    return int(math.floor(v / 100 + 0.5) * 100)


def rating(d, hiwater="memo"):
    """Rating 7: the register's expanded table, interpolated at 0.01 ft, and above it the memo's high-water segment
    (hiwater='memo'), or the table extended: 'power' (the low-water law the table follows), 'linear' (the last step's
    slope) or 'cap' (the table's top value)."""
    tab = d["table"]
    keys = sorted(tab)
    lo_h, hi_h = keys[0], keys[-1]
    hs = d["hi"]

    def q(h):
        if h <= lo_h:
            return tab[lo_h] * max(0.0, (h - 0.80) / (lo_h - 0.80)) ** 2.3 if h > 0.80 else 0.0
        if h <= hi_h:
            i = int(math.floor((h - lo_h) * 100 + 1e-9))
            a = round(lo_h + i / 100.0, 2)
            b = round(a + 0.01, 2)
            if b not in tab:
                return tab[a]
            return tab[a] + (tab[b] - tab[a]) * (h - a) / 0.01
        if hiwater == "memo":
            return hs["base"] + hs["k"] * (h - hs["top"]) ** hs["p"]
        if hiwater == "power":
            return tab[hi_h] * ((h - 0.80) / (hi_h - 0.80)) ** 2.3
        if hiwater == "linear":
            return tab[hi_h] + (tab[hi_h] - tab[round(hi_h - 0.01, 2)]) / 0.01 * (h - hi_h)
        return tab[hi_h]
    return q


def stage_for(qf, target):
    lo, hi = 0.81, 9.0
    for _ in range(70):
        m = (lo + hi) / 2
        if qf(m) < target:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def shifts(d, qf):
    """Each 2026 measurement's stage shift on Rating 7: the correction to the gauge height that puts the measured
    discharge on the rating."""
    out = []
    for v in d["visits"]:
        s = stage_for(qf, v["q"]) - v["gh"]
        out.append(dict(v, shift=s, rated=qf(v["gh"]), pct=100 * (v["q"] / qf(v["gh"]) - 1)))
    return out


def storm_peak(d):
    """The highest stage between the last measurement on Rating 7 and the first one off it."""
    sh = d["_shifts"]
    pre = max(v["mid"] for v in sh if abs(v["shift"]) < 0.03)
    post = min(v["mid"] for v in sh if v["mid"] > pre)
    seg = [(t, h) for t, h in d["stage"] if pre <= t <= post]
    return max(seg, key=lambda x: x[1])[0]


def compute(d, route="golden", hiwater="memo", days="local", shift_form="stage"):
    """route: golden (Rating 7 to the storm's peak, the post-storm measurements' mean shift after it), rating (Rating 7
    throughout: the easy route), prorate (each measurement's shift prorated in time from the one before), ratio (the
    post-storm measured-to-rated ratio applied to the rated flow)."""
    qf = rating(d, hiwater)
    d["_shifts"] = sh = shifts(d, qf)
    peak = storm_peak(d)
    post = [v for v in sh if v["mid"] > peak]
    s_mean = sum(v["shift"] for v in post) / len(post)
    ratio = sum(v["q"] / v["rated"] for v in post) / len(post)
    marks = sorted(sh, key=lambda v: v["mid"])

    def shift_at(t):
        if route == "rating":
            return 0.0
        if route in ("golden", "ratio"):
            return s_mean if t >= peak else 0.0
        before = [v for v in marks if v["mid"] <= t]
        after = [v for v in marks if v["mid"] > t]
        if not before:
            return 0.0
        if not after:
            return before[-1]["shift"]
        a, b = before[-1], after[0]
        if a["mid"] < peak <= b["mid"] and t >= peak:
            return b["shift"]
        if a["mid"] < peak <= b["mid"]:
            return a["shift"]
        w = (t - a["mid"]).total_seconds() / (b["mid"] - a["mid"]).total_seconds()
        return a["shift"] + w * (b["shift"] - a["shift"])

    sums = {}
    for t, h in d["stage"]:
        if route == "ratio":
            q = qf(h) * (ratio if t >= peak else 1.0)
        else:
            q = qf(h + shift_at(t))
        day = (t.astimezone(B.PDT) if days == "local" else t).date()
        if not (dt.date(2026, 5, 1) <= day <= dt.date(2026, 10, 31)):
            continue
        a = sums.setdefault(day, [0.0, 0])
        a[0] += q
        a[1] += 1
    daily = {k: v[0] / v[1] for k, v in sorted(sums.items())}
    dev = [k for k, v in daily.items() if v < d["minimum"](k)]
    periods = []
    for k in dev:
        if periods and (k - periods[-1][1]).days == 1:
            periods[-1][1] = k
        else:
            periods.append([k, k])
    shortfall = sum((d["minimum"](k) - daily[k]) * AF_PER_CFS_DAY for k in dev)
    vol = {m: sum(v for k, v in daily.items() if k.month == m) * AF_PER_CFS_DAY for m in (5, 6)}
    spring = [(t, (qf(h * 0 + h) if route == "ratio" else qf(h + shift_at(t)))) for t, h in d["stage"]
              if (t.astimezone(B.PDT) if days == "local" else t).month in (5, 6)]
    pk_t, pk_q = max(spring, key=lambda x: x[1])
    return dict(daily=daily, dev=dev, periods=periods, shortfall=shortfall, vol=vol, shifts=sh, peak=peak,
                spring_peak=(pk_t, pk_q),
                s_mean=s_mean, ratio=ratio, post=post)


def figures(d):
    g = compute(d)
    easy = compute(d, route="rating")
    pre = [v for v in g["shifts"] if v["mid"] < g["peak"]]
    fig = {
        "deviation_periods": [[a.isoformat(), b.isoformat()] for a, b in g["periods"]],
        "deviation_periods_text": ["%s to %s" % (a.strftime("%-d %B"), b.strftime("%-d %B")) for a, b in g["periods"]],
        "deviation_days": len(g["dev"]),
        "deviation_days_by_month": {m: sum(1 for k in g["dev"] if k.month == m) for m in (7, 8, 9, 10)},
        "shortfall_af": "{:,}".format(r100(g["shortfall"])),
        "may_af": "{:,}".format(r100(g["vol"][5])), "june_af": "{:,}".format(r100(g["vol"][6])),
        "may_june_af": "{:,}".format(r100(g["vol"][5]) + r100(g["vol"][6])),
        "daily_cfs": {k.isoformat(): r0(v) for k, v in g["daily"].items() if k.month >= 7},
        "easy_route_deviation_days": len(easy["dev"]),
        "easy_route_min_jul_sep_cfs": "%.1f" % r1(min(v for k, v in easy["daily"].items() if 7 <= k.month <= 9)),
        "post_storm_shift_ft": "%.2f" % abs(g["s_mean"]),
        "post_storm_pct_range": ["%.1f" % min(v["pct"] for v in g["post"]), "%.1f" % max(v["pct"] for v in g["post"])],
        "post_storm_pct_below_range": ["%.1f" % abs(max(v["pct"] for v in g["post"])),
                                       "%.1f" % abs(min(v["pct"] for v in g["post"]))],
        "pre_storm_pct_max": "%.1f" % max(abs(v["pct"]) for v in pre),
        "storm_peak_pst": g["peak"].strftime("%Y-%m-%d %H:%M"),
        "held_aug_cfs": "%.1f" % r1(sum(v for k, v in g["daily"].items() if k.month == 8) / 31.0),
        "held_oct_cfs": "%.1f" % r1(sum(v for k, v in g["daily"].items() if k.month == 10) / 31.0),
        "spring_peak_cfs": "{:,}".format(r0(g["spring_peak"][1])),
        "spring_peak_local": g["spring_peak"][0].astimezone(B.PDT).strftime("%-d %B %Y %H:%M"),
        "minimums_cfs": [50, 30], "articles": [403, 404], "table_range_ft": [d["table"] and min(d["table"]), max(d["table"])],
        "high_segment": [d["hi"]["base"], d["hi"]["k"], d["hi"]["p"]],
        "record_days": sum(1 for k in g["daily"] if k.month >= 7), "setpoints_cfs": [54, 70, 33], "article_404_af": "20,000",
        "visits": len(g["shifts"]), "post_storm_visits": len(g["post"]),
        "af_per_cfs_day": AF_PER_CFS_DAY,
    }
    return g, fig


def build(target, gdir, figures_path=None):
    import deliver as DL
    os.makedirs(gdir, exist_ok=True)
    for f in os.listdir(gdir):
        os.remove(os.path.join(gdir, f))
    d = B.load(target)
    g, fig = figures(d)
    DL.write_record(os.path.join(gdir, "bypass_flow_record_2026.xlsx"), d, g, fig)
    DL.write_report(os.path.join(gdir, "minimum_flow_deviation_report_2026.docx"), d, g, fig)
    if figures_path:
        with open(figures_path, "w", encoding="utf-8") as fh:
            json.dump(fig, fh, indent=1, sort_keys=True)
            fh.write("\n")
    return g, fig
