"""Computes the call, every rung and every ask from the shipped files under target/ alone."""
import csv, json, os, re, zlib, base64, zipfile
from datetime import datetime, timedelta
import numpy as np
from xml.etree import ElementTree as ET
from scipy.cluster.hierarchy import linkage, fcluster

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
WEEK_UTC = (datetime(2026, 7, 12, 14, 0), datetime(2026, 7, 19, 14, 0))


def standard_constants(std_text):
    """The filed figures the call runs on, read from the adopted standard."""
    t = " ".join(std_text.split())
    ev = float(re.search(r"charger in the 2027 works schedule adds ([\d.]+) kW", t).group(1))
    ck = float(re.search(r"cooktop conversion adds ([\d.]+) kW", t).group(1))
    lim = float(re.search(r"exceeds (\d+) per cent of its rating per phase", t).group(1)) / 100.0
    volt = float(re.search(r"converted to kilowatts at (\d+) V", t).group(1))
    m = re.search(r"half-hours beginning (\d\d):(\d\d) to (\d\d):(\d\d) market time on Monday (\d+) to Friday (\d+) July 2026", t)
    first = (int(m.group(1)) * 60 + int(m.group(2))) // 30
    last = (int(m.group(3)) * 60 + int(m.group(4))) // 30
    days = list(range(int(m.group(5)), int(m.group(6)) + 1))
    return {"ev": ev, "cook": ck, "limit": lim, "volt": volt, "first": first, "last": last, "days": days}


# ------------------------------------------------------------------------------------------------ readers
def pdf_text(path):
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<((?:(?!<<|stream).)*?)>>\s*stream\r?\n(.*?)\s*endstream", raw, re.S):
        head, data = m.group(1), m.group(2)
        if b"ASCII85Decode" in head:
            d = data.strip()
            if d.endswith(b"~>"):
                d = d[:-2]
            data = base64.a85decode(d, adobe=False)
        if b"FlateDecode" in head:
            try:
                data = zlib.decompress(data)
            except zlib.error:
                continue
        out.append(data)
    text = []
    for blob in out:
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", blob, re.S):
            text.append(s.replace(rb"\(", b"(").replace(rb"\)", b")").decode("latin-1"))
    return "\n".join(text)


def xlsx_rows(path, sheet=None):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wbx = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    sheets = {}
    for s in wbx.find("m:sheets", NS):
        rid = s.get("{%s}id" % NS["r"])
        t = target[rid].lstrip("/")
        if not t.startswith("xl/"):
            t = "xl/" + t
        sheets[s.get("name")] = t
    name = sheet or list(sheets)[0]
    root = ET.fromstring(z.read(sheets[name]))
    rows = []
    for row in root.iter("{%s}row" % NS["m"]):
        rnum = int(row.get("r"))
        while len(rows) < rnum - 1:
            rows.append([])
        vals = {}
        for c in row.findall("m:c", NS):
            ref = c.get("r")
            col = 0
            for ch in re.match(r"[A-Z]+", ref).group(0):
                col = col * 26 + ord(ch) - 64
            v = c.find("m:v", NS)
            isel = c.find("m:is", NS)
            if c.get("t") == "s" and v is not None:
                val = shared[int(v.text)]
            elif c.get("t") == "inlineStr" and isel is not None:
                val = "".join(t.text or "" for t in isel.iter("{%s}t" % NS["m"]))
            elif v is not None:
                val = v.text
            else:
                val = ""
            vals[col] = val
        rows.append([vals.get(k, "") for k in range(1, (max(vals) if vals else 0) + 1)])
    return rows


def table_after(rows, first_header):
    for k, r in enumerate(rows):
        if r and r[0] == first_header:
            return r, [x for x in rows[k + 1:] if x and any(str(v).strip() for v in x)]
    raise KeyError(first_header)


