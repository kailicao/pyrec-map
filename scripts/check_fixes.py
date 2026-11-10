"""check_fixes.py: every possible fix written as a diff in the notes applies cleanly to YREC and compiles.

For each ```diff block in a bug item ("## Bugs, by priority" of yrec-map/notes/*.md): `patch --dry-run` on a scratch
copy of yrec/src must succeed with no fuzz or offset, and each file it changes, patched, must pass
`gfortran -fsyntax-only` (modules compiled first, so that USE finds them). Run from the repository:
    python3 scripts/check_fixes.py ../yrec [scratch folder]"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path

yrec = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2] if len(sys.argv) > 2 else tempfile.mkdtemp()).resolve()
base = work / "base" / "src"
if base.exists():
    shutil.rmtree(base.parent)
shutil.copytree(yrec / "src", base)
FC = ["gfortran", "-ffixed-line-length-132", "-cpp", "-fsyntax-only", "-I."]
pending = sorted(base.glob("*_mod.f"))  # the modules' .mod files, once, in dependency order by retrying
for _ in range(6):
    left = [m for m in pending if subprocess.run(FC + [m.name], cwd=base, capture_output=True).returncode]
    if len(left) == len(pending):
        break
    pending = left
n, bad = 0, []
for p in sorted(Path("yrec-map/notes").glob("*.md")):
    s = p.read_text(encoding="utf-8")
    if "## Bugs, by priority" not in s:
        continue
    sec = re.split(r"\n## ", s.split("## Bugs, by priority", 1)[1])[0]
    for item in re.finditer(r"(?ms)^(\d+)\. \*\*\(.*?(?=^\d+\. \*\*\(|\Z)", sec):
        for k, blk in enumerate(re.findall(r"(?ms)^( *)```diff\n(.*?)^\1```", item.group(0)), 1):
            ind, body = blk
            diff = "\n".join(l[len(ind):] if l.startswith(ind) else l for l in body.rstrip("\n").split("\n")) + "\n"
            name = f"{p.stem}#{item.group(1)}" + (f" (diff {k})" if k > 1 else "")
            n += 1
            d = work / "case"
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(base.parent, d)
            r = subprocess.run(["patch", "-p1", "--dry-run", "-d", str(d)], input=diff, text=True, capture_output=True)
            msg = r.stdout + r.stderr
            if r.returncode or re.search(r"offset|fuzz", msg, re.I):
                bad.append(f"{name}: patch: {msg.strip().splitlines()[-1] if msg.strip() else r.returncode}")
                continue
            subprocess.run(["patch", "-p1", "-s", "-d", str(d)], input=diff, text=True, capture_output=True)
            for f in re.findall(r"(?m)^\+\+\+ b/src/(\S+)", diff):
                c = subprocess.run(FC + [f], cwd=d / "src", capture_output=True, text=True)
                if c.returncode:
                    bad.append(f"{name}: {f} does not compile: {c.stderr.strip().splitlines()[0] if c.stderr.strip() else ''}")
shutil.rmtree(work / "case", ignore_errors=True)
shutil.rmtree(work / "base", ignore_errors=True)
print(f"{n} diffs; {len(bad)} problems")
print("\n".join(bad))
sys.exit(1 if bad else 0)
