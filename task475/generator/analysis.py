"""Every rung, the golden and every ask figure, computed from target/ alone.

    python3 task475/generator/analysis.py [target_dir]

The main call: each November 2026 Paper 2 optional question's move under regulation 14 (how much harder or easier it
proved than the average question, each counted once, for the candidates who sat the paper), read from the
candidates' marks by a two-way additive fit of candidate and question, and the pass list it gives. The asks: each
centre's withdrawals, absentees and sitters who had sat Paper 2 in May; and the May 2026 reviews (results changed and
fees to refund)."""
import csv
import datetime as dt
import json
import os
import re
import sys
import zlib
import base64

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E  # noqa: E402
import params as PR  # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
SITTING = dt.date(2026, 11, 7)
RELEASE = dt.date(2026, 6, 30)
REVIEW_CLOSE = dt.date(2026, 7, 21)
COMMITTEE = dt.date(2026, 6, 18)


# ---------------------------------------------------------------------------------------------------------------
# reading the pack
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pdf_text(path):
    """Text drawn in a PDF: every content stream decoded (ASCII85 then Flate where filtered) and the strings shown
    by Tj and TJ joined in order."""
    data = open(path, "rb").read()
    out = []
    pos = 0
    while True:
        s = data.find(b"stream", pos)
        if s < 0:
            break
        if data[s - 3:s] == b"end":
            pos = s + 6
            continue
        e = data.find(b"endstream", s)
        head = data[data.rfind(b"obj", 0, s):s]
        body = data[s + 6:e].strip(b"\r\n")
        pos = e + 9
        if b"ASCII85Decode" in head:
            body = body.strip()
            if body.endswith(b"~>"):
                body = body[:-2]
            body = base64.a85decode(body, adobe=False)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        for s in re.finditer(rb"\((?:\\.|[^\\)])*\)\s*Tj|\[(?:[^\]]*)\]\s*TJ", body):
            frag = s.group(0)
            for t in re.finditer(rb"\(((?:\\.|[^\\)])*)\)", frag):
                txt = t.group(1)
                txt = re.sub(rb"\\([0-7]{3})", lambda z: bytes([int(z.group(1), 8)]), txt)
                txt = txt.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\")
                out.append(txt.decode("latin-1"))
            out.append("\n")
    return re.sub(r"[ \t]+", " ", "".join(out))


def docx_text(path):
    """A Word document's paragraphs, then each table row's cells joined by spaces."""
    from docx import Document
    d = Document(path)
    out = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            out.append(" ".join(c.text for c in r.cells))
    return "\n".join(out)


def norm(s):
    return "".join(ch for ch in (s or "").upper() if ch.isalpha())


def sydney_offset(t):
    y = t.year

    def first_sunday(m):
        d = dt.date(y, m, 1)
        while d.weekday() != 6:
            d += dt.timedelta(days=1)
        return dt.datetime(d.year, d.month, d.day, 2, 0)

    # the instant is given in UTC here: convert the change times to UTC
    start = first_sunday(10) - dt.timedelta(hours=10)
    end = first_sunday(4) - dt.timedelta(hours=10)
    return 10 if end <= t < start else 11


def utc_to_sydney(s):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    return t + dt.timedelta(hours=sydney_offset(t))


class Pack:
    def __init__(self, target=TARGET):
        self.target = target
        f = lambda k: os.path.join(target, PR.FILES[k])
        self.export = read_csv(f("export"))
        self.nov_reg = read_csv(f("nov_reg"))
        self.centres = read_csv(f("centres"))
        self.reviews = read_csv(f("reviews"))
        self.invoices = read_csv(f("invoices"))
        self.accounts = read_csv(f("accounts"))
        self.requests = json.load(open(f("requests"), encoding="utf-8"))["requests"]
        import openpyxl
        wb = openpyxl.load_workbook(f("may_reg"), read_only=True)
        ws = wb["Candidates"]
        rows = list(ws.iter_rows(values_only=True))
        hdr = list(rows[0])
        self.may_reg = [dict(zip(hdr, r)) for r in rows[1:]]
        self.regs_text = pdf_text(f("regs"))
        self.paper_text = pdf_text(f("paper"))
        self.minutes_text = docx_text(f("minutes"))


