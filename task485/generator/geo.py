"""Lorrimere District's addresses: streets, numbers, blocks of flats, postcodes, UPRNs, the old and new electoral
management systems' property references, polling districts before and after the 2024 review, and parishes."""
import numpy as np

import world as W

STREET_STEMS = ["Mill", "Church", "Station", "Chapel", "Victoria", "Albert", "Park", "School", "Manor", "Orchard",
                "Willow", "Beech", "Elm", "Oak", "Ash", "Cedar", "Holly", "Rowan", "Hazel", "Linden", "Bridge",
                "Brook", "Meadow", "Field", "Green", "Hill", "Spring", "Well", "Grange", "Priory", "Abbey", "Castle",
                "Market", "North", "South", "West", "East", "High", "Back", "Low", "Kings", "Queens", "Princes",
                "York", "Windsor", "Stanley", "Cromwell", "Nelson", "Russell", "Gordon", "Clarence", "Wellington",
                "Garden", "Common", "Moor", "Heath", "Forge", "Tannery", "Malthouse", "Granary", "Barn", "Paddock",
                "Coronation", "Jubilee", "Hawthorn", "Laburnum", "Chestnut", "Sycamore", "Poplar", "Larch", "Alder"]
STREET_TYPES = ["Road", "Street", "Lane", "Avenue", "Close", "Drive", "Way", "Crescent", "Terrace", "Grove", "Place",
                "Gardens", "Walk", "Rise", "View", "Court"]
NEW_STEMS = ["Kingfisher", "Heron", "Skylark", "Wren", "Swift", "Linnet", "Plover", "Curlew", "Bluebell", "Foxglove",
             "Primrose", "Cowslip", "Teasel", "Campion", "Yarrow", "Sorrel", "Thistle", "Clover", "Harebell", "Bramble",
             "Sedge", "Reed", "Osprey", "Kestrel", "Merlin", "Lapwing", "Marigold", "Saffron", "Juniper", "Damson",
             "Quince", "Medlar", "Greengage", "Russet", "Pippin", "Bramley", "Cobnut", "Sloe", "Elder", "Tansy",
             "Chicory", "Burdock", "Mallow", "Vetch", "Fescue", "Timothy", "Sainfoin", "Lucerne", "Barley", "Spelt"]
NEW_TYPES = ["Way", "Close", "Drive", "Road", "Avenue", "Gardens", "Walk", "Lane", "Rise", "Mews", "Place", "Crescent"]
BLOCK_NAMES = ["House", "Court", "Lodge", "Point", "Heights", "Mansions", "Place"]

# parishes are the rural polling districts (each parish its own polling district); the two towns are unparished
TOWN_WARDS = {"LAB", "LCA", "LNO", "LWE", "CCE", "CPK"}
PD_NAMES = {
    "LAB": ["Abbey North", "Abbey South", "Station"], "LCA": ["Castle", "Castle Hill"],
    "LNO": ["North Park", "Northgate", "Hollins"], "LWE": ["West End", "Mill Lane", "Wharf"],
    "CCE": ["Caldenstow Market", "Caldenstow Bridge"], "CPK": ["Park Farm", "Park Grange", "Parkside"],
    "QUE": ["Quenbrook", "Quenbrook Moor"], "TIB": ["Tibberfield", "Tibber Green"], "EBB": ["Ebborby", "Ebbor Heath"],
    "KET": ["Kettermere", "Kettermere Grange", "Upper Ketter", "Ketter Wold"], "SEL": ["Selwarstow", "Selwar Common"],
    "VEL": ["Vellanridge", "Vellan End", "Low Vellan"], "OST": ["Ostenworth", "Osten Fold"],
    "HAR": ["Harnwick", "Harn Moss"], "BRE": ["Brenningholme", "Brenning Carr", "Holme Ings"],
    "FAU": ["Faulcott", "Faul Ridge"], "GRI": ["Griselbrook", "Grisel Lea", "Brookend"],
    "DOR": ["Dorranford", "Dorran Hill", "Fordside"], "PEL": ["Pellanham", "Pellan Wick"],
    "ROT": ["Rothenridge", "Rothen Dale", "Ridgeway"], "STE": ["Stellfield", "Stell Moor", "Fieldhead"],
    "VAR": ["Vardonham", "Vardon End"], "YAR": ["Yarnmere", "Yarn Bank"]}
# the 2024 review: each district's code renamed; in three wards streets moved between districts (old index -> new)
MOVED = {"LWE": {(2, 1): 2}, "KET": {(1, 0): 2, (3, 2): 2}, "CPK": {(0, 1): 1}}


