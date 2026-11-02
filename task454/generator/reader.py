"""Reads the shipped pack under target/ (never the generator's objects): used by verify.py and ceiling.py."""
import csv, os, re, datetime as dt
from collections import defaultdict
import openpyxl
from pypdf import PdfReader


def load(T):
    P = {}
    rows = []
    with open(os.path.join(T, "apn_pos_research_extract_2026.csv")) as f:
        for r in csv.DictReader(f):
            rows.append((r["card_id"], r["merchant_region"], int(r["month"][5:7]), r["statement_sa2"], float(r["spend_aud"]),
                         int(r["transactions"]), int(r["active_days"])))
    P["rows"] = rows
    wb = openpyxl.load_workbook(os.path.join(T, "apn_research_cards_2026.xlsx"), read_only=True)
    ws = wb.active
    P["weight"], P["stratum"] = {}, {}
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        P["weight"][r[0]] = float(r[2]); P["stratum"][r[0]] = r[1]
    P["sa2"] = {}
    with open(os.path.join(T, "erp_sa2_30jun2026_preliminary.csv")) as f:
        for r in csv.DictReader(f):
            P["sa2"][r["sa2_code"]] = {"name": r["sa2_name"], "sa3": r["sa3_name"], "erp": int(r["erp_30jun2026"])}
    # Schedule 1 from the guidelines PDF: regions, their SA3s and the shared SA2s with shares
    text = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "rvif_2027_round_guidelines.pdf")).pages)
    P["guidelines_text"] = text
    P["closure_text"] = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "rtip_closure_decision_2026.pdf")).pages)
    sched = text[text.index("Schedule 1"):]
    names = {"WST": "Westhaven", "JAB": "Jabiru Coast", "LYR": "Lyrebird Peninsula", "YAL": "Yallambee Valley",
             "SPX": "Spinifex Gorges", "TNG": "Tingle Ranges", "PEL": "Pelican Coast", "GID": "Gidgee Basin",
             "CAR": "Carisbrook Tablelands", "WOL": "Lower Wollomby", "MUL": "Mulga Plains", "KEL": "Port Kelburn"}
    P["names"] = names
    flat = " ".join(sched.split())
    starts = {}
    for code, nm in names.items():
        k = flat.find("%s %s " % (nm, code))
        if k >= 0:
            starts[code] = k
    order = sorted(starts, key=lambda c: starts[c])
    shares = defaultdict(dict)
    sa3_region = {}
    sa3_names = sorted({x["sa3"] for x in P["sa2"].values()}, key=len, reverse=True)
    for i, code in enumerate(order):
        a = starts[code] + len("%s %s " % (names[code], code))
        b = starts[order[i + 1]] if i + 1 < len(order) else len(flat)
        seg = flat[a:b]
        for m in re.finditer(r"\((\d{9})\): (\d+) per cent", seg):
            shares[m.group(1)][code] = int(m.group(2)) / 100.0
        body = seg
        for code2, x in P["sa2"].items():
            body = re.sub(r"%s \(%s\): \d+ per cent;?" % (re.escape(x["name"]), code2), "", body)
        for nm in sa3_names:
            if re.search(r"(^|, )%s(,|$| )" % re.escape(nm), body.strip()):
                sa3_region.setdefault(nm, code)
    P["shares"] = dict(shares)
    P["sa2_region"] = {k: sa3_region[v["sa3"]] for k, v in P["sa2"].items()}
    # the program's records
    wb = openpyxl.load_workbook(os.path.join(T, "rtip_agreements_2026-12-31.xlsx"), read_only=True)
    ws = wb.active
    ags = []
    hdr = None
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Agreement":
            hdr = r; continue
        if hdr and r and r[0]:
            d = dict(zip(hdr, r))
            ags.append(d)
    P["agreements"] = ags
    def rd(path):
        with open(os.path.join(T, path)) as f:
            return list(csv.DictReader(f))
    P["claims"] = rd("rtip_claims_2026.csv")
    P["payments"] = rd("ap_payments_rtip_2026.csv")
    P["receipts"] = rd("ar_receipts_rtip_2026.csv")
    return P


def region_pop(P):
    out = defaultdict(float)
    for code, x in P["sa2"].items():
        if code in P["shares"] and P["shares"][code]:
            for r, s in P["shares"][code].items():
                out[r] += x["erp"] * s
        else:
            out[P["sa2_region"][code]] += x["erp"]
    return out


def presence(P):
    months = defaultdict(set); days = defaultdict(int)
    for cid, reg, m, sa2, s, t, d in P["rows"]:
        months[(cid, reg)].add(m); days[(cid, reg)] += d
    return months, days