# ------------------------------------------------------------------------------------------------ the pack
def load(target):
    P = lambda n: os.path.join(target, n)
    names = sorted(os.listdir(target))
    find = lambda pre: [n for n in names if n.startswith(pre)][0]
    D = {}
    hdr, rows = table_after(xlsx_rows(P(find("QES_child_meter_register"))), "Child NMI")
    D["meters"] = [dict(zip(hdr, r)) for r in rows]
    hdr, rows = table_after(xlsx_rows(P(find("OC1_register_extract_lots"))), "Lot")
    D["lots"] = [dict(zip(hdr, r)) for r in rows]
    txt = pdf_text(P(find("MSB_upgrade_2019")))
    D["msb_text"] = txt
    risers = []
    toks = txt.split("\n")
    for k, t in enumerate(toks):
        if re.fullmatch(r"[ABC][1-6]", t.strip()) and k + 4 < len(toks) and re.fullmatch(r"RM-[ABC][A-F]", toks[k + 1].strip()):
            m = re.fullmatch(r"(\d+) to (\d+)", toks[k + 2].strip())
            risers.append({"riser": t.strip(), "former": toks[k + 1].strip(), "lo": int(m.group(1)), "hi": int(m.group(2)),
                           "rating_a": int(toks[k + 4].strip())})
    D["risers"] = risers
    D["std_text"] = pdf_text(P(find("OC1_electrification_capacity_standard")))
    D["K"] = standard_constants(D["std_text"])
    hdr, rows = table_after(xlsx_rows(P(find("OC1_2027_electrification_works")), "Chargers"), "Unit")
    D["chargers"] = [dict(zip(hdr, r)) for r in rows]
    hdr, rows = table_after(xlsx_rows(P(find("OC1_2027_electrification_works")), "Cooktop conversions"), "Unit")
    D["cooktops"] = [dict(zip(hdr, r)) for r in rows]
    D["nem12"] = read_nem12(P(find("nem12_QUAYLIGHT")))
    D["pq"] = read_pq(P(find("QES_PQ_hourly_V")))
    D["pq_max"] = read_pq_max(P(find("QES_PQ_hourly_V")))
    with open(P(find("QES_PQ_events"))) as f:
        D["events"] = json.load(f)["events"]
    with open(P(find("QES_register_reads"))) as f:
        D["reads"] = list(csv.DictReader(f))
    with open(P(find("QES_meter_exchanges"))) as f:
        D["exchanges"] = list(csv.DictReader(f))
    hdr, rows = table_after(xlsx_rows(P(find("basement_remarking"))), "Space before")
    D["remark"] = {r[0]: r[1] for r in rows}
    hdr, rows = table_after(xlsx_rows(P(find("EV_charger_applications"))), "Application")
    D["apps"] = [dict(zip(hdr, r)) for r in rows]
    return D


def read_nem12(path):
    """{nmi: {yyyymmdd: [records]}}, each record carrying its 48 values, quality, register suffix and serial."""
    out = {}
    nmi = sfx = serial = None
    with open(path) as f:
        for line in f:
            p = line.rstrip("\r\n").split(",")
            if p[0] == "200":
                nmi, sfx, serial = p[1], p[4], p[6]
            elif p[0] == "300":
                vals = np.array([float(x) for x in p[2:50]])
                out.setdefault(nmi, {}).setdefault(p[1], []).append({"vals": vals, "q": p[50], "sfx": sfx, "serial": serial})
    return out


def read_pq(path):
    with open(path) as f:
        r = csv.reader(f)
        next(r)
        rows = list(r)
    series = {}
    for s, el, t, va, vmin, vmax, n in rows:
        series.setdefault((s, el), []).append((t, float(va)))
    for k in series:
        series[k].sort()
    return series


def read_pq_max(path):
    """{(meter_serial, element, hour start UTC): the hour's highest voltage}."""
    out = {}
    with open(path) as f:
        r = csv.reader(f)
        next(r)
        for s, el, t, va, vmin, vmax, n in r:
            out[(s, el, t)] = float(vmax)
    return out


