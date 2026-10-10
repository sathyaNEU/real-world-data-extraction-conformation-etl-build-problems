"""Writers for the data files of the pack. Every file is written deterministically (sorted rows,
fixed column order) so two builds are byte-identical.
"""
import csv
import datetime as dt
import json

import pyarrow as pa
import pyarrow.parquet as pq
import openpyxl

from params import COLO, CLOUD, LABEL, CODE, AS_OF
from cves import score_rows

SPINE = "vuln_findings_2026-10-23.csv"
HISTORY = "epss_score_history_2026.parquet"
FEED = "colocation_managed_host_findings_2026-10-23.jsonl"
INVENTORY = "colocation_host_inventory_2026-10-23.xlsx"
CAPREG = "colocation_capacity_register_2026-10.xlsx"
FORECAST = "estate_transaction_forecast_2026.csv"
ACKS = "colocation_change_acknowledgements_may_oct_2026.xlsx"
TICKETLOG = "cloud_patch_ticket_log_q3_2026.csv"
FIXEDF = "cloud_q3_fixed_findings.csv"
DEPLOYLOG = "crew_deployment_log_2026.csv"
COMPLETION = "colocation_completion_reports_2026.csv"
ADVISORY = "vendor_advisory_feed.json"
ASSETREG = "cloud_asset_register_2026-10-23.csv"
COVERAGE = "scanner_coverage_2026-10.csv"
DRAINTOOL = "drain_orchestrator_config.yaml"


def _w(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)


def write_spine(path, W):
    rows = sorted(W["spine"], key=lambda r: (r["estate"], r["host"], r["package"], r["cve"]))
    out = [[r["host"], r["estate"], r["domain"], r["package"], r["cve"], f'{r["cvss"]:.1f}',
            "true" if r["exploit_flag"] else "false", r["first_seen"].isoformat(),
            r["last_scan"].isoformat() if r["last_scan"] else ""] for r in rows]
    _w(path, ["host_id", "estate", "hostname_suffix", "package", "cve", "cvss_base",
              "exploit_available", "first_seen", "last_authenticated_scan"], out)
    return len(out)


def write_history(path, W):
    """Daily EPSS scores for every cloud and close-out CVE referenced by a shipped finding."""
    ref = set(r["cve"] for r in W["spine"]) | set(r["cve"] for r in W["fixed"])
    reg = W["reg"]
    rng = W["rng"]
    import random
    hrng = random.Random(7)
    series = score_rows_for(reg, ref, hrng)
    cols = {"cve": [], "score_date": [], "epss": []}
    for cid in sorted(series):
        for d, s in series[cid]:
            cols["cve"].append(cid)
            cols["score_date"].append(d.isoformat())
            cols["epss"].append(round(s, 5))
    t = pa.table(cols)
    pq.write_table(t, path, compression="snappy")
    return len(cols["cve"])


def score_rows_for(reg, ids, rng):
    """score_rows restricted to the referenced ids, deterministic."""
    sub = type(reg)(rng)
    sub.by_id = {cid: reg.by_id[cid] for cid in ids if cid in reg.by_id}
    return score_rows(sub, rng)


def write_feed(path, W):
    """Provider managed-host findings feed (current state), one JSON object per line."""
    lines = []
    reg = W["reg"]
    for est in COLO:
        for h in W["hosts"][est]:
            for pkg, cve in h.findings:
                c = reg.by_id.get(cve)
                score = c.final if c else 0.42
                fs = (h.in_service + dt.timedelta(days=3)).isoformat()
                lines.append((est, h.hid, pkg, cve, round(max(score, 0.105), 5), fs))
    lines.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for est, hid, pkg, cve, score, fs in lines:
            f.write(json.dumps({"estate": est, "host_id": hid, "package": pkg, "cve": cve,
                                "epss": score, "first_seen": fs}, sort_keys=True) + "\n")
    return len(lines)


def _xlsx(path, sheets):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, header, rows in sheets:
        ws = wb.create_sheet(name)
        ws.append(header)
        for r in rows:
            ws.append(r)
    wb.save(path)


