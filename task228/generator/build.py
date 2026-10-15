"""Write the pack under target/ from the simulated 2026 experiments."""
import csv
import json
import os
from datetime import timedelta

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import params as P
import records as R
import sim
import world as W

FILES = dict(
    standard="dh3_data_health_hold_standard.pdf",
    registry="experiment_registry_2026.json",
    q1="install_summary_2026q1.csv",
    q2="install_summary_2026q2.parquet",
    q3="install_summary_2026q3.parquet",
    register="data_incident_register_2026.xlsx",
    recon="reconciliation_summary_2026.pdf",
    review="weekly_review_log_2026.csv",
    dictionary="data_dictionary.md",
    changes="platform_change_log_2026.md",
    collector="collector_daily_2026.csv",
    releases="app_releases_2026.csv",
    bookings="booking_queue_2027q1.csv",
    manifest="export_manifest.csv",
)
DISTRACTORS = ["collector", "releases", "bookings"]
OS_OLD = {"ios": "iOS", "android": "Android", "web": "Web"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(["" if r[h] is None else r[h] for h in header])
    return len(rows)


def installs(exps, data, rng):
    """one table a quarter: experiment, install, arm, platform and the install's counts"""
    out = {"q1": [], "q2": [], "q3": []}
    for e, (c, t) in zip(exps, data):
        q = R.export_of(e)
        for arm, a in (("control", c), ("treatment", t)):
            ids = R.install_ids(rng, len(a["sess"]))
            out[q].append(dict(key=[e["key"]] * len(ids), id=ids, arm=[arm] * len(ids),
                               plat=[P.PLATFORMS[i] for i in a["plat"]], sess=a["sess"], gaps=a["gaps"], dups=a["dups"],
                               lates=a["lates"], ev=a["ev"]))
    tabs = {}
    for q, parts in out.items():
        cols = {k: (np.concatenate([p[k] for p in parts]) if k in ("sess", "gaps", "dups", "lates", "ev")
                    else sum((list(p[k]) for p in parts), [])) for k in parts[0]}
        order = sorted(range(len(cols["id"])), key=lambda i: (cols["key"][i], cols["id"][i]))
        tabs[q] = {k: ([v[i] for i in order] if isinstance(v, list) else v[order]) for k, v in cols.items()}
    return tabs


def write_installs(target, tabs):
    counts = {}
    t = tabs["q1"]
    path = os.path.join(target, FILES["q1"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["exp_id", "install", "variant", "os", "n_sessions", "sessions_seq_gap", "sessions_dup_ids",
                    "sessions_late", "events"])
        for i in range(len(t["id"])):
            w.writerow([t["key"][i], t["id"][i], "A" if t["arm"][i] == "control" else "B", OS_OLD[t["plat"][i]],
                        int(t["sess"][i]), int(t["gaps"][i]), int(t["dups"][i]), int(t["lates"][i]), int(t["ev"][i])])
    counts["q1"] = len(t["id"])
    for q in ("q2", "q3"):
        t = tabs[q]
        tab = pa.Table.from_arrays([pa.array(t["key"], pa.string()), pa.array(t["id"], pa.string()),
                                    pa.array(t["arm"], pa.string()), pa.array(t["plat"], pa.string()),
                                    pa.array(t["sess"].astype(np.int32), pa.int32()),
                                    pa.array(t["gaps"].astype(np.int32), pa.int32()),
                                    pa.array(t["dups"].astype(np.int32), pa.int32()),
                                    pa.array(t["lates"].astype(np.int32), pa.int32()),
                                    pa.array(t["ev"].astype(np.int32), pa.int32())],
                                   names=["experiment_key", "install_id", "arm", "platform", "sessions", "gap_sessions",
                                          "duplicate_sessions", "late_sessions", "events_received"]).replace_schema_metadata(None)
        pq.write_table(tab, os.path.join(target, FILES[q]), compression="snappy", row_group_size=131072,
                       use_dictionary=True, write_statistics=True, store_schema=False)
        counts[q] = len(t["id"])
    return counts


def recon_rows(exps, rng):
    rows = []
    for e in exps:
        if not e.get("incident_id"):
            continue
        final = "confirmed" if e["kind"] != "clean" else "not confirmed"
        server = int(e["t_ev"] * float(rng.uniform(0.16, 0.20)))
        k = e["kind"]
        fac = {"loss": rng.uniform(0.955, 0.985), "dup": rng.uniform(1.02, 1.045), "late": rng.uniform(0.997, 0.9995),
               "consent": rng.uniform(0.996, 0.9995)}.get(k, rng.uniform(0.9985, 1.0012))
        rd = R.recon_date(e)
        rows.append(dict(month="%s 2026" % MONTHS[e["end"].month - 1], month_no=e["end"].month, key=e["key"],
                         title=e["title"], server=server, telemetry=int(server * float(fac)), finding=final,
                         cause=W.KIND_TYPE[k] if k != "clean" else "", recon=rd))
    rows.sort(key=lambda r: (r["month_no"], r["key"]))
    return rows


def run(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    exps, data, tries = sim.corpus(seed)
    for e, (c, t) in zip(exps, data):
        e["t_ev"] = int(t["ev"].sum())
    rng = np.random.default_rng(seed + 7)
    reg = R.registry(exps, rng)
    R.incidents(exps, rng)
    app = R.app_wide(rng)
    rows, ids = R.register_rows(exps, rng, app)
    for a in app:
        for ln in a["lines"]:
            rows.append(dict(incident_id=a["incident_id"], opened=a["opened"], closed=a["closed"], scope="app-wide",
                             experiment=None, platform=ln["platform"], incident_type=a["first_call"], status="confirmed",
                             status_date=(R.datetime.strptime(a["closed"], "%Y-%m-%d %H:%M") + timedelta(days=9)).strftime("%Y-%m-%d"),
                             sessions_in_window=ln["sessions"], gap_sessions=a["gap"], notes=a["note"]))
    rows.sort(key=lambda r: (r["opened"], r["incident_id"], {"preliminary": 0, "confirmed": 1, "withdrawn": 1}[r["status"]],
                             r["platform"] or ""))
    counts = {}
    with open(os.path.join(target, FILES["registry"]), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"pulled": "2026-10-12T06:00:00+02:00", "source": "Avisly experiment platform", "experiments": reg}, f,
                  indent=2, ensure_ascii=False)
        f.write("\n")
    counts["registry"] = len(reg)
    tabs = installs(exps, data, rng)
    counts.update(write_installs(target, tabs))
    docs.register(os.path.join(target, FILES["register"]), rows)
    counts["register"] = len(rows)
    rr = recon_rows(exps, rng)
    docs.reconciliation(os.path.join(target, FILES["recon"]), rr)
    rv = R.review_log(exps, rng)
    counts["review"] = write_csv(os.path.join(target, FILES["review"]),
                                 ["review_week", "logged_at_utc", "experiment_key", "action", "reviewer", "comment"], rv)
    cd = R.collector_daily(rng)
    counts["collector"] = write_csv(os.path.join(target, FILES["collector"]), list(cd[0].keys()), cd)
    ar = R.app_releases(rng)
    counts["releases"] = write_csv(os.path.join(target, FILES["releases"]), list(ar[0].keys()), ar)
    bq = R.booking_queue(rng)
    counts["bookings"] = write_csv(os.path.join(target, FILES["bookings"]), list(bq[0].keys()), bq)
    docs.standard(os.path.join(target, FILES["standard"]))
    docs.markdown(target, FILES)
    write_manifest(os.path.join(target, FILES["manifest"]), counts)
    return dict(exps=exps, data=data, tries=tries, app=app, register=rows, recon=rr, review=rv, counts=counts, tabs=tabs)


def write_manifest(path, counts):
    desc = [
        ("standard", "DH-3 data-health hold for experiment readouts, version 1.0", "Experimentation Platform"),
        ("registry", "Experiment registry: experiments started in 2026", "Experiment platform"),
        ("q1", "Install export, experiments started 5 January to 30 March 2026 (scorecard service 1)", "Scorecard service 1"),
        ("q2", "Install export, experiments started 6 April to 29 June 2026 (scorecard service 2)", "Scorecard service 2"),
        ("q3", "Install export, experiments started 6 July to 14 September 2026 (scorecard service 2)", "Scorecard service 2"),
        ("register", "Data incident register 2026", "Data-health desk"),
        ("recon", "Telemetry reconciliation summary, January to September 2026", "Data-health desk"),
        ("review", "Weekly review log, 12 January to 5 October 2026", "Data-health desk"),
        ("dictionary", "Data dictionary for these files", "Data-health desk"),
        ("changes", "Experiment platform change log 2026", "Experimentation Platform"),
        ("collector", "Collector daily totals by platform, 1 January to 11 October 2026", "Collector"),
        ("releases", "App releases 2026 with SDK versions", "Mobile release management"),
        ("bookings", "Experiments booked for January to March 2027", "Experiment platform"),
    ]
    rows = [dict(file=FILES[k], description=d, rows=counts.get(k, ""), source=s, pulled="2026-10-12") for k, d, s in desc]
    write_csv(path, ["file", "description", "rows", "source", "pulled"], rows)
