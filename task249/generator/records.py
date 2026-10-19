"""The records task249's pack is cut from: the analytics export, the sign-in register, the reader accounts, the paywall
log and the platform's monthly report (from the World), and the circulation system and the newsletter platform (their
own draws)."""
import datetime as dt
import hashlib
import numpy as np
import pandas as pd
import params as P
import world as W

EPOCH = dt.datetime(2027, 11, 1)                     # absolute hours count from 00:00 UTC on 1 November 2027
EPOCH_UNIX = int((EPOCH - dt.datetime(1970, 1, 1)).total_seconds())
REPLAY_FROM, REPLAY_TO = dt.datetime(2028, 11, 21, 3, 0), dt.datetime(2028, 11, 21, 9, 0)   # the re-sent export rows
YEAR_END_UTC = dt.datetime(2028, 12, 31, 23, 0)      # midnight in Berlin on the night of 31 December 2028
LOG_FROM = dt.datetime(2028, 7, 1)                   # the newsletter platform keeps six months of activity
EXPORT_AT = dt.datetime(2029, 1, 15, 6, 12)          # the newsletter platform's contact export (UTC)
CAMPAIGN_FROM, CAMPAIGN_TO = dt.datetime(2029, 1, 3, 7, 0), dt.datetime(2029, 1, 14, 20, 0)   # the new year's mailing
PROMO_FROM, PROMO_TO = dt.datetime(2028, 11, 7, 5, 30), YEAR_END_UTC   # the newsletters' box offering a neighbour's edition
SLUG = {"RHS": "rhenhagen-stadt", "KBR": "kirchbrunn", "ALH": "altenhorst", "WBR": "wiesbrueck", "HOL": "hollerfeld",
        "SOW": "sonnweiler", "MST": "muehlenstedt", "GRH": "grauheim", "EIT": "eichtal", "BST": "bergstetten",
        "LDN": "lindenau", "FKR": "falkenried"}
ADD_LINK = "https://www.rhenhagener-anzeiger.de/newsletter/ausgabe-hinzufuegen?ausgabe=%s"
SUBJ = ["gemeinderat", "stadtrat", "ortsbeirat", "kreistag", "feuerwehr", "polizei", "kita", "grundschule", "gesamtschule",
        "sportverein", "musikverein", "buergerinitiative", "rathaus", "klinikum", "busverkehr", "bauhof", "stadtwerke",
        "jugendzentrum", "seniorenbeirat", "tafel", "freiwilligenagentur", "wasserverband", "forstamt", "landwirte"]
PRED = ["beschliesst-haushalt", "streitet-ueber-gebuehren", "sucht-personal", "zieht-bilanz", "plant-neubau",
        "erhaelt-foerdergeld", "bekommt-neue-leitung", "warnt-vor-betrug", "verschiebt-entscheidung", "stellt-plaene-vor",
        "feiert-jubilaeum", "wehrt-sich-gegen-kuerzung", "startet-umfrage", "laedt-zur-versammlung", "zieht-um",
        "meldet-rekord", "kritisiert-landkreis", "erweitert-angebot"]


def article_link(code, t, k):
    """the article a newsletter link opens: the edition's section, a story of that day"""
    day = (t - dt.datetime(2028, 1, 1)).days
    aid = 4100000 + day * 97 + P.CODES.index(code) * 8 + k % 6
    return "https://www.rhenhagener-anzeiger.de/%s/%s-%s-%d.html" % (SLUG[code], SUBJ[aid * 7 % len(SUBJ)],
                                                                    PRED[aid * 13 % len(PRED)], aid)


def local_of(ts):
    """UTC datetimes (numpy or pandas) to Europe/Berlin wall time"""
    s = pd.to_datetime(pd.Series(ts)).dt.tz_localize("UTC").dt.tz_convert(P.TZ).dt.tz_localize(None)
    return s


def user_ref(acct):
    return hashlib.sha256(("rhm-%d" % acct).encode()).hexdigest()[:20]


# ---------------------------------------------------------------------------------------------- user agents
IOS = ["17_6_1", "18_0_1", "18_1", "18_1_1", "18_2"]
CHR = ["129.0.6668.100", "130.0.6723.91", "130.0.6723.117", "131.0.6778.85", "131.0.6778.108"]
FFX = ["131.0", "132.0", "133.0"]
EDG = ["130.0.2849.80", "131.0.2903.70", "131.0.2903.86"]
SAM = ["26.0", "27.0"]
AND = ["13", "14", "15"]
PHONES = ["SM-S918B", "SM-A546B", "SM-G991B", "Pixel 7", "Pixel 8", "SM-A156B", "2311DRK48G", "CPH2581"]
TABS = ["SM-X710", "SM-X200", "Lenovo TB-X606F", "SM-T733"]


def _ua(fam, r):
    """one user-agent string and the platform's parse (device, browser, os) for a family"""
    i = r.integers(0, 10 ** 6)
    ios, chv, ffv, edv = IOS[i % 5], CHR[i % 5], FFX[i % 3], EDG[i % 3]
    av, ph, tb, sv = AND[i % 3], PHONES[i % 8], TABS[i % 4], SAM[i % 2]
    iosv = ios.replace("_", ".")
    if fam == "ios_safari":
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/%s Mobile/15E148 Safari/604.1" % (ios, iosv.rsplit(".", 1)[0] if iosv.count(".") > 1 else iosv),
                "mobile", "Safari", "iOS")
    if fam == "ios_chrome":
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "CriOS/%s Mobile/15E148 Safari/604.1" % (ios, chv), "mobile", "Chrome", "iOS")
    if fam == "ios_inapp":
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Mobile/15E148 Instagram 357.0.0.25.101 (iPhone15,3; iOS %s; de_DE; de; scale=3.00)" % (ios, ios),
                "mobile", "Safari (in-app)", "iOS")
    if fam == "ios_gsa":
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "GSA/343.0.695551749 Mobile/15E148 Safari/604.1" % ios, "mobile", "Safari (in-app)", "iOS")
    if fam == "ios_firefox":
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "FxiOS/%s Mobile/15E148 Safari/605.1.15" % (ios, ffv), "mobile", "Firefox", "iOS")
    if fam == "ios_edge":
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/18.0 EdgiOS/%s Mobile/15E148 Safari/605.1.15" % (ios, edv), "mobile", "Edge", "iOS")
    if fam == "ipad_safari":
        return ("Mozilla/5.0 (iPad; CPU OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/%s "
                "Mobile/15E148 Safari/604.1" % (ios, iosv.rsplit(".", 1)[0] if iosv.count(".") > 1 else iosv),
                "tablet", "Safari", "iOS")
    if fam == "ipad_chrome":
        return ("Mozilla/5.0 (iPad; CPU OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/%s "
                "Mobile/15E148 Safari/604.1" % (ios, chv), "tablet", "Chrome", "iOS")
    if fam == "ipad_firefox":
        return ("Mozilla/5.0 (iPad; CPU OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/%s "
                "Mobile/15E148 Safari/605.1.15" % (ios, ffv), "tablet", "Firefox", "iOS")
    if fam == "mac_safari":
        return ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/%s Safari/605.1.15" % ["17.6", "18.0", "18.1", "18.2"][i % 4], "desktop", "Safari", "Macintosh")
    if fam == "and_chrome":
        return ("Mozilla/5.0 (Linux; Android %s; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile "
                "Safari/537.36" % (av, chv.split(".")[0] + ".0.0.0"), "mobile", "Chrome", "Android")
    if fam == "and_samsung":
        return ("Mozilla/5.0 (Linux; Android %s; %s) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/%s "
                "Chrome/125.0.0.0 Mobile Safari/537.36" % (av, ph, sv), "mobile", "Samsung Internet", "Android")
    if fam == "and_firefox":
        return ("Mozilla/5.0 (Android %s; Mobile; rv:%s) Gecko/%s Firefox/%s" % (av, ffv, ffv, ffv), "mobile", "Firefox", "Android")
    if fam == "and_webview":
        return ("Mozilla/5.0 (Linux; Android %s; %s Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Version/4.0 Chrome/%s Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/489.0.0.47.109;]" % (av, ph, chv),
                "mobile", "Android Webview", "Android")
    if fam == "and_opera":
        return ("Mozilla/5.0 (Linux; Android %s; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile "
                "Safari/537.36 OPR/86.0.4363.80926" % av, "mobile", "Opera", "Android")
    if fam == "andtab_chrome":
        return ("Mozilla/5.0 (Linux; Android %s; %s) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s "
                "Safari/537.36" % (av, tb, chv.split(".")[0] + ".0.0.0"), "tablet", "Chrome", "Android")
    if fam == "andtab_samsung":
        return ("Mozilla/5.0 (Linux; Android %s; %s) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/%s "
                "Chrome/125.0.0.0 Safari/537.36" % (av, tb, sv), "tablet", "Samsung Internet", "Android")
    if fam == "andtab_firefox":
        return ("Mozilla/5.0 (Android %s; Tablet; rv:%s) Gecko/%s Firefox/%s" % (av, ffv, ffv, ffv), "tablet", "Firefox", "Android")
    if fam == "win_chrome":
        return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s "
                "Safari/537.36" % (chv.split(".")[0] + ".0.0.0"), "desktop", "Chrome", "Windows")
    if fam == "win_edge":
        return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
                "Safari/537.36 Edg/%s" % edv, "desktop", "Edge", "Windows")
    if fam == "win_firefox":
        return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:%s) Gecko/20100101 Firefox/%s" % (ffv, ffv), "desktop", "Firefox", "Windows")
    if fam == "mac_chrome":
        return ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s "
                "Safari/537.36" % (chv.split(".")[0] + ".0.0.0"), "desktop", "Chrome", "Macintosh")
    if fam == "mac_firefox":
        return ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:%s) Gecko/20100101 Firefox/%s" % (ffv, ffv), "desktop", "Firefox", "Macintosh")
    if fam == "linux_firefox":
        return ("Mozilla/5.0 (X11; Linux x86_64; rv:%s) Gecko/20100101 Firefox/%s" % (ffv, ffv), "desktop", "Firefox", "Linux")
    raise KeyError(fam)


