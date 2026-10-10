#!/usr/bin/env python3
"""task127 generator: build the slot-split folder (target/) and metadata.json under an output root,
deterministically, then assert the ladder, the asks and the input gates on the files as written.

    python3 task127/generator/build.py --out <root>          (root defaults to the task folder)
    python3 task127/generator/build.py --out <root> --record <path.json>

Seeded throughout (params.SEED); two builds into different roots are byte-identical.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import asks as A  # noqa: E402
import orders as O  # noqa: E402
import params as P  # noqa: E402
import world as Wd  # noqa: E402
import writers as Wr  # noqa: E402

REPO = HERE.parents[1]
TASK = HERE.parent
SCRUB = REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
FLOOR, CEILING = "2025-06-01", P.PACK_DATE.isoformat()
F = P.F
NAME = P.COOP_NAME


class World:
    pass


def make_world():
    W = World()
    W.cells = Wd.all_cells()
    W.sv = Wd.survey_records(W.cells)
    W.tables = Wd.published_tables(W.sv)
    W.feeders, W.fmap = Wd.feeder_frames()
    pi = Wd.pilot_installs()
    pools = {c: O.premises_pool(c + "-pilot", 300) for c in P.COOPS}
    pi["premises_id"] = [pools[c][i] for c, i in zip(pi.coop, pi.groupby("coop").cumcount())]
    pi = O.pilot_dates(pi)
    W.fo, W.crews = O.all_orders(pi)
    hp = W.fo[W.fo.order_type == "HPRM"].set_index("premises_id").completed
    pi["meter_set_date"] = pi.premises_id.map(hp)
    assert pi.meter_set_date.notna().all()
    pi = pi.sort_values(["purchase_date", "coop", "premises_id"], kind="stable").reset_index(drop=True)
    pi["rebate_id"] = [f"CH26-{10457 + 3 * i + (i % 3)}" for i in range(len(pi))]
    W.pi = A.pilot_columns(pi)
    W.inv, W.inv_truth, W.inv_kind = A.invoices(W.pi)
    W.L, W.N = A.payments(W.pi)
    return W


# ------------------------------------------------------------------ data files

def survey_csv(W, path):
    df = W.sv.copy()
    df["coop"] = df.coop.map(NAME)
    Wr.write_csv(df, path)


def tables_xlsx(W, path):
    h1, h2, h3, h4 = W.tables
    wb = Wr.workbook(path, P.PEOPLE["survey"], datetime(2026, 3, 9, 10, 12))
    top = lambda t, u: [t, u, ""]
    a = h1.reset_index().rename(columns={"coop": "Co-operative"})
    a["Co-operative"] = a["Co-operative"].map(NAME)
    Wr.sheet_table(wb, "H1", a, top("Table H1. Households by house heating fuel",
                                    "Weighted estimates, occupied housing units in each co-operative's service territory, 2025"),
                   [16] + [14] * 6)
    b = h2.reset_index().rename(columns={"coop": "Co-operative", "tenure": "Tenure"})
    b["Co-operative"] = b["Co-operative"].map(NAME)
    Wr.sheet_table(wb, "H2", b, top("Table H2. Households by tenure and house heating fuel",
                                    "Weighted estimates, occupied housing units, 2025"), [16, 10] + [14] * 6)
    c = h3.reset_index().rename(columns={"coop": "Co-operative", "tenure": "Tenure"})
    c["Co-operative"] = c["Co-operative"].map(NAME)
    Wr.sheet_table(wb, "H3", c, top("Table H3. Households by tenure and type of structure",
                                    "Weighted estimates, occupied housing units, 2025"), [16, 10, 22, 14, 22])
    d = h4.reset_index().rename(columns={"coop": "Co-operative"})
    d["Co-operative"] = d["Co-operative"].map(NAME)
    Wr.sheet_table(wb, "H4", d, top("Table H4. Households by household income in the past 12 months (dollars)",
                                    "Weighted estimates, occupied housing units, 2025"), [16] + [18] * 4)
    notes = pd.DataFrame({"note": [
        "Release 1, 9 March 2026. Heat Survey 2025, fieldwork May to September 2025.",
        "Estimates are weighted to the co-operatives' 2025 residential meter counts by service territory.",
        "House heating fuel is the fuel used most for heating the home. Electricity includes heat pumps.",
        "Sample records are in heat_survey_2025_households.csv; weights are integers.",
    ]})
    Wr.sheet_table(wb, "Notes", notes, None, [110])
    wb.close()


def pilot_xlsx(W, path):
    pi = W.pi
    df = pd.DataFrame({
        "rebate_id": pi.rebate_id, "premises_id": pi.premises_id, "coop": pi.coop.map(NAME),
        "neighbourhood": pi.neighbourhood, "heating_system_replaced": pi.sys.map(P.SYS_LABEL),
        "income_band": pi.income_band, "system_type": pi.system_type, "indoor_heads": pi.indoor_heads.astype(int),
        "installer_id": pi.installer.map(A.INSTALLER_NO), "purchase_date": pi.purchase_date,
        "install_date": pi.install_date, "meter_set_date": pi.meter_set_date})
    wb = Wr.workbook(path, P.PEOPLE["director"], datetime(2026, 12, 9, 15, 41))
    Wr.sheet_table(wb, "rebates", df, None, [12, 11, 12, 18, 26, 18, 22, 8, 11, 12, 12, 13],
                   date_cols=("purchase_date", "install_date", "meter_set_date"))
    wb.close()


def hosting_xlsx(W, path):
    fr = W.feeders.copy()
    study = {c: date(2026, 11, 2 + 3 * i) for i, c in enumerate(P.COOPS)}
    df = pd.DataFrame({"coop": fr.coop.map(NAME), "feeder": fr.feeder, "substation": fr.substation,
                       "hosting_capacity_remaining_kw": fr.headroom_kw.astype(int),
                       "study_date": [study[c] for c in fr.coop]})
    wb = Wr.workbook(path, P.PEOPLE["grid"], datetime(2026, 12, 3, 9, 26))
    top = ["Hosting capacity filings, participating co-operatives, as at 30 November 2026",
           "Remaining hosting capacity for new electrification load on each distribution feeder, kW, as filed by "
           "each co-operative under the participation terms.",
           "Compiled for the fund by B. Robbins, grid liaison, 3 December 2026.", ""]
    Wr.sheet_table(wb, "feeders", df, top, [14, 10, 18, 30, 12], date_cols=("study_date",))
    wb.close()


def fmap_csv(W, path):
    df = W.fmap.copy()
    df["coop"] = df.coop.map(NAME)
    Wr.write_csv(df[["coop", "neighbourhood", "feeder"]], path)


def orders_csv(W, path):
    fo = W.fo
    df = pd.DataFrame({"order_id": fo.order_id, "coop": fo.coop.map(NAME), "crew": fo.crew,
                       "order_type": fo.order_type, "premises_id": fo.premises_id,
                       "requested_date": [d.isoformat() for d in fo.requested],
                       "completed_date": [d.isoformat() if isinstance(d, date) else "" for d in fo.completed]})
    Wr.write_csv(df, path)


def invoices_csv(W, path):
    Wr.write_csv(W.inv, path)


def ledger_csv(W, path):
    Wr.write_csv(A.ledger_frame(W.L), path)


def returns_json(W, path):
    Wr.write_json(A.notices_doc(W.N, W.L), path)


def dims_xlsx(W, path):
    members = {"NS": 14820, "VA": 21460, "LA": 11930, "UP": 10210, "RB": 11870, "PW": 10640}
    sched = {c: ("four 10-hour days, Monday to Thursday" if c in P.FOUR_DAY else
                 "five 8-hour days, Monday to Friday") for c in P.COOPS}
    size = {"NS": 4, "VA": 4, "LA": 3, "UP": 3, "RB": 4, "PW": 3}
    co = pd.DataFrame({"coop": [NAME[c] for c in P.COOPS], "legal_name": [P.COOP_LONG[c] for c in P.COOPS],
                       "residential_members": [members[c] for c in P.COOPS],
                       "meter_crew": [P.CREW[c] for c in P.COOPS], "crew_schedule": [sched[c] for c in P.COOPS],
                       "crew_members": [size[c] for c in P.COOPS],
                       "pilot_neighbourhood": [P.PILOT_NBHD[c] for c in P.COOPS]})
    ins = pd.DataFrame({"installer_id": [A.INSTALLER_NO[k] for k in A.INSTALLERS],
                        "firm": [v[0] for v in A.INSTALLERS.values()],
                        "coops_served": [", ".join(NAME[c] for c in v[1]) for v in A.INSTALLERS.values()],
                        "billing_export": ["portal upload", "portal upload", "portal upload", "portal upload",
                                           "portal upload", "portal upload", "portal upload", "portal upload",
                                           "accounting system export"]})
    wb = Wr.workbook(path, P.PEOPLE["director"], datetime(2026, 2, 16, 11, 5))
    Wr.sheet_table(wb, "cooperatives", co, None, [12, 36, 12, 10, 38, 8, 18])
    Wr.sheet_table(wb, "installers", ins, None, [10, 28, 34, 24])
    wb.close()


def weatherization_csv(W, path):
    g = P.rng("weatherization")
    measures = [("attic insulation", 1400, 3200), ("air sealing", 450, 1300), ("wall insulation", 1800, 4100),
                ("rim joist insulation", 500, 1200), ("storm windows", 900, 2600)]
    rows = []
    pool = {c: O.premises_pool(c + "-wx", 900) for c in P.COOPS}
    k = 0
    for c in P.COOPS:
        nbs = list(P.NBHD[c])
        for j in range(int(g.integers(110, 190))):
            m, lo, hi = measures[int(g.integers(0, len(measures)))]
            d = date(2026, 1, 12) + timedelta(days=int(g.integers(0, 320)))
            k += 1
            rows.append(dict(grant_id=f"WX26-{3100 + 3 * k}", coop=NAME[c], neighbourhood=nbs[int(g.integers(0, len(nbs)))],
                             premises_id=pool[c][j], measure=m, grant_usd=f"{round(g.uniform(lo, hi) / 5) * 5:.2f}",
                             completed_on=d.isoformat()))
    df = pd.DataFrame(rows).sort_values(["completed_on", "grant_id"], kind="stable")
    Wr.write_csv(df, path)


def write_data(W, tgt):
    survey_csv(W, tgt / F["survey"])
    tables_xlsx(W, tgt / F["tables"])
    pilot_xlsx(W, tgt / F["pilot"])
    hosting_xlsx(W, tgt / F["hosting"])
    fmap_csv(W, tgt / F["fmap"])
    orders_csv(W, tgt / F["orders"])
    invoices_csv(W, tgt / F["invoices"])
    ledger_csv(W, tgt / F["ledger"])
    returns_json(W, tgt / F["returns"])
    dims_xlsx(W, tgt / F["dims"])
    weatherization_csv(W, tgt / F["wx"])


# ------------------------------------------------------------------ container hygiene

MTIME = {  # in-fiction write time of each file (local, Central)
    "survey": (2026, 3, 9, 10, 40), "tables": (2026, 3, 9, 10, 12), "pilot": (2026, 12, 9, 15, 41),
    "hosting": (2026, 12, 3, 9, 26), "fmap": (2026, 11, 20, 14, 2), "orders": (2026, 12, 11, 6, 15),
    "rules": (2026, 10, 27, 16, 30), "terms": (2026, 1, 21, 13, 10), "invoices": (2026, 12, 11, 6, 20),
    "ledger": (2026, 12, 11, 6, 22), "returns": (2026, 12, 11, 7, 3), "finance": (2026, 2, 4, 9, 45),
    "prices": (2026, 1, 30, 11, 18), "paper": (2026, 12, 10, 17, 52), "dims": (2026, 2, 16, 11, 5),
    "fields": (2026, 12, 10, 12, 30), "wx": (2026, 12, 8, 8, 55), "upgrades": (2026, 9, 14, 15, 20),
    "about": (2026, 12, 11, 8, 10),
}


def normalise_containers(tgt):
    for k, f in F.items():
        if f.endswith((".docx", ".xlsx")):
            Wr.normalise_zip(str(tgt / f), when=MTIME[k][:5] + (0,))


def scrub(tgt):
    r = subprocess.run([sys.executable, str(SCRUB), str(tgt), "--apply", "--producer", P.FUND,
                        "--stamp", P.PACK_DATE.isoformat(), "--floor", FLOOR, "--ceiling", CEILING],
                       capture_output=True, text=True)
    a = subprocess.run([sys.executable, str(SCRUB), str(tgt), "--floor", FLOOR, "--ceiling", CEILING],
                       capture_output=True, text=True)
    return r.returncode, a.returncode, (r.stdout + r.stderr + a.stdout + a.stderr)


def normalise_mtimes(tgt, root):
    for k, f in F.items():
        ts = datetime(*MTIME[k]).timestamp()
        os.utime(tgt / f, (ts, ts))
    last = datetime(2026, 12, 11, 8, 10).timestamp()
    os.utime(tgt, (last, last))
    if (root / "metadata.json").exists():
        os.utime(root / "metadata.json", (last, last))


# ------------------------------------------------------------------ metadata

def file_rows(tgt):
    out = []
    for f in sorted(os.listdir(tgt)):
        p = tgt / f
        ext = p.suffix.lstrip(".")
        rows = None
        if ext == "csv":
            rows = sum(1 for _ in open(p, encoding="utf-8")) - 1
        out.append(dict(path=f, format=ext, bytes=p.stat().st_size, rows=rows,
                        source="Constructed for this task: fictional fund and co-operatives; no third-party data",
                        date=P.PACK_DATE.isoformat(), license="CC0-1.0 (original work)"))
    return out


def metadata(tgt):
    files = file_rows(tgt)
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task127",
        "title": "2027 heat-pump rebate slots split across six participating co-operatives",
        "domain": "Nonprofit & Grant-making",
        "subdomain": "giving-strategy-program-funding",
        "objective": "Opportunity Sizing & Decision Support",
        "prompt_shape": "05 (allocation to a fixed total)",
        "as_of": P.AS_OF.isoformat(),
        "deliverables": P.DELIVERABLES,
        "distractor_files": P.DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK))
    ap.add_argument("--record", help="write the build record (JSON) here, outside the task folder")
    ap.add_argument("--skip-checks", action="store_true")
    a = ap.parse_args()
    root = Path(a.out).resolve()
    tgt = root / "target"
    if tgt.exists():
        shutil.rmtree(tgt)
    tgt.mkdir(parents=True)
    W = make_world()
    write_data(W, tgt)
    import docs as D
    D.write_docs(W, tgt)
    normalise_containers(tgt)
    sc = scrub(tgt)
    record = {"scrub": [sc[0], sc[1]]}
    if not a.skip_checks:
        import checks
        record.update(checks.run_all(W, tgt, root, sc))
    with open(root / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata(tgt), f, indent=1)
        f.write("\n")
    if not a.skip_checks:
        import checks
        checks.check_metadata(root, tgt, record)
    normalise_mtimes(tgt, root)
    if a.record:
        Path(a.record).write_text(json.dumps(record, indent=1, default=str))
    if "assertions" in record:
        print(f"ASSERTIONS {record['assertions']} passed")


if __name__ == "__main__":
    main()
