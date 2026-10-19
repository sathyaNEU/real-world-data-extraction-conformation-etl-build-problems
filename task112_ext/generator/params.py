"""task112_ext constants: a regional grocery chain's loyalty programme and its 2027 customer reach (dataset only)."""
import datetime as dt

SEED = 112
CHAIN = "Brannvik Livs AB"
CHAIN_DISPLAY = "Brännvik Livs AB"
PROGRAMME = "Brännvik Plus"
DOMAIN = "brannviklivs.se"
AS_OF = dt.date(2028, 1, 12)          # the morning the folder was put together
EXTRACT = dt.date(2028, 1, 8)         # the warehouse extract date
YEAR = 2027
MEMBERS = 40000
LAUNCH = dt.date(2013, 3, 1)          # the programme's launch
APP_LAUNCH = dt.date(2019, 4, 1)
CONSENT_LIVE = dt.date(2026, 1, 1)    # the consent platform's go-live, the state migrated at midnight
PEOPLE = {
    "crm": ("Victor Malmström", "victor.malmstrom", "CRM manager"),
    "campaigns": ("Mia Nygren", "mia.nygren", "campaign manager"),
    "dpo": ("Elisabet Nilsson", "elisabet.nilsson", "data protection officer"),
    "media": ("Gustav Engström", "gustav.engstrom", "media buyer"),
}

# municipality: (county letter, county, postcode areas, population, municipality code)
MUNIS = {
    "Gävle": ("X", "Gävleborg", ["802", "803", "804", "805", "806"], 103600, "2180"),
    "Sandviken": ("X", "Gävleborg", ["811"], 39900, "2181"),
    "Hofors": ("X", "Gävleborg", ["813"], 9500, "2104"),
    "Ockelbo": ("X", "Gävleborg", ["816"], 5900, "2101"),
    "Bollnäs": ("X", "Gävleborg", ["821"], 26300, "2183"),
    "Ovanåker": ("X", "Gävleborg", ["828"], 11500, "2121"),
    "Söderhamn": ("X", "Gävleborg", ["826"], 25300, "2182"),
    "Hudiksvall": ("X", "Gävleborg", ["824"], 37800, "2184"),
    "Nordanstig": ("X", "Gävleborg", ["820"], 9400, "2132"),
    "Ljusdal": ("X", "Gävleborg", ["827"], 18900, "2161"),
    "Sundsvall": ("Y", "Västernorrland", ["852", "853", "854", "856", "857"], 99400, "2281"),
    "Timrå": ("Y", "Västernorrland", ["861"], 18200, "2262"),
    "Härnösand": ("Y", "Västernorrland", ["871"], 24800, "2280"),
    "Kramfors": ("Y", "Västernorrland", ["872"], 18300, "2282"),
    "Sollefteå": ("Y", "Västernorrland", ["881"], 19100, "2283"),
    "Ånge": ("Y", "Västernorrland", ["841"], 9000, "2260"),
    "Örnsköldsvik": ("Y", "Västernorrland", ["891", "892", "893"], 56300, "2284"),
}
# stores per municipality; members in a municipality without a store shop in the neighbouring one
STORES = {"Gävle": 4, "Sundsvall": 4, "Örnsköldsvik": 2, "Sandviken": 2, "Hudiksvall": 2,
          "Söderhamn": 1, "Bollnäs": 1, "Ljusdal": 1, "Härnösand": 1, "Timrå": 1, "Kramfors": 1,
          "Sollefteå": 1, "Ovanåker": 1, "Hofors": 1, "Ånge": 1}
NEIGHBOUR = {"Ockelbo": "Gävle", "Nordanstig": "Hudiksvall"}

# the tier rule (qualifying purchases in a calendar year, SEK, all stores)
SILVER, GULD = 18000, 40000

