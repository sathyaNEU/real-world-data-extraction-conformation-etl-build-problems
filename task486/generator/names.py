"""Names in the fiction: Torvasay's districts, centres and streets, and the pools the employers, traders and owners
draw their names from. The place names come from the slot's screened list (no reference place within reach); the
people in the documents are the card's personas."""

DISTRICTS = [  # code, name, postcode districts (LW numbers), billing system layout
    ("RKG", "Rookgate", range(1, 9), "status"),
    ("DOR", "Dorrstead", range(9, 13), "relief"),
    ("GLN", "Glenskarn", range(13, 16), "status"),
    ("ING", "Ingmouth", range(16, 19), "relief"),
    ("NSH", "Neshdale", range(19, 21), "relief"),
    ("SKL", "Skelrigg", range(21, 23), "relief"),
]

DISTRICTS_NAMES = [(d[0], d[1]) for d in DISTRICTS]

# code, name, district, tier; the order is the prototype's (city, the five district towns, Rookgate's six district
# centres, nine towns, ten small towns)
CENTRES = [
    ("TC01", "Rookgate City Centre", "RKG", "city"),
    ("TC02", "Dorrstead", "DOR", "large"),
    ("TC03", "Glenskarn", "GLN", "large"),
    ("TC04", "Ingmouth", "ING", "large"),
    ("TC05", "Neshdale", "NSH", "large"),
    ("TC06", "Skelrigg", "SKL", "large"),
    ("TC07", "Bromgate", "RKG", "district"),
    ("TC08", "Fenmoss", "RKG", "district"),
    ("TC09", "Halmoss", "RKG", "district"),
    ("TC10", "Kellgarth", "RKG", "district"),
    ("TC11", "Quengate", "RKG", "district"),
    ("TC12", "Ravthwaite", "RKG", "district"),
    ("TC13", "Lundgate", "DOR", "town"),
    ("TC14", "Molwold", "DOR", "town"),
    ("TC15", "Quenmouth", "GLN", "town"),
    ("TC16", "Ravbeck", "GLN", "town"),
    ("TC17", "Kellholm", "ING", "town"),
    ("TC18", "Tavmoss", "ING", "town"),
    ("TC19", "Bromwold", "NSH", "town"),
    ("TC20", "Molscar", "NSH", "town"),
    ("TC21", "Lundstead", "SKL", "town"),
    ("TC22", "Orrstead", "DOR", "small"),
    ("TC23", "Vaskhope", "DOR", "small"),
    ("TC24", "Skelgate", "GLN", "small"),
    ("TC25", "Tormoss", "GLN", "small"),
    ("TC26", "Orrwold", "ING", "small"),
    ("TC27", "Vaskrigg", "ING", "small"),
    ("TC28", "Quenstead", "NSH", "small"),
    ("TC29", "Vaskstow", "NSH", "small"),
    ("TC30", "Ravwold", "SKL", "small"),
    ("TC31", "Tavscar", "SKL", "small"),
]

# villages and estates outside the designated centres, by district
LOCALITIES = {
    "RKG": ["Rookgate", "Inglowe", "Halvask", "Brommoss", "Fenrigg", "Kellness", "Rookholt", "Rookmouth"],
    "DOR": ["Dorrstead", "Dorrfold", "Dorrhope", "Lundmoss", "Molrigg"],
    "GLN": ["Glenskarn", "Glenstow", "Glenscar", "Tormere"],
    "ING": ["Ingmouth", "Ingscar", "Ingrigg", "Orrmoss"],
    "NSH": ["Neshdale", "Neshhope", "Neshstow", "Quensett"],
    "SKL": ["Skelrigg", "Skelsett", "Ravmoss", "Tavthwaite"],
}

CENTRE_STREETS = ["High Street", "Market Place", "Market Street", "Church Street", "Bridge Street", "King Street",
                  "Queen Street", "Castle Street", "Fore Street", "Chapel Street", "Mill Street", "Station Road",
                  "The Square", "Victoria Street", "Union Street", "North Street", "South Street", "West Street",
                  "East Street", "Silver Street", "Back Lane", "Water Street", "George Street", "Princes Street",
                  "Harbour Street", "Quay Street", "Cross Street", "New Street", "Hill Street", "Commercial Street",
                  "Arcade Walk", "Exchange Street", "Bank Street", "Tower Street"]
