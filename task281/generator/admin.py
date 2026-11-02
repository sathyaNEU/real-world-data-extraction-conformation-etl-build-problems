"""The library's administrative records around the lending platform: courses and reading lists, the
catalogue, the licence register, the platform's licence status report, invoices, the Finance Office's
monthly rates and the publishers' package title lists. Built from the world on its own random streams."""
import datetime as dt
import random

import params as P
import world as WD


def fund_code(old_fac, when):
    """Course texts fund a purchase was charged to: 2025-26 faculty funds to 31 July 2026, the new ones after."""
    if when < dt.date(2026, 8, 1):
        return "CT-" + old_fac
    return "CT-" + WD.new_faculty(old_fac)


def build(W, seed=P.SEED):
    ra = random.Random(seed * 11 + 1)   # courses and reading lists
    rc = random.Random(seed * 11 + 2)   # catalogue
    ri = random.Random(seed * 11 + 3)   # invoices
    rx = random.Random(seed * 11 + 4)   # rates
    A = type("Admin", (), {})()

    # ---------------------------------------------------------------- courses
    courses = []
    used = set()
    for code, name, old, n in WD.SCHOOLS:
        for sem in ("A25", "S26", "A26"):
            k = max(5, int(n / 95.0 * ra.uniform(0.8, 1.2)))
            for _ in range(k):
                for _ in range(50):
                    lvl = ra.choice([1, 2, 2, 3, 3, 4, 5])
                    cc = "%s%d%03d" % (code, lvl, ra.randint(1, 199))
                    if cc not in used:
                        used.add(cc)
                        break
                topic = ra.choice(WD.DISCIPLINE_WORDS[code])
                form = ra.choice(["%s", "Advanced %s", "Topics in %s", "%s %d", "Issues in %s"])
                title = form % topic if "%d" not in form else form % (topic, lvl)
                courses.append(dict(code=cc, school=code, sem=sem, title=title, level=lvl,
                                    enrol=int(ra.uniform(25, 260))))
    A.courses = courses
    by_school_sem = {}
    for c in courses:
        by_school_sem.setdefault((c["school"], c["sem"]), []).append(c)

    # ---------------------------------------------------------------- reading lists
    items = []
    lid = 3100
    for t in W.titles:
        sems = {"S26": ["S26"], "A": ["A25", "A26"], "both": ["A25", "S26", "A26"]}[t["sem"]]
        for sem in sems:
            own = by_school_sem[(t["school"], sem)]
            for c in ra.sample(own, min(len(own), ra.choice([1, 1, 2, 2, 3]))):
                items.append(_item(ra, c, t, "Essential" if ra.random() < 0.78 else "Recommended"))
            if t["cross"]:
                cr = by_school_sem[(t["cross"], sem)]
                c = ra.choice(cr)
                items.append(_item(ra, c, t, "Essential" if ra.random() < 0.7 else "Recommended"))
    for b in W.print_only:
        sems = {"S26": ["S26"], "A": ["A25", "A26"], "both": ["A25", "S26", "A26"]}[b["sem"]]
        for sem in sems:
            own = by_school_sem[(b["school"], sem)]
            for c in ra.sample(own, min(len(own), ra.choice([1, 1, 2]))):
                imp = "Essential" if ra.random() < 0.45 else ra.choice(["Recommended", "Background"])
                isbn = b["p_isbn"] if ra.random() < 0.8 else WD.isbn10_from13(b["p_isbn"])
                items.append(dict(course=c["code"], sem=sem, title=b["title"], edition=b["edition"],
                                  isbn=_style(ra, isbn), importance=imp, work=b["work"], kind="print",
                                  cited_edition_isbn=b["p_isbn"]))
    ra.shuffle(items)
    for it in items:
        lid += ra.randint(1, 3)
        it["list_item"] = "RLI-%06d" % (lid * 17 % 999983)
    A.items = items

    # ---------------------------------------------------------------- catalogue (one row per record)
    cat = []
    for t in W.titles:
        cat.append(dict(mms=t["mms"], title=t["title"], edition=t["edition"], year=t["year"], isbn=t["e_isbn"],
                        rtype="Book (electronic)", platform=t["platform_id"], linked=t["mms_print"],
                        preceded_by=t["prev"]["mms"] if t["prev"] else "", publisher=t["publisher"]))
        cat.append(dict(mms=t["mms_print"], title=t["title"], edition=t["edition"], year=t["year"], isbn=t["p_isbn"],
                        rtype="Book (print)", platform="", linked=t["mms"],
                        preceded_by=t["prev"]["mms"] if t["prev"] else "", publisher=t["publisher"]))
        if t["prev"]:
            p = t["prev"]
            cat.append(dict(mms=p["mms"], title=t["title"], edition=p["edition"], year=p["year"], isbn=p["p_isbn"],
                            rtype="Book (print)", platform="", linked="", preceded_by="", publisher=t["publisher"]))
    for b in W.print_only:
        cat.append(dict(mms=b["mms"], title=b["title"], edition=b["edition"], year=b["year"], isbn=b["p_isbn"],
                        rtype="Book (print)", platform="", linked="", preceded_by="", publisher=b["publisher"]))
    rc.shuffle(cat)
    A.catalogue = cat

    # ---------------------------------------------------------------- the platform's licence status at 1 Sep 2025
    status = []
    for L in W.licences:
        if L.model == "1U-M" and L.bought <= P.RECORD_START.date():
            for i in range(L.copies):
                status.append(dict(lic=L.lic_id, copy=i + 1, left=L.remaining0[i] if hasattr(L, "remaining0") else None))
    A.status = status

    # ---------------------------------------------------------------- Finance Office monthly rates (GBP per unit)
    rates = []
    eur, usd = 1.1720, 1.3405
    for m in range(1, 13):
        for y in (2025, 2026):
            pass
    d = dt.date(2025, 8, 1)
    while d <= dt.date(2026, 10, 1):
        eur *= rx.uniform(0.985, 1.015)
        usd *= rx.uniform(0.982, 1.018)
        rates.append(dict(month=d, eur=round(eur, 4), usd=round(usd, 4)))
        d = dt.date(d.year + (d.month // 12), d.month % 12 + 1, 1)
    A.rates = rates
    rate_of = {(r["month"].year, r["month"].month): r for r in rates}

    # ---------------------------------------------------------------- invoices dated 2026
    inv = []
    invno = {"Shelfmark Lend Ltd": 88120, "Lindqvist Digital GmbH": 5520, "Quincy Hall Inc.": 30070}
    tby = {t["id"]: t for t in W.titles}
    for L in W.licences:
        if L.model == "PKG":
            continue
        if not (dt.date(2026, 1, 1) <= L.bought <= dt.date(2026, 10, 31)):
            continue
        t = tby[L.title]
        vendor = [p[1] for p in WD.PUBLISHERS if p[0] == t["publisher"]][0]
        inv_date = L.bought + dt.timedelta(days=ri.randint(2, 19))
        if inv_date > dt.date(2026, 10, 31):
            continue
        invno[vendor] += ri.randint(1, 4)
        cur = t["currency"]
        r = rate_of[(inv_date.year, inv_date.month)]
        amt_cur = L.price_gbp * L.copies if cur == "GBP" else round(L.price_gbp * L.copies * (r["eur"] if cur == "EUR" else r["usd"]), 2)
        inv.append(dict(vendor=vendor, invoice=_invno(vendor, invno[vendor]), inv_date=inv_date, po_line=L.po_line,
                        desc="%s (%s)" % (t["title"], _model_text(L)), isbn=t["e_isbn"], qty=L.copies,
                        currency=cur, amount=round(amt_cur, 2), fund=fund_code(W.school_old[t["school"]], L.bought),
                        line_type="Renewal" if L.order_type == "Renewal" else "Order"))
    # package invoices (annual, January 2026), charged to the central course texts fund
    A.packages = []
    for pname, pub, schools in WD.PACKAGES:
        titles = [t for t in W.titles if t.get("package") == pname]
        extra = [x for x in W.package_extra if x["package"] == pname]
        vendor = [p[1] for p in WD.PUBLISHERS if p[0] == pub][0]
        cur = [p[2] for p in WD.PUBLISHERS if p[0] == pub][0]
        price_gbp = round(sum(ri.uniform(150, 290) for _ in titles) + 35.0 * len(extra), 2)
        inv_date = dt.date(2026, 1, ri.randint(5, 27))
        r = rate_of[(2026, 1)]
        amt = price_gbp if cur == "GBP" else round(price_gbp * (r["eur"] if cur == "EUR" else r["usd"]), 2)
        invno[vendor] += ri.randint(1, 4)
        po = "POL-%d-1" % (419000 + len(A.packages) * 37)
        A.packages.append(dict(name=pname, publisher=pub, titles=titles, extra=extra, amount=amt, currency=cur,
                               po_line=po, inv_date=inv_date))
        inv.append(dict(vendor=vendor, invoice=_invno(vendor, invno[vendor]), inv_date=inv_date, po_line=po,
                        desc="%s, access 1 Jan to 31 Dec 2026" % pname, isbn="", qty=1, currency=cur, amount=amt,
                        fund="CT-CORE", line_type="Package"))
    inv.sort(key=lambda x: (x["inv_date"], x["vendor"], x["invoice"]))
    A.invoices = inv
    return A


def _invno(vendor, n):
    if vendor.startswith("Shelfmark"):
        return "SML-%06d" % n
    if vendor.startswith("Lindqvist"):
        return "RE-2026-%05d" % n
    return "QH%07d" % n


def _model_text(L):
    return {"1U": "1 user, perpetual", "1U-M": "1 user, 40 loans", "3U": "3 users, perpetual"}[L.model]


def _style(ra, isbn):
    """an ISBN as an academic types it into the reading-list tool"""
    if len(isbn) == 13 and ra.random() < 0.28:
        return "%s-%s-%s-%s-%s" % (isbn[:3], isbn[3], isbn[4:8], isbn[8:12], isbn[12])
    if len(isbn) == 10 and ra.random() < 0.3:
        return "%s-%s-%s-%s" % (isbn[0], isbn[1:5], isbn[5:9], isbn[9])
    return isbn


def _item(ra, c, t, imp):
    """a reading-list item citing a platform title: the print or e-book ISBN, or an earlier edition's"""
    if t["prev"] and ra.random() < 0.4:
        isbn = t["prev"]["p_isbn"]
        ed = t["prev"]["edition"]
        if ra.random() < 0.2:
            isbn = WD.isbn10_from13(isbn)
    else:
        u = ra.random()
        isbn = t["p_isbn"] if u < 0.55 else (WD.isbn10_from13(t["p_isbn"]) if u < 0.68 else t["e_isbn"])
        ed = t["edition"]
    return dict(course=c["code"], sem=c["sem"], title=t["title"], edition=ed, isbn=_style(ra, isbn), importance=imp,
                work=t["work"], kind="title", title_id=t["id"])