# ------------------------------------------------------------------ the 2027 campaigns
# code, name, purpose, channels, start, end, audience, budget kSEK (media and production), owner
CAMPAIGNS = [
    ("BV27-01", "Plusbrevet", "retention", "email", "2027-01-07", "2028-01-05",
     "Members with email consent, every other Thursday", 0, "crm"),
    ("BV27-02", "Välkommen till Brännvik Plus", "onboarding", "email", "2027-01-01", "2027-12-31",
     "New members with email consent, on joining and 7 and 21 days after", 0, "crm"),
    ("BV27-03", "Vinterklipp", "traffic", "sms, push", "2027-01-22", "2027-01-31",
     "SMS: members in Gävleborg with SMS consent. Push: app users with push consent", 9, "campaigns"),
    ("BV27-04", "Fettisdagen", "traffic", "push", "2027-02-09", "2027-02-09",
     "App users with push consent", 0, "campaigns"),
    ("BV27-05", "Vårkatalogen", "awareness", "direct mail, email", "2027-03-15", "2027-04-04",
     "Mail: households with post consent. Email: members with email consent", 340, "campaigns"),
    ("BV27-06", "Påsk", "seasonal", "email, sms, push, paid social", "2027-03-19", "2027-03-29",
     "All members by consented channel; Meta: 18 to 64 in both counties", 72, "campaigns"),
    ("BV27-07", "Grillstart", "seasonal", "email, push, paid social", "2027-05-03", "2027-05-23",
     "All members by consented channel; Meta: 18 to 64 in both counties", 70, "campaigns"),
    ("BV27-08", "Midsommar", "seasonal", "email, sms, push, paid social", "2027-06-14", "2027-06-26",
     "All members by consented channel; Meta: 18 to 64 in both counties", 76, "campaigns"),
    ("BV27-09", "Kräftpremiär", "seasonal", "email, push", "2027-08-04", "2027-08-15",
     "All members by consented channel", 0, "campaigns"),
    ("BV27-10", "Vi saknar dig", "win-back", "email, sms", "2027-09-01", "2027-09-30",
     "Members with purchases January to May 2027 and none June to August 2027", 6, "crm"),
    ("BV27-11", "Skördefest", "awareness", "email, paid social", "2027-09-13", "2027-09-26",
     "Members with email consent; Meta: 18 to 64 in both counties", 46, "campaigns"),
    ("BV27-12", "Guldveckan", "loyalty", "email, push", "2027-10-11", "2027-10-17",
     "Guld members (2027 tier)", 0, "crm"),
    ("BV27-13", "Julbrevet", "seasonal", "direct mail, email, sms, push, paid social", "2027-12-01", "2027-12-24",
     "Mail: households buying for 6,000 SEK or more January to October 2027. Other channels: all members by "
     "consented channel; Meta: 18 to 64 in both counties", 395, "campaigns"),
    ("BV27-14", "Bli medlem", "acquisition", "paid social", "2027-01-04", "2027-12-19",
     "Meta: 18 to 64 in both counties, members excluded by customer list", 182, "media"),
]

NEWSLETTER = [dt.date(2027, 1, 7) + dt.timedelta(days=14 * k) for k in range(26)]
THEMES = ["Nystart i k\u00f6ket", "Soppor som v\u00e4rmer", "Semlor och fettisdag", "Sportlovsmat",
          "V\u00e5rens f\u00f6rsta prim\u00f6rer", "P\u00e5skbordet b\u00f6rjar h\u00e4r", "Enkla vardagsr\u00e4tter",
          "Valborg och v\u00e5rgrill", "Rabarber och sparris", "Studentfest och kalas", "Sommarens jordgubbar",
          "Inf\u00f6r midsommar", "Midsommarafton i morgon", "Picknick i juli", "Grillat mitt i sommaren",
          "Kr\u00e4ftor och surstr\u00f6mming", "Skolstart och matl\u00e5dor", "Svamp och h\u00f6stens sk\u00f6rd",
          "\u00c4pplen fr\u00e5n trakten", "Gryta och l\u00e5ngkok", "Viltk\u00f6tt fr\u00e5n trakten",
          "H\u00f6stlov och halloween", "Fars dag p\u00e5 s\u00f6ndag", "F\u00f6rsta advent", "Lucia och julbak",
          "Mellandagsmat"]

