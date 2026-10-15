"""The world of cell C-22, simulated once: its machines asset by asset (rack additions, hardware faults, maintenance,
re-imaging under a new cluster id, retirements), the tenants' quarterly reservations and hourly use, the batch tier's
2026 Q3 training runs with their checkpoints, resizes, preemptions and resumptions, the storage service's load, the
quota changes of 2026 Q3 and the quota service's reconciliation runs, the budgets and the past reviews' outcomes.

Everything downstream (records, documents, the goldens, the checks) reads the World object this module returns."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

H0 = K.EXPORT_START
NMIN = int((K.EXPORT_END - H0).total_seconds() // 60)       # minutes on file
NHOUR = NMIN // 60


def minute_of(t):
    return int((t - H0).total_seconds() // 60)


def t_of_minute(m):
    return H0 + dt.timedelta(minutes=int(m))


class World:
    pass


SALT = {"maint": 2, "runs": 112, "quota": 269}     # fixed stream offsets, chosen once so the 2026 Q3 tables sit mid-bin


def _salted(name, *keys):
    return K.rng(name, *keys, SALT[name]) if SALT[name] else K.rng(name, *keys)


# ---------------------------------------------------------------------------------------------------- racks
RACK_ADDS = {  # date (UTC, 09:00) and racks added, by quarter; the start of 2025 has 210 racks in service
    "2025Q1": [("2025-01-28", 1), ("2025-02-18", 1), ("2025-03-11", 1)],
    "2025Q2": [("2025-04-15", 1), ("2025-05-27", 1)],
    "2025Q3": [("2025-07-08", 1), ("2025-08-26", 1), ("2025-09-16", 1)],
    "2025Q4": [("2025-10-21", 1), ("2025-11-25", 1)],
    "2026Q1": [("2026-01-27", 1), ("2026-02-17", 1), ("2026-03-10", 1)],
    "2026Q2": [("2026-04-21", 1), ("2026-05-19", 1), ("2026-06-16", 1)],
    "2026Q3": [("2026-07-14", 1), ("2026-08-25", 1), ("2026-09-15", 1)],
    "2026Q4": [("2026-10-20", 1), ("2026-11-17", 1), ("2026-12-08", 1)],
}
START_RACKS = 210
MODELS = [("Lena R2-96", 2021), ("Lena R2-96", 2022), ("Lena R3-96", 2024), ("Lena R3-96", 2025), ("Lena R4-96", 2026)]


def _racks(W):
    """Every rack with its row, its position, its in-service time and its model; the 29 racks of the December 2026
    refresh too (in service from 28 December, after the export)."""
    racks = []
    seq = 0

    def add(t, model):
        nonlocal seq
        row = K.ROWS[min(seq // 22, len(K.ROWS) - 1)] if seq < 22 * 11 else K.ROWS[-1]
        racks.append(dict(rack_no=seq, row=row, pos=seq % 22 + 1 if seq < 242 else seq - 242 + 1,
                          in_service=t, model=model))
        seq += 1
    r = K.rng("racks")
    first = []
    for i in range(START_RACKS):
        y = 2021 if i < 96 else (2022 if i < 170 else 2024)
        first.append(dt.datetime(y, 1 + int(r.integers(0, 12)), 1 + int(r.integers(0, 27)), 9, tzinfo=K.UTC))
    for t in sorted(first):          # positions were filled in the order the racks arrived
        add(t, "Lena R2-96" if t.year < 2024 else "Lena R3-96")
    for q in K.QUARTERS:
        for d, n in RACK_ADDS[q]:
            t = dt.datetime.fromisoformat(d).replace(hour=9, tzinfo=K.UTC)
            for _ in range(n):
                add(t, "Lena R3-96" if t.year == 2025 else "Lena R4-96")
    for _ in range(K.NEW_RACKS):
        add(K.REFRESH_IN_SERVICE, "Lena R4-96")
    W.racks = racks
    assert len(racks) == START_RACKS + sum(n for q in K.QUARTERS for _, n in RACK_ADDS[q]) + K.NEW_RACKS
    assert sum(1 for x in racks if x["in_service"] < K.REFRESH_IN_SERVICE) * K.RACK == 4640
    assert len(racks) * K.RACK == K.Q1_MACHINES


# ---------------------------------------------------------------------------------------------------- assets and events
def _new_asset(rk_row, rack, slot, model, installed, origin):
    return dict(tag=None, serial=None, row=rk_row, rack=rack, slot=slot, model=model, installed=installed,
                origin=origin, ids=[], outages=[], retired=None, replaces=None)


def _assets(W):
    """One asset per slot, and the spares that replace retired ones. Each asset's outages over the export window:
    hardware faults (about one in a hundred machines a month; repaired and back under the same cluster id, back after a
    boot-disk replacement and re-image under a new one, or retired and replaced from spares a few days later) and
    planned maintenance (a wave each month: firmware under the same id or an OS re-image under a new one). 2026 Q3's
    outages are kept inside one month each. Cluster ids and asset tags are issued in time order (MAD1's cluster manager
    and stores issue them for all five cells, so each cell's run has gaps)."""
    r = K.rng("assets")
    assets = []
    W.waves = []
    for rk in W.racks:
        for sl in range(1, K.RACK + 1):
            assets.append(_new_asset(rk["row"], "%s-%02d" % (rk["row"], rk["pos"]), sl, rk["model"], rk["in_service"],
                                     "rack"))
    lam = 0.0100 / (30.4 * 24 * 60)          # hardware faults per in-service minute
    end = K.EXPORT_END
    queue = list(assets)
    while queue:
        a = queue.pop(0)
        if a["installed"] >= end:
            continue
        t = max(a["installed"], H0)
        while True:
            t = t + dt.timedelta(minutes=float(r.exponential(1 / lam)))
            if t >= end:
                break
            dur = float(np.clip(r.lognormal(math.log(14.0), 0.62), 3.0, 70.0)) * 60
            fate = str(r.choice(["same", "reimage", "retire"], p=[0.66, 0.27, 0.07]))
            o = dict(cause="hw_fault", start=t.replace(second=0, microsecond=0), minutes=int(round(dur)), fate=fate)
            a["outages"].append(o)
            if fate == "retire":
                a["retired"] = o["start"]
                lag = dt.timedelta(days=int(r.integers(3, 12)), hours=int(r.integers(0, 6)), minutes=int(r.integers(0, 60)))
                ti = (o["start"] + lag).replace(hour=8 + int(r.integers(0, 8)), second=0, microsecond=0)
                while ti.weekday() >= 5:
                    ti += dt.timedelta(days=1)
                spare = "Lena R4-96" if ti.year >= 2026 else "Lena R3-96"
                b = _new_asset(a["row"], a["rack"], a["slot"], spare, ti, "spare")
                b["replaces"] = a
                assets.append(b)
                queue.append(b)
                break
            t = o["start"] + dt.timedelta(minutes=o["minutes"])
    # maintenance: a wave each month (firmware, BIOS and OS rollouts) over about two weeks of working days,
    # some 3 per cent of the machines in service; an OS rollout re-images a machine, which registers anew
    for q in K.QUARTERS:
        qs = K.q_start(q)
        for mi in range(3):
            ms = dt.datetime(qs.year, qs.month + mi, 1, tzinfo=K.UTC)
            if ms >= end:
                continue
            rq = _salted("maint", q, mi) if q == "2026Q3" else K.rng("maint", q, mi)
            w0 = ms + dt.timedelta(days=int(rq.integers(3, 9)))
            W.waves.append((ms, w0))
            live = [a for a in assets if a["installed"] < w0 and not (a["retired"] and a["retired"] < w0)]
            pick = rq.choice(len(live), size=int(len(live) * float(rq.uniform(0.026, 0.036))), replace=False)
            for i in sorted(pick):
                a = live[i]
                st = w0 + dt.timedelta(days=int(rq.integers(0, 15)))
                st = st.replace(hour=7 + int(rq.integers(0, 8)), minute=int(rq.integers(0, 60)), second=0,
                                microsecond=0)
                while st.weekday() >= 5:
                    st += dt.timedelta(days=1)
                if st >= min(end, ms + dt.timedelta(days=27)):
                    continue
                dur = int(rq.integers(120, 540))
                fate = "reimage" if rq.random() < 0.29 else "same"
                a["outages"].append(dict(cause="maintenance", start=st, minutes=dur, fate=fate))
    # an asset is out for one thing at a time (a planned job that would overlap a fault is dropped); 2026 Q3's outages
    # stay inside their month
    for a in assets:
        a["outages"].sort(key=lambda o: (o["start"], o["cause"] != "hw_fault"))
        keep = []
        for o in a["outages"]:
            s0, e0 = o["start"], o["start"] + dt.timedelta(minutes=o["minutes"])
            if a["retired"] and s0 > a["retired"]:
                continue
            if keep:
                p = keep[-1]
                pe = p["start"] + dt.timedelta(minutes=p["minutes"])
                if s0 < pe:
                    if o["cause"] == "maintenance":
                        continue
                    if p["cause"] == "maintenance":
                        keep.pop()
            if o["fate"] != "retire" and K.Q3_START - dt.timedelta(days=4) <= s0 < K.Q3_END + dt.timedelta(days=4):
                mb = dt.datetime(s0.year, s0.month, 1, tzinfo=K.UTC)
                nb = dt.datetime(s0.year + (s0.month == 12), 1 if s0.month == 12 else s0.month + 1, 1, tzinfo=K.UTC)
                if e0 >= nb - dt.timedelta(hours=1) or s0 < mb + dt.timedelta(hours=1):
                    continue
            keep.append(o)
        a["outages"] = keep
        assert not a["retired"] or keep[-1]["fate"] == "retire"
    # registrations in time order: installs (2021 to 2024 for the original racks, with the odd re-image before 2025),
    # re-images in the window, spares; then cluster ids and asset tags issued in that order
    regs = []
    for a in assets:
        if a["installed"] < K.REFRESH_IN_SERVICE:
            regs.append((a["installed"], 0, a))
        if a["installed"] < H0 - dt.timedelta(days=60):
            n = int(r.random() < 0.33) + int(r.random() < 0.07)
            span = (H0 - dt.timedelta(days=12) - a["installed"]).total_seconds()
            for x in sorted(float(r.uniform(0.15, 1.0)) for _ in range(n)):
                regs.append(((a["installed"] + dt.timedelta(seconds=span * x)).replace(second=0, microsecond=0), 1, a))
        for o in a["outages"]:
            if o["fate"] == "reimage":
                regs.append((o["start"] + dt.timedelta(minutes=o["minutes"]), 1, a))
    regs.sort(key=lambda x: (x[0], x[1], x[2]["rack"], x[2]["slot"]))
    mid = 3_104_200
    for t, _, a in regs:
        mid += int(r.integers(1, 26))
        a["ids"].append((t, mid))
    order = sorted(assets, key=lambda a: (a["installed"], a["rack"], a["slot"]))
    tag_no = 402_117
    week_count = {}
    for a in order:
        tag_no += int(r.integers(1, 4))
        a["tag"] = "SRV-%06d" % tag_no
        y, w, _ = (a["installed"] - dt.timedelta(days=int(r.integers(20, 50)))).isocalendar()
        week_count[(y, w)] = week_count.get((y, w), int(r.integers(100, 400))) + int(r.integers(1, 9))
        a["serial"] = "CZ%02d%02d%04d" % (y % 100, w, week_count[(y, w)])
    assert len({a["tag"] for a in assets}) == len(assets) and len({a["serial"] for a in assets}) == len(assets)
    assert len({m for a in assets for _, m in a["ids"]}) == sum(len(a["ids"]) for a in assets)
    W.assets = assets


def _machine_minutes(W):
    """Installed and in-service machine counts per minute of the export window, and hourly averages."""
    inst = np.zeros(NMIN + 1, dtype=np.int32)
    out = np.zeros(NMIN + 1, dtype=np.int32)
    for a in W.assets:
        m0 = minute_of(a["installed"])
        if m0 >= NMIN:
            continue
        inst[max(m0, 0)] += 1
        for o in a["outages"]:
            s = minute_of(o["start"])
            if o["fate"] == "retire":
                if s < NMIN:
                    inst[s] -= 1
                continue
            e = s + o["minutes"]
            if s < NMIN:
                out[s] += 1
                out[min(e, NMIN)] -= 1
    inst = np.cumsum(inst)[:NMIN]
    out = np.cumsum(out)[:NMIN]
    W.installed_min = inst
    W.inservice_min = inst - out
    W.installed_h = inst.reshape(NHOUR, 60).mean(axis=1)
    W.inservice_h = W.inservice_min.reshape(NHOUR, 60).mean(axis=1)


# ---------------------------------------------------------------------------------------------------- the reviews
G_PATH = {"2025Q1": 56000, "2025Q2": 58000, "2025Q3": 55000, "2025Q4": 57000,
          "2026Q1": 58000, "2026Q2": 55000, "2026Q3": 57000, "2026Q4": 56000}


def ceil_to(x, step):
    return int(math.ceil(x / step - 1e-9) * step)


def store_sizing(me, G):
    """The storage platform team's reservation for a quarter: its busiest hour at the quarter's machines and the batch
    tier at its guarantee, with 40 cores to spare, rounded up to the next 100."""
    return ceil_to(K.STORE_BASE + K.STORE_PER_MACHINE * me + K.STORE_PER_BATCH * G + 40, 100)


def _history(W):
    """Each past quarter's review under CS-3: reservable cores from the machines in service at the quarter's start; the
    firm tenants' approved reservations; cell-ctl and cell-store at their forecast busiest hours; the guarantee the
    largest whole thousand left. Racks were added as the firm tenants grew, so the guarantee moved between 55,000 and
    58,000 cores through 2025 and 2026."""
    r = K.rng("history")
    W.m_start, W.m_end, W.reservable = {}, {}, {}
    W.ctl_res, W.store_res, W.guarantee, W.unreserved = {}, {}, {}, {}
    W.firm_res = {t: {} for t in K.FIRM}
    for i, q in enumerate(K.QUARTERS):
        qs, qe = K.q_start(q), K.q_end(q)
        ms = sum(1 for x in W.racks if x["in_service"] <= qs) * K.RACK
        me = sum(1 for x in W.racks if x["in_service"] < qe and x["in_service"] < K.REFRESH_IN_SERVICE) * K.RACK
        W.m_start[q], W.m_end[q] = ms, me
        R = int(round(ms * K.CORES * K.OVERCOMMIT))
        W.reservable[q] = R
        ctl = ceil_to(K.CTL_BASE + 7 * i + 26 + 30 + float(r.uniform(0, 12)), 10)
        G = G_PATH[q]
        F = R - ctl - store_sizing(me, G) - G - int(r.integers(300, 800))
        w = {t: v["w"] / (1 + v["g"]) ** (7 - i) * (1 + float(r.normal(0, 0.004))) for t, v in K.FIRM_INFO.items()}
        tot = sum(w.values())
        for t in K.FIRM:
            W.firm_res[t][q] = int(round(F * w[t] / tot / 100.0)) * 100
        Fs = sum(W.firm_res[t][q] for t in K.FIRM)
        g = next(Gc for Gc in range(R // 1000 * 1000, 0, -1000) if Fs + ctl + store_sizing(me, Gc) + Gc <= R)
        assert g == G, (q, g, G)
        W.ctl_res[q], W.store_res[q], W.guarantee[q] = ctl, store_sizing(me, G), G
        W.unreserved[q] = R - Fs - ctl - W.store_res[q] - G


BUDGET_TUNE = {"search-api": 0.55, "pricing": 0.52, "reco-serve": 0.38}


def _firm_q1(W):
    """The Q1 2027 requests (filed by 4 December), the 2026 monthly budgets (revised in April and October; December's
    held for every month of Q1 2027 by the freeze note) and the approvals under CS-3 section 3: each request held to
    the cores its December budget pays for at the rate from 1 January 2027."""
    r = K.rng("budgets")
    q4 = {t: W.firm_res[t]["2026Q4"] for t in K.FIRM}
    W.q1_request = {t: int(round(q4[t] * K.FIRM_INFO[t]["ratio"] / 50.0)) * 50 for t in K.FIRM}
    r_q4, r_q1 = K.rate_on(dt.date(2026, 12, 1)), K.rate_on(dt.date(2027, 1, 1))
    dec = {}
    for t in K.FIRM:
        lo = q4[t] * r_q4
        if t in K.CAPPED:
            hi = W.q1_request[t] * r_q1
            assert hi > lo * 1.01, t
            dec[t] = int(round((lo + (hi - lo) * BUDGET_TUNE[t]) / 500.0)) * 500
        else:
            dec[t] = ceil_to(max(lo, W.q1_request[t] * r_q1) * (1 + float(r.uniform(0.008, 0.035))), 500)
    budgets = {}
    for t in K.FIRM:
        months = {}
        for m in range(1, 13):
            q = "2026Q%d" % ((m - 1) // 3 + 1)
            need = W.firm_res[t][q] * K.rate_on(dt.date(2026, m, 1))
            months[m] = max(need * (1.012 if m < 4 else 1.008), dec[t] * (0.955 if m < 4 else (0.978 if m < 10 else 1.0)))
            months[m] = ceil_to(months[m], 500)
        months[10] = months[11] = months[12] = dec[t]
        budgets[t] = months
    W.budgets = budgets
    W.q1_cap = {t: int(math.floor(budgets[t][12] / r_q1 + 1e-9)) for t in K.FIRM}
    W.q1_approved = {t: min(W.q1_request[t], W.q1_cap[t]) for t in K.FIRM}
    W.q1_firm = sum(W.q1_approved.values())
    assert sorted(t for t in K.FIRM if W.q1_cap[t] < W.q1_request[t]) == sorted(K.CAPPED)


def _ctl_hourly(W):
    r = K.rng("ctl")
    hrs = np.arange(NHOUR)
    qidx = np.array([K.QUARTERS.index(K.q_of(H0 + dt.timedelta(hours=int(h)))) for h in hrs])
    local_h = (hrs + 1) % 24
    base = K.CTL_BASE + 7 * qidx + 26 * np.sin(2 * np.pi * (local_h - 8) / 24)
    W.ctl_h = base + r.normal(0, 6.5, NHOUR)


def _batch_fill(W):
    """The batch tier's cores in use, hour by hour, outside 2026 Q3: near its guarantee (queues are always deep), with
    the tier's own pauses (scheduler upgrades) and the odd thin hour between jobs."""
    r = K.rng("batchfill")
    b = np.zeros(NHOUR)
    W.batch_pauses = []
    for q in K.QUARTERS:
        qs, qe = K.q_start(q), min(K.q_end(q), K.EXPORT_END)
        h0, h1 = int((qs - H0).total_seconds() // 3600), int((qe - H0).total_seconds() // 3600)
        G = W.guarantee[q]
        fill = 1.0 - r.exponential(0.0085, h1 - h0)
        fill = np.clip(fill, 0.93, 1.0)
        top = r.choice(h1 - h0, size=max(3, (h1 - h0) // 180), replace=False)
        fill[top] = 1.0 - r.uniform(0.0, 0.0012, len(top))
        thin = r.choice(h1 - h0, size=(h1 - h0) // 260, replace=False)
        fill[thin] = r.uniform(0.86, 0.93, len(thin))
        b[h0:h1] = G * fill
        if q == "2026Q3":
            continue
        for p in range(1 if q in ("2025Q1", "2025Q3", "2026Q2") else 2):
            ph = h0 + int(r.integers(240, h1 - h0 - 240))
            d = int(r.integers(3, 6))
            b[ph:ph + d] = G * r.uniform(0.03, 0.08, d)
            W.batch_pauses.append((H0 + dt.timedelta(hours=ph), d))
    W.batch_h = b




# ---------------------------------------------------------------------------------------------------- 2026 Q3 batch runs
JOB_CORES = [256, 384, 512, 768, 1024, 1536, 2048, 3072]
JOB_P = [0.06, 0.08, 0.17, 0.17, 0.20, 0.15, 0.11, 0.06]
TEAM_MIX = {"ranking-ml": 0.24, "pricing-ml": 0.18, "fraud-ml": 0.13, "reco-ml": 0.20, "demand-ml": 0.12, "nlp-ml": 0.13}
TEAM_CKPT_H = {"ranking-ml": 2.6, "pricing-ml": 2.0, "fraud-ml": 1.7, "reco-ml": 3.2, "demand-ml": 2.3, "nlp-ml": 3.6}
TEAM_STEPS_H = {"ranking-ml": 1180, "pricing-ml": 2240, "fraud-ml": 3050, "reco-ml": 760, "demand-ml": 1610, "nlp-ml": 420}
SCHED_PAUSE = (dt.datetime(2026, 9, 9, 2, 0, tzinfo=K.UTC), dt.datetime(2026, 9, 9, 5, 35, tzinfo=K.UTC))
POWER_PAUSE = (K.POWER_EVENT, dt.datetime(2026, 8, 19, 5, 15, tzinfo=K.UTC))
RESTORE_FAIL = 0.36           # a preempted run's newest committed checkpoint fails validation on restore


def _q3_runs(W):
    """An event-driven scheduler for the batch tier from 22 June to 1 October 2026 (the runs file is the batch
    platform's quarter snapshot taken at 1 October 00:00 UTC). Jobs queue by team; a run starts when the tier has its
    cores free; elastic runs resize; every run writes a checkpoint every few hours (its trainer pauses at a step and
    writes; most writes commit a few minutes later); a run is preempted by the 19 August power event, the 9 September
    scheduler upgrade or a machine removal under one of its workers, and is resumed from the newest checkpoint that
    passes validation on restore."""
    import heapq
    r = _salted("runs")
    t0 = dt.datetime(2026, 6, 22, tzinfo=K.UTC)
    t_end = K.Q3_END
    cap = lambda t: W.guarantee["2026Q2"] if t < K.Q3_START else W.guarantee["2026Q3"]
    hits = []
    for a in W.assets:
        for o in a["outages"]:
            if t0 <= o["start"] < t_end - dt.timedelta(hours=16) and r.random() < 0.155:
                hits.append(o["start"])
    hits.sort()
    seq = {"run": 0, "job": 7_200_400, "ev": 0}
    runs, ckpts, resizes = [], [], []
    queue = []                 # jobs waiting (a resume carries its restore point)
    running = {}               # run_id -> run

    def push(t, kind, payload):
        seq["ev"] += 1
        heapq.heappush(evq, (t, seq["ev"], kind, payload))

    def new_job(t):
        t = t.replace(second=0, microsecond=0)
        team = str(r.choice(K.TEAMS, p=[TEAM_MIX[x] for x in K.TEAMS]))
        seq["job"] += int(r.integers(1, 9))
        return dict(job_id="job-%d" % seq["job"], team=team, cores=int(r.choice(JOB_CORES, p=JOB_P)),
                    wall_h=float(np.clip(r.lognormal(math.log(26.0), 0.75), 4.0, 140.0)),
                    ckpt_h=TEAM_CKPT_H[team] * float(r.uniform(0.85, 1.15)), elastic=bool(r.random() < 0.27),
                    submitted=t, progress=0.0, restore=None, resumed_from=None, ready=t, runs=[])

    def used():
        return sum(x["cores_now"] for x in running.values())

    def start(j, t):
        seq["run"] += 1
        rid = "tr-%07d" % (4_118_000 + seq["run"] * 7 + int(r.integers(0, 7)))
        rn = dict(run_id=rid, job=j, team=j["team"], cores=j["cores"], cores_now=j["cores"], started=t, ended=None,
                  state="RUNNING", resumed_from=j["resumed_from"], restore=j["restore"], start_progress=j["progress"],
                  ckpts=[], segs=[(t, j["cores"])])
        running[rid] = rn
        runs.append(rn)
        j["runs"].append(rn)
        if j["restore"] is None:
            c = dict(checkpoint_id="ck-%s-00" % rid[3:], run_id=rid, progress=0.0, write_started=t,
                     committed=t + dt.timedelta(minutes=2), valid=True)
            rn["ckpts"].append(c)
            ckpts.append(c)
            j["last_restore"] = c
        # its checkpoints, its completion, its resizes
        k = 1
        tc = t + dt.timedelta(hours=j["ckpt_h"] * float(r.uniform(0.9, 1.1)))
        remaining = j["wall_h"] - j["progress"]
        t_done = t + dt.timedelta(hours=remaining)
        while tc < t_done:
            c = dict(checkpoint_id="ck-%s-%02d" % (rid[3:], k), run_id=rid,
                     progress=j["progress"] + (tc - t).total_seconds() / 3600.0, write_started=tc.replace(second=0, microsecond=0),
                     committed=None, valid=True, commit_after=dt.timedelta(minutes=int(r.integers(3, 10))),
                     fails=bool(r.random() < 0.03))
            rn["ckpts"].append(c)
            ckpts.append(c)
            k += 1
            tc = tc + dt.timedelta(hours=j["ckpt_h"] * float(r.uniform(0.9, 1.1)))
        push(t_done.replace(second=0, microsecond=0) + dt.timedelta(minutes=1), "done", rid)
        if j["elastic"] and remaining > 6 and r.random() < 0.8:
            for _ in range(int(r.integers(1, 3))):
                push((t + dt.timedelta(hours=float(r.uniform(1.5, remaining - 1.0)))).replace(second=0, microsecond=0),
                     "resize", rid)

    def commit_upto(rn, t):
        """Settle the run's checkpoint writes up to time t (a write commits a few minutes after it starts)."""
        for c in rn["ckpts"]:
            if c.get("commit_after") is None or c["write_started"] + c["commit_after"] > t:
                continue
            if not c["fails"]:
                c["committed"] = c["write_started"] + c["commit_after"]
            c.pop("commit_after", None)

    def end_run(rn, t, state):
        rn["ended"] = t
        rn["state"] = state
        # checkpoints: written before t, committed if the write finished by t; later ones never written
        keep = []
        for c in rn["ckpts"]:
            if c["write_started"] >= t:
                ckpts.remove(c)
                continue
            if "commit_after" in c:
                if c["write_started"] + c["commit_after"] <= t and not c["fails"]:
                    c["committed"] = c["write_started"] + c["commit_after"]
                c.pop("commit_after")
                c.pop("fails", None)
            keep.append(c)
        rn["ckpts"] = keep
        del running[rn["run_id"]]
        rn["segs"].append((t, 0))

    def preempt(rn, t):
        end_run(rn, t, "PREEMPTED")
        j = rn["job"]
        own = [c for c in rn["ckpts"] if c["committed"] is not None and c["committed"] <= t]
        if own and r.random() < RESTORE_FAIL:
            own[-1]["valid"] = False
            own = own[:-1]
        restore = own[-1] if own else j["last_restore"]
        j["last_restore"] = restore
        j["restore"] = restore
        j["progress"] = restore["progress"]
        j["resumed_from"] = rn["run_id"]
        j["ready"] = t + dt.timedelta(minutes=int(r.integers(4, 45)))
        queue.insert(0, j)

    evq = []
    for h in hits:
        push(h, "hit", None)
    for a, b in (POWER_PAUSE, SCHED_PAUSE):
        push(a, "pause", b)
    push(K.Q3_START, "cap", None)
    for _ in range(190):
        queue.append(new_job(t0 - dt.timedelta(hours=float(r.uniform(0, 30)))))
    paused_until = t0
    t = t0
    push(t0, "tick", None)
    while evq:
        t, _, kind, payload = heapq.heappop(evq)
        if t >= t_end:
            break
        if kind == "done" and payload in running:
            rn = running[payload]
            # a run finishes only after its last write has committed
            end_run(rn, t, "COMPLETED")
        elif kind == "resize" and payload in running:
            rn = running[payload]
            cur = rn["cores_now"]
            room = cap(t) - used()
            opts = [v for v in (cur // 2, (cur * 3) // 4, (cur * 5) // 4, (cur * 3) // 2)
                    if 128 <= v <= 4096 and v != cur and v - cur <= room]
            if opts:
                v = int(r.choice(opts))
                tt = t.replace(second=0, microsecond=0)
                rn["cores_now"] = v
                rn["segs"].append((tt, v))
                resizes.append(dict(run_id=rn["run_id"], at=tt, cores_before=cur, cores_after=v))
        elif kind == "hit" and t >= paused_until and running:
            cands = []
            for rn in running.values():
                if rn["started"] > t - dt.timedelta(minutes=10):
                    continue
                commit_upto(rn, t)
                own = [c for c in rn["ckpts"] if c["committed"] is not None and c["committed"] <= t]
                worst = own[-2]["write_started"] if len(own) >= 2 else rn["job"]["runs"][0]["started"]
                if t < K.Q3_START + dt.timedelta(days=5) and (rn["started"] < K.Q3_START or worst < K.Q3_START):
                    continue
                cands.append(rn)
            if cands:
                w = np.array([x["cores_now"] for x in cands], dtype=float)
                rn = cands[int(r.choice(len(cands), p=w / w.sum()))]
                preempt(rn, t.replace(second=0, microsecond=0))
        elif kind == "pause":
            for rn in list(running.values()):
                commit_upto(rn, t)
                preempt(rn, t.replace(second=0, microsecond=0))
            paused_until = payload
            for j in queue:
                j["ready"] = max(j["ready"], payload + dt.timedelta(minutes=int(r.integers(2, 30))))
        # admission at this time (or the next ready time)
        if t >= paused_until:
            room = cap(t) - used()
            i = 0
            waiting = None
            while i < len(queue) and room > 0:
                j = queue[i]
                if j["ready"] > t:
                    waiting = j["ready"] if waiting is None else min(waiting, j["ready"])
                    i += 1
                    continue
                if j["cores"] <= room:
                    queue.pop(i)
                    start(j, t)
                    room -= j["cores"]
                    j["restore"] = j["restore"]
                else:
                    i += 1
            if waiting is not None:
                push(waiting, "tick", None)
        while len(queue) < 140:
            queue.append(new_job(t))
        if not evq or evq[0][0] > t + dt.timedelta(minutes=30):
            push(t + dt.timedelta(minutes=30), "tick", None)
    for rn in list(running.values()):
        for c in list(rn["ckpts"]):
            if c["write_started"] >= t_end:
                rn["ckpts"].remove(c)
                ckpts.remove(c)
            elif "commit_after" in c:
                if c["write_started"] + c["commit_after"] <= t_end and not c["fails"]:
                    c["committed"] = c["write_started"] + c["commit_after"]
                c.pop("commit_after")
                c.pop("fails", None)
    # the quarter's file: every run that held cores in Q3
    W.q3_runs = [x for x in runs if x["ended"] is None or x["ended"] > K.Q3_START]
    keep_ids = {x["run_id"] for x in W.q3_runs}
    ref = {x["restore"]["checkpoint_id"] for x in W.q3_runs if x["restore"] is not None}
    W.q3_ckpts = [c for c in ckpts if c["run_id"] in keep_ids or c["checkpoint_id"] in ref]
    for c in W.q3_ckpts:
        c.pop("commit_after", None)
        c.pop("fails", None)
    W.q3_resizes = [x for x in resizes if x["run_id"] in keep_ids]
    W.all_runs = runs
    # batch cores held per minute, 22 June to 1 October
    held = np.zeros(NMIN + 1)
    for rn in runs:
        segs = rn["segs"] + ([(t_end, 0)] if rn["ended"] is None else [])
        for (a, v), (b, _) in zip(segs[:-1], segs[1:]):
            ma, mb = minute_of(a), minute_of(b)
            held[ma] += v
            held[mb] -= v
    held = np.cumsum(held)[:NMIN]
    W.batch_held_min = held


def _batch_q3_hourly(W):
    r = K.rng("batchq3")
    h0 = int((K.Q3_START - H0).total_seconds() // 3600)
    h1 = int((K.Q3_END - H0).total_seconds() // 3600)
    held_h = W.batch_held_min.reshape(NHOUR, 60).mean(axis=1)
    use = held_h[h0:h1] * r.uniform(0.9955, 0.9995, h1 - h0)
    W.batch_h[h0:h1] = use


# ---------------------------------------------------------------------------------------------------- 2026 Q3 quota changes
RECON_MIN = (5, 6 * 60 + 5, 12 * 60 + 5, 18 * 60 + 5)


def _q3_quota(W):
    """Mid-quarter reservation changes for the firm tenants in 2026 Q3: releases re-granted to other tenants through
    the cell's capacity desk, and one transfer. A change is requested in the quota tool and applied by the quota
    service's next reconciliation run (00:05, 06:05, 12:05 and 18:05 UTC); the service ran none from the power event
    on 19 August to 22 August 12:05."""
    r = _salted("quota")
    rj = K.rng("quota", "jitter")
    runs = []
    d = K.Q3_START
    while d < K.Q3_END:
        for mm in RECON_MIN:
            t = d + dt.timedelta(minutes=mm)
            if K.RECONCILER_STOP[0] <= t < K.RECONCILER_STOP[1] + dt.timedelta(minutes=5):
                continue
            t = t + dt.timedelta(seconds=int(rj.integers(0, 4)))
            runs.append(dict(started=t, finished=t + dt.timedelta(seconds=int(r.integers(40, 260))), applied=[]))
        d += dt.timedelta(days=1)
    changes = []
    cid = 52_810
    for t in K.FIRM:
        base = W.firm_res[t]["2026Q3"]
        kinds = ["release", "grant"] + (["grant"] if base > 40000 else [])
        # releases come in the first half of the quarter and are re-granted in the second
        days = [int(r.integers(3, 38))] + sorted(int(x) for x in r.choice(np.arange(42, 86), size=len(kinds) - 1,
                                                                          replace=False))
        # exactly one request per tenant reaches the quota service late: an evening request (applied at 00:05) for
        # the large tenants, one during the reconciler's stop for the small; reviews and ads-listings have the
        # transfer instead
        late = -1 if t in ("reviews", "ads-listings") else int(r.integers(1, len(kinds)))
        for k, (kind, dd) in enumerate(zip(kinds, days)):
            day = K.Q3_START + dt.timedelta(days=int(dd))
            if k == late and base < 40000:
                req = K.RECONCILER_STOP[0] + dt.timedelta(hours=int(r.integers(5, 43)), minutes=int(r.integers(0, 60)))
            elif k == late:
                if day.day >= 30:
                    day -= dt.timedelta(days=2)
                req = day + dt.timedelta(hours=18, minutes=int(r.integers(12, 335)))
            else:
                if K.RECONCILER_STOP[0] - dt.timedelta(days=1) <= day <= K.RECONCILER_STOP[1]:
                    day += dt.timedelta(days=5)
                req = day + dt.timedelta(hours=7, minutes=int(r.integers(0, 290)))
            share = float(r.uniform(0.026, 0.045)) if kind == "release" else float(r.uniform(0.02, 0.036))
            delta = max(600, int(round(base * share / 100.0)) * 100)
            cid += int(r.integers(3, 40))
            changes.append(dict(change_id="QC-%06d" % cid, tenant=t, delta=-delta if kind == "release" else delta,
                                requested=req.replace(second=int(r.integers(0, 60))), kind=kind,
                                ticket="CAP-%d" % (30400 + int(r.integers(0, 900)))))
    # the transfer: reviews to ads-listings, two changes on one ticket, requested during the reconciler's stop
    tr_t = dt.datetime(2026, 8, 20, 9, 37, 12, tzinfo=K.UTC)
    for t, delta in (("reviews", -1200), ("ads-listings", 1200)):
        cid += int(r.integers(3, 40))
        changes.append(dict(change_id="QC-%06d" % cid, tenant=t, delta=delta, requested=tr_t, kind="transfer",
                            ticket="CAP-30917"))
    # grants re-grant what was released: the quarter's releases and the cell's headroom shared among the grants
    head = W.reservable["2026Q3"] - sum(W.firm_res[t]["2026Q3"] for t in K.FIRM) - W.ctl_res["2026Q3"] - \
        W.store_res["2026Q3"] - W.guarantee["2026Q3"]
    rel = -sum(c["delta"] for c in changes if c["kind"] == "release")
    grants = [c for c in changes if c["kind"] == "grant"]
    pool = rel + head - 400 - 600 * len(grants)
    w = r.dirichlet([2.2] * len(grants))
    for c, x in zip(grants, w):
        c["delta"] = 600 + int(math.floor(pool * float(x) / 100.0)) * 100
    changes.sort(key=lambda c: (c["requested"], c["change_id"]))
    for c in changes:
        nxt = next(x for x in runs if x["started"] > c["requested"])
        c["applied"] = nxt["started"]
        nxt["applied"].append(c["change_id"])
    # the cell's reservations never pass its reservable cores
    run_sum, peak = 0, 0
    for c in sorted(changes, key=lambda c: c["applied"]):
        run_sum += c["delta"]
        peak = max(peak, run_sum)
    assert peak <= head, (peak, head)
    W.q3_headroom = head
    W.q3_changes = changes
    W.q3_recon = runs


# ---------------------------------------------------------------------------------------------------- hourly use
def _firm_hourly(W):
    """Each firm tenant's cores in use: its reservation in force times a utilisation that follows Madrid's day (two
    peaks for consumer traffic), the week, the travel season (summer, the January sales) and its own noise; the
    settlement runs follow their nightly batch window."""
    r = K.rng("firmuse")
    hrs = np.arange(NHOUR)
    tt = [H0 + dt.timedelta(hours=int(h)) for h in hrs]
    loc = np.array([K.madrid(x)[0].hour for x in tt])
    wd = np.array([K.madrid(x)[0].weekday() for x in tt])
    doy = np.array([x.timetuple().tm_yday for x in tt])
    qn = [K.q_of(x) for x in tt]
    season = 1 + 0.05 * np.cos(2 * np.pi * (doy - 200) / 365) + 0.025 * np.exp(-((doy - 10) / 9.0) ** 2)
    W.firm_h = {}
    for t in K.FIRM:
        res = np.array([W.firm_res[t][q] for q in qn], dtype=float)
        for c in W.q3_changes:
            if c["tenant"] == t:
                h = int(math.ceil((c["applied"] - H0).total_seconds() / 3600.0))
                h1 = int((K.Q3_END - H0).total_seconds() // 3600)
                res[h:h1] += c["delta"]
        if t == "settle-batch":
            shape = 0.42 + 0.44 * ((loc >= 0) & (loc < 6)) + 0.08 * (wd == 0)
        else:
            shape = 0.50 + 0.17 * np.exp(-((loc - 12.0) / 2.6) ** 2) + 0.21 * np.exp(-((loc - 21.0) / 2.2) ** 2)
            shape *= np.where(wd >= 5, 0.93, 1.0)
            shape *= season
        noise = 1 + r.normal(0, 0.012, NHOUR)
        u = np.clip(shape * noise * float(r.uniform(0.95, 1.03)), 0.2, 0.985)
        W.firm_h[t] = res * u


def _store_unmodelled(W, draw=None):
    """cell-store's load that neither driver carries, hour by hour: the small tenants' daily cycle, a slow drift, the
    weekly rolling restart and the hours whose samples arrived late. None of it follows the machines or the batch tier:
    within each quarter every part is uncorrelated with the machines in service, the machines out and the batch cores,
    and each part carries the same mean in every quarter."""
    r = K.rng("store-texture", K.STORE_TEXTURE_DRAW if draw is None else draw)
    hrs = [H0 + dt.timedelta(hours=h) for h in range(NHOUR)]
    loc = np.array([K.madrid(x)[0].hour for x in hrs])
    wd = np.array([K.madrid(x)[0].weekday() for x in hrs])
    uwd = np.array([x.weekday() for x in hrs])
    uh = np.array([x.hour for x in hrs])
    qid = np.array([K.QUARTERS.index(K.q_of(x)) for x in hrs])
    drivers = np.column_stack([W.inservice_h, W.installed_h - W.inservice_h, W.batch_h])

    def apart(v, rows):
        v = v.copy()
        for q in range(len(K.QUARTERS)):
            m = (qid == q) & rows
            X = drivers[m] - drivers[m].mean(axis=0)
            co, *_ = np.linalg.lstsq(X, v[m] - v[m].mean(), rcond=None)
            v[m] -= X @ co
        return v
    prof = np.exp(-((loc - 20.5) / 2.8) ** 2) + 0.45 * np.exp(-((loc - 12.0) / 2.5) ** 2)
    prof = prof / prof.max()
    tenants = K.STORE_TENANTS * (np.where(wd >= 5, 0.5, 1.0) * prof - 0.5)
    sd, phi = K.STORE_DRIFT
    e = r.normal(0, sd * math.sqrt(1 - phi ** 2), NHOUR)
    drift = np.zeros(NHOUR)
    for i in range(1, NHOUR):
        drift[i] = phi * drift[i - 1] + e[i]
    restart = (uwd == 1) & (uh >= 3) & (uh < 5)
    p_late, lo, hi = K.STORE_LATE
    late = (r.random(NHOUR) < p_late) & ~restart
    cont = apart(apart(tenants + drift, ~restart & ~late), restart | late)
    for q in range(len(K.QUARTERS)):
        cont[qid == q] += cont.mean() - cont[qid == q].mean()
    rs = np.zeros(NHOUR)
    rs[restart] = -r.uniform(K.STORE_RESTART[0], K.STORE_RESTART[1], int(restart.sum()))
    lt = np.zeros(NHOUR)
    lt[late] = -r.uniform(lo, hi, int(late.sum()))
    parts = []
    for v, rows in ((rs, restart), (lt, late)):
        v = apart(v, rows)
        mu = v.mean()
        for q in range(len(K.QUARTERS)):
            v[qid == q] *= mu / v[qid == q].mean()
        parts.append(v)
    out = cont + parts[0] + parts[1]
    return out - out.mean() + K.STORE_LEVEL


def _store_hourly(W, draw=None):
    r = K.rng("store")
    W.store_h = K.STORE_BASE + K.STORE_PER_MACHINE * W.inservice_h + K.STORE_PER_BATCH * W.batch_h + \
        r.normal(0, K.STORE_NOISE, NHOUR) + _store_unmodelled(W, draw)


# ---------------------------------------------------------------------------------------------------- the world
def simulate():
    W = World()
    _racks(W)
    _assets(W)
    _machine_minutes(W)
    _history(W)
    _firm_q1(W)
    _ctl_hourly(W)
    _batch_fill(W)
    _q3_runs(W)
    _batch_q3_hourly(W)
    _q3_quota(W)
    _firm_hourly(W)
    _store_hourly(W)
    W.hours = [H0 + dt.timedelta(hours=h) for h in range(NHOUR)]
    return W


if __name__ == "__main__":
    import time
    a = time.time()
    W = simulate()
    print("simulated in %.1f s" % (time.time() - a))
    for q in K.QUARTERS:
        print(q, W.m_start[q], W.m_end[q], int(W.reservable[q]), sum(W.firm_res[t][q] for t in K.FIRM), W.ctl_res[q],
              W.store_res[q], W.guarantee[q])
    print("Q1 firm", W.q1_firm, W.q1_approved, W.q1_request)
    print("runs", len(W.q3_runs), "ckpts", len(W.q3_ckpts), "resizes", len(W.q3_resizes),
          "preempted", sum(1 for x in W.q3_runs if x["state"] == "PREEMPTED"))
    print("changes", len(W.q3_changes), "recon runs", len(W.q3_recon))
