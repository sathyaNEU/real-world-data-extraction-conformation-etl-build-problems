"""Write the evidence pack under target/ from the truth in world.py, each file as the system that keeps it writes it.

    python3 task181/generator/build.py
"""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import docs as D     # noqa: E402
import world as W    # noqa: E402

FILES = {
    "ops": "theatre_operations_2022_2027.csv",
    "ssi": "ssi_surveillance_2022_2027.csv",
    "scans": "instrument_tracking_scans_2027.csv",
    "cycles": "steriliser_cycles_2027.csv",
    "register": "cssd_set_register_2027.xlsx",
    "equip": "cssd_equipment_log_2026_2027.xlsx",
    "rates": "haisc_procedure_rates_2026.pdf",
    "notice": "haisc_outlier_notice_kooralong_2027q2.pdf",
    "guide": "haisc_outlier_response_guide_2027.pdf",
    "hygiene": "hand_hygiene_audits_2027.csv",
    "air": "theatre_air_sampling_2027.json",
}
DISTRACTORS = ["hygiene", "air"]
WOUND = {1: "Clean", 2: "Clean-contaminated", 3: "Contaminated", 4: "Dirty"}
DESC = {"COLO": ["Right hemicolectomy", "Anterior resection of rectum", "Sigmoid colectomy", "Left hemicolectomy",
                 "Hartmann's procedure"],
        "SB": ["Small bowel resection", "Small bowel resection with anastomosis"],
        "XLAP": ["Laparotomy", "Exploratory laparotomy"],
        "APPY": ["Laparoscopic appendicectomy", "Appendicectomy"],
        "CHOL": ["Laparoscopic cholecystectomy", "Cholecystectomy, open"],
        "HER": ["Inguinal hernia repair with mesh", "Inguinal hernia repair", "Incisional hernia repair with mesh"]}
THEATRES = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]
FILLER = ["OR", "GY", "UR", "EN", "VA"]


def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M")


