"""task464 architecture 12: write the data files under target/ from the simulation.

Every file is an export a real job board keeps for its own reasons: the warehouse's daily sponsored clicks by mailbox
group (the CRM team's standard cut), the email platforms' daily campaign statistics (Postvane since the March 2025
migration, Inkrelay before it), Postvane's click events for the restart emails, the alert system's restart log for
the pilot's pool, the CRM's pull of the clicks restarted jobseekers made in the 28 days from their send, and two
files the decision does not need (finance's sponsored revenue by sector, the June alerts survey).
"""
import csv
import datetime as dt
import hashlib
import os

import numpy as np

import world as W

WH_GROUP = ["gmail", "microsoft", "yahoo_aol", "apple", "bt", "sky", "virgin_media", "talktalk", "other"]
SL_GROUP = ["Gmail", "Microsoft", "Yahoo/AOL", "Apple", "BT", "Sky", "Virgin Media", "TalkTalk", "Other"]
PB_ISP = ["GMAIL", "HOTMAIL/OUTLOOK", "YAHOO", "ICLOUD", "BTINTERNET", "SKY", "VIRGINMEDIA", "TALKTALK", "OTHER"]
RS_CODE = ["RS-2604", "RS-2605", "RS-2606", "RS-2607", "RS-2608", "RS-2609"]
# the restart email's links: the restart button, six sector tiles that open the newest jobs near the jobseeker in
# that sector (a search page, not a job), and the footer
TILES = ["jobs_care", "jobs_driving", "jobs_warehouse", "jobs_retail", "jobs_admin", "jobs_hospitality"]
LINKS = ["restart_alerts"] + TILES + ["manage_alerts", "privacy", "help", "unsubscribe_page"]
APP_SPLIT = dt.date(2026, 10, 1)
RELOAD = [dt.date(2026, 10, 20), dt.date(2026, 10, 21), dt.date(2026, 10, 22)]
WH_GAP = dt.date(2025, 8, 17)


def bst(d):
    """True when a UK date falls in British Summer Time (last Sunday of March to last Sunday of October)."""
    def last_sun(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return last_sun(d.year, 3) <= d < last_sun(d.year, 10)


def to_utc(day, minute):
    """A UK local day and minute of day to a UTC datetime."""
    t = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=int(minute))
    return t - dt.timedelta(hours=1 if bst(t.date()) else 0)


def device_id(m):
    h = hashlib.md5(("qw-device-%d" % m).encode()).hexdigest().upper()
    return "%s-%s-%s" % (h[:8], h[8:12], h[12:16])


def job_ref(rng):
    return "QJ%07d" % int(rng.integers(1_000_000, 9_999_999))


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def warehouse(h, tgt):
    days, a, pool = h["days"], h["active"], h["pool"]
    idx = h["idx"]
    prov, held = pool["prov"], pool["held"]
    t0 = pool["t0"]
    n_m = np.bincount(prov[~held], minlength=9)
    n_h = np.bincount(prov[held], minlength=9)
    # the pool's clicks by day, provider, arm and channel (the warehouse stitches app devices to accounts)
    c = pool["clicks"]
    T = len(days)
    pc = np.zeros((2, T, 9, 3), dtype=int)
    arm = held[c["m"]].astype(int)
    np.add.at(pc, (arm, c["t"], prov[c["m"]], c["ch"]), 1)
    rng = np.random.default_rng(W.SEED + 1)
    rows = []
    for t, d in enumerate(days):
        if d == WH_GAP:
            continue
        auds = [("alerts_on", None)] + ([("restart_pilot_mailed", 0), ("restart_pilot_holdout", 1)] if t >= t0 else [])
        for aud, ai in auds:
            for p in range(9):
                if ai is None:
                    js = int(a["jobseekers"][t, p])
                    vals = [int(a["alert"][t, p]), int(a["website"][t, p]), int(a["app"][t, p])]
                else:
                    js = int(n_m[p] if ai == 0 else n_h[p])
                    vals = [int(pc[ai, t, p, 0]), int(pc[ai, t, p, 1]), int(pc[ai, t, p, 2])]
                base = [d.isoformat(), WH_GROUP[p], aud]
                rows.append(base + ["alert_email", js, vals[0]])
                rows.append(base + ["website", js, vals[1]])
                if d >= APP_SPLIT:
                    ios = int(rng.binomial(vals[2], 0.57))
                    rows.append(base + ["app_ios", js, ios])
                    rows.append(base + ["app_android", js, vals[2] - ios])
                else:
                    rows.append(base + ["app", js, vals[2]])
        if d in RELOAD:
            rows.extend([list(r) for r in rows[-(len(auds) * 9 * 3):]])
    return write_csv(os.path.join(tgt, "sponsored_clicks_by_mailbox_daily.csv"),
                     ["click_date", "mailbox_group", "audience", "channel", "jobseekers", "sponsored_clicks"], rows)


