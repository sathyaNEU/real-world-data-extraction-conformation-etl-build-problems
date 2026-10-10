"""The four cloud estates: hosts, the open-finding spine (the office scanner export, ~210k rows),
the package updates the crews raise as tickets, and the Q3 close-out of ticketed exposure closed.

A cloud ticket updates one package on one estate and takes out, in place, that package's exploitable
findings on the estate's in-service hosts. Exploitable is scored by EPSS on the day the ticket is
cut, at or above 0.10; the scanner's exploit-available flag is the cruder proxy the natural pipeline
reaches for.
"""
import datetime as dt

from params import (CLOUD, CLOUD_HOSTS, CLOUD_STANDBY, CLOUD_STOPPED, DOMAIN, CLOUD_RELEASE,
                    MEDIA_OLD_DOMAIN, CODE, Q3_CUTS, CUTS)

D = dt.date

# package catalogue for cloud estates: a realistic spread of OS and app packages
CLOUD_PKGS = ["linux-image-generic", "openssl", "libc6", "curl", "libssl3", "openssh-server",
              "python3.11", "python3.12", "libxml2", "nginx", "openjdk-17-jre-headless",
              "libexpat1", "zlib1g", "libsqlite3-0", "sudo", "systemd", "dbus", "libnghttp2-14",
              "redis-tools", "postgresql-client-16", "nodejs", "golang-1.22", "containerd",
              "runc", "git", "vim", "perl-base", "libgnutls30", "ca-certificates", "libpcre2-8",
              "libkrb5-3", "rsync", "wget", "libtiff6", "imagemagick", "ffmpeg", "libavcodec60",
              "elasticsearch", "opensearch", "kafka", "spark-core", "hadoop-common",
              "libgcrypt20", "libjpeg-turbo8", "libpng16-16", "libwebp7", "libzstd1", "liblz4-1",
              "libbz2-1.0", "libxslt1.1", "libyaml-0-2", "libffi8", "libgmp10", "libp11-kit0",
              "libtasn1-6", "libidn2-0", "libunistring2", "libpsl5", "librtmp1", "libldap-2.5-0",
              "libsasl2-2", "libcap2", "libaudit1", "libseccomp2", "libselinux1", "libpam0g",
              "libdevmapper1.02.1", "libjson-c5", "libcurl4", "libgssapi-krb5-2", "libk5crypto3",
              "libkeyutils1", "libmount1", "libblkid1", "libuuid1", "libacl1", "libattr1",
              "libgpg-error0", "libassuan0", "libnpth0", "libreadline8", "libncursesw6", "libtinfo6",
              "libgdbm6", "libdb5.3", "liblzma5", "libcap-ng0", "libmnl0", "libnftnl11", "libedit2",
              "tzdata", "bind9-libs", "dnsutils", "iproute2", "iptables", "net-tools", "procps",
              "coreutils", "findutils", "grep", "sed", "gawk", "diffutils", "gzip", "bzip2", "xz-utils"]
# packages concentrated on each estate (its workload), on top of the OS base
ESTATE_PKGS = {"search": ["elasticsearch", "opensearch", "nginx", "golang-1.22"],
               "media": ["imagemagick", "ffmpeg", "libavcodec60", "libtiff6", "nginx"],
               "tools": ["git", "vim", "python3.11", "nodejs", "postgresql-client-16"],
               "pipeline": ["kafka", "spark-core", "hadoop-common", "containerd", "runc"]}
TEAMS = {"search": "Search platform", "media": "Media services", "tools": "Developer tools",
         "pipeline": "Data platform"}


class CHost:
    __slots__ = ("hid", "estate", "domain", "pkgs", "standby", "stopped", "last_scan",
                 "renamed_from", "iid", "hostname")


