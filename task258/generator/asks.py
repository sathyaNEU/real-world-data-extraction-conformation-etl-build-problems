"""The ask paths' world: the image hosts' hourly request rollups (UTC), the old media server's rollup for the two
legacy aliases (Sydney time), and the DAM's export of each property's hero-image collection. Requests follow each
property's expected page loads hour by hour; the DAM follows each property's page catalogue."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K
import world as W

SLOTS = ("hero", "inline", "thumbnail")


def _prefix(code, slot, cdn=False):
    w, h = K.SLOT_SIZES[code][slot]
    return ("/%s/i/%dx%d/" % (code, w, h)) if cdn else ("/i/%dx%d/" % (w, h))


def image_host_logs() -> pd.DataFrame:
    """Requests an hour by host, path prefix and status for every image host the group runs and the group image
    CDN, over the extract's whole UTC days. The legacy aliases are not in it: the old media server answers them."""
    hours = W._hours(K.EXTRACT_START_UTC, K.EXTRACT_END_UTC)
    rows = []
    for p in K.PROPERTIES:
        code = p["code"]
        r = K.stream("imglog", code)
        loads = W.expected_loads(p, hours)
        a_share = p["alias"][2] if p["alias"] else 0.0
        c_share = p["cdn_share"]
        reval = K.REVALIDATED[code]
        for slot in SLOTS:
            base = loads * K.REQUESTS_PER_LOAD[code][slot]
            for host, share, cdn in ((p["img"], 1.0 - a_share - c_share, False), (K.CDN_HOST, c_share, True)):
                if share <= 0:
                    continue
                for status, f in ((200, 1.0 - reval), (304, reval)):
                    n = r.poisson(base * share * f)
                    for t, k in zip(hours, n):
                        rows.append((t, host, _prefix(code, slot, cdn), status, int(k)))
    df = pd.DataFrame(rows, columns=["hour_utc", "host", "path_prefix", "status", "requests"])
    return df.sort_values(["hour_utc", "host", "path_prefix", "status"], kind="mergesort").reset_index(drop=True)


def legacy_log() -> pd.DataFrame:
    """The old media server's own hourly rollup for the legacy aliases, by its clock (Sydney time), for November's
    local days."""
    start = dt.datetime(2026, 11, 1, 0, 0)
    local = [start + dt.timedelta(hours=k) for k in range(30 * 24)]
    utc = [t - dt.timedelta(hours=K.UTC_OFFSET) for t in local]
    rows = []
    for p in K.PROPERTIES:
        if not p["alias"]:
            continue
        code, host, share = p["code"], p["alias"][0], p["alias"][2]
        r = K.stream("legacylog", code)
        loads = W.expected_loads(p, utc)
        reval = K.REVALIDATED[code]
        for slot in SLOTS:
            base = loads * K.REQUESTS_PER_LOAD[code][slot] * share
            for status, f in ((200, 1.0 - reval), (304, reval)):
                n = r.poisson(base * f)
                for t, k in zip(local, n):
                    rows.append((t, host, _prefix(code, slot), status, int(k)))
    df = pd.DataFrame(rows, columns=["log_hour", "vhost", "uri_dir", "code", "hits"])
    return df.sort_values(["log_hour", "vhost", "uri_dir", "code"], kind="mergesort").reset_index(drop=True)


CAMERA = (("IMG_%04d.JPG", (6000, 4000)), ("DSC_%04d.JPG", (5472, 3648)), ("_MG_%04d.JPG", (8256, 5504)),
          ("IMG_%04d.JPG", (4032, 3024)))
WORDS = {"news": ("parliament", "court", "harbour", "council", "protest", "budget", "flood", "election", "rail",
                  "hospital", "airport", "school"),
         "sport": ("grand-final", "derby", "training", "wicket", "try", "goal", "finish-line", "crowd", "coach",
                   "stadium", "fans", "trophy"),
         "home": ("kitchen", "bathroom", "deck", "garden", "living-room", "facade", "pantry", "laundry", "bedroom",
                  "courtyard", "hallway", "veggie-patch"),
         "personal finance": ("coins", "calculator", "laptop", "couple", "house-keys", "receipt", "piggy-bank",
                              "chart", "wallet", "cards", "office", "family"),
         "travel": ("beach", "hotel-pool", "mountain", "lagoon", "old-town", "market", "cruise-ship", "lookout",
                    "rainforest", "vineyard", "island", "street"),
         "food": ("lamb-shanks", "pavlova", "banana-bread", "ramen", "roast-chicken", "salad", "lasagne", "curry",
                  "scones", "dumplings", "brownies", "frittata")}


