"""The fiction's fixed furniture: garages, stations and their identifier history, the vehicles,
the permits, the vehicle checks, the city fleet and the vehicle reference list.

Everything here is deterministic given the seeded generator passed in.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

GARAGES = {
    "CCN": "Civic Center North Deck",
    "CCS": "Civic Center South Deck",
    "LIB": "Library Garage",
    "FTG": "Ferry Terminal Garage",
    "MSG": "Market Square Garage",
    "CSG": "Cedar Street Garage",
    "SWG": "Seawall Garage",
    "ETG": "Eastside Transit Garage",
}
DECKS = ("CCN", "CCS")
POS_PREFIX = {"CCN": "N", "CCS": "S", "LIB": "L", "FTG": "F", "MSG": "M", "CSG": "C", "SWG": "W", "ETG": "E"}
N_UNITS = {"CCN": 16, "CCS": 16, "LIB": 8, "FTG": 8, "MSG": 10, "CSG": 6, "SWG": 6, "ETG": 8}
INSTALLED = {"CCN": date(2020, 9, 14), "CCS": date(2021, 3, 22), "LIB": date(2019, 6, 3),
             "FTG": date(2018, 11, 5), "MSG": date(2019, 10, 21), "CSG": date(2021, 8, 9),
             "SWG": date(2022, 5, 16), "ETG": date(2020, 2, 10)}
MIGRATION = date(2025, 4, 1)           # platform move: every station takes a new identifier
LIB_FAST_FROM = date(2024, 1, 8)       # the network's only 11.5 kW unit, Library L-09
REISSUE = {"FTG": (date(2025, 8, 18), 4), "MSG": (date(2025, 10, 6), 2)}
REISSUED_POS = ["N-03", "N-08", "N-14", "S-02", "S-09", "S-13"]  # their old identifiers are freed and reissued
GATEWAY_B_POS = ["N-01", "N-02", "N-05", "N-06"]  # reported through the legacy gateway until GATEWAY_B_END
GATEWAY_B_END = date(2024, 4, 22)
RESTATED_POS = ["S-04", "S-05", "S-11", "S-12"]
BACKFED_POS = "N-11"
BACKFEED = (date(2026, 6, 1), date(2026, 7, 12))


def build_stations(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (positions, register).

    positions: one row per physical unit (garage, position, rating, old_id, new_id, from, to).
    register: the shipped identifier history, one row per identifier assignment.
    """
    pos_rows = []
    for g in GARAGES:
        for i in range(1, N_UNITS[g] + 1):
            pos_rows.append({"garage": g, "position": f"{POS_PREFIX[g]}-{i:02d}", "rating_kw": 6.6,
                             "installed": INSTALLED[g], "model": "PL-30"})
    pos_rows.append({"garage": "LIB", "position": "L-09", "rating_kw": 11.5, "installed": LIB_FAST_FROM,
                     "model": "PL-48"})
    for g, (d0, n) in REISSUE.items():
        for i in range(n):
            pos_rows.append({"garage": g, "position": f"{POS_PREFIX[g]}-{N_UNITS[g] + i + 1:02d}",
                             "rating_kw": 6.6, "installed": d0, "model": "PL-30"})
    pos = pd.DataFrame(pos_rows)

    # old identifiers: six-digit, allocated in install order from interleaved blocks
    pre = pos[pos["installed"] < MIGRATION].copy()
    pre = pre.sort_values(["installed", "garage", "position"]).reset_index(drop=True)
    used = set()
    old_ids = []
    cursor = 104000 + int(rng.integers(100, 300))
    last_inst = None
    for _, r in pre.iterrows():
        if r["installed"] != last_inst:
            cursor += int(rng.integers(40, 260))
            last_inst = r["installed"]
        cursor += int(rng.integers(1, 4))
        while cursor in used:
            cursor += 1
        used.add(cursor)
        old_ids.append(cursor)
    pre["old_id"] = old_ids
    pos = pos.merge(pre[["garage", "position", "old_id"]], on=["garage", "position"], how="left")

    # new identifiers at the migration for every unit then in service
    inserv = pos[pos["installed"] < MIGRATION].index
    perm = rng.permutation(len(inserv))
    base = 317000 + int(rng.integers(200, 700))
    new_ids = []
    used_new = set()
    cur = base
    for k in range(len(inserv)):
        cur += int(rng.integers(1, 9))
        new_ids.append(cur)
        used_new.add(cur)
    new_col = pd.Series(pd.NA, index=pos.index, dtype="Int64")
    for j, idx in enumerate(inserv):
        new_col.loc[idx] = new_ids[perm[j]]
    pos["new_id"] = new_col

    # units installed after the migration take freed identifiers from the pool: the decks' six
    reissued_old = pos.set_index("position").loc[REISSUED_POS, "old_id"].astype(int).tolist()
    later = pos[pos["installed"] >= MIGRATION].sort_values(["installed", "position"]).index.tolist()
    order = rng.permutation(len(reissued_old))
    reissue_map = {}
    for j, idx in enumerate(later):
        reissue_map[idx] = reissued_old[order[j]]
    pos["reissued_id"] = pd.Series({k: v for k, v in reissue_map.items()}, dtype="Int64")

    # register rows
    reg = []
    for _, r in pos.iterrows():
        if pd.notna(r["old_id"]):
            reg.append({"station_id": int(r["old_id"]), "garage": GARAGES[r["garage"]], "position": r["position"],
                        "unit_model": r["model"], "rating_kw": r["rating_kw"],
                        "in_service_from": r["installed"], "in_service_to": MIGRATION - timedelta(days=1)})
        if pd.notna(r["new_id"]):
            reg.append({"station_id": int(r["new_id"]), "garage": GARAGES[r["garage"]], "position": r["position"],
                        "unit_model": r["model"], "rating_kw": r["rating_kw"],
                        "in_service_from": MIGRATION, "in_service_to": None})
        if pd.notna(r["reissued_id"]):
            reg.append({"station_id": int(r["reissued_id"]), "garage": GARAGES[r["garage"]], "position": r["position"],
                        "unit_model": r["model"], "rating_kw": r["rating_kw"],
                        "in_service_from": r["installed"], "in_service_to": None})
    register = pd.DataFrame(reg).sort_values(["station_id", "in_service_from"]).reset_index(drop=True)
    return pos, register


