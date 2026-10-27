"""task157 (architecture 2) the analysis, computed from the shipped bundle only.

Every figure the goldens, `figures.json` and `submission.md` carry comes from here, and `checks.py` runs the
rungs through the same functions. `verify.py` recomputes all of it from the same files on its own code path
with pandas and no generator import.

The projection: the office filed 540,000 signature lines and the statute's sample is five per cent of them,
so the sample's own factor is twenty. A signature struck on a ground that belongs to the one signature in
front of the recorder is one of twenty such lines in the petition. A signature struck as a duplicate is not:
a duplicate is a relation between two signature lines, and only the sampled part of the petition was ever
keyed, so the pair was available to be found only where the sample drew both of its members, which happens
with probability one in four hundred."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import records as R     # noqa: E402


def rd(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------------- conforming the returns
def parse_date(county_code, text):
    """Each recorder's return carries dates the way its own system writes them."""
    t = (text or "").strip()
    if not t:
        return None
    if county_code == K.DMY_COUNTY:
        d, m, y = t.split("/")
        return dt.date(int(y), int(m), int(d))
    if county_code == K.OLD_CODE_COUNTY:
        d, mon, y = t.split("-")
        return dt.date(2000 + int(y), K.UMON3.index(mon.upper()), int(d))
    return dt.date(*(int(x) for x in t.split("-")))


def key(row):
    return (row["circulator_reg_no"], int(row["sheet_no"]), int(row["line_no"]))


def conform(target):
    """The fifteen recorders' returns on one code set and one date convention, with the division's own
    correction notices applied line by line."""
    rows = rd(target, R.F_RETURNS)
    late = {int(r["voter_reg_id"]): r for r in rd(target, R.F_SNAP_LATE)}
    corr = {}
    for c in rd(target, R.F_CORR):
        corr[(c["circulator_reg_no"], int(c["sheet_no"]), int(c["line_no"]))] = c
    out = []
    for r in rows:
        cc = r["county_code"]
        code = r["disposition_code"]
        k = key(r)
        if k in corr:
            code = corr[k]["corrected_disposition_code"]
        code = to_current(cc, code, r, late)
        out.append(dict(county=cc, circ=r["circulator_reg_no"], sheet_no=int(r["sheet_no"]),
                        line_no=int(r["line_no"]), vid=(int(r["voter_reg_id"]) if r["voter_reg_id"] else 0),
                        code=code, determined_by=r["determined_by"],
                        signed=parse_date(cc, r["signature_date"]), return_id=r["return_id"],
                        raw_code=r["disposition_code"]))
    return out


def to_current(county_code, code, row, late):
    """Navajo County's recorder files on its own 2019 list. Its code 02 covers two grounds that the current
    set keeps apart, and the registration the recorder matched separates them: a signature struck because
    the signer was not registered at all carries no registration identifier, and one struck because the
    registration had been cancelled carries the cancelled registration."""
    if county_code != K.OLD_CODE_COUNTY:
        return code
    if code == "02":
        return "CA" if row["voter_reg_id"] else "NR"
    news = K.OLD_TO_NEW[code]
    assert len(news) == 1, code
    return news[0]


# ---------------------------------------------------------------------------------- the projection
# Both are exact integers by construction: the statute's sample is one line in twenty, so a single
# signature ground carries twenty lines and a pair, which the sample sees only when it draws both of its
# members, carries four hundred. Computing them in floating point costs a signature to rounding.
FACTOR = K.LINES_FILED // K.SAMPLE_LINES                # 20, the sample's own factor
PAIR_FACTOR = FACTOR * FACTOR                           # 400, one over the pair's inclusion probability
assert FACTOR * K.SAMPLE_LINES == K.LINES_FILED


def tally(rows):
    out = {c: 0 for c in K.CODE_KEYS}
    for r in rows:
        out[r["code"]] += 1
    out["single"] = sum(out[c] for c in K.SINGLE_CODES)
    out["dup"] = out["DU"]
    return out


