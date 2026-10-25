"""Cut task485's pack from the clean truth: the National Bovine Register's animal and movement exports with its herd
register, the June census by farm, the land parcel register's farmed area, the farm practices survey's housing seasons,
the three slurry contractors' exports, three context files and the register's export notes."""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font

import contractors as C
import registry as R
import world as W

D = dt.date
BOLD = Font(bold=True)
PREMISES = {"mart": "%s Mart", "factory": None, "knackery": None, "export": None, "dealer": None}
FACTORY_NAMES = ["Midland Basin Meats", "Southern Vale Beef", "Inner Basin Meat Packers", "Western Seaboard Foods", "Lower Basin Meats"]
KNACKERY_NAMES = ["Eastern Vale Knackery", "Lower Basin Fallen Animals", "Middle Uplands Knackery"]
EXPORT_NAMES = ["Northern Vale Export Assembly Centre", "Coastal Vale Live Export Lairage"]


def _csv(path, header, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def dmy(i):
    return W.dd(i).strftime("%d/%m/%Y")


def _sheet(ws, header, rows, widths, fmts=None):
    ws.append(header)
    for c in ws[1]:
        c.font = BOLD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for k, wd in enumerate(widths):
        ws.column_dimensions[get_column_letter(k + 1)].width = wd
    for col, fmt in (fmts or {}).items():
        for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
            for c in row:
                c.number_format = fmt
    ws.freeze_panes = "A2"


# ------------------------------------------------------------------------------------------- the bovine register
def animals(path, w, IV, tags, bherd):
    A, H = w.A, w.herds
    rows = []
    for a in sorted(IV, key=lambda x: tags[x]):
        b, fc, dam = A["birth"][a], A["fc"][a], A["dam"][a]
        rows.append([tags[a], A["sex"][a], A["breed"][a], dmy(b), dmy(b + A["reg_lag"][a]),
                     tags[dam] if dam is not None and dam in IV else "", H[bherd[a]]["herd_no"],
                     H[A["herd0"][a]]["herd_no"], dmy(fc) if fc is not None and A["sex"][a] == "F" else "",
                     dmy(A["exit"][a]) if A["exit"][a] is not None else "", A["exit_type"][a] or "",
                     H[A["exit_herd"][a]]["herd_no"] if A["exit_herd"][a] is not None else ""])
    return _csv(path, ["TAG_NUMBER", "SEX", "BREED", "DATE_OF_BIRTH", "DATE_REGISTERED", "DAM_TAG", "BIRTH_HERD",
                       "HERD_AT_START", "FIRST_CALVING_DATE", "EXIT_DATE", "EXIT_TYPE", "EXIT_HERD"], rows)


def movements(path, w, tags, rng):
    H = w.herds
    ms = sorted((m for m in w.moves if 0 <= m["dep"] < W.NDAY), key=lambda m: (m["dep"], m["k"]))
    rows, mid = [], 31204117
    for m in ms:
        mid += int(rng.integers(1, 4))
        rows.append([mid, tags[m["a"]], H[m["frm"]]["herd_no"], dmy(m["dep"]), H[m["to"]]["herd_no"], dmy(m["arr"])])
    return _csv(path, ["MOVEMENT_ID", "TAG_NUMBER", "DEPARTURE_HERD", "DEPARTURE_DATE", "DESTINATION_HERD",
                       "ARRIVAL_DATE"], rows)


def premises_names(w):
    names, k = {}, {"factory": 0, "knackery": 0, "export": 0}
    for h in w.herds:
        t = h["type"]
        if t == "mart":
            names[h["id"]] = "%s Mart" % h["region"]
        elif t in k:
            names[h["id"]] = {"factory": FACTORY_NAMES, "knackery": KNACKERY_NAMES, "export": EXPORT_NAMES}[t][k[t]]
            k[t] += 1
    return names


def herd_register(path, w, old, rng):
    names = premises_names(w)
    rows = []
    for h in w.herds:
        main = w.herds[h["out_farm_of"]]["herd_no"] if "out_farm_of" in h else None
        if "valid_from" not in h:
            y0 = 2006 if main else 1987
            h["valid_from"] = D(int(rng.integers(y0, 2024)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        rows.append([h["herd_no"], R.HTYPE[h["type"]], names.get(h["id"]), h["district"], h["region"],
                     W.RCODE[h["region"]], W.RCODE[h["region_pre2024"]], h["farm_no"] or None, main,
                     h["valid_from"], None])
    for o in old:
        rows.append([o["herd_no"], "Farm", None, o["district"], o["region"], W.RCODE[o["region"]],
                     W.RCODE[o["region_pre2024"]], None, None, o["valid_from"], o["valid_to"]])
    rows.sort(key=lambda r: (r[0], r[9]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Herds"
    _sheet(ws, ["Herd No", "Herd type", "Name", "District", "Region", "Region code", "Region code (pre-2024)",
                "NSO farm no", "Main herd no", "Valid from", "Valid to"], rows,
           [12, 22, 32, 9, 13, 8, 10, 12, 12, 12, 12], {10: "DD/MM/YYYY", 11: "DD/MM/YYYY"})
    ws.auto_filter.ref = "A1:K%d" % (len(rows) + 1)
    ws2 = wb.create_sheet("Regions")
    reg_rows = []
    for r in W.REG:
        ds = sorted({h["district"] for h in w.herds if h["region"] == r})
        reg_rows.append([W.RCODE[r], r, ", ".join(ds)])
    _sheet(ws2, ["Region code", "Region", "Districts"], reg_rows, [10, 14, 70])
    ws2.append([])
    ws2.append(["Regions are the Ministry's 2024 regional structure. On 1 January 2024 districts 0412, 0415 and "
                "0418 moved from Coastal Vale (04) to Southern Vale (03); herds there keep their herd numbers, and the "
                "pre-2024 code is kept on each herd for continuity with earlier returns."])
    wb.save(path)
    return len(rows)


# --------------------------------------------------------------------------------------------- the census and land
def census_csv(path, w, cen):
    code = {h["farm_no"]: int(W.RCODE[h["region_pre2024"]]) for h in w.herds if h.get("farm_no") and "out_farm_of" not in h}
    rows = []
    for f in sorted(cen, key=int):
        c = cen[f]
        vals = [c.get(k, 0) for k in R.NSO_CATS]
        rows.append([int(f), code[f]] + vals + [sum(vals)])
    return _csv(path, ["FARM_NO", "REGION"] + [k.upper() for k in R.NSO_CATS] + ["TOTAL_CATTLE"], rows)


def lpr(path, parcels):
    rows = [[p["parcel"], p["herd"], 2026, p["use"], "%.2f" % p["area"], "%.1f" % p["share"]]
            for p in sorted(parcels, key=lambda p: (p["parcel"], p["herd"]))]
    return _csv(path, ["PARCEL_ID", "HERD_NO", "CLAIM_YEAR", "LAND_USE", "AREA_HA", "SHARE_PCT"], rows)


def survey(path, w, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Housing"
    rows = []
    for r in W.REG:
        (im, idd), (om, od) = W.HOUSING[r]
        n = sum(1 for h in w.herds if h["region"] == r and h["type"] in ("dairy", "suckler", "finisher", "rearer"))
        rows.append([r, W.RCODE[r], int(n * rng.uniform(0.78, 0.94)), D(2025, im, idd).strftime("%-d %B"),
                     D(2026, om, od).strftime("%-d %B"), W.housed_days(r)])
    _sheet(ws, ["Region", "Region code", "Farms responding", "Usual housing date", "Usual turnout date",
                "Housed days in a 365-day year"], rows, [14, 8, 11, 14, 14, 14])
    ws2 = wb.create_sheet("Slurry storage")
    rows2 = []
    for r in W.REG:
        t = W.RTYPE[r]
        wk = {"D": 19.4, "B": 18.1, "G": 16.2, "W": 16.8}[t] + rng.uniform(-1.2, 1.2)
        cov = {"D": 21.0, "B": 17.5, "G": 9.5, "W": 11.0}[t] + rng.uniform(-3, 3)
        rows2.append([r, W.RCODE[r], round(wk, 1), round(cov, 1)])
    _sheet(ws2, ["Region", "Region code", "Slurry storage, mean weeks", "Stores covered, % of farms"], rows2,
           [14, 8, 14, 14])
    ws3 = wb.create_sheet("Notes")
    for line in ["Livestock Housing Survey 2025: housing and slurry storage",
                 "Ministry of Agriculture, Livestock Surveys Unit. Fieldwork 3 March to 30 May 2025.",
                 "",
                 "Housing: the median of the dates farmers gave for housing their cattle in the autumn and turning them "
                 "out in the spring in a usual year, by the farm's region (2024 regions).",
                 "Housed days run from the housing date to the day before the turnout date.",
                 "Slurry storage: mean weeks of storage capacity on farms with slurry tanks; covered stores as a share "
                 "of farms with an outdoor store.",
                 "Results are weighted to the June 2024 census population of farms with cattle."]:
        ws3.append([line] if line else [])
    ws3.column_dimensions["A"].width = 110
    wb.save(path)


# ---------------------------------------------------------------------------------------------- the contractors
def ardvale(path, cj):
    rows = [[j["job_id"], dmy(j["date"]), j["herd"], j["material"], j["tanker"], j["gal"], j["loads"], j["equipment"]]
            for j in sorted(cj["av"], key=lambda j: j["job_id"])]
    return _csv(path, ["Job No", "Date", "Herd No", "Material", "Tanker", "Capacity (gal)", "Loads", "Spreader"], rows)


def spaced(herd_no):
    return herd_no[:2] + " " + herd_no[2:]


def kilbrack(path, cj):
    desc = {c: (d, u) for c, d, u, _ in C.KB_SERVICES}
    rows = []
    for l in sorted(cj["kb"], key=lambda l: l["invoice"]):
        lines = [(l["service"], l["qty"])]
        if l["agit"]:
            lines.append(("AG-HR", l["agit"]))
        for svc, q in lines:
            net = round(q * C.KB_RATE[svc], 2)
            vat = round(net * C.VAT, 2)
            rows.append([l["invoice"], W.dd(l["date"]), l["acct"], spaced(l["herd"]), svc, desc[svc][0], q,
                         desc[svc][1], C.KB_RATE[svc], net, vat, round(net + vat, 2), l["ref"]])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Invoice lines"
    _sheet(ws, ["Invoice No", "Invoice date", "Account", "Herd No", "Service", "Description", "Qty", "Unit", "Rate",
                "Net", "VAT", "Gross", "Reference"], rows, [11, 11, 8, 11, 8, 40, 7, 9, 7, 10, 9, 10, 11],
           {2: "DD/MM/YYYY", 7: "0.0", 9: "#,##0.00", 10: "#,##0.00", 11: "#,##0.00", 12: "#,##0.00"})
    ws.auto_filter.ref = "A1:M%d" % (len(rows) + 1)
    ws2 = wb.create_sheet("Services")
    _sheet(ws2, ["Service", "Description", "Unit", "Rate (EUR, ex VAT)"], [list(s) for s in C.KB_SERVICES],
           [8, 44, 9, 12], {4: "#,##0.00"})
    wb.save(path)
    return len(rows)


def northmoor(path, cj):
    rows = [[j["job_no"], W.dd(j["date"]), j["herd"] or None, j["site"] or None, j["material"], j["method"], j["m3"],
             j["operator"]] for j in sorted(cj["nm"], key=lambda j: j["job_no"])]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Job sheets 2026"
    _sheet(ws, ["Job No", "Date", "Herd No", "Site", "Product", "Applicator", "Metered m3", "Operator"], rows,
           [11, 11, 11, 7, 13, 13, 10, 8], {2: "DD/MM/YYYY", 7: "0.0"})
    ws2 = wb.create_sheet("Sites")
    _sheet(ws2, ["Site", "Description"], [["AD01", "Lower Basin Biogas, digestate lagoon"],
                                          ["AD02", "Middle Uplands Anaerobic Digestion, outfield store"],
                                          ["AD03", "Atlantic Coast Renewables, digestate store"]], [7, 50])
    wb.save(path)
    return len(rows)


# --------------------------------------------------------------------------------------------- the context files
def fertiliser(path, land, rng):
    prods = [("CAN", 0.27), ("Urea", 0.46), ("Protected urea", 0.46), ("Compound 18-6-12", 0.18), ("Compound 10-10-20", 0.10)]
    qshare = {"2025Q4": 0.04, "2026Q1": 0.36, "2026Q2": 0.44, "2026Q3": 0.16}
    inten = {"D": 0.62, "B": 0.38, "G": 0.21, "W": 0.27}
    mix = {"CAN": 0.38, "Urea": 0.17, "Protected urea": 0.13, "Compound 18-6-12": 0.22, "Compound 10-10-20": 0.10}
    rows = []
    for i, r in enumerate(W.REG):
        tot = land[i] * inten[W.RTYPE[r]] * rng.uniform(0.9, 1.1)
        for q, qs in qshare.items():
            for p, n in prods:
                t = tot * qs * mix[p] * rng.uniform(0.8, 1.2)
                rows.append([r, q, p, round(t, 1), round(t * n, 1)])
    return _csv(path, ["Region", "Quarter", "Product", "Tonnes product", "Tonnes N"], rows)


def milk(path, w, rng):
    prof = [0.012, 0.035, 0.083, 0.118, 0.135, 0.126, 0.114, 0.101, 0.088, 0.077, 0.064, 0.047]
    rows = []
    for r in W.REG:
        cows = sum(h["size"] for h in w.herds if h["region"] == r and h["type"] == "dairy")
        sup = sum(1 for h in w.herds if h["region"] == r and h["type"] == "dairy")
        if not sup:
            continue
        year = cows * 5350 * rng.uniform(0.93, 1.07)
        for m, p in enumerate(prof):
            rows.append([r, "2025-%02d" % (m + 1), sup - int(rng.integers(0, 2)),
                         int(round(year * p * rng.uniform(0.96, 1.04), -2))])
    return _csv(path, ["Region", "Month", "Suppliers", "Milk intake (litres)"], rows)


def pigs_poultry(path, rng):
    rows = []
    for r in W.REG:
        av = r in C.ARDVALE_REGIONS
        sows = int(rng.integers(900, 2600)) if av else int(rng.integers(0, 400))
        rows.append([int(W.RCODE[r]), sows, int(sows * rng.uniform(9.5, 11.5)), int(rng.integers(20000, 160000)),
                     int(rng.integers(30000, 410000)), int(rng.integers(2000, 21000))])
    return _csv(path, ["REGION", "BREEDING_SOWS", "OTHER_PIGS", "LAYING_HENS", "BROILERS", "OTHER_POULTRY"], rows)


EXPORT_NOTES = """NATIONAL BOVINE REGISTER
Exports for the Ammonia Programme Unit, programme year 2025-26
Extract run 09/11/2026 06:12 from the live register. Data management: Noel Herity.

FILES
  nbr_animals_2025-26.csv          one row per animal present in the State at any time from 01/11/2025 to 31/10/2026
  nbr_movements_2025-26.csv        one row per movement with a departure date from 01/11/2025 to 31/10/2026
  nbr_herd_register_2026-11.xlsx   every herd number on the register at the extract date, with earlier holders of a
                                   reissued number

Dates are DD/MM/YYYY. Herd numbers are the region letter, a digit and six digits (C2123456). Tag numbers are the
herd-of-birth region letter, the two-digit year of birth, a six-digit serial and a check digit.

nbr_animals_2025-26.csv
  TAG_NUMBER          the animal's tag
  SEX                 M or F
  BREED               breed code, a cross shown as the sire's breed code followed by X
  DATE_OF_BIRTH
  DATE_REGISTERED     the date the birth was registered; a birth is registered within 27 days
  DAM_TAG             the dam's tag, where the dam is in this export
  BIRTH_HERD          the herd of birth
  HERD_AT_START       the herd holding the animal on 01/11/2025, or its herd of birth if it was born after that date
  FIRST_CALVING_DATE  the date of a female's first calving, where she has calved
  EXIT_DATE           the date the animal left the register
  EXIT_TYPE           SL slaughtered, DF died on farm (collected by a knackery), EX exported live
  EXIT_HERD           the slaughter plant, knackery or export assembly centre that recorded the exit

nbr_movements_2025-26.csv
  MOVEMENT_ID         the register's movement number
  TAG_NUMBER
  DEPARTURE_HERD      the herd the animal left
  DEPARTURE_DATE      the date it left
  DESTINATION_HERD    the herd that received it
  ARRIVAL_DATE        the date it was received; the register holds an animal in its departure herd until this date
  Marts, dealers' premises and export assembly centres are herds in their own right, so a sale through a mart is two
  movements, farm to mart and mart to farm. An exit is recorded on the animal, not as a movement.

nbr_herd_register_2026-11.xlsx (sheet Herds)
  Herd type           Farm, Mart, Dealer, Slaughter plant, Knackery or Export assembly centre
  District, Region    the herd's district and its region in the 2024 regional structure; Region code (pre-2024) is
                      the region code the herd had before 1 January 2024
  NSO farm no         the statistics office's farm number for the June census; a farmer's herds share one
  Main herd no        for a second herd number a farmer keeps on an out-farm, the farmer's main herd number
  Valid from, to      the dates the number was held; a number reissued to a new holder has a row for each holder
"""


def export_notes(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EXPORT_NOTES.replace("\n", "\r\n"))
