"""The ask side of the pack, built from the world: Sluis's sends from April to September 2026 on its two newsletter
platforms (Postwerk to 1 June, Relaymark from 2 June) with their link clicks, the October nomination form's export
and the platform's 2026 repository renames; and the two files nothing reads (the shortlist's page traffic and the
daily trending lists).

How the sends come to exist. Each issue goes to the Sluis list in two batches on its Tuesday morning, the first at
09:00 Amsterdam time and the second about an hour later (the editors spread the send so the spotlighted repository's
page is not hit all at once); Postwerk reports the batches as two rows of one campaign, Relaymark as two campaigns of
the same name. On the Thursday after, the editors send the issue again to the subscribers who had not opened it, a
third send to the same list under the same name. A [TEST] copy goes to the editorial seed addresses the afternoon
before. Postwerk's template carries the spotlight twice (the heading and the screenshot); Relaymark's template, from
June, carries it as the heading (tag feature) and the button (tag feature_cta), and adds a follow-up link to last
month's spotlight under the tag spotlight. A few subscribers who had not opened the issue by the Thursday opened the
first send later and clicked through in both."""
from __future__ import annotations

import datetime as dt
import hashlib
import json

import numpy as np

import common as K
import records as R

ASK_MONTHS = [(2026, m) for m in range(4, 10)]
PW_MONTHS = [(2026, 4), (2026, 5)]
RM_MONTHS = [(2026, 6), (2026, 7), (2026, 8), (2026, 9)]
DUTCH_MONTH = {4: "april", 5: "mei"}

PW_CAMP_COLS = ["campaign_id", "campaign_name", "list", "send_time", "recipients", "hard_bounces", "soft_bounces",
                "delivered", "unique_opens", "unique_clicks", "unsubscribes", "spam_complaints"]
PW_LINK_COLS = ["campaign_id", "subscriber_id", "link_label", "url", "clicks"]
RM_LINK_COLS = ["campaign_id", "subscriber_id", "link_tag", "url", "clicked_at"]
NOM_COLS = ["response_id", "submitted_at", "signed_in", "account_id", "email_sha256", "repository"]
REN_COLS = ["repository_id", "old_full_name", "new_full_name", "renamed_at"]
TRAFFIC_COLS = ["repository_id", "day", "referrer", "views", "unique_visitors"]
TRENDING_COLS = ["day", "language", "rank", "repository", "stars_today"]


def spotlight_of(W):
    return {r.issue: r for r in W.lottery if r.drawn}


def utm(url, ym, content):
    return "%s?utm_source=sluis&utm_medium=email&utm_campaign=%d-%02d&utm_content=%s" % (url, ym[0], ym[1], content)


def repo_url(r):
    return "https://%s/%s/%s" % (K.HOST, r.owner, r.name)


class Campaign:
    def __init__(self, cid, name, lst, send_local, platform, ym, kind):
        self.id, self.name, self.list = cid, name, lst
        self.send_local, self.platform, self.ym, self.kind = send_local, platform, ym, kind
        self.recipients = self.hard = self.soft = self.delivered = self.opens = self.unsubs = self.complaints = 0
        self.clicks = {}          # link label -> {subscriber: clicks}

    @property
    def unique_clicks(self):
        s = set()
        for d in self.clicks.values():
            s.update(d)
        return len(s)


def _sizes(g, recipients, open_rate):
    hard = int(round(recipients * g.uniform(0.0014, 0.0022)))
    soft = int(round(recipients * g.uniform(0.0024, 0.0043)))
    delivered = recipients - hard - soft
    opens = int(round(delivered * open_rate))
    return hard, soft, delivered, opens


def _ids(g, prefix, start, n, exclude=()):
    """n distinct subscriber ids from the platform's id space."""
    ex = set(exclude)
    out = []
    while len(out) < n:
        draw = g.integers(start, start + 9_000_000, size=n * 2)
        for x in draw:
            sid = "%s%d" % (prefix, x)
            if sid not in ex:
                ex.add(sid)
                out.append(sid)
                if len(out) == n:
                    break
    return out


def labels(pw):
    return ("spotlight", "spotlight-beeld") if pw else ("feature", "feature_cta")


