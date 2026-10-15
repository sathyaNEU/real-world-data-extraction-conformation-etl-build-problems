"""task257 constants shared by every generator module.

Brackenmere Markets (fictional), a grocery chain in Ontario, Quebec and New Brunswick: 148 stores in 12 districts,
three distribution centres and a head office; its 2026 engagement survey run by Kestrava Listening (fictional), the
30 items, the survey calendar and the pack's file names."""
from __future__ import annotations

import datetime as dt

SEED = 2570944

CHAIN = "Brackenmere Markets"
VENDOR = "Kestrava Listening"
PEOPLE = {"head": "Alexander Copeland", "analytics": "Maria Murray", "vendor": "Melissa Vang"}

# Survey calendar (local dates at each site)
OPEN_DAY = dt.date(2026, 9, 14)
CLOSE_DAY = dt.date(2026, 9, 27)
LINKS_CLOSED_UTC = dt.datetime(2026, 9, 28, 6, 0)      # Kestrava stops accepting answers for all clients
INVITE_EXTRACT = dt.date(2026, 8, 31)                  # HR extract the distribution list was built from
INVITE_LOADED = dt.date(2026, 9, 2)
REORG_DAY = dt.date(2026, 7, 6)                        # sites renumbered and departments recoded
TEST_DAYS = (dt.date(2026, 9, 11), dt.date(2026, 9, 12))
EXPORT_UTC = dt.datetime(2026, 10, 19, 13, 42, 7)
HR_EXTRACT = dt.date(2026, 10, 16)
SITE_DIR_DATE = dt.date(2026, 10, 1)
STANDARD_DATE = dt.date(2025, 11, 17)
DECISION_DATE = dt.date(2026, 11, 24)                  # the executive team settles the 2027 dashboard

# UTC offsets in September (daylight time)
TZ_OFFSET = {"America/Toronto": -4, "America/Winnipeg": -5, "America/Moncton": -3}