def station_id_at(pos_row, d: date) -> int:
    """The identifier a unit reported under on local date d."""
    if pd.notna(pos_row.get("reissued_id")) and pd.isna(pos_row.get("old_id")):
        return int(pos_row["reissued_id"])
    if d < MIGRATION:
        return int(pos_row["old_id"])
    return int(pos_row["new_id"])


# --- vehicles ---------------------------------------------------------------------------------
# (make, model, trim, year_from, year_to, body_class, fuel, onboard_kw, permit_class)
REFERENCE = [
    ("Chevrolet", "Bolt EV", "", 2017, 2021, "Hatchback", "BEV", 7.2, "A"),
    ("Chevrolet", "Bolt EV", "", 2022, 2023, "Hatchback", "BEV", 11.0, "A"),
    ("Chevrolet", "Bolt EUV", "", 2022, 2023, "Small SUV", "BEV", 11.0, "A"),
    ("Hyundai", "Kona Electric", "", 2019, 2023, "Small SUV", "BEV", 7.2, "A"),
    ("Hyundai", "Ioniq 5", "", 2022, 2024, "SUV", "BEV", 10.9, "B"),
    ("Kia", "Niro EV", "", 2019, 2022, "Small SUV", "BEV", 7.2, "A"),
    ("Kia", "Niro EV", "", 2023, 2024, "Small SUV", "BEV", 11.0, "A"),
    ("Kia", "EV6", "", 2022, 2024, "SUV", "BEV", 10.9, "B"),
    ("Nissan", "Leaf", "", 2018, 2023, "Hatchback", "BEV", 6.6, "A"),
    ("Nissan", "Ariya", "", 2023, 2024, "SUV", "BEV", 7.2, "B"),
    ("Tesla", "Model 3", "Standard Range Plus", 2019, 2021, "Sedan", "BEV", 7.7, "B"),
    ("Tesla", "Model 3", "Long Range", 2018, 2023, "Sedan", "BEV", 11.5, "B"),
    ("Tesla", "Model Y", "Long Range", 2020, 2024, "SUV", "BEV", 11.5, "B"),
    ("Volkswagen", "ID.4", "", 2021, 2024, "SUV", "BEV", 11.0, "B"),
    ("Volvo", "XC40 Recharge", "", 2021, 2023, "Small SUV", "BEV", 11.0, "A"),
    ("Polestar", "2", "", 2021, 2024, "Sedan", "BEV", 11.0, "B"),
    ("BMW", "i3", "", 2017, 2021, "Hatchback", "BEV", 7.4, "A"),
    ("Ford", "F-150 Lightning", "Standard Range", 2022, 2024, "Pickup", "BEV", 11.3, "C"),
    ("Ford", "F-150 Lightning", "Extended Range", 2022, 2024, "Pickup", "BEV", 19.2, "C"),
    ("Ford", "E-Transit", "", 2022, 2024, "Van", "BEV", 11.3, "C"),
    ("Rivian", "R1T", "", 2022, 2024, "Pickup", "BEV", 11.5, "C"),
    ("Toyota", "Prius Prime", "", 2017, 2022, "Hatchback", "PHEV", 3.3, "A"),
    ("Toyota", "RAV4 Prime", "", 2021, 2024, "SUV", "PHEV", 3.3, "B"),
]