def esp_daily(h, tgt):
    """Postvane from 17 March 2025, Inkrelay before it: the daily alert email, the weekly digest, the six restart sends."""
    days, a, pool, jt = h["days"], h["active"], h["pool"], h["jt"]
    rng = np.random.default_rng(W.SEED + 2)
    prov = pool["prov"]
    # alert recipients: active jobseekers and restarted pool members, about 1.3 alert emails each
    T = len(days)
    delta = np.zeros((T + 1, 9))
    for (m, d0, tod, route, k, sc) in pool["restarts"]:
        delta[d0, prov[m]] += 1
    for (m, d0) in pool["repauses"]:
        delta[d0, prov[m]] -= 1
    restored_n = np.cumsum(delta[:T], axis=0)
    c = pool["clicks"]
    pool_alert = np.zeros((T, 9))
    sel = c["ch"] == 0
    np.add.at(pool_alert, (c["t"][sel], prov[c["m"][sel]]), 1)
    sl, pb = [], []
    open_rate = np.array([0.24, 0.21, 0.19, 0.96, 0.18, 0.20, 0.19, 0.17, 0.22])
    for t, d in enumerate(days):
        js = a["jobseekers"][t] + restored_n[t]
        sent = np.round(js * 1.31).astype(int)
        clicks_s = a["alert"][t] + pool_alert[t]
        for p in range(9):
            s = int(sent[p])
            hb = int(rng.binomial(s, 0.0004))
            sb = int(rng.binomial(s, 0.0021))
            dl = s - hb - sb
            op = int(rng.binomial(dl, open_rate[p] * (1 - 0.5 * jt[t, p])))
            ck = int(round(clicks_s[p] / 0.62 * rng.uniform(0.97, 1.03)))
            un = int(rng.binomial(dl, 0.00011))
            cp = int(rng.binomial(dl, 0.00004)) if p in (1, 2) else 0
            if d < W.MIGRATION:
                pb.append([d.strftime("%d/%m/%Y"), "Job alerts - daily", PB_ISP[p], s, hb + sb, op, ck, un])
            else:
                sl.append([d.isoformat(), "JA-DAILY", SL_GROUP[p], s, dl, hb, sb, op, ck, un, cp])
        if d.weekday() == 6:
            for p in range(9):
                s = int(round(a["jobseekers"][t, p] * 0.83))
                hb = int(rng.binomial(s, 0.0005)); sb = int(rng.binomial(s, 0.003)); dl = s - hb - sb
                op = int(rng.binomial(dl, open_rate[p] * 0.9)); ck = int(rng.binomial(dl, 0.021))
                un = int(rng.binomial(dl, 0.0004)); cp = int(rng.binomial(dl, 0.00006)) if p in (1, 2) else 0
                if d < W.MIGRATION:
                    pb.append([d.strftime("%d/%m/%Y"), "Weekly digest", PB_ISP[p], s, hb + sb, op, ck, un])
                else:
                    sl.append([d.isoformat(), "JA-DIGEST", SL_GROUP[p], s, dl, hb, sb, op, ck, un, cp])
    # restart sends
    stats = restart_send_stats(h)
    for k, sd in enumerate(W.SENDS):
        for p in range(9):
            s, dl, hb, sb, op, ck, un, cp = stats[k][p]
            sl.append([sd.isoformat(), RS_CODE[k], SL_GROUP[p], s, dl, hb, sb, op, ck, un, cp])
    sl.sort(key=lambda r: (r[0], r[1], SL_GROUP.index(r[2])))
    n1 = write_csv(os.path.join(tgt, "postvane_daily_by_domain_group.csv"),
                   ["send_date_utc", "campaign_code", "domain_group", "sent", "delivered", "hard_bounces",
                    "soft_bounces", "unique_opens", "unique_clicks", "unsubscribes", "spam_complaints"], sl)
    n2 = write_csv(os.path.join(tgt, "inkrelay_export_2025-01-01_to_2025-03-16.csv"),
                   ["Date", "Mailing", "ISP", "Sent", "Bounced", "Opened", "Clicked", "Unsubscribed"], pb)
    return n1, n2


