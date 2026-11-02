"""task464 architecture 12: simulate Quaywork's jobseekers, January 2025 to 8 November 2026.

The active base is simulated by day, mailbox provider and channel. The paused pool of 1 April 2026 is simulated member
by member: its random tenth held out, the six restart sends to the rest, gateway scans, restarts, the restarted
jobseekers' sponsored clicks (web, app logged in, app logged out), re-pauses. Each restart send leaves the Google,
Microsoft and Yahoo mailboxes filing Quaywork's alerts as junk for some days; the alert clicks they lose are partly made
on the site and app instead. Everything is drawn from world.SEED.
"""
import datetime as dt

import numpy as np

import world as W

P = len(W.PROVIDERS)
AFF = np.array([p in W.JUNK_PEAK for p in W.PROVIDERS])
JPEAK = np.array([W.JUNK_PEAK.get(p, 0.0) for p in W.PROVIDERS])


def day_index():
    n = (W.END - W.START).days + 1
    days = [W.START + dt.timedelta(days=i) for i in range(n)]
    return days, {d: i for i, d in enumerate(days)}


def dip_shape(t):
    """Share of a send's peak junk filing on day t after the send (t = 0 the send day)."""
    t = np.asarray(t, dtype=float)
    out = np.where(t == 0, W.JUNK_DAY0, np.exp(-(t - 1) / W.JUNK_TAU))
    return np.where((t < 0) | (t > 16), 0.0, out)


def junk_matrix(days, idx):
    T = len(days)
    j = np.zeros((T, P))
    for s in W.SENDS:
        i0 = idx[s]
        t = np.arange(T) - i0
        j += dip_shape(t)[:, None] * JPEAK[None, :]
    return np.minimum(j, 0.9)


def simulate():
    rng = np.random.default_rng(W.SEED)
    days, idx = day_index()
    T = len(days)
    doy = np.array([d.timetuple().tm_yday for d in days])
    wd = np.array([d.weekday() for d in days])
    yrs = np.array([(d - W.START).days / 365.0 for d in days])
    # active jobseekers receiving alerts (the pilot pool excluded), January peak, slow growth
    N = W.ACTIVE_BASE * (1 + 0.09 * np.cos(2 * np.pi * (doy - 12) / 365)) * (1 + 0.035 * yrs)
    N = np.round(N[:, None] * np.array(W.ACTIVE_SHARE)[None, :] * (1 + 0.004 * np.sin(np.arange(P) + 1))[None, :])
    # per-capita clicking holds steady; the seasons move how many jobseekers are active, not how they click
    seas = np.ones(len(days))
    prop = np.array(W.PROPENSITY)
    wa = np.array(W.WEEKDAY_ALERT)[wd]
    ws = np.array(W.WEEKDAY_SITE)[wd]
    app_growth = 1 + 0.18 * np.minimum(yrs, 1.0)    # the app's share grew through 2025 and then held
    jt = junk_matrix(days, idx)
    lam_alert0 = N * W.ALERT_RATE * prop[None, :] * wa[:, None] * seas[:, None]
    lost = lam_alert0 * jt
    lam_alert = lam_alert0 - lost
    lam_site0 = N * W.SITE_RATE * prop[None, :] * ws[:, None] * seas[:, None]
    lam_app0 = N * W.APP_RATE * prop[None, :] * ws[:, None] * seas[:, None] * app_growth[:, None]
    split = lam_site0 / (lam_site0 + lam_app0)
    lam_site = lam_site0 + W.SUBSTITUTION * lost * split
    lam_app = lam_app0 + W.SUBSTITUTION * lost * (1 - split)
    active = {
        "jobseekers": N.astype(int),
        "alert": rng.poisson(lam_alert),
        "website": rng.poisson(lam_site),
        "app": rng.poisson(lam_app),
        "lost_truth": float(((1 - W.SUBSTITUTION) * lost).sum()),
        "lost_alert_truth": float(lost.sum()),
    }
    pool = simulate_pool(rng, days, idx, jt, prop, wa, ws)
    return {"days": days, "idx": idx, "jt": jt, "active": active, "pool": pool, "wd": wd}


