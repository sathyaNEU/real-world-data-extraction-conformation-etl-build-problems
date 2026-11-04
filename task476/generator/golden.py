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
BAND_CFS = 2            # a daily mean is graded within this many cfs of the golden's (27 and 28 July on met only)
SHORT_BAND_AF = 100     # the season's shortfall is graded within this many acre-feet


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


def gh_corrections(d):
    """The staff plate read against the logger at each visit, as a gauge-height correction prorated in time between
    visits and held before the first and after the last."""
    marks = sorted((v["arrival"], v["staff"] - v["logger"]) for v in d["visits"])

    def c(t):
        if t <= marks[0][0]:
            return marks[0][1]
        if t >= marks[-1][0]:
            return marks[-1][1]
        for (ta, ca), (tb, cb) in zip(marks, marks[1:]):
            if ta <= t <= tb:
                return ca + (cb - ca) * (t - ta).total_seconds() / (tb - ta).total_seconds()
    return c


def measured(d, qf, ghcorr=False):
    """Each 2026 measurement against Rating 7 at its own gauge height: the stage shift that puts the measured discharge
    on the rating, the measured-to-rated ratio and the percentage difference."""
    corr = gh_corrections(d) if ghcorr else (lambda t: 0.0)
    out = []
    for v in d["visits"]:
        gh = v["gh"] + corr(v["mid"])
        r = qf(gh)
        out.append(dict(v, ghc=gh, shift=stage_for(qf, v["q"]) - gh, rated=r, ratio=v["q"] / r,
                        pct=100 * (v["q"] / r - 1)))
    return sorted(out, key=lambda v: v["mid"])


def split(sh):
    """The measurements on the published rating and those off it: the first measurement more than 5 per cent off Rating
    7 (the memo's 17 measurements all sit within 5) with every later one off too begins the second group."""
    k = next(i for i in range(len(sh)) if all(abs(v["pct"]) >= 5.0 for v in sh[i:]))
    return sh[:k], sh[k:]


def storm_peak(d, on, off):
    """The highest stage between the last measurement on Rating 7 and the first one off it."""
    seg = [(t, h) for t, h in d["stage"] if on[-1]["mid"] <= t <= off[0]["mid"]]
    return max(seg, key=lambda x: x[1])[0]


def _interp(marks, key, t):
    if t <= marks[0]["mid"]:
        return marks[0][key]
    if t >= marks[-1]["mid"]:
        return marks[-1][key]
    for a, b in zip(marks, marks[1:]):
        if a["mid"] <= t <= b["mid"]:
            return a[key] + (b[key] - a[key]) * (t - a["mid"]).total_seconds() / (b["mid"] - a["mid"]).total_seconds()


