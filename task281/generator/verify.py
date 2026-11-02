"""Independent verifier: recomputes every graded figure from target/ on its own code path (csv.DictReader,
pypdf for the PDFs, a queue-membership test for the counterfactual offers instead of the analysis's recipient
tags, its own ISBN handling and its own licence meter) and compares with figures.json.

    python3 verify.py [target_dir] [figures.json]
"""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

import openpyxl
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LON = ZoneInfo("Europe/London")
Z = dt.timezone.utc


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def rows(path, delim=","):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=delim))


def pdf_lines(path):
    r = pypdf.PdfReader(path)
    out = []
    for p in r.pages:
        out += [x.strip() for x in (p.extract_text() or "").splitlines() if x.strip()]
    return out


def r100(x):
    return int(math.floor(x / 100.0 + 0.5)) * 100


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def schedules(target):
    lines = pdf_lines(find(target, r"^UC-26-114.*\.pdf$"))
    txt = "\n".join(lines)
    s1 = txt.split("Schedule 1. Faculties from 1 August 2026")[1].split("Schedule 2.")[0]
    names = ["Arts and Humanities", "Social Sciences", "Ardmuir Business School", "Law", "Science and Engineering",
             "Life Sciences", "Medicine and Dentistry", "Health Sciences"]
    school_fac = {}
    # pypdf may run a faculty cell into its schools: split on each faculty name standing before a school list
    pos = []
    for n in names:
        for m in re.finditer(r"(?m)^%s(?=\s|$)" % re.escape(n), s1):
            if not re.match(r"\s*\(", s1[m.end():m.end() + 3]):
                pos.append((m.start(), n))
    pos.sort()
    for m in re.finditer(r"\(([A-Z]{4})\)", s1):
        owner = [n for p, n in pos if p < m.start()]
        school_fac[m.group(1)] = owner[-1]
    s2 = txt.split("Schedule 2. Course texts fund codes")[1]
    fund_fac = {}
    parts = re.split(r"(?m)^(CT-[A-Z]+)\s*", s2)
    for i in range(1, len(parts) - 1, 2):
        code, body = parts[i], parts[i + 1]
        if code == "CT-CORE":
            continue
        last = [n for n in names if body.rstrip().endswith(n)]
        fund_fac[code] = max(last, key=len)
    return school_fac, fund_fac


def main_call(target):
    school_fac, fund_fac = schedules(target)
    H = rows(find(target, r"^shelfmark_holds_.*\.csv$"))
    C = rows(find(target, r"^shelfmark_checkouts_.*\.csv$"))
    by_title = collections.defaultdict(list)
    for h in H:
        h["_p"], h["_o"], h["_c"] = ts(h["placed_at"]), ts(h["offer_made_at"]), ts(h["status_changed_at"])
        by_title[h["title_id"]].append(h)
    frees = collections.defaultdict(collections.Counter)
    for c in C:
        if c["ended_at"]:
            frees[c["title_id"]][ts(c["ended_at"])] += 1
    for h in H:
        if h["status"] == "Offer expired":
            frees[h["title_id"]][h["_c"]] += 1
    free_sorted = {t: sorted(v.items()) for t, v in frees.items()}
    extract = max(max(h["_p"] for h in H), max(ts(c["checked_out_at"]) for c in C))

    def cf(h):
        """first instant after the cancellation at which more copies came free than earlier-placed holds were
        still waiting for one"""
        earlier = [g for g in by_title[h["title_id"]] if g["_p"] < h["_p"]]
        for t, k in free_sorted.get(h["title_id"], []):
            if t <= h["_c"]:
                continue
            waiting = 0
            for g in earlier:
                if g["_p"] >= t:
                    continue
                if g["_o"] is not None:
                    if g["_o"] >= t:
                        waiting += 1
                elif g["status"].startswith("Cancelled"):
                    if g["_c"] > t:
                        waiting += 1
                else:
                    waiting += 1
            if waiting < k:
                return t
        return None

    hw = collections.defaultdict(float)
    n = collections.Counter()
    for h in H:
        if h["patron_type"] == "Staff":
            continue
        d = h["_p"].astimezone(LON).date()
        if not (dt.date(2026, 1, 12) <= d <= dt.date(2026, 4, 26)):
            continue
        fac = school_fac[h["department_code"].rsplit("-", 1)[1].upper()]
        n[fac] += 1
        if h["_o"] is not None:
            end = h["_o"]
        elif h["status"].startswith("Cancelled"):
            end = cf(h) or (h["_p"] + dt.timedelta(days=200))
        else:
            end = extract
        w = (end - h["_p"]).total_seconds() / 86400.0
        hw[fac] += max(0.0, min(w, 84.0) - 14.0) / 7.0
    tot = sum(hw.values())
    return {f: dict(holds=n[f], hw=hw[f], amount=180000.0 * hw[f] / tot) for f in n}, fund_fac, school_fac


