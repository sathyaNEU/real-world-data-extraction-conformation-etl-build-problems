"""Cut the pack: python3 task308/generator/build.py [target dir]. Writes every input file under target/ and
metadata.json beside it. Byte-identical on every run."""
import json
import os
import sys

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs  # noqa: E402
import postprocess  # noqa: E402
import params as P  # noqa: E402
import records as R  # noqa: E402
import world  # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "table": "weather_years_2027_hourly.csv",
    "events": "outage_event_log_2016_2025.csv",
    "fleet": "fleet_list_2027.xlsx",
    "tie": "red_willow_tie_outages_2016_2025.csv",
    "profiles": "offer_profiles_2016_2025.parquet",
    "standard": "RA-3_resource_adequacy_standard_rev4.pdf",
    "offers": "2027_capacity_rfo_offers_received.pdf",
    "causes": "gads_cause_codes.csv",
    "meter": "mdm_interval_export_2025.parquet",
    "dps": "delivery_point_register_2025.xlsx",
    "orders": "meter_service_orders_2025.csv",
    "billing": "MS-12_wholesale_billing_procedures.pdf",
    "gas": "northgate_hub_forward_curve_2027.xlsx",
    "forecasts": "member_load_forecasts_2027.xlsx",
}
DISTRACTORS = ["northgate_hub_forward_curve_2027.xlsx", "member_load_forecasts_2027.xlsx"]
STAMP = (2026, 10, 30, 9, 14, 0)


def freeze_zip(path, when=(2026, 10, 30, 9, 14, 0)):
    """rewrite an Office file's zip with fixed entry times, so two builds are byte-identical"""
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    import re
    stamp = "%04d-%02d-%02dT%02d:%02d:%02dZ" % when
    fixed = []
    for name, data in items:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          lambda m: m.group(1) + stamp.encode() + m.group(2), data)
        fixed.append((name, data))
    items = fixed
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            info = zipfile.ZipInfo(name, date_time=when)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)


ORG = "Prairie Hollow Power Cooperative"


def office(path, made, saved, person):
    postprocess.scrub(path, ORG, saved[:10])
    postprocess.finish_office(path, made, saved, ORG, person=person)


def _wb_props(wb, author):
    import datetime
    wb.properties.creator = author
    wb.properties.lastModifiedBy = author
    wb.properties.created = datetime.datetime(2026, 10, 12, 8, 41)
    wb.properties.modified = datetime.datetime(*STAMP)


def _sheet(ws, df, widths=None):
    ws.append(list(df.columns))
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5DA")
    for row in df.itertuples(index=False):
        ws.append([None if (isinstance(v, float) and np.isnan(v)) else v for v in row])
    for i, w in enumerate(widths or []):
        ws.column_dimensions[chr(65 + i)].width = w


