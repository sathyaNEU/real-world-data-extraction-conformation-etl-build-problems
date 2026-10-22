"""metadata.json: the files with source, date and licence, the distractors, the deliverables."""
import json

import pack as P

DATES = {"program": "2027-02-12", "dictionary": "2027-02-09", "schedule": "2024-11-18", "piezo": "2027-02-05",
         "bending": "2027-02-05", "stations": "2027-02-05", "tickets": "2027-02-06", "citations": "2027-02-08",
         "entries": "2027-02-04", "plazas": "2027-02-04", "pavement": "2026-07-22", "bridges": "2026-12-01"}
SOURCE = {"program": "Office of Freight Operations", "dictionary": "Office of Freight Operations, WIM program",
          "schedule": "Board of the Authority", "piezo": "WIM program, piezoelectric station controllers",
          "bending": "WIM program, bending-plate vendor software", "stations": "WIM program",
          "tickets": "enforcement unit, West and East Scale Houses", "citations": "enforcement unit citation log",
          "entries": "toll back office", "plazas": "toll back office", "pavement": "pavement management section",
          "bridges": "structures section, from the state's bridge inventory"}


def write(path, n):
    files = [dict(file=fn, source="Calderwick Turnpike Authority (fictional), %s; synthetic records" % SOURCE[k],
                  date=DATES[k], license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(P.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task478", title="Calderwick Turnpike virtual weigh station sections, 2027 contract",
                setting="A fictional toll road authority in an unnamed U.S. state; every record is synthetic.",
                as_of="2027-02-12", files=files,
                distractor_files=[P.FILES["pavement"], P.FILES["bridges"]],
                distractors=[dict(file=P.FILES["pavement"], why="the 2026 pavement condition survey by section: "
                                  "damage heavy trucks do, not the share of them over the gross limit the program "
                                  "sites on"),
                             dict(file=P.FILES["bridges"], why="posted bridges on the crossing roads near the "
                                  "interchanges: where an overweight truck may not go off the turnpike, not how many "
                                  "run on it")],
                deliverables=["ctpa_vws_sections_2027.xlsx", "ctpa_section_overweight_2026.csv",
                              "ctpa_overweight_share_2026.svg"],
                stated_inputs=["80,000 lb", "five of twelve sections", "calendar 2026"])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
