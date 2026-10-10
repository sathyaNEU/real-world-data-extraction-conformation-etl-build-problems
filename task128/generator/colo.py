"""The two colocated estates at Centro de Datos Guadalhorce: hosts, the el9 advisories, the window
calendar and hourly forecast, the change requests of May to October and the provider's outcomes,
and the managed-host findings feed at 23 October.

The provider returns every host it drains on the estate's current platform build. Nothing in the
pack says so; the generator encodes it by setting a host's in_service_since to the date of the last
window that drained it, and by giving each host every finding whose fix was first published after
that date and nothing else.
"""
import datetime as dt
import random

from params import (COLO, CUTS, N_BY_MONTH, NOV_C, NOV_C_DAY, NOV_OFFICE, POOLS, DENSE, RACK,
                    SUMMER_FREEZE, TPS, WINDOWS, SCORE_LAST, CODE)

D = dt.date
T = dt.timedelta

BASE_PKGS = ["kernel", "openssl", "glibc", "curl", "libxml2", "openssh", "sudo", "systemd", "zlib",
             "expat", "sqlite-libs", "python3", "perl-libs", "bash", "tar", "gnupg2", "krb5-libs",
             "nss", "libssh2", "libtiff", "git-core", "vim-minimal", "less", "util-linux",
             "e2fsprogs", "polkit", "dbus", "libnghttp2"]
ROLE_PKGS = {"payments": {"settle": ["openjdk-11-jre-headless"], "report": ["postgresql15"],
                          "api": ["nginx"]},
             "checkout": {"basket": ["memcached"], "price": ["python3.9"], "web": ["nginx"]}}
# exploitable CVEs (kind X) carried by role packages of the quiet and active pools, by month
ROLE_X = {"openjdk-11-jre-headless": ["2025-12", "2026-06"], "postgresql15": ["2026-03"],
          "nginx": ["2026-07"], "memcached": ["2026-02"], "python3.9": ["2026-01", "2026-08"]}
# exploitable base-package events: (month, package); no package carries more than two
BASE_X = [("2025-11", "openssl"), ("2025-11", "sudo"), ("2025-12", "kernel"), ("2025-12", "curl"),
          ("2026-01", "glibc"), ("2026-01", "libxml2"), ("2026-02", "openssh"),
          ("2026-02", "expat"), ("2026-03", "kernel"), ("2026-03", "polkit"),
          ("2026-04", "libssh2"), ("2026-04", "sqlite-libs"), ("2026-05", "git-core"),
          ("2026-05", "python3"), ("2026-06", "libtiff"), ("2026-06", "nss"),
          ("2026-07", "curl"), ("2026-08", "systemd"), ("2026-08", "libnghttp2"),
          ("2026-09", "gnupg2"), ("2026-09", "glibc"), ("2026-10", "openssl")]
TEAMS = ["SRE platform", "Database operations", "Network engineering", "Payments engineering"]


# fix-publication dates for the exploitable base advisories (one per BASE_X entry), spread monthly
def _mid(ym, day):
    y, m = int(ym[:4]), int(ym[5:7])
    return D(y, m, day)


class Host:
    __slots__ = ("hid", "estate", "pool", "role", "in_service", "pkgs", "findings", "kind")

    def whole(self):
        """Exploitable findings on the host (all of them: a rebuild returns the current image)."""
        return len(self.findings)

    def pkg_count(self, pkg):
        return sum(1 for f in self.findings if f[0] == pkg)


def build_colo(rng, reg, base_adv, role_adv):
    """Return {estate: [Host,...]} with in_service dates and open exploitable findings.

    base_adv: {package: [(cve, fix_date), ...]} exploitable base advisories.
    role_adv: {package: [(cve, fix_date), ...]} exploitable role-package advisories.
    """
    hosts = {}
    for estate in COLO:
        hs = []
        hid = 0
        for pool, role, size, kind in POOLS[estate]:
            dense_pkg = None
            if kind == "dense":
                dense_pkg = dict((p, (pk, k)) for p, pk, k in DENSE[estate])[pool][0]
            for _ in range(size):
                hid += 1
                h = Host()
                h.hid = f"{CODE[estate].lower()}-{pool}-{hid:04d}"
                h.estate = estate
                h.pool = pool
                h.role = role
                h.kind = kind
                base = [p for p in BASE_PKGS if rng.random() < 0.58]
                if "glibc" not in base:       # the C library is on every el9 host
                    base.append("glibc")
                role_pkgs = ROLE_PKGS[estate].get(pool, [])
                h.pkgs = sorted(set(base) | set(role_pkgs) | ({dense_pkg} if dense_pkg else set()))
                # in_service_since: when the host last entered the serving pool
                if kind == "dense":
                    h.in_service = _mid(rng.choice(["2026-09", "2026-10"]), rng.randint(2, 26))
                elif kind == "active":
                    r = rng.random()
                    if r < 0.5:
                        h.in_service = _mid(rng.choice(["2026-06", "2026-07", "2026-08"]), rng.randint(1, 27))
                    elif r < 0.85:
                        h.in_service = _mid(rng.choice(["2026-02", "2026-03", "2026-04"]), rng.randint(1, 27))
                    else:
                        h.in_service = _mid(rng.choice(["2025-10", "2025-11", "2025-12"]), rng.randint(1, 27))
                else:  # quiet pools carry the oldest builds, the most exposed hosts
                    r = rng.random()
                    if r < 0.4:
                        h.in_service = _mid(rng.choice(["2025-09", "2025-10", "2025-11"]), rng.randint(1, 27))
                    elif r < 0.75:
                        h.in_service = _mid(rng.choice(["2026-01", "2026-02", "2026-03"]), rng.randint(1, 27))
                    else:
                        h.in_service = _mid(rng.choice(["2026-02", "2026-03", "2026-04"]), rng.randint(1, 27))
                h.in_service = _snap(h.in_service, estate)
                h.findings = assign_findings(h, base_adv, role_adv, dense_pkg)
                hs.append(h)
        hosts[estate] = hs
    return hosts