VIN_WMI = {  # (make, model, trim) -> VIN prefix through position 8, plant code
    ("Chevrolet", "Bolt EV", ""): ("1G1FY6S0", "4"),
    ("Chevrolet", "Bolt EUV", ""): ("1G1FZ6S0", "4"),
    ("Hyundai", "Kona Electric", ""): ("KM8K23AG", "U"),
    ("Kia", "Niro EV", ""): ("KNDCC3LG", "5"),
    ("Nissan", "Ariya", ""): ("JN1AF0BA", "M"),
    ("Tesla", "Model 3", "Standard Range Plus"): ("5YJ3E1EA", "F"),
    ("Volkswagen", "ID.4", ""): ("WVGDMPE2", "P"),
    ("Volvo", "XC40 Recharge", ""): ("YV4ED3UR", "2"),
    ("Polestar", "2", ""): ("LPSED3KA", "L"),
    ("Ford", "F-150 Lightning", "Extended Range"): ("1FTVW1EL", "W"),
    ("Ford", "E-Transit", ""): ("1FTBW9CK", "K"),
}
YEAR_CODE = {2017: "H", 2018: "J", 2019: "K", 2020: "L", 2021: "M", 2022: "N", 2023: "P", 2024: "R"}
_TRANS = {**{str(i): i for i in range(10)}, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
          "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9, "S": 2, "T": 3, "U": 4, "V": 5, "W": 6,
          "X": 7, "Y": 8, "Z": 9}
_W = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def make_vin(make, model, trim, year, serial) -> str:
    prefix, plant = VIN_WMI[(make, model, trim)]
    body = prefix + "0" + YEAR_CODE[year] + plant + f"{serial:06d}"
    total = sum(_TRANS[c] * w for c, w in zip(body, _W))
    chk = total % 11
    chk = "X" if chk == 10 else str(chk)
    return body[:8] + chk + body[9:]


def rating_of(make, model, trim, year) -> float:
    for mk, md, tr, y0, y1, *_rest in REFERENCE:
        if mk == make and md == model and y0 <= year <= y1 and (tr == "" or tr == trim):
            return _rest[2]
    raise KeyError((make, model, trim, year))


