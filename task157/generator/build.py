"""task157 architecture 3: build the pack under target/, the goldens under golden/, figures.json, metadata.json,
then run the checks. Two runs give byte-identical files.

    python3 build.py            # build and check
    python3 build.py --no-check
"""
from __future__ import annotations

import csv
import io
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C            # noqa: E402
import docs as D            # noqa: E402
import network as N         # noqa: E402
import params as P          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import simulate as SIM      # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

FILES = {
    "avl": "avl_timing_point_events.csv",
    "txc": "gcr_lot2_timetable_winter2026_txc.xml",
    "duty": "saltmeadow_duty_schedule_winter2026.xlsx",
    "log": "control_room_log_sep_dec_2026.csv",
    "returns": "saltmeadow_daily_returns_autumn2026.xlsx",
    "etm": "etm_transactions_service41_oct_nov2026.csv",
    "fleet": "saltmeadow_fleet_register.csv",
    "stages": "service41_fare_stages.csv",
    "causes": "lost_mileage_cause_codes.csv",
    "published": "bus_punctuality_by_route_monthly.csv",
    "sched7": "franchise_lot2_schedule7_performance_regime.pdf",
    "tmp": "thornsby_bridge_closure_tmp_v2.pdf",
    "closeout": "marsh_lane_closure_2025_closeout.pdf",
    "atc": "ring_road_crossing_atc_counts_2026.csv",
    "works": "street_works_permits_2027q1.csv",
}
DISTRACTORS = ("atc", "works")
GOLDEN_XLSX = "closure_punctuality_forecast_2027.xlsx"
GOLDEN_SVG = "closure_punctuality_by_route.svg"
PDF_DATES = {"sched7": (b"D:20260821094200+01'00'", b"D:20260828161500+01'00'"),
             "tmp": (b"D:20261120112000+00'00'", b"D:20261127153800+00'00'"),
             "closeout": (b"D:20250527100500+01'00'", b"D:20250530124700+01'00'")}
OOXML = {"duty": (P.PEOPLE["scheduler"], P.PEOPLE["scheduler"], "2026-08-11T08:40:00Z", "2026-08-14T13:52:00Z",
                  "Saltmeadow winter 2026/27 duty schedule", "Pellbridge Buses Ltd"),
         "returns": ("Saltmeadow Traffic Office", P.PEOPLE["clerk"], "2026-09-01T05:12:00Z", "2026-12-07T06:31:00Z",
                     "Saltmeadow daily returns", "Pellbridge Buses Ltd")}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        w.writerows(rows)


def write_xlsx(path, sheets, title_rows=None, widths=None):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for name, (head, rows) in sheets.items():
        ws = wb.create_sheet(name)
        for t in (title_rows or {}).get(name, []):
            ws.append([t if t else None])
            if t:
                ws.cell(row=ws.max_row, column=1).font = Font(bold=ws.max_row == 1)
        ws.append(list(head))
        hr = ws.max_row
        for c in ws[hr]:
            c.font = Font(bold=True)
        for row in rows:
            ws.append([None if v == "" else v for v in row])
        for i, h in enumerate(head):
            col = ws.cell(row=hr, column=i + 1).column_letter
            ws.column_dimensions[col].width = (widths or {}).get(i, max(9, min(48, 1.1 * max(
                len(str(h)), *(len(str(r[i])) for r in rows[:400])) + 1)) if rows else 12)
        ws.freeze_panes = "A%d" % (hr + 1)
    wb.save(path)


def world():
    """Everything the pack and the goldens are cut from."""
    S = N.build()
    base, lost, meta = SIM.simulate(S, want_meta=True)
    protect = set()
    for d, m in meta.items():
        for u in m["uncovered"]:
            if u[4] is not None:
                protect.add((d, S[P.day_type(d)]["pieces"][u[2]]["board"]))
    head, rows, parsed = R.avl(base, protect=protect)
    return dict(S=S, base=base, lost=lost, meta=meta, avl=(head, rows), parsed=parsed)


