"""Tullan's member stores: the roster, price files, formats, sizes, regions and their changes."""
import datetime as dt

import numpy as np

from world import D, PLACES, REG_SHORT

LONG = {v: k for k, v in REG_SHORT.items()}

# second stores in the bigger towns (routing key, area, county, Jan 2026 region, anchor town)
SECONDS = [
    ("D24", "Tallaght Cookstown", "Dublin", "DNE"), ("D15", "Coolmine", "Dublin", "DNE"),
    ("A92", "Drogheda West Street", "Louth", "DNE"), ("A91", "Dundalk Bridge Street", "Louth", "DNE"),
    ("C15", "Navan Johnstown", "Meath", "DNE"), ("A98", "Bray Vevay", "Wicklow", "DNE"),
    ("K78", "Adamstown", "Dublin", "DNE"),
    ("T12", "Bishopstown", "Cork", "S"), ("T12", "Wilton", "Cork", "S"), ("T23", "Mayfield", "Cork", "S"),
    ("T12", "Togher", "Cork", "S"), ("P31", "Ballincollig Main Street", "Cork", "S"),
    ("P43", "Carrigaline Kilmoney", "Cork", "S"), ("P51", "Mallow Spa Square", "Cork", "S"),
    ("V92", "Tralee Oakpark", "Kerry", "S"), ("V93", "Killarney New Street", "Kerry", "S"),
    ("P25", "Midleton Main Street", "Cork", "S"), ("P85", "Clonakilty Pearse Street", "Cork", "S"),
    ("P24", "Cobh Harbour Row", "Cork", "S"),
    ("H91", "Doughiska", "Galway", "WNW"), ("H91", "Oranmore", "Galway", "WNW"),
    ("H91", "Moycullen", "Galway", "WNW"), ("F23", "Castlebar Hawthorn Avenue", "Mayo", "WNW"),
    ("F91", "Sligo Cartron", "Sligo", "WNW"), ("F92", "Letterkenny Port Road", "Donegal", "WNW"),
    ("V95", "Ennis Gort Road", "Clare", "WNW"), ("F26", "Ballina Ardnaree", "Mayo", "WNW"),
    ("V94", "Raheen", "Limerick", "MSE"), ("X91", "Waterford Ardkeen", "Waterford", "MSE"),
    ("R95", "Kilkenny Loughboy", "Kilkenny", "MSE"), ("N37", "Athlone Monksland", "Westmeath", "MSE"),
    ("W91", "Naas Sallins Road", "Kildare", "MSE"), ("N91", "Mullingar Ashe Road", "Westmeath", "MSE"),
]
JULY_MOVES = {"Kildare": "DNE", "Limerick": "S", "Clare": "S"}           # effective 6 Jul 2026
MAY27_MOVES = {"Waterford": "S", "Wexford": "S"}                          # effective 3 May 2027
FORMAT_MULT = {"Supermarket": 1.55, "Local": 1.0, "Express": 0.6}
QUOTA = {"DNE": {"P": 38, "C": 16, "V": 4}, "S": {"P": 12, "C": 16, "V": 10},
         "WNW": {"P": 6, "C": 12, "V": 18}, "MSE": {"P": 14, "C": 16, "V": 18}}


