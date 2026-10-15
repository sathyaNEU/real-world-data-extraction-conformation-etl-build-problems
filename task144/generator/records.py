"""The call's exports, from the world: the events warehouse's star stream in its two schema vintages, the warehouse's
daily rollup of external first stars, the account snapshot, the organisation memberships, the repositories file and
the surface code crosswalk."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import common as K

EV25_COLS = ["event_id", "event_ts_ms", "repo_id", "actor_id", "action", "src", "client"]
EV26_COLS = ["event_id", "occurred_at", "repository_id", "account_id", "event_type", "surface", "client"]
ROLL_COLS = ["repository_id", "day", "feed", "newsletter", "repo_page", "search", "explore", "api",
             "external_first_stars"]
MEM_COLS = ["organization", "account_id", "role", "joined_at", "left_at"]
XW_COLS = ["v5_src", "v6_surface", "meaning", "v5_used_to", "v6_used_from"]

CROCK = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
CLIENTS = {"feed": (("web", 0.61), ("ios", 0.21), ("android", 0.18)),
           "newsletter": (("web", 0.83), ("ios", 0.10), ("android", 0.07)),
           "repo_page": (("web", 0.86), ("ios", 0.08), ("android", 0.06)),
           "search": (("web", 0.95), ("ios", 0.03), ("android", 0.02)),
           "explore": (("web", 0.88), ("ios", 0.07), ("android", 0.05)),
           "api": (("cli", 0.74), ("api", 0.26))}


def _client(surface, *key):
    u = int(K.hexid("client", *key, n=8), 16) / 16 ** 8
    acc = 0.0
    for name, share in CLIENTS[surface]:
        acc += share
        if u < acc:
            return name
    return CLIENTS[surface][-1][0]


def ulid(t, *key):
    """A ULID: 48 bits of milliseconds since the epoch and 80 bits from a hash, Crockford base32."""
    ms = int((t.replace(tzinfo=K.UTC)).timestamp() * 1000)
    rnd = int(K.hexid("ulid", *key, n=20), 16)
    n = (ms << 80) | rnd
    out = []
    for _ in range(26):
        out.append(CROCK[n & 31])
        n >>= 5
    return "".join(reversed(out))


def in_window(r, t):
    """A star event the extract carries: in the repository's first 100 days public and by the extract's last second."""
    return t <= K.CUT and 1 <= K.day_index(r.public, t) <= 100


def star_events(W):
    """Every star, restar and unstar of the event-level repositories, in time order, at the world's precision."""
    out = []
    for r in W.repos:
        if not r.shipped_events:
            continue
        for s in r.stars:
            if in_window(r, s.t):
                out.append((s.t, r.id, s.account, "star", s.surface, s.first))
            if s.first and s.unstar_at is not None and in_window(r, s.unstar_at):
                u = int(K.hexid("unstar-surface", r.id, s.account, n=4), 16) % 10
                out.append((s.unstar_at, r.id, s.account, "unstar", "api" if u == 0 else "repo_page", False))
    out.sort(key=lambda e: (e[0], e[1], e[2], e[3]))
    return out


def ev_rows(W):
    """Split at the schema change: v5 rows to 1 March 2026 (epoch milliseconds, short codes), v6 rows from 2 March."""
    v5, v6 = [], []
    seq = 7_214_880_331
    for t, rid, aid, action, surface, first in star_events(W):
        cl = _client(surface, rid, aid, action, t.isoformat())
        if t < K.SCHEMA_V6:
            seq += 1 + int(K.hexid("seq", rid, aid, action, n=4), 16) % 37
            v5.append([seq, int(t.replace(tzinfo=K.UTC).timestamp() * 1000), rid, aid, action, K.V5_OF[surface], cl])
        else:
            v6.append([ulid(t, rid, aid, action), K.iso_z(t), rid, aid,
                       "star.created" if action == "star" else "star.deleted", surface, cl])
    return v5, v6


def external_first(r, W):
    """The memo's external stars: an account's first star, not a bot, not a member of the owning organisation when
    it stars (the world's members are members throughout)."""
    mem = set(W.members[r.id])
    acc = W.accounts.by_id
    return [s for s in r.stars if s.first and acc[s.account].type != "bot" and s.account not in mem]


