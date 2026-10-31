"""The independent verifier: reads only the shipped bundle (target/) with its own code path (pandas, a sorted merge on
terminal, amount and time, a label-propagation pass for the homes, its own counter matcher and funding sum) and checks
every graded figure in figures.json. It reads back every format the pack ships and each document a figure leans on.

    python3 task268/generator/verify.py [target_dir] [figures.json]"""
import collections
import datetime as dt
import itertools
import json
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

IRISH = "Europe/Dublin"


def brand_key(s):
    s = re.sub(r"[^A-Z ]", "", s.upper().replace("'", ""))
    return " ".join(w for w in s.split() if w not in ("COFFEE", "ROASTERS", "CAFFE", "KAFFE"))


NAMES = {"CORCALLYS ROASTERY": "Corcally's Roastery", "HALLORANS": "Halloran's", "BELLVALE": "Bellvale",
         "NORDHAVN": "Nordhavn", "ORO ROSSO": "Oro Rosso", "CAFETTO": "Cafetto", "WESTQUAY": "Westquay",
         "KINVARA HILLS": "Kinvara Hills"}


def load(T):
    p = lambda k: os.path.join(T, K.FILES[k])
    master = pd.read_excel(p("master"), dtype={"PLU": str})
    packs = master[master["Sub-category"].isin(["Ground", "Beans", "Capsules", "Instant"])]
    brand = {r.PLU: NAMES[brand_key(r.Brand)] for r in packs.itertuples()}
    price = {r.PLU: float(r._6) for r in packs.itertuples()}
    till = pd.read_csv(p("till"), dtype={"plu": str, "receipt": str, "rewards_card": str, "note": str, "promo": str})
    till["when"] = pd.to_datetime(till["txn_time"])
    reg = pd.read_csv(p("register"), dtype=str)
    settle = pd.read_parquet(p("settle"))
    online = json.load(open(p("online"), encoding="utf-8"))
    return dict(brand=brand, price=price, till=till, reg=reg, settle=settle, online=online, T=T)


def homes(D):
    till, reg, settle, brand = D["till"], D["reg"], D["settle"], D["brand"]
    store = set(reg.loc[reg.card_type == "STORE", "card_no"])
    succ = dict(zip(reg.loc[reg.replaced_by.notna(), "card_no"], reg.loc[reg.replaced_by.notna(), "replaced_by"]))

    def fold(c):
        while c in succ:
            c = succ[c]
        return c
    rc = till[["store", "till", "receipt", "when", "rewards_card", "card_amount"]].drop_duplicates(
        ["store", "till", "receipt", "when"])
    rc = rc[(rc.card_amount > 0)].copy()

    def tid(r):
        if (r.store, r.till) == ("LSG", 2):
            return "41023202" if r.when < pd.Timestamp(K.SWAP_DATE) else "41023212"
        return {"DRM": "410231", "LSG": "410232", "KBN": "410233"}[r.store] + "%02d" % r.till
    rc["terminal_id"] = [tid(r) for r in rc.itertuples()]
    rc["utc"] = rc["when"].dt.tz_localize(IRISH).dt.tz_convert("UTC").dt.tz_localize(None)
    rc["amount"] = rc["card_amount"].round(2)
    st = settle[(settle.txn_type == "SALE") & (~settle.terminal_id.isin([K.WEB_TID, K.COUNTER_TID]))].copy()
    st["utc"] = st["txn_time_utc"].dt.tz_localize(None)
    st["amount"] = st["amount"].round(2)
    m = rc.merge(st[["terminal_id", "amount", "utc", "card_ref"]], on=["terminal_id", "amount"], suffixes=("", "_s"))
    m = m[(m.utc_s <= m.utc + pd.Timedelta(seconds=5)) & (m.utc_s >= m.utc - pd.Timedelta(seconds=120))]
    counts = m.groupby(["store", "till", "receipt", "when"]).size()
    assert counts.max() == 1, "a receipt matched twice"
    edges = []
    for r in m.itertuples():
        c = r.rewards_card
        if isinstance(c, str) and c and c not in store:
            edges.append((r.card_ref, "C" + fold(c)))
    web = settle[(settle.terminal_id == K.WEB_TID) & settle.merchant_ref.notna()]
    webref = dict(zip(web.merchant_ref, web.card_ref))
    orders = []
    for o in D["online"]["orders"]:
        if o["status"] != "delivered" or not (o["delivered_on"] or "").startswith(str(K.YEAR)):
            continue
        bs = {brand[ln["sku"]] for ln in o["versions"][-1]["coffee_lines"] if ln["sku"] in brand}
        if bs:
            orders.append(("A" + o["account"], bs))
            if o["order"] in webref:
                edges.append((webref[o["order"]], "A" + o["account"]))
    # label propagation over the bipartite graph of card references and nodes
    nbr = collections.defaultdict(set)
    for ref, nd in edges:
        nbr["R" + ref].add(nd)
        nbr[nd].add("R" + ref)
    label = {}
    for start in sorted(nbr):
        if start in label:
            continue
        stack, comp = [start], []
        label[start] = start
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in nbr[x]:
                if y not in label:
                    label[y] = start
                    stack.append(y)
    buys = collections.defaultdict(set)
    lines = till[till.plu.isin(brand.keys()) & (till.qty > 0) & till.rewards_card.notna()]
    for r in lines.itertuples():
        if r.rewards_card in store:
            continue
        nd = "C" + fold(r.rewards_card)
        buys[label.get(nd, nd)].add(brand[r.plu])
    for nd, bs in orders:
        buys[label.get(nd, nd)] |= bs
    return list(buys.values()), len(m)


