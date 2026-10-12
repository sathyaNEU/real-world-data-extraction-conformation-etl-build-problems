"""The three supplemental measures for every airport, golden and the ladder stops a solver lands on: passengers
screened at the checkpoint over last summer's window, the hotel cost per officer-night of last summer's postings,
and the unit's expense claims per posting week. Computed from the generator's own records; verify.py recomputes the
goldens from the shipped files on its own path."""
import collections
import datetime as dt

import records as R
import sim as S
import world as W


def passengers_2026(world, how="golden"):
    """golden: passenger lanes and the unit's lanes; 'every lane' adds the staff and aircrew lanes; 'no unit' drops
    the unit's lanes."""
    out = {}
    for c in W.CODES:
        staff = set(S.staff_ids(c))
        tot = 0
        for (_, lane, d, i, n) in world["airports"][c]["lanes"]:
            if how == "golden" and lane in staff:
                continue
            if how == "no unit" and (lane in staff or lane in S.TEAM_IDS):
                continue
            tot += n
        out[c] = tot
    return out


def hotel_per_night(lines, posts, how="golden"):
    """golden: every invoice and credit-note line's amount over the officer-nights (each stay's nights once, net of
    credited nights). 'every line': nights summed over every line. 'no credit': the credit note dropped."""
    po_airport = {p["po"]: p["airport"] for p in posts}
    amt, nights = collections.defaultdict(float), collections.defaultdict(float)
    for x in lines:
        c = po_airport[x["po"]]
        credit = x["nights"] < 0
        if how == "no credit" and credit:
            continue
        amt[c] += x["amount"]
        if how == "every line" or x["line"] == 1:
            nights[c] += x["nights"]
    return {c: amt[c] / nights[c] for c in W.CODES}


def weeks_at(posts):
    k = collections.Counter(p["airport"] for p in posts)
    return {c: k[c] for c in W.CODES}


def week_airport(posts, d):
    for p in posts:
        if p["from"] <= d <= p["to"]:
            return p["airport"]
    return None


def claims_per_week(export_rows, posts, how="golden"):
    """golden: each claim line once (claim reference and line), each claim to the posting its days of subsistence
    fall in, over the airport's posting weeks. 'every row by date': the export as it stands, each line to the week
    its date falls in. 'dedup by date': lines once, but each to the week its date falls in. 'dedup on officer':
    rows dropped when officer, date, category and amount repeat, claims to their posting."""
    rows = export_rows
    if how in ("golden", "dedup by date"):
        seen, keep = set(), []
        for r in rows:
            k = (r["claim_ref"], r["line"])
            if k in seen:
                continue
            seen.add(k)
            keep.append(r)
        rows = keep
    elif how == "dedup on officer":
        seen, keep = set(), []
        for r in rows:
            k = (r["officer"], r["date"], r["category"], r["amount"])
            if k in seen:
                continue
            seen.add(k)
            keep.append(r)
        rows = keep
    claim_home = {}
    by_claim = collections.defaultdict(list)
    for r in rows:
        by_claim[r["claim_ref"]].append(r)
    for ref, rs in by_claim.items():
        subs = [r["date"] for r in rs if r["category"] == "SUBS-DAY"]
        claim_home[ref] = week_airport(posts, min(subs)) if subs else None
    tot = collections.defaultdict(float)
    for r in rows:
        if how in ("every row by date", "dedup by date"):
            c = week_airport(posts, r["date"])
        else:
            c = claim_home[r["claim_ref"]]
        if c is not None:
            tot[c] += r["amount"]
    wk = weeks_at(posts)
    return {c: tot[c] / wk[c] for c in W.CODES}