# Districts: code, name, provinces, stores (name, city, province, format), formats: U urban, S suburban, T town,
# X express (a small urban format). Gatineau, Aylmer and Buckingham are Quebec stores in the Ottawa-Gatineau district.
DISTRICTS = [
    ("OTG", "Ottawa-Gatineau", [
        ("Barrhaven", "Ottawa", "ON", "S"), ("Kanata", "Ottawa", "ON", "S"), ("Orleans", "Ottawa", "ON", "S"),
        ("Westboro", "Ottawa", "ON", "U"), ("Alta Vista", "Ottawa", "ON", "U"), ("Nepean", "Ottawa", "ON", "S"),
        ("Stittsville", "Ottawa", "ON", "T"), ("Glebe", "Ottawa", "ON", "X"), ("Centretown", "Ottawa", "ON", "X"),
        ("Hull", "Gatineau", "QC", "U"), ("Plateau", "Gatineau", "QC", "S"), ("Aylmer", "Gatineau", "QC", "S"),
        ("Buckingham", "Gatineau", "QC", "T"), ("Rockland", "Clarence-Rockland", "ON", "T")]),
    ("EON", "Eastern Ontario", [
        ("Cornwall", "Cornwall", "ON", "S"), ("Brockville", "Brockville", "ON", "S"),
        ("Hawkesbury", "Hawkesbury", "ON", "T"), ("Kemptville", "North Grenville", "ON", "T"),
        ("Smiths Falls", "Smiths Falls", "ON", "T"), ("Perth", "Perth", "ON", "T"), ("Prescott", "Prescott", "ON", "T"),
        ("Carleton Place", "Carleton Place", "ON", "T"), ("Arnprior", "Arnprior", "ON", "T"),
        ("Renfrew", "Renfrew", "ON", "T")]),
    ("KQU", "Kingston and Quinte", [
        ("Cataraqui", "Kingston", "ON", "S"), ("Princess Street", "Kingston", "ON", "X"),
        ("Kingscourt", "Kingston", "ON", "U"), ("Napanee", "Greater Napanee", "ON", "T"),
        ("Belleville", "Belleville", "ON", "S"), ("Belleville North", "Belleville", "ON", "S"),
        ("Trenton", "Quinte West", "ON", "S"), ("Picton", "Prince Edward County", "ON", "T"),
        ("Gananoque", "Gananoque", "ON", "T")]),
    ("DKA", "Durham and Kawartha", [
        ("Oshawa North", "Oshawa", "ON", "S"), ("Oshawa Centre", "Oshawa", "ON", "U"), ("Whitby", "Whitby", "ON", "S"),
        ("Ajax", "Ajax", "ON", "S"), ("Pickering", "Pickering", "ON", "S"), ("Bowmanville", "Clarington", "ON", "S"),
        ("Port Perry", "Scugog", "ON", "T"), ("Uxbridge", "Uxbridge", "ON", "T"),
        ("Peterborough", "Peterborough", "ON", "S"), ("Lansdowne", "Peterborough", "ON", "S"),
        ("Lindsay", "Kawartha Lakes", "ON", "T"), ("Cobourg", "Cobourg", "ON", "T")]),
    ("TOE", "Toronto East", [
        ("Scarborough Town", "Toronto", "ON", "U"), ("Agincourt", "Toronto", "ON", "U"), ("Malvern", "Toronto", "ON", "U"),
        ("Leslieville", "Toronto", "ON", "X"), ("Danforth", "Toronto", "ON", "X"), ("Beaches", "Toronto", "ON", "U"),
        ("East York", "Toronto", "ON", "U"), ("Don Mills", "Toronto", "ON", "U"), ("Leaside", "Toronto", "ON", "U"),
        ("Unionville", "Markham", "ON", "S"), ("Cornell", "Markham", "ON", "S"),
        ("Richmond Hill", "Richmond Hill", "ON", "S"), ("Thornhill", "Vaughan", "ON", "S"),
        ("Bayview Village", "Toronto", "ON", "U"), ("Willowdale", "Toronto", "ON", "U")]),
    ("TOW", "Toronto West", [
        ("Islington", "Toronto", "ON", "U"), ("Queensway", "Toronto", "ON", "U"),
        ("Liberty Village", "Toronto", "ON", "X"), ("Roncesvalles", "Toronto", "ON", "X"),
        ("Bloor West", "Toronto", "ON", "U"), ("Junction", "Toronto", "ON", "U"), ("Weston", "Toronto", "ON", "U"),
        ("Meadowvale", "Mississauga", "ON", "S"), ("Erin Mills", "Mississauga", "ON", "S"),
        ("Port Credit", "Mississauga", "ON", "S"), ("Mount Pleasant", "Brampton", "ON", "S"),
        ("Springdale", "Brampton", "ON", "S"), ("Bolton", "Caledon", "ON", "T"), ("Caledon East", "Caledon", "ON", "T"),
        ("Glen Abbey", "Oakville", "ON", "S"), ("Milton", "Milton", "ON", "S")]),
    ("HNI", "Hamilton and Niagara", [
        ("Westdale", "Hamilton", "ON", "U"), ("Hamilton Mountain", "Hamilton", "ON", "U"),
        ("Stoney Creek", "Hamilton", "ON", "S"), ("Ancaster", "Hamilton", "ON", "S"), ("Dundas", "Hamilton", "ON", "T"),
        ("Appleby", "Burlington", "ON", "S"), ("Grimsby", "Grimsby", "ON", "T"),
        ("St. Catharines", "St. Catharines", "ON", "S"), ("Grantham", "St. Catharines", "ON", "S"),
        ("Niagara Falls", "Niagara Falls", "ON", "S"), ("Welland", "Welland", "ON", "S"),
        ("Fort Erie", "Fort Erie", "ON", "T"), ("Port Colborne", "Port Colborne", "ON", "T"),
        ("Niagara-on-the-Lake", "Niagara-on-the-Lake", "ON", "T")]),
    ("NON", "Northern Ontario", [
        ("New Sudbury", "Greater Sudbury", "ON", "S"), ("South End", "Greater Sudbury", "ON", "S"),
        ("North Bay", "North Bay", "ON", "S"), ("Sault Ste. Marie", "Sault Ste. Marie", "ON", "S"),
        ("Timmins", "Timmins", "ON", "S"), ("Kapuskasing", "Kapuskasing", "ON", "T"),
        ("Elliot Lake", "Elliot Lake", "ON", "T"), ("Intercity", "Thunder Bay", "ON", "S"),
        ("Westfort", "Thunder Bay", "ON", "T"), ("Kenora", "Kenora", "ON", "T"), ("Dryden", "Dryden", "ON", "T"),
        ("Fort Frances", "Fort Frances", "ON", "T")]),
    ("MTL", "Montréal", [
        ("Rosemont", "Montréal", "QC", "U"), ("Plateau-Mont-Royal", "Montréal", "QC", "X"),
        ("Villeray", "Montréal", "QC", "U"), ("Hochelaga", "Montréal", "QC", "U"), ("Verdun", "Montréal", "QC", "U"),
        ("LaSalle", "Montréal", "QC", "U"), ("Saint-Laurent", "Montréal", "QC", "U"),
        ("Ahuntsic", "Montréal", "QC", "U"), ("Anjou", "Montréal", "QC", "S"),
        ("Pointe-aux-Trembles", "Montréal", "QC", "S"), ("Notre-Dame-de-Grâce", "Montréal", "QC", "U"),
        ("Outremont", "Montréal", "QC", "X"), ("Pierrefonds", "Montréal", "QC", "S"), ("Dorval", "Dorval", "QC", "S"),
        ("Montréal-Nord", "Montréal", "QC", "U")]),
    ("LLA", "Laval and Laurentides", [
        ("Chomedey", "Laval", "QC", "S"), ("Sainte-Rose", "Laval", "QC", "S"), ("Vimont", "Laval", "QC", "S"),
        ("Duvernay", "Laval", "QC", "S"), ("Saint-Jérôme", "Saint-Jérôme", "QC", "S"),
        ("Blainville", "Blainville", "QC", "S"), ("Boisbriand", "Boisbriand", "QC", "S"),
        ("Mirabel", "Mirabel", "QC", "T"), ("Sainte-Agathe-des-Monts", "Sainte-Agathe-des-Monts", "QC", "T"),
        ("Terrebonne", "Terrebonne", "QC", "S"), ("Repentigny", "Repentigny", "QC", "S")]),
    ("MES", "Montérégie and Estrie", [
        ("Longueuil", "Longueuil", "QC", "U"), ("Brossard", "Brossard", "QC", "S"),
        ("Saint-Hubert", "Longueuil", "QC", "S"), ("Boucherville", "Boucherville", "QC", "S"),
        ("Chambly", "Chambly", "QC", "T"), ("Saint-Jean-sur-Richelieu", "Saint-Jean-sur-Richelieu", "QC", "S"),
        ("Granby", "Granby", "QC", "S"), ("Saint-Hyacinthe", "Saint-Hyacinthe", "QC", "S"),
        ("Sherbrooke Nord", "Sherbrooke", "QC", "S"), ("Fleurimont", "Sherbrooke", "QC", "S"),
        ("Magog", "Magog", "QC", "T"), ("Cowansville", "Cowansville", "QC", "T")]),
    ("NBR", "New Brunswick", [
        ("Mountain Road", "Moncton", "NB", "S"), ("Elmwood", "Moncton", "NB", "S"), ("Dieppe", "Dieppe", "NB", "S"),
        ("Saint John West", "Saint John", "NB", "S"), ("Saint John East", "Saint John", "NB", "S"),
        ("Fredericton North", "Fredericton", "NB", "S"), ("Uptown", "Fredericton", "NB", "X"),
        ("Bathurst", "Bathurst", "NB", "T")]),
]
CENTRAL_TIME = {"Kenora", "Dryden", "Fort Frances"}

