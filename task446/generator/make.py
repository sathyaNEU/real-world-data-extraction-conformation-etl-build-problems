"""Write task446's evidence pack (architecture 2) to target/. Deterministic: two runs are byte-identical.

    python3 task446/generator/make.py [target_dir]
"""
import csv
import datetime as dt
import io
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world                                   # noqa: E402
from world import D, COHORTS, EXTRACT_DATE, FX  # noqa: E402
import docs                                    # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
FILES = dict(
    signals="ews_entity_signals_2022-09_to_2026-09.csv",
    lei="gleif_lei_cdf_20260930.csv",
    rr="gleif_rr_cdf_20260930.csv",
    repex="gleif_repex_20260930.csv",
    obligors="credit_obligor_master_20260930.csv",
    register="credit_group_register_20260930.xlsx",
    watchlist="watch_list_history_2020-01_to_2026-09.csv",
    facilities="facility_obligor_extract_20260930.csv",
    limits="facility_limit_history_20261008.csv",
    fx="treasury_closing_rates_20260930.csv",
    triggers="ews_trigger_codes.csv",
    standard="early_warning_and_watch_list_standard.pdf",
    agenda="exec_risk_committee_agenda_2026-11-04.docx",
    fieldref="credit_data_field_reference.md",
    log="reference_data_extract_log_20261008.txt",
    ratings="internal_rating_master_scale_2026.xlsx",
    outlook="group_economics_uk_outlook_oct2026.xlsx",
)
DISTRACTORS = [FILES["ratings"], FILES["outlook"]]


def wcsv(path, header, rows):
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\r\n")
    wr.writerow(header)
    for r in rows:
        wr.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def iso(d):
    return d.isoformat() if d else ""


def ts(d, rng, lo_h=7, hi_h=19):
    t = dt.datetime(d.year, d.month, d.day, int(rng.integers(lo_h, hi_h)), int(rng.integers(0, 60)),
                    int(rng.integers(0, 60)))
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def feed_of(trig):
    if not trig:
        return "COMPOSITE"
    first = trig.split(";")[0]
    if first.startswith("PAY"):
        return "BUREAU"
    if first.startswith("RATING"):
        return "RATINGS"
    if first in ("FILING_LATE", "DIRECTOR_CHANGE", "WINDING_UP_PETITION", "CCJ", "GOING_CONCERN"):
        return "REGISTRY"
    if first.startswith("COVENANT"):
        return "INTERNAL"
    return "NEWS"


def entity_key(e):
    if e.lei:
        return e.lei.lower() if e.lower_key else e.lei
    return "CRN:" + e.crn