ISP = ["91.64.%d.0", "92.211.%d.0", "79.204.%d.0", "87.163.%d.0", "93.229.%d.0", "84.150.%d.0", "62.226.%d.0",
       "178.27.%d.0", "37.201.%d.0", "80.187.%d.0", "176.2.%d.0", "109.43.%d.0"]


# ------------------------------------------------------------------------------- versions and addresses over time
def _hours(y, m, d):
    return (dt.datetime(y, m, d, 17, 0) - EPOCH).total_seconds() / 3600.0


# each line: release hour (from EPOCH) and its version strings; browsers move to a release after their own lag
REL_SAFARI = [(_hours(2028, 7, 29), "28.6"), (_hours(2028, 9, 15), "29.0"), (_hours(2028, 10, 2), "29.0.1"),
              (_hours(2028, 10, 27), "29.1"), (_hours(2028, 11, 20), "29.1.1"), (_hours(2028, 12, 11), "29.2")]
REL_IOS = ["28_6", "29_0", "29_0_1", "29_1", "29_1_1", "29_2"]          # the system version apps report
REL_CHROME = [(_hours(2028, 8, 15), "180.0.7206.112"), (_hours(2028, 9, 12), "181.0.7238.94"),
              (_hours(2028, 10, 10), "182.0.7270.86"), (_hours(2028, 11, 7), "183.0.7311.108"),
              (_hours(2028, 12, 5), "184.0.7349.69")]
REL_EDGE = ["180.0.3764.58", "181.0.3790.82", "182.0.3812.62", "183.0.3851.71", "184.0.3889.55"]
REL_FIREFOX = [(_hours(2028, 8, 22), "182.0"), (_hours(2028, 9, 19), "183.0"), (_hours(2028, 10, 17), "184.0"),
               (_hours(2028, 11, 14), "185.0"), (_hours(2028, 12, 12), "186.0")]
REL_SAMSUNG = [(_hours(2028, 7, 18), ("31.0", "174")), (_hours(2028, 10, 24), ("32.0", "178"))]
REL_WEEKLY = [(_hours(2028, 9, 4) + 168.0 * k, k) for k in range(20)]   # in-app browsers: the apps ship weekly
IPHONES = [("iPhone15,4", "3.00", "1179x2556"), ("iPhone16,2", "3.00", "1290x2796"), ("iPhone14,5", "3.00", "1170x2532"),
           ("iPhone17,1", "3.00", "1206x2622"), ("iPhone15,2", "3.00", "1179x2556"), ("iPhone14,7", "3.00", "1170x2532"),
           ("iPhone17,3", "3.00", "1179x2556"), ("iPhone13,2", "3.00", "1170x2532"), ("iPhone16,1", "3.00", "1179x2556")]
ANDROID_MODELS = [("SM-S931B", "AP3A.240905.015.A2"), ("SM-A566B", "BP1A.250305.019"), ("Pixel 9", "BP2A.250605.031.A3"),
                  ("SM-A356B", "AP3A.240905.015.A2"), ("SM-S921B", "BP1A.250305.019"), ("2412DPC0AG", "AQ3A.240912.001")]
SAFARI_FAMS = {"ios_safari", "ipad_safari", "mac_safari"}
CHROME_FAMS = {"ios_chrome", "ipad_chrome", "ios_edge", "and_chrome", "and_webview", "and_opera", "andtab_chrome",
               "win_chrome", "win_edge", "mac_chrome"}
FIREFOX_FAMS = {"ios_firefox", "ipad_firefox", "and_firefox", "andtab_firefox", "win_firefox", "mac_firefox", "linux_firefox"}
SAMSUNG_FAMS = {"and_samsung", "andtab_samsung"}
WEEKLY_FAMS = {"ios_inapp", "ios_gsa"}
# addresses: a household's line with its provider (the address changes when the line reconnects), a mobile network's
# shared pool, an office line; the third part of a fixed line's address comes from its region's block
FIXED = ["79.204.%d.0", "87.163.%d.0", "93.229.%d.0", "84.150.%d.0", "91.64.%d.0", "178.27.%d.0", "37.201.%d.0",
         "92.211.%d.0", "62.226.%d.0"]
FIXED_P = [.20, .16, .14, .08, .12, .11, .07, .07, .05]
MOBILE = ["80.187.%d.0", "109.43.%d.0", "176.2.%d.0"]
MOBILE_P = [.45, .32, .23]
OFFICE = ["212.185.%d.0", "195.243.%d.0", "62.153.%d.0"]
BLOCK = 21                                   # /24 blocks a provider holds in each edition's region


def _mix(a, b):
    """a fixed integer hash of two integer arrays (uint64, wraps)"""
    x = np.asarray(a).astype(np.uint64) * np.uint64(0x9E3779B97F4A7C15)
    x = x ^ (np.asarray(b).astype(np.uint64) + np.uint64(0x632BE59BD9B4E019))
    x = x ^ (x >> np.uint64(29))
    x = x * np.uint64(0xBF58476D1CE4E5B9)
    x = x ^ (x >> np.uint64(32))
    return x


def _version_index(rel, t_hours, lag_hours):
    """the newest release a browser had installed at each session: released before the session less its lag"""
    hrs = np.array([h for h, _ in rel])
    k = np.searchsorted(hrs, np.asarray(t_hours) - np.asarray(lag_hours), side="right") - 1
    return np.clip(k, 0, len(rel) - 1)


