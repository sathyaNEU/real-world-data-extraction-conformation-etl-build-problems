"""The 2025 pilot's records: the voucher register the program office kept (one row per voucher, as paid) and the
three licensed dismantlers' invoice lines for towing and processing the surrendered vehicles."""
import datetime as dt
from functools import lru_cache

import numpy as np

import fleet as F
import world as W

DISMANTLERS = {"D-3317": ("Calderwick Auto Recyclers", "Dunmarsh"), "D-2864": ("Oakhaven Salvage & Parts", "Elkhollow"),
               "D-4021": ("Thistlebury Auto Salvage", "Larkhaven")}
SERVES = {"Dunmarsh": "D-3317", "Elkhollow": "D-2864", "Larkhaven": "D-4021", "Kinnard": "D-4021"}
PROCESS = 185
TOW = {0: 0, 1: 95, 2: 145, 3: 210}
# the dismantler whose billing system writes the invoice total on each line of the export
HEADER_ON_LINES = "D-2864"


@lru_cache(maxsize=None)
def vouchers():
    T = F.build()
    P = T[T["kind"] == "pilot"].sort_values("surrendered", kind="mergesort").reset_index(drop=True)
    rng = np.random.default_rng(W.SEED + 41)
    out = []
    for k, v in enumerate(P.itertuples(index=False)):
        s = v.surrendered
        lic = SERVES[v.county]
        if v.county == "Kinnard" and rng.random() < 0.35:
            lic = "D-3317"
        zone = int(rng.choice(4, p=[0.38, 0.32, 0.20, 0.10]))
        out.append(dict(voucher="VRP25-%05d" % (10 + k * 3 + int(rng.integers(0, 3))), county=v.county, vin=v.vin,
                        plate=v.plate, my=int(v.my), make=v.make, model=v.model, body=v.body,
                        applied=s - dt.timedelta(days=int(rng.integers(9, 45))), surrendered=s, licence=lic,
                        cert="CD25-%06d" % int(rng.integers(100000, 999999)),
                        paid=s + dt.timedelta(days=int(rng.integers(6, 26))), zone=zone, reinstated=bool(v.reinstated)))
    return out


VOUCHER_COLS = ["voucher_no", "applicant_county_no", "vin", "plate", "model_year", "make", "model", "body_code",
                "applied_on", "surrendered_on", "dismantler_licence", "certificate_no", "voucher_amount", "paid_on",
                "status"]


def voucher_rows():
    return [[v["voucher"], "%02d" % W.CNO[v["county"]], v["vin"], v["plate"], v["my"], v["make"], v["model"], v["body"],
             v["applied"], v["surrendered"], v["licence"], v["cert"], W.VOUCHER, v["paid"], "PAID"] for v in vouchers()]


INVOICE_COLS = ["invoice_no", "dismantler_licence", "dismantler", "invoice_date", "voucher_no", "vin", "service",
                "tow_zone", "amount"]


def charge(v):
    return PROCESS + TOW[v["zone"]]


@lru_cache(maxsize=None)
def invoices():
    """Two dismantlers bill every second Friday for the vehicles taken in over the fortnight before; Oakhaven bills
    each vehicle driven in on its own invoice and each day's tow run on one, and its billing export writes the
    invoice total on every line."""
    rng = np.random.default_rng(W.SEED + 43)
    rows = []
    n = 0
    for lic, (name, _) in sorted(DISMANTLERS.items()):
        vs = [v for v in vouchers() if v["licence"] == lic]
        if lic == HEADER_ON_LINES:
            groups = []
            for d in sorted({v["surrendered"] for v in vs}):
                day = [v for v in vs if v["surrendered"] == d]
                bill = d + dt.timedelta(days=int(rng.integers(1, 4)))
                groups += [(bill, [v]) for v in day if v["zone"] == 0]
                towed = [v for v in day if v["zone"]]
                if towed:
                    groups.append((bill, towed))
        else:
            groups = []
            d = dt.date(2025, 6, 13)
            while d <= dt.date(2026, 1, 9):
                groups.append((d, [v for v in vs if d - dt.timedelta(days=14) < v["surrendered"] <= d]))
                d += dt.timedelta(days=14)
        for d, batch in groups:
            if not batch:
                continue
            n += 1
            inv = "%s-%04d" % (lic.replace("-", ""), 100 + n * 7 + int(rng.integers(0, 7)))
            total = sum(charge(v) for v in batch)
            for v in batch:
                amt = total if lic == HEADER_ON_LINES else charge(v)
                rows.append([inv, lic, name, d.isoformat(), v["voucher"], v["vin"],
                             "TOW+PROCESS" if v["zone"] else "PROCESS", v["zone"], "%.2f" % amt])
    return rows


def truth():
    """What the pilot retired, county by county: the vehicles whose titles stayed cancelled, the charges paid for
    them, and their vins (for the NOx they would have emitted)."""
    out = {}
    for c in W.PILOT_COUNTIES:
        vs = [v for v in vouchers() if v["county"] == c and not v["reinstated"]]
        out[c] = dict(n=len(vs), charges=sum(charge(v) for v in vs), vins=[v["vin"] for v in vs])
    return out
