"""Names on Grachtwerk the way a code host's population has them: personal handles built from a person's name
(initials, fragments, the odd digit or underscore), organisations named after a project or a company, repositories
named for what they do with a minority of brandable names, and renames with a reason. Every generator takes its own
random stream, so a name never moves a star."""
from __future__ import annotations

FIRST = ["anna", "bram", "chen", "daan", "eva", "femke", "gus", "hana", "ivan", "jan", "kai", "lena", "mats", "nina",
         "omar", "pia", "quinn", "ravi", "sara", "tom", "uma", "vera", "wout", "xin", "yusuf", "zoe", "lars", "maya",
         "noor", "pieter", "ruben", "sanne", "thijs", "yara", "lotte", "joris", "amir", "elif", "kenji", "lucia", "marco",
         "sofia", "tariq", "wei", "aiko", "bruno", "dara", "emre", "fleur", "goran", "hugo", "ilse", "jesse", "koen",
         "lieke", "milan", "niels", "olga", "priya", "rosa", "sem", "tess", "vince", "wiebe", "anouk", "bas", "carmen",
         "dirk", "esther", "finn", "gijs", "hidde", "isa", "jop", "kim", "luuk", "merel", "nadia", "otto", "pablo",
         "renske", "siem", "teun", "valentina", "willem", "zayn", "ahmed", "bilal", "camila", "diego", "fatima",
         "jonas", "leon", "mila", "nora", "oscar", "paula", "rahul", "sven", "timo", "yuki", "aditi", "bjorn"]
LAST = ["devries", "jansen", "bakker", "visser", "smit", "meijer", "mulder", "bos", "vos", "peters", "hendriks",
        "dekker", "brouwer", "dijkstra", "koster", "prins", "huisman", "kuipers", "vermeulen", "postma", "garcia",
        "silva", "kowalski", "novak", "tanaka", "kim", "nguyen", "okafor", "haddad", "rossi", "muller", "larsen",
        "schouten", "willems", "hoekstra", "veenstra", "kok", "jacobs", "vink", "boer", "maas", "verhoeven",
        "lindqvist", "moreau", "ferreira", "costa", "schmidt", "weber", "fischer", "yilmaz", "demir", "sato",
        "suzuki", "patel", "shah", "ali", "khan", "ozturk", "wojcik", "horvat", "popescu", "ivanova", "eriksen",
        "nieminen", "oconnor", "murphy", "walsh", "byrne", "dubois", "lambert", "romero", "navarro"]
DUTCH_PARTICLE = [("van der ", "vd"), ("van den ", "vd"), ("van ", "v"), ("de ", "d"), ("van de ", "vd")]
DUTCH_LAST = ["berg", "linden", "meer", "heuvel", "broek", "wal", "veen", "beek", "dam", "graaf", "jong", "boer",
              "wit", "groot", "laan", "hoek", "leeuwen", "vliet", "zande", "kamp"]


def handle(g):
    """A personal login: name fragments, initials, the odd digit or underscore."""
    f = FIRST[int(g.integers(len(FIRST)))]
    u = g.random()
    if u < 0.16:
        p, short = DUTCH_PARTICLE[int(g.integers(len(DUTCH_PARTICLE)))]
        last = DUTCH_LAST[int(g.integers(len(DUTCH_LAST)))]
        h = f[0] + ("" if g.random() < 0.5 else FIRST[int(g.integers(len(FIRST)))][0]) + short + last
    else:
        last = LAST[int(g.integers(len(LAST)))]
        v = g.random()
        if v < 0.24:
            h = f + last
        elif v < 0.42:
            h = f[0] + last
        elif v < 0.56:
            h = "%s-%s" % (f, last)
        elif v < 0.66:
            h = f + last[0]
        elif v < 0.74:
            h = "%s_%s" % (f, last[:int(g.integers(3, len(last) + 1))])
        elif v < 0.84:
            h = f + last[:int(g.integers(2, 5))]
        elif v < 0.92:
            h = f + ("dev" if g.random() < 0.5 else "codes")
        else:
            h = last + f[0]
    if g.random() < 0.27:
        h += str(int(g.integers(1, 100))) if g.random() < 0.7 else str(int(g.integers(1979, 2004)))
    return h


ORG_ROOT_A = ["bel", "cor", "dal", "ev", "fen", "gar", "hol", "is", "jor", "kel", "lum", "mar", "nor", "ost", "pel",
              "quin", "ros", "sel", "tor", "ul", "ver", "wil", "yar", "zan", "ar", "bri", "cal", "dun", "el", "fal"]