def build_sends(W):
    """Every send of April to September 2026 on both platforms, with each subscriber's clicks by link."""
    spot = spotlight_of(W)
    camps = []
    for ym in ASK_MONTHS:
        g = K.rng("sends", *ym)
        y, m = ym
        L = W.list[ym]
        send = K.to_amsterdam(K.ISSUE_SEND[ym])
        pw = ym in PW_MONTHS
        prefix = "PW-" if pw else "sub_"
        base_id = 10_000_000 if pw else 40_000_000
        label = DUTCH_MONTH[m] if pw else K.MONTH_NAME[m]
        name = "Sluis %s %d" % (label, y)
        plat = "postwerk" if pw else "relaymark"
        recipients = int(round(L * (1 + g.uniform(0.0012, 0.0031)) * (1 - g.uniform(0.0049, 0.0066))))
        first = int(round(recipients * g.uniform(0.47, 0.56)))
        open_rate = g.uniform(0.392, 0.437)
        pw_id = "PW%06d" % (318_000 + m * 211 + int(g.integers(0, 90)))
        group = []
        second_at = send + dt.timedelta(minutes=int(g.integers(52, 71)), seconds=int(g.integers(0, 59)))
        for b, (n, at) in enumerate(((first, send), (recipients - first, second_at)), 1):
            cid = pw_id if pw else "cmp_" + K.hexid("rm", y, m, b, n=12)
            c = Campaign(cid, name, "Sluis", at, plat, ym, "batch")
            c.recipients = n
            c.hard, c.soft, c.delivered, c.opens = _sizes(g, n, open_rate * g.uniform(0.985, 1.015))
            c.unsubs = int(round(c.delivered * g.uniform(0.0011, 0.0017)))
            c.complaints = int(g.integers(5, 17))
            group.append(c)
        if sum(c.delivered for c in group) % 100 == 0:
            # a round total is a coincidence of the draw; one more soft bounce in the second batch breaks it
            group[1].soft += 1
            group[1].delivered -= 1
        delivered = sum(c.delivered for c in group)
        opens = sum(c.opens for c in group)
        rid = ("PW%06d" % (318_000 + m * 211 + 97 + int(g.integers(0, 90)))) if pw else ("cmp_" + K.hexid("rm-resend", *ym, n=12))
        days = 2
        rc = Campaign(rid, name, "Sluis", send.replace(hour=9, minute=0) + dt.timedelta(days=days, minutes=int(g.integers(0, 4))),
                      plat, ym, "resend")
        rc.recipients = delivered - int(round(opens * g.uniform(0.86, 0.92)))
        rc.hard = 0
        rc.soft = int(round(rc.recipients * g.uniform(0.0006, 0.0011)))
        rc.delivered = rc.recipients - rc.soft
        rc.opens = int(round(rc.delivered * g.uniform(0.112, 0.141)))
        rc.unsubs = int(round(rc.delivered * g.uniform(0.0016, 0.0024)))
        rc.complaints = int(g.integers(14, 40))
        group.append(rc)
        test = Campaign(("PW%06d" % (318_000 + m * 211 - 3)) if pw else ("cmp_" + K.hexid("rm-test", *ym, n=12)),
                        "[TEST] %s" % name, "Redactie seed" if pw else "Editorial seeds",
                        send - dt.timedelta(hours=17, minutes=int(g.integers(5, 50))), plat, ym, "test")
        test.recipients = test.delivered = 14
        test.opens = int(g.integers(9, 14))
        group.append(test)
        news = Campaign(("PW%06d" % (318_000 + m * 211 + 41)) if pw else ("cmp_" + K.hexid("rm-news", *ym, n=12)),
                        ("Grachtwerk productnieuws %s %d" % (label, y)) if pw else ("Grachtwerk Product News, %s %d" % (label, y)),
                        "Productnieuws" if pw else "Product News",
                        send + dt.timedelta(days=8, hours=1, minutes=int(g.integers(0, 40))), plat, ym, "news")
        news.recipients = int(round(L * g.uniform(0.31, 0.36)))
        news.hard, news.soft, news.delivered, news.opens = _sizes(g, news.recipients, g.uniform(0.27, 0.33))
        news.unsubs = int(round(news.delivered * 0.002))
        news.complaints = int(g.integers(5, 20))
        group.append(news)
        _clicks(W, g, ym, group, spot, prefix, base_id, pw)
        _clear_of_edges(group, pw)
        camps.extend(group)
    return camps


