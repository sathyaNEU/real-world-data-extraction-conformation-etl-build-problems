"""Independent verifier: recomputes the call, every graded figure and both asks from the shipped files alone and
compares them with figures.json. Exit 1 on any mismatch."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reader

FAIL = []


def ok(c, label):
    print(("PASS " if c else "FAIL ") + label)
    if not c:
        FAIL.append(label)


def main():
    T = os.path.join(os.path.dirname(HERE), "target")
    P = reader.load(T)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    pop = reader.region_pop(P)
    months, days = reader.presence(P)
    routine = lambda cid, reg: len(months[(cid, reg)]) >= 6 and days[(cid, reg)] >= 30
    q = reader.visitor_spend(P, lambda row: not routine(row[0], row[1]))
    pr = {r: sum(q[r]) / pop[r] for r in q}
    order = sorted(pr, key=lambda r: (-pr[r], pop[r]))
    names = P["names"]
    ok([names[r] for r in order[:5]] == f["call"], "the five regions recompute: " + ", ".join(order[:5]))
    ok(names[order[5]] == f["first_below"], "the first region below the line recomputes: " + order[5])
    ok(int(round(pr[order[4]])) - int(round(pr[order[5]])) == f["gap_per_resident"], "the gap recomputes")
    for r in pr:
        ok([int(round(x / 1000.0)) * 1000 for x in q[r]] == f["q_%s" % r], "quarterly visitor spending %s" % r)
        ok(int(round(sum(q[r]) / 1000.0)) * 1000 == f["total_%s" % r], "2026 visitor spending %s" % r)
        ok(int(round(pr[r])) == f["per_resident_%s" % r], "per resident %s" % r)
        ok(abs(pop[r] - f["erp_%s" % r]) < 0.01, "estimated resident population %s from the schedule" % r)
    # positive control: the statement-address route through the verifier's own readers files another set
    sa2r = P["sa2_region"]
    def home(sa2):
        if sa2 in P["shares"] and P["shares"][sa2]:
            return max(P["shares"][sa2], key=P["shares"][sa2].get)
        return sa2r.get(sa2, "IS")
    qd = reader.visitor_spend(P, lambda row: home(row[3]) != row[1])
    prd = {r: sum(qd[r]) / pop[r] for r in qd}
    od = sorted(prd, key=lambda r: (-prd[r], pop[r]))
    ok(set(od[:5]) != set(order[:5]), "positive control: the statement-address route files " + ", ".join(od[:5]))
    # the filed sentences the figures rest on, read back through the verifier's own PDF reader (positive controls)
    gt, ct = " ".join(P["guidelines_text"].split()), " ".join(P["closure_text"].split())
    ok("A visitor has the meaning the International Recommendations for Tourism Statistics 2008 give it." in gt
       and "raising each sampled card by its selection weight" in gt and "preliminary estimate for 30 June 2026" in gt,
       "the guidelines' section 4 reads back: the standard's visitor, the sample raised by selection weight, the 2026 population")
    ok("What remains of an agreement is its approved amount less what the program had paid on it by 31 December 2026." in ct
       and "Money a council returned to the program in 2026 because it did not spend it is added to the Fund's 2027 round." in ct,
       "the closure decision reads back: what remains of an agreement, and the unspent money added to the round")
    ok(len(P["rows"]) == f["sample_rows"] and len(P["weight"]) == f["sample_cards"], "the sample's rows and cards read back from the CSV and the register")
    A, B = reader.program_answers(P, link=True)
    for r in pr:
        ok(int(round(A[names[r]])) == f["remaining_%s" % r], "what remains of %s's open agreements" % r)
        ok(int(round(B[names[r]])) == f["unspent_%s" % r], "unspent money %s's councils returned" % r)
    total = 12_000_000 + sum(B.values()) - sum(A.values())
    ok(int(round(total)) == f["round_total"] and int(round(total / 5)) == f["grant_each"], "the round's total and each grant")
    Ac, Bc = reader.program_answers(P, link=False)
    ok(all(int(round(Ac[names[r]])) != f["remaining_%s" % r] for r in pr), "positive control: payments booked to the agreement they quote miss every region")
    print("\n%d failures" % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
