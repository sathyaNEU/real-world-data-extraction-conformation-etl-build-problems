"""Independent verifier for task450: reads only the shipped bundle with DuckDB and NumPy, on its own code path (no
calc.py, reader.py or generator state), screens the items both forms carry for a change in difficulty between the
cohorts (the delta plot and the change in share correct, written here), links the 2026 form to the 2025 scale through
the shared items that held (chained equipercentile and Tucker, written here), recomputes every campus's figures, the designated campuses and the
two asks, and compares them with the golden workbook, the golden memo and figures.json.

    python3 task450/generator/verify.py [target] [golden]
"""
import json
import os
import re
import sys

import duckdb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def pct(k, n):
    return "%.1f" % (100.0 * k / n)


def eq_chain(X, V1, Y, V2, nx, nv):
    """Chained equipercentile: Y to V2's percentile, then V1's score at that rank, then X's score at V1's rank."""
    def cdf(s, k):
        f = np.bincount(s, minlength=k + 1) / len(s)
        return f, np.cumsum(f)

    def prank(x, f, F, k):
        i = int(min(max(np.floor(x + 0.5), 0), k))
        return (F[i - 1] if i > 0 else 0.0) + (x - (i - 0.5)) * f[i]

    def score_at(p, f, F, k):
        j = int(min(np.searchsorted(F, p, side="left"), k))
        return (p - (F[j - 1] if j > 0 else 0.0)) / f[j] + j - 0.5

    fX, FX = cdf(X, nx)
    fY, FY = cdf(Y, nx)
    f1, F1 = cdf(V1, nv)
    f2, F2 = cdf(V2, nv)
    return lambda y: score_at(prank(score_at(prank(y, fY, FY, nx), f2, F2, nv), f1, F1, nv), fX, FX, nx)


