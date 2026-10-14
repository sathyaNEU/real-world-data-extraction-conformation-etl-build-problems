"""build the pack: the world, the processes, the records, the documents, the two distractors and the manifest"""
import csv
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import params as P
import records as R
import sim
import world as W

FILES = dict(
    outages="oms_outage_export_2016-2025.csv",
    register="trim_unit_register.csv",
    completions="row_trim_completions_2012-2025.csv",
    survey="row_tree_survey_2023-2024.parquet",
    weather="weather_daily_2016-2025.csv",
    members="member_counts_2015-2025.csv",
    invoices="ap_invoices_row_trimming_2024-12_2025-12.csv",
    contracts="trimming_contracts_register.xlsx",
    row_policy="right_of_way_maintenance_policy.pdf",
    rel_policy="reliability_reporting_policy.docx",
    dictionary="data_dictionary.xlsx",
    manifest="export_manifest.csv",
    benchmark="statewide_cooperative_reliability_2020-2024.csv",
    ami="ami_momentary_events_2025.csv",
)
DISTRACTORS = ("benchmark", "ami")


def write_csv(path, df):
    df.to_csv(path, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    return len(df)


def write_parquet(path, df):
    t = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=False)
    return len(df)


def run(target):
    ss = np.random.SeedSequence(P.SEED).spawn(10)
    r = [np.random.default_rng(s) for s in ss]
    U = W.energised(W.network(r[0]))
    U = W.changes(U, r[1])
    M = W.members(r[2])
    S = W.survey(U, r[3])
    dens = W.ash_density(S, U)
    Wx = sim.weather(r[4])
    T = sim.trims(U, r[5])
    O = sim.outages(U, T, Wx, dens, M, r[6])
    X, K = R.outage_export(O, r[7])
    I = R.invoices(T, U, r[8])
    counts = {}
    f = lambda k: os.path.join(target, FILES[k])
    counts["outages"] = write_csv(f("outages"), X)
    counts["register"] = write_csv(f("register"), R.unit_register(U))
    counts["completions"] = write_csv(f("completions"), R.completions(T, r[9]))
    counts["survey"] = write_parquet(f("survey"), R.survey_rows(S))
    counts["weather"] = write_csv(f("weather"), R.weather_rows(Wx))
    Mo = M.rename(columns={"members": "members_at_year_end"})
    counts["members"] = write_csv(f("members"), Mo)
    counts["invoices"] = write_csv(f("invoices"), I)
    counts["benchmark"] = write_csv(f("benchmark"), distractor_benchmark(np.random.default_rng(P.SEED + 61)))
    counts["ami"] = write_csv(f("ami"), distractor_ami(X, U, np.random.default_rng(P.SEED + 62)))
    facts = docs.write_all(target, FILES, U, T, M)
    counts.update(facts.get("counts", {}))
    write_manifest(f("manifest"), counts)
    return dict(U=U, M=M, S=S, dens=dens, Wx=Wx, T=T, O=O, X=X, K=K, I=I, counts=counts, facts=facts)


def distractor_benchmark(rng):
    """the state cooperative association's yearly reliability survey of its member cooperatives: each cooperative's
    reported indices as it filed them, excluding major event days by its own method"""
    names = ["Brask Valley Electric Cooperative", "Callender Bend REC", "Corvell County Electric",
             "Dunsford Rural Electric", "Gorrell Valley Electric", "Harrow Fork Electric Cooperative",
             "Lomax Prairie Electric", "Merrin County Power", "Orlen Rural Electric", "Pinnow River Electric",
             "Quarry Bend Electric", "Sallow Creek Cooperative", "Selden Hills REC", "Yarrow Plains Electric"]
    rows = []
    for n in names:
        mi = rng.uniform(900, 5200)
        mem = mi * rng.uniform(3.2, 8.5)
        base_saidi = rng.uniform(95, 260)
        base_saifi = rng.uniform(0.9, 2.4)
        tree = rng.uniform(0.18, 0.46)
        for y in range(2020, 2025):
            f = float(np.exp(rng.normal(0, 0.12)))
            mi_y = mi * (1 - 0.003 * (y - 2020)) * float(np.exp(rng.normal(0, 0.004)))   # conversions to underground
            mem_y = mem * (1 + rng.uniform(0.002, 0.016)) ** (y - 2020) * float(np.exp(rng.normal(0, 0.004)))
            rows.append((n, y, int(mem_y), round(mi_y, 0), round(base_saidi * f, 1),
                         round(base_saifi * f ** 0.6, 2), round(tree * float(np.exp(rng.normal(0, 0.1))), 3)))
    return pd.DataFrame(rows, columns=["cooperative", "year", "members", "overhead_miles", "saidi_minutes_excl_med",
                                       "saifi_excl_med", "tree_share_of_saidi"])


def distractor_ami(X, U, rng):
    """meter last-gasp and restore pairs under five minutes (blinks) the AMI head end counted by circuit and month in
    2025: what members saw of the reclosers' momentary operations"""
    X = X.drop_duplicates("outage_id")
    st = pd.to_datetime(X.start_local)
    en = pd.to_datetime(X.step_restored_local)
    mom = X[((en - st).dt.total_seconds() <= 300) & (st.dt.year == 2025)]
    mom = mom.assign(month=pd.to_datetime(mom.start_local).dt.month)
    g = mom.groupby(["circuit", "month"]).members_out.sum()
    circuits = sorted(U.circuit.unique())
    rows = []
    for c in circuits:
        meters = int(U[(U.circuit == c)].miles.sum() * 4.3)
        for m in range(1, 13):
            base = g.get((c, m), 0)
            rows.append((c, "2025-%02d" % m, meters, int(base * rng.uniform(0.85, 1.0) + rng.poisson(meters * 0.03))))
    return pd.DataFrame(rows, columns=["circuit", "month", "meters_reporting", "blink_events"])


def write_manifest(path, counts):
    desc = {
        "outages": ("Outage management system", "Every outage opened from 1 January 2016 to 31 December 2025, one row per restoration step"),
        "register": ("Engineering GIS", "Trim units of overhead primary with in-service and retirement dates"),
        "completions": ("Right-of-way work order system", "Trimming completions and audit results from 2012"),
        "survey": ("Forestry survey tool", "Trees within falling distance of each span, 2023 survey and 2024 re-survey of rebuilt lines"),
        "weather": ("Weather station network", "Daily peak gust and precipitation at the three district stations"),
        "members": ("Member services", "Members served at the end of each year by district"),
        "invoices": ("Accounts payable", "Right-of-way trimming invoices and credit memos for service December 2024 to December 2025"),
        "contracts": ("Purchasing", "Trimming contracts by district"),
        "row_policy": ("Operations", "Right-of-way maintenance policy"),
        "rel_policy": ("Engineering", "Reliability reporting policy"),
        "dictionary": ("Engineering", "Field definitions for the exports"),
        "benchmark": ("State cooperative association", "Member cooperatives' reported reliability indices, 2020 to 2024"),
        "ami": ("AMI head end", "Meter-level momentary interruptions (blinks) by circuit and month, 2025"),
    }
    rows = []
    for k, f in FILES.items():
        if k == "manifest":
            continue
        src, what = desc[k]
        rows.append((f, src, what, counts.get(k, ""), "2026-01-13"))
    df = pd.DataFrame(rows, columns=["file", "source_system", "contents", "rows", "extracted"])
    df.to_csv(path, index=False, lineterminator="\n")
