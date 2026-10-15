"""Independent verifier for task141. Reads only the shipped bundle (target/) and the goldens, imports no generator
module, and recomputes on its own code path (csv, openpyxl, python-docx and pdfplumber, its own clock rules): the
eligible first appearances, their screens, releases and new-offense arrests; each score's safety rate among the
released (the default path) and for every eligible defendant (the magistrates' leniency gradient at full release);
both tiers; and every ask figure. Then holds figures.json and the golden workbook to them."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np

D1 = dt.timedelta(days=1)
FLOOR = 0.85


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------------------------------- clocks
def _sunday(y, m, k):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (k - 1))


def to_eastern(u):
    """UTC (naive) to Eastern wall time: daylight time from 07:00 UTC on the second Sunday of March to 06:00 UTC on
    the first Sunday of November."""
    a = dt.datetime.combine(_sunday(u.year, 3, 2), dt.time(7))
    b = dt.datetime.combine(_sunday(u.year, 11, 1), dt.time(6))
    return u - dt.timedelta(hours=4 if a <= u < b else 5)


def zulu(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ") if s else None


def midnight_counts(a, b, last_day):
    """The midnight counts (each dated with the day it begins) at which a person held from a to b is in: the 00:00
    of every day after a's date that is before b, up to last_day."""
    if b is None:
        b = dt.datetime.combine(last_day + D1, dt.time(0))
    first = a.date() + D1
    last = b.date() if b > dt.datetime.combine(b.date(), dt.time(0)) else b.date() - D1
    last = min(last, last_day)
    return max(0, (last - first).days + 1)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def r10(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


# ---------------------------------------------------------------------------------------------------- the pack
class Pack:
    def __init__(self, T):
        import openpyxl
        self.T = T
        P = lambda f: os.path.join(T, f)
        names = sorted(os.listdir(T))
        pick = lambda pre: [f for f in names if f.startswith(pre)][0]
        wb = openpyxl.load_workbook(P(pick("magistrate_roster")), data_only=True)
        ws = wb["Magistrates"]
        hdr, self.ini = None, {}
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Magistrate":
                hdr = row
                continue
            if hdr and row and row[1]:
                self.ini[row[1]] = row[2]
        wb = openpyxl.load_workbook(P(pick("offense_code_crosswalk")), data_only=True)
        ws = wb.worksheets[0]
        hdr, self.leg, self.cls = None, {}, {}
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Legacy code":
                hdr = row
                continue
            if hdr and row and row[0]:
                self.leg[str(row[0])] = str(row[1])
                self.cls[str(row[1])] = (str(row[2]), str(row[4]))
        # the misdemeanor classes, from the 2024 policy's guideline table; Appendix B from the draft
        import pdfplumber
        with pdfplumber.open(P(pick("local_bail_policy_2024"))) as pdf:
            txt = "\n".join(p.extract_text() or "" for p in pdf.pages)
        self.misd = set(re.findall(r"Misdemeanor, Class (A1|\d)", txt))
        import docx
        d = docx.Document(P(pick("bail_policy_revision_2027_draft")))
        self.appb = []
        for t in d.tables:
            for r in t.rows[1:]:
                gs, desc = r.cells[0].text.strip(), r.cells[1].text.strip()
                self.appb.append((gs, "any subsection" in desc))
        self.files = {k: P(pick(k)) for k in ("first_appearances_2021", "first_appearances_2024",
                                                "first_appearance_charges", "pas_screens", "jail_bookings",
                                                "state_arrest_extract", "court_case_index", "court_events",
                                                "sentry_point", "halsey_county")}

    def excluded(self, gs):
        return any(gs == s or (anysub and gs.startswith(s + "(")) for s, anysub in self.appb)

    def eligible_code(self, code):
        gs, c = self.cls[code]
        return c in self.misd and not self.excluded(gs)


def first_appearances(pk):
    out = []
    for r in rows(pk.files["first_appearances_2021"]):
        t = dt.datetime.strptime(r["APPEAR_DATE"] + " " + r["APPEAR_TIME"], "%m/%d/%Y %H:%M")
        codes = [pk.leg[c] for c in r["CHARGE_CODES"].split(";")]
        out.append(dict(sid=r["SID"], booking="B%s-%s" % (r["BOOKING_NO"][:2], r["BOOKING_NO"][2:]), t=t,
                        mag=pk.ini[r["MAG"]], cases=[c.replace(" ", "") for c in r["CASE_NOS"].split(";")],
                        codes=codes, det=r["HOLD_OTHER"] == "Y", last=r["DEF_LAST"].upper(),
                        first=r["DEF_FIRST"].upper(), dob=dt.datetime.strptime(r["DOB"], "%m/%d/%Y").date()))
    chg = {}
    for r in rows(pk.files["first_appearance_charges"]):
        c = chg.setdefault(r["fa_id"], ([], []))
        c[0].append(r["offense_code"])
        if r["case_number"] not in c[1]:
            c[1].append(r["case_number"])
    for r in rows(pk.files["first_appearances_2024"]):
        codes, cases = chg[r["fa_id"]]
        out.append(dict(sid=r["sid"], booking=r["booking_number"],
                        t=dt.datetime.strptime(r["appearance_at"], "%Y-%m-%d %H:%M"), mag=r["judicial_official_id"],
                        cases=cases, codes=codes, det=r["detainer_agency"] != "", last=r["defendant_last"].upper(),
                        first=r["defendant_first"].upper(), dob=dt.date.fromisoformat(r["dob"])))
    for f in out:
        f["elig"] = (not f["det"]) and all(pk.eligible_code(c) for c in f["codes"])
    return out


def attach(pk, fas):
    # screens: booking number, else (paper screens) the state number and the next appearance within 12 hours
    by_bk, paper = {}, []
    for r in rows(pk.files["pas_screens"]):
        t = dt.datetime.strptime(r["screened_at"], "%m/%d/%Y %I:%M %p")
        v = (int(r["nca_score"]), int(r["fta_score"]))
        if r["booking_number"]:
            by_bk[r["booking_number"]] = v
        else:
            paper.append((r["sid"], t, v))
    for f in fas:
        f["nca"], f["fta"] = by_bk.get(f["booking"], (None, None))
    by_sid = {}
    for f in sorted(fas, key=lambda x: x["t"]):
        by_sid.setdefault(f["sid"], []).append(f)
    for sid, t, v in paper:
        for f in by_sid.get(sid, []):
            if t <= f["t"] <= t + dt.timedelta(hours=12):
                f["nca"], f["fta"] = v
                break
    # releases: the booking's own row in the jail export, a releasing type within 24 hours
    rel_types = {"WPA", "UNSEC", "CUST", "BOND", "TS", "DISM", "CRTO"}
    jail = rows(pk.files["jail_bookings"])
    newbk = {r["booking_number"]: r for r in jail if r["booking_type"] == "NEW"}
    for f in fas:
        j = newbk[f["booking"]]
        rt = to_eastern(zulu(j["released_utc"])) if j["released_utc"] else None
        f["rel_t"] = rt
        f["rel"] = j["release_type"] in rel_types and rt is not None and rt <= f["t"] + dt.timedelta(hours=24)
    return jail


def outcomes(pk, fas):
    disp = {r["case_number"]: r["disposition_date"] for r in rows(pk.files["court_case_index"])}
    offs, seen = {}, set()
    for r in rows(pk.files["state_arrest_extract"]):
        if r["arrest_type"] != "NEW" or r["arrest_id"] in seen:
            continue
        seen.add(r["arrest_id"])
        offs.setdefault(r["sid"], []).append(dt.date.fromisoformat(r["offense_date"]))
    for f in fas:
        if not f["rel"]:
            f["y"] = None
            continue
        a = f["rel_t"].date()
        e = a + dt.timedelta(days=365)
        ds = [disp.get(c, "") for c in f["cases"]]
        if all(ds):
            e = min(e, max(dt.date.fromisoformat(x) for x in ds))
        f["y"] = int(any(a < o <= e for o in offs.get(f["sid"], [])))


def estimates(fas):
    lo, hi = dt.date(2021, 10, 1), dt.date(2025, 9, 30)
    hist = [f for f in fas if f["elig"] and f["nca"] is not None and lo <= f["t"].date() <= hi]
    naive, grad, n, rel = {}, {}, {}, {}
    for s in range(1, 7):
        g = [f for f in hist if f["nca"] == s]
        n[s] = len(g)
        rr = [f for f in g if f["rel"]]
        rel[s] = len(rr) / len(g)
        naive[s] = 1 - sum(f["y"] for f in rr) / len(rr)
        m = {}
        for f in g:
            v = m.setdefault(f["mag"], [0, 0, 0])
            v[0] += 1
            v[1] += int(f["rel"])
            v[2] += f["y"] if f["rel"] else 0
        k = np.array([v[0] for v in m.values()], float)
        R = np.array([v[1] / v[0] for v in m.values()])
        A = np.array([v[2] / v[0] for v in m.values()])
        w = k / k.sum()
        rb, ab = (w * R).sum(), (w * A).sum()
        slope = (w * (R - rb) * (A - ab)).sum() / (w * (R - rb) ** 2).sum()
        grad[s] = 1 - (ab + slope * (1 - rb))
    tier = lambda r: max([0] + [s for s in range(1, 7) if all(r[x] >= FLOOR for x in range(1, s + 1))])
    return dict(hist=hist, naive=naive, grad=grad, n=n, rel=rel, tier_naive=tier(naive), tier=tier(grad),
                mags=len({f["mag"] for f in hist}))


# ---------------------------------------------------------------------------------------------------- the asks
def ask_a(pk, fas, jail):
    """Bed-days in custody: every Eastern midnight from booking to final release, through annex moves, a boarding
    at Halsey and a return, or to Halsey's date out for a defendant released there."""
    import openpyxl
    lo, hi = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
    by_sid = {}
    for r in jail:
        r["b"] = to_eastern(zulu(r["booked_utc"]))
        r["e"] = to_eastern(zulu(r["released_utc"])) if r["released_utc"] else None
        by_sid.setdefault(r["sid"], []).append(r)
    for v in by_sid.values():
        v.sort(key=lambda r: r["b"])
    wb = openpyxl.load_workbook(pk.files["halsey_county"], data_only=True)
    hal = {}
    for ws in wb.worksheets:
        on = False
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Halsey booking":
                on = True
                continue
            if on and row and row[0] and str(row[0]).startswith("HC"):
                h = hal.setdefault(row[0], dict(name=row[1], dob=row[2].date(), din=row[4].date(), dout=None))
                if row[5]:
                    h["dout"] = row[5].date()
    hal_by = {}
    for h in hal.values():
        hal_by.setdefault((h["name"], h["dob"], h["din"]), []).append(h)
    out = {}
    for f in fas:
        if not (lo <= f["t"].date() <= hi) or not f["elig"] or f["nca"] is None or f["rel"]:
            continue
        segs = by_sid[f["sid"]]
        cur = [r for r in segs if r["booking_number"] == f["booking"]][0]
        start, end = cur["b"], None
        while True:
            if cur["release_type"] == "TRF":
                cur = [r for r in segs if r["booking_type"] == "TRF" and r["b"] == cur["e"]][0]
                continue
            if cur["release_type"] == "BO":
                back = [r for r in segs if r["booking_type"] == "BI" and cur["e"] < r["b"] <= cur["e"] + dt.timedelta(days=60)]
                if back:
                    cur = back[0]
                    continue
                h = hal_by[("%s, %s" % (f["last"], f["first"]), f["dob"], cur["e"].date())][0]
                end = dt.datetime.combine(h["dout"], dt.time(12)) if h["dout"] else None
                break
            end = cur["e"]
            break
        out[f["nca"]] = out.get(f["nca"], 0) + midnight_counts(start, end, hi)
    return out


def ask_b(pk, fas):
    """Releases at first appearances from 1 October 2025 to 30 June 2026 followed within 90 days by a
    called-and-failed court date in the appearance's cases or the superior court cases their indictments opened."""
    lo, hi = dt.date(2025, 10, 1), dt.date(2026, 6, 30)
    cont = {}
    for r in rows(pk.files["court_case_index"]):
        if r["district_case_ref"]:
            cont.setdefault(r["district_case_ref"], []).append(r["case_number"])
    fta = {}
    for r in rows(pk.files["court_events"]):
        if r["event_code"] == "FTA":
            fta.setdefault(r["case_number"], []).append(dt.date.fromisoformat(r["event_date"]))
    out = {}
    for f in fas:
        if not (lo <= f["t"].date() <= hi) or not f["rel"] or f["fta"] is None:
            continue
        a = f["rel_t"].date()
        cs = set(f["cases"])
        for c in list(cs):
            cs.update(cont.get(c, []))
        hit = any(a <= d <= a + dt.timedelta(days=90) for c in cs for d in fta.get(c, []))
        v = out.setdefault(f["fta"], [0, 0])
        v[0] += int(hit)
        v[1] += 1
    return out


def ask_c(pk, fas):
    """Calendar days on electronic monitoring to 30 September 2026: each enrollment matched to the release (court
    case number, else name and date of birth and the latest release before it), each day counted once."""
    lo, hi = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
    yr = [f for f in fas if lo <= f["t"].date() <= hi and f["rel"]]
    by_case = {c: f for f in yr for c in f["cases"]}
    by_name = {}
    for f in yr:
        by_name.setdefault((f["last"], f["first"], f["dob"]), []).append(f)
    enr = {}
    for r in rows(pk.files["sentry_point"]):
        e = enr.setdefault(r["participant_no"], dict(last=r["last_name"].upper(), first=r["first_name"].upper(),
                                                      dob=dt.datetime.strptime(r["dob"], "%m/%d/%Y").date(),
                                                      case=r["court_case"],
                                                      s=dt.datetime.strptime(r["enroll_date"], "%m/%d/%Y").date(),
                                                      e=None))
        if r["court_case"]:
            e["case"] = r["court_case"]
        if r["end_date"]:
            e["e"] = dt.datetime.strptime(r["end_date"], "%m/%d/%Y").date()
    days = {}
    for e in enr.values():
        f = by_case.get(e["case"]) if e["case"] else None
        if f is None:
            c = [x for x in by_name.get((e["last"], e["first"], e["dob"]), []) if x["rel_t"].date() <= e["s"]]
            f = max(c, key=lambda x: x["rel_t"]) if c else None
        if f is None or f["nca"] is None:
            continue
        end = e["e"] or hi
        s = days.setdefault(id(f), (f, set()))[1]
        d = e["s"]
        while d <= end:
            s.add(d)
            d += D1
    out = {}
    for f, s in days.values():
        out[f["nca"]] = out.get(f["nca"], 0) + len(s)
    return out


# ---------------------------------------------------------------------------------------------------- the check
def main(target, golden):
    pk = Pack(target)
    fas = first_appearances(pk)
    jail = attach(pk, fas)
    outcomes(pk, fas)
    E = estimates(fas)
    a, b, c = ask_a(pk, fas, jail), ask_b(pk, fas), ask_c(pk, fas)
    figs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    p1 = lambda x: "%.1f" % r1(100 * x)
    bad = []

    def eq(name, got, want):
        if str(got) != str(want):
            bad.append("%s: verifier %s, figures.json %s" % (name, got, want))
    eq("tier", E["tier"], figs["call"]["tier_top_score"])
    eq("default tier", "1 to %d" % E["tier_naive"], figs["default_path"]["tier_scores"])
    for s in range(1, 7):
        eq("full release %d" % s, p1(E["grad"][s]), figs["steps"]["full_release_safety_pct"][str(s)])
        eq("released %d" % s, p1(E["naive"][s]), figs["steps"]["released_safety_pct"][str(s)])
        eq("released share %d" % s, p1(E["rel"][s]), figs["steps"]["released_share_pct"][str(s)])
        eq("history n %d" % s, "{:,}".format(E["n"][s]), figs["steps"]["history_by_score"][str(s)])
        eq("ask A %d" % s, "{:,}".format(r10(a.get(s, 0))), figs["ask_a"][str(s)])
        eq("ask B missed %d" % s, "{:,}".format(b[s][0]), figs["ask_b"][str(s)]["missed"])
        eq("ask B releases %d" % s, "{:,}".format(b[s][1]), figs["ask_b"][str(s)]["releases"])
        eq("ask B share %d" % s, p1(b[s][0] / b[s][1]), figs["ask_b"][str(s)]["share_pct"])
        eq("ask C %d" % s, "{:,}".format(r10(c.get(s, 0))), figs["ask_c"][str(s)])
    eq("magistrates", E["mags"], figs["steps"]["magistrates"])
    if E["grad"][4] >= 0.80 or E["grad"][3] <= 0.90:
        bad.append("shared bounds: score 4 %.4f, score 3 %.4f" % (E["grad"][4], E["grad"][3]))
    # the golden workbook carries the same figures
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden, "presumptive_release_tier_2027.xlsx"), data_only=True)
    ws = wb["Bed-days in custody"]
    for s in range(1, 7):
        eq("book A %d" % s, ws.cell(row=4 + s, column=2).value, r10(a.get(s, 0)))
    ws = wb["Monitoring days"]
    for s in range(1, 7):
        eq("book C %d" % s, ws.cell(row=4 + s, column=2).value, r10(c.get(s, 0)))
    ws = wb["Missed court dates"]
    for s in range(1, 7):
        eq("book B %d" % s, (ws.cell(row=4 + s, column=2).value, ws.cell(row=4 + s, column=3).value,
                             "%.1f" % ws.cell(row=4 + s, column=4).value), (b[s][1], b[s][0], p1(b[s][0] / b[s][1])))
    # the Word documents as Word leaves them: no template part, the statistics their own text gives
    import zipfile
    import docx
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for path in [os.path.join(target, f) for f in sorted(os.listdir(target)) if f.endswith(".docx")] + \
            [os.path.join(golden, f) for f in sorted(os.listdir(golden)) if f.endswith(".docx")]:
        z = zipfile.ZipFile(path)
        extra = [n for n in z.namelist() if n.startswith("customXml/") or n.endswith(("stylesWithEffects.xml",
                                                                                     "thumbnail.jpeg", "numbering.xml"))]
        if extra:
            bad.append("%s carries template parts %s" % (os.path.basename(path), extra))
        body = docx.Document(path).element.body
        words = sum(len("".join(t.text or "" for t in p.iter(ns + "t")).split()) for p in body.iter(ns + "p"))
        app = z.read("docProps/app.xml").decode()
        eq("%s words" % os.path.basename(path), re.search(r"<Words>(\d+)</Words>", app).group(1), words)
    if bad:
        raise SystemExit("verify.py: %d mismatches\n  " % len(bad) + "\n  ".join(bad))
    print("verify.py: the call (top score %d, against %d on the released defendants' rate), %d scores' full-release "
          "and released rates, and all 30 ask figures recomputed from the bundle on an independent path; figures.json "
          "and the golden workbook agree; the Word documents carry no template part and count their own words"
          % (E["tier"], E["tier_naive"], 6))


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden"))
