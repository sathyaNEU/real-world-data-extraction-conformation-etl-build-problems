"""task129 generator: the monthly synthetic crawl (request grain), its run configuration and the
web asset register. One cold-cache run per URL per crawl, anonymous (ad-supported) profile."""
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

import params as P
from knobs_lab import LAB_ADJ

CRAWL_DATES = [date(2026, 2, 18), date(2026, 3, 18), date(2026, 4, 15), date(2026, 5, 20),
               date(2026, 6, 17), date(2026, 7, 15), date(2026, 8, 19)]
LIST_V2_FROM = date(2026, 6, 1)
AGENT = "SMDQ-Synth/3.4 (Moto G Power emulation; +ops@sonderaa-medier.dk)"

H_STATIC = "static.sonderaa-medier.dk"
H_IMG_OLD = "img.sonderaa-medier.dk"
H_PIX = "pix.sonderaa-medier.dk"
H_CMP = "cmp.sonderaa-medier.dk"
H_PUBCDN = "cdn.jsdelivr.net"
H_GPT = "securepubads.g.doubleclick.net"
H_SSP = ["ib.adnxs.com", "fastlane.rubiconproject.com", "hbopenbid.pubmatic.com"]
H_ANALYTICS = "metrics.sonderaa-medier.dk"

# asset register: (host, path prefix) -> change letter or "" (platform baseline)
ASSETS = [
    (H_STATIC, "/css/", "", "Site stylesheets"),
    (H_STATIC, "/js/legacy/", "C", "Front-end bundle before Bølge (retired per wave)"),
    (H_STATIC, "/boelge/", "C", "Bølge front end: application chunks"),
    (H_PUBCDN, "/npm/preact@", "C", "Bølge front end: framework runtime"),
    (H_PUBCDN, "/npm/@sonderaa/boelge-ui@", "C", "Bølge front end: component library"),
    (H_STATIC, "/hb/", "A", "Header bidding: wrapper core library"),
    (H_STATIC, "/ads/legacy/", "A", "Ad tags before header bidding"),
    (H_GPT, "/", "A", "Ad server tag and creatives"),
    (H_SSP[0], "/", "A", "Header bidding: bidder"),
    (H_SSP[1], "/", "A", "Header bidding: bidder"),
    (H_SSP[2], "/", "A", "Header bidding: bidder"),
    (H_STATIC, "/fonts/legacy/", "E", "Web fonts before the brand fonts"),
    (H_STATIC, "/fonts/brand/", "E", "Brand web fonts"),
    (H_IMG_OLD, "/billeder/", "B", "Image delivery before the pipeline (retired 7 April)"),
    (H_PIX, "/r/", "B", "Image pipeline renditions"),
    (H_CMP, "/", "D", "Consent management (banner and vendor list)"),
    (H_ANALYTICS, "/", "", "Page analytics and RUM beacon"),
]