def eq_tucker(X, V1, Y, V2):
    w1 = len(X) / (len(X) + len(Y))
    w2 = 1 - w1
    g1 = np.cov(X, V1)[0, 1] / np.var(V1, ddof=1)
    g2 = np.cov(Y, V2)[0, 1] / np.var(V2, ddof=1)
    dv = V1.mean() - V2.mean()
    mx = X.mean() - w2 * g1 * dv
    my = Y.mean() + w1 * g2 * dv
    vx = X.var() - w2 * g1 ** 2 * (V1.var() - V2.var()) + w1 * w2 * g1 ** 2 * dv ** 2
    vy = Y.var() + w1 * g2 ** 2 * (V1.var() - V2.var()) + w1 * w2 * g2 ** 2 * dv ** 2
    return lambda y: np.sqrt(vx / vy) * (y - my) + mx


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    q = duckdb.connect()
    t = lambda f: os.path.join(target, f).replace("'", "''")
    import openpyxl
    from pypdf import PdfReader
    bank = [r for r in openpyxl.load_workbook(t("dma_item_bank_grade5_math.xlsx"), read_only=True)["Items"].iter_rows(
        min_row=2, values_only=True)]
    note = " ".join(" ".join(p.extract_text() for p in PdfReader(t("dma_key_correction_2026-05-19.pdf")).pages).split())
    m = re.search(r"Item (M5\d{5}), position \d+ .*?Score the item with key ([A-D])", note)
    fixed_item, fixed_key = m.group(1), m.group(2)
    key25 = {int(r[6]): r[4] for r in bank if r[6]}
    key26 = {r[0]: (fixed_key if r[0] == fixed_item else r[4]) for r in bank if r[7]}
    pos26 = {r[0]: int(r[7]) for r in bank if r[7]}
    shared = sorted(int(r[6]) for r in bank if r[6] and r[7])
    q.execute("CREATE TABLE k26 AS SELECT * FROM (VALUES %s) AS v(item_id, k)" %
              ",".join("('%s','%s')" % kv for kv in key26.items()))
    q.execute("CREATE TABLE p26 AS SELECT * FROM (VALUES %s) AS v(item_id, pos)" %
              ",".join("('%s',%d)" % kv for kv in pos26.items()))
    # each shared item's share answering correctly in each year, and the delta plot (written here) that screens
    # them for a change in difficulty between the cohorts before any link is made
    from scipy.stats import norm
    q.execute("""CREATE TABLE pc26 AS SELECT p.pos AS pos, avg((r.response = k.k)::INT) AS pc
                 FROM read_csv('%s', all_varchar=true) r JOIN k26 k USING (item_id) JOIN p26 p USING (item_id)
                 GROUP BY 1""" % t("grade5_math_responses_2026.csv"))
    pc26 = dict(q.execute("SELECT pos, pc FROM pc26").fetchall())
    pc25 = {}
    for p_ in shared:
        pc25[p_] = q.execute("SELECT avg((coalesce(I%02d, '') = '%s')::INT) FROM read_csv('%s', all_varchar=true)" % (
            p_, key25[p_], t("grade5_math_responses_2025.csv"))).fetchone()[0]
    x = np.array([13 + 4 * norm.ppf(1 - pc25[p_]) for p_ in shared])
    y = np.array([13 + 4 * norm.ppf(1 - pc26[p_]) for p_ in shared])
    cxy = np.mean((x - x.mean()) * (y - y.mean()))
    slope = (y.var() - x.var() + np.sqrt((y.var() - x.var()) ** 2 + 4 * cxy ** 2)) / (2 * cxy)
    dist = (slope * x - y + y.mean() - slope * x.mean()) / np.sqrt(slope ** 2 + 1)
    flagged = [p_ for p_, d in zip(shared, dist) if abs(d) > 1.5]
    gap = np.array([pc26[p_] - pc25[p_] for p_ in shared])
    mad = np.median(np.abs(gap - np.median(gap))) * 1.4826
    flagged_gap = [p_ for p_, g in zip(shared, gap) if abs(g - np.median(gap)) > 4 * mad]
    if flagged != flagged_gap or len(flagged) != 3:
        raise SystemExit("VERIFY: the screens disagree on the shared items that moved: %s, %s" % (flagged, flagged_gap))
    linking = [p_ for p_ in shared if p_ not in flagged]
    sh = ",".join(str(p) for p in linking)
    # 2026: scored answers per test taker
    q.execute("""CREATE TABLE s26 AS SELECT r.test_taker_id AS tt, sum((r.response = k.k)::INT) AS raw,
                 sum(CASE WHEN p.pos IN (%s) THEN (r.response = k.k)::INT ELSE 0 END) AS v
                 FROM read_csv('%s', all_varchar=true) r JOIN k26 k USING (item_id) JOIN p26 p USING (item_id)
                 GROUP BY 1""" % (sh, t("grade5_math_responses_2026.csv")))
    # 2025: wide by position
    cols = ", ".join("(coalesce(I%02d, '') = '%s')::INT" % (p, key25[p]) for p in range(1, 51))
    vcols = ", ".join("(coalesce(I%02d, '') = '%s')::INT" % (p, key25[p]) for p in linking)
    q.execute("""CREATE TABLE s25 AS SELECT SCHOOL_NAME AS nm, SCHOOL_CODE AS code, list_sum([%s]) AS raw,
                 list_sum([%s]) AS v FROM read_csv('%s', all_varchar=true)""" % (cols, vcols, t("grade5_math_responses_2025.csv")))
    X, V1 = (np.array(c, int) for c in zip(*q.execute("SELECT raw, v FROM s25").fetchall()))
    Y, V2 = (np.array(c, int) for c in zip(*q.execute("SELECT raw, v FROM s26").fetchall()))
    cut = 26.5 - 0.5 / 6
    passes = {}
    for nm, f in (("chained equipercentile", eq_chain(X, V1, Y, V2, 50, len(linking))), ("Tucker", eq_tucker(X, V1, Y, V2))):
        passes[nm] = min(y for y in range(51) if f(y) >= cut)
    if len(set(passes.values())) != 1:
        raise SystemExit("VERIFY: the two links disagree on the passing raw score: %s" % passes)
    r = passes["chained equipercentile"]
    # campuses: full academic year, closure, n-size
    q.execute("CREATE TABLE en AS SELECT * FROM read_csv('%s', all_varchar=true)" % t("sis_grade5_enrollment_2025-26.csv"))
    q.execute("CREATE TABLE xw AS SELECT * FROM read_csv('%s', all_varchar=true)" % t("dma_registrations_2026.csv"))
    ws = openpyxl.load_workbook(t("campus_directory_2026-27.xlsx"), read_only=True)["Campuses"]
    dirx = [r_ for r_ in ws.iter_rows(min_row=2, values_only=True)]
    by_name = {d[1]: str(d[0]) for d in dirx}
    rated_as = {}
    community = {}
    for d in dirx:
        community[str(d[0])] = d[2]
        mm = re.search(r"attendance zone to (.+)$", d[5] or "")
        rated_as[str(d[0])] = by_name[mm.group(1).strip()] if mm else str(d[0])
    fay = dict(q.execute("""
        WITH sp AS (SELECT student_id, campus_number AS c, CAST(entry_date AS DATE) AS a, CAST(exit_date AS DATE) AS b FROM en),
        cover AS (SELECT student_id, c FROM sp WHERE a <= DATE '2025-10-31' AND b >= DATE '2026-04-20'),
        one AS (SELECT student_id, min(c) AS c FROM cover GROUP BY 1 HAVING count(*) = 1)
        SELECT o.student_id, o.c FROM one o WHERE NOT EXISTS (SELECT 1 FROM sp s WHERE s.student_id = o.student_id
          AND s.c <> o.c AND s.a <= DATE '2026-04-20' AND s.b >= DATE '2025-10-31')""").fetchall())
    agg = {}
    for tt, sid, raw in q.execute("SELECT s.tt, x.student_id, s.raw FROM s26 s JOIN xw x ON x.test_taker_id = s.tt").fetchall():
        c = fay.get(sid)
        if c is None:
            continue
        c = rated_as[c]
        n, k = agg.get(c, (0, 0))
        agg[c] = (n + 1, k + int(raw >= r))
    rated = {c: v for c, v in agg.items() if v[0] >= 10}
    des = sorted(c for c, (n, k) in rated.items() if k < 0.40 * n)
    names = {str(d[0]): d[1] for d in dirx}
    # Ask A: 2025 test takers by learning community, placed by the campus name the platform recorded
    def expand(a):
        n_ = " " + a + " "
        for x, y in ((" EL ", " ELEMENTARY "), (" AVE ", " AVENUE "), (" ST ", " STREET "), (" RD ", " ROAD "),
                     (" TER ", " TERRACE "), (" XING ", " CROSSING "), (" PR ", " PRAIRIE "), (" HOLW ", " HOLLOW "),
                     (" MDW ", " MEADOW "), (" JUNP ", " JUNIPER ")):
            n_ = n_.replace(x, y)
        return n_.strip()
    up = {v.upper(): k for k, v in names.items()}
    a25 = {}
    for nm, raw in q.execute("SELECT nm, raw FROM s25").fetchall():
        k = community[rated_as[up[expand(nm)]]]
        n, m_ = a25.get(k, (0, 0))
        a25[k] = (n + 1, m_ + int(raw >= 27))
    # Ask B: enrolled in the window, no 2026 result, one person per student after the merges
    q.execute("CREATE TABLE mg AS SELECT * FROM read_csv('%s', all_varchar=true)" % t("sis_student_id_merges_2026.csv"))
    rows = q.execute("""
        WITH person AS (SELECT e.*, coalesce(m.surviving_id, e.student_id) AS pid FROM en e
                        LEFT JOIN mg m ON m.merged_id = e.student_id),
        inw AS (SELECT DISTINCT pid, campus_number FROM person WHERE CAST(entry_date AS DATE) <= DATE '2026-05-01'
                AND CAST(exit_date AS DATE) >= DATE '2026-04-20'),
        tested AS (SELECT DISTINCT coalesce(m.surviving_id, x.student_id) AS pid FROM s26 s
                   JOIN xw x ON x.test_taker_id = s.tt LEFT JOIN mg m ON m.merged_id = x.student_id)
        SELECT pid, campus_number FROM inw WHERE pid NOT IN (SELECT pid FROM tested)""").fetchall()
    per = {}
    for pid, c in rows:
        per.setdefault(pid, set()).add(community[rated_as[c]])
    if any(len(v) != 1 for v in per.values()):
        raise SystemExit("VERIFY: an untested student sits in two communities")
    un = {}
    for v in per.values():
        k = v.pop()
        un[k] = un.get(k, 0) + 1
    # compare with the goldens
    fail = []
    wb = openpyxl.load_workbook(os.path.join(golden, "grade5_math_results_2026.xlsx"), data_only=True)
    got = {str(x[0]): x for x in wb["Campus results"].iter_rows(min_row=4, values_only=True) if x[0]}
    if set(got) != set(rated):
        fail.append("rated campuses")
    for c, (n, k) in rated.items():
        g = got.get(c)
        if not g or (g[3], g[4]) != (n, k) or "%.1f" % g[5] != pct(k, n) or (g[6] == "Yes") != (c in des):
            fail.append("campus %s" % c)
    g2 = {x[0]: x for x in wb["2025 by community"].iter_rows(min_row=4, values_only=True)}
    for k, (n, m_) in a25.items():
        if g2[k][1] != n or "%.1f" % g2[k][2] != pct(m_, n):
            fail.append("Ask A %s" % k)
    g3 = {x[0]: x[1] for x in wb["No 2026 result"].iter_rows(min_row=4, values_only=True)}
    for k, v in un.items():
        if g3.get(k) != v:
            fail.append("Ask B %s" % k)
    if g3.get("District") != sum(un.values()):
        fail.append("Ask B district")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    if fig["passing_raw"] != str(r) or sorted(fig["designated"]) != sorted(names[c] for c in des):
        fail.append("figures.json")
    if fig.get("flagged_positions") != [str(p_) for p_ in flagged] or fig.get("kept_items") != str(len(linking)):
        fail.append("figures.json: the shared items set aside")
    from docx import Document
    doc = Document(os.path.join(golden, "intervention_schools_2027.docx"))
    text = " ".join(p.text for p in doc.paragraphs) + " " + " ".join(c.text for tb in doc.tables for row in tb.rows
                                                                    for c in row.cells)
    for c in des:
        if names[c] not in text or pct(rated[c][1], rated[c][0]) not in text:
            fail.append("memo %s" % names[c])
    print("verify: passing raw score %d on the 2026 form (%s); %d of %d rated campuses designated" % (
        r, ", ".join("%s %d" % kv for kv in passes.items()), len(des), len(rated)))
    print("verify: 2025 by community %s; no 2026 result %s, district %d" % (
        ", ".join("%s %d/%s" % (k, a25[k][0], pct(a25[k][1], a25[k][0])) for k in sorted(a25)),
        ", ".join("%s %d" % (k, un[k]) for k in sorted(un)), sum(un.values())))
    if fail:
        raise SystemExit("VERIFY FAILED: " + "; ".join(fail))
    print("verify: PASS (bundle-only recomputation agrees with the workbook, the memo and figures.json)")


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
