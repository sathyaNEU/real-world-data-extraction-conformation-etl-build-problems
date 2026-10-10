"""The shipped tables, built from the world: dockets, links, office actions, the production ledger, docket
transfers, the art unit table and the examiner roster. Row-level, in the production system's own layout."""
import datetime as dt
import random

import params as P

ACTION_COUNTS = {"1N": "1.25", "1R": "1.00", "DP": "0.75"}
FINAL_CODE = {"A": "NOA", "R": "REF", "B": "ABN"}


def iso(o):
    return dt.date.fromordinal(int(o)).isoformat() if o is not None else ""


def wd_between(R, lo, hi):
    """A weekday strictly inside (lo, hi), or None."""
    if hi - lo < 4:
        return None
    for _ in range(6):
        o = R.randint(lo + 1, hi - 1)
        if (o - 1) % 7 < 5:
            return o
    return None


def pay_period(o):
    fy = P.fy_of(o)
    lo = P.fy_bounds(fy)[0]
    return "FY%d-PP%02d" % (fy, min((o - lo) // 14 + 1, 26))


class Tables:
    def __init__(self, W):
        self.W = W
        R = random.Random(P.SEED + 11)
        n = W.n()
        # docket numbers: a serial per docketing year in docketing order, with the odd voided number
        order = sorted(range(n), key=lambda i: (W.start[i], R.random()))
        self.no = [None] * n
        serial = {}
        for i in order:
            fy = P.fy_of(W.start[i])
            s = serial.get(fy, 100000) + (2 if R.random() < 0.004 else 1)
            serial[fy] = s
            self.no[i] = "%02d-%06d" % (fy % 100, s)
        lo = P.fy_bounds(P.SHIP_FROM_FY)[0]
        self.ship = [i for i in order if W.start[i] >= lo]
        self.shipset = set(self.ship)

    # ------------------------------------------------------------------------------------------- dockets
    def dockets(self):
        W, S = self.W, self.W.S
        rows = []
        for i in self.ship:
            au = W.au_dock[i]
            tg = S.old_group[au] if W.start[i] < P.RECUT else S.cur_group[au]
            rows.append({"docket_no": self.no[i], "docketed_on": iso(W.start[i]), "art_unit": W.au_close[i],
                         "tg": tg, "examiner_id": W.ex_close[i], "closed_on": iso(W.close[i]),
                         "end_code": W.status[i]})
        return rows

    def links(self):
        W = self.W
        rows = []
        for i in self.ship:
            if W.kind[i] == 0:
                continue
            rows.append({"parent_docket": self.no[W.parent[i]], "child_docket": self.no[i],
                         "link_type": {1: "CX", 2: "CN", 3: "DV"}[W.kind[i]], "linked_on": iso(W.start[i])})
        rows.sort(key=lambda r: (r["linked_on"], r["child_docket"]))
        return rows

    def transfers(self):
        W = self.W
        rows = []
        for i in self.ship:
            if W.xfer[i] is not None:
                rows.append({"docket_no": self.no[i], "transferred_on": iso(W.xfer[i]), "from_au": W.au_dock[i],
                             "to_au": W.au_close[i]})
        rows.sort(key=lambda r: (r["transferred_on"], r["docket_no"]))
        return rows

    # ------------------------------------------------------------------------------------- office actions
    def actions(self):
        """(docket index, served ordinal, code, examiner, credit class or '') for every action on a shipped
        docket served by the extract."""
        W = self.W
        X = P.EXTRACT
        R = random.Random(P.SEED + 23)
        acts = []
        for i in self.ship:
            ex_at = (lambda o, i=i: W.ex_dock[i] if (W.xfer[i] is None or o < W.xfer[i]) else W.ex_close[i])
            first_cls = "1R" if (W.kind[i] == 1 and W.route[i] == 1) else "1N"
            if W.twin[i]:
                T = P.TWIN
                if W.kind[i] == 0:
                    seq = [(T["fa"], "EXR", first_cls), (T["mid"], "EXR", ""), (T["ref"], "REF", "DP")]
                else:
                    seq = [(T["succ_fa"], "EXR", first_cls), (T["noa"], "NOA", "DP"), (T["grant"], "GRT", "")]
                for d, c, cl in seq:
                    acts.append((i, d.toordinal(), c, W.ex_dock[i], cl))
                continue
            fa, dec = W.fa[i], W.dec[i]
            nmid = W.nmid[i]
            mids = []
            for _ in range(nmid):
                o = wd_between(R, fa + 20, dec - 20)
                kind_draw = R.random()
                if o is not None:
                    mids.append((o, "ITV" if kind_draw < 0.18 else "EXR"))
            if fa <= X:
                acts.append((i, fa, "EXR", ex_at(fa), first_cls))
            for o, c in sorted(set(mids)):
                if o <= X and o != fa:
                    acts.append((i, o, c, ex_at(o), ""))
            if dec <= X:
                acts.append((i, dec, FINAL_CODE[W.code[i]], ex_at(dec), "DP"))
                if W.code[i] == "A" and W.grant[i] is not None and W.grant[i] <= X:
                    acts.append((i, W.grant[i], "GRT", ex_at(W.grant[i]), ""))
        acts.sort(key=lambda a: (a[1], self.no[a[0]], {"EXR": 0, "ITV": 1, "NOA": 2, "REF": 2, "ABN": 2,
                                                         "GRT": 3}[a[2]]))
        self.acts = acts
        self.action_id = ["A%09d" % (310000000 + k * 3 + (k % 3)) for k in range(len(acts))]
        return acts

    def action_rows(self):
        """Column lists (the action history is too long for one dict per row)."""
        return {"action_id": list(self.action_id), "docket_no": [self.no[a[0]] for a in self.acts],
                "action_code": [a[2] for a in self.acts], "served_on": [iso(a[1]) for a in self.acts]}

    def ledger_rows(self):
        rows = []
        for aid, a in zip(self.action_id, self.acts):
            if a[4]:
                rows.append({"pay_period": pay_period(a[1]), "examiner_id": a[3], "action_id": aid,
                             "credit_class": a[4], "counts": ACTION_COUNTS[a[4]]})
        rows.sort(key=lambda r: (r["pay_period"], r["examiner_id"], r["action_id"]))
        for k, r in enumerate(rows):
            r["credit_id"] = "C%08d" % (20000000 + k)
        return rows

    # ----------------------------------------------------------------------------------- reference tables
    def art_unit_rows(self):
        S = self.W.S
        rows = []
        for au in sorted(S.aus):
            if au in S.moved:
                rows.append({"art_unit": au, "tg": S.old_group[au], "tg_name": P.GROUP_NAMES[S.old_group[au]],
                             "valid_from": "2005-10-01", "valid_to": "2023-09-30"})
                rows.append({"art_unit": au, "tg": S.cur_group[au], "tg_name": P.GROUP_NAMES[S.cur_group[au]],
                             "valid_from": "2023-10-01", "valid_to": ""})
            else:
                rows.append({"art_unit": au, "tg": S.cur_group[au], "tg_name": P.GROUP_NAMES[S.cur_group[au]],
                             "valid_from": "2005-10-01", "valid_to": ""})
        return rows

    def roster_rows(self):
        S = self.W.S
        R = random.Random(P.SEED + 31)
        rows = []
        for au in sorted(S.aus):
            for e in S.examiners[au]:
                home = S.home[e]
                rows.append({"examiner_id": e, "grade": R.choice(["Examiner", "Examiner", "Senior Examiner",
                                                                  "Senior Examiner", "Principal Examiner"]),
                             "home_art_unit": home, "tg": S.cur_group[home],
                             "fte": R.choice(["1.0", "1.0", "1.0", "1.0", "0.8", "0.6"]),
                             "on_roster_since": iso(R.randint(dt.date(1996, 1, 8).toordinal(),
                                                              dt.date(2015, 6, 1).toordinal()))})
        rows.sort(key=lambda r: r["examiner_id"])
        return rows
