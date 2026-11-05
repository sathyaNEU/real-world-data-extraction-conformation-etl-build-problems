"""Ask record systems (sorter stoppages; damage claims), their clean truth and the golden ask figures."""
import datetime as dt
import numpy as np
import pandas as pd
from world import HUBS, HUB_KEYS, UTC_OFFSET_H

HUB_NO = {h[0]: h[1] for h in HUBS}
CS_HUB = {"ZAZ": "ZARAGOZA", "VLC": "VALENCIA", "SVQ": "SEVILLA", "MAD": "MADRID", "BCN": "BARCELONA", "BIO": "BILBAO"}
CUTOFF_PAID = dt.date(2026, 10, 20)


def stoppages(days, seed):
    """Truth: one row per stoppage. Records: the sorter's event log (two controllers, gaps) and work orders."""
    r = np.random.default_rng(seed + 20)
    rate = {"ZAZ": 2.6, "VLC": 2.9, "SVQ": 3.3, "MAD": 3.8, "BCN": 3.4, "BIO": 2.4}
    truth, ev, wo, gaps = [], [], [], []
    wo_seq = int(r.integers(310000, 330000))
    for h in HUB_KEYS:
        line = "S1"
        for d in days:
            night0 = dt.datetime.combine(d, dt.time(20, 50))
            k = int(r.poisson(rate[h]))
            starts = np.sort(r.uniform(0, 7.3 * 3600, k))
            last_end = -1
            for s in starts:
                if s < last_end + 120:
                    continue
                dur = float(np.clip(r.lognormal(np.log(420), 0.95), 45, 3 * 3600))
                safety = r.random() < 0.34
                t0 = night0 + dt.timedelta(seconds=int(s)); t1 = t0 + dt.timedelta(seconds=int(dur))
                last_end = s + dur
                truth.append((h, d, t0, t1, dur / 3600.0, safety))
            # heartbeat gaps: the event logger loses its link to the historian on a few nights
        n_gap = int(r.integers(3, 6))
        gd = r.choice(len(days), n_gap, replace=False)
        for gi in gd:
            d = days[int(gi)]
            g0 = dt.datetime.combine(d, dt.time(21, 30)) + dt.timedelta(minutes=int(r.integers(0, 240)))
            g1 = g0 + dt.timedelta(minutes=int(r.integers(70, 200)))
            gaps.append((h, g0, g1))
    st = pd.DataFrame(truth, columns=["hub", "night", "t0", "t1", "hours", "safety"])
    gp = pd.DataFrame(gaps, columns=["hub", "g0", "g1"])
    # make sure every gap holds at least one stoppage (the engineer is called to the stopped sorter)
    extra = []
    for g in gp.itertuples():
        inside = st[(st.hub == g.hub) & (st.t0 >= g.g0) & (st.t1 <= g.g1)]
        if len(inside) == 0:
            t0 = g.g0 + dt.timedelta(minutes=int(r.integers(8, 30)))
            dur = float(r.uniform(900, 2400))
            t1 = t0 + dt.timedelta(seconds=int(dur))
            if t1 < g.g1:
                extra.append((g.hub, t0.date() if t0.hour >= 12 else t0.date() - dt.timedelta(days=1), t0, t1, dur / 3600, False))
    if extra:
        st = pd.concat([st, pd.DataFrame(extra, columns=st.columns)]).reset_index(drop=True)
    # drop truth stoppages that straddle a gap edge (keeps the records unambiguous)
    keep = []
    for s in st.itertuples():
        bad = gp[(gp.hub == s.hub) & (((s.t0 < gp.g0) & (s.t1 > gp.g0)) | ((s.t0 < gp.g1) & (s.t1 > gp.g1)))]
        keep.append(len(bad) == 0)
    st = st[np.array(keep)].sort_values(["hub", "t0"]).reset_index(drop=True)
    for s in st.itertuples():
        in_gap = len(gp[(gp.hub == s.hub) & (s.t0 >= gp.g0) & (s.t1 <= gp.g1)]) > 0
        reason = r.choice(["JAM", "JAM", "EMPTY_TRAY", "OVERLOAD", "MANUAL", "E-STOP", "LIGHT_CURTAIN"]) if not s.safety \
            else r.choice(["E-STOP", "LIGHT_CURTAIN", "GATE_OPEN"])
        if not in_gap:
            u0 = s.t0 - dt.timedelta(hours=UTC_OFFSET_H); u1 = s.t1 - dt.timedelta(hours=UTC_OFFSET_H)
            ev.append((HUB_NO[s.hub], "S1", "PLC", "STOP", u0, reason))
            ev.append((HUB_NO[s.hub], "S1", "PLC", "RUN", u1, ""))
            if s.safety:
                ev.append((HUB_NO[s.hub], "S1", "SAF", "STOP", u0 + dt.timedelta(seconds=int(r.integers(1, 4))), reason))
                ev.append((HUB_NO[s.hub], "S1", "SAF", "RUN", u1 - dt.timedelta(seconds=int(r.integers(1, 4))), ""))
        call_eng = in_gap or (s.hours > 0.33 and r.random() < 0.55) or r.random() < 0.08
        if call_eng:
            wo_seq += int(r.integers(1, 7))
            wo.append(("WO%d" % wo_seq, s.hub, s.t0 + dt.timedelta(minutes=int(r.integers(0, 4))),
                       s.t1 + dt.timedelta(minutes=int(r.integers(0, 6))), s.t0, s.t1,
                       str(r.choice(["induction belt", "merge 2", "tilt tray drive", "chute 14 gate", "scanner arch",
                                     "light curtain", "e-stop circuit", "PLC card"])),
                       str(r.choice(["cleared jam", "reset and tested", "replaced sensor", "adjusted belt tension",
                                     "replaced fuse", "re-seated connector"]))))
    # heartbeats every 15 minutes through each sorting night, absent inside the gaps
    hb = []
    for h in HUB_KEYS:
        gh = gp[gp.hub == h]
        for d in days:
            t = dt.datetime.combine(d, dt.time(20, 45))
            while t <= dt.datetime.combine(d + dt.timedelta(days=1), dt.time(4, 45)):
                if not ((gh.g0 <= t) & (gh.g1 >= t)).any():
                    hb.append((HUB_NO[h], "S1", "PLC", "HEARTBEAT", t - dt.timedelta(hours=UTC_OFFSET_H), ""))
                t += dt.timedelta(minutes=15)
    events = pd.DataFrame(ev + hb, columns=["hub_no", "line", "controller", "event", "ts_utc", "reason"])
    events = events.sort_values(["hub_no", "ts_utc", "controller", "event"]).reset_index(drop=True)
    wos = pd.DataFrame(wo, columns=["work_order", "hub", "opened_local", "closed_local", "machine_stopped_local",
                                    "machine_running_local", "asset", "action"])
    return st, events, wos, gp