ORG_ROOT_B = ["vik", "tex", "ora", "ion", "bit", "dex", "ent", "ica", "ly", "ris", "nova", "ware", "ford", "mont",
              "stad", "berg", "wick", "dale", "gate", "lane"]
ORG_TAIL = ["", "", "", "-software", "-systems", "hq", "-dev", "-oss", "-tech", "-data", "-studio", "-cloud"]
TOPIC = ["dataplane", "logship", "pgtools", "tracekit", "queuebird", "routekit", "formkit", "edgecache", "pipewerk",
         "statusboard", "keyring", "schemaforge", "vaultline", "taskbay", "docsmith", "chartmill", "testgrid",
         "buildhive", "patchbay", "sitekit"]


def org(g):
    """An organisation: a company with a coined name, or the home of a project."""
    u = g.random()
    if u < 0.55:
        root = ORG_ROOT_A[int(g.integers(len(ORG_ROOT_A)))] + ORG_ROOT_B[int(g.integers(len(ORG_ROOT_B)))]
        return root + ORG_TAIL[int(g.integers(len(ORG_TAIL)))]
    if u < 0.85:
        t = TOPIC[int(g.integers(len(TOPIC)))]
        return t + ["", "-project", "-dev", "hq", "-org"][int(g.integers(5))]
    city = ["utrecht", "leiden", "zwolle", "gent", "aarhus", "tartu", "porto", "brno", "graz", "lyon", "tampere",
            "bergen", "malmo", "lille", "turin"][int(g.integers(15))]
    return "%s-%s" % (city, ["software", "devs", "makers", "opensource", "coders"][int(g.integers(5))])


TECH_KINDS = {
    "exporter": ["nginx", "postgres", "redis", "kafka", "nats", "rabbitmq", "clickhouse", "etcd", "minio", "systemd",
                 "zfs", "caddy", "haproxy", "unbound"],
    "backup": ["postgres", "mysql", "sqlite", "redis", "etcd", "clickhouse", "zfs", "mongo"],
    "operator": ["postgres", "mysql", "redis", "kafka", "nats", "rabbitmq", "clickhouse", "etcd", "minio"],
    "cli": ["nats", "redis", "s3", "minio", "kafka", "etcd", "grpc", "consul", "loki"],
}
TECH_NAME = {"nginx": "nginx", "postgres": "Postgres", "redis": "Redis", "kafka": "Kafka", "nats": "NATS",
             "rabbitmq": "RabbitMQ", "clickhouse": "ClickHouse", "etcd": "etcd", "minio": "MinIO", "systemd": "systemd",
             "zfs": "ZFS", "caddy": "Caddy", "haproxy": "HAProxy", "unbound": "Unbound", "mysql": "MySQL",
             "sqlite": "SQLite", "mongo": "MongoDB", "s3": "S3", "grpc": "gRPC", "consul": "Consul", "loki": "Loki"}
LANG_PREFIX = {"go": "Go", "rust": "Rust", "py": "Python", "node": "TypeScript", "kt": "Kotlin", "zig": "Zig",
               "ex": "Elixir", "rb": "Ruby"}
UTIL = [("retry", "retry with backoff"), ("ratelimit", "rate limiting"), ("semver", "semantic version parsing"),
        ("dotenv", ".env file loading"), ("cron", "cron expression parsing"), ("csv", "streaming CSV reading"),
        ("toml", "TOML parsing"), ("diff", "text diffs"), ("uuid", "UUID v7 generation"), ("jwt", "JWT signing"),
        ("pool", "connection pooling"), ("mock", "HTTP mocking in tests"), ("fixtures", "test fixtures"),
        ("cache", "in-process caching"), ("flags", "feature flags"), ("slug", "URL slugs"), ("money", "money amounts"),
        ("geo", "geodesic distances"), ("i18n", "translations"), ("sse", "server-sent events")]
FMT_NAME = {"csv": "CSV", "parquet": "Parquet", "json": "JSON", "md": "Markdown", "pdf": "PDF", "html": "HTML",
            "yaml": "YAML", "xlsx": "Excel", "ics": "iCalendar", "gpx": "GPX", "geojson": "GeoJSON", "toml": "TOML",
            "sqlite": "SQLite", "srt": "SRT", "vtt": "WebVTT"}
FMT_PAIRS = [("csv", "parquet"), ("json", "csv"), ("md", "pdf"), ("md", "html"), ("yaml", "json"), ("xlsx", "csv"),
             ("html", "pdf"), ("ics", "csv"), ("gpx", "geojson"), ("toml", "yaml"), ("csv", "sqlite"), ("srt", "vtt")]