def restart_send_stats(h):
    """Per restart send and provider: sent, delivered, bounces, opens, unique clickers, unsubscribes, complaints."""
    pool = h["pool"]
    rng = np.random.default_rng(W.SEED + 3)
    prov, held, dead = pool["prov"], pool["held"], pool["dead"]
    n = pool["n"]
    restarted_before = {}
    out = []
    # who was mailed at each send: not held out, not restarted and still running, not suppressed after a hard bounce
    status = mailed_lists(h)
    open_rate = np.array([0.13, 0.11, 0.10, 0.93, 0.09, 0.10, 0.10, 0.09, 0.12])
    clickers = {}
    for (m, k, mins, link) in pool["email_clicks"]:
        clickers.setdefault(k, set()).add(m)
    for (m, k, lag) in pool["scans"]:
        clickers.setdefault(k, set()).add(m)
    for k in range(6):
        ml = status[k]
        rows = []
        for p in range(9):
            sel = ml[prov[ml] == p]
            s = int(sel.size)
            hb = int(dead[sel].sum()) if k == 0 else int(rng.binomial(s, 0.0009))
            sb = int(rng.binomial(s, 0.004))
            dl = s - hb - sb
            op = int(rng.binomial(dl, open_rate[p]))
            ck = int(sum(1 for m in clickers.get(k, ()) if prov[m] == p))
            un = int(rng.binomial(dl, 0.0016))
            cp = int(rng.binomial(dl, 0.00045)) if p in (1, 2) else 0
            rows.append((s, dl, hb, sb, op, ck, un, cp))
        out.append(rows)
    return out


def mailed_lists(h):
    """The pool members each restart send went to (recomputed from the simulation's restart and re-pause events)."""
    pool = h["pool"]
    n = pool["n"]
    held, dead = pool["held"], pool["dead"]
    send_days = pool["send_days"]
    on = np.zeros(n, bool)
    ev = []
    for (m, d, tod, route, k, sc) in pool["restarts"]:
        ev.append((d, 0, m))
    for (m, d) in pool["repauses"]:
        ev.append((d, 1, m))
    ev.sort()
    out = []
    i = 0
    suppressed = np.zeros(n, bool)
    for k, sd in enumerate(send_days):
        while i < len(ev) and ev[i][0] < sd:
            d, kind, m = ev[i]
            on[m] = (kind == 0)
            i += 1
        ml = np.where((~held) & (~on) & (~suppressed))[0]
        # restarts on the send day itself come from this send's own emails
        out.append(ml)
        if k == 0:
            suppressed |= dead
    return out