def agent_strings(fam, t_hours, lag_hours, extra):
    """the user-agent string of each session from its browser family, the session's time, the browser's update lag
    and a per-browser detail (phone model, Android version); vectorised over sessions by unique combination"""
    fam = np.asarray(fam, dtype=object)
    t_hours = np.asarray(t_hours, float)
    lag_hours = np.asarray(lag_hours, float)
    extra = np.asarray(extra, np.int64)
    key = np.zeros(len(fam), np.int64)
    ks = _version_index(REL_SAFARI, t_hours, lag_hours)
    kc = _version_index(REL_CHROME, t_hours, lag_hours)
    kf = _version_index(REL_FIREFOX, t_hours, lag_hours)
    km = _version_index(REL_SAMSUNG, t_hours, lag_hours)
    kw = _version_index(REL_WEEKLY, t_hours, np.minimum(lag_hours, 96.0))
    is_s = np.isin(fam, list(SAFARI_FAMS)); is_c = np.isin(fam, list(CHROME_FAMS)); is_f = np.isin(fam, list(FIREFOX_FAMS))
    is_m = np.isin(fam, list(SAMSUNG_FAMS)); is_w = np.isin(fam, list(WEEKLY_FAMS))
    key = np.where(is_s, ks, key); key = np.where(is_c, kc, key); key = np.where(is_f, kf, key)
    key = np.where(is_m, km, key); key = np.where(is_w, kw * 16 + ks, key)
    combo = pd.DataFrame({"fam": fam, "k": key, "x": extra})
    codes, uniq = pd.factorize(pd.MultiIndex.from_frame(combo))
    out = []
    for f, k, x in uniq:
        out.append(_agent(f, int(k), int(x)))
    return np.array(out, dtype=object)[codes]


