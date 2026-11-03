"""task402 ask ceiling on the cut pack. Shares no code with the generator: it reads target/ and the golden figures in
figures.json, runs two responses through every ask and scores them at each asking sentence's stated rounding.

The cracker lands the call, runs the hygiene battery (UTC to local, exact duplicates, closed referrals off a list,
booking lines joined as of the day) and executes every filed WHAT (the waiting list initiative's therapists only,
whole patients, the national measure). The mirror is off the call and takes each ask's most attractive wrong
reading. Pair arithmetic: landed call 38 + 7 + 55 x kept, missed call 5 + 7 + 55 x kept.

    python3 task402/generator/ceiling.py [target_dir]
"""
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def london(ts):
    """UTC stamp to UK local time (the battery's own conversion: BST from the last Sunday of March to the last of
    October, changing at 01:00 UTC)."""
    t = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")

    def last_sunday(y, m):
        d = date(y, m, 31)
        return d - timedelta(days=(d.weekday() + 1) % 7)
    a = datetime.combine(last_sunday(t.year, 3), datetime.min.time()) + timedelta(hours=1)
    b = datetime.combine(last_sunday(t.year, 10), datetime.min.time()) + timedelta(hours=1)
    return t + timedelta(hours=1) if a <= t < b else t


def waiting(t, battery):
    refs = pd.read_csv(os.path.join(t, "referrals_received_2023-10_to_2026-03.csv"), dtype=str).set_index("referral_id")
    dis = pd.to_datetime(refs.discharge_date).dt.date
    out = {}
    for fn, ct, cr, fmt in (("step3_waiting_list_month_end_2025-04_to_2025-09.csv", "SnapshotTaken", "ReferralID", "%d/%m/%Y %H:%M"),
                            ("step3_waiting_list_month_end_2025-10_to_2026-03.csv", "snapshot_at", "referral_id", "%Y-%m-%d %H:%M")):
        s = pd.read_csv(os.path.join(t, fn), dtype=str).drop_duplicates()
        s["k"] = pd.to_datetime(s[ct], format=fmt)
        for tk, g in s.groupby("k"):
            mend = (tk.to_period("M") - 1).end_time.date()
            if battery:
                closed = g[cr].map(dis)
                g = g[~(closed.notna() & (closed <= mend))]
            out[str(pd.Period(mend, "M"))] = len(g)
    return out


