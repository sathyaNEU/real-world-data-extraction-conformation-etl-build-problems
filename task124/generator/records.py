"""Turn the world and the ask frames into the rows the district's systems export, and write the CSV files.

GIS service line inventory (8 January 2027), the verification history as the work management system holds it
(customer-system service orders before the 13 March 2023 cut-over keyed by premise number, work orders after keyed by
service line id), the migration crosswalk, the result code list, the 2026 completions export, the contracts list, the
access agreements and the two neighbouring extracts."""
from __future__ import annotations

import csv
import datetime as dt

import numpy as np
import pandas as pd

import asks as A
import common as K

MUNI = {z[0]: z[2] for z in K.ZONES}

# result codes as each recording route writes them: (route, material) -> code
CODEBOOK = {
    "CIS": {"LEAD": "LEAD", "GALV-R": "GALV-R", "COPPER": "COPPER", "PLASTIC": "PLASTIC", "GALV-N": "GALV-N"},
    "WMS district": {"LEAD": "L", "GALV-R": "GRR", "COPPER": "C", "PLASTIC": "P", "GALV-N": "GN"},
    "WMS contractor": {"LEAD": "PB", "GALV-R": "FE-R", "COPPER": "CU", "PLASTIC": "PE", "GALV-N": "FE-N"},
}
MATERIAL_TEXT = {"LEAD": "Lead", "GALV-R": "Galvanized, downstream of lead now or in the past",
                 "COPPER": "Copper", "PLASTIC": "Plastic (PE, PEX or PVC)",
                 "GALV-N": "Galvanized, never downstream of lead"}
CLASS_OF = {"LEAD": "LEAD", "GALV-R": "GRR", "COPPER": "NON-LEAD", "PLASTIC": "NON-LEAD", "GALV-N": "NON-LEAD"}
NONLEAD_MIX = {0: (("COPPER", 0.88), ("GALV-N", 0.07), ("PLASTIC", 0.05)),
               1: (("COPPER", 0.85), ("GALV-N", 0.08), ("PLASTIC", 0.07)),
               2: (("COPPER", 0.80), ("PLASTIC", 0.18), ("GALV-N", 0.02)),
               3: (("COPPER", 0.70), ("PLASTIC", 0.30))}


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def iso(d):
    return d.isoformat() if isinstance(d, dt.date) else ""


# ------------------------------------------------------------------------------------------------ inventory
INV_COLS = ["sl_id", "service_address", "municipality", "zone", "main_segment", "year_built", "tap_card_material",
            "sl_class", "class_basis", "field_verified_on", "replaced_on"]


def assessor_year(ln) -> int:
    """The assessor carries no residential year built on most non-residential parcels; it exports 0."""
    if ln.record and ln.era in (0, 1, 2) and K.stream("assessor", ln.sl_id).random() < 0.012:
        return 0
    return int(ln.year_built)


def inventory(lines: pd.DataFrame, ev: pd.DataFrame) -> pd.DataFrame:
    last = ev.groupby("sl_id").date.max()
    rows = []
    for ln in lines.sort_values("sl_id").itertuples():
        rows.append((ln.sl_id, ln.address, MUNI[ln.zone], ln.zone, ln.segment, assessor_year(ln), ln.record,
                     ln.cls, ln.basis, iso(last.get(ln.sl_id)), iso(ln.replaced)))
    return pd.DataFrame(rows, columns=INV_COLS)


# ------------------------------------------------------------------------------------------ verification log
VER_COLS = ["source", "wo_no", "verified_date", "premise_no", "sl_id", "method", "crew", "result_code"]


def material_found(ln, sl_id: str, k: int) -> str:
    """The material a crew records: what is in the ground, a non-lead line read as copper, plastic or galvanized
    never downstream of lead (the same reading on every visit)."""
    if ln.truth == "LEAD":
        return "LEAD"
    if ln.truth == "GRR":
        return "GALV-R"
    if ln.record == "COPPER":
        return "COPPER"
    if ln.record == "PLASTIC":
        return "PLASTIC"
    r = K.stream("nonlead-material", sl_id)
    mats, ps = zip(*NONLEAD_MIX[max(ln.era, 0)])
    return str(r.choice(mats, p=np.array(ps) / sum(ps)))


def verifications(ev: pd.DataFrame, lines: pd.DataFrame) -> pd.DataFrame:
    by = lines.set_index("sl_id")
    ev = ev.sort_values(["date", "sl_id", "cause"]).reset_index(drop=True)
    r = K.stream("work-order-numbers")
    so, wo = 2_100_400, {}
    rows = []
    for e in ev.itertuples():
        ln = by.loc[e.sl_id]
        mat = material_found(ln, e.sl_id, 0)
        if e.date < K.MIGRATION:
            so += int(r.integers(2, 9))
            route = "CIS"
            rows.append(("CIS", "SO%07d" % so, e.date.strftime("%m/%d/%Y"), str(int(ln.legacy_premise)), "",
                         e.method, e.crew, CODEBOOK[route][mat]))
        else:
            y = e.date.year % 100
            wo[y] = wo.get(y, 1_200 if y == 23 else 400) + int(r.integers(2, 9))
            route = "WMS contractor" if e.crew in K.CREW_CONTRACT else "WMS district"
            rows.append(("WMS", "WO-%02d-%06d" % (y, wo[y]), e.date.isoformat(), "", e.sl_id, e.method, e.crew,
                         CODEBOOK[route][mat]))
    return pd.DataFrame(rows, columns=VER_COLS)