# Non-store sites: site number, legacy number, name, city, province, type, time zone
OTHER_SITES = [
    (9001, 801, "Milton Distribution Centre", "Milton", "ON", "distribution centre", "America/Toronto"),
    (9002, 802, "Laval Distribution Centre", "Laval", "QC", "distribution centre", "America/Toronto"),
    (9003, 803, "Moncton Distribution Centre", "Moncton", "NB", "distribution centre", "America/Moncton"),
    (9100, 900, "Head Office", "Oakville", "ON", "head office", "America/Toronto"),
]

# The 30 items. Topic letters: W workload and staffing, T tools and basics, M manager, G growth, B belonging,
# R recognition (topics are the generator's own labels; nothing in the pack names them). Factor 0 resources,
# 1 leadership and growth, 2 connection. kind 'a5' five-point agreement, 'yn' yes or no. rev: negatively worded.
ITEMS = [
    # code, topic, kind, rev, English, French
    ("W1", "W", "a5", False, "My workload is manageable on a normal shift.",
     "Ma charge de travail est raisonnable pendant un quart normal."),
    ("W2", "W", "a5", False, "Enough people are scheduled on my shifts to get the work done.",
     "Il y a assez de personnel à l'horaire pendant mes quarts pour faire le travail."),
    ("W3", "W", "a5", True, "I often have to skip or cut short my breaks.",
     "Je dois souvent sauter ou écourter mes pauses."),
    ("W4", "W", "a5", False, "My schedule gives me enough rest between shifts.",
     "Mon horaire me laisse assez de repos entre deux quarts."),
    ("W5", "W", "yn", False, "In the past four weeks, were you able to leave on time at the end of every shift?",
     "Au cours des quatre dernières semaines, avez-vous pu partir à l'heure à la fin de chaque quart?"),
    ("T1", "T", "yn", False, "In the past four weeks, was your scanner or till working whenever you needed it?",
     "Au cours des quatre dernières semaines, votre lecteur ou votre caisse fonctionnait-il chaque fois que vous en "
     "aviez besoin?"),
    ("T2", "T", "yn", False, "In the past four weeks, was your schedule posted at least two weeks ahead?",
     "Au cours des quatre dernières semaines, votre horaire a-t-il été affiché au moins deux semaines à l'avance?"),
    ("T3", "T", "yn", False, "Do you have the safety gear your job requires?",
     "Avez-vous l'équipement de sécurité que votre travail exige?"),
    ("T4", "T", "yn", False, "Were your last three pays correct and on time?",
     "Vos trois dernières paies étaient-elles exactes et versées à temps?"),
    ("T5", "T", "yn", False, "Can you get into the scheduling and pay app when you need to?",
     "Pouvez-vous accéder à l'application d'horaire et de paie quand vous en avez besoin?"),
    ("T6", "T", "yn", False, "Do you know who to call when equipment in your department breaks down?",
     "Savez-vous qui appeler quand un équipement de votre service tombe en panne?"),
    ("M1", "M", "a5", False, "My manager treats me with respect.",
     "Mon gestionnaire me traite avec respect."),
    ("M2", "M", "a5", False, "My manager keeps me informed about changes that affect my work.",
     "Mon gestionnaire me tient informé des changements qui touchent mon travail."),
    ("M3", "M", "a5", True, "My manager is hard to approach about problems.",
     "Il est difficile d'aborder mon gestionnaire au sujet d'un problème."),
    ("M4", "M", "a5", False, "My manager gives me useful feedback on my work.",
     "Mon gestionnaire me donne une rétroaction utile sur mon travail."),
    ("M5", "M", "yn", False, "In the past four weeks, has your manager talked with you one to one about how you are "
                             "doing?",
     "Au cours des quatre dernières semaines, votre gestionnaire vous a-t-il parlé seul à seul de la façon dont les "
     "choses se passent pour vous?"),
    ("G1", "G", "yn", False, "Do you have a written development plan agreed with your manager?",
     "Avez-vous un plan de perfectionnement écrit convenu avec votre gestionnaire?"),
    ("G2", "G", "yn", False, "In the past twelve months, have you been offered training beyond what your role "
                             "requires?",
     "Au cours des douze derniers mois, vous a-t-on offert une formation au-delà de ce que votre poste exige?"),
    ("G3", "G", "yn", False, "In the past twelve months, have you been put forward for a promotion or a lead role?",
     "Au cours des douze derniers mois, a-t-on proposé votre candidature pour une promotion ou un rôle de chef "
     "d'équipe?"),
    ("G4", "G", "yn", False, "In the past twelve months, have you shadowed or covered a role in another department to "
                             "learn it?",
     "Au cours des douze derniers mois, avez-vous accompagné ou remplacé une personne d'un autre service pour "
     "apprendre son rôle?"),
    ("G5", "G", "yn", False, "In the past twelve months, has someone outside your store or site talked with you about "
                             "your career?",
     "Au cours des douze derniers mois, une personne de l'extérieur de votre magasin ou de votre site vous a-t-elle "
     "parlé de votre carrière?"),
    ("G6", "G", "yn", False, "Have you been invited to apply to the Brackenmere Leaders programme?",
     "Vous a-t-on invité à poser votre candidature au programme Leaders Brackenmere?"),
    ("B1", "B", "a5", False, "I feel part of a team at work.",
     "Je me sens membre d'une équipe au travail."),
    ("B2", "B", "a5", True, "I sometimes feel like an outsider where I work.",
     "Je me sens parfois à l'écart à mon travail."),
    ("B3", "B", "a5", False, "People here treat each other fairly whatever their background.",
     "Ici, les gens se traitent équitablement, quelle que soit leur origine."),
    ("B4", "B", "yn", False, "In the past four weeks, has a coworker helped you without being asked?",
     "Au cours des quatre dernières semaines, un collègue vous a-t-il aidé sans que vous le demandiez?"),
    ("R1", "R", "a5", False, "I get credit for the work I do.",
     "On reconnaît le travail que j'accomplis."),
    ("R2", "R", "a5", True, "Good work in my department usually goes unnoticed.",
     "Le bon travail passe généralement inaperçu dans mon service."),
    ("R3", "R", "a5", False, "The people I work with appreciate what I do.",
     "Les personnes avec qui je travaille apprécient ce que je fais."),
    ("R4", "R", "yn", False, "In the past four weeks, has anyone thanked you for your work?",
     "Au cours des quatre dernières semaines, quelqu'un vous a-t-il remercié pour votre travail?"),
]
TOPIC_FACTOR = {"W": 0, "T": 0, "M": 1, "G": 1, "B": 2, "R": 2}
FACTOR_NAME = {0: "Resources", 1: "Manager and growth", 2: "Connection"}