def issue_share(group, pw):
    """The issue's delivered subscribers and spotlight click-through, as the golden counts them."""
    labs = labels(pw)
    delivered = sum(c.delivered for c in group if c.kind == "batch")
    who = set()
    for c in group:
        if c.kind in ("batch", "resend"):
            for lab in labs:
                who.update(c.clicks.get(lab, {}))
    return delivered, len(who), 100.0 * len(who) / delivered


def _clear_of_edges(group, pw):
    """Keep the click-through share at least 0.003 points from a two-decimal rounding edge: subscribers who clicked
    only the spotlight heading in the first batch are taken out of it, one at a time, the last first."""
    a_lab, b_lab = labels(pw)
    first = group[0]
    while True:
        d, n, share = issue_share(group, pw)
        pos = (share * 100) % 1
        if pos <= 0.2 or pos >= 0.8:
            return
        only = sorted(s for s in first.clicks[a_lab] if s not in first.clicks[b_lab]
                      and all(s not in c.clicks.get(a_lab, {}) and s not in c.clicks.get(b_lab, {})
                              for c in group[1:]))
        del first.clicks[a_lab][only[-1]]


def _clicks(W, g, ym, group, spot, prefix, base_id, pw):
    prev = spot.get((ym[0], ym[1] - 1))
    used = set()
    a_lab, b_lab = labels(pw)
    batch_spot = []
    for c in group:
        if c.kind == "test":
            for lab in (a_lab, b_lab):
                c.clicks[lab] = {"%sseed%02d" % (prefix, i): 1 for i in range(1, int(g.integers(3, 7)))}
            continue
        if c.kind == "news":
            n = int(round(c.delivered * g.uniform(0.021, 0.028)))
            ids = _ids(g, prefix, base_id, n, used)
            used.update(ids)
            c.clicks["release-notes" if pw else "release_notes"] = {s: 1 + int(g.poisson(0.3)) for s in ids}
            continue
        rate = g.uniform(0.0104, 0.0136) if c.kind == "batch" else g.uniform(0.0039, 0.0052)
        n_spot = int(round(c.delivered * rate))
        ids = _ids(g, prefix, base_id, n_spot, used)
        if c.kind == "resend":
            # a few of the Thursday's non-openers had opened the Tuesday send after all and clicked through in both
            k = int(round(n_spot * g.uniform(0.025, 0.04)))
            take = [batch_spot[int(i)] for i in g.choice(len(batch_spot), size=k, replace=False)]
            ids = ids[:n_spot - k] + take
        used.update(ids)
        u = g.random(len(ids))
        c.clicks[a_lab] = {s: 1 + int(g.poisson(0.35)) for s, x in zip(ids, u) if x < 0.81}
        c.clicks[b_lab] = {s: 1 + int(g.poisson(0.2)) for s, x in zip(ids, u) if x >= 0.68}
        if c.kind == "batch":
            batch_spot.extend(sorted(set(c.clicks[a_lab]) | set(c.clicks[b_lab])))
        scale = 1.0 if c.kind == "batch" else 0.31
        others = []
        if not pw and prev is not None:
            others.append(("spotlight", c.delivered * g.uniform(0.0036, 0.0047) * scale))
        for i in range(1, 4):
            others.append((("artikel-%d" if pw else "article_%d") % i, c.delivered * g.uniform(0.0021, 0.0072) * scale))
        others += [("pipelines", c.delivered * g.uniform(0.0011, 0.0019) * scale),
                   ("webversie" if pw else "view_online", c.delivered * g.uniform(0.0012, 0.0021) * scale),
                   ("afmelden" if pw else "unsubscribe", c.unsubs * g.uniform(1.12, 1.24))]
        pool = list(ids)
        for lab, n in others:
            n = int(round(n))
            fresh = _ids(g, prefix, base_id, int(round(n * 0.72)), used)
            used.update(fresh)
            back = [pool[int(i)] for i in g.choice(len(pool), size=min(len(pool), n - len(fresh)), replace=False)]
            c.clicks[lab] = {s: 1 + int(g.poisson(0.18)) for s in fresh + back}
            pool.extend(fresh)


