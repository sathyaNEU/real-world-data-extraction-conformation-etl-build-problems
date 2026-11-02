"""Independent verifier for task484: its own readers for every shipped format (a quote-aware CSV splitter, the
xlsx and docx XML read straight from the zip, PDF streams decoded ASCII85 then Flate) and its own computation of
every golden figure, compared with golden/. Shares no code with the generator.

    python3 task484/generator/verify.py
"""
import base64
import datetime as dt
import math
import os
import re
import statistics
import sys
import zipfile
import zlib
from itertools import permutations

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TGT = os.path.join(TASK, "target")
GLD = os.path.join(TASK, "golden")
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def split_line(line):
    out, cur, q = [], "", False
    for ch in line:
        if ch == '"':
            q = not q
        elif ch == "," and not q:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def read_table(path):
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\r\n") for l in f]
    hdr = split_line(lines[0])
    rows = []
    for l in lines[1:]:
        p = split_line(l)
        if p == hdr:
            continue
        rows.append(dict(zip(hdr, p)))
    return rows


def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        x = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            ss.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    wbx = z.read("xl/workbook.xml").decode("utf-8")
    names = re.findall(r'<sheet [^>]*name="([^"]+)"', wbx)
    out = {}
    for k, nm in enumerate(names, start=1):
        x = z.read("xl/worksheets/sheet%d.xml" % k).decode("utf-8")
        rows = []
        for r in re.findall(r"<row [^>]*>(.*?)</row>", x, re.S):
            cells = {}
            for c in re.finditer(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)', r, re.S):
                col, attrs, body = c.group(1), c.group(2), c.group(3) or ""
                v = re.search(r"<v>(.*?)</v>", body, re.S)
                t = re.search(r't="(\w+)"', attrs)
                if t and t.group(1) == "s" and v:
                    val = ss[int(v.group(1))]
                elif t and t.group(1) == "inlineStr":
                    val = "".join(re.findall(r"<t[^>]*>(.*?)</t>", body, re.S))
                elif v:
                    val = float(v.group(1))
                else:
                    val = None
                cells[col] = val
            idx = sorted(cells, key=lambda c: (len(c), c))
            rows.append([cells[c] for c in idx])
        out[nm] = rows
    return out