OTHER_STREETS = ["Moor Road", "Green Lane", "Park Road", "Shore Road", "Hall Lane", "Long Lane", "Field Road",
                 "Ash Grove", "Elm Road", "Beech Avenue", "Oak Crescent", "Cedar Way", "Highfield Road",
                 "Brookside", "Westfield Avenue", "Northgate", "Southgate", "Hawthorn Road", "Larch Close",
                 "Rowan Drive", "Heather Road", "Kiln Lane", "Quarry Road", "Dock Road", "Links Road",
                 "Meadow Way", "School Lane", "Manor Road", "Forge Lane", "Cliff Road"]
ESTATES = {"park": ["Retail Park", "Shopping Park", "Trade Park"],
           "ind": ["Industrial Estate", "Business Centre", "Trading Estate", "Enterprise Park"],
           "biz": ["Business Park", "Office Park", "Technology Park"]}

SURNAMES = """Abbott Acton Ainsworth Allen Allsop Ambler Ancell Appleby Archer Ashby Ashworth Atherton Atkin Austin Aylott
Bagley Bainbridge Baird Bakewell Bamford Banner Barlow Barraclough Bartram Bassett Batty Baxter Beardsley Beckett Bell
Bennion Bentley Berridge Bickerton Binns Birch Birkett Blackburn Blake Blenkinsop Bolton Booth Bostock Boswell Bowden
Bowker Bradley Bramley Brass Brennan Brierley Brigg Broadbent Brockley Brough Buckley Bulmer Burgin Burrows Butterworth
Cadman Calvert Capstick Carver Catlow Cawthorne Chadwick Chappell Chorlton Clegg Clough Cockburn Collier Coombes Cottam
Coulson Cowell Crabtree Crawshaw Cropper Crossley Crowther Dale Danson Dawber Dearden Denby Dewhurst Dickinson Dobson
Drury Duckworth Dunford Dyson Eastwood Eccles Edmondson Elland Ellwood Emmott Entwistle Fairbairn Fairclough Farnworth
Fawcett Fearnley Fenton Fielding Firth Fletcher Foulds Garside Gaskell Gledhill Goodall Gornall Greenhalgh Greenwood
Grimshaw Haigh Halstead Hammond Hanson Hardcastle Hargreaves Harker Hartley Haworth Heap Heaton Hebden Helliwell Heseltine
Hibbert Hindle Hirst Holden Holroyd Horrocks Howarth Hoyle Hulme Ibbotson Illingworth Ingham Iveson Jagger Jowett Kay
Kershaw Kenyon Kitchen Knowles Lacey Lambert Lawton Laycock Leadbetter Leatham Lister Littlewood Lockwood Lomax Longbottom
Lumb Marsden Mellor Metcalfe Midgley Milner Moorhouse Mottram Naylor Nuttall Oddie Oldroyd Ormerod Outhwaite Parkin
Pickles Pilling Platt Priestley Pullan Ramsden Rawlinson Redfearn Rhodes Riley Robertshaw Rothwell Royle Sagar Scholes
Schofield Senior Shackleton Sharples Shuttleworth Sidebottom Slater Smethurst Sowerby Speight Spencer Stansfield Starkey
Stead Stott Sugden Sutcliffe Swallow Tasker Tattersall Thewlis Thornber Threlfall Tillotson Toothill Townend Turton
Varley Waddington Wadsworth Walmsley Warburton Wardle Waring Wainwright Whiteley Whittaker Whitworth Wilde Wolstenholme
Womersley Wood Worsley Yates Yeadon Ackroyd Barstow Briggs Calverley Dransfield Feather Gaunt Hepworth Jessop Kilner
Ledger Mallinson Normington Pogson Rushworth Shaw Tetley Utley Walshaw Booker Cardwell Dawes Eyre Furness Gill Holt""".split()