def codes() -> list:
    routes = [("CIS", "Customer system service orders, to 12 March 2023 (all crews)"),
              ("WMS district", "Work management system, district crews (SLV), from 13 March 2023"),
              ("WMS contractor", "Work management system, contractor field forms, from 13 March 2023")]
    out = []
    for key, text in routes:
        for mat in ("LEAD", "GALV-R", "COPPER", "PLASTIC", "GALV-N"):
            out.append((CODEBOOK[key][mat], text, MATERIAL_TEXT[mat], CLASS_OF[mat]))
    return out


# ------------------------------------------------------------------------------------------------- crosswalk
def crosswalk(lines: pd.DataFrame) -> list:
    t = lines[lines.legacy_premise.notna()].copy()
    t["legacy"] = t.legacy_premise.astype(int)
    out = []
    for ln in t.sort_values("legacy").itertuples():
        u = K.stream("xwalk", ln.sl_id).random()
        method = "ADDRESS" if u < 0.81 else ("METER" if u < 0.97 else "FIELD")
        out.append(("%08d" % ln.legacy, ln.sl_id, method, K.MIGRATION.isoformat()))
    return out


# ----------------------------------------------------------------------------------- ask A: completions export
COMP_COLS = ["wo_no", "site_id", "site_address", "contract_no", "vendor_no", "vendor_name", "work_type",
             "completed_utc", "closed_on", "row_status", "service_length_ft", "restoration_type", "paid_base",
             "paid_extra_ft", "paid_restoration", "co_no", "co_amount"]
VENDOR_NAME = {"V-10482": "BRANNIGAN EXCAVATING INC", "V-20877": "TRI-COUNTY UNDERGROUND INC",
               "V-31560": "TRI-COUNTY UNDERGROUND LLC", "V-11935": "KESTREL PIPE AND UTILITY CO"}


def vendor_of(contract: str, local_day: dt.date) -> str:
    c = [x for x in K.CONTRACTS_2026 if x[0] == contract][0]
    if len(c[2]) == 1:
        return c[2][0]
    return c[2][0] if local_day < K.TC_SWITCH else c[2][1]


