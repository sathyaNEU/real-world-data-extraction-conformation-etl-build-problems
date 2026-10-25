"""The pack as a solver reads it: every file loaded from target/ with the plain tools (pandas, openpyxl), parcel
numbers carried to the 2026 roll's form, nothing taken from the generator."""
import os

import pandas as pd

import common as K


def to26(dashed_no):
    """book-page-parcel as written in 2025 to the 2026 roll's identifier (suffix 0)."""
    return str(dashed_no).replace("-", "") + "0"


class Pack:
    def __init__(self, target):
        f = lambda k: os.path.join(target, K.FILES[k])
        self.roll26 = pd.read_csv(f("roll26"), dtype={"parcel_id": str, "nbhd_code": str})
        self.roll25 = pd.read_excel(f("roll25"), skiprows=3, dtype={"Parcel No.": str})
        self.crosswalk = pd.read_csv(f("crosswalk"), dtype={"nbhd_code": str})
        self.changes = pd.read_csv(f("changes"), dtype={"old_parcel_no": str, "new_parcel_id": str},
                                   parse_dates=["effective_date"])
        self.deeds = pd.read_csv(f("deeds"), dtype={"parcel_no": str, "instrument_no": str},
                                 parse_dates=["recorded_date", "deed_date"])
        self.index = pd.read_csv(f("index"), dtype={"period": str})
        self.permits = pd.read_csv(f("permits"), dtype={"parcel_no": str},
                                   parse_dates=["issued_date", "final_inspection_date"])
        self.bor = pd.read_csv(f("bor"), dtype={"parcel_no": str}, parse_dates=["hearing_date"])
        self.idx = dict(zip(self.index["period"], self.index["index_jan2025_100"]))
        self.roll25["pid26"] = self.roll25["Parcel No."].map(to26)
        self.deeds["pid26"] = self.deeds["parcel_no"].map(to26)
        self.permits["pid26"] = self.permits["parcel_no"].map(to26)
        self.bor["pid26"] = self.bor["parcel_no"].map(to26)
        name_to_code = dict(zip(self.crosswalk["nbhd_name"], self.crosswalk["nbhd_code"]))
        code_to_area = dict(zip(self.crosswalk["nbhd_code"], self.crosswalk["market_area"]))
        self.roll25["nbhd_code"] = self.roll25["Neighborhood"].map(name_to_code)
        self.roll25["market_area"] = self.roll25["nbhd_code"].map(code_to_area)
        self.roll26["market_area"] = self.roll26["nbhd_code"].map(code_to_area)
        self.code_to_area = code_to_area

    def index_carry(self, deed_dates):
        """Rule 18-7, 3.1: the index for January 2026 over the index for the deed's month."""
        jan = self.idx["2026-01"]
        return deed_dates.map(lambda d: jan / self.idx["%d-%02d" % (d.year, d.month)])
