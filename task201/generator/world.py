"""task201: the operator's world, built forward from params.py. Deterministic.

Nothing here knows about the ladder. build.py writes the pack from these frames; drill.py computes
every rung from the shipped columns only.
"""
import numpy as np, pandas as pd
import params as P

HOUR = np.timedelta64(1, "h")
# Poland leaves summer time at 03:00 local on 25 October 2026, so the operational record (local wall
# clock) stands two hours ahead of UTC before that instant and one hour ahead after it. The SCADA
# historian keeps UTC, the dispatch system keeps local time, and the archive is written from the
# local instant with the offset that applied to it.
DST_END_LOCAL = np.datetime64("2026-10-25T03:00")


def utc_offset_hours(local_naive):
    """Hours the local wall clock stands ahead of UTC, per Europe/Warsaw, for this window."""
    return np.where(np.asarray(local_naive, dtype="datetime64[m]") < DST_END_LOCAL, 2, 1)


def _loguniform(rng, lo, hi, n):
    return np.exp(rng.uniform(np.log(lo), np.log(hi), n))


def build_world(seed=P.SEED):
    rng = np.random.default_rng(seed)
    t0 = np.datetime64(P.WIN_FROM + "T00:00"); t1 = np.datetime64(P.WIN_TO + "T23:59")
    span_h = (t1 - t0) / HOUR

    # ---------------------------------------------------------------- feeders and devices
    feeders, devices = [], []
    for br, prof in P.DISTRICT_PROFILE.items():
        bp = P.BRANCH[br]
        for di, (dist, w, inst_share, mixmul, fixmul) in enumerate(prof):
            nf = max(4, int(round(bp["feeders"] * w)))
            for fi in range(nf):
                stn = 100 + len(feeders) * 3 + rng.integers(0, 3)
                fid = "%s-%02d-%02d" % (br, di + 1, fi + 1)
                instr = rng.random() < inst_share
                feeders.append(dict(feeder_id=fid, oddzial=br, rejon=dist, stacja_gpz="GPZ-%04d" % stn,
                                    telemetria_linii=bool(instr)))
                for ci, cls in enumerate(P.CLS):
                    ndev = [1, 4, 9, 7][ci]
                    lo, hi = bp["cust"][ci]
                    cu = _loguniform(rng, lo, hi, ndev)
                    for k in range(ndev):
                        devices.append(dict(
                            urzadzenie_id="%s/%s/%02d" % (fid, ["M", "S", "O", "N"][ci], k + 1),
                            feeder_id=fid, oddzial=br, rejon=dist, klasa_odcinka=cls,
                            odbiorcy_za_urzadzeniem=int(max(1, round(cu[k]))),
                            telemetria_linii=bool(instr)))
    fd = pd.DataFrame(feeders); dv = pd.DataFrame(devices)

    # ---------------------------------------------------------------- events
    rows = []
    for br, bp in P.BRANCH.items():
        prof = P.DISTRICT_PROFILE[br]
        dw = np.array([x[1] for x in prof]); dw = dw / dw.sum()
        n = bp["n_ev"]
        di = rng.choice(len(prof), size=n, p=dw)
        # class draw uses the district's own multiplier on the branch mix
        base = np.array(bp["mix"])
        ci = np.empty(n, dtype=int)
        for j in range(len(prof)):
            m = base * np.array(prof[j][3]); m = m / m.sum()
            sel = di == j
            ci[sel] = rng.choice(4, size=int(sel.sum()), p=m)
        # which episode each event belongs to
        shares = [e[3] for e in P.EPISODES]
        ep = np.full(n, -1)
        for k, (nm, s, e, sh, bw) in enumerate(P.EPISODES):
            ep = np.where((ep < 0) & (rng.random(n) < sh * bw[br] / (1 - sum(shares[:k]) + 1e-9)), k, ep)
        idx = {}
        for key, sub in dv.groupby(["oddzial", "rejon", "klasa_odcinka"], sort=True):
            idx[key] = sub.reset_index(drop=True)
        for i in range(n):
            dist = prof[di[i]][0]
            cand = idx[(br, dist, P.CLS[ci[i]])]
            d = cand.iloc[int(rng.integers(0, len(cand)))]
            if ep[i] >= 0:
                nm, s, e, sh, bw = P.EPISODES[ep[i]]
                a, z = np.datetime64(s), np.datetime64(e)
                start = a + np.timedelta64(int(rng.uniform(0, (z - a) / np.timedelta64(1, "m"))), "m")
            else:
                start = t0 + np.timedelta64(int(rng.uniform(0, span_h * 60)), "m")
            cls = P.CLS[ci[i]]
            dly = P.DELAY_MIN[cls] / 0.901168 * rng.weibull(P.WEIBULL_SHAPE)              # minutes
            fix = max(5.0, rng.gamma(3.4, bp["fix"][ci[i]] * prof[di[i]][4] * 60.0 / 3.4))
            tele = (cls == "SN-magistrala") or bool(d.telemetria_linii)
            rows.append(dict(oddzial=br, rejon=dist, feeder_id=d.feeder_id,
                             urzadzenie_id=d.urzadzenie_id, klasa_odcinka=cls,
                             odbiorcy=int(d.odbiorcy_za_urzadzeniem), telemetrowane=tele,
                             epizod=("" if ep[i] < 0 else P.EPISODES[ep[i]][0]),
                             t_utrata=start, zwloka_min=dly, naprawa_min=fix))
    ev = pd.DataFrame(rows).sort_values("t_utrata").reset_index(drop=True)
    ev["zdarzenie_id"] = ["AW-2026-%06d" % (4100 + 7 * i) for i in range(len(ev))]
    ev["t_zgloszenie"] = ev.t_utrata + pd.to_timedelta(ev.zwloka_min, unit="m")
    ev["t_zalaczenie"] = ev.t_zgloszenie + pd.to_timedelta(ev.naprawa_min, unit="m")
    # the dispatch system's recorded start: the line device's own signal where the feeder reports
    # one, otherwise the first customer notification
    ev["t_poczatek_oms"] = np.where(ev.telemetrowane, ev.t_utrata, ev.t_zgloszenie)
    ev["t_poczatek_oms"] = pd.to_datetime(ev.t_poczatek_oms)
    # a handful of interruptions were still not restored when the extract was taken
    cut = np.datetime64(P.ASOF + "T06:00")
    rng2 = np.random.default_rng(seed + 5)
    late = ev.index[(ev.t_utrata > np.datetime64("2026-11-13T12:00")) & (rng2.random(len(ev)) < 0.004)]
    ev["nieusunieta"] = False
    ev.loc[late, "nieusunieta"] = True
    ev.loc[late, "t_zalaczenie"] = pd.NaT
    ev = ev[ev.t_zalaczenie.isna() | (ev.t_zalaczenie < cut)].reset_index(drop=True)
    ev["rodzaj"] = "awaryjne"
    pl = planned_work(dv, seed)
    ev = pd.concat([ev, pl], ignore_index=True).sort_values("t_utrata").reset_index(drop=True)
    ev["zdarzenie_id"] = ["AW-2026-%06d" % (4100 + 7 * i) for i in range(len(ev))]
    ev["t_zgloszenie"] = ev.t_utrata + pd.to_timedelta(ev.zwloka_min, unit="m")
    ev["t_zalaczenie"] = np.where(ev.nieusunieta, np.datetime64("NaT"),
                                  ev.t_zgloszenie + pd.to_timedelta(ev.naprawa_min, unit="m"))
    ev["t_zalaczenie"] = pd.to_datetime(ev.t_zalaczenie)
    # the dispatch system and the contact centre store whole minutes; the SCADA historian stores
    # seconds, so only the archive keeps them
    for c in ["t_zgloszenie", "t_zalaczenie"]:
        ev[c] = pd.to_datetime(ev[c]).dt.floor("min")
    ev["t_poczatek_oms"] = pd.to_datetime(np.where(ev.telemetrowane, ev.t_utrata, ev.t_zgloszenie))
    ev["t_poczatek_oms"] = ev.t_poczatek_oms.dt.floor("min")
    # a planned switching is notified by the schedule, so its recorded start is the real one
    ev.loc[ev.rodzaj == "planowane", "t_poczatek_oms"] = ev.loc[ev.rodzaj == "planowane", "t_utrata"]
    rng3 = np.random.default_rng(seed + 31)
    ev["klucz_bez_zer"] = rng3.random(len(ev)) < ev.oddzial.map(P.UNPADDED_SHARE).values
    # C1 on axes 3 and 9: nothing sits outside the window on the dispatch clock, so every reading of
    # the window selects the same rows
    lo = np.datetime64(P.WIN_FROM + "T00:00"); hi = np.datetime64(P.WIN_TO + "T23:59")
    ev = ev[(ev.t_poczatek_oms >= lo) & (ev.t_poczatek_oms <= hi)].reset_index(drop=True)
    return fd, dv, ev