def link_url(W, c, lab):
    spot = spotlight_of(W)
    ym = c.ym
    pw = c.platform == "postwerk"
    if c.kind == "news":
        return "https://%s/changelog/%d-%02d" % (K.HOST, ym[0], ym[1])
    if lab in ("spotlight", "spotlight-beeld") and pw:
        return utm(repo_url(spot[ym]), ym, "spotlight" if lab == "spotlight" else "spotlight_image")
    if lab == "feature":
        return utm(repo_url(spot[ym]), ym, "feature")
    if lab == "feature_cta":
        return utm(repo_url(spot[ym]), ym, "feature_button")
    if lab == "spotlight":
        return utm(repo_url(spot[(ym[0], ym[1] - 1)]), ym, "last_spotlight")
    if lab.startswith("artikel") or lab.startswith("article"):
        i = int(lab[-1])
        return "https://%s/blog/%d/%02d/%s" % (K.HOST, ym[0], ym[1], ARTICLES[(ym[1] * 4 + i) % len(ARTICLES)])
    if lab == "pipelines":
        return "https://%s/pipelines?utm_source=sluis&utm_campaign=%d-%02d" % (K.HOST, ym[0], ym[1])
    if lab in ("webversie", "view_online"):
        return "https://sluis.%s/%d-%02d" % (K.HOST, ym[0], ym[1])
    return "https://%s/sluis/unsubscribe" % K.HOST


ARTICLES = ["faster-clones-for-large-monorepos", "signed-commits-by-default", "what-we-learned-moving-ci-to-arm",
            "pipelines-caching-explained", "a-year-of-code-search", "review-requests-that-get-answered",
            "keeping-forks-in-sync", "the-new-explore-page", "issue-forms-in-practice", "merge-queues-at-scale",
            "dependency-alerts-without-the-noise", "how-we-run-grachtwerk-on-call", "packages-for-rust",
            "writing-good-release-notes", "secret-scanning-for-everyone", "web-ide-tips", "sponsors-in-europe",
            "notifications-you-can-trust", "project-boards-for-maintainers", "our-status-page-rebuilt",
            "ssh-certificates-for-teams", "codespaces-in-amsterdam", "triage-with-labels", "actions-to-pipelines"]


def pw_camp_rows(W, camps):
    rows = []
    for c in camps:
        if c.platform != "postwerk":
            continue
        rows.append([c.id, c.name, c.list, c.send_local.strftime("%d-%m-%Y %H:%M"), c.recipients, c.hard, c.soft,
                     c.delivered, c.opens, c.unique_clicks, c.unsubs, c.complaints])
    rows.sort(key=lambda r: (dt.datetime.strptime(r[3], "%d-%m-%Y %H:%M"), r[0]))
    return rows


def pw_link_rows(W, camps):
    """Postwerk reports a campaign's clicks once for all its batches."""
    merged = {}
    order = []
    for c in camps:
        if c.platform != "postwerk":
            continue
        if c.id not in merged:
            merged[c.id] = (c, {})
            order.append(c.id)
        for lab, d in c.clicks.items():
            tgt = merged[c.id][1].setdefault(lab, {})
            for s, n in d.items():
                tgt[s] = tgt.get(s, 0) + n
    rows = []
    for cid in order:
        c, clicks = merged[cid]
        for lab in sorted(clicks):
            url = link_url(W, c, lab)
            for s in sorted(clicks[lab]):
                rows.append([cid, s, lab, url, clicks[lab][s]])
    return rows


