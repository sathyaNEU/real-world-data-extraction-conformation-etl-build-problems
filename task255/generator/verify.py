"""An independent recomputation of every graded figure from the shipped files, on its own code path (pandas for the
tables, its own PDF stream decoder, its own routing and its own reading of the service pattern), compared with
generator/figures.json.

    python3 task255/generator/verify.py [target_dir]
"""
import base64
import collections
import datetime as dt
import json
import math
import os
import re
import sys
import zlib

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OK = []


def say(label, ok, detail=""):
    OK.append(ok)
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))


# ---------------------------------------------------------------------- PDF text, decoded here
def pdf_strings(path):
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<((?:(?!<<).)*?)>>\s*stream\r?\n(.*?)\s*endstream", raw, re.S):
        head, body = m.group(1), m.group(2)
        if b"ASCII85Decode" in head:
            body = body.strip()
            if body.startswith(b"<~"):
                body = body[2:]
            if body.endswith(b"~>"):
                body = body[:-2]
            body = base64.a85decode(re.sub(rb"\s", b"", body))
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        for s in re.finditer(rb"\((.*?)(?<!\\)\)\s*Tj", body, re.S):
            t = s.group(1)
            t = re.sub(rb"\\([0-7]{3})", lambda x: bytes([int(x.group(1), 8)]), t)
            t = t.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\")
            out.append(t.decode("latin-1"))
    return "\n".join(out)


def num_nl(s):
    return float(str(s).replace(".", "").replace(",", "."))


# ---------------------------------------------------------------------- the main call
def minutes(s):
    h, m, sec = (int(x) for x in str(s).split(":"))
    return h * 60 + m + sec / 60.0


