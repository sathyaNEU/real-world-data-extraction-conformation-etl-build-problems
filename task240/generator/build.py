"""Write the task240 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "standard": "ssb_qs7_statistical_quality_standard.pdf",
    "note": "hrs27_weighting_note.docx",
    "close": "hrs27_fieldwork_closeout.docx",
    "codebook": "hrs27_codebook.xlsx",
    "households": "hrs27_households.csv",
    "members": "hrs27_household_members.csv",
    "weights": "hrs27_final_weights.csv",
    "issued": "hrs27_issued_sample.csv",
    "outcomes": "hrs27_outcomes_2027-09-30.csv",
    "calls": "hrs27_call_records.csv",
    "interviewers": "hrs27_interviewers.csv",
    "population": "ssb_population_estimates_2027-07-01.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["interviewers", "population"]
WORDS = {79: "Seventy-nine", 80: "Eighty", 78: "Seventy-eight"}


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    hh, mem, wt = R.households(), R.members(), R.weights()
    csv(hh, "households")
    csv(mem, "members")
    csv(wt, "weights")
    iss = R.issued()
    csv(iss, "issued")
    csv(R.outcomes(), "outcomes")
    csv(R.call_records(), "calls")
    iv = R.interviewers()
    csv(iv, "interviewers")
    csv(R.population(), "population")
    f = dict(issued="{:,}".format(len(iss)), psus="%d" % iss["psu"].nunique(), interviewers_word=WORDS[len(iv)])
    docs.standard(p("standard"))
    docs.weighting_note(p("note"), FILES, f)
    docs.close_out(p("close"), FILES, f)
    docs.codebook(p("codebook"))
    with open(p("dict"), "w") as fh:
        fh.write(docs.dictionary(FILES))
    with open(p("readme"), "w") as fh:
        fh.write(docs.readme(FILES))
    return dict(W=W, R=R, f=f)
