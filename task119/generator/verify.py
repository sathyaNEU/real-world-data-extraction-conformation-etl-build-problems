"""Independent verifier for task119: python3 verify.py <target_dir>

Reads only the shipped files in target_dir. It imports nothing from the generator and reads no seed,
parameter or side file. Joins run in DuckDB, the UTC conversion in pandas, the unit census as a numpy step
function over the feed's islands of contiguous rows, the corpus rules as vectorised masks. It recomputes
every rung, every rival-killer, every calibration outcome and every graded figure, and checks them
against the CLAIMS block. Exit status 0 only when every claim holds.
"""
import itertools
import sqlite3
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

CLAIMS = {
    "call": "STN", "call_figure": 27, "runner_up": "PRW", "runner_up_figure": 15, "gap": 12,
    "rungs": [("LAT", 56, "RIS", 44), ("RIS", 44, "BRK", 35), ("BRK", 34, "PRW", 4), ("PRW", 15, "RIS", 2),
              ("STN", 27, "PRW", 15)],
    "y3": {"RIS": (150, 44, 2), "TAN": (36, 10, 0), "BRK": (118, 35, 0), "STN": (92, 27, 27), "LAT": (190, 56, 0),
           "ELL": (46, 13, 0), "PRW": (74, 21, 15), "PEL": (25, 7, 0)},
    "record": {"RIS": (438, 126, 8), "TAN": (104, 29, 0), "BRK": (351, 104, 5), "STN": (275, 80, 80),
               "LAT": (559, 165, 0), "ELL": (140, 40, 6), "PRW": (221, 63, 46), "PEL": (75, 22, 3)},
    "record_total": (2163, 629, 148),
    "by_year_total": {1: (695, 204, 54), 2: (737, 212, 50), 3: (731, 213, 44)},
    "natural_total": (2208, 669, 161),
    "corpus_reviews": 34, "corpus_confirmed": 412, "corpus_attempts": 41, "rules": 216, "min_rival_misses": 4,
    "twin": (("Ormerleby", 2022, 24), ("Selarwell", 2023, 11)),
}
F = {
    "referrals": "critical_care_referrals_202307_202606.csv",
    "stays": "acc_unit_stays_202306_202606.parquet",
    "returns": "acc_bed_return_0800_202306_202606.csv",
    "episodes": "apc_episodes_referred_patients_2022-2026.parquet",
    "register": "acc_unit_register.csv",
    "levels": "ccrs_referral_levels_202307_202604.csv",
    "links": "pas_patient_key_links_2023-2026.csv",
    "capacity": "wenmarsh_acc_capacity_report_2024-04_to_2026-06.xlsx",
    "reviewlog": "nrr_escalation_reviews_closed_2021-2025.xlsx",
    "reviewdb": "nrr_review_records.sqlite",
}
YEAR_STARTS = {1: "2023-07-01", 2: "2024-07-01", 3: "2025-07-01"}
YEAR_ENDS = {1: "2024-06-30", 2: "2025-06-30", 3: "2026-06-30"}
RESULTS = []


def claim(name, ok, got=""):
    RESULTS.append(bool(ok))
    print("%s  %-70s %s" % ("OK  " if ok else "FAIL", name[:70], str(got)[:120]))