def url_lists(rng):
    """Crawl URL lists. v1 for February to May, v2 (refreshed) from June."""
    mix = {"forside": 1, "sektion": 5, "artikel": 34, "galleri": 6, "liveblog": 3, "sport": 9,
           "arkiv": 5, "tjenester": 3, "spil": 2}
    rows = []
    for t in P.TITLES:
        for tpl, k in mix.items():
            for i in range(k):
                rows.append((t, tpl))
    v1 = pd.DataFrame(rows, columns=["title", "template"])
    v1["page_id"] = rng.choice(np.arange(5_150_000, 5_250_000), len(v1), replace=False)
    # refresh: about 45 per cent of article, sport and gallery URLs replaced, galleries added
    keep = np.ones(len(v1), bool)
    churn = v1.template.isin(["artikel", "sport", "galleri", "liveblog"]).values
    keep[churn] = rng.random(churn.sum()) > 0.45
    add = []
    for t in P.TITLES:
        n_out = int((~keep & (v1.title.values == t)).sum())
        tpls = ["galleri"] * (n_out // 2 + 4) + ["artikel"] * (n_out - n_out // 2)
        for tpl in tpls:
            add.append((t, tpl))
    v2 = pd.concat([v1[keep], pd.DataFrame(add, columns=["title", "template"])],
                   ignore_index=True)
    newid = rng.choice(np.arange(5_330_000, 5_380_000), len(add), replace=False)
    v2.loc[v2.page_id.isna(), "page_id"] = newid
    for df in (v1, v2):
        df["page_id"] = df.page_id.astype(np.int64)
        df["url"] = [_url(r.title, r.template, r.page_id) for r in df.itertuples()]
    return v1.reset_index(drop=True), v2.reset_index(drop=True)


def _url(title, tpl, pid):
    dom = P.TITLE_DOMAIN[title]
    path = {"forside": "/", "sektion": f"/nyheder?s={pid % 7}", "artikel": f"/nyheder/art{pid}",
            "galleri": f"/galleri/art{pid}", "liveblog": f"/liveblog/art{pid}",
            "sport": f"/sport/art{pid}", "arkiv": f"/arkiv/art{pid - 2_900_000}",
            "tjenester": ["/tv-guide", "/vejret", "/doedsfald"][pid % 3],
            "spil": ["/spil/krydsord", "/spil/sudoku"][pid % 2]}[tpl]
    if tpl == "sektion":
        path = "/" + ["nyheder", "kultur", "erhverv", "debat", "112", "lokalt", "motor"][pid % 7]
    return "https://" + dom + path


def _switch_on(tpl, d):
    """Which changes are live on a crawled page of this template on this crawl date."""
    live = {"E": d >= P.DATED["E"], "B": d >= P.DATED["B"] and tpl in P.HERO,
            "D": d >= P.DATED["D"]}
    if tpl in P.COHORTS:
        on = d >= P.COHORT_SWITCH[tpl]
        live["A"] = on
        live["C"] = on
    else:
        live["A"] = tpl == P.PUZZLE_T and d >= P.PUZZLE_AD_SWITCH
        live["C"] = False
    return live


IMG_N = {"forside": 22, "sektion": 16, "artikel": 6, "galleri": 28, "liveblog": 9, "sport": 10,
         "arkiv": 4, "tjenester": 3, "spil": 1}


def page_requests(rng, title, tpl, pid, d, prof):
    """Requests of one crawled page on one crawl date. prof holds the URL's stable sizes."""
    live = _switch_on(tpl, d)
    req = []
    req.append(("document", "https://" + P.TITLE_DOMAIN[title], "/", prof["html"]))
    req.append(("stylesheet", H_STATIC, "/css/site-2026.css", 41.3 + prof["css"]))
    req.append(("script", H_ANALYTICS, "/rum/v2.js", 18.6))
    req.append(("xhr", H_ANALYTICS, "/collect", 0.9))
    tl = title.lower()
    adj = LAB_ADJ[title]
    if live["E"]:
        for i, kb in enumerate([88.4, 91.2, 86.7, 94.1]):
            req.append(("font", H_STATIC, f"/fonts/brand/sondera-sans-{i}.woff2", kb))
        req.append(("font", H_STATIC, f"/fonts/brand/{tl}-display.woff2", 24.0 + adj["E"]))
    else:
        req.append(("font", H_STATIC, "/fonts/legacy/georgia-sub.woff2", 31.5))
        req.append(("font", H_STATIC, "/fonts/legacy/arial-sub.woff2", 28.0))
    nimg = IMG_N[tpl]
    for i in range(nimg):
        base = prof["img"][i]
        if live["B"]:
            req.append(("image", H_PIX, f"/r/{pid}-{i}-w1080.avif", base * prof["pipe"]))
            if i == 0:
                req.append(("image", H_PIX, f"/r/{tl}-masthead-w1080.avif", 9.0 + adj["B"]))
        else:
            req.append(("image", H_IMG_OLD, f"/billeder/{pid}-{i}.jpg", base))
    if live["C"]:
        req.append(("script", H_PUBCDN, "/npm/preact@10.22.1/dist/preact.min.js", 11.6))
        req.append(("script", H_PUBCDN, "/npm/@sonderaa/boelge-ui@4.8.2/dist/ui.min.js", 26.3))
        req.append(("script", H_STATIC, f"/boelge/{tpl}.chunk.js", prof["chunk"]))
        req.append(("script", H_STATIC, "/boelge/runtime.js", 172.4 + prof["c_extra"]))
        req.append(("stylesheet", H_STATIC, f"/boelge/theme-{tl}.css", 18.0 + adj["C"]))
    else:
        req.append(("script", H_STATIC, "/js/legacy/app.js", 104.8))
    if tpl != "tjenester" and tpl != "arkiv" or live["A"]:
        if live["A"]:
            req.append(("script", H_STATIC, "/hb/prebid-8.52.0.min.js", 64.2))
            req.append(("script", H_STATIC, "/hb/adapters-2026.06.js", 48.5))
            req.append(("script", H_STATIC, f"/hb/config-{tl}.js", 6.0 + adj["A"]))
            req.append(("script", H_GPT, "/tag/js/gpt.js", 48.9))
            for j, h in enumerate(H_SSP):
                req.append(("xhr", h, "/openrtb2/auction", 9.6 + 1.3 * j))
            for k in range(prof["slots"]):
                req.append(("image", H_GPT, f"/pagead/creative/{pid % 997}-{k}", prof["cre"] + 38.0))
            req.append(("script", H_PUBCDN, "/npm/prebid-universal-creative@1.17.0/dist/uc.js",
                        prof["a_extra"]))
        else:
            req.append(("script", H_STATIC, "/ads/legacy/adtags.js", 42.0))
            req.append(("script", H_GPT, "/tag/js/gpt.js", 48.9))
            for k in range(prof["slots"]):
                req.append(("image", H_GPT, f"/pagead/creative/{pid % 997}-{k}", prof["cre"]))
    if live["D"]:
        req.append(("script", H_CMP, "/v3/cmp.js", 47.7))
        req.append(("xhr", H_CMP, f"/v3/vendor-list-{tl}.json", 12.9 + prof["cmp"] + adj["D"]))
    return req


def profiles(rng, pages):
    prof = {}
    for r in pages.itertuples():
        n = IMG_N[r.template]
        prof[r.url] = {
            "html": float(np.round(rng.uniform(52, 96), 1)),
            "css": float(np.round(rng.uniform(0, 6), 1)),
            "img": np.round(rng.uniform(28, 64, n) * (1.6 if r.template == "galleri" else 1.0), 1),
            "pipe": float(rng.uniform(1.40, 1.64) if r.template != "galleri" else
                          rng.uniform(1.22, 1.38)),
            "chunk": float(np.round(rng.uniform(38, 66), 1)),
            "c_extra": float(np.round(rng.uniform(0, 9), 1)),
            "a_extra": float(np.round(rng.uniform(6, 14), 1)),
            "slots": int(rng.integers(2, 5)) if r.template != "spil" else 2,
            "cre": float(np.round(rng.uniform(14, 26), 1)),
            "cmp": float(np.round(rng.uniform(0, 4), 1)),
        }
    return prof


def crawl(rng):
    v1, v2 = url_lists(rng)
    allp = pd.concat([v1, v2]).drop_duplicates("url").reset_index(drop=True)
    prof = profiles(rng, allp)
    rows = []
    run_no = 0
    for d in CRAWL_DATES:
        lst = v2 if d >= LIST_V2_FROM else v1
        lid = "v2" if d >= LIST_V2_FROM else "v1"
        t0 = datetime(d.year, d.month, d.day, 1, 10)
        order = rng.permutation(len(lst))
        for k, i in enumerate(order):
            r = lst.iloc[i]
            run_no += 1
            start = t0 + timedelta(seconds=int(k * 21 + rng.integers(0, 9)))
            reqs = page_requests(rng, r.title, r.template, int(r.page_id), d, prof[r.url])
            timeout = rng.random() < (0.05 if r.title == "LA" else 0.03)
            runs = []
            if timeout:
                cut = int(len(reqs) * rng.uniform(0.35, 0.7))
                runs.append(("timeout", reqs[:cut], start))
                run_no += 1
                runs.append(("complete", reqs, start + timedelta(minutes=int(rng.integers(52, 95)))))
            else:
                runs.append(("complete", reqs, start))
            for status, rq, st in runs:
                rid = f"{d.strftime('%Y%m')}-{run_no:05d}"
                for j, (rtype, host, path, kb) in enumerate(rq):
                    rows.append((rid, d.isoformat(), lid, r.url, r.title, status,
                                 (st + timedelta(milliseconds=j * 37)).strftime("%Y-%m-%dT%H:%M:%S"),
                                 rtype, "https://" + host.replace("https://", "") + path,
                                 int(round(kb * 1000))))
    df = pd.DataFrame(rows, columns=["run_id", "crawl_date", "url_list", "page_url", "masthead",
                                     "run_status", "requested_at_utc", "resource_type",
                                     "request_url", "transfer_bytes"])
    return df, v1, v2


def asset_register():
    rows = []
    for host, prefix, chg, desc in ASSETS:
        rows.append({"host": host, "path_prefix": prefix,
                     "change_id": P.CHG[chg][0] if chg else "", "description": desc})
    return pd.DataFrame(rows)
