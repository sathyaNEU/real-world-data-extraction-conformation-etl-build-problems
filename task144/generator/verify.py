"""Independent verifier for task144: reads only the bundle (target/) and the goldens, on its own code path (csv,
json, pyarrow, openpyxl; no pandas, no generator module but the calendar helpers), and recomputes the pick, every
candidate's expected stars, the default path and both asks."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import openpyxl
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

CUT = dt.datetime(2026, 9, 27, 23, 59, 59)


def rows(path, delim=","):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def utc_of_amsterdam_nine(d):
    """09:00 Amsterdam on day d in UTC: CEST (UTC+2) between the last Sundays of March and October, else UTC+1."""
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        while x.weekday() != 6:
            x -= dt.timedelta(days=1)
        return x
    summer = last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)
    return dt.datetime.combine(d, dt.time(9, 0)) - dt.timedelta(hours=2 if summer else 1)


def main(target, golden):
    p = lambda f: os.path.join(target, f)
    repos = {r["id"]: r for r in json.load(open(p(K.REPOS), encoding="utf-8"))}
    public = {i: dt.datetime.strptime(r["made_public_at"], "%Y-%m-%dT%H:%M:%SZ") for i, r in repos.items()}
    by_full = {r["full_name"]: i for i, r in repos.items()}
    wb = openpyxl.load_workbook(p(K.LOTTERY), data_only=True)
    issues = []
    r25 = list(wb["2025"].iter_rows(values_only=True))
    h = [i for i, r in enumerate(r25) if r and r[0] == "Issue"][0]
    for r in r25[h + 1:]:
        if r and r[0]:
            issues.append((r[0].date(), int(r[2]), [by_full[x] for x in r[3:10]], by_full[r[10]]))
    for r in list(wb["2026"].iter_rows(values_only=True))[1:]:
        if r and r[0]:
            issues.append((r[0].date(), int(r[2]), [int(x) for x in r[3:10]], int(r[10]) if r[10] else None))
    oct_row = [x for x in issues if x[0] == dt.date(2026, 10, 6)][0]
    past = [x for x in issues if x[3] is not None]
    t = pq.read_table(p(K.ACCOUNTS)).to_pydict()
    foll = dict(zip(t["account_id"], t["followers"]))
    atype = dict(zip(t["account_id"], t["account_type"]))
    mem = {}
    for r in rows(p(K.MEMBERS)):
        mem.setdefault((r["organization"], int(r["account_id"])), []).append(
            (dt.datetime.strptime(r["joined_at"], "%Y-%m-%dT%H:%M:%SZ"),
             dt.datetime.strptime(r["left_at"], "%Y-%m-%dT%H:%M:%SZ") if r["left_at"] else None))
    code = {r["v5_src"]: r["v6_surface"] for r in rows(p(K.CROSSWALK))}
    first = {}
    for r in rows(p(K.EV25)):
        if r["action"] == "star":
            key = (int(r["repo_id"]), int(r["actor_id"]))
            tt = dt.datetime(1970, 1, 1) + dt.timedelta(milliseconds=int(r["event_ts_ms"]))
            if key not in first or tt < first[key][0]:
                first[key] = (tt, code[r["src"]])
    for r in rows(p(K.EV26)):
        if r["event_type"] == "star.created":
            key = (int(r["repository_id"]), int(r["account_id"]))
            tt = dt.datetime.strptime(r["occurred_at"], "%Y-%m-%dT%H:%M:%SZ")
            if key not in first or tt < first[key][0]:
                first[key] = (tt, r["surface"])

    def org(rid):
        o = repos[rid]["owner"]
        return o["login"] if o["type"] == "Organization" else None

    def member(o, a, tt):
        return any(j <= tt and (l is None or tt < l) for j, l in mem.get((o, a), []))

    ext = {}
    for (rid, a), (tt, sf) in first.items():
        if atype.get(a) == "bot" or (org(rid) and member(org(rid), a, tt)):
            continue
        ext.setdefault(rid, []).append((tt, sf, a))
    roll = {}
    for r in rows(p(K.ROLLUP)):
        rid = int(r["repository_id"])
        kk = (dt.date.fromisoformat(r["day_utc"]) - public[rid].date()).days + 1
        roll.setdefault(rid, np.zeros(102))[kk] = int(r["external_first_stars"])
    runners = [x for row in past for x in row[2] if x != row[3] and public[x].date() + dt.timedelta(days=89) <= CUT.date()]

    def G(a):
        return sum(roll[x][a + 1:91].sum() for x in runners) / sum(roll[x][a - 6:a + 1].mean() for x in runners)
    nl = {rid: sum(1 for _, sf, _ in ext.get(rid, []) if sf == "newsletter") for rid in [x[3] for x in past]}
    rate = sum(nl[x[3]] for x in past) / sum(x[1] for x in past)
    D = rate * oct_row[1]
    spot_ids = {x[3] for x in past}
    fR = float(np.mean([foll[a] for (rid, a), (tt, sf) in first.items() if rid in spot_ids and sf == "newsletter"]))
    f2 = float(np.mean([foll[a] for (rid, a), (tt, sf) in first.items() if sf == "feed"]))
    res = {}
    for rid in oct_row[2]:
        a = (CUT.date() - public[rid].date()).days + 1
        d = np.zeros(102)
        for tt, sf, acc in ext[rid]:
            kk = (tt.date() - public[rid].date()).days + 1
            if 1 <= kk <= a:
                d[kk] += 1
        base = d[1:a + 1].sum() + d[a - 6:a + 1].mean() * G(a)
        mine = [(tt, sf, acc) for (r2, acc), (tt, sf) in first.items() if r2 == rid and tt <= CUT]
        late = [(tt, sf, acc) for tt, sf, acc in mine if (tt.date() - public[rid].date()).days + 1 >= 8]
        c = sum(1 for _, sf, _ in late if sf == "feed") / sum(foll[acc] for _, _, acc in late)
        c_life = sum(1 for _, sf, _ in mine if sf == "feed") / sum(foll[acc] for _, _, acc in mine)
        lift = D * (1 + c * fR / (1 - c * f2))
        lift_life = D * (1 + c_life * fR / (1 - c_life * f2))
        res[repos[rid]["name"]] = dict(base=base, lift=lift, total=base + lift, total_life=base + lift_life)
    pick = max(res, key=lambda n: res[n]["total"])
    life_pick = max(res, key=lambda n: res[n]["total_life"])
    # the default path: the lottery's average lift on each repository's own trajectory
    lifts, subs = [], []
    for x in past:
        rid = x[3]
        if public[rid].date() + dt.timedelta(days=89) > CUT.date():
            continue
        send = utc_of_amsterdam_nine(x[0])
        a = (send.date() - public[rid].date()).days
        d = roll[rid]
        base = d[1:a + 1].sum() + d[a - 6:a + 1].mean() * G(a)
        lifts.append(d[1:91].sum() - base)
        subs.append(x[1])
    Lbar = np.mean(lifts) * oct_row[1] / np.mean(subs)
    default = max(res, key=lambda n: res[n]["base"] + Lbar)
    # golden workbook and figures.json
    gb = openpyxl.load_workbook(os.path.join(golden, K.GOLD_BOOK), data_only=True)
    ws = gb["Spotlight"]
    ok_pick = ws["C4"].value.startswith(pick)
    ok_total = ws["C5"].value == K.round_to(res[pick]["total"], 1000) and ws["C6"].value == K.round_to(res[pick]["lift"], 1000)
    table = {}
    for r in ws.iter_rows(min_row=10, max_row=16, values_only=True):
        table[r[0]] = r[11]
    ok_table = all(table[n] == K.round_to(v["total"], 1000) for n, v in res.items())
    figs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(golden).rstrip("/")), "generator", "figures.json")))
    ok_figs = figs["call"]["pick"] == pick and figs["default_path"]["pick"] == default
    # Ask A
    lot = {x[0]: x for x in issues}
    sends = []
    for r in rows(p(K.PW_CAMP), ";"):
        when = dt.datetime.strptime(r["send_time"], "%d-%m-%Y %H:%M")
        sends.append(dict(id=r["campaign_id"], list=r["list"], date=when.date(), delivered=int(r["delivered"]), pw=True))
    for c in json.load(open(p(K.RM_CAMP), encoding="utf-8"))["campaigns"]:
        sends.append(dict(id=c["id"], list=c["audience"]["list"], date=dt.date.fromisoformat(c["sent_at"][:10]),
                          delivered=c["stats"]["delivered"], pw=False))
    # a reader's own clicks: a mail gateway fetches every link of a message as it is delivered, which Postwerk shows as
    # one click on every link of the send and Relaymark as four or more links within two seconds
    clicks = {}
    pwl = list(rows(p(K.PW_LINKS), ";"))
    labs_of = {}
    for r in pwl:
        labs_of.setdefault(r["campaign_id"], set()).add(r["link_label"])
    seen = {}
    for r in pwl:
        seen.setdefault((r["campaign_id"], r["subscriber_id"]), set()).add(r["link_label"])
    for r in pwl:
        n = int(r["clicks"]) - (1 if seen[(r["campaign_id"], r["subscriber_id"])] == labs_of[r["campaign_id"]] else 0)
        if n > 0:
            clicks.setdefault(r["campaign_id"], []).append((r["subscriber_id"], r["url"]))
    rml = {}
    for r in rows(p(K.RM_LINKS)):
        at = dt.datetime.fromisoformat(r["clicked_at"].replace("Z", "+00:00")).timestamp()
        rml.setdefault((r["campaign_id"], r["subscriber_id"]), []).append((at, r["link_tag"], r["url"]))
    for (cid, sub), xs in rml.items():
        xs.sort()
        fetched = set()
        lo = 0
        for hi in range(len(xs)):
            while xs[hi][0] - xs[lo][0] > 2:
                lo += 1
            if len({x[1] for x in xs[lo:hi + 1]}) >= 4:
                fetched.update(range(lo, hi + 1))
        for i, (at, tag, url) in enumerate(xs):
            if i not in fetched:
                clicks.setdefault(cid, []).append((sub, url))
    ask_a = {}
    for m in range(4, 10):
        issue = K.first_tuesday(2026, m)
        path = repos[lot[issue][3]]["full_name"].lower()
        mine = [s for s in sends if s["list"] == "Sluis" and s["date"].month == m and s["date"].year == 2026]
        delivered = sum(s["delivered"] for s in mine if s["date"] == issue)
        who = set()
        for cid in {s["id"] for s in mine}:
            for sub, url in clicks.get(cid, []):
                # a link reaches the repository by its owner/name or by the host's permanent address for its id
                byid = re.match(r"https?://[^/]+/repositories/(\d+)", url)
                mm = re.match(r"https?://[^/]+/([^/?#]+)/([^/?#]+)", url)
                if (byid and int(byid.group(1)) == lot[issue][3]) or \
                        (mm and ("%s/%s" % (mm.group(1), mm.group(2))).lower() == path):
                    who.add(sub)
        ask_a[m] = (delivered, len(who), round(100.0 * len(who) / delivered + 1e-12, 2))
    s2 = gb["Sluis issues"]
    ok_a = all((r[3], r[4], r[5]) == ask_a[i + 4] for i, r in enumerate(s2.iter_rows(min_row=5, max_row=10, values_only=True)))
    # Ask B
    hashes = {hsh: a for a, hsh in zip(t["account_id"], t["primary_email_sha256"]) if hsh}
    # a signed-in response records the address the account had then, which the snapshot may no longer show
    for r in rows(p(K.NOMS)):
        if r["account_id"] and r["email_sha256"]:
            hashes.setdefault(r["email_sha256"], int(r["account_id"]))
    merged = {a: m for a, m in zip(t["account_id"], t["merged_into"]) if m is not None}
    ren = {r["old_full_name"].lower(): r["new_full_name"].lower() for r in rows(p(K.RENAMES))}
    short = {repos[i]["full_name"].lower(): i for i in oct_row[2]}
    names = {repos[i]["name"].lower(): i for i in oct_row[2]}
    for o, n in ren.items():
        if n in short:
            names.setdefault(o.split("/")[1], short[n])
    ppl = {i: {} for i in oct_row[2]}
    for r in rows(p(K.NOMS)):
        ref = re.sub(r"^https?://", "", r["repository"].strip(), flags=re.I)
        ref = re.sub(r"^(www\.)?grachtwerk\.dev/", "", ref, flags=re.I).strip("/").lower()
        ref = ref[:-4] if ref.endswith(".git") else ref
        ref = ren.get(ref, ref)
        rid = short.get(ref) if "/" in ref else names.get(ref)
        if rid is None:
            continue
        if r["account_id"]:
            a = int(r["account_id"])
        elif r["email_sha256"] in hashes:
            a = hashes[r["email_sha256"]]
        else:
            a = None
        while a in merged:
            a = merged[a]
        key = ("a", a) if a is not None else ("h", r["email_sha256"])
        when = dt.datetime.fromisoformat(r["submitted_at"])
        ppl[rid].setdefault(key, []).append((when - when.utcoffset()).replace(tzinfo=None))
    # a person is a member while any of their accounts is: the accounts later merged into the one they used count
    folded = {}
    for a in merged:
        b = a
        while b in merged:
            b = merged[b]
        folded.setdefault(b, set()).add(a)
    ask_b = {}
    for rid, pp in ppl.items():
        o = org(rid)
        inside = sum(1 for key, ts in pp.items() if o and key[0] == "a"
                     and any(member(o, a, x) for a in {key[1]} | folded.get(key[1], set()) for x in ts))
        ask_b[repos[rid]["name"]] = (len(pp), round(100.0 * (len(pp) - inside) / len(pp) + 1e-12, 2) if o else None)
    s3 = gb["Nominations"]
    ok_b = all((r[2], r[4] if ask_b[r[0]][1] is not None else None) == ask_b[r[0]]
               for r in s3.iter_rows(min_row=5, max_row=11, values_only=True))
    print("verify: pick %s at %.0f (adds %.0f); runner-up %s; default path %s; whole-life rate %s; "
          "workbook %s, table %s, figures.json %s, Ask A %s, Ask B %s" % (
              pick, res[pick]["total"], res[pick]["lift"], sorted(res, key=lambda n: -res[n]["total"])[1], default,
              life_pick, ok_pick and ok_total, ok_table, ok_figs, ok_a, ok_b))
    if not (ok_pick and ok_total and ok_table and ok_figs and ok_a and ok_b and pick == "kilnkit" and default == "tracewire"
            and life_pick == "slidewell"):
        raise SystemExit("verify failed")
    return res


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    main(os.path.join(task, "target"), os.path.join(task, "golden"))
