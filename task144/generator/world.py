"""The world before any export is written: Grachtwerk's accounts, the shortlisted repositories, every star each
repository received (with the surface it came from), the spotlight lottery, organisation memberships, Sluis's sends
and the October nominations.

How a star comes to exist here: a repository is found from outside (a link forum, a blog, search, the explore page,
the command line) at a rate that decays from its launch; every first star is shown in the starrer's followers' home
feeds, where each follower who sees it stars from the card with a probability set by the repository (its rate per
view); the stars made from a feed card are shown to their own followers in turn. A spotlighted repository also gets
the newsletter readers' stars, about the same share of the list whatever the repository, and those readers' stars go
into their followers' feeds like any other."""
from __future__ import annotations

import datetime as dt
import hashlib
import heapq
import math
from dataclasses import dataclass, field

import numpy as np

import common as K

H = dt.timedelta(hours=1)

# Follower counts by the kind of account a star comes from: (mu, sigma, share with no followers). Lognormal
# floors, capped at 25,000.
FOLLOWERS = {"forum": (1.30, 1.10, 0.55), "regular": (1.55, 1.35, 0.15), "senior": (4.25, 1.20, 0.0),
             "reader": (3.65, 1.25, 0.0), "feed": (1.60, 1.30, 0.10), "member": (3.10, 1.10, 0.0)}
FCAP = 25000
NL_RATE = 0.00722            # newsletter stars on the spotlight per subscriber sent
NL_DELAY = [(0.40, 2.0), (0.30, 14.0), (0.20, 48.0), (0.10, 120.0)]      # (share, mean hours)
FEED_DELAY = [(0.55, 4.0), (0.35, 20.0), (0.10, 60.0)]
UNSTAR_P = 0.025
RESTAR_P = 0.25

# Diurnal weights by UTC hour (developers worldwide; Europe's afternoon and the Americas' morning are busiest).
DIURNAL = np.array([0.55, 0.48, 0.44, 0.42, 0.45, 0.55, 0.70, 0.86, 1.00, 1.08, 1.14, 1.20,
                    1.26, 1.34, 1.42, 1.44, 1.40, 1.33, 1.24, 1.13, 1.00, 0.86, 0.73, 0.62])
DIURNAL = DIURNAL / DIURNAL.mean()
WEEKEND = 0.62

LANGS = ["Go", "Rust", "TypeScript", "Python", "Kotlin", "C++", "Java", "Elixir", "Zig", "Ruby", "C#", "Swift"]
WORDS_A = ["amber", "anvil", "basalt", "beacon", "birch", "bramble", "cinder", "cobalt", "copper", "coral", "dune",
           "ember", "fable", "fern", "flint", "frost", "gale", "garnet", "granite", "harbor", "hazel", "heron",
           "indigo", "iris", "jasper", "juniper", "kestrel", "lark", "lumen", "maple", "marble", "mica", "moss",
           "nimbus", "onyx", "orchid", "otter", "pebble", "pine", "quartz", "raven", "reed", "rowan", "saffron",
           "sable", "slate", "sorrel", "spruce", "tansy", "thistle", "tidal", "umber", "vale", "willow", "wren",
           "yarrow", "zephyr", "alder", "briar", "cedar", "delta", "estuary", "fjord", "glacier", "isle", "lagoon"]
WORDS_B = ["db", "kit", "cli", "log", "queue", "mesh", "cache", "lint", "fmt", "proxy", "graph", "sync", "flow",
           "watch", "check", "forge", "stack", "trace", "parse", "pack", "shell", "board", "notes", "deck", "ui",
           "api", "auth", "store", "lens", "bench", "sched", "relay", "vault", "scope", "probe", "loom", "pipe"]
OWNER_A = ["north", "south", "east", "west", "blue", "red", "grey", "high", "low", "long", "open", "deep", "bright",
           "quiet", "swift", "iron", "stone", "river", "lake", "harbour", "polder", "dyke", "canal", "meadow"]
