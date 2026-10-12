"""The world behind the pack: the real register, and Tallybridge's book drawn over it.

Everything is seeded. The register files are the DfE extract of 7 October 2026, read as published.
"""
import datetime as dt
import hashlib
import math
import os
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
EXTRACT = "20261007"
GIAS_URL = "https://ea-edubase-api-prod.azurewebsites.net/edubase/downloads/public/"
REG_FILES = {
    "est": f"edubasealldata{EXTRACT}.csv",
    "links": f"links_edubasealldata{EXTRACT}.csv",
    "groups": f"allgroupsdata{EXTRACT}.csv",
    "members": f"academiesmatmembership{EXTRACT}.csv",
}

SEED = 116
AS_AT = dt.date(2026, 10, 1)            # the book is read at 1 October 2026
PILOT_PRICED = dt.date(2026, 6, 15)     # pilot quotes priced on the register as then published
LICENCE_START = dt.date(2026, 9, 1)
PRICE_CHANGE = dt.date(2026, 4, 1)      # 2026-27 prices apply to terms starting on or after this date
CUTOVER = dt.date(2026, 5, 1)           # new billing platform from this date
RATE = 4.05                             # Trust Licence, per pupil on roll
PRICE = {("2025-26", "Primary"): 4.40, ("2025-26", "Secondary"): 5.10,
         ("2026-27", "Primary"): 4.60, ("2026-27", "Secondary"): 5.30}
MINIMUM = {"2025-26": 820.0, "2026-27": 850.0}
SIGN_RATE_NUM, SIGN_RATE_DEN = 7, 13   # Trust Licence offers closed to date: the pilot's 12 and one in September
MARGIN = 0.12                           # reseller margin on framework contracts
TERM_WEEK0 = dt.date(2026, 9, 7)        # first counted week of the autumn term
TERM_WEEKS = 6

SELL_TYPES = {
    "Academies": {"Academy converter", "Academy sponsor led", "Academy special converter", "Academy special sponsor led"},
    "Free Schools": {"Free schools", "Free schools special"},
    "Local authority maintained schools": {"Community school", "Foundation school", "Voluntary aided school",
                                           "Voluntary controlled school"},
    "Special schools": {"Community special school", "Foundation special school"},
}
PRIMARY_PHASES = {"Primary", "Middle deemed primary"}


def rng(*key):
    h = hashlib.sha256(("%d|" % SEED + "|".join(map(str, key))).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "big"))


def fetch():
    CACHE.mkdir(exist_ok=True)
    for name in REG_FILES.values():
        p = CACHE / name
        if not p.exists():
            urllib.request.urlretrieve(GIAS_URL + name, p)
    return {k: CACHE / v for k, v in REG_FILES.items()}


def gdate(s):
    """Register dates are dd-mm-yyyy."""
    return pd.to_datetime(s, format="%d-%m-%Y", errors="coerce")


def band_of(phase):
    return "Primary" if phase in PRIMARY_PHASES else "Secondary"


def add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:
        return d.replace(year=d.year + n, day=28)


def term_for(start, on):
    """The annual term of an agreement that started on `start`, in force on date `on`."""
    k = on.year - start.year
    ts = add_years(start, k)
    if ts > on:
        ts = add_years(start, k - 1)
    te = add_years(ts, 1) - dt.timedelta(days=1)
    return ts, te


def price_year(term_start):
    return "2026-27" if term_start >= PRICE_CHANGE else "2025-26"


def annual_value(band, term_start, pupils):
    py = price_year(term_start)
    return round(max(PRICE[(py, band)] * pupils, MINIMUM[py]), 2)


class Register:
    def __init__(self):
        paths = fetch()
        self.est = pd.read_csv(paths["est"], encoding="latin-1", low_memory=False)
        self.links = pd.read_csv(paths["links"], encoding="latin-1", low_memory=False)
        self.groups = pd.read_csv(paths["groups"], encoding="latin-1", low_memory=False,
                                  dtype={"Companies House Number": str})
        self.members = pd.read_csv(paths["members"], encoding="latin-1", low_memory=False)
        e = self.est
        e["open_d"] = gdate(e["OpenDate"])
        e["close_d"] = gdate(e["CloseDate"])
        self.by_urn = e.set_index("URN")
        cols = ["PhaseOfEducation (name)", "NumberOfPupils", "LA (code)", "EstablishmentNumber", "PreviousLA (code)",
                "PreviousEstablishmentNumber", "EstablishmentName", "open_d", "EstablishmentStatus (name)",
                "EstablishmentTypeGroup (name)", "TypeOfEstablishment (name)", "Trusts (code)", "GOR (name)",
                "close_d", "LA (name)"]
        self.info = {int(u): dict(zip(cols, vals)) for u, vals in zip(e["URN"], e[cols].itertuples(index=False))}
        mats = self.groups[(self.groups["Group Type"] == "Multi-academy trust") & (self.groups["Group Status"] == "Open")]
        self.mat_uids = set(mats["Group UID"].astype(int))
        self.group_name = dict(zip(self.groups["Group UID"].astype(int), self.groups["Group Name"]))
        self.group_ch = dict(zip(self.groups["Group UID"].astype(int), self.groups["Companies House Number"]))
        # successor links: predecessor URN -> current URN, from the academy's own 'Predecessor' rows
        pl = self.links[self.links["LinkType"] == "Predecessor"]
        self.pred_of = pl.groupby("URN")["LinkURN"].apply(list).to_dict()
        # membership changes after 1 June 2026, from the membership history
        m = self.members
        j = pd.to_datetime(m["Date Joined Group"], format="%Y-%m-%d", errors="coerce")
        lft = pd.to_datetime(m["Date Left Group"], format="%Y-%m-%d", errors="coerce")
        moved = m[(j >= "2026-06-01") | (lft >= "2026-06-01")]
        self.moved_since_june = set(moved["Group UID"].dropna().astype(int))

    def open_state(self):
        e = self.est
        o = e[e["EstablishmentStatus (name)"] == "Open"].copy()
        ok = np.zeros(len(o), bool)
        for grp, types in SELL_TYPES.items():
            ok |= (o["EstablishmentTypeGroup (name)"] == grp) & o["TypeOfEstablishment (name)"].isin(types)
        o = o[ok]
        o = o[o["PhaseOfEducation (name)"].isin(["Primary", "Secondary", "All-through", "Middle deemed primary",
                                                  "Middle deemed secondary", "Not applicable"])]
        o = o[o["NumberOfPupils"].notna() & (o["NumberOfPupils"] > 0)]
        o["band"] = o["PhaseOfEducation (name)"].map(band_of)
        o["tcode"] = o["Trusts (code)"]
        return o

    def trust_academies(self, uid):
        """Every academy the register shows open in the trust (any type)."""
        e = self.est
        return e[(e["Trusts (code)"] == uid) & (e["EstablishmentStatus (name)"] == "Open")]