# ------------------------------------------------------------------------------------------------- frames
def frame(D):
    """Units with their lot, NMI, meter, supply, riser and works items."""
    lots = {int(r["Lot"]): r for r in D["lots"]}
    units = {}
    for m in D["meters"]:
        lot = int(m["Lot"])
        u = lots[lot]["Unit"]
        tw, fl, pos = u[0], int(u[1:3]), int(u[3:5])
        rz = [r for r in D["risers"] if r["riser"][0] == tw and r["lo"] <= fl <= r["hi"]]
        assert len(rz) == 1
        units[u] = {"unit": u, "lot": lot, "nmi": m["Child NMI"], "serial": m["Meter serial"], "module": m["Comms module"],
                    "three": m["Supply"] == "3PH", "tower": tw, "floor": fl, "pos": pos, "riser": rz[0]["riser"],
                    "spaces": [s.strip() for s in lots[lot]["Accessory car spaces"].split(",") if s.strip()]}
    for c in D["chargers"]:
        units[c["Unit"].replace("-", "")]["ev"] = True
    for c in D["cooktops"]:
        units[c["Unit"].replace("-", "")]["cook"] = True
    for u in units.values():
        u.setdefault("ev", False)
        u.setdefault("cook", False)
        u["added"] = D["K"]["ev"] * u["ev"] + D["K"]["cook"] * u["cook"]
    return units


def evening_matrix(D, units, shift=0):
    """kW in each of the standard's half-hours (beginning 17:00 to 20:30 market time, 13 to 17 July)."""
    K = D["K"]
    days = ["202607%02d" % d for d in K["days"]]
    a, b = K["first"] + shift, K["last"] + 1 + shift
    M = {}
    for u, x in units.items():
        recs = D["nem12"][x["nmi"]]
        col = []
        for d in days:
            v = sum(r["vals"] for r in recs[d])
            col.extend(list(v[a:b] * 2.0))
        M[u] = np.array(col)
    return M


def phase_groups(D, units, method="det_hier"):
    """Each riser's single-phase apartments sorted into three groups by how their hourly voltages move together."""
    groups = {}
    for r in D["risers"]:
        us = sorted([u for u, x in units.items() if x["riser"] == r["riser"]])
        sp = [u for u in us if not units[u]["three"]]
        allser = []
        for u in us:
            x = units[u]
            if x["three"]:
                els = [np.array([v for _, v in D["pq"][(x["serial"], e)]]) for e in "123"]
                allser.append(np.mean(els, axis=0))
            else:
                allser.append(np.array([v for _, v in D["pq"][(x["serial"], "1")]]))
        A = np.array(allser)
        X = np.array([A[us.index(u)] for u in sp])
        if method == "det_hier":
            Xd = X - A.mean(0, keepdims=True)
            lab = fcluster(linkage(Xd, "average", metric="correlation"), 3, "maxclust") - 1
        elif method == "raw_hier":
            lab = fcluster(linkage(X, "average", metric="correlation"), 3, "maxclust") - 1
        elif method == "diff_complete":
            lab = fcluster(linkage(np.diff(X, axis=1), "complete", metric="correlation"), 3, "maxclust") - 1
        elif method == "det_ward":
            Xd = X - A.mean(0, keepdims=True)
            Z = (Xd - Xd.mean(1, keepdims=True)) / Xd.std(1, keepdims=True)
            lab = fcluster(linkage(Z, "ward"), 3, "maxclust") - 1
        else:
            raise ValueError(method)
        # canonical labels: group of the lowest unit number first
        order = []
        for u, l in zip(sp, lab):
            if l not in order:
                order.append(l)
        canon = {l: k for k, l in enumerate(order)}
        groups[r["riser"]] = {u: canon[l] for u, l in zip(sp, lab)}
    return groups


