"""Build task132's evidence pack into <out>/ (default: task132/target)."""
import argparse
import datetime as dt
import json
import os
import shutil
import sys
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim as S
import extracts as X
import docs as D
import distract as Q
import postprocess as P

TASK = os.path.dirname(HERE)
TZ = ZoneInfo("America/Toronto")
FILES = {
    "register": "protection_asset_register_2026-09-30.csv",
    "hist": "psu_rotating_item_history_2021-01_2026-09.csv",
    "wo": "eam_work_orders_protection_2021-01_2026-09.csv",
    "subs": "substations.csv",
    "prog": "protection_renewal_program_2026.xlsx",
    "eol": "veldtek_vpr340_eol_notice.pdf",
    "procedure": "AM-PC-014_obsolete_spares_final_buy.docx",
    "stock": "spares_stock_2026-09-30.csv",
    "rma": "veldtek_rma_log_vpr340_psu.xlsx",
    "dictionary": "eam_extract_dictionary.txt",
    "trips": "feeder_relay_operations_2025.csv",
    "compliance": "pc_relay_maintenance_compliance_2025.xlsx",
}
DISTRACTORS = ["rma", "trips", "compliance"]
# (created, modified) local Eastern time, author, last saved by, company (Excel stamps the second, Word the minute)
OFFICE = {
    "prog": ((2026, 3, 20, 9, 12, 41), (2026, 3, 24, 16, 40, 17), "Kurt Allison", "Rachael Villanueva", "Tarrock Hydro Distribution"),
    "rma": ((2015, 2, 9, 14, 31, 22), (2026, 9, 29, 11, 2, 38), "Veldtek Service Centre", "Veldtek Service Centre",
            "Veldtek Protection Systems"),
    "compliance": ((2026, 2, 3, 10, 25, 9), (2026, 2, 27, 15, 5, 52), "Rachael Villanueva", "Kurt Allison", "Tarrock Hydro Distribution"),
    "procedure": ((2019, 5, 14, 10, 40, 0), (2026, 4, 14, 11, 20, 0), "Kurt Allison", "Kurt Allison", "Tarrock Hydro Distribution"),
}
# the Excel that last saved each workbook: Kurt's on a second screen, Rachael's laptop, and Veldtek's service-centre
# register, started in 2015 from an Excel 2010 template and still carrying its theme
EXCEL = {
    "prog": dict(rup="27328", window=(28680, -120, 29040, 15720), docid="13_ncr:1_", coauth="47"),
    "compliance": dict(rup="27130", window=(-108, -108, 23256, 12456), docid="11_", coauth="47"),
    "rma": dict(rup="27425", lowest="5", theme="2007", theme_version="124226", window=(-120, -120, 20730, 11160),
                docid="8_", coauth="47"),
}
MTIMES = {
    "register": (2026, 10, 1, 6, 12), "hist": (2026, 10, 1, 9, 41), "wo": (2026, 10, 1, 6, 14), "subs": (2026, 10, 1, 6, 11),
    "prog": (2026, 3, 24, 16, 40), "eol": (2026, 8, 20, 9, 5), "procedure": (2026, 4, 14, 11, 20),
    "stock": (2026, 9, 30, 17, 25), "rma": (2026, 9, 29, 11, 2), "dictionary": (2026, 10, 1, 6, 10),
    "trips": (2026, 1, 14, 10, 20), "compliance": (2026, 2, 27, 15, 5),
}
# the notice as Veldtek's lifecycle team saved it from Word, 9:05 on 20 August 2026 Eastern time
EOL_SAVED = (2026, 8, 20, 9, 5, 37)
EOL_ID = "6D1F4C0A-92B8-4E57-A1C4-D90E3B7F2A61"


def utc(t):
    return dt.datetime(*t, tzinfo=TZ).astimezone(dt.timezone.utc).timetuple()[:6]


def candidates(sp):
    """modules fitted as replacements before the go-live and still in place at it (their legacy date is loaded)"""
    rem = sp["removed"]
    return sp[(sp["module"] > 0) & (sp["fitted"] < W.MIGRATION)
              & (rem.isna() | rem.map(lambda d: d is not None and not isinstance(d, float) and d >= W.MIGRATION))].index.tolist()