# email drops beside the newsletter and the welcome series: mailing id, campaign, local send time, audience, subject,
# interest (the read propensity against a newsletter issue)
EMAILS = [
    ("BV27-05-E1", "BV27-05", (2027, 3, 16, 7, 0), "all", "Vårkatalogen är här", 1.05),
    ("BV27-06-E1", "BV27-06", (2027, 3, 22, 7, 0), "all", "Påskhandla med Brännvik Plus", 1.10),
    ("BV27-07-E1", "BV27-07", (2027, 5, 3, 7, 0), "all", "Dags att tända grillen", 1.0),
    ("BV27-08-E1", "BV27-08", (2027, 6, 14, 7, 0), "all", "Allt till midsommarbordet", 1.12),
    ("BV27-09-E1", "BV27-09", (2027, 8, 4, 7, 0), "all", "Kräftpremiär i veckan", 0.95),
    ("BV27-10-E1", "BV27-10", (2027, 9, 1, 7, 30), "lapsed", "Vi saknar dig, här är 100 kr", 0.80),
    ("BV27-11-E1", "BV27-11", (2027, 9, 13, 7, 0), "all", "Skördefest: närodlat i butik", 0.92),
    ("BV27-12-E1", "BV27-12", (2027, 10, 11, 7, 0), "guld", "Guldveckan: 10 % på hela köpet", 1.35),
    ("BV27-13-E1", "BV27-13", (2027, 12, 6, 7, 0), "all", "Julbrevet: allt till julbordet", 1.15),
    ("BV27-13-E2", "BV27-13", (2027, 12, 20, 7, 0), "all", "Sista dagarna före jul", 1.0),
]
WELCOME = [("BV27-02-W1", 0, "Välkommen till Brännvik Plus"),
           ("BV27-02-W2", 7, "Så får du ut mest av ditt medlemskap"),
           ("BV27-02-W3", 21, "Dina personliga erbjudanden väntar")]

# SMS drops: id, campaign, local submit time, audience, characters of text
SMS = [
    ("BV27-03-S1", "BV27-03", (2027, 1, 22, 10, 0), "county:X", 148),
    ("BV27-06-S1", "BV27-06", (2027, 3, 25, 11, 0), "all", 156),
    ("BV27-08-S1", "BV27-08", (2027, 6, 23, 10, 0), "all", 171),
    ("BV27-10-S1", "BV27-10", (2027, 9, 9, 12, 0), "lapsed", 139),
    ("BV27-13-S1", "BV27-13", (2027, 12, 16, 10, 0), "all", 158),
    ("BV27-13-S2", "BV27-13", (2027, 12, 22, 15, 0), "all", 122),
]
SMS_PRICE = 0.34          # SEK per segment
# push drops: id, campaign, local send time, audience, title
PUSH = [
    ("BV27-03-P1", "BV27-03", (2027, 1, 22, 8, 30), "all", "Vinterklipp hela helgen"),
    ("BV27-04-P1", "BV27-04", (2027, 2, 9, 8, 15), "all", "Semlor 4 för 60 kr i dag"),
    ("BV27-06-P1", "BV27-06", (2027, 3, 24, 17, 0), "all", "Påskens erbjudanden i appen"),
    ("BV27-06-P2", "BV27-06", (2027, 3, 27, 9, 30), "all", "Öppet påskafton kl. 8-18"),
    ("BV27-07-P1", "BV27-07", (2027, 5, 7, 16, 0), "all", "Grillhelg? Vi har kolen"),
    ("BV27-08-P1", "BV27-08", (2027, 6, 24, 16, 30), "all", "Glöm inte jordgubbarna"),
    ("BV27-09-P1", "BV27-09", (2027, 8, 4, 16, 0), "all", "Kräftpremiär i dag"),
    ("BV27-12-P1", "BV27-12", (2027, 10, 11, 8, 30), "guld", "Guldveckan har börjat"),
    ("BV27-13-P1", "BV27-13", (2027, 12, 10, 17, 0), "all", "Julskinkan är här"),
    ("BV27-13-P3", "BV27-13", (2027, 12, 22, 8, 30), "all", "Öppettider över jul"),
]
# addressed mail: drop code, campaign, posted, selection date, audience, print and postage SEK per piece
MAIL = [("BV27-05-D1", "BV27-05", dt.date(2027, 3, 11), dt.date(2027, 2, 24), "households_post", 9.85),
        ("BV27-13-D1", "BV27-13", dt.date(2027, 12, 1), dt.date(2027, 11, 15), "households_spend", 11.40)]
