"""task464 architecture 12: every graded figure, recomputed from the files under target/ alone.

    python3 generator/answers.py            # prints the figures and writes generator/figures.json

The main call: the restart series' effect on the sponsored clicks Quaywork takes, over the pilot's six 28-day
windows, is the holdout uplift among the pool less the clicks the rest of the board lost while the mailbox providers
filed its mail as junk after each send (read by mailbox group against the send dates, against the groups that never
filed it, net of the clicks those jobseekers made on the site and app instead). The 2027 series is sized at what one
pilot send did on average, thirteen times. The asks: each send's restarts by people, and how many of them clicked a
sponsored job on the send's date or in the 27 days after it, whether before or after restarting.
"""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import world as W  # noqa: E402

GROUPS = ["gmail", "microsoft", "yahoo_aol", "apple", "bt", "sky", "virgin_media", "talktalk", "other"]
RS = ["RS-2604", "RS-2605", "RS-2606", "RS-2607", "RS-2608", "RS-2609"]
SENDS = list(W.SENDS)
D = dt.timedelta


def r_to(x, unit):
    return int(unit * round(float(x) / unit))


# ---------------------------------------------------------------------------------------------------------------
# the warehouse's daily sponsored clicks
# ---------------------------------------------------------------------------------------------------------------
class Warehouse:
    def __init__(self, tgt, dedupe=True):
        seen = set()
        self.clicks = defaultdict(float)       # (date, group, audience, channel3) -> clicks
        self.js = {}                           # (date, group, audience) -> jobseekers
        with open(os.path.join(tgt, "sponsored_clicks_by_mailbox_daily.csv"), newline="") as f:
            for r in csv.DictReader(f):
                key = tuple(r.values())
                if dedupe and key in seen:
                    continue                    # the warehouse reload of 3 to 5 May 2026 sent those days twice
                seen.add(key)
                d = dt.date.fromisoformat(r["click_date"])
                ch = "app" if r["channel"].startswith("app") else r["channel"]
                self.clicks[(d, r["mailbox_group"], r["audience"], ch)] += int(r["sponsored_clicks"])
                self.js[(d, r["mailbox_group"], r["audience"])] = int(r["jobseekers"])
        self.days = sorted({k[0] for k in self.js})

    def total(self, d, g, aud, channels=("alert_email", "website", "app")):
        return sum(self.clicks.get((d, g, aud, c), 0.0) for c in channels)

    def n(self, d, g, aud):
        return self.js.get((d, g, aud), 0)


def window_days(k, lo=0, hi=W.WINDOW):
    return [SENDS[k] + D(days=i) for i in range(lo, hi)]


def pilot_days():
    return [d for k in range(6) for d in window_days(k)]


def uplift(wh, stratified=False):
    """The holdout uplift: the mailed arm's sponsored clicks per member over the six windows less the holdout's, times
    the mailed arm."""
    days = pilot_days()
    if not stratified:
        cm = sum(wh.total(d, g, "restart_pilot_mailed") for d in days for g in GROUPS)
        ch = sum(wh.total(d, g, "restart_pilot_holdout") for d in days for g in GROUPS)
        nm = sum(wh.n(SENDS[0], g, "restart_pilot_mailed") for g in GROUPS)
        nh = sum(wh.n(SENDS[0], g, "restart_pilot_holdout") for g in GROUPS)
        return (cm / nm - ch / nh) * nm
    u = 0.0
    for g in GROUPS:
        cm = sum(wh.total(d, g, "restart_pilot_mailed") for d in days)
        ch = sum(wh.total(d, g, "restart_pilot_holdout") for d in days)
        nm, nh = wh.n(SENDS[0], g, "restart_pilot_mailed"), wh.n(SENDS[0], g, "restart_pilot_holdout")
        u += (cm / nm - ch / nh) * nm
    return u


def rate(wh, d, g, channels=("alert_email", "website", "app")):
    n = wh.n(d, g, "alerts_on")
    return wh.total(d, g, "alerts_on", channels) / n if n else None


def pooled_rate(wh, d, groups, channels=("alert_email", "website", "app")):
    c = sum(wh.total(d, g, "alerts_on", channels) for g in groups)
    n = sum(wh.n(d, g, "alerts_on") for g in groups)
    return c / n if n else None


