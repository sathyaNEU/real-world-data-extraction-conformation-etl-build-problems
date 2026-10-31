"""The two asks from the shipped files: each municipality's resident births and resident deaths in the estimate year,
by the municipality the residence lies in (the county's address points), and the readings a careful solver takes
instead (the written city of residence, the registrar's residence code)."""
import functools
import os
import re

import pandas as pd

import world as W

SUFFIX = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "LANE": "LN", "COURT": "CT", "ROAD": "RD", "CIRCLE": "CIR",
          "TRAIL": "TRL", "PLACE": "PL", "WAY": "WAY", "PARKWAY": "PKWY", "TERRACE": "TER"}
SHORTS = set(SUFFIX.values())


def norm(addr):
    """house number, street name and suffix of a written address: case folded, the suffix abbreviated, the unit
    dropped (every unit of a building lies in one municipality)"""
    a = re.sub(r"\s+", " ", addr.upper().strip())
    a = re.sub(r"\s+(APT|UNIT|#)\s*\S+$", "", a)
    a = re.sub(r"\s+#\S+$", "", a)
    parts = a.split(" ")
    num, rest = parts[0], parts[1:]
    if rest and rest[-1] in SUFFIX:
        rest[-1] = SUFFIX[rest[-1]]
    if rest and rest[-1] in SHORTS:
        return num, " ".join(rest[:-1]), rest[-1]
    return num, " ".join(rest), ""


@functools.lru_cache(maxsize=None)
def points(t):
    p = pd.read_csv(os.path.join(t, W.FILES["points"]), dtype=str, keep_default_na=False)
    p = p.sort_values(["STATUS"])           # an Active point before a Retired one at the same address
    key = list(zip(p["ADD_NUM"], p["ST_NAME"], p["ST_TYPE"]))
    out = {}
    for k, m in zip(key, p["MCD"]):
        out.setdefault(k, m)
    return out


def in_window(dates):
    d = pd.to_datetime(dates)
    return (d >= pd.Timestamp(W.VITAL_FROM)) & (d <= pd.Timestamp(W.VITAL_TO))


def city_to_muni(city):
    c = city.upper().strip()
    for pre in ("TOWN OF ", "VILLAGE OF ", "CITY OF "):
        c = c.replace(pre, "")
    c = re.sub(r" (TWP|VLG|CITY)$", "", c)
    hit = [m[1] for m in W.MUNIS if m[1].split(" of ", 1)[1].upper() == c]
    return hit[0] if hit else None


def by_address(t, df, col):
    pts = points(t)
    mcd = [pts.get(norm(a)) for a in df[col]]
    assert all(mcd), "an address with no point"
    return pd.Series([W.NAME[m] for m in mcd], index=df.index)


@functools.lru_cache(maxsize=None)
def births(t):
    b = pd.read_csv(os.path.join(t, W.FILES["births"]), dtype=str, keep_default_na=False)
    b = b[in_window(b["CHILD_DOB"])]
    gold = by_address(t, b, "RES_STREET").value_counts().to_dict()
    naive = b["RES_CITY"].map(city_to_muni).value_counts().to_dict()
    names = [m[1] for m in W.MUNIS]
    return {n: int(gold.get(n, 0)) for n in names}, {n: int(naive.get(n, 0)) for n in names}


@functools.lru_cache(maxsize=None)
def deaths(t):
    d = pd.read_csv(os.path.join(t, W.FILES["deaths"]), dtype=str, keep_default_na=False)
    d = d[in_window(d["DATE_OF_DEATH"])]
    gold = by_address(t, d, "RES_STREET").value_counts().to_dict()
    naive = d["RES_MCD_CODE"].str[-5:].map(W.NAME).value_counts().to_dict()
    city = d["RES_CITY"].map(city_to_muni).value_counts().to_dict()
    names = [m[1] for m in W.MUNIS]
    return ({n: int(gold.get(n, 0)) for n in names}, {n: int(naive.get(n, 0)) for n in names},
            {n: int(city.get(n, 0)) for n in names})