NOUN = [("cost", "cost"), ("quota", "quota"), ("image", "image"), ("secret", "secret"), ("pvc", "volume claim"),
        ("ingress", "ingress"), ("cert", "certificate")]
NVIM = [("diagnostics", "Show diagnostics in a floating list"), ("git-blame", "Inline git blame for the current line"),
        ("quickfix-list", "A quickfix list you can filter and edit"), ("test-runner", "Run the nearest test from the editor"),
        ("markdown-preview", "Live Markdown preview in the browser"), ("sql-console", "Run SQL against a database "
        "from a buffer"), ("http-client", "Send HTTP requests from a scratch buffer"), ("color-picker", "Pick and "
        "convert colours in place"), ("spell-check", "Spell checking for code comments"), ("outline", "A symbols "
        "outline in a side window")]
STEPS = [("cache-restore", "Restore and save build caches between Pipelines runs"),
         ("release-notes", "Draft release notes from merged changes"), ("sbom", "Generate an SBOM for each build"),
         ("deploy-preview", "Deploy a preview environment for each change"),
         ("lint-report", "Post lint results as review comments"), ("image-scan", "Scan container images before push"),
         ("changelog", "Keep a changelog from commit messages"), ("semver-tag", "Tag releases from commit messages"),
         ("coverage-badge", "Publish a coverage badge from test results"),
         ("matrix-split", "Split a test suite across parallel jobs")]
AWESOME = [("selfhosting", "self-hosting"), ("rust-cli", "Rust command-line tools"), ("postgres", "Postgres"),
           ("observability", "observability"), ("accessibility", "web accessibility"),
           ("dutch-open-data", "Dutch open data"), ("static-sites", "static site"), ("home-automation", "home automation"),
           ("data-engineering", "data engineering"), ("terminal-tools", "terminal tool")]
SERVICES = {"grachtwerk": "Grachtwerk", "fietsbox": "Fietsbox", "kademail": "Kademail", "polderdns": "PolderDNS",
            "sluisstore": "Sluisstore", "dijkpay": "DijkPay", "havencdn": "HavenCDN", "brugsms": "BrugSMS"}
WORD = ["skiff", "plume", "tandem", "quokka", "lumen", "brisk", "kettle", "pylon", "sorbet", "marmot", "cobble",
        "tinsel", "ripple", "bobbin", "trellis", "muffin", "lantern", "pinwheel", "sprocket", "gondola", "otter",
        "caravel", "tumble", "nugget", "walrus", "puffin", "zipline", "hopscotch", "jigsaw", "pemmican"]
COIN_A = ["zor", "kel", "nuv", "fer", "vim", "qua", "dax", "lio", "bry", "tav", "mox", "pex", "rin", "sol", "zen",
          "hal", "jun", "kiv", "obe", "ury", "brak", "cly", "drom", "esk", "fyn", "gho", "hux", "ilm", "jex", "kro",
          "lyt", "mur", "nim", "orv", "plo", "quil", "rask", "sty", "tro", "vex"]
COIN_B = ["o", "ix", "a", "en", "ly", "um", "is", "ra", "et", "ik", "an", "e", "io", "us", "ar", "el"]
BRAND_DESC = ["A small static site generator", "Fast fuzzy finder for the terminal", "Self-hosted bookmarks with "
              "full-text search", "A note-taking app that stores plain Markdown", "Lightweight job runner for small "
              "teams", "A tiny web framework with typed routes", "Local-first sync for small apps", "A terminal "
              "dashboard for your services", "Feature flags you can host yourself", "Typed config loading with good "
              "error messages", "Screenshots of web pages from the command line", "Keyboard-driven window manager",
              "A friendlier replacement for find", "A minimal reverse proxy with automatic certificates",
              "Offline-first issue tracker", "Load testing from a single script", "A pastebin you can run on a "
              "Raspberry Pi", "Diagrams from plain text", "A tiny embedded key-value store", "Read-it-later service "
              "with a terminal client", "Tail many log files in one view", "A spreadsheet in your terminal",
              "Snapshot testing for command-line output", "A Git client for people who live in the terminal",
              "Generate fake data from a schema", "A calendar that syncs over plain files", "Watch a folder and "
              "rerun a command", "A queue on top of SQLite", "Encrypted secrets in your repository", "An uptime monitor "
              "with a status page", "Find and remove duplicate photos", "Run SQL over CSV files", "An HTTP client "
              "with a request history", "Translate commit messages into release notes", "A tiny RSS reader",
              "Measure how long your builds take", "Cron with logs and retries", "A launcher for scripts you keep "
              "forgetting", "Back up your dotfiles to any git host", "A minimal password manager for teams"]