def visitor_spend(P, is_visitor):
    q = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for row in P["rows"]:
        cid, reg, m, sa2, s, t, d = row
        if reg != "WST" and is_visitor(row):
            q[reg][(m - 1) // 3] += P["weight"][cid] * s
    return q


def _program(P):
    """The program's records as read from the pack: agreements, claims, transfers (the 20 March repeats set apart as
    duplicates of the run before) and receipts."""
    ags = {a["Agreement"]: a for a in P["agreements"]}
    region_of = {a["Council"]: a["Region"] for a in P["agreements"]}
    pays = sorted(P["payments"], key=lambda p: (p["paid_on"], p["payment_id"]))
    seen, repeats = defaultdict(list), []
    for p in pays:
        key = (p["payee"], p["amount_aud"], p["agreement_ref"], p["payment_run"])
        if seen[key] and (dt.date.fromisoformat(p["paid_on"]) - dt.date.fromisoformat(seen[key][-1])).days <= 2:
            repeats.append(p)
        seen[key].append(p["paid_on"])
    rep_ids = {p["payment_id"] for p in repeats}
    live = [p for p in pays if p["payment_id"] not in rep_ids]
    claims = [dict(c, approved=float(c["approved_aud"]), on=dt.datetime.strptime(c["approved_on"], "%d/%m/%Y").date())
              for c in P["claims"]]
    return ags, region_of, live, repeats, claims


def _remaining(P, paid):
    A = defaultdict(float)
    for a in P["agreements"]:
        if a["Status"] == "Open":
            A[a["Region"]] += a["Approved ($)"] - a["Paid to 31 Dec 2025 ($)"] - paid[a["Agreement"]]
    return A


def split_transfers(P, cross=True):
    """Book each transfer to the claims it paid. cross=True: any one to three of the payee's unpaired claims approved
    before the transfer that sum to it (the claims may sit on different agreements). cross=False (the careful solver's
    pairing): one claim, or claims of one agreement, that sum to it; otherwise the agreement it quotes."""
    import itertools
    ags, region_of, live, repeats, claims = _program(P)
    paid, used = defaultdict(float), set()
    for p in live:
        amt = float(p["amount_aud"]); on = dt.date.fromisoformat(p["paid_on"])
        window = [c for c in claims if c["council"] == p["payee"] and c["claim_no"] not in used and c["on"] < on]
        match = None
        for k in (1, 2, 3):
            for combo in itertools.combinations(window, k):
                if (cross or len({c["agreement"] for c in combo}) == 1) and abs(sum(c["approved"] for c in combo) - amt) < 0.005:
                    match = combo
                    break
            if match:
                break
        if match:
            for c in match:
                used.add(c["claim_no"]); paid[c["agreement"]] += c["approved"]
        else:
            assert not cross, p
            paid[p["agreement_ref"]] += amt
    return paid


def ask_routes(P):
    """Every complete pipeline a careful solver could file for the two asks, read from the pack: route -> (A, B) by
    region name. 'golden' splits each transfer into the claims it paid and each receipt into what it returns."""
    ags, region_of, live, repeats, claims = _program(P)
    rep_by = defaultdict(list)
    for p in repeats:
        rep_by[p["payee"]].append(float(p["amount_aud"]))
    golden_paid = split_transfers(P, cross=True)
    careful_paid = split_transfers(P, cross=False)
    last = max(dt.date.fromisoformat(p["paid_on"]) for p in live)
    allc, timing, matched = defaultdict(float), defaultdict(float), defaultdict(float)
    for c in claims:
        allc[c["agreement"]] += c["approved"]
        if c["on"] <= last - dt.timedelta(days=4):
            timing[c["agreement"]] += c["approved"]
    for p in live:
        amt = float(p["amount_aud"])
        hit = [c for c in claims if c["council"] == p["payee"] and abs(c["approved"] - amt) < 0.005]
        if len(hit) == 1:
            matched[hit[0]["agreement"]] += amt
    whole, paired, net = defaultdict(float), defaultdict(float), defaultdict(float)
    for r in P["receipts"]:
        amt = float(r["amount_aud"]); reg = region_of[r["payer"]]
        reps = rep_by.get(r["payer"], [])
        whole[reg] += amt
        if not (any(abs(amt - x) < 0.005 for x in reps) or (reps and abs(amt - sum(reps)) < 0.005)):
            paired[reg] += amt
    for name, reg in region_of.items():
        got = sum(float(r["amount_aud"]) for r in P["receipts"] if r["payer"] == name)
        if got:
            net[reg] += got - sum(rep_by.get(name, []))
    rr26, rrall = defaultdict(float), defaultdict(float)
    for a in P["agreements"]:
        if a["Status"] != "Open" and a["Final cost ($)"] is not None:
            u = a["Paid to 31 Dec 2025 ($)"] + golden_paid[a["Agreement"]] - a["Final cost ($)"]
            if u > 0.005:
                rrall[a["Region"]] += u
                if a["Acquitted or withdrawn"].year == 2026:
                    rr26[a["Region"]] += u
    # the full handling: a receipt carries a repeat only where it equals the repeat, or the repeat plus what one of
    # the council's closed agreements left unspent (its paid amount less its final cost)
    gold = defaultdict(float)
    for name, reg in region_of.items():
        reps = list(rep_by.get(name, []))
        owed = [a["Paid to 31 Dec 2025 ($)"] + golden_paid[a["Agreement"]] - a["Final cost ($)"] for a in P["agreements"]
                if a["Council"] == name and a["Status"] != "Open" and a["Final cost ($)"] is not None]
        for r in P["receipts"]:
            if r["payer"] != name:
                continue
            amt, back = float(r["amount_aud"]), 0.0
            for x in reps:
                if abs(amt - x) < 0.005 or any(abs(amt - x - u) < 0.005 for u in owed):
                    back = x
                    reps.remove(x)
                    break
            gold[reg] += amt - back
    rem = lambda paid: _remaining(P, paid)
    return {"golden": (rem(golden_paid), gold),
            "cracker": (rem(careful_paid), paired),
            "every receipt": (rem(careful_paid), whole),
            "claims all paid": (rem(allc), paired),
            "claims a transfer equals": (rem(matched), paired),
            "claims by payment timing": (rem(timing), paired),
            "receipts net of every repeat": (rem(careful_paid), net),
            "register, closed in 2026": (rem(careful_paid), rr26),
            "register, every closure": (rem(careful_paid), rrall)}


def program_answers(P, link=True):
    """link=True: the golden handling of both asks; link=False: the careful solver's (the cracker)."""
    R = ask_routes(P)
    return R["golden"] if link else R["cracker"]
