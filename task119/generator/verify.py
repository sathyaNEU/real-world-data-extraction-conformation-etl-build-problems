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
    "rungs": [("LAT", 56, "RIS", 44), ("BRK", 34, "PRW", 4), ("PRW", 15, "RIS", 2), ("RIS", 37, "PRW", 17),
              ("STN", 27, "PRW", 15)],
    "y3": {"RIS": (150, 44, 2), "TAN": (36, 10, 0), "BRK": (118, 35, 0), "STN": (92, 27, 27), "LAT": (190, 56, 0),
           "ELL": (46, 13, 0), "PRW": (74, 21, 15), "PEL": (25, 7, 0)},
    "record": {"RIS": (438, 126, 8), "TAN": (104, 29, 0), "BRK": (351, 104, 5), "STN": (275, 80, 80),
               "LAT": (559, 165, 0), "ELL": (140, 40, 6), "PRW": (221, 63, 46), "PEL": (75, 22, 3)},
    "record_total": (2163, 629, 148),
    "by_year_total": {1: (695, 204, 54), 2: (737, 212, 50), 3: (731, 213, 44)},
    "natural_total": (2366, 720, 205),
    "readings": {"referral": ("PRW", 15, "RIS", 2), "local": ("PRW", 15, "RIS", 2), "t04": ("PRW", 15, "RIS", 2),
                 "planned": ("RIS", 37, "PRW", 15), "not02": ("RIS", 37, "PRW", 15)},
    "every_hold_empty": ("RIS", 37, "STN", 27),
    "held_legacy_transfers_min": 900, "never_linked": 10,
    "corpus_reviews": 34, "corpus_confirmed": 412, "corpus_attempts": 41, "rules": 216, "min_rival_misses": 4,
    "twin": (("Ormerleby", 2022, 24), ("Selarwell", 2023, 11)),
}
F = {
    "referrals": "critical_care_referrals_202307_202606.csv",
    "stays": "acc_unit_stays_202306_202606.parquet",
    "returns": "acc_bed_return_0800_202306_202606.csv",
    "episodes": "apc_episodes_referred_patients_2022-2026.parquet",
    "register": "acc_unit_register.csv",
    "levels": "ccrs_referral_levels_202307_202404.csv",
    "links": "pas_patient_key_links_2023-2026.csv",
    "capacity": "wenmarsh_acc_capacity_report_2024-04_to_2026-06.xlsx",
    "reviewlog": "nrr_escalation_reviews_closed_2021-2025.xlsx",
    "reviewdb": "nrr_review_records.sqlite",
    "transfers": "interhospital_transfer_audit_202307_202606.csv",
    "theatre": "rds_theatre_cases_2023-2026.parquet",
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
    con.execute("CREATE TABLE ep AS SELECT patient_key, date_of_death, discharge_method, discharge_date "
                "FROM read_parquet('%s')" % p("episodes"))
    con.execute("CREATE TABLE tx AS SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % p("transfers"))
    # the unit feed with each legacy transfer dated from the bureau's allocation: the legacy bed list began the row at
    # the patient's arrival (the audit's arrived_at), the platform at the allocation (bed_confirmed_at)
    con.execute("""
        CREATE TABLE st2 AS
        WITH s AS (SELECT st.*, COALESCE(l.verified_key, st.patient_key) vk
                   FROM st LEFT JOIN links l ON l.temporary_key = st.patient_key),
             t AS (SELECT tx.to_unit, CAST(tx.arrived_at AS TIMESTAMP) arr, CAST(tx.bed_confirmed_at AS TIMESTAMP) conf,
                          COALESCE(l.verified_key, tx.patient_key) vk
                   FROM tx LEFT JOIN links l ON l.temporary_key = tx.patient_key
                   WHERE tx.bed_confirmed_at < '2024-04-02')
        SELECT s.stay_id, s.unit_code, s.referral_id, s.patient_key,
               CASE WHEN s.stay_id LIKE 'LB%' AND s.referral_id <> '' AND t.conf IS NOT NULL THEN t.conf
                    ELSE s.admitted_at END AS admitted_at,
               s.discharged_at, s.admission_type, s.source_location
        FROM s LEFT JOIN t ON t.to_unit = s.unit_code AND t.arr = s.admitted_at AND t.vk = s.vk""")
    con.execute("CREATE TABLE th AS SELECT * FROM read_parquet('%s')" % p("theatre"))
    for base in ("st2", "st"):
        held_tables(con, base)
    return con


def held_tables(con, base):
    """<base>_own: a bed the unit assigned to its own trust's patient who had not yet left theatre recovery (the theatre
    extract's case at the unit's trust, destination critical care, left_recovery_at after the assignment) stands empty
    until the patient left recovery. <base>_all: every held bed empty, a transfer's bed until the audit's arrival too."""
    con.execute("""
        CREATE TABLE %s_own AS
        WITH s AS (SELECT b.*, COALESCE(l.verified_key, b.patient_key) vk, r.trust_code ut
                   FROM %s b LEFT JOIN links l ON l.temporary_key = b.patient_key
                   LEFT JOIN (SELECT DISTINCT unit_code, trust_code FROM reg) r USING (unit_code)),
             h AS (SELECT COALESCE(l.verified_key, th.patient_key) vk, th.provider_code, th.left_recovery_at lft
                   FROM th LEFT JOIN links l ON l.temporary_key = th.patient_key
                   WHERE th.recovery_destination = 'Critical care unit')
        SELECT s.stay_id, s.unit_code, s.referral_id, s.patient_key,
               COALESCE((SELECT MIN(h.lft) FROM h WHERE h.vk = s.vk AND h.provider_code = s.ut
                         AND h.lft > s.admitted_at AND h.lft < LEAST(s.discharged_at, s.admitted_at + INTERVAL 18 HOUR)),
                        s.admitted_at) AS admitted_at,
               s.discharged_at, s.admission_type, s.source_location FROM s""" % (base, base))
    con.execute("""
        CREATE TABLE %s_all AS
        WITH s AS (SELECT b.*, COALESCE(l.verified_key, b.patient_key) vk FROM %s_own b
                   LEFT JOIN links l ON l.temporary_key = b.patient_key),
             t AS (SELECT tx.to_unit, CAST(tx.arrived_at AS TIMESTAMP) arr, CAST(tx.bed_confirmed_at AS TIMESTAMP) conf,
                          COALESCE(l.verified_key, tx.patient_key) vk
                   FROM tx LEFT JOIN links l ON l.temporary_key = tx.patient_key)
        SELECT s.stay_id, s.unit_code, s.referral_id, s.patient_key, COALESCE(t.arr, s.admitted_at) AS admitted_at,
               s.discharged_at, s.admission_type, s.source_location
        FROM s LEFT JOIN t ON t.to_unit = s.unit_code AND t.conf = s.admitted_at AND t.vk = s.vk""" % (base, base))


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
    first = con.execute("SELECT referral_id, MIN(admitted_at) a FROM %s WHERE referral_id IS NOT NULL AND "
                        "referral_id <> '' GROUP BY referral_id" % ("st" if natural else "st2")).df()
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
    if not natural:
        # a death no registration links: the spell under the patient's key that ended in death
        dm = con.execute("SELECT COALESCE(l.verified_key, ep.patient_key) person, MIN(discharge_date) dm FROM ep "
                         "LEFT JOIN links l ON l.temporary_key = ep.patient_key WHERE discharge_method = '4' "
                         "GROUP BY 1").df()
        ref = ref.merge(dm, on="person", how="left")
        ref["dod"] = pd.to_datetime(ref["dod"]).fillna(pd.to_datetime(ref["dm"]))
    if natural:
        ref["mins"] = (ref["end_t"] - ref["dta_t"]).dt.total_seconds() / 60          # the clock readings
    else:
        # elapsed time: CCRS decision and outcome times are UTC, the platform and the unit feed local
        raw = {c: pd.to_datetime(ref[c].replace("", None), format="%Y-%m-%d %H:%M") for c in ("dta_at", "outcome_at")}
        lon = lambda x: x.dt.tz_localize("Europe/London", ambiguous="raise", nonexistent="raise").dt.tz_convert("UTC")
        dta_u = raw["dta_at"].dt.tz_localize("UTC").where(leg, lon(ref["dta_t"]))
        out_u = raw["outcome_at"].dt.tz_localize("UTC").where(leg & ~adm_leg, lon(ref["end_t"]))
        ref["mins"] = (out_u - dta_u).dt.total_seconds() / 60
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


def islands(con, merge=True, table="st2"):
    """Stays as islands of contiguous rows of one patient in one unit (or every row, merge=False)."""
    if not merge:
        return con.execute("SELECT unit_code, patient_key, admitted_at a, discharged_at b, admission_type t, "
                           "referral_id r FROM " + table).df()
    q = """
    WITH s AS (SELECT unit_code, patient_key, admitted_at, discharged_at, admission_type, referral_id,
                      LAG(discharged_at) OVER (PARTITION BY unit_code, patient_key ORDER BY admitted_at, stay_id) prev
               FROM TABLE_NAME),
    g AS (SELECT *, SUM(CASE WHEN prev = admitted_at THEN 0 ELSE 1 END)
                     OVER (PARTITION BY unit_code, patient_key ORDER BY admitted_at ROWS UNBOUNDED PRECEDING) grp FROM s)
    SELECT unit_code, patient_key, MIN(admitted_at) a, MAX(discharged_at) b,
           ARG_MIN(admission_type, admitted_at) t, ARG_MIN(referral_id, admitted_at) r
    FROM g GROUP BY unit_code, patient_key, grp"""
    return con.execute(q.replace("TABLE_NAME", table)).df()


TYPE_READINGS = {"local": ["01", "04", "05"], "t04": ["04"], "planned": ["03", "04", "05"],
                 "not02": ["01", "03", "04", "05", "06"]}


def placed_by_unit(con, isl, reading="referral"):
    """Admission minutes per unit of stays the unit's own trust placed: not referred by another trust (or, under a
    type reading, coded with one of that reading's admission types)."""
    rt = dict(con.execute("SELECT referral_id, referring_trust FROM ref").fetchall())
    ut = dict(con.execute("SELECT DISTINCT unit_code, trust_code FROM reg").fetchall())
    out = {}
    for u, g in isl.groupby("unit_code"):
        if reading != "referral":
            keep = g["t"].isin(TYPE_READINGS[reading])
        else:
            keep = g["r"].fillna("").map(lambda x: rt.get(x, ut.get(u)) == ut.get(u)) if "r" in g else True
        out[u] = np.sort(g[keep]["a"].values.astype("datetime64[m]").astype(np.int64))
    return out


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


def classify(con, W, current_register=False, merge=True, hourly=False, reading="referral", table="st2"):
    reg = own_unit_table(con, current_register)
    isl = islands(con, merge, table)
    ret = con.execute("SELECT * FROM ret").df()
    cen = Census(islands(con, True, table), ret)
    plan = placed_by_unit(con, isl, reading)
    anyadm = {u: np.sort(g["a"].values.astype("datetime64[m]").astype(np.int64)) for u, g in isl.groupby("unit_code")}
    own, emp, alloc, alloc_any, v08 = [], [], [], [], []
    for r in W.itertuples():
        d = str(r.dday)[:10]
        rows = reg[(reg.trust_code == r.referring_trust) & (reg.valid_from <= d) &
                   ((reg.valid_to == "") | (reg.valid_to >= d))] if not current_register else \
            reg[reg.trust_code == r.referring_trust]
        units = sorted(rows.unit_code.unique())
        a = np.datetime64(r.dta_t, "m").astype(np.int64)
        b = np.datetime64(r.end_t, "m").astype(np.int64)
        e = al = an = v = False
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
            for arr, flag in ((plan.get(u), "al"), (anyadm.get(u), "an")):
                if arr is None:
                    continue
                k = np.searchsorted(arr, a, side="right")
                if k < len(arr) and arr[k] < b:
                    if flag == "al":
                        al = True
                    else:
                        an = True
        own.append(bool(units))
        emp.append(e)
        alloc.append(al)
        alloc_any.append(an)
        v08.append(v)
    W = W.copy()
    W["own"], W["empty"], W["alloc"], W["alloc_any"], W["v08"] = own, emp, alloc, alloc_any, v08
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
    W["empty_own"] = classify(con, build_waits(con), table="st2_own")["empty"].values
    W["empty_all"] = classify(con, build_waits(con), table="st2_all")["empty"].values
    conf_m = W["empty_own"] | W["alloc"]
    died = W["died30"]
    y3 = W["year"] == 3
    # the rungs on the latest four quarters
    r0 = per_trust(W, y3 & died)
    r1 = per_trust(W, y3 & died & W["own"] & W["v08"])
    r2 = per_trust(W, y3 & died & W["own"] & W["empty"])
    r3 = per_trust(W, y3 & died & W["own"] & (W["empty"] | W["alloc_any"]))
    r4 = per_trust(W, y3 & died & W["own"] & conf_m)
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
    claim("killer of the structural reading: RIS-ACC reported no empty bed at 08:00 on any day RIS referrals waited",
          len(rr) > 0 and (rr.occ >= rr.beds).all(), "%d days" % len(rr))
    brk = W[y3 & (W.referring_trust == "BRK")]
    claim("killer of rung 1: BRK-ACC full at every moment of every BRK long wait", not brk["empty"].any(), len(brk))
    ris = W[y3 & (W.referring_trust == "RIS")]
    stn = W[y3 & (W.referring_trust == "STN")]
    claim("killer of rung 2: through every STN long wait STN-ACC held a bed assigned to a Stennock patient still in "
          "theatre (the theatre extract), full by assignment and admitting no one",
          stn["empty_own"].all() and not stn["empty"].any() and not stn["alloc_any"].any(), len(stn))
    # killer of rung 3: every admission inside a RIS long wait is another trust's patient in the bureau's audit
    isl = islands(con, True)
    rt = dict(con.execute("SELECT referral_id, referring_trust FROM ref").fetchall())
    tx = pd.read_csv(Path(T) / F["transfers"], dtype=str, keep_default_na=False)
    lk = dict(con.execute("SELECT temporary_key, verified_key FROM links").fetchall())
    audit = {(r.patient_key, r.to_unit, r.bed_confirmed_at) for r in tx.itertuples(index=False)}
    ri = isl[isl.unit_code == "RIS-ACC"].copy()
    ri["m"] = ri["a"].values.astype("datetime64[m]").astype(np.int64)
    bad = n_in = 0
    for r in ris.itertuples():
        a = np.datetime64(r.dta_t, "m").astype(np.int64)
        b = np.datetime64(r.end_t, "m").astype(np.int64)
        for x in ri[(ri.m > a) & (ri.m < b)].itertuples():
            n_in += 1
            when = pd.Timestamp(x.a).strftime("%Y-%m-%d %H:%M")
            if rt.get(x.r or "", "RIS") == "RIS" or (lk.get(x.patient_key, x.patient_key), "RIS-ACC", when) not in audit:
                bad += 1
    claim("killer of rung 3: every admission inside a RIS long wait is a patient referred by another trust, in the "
          "bed bureau's transfer audit", n_in > 0 and bad == 0, "%d admissions" % n_in)
    # the holds themselves: own-trust theatre cases leaving recovery after the bed was assigned
    hold = con.execute("SELECT s.unit_code, COUNT(*) n, MIN(CAST(s.admitted_at AS TIME)) t0 FROM st2 s JOIN st2_own o "
                       "USING (stay_id) WHERE o.admitted_at <> s.admitted_at GROUP BY 1").df()
    claim("own holds: only at STN-ACC, every bed assigned at 08:10 or later",
          list(hold.unit_code) == ["STN-ACC"] and str(hold.t0.iloc[0]) >= "08:10:00", hold.to_dict("records"))
    codes_ris = set()
    for r in ris[ris.died30].itertuples():
        a = np.datetime64(r.dta_t, "m").astype(np.int64)
        b = np.datetime64(r.end_t, "m").astype(np.int64)
        for x in ri[(ri.m > a) & (ri.m < b)].itertuples():
            codes_ris.add((x.t, rt.get(x.r or "", "")))
    claim("RIS's in-wait admissions include planned transfers in (03) referred by other trusts",
          any(c[0] == "03" and c[1] != "RIS" for c in codes_ris), sorted(codes_ris)[:6])
    rr_ = per_trust(W, y3 & died & W["own"] & (W["empty_all"] | W["alloc_any"]))
    got = top2({t: rr_.get(t, 0) for t in CLAIMS["y3"]})
    claim("every held bed read empty (the bureau's too): %s %d over %s %d" % CLAIMS["every_hold_empty"],
          got == CLAIMS["every_hold_empty"], got)
    for rd, want in CLAIMS["readings"].items():
        Wr = W if rd == "referral" else classify(con, build_waits(con), reading=rd)
        rr_ = per_trust(Wr, (Wr.year == 3) & Wr.died30 & Wr["own"] & (Wr["empty"] | Wr["alloc"]))
        got = top2({t: rr_.get(t, 0) for t in CLAIMS["y3"]})
        claim("own placement read as %s: %s %d over %s %d" % ((rd,) + want), got == want, got)
    # the device organs the record leans on: legacy transfers dated from the arrival, deaths only by discharge method
    held = con.execute("SELECT COUNT(*) FROM st JOIN st2 USING (stay_id) "
                       "WHERE st.admitted_at <> st2.admitted_at").fetchone()[0]
    claim("legacy transfers: %d bed rows re-dated from the arrival to the bureau's allocation" % held,
          held >= CLAIMS["held_legacy_transfers_min"], held)
    nl = con.execute("SELECT COUNT(DISTINCT patient_key) FROM ref WHERE patient_key LIKE 'U%' AND patient_key NOT IN "
                     "(SELECT temporary_key FROM links)").fetchone()[0]
    claim("temporary keys the links never resolve: %d, each death on a spell ending in death" % nl,
          nl == CLAIMS["never_linked"])
    # the graded figures
    y3t = {t: (W[y3 & (W.referring_trust == t)]["person"].nunique(),
               W[y3 & died & (W.referring_trust == t)]["person"].nunique(),
               W[y3 & died & (W.referring_trust == t) & conf_m]["person"].nunique())
           for t in CLAIMS["y3"]}
    claim("latest four quarters: patients, deaths, confirmable per trust", y3t == CLAIMS["y3"])
    rec = {t: (W[W.referring_trust == t]["person"].nunique(), W[died & (W.referring_trust == t)]["person"].nunique(),
               W[died & (W.referring_trust == t) & conf_m]["person"].nunique())
           for t in CLAIMS["record"]}
    claim("record: 24 trust figures (3a, 3b, 3c)", rec == CLAIMS["record"], rec)
    tot = tuple(sum(v[i] for v in rec.values()) for i in range(3))
    claim("record totals 2163 / 629 / 148", tot == CLAIMS["record_total"], tot)
    by = {}
    for y in (1, 2, 3):
        m = W["year"] == y
        by[y] = (W[m]["person"].nunique(), W[m & died]["person"].nunique(),
                 W[m & died & conf_m]["person"].nunique())
    claim("by four-quarter year", by == CLAIMS["by_year_total"], by)
    # the hourly clean-data replacement names G on its rung and leaves the call alone
    Wh = classify(con, build_waits(con), hourly=True)
    rh = per_trust(Wh, (Wh.year == 3) & Wh.died30 & Wh["own"] & Wh["empty"])
    claim("clean-data test: hourly return names PRW, the call stays STN", top2({t: rh.get(t, 0) for t in CLAIMS["y3"]})[0] == "PRW")
    # the natural path: every field as it stands, current register, rows as admissions, deaths per referral row
    Wn = classify(con, build_waits(con, natural=True), current_register=True, merge=False, table="st")
    Wn["empty_own"] = classify(con, build_waits(con, natural=True), current_register=True, merge=False,
                               table="st_own")["empty"].values
    nat = (len(Wn), int(Wn["died30"].sum()), int((Wn["died30"] & (Wn["empty_own"] | Wn["alloc"])).sum()))
    claim("natural path totals %d / %d / %d" % CLAIMS["natural_total"], nat == CLAIMS["natural_total"], nat)
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
    rf = con.execute("SELECT referral_id, referring_trust t, received_at, outcome_at FROM ref WHERE level_of_care = '3' "
                     "AND received_at >= '2024-04-01' AND received_at < '2026-07-01'").df()
    rf["m"] = rf["received_at"].str[:7]
    rc = pd.to_datetime(rf["received_at"], format="%Y-%m-%d %H:%M")
    oc = pd.to_datetime(rf["outcome_at"].replace("", None), format="%Y-%m-%d %H:%M")
    cc = rf["referral_id"].str.startswith("CC")
    z = lambda x: x.dt.tz_localize("Europe/London", ambiguous="raise", nonexistent="raise").where(
        ~cc, x.dt.tz_localize("UTC").dt.tz_convert("Europe/London"))
    rf["k"] = ((z(oc) - z(rc)).dt.total_seconds() > 240 * 60).astype(int)
    g = rf.groupby(["m", "t"])["k"].sum()
    ok = all(g.get((r.Month, r._2), 0) == r._4 for r in cap.itertuples())
    naive = rf.assign(kn=((oc - rc).dt.total_seconds() > 240 * 60).astype(int)).groupby(["m", "t"])["kn"].sum()
    differ = sum(1 for r in cap.itertuples() if naive.get((r.Month, r._2), 0) != r._4)
    claim("capacity report: referral waits reproduce from the referral log in elapsed time", ok,
          "%d trust-months differ on the clock readings" % differ)
    n = len(RESULTS)
    print("\n%d claims, %d failed" % (n, n - sum(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "target")))