FIRST_NAMES = """Adam Alan Alice Alison Amanda Andrew Angela Anne Anthony Barbara Barry Brian Carol Caroline Catherine Chris
Christine Claire Colin Craig Daniel Darren Dawn Dean Deborah Denise Derek Diane Donna Douglas Elaine Elizabeth Eric
Fiona Gail Gary Gavin Geoffrey Gillian Graham Hazel Helen Ian Jacqueline James Janet Janice Jason Jean Jennifer Joanne
John Jonathan Joyce Julie Karen Kathleen Keith Kenneth Kevin Kim Laura Lee Linda Lisa Lorraine Louise Lynn Margaret Mark
Martin Matthew Maureen Michael Michelle Neil Nicola Nigel Patricia Paul Pauline Peter Philip Rachel Raymond Richard Robert
Ronald Rosemary Ruth Sandra Sarah Sharon Sheila Simon Stephen Steven Susan Teresa Timothy Tracey Valerie Wendy William
Yvonne Zoe""".split()

PERSONAS = {"Frances Davies": "head of economic statistics, Torvasay Statistics",
            "Stewart Sheppard": "data-sharing lead, the Revenue Office",
            "Irene Walters": "programme manager, Town Centre Renewal Fund, Department for the Economy"}
_PERSONA_SURNAMES = {n.split()[1] for n in PERSONAS}
_PERSONA_FIRST = {n.split()[0] for n in PERSONAS}
SURNAMES = [s for s in SURNAMES if s not in _PERSONA_SURNAMES]
FIRST_NAMES = [f for f in FIRST_NAMES if f not in _PERSONA_FIRST]

SURNAMES += """Alderson Allerton Anson Armitage Arkwright Ashton Askew Aspinall Badger Bancroft Bardsley Barker Barnsdale
Beaumont Bedford Bellamy Bilton Birtwistle Blackwell Blamire Bleasdale Bollard Bottomley Boyes Braithwaite Brayshaw
Brierley Brook Broughton Bullock Burnley Bywater Calthorpe Carnaby Catterall Cawood Chambers Clayton Clitheroe Coates
Collinson Cooksey Copley Cordingley Cowgill Cowling Crabb Craven Crosland Culshaw Dalby Darnbrook Dennison Denton Dibb
Dixon Dodsworth Dowson Duckett Dunwell Easby Eckersley Edge Elsworth Emsley Exley Fairburn Farrar Fawthrop Fieldhouse
Flather Forrest Fothergill Frankland Garbutt Gargrave Garnett Gilberthorpe Glover Goldsbrough Gomersall Gratton Greaves
Grundy Hainsworth Halliday Hampshire Hanley Harrop Hartas Hawksworth Haxby Hebblethwaite Hemingway Hesketh Hindley
Hinchliffe Holdsworth Holmes Horsfall Houldsworth Hudson Hustwick Ingle Inman Jackling Jowsey Kellett Kendall Kilburn
Kirkby Lamplugh Langstaff Lassey Lazenby Leeming Lightfoot Lofthouse Longstaff Lund Mawson Midgeley Moorby Moxon
Murgatroyd Myers Nettleton Newsome Normanton Oates Overend Parkinson Peacock Pennington Petch Pickering Pilkington
Pinder Pocklington Prest Pybus Raistrick Rawling Raynor Redman Ridsdale Rishworth Robinson Roebuck Rowntree Rushton
Sanderson Scaife Scarth Settle Sheard Shepherd Simpkin Skirrow Smallwood Snowden Stainthorpe Stansfield Stockdale
Storr Sunderland Swithenbank Taylor Teale Thackray Thornton Tindall Topham Trotter Turnbull Ulyatt Verity Wadley
Walker Waterhouse Wetherall Whitehead Wilkinson Willoughby Winterburn Witherington Wrigglesworth Yeoman Youngman""".split()
SURNAMES = sorted(set(SURNAMES))
FIRST_NAMES += """Aidan Alfie Amber Amy Ashley Beth Bethany Callum Carl Chloe Connor Danielle Declan Dominic Duncan Eleanor
Emily Ethan Faye Frank Freya Gareth Georgia Glenn Grace Hannah Harry Heather Holly Imogen Isaac Jack Jade Jake Jamie Jodie
Joe Josh Kate Katie Kieran Leanne Liam Lucy Luke Lydia Martyn Megan Melanie Molly Natalie Nathan Niall Oliver Owen Phoebe
Robyn Rory Ross Ryan Sally Samantha Scott Shaun Sophie Stacey Stuart Tom Toby Vicky""".split()
FIRST_NAMES = sorted(set(FIRST_NAMES) - _PERSONA_FIRST)
SURNAMES = [x for x in SURNAMES if x not in _PERSONA_SURNAMES]

