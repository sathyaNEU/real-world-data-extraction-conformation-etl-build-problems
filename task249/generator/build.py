"""Write the task249 pack into a target folder: the provider's results exports, layouts, the bank snapshot and its
renumbering, the register's number changes, the review bookings, the seat plan, the event log, the incident
reports, the panel's decision log and minutes, the regulations, the notes and the request.   B.run(target) -> world"""
import os

import docs as D
import params as P
import postprocess
import records as R
import asks as A
import sim

FILES = dict(
    request="resit_exposure_request.eml",
    regs="CCC_examination_regulations.pdf",
    notes="data_notes.md",
    export3="results_export_r3_2026-02_to_2027-05.csv",
    export4="results_export_r4_2027-08_to_2027-11.csv",
    layouts="form_layouts_2026_2027.csv",
    bank="item_bank_snapshot_2027-12-31.xlsx",
    crosswalk="item_renumbering_2027-01-11.csv",
    register="candidate_number_changes.csv",
    reviews="results_review_bookings.csv",
    seat="seat_plan_2027.csv",
    events="workstation_event_log_2027.csv",
    incidents="invigilator_incident_reports_2027.xlsx",
    panel_log="item_panel_decision_log.csv",
    minutes="item_review_panel_minutes_2027.pdf",
    practice="practice_exam_orders_2026_2027.csv",
    capacity="exam_centre_capacity_2027.xlsx",
)
PACK = ["request", "regs", "notes", "export3", "export4", "layouts", "bank", "crosswalk", "register", "reviews",
        "seat", "events", "incidents", "panel_log", "minutes", "practice", "capacity"]
DISTRACTORS = ["practice", "capacity", "panel_log", "minutes"]
CONTEXT = ["regs"]
STAMP_PDF = {"regs": "2027-06-09T11:20:00", "minutes": "2027-12-20T16:05:00"}


def practice_orders(W, R0, rng):
    """the Institute's online practice test, sold to registered candidates: an order log"""
    import datetime as dt
    import pandas as pd
    out = []
    serial = 0
    for i, r in enumerate(W["rows"]):
        if rng.uniform() < 0.22:
            serial += 1
            d = R.window_day(r["w"], 0) - dt.timedelta(days=int(rng.integers(5, 60)))
            out.append(dict(order_no="PT%06d" % (500000 + serial * 11 % 400000 + serial),
                            candidate_no=R.number_on(R0["held"], r["cand"], d),
                            ordered_on=d.isoformat(), product="CCC practice test (100 items, online)",
                            price_inr=1450 if d.year == 2026 else 1600))
    return pd.DataFrame(out).sort_values(["ordered_on", "order_no"]).reset_index(drop=True)


def run(target):
    import numpy as np
    os.makedirs(target, exist_ok=True)
    F = FILES
    W = sim.world()
    R0 = R.build(W)
    AK = A.build(W, R0)
    j = lambda k: os.path.join(target, F[k])
    R0["exp_a"].to_csv(j("export3"), index=False, encoding="utf-8")
    R0["exp_b"].to_csv(j("export4"), index=False, encoding="utf-8")
    R0["layouts"].to_csv(j("layouts"), index=False, encoding="utf-8")
    bank = R.bank_snapshot(W, R0["ids"], R0["dec"], AK["panel"]["logged"])
    D.bank_xlsx(j("bank"), bank)
    R0["crosswalk"].to_csv(j("crosswalk"), index=False, encoding="utf-8")
    R0["changes"].to_csv(j("register"), index=False, encoding="utf-8")
    R0["reviews"].to_csv(j("reviews"), index=False, encoding="utf-8")
    AK["a"]["seat"].to_csv(j("seat"), index=False, encoding="utf-8")
    AK["a"]["events"].to_csv(j("events"), index=False, encoding="utf-8")
    D.incidents_xlsx(j("incidents"), AK["a"]["reports"])
    AK["panel"]["log"].to_csv(j("panel_log"), index=False, encoding="utf-8")
    counts = {w: sum(1 for d in R0["dec"].values() if d["w"] == w) for w in range(4, 8)}
    D.minutes(j("minutes"), F, counts)
    practice_orders(W, R0, np.random.default_rng(P.SEED + 77)).to_csv(j("practice"), index=False, encoding="utf-8")
    D.capacity_xlsx(j("capacity"))
    D.regulations(j("regs"), F)
    D.notes(j("notes"), F)
    D.request(j("request"), F)
    for k, stamp in STAMP_PDF.items():
        postprocess.scrub(j(k), "Microsoft Word 2019", stamp)
    for k, created, modified in (("bank", "2027-01-11T06:10:00Z", "2027-12-31T17:45:00Z"),
                                 ("incidents", "2027-02-08T03:30:00Z", "2027-11-20T12:15:00Z"),
                                 ("capacity", "2026-12-14T09:00:00Z", "2027-01-20T10:40:00Z")):
        postprocess.scrub(j(k), P.ORG, modified[:10])
        postprocess.finish_office(j(k), created, modified, P.ORG)
    return {"W": W, "R": R0, "A": AK, "bank": bank, "F": F}