def build(w, seed=W.SEED + 1):
    rng = np.random.default_rng(seed)
    dw = w["dwellings"]
    wards = {c: (n, cl, r, p) for c, n, cl, r, p in W.WARDS}
    codes = list(wards)
    used_streets = set()

    def street_name(stems, types):
        for _ in range(1000):
            s = "%s %s" % (stems[int(rng.integers(0, len(stems)))], types[int(rng.integers(0, len(types)))])
            if s not in used_streets:
                used_streets.add(s)
                return s
        raise RuntimeError("streets")
    # old (2014 scheme) district codes: two letters by ward order; new (2024 scheme): ward code and a number
    old_code, new_code = {}, {}
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    for i, c in enumerate(codes):
        n, cl, r, p = wards[c]
        for j in range(p):
            old_code[(c, j)] = letters[i] + "ABCD"[j]
            new_code[(c, j)] = "%s%d" % (c, j + 1)
    # settled stock: streets of 20 to 90 dwellings per polling district, flats in blocks of 6 to 30
    by_pd = {}
    for k, d in enumerate(dw):
        by_pd.setdefault((d["ward"], d["pd"], d["site"]), []).append(k)
    uprn_settled = rng.choice(np.arange(100061000000, 100061999999), size=len(dw), replace=False)
    nu = 0
    blocks = []
    street_of = {}
    nmajor = len(W.SITES)
    street_len = {}
    for (c, j, site), ks in sorted(by_pd.items(), key=lambda kv: (kv[0][0], kv[0][1], -1 if kv[0][2] is None else kv[0][2])):
        houses = [k for k in ks if dw[k]["type"] == "house"]
        flats = [k for k in ks if dw[k]["type"] == "flat"]
        if site is not None and site >= nmajor:
            # a small site: infill along, or a conversion on, one of the district's existing streets
            hosts = street_of.get((c, j, None)) or [st for (cc, jj, ss), sts in street_of.items() if cc == c for st in sts]
            st = hosts[int(rng.integers(0, len(hosts)))]
            houses.sort(key=lambda k: dw[k]["done"])
            for k in houses:
                street_len[st] = street_len.get(st, 0) + 1
                dw[k]["street"], dw[k]["number"], dw[k]["block"] = st, street_len[st], None
            if flats:
                street_len[st] = street_len.get(st, 0) + 1
                bname = "%s %s" % (st.split()[0], BLOCK_NAMES[int(rng.integers(0, len(BLOCK_NAMES)))])
                blocks.append(dict(name=bname, street=st, ward=c, pd=j, site=site, number=street_len[st]))
                for fl, k in enumerate(sorted(flats, key=lambda k: dw[k]["done"]), start=1):
                    dw[k]["street"], dw[k]["number"], dw[k]["block"], dw[k]["flat"] = st, street_len[st], len(blocks) - 1, fl
            continue
        stems, types = (STREET_STEMS, STREET_TYPES) if site is None else (NEW_STEMS, NEW_TYPES)
        if site is not None:
            # a site's dwellings in completion order along its new streets
            houses.sort(key=lambda k: dw[k]["done"])
            flats.sort(key=lambda k: dw[k]["done"])
        i = 0
        while i < len(houses):
            size = int(rng.integers(20, 91)) if site is None else int(rng.integers(25, 70))
            st = street_name(stems, types)
            for num, k in enumerate(houses[i:i + size], start=1):
                dw[k]["street"], dw[k]["number"], dw[k]["block"] = st, num, None
            street_len[st] = len(houses[i:i + size])
            street_of.setdefault((c, j, site), []).append(st)
            i += size
        i = 0
        while i < len(flats):
            size = int(rng.integers(6, 31))
            hosts = street_of.get((c, j, site)) or [street_name(stems, types)]
            st = hosts[int(rng.integers(0, len(hosts)))]
            bname = "%s %s" % (st.split()[0], BLOCK_NAMES[int(rng.integers(0, len(BLOCK_NAMES)))])
            street_len[st] = street_len.get(st, 0) + 1
            bnum = street_len[st]
            blocks.append(dict(name=bname, street=st, ward=c, pd=j, site=site, number=bnum))
            for fl, k in enumerate(flats[i:i + size], start=1):
                dw[k]["street"], dw[k]["number"], dw[k]["block"], dw[k]["flat"] = st, bnum, len(blocks) - 1, fl
            i += size
    # UPRNs: settled stock from the address register's original load; new dwellings numbered when addressed
    new_seq = 10093000000 + int(rng.integers(1000, 9000)) * 100
    order_new = sorted([k for k, d in enumerate(dw) if d["site"] is not None], key=lambda k: (dw[k]["done"], k))
    for k, d in enumerate(dw):
        if d["site"] is None:
            d["uprn"] = int(uprn_settled[nu]); nu += 1
    for k in order_new:
        new_seq += int(rng.integers(1, 4))
        dw[k]["uprn"] = new_seq
    for b in blocks:
        new_seq += 1
        b["uprn"] = int(uprn_settled[nu]) if b["site"] is None else new_seq
        nu += 1
    # polling districts: the 2024 code, and the 2014 code before the review (moved streets carry another index)
    for d in dw:
        c, j = d["ward"], d["pd"]
        d["pd_new"] = new_code[(c, j)]
        d["pd_old_idx"] = j
    moved_streets = {}
    for c, mv in MOVED.items():
        for (old_j, new_j), nstreets in mv.items():
            cands = sorted(set(d["street"] for d in dw if d["ward"] == c and d["pd"] == new_j and d["site"] is None))
            pick = [cands[int(x)] for x in rng.choice(len(cands), size=min(nstreets, len(cands)), replace=False)]
            for s in pick:
                moved_streets[(c, s)] = (old_j, new_j)
    for d in dw:
        key = (d["ward"], d["street"])
        if key in moved_streets:
            d["pd_old_idx"] = moved_streets[key][0]
        d["pd_old"] = old_code[(d["ward"], d["pd_old_idx"])]
    return dict(blocks=blocks, old_code=old_code, new_code=new_code, moved_streets=moved_streets)
