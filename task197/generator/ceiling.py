"""task197 pair ceiling, measured on the cut pack.

Part 0 weights, unchanged so builds are comparable: a landed call banks 38 (recommendation and
critical components) plus 7 (instruction following); the asks carry 55. A wrong call keeps 5 of the
recommendation weight.

The two responses are scored from DIFFERENT readings of the same pack.

  cracker  the response that landed the call. It therefore has the traverse construction, so every
           down-regulation gain is right. It ran the hygiene battery (key uniqueness, exact
           duplicates, unmatched joins, fan-out, count ties) and executed every filed sentence it
           points at: clause 2's scope, clause 4's availability, clause 5's exposure, the unit
           column on the kWh meter, the replaced metering point the event log records, the amended
           October statement and the correction rows that cancel three logged withdrawals. It does
           not find the three devices, because no sentence adjudicates one and no sweep sees one:
             A  the minute summary rows that carry the SCADA chain's one-minute average, which hide
                over-frequency episodes from a response that locates episodes from the summary
             B  the start_local field on the operator-interface rows, which reads two hours early
             C  the meter data platform's interval index, which names the period after the one the
                row carries
           Device A is the only one whose bite depends on the route a response takes, so the
           cracker is scored twice: "summary" locates episodes from the minute summary (the pack's
           index to a 97,730 row extract file, and the route the under-frequency call rewards) and
           "extracts" scans the extract rows directly and so beats device A. The gated figure is
           the worse of the two for the build, which is the extract-scanning cracker.

  mirror   the strongest response that stopped at a wrong rung: rung 0, the undisturbed level
           before each episode, which names VKF-ZWT. Every down-regulation gain is wrong on that
           baseline. It misses the three devices as well, and it does not apply the correction rows.

Every ask contributes scored figures to both rows. A figure is kept when the response's own path
lands within half the rounding unit the asking sentence states: half a per cent on a gain, half an
episode on a count, 0.05 MWh on an energy.
"""
import os, sys, json, csv, datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_WRONG = 5.0
OFFSET = dt.timedelta(hours=2)
QUAL_OVER, QUAL_SECS = 50.080, 15
LOGGED_LAG = 90                      # seconds between a window's start and the platform's log row


def rd(p):
    with open(os.path.join(TGT, p), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _local(s):
    return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")


def _utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- the pack, read once ----------
def load():
    P = {}
    P["ev"] = rd("platform/control_platform_event_log.csv")
    P["com"] = rd("platform/fcr_block_commitments.csv")
    P["prog"] = rd("platform/site_programme_15min.csv")
    P["met"] = rd("settlement/metered_volumes_15min.csv")
    ex = rd("operator/system_frequency_1s_extracts.csv")
    P["ex"] = [(_utc(r["ts_utc"]), float(r["frequency_hz"])) for r in ex]
    P["min"] = [(_utc(r["minute_utc"]), float(r["frequency_max_hz"]))
                for r in rd("operator/system_frequency_minute_summary.csv")]
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TGT, "register", "asset_register.xlsx"))
    ws = wb["Sites"]
    hdr = [c.value for c in ws[1]]
    P["reg"] = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(hdr, row))
        P["reg"][d["Site id"]] = d
    return P


def over_episodes(P):
    """Every qualifying over-frequency episode in the published extracts: (extreme utc, peak)."""
    out, run = [], []
    prev = None
    for (ts, f) in P["ex"]:
        if prev is not None and (ts - prev).total_seconds() != 1:
            run = []
        prev = ts
        if f >= QUAL_OVER:
            run.append((ts, f))
        else:
            if len(run) >= QUAL_SECS:
                out.append(max(run, key=lambda x: (x[1], -x[0].timestamp())))
            run = []
    if len(run) >= QUAL_SECS:
        out.append(max(run, key=lambda x: (x[1], -x[0].timestamp())))
    return out


def summary_visible(P):
    """The minutes a response that locates episodes from the minute summary would open."""
    return {m for (m, mx) in P["min"] if mx >= QUAL_OVER}


def commitments(P):
    """(site, local date) -> set of committed blocks, 1 based."""
    out = defaultdict(set)
    for r in P["com"]:
        out[(r["site_id"], r["delivery_date"])].add(int(r["block"]))
    return out


