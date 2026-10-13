"""task131 generator: build the evidence pack.

    python3 task131/generator/build.py [--out DIR]

Writes DIR/target/ and returns the in-memory world for the checks (DIR defaults to the task folder)."""
import argparse
import json
import os
import shutil
import sys
from datetime import date, datetime

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import params as P     # noqa: E402
import weather as WX   # noqa: E402
import world as W      # noqa: E402
import sim as S        # noqa: E402
import nem12 as N12    # noqa: E402
import records as R    # noqa: E402
import docs            # noqa: E402

F = {
    "nem11": "MRP_NEM12_202511.csv", "nem12": "MRP_NEM12_202512.csv", "nem01": "MRP_NEM12_202601.csv",
    "nem02": "MRP_NEM12_202602.csv",
    "notes": "load_research_extracts_file_notes.pdf",
    "register": "summer_pricing_trial_register.xlsx",
    "plan": "summer_pricing_trial_plan.pdf",
    "tariffs": "residential_charges_2025-26.pdf",
    "forecast": "murrandi_demand_forecast_2026.xlsx",
    "history": "account_tariff_history_2026-03-12.csv",
    "survey": "trial_survey_responses_2026-03.csv",
    "instruments": "trial_survey_instruments_2026-03.pdf",
    "wx_daily": "IDCJAC0010_013027_1800_Data.csv",
    "wx_hh": "HM01X_Data_013027_202511_202602.csv",
    "zones": "zone_substation_loads_2025-26.csv",
    "pv": "rooftop_pv_connections_2026-06.csv",
    "gen": "generation_availability_2027-28.xlsx",
    "manifest": "tariff_advice_file_list_2026-10-09.csv",
}
DISTRACTORS = ["zones", "pv", "gen"]
DESC = {
    "nem11": ("interval reads for every trial premise, November 2025 (NEM12)", "Metering Services", "2025-12-05"),
    "nem12": ("interval reads for every trial premise, December 2025 (NEM12)", "Metering Services", "2026-01-06"),
    "nem01": ("interval reads for every trial premise, January 2026 (NEM12)", "Metering Services", "2026-02-05"),
    "nem02": ("interval reads for every trial premise, February 2026 (NEM12)", "Metering Services", "2026-03-10"),
    "notes": ("how the load research extracts are laid out", "Metering Services", "2024-02-12"),
    "register": ("the trial households, their blocks and assignment", "Load Research", "2025-11-07"),
    "plan": ("the summer pricing trial plan, version 2", "Load Research", "2025-11-03"),
    "tariffs": ("the gazetted residential charges for 2025-26", "Pricing and Tariffs", "2025-10-31"),
    "forecast": ("the 2026 system demand forecast, version 1.2", "System Planning", "2026-08-14"),
    "history": ("each account's tariff by register and date", "Billing", "2026-03-12"),
    "survey": ("every response started in the March 2026 survey of design households", "Customer Insights", "2026-03-26"),
    "instruments": ("the March 2026 survey's online form and telephone script", "Customer Insights", "2026-03-01"),
    "wx_daily": ("daily maximum temperature, Murrandi Aero (Bureau of Meteorology product IDCJAC0010)", "Bureau of Meteorology", "2026-04-02"),
    "wx_hh": ("half-hourly observations, Murrandi Aero, November 2025 to February 2026 (Bureau of Meteorology product HM01X)", "Bureau of Meteorology", "2026-04-02"),
    "zones": ("half-hourly zone substation loads, November 2025 to February 2026 (SCADA)", "Network Operations", "2026-03-04"),
    "pv": ("rooftop PV connection applications and connections", "Network Connections", "2026-06-30"),
    "gen": ("generating units' firm summer capacity and planned outages, 2027-28", "System Planning", "2026-08-21"),
    "manifest": ("this list", "Pricing and Tariffs", "2026-10-09"),
}
MTIME = {k: v[2] + " 09:15" for k, v in DESC.items()}
MTIME["manifest"] = "2026-10-09 16:40"