def build_cloud_hosts(rng):
    hosts = {}
    for est in CLOUD:
        hs = []
        n = CLOUD_HOSTS[est]
        standby = set(rng.sample(range(n), CLOUD_STANDBY[est]))
        stopped = set(rng.sample([i for i in range(n) if i not in standby], CLOUD_STOPPED[est]))
        for i in range(n):
            h = CHost()
            h.hid = f"{CODE[est].lower()}-{i:04d}"
            h.estate = est
            h.domain = DOMAIN[est]
            h.standby = i in standby
            h.stopped = i in stopped
            h.renamed_from = None
            h.iid = f"i-{est[:2]}{i:05d}{rng.randint(10,99)}"
            h.hostname = f"{h.hid}.{h.domain}"
            # last authenticated scan: most within the 14-day window before export, some older/none
            import datetime as _dt
            if h.stopped:
                h.last_scan = None
            else:
                r = rng.random()
                if r < 0.84:
                    h.last_scan = _dt.date(2026, 10, rng.randint(9, 22))
                elif r < 0.95:
                    h.last_scan = _dt.date(2026, 10, rng.randint(1, 8))
                else:
                    h.last_scan = None
            base = [p for p in CLOUD_PKGS if rng.random() < 0.14]
            h.pkgs = sorted(set(base) | set(ESTATE_PKGS[est]))
            hs.append(h)
        # media domain migration mid-September: a block of media hosts renamed, their recent scans
        # recorded under the old hostname in the coverage file
        if est == "media":
            migr = [h for h in hs if not h.stopped][:140]
            for h in migr:
                h.renamed_from = f"{h.hid}.{MEDIA_OLD_DOMAIN}"
        hosts[est] = hs
    return hosts


def build_cve_pool(rng, reg):
    """{(estate, package): {"bulk":[cve...], "exp": cve or None, "target": v}}.

    Each cloud package carries several below-the-line CVEs (the spine bulk) and, for about three
    quarters of packages, one exploitable CVE placed on `target` of the package's hosts, so a
    package update takes out that modest count in November and the candidate cutline sits low.
    """
    import datetime as dt, math
    pool = {}
    for est in CLOUD:
        pkgset = CLOUD_PKGS + ESTATE_PKGS[est]
        for pkg in sorted(set(pkgset)):
            m = rng.randint(3, 6)
            bulk = []
            for _ in range(m):
                mo = rng.randint(1, 9)
                bulk.append(reg.make(pkg, "N", dt.date(2026, mo, rng.randint(1, 27))))
            exp = None
            target = 0
            if rng.random() < 0.76:
                mo = rng.randint(1, 9)
                exp = reg.make(pkg, "X" if rng.random() < 0.72 else "NX",
                               dt.date(2026, mo, rng.randint(1, 27)))
                target = max(6, int(round(math.exp(rng.uniform(math.log(8), math.log(90))))))
            pool[(est, pkg)] = {"bulk": bulk, "exp": exp, "target": target}
    return pool


def exploitable_now(cve):
    """Latest EPSS score at or above 0.10 (jitter never crosses the clamps)."""
    return cve.final >= 0.10


def exploitable_on(cve, d):
    lvl = cve.pre if d < cve.change else cve.final
    return lvl >= 0.10


def build_spine(rng, hosts, pool):
    """Open findings on in-service cloud hosts: list of dicts, ~210k rows.

    A host is in service unless stopped. first_seen is the day the finding was first observed;
    last_scan is the host's latest authenticated scan.
    """
    import datetime as dt
    rows = []
    for est in CLOUD:
        serving = [h for h in hosts[est] if not h.stopped]
        # bulk (below-the-line) findings
        for h in serving:
            for pkg in h.pkgs:
                ent = pool.get((est, pkg))
                if not ent:
                    continue
                for c in ent["bulk"]:
                    if rng.random() < 0.90:
                        fs = c.published + dt.timedelta(days=rng.randint(1, 20))
                        rows.append({"host": h.hid, "estate": est, "domain": h.domain, "package": pkg,
                                     "cve": c.id, "cvss": c.cvss, "exploit_flag": c.flag,
                                     "first_seen": fs, "last_scan": h.last_scan})
        # the one exploitable finding per package, placed on exactly `target` serving hosts
        for pkg in sorted({p for (e, p) in pool if e == est}):
            ent = pool[(est, pkg)]
            if not ent["exp"] or ent["target"] <= 0:
                continue
            carriers = [h for h in serving if pkg in h.pkgs]
            if not carriers:
                continue
            t = min(ent["target"], len(carriers))
            ent["target"] = t
            c = ent["exp"]
            for h in sorted(carriers, key=lambda x: x.hid)[:t]:
                fs = c.published + dt.timedelta(days=rng.randint(1, 20))
                rows.append({"host": h.hid, "estate": est, "domain": h.domain, "package": pkg,
                             "cve": c.id, "cvss": c.cvss, "exploit_flag": c.flag,
                             "first_seen": fs, "last_scan": h.last_scan})
    rng.shuffle(rows)
    return rows


