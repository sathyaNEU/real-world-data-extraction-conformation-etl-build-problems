"""Independent verifier: recomputes the call and both asks from target/ alone with code that shares nothing with
analysis.py, pack.py or models.py (pandas readers, group-by calendars, an as-of join for the write-offs), and compares
them with generator/figures.json."""
import decimal
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM = {"FA_PRESUMPTIVE", "BATCHPE", "PE-AUTOSCREEN"}
PUGET_WORK = {"Farm or orchard": 1, "Packing or food processing": 2, "Fishing or seafood": 3,
              "Hotel, resort or ski area": 4, "Logging or tree farm": 5, "Construction": 6, "Health care": 7,
              "Retail or warehouse": 8, "Office, school or government": 9, "Factory": 10, "Other work": 11,
              "Not working or retired": 12}
COLUMBIA_WORK = {"FARM": 1, "PACK": 2, "FISH": 3, "RSRT": 4, "LOGG": 5, "CONS": 6, "HLTH": 7, "RETL": 8, "OFFC": 9,
                 "FACT": 10, "OTHR": 11, "NONE": 12}


def load(target):
    f = {x: os.path.join(target, x) for x in os.listdir(target)}
    find = lambda stem: next(v for k, v in f.items() if k.startswith(stem))
    p = pd.read_csv(find("fac_determinations_2024_2025_puget"), dtype=str, keep_default_na=False)
    w = pd.read_csv(find("fac_determinations_2024_2025_willamette"), dtype=str, keep_default_na=False)
    c = pd.read_csv(find("fac_determinations_2024_2025_columbia"), dtype=str, keep_default_na=False)
    num = lambda s: pd.to_numeric(s.replace("", np.nan))
    a = pd.DataFrame({"hosp": p.hospital_code, "t": pd.to_datetime(p.determined_at), "user": p.user_id,
                      "app": p.application_id, "guar": p.guarantor_id,
                      "res": p.outcome.map({"APPROVED": "A", "DENIED": "D"}).fillna("O"),
                      "kind": p.determination_type, "why": p.denial_reason, "pct": num(p.discount_pct),
                      "rcvd": pd.to_datetime(p.received_date.replace("", np.nan)), "size": num(p.household_size),
                      "annual": num(p.income_3mo) * 4, "work": p.work_type.map(PUGET_WORK)})
    b = pd.DataFrame({"hosp": w.HOSP_ID, "t": pd.to_datetime(w.DET_DATE + " " + w.DET_TIME, format="%m/%d/%Y %H:%M:%S"),
                      "user": w.USER_ID, "app": w.APPL_NO, "guar": w.GUAR_NO,
                      "res": w.RESULT.where(w.RESULT.isin(["A", "D"]), "O"),
                      "kind": np.where(w.USER_ID.isin(SYSTEM), "PRESUMPTIVE",
                                       np.where(w.RECON == "Y", "RECONSIDERATION", "INITIAL")),
                      "why": w.DENY_RSN, "pct": num(w.ADJ_PCT),
                      "rcvd": pd.to_datetime(w.RCVD_DATE.replace("", np.nan), format="%m/%d/%Y"),
                      "size": num(w.HH_SIZE), "annual": num(w.ANN_INC), "work": num(w.WORK_CD)})
    ct = pd.to_datetime(c.ts_utc, utc=True).dt.tz_convert("America/Los_Angeles").dt.tz_localize(None)
    d = pd.DataFrame({"hosp": c.facility, "t": ct, "user": c.staff_key, "app": c.app_ref, "guar": c.guarantor,
                      "res": c.decision.map({"1": "A", "2": "A", "3": "D"}).fillna("O"),
                      "kind": c.kind.map({"new": "INITIAL", "recheck": "RECONSIDERATION", "screen": "PRESUMPTIVE"}),
                      "why": c.reason, "pct": num(c.pct), "rcvd": pd.to_datetime(c.rcvd.replace("", np.nan)),
                      "size": num(c.hh), "annual": num(c.inc_mo) * 12, "work": c.work.map(COLUMBIA_WORK)})
    log = pd.concat([a, b, d], ignore_index=True)
    members = pd.read_excel(find("fac_member_hospitals"), header=2)
    region = dict(zip(members["Code"], members["Region"]))
    xw = pd.read_excel(find("fac_h23_id_crosswalk"), sheet_name="Guarantor numbers", header=3)
    gmap = dict(zip(xw.iloc[:, 2].astype(str), xw.iloc[:, 1].astype(str)))
    return log, pd.read_csv(find("fac_assistance_adjustments"), dtype=str), region, gmap


def half_up(v, places):
    return float(decimal.Decimal(repr(float(v))).quantize(decimal.Decimal(1).scaleb(-places),
                                                          rounding=decimal.ROUND_HALF_UP))


