"""Recompute every graded figure from the shipped bundle alone (target/ and the prompt); share no code with the
generator. Exit 0 when every figure equals figures.json at its printed precision and every convergence holds.

    python3 task399/generator/verify.py [target_dir]
"""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NZT = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
P1 = (dt.date(2024, 10, 1), dt.date(2025, 9, 30))
P2 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
MONTHS = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]
MAG = "Community Magistrate J. Pellow"


def rows_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def rows_xlsx(path, sheet):
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    hdr = list(next(it))
    return [dict(zip(hdr, r)) for r in it]


def to_date(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def minutes_text(s):
    t, ap = s.split(" ")
    h, m = t.split(":")
    h = int(h) % 12 + (12 if ap.startswith("p") else 0)
    return h * 60 + int(m)


def local_of_utc(s):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(NZT)
    return t


def gap(rows):
    a = [r for r in rows if not r["counsel"]]
    b = [r for r in rows if r["counsel"]]
    sa = sum(r["ric"] for r in a) / len(a)
    sb = sum(r["ric"] for r in b) / len(b)
    return 100.0 * (sa - sb)


def main_figures(target):
    app = rows_csv(os.path.join(target, "cms_appearances_oct2024_sep2026.csv"))
    first = []
    for r in app:
        if r["AppearanceType"] != "First appearance (custody)":
            continue
        d = dt.date.fromisoformat(r["AppearanceDate"])
        called = dt.datetime.fromisoformat(r["CalledAt"])
        assert called.astimezone(NZT).date() == d, ("SF4", r["CRN"])
        first.append(dict(crn=r["CRN"], court=r["Court"], date=d, minute=called.hour * 60 + called.minute,
                          officer=r["JudicialOfficer"], counsel=r["CounselOfRecord"].strip(),
                          ric=int(r["Outcome"] == "Remanded in custody")))
    crns = [r["crn"] for r in first]
    assert len(crns) == len(set(crns)), "SF10 one first appearance per case"
    cal = rows_xlsx(os.path.join(target, "court_sitting_calendar_2024-2026.xlsx"), "Sittings")
    win = {}
    for c in cal:
        if c["List"] == "AVL remand list" and c["Court"].startswith("Kestrel Bay"):
            win[to_date(c["Sitting date"])] = (minutes_text(c["Start"]), minutes_text(c["Finish"]))
    # SF8: the AVL list's own appearances span the same window
    avl_calls = defaultdict(list)
    for r in app:
        if r["List"] == "AVL remand" and r["Court"] == "KBY":
            t = dt.datetime.fromisoformat(r["CalledAt"])
            avl_calls[dt.date.fromisoformat(r["AppearanceDate"])].append(t.hour * 60 + t.minute)
    alt = {d: (min(v), max(v)) for d, v in avl_calls.items()}
    assert set(alt) == set(win), "SF8 every calendar AVL sitting has its appearances"
    f = {}
    for r in first:
        w = win.get(r["date"]) if r["court"] == "KBY" else None
        r["avl"] = int(w is not None and w[0] <= r["minute"] < w[1])
        a = alt.get(r["date"]) if r["court"] == "KBY" else None
        r["avl_alt"] = int(a is not None and a[0] <= r["minute"] <= a[1])
        assert r["avl"] == r["avl_alt"], ("SF8", r["crn"])
    for lab, (lo, hi) in (("2025", P1), ("2026", P2)):
        yr = [r for r in first if lo <= r["date"] <= hi]
        f["region_gap_" + lab] = gap(yr)
        for code, c in (("KBY", "KB"), ("DUN", "DN"), ("ASH", "AG"), ("THM", "RC")):
            f["gap_%s_%s" % (c, lab)] = gap([r for r in yr if r["court"] == code])
    kb = [r for r in first if r["court"] == "KBY" and P2[0] <= r["date"] <= P2[1]]
    f["kb_avl_gap"] = gap([r for r in kb if r["avl"]])
    f["kb_other_gap"] = gap([r for r in kb if not r["avl"]])
    f["kb_avl_mag_gap"] = gap([r for r in kb if r["avl"] and r["officer"] == MAG])
    f["kb_avl_judges_gap"] = gap([r for r in kb if r["avl"] and r["officer"] != MAG])
    f["kb_other_mag_gap"] = gap([r for r in kb if not r["avl"] and r["officer"] == MAG])
    f["kb_other_judges_gap"] = gap([r for r in kb if not r["avl"] and r["officer"] != MAG])
    f["kb_avl_unrepresented"] = sum(1 for r in kb if r["avl"] and not r["counsel"])
    rest1 = [r for r in first if P1[0] <= r["date"] <= P1[1] and not r["avl"]]
    rest2 = [r for r in first if P2[0] <= r["date"] <= P2[1] and not r["avl"]]
    f["region_widening"] = f["region_gap_2026"] - f["region_gap_2025"]
    f["region_widening_rest"] = gap(rest2) - gap(rest1)
    return f


def em_figures(target):
    """Section 2 of the standard on section 1's population: the District Courts' orders. An order the unit holds with no
    District Court order behind it sits on a case the District Court had transferred to the High Court, which sits at
    the Kestrel Bay courthouse and made the order itself."""
    app = rows_csv(os.path.join(target, "cms_appearances_oct2024_sep2026.csv"))
    orders_by_crn, orders_by_person = defaultdict(list), defaultdict(list)
    moved_by_crn, moved_by_person = defaultdict(list), defaultdict(list)
    for r in app:
        d = dt.date.fromisoformat(r["AppearanceDate"])
        pk = (r["Surname"].upper(), r["GivenNames"].upper(), r["DateOfBirth"])
        if r["Outcome"] == "Remanded in custody, EM bail address assessment ordered":
            orders_by_crn[r["CRN"]].append(d)
            orders_by_person[pk].append(d)
        elif r["Outcome"] == "Transferred to the High Court":
            moved_by_crn[r["CRN"]].append(d)
            moved_by_person[pk].append(d)
    leg = rows_xlsx(os.path.join(target, "em_bail_tracker_2025-26.xlsx"), "Tracker")
    case = rows_csv(os.path.join(target, "em_case_system_assessments.csv"))
    ups = rows_csv(os.path.join(target, "em_document_uploads.csv"))
    first_up = {}
    for u in ups:
        if u["DocumentType"] == "EM address assessment report":
            d = local_of_utc(u["UploadedAt"]).date()
            first_up[u["OrderRef"]] = min(d, first_up.get(u["OrderRef"], d))

    def court_order(crn, pk, on_or_before, exact=None):
        """The District Court's order behind a unit's order, or None where the case had gone to the High Court."""
        cands = orders_by_crn.get(crn, []) if crn else orders_by_person.get(pk, [])
        cands = [d for d in cands if d <= on_or_before and (exact is None or d == exact)]
        if cands:
            return max(cands)
        moved = moved_by_crn.get(crn, []) if crn else moved_by_person.get(pk, [])
        assert any(d < on_or_before for d in moved), ("an order with no court order and no transfer", crn, pk)
        return None

    lorders, laddr = {}, defaultdict(set)
    for r in leg:
        key = r["Ref"].split("/")[0]
        lorders.setdefault(key, r)
        laddr[key].add(r["Address"])
    migrated = {}
    done = []
    high_court = 0
    for key, r in lorders.items():
        ref = to_date(r["Referral date"])
        crn = (r["CRN"] or "").strip() if r["CRN"] else ""
        pk = (str(r["Surname"]).upper(), str(r["First name"]).upper(), to_date(r["DOB"]).isoformat())
        od = court_order(crn, pk, ref)
        if r["Status"] == "Completed":
            if od is None:
                high_court += 1
            else:
                done.append((od, to_date(r["Report filed"])))
        else:
            migrated[frozenset(laddr[key])] = od          # carried over: the same addresses in the case system
    corders, caddr = {}, defaultdict(set)
    for r in case:
        corders.setdefault(r["OrderRef"], r)
        caddr[r["OrderRef"]].add(r["Address"])
    for ref, r in corders.items():
        od = dt.date.fromisoformat(r["OrderDate"])
        if od == dt.date(2026, 2, 2) and frozenset(caddr[ref]) in migrated:
            od = migrated.pop(frozenset(caddr[ref]))
        else:
            od = court_order(r["CRN"], None, od, exact=od)
        if od is None:
            high_court += 1
            continue
        assert ref in first_up, ("a District Court order with no report filed", ref)
        done.append((od, first_up[ref]))
    assert not migrated, "every carried-over order found in the case system"
    assert high_court > 0, "the High Court's orders are in the unit's records"
    out = {}
    for ym in MONTHS:
        v = [(rep - od).days for od, rep in done if (od.year, od.month) == ym]
        out["em_%d_%02d" % ym] = sum(v) / len(v)
    return out


def bh_figures(target):
    """Clause 4 on the incident log and the case app's absence records: since the app went live the log records a
    departure and the app's absence record closes it on the resident's return, so a departure that neither a logged
    return nor an absence record closes is the resident leaving."""
    reg = rows_xlsx(os.path.join(target, "bail_house_register_2025-26.xlsx"), "Placements")
    away = rows_xlsx(os.path.join(target, "bail_house_register_2025-26.xlsx"), "Away")
    inc = rows_csv(os.path.join(target, "bail_house_incidents.csv"))
    by = defaultdict(list)
    for e in inc:
        by[e["Placement"]].append((local_of_utc(e["ReportedAt"]), e["Type"]))
    away_by = defaultdict(list)
    for a in away:
        away_by[a["Placement"]].append((to_date(a["Away from"]), to_date(a["Away to (last night away)"]), a["Reason"]))
    went = {"Taken into police custody": "Returned from police custody", "Admitted to hospital": "Returned from hospital",
            "Resident did not return": "Resident returned"}
    nights = {ym: 0 for ym in MONTHS}
    for p in reg:
        pid = p["Placement"]
        ev = sorted(by.get(pid, []))
        first = min(t for t, k in ev if k == "Resident arrived").date()
        assert first >= to_date(p["First night"]), ("the register's first night is never after the arrival", pid)
        away_n, exits, used = set(), [t.date() for t, k in ev if k == "Resident moved out"], set()
        for i, (t, k) in enumerate(ev):
            if k not in went:
                continue
            back = [b for b, kb in ev[i + 1:] if kb == went[k]]
            rows = [a for a in away_by.get(pid, []) if a[0] == t.date() and a[2] != "Approved leave"]
            if back:
                used.update(rows)                   # the app's record of the same absence, where it kept one
                b = min(back)
                d = t.date()
                while True:
                    midnight = dt.datetime(d.year, d.month, d.day, tzinfo=NZT) + dt.timedelta(days=1)
                    if t < midnight < b:
                        away_n.add(d)
                    if midnight >= b:
                        break
                    d += dt.timedelta(days=1)
            elif rows:
                lo, hi, _ = rows[0]
                used.add(rows[0])
                while lo <= hi:
                    away_n.add(lo)
                    lo += dt.timedelta(days=1)
            else:
                exits.append(t.date())              # never back: the day the resident left
        for a in away_by.get(pid, []):
            if a[2] == "Approved leave":
                d, last = a[0], a[1]
                while d <= last:
                    away_n.add(d)
                    d += dt.timedelta(days=1)
            else:
                assert a in used, ("every absence record has its departure in the log", pid, a)
        depart = min(exits) if exits else None
        if depart is not None and p["Left"]:
            assert to_date(p["Left"]) >= depart, ("the register's Left is never before the departure", pid)
        end = depart if depart is not None else P2[1] + dt.timedelta(days=1)
        d = first
        while d < end:
            if P2[0] <= d <= P2[1] and d not in away_n:
                nights[(d.year, d.month)] += 1
            d += dt.timedelta(days=1)
    return {"bh_%d_%02d" % ym: v for ym, v in nights.items()}


def pdf_text(path):
    from pypdf import PdfReader
    t = " ".join((p.extract_text() or "") for p in PdfReader(path).pages)
    return " ".join(t.split())


def documents(target):
    """Each governing document read back through one extractor, a positive control first."""
    want = {
        "budget2027_bid_instructions_halsey_coast.pdf": ["Budget 2027", "every first appearance from police custody",
                                                         "no lawyer of record", "percentage points",
                                                         "assessments of the District Courts' orders"],
        "em_bail_service_standard_v4.pdf": ["Electronically monitored bail", "the day the court orders the assessment",
                                            "filed with the court", "the first assessment report is filed",
                                            "an amended report is a later document"],
        "bail_support_contract_schedule2.pdf": ["Schedule 2", "at the house at midnight",
                                                "police custody or in hospital", "approved leave",
                                                "the night the resident arrives at the house",
                                                "neither starts nor extends a placement",
                                                "ends on the day the resident leaves it",
                                                "although the bed is held for the resident"],
    }
    for f, phrases in want.items():
        t = pdf_text(os.path.join(target, f))
        assert len(t) > 200, ("empty extraction", f)
        for ph in phrases:
            assert ph in t, ("missing", f, ph)


def main(argv):
    target = argv[1] if len(argv) > 1 else os.path.join(TASK, "target")
    documents(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    got = {}
    got.update(main_figures(target))
    got.update(em_figures(target))
    got.update(bh_figures(target))
    units = figs["_units"]
    bad = []
    for k, unit in units.items():
        v = got[k]
        want = figs[k]
        if round(v / unit) != round(float(want) / unit):
            bad.append((k, v, want))
        edge = (unit / 2.0 - abs(v - round(v / unit) * unit)) / unit
        if unit < 1 and edge < 0.07:
            bad.append((k, "edge", round(edge, 3)))
    assert got["region_widening_rest"] <= 0.25 * got["region_widening"], "the AVL split carries the widening"
    for b in bad:
        print("MISMATCH", b)
    print("verify: %d graded figures recomputed from the bundle, %d mismatches" % (len(units), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
