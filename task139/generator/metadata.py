"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import common as K  # noqa: E402

SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
CVP = "Copperline Vehicle Protection"
ADM = CVP + ", Drive Plus administration system"
SOURCES = {
    K.REGISTER: (ADM + ", contract register as at 30 September 2026", "2026-10-01"),
    K.CROSSWALK: (ADM + ", contract number crosswalk from the March 2024 system migration", "2024-03-04"),
    K.CLAIMS: (ADM + ", claim payment lines, January 2019 to September 2026", "2026-10-01"),
    K.READINGS: (ADM + ", odometer readings from repair orders, CarLink reporters, maintenance uploads and the "
                 "Fareline mileage feed, January 2019 to September 2026", "2026-10-01"),
    K.CANCELS: (ADM + ", cancellation requests received, December 2024 to September 2026", "2026-10-01"),
    K.BORDEREAUX: (CVP + ", dealer remittance bordereaux received, November 2024 to September 2026", "2026-10-02"),
    K.RETURNS: ("Copperline's bank, ACH returns report on dealer remittances, 2025 to September 2026", "2026-10-01"),
    K.DEALERS: (CVP + ", approved dealer directory", "2026-09-15"),
    K.FACILITIES: (CVP + ", claims department repair facility directory", "2026-08-31"),
    K.RATE_MANUAL: (CVP + ", Drive Plus rate manual effective 1 January 2026", "2026-01-05"),
    K.TERMS: (CVP + ", Drive Plus contract terms, form DP-T 4.2", "2023-08-15"),
    K.AGREEMENT: (CVP + ", Fareline channel agreement summary of terms", "2026-03-12"),
    K.CLIP: ("Tarrant Mutual Casualty Company, contractual liability policy summary TMC-CL-2025-118", "2025-07-01"),
}
DISTRACTORS = ["target/" + K.CLIP, "target/" + K.FACILITIES]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task139", title="Whether Copperline renews its Fareline rideshare channel in 2027 at current rates, "
                                      "with the high-use surcharge, or lets it lapse",
                setting="A fictional Texas vehicle service contract obligor and administrator selling Drive Plus "
                        "contracts through dealers since 2019 and to a rideshare platform's drivers since April 2026, "
                        "whose rate manual decides the channel's renewal on the forecast lifetime loss ratio of its next "
                        "year's sales. The company, its partners, its dealers and its people are fictional, and every "
                        "record is synthetic.",
                as_of="2026-10-19", deliverables=[K.DECK, K.BOOK], distractor_files=DISTRACTORS,
                stated_inputs=["the 1 January 2027 renewal", "the rate manual's maximum high-use surcharge",
                               "records to 30 September 2026", "loss ratios to the nearest 5 per cent",
                               "dollar figures to the nearest dollar", "75,000"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