def world():
    hh, ev = W.build()
    taken = set(list(hh["account"]) + list(hh["customer"]) + list(hh["nmi"]) + list(hh["serial"]))
    newp, occ = W.new_premises(P.SEED + 11, hh, ev, taken)
    ex = W.exchanges(P.SEED + 12, hh, ev)
    tmax, tmin = WX.daily()
    loads, meta, status, at_new, sday, wkd = S.simulate(hh, ev, newp, occ, ex, tmax, tmin)
    return {"hh": hh, "ev": ev, "newp": newp, "occ": occ, "exch": ex, "tmax": tmax, "tmin": tmin, "loads": loads,
            "meta": meta, "status": status, "at_new": at_new, "sday": sday, "wkd": wkd}


def write_pack(outdir, Wd=None):
    tgt = os.path.join(outdir, "target")
    if os.path.exists(tgt):
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    Wd = Wd or world()
    hh = Wd["hh"]
    by_month = {}
    for d in P.DAYS:
        by_month.setdefault(d.month, []).append(d)
    streams, resend = N12.plan(hh, Wd["loads"], Wd["meta"], Wd["exch"], Wd["newp"], Wd["occ"], P.SEED + 21)
    Wd["streams"], Wd["resend"] = streams, resend
    for m, key in ((11, "nem11"), (12, "nem12"), (1, "nem01"), (2, "nem02")):
        N12.write(os.path.join(tgt, F[key]), m, hh, Wd["loads"], Wd["meta"], Wd["exch"], Wd["newp"], Wd["occ"],
                  streams, resend, by_month)
    hist = R.account_history(hh, Wd["ev"], Wd["newp"], Wd["occ"], Wd["exch"], P.SEED + 31)
    hist.to_csv(os.path.join(tgt, F["history"]), index=False, lineterminator="\n")
    reg = R.register(hh)
    docs.register_book(reg, os.path.join(tgt, F["register"]))
    sv = R.survey(hh, Wd["ev"], P.SEED + 41)
    sv.to_csv(os.path.join(tgt, F["survey"]), index=False, lineterminator="\n")
    dly, hhw = R.weather_files(Wd["tmax"], Wd["tmin"])
    dly.to_csv(os.path.join(tgt, F["wx_daily"]), index=False, lineterminator="\n")
    hhw.to_csv(os.path.join(tgt, F["wx_hh"]), index=False, lineterminator="\n")
    R.zone_loads(Wd["tmax"], P.SEED + 51).to_csv(os.path.join(tgt, F["zones"]), index=False, lineterminator="\n")
    R.pv_connections(hh, Wd["exch"], P.SEED + 61).to_csv(os.path.join(tgt, F["pv"]), index=False, lineterminator="\n")
    docs.trial_plan(os.path.join(tgt, F["plan"]))
    docs.tariffs(os.path.join(tgt, F["tariffs"]))
    docs.meter_notes(os.path.join(tgt, F["notes"]))
    docs.survey_instruments(os.path.join(tgt, F["instruments"]))
    docs.forecast(os.path.join(tgt, F["forecast"]))
    docs.generation(os.path.join(tgt, F["gen"]))
    man = []
    for k in F:
        if k == "manifest":
            continue
        man.append({"file": F[k], "holds": DESC[k][0], "from": DESC[k][1], "as_at": DESC[k][2]})
    pd.DataFrame(man).to_csv(os.path.join(tgt, F["manifest"]), index=False, lineterminator="\n")
    Wd["hist"], Wd["reg"], Wd["survey"] = hist, reg, sv
    return tgt, Wd


def set_mtimes(tgt):
    for k, f in F.items():
        t = datetime.strptime(MTIME[k], "%Y-%m-%d %H:%M").timestamp()
        os.utime(os.path.join(tgt, f), (t, t))


def metadata(outdir):
    meta = {"task": "task131", "distractor_files": ["target/" + F[k] for k in DISTRACTORS],
            "deliverables": ["tariff_default_advice_2027-28.pdf", "tariff_trial_tables_2025-26.xlsx"],
            "domain": "Energy Systems & Utilities", "task_type": "tariff-demand-response-evaluation",
            "objective": "Experiment & Causal Analysis",
            "stated_inputs": ["41,860", "41860", "214.6", "44.6"],
            "sources": {"all files": "constructed for this task by the author (synthetic, no third-party data); no licence restriction"}}
    with open(os.path.join(outdir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.dirname(HERE))
    a = ap.parse_args()
    tgt, _ = write_pack(a.out)
    set_mtimes(tgt)
    metadata(a.out)
    print("wrote", tgt, len(os.listdir(tgt)), "files")
