"""Turn the simulated world into system records: MDM deliveries, the head-end history, the register,
the Wave 8 schedule. Pure functions of the simulation and their own seeded streams."""
import datetime as dt

import numpy as np

import world as W
import sim as S

EM_CHAIN = ["EM3.9.6", "EM3.10.2", "EM3.10.9", "EM3.11.4", "EM3.12.0", "EM3.12.1", "EM3.12.2"]
PX_CHAIN = ["PX5.1.9", "PX5.2.3", "PX5.2.7", "PX5.3.0", "PX5.3.1"]
ALL_IMAGES = dict(W.IMAGE)
for fam in W.OLD_IMAGES.values():
    for rel, img in fam:
        ALL_IMAGES[rel] = img
# the windows in which past waves moved meters onto each release (local dates)
WAVE_WINDOWS = {
    "EM3.10.2": ("2023-05-08", "2023-08-25"), "EM3.10.9": ("2024-09-02", "2024-11-29"),
    "EM3.11.4": ("2025-03-17", "2025-06-27"), "EM3.12.0": ("2025-12-01", "2026-03-27"),
    "EM3.12.1": ("2026-02-16", "2026-02-27"), "EM3.12.2": ("2026-09-22", "2026-09-23"),
    "PX5.2.3": ("2024-04-08", "2024-06-28"), "PX5.2.7": ("2025-07-14", "2025-09-26"),
    "PX5.3.0": ("2026-01-27", "2026-04-24"), "PX5.3.1": ("2026-09-08", "2026-09-09"),
}
RELEASED = {b[0]: b[4] for b in W.BUILDS}
RELEASED.update({"EM3.9.6": "2022-06-06", "EM3.10.2": "2023-04-24", "PX5.1.9": "2023-02-13", "PX5.2.3": "2024-03-25"})


def d(s):
    return dt.date.fromisoformat(s)


def _local(t):
    return t.astimezone(W.AEDT) if t.astimezone(W.AEDT).dst() is None else t


def utc(t):
    return t.astimezone(W.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_tz_for(day):
    """NSW local offset on a calendar date: AEDT from the first Sunday in October to the first
    Sunday in April, AEST otherwise (the transitions fall in the small hours, never in a window here)."""
    y = day.year
    def first_sun(m):
        x = dt.date(y, m, 1)
        return x + dt.timedelta(days=(6 - x.weekday()) % 7)
    if day >= first_sun(10) or day < first_sun(4):
        return W.AEDT
    return W.AEST


def night_activation(r, day):
    """An activation inside the 23:30 to 03:30 local window that opens on the given date."""
    tz = local_tz_for(day)
    start = dt.datetime(day.year, day.month, day.day, 23, 30, tzinfo=tz)
    return start + dt.timedelta(minutes=int(r.integers(0, 240)), seconds=int(r.integers(0, 60)))


def history(insts):
    """Every meter's firmware history from commissioning, ending on the build it starts the week on."""
    r = S.rng("history")
    ev = {}
    for i in sorted(insts, key=lambda x: x.nmi):
        serial, model, module, installed, _ = i.meters[0]
        chain = EM_CHAIN if module == "EM3" else PX_CHAIN
        target = i.build_start
        ti = chain.index(target)
        inst_day = installed.date()
        # commissioning image: the newest release out before the meter went in, not newer than target
        cands = [k for k in range(ti + 1) if d(RELEASED[chain[k]]) <= inst_day - dt.timedelta(days=40)]
        k0 = max(cands) if cands else 0
        if k0 > ti:
            k0 = ti
        steps = []
        k = k0
        while k < ti:
            nxt = [j for j in range(k + 1, ti + 1)]
            # EM3.12.1 is a hotfix only for its own subset; others skip it
            nxt = [j for j in nxt if chain[j] != "EM3.12.1" or target == "EM3.12.1"]
            # skip an intermediate release now and then, as waves did
            j = nxt[0] if (len(nxt) == 1 or r.random() < 0.7) else nxt[1]
            steps.append(chain[j])
            k = j
        if steps and steps[-1] != target:
            steps.append(target)
        out = []
        tz_in = local_tz_for(inst_day)
        t_comm = installed.replace(tzinfo=tz_in) + dt.timedelta(minutes=int(r.integers(20, 90)))
        out.append(dict(type="COMMISSIONED", image=ALL_IMAGES[chain[k0]], at=t_comm, job=None))
        last = t_comm
        for rel in steps:
            a, b = WAVE_WINDOWS[rel]
            lo, hi = max(d(a), last.date() + dt.timedelta(days=3)), d(b)
            if lo > hi:
                lo = last.date() + dt.timedelta(days=3)
                hi = lo + dt.timedelta(days=20)
            day = lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))
            if rel in ("EM3.12.2", "PX5.3.1"):
                day = d(a) + dt.timedelta(days=int(r.integers(0, 2)))
            t = night_activation(r, day)
            job = "W%s-%s" % (day.strftime("%y%m"), "EM" if module == "EM3" else "PX")
            if rel == "EM3.12.2":
                job = "WAVE6-%s" % ("A" if day == d(a) else "B")
            out.append(dict(type="FW_IMAGE_STAGED", image=ALL_IMAGES[rel],
                            at=t - dt.timedelta(hours=int(r.integers(20, 44)), minutes=int(r.integers(0, 60))), job=job))
            if r.random() < 0.035:      # a failed attempt, rolled back, retried a week later
                out.append(dict(type="FW_ACTIVATION_FAILED", image=ALL_IMAGES[rel], at=t, job=job))
                out.append(dict(type="FW_ROLLBACK_OK", image=ALL_IMAGES[chain[k0]] if not out[1:-2] else out[-2]["image"],
                                at=t + dt.timedelta(minutes=int(r.integers(6, 16))), job=job))
                t = night_activation(r, day + dt.timedelta(days=7))
            out.append(dict(type="FW_ACTIVATED", image=ALL_IMAGES[rel], at=t, job=job))
            last = t
        ev[serial] = out
    return ev