# trades of independent shops: (SIC 2007 subclass, the words a trading name takes)
SHOP_TRADES = [("47110", ["Stores", "Mini Market", "Convenience Store", "General Stores"]),
               ("47190", ["Discount Store", "Variety Store", "Pound Shop"]),
               ("47210", ["Greengrocer", "Fruit and Veg"]), ("47220", ["Butchers", "Family Butcher"]),
               ("47230", ["Fishmonger"]), ("47240", ["Bakery", "Bakers", "Cake Shop"]),
               ("47250", ["Wine Merchants", "Off Licence"]), ("47260", ["Tobacconist"]),
               ("47290", ["Delicatessen", "Health Foods", "Farm Shop"]), ("47410", ["Computers"]),
               ("47421", ["Mobiles", "Phone Repairs"]), ("47510", ["Fabrics", "Wool Shop", "Haberdashery"]),
               ("47520", ["Hardware", "DIY", "Ironmongers"]), ("47530", ["Carpets", "Flooring"]),
               ("47540", ["Electrical"]), ("47599", ["Furniture", "Interiors", "Home Store", "Kitchenware"]), ("47591", ["Music"]),
               ("47610", ["Books", "Bookshop"]), ("47620", ["News", "Newsagents", "Stationers"]),
               ("47640", ["Cycles", "Sports", "Outdoor"]), ("47650", ["Toys", "Games"]),
               ("47710", ["Fashions", "Boutique", "Menswear", "Clothing"]), ("47721", ["Shoes", "Footwear"]),
               ("47730", ["Pharmacy", "Chemist"]), ("47741", ["Hearing"]), ("47749", ["Mobility"]),
               ("47750", ["Beauty", "Cosmetics"]), ("47760", ["Florist", "Pets", "Garden Shop"]),
               ("47770", ["Jewellers", "Watches"]), ("47781", ["Gallery", "Framing"]), ("47782", ["Opticians"]),
               ("47789", ["Gifts", "Crafts", "Cards"]), ("47791", ["Antiques"]), ("47799", ["Second Hand", "Vintage"])]

# retail park and warehouse independents (single-site)
RW_TRADES = [("47599", ["Furniture Centre", "Beds", "Sofa Warehouse"]), ("47530", ["Carpet Warehouse", "Flooring Centre"]),
             ("47520", ["Building Supplies", "DIY Centre", "Timber and Hardware"]), ("47760", ["Garden Centre", "Pet Superstore"]),
             ("47540", ["Appliance Centre"]), ("47599", ["Kitchen Studio", "Bathroom Centre", "Home Centre"])]
ONLINE_TRADES = ["Direct", "Online", "Outlet", "Mail Order", "Fulfilment"]

LANDLORD_WORDS = ["Estates", "Property Holdings", "Properties", "Investments", "Real Estate", "Property Company",
                  "Land and Property", "Commercial Property"]
LANDLORD_ROOTS = ["Harbour", "Northgate", "Westholm", "Castleview", "Kingsmarsh", "Quayside", "Ashlar", "Granite",
                  "Seaview", "Brackenhill", "Copperfield", "Highgable", "Larchcroft", "Millstone", "Oakhurst",
                  "Redstone", "Saltmarsh", "Thornwater", "Wharfside", "Cowslip", "Beacon", "Corbel", "Lintel",
                  "Architrave", "Plinth", "Rampart", "Sandstone", "Tidewater", "Gatehouse", "Keystone"]

