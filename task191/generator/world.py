"""The world: Kestrel Pay's nightly monitoring runs, the alerts they raise, triage, the investigations in the case
manager, and the SAR filings, from July 2025 to the extract on 2 November 2026. Every alert carries its true eventual
outcome, so the truth of each scenario's productivity is known even where the extract shows an alert undecided."""
import datetime as dt

import numpy as np

import common as C


def _office_time(r, day, lo=8.5, hi=17.5):
    """A time on an Eastern business day, moved off weekends."""
    while day.weekday() >= 5:
        day = day + dt.timedelta(days=1)
    h = float(r.uniform(lo, hi))
    return dt.datetime.combine(day, dt.time(0)) + dt.timedelta(hours=h)


def build():
    W = {}
    r = C.rng("customers")
    n_cust = 160_000
    # a heavy-tailed propensity to alert: most customers never alert, a few alert again and again
    prop = r.gamma(0.35, 1.0, size=n_cust)
    prop = prop / prop.sum()
    cdf = np.cumsum(prop)
    cust_ids = r.choice(np.arange(10_000_000, 99_999_999), size=n_cust, replace=False)
    acct_of = {}
    W["customers"] = cust_ids
    W["prop"] = prop

    runs, alerts, cases = [], [], []
    rr = C.rng("runs")
    rs_run = C.rng("run-seconds")
    ra = C.rng("alerts")
    RT = {code: C.rng("triage-" + code) for code in C.CODES}
    RC = {code: C.rng("case-" + code) for code in C.CODES}
    alert_no = 4_100_000
    case_no = 270_000
    open_cases = []          # cases open for joining: (opened_at, case)
    d = C.WARM0
    while d <= C.DATA1:
        start = dt.datetime.combine(d, dt.time(22, 5)) + dt.timedelta(minutes=int(rr.integers(0, 26)))
        run_id = "TMR-%s-01" % d.strftime("%Y%m%d")
        n_run = 0
        day_alerts = []
        wk = 0.85 if d.weekday() >= 5 else 1.05
        for code, name, rate, esc, q, sar_med, sar_sd, nosar_med in C.SCEN:
            shown = code
            if code in C.REPLACEMENT and d >= C.REPLACED_ON:
                shown = C.REPLACEMENT[code]
            n = int(ra.poisson(rate * wk))
            for _ in range(n):
                step = int(ra.integers(1, 4))
                ci = min(int(np.searchsorted(cdf, ra.random())), n_cust - 1)
                cust = int(cust_ids[ci])
                if cust not in acct_of:
                    acct_of[cust] = "W%09d" % int(ra.integers(100_000_000, 999_999_999))
                gen = start + dt.timedelta(seconds=int(ra.integers(60, 3600 * 1.4)))
                a = dict(alert_id=None, scenario=code, shown=shown, run_id=run_id, bdate=d,
                         gen=C.to_utc(gen), customer=cust, account=acct_of[cust],
                         score=int(np.clip(ra.normal(70, 12), 31, 99)), dup=False, step=step)
                day_alerts.append(a)
                n_run += 1
        # the monitoring system numbers alerts as it raises them, so numbers run in the order of the run's clock
        day_alerts.sort(key=lambda a: (a["gen"], a["scenario"]))
        for a in day_alerts:
            alert_no += a.pop("step")
            a["alert_id"] = "A%08d" % alert_no
        alerts.extend(day_alerts)
        lag = int(rs_run.integers(0, 50))
        rr.integers(48, 84)
        last = max(a["gen"] for a in day_alerts)
        runs.append(dict(run_id=run_id, bdate=d, type="SCHEDULED", start=C.to_utc(start + dt.timedelta(seconds=lag)),
                         end=last + dt.timedelta(seconds=int(rs_run.integers(40, 420))), n=n_run, note=""))
        if d == C.RERUN_DATE:
            rstart = dt.datetime.combine(d + dt.timedelta(days=1), dt.time(9, 40))
            rid = "TMR-%s-02" % d.strftime("%Y%m%d")
            for a in list(day_alerts):
                alert_no += int(ra.integers(1, 4))
                b = dict(a)
                b.update(alert_id="A%08d" % alert_no, run_id=rid, dup=True,
                         gen=C.to_utc(rstart + (C.to_eastern(a["gen"]) - start)))
                alerts.append(b)
            runs.append(dict(run_id=rid, bdate=d, type="RERUN", start=C.to_utc(rstart + dt.timedelta(seconds=14)),
                             end=max(b["gen"] for b in alerts if b["run_id"] == rid) + dt.timedelta(seconds=97),
                             n=len(day_alerts),
                             note="re-run after the ledger feed for 10 March was reloaded; run TMR-20260310-01 stands"))
        d += dt.timedelta(days=1)

    # ---- triage, escalation and the investigations
    spec = {s[0]: s for s in C.SCEN}
    by_time = sorted(alerts, key=lambda a: (a["gen"], a["alert_id"]))
    # triage, in the order the alerts were raised
    for a in by_time:
        code, name, rate, esc, q, sar_med, sar_sd, nosar_med = spec[a["scenario"]]
        rt = RT[code]
        gen_e = C.to_eastern(a["gen"])
        if a["dup"]:
            a["triage_end"] = C.to_utc(_office_time(rt, gen_e.date() + dt.timedelta(days=int(rt.integers(1, 3)))))
            a["outcome"], a["triage"], a["case"] = "DUP", "DUP", None
            continue
        tdays = float(rt.lognormal(np.log(4.0), 0.6))
        a["triage_end"] = C.to_utc(_office_time(rt, (gen_e + dt.timedelta(days=tdays)).date()))
        if rt.random() >= esc:
            a["triage"], a["case"], a["outcome"] = "NSA", None, "NO_SAR"
            continue
        a["triage"] = "ESC"
    # the escalations, in the order the analysts escalated them: one in eight is on a customer whose activity has
    # already raised an alert of another night's run that opened an investigation while this one waited in triage
    escs = sorted((a for a in alerts if a["triage"] == "ESC"), key=lambda a: (a["triage_end"], a["alert_id"]))
    recent, by_cust = [], {}
    for a in escs:
        code, name, rate, esc, q, sar_med, sar_sd, nosar_med = spec[a["scenario"]]
        rc = RC[code]
        esc_t = a["triage_end"]
        recent[:] = [c for c in recent if c["opened"] >= esc_t - dt.timedelta(days=30)]
        own = [c for c in by_cust.get(a["customer"], []) if c["opened"] <= esc_t < c["decided"]]
        if own:
            # the customer already has an open investigation: the alert is added to it (procedure section 3)
            c = max(own, key=lambda c: c["opened"])
            c["alerts"].append(a["alert_id"])
            a["case"] = c
            a["outcome"] = c["outcome"]
            continue
        live = [c for c in recent if c["opened"] <= esc_t < c["decided"]
                and abs((c["lead_gen"] - a["gen"]).total_seconds()) <= 2 * 86400]
        if live and rc.random() < 0.125:
            c = live[int(rc.integers(0, len(live)))]
            a["customer"], a["account"] = c["customer"], c["account"]
            c["alerts"].append(a["alert_id"])
            a["case"] = c
            a["outcome"] = c["outcome"]
            continue
        sar = bool(rc.random() < q)
        if sar:
            days = float(rc.lognormal(np.log(sar_med - 5.0), sar_sd))
        else:
            days = float(rc.lognormal(np.log(max(nosar_med - 5.0, 8.0)), 0.40))
        decided = C.to_utc(_office_time(rc, (C.to_eastern(esc_t) + dt.timedelta(days=days)).date()))
        c = dict(case_id=None, customer=a["customer"], account=a["account"], opened=esc_t, decided=decided,
                 outcome="SAR" if sar else "NO_SAR", alerts=[a["alert_id"]], lead=a["scenario"], lead_gen=a["gen"],
                 step=int(rc.integers(1, 3)))
        cases.append(c)
        recent.append(c)
        by_cust.setdefault(c["customer"], []).append(c)
        a["case"] = c
        a["outcome"] = c["outcome"]
    # the case manager numbers investigations as they open
    for c in cases:
        case_no += c.pop("step")
        c["case_id"] = "FCM-%07d" % case_no
    for a in escs:
        if isinstance(a["case"], dict):
            a["case"] = a["case"]["case_id"]
    W["runs"], W["alerts"], W["cases"] = runs, alerts, cases

    # ---- SAR filings: the initial report on each SAR case's decision, continuing-activity reports, amendments
    rs = C.rng("sars")
    filings = []
    for c in sorted(cases, key=lambda c: (c["decided"], c["case_id"])):
        if c["outcome"] != "SAR" or c["decided"] > C.EXTRACT_UTC:
            continue
        act_end = C.to_eastern(c["opened"]).date() - dt.timedelta(days=int(rs.integers(2, 12)))
        act_start = act_end - dt.timedelta(days=int(rs.integers(25, 120)))
        amount = int(rs.lognormal(np.log(38_000), 0.9))
        f = dict(key=len(filings), case_id=c["case_id"], filed=c["decided"], prior=None, start=act_start, end=act_end,
                 amount=amount, subjects=int(rs.choice([1, 1, 1, 2, 2, 3])), kind="initial")
        filings.append(f)
        prior = f
        if rs.random() < 0.45:
            for _k in range(2):
                review = C.to_eastern(prior["filed"]) + dt.timedelta(days=int(rs.integers(95, 121)))
                if rs.random() > 0.70:
                    break
                t = C.to_utc(_office_time(rs, review.date()))
                if t > C.EXTRACT_UTC:
                    break
                g = dict(key=len(filings), case_id=c["case_id"], filed=t, prior=prior["key"], prior_filed=prior["filed"],
                         start=prior["end"] + dt.timedelta(days=1),
                         end=review.date() - dt.timedelta(days=int(rs.integers(3, 15))),
                         amount=int(rs.lognormal(np.log(21_000), 0.8)), subjects=prior["subjects"], kind="continuing")
                filings.append(g)
                prior = g
    for f in list(filings):
        if rs.random() < 0.045:
            t = C.to_utc(_office_time(rs, (C.to_eastern(f["filed"]) + dt.timedelta(days=int(rs.integers(3, 46)))).date()))
            if t <= C.EXTRACT_UTC:
                filings.append(dict(key=len(filings), case_id=f["case_id"], filed=t, prior=f["key"],
                                    prior_filed=f["filed"], start=f["start"],
                                    end=f["end"], amount=f["amount"] + int(rs.integers(-900, 2500)),
                                    subjects=f["subjects"], kind="amendment"))
    # FinCEN numbers each filing as the e-filing system accepts it, so BSA IDs run in filing order
    filings.sort(key=lambda f: (f["filed"], f["key"]))
    rb = C.rng("bsa-ids")
    bsa = 31000025_000000 + int(rb.integers(10_000, 90_000))
    ids = {}
    for f in filings:
        bsa += int(rb.integers(40, 2600))
        ids[f["key"]] = str(bsa)
    # the tracker takes the prior report number from the filing's prior-report field, which the FIU's analysts
    # leave empty on some continuing activity reports and give in the narrative instead
    rp = C.rng("prior-field")
    for f in filings:
        f["bsa_id"] = ids[f["key"]]
        f["prior"] = ids[f["prior"]] if f["prior"] is not None else ""
        blank = rp.random() < 0.18
        f["shown_prior"] = "" if (f["kind"] == "continuing" and blank and f["prior_filed"] >= C.DATA0_UTC) else f["prior"]
    W["filings"] = filings
    return W


def truth(W):
    """Each scenario's true productivity over the tuning year: every non-duplicate alert by its eventual outcome."""
    n, s = {}, {}
    for a in W["alerts"]:
        if a["dup"] or not (C.P0 <= a["bdate"] <= C.P1):
            continue
        n[a["scenario"]] = n.get(a["scenario"], 0) + 1
        s[a["scenario"]] = s.get(a["scenario"], 0) + (a["outcome"] == "SAR")
    return {k: 100.0 * s[k] / n[k] for k in n}, n, s