def isbn13(s):
    s = re.sub(r"[^0-9X]", "", (s or "").upper())
    if len(s) == 10:
        b = "978" + s[:9]
        return b + str((10 - sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(b)) % 10) % 10)
    return s


def asks(target, fund_fac, school_fac):
    cat = rows(find(target, r"^alma_.*\.csv$"))
    by_mms = {r["mms_id"]: r for r in cat}
    by_isbn = {r["isbn"]: r for r in cat}
    # a work: the e-book reachable through related-record and preceding-edition links in either direction
    nbr = collections.defaultdict(set)
    for r in cat:
        for o in (r["related_record_mms"], r["preceding_edition_mms"]):
            if o:
                nbr[r["mms_id"]].add(o)
                nbr[o].add(r["mms_id"])

    def ebook(mms):
        seen, stack = set(), [mms]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            if by_mms.get(x, {}).get("shelfmark_title_id"):
                return by_mms[x]
            stack += list(nbr[x])
        return None
    wb = openpyxl.load_workbook(find(target, r"^course_catalogue.*\.xlsx$"), read_only=True)
    course_school = {}
    for ws in wb.worksheets:
        for r in list(ws.iter_rows(values_only=True))[1:]:
            course_school[r[0]] = r[2]
    items = rows(find(target, r"^leganto_.*\.csv$"))
    for it in items:
        it["_fac"] = school_fac[course_school[it["course_code"]]]
        rec = by_isbn.get(isbn13(it["isbn"]))
        it["_eb"] = ebook(rec["mms_id"]) if rec else None
        it["_ed"] = int(re.match(r"\d+", it["edition"]).group(0))
    pk_titles = {}
    for fn in os.listdir(target):
        if fn.endswith("_kbart.txt"):
            ks = rows(os.path.join(target, fn), "\t")
            s = set()
            for k in ks:
                rec = by_isbn.get(isbn13(k["online_identifier"]))
                if rec and rec["shelfmark_title_id"]:
                    s.add(rec["shelfmark_title_id"])
            pk_titles[fn] = s
    wb = openpyxl.load_workbook(find(target, r"^erm_licence_register.*\.xlsx$"), read_only=True)
    lic = list(wb["Licences"].iter_rows(values_only=True))
    lh = lic[0]
    lic = [dict(zip(lh, r)) for r in lic[1:]]
    pk = list(wb["Packages"].iter_rows(values_only=True))
    pk = [dict(zip(pk[0], r)) for r in pk[1:]]

    def kbart_of(name):
        best = [fn for fn in pk_titles if all(w.lower() in fn.lower() for w in re.findall(r"[A-Za-z]+", name)[:1])]
        return best

    # package name -> KBART title set: match on the package's own titles appearing in its KBART file
    pk_set = {}
    for p in pk:
        cands = [fn for fn in pk_titles if p["Publisher"].split()[0].lower() in fn.lower()]
        assert len(cands) == 1, (p["Package"], cands)
        pk_set[p["Package"]] = pk_titles[cands[0]]

    # A
    rates = {r["month"]: (float(r["EUR_per_GBP"]), float(r["USD_per_GBP"])) for r in
             rows(find(target, r"^finance_office_monthly_rates.*\.csv$"))}
    fac_titles = collections.defaultdict(set)
    for it in items:
        if it["importance"] == "Essential" and it["teaching_period"].startswith("2025-26") and it["_eb"]:
            fac_titles[it["_fac"]].add(it["_eb"]["shelfmark_title_id"])
    spend = collections.defaultdict(float)
    for ln in rows(find(target, r"^agresso_invoice_lines.*\.csv$")):
        d = dt.datetime.strptime(ln["invoice_date"], "%d/%m/%Y").date()
        if not (dt.date(2026, 1, 1) <= d <= dt.date(2026, 10, 31)):
            continue
        amt = float(ln["net_amount"])
        if ln["currency"] != "GBP":
            e, u = rates["%04d-%02d" % (d.year, d.month)]
            amt = amt / (e if ln["currency"] == "EUR" else u)
        if ln["fund_code"] == "CT-CORE":
            p = [p for p in pk if p["PO line"] == ln["po_line"]][0]
            cnt = {f: len(fac_titles[f] & pk_set[p["Package"]]) for f in fac_titles}
            tot = sum(cnt.values())
            for f, c in cnt.items():
                spend[f] += amt * c / tot
        else:
            spend[fund_fac[ln["fund_code"]]] += amt
    # B
    day = dt.date(2026, 1, 12)

    def as_d(v):
        return v.date() if isinstance(v, dt.datetime) else v
    lendable = set(r["Platform title ID"] for r in lic if as_d(r["Order date"]) <= day)
    for p in pk:
        if as_d(p["Access from"]) <= day <= as_d(p["Access to"]):
            lendable |= pk_set[p["Package"]]
    unc = collections.Counter()
    for it in items:
        if it["importance"] != "Essential" or it["teaching_period"] != "2025-26 Semester 2":
            continue
        eb = it["_eb"]
        ok = bool(eb) and int(re.match(r"\d+", eb["edition"]).group(0)) >= it["_ed"] and \
            eb["shelfmark_title_id"] in lendable
        if not ok:
            unc[it["_fac"]] += 1
    # C: replay the meter title by title
    status = {r["licence_id"]: int(r["loans_remaining"]) for r in rows(find(target, r"^shelfmark_licence_status.*\.csv$"))}
    end_oct30 = dt.datetime(2026, 10, 31, tzinfo=LON)
    first = dt.date(2025, 9, 1)
    metered = collections.defaultdict(list)
    for r in lic:
        if r["Licence model"] != "1 user, 40 loans":
            continue
        od = as_d(r["Order date"])
        x = dict(id=r["Licence ID"], od=od, ref=r["PO line"], renewal=r["Order type"] == "Renewal",
                 fac=fund_fac.get(r["Fund code"]) if r["Fund code"] else None, out_until=None, gone=None,
                 start=None, left=40)
        if od < first:
            x["start"] = dt.datetime(od.year, od.month, od.day, tzinfo=LON)
            if x["id"] in status:
                x["left"] = status[x["id"]]
            else:
                x["gone"], x["left"] = x["start"], 0          # not in force when the record began
        elif not x["renewal"]:
            x["start"] = dt.datetime(od.year, od.month, od.day, tzinfo=LON)
        metered[r["Platform title ID"]].append(x)
    for t, ls in metered.items():
        lapsed_before = [x for x in ls if not x["renewal"] and x["gone"] is not None]
        for x in ls:
            if x["renewal"] and x["od"] < first and lapsed_before:
                x["fac"] = lapsed_before[0]["fac"]
    loans = collections.defaultdict(list)
    for c in rows(find(target, r"^shelfmark_checkouts_.*\.csv$")):
        s_ = ts(c["checked_out_at"])
        if s_ < end_oct30:
            loans[c["title_id"]].append((s_, ts(c["ended_at"])))
    held = collections.Counter()
    far = dt.datetime(2100, 1, 1, tzinfo=Z)
    for t, ls in metered.items():
        due = []

        def raise_relicences(upto):
            due.sort(key=lambda z: z[0])
            while due and due[0][0] <= upto:
                e0, x0 = due.pop(0)
                day = e0.astimezone(LON).date()
                nxt = sorted([y for y in ls if y["renewal"] and y["od"] == day and y["start"] is None],
                             key=lambda y: y["ref"])
                if nxt:
                    nxt[0]["start"], nxt[0]["fac"] = e0, x0["fac"]
        for s_, e in sorted(loans.get(t, [])):
            raise_relicences(s_)
            cand = [x for x in ls if x["start"] is not None and x["start"] <= s_ and x["gone"] is None
                    and x["left"] > 0 and (x["out_until"] is None or x["out_until"] <= s_)]
            if not cand:
                continue
            x = min(cand, key=lambda x: (x["start"], x["od"], x["id"]))
            x["left"] -= 1
            x["out_until"] = e or far
            if x["left"] == 0:
                x["gone"] = e or far
                if e is not None:
                    due.append((e, x))
        raise_relicences(far)
        for x in ls:
            if x["start"] is not None and x["start"] <= end_oct30 and (x["gone"] is None or x["gone"] > end_oct30):
                held[x["fac"]] += x["left"]
    return spend, unc, held


