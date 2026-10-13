"""task129 generator: the image CDN's daily delivery log (both vendors, all clients)."""
from datetime import date

import numpy as np
import pandas as pd

POPS = {"CPH": 0.46, "AMS": 0.22, "FRA": 0.15, "ARN": 0.08, "OSL": 0.06, "HEL": 0.03}
FALLBACK = (date(2026, 6, 9), date(2026, 7, 21))
FALLBACK_SHARE = 0.40
from knobs_lab import IPV, KBPR, NATIVE_RPV, NATIVE_KB  # noqa: E402
MISS = {"smartphone": 0.071, "tablet": 0.083, "desktop": 0.064, "other": 0.41}
UA = {"smartphone": {"Chrome Mobile": 0.46, "Mobile Safari": 0.38, "Samsung Internet": 0.08,
                     "Sønderå app WebView": 0.08},
      "tablet": {"Mobile Safari": 0.62, "Chrome Mobile": 0.38},
      "desktop": {"Chrome": 0.58, "Safari": 0.17, "Edge": 0.16, "Firefox": 0.09},
      "other": {"bot": 1.0}}
# the group app's native screens (article lists, push images and galleries) fetch images with the
# platforms' own HTTP clients; the vendor classes them by device like any browser
NATIVE = {"CFNetwork": 0.44, "okhttp": 0.56}
NATIVE_MISS = 0.052


def _rows(rng, d, cls, req_total, kbpr, fams, miss, fb):
    rows = []
    for pop, ps in POPS.items():
        for ua, us in fams.items():
            n = req_total * ps * us * rng.uniform(0.97, 1.03)
            parts = [("primary", n * (1 - FALLBACK_SHARE)), ("fallback", n * FALLBACK_SHARE)] \
                if fb else [("primary", n)]
            for vendor, nn in parts:
                nreq = int(round(nn))
                fills = int(round(nreq * miss * rng.uniform(0.9, 1.1)))
                b = nreq * kbpr * rng.uniform(0.985, 1.015) * 1000
                out = int(round(b / 1000)) if vendor == "fallback" else int(round(b))
                rows.append((d.isoformat(), pop, vendor, cls, ua, nreq - fills, fills, out))
    return rows


def delivery_log(rng, phone_views_by_day):
    """phone_views_by_day: Series indexed by local date -> mobile page views (every phone view, once)."""
    rows = []
    for d, pv in phone_views_by_day.items():
        if d < date(2026, 2, 1):
            continue
        m = d.month
        vol = {"smartphone": pv * IPV[m] * rng.uniform(0.985, 1.015),
               "tablet": pv * 0.16 * IPV[m] * rng.uniform(0.95, 1.05),
               "desktop": pv * 0.52 * IPV[m] * 1.3 * rng.uniform(0.95, 1.05),
               "other": pv * 0.004 * IPV[m]}
        fb = FALLBACK[0] <= d <= FALLBACK[1]
        for cls, req in vol.items():
            kbpr = KBPR[m] * (1.35 if cls == "desktop" else 1.0) * (0.6 if cls == "other" else 1.0)
            rows += _rows(rng, d, cls, req, kbpr, UA[cls], MISS[cls], fb)
        nat = pv * NATIVE_RPV[m] * rng.uniform(0.96, 1.04)
        rows += _rows(rng, d, "smartphone", nat, KBPR[m] * NATIVE_KB, NATIVE, NATIVE_MISS, fb)
    df = pd.DataFrame(rows, columns=["log_date", "pop", "vendor", "device_class", "ua_family",
                                     "edge_hits", "origin_fills", "bytes_served"])
    return df.sort_values(["log_date", "pop", "vendor", "device_class", "ua_family"],
                          kind="stable").reset_index(drop=True)
