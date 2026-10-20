"""Write the task249 pack into a target folder: the simulated rivers, the records, the published loads computed from
the shipped record the way the company computes them, and the documents.   B.run(target) -> world"""
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import docs as D
import params as P
import postprocess
import records as R
import sim

FILES = dict(
    record="sediment_stations_15min_2025-2027.parquet",
    field="field_samples_2025-2027.csv",
    lims="lims_ssc_results_2025-2027.xlsx",
    report="suspended_sediment_loads_2027.pdf",
    procedure="SMP-03_surrogate_load_procedure_v3.pdf",
    register="station_register.xlsx",
    log="station_maintenance_log_2025-2027.csv",
    batches="lab_batch_export_2027.csv",
    statement="SMA_quality_statement_2027.pdf",
    request="spring_review_request.eml",
    dictionary="data_dictionary.md",
    precip="precipitation_daily_2025-2027.csv",
    reservoirs="reservoir_levels_daily_2025-2027.csv",
)
PACK = ["request", "procedure", "report", "register", "record", "field", "lims", "batches", "statement", "log",
        "dictionary", "precip", "reservoirs"]
DISTRACTORS = ["precip", "reservoirs"]
CONTEXT = ["report"]
STAMP_PDF = {"procedure": "2027-01-18T10:22:00", "report": "2028-02-15T09:05:00", "statement": "2028-01-18T13:40:00"}


def publish(rec, S):
    """the company's 2027 loads: log10 concentration on log10 turbidity at the reading nearest each sample, all
    accepted samples of 2025 to 2027, Duan's smearing, every 15-minute interval of 2027"""
    out = {}
    for key in P.KEYS:
        code = P.CODE[key]
        r = rec[rec["station"] == code].drop_duplicates(["time_utc"]).set_index("time_utc")
        s = S[S["key"] == key]
        t = pd.to_datetime(s["utc"], utc=True).dt.round("15min")
        T = r.loc[t, "turbidity_fnu"].to_numpy()
        y = np.log10(s["ssc_lab"].to_numpy())
        x = np.log10(T)
        X = np.c_[np.ones(len(x)), x]
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        res = y - X @ b
        bcf = float(np.mean(10 ** res))
        r2 = 1 - np.sum(res ** 2) / np.sum((y - y.mean()) ** 2)
        y27 = r[r.index >= pd.Timestamp("2027-01-01", tz="UTC")]
        a4, b4, c4 = round(b[0], 4), round(b[1], 4), round(bcf, 4)
        load = float(np.sum(10 ** b[0] * y27["turbidity_fnu"].to_numpy() ** b[1] * bcf
                            * y27["discharge_m3s"].to_numpy()) * 900 / 1e6)
        out[key] = {"n": int(len(s)), "a": a4, "b": b4, "bcf": c4, "r2": float(r2), "load_t": int(round(load)),
                    "load_exact": load}
    return out


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: v for k, v in FILES.items()}
    W = sim.world()
    H, parts = {}, []
    for k in P.KEYS:
        h = R.record_history(k, W[k], np.random.default_rng(P.SEED[k] + 17))
        H[k], df = R.settle_quarter_hours(
            k, W[k], h, lambda hh, k=k: R.logger_record(k, W[k], hh, np.random.default_rng(P.SEED[k] + 23)))
        parts.append(df)
    rec = pd.concat(parts, ignore_index=True)
    tab = pa.Table.from_pandas(rec, preserve_index=False)
    pq.write_table(tab, os.path.join(target, F["record"]), compression="snappy", row_group_size=262144,
                   use_dictionary=True, write_statistics=True, store_schema=False)
    rng = np.random.default_rng(24901)
    S = R.samples(W, rng)
    R.field_sheet(S, rng).to_csv(os.path.join(target, F["field"]), index=False, encoding="utf-8")
    old, new = R.lims(S, rng)
    D.lims_xlsx(os.path.join(target, F["lims"]), old, new)
    groups, truth = R.batches(S, rng)
    truth = R.plant_failures(truth, rng)
    R.batch_export(groups, truth).to_csv(os.path.join(target, F["batches"]), index=False, encoding="utf-8")
    reg = R.register(H)
    D.register_xlsx(os.path.join(target, F["register"]), reg)
    R.maintenance_log(H, rng).to_csv(os.path.join(target, F["log"]), index=False, encoding="utf-8")
    R.precipitation(sim.storms(), rng).to_csv(os.path.join(target, F["precip"]), index=False, encoding="utf-8",
                                             sep=";", decimal=",")
    R.reservoir_levels(rng).to_csv(os.path.join(target, F["reservoirs"]), index=False, encoding="utf-8")
    pub = publish(rec, S)
    D.request(os.path.join(target, F["request"]), F)
    D.procedure(os.path.join(target, F["procedure"]), F)
    D.report(os.path.join(target, F["report"]), F, pub)
    D.lab_statement(os.path.join(target, F["statement"]), F, int((S["year"] == 2027).sum()))
    D.dictionary(os.path.join(target, F["dictionary"]), F)
    for k, stamp in STAMP_PDF.items():
        producer = "Microsoft Word 2019"
        postprocess.scrub(os.path.join(target, F[k]), producer, stamp)
    for k, created, modified, company in (("register", "2025-01-09T08:30:00Z", "2026-11-20T14:05:00Z", P.ORG),
                                          ("lims", "2025-02-03T07:45:00Z", "2028-01-12T15:20:00Z", P.LAB)):
        postprocess.scrub(os.path.join(target, F[k]), company, modified[:10])
        postprocess.finish_office(os.path.join(target, F[k]), created, modified, company)
    return {"W": W, "H": H, "S": S, "truth": truth, "groups": groups, "pub": pub, "F": F}