def nov_ticket_values(rows, pool):
    """{(estate, package): exploitable-now open-finding count} = November take-out of that ticket."""
    byid = {}
    for ent in pool.values():
        for c in ent["bulk"]:
            byid[c.id] = c
        if ent["exp"]:
            byid[ent["exp"].id] = ent["exp"]
    vals = {}
    for r in rows:
        c = byid[r["cve"]]
        if exploitable_now(c):
            vals[(r["estate"], r["package"])] = vals.get((r["estate"], r["package"]), 0) + 1
    return vals


MONTHS_Q3 = {7: Q3_CUTS[0], 8: Q3_CUTS[1], 9: Q3_CUTS[2]}


def build_closeout(rng, reg):
    """Q3 completed cloud tickets and their fixed findings; the 12 estate-month figures of ticketed
    exposure closed under the cut-day rule, with every rival's miss.

    Returns (fixed_rows, figures, rivals). fixed_rows ship in the Q3 ticket log and its fixed
    findings; figures[(estate, month)] = truth; rivals[name] = total absolute miss across the 12.
    """
    import datetime as dt
    fixed = []       # dicts: ticket_id, estate, month, cut, host, package, cve
    cve_meta = {}    # cve -> (kind, change, cut)
    tnum = 0
    for est in CLOUD:
        for mo, cut in MONTHS_Q3.items():
            tnum += 1
            npkg = rng.randint(3, 5)
            pkgs = rng.sample(sorted(set(CLOUD_PKGS + ESTATE_PKGS[est])), npkg)
            for pkg in pkgs:
                tnum += 1
                tid = f"CHG-{est[:3].upper()}-2026{mo:02d}-{tnum:04d}"
                nf = rng.randint(14, 40)
                for _ in range(nf):
                    roll = rng.random()
                    kind = "X" if roll < 0.52 else "XN" if roll < 0.72 else "NX" if roll < 0.86 else "N"
                    pub = dt.date(2026, rng.randint(1, mo), rng.randint(1, 27))
                    # change date lands between the cut and the export for the crossing kinds, so
                    # the cut-day and export readings disagree on exactly those findings
                    if kind in ("XN", "NX"):
                        change = cut + dt.timedelta(days=rng.randint(5, 110))
                        if change > dt.date(2026, 10, 20):
                            change = dt.date(2026, 10, 20)
                    else:
                        change = pub + dt.timedelta(days=rng.randint(1, 20))
                    c = reg.make(pkg, kind, pub, change=change)
                    # the scanner's exploit flag is a noisy proxy: it fires on most exploitable
                    # findings and on some that are not, so it is ~14 per cent off the cut-day truth
                    truth_cut = exploitable_on(c, cut)
                    c.flag = rng.random() < (0.73 if truth_cut else 0.22)
                    cve_meta[c.id] = (kind, change, cut)
                    host = f"{CODE[est].lower()}-{rng.randint(0, CLOUD_HOSTS[est]-1):04d}"
                    fixed.append({"ticket": tid, "estate": est, "month": mo, "cut": cut,
                                  "host": host, "package": pkg, "cve": c.id})
    def count(rule):
        fig = {}
        for r in fixed:
            kind, change, cut = cve_meta[r["cve"]]
            c = reg.by_id[r["cve"]]
            if rule(c, kind, change, cut):
                fig[(r["estate"], r["month"])] = fig.get((r["estate"], r["month"]), 0) + 1
        return fig
    truth = count(lambda c, k, ch, cut: exploitable_on(c, cut))
    rules = {
        "flag": lambda c, k, ch, cut: c.flag,
        "score_at_export": lambda c, k, ch, cut: exploitable_now(c),
        "score_quarter_end": lambda c, k, ch, cut: exploitable_on(c, dt.date(2026, 9, 30)),
        "cvss_band": lambda c, k, ch, cut: c.cvss >= 7.0,
        "threshold_005": lambda c, k, ch, cut: (c.pre if cut < ch else c.final) >= 0.05,
        "flag_or_score": lambda c, k, ch, cut: c.flag or exploitable_on(c, cut),
    }
    rivals = {}
    cells = [(e, m) for e in CLOUD for m in MONTHS_Q3]
    for name, rule in rules.items():
        fig = count(rule)
        miss = sum(1 for cell in cells if fig.get(cell, 0) != truth.get(cell, 0))
        tot_truth = sum(truth.values())
        tot_r = sum(fig.values())
        pct = abs(tot_r - tot_truth) / tot_truth * 100
        rivals[name] = {"cell_misses": miss, "total": tot_r, "pct_off": round(pct, 1)}
    return fixed, truth, rivals, cve_meta
