"""Read the pack as shipped: every frame the analysis uses comes from target/, parsed the way the files say."""
from __future__ import annotations

import csv
import datetime as dt
import os
import re

import numpy as np
import openpyxl
import pandas as pd

import common as K

PARTS = ("lcp_ms", "ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms")


def _csv(target, name, **kw):
    return pd.read_csv(os.path.join(target, name), keep_default_na=False, na_values=[""], **kw)


def beacons(target):
    df = _csv(target, K.BEACONS, dtype={c: "float64" for c in PARTS}).rename(columns={"form_factor": "device"})
    df["fired_at_utc"] = pd.to_datetime(df.fired_at_utc, format="%Y-%m-%dT%H:%M:%SZ")
    return df


def sampling(target):
    out = {}
    for r in csv.DictReader(open(os.path.join(target, K.SAMPLING_CFG), encoding="utf-8")):
        out.setdefault(r["origin"], []).append((dt.datetime.strptime(r["effective_from_utc"], "%Y-%m-%dT%H:%M:%SZ"),
                                                float(r["sample_rate"])))
    return {o: sorted(v) for o, v in out.items()}


def weights(df, rates):
    """1 / the sampling rate in force for the beacon's origin when its page load started."""
    w = np.full(len(df), np.nan)
    t = df.fired_at_utc.to_numpy()
    org = df.origin.to_numpy()
    for o, hist in rates.items():
        m = org == o
        r = np.full(m.sum(), np.nan)
        for since, rate in hist:
            r = np.where(t[m] >= np.datetime64(since), rate, r)
        w[m] = 1.0 / r
    return w


def hosts(target):
    """property name -> (own image hosts, image CDN path prefix) from the CDN host list."""
    own, cdn = {}, {}
    for r in csv.DictReader(open(os.path.join(target, K.CDN_HOSTS), encoding="utf-8")):
        if r["kind"] in ("image host", "legacy image alias"):
            own.setdefault(r["property"], set()).add(r["host"])
        elif r["kind"] == "image CDN path":
            cdn[r["property"]] = r["path_prefix"]
    return {p: (own[p], cdn[p]) for p in own}


def origins(target):
    return {r["host"]: r["property"] for r in csv.DictReader(open(os.path.join(target, K.CDN_HOSTS), encoding="utf-8"))
            if r["kind"] == "page origin"}


def change_log(target):
    """engagement -> (before from, before to, shipped, after from, after to) as dates."""
    ws = openpyxl.load_workbook(os.path.join(target, K.ENG_LOG), data_only=True)["Engagements"]
    out = {}
    for row in ws.iter_rows(values_only=True):
        if isinstance(row[0], str) and re.fullmatch(r"E\d\d", row[0]):
            out[row[0]] = tuple(v.date() if isinstance(v, dt.datetime) else v for v in row[4:9])
    return out


def engagement_beacons(target):
    df = _csv(target, K.ENG_BEACONS, dtype={c: "float64" for c in PARTS}).rename(columns={"form_factor": "device"})
    df["fired_at_utc"] = pd.to_datetime(df.fired_at_utc, format="%Y-%m-%dT%H:%M:%SZ")
    return df


def image_logs(target):
    df = _csv(target, K.IMG_LOGS)
    df["hour_utc"] = pd.to_datetime(df.hour_utc, format="%Y-%m-%d %H:%M")
    return df


def legacy_log(target):
    df = _csv(target, K.LEGACY_LOGS)
    df["log_hour"] = pd.to_datetime(df.log_hour, format="%d/%b/%Y:%H %z")
    return df


def avif(target):
    ws = openpyxl.load_workbook(os.path.join(target, K.AVIF_TABLE), data_only=True)["AVIF sizes"]
    out = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0]:
            out[(row[0], row[1])] = (int(row[2]), int(row[3]), float(row[4]))
    return out


def cdn_rate(target):
    from pypdf import PdfReader
    text = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, K.CONTRACT)).pages)
    return float(re.search(r"AUD (\d+\.\d+) per GB", text).group(1))


def dam(target):
    return _csv(target, K.DAM, dtype={"asset_id": str, "legacy_id": str})