def group_dip(wh, g, controls, channels=("alert_email", "website", "app"), mode="event"):
    """The sponsored clicks group g's active jobseekers lost to each send, against the control groups' same days.

    mode 'event': days 0 to 13 after each send, the group's ratio to the controls read on days 14 to 27 of the same
    window; 'full': all 28 days, the ratio read on the 14 weeks before the first send; 'its': days 0 to 13 against
    the group's own same-weekday rate in the 14 days before the send."""
    out = []
    for k in range(6):
        ev = window_days(k, 0, 14)
        if mode == "its":
            prev = [SENDS[k] - D(days=i) for i in range(1, 15)]
            loss = 0.0
            for d in ev:
                same = [x for x in prev if x.weekday() == d.weekday() and rate(wh, x, g, channels) is not None]
                cf = sum(rate(wh, x, g, channels) for x in same) / len(same)
                loss += (cf - rate(wh, d, g, channels)) * wh.n(d, g, "alerts_on")
            out.append(loss)
            continue
        if mode == "event":
            ref = window_days(k, 14, 28)
            evd = ev
        else:
            ref = [SENDS[0] - D(days=i) for i in range(1, 99)]
            evd = window_days(k)
        ref = [d for d in ref if wh.n(d, g, "alerts_on")]
        num = sum(wh.total(d, g, "alerts_on", channels) for d in ref) / sum(wh.n(d, g, "alerts_on") for d in ref)
        den = sum(sum(wh.total(d, c, "alerts_on", channels) for c in controls) for d in ref) / \
            sum(sum(wh.n(d, c, "alerts_on") for c in controls) for d in ref)
        ratio = num / den
        loss = 0.0
        for d in evd:
            loss += (pooled_rate(wh, d, controls, channels) * ratio - rate(wh, d, g, channels)) * wh.n(d, g, "alerts_on")
        out.append(loss)
    return out


def affected_groups(wh):
    """The groups whose active jobseekers dip after the sends: each group's sponsored clicks per jobseeker over days 0 to
    13 after each send against its own same-weekday rate in the 14 days before; a group whose mail was never filed
    reads within noise of zero, a filing group falls after every send."""
    res = {}
    for g in GROUPS:
        loss = sum(group_dip(wh, g, None, mode="its"))
        base = sum(wh.total(d, g, "alerts_on") for k in range(6) for d in window_days(k, 0, 14))
        res[g] = loss / base
    aff = [g for g in GROUPS if res[g] > 0.01]
    return aff, res


def damage(wh, mode="event", channels=("alert_email", "website", "app"), controls=None):
    aff, _ = affected_groups(wh)
    ctl = controls or [g for g in GROUPS if g not in aff]
    per = {g: group_dip(wh, g, ctl, channels, mode) for g in aff}
    return per, aff, ctl


# ---------------------------------------------------------------------------------------------------------------
# the asks: the restart log, Postvane's click events and the CRM's pull of restarted jobseekers' clicks
# ---------------------------------------------------------------------------------------------------------------
def restart_rows(tgt):
    with open(os.path.join(tgt, "alert_restarts_pilot_pool_2026.csv"), newline="") as f:
        return list(csv.DictReader(f))


def burst_keys(tgt, links_min=4, seconds=10):
    """(campaign, subscriber) pairs whose restart email had nearly every link clicked inside a few seconds."""
    ev = defaultdict(list)
    with open(os.path.join(tgt, "postvane_clicks_restart_series_2026.csv"), newline="") as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["clicked_at_utc"][:19], "%Y-%m-%dT%H:%M:%S")
            ev[(r["campaign_code"], r["subscriber_key"])].append((t, r["link_name"]))
    out = set()
    for key, lst in ev.items():
        lst.sort()
        for i in range(len(lst)):
            j = i
            links = set()
            while j < len(lst) and (lst[j][0] - lst[i][0]).total_seconds() <= seconds:
                links.add(lst[j][1])
                j += 1
            if len(links) >= links_min:
                out.add(key)
                break
    return out, ev


def restarts_by_send(tgt, handling="golden", seconds_after_delivery=None):
    rows = restart_rows(tgt)
    bursts, ev = burst_keys(tgt)
    per = [set() for _ in range(6)]
    for r in rows:
        if r["route"] != "email_link" or r["link_campaign"] not in RS:
            continue
        k = RS.index(r["link_campaign"])
        key = (r["link_campaign"], r["account_id"])
        if handling == "golden" and key in bursts:
            continue
        if handling == "fast" and seconds_after_delivery is not None:
            # the over-cleaning reading: any restart click within a set time of the send's first delivery
            first = ev.get(key)
            if first:
                rt = [t for (t, l) in first if l == "restart_alerts"]
                t0 = dt.datetime(SENDS[k].year, SENDS[k].month, SENDS[k].day, 9, 0)
                if rt and (min(rt) - t0).total_seconds() <= seconds_after_delivery:
                    continue
        per[k].add(r["account_id"])
    return per