def write_inventory(path, W):
    rows = []
    for est in COLO:
        for h in W["hosts"][est]:
            rows.append([h.hid, est, LABEL[est], h.pool, h.role, h.in_service.isoformat()])
    rows.sort(key=lambda r: (r[1], r[0]))
    _xlsx(path, [("Hosts", ["host_id", "estate", "estate_label", "pool", "role", "in_service_since"],
                  rows)])
    return len(rows)


def write_forecast(path, W, seed):
    """Hourly transactions-per-second forecast for the two colocated estates, May to November.

    On a window date the window-hours peak gives the concurrent drains; on separator windows a
    daytime hour peaks higher, which is what the day's-peak reading (R2) reads instead.
    """
    import random
    from params import TPS, N_BY_MONTH, WINDOWS, NOV_OFFICE
    import windows as WIN
    peaks = WIN.forecast_peaks(random.Random(seed + 20))
    nov = WIN.nov_office_peaks()
    header = ["estate", "date", "hour", "tps"]
    rows = []
    for est in COLO:
        per = TPS[est]
        pastmap = {d: (wp, dp) for d, (wp, dp, c, nd, n) in peaks[est].items()}
        novmap = {d: (wp, dp) for d, wp, dp in nov[est]}
        (wa, wb), start, length = WINDOWS[est]
        whours = [(start + k) % 24 for k in range(length)]
        d = dt.date(2026, 5, 1)
        while d <= dt.date(2026, 11, 30):
            n = N_BY_MONTH[est][d.month]
            base = (n - 60) * per
            wp = dp = None
            if d in pastmap:
                wp, dp = pastmap[d]
            elif d in novmap:
                wp, dp = novmap[d]
            for h in range(24):
                v = base * (0.6 + 0.08 * (1 if 8 <= h <= 20 else 0))
                if wp is not None and h in whours:
                    v = wp if h == whours[1] else wp * 0.88
                if dp is not None and h == 12:
                    v = max(v, dp)
                rows.append([est, d.isoformat(), h, f"{v:.1f}"])
            d += dt.timedelta(days=1)
    _w(path, header, rows)
    return len(rows)


def write_capreg(path, W):
    """Capacity register: per colocated estate, hosts in service by month, per-host throughput, the
    rack (failure-domain) size and the 30-minute drain cycle count per 4-hour window."""
    from params import N_BY_MONTH, TPS, RACK
    rows = []
    for est in COLO:
        for m in range(5, 12):
            rows.append([est, LABEL[est], f"2026-{m:02d}", N_BY_MONTH[est][m], f"{TPS[est]:.1f}",
                         RACK, 8])
    _xlsx(path, [("Capacity", ["estate", "estate_label", "month", "hosts_in_service",
                               "per_host_tps", "failure_domain_hosts", "drain_cycles_per_window"],
                  rows)])
    return len(rows)


def write_acks(path, W):
    """The provider's change-request acknowledgements, May to October."""
    rows = []
    for r in W["requests"]:
        status = "accepted" if r["accepted"] == r["requested"] else (
            "part-accepted" if r["accepted"] > 0 else "declined")
        reason = "" if status == "accepted" else "window concurrent-drain limit reached"
        hosts = " ".join(r["hosts"][:r["requested"]])
        rows.append([r["rid"], r["estate"], r["date"].isoformat(), r["hours"], r["team"], r["order"],
                     r["requested"], r["accepted"], status, reason, hosts])
    rows.sort(key=lambda x: (x[1], x[2], x[5]))
    _xlsx(path, [("Acknowledgements",
                  ["request_id", "estate", "window_date", "window_hours_local", "team",
                   "submission_order", "hosts_requested", "hosts_accepted", "status", "reason",
                   "host_ids"], rows)])
    return len(rows)


