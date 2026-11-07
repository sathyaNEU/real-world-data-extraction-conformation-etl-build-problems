"""task212 build: python3 build.py writes target/, golden/, generator/figures.json, metadata.json and target.zip."""
import json
import os
import shutil
import time
import datetime as dt
import numpy as np
import pandas as pd
import world
import records
import asks
import docs
import analysis as A

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GLD = os.path.join(TASK, "golden")
PACK_MTIME = time.mktime((2026, 10, 27, 9, 30, 0, 0, 0, -1))
GOLD_MTIME = time.mktime((2026, 10, 29, 17, 10, 0, 0, 0, -1))
SEED = world.SEED

FILES = {
    "findings": "audit_findings_q3_2026.parquet",
    "headers": "audit_headers_q3_2026.csv",
    "build_log": "cage_build_log_q3_2026.parquet",
    "dws": "dws_induction_q3_2026.parquet",
    "manifest": "shipment_lines_q3_2026.parquet",
    "accounts": "accounts_register.xlsx",
    "hubs": "hub_register.csv",
    "plan": "peak_plan_2026.xlsx",
    "programme": "sortation_survey_programme_2026.pdf",
    "procedure": "outbound_cage_audit_procedure_v4.pdf",
    "report2025": "survey_report_basauri_2025.pdf",
    "cases": "damage_claims_cases_2026-10-23.csv",
    "transfers": "claims_transfers_2026.xlsx",
    "refunds": "card_refunds_settlement_2026-07-01_2026-10-22.csv",
    "tracking": "tracking_events_claimed_parcels.parquet",
    "terms": "flat_rate_damage_terms.xlsx",
    "claims_note": "damage_claims_handling_note.pdf",
    "events": "sorter_event_log_q3_2026.csv",
    "orders": "sorter_work_orders_q3_2026.xlsx",
    "standard": "sorter_stoppage_reporting_standard.pdf",
    "visits": "sorter_maker_visits_2026.xlsx",
}
DELIVERABLES = {"note": "survey_case_note.pdf", "workbook": "hub_damage_q3_2026.xlsx"}


def edge(v, u):
    """Distance from v to the nearest edge of its printed cell, as a share of the unit."""
    return (u / 2 - abs(v - round(v / u) * u)) / u


def nudge_claims(t, flat):
    """Seat every hub's euros inside its euro: one ordinary business case per hub, paid once in full by the cutoff,
    moves by the cents that put the hub's total 0.17 above a whole euro."""
    _, _, _, _, paid = asks.claim_records(t, flat, SEED)
    T = asks.claims_truth(t, paid)
    for h in world.HUB_KEYS:
        e = float(T.loc[h, "claims_eur"])
        delta = round(round(e) + 0.17 - e, 2)
        m = (t.sort_hub == h) & (t.kind == "EMPRESA") & (t.status == "APPROVED") & ~t.reopen & \
            t.night.between(asks.Q3[0], asks.Q3[1]) & (t.decided <= dt.date(2026, 10, 1)) & \
            (t.barcode.map(paid).round(2) == t.amount.round(2)) & (t.amount > 5)
        i = t[m].index[-1]
        t.at[i, "amount"] = round(float(t.at[i, "amount"]) + delta, 2)
    _, _, _, _, paid = asks.claim_records(t, flat, SEED)
    T = asks.claims_truth(t, paid)
    assert all(edge(float(T.loc[h, "claims_eur"]), 1.0) >= 0.3 for h in world.HUB_KEYS), T
    return t