def simulate():
    rng = np.random.default_rng(W.SEED)
    subs = S.substations(rng)
    fl = S.fleet(rng, subs)
    prog, extra = S.programme(rng, fl, subs)
    fl, prog = S.cutovers(subs, fl, prog)
    sp, f = S.modules(rng, fl, prog)
    # rounding knob: the legacy fitted date of a module that was already a replacement at go-live, moved a month
    # (a service-bulletin fit stays on a working day in its new month)
    cand = candidates(sp)
    adj = np.random.default_rng([W.SEED, 10])
    for k, shift in W.TUNE:
        i = cand[k]
        d = sp.at[i, "fitted"]
        m = S.month_add(dt.date(d.year, d.month, 1), shift)
        nd = dt.date(m.year, m.month, min(d.day, 28))
        if sp.at[i - 1, "reason"] == "CAMPAIGN" and not S.is_bday(nd):
            nd = S.bday_like(adj, nd)
        sp.at[i, "fitted"] = nd
    return rng, subs, fl, prog, extra, sp, f


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    rng, subs, fl, prog, extra, sp, f = simulate()
    rng2 = np.random.default_rng(W.SEED + 1)
    p = lambda k: os.path.join(out, FILES[k])

    plan = X.bay_plan(fl, prog)
    reg, key2aid, relay_mfg, yearonly = X.register(rng2, subs, fl, prog, plan)
    reg.to_csv(p("register"), index=False)
    eq = X.equipment(subs, reg)
    region = dict(zip(subs["sub_code"], subs["region"]))
    sub_of = {int(k): s for k, s in zip(fl["relay_key"], fl["sub_code"])}
    depot_of = {k: X.STORES[region[s]] for k, s in sub_of.items()}
    sp2, ships = X.psu_cycle(sp, f, key2aid, relay_mfg, sub_of, depot_of)
    fits = X.refit_plan(f, sp)
    rebuilt = set(prog["sub_code"][prog["cut_days"].map(lambda d: isinstance(d, list))])
    wo, keymap = X.work_orders(subs, reg, f, sp2, ships, rebuilt, fits, eq)
    wo.to_csv(p("wo"), index=False)
    X.module_history(sp2, keymap, fits, yearonly).to_csv(p("hist"), index=False)
    subs[["sub_code", "sub_name", "region", "legacy_region", "station_type"]].to_csv(p("subs"), index=False)
    rma = X.rma_log(ships, keymap)
    X.stock(int((rma["result"] == "OPEN").sum())).to_csv(p("stock"), index=False)
    X.rma_xlsx(p("rma"), rma)
    D.programme_xlsx(p("prog"), np.random.default_rng(W.SEED + 4), prog, subs, reg, plan)
    D.eol_pdf(p("eol"))
    D.procedure_docx(p("procedure"))
    D.dictionary_txt(p("dictionary"))
    Q.trip_operations_csv(p("trips"), np.random.default_rng(W.SEED + 2), reg)
    Q.test_compliance_xlsx(p("compliance"), reg, subs, wo)

    for k, fn in FILES.items():
        path = p(k)
        if fn.endswith(".xlsx"):
            c, m, a, b, co = OFFICE[k]
            P.normalize_xlsx(path, a, b, utc(c), utc(m), company=co, seed=fn, excel=EXCEL[k])
        elif fn.endswith(".docx"):
            c, m, a, b, co = OFFICE[k]
            P.normalize_docx(path, a, b, utc(c), utc(m), revision=23, total_time=312,
                             title="AM-PC-014 Obsolete protection spares: final-buy sizing", company=co, seed="AM-PC-014")
        elif fn.endswith(".pdf"):
            P.normalize_pdf(path, "Product end-of-life notice EOL-2026-07", "George Ray",
                            dt.datetime(*EOL_SAVED, tzinfo=TZ), EOL_ID)
        ts = dt.datetime(*MTIMES[k], tzinfo=TZ).timestamp()
        os.utime(path, (ts, ts))
    return subs, fl, prog, sp, f, reg, wo


def write_metadata():
    meta = {
        "task": "task132",
        "title": "VPR-340 power-supply modules: the last-time buy",
        "domain": "Energy Systems & Utilities",
        "subdomain": "asset-condition-maintenance",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": W.ASOF.isoformat(),
        "deliverables": ["vpr340_psu_final_buy.xlsx", "psu_last_time_buy_memo.docx"],
        "input_files": [{"path": FILES[k], "format": FILES[k].rsplit(".", 1)[1]} for k in sorted(FILES, key=lambda k: FILES[k])],
        "distractors": [FILES[k] for k in DISTRACTORS],
        "provenance": "Fully constructed pack (dataset-generation section 2): every extract is generated by "
                      "task132/generator from a simulated protection-relay fleet, its power-supply modules, work-order "
                      "history and renewal program for a fictional Ontario distribution utility (Tarrock Hydro "
                      "Distribution) and its fictional relay vendor (Veldtek Protection Systems); documents written "
                      "for the fiction. No real utility's data.",
        "license": "Constructed data, released with the task (CC BY 4.0).",
        "created": "2026-10-11",
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    a = ap.parse_args()
    build(a.out)
    if a.out == os.path.join(TASK, "target"):
        write_metadata()
    print("built", a.out)
