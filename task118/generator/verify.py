"""Independent verifier: reads target.zip only (no generator state, its own code path), takes the policy's filed
figures from the PDF's text, dates each start by the earliest template across both exports, integrates the excess day by
day, rebuilds the stays its own way, and checks figures.json, submission.md and both goldens against what it finds.

    python3 task118/generator/verify.py [target.zip]
"""
import collections
import csv
import datetime as dt
import email
import io
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def rows(z, name):
    return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8"))))


def text_of_pdf(data):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(io.BytesIO(data)).pages))


def months_later(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    y += d.year
    mo += 1
    for day in (d.day, 30, 29, 28):
        try:
            return dt.date(y, mo, day)
        except ValueError:
            continue


def main(zp=None):
    zp = zp or os.path.join(TASK, "target.zip")
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    fails = []

    def check(label, cond, detail=""):
        if not cond:
            fails.append("%s %s" % (label, detail))
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, (" [%s]" % detail) if detail and not cond else ""))

    def one(pattern):
        m = [n for n in names if re.search(pattern, n)]
        assert len(m) == 1, (pattern, m)
        return m[0]

    fig = json.load(open(os.path.join(HERE, "figures.json")))

    # the policy's filed figures, read from the document itself
    pol = text_of_pdf(z.read(one(r"deprescribing_policy.*\.pdf$")))
    base = float(re.search(r"run at ([\d.]+) per 100 patients a year", pol).group(1))
    stop = int(re.search(r"Coming off (\d+) in every 100", pol).group(1)) / 100.0
    under = re.search(r"Under (\d+) months ([\d.]+) (\d+) months to under (\d+) months ([\d.]+) (\d+) months or more "
                      r"([\d.]+)", pol)
    b1, r1, _, b2, r2, _, r3 = under.groups()
    b1, b2, r1, r2, r3 = int(b1), int(b2), float(r1), float(r2), float(r3)
    off = re.search(r"off the drug from (\d+) April (\d{4}) to (\d+) December (\d{4})", pol)
    off_from, off_to = dt.date(int(off.group(2)), 4, int(off.group(1))), dt.date(int(off.group(4)), 12, int(off.group(3)))
    cu = re.search(r"aged (\d+) or over on 1 January (\d{4}) with a benzodiazepine or Z-drug dispensed between 1 July "
                   r"and 30 September (\d{4})", pol)
    age_min, age_year, disp_year = int(cu.group(1)), int(cu.group(2)), int(cu.group(3))
    check("policy read back: base %.1f, stop %.2f, bands %d/%d at %.1f/%.1f/%.1f, off %s to %s" % (
        base, stop, b1, b2, r1, r2, r3, off_from, off_to), (base, stop, b1, b2, r1, r2, r3) == (4.0, 0.45, 6, 24, 3.0, 1.8, 1.1))

    # the register, with the codes each practice has taken over
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(z.read(one(r"register.*\.xlsx$"))), read_only=True)
    ws = wb["Practices"]
    it = ws.iter_rows(values_only=True)
    hdr = next(it)
    loc = {}
    for r in it:
        rec = dict(zip(hdr, r))
        loc[rec["Practice code"]] = rec["Locality code"]
        for code in re.findall(r"[A-Z]\d{5}", str(rec["Previous practice codes"] or "")):
            loc[code] = rec["Locality code"]
    names_of = {}
    for r in wb["Localities"].iter_rows(min_row=2, values_only=True):
        names_of[r[0]] = r[1]
    check("register read back: %d practice codes, %d localities" % (len(loc), len(names_of)), len(names_of) == 6)

    # current users
    disp = rows(z, one(r"^dispensing_.*\.csv$"))
    lo, hi = "%d-07-01" % disp_year, "%d-09-30" % disp_year
    born_by = age_year - 1 - age_min
    cur, where = set(), {}
    for x in disp:
        if lo <= x["dispensed_date"] <= hi and int(x["year_of_birth"]) <= born_by:
            cur.add(x["patient_pseudo_id"])
            where[x["patient_pseudo_id"]] = loc[x["practice_code"]]
    check("current users %d" % len(cur), len(cur) == fig["n_users"], "figures.json %d" % fig["n_users"])

    # first starts: the earliest template across both exports, skipping templates the move re-created
    start = {}
    for t in rows(z, one(r"^repeat_templates_.*\.csv$")):
        if t["migration_source_ref"]:
            continue
        d = dt.date.fromisoformat(t["authorised_from"])
        p = t["patient_pseudo_id"]
        if p not in start or d < start[p]:
            start[p] = d
    for t in rows(z, one(r"previous_system.*\.csv$")):
        d = dt.datetime.strptime(t["StartDate"], "%d/%m/%Y").date()
        p = t["PatientPseudoID"]
        if p not in start or d < start[p]:
            start[p] = d
    check("every current user has a start", all(p in start for p in cur))

    # excess admissions, a day at a time
    days = [off_from + dt.timedelta(days=k) for k in range((off_to - off_from).days + 1)]
    tot = collections.defaultdict(float)
    for p in cur:
        s = start[p]
        e1, e2 = months_later(s, b1), months_later(s, b2)
        ex = 0.0
        for d in days:
            ex += (r1 if d < e1 else (r2 if d < e2 else r3)) - 1.0
        tot[where[p]] += ex / 365.0
    av = {k: stop * base / 100.0 * v for k, v in tot.items()}
    order = sorted(av, key=lambda k: -av[k])
    w, r = order[0], order[1]
    check("the call: %s %.3f, runner-up %s %.3f" % (names_of[w], av[w], names_of[r], av[r]),
          w == fig["winner"] and r == fig["runner"] and abs(av[w] - fig["avoided"]) < 1e-3 and
          abs(av[r] - fig["runner_avoided"]) < 1e-3, "figures.json %s %.3f, %s %.3f" % (
              fig["winner"], fig["avoided"], fig["runner"], fig["runner_avoided"]))
    rw, rr_, rg = int(av[w] + 0.5), int(av[r] + 0.5), int(av[w] - av[r] + 0.5)
    check("rounded: %d, %d, %d fewer" % (rw, rr_, rg), (rw, rr_, rg) == (fig["avoided_r"], fig["runner_avoided_r"],
                                                                          fig["gap_r"]))

    # the falls definitions, read back
    fd = text_of_pdf(z.read(one(r"falls_indicator.*\.pdf$")))
    meth = set(re.search(r"admission method ([\w, ]+?) or (\w\w)\b", fd).group(1).replace(" ", "").split(",")) | {
        re.search(r"admission method ([\w, ]+?) or (\w\w)\b", fd).group(2)}
    window = int(re.search(r"in the (\d+) days after it", fd).group(1))
    check("falls definitions read back: %d methods, %d days" % (len(meth), window), len(meth) == 10 and window == 30)

    # stays rebuilt: walk each patient's spells in time order; a discharge to another hospital (49 to 53, 84, 87)
    # carries the stay into the spell at another site that begins that day or the next
    eps = rows(z, one(r"^sus_.*\.csv$"))
    spell = {}
    for e in eps:
        k = (e["provider_code"], e["hospital_spell_no"])
        s = spell.setdefault(k, {"pid": e["sus_pseudo_id"], "site": e["site_code"], "adm": e["admission_date"],
                                 "method": e["admission_method"], "first": None, "last": None})
        n = int(e["episode_no"])
        if s["first"] is None or n < int(s["first"]["episode_no"]):
            s["first"] = e
        if s["last"] is None or n > int(s["last"]["episode_no"]):
            s["last"] = e
    per = collections.defaultdict(list)
    for s in spell.values():
        s["dis"] = s["last"]["discharge_date"]
        s["dest"] = s["last"]["discharge_destination"]
        s["died"] = s["last"]["discharge_method"] == "4"
        per[s["pid"]].append(s)
    moved = {"49", "50", "51", "52", "53", "84", "87"}
    out = {k: [0, 0, 0, 0] for k in names_of}
    for pid, ss in per.items():
        pool = sorted(ss, key=lambda s: (s["adm"], s["dis"]))
        used, stays = set(), []
        for s in pool:
            if id(s) in used:
                continue
            chain = [s]
            used.add(id(s))
            while chain[-1]["dest"] in moved:
                last = dt.date.fromisoformat(chain[-1]["dis"])
                nxt = [b for b in pool if id(b) not in used and b["site"] != chain[-1]["site"] and
                       0 <= (dt.date.fromisoformat(b["adm"]) - last).days <= 1]
                if not nxt:
                    break
                nxt.sort(key=lambda b: (b["adm"], b["dis"]))
                chain.append(nxt[0])
                used.add(id(nxt[0]))
            stays.append(chain)
        emerg = [c_ for c_ in stays if c_[0]["method"] in meth and c_[0]["method"] not in ("2B", "81")]
        for c_ in stays:
            f = c_[0]["first"]
            codes = [f["primary_diagnosis"]] + [f["diag_%02d" % i] for i in range(2, 9)]
            fall = any(re.fullmatch(r"W(0\d|1\d)\w*", x or "") for x in codes)
            a0 = c_[0]["adm"]
            if not (fall and c_[0]["method"] in meth and "2025-04-01" <= a0 <= "2026-03-31"):
                continue
            k = loc[f["gp_practice_code"]]
            o = out[k]
            o[0 if int(f["age_at_start"]) < 80 else 1] += 1
            end = dt.date.fromisoformat(c_[-1]["dis"])
            o[2] += (end - dt.date.fromisoformat(a0)).days
            if not c_[-1]["died"]:
                if any(x is not c_ and 0 <= (dt.date.fromisoformat(x[0]["adm"]) - end).days <= window for x in emerg):
                    o[3] += 1
    want = {k: [fig["asks"][k][f] for f in ("falls_65_79", "falls_80", "bed_days", "readmitted")] for k in names_of}
    for k in names_of:
        check("falls %s: %s" % (names_of[k], out[k]), out[k] == want[k], "figures.json %s" % want[k])

    # the thread and the goldens read back
    msg = email.message_from_bytes(z.read(one(r"\.eml$")))
    body = msg.get_payload(decode=True).decode("utf-8")
    check("thread read back: %s, %d lines" % (msg["Subject"], body.count("\n")), "placement" in msg["Subject"].lower())
    gx = load_workbook(os.path.join(TASK, "golden", "deprescribing_placement_2027.xlsx"), read_only=True)
    grid = {}
    for row in gx["Falls 2025-26"].iter_rows(min_row=4, values_only=True):
        if row and row[0] in names_of:
            grid[row[0]] = list(row[2:6])
    check("golden workbook carries the 24 falls figures", grid == want)
    from docx import Document
    doc = " ".join(p.text for p in Document(os.path.join(TASK, "golden", "deprescribing_case_2027.docx")).paragraphs)
    check("golden paper names %s, %d avoided, %s at %d, %d fewer" % (names_of[w], rw, names_of[r], rr_, rg),
          ("place the deprescribing team in %s" % names_of[w]).lower() in doc.lower() and
          ("avoid %d emergency admissions" % rw) in doc and ("%s is the runner-up at %d, %d fewer" % (
              names_of[r], rr_, rg)) in doc)
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("submission.md states the call", ("in %s, where it will avoid %d emergency admissions" % (names_of[w], rw)) in sub
          and ("%s is the runner-up at %d, %d fewer" % (names_of[r], rr_, rg)) in sub)
    block = sub[sub.index("### deprescribing_placement_2027.xlsx"):]
    nums = [int(x.replace(",", "")) for x in re.findall(r"   - [A-Za-z ]+: ([\d,]+)", block)]
    flat = [want[k][i] for i in range(4) for k in [c_ for c_ in ("CC", "FM", "SC", "QR", "HM", "LN")]]
    check("submission.md's 24 falls figures", nums == flat)
    print("verify: %d failure(s)" % len(fails))
    return len(fails)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
