"""The files the three supplemental asks run on. None of them carries an evening shortfall."""
import datetime as dt
import json
import os
import random

import pack
import sim
import world as W

# the peers the edge bills, and the ports each holds in the quarter
# (peer, its ports, the commitment in force at the quarter's start, euros per megabit a second for
# the quarter). The three smallest interconnects peer settlement free and carry no commitment.
BILLED = [
    ("Noordlijn Transit", ["TRN-A1", "TRN-A2"], 540, 5.40),
    ("Grensweg Carrier", ["TRN-B1", "TRN-B2"], 250, 7.20),
    ("Zandpoort IX", ["TRN-C1"], 72, 9.30),
    ("Kabelnet Zuid", ["KZD-01"], 196, 5.85),
    ("Vastnet", ["VSN-01"], 205, 6.15),
    ("Delfzicht Breedband", ["DLF-01"], 124, 6.75),
    ("Rhenia Telecom", ["RHN-01"], 130, 7.05),
]
SAMPLE_MINUTES = 5
BUILDS = [
    ("4.16.0", "b-41600", dt.date(2026, 11, 3), dt.date(2027, 1, 19)),
    ("4.17.0", "b-41700", dt.date(2027, 1, 20), dt.date(2027, 2, 8)),
    ("4.18.0", "b-41800", dt.date(2027, 2, 9), dt.date(2027, 2, 22)),
    ("4.18.1", "b-41810", dt.date(2027, 2, 23), dt.date(2027, 3, 5)),
    ("4.18.0", "b-41806", dt.date(2027, 3, 6), dt.date(2027, 3, 17)),   # the number reissued
    ("4.19.0", "b-41900", dt.date(2027, 3, 18), dt.date(2027, 3, 31)),
]
CAUSES = [("access network", "outside"), ("transit provider", "outside"),
          ("customer premises", "outside"), ("power or facility", "outside"),
          ("origin service", "inside"), ("packager", "inside"), ("edge cache", "inside"),
          ("client application", "inside"), ("configuration change", "inside")]
RESTORE_STANDARD_HOURS = 4


def write_edge(target):
    """the edge's five-minute traffic samples, one row per port per sample"""
    rng = random.Random(W.SEED + 23)
    peak = {"TRN-A1": 331, "TRN-A2": 318, "TRN-B1": 172, "TRN-B2": 166, "TRN-C1": 88,
            "KZD-01": 236, "VSN-01": 197, "DLF-01": 158, "RHN-01": 141,
            "STR-01": 74, "OPL-01": 69, "HVT-01": 63}
    rows = []
    day = W.Q_FROM
    while day <= W.Q_TO:
        for code in sorted(peak):
            base = peak[code] * (0.97 + 0.06 * rng.random())
            for m in range(0, 24 * 60, SAMPLE_MINUTES):
                h = m // 60
                shape = 0.28 + 0.72 * (0.5 - 0.5 * __import__("math").cos(
                    2 * 3.141592653589793 * ((h - 4) % 24) / 24.0)) ** 1.7
                if 19 <= h < 23:
                    shape *= 1.18
                v = base * shape * (0.94 + 0.12 * rng.random())
                stamp = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=m) \
                    - dt.timedelta(hours=1 if day < W.DST_SPRING else 2)
                rows.append([stamp.strftime("%Y-%m-%dT%H:%M:%SZ"), code,
                             "%.1f" % v, "%.1f" % (v * (0.012 + 0.006 * rng.random()))])
        day += dt.timedelta(days=1)
    rows.sort(key=lambda r: (r[0], r[1]))
    return pack._csv(os.path.join(target, pack.FILES["edge"]),
                     ["sampled_at_utc", "port_code", "out_mbps", "in_mbps"], rows)


def write_commitments(target):
    rows = []
    for peer, ports, commit, rate in BILLED:
        rows.append([peer, commit, "%.2f" % rate, "AGR-%04d" % (1200 + len(rows) * 7),
                     "2026-01-01"])
    pack._csv(os.path.join(target, pack.FILES["commit"]),
              ["peer", "commitment_mbps", "rate_eur_per_mbps", "agreement_ref",
               "in_force_from"], rows)
    # one peer's commitment was amended inside the quarter, and one amendment was never accepted
    am = [["AGR-1207", "Grensweg Carrier", 250, 326, "2027-02-01", "2027-01-24", "accepted"],
          ["AGR-1200", "Noordlijn Transit", 540, 672, "2027-03-01", "", "delivered, not accepted"],
          ["AGR-1221", "Vastnet", 205, 183, "2026-10-01", "2026-09-19", "accepted"]]
    pack._csv(os.path.join(target, pack.FILES["amend"]),
              ["agreement_ref", "peer", "commitment_mbps_before", "commitment_mbps_after",
               "effective_from", "accepted_on", "status"], am)
    rng = random.Random(W.SEED + 29)
    cr = []
    for i, (peer, ports, commit, rate) in enumerate(BILLED):
        if i % 3:
            continue
        cr.append(["CRD-%04d" % (400 + i), peer, "2027-02-%02d" % (4 + i),
                   "%.2f" % round(180 + rng.random() * 900, 2),
                   "credit for the January service incident"])
    pack._csv(os.path.join(target, pack.FILES["credits"]),
              ["credit_ref", "peer", "credited_on", "amount_eur", "reason"], cr)
    return am


