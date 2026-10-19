"""The pack's record files: the consortium's hepatobiliary and pancreatic discharge files in their three layouts, the
two 2026 releases, the death linkage, the hospital directory, the procedure classes, the plan's facility claims and
two files that sit beside the decision (the public star ratings and the travel benefit estimates)."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K

NDX = {1: 9, 2: 25, 3: 25}     # diagnosis slots in each layout
NPX = {1: 6, 2: 25, 3: 25}


def _rng(seed, *key):
    return np.random.default_rng([seed] + [int(k) for k in key])


def era(year):
    return 1 if year <= 2018 else 2 if year <= 2022 else 3


def _nodot(c):
    return c.replace(".", "")


def _age(rec, on):
    d = rec["dob"]
    return on.year - d.year - ((on.month, on.day) < (d.month, d.day))


def assign_ids(w):
    """Record numbers in discharge order within each year; the 2026 releases get their own."""
    allr = w["index"] + w["earlier"] + w["background"]
    allr.sort(key=lambda r: (r["discharge"], r["hosp"], r["key"]))
    seq = {}
    for rec in allr:
        y = rec["discharge"].year
        seq[y] = seq.get(y, 0) + 1
        rec["year"] = y
        rec["rec_id"] = "%d%06d" % (y, seq[y])
    w["all"] = allr
    return allr


def _missing_key(w, rec):
    """About one record in a hundred before 2019 came from a hospital that sent no identifiers that quarter."""
    if rec["year"] > 2018 or rec.get("index"):
        return False
    r = _rng(w["seed"], 41, int(rec["rec_id"]))
    return r.random() < .011


def _row(rec, e, w):
    adm, dis = rec["admit"], rec["discharge"]
    dx = rec["dx"][:NDX[e]]
    px = rec["px"][:NPX[e]]
    key = "" if _missing_key(w, rec) else rec["key"]
    hosp = K.OLD_NO[rec["hosp"]] if e < 3 else K.NEW_NO["G" if rec["hosp"] == "G2" and adm >= K.MERGER else rec["hosp"]]
    age = _age(rec, adm)
    return dict(rec_id=rec["rec_id"], hosp=hosp, key=key, sex=rec["sex"], age=age, admit=adm, discharge=dis,
                atype=rec["admit_type"], asrc=rec["admit_source"], disp=rec["disposition"], pcat=rec["payer_cat"],
                payer=rec["payer"], dx=dx, px=px)


# the 2016 and 2017 fixed-width layout, and 2018's, which inserts the patient's county code after the payer category
FW1 = [("rec_id", 10), ("hosp", 4), ("key", 16), ("sex", 1), ("age", 3), ("admit", 8), ("discharge", 8),
       ("atype", 1), ("asrc", 1), ("disp", 2), ("pcat", 1)]
FW_COUNTY = [("county", 2)]


def write_fixed(path, recs, w, year):
    county = year == 2018
    r = _rng(w["seed"], 51, year)
    with open(path, "w", encoding="ascii", newline="") as f:
        for rec in recs:
            row = _row(rec, 1, w)
            parts = [row["rec_id"].ljust(10), row["hosp"].ljust(4), row["key"].ljust(16), row["sex"],
                     ("%3d" % row["age"]), row["admit"].strftime("%Y%m%d"), row["discharge"].strftime("%Y%m%d"),
                     row["atype"], row["asrc"], row["disp"].ljust(2), row["pcat"]]
            if county:
                parts.append("%02d" % int(r.integers(1, 73)))
            for i in range(NDX[1]):
                c, p = (row["dx"][i] if i < len(row["dx"]) else ("", ""))
                parts.append(_nodot(c).ljust(7))
                parts.append((p if c else "").ljust(1))
            for i in range(NPX[1]):
                c = row["px"][i][0] if i < len(row["px"]) else ""
                parts.append(c.ljust(7))
            d0 = row["px"][0][1].strftime("%Y%m%d") if row["px"] else ""
            parts.append(d0.ljust(8))
            f.write("".join(parts) + "\r\n")
    return len(recs)


def _csv_rows(recs, w, e):
    for rec in recs:
        row = _row(rec, e, w)
        if e == 2:
            out = [row["rec_id"], row["hosp"], row["key"], row["sex"], row["age"], row["admit"].strftime("%m/%d/%Y"),
                   row["discharge"].strftime("%m/%d/%Y"), row["atype"], row["asrc"], row["disp"], row["pcat"],
                   row["payer"]]
        else:
            out = [row["rec_id"], row["hosp"], row["key"], row["sex"], row["age"], row["admit"].isoformat(),
                   row["discharge"].isoformat(), row["atype"], row["asrc"], row["disp"], row["pcat"], row["payer"]]
        for i in range(NDX[e]):
            c, p = row["dx"][i] if i < len(row["dx"]) else ("", "")
            out += [_nodot(c) if e == 2 else c, p if c else ""]
        for i in range(NPX[e]):
            if i < len(row["px"]):
                c, d = row["px"][i]
                out += [c, d.strftime("%m/%d/%Y") if e == 2 else d.isoformat()]
            else:
                out += ["", ""]
        yield out


HEAD2 = ["record_id", "hospital_no", "person_key", "sex", "age", "admit_date", "discharge_date", "admit_type",
         "admit_source", "discharge_status", "payer_cat", "payer_name"]
HEAD3 = ["rec_no", "hosp_id", "link_key", "sex", "age_years", "admission_date", "discharge_date", "adm_type",
         "adm_source", "dsch_disposition", "payer_group", "payer"]


def _header(e):
    h = list(HEAD2 if e == 2 else HEAD3)
    for i in range(1, NDX[e] + 1):
        h += (["dx%02d" % i, "poa%02d" % i] if e == 2 else ["diag_%d" % i, "poa_%d" % i])
    for i in range(1, NPX[e] + 1):
        h += (["px%02d" % i, "pxdate%02d" % i] if e == 2 else ["proc_%d" % i, "proc_date_%d" % i])
    return h


def write_csv(path, recs, w, e):
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\r\n" if e == 2 else "\n")
        wr.writerow(_header(e))
        for out in _csv_rows(recs, w, e):
            wr.writerow(out)
    return len(recs)


def discharges(w):
    """Records by file, in discharge order."""
    allr = [r for r in w["all"] if r["discharge"] <= dt.date(2025, 12, 31)]
    by = {}
    for rec in sorted(allr, key=lambda r: (r["discharge"], r["rec_id"])):
        by.setdefault(rec["year"], []).append(rec)
    return by


def _is_res(rec):
    return any(c in K.RESECTION for c, _ in rec["px"])


OTHER_DISP = {"01": "06", "06": "01", "03": "62", "62": "03", "02": "03", "50": "51", "51": "50", "20": "20", "07": "01"}


def releases_2026(w):
    """The first quarter's preliminary release (15 May) and the first half's revised release (18 September), each
    with its own record numbers. Between the two, hospitals sent first-quarter records that missed the preliminary
    cut, withdrew a duplicate submission, recoded a few operations the surgeon abandoned after exploration and
    corrected records. The consortium matches a correction to the record it corrects on the hospital's account number
    and the discharge date, so a correction that changed the discharge date loads beside the record it corrects: both
    stand in the revised release (the research files carry no account number)."""
    seed = w["seed"]
    r = _rng(seed, 61, 2026)
    h1 = [rec for rec in w["all"] if rec["discharge"].year == 2026 and rec["discharge"] <= K.H1_2026[1]]
    q1end = dt.date(2026, 3, 31)
    q1 = [rec for rec in h1 if rec["discharge"] <= q1end]
    late = {rec["rec_id"] for rec in q1 if r.random() < .06}
    rf = _rng(seed, 64, 2026)
    for h in K.ELIGIBLE:
        # every eligible hospital sent at least one first-quarter resection after the preliminary cut
        mine = [rec for rec in q1 if rec["hosp"] == h and _is_res(rec) and rec["kind"] != "reop"]
        if not any(rec["rec_id"] in late for rec in mine):
            late.add(mine[int(rf.integers(0, len(mine)))]["rec_id"])
    prelim = [rec for rec in q1 if rec["rec_id"] not in late]
    dups = []
    for rec in prelim:
        if rec["hosp"] in ("C", "F") and r.random() < .05:
            dups.append(dict(rec, dup=True))
    recoded = set()
    for rec in prelim:
        if _is_res(rec) and rec["kind"] != "reop" and r.random() < .05:
            recoded.add(rec["rec_id"])
    # corrections the consortium did not match: the hospital's first record carried the discharge date, or the
    # admission date (the emergency department arrival), or the admission and operation dates of a case rebooked by a
    # day, out by a day or two
    rc = _rng(seed, 62, 2026)
    corrected = []
    for rec in h1:
        if rec["rec_id"] in late or rec["rec_id"] in recoded or rec["kind"] == "reop":
            continue
        if rc.random() < (.10 if (rec["hosp"] in K.ELIGIBLE and _is_res(rec)) else .02):
            corrected.append(rec)
    kind = {rec["rec_id"]: ("dis", "adm", "adm_op")[int(rc.choice(3, p=[.55, .25, .20]))] for rec in corrected}
    for h in K.ELIGIBLE:
        # every eligible hospital: at least one resection whose discharge date was corrected, and one rebooked case
        mine = [x for x in corrected if x["hosp"] == h and _is_res(x)]
        pool = [rec for rec in h1 if rec["hosp"] == h and _is_res(rec) and rec["kind"] != "reop"
                and rec["rec_id"] not in late and rec["rec_id"] not in recoded and rec["rec_id"] not in kind]
        for need in ("dis", "adm_op"):
            if not any(kind[x["rec_id"]] == need for x in mine):
                x = pool.pop(int(rf.integers(0, len(pool))))
                corrected.append(x)
                mine.append(x)
                kind[x["rec_id"]] = need
    first = {}
    for rec in corrected:
        k = kind[rec["rec_id"]]
        op = min(d for _, d in rec["px"])
        x = None
        if k == "dis":
            shifts = [1, 2, -1, -2]
            rc.shuffle(shifts)
            for d in shifts:
                nd = rec["discharge"] + dt.timedelta(days=d)
                if (nd <= q1end) == (rec["discharge"] <= q1end) and nd <= K.H1_2026[1] and nd >= op + dt.timedelta(days=2):
                    x = dict(rec, discharge=nd)
                    break
        elif k == "adm":
            na = rec["admit"] - dt.timedelta(days=1)
            if na.year == 2026:
                x = dict(rec, admit=na)
        else:
            d = -1 if rec["admit"] > dt.date(2026, 1, 1) else 1
            na = rec["admit"] + dt.timedelta(days=d)
            if d < 0 or op + dt.timedelta(days=1) < rec["discharge"]:
                x = dict(rec, admit=na, px=[(c, pd_ + dt.timedelta(days=d)) for c, pd_ in rec["px"]])
        if x is None:
            continue
        x["version"] = "first"
        if rc.random() < .4:
            x["disposition"] = OTHER_DISP.get(rec["disposition"], rec["disposition"])
        first[rec["rec_id"]] = x
    w["first_kind"] = kind
    # corrections matched in place: the preliminary release carries the record as first sent
    rm = _rng(seed, 63, 2026)
    p_out = []
    for rec in prelim:
        if rec["rec_id"] in first:
            p_out.append(dict(first[rec["rec_id"]]))
        elif rec["rec_id"] not in recoded and rm.random() < .03:
            p_out.append(dict(rec, disposition=OTHER_DISP.get(rec["disposition"], rec["disposition"])))
        else:
            p_out.append(dict(rec))
    p_out += dups
    p_out.sort(key=lambda x: (x["discharge"], x["rec_id"], x.get("dup", False)))
    for i, rec in enumerate(p_out, 1):
        rec["p_no"] = "P26%05d" % i
    revised = []
    for rec in h1:
        rr = dict(rec, version="final")
        if rec["rec_id"] in recoded:
            # the operation was abandoned after exploration: the revised record carries the diagnostic excision
            rr["px"] = [("0FBG0ZX", d) if c in ("0FBG0ZZ", "0FTG0ZZ") else (c, d) for c, d in rec["px"]
                        if c not in ("0DT90ZZ", "0FT40ZZ", "0F190ZB", "0D160ZA", "07TP0ZZ")]
        revised.append(rr)
        if rec["rec_id"] in first:
            revised.append(dict(first[rec["rec_id"]]))
    revised.sort(key=lambda x: (x["discharge"], x["hosp"], x["key"], x["version"]))
    for i, rec in enumerate(revised, 1):
        rec["r_no"] = "R26%05d" % i
    w["prelim"], w["revised"] = p_out, revised
    w["late"], w["recoded"], w["dups"], w["first_sent"] = late, recoded, dups, first
    return p_out, revised


def write_release(path, recs, w, numkey):
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(_header(3))
        for rec in recs:
            x = dict(rec)
            x["rec_id"] = rec[numkey]
            for out in _csv_rows([x], w, 3):
                wr.writerow(out)
    return len(recs)


def write_deaths(path, w):
    """Every person key the consortium sent for linkage, with the state death record found for it, if any. The day of
    death is imputed to the 15th where the record gives only the month."""
    r = _rng(w["seed"], 71, 1)
    dd = {d["key"]: d["date"] for d in w["deaths"]}
    keys = sorted({p["key"] for p in w["persons"]})
    protect = {rec["key"] for rec in w["index"]}
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["link_key", "death_record_found", "date_of_death", "dod_day_imputed", "place_of_death"])
        for k in keys:
            if k in dd:
                d = dd[k]
                imputed = ""
                if k not in protect and r.random() < .03:
                    d = d.replace(day=15)
                    imputed = "Y"
                place = ["Hospital inpatient", "Decedent's home", "Nursing home", "Hospice facility", "Other"][
                    int(r.choice(5, p=[.35, .3, .2, .1, .05]))]
                wr.writerow([k, "Y", d.isoformat(), imputed, place])
            else:
                wr.writerow([k, "N", "", "", ""])
            n += 1
    return n


def _sheet(ws, header, rows, widths, title=None, note=None):
    r0 = 1
    if title:
        ws.cell(1, 1, title).font = Font(bold=True, size=12)
        r0 = 3
        if note:
            ws.cell(2, 1, note).font = Font(italic=True, size=9)
    for j, h in enumerate(header, 1):
        c = ws.cell(r0, j, h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(i, j, v)
    for j, wdt in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.freeze_panes = ws.cell(r0 + 1, 1)


CITY = {"A": "Madison", "B": "Milwaukee", "C": "Green Bay", "D": "La Crosse", "E": "Wausau", "F": "Eau Claire",
        "G": "Appleton", "G2": "Neenah", "H": "Kenosha"}


def write_hospitals(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Hospitals"
    rows = []
    small_city = ["Rhinelander", "Ashland", "Rice Lake", "Marshfield", "Beaver Dam", "Fond du Lac", "Manitowoc",
                  "Sheboygan", "Janesville", "Oshkosh", "Stevens Point", "Superior", "Racine", "Waukesha"]
    for i, (code, name, old, new, npi, _) in enumerate(K.HOSPITALS):
        city = CITY.get(code) or small_city[int(code[1:]) - 1]
        note = None
        if code == "G2":
            note = "Joined Ferncastle Health 1 July 2024; reports under 550745 from that date."
        rows.append([old, new, name, city, npi, note])
    _sheet(ws, ["Hospital no. (to 2022)", "Hospital ID (from 2023)", "Hospital", "City", "NPI (facility)", "Notes"],
           rows, [16, 16, 38, 16, 14, 60], title="ULHDC member hospitals that report hepatobiliary and pancreatic procedures",
           note="Directory as of 1 September 2026.")
    ws2 = wb.create_sheet("Changes")
    _sheet(ws2, ["Effective", "Change"], [
        ["1 January 2023", "Hospital numbers move from four digits to the six-digit ULHDC hospital ID (state prefix 55)."],
        ["1 July 2024", "Maplewick Community Hospital (0749 / 550749) joins Ferncastle Health (550745). Discharges "
                        "from the Maplewick campus are reported under 550745 from this date; Maplewick's pancreatic "
                        "surgery moved to the Ferncastle campus in 2023."],
        ["1 January 2019", "Discharge files move from the fixed-width layout to comma-separated files with 25 "
                           "diagnosis and 25 procedure slots."],
    ], [18, 110], title="Directory changes")
    wb.save(path)
    return len(rows)


CLASSES = [
    ("0FBG0ZZ", "Pancreas: excision (partial resection)"), ("0FBG4ZZ", "Pancreas: excision (partial resection)"),
    ("0FTG0ZZ", "Pancreas: total resection"), ("0FTG4ZZ", "Pancreas: total resection"),
    ("0FBG0ZX", "Pancreas: biopsy"), ("0FBG3ZX", "Pancreas: biopsy"), ("0FBG8ZX", "Pancreas: biopsy"),
    ("0F1D0ZB", "Pancreas: duct bypass or drainage"), ("0FCG0ZZ", "Pancreas: debridement or extirpation"),
    ("0F9G30Z", "Pancreas: drainage"), ("0F9G00Z", "Pancreas: drainage"),
    ("0F190ZB", "Bile duct: bypass"), ("0F190Z3", "Bile duct: bypass"), ("0FB90ZZ", "Bile duct: excision"),
    ("0FC90ZZ", "Bile duct: exploration and stone removal"),
    ("0F798DZ", "Endoscopic biliary or pancreatic procedure"), ("0FC98ZZ", "Endoscopic biliary or pancreatic procedure"),
    ("0FJD8ZZ", "Endoscopic biliary or pancreatic procedure"),
    ("0FT44ZZ", "Gallbladder: removal"), ("0FT40ZZ", "Gallbladder: removal"),
    ("0FB00ZZ", "Liver: resection"), ("0FT00ZZ", "Liver: resection"), ("0FB04ZZ", "Liver: resection"),
    ("0FB24ZZ", "Liver: resection"),
    ("0DT90ZZ", "Duodenum: resection"), ("0D160ZA", "Stomach: bypass"), ("07TP0ZZ", "Spleen: removal"),
    ("0F1G0ZC", "Pancreas: bypass"), ("0DT60ZZ", "Stomach: resection"),
]


def write_classes(path):
    names = {**K.RESECTION, **K.BIOPSY, **K.WHIPPLE_PARTS, **K.EARLIER_OPS, **K.CHOLE, **K.ERCP, **K.OTHER_OPS,
             "0F9G30Z": "Drainage of pancreas, percutaneous approach", "0F9G00Z": "Drainage of pancreas, open approach",
             "07TP0ZZ": "Resection of spleen, open approach"}
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["icd10pcs", "description", "ulhdc_procedure_class"])
        for c, cls in CLASSES:
            wr.writerow([c, names.get(c, ""), cls])
    return len(CLASSES)


RATE = dict(A=34200, B=31800, C=27400, D=26100, E=25600, F=24900, G=24200, H=23800)
# the Medicare Advantage platform's two re-pricings of 2024: the claims a pass covers by statement-through date, the
# day the pass ran, and the change in the allowed amount
REPRICE = [(dt.date(2024, 1, 1), dt.date(2024, 5, 15), dt.date(2024, 6, 10), 1.028, 1.044),
           (dt.date(2024, 1, 1), dt.date(2024, 9, 30), dt.date(2024, 11, 4), 1.006, 1.016)]


def _version(prev, **kw):
    x = dict(prev)
    x.update(kw)
    return x


def plan_claims(w):
    """The plan's facility claims for its members' resection stays, from its two claims platforms. On the cooperative's
    own platform (commercial and BadgerCare) a replacement claim names the claim it replaces; on the Medicare Advantage
    platform every later version of a claim names the claim first received. Stays over 21 days are billed in interim
    claims (0112, 0113, 0114), each for its own days. A hospital corrects a claim with a replacement (0117), sometimes
    to correct the discharge date; the Medicare Advantage platform re-priced its 2024 claims twice; a claim billed to
    the wrong member of a household is voided (0118) and rebilled. Every version of every claim stays in the extract."""
    seed = w["seed"]
    r = _rng(seed, 81, 1)
    ra = _rng(seed, 82, 1)
    out, stays, chains = [], [], []
    members = {}
    seq = [0]

    def tmp():
        seq[0] += 1
        return seq[0]

    for rec in sorted(w["index"], key=lambda x: (x["discharge"], x["key"])):
        if rec["payer"] != K.PLAN:
            continue
        lob = "MA" if rec["payer_cat"] == "2" else "MCD" if rec["payer_cat"] == "3" else "COM"
        mid = members.setdefault(rec["key"], "CHC%07d" % (1000000 + int(r.integers(0, 8999999))))
        los = (rec["discharge"] - rec["admit"]).days
        mult = {"MA": .78, "MCD": .62, "COM": 1.0}[lob]
        comp = any(p == "N" for _, p in rec["dx"])
        drg = "405" if comp else ("406" if r.random() < .5 else "407")
        allowed = round(RATE[rec["hosp"]] * mult * (1.55 if drg == "405" else 1.0 if drg == "406" else .82)
                        * (1 + max(0, los - 9) * .045) * float(r.uniform(.96, 1.04)), 2)
        segs = []
        if los > 21:
            bounds = [0] + list(range(21, los, 21)) + [los]
            for i in range(len(bounds) - 1):
                bt = "0112" if i == 0 else ("0114" if i == len(bounds) - 2 else "0113")
                segs.append([bt, rec["admit"] + dt.timedelta(days=bounds[i]),
                             rec["admit"] + dt.timedelta(days=bounds[i + 1]),
                             round(allowed * (bounds[i + 1] - bounds[i]) / los, 2)])
            segs[-1][3] = round(segs[-1][3] + round(allowed - sum(s_[3] for s_ in segs), 2), 2)
        else:
            segs.append(["0111", rec["admit"], rec["discharge"], allowed])
        stay = dict(hosp=rec["hosp"], key=rec["key"], member=mid, lob=lob, admit=rec["admit"],
                    discharge=rec["discharge"], chains=[])
        for bt, f_, t_, amt in segs:
            root = dict(tmp=tmp(), orig=None, member_id=mid, line_of_business=lob, billing_npi=K.NPI[rec["hosp"]],
                        bill_type=bt, admit_date=rec["admit"], statement_from=f_, statement_through=t_,
                        discharge_status=rec["disposition"] if bt in ("0111", "0114") else "30", ms_drg=drg,
                        principal_icd10pcs=rec["px"][0][0], allowed_amount=amt,
                        billed_amount=round(amt * float(r.uniform(2.1, 2.9)), 2),
                        received_date=t_ + dt.timedelta(days=int(r.integers(4, 30))), claim_status="paid")
            ch = dict(lob=lob, root=root, versions=[root], wrong=None, final=bt in ("0111", "0114"), stay=stay)
            stay["chains"].append(ch)
            chains.append(ch)
        stays.append(stay)

    def correct(ch, fix_date=False, again=False):
        """A hospital's replacement claim, received weeks after the version it replaces."""
        prev = ch["versions"][-1]
        x = _version(prev, tmp=tmp(), bill_type="0117",
                     orig=ch["root"]["tmp"] if ch["lob"] == "MA" else prev["tmp"],
                     allowed_amount=round(prev["allowed_amount"] * float(ra.uniform(.97, 1.03) if again
                                                                         else ra.uniform(.94, 1.06)), 2),
                     received_date=prev["received_date"] + dt.timedelta(days=int(ra.integers(20, 90))))
        x["billed_amount"] = round(x["allowed_amount"] * float(ra.uniform(2.1, 2.9)), 2)
        if fix_date:
            x["statement_through"] = ch["stay"]["discharge"]
        ch["versions"].append(x)

    def misdate(ch):
        """The first claim carried a discharge date a day or two out; the replacement corrects it."""
        t = ch["stay"]["discharge"]
        for d in [1, -1, 2, -2][int(ra.integers(0, 4)):] + [1, -1]:
            nd = t + dt.timedelta(days=d)
            if nd.year == t.year and nd > ch["root"]["statement_from"]:
                ch["root"]["statement_through"] = nd
                ch["root"]["received_date"] = nd + dt.timedelta(days=int(ra.integers(4, 30)))
                return True
        return False

    for ch in chains:
        u = ra.random()
        if u < .07:
            fix = ch["final"] and ra.random() < .35 and misdate(ch)
            correct(ch, fix_date=fix)
            if ra.random() < .2:
                correct(ch, again=True)
    # every eligible hospital: a commercial or BadgerCare claim replaced twice, and a replacement correcting the date
    rf = _rng(seed, 84, 1)
    for h in K.ELIGIBLE:
        mine = [ch for ch in chains if ch["stay"]["hosp"] == h]
        if not any(ch["lob"] != "MA" and len(ch["versions"]) >= 3 for ch in mine):
            cand = [ch for ch in mine if ch["lob"] != "MA" and len(ch["versions"]) == 1 and ch["final"]]
            ch = cand[int(rf.integers(0, len(cand)))]
            correct(ch)
            correct(ch, again=True)
        if not any(v["statement_through"] != ch["root"]["statement_through"] for ch in mine for v in ch["versions"]):
            cand = [ch for ch in mine if len(ch["versions"]) == 1 and ch["final"]]
            ch = cand[int(rf.integers(0, len(cand)))]
            misdate(ch)
            correct(ch, fix_date=True)
    # the Medicare Advantage platform's re-pricings of 2024: a new version of every claim the pass covers
    for lo, hi, day, f0, f1 in REPRICE:
        for ch in chains:
            if ch["lob"] != "MA" or not (lo <= ch["root"]["statement_through"] <= hi):
                continue
            prev = max(ch["versions"], key=lambda v: (v["received_date"], v["tmp"]))
            if prev["received_date"] >= day:
                continue
            x = _version(prev, tmp=tmp(), bill_type="0117", orig=ch["root"]["tmp"],
                         allowed_amount=round(prev["allowed_amount"] * float(ra.uniform(f0, f1)), 2),
                         received_date=day + dt.timedelta(days=int(ra.integers(0, 12))))
            ch["versions"].append(x)
    # billed first to another member of the household, voided and rebilled
    for ch in chains:
        if len(ch["versions"]) == 1 and ch["root"]["bill_type"] == "0111" and ra.random() < .03:
            root = ch["root"]
            wrong = _version(root, tmp=tmp(), member_id="CHC%07d" % (1000000 + int(ra.integers(0, 8999999))),
                             received_date=root["received_date"])
            void = _version(wrong, tmp=tmp(), bill_type="0118", orig=wrong["tmp"],
                            received_date=wrong["received_date"] + dt.timedelta(days=int(ra.integers(10, 40))))
            root["received_date"] = void["received_date"] + dt.timedelta(days=int(ra.integers(2, 20)))
            ch["wrong"] = (wrong, void)
    # the warehouse numbers claims in the order it received them
    allc = []
    for ch in chains:
        allc += ch["versions"]
        if ch["wrong"]:
            allc += list(ch["wrong"])
    allc.sort(key=lambda x: (x["received_date"], x["tmp"]))
    num = {}
    for i, x in enumerate(allc, 1):
        num[x["tmp"]] = "C%09d" % (240000000 + i * 7)
    for x in allc:
        x["claim_id"] = num[x["tmp"]]
        x["original_claim_id"] = num[x["orig"]] if x["orig"] else ""
    for st in stays:
        st["allowed"] = round(sum(max(ch["versions"], key=lambda v: (v["received_date"], v["tmp"]))["allowed_amount"]
                                  for ch in st["chains"]), 2)
    w["plan_stays"] = stays
    w["plan_chains"] = chains
    w["plan_claims"] = allc
    return allc


