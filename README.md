# PyREC scaffolding, from YREC's development branch

**This site is under development and contains unvetted AI-generated content. It is not part of YREC's official documentation; please refer to the [YREC documentation](https://yrec.readthedocs.io/en/latest/).**

A map of [YREC](https://github.com/yreclab/yrec), the Yale Rotating Evolution Code, read at its development branch's commit 7be4133 (fetched Nov 9, 2026), built as scaffolding for developing PyREC, a Python version of the code. It is Kaili Cao's working material, drafted with AI (Claude); YREC's developers have not vetted it.

- **`yrec-map/`, the code as it is.** One page per source file in `src/`: what each routine does, its calls and modules, questions for the code's experts, and each routine's Python translation beside its Fortran (from the [pyrec](https://github.com/kailicao/pyrec) repository, as the translation proceeds).
- **The glossary.** Every module variable under its current name, in lower case as pyrec writes it, with what it holds, its units and how its name reads; each file page lists the variables it uses. Some of YREC's names are not intuitive (short names from the days of Fortran 77, types implied by the first letter), so they are annotated rather than renamed.
- **`pyrec-map/`, the new design.** One page: the structure the code is meant to have, at a high level, stable against fixes to the Fortran. A draft.
- **Reviews.** The reviews of the pages, shown folded at the end of the pages they concern.

Open `index.html` in a browser, or the site online, at [kailicao.github.io/pyrec-map](https://kailicao.github.io/pyrec-map/), which shows the last pushed version. Each folder holds its sources (`notes/`, `reviews/`) beside the pages generated from them; nothing in YREC was run. `CLAUDE.md` holds the notes for an AI assistant working on the site: its layout and how it is rebuilt.

## Where it stands

The site follows the four stages in which Kaili Cao overhauls a code: a documentation site for the old code, the documentation of the new code, the new code with benchmarks (same inputs, same outputs), and the paper. The first is complete: Every page has an explanation; the pages of the release `rp_1` were reviewed once, and the 86 added on the development branch (its 85 modules and `version.f`) are not yet reviewed. The second is drafted as a high-level design on one page (Nov 9, 2026): a `Model` holding the star's state and its history, with its physics and numerical methods as families of callables, each a Python base class, in Python with Numba; the earlier, detailed design (modern-Fortran types and Python stubs) is in this repository's history. The overview on `index.html` says more, for readers: how to read the site, a reading path and where the overhaul stands.

## Decisions

Kaili Cao's choices, which may change in light of feedback.

- **Where the site's history lives.** This repository (first commit Oct 25, 2026), public since Oct 27, under Kaili Cao's account so that it does not look signed off by YREC's developers, with a notice on every page; the Python translation is a repository of its own, [kailicao/pyrec](https://github.com/kailicao/pyrec). Served by GitHub Pages, at kailicao.github.io/pyrec-map.
- **What it tracks.** The sources (each part's `notes/` and `reviews/`) and the built pages, so that a clone opens in a browser without the generator, which is not public. Might change: if the generator is published, the pages could be left to a build step.
- **Variable names.** YREC's names are kept, in lower case, and explained in the glossary rather than renamed (Oct 31, 2026); the glossary is also the inventory for designing new data structures.
- **What a page may state.** What the code, its comments, YREC's documentation (yrec.readthedocs.io, and the development branch's notes in the repository: `KNOWN_ISSUES.md`, `docs/archive/F90_CONVERSION_PLAN.md`, `REBASELINE_PROTOCOL.md`) or the YREC paper say, and what follows from the code; anything else is a question for the experts (Oct 31, 2026).
- **Licensing.** Open. The code has no license file, and the pages show its source. Might change: talks with YREC's developers and collaborators.
- **The route to a Python version.** Fortran 77 in the old structure, then Python in the old structure (plain Python first; Numba kernels behind plain-Python wrappers later, for the numerics-heavy routines), then Python in the new structure (Numba by default for speed), then modern Fortran for the parts that need more speed. Might change: pyrec's speed in practice, YREC's developers' plans (their development branch already uses modules), and the experts' feedback.
