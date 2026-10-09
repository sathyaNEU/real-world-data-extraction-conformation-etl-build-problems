"""task122 generator: home-carousel traffic by week, the R2 restatement and the app release calendar.

The weekly sessions table counts logged-in home-carousel sessions by ISO week, platform and buyer
tenure band. Its first release banded each session by the buyer account's own creation date, so a
buyer whose older account had been merged in was counted as newer than they are; from 2026-W27 the
table bands by the oldest merged account (the account service's tenure, the one the carousel logger
stamps), and restatement R2 re-bands 2026-W01 to W26 the same way. R2 moves sessions from the two
younger bands to the two older ones and leaves every platform-week total unchanged.
"""
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P

BAND_LABELS = ["0-29", "30-179", "180-729", "730+"]
FIX_WEEK = (2026, 27)     # first week the table bands by the oldest merged account


def iso_monday(year, week):
    return date.fromisocalendar(year, week, 1)


def weeks():
    out = []
    for y in (2025, 2026):
        last = date(y, 12, 28).isocalendar()[1]
        for w in range(1, last + 1):
            if (y, w) <= (2026, 39):
                out.append((y, w))
    return out


def true_table(adjust=None):
    """Sessions by (year, week, platform, band) as the account service would band them."""
    rng = P.stream("traffic")
    rows = []
    for (y, w) in weeks():
        mon = iso_monday(y, w)
        doy = (mon - date(y, 1, 1)).days
        season = (1.0 + 0.10 * np.exp(-((w - 2.5) / 2.2) ** 2) - 0.09 * np.exp(-((w - 31) / 4.5) ** 2)
                  + 0.11 * np.exp(-((w - 48.5) / 2.0) ** 2) + 0.06 * np.exp(-((w - 51) / 1.2) ** 2))
        growth = 1.0 if y == 2026 else 0.935
        total = 2.43e6 * season * growth * (1 + rng.normal(0, 0.012))
        app = 0.647 if y == 2026 else 0.622
        app += rng.normal(0, 0.004)
        # new buyers arrive after the holidays: the two younger bands swell in January and February
        jan = np.exp(-((w - 2.5) / 3.5) ** 2)
        t1 = 0.112 + 0.080 * jan + 0.010 * np.exp(-((w - 48.5) / 2.5) ** 2)
        t2 = 0.221 + 0.040 * jan
        shares = np.array([t1, t2, 0.303, 1 - t1 - t2 - 0.303])
        for pi_, plat in enumerate(P.PLATFORMS):
            pt = total * (app if plat == "app" else 1 - app)
            sh = shares * (1 + rng.normal(0, 0.01, 4))
            sh = sh / sh.sum()
            for b in range(4):
                v = pt * sh[b]
                if adjust is not None and y == 2026 and w in P.ISO_WEEKS_SLOT:
                    v *= adjust[pi_ * 4 + b]
                rows.append((y, w, mon, plat, b, int(round(v))))
    return pd.DataFrame(rows, columns=["year", "week", "week_start", "platform", "band", "sessions"])


def first_release(true):
    """The first release: up to 2026-W26, a share of each platform-week's sessions sits in the two
    younger bands that the account service puts in the two older ones."""
    rng = P.stream("traffic-r1")
    out = true.copy()
    for (y, w, plat), g in true.groupby(["year", "week", "platform"], sort=True):
        if (y, w) >= FIX_WEEK:
            continue
        tot = g.sessions.sum()
        move = int(round(tot * (P.R2_MOVED_SHARE + rng.normal(0, 0.0025))))
        idx = g.index.to_numpy()          # bands 0..3
        old = g.sessions.to_numpy()[2:].astype(float)
        take = np.floor(move * old / old.sum()).astype(int)
        take[0] += move - take.sum()
        young = g.sessions.to_numpy()[:2].astype(float)
        give = np.floor(move * young / young.sum()).astype(int)
        give[0] += move - give.sum()
        out.loc[idx[2:], "sessions"] -= take
        out.loc[idx[:2], "sessions"] += give
    return out


def r2_table(true):
    return true[(true.year == 2026) & (true.week <= 26)].copy()


def arm_sessions(table, app_weeks=P.APP_WEEKS, web_weeks=P.ISO_WEEKS_SLOT, year=2026, share=P.SLOT_SHARE):
    """Planned arm sessions by cell: the slot's share of each platform's sessions on the same ISO
    weeks one year before the slot; app cells only from the first app release (W03)."""
    out = np.zeros(8)
    for c in range(8):
        plat = P.PLATFORMS[c // 4]
        b = c % 4
        wk = app_weeks if plat == "app" else web_weeks
        m = (table.year == year) & table.week.isin(wk) & (table.platform == plat) & (table.band == b)
        out[c] = share * table.loc[m, "sessions"].sum()
    return out


def release_calendar():
    """App releases (iOS and Android together) every other Monday, a code freeze over the year end,
    the first 2027 release on 18 January."""
    ev = []
    d = date(2026, 1, 12)
    ver = 1
    while d <= date(2026, 12, 7):
        ev.append((d, f"26.{ver}", "App release 26.%d (iOS, Android)" % ver))
        d += timedelta(days=14)
        ver += 1
    ev.append((date(2026, 12, 14), None, "App code freeze (no store releases until 17 January)"))
    d = date(2027, 1, 18)
    ver = 1
    while d <= date(2027, 6, 28):
        ev.append((d, f"27.{ver}", "App release 27.%d (iOS, Android)" % ver))
        d += timedelta(days=14)
        ver += 1
    return ev


def ics_text():
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Vouwlijn//Mobile Release Train//NL",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Vouwlijn app releases 2026-2027", "X-WR-TIMEZONE:Europe/Amsterdam"]
    for d, ver, summary in release_calendar():
        uid = f"{d.strftime('%Y%m%d')}-{(ver or 'freeze').replace('.', '-')}@releases.vouwlijn.nl"
        lines += ["BEGIN:VEVENT", f"UID:{uid}", "DTSTAMP:20260930T081500Z",
                  f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}"]
        if ver is None:
            end = date(2027, 1, 18)
            lines.append(f"DTEND;VALUE=DATE:{end.strftime('%Y%m%d')}")
            lines.append(f"SUMMARY:{summary}")
            lines.append("DESCRIPTION:Release train paused for the holiday period. Store submissions resume "
                         "with 27.1.")
        else:
            lines.append(f"DTEND;VALUE=DATE:{(d + timedelta(days=1)).strftime('%Y%m%d')}")
            lines.append(f"SUMMARY:{summary}")
            lines.append("DESCRIPTION:Staged rollout to 100 per cent of app users over the release day. "
                         "Release manager: Mobile Platform.")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def weekly_frame(table):
    df = table.copy()
    df["iso_week"] = [f"{y}-W{w:02d}" for y, w in zip(df.year, df.week)]
    df["tenure_band"] = [BAND_LABELS[b] for b in df.band]
    df["week_start"] = [d.isoformat() for d in df.week_start]
    df = df.sort_values(["year", "week", "platform", "band"], kind="stable")
    return df[["iso_week", "week_start", "platform", "tenure_band", "sessions"]].rename(
        columns={"sessions": "logged_in_sessions"})