_LET = "ABCDEFGHJKLMNPRSTVWXYZ"


def plate(rng, used) -> str:
    while True:
        p = "".join(rng.choice(list(_LET), 3)) + f"{int(rng.integers(1000, 9999)):04d}"
        if p not in used:
            used.add(p)
            return p


def build_vehicles_and_permits(rng: np.random.Generator):
    """Permits (with history), their vehicles by date, the vehicle checks and the fleet roster.

    Returns dict with:
      permits   DataFrame (shipped registry rows)
      checks    DataFrame (shipped check rows)
      pveh      DataFrame internal: permit_no, from, to, make, model, trim, year, plate, rating
      fleet     DataFrame (shipped roster) with internal rating column
    """
    used_plates: set[str] = set()
    serial = iter(rng.permutation(np.arange(110000, 990000, 37))[:400].tolist())

    def vehicle(make, model, trim, year):
        return {"make": make, "model": model, "trim": trim, "year": year,
                "vin": make_vin(make, model, trim, year, next(serial)), "plate": plate(rng, used_plates),
                "rating": rating_of(make, model, trim, year)}

    permits, pveh = [], []
    pno = 20400 + int(rng.integers(5, 60))

    def next_no():
        nonlocal pno
        pno += int(rng.integers(1, 6))
        return f"P-{pno}"

    # North: the county motor pool block (40 permits from 2022, four more from the 2025 renewal)
    # and four private holders, all at the same Tesla trim
    county_issue = [date(2022, 7, 11)] * 40 + [date(2025, 1, 13)] * 4
    for k, iss in enumerate(county_issue):
        yr = 2020 if k < 24 else 2021
        v = vehicle("Chevrolet", "Bolt EV", "", yr)
        no = next_no()
        permits.append({"permit_no": no, "deck": "North", "holder": "Larch County Fleet Services",
                        "holder_type": "Agency", "issued": iss, "status": "ACTIVE", **v})
        pveh.append({"permit_no": no, "from": iss, "to": date(2027, 12, 31), **v})
    for k in range(4):
        yr = [2019, 2020, 2020, 2021][k]
        v = vehicle("Tesla", "Model 3", "Standard Range Plus", yr)
        iss = [date(2021, 2, 1), date(2021, 9, 20), date(2022, 3, 14), date(2023, 1, 9)][k]
        no = next_no()
        permits.append({"permit_no": no, "deck": "North", "holder": f"EMP-{int(rng.integers(30000, 49999))}",
                        "holder_type": "Employee", "issued": iss, "status": "ACTIVE", **v})
        pveh.append({"permit_no": no, "from": iss, "to": date(2027, 12, 31), **v})

    # South: 25 private holders in 2026; a few changed vehicle at the 2025 renewal, two permits are new in 2025,
    # and two lapsed holders ran to the end of 2024
    south_now = ([("Hyundai", "Kona Electric", "", 2019), ("Hyundai", "Kona Electric", "", 2020),
                  ("Hyundai", "Kona Electric", "", 2021), ("Kia", "Niro EV", "", 2019), ("Kia", "Niro EV", "", 2021),
                  ("Nissan", "Ariya", "", 2023)]
                 + [("Tesla", "Model 3", "Standard Range Plus", y) for y in (2019, 2020, 2021)]
                 + [("Volkswagen", "ID.4", "", y) for y in (2021, 2021, 2022, 2022, 2023, 2023)]
                 + [("Polestar", "2", "", y) for y in (2021, 2022, 2022)]
                 + [("Volvo", "XC40 Recharge", "", y) for y in (2021, 2022, 2023)]
                 + [("Kia", "Niro EV", "", y) for y in (2023, 2023)]
                 + [("Chevrolet", "Bolt EUV", "", y) for y in (2022, 2023)])
    assert len(south_now) == 25
    changed_2025 = {9: ("Hyundai", "Kona Electric", "", 2019), 12: ("Chevrolet", "Bolt EV", "", 2019),
                    16: ("Kia", "Niro EV", "", 2020)}  # index in south_now -> vehicle held before Jan 2025
    new_2025 = {20, 23}
    order = rng.permutation(25)
    for j in order:
        mk, md, tr, yr = south_now[j]
        iss = date(2025, 1, 21) if j in new_2025 else [date(2021, 4, 5), date(2021, 10, 18), date(2022, 6, 6),
                                                       date(2023, 2, 13), date(2023, 8, 28)][j % 5]
        first_car_year = changed_2025[j][3] if j in changed_2025 else yr
        if iss < date(first_car_year - 1, 9, 15):
            iss = date(first_car_year - 1, 9, 15) + timedelta(days=int(rng.integers(20, 160)))
        no = next_no()
        v = vehicle(mk, md, tr, yr)
        permits.append({"permit_no": no, "deck": "South", "holder": f"EMP-{int(rng.integers(30000, 49999))}",
                        "holder_type": "Employee", "issued": iss, "status": "ACTIVE", **v})
        if j in changed_2025:
            ov = vehicle(*changed_2025[j])
            pveh.append({"permit_no": no, "from": iss, "to": date(2025, 1, 12), **ov})
            pveh.append({"permit_no": no, "from": date(2025, 1, 13), "to": date(2027, 12, 31), **v})
        else:
            pveh.append({"permit_no": no, "from": iss, "to": date(2027, 12, 31), **v})
    for k in range(2):
        mk, md, tr, yr = [("Kia", "Niro EV", "", 2020), ("Volkswagen", "ID.4", "", 2021)][k]
        no = next_no()
        v = vehicle(mk, md, tr, yr)
        iss = [date(2022, 1, 24), date(2022, 11, 7)][k]
        permits.append({"permit_no": no, "deck": "South", "holder": f"EMP-{int(rng.integers(30000, 49999))}",
                        "holder_type": "Employee", "issued": iss, "status": "LAPSED", **v})
        pveh.append({"permit_no": no, "from": iss, "to": date(2024, 12, 31), **v})

    permits = pd.DataFrame(permits)
    pveh = pd.DataFrame(pveh)

    # vehicle checks: at issue and at every January renewal up to January 2027
    checks = []
    for _, p in pveh.iterrows():
        d = p["from"]
        dates = [d]
        y = d.year + 1
        # a vehicle replaced at a January renewal is not checked at that renewal
        last_year = p["to"].year - 1 if p["to"].month == 1 else p["to"].year
        while y <= last_year and date(y, 1, 1) <= min(p["to"], date(2027, 1, 18)):
            dd = date(y, 1, 5) + timedelta(days=int(rng.integers(0, 9)))
            if dd >= p["from"] and dd <= p["to"] and dd <= date(2027, 1, 15):
                dates.append(dd)
            y += 1
        for dd in dates:
            if dd > date(2027, 1, 15):
                continue
            checks.append({"permit_no": p["permit_no"], "plate": p["plate"], "vin": p["vin"],
                           "make": p["make"].upper(), "model": p["model"].upper(), "trim": p["trim"].upper(),
                           "model_year": p["year"], "checked_on": dd})
    checks = pd.DataFrame(checks).sort_values(["checked_on", "permit_no"]).reset_index(drop=True)

    # city fleet
    fleet_spec = ([("Parking Enforcement", "Chevrolet", "Bolt EUV", "", 2022)] * 6
                  + [("Facilities Maintenance", "Ford", "F-150 Lightning", "Extended Range", 2022)]
                  + [("Facilities Maintenance", "Chevrolet", "Bolt EV", "", 2021)] * 2
                  + [("Public Works", "Chevrolet", "Bolt EV", "", 2020)] * 4
                  + [("Public Works", "Ford", "E-Transit", "", 2022)] * 2
                  + [("Parks & Recreation", "Hyundai", "Kona Electric", "", 2021)] * 2
                  + [("Building Inspection", "Kia", "Niro EV", "", 2021)] * 2)
    fleet = []
    unit = 2100 + int(rng.integers(10, 80))
    card = 70400 + int(rng.integers(10, 90))
    for dept, mk, md, tr, yr in fleet_spec:
        unit += int(rng.integers(1, 7))
        card += int(rng.integers(3, 17))
        v = vehicle(mk, md, tr, yr)
        fleet.append({"unit_no": f"LH-{unit}", "fleet_card": f"FC-{card}", "department": dept,
                      "make": mk, "model": md, "trim": tr, "model_year": yr, "plate": v["plate"], "vin": v["vin"],
                      "in_service": date(yr, 1, 1) + timedelta(days=int(rng.integers(60, 300))),
                      "rating": v["rating"]})
    fleet = pd.DataFrame(fleet)
    pveh, checks, changed = renew_county_2027(pveh, checks, permits, used_plates)
    return {"permits": permits, "pveh": pveh, "checks": checks, "fleet": fleet, "changed_2027": changed}


