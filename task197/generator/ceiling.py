"""task197 pair ceiling, measured on the cut pack.

Part 0 weights: a landed call banks 38 (recommendation and critical components) plus 7
(instruction following); the asks carry 55. The cracker is the response that landed the call, ran
the hygiene battery and executed every filed sentence it points at; the mirror is the strongest
response that stopped at a wrong rung (rung 0, the undisturbed level, which names Zwartewater).

Each ask row is scored figure by figure on the cut pack: a figure is kept when the response's own
path lands within half the rounding unit the asking sentence states. The two rows are scored from
different readings: the cracker handles every documented convention (the kWh meter, the amended
statement, the replaced metering point, the superseded corrections) and the mirror does not.
"""
import os, sys, json, csv, sqlite3, datetime as dt, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_WRONG = 5.0          # recommendation weight a wrong call keeps
OFFSET = dt.timedelta(hours=2)

def rd(p):
    with open(os.path.join(TGT, p), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    asks = []

    # ---- ask A: down regulation, 9 gains and 9 counts -------------------------------------
    gold = {d["site"]: (d["gain_pct"], d["episodes"]) for d in F["down"]}
    # the archive holds one delivery date's recordings twice after the storage-fault restore; a
    # response that averages per recording rather than per episode double counts those episodes
    con = sqlite3.connect(os.path.join(TGT, "platform", "vkf_highres_archive.sqlite"))
    dups = con.execute("""SELECT site_id, start_utc, count(*) c FROM recording
                          GROUP BY site_id, start_utc HAVING c > 1""").fetchall()
    con.close()
    dup_sites = {d[0] for d in dups}
    rowsA = []
    for sid, (g, n) in sorted(gold.items()):
        moved = sid in dup_sites
        rowsA.append(("down gain %s" % sid, not moved, not moved))
        rowsA.append(("down count %s" % sid, not moved, not moved))
    asks.append(("A down regulation", rowsA))

    # ---- ask B: block availability --------------------------------------------------------
    ev = rd("platform/control_platform_event_log.csv")
    cancelled = {e["supersedes_event_id"] for e in ev if e["event_type"] == "correction"}
    live = [e for e in ev if e["event_type"] == "reserve_unavailable" and e["event_id"] not in cancelled]
    allrows = [e for e in ev if e["event_type"] == "reserve_unavailable"]
    cap = {r["site_id"]: float(r["committed_mw"]) for r in rd("platform/fcr_block_commitments.csv")}
    def shortfall(rows):
        out = defaultdict(float)
        for e in rows:
            b = int(dt.datetime.strptime(e["start_local"][:19], "%Y-%m-%dT%H:%M:%S").hour // 4) + 1
            out[b] += cap[e["site_id"]] * int(e["duration_min"]) / 60.0
        return out
    s_gold, s_naive = shortfall(live), shortfall(allrows)
    rowsB = []
    for b in range(1, 7):
        moved = abs(s_gold[b] - s_naive[b]) > 0.05
        rowsB.append(("availability committed block %d" % b, True, True))      # no device on the committed side
        rowsB.append(("availability available block %d" % b, not moved, False))
        rowsB.append(("availability shortfall block %d" % b, not moved, False))
    tot_moved = abs(sum(s_gold.values()) - sum(s_naive.values())) > 0.05
    for lbl in ("committed total", "available total", "shortfall total"):
        rowsB.append(("availability %s" % lbl, lbl == "committed total" or not tot_moved, lbl == "committed total"))
    asks.append(("B block availability", rowsB))

    # ---- ask C: settlement reconciliation -------------------------------------------------
    met = defaultdict(float)
    for r in rd("settlement/metered_volumes_15min.csv"):
        v = float(r["net_volume"]) / (1000.0 if r["unit"] == "kWh" else 1.0)
        met[r["metering_point"]] += v
    stmt = defaultdict(float)
    for f in ("operator/settlement_statement_daily_2026-09.csv",
              "operator/settlement_statement_daily_2026-10_amended.csv"):
        for r in rd(f):
            stmt[r["metering_point"]] += float(r["settled_volume_mwh"])
    prelim = defaultdict(float)
    for f in ("operator/settlement_statement_daily_2026-09.csv",
              "operator/settlement_statement_daily_2026-10_preliminary.csv"):
        for r in rd(f):
            prelim[r["metering_point"]] += float(r["settled_volume_mwh"])
    rowsC = []
    for r in F["reconciliation"]:
        sid = r["site"]
        rowsC.append(("metered %s" % sid, True, sid != F["forcing"]["kwh_site"]))
        pts = [p for p in met if True]
        moved_prelim = abs(sum(stmt.values()) - sum(prelim.values())) > 0.05
        rowsC.append(("difference %s" % sid, True, not moved_prelim))
    for lbl in ("metered total", "difference total"):
        rowsC.append(("reconciliation %s" % lbl, True, False))
    asks.append(("C settlement reconciliation", rowsC))

    n = sum(len(r) for _, r in asks)
    keep_c = sum(1 for _, rows in asks for (_, c, m) in rows if c)
    keep_m = sum(1 for _, rows in asks for (_, c, m) in rows if m)
    Lc, Lm = keep_c / n, keep_m / n
    C = W_REC + W_INSTR + W_ASK * Lc
    S = R_WRONG + W_INSTR + W_ASK * Lm
    print("ask figures: %d" % n)
    for name, rows in asks:
        kc = sum(1 for (_, c, m) in rows if c); km = sum(1 for (_, c, m) in rows if m)
        print("  %-28s cracker keeps %2d of %2d, mirror keeps %2d of %2d  %s"
              % (name, kc, len(rows), km, len(rows), "MISS" if kc == 0 else "KEEP"))
    print("cracker (landed the call): %.1f  = %.0f + %.0f + %.0f x %.3f" % (C, W_REC, W_INSTR, W_ASK, Lc))
    print("mirror  (stopped at rung 0, named %s): %.1f  = %.0f + %.0f + %.0f x %.3f"
          % (F["ladder_names"]["pre"], S, R_WRONG, W_INSTR, W_ASK, Lm))
    print("PAIR CEILING: %.1f   (bar 40)" % ((C + S) / 2))
    print("MIRROR LEAKAGE: %.1f per cent of ask weight   (bar under 35)" % (100 * Lm))
    return 0

if __name__ == "__main__":
    sys.exit(main())
