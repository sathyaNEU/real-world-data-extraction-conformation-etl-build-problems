"""task246 independent verifier: reads only the shipped bundle (target/), the goldens, figures.json and submission.md;
builds the children, the anthropometrists on duty and the standardisation departures by its own code (the normal
distribution through math.erf, the recall start dates read from the protocol's Annex B), recomputes the call, every
zone's two figures and the household figures, reads back every format the pack ships, and requires the goldens and the
write-up to carry the same figures."""
import csv
import datetime as dt
import json
import math
import os
import re
import statistics as st

from openpyxl import load_workbook

CUT, NOTE = 125.0, 2.0


def pdf_text(p):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(p).pages)


def dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def months(dob, day):
    m = (day.year - dob.year) * 12 + day.month - dob.month
    return m - 1 if day.day < dob.day else m


def phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def share(mean, var, n, oed):
    return 100.0 * (oed + n * phi((CUT - mean) / math.sqrt(var))) / (oed + n)


def sheet_rows(path, sheet, header_row):
    ws = load_workbook(path, data_only=True)[sheet]
    rows = list(ws.iter_rows(values_only=True))
    head = list(rows[header_row - 1])
    return [dict(zip(head, r)) for r in rows[header_row:] if any(v is not None for v in r)]


def children(P):
    """(zone, partner, team, day, muac, oedema) for every eligible child, each once"""
    zone = {int(r["cluster"]): r["zone"] for r in csv.DictReader(open(P("lr2027_cluster_sample.csv"), encoding="utf-8"))}
    out, seen = [], set()
    for r in csv.DictReader(open(P("ncha_lr2027_anthropometry.csv"), encoding="utf-8")):
        key = ("NCHA", r["cluster"], r["hh_no"], r["child_no"])
        if key in seen:
            continue
        seen.add(key)
        day = dt.date.fromisoformat(r["today"])
        out.append((zone[int(r["cluster"])], "NCHA", int(r["team"]), day, months(dmy(r["dob"]), day),
                    float(r["muac_mm"]), r["oedema"] == "y"))
    for r in sheet_rows(P("prk_lr2027_anthropometry.xlsx"), "Children", 1):
        key = ("PRK", r["Cluster"], r["HH"], r["Child line"])
        if key in seen:
            continue
        seen.add(key)
        out.append((zone[int(r["Cluster"])], "PRK", int(r["Team"]), dmy(r["Date"]), int(r["Age (months)"]),
                    float(r["MUAC (cm)"]) * 10.0, int(r["Oedema"]) == 1))
    return [c for c in out if 6 <= c[4] <= 59 and (c[6] or 75 <= c[5] <= 220)]


def duty(P):
    """(partner, team) -> the anthropometrist at the start, and the dated takeovers"""
    teams = sheet_rows(P("lr2027_survey_teams.xlsx"), "Teams", 1)
    base = {(r["Partner"], int(r["Team"])): r["Anthropometrist"] for r in teams}
    code = {r["Anthropometrist code"]: r["Anthropometrist"] for r in teams}
    joins = []
    for r in sheet_rows(P("lr2027_survey_teams.xlsx"), "Changes during the round", 1):
        m = re.match(r"(.+?) \((\S+)\) joined team (\d+) as anthropometrist", str(r["Change"]))
        if m:
            joins.append((r["Partner"], int(m.group(3)), dmy(r["Date"]), m.group(1)))
            code[m.group(2)] = m.group(1)

    def who(partner, team, day):
        w = base[(partner, team)]
        for p, t, d, name in joins:
            if p == partner and t == team and day >= d:
                w = name
        return w
    return who, code


def departures(P, code):
    """each anthropometrist's single readings less the supervisor's mean of her two readings of the same test child"""
    rows = list(csv.DictReader(open(P("ncha_lr2027_muac_standardisation.csv"), encoding="utf-8")))
    sup = {}
    for r in rows:
        if r["measured_by"] == "SUPERVISOR":
            sup.setdefault((r["session"], r["test_child"]), []).append(float(r["muac_mm"]))
    dep = {}
    for r in rows:
        if r["measured_by"] != "SUPERVISOR":
            ref = st.mean(sup[(r["session"], r["test_child"])])
            dep.setdefault(code[r["measured_by"]], []).append(float(r["muac_mm"]) - ref)
    for title in ("Session 1 (10 Jun)", "Session 2 (28 Jun)"):
        for r in sheet_rows(P("prk_lr2027_muac_standardisation.xlsx"), title, 4):
            ref = (float(r["Supervisor 1st"]) + float(r["Supervisor 2nd"])) * 10.0 / 2.0
            for k, v in r.items():
                if k and k.endswith((" 1st", " 2nd")) and not k.startswith("Supervisor") and v is not None:
                    dep.setdefault(k[:-4], []).append(float(v) * 10.0 - ref)
    return {a: (st.mean(d), st.variance(d)) for a, d in dep.items()}


