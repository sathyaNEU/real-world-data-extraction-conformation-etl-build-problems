"""The compact's member hospitals with adult intensive care beds (licence number, the board's facility code before
and after the vendor's 8 December migration, the transfer center's directory code, county, time zone, staffed
adult ICU beds), and the other facilities that ask the transfer center for placements. Hospital order and region
membership are fixed: the true states are drawn hospital by hospital in this order."""
import numpy as np

import world as W

# invented hospital names (no real Tennessee hospital)
STEMS = ["Hemlock Valley", "Larkspur", "Sycamore Bend", "Bluestem", "Ironweed", "Copper Hollow", "Fallowfield",
         "Kestrel Point", "Wren Creek", "Thistledown", "Quarry Hill", "Millrace", "Juniper Flats", "Owlhead",
         "Cobbler Gap", "Redbud Hollow", "Silverleaf", "Tanager", "Ashgrove", "Foxfire Ridge", "Highcrest",
         "Bramble Fork", "Coldwater Bend", "Shale Point", "Twin Cedar", "Pinecastle", "Lantern Hill", "Stonewick",
         "Briarwood Gap", "Goldenrod", "Hawthorne Bluff", "Marrowfield", "Elderbank", "Trillium", "Sumac Hollow",
         "Chestnut Run", "Bellwether", "Cardinal Ridge", "Fernbrook", "Gristmill", "Harrowgate", "Kingfisher",
         "Lockwood Bend", "Mossy Ford", "Nettlefield", "Orchard Knob", "Pawpaw Creek", "Quillback", "Rookwood",
         "Saltlick", "Tamarack", "Upland Springs", "Vervain", "Willowmere", "Yellowwood", "Alderbrook",
         "Bittersweet", "Canebrake", "Dogwood Flats", "Eastwind", "Featherbed", "Glenmorrow", "Heronsgate",
         "Indigo Bluff", "Jessamine", "Knotweed", "Lindenhall", "Meadowlark", "Northfork", "Oakhurst Bend",
         "Partridge Hill", "Quietwater", "Riverbirch", "Sassafras", "Thornapple", "Underwood Gap", "Vinewood"]
SUFFIXES = ["Medical Center", "Regional Medical Center", "Community Hospital", "Hospital", "Regional Hospital",
            "Memorial Hospital"]
SHORT = {"Medical Center": ["Med Ctr", "MC", "Medical Ctr"], "Regional Medical Center": ["Reg Med Ctr", "RMC",
         "Regional"], "Community Hospital": ["Comm Hosp", "Community", "CH"], "Hospital": ["Hosp", "Hospital"],
         "Regional Hospital": ["Reg Hosp", "Regional", "RH"], "Memorial Hospital": ["Memorial", "Mem Hosp", "MH"]}
METRO = {"NE": ["Sullivan", "Washington"], "ET": ["Knox", "Blount"], "SE": ["Hamilton", "Bradley"],
         "UC": ["Putnam", "Cumberland"], "MS": ["Davidson", "Williamson", "Rutherford"], "SC": ["Maury", "Coffee"],
         "WT": ["Madison", "Dyer"], "MD": ["Shelby"]}
RURAL = {"NE", "UC", "SC", "WT"}

# facilities outside the compact that ask the transfer center for placements: small Tennessee hospitals with no
# adult ICU (by county) and hospitals across the state line
NONMEMBER_STEMS = ["Hollis Creek", "Pine Barren", "Redwing", "Cumberland Gap Valley", "Ozment", "Long Hollow",
                   "Big Sandy", "Clear Fork", "Dutch Valley", "Elk River", "Falling Water", "Gainesboro Road",
                   "Hatchie Bottom", "Indian Mound", "Jellico Ridge", "Kettle Springs", "Little Pigeon", "Mill Spring",
                   "Nolichucky Bend", "Obed River", "Piney Flats", "Rockcastle"]