def fix_rollback_images(ev):
    """A rollback restores the image the meter was running before the failed attempt."""
    for serial, out in ev.items():
        running = None
        for e in out:
            if e["type"] in ("COMMISSIONED", "FW_ACTIVATED"):
                running = e["image"]
            if e["type"] == "FW_ROLLBACK_OK":
                e["image"] = running
    return ev


def week_events(insts, ev):
    """Wave 7 staging, failures, rollbacks and activations, and the mid-week meter exchanges."""
    r = S.rng("week_events")
    for i in sorted(insts, key=lambda x: x.nmi):
        serial = i.meters[0][0]
        if i.group == "w7":
            img = W.IMAGE[i.build_end]
            fam = "EM" if W.MODULE[i.build_end] == "EM3" else "PX"
            night = "tue" if i.move.get("retry") else i.move["night"]
            job = "WAVE7-%s" % ("A" if night == "tue" else "B")
            ev[serial].append(dict(type="FW_IMAGE_STAGED", image=img, job=job,
                                   at=dt.datetime(2026, 10, 5, 10, 0, tzinfo=W.AEDT) + dt.timedelta(minutes=int(r.integers(0, 600)))))
            if i.move.get("retry"):
                ev[serial].append(dict(type="FW_ACTIVATION_FAILED", image=img, at=i.move["failed_at"], job="WAVE7-A"))
                ev[serial].append(dict(type="FW_ROLLBACK_OK", image=W.IMAGE[i.build_start],
                                       at=i.move["failed_at"] + dt.timedelta(minutes=int(r.integers(6, 16))), job="WAVE7-A"))
                job = "WAVE7-B"
            ev[serial].append(dict(type="FW_ACTIVATED", image=img, at=i.move["at"], job=job))
        if i.group == "exch":
            old, new = i.meters[0][0], i.meters[1][0]
            ev[old].append(dict(type="DECOMMISSIONED", image=None, at=i.exchange, job=None))
            ev[new] = [dict(type="COMMISSIONED", image=W.IMAGE["EM3.12.2"],
                            at=i.meters[1][3].replace(tzinfo=W.AEDT) + dt.timedelta(minutes=int(r.integers(4, 25))), job=None)]
    return ev


def bench_meters():
    """Test-bench meters in the Silverwater lab: in the head-end, never at an installation."""
    r = S.rng("bench")
    out = {}
    for k in range(12):
        fam, rel = ("PX5", "PX5.3.1") if k < 7 else ("EM3", "EM3.12.2")
        serial = ("9" if fam == "PX5" else "8") + "%07d" % r.integers(0, 10 ** 7)
        t0 = dt.datetime(2026, 8, 25 + k % 5, 10, 15, tzinfo=W.AEST)
        out[serial] = (fam, [dict(type="COMMISSIONED", image=ALL_IMAGES["PX5.3.0" if fam == "PX5" else "EM3.12.0"], at=t0, job=None),
                             dict(type="FW_ACTIVATED", image=W.IMAGE[rel], at=t0 + dt.timedelta(days=4, hours=3), job="LAB")])
    return out