def _median(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def compute(d, route="golden", hiwater="memo", days="local", form="shift", level="mean", onset="peak", pre="none",
            ghcorr=False, fixed=None):
    """route 'rating' is Rating 7 throughout, the easy route. route 'golden' computes the record on the relation the
    measurements establish; its options are the correction forms checks.py runs against the golden's: form 'shift' (a
    stage correction) or 'ratio' (measured over rated flow); level 'mean', 'median', 'ls' (least squares on the measured
    flows), 'each' (each measurement's own, prorated in time) or 'stage' (a shift linear in gauge height); onset 'peak'
    (from the storm's peak), 'day27', 'day28', 'day29' (from local midnight that day) or 'ramp' (prorated from the last
    measurement on the rating to the first off it); pre 'none' (Rating 7 as published before the storm), 'each' (each
    earlier measurement's own small correction prorated, the first held back to the record's start) or 'each0' (the
    same, none before the first); ghcorr applies the staff readings' differences from the logger, prorated between
    visits, as gauge-height corrections; fixed replaces the post-storm level with a stated value (the solution's own
    rounded shift). hiwater and days as for rating() and Article 403's local days."""
    qf = rating(d, hiwater)
    sh = measured(d, qf, ghcorr)
    on, off = split(sh)
    peak = storm_peak(d, on, off)
    corr = gh_corrections(d) if ghcorr else None
    key, neutral = ("shift", 0.0) if form == "shift" else ("ratio", 1.0)
    vals = [v[key] for v in off]
    a_st = b_st = None
    if level == "median":
        lvl = _median(vals)
    elif level == "ls":
        if form == "ratio":
            lvl = sum(v["q"] * v["rated"] for v in off) / sum(v["rated"] ** 2 for v in off)
        else:
            lo, hi = -0.4, 0.4
            f = lambda s_: sum((v["q"] - qf(v["ghc"] + s_)) ** 2 for v in off)
            for _ in range(90):
                m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
                if f(m1) < f(m2):
                    hi = m2
                else:
                    lo = m1
            lvl = (lo + hi) / 2
    elif level == "stage":
        n = len(off)
        mx = sum(v["ghc"] for v in off) / n
        my = sum(v["shift"] for v in off) / n
        b_st = sum((v["ghc"] - mx) * (v["shift"] - my) for v in off) / sum((v["ghc"] - mx) ** 2 for v in off)
        a_st = my - b_st * mx
        lvl = my
    else:
        lvl = sum(vals) / len(vals)
    if fixed is not None:
        lvl = fixed
    t0 = {"peak": peak, "day27": dt.datetime(2026, 7, 27, tzinfo=B.PDT), "day28": dt.datetime(2026, 7, 28, tzinfo=B.PDT),
          "day29": dt.datetime(2026, 7, 29, tzinfo=B.PDT), "ramp": off[0]["mid"]}[onset]

    def post_val(t, h):
        if level == "each":
            return _interp(off, key, t)
        if level == "stage":
            return a_st + b_st * h
        return lvl

    def pre_val(t):
        if pre == "none":
            return neutral
        if pre == "each0" and t < on[0]["mid"]:
            return neutral
        return _interp(on, key, t)

    def adj(t, h):
        if route == "rating":
            return neutral
        if onset == "ramp" and on[-1]["mid"] < t < off[0]["mid"]:
            w = (t - on[-1]["mid"]).total_seconds() / (off[0]["mid"] - on[-1]["mid"]).total_seconds()
            return pre_val(on[-1]["mid"]) * (1 - w) + post_val(off[0]["mid"], h) * w
        return post_val(t, h) if t >= t0 else pre_val(t)

    sums = {}
    flows = []
    for t, h in d["stage"]:
        hc = h + corr(t) if corr and route != "rating" else h
        q = qf(hc + adj(t, hc)) if form == "shift" else qf(hc) * adj(t, hc)
        lt = t.astimezone(B.PDT) if days == "local" else t
        day = lt.date()
        flows.append((t, lt, q))
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
    spring = [(t, q) for t, lt, q in flows if lt.month in (5, 6)]
    pk_t, pk_q = max(spring, key=lambda x: x[1])
    s_mean = sum(v["shift"] for v in off) / len(off)
    ratio = sum(v["ratio"] for v in off) / len(off)
    return dict(daily=daily, dev=dev, periods=periods, shortfall=shortfall, vol=vol, shifts=sh, on=on, post=off,
                peak=peak, spring_peak=(pk_t, pk_q), s_mean=s_mean, ratio=ratio, level=lvl)


def figures(d):
    g = compute(d)
    easy = compute(d, route="rating")
    pre = g["on"]
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
        "post_storm_shift_fitted_ft": "%.4f" % g["s_mean"],
        "post_storm_shift_fitted_abs_ft": "%.4f" % abs(g["s_mean"]),
        "post_storm_shifts_ft": ["%.4f" % v["shift"] for v in g["post"]],
        "daily_band_cfs": BAND_CFS, "shortfall_band_af": "%d" % SHORT_BAND_AF, "met_only_days": ["27 July", "28 July"],
        "post_storm_pct_range": ["%.1f" % min(v["pct"] for v in g["post"]), "%.1f" % max(v["pct"] for v in g["post"])],
        "post_storm_pct_below_range": ["%.1f" % abs(max(v["pct"] for v in g["post"])),
                                       "%.1f" % abs(min(v["pct"] for v in g["post"]))],
        "pre_storm_pct_max": "%.1f" % max(abs(v["pct"]) for v in pre),
        "storm_peak_pst": g["peak"].strftime("%Y-%m-%d %H:%M"),
        "storm_peak_local": g["peak"].astimezone(B.PDT).strftime("%-d %B %Y %H:%M"),
        "held_aug_cfs": "%.1f" % r1(sum(v for k, v in g["daily"].items() if k.month == 8) / 31.0),
        "held_oct_cfs": "%.1f" % r1(sum(v for k, v in g["daily"].items() if k.month == 10) / 31.0),
        "spring_peak_cfs": "{:,}".format(r0(g["spring_peak"][1])),
        "spring_peak_local": g["spring_peak"][0].astimezone(B.PDT).strftime("%-d %B %Y %H:%M"),
        "minimums_cfs": [50, 30], "articles": [403, 404], "table_range_ft": [d["table"] and min(d["table"]), max(d["table"])],
        "high_segment": [d["hi"]["base"], d["hi"]["k"], d["hi"]["p"]],
        "record_days": sum(1 for k in g["daily"] if k.month >= 7), "setpoints_cfs": [54, 64, 33], "article_404_af": "20,000",
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
