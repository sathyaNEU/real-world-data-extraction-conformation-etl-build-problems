"""How the survey platform and the scanning bureau write their exports: each question under the tag the survey team
gave it when the questionnaire was built (tc01 to tc12 for the index items, en01 to en06 for the engagement questions)
and each answer as its label. records.py keeps the systems' internal codes; this module writes them out and reads them
back, so the analysis and the shipped-bytes check run on the same records."""
import params as P
import records as RC

TAGS = ["staff_group", "tenure"] + ["tc%02d" % k for k in range(1, 13)] + ["en%02d" % k for k in range(1, 7)]
ONLINE_TAG = dict(zip(RC.ONLINE_Q, TAGS))
PAPER_TAG = dict(zip(RC.PAPER_Q, TAGS))
SCALE = {"1": "Strongly disagree", "2": "Disagree", "3": "Neither agree nor disagree", "4": "Agree",
         "5": "Strongly agree", "6": "Don't know"}
GROUP = {str(k + 1): g for k, g in enumerate(P.STAFF_GROUPS)}
YEARS = {"1": "Less than a year", "2": "One to two years", "3": "Three to five years", "4": "Six to ten years",
         "5": "More than ten years"}


def labels(tag, paper):
    """the label each code of a question is written as; the bureau adds its own marks for a form"""
    if tag == "staff_group":
        m = dict(GROUP)
    elif tag == "tenure":
        m = dict(YEARS)
    else:
        m = dict(SCALE)
    if paper:
        m["9"] = "No mark"
        if tag not in ("staff_group", "tenure"):
            m["8"] = "More than one box"
    return m


def platform(A):
    """the platform's long export: question tag and answer label (blank where the question was left unanswered)"""
    out = A.copy()
    tags = out["question"].map(ONLINE_TAG)
    assert tags.notna().all()
    lab = []
    for t, v in zip(tags, out["response"]):
        lab.append("" if v == "" else labels(t, False)[v])
    out["question"] = tags.values
    out["response"] = lab
    return out


def platform_codes(A):
    """the platform's export read back to its internal codes"""
    out = A.copy()
    back = {v: k for k, v in ONLINE_TAG.items()}
    codes = []
    for t, v in zip(out["question"], out["response"]):
        inv = {lab: c for c, lab in labels(t, False).items()}
        codes.append("" if v == "" else inv[v])
    out["question"] = out["question"].map(back).values
    out["response"] = codes
    return out


def bureau(paper):
    """the bureau's wide file: one column per mark field under its tag, each mark as its label"""
    out = paper.rename(columns=dict(PAPER_TAG, scanned_at="scanned_at_local"))
    for t in TAGS:
        m = labels(t, True)
        out[t] = out[t].map(m)
        assert out[t].notna().all(), t
    return out


def bureau_codes(paper):
    """the bureau's file read back to its codes and its original column names"""
    out = paper.copy()
    for t in TAGS:
        inv = {lab: c for c, lab in labels(t, True).items()}
        out[t] = out[t].map(inv)
        assert out[t].notna().all(), t
    return out.rename(columns=dict({v: k for k, v in PAPER_TAG.items()}, scanned_at_local="scanned_at"))
