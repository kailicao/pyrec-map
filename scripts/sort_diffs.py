#!/usr/bin/env python3
"""Sort YREC's source files by how they changed between two commits, before the pages move to the later one.

    python3 scripts/sort_diffs.py <old checkout>/src ../yrec/src [--csv out.csv]
    (the old checkout: git -C ../yrec worktree add <folder> <old commit>; remove it afterwards)

A file is "mechanical" when its executable statements are the same once comments, case, spacing, continuations
and the statements that only declare (types, DIMENSION, COMMON, USE, IMPLICIT, SAVE, INCLUDE, MODULE wrappers)
are set aside; otherwise "substantive", with the number of executable statements added and removed.
"""
import csv, difflib, pathlib, re, sys

DECL = re.compile(r"^(IMPLICIT|REAL|INTEGER|DOUBLEPRECISION|DOUBLECOMPLEX|COMPLEX|LOGICAL|CHARACTER|DIMENSION|COMMON|USE|"
                  r"SAVE|INCLUDE|EXTERNAL|INTRINSIC|EQUIVALENCE|MODULE|ENDMODULE|CONTAINS|PRIVATE|PUBLIC|TYPE)")  # no \b: spaces are gone
ASSIGN = re.compile(r"^\w+(\([^=]*\))?=")  # REALX=1 is an assignment, not a declaration


def statements(path):
    """Executable statements, normalized: fixed form joined at continuations, comments dropped, upper case, no spaces."""
    out = []
    for raw in path.read_text(errors="replace").splitlines():
        if not raw.strip() or raw[:1] in "cC*!":
            continue
        line = raw.split("!", 1)[0] if "'" not in raw and '"' not in raw else raw
        if len(line) > 5 and line[5] not in " 0" and out and not line[:5].strip():  # a continuation line
            out[-1] += line[6:]
            continue
        if line.lstrip().startswith("&") and out:  # free-form-style continuation at column 6
            out[-1] += line.lstrip()[1:]
            continue
        out.append(line)
    norm = [re.sub(r"\s+", "", s.rstrip("&")).upper() for s in out]
    norm = [re.sub(r"^\d+", "", s) if not s.startswith(("GOTO", "DO")) else s for s in norm]  # labels
    return [s for s in norm if s and not (DECL.match(s) and not ASSIGN.match(s)) and not s.startswith("PARAMETER")]


def main():
    old, new = map(pathlib.Path, sys.argv[1:3])
    names = sorted({p.name for p in old.glob("*.f")} | {p.name for p in new.glob("*.f")})
    rows = []
    for n in names:
        a, b = old / n, new / n
        if not a.exists():
            rows.append((n, "added", 0, len(statements(b))))
        elif not b.exists():
            rows.append((n, "deleted", len(statements(a)), 0))
        elif a.read_bytes() == b.read_bytes():
            rows.append((n, "same", 0, 0))
        else:
            sa, sb = statements(a), statements(b)
            ops = difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes()
            rem = sum(i2 - i1 for t, i1, i2, _, _ in ops if t != "equal")
            add = sum(j2 - j1 for t, _, _, j1, j2 in ops if t != "equal")
            rows.append((n, "mechanical" if not (rem or add) else "substantive", rem, add))
    if "--csv" in sys.argv:
        with open(sys.argv[sys.argv.index("--csv") + 1], "w", newline="") as f:
            csv.writer(f).writerows([("file", "kind", "removed", "added")] + rows)
    kinds = {}
    for r in rows:
        kinds[r[1]] = kinds.get(r[1], 0) + 1
    print(kinds)


if __name__ == "__main__":
    main()