WIN_WD = {"payments": (1, 3), "checkout": (0, 2)}


def _snap(d, estate):
    """A 2026 serving date falls on the window it was returned in; a 2025 provisioning date (before
    the window era) is left as the original build date of a host no window has touched since."""
    if d < D(2026, 5, 1):
        return d
    wd = WIN_WD[estate]
    while d.weekday() not in wd:
        d -= T(days=1)
    return d


def assign_findings(h, base_adv, role_adv, dense_pkg):
    """Every exploitable advisory for an installed package whose fix published after in_service.

    This is the identity the stop-rung solver never checks: a host carries nothing the current
    image already fixes, so a rebuild removes exactly these findings.
    """
    out = []
    for pkg in h.pkgs:
        for cve, fix_date in base_adv.get(pkg, []):
            if fix_date > h.in_service:
                out.append((pkg, cve))
        for cve, fix_date in role_adv.get(pkg, []):
            if fix_date > h.in_service:
                out.append((pkg, cve))
    return out


def build_advisories(rng, reg):
    """Exploitable advisories for base and role packages: {package: [(cve, fix_date), ...]}.

    One exploitable CVE per BASE_X entry; the dense role packages carry a recent burst so a
    freshly-returned dense host still shows several of that one package and little else.
    """
    base_adv = {}
    for ym, pkg in BASE_X:
        fix = min(_mid(ym, rng.randint(3, 25)), LAST_FIX)
        c = reg.make(pkg, "X", fix, change=fix - T(days=rng.randint(1, 20)))
        base_adv.setdefault(pkg, []).append((c.id, fix))
    role_adv = {}
    for pkg, months in ROLE_X.items():
        for ym in months:
            fix = _mid(ym, rng.randint(3, 25))
            c = reg.make(pkg, "X", fix, change=fix - T(days=rng.randint(1, 20)))
            role_adv.setdefault(pkg, []).append((c.id, fix))
    # dense-package bursts, published in October 2026 (after the dense hosts were last returned)
    for estate in COLO:
        for pool, pkg, k in DENSE[estate]:
            if pkg in role_adv:   # nodejs/openjdk shared; add burst entries distinctly
                pass
            for _ in range(k):
                fix = _mid("2026-10", rng.randint(2, 20))
                c = reg.make(pkg, "X", fix, change=fix - T(days=rng.randint(1, 10)))
                role_adv.setdefault(pkg, []).append((c.id, fix))
    # the October glibc advisory: the highest-scoring exploitable finding on both colocated estates,
    # drawn on its own generator so the rest of the world keeps its draws
    saved = reg.rng
    reg.rng = random.Random(GLIBC_SEED)
    c = reg.make("glibc", "X", GLIBC_FIX, change=GLIBC_FIX)
    reg.rng = saved
    c.pre, c.final = GLIBC_SCORE, GLIBC_SCORE
    base_adv.setdefault("glibc", []).append((c.id, GLIBC_FIX))
    return base_adv, role_adv


LAST_FIX = D(2026, 10, 19)       # no advisory in the pack is published after this date
GLIBC_FIX = D(2026, 10, 13)
GLIBC_SCORE = 0.9712
GLIBC_SEED = 128077


def bind_acceptances(requests, hosts, base_adv, role_adv):
    """Make the host inventory agree with the provider's record of past drains.

    A request's accepted hosts are the first `accepted` of its requested hosts. A host the provider
    accepted in a May to October window last entered service on the latest such window; a host it
    never accepted keeps a build date from before the window record began. Findings are re-derived
    from the new date, so the feed still carries exactly what the current image would fix.
    """
    latest = {}
    for r in requests:
        for hid in r["hosts"][:r["accepted"]]:
            if hid not in latest or r["date"] > latest[hid]:
                latest[hid] = r["date"]
    for est in COLO:
        for h in hosts[est]:
            if h.hid in latest:
                h.in_service = latest[h.hid]
            elif h.in_service >= D(2026, 5, 1):
                h.in_service = D(2026, 3, 2) + T(days=int(h.hid[-4:]) % 45)
            h.findings = assign_findings(h, base_adv, role_adv, None)


def tune_host(h, delta, base_adv, role_adv):
    """Raise host h's open exploitable findings by exactly `delta` by giving it installed packages it
    lacked, each bringing every advisory published after its in_service date. Returns True on success."""
    if delta == 0:
        return True
    cand = []
    for pkg in sorted(set(base_adv) | set(role_adv)):
        if pkg in h.pkgs:
            continue
        n = sum(1 for _, f in base_adv.get(pkg, []) + role_adv.get(pkg, []) if f > h.in_service)
        if n:
            cand.append((pkg, n))
    # smallest set of packages whose counts sum to delta (deterministic search)
    best = None
    def go(i, left, chosen):
        nonlocal best
        if left == 0:
            if best is None or len(chosen) < len(best):
                best = list(chosen)
            return
        if i >= len(cand) or left < 0 or (best is not None and len(chosen) >= len(best)):
            return
        chosen.append(cand[i][0]); go(i + 1, left - cand[i][1], chosen); chosen.pop()
        go(i + 1, left, chosen)
    go(0, delta, [])
    if best is None:
        return False
    h.pkgs = sorted(set(h.pkgs) | set(best))
    h.findings = assign_findings(h, base_adv, role_adv, None)
    return True