def repo(g, personal=True, used_desc=None):
    """A repository's name, description and main language; personal=False leaves out the personal kinds (dotfiles,
    a blog, a home lab), which no newsletter shortlists; used_desc keeps brandable descriptions from repeating."""
    u = g.random() * (1.0 if personal else 0.94)
    pick = lambda xs: xs[int(g.integers(len(xs)))]
    if u < 0.24:
        if g.random() < 0.5:
            name = pick(WORD)
        else:
            name = pick(COIN_A) + pick(COIN_B)
        desc = pick(BRAND_DESC)
        if used_desc is not None:
            free = [d for d in BRAND_DESC if d not in used_desc]
            desc = free[int(g.integers(len(free)))] if free else desc
            used_desc.add(desc)
        return name, desc, pick(["Go", "Rust", "TypeScript", "Python", "Zig", "Elixir"])
    if u < 0.40:
        p = pick(list(LANG_PREFIX))
        util, what = pick(UTIL)
        return "%s-%s" % (p, util), "%s for %s" % (what[0].upper() + what[1:], LANG_PREFIX[p]), LANG_PREFIX[p]
    if u < 0.50:
        kind = pick(list(TECH_KINDS))
        t = pick(TECH_KINDS[kind])
        tn = TECH_NAME[t]
        desc = {"exporter": "Expose %s metrics for scraping" % tn, "backup": "Scheduled %s backups to object storage" % tn,
                "operator": "Run %s on Kubernetes with an operator" % tn,
                "cli": "A command-line client for %s" % tn}[kind]
        return "%s-%s" % (t, kind), desc, pick(["Go", "Rust", "Go", "Python"])
    if u < 0.60:
        a, b = pick(FMT_PAIRS)
        return "%s-to-%s" % (a, b), "Convert %s files to %s" % (FMT_NAME[a], FMT_NAME[b]), pick(["Python", "Go", "Rust"])
    if u < 0.67:
        n, what = pick(NOUN)
        return "k8s-%s-report" % n, "Kubernetes %s report per namespace" % what, pick(["Go", "Python"])
    if u < 0.73:
        x, what = pick(NVIM)
        return "%s.nvim" % x, what, "Lua"
    if u < 0.79:
        x, what = pick(STEPS)
        return "%s-step" % x, what, pick(["TypeScript", "Go"])
    if u < 0.84:
        t, what = pick(AWESOME)
        return "awesome-%s" % t, "A curated list of %s resources" % what, None
    if u < 0.89:
        svc = pick(list(SERVICES))
        return "terraform-provider-%s" % svc, "Terraform provider for %s" % SERVICES[svc], "Go"
    if u < 0.94:
        x, what = pick([("pdf-table-extract", "Pull tables out of PDFs into CSV"),
                        ("invoice-parser", "Read totals and dates from invoice PDFs"),
                        ("receipt-ocr", "Turn photos of receipts into rows"),
                        ("gpx-stats", "Distance, climb and pace from GPX tracks"),
                        ("ical-merge", "Merge several calendars into one feed"),
                        ("rss-digest", "A daily email digest of your feeds"),
                        ("budget-cli", "Track a household budget from the terminal"),
                        ("recipe-scaler", "Scale recipes and convert units"),
                        ("habit-tracker", "A habit tracker that lives in a git repo"),
                        ("bike-route-planner", "Plan bike routes from open map data")])
        return x, what, pick(["Python", "Go", "TypeScript", "Rust"])
    x, what = pick([("dotfiles", "zsh, tmux and neovim configuration"), ("homelab", "Configuration for a home lab"),
                    ("nixos-config", "NixOS configuration for my machines"), ("blog", "Source of my blog"),
                    ("talks", "Slides and code from my talks"), ("scripts", "Small scripts I use every day")])
    return x, what, pick(["Shell", "Nix", "Shell", "TypeScript"])


RENAMES = [
    # (old name, new name, owner move): a clearer name, a dropped prefix, a move into the project's organisation,
    # a clash with an existing package, a typo
    ("pgbk", "pg-backup", None), ("tfp-grachtwerk", "terraform-provider-grachtwerk", None),
    ("go-structlog", "structlog", None), ("py-pdftables", "pdftables", None), ("kubernets-cost", "kubernetes-cost", None),
    ("routekit", "routekit", "org"), ("schemaforge", "schemaforge", "org"), ("metrix", "metrix-db", None),
    ("mdslides", "md-slides", None), ("notify", "notify-rs", None), ("dashy-lite", "statusboard", None),
    ("my-nvim-config", "dotfiles", None), ("csv2parquet", "csv-to-parquet", None),
]