def _agent(f, k, x):
    ios = "18_6"                                             # Safari has reported this system version since 26
    if f in SAFARI_FAMS:
        sv = REL_SAFARI[k][1]
        if f == "ios_safari":
            return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/%s Mobile/15E148 Safari/604.1" % (ios, sv))
        if f == "ipad_safari":
            return ("Mozilla/5.0 (iPad; CPU OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/%s "
                    "Mobile/15E148 Safari/604.1" % (ios, sv))
        return ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/%s "
                "Safari/605.1.15" % sv)
    if f in CHROME_FAMS:
        cb = REL_CHROME[k][1]
        cm = cb.split(".")[0]
        if f == "ios_chrome":
            return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "CriOS/%s Mobile/15E148 Safari/604.1" % (ios, cb))
        if f == "ipad_chrome":
            return ("Mozilla/5.0 (iPad; CPU OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/%s "
                    "Mobile/15E148 Safari/604.1" % (ios, cb))
        if f == "ios_edge":
            return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/18.0 EdgiOS/%s Mobile/15E148 Safari/605.1.15" % (ios, REL_EDGE[k]))
        if f == "and_chrome":
            return ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 Mobile "
                    "Safari/537.36" % cm)
        if f == "and_webview":
            model, build = ANDROID_MODELS[x % len(ANDROID_MODELS)]
            return ("Mozilla/5.0 (Linux; Android %d; %s Build/%s; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                    "Chrome/%s Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/%d.0.0.%d.%d;]"
                    % (14 + x % 3, model, build, cb, 520 + k * 4, 31 + k, 88 + 7 * k))
        if f == "and_opera":
            return ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 Mobile "
                    "Safari/537.36 OPR/%d.0.%d.%d" % (cm, 96 + k, 4890 + 37 * k, 81100 + 911 * k))
        if f == "andtab_chrome":
            return ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 "
                    "Safari/537.36" % cm)
        if f == "win_chrome":
            return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 "
                    "Safari/537.36" % cm)
        if f == "win_edge":
            return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 "
                    "Safari/537.36 Edg/%s" % (cm, REL_EDGE[k]))
        return ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 "
                "Safari/537.36" % cm)
    if f in FIREFOX_FAMS:
        fv = REL_FIREFOX[k][1]
        if f == "ios_firefox":
            return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "FxiOS/%s Mobile/15E148 Safari/605.1.15" % (ios, fv))
        if f == "ipad_firefox":
            return ("Mozilla/5.0 (iPad; CPU OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/%s "
                    "Mobile/15E148 Safari/605.1.15" % (ios, fv))
        if f == "and_firefox":
            return "Mozilla/5.0 (Android %d; Mobile; rv:%s) Gecko/%s Firefox/%s" % (14 + x % 3, fv, fv, fv)
        if f == "andtab_firefox":
            return "Mozilla/5.0 (Android %d; Tablet; rv:%s) Gecko/%s Firefox/%s" % (14 + x % 3, fv, fv, fv)
        if f == "win_firefox":
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:%s) Gecko/20100101 Firefox/%s" % (fv, fv)
        if f == "mac_firefox":
            return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:%s) Gecko/20100101 Firefox/%s" % (fv, fv)
        return "Mozilla/5.0 (X11; Linux x86_64; rv:%s) Gecko/20100101 Firefox/%s" % (fv, fv)
    if f in SAMSUNG_FAMS:
        sv, sc = REL_SAMSUNG[k][1]
        return ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/%s Chrome/%s.0.0.0 "
                "%sSafari/537.36" % (sv, sc, "Mobile " if f == "and_samsung" else ""))
    if f in WEEKLY_FAMS:
        w, s = k // 16, k % 16
        if f == "ios_inapp":
            model, scale, res = IPHONES[x % len(IPHONES)]
            return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Mobile/15E148 Instagram %d.0.0.%d.%d (%s; iOS %s; de_DE; de; scale=%s; %s)"
                    % (ios, 402 + w, 24 + (w * 7) % 19, 86 + (w * 13) % 31, model, REL_IOS[s], scale, res))
        return ("Mozilla/5.0 (iPhone; CPU iPhone OS %s like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "GSA/%d.%d.%d Mobile/15E148 Safari/604.1" % (ios, 381 + w // 2, w % 2, 762104511 + 9871 * w))
    raise KeyError(f)


def addresses(sess_idx, gid, t_hours, local_hour, weekday, home, line):
    """each session's address with its last part set to zero: the household's line (its provider's block for the
    region, a new address each time the line reconnects), the phone's mobile network, or the office line on weekdays"""
    L = line
    isp = L["isp"][gid]; period = L["period"][gid]; phase = L["phase"][gid]
    epoch = np.floor((t_hours + phase) / period).astype(np.int64)
    slot = (_mix(gid, epoch) % np.uint64(BLOCK)).astype(np.int64)
    third = (home * BLOCK + slot) % 256
    out = np.empty(len(gid), dtype=object)
    fixed = np.array(FIXED, dtype=object)
    out[:] = [f % o for f, o in zip(fixed[isp], third)]
    u = (_mix(sess_idx, gid + 7) % np.uint64(10 ** 6)).astype(np.int64) / 1e6
    cell = (u < L["p_cell"][gid])
    if cell.any():
        car = L["carrier"][gid[cell]]
        oct3 = 64 + (_mix(sess_idx[cell], 11) % np.uint64(128)).astype(np.int64)
        mob = np.array(MOBILE, dtype=object)
        out[cell] = [f % o for f, o in zip(mob[car], oct3)]
    off = (L["office"][gid] >= 0) & (weekday < 5) & (local_hour >= 7.5) & (local_hour < 17.5) & ~cell
    if off.any():
        o_ = L["office"][gid[off]]
        offs = np.array(OFFICE, dtype=object)
        out[off] = [offs[j % 3] % ((h * BLOCK + j // 3) % 256) for j, h in zip(o_, home[off])]
    return out


class Records:
    def __init__(self, eds, q4, monthly, walls, seed=P.SEED):
        self.eds, self.q4, self.monthly, self.walls = eds, q4, monthly, walls
        self.rng = np.random.default_rng(seed + 101)
        self._browsers()
        self._sessions()
        self._accounts()

    # ------------------------------------------------------------------ browsers: ids, agents, addresses
    def _browsers(self):
        r = self.rng
        rows = []
        for E in self.eds:
            for b in range(E.n):
                ua, dev, br, os_ = _ua(E.family[b], r)
                r.integers(0, len(ISP)); r.integers(1, 255)          # the stream's earlier draws, kept in step
                rows.append((E.idx, b, E.family[b], dev, br, os_))
        B = pd.DataFrame(rows, columns=["home", "b", "family", "device_category", "browser", "os"])
        # each browser's line, update habit and device detail (their own stream)
        q = np.random.default_rng(P.SEED + 151)
        n = len(B)
        fam = B["family"].values
        isapple = np.isin(fam, ["ios_safari", "ios_chrome", "ios_inapp", "ios_gsa", "ios_firefox", "ios_edge",
                                "ipad_safari", "ipad_chrome", "ipad_firefox", "mac_safari"])
        habit = q.choice(3, n, p=[.55, .30, .15])
        lag_days = np.select([habit == 0, habit == 1], [q.exponential(4.0, n), q.exponential(21.0, n)], 400.0)
        auto = np.isin(fam, list(CHROME_FAMS | FIREFOX_FAMS)) & ~isapple
        lag_days = np.where(auto, np.minimum(lag_days, q.exponential(5.0, n)), lag_days)
        phone = B["device_category"].values == "mobile"
        tab = B["device_category"].values == "tablet"
        desk = B["device_category"].values == "desktop"
        self.line = {
            "isp": q.choice(len(FIXED), n, p=FIXED_P),
            "period": q.choice([24.0, 168.0, 720.0, 1e7], n, p=[.35, .25, .25, .15]),
            "carrier": q.choice(len(MOBILE), n, p=MOBILE_P),
            "p_cell": np.where(phone, q.beta(2.0, 2.5, n), np.where(tab, 0.08, 0.0)),
            "office": np.where(desk & (q.random(n) < 0.35), q.integers(0, 3 * BLOCK, n), -1),
            "lag": lag_days * 24.0,
            "extra": q.integers(0, 10 ** 6, n),
        }
        self.line["phase"] = q.random(n) * np.minimum(self.line["period"], 720.0)
        B["webkit"] = np.concatenate([E.webkit for E in self.eds])
        B["printed"] = np.concatenate([E.printed for E in self.eds])
        B["type"] = np.concatenate([E.type for E in self.eds])
        B["dev"] = np.concatenate([E.dev for E in self.eds])
        B["source"] = np.concatenate([E.source for E in self.eds])
        B["reg_day"] = np.concatenate([E.reg_day for E in self.eds])
        B["reg_time"] = np.concatenate([E.reg_time for E in self.eds])
        B["gid"] = np.arange(len(B))
        B["device_id"] = ["d%010x" % x for x in r.integers(0, 2 ** 40, len(B))]
        self.B = B
        self.gid = {E.idx: B.index[B["home"] == E.idx].values for E in self.eds}

    # ------------------------------------------------------------------ the fourth quarter's sessions
    def _sessions(self):
        r = self.rng
        S = W.sessions(self.eds, self.q4)
        gid = np.empty(len(S), np.int64)
        for h in range(len(self.eds)):
            m = S["home"].values == h
            gid[m] = self.gid[h][S["b"].values[m]]
        S["gid"] = gid
        # identifiers: one per browser and identifier counter
        key = S["gid"].values.astype(np.int64) * 10000 + S["cookie"].values
        ukey, first = np.unique(key, return_index=True)
        born = S["born"].values[first]
        counter = S["cookie"].values[first]
        wk = self.B["webkit"].values[S["gid"].values[first]]
        # an identifier still in use from before 2028 was written when the browser first came to the site
        old = (counter == 0) & ~wk
        born = np.where(old, -24.0 * r.integers(30, 2200, len(ukey)) - r.random(len(ukey)) * 24, born)
        born_unix = (EPOCH_UNIX + born * 3600).astype(np.int64)
        num = r.integers(10 ** 8, 2 * 10 ** 9 + 147483647, len(ukey))
        cid = np.char.add(np.char.add(num.astype(str), "."), born_unix.astype(str))
        assert len(set(cid)) == len(cid)
        S["client_id"] = cid[np.searchsorted(ukey, key)]
        self.ID = pd.DataFrame({"client_id": cid, "gid": ukey // 10000, "counter": ukey % 10000, "born": born})
        S["start_utc"] = EPOCH + pd.to_timedelta(np.round(S["start"].values * 3600), unit="s")
        S["end_utc"] = EPOCH + pd.to_timedelta(np.round(S["end"].values * 3600), unit="s")
        loc = local_of(S["start_utc"].values)
        S["month"] = loc.dt.month.values
        S["edition"] = np.array(P.CODES)[S["ed"].values]
        self.S = S

    # ------------------------------------------------------------------ accounts and the sign-in register
    def _accounts(self):
        """accounts: one for each signed-in browser, a share shared by two browsers of one reader, and accounts with no
        browser in the quarter; numbered in the order they were opened"""
        r = self.rng
        B = self.B
        signed = B["source"].values != ""
        idx = np.where(signed)[0]
        owner = np.full(len(B), -1, np.int64)
        owner[idx] = idx
        for (h, src_), grp in B[signed].groupby(["home", "source"]):
            g = grp.index.values.copy()
            r.shuffle(g)
            k = int(len(g) * P.SHARED_ACCOUNTS / 2)
            for a_, b_ in zip(g[:k], g[k:2 * k]):
                owner[b_] = owner[a_]
        origin = {"print": "print subscription", "registration": "registration", "subscription": "digital subscription"}
        rows = {}
        for i in idx:
            o = owner[i]
            if B.at[i, "source"] == "print":
                t = dt.datetime(2019, 3, 1) + dt.timedelta(minutes=int(r.integers(0, 60 * 24 * 365 * 8.7)))
            else:
                t = EPOCH + dt.timedelta(hours=float(B.at[i, "reg_time"]))
            src_ = B.at[o, "source"]
            prev = rows.get(o)
            rows[o] = (min(prev[0], t) if prev else t, origin[src_], P.CODES[B.at[o, "home"]], "active",
                       ("%02d-%07d" % (21 + B.at[o, "home"] % 4, r.integers(10 ** 6, 10 ** 7))) if src_ == "print" else "")
        extra = []
        for _ in range(6000):
            kind = r.choice(["print subscription", "registration", "digital subscription"], p=[.45, .5, .05])
            if kind == "print subscription":
                t = dt.datetime(2019, 3, 1) + dt.timedelta(minutes=int(r.integers(0, 60 * 24 * 365 * 9.5)))
            else:
                t = dt.datetime(2028, 3, 1) + dt.timedelta(minutes=int(r.integers(0, 60 * 24 * 270)))
            extra.append((t, kind, P.CODES[r.integers(0, 12)], "closed" if r.random() < 0.18 else "active",
                          ("%02d-%07d" % (21 + r.integers(0, 4), r.integers(10 ** 6, 10 ** 7))) if kind == "print subscription" else ""))
        keys = list(rows) + [-1 - j for j in range(len(extra))]
        vals = [rows[k] for k in rows] + extra
        order = np.argsort(np.array([v[0] for v in vals], dtype="datetime64[s]"), kind="stable")
        nos = 3000000 + np.cumsum(r.integers(1, 4, len(vals)))
        no_of = {keys[j]: int(nos[rank]) for rank, j in enumerate(order)}
        acct = np.full(len(B), -1, np.int64)
        acct[idx] = [no_of[owner[i]] for i in idx]
        B["account_no"] = acct
        self.acct_table = pd.DataFrame([(no_of[k],) + v for k, v in zip(keys, vals)],
                                       columns=["account_no", "created", "origin", "home_edition", "status", "subscriber_no"])

    # ------------------------------------------------------------------ the analytics export
    def export(self):
        """the analytics platform's export of the quarter's sessions: regular browsers, the newsroom, flagged
        automated traffic and the re-sent rows of 21 November"""
        r = np.random.default_rng(P.SEED + 202)
        S, B = self.S, self.B
        acct = B["account_no"].values[S["gid"].values]
        refs = {a: user_ref(a) for a in np.unique(acct[acct > 0])}
        uref = np.where(S["sig"].values & (acct > 0), pd.Series(acct).map(refs).values, None)
        code = S["edition"].values.astype(object)
        loc = local_of(S["start_utc"].values)
        before = (loc.dt.date.values < P.RECODE_DAY)
        for new, old in P.OLD_CODE.items():
            code = np.where((code == new) & before, old, code)
        g = S["gid"].values
        t_h = S["start"].values.astype(float)
        agents = agent_strings(B["family"].values[g], t_h, self.line["lag"][g], self.line["extra"][g])
        lhour = (loc.dt.hour + loc.dt.minute / 60.0).values
        addr = addresses(np.arange(len(S), dtype=np.int64), g, t_h, lhour, loc.dt.weekday.values,
                         S["home"].values.astype(np.int64), self.line)
        X = pd.DataFrame({
            "client_id": S["client_id"].values, "session_start": S["start_utc"].values, "session_end": S["end_utc"].values,
            "content_group": code, "page_views": S["pv"].values.astype(np.int16),
            "user_agent": agents, "device_category": B["device_category"].values[g],
            "browser": B["browser"].values[g], "os": B["os"].values[g],
            "ip_prefix": addr, "user_ref": uref, "is_bot": False})
        parts = [X, self._newsroom(r), self._bots(r, len(X))]
        X = pd.concat(parts, ignore_index=True)
        rep = X[(X["session_start"] >= REPLAY_FROM) & (X["session_start"] < REPLAY_TO)]
        X = pd.concat([X, rep], ignore_index=True)
        X = X.sort_values(["client_id", "session_start", "session_end"], kind="mergesort").reset_index(drop=True)
        return X

    def _newsroom(self, r):
        """the group's own staff reading the site from the newsroom's addresses (desktop, every edition)"""
        rows = []
        days = [P.Q4_START + dt.timedelta(days=i) for i in range((P.END - P.Q4_START).days + 1)]
        for j in range(P.INTERNAL_BROWSERS):
            fam = ["win_chrome", "win_edge"][j % 3 == 0]
            ua, dev, br, os_ = _ua(fam, r)
            cid = "%d.%d" % (r.integers(10 ** 8, 2 * 10 ** 9), EPOCH_UNIX - int(r.integers(10 ** 6, 10 ** 8)))
            for d in days:
                if d.weekday() >= 5 and r.random() < 0.85:
                    continue
                for _ in range(r.poisson(4.0)):
                    h = float(np.clip(r.normal(13.0, 3.0), 6.5, 22.5))
                    off = 2 if d < dt.date(2028, 10, 29) else 1
                    st = dt.datetime.combine(d, dt.time()) + dt.timedelta(hours=h - off)
                    en = st + dt.timedelta(seconds=int(r.gamma(2.0, 240)))
                    rows.append((cid, st, en, P.CODES[r.integers(0, 12)], int(1 + r.poisson(5)), ua, dev, br, os_,
                                 P.NEWSROOM_PREFIX.split("/")[0], None, False))
        X = pd.DataFrame(rows, columns=["client_id", "session_start", "session_end", "content_group", "page_views",
                                        "user_agent", "device_category", "browser", "os", "ip_prefix", "user_ref", "is_bot"])
        X["session_start"] = X["session_start"].dt.floor("s"); X["session_end"] = X["session_end"].dt.floor("s")
        # the newsroom's machines take every browser release within two days
        fam = np.where(X["browser"].values == "Edge", "win_edge", "win_chrome")
        t_h = (X["session_start"] - EPOCH).dt.total_seconds().values / 3600.0
        X["user_agent"] = agent_strings(fam, t_h, np.full(len(X), 48.0), np.zeros(len(X), np.int64))
        loc = local_of(X["session_start"].values)
        for new, old in P.OLD_CODE.items():
            X.loc[(X["content_group"] == new) & (loc.dt.date.values < P.RECODE_DAY), "content_group"] = old
        X["page_views"] = X["page_views"].astype(np.int16)
        return X

    def _bots(self, r, n_regular):
        """automated sessions the platform flags: a new identifier each time, at any hour"""
        n = int(n_regular * P.BOT_SHARE)
        agents = [("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/130.0.0.0 Safari/537.36", "desktop", "Chrome", "Linux"),
                  ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "desktop", "Chrome", "Windows"),
                  ("Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)", "desktop", "(not set)", "(not set)"),
                  ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "desktop", "Safari", "Macintosh")]
        q0 = (dt.datetime(2028, 9, 30, 22, 0) - EPOCH).total_seconds()
        q1 = (dt.datetime(2028, 12, 31, 23, 0) - EPOCH).total_seconds()
        st = EPOCH + pd.to_timedelta(np.sort(r.uniform(q0, q1, n)).round(), unit="s")
        a = r.choice(len(agents), n, p=[.45, .30, .15, .10])
        born = ((st - dt.datetime(1970, 1, 1)).total_seconds()).astype(np.int64)
        cid = np.char.add(np.char.add(r.integers(10 ** 8, 2 * 10 ** 9, n).astype(str), "."), born.astype(str))
        X = pd.DataFrame({"client_id": cid, "session_start": st, "session_end": st + pd.to_timedelta(r.integers(1, 40, n), unit="s"),
                          "content_group": np.array(P.CODES)[r.integers(0, 12, n)].astype(object),
                          "page_views": (1 + r.poisson(0.4, n)).astype(np.int16),
                          "user_agent": [agents[i][0] for i in a], "device_category": [agents[i][1] for i in a],
                          "browser": [agents[i][2] for i in a], "os": [agents[i][3] for i in a],
                          "ip_prefix": ["%d.%d.%d.0" % (r.integers(3, 200), r.integers(0, 255), r.integers(0, 255)) for _ in range(n)],
                          "user_ref": None, "is_bot": True})
        loc = local_of(X["session_start"].values)
        for new, old in P.OLD_CODE.items():
            X.loc[(X["content_group"] == new) & (loc.dt.date.values < P.RECODE_DAY), "content_group"] = old
        return X

    # ------------------------------------------------------------------ the sign-in register and the accounts
    def register(self):
        S, B = self.S, self.B
        s = S[S["sig"].values]
        g = pd.DataFrame({"account_no": B["account_no"].values[s["gid"].values], "device_id": B["device_id"].values[s["gid"].values],
                          "client_id": s["client_id"].values, "t": s["start_utc"].values})
        R = g.groupby(["account_no", "device_id", "client_id"], sort=True).agg(
            first_signed_in=("t", "min"), last_signed_in=("t", "max"), signed_in_sessions=("t", "size")).reset_index()
        return R

    def accounts(self):
        A = self.acct_table.copy()
        A["created"] = pd.to_datetime(A["created"]).dt.floor("s")
        return A.sort_values("account_no").reset_index(drop=True)

    # ------------------------------------------------------------------ the paywall log
    def paywall(self):
        rows = []
        idmap = self.ID.set_index(["gid", "counter"])["client_id"]
        for home, b, ed, t, cookie, out, since in self.walls:
            gid = self.gid[home][b]
            cid = idmap.get((gid, cookie))
            if cid is None:
                continue
            rows.append((EPOCH + dt.timedelta(hours=t), cid, P.CODES[ed], out, EPOCH + dt.timedelta(hours=float(since))))
        X = pd.DataFrame(rows, columns=["shown_utc", "client_id", "edition", "outcome", "meter_since_utc"])
        X["shown_local"] = local_of(X["shown_utc"].values).values
        X["since_local"] = local_of(X["meter_since_utc"].values).values
        for new, old in P.OLD_CODE.items():
            X.loc[(X["edition"] == new) & (X["shown_local"].dt.date < P.RECODE_DAY), "edition"] = old
        return X.sort_values("shown_utc").reset_index(drop=True)

    # ------------------------------------------------------------------ the platform's monthly report
    def report(self, X):
        """users (distinct identifiers) by content group and month, automated traffic and the newsroom left out;
        January to September from the year's tallies, the quarter from its sessions"""
        out = {}
        for E, tal in zip(self.eds, self.monthly):
            for m in range(9):
                T = tal[m]
                for slot in (0, 1):
                    a = T["act"][:, slot]
                    ids = np.where(a, T["c1"][:, slot] - T["c0"][:, slot] + 1, 0)
                    eds_ = np.where(slot == 0, E.idx, E.second)
                    for e in np.unique(eds_[a]):
                        out[(P.CODES[e], m + 1)] = out.get((P.CODES[e], m + 1), 0) + int(ids[a & (eds_ == e)].sum())
        q = X[~X["is_bot"] & (X["ip_prefix"] != P.NEWSROOM_PREFIX.split("/")[0])]
        loc = local_of(q["session_start"].values)
        cnt = pd.DataFrame({"g": q["content_group"].values, "m": loc.dt.month.values, "c": q["client_id"].values}).drop_duplicates()
        for (g_, m_), n in cnt.groupby(["g", "m"]).size().items():
            out[(g_, int(m_))] = int(n)
        rows = []
        for code in P.CODES:
            old = P.OLD_CODE.get(code)
            for c in ([old] if old else []) + [code]:
                row = {"content_group": c}
                for m in range(1, 13):
                    if old and c == code and m <= 10:
                        v = None
                    elif old and c == old:
                        v = out.get((code, m)) if m <= 9 else out.get((old, m))
                        v = None if m > 10 else v
                    else:
                        v = out.get((c, m))
                    row[m] = v
                rows.append(row)
        return pd.DataFrame(rows)


    # ------------------------------------------------------------------ the circulation system and the e-paper platform
    CIRC = {  # daily print, Saturday-only, combined print and e-paper, e-paper only, print trials, retail points
        "RHS": (4900, 770, 520, 770, 31, 50), "KBR": (6650, 910, 740, 630, 38, 58),
        "ALH": (2170, 320, 210, 230, 14, 25), "WBR": (2660, 450, 320, 420, 21, 32),
        "HOL": (3570, 490, 350, 320, 21, 34), "SOW": (1960, 350, 240, 320, 18, 25),
        "MST": (3850, 520, 380, 350, 24, 38), "GRH": (1500, 280, 180, 240, 14, 20),
        "EIT": (2940, 380, 280, 210, 18, 29), "BST": (1360, 240, 160, 180, 10, 18),
        "LDN": (1680, 320, 210, 280, 16, 22), "FKR": (2700, 350, 240, 190, 16, 27)}

    # the circulation system's release of 6 November 2028: its customer screen wrote the date a change of address, bank
    # details or payment was saved into the subscription's start date, until the fix of 14 December
    BUG_FROM, BUG_TO = dt.date(2028, 11, 6), dt.date(2028, 12, 14)
    LAUNCH = {"COMBI": dt.date(2011, 4, 1), "Digital Plus": dt.date(2011, 4, 1), "Digital Monthly": dt.date(2011, 4, 1),
              "Digital Annual": dt.date(2015, 9, 1), "App iOS": dt.date(2013, 6, 3), "App Android": dt.date(2013, 6, 3)}
    SYSTEM_FROM = dt.date(1999, 1, 4)        # the circulation system's go-live: older subscriptions carry this start

    def circulation(self):
        r = np.random.default_rng(P.SEED + 404)
        q0, q1 = dt.date(2028, 10, 1), dt.date(2028, 12, 31)
        subs, susp, acc, points, single = [], [], [], [], []
        sub_no = 2100000
        acc_no = 880000
        price = {"DAILY": (41.90, 44.90), "SATURDAY": (14.90, 16.90), "COMBI": (46.80, 49.80), "TRIAL": (0.0, 0.0)}
        refs = set()
        customers = set()

        def customer(ci):
            while True:
                x = "%02d-%07d" % (21 + ci % 4, r.integers(10 ** 6, 10 ** 7))
                if x not in customers:
                    customers.add(x)
                    return x

        def span(kind):
            """start and end of a record active at some time in the quarter"""
            u = r.random()
            if kind == "TRIAL":
                s = q0 + dt.timedelta(days=int(r.integers(-10, 85)))
                return s, s + dt.timedelta(days=13)
            if u < 0.030:                                           # started in the quarter, gift subscriptions in December
                s = q0 + dt.timedelta(days=int(r.integers(1, 90) if r.random() < 0.7 else r.integers(61, 85)))
            else:
                s = q0 - dt.timedelta(days=int(1 + min(r.exponential(13.5), 55.0) * 365.25))
                first = self.LAUNCH.get(kind)
                if first and s < first:
                    s = first + dt.timedelta(days=int(r.integers(0, (q0 - first).days)))
                s = max(s, self.SYSTEM_FROM)
            e = None
            if r.random() < 0.033:                                  # cancelled to a month end in the quarter
                e = [dt.date(2028, 10, 31), dt.date(2028, 11, 30), dt.date(2028, 12, 31)][r.integers(0, 3)]
                if e < s:
                    e = None
            return s, e

        def ref(fmt):
            while True:
                x = fmt()
                if x not in refs:
                    refs.add(x)
                    return x
        saved = {}                                                  # sub_no -> dates a change was saved in the quarter
        for ci, code in enumerate(P.CODES):
            nd, ns, nc, ne, nt, npt = self.CIRC[code]
            for kind, n in (("DAILY", nd), ("SATURDAY", ns), ("COMBI", nc), ("TRIAL", nt)):
                for _ in range(n):
                    sub_no += int(r.integers(1, 9))
                    s, e = span(kind)
                    copies = 1 if (kind != "DAILY" or r.random() > 0.018) else int(r.choice([2, 2, 3, 4, 5, 8, 10, 12]))
                    lo, hi = price[kind]
                    pr = round(copies * (lo if s.year < 2026 else hi), 2) if kind != "TRIAL" else 0.0
                    subs.append((sub_no, customer(ci), code, kind, copies, s, e, pr))
                    settled = kind != "TRIAL" and s < q0 - dt.timedelta(days=30)
                    marks = []
                    if settled and kind in ("DAILY", "SATURDAY") and r.random() < (0.105 if kind == "DAILY" else 0.05):
                        a = q0 + dt.timedelta(days=int(r.integers(0, 92)))
                        if r.random() < 0.3:
                            a = dt.date(2028, 12, int(r.integers(18, 28)))
                        b = a + dt.timedelta(days=int(r.integers(6, 22)))
                        k = r.choice(["pause", "forward", "donation"], p=[.65, .25, .10])
                        susp.append((sub_no, a, b, k))
                    if settled and r.random() < 0.011:                                       # address, bank or payment
                        marks.append(self.BUG_FROM + dt.timedelta(days=int(r.integers(0, (self.BUG_TO - self.BUG_FROM).days))))
                    if marks:
                        saved[sub_no] = marks
                    if kind == "COMBI":
                        acc_no += int(r.integers(1, 7))
                        acc.append((acc_no, code, "Digital Plus", s, e, 4.90, "Kombi %d" % sub_no, "web"))
            for _ in range(ne):
                acc_no += int(r.integers(1, 7))
                plan = str(r.choice(["Digital Monthly", "Digital Annual", "App iOS", "App Android"], p=[.42, .30, .17, .11]))
                s, e = span(plan)
                pr = {"Digital Monthly": 24.90, "Digital Annual": 239.00, "App iOS": 26.99, "App Android": 26.99}[plan]
                fmt = {"Digital Monthly": lambda: "WS-%d" % r.integers(10 ** 7, 10 ** 8), "Digital Annual": lambda: "WS-%d" % r.integers(10 ** 7, 10 ** 8),
                       "App iOS": lambda: "%d" % r.integers(10 ** 14, 10 ** 15),
                       "App Android": lambda: "GPA.%04d-%04d-%04d-%05d" % tuple(r.integers(0, 9999, 3).tolist() + [r.integers(0, 99999)])}[plan]
                acc.append((acc_no, code, plan, s, e, pr, ref(fmt), "app" if plan.startswith("App") else "web"))
            for _ in range(int(ne * 0.06)):                         # e-paper trials, two weeks free
                acc_no += int(r.integers(1, 7))
                s = q0 + dt.timedelta(days=int(r.integers(-10, 85)))
                acc.append((acc_no, code, "Trial 14 days", s, s + dt.timedelta(days=13), 0.0,
                            ref(lambda: "WS-%d" % r.integers(10 ** 7, 10 ** 8)), "web"))
            for j in range(npt):
                pt = "%s%03d" % (code, j + 1)
                typ = r.choice(["kiosk", "supermarket", "petrol station", "bakery", "tobacconist"], p=[.32, .22, .2, .14, .12])
                mean = {"kiosk": 26, "supermarket": 34, "petrol station": 14, "bakery": 9, "tobacconist": 18}[typ] * r.uniform(0.6, 1.5)
                rate = r.beta(7, 3)
                rest = int(r.choice([-1, 0, 2], p=[.80, .15, .05]))                      # weekly rest day, if any
                off = None
                if r.random() < 0.08:                                                      # closed for a holiday
                    a0 = dt.date(2028, 10, 9) + dt.timedelta(days=int(r.integers(0, 70)))
                    off = (a0, a0 + dt.timedelta(days=int(r.integers(6, 15))))
                points.append((pt, code, typ, round(mean, 2), round(rate, 3), rest, off))
        S_ = pd.DataFrame(subs, columns=["sub_no", "customer_no", "edition", "product", "copies", "start_date", "end_date", "monthly_price_eur"])
        U_ = pd.DataFrame(susp, columns=["sub_no", "from_date", "to_date", "kind"])
        A_ = pd.DataFrame(acc, columns=["access_id", "edition", "plan", "start_date", "end_date", "price_eur", "order_ref", "channel"])
        # numbers are handed out as orders come in: renumber subscriptions and accesses in order of their start
        g = np.random.default_rng(P.SEED + 414)
        S_ = S_.sort_values(["start_date", "sub_no"], kind="mergesort").reset_index(drop=True)
        new_no = 2100000 + np.cumsum(g.integers(1, 6, len(S_)))
        ren = dict(zip(S_["sub_no"], new_no))
        # the release's start dates: the last change saved while it ran, on a subscription still being delivered
        hit = {}
        end_of = dict(zip(S_["sub_no"], S_["end_date"]))
        for k, marks in saved.items():
            e_ = end_of[k]
            inwin = [m for m in marks if self.BUG_FROM <= m < self.BUG_TO and (e_ is None or pd.isna(e_) or m <= e_)]
            if inwin:
                hit[ren[k]] = max(inwin)
        S_["sub_no"] = new_no
        S_["true_start"] = S_["start_date"]
        S_["start_date"] = [hit.get(k, s) for k, s in zip(S_["sub_no"], S_["start_date"])]
        self.circ_truth = S_[["sub_no", "edition", "product", "true_start", "start_date"]].copy()
        S_ = S_.drop(columns=["true_start"])
        U_["sub_no"] = U_["sub_no"].map(ren)
        U_ = U_.sort_values(["from_date", "sub_no"], kind="mergesort").reset_index(drop=True)
        kombi = A_["order_ref"].str.startswith("Kombi ")
        A_.loc[kombi, "order_ref"] = ["Kombi %d" % ren[int(x.split()[1])] for x in A_.loc[kombi, "order_ref"]]
        A_ = A_.sort_values(["start_date", "access_id"], kind="mergesort").reset_index(drop=True)
        A_["access_id"] = 880000 + np.cumsum(g.integers(1, 5, len(A_)))
        T_ = pd.DataFrame(points, columns=["retail_point", "edition", "type", "_mean", "_rate", "_rest", "_off"])
        # single copies: every issue of the quarter at every retail point
        for code in P.CODES:
            days = pub_days(code)
            pts = T_[T_["edition"] == code]
            for d in days:
                sat = 1.35 if d.weekday() == 5 else 1.0
                dl = r.poisson(pts["_mean"].values * sat)
                sold = r.binomial(dl, pts["_rate"].values)
                for pt, a, b, rest, off in zip(pts["retail_point"].values, dl, sold, pts["_rest"].values, pts["_off"].values):
                    shut = d.weekday() == rest or (off is not None and off[0] <= d <= off[1])
                    if a > 0 and not shut:
                        single.append((d, pt, int(a), int(a - b)))
        X_ = pd.DataFrame(single, columns=["issue_date", "retail_point", "delivered", "returned"])
        return S_, U_, A_, T_.drop(columns=["_mean", "_rate", "_rest", "_off"]), X_

    # ------------------------------------------------------------------ the newsletter platform
    NL = {"RHS": 2700, "KBR": 1800, "ALH": 900, "WBR": 1650, "HOL": 1050, "SOW": 1350, "MST": 1200, "GRH": 900,
          "EIT": 750, "BST": 750, "LDN": 1140, "FKR": 720}

    def newsletter(self, attempt=0):
        """contacts of the one local-newsletter list, a group per edition; each contact's history simulated month by
        month from its sign-up; the platform keeps six months of activity"""
        r = np.random.default_rng(P.SEED + 505 + attempt)
        start, stop = dt.datetime(2019, 6, 1), EXPORT_AT
        span_s = (stop - start).total_seconds()
        codes = P.CODES
        weights = np.array([self.NL[c] for c in codes], float)
        n = int(weights.sum() * 1.9)
        contacts, events, gchanges = [], [], []
        for cid in range(n):
            t0 = start + dt.timedelta(seconds=float(span_s * (1 - r.random() ** 1.6)))
            k = 1 if r.random() < 0.85 else (2 if r.random() < 0.87 else 3)
            groups = set(r.choice(codes, k, replace=False, p=weights / weights.sum()).tolist())
            g0 = set(groups)
            ev = [("subscribed", t0)]
            status = "pending"
            if r.random() < 0.89:
                tc = t0 + dt.timedelta(minutes=float(r.gamma(1.2, 400)))
                if tc < stop:
                    ev.append(("confirmed", tc)); status = "subscribed"
            t = ev[-1][1]
            gl, cl = [], []
            # the box under the newsletters from 7 November, and the new year's mailing, offered a neighbouring edition's
            # newsletter with one click (the link adds the group; only editions the contact does not receive are offered)
            due = []
            if r.random() < 0.030:
                due.append(PROMO_FROM + dt.timedelta(seconds=float(r.uniform(0, (PROMO_TO - PROMO_FROM).total_seconds()))))
            if r.random() < 0.060:
                due.append(CAMPAIGN_FROM + dt.timedelta(seconds=float(r.uniform(0, (CAMPAIGN_TO - CAMPAIGN_FROM).total_seconds()))))
            due.sort()

            def clicks_before(limit):
                while due and due[0] < limit:
                    tc_ = due.pop(0)
                    if status == "subscribed" and tc_ > t:
                        offer = [c for c in codes if c not in groups]
                        if offer:
                            w_ = np.array([self.NL[c] for c in offer], float)
                            add = str(r.choice(offer, p=w_ / w_.sum()))
                            groups.add(add)
                            cl.append((tc_, add))
            while status in ("subscribed", "unsubscribed") and t < stop:
                t_next = t + dt.timedelta(days=float(r.exponential(30.4)))
                clicks_before(min(t_next, stop))
                t = t_next
                if t >= stop:
                    break
                u = r.random()
                if status == "subscribed":
                    if u < 0.0125:
                        status = "unsubscribed"; ev.append(("unsubscribed", t))
                    elif u < 0.0150:
                        status = "cleaned"; ev.append(("cleaned", t))
                    elif u < 0.0240:
                        before = set(groups)
                        v = r.random()
                        if v < 0.40 or len(groups) == 1 and v < 0.70:
                            groups.add(str(r.choice(codes, p=weights / weights.sum())))
                        elif len(groups) > 1 and v < 0.70:
                            groups.discard(sorted(groups)[r.integers(0, len(groups))])
                        else:
                            groups = {str(r.choice(codes, p=weights / weights.sum()))}
                        if groups != before:
                            gl.append((t, "|".join(sorted(before)), "|".join(sorted(groups))))
                else:
                    if u < 0.006:
                        status = "subscribed"; ev.append(("resubscribed", t))
            src = r.choice(["website form", "account registration", "print activation", "event sign-up", "import 2021"],
                           p=[.46, .27, .15, .05, .07]) if t0 > dt.datetime(2021, 5, 1) else "import 2021"
            if status == "pending" and t0 < EXPORT_AT - dt.timedelta(days=30):
                continue                                            # the platform deletes unconfirmed sign-ups after 30 days
            # article links clicked in the newsletters while subscribed, inside the log's six months
            reads = []
            on = None
            for e_, t_ in ev + [("end", stop)]:
                if e_ in ("confirmed", "resubscribed"):
                    on = t_
                elif on is not None:
                    a_, b_ = max(on, LOG_FROM), min(t_, stop)
                    if b_ > a_:
                        k_ = r.poisson(0.7 * (b_ - a_).total_seconds() / (86400 * 30.4))
                        for x_ in np.sort(r.uniform(0, (b_ - a_).total_seconds(), k_)):
                            reads.append((a_ + dt.timedelta(seconds=float(x_)), int(r.integers(0, 10 ** 6))))
                    on = None
            contacts.append((cid, t0, status, set(groups), ev, gl, src, cl, reads, g0))
        return contacts

    def newsletter_tables(self):
        """the contact export, the activity log and the preference centre's group-change log; redrawn until every
        edition's group has preference-centre changes after the year's end that do not cancel, and groups added by a
        link both before and after it"""
        for attempt in range(40):
            C = self.newsletter(attempt)
            net = {c: 0 for c in P.CODES}
            late = {c: 0 for c in P.CODES}
            early = {c: 0 for c in P.CODES}
            for cid, t0, status, groups, ev, gl, src, cl, reads, g0 in C:
                for t, b, a in gl:
                    if t >= YEAR_END_UTC:
                        for g in set(a.split("|")) - set(b.split("|")):
                            net[g] += 1
                        for g in set(b.split("|")) - set(a.split("|")):
                            net[g] -= 1
                for t, g in cl:
                    (late if t >= YEAR_END_UTC else early)[g] += 1
            if all(net[c] != 0 and late[c] > 0 and early[c] > 0 for c in P.CODES):
                break
        r = np.random.default_rng(P.SEED + 606)
        hashes = {cid: hashlib.md5(("nl-%d-%d" % (cid, r.integers(10 ** 9))).encode()).hexdigest() for cid, *_ in C}
        crow, erow, grow = [], [], []
        C = sorted(C, key=lambda c: (c[1], c[0]))
        idmap = {c[0]: 100000 + j * 3 + int(r.integers(0, 3)) for j, c in enumerate(C)}
        for cid, t0, status, groups, ev, gl, src, cl, reads, g0 in C:
            last = max([t for _, t in ev] + [t for t, _, _ in gl] + [t for t, _ in cl])
            crow.append((idmap[cid], hashes[cid], status, "|".join(sorted(groups)), t0, last, src))
            for e, t in ev:
                if LOG_FROM <= t < EXPORT_AT:
                    erow.append((idmap[cid], e, t, ""))
            for t, g in cl:
                if LOG_FROM <= t < EXPORT_AT:
                    erow.append((idmap[cid], "clicked", t, ADD_LINK % SLUG[g]))
            mine = sorted(groups)
            for t, k in reads:
                erow.append((idmap[cid], "clicked", t, article_link(mine[k % len(mine)], t, k)))
            for t, b, a in gl:
                if LOG_FROM <= t < EXPORT_AT:
                    grow.append((idmap[cid], t, b, a))
        Ct = pd.DataFrame(crow, columns=["contact_id", "email_md5", "status", "groups", "first_optin_utc", "last_changed_utc", "source"])
        Et = pd.DataFrame(erow, columns=["contact_id", "event", "at_utc", "link"]).sort_values(["at_utc", "contact_id"]).reset_index(drop=True)
        Gt = pd.DataFrame(grow, columns=["contact_id", "changed_utc", "groups_before", "groups_after"]).sort_values(["changed_utc", "contact_id"]).reset_index(drop=True)
        for df, cols in ((Ct, ["first_optin_utc", "last_changed_utc"]), (Et, ["at_utc"]), (Gt, ["changed_utc"])):
            for c in cols:
                df[c] = pd.to_datetime(df[c]).dt.floor("s")
        self.nl_contacts = C
        return Ct, Et, Gt

    # ------------------------------------------------------------------ distractors
    def ad_delivery(self):
        r = np.random.default_rng(P.SEED + 707)
        rows = []
        for d in pd.date_range("2028-10-01", "2028-12-31"):
            for code in P.CODES:
                for dev, base in (("mobile", 3.1), ("tablet", 0.35), ("desktop", 1.4)):
                    imp = int(r.poisson(base * 1000 * (1.2 if d.weekday() < 5 else 0.9) * self.CIRC[code][0] / 9000))
                    rows.append((d.date(), code, dev, imp, int(imp * r.uniform(0.52, 0.66)), round(r.uniform(0.9, 2.6), 2)))
        return pd.DataFrame(rows, columns=["date", "edition", "device", "impressions_served", "impressions_viewable", "ecpm_eur"])

    def reach_survey(self):
        r = np.random.default_rng(P.SEED + 808)
        rows = []
        for code in P.CODES:
            base = self.CIRC[code][0]
            rows.append((code, int(round(base * r.uniform(2.1, 2.6), -2)), round(r.uniform(18, 31), 1), int(r.integers(41, 64)),
                         int(r.integers(180, 620))))
        return pd.DataFrame(rows, columns=["edition", "readers_per_issue", "reach_pct_of_population_14plus", "median_reader_age", "interviews"])


def pub_days(code):
    """the edition's publication days in the fourth quarter: Monday to Saturday, not on its state's public holidays"""
    state = {e["code"]: e["state"] for e in P.EDITIONS}[code]
    out = []
    d = dt.date(2028, 10, 1)
    while d <= dt.date(2028, 12, 31):
        if d.weekday() < 6 and d not in P.HOLIDAYS[state]:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def build(seed=P.SEED):
    eds, q4, monthly, walls = W.simulate(seed)
    return Records(eds, q4, monthly, walls, seed)
