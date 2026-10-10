"""The two supplemental asks, their data files and their golden answers.

Ask A (patch pace): per estate, the median days from a vendor's first release of a fix to the day
the ticket's last host ran it, over tickets completed 1 May to 23 October (one decimal), and how
many of those tickets missed the 35-day remediation target. Primary device: rolled-back
deployments in the crew log (the first run is not the fix landing; the re-deploy is).

Ask B (scanner coverage): per cloud estate, hosts in service on 23 October and how many had no
authenticated scan in the 14 days before the export. Primary device: the media domain migration,
whose renamed hosts keep their recent scans under the old hostname, so a hostname join counts them
unscanned; the instance id is the stable key.
"""
import datetime as dt
import random
import statistics

from params import ESTATES, CLOUD, LABEL, TARGET_DAYS, AS_OF, MEDIA_OLD_DOMAIN

PKG_POOL = ["openssl", "nginx", "python3.11", "openjdk-17-jre-headless", "curl", "libxml2",
            "systemd", "redis-server", "kafka", "containerd", "elasticsearch", "ffmpeg"]


def build_asks(seed, chosts):
    """Return (deployments, coverage_rows, asset_rows, answer_A, answer_B). Deterministic."""
    rng = random.Random(seed + 40)
    deployments = []          # one row per host-run in the crew/completion log
    tickets = []              # (ticket_id, estate, package, vendor_release, gap_days, missed)
    tnum = 0
    for est in ESTATES:
        ntk = rng.randint(22, 34)
        for _ in range(ntk):
            tnum += 1
            tid = f"DEP-{est[:3].upper()}-{tnum:04d}"
            pkg = rng.choice(PKG_POOL)
            rel = dt.date(2026, rng.randint(4, 9), rng.randint(1, 27))
            gap = max(2, int(round(random.Random(tnum * 7 + seed).gauss(24, 11))))
            last_run = rel + dt.timedelta(days=gap)
            if last_run > AS_OF:
                last_run = AS_OF
                gap = (last_run - rel).days
            rolled_back = rng.random() < 0.30
            # the first run is earlier; a rollback means it did not land then, the re-deploy did
            first_run = last_run - dt.timedelta(days=rng.randint(3, 9)) if rolled_back else last_run
            nhost = rng.randint(3, 20)
            for k in range(nhost):
                hrun = last_run if k == nhost - 1 else last_run - dt.timedelta(days=rng.randint(0, 4))
                deployments.append({"ticket": tid, "estate": est, "package": pkg,
                                    "vendor_first_release": rel.isoformat(),
                                    "run_date": hrun.isoformat(),
                                    "outcome": "succeeded", "is_last_host": k == nhost - 1})
            if rolled_back:
                deployments.append({"ticket": tid, "estate": est, "package": pkg,
                                    "vendor_first_release": rel.isoformat(),
                                    "run_date": first_run.isoformat(),
                                    "outcome": "rolled_back", "is_last_host": False})
            tickets.append((tid, est, pkg, rel, gap, gap > TARGET_DAYS))
    # ---- answer A: median gap and miss count per estate (gap = last successful host run - release)
    ans_A = {}
    for est in ESTATES:
        gaps = [g for (_, e, _, _, g, _) in tickets if e == est]
        miss = sum(1 for (_, e, _, _, _, m) in tickets if e == est and m)
        med = round(statistics.median(gaps), 1)
        ans_A[est] = {"median_days": med, "tickets_missed": miss, "n_tickets": len(gaps)}

    # ---- ask B data: coverage rows and asset register
    coverage, assets = [], []
    ans_B = {}
    boundary = dt.date(2026, 10, 9)   # 14 days before the 23 October export, Madrid local
    for est in CLOUD:
        serving = [h for h in chosts[est] if not h.stopped and not h.standby]
        unscanned = 0
        for h in serving:
            scanned_recent = h.last_scan is not None and h.last_scan >= boundary
            if not scanned_recent:
                unscanned += 1
        ans_B[est] = {"in_service": len(serving), "unscanned_14d": unscanned}
    for est in CLOUD:
        for h in chosts[est]:
            assets.append([h.iid, h.hostname, est, LABEL[est],
                           "standby" if h.standby else ("stopped" if h.stopped else "running")])
            # coverage keyed by the name in effect at the scan: migrated media hosts under old name
            name = h.renamed_from if (h.renamed_from and est == "media") else h.hostname
            ls = h.last_scan.isoformat() if h.last_scan else ""
            coverage.append([name, h.iid, est, ls])
    assets.sort(key=lambda r: (r[2], r[0]))
    coverage.sort(key=lambda r: (r[2], r[1]))
    deployments.sort(key=lambda d: (d["estate"], d["ticket"], d["run_date"]))
    return deployments, coverage, assets, ans_A, ans_B