def zone_figures(kids, who, err):
    out = {}
    for z in sorted({k[0] for k in kids}):
        ks = [k for k in kids if k[0] == z]
        oed = sum(k[6] for k in ks)
        rest = [k for k in ks if not k[6]]
        x = [k[5] for k in rest]
        a = [who(k[1], k[2], k[3]) for k in rest]
        y = [xi - err[ai][0] for xi, ai in zip(x, a)]
        read = share(st.mean(x), st.variance(x), len(x), oed)
        own = share(st.mean(y), st.variance(y) - st.mean(err[ai][1] for ai in a), len(y), oed)
        out[z] = (read, own)
    return out


def recall_starts(proto):
    out = {}
    for sub in ("Laga North", "Laga Central", "Laga East", "Laga West"):
        m = re.search(sub + r" [A-Za-z\- ]+? (\d{1,2} [A-Z][a-z]+ 2027)", proto.split("Annex B. Recall period start events")[1])
        out[sub] = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
    return out


def households(P, proto):
    """each zone's response rate, crude and under-five death rates: the outcome and reason codes read for the form
    version each day's records were made on, the switch found where the households coded 3 stop being visited again"""
    sample = list(csv.DictReader(open(P("lr2027_cluster_sample.csv"), encoding="utf-8")))
    zone = {int(r["cluster"]): r["zone"] for r in sample}
    sub = {int(r["cluster"]): r["sub_county"] for r in sample}
    visits = list(csv.DictReader(open(P("lr2027_household_visits.csv"), encoding="utf-8")))
    back = {(r["cluster"], r["hh_no"]) for r in visits if r["visit"] == "2"}
    revisit_day = {}
    for r in visits:
        if r["visit"] == "1" and r["outcome"] in ("3", "4") and (r["cluster"], r["hh_no"]) in back:
            revisit_day.setdefault(r["outcome"], []).append(dmy(r["date"]))
    switch = min(revisit_day["4"])
    assert max(revisit_day["3"]) < switch, "verify: one switch of the outcome codes"
    last = {}
    for r in visits:
        k = (r["cluster"], r["hh_no"])
        if k not in last or int(r["visit"]) > int(last[k]["visit"]):
            last[k] = r
    meaning = lambda r: {"1": "in", "2": "ref", "3": "empty", "4": "abs"}[r["outcome"]] if dmy(r["date"]) >= switch else \
        {"1": "in", "2": "ref", "3": "abs", "4": "empty"}[r["outcome"]]
    resp = {}
    for (c, h), r in last.items():
        o = meaning(r)
        t = resp.setdefault(zone[int(c)], [0, 0])
        if o != "empty":
            t[1] += 1
            t[0] += o == "in"
    start = recall_starts(proto)
    mem, seen = [], set()
    for r in csv.DictReader(open(P("lr2027_household_members.csv"), encoding="utf-8")):
        k = (r["cluster"], r["hh_no"], r["line_no"])
        if k not in seen:
            seen.add(k)
            mem.append(r)
    early = [r for r in mem if dt.date.fromisoformat(r["interview_date"]) < switch and r["left_reason"] in ("3", "4")]
    adult = {c: [float(r["age"]) >= 15 for r in early if r["left_reason"] == c and r["age_unit"] == "years"] for c in "34"}
    died_early = max("34", key=lambda c: sum(adult[c]) / max(1, len([r for r in early if r["left_reason"] == c])))
    hh = {}
    for r in mem:
        day = dt.date.fromisoformat(r["interview_date"])
        died_code = "4" if day >= switch else died_early
        dead = r["status"] == "D" or (r["status"] == "L" and r["left_reason"] == died_code)
        e = hh.setdefault((r["cluster"], r["hh_no"]), {"day": day, "all": [0, 0, 0, 0], "u5": [0, 0, 0, 0]})
        for key in ("all", "u5") if r["age_unit"] == "months" else ("all",):
            v = e[key]
            v[0] += r["status"] == "P"
            v[1] += r["joined"] == "Yes" or r["born"] == "Yes"
            v[2] += r["status"] in ("L", "D")
            v[3] += dead
    for r in csv.DictReader(open(P("lr2027_household_births.csv"), encoding="utf-8")):
        if r["outcome"] == "died":
            for key in ("all", "u5"):
                v = hh[(r["cluster"], r["hh_no"])][key]
                v[1] += 1
                v[2] += 1
                v[3] += 1
    rates = {}
    for (c, h), e in hh.items():
        days = (e["day"] - start[sub[int(c)]]).days
        t = rates.setdefault(zone[int(c)], {"all": [0.0, 0.0], "u5": [0.0, 0.0]})
        for key in ("all", "u5"):
            cur, j, ld, dead = e[key]
            t[key][0] += dead
            t[key][1] += (cur - 0.5 * j + 0.5 * ld) * days
    out = {}
    for z in resp:
        out[z] = (100.0 * resp[z][0] / resp[z][1], 1e4 * rates[z]["all"][0] / rates[z]["all"][1],
                  1e4 * rates[z]["u5"][0] / rates[z]["u5"][1])
    return out


