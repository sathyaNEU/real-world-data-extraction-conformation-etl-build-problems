"""The pack's data files, written from the simulated world: the cell monitoring export (the spine), the cell's
machines series, the reservation ledger, the Q1 2027 requests, the rate card, the tenant directory, the batch tier's
2026 Q3 runs, checkpoints and resizes, the cluster manager's 2026 Q3 machine events, and the quota service's 2026 Q3
changes and reconciliation runs."""
from __future__ import annotations

import datetime as dt
import json

import common as K
import world as WD

CELL_ID = "MAD1-C22"


def ts(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def in_gap(t):
    return K.COLLECTOR_GAP[0] <= t < K.COLLECTOR_GAP[1]


# ---------------------------------------------------------------------------------------------------- the monitoring export
USAGE_COLS = ["hour_start_utc", "cell", "tenant", "cores_in_use"]


def usage_rows(W):
    """One row per tenant per hour: the tenant's average cores in use over the hour. The collector was down on
    19 August 2026 from 01:00 to 08:00 UTC (no rows for those hours); the collector re-sent 17 March 2026, so that
    day's rows are in the file twice."""
    series = {t: W.firm_h[t] for t in K.FIRM}
    series["cell-ctl"] = W.ctl_h
    series["cell-store"] = W.store_h
    series["batch-train"] = W.batch_h
    order = sorted(series)
    for h, t in enumerate(W.hours):
        if in_gap(t):
            continue
        stamp = ts(t)
        twice = t.date() == K.RESENT_DAY
        for name in order:
            row = [stamp, CELL_ID, name, "%.1f" % max(0.0, float(series[name][h]))]
            yield row
            if twice:
                yield row


CELL_COLS = ["hour_start_utc", "cell", "machines_installed", "machines_in_service"]


def cell_rows(W):
    for h, t in enumerate(W.hours):
        if in_gap(t):
            continue
        yield [ts(t), CELL_ID, "%.1f" % W.installed_h[h], "%.1f" % W.inservice_h[h]]


# ---------------------------------------------------------------------------------------------------- ledger, requests, rates
LEDGER_COLS = ["quarter", "tenant", "class", "reserved_cores", "approved_on", "review"]
REVIEW_DATES = {"2025Q1": "2024-12-17", "2025Q2": "2025-03-18", "2025Q3": "2025-06-17", "2025Q4": "2025-09-16",
                "2026Q1": "2025-12-16", "2026Q2": "2026-03-17", "2026Q3": "2026-06-16", "2026Q4": "2026-09-15"}


def ledger_rows(W):
    for q in K.QUARTERS:
        ref = "CR-%s-C22" % q
        for t in K.FIRM:
            yield [q, t, "firm", W.firm_res[t][q], REVIEW_DATES[q], ref]
        yield [q, "cell-ctl", "platform", W.ctl_res[q], REVIEW_DATES[q], ref]
        yield [q, "cell-store", "platform", W.store_res[q], REVIEW_DATES[q], ref]
        yield [q, "batch-train", "batch", W.guarantee[q], REVIEW_DATES[q], ref]


REQ_COLS = ["request_id", "quarter", "tenant", "cores_requested", "filed_utc", "filed_by", "ticket"]


def request_rows(W):
    r = K.rng("requests")
    t0 = dt.datetime(2026, 11, 16, 8, 0, tzinfo=K.UTC)
    span = (K.REQUESTS_CLOSE - t0).total_seconds()
    filed = sorted(float(r.uniform(0.02, 0.995)) for _ in K.FIRM)
    order = [K.FIRM[i] for i in r.permutation(len(K.FIRM))]
    when = []
    for x, t in zip(filed, order):
        f = t0 + dt.timedelta(seconds=span * x)
        if f.weekday() >= 5:
            f -= dt.timedelta(days=f.weekday() - 4)
        f = f.replace(hour=8 + int(r.integers(0, 9)), minute=int(r.integers(0, 60)), second=int(r.integers(0, 60)))
        when.append((f, t))
    no = 3100 + int(r.integers(0, 40))
    tk = 31480 + int(r.integers(0, 60))
    out = []
    for f, t in sorted(when):
        no += int(r.integers(1, 6))
        tk += int(r.integers(2, 30))
        out.append(["RQ-2027Q1-%04d" % no, K.NEXT_Q, t, W.q1_request[t], ts(f), K.FIRM_INFO[t]["owner"],
                    "CAP-%d" % tk])
    return out


RATE_COLS = ["rate_id", "resource", "site", "unit", "eur_per_unit_month", "effective_from", "published_on"]
MAD1_PUBLISHED = {"2025-01-01": "2024-11-29", "2025-07-01": "2025-06-02", "2026-01-01": "2025-12-01",
                  "2026-09-01": "2026-08-03", "2027-01-01": "2026-12-01"}


def rate_rows(W):
    rid = 104
    for d, v in K.RATES:
        yield ["R%03d" % rid, "reserved core", "MAD1", "core", "%.2f" % v, d.isoformat(),
               MAD1_PUBLISHED[d.isoformat()]]
        rid += int(K.rng("rate-id", d.isoformat()).integers(2, 5))


def directory(W):
    ten = []
    for t in K.FIRM:
        i = K.FIRM_INFO[t]
        ten.append({"id": t, "class": "firm", "name": i["name"], "owner_team": i["owner"], "cost_centre": i["cc"],
                    "since": "2021-06" if t not in ("reco-serve", "ads-listings") else "2023-02"})
    ten.append({"id": "cell-ctl", "class": "platform", "name": "Cell scheduler and monitoring agents",
                "owner_team": "Compute Operations", "cost_centre": None, "since": "2021-03"})
    ten.append({"id": "cell-store", "class": "platform", "name": "Cell storage service",
                "owner_team": "Storage Platform", "cost_centre": None, "since": "2021-03"})
    ten.append({"id": "batch-train", "class": "batch", "name": "Batch training tier", "owner_team": "ML Platform",
                "cost_centre": None, "since": "2022-09",
                "teams": [{"id": x, "name": n} for x, n in (
                    ("ranking-ml", "Search ranking models"), ("pricing-ml", "Pricing models"),
                    ("fraud-ml", "Fraud and risk models"), ("reco-ml", "Recommendation models"),
                    ("demand-ml", "Demand forecasting models"), ("nlp-ml", "Language and content models"))]})
    return {"cell": "MAD1/C-22", "site": "MAD1, Alcobendas (Madrid)", "updated": "2026-12-01",
            "maintained_by": "Compute Operations", "tenants": ten}


def write_directory(path, W):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(directory(W), fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------------------------------------------- batch tier, 2026 Q3
RUNS_COLS = ["run_id", "job_id", "team", "cores", "started_utc", "ended_utc", "end_state", "resumed_from",
             "restore_checkpoint"]
CKPT_COLS = ["checkpoint_id", "run_id", "step", "write_started_utc", "committed_utc", "size_gb"]
RESIZE_COLS = ["run_id", "at_utc", "cores_before", "cores_after"]
SIZE_GB = {"ranking-ml": 38.0, "pricing-ml": 12.4, "fraud-ml": 7.6, "reco-ml": 64.0, "demand-ml": 15.2, "nlp-ml": 212.0}


def runs_rows(W):
    for rn in sorted(W.q3_runs, key=lambda x: (x["started"], x["run_id"])):
        yield [rn["run_id"], rn["job"]["job_id"], rn["team"], rn["cores"], ts(rn["started"]),
               ts(rn["ended"]) if rn["ended"] else "", rn["state"], rn["resumed_from"] or "",
               rn["restore"]["checkpoint_id"] if rn["restore"] is not None else ""]


def _job_of(W):
    return {x["run_id"]: x["job"] for x in W.all_runs}


def ckpt_rows(W):
    jobs = _job_of(W)
    for c in sorted(W.q3_ckpts, key=lambda c: (c["write_started"], c["checkpoint_id"])):
        j = jobs[c["run_id"]]
        r = K.rng("sph", j["job_id"])
        sph = WD.TEAM_STEPS_H[j["team"]] * float(r.uniform(0.85, 1.15))
        step = int(round(c["progress"] * sph / 10.0)) * 10
        size = SIZE_GB[j["team"]] * (1 + 0.004 * float(K.rng("gb", c["checkpoint_id"]).normal()))
        yield [c["checkpoint_id"], c["run_id"], step, ts(c["write_started"]),
               ts(c["committed"]) if c["committed"] else "", "%.1f" % size]


def resize_rows(W):
    for x in sorted(W.q3_resizes, key=lambda x: (x["at"], x["run_id"])):
        yield [x["run_id"], ts(x["at"]), x["cores_before"], x["cores_after"]]


# ---------------------------------------------------------------------------------------------------- machine events, 2026 Q3
MEV_COLS = ["time_utc", "machine_id", "event", "cause", "rack", "ticket"]
CM_RESTART = dt.datetime(2026, 8, 19, 9, 12, tzinfo=K.UTC)       # the cluster manager's restart after the power event


def id_at(a, t):
    cur = None
    for s, m in a["ids"]:
        if s <= t:
            cur = m
    return cur


def machine_events(W):
    """Removals and registrations in C-22 from 1 July to 30 September 2026, as the cluster manager logged them."""
    r = K.rng("mevents")
    ev = []
    hw_no = 260_418
    chg = {}
    for a in W.assets:
        for o in a["outages"]:
            s0 = o["start"]
            if not (K.Q3_START <= s0 < K.Q3_END):
                continue
            mid = id_at(a, s0)
            if o["cause"] == "hw_fault":
                hw_no += int(r.integers(1, 12))
                tk = "INC-%d" % hw_no
            else:
                key = (s0.date(), a["row"])
                if key not in chg:
                    chg[key] = "CHG-%s-%s" % (s0.strftime("%y%m%d"), a["row"])
                tk = chg[key]
            ev.append([s0, mid, "REMOVED", o["cause"], a["rack"], tk])
            if o["fate"] != "retire":
                e0 = s0 + dt.timedelta(minutes=o["minutes"])
                ev.append([e0, id_at(a, e0), "REGISTERED", "", a["rack"], ""])
        if K.Q3_START <= a["installed"] < K.Q3_END:
            ev.append([a["installed"], id_at(a, a["installed"]), "REGISTERED", "", a["rack"], ""])
    ev.sort(key=lambda x: (x[0], x[2] != "REMOVED", x[4], x[1]))
    # tickets for faults are issued in time order
    hw = [x for x in ev if x[3] == "hw_fault"]
    nums = sorted(int(x[5][4:]) for x in hw)
    for x, n in zip(hw, nums):
        x[5] = "INC-%d" % n
    rows = [[ts(t), m, e, c, rk, tk] for t, m, e, c, rk, tk in ev]
    # after its restart the cluster manager re-sent the day's removals up to the restart, as logged
    day = [x for x in rows if x[2] == "REMOVED" and x[0][:10] == "2026-08-19" and x[0] < ts(CM_RESTART)]
    out = []
    for x in rows:
        out.append(x)
        if x in day:
            out.append(list(x))
    W.mev_resent = len(day)
    return out


# ---------------------------------------------------------------------------------------------------- quota service, 2026 Q3
QCH_COLS = ["change_id", "ticket", "tenant", "delta_cores", "requested_utc", "requested_by"]
QRUN_COLS = ["run_id", "run_started_utc", "run_finished_utc", "status", "changes_applied"]


def quota_change_rows(W):
    for c in sorted(W.q3_changes, key=lambda c: c["change_id"]):
        by = "Capacity desk" if c["kind"] == "grant" else K.FIRM_INFO[c["tenant"]]["owner"]
        yield [c["change_id"], c["ticket"], c["tenant"], c["delta"], ts(c["requested"]), by]


def quota_run_rows(W):
    for i, x in enumerate(W.q3_recon):
        yield ["qr-%s" % x["started"].strftime("%Y%m%d-%H%M"), ts(x["started"]), ts(x["finished"]), "completed",
               ";".join(sorted(x["applied"]))]
