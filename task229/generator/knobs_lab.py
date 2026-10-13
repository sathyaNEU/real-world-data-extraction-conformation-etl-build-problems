"""task229 generator: search the gauging salts so every Ask B figure sits mid-bin, every device path lands outside
the bin, and the gauged ranges keep the extrapolation rule where the design puts it. Writes knobs.py.

    python3 task229/generator/knobs_lab.py"""
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P
import records as R
import truth as T
import world as W

LST = "Etc/GMT+8"


def table(rows):
    df = pd.DataFrame(rows)
    df["q"] = np.where(df.unit == "L/s", df.discharge / 1000.0, df.discharge)
    df["day"] = [pd.Timestamp(u).tz_convert(LST).date() for u in df.measured_utc]
    df["uday"] = [pd.Timestamp(u).date() for u in df.measured_utc]
    agg = df.groupby("key", as_index=False).agg(station=("station", "first"), day=("day", "first"), uday=("uday", "first"),
                                                gh=("gh_m", "first"), q=("q", "sum"), parts=("q", "size"),
                                                q1=("q", "first"))
    return agg


def par_for(st, day):
    if st == "C122":
        return W.RATING["C122"]
    return W.OLD_RATING[st] if day < P.MOVE else W.RATING[st]


def figures(agg):
    a = agg[(agg.day >= P.WY_START) & (agg.day <= P.WY_END)]
    def pct(st, q, h, par):
        qr = float(W.q_of_h(par, h))
        return 100.0 * (q - qr) / qr
    gold = np.mean([pct(s, q, h, par_for(s, d)) for s, q, h, d in zip(a.station, a.q, a.gh, a.day)])
    cur = np.mean([pct(s, q, h, W.RATING[s]) for s, q, h in zip(a.station, a.q, a.gh)])
    post = a[a.day >= P.MOVE]
    drop = np.mean([pct(s, q, h, W.RATING[s]) for s, q, h in zip(post.station, post.q, post.gh)]) if len(post) else np.nan
    utc = np.mean([pct(s, q, h, par_for(s, u)) for s, q, h, u in zip(a.station, a.q, a.gh, a.uday)])
    first = np.mean([pct(s, q1, h, par_for(s, d)) for s, q1, h, d in zip(a.station, a.q1, a.gh, a.day)])
    return {"gold": gold, "cur": cur, "drop": drop, "utc": utc, "first": first, "n": len(a),
            "n_pre": int((a.day < P.MOVE).sum()), "n_post": int((a.day >= P.MOVE).sum()),
            "splits": int((a.parts > 1).sum())}


def top_printed(agg, no):
    lim = date(2026, 6, 30) if no == "C122" else date(2026, 3, 31)
    sel = agg[agg.day <= lim]
    v = float(sel.q.max())
    return float(("%#.3g" % v) if v < 10 else ("%.1f" % v))


def ok_top(no, top):
    q = [W.outlook_2027(no, m) for m in range(1, 13)]
    if no == "C107":
        return q[4] >= 1.6 * top and q[5] >= 1.6 * top and all(q[m] <= 1.35 * top for m in range(12) if m not in (4, 5))
    return max(q) <= 1.35 * top


def mid(x, margin=0.025):
    return abs(x - round(x, 1)) <= 0.05 - margin and abs(round(x, 1)) >= 0.1


def apart(a, b):
    return round(a, 1) != round(b, 1) and abs(a - b) >= 0.15


def search(TR):
    out = {}
    fixed_c110 = None
    for no in W.CURRENT:
        for salt in range(0, 400):
            rows = R.station_gaugings(TR, no, salt)
            if no == "C122":
                base = fixed_c110 if fixed_c110 is not None else R.station_gaugings(TR, "C110", 0)
                agg = table(base + rows)
                top = top_printed(table(rows), "C122")
            else:
                agg = table(rows)
                top = top_printed(agg, no)
            f = figures(agg)
            if f["n_pre"] < 2 or f["n_post"] < 2:
                continue
            if not ok_top(no, top):
                continue
            if no in R.SPLIT_Q and f["splits"] < 1:
                continue
            g = f["gold"]
            if not (mid(g) and apart(g, f["cur"]) and apart(g, f["drop"])):
                continue
            if no == "C116" and not apart(g, f["utc"]):
                continue
            if no in R.SPLIT_Q and not apart(g, f["first"]):
                continue
            out[no] = salt
            print(no, salt, "gold %.3f cur %.3f drop %.3f utc %.3f top %.3g n %d/%d" % (g, f["cur"], f["drop"], f["utc"], top, f["n_pre"], f["n"]))
            break
        else:
            print(no, "NO SALT FOUND")
    return out


def daily_salt(TR):
    import knobs as KN
    import golden as GD
    import pandas as pd
    reg = pd.DataFrame({"station": ["C110"], "replaced_by": ["C122"]})
    for salt in range(0, 300):
        KN.DAILY_SALT = salt
        DR = R.daily_record(TR)
        d = DR.copy()
        d["date"] = [x.isoformat() for x in d.date]
        A = GD.ask_a(d, reg)
        x = d[(d.date >= "2025-10-01") & (d.date <= "2026-09-30")].copy()
        x["held"] = GD.held_mask(x)
        x["st"] = x.station.replace({"C110": "C122"})
        held = x[x.held].drop_duplicates(["st", "date"]).assign(ym=lambda y: y.date.str[:7]).groupby("ym").size()
        mm_ok = True
        if len(set(A.values())) == 12 and len(held) == 12 and held.min() >= 3:
            y = x.drop_duplicates(["st", "date"]).sort_values(["st", "date"])
            for n in (2, 3, 4):
                for kf in (True, False):
                    drop = []
                    for st_, gy in y.groupby("st", sort=False):
                        v = gy.water_level_m.values
                        ix = gy.index.values
                        if W.ST[st_]["res"] == 0.01:
                            continue
                        i = 0
                        while i < len(v):
                            j = i
                            while j + 1 < len(v) and v[j + 1] == v[i]:
                                j += 1
                            if j - i + 1 >= n:
                                drop.extend(ix[(i + 1 if kf else i):j + 1])
                            i = j + 1
                    cnt = y.drop(index=drop).assign(ym=lambda z: z.date.str[:7]).groupby("ym").size()
                    for ym, lab in zip(["%04d-%02d" % ym for ym in GD.MONTHS_WY], GD.MLAB):
                        if cnt.get(ym, 0) == A[lab]:
                            mm_ok = False
        if len(set(A.values())) == 12 and len(held) == 12 and held.min() >= 3 and mm_ok:
            print("daily salt", salt, A, held.to_dict())
            return salt
    raise SystemExit("no daily salt")


if __name__ == "__main__":
    TR = T.build_truth()
    dsalt = daily_salt(TR)
    salts = search(TR)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "knobs.py"), "w") as fh:
        fh.write('"""task229 generator: tuning knobs, set by knobs_lab.py so every graded figure sits inside its rounding bin.\n\n'
                 'GAUGE_SALT selects each station\'s gauging stream (dates, times and measurement errors)."""\n')
        fh.write("GAUGE_SALT = %r\n" % dict(sorted(salts.items())))
        fh.write("DAILY_SALT = %d\n" % dsalt)
    print("wrote knobs.py")