def nudge_stops(st, gp):
    """Seat every hub's hours inside its tenth: one short ordinary logged stoppage per hub, with room before the next,
    ends that many seconds later or earlier."""
    ev, wos = asks.stoppage_records(st.copy(), gp, SEED)
    G, _ = asks.stoppages_golden(ev, wos)
    for h in world.HUB_KEYS:
        v = float(G.loc[h, "hours_stood"])
        secs = int(round((round(v, 1) + 0.017 - v) * 3600))
        s = st[(st.hub == h)].sort_values("t0")
        nxt = s.t0.shift(-1)
        room = (nxt - s.t1).dt.total_seconds()
        dur = (s.t1 - s.t0).dt.total_seconds()
        m = ~s.in_gap & ~s.safety & s.night.between(asks.Q3[0], asks.Q3[1]) & (room > 600) & \
            (dur + secs > 90) & (dur + secs < 540) & (dur < 540)
        i = s[m].index[len(s[m]) // 2]
        st.at[i, "t1"] = st.at[i, "t1"] + pd.Timedelta(seconds=secs)
    st["hours"] = (st.t1 - st.t0).dt.total_seconds() / 3600.0
    ev, wos = asks.stoppage_records(st.copy(), gp, SEED)
    G, _ = asks.stoppages_golden(ev, wos)
    assert all(edge(float(G.loc[h, "hours_stood"]), 0.1) >= 0.3 for h in world.HUB_KEYS), G
    return st


def systems():
    """Every record system cut from one world."""
    W = world.simulate(SEED)
    R = records.cut(W, SEED)
    t, flat = asks.claims(W["accounts"], W["depots"], SEED)
    t = nudge_claims(t, flat)
    cases, pays, refunds, trk, paid = asks.claim_records(t, flat, SEED)
    st, gp = asks.stoppages(SEED)
    st = nudge_stops(st, gp)
    events, wos = asks.stoppage_records(st, gp, SEED)
    return dict(W=W, R=R, t=t, flat=flat, cases=cases, pays=pays, refunds=refunds, trk=trk, paid=paid, st=st, gp=gp,
                events=events, wos=wos)


def write_records(S):
    p = lambda k: os.path.join(TGT, FILES[k])
    R, W = S["R"], S["W"]
    docs.write_parquet(R["lines"], p("findings"))
    R["audits"].to_csv(p("headers"), index=False)
    bl = R["scans"].copy()
    bl["scan_utc"] = bl.scan_utc.dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    docs.write_parquet(bl, p("build_log"))
    docs.write_parquet(R["dws"], p("dws"))
    docs.write_parquet(R["manifests"], p("manifest"))
    acc = docs.accounts_register(W["accounts"], SEED)
    docs.sheet_xlsx(p("accounts"), [("Accounts", acc)], "Comercial", "2026-10-01T08:12:00Z", "Accounts register",
                    widths={"account_name": 38, "sector": 22, "collection": 20})
    docs.hub_register().to_csv(p("hubs"), index=False)
    cases = S["cases"]
    cases.to_csv(p("cases"), index=False, float_format="%.2f")
    tr = S["pays"]
    docs.sheet_xlsx(p("transfers"), [("Transferencias", tr)], "Tesoreria", "2026-10-23T15:40:00Z", "Claims transfers",
                    widths={"payment_ref": 14, "case_ref": 14, "payee": 10, "value_date": 12, "amount_eur": 12},
                    numfmt={"amount_eur": "#,##0.00"})
    S["refunds"].to_csv(p("refunds"), index=False, float_format="%.2f")
    docs.write_parquet(S["trk"], p("tracking"))
    terms = S["flat"].copy()
    names = docs.accounts_register(W["accounts"], SEED).set_index("account").account_name
    terms.insert(1, "account_name", terms.account.map(names))
    terms = terms.drop(columns=["home_hub"])
    docs.sheet_xlsx(p("terms"), [("Tarifa plana", terms)], "Comercial", "2026-07-03T10:05:00Z",
                    "Flat-rate damage terms", widths={"account_name": 38}, numfmt={"eur_per_carton": "0.00"})
    S["events"].to_csv(p("events"), index=False)
    wo = S["wos"].copy()
    for c in ("reported", "machine_stopped", "machine_running", "closed"):
        wo[c] = pd.to_datetime(wo[c]).dt.strftime("%d/%m/%Y %H:%M").fillna("")
    docs.sheet_xlsx(p("orders"), [("Ordenes", wo)], "Mantenimiento", "2026-10-05T07:55:00Z", "Sorter work orders",
                    widths={"work_order": 11, "site": 18, "asset": 20, "order_type": 12, "reported": 17,
                            "machine_stopped": 17, "machine_running": 17, "closed": 17, "work_done": 30})
    return acc


def main(stage=3):
    for d in (TGT, GLD):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    S = systems()
    acc = write_records(S)
    if stage >= 3:
        import pack
        pack.finish(S, acc, FILES, DELIVERABLES, TGT, GLD, TASK, HERE, PACK_MTIME, GOLD_MTIME)
    print("built", len(os.listdir(TGT)), "files")
    return S


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
