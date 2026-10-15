"""Business names, worksite addresses and protected keys in the idiom of a state UI employer register."""
import hashlib

import world as W

SURNAMES = [
    "Ashby", "Bardwell", "Beckett", "Birchall", "Blakely", "Bramwell", "Brocklin", "Calloway", "Carden", "Chadwick",
    "Colvin", "Corrigan", "Crandall", "Dalby", "Darrow", "Delacroix", "Draper", "Dunleavy", "Eastman", "Ellery",
    "Farrow", "Felton", "Fenwick", "Garland", "Gilchrist", "Goodwin", "Gorman", "Hadley", "Halstead", "Harlan",
    "Hartwell", "Haskins", "Holloway", "Hoyt", "Ingram", "Jessup", "Kendrick", "Kettering", "Kimball", "Lachance",
    "Langford", "Larkin", "Lockhart", "Lowell", "Maddox", "Marlowe", "Merritt", "Molloy", "Northcott", "Oakes",
    "Ogden", "Osgood", "Pacheco", "Pemberton", "Pickett", "Prescott", "Quimby", "Radcliffe", "Ramsdell", "Redfield",
    "Rowan", "Sadler", "Sandoval", "Sayer", "Selby", "Shipley", "Sorensen", "Stroud", "Talbot", "Thorne", "Tilden",
    "Toller", "Underhill", "Vance", "Varga", "Wadsworth", "Waldron", "Whitcomb", "Whitlock", "Winslow", "Yardley",
    "Zeller", "Abernathy", "Bolling", "Castell", "Dorsey", "Eckert", "Fairbanks", "Grady", "Hollis", "Ivers",
    "Jarrell", "Keane", "Lindgren", "Mercer", "Nyberg", "Okafor", "Petrov", "Quinlan", "Rourke", "Stanek", "Trujillo",
    "Ulrich", "Voss", "Weller", "Yates", "Zamora", "Aldana", "Brannigan", "Cuthbert", "Dennehy", "Esquivel",
    "Albright", "Barrow", "Bertrand", "Bickford", "Caine", "Carrow", "Danforth", "Dempsey", "Driscoll", "Emmons",
    "Faraday", "Fitzroy", "Galloway", "Gatlin", "Hackett", "Hendry", "Hubbell", "Iverson", "Jansky", "Kestner",
    "Kowalski", "Lambert", "Lindqvist", "Lunde", "Macklin", "Mattingly", "Nakamura", "Nolan", "Orcutt", "Pell",
    "Pruett", "Quarles", "Raines", "Rasmussen", "Rutledge", "Sakai", "Schafer", "Spalding", "Strand", "Tanaka",
    "Thibault", "Tollefson", "Urbina", "Vickery", "Wendell", "Wexford", "Whitaker", "Wilder", "Yoder", "Zielinski",
]
NOUN = {
    "Remodeling": ["Remodeling", "Home Improvement", "Renovation", "Builders"],
    "Plumbing & Heating": ["Plumbing & Heating", "Mechanical", "Plumbing", "Heating & Cooling"],
    "Electric": ["Electric", "Electrical Services", "Electrical Contracting"],
    "Contracting": ["Contracting", "Concrete", "Masonry", "Drywall", "Roofing"],
    "Machine": ["Machine Works", "Precision Machining", "Machine & Tool", "Manufacturing"],
    "Sheet Metal": ["Sheet Metal", "Metal Fabrication", "Fabrication"], "Cabinetry": ["Cabinetry", "Woodworks", "Millwork"],
    "Bakery": ["Bakery", "Bake Shop", "Bread Co"], "Foods": ["Foods", "Food Distributors", "Provisions"],
    "Equipment": ["Equipment", "Industrial Supply", "Machinery"], "Grocery": ["Market", "Grocery", "Foods"],
    "Corner Store": ["Corner Store", "Quick Mart", "Pantry"], "Fuel": ["Fuel Stop", "Gas & Go", "Fuel & Food"],
    "Hardware": ["Hardware", "Hardware & Supply", "Farm & Home"], "Auto Parts": ["Auto Parts", "Parts Supply"],
    "Outfitters": ["Outfitters", "Sporting Goods", "Bait & Tackle"], "Variety": ["Variety", "Dollar & More", "Mercantile"],
    "Pharmacy": ["Pharmacy", "Drug", "Apothecary"], "Goods": ["Goods", "Trading Post", "Supply"],
    "Gifts": ["Gifts", "Gift Shop", "Mercantile"], "Resale": ["Resale", "Thrift", "Consignment"],
    "Clothing": ["Clothing", "Apparel", "Boutique"], "Books": ["Books", "Bookshop", "Book Exchange"],
    "Auto Repair": ["Auto Repair", "Automotive", "Garage"], "Machinery Repair": ["Equipment Repair", "Hydraulics", "Repair"],
    "Salon": ["Salon", "Hair Studio", "Beauty"], "Barbers": ["Barber Shop", "Barbers"],
    "Grill": ["Grill", "Tavern", "Diner", "Supper Club"], "Kitchen": ["Kitchen", "Pizza", "Burger Barn", "Taqueria"],
    "Coffee": ["Coffee", "Coffee House", "Espresso"], "Fitness": ["Fitness", "Athletic Club", "Gym"],
    "Family Medicine": ["Family Medicine", "Medical Clinic", "Family Practice"], "Dental": ["Dental", "Dentistry", "Family Dental"],
    "Home Care": ["Home Care", "Senior Services", "Home Health"], "Law": ["Law Office", "Law"],
    "Accounting": ["Accounting", "Tax & Accounting", "CPAs"], "Realty": ["Realty", "Real Estate", "Properties"],
    "Freight": ["Trucking", "Freight", "Transport"], "Landscaping": ["Landscaping", "Lawn Care", "Grounds"],
    "Recreation": ["Adventures", "Fun Park", "Mini Golf"], "Campground": ["Campground", "RV Park", "Camp"],
    "Ice Cream": ["Ice Cream", "Creamery", "Frozen Custard"], "Marina": ["Marina", "Boat Rental", "Landing"],
    "Lawn & Garden": ["Lawn & Garden", "Mowing", "Turf"],
}
SUFFIX_PRO = {"Family Medicine": ["PC", "PLLC"], "Dental": ["PC", "PLLC"], "Law": ["PLLC", "LLP"],
              "Accounting": ["PLLC", "LLP", "PC"]}