# ---------------------------------------------------------------------------------------------------------------
# marks
def question_of(series, item):
    if series == "NOV26":
        m = re.fullmatch(r"Q(\d\d)\.(\d)", item)
        return int(m.group(1)) - 1, int(m.group(2)) - 1
    m = re.fullmatch(r"(\d)\(([a-d])\)", item)
    return int(m.group(1)) - 1, "abcd".index(m.group(2))


def entered(r):
    return dt.datetime.fromisoformat(r["entered_at"])


def marks_of_record(P, series, until=None):
    """candidate -> question -> mark: the last mark entered for each part (to the end of `until`, Sydney time, when
    given), a part shown as no response counting nothing, summed over the question's parts."""
    last = {}
    for r in P.export:
        if r["series"] != series:
            continue
        t = entered(r)
        if until is not None and t.date() > until:
            continue
        q, k = question_of(series, r["item"])
        key = (r["candidate_no"], q, k)
        if key not in last or t >= last[key][0]:
            last[key] = (t, 0 if r["mark"] == "-" else int(r["mark"]))
    out = {}
    for (c, q, k), (_t, v) in last.items():
        out.setdefault(c, {}).setdefault(q, 0)
        out[c][q] += v
    return out


def matrix(marks):
    cands = sorted(marks, key=int)
    m = np.full((len(cands), 8), np.nan)
    for i, c in enumerate(cands):
        for q, v in marks[c].items():
            m[i, q] = v
    return cands, m


def minutes_moves(P):
    txt = P.minutes_text
    i = txt.index("Move (marks)")
    toks = re.findall(r"[+-]?\d+", txt[i + len("Move (marks)"):])[:8]
    return np.array([int(t) for t in toks])


def minutes_pass(P):
    m = re.search(r"With these moves, (\d+) of the (\d+) candidates", P.minutes_text.replace("\n", " "))
    return int(m.group(1)), int(m.group(2))


# ---------------------------------------------------------------------------------------------------------------
# the main call
def main_call(P):
    cands, m = matrix(marks_of_record(P, "NOV26"))
    fam = {k: f(m) for k, f in E.FAMILY.items()}
    golden = np.rint(fam["fe"]).astype(int)
    fac = E.facility(m)
    rungs = {
        "R0 no moves": np.zeros(8, int),
        "R1 facility": np.rint(fac).astype(int),
        "golden": golden,
    }
    passes = {k: E.passes(m, v) for k, v in rungs.items()}
    moved = E.apply_moves(m, golden)
    tot = np.nansum(moved, axis=1).astype(int)
    rows = []
    for i, c in enumerate(cands):
        rows.append([c] + ["" if np.isnan(moved[i, q]) else int(moved[i, q]) for q in range(8)] +
                    [int(tot[i]), "Pass" if tot[i] >= PR.PASS_MARK else "Fail"])
    return {"cands": cands, "m": m, "family": fam, "facility": fac, "golden": golden, "rungs": rungs,
            "passes": passes, "rows": rows, "n_sat": len(cands), "n_pass": passes["golden"],
            "answered": (~np.isnan(m)).sum(0).astype(int)}


def may_backtest(P):
    marks = marks_of_record(P, "MAY26", until=COMMITTEE)
    cands, m = matrix(marks)
    fam = {k: np.rint(f(m)).astype(int) for k, f in E.FAMILY.items()}
    fac = np.rint(E.facility(m)).astype(int)
    mv = minutes_moves(P)
    return {"minutes": mv, "family": fam, "facility": fac, "pass_fac": E.passes(m, fac), "pass_fe": E.passes(m, fam["fe"]),
            "n": len(cands), "minutes_pass": minutes_pass(P)}