def fleet(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Units"
    rows = []
    for code, plant, unit, cls, mw, efor, mttr, gas in P.UNITS + P.RETIRED:
        fuel = {"nuclear": "Uranium", "hydro": "Water", "coal": "Subbituminous coal",
                "combined cycle": "Natural gas", "combustion turbine": "Natural gas",
                "reciprocating engine": "Natural gas / ULSD"}[cls]
        transport = {"firm": "Northgate FT", "interruptible": "Northgate IT",
                     "firm (LDC), diesel backup": "Prairie Gas LDC firm; ULSD backup"}.get(gas, "")
        yr = {"nuclear": 1986, "hydro": 1958, "coal": 1979, "combined cycle": 2009, "combustion turbine": 2001,
              "reciprocating engine": 2014}[cls]
        if plant == "Torrance":
            yr = 2004
        if plant == "Wexford":
            yr = 2011
        ret = "2026-12-31" if code == "PH-121" else ""
        rows.append([code, plant, unit, cls.title() if cls != "combined cycle" else "Combined cycle", mw, fuel,
                     transport, yr, ret])
    df = pd.DataFrame(rows, columns=["GADS unit code", "Plant", "Unit", "Technology", "Net winter capability (MW)",
                                     "Primary fuel", "Gas transportation", "In service", "Retirement date"])
    _sheet(ws, df, [15, 14, 14, 22, 24, 20, 30, 10, 15])
    ws2 = wb.create_sheet("Contracts")
    c = pd.DataFrame([["Red Willow Hydro Authority", "Firm import", 200, "2019-01-01", "2029-12-31",
                       "Delivered at Hollow Junction over the Red Willow tie"],
                      ["Prairie Wind Partners (four farms)", "Wind PPA", 800, "2015-06-01", "2035-05-31",
                       "Output in the planning load table"],
                      ["Bremer and Kettle Falls Solar", "Solar PPA", 400, "2021-07-01", "2041-06-30",
                       "Output in the planning load table"]],
                     columns=["Counterparty", "Type", "MW", "Start", "End", "Note"])
    _sheet(ws2, c, [32, 14, 8, 12, 12, 46])
    _wb_props(wb, "Joseph Graham")
    wb.save(path)


def dp_register(path, M):
    wb = Workbook()
    ws = wb.active
    ws.title = "Delivery points"
    rng = np.random.default_rng(P.SEED + 71)
    gen = set(M["gen"])
    tr = M["transfer"]
    rows = []
    for d in M["dps"]:
        mem = tr["to"] if d["dp"] == tr["dp"] else d["member"]
        rows.append([d["dp"], d["substation"] + " Substation", mem,
                     str(rng.choice(["L+G FOCUS AXR-SD", "Itron Sentinel", "SEL-735"])),
                     "Delivered and received" if d["dp"] in gen else "Delivered", float(rng.choice([12.47, 24.9, 69.0]))])
    _sheet(ws, pd.DataFrame(rows, columns=["Delivery point", "Substation", "Member (31 Dec 2025)", "Meter",
                                           "Channels", "Metering voltage (kV)"]), [14, 26, 30, 20, 22, 20])
    ws2 = wb.create_sheet("Assignment history")
    h = []
    for d in M["dps"]:
        if d["dp"] == tr["dp"]:
            h.append([d["dp"], tr["from_"], "2009-04-01", "2025-06-30"])
            h.append([d["dp"], tr["to"], "2025-07-01", ""])
        else:
            h.append([d["dp"], d["member"], "2009-04-01", ""])
    _sheet(ws2, pd.DataFrame(h, columns=["Delivery point", "Member", "Effective from", "Effective to"]),
           [14, 30, 14, 14])
    _wb_props(wb, "Lindsey Ramos")
    wb.save(path)


def orders(M):
    rng = np.random.default_rng(P.SEED + 72)
    rows = []
    techs = ["K. Ostrowski", "D. Tollefson", "M. Haugen", "R. Brekke"]
    for s in M["swaps"]:
        # the crew finishes inside the hour before the first interval on the new transformers
        rows.append([s["dp"], s["when"] - pd.Timedelta(minutes=int(rng.integers(8, 55))),
                     "Current transformer replacement",
                     "CTs replaced, ratio %d:5 to %d:5. Meter multiplier %d to %d." % (s["old"] * 5, s["new"] * 5,
                                                                                    s["old"], s["new"])])
    for s in M["stuck"]:
        rows.append([s["dp"], s["reset"] - pd.Timedelta(minutes=int(rng.integers(8, 55))), "Meter clock check",
                     "Meter clock found on standard time; set to daylight time."])
    dps = [d["dp"] for d in M["dps"]]
    for _ in range(120):
        dp = str(rng.choice(dps))
        t = pd.Timestamp(P.METER_YEAR, 1, 1, tz=P.TZ) + pd.Timedelta(days=int(rng.integers(3, 360)),
                                                                     hours=int(rng.integers(8, 16)),
                                                                     minutes=int(rng.integers(0, 60)))
        k = int(rng.integers(0, 5))
        if k == 0:
            rows.append([dp, t, "Meter clock check", "Clock within one minute, no change."])
        elif k == 1:
            rows.append([dp, t, "Meter clock check", "Clock adjusted %d min." % int(rng.integers(2, 6))])
        elif k == 2:
            rows.append([dp, t, "Annual meter test", "As-found accuracy %.2f%%, passed." % rng.uniform(99.85, 100.12)])
        elif k == 3:
            rows.append([dp, t, "Communications", "Cellular modem replaced; interval data backfilled from meter."])
        else:
            rows.append([dp, t, "Seal inspection", "Seals intact."])
    df = pd.DataFrame(rows, columns=["dp_id", "completed", "work_type", "notes"])
    df = df.sort_values("completed").reset_index(drop=True)
    df.insert(0, "order_no", ["WO-25-%04d" % (3101 + i * 3 + int(rng.integers(0, 3))) for i in range(len(df))])
    df["completed"] = [t.strftime("%Y-%m-%d %H:%M") for t in df.completed]
    df["technician"] = [str(rng.choice(techs)) for _ in range(len(df))]
    return df


def gas_curve(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Forward curve"
    months = pd.date_range("2027-01-01", "2027-12-01", freq="MS")
    base = [6.85, 6.10, 4.20, 3.15, 2.95, 3.05, 3.40, 3.55, 3.10, 3.20, 3.85, 5.30]
    df = pd.DataFrame(dict(Month=[m.strftime("%b %Y") for m in months], **{"Northgate hub (USD/MMBtu)": base},
                           **{"Basis to Henry Hub (USD/MMBtu)": [1.35, 1.10, 0.25, -0.15, -0.20, -0.18, -0.05, 0.02,
                                                                 -0.12, -0.08, 0.30, 0.95]}))
    _sheet(ws, df, [12, 26, 30])
    ws.append([])
    ws.append(["Settlements as of 23 October 2026. Fuels desk, N. Wilkinson."])
    _wb_props(wb, "Nicholas Wilkinson")
    wb.save(path)


def forecasts(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 forecasts"
    rng = np.random.default_rng(P.SEED + 73)
    rows = []
    for m, sh in zip(P.MEMBERS, P.MEMBER_SHARE):
        e = sh * 12_150_000 * rng.uniform(0.97, 1.05)
        rows.append([m, round(e, -2), round(sh * 3010 * rng.uniform(0.96, 1.06), 1), "Board approved"
                     if rng.random() < 0.6 else "Draft"])
    _sheet(ws, pd.DataFrame(rows, columns=["Member", "2027 energy (MWh)", "2027 winter peak (MW)", "Status"]),
           [32, 18, 22, 16])
    _wb_props(wb, "Isabel Cole")
    wb.save(path)


def build(target):
    os.makedirs(target, exist_ok=True)
    W = world.build()
    M = world.members(W)
    p = lambda k: os.path.join(target, FILES[k])  # noqa: E731
    R.planning_table(W).to_csv(p("table"), index=False)
    ev = R.events(W)
    R.event_log(ev).to_csv(p("events"), index=False)
    R.tie_log(R.tie_events(W)).to_csv(p("tie"), index=False)
    R.profiles(W).to_parquet(p("profiles"), index=False)
    fleet(p("fleet"))
    office(p("fleet"), "2026-10-12T08:41:00Z", "2026-10-29T16:02:00Z", "Joseph Graham")
    pd.DataFrame(sorted(docs.CAUSE_TEXT.items()), columns=["cause_code", "description"]).to_csv(p("causes"), index=False)
    ex = R.metering(M)
    ex.to_parquet(p("meter"), index=False)
    dp_register(p("dps"), M)
    office(p("dps"), "2025-01-09T10:15:00Z", "2026-01-06T13:47:00Z", "Lindsey Ramos")
    orders(M).to_csv(p("orders"), index=False)
    docs.standard(p("standard"))
    postprocess.scrub(p("standard"), "Microsoft Word 2019", "2026-02-24T15:10:00")
    docs.offers(p("offers"))
    postprocess.scrub(p("offers"), "Microsoft Word 2019", "2026-10-30T08:52:00")
    docs.billing(p("billing"))
    postprocess.scrub(p("billing"), "Microsoft Word 2019", "2025-01-14T10:03:00")
    gas_curve(p("gas"))
    office(p("gas"), "2026-10-23T14:05:00Z", "2026-10-23T14:31:00Z", "Nicholas Wilkinson")
    forecasts(p("forecasts"))
    office(p("forecasts"), "2026-08-18T09:12:00Z", "2026-09-30T11:26:00Z", "Isabel Cole")
    return W, M


def metadata(target):
    meta = {"task": "task308", "title": "Prairie Hollow Power Cooperative: the 2027 capacity award",
            "files": [], "distractors": DISTRACTORS,
            "license": "All files are synthetic, generated for this task by task308/generator; no third-party data.",
            "source_note": "Fictional cooperative, members, pipeline, counterparties and people. GADS event and "
                           "cause code conventions follow the public NERC GADS Data Reporting Instructions in form "
                           "only; every value is generated.",
            "as_of": "2026-10-30"}
    for k, f in FILES.items():
        meta["files"].append({"file": f, "source": "synthetic (task308 generator)", "date": "2026-10-30",
                              "license": "generated for this task", "distractor": f in DISTRACTORS})
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    build(tgt)
    metadata(tgt)
    print("built", tgt)
