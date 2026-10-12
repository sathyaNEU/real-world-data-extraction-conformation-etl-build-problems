"""Fill submission.md from the golden figures, so no figure in the write-up is typed by hand."""
import datetime as dt
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ["Parts & van stock", "Engineer attendance & punctuality", "Travel & routing", "Job duration & standards",
         "Customer access", "Other", "Rota & cover"]
PATCHES = ["Glasgow North & West", "Glasgow South & East", "Lanarkshire", "Ayrshire & Renfrewshire",
           "Edinburgh & Lothians", "Fife & Forth Valley"]


def render():
    f = json.loads((HERE / "golden_figures.json").read_text())
    fc, cr, cp, grid = f["family_counts"], f["credits_by_family"], f["complaints_by_family"], f["patch_family"]
    n = lambda x: "{:,}".format(x)
    by = sorted(ORDER, key=lambda k: -fc[k])
    fam_lines = "\n".join("   - %s: %s missed, %s pounds, %d complaints" % (k, n(fc[k]), n(cr.get(k, 0)), cp.get(k, 0))
                          for k in by)
    patch_lines = "\n".join("   - %s: %s" % (p, n(grid[p].get("Parts & van stock", 0))) for p in PATCHES)
    wd = dt.date.fromisoformat(f["worst_week"]["start"])
    fw = f["forward"]
    winter = set(fw["winter"]["rota_cover_by_month"].values())
    assert len(winter) == 1
    assert fw["answer"] == "Parts & van stock" and fw["ranking"][1][0] == "Engineer attendance & punctuality"
    vals = dict(parts=fc["Parts & van stock"], rota=fc["Rota & cover"], punct=fc["Engineer attendance & punctuality"],
                travel=fc["Travel & routing"], winter_rc=winter.pop(), family_lines=fam_lines,
                patch_lines=patch_lines, worst_day=wd.strftime("%-d %B %Y"), worst_n=f["worst_week"]["count"])
    txt = (HERE / "submission_template.md").read_text().format(**vals)
    assert "\u2014" not in txt
    (HERE.parent / "submission.md").write_text(txt, encoding="utf-8")


if __name__ == "__main__":
    render()
