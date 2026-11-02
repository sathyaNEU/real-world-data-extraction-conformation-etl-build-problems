"""Independent verifier for task134: reads only the shipped bundle (target/, figures.json) on its own code path, with
its own XLSX, PDF and DOCX readers and its own geometry, and recomputes every graded figure and the default path."""
import base64
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


# ---------- readers ----------
def pdf_lines(path):
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\s*endstream", raw, re.S):
        head = raw[raw.rfind(b"<<", 0, m.start()):m.start()]
        data = m.group(1)
        try:
            if b"ASCII85Decode" in head:
                d = data.strip()
                d = d[2:] if d.startswith(b"<~") else d
                d = d[:-2] if d.endswith(b"~>") else d
                data = base64.a85decode(d)
            if b"FlateDecode" in head:
                data = zlib.decompress(data)
        except Exception:
            continue
        for t in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", data, re.S):
            out.append(t.decode("latin-1").replace("\\(", "(").replace("\\)", ")"))
    return out


def docx_words(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return " ".join(" ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x)).split())


def xlsx_sheets(path):
    """{sheet name: [[cell values by column]]}, shared strings resolved, numbers as floats."""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        x = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            ss.append("".join(re.findall(r"<t[^>]*>([^<]*)</t>", si)))
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    target = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    target.update({k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)})
    out = {}
    for name, rid in re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wb):
        p = target[rid].lstrip("/")
        p = p if p.startswith("xl/") else "xl/" + p
        x = z.read(p).decode("utf-8")
        rows = []
        for row in re.findall(r"<row[^>]*>(.*?)</row>", x, re.S):
            cells = {}
            for ref, attrs, body in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(.*?)</c>', row, re.S):
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                v = re.search(r"<v>([^<]*)</v>", body)
                isv = re.search(r"<is>.*?<t[^>]*>([^<]*)</t>", body, re.S)
                if 't="s"' in attrs and v:
                    cells[col] = ss[int(v.group(1))]
                elif isv:
                    cells[col] = isv.group(1)
                elif v:
                    cells[col] = float(v.group(1))
            if cells:
                rows.append([cells.get(c) for c in range(1, max(cells) + 1)])
        out[name.replace("&amp;", "&")] = rows
    return out


def serial_date(v):
    return dt.date(1899, 12, 30) + dt.timedelta(days=int(v))


# ---------- geometry ----------
class Line:
    def __init__(self, wps):
        self.w = wps

    def place(self, e, n):
        best = None
        for i in range(len(self.w) - 1):
            c0, e0, n0 = self.w[i]
            c1, e1, n1 = self.w[i + 1]
            dx, dy = e1 - e0, n1 - n0
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            px, py = e - e0, n - n0
            u = px * ux + py * uy
            uc = min(max(u, 0.0), L)
            d = math.hypot(e - (e0 + uc * ux), n - (n0 + uc * uy))
            if best is None or d < best[0] - 1e-9:
                best = (d, c0 + u / 1000.0, -(ux * py - uy * px))
        return best[1], best[2]