def write_claims(path, w):
    rows = sorted(w["plan_claims"], key=lambda x: (x["received_date"], x["claim_id"]))
    cols = ["claim_id", "original_claim_id", "member_id", "line_of_business", "billing_npi", "bill_type", "admit_date",
            "statement_from", "statement_through", "discharge_status", "ms_drg", "principal_icd10pcs", "billed_amount",
            "allowed_amount", "received_date", "claim_status"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(cols)
        for x in rows:
            wr.writerow([x[c].isoformat() if isinstance(x[c], dt.date) else ("%.2f" % x[c] if isinstance(x[c], float) else x[c])
                         for c in cols])
    return len(rows)


def write_stars(path, w):
    r = _rng(w["seed"], 91, 1)
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["facility_name", "city", "state", "hospital_type", "overall_rating", "mortality_group_measures",
                     "safety_group_measures", "readmission_group_measures", "patient_experience_measures",
                     "rating_period"])
        for code, name, *_ in K.HOSPITALS:
            if code == "G2":
                continue
            city = CITY.get(code, "")
            star = int(r.choice([2, 3, 4, 5], p=[.15, .35, .35, .15]))
            wr.writerow([name, city or "", "WI", "Acute Care Hospitals", star, int(r.integers(4, 8)),
                         int(r.integers(5, 9)), int(r.integers(8, 12)), 8, "Jul 2021 - Jun 2024"])
    return len(K.HOSPITALS) - 1


def write_travel(path, w):
    r = _rng(w["seed"], 95, 1)
    wb = Workbook()
    ws = wb.active
    ws.title = "Estimates"
    rows = []
    for code in K.ELIGIBLE:
        miles = float(r.uniform(38, 120))
        rows.append([K.NAME[code], round(miles, 1), round(miles * 2 * .67, 2), int(r.integers(2, 5)),
                     round(float(r.uniform(119, 169)), 2)])
    _sheet(ws, ["Hospital", "Average member round-trip miles (one way)", "Mileage per trip ($)",
                "Lodging nights per episode", "Nightly lodging rate ($)"], rows, [38, 22, 18, 18, 18],
           title="Travel benefit: finance estimates for 2027 budgeting (draft)",
           note="Finance, 12 August 2026. Mileage at the IRS medical rate; lodging at negotiated rates.")
    wb.save(path)
    return len(rows)
