"""task464 architecture 12: the generator's assertions on the built pack (exit 1 on any failure).

    python3 generator/checks.py

Blocks: the three rules (R1 raw material, R2 each mess item neutral, R3a the analyst test, R3b the decisive step
alone, R3c no plant), the fork table (SF1 to SF18), the estimator family and its bins (lesson 7), the back-test
(lesson 12), the ask devices (forcing, lesson 8, zero main-population rows), the input gates, the realism sweep and
the distractors' deletion test.
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
TGT = os.path.join(BASE, "target")
sys.path.insert(0, HERE)
import answers as A  # noqa: E402
import world as W   # noqa: E402

RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))
    print("%s  %-70s %s" % ("PASS" if cond else "FAIL", label, detail))


def r(x, u):
    return int(u * round(float(x) / u))


class WH(A.Warehouse):
    """The warehouse read with one mess item mishandled."""
    def __init__(self, tgt, keep_dupes=False, drop_android=False):
        self.clicks = defaultdict(float)
        self.js = {}
        seen = set()
        with open(os.path.join(tgt, "sponsored_clicks_by_mailbox_daily.csv"), newline="") as f:
            for row in csv.DictReader(f):
                key = tuple(row.values())
                if not keep_dupes and key in seen:
                    continue
                seen.add(key)
                if drop_android and row["channel"] == "app_android":
                    continue
                d = dt.date.fromisoformat(row["click_date"])
                ch = "app" if row["channel"].startswith("app") else row["channel"]
                self.clicks[(d, row["mailbox_group"], row["audience"], ch)] += int(row["sponsored_clicks"])
                self.js[(d, row["mailbox_group"], row["audience"])] = int(row["jobseekers"])
        self.days = sorted({k[0] for k in self.js})


def sizing(wh, mode="event", channels=("alert_email", "website", "app"), controls=None, groups=None):
    U = A.uplift(wh)
    aff, _ = A.affected_groups(wh)
    aff = groups or aff
    ctl = controls or [g for g in A.GROUPS if g not in A.affected_groups(wh)[0]]
    D = sum(sum(A.group_dip(wh, g, ctl, channels, mode)) for g in aff)
    net = U - D
    return U, D, net, net * W.SENDS_2027 / 6.0


def text_of(path):
    if path.endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            return re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf-8"))
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    if path.endswith(".xlsx"):
        from openpyxl import load_workbook
        wb = load_workbook(path, read_only=True)
        return "\n".join(" ".join(str(c) for c in row if c is not None)
                         for ws in wb.worksheets for row in ws.iter_rows(values_only=True))
    return open(path, encoding="utf-8", errors="replace").read()


def pull_times(tgt):
    """Each restarter's sponsored clicks on the clock the pull states (UK), logged-out app clicks tied as the golden ties
    them."""
    dev = defaultdict(set)
    rows = list(csv.DictReader(open(os.path.join(tgt, "restarted_jobseekers_sponsored_clicks.csv"))))
    for x in rows:
        if x["account_id"] and x["app_install_id"]:
            dev[x["app_install_id"]].add(x["account_id"])
    for x in A.restart_rows(tgt):
        if x["app_install_id"]:
            dev[x["app_install_id"]].add(x["account_id"])
    out = defaultdict(list)
    for x in rows:
        a = x["account_id"]
        if not a and x["app_install_id"] and len(dev.get(x["app_install_id"], ())) == 1:
            a = next(iter(dev[x["app_install_id"]]))
        if a:
            out[a].append(dt.datetime.strptime(x["clicked_at_uk"], "%Y-%m-%d %H:%M:%S"))
    return out


def a2_under(per, times, inside, after=None):
    """Ask 5 under a window rule `inside(k, t)`; `after` maps (send, account) to a restart time for the post-restart
    reading."""
    out = []
    for k in range(6):
        n = 0
        for a in per[k]:
            ts = times.get(a, [])
            if after is not None:
                ts = [t for t in ts if t >= after[(k, a)]]
            n += any(inside(k, t) for t in ts)
        out.append(n)
    return out


def uk_from_utc(t):
    from zoneinfo import ZoneInfo
    return t.replace(tzinfo=dt.timezone.utc).astimezone(ZoneInfo("Europe/London")).replace(tzinfo=None)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    wh = A.Warehouse(TGT)
    U, D, net, f27 = sizing(wh)
    bins = {"2027": (f27, 100000), "gain": (U, 50000), "loss": (D, 50000), "net": (net, 50000)}
    gold_bins = {k: r(v, u) for k, (v, u) in bins.items()}

    # ---------------------------------------------------------------- the three rules
    with open(os.path.join(TGT, "sponsored_clicks_by_mailbox_daily.csv")) as f:
        head = next(csv.reader(f))
    ok("R1 the warehouse ships day x group x audience x channel clicks with jobseekers (the readout's raw rows)",
       head == ["click_date", "mailbox_group", "audience", "channel", "jobseekers", "sponsored_clicks"], str(head))
    cols = set()
    for n in os.listdir(TGT):
        if n.endswith(".csv"):
            with open(os.path.join(TGT, n)) as f:
                cols |= set(next(csv.reader(f)))
    ok("R1 no shipped column holds the deciding quantity (no loss, net, uplift, effect or incremental column)",
       not any(re.search(r"loss|net_|uplift|effect|incremental|lift", c) for c in cols), ", ".join(sorted(cols))[:80])
    for label, kw in [("the reload's repeated days kept", {"keep_dupes": True}),
                      ("the app's Android channel dropped from October", {"drop_android": True})]:
        w2 = WH(TGT, **kw)
        u2, d2, n2, f2 = sizing(w2)
        same = (r(f2, 100000) == gold_bins["2027"] and r(u2, 50000) == gold_bins["gain"] and
                r(d2, 50000) == gold_bins["loss"] and (f2 < 0))
        ok("R2 mess neutral: %s leaves the call and every graded bin" % label, same,
           "2027 %.0f, gain %.0f, loss %.0f" % (f2, u2, d2))
    ok("R2 mess neutral: the missing warehouse day (17 Aug 2025) lies outside every window and ratio",
       dt.date(2025, 8, 17) not in wh.days and all(dt.date(2025, 8, 17) < s for s in A.SENDS))
    default27 = U * W.SENDS_2027 / 6.0
    ok("R3a the analyst test: the holdout uplift carried files keep (+%d)" % round(default27),
       default27 > 0 and r(default27, 100000) == 200000 and fig["call"] == "drop", "%.0f" % default27)
    ok("R3b the decisive step alone: the default path plus the all-channel loss files the golden",
       r(f27, 100000) == fig["series_2027_clicks"], "%.0f" % f27)
    u_, d_g, n_g, f_g = sizing(wh, groups=["gmail"])
    u_, d_a, n_a, f_a = sizing(wh, channels=("alert_email",))
    ok("R3b each lower rung's single correction lands wrong (Google only, alert clicks only)",
       r(f_g, 100000) != fig["series_2027_clicks"] and r(f_a, 100000) != fig["series_2027_clicks"],
       "google-only %.0f, alert-only %.0f" % (f_g, f_a))
    docs = [os.path.join(TGT, n) for n in os.listdir(TGT) if n.endswith((".docx", ".pdf", ".xlsx"))]
    alltext = {os.path.basename(p): text_of(p) for p in docs}
    ok("R3c no plant: no shipped document states a result, a recommendation to keep, or a rate for the decision",
       not any(re.search(r"(uplift|incremental|recommend|results show|per cent of clicks|keep the series|proposal|"
                         r"we propose|should stay|should be kept|nothing else changes)", t, re.I)
               for t in alltext.values()))
    ok("R3c Gate H: no shipped document designates a yield measure (no arm-by-arm count, no pilot named as the evidence)",
       not any(re.search(r"(arm by arm|by arm|is the evidence|the pool's sponsored clicks|each arm's)", t, re.I)
               for t in alltext.values()))
    rows = list(csv.reader(open(os.path.join(TGT, "sponsored_clicks_by_mailbox_daily.csv"))))[1:]
    cnt = Counter(tuple(x) for x in rows)
    rep_days = sorted({k[0] for k, v in cnt.items() if v > 1})
    ok("R3c no plant: the only repeated rows are the reload's exact copies of 20 to 22 October 2026",
       rep_days == ["2026-10-20", "2026-10-21", "2026-10-22"], str(rep_days))

    # ---------------------------------------------------------------- the fork table
    plan = alltext["jobseeker_email_plan_2027.docx"]
    ok("SF1 sponsored clicks counted as the click system records them for billing; no Postvane column equals a warehouse total",
       "counted as the click system records them for billing" in plan)
    u_s = A.uplift(wh, stratified=True)
    ok("SF2 the plan judges the business's clicks with against without (the literal outcome)",
       "sponsored clicks Quaywork takes with it against what it would have taken without it" in plan)
    wins = A.pilot_days()
    ok("SF3 the six 28-day windows tile 14 Apr to 28 Sep 2026 with no gap or overlap",
       len(wins) == len(set(wins)) == 168 and min(wins) == W.SENDS[0] and max(wins) == W.PILOT_END)
    month = sizing_monthly(wh)
    ok("SF3 the calendar-month reading files the same call and 2027 bin", month < 0 and r(month, 100000) == gold_bins["2027"],
       "%.0f" % month)
    ok("SF4 the 2027 sizing is the pilot's net over six sends times thirteen (filed)",
       "sized at what one pilot send did on average, thirteen times" in plan and abs(f27 - net * 13 / 6) < 1e-6)
    ok("SF5 the holdout comparison pooled and stratified by mailbox group agree (C1)", abs(U - u_s) < 100,
       "%.0f against %.0f" % (U, u_s))
    aff, share = A.affected_groups(wh)
    ok("SF6 three groups fall after every send and the six others move under 0.6 per cent (C1)",
       aff == ["gmail", "microsoft", "yahoo_aol"] and all(abs(share[g]) < 0.006 for g in A.GROUPS if g not in aff),
       " ".join("%s %.4f" % (g, share[g]) for g in A.GROUPS))
    fam = {}
    six = [g for g in A.GROUPS if g not in aff]
    for name, kw in [("event, six controls", {}), ("full window, pre-pilot ratio", {"mode": "full"}),
                     ("interrupted series", {"mode": "its"}), ("event, Apple alone", {"controls": ["apple"]}),
                     ("event, broadband four", {"controls": ["bt", "sky", "virgin_media", "talktalk"]}),
                     ("event, Apple and Other", {"controls": ["apple", "other"]})]:
        fam[name] = sizing(wh, **kw)
    ok("SF7 every control set and the interrupted series land the 2027 figure in the -300,000 bin (C3)",
       all(r(v[3], 100000) == gold_bins["2027"] for v in fam.values()),
       "; ".join("%s %.0f" % (k, v[3]) for k, v in fam.items()))
    worst = min(min(abs(v[2]) - 125000, 175000 - abs(v[2])) for v in fam.values())
    ok("SF7 the standing family's nets sit at least 2,500 inside the -150,000 bin's edges", worst >= 2500, "%.0f" % worst)
    ok("SF7 every member of the standing family lands the pilot's loss in the 250,000 bin and its net in the -150,000 bin",
       all(r(v[1], 50000) == gold_bins["loss"] and r(v[2], 50000) == gold_bins["net"] for v in fam.values()),
       "; ".join("%.0f/%.0f" % (v[1], v[2]) for v in fam.values()))
    ok("SF8 the full-window reading on a pre-pilot ratio files the same bins as days 0 to 13 (C1)",
       r(fam["full window, pre-pilot ratio"][3], 100000) == gold_bins["2027"])
    ok("SF9 alert clicks only (no site and app netting) lands outside the golden's bin, ruled out by the outcome",
       r(f_a, 100000) != gold_bins["2027"] and "counted as the click system records them for billing" in plan,
       "%.0f" % f_a)
    w_d = WH(TGT, keep_dupes=True)
    ok("SF10 the reload's repeated days lie after every window: counted twice or once, the same figures (C1)",
       abs(sizing(w_d)[3] - f27) < 1e-6, "%.0f against %.0f" % (sizing(w_d)[3], f27))
    ios_and = sum(1 for x in rows if x[3] in ("app_ios", "app_android"))
    pre_app = sum(1 for x in rows if x[3] == "app" and x[0] >= "2026-10-01")
    ok("SF11 from 1 October 2026 the app arrives only as app_ios and app_android", ios_and > 0 and pre_app == 0)
    ok("SF12 the plan keeps the series only if it adds sponsored clicks", "stays in the plan if it adds sponsored clicks" in plan)
    ok("SF13 every pilot window closes before the data end", W.PILOT_END < W.END and max(wh.days) == W.END)
    rl = list(csv.DictReader(open(os.path.join(TGT, "alert_restarts_pilot_pool_2026.csv"))))
    nm = sum(wh.n(A.SENDS[0], g, "restart_pilot_mailed") for g in A.GROUPS)
    ok("SF14 the arms' sizes come from the warehouse (constant from 1 April), not the restart log",
       all(wh.n(d, "gmail", "restart_pilot_mailed") == wh.n(A.SENDS[0], "gmail", "restart_pilot_mailed")
           for d in wh.days if d >= W.POOL_DATE) and len({x["account_id"] for x in rl}) < nm)

    # ---------------------------------------------------------------- lesson 7 and lesson 12
    per = {g: A.group_dip(wh, g, six) for g in aff}
    shape_ok = all(max(v) / min(v) < 1.35 for v in per.values())
    ok("L7 the dip has one shape per send at each group (max over min under 1.35)", shape_ok,
       " ".join("%s %.2f" % (g, max(v) / min(v)) for g, v in per.items()))
    clean = []
    for g in aff:
        for k in range(6):
            ref = A.window_days(k, 14, 28)
            num = sum(wh.total(d, g, "alerts_on") for d in ref) / sum(wh.n(d, g, "alerts_on") for d in ref)
            den = sum(wh.total(d, c, "alerts_on") for d in ref for c in six) / sum(wh.n(d, c, "alerts_on") for d in ref for c in six)
            clean.append((g, num / den))
    pre = {}
    for g in aff:
        ref = [W.SENDS[0] - dt.timedelta(days=i) for i in range(1, 99)]
        ref = [d for d in ref if wh.n(d, g, "alerts_on")]
        pre[g] = (sum(wh.total(d, g, "alerts_on") for d in ref) / sum(wh.n(d, g, "alerts_on") for d in ref)) / \
            (sum(wh.total(d, c, "alerts_on") for d in ref for c in six) / sum(wh.n(d, c, "alerts_on") for d in ref for c in six))
    ok("L7 no trend and no overlap: each window's days 14 to 27 sit within 1 per cent of the pre-pilot ratio",
       all(abs(v / pre[g] - 1) < 0.01 for g, v in clean), "max %.4f" % max(abs(v / pre[g] - 1) for g, v in clean))
    ok("L7 the interrupted series and the difference in differences give the same sign and 2027 bin",
       (fam["interrupted series"][3] < 0) and r(fam["interrupted series"][3], 100000) == gold_bins["2027"])
    ok("L7 the six control groups show no dip after any send (each against the other five)",
       all(abs(sum(A.group_dip(wh, g, [c for c in six if c != g])) /
               sum(wh.total(d, g, "alerts_on") for k in range(6) for d in A.window_days(k, 0, 14))) < 0.01 for g in six))
    bt_ok = True
    detail = []
    for g in aff:
        first, last = sum(per[g][:3]) / 3, sum(per[g][3:]) / 3
        detail.append("%s %.0f/%.0f" % (g, first, last))
        bt_ok &= abs(last / first - 1) < 0.10
    ok("L12 back-test: the dip fitted on sends 1 to 3 predicts sends 4 to 6 within 10 per cent at each group",
       bt_ok, "; ".join(detail))
    ok("L12 back-test: the restarted arms' gain per send is positive in every window (the textbook route validates)",
       all(window_gain(wh, k) > 0 for k in range(6)))

    # ---------------------------------------------------------------- the asks
    plain = A.restarts_by_send(TGT, "plain")
    gold1 = A.restarts_by_send(TGT, "golden")
    ok("A1 golden restarts by people reproduce figures.json", [len(s) for s in gold1] == fig["restarted_by_people"])
    ok("A1 the plain count misses every send", all(len(p) != len(g) for p, g in zip(plain, gold1)),
       str([len(p) - len(g) for p, g in zip(plain, gold1)]))
    over = A.restarts_by_send(TGT, "fast", 3600)
    ok("A1 the one-hour cut misses every send", all(len(o) != len(g) for o, g in zip(over, gold1)),
       str([len(o) - len(g) for o, g in zip(over, gold1)]))
    conv = set()
    for links in (3, 4, 5, 6):
        for secs in (2, 5, 10, 30, 60):
            b, _ = A.burst_keys(TGT, links, secs)
            conv.add(len(b))
    ok("A1 the burst rule converges: 3 to 6 links inside 2 to 60 seconds select the same emails", len(conv) == 1, str(conv))
    b, ev = A.burst_keys(TGT)
    human_max = 0
    for key, lst in ev.items():
        if key in b:
            continue
        lst.sort()
        for i in range(len(lst)):
            human_max = max(human_max, len({l for t, l in lst if 0 <= (t - lst[i][0]).total_seconds() <= 60}))
    burst_min = min(len({l for t, l in ev[k]}) for k in b)
    ok("A1 lesson 8: no person clicks more than two links of an email in a minute; every burst clicks six or more",
       human_max <= 2 and burst_min >= 6, "people max %d, bursts min %d" % (human_max, burst_min))
    a2g = A.clicked_within(TGT, gold1, True)
    a2p = A.clicked_within(TGT, plain, False)
    ok("A2 golden clickers reproduce figures.json", a2g == fig["clicked_within_28_days"])
    ok("A2 the account-only count misses every send", all(x != y for x, y in zip(a2g, a2p)),
       str([y - x for x, y in zip(a2g, a2p)]))
    ck = list(csv.DictReader(open(os.path.join(TGT, "restarted_jobseekers_sponsored_clicks.csv"))))
    dev = defaultdict(set)
    for x in ck:
        if x["account_id"] and x["app_install_id"]:
            dev[x["app_install_id"]].add(x["account_id"])
    for x in rl:
        if x["app_install_id"]:
            dev[x["app_install_id"]].add(x["account_id"])
    lo = [x for x in ck if not x["account_id"]]
    ok("A2 lesson 8: every logged-out click's install carries exactly one jobseeker",
       all(len(dev.get(x["app_install_id"], ())) == 1 for x in lo) and all(x["channel"] == "app" for x in lo),
       "%d logged-out clicks" % len(lo))
    # ---------------------------------------------------------------- ask 5's window, the clocks, the email's links
    prompt = open(os.path.join(BASE, "prompt.txt")).read()
    times = pull_times(TGT)
    cal = lambda k, t: A.SENDS[k] <= t.date() <= A.SENDS[k] + dt.timedelta(days=W.WINDOW - 1)
    a2cal = a2_under(gold1, times, cal)
    a2hrs = a2_under(gold1, times, lambda k, t: dt.datetime.combine(A.SENDS[k], dt.time(10)) <= t <
                     dt.datetime.combine(A.SENDS[k], dt.time(10)) + dt.timedelta(days=W.WINDOW))
    ok("SF15 ask 5's window is filed as calendar days, the send's date first: the golden is that count, the "
       "28 x 24 hours from the 10:00 send another",
       "on the send's date or in the 27 days after it" in prompt and a2cal == fig["clicked_within_28_days"] and
       a2hrs != a2cal, "hours %s" % a2hrs)
    rt = {}
    for x in rl:
        if x["route"] == "email_link" and x["link_campaign"] in A.RS:
            k = A.RS.index(x["link_campaign"])
            if x["account_id"] in gold1[k]:
                t = dt.datetime.strptime(x["restarted_at_uk"], "%Y-%m-%d %H:%M")
                rt[(k, x["account_id"])] = min(rt.get((k, x["account_id"]), t), t)
    a2post = a2_under(gold1, times, cal, after=rt)
    ok("SF16 ask 5 counts every click in the window, before or after restarting (the prompt says so); after the "
       "restart only is another count", "whether before or after restarting" in prompt and a2post != a2cal,
       "after only %s" % a2post)
    import sim  # noqa: E402  the clean truth: nothing in a send's window is missing from the pull
    h = sim.simulate()
    pool = h["pool"]
    cm, ct = pool["clicks"]["m"], pool["clicks"]["t"]
    by_m = defaultdict(list)
    for m_, t_ in zip(cm.tolist(), ct.tolist()):
        by_m[m_].append(t_)
    gap = 0
    for (m_, d_, tod, route, k_, sc) in pool["restarts"]:
        if route == "email_link" and not sc:
            s0 = pool["send_days"][k_]
            gap += sum(1 for t_ in by_m.get(m_, ()) if s0 <= t_ < d_)
    ok("SF16 the pull loses nothing in a window: no restarter made a sponsored click between the send's date and "
       "the restart day (clean truth)", gap == 0, "%d clicks" % gap)
    ev_rows = list(csv.DictReader(open(os.path.join(TGT, "postvane_clicks_restart_series_2026.csv"))))
    first_restart = {}
    for x in ev_rows:
        if x["link_name"] == "restart_alerts":
            t = uk_from_utc(dt.datetime.strptime(x["clicked_at_utc"][:19], "%Y-%m-%dT%H:%M:%S")).replace(second=0)
            key = (x["campaign_code"], x["subscriber_key"])
            first_restart[key] = min(first_restart.get(key, t), t)
    gaps, rival = Counter(), Counter()
    for x in rl:
        key = (x["link_campaign"], x["account_id"])
        if x["route"] == "email_link" and key in first_restart:
            lt = dt.datetime.strptime(x["restarted_at_uk"], "%Y-%m-%d %H:%M")
            gaps[(lt - first_restart[key]).total_seconds() / 60] += 1
            rival[(uk_from_utc(lt) - first_restart[key]).total_seconds() / 60] += 1
    heads_ok = ("restarted_at_uk" in rl[0] and "clicked_at_uk" in ck[0] and "clicked_at_utc" in ev_rows[0])
    a2utc = a2_under(gold1, {a: [uk_from_utc(t) for t in ts] for a, ts in times.items()}, cal)
    ok("SF17 the restart log and the pull carry their clock in the header (UK), Postvane its own (UTC); the golden "
       "is the labelled reading", heads_ok and a2cal == fig["clicked_within_28_days"], "as UTC: %s" % a2utc)
    ok("SF17 the rival clock is impossible: every email restart logs the minute of the Postvane click that made it "
       "on the UK clock, and would trail it by exactly an hour read as UTC",
       set(gaps) == {0.0} and sum(gaps.values()) > 40000 and set(rival) == {60.0} and a2utc != a2cal,
       "%d restarts, gaps %s" % (sum(gaps.values()), sorted(gaps)))
    links = {x["link_name"] for x in ev_rows}
    brief_txt = re.sub(r"\s+", " ", text_of(os.path.join(TGT, "restart_pilot_brief_2026.pdf")))
    plan_txt = re.sub(r"\s+", " ", text_of(os.path.join(TGT, "jobseeker_email_plan_2027.docx")))
    ok("SF18 the restart email links to six sector pages and no job, so no Postvane click is a click on a sponsored job",
       not any(l.startswith("job_") for l in links) and len(links) == 11 and
       "newest jobs near them in six sectors" in plan_txt and "newest jobs near them in six sectors" in brief_txt,
       ", ".join(sorted(links)))
    ok("Asks: zero device rows in the main call's population (the warehouse has no account, device or link column)",
       not {"account_id", "app_install_id", "link_name", "subscriber_key"} & set(head))

    # ---------------------------------------------------------------- input gates and realism
    names = sorted(os.listdir(TGT))
    fmts = {n.rsplit(".", 1)[1] for n in names}
    big = max(sum(1 for _ in open(os.path.join(TGT, n))) - 1 for n in names if n.endswith(".csv"))
    meta = json.load(open(os.path.join(BASE, "metadata.json")))
    ok("Gate: 10 or more files, 3 or more formats, a 25,000-row file", len(names) >= 10 and len(fmts) >= 3 and big >= 25000,
       "%d files, %s, %d rows" % (len(names), sorted(fmts), big))
    ok("Gate: two or more distractors named in metadata.json, none in a file name",
       len(meta["distractor_files"]) >= 2 and not any("distract" in n for n in names))
    ok("Gate: every file has source, date and licence in metadata.json",
       all(f.get("source") and f.get("date") and f.get("licence") for f in meta["files"]) and len(meta["files"]) == len(names))
    ok("Gate: no file or sheet describes the data (readme, dictionary, notes, manifest, field guide)",
       not any(re.search(r"readme|dictionary|notes|manifest|field_guide|codebook", n, re.I) for n in names))
    ids = [int(x[0][3:]) for x in csv.reader(open(os.path.join(TGT, "restarted_jobseekers_sponsored_clicks.csv")))
           if x[0].startswith("qc")]
    steps = {b - a for a, b in zip(ids[:2000], ids[1:2001])}
    ok("Realism: click ids are not an arithmetic sequence", len(steps) > 1, str(sorted(steps)[:5]))
    evid = [int(x[0][4:]) for x in csv.reader(open(os.path.join(TGT, "postvane_clicks_restart_series_2026.csv")))
            if x[0].startswith("evt_")]
    ok("Realism: Postvane event ids are not an arithmetic sequence", len({b - a for a, b in zip(evid[:2000], evid[1:2001])}) > 1)
    sv = list(csv.DictReader(open(os.path.join(TGT, "alerts_feedback_survey_2026-06.csv"))))
    norm = lambda s: " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    com = Counter(norm(x["comment"]) for x in sv if x["comment"].strip())
    masked = Counter(re.sub(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b", "#", k) for k in
                     (norm(x["comment"]) for x in sv if x["comment"].strip()))
    ok("Realism: the survey's free text repeats no comment more than twice, and no wording recurs with only a "
       "number swapped", com and max(com.values()) <= 2 and max(masked.values()) <= 2,
       "%d comments, %d distinct, max %d, max with numbers masked %d"
       % (sum(com.values()), len(com), max(com.values()), max(masked.values())))
    hint = re.compile(r"(spam|junk|inbox|filter|folder|deliver|arriv|restart|link|gateway|scan|secur|work email|"
                      r"gmail|outlook|hotmail|yahoo|blocked|bounce|click)", re.I)
    ok("Realism: no survey comment carries the step's or the devices' vocabulary",
       not any(hint.search(x["comment"]) for x in sv), str([x["comment"] for x in sv if hint.search(x["comment"])][:3]))
    tot = [round(v) for v in fig["loss_by_group_exact"].values()] + [round(fig["pilot_uplift_exact"])]
    ok("Realism: no round headline totals", all(t % 1000 for t in tot), str(tot))
    persons = set(W.PEOPLE.values())
    card = json.load(open(os.path.join(BASE, "..", ".claude", "skills", "fingerprint", "cards", "task464.json")))
    ok("Realism: every persona is on the card, drawn with guard.py names", persons <= set(card["world"]["people"]))
    dash = any("\u2014" in t or "\u2013" in t for t in alltext.values())
    ok("Realism: no em or en dash in any shipped document", not dash)
    ok("Realism: the plan postdates the data it describes and the brief predates the pilot",
       re.search(r"16 November 2026", plan) and "10 March 2026" in alltext["restart_pilot_brief_2026.pdf"])
    ok("Realism: positive control, every document's text extracts (non-empty) through the same reader",
       all(len(t) > 300 for t in alltext.values()), str({k: len(v) for k, v in alltext.items()}))
    vocab = re.compile(r"\b(junk|spam folder|reputation|deliverability|inbox placement|spam trap|interference|spillover|"
                       r"gateway|scanner|logged.out|bot)\b", re.I)
    ok("Leak: no shipped document carries the decisive step's or the devices' vocabulary",
       not any(vocab.search(t) for t in alltext.values()) and "judged on the sponsored clicks" in plan)
    ok("Gate G: no shipped document states a count of sponsored clicks or sizes the series",
       not any(re.search(r"\d[\d,]*\s+(more |fewer |extra )?sponsored clicks", t, re.I) for t in alltext.values()))

    # ---------------------------------------------------------------- distractors deleted
    tmp = tempfile.mkdtemp(prefix="t464_")
    try:
        for n in names:
            if "target/" + n not in meta["distractor_files"]:
                os.symlink(os.path.join(TGT, n), os.path.join(tmp, n))
        f2 = A.figures(write=False, tgt=tmp)
        same = all(f2[k] == fig[k] for k in ("series_2027_clicks_exact", "pilot_uplift_exact", "pilot_loss_exact",
                                             "restarted_by_people", "clicked_within_28_days"))
        ok("Distractors: the golden and every ask unchanged with both distractors deleted", same)
        for n in ("postvane_daily_by_domain_group.csv", "inkrelay_export_2025-01-01_to_2025-03-16.csv"):
            os.remove(os.path.join(tmp, n))
        w3 = A.Warehouse(tmp)
        ok("R2 mess neutral: Postvane's UTC daily statistics and Inkrelay's layout are never read by the main call",
           abs(sizing(w3)[3] - f27) < 1e-6)
    finally:
        shutil.rmtree(tmp)

    # ---------------------------------------------------------------- bins
    for k, (v, u) in bins.items():
        edge = abs((v / u) - round(v / u)) * u
        ok("Bins: %s sits %.0f from its nearest-%d bin edge (at least a fifth of the bin from the edge)" %
           (k, u / 2 - edge, u), u / 2 - edge >= u * 0.2, "%.0f" % v)
    fails = [x for x in RES if not x[1]]
    print("checks: %d assertions, %d failures" % (len(RES), len(fails)))
    return 1 if fails else 0


def window_gain(wh, k):
    days = A.window_days(k)
    cm = sum(wh.total(d, g, "restart_pilot_mailed") for d in days for g in A.GROUPS)
    ch = sum(wh.total(d, g, "restart_pilot_holdout") for d in days for g in A.GROUPS)
    nm = sum(wh.n(A.SENDS[0], g, "restart_pilot_mailed") for g in A.GROUPS)
    nh = sum(wh.n(A.SENDS[0], g, "restart_pilot_holdout") for g in A.GROUPS)
    return cm / nm - ch / nh


def sizing_monthly(wh):
    """The calendar-month reading: April to September 2026 in place of the six windows."""
    months = [d for d in wh.days if dt.date(2026, 4, 1) <= d <= dt.date(2026, 9, 30)]
    nm = sum(wh.n(A.SENDS[0], g, "restart_pilot_mailed") for g in A.GROUPS)
    nh = sum(wh.n(A.SENDS[0], g, "restart_pilot_holdout") for g in A.GROUPS)
    cm = sum(wh.total(d, g, "restart_pilot_mailed") for d in months for g in A.GROUPS)
    ch = sum(wh.total(d, g, "restart_pilot_holdout") for d in months for g in A.GROUPS)
    U = (cm / nm - ch / nh) * nm
    aff, _ = A.affected_groups(wh)
    six = [g for g in A.GROUPS if g not in aff]
    D = sum(sum(A.group_dip(wh, g, six)) for g in aff)
    return (U - D) * 13 / 6.0


if __name__ == "__main__":
    sys.exit(main())