def fmt_legacy(num, dirn, street, stype, suite):
    """Legacy-system worksite address: words spelt out, mixed case."""
    s = "%d %s%s %s" % (num, (dirn[0] + " ") if dirn else "", street, stype[0])
    return s + (", Suite %s" % suite if suite else "")


def fmt_usps(num, dirn, street, stype, suite):
    """Address as the replacement system standardises it (USPS abbreviations, capitals)."""
    s = "%d %s%s %s" % (num, (dirn[1] + " ") if dirn else "", street.upper(), stype[1])
    return s + (" STE %s" % suite if suite else "")


def worker_key(i):
    h = hashlib.sha256(("lornock-pik-%d-%d" % (W.SEED, i)).encode()).hexdigest().upper()
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    n = int(h[:20], 16)
    out = []
    for _ in range(11):
        n, r = divmod(n, len(alphabet))
        out.append(alphabet[r])
    return "".join(out)


class Namer:
    def __init__(self, rng):
        self.rng = rng
        self.legal = set()
        self.trade = set()

    def pick(self, seq):
        return seq[int(self.rng.integers(len(seq)))]

    def business(self, noun_key, county, town, style=None):
        """A legal name and a trade name for a business in the industry `noun_key`."""
        rng = self.rng
        for _ in range(2000):
            noun = self.pick(NOUN[noun_key])
            kind = style or ("surname" if rng.random() < 0.5 else "place")
            if kind == "surname":
                sur = self.pick(SURNAMES)
                if rng.random() < 0.12:
                    sur = "%s & %s" % (sur, self.pick(SURNAMES))
                trade = "%s %s" % (sur, noun) if rng.random() < 0.6 else "%s's %s" % (sur.split(" & ")[0], noun)
            else:
                pw = self.pick(W.PLACE_WORDS + [town] * 3 + [county] * 2)
                trade = "%s %s" % (pw, noun)
            if noun_key in SUFFIX_PRO:
                suffix = self.pick(SUFFIX_PRO[noun_key])
            else:
                suffix = self.pick(["LLC"] * 6 + ["Inc"] * 3 + ["Co", "Corp"])
            base = trade.replace("'s ", " ")
            if rng.random() < 0.25:
                legal = "%s %s %s" % (base.split(" ")[0], self.pick(["Holdings", "Enterprises", "Group", "Partners"]),
                                      suffix)
            else:
                legal = "%s %s" % (base, suffix)
            if legal not in self.legal and trade not in self.trade:
                self.legal.add(legal)
                self.trade.add(trade)
                return legal, trade
        raise RuntimeError("name space exhausted")

    def legal_for(self, trade, suffixes=("LLC", "Inc")):
        """A new legal entity's name keeping a trade name (a take-over that kept the shop's name): the new owner's own
        entity, whatever its owner called it."""
        rng = self.rng
        for _ in range(200):
            stem = trade.replace("'s ", " ").split(" ")
            r = rng.random()
            if r < 0.22:
                legal = "%s %s" % (self.pick(SURNAMES), self.pick(["Enterprises LLC", "Holdings LLC", "Group Inc",
                                                                   "Ventures LLC", "Management LLC", "& Sons Inc",
                                                                   "Family LLC", "Investments LLC"]))
            elif r < 0.38:
                legal = "%s & %s %s" % (self.pick(SURNAMES), self.pick(SURNAMES), self.pick(["LLC", "Inc", "LLP"]))
            elif r < 0.52:
                letters = "ABCDEFGHJKLMNPRSTW"
                initials = "".join(letters[int(rng.integers(len(letters)))] for _ in range(int(rng.integers(2, 4))))
                legal = "%s %s" % (initials, self.pick(["LLC", "Inc", "Ventures LLC", "Partners LLC", "Group LLC"]))
            elif r < 0.66:
                legal = "%s %s %s" % (self.pick(W.PLACE_WORDS), self.pick(["Ventures", "Partners", "Hospitality",
                                                                           "Retail", "Services", "Brands"]),
                                      self.pick(["LLC", "Inc"]))
            elif r < 0.80:
                legal = "%s %s" % (" ".join(stem), self.pick(["LLC", "Inc", "Co", "Ltd"]))
                if legal in self.legal:
                    legal = "%s %d LLC" % (" ".join(stem[:2]), int(rng.integers(2, 9)))
            elif r < 0.90:
                legal = "%s %s %s" % (self.pick(SURNAMES), " ".join(stem[1:3]) or stem[0], self.pick(suffixes))
            else:
                legal = "%s %s LLC" % (" ".join(stem[:2]), self.pick(["Operating", "Acquisition", "Holdings",
                                                                     "of the Valley", "Company"]))
            if legal not in self.legal:
                self.legal.add(legal)
                return legal
        raise RuntimeError("legal name space exhausted")