# ------------------------------------------------------------------ MDM deliveries

def deliveries(insts):
    """One row per data stream, read date and delivery. A delivery carries the whole register-day."""
    r = S.rng("deliveries")
    rows = []
    for i in sorted(insts, key=lambda x: x.nmi):
        suff, L, _ = W.PROFILES[i.profile]
        dc = S.day_counts(i)
        for dd, (per, c1, c2, c3) in enumerate(dc):
            rd = W.READ_DATES[dd]
            nxt = dt.datetime(rd.year, rd.month, rd.day, tzinfo=W.AEST) + dt.timedelta(days=1)
            t1 = nxt + dt.timedelta(minutes=int(r.integers(55, 285)), seconds=int(r.integers(0, 60)))
            vers = [(t1, per - c1 - c2 - c3, c1 + c2 + c3, 0)]
            if c1:
                t2 = nxt + dt.timedelta(minutes=int(r.integers(305, 352)), seconds=int(r.integers(0, 60)))
                vers.append((t2, per - c2 - c3, c2 + c3, 0))
            if c2:
                base = nxt + dt.timedelta(hours=int(r.integers(9, 15)), minutes=int(r.integers(0, 60)))
                if rd < W.READ_DATES[-1] and r.random() < 0.35:
                    base = base + dt.timedelta(days=1)
                vers.append((base, per - c3, c3, 0))
            # settlement turns substituted reads final two days on, where the extract reaches it
            last = vers[-1]
            tf = nxt + dt.timedelta(days=2, hours=4, minutes=int(r.integers(0, 50)))
            if last[2] > 0 and tf < W.EXTRACT_AT and tf > last[0]:
                vers.append((tf, last[1], 0, last[2]))
            for vi, (t, a, s_, f) in enumerate(vers):
                if t >= W.EXTRACT_AT:
                    continue
                for sx in suff:
                    rows.append((i.nmi, sx, rd, L, t, a, s_, f, vi))
    return rows


def cutoff_of(rd):
    return dt.datetime(rd.year, rd.month, rd.day, W.CUTOFF_HOUR_AEST, tzinfo=W.AEST) + dt.timedelta(days=1)


# ------------------------------------------------------------------ Wave 8 schedule

def wave8(insts):
    """The schedule as cut on Thursday 1 October from the meters then on each source build."""
    r = S.rng("wave8")
    pool = sorted(insts, key=lambda x: x.nmi)
    exch = [i for i in pool if i.group == "exch"]
    w7em = [i for i in pool if i.group == "w7" and i.build_end == "EM3.12.2"]
    w7px = [i for i in pool if i.group == "w7" and i.build_end == "PX5.3.1"]
    ex_pick = [exch[j] for j in sorted(r.choice(len(exch), 22, replace=False))]
    w7_pick = [w7em[j] for j in sorted(r.choice(len(w7em), W.WAVE8_PULLED_FORWARD, replace=False))]
    w7_pick += [w7px[j] for j in sorted(r.choice(len(w7px), W.WAVE8_PX_PULLED_FORWARD, replace=False))]
    quota = dict(W.WAVE8_EM_FROM)
    quota.update(W.WAVE8_PX_FROM)
    rows = []
    for i in ex_pick + w7_pick:
        rows.append(dict(inst=i, serial=i.meters[0][0], frm=i.build_start,
                         tgt="EM3.12.2" if i.build_start.startswith("EM") else "PX5.3.1"))
        quota[i.build_start] -= 1
    for frm, n in quota.items():
        full = [i for i in pool if i.group == "full" and i.build_start == frm]
        tgt = "EM3.12.2" if frm.startswith("EM") else "PX5.3.1"
        for j in sorted(r.choice(len(full), n, replace=False)):
            rows.append(dict(inst=full[j], serial=full[j].meters[0][0], frm=frm, tgt=tgt))
    order = r.permutation(len(rows))
    rows = [rows[j] for j in order]
    for k, row in enumerate(rows):
        row["batch"] = "A" if k % 2 == 0 else "B"
    # the depot re-batch: rows copied onto batch B and never deleted from batch A
    a_em = [x for x in rows if x["batch"] == "A" and x["tgt"] == "EM3.12.2" and x["inst"].group == "full"]
    a_px = [x for x in rows if x["batch"] == "A" and x["tgt"] == "PX5.3.1" and x["inst"].group == "full"]
    dup = [dict(x, batch="B") for x in a_em[:W.WAVE8_REBATCHED] + a_px[:W.WAVE8_PX_REBATCHED]]
    return rows + dup