def docx_text(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    return re.sub(r"\s+", " ", " ".join(re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", x)))


def pdf_text(path):
    raw = open(path, "rb").read()
    parts = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        data = m.group(1).strip()
        try:
            if data.endswith(b"~>"):
                data = base64.a85decode(data, adobe=True)
            data = zlib.decompress(data)
        except Exception:
            continue
        parts += re.findall(rb"\((.*?)\)\s*Tj", data)
    return " ".join(p.decode("latin-1") for p in parts)


def canon(road):
    road = road.strip().lower()
    if len(road) > 2 and road[-2] == " " and road[-1] in "nsew":
        road = road[:-2]
    for a, b in ((" ave", " avenue"), (" rd", " road"), (" st", " street"), (" la", " lane"), (" wy", " way"), (" hl", " hill")):
        if road.endswith(a):
            road = road[: -len(a)] + b
    return road


def main():
    # positive controls on every document format
    terms = pdf_text(os.path.join(TGT, "traffic_estimate_terms_2025.pdf"))
    scope = pdf_text(os.path.join(TGT, "noise_mapping_2026_scope.pdf"))
    log = docx_text(os.path.join(TGT, "network_operations_log_2025.docx"))
    ok("PDF read back (terms note): annual traffic is both directions on all days", "both directions together" in terms and "all the" in terms)
    ok("PDF read back (scope note): more than three million vehicle passages, every section counted in 2025",
       "three million vehicle passages" in scope and "counted in 2025" in scope)
    ok("DOCX read back (operations log): the firmware push is logged", "Firmware 5.1.3" in log)
    reg = xlsx_sheets(os.path.join(TGT, "utc_asset_register_2025.xlsx"))
    cpx = xlsx_sheets(os.path.join(TGT, "count_points_2025.xlsx"))
    ok("XLSX read back (UTC register and count point register)", len(reg["Junctions"]) > 15 and len(cpx["Count points"]) > 20)

    base = dt.date(1899, 12, 30)
    # count points and counts
    hdr = cpx["Count points"][0]
    points = {int(r[0]): dict(zip(hdr, r)) for r in cpx["Count points"][1:]}
    c12, cdate = {}, {}
    for r in read_table(os.path.join(TGT, "manual_counts_2025.csv")):
        cp = int(r["count_point_id"])
        c12[cp] = c12.get(cp, 0) + int(r["all_motor_vehicles"])
        cdate[cp] = dt.date.fromisoformat(r["count_date"])
    # counters
    sites = {r["site_id"]: r for r in read_table(os.path.join(TGT, "atc_sites_2025.csv"))}
    atc = {}
    for r in read_table(os.path.join(TGT, "atc_daily_2025.csv")):
        atc.setdefault(r["site_id"], {})[dt.date.fromisoformat(r["date"])] = r
    # detectors
    det = {}
    for r in read_table(os.path.join(TGT, "utc_detector_daily_2025.csv")):
        d = dt.datetime.strptime(r["date"], "%d/%m/%Y").date()
        det.setdefault(r["detector"], {})[d] = (float(r["flow_0700_1900"]) if r["flow_0700_1900"] else None,
                                                float(r["flow_0000_2400"]) if r["flow_0000_2400"] else None,
                                                float(r["availability_pct"]))
    jh = reg["Junctions"][0]
    junc = {r[0]: dict(zip(jh, r)) for r in reg["Junctions"][1:]}
    dh = reg["Detectors"][0]
    dreg = {r[0]: dict(zip(dh, r)) for r in reg["Detectors"][1:]}

    # golden sections
    gold = {}
    for r in read_table(os.path.join(GLD, "noise_round_sections_2025.csv")):
        gold[int(r["count_point_id"])] = (float(r["annual_traffic_2025_millions"]), r["over_three_million"] == "yes")

    def annual_mean(series):
        return statistics.fmean(v24 for (v12, v24, av) in series.values() if av >= 100 and v24 is not None)

    mine = {}
    for cp in sorted(c12):
        p = points[cp]
        road = canon(p["road_name"])
        ends = {canon(p["start_junction_road_name"]), canon(p["end_junction_road_name"])}
        js = [k for k, j in junc.items() if road in {canon(x) for x in j["junction"].split("/")}
              and ends & {canon(x) for x in j["junction"].split("/")}]
        day = cdate[cp]
        if js:
            ds = [k for k, x in dreg.items() if x["junction_ref"] == js[0] and canon(x["approach"]) == road]
            tot24 = {}
            for k in ds:
                for d, (v12, v24, av) in det[k].items():
                    if av >= 100:
                        tot24.setdefault(d, []).append(v24)
            full = [sum(v) for d, v in tot24.items() if len(v) == len(ds)]
            num = statistics.fmean(full)
            den = sum(det[k][day][0] for k in ds)
            aadf = c12[cp] * num / den
        else:
            grp = [s for s in sites if sites[s]["setting"] == p["setting"]]
            num = sum(statistics.fmean(float(v["mv_0000_2400"]) for v in atc[s].values()) for s in grp)
            den = sum(float(atc[s][day]["mv_0700_1900"]) for s in grp)
            aadf = c12[cp] * num / den
        v = aadf * 365 / 1e6
        mine[cp] = (math.floor(v * 10 + 0.5) / 10, v > 3.0)
    ok("sections: every annual figure and every over-the-line mark recomputes", mine == gold,
       "; ".join("%d %s vs %s" % (k, mine[k], gold.get(k)) for k in mine if mine[k] != gold.get(k)))

    # ask A: the switch day from the log, confirmed in the data
    m = re.search(r"(\d\d)/(\d\d)/(\d{4}) ATC network Firmware 5\.1\.3", log)
    sw = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    flips = []
    for s in sorted(atc):
        before = [float(r["class_5"]) / float(r["class_8"]) for d, r in atc[s].items() if d < sw and d.weekday() < 5 and d >= sw - dt.timedelta(28)]
        after = [float(r["class_5"]) / float(r["class_8"]) for d, r in atc[s].items() if d >= sw and d.weekday() < 5 and d < sw + dt.timedelta(28)]
        flips.append(statistics.median(before) > 1.0 > statistics.median(after))
    ok("ask A: channel 5 reads two-axle rigid lorries before the logged push and buses after it at every counter", all(flips))
    wbA = xlsx_sheets(os.path.join(GLD, "traffic_network_2025.xlsx"))
    gA = {r[0]: int(r[3]) for r in wbA["Counters"][2:]}
    mA = {}
    for s in sorted(atc):
        vals = []
        for d, r in atc[s].items():
            if d < sw:
                vals.append(sum(float(r["class_%d" % k]) for k in (5, 6, 7)))
            else:
                vals.append(sum(float(r["class_%d" % k]) for k in (6, 7, 8)))
        mA[s] = int(math.floor(statistics.fmean(vals) / 10 + 0.5) * 10)
    ok("ask A: every counter's heavy goods vehicles a day recomputes", mA == gA, str({k: (mA[k], gA.get(k)) for k in mA if mA[k] != gA.get(k)}))

    # ask B: the renewed junctions, matched by an independent route (pairs by residual correlation, arms by level ratio)
    gB = {(r[0], r[1]): int(r[2]) for r in wbA["Junction approaches"][2:]}
    mB = {}
    for jname in ("Western Avenue / Fenwick Road", "Ring Road / Tanyard Lane"):
        want = {canon(x) for x in jname.split("/")}
        ref = [k for k, j in junc.items() if {canon(x) for x in j["junction"].split("/")} == want][0]
        ds = sorted(k for k, x in dreg.items() if x["junction_ref"] == ref)
        dark = sorted(d for d in det[ds[0]] if all(det[k][d][2] == 0 for k in ds))
        sw2 = dark[1]
        pre = [sw2 - dt.timedelta(n) for n in range(3, 50)]
        post = [sw2 + dt.timedelta(n) for n in range(3, 50)]

        def detr(k, days):
            xs = [math.log(det[k][d][1]) for d in days]
            out = []
            for i, d in enumerate(days):
                same = [xs[j] for j, e in enumerate(days) if e.weekday() == d.weekday()]
                out.append(xs[i] - statistics.fmean(same))
            return out

        arms = {}
        for k in ds:
            arms.setdefault(dreg[k]["approach"], []).append(k)
        ok("ask B: the register's approach column names %d arms at %s" % (len(arms), jname), len(arms) == 4)
        res = {k: detr(k, pre) for k in ds}

        def corr(a, b):
            ma, mb = statistics.fmean(a), statistics.fmean(b)
            num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
            return num / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
        n2 = sum(1 for v in arms.values() if len(v) == 2)
        pairs = sorted(((corr(res[a], res[b]), a, b) for i, a in enumerate(ds) for b in ds[i + 1:]), reverse=True)
        used, groups = set(), []
        for c, a, b in pairs:
            if len([g for g in groups if len(g) == 2]) == n2:
                break
            if a not in used and b not in used:
                groups.append((a, b))
                used |= {a, b}
        groups += [(k,) for k in ds if k not in used]

        def lvl(ks, days):
            return statistics.fmean(sum(det[k][d][1] for k in ks) for d in days)

        def wkend(ks, days):
            return statistics.fmean(sum(det[k][d][1] for k in ks) for d in days if d.weekday() >= 5) / lvl(ks, days)
        best = None
        alist = list(arms)
        for perm in permutations(alist):
            if any(len(g) != len(arms[a]) for g, a in zip(groups, perm)):
                continue
            cost = sum(abs(math.log(lvl(g, pre) / lvl(arms[a], post))) + 3 * abs(wkend(g, pre) - wkend(arms[a], post)) for g, a in zip(groups, perm))
            if best is None or cost < best[0]:
                best = (cost, perm)
        for g, a in zip(groups, best[1]):
            total = 0.0
            for k in g:
                total += sum(v24 for d, (v12, v24, av) in det[k].items() if d < sw2 and v24 is not None)
            for k in arms[a]:
                total += sum(v24 for d, (v12, v24, av) in det[k].items() if d >= sw2 and v24 is not None)
            mB[(jname, a)] = int(math.floor(total / 1000 + 0.5))
    ok("ask B: every approach's recorded vehicles recompute", mB == gB, str({k: (mB.get(k), gB.get(k)) for k in set(mB) | set(gB) if mB.get(k) != gB.get(k)}))

    # containers: the producing application's own properties, no writer-template parts, entries at the document's date
    bad = []
    for d in (TGT, GLD):
        for fn in sorted(os.listdir(d)):
            if not fn.endswith((".xlsx", ".docx")):
                continue
            z = zipfile.ZipFile(os.path.join(d, fn))
            names = z.namelist()
            app = z.read("docProps/app.xml").decode("utf-8")
            core = z.read("docProps/core.xml").decode("utf-8")
            created = re.search(r"<dcterms:created[^>]*>(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d)", core).groups()
            stamp = tuple(int(x) for x in created)
            if not re.search(r"<AppVersion>16\.\d{4}</AppVersion>", app) or "Microsoft" not in app:
                bad.append(fn + " app.xml")
            if any(n in names for n in ("docProps/thumbnail.jpeg", "word/stylesWithEffects.xml")) or any(n.startswith("customXml/") for n in names):
                bad.append(fn + " template parts")
            if any(i.date_time[:5] != stamp for i in z.infolist()):
                bad.append(fn + " entry dates")
            blob = b"".join(z.read(n) for n in names)
            if any(t in blob for t in (b"openpyxl", b"python-docx", b"python-pptx")):
                bad.append(fn + " writer name")
    ok("containers: every xlsx and docx carries its application's own properties, no template parts, entries at its own date", not bad, str(bad))
    fails = [r for r in RES if not r[1]]
    for label, c, detail in RES:
        print("%s  %s%s" % ("PASS" if c else "FAIL", label, ("  [" + detail + "]") if detail and not c else ""))
    print("verify: %d checks, %d failed" % (len(RES), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
