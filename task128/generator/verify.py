"""Independent verifier: reads only the shipped bundle (DuckDB over the files, no generator module) and recomputes
the call, every centre's rolls, the contact and promise rates and the arrangement balances, then compares them with
the golden CSV at its rounding."""
import csv
import os
import sys

import duckdb


def q(con, sql):
    return con.execute(sql).fetchall()


def main(target, golden):
    con = duckdb.connect()
    t = lambda n: os.path.join(target, n).replace("'", "''")
    con.execute("CREATE TABLE lists AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % t("ES30_DIALLER_LISTS_2025-01_2026-09.csv"))
    con.execute("CREATE TABLE hist AS SELECT * FROM read_parquet('%s')" % t("CARD_DELINQUENCY_HISTORY_2025-01_2026-10.parquet"))
    con.execute("CREATE TABLE wl AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % t("ES_WORKFORCE_DIALLER_LOG_2025-01_2026-09.csv"))
    con.execute("CREATE TABLE arr AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % t("ES30_PAYMENT_ARRANGEMENTS_2025-01_2026-09.csv"))
    con.execute("CREATE TABLE fx AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % t("TREASURY_BOOKING_RATES_USDCAD_2025-01_2026-10.csv"))
    # the cycle date two months on, from the history's own cycle dates
    con.execute("""CREATE TABLE cyc AS SELECT DISTINCT CYCLE_CD, year(CYCLE_DT) y, month(CYCLE_DT) m, CYCLE_DT FROM hist""")
    con.execute("""CREATE TABLE rec AS
        SELECT l.*, CAST(l.LIST_DT AS DATE) d,
               COALESCE(l.RESULT_CD, '') rc,
               (COALESCE(l.RESULT_CD, '') = '') AS left_,
               (COALESCE(l.RESULT_CD, '') IN ('DNC', 'NDN')) AS skipped,
               c.CYCLE_DT AS out_dt
        FROM lists l LEFT JOIN cyc c
          ON c.CYCLE_CD = l.CYCLE_CD
         AND c.y * 12 + c.m = year(CAST(l.LIST_DT AS DATE)) * 12 + month(CAST(l.LIST_DT AS DATE)) + 2""")
    con.execute("""CREATE TABLE r2 AS SELECT r.*, (h.ACCT_NO IS NOT NULL) AS rolled
        FROM rec r LEFT JOIN (SELECT DISTINCT ACCT_NO, CYCLE_DT FROM hist WHERE DPD >= 90) h
          ON h.ACCT_NO = r.ACCT_NO AND h.CYCLE_DT = r.out_dt
        WHERE r.d BETWEEN DATE '2025-07-01' AND DATE '2026-06-30'""")
    rows = q(con, """
        WITH od AS (SELECT CENTRE_CD, d FROM r2 GROUP BY 1, 2 HAVING SUM(CASE WHEN left_ THEN 1 ELSE 0 END) > 0),
        day AS (SELECT r.CENTRE_CD, r.d,
                   SUM(CASE WHEN left_ THEN 1 ELSE 0 END) nb,
                   SUM(CASE WHEN NOT left_ THEN 1 ELSE 0 END) na,
                   SUM(CASE WHEN left_ AND rolled THEN 1 ELSE 0 END) * 1.0 / SUM(CASE WHEN left_ THEN 1 ELSE 0 END) rb,
                   SUM(CASE WHEN NOT left_ AND rolled THEN 1 ELSE 0 END) * 1.0 / SUM(CASE WHEN NOT left_ THEN 1 ELSE 0 END) ra,
                   SUM(CASE WHEN skipped THEN 1 ELSE 0 END) sk
                FROM r2 r JOIN od USING (CENTRE_CD, d) GROUP BY 1, 2),
        cen AS (SELECT CENTRE_CD, SUM(nb * (rb - ra)) / SUM(nb) itt_nb,
                       SUM(nb * na / (nb + na) * (rb - ra)) / SUM(nb * na / (nb + na)) itt_mh,
                       SUM(sk) * 1.0 / SUM(na) s FROM day GROUP BY 1)
        SELECT c.CENTRE_CD, c.itt_nb, c.itt_mh, c.s,
               (SELECT SUM(LEAST((1 - c.s) * nb, 400)) FROM day x WHERE x.CENTRE_CD = c.CENTRE_CD) dials
        FROM cen c ORDER BY 1""")
    names = {"TBY": "Thunder Bay", "SUD": "Sudbury", "KGN": "Kingston", "LON": "London", "WPG": "Winnipeg"}
    gold = {r["CENTRE"]: r for r in csv.DictReader(open(os.path.join(golden, "centre_call_effects_2025_2026.csv")))}
    r100 = lambda x: int((x / 100.0) + 0.5) * 100
    worst = 0
    calls = {}
    for c, itt_nb, itt_mh, s, dials in rows:
        a = itt_nb / (1 - s) * dials
        b = itt_mh / (1 - s) * dials
        g = int(gold[names[c]]["ROLLS_PREVENTED_JUL25_JUN26"])
        assert r100(a) == g and r100(b) == g, (c, a, b, g)
        calls[c] = a
        print("  verify %-12s rolls %6.1f (nb-weighted) %6.1f (Mantel-Haenszel) -> %d" % (names[c], a, b, g))
    assert max(calls.values()) < 694, calls
    print("  verify call: no centre reaches 694 (largest %s %.1f)" % (max(calls, key=calls.get), max(calls.values())))
    up = dict(q(con, "SELECT CENTRE_CD, MIN(CAST(WORK_DT AS DATE)) FROM wl WHERE DIALLER_VER = 'CX2.1' GROUP BY 1"))
    for c in names:
        n_d, n_rpc, n_ptp = q(con, """SELECT COUNT(*),
              SUM(CASE WHEN rc IN ('RPC','PTP','ARR','RTP','CBK') OR (rc = 'AR' AND d < DATE '%s') THEN 1 ELSE 0 END),
              SUM(CASE WHEN rc = 'PTP' THEN 1 ELSE 0 END)
            FROM r2 WHERE CENTRE_CD = '%s' AND NOT left_ AND NOT skipped""" % (up[c], c))[0]
        rr, pr = 100.0 * n_rpc / n_d, 100.0 * n_ptp / n_rpc
        assert "%.1f" % (int(rr * 10 + 0.5) / 10.0) == gold[names[c]]["RPC_PER_100_DIALLED"], (c, rr)
        assert "%.1f" % (int(pr * 10 + 0.5) / 10.0) == gold[names[c]]["PTP_PER_100_RPC"], (c, pr)
        bal = q(con, """SELECT SUM(CASE WHEN p.PRODUCT_CD = 'VUSD' THEN CAST(a.ARR_BAL AS DOUBLE) * CAST(f.BOOKING_RATE AS DOUBLE)
                                    ELSE CAST(a.ARR_BAL AS DOUBLE) END)
            FROM arr a
            LEFT JOIN (SELECT DISTINCT ACCT_NO, PRODUCT_CD FROM hist) p ON p.ACCT_NO = a.ACCT_NO
            LEFT JOIN fx f ON f.RATE_DT = a.SETUP_DT
            WHERE a.CENTRE_CD = '%s' AND CAST(a.SETUP_DT AS DATE) BETWEEN DATE '2025-07-01' AND DATE '2026-06-30'""" % c)[0][0]
        assert int(bal / 100000.0 + 0.5) * 100000 == int(gold[names[c]]["ARR_BAL_PLACED_CAD"]), (c, bal)
        print("  verify %-12s contacts %.3f, promises %.3f, balances %.0f" % (names[c], rr, pr, bal))
    print("verify: green from the bundle")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
