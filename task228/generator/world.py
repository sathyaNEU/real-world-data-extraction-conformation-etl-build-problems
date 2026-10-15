"""task228 world: Avisly Medier A/S (Copenhagen), its news app and its experiment platform. The group, the app, the
platform, the people and the data are fictional."""

ORG = "Avisly Medier A/S"
APP = "Avisly"
DESK = "Data-health desk"
PLATFORM_TEAM = "Experimentation Platform"

PEOPLE = {"head": "Mathilde Knudsen", "engineer": "Kaspar Gregersen", "analyst": "Inge Lund",
          "reviewers": ["Inge Lund", "Thea Koch", "Justina Bach"]}

TEAMS = ["Front Page", "Article", "Audio", "Subscriptions", "Notifications", "Search"]

TITLES = {
    "Front Page": ["Lead story image ratio", "Breaking strip placement", "Most read rail order", "Topic chips row",
                   "Local news module", "Front page density", "Live score widget", "Sunday edition layout",
                   "Opinion carousel", "Weather card in feed", "Card headline length", "Video row autoplay",
                   "Front page refresh prompt", "Election results tile"],
    "Article": ["Inline related links", "Reading time label", "Paragraph spacing", "Byline photo",
                "Comment teaser", "Article end recommendations", "Fact box styling", "Share sheet order",
                "Image gallery swipe", "Live blog pinned post", "Live blog update badge", "Font size control",
                "Read later button", "Correction notice format", "Article audio button"],
    "Audio": ["Audio player background mode", "Podcast autoplay next", "Mini player on front page",
              "Playback speed menu", "Download for offline", "Audio articles shelf", "Sleep timer",
              "Episode chapter marks", "Podcast follow prompt", "Car mode layout", "Audio resume point",
              "Daily briefing card", "Waveform scrubber"],
    "Subscriptions": ["Paywall copy", "Trial length banner", "Student offer page", "Checkout step order",
                      "Gift subscription entry", "Price anchor display", "Login wall timing", "Family plan teaser",
                      "Payment method order", "Cancellation survey", "Win-back offer", "Metered counter"],
    "Notifications": ["Breaking alert sound", "Push opt-in timing", "Evening digest push", "Topic follow alerts",
                      "Notification grouping", "Quiet hours default", "Local alert radius", "Sports result alerts",
                      "Push copy length", "Weekly roundup push", "In-app inbox", "Badge count reset",
                      "Alert preview image"],
    "Search": ["Search suggestions", "Recent searches", "Archive search filters", "Search result snippets",
               "Topic pages from search", "Spelling correction", "Search in audio", "Trending searches",
               "Author pages", "Date facet", "Saved searches", "Search empty state", "Voice search entry",
               "Tag cloud removal", "Search ranking freshness"],
}

TYPES = ["telemetry loss", "duplicate delivery", "late delivery", "consent loss"]
KIND_TYPE = {"loss": "telemetry loss", "dup": "duplicate delivery", "late": "late delivery", "consent": "consent loss"}

# incidents the register logs against the whole app (all experiments' arms alike), Copenhagen local time
APP_WIDE = [
    dict(opened="2026-02-11 09:40", frac=0.18, closed="2026-02-11 12:55", platforms=["ios", "android", "web"],
         first_call="telemetry loss", note="collector certificate rotation; uploads refused"),
    dict(opened="2026-03-29 01:20", frac=0.30, closed="2026-03-29 04:05", platforms=["ios", "android"],
         first_call="late delivery", note="uploader clock jump at the change to summer time"),
    dict(opened="2026-05-06 14:10", frac=0.31, closed="2026-05-06 18:25", platforms=["android", "web"],
         first_call="telemetry loss", note="edge routing change sent part of the traffic to a retired endpoint"),
    dict(opened="2026-06-18 07:30", frac=0.21, closed="2026-06-18 13:40", platforms=["ios", "android", "web"],
         first_call="late delivery", note="collector queue backlog after a broker restart"),
    dict(opened="2026-08-03 18:00", frac=0.32, closed="2026-08-04 02:30", platforms=["ios", "android"],
         first_call="duplicate delivery", note="SDK 9.4.1 batching regression"),
    dict(opened="2026-09-15 20:45", frac=0.29, closed="2026-09-15 22:20", platforms=["ios", "web"],
         first_call="consent loss", note="consent service timeouts; events held back"),
]