# ---------------------------------------------------------------------------------------------------------------
# ask 1: each centre's withdrawals, absentees and sitters who had sat Paper 2 in May
def nov_sat(P):
    return {r["candidate_no"] for r in P.export if r["series"] == "NOV26"}


def withdrawal_requests(P):
    """applicant -> Sydney time of a request withdrawing the Paper 2 entry."""
    out = {}
    for q in P.requests:
        if q["type"] == "Withdrawal" and "P2" in q["papers"].split(",") and q["status"] == "Actioned":
            t = utc_to_sydney(q["submitted"])
            if q["applicant_id"] not in out or t < out[q["applicant_id"]]:
                out[q["applicant_id"]] = t
    return out


def ask_centres(P, route="golden"):
    sat = nov_sat(P)
    wr = withdrawal_requests(P)
    p2 = [r for r in P.nov_reg if r["paper"] == "P2"]
    codes = [c[0] for c in PR.CENTRES]
    wd = {c: 0 for c in codes}
    ab = {c: 0 for c in codes}
    for r in p2:
        c = r["centre_code"]
        if route == "golden":
            t = wr.get(r["applicant_id"])
            withdrawn = r["status"] == "Withdrawn" and t is not None and t.date() < SITTING
        else:
            withdrawn = r["status"] == "Withdrawn" and dt.date.fromisoformat(r["status_changed"]) < SITTING
        if withdrawn:
            wd[c] += 1
        elif r["candidate_no"] not in sat:
            ab[c] += 1
    may = may_sitters_by_centre(P, route)
    return {c: {"withdrawals": wd[c], "absentees": ab[c], "may_sitters": may[c]} for c in codes}


def may_people(P, route):
    """Paper 2 candidates of the May sitting: (member number, name key) for each one who sat (golden) or who was
    entered and not withdrawn (the register alone)."""
    sat = {r["candidate_no"] for r in P.export if r["series"] == "MAY26"}
    out = []
    for r in P.may_reg:
        if "2" not in str(r["Papers"]):
            continue
        cand = str(r["Cand No"])
        if route == "golden":
            if cand not in sat:
                continue
        elif r["Status"] != "Entered":
            continue
        fam, given = [s.strip() for s in r["Candidate Name"].split(",", 1)]
        dob = dt.datetime.strptime(r["Date of Birth"], "%d/%m/%Y").date()
        out.append({"member": str(r["Member No"] or "").strip(), "key": (norm(fam), norm(given.split()[0]), dob)})
    return out


def may_sitters_by_centre(P, route="golden"):
    may = may_people(P, route)
    members = {x["member"] for x in may if x["member"]}
    keys = {x["key"] for x in may}
    sat = nov_sat(P)
    codes = [c[0] for c in PR.CENTRES]
    out = {c: 0 for c in codes}
    for r in P.nov_reg:
        if r["paper"] != "P2" or r["candidate_no"] not in sat:
            continue
        key = (norm(r["family_name"]), norm(r["given_names"].split()[0]), dt.date.fromisoformat(r["date_of_birth"]))
        hit = key in keys
        if route == "golden" and r["member_no"] and r["member_no"] in members:
            hit = True
        if hit:
            out[r["centre_code"]] += 1
    return out


# ---------------------------------------------------------------------------------------------------------------
# ask 2: the May reviews
def fee_schedule(P):
    txt = P.regs_text
    i = txt.index("Re-mark, per question named")
    a = re.findall(r"\d+\.\d\d", txt[i:i + 120])
    j = txt.index("Clerical check, per script")
    b = re.findall(r"\d+\.\d\d", txt[j:j + 120])
    return {"2025-26": {"remark": float(a[0]), "clerical": float(b[0])},
            "2026-27": {"remark": float(a[1]), "clerical": float(b[1])}}