def theatre_csv(path, T):
    r = C.rng("pack-ops")
    ops, inf = T["ops"], {i["op"]: i for i in T["inf"]}
    rows = []
    book = 7_400_000
    list_theatre = {}
    for o in ops:
        book += int(r.integers(1, 9))
        o["booking"] = book
        if o["list_id"] not in list_theatre:
            list_theatre[o["list_id"]] = "T8" if o["emergency"] else THEATRES[int(r.integers(0, 7))]
        o["theatre"] = list_theatre[o["list_id"]]
        code = o["consultant"]
        if code == "GS-14" and o["start"].date() < dt.date(2025, 7, 1):
            code = "GS-41"                      # the consultant's code before the 2025 rostering change
        booked = code
        # an emergency admitted and booked under the previous on-call consultant and operated by the next one
        if o["emergency"] and r.random() < 0.32:
            others = [c for c in C.CONSULTANTS if c != o["consultant"]]
            booked = others[int(r.integers(0, len(others)))]
            if booked == "GS-14" and o["start"].date() < dt.date(2025, 7, 1):
                booked = "GS-41"
        o["booked"] = booked
        o["code"] = code
        knife = o["start"]
        anaes = knife - dt.timedelta(minutes=int(r.integers(18, 45)))
        close = knife + dt.timedelta(minutes=o["minutes"])
        out = close + dt.timedelta(minutes=int(r.integers(8, 22)))
        desc = DESC[o["proc"]]
        d = desc[int(r.integers(0, len(desc)))]
        if o["proc"] == "HER":
            d = desc[0] if o["mesh"] else desc[1]
        rows.append([book, 1, o["ur"], o["theatre"], o["start"].date().isoformat(),
                     "EM" if o["emergency"] else ("PM" if o["list_id"].endswith("PM") else "AM"),
                     booked, code, d, o["proc"], fmt(anaes), fmt(knife), fmt(close), fmt(out), o["asa"],
                     WOUND[o["wound"]], "Emergency" if o["emergency"] else "Elective", "Completed", "N",
                     "Y" if o["mesh"] else "N"])
        if o["proc"] == "CHOL" and not o["emergency"] and r.random() < 0.06:
            # an add-on procedure: its own booking before the 2025 theatre system upgrade, a second line after
            if o["start"].year <= 2024:
                book += 1
                rows.append([book, 1, o["ur"], o["theatre"], o["start"].date().isoformat(), rows[-1][5], booked,
                             code, "Umbilical hernia repair", "HER", fmt(anaes), fmt(knife), fmt(close), fmt(out),
                             o["asa"], WOUND[o["wound"]], "Elective", "Completed", "N", "N"])
            else:
                rows.append([book, 2, o["ur"], o["theatre"], o["start"].date().isoformat(), rows[-1][5], booked,
                             code, "Umbilical hernia repair", "HER", fmt(anaes), fmt(knife), fmt(close), fmt(out),
                             o["asa"], WOUND[o["wound"]], "Elective", "Completed", "N", "N"])
        i = inf.get(o["id"])
        if i and i["depth"] == "Organ/space" and r.random() < 0.55:
            rt = dt.datetime.combine(i["onset"] + dt.timedelta(days=int(r.integers(0, 3))), dt.time(int(r.integers(9, 21)),
                                     int(r.choice([0, 15, 30, 45]))))
            book += 1
            rows.append([book, 1, o["ur"], "T8", rt.date().isoformat(), "EM", code, code, "Laparotomy, washout",
                         "XLAP", fmt(rt - dt.timedelta(minutes=30)), fmt(rt), fmt(rt + dt.timedelta(minutes=75)),
                         fmt(rt + dt.timedelta(minutes=90)), max(o["asa"], 3), "Dirty", "Emergency", "Completed",
                         "Y", "N"])
        if r.random() < 0.025:
            book += 1
            rows.append([book, 1, o["ur"] + 7, o["theatre"], o["start"].date().isoformat(), rows[-1][5], code, code,
                         d, o["proc"], "", "", "", "", "", "", "Elective", "Cancelled", "N", "N"])
    rows.sort(key=lambda x: (x[4], x[11] or "99", x[0], x[1]))
    C.write_csv(path, ["booking_no", "procedure_seq", "ur_number", "theatre", "list_date", "session",
                       "booked_consultant", "responsible_consultant", "procedure", "surveillance_category",
                       "anaesthetic_start", "knife_to_skin", "wound_closure", "out_of_theatre", "asa_class",
                       "wound_class", "urgency", "status", "return_to_theatre", "implant"], rows)
    return len(rows)


