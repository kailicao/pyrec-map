# PyREC scaffolding: notes for Claude

For a Claude session working on this site, Kaili Cao's (KC's) map of [YREC](https://github.com/yreclab/yrec), the Yale Rotating Evolution Code, and the start of its Python version, pyrec. Structural only: what the code does, and what each file's page says, is on the site itself (its sources in `notes/`); where the overhaul stands, for readers, is the overview (`yrec-map/notes/index.md`), kept current; the plan and KC's decisions are in this repository's README. The site lives in a project folder beside two other checkouts:

```text
<project folder>/
  yrec/        the code, a clone at the development branch's 7be4133 (read-only;
               the tag rp_1, 99ffc42, still in its history); only src/ is mapped
  pyrec/       the Python translation in the current structure (kailicao/pyrec):
               one pyrec/<stem>.py per Fortran file, shown under the routine it translates
  pyrec-map/   this repository
```

## The stage

KC overhauls a code in four stages (lsap-meth's `research/research-coding-style.md`, Overhauling a code: a documentation site for the old code, the documentation of the new code, the new code with benchmarks (same inputs, same outputs), and the paper). Stage 1 was completed at `rp_1` (every page reviewed once), moved to the development branch on Oct 27, 2026 (each page with its Python translation) and to a8a5950 on Oct 31 (to 7be4133 on Nov 9, after a round of the developers' bug fixes), with YREC's public documentation brought into the pages, notation from the YREC paper, files grouped by topic with a reading path, and a flowchart of each routine's calls. Stage 2 is drafted as a high-level design on one page (Nov 9, 2026): a `Model` holding the star's state and its history, with its physics and numerical methods as families of callables, each a Python base class, in Python with Numba (the earlier design of Oct 25, with modern-Fortran types and Python stubs, is in the history). No structural change to pyrec until KC has checked the whole translation.

**Sources.** Those of the README, Decisions, What a page may state: the code, its comments, YREC's public documentation ([yrec.readthedocs.io](https://yrec.readthedocs.io/en/latest/), its sources in `yrec/docs/`), the development branch's notes at the repository's root (`KNOWN_ISSUES.md`, `docs/archive/F90_CONVERSION_PLAN.md`, `REBASELINE_PROTOCOL.md`) and the YREC paper (in `yrec/`'s root); cite only these, and write anything else as a question for the experts.

## Where things are

- `yrec-map/`: the code as it is, one page per Fortran file (an outline in the margin; the text on the left: the explanation in sections, its questions in place, the suspected bugs, each routine's calls, the change log; the whole file's code on the right, Fortran, tidied or as in YREC, or Python), the home page's "Files by topic" (each topic's files, suspected bugs, and questions, in folded tables), `modules.html`, `callgraph.json` (every unit, its calls and modules); the glossary is `glossary.html`, at the site's root; sources: `yrec-map/notes/` (one `<file>.md` per source file; `index.md`, the overview shown on `index.html`; `glossary.md`, the glossary) and `yrec-map/reviews/` (each round's findings by group, and `settled.md`, points already settled, for reviewers only; each file starts with a `# Pages …` heading naming its pages, each file shown folded on `reviews.html`, its `## <file>` sections included, not on the file pages).
- `pyrec-map/`: the new design, one page (`pyrec-map/notes/overview.md`): the `Model`, its families against the home page's topics and today's routines, the files, performance, the route there, and the open questions, KC's tagged *[KC]*; `pyrec-map/reviews/round1-design.md`, the review of the earlier design, is kept but not shown.
- **The glossary** (`yrec-map/notes/glossary.md`): every module variable, under its current name in lower case (as pyrec writes it), with what it holds, its units, the paper's symbol and how its name reads; one `## <MODULE>` section per module, entries `- **`name`**: …`. The names stay as they are (README, Decisions, Variable names); each file page lists the ones its source uses. When a module gains or loses a variable, its entry follows.
- `scripts/`: `fortran_warnings.py` and `python_lint.py` (the compiler's warnings and ruff's findings marked on the pages), `check_lines.py` (the notes' links to lines, followed to a later commit), `sort_diffs.py` (the files sorted by how they changed between two commits, before a move), `check_returns.py` (pyrec's calls against the routines' returns and arguments), `annotate.py` (pyrec's type annotations, from YREC's declarations, and the blank lines around its docstrings); `logo.svg`, PyREC's logo (the pages' icon).
- The generator, `codemap.py`, and the briefs for each task live in KC's methods repository (lsap-meth, `research/`), which is private; the pages are committed built, so a clone opens in a browser without them.

## Rebuilding the site

After editing notes or reviews, from the project folder (the build writes over the pages and never touches the `notes/` and `reviews/` folders). The compiler's warnings and ruff's findings marked on the pages come from `scripts/fortran_warnings.py` (gfortran, compiling only, about 15 seconds; rerun when the code moves) and `scripts/python_lint.py` (rerun when pyrec changes):

```bash
cd pyrec-map && python3 scripts/fortran_warnings.py ../yrec/src yrec-map/warnings.json
python3 scripts/python_lint.py ../pyrec yrec-map/ruff.json
python3 ~/lsap-home/lsap-meth/research/codemap.py --root ../yrec/src \
  --out . --title "PyREC scaffolding (from YREC development, 7be4133)" --url https://github.com/yreclab/yrec \
  --ref 7be4133 --prefix src --lang fortran --readme ../yrec/README.md \
  --files-dir yrec-map --notes yrec-map/notes --reviews yrec-map/reviews \
  --pages "pyrec-map=A new design" --pages-src pyrec-map/notes --twin ../pyrec/pyrec \
  --suspected --warnings yrec-map/warnings.json --twin-warnings yrec-map/ruff.json --tidy --logo logo.svg --reviews-index-only \
  --banner "This site is under development and contains unvetted AI-generated content. It is not part of YREC's official documentation; please refer to the <a href='https://yrec.readthedocs.io/en/latest/'>YREC documentation</a>."
```

Fix every link to nothing it reports. The notice at the top of every page (`--banner`) is required: the repository is public, `kailicao/pyrec-map`, under KC's account so that it does not look signed off by YREC's developers (first `yrec-doc`; it spent Oct 26 in the yreclab organization). The build never deletes a page: pages of files deleted since `rp_1` stay until removed by hand.

**When the code moves to a later commit,** the notes' links to lines (`[[#L120-L130]]`, `[[file.f#L88]]`) are followed through the diff by `python3 scripts/check_lines.py ../yrec OLD NEW` (with `--fix` to renumber the lines that only moved); it lists the citations whose lines changed, to check by hand.

## The briefs

In lsap-meth's `research/research-coding-brief.md`, one section per task, for helpers and for Claude alike (`P` there is this repository): Stage 1, explanations (the notes' format and rules); review and revision; Stage 2, design; the generator (`codemap.py` and its options). Helpers get lean briefs that point to the saved files, and their cost is estimated before they start.