def write_pack(W):
    if os.path.exists(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    S = W["S"]
    t = lambda k: os.path.join(TARGET, FILES[k])
    write_csv(t("avl"), *W["avl"])
    with open(t("txc"), "w", encoding="utf-8", newline="\n") as f:
        f.write(R.txc(S))
    duties, pieces = R.duty_rows(S)
    title = ["Pellbridge Buses Ltd, Saltmeadow depot (SMD): Lot 2 duty schedule, winter 2026/27",
             "In force 31 August 2026 to 3 April 2027 (the winter registration). Agreed with the depot's trade union "
             "representatives on 14 August 2026.", ""]
    write_xlsx(t("duty"), {
        "Duties": (("Duty", "Days", "Sign on", "On at", "Sign off", "Off at", "Spread", "Platform", "Pieces"), duties),
        "Pieces": (("Duty", "Days", "Piece", "Running board", "Svc", "Takes over", "At", "Relieved", "At"), pieces)},
        title_rows={"Duties": title, "Pieces": title})
    log, ret = R.logs(S, W["lost"], W["meta"], W["base"])
    write_csv(t("log"), ("log_time", "line_no", "journey_ref", "fleet_no", "log_event", "lost_from_stop", "lost_to_stop",
                         "cause", "remarks"),
              [(e["t"].strftime("%d/%m/%Y %H:%M"), e["service"], e["journey"], e["vehicle"], e["event"], e["lost_from"],
                e["lost_to"], e["cause"], e["remarks"]) for e in log])
    write_xlsx(t("returns"), {"Returns": (("Date", "Duty", "Piece", "Board", "Svc", "Status", "Covered from", "Reason"),
                                          [(e["date"].strftime("%d/%m/%Y"), e["duty"], e["piece"], e["board"], e["service"],
                                            e["status"], e["covered_from"], e["reason"]) for e in ret])},
               title_rows={"Returns": ["Saltmeadow depot: daily return of uncovered and covered work", ""]})
    eh, er, truth = R.etm(S, W["base"])
    write_csv(t("etm"), eh, er)
    write_csv(t("fleet"), *R.fleet_rows())
    write_csv(t("stages"), *R.fare_stage_rows())
    write_csv(t("causes"), *R.cause_rows())
    ph, pr = R.published(W["parsed"])
    write_csv(t("published"), ph, pr)
    write_csv(t("atc"), *R.ring_road_counts())
    write_csv(t("works"), *R.street_works())
    D.write_schedule7(t("sched7"))
    D.write_tm_plan(t("tmp"))
    close = closeout_rows(pr)
    D.write_closeout(t("closeout"), close)
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(t(k), c, m)
    for k, (cr, lb, c, m, title_, co) in OOXML.items():
        PP.normalize_ooxml(t(k), cr, lb, c, m, title=title_, excel=True, company=co)
    W.update(log=log, ret=ret, etm=(eh, er), etm_truth=truth, published=pr, duties=duties, pieces=pieces)
    return W


def closeout_rows(pub_rows):
    vals = {(r[0], r[1], r[5]): r for r in pub_rows}
    on = sum(vals[("14", m, "final")][3] for m in ("2025-03", "2025-04"))
    dep = sum(vals[("14", m, "final")][2] for m in ("2025-03", "2025-04"))
    return dict(running=[("Weekday peaks (07:30 to 09:30, 16:00 to 18:30)", "6 minutes", "5.8 minutes"),
                         ("All other times", "4 minutes", "4.3 minutes")],
                forecast="72.9", realised="%.1f" % (100.0 * on / dep))


PROVENANCE = {
    "avl": ("2026-12-07", "the Combined Authority's AVL archive of Lot 2 timing point events, 1 September to 6 December 2026"),
    "txc": ("2026-08-21", "the Lot 2 winter 2026/27 registered timetable as published in the Combined Authority's TransXChange data"),
    "duty": ("2026-08-14", "Pellbridge Buses' Saltmeadow depot duty schedule for the winter 2026/27 registration"),
    "log": ("2026-12-07", "the Combined Authority's bus control room log for Lot 2, 1 September to 7 December 2026"),
    "returns": ("2026-12-07", "Pellbridge Buses' Saltmeadow depot daily returns of uncovered and covered work"),
    "etm": ("2026-12-02", "Pellbridge Buses' ticket machine transactions on service 41, October and November 2026"),
    "fleet": ("2026-11-30", "Pellbridge Buses' Saltmeadow fleet register"),
    "stages": ("2026-08-31", "the service 41 fare stage table"),
    "causes": ("2026-08-31", "the control room's lost mileage cause codes"),
    "published": ("2026-12-04", "the Combined Authority's published monthly punctuality by route, January 2025 to November 2026"),
    "sched7": ("2026-08-28", "the Lot 2 bus franchise agreement, Schedule 7 (Performance Regime), consolidated version 1.4"),
    "tmp": ("2026-11-27", "Grainford City Council's traffic management plan for the Thornsby Bridge closure, version 2"),
    "closeout": ("2025-05-30", "the Combined Authority's close-out note on the 2025 Marsh Lane outbound closure"),
    "atc": ("2026-12-01", "Grainford City Council's automatic traffic counter on the Ring Road crossing, 2026"),
    "works": ("2026-12-09", "Grainford City Council's street works permit register, works starting January to March 2027"),
}
FICTION = ("constructed by the task generator (seeded); the Grainford City Region Combined Authority, Pellbridge Buses, "
           "Grainford City Council, the places, people and records are fictional")


def _relief_gaps(S):
    """The duty schedule's joins off route 41 at the interchange: the gap to each city route's departure."""
    gaps = {}
    for dt, s in S.items():
        for b41, k, b, i, r, g in s["feeds"]:
            gaps.setdefault(r, set()).add(g)
    return dict(gap_27=sorted(gaps["27"]), gap_58=sorted(gaps["58"]), min_gap_33=min(gaps["33"]),
                max_gap_33=max(gaps["33"]), join_max=30, turn_min=1)


def figures(W, M):
    S = W["S"]
    A = C.ask_a(S, W["lost"])
    B = C.ask_b(W["etm_truth"], W["etm"][1])
    sea = C.seasonal(M, W["published"])
    named = M["golden"]["set"]
    total_km = sum(A["op_km"].values())
    lot_rel = 100.0 * (sum(A["sched_km"].values()) - total_km) / sum(A["sched_km"].values())
    A["op_km_total"] = total_km
    A["reliability_lot"] = lot_rel
    sets = {k: M[k]["set"] for k in M if isinstance(M[k], dict) and "set" in M[k]}
    fig = dict(
        call=dict(routes=named, sentence="Name routes 27, 41 and 58 in the Thornsby Bridge Disruption Notice: each is "
                  "forecast below the 80 per cent punctuality floor while the bridge is shut; every other Lot 2 route "
                  "stays above it.", default_path_set=M["R0"]["set"]),
        autumn={r: round(M["autumn"][r], 1) for r in P.ROUTE_ORDER},
        autumn_raw=M["autumn"],
        forecast={r: M["golden"]["p"][r] for r in P.ROUTE_ORDER},
        below_floor={r: r in named for r in P.ROUTE_ORDER},
        rungs={k: dict(set=v, p={r: round(x, 2) for r, x in M[k]["p"].items()}) for k, v in sets.items()},
        seasonal=dict(shift={r: round(x, 2) for r, x in sea["shift"].items()}, set=sea["set"]),
        closure_mix=M["mix"],
        ask_a=dict(op_km={r: round(A["op_km"][r]) for r in P.ROUTE_ORDER},
                   op_km_raw={r: A["op_km"][r] for r in P.ROUTE_ORDER},
                   reliability={r: round(A["reliability"][r], 2) for r in P.ROUTE_ORDER},
                   reliability_raw=A["reliability"], sched_km={r: round(A["sched_km"][r], 1) for r in P.ROUTE_ORDER},
                   op_km_total=round(total_km), reliability_lot=round(lot_rel, 2)),
        ask_b=dict(weekdays=B["weekdays"], cells={"%s|%s" % k: round(v) for k, v in B["cells"].items()},
                   cells_raw={"%s|%s" % k: v for k, v in B["cells"].items()},
                   by_band={b: round(B["cells"][("I", b)] + B["cells"][("O", b)]) for b in ("AM peak", "PM peak", "Other times")},
                   by_dir={d: round(sum(B["cells"][(d, b)] for b in ("AM peak", "PM peak", "Other times"))) for d in ("I", "O")},
                   total=round(B["total"])),
        relief=_relief_gaps(S),
        schedule7=dict(schedule=7, clauses=["7.2", "7.4", "7.5", "7.6"]),
        diversion=dict(peak_min=P.DIV_MIN_PEAK, off_min=P.DIV_MIN_OFF, corridor_min=P.CORRIDOR_MIN_PEAK, floor=P.FLOOR,
                       km_out=P.DIV_KM_OUT, km_in=P.DIV_KM_IN, notice_due="21 December 2026"),
    )
    wb = dict(autumn=M["autumn"], forecast=fig["forecast"], call=dict(routes=named),
              ask_a=dict(A, op_km_total=total_km, reliability_lot=lot_rel), ask_b=B)
    return fig, wb


def write_goldens(wbfig):
    import deliver as DL
    if os.path.exists(GOLDEN):
        shutil.rmtree(GOLDEN)
    os.makedirs(GOLDEN)
    DL.write_workbook(os.path.join(GOLDEN, GOLDEN_XLSX), wbfig)
    PP.normalize_ooxml(os.path.join(GOLDEN, GOLDEN_XLSX), P.PEOPLE["authority"], P.PEOPLE["authority"],
                       "2026-12-09T09:14:00Z", "2026-12-11T16:42:00Z", title="Thornsby Bridge closure: punctuality forecast",
                       excel=True, company=P.AUTHORITY)
    DL.write_chart(os.path.join(GOLDEN, GOLDEN_SVG), wbfig)
    PP.normalize_svg(os.path.join(GOLDEN, GOLDEN_SVG))


def write_metadata(W, fig):
    import hashlib
    rows = {}
    for k, f in FILES.items():
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                rows[f] = sum(1 for _ in fh) - 1
    meta = dict(
        task="task157",
        title="Thornsby Bridge: the routes the Disruption Notice names",
        domain="Urban & Regional Science (transport forecasting)",
        objective="Forecasting & Predictive Modeling",
        answer=fig["call"]["sentence"],
        deliverables=[GOLDEN_XLSX, GOLDEN_SVG],
        distractor_files=["target/" + FILES[k] for k in DISTRACTORS],
        stated_inputs=["target/" + FILES[k] for k in FILES if k not in DISTRACTORS],
        rows=rows,
        provenance={FILES[k]: dict(date=d, source="%s; %s" % (src, FICTION), licence="CC0 1.0 (constructed for this task)")
                    for k, (d, src) in PROVENANCE.items()},
    )
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
        f.write("\n")


def run(check=True):
    W = world()
    W = write_pack(W)
    M = C.main(W["parsed"], W["S"])
    fig, wbfig = figures(W, M)
    write_goldens(wbfig)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, sort_keys=True, default=str)
        f.write("\n")
    write_metadata(W, fig)
    if check:
        import checks
        ok = checks.run(TARGET, GOLDEN, W, M, fig)
        if not ok:
            sys.exit(1)
    return W, M, fig


if __name__ == "__main__":
    run(check="--no-check" not in sys.argv)