def ssi_csv(path, T):
    r = C.rng("pack-ssi")
    ops = {o["id"]: o for o in T["ops"]}
    rows = []
    iid = 20_000
    for i in sorted(T["inf"], key=lambda x: (x["onset"], x["op"])):
        o = ops[i["op"]]
        iid += int(r.integers(1, 4))
        nurse = ["IPC-04", "IPC-07", "IPC-11", "IPC-15"][int(r.integers(0, 4))]
        det = "Post-discharge review" if i["post_discharge"] else ("Readmission" if r.random() < 0.3 else "Inpatient")
        entered = i["onset"] + dt.timedelta(days=int(r.integers(1, 9)))
        first = i["depth"]
        legacy = o["start"].year <= 2024
        opdate = o["start"].date()
        cons = o["code"]
        bk = "" if legacy else o["booking"]
        if legacy:
            cons = o["booked"]
            if o["emergency"] and r.random() < 0.4:
                opdate = opdate - dt.timedelta(days=int(r.integers(1, 3)))
        # a deep or organ/space infection first recorded as superficial and reclassified
        if i["depth"] != "Superficial incisional" and r.random() < 0.22:
            first = "Superficial incisional"
            rows.append([iid, 1, bk, o["ur"], opdate.isoformat(), o["proc"], cons,
                         i["onset"].isoformat(), first, det, "Confirmed", entered.isoformat(), nurse])
            rows.append([iid, 2, bk, o["ur"], opdate.isoformat(), o["proc"], cons,
                         i["onset"].isoformat(), i["depth"], det, "Confirmed",
                         (entered + dt.timedelta(days=int(r.integers(3, 15)))).isoformat(), nurse])
        else:
            rows.append([iid, 1, bk, o["ur"], opdate.isoformat(), o["proc"], cons,
                         i["onset"].isoformat(), i["depth"], det, "Confirmed", entered.isoformat(), nurse])
        # the same infection entered again from the readmission ward by a second nurse
        if r.random() < 0.06:
            iid += int(r.integers(1, 4))
            other = ["IPC-04", "IPC-07", "IPC-11", "IPC-15"][int(r.integers(0, 4))]
            rows.append([iid, 1, bk, o["ur"], opdate.isoformat(), o["proc"], cons,
                         (i["onset"] + dt.timedelta(days=int(r.integers(0, 3)))).isoformat(), i["depth"],
                         "Readmission", "Confirmed", (entered + dt.timedelta(days=int(r.integers(1, 6)))).isoformat(),
                         other])
    # suspected wound infections reviewed and found not to meet the definition
    ops_list = T["ops"]
    for k in range(int(len(T["inf"]) * 0.18)):
        o = ops_list[int(r.integers(0, len(ops_list)))]
        iid += int(r.integers(1, 4))
        on = o["start"].date() + dt.timedelta(days=int(r.integers(2, 20)))
        rows.append([iid, 1, "" if o["start"].year <= 2024 else o["booking"], o["ur"], o["start"].date().isoformat(),
                     o["proc"], o.get("code", o["consultant"]), on.isoformat(), "Superficial incisional", "Inpatient",
                     "Not SSI", (on + dt.timedelta(days=4)).isoformat(), "IPC-07"])
    rows = [x for x in rows if x[7] <= C.EXTRACT.isoformat()]
    rows.sort(key=lambda x: (x[11], x[0], x[1]))
    C.write_csv(path, ["infection_id", "record_version", "booking_no", "ur_number", "operation_date",
                       "surveillance_category",
                       "consultant_code", "onset_date", "depth", "detected", "status", "entered", "entered_by"], rows)
    return len(rows)