def planned_work(dv, seed=P.SEED):
    """The autumn maintenance programme: whole sections switched out to a published schedule."""
    rng = np.random.default_rng(seed + 41)
    # The work order's scope, drawn per visit on its own stream so the programme's days, feeders and
    # durations do not move with it. The dispatcher copies a short form of it into the outage record.
    rngz = np.random.default_rng(seed + 57)
    w = np.array([P.PLANNED_SHARE[b] for b in P.BRANCH]); w = w / w.sum()
    brs = rng.choice(list(P.BRANCH), size=P.PLANNED_JOBS, p=w)
    rows = []
    pool = {b: dv[(dv.oddzial == b) & (dv.klasa_odcinka == "SN/nN-stacja")]
            .reset_index(drop=True) for b in P.BRANCH}
    byfeeder = {b: {f: g.reset_index(drop=True) for f, g in pool[b].groupby("feeder_id")}
                for b in P.BRANCH}
    used_days = set()
    for i, b in enumerate(brs):
        feeders = list(byfeeder[b])
        f = feeders[int(rng.integers(0, len(feeders)))]
        cand = byfeeder[b][f]
        # one visit switches out one, two or three sections of the same feeder in turn
        k = int(min(len(cand), rng.choice([1, 2, 3], p=[0.46, 0.34, 0.20])))
        picks = rng.choice(len(cand), size=k, replace=False)
        # one feeder is never scheduled twice on one day, so a published window identifies its job
        for _ in range(40):
            day = np.datetime64("2026-10-01") + np.timedelta64(int(rng.integers(0, 40)), "D")
            if (f, day) not in used_days:
                break
        used_days.add((f, day))
        zi = int(rngz.choice(len(P.PLANNED_SCOPE), p=P.PLANNED_SCOPE_W))
        zakres, przyczyna = P.PLANNED_SCOPE[zi]
        t = day + np.timedelta64(int(rng.integers(6, 10)), "h") + np.timedelta64(int(rng.integers(0, 55)), "m")
        for j, pi in enumerate(sorted(picks)):
            d = cand.iloc[int(pi)]
            dur = float(rng.uniform(*P.PLANNED_MIN))
            rows.append(dict(oddzial=b, rejon=d.rejon, feeder_id=d.feeder_id,
                             urzadzenie_id=d.urzadzenie_id, klasa_odcinka=d.klasa_odcinka,
                             odbiorcy=int(d.odbiorcy_za_urzadzeniem), telemetrowane=True,
                             epizod="", t_utrata=t, zwloka_min=0.0,
                             naprawa_min=dur, nieusunieta=False, rodzaj="planowane",
                             zakres_pracy=zakres, przyczyna_planowa=przyczyna))
            t = t + np.timedelta64(int(dur) + int(rng.integers(12, 45)), "m")
    return pd.DataFrame(rows)


