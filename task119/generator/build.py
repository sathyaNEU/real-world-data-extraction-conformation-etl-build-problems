"""Build the task119 evidence pack: python3 build.py [--out DIR] [--no-checks]

Writes DIR/target/ and DIR/metadata.json (DIR defaults to the task folder), then runs every assertion in
checks.py against the files as written. Exit status 0 only when every assertion holds.
"""
import argparse
import datetime as dt
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as C            # noqa: E402
import world as WM            # noqa: E402
import sim                    # noqa: E402
import people                 # noqa: E402
import legacy                 # noqa: E402
import extracts               # noqa: E402
import corpus                 # noqa: E402
import docs                   # noqa: E402
import writers as WR          # noqa: E402
import theatre                # noqa: E402

TASK = HERE.parent
F = dict(
    referrals="critical_care_referrals_202307_202606.csv",
    stays="acc_unit_stays_202306_202606.parquet",
    returns="acc_bed_return_0800_202306_202606.csv",
    episodes="apc_episodes_referred_patients_2022-2026.parquet",
    register="acc_unit_register.csv",
    capacity="wenmarsh_acc_capacity_report_2024-04_to_2026-06.xlsx",
    remit="review_terms_of_reference_2027-28.docx",
    guide="wenmarsh_acc_extract_field_guide.pdf",
    reviewlog="nrr_escalation_reviews_closed_2021-2025.xlsx",
    reviewdb="nrr_review_records.sqlite",
    levels="ccrs_referral_levels_202307_202404.csv",
    legacyspec="ccrs_migration_export_specification_rel2.3.pdf",
    links="pas_patient_key_links_2023-2026.csv",
    apcspec="rds_apc_extract_specification.txt",
    boardpaper="accn_board_paper_2023-11-21_level3_capacity.pdf",
    transfers="interhospital_transfer_audit_202307_202606.csv",
    theatre="rds_theatre_cases_2023-2026.parquet",
    thread="review_placement_correspondence.eml",
    l2returns="level2_unit_bed_return_0800_2025-26.csv",
    ambulance="ambulance_handovers_hourly_2025-26.csv",
)
DISTRACTORS = ["l2returns", "ambulance", "capacity", "reviewlog", "reviewdb"]
EXPORT_TIME = dt.datetime(2026, 9, 30, 17, 40)

REF_COLS = ["referral_id", "received_at", "referring_trust", "referred_from", "patient_key", "dta_at",
            "level_of_care", "outcome", "outcome_at", "admitting_unit"]
STAY_COLS = ["stay_id", "unit_code", "referral_id", "patient_key", "admitted_at", "discharged_at", "admission_type",
             "source_location"]
STAY_TYPES = ["str", "str", "str", "str", "ts", "ts", "str", "str"]
EP_COLS = ["episode_id", "spell_id", "patient_key", "provider_code", "admission_date", "admission_method",
           "episode_order", "episode_start", "episode_end", "main_specialty", "discharge_date", "discharge_method",
           "discharge_destination", "date_of_death"]
TH_COLS = ["case_id", "patient_key", "provider_code", "site_name", "case_date", "urgency", "procedure_code",
           "into_theatre_at", "out_of_theatre_at", "left_recovery_at", "recovery_destination"]
TH_TYPES = ["str", "str", "str", "str", "date", "str", "str", "ts", "ts", "ts", "str"]
EP_TYPES = ["str", "str", "str", "str", "date", "str", "int", "date", "date", "str", "date", "str", "str", "date"]


def build_world(log=print):
    t0 = time.time()
    W = WM.World()
    W.build_days()
    W.assign_roles()
    W.build_c_gaps()
    sim.unit_windows(W)
    W.place_all()
    W.build_planned()
    W.build_background()
    W.index()
    log("  waits placed: %d (%.1fs)" % (len(W.waits), time.time() - t0))
    P = sim.Patients()
    stays, _ = sim.simulate(W, P)
    log("  stays simulated: %d (%.1fs)" % (len(stays), time.time() - t0))
    refs = people.build_referrals(W, P, stays)
    death, where = people.assign_deaths(W, P, refs, stays)
    temp = people.assign_identities(W, P, refs, death)
    eps, verified = people.build_episodes(W, P, refs, stays, death, where, temp)
    out = legacy.finalize(W, P, stays, refs, death, temp, eps, verified)
    out["theatre"] = theatre.build_theatre(W, P, stays, refs, out)
    log("  referrals %d, episodes %d (%.1fs)" % (len(out["referrals"]), len(out["episodes"]), time.time() - t0))
    revs = corpus.build_corpus()
    log("  corpus: %d reviews (%.1fs)" % (len(revs), time.time() - t0))
    return {"W": W, "P": P, "stays": stays, "refs": refs, "death": death, "temp": temp, "out": out, "revs": revs}