def run(task):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    log, adj, region, gmap = load(os.path.join(task, "target"))
    bad = 0

    # the call
    fr = log[(log.kind == "INITIAL") & log.res.isin(["A", "D"]) & ~log.user.isin(SYSTEM)].copy()
    fr["guide"] = 15650 + 5500 * (fr["size"] - 1)
    fr["lvl"] = fr.annual / fr.guide
    fr["region"] = fr.hosp.map(region)
    fr["month"] = fr.rcvd.dt.month
    cell = fr.groupby(["region", "work", "month"])["lvl"].mean().rename("m").reset_index()
    cell["factor"] = cell.m / cell.groupby(["region", "work"]).m.transform("mean")
    fr = fr.merge(cell[["region", "work", "month", "factor"]], on=["region", "work", "month"], how="left")
    fr["twelve"] = fr.annual / fr.factor
    e = fr[(fr.t.dt.year == 2025) & (fr.twelve / fr.guide <= 2.0)].copy()
    e["owing"] = (e.res == "D") | (e.pct == 25)
    share = 100 * e.groupby("hosp").owing.mean()
    q = sorted(c for c, v in share.items() if v >= 6)
    for code in sorted(share.index):
        ok = abs(share[code] - fig["measure"][code]) < 1e-3
        bad += not ok
        print("%s share %7.3f  figures %7.3f  %s" % (code, share[code], fig["measure"][code], "ok" if ok else "MISMATCH"))
    ok = q == fig["call"]["qualify"] and len(q) == fig["call"]["count"]
    bad += not ok
    print("call: %d %s  %s" % (len(q), q, "ok" if ok else "MISMATCH"))

    # Ask A: one amount per write-off (number and posting date), credited by an as-of join to the household's approval
    adj = adj.drop_duplicates()
    adj["amount"] = adj.amount.astype(float)
    adj["posted"] = pd.to_datetime(adj.posted_date)
    keyg = log[["hosp", "app", "guar"]].drop_duplicates(["hosp", "app"])
    keyg["hh"] = np.where(keyg.hosp == "H23", keyg.guar.map(gmap).fillna(keyg.guar), keyg.guar)
    appr = log[log.res == "A"][["hosp", "app", "guar", "t", "user"]].copy()
    appr["hh"] = np.where(appr.hosp == "H23", appr.guar.map(gmap).fillna(appr.guar), appr.guar)
    appr["dday"] = pd.to_datetime(appr.t.dt.date).astype("datetime64[ns]")
    wo = adj[adj.adjustment_code == "FAWO"].drop_duplicates(["hospital_code", "application_id", "posted_date"])
    wo = wo.merge(keyg, left_on=["hospital_code", "application_id"], right_on=["hosp", "app"], how="left")
    wo["edge"] = (wo.posted - pd.Timedelta(days=1)).astype("datetime64[ns]")
    wo = wo.sort_values("edge")
    ap = appr.sort_values("dday")[["hosp", "hh", "dday", "app", "user"]].rename(columns={"app": "by_app"})
    wo = pd.merge_asof(wo, ap, left_on="edge", right_on="dday", by=["hosp", "hh"], direction="backward")
    wo["counts"] = (~wo.user.isin(SYSTEM)) & (wo.dday.dt.year == 2025)
    gain = wo[wo.counts].groupby("hospital_code").amount.sum()
    ev = wo[["hospital_code", "application_id", "posted", "by_app", "counts"]]
    lines = adj[adj.adjustment_code == "FAWO"][["hospital_code", "application_id", "account_number", "posted"]]
    lines = lines.merge(ev, on=["hospital_code", "application_id", "posted"])
    rv = adj[adj.adjustment_code == "FAWR"].copy()
    rv["edge"] = (rv.posted - pd.Timedelta(days=1)).astype("datetime64[ns]")
    rv = rv.sort_values("edge")
    lines = lines.sort_values("posted").rename(columns={"posted": "wo_posted"})
    lines["wo_posted"] = lines.wo_posted.astype("datetime64[ns]")
    rv = pd.merge_asof(rv, lines[["hospital_code", "account_number", "wo_posted", "counts"]], left_on="edge",
                       right_on="wo_posted", by=["hospital_code", "account_number"], direction="backward")
    loss = rv[rv["counts"].fillna(False).astype(bool)].groupby("hospital_code").amount.sum()
    net = gain.sub(loss, fill_value=0.0)
    for code in fig["ask_a"]:
        v = half_up(net.get(code, 0.0) / 1000.0, 1)
        ok = v == fig["ask_a"][code]
        bad += not ok
        if not ok:
            print("Ask A %s %.1f against %.1f MISMATCH" % (code, v, fig["ask_a"][code]))

    # Ask B: denials for documents not received, the reason list renumbered on 1 July 2025
    dn = log[(log.res == "D") & ~log.user.isin(SYSTEM) & (log.t.dt.year == 2025)].copy()
    want = np.where(dn.t < pd.Timestamp("2025-07-01"), "2", "1")
    cnt = dn[dn.why.values == want].groupby("hosp").size()
    for code in fig["ask_b"]:
        ok = int(cnt.get(code, 0)) == fig["ask_b"][code]
        bad += not ok
        if not ok:
            print("Ask B %s %d against %d MISMATCH" % (code, int(cnt.get(code, 0)), fig["ask_b"][code]))
    print("asks: %d hospital figures each checked" % len(fig["ask_a"]))
    print("verify:", "PASS" if bad == 0 else "FAIL %d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
