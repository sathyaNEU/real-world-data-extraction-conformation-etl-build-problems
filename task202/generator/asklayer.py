"""The closed period's own records: the Office's pre-payment claim check and the Treasury's archived
payment runs, for claim months July 2024 to December 2025.

Nothing here touches the twelve months to 31 March 2027. The referral ceiling is struck on the claim
returns' own totals and counts for that window and on the portal's awards inside it; every row this
module produces sits in a claim month that closed before the window opened, in two files the ceiling
never reads, which is what keeps the ask layer off the main call's population.

What the closed period holds, and why each shape is in the record rather than placed there:

* the check held an amount back on about one partner-month in six, and the claims system writes the
  two currency columns as the partner's position in the scheme year rather than the month's own
  figure, because the finance report the columns were added for is a year-to-date report. The award
  count column was left alone. Nothing says so; the row's own amount above the month's claim and the
  July reset are what say so.
* the 2024/25 year-end reconciliation checked some partner-months again and released part of a hold,
  so those partner-months carry the original check and the later one.
* the reason was a free-text field until the April 2025 release made it a list, so the earlier
  entries are the same five reasons written in whatever case and punctuation the checker used.
* the Treasury settles a partner's two half-month runs on one payment instruction when the first
  half's release was held back for a mandate re-validation, and the archive is an export of
  instructions against run lines, so the instruction's amounts land on both lines it covers.
* a recovery is applied against the partner's next transfer, not against the month it was claimed
  back in.
* a few partner-months were released in a run dated after the archive's cut-off and are not in it.
"""
import datetime as dt

import numpy as np

import params as P
import sim

MONTHS = [t for t in sim.MONTHS if P.CHECK_FROM <= t <= P.CHECK_TO]
IDX = {t: i for i, t in enumerate(MONTHS)}


def scheme_year(mo):
    """The scheme year a claim month falls in, named by its opening calendar year."""
    return mo[0] if mo[1] >= P.SCHEME_YEAR_START else mo[0] - 1


def quarter(mo):
    """(scheme year, quarter) with the scheme year opening in July, as the workbooks label it."""
    return scheme_year(mo), (mo[1] - P.SCHEME_YEAR_START) % 12 // 3 + 1


def qlabel(q):
    y, n = q
    return "%d/%s Q%d" % (y, str(y + 1)[2:], n)


QUARTERS = []
for _t in MONTHS:
    if quarter(_t) not in QUARTERS:
        QUARTERS.append(quarter(_t))


def next_month(mo):
    y, m = mo
    return (y + (m == 12), m % 12 + 1)


def half(day):
    return 1 if day <= 15 else 2