def busiest(units, M, riser, assign, rating, volt=230.0):
    """Busiest-phase demand (kW) with its share of the per-phase rating, for one phase assignment."""
    us = [u for u, x in units.items() if x["riser"] == riser]
    S = np.zeros((3, len(next(iter(M.values())))))
    A = np.zeros(3)
    for u in us:
        x = units[u]
        if x["three"]:
            S += M[u] / 3
            A += x["added"] / 3
        else:
            p = assign[u]
            S[p] += M[u]
            A[p] += x["added"]
    ph = S.max(1) + A
    k = int(np.argmax(ph))
    cap = rating * volt / 1000.0
    return float(ph[k]), float(ph[k] / cap * 100.0), [float(v / cap * 100.0) for v in ph]


def call(D, units=None, M=None, groups=None):
    units = units or frame(D)
    M = M if M is not None else evening_matrix(D, units)
    groups = groups or phase_groups(D, units)
    res = {}
    K = D["K"]
    for r in D["risers"]:
        kw, share, per = busiest(units, M, r["riser"], groups[r["riser"]], r["rating_a"], K["volt"])
        res[r["riser"]] = {"kw": kw, "share": share, "per_phase": per, "rating_a": r["rating_a"]}
    designated = [k for k, v in res.items() if v["share"] > K["limit"] * 100]
    rest = [k for k in res if k not in designated]
    nearest = max(rest, key=lambda k: res[k]["share"]) if rest else None
    return {"risers": res, "designated": designated, "nearest": nearest}


def rungs(D, units=None, M=None, sims=20000, seed=7):
    """Rung 0 balanced, rung 1 the installer's rotation by position, rung 2 the expected busiest phase over
    random phasing."""
    units = units or frame(D)
    M = M if M is not None else evening_matrix(D, units)
    out = {}
    rng = np.random.default_rng(seed)
    for r in D["risers"]:
        rid = r["riser"]
        us = [u for u, x in units.items() if x["riser"] == rid]
        K = D["K"]
        cap = r["rating_a"] * K["volt"] / 1000.0
        tot = sum(M[u] for u in us)
        bal = (tot.max() + sum(units[u]["added"] for u in us)) / 3 / cap * 100
        rot = {u: (units[u]["pos"] - 1) % 3 for u in us if not units[u]["three"]}
        _, rs, _ = busiest(units, M, rid, rot, r["rating_a"], K["volt"])
        sp = [u for u in us if not units[u]["three"]]
        three = [u for u in us if units[u]["three"]]
        nt = len(next(iter(M.values())))
        base3 = sum((M[u] / 3 for u in three), np.zeros(nt))
        add3 = sum(units[u]["added"] / 3 for u in three)
        Ms = np.array([M[u] for u in sp])
        As = np.array([units[u]["added"] for u in sp])
        draws = rng.integers(0, 3, size=(sims, len(sp)))
        best = np.zeros(sims)
        for p in range(3):
            m = (draws == p).astype(float)
            ph = (m @ Ms + base3).max(1) + m @ As + add3
            best = np.maximum(best, ph)
        sim = float(best.mean() / cap * 100)
        out[rid] = {"balanced": float(bal), "rotation": float(rs), "simulated": sim}
    sets = {k: [rid for rid, v in out.items() if v[k] > D["K"]["limit"] * 100] for k in ("balanced", "rotation", "simulated")}
    return out, sets


# --------------------------------------------------------------------------------------------------- asks
def midnight_reads(D):
    """{(meter_serial, register, date): (reading, read type)} for the reads taken at midnight."""
    out = {}
    for r in D["reads"]:
        if r["read_local"][11:] == "00:00":
            out[(r["meter_serial"], r["register"], r["read_local"][:10])] = (float(r["reading_kwh"]), r["read_type"])
    return out