OWNER_B = ["labs", "works", "systems", "dev", "software", "collective", "studio", "hq", "io", "tech", "bytes", "code"]
SYL = ["an", "ba", "bo", "da", "de", "el", "fa", "ga", "ha", "ia", "jo", "ka", "ki", "la", "le", "li", "lo", "ma",
       "me", "mi", "mo", "na", "ne", "ni", "no", "pa", "pe", "ra", "re", "ri", "ro", "sa", "se", "si", "so", "ta",
       "te", "ti", "to", "va", "ve", "vi", "ya", "yo", "za", "zo", "ar", "en", "is", "on", "ul", "ek", "om", "ir"]
FIRST = ["anna", "ben", "chen", "daan", "eva", "femke", "gus", "hana", "ivan", "jan", "kai", "lena", "mats", "nina",
         "omar", "pia", "quinn", "ravi", "sara", "tom", "uma", "vera", "wout", "xin", "yusuf", "zoe", "lars", "maya",
         "noor", "pieter", "ruben", "sanne", "thijs", "yara", "bram", "lotte", "joris", "amir", "elif", "kenji",
         "lucia", "marco", "priyam", "sofia", "tariq", "wei", "aiko", "bruno", "dara", "emre", "fleur", "goran"]
LAST = ["devries", "jansen", "bakker", "visser", "smit", "meijer", "mulder", "bos", "vos", "peters", "hendriks",
        "dekker", "brouwer", "dijkstra", "koster", "prins", "huisman", "kuipers", "vermeulen", "postma", "garcia",
        "silva", "kowalski", "novak", "tanaka", "kim", "nguyen", "okafor", "haddad", "rossi", "muller", "larsen"]


def draw_followers(kind, n, g):
    mu, sg, p0 = FOLLOWERS[kind]
    f = np.floor(np.exp(g.normal(mu, sg, n))).astype(np.int64)
    if p0 > 0:
        f = np.where(g.random(n) < p0, 0, f)
    return np.minimum(f, FCAP)


@dataclass
class Account:
    id: int
    login: str
    kind: str
    created: dt.datetime
    followers: int
    following: int
    type: str = "user"
    email_key: str = ""
    merged_into: int | None = None


@dataclass
class Star:
    t: dt.datetime
    account: int
    surface: str          # v6 vocabulary: feed, newsletter, repo_page, search, explore, api
    first: bool = True    # a first star (False for a restar after an unstar)
    unstar_at: dt.datetime | None = None


@dataclass
class Repo:
    id: int
    name: str
    owner: str
    owner_type: str
    public: dt.datetime
    language: str
    description: str
    issue: tuple
    c: float              # the repository's rate per follower view of a starred card
    burst: float
    burst_kind: str
    burst_hour: float
    org: float
    decay: float
    mix: dict
    n_members: int
    drawn: bool = False
    shipped_events: bool = False
    stars: list = field(default_factory=list)
    horizon: dt.datetime | None = None

    @property
    def full(self):
        return "%s/%s" % (self.owner, self.name)