def shares(units):
    out = {}
    for b in [x[1] for x in K.BRANDS[1:]]:
        buyers = [s for s in units if b in s]
        both = sum(1 for s in buyers if "Corcally's Roastery" in s)
        out[b] = (len(buyers), both, 100.0 * both / len(buyers))
    return out


def counter(D):
    """Labels sold: each counter card payment as labels printed shortly before plus accessories, each counter till
    line as one label of its price; scale 2's block of back-dated labels moved by the offset its payments show."""
    labs = pd.read_csv(os.path.join(D["T"], K.FILES["labels"]))
    labs["kg"] = [w / 1000.0 if s == "S2" else w for s, w in zip(labs.scale, labs.net_weight)]
    labs["when"] = pd.to_datetime(labs.printed)
    labs["no"] = labs.label.str.split("-").str[1].astype(int)
    st = D["settle"]
    pays = st[(st.terminal_id == K.COUNTER_TID) & (st.txn_type == "SALE")].copy()
    pays["when"] = pays["txn_time_utc"].dt.tz_convert(IRISH).dt.tz_localize(None)
    pays = pays.sort_values("when")
    # the back-dated block: scale 2 labels whose time runs backwards against their numbers
    s2 = labs[labs.scale == "S2"].sort_values("no")
    jump = s2.when.diff() < pd.Timedelta(days=-2)
    back = s2.when.diff() > pd.Timedelta(days=20)
    i0 = s2.index[jump.values][0]
    i1 = s2.index[back.values][0]
    pos0, pos1 = list(s2.index).index(i0), list(s2.index).index(i1)
    block = s2.iloc[pos0:pos1]
    amt = collections.defaultdict(list)
    for r in pays.itertuples():
        amt[round(r.amount, 2)].append(r.when)
    diffs = sorted((pw - r.when).total_seconds() for r in block.itertuples() for pw in amt.get(round(r.label_price, 2), [])
                   if 86400 < (pw - r.when).total_seconds() < 366 * 86400)
    best, lo = 0, 0
    j = 0
    for i in range(len(diffs)):
        while diffs[i] - diffs[j] > 600:
            j += 1
        if i - j + 1 > best:
            best, lo = i - j + 1, j
    core = diffs[lo:lo + best]
    off = core[len(core) // 2] - 100
    labs.loc[block.index, "when"] = labs.loc[block.index, "when"] + pd.Timedelta(seconds=off)
    labs = labs.sort_values("when").reset_index(drop=True)
    acc = {0} | {int(round(a * 100)) for _, a in K.ACCESSORIES} | \
        {int(round((a + b) * 100)) for (_, a), (_, b) in itertools.combinations_with_replacement(K.ACCESSORIES, 2)}
    cents = [int(round(x * 100)) for x in labs.label_price]
    times = list(labs.when)
    import bisect
    used, sold = set(), set()
    for r in pays.itertuples():
        a0 = bisect.bisect_left(times, r.when - pd.Timedelta(minutes=25))
        a1 = bisect.bisect_right(times, r.when + pd.Timedelta(minutes=3))
        cand = [i for i in range(a0, a1) if i not in used]
        target = int(round(r.amount * 100))
        hit = None
        for k in (1, 2, 3):
            for comb in itertools.combinations(cand, k):
                if target - sum(cents[i] for i in comb) in acc:
                    hit = comb
                    break
            if hit:
                break
        if hit:
            used |= set(hit)
            sold |= set(hit)
    till = D["till"]
    cl = till[till.plu == K.COUNTER_PLU].sort_values("when")
    for r in cl.itertuples():
        a0 = bisect.bisect_left(times, r.when - pd.Timedelta(minutes=150))
        a1 = bisect.bisect_right(times, r.when + pd.Timedelta(minutes=1))
        cand = [i for i in range(a0, a1) if i not in used and cents[i] == int(round(r.value * 100))]
        if cand:
            used.add(cand[-1])
            sold.add(cand[-1])
    out = collections.defaultdict(float)
    for i in sold:
        out["%s Q%d" % (labs.roaster[i], (labs.when[i].month - 1) // 3 + 1)] += labs.kg[i]
    return {k: round(v, 1) for k, v in out.items()}


def funding(D):
    deals = pd.read_excel(os.path.join(D["T"], K.FILES["deals"]), sheet_name="Deal log 2026")
    info = {}
    for r in deals.itertuples(index=False):
        d = info.setdefault(r[0], dict(supplier=r[1], plus=set(str(r[3]).split(", ")), start=r[5].date(), end=r[6].date(),
                                       price=float(str(r[4]).split()[-1]), rates=[]))
        d["rates"].append((r[10].date(), float(r[7])))

    def rate(d, day):
        return [f for eff, f in sorted(d["rates"]) if eff <= day][-1]
    till = D["till"]
    rc = {}
    for key, g in till.groupby(["store", "till", "receipt"]):
        rc[key] = g
    tot = collections.defaultdict(float)
    for key, g in rc.items():
        day = g.when.iloc[0].date()
        for r in g.itertuples():
            if r.description == "MULTIBUY SAVING":
                d = info[r.promo]
                sday = day
                if r.qty < 0:
                    note = " ".join(str(x) for x in g.note if isinstance(x, str))
                    m = re.search(r"refund rcpt (\w{3}) (\d) (\d{6})", note)
                    sday = rc[(m.group(1), int(m.group(2)), m.group(3))].when.iloc[0].date()
                if d["start"] <= sday <= d["end"]:
                    tot["%s Q%d" % (d["supplier"], (sday.month - 1) // 3 + 1)] += r.qty * rate(d, sday)
            elif r.plu == K.ADJ_PLU:
                m = re.search(r"MB missed rcpt (\w{3}) (\d) (\d{6})", r.note)
                og = rc[(m.group(1), int(m.group(2)), m.group(3))]
                oday = og.when.iloc[0].date()
                left = round(-r.value, 2)
                for did, d in info.items():
                    if not (d["start"] <= oday <= d["end"]):
                        continue
                    n = int(og[og.plu.isin(d["plus"]) & (og.qty > 0)].qty.sum())
                    given = int(((og.promo == did) & (og.qty > 0)).sum())
                    miss = n // 2 - given
                    if miss < 1 or left <= 0:
                        continue
                    p = og[og.plu.isin(d["plus"]) & (og.qty > 0)].iloc[0]
                    save = round(2 * D["price"][p.plu] - d["price"], 2)
                    pairs = min(miss, int(round(left / save)))
                    left = round(left - pairs * save, 2)
                    tot["%s Q%d" % (d["supplier"], (oday.month - 1) // 3 + 1)] += pairs * rate(d, oday)
    return {k: int(round(v)) for k, v in tot.items()}


def documents(T):
    """One read-back per shipped format, each with a positive control on the same extractor."""
    bad = []
    from pypdf import PdfReader
    import docx
    for k, want in (("terms", "Each card is issued to one member"), ("agreement", "Coordinated Universal Time"),
                    ("board", "Take your label to any checkout")):
        t = re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in PdfReader(os.path.join(T, K.FILES[k])).pages))
        if not t.strip() or want not in t:
            bad.append("%s: control %r not read" % (k, want))
    b = " ".join(p.text for p in docx.Document(os.path.join(T, K.FILES["brief"])).paragraphs)
    if "anyone in it" not in b:
        bad.append("brief: control not read")
    x = pd.read_excel(os.path.join(T, K.FILES["tracker"]), header=None)
    if x.shape[0] < 10:
        bad.append("tracker: not read")
    c = pd.read_csv(os.path.join(T, K.FILES["census"]))
    if c.shape[0] < 10:
        bad.append("census: not read")
    return bad


def run(T, figs_path):
    F = json.load(open(figs_path))
    D = load(T)
    bad = documents(T)
    units, n = homes(D)
    sh = shares(units)
    low = min(sh, key=lambda b: sh[b][2])
    order = sorted(sh, key=lambda b: sh[b][2])
    if low != F["call"]:
        bad.append("call %s against %s" % (low, F["call"]))
    if order[1] != F["runner_up"]:
        bad.append("runner-up %s against %s" % (order[1], F["runner_up"]))
    for b, v in sh.items():
        f = F["rivals"][b]
        if (v[0], v[1], int(round(v[2]))) != (f["homes"], f["both"], f["share"]):
            bad.append("%s %s against %s" % (b, v, f))
    if int(round(sh[order[1]][2] - sh[low][2])) != F["gap_points"]:
        bad.append("gap")
    if n != F["receipts_matched"]:
        bad.append("receipts matched %d against %d" % (n, F["receipts_matched"]))
    ca = counter(D)
    for k, v in F["ask_a"].items():
        if abs(ca.get(k, 0.0) - v) > 1e-9:
            bad.append("ask A %s %.1f against %.1f" % (k, ca.get(k, 0.0), v))
    fb = funding(D)
    for k, v in F["ask_b"].items():
        if fb.get(k, 0) != v:
            bad.append("ask B %s %d against %d" % (k, fb.get(k, 0), v))
    return bad


if __name__ == "__main__":
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    fp = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "figures.json")
    b = run(T, fp)
    print("verify: %s" % ("PASS" if not b else "FAIL " + "; ".join(b)))
    sys.exit(1 if b else 0)