def utc_stamp(day: dt.date, minute: int) -> str:
    t = dt.datetime.combine(day, dt.time(minute // 60, minute % 60)) + dt.timedelta(hours=K.utc_offset_hours(day))
    return t.strftime("%Y-%m-%dT%H:%M:00Z")


def completions(st: pd.DataFrame, co: pd.DataFrame, ev: pd.DataFrame, lines: pd.DataFrame) -> pd.DataFrame:
    first = ev.groupby("sl_id").date.min()
    addr = lines.set_index("sl_id").address
    co_amt = dict(zip(co.co_no, co.amount))
    order = st.assign(found=st.sl_id.map(first)).sort_values(["found", "sl_id"])
    r = K.stream("completion-wo")
    seq, nos = {}, {}
    for s in order.itertuples():
        y = s.found.year % 100
        seq[y] = seq.get(y, 3_000) + int(r.integers(3, 40))
        nos[s.sl_id] = "WO-%02d-%06d" % (y, seq[y])
    rows = []
    for s in st.itertuples():
        base = [nos[s.sl_id], s.sl_id, addr[s.sl_id], s.contract, vendor_of(s.contract, s.date),
                VENDOR_NAME[vendor_of(s.contract, s.date)], "FULL LSL REPLACEMENT", utc_stamp(s.date, s.minute)]
        tail = [s.length, s.surface, "%.2f" % s.paid_base, "%.2f" % s.paid_extra_ft]
        co_cols = [s.co_no, "%.2f" % co_amt[s.co_no]] if s.co_no else ["", ""]
        rows.append(base + [s.date.isoformat(), "CLOSED"] + tail + ["%.2f" % s.paid_restoration] + co_cols)
        if not np.isnan(s.reclosed_restoration):
            rows.append(base + [(s.date + dt.timedelta(days=int(s.reclosed_days))).isoformat(), "RECLOSED"] + tail +
                        ["%.2f" % s.reclosed_restoration] + co_cols)
    df = pd.DataFrame(rows, columns=COMP_COLS)
    return df.sort_values(["wo_no", "closed_on"], kind="stable").reset_index(drop=True)


CONTRACT_COLS = ["contract_no", "contractor", "vendor_no", "vendor_name", "vendor_from", "vendor_to", "awarded_on",
                 "zones", "bid_price_full_replacement", "extra_length_rate_per_ft_over_50", "not_to_exceed"]


def contracts() -> list:
    out = []
    award = {"2026-LSL-01": "2025-12-09", "2026-LSL-02": "2025-12-09", "2026-LSL-03": "2025-12-16"}
    nte = {"2026-LSL-01": "8,450,000.00", "2026-LSL-02": "4,050,000.00", "2026-LSL-03": "4,300,000.00"}
    for no, name, vendors, zones, price, rate in K.CONTRACTS_2026:
        for k, v in enumerate(vendors):
            frm = "2026-01-01" if k == 0 else K.TC_SWITCH.isoformat()
            to = "" if k == len(vendors) - 1 else (K.TC_SWITCH - dt.timedelta(days=1)).isoformat()
            out.append((no, name, v, VENDOR_NAME[v], frm, to, award[no], " ".join(zones), "%.2f" % price,
                        "%.2f" % rate, nte[no]))
    return out


# ------------------------------------------------------------------------------------- ask B: access agreements
AG_COLS = ["agreement_no", "signed_on", "channel", "premise_no", "sl_id", "zone_on_form", "status", "status_date"]


def agreements(ag: pd.DataFrame) -> list:
    """The agreement system's open file: the forms it holds (a portal form its import refused is not among them)."""
    return [(a.agreement_no, a.signed_on.isoformat(), a.channel, a.premise_no, a.form_sl_id, a.zone_on_form,
             a.status, a.status_date.isoformat()) for a in ag.itertuples() if a.imported]


OUTREACH_COLS = ["sl_id", "zone", "letter_1_mailed", "portal_invite_sent", "portal_status", "portal_status_date"]


def outreach(tr: pd.DataFrame) -> list:
    return [(t.sl_id, t.zone, t.letter_1_mailed.isoformat(), t.portal_invite_sent.isoformat(), t.portal_status,
             t.portal_status_date.isoformat()) for t in tr.sort_values("sl_id").itertuples()]


# ------------------------------------------------------------------------------------------------ distractors
TAP_COLS = ["sample_id", "sl_id", "monitoring_period", "collected_on", "site_tier", "first_draw_lead_ugL",
            "fifth_liter_lead_ugL", "copper_mgL", "lab_sample_no"]


def tap_samples(lines: pd.DataFrame) -> list:
    """Lead and copper compliance monitoring at the tier 1 sites (lines known to be lead), 2025 and 2026."""
    r = K.stream("tap-sites")
    pool = sorted(lines[(lines.cls == "LEAD") & lines.zone.isin(K.PLAN_ORDER)].sl_id)
    sites = sorted(r.choice(pool, size=96, replace=False))
    out, n = [], 0
    periods = [("2025-H1", dt.date(2025, 1, 6), dt.date(2025, 6, 27)), ("2025-H2", dt.date(2025, 7, 7),
               dt.date(2025, 12, 12)), ("2026-H1", dt.date(2026, 1, 5), dt.date(2026, 6, 26)),
               ("2026-H2", dt.date(2026, 7, 6), dt.date(2026, 12, 11))]
    for name, lo, hi in periods:
        rr = K.stream("tap", name)
        for sl in sites:
            if rr.random() < 0.06:
                continue
            d = lo + dt.timedelta(days=int(rr.integers(0, (hi - lo).days + 1)))
            while d.weekday() >= 5:
                d -= dt.timedelta(days=1)
            n += 1
            first = rr.lognormal(np.log(3.6), 0.85)
            fifth = first * rr.lognormal(np.log(1.9), 0.45)
            out.append(("TS-%s-%04d" % (name, n), sl, name, d.isoformat(), 1, "%.1f" % first, "%.1f" % fifth,
                        "%.3f" % rr.lognormal(np.log(0.21), 0.5), "L%d-%05d" % (d.year % 100, 20_000 + 3 * n)))
    return sorted(out, key=lambda x: (x[3], x[0]))


METER_COLS = ["exchange_id", "sl_id", "exchanged_on", "old_meter_no", "new_meter_no", "meter_size_in",
              "setter_condition", "crew"]


def meter_exchanges(lines: pd.DataFrame) -> list:
    """The automated metering rollout, 2023 to 2025, in the plan zones and the two newer zones."""
    out, n = [], 0
    for ln in lines.sort_values("sl_id").itertuples():
        r = K.stream("meter", ln.sl_id)
        if r.random() >= 0.36 or ln.year_built > 2022:
            continue
        lo = dt.date(2023, 4, 3)
        d = lo + dt.timedelta(days=int(r.integers(0, (dt.date(2025, 12, 19) - lo).days + 1)))
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
        n += 1
        size = str(r.choice(["5/8", "3/4", "1"], p=[0.86, 0.11, 0.03]))
        cond = str(r.choice(["GOOD", "REPLACED SETTER", "BYPASS REMOVED", "FROZEN VALVE"],
                            p=[0.88, 0.07, 0.03, 0.02]))
        out.append(("MX%06d" % (n * 7 + 100_000), ln.sl_id, d.isoformat(), "%08d" % (40_000_000 + int(r.integers(0, 9_000_000))),
                    "H%09d" % (310_000_000 + int(r.integers(0, 90_000_000))), size, cond,
                    "MTR%d" % int(r.integers(1, 5))))
    return sorted(out, key=lambda x: (x[2], x[0]))