def build(target=TARGET, devices=True):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    w = world.build(devices=devices)

    # ---------------------------------------------------------------- signals (spine)
    rows = []
    for m, e, colour, score, trig in w.signals:
        rows.append((m.isoformat(), entity_key(e), e.vendor_name, e.country, colour, score, trig,
                     feed_of(trig), "3.2"))
    rows.sort(key=lambda r: (r[0], r[1].upper()))
    wcsv(os.path.join(target, FILES["signals"]),
         ["publication_date", "entity_key", "entity_name", "country", "signal", "score", "trigger_codes", "feed",
          "engine_release"], rows)

    # ---------------------------------------------------------------- GLEIF level 1
    ents = [w.ents[k] for k in sorted(w.ents)]
    rng = np.random.default_rng(world.SEED + 7)
    l1 = []
    for e in ents:
        if not e.lei:
            continue
        g = w.groups[e.gid]
        last = min(EXTRACT_DATE - dt.timedelta(days=int(rng.integers(3, 330))), EXTRACT_DATE)
        if e.reg_status == "LAPSED":
            nxt = EXTRACT_DATE - dt.timedelta(days=int(rng.integers(30, 700)))
            last = min(last, nxt - dt.timedelta(days=int(rng.integers(5, 300))))
        elif e.reg_status == "RETIRED":
            nxt = e.merged_on + dt.timedelta(days=int(rng.integers(40, 200)))
            last = min(EXTRACT_DATE, e.merged_on + dt.timedelta(days=int(rng.integers(10, 60))))
        else:
            nxt = EXTRACT_DATE + dt.timedelta(days=int(rng.integers(5, 360)))
        succ = w.ents[e.successor].lei if e.successor else ""
        status = "INACTIVE" if e.reg_status == "RETIRED" else "ACTIVE"
        l1.append((e.lei, e.name, e.country, e.country, e.category, status, succ, ts(e.reg, rng), ts(last, rng),
                   e.reg_status, ts(nxt, rng), world.LOUS[e.country],
                   "FULLY_CORROBORATED" if rng.random() < 0.7 else "ENTITY_SUPPLIED_ONLY"))
    l1.sort()
    wcsv(os.path.join(target, FILES["lei"]),
         ["LEI", "Entity.LegalName", "Entity.LegalAddress.Country", "Entity.LegalJurisdiction",
          "Entity.EntityCategory", "Entity.EntityStatus", "Entity.SuccessorEntity.SuccessorLEI",
          "Registration.InitialRegistrationDate", "Registration.LastUpdateDate", "Registration.RegistrationStatus",
          "Registration.NextRenewalDate", "Registration.ManagingLOU", "Registration.ValidationSources"], l1)

    # ---------------------------------------------------------------- GLEIF level 2
    rng = np.random.default_rng(world.SEED + 8)
    rr = []
    for e in ents:
        if not e.lei or e.parent is None:
            continue
        par = w.ents[e.parent]
        g = w.groups[e.gid]
        top = g.members[0]
        start = min(e.reg, D(2019, 12, 31)) - dt.timedelta(days=int(rng.integers(0, 900)))
        if e.reg > D(2025, 1, 1):
            start = e.reg
        if e.hz:
            start = e.joined
        end = ""
        status = "ACTIVE"
        regst = "LAPSED" if e.reg_status == "LAPSED" else "PUBLISHED"
        if e.reg_status == "RETIRED":
            end, status, regst = e.merged_on.isoformat(), "INACTIVE", "RETIRED"
        vs = "FULLY_CORROBORATED" if rng.random() < 0.75 else "PARTIALLY_CORROBORATED"
        initial = ts(max(start, e.reg), rng)
        upd = ts(EXTRACT_DATE - dt.timedelta(days=int(rng.integers(5, 400))), rng)
        if e.role == "branch":
            rr.append((e.lei, "LEI", par.lei, "LEI", "IS_INTERNATIONAL_BRANCH_OF", "ACTIVE", start.isoformat(), "",
                       "RELATIONSHIP_PERIOD", initial, upd, regst, vs))
            continue
        if e.role == "fund":
            rr.append((e.lei, "LEI", par.lei, "LEI", "IS_FUND-MANAGED_BY", "ACTIVE", start.isoformat(), "",
                       "RELATIONSHIP_PERIOD", initial, upd, regst, vs))
            continue
        if par.lei:
            rr.append((e.lei, "LEI", par.lei, "LEI", "IS_DIRECTLY_CONSOLIDATED_BY", status, start.isoformat(), end,
                       "RELATIONSHIP_PERIOD", initial, upd, regst, vs))
        if top.lei and not e.direct_only:
            rr.append((e.lei, "LEI", top.lei, "LEI", "IS_ULTIMATELY_CONSOLIDATED_BY", status, start.isoformat(),
                       end, "RELATIONSHIP_PERIOD", initial, upd, regst, vs))
    rr.sort()
    wcsv(os.path.join(target, FILES["rr"]),
         ["Relationship.StartNode.NodeID", "Relationship.StartNode.NodeIDType", "Relationship.EndNode.NodeID",
          "Relationship.EndNode.NodeIDType", "Relationship.RelationshipType", "Relationship.RelationshipStatus",
          "Relationship.Period1.startDate", "Relationship.Period1.endDate", "Relationship.Period1.periodType",
          "Registration.InitialRegistrationDate", "Registration.LastUpdateDate", "Registration.RegistrationStatus",
          "Registration.ValidationSources"], rr)

    # ---------------------------------------------------------------- reporting exceptions
    rx = []
    for gid, g in sorted(w.groups.items()):
        top = g.members[0]
        if not top.lei:
            continue
        reason = top.repex or "NON_CONSOLIDATING"
        for cat in ("DIRECT_ACCOUNTING_CONSOLIDATION_PARENT", "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT"):
            rx.append((top.lei, cat, reason, ""))
    rx.sort()
    wcsv(os.path.join(target, FILES["repex"]), ["LEI", "ExceptionCategory", "ExceptionReason", "ExceptionReference"],
         rx)

    # ---------------------------------------------------------------- obligor master
    ob = []
    for e in ents:
        if e.cust is None:
            continue
        g = w.groups[e.gid]
        since = world.cust_since(w, e)
        closed = (g.active_to is not None and g.active_to <= EXTRACT_DATE) or (not e.borrower)
        booking = "HB-DAC" if e.country == "IE" else "HB-PLC"
        ob.append((e.cust, e.name, e.lei or "", e.crn or "", e.country, "" if e.hz else (e.booked or g.gid), since.isoformat(),
                   "CLOSED" if closed else "ACTIVE", booking))
    ob.sort()
    wcsv(os.path.join(target, FILES["obligors"]),
         ["customer_id", "customer_name", "lei", "companies_house_no", "country", "group_id", "customer_since",
          "customer_status", "primary_booking_entity"], ob)

    # ---------------------------------------------------------------- watch-list history
    rng = np.random.default_rng(world.SEED + 9)
    wl = []
    teams = ["Business Support North", "Business Support South", "Restructuring", "Business Support Midlands"]
    for gid, g in sorted(w.groups.items()):
        for ep in g.episodes:
            wl.append((ep["case"], gid, g.name, ep["start"].isoformat(), ep["level"], iso(ep["end"]),
                       ep["reason"] or "", str(rng.choice(teams))))
    wl.sort(key=lambda r: (r[3], r[0]))
    wcsv(os.path.join(target, FILES["watchlist"]),
         ["case_id", "group_id", "group_name", "placed_on", "watch_level", "removed_on", "removal_reason",
          "case_team"], wl)

    # ---------------------------------------------------------------- facilities and their limit history
    rng = np.random.default_rng(world.SEED + 10)
    fx_rows, lh = [], []
    for f in w.facilities:
        ext = world.version_at(f, world.EXTRACT_RUN) or 0.0
        if f.status != "ACTIVE":
            ext = 0.0
        shares = rng.dirichlet(np.ones(len(f.obligors)) * 2.0) if len(f.obligors) > 1 else [1.0]
        util = 0.0 if f.status != "ACTIVE" or f.start > EXTRACT_DATE else \
            (rng.uniform(0.2, 0.95) if f.product != "OVERDRAFT" else rng.uniform(0, 0.6))
        for eid, sh in zip(f.obligors, shares):
            e = w.ents[eid]
            fx_rows.append((f.booking, f.fid, e.cust, f.product, f.ccy, "%.2f" % ext, "%.2f" % (ext * util * sh),
                            f.start.isoformat(), f.maturity.isoformat(), f.status))
        for t, v, src in f.history:
            lh.append((f.booking, f.fid, "%.2f" % v, t.strftime("%Y-%m-%dT%H:%M:%SZ"), src))
    fx_rows.sort(key=lambda r: (r[0], r[1], r[2]))
    wcsv(os.path.join(target, FILES["facilities"]),
         ["booking_entity", "facility_id", "customer_id", "product", "currency", "committed_limit", "drawn_balance",
          "start_date", "final_maturity_date", "facility_status"], fx_rows)
    lh.sort(key=lambda r: (r[0], r[1], r[3]))
    wcsv(os.path.join(target, FILES["limits"]),
         ["booking_entity", "facility_id", "committed_limit", "effective_from", "source"], lh)
    wcsv(os.path.join(target, FILES["fx"]), ["rate_date", "currency", "units_per_gbp", "source"],
         [("2026-09-30", c, "%.4f" % FX[c], "Group Treasury 16:00 London close") for c in ("EUR", "USD")] +
         [("2026-09-30", "CHF", "1.0732", "Group Treasury 16:00 London close"),
          ("2026-09-30", "SEK", "14.6815", "Group Treasury 16:00 London close")])
    wcsv(os.path.join(target, FILES["triggers"]), ["trigger_code", "description", "feed", "default_signal"], [
        ("CCJ", "County court judgment registered against the entity", "REGISTRY", "AMBER"),
        ("COVENANT_BREACH", "Financial covenant breached on the latest compliance certificate", "INTERNAL", "RED"),
        ("COVENANT_RISK", "Covenant headroom under 10 per cent on the latest certificate", "INTERNAL", "AMBER"),
        ("DIRECTOR_CHANGE", "Resignation of a finance director or two or more directors in a quarter", "REGISTRY", "AMBER"),
        ("FILING_LATE", "Statutory accounts overdue at Companies House or the CRO", "REGISTRY", "AMBER"),
        ("GOING_CONCERN", "Material uncertainty paragraph in the latest audited accounts", "REGISTRY", "RED"),
        ("PAY_DEFAULT", "Trade or bank payment more than 60 days past due", "BUREAU", "RED"),
        ("PAY_DELAY", "Days beyond terms up 15 or more on the bureau's trade-payment index", "BUREAU", "AMBER"),
        ("RATING_DOWN", "Downgrade by a rating agency or credit reference agency band", "RATINGS", "RED"),
        ("RATING_WATCH", "Placed on negative watch or outlook", "RATINGS", "AMBER"),
        ("SECTOR_STRESS", "Sector stress overlay from Group Risk's sector watch", "NEWS", "AMBER"),
        ("ADVERSE_NEWS", "Adverse media item classified as credit-relevant", "NEWS", "AMBER"),
        ("WINDING_UP_PETITION", "Winding-up petition advertised in the Gazette", "REGISTRY", "RED"),
    ])

    # ---------------------------------------------------------------- documents and workbooks
    docs.register_workbook(w, os.path.join(target, FILES["register"]))
    docs.standard_pdf(os.path.join(target, FILES["standard"]))
    docs.agenda_docx(os.path.join(target, FILES["agenda"]))
    docs.field_reference(os.path.join(target, FILES["fieldref"]), FILES)
    docs.extract_log(os.path.join(target, FILES["log"]), FILES, target)
    docs.ratings_workbook(w, os.path.join(target, FILES["ratings"]))
    docs.outlook_workbook(os.path.join(target, FILES["outlook"]))

    # file times: one coherent pull
    stamp = dt.datetime(2026, 10, 8, 17, 42, 0).timestamp()
    for f in sorted(os.listdir(target)):
        os.utime(os.path.join(target, f), (stamp, stamp))
    return w


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else TARGET
    build(t, devices="--no-devices" not in sys.argv)
    print("wrote", t)