def rm_campaigns(W, camps):
    out = []
    for c in camps:
        if c.platform != "relaymark":
            continue
        t_utc = K.from_amsterdam(c.send_local)
        off = K.amsterdam_offset(t_utc)
        g = K.rng("rm-sec", c.id)
        sent = c.send_local + dt.timedelta(seconds=int(g.integers(1, 40)))
        out.append({
            "id": c.id, "name": c.name,
            "audience": {"list": c.list, "segment": None},
            "sent_at": sent.strftime("%Y-%m-%dT%H:%M:%S") + "+%02d:00" % off,
            "stats": {"recipients": c.recipients, "delivered": c.delivered,
                      "bounced": {"hard": c.hard, "soft": c.soft},
                      "unique_opens": c.opens, "unique_clicks": c.unique_clicks,
                      "unsubscribed": c.unsubs, "complaints": c.complaints},
        })
    out.sort(key=lambda x: (x["sent_at"], x["id"]))
    return {"account": "Grachtwerk B.V. / Sluis", "exported_at": "2026-09-28T08:12:44+02:00", "campaigns": out}


def rm_link_rows(W, camps):
    rows = []
    for c in camps:
        if c.platform != "relaymark":
            continue
        t0 = K.from_amsterdam(c.send_local)
        for lab in sorted(c.clicks):
            url = link_url(W, c, lab)
            for s in sorted(c.clicks[lab]):
                g = K.rng("click-t", c.id, lab, s)
                for j in range(c.clicks[lab][s]):
                    h = float(g.exponential(9.0)) if g.random() < 0.8 else float(g.uniform(10, 400))
                    t = t0 + dt.timedelta(minutes=2, hours=h)
                    rows.append([c.id, s, lab, url, K.iso_z(t.replace(microsecond=0))])
    rows.sort(key=lambda r: (r[4], r[0], r[1], r[2]))
    return rows


# ---------------------------------------------------------------------------------------------------- nominations

# per candidate: people, of them members of the owning organisation, nominated both signed in and signed out,
# members who nominated signed out only, and people whose earlier account was merged into the one they used later
NOM_PLAN = {
    "tracewire": dict(people=47, inside=4, both=3, both_member=1, member_out=1, merged=1, forks=1),
    "slidewell": dict(people=58, inside=0, both=4, both_member=0, member_out=0, merged=1, forks=3),
    "shiftgres": dict(people=31, inside=3, both=2, both_member=0, member_out=1, merged=1, forks=2),
    "kilnkit": dict(people=27, inside=5, both=2, both_member=0, member_out=2, merged=1, forks=0),
    "hullcheck": dict(people=26, inside=3, both=2, both_member=0, member_out=1, merged=1, forks=0),
    "timeloom": dict(people=19, inside=0, both=2, both_member=0, member_out=0, merged=1, forks=2),
    "ferrolog": dict(people=37, inside=7, both=3, both_member=1, member_out=2, merged=1, forks=0),
}
TWO_HOP = {"tracewire", "ferrolog"}
NOM_OPEN = dt.datetime(2026, 9, 1, 0, 0, 0)          # Amsterdam time
NOM_CLOSE = dt.datetime(2026, 9, 20, 23, 59, 59)


