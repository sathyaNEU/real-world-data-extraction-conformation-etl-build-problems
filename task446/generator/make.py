"""Cut the task446 pack into target/. Deterministic: run twice, byte-identical."""
import csv
import datetime as dt
import io
import math
import os
import sys

import numpy as np

import world
import truth
from world import QE, D
import docs
import tune

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
EXPORT_TS = dt.datetime(2026, 10, 9, 18, 42, 0)

LIMITS_AGENDA = {"X": 170.0, "W": 85.0, "A": 100.0, "B": 90.0, "C": 85.0, "D": 30.0}
REQUESTS = {  # group: (borrower key, facility type, amount GBP m, tenor, purpose)
    "X": ("X1", "Term loan", 30.0, "5 years", "acquisition of a contract-catering business (completion 27 November 2026)"),
    "W": ("W1", "Term loan", 12.0, "4 years", "new corrugator line, Gateshead"),
    "A": ("A1", "Term loan", 20.0, "3 years", "working capital for the Coventry gearbox programme"),
    "B": ("B1", "Revolving credit facility", 25.0, "3 years", "fleet replacement, 2027 to 2028"),
    "C": ("C2", "Term loan", 14.0, "5 years", "chilled distribution centre, Wakefield"),
    "D": ("D2", "Revolving credit facility", 20.0, "2 years", "general corporate purposes, seed capital for new funds"),
}


def wcsv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, delimiter=delimiter, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def fmt_money(x):
    return "%.2f" % x


def bank_name_variant(rng, name):
    r = rng.random()
    n = name
    if r < 0.35:
        n = n.upper()
    elif r < 0.5:
        n = n.replace(" Ltd", " Limited").replace(" plc", " PLC")
    elif r < 0.6:
        n = n.replace(" Ltd", " LTD")
    if rng.random() < 0.04:
        n = n + " "
    return n


def rm_codes(w):
    """The customer master's relationship-management group code at each quarter-end: the code of the
    group as RM coverage records it then (managed funds sit under their manager's code, overseas
    branches under a separate branch-desk code)."""
    rng = np.random.default_rng(world.SEED + 7)
    code_of_top = {}
    def code(top):
        if top not in code_of_top:
            code_of_top[top] = "RMG%05d" % int(rng.integers(10000, 99999))
        return code_of_top[top]
    out = {}
    for t, d in enumerate(QE):
        R = truth.Resolver(w, d, follow_funds=True, branches=False)
        for f in w.fac:
            if f.limit[t] is None:
                continue
            top = R.top(f.lei)
            if w.ent[f.lei]["category"] == "BRANCH":
                out[(f.lei, t)] = "BRD%05d" % (int(f.lei[-6:-2], 36) % 100000)
            else:
                out[(f.lei, t)] = code(top)
    return out