def dam_export():
    """The DAM's export of each property's hero-image collection, one row per rendition. Live hero images are the
    heroes of the property's own pages (the page catalogue); retired ones left their pages before October. Assets
    uploaded before the cutover keep their library record beside the DAM record. A few distinct assets share a file
    name, pixel size and upload time (camera names in one batch upload). Returns the frame and, per property, the
    live hero images."""
    rows, live_n = [], {}
    for p in K.PROPERTIES:
        code, kind = p["code"], p["kind"]
        r = K.stream("dam", code)
        cat = W.catalogue(p)
        idx = np.flatnonzero(cat["hero"] == "own")
        n_live = len(idx)
        n_ret = int(round(n_live * (0.16 + 0.06 * r.random())))
        live_n[code] = n_live
        assets = []
        moved = W.MOVED.get(code)
        for j, k in enumerate(idx):
            pub = cat["pub"][k]
            up = dt.datetime.combine(pub - dt.timedelta(days=int(r.integers(0, 4))), dt.time()) + \
                dt.timedelta(seconds=int(r.integers(20000, 80000)))
            label = p["name"]
            if moved and cat["sec"][k] == moved[0] and pub < W.MOVE_DATE:
                label = K.BY_CODE[moved[1]]["name"]     # uploaded for the property the section came from
            assets.append(dict(up=up, last=K.LATEST_CRAWL, key=("live", j), label=label,
                               used="https://%s%s" % (p["origin"], cat["path"][k])))
        for j in range(n_ret):
            up = dt.datetime(2018, 1, 1) + dt.timedelta(seconds=int(r.integers(0, int((dt.datetime(2026, 7, 1) -
                                                                                        dt.datetime(2018, 1, 1))
                                                                                       .total_seconds()))))
            gone = up.date() + dt.timedelta(days=int(r.integers(30, 900)))
            gone = min(gone, dt.date(2026, 9, 30))
            secs = W.SECTIONS[kind]
            assets.append(dict(up=up, last=gone, key=("retired", j), label=p["name"],
                               used="https://%s/%s/%d" % (p["origin"], secs[int(r.integers(0, len(secs)))],
                                                          int(r.integers(100000, 1000000)))))
        for a in assets:
            if r.random() < 0.55:
                fmt, px = CAMERA[int(r.integers(0, len(CAMERA)))]
                a["name"], a["px"] = fmt % int(r.integers(1, 10000)), px
            else:
                words = WORDS[kind]
                a["name"] = "%s-%s-%02d.jpg" % (words[int(r.integers(0, len(words)))],
                                                words[int(r.integers(0, len(words)))], int(r.integers(1, 40)))
                a["px"] = ((2400, 1350), (2048, 1152), (3000, 2000), (2560, 1707))[int(r.integers(0, 4))]
        # a few distinct live assets share a camera name, pixel size and upload time with another (one batch)
        live = [a for a in assets if a["key"][0] == "live"]
        cam = [a for a in live if a["name"].upper().endswith(".JPG") and a["name"][:3] in ("IMG", "DSC", "_MG")]
        n_twin = int(round(len(live) * 0.025))
        pick = r.choice(len(cam), 2 * n_twin, replace=False)
        for i in range(n_twin):
            a, b = cam[pick[2 * i]], cam[pick[2 * i + 1]]
            b["name"], b["px"], b["up"] = a["name"], a["px"], a["up"]
        for a in assets:
            a["id"] = W._hexid("dam", code, *a["key"])[:12]
            a["lib"] = W._hexid("library", code, *a["key"])[:12] if a["up"].date() < K.DAM_CUTOVER else ""
        w_slot, h_slot = K.SLOT_SIZES[code]["hero"]
        for a in assets:
            ow, oh = a["px"]
            rends = (("original", ow, oh), ("large", 2048, int(round(2048 * oh / ow))), ("web", w_slot, h_slot))
            recs = [(a["id"], a["lib"])] + ([(a["lib"], "")] if a["lib"] else [])
            for aid, leg in recs:
                for rend, rw, rh in rends:
                    rows.append((aid, leg, a["label"], rend, a["name"], rw, rh, a["up"], a["last"], a["used"]))
    df = pd.DataFrame(rows, columns=["asset_id", "legacy_id", "property", "rendition", "file_name", "width_px",
                                     "height_px", "uploaded_utc", "last_used_on", "last_used_page"])
    df = df.sort_values(["property", "uploaded_utc", "asset_id", "rendition"], kind="mergesort").reset_index(drop=True)
    return df, live_n


def build():
    dam, live_n = dam_export()
    return dict(img=image_host_logs(), legacy=legacy_log(), dam=dam, dam_live=live_n)