def project(single, dup_estimate):
    return K.LINES_FILED - single * FACTOR - dup_estimate


def call(rows):
    t = tally(rows)
    single_proj = t["single"] * FACTOR
    dup_proj = t["dup"] * PAIR_FACTOR
    valid = K.LINES_FILED - single_proj - dup_proj
    return dict(sampled=len(rows), single=t["single"], dup=t["dup"], valid_sampled=t["V"],
                single_projected=single_proj, dup_projected=dup_proj, valid=valid,
                printed=K.round_to(valid, K.BIN), pct=100.0 * valid / K.REQUIRED, band=K.band(valid),
                tally=t)


def rungs(target, rows):
    """The ladder, each rung computed from the bundle."""
    t = tally(rows)
    early = {int(r["voter_reg_id"]): r for r in rd(target, R.F_SNAP_EARLY)}
    # rung 0: the registration grounds re-derived from the snapshot current when circulation opened, which
    # still shows the registrations the 14 March run cancelled as active
    slip = 0
    for r in rows:
        if r["code"] != "CA":
            continue
        e = early.get(r["vid"])
        if e is not None and e["registration_status"] == "ACTIVE":
            slip += 1
    county_dup = sum(1 for r in rows if r["code"] == "DU" and r["determined_by"] == "RECORDER")
    division_dup = t["dup"] - county_dup
    return dict(
        slip=slip, county_dup=county_dup, division_dup=division_dup,
        rung0=project(t["single"] - slip, t["dup"] * FACTOR),
        rung1=project(t["single"], t["dup"] * FACTOR),
        rung2=project(t["single"], county_dup * FACTOR + division_dup * PAIR_FACTOR),
        rung3=project(t["single"], t["dup"] * PAIR_FACTOR),
    )


# ---------------------------------------------------------------------------------- the full count's size
def closeout(target):
    """The 2024 full count's own record: the only settled measure the office has of what examining a
    petition line by line costs."""
    import postprocess as PP
    rows = PP.read_xlsx_rows(os.path.join(target, R.F_CLOSEOUT), "Full count")
    head = {r[0]: r[1] for r in rows if len(r) >= 2 and isinstance(r[0], str)}
    lines = int(head["Signature lines examined"])
    days = int(head["Examination business days"])
    staff = int(head["Examiners assigned"])
    rate = lines / float(days * staff)
    need = K.LINES_FILED / rate
    examiners = 30
    bdays = int(math.ceil(need / examiners))
    d, left = K.FULL_COUNT_START, bdays
    while left > 1:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            left -= 1
    return dict(prior_lines=lines, prior_days=days, prior_staff=staff, rate=rate,
                examiner_days=need, examiners=examiners, business_days=bdays, finish=d,
                deadline=K.CERTIFY_BY, inside=d <= K.CERTIFY_BY)


# ---------------------------------------------------------------------------------- the registration state
def reg_state(row, when):
    """Was the registration this snapshot row carries in force on a given date?

    The row carries the registration's own date and the date of a cancellation if one stands against it.
    Where the registration date is the later of the two the registration was re-established, and the
    cancellation no longer takes the elector off on any date after it; where the cancellation is the later,
    the elector was registered from the registration date until the cancellation."""
    if row is None or when is None:
        return False
    reg = row["registration_date"].strip()
    if not reg:
        return False
    reg = dt.date(*(int(x) for x in reg.split("-")))
    if reg > when:
        return False
    canc = row["cancellation_date"].strip()
    if not canc:
        return True
    canc = dt.date(*(int(x) for x in canc.split("-")))
    if reg > canc:
        return True
    return when < canc


def cancelled_now(row):
    return row is not None and row["registration_status"] == "CANCELLED"


