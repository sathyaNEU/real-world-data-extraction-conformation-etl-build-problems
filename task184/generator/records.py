"""The two recording systems' exports.

Kelverstoke City Police moved from its crime information system to a records management system class by class
through 2025. The five classes the patrol contract covers moved in January and February, before either season
opens, so the records management export holds them whole. The four witnessed classes moved on 28 July 2025, and
for the fortnight of 14 to 27 July three of them were written to both systems, each under that system's own
reference. The records management export carries a location code for every offence the contract covers, because
the tasking contract is settled on them; for the witnessed classes the code is whatever the call handler entered,
and often nothing, so those rows reach a location only through their address.
"""
import datetime as dt

import numpy as np

import places as PL
import world as W

RMS = "kcp_rms_offence_extract_2027-01-22.csv"
LEGACY = "kcp_cis_offence_extract_2025.csv"

# the street number ranges the register gives the quarter
NUMBERS = {
    "Harbourgate Street": (2, 178, 2),
    "Quayside": (1, 1, 1),
    "Lamphouse Lane": (1, 63, 1),
    "Fishmarket Square": (1, 28, 1),
    "Netherbow Wynd": (14, 14, 1),
}
ALT = {"Harbourgate Street": "Harbour Gate Street", "Lamphouse Lane": "Lamp House Lane"}
FRINGE_STREET = "Harbourgate Street"          # Cranstoun's street of the same name, numbered above 178
UNCODED_SHARE = 0.22                          # witnessed-class rows the call handler left without a location code
ALT_SHARE = 0.38                              # uncoded rows written with the gazetteer's alternative spelling
FRINGE_PER_SEASON = 310                       # offences on Cranstoun's Harbourgate Street caught by the extract


def rng(k):
    return np.random.default_rng([W.SEED, 5, k, W.NUDGE])


def in_legacy(r):
    """Was the offence recorded in the crime information system? Only the witnessed classes, and only until the
    system stopped taking them on 27 July 2025."""
    return r["cls"] not in W.CONTRACTED and r["reported"].date() <= W.MIGRATION[r["cls"]] - dt.timedelta(days=1)


def in_rms(r):
    """Was it recorded in the records management system? Everything the contract covers, and the witnessed classes
    from the day their class migrated, plus the fortnight of parallel running for the three that were double
    written."""
    if r["cls"] in W.CONTRACTED:
        return True
    d = r["reported"].date()
    if d >= W.MIGRATION[r["cls"]]:
        return True
    return r["cls"] in W.LEGACY_NAMES and r["cls"] != "Theft from the person" and W.PARALLEL[0] <= d <= W.PARALLEL[1]


def address(street, number, alt):
    name = ALT[street] if alt and street in ALT else street
    if street == "Quayside":
        return "Quayside Multi-Storey, Quayside"
    if street == "Netherbow Wynd":
        return "Netherbow Car Park, 14 Netherbow Wynd"
    return "%d %s" % (number, name)