class Accounts:
    """Every account the pack can show, created when first needed. Ids rise with creation time, as the platform
    issues them; follower counts are a property of the account, as at the snapshot."""

    def __init__(self):
        self.by_id = {}
        self.pools = {}
        self.g = K.rng("accounts")
        self.logins = set()

    def _login(self, g):
        while True:
            r = g.random()
            if r < 0.42:
                s = "%s%s" % (FIRST[g.integers(len(FIRST))], LAST[g.integers(len(LAST))])
            elif r < 0.62:
                s = "%s-%s" % (FIRST[g.integers(len(FIRST))], LAST[g.integers(len(LAST))])
            elif r < 0.80:
                s = "".join(SYL[g.integers(len(SYL))] for _ in range(int(g.integers(2, 4))))
            else:
                s = "%s%s" % (FIRST[g.integers(len(FIRST))][0], LAST[g.integers(len(LAST))])
            if g.random() < 0.38:
                s += str(int(g.integers(1, 99)))
            if s not in self.logins:
                self.logins.add(s)
                return s

    def _new(self, kind, created, followers):
        g = self.g
        # ids are issued in creation order: about 9.4 million accounts by 2026, a few thousand new ones a day
        base = int((created - dt.datetime(2014, 3, 1)).total_seconds() / 86400.0 * 1730) + 1000003
        aid = base + int(g.integers(0, 1600))
        while aid in self.by_id:
            aid += 1 + int(g.integers(0, 40))
        following = int(max(0, np.floor(np.exp(g.normal(2.2, 1.2)))))
        a = Account(aid, self._login(g), kind, created, int(followers), following,
                    email_key=hashlib.sha256(("%s@%s" % (K.hexid("mailbox", aid, n=12), "mail.example")).encode()).hexdigest())
        self.by_id[aid] = a
        return a

    def pool(self, kind, size):
        if kind in self.pools:
            return self.pools[kind]
        g = K.rng("pool", kind)
        f = draw_followers(kind, size, g)
        out = []
        for i in range(size):
            if kind == "reader":
                created = dt.datetime(2014, 6, 1) + dt.timedelta(days=float(g.uniform(0, 4200)))
            elif kind == "senior":
                created = dt.datetime(2014, 3, 1) + dt.timedelta(days=float(g.uniform(0, 3300)))
            else:
                created = dt.datetime(2015, 1, 1) + dt.timedelta(days=float(g.uniform(0, 4200)))
            out.append(self._new(kind, created, f[i]).id)
        self.pools[kind] = out
        return out

    def fresh(self, kind, around, g):
        """A new account opened near a date (a link forum's newcomers sign up to star)."""
        created = around - dt.timedelta(hours=float(g.exponential(30.0)))
        if g.random() < 0.35:
            created = around - dt.timedelta(days=float(g.uniform(20, 2400)))
        return self._new(kind, created, draw_followers(kind, 1, g)[0]).id


POOL_SIZE = {"reader": 30000, "regular": 110000, "senior": 9000, "feed": 140000}


def mix_choice(mix, g, n):
    kinds = list(mix.keys())
    p = np.array([mix[k] for k in kinds], float)
    p = p / p.sum()
    idx = g.choice(len(kinds), size=n, p=p)
    return [kinds[i] for i in idx]


def surface_for(kind, g, burst=False):
    if burst:
        return "repo_page"
    r = g.random()
    if kind == "senior":
        return "explore" if r < 0.28 else ("search" if r < 0.52 else ("api" if r < 0.58 else "repo_page"))
    if kind == "forum":
        return "repo_page" if r < 0.92 else "search"
    return "search" if r < 0.27 else ("explore" if r < 0.42 else ("api" if r < 0.47 else "repo_page"))


def delay_hours(mixture, g):
    r = g.random()
    acc = 0.0
    for share, mean in mixture:
        acc += share
        if r < acc:
            return float(g.exponential(mean))
    return float(g.exponential(mixture[-1][1]))