def clicked_within(tgt, per, stitch=True):
    """Of each send's restarters, how many made a sponsored click, before or after restarting, on the send's date or
    in the 27 days after it (UK dates, as the pull's clicked_at_uk carries them)."""
    dev2acct = defaultdict(set)
    rows = []
    with open(os.path.join(tgt, "restarted_jobseekers_sponsored_clicks.csv"), newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
            if r["account_id"] and r["app_install_id"]:
                dev2acct[r["app_install_id"]].add(r["account_id"])
    for r in restart_rows(tgt):
        if r["app_install_id"]:
            dev2acct[r["app_install_id"]].add(r["account_id"])
    days_by_acct = defaultdict(set)
    for r in rows:
        acct = r["account_id"]
        if not acct and stitch and r["app_install_id"] and len(dev2acct.get(r["app_install_id"], ())) == 1:
            acct = next(iter(dev2acct[r["app_install_id"]]))
        if acct:
            days_by_acct[acct].add(dt.date.fromisoformat(r["clicked_at_uk"][:10]))
    out = []
    for k in range(6):
        lo, hi = SENDS[k], SENDS[k] + D(days=W.WINDOW - 1)
        out.append(sum(1 for a in per[k] if any(lo <= d <= hi for d in days_by_acct.get(a, ()))))
    return out


# ---------------------------------------------------------------------------------------------------------------
def figures(write=False, tgt=None):
    tgt = tgt or os.path.join(BASE, "target")
    wh = Warehouse(tgt)
    U = uplift(wh)
    per, aff, ctl = damage(wh, "event")
    Dg = {g: sum(v) for g, v in per.items()}
    Dt = sum(Dg.values())
    net = U - Dt
    f27 = net * W.SENDS_2027 / 6.0
    per_send_net = [U / 6.0 - sum(per[g][k] for g in aff) for k in range(6)]
    a1 = restarts_by_send(tgt, "golden")
    a2 = clicked_within(tgt, a1, stitch=True)
    logged = [len(s) for s in restarts_by_send(tgt, "plain")]
    days = pilot_days()
    nm = sum(wh.n(SENDS[0], g, "restart_pilot_mailed") for g in GROUPS)
    nh = sum(wh.n(SENDS[0], g, "restart_pilot_holdout") for g in GROUPS)
    cm = sum(wh.total(d, g, "restart_pilot_mailed") for d in days for g in GROUPS)
    ch = sum(wh.total(d, g, "restart_pilot_holdout") for d in days for g in GROUPS)
    fig = {
        "call": "drop",
        "series_2027_clicks": r_to(f27, 100000),
        "series_2027_clicks_exact": round(f27, 1),
        "pilot_net_clicks": r_to(net, 50000),
        "pilot_net_exact": round(net, 1),
        "pilot_uplift_clicks": r_to(U, 50000),
        "pilot_uplift_exact": round(U, 1),
        "pilot_loss_clicks": r_to(Dt, 50000),
        "pilot_loss_exact": round(Dt, 1),
        "affected_groups": aff,
        "control_groups": ctl,
        "loss_by_group_exact": {g: round(v, 1) for g, v in Dg.items()},
        "per_send_net_exact": [round(x, 1) for x in per_send_net],
        "default_2027_clicks": r_to(U * W.SENDS_2027 / 6.0, 100000),
        "default_2027_exact": round(U * W.SENDS_2027 / 6.0, 1),
        "restarted_by_people": [len(s) for s in a1],
        "clicked_within_28_days": a2,
        "restarts_logged_from_links": logged,
        "gateway_restarts_removed": sum(logged) - sum(len(s) for s in a1),
        "restarts_logged_total": sum(logged),
        "mailed_arm": nm,
        "holdout_arm": nh,
        "mailed_clicks_per_jobseeker": round(cm / nm, 3),
        "holdout_clicks_per_jobseeker": round(ch / nh, 3),
        "pilot_uplift_int": int(round(U)),
        "pilot_loss_int": int(round(Dt)),
        "pilot_net_int": int(round(net)),
        "per_send_net_int": int(round(net / 6.0)),
        "series_2027_int": int(round(f27)),
        "loss_by_group_int": {g: int(round(v)) for g, v in Dg.items()},
        "sends_2027": W.SENDS_2027,
        "window_days": W.WINDOW,
        "burst_rule": {"links": 4, "seconds": 10},
        "event_days": [0, 13, 14, 27],
        "series_2027_cost_clicks": -r_to(f27, 100000),
    }
    if write:
        json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=2)
    return fig


if __name__ == "__main__":
    f = figures(write=True)
    for k, v in f.items():
        print(k, v)