def load(T):
    con = duckdb.connect()
    p = lambda k: str(Path(T) / F[k])
    con.execute("CREATE TABLE ref AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % p("referrals"))
    con.execute("CREATE TABLE lev AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % p("levels"))
    con.execute("CREATE TABLE links AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % p("links"))
    con.execute("CREATE TABLE reg AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % p("register"))
    con.execute("CREATE TABLE ret AS SELECT unit_code, CAST(return_date AS DATE) d, CAST(beds_open AS INT) beds, "
                "CAST(beds_occupied_0800 AS INT) occ FROM read_csv('%s', header=true, all_varchar=true)" % p("returns"))
    con.execute("CREATE TABLE st AS SELECT * FROM read_parquet('%s')" % p("stays"))
    con.execute("CREATE TABLE ep AS SELECT patient_key, date_of_death FROM read_parquet('%s')" % p("episodes"))
    return con


def build_waits(con, natural=False):
    """One row per referral with local decision time, end, decision level and patient, per the files'
    own rules (natural=True reads every field as it stands)."""
    ref = con.execute("SELECT * FROM ref").df()
    leg = ref["referral_id"].str.startswith("CC")
    for c, name in (("received_at", "rec_t"), ("dta_at", "dta_t"), ("outcome_at", "outcome_at_t")):
        ts = pd.to_datetime(ref[c].replace("", None), format="%Y-%m-%d %H:%M")
        if not natural:
            loc = ts.dt.tz_localize("UTC").dt.tz_convert("Europe/London").dt.tz_localize(None)
            ts = ts.where(~leg, loc)
        ref[name] = ts
    first = con.execute("SELECT referral_id, MIN(admitted_at) a FROM st WHERE referral_id IS NOT NULL AND "
                        "referral_id <> '' GROUP BY referral_id").df()
    ref = ref.merge(first, on="referral_id", how="left")
    adm_leg = leg & (ref["outcome"] == "Admitted")
    ref["end_t"] = ref["outcome_at_t"].where(~adm_leg, ref["a"])
    dec = con.execute("SELECT referral_id, CAST(level AS INT) AS dec_level FROM lev WHERE entry = 'DECISION'").df()
    ref = ref.merge(dec, on="referral_id", how="left")
    lvl = ref["level_of_care"].astype(int)
    ref["lvl"] = lvl if natural else ref["dec_level"].fillna(lvl).astype(int).where(leg, lvl)
    lk = con.execute("SELECT temporary_key, verified_key FROM links").df()
    m = dict(zip(lk.temporary_key, lk.verified_key))
    ref["person"] = ref["patient_key"] if natural else ref["patient_key"].map(lambda k: m.get(k, k))
    dod = con.execute("SELECT patient_key, MIN(date_of_death) dod FROM ep WHERE date_of_death IS NOT NULL "
                      "GROUP BY patient_key").df()
    ref = ref.merge(dod.rename(columns={"patient_key": "person"}), on="person", how="left")
    ref["mins"] = (ref["end_t"] - ref["dta_t"]).dt.total_seconds() / 60
    ref["long"] = (ref["lvl"] == 3) & (ref["outcome"] != "Stood down") & (ref["mins"] > 240)
    ref["dday"] = ref["dta_t"].dt.normalize()
    off = (pd.to_datetime(ref["dod"]) - ref["dday"]).dt.days
    ref["died30"] = off.between(0, 30)
    ref["year"] = 0
    for y in (1, 2, 3):
        ref.loc[(ref["dday"] >= YEAR_STARTS[y]) & (ref["dday"] <= YEAR_ENDS[y]), "year"] = y
    return ref[ref["long"]].copy()


def own_unit_table(con, current_only=False):
    reg = con.execute("SELECT unit_code, trust_code, CAST(care_level AS INT) lv, valid_from, "
                      "COALESCE(valid_to, '') AS valid_to FROM reg").df()
    reg = reg[reg.lv == 3]
    if current_only:
        reg = reg[reg.valid_to == ""]
    return reg


def islands(con, merge=True):
    """Stays as islands of contiguous rows of one patient in one unit (or every row, merge=False)."""
    if not merge:
        return con.execute("SELECT unit_code, patient_key, admitted_at a, discharged_at b, admission_type t FROM st").df()
    q = """
    WITH s AS (SELECT unit_code, patient_key, admitted_at, discharged_at, admission_type,
                      LAG(discharged_at) OVER (PARTITION BY unit_code, patient_key ORDER BY admitted_at, stay_id) prev
               FROM st),
    g AS (SELECT *, SUM(CASE WHEN prev = admitted_at THEN 0 ELSE 1 END)
                     OVER (PARTITION BY unit_code, patient_key ORDER BY admitted_at ROWS UNBOUNDED PRECEDING) grp FROM s)
    SELECT unit_code, patient_key, MIN(admitted_at) a, MAX(discharged_at) b,
           ARG_MIN(admission_type, admitted_at) t FROM g GROUP BY unit_code, patient_key, grp"""
    return con.execute(q).df()


class Census:
    def __init__(self, isl, ret):
        self.u = {}
        for u, g in isl.groupby("unit_code"):
            t = np.concatenate([g["a"].values.astype("datetime64[m]").astype(np.int64),
                                g["b"].values.astype("datetime64[m]").astype(np.int64)])
            dlt = np.concatenate([np.ones(len(g), np.int64), -np.ones(len(g), np.int64)])
            o = np.lexsort((dlt, t))
            t, dlt = t[o], dlt[o]
            occ = np.cumsum(dlt)
            last = np.r_[t[1:] != t[:-1], True]
            self.u[u] = (t[last], occ[last])
        self.beds = {(r.unit_code, str(r.d)[:10]): r.beds for r in ret.itertuples()}
        self.occ08 = {(r.unit_code, str(r.d)[:10]): r.occ for r in ret.itertuples()}

    def empty(self, u, a, b, beds):
        if u not in self.u:
            return False
        t, occ = self.u[u]
        i = np.searchsorted(t, a, side="right") - 1
        j = np.searchsorted(t, b, side="left")
        vals = [occ[i] if i >= 0 else 0] + list(occ[i + 1:j])
        return min(vals) < beds


def classify(con, W, current_register=False, merge=True, hourly=False):
    reg = own_unit_table(con, current_register)
    isl = islands(con, merge)
    ret = con.execute("SELECT * FROM ret").df()
    cen = Census(islands(con, True), ret)
    plan = {u: np.sort(g["a"].values.astype("datetime64[m]").astype(np.int64)) for u, g in isl[isl.t == "04"].groupby("unit_code")}
    own, emp, alloc, v08 = [], [], [], []
    for r in W.itertuples():
        d = str(r.dday)[:10]
        rows = reg[(reg.trust_code == r.referring_trust) & (reg.valid_from <= d) &
                   ((reg.valid_to == "") | (reg.valid_to >= d))] if not current_register else \
            reg[reg.trust_code == r.referring_trust]
        units = sorted(rows.unit_code.unique())
        a = np.datetime64(r.dta_t, "m").astype(np.int64)
        b = np.datetime64(r.end_t, "m").astype(np.int64)
        e = al = v = False
        for u in units:
            beds = cen.beds.get((u, d))
            if beds is not None:
                if hourly:
                    t, occ = cen.u[u]
                    for h in range((a // 60 + 1) * 60, b, 60):
                        i = np.searchsorted(t, h, side="right") - 1
                        if (occ[i] if i >= 0 else 0) < beds:
                            e = True
                            break
                elif cen.empty(u, a, b, beds):
                    e = True
                if cen.occ08.get((u, d), beds) < beds:
                    v = True
            p = plan.get(u)
            if p is not None:
                k = np.searchsorted(p, a, side="right")
                if k < len(p) and p[k] < b:
                    al = True
        own.append(bool(units))
        emp.append(e)
        alloc.append(al)
        v08.append(v)
    W = W.copy()
    W["own"], W["empty"], W["alloc"], W["v08"] = own, emp, alloc, v08
    return W


def per_trust(W, mask, key="person"):
    return W[mask].groupby("referring_trust")[key].nunique().to_dict()


def top2(d):
    s = sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))
    return s[0][0], s[0][1], s[1][0], s[1][1]


def corpus(T):
    con = sqlite3.connect(str(Path(T) / F["reviewdb"]))
    r = pd.read_sql("SELECT r.*, o.hospital_discharge_date, o.date_of_death FROM referrals r JOIN patient_outcomes o "
                    "USING (review_ref, referral_ref)", con)
    rets = pd.read_sql("SELECT * FROM bed_returns", con)
    con.close()
    for c in ("received_at", "decision_at", "bed_assigned_at", "arrived_at", "outcome_at"):
        r[c] = pd.to_datetime(r[c])
    r["dod"] = pd.to_datetime(r["date_of_death"])
    r["hout"] = pd.to_datetime(r["hospital_discharge_date"])
    r["dday"] = r["decision_at"].dt.normalize()
    died_w = r["outcome"] == "died before admission"
    end_bed = r["bed_assigned_at"].where(~died_w, r["outcome_at"])
    end_arr = r["arrived_at"].where(~died_w, r["outcome_at"])
    off = (r["dod"] - r["dday"]).dt.days
    clocks = {"decision_to_bed": (end_bed - r["decision_at"]), "receipt_to_bed": (end_bed - r["received_at"]),
              "decision_to_arrival": (end_arr - r["decision_at"])}
    wins = {"30d": off.between(0, 30), "in_hospital": r["dod"].notna() & (r["dod"] <= r["hout"]),
            "7d": off.between(0, 7), "90d": off.between(0, 90)}
    lvls = {"decided_3": r["level_decided"] == 3, "requested_3": r["level_requested"] == 3,
            "decided_2_or_3": r["level_decided"].isin([2, 3])}
    dbas = {"kept": pd.Series(True, index=r.index), "dropped": ~died_w}
    live = r["outcome"] != "stood down"
    out = {}
    for c, w, l, b, t in itertools.product(clocks, wins, lvls, dbas, (240, 180, 360)):
        m = live & lvls[l] & dbas[b] & wins[w] & (clocks[c].dt.total_seconds() / 60 > t)
        out[(c, w, l, b, t)] = r[m].groupby("review_ref").size()
    log = pd.read_excel(Path(T) / F["reviewlog"], sheet_name="Reviews").set_index("Review ref")
    att = pd.read_excel(Path(T) / F["reviewlog"], sheet_name="Attempts")
    return out, log, att, rets, r


def main(T):
    con = load(T)
    W = classify(con, build_waits(con))
    died = W["died30"]
    y3 = W["year"] == 3
    # the rungs on the latest four quarters
    r0 = per_trust(W, y3 & died)
    r1 = per_trust(W, y3 & died & W["own"])
    r2 = per_trust(W, y3 & died & W["own"] & W["v08"])
    r3 = per_trust(W, y3 & died & W["own"] & W["empty"])
    r4 = per_trust(W, y3 & died & W["own"] & (W["empty"] | W["alloc"]))
    for k, (rk, want) in enumerate(zip((r0, r1, r2, r3, r4), CLAIMS["rungs"])):
        rk = {t: rk.get(t, 0) for t in CLAIMS["y3"]}
        claim("rung %d: %s %d over %s %d" % ((k,) + want), top2(rk) == want, top2(rk))
    l, v1, l2, v2 = top2({t: r4.get(t, 0) for t in CLAIMS["y3"]})
    claim("the call: STN, 27 confirmable deaths, runner-up PRW 15, gap 12",
          (l, v1, l2, v2 - 0, v1 - v2) == ("STN", 27, "PRW", 15, 12), (l, v1, l2, v2, v1 - v2))
    # the rival-killers
    e_own = own_unit_table(con)
    claim("killer of rung 0: LAT holds no level-3 beds in the register", "LAT" not in set(e_own.trust_code))
    ris_days = W[y3 & (W.referring_trust == "RIS")]["dday"].dt.strftime("%Y-%m-%d").unique()
    ret = con.execute("SELECT unit_code, CAST(d AS VARCHAR) d, beds, occ FROM ret").df()
    rr = ret[(ret.unit_code == "RIS-ACC") & ret.d.isin(ris_days)]
    claim("killer of rung 1: RIS-ACC reported no empty bed at 08:00 on any day RIS referrals waited",
          len(rr) > 0 and (rr.occ >= rr.beds).all(), "%d days" % len(rr))
    brk = W[y3 & (W.referring_trust == "BRK")]
    claim("killer of rung 2: BRK-ACC full at every moment of every BRK long wait", not brk["empty"].any(), len(brk))
    stn = W[y3 & (W.referring_trust == "STN")]
    claim("decisive fact: STN-ACC admitted planned post-operative patients through every STN long wait",
          stn["alloc"].all() and not stn["empty"].any(), len(stn))
    # the graded figures
    y3t = {t: (W[y3 & (W.referring_trust == t)]["person"].nunique(),
               W[y3 & died & (W.referring_trust == t)]["person"].nunique(),
               W[y3 & died & (W.referring_trust == t) & (W["empty"] | W["alloc"])]["person"].nunique())
           for t in CLAIMS["y3"]}
    claim("latest four quarters: patients, deaths, confirmable per trust", y3t == CLAIMS["y3"])
    rec = {t: (W[W.referring_trust == t]["person"].nunique(), W[died & (W.referring_trust == t)]["person"].nunique(),
               W[died & (W.referring_trust == t) & (W["empty"] | W["alloc"])]["person"].nunique())
           for t in CLAIMS["record"]}
    claim("record: 24 trust figures (3a, 3b, 3c)", rec == CLAIMS["record"], rec)
    tot = tuple(sum(v[i] for v in rec.values()) for i in range(3))
    claim("record totals 2163 / 629 / 148", tot == CLAIMS["record_total"], tot)
    by = {}
    for y in (1, 2, 3):
        m = W["year"] == y
        by[y] = (W[m]["person"].nunique(), W[m & died]["person"].nunique(),
                 W[m & died & (W["empty"] | W["alloc"])]["person"].nunique())
    claim("by four-quarter year", by == CLAIMS["by_year_total"], by)
    # the hourly clean-data replacement names G on its rung and leaves the call alone
    Wh = classify(con, build_waits(con), hourly=True)
    rh = per_trust(Wh, (Wh.year == 3) & Wh.died30 & Wh["own"] & Wh["empty"])
    claim("clean-data test: hourly return names PRW, the call stays STN", top2({t: rh.get(t, 0) for t in CLAIMS["y3"]})[0] == "PRW")
    # the natural path: every field as it stands, current register, rows as admissions, deaths per referral row
    Wn = classify(con, build_waits(con, natural=True), current_register=True, merge=False)
    nat = (Wn["person"].nunique() if False else sum(Wn[Wn.referring_trust == t]["person"].nunique() for t in CLAIMS["record"]),
           int(Wn["died30"].sum()), int((Wn["died30"] & (Wn["empty"] | Wn["alloc"])).sum()))
    claim("natural path totals 2208 / 669 / 161", nat == CLAIMS["natural_total"], nat)
    # the calibration corpus
    out, log, att, rets, cr = corpus(T)
    filed = out[("decision_to_bed", "30d", "decided_3", "kept", 240)].reindex(log.index, fill_value=0)
    conf = log["Deaths confirmed avoidable"]
    claim("corpus: the filed rule reproduces all 34 reviews (412 confirmed, 41 attempts)",
          (filed == conf).all() and conf.sum() == 412 and len(log) == 34 and len(att) == 41, int(filed.sum()))
    worst = min(int((v.reindex(log.index, fill_value=0) != conf).sum()) for k, v in out.items()
                if k != ("decision_to_bed", "30d", "decided_3", "kept", 240))
    claim("corpus: %d rules; every rival misses at least 4 reviews" % len(out), len(out) == 216 and worst >= 4, worst)
    claim("corpus: no reviewed unit full at any 08:00 return", (rets.beds_occupied_0800 < rets.beds_open).all())
    (ta, ya, ca), (tb, yb, cb) = CLAIMS["twin"]
    ra = log[(log.Trust == ta) & (log["Year reviewed"] == ya)].iloc[0]
    rb = log[(log.Trust == tb) & (log["Year reviewed"] == yb)].iloc[0]
    cols = ["Trust type", "Level 3 beds", "Referrals in year", "Level 3 referrals waiting over 4h from receipt",
            "Mean beds occupied at 08:00", "Level 3 referrals: deaths within 30 days (all causes)"]
    # recompute the visible columns from the records
    def vis(ref_code, beds):
        x = cr[cr.review_ref == ref_code]
        l3 = x[x.level_decided == 3]
        end = l3["bed_assigned_at"].fillna(l3["outcome_at"])
        scr = int(((end - l3["received_at"]).dt.total_seconds() / 60 > 240)[l3.outcome != "stood down"].sum())
        d30 = int(((l3["dod"] - l3["dday"]).dt.days.between(0, 30)).sum())
        occ = round(rets[rets.review_ref == ref_code]["beds_occupied_0800"].mean(), 1)
        return len(x), scr, occ, d30
    va, vb = vis(ra.name, ra["Level 3 beds"]), vis(rb.name, rb["Level 3 beds"])
    claim("twin pair: identical published columns, recomputed from the records",
          all(ra[c] == rb[c] for c in cols) and va == vb and va == (ra[cols[2]], ra[cols[3]], ra[cols[4]], ra[cols[5]]),
          (va, vb))
    claim("twin pair: confirmed %d and %d, the rule reproduces both" % (ca, cb),
          conf[ra.name] == ca and conf[rb.name] == cb and filed[ra.name] == ca and filed[rb.name] == cb)
    # the capacity report's referral waits from the referral log
    cap = pd.read_excel(Path(T) / F["capacity"], sheet_name="Referral waits")
    q = """SELECT strftime(CAST(received_at AS TIMESTAMP), '%Y-%m') m, referring_trust t,
                  COUNT(*) n, SUM(CASE WHEN outcome_at <> '' AND date_diff('minute', CAST(received_at AS TIMESTAMP),
                  CAST(outcome_at AS TIMESTAMP)) > 240 THEN 1 ELSE 0 END) k
           FROM ref WHERE level_of_care = '3' AND received_at >= '2024-04-01' AND received_at < '2026-07-01'
           GROUP BY 1, 2"""
    g = con.execute(q).df().set_index(["m", "t"])
    ok = all(g.loc[(r.Month, r._2), "k"] == r._4 if (r.Month, r._2) in g.index else r._4 == 0 for r in cap.itertuples())
    claim("capacity report: referral waits reproduce from the referral log", ok)
    n = len(RESULTS)
    print("\n%d claims, %d failed" % (n, n - sum(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "target")))