def simulate_pool(rng, days, idx, jt, prop, wa, ws):
    T = len(days)
    t0 = idx[W.POOL_DATE]
    n = W.POOL_SIZE
    prov = rng.choice(P, size=n, p=np.array(W.POOL_SHARE) / sum(W.POOL_SHARE))
    held = rng.random(n) < W.HOLDOUT
    dead = rng.random(n) < W.DEAD_SHARE
    gw_p = np.array([W.GATEWAY_SHARE.get(p, 0.0) for p in W.PROVIDERS])
    gateway = rng.random(n) < gw_p[prov]
    human_mult = np.where(gateway, 0.35, 1.0)     # gateway addresses are mostly mailboxes nobody reads any more
    acct = rng.choice(np.arange(10_000_000, 99_999_999), size=n, replace=False)
    has_app = rng.random(n) < 0.58
    restored = np.zeros(n, bool)
    scanner_spell = np.zeros(n, bool)
    spell_start = np.full(n, -1)
    last_click = np.full(n, -10 ** 6)
    app_seen = np.zeros(n, bool)
    pending = {}
    restarts = []          # (member, day, minute_of_day, route, send_k, scanner)
    scans = []             # (member, send_k, minute after delivery)
    email_clicks = []      # (member, send_k, minutes after delivery, link)
    repauses = []          # (member, day)
    cm, ct, cch, cli = [], [], [], []
    send_days = [idx[s] for s in W.SENDS]
    self_p = 1 - (1 - W.SELF_RESTART_28) ** (1 / 28.0)
    deliver = rng.integers(0, 32, size=n)          # minutes after 10:00 that each address's email is delivered
    for t in range(t0, T):
        due = restored & (t - np.maximum(spell_start, last_click) >= W.REPAUSE_DAYS)
        for m in np.where(due)[0]:
            repauses.append((int(m), t))
        restored[due] = False
        scanner_spell[due] = False
        if t in send_days:
            k = send_days.index(t)
            mailed = (~held) & (~dead) & (~restored)
            pend = np.zeros(n, bool)
            for lst in pending.values():
                for (m, _, _) in lst:
                    pend[m] = True
            mailed &= ~pend
            sc = mailed & gateway & (rng.random(n) < W.GATEWAY_SCAN_P)
            hu = mailed & (~sc) & (rng.random(n) < W.RESTART_P[k] * human_mult)
            for m in np.where(sc)[0]:
                lag = int(rng.choice([0, 0, 0, 1, 2, 4, 7, 11, 15])) if rng.random() > 0.12 else int(rng.integers(70, 380))
                scans.append((int(m), k, lag))
                restarts.append((int(m), t, 600 + int(deliver[m]) + lag, "email_link", k, True))
            restored[sc] = True
            scanner_spell[sc] = True
            spell_start[sc] = t
            fast = rng.random(n) < 0.16
            delay = np.where(fast, rng.uniform(0, 25, size=n), rng.exponential(1.6, size=n) * 1440)
            delay = np.minimum(delay, 26 * 1440).astype(int)
            for m in np.where(hu)[0]:
                mins = int(delay[m]) + 1
                tod = 600 + int(deliver[m]) + mins
                d = t + tod // 1440
                if d >= T:
                    continue
                email_clicks.append((int(m), k, mins, "restart"))
                if rng.random() < 0.22:
                    email_clicks.append((int(m), k, mins + int(rng.integers(1, 40)), "job"))
                pending.setdefault(d, []).append((int(m), k, tod % 1440))
            look = mailed & (~sc) & (~hu) & (rng.random(n) < 0.004)
            for m in np.where(look)[0]:
                email_clicks.append((int(m), k, int(rng.integers(3, 4000)), "job"))
        for (m, k, tod) in pending.pop(t, []):
            if restored[m]:
                continue
            restarts.append((m, t, tod, "email_link", k, False))
            restored[m] = True
            scanner_spell[m] = False
            spell_start[m] = t
        cand = (~restored) & (~dead) & (rng.random(n) < self_p * human_mult)
        for m in np.where(cand)[0]:
            route = "app" if (has_app[m] and rng.random() < 0.5) else "website"
            restarts.append((int(m), t, int(rng.integers(420, 1380)), route, -1, False))
            if route == "app":
                app_seen[m] = True
        restored[cand] = True
        scanner_spell[cand] = False
        spell_start[cand] = t
        act = np.where(restored & (~scanner_spell))[0]
        if act.size:
            p = prov[act]
            base = W.RESTORED_RATE * prop[p]
            la = base * 0.5 * wa[t] * (1 - jt[t, p])
            lo = base * 0.5 * ws[t] + base * 0.5 * wa[t] * jt[t, p] * W.SUBSTITUTION
            na = rng.poisson(la)
            no = rng.poisson(lo)
            for m, c in zip(act[na > 0], na[na > 0]):
                for _ in range(int(c)):
                    cm.append(int(m)); ct.append(t); cch.append(0); cli.append(True)
            for m, c in zip(act[no > 0], no[no > 0]):
                for _ in range(int(c)):
                    if has_app[m] and rng.random() < 0.5:
                        li = rng.random() >= W.LOGGED_OUT_APP
                        cm.append(int(m)); ct.append(t); cch.append(2); cli.append(li)
                    else:
                        cm.append(int(m)); ct.append(t); cch.append(1); cli.append(True)
            hit = (na + no) > 0
            last_click[act[hit]] = t
    cm, ct, cch, cli = np.array(cm), np.array(ct), np.array(cch), np.array(cli)
    # an app user logs in at least once: where every app click of a member was logged out, the last one was not
    app = np.where(cch == 2)[0]
    last_app = {}
    any_in = set()
    for i in app:
        last_app[int(cm[i])] = i
        if cli[i]:
            any_in.add(int(cm[i]))
    for m, i in last_app.items():
        if m not in any_in:
            cli[i] = True
    clicks = {"m": cm, "t": ct, "ch": cch, "li": cli}
    return {"n": n, "prov": prov, "held": held, "dead": dead, "gateway": gateway, "acct": acct, "has_app": has_app,
            "deliver": deliver, "restarts": restarts, "scans": scans, "email_clicks": email_clicks,
            "repauses": repauses, "clicks": clicks, "t0": t0, "send_days": send_days}