def build(seed):
    """Return the store list. Each store is a dict; history stores carry open/close weeks."""
    rng = np.random.default_rng(seed * 7 + 1)
    slots = [p for p in PLACES if p[1] != "Ballinrobe"] + SECONDS
    assert len(slots) == 179, len(slots)          # 180 with the new Swords store below
    # store numbers: a sparse block, old stores low, newer high
    pool = list(range(101, 380))
    rng.shuffle(pool)
    taken = {119, 147, 231, 256, 203, 377, 388, 412, 415}
    nums = [n for n in pool if n not in taken]
    stores = []
    special = {("D07", "Phibsborough"): 147, ("D11", "Finglas"): 256, ("R35", "Tullamore"): 203}
    for (rk, town, county, reg) in slots:
        no = special.get((rk, town))
        if no is None:
            no = nums.pop()
        stores.append({"no": "%04d" % no, "routing": rk, "town": town, "county": county, "reg_jan": reg})
    # the store that joined in June 2025 takes 0377
    j = next(s for s in stores if s["town"] == "Adamstown")
    j["no"] = "0377"
    # the new member at Swords takes the reissued 0119 from 3 Aug 2026
    stores.append({"no": "0119", "routing": "K67", "town": "Swords Rivervalley", "county": "Dublin",
                   "reg_jan": "DNE", "opened": D(2026, 8, 3), "reissued": True})
    # formats
    for s in stores:
        u = rng.random()
        s["format"] = "Supermarket" if u < 0.34 else ("Local" if u < 0.78 else "Express")
    # price files: quota by Jan 2026 region, Kildare and the Dublin commuter belt lean Premium
    for reg, q in QUOTA.items():
        members = [s for s in stores if s["reg_jan"] == reg]
        if reg == "DNE":
            q = dict(q)
        order = sorted(members, key=lambda s: (0 if s["county"] in ("Kildare", "Wicklow", "Meath") else 1,
                                               rng.random()))
        files = ["P"] * q["P"] + ["C"] * q["C"] + ["V"] * q["V"]
        # the commuter-belt stores take the first Premium places, the rest are shuffled
        head = [s for s in order if s["county"] in ("Kildare", "Wicklow", "Meath")]
        tail = [s for s in order if s not in head]
        rng.shuffle(tail)
        seq = head + tail
        assert len(seq) == len(files), (reg, len(seq), len(files))
        for s, f in zip(seq, files):
            s["pfile"] = f
    # Swords Rivervalley is a Premium store; make the quota hold by swapping one DNE Premium to Core
    sw = next(s for s in stores if s["no"] == "0119")
    if sw["pfile"] != "P":
        other = next(s for s in stores if s["reg_jan"] == "DNE" and s["pfile"] == "P" and s is not sw)
        other["pfile"], sw["pfile"] = sw["pfile"], "P"
    for s in stores:
        s["size"] = FORMAT_MULT[s["format"]] * float(rng.lognormal(0, 0.22))
        s["opened"] = s.get("opened", D(2008, 1, 1))
        s["closed"] = None
        s["scanning"] = True
        s["reg_event"] = JULY_MOVES.get(s["county"], s["reg_jan"]) if s["reg_jan"] in ("MSE", "WNW") else s["reg_jan"]
        s["reg_may27"] = MAY27_MOVES.get(s["county"], s["reg_event"])
    j["opened"] = D(2025, 6, 2)
    # history stores
    phib = next(s for s in stores if s["no"] == "0147")
    phib["renumbered_to"] = "0388"
    phib["renumber_week"] = D(2026, 4, 6)
    ballinrobe = {"no": "0119", "routing": "F31", "town": "Ballinrobe", "county": "Mayo", "reg_jan": "WNW",
                  "format": "Local", "pfile": "V", "size": 0.95, "opened": D(2008, 1, 1), "closed": D(2026, 5, 31),
                  "scanning": True, "reg_event": "WNW", "reg_may27": "WNW", "history_only": True}
    ballyfermot = {"no": "0231", "routing": "D10", "town": "Ballyfermot", "county": "Dublin", "reg_jan": "DNE",
                   "format": "Local", "pfile": "C", "size": 0.9, "opened": D(2008, 1, 1), "closed": D(2025, 12, 31),
                   "scanning": True, "reg_event": "DNE", "reg_may27": "DNE", "history_only": True}
    islands = [
        {"no": "0412", "routing": "F94", "town": "Arranmore Island", "county": "Donegal", "reg_jan": "WNW",
         "format": "Express", "pfile": "P", "size": 0.35, "opened": D(2008, 1, 1), "closed": None, "scanning": False,
         "reg_event": "WNW", "reg_may27": "WNW"},
        {"no": "0415", "routing": "H91", "town": "Inis Mor", "county": "Galway", "reg_jan": "WNW",
         "format": "Express", "pfile": "P", "size": 0.4, "opened": D(2008, 1, 1), "closed": None, "scanning": False,
         "reg_event": "WNW", "reg_may27": "WNW"},
    ]
    stores += [ballinrobe, ballyfermot] + islands
    for s in stores:
        s["name"] = "Tullan " + s["town"]
    return stores


def scan_ids(store, w):
    """The store number the feed carries for week w, or None if the store sent no file that week."""
    if not store["scanning"]:
        return None
    if w < store["opened"] or (store["closed"] and w > store["closed"]):
        return None
    if store.get("renumbered_to") and w >= store["renumber_week"]:
        return store["renumbered_to"]
    return store["no"]