def ask_july_use(D, units):
    """Each riser's apartments' July 2026 use (MWh): the energy each meter registered over July on both registers,
    from the midnight register reads of 1 July and 1 August (through the exchange log where a meter was changed)
    and, where the midnight 1 August read is an estimate, from the meter's own July interval data."""
    reads = midnight_reads(D)
    ex = {e["nmi"]: e for e in D["exchanges"]}
    per_unit = {}
    for u, x in units.items():
        regs = [g for g in ("E1", "E2") if (x["serial"], g, "2026-08-01") in reads]
        if any(reads[(x["serial"], g, "2026-08-01")][1] != "A" for g in regs):
            recs = D["nem12"][x["nmi"]]
            per_unit[u] = sum(r["vals"].sum() for d in recs for r in recs[d])
            continue
        use = 0.0
        for reg in regs:
            if x["nmi"] in ex:
                e = ex[x["nmi"]]
                use += (float(e["old_final_%s_kwh" % reg]) - reads[(e["old_meter_serial"], reg, "2026-07-01")][0]) + \
                       (reads[(e["new_meter_serial"], reg, "2026-08-01")][0] - float(e["new_initial_%s_kwh" % reg]))
            else:
                use += reads[(x["serial"], reg, "2026-08-01")][0] - reads[(x["serial"], reg, "2026-07-01")][0]
        per_unit[u] = use
    out = {}
    for r in D["risers"]:
        out[r["riser"]] = sum(v for u, v in per_unit.items() if units[u]["riser"] == r["riser"]) / 1000.0
    return out, per_unit


def parse_unit(txt):
    """A unit written as A1402, A-1402, 1402/A or Apt 14.02 Tower A; None for an owner's postal address."""
    t = txt.strip()
    m = re.fullmatch(r"([ABC])-?(\d{2})(\d{2})(?: \(for the OC\))?", t)
    if m:
        return "%s%s%s" % m.groups()
    m = re.fullmatch(r"(\d{2})(\d{2})/([ABC])", t)
    if m:
        return "%s%s%s" % (m.group(3), m.group(1), m.group(2))
    m = re.fullmatch(r"Apt (\d{1,2})\.(\d{2}) Tower ([ABC])", t)
    if m:
        return "%s%02d%s" % (m.group(3), int(m.group(1)), m.group(2))
    return None


def parse_lot(txt):
    """The lot an owner writing from another address gives (Lot 214, 3/45 Hyde St, ...); None otherwise."""
    m = re.match(r"Lot (\d+), ", txt.strip())
    return int(m.group(1)) if m else None


def applicant_spaces(a, D, units):
    """The accessory car spaces of the applicant's lot, by the unit written or the lot given; None for the
    committee's own applications."""
    w = a["Unit or owner address"]
    if "(for the OC)" in w:
        return None
    u = parse_unit(w)
    if u is not None:
        return set(units[u]["spaces"])
    lot = parse_lot(w)
    if lot is not None:
        row = [r for r in D["lots"] if int(r["Lot"]) == lot][0]
        return {s_.strip() for s_ in row["Accessory car spaces"].split(",") if s_.strip()}
    return None


def candidate_spaces(a, D):
    """The car spaces an application's written number can mean: before the March 2025 re-marking only the old
    numbering existed; after it, a B2 or B3 number may be new or an owner's old one."""
    sp = a["Car space"].strip()
    if sp[:3] not in ("B2-", "B3-"):
        return [sp]
    if datetime.strptime(a["Lodged"], "%d/%m/%Y") < datetime(2025, 3, 15):
        return [D["remark"][sp]]
    return [sp, D["remark"][sp]] if D["remark"][sp] != sp else [sp]


def true_space(a, D, units):
    """The car space an application means: the candidate that is one of the applicant's own spaces."""
    cands = candidate_spaces(a, D)
    own = applicant_spaces(a, D, units)
    if own is None or len(cands) == 1:
        return cands[0]
    mine = [c for c in cands if c in own]
    return mine[0] if len(mine) == 1 else cands[0]