def _hash_email(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _ref(g, owner, name):
    u = g.random()
    if u < 0.58:
        return "%s/%s" % (owner, name)
    if u < 0.78:
        return "https://%s/%s/%s" % (K.HOST, owner, name)
    if u < 0.86:
        return "%s/%s/%s/" % (K.HOST, owner, name)
    if u < 0.92:
        return "%s/%s" % (owner.capitalize(), name.capitalize())
    return name


def build_nominations(W):
    """The form's rows and the truth behind them (each row's person)."""
    A = W.accounts
    rows = []
    truth = {}
    acc = A.by_id
    W.nominator_accounts = set()
    for key, plan in NOM_PLAN.items():
        r = W.by_name[key]
        g = K.rng("noms", key)
        start = max(NOM_OPEN, K.to_amsterdam(r.public) + dt.timedelta(hours=3))
        span = (NOM_CLOSE - start).total_seconds()
        members = list(W.members[r.id])
        starrers = [s.account for s in R.external_first(r, W) if s.t <= K.CUT]
        people = []      # each: dict(kind, account, hash, member)
        mem_pick = [members[int(i)] for i in g.choice(len(members), size=plan["inside"], replace=False)] if plan["inside"] else []
        n_mem_out = plan["member_out"]
        n_both_mem = plan["both_member"]
        for j, aid in enumerate(mem_pick):
            if j < n_mem_out:
                people.append(dict(kind="out", account=aid, hash=acc[aid].email_key, member=True))
            elif j < n_mem_out + n_both_mem:
                people.append(dict(kind="both", account=aid, hash=acc[aid].email_key, member=True))
            else:
                people.append(dict(kind="in", account=aid, hash=None, member=True))
        for _ in range(plan["both"] - n_both_mem):
            a = A._new("regular", dt.datetime(2016, 1, 1) + dt.timedelta(days=float(g.uniform(0, 3500))),
                       int(np.floor(np.exp(g.normal(1.6, 1.2)))))
            people.append(dict(kind="both", account=a.id, hash=a.email_key, member=False))
        for _ in range(plan["merged"]):
            old = A._new("regular", dt.datetime(2015, 6, 1) + dt.timedelta(days=float(g.uniform(0, 2000))), 0)
            new = A._new("regular", dt.datetime(2022, 1, 1) + dt.timedelta(days=float(g.uniform(0, 1200))),
                         int(np.floor(np.exp(g.normal(1.8, 1.1)))))
            if key in TWO_HOP:
                # merged twice: the oldest account into a second one, which was later merged into the current one
                mid = A._new("regular", dt.datetime(2019, 3, 1) + dt.timedelta(days=float(g.uniform(0, 900))), 0)
                old.merged_into = mid.id
                mid.merged_into = new.id
                W.nominator_accounts.add(mid.id)
            else:
                old.merged_into = new.id
            people.append(dict(kind="merged", account=new.id, old=old.id, hash=None, member=False))
        rest = plan["people"] - len(people)
        pick = [starrers[int(i)] for i in g.choice(len(starrers), size=rest, replace=False)]
        for aid in pick:
            u = g.random()
            if u < 0.62:
                people.append(dict(kind="in", account=aid, hash=None, member=False))
            elif u < 0.80:
                people.append(dict(kind="out", account=aid, hash=acc[aid].email_key, member=False))
            else:
                h = _hash_email("%s@mail.example" % K.hexid("nominee", key, aid, n=10))
                people.append(dict(kind="anon", account=None, hash=h, member=False))
        for pi, p in enumerate(people):
            pid = "%s-%d" % (key, pi)
            truth[pid] = dict(repo=key, member=p["member"], account=p.get("account"))
            subs = []
            if p["kind"] == "in":
                subs.append((p["account"], None))
            elif p["kind"] in ("out", "anon"):
                subs.append((None, p["hash"]))
            elif p["kind"] == "both":
                subs += [(p["account"], None), (None, p["hash"])]
            elif p["kind"] == "merged":
                subs += [(p["old"], None), (p["account"], None)]
                W.nominator_accounts.add(p["old"])
            ts = sorted(start + dt.timedelta(seconds=float(g.uniform(0, span))) for _ in subs)
            if p["kind"] == "merged":
                ts[1] = max(ts[1], ts[0] + dt.timedelta(days=float(g.uniform(2, 6))))
                ts[1] = min(ts[1], NOM_CLOSE - dt.timedelta(minutes=5))
            for (aid, h), t in zip(subs, ts):
                rows.append(dict(t=t, account=aid, hash=h, repo=key, pid=pid))
                if aid is not None:
                    W.nominator_accounts.add(aid)
            if g.random() < 0.06:
                aid, h = subs[0]
                rows.append(dict(t=ts[0] + dt.timedelta(seconds=float(g.uniform(3, 40))), account=aid, hash=h,
                                 repo=key, pid=pid))
    # nominations that name a fork of a shortlisted repository: the nominator copied the address of the fork they
    # had found (another owner, the same name)
    for key, plan in NOM_PLAN.items():
        r = W.by_name[key]
        g = K.rng("noms-fork", key)
        start = max(NOM_OPEN, K.to_amsterdam(r.public) + dt.timedelta(hours=30))
        for i in range(plan["forks"]):
            fowner = "%s%s" % (["ruben", "lotte", "mats", "yara", "joris", "elif", "kenji", "noor"][(i * 3 + len(key)) % 8],
                               ["bos", "vos", "smit", "kuip", "prins", "dekk"][(i + len(key)) % 6])
            t = start + dt.timedelta(seconds=float(g.uniform(0, (NOM_CLOSE - start).total_seconds())))
            pool = A.pool("regular", 110000)
            aid = pool[int(g.integers(len(pool)))]
            signed = g.random() < 0.5
            rows.append(dict(t=t, account=aid if signed else None,
                             hash=None if signed else _hash_email("f%s%d@mail.example" % (key, i)), repo=None,
                             ref=("https://%s/%s/%s" % (K.HOST, fowner, r.name)) if i % 2 == 0 else "%s/%s" % (fowner, r.name),
                             pid=None))
            if signed:
                W.nominator_accounts.add(aid)
    # nominations of repositories that did not make the shortlist
    g = K.rng("noms-other")
    others = []
    for i in range(57):
        owner = "%s%s" % (["kade", "brug", "dijk", "sloot", "haven", "polder", "werf", "molen", "veld", "duin"][i % 10],
                          ["labs", "dev", "works", "hq", "io", "tools"][(i * 7) % 6])
        nm = "%s%s" % (["swift", "tiny", "open", "micro", "quick", "safe", "plain", "deep", "sharp", "calm"][(i * 3) % 10],
                       ["rpc", "csv", "cron", "diff", "env", "grep", "json", "lsp", "orm", "sql"][(i * 11) % 10])
        others.append((owner, nm))
    for i, (owner, nm) in enumerate(others):
        for _ in range(1 + int(g.poisson(1.8))):
            t = NOM_OPEN + dt.timedelta(seconds=float(g.uniform(0, (NOM_CLOSE - NOM_OPEN).total_seconds())))
            if g.random() < 0.6:
                pool = A.pool("regular", 110000)
                aid = pool[int(g.integers(len(pool)))]
                rows.append(dict(t=t, account=aid, hash=None, repo=None, ref="%s/%s" % (owner, nm), pid=None))
                W.nominator_accounts.add(aid)
            else:
                rows.append(dict(t=t, account=None, hash=_hash_email("o%d-%d@mail.example" % (i, int(g.integers(1e6)))),
                                 repo=None, ref="https://%s/%s/%s" % (K.HOST, owner, nm), pid=None))
    rows.sort(key=lambda x: (x["t"], x["pid"] or "", x["account"] or 0))
    out = []
    for i, x in enumerate(rows):
        g2 = K.rng("ref", i)
        if x["repo"] is None:
            ref = x["ref"]
        else:
            r = W.by_name[x["repo"]]
            name = r.name
            if x["repo"] in K.RENAMED:
                old, when = K.RENAMED[x["repo"]]
                if x["t"] < K.to_amsterdam(when) or g2.random() < 0.05:
                    name = old
            ref = _ref(g2, r.owner, name)
        out.append([K.hexid("resp", i, n=10), x["t"].replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S"),
                    "yes" if x["account"] is not None else "no", x["account"] if x["account"] is not None else "",
                    x["hash"] or "", ref])
        x["row"] = out[-1]
    W.nomination_truth = truth
    W.nomination_rows = rows
    return out


def rename_rows(W):
    g = K.rng("renames")
    rows = []
    for key, (old, when) in K.RENAMED.items():
        r = W.by_name[key]
        rows.append([r.id, "%s/%s" % (r.owner, old), "%s/%s" % (r.owner, r.name), K.iso_z(when)])
    words = ["tern", "gull", "pike", "carp", "eel", "perch", "crane", "stork", "heron", "swift", "finch", "plover"]
    for i in range(13):
        rid = 600_000_000 + int(g.integers(0, 60_000_000))
        owner = "%s%s" % (words[i % 12], ["-dev", "labs", "-io", "hq"][i % 4])
        a = "%s-%s" % (words[(i * 5) % 12], ["kit", "cli", "db", "ui", "api"][i % 5])
        b = "%s%s" % (words[(i * 7 + 3) % 12], ["kit", "cli", "db", "ui", "api"][(i + 2) % 5])
        when = dt.datetime(2026, 1, 3) + dt.timedelta(days=float(g.uniform(0, 265)), seconds=float(g.uniform(0, 86400)))
        rows.append([rid, "%s/%s" % (owner, a), "%s/%s" % (owner, b), K.iso_z(when.replace(microsecond=0))])
    rows.sort(key=lambda x: x[3])
    return rows


# ---------------------------------------------------------------------------------------------------- distractors

REFERRERS = ["direct", "grachtwerk.dev", "search engines", "link forums", "social", "other"]


def traffic_rows(W):
    rows = []
    start = dt.date(2026, 8, 24)
    for r in W.october:
        g = K.rng("traffic", r.id)
        daily = {}
        for s in r.stars:
            if s.first and s.t <= K.CUT:
                daily.setdefault(s.t.date(), {}).setdefault(s.surface, 0)
                daily[s.t.date()][s.surface] += 1
        d = r.public.date()
        while d <= K.CUT_DATE:
            st = daily.get(d, {})
            internal = st.get("feed", 0) + st.get("explore", 0) + st.get("search", 0) * 0.4
            outside = st.get("repo_page", 0)
            mix = {"direct": 0.22 * outside + 3, "grachtwerk.dev": internal * 1.0 + 2,
                   "search engines": 0.18 * outside + st.get("search", 0) * 0.6 + 1,
                   "link forums": (0.55 if r.burst_kind == "forum" else 0.25) * outside,
                   "social": 0.12 * outside + 1, "other": 0.05 * outside + 1}
            for ref in REFERRERS:
                uv = int(g.poisson(max(0.5, mix[ref] * g.uniform(6.5, 9.5))))
                views = uv + int(g.poisson(uv * g.uniform(0.35, 0.8)))
                if uv or views:
                    rows.append([r.id, d.isoformat(), ref, views, uv])
            d += dt.timedelta(days=1)
    rows.sort(key=lambda x: (x[1], x[0], REFERRERS.index(x[2])))
    return rows


def trending_rows(W):
    """Grachtwerk's daily trending lists by language: the 25 repositories with the most stars that day."""
    rows = []
    g = K.rng("trending")
    langs = ["Go", "Python", "Rust", "TypeScript"]
    filler = {}
    for lang in langs:
        filler[lang] = []
        for i in range(140):
            owner = "%s%s" % (["amstel", "ij", "zaan", "vecht", "spaarne", "linge", "dommel", "berkel", "regge", "eem"][i % 10],
                              ["-labs", "dev", "-hq", "works", "-io", "code", "soft"][(i * 3) % 7])
            nm = "%s-%s" % (["fast", "lite", "nano", "hyper", "quiet", "bold", "lazy", "eager", "tidy", "busy"][(i * 7) % 10],
                            ["router", "cache", "parser", "queue", "logger", "shell", "store", "proxy", "grid", "form",
                             "auth", "sync", "chart", "table"][(i * 5 + len(lang)) % 14])
            filler[lang].append(("%s/%s" % (owner, nm), float(np.exp(g.normal(3.6, 0.9)))))
    by_lang = {}
    for r in W.october:
        by_lang.setdefault(r.language, []).append(r)
    d = dt.date(2026, 8, 24)
    while d <= K.CUT_DATE:
        for lang in langs:
            cands = []
            for name, level in filler[lang]:
                cands.append((name, int(g.poisson(level * g.uniform(0.5, 1.6)))))
            for r in by_lang.get(lang, []):
                n = sum(1 for s in r.stars if s.t.date() == d and s.first)
                if n:
                    cands.append(("%s/%s" % (r.owner, K.RENAMED[r.name][0] if r.name in K.RENAMED and
                                              dt.datetime.combine(d, dt.time(12)) < K.RENAMED[r.name][1] else r.name), n))
            cands.sort(key=lambda x: (-x[1], x[0]))
            for rank, (name, n) in enumerate(cands[:25], 1):
                rows.append([d.isoformat(), lang, rank, name, n])
        d += dt.timedelta(days=1)
    return rows