def notification_log(ev, seed=P.SEED):
    """One row per customer notification. Only the first of an event's rows sets the OMS start."""
    rng = np.random.default_rng(seed + 11)
    k = np.minimum(34, np.maximum(1, rng.binomial(ev.odbiorcy.values, 0.18)))
    rep = np.repeat(np.arange(len(ev)), k)
    extra = np.abs(rng.gamma(1.6, 38.0, len(rep)))
    first_in_event = np.concatenate([[True], rep[1:] != rep[:-1]])
    extra[first_in_event] = 0.0
    # later notifications on one event arrive in order
    order = np.lexsort((extra, rep))
    extra = extra[order]
    base = ev.t_zgloszenie.values[rep]
    ts = pd.to_datetime(base + extra.astype("int64").astype("timedelta64[m]")).floor("min")
    ch = rng.random(len(rep)); ch2 = rng.random(len(rep))
    out = pd.DataFrame(dict(
        zgloszenie_id=["ZG26%08d" % (1700021 + 3 * i) for i in range(len(rep))],
        zdarzenie_id=ev.zdarzenie_id.values[rep], oddzial=ev.oddzial.values[rep],
        rejon=ev.rejon.values[rep], urzadzenie_id=ev.urzadzenie_id.values[rep],
        kanal=np.where(ch < 0.34, "IVR", np.where(ch2 < 0.45, "aplikacja", "telefon")),
        t_przyjecia=ts,
        nr_odbiorcy=["PPE%09d" % v for v in rng.integers(100000000, 999999999, len(rep))],
        opis=np.where(rng.random(len(rep)) < 0.82, "brak zasilania", "brak napiecia, caly budynek")))
    return out


def scada_log(ev, seed=P.SEED):
    """Device-operation records from the telemetry archive, timestamped in UTC."""
    rng = np.random.default_rng(seed + 23)
    t = ev[ev.telemetrowane].copy()
    out = pd.DataFrame(dict(
        rekord_id=["SC%09d" % (3100007 + 11 * i) for i in range(len(t))],
        urzadzenie_id=t.urzadzenie_id.values,
        feeder_id=t.feeder_id.values,
        operacja=np.where(t.klasa_odcinka.values == "SN-magistrala", "wylacznik-otwarcie",
                          np.where(t.klasa_odcinka.values == "SN/nN-stacja", "rozlacznik-otwarcie",
                                   "wskaznik-zwarcia")),
        ts_utc=(t.t_utrata.values
                - utc_offset_hours(t.t_utrata.values).astype("timedelta64[h]")),
        jakosc_sygnalu=np.where(rng.random(len(t)) < 0.93, "OK", "OK-opozniony")))
    return out.sort_values("ts_utc").reset_index(drop=True)