def ask_requests(D, units):
    """Each riser's charger requests: one per car space, on the riser of the apartment the space is accessory to."""
    space_unit = {}
    for u, x in units.items():
        for s_ in x["spaces"]:
            space_unit[s_] = u
    reqs = {}
    for a in D["apps"]:
        reqs.setdefault(true_space(a, D, units), []).append(a)
    out = {r["riser"]: 0 for r in D["risers"]}
    for sp in reqs:
        if sp in space_unit:
            out[units[space_unit[sp]]["riser"]] += 1
    return out, reqs


def excursion_record(e, D):
    """A record is a time the meter recorded its supply outside the limits only if the meter's own hourly maxima
    go above the upper limit in an hour the record covers (records outside the hourly export are kept)."""
    s = datetime.strptime(e["start_utc"], "%Y-%m-%dT%H:%M:%SZ")
    t = datetime.strptime(e["end_utc"], "%Y-%m-%dT%H:%M:%SZ")
    h = s.replace(minute=0, second=0)
    seen = False
    while h < t:
        v = D["pq_max"].get((e["meter_serial"], e["element"], h.strftime("%Y-%m-%dT%H:%M:%SZ")))
        if v is not None:
            seen = True
            if v > 253.0:
                return True
        h += timedelta(hours=1)
    return not seen


def ask_voltage(D, units):
    """Each riser's share of its apartments' time in the week of 13 to 19 July (market time) outside the limits:
    per apartment, the union of its meter's excursion records over every element, clipped to the week; a record
    in hours when the meter's own hourly maxima stay inside the limits records no time outside them."""
    ser_unit = {x["serial"]: u for u, x in units.items()}
    iv = {}
    for e in D["events"]:
        u = ser_unit.get(e["meter_serial"])
        if u is None or not excursion_record(e, D):
            continue
        s = datetime.strptime(e["start_utc"], "%Y-%m-%dT%H:%M:%SZ")
        t = datetime.strptime(e["end_utc"], "%Y-%m-%dT%H:%M:%SZ")
        s, t = max(s, WEEK_UTC[0]), min(t, WEEK_UTC[1])
        if t > s:
            iv.setdefault(u, []).append((s, t))
    secs = {}
    for u, lst in iv.items():
        lst.sort()
        tot = 0.0
        cs, ce = lst[0]
        for s, t in lst[1:]:
            if s <= ce:
                ce = max(ce, t)
            else:
                tot += (ce - cs).total_seconds()
                cs, ce = s, t
        tot += (ce - cs).total_seconds()
        secs[u] = tot
    week = 7 * 86400.0
    out = {}
    for r in D["risers"]:
        us = [u for u, x in units.items() if x["riser"] == r["riser"]]
        out[r["riser"]] = sum(secs.get(u, 0.0) for u in us) / (len(us) * week) * 100.0
    return out, secs


def everything(target):
    D = load(target)
    units = frame(D)
    M = evening_matrix(D, units)
    groups = phase_groups(D, units)
    C = call(D, units, M, groups)
    R, sets = rungs(D, units, M)
    A1, per_unit = ask_july_use(D, units)
    A2, reqs = ask_requests(D, units)
    A3, secs = ask_voltage(D, units)
    return {"D": D, "units": units, "M": M, "groups": groups, "call": C, "rungs": R, "rung_sets": sets,
            "july_mwh": A1, "requests": A2, "voltage_pct": A3, "per_unit_use": per_unit, "reqs": reqs, "secs": secs}


if __name__ == "__main__":
    import sys
    E = everything(sys.argv[1])
    C = E["call"]
    print("designated", C["designated"], "nearest", C["nearest"])
    for k, v in C["risers"].items():
        print(k, "%.2f%%" % v["share"], "%.1f kW" % v["kw"], "| bal %.2f rot %.2f sim %.2f" % tuple(E["rungs"][k][x] for x in ("balanced", "rotation", "simulated")),
              "| July %.3f MWh" % E["july_mwh"][k], "| req %d" % E["requests"][k], "| V %.3f%%" % E["voltage_pct"][k])
    print(E["rung_sets"])