def rollup_rows(W):
    rows = []
    for r in sorted(W.repos, key=lambda x: x.id):
        last = min(100, K.day_index(r.public, K.CUT))
        days = {}
        for s in external_first(r, W):
            k = K.day_index(r.public, s.t)
            if 1 <= k <= last and s.t <= K.CUT:
                days.setdefault(k, {}).setdefault(s.surface, 0)
                days[k][s.surface] += 1
        for k in range(1, last + 1):
            d = days.get(k, {})
            row = {"repository_id": r.id, "day": (r.public.date() + dt.timedelta(days=k - 1)).isoformat()}
            tot = 0
            for sf in K.SURFACES_V6:
                row[sf] = d.get(sf, 0)
                tot += row[sf]
            row["external_first_stars"] = tot
            rows.append(row)
    return rows


def crosswalk_rows():
    return [
        ["dash", "feed", "star button on a card in the home feed", "2026-03-01", "2026-03-02"],
        ["nl", "newsletter", "repository opened from a link in Sluis", "2026-03-01", "2026-03-02"],
        ["repo", "repo_page", "star button on the repository page (web and apps)", "2026-03-01", "2026-03-02"],
        ["srch", "search", "star button in search results", "2026-03-01", "2026-03-02"],
        ["expl", "explore", "star button on the explore and trending pages", "2026-03-01", "2026-03-02"],
        ["api", "api", "starred through the REST API or the gw command-line client", "2026-03-01", "2026-03-02"],
    ]


# ---------------------------------------------------------------------------------------------------- accounts

def email_hash(aid):
    return hashlib.sha256(("%s@users.mail.example" % K.hexid("mail", aid, n=12)).encode()).hexdigest()


def referenced_accounts(W, extra=()):
    ids = set()
    for r in W.repos:
        if r.shipped_events:
            for s in r.stars:
                if in_window(r, s.t):
                    ids.add(s.account)
    for org, aid, joined, left, role in W.member_rows:
        ids.add(aid)
    ids.update(W.owner_account.values())
    ids.update(extra)
    for aid in list(ids):
        m = W.accounts.by_id[aid].merged_into
        if m is not None:
            ids.add(m)
    return sorted(ids)


def write_accounts(path, W, ids):
    acc = W.accounts.by_id
    rows = [acc[i] for i in ids]
    created = [int(a.created.replace(microsecond=0, tzinfo=K.UTC).timestamp()) for a in rows]
    table = pa.table({
        "account_id": pa.array([a.id for a in rows], pa.int64()),
        "login": pa.array([a.login for a in rows], pa.string()),
        "account_type": pa.array([a.type for a in rows], pa.string()),
        "created_at": pa.array(created, pa.timestamp("s", tz="UTC")),
        "followers": pa.array([a.followers for a in rows], pa.int32()),
        "following": pa.array([a.following for a in rows], pa.int32()),
        "primary_email_sha256": pa.array([a.email_key if a.type == "user" else None for a in rows], pa.string()),
        "merged_into": pa.array([a.merged_into for a in rows], pa.int64()),
    })
    pq.write_table(table, path, compression="snappy", use_dictionary=["account_type"], write_statistics=True,
                   row_group_size=65536)
    return len(rows)


def member_rows(W):
    out = []
    for org, aid, joined, left, role in sorted(W.member_rows, key=lambda x: (x[0], x[2], x[1])):
        out.append([org, aid, role, joined.strftime("%Y-%m-%d %H:%M:%S"),
                    left.strftime("%Y-%m-%d %H:%M:%S") if left else ""])
    return out


# ---------------------------------------------------------------------------------------------------- repositories

LICENSES = ["MIT", "Apache-2.0", "MIT", "BSD-3-Clause", "MPL-2.0", "MIT", "Apache-2.0", "GPL-3.0-only", "ISC"]


def repo_records(W):
    out = []
    for r in sorted(W.repos, key=lambda x: x.id):
        g = K.rng("repo-meta", r.id)
        created = r.public - dt.timedelta(days=float(g.uniform(12, 260)), hours=float(g.uniform(0, 23)))
        name = r.name
        full = "%s/%s" % (r.owner, name)
        out.append({
            "id": r.id,
            "full_name": full,
            "name": name,
            "owner": {"login": r.owner, "type": "Organization" if r.owner_type == "organization" else "User",
                      "id": W.owner_account[r.owner]},
            "description": r.description,
            "language": r.language,
            "license": LICENSES[int(g.integers(len(LICENSES)))],
            "default_branch": "main" if g.random() < 0.86 else "trunk",
            "created_at": K.iso_z(created.replace(microsecond=0)),
            "made_public_at": K.iso_z(r.public),
            "archived": False,
            "html_url": "https://%s/%s" % (K.HOST, full),
        })
    return out