def restart_clicks(h, tgt):
    pool, days = h["pool"], h["days"]
    rng = np.random.default_rng(W.SEED + 4)
    acct, deliver = pool["acct"], pool["deliver"]
    rows = []
    for (m, k, lag) in pool["scans"]:
        sd = W.SENDS[k]
        t = to_utc(sd, 600 + int(deliver[m]) + lag) + dt.timedelta(seconds=int(rng.integers(0, 50)))
        # a gateway follows most or all of the email's links in one pass, the restart link among them
        others = [l for l in LINKS if l != "restart_alerts"]
        nl = int(rng.integers(5, 11))
        pick = ["restart_alerts"] + [others[x] for x in rng.choice(len(others), size=nl, replace=False)]
        rng.shuffle(pick)
        step = int(rng.integers(30, 220))
        for j2, link in enumerate(pick):
            rows.append([RS_CODE[k], int(acct[m]), link, t + dt.timedelta(milliseconds=j2 * step + int(rng.integers(0, 25)))])
    for (m, k, mins, link) in pool["email_clicks"]:
        sd = W.SENDS[k]
        t = to_utc(sd, 600 + int(deliver[m]) + mins) + dt.timedelta(seconds=int(rng.integers(0, 60)))
        name = "restart_alerts" if link == "restart" else TILES[int(rng.integers(1, 7)) - 1]
        rows.append([RS_CODE[k], int(acct[m]), name, t])
    rows.sort(key=lambda r: (r[3], r[1], r[2]))
    out = []
    for i, r in enumerate(rows):
        ts = r[3].strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (r[3].microsecond // 1000)
        out.append(["evt_%08d" % (1_200_000 + i * 7 + int(rng.integers(0, 7))), r[0], r[1], r[2], ts])
    return write_csv(os.path.join(tgt, "postvane_clicks_restart_series_2026.csv"),
                     ["event_id", "campaign_code", "subscriber_key", "link_name", "clicked_at_utc"], out)


def restart_log(h, tgt):
    pool, days = h["pool"], h["days"]
    acct, held = pool["acct"], pool["held"]
    rows = []
    for (m, d, tod, route, k, sc) in pool["restarts"]:
        day = days[d]
        ts = "%s %02d:%02d" % (day.isoformat(), (tod // 60) % 24, tod % 60)
        rows.append([int(acct[m]), "holdout" if held[m] else "mailed", ts, route,
                     device_id(m) if route == "app" else "", RS_CODE[k] if route == "email_link" else ""])
    rows.sort(key=lambda r: (r[2], r[0]))
    return write_csv(os.path.join(tgt, "alert_restarts_pilot_pool_2026.csv"),
                     ["account_id", "pilot_arm", "restarted_at_uk", "route", "app_install_id", "link_campaign"], rows)


def restarted_clicks(h, tgt):
    """The CRM's pull: every sponsored click by the jobseekers whose alerts a restart email's link restarted, from the
    date of the send whose link restarted them to 8 November 2026, on the UK clock. A paused jobseeker makes no
    sponsored click, so the rows start on the restart day (checks.py asserts nothing in a send's window is missing)."""
    pool, days, idx = h["pool"], h["days"], h["idx"]
    rng = np.random.default_rng(W.SEED + 5)
    acct = pool["acct"]
    first = {}
    for (m, d, tod, route, k, sc) in pool["restarts"]:
        if route == "email_link" and not sc:
            first[m] = min(first.get(m, 10 ** 9), d)
    c = pool["clicks"]
    rows = []
    for i in range(c["m"].size):
        m = int(c["m"][i])
        t = int(c["t"][i])
        if m not in first or t < first[m]:
            continue
        ch = ["alert_email", "website", "app"][int(c["ch"][i])]
        li = bool(c["li"][i])
        tod = int(rng.integers(360, 1410))
        ts = "%s %02d:%02d:%02d" % (days[t].isoformat(), tod // 60, tod % 60, int(rng.integers(0, 60)))
        rows.append([ts, int(acct[m]) if li else "", device_id(m) if ch == "app" else "", ch, job_ref(rng)])
    rows.sort(key=lambda r: (r[0], str(r[1]), r[2]))
    out = [["qc%09d" % (40_000_000 + i * 3 + int(rng.integers(0, 3)))] + r for i, r in enumerate(rows)]
    return write_csv(os.path.join(tgt, "restarted_jobseekers_sponsored_clicks.csv"),
                     ["click_id", "clicked_at_uk", "account_id", "app_install_id", "channel", "job_ref"], out)


def write_all(h, tgt):
    st = {}
    st["warehouse"] = warehouse(h, tgt)
    st["esp"] = esp_daily(h, tgt)
    st["restart_clicks"] = restart_clicks(h, tgt)
    st["restart_log"] = restart_log(h, tgt)
    st["restarted_clicks"] = restarted_clicks(h, tgt)
    return st