def write_pack(S, target, log=print):
    target.mkdir(parents=True, exist_ok=True)
    out = S["out"]
    n = {}
    n["referrals"] = WR.write_csv(target / F["referrals"], out["referrals"], REF_COLS)
    n["stays"] = WR.write_parquet(target / F["stays"], STAY_COLS, STAY_TYPES, out["stays"])
    returns = extracts.returns_0800(out["stays"])
    n["returns"] = WR.write_csv(target / F["returns"], returns, ["unit_code", "return_date", "beds_open",
                                                                 "beds_occupied_0800"])
    n["episodes"] = WR.write_parquet(target / F["episodes"], EP_COLS, EP_TYPES, out["episodes"], row_group=60_000)
    reg = extracts.register_rows()
    n["register"] = WR.write_csv(target / F["register"], reg, ["unit_code", "unit_name", "trust_code", "care_level",
                                                              "commissioned_beds", "valid_from", "valid_to"])
    n["levels"] = WR.write_csv(target / F["levels"], out["level_history"], ["referral_id", "entry_no", "recorded_at",
                                                                          "entry", "level"])
    n["links"] = WR.write_csv(target / F["links"], out["merges"], ["temporary_key", "verified_key", "merged_on",
                                                                  "registering_trust"])
    n["transfers"] = WR.write_csv(target / F["transfers"], out["transfers"],
                                  ["transfer_ref", "patient_key", "from_trust", "from_site", "to_unit", "decision_at",
                                   "bed_confirmed_at", "departed_at", "arrived_at"])
    n["theatre"] = WR.write_parquet(target / F["theatre"], TH_COLS, TH_TYPES, out["theatre"])
    n["l2returns"] = WR.write_csv(target / F["l2returns"], extracts.level2_returns(),
                                  ["unit_code", "return_date", "beds_open", "beds_occupied_0800"])
    n["ambulance"] = WR.write_csv(target / F["ambulance"], extracts.ambulance_handovers(),
                                  ["site", "trust_code", "arrival_date", "arrival_hour", "arrivals", "handover_0_15",
                                   "handover_15_30", "handover_30_60", "handover_60_plus", "hours_lost"])
    occ_rows, wait_rows = extracts.capacity_figures(returns, out["referrals"])
    n["capacity"] = docs.capacity_report(target / F["capacity"], occ_rows, wait_rows)
    n["reviewlog"], n["reviewdb"] = docs.review_files(target / F["reviewlog"], target / F["reviewdb"], S["revs"])
    docs.remit(target / F["remit"])
    docs.field_guide(target / F["guide"], F, n, DISTRACTORS)
    docs.legacy_spec(target / F["legacyspec"])
    docs.apc_spec(target / F["apcspec"])
    docs.board_paper(target / F["boardpaper"])
    docs.thread(target / F["thread"], F)
    WR.set_mtimes(target, EXPORT_TIME)
    return n, returns


def write_metadata(path, target, n):
    files = []
    fmt_of = lambda p: p.suffix.lstrip(".").lower()
    for k, name in F.items():
        p = target / name
        files.append({"path": name, "format": fmt_of(p), "bytes": p.stat().st_size, "rows": n.get(k),
                      "source": docs.PROVENANCE[k][0], "date": docs.PROVENANCE[k][1],
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    biggest = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    meta = {
        "task": "task119",
        "title": "Placing the Wenmarsh external review of deaths after delayed escalation to critical care, 2027-28",
        "domain": "Policy & Education",
        "subdomain": "public-administration",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "07 (grid of cells): eight trusts by three record columns with totals, and the trusts ranked on the confirmable part",
        "as_of": C.AS_OF.isoformat(),
        "deliverables": ["external_review_placement_2027-28.docx", "review_placement_workings.xlsx",
                         "review_placement_by_trust.png"],
        "distractor_files": [F[k] for k in DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": biggest["path"], "largest_file_rows": biggest["rows"],
                        "database_file": F["reviewdb"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task119/generator/build.py (seeded, deterministic) "
                               "around a fictional English region (Wenmarsh), its eight acute trusts, its adult "
                               "critical care network and a national review programme; no real patient, trust or "
                               "record is depicted. Code lists follow the published NHS Critical Care Minimum Data "
                               "Set and Hospital Episode Statistics conventions.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task119/generator/build.py",
        "files": files,
    }
    Path(path).write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK))
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    target = out / "target"
    if target.exists():
        shutil.rmtree(target)
    print("building world")
    S = build_world()
    print("writing pack to %s" % target)
    n, returns = write_pack(S, target)
    meta = write_metadata(out / "metadata.json", target, n)
    print("files %d, formats %s" % (len(meta["files"]), ", ".join(meta["input_gates"]["formats"])))
    if a.no_checks:
        return 0
    import checks
    ok = checks.run_all(S, target, out / "metadata.json", F, DISTRACTORS)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