# The English questionnaire order (item keys) and the French order (Kestrava's French version was laid out with its own
# item randomisation); the export's codes follow each order
EN_ORDER = ["M1", "W1", "B1", "T1", "R1", "G1", "W2", "M2", "T2", "B2", "G2", "R2", "W3", "T3", "M3", "B3", "G3",
            "R3", "T4", "W4", "M4", "G4", "B4", "T5", "R4", "G5", "W5", "M5", "T6", "G6"]
FR_ORDER = ["R4", "W5", "G1", "B1", "W4", "M2", "W3", "M4", "G4", "R3", "W2", "T5", "T6", "M5", "T1", "M1", "M3", "T2",
            "W1", "T4", "G3", "T3", "G2", "G6", "B3", "B2", "R2", "B4", "R1", "G5"]

ENPS_EN = "How likely are you to recommend Brackenmere Markets as a place to work? (0 not at all likely, 10 extremely " \
          "likely)"
ENPS_FR = "Quelle est la probabilité que vous recommandiez Marchés Brackenmere comme employeur? (0 pas du tout " \
          "probable, 10 extrêmement probable)"

# Pack file names
RESPONSES = "kestrava_brackenmere_2026_responses.csv"
SUBMISSIONS = "kestrava_brackenmere_2026_submissions.csv"
CODEBOOK = "kestrava_brackenmere_2026_codebook.xlsx"
EXPORT_NOTES = "kestrava_export_notes_2026.pdf"
INVITATIONS = "kestrava_brackenmere_2026_distribution_list.csv"
KIOSK = "kiosk_sessions_2026-09.jsonl"
PAPER = "paper_returns_engagement_2026.xlsx"
HRIS = "hris_assignment_history_2026.csv"
SITES = "site_directory_2026-10.csv"
STANDARD = "survey_reporting_standard_2025.pdf"
PULSE = "pulse_survey_2026_q2_site_results.csv"
BENCHMARK = "kestrava_retail_benchmark_2026.xlsx"

DELIVERABLES = ("engagement_subscales_2027.xlsx", "engagement_dimensions_2026.png", "engagement_subscales_2027.md")


def site_tz_offset(tz):
    return TZ_OFFSET[tz]


def local_close_utc(tz):
    """The instant the survey closed at a site: 23:59:59 local time on the closing day, in UTC (naive)."""
    off = TZ_OFFSET[tz]
    return dt.datetime(CLOSE_DAY.year, CLOSE_DAY.month, CLOSE_DAY.day, 23, 59, 59) - dt.timedelta(hours=off)


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")