RENEWAL_SEED = 2027_0111
N_RENEWED = 18


def renew_county_2027(pveh: pd.DataFrame, checks: pd.DataFrame, permits: pd.DataFrame, used_plates: set):
    """The January 2027 renewal: Larch County Fleet Services renewed 18 of its 24 permits held by 2020
    Bolt EVs onto 2023 Bolt EVs, the same make and model in a later model year. The renewal check row
    names the replacement; the replaced car stays on its permit until the day before. Drawn on its own
    stream so nothing else in the world moves."""
    rng = np.random.default_rng(RENEWAL_SEED)
    county = set(permits.loc[permits["holder"] == "Larch County Fleet Services", "permit_no"])
    cur = pveh[(pveh["permit_no"].isin(county)) & (pveh["to"] == date(2027, 12, 31)) & (pveh["year"] == 2020)
               & (pveh["model"] == "Bolt EV")]
    assert len(cur) == 24, len(cur)
    pick = sorted(rng.choice(cur["permit_no"].to_numpy(), size=N_RENEWED, replace=False).tolist())
    serials = iter(rng.permutation(np.arange(110003, 990000, 37))[:N_RENEWED].tolist())
    new_rows = []
    checks = checks.copy()
    pveh = pveh.copy()
    for pn in pick:
        i = cur.index[cur["permit_no"] == pn][0]
        jan = checks[(checks["permit_no"] == pn) & (checks["checked_on"] >= date(2027, 1, 1))]
        assert len(jan) == 1, (pn, len(jan))
        renewed = jan["checked_on"].iloc[0]
        plate_new = plate(rng, used_plates)
        vin_new = make_vin("Chevrolet", "Bolt EV", "", 2023, next(serials))
        pveh.at[i, "to"] = renewed - timedelta(days=1)
        new_rows.append({"permit_no": pn, "from": renewed, "to": date(2027, 12, 31), "make": "Chevrolet",
                         "model": "Bolt EV", "trim": "", "year": 2023, "vin": vin_new, "plate": plate_new,
                         "rating": rating_of("Chevrolet", "Bolt EV", "", 2023)})
        j = jan.index[0]
        checks.loc[j, ["plate", "vin", "model_year"]] = [plate_new, vin_new, 2023]
    pveh = pd.concat([pveh, pd.DataFrame(new_rows)], ignore_index=True)
    assert all(r == 11.0 for r in pveh.loc[pveh.index >= len(pveh) - N_RENEWED, "rating"])
    return pveh, checks, set(pick)


def reference_frame() -> pd.DataFrame:
    return pd.DataFrame(REFERENCE, columns=["make", "model", "trim", "model_year_from", "model_year_to",
                                            "body_class", "fuel", "onboard_charger_kw", "permit_class"])