def main(tdir):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(tdir))
    # notice
    nl = pdf_lines(os.path.join(tdir, "notice_to_mariners_03-2026.pdf"))
    ok("PDF read: the notice carries its datum sentence (positive control)", any("2.90 m below Ordnance Datum Newlyn" in l for l in nl))
    wps = []
    for i, l in enumerate(nl):
        if re.fullmatch(r"W\d", l):
            wps.append((float(nl[i + 1]), float(nl[i + 2]), float(nl[i + 3])))
    line = Line(wps)
    names = ["Outer Channel", "Fend Roads", "Middle Reach", "Inner Reach", "Turning Basin"]
    parts = {}
    for i, l in enumerate(nl):
        if l in names:
            a, b = re.match(r"([\d.]+) to ([\d.]+)", nl[i + 1]).groups()
            parts[l] = (float(a), float(b), float(nl[i + 2]) / 2.0, float(nl[i + 3]))
    ok("PDF read: five maintained parts at 12.3 m", len(parts) == 5 and all(p[3] == 12.3 for p in parts.values()))
    # basis
    bw = docx_words(os.path.join(tdir, "deepening_2027_maintenance_planning_basis.docx"))
    ok("DOCX read: the basis files the year 1 quantity and the 14.3 m hold",
       "will settle in the maintained areas between 1 October 2027 and 30 September 2028" in bw and "held at 14.3 m below chart datum" in bw)
    # certificates
    sh = xlsx_sheets(os.path.join(tdir, "maintenance_dredging_certificates_2016-2026.xlsx"))
    code = {r[0]: r[1] for r in sh["Area codes"][1:]}
    rec = {}
    for nm, rows in sh.items():
        if nm == "Area codes":
            continue
        for r in rows[3:]:
            if r[0] is None or not isinstance(r[0], float):
                continue
            mon = serial_date(r[0])
            area = code.get(r[1], r[1])
            key = (mon, area)
            if key not in rec or str(r[5]) > rec[key][1]:
                rec[key] = (r[4], str(r[5]))
    V = {}
    for (mon, area), (vol, c) in rec.items():
        if dt.date(2016, 10, 1) <= mon <= dt.date(2026, 9, 1):
            V[area] = V.get(area, 0.0) + vol / 10.0
    # surveys
    pts = []
    with open(os.path.join(tdir, "holmwood_channel_surveys_2016-2023.csv"), newline="") as f:
        for r in csv.reader(f):
            if r[0] == "SURVEY_REF" or float(r[4]) <= -99:
                continue
            pts.append((float(r[2]), float(r[3]), float(r[4])))
    odn = 2.90
    with open(os.path.join(tdir, "seaward_channel_surveys_2023-2026.csv"), newline="") as f:
        for r in csv.reader(f):
            if r[0] == "survey_id":
                continue
            pts.append((float(r[2]), float(r[3]), -float(r[4]) - odn))
    sums = {n: [0.0, 0] for n in names}
    for e, n, z in pts:
        s, t = line.place(e, n)
        for nm in names:
            c0, c1, half, d = parts[nm]
            if nm == "Turning Basin":
                if c0 <= s <= c1 and -(half + 300) <= t < -(half + 50):
                    sums[nm][0] += z
                    sums[nm][1] += 1
            elif c0 <= s < c1 and half + 50 < abs(t) <= half + 300:
                sums[nm][0] += z
                sums[nm][1] += 1
    nat = {nm: sums[nm][0] / sums[nm][1] for nm in names}
    for nm in names:
        ok("natural bed beside %s recomputes" % nm, "%.2f" % nat[nm] == figs["component.natural_bed.%s" % nm], "%.3f" % nat[nm])
    berth = V["North Quay Berth 1"] + V["North Quay Berth 3"] + V["Container Terminal Berth 5"]
    rec_tot = sum(V[n] for n in names) + berth
    ok("record mean recomputes", "{:,}".format(round(rec_tot)) == figs["component.record_mean_m3"], "%.0f" % rec_tot)
    gp = {nm: V[nm] * (14.3 - nat[nm]) / (12.3 - nat[nm]) for nm in names}
    gp["Berth pockets"] = berth
    total = sum(gp.values())
    ok("year 1 total recomputes at the nearest 50,000", "{:,}".format(int(round(total / 50000.0)) * 50000) == figs["call.total_m3"], "%.0f" % total)
    for nm, v in gp.items():
        ok("year 1 %s recomputes at the nearest 20,000" % nm, "{:,}".format(int(round(v / 20000.0)) * 20000) == figs["answer.part.%s" % nm], "%.0f" % v)
    r1 = sum(V[n] * 14.3 / 12.3 for n in names) + berth
    ok("the default path (depth ratio) files 1,500,000 on the bundle", int(round(r1 / 50000.0)) * 50000 == 1500000, "%.0f" % r1)

    # ask A
    ll = pdf_lines(os.path.join(tdir, "marine_licence_L2021-00317-2.pdf"))
    boxes, cur = {}, None
    for i, l in enumerate(ll):
        m = re.match(r"(Fend Spit|Wenning Deep) \(", l)
        if m:
            cur = m.group(1)
            boxes[cur] = []
        m2 = re.match(r"(\d+) ([\d.]+)' N", l)
        if m2 and cur:
            m3 = re.match(r"(\d+) ([\d.]+)' E", ll[i + 1])
            boxes[cur].append((int(m2.group(1)) + float(m2.group(2)) / 60, int(m3.group(1)) + float(m3.group(2)) / 60))
    ok("PDF read: two disposal sites of four corners each", len(boxes) == 2 and all(len(v) == 4 for v in boxes.values()))
    samp = xlsx_sheets(os.path.join(tdir, "sediment_sampling_2025-2026.xlsx"))
    frac = [(serial_date(r[1]), r[3], r[4]) for r in samp["Area summary"][1:] if r and r[0]]
    rev = {r["trip_ref"]: float(r["dry_solids_t_revised"]) for r in csv.DictReader(open(os.path.join(tdir, "FE_dry_solids_revision_20260330.csv")))}
    loads = list(csv.DictReader(open(os.path.join(tdir, "dunmarsh_load_log_2023-2026.csv"))))

    def local(t):
        y = t.year

        def ls(mo):
            d = dt.datetime(y, mo, 31)
            while d.weekday() != 6:
                d -= dt.timedelta(days=1)
            return d.replace(hour=1)
        return t + dt.timedelta(hours=1) if ls(3) <= t < ls(10) else t
    day = {}
    for r in sorted(loads, key=lambda r: r["loading_start_utc"]):
        if r["vessel"] == "Fend Endeavour":
            d = local(dt.datetime.strptime(r["loading_start_utc"], "%Y-%m-%dT%H:%M:00Z")).date()
            day[d] = day.get(d, 0) + 1
            r["trip"] = "FE%s/%d" % (d.strftime("%y%m%d"), day[d])
    placed = {}
    for r in loads:
        tl = local(dt.datetime.strptime(r["dump_start_utc"], "%Y-%m-%dT%H:%M:00Z"))
        if not (dt.datetime(2025, 10, 1) <= tl < dt.datetime(2026, 10, 1)):
            continue
        la, lo = float(r["dump_lat"]), float(r["dump_lon"])
        site = [k for k, v in boxes.items() if min(p[0] for p in v) <= la <= max(p[0] for p in v) and min(p[1] for p in v) <= lo <= max(p[1] for p in v)][0]
        tds = rev.get(r.get("trip"), float(r["dry_solids_t"])) if r["dry_solids_t"] else float(r["hopper_m3"]) * 2.65 * (float(r["mixture_density_t_m3"]) - 1.025) / 1.625
        area = code[r["area"]]
        f = max((c, fr) for c, a, fr in frac if a == area and c < dt.date(tl.year, tl.month, 1))[1]
        q = (tl.month - 10) // 3 + 1 if tl.month >= 10 else (tl.month - 1) // 3 + 2
        placed[(site, q)] = placed.get((site, q), 0.0) + tds / f
    for (site, q), v in sorted(placed.items()):
        ok("placements %s Q%d recompute at the nearest 1,000 t" % (site, q), "{:,}".format(int(round(v / 1000.0)) * 1000) == figs["answer.placed.%s.Q%d" % (site, q)], "%.0f" % v)

    # ask B
    field = [r for r in samp["Field log 2026"][1:] if r and r[0]]
    lab = {}
    for r in csv.DictReader(open(os.path.join(tdir, "aldern_results_FEN26.csv"))):
        v = float(r["result"]) / (1000.0 if r["units"] == "ug/kg" else 1.0)
        lab.setdefault(r["client_ref"], {})[r["determinand"]] = v
    prim = [r for r in field if r[1] != "QA"]
    dups = [r for r in field if r[1] == "QA"]

    def tmin(r):
        h, m = str(r[3]).split(":")
        return float(r[2]) * 1440 + int(h) * 60 + int(m)
    pair = {}
    for d in dups:
        p = min(prim, key=lambda p: math.hypot(p[4] - d[4], p[5] - d[5]) + abs(tmin(p) - tmin(d)))
        pair[p[0]] = d[0]
    groups = {}
    for p in prim:
        s, t = line.place(p[4], p[5])
        area = None
        for nm in names:
            c0, c1, half, d = parts[nm]
            if c0 <= s <= c1 and abs(t) <= half:
                area = nm
                break
        if area is None:
            continue
        v = dict(lab[p[0]])
        if p[0] in pair:
            v = {k: (v[k] + lab[pair[p[0]]][k]) / 2.0 for k in v}
        groups.setdefault(area, []).append(v)
    for nm in names:
        for met in ("Cadmium", "Mercury", "Lead", "Copper"):
            m = sum(x[met] for x in groups[nm]) / len(groups[nm])
            ok("mean %s %s recomputes" % (nm, met), "%.2f" % (m + 1e-12) == figs["answer.metal.%s.%s" % (nm, met)], "%.4f" % m)
    # the golden workbook carries every graded figure exactly as figures.json and block 4 state it
    gpath = os.path.join(os.path.dirname(HERE), "golden", "fendmouth_maintenance_2027-28.xlsx")
    if os.path.exists(gpath):
        gs = xlsx_sheets(gpath)
        y1 = gs["Year 1 quantity"]
        head = [r for r in y1 if r and r[0] == "Year 1 quantity (m3 in situ, nearest 50,000)"][0]
        ok("golden workbook: the year 1 total agrees with figures.json", "{:,}".format(int(head[-1])) == figs["call.total_m3"])
        for nm in names + ["Berth pockets (NQ1, NQ3, CT5)"]:
            row = [r for r in y1 if r and r[0] == nm][0]
            key = "Berth pockets" if nm.startswith("Berth") else nm
            ok("golden workbook: %s agrees with figures.json" % key, "{:,}".format(int(row[6])) == figs["answer.part.%s" % key])
        qn = {"October to December 2025": 1, "January to March 2026": 2, "April to June 2026": 3, "July to September 2026": 4}
        got = 0
        for r in gs["Placements 2025-26"]:
            if r and r[0] in qn:
                for i, site in ((1, "Fend Spit"), (2, "Wenning Deep")):
                    got += "{:,}".format(int(r[i])) == figs["answer.placed.%s.Q%d" % (site, qn[r[0]])]
        ok("golden workbook: the eight placements agree with figures.json", got == 8, "%d of 8" % got)
        got = 0
        for r in gs["Sediment 2026"]:
            if r and r[0] in names:
                for i, met in enumerate(("Cadmium", "Mercury", "Lead", "Copper"), start=1):
                    got += "%.2f" % r[i] == figs["answer.metal.%s.%s" % (r[0], met)]
        ok("golden workbook: the twenty metal means agree with figures.json", got == 20, "%d of 20" % got)
    ok("every format reads back: csv, xlsx, pdf, docx", {f.rsplit(".", 1)[1] for f in files} == {"csv", "xlsx", "pdf", "docx"})
    bad = [r for r in RES if not r[1]]
    for label, c, detail in RES:
        print("%s  %s%s" % ("PASS" if c else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("verify: %d checks, %d FAIL" % (len(RES), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