def windows(P, read):
    """Reserve-withdrawal windows as a response would place them.
    read "true"    : from the platform's own log timestamp, 90 s after the window opened
    read "stamped" : from the start_local field as it stands
    read "mirror"  : stamped, with the correction rows not applied
    """
    cancelled = {e["supersedes_event_id"] for e in P["ev"] if e["event_type"] == "correction"}
    out = []
    for e in P["ev"]:
        if e["event_type"] != "reserve_unavailable":
            continue
        if e["event_id"] in cancelled and read != "mirror":
            continue
        mins = int(e["duration_min"])
        if read == "true":
            start = _utc(e["logged_utc"]) - dt.timedelta(seconds=LOGGED_LAG) + OFFSET
        else:
            start = _local(e["start_local"])
        out.append((e["site_id"], start, start + dt.timedelta(minutes=mins), mins))
    return out


# ---------------------------------------------------------------- ask A ------------------------
def ask_a(P, read):
    """Episode count per site on the qualifying over-frequency episodes it was contracted for.
    read: ("true"|"stamped", "extracts"|"summary")
    """
    scope, route = read
    com = commitments(P)
    vis = summary_visible(P) if route == "summary" else None
    wins = windows(P, "true" if scope == "true" else "stamped")
    by_site = defaultdict(list)
    for (sid, a, b, m) in wins:
        by_site[sid].append((a, b))
    BLOCK = lambda t: t.hour // 4 + 1
    counts = {sid: 0 for sid in P["reg"]}
    for (ts, pk) in over_episodes(P):
        if vis is not None and ts.replace(second=0, microsecond=0) not in vis:
            continue
        loc = ts + OFFSET
        for sid in P["reg"]:
            if BLOCK(loc) not in com[(sid, loc.date().isoformat())]:
                continue
            if any(a <= loc < b for (a, b) in by_site[sid]):
                continue
            counts[sid] += 1
    return counts


# ---------------------------------------------------------------- ask B ------------------------
def ask_b(P, read):
    """Reserve capacity hours held available and the shortfall, per delivery block."""
    com = commitments(P)
    cap = {sid: float(d["Contracted FCR (MW)"]) for sid, d in P["reg"].items()}
    committed = {b: 0.0 for b in range(1, 7)}
    for (sid, d), blocks in com.items():
        for b in blocks:
            committed[b] += cap[sid] * 4.0
    lost = {b: 0.0 for b in range(1, 7)}
    for (sid, a, bnd, mins) in windows(P, read):
        b = a.hour // 4 + 1
        if read == "true" or b in com[(sid, a.date().isoformat())]:
            lost[b] += cap[sid] * mins / 60.0
    return {b: (committed[b] - lost[b], lost[b]) for b in range(1, 7)}


# ---------------------------------------------------------------- ask C ------------------------
def ask_c(P, read):
    """Energy above and below programme over the periods a site held no block commitment.
    read "golden"  : each row carries the interval that closed at its own timestamp
    read "natural" : each row carries the period its settlement_period names
    """
    com = commitments(P)
    ean = {}
    for sid, d in P["reg"].items():
        ean[str(d["Metering point (EAN)"])] = sid
    # the replaced metering point the event log records, recovered from the metered file's own codes
    codes = {r["metering_point"] for r in P["met"]}
    for e in P["ev"]:
        if e["event_type"] == "metering":
            for c in codes - set(ean):
                ean[c] = e["site_id"]
    prog = {}
    for r in P["prog"]:
        prog[(r["site_id"], _local(r["period_start_local"]))] = float(r["programme_mw"])
    above = {sid: 0.0 for sid in P["reg"]}
    below = {sid: 0.0 for sid in P["reg"]}
    for r in P["met"]:
        sid = ean.get(r["metering_point"])
        if sid is None:
            continue
        v = float(r["net_volume"]) / (1000.0 if r["unit"] == "kWh" else 1.0)
        ts = _local(r["interval_ts_local"])
        key = ts - dt.timedelta(minutes=15) if read == "golden" else ts
        if (sid, key) not in prog:
            continue
        if key.hour // 4 + 1 in com[(sid, key.date().isoformat())]:
            continue
        dv = v - prog[(sid, key)] * 0.25
        if dv >= 0:
            above[sid] += dv
        else:
            below[sid] += -dv
    return above, below