class Closed:
    """The closed period's truth, built once from the simulated awards."""

    def __init__(self, W, parts, ledger):
        self.W = W
        self.parts = parts
        self.ledger = ledger
        self.cells = {}          # (partner, claim month) -> dict of the month's truth
        self._build()

    # ---------------------------------------------------------------- the check
    def _build(self):
        bymonth = {}
        for a in self.W["awards"]:
            if not (P.CHECK_FROM <= a["month"] <= P.CHECK_TO):
                continue
            bymonth.setdefault((a["partner"], a["month"]), []).append(a)
        recov = self._recoveries()
        for key in sorted(bymonth):
            pi, mo = key
            aws = sorted(bymonth[key], key=lambda a: (a["paid"], a["amount"], a["band"]))
            r = sim.stream(41, pi, IDX[mo])
            claimed_n = len(aws)
            claimed = round(sum(a["amount"] for a in aws), 2)
            held, held_extra, reason = [], [], ""
            if r.random() < P.HOLD_RATE and claimed_n >= P.HOLD_AWARDS[1]:
                k = int(r.integers(*P.HOLD_AWARDS))
                pick = sorted(r.choice(claimed_n, size=k, replace=False).tolist())
                held = [aws[i] for i in pick]
                if mo >= P.REASON_FROM or r.random() < P.REASON_EARLY:
                    reason = P.HOLD_REASONS[int(r.choice(len(P.HOLD_REASONS), p=P.REASON_W))]
                    if mo < P.REASON_FROM:
                        reason = P.REASON_STYLE[int(r.integers(0, len(P.REASON_STYLE)))](reason)
                # the month is checked again where the partner answered the hold and one award
                # was released, so the register holds the original check and the later one
                if r.random() < P.RECHECK_RATE:
                    rest = [i for i in range(claimed_n) if i not in pick]
                    if rest:
                        held_extra = [aws[rest[int(r.integers(0, len(rest)))]]]
            recd = dt.date(*next_month(mo), 1) + dt.timedelta(days=3 + int(r.integers(0, 9)))
            chk = recd + dt.timedelta(days=2 + int(r.integers(0, 7)))
            self.cells[key] = dict(
                partner=pi, month=mo, awards=aws, claimed_n=claimed_n, claimed=claimed,
                held=held, held_extra=held_extra, reason=reason,
                held_amount=round(sum(a["amount"] for a in held), 2),
                held_n=len(held), received=recd, checked=chk,
                checker="CHK-%02d" % (1 + (pi * 5 + IDX[mo]) % P.CHECKERS),
                recovery=recov.get(key, 0.0),
                deferred=bool(r.random() < P.DEFER_RATE),
                consolidated=False)
        # a run the Treasury has to net a recovery against is not one it defers
        for c in self.cells.values():
            if c["recovery"] > 0:
                c["deferred"] = False
        # the payment instruction that settles both halves of a partner's claim month
        for key, c in self.cells.items():
            r = sim.stream(42, key[0], IDX[key[1]])
            halves = {half(a["paid"].day) for a in c["awards"] if a not in c["held"]}
            c["consolidated"] = (not c["deferred"] and len(halves) == 2
                                 and r.random() < P.CONSOL_RATE)

    def _recoveries(self):
        """The three awards recovered inside the 2024/25 returns, each applied against the partner's
        next transfer rather than against the month it was claimed back in."""
        out = {}
        self.recovery_lines = []
        for prov, slot, mo, band in P.ASK_RECOVERIES:
            pi = [p["idx"] for p in self.parts if p["province"] == prov and p["slot"] == slot][0]
            cand = sorted([a for a in self.W["awards"] if a["partner"] == pi and a["band"] == band
                           and a["month"] < mo and a["month"] >= P.CHECK_FROM],
                          key=lambda a: (a["paid"], a["amount"]))
            a = cand[-1]
            self.recovery_lines.append((mo, self.ledger[pi], band, a["amount"], a["paid"]))
            out[(pi, next_month(mo))] = round(a["amount"], 2)
        return out

    # ---------------------------------------------------------------- what each month really is
    def monthly(self, key):
        c = self.cells[key]
        return dict(passed=round(c["claimed"] - c["held_amount"], 2), held=c["held_amount"],
                    passed_n=c["claimed_n"] - c["held_n"], reason=c["reason"])

    def superseded(self, key):
        """The original check's figures where the year-end reconciliation checked the month again."""
        c = self.cells[key]
        if not c["held_extra"]:
            return None
        extra = round(sum(a["amount"] for a in c["held_extra"]), 2)
        return dict(passed=round(c["claimed"] - c["held_amount"] - extra, 2),
                    held=round(c["held_amount"] + extra, 2),
                    passed_n=c["claimed_n"] - c["held_n"] - len(c["held_extra"]),
                    reason=c["reason"])

    def ytd(self):
        """The position each row states: the partner's scheme-year running total at that check."""
        out = {}
        run = {}
        for mo in MONTHS:
            for pi in sorted({k[0] for k in self.cells if k[1] == mo}):
                key = (pi, mo)
                sy = scheme_year(mo)
                base = run.get((pi, sy), (0.0, 0.0))
                m = self.monthly(key)
                cur = (round(base[0] + m["passed"], 2), round(base[1] + m["held"], 2))
                run[(pi, sy)] = cur
                sup = self.superseded(key)
                prior = None
                if sup is not None:
                    prior = (round(base[0] + sup["passed"], 2), round(base[1] + sup["held"], 2))
                out[key] = dict(current=cur, superseded=prior)
        return out

    # ---------------------------------------------------------------- the Treasury's run lines
    def run_lines(self):
        """One line per payment run and partner, as the archive exports it: the instruction's
        amounts, which for a consolidated instruction are the amounts of both lines it covers."""
        rows = []
        for key in sorted(self.cells):
            c = self.cells[key]
            if c["deferred"]:
                continue
            pi, mo = key
            heldset = {id(a) for a in c["held"]}
            gross = {1: 0.0, 2: 0.0}
            for a in c["awards"]:
                if id(a) in heldset:
                    continue
                gross[half(a["paid"].day)] = round(gross[half(a["paid"].day)] + a["amount"], 2)
            rec = {1: round(c["recovery"], 2), 2: 0.0}
            lines = [h for h in (1, 2) if gross[h] > 0 or rec[h] > 0]
            if c["consolidated"]:
                g = round(gross[1] + gross[2], 2)
                v = round(rec[1] + rec[2], 2)
                stated = {h: (g, v) for h in lines}
            else:
                stated = {h: (gross[h], rec[h]) for h in lines}
            nm = next_month(mo)
            for h in lines:
                run = dt.date(nm[0], nm[1], 8 if h == 1 else 22)
                g, v = stated[h]
                rows.append(dict(partner=pi, month=mo, half=h, run_date=run,
                                 value_date=run + dt.timedelta(days=2),
                                 run_ref="DR-%04d%02d-%d" % (nm[0], nm[1], h),
                                 gross=g, recovered=v, net=round(g - v, 2),
                                 true_gross=gross[h], true_recovered=rec[h],
                                 consolidated=c["consolidated"]))
        return rows

    # ---------------------------------------------------------------- the ask goldens, from truth
    def goldens(self):
        trans = {q: 0.0 for q in QUARTERS}
        held = {q: 0.0 for q in QUARTERS}
        claimed = {q: 0.0 for q in QUARTERS}
        recov = {q: 0.0 for q in QUARTERS}
        defer = {q: 0.0 for q in QUARTERS}
        reasons = {r: 0 for r in P.HOLD_REASONS}
        reasons["Not recorded"] = 0
        for key in sorted(self.cells):
            c = self.cells[key]
            q = quarter(key[1])
            m = self.monthly(key)
            claimed[q] = round(claimed[q] + c["claimed"], 2)
            held[q] = round(held[q] + m["held"], 2)
            if c["deferred"]:
                defer[q] = round(defer[q] + m["passed"] - c["recovery"], 2)
            else:
                trans[q] = round(trans[q] + m["passed"] - c["recovery"], 2)
            recov[q] = round(recov[q] + c["recovery"], 2)
            if m["held"] > 0:
                reasons[m["reason"] or "Not recorded"] += 1
        return dict(transferred={qlabel(q): round(trans[q], 2) for q in QUARTERS},
                    held={qlabel(q): round(held[q], 2) for q in QUARTERS},
                    claimed={qlabel(q): round(claimed[q], 2) for q in QUARTERS},
                    recovered={qlabel(q): round(recov[q], 2) for q in QUARTERS},
                    deferred={qlabel(q): round(defer[q], 2) for q in QUARTERS},
                    holds_by_reason=reasons)
