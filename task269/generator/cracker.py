"""task269's cracker and mirror, run on the cut pack: the ask figures a response files on each path, scored against
generator/figures.json, and the pair ceiling on the weights the bar was set on (supplemental-stumping Part 0:
38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 cracker.py <target>

The cracker lands the call (15 stations) and works the asks the careful way that executes the filed rules: policy
4.4 by the bank's status, its review dates read day first and the sittings joined on the case code; policy 5.2 by
the register's grade, status and training dates, the availability responses matched on email and then on the name
without titles, accents or punctuation, the latest response standing. The mirror stops at the default rung
(12 stations) and works the asks the same way, since neither ask reads anything the call computes. The other
routes are the over-cleaners and the careless readers each device is aimed against."""
import csv
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V   # noqa: E402

DOMAINS = V.DOMAINS
SESS = V.SESS


def a_by_code(t, title_match=False, month_first=False):
    cases = V.rows_xlsx(os.path.join(t, "case_bank_export_2026-11-30.xlsx"), "Cases")
    exposed = set()
    with open(os.path.join(t, "case_usage_history_2021_2026.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if int(r["sitting_date"][:4]) in (2025, 2026):
                exposed.add(r["case_code"])
    titles = {(c["Blueprint domain"], c["Title"]) for c in cases if c["Case code"] in exposed}

    def rev(x):
        if isinstance(x, (dt.date, dt.datetime)):
            return x.date() if isinstance(x, dt.datetime) else x
        a, b, y = (int(p) for p in str(x).split("/"))
        if month_first:
            try:
                return dt.date(y, a, b)
            except ValueError:
                return dt.date(y, b, a)
        return dt.date(y, b, a)
    out = {}
    for d in DOMAINS:
        el = [c for c in cases if c["Blueprint domain"] == d and c["Status"] in ("Active", "Active - edits pending")
              and rev(c["Last reviewed"]) >= dt.date(2024, 5, 11) and c["Case code"] not in exposed
              and not (title_match and (d, c["Title"]) in titles)]
        out[d] = (len(el), sum(1 for c in el if c["Resources"] in ("SP", "SP and task trainer")))
    return out


def b_by_register(t, initial_only=False, no_dedup=False, email_only=False):
    reg = V.rows_xlsx(os.path.join(t, "examiner_register_2026-11-30.xlsx"))
    by_email = {r["Email"].lower(): r["Staff no."] for r in reg}
    by_name = {}
    for r in reg:
        by_name.setdefault(V.norm_name("%s %s" % (r["Forename"], r["Surname"])), []).append(r["Staff no."])
    grades = {"Professor", "Associate Professor", "Senior Lecturer", "Lecturer", "Consultant", "GP Trainer"}
    ok = set()
    for r in reg:
        dates = [V.bank_date(r["Examiner training"])]
        if r["Last refresher"] and not initial_only:
            d = V.bank_date(r["Last refresher"])
            if d <= dt.date(2026, 12, 7):
                dates.append(d)
        if r["Status"] == "Active" and r["Grade"] in grades and max(dates) >= dt.date(2023, 12, 7):
            ok.add(r["Staff no."])
    resp = []
    with open(os.path.join(t, "examiner_availability_2027_responses.csv"), newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            staff = by_email.get(r[1].lower())
            if staff is None and not email_only:
                hits = by_name.get(V.norm_name(r[2]), [])
                staff = hits[0] if len(hits) == 1 else None
            if staff is None:
                continue
            resp.append((dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M:%S"), staff, V.SITES[r[3]],
                         {s: r[4 + k] == "Yes" for k, s in enumerate(SESS)}))
    if not no_dedup:
        latest = {}
        for x in resp:
            if x[1] not in latest or x[0] > latest[x[1]][0]:
                latest[x[1]] = x
        resp = list(latest.values())
    out = {}
    for site in ("CSC", "CUH", "FCS"):
        for s in SESS:
            out[(site, s)] = sum(1 for (_, st, si, ti) in resp if st in ok and si == site and ti[s])
    return out


def score(fig, a, b):
    hits = [d for d in DOMAINS if a[d][0] == fig["ask_a"][d][0]] + \
           [d + " SP" for d in DOMAINS if a[d][1] == fig["ask_a"][d][1]] + \
           ["%s %s" % k for k, v in b.items() if v == fig["ask_b"]["%s %s" % k]]
    return hits


def run(t, quiet=False):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    n_ask = 2 * len(DOMAINS) + 12
    routes = {
        "cracker (lands the call; code join, register dates)": (a_by_code(t), b_by_register(t)),
        "title matcher, register dates": (a_by_code(t, title_match=True), b_by_register(t)),
        "month-first review dates": (a_by_code(t, month_first=True), b_by_register(t)),
        "initial training only": (a_by_code(t), b_by_register(t, initial_only=True)),
        "every response counted": (a_by_code(t), b_by_register(t, no_dedup=True)),
        "email matches only": (a_by_code(t), b_by_register(t, email_only=True)),
    }
    res = {}
    for name, (a, b) in routes.items():
        h = score(fig, a, b)
        res[name] = h
        if not quiet:
            print("%-52s ask figures hit %2d of %d %s" % (name, len(h), n_ask, h))
            print("    A", a)
            print("    B", {"%s %s" % k: v for k, v in b.items()})
    crack = res["cracker (lands the call; code join, register dates)"]
    cracker = 38 + 7 + 55 * len(crack) / n_ask
    mirror = 5 + 7 + 55 * len(crack) / n_ask
    leak = 100.0 * len(crack) / n_ask
    if not quiet:
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" %
              (cracker, mirror, (cracker + mirror) / 2, leak))
    return {"routes": res, "pair": (cracker + mirror) / 2, "leak": leak, "n_ask": n_ask}


if __name__ == "__main__":
    run(sys.argv[1])
