"""Independent verifier: reads only the shipped bundle (target/, golden/, figures.json, submission.md), on its
own parsers, and recomputes the call, the critical components and every ask.  Exit 1 on any mismatch."""
import csv, io, json, os, re, sys, zipfile, zlib
from datetime import datetime, timedelta
import numpy as np

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ------------------------------------------------------------------------------------- own format readers
def a85(b):
    """ASCII85 decoder written out by hand (Adobe framing stripped)."""
    b = re.sub(rb"\s", b"", b)
    if b.startswith(b"<~"):
        b = b[2:]
    if b.endswith(b"~>"):
        b = b[:-2]
    out = bytearray()
    group = []
    for ch in b:
        if ch == ord("z") and not group:
            out += b"\0\0\0\0"
            continue
        group.append(ch - 33)
        if len(group) == 5:
            n = 0
            for g in group:
                n = n * 85 + g
            out += n.to_bytes(4, "big")
            group = []
    if group:
        k = len(group)
        group += [84] * (5 - k)
        n = 0
        for g in group:
            n = n * 85 + g
        out += n.to_bytes(4, "big")[:k - 1]
    return bytes(out)


def pdf_strings(path):
    data = open(path, "rb").read()
    texts = []
    pos = 0
    while True:
        i = data.find(b"stream", pos)
        if i < 0:
            break
        j = data.find(b"endstream", i)
        head = data[data.rfind(b"<<", 0, i):i]
        body = data[i + 6:j].strip(b"\r\n")
        pos = j + 9
        if b"/Filter" not in head:
            continue
        try:
            if b"ASCII85" in head:
                body = a85(body)
            if b"Flate" in head:
                body = zlib.decompressobj().decompress(body)
        except Exception:
            continue
        for m in re.finditer(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", body):
            texts.append(m.group(1).replace(b"\\(", b"(").replace(b"\\)", b")").decode("latin-1"))
    return texts


def xlsx(path, sheet):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    ss = []
    if "xl/sharedStrings.xml" in names:
        x = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            ss.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    rid = re.search(r'<sheet[^>]*name="%s"[^>]*r:id="(rId\d+)"' % re.escape(sheet), wb).group(1)
    tgt = re.search(r'<Relationship[^>]*Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or \
        re.search(r'<Relationship[^>]*Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
    t = tgt.group(1).lstrip("/")
    t = t if t.startswith("xl/") else "xl/" + t
    x = z.read(t).decode("utf-8")
    rows = {}
    for rnum, body in re.findall(r'<row r="(\d+)"[^>]*>(.*?)</row>', x, re.S):
        cells = {}
        for ref, attrs, inner in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(.*?)</c>', body, re.S):
            col = 0
            for ch in ref:
                col = col * 26 + ord(ch) - 64
            v = re.search(r"<v>(.*?)</v>", inner, re.S)
            if 't="s"' in attrs:
                val = ss[int(v.group(1))]
            elif 't="inlineStr"' in attrs:
                val = "".join(re.findall(r"<t[^>]*>(.*?)</t>", inner, re.S))
            else:
                val = v.group(1) if v else ""
            cells[col] = val.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        rows[int(rnum)] = cells
    return rows


def grid(rows, first):
    hr = [r for r, c in rows.items() if c.get(1) == first][0]
    hdr = rows[hr]
    out = []
    for r in sorted(rows):
        if r > hr and rows[r].get(1, "") != "":
            out.append({hdr[k]: rows[r].get(k, "") for k in hdr})
    return out


# ----------------------------------------------------------------------------------------------- recompute
def main():
    T = os.path.join(TASK, "target")
    names = os.listdir(T)
    f = lambda pre: os.path.join(T, [n for n in names if n.startswith(pre)][0])
    fails = []

    def check(label, cond):
        if not cond:
            fails.append(label)
        print(("PASS  " if cond else "FAIL  ") + label)

    std = " ".join(pdf_strings(f("OC1_electrification_capacity_standard")))
    check("standard PDF read through the verifier's own decoder", "A charger request is an owner" in std)
    ev = float(re.search(r"adds ([\d.]+) kW and each cooktop", std).group(1))
    ck = float(re.search(r"cooktop conversion adds ([\d.]+) kW", std).group(1))
    lim = float(re.search(r"exceeds (\d+) per cent", std).group(1))
    volt = float(re.search(r"kilowatts at (\d+) V", std).group(1))
    msb = pdf_strings(f("MSB_upgrade_2019"))
    risers = {}
    for k, s in enumerate(msb):
        if re.fullmatch(r"[ABC][1-6]", s) and k + 4 < len(msb) and msb[k + 1].startswith("RM-"):
            lo, hi = [int(v) for v in msb[k + 2].split(" to ")]
            risers[s] = (s[0], lo, hi, int(msb[k + 4]))
    check("rising main schedule PDF read: 18 mains", len(risers) == 18)
    meters = grid(xlsx(f("QES_child_meter_register"), "Child meters"), "Child NMI")
    lots = {int(r["Lot"]): r for r in grid(xlsx(f("OC1_register_extract_lots"), "Lots"), "Lot")}
    units = {}
    for m in meters:
        lot = lots[int(m["Lot"])]
        u = lot["Unit"]
        rz = [k for k, v in risers.items() if v[0] == u[0] and v[1] <= int(u[1:3]) <= v[2]][0]
        units[u] = dict(nmi=m["Child NMI"], serial=m["Meter serial"], three=m["Supply"] == "3PH", riser=rz,
                        spaces=[s.strip() for s in lot["Accessory car spaces"].split(",") if s.strip()], add=0.0)
    for r in grid(xlsx(f("OC1_2027_electrification_works"), "Chargers"), "Unit"):
        units[r["Unit"].replace("-", "")]["add"] += ev
    for r in grid(xlsx(f("OC1_2027_electrification_works"), "Cooktop conversions"), "Unit"):
        units[r["Unit"].replace("-", "")]["add"] += ck
    # NEM12, own pass: evening kW per NMI over 13 to 17 July
    evening = {}
    nmi = None
    allsum = {}
    for line in open(f("nem12_QUAYLIGHT")):
        p = line.strip().split(",")
        if p[0] == "200":
            nmi = p[1]
        elif p[0] == "300":
            vals = np.array(p[2:50], dtype=float)
            allsum[nmi] = allsum.get(nmi, 0.0) + vals.sum()
            if "20260713" <= p[1] <= "20260717":
                key = (nmi, p[1])
                evening[key] = evening.get(key, np.zeros(8)) + vals[34:42] * 2
    # PQ: hourly averages per serial
    pq = {}
    with open(f("QES_PQ_hourly_V")) as fh:
        rd = csv.DictReader(fh)
        for r in rd:
            pq.setdefault(r["meter_serial"], {}).setdefault(r["element"], []).append((r["interval_start_utc"], float(r["v_avg"])))
    # phase groups: iterative correlation-to-centroid assignment, its own method
    shares = {}
    for rid in sorted(risers):
        us = sorted(u for u in units if units[u]["riser"] == rid)
        series = {}
        for u in us:
            el = pq[units[u]["serial"]]
            series[u] = np.mean([np.array([v for _, v in sorted(el[e])]) for e in sorted(el)], axis=0)
        mean = np.mean([series[u] for u in us], axis=0)
        sp = [u for u in us if not units[u]["three"]]
        X = np.array([series[u] - mean for u in sp])
        X = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
        Cm = X @ X.T / X.shape[1]
        # seeds: the first unit, then the units least correlated with the seeds chosen so far
        seeds = [0]
        while len(seeds) < 3:
            seeds.append(int(np.argmin(np.max(Cm[:, seeds], axis=1))))
        lab = np.argmax(Cm[:, seeds], axis=1)
        for _ in range(20):
            cent = np.array([X[lab == k].mean(0) for k in range(3)])
            new = np.argmax(X @ cent.T, axis=1)
            if (new == lab).all():
                break
            lab = new
        S = np.zeros((3, 40))
        Ad = np.zeros(3)
        for u in us:
            vec = np.concatenate([evening[(units[u]["nmi"], "202607%02d" % d)] for d in range(13, 18)])
            if units[u]["three"]:
                S += vec / 3
                Ad += units[u]["add"] / 3
            else:
                k = lab[sp.index(u)]
                S[k] += vec
                Ad[k] += units[u]["add"]
        shares[rid] = float(((S.max(1) + Ad).max()) / (risers[rid][3] * volt / 1000) * 100)
    designated = sorted(k for k, v in shares.items() if v > lim)
    rest = [k for k in shares if k not in designated]
    nearest = max(rest, key=lambda k: shares[k]) if rest else None
    F = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    check("call: designated rising mains recompute (%s)" % ", ".join(designated), designated == sorted(F["designated"]))
    for k in designated:
        check("component: %s share of rating %d%%" % (k, round(shares[k])), round(shares[k]) == F["share_pct"][k])
    check("component: nearest undesignated %s at %d%%" % (nearest, round(shares[nearest])),
          nearest == F["nearest"] and round(shares[nearest]) == F["nearest_share_pct"])
    # ask A: July use from the reads (estimated 1 August reads replaced by the meter's own July intervals)
    reads, rtype = {}, {}
    with open(f("QES_register_reads")) as fh:
        for r in csv.DictReader(fh):
            reads[(r["meter_serial"], r["register"], r["read_local"][:10])] = float(r["reading_kwh"])
            rtype[(r["meter_serial"], r["register"], r["read_local"][:10])] = r["read_type"]
    exch = {}
    with open(f("QES_meter_exchanges")) as fh:
        for r in csv.DictReader(fh):
            exch[r["nmi"]] = r
    use = {}
    for u, x in units.items():
        regs = [g for g in ("E1", "E2") if (x["serial"], g, "2026-08-01") in reads]
        if any(rtype[(x["serial"], g, "2026-08-01")] != "A" for g in regs):
            use[u] = allsum[x["nmi"]]
            continue
        t = 0.0
        for g in regs:
            if x["nmi"] in exch:
                e = exch[x["nmi"]]
                t += float(e["old_final_%s_kwh" % g]) - reads[(e["old_meter_serial"], g, "2026-07-01")] + \
                    reads[(e["new_meter_serial"], g, "2026-08-01")] - float(e["new_initial_%s_kwh" % g])
            else:
                t += reads[(x["serial"], g, "2026-08-01")] - reads[(x["serial"], g, "2026-07-01")]
        use[u] = t
    for rid in sorted(risers):
        v = round(sum(use[u] for u in units if units[u]["riser"] == rid) / 1000, 2)
        check("ask A: %s July use %.2f MWh" % (rid, v), abs(v - F["july_mwh"][rid]) < 0.001)
    # ask B: requests per car space
    remark = {r["Space before"]: r["Space after"] for r in grid(xlsx(f("basement_remarking"), "B2 and B3 re-marking"), "Space before")}
    apps = grid(xlsx(f("EV_charger_applications"), "Applications"), "Application")
    owner = {s: u for u, x in units.items() for s in x["spaces"]}
    spaces = set()
    for a in apps:
        sp = a["Car space"].strip()
        if sp[:3] in ("B2-", "B3-"):
            if datetime.strptime(a["Lodged"], "%d/%m/%Y") < datetime(2025, 3, 15):
                sp = remark[sp]
            else:
                w = a["Unit or owner address"]
                m = re.match(r"([ABC])-?(\d{4})$", w) or re.match(r"(\d{4})/([ABC])$", w)
                m2 = re.match(r"Apt (\d+)\.(\d{2}) Tower ([ABC])$", w)
                cand = None
                if m and m.re.pattern.startswith("([ABC])"):
                    cand = m.group(1) + m.group(2)
                elif m:
                    cand = m.group(2) + m.group(1)
                elif m2:
                    cand = "%s%02d%s" % (m2.group(3), int(m2.group(1)), m2.group(2))
                if cand and owner.get(sp) != cand and owner.get(remark.get(sp)) == cand:
                    sp = remark[sp]
        spaces.add(sp)
    reqs = {rid: 0 for rid in risers}
    for sp in spaces:
        if sp in owner:
            reqs[units[owner[sp]]["riser"]] += 1
    for rid in sorted(risers):
        check("ask B: %s requests %d" % (rid, reqs[rid]), reqs[rid] == F["requests"][rid])
    # ask C: union of each apartment's records in the market-time week
    ev_doc = json.load(open(f("QES_PQ_events")))
    lo, hi = datetime(2026, 7, 12, 14), datetime(2026, 7, 19, 14)
    by = {}
    s2u = {x["serial"]: u for u, x in units.items()}
    for e in ev_doc["events"]:
        u = s2u.get(e["meter_serial"])
        if not u:
            continue
        s = max(datetime.strptime(e["start_utc"], "%Y-%m-%dT%H:%M:%SZ"), lo)
        t = min(datetime.strptime(e["end_utc"], "%Y-%m-%dT%H:%M:%SZ"), hi)
        if t > s:
            by.setdefault(u, []).append((s, t))
    secs = {}
    for u, iv in by.items():
        iv.sort()
        tot, cur = 0.0, list(iv[0])
        for s, t in iv[1:]:
            if s <= cur[1]:
                cur[1] = max(cur[1], t)
            else:
                tot += (cur[1] - cur[0]).total_seconds()
                cur = [s, t]
        secs[u] = tot + (cur[1] - cur[0]).total_seconds()
    for rid in sorted(risers):
        us = [u for u in units if units[u]["riser"] == rid]
        v = round(sum(secs.get(u, 0) for u in us) / (len(us) * 7 * 86400) * 100, 2)
        check("ask C: %s time outside %.2f%%" % (rid, v), abs(v - F["voltage_pct"][rid]) < 0.001)
    # the goldens carry the same figures
    G = os.path.join(TASK, "golden")
    wbrows = xlsx(os.path.join(G, "riser_capacity_2027.xlsx"), "Rising mains")
    tab = grid(wbrows, "Rising main")
    ok = True
    for r in tab:
        rid = r["Rising main"]
        if rid in F["july_mwh"]:
            ok &= abs(float(r["July 2026 use (MWh)"]) - F["july_mwh"][rid]) < 1e-9
            ok &= int(float(r["Charger requests lodged"])) == F["requests"][rid]
            ok &= abs(float(r["Time outside 216-253 V, week of 13 July (%)"]) - F["voltage_pct"][rid]) < 1e-9
            ok &= int(float(r["Busiest phase, share of rating (%)"])) == round(shares[rid])
    check("golden workbook carries every riser's figures as recomputed", ok and len(tab) == 18)
    svg = open(os.path.join(G, "riser_phase_loading_2027.svg")).read()
    check("golden chart is an SVG with the 80% limit and every main", "80% limit" in svg and all(k in svg for k in risers))
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("submission names every designated main", all(k in sub for k in designated))
    print("\n%d failures" % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