class StarSim:
    """One repository's stars in time order: seeds, members, bots, the newsletter, and the feed cascade."""

    def __init__(self, repo, accounts, members, until, spotlight_at=None, list_size=0):
        self.r = repo
        self.A = accounts
        self.members = members
        self.until = until
        self.spot = spotlight_at
        self.list_size = list_size
        self.g = K.rng("stars", repo.id)
        self.seen = set()
        self.heap = []
        self.n = 0

    def push(self, t, kind, surface, account=None):
        if t > self.until:
            return
        self.n += 1
        heapq.heappush(self.heap, (t, self.n, kind, surface, account))

    def pick(self, kind):
        """An account of this kind that has not starred the repository yet."""
        g = self.g
        if kind in POOL_SIZE:
            pool = self.A.pool(kind, POOL_SIZE[kind])
            for _ in range(60):
                aid = pool[int(g.integers(len(pool)))]
                if aid not in self.seen:
                    return aid
        return self.A.fresh(kind if kind in FOLLOWERS else "regular", self.t_now, g)

    def run(self):
        r, g = self.r, self.g
        hours = int((self.until - r.public).total_seconds() // 3600) + 1
        # seeds from outside: the launch burst and the organic decay, hour by hour
        for hh in range(hours):
            t0 = r.public + hh * H
            how = t0.hour
            wk = WEEKEND if t0.weekday() >= 5 else 1.0
            day = hh / 24.0
            lam_o = r.org / 24.0 * (day + 2.0) ** (-r.decay) * DIURNAL[how] * wk
            lam_b = 0.0
            if r.burst > 0 and hh >= r.burst_hour:
                tau = 31.0
                lam_b = r.burst / tau * math.exp(-(hh - r.burst_hour) / tau) * (0.55 + 0.45 * DIURNAL[how])
            nb, no = g.poisson(lam_b), g.poisson(lam_o)
            for _ in range(nb):
                self.push(t0 + dt.timedelta(seconds=float(g.uniform(0, 3600))), r.burst_kind, "repo_page")
            if no:
                for kind in mix_choice(r.mix, g, no):
                    self.push(t0 + dt.timedelta(seconds=float(g.uniform(0, 3600))), kind, surface_for(kind, g))
        # the owning organisation's members, mostly in the first days
        for aid in self.members:
            t = r.public + dt.timedelta(hours=float(g.exponential(30.0)))
            self.push(t, "member", "repo_page" if g.random() < 0.7 else "feed", aid)
        # an occasional crawler bot
        for _ in range(int(g.poisson(0.7))):
            t = r.public + dt.timedelta(hours=float(g.uniform(1, max(2, hours - 1))))
            self.push(t, "bot", "api")
        # the newsletter readers' stars on a spotlighted repository
        if self.spot is not None:
            n = int(g.poisson(NL_RATE * self.list_size * float(np.exp(g.normal(0, 0.02)))))
            for _ in range(n):
                self.push(self.spot + dt.timedelta(hours=delay_hours(NL_DELAY, g)), "reader", "newsletter")
        # process in time order, every first star spawning its feed stars
        out = []
        while self.heap:
            t, _, kind, surface, account = heapq.heappop(self.heap)
            self.t_now = t
            if account is None:
                if kind == "bot":
                    a = self.A._new("regular", t - dt.timedelta(days=float(g.uniform(30, 900))), 0)
                    a.type = "bot"
                    a.login = "%s-bot" % a.login.split("-")[0][:10]
                    account = a.id
                else:
                    account = self.pick(kind)
            if account in self.seen:
                continue
            self.seen.add(account)
            s = Star(t, account, surface)
            out.append(s)
            f = self.A.by_id[account].followers
            k = int(g.poisson(r.c * f)) if f > 0 else 0
            for _ in range(k):
                self.push(t + dt.timedelta(hours=delay_hours(FEED_DELAY, g)), "feed", "feed")
            if g.random() < UNSTAR_P:
                s.unstar_at = t + dt.timedelta(hours=float(g.exponential(6 * 24.0)))
        # restars after an unstar (not first stars)
        extra = []
        for s in out:
            if s.unstar_at is not None and g.random() < RESTAR_P:
                extra.append(Star(s.unstar_at + dt.timedelta(hours=float(g.exponential(10 * 24.0))), s.account,
                                  s.surface if s.surface != "newsletter" else "repo_page", first=False))
        out.extend(extra)
        out.sort(key=lambda s: (s.t, s.account))
        return out


# ---------------------------------------------------------------------------------------------------- repositories
# The October candidates' parameters (rate per view c; launch burst and its audience; organic seeds per day at
# launch and their decay; the organic audience; members of the owning organisation).
OCT_PARAMS = {
    "tracewire": dict(c=0.0010, burst=1200, burst_kind="senior", burst_hour=5, org=295, decay=0.55,
                      mix={"senior": 0.8, "regular": 0.2}, n_members=11),
    "slidewell": dict(c=0.0181, burst=2000, burst_kind="forum", burst_hour=14, org=60, decay=0.55,
                      mix={"forum": 0.85, "regular": 0.15}, n_members=0),
    "shiftgres": dict(c=0.0037, burst=0, burst_kind="regular", burst_hour=0, org=290, decay=0.55,
                      mix={"regular": 0.9, "senior": 0.1}, n_members=7),
    "kilnkit": dict(c=0.0062, burst=200, burst_kind="senior", burst_hour=3, org=82, decay=0.55,
                    mix={"senior": 0.55, "regular": 0.45}, n_members=9),
    "hullcheck": dict(c=0.0030, burst=900, burst_kind="regular", burst_hour=8, org=155, decay=0.55,
                      mix={"regular": 0.7, "senior": 0.3}, n_members=5),
    "timeloom": dict(c=0.0022, burst=500, burst_kind="forum", burst_hour=11, org=122, decay=0.55,
                     mix={"regular": 0.6, "forum": 0.4}, n_members=0),
    "ferrolog": dict(c=0.0045, burst=500, burst_kind="regular", burst_hour=4, org=205, decay=0.55,
                     mix={"regular": 0.85, "senior": 0.15}, n_members=14),
}
MIXES = [{"regular": 0.8, "senior": 0.2}, {"regular": 0.5, "senior": 0.5}, {"forum": 0.6, "regular": 0.4},
         {"regular": 0.95, "senior": 0.05}, {"senior": 0.7, "regular": 0.3}, {"forum": 0.85, "regular": 0.15}]
# The twin pair: two spotlighted repositories of consecutive issues alike on age, pre-issue stars, pace and feed share,
# about ten-fold apart on the rate per view (one's starrers well followed, the other's not).
TWINS = {(2026, 3): dict(c=0.0015, burst=850, burst_kind="senior", burst_hour=6, org=91, decay=0.55,
                         mix={"senior": 0.85, "regular": 0.15}, n_members=6),
         (2026, 4): dict(c=0.0150, burst=700, burst_kind="regular", burst_hour=6, org=95, decay=0.55,
                         mix={"regular": 0.95, "senior": 0.05}, n_members=6)}
TWIN_AGE = {(2026, 3): 38.6, (2026, 4): 38.4}     # days public at the issue's send


def _repo_name(g, used):
    while True:
        n = "%s%s" % (WORDS_A[g.integers(len(WORDS_A))], WORDS_B[g.integers(len(WORDS_B))])
        if g.random() < 0.3:
            n = "%s-%s" % (WORDS_A[g.integers(len(WORDS_A))], WORDS_B[g.integers(len(WORDS_B))])
        if n not in used and n not in K.OCT_NAMES:
            used.add(n)
            return n


def _owner(g, user):
    if user:
        return "%s%s" % (FIRST[g.integers(len(FIRST))], LAST[g.integers(len(LAST))][:int(g.integers(3, 9))])
    return "%s%s" % (OWNER_A[g.integers(len(OWNER_A))], ("-" if g.random() < 0.5 else "") + OWNER_B[g.integers(len(OWNER_B))])


def lottery_repos():
    g = K.rng("lottery-repos")
    used = set()
    out = []
    rid = 418_200_311
    for (y, m) in K.LOTTERY_MONTHS:
        send = K.ISSUE_SEND[(y, m)]
        drawn = int(K.rng("draw", y, m).integers(7))
        for j in range(7):
            rid += int(g.integers(9_000, 260_000))
            user = g.random() < 0.3
            public = send - dt.timedelta(days=float(g.uniform(29, 44)), hours=float(g.uniform(0, 24)))
            public = public.replace(microsecond=0)
            p = dict(c=float(min(0.016, max(0.0006, np.exp(g.normal(math.log(0.0042), 0.75))))),
                     burst=float(g.choice([0, 300, 900, 1800, 2600])),
                     burst_kind=str(g.choice(["forum", "regular", "senior"], p=[0.5, 0.35, 0.15])),
                     burst_hour=float(g.uniform(2, 20)), org=float(np.exp(g.normal(math.log(85), 0.5))),
                     decay=0.55, mix=MIXES[int(g.integers(len(MIXES)))],
                     n_members=0 if user else int(g.integers(3, 18)))
            if j == drawn and (y, m) in TWINS:
                p = dict(TWINS[(y, m)])
                public = (send - dt.timedelta(days=TWIN_AGE[(y, m)])).replace(microsecond=0)
            name = _repo_name(g, used)
            out.append(Repo(rid, name, _owner(g, user), "user" if user else "organization", public,
                            LANGS[int(g.integers(len(LANGS)))], "", (y, m), drawn=(j == drawn), **p))
    # owners are distinct accounts: a repeated draw takes another name from a hash (the stream above is untouched)
    taken = {o for _, o, *_ in K.OCT_SHORTLIST}
    for r in out:
        k = 0
        while r.owner in taken:
            k += 1
            h = int(K.hexid("owner", r.id, k, n=8), 16)
            if r.owner_type == "user":
                r.owner = "%s%s%d" % (FIRST[h % len(FIRST)], LAST[(h // 97) % len(LAST)][:3 + h % 5], 1 + h % 89)
            else:
                r.owner = "%s%s%s" % (OWNER_A[h % len(OWNER_A)], "-" if h % 2 else "", OWNER_B[(h // 31) % len(OWNER_B)])
        taken.add(r.owner)
        r.description = describe(r)
    return out


DESC = {
    "db": ["An embedded key-value store", "A small document database you can ship inside your app",
           "Typed queries for SQLite"],
    "kit": ["Building blocks for command-line tools", "A starter kit for small web services", "Helpers for testing HTTP handlers"],
    "cli": ["A command-line client for the Grachtwerk API", "Run scripts from a single YAML file", "A friendlier ls"],
    "log": ["Structured logs with zero allocations", "Tail and filter JSON logs in the terminal", "Log shipping without an agent"],
    "queue": ["A job queue on top of Postgres", "Durable background jobs with retries", "A tiny message queue for one machine"],
    "mesh": ["Service discovery for small clusters", "Peer-to-peer networking for local apps", "mTLS between services, simply"],
    "cache": ["An in-process cache with expiry", "HTTP caching middleware", "A read-through cache for slow APIs"],
    "lint": ["Lint your SQL migrations", "A linter for Dockerfiles", "Catch broken links in Markdown"],
    "fmt": ["A formatter for TOML", "Opinionated formatting for SQL", "Pretty-print diffs in the terminal"],
    "proxy": ["A local HTTPS proxy for development", "Record and replay HTTP traffic", "A reverse proxy in one binary"],
    "graph": ["Graph algorithms with a plain API", "Draw dependency graphs from your lockfile", "A property graph in memory"],
    "sync": ["Sync dotfiles between machines", "Two-way folder sync over SSH", "Offline-first sync for web apps"],
    "flow": ["Small workflows as code", "A state machine library", "Visual pipelines for data jobs"],
    "watch": ["Rerun commands when files change", "Uptime checks from the command line", "Watch Kubernetes events in the terminal"],
    "check": ["Health checks for your services", "Validate config files against a schema", "Check licenses of your dependencies"],
    "forge": ["Generate project scaffolds from templates", "A build tool for monorepos", "Self-hosted package registry"],
    "stack": ["A local dev stack in one file", "Infrastructure templates for small teams", "Run your stack on one VM"],
    "trace": ["Lightweight tracing for async code", "Trace syscalls without root", "Flame graphs from production"],
    "parse": ["A fast CSV parser", "Parser combinators without the magic", "Parse dates in any format"],
    "pack": ["Bundle a static site into one file", "Package Python apps as single binaries", "Asset packing for games"],
    "shell": ["A shell prompt that stays out of the way", "Scripting with types", "A shell history you can search"],
    "board": ["A kanban board in the terminal", "Self-hosted status page", "A whiteboard for remote teams"],
    "notes": ["Plain-text notes with backlinks", "Meeting notes from your calendar", "Notes that live in your git repo"],
    "deck": ["Slides from Markdown", "A pitch deck template", "Present code walkthroughs"],
    "ui": ["Headless UI components", "A design system for internal tools", "Terminal UI widgets"],
    "api": ["Mock any REST API from an OpenAPI file", "A typed client generator", "Rate limiting for APIs"],
    "auth": ["Passkeys for small apps", "Session management without a database", "OAuth for command-line tools"],
    "store": ["Object storage you can run anywhere", "A content-addressed blob store", "State management for small apps"],
    "lens": ["Inspect Postgres queries as they run", "See inside your container images", "Browse Parquet files in the terminal"],
    "bench": ["Benchmarks that run in CI", "Load testing from a single script", "Compare benchmark runs over time"],
    "sched": ["Cron with retries and logs", "A scheduler for one-off jobs", "Calendar scheduling for teams"],
    "relay": ["Webhooks relayed to localhost", "A relay for server-sent events", "Forward logs to many sinks"],
    "vault": ["Secrets in your repo, encrypted", "A password manager for teams", "Rotate API keys automatically"],
    "scope": ["Profile memory in production", "Scope permissions for CI tokens", "An oscilloscope for audio signals"],
    "probe": ["Synthetic probes for your endpoints", "Inspect TLS certificates", "eBPF probes made simple"],
    "loom": ["Weave config from many sources", "Structured concurrency helpers", "Thread visualisation for async runtimes"],
    "pipe": ["Unix pipes for JSON", "Stream processing in a few lines", "Pipelines for data cleaning"],
}


def describe(r):
    for suffix in sorted(DESC, key=len, reverse=True):
        if r.name.endswith(suffix):
            opts = DESC[suffix]
            return opts[int(K.hexid("desc", r.id, n=8), 16) % len(opts)]
    return "Tools for %s developers" % r.language


def october_repos():
    out = []
    rid = 627_403_118
    g = K.rng("oct-ids")
    for name, owner, otype, public, lang, desc in K.OCT_SHORTLIST:
        rid += int(g.integers(40_000, 900_000))
        out.append(Repo(rid, name, owner, otype, public, lang, desc, K.OCT, **OCT_PARAMS[name]))
    return out


# ---------------------------------------------------------------------------------------------------- the world
class World:
    pass


def list_size(ym):
    """Sluis subscribers sent to: about 248,000 in January 2025, growing to about 434,000 by September 2026."""
    i = K.LOTTERY_MONTHS.index(ym) if ym in K.LOTTERY_MONTHS else len(K.LOTTERY_MONTHS)
    g = K.rng("list", *ym)
    base = 247_900 + 11_200 * i - 95 * i * i if i < 18 else 433_100 + 260 * (i - 18)
    return int(base + g.integers(-900, 900))


def simulate():
    W = World()
    A = Accounts()
    W.accounts = A
    W.lottery = lottery_repos()
    W.october = october_repos()
    W.repos = W.lottery + W.october
    W.by_name = {r.name: r for r in W.repos}
    W.list = {ym: list_size(ym) for ym in K.LOTTERY_MONTHS}
    W.list[K.OCT] = 433_812
    # the owners' own accounts (organisations and individual developers)
    W.owner_account = {}
    for r in W.repos:
        go = K.rng("owner-account", r.owner)
        created = r.public - dt.timedelta(days=float(go.uniform(300, 3600)))
        a = A._new("senior" if r.owner_type == "organization" else "regular", created,
                   draw_followers("senior" if r.owner_type == "organization" else "regular", 1, go)[0])
        a.login = r.owner
        a.type = r.owner_type
        W.owner_account[r.owner] = a.id
    # members of the owning organisations: the members who star at launch, the earliest of them the owner, and a few
    # former members who left well before the repository went public
    W.members = {}
    W.member_spans = []
    W.member_rows = []
    mpool = A.pool("senior", POOL_SIZE["senior"])
    for r in W.repos:
        gm = K.rng("members", r.id)
        ids = []
        for _ in range(r.n_members):
            a = A._new("member", r.public - dt.timedelta(days=float(gm.uniform(200, 2600))),
                       draw_followers("member", 1, gm)[0])
            ids.append(a.id)
            joined = r.public - dt.timedelta(days=float(gm.uniform(5, 700)), hours=float(gm.uniform(0, 23)))
            W.member_spans.append((r.owner, a.id, joined.replace(microsecond=0), None))
        W.members[r.id] = ids
        if r.owner_type != "organization":
            continue
        spans = [s for s in W.member_spans if s[0] == r.owner]
        first = min(spans, key=lambda s: s[2])[1] if spans else None
        for org, aid, joined, left in spans:
            W.member_rows.append((org, aid, joined, left, "owner" if aid == first else "member"))
        gf = K.rng("former", r.id)
        for _ in range(int(gf.integers(0, 3))):
            a = A._new("member", r.public - dt.timedelta(days=float(gf.uniform(900, 3000))),
                       draw_followers("member", 1, gf)[0])
            joined = r.public - dt.timedelta(days=float(gf.uniform(800, 1500)))
            left = joined + dt.timedelta(days=float(gf.uniform(60, 700)))
            W.member_rows.append((r.owner, a.id, joined.replace(microsecond=0), left.replace(microsecond=0), "member"))
    # every repository's stars: event level for the spotlighted lottery repositories and the October shortlist, the
    # runners-up simulated the same way for the warehouse rollup only
    for r in W.repos:
        if r.issue == K.OCT:
            until = K.CUT
        else:
            until = min(r.public + dt.timedelta(days=100), K.CUT)
        r.horizon = until
        spot = K.ISSUE_SEND[r.issue] if (r.drawn and r.issue != K.OCT) else None
        sim = StarSim(r, A, W.members[r.id], until, spotlight_at=spot, list_size=W.list.get(r.issue, 0))
        r.stars = sim.run()
        r.shipped_events = r.drawn or r.issue == K.OCT
    gx = K.rng("merged")
    oct_ids = {s.account for r in W.october for s in r.stars}
    feedish = {s.account for r in W.repos for s in r.stars if s.surface in ("feed", "newsletter")}
    cands = sorted({s.account for r in W.lottery if r.drawn for s in r.stars
                    if s.first and s.surface in ("search", "repo_page") and A.by_id[s.account].kind == "regular"}
                   - oct_ids - feedish)
    for i in gx.choice(len(cands), size=46, replace=False):
        a = A.by_id[cands[int(i)]]
        b = A._new("regular", min(a.created + dt.timedelta(days=float(gx.uniform(200, 2000))),
                                  dt.datetime(2026, 8, 30) - dt.timedelta(days=float(gx.uniform(0, 300)))), a.followers)
        a.merged_into = b.id
        a.followers = 0
    return W


if __name__ == "__main__":
    import time
    t = time.time()
    W = simulate()
    print("simulated %d repositories, %d accounts in %.1fs" % (len(W.repos), len(W.accounts.by_id), time.time() - t))
    for r in W.october:
        s = [x for x in r.stars if x.first]
        print(r.name, len(s), sum(1 for x in s if x.surface == "feed"))
