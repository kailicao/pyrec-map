"""namelist_viewer.py: one page per made-up case in bugs/namelists/, showing how its .nml1 and .nml2 differ from
the YREC case it starts from, as diffs in the site's style (the whole files are downloads from the page).

Each .nml1 names its YREC case on its second line ("! From YREC <commit>, <path>..."). Run from the repository:
    python3 scripts/namelist_viewer.py ../yrec bugs/namelists
then rebuild nothing: the pages link to the site's stylesheet and to the bug list (bugs/index.html)."""
import difflib, html, re, sys
from pathlib import Path

GH = "https://github.com/yreclab/yrec/blob/{ref}/{path}"
TITLE = "PyREC scaffolding (from YREC development, 7be4133)"
esc = html.escape


def header(lines):
    """The leading "!" lines: what the case is, what changed, which bugs it reaches."""
    out = []
    for ln in lines:
        if not ln.startswith("!"):
            break
        out.append(ln[1:].strip())
    return out


def tokens(t):
    return re.findall(r"\w+|\s+|[^\w\s]", t)


def shade(a, b):
    """Two lines with the tokens that differ wrapped (VS Code's word-level shading), or None if they share little."""
    ta, tb = tokens(a), tokens(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    if sm.ratio() < 0.5:
        return None
    oa, ob = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        xa, xb = esc("".join(ta[i1:i2])), esc("".join(tb[j1:j2]))
        if tag == "equal":
            oa.append(xa); ob.append(xb)
        else:
            oa.append(f"<span class='dw'>{xa}</span>" if xa else ""); ob.append(f"<span class='dw'>{xb}</span>" if xb else "")
    return "".join(oa), "".join(ob)


def diff(new, old, nhead=0):
    """The changed settings as a unified diff (three lines of context), in the site's diff style: new's head
    (its first nhead comment lines) left out, since the page shows it above; old given with the case's file
    names already renamed to the pair's, so that those are not changes. Returns (HTML, changed lines)."""
    body = [l.rstrip() for l in new[nhead:]]
    old = [l.rstrip() for l in old]
    sm = difflib.SequenceMatcher(None, old, body, autojunk=False)
    rows, changed = [], 0
    for group in sm.get_grouped_opcodes(3):
        a1, b1 = group[0][1] + 1, group[0][3] + 1 + nhead
        rows.append(f"<span class='hunk'>@@ YREC's line {a1}, this file's line {b1} @@</span>")
        for tag, i1, i2, j1, j2 in group:
            if tag == "equal":
                rows += [" " + esc(l) for l in body[j1:j2]]
                continue
            dels, adds = old[i1:i2], body[j1:j2]
            changed += max(len(dels), len(adds))
            pd, pa, start = {}, {}, 0
            for k, d in enumerate(dels):
                best = max(range(start, len(adds)), default=None,
                           key=lambda q: difflib.SequenceMatcher(None, tokens(d), tokens(adds[q])).ratio())
                w = shade(d, adds[best]) if best is not None else None
                if w:
                    pd[k], pa[best], start = w[0], w[1], best + 1
            rows += [f"<span class='del'>-{pd[k] if k in pd else esc(d)}</span>" for k, d in enumerate(dels)]
            rows += [f"<span class='add'>+{pa[k] if k in pa else esc(a)}</span>" for k, a in enumerate(adds)]
    return "\n".join(rows), changed


def page(name, d, yrec):
    n1 = (d / f"{name}.nml1").read_text(errors="replace").split("\n")
    m = re.match(r"!\s*From YREC (\w+), ([\w/+.-]+?)[,:]?(?:\s|$)", n1[1] if len(n1) > 1 else "")
    if not m:
        sys.exit(f"{name}.nml1: no '! From YREC <commit>, <path>' on its second line")
    ref, base = m.group(1), m.group(2)
    hd = header(n1)
    parts = []
    for ext in ("nml1", "nml2"):
        new = (d / f"{name}.{ext}").read_text(errors="replace").split("\n")
        old_p = Path(yrec) / f"{base}.{ext}"
        old = old_p.read_text(errors="replace").split("\n") if old_p.exists() else []
        old = [l.replace(Path(base).name, name) for l in old]  # file names that follow the case's name are not changes
        body, n = diff(new, old, len(header(new)))
        parts.append(f"<h2 id='{ext}'>{name}.{ext} <span class='muted'>({n} setting line{'s' if n != 1 else ''} changed from "
                     f"<a href='{GH.format(ref=ref, path=base)}.{ext}'>{esc(base)}.{ext}</a>; "
                     f"<a href='{name}.{ext}' download>download the whole file</a>)</span></h2>"
                     + (f"<pre class='diff'><code>{body}</code></pre>" if body else "<p class='muted'>Unchanged.</p>"))
    return "\n".join([
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        f"<title>{esc(name)} · {esc(TITLE)}</title><link rel='icon' type='image/svg+xml' href='../../logo.svg'>"
        "<link rel='stylesheet' href='../../style.css'>",
        "</head><body>",
        f"<header class='top'><a href='../../index.html'>{esc(TITLE)}</a><span class='muted'>/ "
        f"<a href='../index.html'>Suspected bugs</a> / {esc(name)}</span></header><main>",
        f"<h1>{esc(name)}</h1>",
        f"<p>A made-up case for checking suspected bugs by running YREC: <a href='{GH.format(ref=ref, path=base)}.nml1'>"
        f"<code>{esc(base)}</code></a> at {esc(ref)}, with the changes below as diffs against that case (removed lines red, added green, the words that differ "
        "shaded darker); besides these, only the head and the output names differ. Its head says what it is:</p>",
        "<pre class='doc'>" + esc("\n".join(hd)) + "</pre>",
        *parts, "</main></body></html>"])


if __name__ == "__main__":
    yrec, d = sys.argv[1], Path(sys.argv[2])
    for p in sorted(d.glob("*.nml1")):
        (d / f"{p.stem}.html").write_text(page(p.stem, d, yrec), encoding="utf-8")
        print(p.stem)