def write_scans(path, T, inst, ops_by_id):
    """Theatre, decontamination and packing scans, then each steriliser load scan with its cycle and the release."""
    r = C.rng("pack-scans")
    rows = []
    for u in inst["uses"]:
        o = ops_by_id[u["op"]]
        rows.append([C.to_utc(u["scan"]).strftime("%Y-%m-%dT%H:%M:%SZ"), u["barcode"], "THEATRE %s" % o["theatre"],
                     o["ur"], "", "TH%02d" % int(r.integers(1, 40))])
    for p in inst["passes"]:
        for when, station in ((p["recv"], "DECON RECEIVE"), (p["wash"], "WASHER"), (p["pack"], "PACK BENCH")):
            rows.append([C.to_utc(when).strftime("%Y-%m-%dT%H:%M:%SZ"), p["barcode"], station, "", "",
                         "CS%02d" % int(r.integers(1, 30))])
    for c in inst["cycles"]:
        if c["kind"] != "Load":
            continue
        for b in c["contents"]:
            rows.append([C.to_utc(c["start"] - dt.timedelta(minutes=int(r.integers(2, 9)))).strftime(
                "%Y-%m-%dT%H:%M:%SZ"), b, "STERILISER %s" % c["st"], "", c["no"], "CS%02d" % int(r.integers(1, 30))])
            if c["result"] == "Pass":
                rows.append([C.to_utc(c["end"] + dt.timedelta(minutes=int(r.integers(25, 50)))).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"), b, "STORE RELEASE", "", "", "CS%02d" % int(r.integers(1, 30))])
    rows.sort(key=lambda x: (x[0], x[1]))
    C.write_csv(path, ["scan_utc", "barcode", "station", "ur_number", "cycle_no", "operator"], rows)
    return len(rows)


def cycles_csv(path, inst):
    r = C.rng("pack-cycles")
    rows = []
    for c in inst["cycles"]:
        items = list(c["contents"])
        if c["kind"] == "Load":
            for k in range(int(r.integers(2, 9))):
                items.append("%s%05d" % (FILLER[int(r.integers(0, len(FILLER)))], int(r.integers(10000, 99999))))
            r.shuffle(items)
        prog = "" if c["kind"] != "Load" else ("134C 3.5 min porous load" if c["st"] != "S3" else
                                                "134C 3.5 min containers")
        rows.append([c["st"], c["no"], c["kind"], prog, C.to_utc(c["start"]).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     C.to_utc(c["end"]).strftime("%Y-%m-%dT%H:%M:%SZ"), c["result"],
                     "%.1f" % (134.0 + float(r.uniform(0.1, 0.9))) if c["kind"] != "Vacuum leak test" else "",
                     "CS%02d" % int(r.integers(1, 30)), ";".join(items)])
    rows.sort(key=lambda x: (x[4], x[0]))
    C.write_csv(path, ["steriliser", "cycle_no", "cycle_type", "program", "start_utc", "end_utc", "result",
                       "sterilising_temperature", "operator", "items"], rows)
    return len(rows)


def hygiene_csv(path):
    r = C.rng("pack-hygiene")
    rows = []
    wards = ["4 East", "4 West", "5 North", "Surgical Short Stay", "ICU", "Theatre Recovery"]
    for m in range(1, 10):
        for w in wards:
            for mom in ["Before patient contact", "Before procedure", "After body fluid exposure",
                        "After patient contact", "After touching surroundings"]:
                n = int(r.integers(18, 46))
                k = int(r.binomial(n, float(r.uniform(0.78, 0.93))))
                rows.append(["2027-%02d" % m, w, mom, n, k])
    C.write_csv(path, ["audit_month", "ward", "moment", "moments_observed", "moments_compliant"], rows)


def air_json(path):
    r = C.rng("pack-air")
    recs = []
    d = dt.date(2027, 1, 6)
    while d <= C.WIN1:
        for t in THEATRES:
            recs.append({"theatre": t, "sampled": d.isoformat(), "state": "at rest",
                         "particles_0_5um_m3": int(r.integers(9000, 32000)),
                         "settle_plate_cfu": int(r.poisson(1.2))})
        d += dt.timedelta(days=14)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"system": "Kooralong Hospital BMS theatre monitoring", "exported": "2028-01-04T09:12:00+11:00",
                   "records": recs}, f, indent=1)
        f.write("\n")
    C.set_mtime(path)


def build(target=C.TARGET):
    os.makedirs(target, exist_ok=True)
    for n in os.listdir(target):
        os.remove(os.path.join(target, n))
    T = W.build_truth()
    ops_by_id = {o["id"]: o for o in T["ops"]}
    p = lambda k: os.path.join(target, FILES[k])
    n_ops = theatre_csv(p("ops"), T)
    n_ssi = ssi_csv(p("ssi"), T)
    n_scans = write_scans(p("scans"), T, T["inst"], ops_by_id)
    n_cyc = cycles_csv(p("cycles"), T["inst"])
    D.set_register(p("register"), T["inst"])
    D.equipment_log(p("equip"))
    D.rates_pdf(p("rates"))
    D.guide_pdf(p("guide"))
    D.notice_pdf(p("notice"), T)
    hygiene_csv(p("hygiene"))
    air_json(p("air"))
    return T, dict(ops=n_ops, ssi=n_ssi, scans=n_scans, cycles=n_cyc)


if __name__ == "__main__":
    T, n = build()
    print(n)
