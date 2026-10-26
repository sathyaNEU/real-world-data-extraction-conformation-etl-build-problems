"""The independent verifier for task270: every figure in generator/figures.json recomputed from the shipped pack with
the standard library's csv reader and plain arithmetic, none of the generator's analysis code, and compared at the
figure's own rounding."""
import csv
import datetime as dt
import json
import math
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = ["active_days_d1_14", "sessions_d1_14", "first_purchase_d14", "items_saved_d1_14", "push_opens_d1_14"]
RET = "retained_m6"
PP = {"first_purchase_d14", RET}
EXPORT = "2026-10-23"


def rd(x, n):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cov(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (len(a) - 1)


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    # former keys from the catalogue
    former, key = {}, None
    for line in open(os.path.join(t, "metric_catalogue.yaml"), encoding="utf-8"):
        s = line.strip()
        if s.startswith("- key:"):
            key = s.split(":", 1)[1].strip()
        if s.startswith("former_key:"):
            former[s.split(":", 1)[1].split("#")[0].strip()] = key
    # latest computation of each arm and metric
    sc = {}
    for r in rows(os.path.join(t, "experiment_scorecards_2024_2026.csv")):
        m = former.get(r["metric"], r["metric"])
        k = (r["experiment_id"], r["arm"], m)
        if k not in sc or r["computed_at"] >= sc[k]["computed_at"]:
            sc[k] = dict(r, metric=m)
    ch = []
    exps = set()
    for r in rows(os.path.join(t, "onboarding_experiments_2024_2026.csv")):
        if not r["six_month_read_closes"] or r["six_month_read_closes"] > EXPORT:
            continue
        if r["srm_check"] != "pass" or r["status"] not in ("completed", "stopped_early"):
            continue
        ctrl = r["control_arm"]
        for arm in r["arms"].split(";"):
            if arm == ctrl:
                continue
            need = [(r["experiment_id"], a, m) for a in (arm, ctrl) for m in CAND + [RET]]
            if not all(x in sc for x in need):
                continue
            g = lambda a, m, f: float(sc[(r["experiment_id"], a, m)][f])
            ch.append({m: (g(arm, m, "mean"), g(arm, m, "std_dev"), g(arm, m, "users"),
                           g(ctrl, m, "mean"), g(ctrl, m, "std_dev"), g(ctrl, m, "users")) for m in CAND + [RET]})
            exps.add(r["experiment_id"])
    if len(ch) != fig["call"]["changes"] or len(exps) != fig["call"]["experiments"]:
        bad.append(("changes", len(ch), len(exps)))
    hold = rows(os.path.join(t, "global_holdout_users_2025.csv"))
    hv = {m: [float(x[m]) for x in hold] for m in CAND + [RET]}

    def corr(a, b):
        return cov(a, b) / math.sqrt(cov(a, a) * cov(b, b))
    rho = {m: corr(hv[m], hv[RET]) for m in CAND}
    y = [c[RET][0] - c[RET][3] for c in ch]
    vy = [c[RET][1] ** 2 / c[RET][2] + c[RET][4] ** 2 / c[RET][5] for c in ch]
    got = {}
    for m in CAND:
        x = [c[m][0] - c[m][3] for c in ch]
        vx = [c[m][1] ** 2 / c[m][2] + c[m][4] ** 2 / c[m][5] for c in ch]
        s12 = [rho[m] * (c[m][1] * c[RET][1] / c[RET][2] + c[m][4] * c[RET][4] / c[RET][5]) for c in ch]
        got[m] = (cov(x, y) - statistics.fmean(s12)) / math.sqrt((cov(x, x) - statistics.fmean(vx)) *
                                                                  (cov(y, y) - statistics.fmean(vy)))
        if rd(got[m], 2) != fig["correlations"][m]:
            bad.append(("correlation", m, got[m], fig["correlations"][m]))
        if rd(rho[m], 2) != fig["components"]["user_level_correlation"][m]:
            bad.append(("rho", m, rho[m]))
    if max(got, key=got.get) != fig["call"]["proxy"]:
        bad.append(("proxy", max(got, key=got.get)))

    # Ask B
    sd = {m: statistics.stdev(hv[m]) for m in CAND}
    weekly = {}
    for r in rows(os.path.join(t, "new_user_forecast_2027.csv")):
        d = dt.date.fromisoformat(r["date"])
        weekly[(d - dt.timedelta(days=d.weekday()), r["platform"])] = float(r["new_consumer_users_forecast"])
    cal = rows(os.path.join(t, "onboarding_calendar_2027q1.csv"))
    users = {c["experiment_id"]: 0.0 for c in cal}
    d0 = min(dt.date.fromisoformat(c["start_date"]) for c in cal)
    d1 = max(dt.date.fromisoformat(c["end_date"]) for c in cal)
    d = d0
    while d <= d1:
        for p in ("ios", "android"):
            n = weekly[(d - dt.timedelta(days=d.weekday()), p)] / 7 * 0.97
            for layer in {c["layer"] for c in cal}:
                live = [c for c in cal if c["layer"] == layer and c["platforms"] in ("all", p) and
                        c["start_date"] <= d.isoformat() <= c["end_date"]]
                for c in live:
                    users[c["experiment_id"]] += n / len(live)
        d += dt.timedelta(days=1)
    z = statistics.NormalDist().inv_cdf(0.975) + statistics.NormalDist().inv_cdf(0.80)
    for c in cal:
        e = c["experiment_id"]
        na = users[e] / int(c["arms"])
        if round(na) != fig["asks"]["B"]["users_per_arm"][e]:
            bad.append(("users", e, na))
        for m in CAND:
            v = z * sd[m] * math.sqrt(2 / na)
            v = rd(100 * v, 2) if m in PP else rd(v, 3)
            if v != fig["asks"]["B"]["detectable"][e][m]:
                bad.append(("mde", e, m, v))

    # Ask C
    latest = {}
    for r in rows(os.path.join(t, "signup_cohorts_2025.csv")):
        if r["signup_account_type"] != "consumer":
            continue
        k = (r["signup_date"], r["platform"], r["country"], r["account_type"])
        if k not in latest or r["refreshed_at"] > latest[k]["refreshed_at"]:
            latest[k] = r
    col = {"active_days_d1_14": "active_days_total", "sessions_d1_14": "sessions_total",
           "first_purchase_d14": "first_purchases", "items_saved_d1_14": "items_saved_total",
           "push_opens_d1_14": "push_opens_total", RET: "retained_m6_users"}
    for half, (a, b) in (("H1", ("2025-01-01", "2025-06-30")), ("H2", ("2025-07-01", "2025-12-31"))):
        cs = [r for k, r in latest.items() if a <= k[0] <= b]
        hs = [x for x in hold if a <= x["signed_up_on"] <= b]
        n_all, n_h = sum(int(r["new_users"]) for r in cs), len(hs)
        for m in CAND + [RET]:
            s_all, s_h = sum(int(r[col[m]]) for r in cs), sum(float(x[m]) for x in hs)
            v = (s_all - s_h) / (n_all - n_h) - s_h / n_h
            v = rd(100 * v, 2) if m in PP else rd(v, 3)
            if v != fig["asks"]["C"][half][m]:
                bad.append(("gap", half, m, v))
    for x in bad:
        print("VERIFY MISMATCH", x)
    print("verify: %d changes, %d calendar experiments, %d mismatches" % (len(ch), len(cal), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(run(os.path.dirname(HERE)))