# the multi-site retail employers: (kind, brand, registered name, SIC 2007 subclass)
CHAINS = [
    ("grocer", "Brackmoor", "Brackmoor Food Stores Limited", "47110"),
    ("grocer", "Torvasay Co-operative", "Torvasay Co-operative Society Limited", "47110"),
    ("grocer", "Kestle", "Kestle Supermarkets Limited", "47110"),
    ("grocer", "Halvask Fresh", "Halvask Fresh Foods Limited", "47110"),
    ("fashion", "Marlowe & Finch", "Marlowe and Finch Retail Limited", "47710"),
    ("fashion", "Tidemark", "Tidemark Clothing Limited", "47710"),
    ("fashion", "Pennant", "Pennant Fashions Limited", "47710"),
    ("fashion", "Cobble Shoes", "Cobble Shoes Limited", "47721"),
    ("fashion", "Hartsmere Home", "Hartsmere Home Stores Limited", "47599"),
    ("fashion", "Fernlea", "Fernlea Retail Limited", "47190"),
    ("fashion", "Quillon", "Quillon Stationery Limited", "47620"),
    ("fashion", "Slate & Shore", "Slate and Shore Outdoor Limited", "47640"),
    ("fashion", "Wrenhaven", "Wrenhaven Gifts Limited", "47789"),
    ("fashion", "Larkspur", "Larkspur Fashion Limited", "47710"),
    ("fashion", "Hobbyhorse Toys", "Hobbyhorse Toys and Games Limited", "47650"),
    ("fashion", "Bellcote", "Bellcote Stores Limited", "47190"),
    ("fashion", "Signalbox", "Signalbox Mobile Limited", "47421"),
    ("fashion", "Gannet Books", "Gannet Books Limited", "47610"),
    ("health", "Quellan Chemists", "Quellan Chemists Limited", "47730"),
    ("health", "Sightwell", "Sightwell Opticians Limited", "47782"),
    ("health", "Pellucid Beauty", "Pellucid Beauty Limited", "47750"),
    ("health", "Islandcare Pharmacy", "Islandcare Pharmacy Limited", "47730"),
    ("health", "Wellsprig", "Wellsprig Health Stores Limited", "47290"),
    ("home", "Hearthside", "Hearthside Furniture Limited", "47599"),
    ("home", "Joistworks", "Joistworks DIY Limited", "47520"),
    ("home", "Floorcraft", "Floorcraft Carpets Limited", "47530"),
    ("home", "Fernhollow", "Fernhollow Garden Centres Limited", "47760"),
    ("home", "Voltway", "Voltway Electrical Limited", "47540"),
    ("home", "Kilnhaven", "Kilnhaven Kitchens and Bathrooms Limited", "47599"),
]
SMALL_CHAIN_TRADES = ["47240", "47220", "47770", "47620", "47760", "47750", "47710", "47250", "47290", "47721",
                      "47730", "47789", "47640", "47410", "47290", "47240"]

# the owners of empty premises, as the companies register holds them: property companies under names that say so and
# under names that do not (nominee and holding companies, a year or a number), and the developers holding premises they
# bought for schemes; and the estate and letting agencies that trade from shops
OWNER_ROOTS = LANDLORD_ROOTS + [
    "Kittiwake", "Guillemot", "Fulmar", "Shearwater", "Curlew", "Dunlin", "Redshank", "Whimbrel", "Turnstone", "Eider",
    "Plover", "Sanderling", "Petrel", "Cormorant", "Lapwing", "Oystercatcher", "Heather", "Thrift", "Samphire",
    "Tormentil", "Bilberry", "Juniper", "Blackthorn", "Hawthorn", "Bramble", "Campion", "Anchorage", "Mooring",
    "Bollard", "Capstan", "Slipway", "Breakwater", "Lantern", "Tideway", "Wherry", "Basalt", "Chert", "Shale", "Schist",
    "Feldspar", "Marram", "Gullery", "Kelpie", "Selkie", "Mizzen", "Bowsprit", "Lugsail", "Cairn"]
OWNER_WORDS_PLAIN = ["Nominees", "Securities", "Capital", "Holdings", "Trustees", "Ventures", "Partners",
                     "Asset Management", "Trust Company"]
DEVELOPER_WORDS = ["Homes", "Developments", "Construction", "Build", "Regeneration"]
AGENT_WORDS = ["Estate Agents", "Estates", "Property Shop", "Property Services", "Lettings", "Homes", "Property"]
