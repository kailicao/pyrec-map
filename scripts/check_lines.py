#!/usr/bin/env python3
"""Check the notes' links to lines of the code when the site moves to a later commit.

    python3 scripts/check_lines.py yrec OLD NEW [--fix]

The notes cite lines as links to the code on GitHub, [lines 120–130](https://github.com/yreclab/yrec/blob/<ref>/src/
main.f#L120-L130), the form the build writes so that the notes read on GitHub, or in the generator's form [[#L120]],
[[#L120-L130]] (the page's own file) or [[file.f#L88]], which the build rewrites. For every cited file
that changed between the commits OLD and NEW (in the clone's src/), each citation's lines are followed through
the diff: lines that are unchanged and only moved get their new numbers (written into the notes with --fix);
lines that changed or went are listed, for a person to check against the new code. A link's text is renumbered
with it when it is the one the page shows ("lines 120–130", "main.f, line 88"); the commit in the URLs follows the
site's --ref at the next build. Nothing else is changed.
"""
import difflib, pathlib, re, subprocess, sys

NOTES = pathlib.Path(__file__).resolve().parent.parent / "yrec-map" / "notes"
CITE = re.compile(r"\[\[([^\]|#]*)#L(\d+)(?:-L(\d+))?((?:\|[^\]]*)?)\]\]")
URL = re.compile(r"\[([^\[\]\n]*)\]\((https://github\.com/yreclab/yrec/blob/[^/]+/src/)([\w.]+)#L(\d+)(?:-L(\d+))?\)")


def shown(a, b, target, own):
    """A link's text as the page shows it: "lines 120–130", or "main.f, line 88" for another file."""
    s = f"line {a}" if b is None else f"lines {a}–{b}"
    return s if target == own else f"{target}, {s}"


def show(repo, commit, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{commit}:src/{path}"], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else None


def line_map(old, new):
    """{old line: new line} for the lines the diff keeps unchanged (1-based)."""
    out = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == "equal":
            out.update({i1 + k + 1: j1 + k + 1 for k in range(i2 - i1)})
    return out


def main(repo, old, new, fix=False):
    changed = set(subprocess.run(["git", "-C", repo, "diff", "--name-only", old, new, "--", "src"],
                                 capture_output=True, text=True).stdout.split())
    changed = {p[len("src/"):] for p in changed}
    maps, moved, broken = {}, 0, []
    for note in sorted(NOTES.glob("*.md")):
        own = note.name[:-3]
        text = note.read_text(encoding="utf-8")
        def one(m):
            nonlocal moved
            target = m.group(1) or own
            if target not in changed:
                return m.group(0)
            if target not in maps:
                a, b = show(repo, old, target), show(repo, new, target)
                maps[target] = line_map(a, b) if a is not None and b is not None else {}
            lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
            mp = maps[target]
            if all(k in mp for k in range(lo, hi + 1)) and mp[hi] - mp[lo] == hi - lo:
                if mp[lo] != lo:
                    moved += 1
                rng = f"L{mp[lo]}" + (f"-L{mp[hi]}" if m.group(3) else "")
                return f"[[{m.group(1)}#{rng}{m.group(4)}]]"
            broken.append(f"{note.name}: {m.group(0)} (lines changed in {target})")
            return m.group(0)
        def url(m):
            nonlocal moved
            target, lo, hi = m.group(3), int(m.group(4)), int(m.group(5) or m.group(4))
            if target not in changed:
                return m.group(0)
            if target not in maps:
                a, b = show(repo, old, target), show(repo, new, target)
                maps[target] = line_map(a, b) if a is not None and b is not None else {}
            mp = maps[target]
            if all(k in mp for k in range(lo, hi + 1)) and mp[hi] - mp[lo] == hi - lo:
                if mp[lo] != lo:
                    moved += 1
                b_old, b_new = (hi, mp[hi]) if m.group(5) else (None, None)
                text = m.group(1)
                if text == shown(lo, b_old, target, own):
                    text = shown(mp[lo], b_new, target, own)
                rng = f"L{mp[lo]}" + (f"-L{mp[hi]}" if m.group(5) else "")
                return f"[{text}]({m.group(2)}{target}#{rng})"
            broken.append(f"{note.name}: {m.group(0)} (lines changed in {target})")
            return m.group(0)
        new_text = URL.sub(url, CITE.sub(one, text))
        if fix and new_text != text:
            note.write_text(new_text, encoding="utf-8")
    print(f"{moved} citations moved with their lines" + (" (fixed)" if fix else " (run with --fix to renumber)"))
    print(f"{len(broken)} citations whose lines changed, to check by hand:")
    for b in broken:
        print("  " + b)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--fix"]
    main(*args[:3], fix="--fix" in sys.argv)
