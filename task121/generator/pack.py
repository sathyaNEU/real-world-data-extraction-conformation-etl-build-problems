"""Read the cut pack back for the golden, the asks, the checks and the cracker: every figure is computed from the
shipped files, never from the generator's world."""
import os

import pandas as pd

import common as K

_CACHE = {}


def load(target):
    key = os.path.abspath(target)
    if key in _CACHE:
        return _CACHE[key]
    p = lambda k: os.path.join(target, K.FILES[k])
    d = {}
    for k in ("takers", "roster", "calls", "epcr", "units", "che", "tcpr", "casereview", "unithours"):
        d[k] = pd.read_csv(p(k), dtype=str, keep_default_na=False)
    d["trunks"] = pd.read_excel(p("reference"), sheet_name="Trunk groups", dtype=str)
    _CACHE[key] = d
    return d


def local(s, seconds=True):
    return pd.to_datetime(s, format="%m/%d/%Y %H:%M:%S" if seconds else "%m/%d/%Y %H:%M")


def month(ts):
    return list(zip(ts.dt.year, ts.dt.month))