def verify_main(target, fig):
    X = os.path.join(target, "RVB_metronet_planningsmodel_2026.xlsx")
    stops = pd.read_excel(X, "Stops")
    runs = pd.read_excel(X, "Run times")
    halls = pd.read_excel(X, "Halls").set_index("hall_code")
    inter = pd.read_excel(X, "Interchanges").set_index("stop_code")
    gates = pd.read_excel(X, "Gates").set_index("gate_code")["hall_code"].to_dict()
    freq = pd.read_excel(X, "Frequencies")
    seq = collections.defaultdict(list)
    run = {}
    for _, x in runs.iterrows():
        if not seq[x.line]:
            seq[x.line].append(x.from_stop)
        seq[x.line].append(x.to_stop)
        run[(x.line, x.from_stop, x.to_stop)] = run[(x.line, x.to_stop, x.from_stop)] = float(x.run_min)
    lines_of = {s: [l for l in seq if s in seq[l]] for s in stops.stop_code}
    side = {}
    for s in stops.stop_code:
        if s == "CEN":
            side[s] = "C"
        elif s in seq["M1"]:
            side[s] = "N" if seq["M1"].index(s) < seq["M1"].index("CEN") else "S"
        elif s in seq["M2"]:
            side[s] = "W" if seq["M2"].index(s) < seq["M2"].index("CEN") else "E"
        else:
            side[s] = "R"

    def rt(l, a, b):
        i, j = seq[l].index(a), seq[l].index(b)
        st = 1 if j > i else -1
        return sum(run[(l, seq[l][k], seq[l][k + st])] for k in range(i, j, st))

    # fewest changes, then the shortest time (a breadth-first search over line changes)
    cache = {}

    def path(o, d):
        if (o, d) in cache:
            return cache[(o, d)]
        best = None
        frontier = [(0.0, [(l, o)]) for l in lines_of[o]]
        for _changes in range(3):
            found = []
            nxt = []
            for t, p in frontier:
                l, a = p[-1]
                for b in seq[l]:
                    if b == a:
                        continue
                    tt = t + rt(l, a, b)
                    if b == d:
                        found.append((tt, p + [(None, b)]))
                    for l2 in lines_of[b]:
                        if l2 != l and b in inter.index:
                            nxt.append((tt + float(inter.loc[b, "walk_min"]), p + [(l2, b)]))
            if found:
                best = min(found, key=lambda x: x[0])[1]
                break
            frontier = nxt
        legs = [(best[k][0], best[k][1], best[k + 1][1]) for k in range(len(best) - 1)]
        cache[(o, d)] = legs
        return legs

    J = pd.read_csv(os.path.join(target, "RVB_metro_ritten_20261001_20261104.csv"), dtype=str, keep_default_na=False)
    prod = pd.read_csv(os.path.join(target, "RVB_productcodes.csv"), dtype=str)
    passenger = set(prod[prod.card_class == "reiziger"].product_code)
    J["d"] = pd.to_datetime(J.travel_date).dt.date
    W = J[(J.d >= dt.date(2026, 10, 5)) & (J.d <= dt.date(2026, 11, 1)) & J.product_code.isin(passenger)]
    wk = W.groupby("card_id")["d"].apply(lambda s: len({x.isocalendar()[1] for x in s}))
    regular = set(wk[wk == 4].index)

    def headway(day, m):
        tag = "ma-vr" if day.weekday() < 5 else ("za" if day.weekday() == 5 else "zo")
        for _, f in freq[(freq.line == "M1") & (freq.days == tag)].iterrows():
            a, b = minutes(f["from"] + ":00"), minutes(f["to"] + ":00")
            if b <= a:
                b += 1440
            if a <= m < b:
                return 60.0 / f.trains_per_hour
        return 10.0

    service = {"N": "A", "E": "A", "W": "B", "S": "B"}
    line = {"N": "M1", "S": "M1", "W": "M2", "E": "M2"}
    # the service pattern: read from the clean three-minute hours, by the ten-minute bin of the minute at Centraal
    probe = collections.defaultdict(lambda: [0, 0])
    rows = []
    for x in W[W.card_id.isin(regular)].itertuples():
        legs = path(x.check_in_stop, x.check_out_stop) if x.check_out_stop else None
        rows.append((x, legs))
        if not legs or x.d.weekday() >= 5:
            continue
        if len(legs) not in (1, 2) or any(l == "M3" for l, a, b in legs):
            continue
        u, v = legs[0][1], legs[-1][2]
        pair = {side[u], side[v]}
        if pair not in ({"N", "E"}, {"N", "S"}):
            continue
        lu, lv = line[side[u]], line[side[v]]
        t1, t2 = minutes(x.check_in_time), minutes(x.check_out_time)
        if headway(x.d, t1) > 3.0:
            continue
        dur = (t2 - t1) % 1440
        base = float(halls.loc[gates[x.check_in_gate], "walk_to_%s_min" % lu]) + rt(lu, u, "CEN") + rt(lv, "CEN", v) + \
            float(halls.loc[gates[x.check_out_gate], "walk_to_%s_min" % lv])
        changed = dur - base > 5.0
        line_map_fails = (not changed) if pair == {"N", "E"} else changed
        at_cen = t1 + float(halls.loc[gates[x.check_in_gate], "walk_to_%s_min" % lu]) + 1.5 + rt(lu, u, "CEN")
        probe[int(at_cen // 10)][1 if line_map_fails else 0] += 1
    peak_bins = {b for b, (holds, fails) in probe.items() if holds + fails >= 8 and fails > holds}   # the line map fails
    windows = sorted(peak_bins)
    say("the service pattern read from the three-minute hours: two windows of departures through Centraal",
        bool(windows), "%s" % ", ".join("%02d:%d0" % (b // 6, b % 6) for b in windows))

    passes = collections.Counter()
    for x, legs in rows:
        passes[(x.card_id, gates[x.check_in_gate])] += 1
        if not legs:
            continue
        passes[(x.card_id, gates[x.check_out_gate])] += 1
        # group the legs into movements; a line-map change at Centraal between M1 and M2 sits inside one movement
        mv, k = [], 0
        while k < len(legs):
            l, a, b = legs[k]
            if l in ("M1", "M2") and b == "CEN" and k + 1 < len(legs) and legs[k + 1][0] in ("M1", "M2") and \
                    legs[k + 1][0] != l:
                mv.append(("MM", a, legs[k + 1][2]))
                k += 2
            else:
                mv.append(("MM" if l != "M3" else "M3", a, b))
                k += 1
        t = minutes(x.check_in_time)
        first = legs[0][0]
        t += float(halls.loc[gates[x.check_in_gate], "walk_to_%s_min" % first]) + 1.5
        for i, (kind, a, b) in enumerate(mv):
            if i > 0:
                passes[(x.card_id, inter.loc[a, "passage_code"])] += 1
                t += float(inter.loc[a, "walk_min"]) + 3.0
            if kind == "MM" and side[a] in "NSWE" and side[b] in "NSWE" and side[a] != side[b]:
                at = t + rt(line[side[a]], a, "CEN")
                peak = x.d.weekday() < 5 and int((at % 1440) // 10) in peak_bins
                change = service[side[a]] != service[side[b]] if peak else line[side[a]] != line[side[b]]
                if change:
                    passes[(x.card_id, "CEN-OV")] += 1
                t = at + (6.5 if change else 0.5) + rt(line[side[b]], "CEN", b)
            elif kind == "M3":
                t += rt("M3", a, b)
            else:
                t += rt([l for l in ("M1", "M2") if a in seq[l] and b in seq[l]][0], a, b)
    rc = pdf_strings(os.path.join(target, "Spoorbeeld_tariefkaart_2027.pdf"))
    annex = rc[rc.index("Annex A"):]
    pk = {}
    for m in re.finditer(r"([A-Z][a-z]+)\s*\n?\s*([A-Z]{3})\s*\n?\s*((?:[A-Z]{3}-(?:HN|HZ|OV|H)\s*\([^)]*\);?\s*)+)", annex):
        pk[m.group(1)] = set(re.findall(r"([A-Z]{3}-(?:HN|HZ|OV|H))\s*\(", m.group(3)))
    reach = {}
    for name, places in pk.items():
        n = sum(1 for c in regular if sum(passes[(c, p)] for p in places) >= 3)
        reach[name] = 100.0 * n / len(regular)
    got = {k: int(math.floor(v + 0.5)) for k, v in reach.items()}
    say("every package's reach to the whole per cent", got == fig["reach"],
        "; ".join("%s %d/%d" % (k, got.get(k, -1), fig["reach"][k]) for k in fig["reach"]))
    tier = sorted(k for k, v in reach.items() if v >= 40.0)
    say("the Tier G call", tier == sorted(fig["call"]), ", ".join(tier))
    say("the regular riders", len(regular) == fig["regular_riders"], "%d" % len(regular))


# ---------------------------------------------------------------------- make-good
def verify_make_good(target, fig):
    R = os.path.join(target, "schermregister_2026-11-12.xlsx")
    scr = pd.read_excel(R, "Schermen", dtype=str).fillna("")
    cab = pd.read_excel(R, "Bekabeling", dtype=str).fillna("")
    cms = pd.read_csv(os.path.join(target, "cms_player_status_20261001_20261104.csv"), dtype=str, keep_default_na=False)
    B = os.path.join(target, "boekingen_najaar_2026.xlsx")
    bk = pd.read_excel(B, "Boekingen", dtype=str)
    lines = pd.read_excel(B, "Geboekte schermen", dtype=str)

    def local(s):
        t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:00Z")
        return t + dt.timedelta(hours=2 if t < dt.datetime(2026, 10, 25, 1) else 1)
    cms["t"] = cms.event_time_utc.map(local)
    cms = cms.sort_values(["player_id", "t"])
    off = collections.defaultdict(list)
    for p, g in cms.groupby("player_id"):
        cur = None
        for x in g.itertuples():
            if x.event == "OFFLINE" and cur is None:
                cur = x.t
            elif x.event == "ONLINE" and cur is not None:
                off[p].append((cur, x.t))
                cur = None
        if cur is not None:
            off[p].append((cur, dt.datetime(2027, 1, 1)))
    dead = {p for p, v in off.items() if v and v[-1][1] == dt.datetime(2027, 1, 1)}
    conns = collections.defaultdict(list)
    for x in cab.itertuples():
        a = dt.datetime.strptime(x.connected_from, "%Y-%m-%d %H:%M")
        b = dt.datetime.strptime(x.connected_to, "%Y-%m-%d %H:%M") if x.connected_to else dt.datetime(2027, 1, 1)
        conns[x.asset_tag].append([x.player_id, a, b])
    # a move off a dead player: the receiving player's first report of its new display count dates it
    moves = collections.defaultdict(list)
    for tag, cs in conns.items():
        cs.sort(key=lambda c: c[1])
        for c0, c1 in zip(cs, cs[1:]):
            if c0[0] in dead and c0[2] == c1[1]:
                moves[(c0[0], c1[0], c1[1])].append(tag)
    for (p0, p1, when), tags in moves.items():
        n_before = sum(1 for t, cs in conns.items() if t not in tags for c in cs if c[0] == p1 and c[1] < when <= c[2])
        died = off[p0][-1][0]
        ev = cms[(cms.player_id == p1) & (cms.displays != "") & (cms.t >= died) & (cms.t <= when)]
        hit = ev[ev.displays.astype(int) == n_before + len(tags)]
        real = hit.t.iloc[0] if len(hit) else when
        for tag in tags:
            for c in conns[tag]:
                if c[0] == p0 and c[2] == when:
                    c[2] = real
                if c[0] == p1 and c[1] == when:
                    c[1] = real
    down = {}
    for x in scr.itertuples():
        if x.taken_down:
            d = dt.date.fromisoformat(x.taken_down[:10])
            ps = {c[0] for c in conns[x.asset_tag]}
            z = cms[cms.player_id.isin(ps) & (cms.event == "DISPLAYS") & (cms.displays == "0")]
            z = z[z.t.map(lambda t: t.date() == d)]
            first = {5: dt.time(6, 30), 6: dt.time(7, 0)}.get(d.weekday(), dt.time(5, 45))
            down[x.asset_tag] = min(z.t) if len(z) else dt.datetime.combine(d, first)
    out = {}
    for b in bk.itertuples():
        f0, f1 = dt.date.fromisoformat(b.flight_start[:10]), dt.date.fromisoformat(b.flight_end[:10])
        tags = list(lines[lines.booking_ref == b.booking_ref].asset_tag)
        dark = 0.0
        for tag in tags:
            day = f0
            while day <= f1:
                start = {5: dt.time(6, 30), 6: dt.time(7, 0)}.get(day.weekday(), dt.time(5, 45))
                o0, o1 = dt.datetime.combine(day, start), dt.datetime.combine(day + dt.timedelta(days=1), dt.time(0, 30))
                if down.get(tag) and down[tag] < o1:
                    dark += (o1 - max(o0, down[tag])).total_seconds() / 3600
                    o1 = max(o0, down[tag])
                for p, a, c in conns[tag]:
                    for s0, s1 in off[p]:
                        lo, hi = max(o0, a, s0), min(o1, c, s1)
                        if lo < hi:
                            dark += (hi - lo).total_seconds() / 3600
                day += dt.timedelta(days=1)
        x = dark - 0.005 * float(b.booked_screen_hours)
        out[b.booking_ref] = math.ceil(round(x, 6)) if x > 0 else 0
    say("make-good hours for every autumn booking", out == fig["make_good_hours"],
        "; ".join("%s %d/%d" % (k, out[k], fig["make_good_hours"][k]) for k in out))


# ---------------------------------------------------------------------- screens on sale on 1 January 2027
def verify_screens(target, fig):
    R = os.path.join(target, "schermregister_2026-11-12.xlsx")
    s = pd.read_excel(R, "Schermen", dtype=str).fillna("")
    s["h"] = s.hung.str[:10]
    s = s[s.h <= "2027-01-01"]
    s = s.sort_values(["h", "asset_tag"]).groupby("asset_tag").tail(1)            # a tag stands where it was last hung
    s = s[(s.taken_down == "") | (s.taken_down.str[:10] > "2027-01-01")]
    s = s.sort_values("h").groupby(["location_code", "position"]).tail(1)            # one screen to a position
    rc = pdf_strings(os.path.join(target, "Spoorbeeld_tariefkaart_2027.pdf"))
    names = dict(re.findall(r"([A-Z][a-z]+)\s*\n?\s*([A-Z]{3})\s*\n?\s*[A-Z]{3}-", rc[rc.index("Annex A"):]))
    cnt = s[s.package != "-"].package.value_counts().to_dict()
    got = {n: int(cnt.get(c, 0)) for n, c in names.items()}
    say("screens on sale on 1 January 2027 by package", got == fig["screens_on_sale_2027"],
        "; ".join("%s %d/%d" % (k, got[k], fig["screens_on_sale_2027"][k]) for k in got))


# ---------------------------------------------------------------------- net revenue
def verify_revenue(target, fig):
    L = pd.read_csv(os.path.join(target, "facturen_oud_systeem_2026.csv"), sep=";", dtype=str)
    inv = {x.factuurnummer: (x.boekingsnummer, round(num_nl(x.bedrag_incl_btw) / 1.21, 2)) for x in L.itertuples()}
    D = pd.read_excel(os.path.join(target, "billing_export_2026-10-15_2026-11-12.xlsx"), "Documents", dtype=str).fillna("")
    for x in D[D.document_type == "invoice"].itertuples():
        inv[x.document_no] = (x.booking_ref, float(x.net_eur))
    B = pd.read_excel(os.path.join(target, "boekingen_najaar_2026.xlsx"), "Boekingen", dtype=str).fillna("")
    value = collections.Counter()
    for no, (ref, v) in inv.items():
        value[ref] += v
    credits = collections.defaultdict(list)
    for x in D[D.document_type == "credit note"].itertuples():
        if x.reference in inv:
            credits[inv[x.reference][0]].append((x.document_date[:10], float(x.net_eur)))
    st = pdf_strings(os.path.join(target, "bureaucommissie_najaar_2026.pdf"))
    comm = {}
    for m in re.finditer(r"([A-Za-z ]+) \xb7 Commissienota.*?datum (\d+) oktober 2026.*?\((SB-[^)]*)\).*?najaarsboekingen 2026\s+([\d.,]+)",
                         st, re.S):
        refs = [r.strip() for r in m.group(3).split(",")]
        sdate = "2026-10-%02d" % int(m.group(2))
        base = sum(value[r] + sum(a for d, a in credits[r] if d <= sdate) for r in refs)
        rate = num_nl(m.group(4)) / base
        for r in refs:
            comm[r] = rate * (value[r] + sum(a for d, a in credits[r]))
    rc = pdf_strings(os.path.join(target, "Spoorbeeld_tariefkaart_2027.pdf"))
    out = collections.Counter()
    for x in B.itertuples():
        out[x.package] += value[x.booking_ref] + sum(a for d, a in credits[x.booking_ref]) - comm.get(x.booking_ref, 0.0)
    got = {k: int(math.floor(v / 10.0 + 0.5)) * 10 for k, v in out.items()}
    want = fig["net_revenue_eur"]
    say("net revenue per package to the nearest 10 euros", all(got.get(k) == v for k, v in want.items()),
        "; ".join("%s %s/%d" % (k, got.get(k), v) for k, v in want.items()))


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    verify_main(target, fig)
    verify_make_good(target, fig)
    verify_screens(target, fig)
    verify_revenue(target, fig)
    print("verify: %d of %d blocks pass" % (sum(OK), len(OK)))
    return all(OK)


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")) else 1)