def build(target=TARGET):
    os.makedirs(target, exist_ok=True)
    for fn in os.listdir(target):
        os.remove(os.path.join(target, fn))
    w = world.full_world()
    tune.tune(w, LIMITS_AGENDA, REQUESTS)
    rng = np.random.default_rng(world.SEED + 1)
    rm = rm_codes(w)
    # ---------------- loan book extracts (one file, five quarter-end extracts)
    blank_lei = set()
    for f in w.fac:
        if f.lei not in w.agenda_leis and rng.random() < 0.025:
            blank_lei.add(f.lei)
    names = {}
    rows = []
    for t, d in enumerate(QE):
        for f in sorted(w.fac, key=lambda x: (w.customer_id[x.lei], x.ref)):
            if f.limit[t] is None:
                continue
            key = (f.lei, t // 2)
            if key not in names:
                names[key] = bank_name_variant(rng, w.ent[f.lei]["name"])
            lim = f.limit[t] * 1e6
            dr = f.drawn[t]
            rows.append([d.isoformat(), f.ref, f.booking[t], w.customer_id[f.lei],
                         "" if f.lei in blank_lei else f.lei, names[key], rm[(f.lei, t)],
                         {"TERM": "TERM", "RCF": "RCF", "OVD": "OVD"}[f.ftype],
                         "N" if f.ftype == "OVD" else "Y", f.ccy, fmt_money(lim), fmt_money(dr),
                         fmt_money(max(0.0, lim - dr)), f.start.isoformat(), f.maturity.isoformat(),
                         f.migrated_from or "", w.ent[f.lei]["sector"] or ""])
    hdr = ["extract_date", "facility_ref", "booking_entity", "customer_id", "customer_lei", "customer_name",
          "rm_group_code", "facility_type", "committed", "currency", "facility_limit", "drawn_balance",
          "undrawn_balance", "start_date", "maturity_date", "migrated_from", "sic_division"]
    late = [r for r in rows if r[0] == "2025-12-31" and r[2] == "CWB-DUB"]
    main = [r for r in rows if not (r[0] == "2025-12-31" and r[2] == "CWB-DUB")]
    wcsv(os.path.join(target, "loan_book_qe_extracts.csv"), hdr, main)
    wcsv(os.path.join(target, "loan_book_cwb_dub_20251231_late.csv"), hdr, late)

    # ---------------- investment securities
    rows = []
    for t, d in enumerate(QE):
        for s in sorted(w.sec, key=lambda x: x["isin"]):
            if s["cv"][t] is None:
                continue
            nm = w.ent[s["lei"]]["name"].upper().replace(" LIMITED", "").replace(" LTD", "").replace(" PLC", "")
            desc = "%s %.3f%% %s" % (nm[:22], s["coupon"], s["maturity"].strftime("%d/%m/%y"))
            lei_out = "" if (s["blank_from"] is not None and t >= s["blank_from"]) else s["lei"]
            rows.append([d.strftime("%d/%m/%Y"), "FVOCI" if (int(s["isin"][-3:-1], 36) % 3) else "AMC",
                         s["isin"], desc, lei_out, nm, s["ccy"], "%.0f" % (s["nominal"] * 1e6),
                         fmt_money(s["cv"][t])])
    wcsv(os.path.join(target, "treasury_investment_positions_qe.csv"),
         ["position_date", "ifrs9_category", "isin", "security_description", "issuer_lei", "issuer_short_name",
          "currency", "nominal", "carrying_value"], rows)

    # ---------------- derivatives (xlsx, one sheet per quarter-end, GBP thousands)
    docs.derivatives_workbook(w, os.path.join(target, "ccr_netting_set_exposure_qe.xlsx"))
    # ---------------- CSA collateral
    rows = []
    for t, d in enumerate(QE):
        for n in sorted(w.drv, key=lambda x: x["ns"]):
            if n["csa"] is None:
                continue
            rows.append([n["csa"], d.strftime("%d-%b-%Y").upper(), "CASH", n["coll_ccy"], fmt_money(n["coll"][t])])
            if int(n["ns"][-2:]) % 4 == 0 or n["lei"] == w.B["BP"]:
                rows.append([n["csa"], d.strftime("%d-%b-%Y").upper(), "UK GILT", "GBP",
                             fmt_money(round(float(np.random.default_rng(int(n["ns"][3:]) + t).uniform(2e5, 2e6)), -3))])
    wcsv(os.path.join(target, "csa_collateral_held_qe.csv"),
         ["csa_reference", "valuation_date", "collateral_type", "currency", "amount_held"], rows)
    # ---------------- FX
    rows = []
    for t, d in enumerate(QE):
        for c in ("EUR", "USD", "CHF", "SEK"):
            v = truth.FX.get(c, None)
            val = v[t] if v else {"CHF": [1.0712, 1.0688, 1.0745, 1.0731, 1.0679], "SEK": [12.6631, 12.7458, 12.5917, 12.7752, 12.6119]}[c][t]
            rows.append([d.isoformat(), "GBP", c, "%.4f" % val])
    wcsv(os.path.join(target, "treasury_fx_closing_rates.csv"), ["rate_date", "base_currency", "quote_currency", "rate"], rows)

    # ---------------- GLEIF archive: level 1 and level 2, reporting exceptions, ISIN map
    l1, rr = gleif_archive(w)
    wcsv(os.path.join(target, "gleif_lei_records_qe_archive.csv"), l1[0], l1[1])
    wcsv(os.path.join(target, "gleif_relationship_records_qe_archive.csv"), rr[0], rr[1])
    rows = []
    for (lei, cat, reason) in sorted(set(w.repex)):
        rows.append([lei, cat, reason, ""])
    wcsv(os.path.join(target, "gleif_reporting_exceptions_20260930.csv"),
         ["LEI", "ExceptionCategory", "ExceptionReason", "ExceptionReference"], rows)
    rows = [[s["lei"], s["isin"]] for s in w.sec]
    filler_rng = np.random.default_rng(world.SEED + 3)
    leis = sorted(w.ent)
    for i in range(4300):
        lei = leis[int(filler_rng.integers(0, len(leis)))]
        rows.append([lei, world.make_isin(filler_rng, "GB" if filler_rng.random() < 0.6 else "XS", w.used_isin)])
    rows.sort()
    wcsv(os.path.join(target, "isin_lei_20260930.csv"), ["LEI", "ISIN"], rows)

    # ---------------- house limit register, agenda, ratings, sector report, documents
    limits = house_limits(w)
    docs.limits_workbook(w, limits, os.path.join(target, "house_limit_register_20260930.xlsx"))
    docs.agenda_docx(w, REQUESTS, os.path.join(target, "credit_committee_agenda_20261104.docx"))
    docs.policy_pdf(os.path.join(target, "credit_concentration_policy.pdf"))
    docs.lms_pdf(os.path.join(target, "limit_monitoring_standard_LMS-03.pdf"))
    docs.field_reference(os.path.join(target, "crdm_field_reference.md"))
    ratings(w, os.path.join(target, "obligor_ratings_qe.csv"))
    docs.sector_report(w, os.path.join(target, "sector_concentration_2026Q3.xlsx"))
    docs.extract_log(target, os.path.join(target, "crdm_extract_log_20261009.txt"))
    # timestamps
    ts = EXPORT_TS.timestamp()
    for fn in sorted(os.listdir(target)):
        os.utime(os.path.join(target, fn), (ts, ts))
    return w, limits


def gleif_archive(w):
    rng = np.random.default_rng(world.SEED + 5)
    h1 = ["archive_date", "LEI", "Entity.LegalName", "Entity.LegalAddress.Country", "Entity.LegalJurisdiction",
          "Entity.EntityCategory", "Entity.EntityStatus", "Entity.SuccessorEntity.SuccessorLEI",
          "Registration.InitialRegistrationDate", "Registration.LastUpdateDate", "Registration.RegistrationStatus",
          "Registration.NextRenewalDate", "Registration.ManagingLOU"]
    rows1 = []
    upd = {l: int(rng.integers(0, 330)) for l in w.ent}
    for d in world.ARCHIVE_DATES:
        for lei in sorted(w.ent):
            e = w.ent[lei]
            if e["initial"] > d:
                continue
            status, est, succ = "ISSUED", "ACTIVE", ""
            # renewal cycle: anniversary of initial registration
            years = (d - e["initial"]).days // 365
            next_ren = dt.date(e["initial"].year + years + 1, e["initial"].month, min(e["initial"].day, 28))
            last_upd = min(d, e["initial"] + dt.timedelta(days=365 * years + upd[lei] % 200))
            if e["merged_on"] is not None and e["merged_on"] <= d:
                status, est, succ = "MERGED", "INACTIVE", e["successor"]
                last_upd = min(d, e["merged_on"] + dt.timedelta(days=9))
            elif e["lapse_from"] is not None and e["lapse_from"] <= d:
                status = "LAPSED"
                next_ren = e["lapse_from"]
                last_upd = e["lapse_from"] - dt.timedelta(days=int(upd[lei] % 300) + 30)
            jur = e["country"]
            rows1.append([d.isoformat(), lei, e["name"], e["country"], jur, e["category"], est, succ,
                          e["initial"].isoformat() + "T00:00:00Z", last_upd.isoformat() + "T09:%02d:00Z" % (upd[lei] % 60),
                          status, next_ren.isoformat() + "T00:00:00Z", e["lou"]])
    h2 = ["archive_date", "Relationship.StartNode.NodeID", "Relationship.StartNode.NodeIDType",
          "Relationship.EndNode.NodeID", "Relationship.EndNode.NodeIDType", "Relationship.RelationshipType",
          "Relationship.RelationshipStatus", "Relationship.Period.1.startDate", "Relationship.Period.1.endDate",
          "Relationship.Period.1.periodType", "Registration.InitialRegistrationDate", "Registration.LastUpdateDate",
          "Registration.RegistrationStatus", "Registration.NextRenewalDate", "Registration.ManagingLOU",
          "Registration.ValidationSources"]
    rows2 = []
    vs = ["FULLY_CORROBORATED", "FULLY_CORROBORATED", "PARTIALLY_CORROBORATED", "ENTITY_SUPPLIED_ONLY"]
    for d in world.ARCHIVE_DATES:
        for i, r in sorted(enumerate(w.rel), key=lambda x: (x[1]["child"], x[1]["type"], x[1]["start"])):
            if r["reg"] > d:
                continue
            if w.ent[r["child"]]["initial"] > d:
                continue
            ended = r["end"] is not None and r["end"] <= d
            status = "INACTIVE" if ended else "ACTIVE"
            regst = "PUBLISHED"
            years = (d - r["reg"]).days // 365
            nr = dt.date(r["reg"].year + years + 1, r["reg"].month, min(r["reg"].day, 28))
            lu = min(d, r["reg"] + dt.timedelta(days=365 * years + (i * 37) % 200))
            if r["lapsed_from"] is not None and r["lapsed_from"] <= d:
                regst = "LAPSED"
                nr = r["lapsed_from"]
                lu = r["lapsed_from"] - dt.timedelta(days=60 + (i * 13) % 200)
            if ended:
                lu = r["end"] + dt.timedelta(days=12 + i % 20)
                lu = min(lu, d)
            rows2.append([d.isoformat(), r["child"], "LEI", r["parent"], "LEI", r["type"], status,
                          r["start"].isoformat() + "T00:00:00Z", (r["end"].isoformat() + "T00:00:00Z") if ended else "",
                          "RELATIONSHIP_PERIOD", r["reg"].isoformat() + "T00:00:00Z",
                          lu.isoformat() + "T10:%02d:00Z" % (i % 60), regst, nr.isoformat() + "T00:00:00Z",
                          w.ent[r["child"]]["lou"], vs[i % 4]])
    return (h1, rows1), (h2, rows2)


def house_limits(w):
    """House limit register: one limit per obligor group (policy groups at 30 September 2026)."""
    rng = np.random.default_rng(world.SEED + 9)
    R = truth.Resolver(w, world.PROJ_DATE)
    ge = truth.group_exposures(w, lambda lei, t: R.top(lei), 4)
    lim = {}
    tops_agenda = {w.groups[k]["top"]: k for k in LIMITS_AGENDA}
    for top, parts in ge.items():
        e = sum(parts.values()) / 1e6
        if top in tops_agenda:
            lim[top] = LIMITS_AGENDA[tops_agenda[top]]
            continue
        if e < 0.25:
            continue
        head = e * float(rng.uniform(1.15, 1.9))
        step = 5.0 if head > 20 else 1.0
        lim[top] = max(step, math.ceil(head / step) * step)
    return lim


def ratings(w, path):
    rng = np.random.default_rng(world.SEED + 11)
    rows = []
    custs = sorted({f.lei for f in w.fac})
    base = {l: int(rng.integers(2, 9)) for l in custs}
    for t, d in enumerate(QE):
        for l in custs:
            if rng.random() < 0.06:
                base[l] = int(min(10, max(1, base[l] + rng.choice([-1, 1]))))
            rows.append([d.isoformat(), w.customer_id[l], "CW%d" % base[l],
                         {1: "0.03", 2: "0.05", 3: "0.10", 4: "0.20", 5: "0.40", 6: "0.80", 7: "1.60", 8: "3.20",
                          9: "6.40", 10: "15.00"}[base[l]], "MRS-2"])
    wcsv(path, ["rating_date", "customer_id", "grade", "grade_pd_pct", "model"], rows)


if __name__ == "__main__":
    build()
    print("built", len(os.listdir(TARGET)), "files")