def main(target, golden, figures, submission):
    fig = json.load(open(figures))
    P = lambda f: os.path.join(target, f)
    proto = pdf_text(P("laga_nutrition_surveillance_protocol_v2_1.pdf"))
    assert "differ by 2.0 points or more" in proto and "The supervisor's mean of her two readings" in proto, "verify: protocol"
    eml = open(P("lr2027_figures_request.eml"), encoding="utf-8").read()
    assert eml.startswith("From: ") and "Subject: " in eml, "verify: request"
    pdf_text(P("laga_ewb_bulletin_june_2027.pdf"))
    kids = children(P)
    who, code = duty(P)
    err = departures(P, code)
    Z = zone_figures(kids, who, err)
    name_of = {s["name"]: s for s in fig["zones"]}
    noted = [s["code"] for s in fig["zones"] if abs(round(Z[s["name"]][0], 1) - round(Z[s["name"]][1], 1)) >= NOTE - 1e-9]
    assert noted == fig["call"], ("verify: the call", noted)
    for zname, (read, own) in Z.items():
        s = name_of[zname]
        assert round(read, 1) == s["readings"], ("verify: readings' figure", zname, read)
        assert s["own_range"][0] <= round(own, 1) <= s["own_range"][1], ("verify: own figure", zname, own)
    H = households(P, proto)
    for zname, (resp, cdr, u5) in H.items():
        s = name_of[zname]
        assert (round(resp, 1), round(cdr, 2), round(u5, 2)) == (s["response"], s["cdr"], s["u5dr"]), ("verify: household", zname, resp, cdr, u5)
    # the goldens carry the figures
    wb = load_workbook(os.path.join(golden, "lr2027_muac_measurement_review.xlsx"), data_only=True)
    got = 0
    for row in wb["Zones"].iter_rows(min_row=5, values_only=True):
        if row[0] in name_of:
            s = name_of[row[0]]
            assert (row[4], row[5], row[6], row[7] == "Note") == (s["readings"], s["own"], "%.1f to %.1f" % tuple(s["own_range"]), s["note"]), ("wb", row)
            assert (row[10], row[11], row[12]) == (s["response"], s["cdr"], s["u5dr"]), ("wb household", row)
            got += 1
    assert got == 12, "verify: workbook rows"
    from pypdf import PdfReader
    note_pdf = os.path.join(golden, "lr2027_gam_measurement_note.pdf")
    assert len(PdfReader(note_pdf).pages) == 1, "verify: one page"
    note = pdf_text(note_pdf)
    head = note.split("Two kinds of error")[0]
    for s in fig["zones"]:
        assert (s["name"] in head) == s["note"], ("verify: the note's opening", s["name"])
    sub = open(submission, encoding="utf-8").read()
    for s in fig["zones"]:
        assert "- %s: %.1f; %.1f (%.1f to %.1f); %s" % (s["name"], s["readings"], s["own"], s["own_range"][0],
                                                      s["own_range"][1], "note" if s["note"] else "no note") in sub, ("sub", s["name"])
        for fmt, v in (("- %s %.1f", s["response"]), ("- %s %.2f", s["cdr"]), ("- %s %.2f", s["u5dr"])):
            assert fmt % (s["name"], v) in sub, ("verify: submission household", s["name"])
    print("verify: call (%s), every zone's two figures, response and death rates by its own code, every format read back, "
          "goldens and write-up agree" % ", ".join(noted))


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"),
         os.path.join(task, "generator", "figures.json"), os.path.join(task, "submission.md"))