def lapsed(rows, late, sel=None):
    """Sampled signatures whose signer was registered on the date the signature was given and whose
    registration the 10 July 2028 snapshot no longer shows as valid."""
    k = 0
    for r in (rows if sel is None else sel):
        if not r["vid"]:
            continue
        e = late.get(r["vid"])
        if reg_state(e, r["signed"]) and cancelled_now(e):
            k += 1
    return k


# ---------------------------------------------------------------------------------- the circulators' firms
def firm_register(target):
    """The office's circulator extract, as the rows a registration number carries in date order."""
    out = {}
    for r in rd(target, R.F_CIRC):
        out.setdefault(r["circulator_reg_no"], []).append(r)
    for v in out.values():
        v.sort(key=lambda r: r["registered_on"])
    return out


def firm_on(reg, circ, when):
    """The firm that had a circulator registered on a date. A circulator who moved firm inside the window
    registered again, so the number carries two rows with their own dates, and a signature belongs to the
    firm that had the circulator registered on the day the signature was given."""
    if when is None:
        return None
    for row in reg.get(circ, []):
        start = dt.date(*(int(x) for x in row["registered_on"].split("-")))
        if start > when:
            continue
        end = row["withdrawn_on"].strip()
        if end and dt.date(*(int(x) for x in end.split("-"))) <= when:
            continue
        return row["firm_registration_no"]
    return None


# ---------------------------------------------------------------------------------- the asks
def sheet_serials(target):
    """The office's serial for each receipted sheet, keyed the way a sampled line identifies its sheet: the
    circulator's registration number with the sheet number the firm printed on it."""
    out = {}
    for s in rd(target, R.F_SHEETS):
        out[(s["circulator_reg_no"], int(s["sheet_no"]))] = s["sheet_serial"]
    return out


def ask_a(target, rows):
    """For each county: the sampled signatures its recorder returned a determination for, and how many of
    those were registered on the day they signed and are no longer shown as valid."""
    late = {int(r["voter_reg_id"]): r for r in rd(target, R.F_SNAP_LATE)}
    out = {}
    for cc, name, _ in K.COUNTIES:
        det = [r for r in rows if r["county"] == cc and r["determined_by"] == "RECORDER"]
        out[cc] = dict(name=name, determined=len(det), lapsed=lapsed(rows, late, det))
    return out


def ask_b(target, rows):
    """For each circulator firm and each month of the circulation period: the sampled signatures gathered by
    circulators that firm had registered on the day the signature was given, and how many of them the
    recorders struck on a ground other than duplication."""
    reg = firm_register(target)
    out = {}
    for fc, name, _, regno in K.FIRMS:
        for y, m in K.WINDOW_MONTHS:
            out[(regno, "%04d-%02d" % (y, m))] = dict(firm=name, signatures=0, struck=0)
    for r in rows:
        if r["signed"] is None or not (K.WINDOW_OPEN <= r["signed"] <= K.WINDOW_CLOSE):
            continue
        f = firm_on(reg, r["circ"], r["signed"])
        if f is None:
            continue
        cell = out[(f, "%04d-%02d" % (r["signed"].year, r["signed"].month))]
        cell["signatures"] += 1
        if r["code"] in K.SINGLE_CODES:
            cell["struck"] += 1
    return out


def ask_c(target, rows):
    """For each month of the circulation period: the sampled signatures signed in it and the petition sheet
    serials they sit on."""
    ser = sheet_serials(target)
    out = {}
    for y, m in K.WINDOW_MONTHS:
        sel = [r for r in rows if r["signed"] is not None
               and (r["signed"].year, r["signed"].month) == (y, m)]
        out["%04d-%02d" % (y, m)] = dict(signatures=len(sel),
                                         sheets=len({ser[(r["circ"], r["sheet_no"])] for r in sel}))
    return out


def everything(target):
    rows = conform(target)
    c = call(rows)
    return dict(rows=rows, call=c, rungs=rungs(target, rows), closeout=closeout(target),
                a=ask_a(target, rows), b=ask_b(target, rows), c=ask_c(target, rows))