def write_sessions(target):
    rng = random.Random(W.SEED + 31)
    srows, rrows = [], []
    day = W.Q_FROM
    while day <= W.Q_TO:
        live = [b for b in BUILDS if b[2] <= day <= b[3]]
        if not live:
            live = [BUILDS[0]]
        for version, ref, frm, to in live:
            n = int(420000 * (0.9 + 0.2 * rng.random()) / len(live))
            srows.append([day.isoformat(), version, n])
            share = 0.021 + 0.019 * rng.random()
            if ref == "b-41800":
                share += 0.028            # the build that was rolled back
            rrows.append([day.isoformat(), version, int(n * share)])
        day += dt.timedelta(days=1)
    pack._csv(os.path.join(target, pack.FILES["sessions"]),
              ["session_date_local", "build_version", "sessions"], srows)
    pack._csv(os.path.join(target, pack.FILES["rebuffer"]),
              ["session_date_local", "build_version", "sessions_with_rebuffer"], rrows)
    out = {"product": "%s client" % W.PLATFORM,
           "note": "One version number was issued twice. A build is the reference, not the number.",
           "builds": [{"build_ref": r, "build_version": v,
                       "rolled_out_from": f.isoformat(), "rolled_out_to": t.isoformat()}
                      for v, r, f, t in BUILDS]}
    with open(os.path.join(target, pack.FILES["releases"]), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    return srows, rrows


def write_incidents(target):
    rng = random.Random(W.SEED + 37)
    inc, res = [], []
    n = 0
    day = W.Q_FROM
    while day <= W.Q_TO:
        for _ in range(rng.randrange(0, 4)):
            n += 1
            ref = "INC-%05d" % (4100 + n)
            opened = dt.datetime(day.year, day.month, day.day,
                                 rng.randrange(0, 24), rng.randrange(0, 60))
            cause, side = CAUSES[rng.randrange(0, len(CAUSES))]
            # the ticket is closed well after service came back
            rest_h = max(0.2, rng.lognormvariate(0.9, 0.8))
            closed = opened + dt.timedelta(hours=rest_h + max(0.5, rng.lognormvariate(1.5, 0.9)))
            inc.append([ref, opened.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        closed.strftime("%Y-%m-%dT%H:%M:%SZ"), cause,
                        ["P1", "P2", "P3"][rng.randrange(0, 3)],
                        ["network", "streaming", "platform"][rng.randrange(0, 3)]])
            if rng.random() < 0.82:       # the rest never had a restoration time recorded
                res.append([ref, (opened + dt.timedelta(hours=rest_h))
                            .strftime("%Y-%m-%dT%H:%M:%SZ"),
                            W.PEOPLE["ops"] if rng.random() < 0.4 else "duty engineer"])
        day += dt.timedelta(days=1)
    pack._csv(os.path.join(target, pack.FILES["incidents"]),
              ["incident_ref", "opened_at_utc", "ticket_closed_at_utc", "cause_category",
               "severity", "queue"], inc)
    pack._csv(os.path.join(target, pack.FILES["restored"]),
              ["incident_ref", "service_restored_at_utc", "recorded_by"], res)
    return inc, res


def write_distractors(target):
    rng = random.Random(W.SEED + 41)
    cat = []
    for genre in ("drama", "comedy", "documentary", "children", "sport", "film", "news"):
        for m in ("2027-01", "2027-02", "2027-03"):
            cat.append([genre, m, int(1200 + rng.random() * 9000),
                        "%.1f" % round(0.4 + rng.random() * 3.1, 1)])
    pack._csv(os.path.join(target, pack.FILES["catalogue"]),
              ["genre", "month", "titles_available", "hours_added_000"], cat)
    pops = ("Amsterdam", "Rotterdam", "Eindhoven", "Groningen", "Maastricht")
    ch = []
    for pop in pops:
        for m in ("2027-01", "2027-02", "2027-03"):
            ch.append([pop, m, "%.3f" % round(0.936 + rng.random() * 0.058, 3),
                       int(40 + rng.random() * 260)])
    pack._csv(os.path.join(target, pack.FILES["cache"]),
              ["point_of_presence", "month", "cache_hit_ratio", "egress_tb"], ch)