# Meta flights: campaign, first day, last day, planned SEK, objective
META = [("BV27-06", dt.date(2027, 3, 19), dt.date(2027, 3, 28), 48000, "Traffic"),
        ("BV27-07", dt.date(2027, 5, 3), dt.date(2027, 5, 23), 62000, "Traffic"),
        ("BV27-08", dt.date(2027, 6, 14), dt.date(2027, 6, 25), 55000, "Traffic"),
        ("BV27-11", dt.date(2027, 9, 13), dt.date(2027, 9, 26), 40000, "Awareness"),
        ("BV27-13", dt.date(2027, 12, 6), dt.date(2027, 12, 23), 85000, "Traffic"),
        ("BV27-14", dt.date(2027, 1, 4), dt.date(2027, 12, 19), 180000, "Leads")]

# personal offers loaded to members' cards: code, campaign, text, kind (fixed SEK or per cent), value, base rate
OFFERS = [
    ("BV27-02-O1", "BV27-02", "50 kr rabatt på första köpet över 300 kr", "fixed", 50, 0.30),
    ("BV27-05-O1", "BV27-05", "20 % på vårlök och sättpotatis", "pct", 20, 0.035),
    ("BV27-05-O2", "BV27-05", "25 kr rabatt vid köp över 400 kr", "fixed", 25, 0.060),
    ("BV27-06-O1", "BV27-06", "Lammstek 20 % billigare", "pct", 20, 0.055),
    ("BV27-06-O2", "BV27-06", "Påskgodis 3 hg för 2", "pct", 33, 0.070),
    ("BV27-07-O1", "BV27-07", "30 kr rabatt på grillkol och tändvätska", "fixed", 30, 0.045),
    ("BV27-08-O1", "BV27-08", "Sill och potatis 15 % billigare", "pct", 15, 0.065),
    ("BV27-08-O2", "BV27-08", "Jordgubbar 2 liter, 20 kr rabatt", "fixed", 20, 0.080),
    ("BV27-09-O1", "BV27-09", "Kräftor 1 kg, 40 kr rabatt", "fixed", 40, 0.040),
    ("BV27-10-O1", "BV27-10", "100 kr rabatt vid köp över 500 kr", "fixed", 100, 0.11),
    ("BV27-11-O1", "BV27-11", "Närodlade grönsaker 15 % billigare", "pct", 15, 0.050),
    ("BV27-12-O1", "BV27-12", "10 % på hela köpet över 300 kr", "pct", 10, 0.34),
    ("BV27-13-O1", "BV27-13", "Julskinka 25 % billigare", "pct", 25, 0.090),
    ("BV27-13-O2", "BV27-13", "50 kr rabatt vid köp över 700 kr", "fixed", 50, 0.075),
]
# the newsletter's issue offers: one per issue, valid 14 days
NEWS_OFFER = [("fixed", 15), ("pct", 20), ("fixed", 10), ("fixed", 20), ("pct", 15), ("fixed", 25), ("pct", 20),
              ("fixed", 15), ("pct", 25), ("fixed", 20), ("fixed", 10), ("pct", 20), ("fixed", 15), ("fixed", 20),
              ("pct", 15), ("fixed", 25), ("pct", 20), ("fixed", 15), ("fixed", 20), ("pct", 25), ("fixed", 10),
              ("pct", 15), ("fixed", 20), ("fixed", 25), ("pct", 20), ("fixed", 15)]
NEWS_ITEMS = ["kaffe 450 g", "frukt och gr\u00f6nt", "semlor fr\u00e5n bageriet", "pasta och ris", "f\u00e4rsk fisk",
              "p\u00e5skmust", "mj\u00f6lk och fil", "korv och grillk\u00f6tt", "rabarber och sparris", "t\u00e5rtor",
              "jordgubbar", "sill och lax", "glass", "grillk\u00f6tt", "vattenmelon", "kr\u00e4ftor",
              "matl\u00e5dor och kyckling", "svamp och potatis", "\u00e4pplen", "n\u00f6tk\u00f6tt f\u00f6r gryta",
              "viltf\u00e4rs", "pumpa och godis", "t\u00e5rtbotten och gr\u00e4dde", "gl\u00f6gg och pepparkakor",
              "saffran och kardemumma", "julost"]

# the purchase an offer needs before it applies (SEK); offers not listed apply to the item
OFFER_MIN = {"BV27-02-O1": 300, "BV27-05-O2": 400, "BV27-10-O1": 500, "BV27-12-O1": 300, "BV27-13-O2": 700}