def may_register_names(P):
    out = {}
    for r in P.may_reg:
        fam = r["Candidate Name"].split(",", 1)[0].strip()
        out[str(r["Cand No"])] = norm(fam)
    return out


def transpositions(s):
    out = set()
    for k in range(len(s) - 1):
        t = list(s)
        t[k], t[k + 1] = t[k + 1], t[k]
        out.add("".join(t))
    return out


def resolve_request(P, row, route):
    typed = row["candidate_no"].strip()
    if route != "golden":
        return typed
    names = may_register_names(P)
    fam = norm(row["family_name"])
    hits = [c for c in [typed] + sorted(transpositions(typed)) if names.get(c) == fam]
    return hits[0] if hits else typed


def may_totals(P, until=None):
    mv = minutes_moves(P)
    marks = marks_of_record(P, "MAY26", until=until)
    out = {}
    for c, qs in marks.items():
        out[c] = sum(int(min(20, max(0, v + mv[q]))) for q, v in qs.items())
    return out


def ask_reviews(P, route="golden"):
    fees = fee_schedule(P)
    disc = {a["account_code"]: float(a["exam_services_discount_pct"]) for a in P.accounts}
    issued = may_totals(P, until=RELEASE)
    final = may_totals(P)
    changed, refund, detail = 0, 0.0, []
    for r in P.reviews:
        t = dt.datetime.strptime(r["received"], "%d/%m/%Y %H:%M")
        declined = t.date() > REVIEW_CLOSE
        cand = resolve_request(P, r, route)
        ch = (not declined) and issued.get(cand, 0) < PR.PASS_MARK <= final.get(cand, 0)
        fy = "2025-26" if t.date() < dt.date(2026, 7, 1) else "2026-27"
        if r["service"] == "Re-mark":
            sched = fees[fy]["remark"] * len([q for q in r["questions"].split(";") if q.strip()])
        else:
            sched = fees[fy]["clerical"]
        if r["payment"] == "Card":
            paid = float(r["amount_aud"])
        elif route == "golden":
            paid = round(sched * (1 - disc[r["account_code"]] / 100.0), 2)
        else:
            paid = sched
        if ch:
            changed += 1
        if ch or declined:
            refund += paid
        detail.append({"request": r["request_no"], "cand": cand, "declined": declined, "changed": ch, "paid": paid,
                       "sched": sched})
    return {"changed": changed, "refund": round(refund, 2), "detail": detail}


def invoice_allocation(P):
    """The fee each account-paid request carries, as its share of its invoice by the schedule fee."""
    fees = fee_schedule(P)
    inv = {r["invoice_no"]: float(r["amount_aud"]) for r in P.invoices}
    by_inv = {}
    for r in P.reviews:
        if r["payment"] != "Account":
            continue
        t = dt.datetime.strptime(r["received"], "%d/%m/%Y %H:%M")
        fy = "2025-26" if t.date() < dt.date(2026, 7, 1) else "2026-27"
        n = len([q for q in r["questions"].split(";") if q.strip()])
        sched = fees[fy]["remark"] * n if r["service"] == "Re-mark" else fees[fy]["clerical"]
        by_inv.setdefault(r["invoice_no"], []).append((r["request_no"], sched))
    out = {}
    for no, items in by_inv.items():
        tot = sum(s for _r, s in items)
        for req, s in items:
            out[req] = round(inv[no] * s / tot, 2)
    return out


def run(target=TARGET):
    P = Pack(target)
    return P, main_call(P), may_backtest(P), ask_centres(P), ask_reviews(P)


if __name__ == "__main__":
    P, M, B, C, R = run(sys.argv[1] if len(sys.argv) > 1 else TARGET)
    print("moves", M["golden"].tolist(), "passes", M["passes"], "sat", M["n_sat"])
    print("May back-test", B["minutes"].tolist(), B["facility"].tolist(), B["family"]["fe"].tolist(), B["pass_fac"],
          B["minutes_pass"])
    print("centres", C)
    print("reviews", R["changed"], R["refund"])