def write_ticketlog(path, W):
    """Q3 cloud patch tickets, one row per ticket, with cut and completion dates."""
    from collections import defaultdict
    g = defaultdict(list)
    for r in W["fixed"]:
        g[r["ticket"]].append(r)
    rows = []
    for tid, rs in g.items():
        r0 = rs[0]
        comp = r0["cut"] + dt.timedelta(days=7 + (len(rs) % 11))
        rows.append([tid, r0["estate"], r0["package"], r0["cut"].isoformat(), comp.isoformat(),
                     len(rs), "completed"])
    rows.sort(key=lambda x: (x[1], x[3], x[0]))
    _w(path, ["ticket_id", "estate", "package", "cut_date", "completed_date", "hosts_fixed",
              "status"], rows)
    return len(rows)


def write_fixed(path, W):
    """The findings each Q3 ticket closed; the close-out figures recompute from these against the
    score history at each ticket's cut day."""
    rows = [[r["ticket"], r["estate"], r["host"], r["package"], r["cve"], r["cut"].isoformat()]
            for r in W["fixed"]]
    rows.sort(key=lambda x: (x[1], x[0], x[2], x[4]))
    _w(path, ["ticket_id", "estate", "host_id", "package", "cve", "cut_date"], rows)
    return len(rows)


def write_draintool(path):
    """Distractor: the drain orchestrator's configuration. Its max_parallel_drains is a tool limit,
    not the window headroom, and it never binds."""
    text = (
        "# Centro de Datos Guadalhorce - drain orchestrator configuration\n"
        "# Managed service configuration, revision 2026-07. Applies to all colocated estates.\n"
        "orchestrator:\n"
        "  version: \"4.3.1\"\n"
        "  cycle_minutes: 30\n"
        "  max_parallel_drains: 7        # tool concurrency ceiling per estate\n"
        "  rebuild_from: current_platform_image\n"
        "  health_gate: true\n"
        "  retries: 2\n"
        "estates:\n"
        "  payments: {queue: payments-drain, priority: high}\n"
        "  checkout: {queue: checkout-drain, priority: high}\n"
        "notes: >\n"
        "  The orchestrator concurrency is a safety ceiling on simultaneous drains. The number of\n"
        "  drains a window can actually run is set by the estate's headroom over the forecast peak,\n"
        "  not by this value.\n"
    )
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_deploylog(path, deployments):
    rows = [[d["ticket"], d["estate"], d["package"], d["vendor_first_release"], d["run_date"],
             d["outcome"], "true" if d["is_last_host"] else "false"] for d in deployments]
    _w(path, ["ticket_id", "estate", "package", "vendor_first_release", "run_date", "outcome",
              "is_last_host"], rows)
    return len(rows)


def write_assetreg(path, assets):
    _w(path, ["instance_id", "hostname", "estate", "estate_label", "power_state"], assets)
    return len(assets)


def write_coverage(path, coverage):
    _w(path, ["hostname", "instance_id", "estate", "last_authenticated_scan"], coverage)
    return len(coverage)


def write_advisory(path, deployments):
    """Vendor advisory feed: first release and a later republished revision for each package."""
    seen = {}
    for d in deployments:
        seen.setdefault(d["package"], d["vendor_first_release"])
    out = []
    for pkg, rel in sorted(seen.items()):
        y, m, day = map(int, rel.split("-"))
        rev = dt.date(y, m, day) + dt.timedelta(days=21)
        out.append({"package": pkg, "first_published": rel, "latest_revision": rev.isoformat(),
                    "advisory": f"CDG-ADV-{pkg[:4].upper()}-2026"})
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")
    return len(out)


NOVCAL = "november_window_calendar.csv"


def write_novcal(path):
    """The November maintenance windows booked to the office, machine-readable beside the schedule
    PDF: one row per estate-window, with the local window hours."""
    from params import NOV_OFFICE, WINDOWS
    rows = []
    for est in COLO:
        (wa, wb), start, length = WINDOWS[est]
        hours = f"{start:02d}:00-{(start+length) % 24:02d}:00"
        for d in NOV_OFFICE[est]:
            rows.append([est, d.isoformat(), hours, length * 2])
    rows.sort(key=lambda r: (r[0], r[1]))
    _w(path, ["estate", "window_date", "window_hours_local", "drain_cycles"], rows)
    return len(rows)