def main(argv):
    target = argv[1] if len(argv) > 1 else os.path.join(TASK, "target")
    figp = argv[2] if len(argv) > 2 else os.path.join(HERE, "figures.json")
    figs = json.load(open(figp))
    res, fund_fac, school_fac = main_call(target)
    spend, unc, held = asks(target, fund_fac, school_fac)
    bad = []
    n = 0
    for name, r in res.items():
        for key, got, want in (("amount", r100(r["amount"]), figs["call"][name]),
                               ("holds", r["holds"], figs["holds"][name]),
                               ("hold-weeks", r100(r["hw"]), figs["hold_weeks"][name]),
                               ("spend", r100(spend[name]), figs["spend"][name]),
                               ("uncovered", unc[name], figs["uncovered"][name]),
                               ("metered", held[name], figs["metered"][name])):
            n += 1
            if got != want:
                bad.append("%s %s: verifier %s, figures.json %s" % (name, key, got, want))
    # positive controls: the verifier must also see what the analysis rejects
    total_holds = sum(r["holds"] for r in res.values())
    n += 1
    if "{:,}".format(total_holds) != figs["holds_total"]:
        bad.append("holds total %d against %s" % (total_holds, figs["holds_total"]))
    for b in bad:
        print("MISMATCH", b)
    print("verify: %d figures compared, %d mismatches" % (n, len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