def digital(t, mode):
    d = json.load(open(os.path.join(t, "steadyway_activity_export_2025-07_to_2026-05.json")))
    ev = pd.DataFrame(d["events"]).drop_duplicates()
    ev["loc"] = ev.at_utc.map(london)
    b = ev[ev.event == "section_started"].groupby("user_id")["loc"].min()
    secs = ev.groupby("module").content_id.nunique()
    out = {}
    for uid, g in ev[ev.event == "section_completed"].groupby("user_id"):
        g = g[g["loc"] <= b[uid] + timedelta(days=56)]
        per = g.groupby("module").content_id.nunique()
        if mode == "cracker":
            fin = sum(1 for mod, k in per.items() if k >= secs[mod])
        elif mode == "includer":
            started = ev[(ev.user_id == uid) & (ev.event == "section_started")].groupby("module").content_id.nunique()
            fin = sum(1 for mod, k in per.items() if k >= started.get(mod, 0))
        else:
            fin = len(per)
        key = str(pd.Period(b[uid].date(), "M"))
        out[key] = out.get(key, 0) + int(fin >= 4)
    return {k: out.get(k, 0) for k in ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"]}


def agency(t, mode):
    ts = pd.read_csv(os.path.join(t, "agency_timesheets_2025-04_to_2026-03.csv"), dtype=str).drop_duplicates()
    ts["wk"] = pd.to_datetime(ts["Week commencing"], format="%d/%m/%Y").dt.date
    ts["h"] = ts["Hours claimed"].astype(float)
    bk = pd.read_excel(os.path.join(t, "agency_bookings_psychological_therapies_2025-26.xlsx"), header=4, dtype=str)
    bk["s"] = bk["Line start (UTC)"].map(lambda x: london(x).date())
    bk["e"] = bk["Line end (UTC)"].map(lambda x: london(x).date())
    bk["rate"] = bk["Charge rate (GBP per hour)"].astype(float)
    first = bk.groupby("Booking ref").s.min()
    if mode == "cracker":
        keep = set(first[first >= date(2025, 5, 1)].index)
        ts = ts[ts["Booking ref"].isin(keep)]
        # the battery's latest-version rule: one timesheet per booking and week, the last submitted
        ts["sub"] = pd.to_datetime(ts["Submitted"], format="%d/%m/%Y %H:%M")
        ts = ts.sort_values("sub").groupby(["Booking ref", "wk"]).tail(1)
    rows = []
    for r in ts.itertuples():
        lines = bk[bk["Booking ref"] == r._2]
        if mode in ("cracker", "includer"):
            days = [r.wk + timedelta(days=i) for i in range(5)]
            for d in days:
                ln = lines[(lines.s <= d) & (lines.e >= d)]
                rate = float(ln.rate.iloc[0]) if len(ln) else float(lines.rate.iloc[-1])
                rows.append((d, r.h / 5, rate))
        else:
            ln = lines[(lines.s <= r.wk) & (lines.e >= r.wk)]
            rate = float(ln.rate.iloc[0]) if len(ln) else float(lines.rate.iloc[0])
            rows.append((r.wk, r.h, rate))
    df = pd.DataFrame(rows, columns=["d", "h", "rate"])
    df["m"] = pd.to_datetime(df.d).dt.to_period("M").astype(str)
    df["c"] = df.h * df.rate
    g = df.groupby("m")[["h", "c"]].sum()
    keep = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"]
    return ({k: int(round(g.at[k, "h"])) if k in g.index else 0 for k in keep},
            {k: int(round(g.at[k, "c"] / 100.0) * 100) if k in g.index else 0 for k in keep})


def score(resp, gold):
    return sum(1 for k, v in gold.items() if resp.get(k) == v), len(gold)


def main(argv):
    t = argv[0] if argv else os.path.join(TASK, "target")
    f = json.load(open(os.path.join(HERE, "figures.json")))
    gold = {"waiting": f["ask_waiting"], "digital": f["ask_digital"], "hours": f["ask_hours"], "cost": f["ask_cost"]}
    cr = {"waiting": waiting(t, True), "digital": digital(t, "cracker")}
    cr["hours"], cr["cost"] = agency(t, "cracker")
    mi = {"waiting": waiting(t, False), "digital": digital(t, "mirror")}
    mi["hours"], mi["cost"] = agency(t, "mirror")
    fi = {"waiting": waiting(t, False), "digital": digital(t, "includer")}
    fi["hours"], fi["cost"] = agency(t, "includer")
    labels = {"waiting": "Ask 1, step 3 patients waiting at each month end (12)",
              "digital": "Ask 2, digital completers by month began, September to February (6)",
              "hours": "Ask 3, agency hours, May to October (6)", "cost": "Ask 3, agency cost, May to October (6)"}
    tot_c = tot_m = n_all = 0
    print("| Block | Cracker keeps | Mirror keeps | Cracker |")
    print("|---|---|---|---|")
    for k in ("waiting", "digital", "hours", "cost"):
        kc, n = score(cr[k], gold[k])
        km, _ = score(mi[k], gold[k])
        tot_c += kc
        tot_m += km
        n_all += n
        print("| %s | %d of %d | %d of %d | %s |" % (labels[k], kc, n, km, n, "miss" if kc == 0 else "keeps"))
    lc, lm = tot_c / n_all, tot_m / n_all
    c_score = 38 + 7 + 55 * lc
    s_score = 5 + 7 + 55 * lm
    tot_f = sum(score(fi[k], gold[k])[0] for k in ("waiting", "digital", "hours", "cost"))
    lf = tot_f / n_all
    f_score = 5 + 7 + 55 * lf
    print("full includer (every row as it stands, no exclusion, no dedupe) keeps %d of %d: %s" % (
        tot_f, n_all, {k: score(fi[k], gold[k])[0] for k in ("waiting", "digital", "hours", "cost")}))
    print("cracker keeps %.1f per cent of ask weight; mirror keeps %.1f per cent; full includer %.1f per cent" % (
        100 * lc, 100 * lm, 100 * lf))
    print("pair ceiling %.1f (landed call %.1f, missed call %.1f); with the full includer as the miss %.1f" % (
        (c_score + s_score) / 2, c_score, s_score, (c_score + f_score) / 2))
    for k in ("waiting", "digital", "hours", "cost"):
        print(k, "gold", gold[k])
        print(k, "cracker", cr[k])
        print(k, "mirror", mi[k])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