OUT_OF_STATE = [("Bluegrass Border Medical Center", "KY"), ("Tri-State Southern Hospital", "GA"),
                ("Delta Crossing Regional", "MS"), ("Shoals Valley Hospital", "AL"), ("Ozark Gateway Medical Center",
                "AR"), ("Mountain Empire Hospital", "VA")]


def hospitals():
    rng = np.random.default_rng(W.SEED + 1)
    stems = list(STEMS)
    rng.shuffle(stems)
    n_all = sum(r[3] for r in W.REGIONS)
    lic = rng.choice(np.arange(10100, 99900, 7), size=n_all, replace=False)
    out, k = [], 0
    for code, name, _, n, _ in W.REGIONS:
        counties = W.COUNTIES[code]
        metro = METRO[code]
        for i in range(n):
            if i < len(metro) * 2 and rng.random() < 0.7:
                county = metro[i % len(metro)]
            else:
                county = counties[int(rng.integers(0, len(counties)))]
            big = county in metro and code not in RURAL
            beds = int(rng.integers(16, 49)) if big else int(rng.integers(5, 17))
            stem = stems[k]
            suffix = SUFFIXES[int(rng.integers(0, len(SUFFIXES)))]
            out.append(dict(licence="%05d" % int(lic[k]), name="%s %s" % (stem, suffix), stem=stem, suffix=suffix,
                            region=code, county=county, fips="47" + W.FIPS[county],
                            tz="Eastern" if county in W.EASTERN_COUNTIES else "Central", beds=beds))
            k += 1
    # the board's facility codes: since the 8 December migration in alphabetical order of name; before it, in the
    # order hospitals joined the board, from the same code space (so every old code is another hospital's new one)
    order_new = sorted(range(len(out)), key=lambda j: out[j]["name"])
    for rank, j in enumerate(order_new):
        out[j]["board_code"] = "F%04d" % (1001 + rank)
    joined = list(range(len(out)))
    rng2 = np.random.default_rng(W.SEED + 2)
    rng2.shuffle(joined)
    for rank, j in enumerate(joined):
        out[j]["board_code_old"] = "F%04d" % (1001 + rank)
    for j, h in enumerate(out):
        h["center_code"] = "TC%03d" % (101 + order_new.index(j) * 3 % 301)
    return out


def aliases(hosp):
    """the names the transfer center's staff type for a facility that asks for a placement, each mapped to the
    facility: [(typed name, facility id, county or state)]"""
    rng = np.random.default_rng(W.SEED + 3)
    out = []
    for h in hosp:
        sh = SHORT[h["suffix"]]
        names = {h["name"], "%s %s" % (h["stem"], sh[int(rng.integers(0, len(sh)))]), h["name"].upper()}
        if rng.random() < 0.5:
            names.add("%s %s" % (h["stem"], sh[int(rng.integers(0, len(sh)))]))
        for nm in sorted(names):
            out.append((nm, h["licence"], h["county"]))
    return out


def nonmembers():
    """facilities outside the compact that ask the transfer center for placements"""
    rng = np.random.default_rng(W.SEED + 4)
    out = []
    regions = [r[0] for r in W.REGIONS]
    for i, stem in enumerate(NONMEMBER_STEMS):
        code = regions[i % len(regions)]
        cty = W.COUNTIES[code][int(rng.integers(0, len(W.COUNTIES[code])))]
        out.append(dict(fid="NM%03d" % (i + 1), name="%s %s" % (stem, ["Hospital", "Community Hospital",
                        "Medical Center"][int(rng.integers(0, 3))]), county=cty, state="TN", region=code,
                        tz="Eastern" if cty in W.EASTERN_COUNTIES else "Central"))
    for i, (nm, st) in enumerate(OUT_OF_STATE):
        out.append(dict(fid="OS%03d" % (i + 1), name=nm, county="", state=st, region="",
                        tz="Eastern" if st in ("GA", "VA") else "Central"))
    return out