def claims(days, seed):
    """Truth: one row per damaged parcel with a claim. Records: the customer-service export and finance payments."""
    r = np.random.default_rng(seed + 30)
    vol = {"ZAZ": 1180, "VLC": 1420, "SVQ": 1310, "MAD": 2650, "BCN": 2390, "BIO": 980}
    rows, used = [], set()
    for h in HUB_KEYS:
        n = int(r.poisson(vol[h]))
        for _ in range(n):
            while True:
                bc = "BQ%02d%08d%02d" % (int(r.integers(10, 99)), int(r.integers(0, 10 ** 8)), int(r.integers(0, 100)))
                if bc not in used:
                    used.add(bc)
                    break
            night = days[int(r.integers(0, len(days)))]
            national = r.random() < 0.36
            dest = h if not national else str(r.choice([x for x in HUB_KEYS if x != h]))
            first_eur = float(np.round(np.clip(r.lognormal(np.log(26), 0.8), 4.5, 450), 2))
            opened = night + dt.timedelta(days=int(r.integers(2, 16)))
            decided = opened + dt.timedelta(days=int(r.integers(3, 22)))
            paid = decided + dt.timedelta(days=int(r.integers(1, 9)))
            reopen = r.random() < 0.11
            top = float(np.round(first_eur * r.uniform(0.3, 1.6), 2)) if reopen else 0.0
            ro_dec = decided + dt.timedelta(days=int(r.integers(10, 35))) if reopen else None
            ro_paid = ro_dec + dt.timedelta(days=int(r.integers(1, 9))) if reopen else None
            rows.append((bc, h, dest, night, national, opened, decided, paid, first_eur, reopen, top, ro_dec, ro_paid))
    t = pd.DataFrame(rows, columns=["barcode", "sort_hub", "dest_hub", "night", "national", "opened", "decided", "paid",
                                    "first_eur", "reopen", "top_eur", "ro_decided", "ro_paid"])
    # customer-service export (pulled 23 October): one row per claim reference; reopened claims get a new reference
    cs, pay = [], []
    ref = int(r.integers(7100000, 7200000))
    pref = int(r.integers(880000, 900000))
    for c in t.itertuples():
        if c.opened > dt.date(2026, 10, 23):
            continue
        ref += int(r.integers(1, 5))
        status = "APPROVED" if c.decided <= dt.date(2026, 10, 23) else "OPEN"
        cs.append(("RC%d" % ref, c.barcode, CS_HUB[c.dest_hub], c.opened.isoformat(), status,
                   c.decided.isoformat() if status == "APPROVED" else "", c.first_eur if status == "APPROVED" else None))
        if status == "APPROVED" and c.paid <= dt.date(2026, 10, 23):
            pref += int(r.integers(1, 4))
            pay.append(("PY%d" % pref, "RC%d" % ref, c.paid.isoformat(), c.first_eur))
        if c.reopen and c.ro_decided <= dt.date(2026, 10, 23):
            ref += int(r.integers(1, 5))
            cs.append(("RC%d" % ref, c.barcode, CS_HUB[c.dest_hub], c.ro_decided.isoformat(), "APPROVED",
                       c.ro_decided.isoformat(), round(c.first_eur + c.top_eur, 2)))
            if c.ro_paid <= dt.date(2026, 10, 23):
                pref += int(r.integers(1, 4))
                pay.append(("PY%d" % pref, "RC%d" % ref, c.ro_paid.isoformat(), c.top_eur))
    cs = pd.DataFrame(cs, columns=["claim_ref", "tracking_no", "hub", "opened", "status", "decided", "approved_eur"])
    pay = pd.DataFrame(pay, columns=["payment_ref", "claim_ref", "paid_date", "amount_eur"])
    # tracking history for claimed parcels: the sort scan at the hub the night it was collected, then the destination
    tr = []
    for c in t.itertuples():
        t0 = dt.datetime.combine(c.night, dt.time(21, 0)) + dt.timedelta(minutes=int(r.integers(0, 400)))
        tr.append((c.barcode, "SORT", HUB_NO[c.sort_hub], t0 - dt.timedelta(hours=UTC_OFFSET_H)))
        if c.national:
            t1 = t0 + dt.timedelta(hours=int(r.integers(20, 26)))
            tr.append((c.barcode, "SORT", HUB_NO[c.dest_hub], t1 - dt.timedelta(hours=UTC_OFFSET_H)))
        t2 = t0 + dt.timedelta(hours=int(r.integers(30, 55)))
        tr.append((c.barcode, "DELIVERED", 0, t2 - dt.timedelta(hours=UTC_OFFSET_H)))
    trk = pd.DataFrame(tr, columns=["tracking_no", "event", "hub_no", "ts_utc"]).sort_values(["tracking_no", "ts_utc"])
    return t, cs, pay, trk


def ask_golden(st, t):
    out = {}
    # stoppages: every truth stoppage on the nights of July to September
    g = st.groupby("hub")
    out["stoppages"] = g.size().reindex(HUB_KEYS).astype(int)
    out["hours_stood"] = g.hours.sum().reindex(HUB_KEYS)
    # claims: damaged parcels paid by 20 October, charged to the hub that sorted them the night they were collected
    paid1 = t.paid <= CUTOFF_PAID
    paid2 = t.reopen & t.ro_paid.notna() & (t.ro_paid.apply(lambda x: x is not None and x <= CUTOFF_PAID))
    eur = np.where(paid1, t.first_eur, 0.0) + np.where(paid2, t.top_eur, 0.0)
    t2 = t.assign(eur=eur, any_paid=paid1 | paid2)
    gg = t2[t2.any_paid].groupby("sort_hub")
    out["claims"] = gg.size().reindex(HUB_KEYS).astype(int)
    out["claims_eur"] = gg.eur.sum().reindex(HUB_KEYS).round(2)
    return pd.DataFrame(out)
