"""The dashboard's development plans: from Monday 1 November 2027 each reported team's leader can choose up to three items
on the team's page as the team's development targets and send the plan to their manager to agree. The plans module
saved each target as the item's row on the team's page (the page lists the items from the team's lowest percent
favourable to its highest) until the release of Monday 8 November, and as the item code from then on; leaders whose plan
summary then showed the wrong items saved their plans again. Written from its own random stream, apart from the survey
world, after the dashboard's pages are made from the shipped returns."""
import datetime as dt
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import postprocess

ITEMS = [it[0] for it in P.ITEMS]
SEED = 175                                         # screened: every plan figure apart under every wrong read
OPEN = dt.date(2027, 11, 1)
RELEASE = dt.datetime(2027, 11, 8, 7, 0)           # the plans module saves the item code from this release
EXPORT = dt.datetime(2027, 11, 19, 16, 20)
P_PLAN = 0.63                                      # reported teams whose leader has saved a plan by the export
K_P = (0.3, 0.45, 0.25)                            # one, two or three targets
DECAY = 0.33                                       # leaders choose from the top of the page, the team's lowest items
P_RESAVE = 0.28                                    # earlier plans saved again after the release, the same items
P_EDIT = 0.10                                      # plans saved again with one target changed
COLUMNS = ["plan_ref", "version", "team_code", "team_name", "saved_at_local", "target_1", "target_2", "target_3",
           "status"]


def shown(fav, base):
    """an item's percent favourable as the team page shows it: one decimal place"""
    return float((Decimal(100 * int(fav)) / Decimal(int(base))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def page_order(fav, base):
    """the team page's items, from the team's lowest percent favourable to its highest, ties in Table 1 order"""
    vals = [(shown(f, b), k) for k, (f, b) in enumerate(zip(fav, base))]
    return [ITEMS[k] for v, k in sorted(vals)]


def team_counts(R, reported):
    U = R[R["team"].isin(reported)]
    base = U.groupby("team")[ITEMS].count()
    fav = U.groupby("team")[ITEMS].agg(lambda s: int((s >= 4).sum()))
    return fav, base


def team_pages(R, reported):
    fav, base = team_counts(R, reported)
    assert int(base.values.min()) > 0, "every reported team has an answer on the scale for every item"
    return {t: page_order(fav.loc[t].values, base.loc[t].values) for t in sorted(reported)}


def _working_days(a, b):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        n += d.weekday() < 5
    return n


def simulate(pages, seed=SEED):
    """every version of every plan saved by the export: the team, when, and the items the leader chose"""
    rng = np.random.default_rng(seed)
    days = [OPEN + dt.timedelta(days=k) for k in range(19) if (OPEN + dt.timedelta(days=k)).weekday() < 5]
    w_day = np.array([3.0 if d < RELEASE.date() else (1.6 if d < dt.date(2027, 11, 15) else 1.0) for d in days])
    w_row = np.exp(-DECAY * np.arange(12))
    w_row = w_row / w_row.sum()

    def when(after=None):
        ok = [k for k, d in enumerate(days) if after is None or d >= after.date()]
        if not ok:
            return None
        w = w_day[ok] / w_day[ok].sum()
        for _ in range(100):
            d = days[ok[int(rng.choice(len(ok), p=w))]]
            t = dt.datetime.combine(d, dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(0, 570)))
            if (after is None or t > after) and t < EXPORT:
                return t
        return None

    plans = []
    for t in sorted(pages):
        if rng.random() >= P_PLAN:
            continue
        k = int(rng.choice([1, 2, 3], p=K_P))
        rows = sorted(int(x) for x in rng.choice(12, k, replace=False, p=w_row))
        t1 = when()
        versions = [dict(at=t1, items=[pages[t][r] for r in rows])]
        u = rng.random()
        if t1 < RELEASE and u < P_RESAVE:
            t2 = when(after=max(t1, RELEASE) + dt.timedelta(minutes=30))
            if t2 is not None:
                versions.append(dict(at=t2, items=list(versions[0]["items"])))
        elif u < P_RESAVE + P_EDIT:
            # a change of mind a day or more later; the summary after the release showed every earlier plan's
            # targets wrongly, so a leader who saved again after it re-entered the items the plan already held
            t2 = when(after=t1 + dt.timedelta(hours=20))
            if t2 is not None and (t2 < RELEASE) == (t1 < RELEASE):
                keep = list(versions[0]["items"])
                others = [x for x in pages[t] if x not in keep]
                w = np.array([w_row[pages[t].index(x)] for x in others])
                new = others[int(rng.choice(len(others), p=w / w.sum()))]
                keep[int(rng.integers(len(keep)))] = new
                versions.append(dict(at=t2, items=sorted(keep, key=pages[t].index)))
        plans.append(dict(team=t, versions=versions))
    # each plan's latest version as it stands at the export; the earlier versions are replaced
    for p in plans:
        last = p["versions"][-1]
        age = _working_days(last["at"].date(), EXPORT.date())
        if rng.random() < min(0.8, 0.12 + 0.06 * age):
            last["status"] = "Agreed"
        else:
            last["status"] = "With manager" if rng.random() < 0.7 else "Draft"
        for v in p["versions"][:-1]:
            v["status"] = "Replaced"
    # plan references in the order plans were started, with the gaps left by plans started and deleted
    plans.sort(key=lambda p: p["versions"][0]["at"])
    ref = 1
    for p in plans:
        ref += 1 + int(rng.poisson(0.15))
        p["ref"] = "DP-%04d" % ref
    return plans


def rows(plans, pages, names):
    out = []
    for p in plans:
        for n, v in enumerate(p["versions"], 1):
            if v["at"] < RELEASE:
                targets = [pages[p["team"]].index(x) + 1 for x in v["items"]]
            else:
                targets = list(v["items"])
            targets += [None] * (3 - len(targets))
            out.append([p["ref"], n, p["team"], names[p["team"]], v["at"]] + targets + [v["status"]])
    out.sort(key=lambda r: (r[4], r[0]))
    return out


def write(path, plans, pages, names):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plans"
    ws.append(COLUMNS)
    for r in rows(plans, pages, names):
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F1")
    for row in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "dd/mm/yyyy hh:mm"
    for i, w in enumerate([11, 8, 11, 34, 17, 10, 10, 10, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=1):
        for c in row:
            c.alignment = Alignment(vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:I%d" % ws.max_row
    wb.save(path)
    postprocess.scrub(path, "Staff Voice dashboard", "2027-11-19")
    postprocess.finish_office(path, "2027-11-19T16:20:00Z", "2027-11-19T16:20:00Z", "Lowfirth Parcels")


def frame(plans, pages):
    """the plans as a table of versions with the items each names (the generator's truth)"""
    out = []
    for p in plans:
        for n, v in enumerate(p["versions"], 1):
            out.append(dict(ref=p["ref"], version=n, team=p["team"], at=v["at"], items=tuple(v["items"]),
                            status=v["status"], pre=v["at"] < RELEASE))
    return pd.DataFrame(out)