# ---------------------------------------------------------------- scoring ----------------------
def build_rows(P, F):
    gold_a = ask_a(P, ("true", "extracts"))
    gold_b = ask_b(P, "true")
    gold_c = ask_c(P, "golden")
    reads = {
        "cracker_sum": (("stamped", "summary"), "stamped", "natural"),
        "cracker_ext": (("stamped", "extracts"), "stamped", "natural"),
        "mirror": (("stamped", "summary"), "mirror", "natural"),
    }
    vals = {k: (ask_a(P, r[0]), ask_b(P, r[1]), ask_c(P, r[2])) for k, r in reads.items()}
    rows = []                            # (ask, label, unit, golden, {who: value})

    # ask A: nine gains then nine counts
    dn = {d["site"]: d for d in F["down"]}
    for sid in sorted(dn):
        g = dn[sid]["gain_pct"]
        # the construction decides the gain: the cracker has it, the mirror does not
        rows.append(("A down regulation", "down gain %s" % sid, 1.0, g,
                     {"cracker_sum": g, "cracker_ext": g,
                      "mirror": (None if g is None else g + 20.0)}))
    for sid in sorted(gold_a):
        rows.append(("A down regulation", "down episodes %s" % sid, 1.0, gold_a[sid],
                     {k: vals[k][0][sid] for k in reads}))
    # ask B: six held-available figures then six shortfalls
    for b in range(1, 7):
        rows.append(("B block availability", "available block %d" % b, 0.1, gold_b[b][0],
                     {k: vals[k][1][b][0] for k in reads}))
    for b in range(1, 7):
        rows.append(("B block availability", "shortfall block %d" % b, 0.1, gold_b[b][1],
                     {k: vals[k][1][b][1] for k in reads}))
    # ask C: nine above, nine below, two portfolio totals
    for sid in sorted(gold_c[0]):
        rows.append(("C imbalance exposure", "above programme %s" % sid, 0.1, gold_c[0][sid],
                     {k: vals[k][2][0][sid] for k in reads}))
    for sid in sorted(gold_c[1]):
        rows.append(("C imbalance exposure", "below programme %s" % sid, 0.1, gold_c[1][sid],
                     {k: vals[k][2][1][sid] for k in reads}))
    rows.append(("C imbalance exposure", "above programme portfolio", 0.1, sum(gold_c[0].values()),
                 {k: sum(vals[k][2][0].values()) for k in reads}))
    rows.append(("C imbalance exposure", "below programme portfolio", 0.1, sum(gold_c[1].values()),
                 {k: sum(vals[k][2][1].values()) for k in reads}))
    return rows


def hit(gold, got, unit):
    if gold is None or got is None:
        return gold is None and got is None
    return abs(float(got) - float(gold)) <= unit / 2.0


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    P = load()
    rows = build_rows(P, F)
    n = len(rows)
    who = ["cracker_sum", "cracker_ext", "mirror"]
    keep = {k: sum(1 for (_, _, u, g, v) in rows if hit(g, v[k], u)) for k in who}

    print("ask figures scored on the cut pack: %d" % n)
    asks = []
    for ask in ["A down regulation", "B block availability", "C imbalance exposure"]:
        sub = [r for r in rows if r[0] == ask]
        line = "  %-22s of %2d:" % (ask, len(sub))
        for k in who:
            line += "  %s %2d" % (k, sum(1 for (_, _, u, g, v) in sub if hit(g, v[k], u)))
        print(line)
        asks.append((ask, sub))
    print("  (the cracker's kept figures in ask A are the nine down-regulation gains, which the")
    print("   traverse construction decides and which no ask device moves; the separation")
    print("   assertions in checks.py prove no device row sits in the main call's population)")

    out = {}
    for k in who:
        L = keep[k] / n
        base = W_REC if k.startswith("cracker") else R_WRONG
        out[k] = (base + W_INSTR + W_ASK * L, L)
        print("%-12s %-32s %5.1f  = %.0f + %.0f + %.0f x %.3f"
              % (k, "(landed the call)" if k.startswith("cracker") else "(rung 0, named %s)"
                 % F["ladder_names"]["pre"], out[k][0], base, W_INSTR, W_ASK, L))
    pair_sum = (out["cracker_sum"][0] + out["mirror"][0]) / 2
    pair_ext = (out["cracker_ext"][0] + out["mirror"][0]) / 2
    print("pair, summary-first cracker : %.1f" % pair_sum)
    print("PAIR CEILING: %.1f   (bar 40, the worse of the two crackers)" % max(pair_sum, pair_ext))
    print("MIRROR LEAKAGE: %.1f per cent of ask weight   (bar under 35)" % (100 * out["mirror"][1]))

    print("sweep: the pair against the number of ask figures the gated cracker keeps")
    for kc in range(0, n + 1, max(1, n // 10)):
        c = W_REC + W_INSTR + W_ASK * kc / n
        m = R_WRONG + W_INSTR + W_ASK * min(kc, keep["mirror"]) / n
        print("   cracker keeps %2d of %d -> pair %.1f" % (kc, n, (c + m) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