def decorate(rows):
    """Give every offence its references, its address as each system wrote it, and whether its location code was
    entered. Mutates the rows."""
    g = rng(1)
    seq = {}
    for i, r in enumerate(rows):
        year = r["from"].year
        seq[year] = seq.get(year, 0) + 1
        r["ref"] = "KC/%d/%06d" % (year, 100000 + seq[year] * 3 + (i % 3))
        street = PL.REG[W.LOCATIONS.index(r["loc"])][2]
        lo, hi, step = NUMBERS[street]
        n = int(lo + step * g.integers(0, max(1, (hi - lo) // step + 1)))
        alt = bool(g.random() < ALT_SHARE)
        r["street"], r["number"] = street, n
        r["address"] = address(street, n, alt)
        r["coded"] = r["cls"] in W.CONTRACTED or g.random() >= UNCODED_SHARE
        r["beat"] = PL.REG[W.LOCATIONS.index(r["loc"])][5]
    lg = rng(2)
    k = 0
    for r in rows:
        if in_legacy(r) or (in_rms(r) and r["cls"] in W.LEGACY_NAMES and
                            W.PARALLEL[0] <= r["reported"].date() <= W.PARALLEL[1]):
            k += 1
            r["cis"] = "CIS-%02d-%05d" % (r["from"].year % 100, 14000 + k * 2 + int(lg.integers(0, 2)))
    return rows


def fringe():
    """The offences the extract caught on the Cranstoun length of Harbourgate Street, which carries the same street
    name as the quarter's and is numbered above the quarter's 178. They are not in the quarter: the classes under a
    tasking agreement carry Cranstoun's own location codes, and the rest carry the address alone."""
    import offences as O
    out = []
    g = rng(3)
    classes = list(W.CLASSES)
    for si in range(len(W.SEASONS)):
        days = W.season_days(si)
        for j in range(FRINGE_PER_SEASON):
            cls = classes[int(g.integers(0, len(classes)))]
            kind = W.CLASSES[cls][1]
            if kind == "routine":
                by_dow = {k: [x for x in days if x.weekday() == k] for k in range(7)}
                at, end, _true = O.covered_record(cls, g, by_dow, W.SEASONS[si])
            else:
                d = days[int(g.integers(0, len(days)))]
                sh, _ln = O.window(kind, g, 1)
                at = (dt.datetime.combine(d, dt.time()) +
                      dt.timedelta(hours=float(sh[0]))).replace(second=0, microsecond=0)
                end = at
            n = int(180 + 2 * g.integers(0, 60))
            alt = bool(g.random() < ALT_SHARE)
            coded = cls in W.CONTRACTED
            out.append({
                "cls": cls, "season": si, "from": at, "to": end, "true": at,
                "reported": (end + dt.timedelta(hours=float(g.gamma(1.6, 5.0)))).replace(second=0, microsecond=0),
                "loc": None, "street": FRINGE_STREET, "number": n,
                "address": address(FRINGE_STREET, n, alt), "coded": coded, "beat": "KC-06",
                "code": PL.CRANSTOUN[int(g.integers(0, len(PL.CRANSTOUN)))] if coded else "",
                "ref": None,
            })
    out.sort(key=lambda r: (r["reported"], r["cls"]))
    g2 = rng(4)
    for i, r in enumerate(out):
        year = r["from"].year
        r["ref"] = "KC/%d/%06d" % (year, 700000 + i * 2 + int(g2.integers(0, 2)))
        if r["cls"] not in W.CONTRACTED and r["reported"].date() <= W.MIGRATION[r["cls"]] - dt.timedelta(days=1):
            r["cis"] = "CIS-%02d-%05d" % (year % 100, 60000 + i * 2)
    return out


def unique_keys(*groups):
    """No two offences of a witnessed class share a class, an occurrence time and an address. Those are the classes
    the two systems both held through the parallel fortnight, so the occurrence details are what reconciles the two
    exports, and a recording officer does not file two reports at the same minute for the same address."""
    seen = set()
    for rows in groups:
        for r in rows:
            if r["cls"] not in W.LEGACY_NAMES:
                continue
            key = (r["cls"], r["from"], r["to"], r["address"])
            while key in seen:
                r["from"] += dt.timedelta(minutes=1)
                r["to"] = r["from"]
                r["true"] = r["from"]
                key = (r["cls"], r["from"], r["to"], r["address"])
            seen.add(key)
    return groups


def fmt(ts):
    return ts.strftime("%Y-%m-%d %H:%M")


def rms_rows(rows, fr):
    head = ("crime_reference", "offence_class", "occurred_from", "occurred_to", "reported_at", "location_code",
            "address_text", "beat_code", "record_status")
    out = []
    for r in list(rows) + list(fr):
        if not in_rms(r):
            continue
        code = PL.CODE[r["loc"]] if (r["coded"] and r["loc"]) else r.get("code", "")
        out.append([r["ref"], r["cls"], fmt(r["from"]), fmt(r["to"]) if r["to"] > r["from"] else fmt(r["from"]),
                    fmt(r["reported"]), code, r["address"], r["beat"], "recorded"])
    out.sort(key=lambda x: (x[4], x[0]))
    return [head] + out


def legacy_rows(rows, fr):
    head = ("cis_ref", "offence_type", "occ_from_date", "occ_from_time", "occ_to_date", "occ_to_time",
            "address_text", "beat", "recorded_date")
    out = []
    for r in list(rows) + list(fr):
        if "cis" not in r:
            continue
        out.append([r["cis"], W.LEGACY_NAMES[r["cls"]],
                    r["from"].strftime("%d/%m/%Y"), r["from"].strftime("%H:%M"),
                    r["to"].strftime("%d/%m/%Y") if r["to"] > r["from"] else "",
                    r["to"].strftime("%H:%M") if r["to"] > r["from"] else "",
                    r["address"], r["beat"], r["reported"].strftime("%d/%m/%Y")])
    out.sort(key=lambda x: (x[8].split("/")[::-1], x[0]))
    return [head] + out
